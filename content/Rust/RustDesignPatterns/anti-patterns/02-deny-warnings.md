+++
title = "02-`#[deny(warnings)]`"
date = 2026-08-18T22:10:00+08:00
weight = 44
type = "docs"
description = "`#[deny(warnings)]` — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/anti_patterns/deny-warnings.html](https://rust-unofficial.github.io/patterns/anti_patterns/deny-warnings.html)

# `#[deny(warnings)]`

## 描述 {#description}

用心良苦的 crate 作者希望确保代码在无警告的情况下构建。于是他们在 crate 根上加了如下注解：

## 示例 {#example}

```rust
#![deny(warnings)]

// 一切正常。
```

## 优点 {#advantages}

写法简短，一旦出问题就会中止构建。

## 缺点 {#drawbacks}

通过禁止编译器在有警告时构建，crate 作者实际上放弃了 Rust 广为人知的稳定性。有时新功能或旧的不良特性需要改变既有做法，因此会先写出在一定宽限期内只 `warn` 的 lint，然后再改为 `deny`。

例如，曾发现一个类型可以有两个带相同方法的 `impl`。这被认为是个坏主意，但为了让过渡平滑，引入了 `overlapping-inherent-impls` lint，在它成为未来版本中的硬错误之前，先向碰到该情况的人发出警告。

有时 API 会被弃用，因此其用法会发出之前没有的警告。

这一切合起来，可能导致只要有变化就可能破坏构建。

此外，提供额外 lint 的 crate（例如 [rust-clippy]）除非去掉该注解，否则无法再使用。这一点可用 [--cap-lints] 缓解。命令行参数 `--cap-lints=warn` 会把所有 `deny` 级别的 lint 错误降为警告。

## 替代方案 {#alternatives}

有两种应对方式：第一，把构建设置与代码解耦；第二，显式点名我们想要 `deny` 的 lint。

下面的命令行会以所有警告均为 `deny` 的方式构建：

`RUSTFLAGS="-D warnings" cargo build`

任何开发者都可以这样做（或在 Travis 等 CI 工具中设置，但请记住，一旦有变化这可能破坏构建），而无需改动代码。

或者，我们可以在代码中指定想要 `deny` 的 lint。下面是一份（希望）可以安全 deny 的警告 lint 列表（截至 rustc 1.48.0）：

```rust,ignore
#![deny(
    bad_style,
    const_err,
    dead_code,
    improper_ctypes,
    non_shorthand_field_patterns,
    no_mangle_generic_items,
    overflowing_literals,
    path_statements,
    patterns_in_fns_without_body,
    private_in_public,
    unconditional_recursion,
    unused,
    unused_allocation,
    unused_comparisons,
    unused_parens,
    while_true
)]
```

此外，将下列默认 `allow` 的 lint 设为 `deny` 可能也是好主意：

```rust,ignore
#![deny(
    missing_debug_implementations,
    missing_docs,
    trivial_casts,
    trivial_numeric_casts,
    unused_extern_crates,
    unused_import_braces,
    unused_qualifications,
    unused_results
)]
```

有些人可能还想把 `missing-copy-implementations` 加入列表。

注意我们刻意没有加入 `deprecated` lint，因为相当确定将来还会有更多 API 被弃用。

## 参见 {#see-also}

- [clippy lint 全集](https://rust-lang.github.io/rust-clippy/master)
- [deprecate attribute] 文档
- 输入 `rustc -W help` 可查看本机 lint 列表。也可输入
  `rustc --help` 查看通用选项列表
- [rust-clippy] 是一组用于写出更好 Rust 代码的 lint 集合

[rust-clippy]: https://github.com/rust-lang/rust-clippy
[deprecate attribute]: https://doc.rust-lang.org/reference/attributes.html#deprecation
[--cap-lints]: https://doc.rust-lang.org/rustc/lints/levels.html#capping-lints
