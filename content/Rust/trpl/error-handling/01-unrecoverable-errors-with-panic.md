+++
title = "9.1 用 panic! 处理不可恢复错误"
date = 2026-08-05T08:44:00+08:00
weight = 38
type = "docs"
description = "用 panic! 处理不可恢复错误，并阅读回溯信息定位问题"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 panic! 处理不可恢复错误 {#panic}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch09-01-unrecoverable-errors-with-panic.html](https://doc.rust-lang.org/stable/book/ch09-01-unrecoverable-errors-with-panic.html)


## 用 `panic!` 处理不可恢复错误

　　有时代码里会发生你无能为力的坏事。这时可以用 Rust 的 `panic!` 宏。实践中引发 panic 的方式有两种：一是执行了会让代码 panic 的操作（例如访问数组越界），二是显式调用 `panic!` 宏。无论哪种，都会在程序中引发 panic。默认情况下，这些 panic 会打印失败信息、展开（unwind）并清理栈，然后退出。你也可以通过环境变量让 Rust 在 panic 时显示调用栈，以便更容易定位 panic 的来源。

> ### 面对 Panic：展开栈，还是直接中止？
>
> 默认情况下，发生 panic 时程序会开始*展开（unwinding）*：Rust 沿栈向上回溯，并清理途经的每个函数中的数据。不过回溯与清理代价不小，因此 Rust 也允许你选择立刻*中止（abort）*——不做清理就结束程序。
>
> 程序占用的内存随后需要由操作系统回收。若你希望生成的二进制尽可能小，可以在 _Cargo.toml_ 相应的 `[profile]` 段中加入 `panic = 'abort'`，把 panic 时的行为从展开改为中止。例如，若希望在 release 模式下 panic 时中止，可添加：
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

　　我们先在一个简单程序里调用 `panic!`：

**文件名：`src/main.rs`**
```rust
fn main() {
    panic!("crash and burn");
}
```

　　运行程序时，你会看到类似这样的输出：

```console
$ cargo run
   Compiling panic v0.1.0 (file:///projects/panic)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.25s
     Running `target/debug/panic`

thread 'main' (6018279) panicked at src/main.rs:2:5:
crash and burn
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　对 `panic!` 的调用产生了最后两行的错误信息。第一行显示我们的 panic 消息，以及源码中发生 panic 的位置：_src/main.rs:2:5_ 表示是 _src/main.rs_ 文件的第 2 行、第 5 个字符。

　　本例中，指出的那一行就是我们自己的代码；打开该行就能看到 `panic!` 宏调用。另一些情况下，`panic!` 可能出现在我们所调用的代码里，错误信息报告的文件名与行号会是别人代码中调用 `panic!` 的位置，而不是最终导致这次调用的那一行我们自己的代码。

　　我们可以利用 `panic!` 调用所经过的函数回溯（backtrace），找出自己代码里引发问题的部分。为理解如何使用 `panic!` 回溯，我们再看一个例子：这次 `panic!` 来自库代码，根因是我们代码里的 bug，而不是我们直接调用了该宏。示例 9-1 尝试访问向量中超出有效索引范围的元素。

**文件名：`src/main.rs`**
```rust
fn main() {
    let v = vec![1, 2, 3];

    v[99];
}
```

**示例 9-1：尝试访问向量末尾之后的元素，会引发对 `panic!` 的调用**

　　这里我们尝试访问向量的第 100 个元素（索引从 0 开始，因此是索引 99），但向量只有三个元素。这种情况下 Rust 会 panic。使用 `[]` 本应返回一个元素；若传入无效索引，Rust 无法返回任何“正确”的元素。

　　在 C 中，读取超出数据结构末尾的内存是未定义行为。你可能读到内存中对应那个“元素”位置上碰巧存在的内容，即便那块内存并不属于该结构。这叫做*缓冲区过度读取（buffer overread）*：若攻击者能操纵索引，读到本不该访问、却紧跟在结构之后的数据，就可能造成安全漏洞。

　　为防止这类漏洞，若你尝试读取不存在的索引处的元素，Rust 会停止执行并拒绝继续。我们试一下：

```console
$ cargo run
   Compiling panic v0.1.0 (file:///projects/panic)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.27s
     Running `target/debug/panic`

thread 'main' (6017887) panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

　　这条错误指向 _main.rs_ 的第 4 行，也就是我们尝试访问 `v` 中索引 99 的地方。

　　`note:` 那一行提示：可以设置 `RUST_BACKTRACE` 环境变量，获取导致错误的确切回溯。*回溯*是到达当前点所调用过的全部函数的列表。Rust 中的回溯读法与其他语言类似：关键是从顶部往下读，直到看到你自己编写的文件——那里往往就是问题起源。该位置之上是你的代码所调用的代码；之下是调用你代码的代码。这些前后文可能包含 Rust 核心库、标准库，或你使用的 crate。我们把 `RUST_BACKTRACE` 设为除 `0` 以外的任意值来获取回溯。示例 9-2 展示了类似你会看到的输出。


```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

**示例 9-2：设置环境变量 `RUST_BACKTRACE` 后，`panic!` 调用生成的回溯**

　　输出很长！你看到的具体内容可能因操作系统和 Rust 版本而异。要得到带这类信息的回溯，必须启用调试符号。使用不带 `--release` 的 `cargo build` 或 `cargo run`（正如我们这里所做）时，调试符号默认是开启的。

　　在示例 9-2 的输出中，回溯的第 6 行指向我们项目中引发问题的位置：_src/main.rs_ 第 4 行。若不想让程序 panic，应从第一条提到我们自己编写文件的行开始调查。在示例 9-1 中我们故意写了会 panic 的代码，修复办法就是不要请求超出向量索引范围的元素。以后代码再 panic 时，你需要弄清代码用哪些值执行了什么操作才导致 panic，以及本应怎么做。

　　本章稍后的[「要不要 `panic!`」][to-panic-or-not-to-panic]一节还会回到 `panic!`，讨论何时该用、何时不该用它处理错误。接下来，我们看看如何用 `Result` 从错误中恢复。

[to-panic-or-not-to-panic]: ../03-to-panic-or-not-to-panic/#to-panic-or-not-to-panic
