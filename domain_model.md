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
        +String episodeTitle
        +int durationSeconds
    }
    class Genre {
        +String genreName
    }
    class Actor {
        +String fullName
    }
    class Review {
        +int ratingStars
        +String reviewText
    }

    Film --|> Title : extends
    TVShow --|> Title : extends

    TVShow "1" *-- "0..*" Season : owns
    Season "1" *-- "1..*" Episode : contains

    Title "0..*" -- "1..*" Genre : categorized_under
    Title "1" *-- "0..*" Actor : features
    Title "1" -- "0..*" Review : receives
