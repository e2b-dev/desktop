---
"@e2b/desktop": minor
"@e2b/desktop-python": minor
---

Update `e2b` (js → `2.27.1`, python → `2.25.1`). The js SDK now requires Node `>=20.18.1`, matching the upstream engine range.

The base SDK removed the beta create API in e2b 2.24.0, so the desktop overrides have been removed: `Sandbox.betaCreate` / `SandboxBetaCreateOpts` (js) and `Sandbox.beta_create` (python). Use `Sandbox.create` with the `lifecycle` option instead:

```ts
// before
await Sandbox.betaCreate({ autoPause: true })
// after
await Sandbox.create({ lifecycle: { onTimeout: 'pause' } })
```

```python
# before
Sandbox.beta_create(auto_pause=True)
# after
Sandbox.create(lifecycle={"on_timeout": "pause"})
```
