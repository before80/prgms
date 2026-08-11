+++
title = "06-cargo yank"
date = 2026-07-30T14:49:00+08:00
weight = 83
type = "docs"
description = "cargo-yank(1) 撤回某个版本"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-yank(1) {#cargo-yank1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-yank.html](https://doc.rust-lang.org/cargo/commands/cargo-yank.html)


## 名称 {#name}
cargo-yank --- 从索引中移除已推送的 crate

## 大纲 {#synopsis}
`cargo yank` [_options_] _crate_@_version_\
`cargo yank` [_options_] `--version` _version_ [_crate_]

## 描述 {#description}
yank 命令从服务器索引中移除先前发布的 crate 版本。此命令不删除任何数据，
该 crate 仍可通过注册表的下载链接下载。

对于没有预先存在锁文件的任何新项目或检出，Cargo 不会使用已 yank 的版本，
若你的 crate 不再有任何兼容版本，将生成错误。

此命令要求你通过 `--token` 选项或使用 [cargo-login(1)](../01-cargo-login/) 完成身份验证。

若未指定 crate 名称，将使用当前目录中的包名。

### yank 如何工作 {#how-yank-works}
例如，`foo` crate 发布了版本 `1.5.0`，另一个 crate `bar`
声明了对版本 `foo = "1.5"` 的依赖。现在 `foo` 发布了新的但不兼容 SemVer 的版本 `2.0.0`，
并发现 `1.5.0` 有严重问题。若 yank 了 `1.5.0`，任何没有现有锁文件的新项目或检出
都将无法使用依赖 `1.5` 的 crate `bar`。

在这种情况下，`foo` 的维护者应在 yank `1.5.0` 之前先发布 SemVer 兼容版本（如 `1.5.1`），
以便 `bar` 以及所有依赖 `bar` 的项目继续工作。

再举一例，考虑已发布版本 `1.5.0`、`1.5.1`、`1.5.2`、`2.0.0` 与 `3.0.0` 的 crate `bar`。
下表标明在没有锁文件时，给定版本被 yank 后，Cargo 对不同 SemVer 需求可能使用的版本：

| 已 Yank 版本 / SemVer 需求 | `bar = "1.5.0"` | `bar = "=1.5.0"` | `bar = "2.0.0"` |
|-------------------------------------|-----------------------------------------|------------------|------------------|
| `1.5.0` | 使用 `1.5.1` 或 `1.5.2` | **返回错误** | 使用 `2.0.0` |
| `1.5.1` | 使用 `1.5.0` 或 `1.5.2` | 使用 `1.5.0` | 使用 `2.0.0` |
| `2.0.0` | 使用 `1.5.0`、`1.5.1` 或 `1.5.2` | 使用 `1.5.0` | **返回错误** |

### 何时 yank {#when-to-yank}
仅应在例外情况下 yank crate，例如意外发布、无意的 SemVer 破坏，或严重损坏且无法使用的 crate。
对于安全漏洞，[RustSec] 通常是告知用户并鼓励升级的干扰更小的机制，
并可避免不论是否易受该漏洞影响都造成显著的下游中断。

常见工作流是在已发布 SemVer 兼容版本后再 yank 某个 crate，
以降低阻止依赖 crate 编译的可能性。

在处理已发布 crate 的版权、许可或个人数据问题时，仅 yank 可能不够。
在这种情况下，请联系你所用注册表的维护者。对于 crates.io，请参阅其[政策]并联系
<help@crates.io>。

若凭证已泄露，建议立即吊销。一旦 crate 已发布，就无法确定泄露的凭证是否已被复制。
yank 仅防止 Cargo 在默认解析依赖时选择此版本。现有锁文件或直接下载不受影响，
因此 yank 无法阻止泄露凭证的进一步传播。

[RustSec]: https://rustsec.org/
[政策]: https://crates.io/policies

## 选项 {#options}
### Yank 选项 {#yank-options}
<dl>

<dt class="option-term" id="option-cargo-yank---vers"><a class="option-anchor" href="#option-cargo-yank---vers"><code>--vers</code> <em>version</em></a></dt>
<dt class="option-term" id="option-cargo-yank---version"><a class="option-anchor" href="#option-cargo-yank---version"><code>--version</code> <em>version</em></a></dt>
<dd class="option-desc"><p>要 yank 或取消 yank 的版本。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---undo"><a class="option-anchor" href="#option-cargo-yank---undo"><code>--undo</code></a></dt>
<dd class="option-desc"><p>撤销 yank，将版本放回索引。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---token"><a class="option-anchor" href="#option-cargo-yank---token"><code>--token</code> <em>token</em></a></dt>
<dd class="option-desc"><p>身份验证时使用的 API 令牌。这会覆盖凭证文件中存储的令牌
（由 <a href="01-cargo-login.md">cargo-login(1)</a> 创建）。</p>
<p><a href="../../cargo-reference/06-configuration.md">Cargo 配置</a>环境变量可用于覆盖凭证文件中存储的令牌。
crates.io 的令牌可用 <code>CARGO_REGISTRY_TOKEN</code> 环境变量指定。
其他注册表的令牌可用形如 <code>CARGO_REGISTRIES_NAME_TOKEN</code> 的环境变量指定，
其中 <code>NAME</code> 为注册表名称的全大写形式。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---index"><a class="option-anchor" href="#option-cargo-yank---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---registry"><a class="option-anchor" href="#option-cargo-yank---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置
文件</a>中定义。若未指定，则使用默认注册表，
由 <code>registry.default</code> 配置键定义，默认为
<code>crates-io</code>。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-yank--v"><a class="option-anchor" href="#option-cargo-yank--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-yank---verbose"><a class="option-anchor" href="#option-cargo-yank---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-yank--q"><a class="option-anchor" href="#option-cargo-yank--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-yank---quiet"><a class="option-anchor" href="#option-cargo-yank---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---color"><a class="option-anchor" href="#option-cargo-yank---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-yank-+toolchain"><a class="option-anchor" href="#option-cargo-yank-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-yank---config"><a class="option-anchor" href="#option-cargo-yank---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-yank--C"><a class="option-anchor" href="#option-cargo-yank--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-yank--h"><a class="option-anchor" href="#option-cargo-yank--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-yank---help"><a class="option-anchor" href="#option-cargo-yank---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-yank--Z"><a class="option-anchor" href="#option-cargo-yank--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 从索引中 yank 一个 crate：

       cargo yank foo@1.0.7

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-login(1)](../01-cargo-login/), [cargo-publish(1)](../05-cargo-publish/)
