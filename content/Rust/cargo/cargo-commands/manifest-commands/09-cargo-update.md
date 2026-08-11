+++
title = "09-cargo update"
date = 2026-07-30T14:49:00+08:00
weight = 69
type = "docs"
description = "cargo-update(1) 更新依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-update(1) {#cargo-update1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-update.html](https://doc.rust-lang.org/cargo/commands/cargo-update.html)


## 名称 {#name}
cargo-update --- 按本地锁文件记录更新依赖

## 大纲 {#synopsis}
`cargo update` [_options_] _spec_

## 描述 {#description}
此命令会将 `Cargo.lock` 文件中的依赖更新到最新版本。若 `Cargo.lock` 文件不存在，
将用最新可用版本创建。

## 选项 {#options}
### 更新选项 {#update-options}
<dl>

<dt class="option-term" id="option-cargo-update-spec…"><a class="option-anchor" href="#option-cargo-update-spec…"><em>spec</em>…</a></dt>
<dd class="option-desc"><p>仅更新指定的包。此标志可指定多次。SPEC 格式见 <a href="06-cargo-pkgid.md">cargo-pkgid(1)</a>。</p>
<p>若用 <em>spec</em> 指定了包，则会对锁文件执行保守更新。这意味着仅更新 SPEC 指定的依赖。
其传递依赖仅在不更新它们就无法更新 SPEC 时才会更新。所有其他依赖将保持锁定在当前记录的版本。</p>
<p>若未指定 <em>spec</em>，则更新所有依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-update---recursive"><a class="option-anchor" href="#option-cargo-update---recursive"><code>--recursive</code></a></dt>
<dd class="option-desc"><p>与 <em>spec</em> 一起使用时，也会强制更新 <em>spec</em> 的依赖。
不能与 <code>--precise</code> 一起使用。</p>
</dd>


<dt class="option-term" id="option-cargo-update---precise"><a class="option-anchor" href="#option-cargo-update---precise"><code>--precise</code> <em>precise</em></a></dt>
<dd class="option-desc"><p>与 <em>spec</em> 一起使用时，允许你指定将该包设为的具体版本号。若包来自 git 仓库，可以是 git
修订（例如 SHA 哈希或标签）。</p>
<p>虽然不推荐，但你可以指定已 yank 的包版本。
尽可能尝试其他未 yank 的 SemVer 兼容版本，或向包维护者寻求帮助。</p>
<p>即使 <code>Cargo.toml</code> 中的版本需求不包含任何预发布标识符，也可以指定兼容的 <code>pre-release</code> 版本（仅 nightly）。</p>
</dd>


<dt class="option-term" id="option-cargo-update---breaking"><a class="option-anchor" href="#option-cargo-update---breaking"><code>--breaking</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>将 <em>spec</em> 更新到最新的 SemVer 破坏性版本。</p>
<p>版本需求将被修改以允许此更新。</p>
<p>这仅在以下情况应用于依赖：</p>
<ul>
<li>该包是工作空间成员的依赖</li>
<li>该依赖未被重命名</li>
<li>存在 SemVer 不兼容版本</li>
<li>使用了“SemVer 运算符”（默认的 <code>^</code>）</li>
</ul>
<p>此选项不稳定，仅在
<a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a>
上可用，且需要 <code>-Z unstable-options</code> 标志才能启用。
更多信息见 <a href="https://github.com/rust-lang/cargo/issues/12425">https://github.com/rust-lang/cargo/issues/12425</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-update--w"><a class="option-anchor" href="#option-cargo-update--w"><code>-w</code></a></dt>
<dt class="option-term" id="option-cargo-update---workspace"><a class="option-anchor" href="#option-cargo-update---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>尝试仅更新工作空间中定义的包。其他包仅在锁文件中尚不存在时才会更新。
在你更改 <code>Cargo.toml</code> 中的版本号后更新 <code>Cargo.lock</code> 时，此选项很有用。</p>
</dd>


<dt class="option-term" id="option-cargo-update---dry-run"><a class="option-anchor" href="#option-cargo-update---dry-run"><code>--dry-run</code></a></dt>
<dd class="option-desc"><p>显示将要更新的内容，但实际上不写入锁文件。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-update--v"><a class="option-anchor" href="#option-cargo-update--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-update---verbose"><a class="option-anchor" href="#option-cargo-update---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-update--q"><a class="option-anchor" href="#option-cargo-update--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-update---quiet"><a class="option-anchor" href="#option-cargo-update---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-update---color"><a class="option-anchor" href="#option-cargo-update---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-update---manifest-path"><a class="option-anchor" href="#option-cargo-update---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索
<code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-update---ignore-rust-version"><a class="option-anchor" href="#option-cargo-update---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-update---locked"><a class="option-anchor" href="#option-cargo-update---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-update---offline"><a class="option-anchor" href="#option-cargo-update---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-update---frozen"><a class="option-anchor" href="#option-cargo-update---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-update-+toolchain"><a class="option-anchor" href="#option-cargo-update-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-update---config"><a class="option-anchor" href="#option-cargo-update---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-update--C"><a class="option-anchor" href="#option-cargo-update--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-update--h"><a class="option-anchor" href="#option-cargo-update--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-update---help"><a class="option-anchor" href="#option-cargo-update---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-update--Z"><a class="option-anchor" href="#option-cargo-update--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 更新锁文件中的所有依赖：

       cargo update

2. 仅更新特定依赖：

       cargo update foo bar

3. 将特定依赖设为特定版本：

       cargo update foo --precise 1.2.3

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-generate-lockfile(1)](../02-cargo-generate-lockfile/)
