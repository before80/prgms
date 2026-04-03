+++
title = "Plugin SDK Migration"
date = 2026-04-03T15:33:23+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Plugin SDK Migration

OpenClaw has moved from a broad backwards-compatibility layer to a modern plugin architecture with focused, documented imports. If your plugin was built before the new architecture, this guide helps you migrate.

## What is changing

The old plugin system provided two wide-open surfaces that let plugins import anything they needed from a single entry point:

- **`openclaw/plugin-sdk/compat`** — a single import that re-exported dozens of helpers. It was introduced to keep older hook-based plugins working while the new plugin architecture was being built.
- **`openclaw/extension-api`** — a bridge that gave plugins direct access to host-side helpers like the embedded agent runner.

Both surfaces are now **deprecated**. They still work at runtime, but new plugins must not use them, and existing plugins should migrate before the next major release removes them.



The backwards-compatibility layer will be removed in a future major release. Plugins that still import from these surfaces will break when that happens.

## Why this changed

The old approach caused problems:

- **Slow startup** — importing one helper loaded dozens of unrelated modules
- **Circular dependencies** — broad re-exports made it easy to create import cycles
- **Unclear API surface** — no way to tell which exports were stable vs internal

The modern plugin SDK fixes this: each import path (`openclaw/plugin-sdk/\<subpath\>`) is a small, self-contained module with a clear purpose and documented contract.

## How to migrate

1) Audit Windows wrapper fallback behavior

If your plugin uses `openclaw/plugin-sdk/windows-spawn`, unresolved Windows `.cmd`/`.bat` wrappers now fail closed unless you explicitly pass `allowShellFallback: true`.



```
// Before
const program = applyWindowsSpawnProgramPolicy({ candidate });

// After
const program = applyWindowsSpawnProgramPolicy({
  candidate,
  // Only set this for trusted compatibility callers that intentionally
  // accept shell-mediated fallback.
  allowShellFallback: true,
});
```

If your caller does not intentionally rely on shell fallback, do not set `allowShellFallback` and handle the thrown error instead.

2) Find deprecated imports

Search your plugin for imports from either deprecated surface:



```
grep -r "plugin-sdk/compat" my-plugin/
grep -r "openclaw/extension-api" my-plugin/
```

3) Replace with focused imports

Each export from the old surface maps to a specific modern import path:



```
// Before (deprecated backwards-compatibility layer)
import {
  createChannelReplyPipeline,
  createPluginRuntimeStore,
  resolveControlCommandGate,
} from "openclaw/plugin-sdk/compat";

// After (modern focused imports)
import { createChannelReplyPipeline } from "openclaw/plugin-sdk/channel-reply-pipeline";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import { resolveControlCommandGate } from "openclaw/plugin-sdk/command-auth";
```

For host-side helpers, use the injected plugin runtime instead of importing directly:



```
// Before (deprecated extension-api bridge)
import { runEmbeddedPiAgent } from "openclaw/extension-api";
const result = await runEmbeddedPiAgent({ sessionId, prompt });

// After (injected runtime)
const result = await api.runtime.agent.runEmbeddedPiAgent({ sessionId, prompt });
```

The same pattern applies to other legacy bridge helpers:

| Old import                 | Modern equivalent                            |
| :------------------------- | :------------------------------------------- |
| `resolveAgentDir`          | `api.runtime.agent.resolveAgentDir`          |
| `resolveAgentWorkspaceDir` | `api.runtime.agent.resolveAgentWorkspaceDir` |
| `resolveAgentIdentity`     | `api.runtime.agent.resolveAgentIdentity`     |
| `resolveThinkingDefault`   | `api.runtime.agent.resolveThinkingDefault`   |
| `resolveAgentTimeoutMs`    | `api.runtime.agent.resolveAgentTimeoutMs`    |
| `ensureAgentWorkspace`     | `api.runtime.agent.ensureAgentWorkspace`     |
| session store helpers      | `api.runtime.agent.session.*`                |

4) Build and test



```
pnpm build
pnpm test -- my-plugin/
```

## Import path reference

Use the narrowest import that matches the job. If you cannot find an export, check the source at `src/plugin-sdk/` or ask in Discord.

## Removal timeline

| When                   | What happens                                                 |
| :--------------------- | :----------------------------------------------------------- |
| **Now**                | Deprecated surfaces emit runtime warnings                    |
| **Next major release** | Deprecated surfaces will be removed; plugins still using them will fail |

All core plugins have already been migrated. External plugins should migrate before the next major release.

## Suppressing the warnings temporarily

Set these environment variables while you work on migrating:



```
OPENCLAW_SUPPRESS_PLUGIN_SDK_COMPAT_WARNING=1 openclaw gateway run
OPENCLAW_SUPPRESS_EXTENSION_API_WARNING=1 openclaw gateway run
```

This is a temporary escape hatch, not a permanent solution.

## Related

- [Getting Started](https://docs.openclaw.ai/plugins/building-plugins) — build your first plugin
- [SDK Overview](https://docs.openclaw.ai/plugins/sdk-overview) — full subpath import reference
- [Channel Plugins](https://docs.openclaw.ai/plugins/sdk-channel-plugins) — building channel plugins
- [Provider Plugins](https://docs.openclaw.ai/plugins/sdk-provider-plugins) — building provider plugins
- [Plugin Internals](https://docs.openclaw.ai/plugins/architecture) — architecture deep dive
- [Plugin Manifest](https://docs.openclaw.ai/plugins/manifest) — manifest schema reference
