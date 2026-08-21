+++
title = "第16章 内联汇编"
date = 2026-08-18T08:45:00+08:00
weight = 107
type = "docs"
description = "内联汇编 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/inline-assembly.html](https://doc.rust-lang.org/reference/inline-assembly.html)

r[asm]
# 内联汇编

r[asm.intro]
内联汇编支持由 [`asm!`]、[`naked_asm!`] 和 [`global_asm!`] 宏提供。可用于在编译器生成的汇编输出中嵌入手写汇编。

[`asm!`]: core::arch::asm
[`naked_asm!`]: core::arch::naked_asm
[`global_asm!`]: core::arch::global_asm

r[asm.stable-targets]
内联汇编在以下架构上已稳定：
- x86 与 x86-64
- ARM
- AArch64 与 Arm64EC
- RISC-V
- LoongArch
- s390x
- PowerPC 与 PowerPC64

若在不受支持的目标上使用汇编宏，编译器会报错。

r[asm.example]
## 示例

```rust
## #[cfg(target_arch = "x86_64")] {
use std::arch::asm;

// 使用移位与加法将 x 乘以 6
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
## }
```

r[asm.syntax]
## 语法

以下文法规定可传给 `asm!`、`global_asm!` 和 `naked_asm!` 宏的参数。

```grammar,assembly
@root AsmArgs -> AsmAttrFormatString (`,` AsmAttrFormatString)* (`,` AsmAttrOperand)* `,`?

FormatString -> STRING_LITERAL | RAW_STRING_LITERAL | MacroInvocation

AsmAttrFormatString -> (OuterAttribute)* FormatString

AsmOperand ->
      ClobberAbi
    | AsmOptions
    | RegOperand

AsmAttrOperand -> (OuterAttribute)* AsmOperand

ClobberAbi -> `clobber_abi` `(` Abi (`,` Abi)* `,`? `)`

AsmOptions ->
    `options` `(` ( AsmOption (`,` AsmOption)* `,`? )? `)`

AsmOption ->
      `pure`
    | `nomem`
    | `readonly`
    | `preserves_flags`
    | `noreturn`
    | `nostack`
    | `att_syntax`
    | `raw`

RegOperand -> (ParamName `=`)?
    (
          DirSpec `(` RegSpec `)` Expression
        | DualDirSpec `(` RegSpec `)` DualDirSpecExpression
        | `sym` PathExpression
        | `const` Expression
        | `label` `{` Statements? `}`
    )

ParamName -> IDENTIFIER_OR_KEYWORD | RAW_IDENTIFIER

DualDirSpecExpression ->
      Expression
    | Expression `=>` Expression

RegSpec -> RegisterClass | ExplicitRegister

RegisterClass -> IDENTIFIER_OR_KEYWORD

ExplicitRegister -> STRING_LITERAL

DirSpec ->
      `in`
    | `out`
    | `lateout`

DualDirSpec ->
      `inout`
    | `inlateout`
```

r[asm.scope]
## 作用域

r[asm.scope.intro]
内联汇编可通过以下三种方式之一使用。

r[asm.scope.asm]
使用 `asm!` 宏时，汇编代码在函数作用域中发出，并并入编译器为该函数生成的汇编代码。此汇编代码必须遵守[严格规则](#rules-for-inline-assembly)，以避免未定义行为。注意：在某些情况下，编译器可能选择将汇编代码作为单独函数发出，并生成对其的调用。

```rust
## #[cfg(target_arch = "x86_64")] {
unsafe { core::arch::asm!("/* {} */", in(reg) 0); }
## }
```

r[asm.scope.naked_asm]
使用 `naked_asm!` 宏时，汇编代码在函数作用域中发出，并构成该函数的全部汇编代码。`naked_asm!` 宏仅允许用于[裸函数](../attributes/04-codegen/#the-naked-attribute)。

```rust
## #[cfg(target_arch = "x86_64")] {
## #[unsafe(naked)]
## extern "C" fn wrapper() {
core::arch::naked_asm!("/* {} */", const 0);
## }
## }
```

r[asm.scope.global_asm]
使用 `global_asm!` 宏时，汇编代码在全局作用域中发出，位于函数之外。可用于用手写汇编实现完整函数，通常在使用任意寄存器与汇编器指令方面提供更大自由度。

```rust
## fn main() {}
## #[cfg(target_arch = "x86_64")]
core::arch::global_asm!("/* {} */", const 0);
```

r[asm.ts-args]
## 模板字符串参数

r[asm.ts-args.syntax]
汇编器模板使用与[格式字符串][format-syntax]相同的语法（即占位符由花括号指定）。

r[asm.ts-args.order]
对应参数可按顺序、按索引或按名称访问。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64;
let y: i64;
let z: i64;
// 这种写法
unsafe { core::arch::asm!("mov {}, {}", out(reg) x, in(reg) 5); }
// ... 这种写法
unsafe { core::arch::asm!("mov {0}, {1}", out(reg) y, in(reg) 5); }
// ... 以及这种写法
unsafe { core::arch::asm!("mov {out}, {in}", out = out(reg) z, in = in(reg) 5); }
// 行为均相同
assert_eq!(x, y);
assert_eq!(y, z);
## }
```

r[asm.ts-args.no-implicit]
但（由 [RFC #2795][rfc-2795] 引入的）隐式命名参数不受支持。

```rust
## #[cfg(target_arch = "x86_64")] {
let x = 5;
// 我们不能直接从作用域引用 `x`，需要像 `in(reg) x` 这样的操作数
unsafe { core::arch::asm!("/* {x} */"); } // ERROR: no argument named x
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.ts-args.one-or-more]
一次 `asm!` 调用可以有一个或多个模板字符串参数；带有多个模板字符串参数的 `asm!` 会被视为这些字符串之间用 `\n` 连接。预期用法是每个模板字符串参数对应一行汇编代码。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64;
let y: i64;
// 可将多个字符串分开书写，效果如同写在一起
unsafe { core::arch::asm!("mov eax, 5", "mov ecx, eax", out("rax") x, out("rcx") y); }
assert_eq!(x, y);
## }
```

r[asm.ts-args.before-other-args]
所有模板字符串参数都必须出现在其他任何参数之前。

```rust
let x = 5;
## #[cfg(target_arch = "x86_64")] {
// 模板字符串需要出现在 asm 调用的最前面
unsafe { core::arch::asm!("/* {x} */", x = const 5, "ud2"); } // ERROR: unexpected token
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.ts-args.positional-first]
与格式字符串一样，位置参数必须出现在命名参数和显式[寄存器操作数](#register-operands)之前。

```rust
## #[cfg(target_arch = "x86_64")] {
// 命名操作数需要放在位置操作数之后
unsafe { core::arch::asm!("/* {x} {} */", x = const 5, in(reg) 5); }
// ERROR: positional arguments cannot follow named arguments or explicit register arguments
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

```rust
## #[cfg(target_arch = "x86_64")] {
// 也不能把显式寄存器放在位置操作数之前
unsafe { core::arch::asm!("/* {} */", in("eax") 0, in(reg) 5); }
// ERROR: positional arguments cannot follow named arguments or explicit register arguments
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.ts-args.register-operands]
显式寄存器操作数不能被模板字符串中的占位符使用。

```rust
## #[cfg(target_arch = "x86_64")] {
// 显式寄存器操作数不会被替换，请在字符串中显式使用 `eax`
unsafe { core::arch::asm!("/* {} */", in("eax") 5); }
// ERROR: invalid reference to argument at index 0
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.ts-args.at-least-once]
所有其他命名与位置操作数都必须在模板字符串中至少出现一次，否则会生成编译器错误。

```rust
## #[cfg(target_arch = "x86_64")] {
// 必须在格式字符串中写出所有操作数
unsafe { core::arch::asm!("", in(reg) 5, x = const 5); }
// ERROR: multiple unused asm arguments
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.ts-args.opaque]
确切的汇编代码语法是目标相关的，对编译器不透明——唯一例外是操作数如何被代入模板字符串以形成传给汇编器的代码。

r[asm.ts-args.llvm-syntax]
目前，所有受支持的目标都遵循 LLVM 内部汇编器所用的汇编语法，该语法通常与 GNU 汇编器（GAS）一致。在 x86 上，默认使用 GAS 的 `.intel_syntax noprefix` 模式。在 ARM 上，使用 `.syntax unified` 模式。这些目标对汇编代码还有额外限制：任何汇编器状态（例如可用 `.section` 更改的当前段）都必须在 asm 字符串结束时恢复为其原始值。不符合 GAS 语法的汇编代码会导致汇编器特定行为。内联汇编所用指令的进一步约束见[指令支持](#directives-support)。

[format-syntax]: std::fmt#syntax
[rfc-2795]: https://github.com/rust-lang/rfcs/pull/2795

r[asm.attributes]
## 属性

r[asm.attributes.supported-attributes]
在语义上，内联汇编模板字符串与操作数仅接受 [`cfg`] 和 [`cfg_attr`] 属性。其他属性会被解析，但在汇编宏展开时会被拒绝。

```rust
## fn main() {}
## #[cfg(target_arch = "x86_64")]
core::arch::global_asm!(
    #[cfg(not(panic = "abort"))]
    ".cfi_startproc",
    // ...
    "ret",
    #[cfg(not(panic = "abort"))]
    ".cfi_endproc",
);
```

> **注意**
> 在 `rustc` 中，汇编宏对这些属性的处理与语言中处理类似属性的常规系统是分开实现的。这解释了为何支持的属性种类有限，并可能导致行为上的细微差异。

r[asm.attributes.starts-with-template]
在语法上，第一个操作数之前必须至少有一个模板字符串。

```rust
// 这会被拒绝，因为 `a = out(reg) x` 不能解析为
// 模板字符串。
core::arch::asm!(
    #[cfg(false)]
    a = out(reg) x, // ERROR.
    "",
);
```

[`cfg`]: conditional-compilation.md#the-cfg-attribute
[`cfg_attr`]: conditional-compilation.md#the-cfg_attr-attribute

r[asm.operand-type]
## 操作数类型

r[asm.operand-type.supported-operands]
支持多种类型的操作数：

r[asm.operand-type.supported-operands.in]
* `in(<reg>) <expr>`
  - `<reg>` 可以指寄存器类或显式寄存器。分配的寄存器名会被替换进 asm 模板字符串。
  - 在汇编代码开始时，分配的寄存器将包含 `<expr>` 的值。
  - 在汇编代码结束时，分配的寄存器必须仍包含相同的值（除非有 `lateout` 分配到同一寄存器）。

```rust
## #[cfg(target_arch = "x86_64")] {
// ``in` 可用于向内联汇编传入值...
unsafe { core::arch::asm!("/* {} */", in(reg) 5); }
## }
```

> **注意**
> 若值的类型小于寄存器，高位的值是平台相关的。有些目标会将高位清零，有些则保持不变。

r[asm.operand-type.supported-operands.out]
* `out(<reg>) <expr>`
  - `<reg>` 可以指寄存器类或显式寄存器。分配的寄存器名会被替换进 asm 模板字符串。
  - 在汇编代码开始时，分配的寄存器将包含未定义的值。
  - `<expr>` 必须是（可能未初始化的）位置表达式（place expression），汇编代码结束时会将分配寄存器的内容写入该表达式。
  - 也可以用下划线（`_`）代替表达式，这样在汇编代码结束时会丢弃寄存器的内容（实际上相当于 clobber）。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64;
// 而 `out` 可用于将值传回 Rust。
unsafe { core::arch::asm!("/* {} */", out(reg) x); }
## }
```

r[asm.operand-type.supported-operands.lateout]
* `lateout(<reg>) <expr>`
  - 与 `out` 相同，但寄存器分配器可以复用已分配给 `in` 的寄存器。
  - 应仅在读取所有输入之后再写入该寄存器，否则可能覆盖某个输入。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64;
// `lateout` 与 `out` 相同
// 但编译器知道在我们覆盖它时，已不再关心任何输入的值。
unsafe { core::arch::asm!("mov {}, 5", lateout(reg) x); }
assert_eq!(x, 5)
## }
```

r[asm.operand-type.supported-operands.inout]
* `inout(<reg>) <expr>`
  - `<reg>` 可以指寄存器类或显式寄存器。分配的寄存器名会被替换进 asm 模板字符串。
  - 在汇编代码开始时，分配的寄存器将包含 `<expr>` 的值。
  - `<expr>` 必须是可变且已初始化的位置表达式，汇编代码结束时会将分配寄存器的内容写入该表达式。

```rust
## #[cfg(target_arch = "x86_64")] {
let mut x: i64 = 4;
// `inout` 可用于在寄存器中修改值
unsafe { core::arch::asm!("inc {}", inout(reg) x); }
assert_eq!(x, 5);
## }
```

r[asm.operand-type.supported-operands.inout-arrow]
* `inout(<reg>) <in expr> => <out expr>`
  - 与 `inout` 相同，但寄存器的初始值取自 `<in expr>` 的值。
  - `<out expr>` 必须是（可能未初始化的）位置表达式，汇编代码结束时会将分配寄存器的内容写入该表达式。
  - 也可以用下划线（`_`）代替 `<out expr>` 的表达式，这样在汇编代码结束时会丢弃寄存器的内容（实际上相当于 clobber）。
  - `<in expr>` 与 `<out expr>` 可以有不同的类型。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64;
// `inout` 也可以将值移动到不同的位置
unsafe { core::arch::asm!("inc {}", inout(reg) 4u64=>x); }
assert_eq!(x, 5);
## }
```

r[asm.operand-type.supported-operands.inlateout]
* `inlateout(<reg>) <expr>` / `inlateout(<reg>) <in expr> => <out expr>`
  - 与 `inout` 相同，但寄存器分配器可以复用已分配给 `in` 的寄存器（当编译器知道该 `in` 与 `inlateout` 具有相同初始值时可能发生）。
  - 应仅在读取所有输入之后再写入该寄存器，否则可能覆盖某个输入。

```rust
## #[cfg(target_arch = "x86_64")] {
let mut x: i64 = 4;
// `inlateout` 是使用 `lateout` 的 `inout`
unsafe { core::arch::asm!("inc {}", inlateout(reg) x); }
assert_eq!(x, 5);
## }
```

r[asm.operand-type.supported-operands.sym]
* `sym <path>`
  - `<path>` 必须引用 `fn` 或 `static`。
  - 指向该项的经过名称修饰（mangled）的符号名会被替换进 asm 模板字符串。
  - 替换后的字符串不包含任何修饰符（例如 GOT、PLT、重定位等）。
  - 允许 `<path>` 指向 `#[thread_local]` 静态变量，此时汇编代码可将该符号与重定位（例如 `@plt`、`@TPOFF`）组合，以读取线程局部数据。

```rust
## #[cfg(target_arch = "x86_64")] {
extern "C" fn foo() {
    println!("Hello from inline assembly")
}
// `sym` 可用于引用函数（即使它没有我们可以直接书写的
// 外部名称）
unsafe { core::arch::asm!("call {}", sym foo, clobber_abi("C")); }
## }
```

r[asm.operand-type.supported-operands.const]
* `const <expr>`
  - `<expr>` 必须是整数常量表达式。该表达式遵循与内联 `const` 块相同的规则。
  - 表达式的类型可以是任意整数类型，但与整数字面量一样，默认为 `i32`。
  - 表达式的值会格式化为字符串并直接替换进 asm 模板字符串。

```rust
## #[cfg(target_arch = "x86_64")] {
// 重排 [0, 1, 2, 3] => [3, 2, 0, 1]
const SHUFFLE: u8 = 0b01_00_10_11;
let x: core::arch::x86_64::__m128 = unsafe { core::mem::transmute([0u32, 1u32, 2u32, 3u32]) };
let y: core::arch::x86_64::__m128;
// 向需要立即数的指令（如 `pshufd`）传入常量值
unsafe {
    core::arch::asm!("pshufd {xmm}, {xmm}, {shuffle}",
        xmm = inlateout(xmm_reg) x=>y,
        shuffle = const SHUFFLE
    );
}
let y: [u32; 4] = unsafe { core::mem::transmute(y) };
assert_eq!(y, [3, 2, 0, 1]);
## }
```

r[asm.operand-type.supported-operands.label]
* `label <block>`
  - 该块的地址会被替换进 asm 模板字符串。汇编代码可以跳转到被替换的地址。
  - 对于区分直接跳转与间接跳转的目标（例如启用了 `cf-protection` 的 x86-64），汇编代码不得间接跳转到被替换的地址。
  - 执行完该块后，`asm!` 表达式返回。
  - 该块的类型必须是 unit 或 `!`（never）。
  - 该块开启新的安全上下文；即使整个 `asm!` 表达式已包裹在 `unsafe` 中，`label` 块内的不安全操作仍须用内层 `unsafe` 块包裹。

```rust
## #[cfg(target_arch = "x86_64")]
unsafe {
    core::arch::asm!("jmp {}", label {
        println!("Hello from inline assembly label");
    });
}
```

r[asm.operand-type.left-to-right]
操作数表达式按从左到右的顺序求值，与函数调用参数相同。在 `asm!` 执行完毕后，输出也按从左到右的顺序写入。这一点在两个输出指向同一位置时很重要：该位置将包含最右侧输出的值。

```rust
## #[cfg(target_arch = "x86_64")] {
let mut y: i64;
// y 的值来自第二个输出，而非第一个
unsafe { core::arch::asm!("mov {}, 0", "mov {}, 1", out(reg) y, out(reg) y); }
assert_eq!(y, 1);
## }
```

r[asm.operand-type.naked_asm-restriction]
因为 `naked_asm!` 定义的是整个函数体，且编译器无法为处理操作数而发出任何额外代码，所以它只能使用 `sym` 和 `const` 操作数。

r[asm.operand-type.global_asm-restriction]
因为 `global_asm!` 存在于函数之外，所以它只能使用 `sym` 和 `const` 操作数。

```rust
## fn main() {}
// 不允许使用寄存器操作数，因为我们不在函数中
## #[cfg(target_arch = "x86_64")]
core::arch::global_asm!("", in(reg) 5);
// 错误：`in` 操作数不能与 `global_asm!` 一起使用
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

```rust
## fn main() {}
fn foo() {}

## #[cfg(target_arch = "x86_64")]
// 不过，`const` 和 `sym` 都是允许的
core::arch::global_asm!("/* {} {} */", const 0, sym foo);
```

r[asm.register-operands]
## 寄存器操作数

r[asm.register-operands.register-or-class]
输入与输出操作数既可指定为显式寄存器，也可指定为寄存器类，由寄存器分配器从该类中选取寄存器。显式寄存器以字符串字面量指定（例如 `"eax"`），寄存器类则以标识符指定（例如 `reg`）。

```rust
## #[cfg(target_arch = "x86_64")] {
let mut y: i64;
// 既可使用 `reg`，也可使用如 `eax` 这样的显式寄存器来获得整数寄存器
unsafe { core::arch::asm!("mov eax, {:e}", in(reg) 5, lateout("eax") y); }
assert_eq!(y, 5);
## }
```

r[asm.register-operands.equivalence-to-base-register]
注意，显式寄存器会将寄存器别名（例如 ARM 上的 `r14` 与 `lr`）以及同一寄存器的较小视图（例如 `eax` 与 `rax`）视为与基寄存器等价。

r[asm.register-operands.error-two-operands]
对两个输入操作数或两个输出操作数使用同一显式寄存器是编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
// 不能两次指定 eax
unsafe { core::arch::asm!("", in("eax") 5, in("eax") 4); }
// ERROR: register `eax` conflicts with register `eax`
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```
```rust
## #[cfg(target_arch = "x86_64")] {
// ……即便使用不同别名也不行
unsafe { core::arch::asm!("", in("ax") 5, in("rax") 4); }
// ERROR: register `rax` conflicts with register `ax`
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-operands.error-overlapping]
此外，在输入操作数或输出操作数中使用重叠寄存器（例如 ARM VFP）同样是编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
// al 与 ax 重叠，因此不能同时指定二者。
unsafe { core::arch::asm!("", in("ax") 5, in("al") 4i8); }
// ERROR: register `al` conflicts with register `ax`
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-operands.allowed-types]
内联汇编操作数仅允许使用以下类型：
- 整数（有符号与无符号）
- 浮点数
- 指针（仅瘦指针）
- 函数指针
- SIMD 向量（以 `#[repr(simd)]` 定义且实现 `Copy` 的结构体）。这包括 `std::arch` 中定义的架构特定向量类型，例如 `__m128`（x86）或 `int8x16_t`（ARM）。

```rust
## #[cfg(target_arch = "x86_64")] {
extern "C" fn foo() {}

// 允许使用整数……
let y: i64 = 5;
unsafe { core::arch::asm!("/* {} */", in(reg) y); }

// 以及指针……
let py = &raw const y;
unsafe { core::arch::asm!("/* {} */", in(reg) py); }

// 浮点数也可以……
let f = 1.0f32;
unsafe { core::arch::asm!("/* {} */", in(xmm_reg) f); }

// 甚至函数指针和 SIMD 向量。
let func: extern "C" fn() = foo;
unsafe { core::arch::asm!("/* {} */", in(reg) func); }

let z = unsafe { core::arch::x86_64::_mm_set_epi64x(1, 0) };
unsafe { core::arch::asm!("/* {} */", in(xmm_reg) z); }
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
struct Foo;
let x: Foo = Foo;
// 不允许使用结构体这类复杂类型
unsafe { core::arch::asm!("/* {} */", in(reg) x); }
// ERROR: cannot use value of type `Foo` for inline assembly
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-operands.supported-register-classes]
当前支持的寄存器类如下：

| 架构 | 寄存器类 | 寄存器 | LLVM 约束码 |
| ------------ | -------------- | --------- | -------------------- |
| x86 | `reg` | `ax`, `bx`, `cx`, `dx`, `si`, `di`, `bp`, `r[8-15]`（仅 x86-64） | `r` |
| x86 | `reg_abcd` | `ax`, `bx`, `cx`, `dx` | `Q` |
| x86-32 | `reg_byte` | `al`, `bl`, `cl`, `dl`, `ah`, `bh`, `ch`, `dh` | `q` |
| x86-64 | `reg_byte`\* | `al`, `bl`, `cl`, `dl`, `sil`, `dil`, `bpl`, `r[8-15]b` | `q` |
| x86 | `xmm_reg` | `xmm[0-7]` (x86) `xmm[0-15]` (x86-64) | `x` |
| x86 | `ymm_reg` | `ymm[0-7]` (x86) `ymm[0-15]` (x86-64) | `x` |
| x86 | `zmm_reg` | `zmm[0-7]` (x86) `zmm[0-31]` (x86-64) | `v` |
| x86 | `kreg` | `k[1-7]` | `Yk` |
| x86 | `kreg0` | `k0` | 仅限 clobber |
| x86 | `x87_reg` | `st([0-7])` | 仅限 clobber |
| x86 | `mmx_reg` | `mm[0-7]` | 仅限 clobber |
| x86-64 | `tmm_reg` | `tmm[0-7]` | 仅限 clobber |
| AArch64 | `reg` | `x[0-30]` | `r` |
| AArch64 | `vreg` | `v[0-31]` | `w` |
| AArch64 | `vreg_low16` | `v[0-15]` | `x` |
| AArch64 | `preg` | `p[0-15]`, `ffr` | 仅限 clobber |
| Arm64EC | `reg` | `x[0-12]`, `x[15-22]`, `x[25-27]`, `x30` | `r` |
| Arm64EC | `vreg` | `v[0-15]` | `w` |
| Arm64EC | `vreg_low16` | `v[0-15]` | `x` |
| ARM (ARM/Thumb2) | `reg` | `r[0-12]`, `r14` | `r` |
| ARM (Thumb1) | `reg` | `r[0-7]` | `r` |
| ARM | `sreg` | `s[0-31]` | `t` |
| ARM | `sreg_low16` | `s[0-15]` | `x` |
| ARM | `dreg` | `d[0-31]` | `w` |
| ARM | `dreg_low16` | `d[0-15]` | `t` |
| ARM | `dreg_low8` | `d[0-8]` | `x` |
| ARM | `qreg` | `q[0-15]` | `w` |
| ARM | `qreg_low8` | `q[0-7]` | `t` |
| ARM | `qreg_low4` | `q[0-3]` | `x` |
| RISC-V | `reg` | `x1`, `x[5-7]`, `x[9-15]`, `x[16-31]`（非 RV32E） | `r` |
| RISC-V | `freg` | `f[0-31]` | `f` |
| RISC-V | `vreg` | `v[0-31]` | 仅限 clobber |
| LoongArch | `reg` | `$r1`, `$r[4-20]`, `$r[23,30]` | `r` |
| LoongArch | `freg` | `$f[0-31]` | `f` |
| s390x | `reg` | `r[0-10]`, `r[12-14]` | `r` |
| s390x | `reg_addr` | `r[1-10]`, `r[12-14]` | `a` |
| s390x | `freg` | `f[0-15]` | `f` |
| s390x | `vreg` | `v[0-31]` | `v` |
| s390x | `areg` | `a[2-15]` | 仅限 clobber |
| PowerPC | `reg` | `r0`, `r[3-12]`, `r[14-28]` | `r` |
| PowerPC | `reg_nonzero` | `r[3-12]`, `r[14-28]` | `b` |
| PowerPC | `spe_acc` | `spe_acc` | 仅限 clobber |
| PowerPC64 | `reg` | `r0`, `r[3-12]`, `r[14-29]` | `r` |
| PowerPC64 | `reg_nonzero` | `r[3-12]`, `r[14-29]` | `b` |
| PowerPC/PowerPC64 | `freg` | `f[0-31]` | `f` |
| PowerPC/PowerPC64 | `vreg` | `v[0-31]` | `v` |
| PowerPC/PowerPC64 | `vsreg` | `vs[0-63]` | `wa` |
| PowerPC/PowerPC64 | `cr` | `cr[0-7]`, `cr` | 仅限 clobber |
| PowerPC/PowerPC64 | `ctr` | `ctr` | 仅限 clobber |
| PowerPC/PowerPC64 | `lr` | `lr` | 仅限 clobber |
| PowerPC/PowerPC64 | `xer` | `xer` | 仅限 clobber |

> **注意**
> - 在 x86 上，我们对 `reg_byte` 的处理与 `reg` 不同，因为编译器可以分别分配 `al` 和 `ah`，而 `reg` 会保留整个寄存器。
> - 在 x86-64 上，高字节寄存器（例如 `ah`）在 `reg_byte` 寄存器类中不可用。
> - 某些寄存器类标记为「仅限 clobber」，表示这些类中的寄存器不能用于输入或输出，只能以 `out(<explicit register>) _` 或 `lateout(<explicit register>) _` 的形式作为 clobber。
> - `spe_acc` 寄存器仅在 PowerPC SPE 目标上可用。

r[asm.register-operands.value-type-constraints]
每个寄存器类对其可搭配的值类型都有约束。这是必要的，因为将值装入寄存器的方式取决于其类型。例如，在大端系统上，将 `i32x4` 和 `i8x16` 装入 SIMD 寄存器，即便二者的按字节内存表示相同，寄存器内容也可能不同。某一寄存器类所支持类型的可用性，可能取决于当前启用了哪些目标特性。

| 架构 | 寄存器类 | 目标特性 | 允许的类型 |
| ------------ | -------------- | -------------- | ------------- |
| x86-32 | `reg` | 无 | `i16`, `i32`, `f32` |
| x86-64 | `reg` | 无 | `i16`, `i32`, `f32`, `i64`, `f64` |
| x86 | `reg_byte` | 无 | `i8` |
| x86 | `xmm_reg` | `sse` | `i32`, `f32`, `i64`, `f64`, `i128`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` |
| x86 | `ymm_reg` | `avx` | `i32`, `f32`, `i64`, `f64`, `i128`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` <br> `i8x32`, `i16x16`, `i32x8`, `i64x4`, `f32x8`, `f64x4` |
| x86 | `zmm_reg` | `avx512f` | `i32`, `f32`, `i64`, `f64`, `i128`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` <br> `i8x32`, `i16x16`, `i32x8`, `i64x4`, `f32x8`, `f64x4` <br> `i8x64`, `i16x32`, `i32x16`, `i64x8`, `f32x16`, `f64x8` |
| x86 | `kreg` | `avx512f` | `i8`, `i16` |
| x86 | `kreg` | `avx512bw` | `i32`, `i64` |
| x86 | `mmx_reg` | N/A | 仅限 clobber |
| x86 | `x87_reg` | N/A | 仅限 clobber |
| x86 | `tmm_reg` | N/A | 仅限 clobber |
| AArch64 | `reg` | 无 | `i8`, `i16`, `i32`, `f32`, `i64`, `f64` |
| AArch64 | `vreg` | `neon` | `i8`, `i16`, `i32`, `f32`, `i64`, `f64`, <br> `i8x8`, `i16x4`, `i32x2`, `i64x1`, `f32x2`, `f64x1`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` |
| AArch64 | `preg` | N/A | 仅限 clobber |
| Arm64EC | `reg` | 无 | `i8`, `i16`, `i32`, `f32`, `i64`, `f64` |
| Arm64EC | `vreg` | `neon` | `i8`, `i16`, `i32`, `f32`, `i64`, `f64`, <br> `i8x8`, `i16x4`, `i32x2`, `i64x1`, `f32x2`, `f64x1`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` |
| ARM | `reg` | 无 | `i8`, `i16`, `i32`, `f32` |
| ARM | `sreg` | `vfp2` | `i32`, `f32` |
| ARM | `dreg` | `vfp2` | `i64`, `f64`, `i8x8`, `i16x4`, `i32x2`, `i64x1`, `f32x2` |
| ARM | `qreg` | `neon` | `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4` |
| RISC-V32 | `reg` | 无 | `i8`, `i16`, `i32`, `f32` |
| RISC-V64 | `reg` | 无 | `i8`, `i16`, `i32`, `f32`, `i64`, `f64` |
| RISC-V | `freg` | `f` | `f32` |
| RISC-V | `freg` | `d` | `f64` |
| RISC-V | `vreg` | N/A | 仅限 clobber |
| LoongArch32 | `reg` | 无 | `i8`, `i16`, `i32`, `f32` |
| LoongArch64 | `reg` | 无 | `i8`, `i16`, `i32`, `i64`, `f32`, `f64` |
| LoongArch | `freg` | `f` | `f32` |
| LoongArch | `freg` | `d` | `f64` |
| s390x | `reg`, `reg_addr` | 无 | `i8`, `i16`, `i32`, `i64` |
| s390x | `freg` | 无 | `f32`, `f64` |
| s390x | `vreg` | `vector` | `i32`, `f32`, `i64`, `f64`, `i128`, <br> `i8x16`, `i16x8`, `i32x4`, `i64x2`, `f32x4`, `f64x2` |
| s390x | `areg` | N/A | 仅限 clobber |
| PowerPC | `spe_acc` | 无 | 仅限 clobber |
| PowerPC/PowerPC64 | `reg` | 无 | `i8`, `i16`, `i32`, `i64`（仅 PowerPC64） |
| PowerPC/PowerPC64 | `reg_nonzero` | 无 | `i8`, `i16`, `i32`, `i64`（仅 PowerPC64） |
| PowerPC/PowerPC64 | `freg` | 无 | `f32`, `f64` |
| PowerPC/PowerPC64 | `vreg` | `altivec` | `i8x16`, `i16x8`, `i32x4`, `f32x4` |
| PowerPC/PowerPC64 | `vreg` | `vsx` | `f32`, `f64`, `i64x2`, `f64x2` |
| PowerPC/PowerPC64 | `vsreg` | `vsx` | vsx 与 altivec 的 `vreg` 类型之并集 |
| PowerPC/PowerPC64 | `cr` | 无 | 仅限 clobber |
| PowerPC/PowerPC64 | `ctr` | 无 | 仅限 clobber |
| PowerPC/PowerPC64 | `lr` | 无 | 仅限 clobber |
| PowerPC/PowerPC64 | `xer` | 无 | 仅限 clobber |

> **注意**
> 就上表而言，指针、函数指针以及 `isize`/`usize` 按等价整数类型处理（依目标分别为 `i16`/`i32`/`i64`）。

```rust
## #[cfg(target_arch = "x86_64")] {
let x = 5i32;
let y = -1i8;
let z = unsafe { core::arch::x86_64::_mm_set_epi64x(1, 0) };

// `reg` 可用于 `i32`，`reg_byte` 可用于 `i8`，`xmm_reg` 可用于 `__m128i`
// 不能将 `tmm0` 用作输入或输出，但可以将其 clobber。
unsafe { core::arch::asm!("/* {} {} {} */", in(reg) x, in(reg_byte) y, in(xmm_reg) z, out("tmm0") _); }
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let z = unsafe { core::arch::x86_64::_mm_set_epi64x(1, 0) };
// 不能将 `__m128i` 传给 `reg` 输入
unsafe { core::arch::asm!("/* {} */", in(reg) z); }
// ERROR: type `__m128i` cannot be used with this register class
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-operands.smaller-value]
若值的大小小于其所分配的寄存器，则对输入而言该寄存器的高位为未定义值，对输出而言高位会被忽略。唯一例外是 RISC-V 上的 `freg` 寄存器类：按 RISC-V 架构要求，`f32` 值会以 NaN-boxing 的方式放入 `f64`。

<!--no_run, 此测试具有非确定性运行时行为-->
```rust
## #[cfg(target_arch = "x86_64")] {
let mut x: i64;
// 把 32 位值移入 64 位值，糟糕。
#[allow(asm_sub_register)] // rustc 会警告这种行为
unsafe { core::arch::asm!("mov {}, {}", lateout(reg) x, in(reg) 4i32); }
// 高 32 位不确定
assert_eq!(x, 4); // 此断言不保证成功
assert_eq!(x & 0xFFFFFFFF, 4); // 但这条会成功
## }
```

r[asm.register-operands.separate-input-output]
当 `inout` 操作数分别指定输入与输出表达式时，两个表达式必须具有相同类型。唯一例外是二者均为指针或整数：此时只要求大小相同。存在此限制是因为 LLVM 与 GCC 的寄存器分配器有时无法处理类型不同的绑定操作数。

```rust
## #[cfg(target_arch = "x86_64")] {
// 指针与整数可以混用（只要大小相同）
let x: isize = 0;
let y: *mut ();
// 用内联汇编的手法将 `isize` 转为 `*mut ()`
unsafe { core::arch::asm!("/*{}*/", inout(reg) x=>y); }
assert!(y.is_null()); // 制造空指针的极其迂回的方式
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i32 = 0;
let y: f32;
// 但不能像这样把 `i32` 重新解释为 `f32`
unsafe { core::arch::asm!("/* {} */", inout(reg) x=>y); }
// ERROR: incompatible types for asm inout argument
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-names]
## 寄存器名称

r[asm.register-names.supported-register-aliases]
部分寄存器有多个名称。编译器将它们全部视为与基寄存器名称等价。所有受支持的寄存器别名如下：

| 架构 | 基寄存器 | 别名 |
| ------------ | ------------- | ------- |
| x86 | `ax` | `eax`, `rax` |
| x86 | `bx` | `ebx`, `rbx` |
| x86 | `cx` | `ecx`, `rcx` |
| x86 | `dx` | `edx`, `rdx` |
| x86 | `si` | `esi`, `rsi` |
| x86 | `di` | `edi`, `rdi` |
| x86 | `bp` | `bpl`, `ebp`, `rbp` |
| x86 | `sp` | `spl`, `esp`, `rsp` |
| x86 | `ip` | `eip`, `rip` |
| x86 | `st(0)` | `st` |
| x86 | `r[8-15]` | `r[8-15]b`, `r[8-15]w`, `r[8-15]d` |
| x86 | `xmm[0-31]` | `ymm[0-31]`, `zmm[0-31]` |
| AArch64 | `x[0-30]` | `w[0-30]` |
| AArch64 | `x29` | `fp` |
| AArch64 | `x30` | `lr` |
| AArch64 | `sp` | `wsp` |
| AArch64 | `xzr` | `wzr` |
| AArch64 | `v[0-31]` | `b[0-31]`, `h[0-31]`, `s[0-31]`, `d[0-31]`, `q[0-31]` |
| Arm64EC | `x[0-30]` | `w[0-30]` |
| Arm64EC | `x29` | `fp` |
| Arm64EC | `x30` | `lr` |
| Arm64EC | `sp` | `wsp` |
| Arm64EC | `xzr` | `wzr` |
| Arm64EC | `v[0-15]` | `b[0-15]`, `h[0-15]`, `s[0-15]`, `d[0-15]`, `q[0-15]` |
| ARM | `r[0-3]` | `a[1-4]` |
| ARM | `r[4-9]` | `v[1-6]` |
| ARM | `r9` | `rfp` |
| ARM | `r10` | `sl` |
| ARM | `r11` | `fp` |
| ARM | `r12` | `ip` |
| ARM | `r13` | `sp` |
| ARM | `r14` | `lr` |
| ARM | `r15` | `pc` |
| RISC-V | `x0` | `zero` |
| RISC-V | `x1` | `ra` |
| RISC-V | `x2` | `sp` |
| RISC-V | `x3` | `gp` |
| RISC-V | `x4` | `tp` |
| RISC-V | `x[5-7]` | `t[0-2]` |
| RISC-V | `x8` | `fp`, `s0` |
| RISC-V | `x9` | `s1` |
| RISC-V | `x[10-17]` | `a[0-7]` |
| RISC-V | `x[18-27]` | `s[2-11]` |
| RISC-V | `x[28-31]` | `t[3-6]` |
| RISC-V | `f[0-7]` | `ft[0-7]` |
| RISC-V | `f[8-9]` | `fs[0-1]` |
| RISC-V | `f[10-17]` | `fa[0-7]` |
| RISC-V | `f[18-27]` | `fs[2-11]` |
| RISC-V | `f[28-31]` | `ft[8-11]` |
| LoongArch | `$r0` | `$zero` |
| LoongArch | `$r1` | `$ra` |
| LoongArch | `$r2` | `$tp` |
| LoongArch | `$r3` | `$sp` |
| LoongArch | `$r[4-11]` | `$a[0-7]` |
| LoongArch | `$r[12-20]` | `$t[0-8]` |
| LoongArch | `$r21` | |
| LoongArch | `$r22` | `$fp`, `$s9` |
| LoongArch | `$r[23-31]` | `$s[0-8]` |
| LoongArch | `$f[0-7]` | `$fa[0-7]` |
| LoongArch | `$f[8-23]` | `$ft[0-15]` |
| LoongArch | `$f[24-31]` | `$fs[0-7]` |
| PowerPC/PowerPC64 | `r1` | `sp` |
| PowerPC/PowerPC64 | `r31` | `fp` |
| PowerPC/PowerPC64 | `r[0-31]` | `[0-31]` |
| PowerPC/PowerPC64 | `f[0-31]` | `fr[0-31]`|

```rust
## #[cfg(target_arch = "x86_64")] {
let z = 0i64;
// rax 是 eax 和 ax 的别名
unsafe { core::arch::asm!("", in("rax") z); }
## }
```

r[asm.register-names.not-for-io]
部分寄存器不能用作输入或输出操作数：

| 架构 | 不支持的寄存器 | 原因 |
| ------------ | -------------------- | ------ |
| 所有 | `sp`, `r15` (s390x), `r1` (PowerPC 与 PowerPC64) | 汇编代码结束时，或跳转到 `label` 块之前，必须将栈指针恢复为其原始值。 |
| 所有 | `bp` (x86), `x29` (AArch64 与 Arm64EC), `x8` (RISC-V), `$fp` (LoongArch), `r11` (s390x), `fp` (PowerPC 与 PowerPC64) | 帧指针不能用作输入或输出。 |
| ARM | `r7` 或 `r11` | 在 ARM 上，帧指针可以是 `r7` 或 `r11`，取决于具体目标。帧指针不能用作输入或输出。 |
| 所有 | `si` (x86-32), `bx` (x86-64), `r6` (ARM), `x19` (AArch64 与 Arm64EC), `x9` (RISC-V), `$s8` (LoongArch), `r29` 与 `r30` (PowerPC), `r30` (PowerPC64) | LLVM 在内部将其用作具有复杂栈帧的函数的「基址指针」。 |
| x86 | `ip` | 这是程序计数器，不是真正的寄存器。 |
| AArch64 | `xzr` | 这是不可修改的常量零寄存器。 |
| AArch64 | `x18` | 在某些 AArch64 目标上，这是操作系统保留的寄存器。 |
| Arm64EC | `xzr` | 这是不可修改的常量零寄存器。 |
| Arm64EC | `x18` | 这是操作系统保留的寄存器。 |
| Arm64EC | `x13`, `x14`, `x23`, `x24`, `x28`, `v[16-31]`, `p[0-15]`, `ffr` | 这些是 Arm64EC 不支持的 AArch64 寄存器。 |
| ARM | `pc` | 这是程序计数器，不是真正的寄存器。 |
| ARM | `r9` | 在某些 ARM 目标上，这是操作系统保留的寄存器。 |
| RISC-V | `x0` | 这是不可修改的常量零寄存器。 |
| RISC-V | `gp`, `tp` | 这些寄存器被保留，不能用作输入或输出。 |
| LoongArch | `$r0` 或 `$zero` | 这是不可修改的常量零寄存器。 |
| LoongArch | `$r2` 或 `$tp` | 这是为 TLS 保留的。 |
| LoongArch | `$r21` | 这是由 ABI 保留的。 |
| s390x | `c[0-15]` | 由内核保留。 |
| s390x | `a[0-1]` | 保留供系统使用。 |
| PowerPC/PowerPC64 | `r2`, `r13` | 这些是系统保留寄存器。 |
| PowerPC/PowerPC64 | `vrsave` | vrsave 寄存器不能用作输入或输出。 |

```rust
## #[cfg(target_arch = "x86_64")] {
// bp 是保留寄存器
unsafe { core::arch::asm!("", in("bp") 5i32); }
// ERROR: invalid register `bp`: the frame pointer cannot be used as an operand for inline asm
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.register-names.fp-bp-reserved]
帧指针和基址指针寄存器保留供 LLVM 内部使用。虽然 `asm!` 语句不能显式指定使用保留寄存器，但在某些情况下 LLVM 会为 `reg` 操作数分配其中一个保留寄存器。使用保留寄存器的汇编代码应格外小心，因为 `reg` 操作数可能使用相同的寄存器。

r[asm.template-modifiers]
## 模板修饰符

r[asm.template-modifiers.intro]
占位符可以通过修饰符进行扩展，修饰符在花括号中的 `:` 之后指定。这些修饰符不影响寄存器分配，但会改变操作数插入模板字符串时的格式化方式。

r[asm.template-modifiers.only-one]
每个模板占位符只允许一个修饰符。

```rust
## #[cfg(target_arch = "x86_64")] {
// 不能同时指定 `r` 和 `e`。
unsafe { core::arch::asm!("/* {:er}", in(reg) 5i32); }
// ERROR: asm template modifier must be a single character
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.template-modifiers.supported-modifiers]
支持的修饰符是 LLVM（以及 GCC）的 [asm 模板参数修饰符][llvm-argmod] 的子集，但不使用相同的字母代码。

| 架构 | 寄存器类 | 修饰符 | 示例输出 | LLVM 修饰符 |
| ------------ | -------------- | -------- | -------------- | ------------- |
| x86-32 | `reg` | None | `eax` | `k` |
| x86-64 | `reg` | None | `rax` | `q` |
| x86-32 | `reg_abcd` | `l` | `al` | `b` |
| x86-64 | `reg` | `l` | `al` | `b` |
| x86 | `reg_abcd` | `h` | `ah` | `h` |
| x86 | `reg` | `x` | `ax` | `w` |
| x86 | `reg` | `e` | `eax` | `k` |
| x86-64 | `reg` | `r` | `rax` | `q` |
| x86 | `reg_byte` | None | `al` / `ah` | None |
| x86 | `xmm_reg` | None | `xmm0` | `x` |
| x86 | `ymm_reg` | None | `ymm0` | `t` |
| x86 | `zmm_reg` | None | `zmm0` | `g` |
| x86 | `*mm_reg` | `x` | `xmm0` | `x` |
| x86 | `*mm_reg` | `y` | `ymm0` | `t` |
| x86 | `*mm_reg` | `z` | `zmm0` | `g` |
| x86 | `kreg` | None | `k1` | None |
| AArch64/Arm64EC | `reg` | None | `x0` | `x` |
| AArch64/Arm64EC | `reg` | `w` | `w0` | `w` |
| AArch64/Arm64EC | `reg` | `x` | `x0` | `x` |
| AArch64/Arm64EC | `vreg` | None | `v0` | None |
| AArch64/Arm64EC | `vreg` | `v` | `v0` | None |
| AArch64/Arm64EC | `vreg` | `b` | `b0` | `b` |
| AArch64/Arm64EC | `vreg` | `h` | `h0` | `h` |
| AArch64/Arm64EC | `vreg` | `s` | `s0` | `s` |
| AArch64/Arm64EC | `vreg` | `d` | `d0` | `d` |
| AArch64/Arm64EC | `vreg` | `q` | `q0` | `q` |
| ARM | `reg` | None | `r0` | None |
| ARM | `sreg` | None | `s0` | None |
| ARM | `dreg` | None | `d0` | `P` |
| ARM | `qreg` | None | `q0` | `q` |
| ARM | `qreg` | `e` / `f` | `d0` / `d1` | `e` / `f` |
| RISC-V | `reg` | None | `x1` | None |
| RISC-V | `freg` | None | `f0` | None |
| LoongArch | `reg` | None | `$r1` | None |
| LoongArch | `freg` | None | `$f0` | None |
| s390x | `reg` | None | `%r0` | None |
| s390x | `reg_addr` | None | `%r1` | None |
| s390x | `freg` | None | `%f0` | None |
| s390x | `vreg` | None | `%v0` | None |
| PowerPC/PowerPC64 | `reg` | None | `0` | None |
| PowerPC/PowerPC64 | `reg_nonzero` | None | `3` | None |
| PowerPC/PowerPC64 | `freg` | None | `0` | None |
| PowerPC/PowerPC64 | `vreg` | None | `0` | None |
| PowerPC/PowerPC64 | `vsreg` | None | `0` | None |

> **注意**
> - 在 ARM 上，`e` / `f`：这会打印 NEON 四字（128 位）寄存器的低半或高半双字寄存器名。
> - 在 x86 上：我们对不带修饰符的 `reg` 的行为与 GCC 不同。GCC 会根据操作数值类型推断修饰符，而我们默认使用完整寄存器大小。
> - 在 x86 的 `xmm_reg` 上：`x`、`t` 和 `g` LLVM 修饰符尚未在 LLVM 中实现（它们仅由 GCC 支持），但这应该是一个简单的改动。

```rust
## #[cfg(target_arch = "x86_64")] {
let mut x = 0x10u16;

// 使用 `xchg` 实现 u16::swap_bytes
// `{x}` 的低半部分通过 `{x:l}` 引用，高半部分通过 `{x:h}` 引用
unsafe { core::arch::asm!("xchg {x:l}, {x:h}", x = inout(reg_abcd) x); }
assert_eq!(x, 0x1000u16);
## }
```

r[asm.template-modifiers.smaller-value]
如上一节所述，传入小于寄存器宽度的输入值会导致寄存器高位包含未定义值。如果内联汇编只访问寄存器的低位，这不成问题，可以通过使用模板修饰符在汇编代码中使用子寄存器名来实现（例如用 `ax` 代替 `rax`）。由于这是一个容易踩的坑，编译器会根据输入类型在适当的地方建议使用模板修饰符。如果对某个操作数的所有引用都已带有修饰符，则对该操作数抑制此警告。

[llvm-argmod]: http://llvm.org/docs/LangRef.html#asm-template-argument-modifiers

r[asm.abi-clobbers]
## ABI 破坏寄存器

r[asm.abi-clobbers.intro]
`clobber_abi` 关键字可用于对汇编代码应用一组默认的破坏寄存器。这会自动插入调用具有特定调用约定的函数所需的破坏约束：如果调用约定不完全保留某个寄存器在调用前后的值，则会隐式地向操作数列表添加 `lateout("...") _`（其中 `...` 替换为该寄存器的名称）。

```rust
## #[cfg(target_arch = "x86_64")] {
extern "C" fn foo() -> i32 { 0 }

let z: i32;
// 要调用函数，我们必须告知编译器我们正在破坏被调用者保存的寄存器
unsafe { core::arch::asm!("call {}", sym foo, out("rax") z, clobber_abi("C")); }
assert_eq!(z, 0);
## }
```

r[asm.abi-clobbers.many]
`clobber_abi` 可以指定任意次数。它会为所有指定调用约定的并集中的所有唯一寄存器插入破坏约束。

```rust
## #[cfg(target_arch = "x86_64")] {
extern "sysv64" fn foo() -> i32 { 0 }
extern "win64" fn bar(x: i32) -> i32 { x + 1 }

let z: i32;
// 我们甚至可以调用具有不同约定和不同保存寄存器的多个函数
unsafe {
    core::arch::asm!(
        "call {}",
        "mov ecx, eax",
        "call {}",
        sym foo,
        sym bar,
        out("rax") z,
        clobber_abi("sysv64"),
        clobber_abi("win64"),
    );
}
assert_eq!(z, 1);
## }
```

r[asm.abi-clobbers.must-specify]
使用 `clobber_abi` 时，编译器不允许使用通用寄存器类输出：所有输出都必须指定显式寄存器。

```rust
## #[cfg(target_arch = "x86_64")] {
extern "C" fn foo(x: i32) -> i32 { 0 }

let z: i32;
// 必须使用显式寄存器，以免意外重叠。
unsafe {
    core::arch::asm!(
        "mov eax, {:e}",
        "call {}",
        out(reg) z,
        sym foo,
        clobber_abi("C")
    );
    // ERROR: asm with `clobber_abi` must specify explicit registers for outputs
}
assert_eq!(z, 0);
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.abi-clobbers.explicit-have-precedence]
显式寄存器输出优先于由 `clobber_abi` 插入的隐式破坏约束：仅当某个寄存器未被用作输出时，才会为其插入破坏约束。

r[asm.abi-clobbers.supported-abis]
以下 ABI 可与 `clobber_abi` 一起使用：

| 架构 | ABI 名称 | 被破坏的寄存器 |
| ------------ | -------- | ------------------- |
| x86-32 | `"C"`, `"system"`, `"efiapi"`, `"cdecl"`, `"stdcall"`, `"fastcall"` | `ax`, `cx`, `dx`, `xmm[0-7]`, `mm[0-7]`, `k[0-7]`, `st([0-7])` |
| x86-64 | `"C"`, `"system"` (on Windows), `"efiapi"`, `"win64"` | `ax`, `cx`, `dx`, `r[8-11]`, `xmm[0-31]`, `mm[0-7]`, `k[0-7]`, `st([0-7])`, `tmm[0-7]` |
| x86-64 | `"C"`, `"system"` (on non-Windows), `"sysv64"` | `ax`, `cx`, `dx`, `si`, `di`, `r[8-11]`, `xmm[0-31]`, `mm[0-7]`, `k[0-7]`, `st([0-7])`, `tmm[0-7]` |
| AArch64 | `"C"`, `"system"`, `"efiapi"` | `x[0-17]`, `x18`\*, `x30`, `v[0-31]`, `p[0-15]`, `ffr` |
| Arm64EC | `"C"`, `"system"` | `x[0-12]`, `x[15-17]`, `x30`, `v[0-15]` |
| ARM | `"C"`, `"system"`, `"efiapi"`, `"aapcs"` | `r[0-3]`, `r12`, `r14`, `s[0-15]`, `d[0-7]`, `d[16-31]` |
| RISC-V | `"C"`, `"system"`, `"efiapi"` | `x1`, `x[5-7]`, `x[10-17]`\*, `x[28-31]`\*, `f[0-7]`, `f[10-17]`, `f[28-31]`, `v[0-31]` |
| LoongArch | `"C"`, `"system"` | `$r1`, `$r[4-20]`, `$f[0-23]` |
| s390x | `"C"`, `"system"` | `r[0-5]`, `r14`, `f[0-7]`, `v[0-31]`, `a[2-15]` |

> **注意**
> - 在 AArch64 上，仅当 `x18` 在目标上不被视为保留寄存器时，才会将其包含在破坏列表中。
> - 在 RISC-V 上，仅当 `x[16-17]` 和 `x[28-31]` 在目标上不被视为保留寄存器时，才会将它们包含在破坏列表中。

随着各架构获得新寄存器，rustc 会更新每个 ABI 的被破坏寄存器列表：这确保当 LLVM 开始在其生成的代码中使用这些新寄存器时，`asm!` 的破坏约束仍然正确。

r[asm.options]
## 选项

r[asm.options.supported-options]
标志用于进一步影响内联汇编代码的行为。当前定义了以下选项：

r[asm.options.supported-options.pure]
- `pure`：汇编代码没有副作用，最终必须返回，并且其输出仅依赖于其直接输入（即值本身，而非它们所指向的内容）或从内存读取的值（除非同时设置了 `nomem` 选项）。这允许编译器执行汇编代码的次数少于程序中指定的次数（例如将其提升出循环），甚至在输出未被使用时完全消除它。`pure` 选项必须与 `nomem` 或 `readonly` 选项之一组合使用，否则会发出编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i32 = 0;
let z: i32;
// pure 可用于优化，假定汇编没有副作用
unsafe { core::arch::asm!("inc {}", inout(reg) x => z, options(pure, nomem)); }
assert_eq!(z, 1);
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i32 = 0;
let z: i32;
// 必须满足 nomem 或 readonly，以表明是否允许读取内存
unsafe { core::arch::asm!("inc {}", inout(reg) x => z, options(pure)); }
// ERROR: the `pure` option must be combined with either `nomem` or `readonly`
assert_eq!(z, 0);
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.options.supported-options.nomem]
- `nomem`：汇编代码不从汇编代码外部可访问的任何内存读取或写入。这允许编译器在汇编代码执行期间将已修改的全局变量的值缓存在寄存器中，因为它知道汇编代码不会读取或写入它们。编译器还假定汇编代码不与其他线程进行任何形式的同步，例如通过屏障。

<!-- no_run: This test has unpredictable or undefined behavior at runtime -->
```rust
## #[cfg(target_arch = "x86_64")] {
let mut x = 0i32;
let z: i32;
// 在指定 `nomem` 时，从汇编访问外部内存是不允许的
unsafe {
    core::arch::asm!("mov {val:e}, dword ptr [{ptr}]",
        ptr = in(reg) &mut x,
        val = lateout(reg) z,
        options(nomem)
    )
}

// 在指定 `nomem` 时，从汇编写入外部内存也是未定义行为
unsafe {
    core::arch::asm!("mov  dword ptr [{ptr}], {val:e}",
        ptr = in(reg) &mut x,
        val = in(reg) z,
        options(nomem)
    )
}
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i32 = 0;
let z: i32;
// 不过，如果我们通过 `push` 等方式自己分配内存，
// 仍然可以使用它
unsafe {
    core::arch::asm!("push {x}", "add qword ptr [rsp], 1", "pop {x}",
        x = inout(reg) x => z,
        options(nomem)
    );
}
assert_eq!(z, 1);
## }
```

r[asm.options.supported-options.readonly]
- `readonly`：汇编代码不写入汇编代码外部可访问的任何内存。这允许编译器在汇编代码执行期间将未修改的全局变量的值缓存在寄存器中，因为它知道汇编代码不会写入它们。编译器还假定此汇编代码不与其他线程进行任何形式的同步，例如通过屏障。

<!-- no_run: This test has undefined behaviour at runtime -->
```rust
## #[cfg(target_arch = "x86_64")] {
let mut x = 0;
// 在指定 `readonly` 时，我们不能修改外部内存
unsafe {
    core::arch::asm!("mov dword ptr[{}], 1", in(reg) &mut x, options(readonly))
}
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64 = 0;
let z: i64;
// 不过，我们仍然可以从中读取
unsafe {
    core::arch::asm!("mov {x}, qword ptr [{x}]",
        x = inout(reg) &x => z,
        options(readonly)
    );
}
assert_eq!(z, 0);
## }
```

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i64 = 0;
let z: i64;
// 与 nomem 适用相同的例外。
unsafe {
    core::arch::asm!("push {x}", "add qword ptr [rsp], 1", "pop {x}",
        x = inout(reg) x => z,
        options(readonly)
    );
}
assert_eq!(z, 1);
## }
```

r[asm.options.supported-options.preserves_flags]
- `preserves_flags`：汇编代码不修改标志寄存器（在下方规则中定义）。这允许编译器在执行汇编代码后避免重新计算条件标志。

r[asm.options.supported-options.noreturn]
- `noreturn`：汇编代码不会继续向下执行；如果这样做则行为未定义。它仍然可以跳转到 `label` 块。如果任何 `label` 块返回 unit，则 `asm!` 块将返回 unit。否则它将返回 `!`（never）。与调用不返回的函数一样，作用域中的局部变量在执行汇编代码之前不会被丢弃。

<!-- no_run: This test aborts at runtime -->
```rust
fn main() -> ! {
## #[cfg(target_arch = "x86_64")] {
    // 我们可以在 noreturn 块内使用指令来陷入执行
    unsafe { core::arch::asm!("ud2", options(noreturn)); }
## }
## #[cfg(not(target_arch = "x86_64"))] panic!("no return");
}
```

<!-- no_run: Test has undefined behavior at runtime -->
```rust
## #[cfg(target_arch = "x86_64")] {
// 你有责任确保不会越过 noreturn asm 块的末尾继续执行
unsafe { core::arch::asm!("", options(noreturn)); }
## }
```

```rust
## #[cfg(target_arch = "x86_64")]
let _: () = unsafe {
    // 你仍然可以跳转到 `label` 块
    core::arch::asm!("jmp {}", label {
        println!();
    }, options(noreturn));
};
```

r[asm.options.supported-options.nostack]
- `nostack`：汇编代码不向栈推送数据，也不写入栈红区（如果目标支持）。如果*不*使用此选项，则编译器保证在汇编代码开始时栈指针已按目标 ABI 适当地对齐，以便进行函数调用。

<!-- no_run: Test has undefined behavior at runtime -->
```rust
## #[cfg(target_arch = "x86_64")] {
// 与 nostack 一起使用时，`push` 和 `pop` 是 UB
unsafe { core::arch::asm!("push rax", "pop rax", options(nostack)); }
## }
```

r[asm.options.supported-options.att_syntax]
- `att_syntax`：此选项仅在 x86 上有效，会使汇编器使用 GNU 汇编器的 `.att_syntax prefix` 模式。寄存器操作数在替换时会带有前导 `%`。

```rust
## #[cfg(target_arch = "x86_64")] {
let x: i32;
let y = 1i32;
// 这里需要使用 AT&T 语法。操作数顺序为 src, dest
unsafe {
    core::arch::asm!("mov {y:e}, {x:e}",
        x = lateout(reg) x,
        y = in(reg) y,
        options(att_syntax)
    );
}
assert_eq!(x, y);
## }
```

r[asm.options.supported-options.raw]
- `raw`：这会使模板字符串被解析为原始汇编字符串，对 `{` 和 `}` 不做特殊处理。这主要在使用 `include_str!` 从外部文件包含原始汇编代码时有用。

r[asm.options.checks]
编译器会对选项执行一些额外检查：

r[asm.options.checks.mutually-exclusive]
- `nomem` 和 `readonly` 选项互斥：同时指定两者是编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
// nomem 严格强于 readonly，不能一起指定
unsafe { core::arch::asm!("", options(nomem, readonly)); }
// ERROR: the `nomem` and `readonly` options are mutually exclusive
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.options.checks.pure]
- 在没有输出或只有被丢弃的输出（`_`）的 asm 块上指定 `pure` 是编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
// pure 块至少需要一个输出
unsafe { core::arch::asm!("", options(pure)); }
// ERROR: asm with the `pure` option must have at least one output
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.options.checks.noreturn]
- 在带有输出且没有标签的 asm 块上指定 `noreturn` 是编译时错误。

```rust
## #[cfg(target_arch = "x86_64")] {
let z: i32;
// noreturn 不能有输出
unsafe { core::arch::asm!("mov {:e}, 1", out(reg) z, options(noreturn)); }
// ERROR: asm outputs are not allowed with the `noreturn` option
## }
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.options.checks.label-with-outputs]
- 在带有输出的 asm 块中包含任何 `label` 块是编译时错误。

r[asm.options.naked_asm-restriction]
`naked_asm!` 仅支持 `att_syntax` 和 `raw` 选项。其余选项没有意义，因为内联汇编定义了整个函数体。

r[asm.options.global_asm-restriction]
`global_asm!` 仅支持 `att_syntax` 和 `raw` 选项。其余选项对全局作用域的内联汇编没有意义。

```rust
## fn main() {}
## #[cfg(target_arch = "x86_64")]
// nomem 对 global_asm! 没有用处
core::arch::global_asm!("", options(nomem));
## #[cfg(not(target_arch = "x86_64"))] core::compile_error!("Test not supported on this arch");
```

r[asm.rules]
## 内联汇编的规则

r[asm.rules.intro]
为避免未定义行为，在使用函数作用域内联汇编（`asm!`）时必须遵守以下规则：

r[asm.rules.reg-not-input]
- 任何未指定为输入的寄存器，在进入汇编代码时将包含未定义值。
  - 在内联汇编语境中，「未定义值」意味着该寄存器可以（非确定性地）持有该架构所允许的任意可能值。尤其要注意，它与 LLVM 的 `undef` 不同：后者每次读取都可能得到不同的值（因为汇编代码中不存在这种概念）。

r[asm.rules.reg-not-output]
- 任何未指定为输出的寄存器，在退出汇编代码时必须与进入时具有相同的值，否则行为未定义。
  - 这仅适用于可作为输入或输出指定的寄存器。其他寄存器遵循目标相关规则。
  - 注意，`lateout` 可能被分配到与 `in` 相同的寄存器，此时本规则不适用。但代码不应依赖这一点，因为它取决于寄存器分配的结果。

r[asm.rules.unwind]
- 若执行从汇编代码中展开（unwind）出去，则行为未定义。
  - 若汇编代码调用某个随后展开的函数，同样适用。

r[asm.rules.mem-same-as-ffi]
- 汇编代码允许读取和写入的内存位置集合，与 FFI 函数所允许的相同。
  - 若设置了 `readonly` 选项，则仅允许内存读取。
  - 若设置了 `nomem` 选项，则不允许任何内存读或写。
  - 这些规则不适用于汇编代码私有的内存，例如在其中分配的栈空间。

r[asm.rules.black-box]
- 编译器不能假定汇编代码中的指令就是最终实际执行的指令。
  - 这实际上意味着编译器必须将汇编代码视为黑盒，只考虑接口规范，而不考虑指令本身。
  - 允许通过目标相关机制进行运行时代码修补。
  - 但不保证源码中的每一块汇编代码都直接对应目标文件中的单一指令实例；编译器可以自由地对 `asm!` 块中的汇编代码进行复制或去重。

r[asm.rules.stack-below-sp]
- 除非设置了 `nostack` 选项，否则汇编代码允许使用栈指针以下的栈空间。
  - 进入汇编代码时，保证栈指针已按目标 ABI 为函数调用适当地对齐。
  - 你有责任确保不会栈溢出（例如使用栈探测以确保触及保护页）。
  - 分配栈内存时应按目标 ABI 的要求调整栈指针。
  - 离开汇编代码之前，必须将栈指针恢复为其原始值。

r[asm.rules.stack-above-sp]
- 除非设置了 `nostack` 选项，否则当目标 ABI 要求在调用者栈帧中存储某些值时（例如在 PowerPC64 上保存 `lr`），汇编代码允许修改调用者的栈帧。

r[asm.rules.noreturn]
- 若设置了 `noreturn` 选项，则执行落到汇编代码末尾之后属于未定义行为。

r[asm.rules.pure]
- 若设置了 `pure` 选项，而 `asm!` 除直接输出外还有副作用，则行为未定义。若两次以相同输入执行 `asm!` 代码得到不同输出，行为也未定义。
  - 与 `nomem` 选项一起使用时，「输入」仅指 `asm!` 的直接输入。
  - 与 `readonly` 选项一起使用时，「输入」包括汇编代码的直接输入以及它被允许读取的任何内存。

r[asm.rules.preserved-registers]
- 若设置了 `preserves_flags` 选项，则退出汇编代码时必须恢复以下标志寄存器：
  - x86
    - `EFLAGS` 中的状态标志（CF、PF、AF、ZF、SF、OF）。
    - 浮点状态字（全部）。
    - `MXCSR` 中的浮点异常标志（PE、UE、OE、ZE、DE、IE）。
  - ARM
    - `CPSR` 中的条件标志（N、Z、C、V）
    - `CPSR` 中的饱和标志（Q）
    - `CPSR` 中的大于或等于标志（GE）。
    - `FPSCR` 中的条件标志（N、Z、C、V）
    - `FPSCR` 中的饱和标志（QC）
    - `FPSCR` 中的浮点异常标志（IDC、IXC、UFC、OFC、DZC、IOC）。
  - AArch64 与 Arm64EC
    - 条件标志（`NZCV` 寄存器）。
    - 浮点状态（`FPSR` 寄存器）。
  - RISC-V
    - `fcsr`（`fflags`）中的浮点异常标志。
    - 向量扩展状态（`vtype`、`vl`、`vxsat` 和 `vxrm`）。
  - LoongArch
    - `$fcc[0-7]` 中的浮点条件标志。
  - PowerPC/PowerPC64
    - `fpscr` 中的浮点状态与粘滞位（除 DRN、VE、OE、UE、ZE、XE、NI 或 RN 以外的任何字段）。
    - `vscr` 中的向量状态与粘滞位（除 NJ 以外的任何字段）。
  - PowerPC SPE
    - `spefscr` 的粘滞位与状态位（除 FINXE、FINVE、FDBZE、FUNFE、FOVFE 或 FRMC 以外的任何字段）。
  - s390x
    - 条件码寄存器 `cc`。

r[asm.rules.x86-df]
- 在 x86 上，进入汇编代码时方向标志（`EFLAGS` 中的 DF）为清除状态，退出时也必须为清除状态。
  - 若退出汇编代码时方向标志被置位，则行为未定义。

r[asm.rules.x86-x87]
- 在 x86 上，除非所有 `st([0-7])` 寄存器都已用 `out("st(0)") _, out("st(1)") _, ...` 标记为 clobber，否则 x87 浮点寄存器栈必须保持不变。
  - 若所有 x87 寄存器都被 clobber，则保证进入汇编代码时 x87 寄存器栈为空。汇编代码必须确保退出汇编代码时 x87 寄存器栈同样为空。

```rust
## #[cfg(target_arch = "x86_64")]
pub fn fadd(x: f64, y: f64) -> f64 {
  let mut out = 0f64;
  let mut top = 0u16;
  // 若 clobber 整个 x87 栈，就可以用 x87 做复杂操作
  unsafe { core::arch::asm!(
    "fld qword ptr [{x}]",
    "fld qword ptr [{y}])",
    "faddp",
    "fstp qword ptr [{out}]",
    "xor eax, eax",
    "fstsw ax",
    "shl eax, 11",
    x = in(reg) &x,
    y = in(reg) &y,
    out = in(reg) &mut out,
    out("st(0)") _, out("st(1)") _, out("st(2)") _, out("st(3)") _,
    out("st(4)") _, out("st(5)") _, out("st(6)") _, out("st(7)") _,
    out("eax") top
  );}

  assert_eq!(top & 0x7, 0);
  out
}

pub fn main() {
## #[cfg(target_arch = "x86_64")]{
  assert_eq!(fadd(1.0, 1.0), 2.0);
## }
}
```

r[asm.rules.arm64ec]
- 在 arm64ec 上，调用函数时必须使用[带有适当 thunk 的调用检查器](https://learn.microsoft.com/en-us/windows/arm/arm64ec-abi#authoring-arm64ec-in-assembly)。

r[asm.rules.only-on-exit]
- 将栈指针和非输出寄存器恢复为其原始值的要求，仅在退出汇编代码时适用。
  - 这意味着：即使未标记 `noreturn`，不会落到末尾之后、也不跳转到任何 `label` 块的汇编代码，同样不需要保留这些寄存器。
  - 当返回到与进入时不同的 `asm!` 块的汇编代码时（例如用于上下文切换），这些寄存器必须包含你正在*退出*的那个 `asm!` 块进入时的值。
    - 不能退出尚未进入的 `asm!` 块的汇编代码。也不能退出其汇编代码已经退出的 `asm!` 块（除非先再次进入）。
    - 你有责任切换任何目标相关状态（例如线程局部存储、栈边界）。
    - 即使在同一函数或块内，也不能从一个 `asm!` 块中的地址跳转到另一个 `asm!` 块中的地址，除非将其上下文视为可能不同并需要上下文切换。不能假定这些上下文中的任何特定值（例如当前栈指针，或栈指针以下的临时值）在两个 `asm!` 块之间保持不变。
    - 可以访问的内存位置集合，是进入和退出的 `asm!` 块所允许的集合之交集。

r[asm.rules.not-successive]
- 不能假定源码中相邻的两个 `asm!` 块——即便它们之间没有任何其他代码——会在二进制中位于连续地址，且中间没有任何其他指令。

r[asm.rules.not-exactly-once]
- 不能假定一个 `asm!` 块会在输出二进制中恰好出现一次。编译器可以实例化该 `asm!` 块的多个副本，例如当包含它的函数在多处被内联时。

r[asm.rules.x86-prefix-restriction]
- 在 x86 上，内联汇编不得以会作用于编译器所生成指令的指令前缀（例如 `LOCK`）结尾。
  - 由于内联汇编的编译方式，编译器目前无法检测这种情况，但将来可能会捕获并拒绝。

r[asm.rules.preserves_flags]
> **注意**
> 作为一般规则，`preserves_flags` 所涵盖的标志，是执行函数调用时*不会*被保留的那些标志。

r[asm.naked-rules]
## 裸内联汇编的规则

r[asm.naked-rules.intro]
为避免未定义行为，在裸函数中使用函数作用域内联汇编（`naked_asm!`）时必须遵守以下规则：

r[asm.naked-rules.reg-not-input]
- 根据调用约定和函数签名，任何未用作函数输入的寄存器，在进入 `naked_asm!` 块时将包含未定义值。
  - 在内联汇编语境中，「未定义值」表示该寄存器可以（非确定性地）取架构所允许的任意可能值。需要注意的是，这与 LLVM 的 `undef` 不同——后者每次读取都可能得到不同的值（因为汇编代码中不存在这种概念）。

r[asm.naked-rules.callee-saved-registers]
- 所有被调用者保存寄存器在返回时必须与进入时具有相同的值。

r[asm.naked-rules.caller-saved-registers]
- 调用者保存寄存器可以自由使用。

r[asm.naked-rules.noreturn]
- 若执行流落到汇编代码末尾之后，行为未定义。
  - 汇编代码中的每条路径都预期以返回指令结束，或发散（不返回）。

r[asm.naked-rules.mem-same-as-ffi]
- 汇编代码允许读写的内存位置集合，与 FFI 函数所允许的相同。

r[asm.naked-rules.black-box]
- 编译器不能假定 `naked_asm!` 块中的指令就是实际会执行的指令。
  - 这实际上意味着编译器必须将 `naked_asm!` 视为黑盒，只考虑接口规范，而不考虑指令本身。
  - 允许通过目标特定机制进行运行时代码修补。

r[asm.naked-rules.unwind]
- 允许从 `naked_asm!` 块向外展开（unwind）。
  - 为获得正确行为，必须使用会发出展开元数据的相应汇编器指令。

```rust
## #[cfg(target_arch = "x86_64")] {
#[unsafe(naked)]
extern "sysv64-unwind" fn unwinding_naked() {
    core::arch::naked_asm!(
        // 此处「CFI」表示「调用帧信息」（call frame information）。
        ".cfi_startproc",
        // CFA（规范帧地址，canonical frame address）是 `call` 之前
        // `rsp` 的值，即返回地址 `rip` 被压入 `rsp` 之前的值，
        // 因此它在内存中比函数入口时（`rip` 已被压入后）的 `rsp`
        // 高 8 个字节。
        //
        // 这是默认行为，所以我们不必写出它。
        //".cfi_def_cfa rsp, 8",
        //
        // 传统做法是保存基址指针，因此我们也这样做。
        "push rbp",
        // 由于我们现在已将栈在内存中向下扩展了 8 个字节，
        // 需要将从 `rsp` 到 CFA 的偏移再调整 8 个字节。
        ".cfi_adjust_cfa_offset 8",
        // 然后我们还要标注相对于 CFA 存放了调用者 `rbp` 值的位置，
        // 以便在展开回调用者时能够找到它，以防我们需要根据它
        // 计算调用者的 CFA。
        //
        // 这里，我们把调用者的 `rbp` 存放在 CFA 下方 16 字节处。
        // 也就是说，从 CFA 开始，首先是 `rip`（从 CFA 下方 8 字节
        // 开始一直到 CFA），然后是我们刚刚压入的调用者 `rbp`。
        ".cfi_offset rbp, -16",
        // 按照传统，我们将基址指针设为栈指针的值。
        // 这样，基址指针在整个函数体中保持不变。
        "mov rbp, rsp",
        // 现在可以从基址指针跟踪到 CFA 的偏移。
        // 这意味着直到结束都不必再做进一步调整，因为我们不会
        // 改变 `rbp`。
        ".cfi_def_cfa_register rbp",
        // 现在可以调用一个可能 panic 的函数。
        "call {f}",
        // 返回后，我们恢复 `rbp`，为自身返回做准备。
        "pop rbp",
        // 既然已经恢复了 `rbp`，必须再次以 `rsp` 来指定到 CFA 的偏移。
        ".cfi_def_cfa rsp, 8",
        // 现在可以返回。
        "ret",
        ".cfi_endproc",
        f = sym may_panic,
    )
}

extern "sysv64-unwind" fn may_panic() {
    panic!("unwind");
}
## }
```

> **注意**
>
> 关于上述 `cfi` 汇编器指令的更多信息，请参阅以下资源：
>
> - [Using `as` - CFI directives](https://sourceware.org/binutils/docs/as/CFI-directives.html)
> - [DWARF Debugging Information Format Version 5](https://dwarfstd.org/doc/DWARF5.pdf)
> - [ImperialViolet - CFI directives in assembly files](https://www.imperialviolet.org/2017/01/18/cfi.html)

r[asm.validity]
### 正确性与有效性

r[asm.validity.necessary-but-not-sufficient]
除前述全部规则外，传给 `asm!` 的字符串参数最终必须成为——在所有其他参数求值、格式化完成、操作数被翻译之后——对目标架构而言既语法正确又语义有效的汇编。格式化规则使编译器能够生成语法正确的汇编。关于操作数的规则允许将 Rust 操作数有效地翻译进、出汇编代码。遵守这些规则是必要的，但不足以保证最终展开的汇编既正确又有效。例如：

- 参数可能被放在格式化后语法不正确的位置
- 指令可能书写正确，但给出了架构上无效的操作数
- 架构未规定的指令可能被汇编成未指定的代码
- 一组各自正确且有效的指令，若紧挨着放置，可能引起未定义行为

r[asm.validity.non-exhaustive]
因此，这些规则是*非穷尽的*。编译器不必检查初始字符串或最终生成汇编的正确性与有效性。汇编器可以检查正确性与有效性，但并非必须如此。使用 `asm!` 时，一个笔误就足以使程序变得不健全（unsound），而汇编规则可能包含数千页的架构参考手册。程序员应给予适当注意，因为调用这一 `unsafe` 能力意味着承担不违反编译器规则与架构规则的责任。

r[asm.directives]
### 指令支持

r[asm.directives.subset-supported]
内联汇编支持 GNU AS 与 LLVM 内部汇编器共同支持的指令子集，如下所列。使用其他指令的结果是汇编器特定的（可能报错，也可能原样接受）。

r[asm.directives.stateful]
若内联汇编包含任何会改变后续汇编处理方式的「有状态」指令，则必须在内联汇编结束前撤销此类指令的效果。

r[asm.directives.supported-directives]
以下指令保证会被汇编器支持：

- `.2byte`
- `.4byte`
- `.8byte`
- `.align`
- `.alt_entry`
- `.ascii`
- `.asciz`
- `.balign`
- `.balignl`
- `.balignw`
- `.bss`
- `.byte`
- `.comm`
- `.data`
- `.def`
- `.double`
- `.endef`
- `.equ`
- `.equiv`
- `.eqv`
- `.fill`
- `.float`
- `.global`
- `.globl`
- `.inst`
- `.insn`
- `.lcomm`
- `.long`
- `.octa`
- `.option`
- `.p2align`
- `.popsection`
- `.private_extern`
- `.pushsection`
- `.quad`
- `.scl`
- `.section`
- `.set`
- `.short`
- `.size`
- `.skip`
- `.sleb128`
- `.space`
- `.string`
- `.text`
- `.type`
- `.uleb128`
- `.word`

```rust
## #[cfg(target_arch = "x86_64")] {
let bytes: *const u8;
let len: usize;
unsafe {
    core::arch::asm!(
        "jmp 3f", "2: .ascii \"Hello World!\"",
        "3: lea {bytes}, [2b+rip]",
        "mov {len}, 12",
        bytes = out(reg) bytes,
        len = out(reg) len
    );
}

let s = unsafe { core::str::from_utf8_unchecked(core::slice::from_raw_parts(bytes, len)) };

assert_eq!(s, "Hello World!");
## }
```

r[asm.target-specific-directives]
#### 目标特定指令支持

r[asm.target-specific-directives.dwarf-unwinding]
##### DWARF 展开

以下指令在支持 DWARF 展开信息的 ELF 目标上受支持：

- `.cfi_adjust_cfa_offset`
- `.cfi_def_cfa`
- `.cfi_def_cfa_offset`
- `.cfi_def_cfa_register`
- `.cfi_endproc`
- `.cfi_escape`
- `.cfi_lsda`
- `.cfi_offset`
- `.cfi_personality`
- `.cfi_register`
- `.cfi_rel_offset`
- `.cfi_remember_state`
- `.cfi_restore`
- `.cfi_restore_state`
- `.cfi_return_column`
- `.cfi_same_value`
- `.cfi_sections`
- `.cfi_signal_frame`
- `.cfi_startproc`
- `.cfi_undefined`
- `.cfi_window_save`

r[asm.target-specific-directives.structured-exception-handling]
##### 结构化异常处理

在具有结构化异常处理的目标上，保证额外支持以下指令：

- `.seh_endproc`
- `.seh_endprologue`
- `.seh_proc`
- `.seh_pushreg`
- `.seh_savereg`
- `.seh_setframe`
- `.seh_stackalloc`

r[asm.target-specific-directives.x86]
##### x86（32 位与 64 位）

在 32 位与 64 位 x86 目标上，保证额外支持以下指令：
- `.nops`
- `.code16`
- `.code32`
- `.code64`

仅当在退出汇编代码前将状态重置为默认值时，才支持使用 `.code16`、`.code32` 和 `.code64` 指令。32 位 x86 默认使用 `.code32`，x86_64 默认使用 `.code64`。

r[asm.target-specific-directives.arm-32-bit]
##### ARM（32 位）

在 ARM 上，保证额外支持以下指令：

- `.even`
- `.fnstart`
- `.fnend`
- `.save`
- `.movsp`
- `.code`
- `.thumb`
- `.thumb_func`
