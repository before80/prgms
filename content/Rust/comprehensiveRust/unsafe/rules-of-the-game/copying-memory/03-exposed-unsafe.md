+++
title = "5.2.3 暴露的 Unsafe Rust"
date = 2026-08-11T11:30:00+08:00
weight = 530
type = "docs"
description = "03-暴露的 Unsafe Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/exposed-unsafe.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/exposed-unsafe.html)

# 5.2.3 暴露的 Unsafe Rust

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub fn copy(dest: &mut [u8], source: *const u8) {
    let source = {
        let mut len = 0;

        let mut end = source;
        while unsafe { *end != 0 } {
            len += 1;
            end = unsafe { end.add(1) };
        }

        unsafe { std::slice::from_raw_parts(source, len + 1) }
    };

    for (dest, src) in dest.iter_mut().zip(source) {
        *dest = *src;
    }
}

fn main() {
    let a = [114, 117, 115, 116].as_ptr();
    let b = &mut [82, 85, 83, 84, 0];

    println!("{}", String::from_utf8_lossy(b));
    copy(b, a);
    println!("{}", String::from_utf8_lossy(b));
}
```

> 从一处复制字节到另一处的功能保持不变。
>
> 「但我们需要手动创建切片。为此，首先要找到数据的末尾。
>
> 「由于处理的是文本，我们采用 C 语言以空字节（null）结尾的字符串约定。
>
> 编译这段代码，可以看到输出与之前相同。
>
> 「不健全的函数对某些输入仍可能正确运行。测试通过并不意味着函数是健全的。」
>
> 「有人能发现问题吗？」
>
> - 可读性：难以快速扫读代码
> - `source` 指针可能为 null
> - `source` 指针可能悬垂，即指向已释放或未初始化的内存
> - `source` 可能没有以 null 结尾
>
> 「假设不能修改函数签名，可以做哪些改进来解决这些问题？」
>
> - 空指针：添加空指针检查并提前返回
>   （`if source.is_null() { return; }`）
> - 可读性：使用经过充分测试的库，而不是自己实现「查找第一个 null 字节」
>
> 「但有些安全要求无法通过防御性检查来验证，例如：」
>
> - 悬垂指针
> - 缺少 null 终止字节
>
> 「如何让这个函数变得健全？」
>
> - 要么
>   - 将 `source` 参数的类型改为长度已知的类型，即像前一个例子那样使用切片。
> - 要么
>   - 将函数标记为 `unsafe`
>   - 记录安全前置条件

