+++
title = "3.6 练习：GUI 库的模块划分"
date = 2026-08-11T11:30:00+08:00
weight = 176
type = "docs"
description = "练习：GUI 库的模块划分 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/exercise.html](https://google.github.io/comprehensive-rust/modules/exercise.html)

# 3.6 练习：GUI 库的模块划分

在本练习中，你将重组一个小型 GUI 库的实现。该库定义了 `Widget` trait 以及若干实现，还有一个 `main` 函数。

通常会把每个类型或一组密切相关的类型放进各自的模块，因此每种 widget 类型都应有自己的模块。

## Cargo 设置

Rust playground 只支持单个文件，因此需要在本地文件系统上创建一个 Cargo 项目：

```shell
cargo init gui-modules
cd gui-modules
cargo run
```

编辑生成的 `src/main.rs` 以添加 `mod` 声明，并在 `src` 目录下增加额外文件。

## 源码

下面是该 GUI 库的单模块实现：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Widget {
    /// `self` 的自然宽度。
    fn width(&self) -> usize;

    /// 将 widget 绘制到缓冲区。
    fn draw_into(&self, buffer: &mut dyn std::fmt::Write);

    /// 将 widget 绘制到标准输出。
    fn draw(&self) {
        let mut buffer = String::new();
        self.draw_into(&mut buffer);
        println!("{buffer}");
    }
}

pub struct Label {
    label: String,
}

impl Label {
    fn new(label: &str) -> Label {
        Label { label: label.to_owned() }
    }
}

pub struct Button {
    label: Label,
}

impl Button {
    fn new(label: &str) -> Button {
        Button { label: Label::new(label) }
    }
}

pub struct Window {
    title: String,
    widgets: Vec<Box<dyn Widget>>,
}

impl Window {
    fn new(title: &str) -> Window {
        Window { title: title.to_owned(), widgets: Vec::new() }
    }

    fn add_widget(&mut self, widget: Box<dyn Widget>) {
        self.widgets.push(widget);
    }

    fn inner_width(&self) -> usize {
        std::cmp::max(
            self.title.chars().count(),
            self.widgets.iter().map(|w| w.width()).max().unwrap_or(0),
        )
    }
}

impl Widget for Window {
    fn width(&self) -> usize {
        // 为边框额外加 4 的内边距
        self.inner_width() + 4
    }

    fn draw_into(&self, buffer: &mut dyn std::fmt::Write) {
        let mut inner = String::new();
        for widget in &self.widgets {
            widget.draw_into(&mut inner);
        }

        let inner_width = self.inner_width();

        // TODO: 将 draw_into 改为返回 Result<(), std::fmt::Error>，然后在这里
        // 用 ? 运算符代替 .unwrap()。
        writeln!(buffer, "+-{:-<inner_width$}-+", "").unwrap();
        writeln!(buffer, "| {:^inner_width$} |", &self.title).unwrap();
        writeln!(buffer, "+={:=<inner_width$}=+", "").unwrap();
        for line in inner.lines() {
            writeln!(buffer, "| {:inner_width$} |", line).unwrap();
        }
        writeln!(buffer, "+-{:-<inner_width$}-+", "").unwrap();
    }
}

impl Widget for Button {
    fn width(&self) -> usize {
        self.label.width() + 8 // 稍微加点内边距
    }

    fn draw_into(&self, buffer: &mut dyn std::fmt::Write) {
        let width = self.width();
        let mut label = String::new();
        self.label.draw_into(&mut label);

        writeln!(buffer, "+{:-<width$}+", "").unwrap();
        for line in label.lines() {
            writeln!(buffer, "|{:^width$}|", &line).unwrap();
        }
        writeln!(buffer, "+{:-<width$}+", "").unwrap();
    }
}

impl Widget for Label {
    fn width(&self) -> usize {
        self.label.lines().map(|line| line.chars().count()).max().unwrap_or(0)
    }

    fn draw_into(&self, buffer: &mut dyn std::fmt::Write) {
        writeln!(buffer, "{}", &self.label).unwrap();
    }
}

fn main() {
    let mut window = Window::new("Rust GUI Demo 1.23");
    window.add_widget(Box::new(Label::new("This is a small text GUI demo.")));
    window.add_widget(Box::new(Button::new("Click me!")));
    window.draw();
}
```

> 鼓励学员按自己觉得自然的方式划分代码，并熟悉所需的 `mod`、`use` 与 `pub` 声明。之后再讨论哪种组织方式最符合惯用法。

