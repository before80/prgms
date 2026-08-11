+++
title = "02-cargo report future-incompatibilities"
date = 2026-07-30T14:49:00+08:00
weight = 86
type = "docs"
description = "报告未来不兼容性"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-report-future-incompatibilities(1) {#cargo-report-future-incompatibilities1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-report-future-incompatibilities.html](https://doc.rust-lang.org/cargo/commands/cargo-report-future-incompatibilities.html)


## 名称 {#name}
cargo-report-future-incompatibilities --- 报告最终将停止编译的 crate

## 大纲 {#synopsis}
`cargo report future-incompatibilities` [_options_]

## 描述 {#description}
显示先前构建期间发出的未来不兼容警告报告。
这些是关于将来可能变成硬错误的变更的警告，
会导致依赖在未来版本的 rustc 中停止构建。

更多信息见[未来不兼容报告](../../../cargo-reference/14-future-incompat-report/)一章。

## 选项 {#options}
<dl>

<dt class="option-term" id="option-cargo-report-future-incompatibilities---id"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---id"><code>--id</code> <em>id</em></a></dt>
<dd class="option-desc"><p>显示具有指定 Cargo 生成 id 的报告。
若未指定，显示最近的报告。</p>
</dd>


</dl>

### 包选择 {#package-selection}
默认选择当前工作目录中的包。可用 `-p`
标志选择工作空间中的其他包。

<dl>

<dt class="option-term" id="option-cargo-report-future-incompatibilities--p"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--p"><code>-p</code> <em>spec</em></a></dt>
<dt class="option-term" id="option-cargo-report-future-incompatibilities---package"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---package"><code>--package</code> <em>spec</em></a></dt>
<dd class="option-desc"><p>要显示报告的包。SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-report-future-incompatibilities--v"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-report-future-incompatibilities---verbose"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities--q"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-report-future-incompatibilities---quiet"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities---color"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code>（默认）：自动检测终端是否支持颜色。</li>
<li><code>always</code>：始终显示颜色。</li>
<li><code>never</code>：从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>

</dl>

### 清单选项 {#manifest-options}
<dl>
<dt class="option-term" id="option-cargo-report-future-incompatibilities---locked"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities---offline"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities---frozen"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-report-future-incompatibilities-+toolchain"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities---config"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities--C"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities--h"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-report-future-incompatibilities---help"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-report-future-incompatibilities--Z"><a class="option-anchor" href="#option-cargo-report-future-incompatibilities--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 显示最新的未来不兼容报告：

       cargo report future-incompat

2. 显示特定包的最新未来不兼容报告：

       cargo report future-incompat --package my-dep@0.0.1

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-report(1)](../01-cargo-report/), [cargo-build(1)](../../build-commands/02-cargo-build/)
