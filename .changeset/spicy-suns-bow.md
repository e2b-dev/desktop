---
"@e2b/desktop": minor
---

Update `e2b` to `2.27.1` and require Node `>=20.18.1` (matching the SDK's engine range).

The base SDK removed the beta create API in e2b 2.24.0, so `Sandbox.betaCreate` and `SandboxBetaCreateOpts` have been removed. Use `Sandbox.create` with the `lifecycle` option instead:

```ts
// before
await Sandbox.betaCreate({ autoPause: true })
// after
await Sandbox.create({ lifecycle: { onTimeout: 'pause' } })
```
