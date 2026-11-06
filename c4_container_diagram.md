# Listing Service C4 Model: Container Diagram
```mermaid
flowchart TD
    classDef person fill:#08427b,stroke:#0b4884,color:#fff
    classDef container fill:#1168bd,stroke:#0b4884,color:#fff
    classDef externalSystem fill:#666666,stroke:#0b4884,color:#fff

    User["Premium Member<br/>[Person]<br/>A user of the website who has purchased a subscription"]:::person

    WebApp["Web Application<br/>[Spring Web App]<br/>Allows members to view and review titles via a web browser"]:::container
    MobileApp["Mobile Application<br/>[Xamarin App]<br/>Allows members to view and review titles from their mobile devices"]:::container

    ListingService["Listing Service<br/>[Spring Boot Service]<br/>Provides listing, search and review functions"]:::container
    Redis[("Redis Cache<br/>[Redis]<br/>Cache titles and reviews")]:::container
    Kafka["Kafka<br/>[Message Broker]<br/>Publish domain events"]:::container

    TitleService["Title Service<br/>[External System]<br/>Supply title information"]:::externalSystem
    ReviewService["Review Service<br/>[External System]<br/>Handle review data"]:::externalSystem

    User --> WebApp
    User --> MobileApp

    WebApp --> ListingService
    MobileApp --> ListingService

    ListingService --> Redis
    ListingService --> Kafka
    ListingService --> TitleService
    ListingService --> ReviewService
