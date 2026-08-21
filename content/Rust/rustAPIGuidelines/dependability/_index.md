+++
title = "第8章 可靠性"
date = 2026-08-18T21:50:00+08:00
weight = 100
type = "docs"
description = "可靠性 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/dependability.html](https://rust-lang.github.io/api-guidelines/dependability.html)

# 可靠性

## 函数校验其参数 (C-VALIDATE) {#c-validate}

Rust API 通常*不*遵循 [robustness principle]：「发送时保守；接受时宽松」。

[robustness principle]: http://en.wikipedia.org/wiki/Robustness_principle

相反，只要可行，Rust 代码就应当*强制*输入的有效性。

强制可以通过以下机制实现（按优先顺序列出）。

### 静态强制

选择能够排除非法输入的参数类型。

例如，优先

```rust
fn foo(a: Ascii) { /* ... */ }
```

而不是

```rust
fn foo(a: u8) { /* ... */ }
```

其中 `Ascii` 是 `u8` 的一个*包装器*，保证最高位为零；关于创建类型安全包装器的更多细节，见 newtype 模式（[C-NEWTYPE]）。

静态强制通常几乎没有运行时成本：它把成本推到边界处（例如当 `u8` 首次被转换成 `Ascii` 时）。它还能在编译期尽早捕获缺陷，而不是等到运行时失败。

另一方面，有些性质很难或无法用类型表达。

[C-NEWTYPE]: ../type-safety/#c-newtype
### 动态强制

在处理输入时（或必要时提前）校验输入。动态检查通常比静态检查更容易实现，但有若干缺点：

1. 运行时开销（除非检查可以作为处理输入的一部分完成）。
2. 缺陷检测被推迟。
3. 引入失败情形，无论是通过 `panic!` 还是 `Result`/`Option` 类型，随后都必须由客户端代码处理。

#### 用 `debug_assert!` 动态强制

与动态强制相同，但可以方便地为生产构建关闭代价昂贵的检查。

#### 可选择退出的动态强制

与动态强制相同，但增加了可选择退出检查的姊妹函数。

惯例是用 `_unchecked` 这样的后缀标记这些可退出函数，或把它们放在 `raw` 子模块中。

未检查版本的函数可以在以下情况审慎使用：（1）性能要求避免检查，并且（2）客户端有其他理由确信输入是有效的。

## 析构器永不失败 (C-DTOR-FAIL) {#c-dtor-fail}

析构器会在 panic 期间执行，在这种上下文中，失败的析构器会导致程序中止。

与其在析构器中失败，不如提供一个单独的方法来检查干净拆除，例如返回 `Result` 以报告问题的 `close` 方法。如果没有调用该 `close` 方法，`Drop` 实现应当执行拆除，并忽略或记录/追踪它所产生的任何错误。

## 可能阻塞的析构器提供替代方案 (C-DTOR-BLOCK) {#c-dtor-block}

同样，析构器不应调用阻塞操作，否则会大大增加调试难度。同样地，考虑提供一个单独的方法，为不会失败、也不会阻塞的拆除做准备。
