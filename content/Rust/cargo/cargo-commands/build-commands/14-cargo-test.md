+++
title = "14-cargo test"
date = 2026-07-30T14:49:00+08:00
weight = 59
type = "docs"
description = "cargo-test(1) 运行测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-test(1) {#cargo-test1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-test.html](https://doc.rust-lang.org/cargo/commands/cargo-test.html)


## 名称 {#name}
cargo-test --- 执行包的单元测试与集成测试

## 大纲 {#synopsis}
`cargo test` [_options_] [_testname_] [`--` _test-options_]

## 描述 {#description}
编译并执行单元测试、集成测试与文档测试。

测试过滤参数 `TESTNAME` 以及两个短划线（`--`）之后的所有参数都会传给测试二进制，进而传给 _libtest_（rustc 内置的单元测试与微基准测试框架）。若同时向 Cargo 与二进制传参，则 `--` 之后的参数传给二进制，之前的传给 Cargo。关于 libtest 参数的详情，请参见 `cargo test -- --help` 的输出，以及 rustc 手册中关于测试工作原理的章节：<https://doc.rust-lang.org/rustc/tests/index.html>。

例如，以下命令会过滤名称中含 `foo` 的测试，并以 3 个线程并行运行：

    cargo test foo -- --test-threads 3

测试使用 `rustc` 的 `--test` 选项构建，通过将你的代码与 libtest 链接来创建特殊可执行文件。该可执行文件会在多个线程中自动运行所有标注了 `#[test]` 属性的函数。标注了 `#[bench]` 的函数也会以一次迭代运行，以验证其功能正常。

若包包含多个测试目标，每个目标都会如上所述编译为特殊可执行文件，然后串行运行。

可通过在目标清单设置中将 `harness = false` 来禁用 libtest 框架，此时你的代码需要提供自己的 `main` 函数来处理测试的运行。

默认情况下，`cargo test` 使用 [`test` 配置文件]，它会启用调试。

[`test` 配置文件]: ../../../cargo-reference/05-profiles/#test

### 文档测试 {#documentation-tests}
默认也会运行文档测试，由 `rustdoc` 处理。它从库目标的文档注释中提取代码示例并执行。

与普通测试目标不同，每个代码块都会用 `rustc` 即时编译为 doctest 可执行文件。这些可执行文件在独立进程中并行运行。代码块的编译实际上是由 libtest 控制的测试函数的一部分，因此某些选项（如 `--jobs`）可能不会生效。注意：doctest 的这种执行模型不保证稳定，将来可能变更；请谨慎依赖它。

关于编写文档测试的更多信息，请参见 [rustdoc 手册](https://doc.rust-lang.org/rustdoc/)。

### 测试的工作目录 {#working-directory-of-tests}
运行每个单元测试与集成测试时，工作目录设为该测试所属包的根目录。
将测试的工作目录设为包的根目录，使测试能够使用相对路径可靠地访问包的文件，而无论从何处执行 `cargo test`。

对于文档测试，调用 `rustdoc` 时的工作目录设为工作空间根目录，这也是 `rustdoc` 用作每个文档测试编译目录的目录。
运行每个文档测试时的工作目录设为该测试所属包的根目录，并通过 `rustdoc` 的 `--test-run-directory` 选项控制。

## 选项 {#options}
### 测试选项 {#test-options}
<dl>

<dt class="option-term" id="option-cargo-test---no-run"><a class="option-anchor" href="#option-cargo-test---no-run"><code>--no-run</code></a></dt>
<dd class="option-desc"><p>编译但不运行测试。</p>
</dd>


<dt class="option-term" id="option-cargo-test---no-fail-fast"><a class="option-anchor" href="#option-cargo-test---no-fail-fast"><code>--no-fail-fast</code></a></dt>
<dd class="option-desc"><p>无论失败与否都运行所有测试。若不带此标志，Cargo 会在第一个可执行文件失败后退出。Rust 测试框架会运行可执行文件内的全部测试直至完成；此标志仅作用于整个可执行文件。</p>
</dd>


</dl>

### 包选择 {#package-selection}
默认情况下，若未给出包选择选项，所选包取决于所选清单文件（若未给出 `--manifest-path`，则基于当前工作目录）。若清单是工作空间根，则选择该工作空间的默认成员；否则仅选择清单所定义的包。

工作空间的默认成员可通过根清单中的 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间将仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-test--p"><a class="option-anchor" href="#option-cargo-test--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-test---package"><a class="option-anchor" href="#option-cargo-test---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>Test only the specified packages. SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。 此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-test---workspace"><a class="option-anchor" href="#option-cargo-test---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>测试工作空间中的所有成员。</p>
</dd>


<dt class="option-term" id="option-cargo-test---all"><a class="option-anchor" href="#option-cargo-test---all"><code>--all</code></a></dt>
<dd class="option-desc"><p><code>--workspace</code> 的已弃用别名。</p>
</dd>


<dt class="option-term" id="option-cargo-test---exclude"><a class="option-anchor" href="#option-cargo-test---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。 此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 目标选择 {#target-selection}
若未给出目标选择选项，`cargo test` 将构建所选包的以下目标：

- lib --- 用于与二进制、示例、集成测试和文档测试链接
- bins（仅当构建集成测试且所需特性可用时）
- examples --- 以确保它们能编译
- 作为单元测试的 lib
- 作为单元测试的 bins
- 集成测试
- lib 目标的文档测试

可通过在清单设置中为目标设置 `test` 标志来更改默认行为。将示例设为 `test = true` 会将该示例作为测试构建并运行，用 libtest 框架替换示例的 `main` 函数。若不希望替换 `main` 函数，还需包含 `harness = false`，此时示例将按原样构建并执行。

将目标设为 `test = false` 会停止默认对它们进行测试。按名称选取目标的目标选择选项（如 `--example foo`）会忽略 `test` 标志，并始终测试给定目标。

可通过在清单中为库设置 `doctest = false` 来禁用库的文档测试。

参见[配置目标](../../../cargo-reference/the-manifest-format/01-cargo-targets/#configuring-a-target)
了解更多关于各目标设置的信息。

若选择测试集成测试或基准测试，则会自动构建二进制目标。这样集成测试可以执行该二进制以演练并测试其行为。
在构建并运行集成测试时会设置 `CARGO_BIN_EXE_<name>`
[环境变量](../../../cargo-reference/07-environment-variables/#environment-variables-cargo-sets-for-crates)，
以便测试可使用 [`env` 宏](https://doc.rust-lang.org/std/macro.env.html) 或
[`var` 函数](https://doc.rust-lang.org/std/env/fn.var.html) 定位可执行文件。

传入目标选择标志将仅测试指定的目标。 

注意：`--bin`、`--example`、`--test` 和 `--bench` 标志也支持常见的 Unix glob 模式，如 `*`、`?` 和 `[]`。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个 glob 模式。

<dl>

<dt class="option-term" id="option-cargo-test---lib"><a class="option-anchor" href="#option-cargo-test---lib"><code>--lib</code></a></dt>
<dd class="option-desc"><p>测试包的库。</p>
</dd>


<dt class="option-term" id="option-cargo-test---bin"><a class="option-anchor" href="#option-cargo-test---bin"><code>--bin</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>测试指定的二进制目标。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-test---bins"><a class="option-anchor" href="#option-cargo-test---bins"><code>--bins</code></a></dt>
<dd class="option-desc"><p>测试所有二进制目标。</p>
</dd>


<dt class="option-term" id="option-cargo-test---example"><a class="option-anchor" href="#option-cargo-test---example"><code>--example</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>测试指定的示例。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-test---examples"><a class="option-anchor" href="#option-cargo-test---examples"><code>--examples</code></a></dt>
<dd class="option-desc"><p>测试所有示例目标。</p>
</dd>


<dt class="option-term" id="option-cargo-test---test"><a class="option-anchor" href="#option-cargo-test---test"><code>--test</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>测试指定的集成测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-test---tests"><a class="option-anchor" href="#option-cargo-test---tests"><code>--tests</code></a></dt>
<dd class="option-desc"><p>测试所有在清单中设置了 <code>test = true</code> 标志的目标。默认包括作为单元测试构建的库与二进制目标，以及集成测试。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为单元测试，一次作为二进制、集成测试等的依赖）。可通过在目标的清单设置中设置 <code>test</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-test---bench"><a class="option-anchor" href="#option-cargo-test---bench"><code>--bench</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>测试指定的基准测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-test---benches"><a class="option-anchor" href="#option-cargo-test---benches"><code>--benches</code></a></dt>
<dd class="option-desc"><p>测试所有在清单中设置了 <code>bench = true</code> 标志的目标。默认包括作为基准测试构建的库与二进制目标，以及 bench 目标。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为基准测试，一次作为二进制、基准测试等的依赖）。可通过在目标的清单设置中设置 <code>bench</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-test---all-targets"><a class="option-anchor" href="#option-cargo-test---all-targets"><code>--all-targets</code></a></dt>
<dd class="option-desc"><p>测试所有目标。等价于指定 <code>--lib --bins --tests --benches --examples</code>。</p>
</dd>


</dl>

<dl>

<dt class="option-term" id="option-cargo-test---doc"><a class="option-anchor" href="#option-cargo-test---doc"><code>--doc</code></a></dt>
<dd class="option-desc"><p>仅测试库的文档。不能与其他目标选项混用。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性（feature）。若未给出特性选项，则为每个所选包激活 `default` 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)
了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-test--F"><a class="option-anchor" href="#option-cargo-test--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-test---features"><a class="option-anchor" href="#option-cargo-test---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>要激活的特性列表，以空格或逗号分隔。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，将启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-test---all-features"><a class="option-anchor" href="#option-cargo-test---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-test---no-default-features"><a class="option-anchor" href="#option-cargo-test---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-test---target"><a class="option-anchor" href="#option-cargo-test---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>Test for the specified target architecture. Flag may be specified multiple times. The default is the host architecture. triple 的一般格式为
<code>&lt;arch&gt;&lt;sub&gt;-&lt;vendor&gt;-&lt;sys&gt;-&lt;abi&gt;</code>。</p>
<p>可能的值：</p>
<ul>
<li><code>rustc --print target-list</code> 中任何受支持的目标。</li>
<li><code>"host-tuple"</code>，内部会替换为主机目标。若你在交叉编译某些 crate，又不想把主机机器指定为目标（例如可能由多台主机协作的共享项目中的 <code>xtask</code>），这会特别有用。</li>
<li>自定义目标规范的路径。更多信息见 <a href="https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path">自定义目标查找路径</a>。</li>
</ul>
<p>也可通过 <code>build.target</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
<p>注意：指定此标志会使 Cargo 以不同模式运行，目标产物会放在单独目录中。详情见
<a href="../../cargo-reference/09-build-cache.md">构建缓存</a>文档。</p>
</dd>


<dt class="option-term" id="option-cargo-test--r"><a class="option-anchor" href="#option-cargo-test--r"><code>-r</code></a></dt>
<dt class="option-term" id="option-cargo-test---release"><a class="option-anchor" href="#option-cargo-test---release"><code>--release</code></a></dt>
<dd class="option-desc"><p>使用 <code>release</code> 配置文件测试优化后的产物。
也可使用 <code>--profile</code> 选项按名称选择特定配置文件。</p>
</dd>


<dt class="option-term" id="option-cargo-test---profile"><a class="option-anchor" href="#option-cargo-test---profile"><code>--profile</code> <em>name</em></a></dt>
<dd class="option-desc"><p>使用给定的配置文件测试。
关于配置文件的更多详情见<a href="../../cargo-reference/05-profiles.md">参考文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-test---timings"><a class="option-anchor" href="#option-cargo-test---timings"><code>--timings</code></a></dt>
<dd class="option-desc"><p>输出每次编译耗时信息，并跟踪一段时间内的并发信息。</p>
<p>构建结束时会将 <code>cargo-timing.html</code> 文件写入 <code>target/cargo-timings</code>
目录。还会写入一份文件名带时间戳的额外报告，便于查看先前运行。
这些报告仅供人阅读，不提供机器可读的耗时数据。</p>
</dd>



</dl>

### 输出选项 {#output-options}
<dl>
<dt class="option-term" id="option-cargo-test---target-dir"><a class="option-anchor" href="#option-cargo-test---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或
<code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。
默认为工作空间根目录下的 <code>target</code>。</p>
</dd>

</dl>

### 显示选项 {#display-options}
默认情况下，Rust 测试框架会隐藏测试执行的输出以保持结果可读。可通过向测试二进制传递 `--no-capture` 来恢复测试输出（例如用于调试）：

    cargo test -- --no-capture

<dl>

<dt class="option-term" id="option-cargo-test--v"><a class="option-anchor" href="#option-cargo-test--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-test---verbose"><a class="option-anchor" href="#option-cargo-test---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-test--q"><a class="option-anchor" href="#option-cargo-test--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-test---quiet"><a class="option-anchor" href="#option-cargo-test---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-test---color"><a class="option-anchor" href="#option-cargo-test---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code> （默认）： 自动检测终端是否支持颜色。</li>
<li><code>always</code>: 始终显示颜色。</li>
<li><code>never</code>: 从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-test---message-format"><a class="option-anchor" href="#option-cargo-test---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
<dd class="option-desc"><p>诊断消息的输出格式。可指定多次，由逗号分隔的值组成。有效值：</p>
<ul>
<li><code>human</code> （默认）： 以人类可读的文本格式显示。与 <code>short</code> 和 <code>json</code> 冲突。</li>
<li><code>short</code>: 发出更短的人类可读文本消息。与 <code>human</code> 和 <code>json</code> 冲突。</li>
<li><code>json</code>: 向 stdout 发出 JSON 消息。详情见
<a href="../../cargo-reference/11-external-tools.md#json-messages">参考文档</a>。
与 <code>human</code> 和 <code>short</code> 冲突。</li>
<li><code>json-diagnostic-short</code>: 确保 JSON 消息的 <code>rendered</code> 字段包含 rustc 的「short」渲染。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-diagnostic-rendered-ansi</code>: 确保 JSON 消息的 <code>rendered</code> 字段包含嵌入的 ANSI 颜色代码，以遵循 rustc 的默认配色方案。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-render-diagnostics</code>: 指示 Cargo 不要在打印的 JSON 消息中包含 rustc 诊断，而是由 Cargo 自身渲染来自 rustc 的 JSON 诊断。Cargo 自己的 JSON 诊断以及来自 rustc 的其他内容仍会发出。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
</ul>
</dd>


</dl>

### Manifest 选项 {#manifest-options}
<dl>

<dt class="option-term" id="option-cargo-test---manifest-path"><a class="option-anchor" href="#option-cargo-test---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 会在当前目录或其任意父目录中搜索 <code>Cargo.toml</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-test---ignore-rust-version"><a class="option-anchor" href="#option-cargo-test---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-test---locked"><a class="option-anchor" href="#option-cargo-test---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-test---offline"><a class="option-anchor" href="#option-cargo-test---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-test---frozen"><a class="option-anchor" href="#option-cargo-test---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-test-+toolchain"><a class="option-anchor" href="#option-cargo-test-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-test---config"><a class="option-anchor" href="#option-cargo-test---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-test--C"><a class="option-anchor" href="#option-cargo-test--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-test--h"><a class="option-anchor" href="#option-cargo-test--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-test---help"><a class="option-anchor" href="#option-cargo-test---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-test--Z"><a class="option-anchor" href="#option-cargo-test--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

### 杂项选项 {#miscellaneous-options}
`--jobs` 参数影响测试可执行文件的构建，但不影响运行测试时使用的线程数。Rust 测试框架包含用于控制线程数的选项：

    cargo test -j 2 -- --test-threads=2

<dl>

<dt class="option-term" id="option-cargo-test--j"><a class="option-anchor" href="#option-cargo-test--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-test---jobs"><a class="option-anchor" href="#option-cargo-test---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为
逻辑 CPU 数量。若为负数，则将并行作业上限设为逻辑 CPU 数加上所给值。若
提供字符串 <code>default</code>，则恢复为默认值。
不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-test---future-incompat-report"><a class="option-anchor" href="#option-cargo-test---future-incompat-report"><code>--future-incompat-report</code></a></dt>
<dd class="option-desc"><p>对本命令执行期间产生的任何未来不兼容警告显示未来不兼容报告</p>
<p>参见 <a href="../report-commands/01-cargo-report.md">cargo-report(1)</a></p>
</dd>


</dl>

虽然 `cargo test` 涉及编译，但它不提供 `--keep-going` 标志。使用 `--no-fail-fast` 可在不停在第一个失败处的情况下尽可能多地运行测试。若要尽可能多地「编译」测试，可使用 `--tests` 单独构建测试二进制。例如：

    cargo build --tests --keep-going
    cargo test --tests --no-fail-fast

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/) 了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`: Cargo 成功完成。
* `101`: Cargo 未能完成。

## 示例 {#examples}
1. 执行当前包的所有单元测试与集成测试：

       cargo test

2. 仅运行名称匹配过滤字符串的测试：

       cargo test name_filter

3. 仅运行特定集成测试中的某个测试：

       cargo test --test int_test_name -- modname::test_name

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、[cargo-bench(1)](../01-cargo-bench/)、[测试类型](../../../cargo-reference/the-manifest-format/01-cargo-targets/#tests)、[如何编写测试](https://doc.rust-lang.org/rustc/tests/index.html)
