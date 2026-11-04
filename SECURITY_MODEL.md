# Security model: Desktop template

This file describes what this repository is trusted to do, who might attack it, and which risks are accepted. Security scans read it to prioritize findings. It is one of four views of the same system:

- [e2b-dev/E2B](https://github.com/e2b-dev/E2B/blob/main/SECURITY_MODEL.md): SDKs and CLI
- [e2b-dev/code-interpreter](https://github.com/e2b-dev/code-interpreter/blob/main/SECURITY_MODEL.md): code interpreter template
- [e2b-dev/desktop](https://github.com/e2b-dev/desktop/blob/main/SECURITY_MODEL.md): desktop template
- [e2b-dev/customer-starter-templates](https://github.com/e2b-dev/customer-starter-templates/blob/main/SECURITY_MODEL.md): customer starter templates

The E2B API, edge proxy, envd server and sandbox isolation (Firecracker) live in other repositories and are not covered here.

## System overview

Developers' code (often an AI agent) uses the E2B SDKs and CLI on a **host** (laptop, server, CI) to create sandboxes on E2B clusters and to run code, files and processes in them. Templates define what runs inside a sandbox.

Trust boundaries:

1. **Host to E2B API** (`api.<E2B_DOMAIN>`): HTTPS with `X-API-Key` (team API key) or `Authorization: Bearer` (access token).
2. **Host to sandbox envd** (`<port>-<sandboxId>.<E2B_DOMAIN>`): Connect RPC/HTTP with `X-Access-Token` (envd access token), a Basic auth username for the run-as user, signed file URLs, and `e2b-traffic-access-token` for public ports.
3. **Sandbox to host**: everything a sandbox returns (command output, files, paths, Jupyter results, VNC, MCP responses) is produced by untrusted code.
4. **Internet to sandbox ports**: ports are reachable through the E2B edge by hostname unless the sandbox requires a traffic access token.
5. **GitHub PRs and supply chain to CI**: workflows build templates and publish packages, images and templates.

## Components

| Component | Code |
|---|---|
| **desktop-template** | `template/`: XFCE desktop, x11vnc, noVNC (from the `e2b-dev/noVNC` fork, branch `e2b-desktop`) and websockify, browser policies (`template/files`) |
| **ci-release** | `.github/workflows/template.yml`: builds the template on push with `DOCKERHUB_TOKEN` and `E2B_API_KEY` |

The SDKs that drive this template are **addon-sdks** (`packages/desktop-{js,python}` in e2b-dev/E2B).

## Entry points

- VNC stream through noVNC/websockify, exposed on a sandbox port. The SDK starts x11vnc with a password when `requireAuth` is set and with `-nopw` otherwise; the password is passed as `?password=` in the stream URL.
- Shell commands the desktop SDKs run in the sandbox for `open()`, `press()`, `launch()` and window lookups.
- Third-party code pulled at build time: the noVNC fork and websockify cloned from GitHub, apt packages.

## Existing controls

- Optional VNC password via the SDK's `requireAuth`.
- Template builds run only on push, not on PRs.

## Accepted risk

- **In-sandbox services without authentication are by design** (code interpreter server and Jupyter with an empty token, x11vnc/noVNC without a password, the MCP gateway without a token, other template daemons). Code running in the sandbox already owns the sandbox. A finding whose only impact is that a process inside the sandbox can reach such a service is accepted risk.
- Still in scope: reaching those services **from the internet** without the owner's tokens, and SDK bugs that turn off authentication the user asked for (`requireAuth`, `secure`, traffic access tokens).
- Server-side components and sandbox isolation are out of scope here.

## Attackers

All of these matter equally:

1. **Untrusted code inside the sandbox** (LLM-generated or user-supplied) attacking the host through what it returns: file names and paths, symlinks, oversized or malformed responses, terminal escape sequences, poisoned results.
2. **Internet users reaching sandbox ports** without the owner's tokens.
3. **Malicious PR authors and supply-chain attackers** against CI, release pipelines, template build scripts and third-party downloads.
4. **Network attackers** between the host and E2B (TLS, custom CA, `E2B_DOMAIN` overrides).
5. **Local attackers and malicious web pages** on the developer's machine.

## Assets

All equally important: users' E2B API keys and access/refresh tokens; envd and traffic access tokens and signed file URLs; CI and publishing credentials (npm/PyPI trusted publishing, Docker Hub, GitHub App keys, per-cluster E2B keys); customer data in sandboxes (files, env vars, secrets, desktop sessions); integrity of the host running the SDK or CLI.

## Finding tags

- `CWE`: CWE id of the weakness, e.g. `CWE-22`.
- `CVE`: CVE id for dependency findings.
- `package`: affected package or template (`js-sdk`, `python-sdk`, `cli`, `code-interpreter-sdk`, `desktop-sdk`, `dockerfile-utils`, `code-interpreter-template`, `desktop-template`, `template:<name>`, `ci`).

## Open questions

- Should the noVNC and websockify clones be pinned to a commit?
