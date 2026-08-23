+++
title = "01-Lint 配置项"
date = 2026-08-22T18:00:00+08:00
weight = 31
type = "docs"
description = "所有可配置 lint 选项列表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# Lint 配置项 {#lint-configuration}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/lint_configuration.html](https://doc.rust-lang.org/nightly/clippy/lint_configuration.html)


<!--
此文件由 `cargo bless --test config-metadata` 生成。
请使用该命令更新此文件，不要手动编辑。
-->


下列列表展示每个配置项及其说明、默认值、示例和受影响的 lint。

---

## `absolute-paths-allowed-crates`
允许使用绝对路径的 crate 列表

**默认值：** `[]`

---
**受影响的 lint：**
* [`absolute_paths`](https://rust-lang.github.io/rust-clippy/main/index.html#absolute_paths)


## `absolute-paths-max-segments`
路径在被 lint 检查之前可拥有的最大段数，超过此限制的将被 lint。

**默认值：** `2`

---
**受影响的 lint：**
* [`absolute_paths`](https://rust-lang.github.io/rust-clippy/main/index.html#absolute_paths)


## `accept-comment-above-attributes`
是否允许将安全注释放在 `unsafe` 块的属性上方

**默认值：** `true`

---
**受影响的 lint：**
* [`undocumented_unsafe_blocks`](https://rust-lang.github.io/rust-clippy/main/index.html#undocumented_unsafe_blocks)


## `accept-comment-above-statement`
是否允许将安全注释放在包含 `unsafe` 块的语句上方

**默认值：** `true`

---
**受影响的 lint：**
* [`undocumented_unsafe_blocks`](https://rust-lang.github.io/rust-clippy/main/index.html#undocumented_unsafe_blocks)


## `allow-comparison-to-zero`
当模运算结果与零比较时不触发 lint。

**默认值：** `true`

---
**受影响的 lint：**
* [`modulo_arithmetic`](https://rust-lang.github.io/rust-clippy/main/index.html#modulo_arithmetic)


## `allow-dbg-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中使用 `dbg!`

**默认值：** `false`

---
**受影响的 lint：**
* [`dbg_macro`](https://rust-lang.github.io/rust-clippy/main/index.html#dbg_macro)


## `allow-exact-repetitions`
是否允许项与其所在模块同名

**默认值：** `true`

---
**受影响的 lint：**
* [`module_name_repetitions`](https://rust-lang.github.io/rust-clippy/main/index.html#module_name_repetitions)


## `allow-expect-in-consts`
是否允许在始终在编译时求值的代码中使用 `expect`

**默认值：** `true`

---
**受影响的 lint：**
* [`expect_used`](https://rust-lang.github.io/rust-clippy/main/index.html#expect_used)


## `allow-expect-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中使用 `expect`

**默认值：** `false`

---
**受影响的 lint：**
* [`expect_used`](https://rust-lang.github.io/rust-clippy/main/index.html#expect_used)


## `allow-indexing-slicing-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中忽略 `indexing_slicing`

**默认值：** `false`

---
**受影响的 lint：**
* [`indexing_slicing`](https://rust-lang.github.io/rust-clippy/main/index.html#indexing_slicing)


## `allow-large-stack-frames-in-tests`
是否检查 `#[cfg(test)]` 模块内或测试函数中的函数。

**默认值：** `true`

---
**受影响的 lint：**
* [`large_stack_frames`](https://rust-lang.github.io/rust-clippy/main/index.html#large_stack_frames)


## `allow-mixed-uninlined-format-args`
是否允许混合的非内联 format 参数，例如 `format!("{} {}", a, foo.bar)`

**默认值：** `true`

---
**受影响的 lint：**
* [`uninlined_format_args`](https://rust-lang.github.io/rust-clippy/main/index.html#uninlined_format_args)


## `allow-one-hash-in-raw-strings`
当可以使用 `r""` 时，是否允许使用 `r#""#`

**默认值：** `false`

---
**受影响的 lint：**
* [`needless_raw_string_hashes`](https://rust-lang.github.io/rust-clippy/main/index.html#needless_raw_string_hashes)


## `allow-panic-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中使用 `panic`

**默认值：** `false`

---
**受影响的 lint：**
* [`panic`](https://rust-lang.github.io/rust-clippy/main/index.html#panic)


## `allow-print-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中使用打印宏（例如 `println!`）

**默认值：** `false`

---
**受影响的 lint：**
* [`print_stderr`](https://rust-lang.github.io/rust-clippy/main/index.html#print_stderr)
* [`print_stdout`](https://rust-lang.github.io/rust-clippy/main/index.html#print_stdout)


## `allow-private-module-inception`
若非 public，是否允许模块嵌套 inception。

**默认值：** `false`

---
**受影响的 lint：**
* [`module_inception`](https://rust-lang.github.io/rust-clippy/main/index.html#module_inception)


## `allow-renamed-params-for`
检查重命名函数参数时忽略的 trait 路径列表。

#### 示例

```toml
allow-renamed-params-for = [ "std::convert::From" ]
```

#### 注意事项

- 默认情况下，以下 trait 会被忽略：`From`、`TryFrom`、`FromStr`
- 可将 `".."` 作为列表的一部分，表示将配置值追加到 Clippy 的默认配置。默认情况下，任何配置都会替换默认值。

**默认值：** `["core::convert::From", "core::convert::TryFrom", "core::str::FromStr"]`

---
**受影响的 lint：**
* [`renamed_function_params`](https://rust-lang.github.io/rust-clippy/main/index.html#renamed_function_params)


## `allow-unwrap-in-consts`
是否允许在始终在编译时求值的代码中使用 `unwrap`

**默认值：** `true`

---
**受影响的 lint：**
* [`unwrap_used`](https://rust-lang.github.io/rust-clippy/main/index.html#unwrap_used)


## `allow-unwrap-in-tests`
是否允许在测试函数或 `#[cfg(test)]` 中使用 `unwrap`

**默认值：** `false`

---
**受影响的 lint：**
* [`unwrap_used`](https://rust-lang.github.io/rust-clippy/main/index.html#unwrap_used)


## `allow-unwrap-types`
允许对哪些类型使用 `unwrap()` 和 `expect()`。

#### 示例

```toml
allow-unwrap-types = [ "std::sync::LockResult" ]
```

**默认值：** `[]`

---
**受影响的 lint：**
* [`expect_used`](https://rust-lang.github.io/rust-clippy/main/index.html#expect_used)
* [`unwrap_used`](https://rust-lang.github.io/rust-clippy/main/index.html#unwrap_used)


## `allow-useless-vec-in-tests`
`useless_vec` 是否应忽略测试函数或 `#[cfg(test)]`

**默认值：** `false`

---
**受影响的 lint：**
* [`useless_vec`](https://rust-lang.github.io/rust-clippy/main/index.html#useless_vec)


## `allowed-dotfiles`
额外允许的点文件（以点开头的文件或目录）

**默认值：** `[]`

---
**受影响的 lint：**
* [`path_ends_with_ext`](https://rust-lang.github.io/rust-clippy/main/index.html#path_ends_with_ext)


## `allowed-duplicate-crates`
允许重复的 crate 名称列表

**默认值：** `[]`

---
**受影响的 lint：**
* [`multiple_crate_versions`](https://rust-lang.github.io/rust-clippy/main/index.html#multiple_crate_versions)


## `allowed-idents-below-min-chars`
允许低于最小字符数的名称。可将值 `".."` 作为列表的一部分，表示将配置值追加到 Clippy 的默认配置。默认情况下，任何配置都会替换默认值。

**默认值：** `["i", "j", "x", "y", "z", "w", "n"]`

---
**受影响的 lint：**
* [`min_ident_chars`](https://rust-lang.github.io/rust-clippy/main/index.html#min_ident_chars)


## `allowed-prefixes`
在判断项名称是否以模块名结尾时允许的前缀列表。若项名称的其余部分是允许的前缀（例如模块 `foo` 中的项 `ToFoo` 或 `to_foo`），则不发出警告。

#### 示例

```toml
allowed-prefixes = [ "to", "from" ]
```

#### 注意事项

- 默认情况下，以下前缀被允许：`to`、`as`、`into`、`from`、`try_into` 和 `try_from`
- 每个 snake_case 变体自动包含 PascalCase 变体（例如若包含 `try_into`，也会包含 `TryInto`）
- 使用 `".."` 作为列表的一部分，表示将配置值追加到 Clippy 的默认配置。默认情况下，任何配置都会替换默认值

**默认值：** `["to", "as", "into", "from", "try_into", "try_from"]`

---
**受影响的 lint：**
* [`module_name_repetitions`](https://rust-lang.github.io/rust-clippy/main/index.html#module_name_repetitions)


## `allowed-scripts`
范围内允许使用的 Unicode 脚本列表。

**默认值：** `["Latin"]`

---
**受影响的 lint：**
* [`disallowed_script_idents`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_script_idents)


## `allowed-wildcard-imports`
允许使用通配符导入的路径段列表。

#### 示例

```toml
allowed-wildcard-imports = [ "utils", "common" ]
```

#### 注意事项

1. 若与 `warn_on_all_wildcard_imports = true` 一起使用，此配置无效。
2. 包含单词 'prelude' 的任意段的路径默认已允许。

**默认值：** `[]`

---
**受影响的 lint：**
* [`wildcard_imports`](https://rust-lang.github.io/rust-clippy/main/index.html#wildcard_imports)


## `arithmetic-side-effects-allowed`
在所有类型的运算中抑制对指定类型名称的检查。

若需要特定运算，请考虑使用 `arithmetic_side_effects_allowed_binary` 或 `arithmetic_side_effects_allowed_unary`。

#### 示例

```toml
arithmetic-side-effects-allowed = ["SomeType", "AnotherType"]
```

#### 注意事项

在此配置中列出的类型（例如 `SomeType`）的行为与在 `arithmetic_side_effects_allowed_binary` 中使用 `["SomeType" , "*"]`、`["*", "SomeType"]` 相同。

**默认值：** `[]`

---
**受影响的 lint：**
* [`arithmetic_side_effects`](https://rust-lang.github.io/rust-clippy/main/index.html#arithmetic_side_effects)


## `arithmetic-side-effects-allowed-binary`
在加法或乘法等二元运算中抑制对指定类型对名称的检查。

支持 `"*"` 通配符，表示无论涉及的另一方类型如何，某种类型都不会触发 lint。例如 `["SomeType", "*"]` 或 `["*", "AnotherType"]`。

类型对不对称，即 `["SomeType", "AnotherType"]` 与 `["AnotherType", "SomeType"]` 不同。

#### 示例

```toml
arithmetic-side-effects-allowed-binary = [["SomeType" , "f32"], ["AnotherType", "*"]]
```

**默认值：** `[]`

---
**受影响的 lint：**
* [`arithmetic_side_effects`](https://rust-lang.github.io/rust-clippy/main/index.html#arithmetic_side_effects)


## `arithmetic-side-effects-allowed-unary`
在取负（`-`）等一元运算中抑制对指定类型名称的检查。

#### 示例

```toml
arithmetic-side-effects-allowed-unary = ["SomeType", "AnotherType"]
```

**默认值：** `[]`

---
**受影响的 lint：**
* [`arithmetic_side_effects`](https://rust-lang.github.io/rust-clippy/main/index.html#arithmetic_side_effects)


## `array-size-threshold`
栈上数组允许的最大大小

**默认值：** `16384`

---
**受影响的 lint：**
* [`large_const_arrays`](https://rust-lang.github.io/rust-clippy/main/index.html#large_const_arrays)
* [`large_stack_arrays`](https://rust-lang.github.io/rust-clippy/main/index.html#large_stack_arrays)


## `avoid-breaking-exported-api`
当建议的更改会导致其他 crate 出现破坏性变更时，抑制 lint。

**默认值：** `true`

---
**受影响的 lint：**
* [`box_collection`](https://rust-lang.github.io/rust-clippy/main/index.html#box_collection)
* [`enum_variant_names`](https://rust-lang.github.io/rust-clippy/main/index.html#enum_variant_names)
* [`large_types_passed_by_value`](https://rust-lang.github.io/rust-clippy/main/index.html#large_types_passed_by_value)
* [`linkedlist`](https://rust-lang.github.io/rust-clippy/main/index.html#linkedlist)
* [`needless_pass_by_ref_mut`](https://rust-lang.github.io/rust-clippy/main/index.html#needless_pass_by_ref_mut)
* [`option_option`](https://rust-lang.github.io/rust-clippy/main/index.html#option_option)
* [`owned_cow`](https://rust-lang.github.io/rust-clippy/main/index.html#owned_cow)
* [`rc_buffer`](https://rust-lang.github.io/rust-clippy/main/index.html#rc_buffer)
* [`rc_mutex`](https://rust-lang.github.io/rust-clippy/main/index.html#rc_mutex)
* [`redundant_allocation`](https://rust-lang.github.io/rust-clippy/main/index.html#redundant_allocation)
* [`ref_option`](https://rust-lang.github.io/rust-clippy/main/index.html#ref_option)
* [`single_call_fn`](https://rust-lang.github.io/rust-clippy/main/index.html#single_call_fn)
* [`trivially_copy_pass_by_ref`](https://rust-lang.github.io/rust-clippy/main/index.html#trivially_copy_pass_by_ref)
* [`unnecessary_box_returns`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_box_returns)
* [`unnecessary_wraps`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_wraps)
* [`unused_self`](https://rust-lang.github.io/rust-clippy/main/index.html#unused_self)
* [`upper_case_acronyms`](https://rust-lang.github.io/rust-clippy/main/index.html#upper_case_acronyms)
* [`vec_box`](https://rust-lang.github.io/rust-clippy/main/index.html#vec_box)
* [`wrong_self_convention`](https://rust-lang.github.io/rust-clippy/main/index.html#wrong_self_convention)


## `await-holding-invalid-types`
在 await 点不允许持有的类型列表。

**默认值：** `[]`

---
**受影响的 lint：**
* [`await_holding_invalid_type`](https://rust-lang.github.io/rust-clippy/main/index.html#await_holding_invalid_type)


## `cargo-ignore-publish`
仅供内部测试使用，忽略 Cargo manifest 中当前的 `publish` 设置。

**默认值：** `false`

---
**受影响的 lint：**
* [`cargo_common_metadata`](https://rust-lang.github.io/rust-clippy/main/index.html#cargo_common_metadata)


## `check-grouped-late-init`
是否检查来自多个 `let` 语句的分组延迟初始化。

#### 示例

```rust
let a;
let b;
if true {
    a = 1;
    b = 2;
} else {
    a = 3;
    b = 4;
}
```

可改为：

```rust
let (a, b) = if true {
    (1, 2)
} else {
    (3, 4)
};
```

**默认值：** `true`

---
**受影响的 lint：**
* [`needless_late_init`](https://rust-lang.github.io/rust-clippy/main/index.html#needless_late_init)


## `check-incompatible-msrv-in-tests`
是否在 `#[test]` 和 `#[cfg(test)]` 代码中检查 MSRV 兼容性。

**默认值：** `false`

---
**受影响的 lint：**
* [`incompatible_msrv`](https://rust-lang.github.io/rust-clippy/main/index.html#incompatible_msrv)


## `check-inconsistent-struct-field-initializers`
当初始化器存在时，是否建议重新排序构造函数字段。

此配置产生的警告不一定仅通过重新排序字段即可修复。即使建议的代码能够编译，若初始化表达式有副作用，也可能改变语义。以下 [rust-clippy#11846] 中的示例展示了建议如何导致借用检查错误：

```rust
struct MyStruct {
    vector: Vec<u32>,
    length: usize
}
fn main() {
    let vector = vec![1,2,3];
    MyStruct { length: vector.len(), vector};
}
```

[from rust-clippy#11846]: https://github.com/rust-lang/rust-clippy/issues/11846#issuecomment-1820747924

**默认值：** `false`

---
**受影响的 lint：**
* [`inconsistent_struct_constructor`](https://rust-lang.github.io/rust-clippy/main/index.html#inconsistent_struct_constructor)


## `check-private-items`
是否也对私有项运行所列 lint。

**默认值：** `false`

---
**受影响的 lint：**
* [`missing_errors_doc`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_errors_doc)
* [`missing_panics_doc`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_panics_doc)
* [`missing_safety_doc`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_safety_doc)
* [`unnecessary_safety_doc`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_safety_doc)


## `cognitive-complexity-threshold`
函数可拥有的最大认知复杂度

**默认值：** `25`

---
**受影响的 lint：**
* [`cognitive_complexity`](https://rust-lang.github.io/rust-clippy/main/index.html#cognitive_complexity)


## `const-literal-digits-threshold`
常量浮点字面量抑制 `excessive_precicion` lint 所需的最少位数

**默认值：** `30`

---
**受影响的 lint：**
* [`excessive_precision`](https://rust-lang.github.io/rust-clippy/main/index.html#excessive_precision)


## `disallowed-fields`
禁止使用的字段列表，以完全限定路径书写。

**字段：**
- `path`（必需）：应禁止的字段的完全限定路径
- `reason`（可选）：禁止此字段的原因说明
- `replacement`（可选）：建议的替代方法
- `allow-invalid`（可选，默认为 `false`）：设为 `true` 时，若路径不存在则忽略此项，而不是发出错误

**默认值：** `[]`

---
**受影响的 lint：**
* [`disallowed_fields`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_fields)


## `disallowed-macros`
禁止使用的宏列表，以完全限定路径书写。

**字段：**
- `path`（必需）：应禁止的宏的完全限定路径
- `reason`（可选）：禁止此宏的原因说明
- `replacement`（可选）：建议的替代宏
- `allow-invalid`（可选，默认为 `false`）：设为 `true` 时，若路径不存在则忽略此项，而不是发出错误

**默认值：** `[]`

---
**受影响的 lint：**
* [`disallowed_macros`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_macros)


## `disallowed-methods`
禁止使用的方法列表，以完全限定路径书写。

**字段：**
- `path`（必需）：应禁止的方法的完全限定路径
- `reason`（可选）：禁止此方法的原因说明
- `replacement`（可选）：建议的替代方法
- `allow-invalid`（可选，默认为 `false`）：设为 `true` 时，若路径不存在则忽略此项，而不是发出错误

**默认值：** `[]`

---
**受影响的 lint：**
* [`disallowed_methods`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_methods)


## `disallowed-names`
要对其发出 lint 的禁止名称列表。注意：`bar` 不在此列，因为它有合法用途。可将值 `".."` 作为列表的一部分，表示将配置值追加到 Clippy 的默认配置。默认情况下，任何配置都会替换默认值。

**默认值：** `["foo", "baz", "quux"]`

---
**受影响的 lint：**
* [`disallowed_names`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_names)


## `disallowed-types`
禁止使用的类型列表，以完全限定路径书写。

**字段：**
- `path`（必需）：应禁止的类型的完全限定路径
- `reason`（可选）：禁止此类型的原因说明
- `replacement`（可选）：建议的替代类型
- `allow-invalid`（可选，默认为 `false`）：设为 `true` 时，若路径不存在则忽略此项，而不是发出错误

**默认值：** `[]`

---
**受影响的 lint：**
* [`disallowed_types`](https://rust-lang.github.io/rust-clippy/main/index.html#disallowed_types)


## `doc-valid-idents`
此 lint 不应视为需要反引号的标识符的单词列表。可将值 `".."` 作为列表的一部分，表示将配置值追加到 Clippy 的默认配置。默认情况下，任何配置都会替换默认值。例如：
* `doc-valid-idents = ["ClipPy"]` 会用 `["ClipPy"]` 替换默认列表。
* `doc-valid-idents = ["ClipPy", ".."]` 会将 `ClipPy` 追加到默认列表。

**默认值：** `["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "MHz", "GHz", "THz", "AccessKit", "CoAP", "CoreFoundation", "CoreGraphics", "CoreText", "DevOps", "Direct2D", "Direct3D", "DirectWrite", "DirectX", "ECMAScript", "GPLv2", "GPLv3", "GitHub", "GitLab", "IPv4", "IPv6", "InfiniBand", "RoCE", "ClojureScript", "CoffeeScript", "JavaScript", "PostScript", "PureScript", "TypeScript", "PowerPC", "PowerShell", "WebAssembly", "NaN", "NaNs", "OAuth", "GraphQL", "SQLite", "MySQL", "PostgreSQL", "MariaDB", "MongoDB", "OCaml", "OpenAL", "OpenDNS", "OpenGL", "OpenMP", "OpenSSH", "OpenSSL", "OpenStreetMap", "OpenTelemetry", "OpenType", "WebAuthn", "WebGL", "WebGL2", "WebGPU", "WebRTC", "WebSocket", "WebTransport", "WebP", "OpenExr", "YCbCr", "sRGB", "TensorFlow", "TrueType", "iOS", "macOS", "FreeBSD", "NetBSD", "OpenBSD", "NixOS", "TeX", "LaTeX", "BibTeX", "BibLaTeX", "MinGW", "CamelCase"]`

---
**受影响的 lint：**
* [`doc_markdown`](https://rust-lang.github.io/rust-clippy/main/index.html#doc_markdown)


## `enable-raw-pointer-heuristic-for-send`
是否应用原始指针启发式来判断类型是否为 `Send`。

**默认值：** `true`

---
**受影响的 lint：**
* [`non_send_fields_in_send_ty`](https://rust-lang.github.io/rust-clippy/main/index.html#non_send_fields_in_send_ty)


## `enforce-iter-loop-reborrow`
是否建议对重新借用的值使用隐式 into iter。

#### 示例

```no_run
let mut vec = vec![1, 2, 3];
let rmvec = &mut vec;
for _ in rmvec.iter() {}
for _ in rmvec.iter_mut() {}
```

可改为：

```no_run
let mut vec = vec![1, 2, 3];
let rmvec = &mut vec;
for _ in &*rmvec {}
for _ in &mut *rmvec {}
```

**默认值：** `false`

---
**受影响的 lint：**
* [`explicit_iter_loop`](https://rust-lang.github.io/rust-clippy/main/index.html#explicit_iter_loop)


## `enforced-import-renames`
始终要重命名的导入列表，为完全限定路径后跟重命名名称。

**默认值：** `[]`

---
**受影响的 lint：**
* [`missing_enforced_import_renames`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_enforced_import_renames)


## `enum-variant-name-threshold`
触发变体名称相关 lint 所需的最少枚举变体数

**默认值：** `3`

---
**受影响的 lint：**
* [`enum_variant_names`](https://rust-lang.github.io/rust-clippy/main/index.html#enum_variant_names)


## `enum-variant-size-threshold`
避免 box 建议的枚举变体最大大小

**默认值：** `200`

---
**受影响的 lint：**
* [`large_enum_variant`](https://rust-lang.github.io/rust-clippy/main/index.html#large_enum_variant)


## `excessive-nesting-threshold`
代码块可嵌套的最大层数

**默认值：** `0`

---
**受影响的 lint：**
* [`excessive_nesting`](https://rust-lang.github.io/rust-clippy/main/index.html#excessive_nesting)


## `future-size-threshold`
`Future` 可拥有的最大字节大小，超过此值将触发 `clippy::large_futures` lint

**默认值：** `16384`

---
**受影响的 lint：**
* [`large_futures`](https://rust-lang.github.io/rust-clippy/main/index.html#large_futures)


## `ignore-interior-mutability`
应视为不包含内部可变性的类型路径列表

**默认值：** `["bytes::Bytes"]`

---
**受影响的 lint：**
* [`borrow_interior_mutable_const`](https://rust-lang.github.io/rust-clippy/main/index.html#borrow_interior_mutable_const)
* [`declare_interior_mutable_const`](https://rust-lang.github.io/rust-clippy/main/index.html#declare_interior_mutable_const)
* [`ifs_same_cond`](https://rust-lang.github.io/rust-clippy/main/index.html#ifs_same_cond)
* [`mutable_key_type`](https://rust-lang.github.io/rust-clippy/main/index.html#mutable_key_type)


## `inherent-impl-lint-scope`
设置对同一类型的重复固有 `impl` 块进行 lint 的范围（`"crate"`、`"file"` 或 `"module"`）。

**默认值：** `"crate"`

---
**受影响的 lint：**
* [`multiple_inherent_impl`](https://rust-lang.github.io/rust-clippy/main/index.html#multiple_inherent_impl)


## `large-error-ignored`
在函数返回的 `Result` 中应作为过大 `Err` 变体忽略的类型路径列表

**默认值：** `[]`

---
**受影响的 lint：**
* [`result_large_err`](https://rust-lang.github.io/rust-clippy/main/index.html#result_large_err)


## `large-error-threshold`
函数返回的 `Result` 中 `Err` 变体的最大大小

**默认值：** `128`

---
**受影响的 lint：**
* [`result_large_err`](https://rust-lang.github.io/rust-clippy/main/index.html#result_large_err)


## `lint-commented-code`
若要折叠的 `if` 和 `else if` 链在被折叠部分内含注释，是否仍对其发出 lint。

**默认值：** `false`

---
**受影响的 lint：**
* [`collapsible_else_if`](https://rust-lang.github.io/rust-clippy/main/index.html#collapsible_else_if)
* [`collapsible_if`](https://rust-lang.github.io/rust-clippy/main/index.html#collapsible_if)


## `literal-representation-threshold`
对十进制字面量进行 lint 的下限

**默认值：** `16384`

---
**受影响的 lint：**
* [`decimal_literal_representation`](https://rust-lang.github.io/rust-clippy/main/index.html#decimal_literal_representation)


## `matches-for-let-else`
是否应由 lint 考虑 `matches`，以及是否应对常见类型进行过滤。

**默认值：** `"WellKnownTypes"`

---
**受影响的 lint：**
* [`manual_let_else`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_let_else)


## `max-fn-params-bools`
函数可拥有的 bool 参数最大数量。
使用 `0` 可对任何带 bool 参数的函数发出 lint。

**默认值：** `3`

---
**受影响的 lint：**
* [`fn_params_excessive_bools`](https://rust-lang.github.io/rust-clippy/main/index.html#fn_params_excessive_bools)


## `max-include-file-size`
通过 `include_bytes!()` 或 `include_str!()` 包含的文件的最大大小（字节）

**默认值：** `1000000`

---
**受影响的 lint：**
* [`large_include_file`](https://rust-lang.github.io/rust-clippy/main/index.html#large_include_file)


## `max-struct-bools`
结构体可拥有的 bool 字段最大数量

**默认值：** `3`

---
**受影响的 lint：**
* [`struct_excessive_bools`](https://rust-lang.github.io/rust-clippy/main/index.html#struct_excessive_bools)


## `max-suggested-slice-pattern-length`
当 Clippy 建议使用切片模式时，建议的切片模式中允许的最大元素数量。若需要更多元素，则抑制该 lint。
例如，`[_, _, _, e, ..]` 是包含 4 个元素的切片模式。

**默认值：** `3`

---
**受影响的 lint：**
* [`index_refutable_slice`](https://rust-lang.github.io/rust-clippy/main/index.html#index_refutable_slice)


## `max-trait-bounds`
trait 可被 lint 检查的最大 bound 数量

**默认值：** `3`

---
**受影响的 lint：**
* [`type_repetition_in_bounds`](https://rust-lang.github.io/rust-clippy/main/index.html#type_repetition_in_bounds)


## `min-ident-chars-lint-trait-impl`
即使在 trait 声明之后，是否仍对字符过少的标识符发出 lint。

**默认值：** `false`

---
**受影响的 lint：**
* [`min_ident_chars`](https://rust-lang.github.io/rust-clippy/main/index.html#min_ident_chars)


## `min-ident-chars-threshold`
标识符可拥有的最少字符数，低于或等于此值的将被 lint。

**默认值：** `1`

---
**受影响的 lint：**
* [`min_ident_chars`](https://rust-lang.github.io/rust-clippy/main/index.html#min_ident_chars)


## `missing-docs-allow-unused`
是否允许以下划线开头的字段跳过文档要求

**默认值：** `false`

---
**受影响的 lint：**
* [`missing_docs_in_private_items`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_docs_in_private_items)


## `missing-docs-in-crate-items`
是否**仅**检查当前 crate 内可见项是否缺少文档。例如 `pub(crate)` 项。

**默认值：** `false`

---
**受影响的 lint：**
* [`missing_docs_in_private_items`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_docs_in_private_items)


## `module-item-order-groupings`
模块内不同源项种类的命名分组。

**默认值：** `[["modules", ["extern_crate", "mod", "foreign_mod"]], ["use", ["use"]], ["macros", ["macro"]], ["global_asm", ["global_asm"]], ["UPPER_SNAKE_CASE", ["static", "const"]], ["PascalCase", ["ty_alias", "enum", "struct", "union", "trait", "trait_alias", "impl"]], ["lower_snake_case", ["fn"]]]`

---
**受影响的 lint：**
* [`arbitrary_source_item_ordering`](https://rust-lang.github.io/rust-clippy/main/index.html#arbitrary_source_item_ordering)


## `module-items-ordered-within-groupings`
模块分组内的项是否应按字母顺序排列。

此选项可配置为 `"all"`、`"none"`，或应检查的特定分组名称列表（例如仅 `"enums"`）。

**默认值：** `"none"`

---
**受影响的 lint：**
* [`arbitrary_source_item_ordering`](https://rust-lang.github.io/rust-clippy/main/index.html#arbitrary_source_item_ordering)


## `msrv`
项目支持的最低 Rust 版本。默认为 `Cargo.toml` 中的 `rust-version` 字段

**默认值：** `current version`

---
**受影响的 lint：**
* [`allow_attributes`](https://rust-lang.github.io/rust-clippy/main/index.html#allow_attributes)
* [`allow_attributes_without_reason`](https://rust-lang.github.io/rust-clippy/main/index.html#allow_attributes_without_reason)
* [`almost_complete_range`](https://rust-lang.github.io/rust-clippy/main/index.html#almost_complete_range)
* [`approx_constant`](https://rust-lang.github.io/rust-clippy/main/index.html#approx_constant)
* [`assigning_clones`](https://rust-lang.github.io/rust-clippy/main/index.html#assigning_clones)
* [`borrow_as_ptr`](https://rust-lang.github.io/rust-clippy/main/index.html#borrow_as_ptr)
* [`cast_abs_to_unsigned`](https://rust-lang.github.io/rust-clippy/main/index.html#cast_abs_to_unsigned)
* [`checked_conversions`](https://rust-lang.github.io/rust-clippy/main/index.html#checked_conversions)
* [`cloned_instead_of_copied`](https://rust-lang.github.io/rust-clippy/main/index.html#cloned_instead_of_copied)
* [`collapsible_match`](https://rust-lang.github.io/rust-clippy/main/index.html#collapsible_match)
* [`collapsible_str_replace`](https://rust-lang.github.io/rust-clippy/main/index.html#collapsible_str_replace)
* [`deprecated_cfg_attr`](https://rust-lang.github.io/rust-clippy/main/index.html#deprecated_cfg_attr)
* [`derivable_impls`](https://rust-lang.github.io/rust-clippy/main/index.html#derivable_impls)
* [`err_expect`](https://rust-lang.github.io/rust-clippy/main/index.html#err_expect)
* [`filter_map_next`](https://rust-lang.github.io/rust-clippy/main/index.html#filter_map_next)
* [`from_over_into`](https://rust-lang.github.io/rust-clippy/main/index.html#from_over_into)
* [`if_then_some_else_none`](https://rust-lang.github.io/rust-clippy/main/index.html#if_then_some_else_none)
* [`implicit_saturating_sub`](https://rust-lang.github.io/rust-clippy/main/index.html#implicit_saturating_sub)
* [`index_refutable_slice`](https://rust-lang.github.io/rust-clippy/main/index.html#index_refutable_slice)
* [`inefficient_to_string`](https://rust-lang.github.io/rust-clippy/main/index.html#inefficient_to_string)
* [`io_other_error`](https://rust-lang.github.io/rust-clippy/main/index.html#io_other_error)
* [`iter_kv_map`](https://rust-lang.github.io/rust-clippy/main/index.html#iter_kv_map)
* [`legacy_numeric_constants`](https://rust-lang.github.io/rust-clippy/main/index.html#legacy_numeric_constants)
* [`len_zero`](https://rust-lang.github.io/rust-clippy/main/index.html#len_zero)
* [`lines_filter_map_ok`](https://rust-lang.github.io/rust-clippy/main/index.html#lines_filter_map_ok)
* [`manual_abs_diff`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_abs_diff)
* [`manual_bits`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_bits)
* [`manual_c_str_literals`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_c_str_literals)
* [`manual_clamp`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_clamp)
* [`manual_div_ceil`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_div_ceil)
* [`manual_flatten`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_flatten)
* [`manual_hash_one`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_hash_one)
* [`manual_is_ascii_check`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_is_ascii_check)
* [`manual_is_power_of_two`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_is_power_of_two)
* [`manual_is_variant_and`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_is_variant_and)
* [`manual_isolate_lowest_one`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_isolate_lowest_one)
* [`manual_let_else`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_let_else)
* [`manual_midpoint`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_midpoint)
* [`manual_non_exhaustive`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_non_exhaustive)
* [`manual_noop_waker`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_noop_waker)
* [`manual_option_as_slice`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_option_as_slice)
* [`manual_pattern_char_comparison`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_pattern_char_comparison)
* [`manual_range_contains`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_range_contains)
* [`manual_rem_euclid`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_rem_euclid)
* [`manual_repeat_n`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_repeat_n)
* [`manual_retain`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_retain)
* [`manual_slice_fill`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_slice_fill)
* [`manual_slice_size_calculation`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_slice_size_calculation)
* [`manual_split_once`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_split_once)
* [`manual_str_repeat`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_str_repeat)
* [`manual_strip`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_strip)
* [`manual_take`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_take)
* [`manual_try_fold`](https://rust-lang.github.io/rust-clippy/main/index.html#manual_try_fold)
* [`map_clone`](https://rust-lang.github.io/rust-clippy/main/index.html#map_clone)
* [`map_unwrap_or`](https://rust-lang.github.io/rust-clippy/main/index.html#map_unwrap_or)
* [`map_with_unused_argument_over_ranges`](https://rust-lang.github.io/rust-clippy/main/index.html#map_with_unused_argument_over_ranges)
* [`match_like_matches_macro`](https://rust-lang.github.io/rust-clippy/main/index.html#match_like_matches_macro)
* [`mem_replace_option_with_some`](https://rust-lang.github.io/rust-clippy/main/index.html#mem_replace_option_with_some)
* [`mem_replace_with_default`](https://rust-lang.github.io/rust-clippy/main/index.html#mem_replace_with_default)
* [`missing_const_for_fn`](https://rust-lang.github.io/rust-clippy/main/index.html#missing_const_for_fn)
* [`needless_borrow`](https://rust-lang.github.io/rust-clippy/main/index.html#needless_borrow)
* [`non_std_lazy_statics`](https://rust-lang.github.io/rust-clippy/main/index.html#non_std_lazy_statics)
* [`nonnull_unchecked_on_box_ptr`](https://rust-lang.github.io/rust-clippy/main/index.html#nonnull_unchecked_on_box_ptr)
* [`option_as_ref_deref`](https://rust-lang.github.io/rust-clippy/main/index.html#option_as_ref_deref)
* [`or_fun_call`](https://rust-lang.github.io/rust-clippy/main/index.html#or_fun_call)
* [`ptr_as_ptr`](https://rust-lang.github.io/rust-clippy/main/index.html#ptr_as_ptr)
* [`question_mark`](https://rust-lang.github.io/rust-clippy/main/index.html#question_mark)
* [`redundant_field_names`](https://rust-lang.github.io/rust-clippy/main/index.html#redundant_field_names)
* [`redundant_static_lifetimes`](https://rust-lang.github.io/rust-clippy/main/index.html#redundant_static_lifetimes)
* [`repeat_vec_with_capacity`](https://rust-lang.github.io/rust-clippy/main/index.html#repeat_vec_with_capacity)
* [`same_item_push`](https://rust-lang.github.io/rust-clippy/main/index.html#same_item_push)
* [`seek_from_current`](https://rust-lang.github.io/rust-clippy/main/index.html#seek_from_current)
* [`to_digit_is_some`](https://rust-lang.github.io/rust-clippy/main/index.html#to_digit_is_some)
* [`transmute_ptr_to_ref`](https://rust-lang.github.io/rust-clippy/main/index.html#transmute_ptr_to_ref)
* [`tuple_array_conversions`](https://rust-lang.github.io/rust-clippy/main/index.html#tuple_array_conversions)
* [`type_repetition_in_bounds`](https://rust-lang.github.io/rust-clippy/main/index.html#type_repetition_in_bounds)
* [`unchecked_time_subtraction`](https://rust-lang.github.io/rust-clippy/main/index.html#unchecked_time_subtraction)
* [`uninlined_format_args`](https://rust-lang.github.io/rust-clippy/main/index.html#uninlined_format_args)
* [`unnecessary_lazy_evaluations`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_lazy_evaluations)
* [`unnecessary_unwrap`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_unwrap)
* [`unnested_or_patterns`](https://rust-lang.github.io/rust-clippy/main/index.html#unnested_or_patterns)
* [`unused_trait_names`](https://rust-lang.github.io/rust-clippy/main/index.html#unused_trait_names)
* [`use_self`](https://rust-lang.github.io/rust-clippy/main/index.html#use_self)
* [`zero_ptr`](https://rust-lang.github.io/rust-clippy/main/index.html#zero_ptr)


## `pass-by-value-size-limit`
考虑按引用而非按值传递的类型最小大小（字节）。

**默认值：** `256`

---
**受影响的 lint：**
* [`large_types_passed_by_value`](https://rust-lang.github.io/rust-clippy/main/index.html#large_types_passed_by_value)


## `pub-underscore-fields-behavior`
根据导出可见性或是否标记为 `pub`，对结构体中带下划线前缀的「公开」字段进行 lint。

**默认值：** `"PubliclyExported"`

---
**受影响的 lint：**
* [`pub_underscore_fields`](https://rust-lang.github.io/rust-clippy/main/index.html#pub_underscore_fields)


## `recursive-self-in-type-definitions`
遇到递归类型时，是否应将结构体或枚举中的类型本身替换为 `Self`。

**默认值：** `true`

---
**受影响的 lint：**
* [`use_self`](https://rust-lang.github.io/rust-clippy/main/index.html#use_self)


## `semicolon-inside-block-ignore-singleline`
是否仅在多行时发出 lint。

**默认值：** `false`

---
**受影响的 lint：**
* [`semicolon_inside_block`](https://rust-lang.github.io/rust-clippy/main/index.html#semicolon_inside_block)


## `semicolon-outside-block-ignore-multiline`
是否仅在单行时发出 lint。

**默认值：** `false`

---
**受影响的 lint：**
* [`semicolon_outside_block`](https://rust-lang.github.io/rust-clippy/main/index.html#semicolon_outside_block)


## `single-char-binding-names-threshold`
作用域内可拥有的单字符绑定最大数量

**默认值：** `4`

---
**受影响的 lint：**
* [`many_single_char_names`](https://rust-lang.github.io/rust-clippy/main/index.html#many_single_char_names)


## `source-item-ordering`
应内部排序的元素种类，可选值为 `enum`、`impl`、`module`、`struct`、`trait`。

**默认值：** `["enum", "impl", "module", "struct", "trait"]`

---
**受影响的 lint：**
* [`arbitrary_source_item_ordering`](https://rust-lang.github.io/rust-clippy/main/index.html#arbitrary_source_item_ordering)


## `stack-size-threshold`
函数允许的最大栈大小（字节）

**默认值：** `512000`

---
**受影响的 lint：**
* [`large_stack_frames`](https://rust-lang.github.io/rust-clippy/main/index.html#large_stack_frames)


## `standard-macro-braces`
强制指定宏始终使用所规定的花括号。

可如下添加 `MacroMatcher`：`{ name = "macro_name", brace = "(" }`。若宏可使用完整路径，则需添加两个 `MacroMatcher`，一个为完整路径 `crate_name::macro_name`，另一个仅为宏名。

**默认值：** `[]`

---
**受影响的 lint：**
* [`nonstandard_macro_braces`](https://rust-lang.github.io/rust-clippy/main/index.html#nonstandard_macro_braces)


## `struct-field-name-threshold`
触发字段名称相关 lint 所需的最少结构体字段数

**默认值：** `3`

---
**受影响的 lint：**
* [`struct_field_names`](https://rust-lang.github.io/rust-clippy/main/index.html#struct_field_names)


## `suppress-restriction-lint-in-const`
是否在常量代码中抑制 restriction lint。在某些情况下，重构后的运算可能无法避免，因为建议的替代写法在常量代码中不可用。此配置会导致 restriction lint 即使无法给出建议也会触发。

**默认值：** `false`

---
**受影响的 lint：**
* [`indexing_slicing`](https://rust-lang.github.io/rust-clippy/main/index.html#indexing_slicing)


## `too-large-for-stack`
将被 lint 的对象最大大小（字节）。更大的对象放在堆上是可以的

**默认值：** `200`

---
**受影响的 lint：**
* [`boxed_local`](https://rust-lang.github.io/rust-clippy/main/index.html#boxed_local)
* [`useless_vec`](https://rust-lang.github.io/rust-clippy/main/index.html#useless_vec)


## `too-many-arguments-threshold`
函数或方法可拥有的最大参数数量

**默认值：** `7`

---
**受影响的 lint：**
* [`too_many_arguments`](https://rust-lang.github.io/rust-clippy/main/index.html#too_many_arguments)


## `too-many-lines-threshold`
函数或方法可拥有的最大行数

**默认值：** `100`

---
**受影响的 lint：**
* [`too_many_lines`](https://rust-lang.github.io/rust-clippy/main/index.html#too_many_lines)


## `trait-assoc-item-kinds-order`
trait 中关联项的顺序。

**默认值：** `["const", "type", "fn"]`

---
**受影响的 lint：**
* [`arbitrary_source_item_ordering`](https://rust-lang.github.io/rust-clippy/main/index.html#arbitrary_source_item_ordering)


## `trait-impl-item-order`
trait impl 中关联项的所需顺序：纯字母顺序、遵循 trait 定义顺序，或两者皆可。

注意，定义 trait 的 crate 在不同版本间 trait 定义顺序可能改变，而不被视为破坏性变更。

示例：

使用 trait 定义项顺序时：

```toml
trait-impl-item-order = "trait_item_ordering"
使用 trait 定义项顺序且回退为字母顺序时：

```toml
trait-impl-item-order = "alphabetical_or_trait_item_ordering"
```

**默认值：** `"alphabetical"`

---
**受影响的 lint：**
* [`arbitrary_source_item_ordering`](https://rust-lang.github.io/rust-clippy/main/index.html#arbitrary_source_item_ordering)


## `trivial-copy-size-limit`
考虑按值而非按引用传递的 `Copy` 类型的最大大小（字节）。

**默认值：** `target_pointer_width`

---
**受影响的 lint：**
* [`trivially_copy_pass_by_ref`](https://rust-lang.github.io/rust-clippy/main/index.html#trivially_copy_pass_by_ref)


## `type-complexity-threshold`
类型可拥有的最大复杂度

**默认值：** `250`

---
**受影响的 lint：**
* [`type_complexity`](https://rust-lang.github.io/rust-clippy/main/index.html#type_complexity)


## `unnecessary-box-size`
`Box<T>` 中 `T` 的字节大小，低于此值将触发 `clippy::unnecessary_box` lint

**默认值：** `128`

---
**受影响的 lint：**
* [`unnecessary_box_returns`](https://rust-lang.github.io/rust-clippy/main/index.html#unnecessary_box_returns)


## `unreadable-literal-lint-fractions`
是否应对小数的分数部分发出 lint 以包含分隔符。

**默认值：** `true`

---
**受影响的 lint：**
* [`unreadable_literal`](https://rust-lang.github.io/rust-clippy/main/index.html#unreadable_literal)


## `upper-case-acronyms-aggressive`
启用详细模式。若相邻有超过一个大写字符则触发

**默认值：** `false`

---
**受影响的 lint：**
* [`upper_case_acronyms`](https://rust-lang.github.io/rust-clippy/main/index.html#upper_case_acronyms)


## `vec-box-size-threshold`
在 `Vec` 中装箱的类型大小（字节），低于此值允许装箱

**默认值：** `4096`

---
**受影响的 lint：**
* [`vec_box`](https://rust-lang.github.io/rust-clippy/main/index.html#vec_box)


## `verbose-bit-mask-threshold`
在建议使用 `trailing_zeros` 之前位掩码允许的最大大小

**默认值：** `1`

---
**受影响的 lint：**
* [`verbose_bit_mask`](https://rust-lang.github.io/rust-clippy/main/index.html#verbose_bit_mask)


## `warn-on-all-wildcard-imports`
是否对所有通配符导入发出警告，包括来自 `prelude`、测试中来自 `super` 的，或 `pub use` 再导出。

**默认值：** `false`

---
**受影响的 lint：**
* [`wildcard_imports`](https://rust-lang.github.io/rust-clippy/main/index.html#wildcard_imports)


## `warn-unsafe-macro-metavars-in-private-macros`
是否也对**私有**宏中带有元变量展开的 `unsafe` 块发出警告。

**默认值：** `false`

---
**受影响的 lint：**
* [`macro_metavars_in_unsafe`](https://rust-lang.github.io/rust-clippy/main/index.html#macro_metavars_in_unsafe)
