+++
title = "03-cargo info"
date = 2026-07-30T14:49:00+08:00
weight = 63
type = "docs"
description = "cargo-info(1) 显示包信息"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-info(1) {#cargo-info1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-info.html](https://doc.rust-lang.org/cargo/commands/cargo-info.html)


## 名称 {#name}
cargo-info --- 显示关于某个包的信息。

## 大纲 {#synopsis}
`cargo info` [_options_] _spec_

## 描述 {#description}
此命令显示关于某个包的信息。它从包的 Cargo.toml 文件获取数据，
并以人类可读的格式呈现。

## 选项 {#options}
### 信息选项 {#info-options}
<dl>

<dt class="option-term" id="option-cargo-info-spec"><a class="option-anchor" href="#option-cargo-info-spec"><em>spec</em></a></dt>
<dd class="option-desc"><p>获取指定包的信息。<em>spec</em> 可以是包 ID，SPEC 格式见 <a href="06-cargo-pkgid.md">cargo-pkgid(1)</a>。
若指定包是当前工作空间的一部分，将显示本地 Cargo.toml 文件中的信息。
若 <code>Cargo.lock</code> 文件不存在，则会创建。若未指定版本，将根据最低支持的 Rust 版本（MSRV）选择合适版本。</p>
</dd>

<dt class="option-term" id="option-cargo-info---index"><a class="option-anchor" href="#option-cargo-info---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>

<dt class="option-term" id="option-cargo-info---registry"><a class="option-anchor" href="#option-cargo-info---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置
文件</a>中定义。若未指定，则使用默认注册表，
由 <code>registry.default</code> 配置键定义，默认为
<code>crates-io</code>。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-info--v"><a class="option-anchor" href="#option-cargo-info--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-info---verbose"><a class="option-anchor" href="#option-cargo-info---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-info--q"><a class="option-anchor" href="#option-cargo-info--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-info---quiet"><a class="option-anchor" href="#option-cargo-info---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-info---color"><a class="option-anchor" href="#option-cargo-info---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo-info---locked"><a class="option-anchor" href="#option-cargo-info---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-info---offline"><a class="option-anchor" href="#option-cargo-info---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-info---frozen"><a class="option-anchor" href="#option-cargo-info---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-info-+toolchain"><a class="option-anchor" href="#option-cargo-info-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-info---config"><a class="option-anchor" href="#option-cargo-info---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-info--C"><a class="option-anchor" href="#option-cargo-info--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-info--h"><a class="option-anchor" href="#option-cargo-info--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-info---help"><a class="option-anchor" href="#option-cargo-info---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-info--Z"><a class="option-anchor" href="#option-cargo-info--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 查看 crates.io 上的 `serde` 包：

        cargo info serde
2. 查看版本为 `1.0.0` 的 `serde` 包：

        cargo info serde@1.0.0
3. 从本地注册表查看 `serde` 包：

        cargo info serde --registry my-registry

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-search(1)](../../package-commands/04-cargo-search/)
