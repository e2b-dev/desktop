---
"@e2b/desktop": patch
"@e2b/desktop-python": patch
---

Disconnect from fire-and-forget background commands. After background `commands.run` calls whose output is never read (`xdg-open`, `gtk-launch`, `Xvfb`, `startxfce4`), the SDK now calls `.disconnect()` so it stops holding the command's event stream open while the process keeps running.
