+++
title = "第5章 条件编译"
date = 2026-08-18T08:45:00+08:00
weight = 16
type = "docs"
description = "条件编译 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/conditional-compilation.html](https://doc.rust-lang.org/reference/conditional-compilation.html)

r[cfg]
# 条件编译

r[cfg.syntax]
```grammar,configuration
ConfigurationPredicate ->
      ConfigurationOption
    | ConfigurationAll
    | ConfigurationAny
    | ConfigurationNot
    | `true`
    | `false`

ConfigurationOption ->
    IDENTIFIER ( `=` ( STRING_LITERAL | RAW_STRING_LITERAL ) )?

ConfigurationAll ->
    `all` `(` ConfigurationPredicateList? `)`

ConfigurationAny ->
    `any` `(` ConfigurationPredicateList? `)`

ConfigurationNot ->
    `not` `(` ConfigurationPredicate `)`

ConfigurationPredicateList ->
    ConfigurationPredicate (`,` ConfigurationPredicate)* `,`?
```

r[cfg.intro]
*条件编译的源代码* 是仅在特定条件下才被编译的源代码。

r[cfg.attributes-macro]
源代码可以使用 [`cfg`] 和 [`cfg_attr`] [属性][attributes] 以及内置的 [`cfg!`] 和 [`cfg_select!`] [宏][macros] 进行条件编译。

r[cfg.conditional]
是否编译可以取决于所编译 crate 的目标架构、传给编译器的任意值，以及下文进一步描述的其他事项。

r[cfg.predicate]
每种形式的条件编译都接受一个求值为 true 或 false 的 *配置谓词*。谓词是下列之一：

r[cfg.predicate.option]
* 配置选项。若该选项已设置则谓词为 true，若未设置则为 false。

r[cfg.predicate.all]
* 带逗号分隔的配置谓词列表的 `all()`。若所有给定谓词都为 true，或列表为空，则为 true。

r[cfg.predicate.any]
* 带逗号分隔的配置谓词列表的 `any()`。若至少一个给定谓词为 true，则为 true。若没有谓词，则为 false。

r[cfg.predicate.not]
* 带一个配置谓词的 `not()`。若其谓词为 false 则为 true，若其谓词为 true 则为 false。

r[cfg.predicate.literal]
* `true` 或 `false` 字面量，分别总是 true 或 false。

r[cfg.option-spec]
*配置选项* 要么是名称，要么是键值对，并且要么已设置，要么未设置。

r[cfg.option-name]
名称写为单个标识符，例如 `unix`。

r[cfg.option-key-value]
键值对写为标识符、`=`、然后是字符串，例如 `target_arch = "x86_64"`。

> **注意**
> `=` 周围的空白被忽略，因此 `foo="bar"` 和 `foo = "bar"` 是等价的。

r[cfg.option-key-uniqueness]
键不需要唯一。例如，`feature = "std"` 和 `feature = "serde"` 可以同时设置。

r[cfg.options.set]
## 已设置的配置选项

r[cfg.options.intro]
哪些配置选项被设置，在编译 crate 期间静态确定。

r[cfg.options.target]
一些选项是根据关于编译的数据 *由编译器设置* 的。

r[cfg.options.other]
其他选项是根据代码之外传给编译器的输入 *任意设置* 的。

r[cfg.options.crate]
不可能从正在编译的 crate 的源代码内部设置配置选项。

> **注意**
> 对 `rustc` 而言，任意设置的配置选项使用 [`--cfg`] 标志设置。指定目标的配置值可用 `rustc --print cfg --target $TARGET` 显示。

> **注意**
> 键为 `feature` 的配置选项是 [Cargo][cargo-feature] 用于指定编译期选项和可选依赖的惯例。

r[cfg.target_arch]
### `target_arch`

r[cfg.target_arch.def]
键值选项，针对目标的 CPU 架构设置一次。该值类似于平台目标三元组的第一个元素，但不相同。

r[cfg.target_arch.values]
示例值：

* `"x86"`
* `"x86_64"`
* `"mips"`
* `"powerpc"`
* `"powerpc64"`
* `"arm"`
* `"aarch64"`

r[cfg.target_feature]
### `target_feature`

r[cfg.target_feature.def]
键值选项，为当前编译目标可用的每个平台特性设置。

r[cfg.target_feature.values]
示例值：

* `"avx"`
* `"avx2"`
* `"crt-static"`
* `"rdrand"`
* `"sse"`
* `"sse2"`
* `"sse4.1"`

可用特性的更多细节见 [`target_feature` 属性][`target_feature` attribute]。

r[cfg.target_feature.crt_static]
`target_feature` 选项还有一个额外的 `crt-static` 特性，用于表明 [静态 C 运行时][static C runtime] 可用。

r[cfg.target_os]
### `target_os`

r[cfg.target_os.def]
键值选项，针对目标的操作系统设置一次。该值类似于平台目标三元组的第二个和第三个元素。

r[cfg.target_os.values]
示例值：

* `"windows"`
* `"macos"`
* `"ios"`
* `"linux"`
* `"android"`
* `"freebsd"`
* `"dragonfly"`
* `"openbsd"`
* `"netbsd"`
* `"none"`（嵌入式目标的典型值）

r[cfg.target_family]
### `target_family`

r[cfg.target_family.def]
键值选项，提供对目标更通用的描述，例如该目标通常所属的操作系统族或架构族。可以设置任意数量的 `target_family` 键值对。

r[cfg.target_family.values]
示例值：

* `"unix"`
* `"windows"`
* `"wasm"`
* `"unix"` 和 `"wasm"` 同时存在

r[cfg.target_family.unix]
### `unix` 和 `windows`

若设置了 `target_family = "unix"`，则设置 `unix`。

r[cfg.target_family.windows]
若设置了 `target_family = "windows"`，则设置 `windows`。

r[cfg.target_env]
### `target_env`

r[cfg.target_env.def]
键值选项，设置关于目标平台的进一步消歧信息，包括所用的 ABI 或 `libc`。由于历史原因，仅在实际需要消歧时，此值才被定义为非空字符串。因此，例如，在许多 GNU 平台上，此值将为空。此值类似于平台目标三元组的第四个元素。一个区别是，像 `gnueabihf` 这样的嵌入式 ABI 会简单地将 `target_env` 定义为 `"gnu"`。

r[cfg.target_env.values]
示例值：

* `""`
* `"gnu"`
* `"msvc"`
* `"musl"`
* `"sgx"`
* `"sim"`
* `"macabi"`

r[cfg.target_abi]
### `target_abi`

r[cfg.target_abi.def]
键值选项，设置为用关于目标 ABI 的信息进一步消歧目标。

r[cfg.target_abi.disambiguation]
由于历史原因，仅在实际需要消歧时，此值才被定义为非空字符串。因此，例如，在许多 GNU 平台上，此值将为空。

r[cfg.target_abi.values]
示例值：

* `""`
* `"llvm"`
* `"eabihf"`
* `"abi64"`

r[cfg.target_endian]
### `target_endian`

键值选项，根据目标 CPU 的端序，设置一次，值为 "little" 或 "big"。

r[cfg.target_pointer_width]
### `target_pointer_width`

r[cfg.target_pointer_width.def]
键值选项，针对目标的指针宽度（以位计）设置一次。

r[cfg.target_pointer_width.values]
示例值：

* `"16"`
* `"32"`
* `"64"`

r[cfg.target_vendor]
### `target_vendor`

r[cfg.target_vendor.def]
键值选项，针对目标的供应商设置一次。

r[cfg.target_vendor.values]
示例值：

* `"apple"`
* `"fortanix"`
* `"pc"`
* `"unknown"`

r[cfg.target_has_atomic]
### `target_has_atomic`

r[cfg.target_has_atomic.def]
键值选项，为目标支持原子加载、存储和比较并交换操作的每个位宽设置。

r[cfg.target_has_atomic.stdlib]
当此 cfg 存在时，相关原子宽度的所有稳定 [`core::sync::atomic`] API 都可用。

r[cfg.target_has_atomic.values]
可能的值：

* `"8"`
* `"16"`
* `"32"`
* `"64"`
* `"128"`
* `"ptr"`

r[cfg.target_has_atomic_primitive_alignment]
### `target_has_atomic_primitive_alignment`

r[cfg.target_has_atomic_primitive_alignment.def]
键值选项，为 [原子][core::sync::atomic] 类型与对应整数类型具有相同对齐的每个位宽设置。

> **注意**
> 对于给定位宽，对齐通常相同。然而，在某些目标上，例如 32 位 x86，像 [`AtomicI64`][core::sync::atomic::AtomicI64] 这样的 64 位原子类型对齐为 8 字节，而 `i64` 只对齐到 4 字节。在这种情况下，不设置 `target_has_atomic_primitive_alignment = "64"`。

r[cfg.target_has_atomic_primitive_alignment.values]
可能的值：

* `"8"`
* `"16"`
* `"32"`
* `"64"`
* `"128"`
* `"ptr"`

r[cfg.test]
### `test`

在编译测试工具时启用。对 `rustc` 使用 [`--test`] 标志完成。测试支持见 [测试][Testing]。

r[cfg.debug_assertions]
### `debug_assertions`

在不带优化编译时默认启用。这可用于在开发中启用额外的调试代码，而在生产中不启用。例如，它控制标准库 [`debug_assert!`] 宏的行为。

r[cfg.proc_macro]
### `proc_macro`

当正在编译的 crate 以 `proc_macro` [crate 类型][crate type] 编译时设置。

r[cfg.panic]
### `panic`

r[cfg.panic.def]
键值选项，根据 [panic 策略][panic strategy] 设置。注意将来可能加入更多值。

r[cfg.panic.values]
示例值：

* `"abort"`
* `"unwind"`

[panic strategy]: panic.md#panic-strategy

## 条件编译的形式

<!-- template:attributes -->
r[cfg.attr]
### `cfg` 属性

r[cfg.attr.intro]
*`cfg` [属性][attribute]* 根据配置谓词有条件地包含它所附着的形式。

> [!EXAMPLE]
> ```rust
> // 仅在为 macOS 编译时，该函数才包含在构建中
> #[cfg(target_os = "macos")]
> fn macos_only() {
>   // ...
> }
>
> // 仅在定义了 foo 或 bar 时才包含此函数
> #[cfg(any(foo, bar))]
> fn needs_foo_or_bar() {
>   // ...
> }
>
> // 仅在为 32 位的类 unix OS 编译时才包含此函数
> #[cfg(all(unix, target_pointer_width = "32"))]
> fn on_32bit_unix() {
>   // ...
> }
>
> // 仅在未定义 foo 时才包含此函数
> #[cfg(not(foo))]
> fn needs_not_foo() {
>   // ...
> }
>
> // 仅在 panic 策略设置为 unwind 时才包含此函数
> #[cfg(panic = "unwind")]
> fn when_unwinding() {
>   // ...
> }
> ```

r[cfg.attr.syntax]
`cfg` 属性的语法为：

```grammar,configuration
@root CfgAttribute -> `cfg` `(` ConfigurationPredicate `)`
```

r[cfg.attr.allowed-positions]
只要允许属性的地方都可以使用 `cfg` 属性。

r[cfg.attr.duplicates]
`cfg` 属性可以在一个形式上使用任意次数。除非如 [cfg.attr.crate-level-attrs] 所述，若任何 `cfg` 谓词为 false，则属性所附着的形式将不被包含。

r[cfg.attr.effect]
若谓词为 true，该形式被改写为不再带有其上的 `cfg` 属性。若任何谓词为 false，该形式从源代码中移除。

r[cfg.attr.crate-level-attrs]
当 crate 级 `cfg` 的谓词为 false 时，crate 本身仍然存在。该 `cfg` 之前的任何 crate 属性被保留，该 `cfg` 之后的任何 crate 属性被移除，其后的全部 crate 内容也被移除。

> [!EXAMPLE]
> 不移除前面属性的行为允许你做诸如包含 `#![no_std]` 以避免链接 `std` 之类的事情，即使 `#![cfg(...)]` 在其他方面已移除 crate 的内容。例如：
>
> <!-- ignore: test infrastructure can't handle no_std -->
> ```rust
> // 即使 crate 级 `cfg` 属性为 false，
> // 此 `no_std` 属性仍被保留。
> #![no_std]
> #![cfg(false)]
>
> // 此函数不被包含。
> pub fn example() {}
> ```

<!-- template:attributes -->
r[cfg.cfg_attr]
### `cfg_attr` 属性

r[cfg.cfg_attr.intro]
*`cfg_attr` [属性][attribute]* 根据配置谓词有条件地包含属性。

> [!EXAMPLE]
> 下列模块将根据目标在 `linux.rs` 或 `windows.rs` 中找到。
>
> <!-- ignore: `mod` needs multiple files -->
> ```rust
> #[cfg_attr(target_os = "linux", path = "linux.rs")]
> #[cfg_attr(windows, path = "windows.rs")]
> mod os;
> ```

r[cfg.cfg_attr.syntax]
`cfg_attr` 属性的语法为：

```grammar,configuration
@root CfgAttrAttribute -> `cfg_attr` `(` ConfigurationPredicate `,` CfgAttrs? `)`

CfgAttrs -> Attr (`,` Attr)* `,`?
```

r[cfg.cfg_attr.allowed-positions]
只要允许属性的地方都可以使用 `cfg_attr` 属性。

r[cfg.cfg_attr.duplicates]
`cfg_attr` 属性可以在一个形式上使用任意次数。

r[cfg.cfg_attr.attr-restriction]
[`crate_type`] 和 [`crate_name`] 属性不能与 `cfg_attr` 一起使用。

r[cfg.cfg_attr.behavior]
当配置谓词为 true 时，`cfg_attr` 展开为谓词之后列出的属性。

r[cfg.cfg_attr.attribute-list]
可以列出零个、一个或多个属性。多个属性将各自展开为单独的属性。

> [!EXAMPLE]
> <!-- ignore: fake attributes -->
> ```rust
> #[cfg_attr(feature = "magic", sparkles, crackles)]
> fn bewitched() {}
>
> // 当启用 `magic` 特性标志时，上面将展开为：
> #[sparkles]
> #[crackles]
> fn bewitched() {}
> ```

> **注意**
> `cfg_attr` 可以展开为另一个 `cfg_attr`。例如，`#[cfg_attr(target_os = "linux", cfg_attr(feature = "multithreaded", some_other_attribute))]` 是合法的。此例等价于 `#[cfg_attr(all(target_os = "linux", feature = "multithreaded"), some_other_attribute)]`。

r[cfg.macro]
### `cfg` 宏

内置的 `cfg` 宏接受单个配置谓词，当谓词为 true 时求值为 `true` 字面量，当其为 false 时求值为 `false` 字面量。

例如：

```rust
let machine_kind = if cfg!(unix) {
  "unix"
} else if cfg!(windows) {
  "windows"
} else {
  "unknown"
};

println!("I'm running on a {} machine!", machine_kind);
```

r[cfg.cfg_select]
### `cfg_select` 宏

r[cfg.cfg_select.intro]
内置的 [`cfg_select!`][std::cfg_select] 宏可用于根据多个配置谓词在编译期选择代码。

> [!EXAMPLE]
> ```rust
> cfg_select! {
>     unix => {
>         fn foo() { /* unix 特有功能 */ }
>     }
>     target_pointer_width = "32" => {
>         fn foo() { /* 非 unix、32 位功能 */ }
>     }
>     _ => {
>         fn foo() { /* 回退实现 */ }
>     }
> }
>
> let is_unix_str = cfg_select! {
>     unix => "unix",
>     _ => "not unix",
> };
> ```

r[cfg.cfg_select.syntax]
```grammar,configuration
@root CfgSelect -> CfgSelectArms?

CfgSelectArms ->
    CfgSelectConfigurationPredicate `=>`
    (
        `{` ^ TokenTree `}` `,`? CfgSelectArms?
      | ExpressionWithBlockNoAttrs `,`? CfgSelectArms?
      | ExpressionWithoutBlockNoAttrs ( `,` CfgSelectArms? )?
    )

CfgSelectConfigurationPredicate ->
    ConfigurationPredicate | `_`
```

r[cfg.cfg_select.first-arm]
`cfg_select` 展开为第一个配置谓词求值为 true 的分支的载荷。

r[cfg.cfg_select.braces]
若整个载荷用花括号包裹，展开时花括号会被移除。

r[cfg.cfg_select.wildcard]
配置谓词 `_` 总是求值为 true。

r[cfg.cfg_select.fallthrough]
若没有任何谓词求值为 true，则为编译错误。

r[cfg.cfg_select.well-formed]
每个右端必须是该宏被调用位置上语法合法的展开。

[Testing]: attributes/testing.md
[`--cfg`]: ../rustc/command-line-arguments.html#--cfg-configure-the-compilation-environment
[`--test`]: ../rustc/command-line-arguments.html#--test-build-a-test-harness
[`cfg`]: #the-cfg-attribute
[`cfg!`]: #the-cfg-macro
[`cfg_attr`]: #the-cfg_attr-attribute
[`cfg_select!`]: #the-cfg_select-macro
[`crate_name`]: crates-and-source-files.md#the-crate_name-attribute
[`crate_type`]: linkage.md
[`target_feature` attribute]: attributes/codegen.md#the-target_feature-attribute
[attribute]: attributes.md
[attributes]: attributes.md
[cargo-feature]: ../cargo/reference/features.html
[crate type]: linkage.md
[macros]: macros.md
[static C runtime]: linkage.md#static-and-dynamic-c-runtimes
