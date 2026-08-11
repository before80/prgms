+++
title = "3.4.3.4 Serializer：完整实现"
date = 2026-08-11T11:30:00+08:00
weight = 452
type = "docs"
description = "04-Serializer：完整实现 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/complete.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/typestate-pattern/typestate-generics/complete.html)

# 3.4.3.4 Serializer：完整实现

## Serializer：完整实现

回顾最初期望的流程：

```bob
    +-----------+   +---------+------------+-----+
    |           |   |         |            |     |
    V           |   V         |            V     |
                +                                |
serializer --> structure --> property --> list +-+

    |           |   ^           |          ^
    V           |   |           |          |
                |   +-----------+          |
  String        |                          |
                +--------------------------+
```

现在可以直接在序列化器的类型中看到这一点：

```bob
                                                     +------+
                                             finish  |      |
                          serialize          struct  V      |
                          struct
+--------------------+ --------------> +-------------------------+ <---------------+
| "Serializer<Root>" |                 | "Serializer<Struct<S>>" |                 |
+--------------------+ <-------------- +-------------------------+ <-----------+   |
                         finish struct                                         |   |
         |                                  |  serialize   |                   |   |
         |                       +----------+  property    V        serialize  |   |
         |                       |                                  string or  |   |
finish   |                       |   +---------------------------+  struct     |   |
         V                       |   | "Serializer<Property<S>>" | ------------+   |
                         finish  |   +---------------------------+                 |
     +--------+          struct  |                                                 |
     | String |                  |             serialize   |                       |
     +--------+                  |             list        V                       |
                                 |                                    finish       |
                                 |       +-----------------------+    list         |
                                 +-----> | "Serializer<List<S>>" | ----------------+
                                         +-----------------------+
                                              serialize
                                            | list or string  ^
                                            | or finish list  |
                                            +-----------------+
```

`Serializer` 及其全部状态的完整实现代码见
[此 Rust playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=c9cbb831cd05fe9db4ce42713c83ca16)。

> - 此模式并非银弹。它仍允许以下问题：
>   - 空或无效的属性名（可用
>     [newtype 模式](../../newtype-pattern.md)
>     修复）
>   - 重复的属性名（可在 `Struct<S>` 中跟踪并通过 `Result` 处理）
>
> - 若发生校验失败，我们也可以将方法签名改为返回 `Result`，以允许恢复：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   struct PropertySerializeError<S> {
>       kind: PropertyError,
>       serializer: Serializer<Struct<S>>,
>   }
>
>   impl<S> Serializer<Struct<S>> {
>       fn serialize_property(
>           self,
>           name: &str,
>       ) -> Result<Serializer<Property<Struct<S>>>, PropertySerializeError<S>> {
>           /* ... */
>       }
>   }
>   ```
>
> - 尽管此 API 很强大，但并不总是符合人体工学。生产级序列化器通常偏好更简单的 API，并将 typestate 模式留给强制关键不变量。
>
> - 一个优秀的现实世界例子是
>   [`rustls::ClientConfig`](https://docs.rs/rustls/latest/rustls/client/struct.ClientConfig.html#method.builder)，
>   它用带泛型的 typestate 引导用户完成安全且正确的配置步骤。

