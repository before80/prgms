+++
title = "02-Fold"
date = 2026-08-18T22:10:00+08:00
weight = 33
type = "docs"
description = "Fold — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/creational/fold.html](https://rust-unofficial.github.io/patterns/patterns/creational/fold.html)

# Fold

## 描述 {#description}

对数据集合中的每一项运行算法以创建新项，从而创建整个新集合。

此处的词源对我来说并不清楚。术语 “fold” 和 “folder” 用于 Rust 编译器，但在我看来它更像通常意义上的 map，而不是 fold。更多细节见下方讨论。

## 示例 {#example}

```rust,ignore
// 我们将要 fold 的数据，一个简单的 AST。
mod ast {
    pub enum Stmt {
        Expr(Box<Expr>),
        Let(Box<Name>, Box<Expr>),
    }

    pub struct Name {
        value: String,
    }

    pub enum Expr {
        IntLit(i64),
        Add(Box<Expr>, Box<Expr>),
        Sub(Box<Expr>, Box<Expr>),
    }
}

// 抽象 folder
mod fold {
    use ast::*;

    pub trait Folder {
        // 叶节点直接返回节点本身。在某些情况下，内节点也可以这样做。
        fn fold_name(&mut self, n: Box<Name>) -> Box<Name> { n }
        // 通过 fold 其子节点来创建新的内节点。
        fn fold_stmt(&mut self, s: Box<Stmt>) -> Box<Stmt> {
            match *s {
                Stmt::Expr(e) => Box::new(Stmt::Expr(self.fold_expr(e))),
                Stmt::Let(n, e) => Box::new(Stmt::Let(self.fold_name(n), self.fold_expr(e))),
            }
        }
        fn fold_expr(&mut self, e: Box<Expr>) -> Box<Expr> { ... }
    }
}

use fold::*;
use ast::*;

// 一个具体实现示例——把每个名称重命名为 'foo'。
struct Renamer;
impl Folder for Renamer {
    fn fold_name(&mut self, n: Box<Name>) -> Box<Name> {
        Box::new(Name { value: "foo".to_owned() })
    }
    // 其他节点使用默认方法。
}
```

对 AST 运行 `Renamer` 的结果是一棵与旧 AST 相同的新 AST，但每个名称都变成了 `foo`。真实场景中的 folder 可能在结构体自身中保存节点之间的状态。

也可以定义 folder，将一种数据结构映射到另一种（通常相似的）数据结构。例如，我们可以把 AST fold 成 HIR 树（HIR 表示高层中间表示，high-level intermediate representation）。

## 动机 {#motivation}

常见需求是通过对结构中的每个节点执行某些操作来映射数据结构。对于简单数据结构上的简单操作，可以用 `Iterator::map` 完成。对于更复杂的操作——例如较早的节点会影响对较晚节点的操作，或对数据结构的遍历并不平凡——使用 fold 模式更为合适。

与访问者模式类似，fold 模式允许我们将数据结构的遍历与对每个节点执行的操作分离。

## 讨论 {#discussion}

以这种方式映射数据结构在函数式语言中很常见。在 OO 语言中，更常见的是原地修改数据结构。Rust 中“函数式”做法很常见，主要是因为更偏好不可变性。使用新的数据结构而非修改旧的，在大多数情况下更容易对代码进行推理。

通过改变 `fold_*` 方法接受节点的方式，可以调整效率与可复用性之间的权衡。

在上面的示例中，我们操作的是 `Box` 指针。由于它们独占其数据，原始数据结构副本无法被复用。另一方面，如果节点未改变，复用它会非常高效。

若我们操作借用引用，则可以复用原始数据结构；然而，即使节点未改变也必须克隆，这可能代价高昂。

使用引用计数指针可以兼得两者之长——我们可以复用原始数据结构，且不必克隆未改变的节点。然而，它们用起来人体工程学较差，并意味着数据结构不能是可变的。

## 参见 {#see-also}

迭代器具有 `fold` 方法，不过它是将数据结构折叠成一个值，而不是折叠成新的数据结构。迭代器的 `map` 更接近本 fold 模式。

在其他语言中，fold 通常按 Rust 迭代器的含义使用，而不是本模式。一些函数式语言拥有对数据结构执行灵活映射的强大构造。

[访问者](../01-behavioural/06-visitor/)模式与 fold 密切相关。
它们都包含遍历数据结构并对每个节点执行操作的概念。然而，访问者既不创建新的数据结构，也不消费旧的数据结构。
