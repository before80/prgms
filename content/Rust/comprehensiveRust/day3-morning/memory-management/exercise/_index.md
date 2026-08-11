+++
title = "2.8 练习：构建器类型"
date = 2026-08-11T11:30:00+08:00
weight = 131
type = "docs"
description = "练习：构建器类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/exercise.html](https://google.github.io/comprehensive-rust/memory-management/exercise.html)

# 2.8 练习：构建器类型

本例中，我们将实现一个拥有其全部数据的复杂数据类型。我们使用「构建器模式」（builder pattern），通过便捷函数逐步构建新值。

请补全缺失部分。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
enum Language {
    Rust,
    Java,
    Perl,
}

#[derive(Clone, Debug)]
struct Dependency {
    name: String,
    version_expression: String,
}

/// 软件包的表示。
#[derive(Debug)]
struct Package {
    name: String,
    version: String,
    authors: Vec<String>,
    dependencies: Vec<Dependency>,
    language: Option<Language>,
}

impl Package {
    /// 将该包表示为依赖项，供构建其他包时使用。
    fn to_dependency(&self) -> Dependency {
        todo!("1")
    }
}

/// Package 的构建器。使用 `build()` 创建 `Package` 本身。
struct PackageBuilder(Package);

impl PackageBuilder {
    fn new(name: impl Into<String>) -> Self {
        todo!("2")
    }

    /// 设置包版本。
    fn version(mut self, version: impl Into<String>) -> Self {
        self.0.version = version.into();
        self
    }

    /// 设置包作者。
    fn authors(mut self, authors: Vec<String>) -> Self {
        todo!("3")
    }

    /// 追加一个依赖项。
    fn dependency(mut self, dependency: Dependency) -> Self {
        todo!("4")
    }

    /// 设置语言。若未设置，language 默认为 None。
    fn language(mut self, language: Language) -> Self {
        todo!("5")
    }

    fn build(self) -> Package {
        self.0
    }
}

fn main() {
    let base64 = PackageBuilder::new("base64").version("0.13").build();
    dbg!(&base64);
    let log =
        PackageBuilder::new("log").version("0.4").language(Language::Rust).build();
    dbg!(&log);
    let serde = PackageBuilder::new("serde")
        .authors(vec!["djmitche".into()])
        .version(String::from("4.0"))
        .dependency(base64.to_dependency())
        .dependency(log.to_dependency())
        .build();
    dbg!(serde);
}
```
