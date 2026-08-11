+++
title = "02-命令行参数"
date = 2026-08-01T07:35:00+08:00
weight = 20
type = "docs"
description = "rustdoc 命令行参数参考"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 命令行参数 {#command-line-arguments}


> 原文链接: [https://doc.rust-lang.org/rustdoc/command-line-arguments.html](https://doc.rust-lang.org/rustdoc/command-line-arguments.html)


以下是你可以传给 `rustdoc` 的参数列表：

## `-h`/`--help`：帮助 {#h---help-help}

使用该标志如下：

```bash
$ rustdoc -h
$ rustdoc --help
```

这会显示 `rustdoc` 的内置帮助，其中主要是可能的命令行标志列表。

`rustdoc` 的部分标志是不稳定的；本页只展示稳定选项，`--help` 会显示全部。

## `-V`/`--version`：版本信息 {#v---version-version-information}

使用该标志如下：

```bash
$ rustdoc -V
$ rustdoc --version
```

这会显示 `rustdoc` 的版本，大致如下：

```text
rustdoc 1.17.0 (56124baa9 2017-04-24)
```

## `-v`/`--verbose`：更详细的输出 {#v---verbose-more-verbose-output}

使用该标志如下：

```bash
$ rustdoc -v src/lib.rs
$ rustdoc --verbose src/lib.rs
```

这会启用“详细模式”，意味着会向标准输出写入更多信息。具体写入什么取决于你传入的其它标志。例如，配合 `--version`：

```text
$ rustdoc --verbose --version
rustdoc 1.17.0 (56124baa9 2017-04-24)
binary: rustdoc
commit-hash: hash
commit-date: date
host: host-tuple
release: 1.17.0
LLVM version: 3.9
```

## `-o`/`--out-dir`：输出目录路径 {#o---out-dir-output-directory-path}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -o target/doc
$ rustdoc src/lib.rs --out-dir target/doc
```

默认情况下，`rustdoc` 的输出会出现在当前工作目录下名为 `doc` 的目录中。使用该标志后，所有输出都会放到你指定的目录中。


## `--crate-name`：控制 crate 名称 {#--crate-name-controlling-the-name-of-the-crate}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --crate-name mycrate
```

默认情况下，`rustdoc` 假定你的 crate 名称与 `.rs` 文件名相同。`--crate-name` 让你用任意选定的名称覆盖该假定。

## `--document-private-items`：显示非公有项 {#--document-private-items-show-items-that-are-not-public}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --document-private-items
```

默认情况下，`rustdoc` 只为可公有可达的项生成文档。

```rust
pub fn public() {} // 该项是公有的，会出现在文档中
mod private { // 该项是私有的，不会出现在文档中
    pub fn unreachable() {} // 该项是公有的，但不可达，因此不会出现在文档中
}
```

`--document-private-items` 会把生成文档中所有非公有项都包含进来，但 `#[doc(hidden)]` 项除外。私有项会带有 🔒 图标显示。


## `-L`/`--library-path`：在何处查找依赖 {#l---library-path-where-to-look-for-dependencies}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -L target/debug/deps
$ rustdoc src/lib.rs --library-path target/debug/deps
```

如果你的 crate 有依赖，`rustdoc` 需要知道在哪里找到它们。传入 `--library-path` 会给 `rustdoc` 一份查找这些依赖的位置列表。

该标志接受任意数量的目录作为参数，并在搜索时使用它们全部。


## `--cfg`：传入配置标志 {#--cfg-passing-configuration-flags}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --cfg feature="foo"
```

该标志接受与 `rustc --cfg` 相同的值，并用它来配置编译。上面的例子使用了 `feature`，但任何 `cfg` 值都可以。

## `--check-cfg`：检查配置标志 {#--check-cfg-check-configuration-flags}

该标志接受与 `rustc --check-cfg` 相同的值，并用它来检查配置标志。

使用该标志如下：

```bash
$ rustdoc src/lib.rs --check-cfg='cfg(my_cfg, values("foo", "bar"))'
```

上面的例子会检查每个已知名称和值（`target_os`、`doc`、`test` 等），并检查 `my_cfg` 的值：`foo` 和 `bar`。

## `--extern`：指定依赖的位置 {#--extern-specify-a-dependencys-location}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --extern lazy-static=/path/to/lazy-static
```

与 `--library-path` 类似，`--extern` 也与指定依赖位置有关。`--library-path` 提供要搜索的目录，而 `--extern` 则让你精确指定某个依赖位于何处。

## `-C`/`--codegen`：向 rustc 传递 codegen 选项 {#c---codegen-pass-codegen-options-to-rustc}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -C target_feature=+avx
$ rustdoc src/lib.rs --codegen target_feature=+avx

$ rustdoc --test src/lib.rs -C target_feature=+avx
$ rustdoc --test src/lib.rs --codegen target_feature=+avx

$ rustdoc --test README.md -C target_feature=+avx
$ rustdoc --test README.md --codegen target_feature=+avx
```

当 rustdoc 生成文档、查找文档测试或执行文档测试时，它需要至少部分地编译一些 Rust 代码。该标志允许你告诉 rustdoc，在运行这些编译时向 rustc 提供一些额外的 codegen 选项。大多数时候，这些选项不会影响常规的文档生成；但如果有东西依赖于启用目标特性，或者文档测试需要使用一些额外选项，该标志就允许你施加影响。

传给该标志的参数与 rustc 的 `-C` 标志相同。运行 `rustc -C help` 可获取完整列表。

## `--remap-path-prefix`：在输出中重映射源路径 {#--remap-path-prefix-remap-source-paths-in-output}

该标志等价于 `rustc` 的 `--remap-path-prefix`。

```bash
$ rustdoc src/lib.rs --remap-path-prefix="$PWD=/foo"
```

它允许（尽力而为地）在所有输出中重映射源路径前缀，包括诊断、调试信息、宏展开、生成的文档等。它接受形如 `FROM=TO` 的值：等于 `FROM` 的路径前缀会被改写为 `TO`。

## `--test`：将代码示例作为测试运行 {#--test-run-code-examples-as-tests}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --test
```

该标志会将你的代码示例作为测试运行。更多信息见[关于文档测试的章节](how-to-write-documentation/05-documentation-tests/)。

另见 `--test-args` 和 `--test-run-directory`。

## `--test-args`：向测试运行器传递选项 {#--test-args-pass-options-to-test-runner}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --test --test-args ignored
```

该标志会在运行文档测试时向测试运行器传递选项。更多信息见[关于文档测试的章节](how-to-write-documentation/05-documentation-tests/)。

另见 `--test`。

## `--test-run-directory`：在特定目录中运行代码示例 {#--test-run-directory-run-code-examples-in-a-specific-directory}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --test --test-run-directory=/path/to/working/directory
```

该标志会在指定的工作目录中运行你的代码示例。更多信息见[关于文档测试的章节](how-to-write-documentation/05-documentation-tests/)。

另见 `--test`。

## `--test-runtool`、`--test-runtool-arg`：用于运行测试的程序；传给它的参数 {#--test-runtool---test-runtool-arg-program-to-run-tests-with-args-to-pass-to-it}

可以用 `--test-runtool` 标志指定一个 doctest 包装程序。在运行测试时，rustdoc 会执行该包装程序，而不是直接执行 doctest 可执行文件。传给包装程序的第一批参数是用 `--test-runtool-arg` 指定的任意参数，随后是要运行的 doctest 可执行文件路径。

使用这些选项如下：

```bash
$ rustdoc src/lib.rs --test-runtool path/to/runner --test-runtool-arg --do-thing --test-runtool-arg --do-other-thing
```

例如，如果你想在 valgrind 下运行 doctest，可以这样：

```bash
$ rustdoc src/lib.rs --test-runtool valgrind
```

另一个用例是在模拟器中，或通过虚拟机来运行测试。

## `--target`：为指定目标三元组生成文档 {#--target-generate-documentation-for-the-specified-target-triple}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --target x86_64-pc-windows-gnu
```

与 `rustc` 的 `--target` 标志类似，这会为不同于宿主三元组的目标三元组生成文档。

交叉编译代码时的常见注意事项同样适用。

## `--default-theme`：设置默认主题 {#--default-theme-set-the-default-theme}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --default-theme=ayu
```

设置默认主题（针对浏览器尚未从页面上主题选择器记住先前主题选择的用户）。

提供的值应为主题名称的小写形式。可用主题集合可在生成输出中的主题选择器里看到。

请注意，可用主题集合——以及它们的外观——并不一定在不同 rustdoc 版本之间保持稳定。如果请求的主题不存在，则会改用内置默认主题（当前为 `light`）。

## `--markdown-css`：渲染 Markdown 时包含更多 CSS 文件 {#--markdown-css-include-more-css-files-when-rendering-markdown}

使用该标志如下：

```bash
$ rustdoc README.md --markdown-css foo.css
```

在渲染 Markdown 文件时，这会在生成 HTML 的 `<head>` 部分创建一个 `<link>` 元素。例如，使用上面的调用时，会添加：

```html
<link rel="stylesheet" type="text/css" href="foo.css">
```

在渲染 Rust 文件时，该标志会被忽略。

## `--html-in-header`：在 `<head>` 中包含更多 HTML {#--html-in-header-include-more-html-in-head}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --html-in-header header.html
$ rustdoc README.md --html-in-header header.html
```

该标志接受文件列表，并将它们插入到渲染文档的 `<head>` 部分。

## `--html-before-content`：在内容之前包含更多 HTML {#--html-before-content-include-more-html-before-the-content}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --html-before-content extra.html
$ rustdoc README.md --html-before-content extra.html
```

该标志接受文件列表，并将它们插入到 `<body>` 标签内，但位于 `rustdoc` 通常会在渲染文档中生成的其它内容之前。

## `--html-after-content`：在内容之后包含更多 HTML {#--html-after-content-include-more-html-after-the-content}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --html-after-content extra.html
$ rustdoc README.md --html-after-content extra.html
```

该标志接受文件列表，并将它们插入到 `</body>` 标签之前，但位于 `rustdoc` 通常会在渲染文档中生成的其它内容之后。


## `--markdown-playground-url`：控制 playground 的位置 {#--markdown-playground-url-control-the-location-of-the-playground}

使用该标志如下：

```bash
$ rustdoc README.md --markdown-playground-url https://play.rust-lang.org/
```

在渲染 Markdown 文件时，该标志给出 Rust Playground 的基础 URL，用于生成 `Run` 按钮。


## `--markdown-no-toc`：不生成目录 {#--markdown-no-toc-dont-generate-a-table-of-contents}

使用该标志如下：

```bash
$ rustdoc README.md --markdown-no-toc
```

从 Markdown 文件生成文档时，默认情况下 `rustdoc` 会生成目录。该标志会抑制这一点，不会生成 TOC。


## `-e`/`--extend-css`：扩展 rustdoc 的 CSS {#e---extend-css-extend-rustdocs-css}

使用该标志如下：

```bash
$ rustdoc src/lib.rs -e extra.css
$ rustdoc src/lib.rs --extend-css extra.css
```

使用该标志时，你传入的文件内容会包含在 `theme.css` 文件的底部。

## `--sysroot`：覆盖系统根 {#--sysroot-override-the-system-root}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --sysroot /path/to/sysroot
```

与 `rustc --sysroot` 类似，这让你可以更改 `rustdoc` 在编译代码时使用的 sysroot。

## `--edition`：控制文档与 doctest 的 edition {#--edition-control-the-edition-of-docs-and-doctests}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --edition 2018
$ rustdoc --test src/lib.rs --edition 2018
```

该标志允许 `rustdoc` 将你的 Rust 代码按给定 edition 处理。它也会用给定 edition 编译 doctest。与 `rustc` 一样，`rustdoc` 默认使用的 edition 是 `2015`（第一个 edition）。

## `--theme`：向文档输出添加主题 {#--theme-add-a-theme-to-the-documentation-output}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --theme /path/to/your/custom-theme.css
```

`rustdoc` 的默认输出包含两个主题：`light`（默认）和 `dark`。该标志允许你向输出添加自定义主题。向该标志提供一个 CSS 文件，会把它作为额外的主题选项加入文档。主题名称由其文件名决定；名为 `custom-theme.css` 的主题文件会向文档添加名为 `custom-theme` 的主题。

## `--check-theme`：对照默认主题验证自定义主题 {#--check-theme-verify-custom-themes-against-the-default-theme}

使用该标志如下：

```bash
$ rustdoc --check-theme /path/to/your/custom-theme.css
```

虽然 `rustdoc` 的 HTML 输出在不同版本之间大致一致，但不能保证主题文件会有相同效果。`--theme` 标志仍然允许你把主题加到文档中，但为了确保主题按预期工作，你可以使用该标志验证它是否实现了与官方 `light` 主题相同的 CSS 规则。

`--check-theme` 是 `rustdoc` 中的一种独立模式。当 `rustdoc` 看到 `--check-theme` 标志时，它会丢弃所有其它标志，只执行 CSS 规则比较操作。

## `--crate-version`：控制 crate 版本 {#--crate-version-control-the-crate-version}

使用该标志如下：

```bash
$ rustdoc src/lib.rs --crate-version 1.3.37
```

当 `rustdoc` 收到该标志时，它会在 crate 根文档的侧边栏中额外打印 “Version (version)”。你可以用该标志区分库文档的不同版本。

## `--emit`：控制 rustdoc 产出的输出类型 {#--emit-control-the-types-of-output-for-rustdoc-to-emit}

该标志控制 rustdoc 的输出类型。它接受逗号分隔的值列表，并且可以指定多次。有效的 emit 种类有：

- `html-static-files` —— 生成共享静态文件，其内容与特定工具链版本绑定。这些文件的文件名包含内容哈希，因此在工具链版本或其内容变化时可以安全地按变化缓存，也可以配合 `Cache-Control: immutable` 指令使用。
- `html-non-static-files` —— 基于被文档化的 crate 生成文件。这些文件名需要是确定性的，因此文件名中没有内容哈希。
- `dep-info` —— 生成一个使用 Makefile 语法的文件，指出为文档化该 crate 而加载的所有源文件。默认输出文件名是 `CRATE_NAME.d`。该 emit 类型后面可以可选地跟 `=` 以指定显式输出路径，例如 `--emit=dep-info=/path/to/foo.d`。也可以通过将路径指定为 `-` 把输出发送到 stdout（例如 `--emit=dep-info=-`）。

使用该标志如下：

```bash
$ rustdoc src/lib.rs --emit=html-static-files,html-non-static-files,dep-info=/path/to/build/cache/foo.d
```

如果未指定，默认 emit 类型为 `--emit=html-static-files,html-non-static-files`。

除非使用 `--out-dir` 标志，否则输出文件会写入当前目录。

## `-`：从标准输入加载源代码 {#--load-source-code-from-the-standard-input}

如果你在命令行上将 INPUT 指定为 `-`，那么 `rustdoc` 会从 stdin（标准输入流）读取源代码直到 EOF，而不是从文件系统上另行指定的路径读取。

## `@path`：从路径加载命令行标志 {#path-load-command-line-flags-from-a-path}

如果你在命令行上指定 `@path`，它会打开 `path` 并从中读取命令行选项。这些选项每行一个；空行表示一个空选项。该文件可以使用 Unix 或 Windows 风格的换行，并且必须以 UTF-8 编码。

## `--passes`：添加更多 rustdoc pass {#--passes-add-more-rustdoc-passes}

该标志已**弃用**。
关于 pass 的更多细节，见[相关章节](09-deprecated-features/#passes)。

## `--no-defaults`：不运行默认 pass {#--no-defaults-dont-run-default-passes}

该标志已**弃用**。
关于 pass 的更多细节，见[相关章节](09-deprecated-features/#passes)。

## `-r`/`--input-format`：输入格式 {#r---input-format-input-format}

该标志已**弃用**且**没有效果**。

rustdoc 只支持 Rust 源代码和 Markdown 输入格式。如果文件以 `.md` 或 `.markdown` 结尾，`rustdoc` 会将其视为 Markdown 文件。否则，它假定输入文件是 Rust。
