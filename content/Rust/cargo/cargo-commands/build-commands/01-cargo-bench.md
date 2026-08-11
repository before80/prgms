+++
title = "01-cargo bench"
date = 2026-07-30T14:49:00+08:00
weight = 46
type = "docs"
description = "cargo-bench(1) 运行基准测试"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-bench(1) {#cargo-bench1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-bench.html](https://doc.rust-lang.org/cargo/commands/cargo-bench.html)


## 名称 {#name}
cargo-bench --- 执行包的基准测试

## 大纲 {#synopsis}
`cargo bench` [_options_] [_benchname_] [`--` _bench-options_]

## 描述 {#description}
编译并执行基准测试。

基准测试过滤参数 _benchname_ 以及两个短划线（`--`）之后的所有参数都会传给基准测试二进制，进而传给 _libtest_（rustc 内置的单元测试与微基准测试框架）。若同时向 Cargo 与二进制传参，则 `--` 之后的参数传给二进制，之前的传给 Cargo。关于 libtest 参数的详情，请参见 `cargo bench -- --help` 的输出，以及 rustc 手册中关于测试工作原理的章节：
<https://doc.rust-lang.org/rustc/tests/index.html>。

例如，以下命令仅运行名为 `foo` 的基准测试（并跳过如 `foobar` 等名称相似的其他基准测试）：

    cargo bench -- foo --exact

基准测试使用 `rustc` 的 `--test` 选项构建，通过将你的代码与 libtest 链接来创建特殊可执行文件。该可执行文件会自动运行所有标注了 `#[bench]` 属性的函数。Cargo 向测试框架传递 `--bench` 标志，告知其仅运行基准测试，无论框架是 libtest 还是自定义框架。

可通过在目标清单设置中将 `harness = false` 来禁用 libtest 框架，此时你的代码需要提供自己的 `main` 函数来处理基准测试的运行。

> **注意**：
> [`#[bench]` 属性](https://doc.rust-lang.org/nightly/unstable-book/library-features/test.html)
> 目前不稳定，仅在
> [nightly 通道](https://doc.rust-lang.org/book/appendix-07-nightly-rust.html) 可用。
> [crates.io](https://crates.io/keywords/benchmark) 上有一些包可帮助在
> stable 通道上运行基准测试，例如
> [Criterion](https://crates.io/crates/criterion)。

默认情况下，`cargo bench` 使用 [`bench` 配置文件]，它会启用优化并禁用调试信息。若需要调试基准测试，可使用 `--profile=dev` 命令行选项切换到 dev 配置文件，然后在调试器中运行启用了调试的基准测试。

[`bench` 配置文件]: ../../../cargo-reference/05-profiles/#bench

### 基准测试的工作目录 {#working-directory-of-benchmarks}
每个基准测试的工作目录都设为该基准测试所属包的根目录。
将基准测试的工作目录设为包的根目录，使基准测试能够使用相对路径可靠地访问包的文件，而无论从何处执行 `cargo bench`。

## 选项 {#options}
### 基准测试选项 {#benchmark-options}
<dl>

<dt class="option-term" id="option-cargo-bench---no-run"><a class="option-anchor" href="#option-cargo-bench---no-run"><code>--no-run</code></a></dt>
<dd class="option-desc"><p>编译但不运行基准测试。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---no-fail-fast"><a class="option-anchor" href="#option-cargo-bench---no-fail-fast"><code>--no-fail-fast</code></a></dt>
<dd class="option-desc"><p>无论失败与否都运行所有基准测试。若不带此标志，Cargo 会在第一个可执行文件失败后退出。Rust 测试框架会运行可执行文件内的全部基准测试直至完成；此标志仅作用于整个可执行文件。</p>
</dd>


</dl>

### 包选择 {#package-selection}
默认情况下，若未给出包选择选项，所选包取决于所选清单文件（若未给出 `--manifest-path`，则基于当前工作目录）。若清单是工作空间根，则选择该工作空间的默认成员；否则仅选择清单所定义的包。

工作空间的默认成员可通过根清单中的 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间将仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-bench--p"><a class="option-anchor" href="#option-cargo-bench--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-bench---package"><a class="option-anchor" href="#option-cargo-bench---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>Benchmark only the specified packages. SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。 此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---workspace"><a class="option-anchor" href="#option-cargo-bench---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>对工作空间中的所有成员运行基准测试。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---all"><a class="option-anchor" href="#option-cargo-bench---all"><code>--all</code></a></dt>
<dd class="option-desc"><p><code>--workspace</code> 的已弃用别名。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---exclude"><a class="option-anchor" href="#option-cargo-bench---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。 此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 目标选择 {#target-selection}
若未给出目标选择选项，`cargo bench` 将构建所选包的以下目标：

- lib --- 用于与二进制和基准测试链接
- bins（仅当构建基准测试目标且所需特性可用时）
- 作为基准测试的 lib
- 作为基准测试的 bins
- 基准测试目标

可通过在清单设置中为目标设置 `bench` 标志来更改默认行为。将示例设为 `bench = true` 会将该示例作为基准测试构建并运行，用 libtest 框架替换示例的 `main` 函数。

将目标设为 `bench = false` 会停止默认对它们进行基准测试。按名称选取目标的目标选择选项（如 `--example foo`）会忽略 `bench` 标志，并始终对给定目标运行基准测试。

参见[配置目标](../../../cargo-reference/the-manifest-format/01-cargo-targets/#configuring-a-target)
了解更多关于各目标设置的信息。

若选择对集成测试或基准测试做基准测试，则会自动构建二进制目标。这样集成测试可以执行该二进制以演练并测试其行为。
在构建并运行集成测试时会设置 `CARGO_BIN_EXE_<name>`
[环境变量](../../../cargo-reference/07-environment-variables/#environment-variables-cargo-sets-for-crates)，
以便测试可使用 [`env` 宏](https://doc.rust-lang.org/std/macro.env.html) 或
[`var` 函数](https://doc.rust-lang.org/std/env/fn.var.html) 定位可执行文件。

传入目标选择标志将仅对指定目标运行基准测试。 

注意：`--bin`、`--example`、`--test` 和 `--bench` 标志也支持常见的 Unix glob 模式，如 `*`、`?` 和 `[]`。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个 glob 模式。

<dl>

<dt class="option-term" id="option-cargo-bench---lib"><a class="option-anchor" href="#option-cargo-bench---lib"><code>--lib</code></a></dt>
<dd class="option-desc"><p>对包的库运行基准测试。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---bin"><a class="option-anchor" href="#option-cargo-bench---bin"><code>--bin</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>对指定的二进制目标运行基准测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---bins"><a class="option-anchor" href="#option-cargo-bench---bins"><code>--bins</code></a></dt>
<dd class="option-desc"><p>对所有二进制目标运行基准测试。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---example"><a class="option-anchor" href="#option-cargo-bench---example"><code>--example</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>对指定的示例运行基准测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---examples"><a class="option-anchor" href="#option-cargo-bench---examples"><code>--examples</code></a></dt>
<dd class="option-desc"><p>对所有示例目标运行基准测试。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---test"><a class="option-anchor" href="#option-cargo-bench---test"><code>--test</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>对指定的集成测试运行基准测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---tests"><a class="option-anchor" href="#option-cargo-bench---tests"><code>--tests</code></a></dt>
<dd class="option-desc"><p>对所有在清单中设置了 <code>test = true</code> 标志的目标运行基准测试。默认包括作为单元测试构建的库与二进制目标，以及集成测试。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为单元测试，一次作为二进制、集成测试等的依赖）。可通过在目标的清单设置中设置 <code>test</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---bench"><a class="option-anchor" href="#option-cargo-bench---bench"><code>--bench</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>对指定的基准测试运行基准测试。 此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---benches"><a class="option-anchor" href="#option-cargo-bench---benches"><code>--benches</code></a></dt>
<dd class="option-desc"><p>对所有在清单中设置了 <code>bench = true</code> 标志的目标运行基准测试。默认包括作为基准测试构建的库与二进制目标，以及 bench 目标。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为基准测试，一次作为二进制、基准测试等的依赖）。可通过在目标的清单设置中设置 <code>bench</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---all-targets"><a class="option-anchor" href="#option-cargo-bench---all-targets"><code>--all-targets</code></a></dt>
<dd class="option-desc"><p>对所有目标运行基准测试。等价于指定 <code>--lib --bins --tests --benches --examples</code>。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性（feature）。若未给出特性选项，则为每个所选包激活 `default` 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)
了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-bench--F"><a class="option-anchor" href="#option-cargo-bench--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-bench---features"><a class="option-anchor" href="#option-cargo-bench---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>要激活的特性列表，以空格或逗号分隔。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，将启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---all-features"><a class="option-anchor" href="#option-cargo-bench---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---no-default-features"><a class="option-anchor" href="#option-cargo-bench---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-bench---target"><a class="option-anchor" href="#option-cargo-bench---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>Benchmark for the specified target architecture. Flag may be specified multiple times. The default is the host architecture. triple 的一般格式为
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


<dt class="option-term" id="option-cargo-bench---profile"><a class="option-anchor" href="#option-cargo-bench---profile"><code>--profile</code> <em>name</em></a></dt>
<dd class="option-desc"><p>使用给定的配置文件运行基准测试。
关于配置文件的更多详情见<a href="../../cargo-reference/05-profiles.md">参考文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---timings"><a class="option-anchor" href="#option-cargo-bench---timings"><code>--timings</code></a></dt>
<dd class="option-desc"><p>输出每次编译耗时信息，并跟踪一段时间内的并发信息。</p>
<p>构建结束时会将 <code>cargo-timing.html</code> 文件写入 <code>target/cargo-timings</code>
目录。还会写入一份文件名带时间戳的额外报告，便于查看先前运行。
这些报告仅供人阅读，不提供机器可读的耗时数据。</p>
</dd>



</dl>

### 输出选项 {#output-options}
<dl>
<dt class="option-term" id="option-cargo-bench---target-dir"><a class="option-anchor" href="#option-cargo-bench---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或
<code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。
默认为工作空间根目录下的 <code>target</code>。</p>
</dd>

</dl>

### 显示选项 {#display-options}
默认情况下，Rust 测试框架会隐藏基准测试执行的输出以保持结果可读。可通过向基准测试二进制传递 `--no-capture` 来恢复输出（例如用于调试）：

    cargo bench -- --no-capture

<dl>

<dt class="option-term" id="option-cargo-bench--v"><a class="option-anchor" href="#option-cargo-bench--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-bench---verbose"><a class="option-anchor" href="#option-cargo-bench---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-bench--q"><a class="option-anchor" href="#option-cargo-bench--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-bench---quiet"><a class="option-anchor" href="#option-cargo-bench---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---color"><a class="option-anchor" href="#option-cargo-bench---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code> （默认）： 自动检测终端是否支持颜色。</li>
<li><code>always</code>: 始终显示颜色。</li>
<li><code>never</code>: 从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---message-format"><a class="option-anchor" href="#option-cargo-bench---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
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
<dt class="option-term" id="option-cargo-bench---manifest-path"><a class="option-anchor" href="#option-cargo-bench---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 会在当前目录或其任意父目录中搜索 <code>Cargo.toml</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---ignore-rust-version"><a class="option-anchor" href="#option-cargo-bench---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---locked"><a class="option-anchor" href="#option-cargo-bench---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---offline"><a class="option-anchor" href="#option-cargo-bench---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---frozen"><a class="option-anchor" href="#option-cargo-bench---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-bench-+toolchain"><a class="option-anchor" href="#option-cargo-bench-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-bench---config"><a class="option-anchor" href="#option-cargo-bench---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-bench--C"><a class="option-anchor" href="#option-cargo-bench--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-bench--h"><a class="option-anchor" href="#option-cargo-bench--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-bench---help"><a class="option-anchor" href="#option-cargo-bench---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-bench--Z"><a class="option-anchor" href="#option-cargo-bench--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

### 杂项选项 {#miscellaneous-options}
`--jobs` 参数影响基准测试可执行文件的构建，但不影响运行基准测试时使用的线程数。Rust 测试框架在单线程中串行运行基准测试。

<dl>
<dt class="option-term" id="option-cargo-bench--j"><a class="option-anchor" href="#option-cargo-bench--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-bench---jobs"><a class="option-anchor" href="#option-cargo-bench---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为
逻辑 CPU 数量。若为负数，则将并行作业上限设为逻辑 CPU 数加上所给值。若
提供字符串 <code>default</code>，则恢复为默认值。
不应为 0。</p>
</dd>

</dl>

虽然 `cargo bench` 涉及编译，但它不提供 `--keep-going` 标志。使用 `--no-fail-fast` 可在不停在第一个失败处的情况下尽可能多地运行基准测试。若要尽可能多地「编译」基准测试，可使用 `--benches` 单独构建基准测试二进制。例如：

    cargo build --benches --release --keep-going
    cargo bench --no-fail-fast

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/) 了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`: Cargo 成功完成。
* `101`: Cargo 未能完成。

## 示例 {#examples}
1. 构建并执行当前包的所有基准测试：

       cargo bench

2. 仅运行特定基准测试目标中的某个基准测试：

       cargo bench --bench bench_name -- modname::some_benchmark

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、[cargo-test(1)](../14-cargo-test/)
