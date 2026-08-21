+++
title = "13-外部块"
date = 2026-08-18T08:45:00+08:00
weight = 30
type = "docs"
description = "外部块 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/external-blocks.html](https://doc.rust-lang.org/reference/items/external-blocks.html)

r[items.extern]
# 外部块

r[items.extern.syntax]
```grammar,items
ExternBlock ->
    `unsafe`?[^unsafe-2024] `extern` Abi? `{`
        InnerAttribute*
        ExternalItem*
    `}`

ExternalItem ->
    OuterAttribute* (
        MacroInvocationSemi
      | Visibility? StaticItem
      | Visibility? Function
    )
```

[^unsafe-2024]: 从 2024 Edition 开始，语义上要求使用 `unsafe` 关键字。

r[items.extern.intro]
外部块提供当前 crate 中未*定义*的项的*声明*，是 Rust 外部函数接口的基础。它们类似于未经检查的导入。

r[items.extern.allowed-kinds]
外部块中允许两种项*声明*：[函数][functions]和[静态项][statics]。

r[items.extern.safety]
调用外部块中声明的不安全函数或访问其中声明的不安全静态项，只允许在 [`unsafe` 上下文][`unsafe` context]中进行。

r[items.extern.namespace]
外部块在其所在模块或块的[值命名空间][value namespace]中定义其函数和静态项。

r[items.extern.unsafe-required]
在语义上，外部块要求 `unsafe` 关键字出现在 `extern` 关键字之前。

r[items.extern.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，`unsafe` 关键字是可选的。只有当外部块本身被标记为 `unsafe` 时，才允许使用 `safe` 和 `unsafe` 项限定符。

r[items.extern.fn]
## 函数

r[items.extern.fn.body]
外部块中的函数以与其他 Rust 函数相同的方式声明，例外是它们不得有函数体，而是以分号结束。

r[items.extern.fn.param-patterns]
参数中不允许模式，只能使用 [IDENTIFIER] 或 `_`。

r[items.extern.fn.qualifiers]
允许 `safe` 和 `unsafe` 函数限定符，但不允许其他函数限定符（例如 `const`、`async`、`extern`）。`safe` 限定符在 `extern "custom"` 块中会被拒绝。

r[items.extern.fn.foreign-abi]
外部块中的函数可以由 Rust 代码调用，就像在 Rust 中定义的函数一样。Rust 编译器会自动在 Rust ABI 与外部 ABI 之间转换。

r[items.extern.fn.safety]
在 extern 块中声明的函数隐式为 `unsafe`，除非存在 `safe` 函数限定符。

r[items.extern.fn.fn-ptr]
当被强制转换为函数指针时，在 extern 块中声明的函数具有类型 `for<'l1, ..., 'lm> extern "abi" fn(A1, ..., An) -> R`，其中 `'l1`、... `'lm` 是其生命周期参数，`A1`、...、`An` 是其参数的声明类型，`R` 是声明的返回类型。

r[items.extern.static]
## 静态项

r[items.extern.static.intro]
外部块中的静态项以与外部块外的[静态项][statics]相同的方式声明，只不过它们没有初始化其值的表达式。

r[items.extern.static.safety]
除非在 extern 块中声明的静态项被限定为 `safe`，否则访问该项是 `unsafe` 的，无论它是否可变，因为没有任何保证该静态项内存中的位模式对其所声明的类型是合法的——负责初始化该静态项的是某些任意（例如 C）代码。

r[items.extern.static.mut]
Extern 静态项可以像外部块外的[静态项][statics]一样是不可变或可变的。

r[items.extern.static.read-only]
不可变静态项*必须*在任何 Rust 代码执行之前完成初始化。仅在 Rust 代码读取它之前初始化是不够的。一旦 Rust 代码运行，变更不可变静态项（无论来自 Rust 内部还是外部）都是 UB，除非变更发生在 `UnsafeCell` 内部的字节上。

r[items.extern.abi]
## ABI

r[items.extern.abi.intro]
`extern` 关键字后面可以跟可选的 [ABI] 字符串。ABI 指定块中函数的调用约定。调用约定定义函数的底层接口，例如实参如何放入寄存器或栈上、返回值如何传递，以及由谁负责清理栈。

> [!EXAMPLE]
> ```rust
> // 到 Windows API 的接口。
> unsafe extern "system" { /* ... */ }
> ```

r[items.extern.abi.default]
若未指定 ABI 字符串，则默认为 `"C"`。

> **注意**
> 没有显式 ABI 的 `extern` 语法正在被逐步淘汰，因此最好始终显式写出 ABI。
>
> 更多细节参见 [Rust issue #134986](https://github.com/rust-lang/rust/issues/134986)。

r[items.extern.abi.standard]
以下 ABI 字符串在所有平台上都受支持：

r[items.extern.abi.rust]
* `unsafe extern "Rust"` —— Rust 函数和闭包的原生调用约定。这是声明函数时不使用 [`extern fn`] 的默认值。Rust ABI 不提供稳定性保证。

r[items.extern.abi.c]
* `unsafe extern "C"` —— `"C"` ABI 匹配目标上占主导地位的 C 编译器所选择的默认 ABI。

r[items.extern.abi.system]
* `unsafe extern "system"` —— 这等价于 `extern "C"`，但在 Windows x86_32 上，对非可变参数函数等价于 `"stdcall"`，对可变参数函数等价于 `"C"`。

  > [!NOTE]
  > 由于 Windows 上正确的底层 ABI 是目标相关的，在尝试链接未使用显式定义 ABI 的 Windows API 函数时，最好使用 `extern "system"`。

r[items.extern.abi.unwind]
* `extern "C-unwind"` 和 `extern "system-unwind"` —— 分别与 `"C"` 和 `"system"` 相同，但当被调用者展开（通过 panic 或抛出 C++ 风格异常）时具有[不同的行为][unwind-behavior]。

r[items.extern.abi.custom]
* `unsafe extern "custom"` —— 编译器未知的自定义 ABI。

r[items.extern.abi.platform]
还有一些平台特定的 ABI 字符串：

r[items.extern.abi.cdecl]
* `unsafe extern "cdecl"` —— 通常用于 x86_32 C 代码的调用约定。
  * 仅在 x86_32 目标上可用。
  * 对应于 MSVC 的 `__cdecl` 以及 GCC 和 clang 的 `__attribute__((cdecl))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://learn.microsoft.com/en-us/cpp/cpp/cdecl>
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#cdecl>

r[items.extern.abi.stdcall]
* `unsafe extern "stdcall"` —— 通常由 x86_32 上的 [Win32 API] 使用的调用约定。
  * 仅在 x86_32 目标上可用。
  * 对应于 MSVC 的 `__stdcall` 以及 GCC 和 clang 的 `__attribute__((stdcall))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://learn.microsoft.com/en-us/cpp/cpp/stdcall>
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#stdcall>

r[items.extern.abi.win64]
* `unsafe extern "win64"` —— Windows x64 ABI。
  * 仅在 x86_64 目标上可用。
  * 在 Windows x86_64 目标上，"win64" 与 "C" ABI 相同。
  * 对应于 GCC 和 clang 的 `__attribute__((ms_abi))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions>
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#Microsoft_x64_calling_convention>

r[items.extern.abi.sysv64]
* `unsafe extern "sysv64"` —— System V ABI。
  * 仅在 x86_64 目标上可用。
  * 在非 Windows 的 x86_64 目标上，"sysv64" 与 "C" ABI 相同。
  * 对应于 GCC 和 clang 的 `__attribute__((sysv_abi))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://wiki.osdev.org/System_V_ABI>
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#System_V_AMD64_ABI>

r[items.extern.abi.aapcs]
* `unsafe extern "aapcs"` —— ARM 的软浮点 ABI。
  * 仅在 ARM32 目标上可用。
  * 在软浮点 ARM32 上，"aapcs" 与 "C" ABI 相同。
  * 对应于 clang 的 `__attribute__((pcs("aapcs")))`。

  > [!NOTE]
  > 细节参见：
  >
  > - [Arm Procedure Call Standard](https://developer.arm.com/documentation/107656/0101/Getting-started-with-Armv8-M-based-systems/Procedure-Call-Standard-for-Arm-Architecture--AAPCS-)

r[items.extern.abi.fastcall]
* `unsafe extern "fastcall"` —— 在寄存器中传递某些实参的 stdcall 的“快速”变体。
  * 仅在 x86_32 目标上可用。
  * 对应于 MSVC 的 `__fastcall` 以及 GCC 和 clang 的 `__attribute__((fastcall))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://learn.microsoft.com/en-us/cpp/cpp/fastcall>
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#Microsoft_fastcall>

r[items.extern.abi.thiscall]
* `unsafe extern "thiscall"` —— 通常用于 x86_32 MSVC 上 C++ 类成员函数的调用约定。
  * 仅在 x86_32 目标上可用。
  * 对应于 MSVC 的 `__thiscall` 以及 GCC 和 clang 的 `__attribute__((thiscall))`。

  > [!NOTE]
  > 细节参见：
  >
  > - <https://en.wikipedia.org/wiki/X86_calling_conventions#thiscall>
  > - <https://learn.microsoft.com/en-us/cpp/cpp/thiscall>

r[items.extern.abi.efiapi]
* `unsafe extern "efiapi"` —— 用于 [UEFI] 函数的 ABI。
  * 仅在 x86 和 ARM 目标上可用（32 位和 64 位）。

r[items.extern.abi.platform-unwind-variants]
与 `"C"` 和 `"system"` 一样，大多数平台特定的 ABI 字符串也有[对应的 `-unwind` 变体][unwind-behavior]；具体是：

* `"aapcs-unwind"`
* `"cdecl-unwind"`
* `"fastcall-unwind"`
* `"stdcall-unwind"`
* `"sysv64-unwind"`
* `"thiscall-unwind"`
* `"win64-unwind"`

r[items.extern.variadic]
## 可变参数函数

可以通过将 `...` 指定为最后一个参数，使外部块中的函数成为可变参数函数。可变参数可以用模式指定。

```rust
unsafe extern "C" {
    unsafe fn foo(...);
    unsafe fn bar(x: i32, ...);
    unsafe fn with_name(format: *const u8, args: ...);
    // 安全性：此函数保证不会访问
    // 可变参数。
    safe fn ignores_variadic_arguments(x: i32, ...);
}
```

> **警告**
> 除非 `extern` 块中的函数保证完全不会访问可变参数，否则不应对其使用 `safe` 限定符。向可变参数函数传入意外数量的实参或意外类型的实参可能导致[未定义行为][undefined]。

r[items.extern.variadic.conventions]
可变参数只能在具有下列 ABI 字符串或其对应 [`-unwind` 变体][items.fn.extern.unwind]的 `extern` 块中指定：

- `"aapcs"`
- `"C"`
- `"cdecl"`
- `"efiapi"`
- `"system"`
- `"sysv64"`
- `"win64"`

r[items.extern.attributes]
## 外部块上的属性

r[items.extern.attributes.intro]
下列[属性][attributes]控制外部块的行为。

r[items.extern.attributes.link]
### `link` 属性

r[items.extern.attributes.link.intro]
*`link` 属性*指定编译器应为 `extern` 块中的项与之链接的原生库的名称。

r[items.extern.attributes.link.syntax]
它使用 [MetaListNameValueStr] 语法指定其输入。`name` 键是要链接的原生库的名称。`kind` 键是可选值，指定库的种类，可能的取值如下：

r[items.extern.attributes.link.dylib]
- `dylib` —— 表示动态库。若未指定 `kind`，这是默认值。

r[items.extern.attributes.link.static]
- `static` —— 表示静态库。

r[items.extern.attributes.link.framework]
- `framework` —— 表示 macOS framework。仅对 macOS 目标合法。

r[items.extern.attributes.link.raw-dylib]
- `raw-dylib` —— 表示动态库，编译器将生成导入库以与之链接（细节参见下方的 [`dylib` 与 `raw-dylib`][`dylib` versus `raw-dylib`]）。仅对 Windows 目标合法。

r[items.extern.attributes.link.name-requirement]
若指定了 `kind`，则必须包含 `name` 键。

r[items.extern.attributes.link.modifiers]
可选的 `modifiers` 实参是为要链接的库指定链接修饰符的方式。

r[items.extern.attributes.link.modifiers.syntax]
修饰符指定为逗号分隔的字符串，每个修饰符以 `+` 或 `-` 为前缀，分别表示启用或禁用该修饰符。

r[items.extern.attributes.link.modifiers.multiple]
目前不支持在单个 `link` 属性中指定多个 `modifiers` 实参，或在同一 `modifiers` 实参中指定多个相同的修饰符。例如：`#[link(name = "mylib", kind = "static", modifiers = "+whole-archive")]`。

r[items.extern.attributes.link.wasm_import_module]
`wasm_import_module` 键可用于在从宿主环境导入符号时，指定 `extern` 块中项的 [WebAssembly 模块][WebAssembly module]名。若未指定 `wasm_import_module`，默认模块名是 `env`。

<!-- ignore: requires extern linking -->
```rust
#[link(name = "crypto")]
unsafe extern {
    // …
}

#[link(name = "CoreFoundation", kind = "framework")]
unsafe extern {
    // …
}

#[link(wasm_import_module = "foo")]
unsafe extern {
    // …
}
```

r[items.extern.attributes.link.empty-block]
在空的 extern 块上添加 `link` 属性是合法的。你可以用它来满足代码中其他地方（包括上游 crate）的 extern 块的链接需求，而不必把该属性添加到每个 extern 块上。

r[items.extern.attributes.link.modifiers.bundle]
#### 链接修饰符：`bundle`

r[items.extern.attributes.link.modifiers.bundle.allowed-kinds]
此修饰符只与 `static` 链接种类兼容。使用任何其他种类都会导致编译器错误。

r[items.extern.attributes.link.modifiers.bundle.behavior]
构建 rlib 或 staticlib 时，`+bundle` 表示原生静态库会被打包进 rlib 或 staticlib 归档，然后在链接最终二进制时从中取出。

r[items.extern.attributes.link.modifiers.bundle.behavior-negative]
构建 rlib 时，`-bundle` 表示原生静态库“按名称”注册为该 rlib 的依赖，其目标文件仅在链接最终二进制时包含，按该名称进行的文件搜索也在最终链接时执行。构建 staticlib 时，`-bundle` 表示原生静态库根本不包含进归档，更高层的构建系统需要稍后在链接最终二进制时添加它。

r[items.extern.attributes.link.modifiers.bundle.no-effect]
构建可执行文件或动态库等其他目标时，此修饰符没有效果。

r[items.extern.attributes.link.modifiers.bundle.default]
此修饰符的默认值是 `+bundle`。

关于此修饰符的更多实现细节，参见 rustc 的 [`bundle` 文档][`bundle` documentation for rustc]。

r[items.extern.attributes.link.modifiers.whole-archive]
#### 链接修饰符：`whole-archive`

r[items.extern.attributes.link.modifiers.whole-archive.allowed-kinds]
此修饰符只与 `static` 链接种类兼容。使用任何其他种类都会导致编译器错误。

r[items.extern.attributes.link.modifiers.whole-archive.behavior]
`+whole-archive` 表示静态库作为完整归档链接，不会丢弃任何目标文件。

r[items.extern.attributes.link.modifiers.whole-archive.default]
此修饰符的默认值是 `-whole-archive`。

关于此修饰符的更多实现细节，参见 rustc 的 [`whole-archive` 文档][`whole-archive` documentation for rustc]。

r[items.extern.attributes.link.modifiers.verbatim]
### 链接修饰符：`verbatim`

r[items.extern.attributes.link.modifiers.verbatim.allowed-kinds]
此修饰符与所有链接种类兼容。

r[items.extern.attributes.link.modifiers.verbatim.behavior]
`+verbatim` 表示 rustc 自身不会向库名添加任何目标指定的库前缀或后缀（如 `lib` 或 `.a`），并会尽力向链接器请求同样的东西。

r[items.extern.attributes.link.modifiers.verbatim.behavior-negative]
`-verbatim` 表示 rustc 会在将库名传给链接器之前添加目标特定的前缀和后缀，或者不会阻止链接器隐式添加它们。

r[items.extern.attributes.link.modifiers.verbatim.default]
此修饰符的默认值是 `-verbatim`。

关于此修饰符的更多实现细节，参见 rustc 的 [`verbatim` 文档][`verbatim` documentation for rustc]。

r[items.extern.attributes.link.kind-raw-dylib]
#### `dylib` 与 `raw-dylib`

r[items.extern.attributes.link.kind-raw-dylib.intro]
在 Windows 上，链接动态库需要向链接器提供导入库：这是一种特殊的静态库，它以链接器知道这些符号必须在运行时动态加载的方式声明该动态库导出的所有符号。

r[items.extern.attributes.link.kind-raw-dylib.import]
指定 `kind = "dylib"` 指示 Rust 编译器根据 `name` 键链接导入库。链接器随后会使用其正常的库解析逻辑查找该导入库。或者，指定 `kind = "raw-dylib"` 指示编译器在编译期间生成导入库并将其提供给链接器。

r[items.extern.attributes.link.kind-raw-dylib.platform-specific]
`raw-dylib` 仅在 Windows 上受支持。在面向其他平台时使用它会导致编译器错误。

r[items.extern.attributes.link.import_name_type]
#### `import_name_type` 键

r[items.extern.attributes.link.import_name_type.intro]
在 x86 Windows 上，函数名会被“修饰”（即添加特定前缀和/或后缀）以指示其调用约定。例如，名为 `fn1`、没有实参的 `stdcall` 调用约定函数会被修饰为 `_fn1@0`。不过，[PE 格式][PE Format]也允许名称没有前缀或未经修饰。此外，MSVC 和 GNU 工具链对同一调用约定使用不同的修饰，这意味着默认情况下，某些 Win32 函数无法通过 GNU 工具链使用 `raw-dylib` 链接种类来调用。

r[items.extern.attributes.link.import_name_type.values]
为允许这些差异，在使用 `raw-dylib` 链接种类时，还可以用下列值之一指定 `import_name_type` 键，以更改生成的导入库中函数的命名方式：

* `decorated`：函数名将使用 MSVC 工具链格式完全修饰。
* `noprefix`：函数名将使用 MSVC 工具链格式修饰，但跳过前导的 `?`、`@` 或可选的 `_`。
* `undecorated`：函数名不会被修饰。

r[items.extern.attributes.link.import_name_type.default]
若未指定 `import_name_type` 键，则函数名将使用目标工具链的格式完全修饰。

r[items.extern.attributes.link.import_name_type.variables]
变量永远不会被修饰，因此 `import_name_type` 键对它们在生成的导入库中的命名没有影响。

r[items.extern.attributes.link.import_name_type.platform-specific]
`import_name_type` 键仅在 x86 Windows 上受支持。在面向其他平台时使用它会导致编译器错误。

<!-- template:attributes -->
r[items.extern.attributes.link_name]
### `link_name` 属性

r[items.extern.attributes.link_name.intro]
*`link_name` [属性][attributes]*可以应用于 `extern` 块内的声明，以指定给定函数或静态项要导入的符号。

> [!EXAMPLE]
> ```rust
> unsafe extern "C" {
>     #[link_name = "actual_symbol_name"]
>     safe fn name_in_rust();
> }
> ```

r[items.extern.attributes.link_name.syntax]
`link_name` 属性使用 [MetaNameValueStr] 语法。

r[items.extern.attributes.link_name.invalid-names]
符号名不得为空字符串，也不得包含任何 `U+0000`（NUL）字节。

r[items.extern.attributes.link_name.allowed-positions]
`link_name` 属性只能应用于 `extern` 块中的函数或静态项。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变为错误。

r[items.extern.attributes.link_name.duplicates]
只有第一次在项上使用 `link_name` 会生效。

> **注意**
> `rustc` 会对第一次之后的任何使用发出面向未来兼容性的警告。将来这可能变为错误。

r[items.extern.attributes.link_name.link_ordinal]
`link_name` 属性不能与 [`link_ordinal`] 属性一起使用。

r[items.extern.attributes.link_ordinal]
### `link_ordinal` 属性

r[items.extern.attributes.link_ordinal.intro]
*`link_ordinal` 属性*可以应用于 `extern` 块内的声明，以指示生成用于链接的导入库时所使用的数字序数。序数是 Windows 上动态库导出的每个符号的唯一编号，可以在加载库时用来查找该符号，而不必按名称查找。

> **警告**
> `link_ordinal` 只应在已知符号序数稳定的情况下使用：若包含该符号的二进制文件在构建时未显式设置序数，则会自动为其分配一个，且该分配的序数可能在该二进制文件的不同构建之间变化。

```rust
## #[cfg(all(windows, target_arch = "x86"))]
#[link(name = "exporter", kind = "raw-dylib")]
unsafe extern "stdcall" {
    #[link_ordinal(15)]
    safe fn imported_function_stdcall(i: i32);
}
```

r[items.extern.attributes.link_ordinal.allowed-kinds]
此属性仅与 `raw-dylib` 链接种类一起使用。使用任何其他种类都会导致编译器错误。

r[items.extern.attributes.link_ordinal.exclusive]
将此属性与 `link_name` 属性一起使用会导致编译器错误。

r[items.extern.attributes.fn-parameters]
### 函数参数上的属性

外部函数参数上的属性遵循与[普通函数参数][regular function parameters]相同的规则和限制。

[ABI]: glossary.abi
[PE Format]: https://learn.microsoft.com/windows/win32/debug/pe-format#import-name-type
[UEFI]: https://uefi.org/specifications
[WebAssembly module]: https://webassembly.github.io/spec/core/syntax/modules.html
[`bundle` documentation for rustc]: ../../rustc/command-line-arguments.html#linking-modifiers-bundle
[`dylib` versus `raw-dylib`]: #dylib-versus-raw-dylib
[`extern fn`]: items.fn.extern
[`unsafe` context]: ../unsafe-keyword.md
[`verbatim` documentation for rustc]: ../../rustc/command-line-arguments.html#linking-modifiers-verbatim
[`whole-archive` documentation for rustc]: ../../rustc/command-line-arguments.html#linking-modifiers-whole-archive
[attributes]: ../attributes.md
[functions]: functions.md
[regular function parameters]: functions.md#attributes-on-function-parameters
[statics]: static-items.md
[unwind-behavior]: functions.md#unwinding
[value namespace]: ../names/namespaces.md
[win32 api]: https://learn.microsoft.com/en-us/windows/win32/api/
[`link_ordinal`]: items.extern.attributes.link_ordinal
