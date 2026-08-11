+++
title = "07-测试"
date = 2026-07-30T14:49:00+08:00
weight = 27
type = "docs"
description = "用 Cargo 运行单元测试与集成测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 测试 {#tests}


> 原文链接: [https://doc.rust-lang.org/cargo/guide/tests.html](https://doc.rust-lang.org/cargo/guide/tests.html)


Cargo 可以用 `cargo test` 命令运行你的测试。Cargo 会在两个地方查找要运行的测试：每个 `src` 文件中，以及 `tests/` 中的任何测试。`src` 文件中的测试应为单元测试与[文档测试]。`tests/` 中的测试应为集成风格的测试。因此，你需要在 `tests` 中的文件里导入你的 crate。

下面是在我们的[包][def-package]中运行 `cargo test` 的例子，该包目前还没有测试：

```console
$ cargo test
   Compiling regex v1.5.0 (https://github.com/rust-lang/regex.git#9f9f693)
   Compiling hello_world v0.1.0 (file:///path/to/package/hello_world)
     Running target/test/hello_world-9c2b65bbb79eabce

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

若包中有测试，你会看到更多输出，并带有正确的测试数量。

也可以传入过滤器来运行特定测试：

```console
$ cargo test foo
```

这会运行名称中包含 `foo` 的任何测试。

`cargo test` 还会做额外检查。它会编译你包含的任何示例，以确保它们仍能编译。它也会运行文档测试，以确保文档注释中的代码示例能够编译。关于编写与组织测试的一般性说明，请参阅 Rust 文档中的[测试指南][testing]。关于 Cargo 中不同测试风格的更多信息，参见 [Cargo 目标：测试]。

[documentation tests]: https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
[文档测试]: https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
[def-package]:  ../../appendix/01-glossary/#package  '"package" (glossary entry)'
[testing]: https://doc.rust-lang.org/book/ch11-00-testing.html
[Cargo Targets: Tests]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#tests
[Cargo 目标：测试]: ../../cargo-reference/the-manifest-format/01-cargo-targets/#tests
