+++
title = "19-推断类型"
date = 2026-08-18T08:45:00+08:00
weight = 84
type = "docs"
description = "推断类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/inferred.html](https://doc.rust-lang.org/reference/types/inferred.html)

r[type.inferred]
# 推断类型

r[type.inferred.syntax]
```grammar,types
InferredType -> `_`
```

r[type.inferred.intro]
推断类型要求编译器在可能的情况下，根据周围可用信息来推断类型。

> [!EXAMPLE]
> 推断类型常用于泛型参数：
>
> ```rust
> let x: Vec<_> = (0..10).collect();
> ```

r[type.inferred.constraint]
推断类型不能用在项的签名中。

<!--
  这里还应补充什么？
  我所知的唯一文档是 https://rustc-dev-guide.rust-lang.org/type-inference.html
  某处应该有对类型推断的更广泛讨论。
-->
