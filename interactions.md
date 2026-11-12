# Streamy Code Flow Sequence Diagrams

## 1. Playback Initialization Sequence Analysis

```mermaid
---
title: Streamy Playback Initialization Sequence Analysis
---
sequenceDiagram
    actor Viewer as 👤 Platform Viewer
    participant Auth as 🔒 Auth Token Validator
    participant Catalog as 🎬 Media Catalog Engine

    Viewer->>Auth: 1. Request Playback Route (stream_id, token)
    Auth->>Auth: 2. Check token expiration state
    alt token is expired / invalid
        Auth-->>Viewer: 3a. Return 401 Unauthorized Payload
    else token is active
        Auth->>Catalog: 3b. Request Streaming Meta-payload (stream_id)
        Catalog->>Catalog: 4. Fetch content encryption descriptors
        Catalog-->>Viewer: 5. Handshake OK (Return 200 OK + HLS Stream URL)
    end
```

## 2. Lab 8 Extra: POST /users Account Registration

### 2.1 Registration Sequence (activation, loop, alt/else, par/and)

The registration flow activates the service on entry, loops over matched users to detect active accounts, branches on the duplicate-account outcome with `alt/else`, and runs the welcome email and creation event concurrently inside a `par/and` frame.

```mermaid
---
title: Streamy POST /users Registration
---
sequenceDiagram
    autonumber
    participant C as UserController
    participant S as CreateUserService
    participant R as UserRepository
    participant M as WelcomeEmailService
    participant E as EventPublisher

    C->>+S: create_user(email: String) : Result
    S->>R: find_by_email(email: String) : User[]
    R-->>S: existingUsers: User[]
    loop each existingUser
        S->>S: is_active(existingUser) : Boolean
    end
    alt active account exists
        S-->>C: conflict: RegistrationError
    else registration permitted
        S->>R: insert_user(email: String) : User
        R-->>S: newUser: User
        par welcome email
            S->>M: send_welcome_email(newUser) : Boolean
            M-->>S: emailAccepted: Boolean
        and creation event
            S->>E: publish_user_created(newUser) : Boolean
            E-->>S: eventAccepted: Boolean
        end
        S-->>C: newUser: User
    end
    deactivate S
```

### 2.2 Code Smell Analysis

- **Leaky Abstractions:** Iterating over all matched users to identify active accounts may be inefficient. Consider a repository method such as `exists_active_by_email(email)`, supported by appropriate uniqueness rules.
- **Side-Effect Coupling:** Sending email and publishing an event during registration can make retries and partial failures difficult. Consider an event-driven worker and, where needed, a transactional outbox for reliable delivery.

## 3. Challenge: Playback Service Flow Applied to the Streamy Codebase

### 3.1 Participants and Signatures

| Participant | Role | Key methods |
|---|---|---|
| `Viewer` | Platform actor | Initiates the playback request |
| `PlaybackController` | Controller entry point | `request_playback(stream_id: String, token: String) : PlaybackResult` |
| `TokenValidator` | Auth service | `validate_token(token: String) : Boolean` |
| `CatalogService` | Business service | `get_stream_meta(stream_id: String) : List<StreamMeta>` |
| `StreamRepository` | Persistence repository | `find_by_stream_id(stream_id: String) : StreamMeta` |
| `EventPublisher` | Notification dependency | `publish_stream_started(viewer_id: String) : Boolean` |

### 3.2 Sequence Diagram

```mermaid
---
title: Streamy Playback Request Flow (Challenge)
---
sequenceDiagram
    autonumber
    actor V as Viewer
    participant C as PlaybackController
    participant T as TokenValidator
    participant CS as CatalogService
    participant R as StreamRepository
    participant E as EventPublisher

    V->>C: request_playback(stream_id: String, token: String) : PlaybackResult
    C->>+T: validate_token(token: String) : Boolean
    T-->>C: isValid: Boolean
    alt invalid or expired token
        C-->>V: 401 Unauthorized: ErrorPayload
    else valid token
        C->>+CS: get_stream_meta(stream_id: String) : List<StreamMeta>
        loop each meta record
            CS->>R: find_by_stream_id(stream_id: String) : StreamMeta
            R-->>CS: meta: StreamMeta
        end
        par telemetry event
            CS->>E: publish_stream_started(viewer_id: String) : Boolean
        and cache refresh
            CS->>CS: refresh_cache(stream_id: String) : void
        end
        CS-->>C: meta: StreamMeta
        C-->>V: 200 OK: HlsUrl
        deactivate CS
    end
    deactivate T
```

### 3.3 Observed vs Proposed Behavior

- **Observed in the codebase:** token validation, repository lookup by stream id, and the unauthorized/authorized branching are existing behaviors of the playback flow.
- **Proposed (not yet proven non-blocking):** the `par` frame runs the telemetry event and cache refresh concurrently as an intended design; it does not by itself prove the implementation is non-blocking or retry-safe.
