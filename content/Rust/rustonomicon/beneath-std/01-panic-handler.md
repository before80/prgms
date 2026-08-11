+++
title = "12.1 #[panic_handler]"
date = 2026-08-06T17:08:00+08:00
weight = 63
type = "docs"
description = "自定义 panic 处理函数"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# #[panic_handler]


> 原文链接: [https://doc.rust-lang.org/nomicon/panic-handler.html](https://doc.rust-lang.org/nomicon/panic-handler.html)


　　`#[panic_handler]` 用于定义 `#![no_std]` 应用中 `panic!` 的行为。`#[panic_handler]` 必须应用于签名为 `fn(&PanicInfo) -> !` 的函数，且二进制 / dylib / cdylib crate 的依赖图中该函数必须*恰好出现一次*。`PanicInfo` 的 API 见 [API 文档]。

[API docs]: ../core/panic/struct.PanicInfo.html

　　鉴于 `#![no_std]` 应用没有*标准*输出，且部分 `#![no_std]` 应用（如嵌入式）在开发与发布时需要不同的 panic 行为，使用 panic crate（只包含 `#[panic_handler]` 的 crate）会很有帮助。这样应用只需链接不同的 panic crate 即可轻松切换 panic 行为。

　　下面示例：应用根据 dev profile（`cargo build`）或 release profile（`cargo build --release`）采用不同 panic 行为。

　　`panic-semihosting` crate——用 semihosting 把 panic 消息记录到宿主 stderr：

```rust,ignore
#![no_std]

use core::fmt::{Write, self};
use core::panic::PanicInfo;

struct HStderr {
    // ..
#     _0: (),
}
#
# impl HStderr {
#     fn new() -> HStderr { HStderr { _0: () } }
# }
#
# impl fmt::Write for HStderr {
#     fn write_str(&mut self, _: &str) -> fmt::Result { Ok(()) }
# }

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    let mut host_stderr = HStderr::new();

    // 向宿主 stderr 记录 "panicked at '$reason', src/main.rs:27:4"
    writeln!(host_stderr, "{}", info).ok();

    loop {}
}
```

　　`panic-halt` crate——panic 时挂起线程；消息被丢弃：

```rust,ignore
#![no_std]

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
```

　　`app` crate：

```rust,ignore
#![no_std]

// dev profile
#[cfg(debug_assertions)]
extern crate panic_semihosting;

// release profile
#[cfg(not(debug_assertions))]
extern crate panic_halt;

fn main() {
    // ..
}
```
