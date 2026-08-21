+++
title = "第7章 性能"
date = 2026-08-18T18:10:00+08:00
weight = 90
type = "docs"
description = "性能指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/performance/index.html](https://microsoft.github.io/rust-guidelines/guidelines/performance/index.html)

# 性能

## 优化吞吐量，避免空转 (M-THROUGHPUT) {#M-THROUGHPUT}

*本条守护：规模化下的 COGS（成本）节省。*

你应当为吞吐量优化你的库，关键指标之一应当是 _每 CPU 周期处理的条目数_。

这并不意味着忽视延迟——毕竟吞吐量可以靠扩展换取，延迟却不行。然而，
在多数情况下，你不应为延迟付出 _空转_ 的代价：那往往来自逐条处理、高争用锁以及频繁的任务切换。

理想情况下，你应当

- 预先划分合理的工作块，
- 让各个线程与任务独立处理各自的工作切片，
- 没有工作时休眠或让出，
- 自行设计面向批处理的 API，
- 在可用时通过批处理 API 执行工作，
- 在漫长的单个条目内部、或在批处理块之间让出（见 [M-YIELD-POINTS]），
- 利用 CPU 缓存以及时间局部性与空间局部性。

你不应当：

- 为了更快收到单个条目而热自旋，
- 在可以批处理时仍对单个条目做功，
- 为了平衡单个条目而做 work stealing 或类似手段。

仅当共享的成本低于重新计算的成本时，才应使用共享状态。

[M-YIELD-POINTS]: ./#M-YIELD-POINTS

## 尽早识别、剖析并优化热路径 (M-HOTPATH) {#M-HOTPATH}

*本条守护：高性能代码。*

你应当在开发早期识别你的 crate 是否与性能或 COGS（成本）相关。若相关：

- 识别热路径并围绕它们建立基准测试，
- 定期运行分析器，收集 CPU 与分配方面的洞察，
- 记录或沟通最敏感于性能的区域。

基准测试我们推荐 [criterion](https://crates.io/crates/criterion) 或 [divan](https://crates.io/crates/divan)。
若可能，基准测试不应只测量经过的墙钟时间，还应测量所有线程上的 CPU 时间总和（这不幸地
需要手工处理，常见基准工具开箱并不支持）。

在 Windows 上剖析 Rust 可开箱使用 [Intel VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html)
与 [Superluminal](https://superluminal.eu/)。不过，要获得有意义的 CPU 洞察，你应在 `Cargo.toml` 中为基准启用调试符号：

```toml
[profile.bench]
debug = 1
```

记录最敏感于性能的区域，有助于其他贡献者做出更好决策。这可以很简单，例如
分享你最近剖析热点的截图。

### 延伸阅读

- [Performance Tips](https://cheats.rs/#performance-tips)

> ### 💡 能快多少？
>
> 我们见过的一些最常见的「与语言相关」的问题包括：
>
> - 频繁重新分配，尤其是克隆、增长或用 `format!` 拼装的字符串，
> - 相对 bump 分配等而言过于短命的分配，
> - 克隆 String 与集合带来的内存拷贝开销，
> - 对相同数据结构反复重新哈希
> - 在碰撞抗性并非问题时仍使用 Rust 的默认 hasher
>
> 据经验，在热路径上仅解决部分此类 `String` 问题，我们就见过约 15% 的基准提升，
> 高度优化的版本似乎可达约 50%。

## 长时间任务应有让出点 (M-YIELD-POINTS) {#M-YIELD-POINTS}

*本条守护：所有任务都能公平获得 CPU 时间。*

若你执行长时间计算，其中应包含 `yield_now().await` 让出点。

你的 future 可能运行在无法绕过阻塞或长时间任务的运行时中。即便如此，这类任务仍
被视为糟糕设计并带来运行时开销。若你的复杂任务会定期做 I/O，它只需利用这些 await 点自行抢占：

```rust
async fn process_items(items: &[items]) {
    // 持续处理条目，运行时会自动抢占你。
    for i in items {
        read_item(i).await;
    }
}
```

若你的任务执行长时间 CPU 操作且其间没有穿插 I/O，则应改为按固定间隔协作式让出，以免饿死并发操作：

```rust
async fn process_items(zip_file: File) {
    let items = zip_file.read().async;
    for i in items {
        decompress(i);
        yield_now().await;
    }
}
```

若单个操作的数量与耗时难以预测，你应使用诸如 `has_budget_remaining()` 及相关
API 来查询宿主运行时。

> ### 💡 多久让出一次？
>
> 在 thread-per-core 模型中，任务切换的开销必须与饿死无关任务所带来的系统性影响相权衡。
>
> 在假定运行时任务切换耗时为数百纳秒、外加丢失 CPU 缓存的开销时，
> 两次切换之间的连续执行应足够长，使切换成本可忽略（<1%）。
>
> 因此，在让出点之间执行 10–100μs 的 CPU 密集工作会是一个不错的起点。

## 尽可能复用分配 (M-MEM-REUSE) {#M-MEM-REUSE}

*本条守护：低分配开销与快速热路径。*

设计 API 时，你应允许用户持有可复用资源。在你自己的代码中，有可用资源时也应加以利用。

热循环内反复分配的成本可能很大，而从用户视角，除非经过剖析，否则往往看不见：

```rust
// 不好：API 设计迫使每个元素都新分配。
for id in ids {
    let value = db.get(id);
}
```

这类 API 风格可作为便利存在，但应是辅助性的。核心 API 应允许用户拥有底层对象并复用它：

```rust
// 更好：让用户决定是否需要新分配。
let mut value = Value::new();
for id in ids {
    db.get_in(id, &mut value);
}
```

可复用类型上复用自身的典型方法是 `.clear()`，这在许多 `std` 类型上都能找到。该模式有多种变体。简单情况下，用户自有类型可以直接持有已有的、可复用的集合：

```rust
struct Value {
    data: Vec<u8>
}
```

在重量级、深度嵌套的库中，值得传入 bump 风格的 `Arena`，或将其封装进用户类型，以便在整个调用栈中使用：

```rust
struct Query {
    arena: Arena,
    request: Request,
    data: Vec<u8>    
}

fn client_do_work(query: &mut Query) {
    let request = rewrite_request(&query.request, &query.arena);
    get_in(request, &mut query.data);
}
```

## 库的遥测不得拖垮性能 (M-LOG-OVERHEAD) {#M-LOG-OVERHEAD}

*本条守护：诊断期间低开销的遥测。*

发出遥测的库代码应确保这样做不会在热路径上显著影响吞吐量或延迟。

向第三方提供、会发出日志或指标的 crate，应假定遥测会长期开启，或在负载下开启。因此应谨慎控制所发事件的量与开销，使其合理，且不会造成过度的性能退化。

热内层循环最好完全不发出遥测。若无法避免，发出的事件应轻量且避免分配（例如 `format!` 字符串拼接）。

```rust
// 不好：每条消息都打日志，并触发基于分配的格式化。
for m in messages {
    log(format!("Emitting message {}", m.id()))
}

// 更好：避免按消息分配。
for m in messages {
    log(("Emitting message", m.id()))
}

// 最佳：若可能，让遥测用户离线重建发生了什么
log(("Processing message batch", messages.batch_id()))
for m in messages { ... }
```

## 嵌套类型层次应避免不必要的间接 (M-AVOID-INDIRECTION) {#M-AVOID-INDIRECTION}

*本条守护：快速、对缓存友好的内存访问。*

热类型应避免嵌套的堆间接，并考虑将热的、可缓存的深层字段上提，以改善缓存利用率。  

虽然黄金标准是做基准测试，但在将 C# 代码移植到 Rust 时反复出现的模式是：反射性地对嵌套类型加 `Arc`，往往层层套叠。虽然在真正需要被多个所有者共享的很宽或很重的类型上这说得通，但当必须顺序执行多轮 DRAM 查找时，该模式会毁掉访问延迟。

在并非严格需要嵌套共享所有权时，通常更好的做法是从局部的、内嵌的数据起步，并上提可缓存字段。

```rust
// 不好：`print`（假定它相当热）需要 2 次间接
// 才能查询是否启用。
struct Item {
    config: Arc<Config>,
    payload: Payload,
}

struct Config {
    feature: Arc<Feature>
}

impl Item {
    fn print(&self) {
        if self.config.feature.is_enabled() { ... }
    }
}

// 更好：`enabled` 就在附近，一旦调用 `print`
// 很可能立即可用。
struct Item {
    config: Arc<Config>,
    payload: Payload,
    enabled: bool,
}

impl Item {
    fn print(&self) {
        if self.enabled { ... }
    }
}

```

## 不可变自有序列使用 boxed slice 与 string (M-BOX-DST) {#M-BOX-DST}

*本条守护：低内存消耗与良好的缓存利用率。*

频繁使用的、内部的、构造后不会再调整大小的不可变序列，应存为 `Box<[T]>`、`Arc<str>` 或类似形式，而非原来的 `Vec<T>` 或 `String` 对应物。

常规可增长集合由 `(ptr, len, capacity)` 三元组组成。将它们转为 boxed slice 会使其不可变、执行 [shrink-to-fit](./#M-SHRINK-TO-FIT)，并丢弃 `capacity` 位，使句柄大小减少 1/3。要使该模式有用，应满足以下前提：

- 该序列应被频繁实例化（例如实例数 >1000），
- 它必须是不可变的，
- 它不应对外可见，即普通用户只需处理 `&str` 或类似类型。

某些集合提供了专用方法，例如 `String::into_boxed_str`。

```rust
// 不好：条目很多时浪费空间，并使
// 遍历最终更慢。
struct Data {
    ids: Vec<String>
}

// 更好：降低内存消耗，并把更多元素
// 装进缓存。
struct Data {
    ids: Vec<Box<str>>
}
```

## 构建完成后收缩集合以贴合容量 (M-SHRINK-TO-FIT) {#M-SHRINK-TO-FIT}

*本条守护：最小内存占用。*

若大型、长生命周期、可增长的集合（如 `Vec` 或 `String`）在构建时没有精确预留大小（参见 [M-INITIAL-CAPACITY](./#M-INITIAL-CAPACITY)），则在存储前应通过 `shrink_to_fit` 收缩结果集合。

许多 Rust 集合在迭代添加元素时按二的幂增长。最坏情况下，集合因此可能使用约所需内存的 2 倍。

```rust
// 不好：长生命周期对象最终可能使用 2 倍所需内存。
let mut long_lived = Vec::new();
for x in large_iter {
    long_lived.push(x);
}

// 更好：释放多余内存。
long_lived.shrink_to_fit();
```

注意：这不适用于经由 `into_boxed_*` 及其同类完成的转换（参见 [M-BOX-DST](./#M-BOX-DST)），因为它们通常在转换前已经收缩。

## 尽可能使用快速 hasher (M-FAST-HASHER) {#M-FAST-HASHER}

*本条守护：哈希性能。*

在对可信的内部键做哈希时，优先使用快速的非密码学 hasher（例如 `foldhash`、`FxHash`），而非标准库默认值。

Rust 的默认 hasher 对不可信用户输入具有合理的 DoS 安全性，但这有性能代价。若你可以信任键不会被恶意构造以撑爆单个桶，自定义快速 hasher 可带来显著性能收益。

```rust
// 不好：对我们控制的键使用默认 hasher。
let lookup = HashMap::<UserID, Data>::with_capacity(1024);

// 更好：对内部键使用更快的 foldhash。
let lookup = foldhash::HashMap<UserID, Data>::with_capacity(1024);
```

## 创建集合时给予足够初始容量 (M-INITIAL-CAPACITY) {#M-INITIAL-CAPACITY}

*本条守护：高效的集合创建。*

若在构造时已知集合（`Vec`、`String`、`HashMap`、`HashSet` 等）的最终或近似大小，应通过 `with_capacity` 创建，而非 `new` 或 `default`。

未指定容量创建的集合，在初始化过程中可能多次重新分配，其中也包括拷贝内容。以足够容量创建它们，可完全避免这种无谓开销。

```rust
// 不好：很可能多次重新分配并拷贝内容。
let mut rval = Vec::new();
for x in &other {
    rval.push(convert(x));
}

// 更好：一开始就以足够容量创建集合。
let mut rval = Vec::with_capacity(other.len());
for x in &other {
    rval.push(convert(x));
}
```

由迭代器驱动的构造（`collect`）通过 `size_hint` 继承该行为；在可能时应优先于手工 `push` 循环：

```rust
// 理想：看起来更干净且性能好
let rval: Vec<_> = other.iter().map(convert).collect();
```

## 热路径 `async` 函数减小栈尺寸 (M-ASYNC-STACK-SIZE) {#M-ASYNC-STACK-SIZE}

*本条守护：较小的 async 栈尺寸与低 memcpy 开销。*

热路径上标记为 `async` 的函数应跟踪其 future 大小，并采取以下一项或多项措施以降低影响：

- 减小参数与返回值类型的大小，
- 减小跨越 `.await` 点所持有条目的类型大小，
- 返回 `impl Future`，并将准备逻辑从 `async {}` 捕获中抽出。

> ### 💡 Future 的「栈」大小
>
> 在 Future 中，人们天真地以为是 _它们的栈_ 的东西，实际上是底层更复杂机制的一部分。
>
> 仅在两个 `.await` 点之间短暂存活的普通局部变量，仍停留在运行时线程的常规栈上。然而，任何跨越 `.await` 点存活的局部变量，或构造时传入的参数，都会成为该 Future 状态机类型的一部分；而该类型的布局目前尚未优化到应有水平。
>
> 这不仅可能在创建或装箱 Future 时引起栈到堆的 memcpy，还可能迫使相关 async 函数在假想的最深嵌套跨 async 调用栈上预留很大的前置栈尺寸（顺便说一句，这也是它们不能简单递归的原因）。
>
> ```rust
> async fn foo(_large: Large) {
>     let within_future = [0_u8; 1024]; // 跨越下方 .await，嵌入 `foo` 类型
>     let on_stack = [0_u8; 1024]; // 不跨越 .await 点，活在栈上
>     let sneaky = Droppable::with_size(1024); // 偷偷跨越 .await 点！
>     dbg!(&on_stack, &sneaky);
>     bar(&within_future).await;
>     dbg!(&within_future);
>     // <- `sneaky` 在此丢弃，尽管别处并未使用！
> }
> 
> let future = foo(Large::new()); // `Large` 嵌入 `foo` 类型，
>                                 // 撑大其尺寸，即便根本
>                                 // 未被使用。
> 
> // 此处，尽管 `foo` 尚未运行，我们也可能消耗多达 `Large` +
> // 2kb 的本线程栈内存。一旦 spawn，会 memcpy 到
> // 运行时 Task 结构：
> rt.spawn(future);
>```

对许多 async 函数而言这不是问题，因为其关联的 `Future` 成本可忽略。然而，热路径上使用的、被频繁调用或实例化的函数（例如每秒数千次调用或并发任务）可能会从监控与优化中受益。

热 future 应通过 `size_of_val` 跟踪：

```rust
async fn hot() { ... }

#[test]
fn has_reasonable_size() {
    let f = hot();
    assert!(size_of_val(&f) < ...); // 首次运行时确定取值 / 上限。
}
```

然后考虑以下组合：

```rust
// 1) 改为返回 `impl Future`，这可防止大参数
//    感染 future 大小，等等。
fn hot(args: Args) -> impl Future<Output = Result<T>> { 
    // 2) 若不需要 async 功能，在 async 上下文外
    //    处理参数。
    let args = args.do_something(); 

    if args.invalid() {
        // 3) 用 `Either` 返回单一 `impl Future` 类型，
        //    否则你得发明新类型。
        async { Err(InvalidArgs) }.left_future() 
    } else {
        // 4) 通过 future 辅助函数串联调用，这同样
        //    可防止沉重的局部变量穿过状态机。
        read(args).then(|x| foo(x)).right_future() 
    }
}
```
