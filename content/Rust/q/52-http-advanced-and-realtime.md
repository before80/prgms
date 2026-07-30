+++
title = "52-http-advanced-and-realtime"
date = 2026-07-28T14:49:00+08:00
weight = 520
type = "docs"
description = "面向 Go 用户讲清 CORS、Cookie、multipart、WebSocket/SSE、限流与 tower-http"
isCJKLanguage = true
draft = false

+++

# HTTP 进阶与实时通信 (HTTP Advanced and Realtime)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否已经会 [40-http](../40-http-client-and-server/) 的 GET/JSON/路由，却卡在 **CORS**、Cookie、文件上传？
- 你是否想找 Go 的 WebSocket / SSE 等价物，却不知道 axum 怎么挂？
- 你是否分不清 **tower-http** 的 CorsLayer、限流、压缩、Trace 该怎么叠？
- 你是否在反代后面丢了真实 IP，或不知怎么测 handler（对标 `httptest`）？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| CORS | Cross-Origin Resource Sharing | 跨域资源共享 | 浏览器跨源请求的安全策略与响应头 | `rs/cors` 等中间件 |
| Cookie | — | 小甜饼 | 浏览器自动带回的会话碎片 | `net/http` Cookie |
| multipart | multipart/form-data | 多部分表单 | 上传文件常用的正文编码 | `multipart.Reader` |
| WebSocket | — | 全双工长连接 | HTTP 升级后的双向帧通道 | `gorilla/websocket` 等 |
| SSE | Server-Sent Events | 服务端推送事件 | 服务端单向推文本事件流 | 手写 `text/event-stream` |
| **tower-http** | — | HTTP 中间件包 | CORS/压缩/Trace/限流等 Layer | 中间件链 |
| CorsLayer | — | CORS 层 | tower-http 里配置 CORS 的 Layer | CORS middleware |
| rate limit | — | 限流 | 限制单位时间请求数/并发 | 自研或第三方中间件 |
| X-Forwarded-For | — | 转发客户端 IP 头 | 反代后还原来源 IP（需信任链） | 同名头 |
| `ServiceExt` | — | Tower 服务扩展 | 对 Router 发 oneshot 请求做单测 | `httptest` |
| tungstenite | — | WebSocket 协议库 | 常见 WS 实现；常与 tokio 搭配 | gorilla/websocket 底层感 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q6](#q6), [Q10](#q10) |
| `common` | [Q5](#q5), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q11](#q11), [Q12](#q12) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. axum 里 CORS 最小怎么配？（对标 Go CORS 中间件） {#q1}
**Tags:** `hot` `CORS` `tower-http` `CorsLayer`
**适用版本:** axum + tower-http（版本以 crates.io 为准）

**一句话答案：**
加依赖 **tower-http**，用 **`CorsLayer`**（CORS 层）挂到 Router：允许的 origin / method / header 写清楚。浏览器跨域失败多半是缺这层或配错，不是业务 handler 写错。

**解答：**
```toml
[dependencies]
axum = "0.8"
tower-http = { version = "0.6", features = ["cors"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

```text
use axum::{routing::get, Router};
use tower_http::cors::{Any, CorsLayer};

let cors = CorsLayer::new()
    .allow_origin(Any)           // 生产请改成具体 Origin
    .allow_methods(Any)
    .allow_headers(Any);

let app = Router::new()
    .route("/api/hi", get(|| async { "hi" }))
    .layer(cors);
```

生产口令：

```text
allow_origin = 前端真实 Origin（可多个）
allow_credentials = true 时不能再用 Any origin
预检 OPTIONS 由 CorsLayer 处理，别手写半套
```

**Go 对比：**
```go
import "github.com/rs/cors"
handler := cors.Default().Handler(mux)
```
- **Go 怎么做**：中间件包一层 `http.Handler`。
- **Rust 为什么不同**：tower `Layer` 叠在 Router 上，API 名是 `CorsLayer`。
- **Go 程序员易踩的坑**：只在 handler 里设 `Access-Control-Allow-Origin`，漏掉预检。

**记忆点：**
- CORS → `tower-http` + `CorsLayer`。
- 凭证模式别用 `Any` origin。

---

## Q2. Cookie / Session 在 Rust Web 里怎么做？ {#q2}
**Tags:** `hot` `Cookie` `Session` `axum`
**适用版本:** 生态选型；以当前 crate 文档为准

**一句话答案：**
读/写 Cookie 用 `axum-extra` 的 Cookie jar 或手动 `HeaderMap`；服务端 Session 常把会话 ID 放 Cookie，数据放内存/`moka`/Redis（见 [48-caching](../48-caching-and-redis/)）。对标 Go `gorilla/sessions`：没有单一标准库，组合 Cookie + 存储。

**解答：**
```text
# 常见组合
# Cookie：axum-extra / headers crate
# Session 存储：内存 / Redis / 加密 Cookie（signed）
```

```text
// 写 Cookie 直觉（示意）
// headers.append(SET_COOKIE, "sid=...; Path=/; HttpOnly; Secure; SameSite=Lax");
```

```rust
fn main() {
    // 安全默认：HttpOnly + Secure（HTTPS）+ SameSite
    // 别把 JWT 长期放 localStorage 就以为「不用 Cookie」——XSS/CSRF 模型不同
    println!("cookie = transport; session = server-side state");
}
```

选型：

| 需求 | 做法 |
|------|------|
| 无状态 API | Bearer JWT（见 [46](../46-cryptography-and-hashing/)） |
| 浏览器登录态 | Session ID Cookie + 服务端存储 |
| 简单闪存消息 | 短寿命 Cookie |

**Go 对比：**
- **Go 怎么做**：`http.SetCookie` + gorilla/sessions 等。
- **Rust 为什么不同**：框架不绑死 session 实现。
- **Go 程序员易踩的坑**：找 `axum::session` 官方模块——多半是第三方。

**记忆点：**
- Cookie 传 ID；状态放服务端或加密载荷。
- 浏览器场景优先 `HttpOnly`。

---

## Q3. multipart 文件上传 handler 怎么写？ {#q3}
**Tags:** `hot` `multipart` `upload` `axum`
**适用版本:** axum multipart feature

**一句话答案：**
依赖打开 axum 的 `multipart` feature，handler 参数用 **`Multipart`** 提取器，循环 `next_field()` 读文件名与字节。限制大小用 tower-http 的 body limit，避免被大文件打爆内存。

**解答：**
```toml
[dependencies]
axum = { version = "0.8", features = ["multipart"] }
```

```text
use axum::extract::Multipart;

async fn upload(mut multipart: Multipart) -> Result<String, StatusCode> {
    while let Some(field) = multipart.next_field().await.map_err(|_| StatusCode::BAD_REQUEST)? {
        let name = field.file_name().unwrap_or("unknown").to_string();
        let data = field.bytes().await.map_err(|_| StatusCode::BAD_REQUEST)?;
        // 写盘 / 传对象存储；别默认整文件进内存后无上限
        let _ = (name, data);
    }
    Ok("ok".into())
}
```

```text
// 叠加体积限制（示意）
// .layer(RequestBodyLimitLayer::new(10 * 1024 * 1024))
```

**Go 对比：**
```go
r.ParseMultipartForm(10 << 20)
file, hdr, err := r.FormFile("file")
```
- **Go 怎么做**：`ParseMultipartForm` / `FormFile`。
- **Rust 为什么不同**：提取器异步拉 field；要自觉限流体积。
- **Go 程序员易踩的坑**：忘记 feature，编译找不到 `Multipart`。

**记忆点：**
- `features = ["multipart"]` + `Multipart` 提取器。
- 必加 body 大小上限。

---

## Q4. WebSocket 在 axum 里怎么接？ {#q4}
**Tags:** `hot` `WebSocket` `realtime`
**适用版本:** axum `ws` feature；协议常经 tungstenite

**一句话答案：**
打开 axum **`ws`** feature，路由用 `get(ws_handler)`，handler 里 `WebSocketUpgrade` 再 `on_upgrade`。帧读写在升级后的任务里循环；对标 Go 的 `Upgrader.Upgrade`。

**解答：**
```toml
axum = { version = "0.8", features = ["ws"] }
```

```text
use axum::{
    extract::ws::{Message, WebSocket, WebSocketUpgrade},
    response::IntoResponse,
    routing::get, Router,
};

async fn ws_handler(ws: WebSocketUpgrade) -> impl IntoResponse {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    while let Some(Ok(msg)) = socket.recv().await {
        if let Message::Text(t) = msg {
            let _ = socket.send(Message::Text(t)).await; // echo
        }
    }
}

// Router::new().route("/ws", get(ws_handler))
```

```rust
fn main() {
    // 浏览器: new WebSocket("ws://host/ws")
    // 鉴权: 升级前校验 Cookie/Header；升级后也可再发首帧 token
    println!("upgrade then frame loop");
}
```

**Go 对比：**
```go
upgrader.Upgrade(w, r, nil)
```
- **Go 怎么做**：第三方 Upgrader + Conn 读写。
- **Rust 为什么不同**：axum 提取器封装升级；循环是 async。
- **Go 程序员易踩的坑**：在同步线程里阻塞读 WS——应用 `tokio` 任务。

**记忆点：**
- `WebSocketUpgrade` → `on_upgrade`。
- 业务循环与 HTTP handler 生命周期分开。

---

## Q5. SSE 和 WebSocket 怎么选？ {#q5}
**Tags:** `common` `SSE` `WebSocket`
**适用版本:** 概念选型

**一句话答案：**
只要**服务端推、客户端听**（通知、进度）→ 优先 **SSE**（实现简单、走普通 HTTP）。要**双向**（聊天、协作光标、二进制帧）→ **WebSocket**。不要「凡实时就上 WS」。

**解答：**

| | SSE | WebSocket |
|--|-----|-----------|
| 方向 | 服务端 → 客户端 | 双向 |
| 协议 | HTTP `text/event-stream` | 升级后独立帧 |
| 代理友好 | 通常更好 | 要支持 Upgrade |
| 浏览器 API | `EventSource` | `WebSocket` |

```text
// SSE 直觉：Content-Type: text/event-stream
// data: {"progress":10}\n\n
// 用流式 Body / async_stream 推行
```

```rust
fn main() {
    assert!(true); // 选型表比抄模板重要
}
```

**Go 对比：**
- 同样两套；Go 也常手写 SSE flusher。
- **Go 程序员易踩的坑**：用 WS 做纯进度条——杀鸡用牛刀。

**记忆点：**
- 单向推 → SSE；双向 → WS。

---

## Q6. tower-http 限流 / 并发限制怎么挂？ {#q6}
**Tags:** `hot` `rate-limit` `tower` `ConcurrencyLimitLayer`
**适用版本:** tower / tower-http；以文档为准

**一句话答案：**
用 Tower 的 **`ConcurrencyLimitLayer`**（限制同时处理数）或社区/自研 rate-limit Layer；挂在 Router `.layer(...)`。对标 Go 中间件里的 token bucket / `x/time/rate`。

**解答：**
```text
use tower::limit::ConcurrencyLimitLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(ConcurrencyLimitLayer::new(100)); // 最多 100 个 in-flight
```

```text
# 更细的「每 IP QPS」常需：
# - tower_governor / governor
# - 或反代（nginx/envoy）限流
# 应用内限流是第二道闸
```

```rust
fn main() {
    // 无界并发 + 慢下游 = 雪崩；先有上限再谈优化
    let max_in_flight = 256usize;
    assert!(max_in_flight > 0);
}
```

**Go 对比：**
```go
limiter := rate.NewLimiter(rate.Limit(10), 20)
```
- **Go 怎么做**：`x/time/rate` 或中间件。
- **Rust 为什么不同**：Layer 组合；细节 crate 分散。
- **Go 程序员易踩的坑**：只限路由层、不限全局 in-flight。

**记忆点：**
- 先 `ConcurrencyLimit`；细粒度 QPS 再专项 crate/网关。

---

## Q7. 反代后如何信任 `X-Forwarded-*`？ {#q7}
**Tags:** `common` `X-Forwarded-For` `proxy`
**适用版本:** 部署惯例

**一句话答案：**
只信任**你自己的**反代写入的转发头；用 `Forwarded` / `X-Forwarded-For` 还原客户端 IP 时要配置「可信跳数」。裸奔公网时**不要**盲信客户端自带的 `X-Forwarded-For`。

**解答：**
```text
Client → CDN/LB → 你的反代 → Rust 服务
                    ↑ 只信这一跳写入的头
```

```text
# 常见需求
# - 真实 IP 做限流/审计
# - 生成绝对 URL 时的 scheme/host（X-Forwarded-Proto）
# axum 生态有 ForwardedHeaderLayer 一类（以当前文档为准）
```

```rust
fn main() {
    // 安全默认：忽略外来 XFF，除非前面是受信反代
    println!("trust hop count, don't trust the internet");
}
```

**Go 对比：**
- 同样问题；`gin` 等有 `TrustedProxies`。
- **Go 程序员易踩的坑**：日志里直接打 `X-Forwarded-For` 当真实 IP。

**记忆点：**
- 受信代理 + 跳数；否则当不可信。

---

## Q8. 大文件下载 / `Content-Disposition` 怎么设？ {#q8}
**Tags:** `common` `download` `Content-Disposition`
**适用版本:** axum / http 类型

**一句话答案：**
流式响应（`Body` 从文件/`AsyncRead` 来），设 `Content-Type` 与 **`Content-Disposition: attachment; filename="..."`**。别 `read_to_end` 整文件进内存再返回。

**解答：**
```text
// 示意
// headers.insert(CONTENT_DISPOSITION, "attachment; filename=\"report.csv\"");
// Body::from_stream(ReaderStream::new(file))
```

```rust
fn main() {
    let disposition = "attachment; filename=\"a.csv\"";
    assert!(disposition.contains("attachment"));
}
```

```text
# Range 断点续传：按需再加；先保证流式与正确文件名编码
```

**Go 对比：**
```go
w.Header().Set("Content-Disposition", "attachment; filename=a.csv")
http.ServeContent(w, r, name, modtime, content)
```
- 心智相同：头 + 流式。

**记忆点：**
- 下载 = 流式 Body + Disposition。
- 大文件禁止整包进 `Vec<u8>`。

---

## Q9. reqwest 怎么发 multipart / 看上传？ {#q9}
**Tags:** `common` `reqwest` `multipart` `client`
**适用版本:** reqwest multipart feature

**一句话答案：**
`reqwest` 打开 `multipart` feature，用 `multipart::Form` 加文本字段与 `File`/`Part`，再 `.multipart(form).send().await`。进度要自己包读流或看社区方案，不是默认一行 API。

**解答：**
```toml
reqwest = { version = "0.12", features = ["multipart", "json"] }
```

```text
use reqwest::multipart::{Form, Part};

let form = Form::new()
    .text("title", "doc")
    .part("file", Part::bytes(data).file_name("a.bin"));

let resp = client.post(url).multipart(form).send().await?;
```

```rust
fn main() {
    println!("client multipart ≠ server Multipart extractor, but same MIME idea");
}
```

**Go 对比：**
```go
writer := multipart.NewWriter(&buf)
```
- 都是拼 multipart body；Rust 常走 reqwest 封装。

**记忆点：**
- feature `multipart` + `Form`。
- 进度条要额外做。

---

## Q10. 怎么测 axum handler？（对标 `httptest`） {#q10}
**Tags:** `hot` `testing` `ServiceExt` `httptest`
**适用版本:** axum + tower；测试依赖

**一句话答案：**
把 `Router` 当 Tower `Service`，用 **`oneshot`**（`ServiceExt`）发 `Request`，断言 `Response`——这就是 Go `httptest` 的常见 Rust 写法。也可用 `axum-test` 等更高层封装。

**解答：**
```toml
[dev-dependencies]
tower = { version = "0.5", features = ["util"] }
http-body-util = "0.1"
```

```text
use axum::{body::Body, http::Request, routing::get, Router};
use tower::ServiceExt; // oneshot

let app = Router::new().route("/", get(|| async { "hi" }));
let res = app.oneshot(Request::builder().uri("/").body(Body::empty())?).await?;
assert_eq!(res.status(), 200);
```

```rust
fn main() {
    // 不升端口、不起真 TCP：单测更快更稳
    println!("Router as Service ≈ httptest");
}
```

**Go 对比：**
```go
rec := httptest.NewRecorder()
mux.ServeHTTP(rec, req)
```
- **Go 怎么做**：`httptest` + `ServeHTTP`。
- **Rust 为什么不同**：`oneshot` 走 Tower 服务接口。
- **Go 程序员易踩的坑**：集成测试一律 `TcpListener`——单测过重。

**记忆点：**
- `ServiceExt::oneshot` = 进程内 httptest。
- 真端口留给少量集成测试。

---

## Q11. 常见 tower-http Layer 怎么选？ {#q11}
**Tags:** `common` `tower-http` `Layer` `cheatsheet`
**适用版本:** tower-http 0.5/0.6 一带

**一句话答案：**
按需叠 Layer：Trace（日志）、CORS、Compression、Timeout、RequestBodyLimit、SetHeader。顺序有意义——一般「外层先看到请求」（具体以文档与实验为准）。

**解答：**

| Layer | 用途 | Go 近亲 |
|-------|------|---------|
| `TraceLayer` | 请求日志/span | 访问日志中间件 |
| `CorsLayer` | 跨域 | CORS middleware |
| `CompressionLayer` | gzip 等 | gzip handler |
| `TimeoutLayer` | 超时 | 中间件 timeout |
| `RequestBodyLimitLayer` | 限制正文 | `MaxBytesReader` |
| `SetRequestIdLayer` 等 | 请求 ID | 自研中间件 |

```text
Router::new()
  .route(...)
  .layer(TraceLayer::new_for_http())
  .layer(cors)
  .layer(CompressionLayer::new());
```

```rust
fn main() {
    println!("layer order matters; start with trace + limits");
}
```

**Go 对比：**
- 中间件洋葱模型相同。
- **Go 程序员易踩的坑**：把所有 Layer 当无序装饰器。

**记忆点：**
- 先限大小/超时，再业务；CORS/Trace 按团队惯例叠。

---

## Q12. 和 Go `net/http` 中间件链怎么整表对照？ {#q12}
**Tags:** `common` `cheatsheet` `Go`
**适用版本:** 概念对照

**一句话答案：**
Go 的 `Handler` 包装 ≈ Tower `Layer`/`Service`；`httptest` ≈ `oneshot`；CORS/gzip/限流在 Rust 多落在 **tower-http** 与社区 Layer。入门 JSON API 见 [40](../40-http-client-and-server/)；本篇补浏览器与实时场景。

**解答：**

| Go | Rust |
|----|------|
| 中间件 `func(http.Handler) http.Handler` | `Layer` / middleware fn |
| `httptest` | `ServiceExt::oneshot` |
| CORS 中间件 | `CorsLayer` |
| WebSocket 升级 | `WebSocketUpgrade` |
| `ParseMultipartForm` | `Multipart` 提取器 |
| `SetCookie` | Cookie jar / `SET_COOKIE` |
| `x/time/rate` | governor / ConcurrencyLimit |

```rust
fn main() {
    println!("40 = basics; 52 = browser + realtime + layers");
}
```

**记忆点：**
- 基础走 40；跨域/上传/WS/测 handler 走本篇。
- Layer = 中间件的 Rust 口音。
