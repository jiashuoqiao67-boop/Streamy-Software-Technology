# Streamy Video Streaming Backend Platform
## Software Technology Course Laboratory Node
* **Student Identity:** Qiao jiashuo
* **Neptun System Code:** [TNUVNQ]
**Course Section Reference:** GEIAL314‑B2a

## Workspace Environment Architecture
The diagram below maps out how our development environment connects local code
authoring to remote version tracking, using a **Diagrams‑as‑Code** design pipeline.

```mermaid
---
title: Streamy Production Architecture Proof
---
flowchart TD
%% Base Diagram Configurations and Properties
UserNode[" Workstation Client <br> (Terminal CLI / Web Browser)"]
LiveSandbox{" Cloud Sandbox <br> (mermaid.live)"}
LocalIDE[" VS Code IDE <br> (Markdown Preview Extension)"]
GitStage[" Local Git Index <br> (Staging Ledger)"]
RemoteHub[" GitHub Remote Cloud <br> (Streamy Repository Workspace)"]

UserNode -- 1. Sandbox Syntax --> LiveSandbox
LiveSandbox -- 2. Verified Block Migration --> LocalIDE
LocalIDE -- 3. git add CLI Operations --> GitStage
GitStage -- 4. git push Pipeline Push --> RemoteHub
