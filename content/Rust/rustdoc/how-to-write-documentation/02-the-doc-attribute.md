+++
title = "02-#[doc] 属性"
date = 2026-08-01T07:35:00+08:00
weight = 42
type = "docs"
description = "#[doc] 属性的用法与选项"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# #[doc] 属性 {#the-doc-attribute}


> 原文链接: [https://doc.rust-lang.org/rustdoc/write-documentation/the-doc-attribute.html](https://doc.rust-lang.org/rustdoc/write-documentation/the-doc-attribute.html)


`#[doc]` 属性（attribute）让你控制 `rustdoc` 工作方式的多个方面。

`#[doc]` 最基本的功能是处理实际的文档文本。也就是说，`///` 是 `#[doc]` 的语法糖（`//!` 对应 `#![doc]`）。这意味着下面两者等价：

```rust,no_run
/// 这是一条文档注释。
#[doc = r" 这是一条文档注释。"]
# fn f() {}
```

（注意属性写法中前导空格与原始字符串字面量。）

多数情况下，`///` 比 `#[doc]` 更好用。后者更好用的一种情形是在宏中生成文档；`collapse-docs` 过程会把多个 `#[doc]` 属性合并成一条文档注释，从而可以生成这样的代码：

```rust,no_run
#[doc = "这是"]
#[doc = "一条"]
#[doc = "文档注释"]
# fn f() {}
```

这会显得更灵活。注意这会生成：

```rust,no_run
#[doc = "这是\n一条\n文档注释"]
# fn f() {}
```

但由于文档经 Markdown 渲染，这些换行会被去掉。

另一个用例是把外部文件包含为文档：

```rust,no_run
#[doc = include_str!("../../README.md")]
# fn f() {}
```

不过 `doc` 属性还有更多选项！它们不涉及输出文本本身，而是输出呈现的各个方面。下面分成两类：在 crate 级有用的属性，以及在项级有用的属性。

## 在 crate 级 {#at-the-crate-level}

这些选项控制文档在 crate 级的外观。

### `html_favicon_url` {#html-favicon-url}

这种形式的 `doc` 属性让你控制文档的 favicon。

```rust,no_run
#![doc(html_favicon_url = "https://example.com/favicon.ico")]
```

这会在文档中放入 `<link rel="icon" href="{}">`，属性字符串填入 `{}`。

若不使用该属性，会使用默认 favicon。

### `html_logo_url` {#html-logo-url}

这种形式的 `doc` 属性让你控制文档左上角的 logo。

```rust,no_run
#![doc(html_logo_url = "https://example.com/logo.jpg")]
```

这会在文档中放入 `<a href='../index.html'><img src='{}' alt='logo' width='100'></a>`，属性字符串填入 `{}`。

若不使用该属性，则没有 logo。

### `html_playground_url` {#html-playground-url}

这种形式的 `doc` 属性让你控制文档示例上「运行」按钮请求的目标。

```rust,no_run
#![doc(html_playground_url = "https://playground.example.com/")]
```

现在按下「运行」时，按钮会向该域名发请求。请求 URL 会包含 3 个查询参数：
1. `code`：文档中的代码
2. `version`：Rust 通道，例如 nightly，由 `code` 是否包含不稳定特性决定
3. `edition`：Rust edition，例如 2024

若不使用该属性，则没有运行按钮。

### `issue_tracker_base_url` {#issue-tracker-base-url}

这种形式的 `doc` 属性主要对标准库有用；当某个特性不稳定时，必须给出用于跟踪该特性的 issue 编号。`rustdoc` 用这个编号，加上此处给出的 base URL，链接到跟踪 issue。

```rust,no_run
#![doc(issue_tracker_base_url = "https://github.com/rust-lang/rust/issues/")]
```

### `html_root_url` {#html-root-url}

`#[doc(html_root_url = "…")]` 属性值指示生成指向外部 crate 链接时使用的 URL。当 rustdoc 需要生成指向外部 crate 中某项的链接时，会先检查该 extern crate 是否已在本地磁盘上生成文档，若有则直接链接。否则，若可用则使用 `--extern-html-root-url` 命令行标志给出的 URL。若也不可用，则使用该 extern crate 中的 `html_root_url`（若有）。若仍不可用，则不会为这些外部项生成链接。

```rust,no_run
#![doc(html_root_url = "https://docs.rs/serde/1.0")]
```

### `html_no_source` {#html-no-source}

默认情况下，`rustdoc` 会包含程序的源代码，并在文档中链接到它。但若包含：

```rust,no_run
#![doc(html_no_source)]
```

则不会。

### `test(no_crate_inject)` {#testno-crate-inject}

默认情况下，`rustdoc` 会自动在每个文档测试中加入一行 `extern crate my_crate;`。但若包含：

```rust,no_run
#![doc(test(no_crate_inject))]
```

则不会。

## 在项级 {#at-the-item-level}

这些形式的 `#[doc]` 属性用在单个项上，控制其文档方式。

### `inline` 与 `no_inline` {#inline-and-no-inline}

这些属性用在 `use` 语句上，控制文档出现在何处。例如，考虑这段 Rust 代码：

```rust,no_run
pub use bar::Bar;

/// bar 的文档
pub mod bar {
    /// Bar 的文档
    pub struct Bar;
}
# fn main() {}
```

文档会生成「Re-exports」小节，并显示 `pub use bar::Bar;`，其中 `Bar` 是指向其页面的链接。

若把 `use` 行改成这样：

```rust,no_run
#[doc(inline)]
pub use bar::Bar;
# pub mod bar { pub struct Bar; }
# fn main() {}
```

则 `Bar` 会出现在 `Structs` 小节中，就像 `Bar` 定义在顶层一样，而不是被 `pub use`。

再把原来的例子改成让 `bar` 为私有：

```rust,no_run
pub use bar::Bar;

/// bar 的文档
mod bar {
    /// Bar 的文档
    pub struct Bar;
}
# fn main() {}
```

这里因为 `bar` 不是公开的，`bar` 不会有自己的页面，也就无处可链。`rustdoc` 会内联这些定义，于是情况与上面的 `#[doc(inline)]` 相同；`Bar` 出现在 `Structs` 小节中，就像定义在顶层一样。若加上 `no_inline` 形式的属性：

```rust,no_run
#[doc(no_inline)]
pub use bar::Bar;

/// bar 的文档
mod bar {
    /// Bar 的文档
    pub struct Bar;
}
# fn main() {}
```

现在会有一行「Re-exports」，且 `Bar` 不会链接到任何地方。

一个特例：在 Rust 2018 及之后，若你 `pub use` 某个依赖，除非加上 `#[doc(inline)]`，否则 `rustdoc` 不会自动把它作为模块内联。

若想了解更多内联规则，请参阅[重导出](03-re-exports/)章节。

### `hidden` {#hidden}

标注了 `#[doc(hidden)]` 的项不会出现在文档中，除非使用了 [`--document-hidden-items`](../08-unstable-features/#document-hidden-items) 标志。

更多信息见[重导出](03-re-exports/)章节。

### `alias` {#alias}

该属性在搜索索引中添加别名。

来看一个例子：

```rust,no_run
#[doc(alias = "TheAlias")]
pub struct SomeType;
```

于是在搜索中输入 "TheAlias" 会显示 `SomeType`。当然，输入 `SomeType` 也会如预期返回 `SomeType`！

#### FFI 示例 {#ffi-example}

在为 C 库编写绑定时，这个文档属性尤其有用。例如，假设有这样一个 C 函数：

```c
int lib_name_do_something(Obj *obj);
```

它接受指向 `Obj` 类型的指针并返回整数。在 Rust 中可能写成：

```ignore (using non-existing ffi types)
pub struct Obj {
    inner: *mut ffi::Obj,
}

impl Obj {
    pub fn do_something(&mut self) -> i32 {
        unsafe { ffi::lib_name_do_something(self.inner) }
    }
}
```

该函数被改成了方法以便使用。但若你想查找 `lib_name_do_something` 的 Rust 等价物，却无从下手。

为绕过这一限制，只需在 `do_something` 方法上加上 `#[doc(alias = "lib_name_do_something")]` 即可！用户现在可以直接在我们的 crate 中搜索 `lib_name_do_something` 并找到 `Obj::do_something`。

### `test(attr(...))` {#testattr}

这种形式的 `doc` 属性允许你为所有文档测试添加任意属性。例如，若希望文档测试在存在死代码时失败，可以加：

```rust,no_run
#![doc(test(attr(deny(dead_code))))]

mod my_mod {
    #![doc(test(attr(allow(dead_code))))] // 但对该模块允许 `dead_code`
}
```

`test(attr(..))` 属性会追加到父模块的属性之后，而不是替换当前属性列表。在上例中，两个属性都会存在：

```rust,no_run
// 对 `my_mod` 中的每个文档测试

#![deny(dead_code)] // 来自 crate 根
#![allow(dead_code)] // 来自 `my_mod`
```
