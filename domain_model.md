# Streamy Core Domain Structural Architecture

## Advanced Object-Oriented System Entity Specifications
This structural document acts as the definitive blueprint for the Streamy runtime system. It establishes core hierarchies, lifecycle coupling, and cardinality rules, dictating how object models must inherit attributes and clear space allocations out of memory.

## 2. Comprehensive Production Class Diagram
The advanced structural design schematic below details all inheritance, composition, and aggregation parameters for the Streamy domain engine:

```mermaid
classDiagram
    direction TB
    class Title {
        <<abstract>>
        +String name
        +int releaseYear
        +playMedia() Boolean
    }
    class Film {
        +int lengthMinutes
    }
    class TVShow {
        +int seasonsCount
    }
    class Season {
        +int seasonNumber
    }
    class Episode {
        +int episodeNo
        +int runtime
    }
    class User {
        +String email
        +String passwordHash
    }
    class Subscription {
        +Date startDate
        +Date expiryDate
    }
    class WatchHistory {
        +Date watchedAt
    }

    Film --|> Title : extends
    TVShow --|> Title : extends
    TVShow "1" *-- "0..*" Season : owns
    Season "1" *-- "0..*" Episode : contains
    User "1" *-- "1" Subscription : has
    User "1" -- "0..*" WatchHistory : records
    WatchHistory "0..*" -- "1" Title : references
