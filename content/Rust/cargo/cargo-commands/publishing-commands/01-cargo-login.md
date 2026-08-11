+++
title = "01-cargo login"
date = 2026-07-30T14:49:00+08:00
weight = 78
type = "docs"
description = "cargo-login(1) 保存 API token"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-login(1) {#cargo-login1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-login.html](https://doc.rust-lang.org/cargo/commands/cargo-login.html)


## 名称 {#name}
cargo-login --- 登录到注册表

## 大纲 {#synopsis}
`cargo login` [_options_] [`--` _args_]

## 描述 {#description}
此命令会运行凭证提供者保存令牌，以便需要身份验证的命令
（如 [cargo-publish(1)](../05-cargo-publish/)）能够
自动完成身份验证。

双破折号（`--`）之后的所有参数都会传给凭证提供者。

对于默认的 `cargo:token` 凭证提供者，令牌保存在
`$CARGO_HOME/credentials.toml` 中。`CARGO_HOME` 默认为你主目录下的 `.cargo`。

若注册表指定了 credential-provider，则使用它。否则，
将从配置值 `registry.global-credential-providers` 中的提供者列表末尾开始尝试。

_token_ 将从标准输入读取。

crates.io 的 API 令牌可从 <https://crates.io/me> 获取。

请妥善保管令牌，不要与他人共享。

## 选项 {#options}
### 登录选项 {#login-options}
<dl>
<dt class="option-term" id="option-cargo-login---registry"><a class="option-anchor" href="#option-cargo-login---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置
文件</a>中定义。若未指定，则使用默认注册表，
由 <code>registry.default</code> 配置键定义，默认为
<code>crates-io</code>。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-login--v"><a class="option-anchor" href="#option-cargo-login--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-login---verbose"><a class="option-anchor" href="#option-cargo-login---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-login--q"><a class="option-anchor" href="#option-cargo-login--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-login---quiet"><a class="option-anchor" href="#option-cargo-login---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-login---color"><a class="option-anchor" href="#option-cargo-login---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-login-+toolchain"><a class="option-anchor" href="#option-cargo-login-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-login---config"><a class="option-anchor" href="#option-cargo-login---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-login--C"><a class="option-anchor" href="#option-cargo-login--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-login--h"><a class="option-anchor" href="#option-cargo-login--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-login---help"><a class="option-anchor" href="#option-cargo-login---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-login--Z"><a class="option-anchor" href="#option-cargo-login--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 保存默认注册表的令牌：

       cargo login

2. 保存特定注册表的令牌：

       cargo login --registry my-registry

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-logout(1)](../02-cargo-logout/), [cargo-publish(1)](../05-cargo-publish/)
