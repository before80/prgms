+++
title = "3.7.1 调试"
date = 2026-08-11T11:30:00+08:00
weight = 306
type = "docs"
description = "01-调试 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/debugging.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/debugging.html)

# 3.7.1 调试

_Embed.toml_：

```toml
[default.general]
chip = "nrf52833_xxAA"

[debug.gdb]
enabled = true
```

在 `src/bare-metal/microcontrollers/examples/` 下的一个终端中：

```sh
cargo embed --bin board_support debug
```

在同目录的另一个终端中：

在 gLinux 或 Debian 上：

```sh
gdb-multiarch target/thumbv7em-none-eabihf/debug/board_support --eval-command="target remote :1338"
```

在 MacOS 上：

```sh
arm-none-eabi-gdb target/thumbv7em-none-eabihf/debug/board_support --eval-command="target remote :1338"
```

> 在 GDB 中可尝试运行：
>
> ```gdb
> b src/bin/board_support.rs:29
> b src/bin/board_support.rs:30
> b src/bin/board_support.rs:32
> c
> c
> c
> ```

