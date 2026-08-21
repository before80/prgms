+++
title = "01-互操作性"
date = 2026-08-18T18:10:00+08:00
weight = 10
type = "docs"
description = "互操作性 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/libs/interop/index.html](https://microsoft.github.io/rust-guidelines/guidelines/libs/interop/index.html)

# 互操作性

## 类型是 Send (M-TYPES-SEND) {#M-TYPES-SEND}

*本条守护：可在 Tokio 中使用，以及置于运行时抽象之后。*

公开类型出于兼容性应当是 `Send`：

- 所产生的全部 future（无论显式还是隐式）必须是 `Send`
- 其他大多数类型也应当是 `Send`，但可能有例外

### Future

当显式声明 future 时，你应当确保它是、并且一直保持为 `Send`。

```rust
# use std::future::Future;
# use std::pin::Pin;
# use std::task::{Context, Poll};
#
struct Foo {}

impl Future for Foo {
    // 为你的类型显式实现 `Future`
    # type Output = ();
    #
    # fn poll(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<<Self as Future>::Output> { todo!() }
}

// 你应当断言你的类型是 `Send`
const fn assert_send<T: Send>() {}
const _: () = assert_send::<Foo>();
```

当通过 `async` 方法调用隐式返回 future 时，你也应当确保它们是 `Send`。
不必测试每一个方法，但至少应验证主要入口点。

```rust
async fn foo() { }

// TODO：我们也希望把它做成宏
fn assert_send<T: Send>(_: T) {}
_ = assert_send(foo());
```

### 普通类型

大多数普通类型应当是 `Send`，否则若跨 `.await` 点持有它们，就会感染 future，使其变成 `!Send`。

```rust
# use std::rc::Rc;
# async fn read_file(x: &str) {}
#
async fn foo() {
    let rc = Rc::new(123);      // <-- 跨 .await 点持有它会阻止
    read_file("foo.txt").await; //     该 future 成为 `Send`。
    dbg!(rc);
}
```

话虽如此，若该类型的默认用法是*瞬时的*，并且没有理由跨 `.await` 边界持有它，则它可以是 `!Send`。

```rust
# use std::rc::Rc;
# struct Telemetry; impl Telemetry { fn ping(&self, _: u32) {} }
# fn telemetry() -> Telemetry  { Telemetry }
# async fn read_file(x: &str) {}
#
async fn foo() {
    // 此处临时召唤一个假设的 Telemetry 实例并即用即弃。
    // Telemetry 为 !Send 或许可以接受。
    telemetry().ping(0);
    read_file("foo.txt").await;
    telemetry().ping(1);
}
```

> ### 💡  Send 的代价
>
> 理想情况下，应有在工作窃取运行时中为 `Send`、在每核一线程模型中为 `!Send` 的抽象，后者基于 `Rc`、`RefCell` 这类非原子类型。
>
> 实际上这类抽象并不存在，非原子情形下就无法与 Tokio 兼容。那意味着若要在每核一线程的世界里做成任何事，你都得「重新发明整个世界」。
>
> 好消息是，在大多数情况下，原子操作和无竞争锁只有在大约每 64 个字就要访问一次以上时，才会有可测影响。
>
> 
>
> ![示意图](img/M-TYPES-SEND.png)
>
> 
>
> 在热循环里操作大型 `Vec<AtomicUsize>` 是个坏主意，但在原本每核一线程的异步代码里偶尔做一次无竞争原子操作，对性能没有影响，却能换来广泛的生态兼容性。

## 提供原生逃生舱 (M-ESCAPE-HATCHES) {#M-ESCAPE-HATCHES}

*本条守护：在替代方案出现前，为不受支持的用例提供变通。*

包装原生 handle 的类型应提供 `unsafe` 逃生舱。在互操作场景中，用户可能从别处拿到原生 handle，或必须把你包装后的 handle 经 FFI 传出。为支持这些用例，你应提供 `unsafe` 转换方法。

```rust
# type HNATIVE = *const u8;
pub struct Handle(HNATIVE);

impl Handle {
    pub fn new() -> Self {
        // 通过 API 调用安全地创建 handle
        # todo!()
    }

    // 用用户从别处得到的原生 handle 构造新的 Handle。
    // 该方法还应文档化必须满足的全部安全要求。
    pub unsafe fn from_native(native: HNATIVE) -> Self {
        Self(native)
    }

    // 用于永久或临时获取原生 handle 的若干额外方法。
    pub fn into_native(self) -> HNATIVE { self.0 }
    pub fn to_native(&self) -> HNATIVE { self.0 }
}
```

## 不要泄漏外部类型 (M-DONT-LEAK-TYPES) {#M-DONT-LEAK-TYPES}

*本条守护：稳定的 API 与较低的长期维护成本。*

在可行之处，公开 API 应优先使用 `std`<sup>1</sup> 类型，而非来自外部 crate 的类型。例外应慎重考虑。

任何公开 API 中的任何类型，都将成为该 API 契约的一部分。由于默认只随发行附带 `std` 及其组成 crate，且它们带有永久稳定性保证，因此只有这些类型没有互操作风险。

一个 crate 若暴露另一 crate 的类型，就称为*泄漏*该类型。

为追求最大的长期稳定性，理论上你的 crate 不应泄漏任何类型。实际上，某些泄漏难以避免，有时甚至有益。我们建议遵循以下启发式规则：

- [ ] 若能避免，就不要泄漏第三方类型
- [ ] 若你属于伞形 crate，<sup>2</sup> 则可自由泄漏兄弟 crate 的类型。
- [ ] 在相关 feature 标志之后，可以泄漏类型（例如 `serde`）
- [ ] 不带 feature 时，*仅当*能带来*实质性收益*才可泄漏。最常见的情形是：基于这些类型，与 Rust 生态中其他重要部分实现互操作。

> <sup>1</sup> 在罕见情况下，例如从嵌入式调用的高性能库，你甚至可能要把自己限制在只用 `core`。
>
> <sup>2</sup> 例如，`runtime` crate 可能是 `runtime_rt`、`runtime_app` 与 `runtime_clock` 的伞。由于期望用户只与伞交互，兄弟之间可以互相泄漏类型。

## 项来自其原始 crate (M-FOREIGN-REEXPORTS) {#M-FOREIGN-REEXPORTS}

*本条守护：明确无歧义的类型身份。*

crate 一般不应再导出其他 crate 的项。例如，若你的 crate 含有方法 `foo::download(url: bar::Url)`，你不应在 `foo` 内部做 `pub use bar::Url`。这样可避免上下文中可能出现几十个别名，对用户和智能体都容易混淆，尤其当这些别名与其他 crate 中同名但实际不同的类型混在一起时。

当 crate 接受或返回某个第三方 crate 中定义的类型时，期望用户直接依赖该第三方 crate，并从那里导入该类型。不过本规则有若干合理例外：

- 伞形 crate（参见 [M-DONT-LEAK-TYPES](./#M-DONT-LEAK-TYPES)）按定义会再导出其他类型
- 因技术原因拆分的 crate（例如从 `foo` 导出 `foo_core::Url`）
- 为提供稳定路径而使用宏，例如经由某个隐藏的 `foo::__private::Url`

## 可行时接受 `impl AsRef<>` (M-IMPL-ASREF) {#M-IMPL-ASREF}

*本条守护：调用方可灵活使用自有类型。*

在**函数**签名中，对具有 [clear reference hierarchy](https://doc.rust-lang.org/stable/std/convert/trait.AsRef.html#implementors) 的类型，在你不需要取得所有权、或对象创建相对廉价时，接受 `impl AsRef<T>`。

| 不要用…… | 而应接受…… |
| --- | --- |
| `&str`、`String` | `impl AsRef<str>` |
| `&Path`、`PathBuf` | `impl AsRef<Path>` |
| `&[u8]`、`Vec<u8>` | `impl AsRef<[u8]>` |

```rust
# use std::path::Path;
// 务必使用 `AsRef`，该函数不需要所有权。
fn print(x: impl AsRef<str>) {}
fn read_file(x: impl AsRef<Path>) {}
fn send_network(x: impl AsRef<[u8]>) {}

// 需要进一步分析。这些情况下函数需要
// 某个 `String` 或 `Vec<u8>` 的所有权。如果它们是
// 「低频、低量」函数，`AsRef` 人体工学更好；
// 否则接受 `String` 或 `Vec<u8>` 性能更好。
fn new_instance(x: impl AsRef<str>) -> HoldsString {}
fn send_to_other_thread(x: impl AsRef<[u8]>) {}
```

相对地，**类型**一般不应被这些约束感染：

```rust
// 通常不合适。出于性能原因可能有例外，
// 但那些例外不应暴露给用户。
struct User<T: AsRef<str>> {
    name: T
}

// 更好
struct User {
    name: String
}
```

## 可行时接受 `impl RangeBounds<>` (M-IMPL-RANGEBOUNDS) {#M-IMPL-RANGEBOUNDS}

*本条守护：指定范围时灵活且清晰。*

接受数字范围的函数必须使用 `Range` 类型或 trait，而不是手写参数：

```rust
// 不好
fn select_range(low: usize, high: usize) {}
fn select_range(range: (usize, usize)) {}
```

此外，能处理任意范围的函数应接受 `impl RangeBounds<T>`，而不是 `Range<T>`。

```rust
# use std::ops::{RangeBounds, Range};
// 调用方必须写成 `select_range(1..3)`
fn select_range(r: Range<usize>) {}

// 调用方可以写成
//     select_any(1..3)
//     select_any(1..)
//     select_any(..)
fn select_any(r: impl RangeBounds<usize>) {}
```

## 可行时接受 `impl 'IO'`（sans IO） (M-IMPL-IO) {#M-IMPL-IO}

*本条守护：业务逻辑与 I/O 解耦，具备 N×M 可组合性。*

只需在初始化期间执行一次性 I/O 的函数和类型，应按 "[sans-io](https://www.firezone.dev/blog/sans-io)" 来写，
并接受某个 `impl T`（其中 `T` 是合适的 I/O trait），从而把 I/O 工作外包给另一种类型：

```rust
// 不好：调用方必须提供 File 才能解析给定数据。若数据
// 来自网络，就得先写到磁盘。
fn parse_data(file: File) {}
```

```rust
// 好得多，可接受
// - File、
// - TcpStream、
// - Stdin、
// - &[u8]、
// - UnixStream、
// ……以及更多。
fn parse_data(data: impl std::io::Read) {}
```

同步函数应使用 [`std::io::Read`](https://doc.rust-lang.org/std/io/trait.Read.html) 和
[`std::io::Write`](https://doc.rust-lang.org/std/io/trait.Write.html)。面向不止一个运行时的异步*函数*应使用
[`futures::io::AsyncRead`](https://docs.rs/futures/latest/futures/io/trait.AsyncRead.html) 及类似项。
需要执行运行时特定、持续 I/O 的*类型*应遵循 [M-RUNTIME-ABSTRACTED]。

[M-RUNTIME-ABSTRACTED]: ./#M-RUNTIME-ABSTRACTED
