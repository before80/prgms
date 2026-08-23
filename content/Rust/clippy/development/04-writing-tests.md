+++
title = "04-编写测试"
date = 2026-08-22T18:00:00+08:00
weight = 74
type = "docs"
description = "Clippy lint 测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 编写测试 {#writing-tests}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/writing_tests.html](https://doc.rust-lang.org/nightly/clippy/development/writing_tests.html)


为 Clippy 开发 lint 是测试驱动开发（TDD）过程，因为在实现任何新 lint 逻辑之前，我们的首要任务是编写测试用例。

## 用测试开发 Lint

开发 Clippy 时，我们进入充满程序问题、风格错误、不合逻辑代码与违反惯例的复杂领域。
测试是我们能利用的第一层秩序，用来定义新 lint 应在何时、何地触发或不触发。

此外，先写测试有助于 Clippy 开发者在 lint 的首个迭代及后续改进之间找到平衡。
有了测试用例，我们就不必担心首版过度设计，也不会遗漏明显的边界情况。这种方式让我们能迭代增强每个 lint。

## Clippy UI 测试

我们使用 **UI 测试** 进行测试。UI 测试检查 Clippy 的输出是否与预期完全一致。每个测试只是一个包含待检查代码的普通 Rust 文件。

Clippy 的输出与 `.stderr` 文件对比。注意你不必自己创建该文件，稍后会用 [`cargo bless`](#cargo-bless) 生成 `.stderr` 文件。

### 编写测试用例

现在为我们的假想 `foo_functions` lint 构思一些测试。先打开 `cargo dev new_lint` 创建的测试文件 `tests/ui/foo_functions.rs`。

用以下示例更新文件以开始：

```rust
#![warn(clippy::foo_functions)] // < 添加此行，确保本文件中启用该 lint

// impl 方法
struct A;
impl A {
    pub fn fo(&self) {}
    pub fn foo(&self) {}
    //~^ foo_functions
    pub fn food(&self) {}
}

// 默认 trait 方法
trait B {
    fn fo(&self) {}
    fn foo(&self) {}
    //~^ foo_functions
    fn food(&self) {}
}

// 普通函数
fn fo() {}
fn foo() {}
//~^ foo_functions
fn food() {}

fn main() {
    // 我们也不希望对方法调用进行 lint
    foo();
    let a = A;
    a.foo();
}
```

在没有实际 lint 逻辑对 `foo` 函数名发出 lint 时，该测试会失败，因为我们在标记了 `//~^ foo_functions` 的行上期望有错误。不过，我们现在可以用以下命令运行测试：

```sh
$ TESTNAME=foo_functions cargo uitest
```

Clippy 会编译并失败，抱怨未收到任何错误：

```
...Clippy warnings and test outputs...
error: diagnostic code `clippy::foo_functions` not found on line 8
 --> tests/ui/foo_functions.rs:9:10
  |
9 |     //~^ foo_functions
  |          ^^^^^^^^^^^^^ expected because of this pattern
  |

error: diagnostic code `clippy::foo_functions` not found on line 16
  --> tests/ui/foo_functions.rs:17:10
   |
17 |     //~^ foo_functions
   |          ^^^^^^^^^^^^^ expected because of this pattern
   |

error: diagnostic code `clippy::foo_functions` not found on line 23
  --> tests/ui/foo_functions.rs:24:6
   |
24 | //~^ foo_functions
   |      ^^^^^^^^^^^^^ expected because of this pattern
   |

```

这很正常。毕竟我们写了很多 Rust 代码，但尚未实现检测 `foo` 函数并发出 lint 的逻辑。

随着逐步实现 lint 逻辑，我们会持续运行该 UI 测试命令。
Clippy 会开始输出信息，让我们检查输出是否朝预期发展。

### 输出示例

测试 `foo_functions` lint 时，输出大致如下：

```
failures:
---- compile_test stdout ----
normalized stderr:
error: function called "foo"
  --> tests/ui/foo_functions.rs:6:12
   |
LL |     pub fn foo(&self) {}
   |            ^^^
   |
   = note: `-D clippy::foo-functions` implied by `-D warnings`
error: function called "foo"
  --> tests/ui/foo_functions.rs:13:8
   |
LL |     fn foo(&self) {}
   |        ^^^
error: function called "foo"
  --> tests/ui/foo_functions.rs:19:4
   |
LL | fn foo() {}
   |    ^^^
error: aborting due to 3 previous errors
```

注意片段顶部的 *failures* 标签，下一节我们会消除它（保存该输出）。

> _注意：_ 可用逗号分隔列表运行多个测试文件：
> `TESTNAME=foo_functions,bar_methods,baz_structs`。

### `cargo bless`

对输出满意后，需运行以下命令为 lint 生成或更新 `.stderr` 文件：

```sh
$ TESTNAME=foo_functions cargo uibless
```

这会将发出的 lint 建议与修复写入 `.stderr` 文件，包括 lint 原因、建议修复与行号等。

之后运行 `TESTNAME=foo_functions cargo uitest` 应能通过。提交 lint 时，也需提交生成的 `.stderr` 文件。

一般而言，只应提交 `cargo bless` 为正在创建/编辑的特定 lint 更改的文件。

> _注意：_ 若生成的 `.stderr` 与 `.fixed` 文件为空，应删除它们。

## `toml` 测试

部分 lint 可通过 `clippy.toml` 配置，这些配置值在 `tests/ui-toml` 中测试。

要添加新测试，创建新目录并添加文件：

- `clippy.toml`：放入要测试的配置值。
- `lint_name.rs`：测试代码文件，应根据 `clippy.toml` 中的配置表现出不同的 lint 行为。

对应的 `.stderr` 与 `.fixed` 文件同样可用 `cargo bless` 生成。

## Cargo Lint

Cargo lint 的测试流程不同：我们关注的是 `Cargo.toml` manifest 文件，还需要与该 manifest 关联的最小 crate。这些测试生成在 `tests/ui-cargo`。

假设新示例 lint 名为 `foo_categories`，可运行：

```sh
$ cargo dev new_lint --name=foo_categories --pass=late --category=cargo
```

运行 `cargo dev new_lint` 后，默认会找到两个新 crate，各有 manifest 文件：

* `tests/ui-cargo/foo_categories/fail/Cargo.toml`：应使新 lint 报错。
* `tests/ui-cargo/foo_categories/pass/Cargo.toml`：不应触发该 lint。

若需要更多用例，可复制其中一个 crate（在 `foo_categories` 下）并重命名。

生成 `.stderr` 的流程与其他 lint 相同，在 `cargo uitest` 前加上 `TESTNAME` 变量对 Cargo lint 同样有效。

## Rustfix 测试

若你正在开发的 lint 使用结构化建议，
[`rustfix`] 会将 lint 的建议应用到测试文件代码，并与 `.fixed` 文件内容对比。

结构化建议告诉用户如何修复或重写被 lint 的代码，通常与 [`span_lint_and_sugg`] 一起使用。

若使用 `span_lint_and_sugg` 生成建议，但并非所有建议都能得到有效代码，可在测试文件顶部使用 `//@no-rustfix` 注释，不对该文件运行 `rustfix`。

关于建议的更多内容见[后续章节](emitting_lints.md)。

运行测试后，用 `cargo bless` 自动生成 `.fixed` 文件。

[`rustfix`]: https://github.com/rust-lang/cargo/tree/master/crates/rustfix
[`span_lint_and_sugg`]: https://doc.rust-lang.org/beta/nightly-rustc/clippy_utils/diagnostics/fn.span_lint_and_sugg.html

## 手动测试

若添加了 `println!` 导致测试套件输出难以阅读，手动针对示例文件测试会很有用。

要在本地修改下试用 Clippy，在工作副本根目录运行：

```sh
$ cargo dev lint input.rs
```
