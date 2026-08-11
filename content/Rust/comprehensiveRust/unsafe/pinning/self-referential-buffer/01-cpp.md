+++
title = "8.7.1 C++ 实现"
date = 2026-08-11T11:30:00+08:00
weight = 554
type = "docs"
description = "01-C++ 实现 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/cpp.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/cpp.html)

# 8.7.1 C++ 实现

```cpp,editable,ignore
#include <cstddef>
#include <cstring>

class SelfReferentialBuffer {
    std::byte data[1024];
    std::byte* cursor = data;
    
public:
    SelfReferentialBuffer(SelfReferentialBuffer&& other) 
        : cursor{data + (other.cursor - other.data)}
    {
        std::memcpy(data, other.data, 1024);
    }
};
```

可在 [Compiler Explorer](https://godbolt.org/z/ascME6aje) 上查看

> `SelfReferentialBuffer` 包含两个成员：`data` 是一 KB 内存，`cursor` 是指向 `data` 的指针。
>
> 其移动构造函数确保 cursor 更新到新的内存地址。
>
> 这种类型在 Rust 中不易表达。

