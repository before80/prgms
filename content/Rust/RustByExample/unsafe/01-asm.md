+++
title = "01-内联汇编"
date = 2026-08-20T21:20:00+08:00
weight = 193
type = "docs"
description = "内联汇编 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/unsafe/asm.html](https://doc.rust-lang.org/stable/rust-by-example/unsafe/asm.html)

# 内联汇编

Rust 通过 `asm!` 宏提供内联汇编支持。
可用它把手工编写的汇编嵌入到编译器生成的汇编输出中。
通常并不需要这样做，但在无法以其他方式达到所需性能或时序时可能有用。
访问底层硬件原语（例如内核代码）也可能需要此功能。

> **注意**：此处示例使用 x86/x86-64 汇编，但也支持其他架构。

当前支持内联汇编的架构包括：

- x86 与 x86-64
- ARM
- AArch64
- RISC-V

## 基本用法 {#基本用法}

先从最简单的例子开始：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

unsafe {
    asm!("nop");
}
# }
```
这会把一条 NOP（空操作）指令插入到编译器生成的汇编中。
注意：所有 `asm!` 调用都必须位于 `unsafe` 块内，因为它们可能插入任意指令并破坏多种不变量。
要插入的指令以字符串字面量形式写在 `asm!` 宏的第一个参数中。

## 输入与输出 {#输入与输出}

插入一条什么都不做的指令相当无聊。我们来做点真正处理数据的事：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let x: u64;
unsafe {
    asm!("mov {}, 5", out(reg) x);
}
assert_eq!(x, 5);
# }
```
这会把值 `5` 写入 `u64` 变量 `x`。
可以看到，用于指定指令的字符串字面量实际上是模板字符串，
遵循与 Rust [格式化字符串][format-syntax]相同的规则。
但插入到模板中的参数写法可能与你熟悉的略有不同。
首先需要指明变量是内联汇编的输入还是输出。本例中是输出，用 `out` 声明。
还需要指明汇编期望该变量位于何种寄存器中。本例用 `reg` 表示任意通用寄存器。
编译器会选择合适的寄存器填入模板，并在内联汇编执行结束后从该寄存器读回变量。

[format-syntax]: https://doc.rust-lang.org/std/fmt/#syntax

再看一个同时使用输入的例子：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let i: u64 = 3;
let o: u64;
unsafe {
    asm!(
        "mov {0}, {1}",
        "add {0}, 5",
        out(reg) o,
        in(reg) i,
    );
}
assert_eq!(o, 8);
# }
```
这会把输入变量 `i` 加上 `5`，并把结果写入变量 `o`。
这段汇编的具体做法是：先把 `i` 的值复制到输出，再对其加 `5`。

该例子说明几点：

第一，`asm!` 允许多个模板字符串参数；每个都被视为单独一行汇编，
相当于用换行符拼接。这样便于格式化汇编代码。

第二，输入用 `in` 而非 `out` 声明。

第三，可以像任何格式化字符串一样指定参数编号或名称。
对内联汇编模板尤其有用，因为参数常被多次使用。
对于更复杂的内联汇编，一般建议使用该功能，以提高可读性，
并允许在不改变参数顺序的情况下重排指令。

可以进一步改进上例，去掉 `mov` 指令：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut x: u64 = 3;
unsafe {
    asm!("add {0}, 5", inout(reg) x);
}
assert_eq!(x, 8);
# }
```
可以看到，`inout` 用于指定既是输入又是输出的参数。
这与分别指定输入和输出不同：它保证两者分配到同一寄存器。

也可以为 `inout` 操作数的输入与输出部分指定不同变量：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let x: u64 = 3;
let y: u64;
unsafe {
    asm!("add {0}, 5", inout(reg) x => y);
}
assert_eq!(y, 8);
# }
```
## 延迟输出操作数 {#延迟输出操作数}

Rust 编译器在分配操作数时偏保守：假定 `out` 可在任意时刻被写入，
因此不能与任何其他参数共享位置。
但为保证最佳性能，应尽量少用寄存器，以免在内联汇编块前后保存/重载。
为此 Rust 提供 `lateout` 说明符，可用于仅在所有输入都被消费之后才写入的任何输出。
还有该说明符的 `inlateout` 变体。

下面的例子在 `release` 模式或其他优化情形下**不能**使用 `inlateout`：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut a: u64 = 4;
let b: u64 = 4;
let c: u64 = 4;
unsafe {
    asm!(
        "add {0}, {1}",
        "add {0}, {2}",
        inout(reg) a,
        in(reg) b,
        in(reg) c,
    );
}
assert_eq!(a, 12);
# }
```
在未优化情形（例如 `Debug` 模式）下，把上例中的 `inout(reg) a` 换成 `inlateout(reg) a`
仍可能得到预期结果。但在 `release` 或其他优化情形下，使用 `inlateout(reg) a`
可能导致最终 `a = 16`，从而使断言失败。

因为在优化情形下，编译器知道 `b` 与 `c` 值相同，可自由为它们分配同一寄存器。
进而，使用 `inlateout` 时，`a` 与 `c` 也可能分配到同一寄存器，
于是第一条 `add` 会覆盖从变量 `c` 的初始加载。
相比之下，使用 `inout(reg) a` 可确保为 `a` 分配单独寄存器。

不过，下面的例子可以使用 `inlateout`，因为输出仅在所有输入寄存器都读完之后才被修改：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut a: u64 = 4;
let b: u64 = 4;
unsafe {
    asm!("add {0}, {1}", inlateout(reg) a, in(reg) b);
}
assert_eq!(a, 8);
# }
```
可以看到，即使 `a` 与 `b` 被分配到同一寄存器，这段汇编仍能正确工作。

## 显式寄存器操作数 {#显式寄存器操作数}

有些指令要求操作数位于特定寄存器。
因此 Rust 内联汇编提供了更具体的约束说明符。
虽然 `reg` 在多数架构上通用，但显式寄存器高度依赖架构。
例如在 x86 上，可用名称引用通用寄存器 `eax`、`ebx`、`ecx`、`edx`、`ebp`、`esi`、`edi` 等。

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let cmd = 0xd1;
unsafe {
    asm!("out 0x64, eax", in("eax") cmd);
}
# }
```
本例调用 `out` 指令，把变量 `cmd` 的内容输出到端口 `0x64`。
由于 `out` 指令只接受 `eax`（及其子寄存器）作为操作数，必须使用 `eax` 约束说明符。

> **注意**：与其他操作数类型不同，显式寄存器操作数不能用于模板字符串：不能使用 `{}`，而应直接写寄存器名。此外，它们必须出现在操作数列表末尾，排在所有其他操作数类型之后。

再看使用 x86 `mul` 指令的例子：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

fn mul(a: u64, b: u64) -> u128 {
    let lo: u64;
    let hi: u64;

    unsafe {
        asm!(
            // x86 的 mul 指令以 rax 为隐式输入，
            // 并把 128 位乘法结果写入 rax:rdx。
            "mul {}",
            in(reg) a,
            inlateout("rax") b => lo,
            lateout("rdx") hi
        );
    }

    ((hi as u128) << 64) + lo as u128
}
# }
```
这里用 `mul` 把两个 64 位输入相乘，得到 128 位结果。
唯一的显式操作数是一个寄存器，由变量 `a` 填充。
第二个操作数是隐式的，必须是 `rax`，由变量 `b` 填充。
结果的低 64 位存在 `rax`，填入变量 `lo`；
高 64 位存在 `rdx`，填入变量 `hi`。

## 被破坏的寄存器（clobbered registers） {#被破坏的寄存器clobbered-registers}

很多情况下，内联汇编会修改并不需要作为输出的状态。
通常是因为汇编中要用到临时寄存器，或指令会修改我们无需继续检查的状态。
这类状态一般称为被“破坏”（clobbered）。
需要告知编译器，因为它可能需要在内联汇编块前后保存并恢复这些状态。

```rust
use std::arch::asm;

# #[cfg(target_arch = "x86_64")]
fn main() {
    // 三个条目，每个四字节
    let mut name_buf = [0_u8; 12];
    // 字符串以 ASCII 依次存在 ebx、edx、ecx 中
    // 由于 ebx 被保留，汇编需要保持其值。
    // 因此在主汇编前后对其 push/pop。
    // 64 位处理器的 64 位模式不允许 push/pop 32 位寄存器（如 ebx），
    // 因此必须改用扩展的 rbx 寄存器。

    unsafe {
        asm!(
            "push rbx",
            "cpuid",
            "mov [rdi], ebx",
            "mov [rdi + 4], edx",
            "mov [rdi + 8], ecx",
            "pop rbx",
            // 用指向数组的指针存储值，以简化 Rust 代码，
            // 代价是多几条汇编指令。
            // 不过这样更能显式体现汇编如何工作，
            // 相对 `out("ecx") val` 这类显式寄存器输出而言。
            // *指针本身* 只是输入，即便其指向的内存会被写入
            in("rdi") name_buf.as_mut_ptr(),
            // 选择 cpuid 0，同时声明 eax 被破坏
            inout("eax") 0 => _,
            // cpuid 也会破坏这些寄存器
            out("ecx") _,
            out("edx") _,
        );
    }

    let name = core::str::from_utf8(&name_buf).unwrap();
    println!("CPU Manufacturer ID: {}", name);
}

# #[cfg(not(target_arch = "x86_64"))]
# fn main() {}
```
上例用 `cpuid` 指令读取 CPU 厂商 ID。
该指令会把最大支持的 `cpuid` 参数写入 `eax`，并把厂商 ID 以 ASCII 字节按序写入 `ebx`、`edx`、`ecx`。

即便从不读取 `eax`，仍需告诉编译器该寄存器已被修改，以便编译器保存汇编前这些寄存器中的值。
做法是将其声明为输出，但用 `_` 代替变量名，表示丢弃输出值。

这段代码还绕开了 LLVM 中 `ebx` 为保留寄存器的限制。
这意味着 LLVM 假定完全控制该寄存器，且在退出 asm 块前必须恢复到原始状态，
因此除编译器用它满足通用寄存器类（例如 `in(reg)`）外，不能将其用作输入或输出。
这使得在使用保留寄存器时，`reg` 操作数很危险——可能在不知情的情况下破坏输入或输出，因为它们共享同一寄存器。

为绕开这一点，我们用 `rdi` 存放输出数组指针，通过 `push` 保存 `ebx`，在 asm 块内从 `ebx` 读入数组，再用 `pop` 恢复 `ebx`。
`push`/`pop` 使用完整的 64 位 `rbx`，以确保保存整个寄存器。在 32 位目标上则会在 `push`/`pop` 中使用 `ebx`。

也可配合通用寄存器类，在 asm 代码内获得临时寄存器：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

// 用移位与加法把 x 乘以 6
let mut x: u64 = 4;
unsafe {
    asm!(
        "mov {tmp}, {x}",
        "shl {tmp}, 1",
        "shl {x}, 2",
        "add {x}, {tmp}",
        x = inout(reg) x,
        tmp = out(reg) _,
    );
}
assert_eq!(x, 4 * 6);
# }
```
## 符号操作数与 ABI 破坏 {#符号操作数与-abi-破坏}

默认情况下，`asm!` 假定任何未声明为输出的寄存器都会被汇编代码保持原样。
传给 `asm!` 的 [`clobber_abi`] 参数会告诉编译器按给定调用约定 ABI 自动插入必要的破坏操作数：
在该 ABI 中未完全保留的任何寄存器都会被视为已破坏。可提供多个 `clobber_abi` 参数，将插入所有指定 ABI 的全部破坏项。

[`clobber_abi`]: https://doc.rust-lang.org/stable/reference/inline-assembly.html#abi-clobbers

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

extern "C" fn foo(arg: i32) -> i32 {
    println!("arg = {}", arg);
    arg * 2
}

fn call_foo(arg: i32) -> i32 {
    unsafe {
        let result;
        asm!(
            "call {}",
            // 要调用的函数指针
            in(reg) foo,
            // 第 1 个参数在 rdi
            in("rdi") arg,
            // 返回值在 rax
            out("rax") result,
            // 将 "C" 调用约定未保留的所有寄存器标记为已破坏
            clobber_abi("C"),
        );
        result
    }
}
# }
```
## 寄存器模板修饰符 {#寄存器模板修饰符}

有时需要精细控制寄存器名插入模板字符串时的格式。
当某架构的汇编语言对同一寄存器有多个名称时（通常是对寄存器子集的“视图”，例如 64 位寄存器的低 32 位）就需要这一点。

默认情况下，编译器总会选择指代完整寄存器大小的名称（例如 x86-64 上的 `rax`、x86 上的 `eax` 等）。

可用模板字符串操作数上的修饰符覆盖该默认行为，就像格式化字符串一样：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut x: u16 = 0xab;

unsafe {
    asm!("mov {0:h}, {0:l}", inout(reg_abcd) x);
}

assert_eq!(x, 0xabab);
# }
```
本例使用 `reg_abcd` 寄存器类，把寄存器分配限制在 4 个传统 x86 寄存器（`ax`、`bx`、`cx`、`dx`）上，其中前两个字节可独立寻址。

假定寄存器分配器把 `x` 分配到了 `ax`。
`h` 修饰符会发出该寄存器高字节的名称，`l` 修饰符发出低字节名称。
因此汇编会展开为 `mov ah, al`，把值的低字节复制到高字节。

若对操作数使用更小的数据类型（例如 `u16`）却忘记使用模板修饰符，编译器会发出警告并建议正确的修饰符。

## 内存地址操作数 {#内存地址操作数}

有时汇编指令需要通过内存地址/内存位置传递的操作数。
必须手动使用目标架构规定的内存地址语法。
例如在 x86/x86_64 使用 Intel 汇编语法时，应用 `[]` 包裹输入/输出以表示内存操作数：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

fn load_fpu_control_word(control: u16) {
    unsafe {
        asm!("fldcw [{}]", in(reg) &control, options(nostack));
    }
}
# }
```
## 标签 {#标签}

任何对命名标签（局部或其他）的重用，都可能导致汇编器或链接器错误，或其他奇怪行为。重用命名标签的方式包括：

- 显式：在一个 `asm!` 块中多次使用同一标签，或跨多个块多次使用。
- 经内联隐式：编译器可实例化多个 `asm!` 块副本，例如包含它的函数在多处被内联时。
- 经 LTO 隐式：LTO 可能把*其他 crate* 的代码放进同一代码生成单元，从而引入任意标签。

因此，在内联汇编中应只使用 GNU 汇编器的**数字**[局部标签]。在汇编代码中定义符号可能导致因重复符号定义而产生汇编/链接错误。

此外，在 x86 使用默认 Intel 语法时，由于 [一个 LLVM bug]，不应使用仅由 `0` 和 `1` 组成的标签，例如 `0`、`11` 或 `101010`，它们可能被解释为二进制值。使用 `options(att_syntax)` 可避免歧义，但会影响*整个* `asm!` 块的语法。（关于 `options`，见下文[选项](#options)。）

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut a = 0;
unsafe {
    asm!(
        "mov {0}, 10",
        "2:",
        "sub {0}, 1",
        "cmp {0}, 3",
        "jle 2f",
        "jmp 2b",
        "2:",
        "add {0}, 2",
        out(reg) a
    );
}
assert_eq!(a, 5);
# }
```
这会把 `{0}` 寄存器的值从 10 递减到 3，再加 2，并存入 `a`。

该例子说明几点：

- 第一，同一数字可在同一内联块中多次用作标签。
- 第二，当数字标签用作引用（例如作为指令操作数）时，应加上后缀 “b”（backward，向后）或 “f”（forward，向前）。它会引用该方向上由该数字定义的最近标签。

[local labels]: https://sourceware.org/binutils/docs/as/Symbol-Names.html#Local-Labels
[an LLVM bug]: https://bugs.llvm.org/show_bug.cgi?id=36144

## 选项 {#选项}

默认情况下，内联汇编块的处理方式与带自定义调用约定的外部 FFI 函数调用相同：可读/写内存、可有可观察副作用等。但很多情况下希望向编译器提供更多关于汇编实际在做什么的信息，以便更好地优化。

以上一节的 `add` 指令为例：

```rust
# #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

let mut a: u64 = 4;
let b: u64 = 4;
unsafe {
    asm!(
        "add {0}, {1}",
        inlateout(reg) a, in(reg) b,
        options(pure, nomem, nostack),
    );
}
assert_eq!(a, 8);
# }
```
选项可作为 `asm!` 宏的可选最后参数提供。这里指定了三个选项：

- `pure` 表示 asm 代码没有可观察副作用，且其输出仅依赖输入。这允许编译器优化器减少甚至完全消除对该内联 asm 的调用。
- `nomem` 表示 asm 代码不读也不写内存。默认情况下编译器假定内联汇编可读写其可访问的任意内存地址（例如通过作为操作数传入的指针，或全局变量）。
- `nostack` 表示 asm 代码不会向栈上 push 任何数据。这允许编译器使用诸如 x86-64 上栈红区之类的优化，以避免调整栈指针。

这些选项让编译器能更好地优化使用 `asm!` 的代码，例如消除输出并不需要的纯 `asm!` 块。

完整可用选项及其效果见[参考手册](https://doc.rust-lang.org/stable/reference/inline-assembly.html)。
