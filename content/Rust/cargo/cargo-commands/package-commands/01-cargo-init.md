+++
title = "01-cargo init"
date = 2026-07-30T14:49:00+08:00
weight = 72
type = "docs"
description = "cargo-init(1) 在已有目录初始化包"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-init(1) {#cargo-init1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-init.html](https://doc.rust-lang.org/cargo/commands/cargo-init.html)


## 名称 {#name}
cargo-init --- 在已有目录中创建新的 Cargo 包

## 大纲 {#synopsis}
`cargo init` [_options_] [_path_]

## 描述 {#description}
此命令会在当前目录创建新的 Cargo 清单。给定路径参数可在指定目录中创建。

若目录中已有典型命名的 Rust 源文件，将使用它们。否则会创建示例
`src/main.rs` 文件；若传入 `--lib`，则创建 `src/lib.rs`。

若该目录尚不在 VCS 仓库中，则会创建新仓库（见下方 `--vcs`）。

类似命令见 [cargo-new(1)](../03-cargo-new/)，它会在新目录中创建新包。

## 选项 {#options}
### 初始化选项 {#init-options}
<dl>

<dt class="option-term" id="option-cargo-init---bin"><a class="option-anchor" href="#option-cargo-init---bin"><code>--bin</code></a></dt>
<dd class="option-desc"><p>创建带有二进制目标（<code>src/main.rs</code>）的包。
这是默认行为。</p>
</dd>


<dt class="option-term" id="option-cargo-init---lib"><a class="option-anchor" href="#option-cargo-init---lib"><code>--lib</code></a></dt>
<dd class="option-desc"><p>创建带有库目标（<code>src/lib.rs</code>）的包。</p>
</dd>


<dt class="option-term" id="option-cargo-init---edition"><a class="option-anchor" href="#option-cargo-init---edition"><code>--edition</code> <em>edition</em></a></dt>
<dd class="option-desc"><p>指定要使用的 Rust edition。默认为 2024。
可选值：2015、2018、2021、2024</p>
</dd>


<dt class="option-term" id="option-cargo-init---name"><a class="option-anchor" href="#option-cargo-init---name"><code>--name</code> <em>name</em></a></dt>
<dd class="option-desc"><p>设置包名。默认为目录名。</p>
</dd>


<dt class="option-term" id="option-cargo-init---vcs"><a class="option-anchor" href="#option-cargo-init---vcs"><code>--vcs</code> <em>vcs</em></a></dt>
<dd class="option-desc"><p>为给定版本控制系统（git、hg、pijul 或 fossil）初始化新的 VCS 仓库，
或完全不初始化任何版本控制（none）。若未指定，默认为 <code>git</code> 或配置值
<code>cargo-new.vcs</code>；若已在 VCS 仓库内，则为 <code>none</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-init---registry"><a class="option-anchor" href="#option-cargo-init---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>这将把 <code>Cargo.toml</code> 中的 <code>publish</code> 字段设为给定注册表名称，
从而限制仅能发布到该注册表。</p>
<p>注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置文件</a>中定义。
若未指定，则使用 <code>registry.default</code> 配置键定义的默认注册表。
若未设置默认注册表且未使用 <code>--registry</code>，则不会设置 <code>publish</code> 字段，
意味着发布不受限制。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-init--v"><a class="option-anchor" href="#option-cargo-init--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-init---verbose"><a class="option-anchor" href="#option-cargo-init---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-init--q"><a class="option-anchor" href="#option-cargo-init--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-init---quiet"><a class="option-anchor" href="#option-cargo-init---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-init---color"><a class="option-anchor" href="#option-cargo-init---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-init-+toolchain"><a class="option-anchor" href="#option-cargo-init-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-init---config"><a class="option-anchor" href="#option-cargo-init---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-init--C"><a class="option-anchor" href="#option-cargo-init--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-init--h"><a class="option-anchor" href="#option-cargo-init--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-init---help"><a class="option-anchor" href="#option-cargo-init---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-init--Z"><a class="option-anchor" href="#option-cargo-init--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 在当前目录创建二进制 Cargo 包：

       cargo init

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-new(1)](../03-cargo-new/)
