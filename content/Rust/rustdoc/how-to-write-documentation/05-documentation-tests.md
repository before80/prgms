+++
title = "05-文档测试"
date = 2026-08-01T07:35:00+08:00
weight = 45
type = "docs"
description = "文档中的示例测试（doctest）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 文档测试 {#documentation-tests}


> 原文链接: [https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html](https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html)


`rustdoc` 支持把文档示例当作测试执行。这能确保文档中的示例是最新的且可运行。

基本思路如下：

```rust,no_run
/// # 示例
///
/// ```
/// let x = 5;
/// ```
# fn f() {}
```

这里，三个反引号开始并结束代码块。若这在名为 `foo.rs` 的文件中，运行 `rustdoc --test foo.rs` 会提取该示例，然后作为测试运行。

请注意：默认情况下，若代码块未设置语言，rustdoc 会假定它是 Rust 代码。因此下面：

``````markdown
```rust
let x = 5;
```
``````

严格等价于：

``````markdown
```
let x = 5;
```
``````

不过还有一些细微差别！请继续阅读了解更多细节。

## 文档测试的通过或失败 {#passing-or-failing-a-doctest}

与普通单元测试类似，常规文档测试在能编译且运行时不 panic 时视为「通过」。因此若要演示某次计算给出特定结果，`assert!` 系列宏与其他 Rust 代码用法相同：

```rust
let foo = "foo";
assert_eq!(foo, "foo");
```

这样，若计算返回不同结果，代码会 panic，文档测试失败。

## 预处理示例 {#pre-processing-examples}

在上面的例子中，你会注意到一件奇怪的事：没有 `main` 函数！强迫你为每个示例（无论多小）都写 `main` 会增加摩擦并弄乱输出。因此 `rustdoc` 在运行示例前会稍作处理。下面是 `rustdoc` 预处理示例的完整算法：

1. 插入一些常见的 `allow` 属性，包括 `unused_variables`、`unused_assignments`、`unused_mut`、`unused_attributes` 和 `dead_code`。小示例经常会触发这些 lint。
2. 加入通过 `#![doc(test(attr(...)))]` 指定的任何属性。
3. 任何前导的 `#![foo]` 属性保留为 crate 属性。
4. 若示例不含 `extern crate`，且未指定 `#![doc(test(no_crate_inject))]`，则插入 `extern crate <mycrate>;`（注意没有 `#[macro_use]`）。
5. 最后，若示例不含 `fn main`，则把剩余文本包在 `fn main() { your_code }` 中。

关于规则 4 的注意事项，见下文「为宏编写文档」。

## 隐藏示例的部分内容 {#hiding-portions-of-the-example}

有时你需要一些设置代码或其他会分散注意力但对测试运行很重要的内容。考虑如下示例块：

```rust,no_run
/// ```
/// /// 一些文档。
/// # fn foo() {} // 该函数会被隐藏
/// println!("Hello, World!");
/// ```
# fn f() {}
```

它会渲染成这样：

```rust
/// 一些文档。
# fn foo() {}
println!("Hello, World!");
```

没错：你可以添加以 `# ` 开头的行，它们会从输出中隐藏，但在编译代码时仍会使用。你可以善用这一点。在本例中，文档注释需要附着在某种函数上，因此若只想展示文档注释，需要在下面加一个小函数定义。同时它只是为了让编译器满意，隐藏它能让示例更清晰。你可以用这种技巧详细解释较长示例，同时仍保持文档的可测试性。

例如，假设我们想为这段代码写文档：

```rust
let x = 5;
let y = 6;
println!("{}", x + y);
```

我们可能希望文档最终看起来像这样：

> 首先，把 `x` 设为五：
>
> ```rust
> let x = 5;
> # let y = 6;
> # println!("{}", x + y);
> ```
>
> 接着，把 `y` 设为六：
>
> ```rust
> # let x = 5;
> let y = 6;
> # println!("{}", x + y);
> ```
>
> 最后，打印 `x` 与 `y` 的和：
>
> ```rust
> # let x = 5;
> # let y = 6;
> println!("{}", x + y);
> ```

为保持每个代码块可测试，我们希望每个块中都有完整程序，但不希望读者每次都看到每一行。源码中应这样写：

``````markdown
首先，把 `x` 设为五：

```
let x = 5;
# let y = 6;
# println!("{}", x + y);
```

接着，把 `y` 设为六：

```
# let x = 5;
let y = 6;
# println!("{}", x + y);
```

最后，打印 `x` 与 `y` 的和：

```
# let x = 5;
# let y = 6;
println!("{}", x + y);
```
``````

通过重复示例的所有部分，你可以确保示例仍能编译，同时只显示与该段说明相关的部分。

用两个连续的井号 `##` 可以阻止 `#` 隐藏行。只需对原本会导致隐藏的第一个 `#` 这样做。若有如下字符串字面量，其中一行以 `#` 开头：

```rust
let s = "foo
## bar # baz";
```

可以通过转义初始的 `#` 来写文档：

```text
/// let s = "foo
/// ## bar # baz";
```

下面是一个宏规则匹配以 `#` 开头的 token 的例子：

`````rust,no_run
/// ```
/// macro_rules! ignore { (##tag) => {}; }
/// ignore! {
///     ###tag
/// }
/// ```
# fn f() {}
`````

可以看到，该规则期望两个 `#`，因此调用时需要再加一个 `#`，因为第一个用作转义。

## 在文档测试中使用 `?` {#using-in-doc-tests}

写示例时，很少有必要包含完整的错误处理，因为那会增加大量样板代码。相反，你可能想要下面这样：

```rust,no_run
/// ```
/// use std::io;
/// let mut input = String::new();
/// io::stdin().read_line(&mut input)?;
/// ```
# fn f() {}
```

问题在于 `?` 返回 `Result<T, E>`，而测试函数不返回任何值，因此会得到类型不匹配错误。

可以通过手动添加返回 `Result<T, E>` 的 `main` 来绕过这一限制，因为 `Result<T, E>` 实现了 `Termination` trait：

```rust,no_run
/// 使用 ? 的文档测试
///
/// ```
/// use std::io;
///
/// fn main() -> io::Result<()> {
///     let mut input = String::new();
///     io::stdin().read_line(&mut input)?;
///     Ok(())
/// }
/// ```
# fn f() {}
```

再结合上一节的 `# `，就能得到对读者看起来像最初想法、但又能通过文档测试的方案：

```rust,no_run
/// ```
/// use std::io;
/// # fn main() -> io::Result<()> {
/// let mut input = String::new();
/// io::stdin().read_line(&mut input)?;
/// # Ok(())
/// # }
/// ```
# fn f() {}
```

从 1.34.0 版起，也可以省略 `fn main()`，但需要消歧错误类型：

```rust,no_run
/// ```
/// use std::io;
/// let mut input = String::new();
/// io::stdin().read_line(&mut input)?;
/// # Ok::<(), io::Error>(())
/// ```
# fn f() {}
```

这是 `?` 运算符会加入隐式转换的不幸后果，因此类型推断因类型不唯一而失败。请注意必须把 `(())` 连写、中间不加空白，这样 `rustdoc` 才明白你想要隐式返回 `Result` 的函数。

## 在文档测试中显示警告 {#showing-warnings-in-doctests}

可以通过运行 `rustdoc --test --test-args=--show-output`（若使用 cargo，则为 `cargo test --doc -- --show-output`）在文档测试中显示警告。默认仍会隐藏 `unused` 警告，因为许多示例使用私有函数；若想看到未使用变量或死代码警告，可在示例顶部加 `#![warn(unused)]`。也可以在 crate 根使用 [`#![doc(test(attr(warn(unused))))]`][test-attr] 全局启用警告。

[test-attr]: 02-the-doc-attribute/#testattr

## 为宏编写文档 {#documenting-macros}

下面是为宏编写文档的例子：

```rust
/// 除非表达式求值为 true，否则以给定消息 panic。
///
/// # 示例
///
/// ```
/// # #[macro_use] extern crate foo;
/// # fn main() {
/// panic_unless!(1 + 1 == 2, “Math is broken.”);
/// # }
/// ```
///
/// ```should_panic
/// # #[macro_use] extern crate foo;
/// # fn main() {
/// panic_unless!(true == false, “I’m broken.”);
/// # }
/// ```
#[macro_export]
macro_rules! panic_unless {
    ($condition:expr, $($rest:expr),+) => ({ if ! $condition { panic!($($rest),+); } });
}
# fn main() {}
```

你会注意到三件事：我们需要自己加 `extern crate` 行，以便加上 `#[macro_use]` 属性。其次，我们也需要自己加 `main()`（原因见上文）。最后，审慎地用 `#` 注释掉这两处，使它们不出现在输出中。

## 属性 {#attributes}

代码块可以用属性标注，告诉 `rustdoc` 如何构建和解释测试。它们跟在开头行的[代码围栏][code fence]之后。因此它们与 `rust` 或 `text` 等语言字符串共用同一位置。多个属性可用逗号、空格或制表符分隔。也可以写括在 `(…)` 中的注释。

正如开篇所暗示的，除非你指定 `rust` 或某个不是属性的内容（`custom` 除外），否则代码块会被假定为 Rust 源代码（并按此做语法高亮）。

当然你也可以显式加上 `rust`（例如 `rust,ignore`），若 Markdown 也会被其他工具消费（例如通过 `include_str` 包含的 `README.md`）。

### `ignore` {#ignore}

`ignore` 属性告诉 `rustdoc` 忽略你的代码。若希望有 Rust 语法高亮，但片段不完整或是伪代码，这很有用。习惯上在 `(…)` 注释中说明为何应忽略。

```rust
/// ```ignore
/// fn foo() {
/// ```
///
/// ```ignore (需要额外依赖)
/// use dependency::functionality;
/// functionality();
/// ```
# fn foo() {}
```

请注意，这几乎从不是你想要的，因为它过于宽泛。相反，若不是代码，可标为 `text`；或者用 `#` 得到一个可运行、只显示你关心部分的示例。

### `should_panic` {#should-panic}

`should_panic` 告诉 `rustdoc` 代码应能正确编译，但在执行时 panic。若不 panic，测试会失败。

```rust
/// ```should_panic
/// assert!(false);
/// ```
# fn foo() {}
```

### `no_run` {#no-run}

`no_run` 属性会编译代码但不运行它。这对诸如「如何获取网页」这类示例很重要：你希望确保能编译，但测试环境可能没有网络访问。该属性也可用于演示可能导致未定义行为的代码片段。

```rust
/// ```no_run
/// loop {
///     println!("Hello, world");
/// }
/// ```
# fn foo() {}
```

### `compile_fail` {#compile-fail}

`compile_fail` 告诉 `rustdoc` 编译应当失败。若能编译，则测试失败。

```rust
/// ```compile_fail
/// let x = 5;
/// x += 2; // 不应编译！
/// ```
# fn foo() {}
```

<div class="warning">
不过请注意：用当前 Rust 发行版会编译失败的代码，在未来发行版中可能成功，因为会加入新特性！
</div>

### `edition…` {#edition}

`edition2015`、`edition2018`、`edition2021` 和 `edition2024` 告诉 `rustdoc` 应使用相应的 Rust edition 编译代码样例。

```rust
/// 仅在 2018 edition 上运行。
///
/// ```edition2018
/// let result: Result<i32, ParseIntError> = try {
///     "1".parse::<i32>()?
///         + "2".parse::<i32>()?
///         + "3".parse::<i32>()?
/// };
/// ```
# fn foo() {}
```

### `standalone_crate` {#standalone-crate}

从 2024 edition[^edition-note] 起，兼容的文档测试在运行前会合并为一个。合并文档测试是出于性能：文档测试最慢的部分是编译。把它们全部合并到一个文件并编译，再运行文档测试会快得多。无论是否合并，文档测试都在各自的进程中运行。

运行文档测试时耗时的一个例子：

[sysinfo crate](https://crates.io/crates/sysinfo)：

```text
wall-time duration: 4.59s
total compile time: 27.067s
total runtime: 3.969s
```

Rust 核心库：

```text
wall-time duration: 102s
total compile time: 775.204s
total runtime: 15.487s
```

[^edition-note]: 这基于整个 crate 的 edition，而不是可能在代码属性中为单个测试用例指定的 edition。

在某些情况下，文档测试无法合并。例如，若你有：

```rust
//! ```
//! let location = std::panic::Location::caller();
//! assert_eq!(location.line(), 4);
//! ```
```

这段代码的问题是：若你改动任何其他文档测试，运行 `rustdoc --test` 时很可能失败，维护起来很棘手。

这就是 `standalone_crate` 属性的用处：它告诉 `rustdoc` 某个文档测试不应与其他合并。因此前面的代码应这样用：

```rust
//! ```standalone_crate
//! let location = std::panic::Location::caller();
//! assert_eq!(location.line(), 4);
//! ```
```

这种情况下，即使增删其他文档测试，行号信息也不会改变。

### `ignore-…`：忽略目标 {#ignore-ignoring-targets}

以 `ignore-` 开头的属性可用于对特定目标忽略文档测试。例如，`ignore-x86_64` 会在目标名包含 `x86_64` 时避免构建文档测试。

```rust
/// ```ignore-x86_64
/// assert!(2 == 2);
/// ```
struct Foo;
```

该文档测试不会为诸如 `x86_64-unknown-linux-gnu` 的目标构建。

可以指定多个 ignore 属性以忽略多个目标：

```rust
/// ```ignore-x86_64,ignore-windows
/// assert!(2 == 2);
/// ```
struct Foo;
```

若要为较旧的 rustdoc 版本保持向后兼容，可以同时指定 `ignore` 和 `ignore-`，例如：

```rust
/// ```ignore,ignore-x86_64
/// assert!(2 == 2);
/// ```
struct Foo;
```

在较旧版本中，这会在所有目标上被忽略；但从 1.88.0 起，`ignore-x86_64` 会覆盖 `ignore`。

### `{…}` 与 `custom`：代码块的自定义 CSS 类 {#custom-custom-css-classes-for-code-blocks}

```rust
/// ```custom,{class=language-c}
/// int main(void) { return 0; }
/// ```
pub struct Bar;
```

文本 `int main(void) { return 0; }` 会在带有 `language-c` 类的代码块中无高亮地渲染。这可用于例如通过 JavaScript 库高亮其他语言。

没有 `custom` 属性时，它会生成为带有额外 `language-C` CSS 类的 Rust 代码示例。因此，若特别不希望它是 Rust 代码示例，别忘了加上 `custom` 属性。

另请注意，可以用 `.` 代替 `class=` 达到相同效果：

```rust
/// ```custom,{.language-c}
/// int main(void) { return 0; }
/// ```
pub struct Bar;
```

另请注意，`rust` 与 `{.rust}` / `{class=rust}` 效果不同：`rust` 表示这是 Rust 代码块，而后两者会在生成 HTML 的代码块上添加 "rust" CSS 类。

也可以使用双引号：

```rust
/// ```"not rust" {."hello everyone"}
/// int main(void) { return 0; }
/// ```
pub struct Bar;
```

### `test_harness` {#test-harness}

应用 `test_harness` 后，`rustdoc` 会运行其中包含的*测试函数*，而不是（可能隐式的）`main` 函数。

```rust
//! ```test_harness
//! #[test]
//! #[should_panic]
//! fn abc() { assert!(false); }
//!
//! #[test]
//! fn xyz() { assert!(true); }
//! ```
```

关于*测试函数*的更多内容，见[《The Book》][testing-book]或[《The Rust Reference》][testing-ref]。

[testing-book]: https://doc.rust-lang.org/book/ch11-01-writing-tests.html
[testing-ref]: https://doc.rust-lang.org/reference/attributes/testing.html

## 语法参考 {#syntax-reference}

代码块的*确切*语法（包括边界情况）见 CommonMark 规范的 [Fenced Code Blocks] 一节。

Rustdoc 也接受*缩进*代码块作为围栏代码块的替代：不必用[代码围栏][code fence]（例如三个反引号）包围代码，可以把每行缩进四个或更多空格。

``````markdown
    let foo = "foo";
    assert_eq!(foo, "foo");
``````

这些同样记录在 CommonMark 规范的 [Indented Code Blocks] 一节。

不过，更推荐使用围栏代码块而不是缩进代码块。围栏代码块不仅被认为更符合 Rust 代码习惯，而且缩进代码块无法使用 `ignore` 或 `should_panic` 等属性。

### 仅在收集文档测试时包含项 {#include-items-only-when-collecting-doctests}

Rustdoc 的文档测试能做一些普通单元测试做不到的事，因此有时用本来不必出现在文档中的样例扩展文档测试会很有用。为此，Rustdoc 允许某些项仅在收集文档测试时出现，这样你就能利用文档测试功能，而不必强迫测试出现在文档中，或找一个任意的私有项来挂载。

为文档测试编译 crate（带 `--test` 选项）时，`rustdoc` 会设置 `#[cfg(doctest)]`。注意它们仍只会链接到 crate 的公开项；若需要测试私有项，需要写单元测试。

在本例中，我们添加已知无法编译的文档测试，以验证我们的结构体只能接受有效数据：

```rust
/// 这里有一个结构体。请记住它不接受负数！
pub struct MyStruct(pub usize);

/// ```compile_fail
/// let x = my_crate::MyStruct(-5);
/// ```
#[cfg(doctest)]
pub struct MyStructOnlyTakesUsize;
```

注意这里的结构体 `MyStructOnlyTakesUsize` 实际上不是公开 crate API 的一部分。使用 `#[cfg(doctest)]` 确保该结构体仅在 `rustdoc` 收集文档测试时存在。这意味着当向 rustdoc 传入 `--test` 时会执行其文档测试，但对公开文档隐藏。

`#[cfg(doctest)]` 的另一个可能用途是测试包含在 README 中的文档测试，而不把它放进主文档。例如，你可以在 `lib.rs` 中这样写，把 README 作为文档测试的一部分来测：

```rust,no_run
#[doc = include_str!("../README.md")]
#[cfg(doctest)]
pub struct ReadmeDoctests;
```

这会把 README 作为隐藏结构体 `ReadmeDoctests` 上的文档包含进来，然后与其余文档测试一起测试。

## 控制编译与运行目录 {#controlling-the-compilation-and-run-directories}

默认情况下，`rustdoc --test` 会从同一工作目录编译并运行文档测试示例。编译目录用于编译器诊断、`file!()` 宏以及 `rustdoc` 测试运行器本身的输出，而运行目录会影响文档测试示例内的文件系统操作，例如 `std::fs::read_to_string`。

`--test-run-directory` 标志允许将运行目录与编译目录分开控制。这在 workspace 中尤其有用：编译器调用及诊断应相对于 workspace 目录，而文档测试示例应相对于 crate 目录运行。


[code fence]: https://spec.commonmark.org/0.29/#code-fence
[Fenced Code Blocks]: https://spec.commonmark.org/0.29/#fenced-code-blocks
[Indented Code Blocks]: https://spec.commonmark.org/0.29/#indented-code-blocks
