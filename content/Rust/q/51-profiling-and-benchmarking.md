+++
title = "51-profiling-and-benchmarking"
date = 2026-07-28T14:49:00+08:00
weight = 510
type = "docs"
description = "面向 Go 用户讲清 criterion、flamegraph、samply/perf 与 tokio-console 对标 pprof"
isCJKLanguage = true
draft = false

+++

# 性能剖析与基准测试 (Profiling and Benchmarking)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否习惯 `go test -bench` / `pprof`，一到 Rust 就问「火焰图和基准怎么搞」？
- 你是否分不清 **criterion**、`cargo bench`、手写 `Instant` 各自能回答什么问题？
- 你是否想对标 Go pprof：CPU 火焰图、分配剖析、异步任务卡住？
- 你是否在 **debug** 下测速、或忘记 `black_box`，结果完全不可信？
- 你是否在 Windows 上不知道用啥代替 Linux `perf`？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| benchmark | — | 基准测试 | 反复跑同一代码测耗时/吞吐 | `testing.B` / `-bench` |
| **criterion** | — | 常用基准框架 | 统计稳、出报告的 Rust bench crate | `testing` + benchstat 一类 |
| profiling | — | 性能剖析 | 看时间/样本花在哪些函数 | `pprof` |
| flamegraph | — | 火焰图 | 用宽度表示采样占比的可视化 | `pprof -http` 火焰图 |
| **cargo-flamegraph** | — | 火焰图工具 | 封装采样并生成 SVG | `go tool pprof` |
| **samply** | — | 采样剖析器 | 跨平台采样，浏览器看结果 | pprof / async-profiler 一类 |
| perf | — | Linux 性能事件工具 | 内核采样与计数 | Linux 上常用底层 |
| `black_box` | — | 黑盒屏障 | 阻止编译器把基准代码优化没 | `KeepAlive` / 汇编屏障近似 |
| allocation profiling | — | 分配剖析 | 看堆分配次数与来源 | `pprof` heap |
| **tokio-console** | — | Tokio 任务观察 | 看异步任务调度/阻塞 | 无单一标配；靠自定义 + pprof |
| release profile | — | 发布构建配置 | `cargo build --release` 的优化档 | 类似 `-ldflags`/`-gcflags` 调优 |
| CI | Continuous Integration | 持续集成 | 自动跑测试/基准的流水线 | 同概念 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q8](#q8) |
| `common` | [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. Rust 里对标 Go `pprof` / `-bench` 的工具链是什么？ {#q1}
**Tags:** `hot` `beginner` `pprof` `overview`
**适用版本:** 工具链选型；与 rustc 1.97 无关

**一句话答案：**
**测快慢**：`cargo bench` + **criterion**（见 [04-running Q18](../04-running/#q18)）。**看 CPU 热点**：`cargo flamegraph` / **samply** / Linux **perf**。**看异步卡住**：**tokio-console**。没有单一「官方 pprof」，而是按问题选工具。

**解答：**

| 你想问 | Rust 常见答案 | Go |
|--------|---------------|-----|
| 这段代码谁更快？ | criterion / `cargo bench` | `go test -bench` |
| CPU 花在哪？ | flamegraph / samply / perf | `pprof` CPU |
| 堆分配狂？ | dhat / heaptrack / 采样分配器 | `pprof` heap |
| Tokio 任务堵？ | tokio-console | 自建指标 + pprof |
| 线上服务 | 持续 profiling 产品 / 导出 | `net/http/pprof` |

```text
问题 ──┬─ 微基准对比 ──► criterion
      ├─ CPU 火焰图 ──► cargo flamegraph / samply
      ├─ 分配 ────────► dhat / heaptrack 等
      └─ async 调度 ──► tokio-console
```

```rust
fn main() {
    // 本篇地图：先选对工具，再谈参数
    println!("bench ≠ profile ≠ tracing spans");
}
```

**Go 对比：**
- **Go 怎么做**：`testing` + `runtime/pprof` / `net/http/pprof` 一条龙很齐。
- **Rust 为什么不同**：语言不绑剖析器；Cargo 生态组合。
- **Go 程序员易踩的坑**：只搜 `pprof` crate 名字，忽略 flamegraph/criterion 主路径。

**记忆点：**
- 比快慢 → criterion；找热点 → 火焰图。
- async 另开 tokio-console。

---

## Q2. criterion 最小怎么写？和手写 `Instant` 差在哪？ {#q2}
**Tags:** `hot` `criterion` `Instant` `cargo bench`
**适用版本:** criterion 0.5.x（API 以文档为准）

**一句话答案：**
严肃对比用 **criterion**（统计重复、暖机、出报告）；`Instant` 只适合粗测或教学。criterion 模板与 `harness = false` 见 [04-running Q18](../04-running/#q18)。

**解答：**
依赖与声明（toml）：

```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "sum"
harness = false
```

bench 文件示意（text）：

```text
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn sum_bench(c: &mut Criterion) {
    c.bench_function("sum_1e6", |b| {
        b.iter(|| (0u64..1_000_000).sum::<u64>())
    });
}

criterion_group!(benches, sum_bench);
criterion_main!(benches);
```

手写粗测（可编译，但不作对比依据）：

```rust
use std::time::Instant;

fn main() {
    let t = Instant::now();
    let n: u64 = (0..1_000_000).sum();
    println!("n={n} {:?}", t.elapsed());
}
```

**Go 对比：**
```go
func BenchmarkSum(b *testing.B) {
    for i := 0; i < b.N; i++ { /* ... */ }
}
```
- **Go 怎么做**：标准库 bench + `b.N`。
- **Rust 为什么不同**：默认 libtest bench 较弱，社区用 criterion。
- **Go 程序员易踩的坑**：用 `println!` + `Instant` 在 debug 下「优化对比」。

**记忆点：**
- `cargo bench` + criterion。
- `Instant` = 粗测，不是 A/B 裁判。

---

## Q3. 为什么必须 `--release`（或 bench 的优化档）？ {#q3}
**Tags:** `hot` `release` `debug` `opt-level`
**适用版本:** Cargo profiles

**一句话答案：**
debug 默认几乎不优化，数字可以慢一个数量级以上；**性能结论只认 release（或 bench profile）**。Go 也常提醒别拿未优化对比当真理，但 Rust debug/release 差距往往更刺眼。

**解答：**
```bash
cargo run --release
cargo bench          # 默认走 bench profile（偏优化）
cargo build --release
```

```toml
# 若要在测试里也较真（慎用，测会变慢）
[profile.test]
opt-level = 1
```

```rust
fn main() {
    // 同一算法：debug 可能「看起来很慢」，release 才接近线上
    let v: Vec<u64> = (0..10_000).collect();
    println!("{}", v.iter().sum::<u64>());
}
```

「❌ 错误写法」——debug 下测完就下结论「Rust 比 Go 慢 10 倍」。

**Go 对比：**
- **Go 怎么做**：默认构建已较优；仍有 `-gcflags` 等。
- **Rust 为什么不同**：dev profile 优先编译速度。
- **Go 程序员易踩的坑**：`cargo run` 当线上性能。

**记忆点：**
- 谈性能先 `--release`。
- bench 走优化 profile，别拿 dev 比。

---

## Q4. `black_box` 是干什么的？为什么基准会被「优化没」？ {#q4}
**Tags:** `hot` `black_box` `optimizer`
**适用版本:** `std::hint::black_box`（1.66+）；criterion 也提供同名

**一句话答案：**
编译器若发现基准结果未使用，可能删掉整段计算。**`black_box`**（黑盒屏障）让优化器不敢假设值「没用」，从而保住被测代码。criterion 的 `b.iter(|| ...)` 里应对输入/输出适当 `black_box`。

**解答：**
```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let t = Instant::now();
    // 没有 black_box：极端情况下优化器可能把无副作用计算掏空
    let n = black_box((0u64..100_000).sum::<u64>());
    black_box(n);
    println!("{:?}", t.elapsed());
}
```

```rust
fn main() {
    // 反例直觉：只算不读，优化器更有动机删
    let _ = (0u64..100_000).sum::<u64>();
    println!("done");
}
```

**Go 对比：**
- **Go 怎么做**：常用 `runtime.KeepAlive` 或把结果写入包级变量；编译器也在变激进。
- **Rust 为什么不同**：LLVM 优化很猛，基准里 `black_box` 是显式习惯。
- **Go 程序员易踩的坑**：基准里算完就丢，测到「接近 0ns」。

**记忆点：**
- 输入输出都考虑 `black_box`。
- 「太快不合理」先查是否被优化掉。

---

## Q5. 火焰图怎么出？`cargo flamegraph` 最小步骤 {#q5}
**Tags:** `hot` `flamegraph` `CPU`
**适用版本:** `cargo-flamegraph`；Linux/macOS 常见；Windows 见 [Q9](#q9)

**一句话答案：**
安装 `cargo install flamegraph`，对 **release** 二进制跑 `cargo flamegraph --bin your_bin`（或 `--` 传参数），打开生成的 SVG 看扁宽栈帧。这是对标 Go CPU pprof 火焰图的最常见路径之一。

**解答：**
```bash
cargo install flamegraph
# Linux 常需 perf 权限；macOS 用 DTrace 等后端（随工具文档）
cargo flamegraph --bin myapp -- --port 8080
```

```text
看图口令：
- 横向越宽 = 采样越多 = 越值得先看
- 自上而下 = 调用栈
- 先确认是 --release
```

```rust
fn main() {
    // 被剖析的程序要「忙得有代表性」：准备压测流量或自循环热点
    let mut n = 0u64;
    for i in 0..5_000_000 {
        n = n.wrapping_add(i);
    }
    println!("{n}");
}
```

**Go 对比：**
```text
go test -cpuprofile=cpu.out
go tool pprof -http=:8080 cpu.out
```
- **Go 怎么做**：pprof 文件 + 网页 UI。
- **Rust 为什么不同**：常用外部采样器生成 flamegraph SVG。
- **Go 程序员易踩的坑**：对 debug 二进制出图——符号与热点都怪。

**记忆点：**
- `cargo flamegraph` + release。
- 宽帧 = 优先优化候选。

---

## Q6. samply / perf 和 flamegraph 怎么分工？ {#q6}
**Tags:** `common` `samply` `perf`
**适用版本:** 外部工具；平台相关

**一句话答案：**
**perf**：Linux 内核级采样/计数，可接 flamegraph 脚本。**samply**：较友好的跨平台采样，浏览器查看。**cargo-flamegraph**：把「跑程序 + 出图」包成 Cargo 子命令。同一目标：CPU 时间分布；选你环境最好装的那个。

**解答：**
```text
Linux 熟练用户     → perf record / perf script → flamegraph.pl
想少折腾、要 GUI  → samply record ./target/release/app
已在 Cargo 工作流 → cargo flamegraph
```

```bash
# samply 示意（安装与命令以项目 README 为准）
samply record ./target/release/myapp
```

```rust
fn main() {
    println!("profile the release binary, not cargo run without --release");
}
```

**Go 对比：**
- pprof 一条龙；Rust 更常「采样器 + 可视化」拆开。
- 概念相同：周期性打断看栈。

**记忆点：**
- 工具名不同，问的都是「CPU 在哪」。
- 先会一个，再换平台补另一个。

---

## Q7. 分配太多怎么查？（对标 heap pprof） {#q7}
**Tags:** `common` `allocation` `dhat` `heap`
**适用版本:** 工具/ crate 以文档为准

**一句话答案：**
CPU 火焰图看不出「狂分配」。用 **分配剖析**：开发期可用 **dhat**（Valgrind 工具/crate 生态）、**heaptrack**（Linux）、或带分配钩子的分析器；先确认是否无必要 `clone`/`to_string`/中间 `Vec`。

**解答：**
常见信号：

```text
- 吞吐随并发掉、CPU 不高 → 可能分配/锁
- criterion 里 bytes 分配指标异常高
- 日志里频繁 clone 大 String
```

```rust
fn main() {
    // 反模式直觉：热路径反复 to_string / format!
    let mut s = String::new();
    for i in 0..1000 {
        s.push_str(&i.to_string()); // 教学反例：大量小分配
    }
    println!("{}", s.len());
}
```

```rust
fn main() {
    // 稍好：复用缓冲
    use std::fmt::Write;
    let mut s = String::new();
    for i in 0..1000 {
        let _ = write!(&mut s, "{i}");
    }
    println!("{}", s.len());
}
```

**Go 对比：**
- **Go 怎么做**：`pprof` heap / `MemProfile`。
- **Rust 为什么不同**：无统一标准库 heap pprof；工具分散。
- **Go 程序员易踩的坑**：只看 CPU 火焰图却忽略分配。

**记忆点：**
- 慢 ≠ 一定 CPU；查分配与锁。
- 热路径少 `format!`/`clone`。

---

## Q8. Tokio 服务卡住怎么看？`tokio-console` {#q8}
**Tags:** `hot` `tokio-console` `async`
**适用版本:** tokio-console 与 Tokio feature；以当前文档为准

**一句话答案：**
异步卡顿常常是「任务不 poll / 阻塞了 worker」，不是纯 CPU 热点。启用 **tokio-console**（或等价 tracing 资源监控）看任务状态、忙闲、是否在 `spawn_blocking` 外阻塞。配合 [31-async](../31-async-programming/) 的取消与超时。

**解答：**
```toml
# 示意：按 tokio-console 文档打开 console subscriber feature
# tokio = { version = "1", features = ["full", "tracing"] }
# console-subscriber = "0.4"
```

```text
# 示意流程
# 1. 程序内初始化 console_subscriber::init();
# 2. 另开 tokio-console 客户端连接
# 3. 看：长时间 busy、未完成的 task、阻塞点
```

```rust
fn main() {
    // 经典事故：async fn 里 std::thread::sleep / 阻塞 Redis
    // 火焰图可能显示「很闲」或怪在运行时——先查是否阻塞 worker
    println!("see 31-async Q9 / Q22");
}
```

**Go 对比：**
- goroutine 泄漏用 pprof goroutine 剖面；Rust async 要看 **任务** 不是 OS 线程数。
- **Go 程序员易踩的坑**：只 `ps` 看线程数——Tokio 线程少也可能逻辑死锁/饿死。

**记忆点：**
- async 卡 → console / 超时 / 找阻塞调用。
- 不等于再加 CPU 火焰图就够。

---

## Q9. Windows 上怎么剖析？ {#q9}
**Tags:** `common` `Windows` `samply` `ETW`
**适用版本:** Windows 10/11；工具随版本变

**一句话答案：**
Linux 的 `perf` 不是默认路径。Windows 上优先试 **samply**、Visual Studio 诊断、或 **cargo-flamegraph** 文档里写明的后端；不要假设 `perf` 命令存在。WSL2 里可对 Linux 目标用熟悉的 perf/flamegraph。

**解答：**
```text
本机原生 Windows 二进制
  → samply / VS Profiler / 厂商工具

WSL2 里的 Linux 二进制
  → 与 Linux 相同：perf / flamegraph

CI 是 Linux
  → 在 CI artifact 上出图往往最省事
```

```rust
fn main() {
    println!("profile where you ship: Win vs WSL vs Linux container");
}
```

```bash
cargo build --release
# 然后用平台支持的采样器挂到 target/release/*.exe
```

**Go 对比：**
- Go pprof 跨平台较一致；Rust 采样后端更吃 OS。
- **Go 程序员易踩的坑**：教程全是 `perf`，在 PowerShell 里硬跑。

**记忆点：**
- Windows → samply/VS；或 WSL/CI 出图。
- 先确认二进制是 release。

---

## Q10. `cargo bench` 怎么只跑某一个？报告在哪？ {#q10}
**Tags:** `common` `cargo bench` `filter`
**适用版本:** Cargo；criterion 过滤语法以文档为准

**一句话答案：**
`cargo bench --bench sum` 指定 bench 目标；criterion 还可用表达式过滤用例名。报告常在 `target/criterion/`（HTML）。首次编译久是正常的。

**解答：**
```bash
cargo bench --bench sum
cargo bench --bench sum -- sum_1e6
# 具体过滤参数随 criterion 版本看 --help
```

```text
target/criterion/
  └── <bench名>/
        └── report/index.html
```

```rust
fn main() {
    // bench 目标在 Cargo.toml [[bench]] name = "sum"
    // 对应 benches/sum.rs
    println!("see 04-running Q7 / Q18 for layout");
}
```

**Go 对比：**
```bash
go test -bench=BenchmarkSum -benchmem ./...
```
- 过滤思想相同；产物目录不同。

**记忆点：**
- `--bench <name>` 选目标。
- HTML 报告在 `target/criterion/`。

---

## Q11. tracing span 能当剖析用吗？ {#q11}
**Tags:** `common` `tracing` `latency` `span`
**适用版本:** tracing 0.1.x

**一句话答案：**
**能辅助看延迟与关键路径**，尤其服务端请求级耗时；但**不是** CPU 采样火焰图的替代品。用 span 找「哪段业务慢」，用 flamegraph 找「CPU 在哪个函数」。两者常一起用。详见 [39-logging](../39-logging-and-tracing/)。

**解答：**
```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = "0.3"
```

```text
// 示意
let span = tracing::info_span!("handle_request", path = %path);
let _g = span.enter();
// ... 业务 ...
```

```rust
fn main() {
    // span = 业务时间线；flamegraph = 采样热点
    assert_ne!("tracing", "pprof");
}
```

**Go 对比：**
- OpenTelemetry / 自定义 span vs pprof：同样是两层。
- **Go 程序员易踩的坑**：只埋日志当 profiling。

**记忆点：**
- span 管「慢在哪段业务」。
- 采样管「CPU 在哪个符号」。

---

## Q12. 和 Go 工具链整表对照 + 实用检查清单 {#q12}
**Tags:** `common` `cheatsheet` `checklist`
**适用版本:** 工作流对照

**一句话答案：**
把 `-bench` 想成 criterion，把 CPU pprof 想成 flamegraph/samply，把 heap pprof 想成 dhat/heaptrack，把 goroutine 剖面想成 tokio-console。开测前勾选：release、代表性负载、`black_box`、别在 CI 把微基准当唯一门禁。

**解答：**

| Go | Rust |
|----|------|
| `go test -bench` | `cargo bench` + criterion |
| `pprof` CPU | flamegraph / samply / perf |
| `pprof` heap | dhat / heaptrack 等 |
| goroutine profile | tokio-console / 任务指标 |
| `KeepAlive` | `black_box` |
| 默认较优构建 | 记住 `--release` |

检查清单：

```text
[ ] 用 release / bench profile
[ ] 负载像生产（数据大小、并发）
[ ] 基准有 black_box
[ ] CPU 与分配分开看
[ ] async 服务查过阻塞与 console
[ ] 微基准涨跌别当唯一上线依据
```

```rust
fn main() {
    println!("measure what you ship; profile the bottleneck you observed");
}
```

**Go 对比：**
- 问题相同，工具名不同。
- 最大陷阱：debug 数字 + 无负载代表性。

**记忆点：**
- 先复现慢，再选工具。
- criterion 比快慢；火焰图找热点；console 看 async。
