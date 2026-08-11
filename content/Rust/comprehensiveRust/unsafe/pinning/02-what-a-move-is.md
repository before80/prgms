+++
title = "8.2 什么是移动"
date = 2026-08-11T11:30:00+08:00
weight = 548
type = "docs"
description = "02-什么是移动 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/what-a-move-is.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/what-a-move-is.html)

# 8.2 什么是移动

即使对于未实现 `Copy` 的类型，移动也始终是按位拷贝：

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, Default)]
pub struct DynamicBuffer {
    data: Vec<u8>,
    position: usize,
};

pub fn move_and_inspect(x: DynamicBuffer) { println!("{x:?}"); }

pub fn main() {
   let a = DynamicBuffer::default();
   let mut b = a;
   b.data.push(b'R');
   b.data.push(b'U');
   b.data.push(b'S');
   b.data.push(b'T');
   move_and_inspect(b);
}
```

调用 `move_and_inspect()` 时生成的 [LLVM IR]：

```llvm
call void @llvm.memcpy.p0.p0.i64(ptr align 8 %_12, ptr align 8 %b, i64 32, i1 false)
invoke void @move_and_inspect(ptr align 8 %_12)
```

- 从变量 `%b` 到 `%_12` 的 `memcpy`
- 使用 `%_12`（拷贝）调用 `move_and_inspect`

> 注意 `DynamicBuffer` 并未实现 `Copy`。
>
> 推论：值的内存地址并不稳定。
>
> 要展示移动是按位拷贝，可以[在 playground 中打开代码][LLVM IR]查看，或使用 [Compiler Explorer]。
>
> 偏好汇编输出的可选内容：
>
> Compiler Explorer 适合讨论生成的汇编，并将光标聚焦在 `main` 函数第 128–136 行的汇编输出上（应以粉色高亮）。
>
> `move_and_inspect` 的相关生成代码：
>
> ```assembly
> mov     rax, qword ptr [rsp + 16]
> mov     qword ptr [rsp + 48], rax    
> mov     rax, qword ptr [rsp + 24]
> mov     qword ptr [rsp + 56], rax
> movups  xmm0, xmmword ptr [rsp]
> movaps  xmmword ptr [rsp + 32], xmm0
> lea     rdi, [rsp + 32]
> call    qword ptr [rip + move_and_inspect@GOTPCREL]
> ```


[LLVM IR]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=6f587283e8e0ec02f1ea8e871fc9ac72
[The Compiler Explorer]: https://rust.godbolt.org/z/6o6nP7do4
