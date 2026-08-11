+++
title = "04-半主机（Semihosting）"
date = 2026-08-01T10:38:00+08:00
weight = 42
type = "docs"
description = "半主机（Semihosting）（Semihosting）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 半主机（Semihosting） {#semihosting}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/semihosting.html](https://doc.rust-lang.org/stable/embedded-book/start/semihosting.html)


半主机（Semihosting）是一种让嵌入式设备在主机上做 I/O 的机制，主要用于把消息记录到主机控制台。半主机需要调试会话，除此之外几乎什么都不需要（无需额外连线！），因此用起来非常方便。缺点是非常慢：每次写操作可能需要数毫秒，具体取决于你使用的硬件调试器（例如 ST-Link）。

[`cortex-m-semihosting`] crate 提供了在 Cortex-M 设备上做半主机操作的 API。下面的程序是半主机版的 “Hello, world!”：

[`cortex-m-semihosting`]: https://crates.io/crates/cortex-m-semihosting

```rust,ignore
#![no_main]
#![no_std]

use panic_halt as _;

use cortex_m_rt::entry;
use cortex_m_semihosting::hprintln;

#[entry]
fn main() -> ! {
    hprintln!("Hello, world!").unwrap();

    loop {}
}
```

若你在硬件上运行该程序，会在 OpenOCD 日志中看到 “Hello, world!” 消息。

``` text
$ openocd
(..)
Hello, world!
(..)
```

你需要先从 GDB 在 OpenOCD 中启用半主机：
``` console
(gdb) monitor arm semihosting enable
semihosting is enabled
```

QEMU 理解半主机操作，因此上面的程序也可以在 `qemu-system-arm` 上运行，而无需启动调试会话。注意你需要向 QEMU 传递 `-semihosting-config` 标志以启用半主机支持；这些标志已包含在模板的 `.cargo/config.toml` 文件中。

``` text
$ # 该程序会阻塞终端
$ cargo run
     Running `qemu-system-arm (..)
Hello, world!
```

还有一个 `exit` 半主机操作，可用于终止 QEMU 进程。重要：不要在硬件上使用 `debug::exit`；该函数可能破坏你的 OpenOCD 会话，在重启之前你将无法再调试其它程序。

```rust,ignore
#![no_main]
#![no_std]

use panic_halt as _;

use cortex_m_rt::entry;
use cortex_m_semihosting::debug;

#[entry]
fn main() -> ! {
    let roses = "blue";

    if roses == "red" {
        debug::exit(debug::EXIT_SUCCESS);
    } else {
        debug::exit(debug::EXIT_FAILURE);
    }

    loop {}
}
```

``` text
$ cargo run
     Running `qemu-system-arm (..)

$ echo $?
1
```

最后一个提示：你可以把 panic 行为设为 `exit(EXIT_FAILURE)`。这将让你能编写可在 QEMU 上运行的 `no_std` run-pass 测试。

为方便起见，`panic-semihosting` crate 有一个 “exit” 特性，启用后会在把 panic 消息记录到主机 stderr 之后调用 `exit(EXIT_FAILURE)`。

```rust,ignore
#![no_main]
#![no_std]

use panic_semihosting as _; // features = ["exit"]

use cortex_m_rt::entry;
use cortex_m_semihosting::debug;

#[entry]
fn main() -> ! {
    let roses = "blue";

    assert_eq!(roses, "red");

    loop {}
}
```

``` text
$ cargo run
     Running `qemu-system-arm (..)
panicked at 'assertion failed: `(left == right)`
  left: `"blue"`,
 right: `"red"`', examples/hello.rs:15:5

$ echo $?
1
```

**注意**：要在 `panic-semihosting` 上启用该特性，请编辑你的 `Cargo.toml` 依赖节中指定 `panic-semihosting` 的地方：

``` toml
panic-semihosting = { version = "VERSION", features = ["exit"] }
```

其中 `VERSION` 是所需版本。关于依赖特性的更多信息，请查看 Cargo book 的 [`specifying dependencies`] 一节。

[`specifying dependencies`]:
https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
