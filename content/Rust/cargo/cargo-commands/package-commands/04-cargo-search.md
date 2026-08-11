+++
title = "04-cargo search"
date = 2026-07-30T14:49:00+08:00
weight = 75
type = "docs"
description = "cargo-search(1) 搜索 crates.io"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-search(1) {#cargo-search1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-search.html](https://doc.rust-lang.org/cargo/commands/cargo-search.html)


## 名称 {#name}
cargo-search --- 在注册表中搜索包。默认注册表为 crates.io

## 大纲 {#synopsis}
`cargo search` [_options_] [_query_...]

## 描述 {#description}
在 <https://crates.io> 上对 crate 执行文本搜索。匹配的
crate 会与其描述一起以适合复制到 `Cargo.toml` 清单中的 TOML 格式显示。

## 选项 {#options}
### 搜索选项 {#search-options}
<dl>

<dt class="option-term" id="option-cargo-search---limit"><a class="option-anchor" href="#option-cargo-search---limit"><code>--limit</code> <em>limit</em></a></dt>
<dd class="option-desc"><p>限制结果数量（默认：10，最大：100）。</p>
</dd>


<dt class="option-term" id="option-cargo-search---index"><a class="option-anchor" href="#option-cargo-search---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>


<dt class="option-term" id="option-cargo-search---registry"><a class="option-anchor" href="#option-cargo-search---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置
文件</a>中定义。若未指定，则使用默认注册表，
由 <code>registry.default</code> 配置键定义，默认为
<code>crates-io</code>。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-search--v"><a class="option-anchor" href="#option-cargo-search--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-search---verbose"><a class="option-anchor" href="#option-cargo-search---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-search--q"><a class="option-anchor" href="#option-cargo-search--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-search---quiet"><a class="option-anchor" href="#option-cargo-search---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-search---color"><a class="option-anchor" href="#option-cargo-search---color"><code>--color</code> <em>when</em></a></dt>
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

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-search-+toolchain"><a class="option-anchor" href="#option-cargo-search-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-search---config"><a class="option-anchor" href="#option-cargo-search---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-search--C"><a class="option-anchor" href="#option-cargo-search--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-search--h"><a class="option-anchor" href="#option-cargo-search--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-search---help"><a class="option-anchor" href="#option-cargo-search---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-search--Z"><a class="option-anchor" href="#option-cargo-search--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 从 crates.io 搜索包：

       cargo search serde

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-install(1)](../02-cargo-install/), [cargo-publish(1)](../../publishing-commands/05-cargo-publish/)
