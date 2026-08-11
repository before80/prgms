+++
title = "03-cargo check"
date = 2026-07-30T14:49:00+08:00
weight = 48
type = "docs"
description = "cargo-check(1) 检查包能否编译"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-check(1) {#cargo-check1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-check.html](https://doc.rust-lang.org/cargo/commands/cargo-check.html)


## 名称 {#name}
cargo-check --- 检查当前包

## 大纲 {#synopsis}
`cargo check` [_options_]

## 描述 {#description}
检查本地包及其所有依赖是否有错误。这实质上会编译这些包，但不执行最终的代码生成步骤，因此比运行 `cargo build` 更快。编译器会将元数据文件保存到磁盘，以便在源文件未修改时后续运行可复用它们。某些诊断与错误仅在代码生成期间发出，因此本质上不会被 `cargo check` 报告。

## 选项 {#options}
### 包选择 {#package-selection}
默认情况下，若未给出包选择选项，所选包取决于所选清单文件（若未给出 `--manifest-path`，则基于当前工作目录）。若清单是工作空间根，则选择该工作空间的默认成员；否则仅选择清单所定义的包。

工作空间的默认成员可通过根清单中的 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间将仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-check--p"><a class="option-anchor" href="#option-cargo-check--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-check---package"><a class="option-anchor" href="#option-cargo-check---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>仅检查指定的包。SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-check---workspace"><a class="option-anchor" href="#option-cargo-check---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>检查工作空间中的所有成员。</p>
</dd>


<dt class="option-term" id="option-cargo-check---all"><a class="option-anchor" href="#option-cargo-check---all"><code>--all</code></a></dt>
<dd class="option-desc"><p><code>--workspace</code> 的已弃用别名。</p>
</dd>


<dt class="option-term" id="option-cargo-check---exclude"><a class="option-anchor" href="#option-cargo-check---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 目标选择 {#target-selection}
若未给出目标选择选项，`cargo check` 将检查所选包的所有二进制与库目标。若二进制目标缺少其 `required-features`，则会被跳过。

传入目标选择标志将仅检查指定的目标。

注意：`--bin`、`--example`、`--test` 和 `--bench` 标志也支持常见的 Unix glob 模式，如 `*`、`?` 和 `[]`。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个 glob 模式。

<dl>

<dt class="option-term" id="option-cargo-check---lib"><a class="option-anchor" href="#option-cargo-check---lib"><code>--lib</code></a></dt>
<dd class="option-desc"><p>检查包的库。</p>
</dd>


<dt class="option-term" id="option-cargo-check---bin"><a class="option-anchor" href="#option-cargo-check---bin"><code>--bin</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>检查指定的二进制目标。此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-check---bins"><a class="option-anchor" href="#option-cargo-check---bins"><code>--bins</code></a></dt>
<dd class="option-desc"><p>检查所有二进制目标。</p>
</dd>


<dt class="option-term" id="option-cargo-check---example"><a class="option-anchor" href="#option-cargo-check---example"><code>--example</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>检查指定的示例。此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-check---examples"><a class="option-anchor" href="#option-cargo-check---examples"><code>--examples</code></a></dt>
<dd class="option-desc"><p>检查所有示例目标。</p>
</dd>


<dt class="option-term" id="option-cargo-check---test"><a class="option-anchor" href="#option-cargo-check---test"><code>--test</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>检查指定的集成测试。此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-check---tests"><a class="option-anchor" href="#option-cargo-check---tests"><code>--tests</code></a></dt>
<dd class="option-desc"><p>检查所有在清单中设置了 <code>test = true</code> 标志的目标。默认包括作为单元测试构建的库与二进制目标，以及集成测试。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为单元测试，一次作为二进制、集成测试等的依赖）。可通过在目标的清单设置中设置 <code>test</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-check---bench"><a class="option-anchor" href="#option-cargo-check---bench"><code>--bench</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>检查指定的基准测试。此标志可指定多次，并支持常见的 Unix glob 模式。</p>
</dd>


<dt class="option-term" id="option-cargo-check---benches"><a class="option-anchor" href="#option-cargo-check---benches"><code>--benches</code></a></dt>
<dd class="option-desc"><p>检查所有在清单中设置了 <code>bench = true</code> 标志的目标。默认包括作为基准测试构建的库与二进制目标，以及 bench 目标。请注意这也会构建任何所需依赖，因此 lib 目标可能会被构建两次（一次作为基准测试，一次作为二进制、基准测试等的依赖）。可通过在目标的清单设置中设置 <code>bench</code> 标志来启用或禁用目标。</p>
</dd>


<dt class="option-term" id="option-cargo-check---all-targets"><a class="option-anchor" href="#option-cargo-check---all-targets"><code>--all-targets</code></a></dt>
<dd class="option-desc"><p>检查所有目标。等价于指定 <code>--lib --bins --tests --benches --examples</code>。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性（feature）。若未给出特性选项，则为每个所选包激活 `default` 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-check--F"><a class="option-anchor" href="#option-cargo-check--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-check---features"><a class="option-anchor" href="#option-cargo-check---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>要激活的特性列表，以空格或逗号分隔。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，将启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-check---all-features"><a class="option-anchor" href="#option-cargo-check---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-check---no-default-features"><a class="option-anchor" href="#option-cargo-check---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-check---target"><a class="option-anchor" href="#option-cargo-check---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>为指定的目标架构检查。此标志可指定多次。默认为主机架构。triple 的一般格式为
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


<dt class="option-term" id="option-cargo-check--r"><a class="option-anchor" href="#option-cargo-check--r"><code>-r</code></a></dt>
<dt class="option-term" id="option-cargo-check---release"><a class="option-anchor" href="#option-cargo-check---release"><code>--release</code></a></dt>
<dd class="option-desc"><p>使用 <code>release</code> 配置文件检查优化后的产物。
也可使用 <code>--profile</code> 选项按名称选择特定配置文件。</p>
</dd>


<dt class="option-term" id="option-cargo-check---profile"><a class="option-anchor" href="#option-cargo-check---profile"><code>--profile</code> <em>name</em></a></dt>
<dd class="option-desc"><p>使用给定的配置文件检查。
关于配置文件的更多详情见<a href="../../cargo-reference/05-profiles.md">参考文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-check---timings"><a class="option-anchor" href="#option-cargo-check---timings"><code>--timings</code></a></dt>
<dd class="option-desc"><p>输出每次编译耗时信息，并跟踪一段时间内的并发信息。</p>
<p>构建结束时会将 <code>cargo-timing.html</code> 文件写入 <code>target/cargo-timings</code>
目录。还会写入一份文件名带时间戳的额外报告，便于查看先前运行。
这些报告仅供人阅读，不提供机器可读的耗时数据。</p>
</dd>



</dl>

### 输出选项 {#output-options}
<dl>
<dt class="option-term" id="option-cargo-check---target-dir"><a class="option-anchor" href="#option-cargo-check---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或
<code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。
默认为工作空间根目录下的 <code>target</code>。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-check--v"><a class="option-anchor" href="#option-cargo-check--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-check---verbose"><a class="option-anchor" href="#option-cargo-check---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-check--q"><a class="option-anchor" href="#option-cargo-check--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-check---quiet"><a class="option-anchor" href="#option-cargo-check---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-check---color"><a class="option-anchor" href="#option-cargo-check---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code>（默认）：自动检测终端是否支持颜色。</li>
<li><code>always</code>：始终显示颜色。</li>
<li><code>never</code>：从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-check---message-format"><a class="option-anchor" href="#option-cargo-check---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
<dd class="option-desc"><p>诊断消息的输出格式。可指定多次，由逗号分隔的值组成。有效值：</p>
<ul>
<li><code>human</code>（默认）：以人类可读的文本格式显示。与 <code>short</code> 和 <code>json</code> 冲突。</li>
<li><code>short</code>：发出更短的人类可读文本消息。与 <code>human</code> 和 <code>json</code> 冲突。</li>
<li><code>json</code>：向 stdout 发出 JSON 消息。详情见
<a href="../../cargo-reference/11-external-tools.md#json-messages">参考文档</a>。
与 <code>human</code> 和 <code>short</code> 冲突。</li>
<li><code>json-diagnostic-short</code>：确保 JSON 消息的 <code>rendered</code> 字段包含 rustc 的「short」渲染。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-diagnostic-rendered-ansi</code>：确保 JSON 消息的 <code>rendered</code> 字段包含嵌入的 ANSI 颜色代码，以遵循 rustc 的默认配色方案。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-render-diagnostics</code>：指示 Cargo 不要在打印的 JSON 消息中包含 rustc 诊断，而是由 Cargo 自身渲染来自 rustc 的 JSON 诊断。Cargo 自己的 JSON 诊断以及来自 rustc 的其他内容仍会发出。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
</ul>
</dd>


</dl>

### Manifest 选项 {#manifest-options}
<dl>
<dt class="option-term" id="option-cargo-check---manifest-path"><a class="option-anchor" href="#option-cargo-check---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 会在当前目录或其任意父目录中搜索 <code>Cargo.toml</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-check---ignore-rust-version"><a class="option-anchor" href="#option-cargo-check---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-check---locked"><a class="option-anchor" href="#option-cargo-check---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-check---offline"><a class="option-anchor" href="#option-cargo-check---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-check---frozen"><a class="option-anchor" href="#option-cargo-check---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-check-+toolchain"><a class="option-anchor" href="#option-cargo-check-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-check---config"><a class="option-anchor" href="#option-cargo-check---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-check--C"><a class="option-anchor" href="#option-cargo-check--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-check--h"><a class="option-anchor" href="#option-cargo-check--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-check---help"><a class="option-anchor" href="#option-cargo-check---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-check--Z"><a class="option-anchor" href="#option-cargo-check--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

### 杂项选项 {#miscellaneous-options}
<dl>
<dt class="option-term" id="option-cargo-check--j"><a class="option-anchor" href="#option-cargo-check--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-check---jobs"><a class="option-anchor" href="#option-cargo-check---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为
逻辑 CPU 数量。若为负数，则将并行作业上限设为逻辑 CPU 数加上所给值。若
提供字符串 <code>default</code>，则恢复为默认值。
不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-check---keep-going"><a class="option-anchor" href="#option-cargo-check---keep-going"><code>--keep-going</code></a></dt>
<dd class="option-desc"><p>尽可能检查依赖图中的更多 crate，而不是在第一个失败时中止。</p>
<p>例如，若当前包依赖 <code>fails</code> 与 <code>works</code>，
其中之一构建失败，则 <code>cargo check -j1</code> 可能构建也可能不构建成功的那个
（取决于 Cargo 先运行哪一个），而 <code>cargo check -j1 --keep-going</code> 肯定会运行两者，
即便先运行的那个失败。</p>
</dd>

<dt class="option-term" id="option-cargo-check---future-incompat-report"><a class="option-anchor" href="#option-cargo-check---future-incompat-report"><code>--future-incompat-report</code></a></dt>
<dd class="option-desc"><p>对本命令执行期间产生的任何未来不兼容警告显示未来不兼容报告</p>
<p>参见 <a href="../report-commands/01-cargo-report.md">cargo-report(1)</a></p>
</dd>

</dl>

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/)了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`：Cargo 成功完成。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 检查本地包及其所有依赖：

       cargo check

2. 以优化方式检查：

       cargo check --release

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、[cargo-build(1)](../02-cargo-build/)
