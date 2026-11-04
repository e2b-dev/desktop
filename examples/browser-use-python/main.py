from __future__ import annotations

import os
import shlex
import textwrap

from dotenv import load_dotenv
from e2b_desktop import Sandbox


load_dotenv()

if not os.environ.get("E2B_API_KEY"):
    raise RuntimeError("Set E2B_API_KEY in .env before running this example")


browser_task = textwrap.dedent(
    """
    set -eu
    export PATH="$(python3 -m site --user-base)/bin:$PATH"
    python3 -m pip install --user --quiet uv
    uv python install 3.12
    uv tool install --python 3.12 browser-use

    chrome_bin="$(command -v google-chrome || command -v chromium || command -v chromium-browser)"
    profile_dir="$(mktemp -d)"
    "$chrome_bin" \
      --no-sandbox \
      --disable-dev-shm-usage \
      --no-first-run \
      --no-default-browser-check \
      --user-data-dir="$profile_dir" \
      --remote-debugging-address=127.0.0.1 \
      --remote-debugging-port=9222 \
      about:blank >/tmp/browser-use-chrome.log 2>&1 &
    chrome_pid=$!
    trap 'kill "$chrome_pid" 2>/dev/null || true; rm -rf "$profile_dir"' EXIT

    for _ in $(seq 1 30); do
      curl -fsS http://127.0.0.1:9222/json/version >/dev/null && break
      sleep 1
    done
    export BU_CDP_WS="$(python3 -c 'import json, urllib.request; print(json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/version"))["webSocketDebuggerUrl"])')"

    browser-use <<'BH'
    new_tab("https://example.com")
    wait_for_load()
    page = js("({title: document.title, heading: document.querySelector('h1')?.textContent})")
    print(page)
    # Browser Harness may prefix the tab title with a browser-state indicator.
    assert page["title"].endswith("Example Domain"), page
    assert page["heading"] == "Example Domain", page
    BH
    """
).strip()


desktop = Sandbox.create(timeout=300)
try:
    result = desktop.commands.run(
        f"bash -lc {shlex.quote(browser_task)}",
        envs={"DISPLAY": ":0"},
        timeout=240,
    )
    print(result.stdout)
finally:
    desktop.kill()
