+++
title = "02-语法树模式"
date = 2026-08-22T18:00:00+08:00
weight = 832
type = "docs"
description = "语法树模式提案"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 语法树模式 {#syntax-tree-patterns}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/proposals/syntax-tree-patterns.html](https://doc.rust-lang.org/nightly/clippy/development/proposals/syntax-tree-patterns.html)


- Feature Name: syntax-tree-patterns
- Start Date: 2019-03-12
- RFC PR: [#3875](https://github.com/rust-lang/rust-clippy/pull/3875)


# 摘要

引入一种领域特定语言（类似正则表达式），用于通过*语法树模式*来描述 lint。

# 动机

在编写 lint 时，查找具有特定属性的语法树部分（AST、HIR 等）是一项主要工作（例如「*条件为 block 的 if*」）。对于非平凡的 lint，通常需要对 AST / HIR 节点进行嵌套的模式匹配。例如，要判断一个表达式是否为布尔字面量，需要如下检查：

```rust,ignore
if let ast::ExprKind::Lit(lit) = &expr.node {
    if let ast::LitKind::Bool(_) = &lit.node {
        ...
    }
}
```

编写这类匹配代码很快会变得复杂，且生成的代码往往难以理解。下面的代码展示了 `collapsible_if` lint 所需的模式匹配的简化版本：

```rust,ignore
// collapsible_if lint 的简化版本
if let ast::ExprKind::If(check, then, None) = &expr.node {
    if then.stmts.len() == 1 {
        if let ast::StmtKind::Expr(inner) | ast::StmtKind::Semi(inner) = &then.stmts[0].node {
            if let ast::ExprKind::If(check_inner, content, None) = &inner.node {
                ...
            }
        }
    }
}
```

`if_chain` 宏可以通过扁平化嵌套的 if 语句来提高可读性，但生成的代码仍然相当难读：

```rust
// collapsible_if lint 的简化版本
if_chain! {
    if let ast::ExprKind::If(check, then, None) = &expr.node;
    if then.stmts.len() == 1;
    if let ast::StmtKind::Expr(inner) | ast::StmtKind::Semi(inner) = &then.stmts[0].node;
    if let ast::ExprKind::If(check_inner, content, None) = &inner.node;
    then {
        ...
    }
}
```

上面的代码匹配的是：if 表达式中仅包含另一个 if 表达式（且两个 if 都没有 else 分支）。虽然很容易用自然语言说明这个 lint 在做什么，但从上面的代码示例中却很难一眼看出。

基于上述动机，本 RFC 的第一个目标是**简化 lint 的编写与阅读**。

动机的第二部分是 Clippy 对不稳定的编译器内部数据结构的依赖。Clippy lint 目前是针对编译器的 AST / HIR 编写的，这意味着这些数据结构哪怕只有微小变动，也可能导致大量 lint 失效。本 RFC 的第二个目标是**使 lint 独立于编译器的 AST / HIR 数据结构**。

# 方案

编写 lint 时的大量复杂性，似乎源于必须手动实现匹配逻辑（见上文代码示例）。这是一种命令式风格：描述*如何*匹配语法树节点，而不是以声明式方式指定*应匹配什么*。在其他领域，常见做法是使用声明式模式来描述所需信息，由实现完成实际匹配。[正则表达式](https://en.wikipedia.org/wiki/Regular_expression)就是这种做法的知名例子。与其编写检测特定字符序列的代码，不如用领域特定语言描述搜索模式，再用该模式搜索匹配项。使用声明式领域特定语言的优势在于，其受限的领域（例如正则表达式中的字符序列匹配）允许以非常自然、富有表现力的方式表达该领域中的实体。

正则表达式在扁平字符序列中搜索模式时非常有用，但难以直接应用于语法树等层次化数据结构。因此，本 RFC 提出一种受正则表达式启发、面向层次化语法树的模式匹配系统。

# 指南级说明

本提案新增 `pattern!` 宏，可用于指定要搜索的语法树模式。下面是一个简单模式：

```rust
pattern!{
    my_pattern: Expr =
        Lit(Bool(false))
}
```

该宏调用定义了名为 `my_pattern` 的模式，可针对 `Expr` 语法树节点进行匹配。实际模式（本例中为 `Lit(Bool(false))`）定义哪些语法树应匹配该模式。此模式匹配值为 `false` 的布尔字面量表达式。

随后可按如下方式使用该模式实现 lint：

```rust,ignore
...

impl EarlyLintPass for MyAwesomeLint {
    fn check_expr(&mut self, cx: &EarlyContext, expr: &syntax::ast::Expr) {

        if my_pattern(expr).is_some() {
            cx.span_lint(
                MY_AWESOME_LINT,
                expr.span,
                "This is a match for a simple pattern. Well done!",
            );
        }

    }
}
```

`pattern!` 宏调用会展开为函数 `my_pattern`，该函数接受语法树表达式作为参数，并返回一个 `Option`，表示模式是否匹配。

> 注：结果类型在[后续章节](#结果类型)中有更详细说明。目前只需知道：匹配成功时结果为 `Some`，否则为 `None`。

## 模式语法

以下示例演示模式语法：

#### 任意（`_`）

最简单的模式是任意模式。它匹配任何内容，因此类似于正则表达式中的 `*`。

```rust
pattern!{
    // 匹配任意表达式
    my_pattern: Expr =
        _
}
```

#### 节点（`<node-name>(<args>)`）

节点用于匹配 AST 节点的特定变体。节点有名称和若干参数，参数数量取决于节点类型。例如，`Lit` 节点有一个描述字面量类型的参数。又如，`If` 节点有三个参数，分别描述 if 的条件、then 块和 else 块。

```rust
pattern!{
    // 匹配任意字面量表达式
    my_pattern: Expr =
        Lit(_)
}

pattern!{
    // 匹配任意布尔字面量表达式
    my_pattern: Expr =
        Lit(Bool(_))
}

pattern!{
    // 匹配条件为布尔字面量的 if 表达式
    // 注：此处的 `_?` 语法表示 else 分支可选且可为任意内容。
    //     详见 `Repetition` 章节。
    my_pattern: Expr =
        If( Lit(Bool(_)) , _, _?)
}
```

#### 字面量（`<lit>`）

模式也可包含 Rust 字面量。这些字面量匹配自身。

```rust
pattern!{
    // 匹配布尔字面量 false
    my_pattern: Expr =
        Lit(Bool(false))
}

pattern!{
    // 匹配字符字面量 'x'
    my_pattern: Expr =
        Lit(Char('x'))
}
```

#### 交替（`a | b`）

```rust
pattern!{
    // 匹配布尔或整数字面量
    my_pattern: Lit =
        Bool(_) | Int(_)
}

pattern!{
    // 匹配值为 'x' 或 'y' 的字符字面量表达式
    my_pattern: Expr =
        Lit( Char('x' | 'y') )
}
```

#### 空（`()`）

空模式表示空序列，或 optional 的 `None` 变体。

```rust
pattern!{
    // 匹配空数组表达式
    my_pattern: Expr =
        Array( () )
}

pattern!{
    // 匹配没有 else 子句的 if 表达式
    my_pattern: Expr =
        If(_, _, ())
}
```

#### 序列（`<a> <b>`）

```rust
pattern!{
    // 匹配数组 [true, false]
    my_pattern: Expr =
        Array( Lit(Bool(true)) Lit(Bool(false)) )
}
```

#### 重复（`<a>*`、`<a>+`、`<a>?`、`<a>{n}`、`<a>{n,m}`、`<a>{n,}`）

元素可以重复。指定重复的语法与[正则表达式语法](https://docs.rs/regex/1.1.2/regex/#repetitions)相同。

```rust
pattern!{
    // 匹配最后两个或倒数第二个元素为 'x' 的数组
    // 示例：
    //     ['x', 'x']                         匹配
    //     ['x', 'x', 'y']                    匹配
    //     ['a', 'b', 'c', 'x', 'x', 'y']     匹配
    //     ['x', 'x', 'y', 'z']               不匹配
    my_pattern: Expr =
        Array( _* Lit(Char('x')){2} _? )
}

pattern!{
    // 匹配**可能有也可能没有** else 块的 if 表达式
    // 注意：`If(_, _, _)` 仅匹配**有** else 块的 if
    //
    //              | 带 else 的 if | 不带 else 的 if
    // If(_, _, _)  |     匹配      |     不匹配
    // If(_, _, _?) |     匹配      |      匹配
    // If(_, _, ()) |    不匹配     |      匹配
    my_pattern: Expr =
        If(_, _, _?)
}
```

#### 命名子匹配（`<a>#<name>`）

```rust
pattern!{
    // 匹配字符字面量，并将该字面量命名为 foo
    my_pattern: Expr =
        Lit(Char(_)#foo)
}

pattern!{
    // 匹配字符字面量，并将字符命名为 bar
    my_pattern: Expr =
        Lit(Char(_#bar))
}

pattern!{
    // 匹配字符字面量，并将表达式命名为 baz
    my_pattern: Expr =
        Lit(Char(_))#baz
}
```

使用命名子匹配的原因见[结果类型](#结果类型)章节。

### 小结

下表概括模式语法：

| Syntax                  | 概念             | Examples                                   |
|-------------------------|------------------|--------------------------------------------|
|`_`                      | 任意             | `_`                                        |
|`<node-name>(<args>)`    | 节点             | `Lit(Bool(true))`, `If(_, _, _)`           |
|`<lit>`                  | 字面量           | `'x'`, `false`, `101`                      |
|`<a> \| <b>`             | 交替             | `Char(_) \| Bool(_)`                       |
|`()`                     | 空               | `Array( () )`                              |
|`<a> <b>`                | 序列             | `Tuple( Lit(Bool(_)) Lit(Int(_)) Lit(_) )` |
|`<a>*` <br> `<a>+` <br> `<a>?` <br> `<a>{n}` <br> `<a>{n,m}` <br> `<a>{n,}` | 重复 <br> <br> <br> <br> <br><br> | `Array( _* )`, <br> `Block( Semi(_)+ )`, <br> `If(_, _, Block(_)?)`, <br> `Array( Lit(_){10} )`, <br> `Lit(_){5,10}`, <br> `Lit(Bool(_)){10,}` |
|`<a>#<name>`             | 命名子匹配       | `Lit(Int(_))#foo` `Lit(Int(_#bar))`        |

## 结果类型

许多 lint 需要超出上文模式语法所能表达的检查。例如，lint 可能想检查某节点是否由宏展开产生，或某节点上方是否没有注释。另一个例子是 lint 需要匹配两个值相同的节点（如 `almost_swapped` 等 lint 所需）。与其让用户把这些检查直接写进模式（可能使模式难以阅读），本方案允许用户为模式表达式的各部分命名。将模式与语法树节点匹配时，返回值会包含这些命名子模式所匹配节点的引用。这类似于正则表达式中的捕获组。

例如，给定如下模式

```rust
pattern!{
    // 匹配字符字面量
    my_pattern: Expr =
        Lit(Char(_#val_inner)#val)#val_outer
}
```

可按如下方式获取匹配子模式的节点引用：

```rust,ignore
...
fn check_expr(expr: &syntax::ast::Expr) {
    if let Some(result) = my_pattern(expr) {
        result.val_inner  // type: &char
        result.val        // type: &syntax::ast::Lit
        result.val_outer  // type: &syntax::ast::Expr
    }
}
```

`result` 结构体中的类型取决于模式。例如，如下模式

```rust
pattern!{
    // 匹配字符字面量数组
    my_pattern_seq: Expr =
        Array( Lit(_)*#foo )
}
```

匹配由任意数量字面量表达式组成的数组。由于这些表达式命名为 `foo`，结果结构体包含 `foo` 字段，其类型为表达式向量：

```rust,ignore
...
if let Some(result) = my_pattern_seq(expr) {
    result.foo        // type: Vec<&syntax::ast::Expr>
}
```

当名称仅在交替的一个分支中定义时，会出现另一种结果类型：

```rust
pattern!{
    // 匹配布尔或整数字面量表达式
    my_pattern_alt: Expr =
        Lit( Bool(_#bar) | Int(_) )
}
```

在上面的模式中，`bar` 名称仅在匹配布尔字面量时定义。若匹配整数字面量，则不会设置该名称。因此，结果结构体的 `bar` 字段为 option 类型：

```rust,ignore
...
if let Some(result) = my_pattern_alt(expr) {
    result.bar        // type: Option<&bool>
}
```

若多个交替分支中的名称类型兼容，也可在多个分支中使用同一名称：

```rust,ignore
pattern!{
    // 匹配布尔或整数字面量表达式
    my_pattern_mult: Expr =
        Lit(_#baz) | Array( Lit(_#baz) )
}
...
if let Some(result) = my_pattern_mult(expr) {
    result.baz        // type: &syntax::ast::Lit
}
```

命名子匹配使用**扁平**命名空间，这是有意为之。在上例中，两个不同子结构被赋给同一扁平名称。我预计对大多数 lint 而言，扁平命名空间已足够，且比层次化命名空间更易使用。

#### 两阶段

借助命名子模式，用户可分两阶段编写 lint。首先，模式语法产生粗粒度的可能匹配集合；第二阶段，可利用命名子模式引用做额外测试，例如断言某节点并非宏展开产生。

## 使用模式实现 Clippy lint

作为「真实世界」示例，我用模式重新实现了 `collapsible_if` lint。代码见[此处](https://github.com/fkohlgrueber/rust-clippy-pattern/blob/039b07ecccaf96d6aa7504f5126720d2c9cceddd/clippy_lints/src/collapsible_if.rs#L88-L163)。基于模式的版本通过了为 `collapsible_if` 编写的全部测试用例。

# 参考级说明

## 概览

下图展示所提方案主要部分之间的依赖关系：

```
                          模式语法
                                |
                                |  解析 / lowering
                                v
                           PatternTree
                                ^
                                |
                                |
                          IsMatch trait
                                |
                                |
             +---------------+-----------+---------+
             |               |           |         |
             v               v           v         v
        syntax::ast     rustc::hir      syn       ...
```

上一节描述的模式语法经解析 /  lowering 转换为所谓的 *PatternTree* 数据结构，它表示有效的语法树模式。将 *PatternTree* 与实际语法树（如 rust ast / hir 或 syn ast 等）匹配，通过 *IsMatch* trait 完成。

*PatternTree* 与 *IsMatch* trait 在以下章节中进一步介绍。

## PatternTree

本 RFC 的核心数据结构是 **PatternTree**。

它与 Rust 的 AST / HIR 类似，但有以下差异：

- PatternTree 不包含 `Span` 等解析信息
- PatternTree 可表示交替、序列与 optional

下面的代码展示当前 PatternTree 的简化版本：

> 注：当前实现见[此处](https://github.com/fkohlgrueber/pattern-matching/blob/dfb3bc9fbab69cec7c91e72564a63ebaa2ede638/pattern-match/src/pattern_tree.rs#L50-L96)。

```rust
pub enum Expr {
    Lit(Alt<Lit>),
    Array(Seq<Expr>),
    Block_(Alt<BlockType>),
    If(Alt<Expr>, Alt<BlockType>, Opt<Expr>),
    IfLet(
        Alt<BlockType>,
        Opt<Expr>,
    ),
}

pub enum Lit {
    Char(Alt<char>),
    Bool(Alt<bool>),
    Int(Alt<u128>),
}

pub enum Stmt {
    Expr(Alt<Expr>),
    Semi(Alt<Expr>),
}

pub enum BlockType {
    Block(Seq<Stmt>),
}
```

`Alt`、`Seq` 和 `Opt` 结构体如下：

> 注：当前实现见[此处](https://github.com/fkohlgrueber/pattern-matching/blob/dfb3bc9fbab69cec7c91e72564a63ebaa2ede638/pattern-match/src/matchers.rs#L35-L60)。

```rust,ignore
pub enum Alt<T> {
    Any,
    Elmt(Box<T>),
    Alt(Box<Self>, Box<Self>),
    Named(Box<Self>, ...)
}

pub enum Opt<T> {
    Any,  // 任意内容，但不是 None
    Elmt(Box<T>),
    None,
    Alt(Box<Self>, Box<Self>),
    Named(Box<Self>, ...)
}

pub enum Seq<T> {
    Any,
    Empty,
    Elmt(Box<T>),
    Repeat(Box<Self>, RepeatRange),
    Seq(Box<Self>, Box<Self>),
    Alt(Box<Self>, Box<Self>),
    Named(Box<Self>, ...)
}

pub struct RepeatRange {
    pub start: usize,
    pub end: Option<usize>  // 不包含上界
}
```

## 解析 / Lowering

`pattern!` 宏调用的输入先被解析为 `ParseTree`，再 lowering 为 `PatternTree`。

有效模式取决于 *PatternTree* 定义。例如，模式 `Lit(Bool(_)*)` 无效，因为 `Expr` 枚举的 `Lit` 变体参数类型为 `Any<Lit>`，不支持重复（`*`）。又如，`Array( Lit(_)* )` 是有效模式，因为 `Array` 的参数类型为 `Seq<Expr>`，允许序列与重复。

> 注：模式语法中的名称对应 *PatternTree* 枚举的**变体**。例如，上例中的 `Lit` 指 `Expr` 枚举的 `Lit` 变体（`Expr::Lit`），而非 `Lit` 枚举。

## IsMatch Trait

模式语法与 *PatternTree* 独立于具体语法树实现（rust ast / hir、syn 等）。回顾前文各节中的模式示例可见，模式中不包含任何特定语法树实现的信息。相比之下，Clippy lint 目前直接匹配 ast / hir 语法树节点，因此直接依赖其实现。

*PatternTree* 与具体语法树实现之间的桥梁是 `IsMatch` trait。它定义如何将 *PatternTree* 节点与具体语法树节点匹配。下面是 `IsMatch` trait 的简化实现：

```rust,ignore
pub trait IsMatch<O> {
    fn is_match(&self, other: &'o O) -> bool;
}
```

该 trait 需在 *PatternTree* 的每个枚举上实现（对应相应语法树类型）。例如，将 `ast::LitKind` 与 *PatternTree* 的 `Lit` 枚举匹配的 `IsMatch` 实现可能如下：

```rust
impl IsMatch<ast::LitKind> for Lit {
    fn is_match(&self, other: &ast::LitKind) -> bool {
        match (self, other) {
            (Lit::Char(i), ast::LitKind::Char(j)) => i.is_match(j),
            (Lit::Bool(i), ast::LitKind::Bool(j)) => i.is_match(j),
            (Lit::Int(i), ast::LitKind::Int(j, _)) => i.is_match(j),
            _ => false,
        }
    }
}
```

将当前 *PatternTree* 与 `syntax::ast` 匹配的全部 `IsMatch` 实现见[此处](https://github.com/fkohlgrueber/pattern-matching/blob/dfb3bc9fbab69cec7c91e72564a63ebaa2ede638/pattern-match/src/ast_match.rs)。

# 缺点

#### 性能

模式匹配代码目前未针对性能优化，可能比手写匹配代码更慢。此外，两阶段方式（先匹配粗粒度模式，再检查额外属性）可能比当前在一遍中同时检查结构与额外属性的做法更慢。例如，下面的 lint

```rust,ignore
pattern!{
    pat_if_without_else: Expr =
        If(
            _,
            Block(
                Expr( If(_, _, ())#inner )
                | Semi( If(_, _, ())#inner )
            )#then,
            ()
        )
}
...
fn check_expr(&mut self, cx: &EarlyContext<'_>, expr: &ast::Expr) {
    if let Some(result) = pat_if_without_else(expr) {
        if !block_starts_with_comment(cx, result.then) {
            ...
        }
}
```

先对模式匹配，再检查 `then` 块是否不以注释开头。使用 Clippy 当前做法，可以更早检查这些条件：

```rust,ignore
fn check_expr(&mut self, cx: &EarlyContext<'_>, expr: &ast::Expr) {
    if_chain! {
        if let ast::ExprKind::If(ref check, ref then, None) = expr.node;
        if !block_starts_with_comment(cx, then);
        if let Some(inner) = expr_block(then);
        if let ast::ExprKind::If(ref check_inner, ref content, None) = inner.node;
        then {
            ...
        }
    }
}
```

是否导致性能回退取决于实际模式。若成为问题，可扩展模式匹配算法以支持「早期过滤」（见未来可能性中的[早期过滤](#早期过滤)章节）。

话虽如此，我认为模式匹配性能在概念上没有固有限制。

#### 适用性

尽管我预计许多 lint 可用所提模式语法编写，但不太可能全部 lint 都能用模式表达。我怀疑仍会有 lint 需要手写自定义匹配代码。这会导致 Clippy 代码库中部分 lint 用模式实现、部分不用，存在不一致，可能被视为缺点。

# 理由与替代方案

与手动编写匹配代码相比，用语法树模式指定 lint 有若干优势。首先，语法树模式允许用户以简单、富有表现力的方式描述模式，使新手与专家都更容易编写新 lint，也更容易阅读 / 修改现有 lint。

另一优势是 lint 独立于具体语法树实现（如 AST / HIR 等）。当这些语法树实现变更时，只需调整 `IsMatch` trait 实现，现有 lint 可保持不变。这也意味着若 `IsMatch` trait 实现集成进编译器，编译器成功编译就需要更新这些实现。这可减少因编译器变更导致 Clippy 失效的次数。模式独立性的另一好处是：将 `EarlyLintPass` lint 转为 `LatePassLint` 时，无需重写整套模式匹配代码；事实上，模式可能无需任何改动即可工作。

## 替代方案

### 类 Rust 模式语法

所提模式语法要求用户了解 `PatternTree` 结构（与 AST / HIR 结构非常相似）以及模式语法本身。一种替代方案是引入与实际 Rust 语法类似的模式语法（可能类似 `quote!` 宏）。例如，匹配条件为 `false` 的 `if` 表达式的模式可能如下：

```rust,ignore
if false {
    #[*]
}
```

#### 问题

在本身已相当复杂的 Rust 语法上扩展用于指定模式的额外语法（交替、序列、重复、命名子匹配等），可能变得难以阅读且极难正确解析。

例如，匹配两侧均为 `0` 的二元运算的模式可能如下：

```
0 #[*:BinOpKind] 0
```

再考虑稍复杂的例子：

```
1 + 0 #[*:BinOpKind] 0
```

解析器需要知道 `#[*:BinOpKind]` 的优先级，因为它影响所得 AST 的结构。`1 + 0 + 0` 解析为 `(1 + 0) + 0`，而 `1 + 0 * 0` 解析为 `1 + (0 * 0)`。由于模式可以是任意 `BinOpKind`，优先级无法预先确定。

命名子匹配是另一个问题示例。看下面这个模式：

```rust,ignore
fn test() {
    1 #foo
}
```

`#foo` 指向哪个节点？`int`、`ast::Lit`、`ast::Expr` 还是 `ast::Stmt`？在类 Rust 语法中命名子模式很困难，因为许多 AST 节点没有可贴名称标签的语法元素。此时唯一合理的选择是把名称标签赋给最外层节点（上例中为 `ast::Stmt`），因为可通过最外层节点获取所有子节点信息。但这样访问内层节点（如 `ast::Lit`）又需要手动模式匹配。

总体而言，Rust 语法隐式包含大量代码结构。解析时会重建这些结构（例如按运算符优先级和从左到右规则重建二元运算），这也是解析复杂的原因之一。该方案的优势是用户写代码更简单。

编写*语法树模式*时，层次结构中的每个元素都可能有交替、重复等。在仍允许隐式结构的、对人友好的语法的同时尊重这一点，似乎非常复杂，甚至不可能。

开发此类语法还需要维护至少与 Rust 解析器同样复杂的自定义解析器。此外，Rust 语法未来的变更可能与这种语法不兼容。

总之，我认为开发此类语法会为解决相对较小的问题引入大量复杂性。

用户不了解 *PatternTree* 结构的问题，可通过工具解决：给定 Rust 程序，生成仅匹配该程序的模式（类似 Clippy author lint）。

对某些简单情况（如上文第一个示例），或许可以成功混合 Rust 与模式语法。这可在未来扩展中进一步探索。

# 既有实践

模式语法大量借鉴正则表达式（重复、交替、序列等）。

据我目前所见，其他 linter 也直接针对语法树数据结构实现 lint，与 Clippy 当前做法相同。因此我认为模式语法是*新的*，若有误请指正。

# 未决问题

#### 如何处理多重匹配？

将语法树节点与模式匹配时，可能存在多种匹配方式。简单示例如下模式：

```rust
pattern!{
    my_pattern: Expr =
        Array( _* Lit(_)+#literals)
}
```

该模式匹配以至少一个字面量结尾的数组。给定数组 `[x, 1, 2]`，`1` 应作为 `_*` 还是 `Lit(_)+` 的一部分匹配？差异很重要，因为命名子匹配 `#literals` 会包含 1 或 2 个元素，取决于如何匹配。正则表达式中，默认「贪婪」匹配，可选「非贪婪」。

我尚未深入研究，因为不确定这对大多数 lint 有多重要。当前实现仅返回找到的第一个匹配。

# 未来可能性

#### 实现其余 Rust 语法

当前项目仅实现 Rust 语法的一小部分。未来应逐步扩展以支持更多 lint。实现更多 Rust 语法需扩展 `PatternTree` 与 `IsMatch` 实现，但应相对直接。

#### 早期过滤

如*缺点/性能*章节所述，在模式匹配过程中允许额外检查可能有益。

下面的模式展示可能的形式：

```rust
pattern!{
    pat_if_without_else: Expr =
        If(
            _,
            Block(
                Expr( If(_, _, ())#inner )
                | Semi( If(_, _, ())#inner )
            )#then,
            ()
        )
    where
        !in_macro(#then.span);
}
```

与当前所提两阶段过滤相比，使用早期过滤时，条件（本例中为 `!in_macro(#then.span)`）会在 `Block(_)#then` 匹配后立即求值。

该方向的另一想法是引入反向引用语法。可用于要求模式中多个部分匹配相同值。例如，搜索 `a = a op b` 并建议改为 `a op= b` 的 `assign_op_pattern` lint 要求两处 `a` 相同。用 `=#...` 作为反向引用语法，该 lint 可如下实现：

```rust,ignore
pattern!{
    assign_op_pattern: Expr =
        Assign(_#target, Binary(_, =#target, _)
}
```

#### 匹配后代

许多 lint 目前实现自定义访问器，检查当前节点的任意子树（可能非直接后代）是否满足某些属性。所提模式语法无法表达这一点。扩展模式语法以支持如「包含至少两个 return 语句的函数」之类的模式，会是实用补充。

#### 交替的否定运算符

对于「非布尔字面量的字面量」这类模式，目前需列出除布尔外的所有交替。引入允许写 `Lit(!Bool(_))` 的否定运算符可能是个好主意。该模式等价于 `Lit( Char(_) | Int(_) )`（鉴于当前仅实现三种字面量类型）。

#### 函数式组合

模式目前没有组合概念，导致模式内重复。例如，collapsible-if 的某个模式目前必须写成：

```rust
pattern!{
    pat_if_else: Expr =
        If(
            _,
            _,
            Block_(
                Block(
                    Expr((If(_, _, _?) | IfLet(_, _?))#else_) |
                    Semi((If(_, _, _?) | IfLet(_, _?))#else_)
                )#block_inner
            )#block
        ) |
        IfLet(
            _,
            Block_(
                Block(
                    Expr((If(_, _, _?) | IfLet(_, _?))#else_) |
                    Semi((If(_, _, _?) | IfLet(_, _?))#else_)
                )#block_inner
            )#block
        )
}
```

若模式支持定义子模式函数，代码可简化为：

```rust
pattern!{
    fn expr_or_semi(expr: Expr) -> Stmt {
        Expr(expr) | Semi(expr)
    }
    fn if_or_if_let(then: Block, else: Opt<Expr>) -> Expr {
        If(_, then, else) | IfLet(then, else)
    }
    pat_if_else: Expr =
        if_or_if_let(
            _,
            Block_(
                Block(
                    expr_or_semi( if_or_if_let(_, _?)#else_ )
                )#block_inner
            )#block
        )
}
```

此外，`expr_or_semi` 等常见模式可在不同 lint 间共享。

#### Clippy Pattern Author

另一改进是创建工具：给定合法 Rust 语法，生成精确匹配该语法的模式。这会让编写模式的起步更容易。用户可查看若干 Rust 代码示例生成的模式，并据此编写匹配所有这些示例的模式。

这类似 clippy 的 author lint。

#### 支持其他语法

所提系统的大部分与语言无关。例如，模式语法也可用于描述其他编程语言的模式。

要支持其他语言语法，需实现另一个足够描述该语言 AST 的 `PatternTree`，并为该 `PatternTree` 与语言 AST 实现 `IsMatch`。

这一方面甚至可编写针对模式语法本身的 lint。例如，编写如下模式时

```rust
pattern!{
    my_pattern: Expr =
        Array( Lit(Bool(false)) Lit(Bool(false)) )
}
```

针对模式语法 AST 的 lint 可建议使用如下模式：

```rust
pattern!{
    my_pattern: Expr =
        Array( Lit(Bool(false)){2} )
}
```

未来 Clippy 可用该系统为宏等中的自定义语法提供 lint。
