+++
title = "02-硬件"
date = 2026-08-01T10:38:00+08:00
weight = 40
type = "docs"
description = "硬件（Hardware）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 硬件 {#hardware}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/hardware.html](https://doc.rust-lang.org/stable/embedded-book/start/hardware.html)


到现在你应该对工具链与开发流程有一定熟悉了。本节我们将切换到真实硬件；过程大体相同。让我们开始。

## 了解你的硬件 {#know-your-hardware}

开始之前，你需要识别目标设备的一些特性，因为这些将用于配置项目：

- ARM 内核。例如 Cortex-M3。

- ARM 内核是否包含 FPU？Cortex-M4**F** 与 Cortex-M7**F** 内核有。

- 目标设备有多少 Flash 存储器与 RAM？例如 256 KiB Flash 与 32 KiB RAM。

- Flash 存储器与 RAM 在地址空间中映射到何处？例如 RAM 通常位于地址 `0x2000_0000`。

你可以在设备的数据手册或参考手册中找到这些信息。

本节我们将使用参考硬件 STM32F3DISCOVERY。该板包含 STM32F303VCT6 微控制器。该微控制器具有：

- 包含单精度 FPU 的 Cortex-M4F 内核

- 位于地址 0x0800_0000 的 256 KiB Flash。

- 位于地址 0x2000_0000 的 40 KiB RAM。（还有另一个 RAM 区域，但为简单起见我们忽略它）。

## 配置 {#configuring}

我们将从全新的模板实例开始。关于如何在不用 `cargo-generate` 的情况下完成，请参阅[上一节关于 QEMU]。

[上一节关于 QEMU]: 01-qemu/

``` text
$ cargo generate --git https://github.com/rust-embedded/cortex-m-quickstart
 Project Name: app
 Creating project called `app`...
 Done! New project created /tmp/app

$ cd app
```

第一步是在 `.cargo/config.toml` 中设置默认编译目标。

``` console
tail -n5 .cargo/config.toml
```

``` toml
# 从下列编译目标中任选其一
# target = "thumbv6m-none-eabi"    # Cortex-M0 与 Cortex-M0+
# target = "thumbv7m-none-eabi"    # Cortex-M3
# target = "thumbv7em-none-eabi"   # Cortex-M4 与 Cortex-M7（无 FPU）
target = "thumbv7em-none-eabihf" # Cortex-M4F 与 Cortex-M7F（有 FPU）
```

我们将使用覆盖 Cortex-M4F 内核的 `thumbv7em-none-eabihf`。
> **注意**：如你从上一章记得的，我们必须安装所有目标，而这是一个新目标。因此别忘了为该目标运行安装过程 `rustup target add thumbv7em-none-eabihf`。

第二步是把内存区域信息写入 `memory.x` 文件。

``` text
$ cat memory.x
/* STM32F303VCT6 的链接器脚本 */
MEMORY
{
  /* 注意 1 K = 1 KiBi = 1024 字节 */
  FLASH : ORIGIN = 0x08000000, LENGTH = 256K
  RAM : ORIGIN = 0x20000000, LENGTH = 40K
}
```
> **注意**：若你在对某个构建目标完成首次构建之后又出于某种原因修改了 `memory.x`，请在 `cargo build` 之前执行 `cargo clean`，因为 `cargo build` 可能不会跟踪 `memory.x` 的更新。

我们再次从 hello 示例开始，但首先要做一小处改动。

在 `examples/hello.rs` 中，确保 `debug::exit()` 调用已被注释掉或删除。它仅用于在 QEMU 中运行。

```rust,ignore
#[entry]
fn main() -> ! {
    hprintln!("Hello, world!").unwrap();

    // 退出 QEMU
    // 注意：不要在硬件上运行此调用；它可能破坏 OpenOCD 状态
    // debug::exit(debug::EXIT_SUCCESS);

    loop {}
}
```

你现在可以用 `cargo build` 交叉编译程序，并像之前一样用 `cargo-binutils` 检查二进制。`cortex-m-rt` crate 处理让芯片运行所需的全部“魔法”——幸好，几乎所有 Cortex-M CPU 都以相同方式启动。

``` console
cargo build --example hello
```

## 调试 {#debugging}

调试看起来会有些不同。事实上，前几步可能因目标设备而异。本节我们将展示在 STM32F3DISCOVERY 上调试程序所需的步骤。这意在作为参考；关于调试的设备特定信息，请查阅 [Debugonomicon](https://github.com/rust-embedded/debugonomicon)。

和之前一样，我们将做远程调试，客户端是 GDB 进程。不过这次服务器将是 OpenOCD。

像在[验证安装]一节中那样，将 Discovery 开发板连接到笔记本/PC，并检查 ST-LINK 排针是否已焊好。

[验证安装]: ../intro/install/04-verify-installation/

在一个终端运行 `openocd` 以连接到 Discovery 板上的 ST-LINK。
从模板根目录运行该命令；`openocd` 会读取 `openocd.cfg` 文件，其中指明使用哪个 interface 文件与 target 文件。

``` console
cat openocd.cfg
```

``` text
# STM32F3DISCOVERY 开发板的示例 OpenOCD 配置

# 根据你拿到的硬件版本，从下列接口中任选其一。
# 任意时刻只应有一个接口处于取消注释状态。

# Revision C（较新版本）
source [find interface/stlink.cfg]

# Revision A 与 B（较旧版本）
# source [find interface/stlink-v2.cfg]

source [find target/stm32f3x.cfg]
```

> **注意** 若你在[验证安装]一节中发现自己有较旧版本的 Discovery 开发板，此时应修改 `openocd.cfg` 文件以使用 `interface/stlink-v2.cfg`。

``` text
$ openocd
Open On-Chip Debugger 0.10.0
Licensed under GNU GPL v2
For bug reports, read
        http://openocd.org/doc/doxygen/bugs.html
Info : auto-selecting first available session transport "hla_swd". To override use 'transport select <transport>'.
adapter speed: 1000 kHz
adapter_nsrst_delay: 100
Info : The selected transport took over low-level target control. The results might differ compared to plain JTAG/SWD
none separate
Info : Unable to match requested speed 1000 kHz, using 950 kHz
Info : Unable to match requested speed 1000 kHz, using 950 kHz
Info : clock speed 950 kHz
Info : STLINK v2 JTAG v27 API v2 SWIM v15 VID 0x0483 PID 0x374B
Info : using stlink api v2
Info : Target voltage: 2.913879
Info : stm32f3x.cpu: hardware has 6 breakpoints, 4 watchpoints
```

在另一个终端也从模板根目录运行 GDB。

``` text
gdb-multiarch -q target/thumbv7em-none-eabihf/debug/examples/hello
```

**注意**：和之前一样，根据你在安装章节安装的版本，你可能需要 `gdb-multiarch` 之外的其它 gdb，也可能是 `arm-none-eabi-gdb` 或就是 `gdb`。

接下来将 GDB 连接到在端口 3333 上等待 TCP 连接的 OpenOCD。

``` console
(gdb) target remote :3333
Remote debugging using :3333
0x00000000 in ?? ()
```

现在用 `load` 命令把程序*烧录*（加载）到微控制器上。

``` console
(gdb) load
Loading section .vector_table, size 0x400 lma 0x8000000
Loading section .text, size 0x1518 lma 0x8000400
Loading section .rodata, size 0x414 lma 0x8001918
Start address 0x08000400, load size 7468
Transfer rate: 13 KB/sec, 2489 bytes/write.
```

程序现已加载。该程序使用半主机，因此在做任何半主机调用之前，我们必须告诉 OpenOCD 启用半主机。你可以用 `monitor` 命令向 OpenOCD 发送命令。

``` console
(gdb) monitor arm semihosting enable
semihosting is enabled
```

> 你可以通过调用 `monitor help` 命令查看所有 OpenOCD 命令。

和之前一样，我们可以用断点与 `continue` 命令直接跳到 `main`。

``` console
(gdb) break main
Breakpoint 1 at 0x8000490: file examples/hello.rs, line 11.
Note: automatically using hardware breakpoints for read-only addresses.

(gdb) continue
Continuing.

Breakpoint 1, hello::__cortex_m_rt_main_trampoline () at examples/hello.rs:11
11      #[entry]
```

> **注意** 若你在发出上面的 `continue` 命令后，GDB 阻塞了终端而没有命中断点，你可能需要仔细检查 `memory.x` 文件中的内存区域信息是否已为你的设备正确设置（起始地址*与*长度）。

用 `step` 步入 main 函数。

``` console
(gdb) step
halted: PC: 0x08000496
hello::__cortex_m_rt_main () at examples/hello.rs:13
13          hprintln!("Hello, world!").unwrap();
```

用 `next` 推进程序后，你应在 OpenOCD 控制台看到 “Hello, world!”（以及其它内容）。

``` console
$ openocd
(..)
Info : halted: PC: 0x08000502
Hello, world!
Info : halted: PC: 0x080004ac
Info : halted: PC: 0x080004ae
Info : halted: PC: 0x080004b0
Info : halted: PC: 0x080004b4
Info : halted: PC: 0x080004b8
Info : halted: PC: 0x080004bc
```
该消息只显示一次，因为程序即将进入第 19 行定义的无限循环：`loop {}`

现在可以用 `quit` 命令退出 GDB。

``` console
(gdb) quit
A debugging session is active.

        Inferior 1 [Remote target] will be detached.

Quit anyway? (y or n)
```

现在调试需要更多步骤，因此我们把这些步骤打包进名为 `openocd.gdb` 的单个 GDB 脚本。该文件在 `cargo generate` 步骤中已创建，通常无需修改即可工作。让我们看一眼：

``` console
cat openocd.gdb
```

``` text
target extended-remote :3333

# 打印去混淆（demangled）符号
set print asm-demangle on

# 检测未处理的异常、HardFault 与 panic
break DefaultHandler
break HardFault
break rust_begin_unwind

monitor arm semihosting enable

load

# 启动进程但立即暂停处理器
stepi
```

现在运行 `<gdb> -x openocd.gdb target/thumbv7em-none-eabihf/debug/examples/hello` 会立即将 GDB 连接到 OpenOCD、启用半主机、加载程序并启动进程。

或者，你可以把 `<gdb> -x openocd.gdb` 变成自定义 runner，使 `cargo run` 构建程序*并*启动 GDB 会话。该 runner 已包含在 `.cargo/config.toml` 中，但被注释掉了。

``` console
head -n10 .cargo/config.toml
```

``` toml
[target.thumbv7m-none-eabi]
# 取消此行注释，使 `cargo run` 在 QEMU 上执行程序
# runner = "qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic -semihosting-config enable=on,target=native -kernel"

[target.'cfg(all(target_arch = "arm", target_os = "none"))']
# 从下列三个选项中取消注释其一，使 `cargo run` 启动 GDB 会话
# 选择哪个取决于你的系统
runner = "arm-none-eabi-gdb -x openocd.gdb"
# runner = "gdb-multiarch -x openocd.gdb"
# runner = "gdb -x openocd.gdb"
```

``` text
$ cargo run --example hello
(..)
Loading section .vector_table, size 0x400 lma 0x8000000
Loading section .text, size 0x1e70 lma 0x8000400
Loading section .rodata, size 0x61c lma 0x8002270
Start address 0x800144e, load size 10380
Transfer rate: 17 KB/sec, 3460 bytes/write.
(gdb)
```
