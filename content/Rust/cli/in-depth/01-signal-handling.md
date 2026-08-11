+++
title = "01-信号处理"
date = 2026-08-01T10:33:00+08:00
weight = 21
type = "docs"
description = "在 Rust CLI 中处理信号"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Command Line Applications in Rust](https://rust-cli.github.io/book/)

# 信号处理 {#signal-handling}


> 原文链接: [https://rust-cli.github.io/book/in-depth/signals.html](https://rust-cli.github.io/book/in-depth/signals.html)


像命令行应用这样的进程，需要响应操作系统发来的信号。最常见的例子大概是 <kbd>Ctrl</kbd>+<kbd>C</kbd>，这个信号通常表示让进程终止。在 Rust 程序中处理信号时，你需要考虑如何接收这些信号，以及如何对它们做出反应。

<aside>

**注意：**
如果你的应用不需要优雅关闭，默认处理就足够了（即立即退出，由操作系统清理打开的文件句柄等资源）。在这种情况下：不必按本章所说的去做！

不过，对于需要自行清理的应用，本章就非常相关了！例如，如果你的应用需要正确地关闭网络连接（向对端进程说「再见」）、删除临时文件，或重置系统设置，请继续往下读。

</aside>

## 操作系统之间的差异

在 Unix 系统（如 Linux、macOS 和 FreeBSD）上，进程可以接收[信号][signals]。它可以按默认（操作系统提供的）方式响应，捕获信号并以程序自定义的方式处理，或者完全忽略该信号。

[signals]: https://manpages.ubuntu.com/manpages/bionic/en/man7/signal.7.html

Windows 没有信号。你可以使用 [Console Handlers] 定义在事件发生时执行的回调。此外还有 [结构化异常处理][structured exception handling]，用于处理各种系统异常，例如除以零、无效访问异常、栈溢出等。

[Console Handlers]: https://docs.microsoft.com/en-us/windows/console/console-control-handlers
[structured exception handling]: https://docs.microsoft.com/en-us/windows/desktop/debug/structured-exception-handling

## 首先：处理 Ctrl+C

[ctrlc] crate 正如其名：它允许你以跨平台的方式响应用户按下 <kbd>Ctrl</kbd>+<kbd>C</kbd>。使用该 crate 的主要方式如下：

[ctrlc]: https://crates.io/crates/ctrlc

```rust
use std::{thread, time::Duration};

fn main() {
    ctrlc::set_handler(move || {
        println!("received Ctrl+C!");
    })
    .expect("Error setting Ctrl-C handler");

    // 下面的代码执行实际工作，可被 Ctrl-C 打断。
    // 举例：等待几秒钟。
    thread::sleep(Duration::from_secs(2));
}
```

这当然没什么用：它只是打印一条消息，并不会真正停止程序。

在真实程序中，更好的做法是在信号处理函数里设置一个变量，然后在程序各处检查它。例如，你可以在信号处理函数中设置一个 `Arc<AtomicBool>`（可在线程间共享的布尔值），并在热循环中，或在等待某个线程时，定期检查其值，当它变为 `true` 时跳出。

## 处理其它类型的信号

[ctrlc] crate 只处理 <kbd>Ctrl</kbd>+<kbd>C</kbd>，也就是 Unix 系统上称为 `SIGINT`（「中断」信号）的情况。若要响应更多 Unix 信号，应看看 [signal-hook]。其设计在[这篇博文][signal-hook-post]中有说明，目前它是社区支持最广的相关库。

下面是一个简单例子：

```rust
use signal_hook::{consts::SIGINT, iterator::Signals};
use std::{error::Error, thread, time::Duration};

fn main() -> Result<(), Box<dyn Error>> {
    let mut signals = Signals::new([SIGINT])?;

    thread::spawn(move || {
        for sig in signals.forever() {
            println!("Received signal {:?}", sig);
        }
    });

    // 下面的代码执行实际工作，可被 Ctrl-C 打断。
    // 举例：等待几秒钟。
    thread::sleep(Duration::from_secs(2));

    Ok(())
}
```

[signal-hook-post]: https://vorner.github.io/2018/06/28/signal-hook.html

## 使用 channel

除了设置变量并让程序其它部分去检查之外，你还可以使用 channel：创建一个 channel，每当收到信号时，由信号处理函数向其中发送一个值。在应用代码中，你把这个 channel 和其它 channel 一起用作线程之间的同步点。用 [crossbeam-channel] 大致可以这样写：

[crossbeam-channel]: https://crates.io/crates/crossbeam-channel

```rust
use anyhow::Result;
use crossbeam_channel::{Receiver, bounded, select, tick};
use std::time::Duration;

fn ctrl_channel() -> Result<Receiver<()>, ctrlc::Error> {
    let (sender, receiver) = bounded(100);
    ctrlc::set_handler(move || {
        let _ = sender.send(());
    })?;

    Ok(receiver)
}

fn main() -> Result<()> {
    let ctrl_c_events = ctrl_channel()?;
    let ticks = tick(Duration::from_secs(1));

    loop {
        select! {
            recv(ticks) -> _ => {
                println!("working!");
            }
            recv(ctrl_c_events) -> _ => {
                println!();
                println!("Goodbye!");
                break;
            }
        }
    }

    Ok(())
}
```

## 使用 future 与 stream

如果你在使用 [tokio]，那么很可能已经在用异步模式和事件驱动设计来编写应用。与其直接使用 crossbeam 的 channel，你可以启用 signal-hook 的 `tokio-support` 特性。这样就可以在 signal-hook 的 `Signals` 类型上调用 [`.into_async()`]，得到一个实现了 `futures::Stream` 的新类型。

[signal-hook]: https://crates.io/crates/signal-hook
[tokio]: https://tokio.rs/
[`.into_async()`]: https://docs.rs/signal-hook/0.1.6/signal_hook/iterator/struct.Signals.html#method.into_async

## 正在处理第一次 Ctrl+C 时又收到一次 Ctrl+C 该怎么办

大多数用户会按下 <kbd>Ctrl</kbd>+<kbd>C</kbd>，然后给你的程序几秒钟时间退出，或者告诉他们发生了什么。如果没有动静，他们会再按一次 <kbd>Ctrl</kbd>+<kbd>C</kbd>。典型行为是让应用立即退出。
