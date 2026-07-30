+++
title = "43-database-and-sql"
date = 2026-07-28T14:49:00+08:00
weight = 430
type = "docs"
description = "面向 Go 用户讲清 Rust 无 std SQL、sqlx/diesel/SeaORM 选型、池事务迁移与防注入"
isCJKLanguage = true
draft = false

+++

# 数据库与 SQL (Database and SQL)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会像找 `database/sql` 一样在 std 里搜 DB API，结果一无所获？
- 你是否分不清 **sqlx** / **diesel** / **SeaORM** 该选哪个，以及和 Go 的 database/sql + ORM 怎么对照？
- 你是否想知道：连接串放哪、`query!` 和运行时查询差在哪、行怎么映射成 struct、事务与连接池怎么写？
- 你是否担心：在 async 里阻塞、SQL 注入、本地怎么起测试库、迁移（migration）放哪跑？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| SQL | Structured Query Language | 结构化查询语言 | 操作关系库的声明式语言 | 同名 |
| **sqlx** | — | 异步 SQL 工具箱 | 写 SQL + 编译期/运行时检查 + FromRow | `database/sql` + 扫描库 |
| **diesel** | — | 同步 ORM/DSL | 用 Rust DSL 拼查询，偏同步 | GORM / 强类型查询层 |
| **SeaORM** | — | 异步 ORM | Entity + ActiveModel，建在 sqlx 等之上 | GORM / ent 一类 |
| DSN | Data Source Name | 数据源名/连接串 | 如 `postgres://user:pass@host/db` | 同概念 / `sql.Open` 第二参 |
| pool | connection pool | 连接池 | 复用到数据库的 TCP/会话连接 | `sql.DB` 内置池 |
| transaction | — | 事务 | 一组语句要么全成要么全撤 | `Begin` / `Tx` |
| migration | — | 迁移 | 版本化改表结构的脚本/工具 | goose / migrate / golang-migrate |
| prepared statement | — | 预编译语句 | 参数与 SQL 分离，防注入并复用计划 | `Prepare` / `?` 占位 |
| `query!` | sqlx 宏 | 编译期查询宏 | 编译时连库校验 SQL/列类型 | 无直接对应（偏 codegen） |
| FromRow | — | 行映射 trait | 把查询结果行填进 struct | `Scan` / sqlx-go |
| ORM | Object-Relational Mapping | 对象关系映射 | 用对象/Entity 表达表与关系 | GORM 等 |
| async | asynchronous | 异步 | Future/`.await` 做 I/O；见 [31-async](../31-async-programming/) | goroutine + 阻塞驱动为主 |
| env | environment variable | 环境变量 | 运行时注入连接串等配置 | `os.Getenv` |
| NULL | — | SQL 空值 | 列无值；映射到 Rust 常用 `Option<T>` | `sql.Null*` / 指针 / `sql.NullString` |
| batch insert | — | 批量插入 | 一次插入多行，减少往返 | 多值 `INSERT` / `CopyIn` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q10](#q10), [Q15](#q15) |
| `common` | [Q8](#q8), [Q9](#q9), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. 为什么 Rust 标准库没有 `database/sql`？ {#q1}
**Tags:** `hot` `beginner` `stdlib` `ecosystem`
**适用版本:** Rust 1.0+（生态选型；与具体 crate 版本无关）

**一句话答案：**
Rust **std 不提供**通用 SQL / 数据库客户端；连接、驱动、池、ORM 全在 crates.io。对标 Go 的 `database/sql` 时，想的是 **sqlx**（或 diesel / SeaORM），不是 `std::`。

**解答：**
Go 把「驱动接口 + 连接池类型」放进标准库：`database/sql` + 第三方 `driver`。Rust 的 std 刻意停在文件系统、套接字、并发原语——数据库协议、TLS 细节、异步模型不绑死进语言发行版。

你能在 std 里做的，只是「自己读配置、自己开 TCP」这类底层事，例如确认环境变量存在（配置细节见 [44-configuration](../44-configuration/) 与 [04-running](../04-running/)）：

```rust
fn main() {
    match std::env::var("DATABASE_URL") {
        Ok(url) => println!("got DATABASE_URL (len={})", url.len()),
        Err(_) => eprintln!("DATABASE_URL not set"),
    }
}
```

真正连库要加依赖（示意，版本随你锁定）：

```toml
# 异步 SQL（常见入门）
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```text
// 示意：需本机 Postgres + 正确 DATABASE_URL；勿当可独立 rustc 的片段
use sqlx::postgres::PgPoolOptions;

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let url = std::env::var("DATABASE_URL").expect("DATABASE_URL");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&url)
        .await?;
    let one: i64 = sqlx::query_scalar("SELECT 1")
        .fetch_one(&pool)
        .await?;
    println!("ok: {one}");
    Ok(())
}
```

**Go 对比：**

```go
import (
    "database/sql"
    _ "github.com/lib/pq" // 或 pgx stdlib
)

db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
```

- **Go 怎么做**：stdlib 定义 `DB`/`Tx`/`Rows`；驱动用 blank import 注册。
- **Rust 为什么不同**：避免把驱动生态与 async 运行时钉进 std；用 Cargo feature 选 Postgres/MySQL/SQLite。
- **Go 程序员易踩的坑**：搜 `std database` 无果就以为 Rust「不能写 SQL」——其实是 `cargo add sqlx`。

**记忆点：**
- 无 std SQL；生态默认从 **sqlx** 起步。
- `DATABASE_URL` + 驱动 feature，对标 `sql.Open`。

---

## Q2. sqlx、diesel、SeaORM 怎么选？ {#q2}
**Tags:** `hot` `beginner` `sqlx` `diesel` `SeaORM` `ORM`
**适用版本:** 选型原则；具体以各 crate 当前文档为准

**一句话答案：**
想「手写 SQL、异步、编译期校验」→ **sqlx**；想「Rust DSL / 同步 ORM 感」→ **diesel**；想「Entity + 异步 ORM、少写 SQL」→ **SeaORM**。多数 Go 用户从 sqlx 最顺。

**解答：**

| 需求 | 更合适 | 不太合适 |
|------|--------|----------|
| 熟悉 `QueryRow` / 手写 SQL | sqlx | 硬上 ORM 只会更绕 |
| 编译期校验 SQL/列 | sqlx `query!`（需连库） | 纯运行时字符串永远无此保障 |
| 强 DSL、迁移工具链一体 | diesel | 只要几条 SQL 的小服务 |
| async + ActiveRecord/Entity 风格 | SeaORM | 想完全掌控每条 SQL 文本 |
| 嵌入式/同步工具 | diesel 或 sqlx（SQLite） | 无脑上重 ORM |

依赖形态对比（示意）：

```toml
# A) sqlx：SQL 文本为主
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros"] }

# B) diesel：同步 DSL（另需 diesel_cli 做迁移）
diesel = { version = "2", features = ["postgres"] }

# C) SeaORM：异步 ORM（底层常走 sqlx）
sea-orm = { version = "1", features = ["sqlx-postgres", "runtime-tokio-native-tls"] }
```

```text
// sqlx：你看见的就是 SQL
let n: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM users")
    .fetch_one(&pool)
    .await?;

// SeaORM：你看见的是 Entity API（示意）
// let count = Users::find().count(db).await?;
```

选型口诀：团队已写惯 SQL、要 async → sqlx；要「表即类型、少碰 SQL」→ SeaORM；偏同步服务/经典 ORM → diesel。

**Go 对比：**
- **Go 怎么做**：`database/sql` 手写 SQL；要 ORM 再选 GORM / ent / sqlc。
- **Rust 为什么不同**：没有「官方 database/sql」，三大路线都是社区主流，选错的成本是心智模型而不是「违规」。
- **Go 程序员易踩的坑**：把 SeaORM 当成唯一答案，或把 diesel 的同步 DSL 硬塞进全 async 服务。

**记忆点：**
- sqlx ≈ database/sql + 更好的扫描/宏。
- SeaORM / diesel ≈ ORM 层；先问「要不要手写 SQL」。

---

## Q3. 连接串和 env 怎么管？ {#q3}
**Tags:** `hot` `beginner` `DSN` `DATABASE_URL` `env`
**适用版本:** 与具体驱动无关；配置习惯见 [44-configuration](../44-configuration/)

**一句话答案：**
用 **DSN**（Data Source Name，数据源名/连接串，常叫 `DATABASE_URL`）放环境变量；代码里 `std::env::var` 读取，**不要**把密码写进仓库。本地可用 dotenvy，生产靠编排注入。

**解答：**
约定俗成的变量名是 `DATABASE_URL`：

```text
postgres://app:secret@localhost:5432/appdb
mysql://user:pass@127.0.0.1:3306/appdb
sqlite:data.db
```

标准库只负责读字符串：

```rust
fn database_url() -> Result<String, std::env::VarError> {
    std::env::var("DATABASE_URL")
}

fn main() {
    match database_url() {
        Ok(u) => println!("url loaded, starts with: {}", &u[..u.find(':').unwrap_or(0)]),
        Err(e) => eprintln!("missing DATABASE_URL: {e}"),
    }
}
```

```toml
# 本地开发可选（勿提交含密钥的 .env）
[dependencies]
dotenvy = "0.15"
```

```text
// 进程启动最早处加载 .env，再读 env（生产可省略）
dotenvy::dotenv().ok();
let url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
```

密钥分层、文件与 CLI 覆盖顺序见 [44-configuration](../44-configuration/)；进程如何带着 env 启动见 [04-running](../04-running/)。

**Go 对比：**

```go
dsn := os.Getenv("DATABASE_URL")
db, err := sql.Open("postgres", dsn)
```

- **Go 怎么做**：同样推荐 env 注入 DSN，而不是写死在源码。
- **Rust 为什么不同**：读 env 的 API 更「显式 Err」；其余习惯几乎一样。
- **Go 程序员易踩的坑**：把 `.env` 提交进 git，或在库代码里 `expect` 掉缺失配置却不在二进制入口统一处理。

**记忆点：**
- `DATABASE_URL` 进 env，不进仓库。
- dotenvy 仅开发；生产靠平台注入。

---

## Q4. `query!` 和运行时查询差在哪？ {#q4}
**Tags:** `hot` `sqlx` `query!` `macros` `compile-time`
**适用版本:** sqlx 0.7+/0.8.x（宏需对应 features 与可连库或 offline 数据）

**一句话答案：**
**运行时** `sqlx::query` / `query_as`：启动后才发现 SQL/列错；**`query!` / `query_as!`**：编译期（或 offline 元数据）校验 SQL 与类型。动态 SQL、无 DB 的 CI 常用运行时；固定查询优先宏。

**解答：**

```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros"] }
```

运行时查询（灵活，错在运行时暴露）：

```text
let row = sqlx::query("SELECT id, email FROM users WHERE id = $1")
    .bind(user_id)
    .fetch_one(&pool)
    .await?;
let id: i64 = row.get("id");
```

编译期宏（示意；需 `DATABASE_URL` 或 `SQLX_OFFLINE=true` + `.sqlx` 数据）：

```text
// query!：编译器根据真实 schema 检查列名/类型
let row = sqlx::query!("SELECT id, email FROM users WHERE id = $1", user_id)
    .fetch_one(&pool)
    .await?;
// row.id / row.email 已是生成好的字段
println!("{} {}", row.id, row.email);
```

| | 运行时 `query` | 宏 `query!` |
|--|----------------|-------------|
| SQL 拼错 | 运行时 Err | 编译失败（有元数据时） |
| 动态表名/片段 | 容易 | 基本不适合 |
| CI 无数据库 | 自然 | 需 offline 或可连库 |

**Go 对比：**
- **Go 怎么做**：默认全是运行时；要编译期安心多用 **sqlc** 等生成代码。
- **Rust 为什么不同**：sqlx 把「连库校验」收进宏，接近 sqlc，但仍可手写运行时 API。
- **Go 程序员易踩的坑**：CI 没库又开了 `query!`，构建直接挂——准备 offline 或改运行时查询。

**记忆点：**
- 固定 SQL → `query!`；动态/脚本 → 运行时。
- 宏不是魔法：背后要 schema 元数据。

---

## Q5. 行怎么映射到 struct？ {#q5}
**Tags:** `hot` `FromRow` `query_as` `mapping`
**适用版本:** sqlx 0.7+/0.8.x

**一句话答案：**
给 struct 派 `sqlx::FromRow`，用 `query_as::<_, T>` 或 `query_as!` 一次取出；列名默认蛇形对齐字段，可用属性改名。对标 Go 的 `Scan` 进结构体字段。

**解答：**

```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros"] }
```

```text
#[derive(Debug, sqlx::FromRow)]
struct User {
    id: i64,
    email: String,
}

let user = sqlx::query_as::<_, User>("SELECT id, email FROM users WHERE id = $1")
    .bind(id)
    .fetch_optional(&pool)
    .await?;
```

列名不一致时：

```text
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    #[sqlx(rename = "email_address")]
    email: String,
}
```

只要一列时可用 `query_scalar`；只要「有没有行」用 `fetch_optional` 得到 `Option<T>`。

序列化到 JSON 再出 API 时，同一 struct 可再派 serde——见 [36-serde-and-serialization](../36-serde-and-serialization/)。

**Go 对比：**

```go
var u User
err := db.QueryRow(`SELECT id, email FROM users WHERE id=$1`, id).
    Scan(&u.ID, &u.Email)
```

- **Go 怎么做**：按位置 `Scan` 进变量；或用扫描辅助库。
- **Rust 为什么不同**：`FromRow` 把列→字段变成类型驱动，少写一长串 `&mut`。
- **Go 程序员易踩的坑**：字段顺序/可空性（`Option<T>` ↔ NULL）没对齐就 `decode` 失败。

**记忆点：**
- `FromRow` + `query_as` = 结构化取行。
- NULL 列用 `Option<T>`。

---

## Q6. 事务怎么写？ {#q6}
**Tags:** `hot` `transaction` `commit` `rollback`
**适用版本:** sqlx 0.7+/0.8.x（其它 crate 有各自 Tx API）

**一句话答案：**
`pool.begin().await?` 拿到事务，在其上 `execute`/`fetch`，成功 `commit`，失败丢弃（或 `rollback`）。对标 Go 的 `db.Begin()` + `tx.Commit()`。

**解答：**

```text
let mut tx = pool.begin().await?;

sqlx::query("UPDATE accounts SET balance = balance - $1 WHERE id = $2")
    .bind(amount)
    .bind(from_id)
    .execute(&mut *tx)
    .await?;

sqlx::query("UPDATE accounts SET balance = balance + $1 WHERE id = $2")
    .bind(amount)
    .bind(to_id)
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
```

错误路径：`?` 传播时 `tx` 被 drop，连接归还且未提交 → 回滚。也可显式：

```text
if let Err(e) = do_work(&mut tx).await {
    tx.rollback().await.ok();
    return Err(e);
}
tx.commit().await?;
```

注意：事务对象要互斥使用；不要把同一个 `Tx` 并发 `.await` 两处。

**Go 对比：**

```go
tx, err := db.Begin()
if err != nil { /* ... */ }
defer tx.Rollback() // Commit 成功后 Rollback 成 no-op 的惯用法因版本而异，需按文档写

_, err = tx.Exec(`UPDATE ...`)
if err != nil { return err }
return tx.Commit()
```

- **Go 怎么做**：`Begin` / `Commit` / `Rollback`；常 `defer Rollback`。
- **Rust 为什么不同**：所有权 + `Drop` 帮你在未 commit 时回滚；但仍要自己设计错误传播。
- **Go 程序员易踩的坑**：在 async 里把 `&mut tx` 跨 await 乱用，或 commit 前就结束作用域。

**记忆点：**
- `begin` → 干活 → `commit`；否则 drop = 回滚。
- 事务内查询也绑在 `tx` 上，不要绑回 `pool`。

---

## Q7. 连接池怎么对标 Go 的 `sql.DB`？ {#q7}
**Tags:** `hot` `pool` `PgPool` `sql.DB`
**适用版本:** sqlx 0.7+/0.8.x

**一句话答案：**
sqlx 的 **`Pool`**（如 `PgPool`）≈ Go 的 **`sql.DB`**：都是带池的句柄，`Clone` 共享，不是「一条连接」。用 `PoolOptions` 设最大连接、超时；不要为每个请求 `connect` 一次。

**解答：**

```text
use sqlx::postgres::PgPoolOptions;
use std::time::Duration;

let pool = PgPoolOptions::new()
    .max_connections(10)
    .acquire_timeout(Duration::from_secs(3))
    .connect(&std::env::var("DATABASE_URL")?)
    .await?;

// Clone 很便宜：内部 Arc
let pool2 = pool.clone();
```

对照表：

| Go `sql.DB` | sqlx |
|-------------|------|
| `Open` + 懒连接 | `PoolOptions::connect` |
| `SetMaxOpenConns` | `max_connections` |
| `SetConnMaxLifetime` | 空闲/寿命相关选项（见文档） |
| 到处传 `*sql.DB` | 到处 `Clone` `Pool` |
| `Ping` | `pool.acquire` / `SELECT 1` |

```text
// 健康检查示意
sqlx::query("SELECT 1").execute(&pool).await?;
```

**Go 对比：**

```go
db.SetMaxOpenConns(10)
db.SetConnMaxLifetime(time.Hour)
err := db.PingContext(ctx)
```

- **Go 怎么做**：`sql.DB` 本身就是池；长期持有、全局或注入。
- **Rust 为什么不同**：池类型按驱动区分（`PgPool`/`MySqlPool`/`SqlitePool`），但用法同一心智。
- **Go 程序员易踩的坑**：每个 handler `connect` 新池；或把 `max_connections` 开到比 DB `max_connections` 还大。

**记忆点：**
- `Pool` ≈ `sql.DB`；`Clone` 共享。
- 启动建一次池，请求里只用引用/克隆。

---

## Q8. 迁移（migration）怎么做？ {#q8}
**Tags:** `common` `migration` `schema`
**适用版本:** 工具选型；sqlx-cli / diesel_cli / 手写 SQL 均可

**一句话答案：**
用版本化 SQL（或 ORM 迁移工具）管理 schema：本地/CI 跑 migrate，应用启动可选择自动 migrate 或只读校验。对标 golang-migrate / goose。

**解答：**
常见三路：

| 工具 | 特点 |
|------|------|
| **sqlx-cli** | `sqlx migrate add/run`，与 sqlx 搭配自然 |
| **diesel_cli** | 与 diesel schema 生成一体 |
| 独立 migrate 二进制 | 多语言团队统一跑同一套 SQL |

```text
# 示意：安装与运行（shell，非 Rust）
cargo install sqlx-cli --no-default-features --features postgres
sqlx migrate add create_users
# 编辑 migrations/....sql 后：
sqlx migrate run
```

迁移文件示意：

```text
-- migrations/20260101000000_create_users.sql
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
);
```

应用内可选（示意）：

```text
sqlx::migrate!("./migrations")
    .run(&pool)
    .await?;
```

生产建议：迁移与应用发布解耦（Job/Init Container），避免多副本同时 migrate 无锁策略。

**Go 对比：**
- **Go 怎么做**：golang-migrate、goose、pressly/goose、或 ORM AutoMigrate（慎用生产）。
- **Rust 为什么不同**：同样「SQL 文件 + 版本表」；没有唯一官方工具。
- **Go 程序员易踩的坑**：在每个实例启动时无条件 AutoMigrate，造成竞态。

**记忆点：**
- schema 进 `migrations/`，不靠口头改表。
- 生产迁移要串行、可回滚策略要事先想清。

---

## Q9. async 里为什么不能阻塞跑同步 DB？ {#q9}
**Tags:** `common` `async` `blocking` `runtime`
**适用版本:** Tokio 等异步运行时；见 [31-async-programming](../31-async-programming/)

**一句话答案：**
异步运行时的工作线程在等 `.await`；若在其上调用 **同步阻塞** 的 DB API（如部分 diesel 用法），会卡住整条 worker，拖死其它任务。要么用 async 驱动（sqlx/SeaORM），要么把阻塞调用丢进 `spawn_blocking`。

**解答：**
错误心智（示意，不要照做）：

```text
// ❌ 在 async fn 里直接阻塞（示意）
async fn bad(pool: &SyncPool) {
    let _ = pool.get(); // 同步捞连接 + 同步查询……卡住 runtime
}
```

正确方向 A——全程 async：

```text
async fn good(pool: &sqlx::PgPool) -> Result<(), sqlx::Error> {
    sqlx::query("SELECT 1").execute(pool).await?;
    Ok(())
}
```

正确方向 B——必须调用同步库时：

```text
async fn call_sync_db() -> Result<(), tokio::task::JoinError> {
    tokio::task::spawn_blocking(|| {
        // 同步 diesel / 其它阻塞客户端
        // do_sync_query();
    })
    .await?;
    Ok(())
}
```

| 场景 | 做法 |
|------|------|
| 新项目 async 服务 | sqlx / SeaORM |
| 遗留同步 ORM | `spawn_blocking` 隔离 |
| 纯同步 CLI | 同步客户端即可，不必强行 async |

**Go 对比：**
- **Go 怎么做**：goroutine 里阻塞 `database/sql` 是常态；runtime 用更多线程调度。
- **Rust 为什么不同**：Tokio 默认工人线程少，**阻塞 ≠ 可接受**；要显式隔离。
- **Go 程序员易踩的坑**：把「在 goroutine 里随便阻塞」的习惯搬进 `async fn`。

**记忆点：**
- async 路径用 async 驱动。
- 同步 DB → `spawn_blocking`，别冻住 runtime。

---

## Q10. 怎么防 SQL 注入？ {#q10}
**Tags:** `hot` `security` `injection` `bind`
**适用版本:** 所有通过占位符绑参的客户端

**一句话答案：**
永远用 **绑定参数**（`$1` / `?`）传用户输入；禁止把字符串拼进 SQL。预编译/参数化对标 Go 的 `?`/`$1` + `Exec` 参数。

**解答：**

```text
// ✅ 参数绑定
sqlx::query("SELECT * FROM users WHERE email = $1")
    .bind(&email)
    .fetch_optional(&pool)
    .await?;
```

```text
// ❌ 字符串拼接（注入温床）
let sql = format!("SELECT * FROM users WHERE email = '{email}'");
sqlx::query(&sql).fetch_optional(&pool).await?;
```

动态 **IN 列表** 也不要手拼未转义内容：用官方宏/按占位符生成，或先校验为合法 ID 集合再绑参。表名/列名不能绑定的，必须用允许列表（allowlist），不能信客户端字符串。

```rust
// 标准库侧：先校验「只含安全字符」再用于标识符（示意策略）
fn safe_ident(s: &str) -> bool {
    !s.is_empty() && s.chars().all(|c| c.is_ascii_alphanumeric() || c == '_')
}

fn main() {
    assert!(safe_ident("users"));
    assert!(!safe_ident("users;drop"));
}
```

**Go 对比：**

```go
// 对
db.Query(`SELECT * FROM users WHERE email=$1`, email)
// 错
db.Query(`SELECT * FROM users WHERE email='` + email + `'`)
```

- **Go 怎么做**：同样靠占位符；拼接即风险。
- **Rust 为什么不同**：原则完全一致；sqlx 宏也不会把「绑参」变成「可拼表名」。
- **Go 程序员易踩的坑**：以为「Rust 类型安全」等于「SQL 自动安全」——类型不管你有没有 `format!` SQL。

**记忆点：**
- 值 → bind；标识符 → allowlist。
- 类型安全 ≠ 注入免疫。

---

## Q11. 测试库怎么搞？ {#q11}
**Tags:** `common` `testing` `testcontainers` `sqlite`
**适用版本:** 测试策略；见 [24-testing](../24-testing/)

**一句话答案：**
单测可用 **SQLite 内存库** 或 mock；集成测用真实引擎（Docker / testcontainers / CI 服务）。每个测试隔离事务或独立 schema，避免共享脏数据。

**解答：**
轻量：SQLite（注意与 Postgres 方言差异）：

```toml
[dev-dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```text
#[tokio::test]
async fn inserts_user() -> Result<(), sqlx::Error> {
    let pool = sqlx::sqlite::SqlitePoolOptions::new()
        .connect("sqlite::memory:")
        .await?;
    sqlx::query("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")
        .execute(&pool)
        .await?;
    sqlx::query("INSERT INTO users (email) VALUES (?1)")
        .bind("a@b.c")
        .execute(&pool)
        .await?;
    Ok(())
}
```

更贴近生产：

| 策略 | 何时 |
|------|------|
| `sqlite::memory:` | 逻辑快测、方言可接受 |
| Docker Compose / CI service | 集成测 Postgres/MySQL |
| testcontainers | 测试代码里拉容器 |
| 事务回滚夹具 | 每个用例结束撤数据 |

测试组织（单元/集成目录）见 [24-testing](../24-testing/)；运行 `cargo test` 见 [04-running](../04-running/)。

**Go 对比：**
- **Go 怎么做**：`testing` + dockertest / testcontainers-go / SQLite。
- **Rust 为什么不同**：工具名不同，隔离原则相同。
- **Go 程序员易踩的坑**：所有包共享一个长期库却不清理，测试顺序一变就红。

**记忆点：**
- 快测可 SQLite；合同测要对齐真实引擎。
- 隔离数据比「能跑通」更重要。

---

## Q12. 和 Go `database/sql` 总对照表？ {#q12}
**Tags:** `common` `cheatsheet` `database/sql`
**适用版本:** 心智对照；实现以所选 crate 为准

**一句话答案：**
把 Go 的 `database/sql` 心智映射到 **sqlx `Pool` + query/bind + Tx**；ORM 另选 SeaORM/diesel。没有 std 替代品，但 API 角色一一可对上。

**解答：**

| Go | Rust（sqlx 为主） |
|----|-------------------|
| `database/sql` | 无 std；用 sqlx（或其它） |
| `sql.Open` | `PoolOptions::connect` |
| `*sql.DB` | `Pool`（可 `Clone`） |
| `Query` / `QueryRow` / `Exec` | `query` / `query_as` / `execute` |
| `Scan` | `FromRow` / `get` / `query_scalar` |
| `Begin` / `Tx` | `pool.begin` / `Transaction` |
| `Prepare` | 驱动侧预处理；优先 bind，勿拼接 |
| 驱动 blank import | Cargo **features** 选 postgres/mysql/sqlite |
| GORM 等 | SeaORM / diesel |
| sqlc | sqlx `query!` / 其它 codegen |
| goose / migrate | sqlx migrate / diesel_cli / 独立工具 |

最小「Go 用户落地清单」：

```text
1. cargo add sqlx --features runtime-tokio,postgres,macros
2. 设置 DATABASE_URL
3. 建 Pool，注入到 axum State / 手写上下文
4. 查询全部 .bind，禁止 format! SQL
5. 迁移进仓库，CI 跑 migrate + test
```

```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

**Go 对比：**
- **Go 怎么做**：stdlib 统一接口，驱动可插拔。
- **Rust 为什么不同**：接口在社区 crate；换驱动常换类型/feature，而不是换 `driver.Driver` 注册。
- **Go 程序员易踩的坑**：死等「官方 database/sql」，耽误选型；或混用同步 ORM 与 async Web 不隔离。

**记忆点：**
- `Pool` = `sql.DB`；bind = 防注入；migrate = schema 真相。
- 先 sqlx，再按需上 ORM。

---

## Q13. SQL NULL 怎么映射到 Rust `Option`？ {#q13}
**Tags:** `common` `NULL` `Option` `FromRow`
**适用版本:** sqlx 0.7+/0.8.x（其它 crate 同思路：可空 → `Option`）

**一句话答案：**
列声明可空（SQL **NULL**）→ Rust 字段用 **`Option<T>`**；`NOT NULL` → 直接 `T`。解码时 NULL 变 `None`，有值变 `Some`；别用「零值」假装空，也别对可空列写非 `Option` 然后指望静默成功。

**解答：**
和 [Q5](#q5) 的 `FromRow` 同一套：

```toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres"] }
```

```text
#[derive(Debug, sqlx::FromRow)]
struct User {
    id: i64,                 // NOT NULL
    email: String,           // NOT NULL
    nickname: Option<String>, // NULL 允许
}

// nickname 为 NULL 的行 → nickname == None
let u = sqlx::query_as::<_, User>("SELECT id, email, nickname FROM users WHERE id = $1")
    .bind(id)
    .fetch_one(&pool)
    .await?;
```

写入时同样用 `Option`：

```text
sqlx::query("INSERT INTO users (email, nickname) VALUES ($1, $2)")
    .bind(&email)
    .bind(nickname.as_deref()) // Option<&str>；None → SQL NULL
    .execute(&pool)
    .await?;
```

三层别混：

| 概念 | 含义 |
|------|------|
| 行不存在 | `fetch_optional` → `Option<User>` 外层是 `None` |
| 行在、列 NULL | `User { nickname: None, ... }` |
| 空字符串 `''` | 仍是 `Some("")`，不是 NULL |

`query!` 宏也会按 schema 空性生成 `Option`；手写 struct 时空性必须与表一致，否则 decode 报错。

**Go 对比：**
```go
var nick sql.NullString
err := row.Scan(&id, &email, &nick)
// 或 *string / pgtype
```
- **Go 怎么做**：`sql.Null*`、指针或驱动专用可空类型。
- **Rust 为什么不同**：`Option<T>` 就是惯用可空表示，和所有权/模式匹配一条路。
- **Go 程序员易踩的坑**：字段写成 `String` 却查可空列——运行时解码失败，而不是得到 `""`。

**记忆点：**
- 可空列 → `Option<T>`；非空 → `T`。
- 「没这行」和「列是 NULL」是两层 `Option` 语义。

---

## Q14. 批量插入 / 多行执行常见写法？（text 示意 sqlx） {#q14}
**Tags:** `common` `batch` `insert` `QueryBuilder`
**适用版本:** sqlx 0.7+/0.8.x（示意；方言按 postgres/mysql/sqlite 调整）

**一句话答案：**
小批量可以循环 `execute`；更常见是**一条多值 `INSERT`** 或 sqlx **`QueryBuilder`** 拼 bind；超大批量再考虑 Postgres `COPY` / 驱动批量 API。始终 `.bind`，禁止 `format!` 拼值（见 [Q10](#q10)）。

**解答：**
循环（简单，往返多）：

```text
for email in emails {
    sqlx::query("INSERT INTO users (email) VALUES ($1)")
        .bind(email)
        .execute(&pool)
        .await?;
}
```

多值插入（示意固定两行；动态行数用 QueryBuilder）：

```text
sqlx::query(
    "INSERT INTO users (email) VALUES ($1), ($2), ($3)",
)
.bind(&emails[0])
.bind(&emails[1])
.bind(&emails[2])
.execute(&pool)
.await?;
```

动态行数用 `QueryBuilder`（text 示意）：

```text
use sqlx::QueryBuilder;

let mut qb = QueryBuilder::new("INSERT INTO users (email) ");
qb.push_values(emails.iter(), |mut b, email| {
    b.push_bind(email);
});
let query = qb.build();
query.execute(&pool).await?;
```

事务里批量（要么全进要么全撤，见 [Q6](#q6)）：

```text
let mut tx = pool.begin().await?;
for email in emails {
    sqlx::query("INSERT INTO users (email) VALUES ($1)")
        .bind(email)
        .execute(&mut *tx)
        .await?;
}
tx.commit().await?;
```

选型直觉：几十行 → 多值/`QueryBuilder`；成千上万行 → 看引擎的 COPY/load；需要原子性 → 包事务。ORM（SeaORM/diesel）各有 `insert_many`，语义类似，API 不同。

**Go 对比：**
- **Go 怎么做**：循环 `Exec`、多值 SQL、或 `CopyIn` / bulk API。
- **Rust 为什么不同**：sqlx 把「安全拼多行」收成 `QueryBuilder` + bind。
- **Go 程序员易踩的坑**：用字符串拼接邮箱列表——注入与转义灾难。

**记忆点：**
- 批量优先多值 / `QueryBuilder`，别傻循环除非行数极小。
- 值全部 bind；大体积再上 COPY 类工具。

---

## Q15. 连接池参数怎么调？（max / acquire / 与 PG 上限） {#q15}
**Tags:** `hot` `pool` `max_connections` `tuning`
**适用版本:** sqlx PoolOptions 一类；其它池同思路

**一句话答案：**
池的 **`max_connections`** 必须小于数据库 `max_connections`，并给管理会话/其它服务留余量；再设 **`acquire_timeout`**、空闲回收，避免请求无限等连接。多副本时用「每实例上限 × 副本数」算总连接。

**解答：**
```text
# 示意（sqlx）
# PgPoolOptions::new()
#   .max_connections(20)
#   .acquire_timeout(Duration::from_secs(3))
#   .idle_timeout(Some(Duration::from_secs(600)))
#   .connect(&url).await?
```

```text
总连接预算例子：
PG max_connections = 100
留 20 给超管/分析/迁移
可分配 80 → 4 个服务副本 × 每池 20
```

```rust
fn main() {
    let pg_max = 100u32;
    let reserve = 20u32;
    let replicas = 4u32;
    let per_pool = (pg_max - reserve) / replicas;
    assert_eq!(per_pool, 20);
}
```

「❌ 错误写法」——每个实例 `max_connections = 100`，K8s 扩到 10 副本：数据库直接拒连。

异步里还要避免「持有连接过久不做查询」。慢 SQL 先优化或加语句超时，而不是只靠加大池。

**Go 对比：**
```go
db.SetMaxOpenConns(20)
db.SetConnMaxLifetime(time.Minute)
```
- **Go 怎么做**：`sql.DB` 池参数。
- **Rust 为什么不同**：名字在 PoolOptions，公式相同。
- **Go 程序员易踩的坑**：按「机器核数」设池却忽略 DB 全局上限。

**记忆点：**
- 先算全局连接预算，再设每进程池。
- `acquire_timeout` 防止无限排队。
