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
    class Series {
        +int seasonsCount
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

    Title <|-- Film
    Title <|-- Series
    Series o-- Episode
    User *-- Subscription
    User -- WatchHistory
    WatchHistory -- Title
