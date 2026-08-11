+++
title = "11-cargo run"
date = 2026-07-30T14:49:00+08:00
weight = 56
type = "docs"
description = "cargo-run(1) 运行二进制目标"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-run(1) {#cargo-run1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-run.html](https://doc.rust-lang.org/cargo/commands/cargo-run.html)


## 名称 {#name}
cargo-run --- 运行当前包

## 大纲 {#synopsis}
`cargo run` [_options_] [`--` _args_]

## 描述 {#description}
运行本地包的二进制目标或示例。

两个短划线（`--`）之后的所有参数都会传给要运行的二进制程序。若同时向 Cargo 与二进制程序传参，则 `--` 之后的参数传给二进制，之前的传给 Cargo。

与 [cargo-test(1)](../14-cargo-test/) 和 [cargo-bench(1)](../01-cargo-bench/) 不同，`cargo run` 将所执行二进制的工作目录设为当前工作目录，就如同直接在 shell 中执行一样。

## 选项 {#options}
### 包选择 {#package-selection}
默认选择当前工作目录中的包。可用 `-p` 标志选择工作空间中的其他包。

<dl>

<dt class="option-term" id="option-cargo-run--p"><a class="option-anchor" href="#option-cargo-run--p"><code>-p</code> <em>spec</em></a></dt>
<dt class="option-term" id="option-cargo-run---package"><a class="option-anchor" href="#option-cargo-run---package"><code>--package</code> <em>spec</em></a></dt>
<dd class="option-desc"><p>要运行的包。 SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。</p>
</dd>


</dl>

### 目标选择 {#target-selection}
若未给出目标选择选项，`cargo run` 将运行二进制目标。若有多个二进制目标，必须传入目标标志以选择其一。或者，可在 `Cargo.toml` 的 `[package]` 节中指定 `default-run` 字段，以选择默认运行的二进制名称。

<dl>

<dt class="option-term" id="option-cargo-run---bin"><a class="option-anchor" href="#option-cargo-run---bin"><code>--bin</code> <em>name</em></a></dt>
<dd class="option-desc"><p>运行指定的二进制目标。</p>
</dd>


<dt class="option-term" id="option-cargo-run---example"><a class="option-anchor" href="#option-cargo-run---example"><code>--example</code> <em>name</em></a></dt>
<dd class="option-desc"><p>运行指定的示例。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性（feature）。若未给出特性选项，则为每个所选包激活 `default` 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)
了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-run--F"><a class="option-anchor" href="#option-cargo-run--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-run---features"><a class="option-anchor" href="#option-cargo-run---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>要激活的特性列表，以空格或逗号分隔。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，将启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-run---all-features"><a class="option-anchor" href="#option-cargo-run---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-run---no-default-features"><a class="option-anchor" href="#option-cargo-run---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-run---target"><a class="option-anchor" href="#option-cargo-run---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>Run for the specified target architecture. The default is the host architecture. triple 的一般格式为
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


<dt class="option-term" id="option-cargo-run--r"><a class="option-anchor" href="#option-cargo-run--r"><code>-r</code></a></dt>
<dt class="option-term" id="option-cargo-run---release"><a class="option-anchor" href="#option-cargo-run---release"><code>--release</code></a></dt>
<dd class="option-desc"><p>使用 <code>release</code> 配置文件运行优化后的产物。
也可使用 <code>--profile</code> 选项按名称选择特定配置文件。</p>
</dd>


<dt class="option-term" id="option-cargo-run---profile"><a class="option-anchor" href="#option-cargo-run---profile"><code>--profile</code> <em>name</em></a></dt>
<dd class="option-desc"><p>使用给定的配置文件运行。
关于配置文件的更多详情见<a href="../../cargo-reference/05-profiles.md">参考文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-run---timings"><a class="option-anchor" href="#option-cargo-run---timings"><code>--timings</code></a></dt>
<dd class="option-desc"><p>输出每次编译耗时信息，并跟踪一段时间内的并发信息。</p>
<p>构建结束时会将 <code>cargo-timing.html</code> 文件写入 <code>target/cargo-timings</code>
目录。还会写入一份文件名带时间戳的额外报告，便于查看先前运行。
这些报告仅供人阅读，不提供机器可读的耗时数据。</p>
</dd>



</dl>

### 输出选项 {#output-options}
<dl>
<dt class="option-term" id="option-cargo-run---target-dir"><a class="option-anchor" href="#option-cargo-run---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或
<code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。
默认为工作空间根目录下的 <code>target</code>。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>

<dt class="option-term" id="option-cargo-run--v"><a class="option-anchor" href="#option-cargo-run--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-run---verbose"><a class="option-anchor" href="#option-cargo-run---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-run--q"><a class="option-anchor" href="#option-cargo-run--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-run---quiet"><a class="option-anchor" href="#option-cargo-run---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-run---color"><a class="option-anchor" href="#option-cargo-run---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code> （默认）： 自动检测终端是否支持颜色。</li>
<li><code>always</code>: 始终显示颜色。</li>
<li><code>never</code>: 从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-run---message-format"><a class="option-anchor" href="#option-cargo-run---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
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

<dt class="option-term" id="option-cargo-run---manifest-path"><a class="option-anchor" href="#option-cargo-run---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 会在当前目录或其任意父目录中搜索 <code>Cargo.toml</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-run---ignore-rust-version"><a class="option-anchor" href="#option-cargo-run---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-run---locked"><a class="option-anchor" href="#option-cargo-run---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-run---offline"><a class="option-anchor" href="#option-cargo-run---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-run---frozen"><a class="option-anchor" href="#option-cargo-run---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-run-+toolchain"><a class="option-anchor" href="#option-cargo-run-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-run---config"><a class="option-anchor" href="#option-cargo-run---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-run--C"><a class="option-anchor" href="#option-cargo-run--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-run--h"><a class="option-anchor" href="#option-cargo-run--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-run---help"><a class="option-anchor" href="#option-cargo-run---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-run--Z"><a class="option-anchor" href="#option-cargo-run--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

### 杂项选项 {#miscellaneous-options}
<dl>
<dt class="option-term" id="option-cargo-run--j"><a class="option-anchor" href="#option-cargo-run--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-run---jobs"><a class="option-anchor" href="#option-cargo-run---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为
逻辑 CPU 数量。若为负数，则将并行作业上限设为逻辑 CPU 数加上所给值。若
提供字符串 <code>default</code>，则恢复为默认值。
不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-run---keep-going"><a class="option-anchor" href="#option-cargo-run---keep-going"><code>--keep-going</code></a></dt>
<dd class="option-desc"><p>尽可能构建依赖图中的更多 crate，而不是在第一个构建失败时中止。</p>
<p>例如，若当前包依赖 <code>fails</code> 与 <code>works</code>，
其中之一构建失败，则 <code>cargo run -j1</code> 可能构建也可能不构建成功的那个
（取决于 Cargo 先运行哪一个），而 <code>cargo run -j1 --keep-going</code> 肯定会运行两者，
即便先运行的那个失败。</p>
</dd>

</dl>

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/) 了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`: Cargo 成功完成。
* `101`: Cargo 未能完成。

## 示例 {#examples}
1. 构建本地包并运行其主目标（假设只有一个二进制）：

       cargo run

2. 运行带额外参数的示例：

       cargo run --example exname -- --exoption exarg1 exarg2

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、[cargo-build(1)](../02-cargo-build/)
