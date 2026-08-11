+++
title = "4.2.16 解题：拆解问题"
date = 2026-08-11T11:30:00+08:00
weight = 496
type = "docs"
description = "16-解题：拆解问题 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/problem-solving.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/problem-solving.html)

# 4.2.16 解题：拆解问题

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 问题：实现一个 GUI API

// 问题：绘图 API 的最小有用行为是什么？
pub trait DrawApi {
    fn arc(&self, center: [f32; 2], radius: f32, start_angle: f32, end_angle: f32);
    fn line(&self, start: [f32; 2], end: [f32; 2]);
}

pub struct TextDraw;

impl DrawApi for TextDraw {
    fn arc(&self, center: [f32; 2], radius: f32, start_angle: f32, end_angle: f32) {
        println!("arc of radius ")
    }

    fn line(&self, start: [f32; 2], end: [f32; 2]) { /* ... */
    }
}

// 问题：对用户而言怎样的 API 更好？

pub trait Draw {
    fn draw<T: DrawApi>(&self, surface: &mut T);
}

pub struct Rect {
    start: [f32; 2],
    end: [f32; 2],
}

impl Draw for Rect {
    fn draw<T: DrawApi>(&self, surface: &mut T) {
        surface.line([self.start[0], self.start[1]], [self.end[0], self.start[1]]);
        surface.line([self.end[0], self.start[1]], [self.end[0], self.end[1]]);
        surface.line([self.end[0], self.end[1]], [self.start[0], self.end[1]]);
        surface.line([self.start[0], self.end[1]], [self.start[0], self.start[1]]);
    }
}
```

> - 你已经擅长拆解问题，但很可能习惯了先伸手拿 OOP 风格的方法。
>
> 这并不是剧烈变化，只是需要重新安排你接近问题的顺序。
>
> - 先尝试用「泛型 & Trait」或「枚举」解题。
>
>   问题是否需要一组特定类型？枚举可能是最干净的解法。
>
>   问题是否真的关心所涉类型的细节，还是可以把焦点放在行为上？
>
> - 围绕「实现某事所需的最小可行知识量」来组织解题。
>
>   是否已有适合该用例的 trait？若有，就用它！
>
> - 若确实需要异构集合，就用！它们在 Rust 中作为工具存在是有原因的。
>
>   注意 XY 问题：某个问题看似最容易用某一种方案解决，但可能并未触及根因，并可能在未来引出新的难题。
>
>   也就是说，在承诺使用 trait 对象做动态分发之前，先确认这正是你需要的。
>
>   在承诺使用 trait 之前，也先确认 trait 正是你需要的。

