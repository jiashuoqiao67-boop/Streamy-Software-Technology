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
