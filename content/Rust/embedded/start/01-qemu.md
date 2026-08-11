+++
title = "01-QEMU"
date = 2026-08-01T10:38:00+08:00
weight = 39
type = "docs"
description = "QEMU"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# QEMU {#qemu}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/qemu.html](https://doc.rust-lang.org/stable/embedded-book/start/qemu.html)


我们将开始为 [LM3S6965]（一颗 Cortex-M3 微控制器）编写程序。
我们选择它作为初始目标，是因为它[可用 QEMU 模拟](https://wiki.qemu.org/Documentation/Platforms/ARM#Supported_in_qemu-system-arm)，
因此本节无需折腾硬件，我们可以专注于工具链与开发流程。

[LM3S6965]: http://www.ti.com/product/LM3S6965

**重要**
本教程中我们将用 “app” 作为项目名。
每当你看到 “app” 这个词，都应替换为你为自己项目选择的名称。或者，你也可以把项目命名为 “app”，从而避免替换。

## 创建非标准 Rust 程序 {#creating-a-non-standard-rust-program}

我们将使用 [`cortex-m-quickstart`] 项目模板从中生成新项目。生成的项目会包含一个极简应用：适合作为新嵌入式 Rust 应用的起点。此外，项目还会包含一个 `examples` 目录，内有若干独立应用，展示嵌入式 Rust 的一些关键功能。

[`cortex-m-quickstart`]: https://github.com/rust-embedded/cortex-m-quickstart

### 使用 `cargo-generate` {#using-cargo-generate}
先安装 cargo-generate
```console
cargo install cargo-generate
```
然后生成新项目
```console
cargo generate --git https://github.com/knurling-rs/app-template
```

```text
 Project Name: app
 Creating project called `app`...
 Done! New project created /tmp/app
```

```console
cd app
```

### 使用 `git` {#using-git}

克隆仓库

```console
git clone https://github.com/rust-embedded/cortex-m-quickstart app
cd app
```

然后填写 `Cargo.toml` 文件中的占位符

```toml
[package]
authors = ["{{authors}}"] # "{{authors}}" -> "John Smith"
edition = "2018"
name = "{{project-name}}" # "{{project-name}}" -> "app"
version = "0.1.0"

# ..

[[bin]]
name = "{{project-name}}" # "{{project-name}}" -> "app"
test = false
bench = false
```

### 两者都不用 {#using-neither}

获取 `cortex-m-quickstart` 模板的最新快照并解压。

```console
curl -LO https://github.com/rust-embedded/cortex-m-quickstart/archive/master.zip
unzip master.zip
mv cortex-m-quickstart-master app
cd app
```

或者你可以浏览到 [`cortex-m-quickstart`]，点击绿色的 “Clone or download” 按钮，再点击 “Download ZIP”。

然后像 “使用 `git`” 版本的第二部分那样填写 `Cargo.toml` 中的占位符。

## 程序概览 {#program-overview}

为方便起见，以下是 `src/main.rs` 中最重要的部分：

```rust,ignore
#![no_std]
#![no_main]

use panic_halt as _;

use cortex_m_rt::entry;

#[entry]
fn main() -> ! {
    loop {
        // 你的代码写在这里
    }
}
```

这个程序与标准 Rust 程序有些不同，让我们仔细看看。

`#![no_std]` 表示该程序*不会*链接到标准 crate `std`。相反，它会链接到其子集：`core` crate。

`#![no_main]` 表示该程序不会使用大多数 Rust 程序使用的标准 `main` 接口。选择 `no_main` 的主要原因是：在 `no_std` 语境下使用 `main` 接口需要 nightly。

`use panic_halt as _;`。该 crate 提供定义程序 panic 行为的 `panic_handler`。我们会在本书的 [Panic 处理](05-panicking/) 一章中更详细地介绍。

[`#[entry]`][entry] 是 [`cortex-m-rt`] crate 提供的属性，用于标记程序的入口点。由于我们不使用标准 `main` 接口，需要另一种方式标明程序入口，那就是 `#[entry]`。

[entry]: https://docs.rs/cortex-m-rt-macros/latest/cortex_m_rt_macros/attr.entry.html
[`cortex-m-rt`]: https://crates.io/crates/cortex-m-rt

`fn main() -> !`。我们的程序将是目标硬件上运行的*唯一*进程，因此我们不希望它结束！我们使用[发散函数（divergent function）](https://doc.rust-lang.org/rust-by-example/fn/diverging.html)（函数签名中的 `-> !`）在编译期确保这一点。

## 交叉编译 {#cross-compiling}

首先我们需要目标微控制器（这里是 LM3S6965）的内存布局，否则构建会在链接镜像时失败。在项目根目录创建名为 `memory.x` 的文件，并粘贴以下内容：

```text
MEMORY
{
  /* 注意 1 K = 1 KiBi = 1024 字节 */
  /* TODO 调整这些内存区域以匹配你的设备内存布局 */
  /* 这些值对应 LM3S6965，QEMU 能模拟的少数设备之一 */
  FLASH : ORIGIN = 0x00000000, LENGTH = 256K
  RAM : ORIGIN = 0x20000000, LENGTH = 64K
}

/* 调用栈将在此分配。 */
/* 栈为 full descending 类型。 */
/* 你可能想用此变量把调用栈与静态变量放在不同内存区域。下面是默认值 */
/* _stack_start = ORIGIN(RAM) + LENGTH(RAM); */

/* 可用此符号自定义 .text 段的位置 */
/* 若省略，.text 段会紧接在 .vector_table 段之后 */
/* 仅在向量表之后还存放某些配置的微控制器上需要 */
/* _stext = ORIGIN(FLASH) + 0x400; */

/* 将未初始化变量放入自定义 RAM 位置的示例。 */
/* 这假设你已在上方定义了 RAM2 区域，并在 Rust
   源码中给要放在那里的数据加了属性 `#[link_section = ".ram2bss"]`。 */
/* 注意：该段不会被运行时零初始化！ */
/* SECTIONS {
     .ram2bss (NOLOAD) : ALIGN(4) {
       *(.ram2bss);
       . = ALIGN(4);
     } > RAM2
   } INSERT AFTER .bss;
*/
```

下一步是为 Cortex-M3 架构*交叉*编译程序。
若你知道编译目标（`$TRIPLE`）应是什么，只需运行 `cargo build --target $TRIPLE`。幸运的是，模板中的 `.cargo/config.toml` 已给出答案：

```console
tail -n6 .cargo/config.toml
```

```toml
[build]
# 从下列编译目标中任选其一
# target = "thumbv6m-none-eabi"    # Cortex-M0 与 Cortex-M0+
target = "thumbv7m-none-eabi"    # Cortex-M3
# target = "thumbv7em-none-eabi"   # Cortex-M4 与 Cortex-M7（无 FPU）
# target = "thumbv7em-none-eabihf" # Cortex-M4F 与 Cortex-M7F（有 FPU）
```

要为 Cortex-M3 架构交叉编译，我们必须使用 `thumbv7m-none-eabi`。安装 Rust 工具链时不会自动安装该目标；若尚未添加，现在是很好的时机：

``` console
rustup target add thumbv7m-none-eabi
```

由于 `thumbv7m-none-eabi` 编译目标已在 `.cargo/config.toml` 中设为默认，下面两条命令效果相同：

```console
cargo build --target thumbv7m-none-eabi
cargo build
```

## 检查 {#inspecting}

现在我们在 `target/thumbv7m-none-eabi/debug/app` 有了一个非原生 ELF 二进制。可用 `cargo-binutils` 检查它。

用 `cargo-readobj` 可以打印 ELF 头，以确认这是 ARM 二进制。

``` console
cargo readobj --bin app -- --file-headers
```

注意：
* `--bin app` 是检查 `target/$TRIPLE/debug/app` 处二进制的简写
* `--bin app` 也会在必要时（重新）编译该二进制


``` text
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0x0
  Type:                              EXEC (Executable file)
  Machine:                           ARM
  Version:                           0x1
  Entry point address:               0x405
  Start of program headers:          52 (bytes into file)
  Start of section headers:          153204 (bytes into file)
  Flags:                             0x5000200
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         2
  Size of section headers:           40 (bytes)
  Number of section headers:         19
  Section header string table index: 18
```

`cargo-size` 可以打印二进制各链接器段的大小。


```console
cargo size --bin app --release -- -A
```
我们使用 `--release` 来检查优化后的版本

``` text
app  :
section             size        addr
.vector_table       1024         0x0
.text                 92       0x400
.rodata                0       0x45c
.data                  0  0x20000000
.bss                   0  0x20000000
.debug_str          2958         0x0
.debug_loc            19         0x0
.debug_abbrev        567         0x0
.debug_info         4929         0x0
.debug_ranges         40         0x0
.debug_macinfo         1         0x0
.debug_pubnames     2035         0x0
.debug_pubtypes     1892         0x0
.ARM.attributes       46         0x0
.debug_frame         100         0x0
.debug_line          867         0x0
Total              14570
```

> ELF 链接器段速记
>
> - `.text` 包含程序指令
> - `.rodata` 包含字符串等常量值
> - `.data` 包含初始值*不为*零的静态分配变量
> - `.bss` 也包含初始值*为*零的静态分配变量
> - `.vector_table` 是我们用来存放向量（中断）表的*非*标准段
> - `.ARM.attributes` 与 `.debug_*` 段包含元数据，烧录二进制时*不会*加载到目标上。

**重要**：ELF 文件包含调试信息等元数据，因此其*磁盘大小*并不能准确反映程序烧录到设备后所占空间。*务必*用 `cargo-size` 检查二进制的真实大小。

`cargo-objdump` 可用于反汇编二进制。

```console
cargo objdump --bin app --release -- --disassemble --no-show-raw-insn --print-imm-hex
```

> **注意** 若上述命令抱怨 `Unknown command line argument`，请参阅此 bug 报告：https://github.com/rust-embedded/book/issues/269

> **注意** 该输出在你的系统上可能不同。新版本的 rustc、LLVM 与库可能生成不同的汇编。我们截断了部分指令以保持片段简短。

```text
app:  file format ELF32-arm-little

Disassembly of section .text:
main:
     400: bl  #0x256
     404: b #-0x4 <main+0x4>

Reset:
     406: bl  #0x24e
     40a: movw  r0, #0x0
     < .. truncated any more instructions .. >

DefaultHandler_:
     656: b #-0x4 <DefaultHandler_>

UsageFault:
     657: strb  r7, [r4, #0x3]

DefaultPreInit:
     658: bx  lr

__pre_init:
     659: strb  r7, [r0, #0x1]

__nop:
     65a: bx  lr

HardFaultTrampoline:
     65c: mrs r0, msp
     660: b #-0x2 <HardFault_>

HardFault_:
     662: b #-0x4 <HardFault_>

HardFault:
     663: <unknown>
```

## 运行 {#running}

接下来，看看如何在 QEMU 上运行嵌入式程序！这次我们使用实际上会做些事情的 `hello` 示例。默认情况下，该示例使用 `[defmt]` 与 RTT 打印文本。

[defmt]: https://defmt.ferrous-systems.com/

> **注意** `defmt` 是嵌入式 Rust 生态中广泛使用的第三方依赖（即非 core）。

为了在主机上读取并解码 `defmt` 产生的消息，我们需要把 RTT 传输输出切换为半主机（semihosting）。在真实硬件上这需要调试会话，但在使用 QEMU 时可以直接工作。

让我们切换依赖：

```console
cargo remove defmt-rtt
cargo add defmt-semihosting
```

打开 `src/lib.rs`，将 `use defmt_rtt as _;` 替换为 `use defmt_semihosting as _;`

现在可以构建该示例：

```console
cargo build --bin hello
```

输出二进制将位于 `target/thumbv7m-none-eabi/debug/hello`。

要在 QEMU 上运行该二进制，通常以下命令就够了：

```console
qemu-system-arm \
  -cpu cortex-m3 \
  -machine lm3s6965evb \
  -nographic \
  -semihosting-config enable=on,target=native \
  -kernel target/thumbv7m-none-eabi/debug/hello
```

在我们的情况下，由于使用了 `defmt`，主机将无法解码输出。我们需要 Ferrous Systems 的工具 [`qemu-run`]：

[`qemu-run`]: https://github.com/knurling-rs/defmt/tree/main/qemu-run/

```console
git clone git@github.com:knurling-rs/defmt.git
cd defmt/qemu-run/
cargo run -- --machine lm3s6965evb ../qemu-rs/target/thumbv7m-none-eabi/debug/hello
```

```text
Hello, world!
```

该命令在打印文本后应成功退出（退出码 = 0）。在 *nix 上可用以下命令检查：

```console
echo $?
```

```text
0
```

让我们拆解这条 QEMU 命令：

- `qemu-system-arm`。这是 QEMU 模拟器。这类 QEMU 二进制有几个变体；这个做完整的 *ARM* 机器*系统*模拟，因而得名。

- `-cpu cortex-m3`。告诉 QEMU 模拟 Cortex-M3 CPU。指定 CPU 型号可帮助捕获一些错误编译：例如，运行为带硬件 FPU 的 Cortex-M4F 编译的程序，会让 QEMU 在执行时出错。

- `-machine lm3s6965evb`。告诉 QEMU 模拟 LM3S6965EVB——一块包含 LM3S6965 微控制器的评估板。

- `-nographic`。告诉 QEMU 不要启动其 GUI。

- `-semihosting-config (..)`。告诉 QEMU 启用半主机。半主机让被模拟设备除其它功能外，还能使用主机的 stdout、stderr 与 stdin，并在主机上创建文件。

- `-kernel $file`。告诉 QEMU 在被模拟机器上加载并运行哪个二进制。

每次敲那么长的 QEMU 命令太费事了！我们可以设置自定义 runner 来简化流程。`.cargo/config.toml` 中有一段被注释掉、用于调用 QEMU 的 runner；让我们取消注释：

```console
head -n3 .cargo/config.toml
```

```toml
[target.thumbv7m-none-eabi]
# 取消此行注释，使 `cargo run` 在 QEMU 上执行程序
runner = "qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic -semihosting-config enable=on,target=native -kernel"
```

该 runner 仅适用于我们的默认编译目标 `thumbv7m-none-eabi`。现在 `cargo run` 会编译程序并在 QEMU 上运行：

```console
cargo run --example hello --release
```

```text
   Compiling app v0.1.0 (file:///tmp/app)
    Finished release [optimized + debuginfo] target(s) in 0.26s
     Running `qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic -semihosting-config enable=on,target=native -kernel target/thumbv7m-none-eabi/release/examples/hello`
Hello, world!
```

## 调试 {#debugging}

调试对嵌入式开发至关重要。让我们看看如何进行。

调试嵌入式设备涉及*远程*调试，因为我们要调试的程序不会运行在运行调试器程序（GDB 或 LLDB）的机器上。

远程调试涉及客户端与服务器。在 QEMU 设置中，客户端是 GDB（或 LLDB）进程，服务器是同时运行嵌入式程序的 QEMU 进程。

本节我们将使用已编译好的 `hello` 示例。

调试的第一步是以调试模式启动 QEMU：

```console
qemu-system-arm \
  -cpu cortex-m3 \
  -machine lm3s6965evb \
  -nographic \
  -semihosting-config enable=on,target=native \
  -gdb tcp::3333 \
  -S \
  -kernel target/thumbv7m-none-eabi/debug/examples/hello
```

该命令不会向控制台打印任何内容，并会阻塞终端。这次我们多传了两个标志：

- `-gdb tcp::3333`。告诉 QEMU 在 TCP 端口 3333 上等待 GDB 连接。

- `-S`。告诉 QEMU 在启动时冻结机器。没有它，程序会在我们有机会启动调试器之前就到达 main 末尾！

接下来在另一个终端启动 GDB，并告诉它加载该示例的调试符号：

```console
gdb-multiarch -q target/thumbv7m-none-eabi/debug/examples/hello
```

**注意**：根据你在安装章节安装的版本，你可能需要 `gdb-multiarch` 之外的其它 gdb，也可能是 `arm-none-eabi-gdb` 或就是 `gdb`。

然后在 GDB shell 中连接到在 TCP 端口 3333 上等待连接的 QEMU。

```console
target remote :3333
```

```text
Remote debugging using :3333
Reset () at $REGISTRY/cortex-m-rt-0.6.1/src/lib.rs:473
473     pub unsafe extern "C" fn Reset() -> ! {
```


你会看到进程已停住，程序计数器指向名为 `Reset` 的函数。那是复位处理函数：Cortex-M 内核启动时执行的内容。

> 注意：在某些环境下，gdb 可能不显示上面那样的 `Reset () at $REGISTRY/cortex-m-rt-0.6.1/src/lib.rs:473`，而打印类似如下警告：
>
>`core::num::bignum::Big32x40::mul_small () at src/libcore/num/bignum.rs:254`
> `    src/libcore/num/bignum.rs: No such file or directory.`
>
> 这是已知小问题。你可以安全地忽略这些警告，你很可能已经停在 Reset()。


该复位处理函数最终会调用我们的 main 函数。让我们用断点与 `continue` 命令直接跳到那里。要设置断点，先用 `list` 命令看看我们想在代码的哪里停下。

```console
list main
```
这将显示源码，来自文件 examples/hello.rs。

```text
6       use panic_halt as _;
7
8       use cortex_m_rt::entry;
9       use cortex_m_semihosting::{debug, hprintln};
10
11      #[entry]
12      fn main() -> ! {
13          hprintln!("Hello, world!").unwrap();
14
15          // 退出 QEMU
```
我们想在 “Hello, world!” 之前加断点，也就是第 13 行。用 `break` 命令完成：

```console
break 13
```
现在可以指示 gdb 运行到我们的 main 函数，使用 `continue` 命令：

```console
continue
```

```text
Continuing.

Breakpoint 1, hello::__cortex_m_rt_main () at examples\hello.rs:13
13          hprintln!("Hello, world!").unwrap();
```

我们现在接近打印 “Hello, world!” 的代码了。用 `next` 命令向前迈一步。

``` console
next
```

```text
16          debug::exit(debug::EXIT_SUCCESS);
```

此时你应在运行 `qemu-system-arm` 的终端上看到 “Hello, world!”。

```text
$ qemu-system-arm (..)
Hello, world!
```

再次调用 `next` 将终止 QEMU 进程。

```console
next
```

```text
[Inferior 1 (Remote target) exited normally]
```

现在可以退出 GDB 会话。

``` console
quit
```
