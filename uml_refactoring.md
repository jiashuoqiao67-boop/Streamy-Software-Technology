# Streamy UML Class Refactoring: Code Smells, Request Objects and Interface Realization

## Refactoring Analysis
This document models code-level class structures, properties, method signatures, visibility and dependencies with Mermaid class diagrams. It traces two refactoring passes over a tightly coupled user-registration flow: first removing a **Data Clump** by introducing a request object, then inverting the dependency through an interface abstraction (`..|>` realization). The final section applies the same techniques to the Streamy codebase itself.

Visibility convention: `-` private, `+` public, `#` protected. Generics are written with tildes, e.g. `List~User~`. A dashed open arrow `..>` marks a dependency; a dashed hollow triangle `..|>` marks an interface realization.

## 1. Initial Tightly Coupled Classes (Before)
The first diagram shows the original tightly coupled implementation. `string email` and `string username` are passed together across multiple signatures, and the controller depends directly on the concrete service.

```mermaid
---
title: Initial Tightly Coupled Classes
---
classDiagram
    class UserController {
        -CreateUserService _createUserService
        +UserController(CreateUserService createUserService)
        +Create(string email, string username) User
    }

    class CreateUserService {
        -UserModel _userModel
        -SendWelcomeEmailService _sendWelcomeEmailService
        -Kafka _kafka
        +CreateUserService(UserModel um, SendWelcomeEmailService es, Kafka k)
        +Call(string email, string username) User
        -CheckActiveUsers(List~User~ users) bool
    }

    class UserModel {
        +FindUsersByEmail(string email) List~User~
        +CreateUser(string email, string username) User
    }

    class User {
        +int UserId
        +string Username
        +string Email
    }

    class SendWelcomeEmailService {
        +Call(string email, string username) bool
    }

    class Kafka {
        +PublishUserCreatedEvent(string email, string username) bool
    }

    UserController ..> CreateUserService: depends on
    CreateUserService ..> UserModel: depends on
    UserModel ..> User: depends on
    CreateUserService ..> SendWelcomeEmailService: depends on
    CreateUserService ..> Kafka: depends on
```

## 2. Refactored Data Clumps (Request Object)
The repeated `email + username` pair is a Data Clump. A dedicated `CreateUserRequest` class encapsulates the registration data and self-validates. Downstream services consume the domain entity `User` instead of raw primitives.

```mermaid
---
title: Refactored Data Clumps
---
classDiagram
    class UserController {
        -CreateUserService _createUserService
        +UserController(CreateUserService createUserService)
        +Create(string email, string username) User
    }

    class CreateUserRequest {
        +string Email
        +string Username
        +Validate() bool
    }

    class CreateUserService {
        -UserModel _userModel
        -SendWelcomeEmailService _sendWelcomeEmailService
        -Kafka _kafka
        +CreateUserService(UserModel um, SendWelcomeEmailService es, Kafka k)
        +Call(CreateUserRequest createUserRequest) User
        -CheckActiveUsers(List~User~ users) bool
    }

    class UserModel {
        +FindUsersByEmail(string email) List~User~
        +CreateUser(string email, string username) User
    }

    class User {
        +int UserId
        +string Username
        +string Email
    }

    class SendWelcomeEmailService {
        +Call(User user) bool
    }

    class Kafka {
        +PublishUserCreatedEvent(User user) bool
    }

    UserController ..> CreateUserRequest: depends on
    UserController ..> CreateUserService: depends on
    CreateUserService ..> UserModel: depends on
    UserModel ..> User: depends on
    CreateUserService ..> SendWelcomeEmailService: depends on
    CreateUserService ..> Kafka: depends on
```

## 3. Final Decoupled Architecture (Interface Realization)
`UserController` previously depended directly on the concrete `CreateUserService`. Following the Dependency Inversion Principle, an `ICreateUserService` interface contract is introduced: the controller depends on the interface (`..>`), and the concrete service realizes it (`..|>`).

```mermaid
---
title: Final Decoupled Architecture
---
classDiagram
    class UserController {
        <<Class>>
        -ICreateUserService _createUserService
        +UserController(ICreateUserService createUserService)
        +Create(string email, string username) User
    }

    class CreateUserRequest {
        <<Class>>
        +string Email
        +string Username
        +Validate() bool
    }

    class ICreateUserService {
        <<Interface>>
        +Call(CreateUserRequest createUserRequest) User
    }

    class CreateUserService {
        <<Class>>
        -UserModel _userModel
        -SendWelcomeEmailService _sendWelcomeEmailService
        -Kafka _kafka
        +CreateUserService(UserModel um, SendWelcomeEmailService es, Kafka k)
        +Call(CreateUserRequest createUserRequest) User
        -CheckActiveUsers(List~User~ users) bool
    }

    class UserModel {
        <<Class>>
        +FindUsersByEmail(string email) List~User~
        +CreateUser(string email, string username) User
    }

    class User {
        <<Class>>
        +int UserId
        +string Username
        +string Email
    }

    class SendWelcomeEmailService {
        <<Class>>
        +Call(User user) bool
    }

    class Kafka {
        <<Class>>
        +PublishUserCreatedEvent(User user) bool
    }

    UserController ..> CreateUserRequest: depends on
    UserController ..> ICreateUserService: depends on
    CreateUserService ..|> ICreateUserService: implements

    CreateUserService ..> UserModel: depends on
    UserModel ..> User: depends on
    CreateUserService ..> SendWelcomeEmailService: depends on
    CreateUserService ..> Kafka: depends on
```

### Rendering Verification
- Stereotypes `<<Class>>` and `<<Interface>>` render centered at the top of their boxes.
- The relationship between `CreateUserService` and `ICreateUserService` displays as a realization arrow (`..|>`).
- `UserController` has no direct dependency line to the concrete `CreateUserService`.

## 4. Challenge: Refactored Architecture Applied to the Streamy Codebase

### Identified Code Smells
1. **Tight coupling / missing abstraction**: `Season` composes the concrete `Episode`, and `Title` holds concrete `Genre`, `Actor` and `Review` lists. High-level content classes are hard-bound to low-level concrete types; adding a new playable unit would require changing `Season`.
2. **Long parameter list / Data Clump**: creating a title passes a long list of raw parameters (`name`, `releaseYear`, `genres`, `actors`, `reviews`), and `Actor.fullName` stores first and last name as a single raw string.

### After Refactored Architecture
- `ITitleRepository` abstracts persistence; `TitleService` depends on the interface, and `TitleRepository` realizes it.
- `CreateTitleRequest` encapsulates the creation parameters and validates them.
- `IContentUnit` abstracts playable units; `Episode` realizes it, and `Season` depends on the abstraction rather than the concrete episode.
- `PersonName` is a value object replacing the raw name string.

```mermaid
---
title: Streamy Refactored Architecture (After)
---
classDiagram
    class ITitleRepository {
        <<Interface>>
        +findByTitleId(int titleId) Title
        +save(Title title) void
    }
    class TitleRepository {
        <<Class>>
        -List~Title~ _titles
        +findByTitleId(int titleId) Title
        +save(Title title) void
    }
    class TitleService {
        <<Class>>
        -ITitleRepository _repository
        +TitleService(ITitleRepository repository)
        +createTitle(CreateTitleRequest request) Title
    }
    class CreateTitleRequest {
        <<Class>>
        +String name
        +int releaseYear
        +List~String~ genreNames
        +List~PersonName~ cast
        +Validate() bool
    }
    class Title {
        <<abstract>>
        #String name
        #int releaseYear
        #List~Genre~ genres
        #List~Actor~ actors
        #List~Review~ reviews
        +playMedia() bool
    }
    class Film {
        <<Class>>
        +int lengthMinutes
    }
    class TVShow {
        <<Class>>
        +int seasonsCount
        +List~Season~ seasons
    }
    class Season {
        <<Class>>
        +int seasonNumber
        +List~IContentUnit~ contentUnits
    }
    class IContentUnit {
        <<Interface>>
        +getRuntimeSeconds() int
    }
    class Episode {
        <<Class>>
        +String episodeTitle
        +int durationSeconds
    }
    class Genre {
        <<Class>>
        +String genreName
    }
    class Actor {
        <<Class>>
        +PersonName name
    }
    class PersonName {
        <<Class>>
        +String firstName
        +String lastName
        +fullName() String
    }
    class Review {
        <<Class>>
        +int ratingStars
        +String reviewText
    }

    TitleRepository ..|> ITitleRepository : implements
    TitleService ..> ITitleRepository : depends on
    TitleService ..> CreateTitleRequest : depends on

    Film --|> Title : extends
    TVShow --|> Title : extends
    Episode ..|> IContentUnit : implements
    Season o-- IContentUnit : groups
    Actor ..> PersonName : depends on

    Title o-- Genre : categorized_under
    Title o-- Actor : features
    Title o-- Review : receives
```
