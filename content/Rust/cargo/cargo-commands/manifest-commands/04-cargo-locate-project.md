+++
title = "04-cargo locate-project"
date = 2026-07-30T14:49:00+08:00
weight = 64
type = "docs"
description = "cargo-locate-project(1) 定位清单路径"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-locate-project(1) {#cargo-locate-project1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-locate-project.html](https://doc.rust-lang.org/cargo/commands/cargo-locate-project.html)


## 名称 {#name}
cargo-locate-project --- 以 JSON 形式打印 Cargo.toml 文件的位置

## 大纲 {#synopsis}
`cargo locate-project` [_options_]

## 描述 {#description}
此命令会向标准输出打印一个 JSON 对象，其中包含清单的完整路径。
通过从当前工作目录开始向上搜索名为 `Cargo.toml` 的文件来找到清单。

若项目恰好属于某个工作空间，则输出该项目的清单，而非工作空间根。
可用 `--workspace` 标志覆盖。根工作空间通过继续向上遍历，
或在定位到工作空间成员的清单后使用字段 `package.workspace` 找到。

## 选项 {#options}
<dl>

<dt class="option-term" id="option-cargo-locate-project---workspace"><a class="option-anchor" href="#option-cargo-locate-project---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>定位工作空间根处的 <code>Cargo.toml</code>，而非当前工作空间成员。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-locate-project---message-format"><a class="option-anchor" href="#option-cargo-locate-project---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
<dd class="option-desc"><p>打印项目位置所用的表示形式。有效值：</p>
<ul>
<li><code>json</code>（默认）：JSON 对象，路径位于键 “root” 下。</li>
<li><code>plain</code>：仅路径。</li>
</ul>
</dd>

<dt class="option-term" id="option-cargo-locate-project--v"><a class="option-anchor" href="#option-cargo-locate-project--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-locate-project---verbose"><a class="option-anchor" href="#option-cargo-locate-project---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project--q"><a class="option-anchor" href="#option-cargo-locate-project--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-locate-project---quiet"><a class="option-anchor" href="#option-cargo-locate-project---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project---color"><a class="option-anchor" href="#option-cargo-locate-project---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo-locate-project---manifest-path"><a class="option-anchor" href="#option-cargo-locate-project---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索
<code>Cargo.toml</code> 文件。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-locate-project-+toolchain"><a class="option-anchor" href="#option-cargo-locate-project-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project---config"><a class="option-anchor" href="#option-cargo-locate-project---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project--C"><a class="option-anchor" href="#option-cargo-locate-project--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project--h"><a class="option-anchor" href="#option-cargo-locate-project--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-locate-project---help"><a class="option-anchor" href="#option-cargo-locate-project---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-locate-project--Z"><a class="option-anchor" href="#option-cargo-locate-project--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 基于当前目录显示清单路径：

       cargo locate-project

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-metadata(1)](../05-cargo-metadata/)
