+++
title = "02-cargo help"
date = 2026-07-30T14:49:00+08:00
weight = 43
type = "docs"
description = "cargo-help(1) 帮助命令"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-help(1) {#cargo-help1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-help.html](https://doc.rust-lang.org/cargo/commands/cargo-help.html)


## 名称 {#name}
cargo-help --- 获取 Cargo 命令的帮助

## 大纲 {#synopsis}
`cargo help` [_subcommand_]

## 描述 {#description}
打印给定命令的帮助消息。

对于带子命令的命令，用空格分隔命令层级。例如，`cargo help report future-incompatibilities` 显示
`cargo report future-incompatibilities` 命令的帮助。

空格仅用于分隔父命令与其子命令之间的层级。命令名本身中的连字符（如
`generate-lockfile`）必须始终保留。

多个命令层级也可写成用连字符连接的单个词。
例如，`cargo help report-future-incompatibilities` 等价于
`cargo help report future-incompatibilities`。

## 选项 {#options}
### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-help--v"><a class="option-anchor" href="#option-cargo-help--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-help---verbose"><a class="option-anchor" href="#option-cargo-help---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-help--q"><a class="option-anchor" href="#option-cargo-help--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-help---quiet"><a class="option-anchor" href="#option-cargo-help---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-help---color"><a class="option-anchor" href="#option-cargo-help---color"><code>--color</code> <em>when</em></a></dt>
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

### Manifest 选项 {#manifest-options}
<dl>
<dt class="option-term" id="option-cargo-help---locked"><a class="option-anchor" href="#option-cargo-help---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-help---offline"><a class="option-anchor" href="#option-cargo-help---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-help---frozen"><a class="option-anchor" href="#option-cargo-help---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-help-+toolchain"><a class="option-anchor" href="#option-cargo-help-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-help---config"><a class="option-anchor" href="#option-cargo-help---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-help--C"><a class="option-anchor" href="#option-cargo-help--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-help--h"><a class="option-anchor" href="#option-cargo-help--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-help---help"><a class="option-anchor" href="#option-cargo-help---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-help--Z"><a class="option-anchor" href="#option-cargo-help--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/)了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`：Cargo 成功完成。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 获取命令的帮助：

       cargo help build

2. 获取嵌套命令的帮助：

       cargo help report future-incompatibilities

3. 连字符连接形式同样有效：

       cargo help report-future-incompatibilities

4. 也可通过 `--help` 标志获取帮助：

       cargo build --help

## 参见 {#see-also}
[cargo(1)](../01-cargo/)
