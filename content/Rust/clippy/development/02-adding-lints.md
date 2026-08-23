+++
title = "02-添加 Lint"
date = 2026-08-22T18:00:00+08:00
weight = 72
type = "docs"
description = "新增 lint 完整流程"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 添加 Lint {#adding-lints}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/adding_lints.html](https://doc.rust-lang.org/nightly/clippy/development/adding_lints.html)


你很可能是因为想为 Clippy 添加新 lint 才来到这里。若这是你第一次为 Clippy 做贡献，本文将引导你从零开始创建一个示例 lint。

我们将创建一个检测名为 `foo` 的函数的 lint，因为显然这不是一个描述性的名称。

- [添加新 lint](#添加新-lint)
  - [设置](#设置)
  - [入门](#入门)
    - [定义我们的 Lint](#定义我们的-lint)
      - [独立 lint](#独立-lint)
      - [特定类型](#特定类型)
      - [测试位置](#测试位置)
  - [测试](#测试)
    - [Cargo lint](#cargo-lint)
  - [Rustfix 测试](#rustfix-测试)
  - [手动测试](#手动测试)
  - [Lint 声明](#lint-声明)
  - [Lint 注册](#lint-注册)
  - [Lint 遍历](#lint-遍历)
  - [发出 lint](#发出-lint)
  - [添加 lint 逻辑](#添加-lint-逻辑)
  - [指定 lint 的最低支持 Rust 版本（MSRV）](#指定-lint-的最低支持-rust-版本msrv)
  - [编写 lint 说明](#author-lint)
  - [Print HIR lint](#print-hir-lint)
  - [文档](#文档)
  - [运行 rustfmt](#运行-rustfmt)
  - [调试](#调试)
  - [冲突的 lint](#冲突的-lint)
  - [PR 检查清单](#pr-检查清单)
  - [为 lint 添加配置](#为-lint-添加配置)
  - [速查表](#速查表)

## 设置

请参阅[基础](basics.md#get-the-code)文档。

## 入门

创建新 lint 时需要设置一些样板代码。幸运的是，你可以使用 Clippy 开发工具来处理这些。我们将新 lint 命名为 `foo_functions`（lint 名称通常使用 snake_case），且不需要类型信息，因此它将使用 early pass 类型（稍后会详细介绍）。若不确定所选名称是否适合该 lint，请查看我们的 [lint 命名指南][lint_naming]。

## 定义我们的 Lint

要入门，有两种方式定义我们的 lint。

### 独立 lint

命令：`cargo dev new_lint --name=foo_functions --pass=early --category=pedantic`
（若未提供 category，默认为 nursery）

该命令会创建新文件：`clippy_lints/src/foo_functions.rs`，并[注册 lint](#lint-注册)。

### 特定类型

命令：`cargo dev new_lint --name=foo_functions --type=functions --category=pedantic`

该命令会创建新文件：`clippy_lints/src/{type}/foo_functions.rs`。

注意此命令使用 `--type` 标志而非 `--pass`。与独立定义不同，该 lint 不会以传统方式注册。你需要在类型 lint pass 中调用你的 lint，该 pass 位于 `clippy_lints/src/{type}/mod.rs`。

“类型”只是 `clippy_lints/src` 下目录的名称，例如示例命令中的 `functions`。这些是按共同行为分组的 lint，若你的 lint 属于某一类，最好将其添加到该类型中。

### 测试位置

两个命令都会创建文件：`tests/ui/foo_functions.rs`。对于 cargo lint，默认会在 `tests/ui-cargo` 下创建两个项目层次结构（fail/pass）。

接下来，我们打开这些文件并添加 lint！

## 测试

先编写一些测试，以便在迭代 lint 时运行。

Clippy 使用 UI 测试。UI 测试检查 Clippy 的输出是否与预期完全一致。每个测试只是一个包含待检查代码的普通 Rust 文件。Clippy 的输出会与 `.stderr` 文件比较。注意你无需自己创建该文件，稍后我们会介绍如何生成 `.stderr` 文件。

首先在 `tests/ui/foo_functions.rs` 打开创建的测试文件。

用一些示例更新该文件以入门：

```rust
#![allow(unused)]
#![warn(clippy::foo_functions)]

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

注意我们在期望报错的行上添加了带 lint 名称的注释标注。除非常特殊的情况（`//@check-pass`），测试文件必须至少包含一个错误标记才会被接受。

实现 lint 后，可运行 `TESTNAME=foo_functions cargo uibless` 生成 `.stderr` 文件。若 lint 使用了结构化建议，该命令还会生成对应的 `.fixed` 文件。

在实现 lint 的过程中，可以持续运行 UI 测试。每次测试运行都会更新 `.stderr` 文件，便于检查输出是否符合预期。

实现 lint 后，运行 `TESTNAME=foo_functions cargo uitest` 应能单独通过。提交 lint 时，还需提交生成的 `.stderr` 文件，以及（如适用）`.fixed` 文件。一般而言，只应提交由 `cargo bless` 为正在创建/编辑的特定 lint 更改的文件。

> _注意：_ 可通过逗号分隔的列表指定多个测试文件：`TESTNAME=foo_functions,test2,test3`。

### Cargo lint

cargo lint 的测试流程不同，我们关注的是 `Cargo.toml` manifest 文件，还需要与之关联的最小 crate。

若新 lint 名为 `foo_categories`，运行 `cargo dev new_lint --name=foo_categories --type=cargo --category=cargo` 后，默认会找到两个新 crate，各带 manifest 文件：

* `tests/ui-cargo/foo_categories/fail/Cargo.toml`：该文件应使新 lint 报错。
* `tests/ui-cargo/foo_categories/pass/Cargo.toml`：该文件不应触发 lint。

若需要更多用例，可复制其中一个 crate（在 `foo_categories` 下）并重命名。

生成 `.stderr` 文件的流程相同，在 `cargo uitest` 前加上 `TESTNAME` 变量也适用。

## Rustfix 测试

若你正在开发的 lint 使用了结构化建议，测试会通过为该测试运行 [rustfix] 创建 `.fixed` 文件。Rustfix 会将 lint 的建议应用到测试文件代码上，并与 `.fixed` 文件内容比较。

使用 `cargo bless` 可在运行测试时自动生成 `.fixed` 文件。

[rustfix]: https://github.com/rust-lang/cargo/tree/master/crates/rustfix

## 手动测试

若添加了 `println!` 导致测试套件输出难以阅读，针对示例文件手动测试会很有用。要在本地修改下试用 Clippy，在 Clippy 目录中运行：

```bash
cargo dev lint input.rs
```

要对现有项目而非单个文件运行 Clippy，可使用：

```bash
cargo dev lint /path/to/project
```

或设置指向本地 Clippy 二进制文件的 rustup toolchain：

```bash
cargo dev setup toolchain

# 然后在 `/path/to/project` 中运行
cargo +clippy clippy
```

## Lint 声明

先在 `clippy_lints` crate 中打开新创建的文件 `clippy_lints/src/foo_functions.rs`。所有 lint 代码都在该 crate 中。该文件已导入一些初始所需内容：

```rust
use rustc_lint::{EarlyLintPass, EarlyContext};
use rustc_session::declare_lint_pass;
use rustc_ast::ast::*;
```

下一步是更新 lint 声明。Lint 使用 [`declare_clippy_lint!`][declare_clippy_lint] 宏声明，我们只需将自动生成的 lint 声明更新为真实描述，类似如下：

```rust
declare_clippy_lint! {
    /// ### 作用
    ///
    /// ### 为何不好？
    ///
    /// ### 示例
    /// ```rust
    /// // 示例代码
    /// ```
    #[clippy::version = "1.29.0"]
    pub FOO_FUNCTIONS,
    pedantic,
    "function named `foo`, which is not a descriptive name"
}
```

* 以 `///` 开头的行构成 lint 文档部分。这是默认文档风格，将[如此显示][example_lint_page]。要在浏览器中本地渲染并打开该文档，运行 `cargo dev serve`。
* `#[clippy::version]` 属性会作为 lint 文档的一部分渲染。值应设为开发该 lint 时的当前 Rust 版本，可在 rust-clippy 目录运行 `rustc -vV` 获取。版本列在 *release* 下。（使用不带 `-nightly` 后缀的版本。）
* `FOO_FUNCTIONS` 是我们的 lint 名称。命名 lint 时请务必遵循 [lint 命名指南][lint_naming]。简言之，名称应说明检查的内容，且与 `allow`/`warn`/`deny` 连用时读起来自然。
* `pedantic` 将 lint 级别设为 `Allow`。确切映射见[此处][category_level_mapping]
* 最后一部分应是说明代码具体有何问题的文本

该文件其余部分包含 lint pass 的空实现，此处为 `EarlyLintPass`，应类似如下：

```rust
// clippy_lints/src/foo_functions.rs

// .. 导入与 lint 声明 ..

declare_lint_pass!(FooFunctions => [FOO_FUNCTIONS]);

impl EarlyLintPass for FooFunctions {}
```

[declare_clippy_lint]: https://github.com/rust-lang/rust-clippy/blob/557f6848bd5b7183f55c1e1522a326e9e1df6030/clippy_lints/src/lib.rs#L60
[example_lint_page]: https://rust-lang.github.io/rust-clippy/master/index.html#redundant_closure
[lint_naming]: https://rust-lang.github.io/rfcs/0344-conventions-galore.html#lints
[category_level_mapping]: ../index.html

## Lint 注册

使用 `cargo dev new_lint` 时，lint 会自动注册，无需其他操作。

手动声明新 lint 并使用 `cargo dev update_lints` 时，可能需通过在 `clippy_lints/src/lib.rs` 的 `early_lint_methods!` 宏调用中、`// add early passes here` 标记处添加条目来手动注册 lint pass：

```rust,ignore
FooFunctions: foo_functions::FooFunctions = foo_functions::FooFunctions,
```

如你所料，也有对应的 `late_lint_methods!` 宏。若未在 `early_lint_methods!` 或 `late_lint_methods!` 中添加条目，对应的 lint pass 将不会运行。

`cargo dev update_lints` 不自动化此步骤的原因之一是，多个 lint 可共用同一 lint pass，添加新 lint 时 lint pass 可能已注册。另一原因是所列 pass 的顺序决定实际运行顺序，进而影响发出 lint 的输出顺序。

## Lint 遍历

编写只检查函数名称的 lint 意味着我们只需处理 AST，完全不必处理类型系统。这很好，因为使该 lint 的实现更简单。

每个新 Clippy lint 都要做此决定。归根结底是使用 [`EarlyLintPass`][early_lint_pass] 还是 [`LateLintPass`][late_lint_pass]。

`EarlyLintPass` 在类型检查和 [HIR](https://rustc-dev-guide.rust-lang.org/hir.html) 降级之前运行，而 `LateLintPass` 在这些阶段之后运行，可访问类型信息。`cargo dev new_lint` 命令默认使用推荐的 `LateLintPass`，若 lint 只需 AST 级分析，可指定 `--pass=early`。

由于检查函数名不需要类型信息，我们在运行新 lint 自动化时使用了 `--pass=early`，相应添加了所有导入。

[early_lint_pass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.EarlyLintPass.html
[late_lint_pass]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.LateLintPass.html

## 发出 lint

有了 UI 测试和 lint 声明，可以开始实现 lint 逻辑。

先为 `FooFunctions` 实现 `EarlyLintPass`：

```rust,ignore
impl EarlyLintPass for FooFunctions {
    fn check_fn(&mut self, cx: &EarlyContext<'_>, fn_kind: FnKind<'_>, span: Span, _: NodeId) {
        // TODO: 在此发出 lint
    }
}
```

我们实现 [`EarlyLintPass`][early_lint_pass] trait 的 [`check_fn`][check_fn] 方法。这让我们能访问当前被检查函数的各种信息。下一节会详述。先不管细节，先对*每个*函数定义发出 lint。

根据希望 lint 消息的复杂程度，可从多种 lint 发出函数中选择。它们都在 [`clippy_utils/src/diagnostics.rs`][diagnostics] 中。

本例中 `span_lint_and_help` 似乎最合适。它允许提供额外帮助消息，且我们无法自动建议更好的名称。用法如下：

```rust,ignore
impl EarlyLintPass for FooFunctions {
    fn check_fn(&mut self, cx: &EarlyContext<'_>, fn_kind: FnKind<'_>, span: Span, _: NodeId) {
        span_lint_and_help(
            cx,
            FOO_FUNCTIONS,
            span,
            "function named `foo`",
            None,
            "consider using a more meaningful name"
        );
    }
}
```

运行 UI 测试现在应产生包含 lint 消息的输出。

根据 [rustc-dev-guide]，文本应客观陈述，避免大写和句号，除非需要多个句子。当消息或标签中必须出现代码或标识符时，应用单反引号 \` 包裹。

[check_fn]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_lint/trait.EarlyLintPass.html#method.check_fn
[diagnostics]: https://github.com/rust-lang/rust-clippy/blob/master/clippy_utils/src/diagnostics.rs
[the rustc-dev-guide]: https://rustc-dev-guide.rust-lang.org/diagnostics.html

## 添加 lint 逻辑

lint 逻辑的实现很可能与我们的示例不同，因此本节保持较短。

使用 [`check_fn`][check_fn] 方法可访问 [`FnKind`][fn_kind]，其中有 [`FnKind::Fn`] 变体，可通过 [`Ident`][ident] 访问函数/方法的名称。

据此可扩展 `check_fn` 方法为：

```rust
impl EarlyLintPass for FooFunctions {
    fn check_fn(&mut self, cx: &EarlyContext<'_>, fn_kind: FnKind<'_>, span: Span, _: NodeId) {
        if is_foo_fn(fn_kind) {
            span_lint_and_help(
                cx,
                FOO_FUNCTIONS,
                span,
                "function named `foo`",
                None,
                "consider using a more meaningful name"
            );
        }
    }
}
```

我们将 lint 条件与 lint 发出分离，使代码更易读。某些情况下这种分离还允许为独立函数编写单元测试（而不仅是 UI 测试）。

在我们的示例中，`is_foo_fn` 如下：

```rust
// use 语句、impl EarlyLintPass、check_fn 等

fn is_foo_fn(fn_kind: FnKind<'_>) -> bool {
    match fn_kind {
        FnKind::Fn(_, _, Fn { ident, .. }) => {
            // 检查 `fn` 名称是否为 `foo`
            ident.name.as_str() == "foo"
        }
        // 忽略闭包
        FnKind::Closure(..) => false
    }
}
```

现在还应使用 `cargo test` 运行完整测试套件。此时运行 `cargo test` 应产生预期输出。记得运行 `cargo bless` 更新 `.stderr` 文件。

`cargo test`（与 `cargo uitest` 相对）还会确保 lint 实现本身未违反任何 Clippy lint。

lint 实现到此应已完成。运行 `cargo test` 现在应能通过。

[fn_kind]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_ast/visit/enum.FnKind.html
[`FnKind::Fn`]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_ast/visit/enum.FnKind.html#variant.Fn
[ident]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/symbol/struct.Ident.html

## 指定 lint 的最低支持 Rust 版本（MSRV）

有时 lint 的建议需要特定 Rust 版本。例如 `manual_strip` lint 建议使用 `str::strip_prefix` 和 `str::strip_suffix`，这些仅在 Rust 1.45 之后可用。此类情况下，需确保项目配置的 MSRV >= 所需 Rust 特性的 MSRV。若建议中使用多个特性，选择支持全部特性的 MSRV。

首先，在 [`clippy_utils::msrvs`] 中为所需特性添加 MSRV 别名。例如之后可访问为 `msrvs::STR_STRIP_PREFIX`。

```rust
msrv_aliases! {
    ..
    1,45,0 { STR_STRIP_PREFIX }
}
```

要访问项目配置的 MSRV，需在 LintPass struct 中有 `msrv` 字段，以及初始化该字段的构造函数。`msrv` 值在 `clippy_lints/lib.rs` 中传给构造函数。

```rust
pub struct ManualStrip {
    msrv: Msrv,
}

impl ManualStrip {
    pub fn new(conf: &'static Conf) -> Self {
        Self { msrv: conf.msrv.into() }
    }
}
```

然后可在 LintPass 中使用 `Msrv::meets` 方法将项目 MSRV 与特性 MSRV 匹配。

``` rust
if !self.msrv.meets(cx, msrvs::STR_STRIP_PREFIX) {
    return;
}
```

Early lint pass 应改用 `MsrvStack` 配合 `extract_msrv_attr!()`

将 `msrv` 添加到 lint 后，应在 lint 测试文件（本例为 `tests/ui/manual_strip.rs`）中添加相关测试用例。应包含低于 MSRV 的版本用例，以及相同内容但针对 MSRV 版本本身的用例。

```rust,ignore
...

#[clippy::msrv = "1.44"]
fn msrv_1_44() {
    /* 会触发该 lint 的代码 */
}

#[clippy::msrv = "1.45"]
fn msrv_1_45() {
    /* 会触发该 lint 的代码 */
}
```

最后一步，应将 lint 添加到 lint 文档。这在 `clippy_config/src/conf.rs` 中完成：

```rust
define_Conf! {
    #[lints(
        allow_attributes,
        allow_attributes_without_reason,
        ..
        <the newly added lint name>,
        ..
        unused_trait_names,
        use_self,
    )]
    msrv: Msrv = Msrv::default(),
    ...
}
```

[`clippy_utils::msrvs`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/msrvs/index.html

之后按[为 lint 添加配置](#为-lint-添加配置)中的说明更新 book 文档。

## 编写 lint 说明

若实现 lint 遇到困难，还有内部 `author` lint 可生成检测违规模式的 Clippy 代码。它并非适用于所有 Rust 语法，但可给出良好起点。

最快用法是 [Rust playground：play.rust-lang.org][author_example]。将要 lint 的代码放入编辑器，在项上方添加 `#[clippy::author]` 属性。然后通过 `Tools -> Clippy` 运行 Clippy，输出中应能看到生成的代码。

[此处][author_example]有 playground 示例。

若命令执行成功，可将代码复制到实现 lint 的位置。

[author_example]: https://play.rust-lang.org/?version=nightly&mode=debug&edition=2024&gist=9a12cb60e5c6ad4e3003ac6d5e63cf55

## Print HIR lint

实现 lint 时，先理解 rustc 使用的内部表示很有帮助。Clippy 有 `#[clippy::dump]` 属性，会打印属性所附项、语句或表达式的[_高级中间表示（HIR）_]。要为表达式附加属性，通常需启用 `#![feature(stmt_expr_attributes)]`。

[此处][print_hir_example]有示例，选择 _Tools_ 并运行 _Clippy_ 即可。

[_High-Level Intermediate Representation (HIR)_]: https://rustc-dev-guide.rust-lang.org/hir.html
[print_hir_example]: https://play.rust-lang.org/?version=nightly&mode=debug&edition=2024&gist=daf14db3a7f39ca467cd1b86c34b9afb

## 文档

提交 PR 前的最后一步是为 lint 声明添加文档。

请用类似以下的 doc 注释记录 lint：

```rust
declare_clippy_lint! {
    /// ### 作用
    /// 检查 ...（描述 lint 匹配的内容）。
    ///
    /// ### 为何不好？
    /// 说明 lint 该代码的原因。
    ///
    /// ### 示例
    ///
    /// ```rust,ignore
    /// // 触发该 lint 的简短代码示例
    /// ```
    ///
    /// 改用：
    /// ```rust,ignore
    /// // 不触发该 lint 的改进代码简短示例
    /// ```
    #[clippy::version = "1.29.0"]
    pub FOO_FUNCTIONS,
    pedantic,
    "function named `foo`, which is not a descriptive name"
}
```

若 lint 因 lint 的内容不一定是“不好”而更多是风格选择，属于 `restriction` 组，则将“为何不好？”小节标题替换为“为何限制？”，避免写“为何不好？其实不算不好，但 ...”。

lint 合并后，该文档会出现在 [lint 列表][lint_list] 中。

[lint_list]: https://rust-lang.github.io/rust-clippy/master/index.html

## 运行 rustfmt

[Rustfmt] 是按风格指南格式化 Rust 代码的工具。PR 合并前代码必须经过 `rustfmt` 格式化。Clippy 在 CI 中使用 nightly `rustfmt`。

可通过 `rustup` 安装：

```bash
rustup component add rustfmt --toolchain=nightly
```

使用 `cargo dev fmt` 格式化整个代码库。确保 nightly toolchain 已安装 `rustfmt`。

[Rustfmt]: https://github.com/rust-lang/rustfmt

## 调试

若要调试 lint 实现的部分，可在代码任意处使用 [`dbg!`] 宏。运行测试时调试输出会出现在 `stdout` 部分。

[`dbg!`]: https://doc.rust-lang.org/std/macro.dbg.html

## 冲突的 lint

有些 lint 处理相同模式但建议不同做法。换言之，某些 lint 可能建议的修改与另一些 lint 对同一代码的建议方向相反，产生冲突的诊断。

当你创建的 lint 处于这种场景时，以下建议可指导分类：

* 它们应处于同一 category 的唯一情况是 category 为 `restriction`。例如 `semicolon_inside_block` 和 `semicolon_outside_block`。
* 其他所有情况，它们应处于不同 category，且 allow 级别不同。例如 `implicit_return`（restriction，allow）和 `needless_return`（style，warn）。

对于处于不同 category 的 lint，还建议至少其中一个应在 `restriction` category。原因是 `restriction` 组是唯一不推荐启用整组、而是从中挑选 lint 的组。

## PR 检查清单

提交 PR 前请确认已满足所有基本要求：

<!-- Sync this with `.github/PULL_REQUEST_TEMPLATE` -->

- \[ ] 遵循 [lint 命名约定][lint_naming]
- \[ ] 添加通过的 UI 测试（包括已提交的 `.stderr` 文件）
- \[ ] 本地 `cargo test` 通过
- \[ ] 已执行 `cargo dev update_lints`
- \[ ] 已添加 lint 文档
- \[ ] 已运行 `cargo dev fmt`

## 为 lint 添加配置

Clippy 支持通过 `clippy.toml` 文件配置 lint 值，该文件在以下位置查找：

1. `CLIPPY_CONF_DIR` 环境变量指定的目录，或
2. [CARGO_MANIFEST_DIR](https://doc.rust-lang.org/cargo/reference/environment-variables.html) 环境变量指定的目录，或
3. 当前目录。

为 lint 添加配置对阈值或约束某些用户可能视为误报的行为很有用。添加配置步骤如下：

1. 在 [`clippy_config::conf`] 中添加新配置项，如下：

   ```rust,ignore
   /// Lint: LINT_NAME.
   ///
   /// <配置字段 doc 注释>
   (configuration_ident: Type = DefaultValue),
   ```

   doc 注释会自动添加到所列 lint 的文档中。默认值会使用类型的 `Debug` 实现格式化。
2. 将配置值添加到 lint impl struct：
    1. 首先需要定义 lint impl struct。Lint impl struct 通常由 `declare_lint_pass!` 宏生成。需手动定义 struct 以添加某种元数据：
       ```rust
       // 生成的 struct 定义
       declare_lint_pass!(StructName => [
           LINT_NAME
       ]);

       // 新的手动 struct 定义
       pub struct StructName {}

       impl_lint_pass!(StructName => [
           LINT_NAME
       ]);
       ```

    2. 接下来添加配置值及对应的创建方法：
       ```rust
       pub struct StructName {
           configuration_ident: Type,
       }

       // ...

       impl StructName {
           pub fn new(conf: &'static Conf) -> Self {
               Self {
                   configuration_ident: conf.configuration_ident,
               }
           }
       }
       ```
3. 将配置值传给 lint impl struct：

   先在 [`clippy_lints` lib file] 中找到 struct 构造。配置值现在被 clone 或 copy 到局部变量，然后传给 impl struct：

   ```rust,ignore
   // 默认生成的注册：
   store.register_*_pass(|| box module::StructName);

   // 带配置值的新注册
   store.register_*_pass(move || box module::StructName::new(conf));
   ```

   恭喜，工作几乎完成。配置值现在可通过 `self.configuration_ident` 在 lint 代码中访问。

4. 添加测试：
    1. 默认配置值可像普通 lint 一样在 [`tests/ui`] 中测试。
    2. 配置本身会在 [`tests/ui-toml`] 中单独测试。只需添加名称合适的新子文件夹。该文件夹包含带配置值的 `clippy.toml` 文件，以及应由 Clippy lint 的 rust 文件。测试写法可照常进行。

5. 更新 [Lint 配置](../lint_configuration.md)

   运行 `cargo bless --test config-metadata` 为 book 生成文档变更。

[`clippy_config::conf`]: https://github.com/rust-lang/rust-clippy/blob/master/clippy_config/src/conf.rs
[`clippy_lints` lib file]: https://github.com/rust-lang/rust-clippy/blob/master/clippy_lints/src/lib.rs
[`tests/ui`]: https://github.com/rust-lang/rust-clippy/blob/master/tests/ui
[`tests/ui-toml`]: https://github.com/rust-lang/rust-clippy/blob/master/tests/ui-toml

## 速查表

以下是每个 lint 可能需要的参考：

* [Clippy utils][utils] - 各种辅助函数。也许所需函数已存在（[`implements_trait`]、[`snippet`] 等）
* [Clippy diagnostics][diagnostics]
* [Let chains][let-chains]
* [`from_expansion`][from_expansion] 和 [`in_external_macro`][in_external_macro]
* [`Span`][span]
* [`Applicability`][applicability]
* [编写 lint 的常用工具](common_tools_writing_lints.md) 帮助常见操作
* [rustc-dev-guide][rustc-dev-guide] 解释许多编译器内部概念
* [nightly rustc 文档][nightly_docs] 本指南中多处链接

对于 `EarlyLintPass` lint：

* [`EarlyLintPass`][early_lint_pass]
* [`rustc_ast::ast`][ast]

对于 `LateLintPass` lint：

* [`LateLintPass`][late_lint_pass]
* [`Ty::TyKind`][ty]

Clippy 的大多数 lint 工具都有文档，但 rustc 内部大多目前缺乏文档。这很遗憾，但多数情况下你可以从现有类似 lint 复制。若卡住，欢迎在 [Zulip] 或 issue/PR 中提问。

[utils]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/index.html
[`implements_trait`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/ty/fn.implements_trait.html
[`snippet`]: https://doc.rust-lang.org/nightly/nightly-rustc/clippy_utils/source/fn.snippet.html
[let-chains]: https://github.com/rust-lang/rust/pull/94927
[from_expansion]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/struct.Span.html#method.from_expansion
[in_external_macro]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/struct.Span.html#method.in_external_macro
[span]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_span/struct.Span.html
[applicability]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_errors/enum.Applicability.html
[rustc-dev-guide]: https://rustc-dev-guide.rust-lang.org/
[nightly_docs]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/
[ast]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_ast/ast/index.html
[ty]: https://doc.rust-lang.org/nightly/nightly-rustc/rustc_middle/ty/sty/index.html
[Zulip]: https://rust-lang.zulipchat.com/#narrow/stream/clippy
