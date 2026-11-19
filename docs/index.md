# System Architecture Documentation

Welcome to the automated documentation site for the **Streamy Video Streaming Backend Platform**. This site is built and deployed automatically by GitHub Actions: Markdown files under `docs/` are compiled with Jekyll, and the Mermaid diagram below is rendered in the browser into an inline SVG graphic.

## Service Flow

```mermaid
sequenceDiagram
    autonumber
    Client->>+API Gateway: Request /data
    API Gateway->>+Service: Fetch Data
    Service-->>-API Gateway: Return Payload
    API Gateway-->>-Client: 200 OK
```

## About This Pipeline

- **build** job: checks out the repository, compiles the Mermaid diagrams, builds the static site with Jekyll, and uploads the Pages artifact.
- **deploy** job: publishes the uploaded artifact to the GitHub Pages environment.

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false, theme: 'neutral' });
  document.querySelectorAll('code.language-mermaid, code[data-lang="mermaid"]').forEach((code) => {
    const pre = code.closest('pre');
    const box = document.createElement('div');
    box.className = 'mermaid';
    box.textContent = code.textContent;
    if (pre) { pre.replaceWith(box); } else { code.replaceWith(box); }
  });
  mermaid.run({ querySelector: '.mermaid' });
</script>
