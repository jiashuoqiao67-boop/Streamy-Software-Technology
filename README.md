## Streamy Application Engineering Development Lifecycle
To guarantee systematic software tracking across the implementation lifespan of **Streamy**, our individual developer pipeline follows the structured iterative gate review framework illustrated below.

```mermaid
---
title: Streamy Iterative SDLC Blueprint
---
flowchart TD
    A[Inception Abstract Created] --> B[SRS Requirements Compiling]
    subgraph SpecPhase [1. Requirements Specification Block]
    end
    subgraph DesignPhase [2. UML Architectural Modeling]
        B --> C[Draft System Border Graphs]
        C --> D[Construct Advanced Class Models]
    end
    subgraph ValidationGate [3. Verification Gatekeeper Loop]
        D --> E{Does Architecture Match Code Specs?}
        E -- No: Refactor Blueprint --> B
    end
    subgraph ProductionPhase [4. Python Construction Layer]
        E -- Yes: Pass Gate --> F[Compile Python Class Skeletons]
        F --> G[Implement Internal Class Logic]
    end
    E:::decisionStyle
    classDef decisionStyle fill:#f9f,stroke:#333,stroke-width:2px;
```

## System Architecture Overview (Native Mermaid)

This repository uses Mermaid for architecture and domain documentation.
The diagram below is rendered natively by GitHub from a fenced `mermaid` code block; changes to the block re-render automatically on commit.

```mermaid
flowchart LR
    Client[Web Client] -->|HTTPS| API[API Gateway]
    API --> Service[Listing Service]
    Service --> DB[(Database)]
```

## Diagram Orientation (Direction Control)

Flowchart and class-diagram layout can be controlled directly with a direction directive:

- `TB` / `TD`: Top-to-bottom (default)
- `LR`: Left-to-right
- `RL`: Right-to-left
- `BT`: Bottom-to-top

For class diagrams, place the `direction` keyword inside the diagram body. The example below uses `direction LR`:

```mermaid
classDiagram
    direction LR
    class Title {
        +String name
        +int releaseYear
    }
    class Genre {
        +String genreName
    }
    Title "0..*" --> "1..*" Genre : categorized_under
```

## C4 System Context Diagram

The system-level context view shows the Streamy platform and its relationships to its users and external supporting systems:

```mermaid
flowchart LR
    User(["Premium Member<br/>[Person]"]) --> Streamy["Streamy Video Streaming Platform<br/>[Software System]<br/>Web & Mobile apps, Listing Service"]
    Streamy --> TitleSvc["Title Service<br/>[External System]"]
    Streamy --> ReviewSvc["Review Service<br/>[External System]"]
    Streamy --> SearchSvc["Search Service<br/>[External System]"]
```

## Fallback for Platforms Without Native Mermaid Support

On platforms that do not render Mermaid natively (e.g. legacy wikis or standard static sites), keep an exported static image and store the editable diagram source in an HTML comment directly below it, so the source is not lost when the architecture changes later:

![Architecture Diagram](./images/architecture.png)
<!--
Editable Diagram Source: a flowchart TD with Service A connected to Service B.
Keep the raw Mermaid source here so it is not lost when the architecture changes.
-->
