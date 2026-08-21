+++
title = "第19章 应用二进制接口"
date = 2026-08-18T08:45:00+08:00
weight = 113
type = "docs"
description = "应用二进制接口 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/abi.html](https://doc.rust-lang.org/reference/abi.html)

r[abi]
# 应用二进制接口

r[abi.intro]
本节记录影响 crate 编译输出 ABI 的特性。

关于为导出函数指定 ABI 的信息，见 *[extern 函数][extern functions]*。关于为链接外部库指定 ABI 的信息，见 *[外部块][external blocks]*。

<!-- template:attributes -->
r[abi.used]
## `used` 属性

r[abi.used.intro]
*`used` [属性][attribute]* 强制将 [static] 保留在输出目标文件（.o、.rlib 等，不包括最终二进制文件）中，即便 crate 中没有任何其他项使用或引用它。不过，链接器仍可将其移除。

> [!EXAMPLE]
> ```rust
> // lib.rs
>
> // 因 `#[used]` 而被保留。
> #[used]
> static S1: u8 = 0;
>
> // 因未使用而可移除。
> #[allow(dead_code)]
> static S2: u8 = 0;
>
> // 因可公开到达而被保留。
> pub static S3: u8 = 0;
>
> // 因被可公开到达的函数引用而被保留。
> static S4: u8 = 0;
> #[unsafe(no_mangle)] pub fn f4() -> &'static u8 { &S4 }
>
> // 因仅被私有、未使用（死）函数引用而可移除。
> static S5: u8 = 0;
> #[allow(dead_code)]
> fn f5() -> &'static u8 { &S5 }
> ```
>
> ```console
> $ rustc -O --emit=obj --crate-type=rlib lib.rs
> $ LC_ALL=C nm -C lib.o
> 0000000000000000 R lib::S1
> 0000000000000000 R lib::S3
> 0000000000000000 r lib::S4
> 0000000000000000 T f4
> ```

r[abi.used.syntax]
`used` 属性使用 [MetaWord] 语法。

r[abi.used.allowed-positions]
`used` 属性只能应用于 [`static` 项][`static` items]。

r[abi.used.duplicates]
同一项上只有第一次使用 `used` 有效果。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。

r[abi.no_mangle]
## `no_mangle` 属性

r[abi.no_mangle.intro]
*`no_mangle` [属性][attribute]* 禁用 [函数][function] 或 [static] 上的标准符号名修饰（mangling）。该项的符号即为其标识符。

> [!EXAMPLE]
> ```rust
> #[unsafe(no_mangle)]
> extern "C" fn foo() {}
> ```

r[abi.no_mangle.syntax]
`no_mangle` 属性使用 [MetaWord] 语法。

r[abi.no_mangle.allowed-positions]
`no_mangle` 属性只能应用于：

- [静态项][items.static]
- [自由函数][items.fn]
- [固有关联函数][items.associated.fn]
- [Trait impl 函数][items.impl.trait]

> **注意**
> `rustc` 会对其他位置的使用发出 lint。将来这可能变为错误。

<!-- TODO: Currently it works on a trait function with a body, but generates a warning about being phased out. how do we document that?
https://github.com/rust-lang/rust/pull/86492#issuecomment-885682960
-->

<!-- TODO: should this clarify that external block items are already unmangled?, and thus the attribute does nothing? Currently it is "phased out" warning. -->

r[abi.no_mangle.closures]
`no_mangle` 属性不得与[闭包][closure]一起使用。

r[abi.no_mangle.generics]
`no_mangle` 属性不得用于带有泛型参数的项。

r[abi.no_mangle.duplicates]
同一项上只有第一次使用 `no_mangle` 有效果。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。

r[abi.no_mangle.export_name]
当 `no_mangle` 与 [`export_name`][abi.export_name] 属性同时应用于同一项时，使用 `export_name` 的符号名，而 `no_mangle` 无效果。

> **注意**
> `rustc` 会对这种组合发出 lint。

r[abi.no_mangle.unsafe]
`no_mangle` 属性必须标以 [`unsafe`][attributes.safety]，因为未修饰的符号可能与同名的另一符号（或与知名符号）冲突，从而导致未定义行为。

r[abi.no_mangle.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，允许在不带 `unsafe` 的情况下使用 `no_mangle` 属性。

r[abi.no_mangle.publicly-exported]
除禁用名称修饰外，`no_mangle` 属性还会使符号从所生成的库或目标文件中公开导出，类似于 [`used`][abi.used] 属性。

r[abi.no_mangle.ascii-only]
`no_mangle` 属性只能用于名称仅包含 ASCII 字符的项。

r[abi.link_section]
## `link_section` 属性

r[abi.link_section.intro]
*`link_section` 属性* 指定 [函数][function] 或 [static] 的内容将被放入目标文件的哪个节区。

r[abi.link_section.syntax]
`link_section` 属性使用 [MetaNameValueStr] 语法来指定节区名称。

<!-- no_run: don't link. The format of the section name is platform-specific. -->
```rust
## #[cfg(target_os = "linux")] {
#[unsafe(no_mangle)]
#[unsafe(link_section = ".example_section")]
pub static VAR1: u32 = 1;
## }
```

r[abi.link_section.unsafe]
此属性是不安全的，因为它允许用户将数据与代码放入不期望它们存在的内存节区，例如将可变数据放入只读区域。

r[abi.link_section.duplicates]
同一项上只有第一次使用 `link_section` 有效果。

> **注意**
> `rustc` 会对第一次之后的任何使用以未来兼容性警告发出 lint。将来这可能变为错误。

r[abi.link_section.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，允许在不带 `unsafe` 限定的情况下使用 `link_section` 属性。

r[abi.export_name]
## `export_name` 属性

r[abi.export_name.intro]
*`export_name` 属性* 指定将为 [函数][function] 或 [static] 导出的符号名称。

r[abi.export_name.syntax]
`export_name` 属性使用 [MetaNameValueStr] 语法来指定符号名称。

```rust
#[unsafe(export_name = "exported_symbol_name")]
pub fn name_in_rust() { }
```

r[abi.export_name.unsafe]
此属性是不安全的，因为具有自定义名称的符号可能与同名的另一符号（或与知名符号）冲突，从而导致未定义行为。

r[abi.export_name.duplicates]
同一项上只有第一次使用 `export_name` 有效果。

> **注意**
> `rustc` 会对第一次之后的任何使用以未来兼容性警告发出 lint。将来这可能变为错误。

r[abi.export_name.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，允许在不带 `unsafe` 限定的情况下使用 `export_name` 属性。

[attribute]: attributes.md
[closure]: expr.closure
[extern functions]: items/functions.md#extern-function-qualifier
[external blocks]: items/external-blocks.md
[function]: items/functions.md
[item]: items.md
[`static` items]: items.static
[static]: items/static-items.md
