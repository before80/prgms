+++
title = "第 18 章 Web 开发"
weight = 180
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter 18 Web 开发

<!-- CONTENT_MARKER -->

> 把写 Web 应用比作开餐厅，那 Rust 的 Web 开发工具链就是一家从零打造的米其林后厨。Tokio 是你的灶台（异步引擎），Axum 是你的主厨（高层框架），hyper 是你的烤箱（底层 HTTP），tower 是你的传菜流水线（中间件系统），而 sqlx/diesel 则是你的食材管理系统（数据库）。每一层都有它存在的理由，每一层都值得你细细品味。准备好了吗？让我们开始这场 Rust Web 开发的烹饪课！

## 18.1 Web 框架概览

想象一下，你想开一家餐厅。首先你得决定：是找一家已经装修好的店面拎包入住（用高级框架），还是自己从砌砖开始造厨房（用底层库）？Rust 的 Web 生态给了你两种选择，而且无论哪种选择，你都能感受到 Rust 那种"要么不做，要做就做到极致"的性格。

### 18.1.1 生态全景

Rust 的 Web 开发生态可以说是一个"低调奢华"的代表。没有 JavaScript 那种眼花缭乱的框架大战，但每一个拿出来都是精品。主流的 Web 框架包括 Axum、Actix-web、Rocket、Poem 和 Warp，它们各有特色，适用于不同的场景。

#### 18.1.1.1 主流框架对比（Axum / Actix-web / Rocket / Poem / Warp）

让我们用一个表格来对比这五大框架的"武功秘籍"：

| 框架 | 开发团队 | 性能 | 学习曲线 | 特色 | 适合场景 |
|------|----------|------|----------|------|----------|
| **Axum** | Tower 团队 | ⭐⭐⭐⭐ | 较平缓 | Tokio 生态，tower 集成 | 入门首选，中大型项目 |
| **Actix-web** | Actix 团队 | ⭐⭐⭐⭐⭐ | 较陡峭 | 最高性能，低层级控制 | 高性能 API，微服务 |
| **Rocket** | Rocket 团队 | ⭐⭐⭐ | 平缓 | 表现力强，类型安全路由 | 快速开发，类型强迫症患者 |
| **Poem** | Poem 团队 | ⭐⭐⭐⭐ | 平缓 | 轻量，符合 HTTP 标准 | 轻量 API，OpenAPI 集成 |
| **Warp** | Sean 团队 | ⭐⭐⭐⭐ | 较陡峭 | 组合式过滤器 | 函数式爱好者，精确控制 |

```mermaid
graph TD
    A[Web 框架选择] --> B[Axum]
    A --> C[Actix-web]
    A --> D[Rocket]
    A --> E[Poem]
    A --> F[Warp]
    B --> G[Tower 生态友好]
    C --> H[极致性能]
    D --> I[类型安全路由]
    E --> J[轻量简洁]
    F --> K[Filter 组合]
```

> 如果你是一个 Rust 新手，想快速上手 Web 开发，我强烈推荐从 Axum 开始。它就像一个装修好的餐厅，你只需要学会怎么点菜（写 Handler），就能快速开张营业。

### 18.1.2 框架对比

每一框架都有它独特的"性格"，让我们来逐一了解这些 Web 开发界的"江湖人物"。

#### 18.1.2.1 Axum（推荐入门，Tokio 生态，tower 集成）

Axum 是由 Tower 团队打造的 Web 框架，天生就站在 Tokio 这个巨人的肩膀上。如果你把 Tokio 比作厨房的灶台，那 Axum 就是那个把所有厨具都安排得明明白白的主厨。

Axum 的设计哲学是"简洁而不简单"——它没有 Rocket 那么多魔法宏，也没有 Warp 那么函数式，但它的 API 非常直观，而且与 tower 中间件系统无缝集成。

```rust
use axum::{
    routing::get,
    Router,
};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    println!("🌐 Axum 框架演示！");

    // 定义路由
    let app = Router::new()
        .route("/", get(handler))
        .route("/api/hello", get(hello_api));

    // 启动服务器
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("🚀 服务器启动在 http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn handler() -> &'static str {
    "你好，Axum 世界！" // 打印：你好，Axum 世界！
}

async fn hello_api() -> &'static str {
    "Hello from Axum API!" // 打印：Hello from Axum API!
}
```

Axum 的路由系统非常灵活，支持嵌套路由、路由分组、多种 HTTP 方法。而且得益于 tower 系统，你可以轻松添加日志、CORS、压缩等中间件。

#### 18.1.2.2 Actix-web（极致性能，低层级控制）

Actix-web 是 Rust Web 框架中的"性能怪兽"。它的性能可以媲美 C/C++ 编写的 HTTP 服务器，在 TechEmpower 的基准测试中长期占据榜首位置。

Actix-web 的设计理念是"让高性能成为默认设置"——它的异步处理、连接管理、HTTP 解析都是经过精心优化的。

```rust
use actix_web::{web, App, HttpServer, HttpResponse};

async fn index() -> HttpResponse {
    HttpResponse::Ok().body("🔥 Actix-web 性能怪兽！")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("🔥 Actix-web 性能怪兽启动中...");

    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            .route("/api/bench", web::get().to(index))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
// 输出: 🔥 Actix-web 性能怪兽启动中...
```

Actix-web 的缺点？它的学习曲线相对较陡，错误消息有时候也比较神秘。但如果你追求极致性能，而且愿意花时间钻研，它绝对值得你拥有。

#### 18.1.2.3 Rocket（表现力强，类型安全路由）

Rocket 是一个"让你写 Web 应用像写普通 Rust 代码一样自然"的框架。它的路由系统是 Rust 宏系统的杰作，能在编译期就检查出大部分错误。

Rocket 的设计理念是"约定大于配置"——你不需要繁琐的配置，只需要按照它的规则写代码，它就能自动帮你搞定一切。这种设计让 Rocket 的代码读起来非常优雅。

```rust
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};

// 定义一个请求体结构
#[derive(Deserialize)]
struct User {
    name: String,
    email: String,
}

// 定义响应结构
#[derive(Serialize)]
struct Response {
    message: String,
    id: u64,
}

// Rocket 的路由会自动处理 JSON 解析
#[post("/user", format = "json", data = "<user>")]
fn create_user(user: Json<User>) -> Json<Response> {
    Json(Response {
        message: format!("欢迎 {} 加入我们！", user.name),
        id: 42, // 模拟数据库返回的 ID
    })
}

#[launch]
fn rocket() -> _ {
    println!("🚀 Rocket 发射！类型安全，编译期检查！");

    rocket::build().mount("/api", rocket::routes![create_user])
}
// 输出: 🚀 Rocket 发射！类型安全，编译期检查！
```

Rocket 的类型安全路由意味着，如果你把路由写错了（比如把 `/user` 拼成 `/users`），编译器会在你运行程序之前就告诉你。这种"早发现，早治疗"的设计哲学，能让你的 Web 开发体验大大提升。

#### 18.1.2.4 Poem（轻量，符合 HTTP 标准）

Poem 是一个"轻量级选手"，它的设计目标就是做一个符合 HTTP 标准的、简洁的 Web 框架。Poem 的代码量相对较少，API 也比较直观，适合那些想要轻装上阵的开发者。

Poem 还有一个亮点，就是它对 OpenAPI（也就是以前的 Swagger）的支持非常好。如果你需要生成 API 文档，Poem 能让你省不少力气。

```rust
use poem::{
    handler,
    listener::TcpListener,
    middleware::Tracing,
    web::{
        path,
        Json, Query,
    },
    Endpoint, EndpointExt, Route,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// 查询参数结构
#[derive(Deserialize, Debug)]
struct PageParams {
    page: Option<usize>,
    size: Option<usize>,
}

// 响应结构
#[derive(Serialize)]
struct ApiResponse<T> {
    data: T,
    total: usize,
}

#[handler]
async fn api_list(Query(params): Query<PageParams>) -> Json<ApiResponse<Vec<&'static str>>> {
    let page = params.page.unwrap_or(1);
    let size = params.size.unwrap_or(10);

    Json(ApiResponse {
        data: vec!["item1", "item2", "item3"],
        total: 3,
    })
}

#[handler]
async fn get_item(path::Path(id): path::Path<i32>) -> Json<HashMap<&'static str, String>> {
    Json(HashMap::from([
        ("id", id.to_string()),
        ("name", "Item".to_string()),
    ]))
}

#[tokio::main]
async fn main() {
    println!("📜 Poem 轻量级 Web 框架！");

    let app = Route::new()
        .route("/api/list", get(api_list))
        .route("/api/item/:id", get(get_item))
        .with(Tracing);

    Poem::new(TcpListener::bind("127.0.0.1:3000")).run(app).await;
}
// 输出: 📜 Poem 轻量级 Web 框架！
```

#### 18.1.2.5 Warp（组合式过滤器，函数式风格）

Warp 是"过滤器组合"理念的践行者。它基于 tower 的 Service trait 构建，但提供了更高级的组合器，让你可以用函数式的方式构建复杂的路由逻辑。

Warp 的过滤器就像是管道——数据从一端流入，经过各种过滤器的处理，从另一端流出。这种设计非常适合处理请求验证、参数提取等场景。

```rust
use warp::{Filter, Rejection, Reply};
use std::convert::Infallible;

// 组合多个过滤器
#[tokio::main]
async fn main() {
    println!("🌀 Warp 组合式过滤器演示！");

    // 健康检查过滤器
    let health = warp::path!("health")
        .and(warp::get())
        .map(|| warp::reply::json(&serde_json::json!({
            "status": "ok"
        })));

    // 带参数的过滤器
    let hello = warp::path!("hello" / String)
        .and(warp::get())
        .map(|name| {
            warp::reply::json(&serde_json::json!({
                "message": format!("你好, {}!", name)
            }))
        });

    // POST 请求过滤器
    let echo = warp::path!("echo")
        .and(warp::post())
        .and(warp::body::json())
        .map(|body: serde_json::Value| {
            warp::reply::json(&body)
        });

    // 组合所有路由
    let routes = health.or(hello).or(echo);

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3000))
        .await;
}
// 输出: 🌀 Warp 组合式过滤器演示！
```

Warp 的学习曲线较陡，但一旦你掌握了过滤器的组合技巧，就能写出非常优雅的路由代码。

---

## 18.2 Axum 框架

### 18.2.1 项目结构

### 18.2.1.1 Cargo.toml 依赖（axum / tower / tokio）

# Axum 项目结构与依赖配置

在开始 Axum 的冒险之前，我们需要先搭建好我们的"魔法工坊"。这个工坊就是 Rust 项目，而 Cargo.toml 就是我们的材料清单。

## 创建项目

首先，让我们创建一个新的 Rust 项目：

```bash
cargo new my-axum-app
cd my-axum-app
```

## Cargo.toml 依赖配置

打开你的 Cargo.toml 文件，这是你最亲密的战友。所有的依赖都需要在这里声明，就像你要做一道菜，需要先列好食材清单一样。

```toml
[package]
name = "my-axum-app"
version = "0.1.0"
edition = "2021"

[dependencies]
# Axum Web 框架核心
# 这是我们的主角，所有 Web 开发的基础
axum = "0.7"

# Tokio 异步运行时
# 想象 Tokio 是那个帮你处理所有繁琐异步工作的超级管家
tokio = { version = "1", features = ["full"] }

# Tower 网络库
# Tower 提供了一整套中间件和服务抽象，让你的代码模块化、可复用
tower = "0.4"

# Tower HTTP 扩展
# 包含 CORS、压缩、静态文件服务等常用中间件
tower-http = { version = "0.5", features = ["cors", "compression-full", "fs"] }

# serde 用于序列化/反序列化
# 有了 serde，JSON 和 Rust 结构体之间转换就像变魔术一样简单
serde = { version = "1", features = ["derive"] }

# serde_json 用于 JSON 解析
serde_json = "1"

# tracing 用于日志记录
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

# 一些实用工具
anyhow = "1"
```

## 推荐的目录结构

一个好的项目结构就像一个整洁的厨房——每样东西都有它的位置。

```
my-axum-app/
├── src/
│   ├── main.rs          # 入口文件
│   ├── router.rs       # 路由定义
│   ├── handlers/       # 处理器（Controller）
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── article.rs
│   ├── models/         # 数据模型
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── article.rs
│   ├── db.rs           # 数据库连接
│   └── error.rs        # 错误处理
├── Cargo.toml
└── .env                # 环境变量
```

## main.rs 基础模板

下面是一个最简单的 Axum 程序模板：

```rust
use axum::{
    routing::get,
    Router,
};

#[tokio::main]
async fn main() {
    println!("🌐 欢迎来到 Axum 世界！");

    // 定义路由
    let app = Router::new()
        .route("/", get(handler));

    // 启动服务器
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();
    println!("🚀 服务器正在监听 http://127.0.0.1:3000");

    axum::serve(listener, app).await.unwrap();
}

async fn handler() -> &'static str {
    "你好，Axum 世界！" // 打印：你好，Axum 世界！
}
```

## Axum 核心依赖解析

```
axum
 ├── axum-core    # 核心类型，如 Request、Response
 ├── tower        # 中间件基础设施
 ├── tokio        # 异步运行时
 └── http         # HTTP 类型定义

tower-http
 ├── cors         # 跨域资源共享
 ├── compression  # 响应压缩
 └── fs           # 静态文件服务
```

### 18.2.2 路由与处理器

#### 18.2.2.1 基本路由定义

Axum 的路由系统非常直观——你只需要定义路径和对应的处理函数即可。

```rust
use axum::{
    routing::{get, post, put, delete},
    Router,
};
use serde::{Deserialize, Serialize};
use axum::extract::{Path, Query, Json};

// === 路径参数 ===

// GET /users/123
async fn get_user(Path(user_id): Path<i32>) -> String {
    format!("获取用户 ID: {}", user_id)
    // 打印: 获取用户 ID: 123
}

// === 查询参数 ===

#[derive(Debug, Deserialize)]
pub struct Pagination {
    pub page: Option<usize>,
    pub size: Option<usize>,
}

async fn list_users(Query(params): Query<Pagination>) -> String {
    let page = params.page.unwrap_or(1);
    let size = params.size.unwrap_or(10);
    format!("第 {} 页，每页 {} 条", page, size)
    // 打印: 第 1 页，每页 10 条
}

// === 请求体 ===

#[derive(Debug, Deserialize)]
pub struct CreateUser {
    pub name: String,
    pub email: String,
}

#[derive(Debug, Serialize)]
pub struct UserResponse {
    pub id: u64,
    pub name: String,
    pub email: String,
}

async fn create_user(Json(payload): Json<CreateUser>) -> Json<UserResponse> {
    // 在这里可以保存到数据库
    Json(UserResponse {
        id: 42,
        name: payload.name,
        email: payload.email,
    })
}

// === 路由组合 ===

#[tokio::main]
async fn main() {
    println!("🛣️ Axum 路由演示！");

    let app = Router::new()
        .route("/users", get(list_users))
        .route("/users/:id", get(get_user))
        .route("/users", post(create_user))
        .route("/articles/:id", delete(|_| async { "删除成功！" }));

    println!("🛣️ 路由已配置: GET /users, GET /users/:id, POST /users, DELETE /articles/:id");

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

#### 18.2.2.2 嵌套路由与路由分组

当你的 API 变得复杂时，你需要对路由进行分组。Axum 允许你创建嵌套路由，就像整理文件夹一样。

```rust
use axum::{
    routing::{get, post},
    Router,
    extract::Path,
};

// 用户相关的处理器
async fn list_users() -> &'static str { "所有用户" }
async fn create_user() -> &'static str { "创建用户" }

// 文章相关的处理器
async fn list_articles() -> &'static str { "所有文章" }
async fn get_article(Path(id): Path<i32>) -> String {
    format!("文章 #{}", id)
}
async fn create_article() -> &'static str { "创建文章" }

#[tokio::main]
async fn main() {
    println!("📁 嵌套路由演示！");

    // 用户模块
    let user_routes = Router::new()
        .route("/", get(list_users))
        .route("/", post(create_user));

    // 文章模块
    let article_routes = Router::new()
        .route("/", get(list_articles))
        .route("/", post(create_article))
        .route("/:id", get(get_article));

    // 顶层路由
    let app = Router::new()
        .nest("/api/users", user_routes)  // /api/users, /api/users (POST)
        .nest("/api/articles", article_routes); // /api/articles, /api/articles/:id

    println!("📁 路由已分组:");
    println!("  - /api/users     (GET: 列表, POST: 创建)");
    println!("  - /api/articles  (GET: 列表, POST: 创建)");
    println!("  - /api/articles/:id (GET: 详情)");

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### 18.2.3 中间件

#### 18.2.3.1 tower-http 中间件

tower-http 是 tower 生态在 HTTP 领域的扩展包，提供了很多开箱即用的中间件。

```rust
use axum::{
    routing::get,
    Router,
};
use tower_http::cors::{CorsLayer, Any};
use tower_http::compression::CompressionLayer;
use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() {
    println!("🔧 中间件演示！");

    let app = Router::new()
        .route("/", get(|| async { "Hello World!" }))
        .layer(TraceLayer::new_for_http())         // 请求追踪
        .layer(CompressionLayer::new())             // 自动压缩响应
        .layer(
            CorsLayer::new()
                .allow_origin(Any)                   // 允许所有来源
                .allow_methods(Any)                 // 允许所有方法
                .allow_headers(Any),                // 允许所有请求头
        );

    println!("🔧 已添加中间件: Trace, Compression, CORS");

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

#### 18.2.3.2 自定义中间件

你可以使用 `axum::middleware::from_fn` 来创建自定义中间件。

```rust
use axum::{
    routing::get,
    Router,
    middleware::{self, Next},
    extract::Request,
};
use tower::ServiceExt;

async fn check_auth(request: Request, next: Next) -> axum::response::Response {
    // 从请求头中获取 Authorization
    let auth_header = request
        .headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok());

    match auth_header {
        Some(token) if token.starts_with("Bearer ") => {
            // 验证 Token（这里简化处理）
            println!("🔓 已认证请求，Token: {}...", &token[7..15]);
            next.run(request).await
        }
        _ => {
            println!("🔒 未认证请求，被中间件拦截！");
            axum::response::Response::builder()
                .status(401)
                .body("Unauthorized".into())
                .unwrap()
        }
    }
}

#[tokio::main]
async fn main() {
    println!("🔐 自定义中间件演示！");

    let protected_app = Router::new()
        .route("/secret", get(|| async { "这是秘密！" }))
        .route("/public", get(|| async { "这是公开的！" }))
        .layer(middleware::from_fn(check_auth));

    println!("🔐 /secret 需要认证，/public 无需认证");

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await.unwrap();
    axum::serve(listener, protected_app).await.unwrap();
}
```

---

## 18.3 Web 后端核心库

### 18.3.1 hyper（底层 HTTP）

hyper 是 Rust 生态中最底层、最核心的 HTTP 库。它直接操作 HTTP 协议，是其他高级框架的底层基础。

hyper 的设计理念是"专注、极致"——它只做 HTTP 相关的事情，而且要做到最好。其他的事情（如路由、中间件、模板）都交给上层的框架去做。

```rust
use hyper::{
    body::HttpBody,
    server::conn::http1,
    Request, Response, StatusCode,
    body::Bytes,
};
use hyper::service::service_fn;
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    println!("⚡ hyper 底层 HTTP 演示！");

    let listener = TcpListener::bind("127.0.0.1:3000").await?;
    println!("⚡ hyper 服务器启动在 http://127.0.0.1:3000");

    loop {
        let (stream, _) = listener.accept().await?;

        let service = service_fn(|req: Request<hyper::body::Incoming>| async move {
            println!("📨 收到请求: {} {}", req.method(), req.uri());

            // 根据路径返回不同响应
            let response = match req.uri().path() {
                "/" => Response::builder()
                    .status(StatusCode::OK)
                    .body("Hello, hyper!".into())?,
                "/health" => Response::builder()
                    .status(StatusCode::OK)
                    .body(r#"{"status":"ok"}"#.into())?,
                _ => Response::builder()
                    .status(StatusCode::NOT_FOUND)
                    .body("Not Found".into())?,
            };

            Ok::<_, hyper::Error>(response)
        });

        if let Err(e) = http1::Builder::new()
            .serve_connection(stream, service)
            .await
        {
            eprintln!("⚠️ 连接错误: {}", e);
        }
    }
}
// 输出:
// ⚡ hyper 底层 HTTP 演示！
// ⚡ hyper 服务器启动在 http://127.0.0.1:3000
// 📨 收到请求: GET /
// 📨 收到请求: GET /health
```

hyper 支持 HTTP/1.1 和 HTTP/2，而且它的性能经过了大量优化。如果你需要构建一个高性能的 HTTP 客户端或服务器，而且不想要上层框架的抽象开销，hyper 是你的首选。

#### 18.3.1.1 hyper 作为 HTTP 客户端

hyper 不仅能做服务器，还能做客户端。以下是一个简单的 HTTP GET 请求示例：

```rust
use hyper::{body::HttpBody, Client};
use hyper::body::Bytes;
use tower::ServiceExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    println!("📡 hyper HTTP 客户端演示！");

    // 创建一个客户端连接
    let connector = hyper::client::HttpConnector::new();
    let client: Client<_, hyper::body::Incoming> =
        hyper::client::Client::builder()
            .pool_idle_timeout(std::time::Duration::from_secs(30))
            .build(connector);

    // 发送 GET 请求
    let uri: hyper::Uri = "https://httpbin.org/get".parse()?;
    let resp = client.get(uri).await?;

    println!("📥 状态码: {}", resp.status());

    // 读取响应体
    let body = hyper::body::to_bytes(resp.into_body()).await?;
    let body_str = String::from_utf8(body.to_vec())?;
    println!("📦 响应体长度: {} 字节", body_str.len());
    println!("📦 响应体前100字符: {}", &body_str[..100.min(body_str.len())]);

    Ok(())
}
// 输出:
// 📡 hyper HTTP 客户端演示！
// 📥 状态码: 200 OK
// 📦 响应体长度: 512 字节
```

#### 18.3.1.2 hyper 与其他库的对比

| 特性 | hyper | reqwest | Other |
|------|-------|---------|-------|
| 协议 | HTTP/1.1, HTTP/2 | HTTP/1.1, HTTP/2, HTTPS | - |
| 异步 | Tokio | Tokio | - |
| 使用场景 | 低级库/框架开发 | 应用层 HTTP 客户端 | - |
| 学习曲线 | 陡峭 | 平缓 | - |

> hyper 是"工具箱里的精密仪器"——它功能强大，但需要你对 HTTP 协议有较深的理解。如果你想快速发 HTTP 请求，用 reqwest；如果你想构建自己的 Web 框架，用 hyper。

### 18.3.2 tower（中间件系统）

tower 是 Rust 异步服务抽象的基石。它的核心是 `Service` trait——一个抽象了"接收请求，返回响应"这种模式的标准接口。

tower 的设计哲学是"组合优于继承"——你可以通过层层包装（Layer）来添加功能，而不是通过继承树。这就像乐高积木，每块积木都有自己的功能，你可以自由组合。

#### 18.3.2.1 Service trait

```rust
use std::future::{Future, FutureExt};
use std::task::{Context, Poll};
use std::pin::Pin;
use tower::{Service, Layer};
use std::time::Instant;

// === 基础 Service ===
// 注意：EchoService 需要实现 Clone，因为 LogService 和 TimeoutService
// 内部需要 clone 持有的 Service 实例

#[derive(Clone)]
struct EchoService;

impl Service<String> for EchoService {
    type Response = String;
    type Error = std::convert::Infallible;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send>>;

    fn poll_ready(&mut self, _: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        Poll::Ready(Ok(()))
    }

    fn call(&mut self, request: String) -> Self::Future {
        async move { Ok(format!("ECHO: {}", request)) }.boxed()
    }
}

// === 日志 Service Wrapper ===

struct LogService<S> {
    inner: S,
}

impl<S, T> Service<T> for LogService<S>
where
    S: Service<T> + Clone + Send + 'static,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, request: T) -> Self::Future {
        println!("📝 [LogService] 收到请求: {:?}", &request);

        let future = self.inner.call(request);

        Box::pin(async move {
            let result = future.await;
            println!("📝 [LogService] 响应: {:?}", &result);
            result
        })
    }
}

// === 超时 Service Wrapper ===

struct TimeoutService<S> {
    inner: S,
    timeout: std::time::Duration,
}

impl<S, T> Service<T> for TimeoutService<S>
where
    S: Service<T> + Clone + Send + 'static,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = tower::timeout::TimeoutError<S::Error>;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, request: T) -> Self::Future {
        let timeout = self.timeout;
        let mut inner = self.inner.clone();

        Box::pin(async move {
            tokio::time::timeout(timeout, inner.call(request)).await
        })
    }
}

// === 使用示例 ===

#[tokio::main]
async fn main() {
    println!("🔧 tower Service trait 演示！");

    // 创建基础 Service
    let echo = EchoService;

    // 包装成日志 Service
    let logged_echo = LogService { inner: echo.clone() };

    // 调用 Service
    let response = logged_echo.call("Hello, tower!".to_string()).await;
    println!("📥 最终响应: {:?}", response);

    println!("\n👋 Service 演示结束！");
}

// Service trait 详解
fn explain_service_trait() {
    /*
    pub trait Service<T> {
        // 请求类型
        type Request;

        // 响应类型
        type Response;

        // 错误类型
        type Error;

        // 异步响应 Future
        type Future: Future<Output = Result<Self::Response, Self::Error>>;

        // 检查 Service 是否准备就绪处理请求
        fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>>;

        // 处理请求
        fn call(&mut self, req: Self::Request) -> Self::Future;
    }

    // 设计哲学:
    // 1. Service 是 "懒" 的 - 必须在 poll_ready 返回 Ready 后才能调用
    // 2. 实现了 Clone 的 Service 可以在多个请求间共享
    */
}
```

---

## 18.4 数据库

如果说 Web 应用是一个大脑，那数据库就是记忆中枢。没有数据库，你的应用就像一个金鱼——只能记住 7 秒钟前的事。Rust 的数据库生态丰富得像是开在金融街上的火锅店：sqlx、diesel、sea-orm 三足鼎立，各有各的绝活。

### 18.4.1 sqlx（编译期查询验证）

sqlx 是 Rust 数据库界的"学霸"——它在编译期就能验证你的 SQL 语句是否正确。你没听错，编译期！想象一下，你写了一行 SQL，写完的瞬间编译器就告诉你"嘿，这列名写错了"，那种快感就像考试的时候提前知道答案。

sqlx 的核心秘密在于 `sqlx::query!` 宏——它会在编译时连接数据库并验证 SQL，而不是等到运行时才发现问题。

```rust
use sqlx::{postgres::PgPoolOptions, FromRow, query_as};
use serde::{Deserialize, Serialize};
use std::time::Duration;
use chrono::NaiveDateTime;

// 用户结构 - 对应数据库的 users 表
#[derive(FromRow, Serialize, Debug, Clone)]
struct User {
    id: i32,
    name: String,
    email: String,
    created_at: chrono::NaiveDateTime, // 需要 chrono 支持日期时间
}

// 博客文章结构
#[derive(FromRow, Serialize, Debug)]
struct Article {
    id: i32,
    title: String,
    content: String,
    author_id: i32,
    published_at: Option<chrono::NaiveDateTime>,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    println!("🔍 sqlx 编译期查询验证演示！");

    // 建立数据库连接池
    // 使用 PostgreSQL，连接字符串（生产环境请用环境变量！）
    let database_url = "postgres://postgres:password@localhost/myapp";

    let pool = PgPoolOptions::new()
        .max_connections(5)                     // 最多 5 个连接
        .acquire_timeout(Duration::from_secs(3)) // 获取连接超时 3 秒
        .connect(database_url).await?;

    println!("✅ 数据库连接成功！");

    // === 方式一：query! 宏（编译期验证，最安全）===
    // 注意：query! 需要在编译时连接数据库
    // 如果你不想在编译时连接，可以使用 query_as! 或 fetch_optional!

    // 编译期验证的查询 - 如果 SQL 错误或列名不对，编译直接失败！
    // let users = sqlx::query!("SELECT id, name, email FROM users")
    //     .fetch_all(&pool)
    //     .await?;

    // === 方式二：query_as! 宏（带结果类型）===
    // 推荐在无法编译时连接数据库的场景使用
    let users: Vec<User> = sqlx::query_as!(
        User,
        // 编译期验证：确保列名和类型与 User 结构体匹配
        "SELECT id, name, email, created_at FROM users WHERE id > $1",
        0
    )
    .fetch_all(&pool)
    .await?;

    println!("📋 查询到 {} 个用户:", users.len());
    for user in &users {
        println!("  👤 {} <{}>", user.name, user.email);
    }

    // === 方式三：fetch_optional（查询单条或零条）===
    // 适合查用户详情、设置等场景
    let maybe_user: Option<User> = sqlx::query_as!(
        User,
        "SELECT id, name, email, created_at FROM users WHERE email = $1",
        "alice@example.com"
    )
    .fetch_optional(&pool)
    .await?;

    match maybe_user {
        Some(user) => println!("🔍 找到用户: {}", user.name),
        None => println!("❌ 用户不存在！"),
    }

    // === 方式四：事务操作 ===
    let mut tx = pool.begin().await?;
    let row = sqlx::query!("INSERT INTO articles (title, content, author_id) VALUES ($1, $2, $3) RETURNING id", "Rust真好学", "sqlx 真香，编译期验证 SQL", 1).fetch_one(&mut *tx).await?;
    let article_id: i32 = row.id;
    tx.commit().await?;
    println!("📝 新文章已创建，ID: {}", article_id);

    println!("\n👋 sqlx 演示结束！");
    Ok(())
}
// 输出示例:
// 🔍 sqlx 编译期查询验证演示！
// ✅ 数据库连接成功！
// 📋 查询到 2 个用户:
//   👤 Alice <alice@example.com>
//   👤 Bob <bob@example.com>
// 🔍 找到用户: Alice
// 📝 新文章已创建，ID: 42
// 👋 sqlx 演示结束！
```

> sqlx 的精髓在于 `query!` 和 `query_as!` 宏。写 SQL 的时候别忘了加上返回类型，不然 Rust 编译器会给你一堆红色的"你以为你能骗过我？"错误信息。

#### 18.4.1.1 sqlx 的离线模式

如果你不想在每次编译时都连接数据库（比如说，你的笔记本没联网，或者数据库在遥远的云端），sqlx 提供了离线模式。它会把你之前验证过的查询缓存起来，即使离线也能编译。

```rust
// Cargo.toml 需要添加：
// sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "macros", "chrono", "migrate"] }
// 在代码顶部添加：
// #[sqlx::query_bundle] // 需要 sqlx-build 或预先准备的离线数据

// 使用离线模式的关键：在 .env 或环境变量中设置 DATABASE_URL
// 然后运行：DATABASE_URL=postgres://... cargo sqlx prepare
// 这会生成 .sqlx 目录，存储查询元数据

fn main() {
    println!("🔧 sqlx 离线模式需要先运行 prepare 命令生成缓存！");
    println!("📝 步骤: 1) 设置 DATABASE_URL  2) cargo sqlx prepare");
}
```

### 18.4.2 diesel ORM（同步为主）

如果说 sqlx 是"原生态"的数据操作库，那 diesel 就是那个帮你把所有东西都打包好的"外卖盒"。diesel 是 Rust 生态中最成熟的 ORM（对象关系映射）框架，它的口号是"让你的数据库操作像操作普通 Rust 对象一样简单"。

diesel 的特点是**同步优先**——它假设你大多数时候不需要异步，适合那些偏传统的 Web 应用。如果你用的是 Actix-web 或者 Rocket，diesel 会是你的好伙伴。

```rust
// 注意：diesel 需要先安装并设置数据库：
// 1. 安装 diesel_cli: cargo install diesel_cli --no-default-features --features postgres
// 2. 初始化项目: diesel database setup
// 3. diesel 会生成 schema.rs 和 types.rs

// 由于 diesel 的完整示例需要预先设置，这里展示核心用法
// === diesel 核心概念 ===

// 1. 定义表（在 src/schema.rs 中由 diesel  CLI 生成）
// diesel::table! {
//     users (id) {
//         id -> Int4,
//         name -> Varchar,
//         email -> Varchar,
//         password_hash -> Varchar,
//         created_at -> Timestamp,
//     }
// }

// 2. 定义模型（在 src/models.rs 中）
// #[derive(Queryable, Selectable, Serialize)]
// #[diesel(table_name = users)]
// struct User {
//     id: i32,
//     name: String,
//     email: String,
//     password_hash: String,
//     created_at: chrono::NaiveDateTime,
// }

// 3. 定义插入结构
// #[derive(Insertable)]
// #[diesel(table_name = users)]
// struct NewUser<'a> {
//     name: &'a str,
//     email: &'a str,
//     password_hash: &'a str,
// }

// === diesel CRUD 操作示例（伪代码，实际运行需要完整项目结构）===

fn diesel_crud_example() {
    println!("🔧 diesel ORM CRUD 演示！");

    // 建立连接（同步的！）
    // let conn = &mut establish_connection();

    // === 增 (Create) ===
    // let new_user = NewUser {
    //     name: "Alice",
    //     email: "alice@example.com",
    //     password_hash: "hashed_password_here",
    // };
    // diesel::insert_into(users::table)
    //     .values(&new_user)
    //     .execute(conn)
    //     .expect("插入用户失败！");

    // === 查 (Read) ===
    // let all_users = users::table
    //     .load::<User>(conn)
    //     .expect("查询用户失败！");

    // let alice = users::table
    //     .filter(users::email.eq("alice@example.com"))
    //     .first::<User>(conn)
    //     .optional()
    //     .expect("查询失败！");

    // === 改 (Update) ===
    // diesel::update(users::table.find(1))
    //     .set(users::name.eq("Alice Updated"))
    //     .execute(conn)
    //     .expect("更新用户失败！");

    // === 删 (Delete) ===
    // diesel::delete(users::table.find(1))
    //     .execute(conn)
    //     .expect("删除用户失败！");

    println!("📝 diesel 使用步骤：");
    println!("  1. 添加 diesel 和数据库驱动到 Cargo.toml");
    println!("  2. 安装 diesel_cli 并初始化数据库");
    println!("  3. diesel 自动生成 schema.rs");
    println!("  4. 定义模型并编写 CRUD");
    println!("\n👋 diesel 是同步 ORM 的最佳选择！");
}

fn main() {
    diesel_crud_example();
}
// 输出:
// 🔧 diesel ORM CRUD 演示！
// 📝 diesel 使用步骤：
//   1. 添加 diesel 和数据库驱动到 Cargo.toml
//   2. 安装 diesel_cli 并初始化数据库
//   3. diesel 自动生成 schema.rs
//   4. 定义模型并编写 CRUD
// 👋 diesel 是同步 ORM 的最佳选择！
```

> diesel 最大的好处是它的**类型安全**——从表结构到查询，全方位给你检查。如果你写错了列名或者类型不匹配，编译器会毫不客气地指出来，比你妈催你穿秋裤还及时。

### 18.4.3 数据库连接池

想象一下，如果每次查询都要重新建立数据库连接，那就像是每次吃饭都要重新去菜市场买菜——效率低得令人发指。数据库连接池就是那个"提前买好菜、洗好菜"的厨房阿姨，让你随用随取，不用等待。

Rust 的数据库连接池主要有三个玩家：

- **sqlx 内置的连接池**（PgPool、MysqlPool、SqlitePool）
- **deadpool**（支持多种后端，包括 PostgreSQL、Redis、MongoDB）
- **bb8**（经典的连接池实现，稳定可靠）

```rust
use sqlx::{postgres::PgPoolOptions, PgPool};
use std::time::Duration;

async fn pool_demo() {
    println!("🏊 数据库连接池演示！");

    // === sqlx 内置连接池（最常用）===
    let pool = PgPoolOptions::new()
        .max_connections(10)                  // 最大连接数
        .min_connections(2)                    // 最小连接数（预热）
        .acquire_timeout(Duration::from_secs(30)) // 获取超时
        .idle_timeout(Duration::from_secs(600))   // 空闲回收时间
        .max_lifetime(Duration::from_secs(1800)) // 单连接最大生命周期
        .connect("postgres://postgres:password@localhost/myapp")
        .await
        .expect("连接池创建失败！");

    println!("✅ 连接池创建成功！最大 {} 个连接", pool.max_connections());

    // 使用连接池并发查询
    // let results = sqlx::query!("SELECT * FROM users")
    //     .fetch_all(&pool)
    //     .await;

    // === 手动借用连接（如果需要事务）===
    {
        let mut conn = pool.acquire().await.expect("获取连接失败");
        // let tx = conn.begin().await?;
        // 在这里执行需要事务的操作
        // tx.commit().await?;
        println!("🔄 手动获取连接成功！");
    } // 连接在这里自动归还给池子

    // === deadpool 连接池（更适合需要池化多种资源）===
    println!("\n📦 deadpool 支持的资源类型：");
    println!("  - deadpool-postgres (PostgreSQL)");
    println!("  - deadpool-redis (Redis)");
    println!("  - deadpool-managed (通用池)");
    println!("  - deadpool-mongodb (MongoDB)");

    println!("\n🏊 连接池是 Web 应用的性能倍增器！");
}

// === 连接池配置最佳实践 ===

fn pool_best_practices() {
    println!("⚙️ 连接池配置建议：");
    println!("  max_connections: CPU 核心数 * 2 ~ 4");
    println!("    - 太多连接 = 数据库压力过大");
    println!("    - 太少连接 = 并发能力不足");
    println!("  acquire_timeout: 3~10 秒，避免无限等待");
    println!("  idle_timeout: 5~10 分钟，防止连接腐烂");
    println!("  max_lifetime: 30~60 分钟，定期刷新连接");
}

#[tokio::main]
async fn main() {
    pool_demo().await;
    pool_best_practices();
}
// 输出:
// 🏊 数据库连接池演示！
// ✅ 连接池创建成功！最大 10 个连接
// 🔄 手动获取连接成功！
// 📦 deadpool 支持的资源类型：
//   - deadpool-postgres (PostgreSQL)
//   - deadpool-redis (Redis)
//   - deadpool-mongodb (MongoDB)
// 🏊 连接池是 Web 应用的性能倍增器！
// ⚙️ 连接池配置建议：
//   max_connections: CPU 核心数 * 2 ~ 4
//   ...
```

```mermaid
graph LR
    A[Web 请求] --> B[连接池]
    B --> C{有空闲连接?}
    C -->|是| D[复用连接]
    C -->|否| E{未达上限?}
    E -->|是| F[创建新连接]
    E -->|否| G[等待...]
    D --> H[执行 SQL]
    F --> H
    G --> D
    H --> I[归还连接]
    I --> B
```

### 18.4.4 sea-orm（异步 ORM）

如果说 diesel 是"老派绅士"，那 sea-orm 就是"新锐潮人"——它专为异步时代而生，与 Actix-web、Axum 这些异步框架是天作之合。sea-orm 的设计受到了 Django ORM 和 SQLAlchemy 的启发，但又加入了 Rust 的类型安全特色。

sea-orm 最吸引人的地方是它的 **Active Record 模式**——你的模型自带 CRUD 方法，写起来非常自然。

```rust
use sea_orm::{Database, DbConn, EntityTrait, Set, ActiveModelTrait, QueryTrait, PaginatorTrait};
use serde::{Deserialize, Serialize};

// === 定义实体 ===

// 假设我们有一个 Article 实体
// 这是 sea-orm 的风格——模型和表结构分离

mod article {
    use sea_orm::entity::prelude::*;

    #[derive(Clone, Debug, DeriveEntityModel, Serialize)]
    #[sea_orm(table_name = "articles")]
    pub struct Model {
        #[sea_orm(primary_key)]
        pub id: i32,
        pub title: String,
        pub content: String,
        pub author_id: i32,
        pub view_count: i32,
        pub created_at: chrono::NaiveDateTime,
        pub updated_at: chrono::NaiveDateTime,
    }

    #[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
    pub enum Relation {}

    impl ActiveModelBehavior for ActiveModel {}

    // 手动定义 ActiveModel（sea-orm 0.12 需要手动写）
    // 注意：Set<T> 是设置值时使用的包装器，不是字段类型
    pub struct ActiveModel {
        pub id: Option<i32>,
        pub title: Option<String>,
        pub content: Option<String>,
        pub author_id: Option<i32>,
        pub view_count: Option<i32>,
        pub created_at: Option<chrono::NaiveDateTime>,
        pub updated_at: Option<chrono::NaiveDateTime>,
    }

    impl ActiveModelTrait for ActiveModel {
        fn get_id(&self) -> Option<i32> { self.id }
        fn set_id(&mut self, id: i32) { self.id = Some(id); }
    }
}

async fn sea_orm_demo() {
    println!("🐚 sea-orm 异步 ORM 演示！");

    // 建立数据库连接
    let db: DbConn = Database::connect("postgres://postgres:password@localhost/myapp")
        .await
        .expect("数据库连接失败！");

    println!("✅ sea-orm 连接成功！");

    // === 查询操作 ===
    // use article::Entity as Article;

    // let article = Article::find_by_id(1).one(&db).await.unwrap();
    // println!("📄 文章标题: {}", article.title);

    // let all_articles = Article::find().all(&db).await.unwrap();
    // for a in all_articles { println!("  📝 {}", a.title); }

    // === 条件查询 ===
    // let popular_articles = Article::find()
    //     .filter(article::Column::ViewCount.gt(100))
    //     .order_by_desc(article::Column::ViewCount)
    //     .limit(10)
    //     .all(&db)
    //     .await
    //     .unwrap();

    // === 分页查询 ===
    // let paginator = Article::find().paginate(&db, 20); // 每页 20 条
    // let total_pages = paginator.num_pages().await.unwrap();
    // let first_page = paginator.fetch_page(0).await.unwrap();

    // === 插入操作 ===
    // let new_article = article::ActiveModel {
    //     title: Set("Rust Web 开发指南".to_string()),
    //     content: Set("这是一篇关于 Rust Web 开发的好文章...".to_string()),
    //     author_id: Set(1),
    //     view_count: Set(0),
    //     created_at: Set(chrono::Utc::now().naive_utc()),
    //     updated_at: Set(chrono::Utc::now().naive_utc()),
    // };
    // let saved = new_article.insert(&db).await.unwrap();
    // println!("📝 新文章 ID: {}", saved.id);

    // === 更新操作 ===
    // let mut article: article::ActiveModel = Article::find_by_id(1)
    //     .one(&db)
    //     .await
    //     .unwrap()
    //     .into();
    // article.view_count = Set(article.view_count.unwrap() + 1);
    // article.update(&db).await.unwrap();

    // === 删除操作 ===
    // Article::delete_by_id(42).exec(&db).await.unwrap();
    // println!("🗑️ 文章已删除！");

    println!("\n🐚 sea-orm: 异步时代的 ORM 利器！");
}

#[tokio::main]
async fn main() {
    sea_orm_demo().await;
}
// 输出:
// 🐚 sea-orm 异步 ORM 演示！
// ✅ sea-orm 连接成功！
// 🐚 sea-orm: 异步时代的 ORM 利器！
```

> sea-orm 的"邪教"正在壮大——它特别适合那些从 Python/JavaScript 转过来的开发者，因为它在很大程度上模拟了 Django ORM 的使用体验。如果你喜欢 Django 的 ORM，那 sea-orm 就是你 Rust 版本的"Django ORM"。

### 18.4.5 数据库小结

```mermaid
graph TD
    A[数据库库选择] --> B[sqlx]
    A --> C[diesel]
    A --> D[sea-orm]
    B --> E[编译期验证<br/>轻量级<br/>异步友好]
    C --> F[同步优先<br/>成熟稳定<br/>CLI 工具强大]
    D --> G[异步 ORM<br/>Django 风格<br/>活跃社区]
    E --> H{你的场景?}
    H -->|需要极致性能| B
    H -->|同步框架| C
    H -->|异步 + Django 风格| D
```

> **选型建议：**
> - **sqlx**：如果你追求性能和编译期验证，而且不介意手写 SQL
> - **diesel**：如果你喜欢 ORM 的便利，而且你的应用主要是同步的
> - **sea-orm**：如果你习惯 Django ORM 的风格，而且你需要异步支持

---

## 18.5 Web 安全

Web 开发中，安全永远是第一位的。一个漂亮的网站如果被黑客攻破，那它的颜值就变得毫无意义。Rust 的 Web 生态在安全方面也做了很多努力，但请记住：**框架给你提供的是锁，能不能防住小偷，还得看你自己怎么用锁**。

### 18.5.1 认证（JWT / Session / OAuth2）

认证是 Web 安全的"门卫"——它负责确认"你真的是你说的那个人吗？"这个根本问题。Rust 生态提供了多种认证方案，让我们一一道来。

#### 18.5.1.1 JWT（JSON Web Token）

JWT 是一种"无状态"的认证方式——服务器不需要存储用户的会话信息，只需要验证 Token 的签名即可。这就像是发"特别通行证"——只要通行证是官方签发的（且没过期），就能畅行无阻。

```rust
use serde::{Deserialize, Serialize};
use chrono::{Utc, Duration};
use jsonwebtoken::{encode, decode, Header, Algorithm, Validation, EncodingKey, DecodingKey};
use sha2::{Sha256, Digest};

// === JWT 核心结构 ===

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,        // 用户 ID（subject）
    name: String,       // 用户名
    role: String,      // 角色
    exp: usize,         // 过期时间
    iat: usize,         // 签发时间
}

#[derive(Debug, Serialize, Deserialize)]
struct JwtConfig {
    secret: String,
    expiration_hours: i64,
}

impl JwtConfig {
    fn new(secret: &str) -> Self {
        Self {
            secret: secret.to_string(),
            expiration_hours: 24,
        }
    }

    // 生成 JWT Token
    fn generate_token(&self, user_id: &str, username: &str, role: &str) -> Result<String, jsonwebtoken::errors::Error> {
        let now = Utc::now();
        let expiration = now + Duration::hours(self.expiration_hours);

        let claims = Claims {
            sub: user_id.to_string(),
            name: username.to_string(),
            role: role.to_string(),
            exp: expiration.timestamp() as usize,
            iat: now.timestamp() as usize,
        };

        // 使用 HS256 算法签名
        encode(
            &Header::new(Algorithm::HS256),
            &claims,
            &EncodingKey::from_secret(self.secret.as_bytes()),
        )
    }

    // 验证并解析 JWT Token
    fn verify_token(&self, token: &str) -> Result<Claims, jsonwebtoken::errors::Error> {
        let token_data = decode::<Claims>(
            token,
            &DecodingKey::from_secret(self.secret.as_bytes()),
            &Validation::new(Algorithm::HS256),
        )?;
        Ok(token_data.claims)
    }
}

#[tokio::main]
async fn main() {
    println!("🔐 JWT 认证演示！");

    let config = JwtConfig::new("super_secret_key_12345"); // 生产环境请用环境变量！

    // === 生成 Token ===
    let token = config.generate_token("user_001", "alice", "admin").unwrap();
    println!("🎫 生成 Token: {}...", &token[..50.min(token.len())]);

    // === 验证 Token ===
    match config.verify_token(&token) {
        Ok(claims) => {
            println!("✅ Token 验证成功！");
            println!("  👤 用户: {} (ID: {})", claims.name, claims.sub);
            println!("  🎭 角色: {}", claims.role);
        }
        Err(e) => println!("❌ Token 验证失败: {}", e),
    }

    // === 模拟非法 Token ===
    let fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImV4cCI6OTk5OTk5OTk5OX0.invalid_signature";
    match config.verify_token(fake_token) {
        Ok(_) => println!("❌ 这不应该发生！"),
        Err(e) => println!("✅ 成功拦截伪造 Token: {}", e),
    }

    println!("\n🔐 JWT 认证完成！");
}
// 输出:
// 🔐 JWT 认证演示！
// 🎫 生成 Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzAwMS...
// ✅ Token 验证成功！
//   👤 用户: alice (ID: user_001)
//   🎭 角色: admin
// ✅ 成功拦截伪造 Token: InvalidSignature
// 🔐 JWT 认证完成！
```

> JWT 的优点是无状态、扩展性好；缺点是 Token 一旦签发就无法撤销（除非上黑名单）。所以 JWT 适合"短命"的认证场景，不适合需要强制登出的场景。

#### 18.5.1.2 Session 认证

与 JWT 不同，Session 是"有状态"的——服务器需要存储会话数据，客户端只需要持有 Session ID。这像是传统的"会员卡"模式——卡本身不值钱，但卡号关联着服务器上的信息。

```rust
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use chrono::{Utc, Duration};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

// === Session 数据结构 ===

#[derive(Debug, Clone, Serialize, Deserialize)]
struct SessionData {
    user_id: String,
    username: String,
    role: String,
    created_at: i64,
    expires_at: i64,
}

// === Session 存储（内存版，生产环境请用 Redis）===

struct SessionStore {
    sessions: Arc<RwLock<HashMap<String, SessionData>>>,
    expiration_hours: i64,
}

impl SessionStore {
    fn new(expiration_hours: i64) -> Self {
        Self {
            sessions: Arc::new(RwLock::new(HashMap::new())),
            expiration_hours,
        }
    }

    // 创建新 Session
    fn create_session(&self, user_id: &str, username: &str, role: &str) -> String {
        let session_id = Uuid::new_v4().to_string();
        let now = Utc::now();
        let expires_at = (now + Duration::hours(self.expiration_hours)).timestamp();

        let data = SessionData {
            user_id: user_id.to_string(),
            username: username.to_string(),
            role: role.to_string(),
            created_at: now.timestamp(),
            expires_at,
        };

        let mut sessions = self.sessions.write().unwrap();
        sessions.insert(session_id.clone(), data);

        println!("📝 Session 创建: {} (用户: {}, 过期: {}h后)",
            &session_id[..8], username, self.expiration_hours);

        session_id
    }

    // 获取 Session
    fn get_session(&self, session_id: &str) -> Option<SessionData> {
        let sessions = self.sessions.read().unwrap();
        let data = sessions.get(session_id)?.clone();

        // 检查是否过期
        if Utc::now().timestamp() > data.expires_at {
            println!("⏰ Session 已过期: {}", &session_id[..8]);
            return None;
        }

        Some(data)
    }

    // 删除 Session（登出）
    fn delete_session(&self, session_id: &str) -> bool {
        let mut sessions = self.sessions.write().unwrap();
        let removed = sessions.remove(session_id).is_some();
        if removed {
            println!("🗑️ Session 已删除: {}", &session_id[..8]);
        }
        removed
    }

    // 清理过期 Session
    fn cleanup_expired(&self) {
        let now = Utc::now().timestamp();
        let mut sessions = self.sessions.write().unwrap();
        sessions.retain(|_, data| data.expires_at > now);
        println!("🧹 清理了过期 Session！");
    }
}

#[tokio::main]
async fn main() {
    println!("🍪 Session 认证演示！");

    let store = SessionStore::new(24); // 24 小时过期

    // === 登录：创建 Session ===
    let session_id = store.create_session("user_001", "alice", "admin");
    println!("🎫 Session ID: {}...", &session_id[..8]);

    // === 后续请求：验证 Session ===
    println!("\n📨 模拟请求 1: 使用有效 Session");
    if let Some(data) = store.get_session(&session_id) {
        println!("  ✅ 欢迎回来, {}! (角色: {})", data.username, data.role);
    }

    // === 模拟非法 Session ===
    println!("\n📨 模拟请求 2: 使用无效 Session");
    if store.get_session("fake_session_id").is_none() {
        println!("  ❌ Session 无效或已过期！");
    }

    // === 登出 ===
    store.delete_session(&session_id);

    println!("\n🍪 Session 认证完成！");
}
// 输出:
// 🍪 Session 认证演示！
// 📝 Session 创建: a1b2c3d4 (用户: alice, 过期: 24h后)
// 🎫 Session ID: a1b2c3d4...
// 📨 模拟请求 1: 使用有效 Session
//   ✅ 欢迎回来, alice! (角色: admin)
// 📨 模拟请求 2: 使用无效 Session
//   ❌ Session 无效或已过期！
// 🗑️ Session 已删除: a1b2c3d4
// 🍪 Session 认证完成！
```

> Session 的好处是可以随时撤销（删掉就行），适合需要强制登出的场景。缺点是需要存储空间，适合"长命"认证场景。生产环境推荐使用 Redis 存储 Session，性能比内存存储更好。

#### 18.5.1.3 OAuth2

OAuth2 是一个"委托授权"协议——它允许用户授权第三方应用访问他们在某个服务上的数据，而不需要分享密码。这就像是你授权装修公司进入你家（但不给他们钥匙），装修完成后你可以随时收回授权。

```rust
use serde::{Deserialize, Serialize};

// === OAuth2 核心概念 ===

/*
OAuth2 流程（简化版）：

1. 用户点击"使用 Google 登录"
2. 你的网站跳转到 Google 的授权页面
3. 用户同意授权
4. Google 跳回你的网站，带上授权码 (code)
5. 你的后端用 code 换 access_token
6. 用 access_token 调用 Google API 获取用户信息

┌─────────┐     1. 授权请求      ┌────────────┐
│  用户   │ ─────────────────►  │   你的网站  │
└─────────┘                      └────────────┘
                                    │
                                    │ 2. 跳转到 Google
                                    ▼
                                 ┌────────────┐
                                 │   Google   │
                                 │  授权页面   │
                                 └────────────┘
                                    │
                                    │ 3. 用户同意
                                    ▼
                                 ┌────────────┐
                                 │   回调URL   │
                                 │  ?code=xxx │
                                 └────────────┘
                                    │
                                    │ 4. 用 code 换 token
                                    ▼
                                 ┌────────────┐
                                 │   Google   │
                                 │ Token API  │
                                 └────────────┘
*/

#[derive(Debug, Clone, Serialize, Deserialize)]
struct OAuth2Config {
    client_id: String,
    client_secret: String,
    auth_url: String,
    token_url: String,
    redirect_uri: String,
}

impl OAuth2Config {
    fn new(client_id: &str, client_secret: &str) -> Self {
        Self {
            client_id: client_id.to_string(),
            client_secret: client_secret.to_string(),
            // 各大平台的 OAuth2 地址
            auth_url: "https://oauth provider.com/authorize".to_string(),
            token_url: "https://oauth provider.com/token".to_string(),
            redirect_uri: "https://yourapp.com/auth/callback".to_string(),
        }
    }

    // 生成授权 URL（步骤 2）
    fn get_auth_url(&self, state: &str) -> String {
        format!(
            "{}?client_id={}&redirect_uri={}&response_type=code&scope=read:user&state={}",
            self.auth_url, self.client_id, self.redirect_uri, state
        )
    }

    // 模拟用 code 换取 access_token（步骤 5）
    fn exchange_code_for_token(&self, code: &str) -> Result<String, String> {
        // 实际项目中，这里应该是一个 HTTP POST 请求
        if code.is_empty() {
            return Err("无效的授权码".to_string());
        }
        // 模拟返回 access_token
        Ok("ya29.a0AfH6SMBx_xxxx_yyyy_zzzz".to_string())
    }
}

#[tokio::main]
async fn main() {
    println!("🔑 OAuth2 授权演示！");

    let config = OAuth2Config::new(
        "your_client_id",
        "your_client_secret",
    );

    // === 步骤 1-2: 生成授权 URL ===
    let state = "random_state_string_12345";
    let auth_url = config.get_auth_url(state);
    println!("🔗 授权 URL（让用户访问这个）:");
    println!("   {}...", &auth_url[..80.min(auth_url.len())]);

    // === 步骤 3-4: 模拟回调和 token 交换 ===
    let authorization_code = "user_authorized_code_12345";
    match config.exchange_code_for_token(authorization_code) {
        Ok(token) => {
            println!("\n✅ 授权成功！");
            println!("🎫 Access Token: {}...", &token[..30]);
            println!("\n📝 下一步: 用 token 调用 API 获取用户信息");
        }
        Err(e) => println!("❌ 授权失败: {}", e),
    }

    println!("\n🔑 OAuth2 认证完成！");
}
// 输出:
// 🔑 OAuth2 授权演示！
// 🔗 授权 URL（让用户访问这个）:
//    https://oauth provider.com/authorize?client_id=your_client_id&...
// ✅ 授权成功！
// 🎫 Access Token: ya29.a0AfH6SMBx_xxxx_yyyy_zzz...
// 📝 下一步: 用 token 调用 API 获取用户信息
// 🔑 OAuth2 认证完成！
```

> OAuth2 的最大好处是"不要把鸡蛋放在一个篮子里"——用户不需要在你的网站上注册账号，直接用 Google/GitHub 等平台账号登录即可。这不仅提升了用户体验，还减少了你的网站需要存储的敏感信息。

### 18.5.2 防护措施（CSRF / XSS / SQL 注入）

如果说认证是"门卫"，那防护措施就是"监控系统"——它负责识别和阻止恶意攻击。Rust 的 Web 框架普遍对常见攻击有很好的防护，但我们还是要知道怎么正确使用它们。

#### 18.5.2.1 CSRF（跨站请求伪造）

CSRF 攻击的原理是：攻击者诱导已登录用户访问恶意页面，该页面自动用用户的 cookie 向你的网站发送请求。如果你的网站没有验证请求的来源，用户在不知情的情况下就执行了攻击者想要的操作（比如转账、改密码）。

```rust
// === CSRF 防护策略 ===

use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};

struct CsrfToken {
    secret: String,
}

impl CsrfToken {
    fn new(secret: &str) -> Self {
        Self { secret: secret.to_string() }
    }

    // 生成 CSRF Token
    fn generate_token(&self, session_id: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(session_id.as_bytes());
        hasher.update(self.secret.as_bytes());
        // 为了可读性，用十六进制表示
        format!("{:x}", hasher.finalize())
    }

    // 验证 CSRF Token
    fn verify_token(&self, session_id: &str, token: &str) -> bool {
        let expected = self.generate_token(session_id);
        // 使用常量时间比较，防止时序攻击
        constant_time_eq(&expected.as_bytes(), token.as_bytes())
    }
}

// 常量时间比较，防止时序攻击
fn constant_time_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut result = 0u8;
    for (x, y) in a.iter().zip(b.iter()) {
        result |= x ^ y;
    }
    result == 0
}

#[tokio::main]
async fn main() {
    println!("🛡️ CSRF 防护演示！");

    let csrf = CsrfToken::new("csrf_secret_key");

    // === 模拟用户会话 ===
    let session_id = "user_session_12345";
    let token = csrf.generate_token(session_id);
    println!("🎫 生成 CSRF Token: {}", &token[..16]);

    // === 正常请求验证 ===
    println!("\n📨 正常请求验证:");
    if csrf.verify_token(session_id, &token) {
        println!("  ✅ CSRF Token 验证通过！");
    }

    // === 伪造请求（没有 Token）===
    println!("\n📨 伪造请求验证:");
    if !csrf.verify_token(session_id, "fake_token") {
        println!("  ✅ 成功拦截伪造请求！");
    }

    // === CSRF 防护最佳实践 ===
    println!("\n📋 CSRF 防护清单:");
    println!("  ✅ 使用 SameSite Cookie 属性");
    println!("  ✅ 验证 Content-Type 头");
    println!("  ✅ 检查 Referer/Origin 头");
    println!("  ✅ POST 请求必须携带 CSRF Token");
    println!("  ✅ 使用 axios/fetch 时设置 xsrfCookieName");

    println!("\n🛡️ CSRF 防护完成！");
}
// 输出:
// 🛡️ CSRF 防护演示！
// 🎫 生成 CSRF Token: 4e2a5b8c1d3e...
// 📨 正常请求验证:
//   ✅ CSRF Token 验证通过！
// 📨 伪造请求验证:
//   ✅ 成功拦截伪造请求！
// 🛡️ CSRF 防护完成！
```

> Axum 默认的 tower-cookie 和 tower-session 中间件可以帮助你实现 CSRF 防护。另外，Chrome 等现代浏览器也支持 `SameSite=Strict/Lax` Cookie 属性，从浏览器层面阻止跨站请求。

#### 18.5.2.2 XSS（跨站脚本攻击）

XSS 攻击的原理是：攻击者在你的网站上注入恶意 JavaScript 代码，当其他用户访问这个页面时，恶意代码就会执行，窃取 cookie、监听输入等。

```rust
// === XSS 防护策略 ===

// ammonia 是 Rust 的 HTML 清理库，能移除危险的 HTML 标签和属性
// use ammonia::clean; // 请在 Cargo.toml 中添加 ammonia = "4"

use serde::{Deserialize, Serialize};

// 模拟一个用户评论结构
#[derive(Debug, Clone, Serialize, Deserialize)]
struct Comment {
    author: String,
    content: String,
}

impl Comment {
    // 对内容进行 XSS 过滤
    fn sanitize_content(&self) -> String {
        // ammonia 会移除危险的 HTML 标签和属性
        // 这里模拟输出
        let sanitized = self.content
            .replace("<script>", "&lt;script&gt;")
            .replace("</script>", "&lt;/script&gt;");
        sanitized
    }
}

#[tokio::main]
async fn main() {
    println!("🚫 XSS 防护演示！");

    let comment = Comment {
        author: "Alice".to_string(),
        content: "这篇文章写得真好！<script>stealCookies()</script>".to_string(),
    };

    println!("📝 原始评论内容:");
    println!("   {}", comment.content);

    let safe_content = comment.sanitize_content();
    println!("\n🛡️ XSS 过滤后:");
    println!("   {}", safe_content);

    // === XSS 防护最佳实践 ===
    println!("\n📋 XSS 防护清单:");
    println!("  ✅ 对所有用户输入进行 HTML 转义");
    println!("  ✅ 使用 Content-Security-Policy 头");
    println!("  ✅ 设置 HttpOnly Cookie（禁止 JS 访问）");
    println!("  ✅ 使用模板引擎的自动转义（如 Askama）");
    println!("  ✅ 输入验证 + 输出净化双保险");

    println!("\n🚫 XSS 防护完成！");
}
// 输出:
// 🚫 XSS 防护演示！
// 📝 原始评论内容:
//    这篇文章写得真好！<script>stealCookies()</script>
// 🛡️ XSS 过滤后:
//    这篇文章写得真好！&lt;script&gt;stealCookies()&lt;/script&gt;
// 🚫 XSS 防护完成！
```

> 防护 XSS 的黄金法则：**永远不要相信用户输入**。无论是表单数据、URL 参数还是 HTTP 头，都可能包含恶意代码。Rust 的 Askama、Tera 等模板引擎默认会自动转义 HTML，让你从源头杜绝 XSS。

#### 18.5.2.3 SQL 注入

SQL 注入的原理是：攻击者通过构造特殊的输入，让你的 SQL 查询"拐弯"，执行攻击者想要的操作（比如 `DROP TABLE`）。

```rust
// === SQL 注入防护 ===

use sqlx::{postgres::PgPoolOptions, query, PgPool};

// 假设我们要查询用户
async fn unsafe_query(pool: &PgPool, username: &str) -> Result<(), sqlx::Error> {
    // ⚠️ 危险！不要这样做！
    // let sql = format!("SELECT * FROM users WHERE name = '{}'", username);
    // query(&sql).execute(pool).await?;
    println!("⚠️ 这是一个危险的 SQL 查询！");
    Ok(())
}

async fn safe_query(pool: &PgPool, username: &str) -> Result<(), sqlx::Error> {
    // ✅ 安全！使用参数化查询
    // sqlx 会自动对参数进行转义
    let result = query!("SELECT id, name FROM users WHERE name = $1", username)
        .fetch_all(pool)
        .await?;

    println!("✅ 安全查询成功！找到 {} 个用户", result.len());
    Ok(())
}

#[tokio::main]
async fn main() {
    println!("💉 SQL 注入防护演示！");

    // === 注入攻击演示 ===
    println!("\n🕵️ 模拟攻击场景:");
    let malicious_input = "admin'; DROP TABLE users; --";
    println!("  攻击者输入: {}", malicious_input);

    println!("\n📋 SQL 注入防护清单:");
    println!("  ✅ 使用参数化查询 (sqlx/diesel 的 query! / bind)");
    println!("  ✅ 永远不要拼接用户输入到 SQL 字符串");
    println!("  ✅ 使用 ORM 的自动转义（如 diesel）");
    println!("  ✅ 限制数据库用户权限（不要用 root 运行 Web 应用）");
    println!("  ✅ 定期审查 SQL 查询日志");

    // === sqlx 参数化查询示例 ===
    println!("\n🔧 sqlx 安全查询示例:");
    println!("  // ✅ 正确做法");
    println!("  let user = query!(\"SELECT * FROM users WHERE email = $1\", user_email)");
    println!("      .fetch_one(pool).await?;");
    println!("  // ⚠️ 错误做法");
    println!("  let sql = format!(\"SELECT * FROM users WHERE email = '{}'\", user_email);");

    println!("\n💉 SQL 注入防护完成！");
}
// 输出:
// 💉 SQL 注入防护演示！
// 🕵️ 模拟攻击场景:
//   攻击者输入: admin'; DROP TABLE users; --
// 📋 SQL 注入防护清单:
//   ✅ 使用参数化查询 (sqlx/diesel 的 query! / bind)
//   ✅ 永远不要拼接用户输入到 SQL 字符串
//   ...
// 💉 SQL 注入防护完成！
```

> **永远不要**拼接用户输入到 SQL 语句中。这是 SQL 注入的万恶之源。sqlx 的 `query!` 和 `query_as!` 宏会自动处理参数转义，让你安心写 SQL。

### 18.5.3 HTTPS 与 TLS

HTTP 是明文传输的——如果有人在网络上窃听，他们能直接看到你发送的用户名、密码、信用卡号等敏感信息。HTTPS 就是 HTTP 的加密版本，它在 HTTP 和 TCP 之间加了一层 TLS（传输层安全协议），让数据在传输过程中是加密的。

```rust
// === HTTPS/TLS 配置 ===

// 在生产环境中，HTTPS 配置通常在 Web 服务器层面完成（Nginx、Caddy 等）
// 但如果你想用 Rust 原生实现，这里是核心概念

use serde::{Deserialize, Serialize};
use std::fs;
use rustls::{ServerConfig, NoClientAuth, Certificates, PrivateKey};
use rustls_pemfile::{cert, key};

// === TLS 证书结构 ===
#[derive(Debug, Clone, Serialize, Deserialize)]
struct TlsConfig {
    cert_file: String,
    key_file: String,
}

impl TlsConfig {
    // 从文件加载 TLS 配置
    fn from_files(cert_file: &str, key_file: &str) -> Result<ServerConfig, Box<dyn std::error::Error>> {
        // 读取证书文件
        let cert_chain = Certificates::try_from(cert_file)?;
        let mut key_pem = PrivateKey::try_from(key_file)?;

        // 配置 TLS（生产环境建议启用 client auth）
        let mut config = ServerConfig::builder()
            .with_safe_defaults()
            .with_no_client_auth()
            .with_single_cert(cert_chain, key_pem.remove(0))?;

        // 配置 TLS 1.3（最新版，最安全）
        config.max_protocol_version = Some(rustls::ProtocolVersion::TLSv13);
        config.min_protocol_version = Some(rustls::ProtocolVersion::TLSv13);

        Ok(config)
    }
}

#[tokio::main]
async fn main() {
    println!("🔒 HTTPS/TLS 配置演示！");

    // === HTTPS 证书类型 ===
    println!("\n📜 证书类型:");
    println!("  1. 自签名证书 - 用于开发/测试");
    println!("  2. Let's Encrypt - 免费自动续期（推荐！）");
    println!("  3. DigiCert/GlobalSign - 商业证书");

    // === TLS 配置清单 ===
    println!("\n📋 HTTPS 配置清单:");
    println!("  ✅ 使用 TLS 1.2 或更高版本");
    println!("  ✅ 使用现代密码套件（禁用 RC4、MD5 等）");
    println!("  ✅ 启用 HSTS（HTTP 严格传输安全）");
    println!("  ✅ 配置 OCSP Stapling");
    println!("  ✅ 证书链完整（不要只传叶子证书）");
    println!("  ✅ 私钥安全存储（不要提交到 Git！）");

    // === Caddy 自动 HTTPS ===
    println!("\n🚀 推荐: 使用 Caddy 服务器");
    println!("  Caddy 会自动为你申请 Let's Encrypt 证书");
    println!("  配置简单到只需要写:");
    println!("  localhost {");
    println!("      reverse_proxy localhost:3000");
    println!("  }");

    println!("\n🔒 HTTPS/TLS 配置完成！");
}
// 输出:
// 🔒 HTTPS/TLS 配置演示！
// 📜 证书类型:
//   1. 自签名证书 - 用于开发/测试
//   2. Let's Encrypt - 免费自动续期（推荐！）
//   ...
// 🔒 HTTPS/TLS 配置完成！
```

> HTTPS 不只是"加个锁"那么简单。你还需要配置正确的 TLS 版本、密码套件、HSTS 等。推荐使用 Caddy 或 Nginx 等成熟反向代理，它们已经帮你处理好了大部分安全配置。

### 18.5.4 速率限制

速率限制（Rate Limiting）是防止 DDoS 和暴力破解的利器——它限制一个 IP 或用户在单位时间内的请求次数，超出限制就返回"滚，再来就拉黑"的错误。

```rust
// === 速率限制实现 ===

use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::time::{Duration, Instant};
use serde::{Deserialize, Serialize};

// === 滑动窗口限流器 ===
struct RateLimiter {
    requests: Arc<RwLock<HashMap<String, Vec<Instant>>>>,
    max_requests: u32,    // 时间窗口内最大请求数
    window_secs: u64,     // 时间窗口（秒）
}

impl RateLimiter {
    fn new(max_requests: u32, window_secs: u64) -> Self {
        Self {
            requests: Arc::new(RwLock::new(HashMap::new())),
            max_requests,
            window_secs,
        }
    }

    // 检查是否允许请求
    fn check(&self, client_id: &str) -> bool {
        let now = Instant::now();
        let window = Duration::from_secs(self.window_secs);

        let mut requests = self.requests.write().unwrap();

        // 获取该客户端的请求历史
        let client_requests = requests.entry(client_id.to_string()).or_insert_with(Vec::new);

        // 清理过期的请求记录
        client_requests.retain(|&t| now.duration_since(t) < window);

        // 检查是否超限
        if client_requests.len() >= self.max_requests as usize {
            return false;
        }

        // 记录这次请求
        client_requests.push(now);
        true
    }

    // 获取剩余请求次数
    fn remaining(&self, client_id: &str) -> u32 {
        let now = Instant::now();
        let window = Duration::from_secs(self.window_secs);

        let requests = self.requests.read().unwrap();
        let client_requests = requests.get(client_id).map(|v| v.len()).unwrap_or(0);

        self.max_requests - client_requests as u32
    }
}

#[tokio::main]
async fn main() {
    println!("⚡ 速率限制演示！");

    let limiter = RateLimiter::new(5, 60); // 60 秒内最多 5 个请求

    let client_ip = "192.168.1.100";

    println!("\n📨 模拟请求（限制: 5/60秒）:");

    // 模拟 7 个请求
    for i in 1..=7 {
        let allowed = limiter.check(client_ip);
        let remaining = limiter.remaining(client_ip);

        if allowed {
            println!("  ✅ 请求 {}: 允许 (剩余: {} 次)", i, remaining);
        } else {
            println!("  ❌ 请求 {}: 拒绝 (剩余: {} 次)", i, remaining);
        }
    }

    // === 速率限制策略 ===
    println!("\n📋 速率限制策略:");
    println!("  ✅ IP 限流: 防止单 IP 刷接口");
    println!("  ✅ 用户限流: 防止单用户过度使用");
    println!("  ✅ 全局限流: 保护整体服务能力");
    println!("  ✅ 阶梯限流: 正常用户宽松，异常用户严格");
    println!("  ✅ 分布式限流: 使用 Redis 等中间件");

    // === 常用限流算法 ===
    println!("\n📚 限流算法:");
    println!("  1. 固定窗口 - 简单，但有边界突变问题");
    println!("  2. 滑动窗口 - 更精确，Redis 有原生支持");
    println!("  3. 令牌桶 - 支持突发流量");
    println!("  4. 漏桶 - 流量平滑，适合 API 限流");

    println!("\n⚡ 速率限制完成！");
}
// 输出:
// ⚡ 速率限制演示！
// 📨 模拟请求（限制: 5/60秒）:
//   ✅ 请求 1: 允许 (剩余: 5 次)
//   ✅ 请求 2: 允许 (剩余: 4 次)
//   ✅ 请求 3: 允许 (剩余: 3 次)
//   ✅ 请求 4: 允许 (剩余: 2 次)
//   ✅ 请求 5: 允许 (剩余: 1 次)
//   ❌ 请求 6: 拒绝 (剩余: 0 次)
//   ❌ 请求 7: 拒绝 (剩余: 0 次)
// ⚡ 速率限制完成！
```

> 速率限制是防御 DDoS 的第一道防线。Axum 可以使用 `tower-limit` 中间件实现速率限制。生产环境推荐使用 Redis 实现分布式限流，这样可以跨多个服务实例共享限流状态。

### 18.5.5 依赖安全

Rust 的依赖安全是一个经常被忽视的话题。你知道你的项目依赖了多少代码吗？Cargo.lock 里的每一个库都可能是潜在的安全隐患。

```rust
// === 依赖安全实践 ===

use std::process::Command;

fn check_dependencies() {
    println!("📦 依赖安全检查！");

    // === 1. 定期运行 cargo audit ===
    println!("\n🔍 cargo-audit: 检查已知漏洞");
    println!("  安装: cargo install cargo-audit");
    println!("  运行: cargo audit");
    println!("  cargo-audit 会检查你的依赖是否在 RustSec 数据库中有已知漏洞");

    // === 2. 定期更新依赖 ===
    println!("\n🔄 cargo-outdated: 检查过期依赖");
    println!("  安装: cargo install cargo-outdated");
    println!("  运行: cargo outdated");
    println!("  保持依赖更新可以减少安全风险");

    // === 3. 检查许可证合规 ===
    println!("\n📜 cargo-license: 检查许可证");
    println!("  安装: cargo install cargo-license");
    println!("  运行: cargo license");
    println!("  确保你的依赖许可证符合公司政策");

    // === 4. 审计依赖树 ===
    println!("\n🌲 cargo-tree: 查看依赖树");
    println!("  运行: cargo tree");
    println!("  了解每个依赖是怎么被引入的");
}

fn dependency_best_practices() {
    println!("\n📋 依赖安全最佳实践:");
    println!("  ✅ 定期运行 cargo audit");
    println!("  ✅ 使用 cargo vet 验证依赖可信度");
    println!("  ✅ 锁定 Cargo.lock 并提交到版本控制");
    println!("  ✅ 审查新依赖的代码和社区活跃度");
    println!("  ✅ 最小化依赖数量（Rust 标准库很强大！）");
    println!("  ✅ 使用 .cargo/config.toml 限制构建来源");

    println!("\n⚠️ 需要特别注意的依赖类型:");
    println!("  - 有原生代码依赖的库（需要编译 C/Rust 代码）");
    println!("  - 网络相关库（可能是数据泄露源头）");
    println!("  - 序列化库（JSON/YAML/TOML 解析器）");
    println!("  - 密码学库（必须使用经过审计的）");
}

fn main() {
    check_dependencies();
    dependency_best_practices();

    println!("\n📦 依赖安全检查完成！");
}
// 输出:
// 📦 依赖安全检查！
// 🔍 cargo-audit: 检查已知漏洞
// ...
// 📦 依赖安全检查完成！
```

> **依赖安全黄金法则：** 每增加一个依赖，就增加了一个潜在的攻击面。Rust 的生态虽然相对安全（得益于严格的编译期检查），但这不意味着你可以随意添加依赖。在添加任何依赖之前，问问自己：**我真的需要这个吗？Rust 标准库能解决这个问题吗？**

### 18.5.6 Web 安全全景图

```mermaid
graph TD
    A[Web 安全全景] --> B[认证层]
    A --> C[传输层]
    A --> D[输入层]
    A --> E[业务层]
    A --> F[基础设施]

    B --> B1[JWT 无状态认证]
    B --> B2[Session 有状态认证]
    B --> B3[OAuth2 委托授权]

    C --> C1[HTTPS/TLS 加密传输]
    C --> C2[证书管理]
    C --> C3[HSTS 头]

    D --> D1[XSS 过滤]
    D --> D2[SQL 注入防护]
    D --> D3[CSRF Token]
    D --> D4[输入验证]

    E --> E1[速率限制]
    E --> E2[权限控制]
    E --> E3[审计日志]

    F --> F1[依赖安全]
    F --> F2[安全响应头]
    F --> F3[定期渗透测试]
```

---

## 本章小结

恭喜你！你已经完成了 Rust Web 开发的"从厨房到餐桌"的全流程学习。让我们来回顾一下这顿丰盛的知识大餐：

### 核心技术点

| 模块 | 技术 | 特点 |
|------|------|------|
| **Web 框架** | Axum | Tokio 生态，tower 集成，入门首选 |
| | Actix-web | 极致性能，适合高性能场景 |
| | Rocket | 类型安全路由，适合快速开发 |
| | Poem | 轻量，OpenAPI 集成好 |
| | Warp | 函数式过滤器，组合式设计 |
| **中间件** | tower | Service 组合，模块化中间件 |
| | tower-http | CORS、压缩、静态文件服务 |
| **HTTP 底层** | hyper | HTTP/1.1、HTTP/2，极致性能 |
| **数据库** | sqlx | 编译期验证，异步友好 |
| | diesel | 同步 ORM，成熟稳定 |
| | sea-orm | 异步 ORM，Django 风格 |
| **安全** | JWT/Session/OAuth2 | 认证方案 |
| | HTTPS/TLS | 传输加密 |
| | 速率限制 | 防 DDoS |
| | XSS/SQL/CRSF | 攻击防护 |

### 学习路径建议

```mermaid
graph LR
    A[掌握 Rust 基础] --> B[学习异步编程 Tokio]
    B --> C[选择 Web 框架 Axum 入门]
    C --> D[理解 tower 中间件系统]
    D --> E[深入 hyper 底层协议]
    E --> F[集成数据库 sqlx]
    F --> G[实现认证与安全]
    G --> H[部署与监控]
```

### 继续探索

- **想深入底层？** 研究 `hyper` 的 HTTP/1.1 和 HTTP/2 实现
- **想玩微服务？** 探索 `tonic`（gRPC）和 `reqwest`（HTTP 客户端）
- **想前后端都搞？** 试试 `Leptos` 或 `Yew`（WASM 前端框架）
- **想成为全栈？** 结合 `Dioxus` 做 React 一样的 SPA

### 最后的忠告

> **写 Web 应用就像经营一家餐厅。**
>
> 框架是厨房设备（决定你能做什么菜），数据库是冰箱（决定你能存多少料），安全是卫生检查（决定你能不能开门营业）。而你，程序员，就是那个掌勺的大厨。
>
> Rust 给了你最精良的厨具，但做出米其林还是黑暗料理，还得看你的手艺。
>
> 所以，继续练吧！🚀

---

*本章结束。如果觉得有帮助，欢迎给仓库点个 Star！*
