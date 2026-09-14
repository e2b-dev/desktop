# Browser Use in E2B Desktop

Run Browser Use inside E2B's graphical sandbox. The example installs an isolated Python 3.12 runtime, starts the Chrome already installed in the desktop template with a temporary profile and local CDP endpoint, then connects Browser Use. Your agent gets browser navigation, DOM inspection, screenshots, clicks, and typing without a custom computer-use loop or remote-debugging approval prompt.

## Run it

```bash
cp .env.example .env
# Add your E2B_API_KEY to .env

uv run main.py
```

The example opens `example.com` inside the E2B Desktop Sandbox, reads the page through Browser Use, and checks the title and heading before Chrome and the sandbox are killed.

## Give the browser to a coding agent

Install the Browser Use skill in the same sandbox image or startup command:

```bash
browser-use skill install
```

Claude Code, Codex, OpenClaw, and other coding agents can then call the `browser-use` CLI directly. The browser stays inside the E2B sandbox.

## Why E2B Desktop instead of a plain sandbox?

The desktop template already has Chrome, its system dependencies, and an X display. A plain E2B sandbox needs a browser and those dependencies installed separately.

## Links

- [E2B Desktop](https://github.com/e2b-dev/desktop)
- [Browser Use CLI skill](https://github.com/browser-use/browser-use/blob/main/browser_use/skills/browser-use/SKILL.md)
