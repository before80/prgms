+++
title = "40-HTTP 客户端与服务端"
date = 2026-07-28T14:49:00+08:00
weight = 400
type = "docs"
description = "面向 Go 用户讲清 reqwest/axum 客户端与服务端、路由 State 与优雅关停"
isCJKLanguage = true
draft = false

+++

# HTTP 客户端与服务端入门 (HTTP Client and Server)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否习惯了 Go 的 `net/http`，一进 Rust 就找「标准库 HTTP」，却发现 std 几乎没有？
- 你是否想用几行代码发 GET/POST JSON，却不知道该选哪个 client crate、超时和 Header 怎么设？
- 你是否想写一个最小 hello 服务、带路径参数和 query，却分不清 axum 路由怎么挂？
- 你是否想返回 JSON、共享 State、加中间件，却不知道和 Go 的 ServeMux / middleware 怎么对照？
- 你是否纠结：怎么优雅关停、怎么测 handler、什么时候才需要碰 tower？
- 你是否分不清 reqwest 的 rustls 与 native-tls，或不知道 Authorization 鉴权头怎么挂？
- 你是否在找 CORS / WebSocket / multipart？→ 见 [52-http-advanced](../52-http-advanced-and-realtime/)。

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| HTTP | HyperText Transfer Protocol | 超文本传输协议 | Web 上最常用的请求/响应协议 | 同名 |
| client | — | 客户端 | 主动发请求、收响应的一方 | `http.Client` |
| server | — | 服务端 | 监听端口、处理请求的一方 | `http.Server` |
| **reqwest** | request（谐音） | 常用 HTTP 客户端 crate | 高层封装，默认 async | `net/http` Client |
| **axum** | — | 常用 Web 框架 | 基于 tower/hyper 的路由与提取器 | `ServeMux` + 中间件生态 |
| hyper | — | 底层 HTTP 实现 | 偏底层的 HTTP 库，很多框架建其上 | 更接近自己拼 `http.Server` |
| tower | — | 服务中间件栈 | `Service` trait + 层叠 Layer | 中间件链 / RoundTripper |
| extractor | — | 提取器 | 从请求里抽出 Path/Query/Json/State 等 | 手写 `r.URL` / `json.NewDecoder` |
| State | — | 共享状态 | 注入到 handler 的应用级数据（连接池等） | 闭包捕获 / 结构体字段 |
| middleware | — | 中间件 | 包在 handler 外的横切逻辑（日志、鉴权） | `http.Handler` 包装 |
| graceful shutdown | — | 优雅关停 | 停接新连接，等在途请求结束再退出 | `Shutdown` / `ShutdownContext` |
| status code | — | 状态码 | 如 200/404/500，表示结果类别 | `http.StatusOK` 等 |
| JSON | JavaScript Object Notation | JSON | 常见 API 正文格式 | `encoding/json` |
| serde | SERialize/DEserialize | 序列化框架 | 类型 ↔ JSON 等格式；详见 [36-serde](../36-serde-and-serialization/) | `encoding/json` |
| async | asynchronous | 异步 | 用 Future/`.await` 做并发 I/O；详见 [31-async](../31-async-programming/) | goroutine + 阻塞 I/O 或异步库 |
| rustls | — | 纯 Rust TLS 实现 | reqwest 常用的 TLS 后端之一 | 自定义 `tls.Config` / 纯 Go TLS |
| native-tls | — | 系统原生 TLS | 走平台 TLS（Schannel/Secure Transport/OpenSSL） | 系统证书库那条路 |
| Authorization | — | 鉴权头 | 常见 `Bearer` / `Basic` 凭证所在 Header | `req.Header.Set("Authorization", ...)` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q14](#q14), [Q15](#q15) |
| `common` | [Q4](#q4), [Q8](#q8), [Q10](#q10), [Q11](#q11), [Q13](#q13) |
| `occasional` | [Q9](#q9), [Q12](#q12) |
| `advanced` | — |

---

## Q1. 为什么 Rust 不像 Go 那样在标准库里内建 `net/http`？ {#q1}
**Tags:** `hot` `beginner` `stdlib` `ecosystem`
**适用版本:** Rust 1.0+（生态选型；与具体 crate 版本无关）

**一句话答案：**
Rust 标准库刻意保持「最小可用」：提供 TCP/UDP、部分 TLS 相关能力的基础，但不绑定某一套 HTTP 客户端/服务端 API；社区用 **reqwest**（客户端）、**axum** / **hyper**（服务端）等 crate 组合，由 Cargo 选版本与 feature。

**解答：**
Go 把 HTTP 当成「语言自带电池」：`net/http` 从 std 直接 `import`，API 稳定、文档统一。Rust 的哲学更接近「语言 + 包管理器」：

| 层级 | Rust 常见选择 | Go |
|------|---------------|-----|
| 字节流 / 套接字 | `std::net`、`tokio::net` | `net` |
| HTTP 语义 | `http` crate（类型）+ hyper | `net/http` |
| 好用的 Client | **reqwest** | `http.Client` |
| 好用的 Server 框架 | **axum**、Actix、Rocket… | 多半仍基于 `net/http` |

```toml
# 典型依赖组合（示意，版本随你锁定）
[dependencies]
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.12", features = ["json"] }
axum = "0.8"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

这意味着：没有「唯一官方 HTTP」，但有「事实上的主流组合」。选型成本换来的是：feature 可裁剪（JSON、rustls/native-tls、blocking）、版本可升级、不把重量级协议绑进 std。

异步运行时（Tokio 等）也不在 std 里——HTTP 栈几乎都建立在 async 之上，详见 [31-async-programming](../31-async-programming/)。

**Go 对比：**
```go
import "net/http" // 标准库即开即用

resp, err := http.Get("https://example.com")
```
- **Go 怎么做**：stdlib 提供 Client、Server、ServeMux、默认 Transport。
- **Rust 为什么不同**：避免把协议细节与 TLS/异步模型永久钉死在 std；用生态迭代。
- **Go 程序员易踩的坑**：搜「Rust http 标准库」无果就以为不能写 HTTP——其实是 `cargo add reqwest` / `axum`。

**记忆点：**
- std ≈ 套接字与基础类型；HTTP 在 crates.io。
- 入门默认：客户端 reqwest，服务端 axum。

---

## Q2. 用 reqwest 怎么发一个 GET？ {#q2}
**Tags:** `hot` `beginner` `reqwest` `GET` `client`
**适用版本:** reqwest 0.11+/0.12.x；需 Tokio 等 async runtime

**一句话答案：**
`reqwest::get(url).await?` 或先建 `Client` 再 `.get(url).send().await?`；响应用 `.text()` / `.bytes()` / `.json()` 取正文。记得这是 **async**，要在 `#[tokio::main]` 里跑。

**解答：**
最小依赖：

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
reqwest = "0.12"
```

一次性 GET：

```text
#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let body = reqwest::get("https://httpbin.org/get")
        .await?
        .error_for_status()? // 4xx/5xx 变成 Err
        .text()
        .await?;
    println!("{body}");
    Ok(())
}
```

可复用的 **Client**（连接池、默认超时更好管）：

```text
let client = reqwest::Client::new();
let resp = client
    .get("https://httpbin.org/get")
    .query(&[("page", "1")])
    .send()
    .await?;
println!("status = {}", resp.status());
```

`reqwest::get` 适合脚本；应用里更常持有一个 `Client` 克隆共享（内部是 `Arc`）。TLS、代理、cookie 等用 `Client::builder()`。

**Go 对比：**
```go
resp, err := http.Get("https://httpbin.org/get")
if err != nil { /* ... */ }
defer resp.Body.Close()
```
- **Go 怎么做**：`http.Get` / `client.Do`；别忘关 `Body`。
- **Rust 为什么不同**：默认走 async Future；阻塞版要用 `reqwest` 的 `blocking` feature。
- **Go 程序员易踩的坑**：在非 async 上下文直接 `.await`；或忘了 `error_for_status`，把 404 当成功读 body。

**记忆点：**
- 脚本：`reqwest::get`；长期：`Client::new()`。
- 先看 `status()`，再读 body。

---

## Q3. 怎么 POST JSON？状态码怎么处理？ {#q3}
**Tags:** `hot` `reqwest` `POST` `JSON` `status`
**适用版本:** reqwest 0.12（需 `json` feature）；serde 1.x

**一句话答案：**
打开 reqwest 的 `json` feature，用 `.json(&value)` 发 body；用 `resp.status()` / `error_for_status()` 处理状态码；反序列化用 `.json::<T>().await`。类型侧依赖 **serde**（见 [36-serde-and-serialization](../36-serde-and-serialization/)）。

**解答：**

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1", features = ["derive"] }
```

```text
use serde::Serialize;

#[derive(Serialize)]
struct CreateUser<'a> {
    name: &'a str,
    age: u32,
}

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let client = reqwest::Client::new();
    let resp = client
        .post("https://httpbin.org/post")
        .json(&CreateUser { name: "Ada", age: 36 })
        .send()
        .await?;

    let status = resp.status();
    if !status.is_success() {
        // 或 resp.error_for_status()?; 把非 2xx 变成 Err
        eprintln!("unexpected status: {status}");
    }

    let v: serde_json::Value = resp.json().await?;
    println!("{v}");
    Ok(())
}
```

状态码习惯：
- `status.is_success()` / `is_client_error()` / `is_server_error()`
- 希望「非 2xx 直接失败」→ `error_for_status()`（消费响应，变 `Err`）
- 要读错误正文再决定 → 先看 status，再 `.text()` / `.json()`

Content-Type：`.json(...)` 会设为 `application/json`。

**Go 对比：**
```go
b, _ := json.Marshal(payload)
resp, err := http.Post(url, "application/json", bytes.NewReader(b))
```
- **Go 怎么做**：自己 Marshal + 设 Content-Type；或第三方客户端封装。
- **Rust 为什么不同**：`.json(&T)` 把 serde 序列化与 Header 绑在一起。
- **Go 程序员易踩的坑**：忘开 `features = ["json"]`，`.json` 方法不存在。

**记忆点：**
- POST JSON = `.post(url).json(&body).send().await`。
- 状态码用 `status()` 或 `error_for_status()`。

---

## Q4. 超时和自定义 Header 怎么设？ {#q4}
**Tags:** `common` `reqwest` `timeout` `header`
**适用版本:** reqwest 0.12.x

**一句话答案：**
在 `Client::builder().timeout(...)` 设默认超时；单次请求用 `.timeout(...)` / `.header(...)`；需要「连接超时 vs 整体超时」时用 builder 的更细选项或自己包一层 `tokio::time::timeout`。

**解答：**

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
reqwest = "0.12"
```

```text
use std::time::Duration;
use reqwest::header::{HeaderMap, HeaderValue, USER_AGENT};

let mut headers = HeaderMap::new();
headers.insert(USER_AGENT, HeaderValue::from_static("my-app/1.0"));
headers.insert("X-Request-Id", HeaderValue::from_static("abc-123"));

let client = reqwest::Client::builder()
    .default_headers(headers)
    .timeout(Duration::from_secs(10)) // 整个请求的默认超时
    .build()?;

let resp = client
    .get("https://httpbin.org/delay/1")
    .header("Accept", "application/json")
    .timeout(Duration::from_secs(3)) // 覆盖本次
    .send()
    .await?;
```

超时到了会返回 `reqwest::Error`（可 `is_timeout()` 判断）。Header 名用常量（如 `AUTHORIZATION`）或字符串；非法字符会在 `HeaderValue` 构造时失败。

需要「最多等 2 秒，不管 client 默认」时，也可：

```text
let fut = client.get(url).send();
let resp = tokio::time::timeout(Duration::from_secs(2), fut).await??;
```

**Go 对比：**
```go
client := &http.Client{Timeout: 10 * time.Second}
req.Header.Set("X-Request-Id", "abc-123")
```
- **Go 怎么做**：`Client.Timeout` + `Header.Set`；更细可用 `context.WithTimeout`。
- **Rust 为什么不同**：同样分「Client 默认」与「单次覆盖」；async 下还可用 `tokio::time::timeout`。
- **Go 程序员易踩的坑**：只设了连接相关超时却以为覆盖了读 body 全程——先读清 reqwest 文档里 timeout 的范围。

**记忆点：**
- 默认超时挂在 `Client::builder`；单次用 `.timeout` / `.header`。
- 超时错误用 `err.is_timeout()` 分支。

---

## Q5. axum 最小 hello 服务怎么写？ {#q5}
**Tags:** `hot` `beginner` `axum` `server` `hello`
**适用版本:** axum 0.7+/0.8.x；tokio 1.x

**一句话答案：**
`Router::new().route("/", get(handler))`，再 `axum::serve(listener, app).await`；handler 可以是返回 `impl IntoResponse` 的 async 函数。

**解答：**

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "net"] }
axum = "0.8"
```

```text
use axum::{routing::get, Router};

async fn hello() -> &'static str {
    "hello"
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(hello));
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

浏览器或 curl：

```bash
curl http://127.0.0.1:3000/
# hello
```

要点：
- handler 签名由 **extractor**（提取器）决定参数、由返回值决定响应。
- `serve` 需要先 `bind` 出 `TcpListener`（较新 axum 的常见写法）。
- 生产还要日志、超时、关停——见后面几题。

**Go 对比：**
```go
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "hello")
})
log.Fatal(http.ListenAndServe(":3000", nil))
```
- **Go 怎么做**：`HandleFunc` + `ListenAndServe`。
- **Rust 为什么不同**：路由树是 `Router`，服务跑在 async runtime 上。
- **Go 程序员易踩的坑**：找 `http.ListenAndServe` 同名 API——在 axum 里是 `TcpListener` + `axum::serve`。

**记忆点：**
- `route + get(handler) + serve(listener, app)`。
- handler 就是 async 函数。

---

## Q6. 路由、路径参数、query 怎么写？ {#q6}
**Tags:** `hot` `axum` `route` `path` `query`
**适用版本:** axum 0.8.x

**一句话答案：**
`.route("/users/{id}", get(...))` 用 `Path` 抽路径参数；`Query<T>` 抽查询串；可用 `Router` 嵌套 `nest` / `merge` 组织模块。

**解答：**

```text
use axum::{
    extract::{Path, Query},
    routing::get,
    Router,
};
use serde::Deserialize;

#[derive(Deserialize)]
struct Page {
    page: Option<u32>,
    q: Option<String>,
}

async fn get_user(Path(id): Path<u64>) -> String {
    format!("user={id}")
}

async fn search(Query(p): Query<Page>) -> String {
    format!("page={:?} q={:?}", p.page, p.q)
}

fn app() -> Router {
    Router::new()
        .route("/users/{id}", get(get_user))
        .route("/search", get(search))
}
```

```bash
curl 'http://127.0.0.1:3000/users/42'
curl 'http://127.0.0.1:3000/search?page=2&q=rust'
```

路径语法随 axum 版本可能是 `{id}` 或 `:id`——以你锁定的版本文档为准；类型不匹配（非数字 id）会变成 400 一类失败响应。

多段参数：`Path((a, b)): Path<(u64, String)>` 或自定义结构体。嵌套：

```text
let api = Router::new().route("/users/{id}", get(get_user));
let app = Router::new().nest("/api/v1", api);
```

**Go 对比：**
```go
// 标准库常手写切 path，或用 chi/gin 的 /users/{id}
r.Get("/users/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
})
```
- **Go 怎么做**：stdlib 弱路由；常用第三方 mux。
- **Rust 为什么不同**：axum 把 Path/Query 做成类型化 extractor。
- **Go 程序员易踩的坑**：把 query 当 path；或 `Page` 字段名与 query key 不一致却怪框架。

**记忆点：**
- 路径 → `Path`；查询 → `Query` + Deserialize。
- 用 `nest` 拼前缀。

---

## Q7. 怎么返回 JSON？和 serde 什么关系？ {#q7}
**Tags:** `hot` `axum` `JSON` `serde` `IntoResponse`
**适用版本:** axum 0.8（通常已带 json）；serde 1.x

**一句话答案：**
返回 `Json(value)`（axum 的 JSON 响应包装）；`value` 需实现 serde 的 `Serialize`。请求体用 `Json<T>` extractor，`T: Deserialize`。序列化细节见 [36-serde-and-serialization](../36-serde-and-serialization/)。

**解答：**

```toml
[dependencies]
axum = "0.8"
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread", "net"] }
```

```text
use axum::{extract::Json, routing::{get, post}, Router};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}

async fn get_user() -> Json<User> {
    Json(User { id: 1, name: "Ada".into() })
}

async fn create_user(Json(body): Json<CreateUser>) -> Json<User> {
    Json(User { id: 99, name: body.name })
}

fn app() -> Router {
    Router::new()
        .route("/users/1", get(get_user))
        .route("/users", post(create_user))
}
```

也可返回 `(StatusCode, Json(T))` 控制状态码。反序列化失败时，axum 默认会变成客户端错误响应（具体状态码/body 可自定义 rejection）。

**Go 对比：**
```go
json.NewEncoder(w).Encode(user)
json.NewDecoder(r.Body).Decode(&in)
```
- **Go 怎么做**：手写 Encoder/Decoder，或框架绑定。
- **Rust 为什么不同**：`Json<T>` 把 HTTP 与 serde 粘在类型上。
- **Go 程序员易踩的坑**：结构体没 `Serialize`/`Deserialize` 就包 `Json`——编译期直接拒绝。

**记忆点：**
- 出站：`Json(T)` + `Serialize`。
- 入站：`Json<T>` + `Deserialize`。

---

## Q8. State 和中间件怎么加？ {#q8}
**Tags:** `common` `axum` `State` `middleware`
**适用版本:** axum 0.8.x

**一句话答案：**
用 `.with_state(s)` 注入共享状态，handler 参数写 `State(s)`；横切逻辑用 `Router::layer(...)` 挂 **middleware**（中间件），常见来自 `tower-http`（trace、cors、timeout）。

**解答：**

```text
use axum::{
    extract::State,
    routing::get,
    Router,
};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    // 例如数据库池、配置；用 Arc 包重资源
    hit: Arc<std::sync::atomic::AtomicU64>,
}

async fn hits(State(st): State<AppState>) -> String {
    let n = st.hit.fetch_add(1, std::sync::atomic::Ordering::Relaxed) + 1;
    format!("hits={n}")
}

fn app(state: AppState) -> Router {
    Router::new()
        .route("/hits", get(hits))
        .with_state(state)
}
```

中间件示例（依赖 `tower-http`）：

```toml
[dependencies]
axum = "0.8"
tower-http = { version = "0.6", features = ["trace", "timeout"] }
```

```text
use tower_http::trace::TraceLayer;
use std::time::Duration;
use tower_http::timeout::TimeoutLayer;

let app = Router::new()
    .route("/", get(|| async { "ok" }))
    .layer(TraceLayer::new_for_http())
    .layer(TimeoutLayer::new(Duration::from_secs(30)))
    .with_state(state);
```

`State` 类型必须 `Clone`（框架会克隆进每个请求）；重资源放进 `Arc`。中间件顺序：后 `layer` 的更靠外（与 tower 惯例一致，写的时候对一下文档）。

**Go 对比：**
```go
type mw func(http.Handler) http.Handler
mux := http.NewServeMux()
http.ListenAndServe(":3000", logging(mux))
```
- **Go 怎么做**：闭包捕获依赖；`Handler` 包装做中间件。
- **Rust 为什么不同**：`State` extractor + `Service`/`Layer` 类型栈（tower）。
- **Go 程序员易踩的坑**：`State` 里塞未 `Clone` 的池子；应 `Arc<Pool>` + `#[derive(Clone)]` 外层。

**记忆点：**
- 共享依赖 → `with_state` + `State`。
- 日志/超时/CORS → `layer` + tower-http。

---

## Q9. 优雅关停怎么简述？ {#q9}
**Tags:** `occasional` `graceful-shutdown` `axum` `signal`
**适用版本:** axum 0.8；tokio 1.x

**一句话答案：**
监听 Ctrl+C / SIGTERM，对 `axum::serve(...).with_graceful_shutdown(signal)` 传入一个「等到信号就完成」的 Future；进程停接新连接，尽量等在途请求结束后再退出。

**解答：**
思路与 Go 的 `Shutdown` 相同：**graceful shutdown**（优雅关停）= 不再接受新请求 + 等待已有请求完成（可带超时）。

```text
async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("failed to install Ctrl+C handler");
}

// 示意：
// axum::serve(listener, app)
//     .with_graceful_shutdown(shutdown_signal())
//     .await
//     .unwrap();
```

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "net", "signal"] }
axum = "0.8"
```

生产上常再加：关停超时（到期强制停）、把信号接到 K8s 的 preStop、把客户端的 idle 连接也清掉。细节因部署环境而异，本篇只要求记住「信号 Future + `with_graceful_shutdown`」这条主线。

**Go 对比：**
```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
defer stop()
server.Shutdown(ctx)
```
- **Go 怎么做**：`signal.Notify` + `Server.Shutdown`。
- **Rust 为什么不同**：关停挂在 serve 的 Future 上，而不是另起一个阻塞 `Shutdown` 调用那么「命令式」。
- **Go 程序员易踩的坑**：只 `ctrl_c` 退出整个进程，不挂 graceful——在途请求被掐断。

**记忆点：**
- 信号 Future → `with_graceful_shutdown`。
- 先停接入，再等在途。

---

## Q10. 和 Go 的 Client / ServeMux 怎么对照？ {#q10}
**Tags:** `common` `go` `Client` `ServeMux` `对照`
**适用版本:** 概念对照；reqwest / axum 主流版本

**一句话答案：**
`http.Client` ≈ `reqwest::Client`；`http.ServeMux` / `HandleFunc` ≈ `axum::Router` + `route`；中间件在 Go 常是 `Handler` 包装，在 Rust 常是 tower `Layer`；JSON 在 Go 靠 `encoding/json`，在 Rust 靠 serde + `Json`。

**解答：**

| 职责 | Go | Rust（本篇默认） |
|------|----|------------------|
| 发请求 | `http.Client` / `http.Get` | `reqwest::Client` |
| 超时 | `Client.Timeout` / context | `Client::builder().timeout` / `tokio::time::timeout` |
| Header | `Header.Set` | `.header` / `HeaderMap` |
| 听端口 | `ListenAndServe` | `TcpListener` + `axum::serve` |
| 路由 | `ServeMux` / chi / gin | `Router::route` / `nest` |
| 共享依赖 | 闭包 / 结构体 | `State` |
| 中间件 | 包装 `Handler` | `layer`（tower） |
| JSON | `encoding/json` | serde + axum `Json` |
| 关停 | `Server.Shutdown` | `with_graceful_shutdown` |

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /users/{id}", getUser)
client := &http.Client{Timeout: 10 * time.Second}
```

```text
let app = Router::new().route("/users/{id}", get(get_user));
let client = reqwest::Client::builder()
    .timeout(Duration::from_secs(10))
    .build()?;
```

心智转换：Go 是「一个包打天下」；Rust 是「runtime + client crate + server crate + serde」拼装。拼装换来的是 feature 裁剪与类型化 extractor。

**Go 对比：**
- **Go 怎么做**：stdlib 一条链学完就能上线原型。
- **Rust 为什么不同**：把协议实现留给生态，用类型系统表达提取与中间件。
- **Go 程序员易踩的坑**：按包名一一对应去找 `net/http`，而不是按「Client / Router / JSON」三张表选型。

**记忆点：**
- Client → reqwest；Mux → axum Router。
- 先对照职责表，再记 API 名。

---

## Q11. 怎么测 handler？ {#q11}
**Tags:** `common` `test` `axum` `handler`
**适用版本:** axum 0.8；建议 `tower::ServiceExt`；`tokio` test

**一句话答案：**
把 `Router` 当 `Service`，用 `oneshot` 发组装好的 `Request`，断言 status 与 body；或抽纯函数测业务，handler 只做薄封装。不必真的 `bind` 端口。

**解答：**

```toml
[dev-dependencies]
# 版本与主依赖对齐
tower = { version = "0.5", features = ["util"] }
http-body-util = "0.1"
```

```text
#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::{Request, StatusCode},
    };
    use tower::ServiceExt; // for oneshot

    #[tokio::test]
    async fn hello_ok() {
        let app = Router::new().route("/", get(|| async { "hello" }));
        let resp = app
            .oneshot(Request::builder().uri("/").body(Body::empty()).unwrap())
            .await
            .unwrap();
        assert_eq!(resp.status(), StatusCode::OK);
        // 再读 body：http_body_util::BodyExt::collect ...
    }
}
```

策略：
- **路由/extractor/状态码**：`oneshot` 集成测 Router。
- **纯业务**：`fn logic(...)` 单测，handler 一行调用——更快、少依赖 HTTP 类型。
- 需要真 TCP 时再用 `TcpListener::bind("127.0.0.1:0")` 起临时端口（更重）。

带 `State` 时：`Router::with_state(test_state)` 再 `oneshot`。

**Go 对比：**
```go
req := httptest.NewRequest(http.MethodGet, "/", nil)
rr := httptest.NewRecorder()
handler.ServeHTTP(rr, req)
```
- **Go 怎么做**：`httptest` + `ResponseRecorder`。
- **Rust 为什么不同**：axum 走 tower `Service`，用 `oneshot` 最省事。
- **Go 程序员易踩的坑**：为每个单测都 `ListenAndServe`——慢且易端口冲突。

**记忆点：**
- 默认：`Router` + `oneshot`，不绑端口。
- 业务逻辑尽量纯函数化。

---

## Q12. 什么时候才需要碰 tower？ {#q12}
**Tags:** `occasional` `tower` `Service` `Layer` `advanced-lite`
**适用版本:** tower 0.4/0.5；与 axum 配套使用

**一句话答案：**
写普通 CRUD 时，用 axum 的 `route` / `State` / `tower-http` 现成 Layer 就够；当你要自定义中间件、限流、连接池式 `Service` 组合，或读懂 axum「一切都是 Service」时，再深入 **tower** 的 `Service` / `Layer`。

**解答：**
**tower** 定义了异步服务的核心抽象：

- `Service`：`poll_ready` + `call(Request) -> Future<Response>`
- `Layer`：把一个 `Service` 包成另一个（中间件）

axum 的 `Router` 本身就是 `Service`；你 `.layer(TraceLayer::...)` 时已经在用 tower，只是不直接写 trait。

该碰 tower 源码/文档的信号：
- 要写「通用中间件」而 `from_fn` 不够用
- 要理解 `Buffer`、`RateLimit`、`Retry`、负载均衡等 tower 工具层
- 要把非 HTTP 的请求也统一成 `Service` 接口
- 调试时错误信息出现 `tower::Service` / `Layer` 边界

```text
// 概念示意（非完整程序）：Layer 包 Service
// Service = 处理 Request
// Layer(Service) = 先做前置逻辑，再调内层 Service
```

入门路径建议：先 axum 官方中间件示例 → `tower-http` → 再读 tower 的 `Service` 教程。过早手写 `Service` 实现收益低。

**Go 对比：**
- **Go 怎么做**：中间件就是 `func(http.Handler) http.Handler`；没有强制统一的 `Service` trait 生态（但有类似模式）。
- **Rust 为什么不同**：tower 把「可组合服务」做成跨 HTTP/gRPC/自定义协议的共同语言。
- **Go 程序员易踩的坑**：一上来就实现 `Service`，其实 `axum::middleware::from_fn` 已覆盖大多数需求。

**记忆点：**
- 日常：axum + tower-http。
- 定制组合/读透栈：再学 tower。

---

## Q13. reqwest 该选 rustls 还是 native-tls？ {#q13}
**Tags:** `common` `reqwest` `rustls` `native-tls` `TLS`
**适用版本:** reqwest 0.12.x（feature 名以当前文档为准）

**一句话答案：**
默认优先 **rustls**（纯 Rust TLS）：跨平台行为更一致、依赖链更清晰；只有需要对接系统证书库/企业定制 OpenSSL、或平台强制原生栈时，再开 **native-tls**。二者是 Cargo feature 二选一（或显式指定），不是运行时开关。

**解答：**

```toml
# 常见：显式 rustls（许多模板默认已是这条）
reqwest = { version = "0.12", default-features = false, features = ["json", "rustls-tls"] }

# 需要系统 TLS 时：
# reqwest = { version = "0.12", default-features = false, features = ["json", "native-tls"] }
```

用法本身不变：

```text
let client = reqwest::Client::builder()
    .timeout(std::time::Duration::from_secs(10))
    .build()?;
let resp = client.get("https://example.com").send().await?;
```

怎么选：

| 诉求 | 更合适 |
|------|--------|
| Linux 容器、CI、行为可复现 | rustls |
| 必须用系统根证书/企业中间件注入的 CA | native-tls（或 rustls + 自定义根） |
| Windows/macOS 想跟 OS 信任库完全一致 | 常选 native-tls |
| 静态链接、少动态库 | 倾向 rustls |

「❌ 错误思路」——在代码里 `if cfg!(windows) { ... }` 换 API：TLS 后端是编译期 feature，不是两套 Client 类型。

**Go 对比：**
- **Go 怎么做**：默认用自己的 TLS 栈 + 系统根；很少在应用里「二选一 crate」。
- **Rust 为什么不同**：reqwest 把 TLS 实现做成可裁剪 feature。
- **Go 程序员易踩的坑**：两个 feature 同时胡开导致冲突，或容器里缺系统 CA 却选了 native-tls。

**记忆点：**
- 默认想 rustls；有系统 TLS 硬需求再 native-tls。
- 换后端改 `Cargo.toml`，不改业务调用。

---

## Q14. Authorization / 鉴权头怎么挂？ {#q14}
**Tags:** `hot` `Authorization` `Bearer` `auth` `header`
**适用版本:** reqwest 0.12.x；axum 侧同属 HTTP Header 概念

**一句话答案：**
客户端用 `.bearer_auth(token)` / `.basic_auth(user, pass)`，或 `.header(AUTHORIZATION, ...)`；需要每个请求都带时，放进 `Client::builder().default_headers(...)`。服务端从 Header 读取并校验——别把 token 塞进 URL query。

**解答：**

```toml
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```text
use reqwest::header::{HeaderMap, HeaderValue, AUTHORIZATION};

// 单次请求：Bearer
let resp = client
    .get("https://api.example.com/me")
    .bearer_auth("TOKEN")
    .send()
    .await?;

// 单次请求：手写 Authorization
let resp = client
    .get("https://api.example.com/me")
    .header(AUTHORIZATION, format!("Bearer {token}"))
    .send()
    .await?;

// Client 默认头：所有请求都带
let mut headers = HeaderMap::new();
headers.insert(
    AUTHORIZATION,
    HeaderValue::from_str(&format!("Bearer {token}"))?,
);
let client = reqwest::Client::builder()
    .default_headers(headers)
    .build()?;
```

服务端（axum）读头示意：

```text
use axum::http::HeaderMap;

async fn me(headers: HeaderMap) -> Result<String, axum::http::StatusCode> {
    let Some(val) = headers.get(axum::http::header::AUTHORIZATION) else {
        return Err(axum::http::StatusCode::UNAUTHORIZED);
    };
    let s = val.to_str().map_err(|_| axum::http::StatusCode::BAD_REQUEST)?;
    // 校验 Bearer ... 后返回业务结果
    Ok(s.to_string())
}
```

注意：token 不要打进日志；轮换凭证时重建 Client 或按请求覆盖 Header（见 [Q4](#q4)）。

**Go 对比：**
```go
req.Header.Set("Authorization", "Bearer "+token)
```
- **Go 怎么做**：`Header.Set`；第三方客户端也有 `SetBasicAuth`。
- **Rust 为什么不同**：reqwest 提供 `bearer_auth`/`basic_auth` 糖，底层仍是 Header。
- **Go 程序员易踩的坑**：`Authorization` 拼写错、或 `Bearer` 后少空格。

**记忆点：**
- 优先 `.bearer_auth` / `.basic_auth`。
- 全局默认头挂 Client；单次覆盖用 `.header`。

---

## Q15. CORS / 上传 / WebSocket 去哪看？ {#q15}
**Tags:** `hot` `CORS` `WebSocket` `multipart` `进阶`
**适用版本:** 导航题；细节见专题

**一句话答案：**
浏览器跨域、Cookie/Session、multipart 上传、WebSocket/SSE、限流 Layer、`httptest` 式测 handler——请看 **[52-http-advanced-and-realtime](../52-http-advanced-and-realtime/)**。本篇（40）停在 JSON API 入门，避免和进阶挤在一章。

**解答：**
```text
40 本篇：reqwest / axum 路由 / State / 关停 / TLS 选型
52 进阶：CORS、Cookie、multipart、WS/SSE、tower-http、oneshot 测试
```

```rust
fn main() {
    println!("learn 40 first, then 52 for browser & realtime");
}
```

```text
# 常见搜索词 → 52 题号
# CORS → 52 Q1；multipart → 52 Q3；WebSocket → 52 Q4；httptest → 52 Q10
```

**Go 对比：**
- Go 常把 CORS/WS 和 `net/http` 教程写在一起；本系列拆成入门/进阶两篇。
- **Go 程序员易踩的坑**：在 40 里找不到 CORS 就以为 axum 不支持。

**记忆点：**
- JSON API 入门 → 40。
- 浏览器与实时 → 52。
