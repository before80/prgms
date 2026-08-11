+++
title = "48-缓存与 Redis"
date = 2026-07-28T14:49:00+08:00
weight = 480
type = "docs"
description = "面向 Go 用户讲清进程内缓存、Redis 连接、TTL 穿透击穿、序列化锁与二级缓存"
isCJKLanguage = true
draft = false

+++

# 缓存与 Redis (Caching and Redis)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否想知道：进程内缓存用 **moka** / **cached** / `HashMap`+`Mutex` 怎么选？
- 你是否疑惑：有了本地缓存，为什么服务还要上 **Redis**？
- 你是否分不清 **redis-rs** 与 **deadpool-redis**、GET/SET/TTL 最小怎么写？
- 你是否怕缓存穿透 / 击穿 / 雪崩，或把分布式锁、pub/sub 用错场景？
- 你是否在 async 里阻塞 Redis、或不知本地 + Redis 二级缓存怎么分层、何时不该上 Redis？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| cache | — | 缓存 | 用空间换时间的临时数据副本 | 同概念 |
| **moka** | — | 进程内缓存 crate | 并发安全、带过期/容量的本地缓存 | Ristretto / bigcache 一类 |
| **cached** | — | 函数结果缓存宏 | 用宏给函数结果做 memoize | 手写 sync.Map / 第三方 memo |
| Redis | Remote Dictionary Server | 远程字典服务 | 常见内存 KV，可共享、可持久化 | 同名 |
| **redis-rs** | — | Redis 客户端 | 连接与命令 API；有 sync/async | go-redis / redigo |
| **deadpool-redis** | — | Redis 连接池 | 在 redis-rs 上做异步连接池 | go-redis 自带池 |
| TTL | Time To Live | 存活时间 | 键过期时间 | `EXPIRE` / `Set` 的 expiration |
| 穿透 | cache penetration | 缓存穿透 | 查不存在的 key，打穿到 DB | 同概念 |
| 击穿 | cache breakdown | 缓存击穿 | 热点 key 过期瞬间打穿 | 同概念 |
| 雪崩 | cache avalanche | 缓存雪崩 | 大量 key 同时过期 | 同概念 |
| NX / PX | Not eXists / milliseconds | 不存在才设 / 毫秒过期 | 分布式锁常用选项 | `SetNX` + 过期 |
| pub/sub | publish/subscribe | 发布订阅 | 消息扇出，不保证可靠投递 | Redis Pub/Sub |
| MessagePack | — | 二进制序列化格式 | 比 JSON 更紧凑的结构编码 | msgpack 库 |
| serde | SERialize/DEserialize | 序列化框架 | 类型 ↔ JSON/MessagePack 等；见 [36-serde](../36-serde-and-serialization/) | `encoding/json` |
| async | asynchronous | 异步 | Future/`.await` 做 I/O；见 [31-async](../31-async-programming/) | goroutine + 客户端 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q10](#q10) |
| `common` | [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q11](#q11), [Q12](#q12) |
| `occasional` | [Q8](#q8) |
| `advanced` | — |

---

## Q1. 进程内缓存用什么？（moka / cached / HashMap+Mutex） {#q1}
**Tags:** `hot` `beginner` `moka` `cached` `HashMap`
**适用版本:** 选型原则；crate 版本以 crates.io 为准

**一句话答案：**
要「并发安全 + TTL/容量淘汰」→ **moka**；要「给纯函数结果 memoize」→ **cached**；只要极简、自己控锁与过期 → `HashMap` + `Mutex`/`RwLock`。多数服务读多写少、要过期策略，优先 moka。

**解答：**
怎么选：

| 需求 | 倾向 | 不太合适 |
|------|------|----------|
| 多线程/多 task 共享、带 TTL、LRU/LFU | **moka** | 手写淘汰易错 |
| 给 `fn(input) -> output` 包一层缓存 | **cached** | 复杂对象图、跨进程共享 |
| 教学/极小工具、策略自己定 | `HashMap` + 锁 | 生产热点、要精细淘汰 |

`HashMap` + 锁最小心智（仅 std）：

```rust
use std::collections::HashMap;
use std::sync::Mutex;

fn main() {
    let cache = Mutex::new(HashMap::<String, i32>::new());
    {
        let mut g = cache.lock().unwrap();
        g.insert("answer".into(), 42);
    }
    let v = cache.lock().unwrap().get("answer").copied();
    println!("{v:?}");
}
```

moka 依赖与用法示意：

```toml
[dependencies]
moka = { version = "0.12", features = ["sync"] }
```

```text
// 示意：需 moka；勿当可独立 rustc 的片段
use moka::sync::Cache;
use std::time::Duration;

let cache = Cache::builder()
    .max_capacity(10_000)
    .time_to_live(Duration::from_secs(60))
    .build();
cache.insert("k".to_string(), 1);
assert_eq!(cache.get(&"k".to_string()), Some(1));
```

cached 宏示意：

```toml
[dependencies]
cached = "0.54"
```

```text
// 示意：cached::proc_macro::cached
use cached::proc_macro::cached;

#[cached(size = 100)]
fn fib(n: u64) -> u64 {
    if n < 2 { n } else { fib(n - 1) + fib(n - 2) }
}
```

**Go 对比：**
- **Go 怎么做**：`sync.Map`、自研 map+mutex，或 Ristretto / groupcache 等。
- **Rust 为什么不同**：std 只有容器+锁；带过期/容量的生产级缓存在 crates.io。
- **Go 程序员易踩的坑**：以为 `HashMap` 默认线程安全——必须外加 `Mutex`/`RwLock`，或用 moka。

**记忆点：**
- 生产本地缓存默认想 **moka**。
- memoize 函数 → **cached**；极简 → `HashMap`+锁。

---

## Q2. 为什么很多服务还要 Redis？ {#q2}
**Tags:** `hot` `beginner` `Redis` `why`
**适用版本:** 架构层面；与具体 Rust 版本无关

**一句话答案：**
进程内缓存只服务**本进程**：多副本不共享、进程重启就没、也难做跨服务协调。**Redis** 提供共享内存 KV、TTL、原子命令、可选持久化——适合会话、限流、分布式锁、跨实例热点数据。

**解答：**
本地缓存 vs Redis：

```text
本地（moka / HashMap）
  ✓ 延迟极低（无网络）
  ✗ 每实例一份，易不一致
  ✗ 扩容/重启丢缓存
  ✗ 难做跨服务协调

Redis
  ✓ 多实例共享同一份视图
  ✓ TTL / 原子 INCR / SET NX 等
  ✓ 可 RDB/AOF 持久化（按配置）
  ✗ 多一跳网络与运维面
```

典型仍上 Redis 的理由：
1. **水平扩展**：K8s 里 N 个 Pod，本地缓存各自为政。
2. **共享状态**：登录会话、购物车、短期 token 黑名单。
3. **协调原语**：分布式锁、限流计数、简易队列/延迟任务（按场景选型）。
4. **容量**：热点太大，不想塞进每个 JVM/进程堆。

「❌ 错误预期」——「有 moka 就永远不需要 Redis」：单机够用时可以；一上多副本，本地缓存立刻变成「各自真相」。

**Go 对比：**
- **Go 怎么做**：同样本地 cache + go-redis；理由几乎一样。
- **Rust 为什么不同**：语言无关——是部署拓扑问题，不是 Rust 特有。
- **Go 程序员易踩的坑**：把 Redis 当「更快的数据库」乱存权威数据——权威仍应在 DB，Redis 是加速与协调层。

**记忆点：**
- 本地 = 快但不共享；Redis = 共享与协调。
- 多副本几乎总会碰到「要不要共享缓存」的问题。

---

## Q3. redis-rs / deadpool-redis 怎么选连接？ {#q3}
**Tags:** `hot` `redis-rs` `deadpool-redis` `pool`
**适用版本:** 选型原则；API 以各 crate 文档为准

**一句话答案：**
直接用 **redis-rs** 的 `Client`/`Connection`（或 async `ConnectionManager`）适合简单脚本、低频；长期运行的 async 服务要**连接池**时，常用 **deadpool-redis**（或生态里等价池）包一层，避免每次命令新建 TCP、也避免单连接打满。

**解答：**
角色对照：

| 组件 | 管什么 |
|------|--------|
| redis-rs `Client` | 地址、建连、发命令 |
| redis-rs 单连接 / Multiplexed | 一条或复用连接上的命令流 |
| **deadpool-redis** | 从池里借还连接，限制并发连接数 |

依赖示意：

```toml
[dependencies]
redis = { version = "0.27", features = ["tokio-comp"] }
deadpool-redis = "0.18"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

建 Client（示意）：

```text
// 示意：需 redis crate + 可达的 Redis
use redis::Client;

let client = Client::open("redis://127.0.0.1/")?;
// sync: let mut con = client.get_connection()?;
// async: 用 aio / ConnectionManager / 或走 deadpool
```

deadpool 配置直觉：

```text
// 示意：deadpool_redis::Config
let cfg = deadpool_redis::Config::from_url("redis://127.0.0.1/");
let pool = cfg.create_pool(Some(deadpool_redis::Runtime::Tokio1))?;
let mut conn = pool.get().await?;
// 然后用 redis::cmd / AsyncCommands 发命令
```

怎么选：CLI/一次性任务 → 直接 redis-rs；Web/API 多并发 → 池（deadpool-redis 很常见）。

**Go 对比：**
```go
rdb := redis.NewClient(&redis.Options{
    Addr:     "127.0.0.1:6379",
    PoolSize: 10,
})
```
- **Go 怎么做**：go-redis 的 `Client` **自带连接池**。
- **Rust 为什么不同**：redis-rs 偏「客户端原语」；池常另选 deadpool 等。
- **Go 程序员易踩的坑**：以为 `Client::open` 就等于 go-redis 那个带池的 Client——高并发下要显式考虑池。

**记忆点：**
- 简单用 redis-rs；服务高并发加 **deadpool-redis**。
- 对标 go-redis：池在 Go 里「默认有」，Rust 里「常要加」。

---

## Q4. GET/SET/过期 TTL 最小写法 {#q4}
**Tags:** `hot` `GET` `SET` `TTL` `EXPIRE`
**适用版本:** redis-rs 命令层；以当前 redis crate 文档为准

**一句话答案：**
连上后：`SET key value`、`GET key`、设过期用 `SET` 带 `EX`/`PX` 或 `EXPIRE`/`SET_EX`。Rust 侧用 `redis::Commands` / `AsyncCommands` 或 `cmd("SET")` 拼参数。

**解答：**
命令层直觉（与 redis-cli 同语义）：

```text
SET session:1 alice EX 3600
GET session:1
TTL session:1
```

async 最小示意：

```toml
[dependencies]
redis = { version = "0.27", features = ["tokio-comp"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```text
// 示意：需本机 Redis；AsyncCommands
use redis::AsyncCommands;

#[tokio::main]
async fn main() -> redis::RedisResult<()> {
    let client = redis::Client::open("redis://127.0.0.1/")?;
    let mut con = client.get_multiplexed_async_connection().await?;

    con.set_ex("session:1", "alice", 3600u64).await?;
    let v: Option<String> = con.get("session:1").await?;
    let ttl: i64 = redis::cmd("TTL").arg("session:1").query_async(&mut con).await?;
    println!("value={v:?} ttl={ttl}");
    Ok(())
}
```

「❌ 错误写法」——只 `SET` 不设过期，又当「短期缓存」：键会常驻，内存与脏数据风险上升。缓存键默认想好 TTL。

**Go 对比：**
```go
rdb.Set(ctx, "session:1", "alice", time.Hour)
val, err := rdb.Get(ctx, "session:1").Result()
```
- **Go 怎么做**：`Set` 第四参直接带 `time.Duration`。
- **Rust 为什么不同**：方法名是 `set_ex` / `set` + 过期参数，或显式 `EXPIRE`；语义对齐 Redis 协议。
- **Go 程序员易踩的坑**：忘处理 `nil`（Rust 侧常用 `Option<T>` 表示键不存在）。

**记忆点：**
- `set_ex` / `EX` = 写入即带 TTL。
- `GET` 不存在 → 当 `None`，不是空字符串幻觉。

---

## Q5. 缓存穿透 / 击穿 / 雪崩直觉与常见缓解 {#q5}
**Tags:** `hot` `penetration` `breakdown` `avalanche`
**适用版本:** 架构模式；语言无关

**一句话答案：**
**穿透**：查根本不存在的数据，缓存与 DB 都没有 → 打穿 DB。**击穿**：单个热点 key 过期瞬间，并发打穿。**雪崩**：大批 key 同时过期，流量洪峰打穿。缓解分别靠：空值/布隆过滤、互斥重建或逻辑过期、TTL 加抖动与多级降级。

**解答：**
一眼对照：

| 现象 | 特征 | 常见缓解 |
|------|------|----------|
| 穿透 | 恶意/乱 ID，永远 miss | 缓存空值短 TTL；布隆过滤器挡非法 ID；参数校验 |
| 击穿 | 一个热 key 过期 | 互斥锁只让一个去加载；逻辑过期+异步刷新 |
| 雪崩 | 大量 key 同时过期 | TTL = 基准 + 随机抖动；多级缓存；DB 限流/熔断 |

TTL 抖动直觉：

```text
ttl = base_secs + random(0..=jitter_secs)
// 避免整点全部一起过期
```

空值缓存直觉（防穿透）：

```text
// 查 DB 无行时也写入短 TTL 占位，避免反复打 DB
SET user:999 "__nil__" EX 60
```

击穿时「单飞」加载（逻辑示意）：

```text
if let Some(v) = cache.get(key) { return v; }
// 抢锁成功者：查 DB → 写缓存 → 放锁
// 失败者：短暂等待再读缓存，或降级
```

**Go 对比：**
- **Go 怎么做**：同样三套概念；singleflight 常用来防击穿。
- **Rust 为什么不同**：可用 `tokio` 互斥 / 自研 singleflight；模式相同。
- **Go 程序员易踩的坑**：只背名词不设 TTL 抖动——雪崩仍会发生。

**记忆点：**
- 穿透=查幽灵；击穿=热点过期；雪崩=集体过期。
- 空值、单飞、TTL 抖动是三板斧。

---

## Q6. 序列化 value：字符串 vs serde JSON vs MessagePack {#q6}
**Tags:** `common` `serde` `JSON` `MessagePack`
**适用版本:** 与 [36-serde](../36-serde-and-serialization/) 一致；格式选型

**一句话答案：**
纯字符串/整数直接存；结构化对象用 **serde** 编成 **JSON**（可读、易调试）或 **MessagePack**（更紧凑）。Redis 存的是字节，格式是你的约定——团队统一一种即可。

**解答：**
怎么选：

| 形态 | 何时 |
|------|------|
| 纯字符串 / 数字 | 会话 ID、计数、开关 |
| JSON（serde_json） | 要可读、跨语言、运维可 `GET` 肉眼看 |
| MessagePack（rmp-serde 等） | 体积敏感、同构服务间、少人手拆 |

JSON 路径示意：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
redis = { version = "0.27", features = ["tokio-comp"] }
```

```text
// 示意：先 serialize 再 SET；GET 再 deserialize
#[derive(serde::Serialize, serde::Deserialize)]
struct UserView { id: u64, name: String }

let json = serde_json::to_string(&user)?;
con.set_ex(format!("user:{}", user.id), json, 300u64).await?;
let raw: String = con.get(key).await?;
let user: UserView = serde_json::from_str(&raw)?;
```

MessagePack 同理：`rmp_serde::to_vec` / `from_slice`，Redis 侧用 `Vec<u8>` 存取。

「❌ 错误写法」——同一 key 有时写 JSON 有时写 MessagePack，或字段随意改名不版本化：反序列化全线爆炸。

**Go 对比：**
```go
b, _ := json.Marshal(user)
rdb.Set(ctx, key, b, time.Minute)
```
- **Go 怎么做**：`encoding/json` 或 msgpack 库，再 `Set` bytes。
- **Rust 为什么不同**：统一走 **serde** 生态选格式后端。
- **Go 程序员易踩的坑**：在 Redis 里塞 `Debug` 打印字符串当序列化——只能调试，不能当契约。

**记忆点：**
- Redis = 字节桶；格式是你的协议。
- 调试友好 → JSON；体积 → MessagePack。

---

## Q7. 分布式锁（SET NX PX）要注意什么？ {#q7}
**Tags:** `common` `distributed-lock` `SET` `NX` `PX`
**适用版本:** Redis 锁模式；非 Redlock 全文展开

**一句话答案：**
用 `SET key token NX PX ttl`：不存在才设、带过期防死锁。必须用**随机 token** 标识持有者，释放时用「比对 token 再 DEL」的脚本，避免误删别人的锁；业务必须能在 TTL 内完成或实现续期，锁不是事务。

**解答：**
最小正确姿势：

```text
SET lock:order:42 <random-token> NX PX 5000
# OK → 持有；nil → 未拿到

# 释放：仅当 value == token 时删除（Lua 原子）
# if redis.call("GET", KEYS[1]) == ARGV[1] then
#   return redis.call("DEL", KEYS[1])
# else return 0 end
```

Rust 侧示意：

```text
// 示意：SET NX PX
let token = uuid::Uuid::new_v4().to_string();
let ok: bool = redis::cmd("SET")
    .arg("lock:order:42")
    .arg(&token)
    .arg("NX")
    .arg("PX")
    .arg(5000)
    .query_async(&mut con)
    .await?;
```

注意清单：
1. **必有 TTL**：进程崩溃不能永久占锁。
2. **token 比对再删**：裸 `DEL` 会删掉后来者的锁。
3. **TTL vs 业务时长**：任务可能超过 TTL → 需续期（watchdog）或拆短任务。
4. **单 Redis 实例**的「够用锁」≠ 跨机房强一致；复杂场景看 Redlock/专用协调服务，别神化。

**Go 对比：**
```go
ok, err := rdb.SetNX(ctx, key, token, 5*time.Second).Result()
```
- **Go 怎么做**：`SetNX` + 过期；释放同样要用 token 校验。
- **Rust 为什么不同**：命令拼法不同，语义一致。
- **Go 程序员易踩的坑**：拿到锁就当「数据库事务」——锁只互斥，不保证 ACID。

**记忆点：**
- `SET NX PX` + 随机 token + 安全解锁。
- 锁会过期；业务要比 TTL 诚实。

---

## Q8. pub/sub 适合干什么、不适合干什么 {#q8}
**Tags:** `occasional` `pubsub` `Redis`
**适用版本:** Redis Pub/Sub 语义；与 Streams 区分

**一句话答案：**
适合**即时扇出通知**（配置热更新信号、缓存失效广播、在线状态提示）。不适合**必须可靠投递**的业务消息：订阅者离线会丢、无持久化积压（要可靠用 Streams/MQ）。

**解答：**

```text
适合
  ✓ 「告诉大家：某 key 失效了」
  ✓ 「配置版本变了，请重载」
  ✓ 在线人数、协作光标一类可丢提示

不适合
  ✗ 订单、支付、必须至少一次投递的任务
  ✗ 需要 ACK / 重试 / 死信
  ✗ 订阅者短暂断线还要补历史
```

心智：Pub/Sub ≈ 电台直播；Streams/Kafka ≈ 带回放的日志。

```text
PUBLISH cache:invalidate "user:42"
// 当时在线的订阅者收到；不在线的永远收不到这条
```

**Go 对比：**
- **Go 怎么做**：go-redis `Subscribe`；同样要认清「不可靠」。
- **Rust 为什么不同**：redis-rs 有 pubsub API；语义跟 Redis 绑定，与语言无关。
- **Go 程序员易踩的坑**：用 Pub/Sub 当任务队列——丢消息时无法追责。

**记忆点：**
- Pub/Sub = 可丢的广播信号。
- 要可靠 → Streams 或真正的消息队列。

---

## Q9. 和 Go go-redis 怎么对照 {#q9}
**Tags:** `common` `go-redis` `对照`
**适用版本:** 概念对照；API 版本各自演进

**一句话答案：**
go-redis 的 `Client` ≈ redis-rs `Client` +（常）自带池；命令都是 Redis 协议的薄封装。Rust 侧 async 要选 feature（`tokio-comp` 等），池常另接 **deadpool-redis**；类型上更爱 `RedisResult` + `Option`。

**解答：**
对照表：

| Go (go-redis) | Rust 常见 |
|---------------|-----------|
| `redis.NewClient(&Options{Addr, PoolSize})` | `Client::open` + deadpool 或 Multiplexed |
| `rdb.Get(ctx, k).Result()` | `con.get(k).await` → `RedisResult<T>` |
| `redis.Nil` | `Ok(None)` / 特定错误，看反序列化类型 |
| `rdb.Set(ctx, k, v, ttl)` | `set_ex` / `SET`+`EX` |
| `rdb.Publish` / `Subscribe` | `PUBLISH` / pubsub 连接 |
| context 取消 | `tokio` cancel / timeout 包装 Future |

```text
// Go: val, err := rdb.Get(ctx, "k").Result()
// Rust 示意:
let val: Option<String> = con.get("k").await?;
```

**Go 对比：**
- **Go 怎么做**：一个 Client 打通池、命令、钩子。
- **Rust 为什么不同**：客户端与池、runtime feature 拆得更开，组合更灵活也更要自己拼。
- **Go 程序员易踩的坑**：把 sync 连接塞进 tokio runtime 阻塞（见 [Q10](#q10)）。

**记忆点：**
- 命令语义对齐；池与 async 接线方式不同。
- `Nil` ↔ 用 `Option` 建模更顺手。

---

## Q10. async runtime 下别阻塞 Redis 调用 {#q10}
**Tags:** `hot` `async` `blocking` `tokio`
**适用版本:** 与 [31-async](../31-async-programming/) 一致

**一句话答案：**
在 **tokio** 等 async 运行时里，不要调用 redis-rs 的**同步** `get_connection` + 阻塞 `query`。应使用 `tokio-comp`（或对应 runtime feature）的 async API，或把同步调用丢进 `spawn_blocking`——否则会堵住 worker 线程，拖垮整个服务。

**解答：**
对错对照：

```text
❌  在 #[tokio::main] 里:
    let mut con = client.get_connection()?; // 同步阻塞
    let _: String = redis::cmd("GET").arg("k").query(&mut con)?;

✅  用 async 连接:
    let mut con = client.get_multiplexed_async_connection().await?;
    let _: String = redis::cmd("GET").arg("k").query_async(&mut con).await?;

✅  或（不得已用同步库时）:
    tokio::task::spawn_blocking(|| { /* sync redis */ }).await?
```

依赖必须开对 feature：

```toml
redis = { version = "0.27", features = ["tokio-comp"] }
```

「❌ 错误写法」——「反正 Go 里同步客户端 + 每请求一个 goroutine 也能跑」：Rust async 是协作式调度，一个阻塞调用可以卡住许多任务。

**Go 对比：**
- **Go 怎么做**：多数 go-redis 调用在 goroutine 里阻塞，靠 M:N 调度消化。
- **Rust 为什么不同**：async worker 默认假设 `.await` 点不长时间占线程。
- **Go 程序员易踩的坑**：把同步 Redis 客户端直接粘进 axum handler。

**记忆点：**
- async 路径用 `query_async` / AsyncCommands。
- 同步只能 `spawn_blocking`，不要直接堵 runtime。

---

## Q11. 本地缓存 + Redis 二级缓存怎么分层 {#q11}
**Tags:** `common` `two-level` `moka` `Redis`
**适用版本:** 架构模式

**一句话答案：**
读路径：**本地（L1）→ Redis（L2）→ DB**；写/更新时先改权威源，再删/更新 L2，并广播或短 TTL 让 L1 失效。L1 要小、TTL 短；L2 共享、TTL 稍长。

**解答：**
分层：

```text
请求
  → L1 moka（本进程，微秒级）
      miss → L2 Redis（共享，亚毫秒~毫秒）
          miss → DB
          → 回填 L2、L1
```

失效策略常见两种：
1. **Cache-aside**：读 miss 回填；写 DB 后 **DEL** 缓存（或短窗口双删）。
2. **失效广播**：写后 `PUBLISH invalidate`，各实例清 L1（见 [Q8](#q8)，可丢则靠短 TTL 兜底）。

```text
// 读路径伪流程（示意，非完整程序）
if let Some(v) = l1.get(&key) { return v; }
if let Some(v) = redis_get(&key).await? {
    l1.insert(key.clone(), v.clone());
    return v;
}
let v = db_load(&key).await?;
redis_set_ex(&key, &v, ttl_l2).await?;
l1.insert(key, v.clone());
v
```

注意：L1 过久会导致多实例「各看各的」；热点可读，强一致字段别只信 L1。

**Go 对比：**
- **Go 怎么做**：同样 L1（Ristretto）+ Redis；模式通用。
- **Rust 为什么不同**：L1 常用 moka；其余一样。
- **Go 程序员易踩的坑**：只更新 Redis 忘了本地——用户隔几秒看到旧值。

**记忆点：**
- L1 短小、L2 共享、DB 权威。
- 写后失效，别只靠「希望 TTL 刚好」。

---

## Q12. 什么时候不该上 Redis {#q12}
**Tags:** `common` `when-not` `Redis`
**适用版本:** 架构判断

**一句话答案：**
单实例、数据可全放内存、无跨进程共享需求时，本地缓存就够。没有运维能力、延迟预算极紧且不能接受网络跳、或只是「把 DB 当慢 Redis 用」时，也不该硬上。Redis 是依赖，不是勋章。

**解答：**
可以不上的信号：

| 信号 | 更合适 |
|------|--------|
| 单进程/单机工具 | moka / HashMap |
| 数据量小且可重建 | 本地 + DB |
| 团队无人会运维 Redis | 先简化架构 |
| 要强事务/复杂查询 | 正经 DB，不是 Redis |
| 「因为别的服务用了」 | 复制依赖不等于需要 |

该上的信号（呼应 [Q2](#q2)）：多副本共享会话/限流/锁、明确的热 key、可接受多一跳网络。

「❌ 错误预期」——上了 Redis 性能一定更好：错误使用（巨 key、热 key 无本地、同步阻塞）可以更慢更脆。

**Go 对比：**
- **Go 怎么做**：同样按拓扑决定，不是按语言决定。
- **Rust 为什么不同**：无差异——别为「Rust 服务标配」强行加组件。
- **Go 程序员易踩的坑**：把 Redis 当唯一数据源，重启或闪断直接业务停摆却无降级。

**记忆点：**
- 无共享需求 → 先本地。
- Redis 是共享与协调工具，不是默认标配。
