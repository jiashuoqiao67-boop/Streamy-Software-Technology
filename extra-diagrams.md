# Lab Extra Diagrams

## 1. Listing Service C4 Component Diagram
```mermaid
---
title: "Listing Service C4 Model: Component Diagram"
---
flowchart TD
    classDef container fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef externalSystem fill:#666666,stroke:#0b4884,color:#ffffff
    classDef component fill:#85bbf0,stroke:#5d82a8,color:#000000

    Browser["Browser\n[Web Browser]\n\nUsed by a user to browse\nthe website"]
    MA["Application\n[Xamarin Application]\n\nAllows members to view and review\ntitles from their mobile devices"]

    subgraph listing-service ["Listing Service"]
        LC["Listing Controller\n[Spring MVC Controller]\n\nHandles requests for listing titles"]
        RC["Review Controller\n[Spring MVC Controller]\n\nHandles requests for reviews"]
        SC["Search Controller\n[Spring MVC Controller]\n\nHandles search requests"]
        LN["Listing Namespace\n[Spring Service]\n\nBusiness logic for listing titles"]
        RN["Review Namespace\n[Spring Service]\n\nBusiness logic for reviews"]
        SN["Search Namespace\n[Spring Service]\n\nBusiness logic for search"]
    end

    R[("In-Memory Cache\n[Redis]\n\nTitles and their reviews\nare cached")]
    K["Message Broker\n[Kafka]\n\nImportant domain events\nare published to Kafka"]
    TS["Title Service\n[Software System]\n\nProvides an API to retrieve\ntitle information"]
    RS["Review Service\n[Software System]\n\nProvides an API to retrieve\nand submit reviews"]
    SS["Search Service\n[Software System]\n\nProvides an API to search\nfor titles"]

    Browser --> LC
    MA --> LC
    MA --> RC
    MA --> SC

    LC --> LN
    RC --> RN
    SC --> SN

    LN --> R
    LN --> TS
    RN --> R
    RN --> RS
    RN --> K
    SN --> SS

    class Browser,MA container
    class TS,RS,SS,K externalSystem
    class LC,RC,SC,LN,RN,SN component
    class R component

    style listing-service stroke:#333,stroke-width:2px,stroke-dasharray:5 5
