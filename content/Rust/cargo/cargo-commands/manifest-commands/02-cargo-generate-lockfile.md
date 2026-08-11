+++
title = "02-cargo generate-lockfile"
date = 2026-07-30T14:49:00+08:00
weight = 62
type = "docs"
description = "cargo-generate-lockfile(1) 生成锁文件"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-generate-lockfile(1) {#cargo-generate-lockfile1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-generate-lockfile.html](https://doc.rust-lang.org/cargo/commands/cargo-generate-lockfile.html)


## 名称 {#name}
cargo-generate-lockfile --- 为包生成锁文件

## 大纲 {#synopsis}
`cargo generate-lockfile` [_options_]

## 描述 {#description}
此命令会为当前包或工作空间创建 `Cargo.lock` 锁文件。若锁文件已存在，
将用每个包的最新可用版本重建。

另见 [cargo-update(1)](../09-cargo-update/)，它也能创建 `Cargo.lock`
锁文件，并有更多控制更新行为的选项。

## 选项 {#options}
### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-generate-lockfile--v"><a class="option-anchor" href="#option-cargo-generate-lockfile--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-generate-lockfile---verbose"><a class="option-anchor" href="#option-cargo-generate-lockfile---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile--q"><a class="option-anchor" href="#option-cargo-generate-lockfile--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-generate-lockfile---quiet"><a class="option-anchor" href="#option-cargo-generate-lockfile---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---color"><a class="option-anchor" href="#option-cargo-generate-lockfile---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo-generate-lockfile---manifest-path"><a class="option-anchor" href="#option-cargo-generate-lockfile---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索
<code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---ignore-rust-version"><a class="option-anchor" href="#option-cargo-generate-lockfile---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---publish-time"><a class="option-anchor" href="#option-cargo-generate-lockfile---publish-time"><code>--publish-time</code> <em>yyyy-mm-ddThh:mm:ssZ</em></a></dt>
<dd class="option-desc"><p>注册表包允许的最晚发布时间（不稳定）</p>
<p>这是对允许包的尽力过滤，包括：</p>
<ul>
<li>来自不受支持注册表的包总是被接受</li>
<li>仅尊重当前的 yank 状态，而非 <code>--publish-time</code> 时刻的状态</li>
<li>发布时间的精度</li>
</ul>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---locked"><a class="option-anchor" href="#option-cargo-generate-lockfile---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---offline"><a class="option-anchor" href="#option-cargo-generate-lockfile---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---frozen"><a class="option-anchor" href="#option-cargo-generate-lockfile---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-generate-lockfile-+toolchain"><a class="option-anchor" href="#option-cargo-generate-lockfile-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile---config"><a class="option-anchor" href="#option-cargo-generate-lockfile---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile--C"><a class="option-anchor" href="#option-cargo-generate-lockfile--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile--h"><a class="option-anchor" href="#option-cargo-generate-lockfile--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-generate-lockfile---help"><a class="option-anchor" href="#option-cargo-generate-lockfile---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-generate-lockfile--Z"><a class="option-anchor" href="#option-cargo-generate-lockfile--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 为当前包或工作空间创建或更新锁文件：

       cargo generate-lockfile

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-update(1)](../09-cargo-update/)
