+++
title = "08-不稳定特性"
date = 2026-08-01T07:35:00+08:00
weight = 80
type = "docs"
description = "rustdoc 的不稳定（nightly）特性"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 不稳定特性 {#unstable-features}


> 原文链接: [https://doc.rust-lang.org/rustdoc/unstable-features.html](https://doc.rust-lang.org/rustdoc/unstable-features.html)


Rustdoc 仍在积极开发中，与 Rust 编译器类似，有些功能仅在 nightly 版本中可用。其中一部分是新功能，需要更多测试才能广泛发布；另一部分则与编译器中的不稳定特性绑定。此处若干特性需要匹配的 `#![feature(...)]` 属性才能启用，因此在 [不稳定手册（Unstable Book）][Unstable Book] 中有更完整的文档。相关小节会在必要时链接到该手册。

[Unstable Book]: https://doc.rust-lang.org/unstable-book/

## Nightly 门控功能 {#nightly-gated-functionality}

这些功能只需 nightly 构建即可使用。与本页其他特性不同，它们无需通过命令行标志或 crate 中的 `#![feature(...)]` 属性来“开启”。这使它们在稳定版上使用时可能出现一些不易察觉的回退行为，请务必小心！

### `compile-fail` 文档测试的错误编号 {#error-numbers-for-compile-fail-doctests}

如[文档测试一章][doctest-attributes]所述，可为文档测试添加 `compile_fail` 属性，表示该测试应编译失败。而在 nightly 上，还可以可选地附上错误编号，表明文档测试应发出特定错误码：

[doctest-attributes]: how-to-write-documentation/05-documentation-tests/#attributes

``````markdown
```compile_fail,E0044
extern { fn some_func<T>(x: T); }
```
``````

错误索引（error index）用它来确保与给定错误编号对应的示例确实会发出该错误码。不过，这些错误码并不保证是某段代码在各个版本之间发出的唯一内容，因此该功能未来不太可能稳定化。

若在稳定版上尝试使用这些错误编号，代码示例会被当作纯文本处理。

### `missing_doc_code_examples` lint {#missing_doc_code_examples-lint}

若某个项的文档中没有代码示例，此 lint 会发出警告。可通过以下方式启用：

```rust,ignore (nightly)
#![deny(rustdoc::missing_doc_code_examples)]
```

对于无法实例化/调用的项，不会发出该警告，例如字段、变体、模块、关联的 trait/impl 项、impl 块、静态项与常量。对外项（foreign items）、别名、`extern crate` 与导入也不会发出。

## `#[doc]` 属性的扩展 {#extensions-to-the-doc-attribute}

这些特性通过扩展 `#[doc]` 属性生效，因此可被编译器识别，并在 crate 中用 `#![feature(...)]` 属性启用。

### 将你的 trait 加入「Notable traits」对话框 {#adding-your-trait-to-the-notable-traits-dialog}

 * 跟踪议题（Tracking issue）：[#45040](https://github.com/rust-lang/rust/issues/45040)

Rustdoc 维护了一份被认为对其实现者“基础（fundamental）”的少量 trait 列表。这些 trait 意在作为其实现者的主要接口，且往往构成可在其类型上文档化的大部分 API。因此，当某个类型实现了这些 trait 之一时，Rustdoc 会加以跟踪；当函数返回这类类型时，会特别提示。这就是「Notable traits」对话框——函数旁带圆圈的 `i` 按钮，点击后显示该对话框。

在标准库中，该列表包含的部分 trait 有 `Iterator`、`Future`、`io::Read` 与 `io::Write`。不过，它们并非硬编码列表，而是带有特殊标记属性：`#[doc(notable_trait)]`。这意味着你也可以把该属性应用到自己的 trait 上，使其出现在文档的「Notable traits」对话框中。

除「Notable traits」对话框外，每个实现了 `#[doc(notable_trait)]` trait 的类型，会在其页面顶部为该 trait 渲染彩色徽章，浏览类型时便于一眼看出关系。

`#[doc(notable_trait)]` 属性目前需要 `#![feature(doc_notable_trait)]` 特性门。更多信息见[不稳定手册中的对应章节][unstable-notable_trait]及其[跟踪议题][issue-notable_trait]。

[unstable-notable_trait]: https://doc.rust-lang.org/unstable-book/language-features/doc-notable-trait.html
[issue-notable_trait]: https://github.com/rust-lang/rust/issues/45040

### 从文档中排除某些依赖 {#exclude-certain-dependencies-from-documentation}

 * 跟踪议题：[#44027](https://github.com/rust-lang/rust/issues/44027)

标准库使用了若干依赖，而这些依赖又使用了标准库中的多种类型与 trait。此外，还有一些编译器内部 crate 不被视为正式标准库的一部分，若纳入文档会造成干扰。仅排除其 crate 文档不够，因为 trait 实现信息会出现在类型页与 trait 页上，而这两者可能分属不同 crate！

为防止内部类型出现在文档中，标准库在其 `extern crate` 声明上添加了属性：`#[doc(masked)]`。这会使 Rustdoc 在构建 trait 实现列表时“遮蔽（mask out）”来自这些 crate 的类型。

`#[doc(masked)]` 属性面向内部使用，并需要 `#![feature(doc_masked)]` 特性门。更多信息见[不稳定手册中的对应章节][unstable-masked]及其[跟踪议题][issue-masked]。

[unstable-masked]: https://doc.rust-lang.org/unstable-book/language-features/doc-masked.html
[issue-masked]: https://github.com/rust-lang/rust/issues/44027

### 为原始类型编写文档 {#document-primitives}

仅供 Rust 编译器内部使用。

由于原始类型（primitive types）在编译器中定义，没有地方可挂文档属性。标准库使用 `#[rustc_doc_primitive = "..."]` 属性为原始类型生成文档，并需要 `#![feature(rustc_attrs)]` 才能启用。

### 为关键字编写文档 {#document-keywords}

仅供标准库内部使用。

Rust 关键字在标准库中有文档（例如可查找 `match`）。

为此使用 `#[doc(keyword = "...")]` 属性。示例：

```rust
#![feature(rustdoc_internals)]
#![allow(internal_features)]

/// 关于该关键字的一些文档。
#[doc(keyword = "break")]
mod empty_mod {}
```

### 为内置属性编写文档 {#document-builtin-attributes}

仅供标准库内部使用。

Rust 内置属性在标准库中有文档（例如可查找 `repr`）。

为此使用 `#[doc(attribute = "...")]` 属性。示例：

```rust
#![feature(rustdoc_internals)]
#![allow(internal_features)]

/// 关于该属性的一些文档。
#[doc(attribute = "repr")]
mod empty_mod {}
```

### 使用 Rust logo 作为 crate logo {#use-the-rust-logo-as-the-crate-logo}

仅供官方 Rust 项目使用。

内部 Rustdoc 页面（如 settings.html 与 scrape-examples-help.html）会显示 Rust logo。该 logo 作为静态资源跟踪。属性 `#![doc(rust_logo)]` 可使同一内置资源作为主 logo。

```rust
#![feature(rustdoc_internals)]
#![allow(internal_features)]
#![doc(rust_logo)]
//! 此 crate 带有 Rust(tm) 品牌标识。
```

## 其他 nightly 特性的影响 {#effects-of-other-nightly-features}

这些仅 nightly 可用的特性并非主要面向 Rustdoc，但对生成的文档有便利影响。

### `fundamental` 类型 {#fundamental-types}

用 `#[fundamental]` 标注类型主要影响泛型类型的一致性（coherence）规则，即改变其他 crate 能否为该类型提供实现。不稳定手册中有[进一步信息的链接][unstable-fundamental]。

[unstable-fundamental]: https://doc.rust-lang.org/unstable-book/language-features/fundamental.html

对文档而言，这还有额外副作用：若方法实现在 `F<T>`（或 `F<&T>`）上，且 `F` 是 fundamental 类型，则该方法不仅会出现在 `F` 的文档页上，也会出现在 `T` 的文档页上。某种意义上，这使类型对 Rustdoc 变得透明。对用作带注解指针的类型（如 `Pin<&mut T>`）尤其方便，可确保仅通过这些带注解指针实现的方法，仍能在其作用的类型上被找到。

若并不希望 `fundamental` 特性影响一致性，可将该类型仅在为文档构建时标为 fundamental：引入自定义特性，并限制仅在构建文档时使用 `fundamental`。

## 不稳定的命令行参数 {#unstable-command-line-arguments}

这些特性通过向 Rustdoc 传入命令行标志启用，但相关标志本身被标为不稳定。要使用其中任一选项，需同时向 Rustdoc 命令行传入 `-Z unstable-options` 与该标志。从 Cargo 使用时，可通过 `RUSTDOCFLAGS` 环境变量或 `cargo rustdoc` 命令实现。

### `--write-doc-meta-dir` 与 `--read-doc-meta-dir` {#--write-doc-meta-dir-and---read-doc-meta-dir}

这些选项控制 rustdoc 如何处理合并多个 crate 数据的文件。

默认情况下，rustdoc 会从文档输出目录本身读取文档元数据并合并。这对手动调用 rustdoc 的脚本很方便，但也很慢，因为它对每个 crate 做 O(crates) 工作，总计 O(crates<sup>2</sup>)。提供 `--write-doc-meta-dir` 和/或 `--read-doc-meta-dir` 时，该默认行为会关闭。

提供 `--write-doc-meta-dir` 时，rustdoc 会将该 crate 的元数据写入该目录。若只提供此参数而未提供 `--read-doc-meta-dir`，则运行于*中间模式（intermediate mode）*：部分页面可能写入输出目录，但许多功能要等到 rustdoc 以*定稿模式（finalize mode）*运行后才会生效。

提供 `--read-doc-meta-dir` 时，rustdoc 以*定稿模式*运行。它会从给定目录读取数据，并以 Web 前端所用形式写入文档输出目录。

若同时指定 `--write-doc-meta-dir` 与 `--read-doc-meta-dir`，crate 元数据会同时写入 HTML `--out-dir` 与所提供的 `--write-doc-meta-dir`。

```console
$ rustdoc crate1.rs --out-dir=doc
$ cat doc/search.index/crateNames/*
rd_("fcrate1")
$ rustdoc crate2.rs --out-dir=doc
$ cat doc/search.index/crateNames/*
rd_("fcrate1fcrate2")
```

为将共享数据的合并推迟到构建末尾，从而只需做 O(crates) 工作，可对每个 crate 使用 `--write-doc-meta-dir`，最后一个再使用 `--read-doc-meta-dir`。

```console
$ rustdoc +nightly crate1.rs --write-doc-meta=crate1.d -Zunstable-options
$ cat doc/search.index/crateNames/*
cat: 'doc/search.index/crateNames/*': No such file or directory
$ rustdoc +nightly crate2.rs --read-doc-meta=crate1.d -Zunstable-options
$ cat doc/search.index/crateNames/*
rd_("fcrate1fcrate2")
```

### `--document-hidden-items`：显示带有 `#[doc(hidden)]` 的项 {#document-hidden-items}

默认情况下，`rustdoc` 不会为标注了 [`#[doc(hidden)]`](how-to-write-documentation/02-the-doc-attribute/#hidden) 的项生成文档。

`--document-hidden-items` 会使所有项都像没有 `#[doc(hidden)]` 一样被文档化，但隐藏项会以 👻 图标显示。

下表完整说明了 `--document-hidden-items` 与 `--document-private-items` 各种组合下会文档化哪些项：


| rustdoc 标志                         | 会被文档化的项                     |
|--------------------------------------|------------------------------------|
| 两个标志都不用                       | 仅非隐藏的公有项                   |
| 仅 `--document-hidden-items`         | 所有公有项                         |
| 仅 `--document-private-items`        | 所有非隐藏项                       |
| 两个标志都用                         | 所有项                             |


### `--markdown-before-content`：在内容前插入渲染后的 Markdown {#--markdown-before-content-include-rendered-markdown-before-the-content}

 * 跟踪议题：[#44027](https://github.com/rust-lang/rust/issues/44027)

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --markdown-before-content extra.md
$ rustdoc README.md -Z unstable-options --markdown-before-content extra.md
```

与 `--html-before-content` 类似，这允许你在 `<body>` 标签内、在 `rustdoc` 通常生成的其他内容之前插入额外内容。不过，文件不会原样直接插入，而是先经过 Markdown 渲染器，再将结果插入文件。

### `--markdown-after-content`：在内容后插入渲染后的 Markdown {#--markdown-after-content-include-rendered-markdown-after-the-content}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --markdown-after-content extra.md
$ rustdoc README.md -Z unstable-options --markdown-after-content extra.md
```

与 `--html-after-content` 类似，这允许你在 `</body>` 标签之前、在 `rustdoc` 通常生成的其他内容之后插入额外内容。不过，文件不会原样直接插入，而是先经过 Markdown 渲染器，再将结果插入文件。

### `--playground-url`：控制 playground 的位置 {#--playground-url-control-the-location-of-the-playground}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --playground-url https://play.rust-lang.org/
```

在渲染 crate 文档时，该标志给出 Rust Playground 的基础 URL，用于生成 `Run` 按钮。与 `--markdown-playground-url` 不同，该参数对独立 Markdown 文件*与* Rust crate 都有效。其作用方式与在 crate 根添加 `#![doc(html_playground_url = "url")]` 相同，见 [`#[doc]` 属性一章][doc-playground]。请注意，官方 Rust Playground（https://play.rust-lang.org）并非包含所有 crate，因此若示例依赖你的 crate，请确保所提供的 playground 上有该 crate。

[doc-playground]: how-to-write-documentation/02-the-doc-attribute/#html_playground_url

若渲染独立 Markdown 文件时同时存在 `--playground-url` 与 `--markdown-playground-url`，则以 `--markdown-playground-url` 给出的 URL 为准。若渲染 crate 文档时同时存在 `--playground-url` 与 `#![doc(html_playground_url = "url")]`，则以属性为准。

## `--sort-modules-by-appearance`：控制模块页上项的排序 {#--sort-modules-by-appearance-control-how-items-on-module-pages-are-sorted}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --sort-modules-by-appearance
```

通常，`rustdoc` 在模块页打印项时会按字母排序（并会考虑稳定性，以及以数字结尾的名称）。向 `rustdoc` 传入此标志会禁用该排序，改为按项在源码中出现的顺序打印。

## `--show-type-layout`：在每个类型的文档中增加描述其内存布局的小节 {#--show-type-layout-add-a-section-to-each-types-docs-describing-its-memory-layout}

 * 跟踪议题：[#113248](https://github.com/rust-lang/rust/issues/113248)

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --show-type-layout
```

传入此标志时，rustdoc 会在每个类型文档页底部增加「Layout」小节，包含 rustc 计算出的该类型内存布局摘要。例如，rustdoc 会显示该类型的值在内存中占用的字节大小。

注意：大多数布局信息**完全不稳定**，甚至可能在不同编译之间有所不同。

## `--resource-suffix`：修改 crate 文档中 CSS/JavaScript 的文件名 {#--resource-suffix-modifying-the-name-of-cssjavascript-in-crate-docs}

 * 跟踪议题：[#54765](https://github.com/rust-lang/rust/issues/54765)

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --resource-suffix suf
```

渲染文档时，`rustdoc` 会在输出中创建若干 CSS 与 JavaScript 文件。由于每个页面都会链接这些文件，若需要特殊缓存它们，更改其位置会很麻烦。此标志会在输出中重命名所有这些文件，在文件名中加入后缀。例如，使用上述命令时，`light.css` 会变成 `light-suf.css`。

## `--extern-html-root-url`：控制 rustdoc 如何链接到非本地 crate {#--extern-html-root-url-control-how-rustdoc-links-to-non-local-crates}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --extern-html-root-url some-crate=https://example.com/some-crate/1.0.1
```

通常，当 rustdoc 要链接到来自不同 crate 的类型时，会查看两处：输出目录中已有的文档，或其他 crate 中设置的 `#![doc(html_root_url)]`。若要链接到这两处都不存在的文档，可用这些标志控制该行为。当 `--extern-html-root-url` 的名称与某个依赖匹配时，rustdoc 会对该文档使用该 URL。请注意，若输出目录中已有这些文档，本地文档仍会覆盖此标志。

此标志中的名称首先与 `--extern name=` 标志给出的名称匹配，从而可在同名多个 crate（例如同一 crate 的多个版本）之间选择。对于尚未通过 `--extern` 标志加载的传递依赖，匹配会回退为仅使用 crate 名称，无法区分同名的多个 crate。

## `-Z force-unstable-if-unmarked` {#-z-force-unstable-if-unmarked}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z force-unstable-if-unmarked
```

这是面向标准库与编译器的内部标志：对任何没有其他稳定性属性的依赖 crate 应用 `#[unstable]` 属性。这样 `rustdoc` 才能为编译器 crate 与标准库生成文档，因为构建这些 crate 时会向 `rustc` 提供等价的命令行参数。

## `--index-page`：为文档提供顶层落地页 {#--index-page-provide-a-top-level-landing-page-for-docs}

此特性允许你用给定的 markdown 文件生成索引页。一个很好的例子是 [Rust 文档索引](https://doc.rust-lang.org/nightly/index.html)。

有了它，你可以在各个 crate 文档的顶部拥有一个可任意定制的页面。

使用 `index-page` 选项也会启用 `enable-index-page` 选项。

## `--enable-index-page`：为文档生成默认索引页 {#--enable-index-page-generate-a-default-index-page-for-docs}

此特性允许生成默认索引页，其中列出已生成的各个 crate。

## `--no-capture`：禁用测试的输出捕获 {#--no-capture-disable-output-capture-for-test}

与 `--test` 一起使用此标志时，测试的输出（stdout 与 stderr）不会被 rustdoc 捕获，而是直接输出到终端，如同手动运行测试可执行文件一样。这对调试测试尤其有用！

## `--check`：仅检查文档 {#--check-only-checks-the-documentation}

提供此标志时，rustdoc 会对代码进行类型检查与 lint，但不会生成任何文档，也不会运行文档测试。

使用方式如下：

```bash
rustdoc -Z unstable-options --check src/lib.rs
```

## `--static-root-path`：控制 HTML 输出中静态文件的加载方式 {#--static-root-path-control-how-static-files-are-loaded-in-html-output}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --static-root-path '/cache/'
```

此标志控制 rustdoc 在 HTML 页面中如何链接其静态文件。若你托管大量由同一版本 rustdoc 生成的 crate 文档，可用此标志将 rustdoc 的 CSS、JavaScript 与字体文件缓存在单一位置，而不必在每个“文档根”（doc root，即生成到同一输出目录的一组 crate 文档，如 `cargo doc`）中重复一份。每个 crate 自身的文件（如搜索索引）仍从文档根加载，但经 `--resource-suffix` 重命名的任何内容会从给定路径加载。

## `--persist-doctests`：运行后保留文档测试可执行文件 {#--persist-doctests-persist-doctest-executables-after-running}

 * 跟踪议题：[#56925](https://github.com/rust-lang/rust/issues/56925)

使用该标志如下：

```bash
$ rustdoc src/lib.rs --test -Z unstable-options --persist-doctests target/rustdoctest
```

此标志允许在文档测试编译或运行后保留其可执行文件。通常，rustdoc 在测试完成后会立即丢弃已编译的文档测试；使用此选项可保留这些二进制文件以便进一步测试。

## `--show-coverage`：计算带有文档的项所占百分比 {#--show-coverage-calculate-the-percentage-of-items-with-documentation}

 * 跟踪议题：[#58154](https://github.com/rust-lang/rust/issues/58154)

使用该标志如下：

```bash
$ rustdoc src/lib.rs -Z unstable-options --show-coverage
```

它会生成类似如下的内容：

```bash
+-------------------------------------+------------+------------+------------+------------+
| File                                | Documented | Percentage |   Examples | Percentage |
+-------------------------------------+------------+------------+------------+------------+
| lib.rs                              |          4 |     100.0% |          1 |      25.0% |
+-------------------------------------+------------+------------+------------+------------+
| Total                               |          4 |     100.0% |          1 |      25.0% |
+-------------------------------------+------------+------------+------------+------------+
```

若想了解 crate 中有多少项已编写文档，可将此标志传给 rustdoc。收到此标志后，它会统计你的 crate 中带有文档的公有项，并打印计数与百分比，而不是生成文档。

关于 rustdoc 在此指标中如何计数的若干说明：

* Rustdoc 只会统计来自你的 crate 的项（即从其他 crate 重导出的项不计入）。
* 直接写在固有 impl 块上的文档不计入，尽管其文档注释会显示——因为 Rust 代码中的常见模式是将所有固有方法写在同一 impl 块中。
* trait 实现中的项不计入，因为这些 impl 会继承 trait 本身的文档。
* 默认仅统计公有项。若要同时统计私有项，请同时传入 `--document-private-items`。

未文档化的公有项可用内置的 `missing_docs` lint 查看。未文档化的私有项可用 Clippy 的 `missing_docs_in_private_items` lint 查看。

代码示例的统计遵循以下规则：

1. 默认不统计这些项：
  * struct/union 字段
  * enum 变体
  * 常量
  * 静态项
  * typedef
2. 若上述某项带有代码示例，则会计入。

若同时使用 `-o` 选项，会将文件生成到给定文件夹名中。例如：

```shell
rustdoc foo.rs --show-coverage -o doc
```

会在 `doc` 文件夹中生成 `foo.txt`。若未传入 `-o`，则显示在 stdout 上。

### JSON 输出 {#json-output}

将此选项与 `--output-format json` 一起使用时，会以 JSON 格式显示覆盖率信息。例如，以下是一个含有一个已文档化项与一个未文档化项的文件对应的 JSON：

```rust
/// 此项有文档
pub fn foo() {}

pub fn no_documentation() {}
```

```json
{"no_std.rs":{"total":3,"with_docs":1,"total_examples":3,"with_examples":0}}
```

注意第三项是 crate 根，在本例中未文档化。

若希望 JSON 输出显示在 `stdout` 上而不是生成文件，可使用 `-o -`。

## `-w`/`--output-format`：输出格式 {#-w--output-format-output-format}

### json {#json}

 * 跟踪议题：[#76578](https://github.com/rust-lang/rust/issues/76578)

`--output-format json` 以实验性的 [JSON 格式](https://doc.rust-lang.org/nightly/nightly-rustc/rustdoc_json_types/) 发出文档。

工具链 crate（`std`、`alloc`、`core`、`test` 与 `proc_macro`）的 JSON 输出可通过 `rust-docs-json` rustup 组件获得。

```shell
rustup component add --toolchain nightly rust-docs-json
```

随后 json 文件会出现在该 rustup 工具链目录的 `share/doc/rust/json/` 目录中。

它也可与 `--show-coverage` 一起使用。详见其[文档](#--show-coverage-calculate-the-percentage-of-items-with-documentation)。

### doctest {#doctest}

 * 跟踪议题：[#134529](https://github.com/rust-lang/rust/issues/134529)

`--output-format doctest` 在 stdout 上发出 JSON，提供关于给定 crate 中文档测试的信息。

可如下使用：

```bash
rustdoc -Zunstable-options --output-format=doctest src/lib.rs
```

对于如下 Rust 代码：

```rust
/// ```
/// #![allow(dead_code)]
/// let x = 12;
/// Ok(())
/// ```
pub trait Trait {}
```

生成的输出（格式化后）类似：

```json
{
  "format_version": 2,
  "doctests": [
    {
      "file": "src/lib.rs",
      "line": 1,
      "doctest_attributes": {
        "original": "",
        "should_panic": false,
        "no_run": false,
        "ignore": "None",
        "rust": true,
        "test_harness": false,
        "compile_fail": false,
        "standalone_crate": false,
        "error_codes": [],
        "edition": null,
        "added_css_classes": [],
        "unknown": []
      },
      "original_code": "#![allow(dead_code)]\nlet x = 12;\nOk(())",
      "doctest_code": {
        "crate_level": "#![allow(unused)]\n#![allow(dead_code)]\n\n",
        "code": "let x = 12;\nOk(())",
        "wrapper": {
          "before": "fn main() { fn _inner() -> core::result::Result<(), impl core::fmt::Debug> {\n",
          "after": "\n} _inner().unwrap() }",
          "returns_result": true
        }
      },
      "name": "src/lib.rs - (line 1)"
    }
  ]
}
```

 * `format_version` 给出生成 JSON 的当前版本。若我们以任何方式更改输出，该数字会增加。
 * `doctests` 包含 crate 中存在的文档测试列表。
   * `file` 是文档测试所在的文件路径。
   * `line` 是文档测试开始的行（即当前代码中 \`\`\` 所在的位置）。
   * `doctest_attributes` 包含关于文档测试所用属性的计算信息。关于文档测试属性的更多信息，见[此处](how-to-write-documentation/05-documentation-tests/#attributes)。
   * `original_code` 是源码中写入、在 rustdoc 修改之前的代码。
   * `doctest_code` 是经 rustdoc 修改后将要运行的代码。若存在致命语法错误，则不会出现此字段。
     * `crate_level` 是将添加到生成文档测试顶层的 crate 级代码（如属性或 `extern crate`）。
     * `code` 是“裸”文档测试，不含 `crate_level` 与 `wrapper` 的内容。
     * `wrapper` 包含将在 `code` 之前与之后添加的额外代码。
       * `returns_result` 是布尔值。若为 `true`，表示该文档测试返回 `Result` 类型。
   * `name` 是 rustdoc 为表示此文档测试而生成的名称。

### html {#html}

`--output-format html` 没有效果，因为默认输出就是 HTML。该选项在稳定版上也可接受，尽管此标志的其他选项并非如此。

## `--with-examples`：将项的使用示例作为文档包含进来 {#--with-examples-include-examples-of-uses-of-items-as-documentation}

 * 跟踪议题：[#88791](https://github.com/rust-lang/rust/issues/88791)

此选项与 `--scrape-examples-target-crate` 及 `--scrape-examples-output-path` 配合，用于实现 [RFC #3123](https://github.com/rust-lang/rfcs/pull/3123) 中的功能。会在某个 crate 及其反向依赖中查找项的用法（目前为函数 / 调用点），再将这些用法作为该项的文档包含进来。此特性预期通过 `cargo doc --scrape-examples` 使用，但仅用 rustdoc 的工作流如下：

```bash
$ rustdoc examples/ex.rs -Z unstable-options \
    --extern foobar=target/deps/libfoobar.rmeta \
    --scrape-examples-target-crate foobar \
    --scrape-examples-output-path output.calls
$ rustdoc src/lib.rs -Z unstable-options --with-examples output.calls
```

首先必须检查库以生成 `rmeta`。然后将反向依赖（如 `examples/ex.rs`）交给 rustdoc，指定正在文档化的目标 crate（`foobar`）以及输出调用信息的路径（`output.calls`）。随后，可将生成的调用文件通过 `--with-examples` 传给后续对 `foobar` 的文档生成。

若要从测试代码（例如标有 `#[test]` 的函数）中抓取示例，请添加 `--scrape-tests` 标志。

## `--generate-link-to-definition`：在源码中为类型生成链接 {#--generate-link-to-definition-generate-links-on-types-in-source-code}

 * 跟踪议题：[#89095](https://github.com/rust-lang/rust/issues/89095)

此标志启用源码页中的链接生成，使读者可跳转到类型定义。

> [!WARNING]
> 在非常特定的场景下，若你依赖 rustdoc 有意不对函数体运行全部语义分析遍次（pass），以辅助文档化 `cfg` 条件项，启用此特性可能导致你的程序被拒绝。
>
> 更具体地说，若函数体包含含方法调用在内的类型相关路径，rustdoc 可能选择对这些函数体进行类型检查。这可能导致 rustdoc 通常会抑制的名称解析与类型错误被报告出来。

### `--test-builder`：类似 `rustc` 的程序，用于构建测试 {#--test-builder-rustc-like-program-to-build-tests}

 * 跟踪议题：[#102981](https://github.com/rust-lang/rust/issues/102981)

使用该标志如下：

```bash
$ rustdoc --test-builder /path/to/rustc src/lib.rs
```

Rustdoc 将使用所提供的程序编译测试，而不是 sysroot 中默认的 `rustc` 程序。

### `--test-builder-wrapper`：包装对测试构建器的调用 {#--test-builder-wrapper-wrap-calls-to-the-test-builder}

 * 跟踪议题：[#102981](https://github.com/rust-lang/rust/issues/102981)

使用该标志如下：

```bash
$ rustdoc -Zunstable-options --test-builder-wrapper /path/to/rustc-wrapper src/lib.rs
$ rustdoc -Zunstable-options \
    --test-builder-wrapper rustc-wrapper1 \
    --test-builder-wrapper rustc-wrapper2 \
    --test-builder rustc \
    src/lib.rs
```

与 cargo 的 `build.rustc-wrapper` 选项类似，此标志接受一个 `rustc` 包装程序。传给该程序的第一个参数是测试构建器程序。

此标志可多次传入以嵌套包装器。

## 编译文档测试时向 rustc 传递参数 {#passing-arguments-to-rustc-when-compiling-doctests}

若希望在编译文档测试时添加选项，可使用 `--doctest-build-arg` 标志。例如若有：

```rust,no_run
/// ```
/// #![deny(warnings)]
/// #![feature(async_await)]
///
/// let x = 12;
/// ```
pub struct Bar;
```

并对它运行 `rustdoc --test`，会得到：

```console
running 1 test
test foo.rs - Bar (line 1) ... FAILED

failures:

---- foo.rs - Bar (line 1) stdout ----
error: the feature `async_await` has been stable since 1.39.0 and no longer requires an attribute to enable
 --> foo.rs:2:12
  |
3 | #![feature(async_await)]
  |            ^^^^^^^^^^^
  |
note: the lint level is defined here
 --> foo.rs:1:9
  |
2 | #![deny(warnings)]
  |         ^^^^^^^^
  = note: `#[deny(stable_features)]` implied by `#[deny(warnings)]`

error: aborting due to 1 previous error

Couldn't compile the test.

failures:
    foo.rs - Bar (line 1)

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
```

但若用 `--doctest-build-arg=--cap-lints=warn` 将 lint 级别限制为 warning：

```console
$ rustdoc --test --doctest-build-arg=--cap-lints=warn file.rs

running 1 test
test tests/rustdoc-ui/doctest/rustflags.rs - Bar (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.06s
```

若要向底层编译器传递多个参数，请为每个参数 `ARG` 传入一次 `--doctest-build-arg ARG`。

## `--generate-macro-expansion`：在源码中生成宏展开开关 {#--generate-macro-expansion-generate-macros-expansion-toggles-in-source-code}

此标志启用 HTML 源码页中用于展开宏的开关生成。

## `--remap-path-scope`：应进行源路径重映射的作用域 {#--remap-path-scope-scopes-to-which-the-source-remapping-should-be-done}

此标志等价于 `rustc` 的 `--remap-path-scope`。

定义 `--remap-path-prefix` 应重映射哪些路径作用域。

### `documentation` 作用域 {#documentation-scope}

`rustdoc`（进而包括 `rustc`）有一个特殊的 `documentation` 重映射作用域，允许重映射最终出现在生成文档中的源路径。

目前该作用域只能从 `rustc` 指定，因为 `rustc` 缺少等价的 `--remap-path-scope` 标志。

## `#[doc(cfg)]` 与 `#[doc(auto_cfg)]` {#doccfg-and-docauto_cfg}

此特性旨在让 rustdoc 用户能为渲染后的文档添加可视化标记，以了解项在何种条件下可用（目前可通过不稳定特性 `doc_cfg` 实现）。

它不旨在允许同一项在不同 `cfg` 下在生成文档中出现多次。

它不旨在为在当前配置下*未激活*（即被 “`cfg` 掉”）的项编写文档。

此特性添加以下属性：

 * `#[doc(auto_cfg)]`/`#[doc(auto_cfg = true)]`/`#[doc(auto_cfg = false)]`
 * `#[doc(cfg(...))]`
 * `#![doc(auto_cfg(hide(...)))]` / `#[doc(auto_cfg(show(...)))]`

所有这些属性都可添加到模块或 crate 根，并由子项继承，除非另一属性覆盖它。这就是为何提供“相反”的属性如 `auto_cfg(hide(...))` 与 `auto_cfg(show(...))`：它们允许子项覆盖其父项。

### `#[doc(cfg(...))]` {#doccfg}

此属性提供标准化格式，以覆盖 `#[cfg()]` 属性，用于为条件可用项编写文档。示例：

```rust,ignore (nightly)
// “真正的” cfg 条件
#[cfg(feature = "futures-io")]
// `doc(cfg())`，以便向读者显示
#[doc(cfg(feature = "futures-io"))]
pub mod futures {}
```

它会在该模块的文档中显示：

```text
仅在 feature="futures-io" 上可用。
```

无论是否存在 `#[cfg()]` 属性，都可用它在生成的文档中显示信息：

```rust,ignore (nightly)
#[doc(cfg(feature = "futures-io"))]
pub mod futures {}
```

显示效果与前一段代码完全相同。

此属性的语法与条件编译相同，但只会导致添加文档。这意味着 `#[doc(cfg(not(windows)))]` 不会使你的文档在非 Windows 目标上隐藏，尽管 `#[cfg(not(windows))]` 会那样做。

若项上启用了 `doc(auto_cfg)`，`doc(cfg)` 仍会覆盖它，因此在前两个示例中，即使启用了 `doc(auto_cfg)` 特性，显示内容仍相同。

此属性适用于模块与项。

### `#[doc(auto_cfg(hide(...)))]` {#docauto_cfghide}

此属性用于防止某些 `cfg` 出现在可视化标记中。它仅作用于 `#[doc(auto_cfg = true)]`，不作用于 `#[doc(cfg(...))]`。因此在前例中：

```rust,ignore (nightly)
#[cfg(any(unix, feature = "futures-io"))]
pub mod futures {}
```

当前会在文档中同时显示 `unix` 与 `feature = "futures-io"`，效果并不理想。若要永远不显示 `unix` cfg，可在 crate 根级别使用此属性：

```rust,ignore (nightly)
#![doc(auto_cfg(hide(unix)))]
```

或直接用在给定项/模块上，因为它会覆盖该项的所有后代：

```rust,ignore (nightly)
#[doc(auto_cfg(hide(unix)))]
#[cfg(any(unix, feature = "futures-io"))]
pub mod futures {
    // `futures` 及其所有后代不会在其 cfg 中显示 "unix"。
}
```

这样，`unix` cfg 就永远不会出现在文档中。

`hide` 的语法如下：你可以列出任意多个 `cfg` 名称：

```rust,ignore (nightly)
#[doc(auto_cfg(hide(feature, target_os)))]
```

在上例中，这意味着 `#[cfg(feature)]` 与 `#[cfg(target_os)]` 不会出现在文档中。但 `#[cfg(target_os = "linux)]` 或 `#[cfg(feature = "something")]` 仍会显示，因为只有不带值的键被标为隐藏。若要隐藏某些值，可以这样做：

```rust,ignore (nightly)
#[doc(auto_cfg(hide(feature, target_os, values("something", "linux"))))]
```

此时，`#[cfg(feature = "linux")]`、`#[cfg(feature = "something")]`、`#[cfg(target_os = "something")]` 与 `#[cfg(target_os = "linux")]` 会被隐藏。所有列出的键都会受 `values(...)` 影响。可通过使用两个 `hide` 来拆分：

```rust,ignore (nightly)
#[doc(auto_cfg(
    hide(feature, values("something")),
    hide(target_os, values("linux")),
))]
```

现在，只有 `#[cfg(feature = "something")]` 与 `#[cfg(target_os = "linux")]` 会被隐藏。若要隐藏某个键及其所有值，可使用 `any()`：

```rust,ignore (nightly)
#[doc(auto_cfg(
    hide(feature, values(any())),
))]
```

若只想在没有值时隐藏，可使用 `none()`：

```rust,ignore (nightly)
#[doc(auto_cfg(
    hide(feature, values("something", none())),
))]
```

因此，若要禁止某个键的所有值，但允许键本身，可以这样做：

```rust,ignore (nightly)
#[doc(auto_cfg(
    hide(feature, values(any())), // 完全隐藏 "feature"。
    show(feature), // 再次显示 "feature"（但不显示任何值）。
))]
```

在前例中，`#[cfg(feature)]` 与 `#[cfg(feature = "something")]` 都会被隐藏。

Rustdoc 默认隐藏 `test`、`doc` 与 `doctest` 属性，并保留更改“默认隐藏”属性列表的权利。

该属性仅接受标识符列表与 `values()`。因此你可以写：

```rust,ignore (nightly)
#[doc(auto_cfg(
    hide(unix, doctest),
    hide(feature, values("something")),
))]
#[doc(auto_cfg(hide()))]
```

但不能写：

```rust,ignore (nightly)
#[doc(auto_cfg(hide(not(unix))))]
```

因此若使用 `doc(auto_cfg(hide(unix)))`，意味着会隐藏所有不带值的 `unix` 提及：

```rust,ignore (nightly)
#[cfg(unix)] // 不显示任何内容
#[cfg(any(unix))] // 不显示任何内容
#[cfg(any(unix, windows))] // 仅显示 `windows`
```

但它只影响 `unix` cfg，不影响 feature：

```rust,ignore (nightly)
#[cfg(feature = "unix")] // 显示 `feature = "unix"`
```

使用此属性会在该位置重新启用已被禁用的 `auto_cfg`：

```rust,ignore (nightly)
#[doc(auto_cfg = false)] // 禁用 `auto_cfg`
pub fn foo() {}
```

而使用 `doc(auto_cfg)` 会重新启用它：

```rust,ignore (nightly)
#[doc(auto_cfg = false)] // 禁用 `auto_cfg`
pub mod module {
    #[doc(auto_cfg(hide(unix)))] // `auto_cfg` 被重新启用。
    pub fn foo() {}
}
```

原因是 `doc(auto_cfg = ...)` 启用或禁用该特性，而 `doc(auto_cfg(...))` 无条件启用它，使前一个属性显得无用，因为会被下一个 `doc(auto_cfg)` 属性覆盖。

### `#[doc(auto_cfg(show(...)))]` {#docauto_cfgshow}

此属性与 `#[doc(auto_cfg(hide(...)))]` 相反：若已使用 `#[doc(auto_cfg(hide(...)))]`，并想在某个项及其后代上撤销其效果，可使用 `#[doc(auto_cfg(show(...)))]`。
它仅作用于 `#[doc(auto_cfg = true)]`，不作用于 `#[doc(cfg(...))]`。

其语法规则与 `#[doc(auto_cfg(hide(...)))]` 相同。

例如：

```rust,ignore (nightly)
#[doc(auto_cfg(hide(unix)))]
#[cfg(any(unix, feature = "futures-io"))]
pub mod futures {
    // `futures` 及其所有后代不会在其 cfg 中显示 "unix"。
    #[doc(auto_cfg(show(unix)))]
    pub mod child {
        // `child` 及其所有后代会在其 cfg 中显示 "unix"。
    }
}
```

该属性仅接受标识符或键/值项列表。因此你可以写：

```rust,ignore (nightly)
#[doc(auto_cfg(
    show(unix, doctest),
    show(feature, values("something")),
))]
#[doc(auto_cfg(show()))]
```

但不能写：

```rust,ignore (nightly)
#[doc(auto_cfg(show(not(unix))))]
```

若在同一项上用 `auto_cfg(show(...))` 与 `auto_cfg(hide(...))` 显示/隐藏同一 `cfg`，会发出错误。示例：

```rust,ignore (nightly)
#[doc(auto_cfg(show(unix)))]
#[doc(auto_cfg(hide(unix)))] // 错误！
pub fn foo() {}
```

使用此属性会在该位置重新启用已被禁用的 `auto_cfg`：

```rust,ignore (nightly)
#[doc(auto_cfg = false)] // 禁用 `auto_cfg`
#[doc(auto_cfg(show(unix)))] // `auto_cfg` 被重新启用。
pub fn foo() {}
```

### `#[doc(auto_cfg)`/`#[doc(auto_cfg = true)]`/`#[doc(auto_cfg = false)]` {#docauto_cfgdocauto_cfg--truedocauto_cfg--false}

默认情况下，`#[doc(auto_cfg)]` 在 crate 级别启用。启用时，Rustdoc 会自动显示 `cfg(...)` 兼容性信息，如同指定了相同的 `#[doc(cfg(...))]`。

此属性影响使用它的项及其后代。

因此，回到前面的例子：

```rust
#[cfg(feature = "futures-io")]
pub mod futures {}
```

无需把 `cfg`“复制”到 `doc(cfg())` 中，Rustdoc 就会显示它。

在某些情况下，用于实现特性的详细条件编译规则可能不宜直接作为文档（例如，支持的平台列表可能很长，更好集中在一处文档化）。要关闭它，请在该项上添加 `#[doc(auto_cfg = false)]` 属性。

若不指定参数（即 `#[doc(auto_cfg)]`），等价于写 `#[doc(auto_cfg = true)]`。

## 继承 {#inheritance}

Rustdoc 会将父模块的 `cfg` 属性合并到其子项。例如，在此情况下，模块 `non_unix` 会描述该模块的完整兼容性矩阵，而不仅是其直接附着的信息：

```rust,ignore (nightly)
#[doc(cfg(any(windows, unix)))]
pub mod desktop {
    #[doc(cfg(not(unix)))]
    pub mod non_unix {
        // ...
    }
}
```

此代码会显示：

```text
仅在（Windows 或 Unix）且非 Unix 上可用。
```

### 重导出与内联 {#re-exports-and-inlining}

重导出的 `cfg` 属性绝不会与被重导出品的属性合并，除非该重导出带有 `#[doc(inline)]` 属性。此时，被重导出品的 `cfg` 会与重导出的 `cfg` 合并。

说到“属性合并”，意思是：若重导出有 `#[cfg(unix)]`，被重导出品有 `#[cfg(feature = "foo")]`，则重导出上只会看到 `cfg(unix)`，被重导出品上只会看到 `cfg(feature = "foo")`；除非重导出有 `#[doc(inline)]`，那时只会看到被重导出品同时带有 `cfg(unix)` 与 `cfg(feature = "foo")`。

示例：

```rust,ignore (nightly)
#[doc(cfg(any(windows, unix)))]
pub mod desktop {
    #[doc(cfg(not(unix)))]
    pub mod non_unix {
        // 代码
    }
}

#[doc(cfg(target_os = "freebsd"))]
pub use desktop::non_unix as non_unix_desktop;
#[doc(cfg(target_os = "macos"))]
#[doc(inline)]
pub use desktop::non_unix as inlined_non_unix_desktop;
```

在此例中，`non_unix_desktop` 只会显示 `cfg(target_os = "freebsd")`，而不会显示来自 `desktop::non_unix` 的任何 `cfg`。

相反，`inlined_non_unix_desktop` 会同时拥有来自重导出与被重导出品的 cfg。

这也意味着：若某个 crate 重导出了外部项，除非带有 `#[doc(inline)]`，否则 `cfg` 与 `doc(cfg)` 属性将不可见：

```rust,ignore (nightly)
// dep:
#[cfg(feature = "a")]
pub struct S;

// 使用 dep 的 crate：

// 文档中不会提及 `feature = "a"`。
pub use dep::S as Y;
```
