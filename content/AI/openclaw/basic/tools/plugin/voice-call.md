+++
title = "Voice Call Plugin"
date = 2026-04-03T15:29:41+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# Voice Call Plugin 语音通话插件

Voice calls for OpenClaw via a plugin. Supports outbound notifications and multi-turn conversations with inbound policies. 

​	通过插件实现 OpenClaw 的语音通话。支持外呼通知以及遵循入站策略的多轮对话。

Current providers:

- `twilio` (Programmable Voice + Media Streams)
- `telnyx` (Call Control v2)
- `plivo` (Voice API + XML transfer + GetInput speech)
- `mock` (dev/no network)

Quick mental model:

​	快速思路模型：

- Install plugin
- Restart Gateway
- Configure under `plugins.entries.voice-call.config`
- Use `openclaw voicecall ...` or the `voice_call` tool

## Where it runs (local vs remote) 运行位置（本地与远程）

The Voice Call plugin runs **inside the Gateway process**.

​	语音通话插件在**网关进程内部**运行。

If you use a remote Gateway, install/configure the plugin on the **machine running the Gateway**, then restart the Gateway to load it.

​	如果使用远程网关，请在**运行网关的计算机**上安装/配置插件，然后重启网关以加载插件。

## Install

### Option A: install from npm (recommended)

```
openclaw plugins install @openclaw/voice-call
```

Restart the Gateway afterwards.

​	之后重启网关。

### Option B: install from a local folder (dev, no copying)

```
PLUGIN_SRC=./path/to/local/voice-call-plugin
openclaw plugins install "$PLUGIN_SRC"
cd "$PLUGIN_SRC" && pnpm install
```

Restart the Gateway afterwards.

​	之后重启网关。

## Config

Set config under `plugins.entries.voice-call.config`:

​	在`plugins.entries.voice-call.config`下设置配置：

```json
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // or "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234",
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          telnyx: {
            apiKey: "...",
            connectionId: "...",
            // Telnyx webhook public key from the Telnyx Mission Control Portal
            // (Base64 string; can also be set via TELNYX_PUBLIC_KEY).
            publicKey: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Webhook server
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Webhook security (recommended for tunnels/proxies)
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
            trustedProxyIPs: ["100.64.0.1"],
          },

          // Public exposure (pick one)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
            preStartTimeoutMs: 5000,
            maxPendingConnections: 32,
            maxPendingConnectionsPerIp: 4,
            maxConnections: 128,
          },
        },
      },
    },
  },
}
```

Notes:

- Twilio/Telnyx require a **publicly reachable** webhook URL.
  - Twilio/Telnyx 需要一个 **可公开访问** 的 webhook URL。

- Plivo requires a **publicly reachable** webhook URL.
  - Plivo 需要一个 **可公开访问** 的 Webhook 网址。

- `mock` is a local dev provider (no network calls).
  - `mock` 是一个本地开发用的提供方（无网络调用）。

- Telnyx requires `telnyx.publicKey` (or `TELNYX_PUBLIC_KEY`) unless `skipSignatureVerification` is true.
  - Telnyx 需要 `telnyx.publicKey`（或 `TELNYX_PUBLIC_KEY`），除非 `skipSignatureVerification` 为 true。

- `skipSignatureVerification` is for local testing only.
  - `skipSignatureVerification`仅适用于本地测试。

- If you use ngrok free tier, set `publicUrl` to the exact ngrok URL; signature verification is always enforced.
  - 如果你使用 ngrok 免费版，请将 `publicUrl` 设置为准确的 ngrok 网址；签名验证将始终强制执行。

- `tunnel.allowNgrokFreeTierLoopbackBypass: true` allows Twilio webhooks with invalid signatures **only** when `tunnel.provider="ngrok"` and `serve.bind` is loopback (ngrok local agent). Use for local dev only.
  - `tunnel.allowNgrokFreeTierLoopbackBypass: true` 仅在 `tunnel.provider="ngrok"` 且 `serve.bind` 为回环地址（ngrok 本地代理）时，允许签名无效的 Twilio Webhook。仅适用于本地开发。

- Ngrok free tier URLs can change or add interstitial behavior; if `publicUrl` drifts, Twilio signatures will fail. For production, prefer a stable domain or Tailscale funnel.
  - Ngrok 免费套餐的 URL 可能会发生变化或插入插播行为；如果 `publicUrl` 发生变动，Twilio 签名验证将会失败。对于生产环境，建议使用稳定的域名或 Tailscale 漏斗。

- Streaming security defaults: 流式传输安全默认值：
  - `streaming.preStartTimeoutMs` closes sockets that never send a valid `start` frame.
    - `streaming.preStartTimeoutMs` 会关闭从未发送有效 `start` 帧的套接字。
  - `streaming.maxPendingConnections` caps total unauthenticated pre-start sockets.
    - `streaming.maxPendingConnections` 限制所有未认证的预启动套接字的总数。
  - `streaming.maxPendingConnectionsPerIp` caps unauthenticated pre-start sockets per source IP.
    - streaming.maxPendingConnectionsPerIp</b> 限制每个源 IP 的未认证预启动套接字数量。
  - `streaming.maxConnections` caps total open media stream sockets (pending + active).
    - `streaming.maxConnections` 限制所有已打开的媒体流套接字总数（挂起 + 活跃）。

## Stale call reaper 失效通话清理程序

Use `staleCallReaperSeconds` to end calls that never receive a terminal webhook (for example, notify-mode calls that never complete). The default is `0` (disabled).

​	使用 `staleCallReaperSeconds` 来终止那些从未收到终端网络钩子的通话（例如，从未完成的通知模式通话）。默认值为 `0`（已禁用）。

Recommended ranges:

​	推荐范围：

- **Production:** `120`–`300` seconds for notify-style flows.
  - **生产环境：**`120`–`300` 秒，适用于通知类型的流程。

- Keep this value **higher than `maxDurationSeconds`** so normal calls can finish. A good starting point is `maxDurationSeconds + 30–60` seconds.
  - 将此值保持为**高于`maxDurationSeconds`**，以便普通调用能够完成。一个良好的初始值是`maxDurationSeconds + 30–60`秒。


Example:

```json
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          maxDurationSeconds: 300,
          staleCallReaperSeconds: 360,
        },
      },
    },
  },
}
```

## Webhook Security

When a proxy or tunnel sits in front of the Gateway, the plugin reconstructs the public URL for signature verification. These options control which forwarded headers are trusted.`webhookSecurity.allowedHosts` allowlists hosts from forwarding headers.`webhookSecurity.trustForwardingHeaders` trusts forwarded headers without an allowlist.`webhookSecurity.trustedProxyIPs` only trusts forwarded headers when the request remote IP matches the list.Webhook replay protection is enabled for Twilio and Plivo. Replayed valid webhook requests are acknowledged but skipped for side effects.Twilio conversation turns include a per-turn token in `<Gather>` callbacks, so stale/replayed speech callbacks cannot satisfy a newer pending transcript turn.Unauthenticated webhook requests are rejected before body reads when the provider’s required signature headers are missing.The voice-call webhook uses the shared pre-auth body profile (64 KB / 5 seconds) plus a per-IP in-flight cap before signature verification.

​	当代理或隧道位于网关前方时，插件会重建用于签名验证的公共 URL。这些选项控制哪些转发的标头是可信的。`webhookSecurity.allowedHosts` 将允许转发标头的主机列入白名单。`webhookSecurity.trustForwardingHeaders` 信任无白名单的转发标头。`webhookSecurity.trustedProxyIPs` 仅在请求的远程 IP 匹配列表时才信任转发的标头。已为 Twilio 和 Plivo 启用 Webhook 重放保护。重放的有效 Webhook 请求会收到确认，但不会产生副作用。Twilio 的对话回合会在 `<Gather>` 回调中包含每个回合的令牌，因此陈旧或重放的语音回调无法满足较新的待处理转录回合。当提供者缺少所需的签名标头时，未经验证的网络钩子请求会在读取请求体之前被拒绝。语音通话网络钩子使用共享的预授权主体配置文件（64千字节/5秒），并在签名验证前为每个IP设置飞行中上限。

Example with a stable public host:

​	带有稳定公共主机的示例：

```json
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          publicUrl: "https://voice.example.com/voice/webhook",
          webhookSecurity: {
            allowedHosts: ["voice.example.com"],
          },
        },
      },
    },
  },
}
```

## TTS for calls

Voice Call uses the core `messages.tts` configuration for streaming speech on calls. You can override it under the plugin config with the **same shape** — it deep‑merges with `messages.tts`.

​	语音通话使用核心的`messages.tts`配置来实现通话中的流式语音播放。你可以在插件配置下使用**相同的结构**覆盖该配置——它会与`messages.tts`进行深度合并。

```json
{
  tts: {
    provider: "elevenlabs",
    providers: {
      elevenlabs: {
        voiceId: "pMsXgVXv3BLzUgSXRplE",
        modelId: "eleven_multilingual_v2",
      },
    },
  },
}
```

Notes:

- Legacy `tts.<provider>` keys inside plugin config (`openai`, `elevenlabs`, `microsoft`, `edge`) are auto-migrated to `tts.providers.<provider>` on load. Prefer the `providers` shape in committed config.
  - 插件配置中的旧版 `tts.<provider>` 密钥（`openai`、`elevenlabs`、`microsoft`、`edge`）会在加载时自动迁移到 `tts.providers.<provider>`。请在已提交的配置中优先使用 `providers` 的结构。

- **Microsoft speech is ignored for voice calls** (telephony audio needs PCM; the current Microsoft transport does not expose telephony PCM output).
  - **Microsoft 语音在语音通话中被忽略**（电话音频需要 PCM；当前的 Microsoft 传输层未暴露电话 PCM 输出）。

- Core TTS is used when Twilio media streaming is enabled; otherwise calls fall back to provider native voices.
  - 启用 Twilio 媒体流时使用核心 TTS；否则通话将回退到提供商原生语音。

- If a Twilio media stream is already active, Voice Call does not fall back to TwiML `<Say>`. If telephony TTS is unavailable in that state, the playback request fails instead of mixing two playback paths.
  - 如果 Twilio 媒体流已处于活动状态，则语音通话不会回退到 TwiML `<Say>`。如果在该状态下电话语音 TTS 不可用，则播放请求会失败，而不会混合两条播放路径。

- When telephony TTS falls back to a secondary provider, Voice Call logs a warning with the provider chain (`from`, `to`, `attempts`) for debugging.
  - 当电话 TTS 回退到备用提供商时，语音通话会记录一条包含提供商链（`from`、`to`、`attempts`）的警告日志，以便进行调试。


### More examples

Use core TTS only (no override):

​	仅使用核心TTS（不覆盖）：

```json
{
  messages: {
    tts: {
      provider: "openai",
      providers: {
        openai: { voice: "alloy" },
      },
    },
  },
}
```

Override to ElevenLabs just for calls (keep core default elsewhere):

​	仅针对通话覆盖为 ElevenLabs（其他位置保留核心默认设置）：

```json
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            provider: "elevenlabs",
            providers: {
              elevenlabs: {
                apiKey: "elevenlabs_key",
                voiceId: "pMsXgVXv3BLzUgSXRplE",
                modelId: "eleven_multilingual_v2",
              },
            },
          },
        },
      },
    },
  },
}
```

Override only the OpenAI model for calls (deep‑merge example):

​	仅覆盖调用时的 OpenAI 模型（深度合并示例）：

```json
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            providers: {
              openai: {
                model: "gpt-4o-mini-tts",
                voice: "marin",
              },
            },
          },
        },
      },
    },
  },
}
```

## Inbound calls 呼入通话

Inbound policy defaults to `disabled`. To enable inbound calls, set:

​	入站策略默认设置为`disabled`。要启用入站呼叫，请设置：

```json
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

`inboundPolicy: "allowlist"` is a low-assurance caller-ID screen. The plugin normalizes the provider-supplied `From` value and compares it to `allowFrom`. Webhook verification authenticates provider delivery and payload integrity, but it does not prove PSTN/VoIP caller-number ownership. Treat `allowFrom` as caller-ID filtering, not strong caller identity.

​	`inboundPolicy: "allowlist"`是一种低安全性的来电者身份识别筛选方式。该插件会对提供商提供的`From`值进行标准化处理，并与`allowFrom`进行比对。网络挂钩验证可对提供商的投递行为和负载完整性进行身份验证，但无法证明公用交换电话网/网络电话的来电号码归属。请将`allowFrom`视为来电者身份筛选，而非可靠的来电身份凭证。

Auto-responses use the agent system. Tune with:

​	自动回复使用智能体系统。可通过以下方式进行调整：

- `responseModel`
- `responseSystemPrompt`
- `responseTimeoutMs`

### Spoken output contract 语音输出协议

For auto-responses, Voice Call appends a strict spoken-output contract to the system prompt:

​	对于自动回复，语音通话会在系统提示后附加一份严格的语音输出约定：

- `{"spoken":"..."}`

Voice Call then extracts speech text defensively:

​	语音通话随后会保护性地提取语音文本：

- Ignores payloads marked as reasoning/error content.
  - 忽略标记为推理/错误内容的负载。

- Parses direct JSON, fenced JSON, or inline `"spoken"` keys.
  - 解析直接 JSON、带格式的 JSON 或内联的`"spoken"`键。

- Falls back to plain text and removes likely planning/meta lead-in paragraphs.
  - 回退到纯文本模式，并移除可能的规划类或元数据类前置段落。


This keeps spoken playback focused on caller-facing text and avoids leaking planning text into audio.

​	这样可以让语音播报只聚焦于面向来电者的文本，同时避免将规划类文本泄露到音频中。

### Conversation startup behavior 对话启动行为

For outbound `conversation` calls, first-message handling is tied to live playback state:

​	对于外发`conversation`呼叫，首条消息处理与实时播放状态相关联：

- Barge-in queue clear and auto-response are suppressed only while the initial greeting is actively speaking.
  - 仅在初始问候语主动播放期间，才会抑制打断队列清除和自动响应功能。

- If initial playback fails, the call returns to `listening` and the initial message remains queued for retry.
  - 如果初始播放失败，呼叫将返回`listening`状态，且初始消息仍会排队等待重试。

- Initial playback for Twilio streaming starts on stream connect without extra delay.
  - Twilio 流媒体的初始播放在流连接时开始，无额外延迟。


### Twilio stream disconnect grace - Twilio 流断开宽限

When a Twilio media stream disconnects, Voice Call waits `2000ms` before auto-ending the call:

​	当 Twilio 媒体流断开连接时，语音通话会等待`2000ms`然后自动结束通话：

- If the stream reconnects during that window, auto-end is canceled.
  - 如果媒体流在此期间重新连接，自动结束将被取消。

- If no stream is re-registered after the grace period, the call is ended to prevent stuck active calls.
  - 如果在宽限期后没有重新注册流，将结束该呼叫以防止活动呼叫卡住。


## CLI



```sh
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall start --to "+15555550123"   # alias for call
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall latency                     # summarize turn latency from logs
openclaw voicecall expose --mode funnel
```

`latency` reads `calls.jsonl` from the default voice-call storage path. Use `--file <path>` to point at a different log and `--last <n>` to limit analysis to the last N records (default 200). Output includes p50/p90/p99 for turn latency and listen-wait times.

​	`latency`读取默认语音通话存储路径中的`calls.jsonl`文件。使用`--file <path>`指定其他日志文件，使用`--last <n>`将分析限制在最近N条记录（默认200条）。输出结果包含通话延迟和监听等待时间的p50/p90/p99分位数。

## Agent tool

Tool name: `voice_call`Actions:

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

This repo ships a matching skill doc at `skills/voice-call/SKILL.md`.

​	该仓库在 `skills/voice-call/SKILL.md` 提供了对应的技能文档。

## Gateway RPC

- `voicecall.initiate` (`to?`, `message`, `mode?`)
- `voicecall.continue` (`callId`, `message`)
- `voicecall.speak` (`callId`, `message`)
- `voicecall.end` (`callId`)
- `voicecall.status` (`callId`)
