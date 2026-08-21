+++
title = "01-命令"
date = 2026-08-18T22:10:00+08:00
weight = 25
type = "docs"
description = "命令 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/command.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/command.html)

# 命令

## 描述 {#description}

命令模式的基本思想是把操作分离成独立的对象，并把它们作为参数传递。

## 动机 {#motivation}

假设我们有一系列封装为对象的操作或事务。我们希望这些操作或命令稍后在不同时间、按某种顺序执行或调用。这些命令也可能由某些事件触发。例如，用户按下按钮，或数据包到达。此外，这些命令可能是可撤销的。这对编辑器一类的操作很有用。我们可能还想存储已执行命令的日志，以便系统崩溃后重新应用这些更改。

## 示例 {#example}

定义两个数据库操作 `create table` 和 `add field`。每个操作都是一条命令，并且知道如何撤销，例如 `drop table` 和 `remove field`。当用户调用数据库迁移操作时，各命令按既定顺序执行；当用户调用回滚操作时，整组命令按相反顺序调用。

## 做法：使用 trait 对象 {#approach-using-trait-objects}

我们定义一个公共 trait，用 `execute` 和 `rollback` 两个操作封装命令。所有命令 `struct` 都必须实现该 trait。

```rust
pub trait Migration {
    fn execute(&self) -> &str;
    fn rollback(&self) -> &str;
}

pub struct CreateTable;
impl Migration for CreateTable {
    fn execute(&self) -> &str {
        "create table"
    }
    fn rollback(&self) -> &str {
        "drop table"
    }
}

pub struct AddField;
impl Migration for AddField {
    fn execute(&self) -> &str {
        "add field"
    }
    fn rollback(&self) -> &str {
        "remove field"
    }
}

struct Schema {
    commands: Vec<Box<dyn Migration>>,
}

impl Schema {
    fn new() -> Self {
        Self { commands: vec![] }
    }

    fn add_migration(&mut self, cmd: Box<dyn Migration>) {
        self.commands.push(cmd);
    }

    fn execute(&self) -> Vec<&str> {
        self.commands.iter().map(|cmd| cmd.execute()).collect()
    }
    fn rollback(&self) -> Vec<&str> {
        self.commands
            .iter()
            .rev() // 反转迭代器方向
            .map(|cmd| cmd.rollback())
            .collect()
    }
}

fn main() {
    let mut schema = Schema::new();

    let cmd = Box::new(CreateTable);
    schema.add_migration(cmd);
    let cmd = Box::new(AddField);
    schema.add_migration(cmd);

    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

## 做法：使用函数指针 {#approach-using-function-pointers}

另一种做法是把每条命令做成不同的函数，并保存函数指针，以便稍后在不同时间调用。由于函数指针实现了 `Fn`、`FnMut` 和 `FnOnce` 这三个 trait，我们也可以传递并存储闭包，而不是函数指针。

```rust
type FnPtr = fn() -> String;
struct Command {
    execute: FnPtr,
    rollback: FnPtr,
}

struct Schema {
    commands: Vec<Command>,
}

impl Schema {
    fn new() -> Self {
        Self { commands: vec![] }
    }
    fn add_migration(&mut self, execute: FnPtr, rollback: FnPtr) {
        self.commands.push(Command { execute, rollback });
    }
    fn execute(&self) -> Vec<String> {
        self.commands.iter().map(|cmd| (cmd.execute)()).collect()
    }
    fn rollback(&self) -> Vec<String> {
        self.commands
            .iter()
            .rev()
            .map(|cmd| (cmd.rollback)())
            .collect()
    }
}

fn add_field() -> String {
    "add field".to_string()
}

fn remove_field() -> String {
    "remove field".to_string()
}

fn main() {
    let mut schema = Schema::new();
    schema.add_migration(|| "create table".to_string(), || "drop table".to_string());
    schema.add_migration(add_field, remove_field);
    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

## 做法：使用 `Fn` trait 对象 {#approach-using-fn-trait-objects}

最后，我们也可以不定义公共的命令 trait，而是把每个实现了 `Fn` trait 的命令分别存入向量。

```rust
type Migration<'a> = Box<dyn Fn() -> &'a str>;

struct Schema<'a> {
    executes: Vec<Migration<'a>>,
    rollbacks: Vec<Migration<'a>>,
}

impl<'a> Schema<'a> {
    fn new() -> Self {
        Self {
            executes: vec![],
            rollbacks: vec![],
        }
    }
    fn add_migration<E, R>(&mut self, execute: E, rollback: R)
    where
        E: Fn() -> &'a str + 'static,
        R: Fn() -> &'a str + 'static,
    {
        self.executes.push(Box::new(execute));
        self.rollbacks.push(Box::new(rollback));
    }
    fn execute(&self) -> Vec<&str> {
        self.executes.iter().map(|cmd| cmd()).collect()
    }
    fn rollback(&self) -> Vec<&str> {
        self.rollbacks.iter().rev().map(|cmd| cmd()).collect()
    }
}

fn add_field() -> &'static str {
    "add field"
}

fn remove_field() -> &'static str {
    "remove field"
}

fn main() {
    let mut schema = Schema::new();
    schema.add_migration(|| "create table", || "drop table");
    schema.add_migration(add_field, remove_field);
    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

## 讨论 {#discussion}

如果命令较小，可以定义为函数或以闭包传入，那么使用函数指针可能更合适，因为它不会走动态分发。但如果命令是带有一组函数和变量、定义为独立模块的整个 struct，那么使用 trait 对象会更合适。实际应用可见 [`actix`](https://actix.rs/)，它在为路由注册处理函数时使用 trait 对象。若使用 `Fn` trait 对象，则可以像使用函数指针时一样创建和使用命令。

就性能而言，性能与代码简洁性、组织结构之间始终存在权衡。静态分发性能更快，而动态分发在组织应用程序时提供了灵活性。

## 参见 {#see-also}

- [命令模式](https://en.wikipedia.org/wiki/Command_pattern)

- [`command` 模式的另一个示例](https://web.archive.org/web/20210223131236/https://chercher.tech/rust/command-design-pattern-rust)
