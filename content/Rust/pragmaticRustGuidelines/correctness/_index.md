+++
title = "第6章 正确性"
date = 2026-08-18T18:10:00+08:00
weight = 80
type = "docs"
description = "正确性指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/correctness/index.html](https://microsoft.github.io/rust-guidelines/guidelines/correctness/index.html)

# 正确性

## Unsafe 需要理由，应当避免 (M-UNSAFE) {#M-UNSAFE}

*本条守护：内存安全与最小攻击面。*

你必须有正当理由才能使用 `unsafe`。唯一正当的理由是

1) 新颖抽象，例如新的智能指针或分配器，
1) 性能，例如试图调用 `.get_unchecked()`，
1) FFI 与平台调用，例如调用 C 或内核，...

Unsafe 代码降低了编译器提供的护栏，把编译器的部分职责转给了程序员。最终代码的正确性主要依赖在代码审查中抓住所有失误，而这容易出错。Unsafe 代码中的失误可能引入高严重性安全漏洞。

你不得使用临时性的 `unsafe` 来

- 缩短本已高性能且安全的 Rust 程序，例如通过 `transmute`「简化」枚举转换，
- 绕过 `Send` 及类似约束，例如写 `unsafe impl Send ...`，
- 通过 `transmute` 及类似手段绕过生命周期要求。

此处的临时性指嵌入在本不相关代码中的 `unsafe`。当然，创建设计得当、健全的抽象来做这些事是允许的。

无论如何，`unsafe` 都必须遵循下列指南。

### 新颖抽象

- [ ] 确认没有既有替代方案。若有，优先用它。
- [ ] 你的抽象必须最小且可测试。
- [ ] 必须针对[「对抗性代码」](https://cheats.rs/#adversarial-code)加固并测试，尤其是
  - 若接受闭包，在闭包 panic 时它们必须变为无效（例如中毒）
  - 它们必须假定任何安全 trait 都可能行为不端，尤其是 `Deref`、`Clone` 和 `Drop`。
- [ ] 任何 `unsafe` 的使用都必须附带说明其安全性的纯文本推理
- [ ] 必须通过 [Miri](https://github.com/rust-lang/miri)，包括对抗性测试用例
- [ ] 必须遵循所有其他 [unsafe 代码指南](https://rust-lang.github.io/unsafe-code-guidelines/)

### 性能

- [ ] 出于性能原因使用 `unsafe` 应仅在基准测试之后进行
- [ ] 任何 `unsafe` 的使用都必须附带说明其安全性的纯文本推理。这既适用于
  调用 `unsafe` 方法，也适用于提供 `_unchecked` 方法。
- [ ] 相关代码必须通过 [Miri](https://github.com/rust-lang/miri)
- [ ] 你必须遵循 [unsafe 代码指南](https://rust-lang.github.io/unsafe-code-guidelines/)

### FFI

- [ ] 我们建议你使用成熟的互操作库以避免 `unsafe` 构造
- [ ] 你必须遵循 [unsafe 代码指南](https://rust-lang.github.io/unsafe-code-guidelines/)
- [ ] 你必须为生成的绑定编写文档，明确哪些调用模式是允许的

### 延伸阅读

- [Nomicon](https://doc.rust-lang.org/nightly/nomicon/)
- [Unsafe Code Guidelines](https://rust-lang.github.io/unsafe-code-guidelines/)
- [Miri](https://github.com/rust-lang/miri)
- ["Adversarial code"](https://cheats.rs/#adversarial-code)

## 所有代码必须是健全的 (M-UNSOUND) {#M-UNSOUND}

*本条守护：可预期的运行时行为，无缺陷与不兼容。*

不健全（unsound）的代码是表面上_安全_、但从其他安全代码调用时——或自行——可能产生未定义行为的代码。

> ### 💡 「安全」的含义
>
> 术语_安全_（safe）与 `unsafe` 在 Rust 中是技术术语。
>
> 若函数签名未将其标为 `unsafe`，则该函数是_安全的_。尽管如此，_安全_函数仍可能很危险
> （例如 `delete_database()`），而 `unsafe` 函数在正确使用时通常相当无害（例如 `vec.get_unchecked()`）。
>
> 因此，若函数看起来_安全_（即未标为 `unsafe`），但其_任何_调用方式都会导致未定义行为，则该函数是_不健全的_。
> 这要以最严格的意义理解。即便引发未定义行为只是「遥远、理论上的可能」、且需要「奇怪的代码」，
> 该函数仍是不健全的。
>
> 另见 [Unsafe, Unsound, Undefined](https://cheats.rs/#unsafe-unsound-undefined)。

```rust
// 「安全地」转换类型
fn unsound_ref<T>(x: &T) -> &u128 {
    unsafe { std::mem::transmute(x) }
}

// 「巧妙技巧」以绕过缺失的 `Send` 约束。
struct AlwaysSend<T>(T);
unsafe impl<T> Send for AlwaysSend<T> {}
unsafe impl<T> Sync for AlwaysSend<T> {}
```

不健全的抽象绝不可接受。若你无法安全地封装某事，则必须改为暴露 `unsafe` 函数，并文档说明正确行为。

无例外

你可以在有充分理由时违反大多数指南，但本条没有例外：不健全的代码永远不可接受。

> ### 💡 关键在模块边界
>
> 注意健全性边界等于模块边界！在一个本身安全的抽象中，
> 完全可以有依赖**同一模块内**别处所保证行为的安全函数。
>
> ```rust
> struct MyDevice(*const u8);
>
> impl MyDevice {
>     fn new() -> Self {
>         // 正确初始化实例 ...
>         # todo!()
>     }
>
>     fn get(&self) -> u8 {
>         // 完全可以依赖 `self.0` 有效，尽管这个
>         // 函数自身无法验证这一点。
>         unsafe { *self.0 }
>     }
> }
>
> ```

## Unsafe 意味着未定义行为 (M-UNSAFE-IMPLIES-UB) {#M-UNSAFE-IMPLIES-UB}

*本条守护：语义一致，且无警告疲劳。*

标记 `unsafe` 仅可应用于函数与 trait，且仅当误用意味着未定义行为（UB）风险时。
不得用它标记因其他原因而调用危险的函数。

```rust
// 对 unsafe 的有效使用
unsafe fn print_string(x: *const String) { }

// 对 unsafe 的无效使用
unsafe fn delete_database() { }
```

## Panic 表示「停止程序」 (M-PANIC-IS-STOP) {#M-PANIC-IS-STOP}

*本条守护：健全性与可预期性。*

Panic 不是异常。相反，它们建议立即终止程序。

尽管你的代码必须是[_最低限度_ panic 安全](https://doc.rust-lang.org/nomicon/exception-safety.html)的（即存活下来的 panic 不得导致未定义状态），
调用 panic 意味着_本程序现在应停止_。以下做法无效：

- 用 panic 向上游传达（错误），
- 用 panic 处理自找的错误条件，
- 假定 panic 会被捕获，即便是被你自己的代码。

例如，若调用你的应用在 `Cargo.toml` 中编译配置为

```toml
[profile.release]
panic = "abort"
```

那么任何 panic 调用都会让本可正常运行的程序无谓中止。合法的 panic 理由是：

- 遇到编程错误时，例如 `x.expect("must never happen")`，
- 在 const 上下文中调用的任何内容，例如 `const { foo.unwrap() }`，
- 用户要求时，例如你自己提供 `unwrap()` 方法，
- 遇到中毒时，例如对锁结果调用 `unwrap()`（锁中毒表示另一线程已经 panic）。

上述任一情况都直接或间接与编程错误相关。

## 检测到的编程错误是 panic 而非 error (M-PANIC-ON-BUG) {#M-PANIC-ON-BUG}

*本条守护：可控的错误处理与运行时一致性。*

作为上文 [M-PANIC-IS-STOP] 的延伸，当检测到不可恢复的编程错误时，
库与应用必须 panic，即请求终止程序。

在这些情况下，不应引入或返回 `Error` 类型，因为此类错误在运行时无法采取行动。

契约违反——即破坏库内部或调用方的不变量——是编程错误，因此必须 panic。

然而，何为违反取决于情境。API 并不被期望特地去检测它们，因为此类
检查可能不可能或代价高昂。在本已存在的检查中遇到 `must_be_even == 3` 显然值得
panic，而函数 `parse(&str)` 显然必须返回 `Result`。若有疑问，我们建议你从标准库汲取灵感。

```rust
// 一般而言，带有不良参数的函数必须要么
// - 忽略某参数和/或返回错误结果
// - 通过 Result 或类似方式发出问题信号
// - Panic
// 若在此 `divide_by` 中我们看到 y == 0，panic 是
// 正确做法。
fn divide_by(x: u32, y: u32) -> u32 { ... }

// 然而，省略此类检查并返回未指明（但非未定义）的结果
// 也可以允许。
fn divide_by_fast(x: u32, y: u32) -> u32 { ... }

// 此处传入无效 URI 不是契约违反。
// 由于解析本质上可失败，必须返回 Result。
fn parse_uri(s: &str) -> Result<Uri, ParseError> { };

```

> ### 💡 做到「构造即正确」
>
> 虽说在检测到编程错误时 panic 是「最不坏的选择」，你的 panic 仍可能毁掉别人的一天。
> 对任何否则会 panic 的用户输入或调用序列，你也应探索能否用类型
> 系统彻底避免会 panic 的代码路径。

[M-PANIC-IS-STOP]: ./#M-PANIC-IS-STOP

## 从 panic 继续执行是最后手段 (M-PANIC-CONTINUATION) {#M-PANIC-CONTINUATION}

*本条守护：状态完整性，免于细微缺陷。*

通过 `catch_unwind()` 从 panic 恢复是最后手段，且一般必须随后受控地重启应用。

Panic 表示程序已进入不可恢复状态（对照 [M-PANIC-IS-STOP](./#M-PANIC-IS-STOP) 与 [M-PANIC-ON-BUG](./#M-PANIC-ON-BUG)）。库代码尤其不应试图捕获 panic 并继续执行，因为有观察到否则不可能出现的状态的风险：

```rust
thread_local! {
    static ALWAYS_EQUAL: RefCell<(i32, i32)> = RefCell::new((0, 0));
}

fn main() {
    let _ = panic::catch_unwind(|| {
        ALWAYS_EQUAL.with_borrow_mut(|p| {
            p.0 += 1;        
            panic!("Assume some user-provided closure failed here");  
            p.1 += 1;
        });
    });

    ALWAYS_EQUAL.with_borrow(|p| {
        assert_eq!(p.0, p.1);  // 已破坏！
    });
}
```

虽然上面的例子略显刻意，被捕获的 panic 的副作用与交互可能更难识别，波及范围可能很大，且十分细微。

许多无关任务同时进行的系统（例如服务器请求处理器）可以按请求使用 `catch_unwind`，但在请求处理器导致 panic 后仍应推动应用重启。此处 `catch_unwind` 的目的不是无限继续执行，而是让其他所有请求优雅结束。

## 自定义 panic 要有有用的消息 (M-PANIC-MESSAGE) {#M-PANIC-MESSAGE}

*本条守护：更快诊断缺陷。*

当代码有意 panic 时（通过 `panic!`、`assert!`、`unreachable!`、`todo!` 或类似方式），必须有消息以清楚说明出了什么问题，并在适用时包含相关值。

```rust
// 不好，该 panic 几乎没给开发者可采取行动的信息。
assert!(buffer.len() >= HEADER_SIZE);

// 好，消息包含原因与实际值。
assert!(buffer.len() >= HEADER_SIZE, "buffer too small for header: got {} bytes, need {HEADER_SIZE}", buffer.len());
```

与 API 误用相关的消息应对最终用户有用。指示缺陷的消息应对作为作者的你、或你之后维护该项目的人有帮助，以便快速定位根本原因。

测试中的 panic 消息一般不需要。
