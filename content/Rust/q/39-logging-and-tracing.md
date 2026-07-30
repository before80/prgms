+++
title = "39-logging-and-tracing"
date = 2026-07-28T14:49:00+08:00
weight = 390
type = "docs"
description = "面向 Go 用户讲清 log/tracing、RUST_LOG、subscriber 与结构化日志"
isCJKLanguage = true
draft = false

+++

# 日志与 tracing (Logging and Tracing)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会觉得 `println!` 够用，直到线上要按级别过滤、按模块关掉噪声？
- 你是否分不清：`log` facade 和 `tracing` 该选哪个，`RUST_LOG` 到底谁在读？
- 你是否写了 `info!` 却没输出，不知道要 **init subscriber**（初始化订阅者）？
- 你是否想知道：span 和普通日志事件差在哪，库该不该自己 init，async 怎么 `Instrument`？
- 你会不会打完日志还纠结：要不要继续 `return Err`？JSON 日志怎么接到 stdout？
- 你是否想把 `Error` 挂进 tracing 字段，或纠结什么时候才上 OpenTelemetry？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| facade | — | 门面 API | 只定义 `info!` 等宏，不绑定具体后端 | 接口式 logger |
| `log` | — | 经典日志门面 | `info!`/`error!` 事件式日志 crate | 简单 `log` 包 |
| `tracing` | — | 诊断/追踪框架 | 事件 + **span**（跨度）的结构化诊断 | zap/slog + 一点 trace 味 |
| subscriber | — | 订阅者 | 真正接收并输出 tracing 数据的后端 | 具体 logger 实现 |
| `RUST_LOG` | — | 日志过滤环境变量 | 常见 EnvFilter 读取的过滤表达式 | zap 级别 / 自定义 env |
| EnvFilter | — | 环境过滤器 | 按模块/级别解析 `RUST_LOG` 的过滤器 | 级别配置 |
| span | — | 跨度 | 有进入/退出的一段时间区间，可挂字段 | 有时像带上下文的 logger |
| event | — | 事件 | 某时刻打出的一条日志点 | 普通 log 行 |
| field | — | 结构化字段 | `key = value` 附加在事件或 span 上 | zap 的 `zap.String(...)` |
| Instrument | — | 给 Future 挂 span | async 里让 span 跟随任务边界 | 上下文注入中间件 |
| JSON | JavaScript Object Notation | JSON 输出 | 一行一个 JSON 对象的日志格式 | zap JSON encoder |
| init | initialize | 初始化 | 进程里安装全局 subscriber / logger | `logger = zap.New...` |
| tracing-error | — | 错误字段增强 | 让 `Error` 在 tracing 里展开 source 链 | zap 的 `zap.Error` + 堆栈选项 |
| OTel | OpenTelemetry | 开放遥测 | 指标/追踪/日志的跨语言标准与导出 | 同名 Go SDK |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q8](#q8), [Q13](#q13) |
| `common` | [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12) |
| `occasional` | [Q14](#q14) |
| `advanced` | — |

---

## Q1. 为什么 `println!` 不够当日志用？ {#q1}
**Tags:** `hot` `beginner` `println` `logging`
**适用版本:** Rust 1.0+

**一句话答案：**
`println!` 没有级别、不能按模块过滤、难对接采集、也分不清 stdout/stderr 职责；日志系统要的是可开关、可结构化、可在库与应用之间解耦的诊断输出。

**解答：**
`println!` 适合本地演示和「把结果打印给用户看」。线上诊断要回答的是：这条信息有多严重？属于哪个模块？现在要不要留下？字段是什么？

```rust
fn main() {
    // 看起来像日志，其实只是普通输出
    println!("connecting...");
    eprintln!("something failed"); // 稍微好点：错误走 stderr
}
```

一旦依赖变多，库里若也 `println!`，应用无法统一关掉或改格式。正确分工是：库发「诊断事件」，应用在 `main` 里决定怎么收集（见 [Q8](#q8)）。

```bash
# 你想要的是这种开关，而不是改代码删 println
RUST_LOG=info cargo run
RUST_LOG=debug cargo run
```

**Go 对比：**
```go
fmt.Println("connecting...") // 同样不是生产日志
log.Println("connecting...") // 标准库 log 仍偏简陋
```
- **Go 怎么做**：生产上常用 zap / slog / zerolog，而不是 `fmt.Println`。
- **Rust 为什么不同**：同样把「打印」和「可过滤诊断」分开；生态重心在 `log` / `tracing`。
- **Go 程序员易踩的坑**：把 `println!` 当成 `log.Printf`，合并请求时噪声无法关。

**记忆点：**
- 给用户看的结果 → 打印可以。
- 给运维/排障看的信号 → 日志门面 + 后端。

---

## Q2. `log` 和 `tracing` 怎么选？ {#q2}
**Tags:** `hot` `log` `tracing`
**适用版本:** `log` 0.4.x；`tracing` 0.1.x（生态主流）

**一句话答案：**
只要「一条条事件日志」，`log` facade 够用；需要 span、结构化字段、async 上下文传播，优先 `tracing`。新二进制两者都能接到，但新项目更常直接上 tracing。

**解答：**
**facade**（门面 API）只提供宏，不负责输出。`log` 是经典事件门面；**tracing** 在事件之外加了 **span**（跨度：有进入/离开的区间）。

```toml
# 经典 log 门面 + 某个后端（示例用 env_logger）
[dependencies]
log = "0.4"
env_logger = "0.11"
```

```text
// log 风格：点状事件
env_logger::init();
log::info!("server started");
log::debug!("cfg = {}", cfg);
```

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

```text
// tracing 风格：事件 + 可选 span
tracing_subscriber::fmt()
    .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
    .init();
tracing::info!("server started");
```

许多库同时支持：内部用 tracing，或通过桥接把 `log` 记录转到 tracing。应用只 init 一次后端即可。

**Go 对比：**
- **Go 怎么做**：`log` 标准库偏简单；结构化用 zap/slog。
- **Rust 为什么不同**：`log` ≈ 简单门面；`tracing` ≈ 结构化 + span 的现代默认。
- **Go 程序员易踩的坑**：以为 `tracing` 等于分布式 tracing 系统（Jaeger）；它首先是进程内诊断框架，导出到 OpenTelemetry 是另一步。

**记忆点：**
- 只要级别日志 → `log` 也能活。
- 要 span / 结构化 / async → `tracing`。

---

## Q3. `RUST_LOG` 是谁读的？为什么一定要 init？ {#q3}
**Tags:** `hot` `RUST_LOG` `EnvFilter` `init`
**适用版本:** tracing-subscriber 0.3.x；env_logger 等同类后端

**一句话答案：**
`RUST_LOG` 本身不会被 Rust 运行时自动消费；是你选用的 **subscriber** / logger 后端（常见是 `EnvFilter`）在 **init** 时去读。不 init，宏调用往往是空操作或看不到输出。

**解答：**
环境变量只是约定；真正解析它的是过滤器实现。tracing 侧最常见：

```text
use tracing_subscriber::EnvFilter;

tracing_subscriber::fmt()
    .with_env_filter(EnvFilter::from_default_env()) // 默认读 RUST_LOG
    .init();
```

```bash
RUST_LOG=info cargo run
RUST_LOG=my_app=debug,hyper=warn cargo run
RUST_LOG=trace cargo run
```

`log` + `env_logger` 同样在 init 时读 `RUST_LOG`：

```text
env_logger::init(); // 默认关注 RUST_LOG
log::info!("hi");
```

没 init 时：`info!` 仍然「调用了」，但没有全局订阅者/ logger，你看不到预期输出——这不是宏坏了，是后端没挂上。

**Go 对比：**
- **Go 怎么做**：zap/slog 也要在 `main` 构造 logger；级别常来自配置或 env，同样不是语言自动读。
- **Rust 为什么不同**：宏是全局门面，输出完全取决于进程里安装了谁。
- **Go 程序员易踩的坑**：导出了 `RUST_LOG` 却忘了 `init`，以为环境变量自己会生效。

**记忆点：**
- `RUST_LOG` → 过滤器读，不是语言内建。
- 先 init，再打日志。

---

## Q4. subscriber 最小初始化长什么样？ {#q4}
**Tags:** `hot` `subscriber` `tracing-subscriber`
**适用版本:** tracing 0.1；tracing-subscriber 0.3

**一句话答案：**
在 `main` 开头用 `tracing_subscriber::fmt()...init()` 安装全局 **subscriber**（订阅者）；带上 `EnvFilter` 就能吃 `RUST_LOG`。整个进程通常只 init 一次。

**解答：**

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

```text
fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .with_target(true)
        .init();

    tracing::info!("boot");
    run();
}

fn run() {
    tracing::debug!(step = 1, "work");
}
```

更短的写法（默认格式 + 默认 env filter，视版本 API 而定）：

```text
tracing_subscriber::fmt::init();
```

重复 `init` 通常会 panic 或返回错误（已有全局 subscriber）。测试里若需要隔离，用 `with_default` / `set_default` 等局部安装，而不是在库里偷偷全局 init（见 [Q8](#q8)）。

**Go 对比：**
```go
logger, err := zap.NewProduction()
if err != nil { log.Fatal(err) }
defer logger.Sync()
logger.Info("boot")
```
- **Go 怎么做**：`main` 构造具体 logger，再往下传或放到全局。
- **Rust 为什么不同**：tracing 习惯「全局 subscriber + 各处宏」，少传 logger 参数。
- **Go 程序员易踩的坑**：在每个模块里各 init 一次，测试和二进制互相抢全局状态。

**记忆点：**
- `main` 里 init 一次。
- `fmt` + `EnvFilter` 就是最小可用集。

---

## Q5. `info!` / `debug!` 事件和 span 有什么差别？ {#q5}
**Tags:** `hot` `event` `span` `info` `debug`
**适用版本:** tracing 0.1

**一句话答案：**
`info!` / `debug!` 是瞬时 **event**（事件）；span 是有进入/退出的区间，用来包住一段工作并携带上下文，内部事件会挂在当前 span 下。

**解答：**

```text
use tracing::{info, debug, info_span, Instrument}; // Instrument 见 [Q9](#q9)

fn handle(req_id: &str) {
    let span = info_span!("handle_request", req_id = %req_id);
    let _enter = span.enter(); // 同步代码：进入 span

    info!("start");           // 事件，落在当前 span 上下文
    do_work();
    debug!(phase = "done", "finished");
} // _enter drop 时离开 span
```

直觉：
- 事件 = 「此刻发生了一句话」；
- span = 「这段工作从这里开始、到这里结束」，适合量耗时、挂 `req_id` 等字段。

级别宏：`error!` / `warn!` / `info!` / `debug!` / `trace!`，和 Go 里按级别打日志一样；span 也有 `info_span!` / `debug_span!` 等。

**Go 对比：**
- **Go 怎么做**：zap 字段常挂在 logger 上；跨度更多靠 OpenTelemetry 或手传 context。
- **Rust 为什么不同**：tracing 把 span 做成一等公民，事件默认能看见当前 span 字段。
- **Go 程序员易踩的坑**：只打 `info!` 从不建 span，请求级字段只能每条事件重复写。

**记忆点：**
- 点 → event；段 → span。
- 请求/任务边界优先 span。

---

## Q6. 怎么按模块过滤日志？ {#q6}
**Tags:** `common` `filter` `RUST_LOG` `target`
**适用版本:** tracing-subscriber EnvFilter

**一句话答案：**
用 `RUST_LOG`（或代码里构造的 `EnvFilter`）写 `模块路径=级别`；默认 target 多半是 module path。把吵的依赖调高阈值，把自己的 crate 调低级别。

**解答：**

```bash
# 只看本 crate 的 debug，依赖保持 warn
RUST_LOG=warn,my_app=debug cargo run

# 某个模块更吵
RUST_LOG=my_app::db=trace,my_app=info cargo run

# 关掉某依赖
RUST_LOG=info,hyper=off,tower=warn cargo run
```

代码侧等价物：

```text
use tracing_subscriber::EnvFilter;

let filter = EnvFilter::new("warn,my_app=debug");
tracing_subscriber::fmt().with_env_filter(filter).init();
```

`with_target(true)` 时输出里能看到 target，便于你对照过滤表达式。模块名以编译单元的 `module_path!` 为准，改名后过滤字符串也要改。

**Go 对比：**
- **Go 怎么做**：zap 常按 logger 名字或包习惯拆；级别多在配置文件。
- **Rust 为什么不同**：`RUST_LOG` 的「`crate::module=level`」语法是日常排障默认入口。
- **Go 程序员易踩的坑**：只设 `RUST_LOG=debug`，被依赖海量 debug 淹没——要会写定向过滤。

**记忆点：**
- `RUST_LOG=warn,my_crate=debug` 是基本功。
- 先压依赖，再开自己的 debug。

---

## Q7. 结构化字段怎么打？ {#q7}
**Tags:** `common` `field` `structured`
**适用版本:** tracing 0.1

**一句话答案：**
在宏里写 `key = value`（或 `key = %Display` / `?Debug`）；让字段成为机器可解析的 **field**，不要把一切都 `format!` 进消息字符串。

**解答：**

```text
let user_id = 42;
let path = "/api/items";

// 更好：字段独立
tracing::info!(user_id, path, status = 200, "request ok");

// Display / Debug 包装
tracing::warn!(err = %err, "retry");
tracing::debug!(cfg = ?cfg, "loaded");

// span 上也挂字段
let span = tracing::info_span!("query", table = "users", user_id);
let _g = span.enter();
tracing::debug!("executing");
```

反模式：`info!("user_id={} path={}", user_id, path)`——人能读，过滤器/采集器却难按字段检索。

消息字符串仍可保留一句人类可读摘要；稳定键名（`user_id`、`error.code`）比散文重要。

**Go 对比：**
```go
logger.Info("request ok",
    zap.Int("user_id", 42),
    zap.String("path", "/api/items"),
    zap.Int("status", 200),
)
```
- **Go 怎么做**：zap/slog 强调 typed fields。
- **Rust 为什么不同**：tracing 宏内嵌字段语法，风格接近，只是写法更「宏」。
- **Go 程序员易踩的坑**：全部拼进字符串，丢了结构化检索能力。

**记忆点：**
- `key = value` 进宏；消息只做摘要。
- `%` / `?` 选择 Display / Debug。

---

## Q8. 为什么库不该 init subscriber？ {#q8}
**Tags:** `hot` `library` `subscriber` `init`
**适用版本:** tracing 0.1

**一句话答案：**
subscriber 是进程级策略，只有二进制（或测试）的 `main` 才知道该输出到哪里、什么格式、什么过滤；库只应 `tracing::info!` / 建 span，把策略留给应用。

**解答：**
库正确姿态：

```text
// 在 library crate 内
pub fn connect(url: &str) {
    tracing::info!(%url, "connecting");
    // ...
}
```

库错误姿态：

```text
// 别在库里干这种事
pub fn connect(url: &str) {
    tracing_subscriber::fmt().init(); // 抢全局；应用无法再装自己的
    tracing::info!("connecting");
}
```

应用方：

```text
fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();
    my_lib::connect("postgres://...");
}
```

若库强制 init，应用想改 JSON、想接 OpenTelemetry、想在测试里静音，都会冲突。需要「默认有点输出」时，文档写清楚：由应用 init；测试可用 `tracing-test` 一类工具，而不是在 `lib.rs` 里装全局。

**Go 对比：**
- **Go 怎么做**：库一般接受 `*zap.Logger` / `slog.Logger` 参数，或用默认 no-op；很少在 `init()` 里抢全局。
- **Rust 为什么不同**：宏默认打到全局 subscriber，更要克制「库里 init」。
- **Go 程序员易踩的坑**：在 Rust 库的 `init`/`lazy_static` 里安装 subscriber，和二进制抢车。

**记忆点：**
- 库：只打事件/span。
- 应用：唯一 init 点。

---

## Q9. async 里 `Instrument` 是干什么的？ {#q9}
**Tags:** `common` `async` `Instrument` `span`
**适用版本:** tracing 0.1；async 生态（Tokio 等）

**一句话答案：**
`.instrument(span)` 把 span 绑到某个 **Future** 上：任务在轮询时进入该 span，避免「只在创建 future 时 `enter()`、await 之后上下文丢了」。

**解答：**
同步代码 `span.enter()` 靠守卫；async 里 `.await` 会让出执行，守卫不能跨 await 傻握着。正确做法是给 future 挂 span：

```text
use tracing::Instrument;

async fn handle(req_id: String) {
    do_io().await;
}

// 调用方：
let span = tracing::info_span!("handle", %req_id);
handle(req_id).instrument(span).await;
```

```toml
[dependencies]
tracing = "0.1"
# 另需你的 async runtime，例如 tokio
```

要点：
- `instrument` 不替代 runtime；它只传播诊断上下文。
- 在 `tokio::spawn` 前挂好 span，子任务才带得上字段。
- 更细的 async 运行时概念见 [31-async-programming](../31-async-programming/)。

**Go 对比：**
- **Go 怎么做**：把 `context.Context` / logger 传进 goroutine；或用 otel 中间件。
- **Rust 为什么不同**：Future 是显式状态机，span 要挂在 future 上才能跨 `.await` 存活。
- **Go 程序员易踩的坑**：在 async 函数开头 `let _e = span.enter();` 然后 `.await`，上下文错乱或持守卫过久。

**记忆点：**
- async 边界用 `.instrument(span)`。
- 别把 `enter()` 守卫跨 `.await`。

---

## Q10. 和 Go 的 zap / slog 怎么对照？ {#q10}
**Tags:** `common` `go` `zap` `slog`
**适用版本:** tracing 0.1；对照 Go 1.21+ slog / zap

**一句话答案：**
`tracing::info!(k = v, "msg")` 对标 zap/slog 的结构化字段日志；subscriber 对标具体 Handler/Core；`RUST_LOG` 对标级别配置；span 比 zap 更强调「区间上下文」。

**解答：**

| 概念 | Go (zap/slog) | Rust (tracing) |
|------|----------------|----------------|
| 打一条 | `logger.Info("msg", fields...)` | `tracing::info!(fields..., "msg")` |
| 级别 | Info/Debug/... | 同名宏 |
| 后端 | Core / Handler | subscriber |
| 配置级别 | config / env | `EnvFilter` + `RUST_LOG` |
| 结构化 | typed fields | 宏内 `key = value` |
| 上下文 | With / context logger | span + Instrument |
| JSON | JSON encoder | `json` layer/feature |

```go
slog.Info("request ok", "user_id", 42, "status", 200)
```

```text
tracing::info!(user_id = 42, status = 200, "request ok");
```

选 zap 还是 slog 是 Go 侧问题；在 Rust 侧，新二进制默认学 tracing 即可，旧代码用 `log` 也能通过桥接共存。

**Go 对比：**
- **Go 怎么做**：标准库现有 slog；很多存量用 zap。
- **Rust 为什么不同**：tracing 把「日志」和「轻量 span」放同一套宏里。
- **Go 程序员易踩的坑**：找「Rust 版 zap 包名」，结果应该学的是 tracing + subscriber。

**记忆点：**
- 字段日志 ≈ zap/slog。
- 再加 span / Instrument，是 tracing 多出来的一层。

---

## Q11. 怎么打 JSON 日志？ {#q11}
**Tags:** `common` `JSON` `fmt`
**适用版本:** tracing-subscriber 0.3（`json` feature）

**一句话答案：**
给 `tracing-subscriber` 打开 `json` feature，用 JSON 层/格式化器输出到 stdout/stderr，让采集器按行解析。

**解答：**

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

```text
use tracing_subscriber::{fmt, EnvFilter};

fmt()
    .json()
    .with_env_filter(EnvFilter::from_default_env())
    .with_current_span(true)
    .with_span_list(true)
    .init();

tracing::info!(user_id = 7, "ready");
```

输出形态（一行一个对象，具体键名随配置变化）：

```text
{"timestamp":"...","level":"INFO","fields":{"message":"ready","user_id":7},...}
```

本地开发可用人读 fmt，生产切 JSON——用 feature / 配置分支在 `main` 选择，而不是让库决定格式。

**Go 对比：**
- **Go 怎么做**：`zap.NewProduction()` 默认 JSON；slog 也可挂 JSON handler。
- **Rust 为什么不同**：同样是 subscriber 配置问题，和业务代码无关。
- **Go 程序员易踩的坑**：忘开 `json` feature，`fmt().json()` 编不过。

**记忆点：**
- JSON = subscriber 的输出格式。
- 采集按「一行一条」约定来。

---

## Q12. 打完日志还要不要 `return Err`？ {#q12}
**Tags:** `common` `error` `Result` `logging`
**适用版本:** Rust 1.0+；与 tracing/log 无关的通用原则

**一句话答案：**
要。日志是给人类/采集看的副作用；`Result` / 退出码才是控制流。该失败时：先记日志（或靠上层统一记），再 `return Err` / 非 0 退出，别只打日志然后假装成功。

**解答：**

```text
fn load_config(path: &str) -> anyhow::Result<Config> {
    match read_config(path) {
        Ok(cfg) => Ok(cfg),
        Err(e) => {
            tracing::error!(error = %e, %path, "load config failed");
            Err(e) // 仍然把失败传出去
        }
    }
}
```

分层建议：
- 底层库：优先返回 `Err`，少打或不打（避免和应用重复刷屏）；需要诊断用 `debug!`/`trace!`。
- 应用边界（HTTP handler / CLI `main`）：记录一次 + 转成用户可见错误 / 退出码。

```text
// CLI 边界
if let Err(e) = run() {
    tracing::error!(error = %e, "exit with failure");
    std::process::exit(1);
}
```

「只 log 不返回」会导致调用方继续跑，数据处于半损坏状态——这和 Go 里 `log.Println(err); return nil` 一样糟。

**Go 对比：**
```go
if err != nil {
    logger.Error("load failed", zap.Error(err))
    return err // 仍然返回
}
```
- **Go 怎么做**：同样是 log 与 `error` 返回值分离。
- **Rust 为什么不同**：原则相同；只是错误是 `Result`，日志是 tracing/log。
- **Go 程序员易踩的坑**：把 `error!` 当成处理完毕，漏了 `?` / `return Err`。

**记忆点：**
- 日志 ≠ 错误处理。
- 失败要可见：日志给人看，`Err` 给代码看。

---

## Q13. 错误怎么进 tracing 字段？要不要上 tracing-error？ {#q13}
**Tags:** `hot` `error` `field` `tracing-error`
**适用版本:** tracing 0.1；可选 `tracing-error` 0.2

**一句话答案：**
日常用 `tracing::error!(error = %err, "...")` 或 `error = ?err` 把错误挂成字段；需要把 `source` 链/`Display` 展开得更完整时，再考虑 **tracing-error**（错误字段增强）与配套 Layer。别只 `error!("{}", err)` 把结构化字段丢掉。

**解答：**

```toml
[dependencies]
tracing = "0.1"
anyhow = "1"
# 需要时再加：
# tracing-error = "0.2"
```

```text
fn load(path: &str) -> anyhow::Result<String> {
    let text = std::fs::read_to_string(path).map_err(|e| {
        tracing::error!(error = %e, %path, "read failed");
        e
    })?;
    Ok(text)
}
```

格式差异：
- `%err`：走 `Display`（给人看的一句话）
- `?err`：走 `Debug`（更胖，适合排查）
- 有 `std::error::Error` source 链时，光 `%` 不一定打全链——这是 tracing-error / 手工 `err.chain()` 的用武之地

```text
// 示意：启用 tracing-error 的 ErrorLayer 后，
// 再配合 error 事件字段，subscriber 能更好展示错误上下文
// （具体 init 顺序以 tracing-error 文档为准）
```

和 [Q12](#q12) 的关系：字段解决「怎么记」；`return Err` 解决「控不控制流」。两者一起用。

**Go 对比：**
```go
logger.Error("read failed", zap.String("path", path), zap.Error(err))
```
- **Go 怎么做**：`zap.Error` / slog 的 `err` 属性。
- **Rust 为什么不同**：tracing 用字段语法；要链信息时可能叠加 tracing-error。
- **Go 程序员易踩的坑**：`error!("failed: {e}")` 只有消息、没有 `error` 字段，查询不好过滤。

**记忆点：**
- 先 `%`/`?` 字段化；链不够再 tracing-error。
- 日志字段 ≠ 吞掉 `Err`。

---

## Q14. 什么时候才需要上 OpenTelemetry（OTel）？ {#q14}
**Tags:** `occasional` `OpenTelemetry` `OTel` `distributed-tracing`
**适用版本:** 架构选型；`tracing` 可与 OTel 桥接

**一句话答案：**
单进程、单服务、只要级别过滤与结构化日志 → `tracing` + subscriber 就够。要**跨服务**串起一次请求（trace id）、对接 Jaeger/Tempo/云厂商、统一 metrics/traces → 再上 **OpenTelemetry（OTel，开放遥测）**。别把「安装 tracing」和「上了分布式追踪」当成一回事。

**解答：**
还早的信号：
- 一个二进制、日志量可控、排障靠 `RUST_LOG` + 字段
- 没有强制「请求必须跨 3 个服务对齐时间线」

该上的信号：
- 微服务调用链要在 UI 里点开父子 span
- 平台已规定 OTLP 导出
- 要和现有 Go/Java 服务的 trace 上下文互通（`traceparent` 等）

```text
// 层次直觉（不是完整代码）：
// 业务：tracing::info_span! / Instrument
// 导出：opentelemetry + tracing-opentelemetry 桥
// 后端：Jaeger / Tempo / 云 APM
```

```toml
# 真要接时再加（版本以当时文档为准），日常 FAQ 不必一上来就依赖
# opentelemetry = "..."
# tracing-opentelemetry = "..."
```

成本：导出延迟、采样配置、collector 运维。没有收集端就先别上。

**Go 对比：**
- **Go 怎么做**：otel-go SDK + 同样「先日志后分布式」的阶梯。
- **Rust 为什么不同**：进程内先 tracing；OTel 是导出层，不是替换 `info!`。
- **Go 程序员易踩的坑**：以为用了 tracing 就自动有 Jaeger 图——还要桥接与 exporter。

**记忆点：**
- tracing = 进程内诊断；OTel = 跨进程标准导出。
- 有收集需求再上，别提前缴税。

---
