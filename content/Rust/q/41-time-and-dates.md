+++
title = "41-时间与日期"
date = 2026-07-28T14:49:00+08:00
weight = 410
type = "docs"
description = "面向 Go 用户讲清 Instant/SystemTime/Duration、chrono 日历与时区"
isCJKLanguage = true
draft = false

+++

# 时间与日期 (Time and Dates)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否分不清：`Instant` 和 `SystemTime` 哪个用来测耗时、哪个用来当时间戳？
- 你是否想算超时/睡眠，却搞混 `Duration`、阻塞 `sleep` 和 Tokio 的 `sleep`？
- 你是否要解析 RFC3339、按时区显示、对标 Go 的 Layout，却发现 std 几乎没有「日历」API？
- 你是否要在 serde 里序列化时间字段，或把 monotonic 时钟误当成文件修改时间？
- 你是否踩过夏令时、定时/间隔任务，不知道该用 chrono 还是 time、怎么和 Go `time` 对照？
- 你是否误把 `NaiveDateTime` 当「带时区时间」，或卡在 `SystemTime` 与 chrono 互转？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| **Instant** | — | 单调时刻 | 适合测间隔；不可跨进程当墙钟 | `time.Now()` 用于 `Since` 的那一侧习惯，更近 `monotonic` 读数 |
| **SystemTime** | — | 系统墙钟时间 | 可转成 UNIX 时间戳；可被 NTP 回调 | `time.Now()` 的日历/墙钟用途 |
| **Duration** | — | 时间长度 | 「过了多久」，不是某个日期 | `time.Duration` |
| monotonic | — | 单调时钟 | 只往前走（相对），不保证与日历对齐 | Go 1.9+ `Since` 用的单调读数 |
| wall clock | — | 墙钟 | 墙上挂的日期时间，可被调整 | 普通 `time.Time` 展示 |
| UNIX timestamp | — | UNIX 时间戳 | 相对 1970-01-01 UTC 的秒/毫秒 | `Unix()` / `UnixMilli()` |
| RFC3339 | — | 日期时间文本标准 | 如 `2026-07-28T14:49:00+08:00` | `time.RFC3339` |
| UTC | Coordinated Universal Time | 协调世界时 | 全球基准时区，无夏令时 | `time.UTC` |
| time zone | — | 时区 | 相对 UTC 的偏移 + 规则（含夏令时） | `time.Location` |
| DST | Daylight Saving Time | 夏令时 | 一年中部分时段拨快/拨慢一小时 | 同概念 |
| chrono | — | 常用日期时间 crate | 日历、时区、解析/格式化 | `time` 包的日历部分 |
| time (crate) | — | 另一常用时间 crate | 与 chrono 二选一或并用，API 不同 | 同左 |
| serde | SERialize/DEserialize | 序列化框架 | 时间字段常见 `Serialize`；见 [36-serde](../36-serde-and-serialization/) | `encoding/json` + `time.Time` |
| Layout | — | Go 格式化参考时间 | Go 用 `2006-01-02...` 当模板 | `time.Format` / `Parse` |
| tokio::time | — | 异步时间工具 | async sleep、interval、timeout | 定时器 + goroutine |
| NaiveDateTime | — | 朴素日期时间 | 无时区信息的日期+时间 | 不带 Location 的本地墙钟片段 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q9](#q9), [Q13](#q13) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q10](#q10), [Q14](#q14) |
| `occasional` | [Q11](#q11), [Q12](#q12) |
| `advanced` | — |

---

## Q1. `Instant` 和 `SystemTime` 有什么差别？ {#q1}
**Tags:** `hot` `beginner` `Instant` `SystemTime`
**适用版本:** Rust 1.0+（`Instant`/`SystemTime` 在 `std::time`）

**一句话答案：**
**Instant** 是单调时钟上的点，只适合算「过了多久」；**SystemTime** 是墙钟，可拿来当时间戳、和文件/网络时间比较。测耗时用 Instant；记录「几点几分」用 SystemTime（或 chrono）。

**解答：**
测耗时：

```rust
use std::time::{Duration, Instant};
use std::thread;

fn main() {
    let start = Instant::now();
    thread::sleep(Duration::from_millis(50));
    let elapsed = start.elapsed();
    println!("elapsed_ms ≈ {}", elapsed.as_millis());
}
```

墙钟时间戳：

```rust
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    let now = SystemTime::now();
    let secs = now
        .duration_since(UNIX_EPOCH)
        .expect("clock before epoch")
        .as_secs();
    println!("unix_secs = {secs}");
}
```

| | Instant | SystemTime |
|--|---------|------------|
| 用途 | 基准、超时、测速 | 日志时间、过期时间、文件 mtime |
| 能否打印成日期 | 不能（无日历意义） | 能（常再交给 chrono） |
| NTP 回调 | 不受影响（相对） | 可能突然跳变 |
| 跨机器比较 | 无意义 | 有意义（若时钟同步） |

```rust
use std::time::{Instant, SystemTime};

fn main() {
    let _a: Instant = Instant::now();
    let _b: SystemTime = SystemTime::now();
    // Instant 不能直接 format 成 "2026-..."；那是日历库的活
}
```

**Go 对比：**
```go
start := time.Now()
elapsed := time.Since(start) // 内部可用单调读数
wall := time.Now().UTC()
```
- **Go 怎么做**：一个 `time.Time` 兼墙钟与单调读数（Go 1.9+ `Since` 更稳）。
- **Rust 为什么不同**：把「测间隔」和「读日历」拆成两个类型，避免混用。
- **Go 程序员易踩的坑**：把 `Instant` 序列化进 JSON 当事件时间——类型本身就不表达墙钟。

**记忆点：**
- 耗时 / 超时基准 → Instant。
- 几点几分 / UNIX 戳 → SystemTime（或 chrono）。

---

## Q2. `Duration` 怎么用？和秒/毫秒怎么换？ {#q2}
**Tags:** `hot` `beginner` `Duration`
**适用版本:** Rust 1.0+（部分便捷方法随版本增加，常用 API 早已稳定）

**一句话答案：**
`Duration` 表示时间长度；用 `from_secs` / `from_millis` / `from_micros` / `from_nanos` 构造，用 `as_secs` / `as_millis` 等读出；可与 Instant 做加减。

**解答：**

```rust
use std::time::Duration;

fn main() {
    let a = Duration::from_millis(1500);
    let b = Duration::from_secs(2);
    let sum = a + b;
    println!("sum_ms = {}", sum.as_millis()); // 3500
    println!("secs_f64 = {}", sum.as_secs_f64());
}
```

饱和与检查：

```rust
use std::time::Duration;

fn main() {
    let d = Duration::from_secs(5);
    // checked_* 在溢出时返回 None，而不是 panic / wrap
    assert_eq!(d.checked_mul(2), Some(Duration::from_secs(10)));
    assert_eq!(d.saturating_sub(Duration::from_secs(9)), Duration::ZERO);
}
```

和 Instant：

```rust
use std::time::{Duration, Instant};

fn main() {
    let start = Instant::now();
    let deadline = start + Duration::from_secs(1);
    while Instant::now() < deadline {
        // 忙等仅作演示；真实代码用 sleep / async sleep
    }
    println!("done in {:?}", start.elapsed());
}
```

注意：`Duration` 不能是负的；「早了多少」用两个 Instant/SystemTime 的 `duration_since` / `checked_duration_since` 表达。

**Go 对比：**
```go
d := 1500 * time.Millisecond
fmt.Println(d.Milliseconds())
```
- **Go 怎么做**：`time.Duration` 底层是 `int64` 纳秒，可为负。
- **Rust 为什么不同**：`Duration` 非负；负间隔要自己换算或用有符号类型。
- **Go 程序员易踩的坑**：写 `Duration::from_secs(-1)`——根本编不过。

**记忆点：**
- 长度用 Duration；时刻用 Instant/SystemTime。
- 构造 `from_*`，读取 `as_*`。

---

## Q3. 为什么 std 几乎没有日历 API？要 chrono 还是 time？ {#q3}
**Tags:** `hot` `chrono` `time` `calendar`
**适用版本:** 概念；chrono 0.4.x / time 0.3.x 为常见选型

**一句话答案：**
标准库只提供 Instant/SystemTime/Duration，不提供时区数据库、RFC3339 解析、本地化格式化；日历与时区交给社区 crate——目前最常见的是 **chrono** 或 **time**，二选一为主即可。

**解答：**
std 能做的边界：

```rust
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    let secs = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    println!("unix = {secs}"); // 到这里为止；没有 "年-月-日" API
}
```

需要日历时（示意，外部 crate 用 text）：

```toml
[dependencies]
chrono = "0.4"
# 或
# time = "0.3"
```

```text
// chrono 思路
use chrono::Utc;
let now = Utc::now();
println!("{}", now.to_rfc3339());
```

```text
// time crate 思路
use time::OffsetDateTime;
let now = OffsetDateTime::now_utc();
```

选型直觉：
- 生态示例多、和 serde feature 文档多 → 很多人选 chrono
- 更小/另一套 API 风格 → time crate
- 不要两个都深度混用，转换成本高

**Go 对比：**
```go
t := time.Now().In(time.UTC)
fmt.Println(t.Format(time.RFC3339))
```
- **Go 怎么做**：日历、时区、Format/Parse 都在 std `time`。
- **Rust 为什么不同**：时区数据与解析策略易变，留给 crate 迭代。
- **Go 程序员易踩的坑**：在 std 里找 `Format("2006...")`——没有，请 `cargo add chrono` 或 `time`。

**记忆点：**
- std = 时钟与长度；日历 = chrono/time。
- 项目内统一选一个生态。

---

## Q4. 怎么解析 RFC3339？ {#q4}
**Tags:** `hot` `RFC3339` `chrono` `parse`
**适用版本:** chrono 0.4.x（或 time 0.3 的等价 API）

**一句话答案：**
用 chrono 的 `DateTime::parse_from_rfc3339` / `DateTime::<FixedOffset>::parse_from_rfc3339`，或先读成带偏移的时间再转 UTC；字符串必须带偏移或 `Z`。

**解答：**

```toml
[dependencies]
chrono = "0.4"
```

```text
use chrono::{DateTime, FixedOffset, Utc};

fn main() {
    let s = "2026-07-28T14:49:00+08:00";
    let dt = DateTime::parse_from_rfc3339(s).expect("bad rfc3339");
    let utc: DateTime<Utc> = dt.with_timezone(&Utc);
    println!("utc = {}", utc.to_rfc3339());
}
```

```text
// 接受 Zulu
let z = "2026-07-28T06:49:00Z";
let dt = DateTime::parse_from_rfc3339(z).unwrap();
assert_eq!(dt.timezone(), FixedOffset::east_opt(0).unwrap());
```

失败时返回 `ParseError`——常见原因：缺偏移、用了空格而不是 `T`、只有日期没有时间。若输入是自定义格式而不是 RFC3339，用 `NaiveDateTime::parse_from_str` + format 字符串（见 [Q6](#q6)）。

**Go 对比：**
```go
t, err := time.Parse(time.RFC3339, "2026-07-28T14:49:00+08:00")
```
- **Go 怎么做**：`time.Parse(time.RFC3339, s)`。
- **Rust 为什么不同**：同等能力在 chrono/time，不在 std。
- **Go 程序员易踩的坑**：把 `2026-07-28 14:49:00` 当 RFC3339——两边都会挂，格式要完整。

**记忆点：**
- RFC3339 → `parse_from_rfc3339`。
- 入库/比较常转成 UTC。

---

## Q5. 时区和 UTC 怎么处理？ {#q5}
**Tags:** `common` `UTC` `timezone` `chrono`
**适用版本:** chrono 0.4（`clock` / `std` feature 按需）；IANA 时区常需 `chrono-tz`

**一句话答案：**
内部存储与跨服务交换优先 **UTC**（协调世界时）；展示给用户时再转到具体 **time zone**（时区）。chrono 里用 `Utc` / `FixedOffset` / `chrono_tz::...`。

**解答：**

```text
use chrono::{TimeZone, Utc};
use chrono_tz::Asia::Shanghai;

let utc = Utc::now();
let sh = utc.with_timezone(&Shanghai);
println!("utc = {utc}");
println!("shanghai = {sh}");
```

```toml
[dependencies]
chrono = "0.4"
chrono-tz = "0.10"
```

固定偏移（不含夏令时规则）：

```text
use chrono::{FixedOffset, Utc};

let east8 = FixedOffset::east_opt(8 * 3600).unwrap();
let local = Utc::now().with_timezone(&east8);
```

原则：
- 数据库 / API 默认存 UTC 或 RFC3339 带偏移
- 「本地时区」依赖机器环境，服务器上不可靠就显式传 `Asia/Shanghai` 这类 IANA 名
- **DST**（夏令时）规则在 IANA 库里，不要自己 ±1 小时硬编码——见 [Q11](#q11)

**Go 对比：**
```go
loc, _ := time.LoadLocation("Asia/Shanghai")
t := time.Now().In(loc)
```
- **Go 怎么做**：`LoadLocation` + `In`。
- **Rust 为什么不同**：标准库不带时区库；chrono-tz / time-tz 提供 IANA 数据。
- **Go 程序员易踩的坑**：在服务器用「本地 Local」写业务——容器时区常是 UTC，显示会错。

**记忆点：**
- 存 UTC，显示再转。
- 真时区用 IANA，不要只记 +08:00 硬编码（有 DST 的地区会错）。

---

## Q6. 格式化怎么对标 Go 的 Layout？ {#q6}
**Tags:** `common` `format` `Layout` `chrono` `strftime`
**适用版本:** chrono 0.4

**一句话答案：**
Go 用参考时间 `2006-01-02 15:04:05` 当 **Layout**；chrono 用类似 strftime 的 `%Y-%m-%d %H:%M:%S`。先记一张对照表，不要把 Go 的 Layout 字符串直接贴进 Rust。

**解答：**

| 意图 | Go Layout | chrono format |
|------|-----------|--------------|
| 日期 | `2006-01-02` | `%Y-%m-%d` |
| 时间 | `15:04:05` | `%H:%M:%S` |
| RFC3339 | `time.RFC3339` | `.to_rfc3339()` 或等价 |
| 12 小时 | `03:04:05 PM` | `%I:%M:%S %p` |

```text
use chrono::Utc;

let s = Utc::now().format("%Y-%m-%d %H:%M:%S").to_string();
println!("{s}");
```

```text
use chrono::NaiveDateTime;

let ndt = NaiveDateTime::parse_from_str("2026-07-28 14:49:00", "%Y-%m-%d %H:%M:%S")
    .expect("parse");
println!("{ndt}");
```

`NaiveDateTime` 表示「无时区的日期时间」——解析本地日志常用；一要跨时区就挂上 `Utc` / `FixedOffset`。

**Go 对比：**
```go
t.Format("2006-01-02 15:04:05")
time.Parse("2006-01-02 15:04:05", s)
```
- **Go 怎么做**：死记参考时间 2006-01-02…。
- **Rust 为什么不同**：chrono 走 `%` 占位符（更像 C strftime / 许多别的语言）。
- **Go 程序员易踩的坑**：写成 `format("2006-01-02")`——chrono 会把它当字面量或乱解析。

**记忆点：**
- Go Layout ≠ chrono format。
- 日常：`%Y-%m-%d %H:%M:%S`；标准交换：RFC3339。

---

## Q7. serde 里时间字段怎么序列化？ {#q7}
**Tags:** `common` `serde` `chrono` `JSON`
**适用版本:** chrono 0.4（`serde` feature）；serde 1.x；概念见 [36-serde](../36-serde-and-serialization/)

**一句话答案：**
给 chrono 打开 `serde` feature，在字段上用 `DateTime<Utc>` 等类型；默认常序列化成字符串（RFC3339 一类）。也可用 `serde_with` / 属性控制时间戳整数形式。

**解答：**

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", features = ["serde"] }
```

```text
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Event {
    id: u64,
    at: DateTime<Utc>,
}

let ev = Event {
    id: 1,
    at: Utc::now(),
};
let s = serde_json::to_string(&ev).unwrap();
// {"id":1,"at":"2026-07-28T06:49:00Z"} 形态（具体以实际为准）
```

只要整数时间戳时，可用辅助 crate 或手写：

```text
// 思路：字段用 i64，自己 as_secs；或 serde_with::TimestampSeconds
```

`Option<DateTime<Utc>>` 表示可缺省；与 Go 的 `*time.Time` / `omitempty` 类似，属性写法见 serde 篇。

**Go 对比：**
```go
type Event struct {
    At time.Time `json:"at"`
}
```
- **Go 怎么做**：`time.Time` 默认 RFC3339 文本。
- **Rust 为什么不同**：类型在 chrono，能力靠 `features = ["serde"]` 打开。
- **Go 程序员易踩的坑**：chrono 没开 serde feature 就 derive——编译失败。

**记忆点：**
- `chrono` + `features = ["serde"]` + `DateTime<Utc>`。
- API 交换优先 RFC3339 字符串。

---

## Q8. 为什么 monotonic 的 Instant 不能当文件时间戳？ {#q8}
**Tags:** `common` `Instant` `mtime` `monotonic`
**适用版本:** Rust 1.0+

**一句话答案：**
Instant 只在本进程内有相对意义，不能持久化、不能跨重启比较、也不能告诉用户「下午三点」；文件修改时间、HTTP `Date`、数据库列都要墙钟（SystemTime / chrono）。

**解答：**

```rust
use std::time::Instant;

fn main() {
    let t = Instant::now();
    // 没有 to_rfc3339，也没有 duration_since(UNIX_EPOCH)
    println!("{t:?}"); // 调试用，不是可移植时间戳
}
```

文件元数据用墙钟：

```rust
use std::fs;
use std::time::SystemTime;

fn main() -> std::io::Result<()> {
    let meta = fs::metadata(".")?;
    let modified: SystemTime = meta.modified()?;
    println!("mtime = {modified:?}");
    Ok(())
}
```

错误心智：
- 「我测延迟用 Instant，顺便存进 Redis」→ 重启后无法解释
- 「两个机器的 Instant 比大小」→ 无意义
- 「日志里打印 Instant」→ 运维读不懂

正确拆分：耗时用 Instant；业务时间用 SystemTime/chrono。

**Go 对比：**
```go
info, _ := os.Stat(path)
info.ModTime() // time.Time 墙钟
```
- **Go 怎么做**：文件时间是 `time.Time`；测速用 `Since`（单调）。
- **Rust 为什么不同**：类型系统强制你分开——Instant 根本转不成 UNIX。
- **Go 程序员易踩的坑**：以为 `Instant` 像 `time.Time` 一样能 `MarshalJSON`。

**记忆点：**
- Instant = 秒表；SystemTime = 挂钟。
- mtime / 过期时间 / 日志 → 挂钟。

---

## Q9. `thread::sleep` 和 `tokio::time::sleep` 有什么差别？ {#q9}
**Tags:** `hot` `sleep` `tokio` `async`
**适用版本:** std；tokio 1.x（`time` feature）；async 见 [31-async-programming](../31-async-programming/)

**一句话答案：**
`std::thread::sleep` 阻塞整条 OS 线程；`tokio::time::sleep` 只让出当前任务，同线程上其它任务还能跑。在 async 函数里用阻塞 sleep 会卡住 runtime。

**解答：**
同步代码：

```rust
use std::thread;
use std::time::Duration;

fn main() {
    println!("before");
    thread::sleep(Duration::from_millis(100));
    println!("after");
}
```

async 代码（外部 crate，text）：

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
```

```text
#[tokio::main]
async fn main() {
    println!("before");
    tokio::time::sleep(Duration::from_millis(100)).await;
    println!("after");
}
```

「❌ 错误写法」——在 async 里阻塞：

```text
async fn bad() {
    std::thread::sleep(Duration::from_secs(5)); // 卡住 worker 线程
}
```

「✅ 正确写法」——`.await` 睡眠：

```text
async fn good() {
    tokio::time::sleep(Duration::from_secs(5)).await;
}
```

超时包裹：`tokio::time::timeout(dur, future)`。同步程序没有 runtime，用 `thread::sleep` 即可。

**Go 对比：**
```go
time.Sleep(100 * time.Millisecond) // 阻塞当前 goroutine，调度器可运转其它 goroutine
```
- **Go 怎么做**：`time.Sleep` 对 goroutine 友好。
- **Rust 为什么不同**：线程 ≠ 异步任务；阻塞线程会饿死同线程任务。
- **Go 程序员易踩的坑**：把 `thread::sleep` 当成 `time.Sleep` 丢进 `async fn`。

**记忆点：**
- sync → `thread::sleep`。
- async → `tokio::time::sleep().await`。

---

## Q10. 和 Go 的 `time` 包怎么对照？ {#q10}
**Tags:** `common` `go` `time` `对照`
**适用版本:** 概念对照

**一句话答案：**
Go 一个 `time` 包揽 Duration、Time、时区、Timer、Ticker；Rust 拆成 std 的 Instant/SystemTime/Duration + chrono/time 日历 + tokio::time 异步定时。按「长度 / 墙钟 / 日历 / 异步定时」四张抽屉找。

**解答：**

| 需求 | Go | Rust |
|------|----|------|
| 长度 | `time.Duration` | `std::time::Duration` |
| 测耗时 | `time.Since` | `Instant::now().elapsed()` |
| 墙钟 | `time.Now()` | `SystemTime::now()` / `Utc::now()` |
| 解析 RFC3339 | `time.Parse(RFC3339, …)` | chrono / time crate |
| Format | Layout `2006-…` | chrono `%Y-…` |
| 时区 | `LoadLocation` | chrono-tz 等 |
| Sleep | `time.Sleep` | `thread::sleep` / `tokio::time::sleep` |
| Ticker | `time.NewTicker` | `tokio::time::interval`（async） |
| JSON | `time.Time` | chrono + serde feature |

```go
d := 2 * time.Second
t := time.Now().UTC()
time.Sleep(d)
```

```rust
use std::time::{Duration, Instant, SystemTime};

fn main() {
    let d = Duration::from_secs(2);
    let _wall = SystemTime::now();
    let _start = Instant::now();
    std::thread::sleep(d);
}
```

**Go 对比：**
- **Go 怎么做**：stdlib 一站式。
- **Rust 为什么不同**：时钟原语进 std，日历与 async 定时进生态。
- **Go 程序员易踩的坑**：按「包名 time」去 std 找 Format/Parse/Ticker——只找到一半。

**记忆点：**
- 四抽屉：Duration、Instant、SystemTime、日历 crate。
- async 定时另开 tokio::time。

---

## Q11. 夏令时有哪些坑？ {#q11}
**Tags:** `occasional` `DST` `timezone`
**适用版本:** 概念；实现依赖 chrono-tz / IANA 数据

**一句话答案：**
**DST**（夏令时）让本地时间出现「跳过一小时」或「重复一小时」；用固定 `+01:00` 硬算、或对本地钟做「加一天」而不用日历 API，都会在换日边界出错。用 UTC 存、用 IANA 时区显示。

**解答：**
典型故障：
- 本地 2:30 在「春季拨快」那天不存在 → 解析歧义/错误
- 「秋季拨慢」同一本地时间出现两次 → 不知道是第一次还是第二次
- `+ 24*time.Hour` 跨过 DST 不等于「下一个日历日」

```text
// 错误思路：自己 now + 3600 当「本地下一小时」
// 正确思路：在 UTC 上算绝对长度；或用时区库的日历加法
```

```text
use chrono::{Duration, Utc};
// 绝对长度：与 DST 无关
let later = Utc::now() + Duration::hours(24);
```

展示到纽约/伦敦时再 `with_timezone(&chrono_tz::America::New_York)`。业务「下一个本地工作日」要用日历 API（按日期加天），不要按固定 24h 加。

**Go 对比：**
```go
// 同样：t.Add(24*time.Hour) 不等于永远「明天同一本地点」
t = t.In(loc).AddDate(0, 0, 1)
```
- **Go 怎么做**：`AddDate` 做日历加法；Location 含 DST 规则。
- **Rust 为什么不同**：同样要分「绝对 Duration」与「日历加减」；规则在 tz 数据里。
- **Go 程序员易踩的坑**：两边都会犯——换语言不免疫 DST。

**记忆点：**
- 存储 UTC；显示用 IANA。
- 「加一天」用日历，不要只用 +24h。

---

## Q12. 定时与间隔怎么简述？ {#q12}
**Tags:** `occasional` `timer` `interval` `tokio`
**适用版本:** tokio 1.x（`time` feature）；同步侧可用 std 或线程

**一句话答案：**
async 里用 `tokio::time::sleep` 做一次性延迟，用 `interval` / `interval_at` 做周期性滴答；同步程序用线程 + `sleep` 循环，或专用定时库。不要在 async 里用阻塞 sleep 冒充定时器。

**解答：**

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
```

```text
use std::time::Duration;
use tokio::time::{interval, sleep};

#[tokio::main]
async fn main() {
    // 一次性
    sleep(Duration::from_secs(1)).await;

    // 周期性
    let mut tick = interval(Duration::from_millis(200));
    for _ in 0..3 {
        tick.tick().await;
        println!("tick");
    }
}
```

注意：
- `interval` 默认可能「追赶」积压的 tick（行为看文档与 `MissedTickBehavior`）
- 任务里干重活要考虑是否 `spawn_blocking`，避免拖慢调度
- 分布式定时（多实例只跑一次）要锁/队列，不是单进程 `interval` 能解决的

同步简述：

```rust
use std::thread;
use std::time::Duration;

fn main() {
    for i in 0..3 {
        println!("sync tick {i}");
        thread::sleep(Duration::from_millis(50));
    }
}
```

**Go 对比：**
```go
ticker := time.NewTicker(200 * time.Millisecond)
defer ticker.Stop()
for i := 0; i < 3; i++ {
    <-ticker.C
}
```
- **Go 怎么做**：`Timer` / `Ticker` + channel。
- **Rust 为什么不同**：async 下是 Future；同步下常自己 sleep 循环。
- **Go 程序员易踩的坑**：在 Tokio 里开一堆线程版 ticker，却占满 blocking 线程池。

**记忆点：**
- 一次：`sleep().await`；周期：`interval`。
- 多实例定时要额外协调，不单靠本地 ticker。

---

## Q13. 为什么说 `NaiveDateTime` 很危险？ {#q13}
**Tags:** `hot` `NaiveDateTime` `timezone` `pitfall`
**适用版本:** chrono 0.4

**一句话答案：**
**NaiveDateTime** 只有「年月日时分秒」，**没有时区**。它看起来像完整时间，却不能安全地做跨区比较、持久化「绝对时刻」或和 `DateTime<Utc>` 混用。日志本地片段可以 naive；业务时刻请用 `DateTime<Utc>` / 带 offset 的类型。

**解答：**
[Q6](#q6) 展示了用 `NaiveDateTime::parse_from_str` 解析——那是合法用法。危险在于**误用语义**：

```text
use chrono::{NaiveDateTime, TimeZone, Utc};

// 看起来像「一个时间点」，其实只是墙上数字
let naive = NaiveDateTime::parse_from_str("2026-07-28 14:49:00", "%Y-%m-%d %H:%M:%S")
    .expect("parse");

// 必须显式宣布「这数字按哪个时区解释」
let as_utc = Utc.from_utc_datetime(&naive);
// 若其实是本地墙钟，应用 Local / FixedOffset::east_opt(...).unwrap().from_local_datetime(&naive)
println!("{as_utc}");
```

「❌ 错误直觉」：

```text
// 把 NaiveDateTime 直接当 UTC 存进数据库，又在别的机器当本地读
// → 偏移错 8 小时一类事故；编译器不会拦你
```

安全默认：
- 存储 / API：`DateTime<Utc>` 或 RFC3339 带偏移
- 仅「排班表上的 09:00」这种无区日历：才用 `NaiveTime` / `NaiveDate` / `NaiveDateTime`，并在文档写清语义

**Go 对比：**
```go
// time.Date(...) 若不 In(loc)，也容易留下「看似有时间实则歧义」
t := time.Date(2026, 7, 28, 14, 49, 0, 0, time.UTC) // 必须带 Location
```
- **Go 怎么做**：`time.Time` 始终带 Location（哪怕是 UTC）。
- **Rust 为什么不同**：chrono 把「无区」和「有区」拆成不同类型——更诚实，也更好踩。
- **Go 程序员易踩的坑**：看见 `DateTime` 字样就当 Go 的 `time.Time`；naive ≠ instant。

**记忆点：**
- Naive = 缺时区；跨机器前先挂上时区。
- 默认存 UTC 的 `DateTime`。

---

## Q14. `SystemTime` 和 chrono 怎么互转？ {#q14}
**Tags:** `common` `SystemTime` `chrono` `conversion`
**适用版本:** chrono 0.4（`clock` / 转换 API）；`std::time::SystemTime`

**一句话答案：**
`SystemTime` ↔ `DateTime<Utc>` 用 chrono 的 `DateTime::<Utc>::from(system_time)` 与 `.into()` / `SystemTime::from(datetime)`（具体方法名以你用的 chrono 版本为准）；先统一到 UTC，再格式化到本地。文件 `metadata().modified()` 拿到的就是 `SystemTime`。

**解答：**

```toml
[dependencies]
chrono = "0.4"
```

```text
use chrono::{DateTime, Utc};
use std::time::SystemTime;

fn system_to_chrono(st: SystemTime) -> DateTime<Utc> {
    DateTime::<Utc>::from(st)
}

fn chrono_to_system(dt: DateTime<Utc>) -> SystemTime {
    SystemTime::from(dt)
}

fn main() {
    let now = SystemTime::now();
    let dt = system_to_chrono(now);
    let back = chrono_to_system(dt);
    let _ = back;
    println!("{}", dt.to_rfc3339());
}
```

和文件时间：

```text
use std::fs;
use chrono::{DateTime, Utc};

let modified = fs::metadata("Cargo.toml")?.modified()?;
let dt: DateTime<Utc> = modified.into();
println!("{}", dt);
```

注意：`SystemTime` 在 Unix 上通常相对 UNIX_EPOCH；转换失败（极端平台/溢出）要用可 fallible 的 API 并处理 `None`/`Err`（若你用的版本提供 checked 变体）。

**Go 对比：**
```go
// Go 一个 time.Time 打通墙钟；从 syscall 来的也是 time.Time
```
- **Go 怎么做**：很少需要「std 墙钟 ↔ 日历库」两套类型。
- **Rust 为什么不同**：std 只有 `SystemTime`；日历在 chrono/time。
- **Go 程序员易踩的坑**：到处传 `SystemTime` 又要 RFC3339——尽早转成 `DateTime<Utc>`。

**记忆点：**
- 文件/OS → `SystemTime` → `DateTime<Utc>`。
- 展示/计算日历 → 留在 chrono。

---
