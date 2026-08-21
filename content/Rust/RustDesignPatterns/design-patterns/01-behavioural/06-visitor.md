+++
title = "06-访问者"
date = 2026-08-18T22:10:00+08:00
weight = 30
type = "docs"
description = "访问者 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/visitor.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/visitor.html)

# 访问者

## 描述 {#description}

访问者封装了在异构对象集合上运行的算法。它允许在同一份数据上编写多种不同算法，而无需修改数据（或其主要行为）。

此外，访问者模式允许把对象集合的遍历与对每个对象执行的操作分离开。

## 示例 {#example}

```rust,ignore
// 我们将访问的数据
mod ast {
    pub enum Stmt {
        Expr(Expr),
        Let(Name, Expr),
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

// 抽象访问者
mod visit {
    use ast::*;

    pub trait Visitor<T> {
        fn visit_name(&mut self, n: &Name) -> T;
        fn visit_stmt(&mut self, s: &Stmt) -> T;
        fn visit_expr(&mut self, e: &Expr) -> T;
    }
}

use ast::*;
use visit::*;

// 一个具体实现示例——遍历 AST 并将其作为代码解释。
struct Interpreter;
impl Visitor<i64> for Interpreter {
    fn visit_name(&mut self, n: &Name) -> i64 {
        panic!()
    }
    fn visit_stmt(&mut self, s: &Stmt) -> i64 {
        match *s {
            Stmt::Expr(ref e) => self.visit_expr(e),
            Stmt::Let(..) => unimplemented!(),
        }
    }

    fn visit_expr(&mut self, e: &Expr) -> i64 {
        match *e {
            Expr::IntLit(n) => n,
            Expr::Add(ref lhs, ref rhs) => self.visit_expr(lhs) + self.visit_expr(rhs),
            Expr::Sub(ref lhs, ref rhs) => self.visit_expr(lhs) - self.visit_expr(rhs),
        }
    }
}
```

还可以实现更多访问者，例如类型检查器，而无需修改 AST 数据。

## 动机 {#motivation}

只要你想把算法应用到异构数据上，访问者模式就很有用。若数据是同构的，可以使用类似迭代器的模式。使用访问者对象（而不是函数式做法）使访问者可以带状态，从而在节点之间传递信息。

## 讨论 {#discussion}

`visit_*` 方法返回 void（与示例相反）很常见。在那种情况下，可以把遍历代码抽取出来，在各算法之间共享（并提供空操作的默认方法）。在 Rust 中，常见做法是为每种数据提供 `walk_*` 函数。例如：

```rust,ignore
pub fn walk_expr(visitor: &mut Visitor, e: &Expr) {
    match *e {
        Expr::IntLit(_) => {}
        Expr::Add(ref lhs, ref rhs) => {
            visitor.visit_expr(lhs);
            visitor.visit_expr(rhs);
        }
        Expr::Sub(ref lhs, ref rhs) => {
            visitor.visit_expr(lhs);
            visitor.visit_expr(rhs);
        }
    }
}
```

在其他语言（例如 Java）中，数据上常有一个 `accept` 方法来承担同样的职责。

## 参见 {#see-also}

访问者模式是大多数面向对象语言中的常见模式。

[Wikipedia 条目](https://en.wikipedia.org/wiki/Visitor_pattern)

[Fold](../02-creational/02-fold/) 模式与访问者类似，但会生成被访问数据结构的新版本。
