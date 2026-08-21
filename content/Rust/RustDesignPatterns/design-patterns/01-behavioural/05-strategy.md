+++
title = "05-策略"
date = 2026-08-18T22:10:00+08:00
weight = 29
type = "docs"
description = "策略 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/strategy.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/strategy.html)

# 策略

## 描述 {#description}

[策略设计模式](https://en.wikipedia.org/wiki/Strategy_pattern) 是一种实现关注点分离的技术。它还可以通过
[依赖倒置](https://en.wikipedia.org/wiki/Dependency_inversion_principle) 解耦软件模块。

策略模式的基本思想是：给定一个求解特定问题的算法，我们只在抽象层面定义算法骨架，并把具体算法实现分离到不同部分。

这样，使用该算法的客户端可以选择具体实现，而总体算法流程保持不变。换句话说，类的抽象规范不依赖于派生类的具体实现，但具体实现必须遵守抽象规范。这就是我们称之为「依赖倒置」的原因。

## 动机 {#motivation}

设想我们正在做一个每月生成报告的项目。报告需要以不同格式（策略）生成，例如 `JSON` 或 `Plain Text`。但需求会随时间变化，我们无法预知将来会有怎样的要求。例如，可能需要以一种全新格式生成报告，或只修改现有格式之一。

## 示例 {#example}

在本例中，不变量（或抽象）是 `Formatter` 和 `Report`，而 `Text` 和 `Json` 是策略 struct。这些策略必须实现 `Formatter` trait。

```rust
use std::collections::HashMap;

type Data = HashMap<String, u32>;

trait Formatter {
    fn format(&self, data: &Data, buf: &mut String);
}

struct Report;

impl Report {
    // 本应使用 Write，但为了忽略错误处理，我们仍使用 String
    fn generate<T: Formatter>(g: T, s: &mut String) {
        // 后端操作……
        let mut data = HashMap::new();
        data.insert("one".to_string(), 1);
        data.insert("two".to_string(), 2);
        // 生成报告
        g.format(&data, s);
    }
}

struct Text;
impl Formatter for Text {
    fn format(&self, data: &Data, buf: &mut String) {
        for (k, v) in data {
            let entry = format!("{k} {v}\n");
            buf.push_str(&entry);
        }
    }
}

struct Json;
impl Formatter for Json {
    fn format(&self, data: &Data, buf: &mut String) {
        buf.push('[');
        for (k, v) in data.into_iter() {
            let entry = format!(r#"{{"{}":"{}"}}"#, k, v);
            buf.push_str(&entry);
            buf.push(',');
        }
        if !data.is_empty() {
            buf.pop(); // 去掉末尾多余的逗号
        }
        buf.push(']');
    }
}

fn main() {
    let mut s = String::from("");
    Report::generate(Text, &mut s);
    assert!(s.contains("one 1"));
    assert!(s.contains("two 2"));

    s.clear(); // 复用同一缓冲区
    Report::generate(Json, &mut s);
    assert!(s.contains(r#"{"one":"1"}"#));
    assert!(s.contains(r#"{"two":"2"}"#));
}
```

## 优点 {#advantages}

主要优点是关注点分离。例如在本例中，`Report` 对 `Json` 和 `Text` 的具体实现一无所知，而输出实现也不关心数据如何预处理、存储和获取。它们只需知道要实现的特定 trait 及其定义具体算法实现、处理结果的方法，即 `Formatter` 和 `format(...)`。

## 缺点 {#disadvantages}

每种策略都必须至少实现一个模块，因此模块数量会随策略数量增加。若可选策略很多，用户就必须了解各策略之间的差异。

## 讨论 {#discussion}

在前面的例子中，所有策略都实现在同一个文件里。提供不同策略的方式包括：

- 全部放在一个文件中（如本例所示，类似于分成模块）
- 分成模块，例如 `formatter::json` 模块、`formatter::text` 模块
- 使用编译器 feature 标志，例如 `json` feature、`text` feature
- 分成 crate，例如 `json` crate、`text` crate

Serde crate 是 `Strategy` 模式实际运用的好例子。Serde 允许通过手动为我们的类型实现 `Serialize` 和 `Deserialize` trait，对序列化行为进行[完全自定义](https://serde.rs/custom-serialization.html)。例如，我们可以轻易把 `serde_json` 换成 `serde_cbor`，因为它们暴露了类似的方法。这使得辅助 crate `serde_transcode` 更加有用、也更符合人体工学。

不过，在 Rust 中设计该模式并不一定要用 trait。

下面这个玩具示例用 Rust `closures` 演示了策略模式的思想：

```rust
struct Adder;
impl Adder {
    pub fn add<F>(x: u8, y: u8, f: F) -> u8
    where
        F: Fn(u8, u8) -> u8,
    {
        f(x, y)
    }
}

fn main() {
    let arith_adder = |x, y| x + y;
    let bool_adder = |x, y| {
        if x == 1 || y == 1 {
            1
        } else {
            0
        }
    };
    let custom_adder = |x, y| 2 * x + y;

    assert_eq!(9, Adder::add(4, 5, arith_adder));
    assert_eq!(0, Adder::add(0, 0, bool_adder));
    assert_eq!(5, Adder::add(1, 3, custom_adder));
}
```

事实上，Rust 已经在 `Option` 的 `map` 方法中使用了这一思想：

```rust
fn main() {
    let val = Some("Rust");

    let len_strategy = |s: &str| s.len();
    assert_eq!(4, val.map(len_strategy).unwrap());

    let first_byte_strategy = |s: &str| s.bytes().next().unwrap();
    assert_eq!(82, val.map(first_byte_strategy).unwrap());
}
```

## 参见 {#see-also}

- [策略模式](https://en.wikipedia.org/wiki/Strategy_pattern)
- [依赖注入](https://en.wikipedia.org/wiki/Dependency_injection)
- [基于策略的设计](https://en.wikipedia.org/wiki/Modern_C++_Design#Policy-based_design)
- [用策略模式在 Rust 中实现面向空间应用的 TCP 服务器](https://web.archive.org/web/20231003171500/https://robamu.github.io/posts/rust-strategy-pattern/)
