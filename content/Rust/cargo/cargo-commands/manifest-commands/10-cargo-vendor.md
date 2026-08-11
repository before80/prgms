+++
title = "10-cargo vendor"
date = 2026-07-30T14:49:00+08:00
weight = 70
type = "docs"
description = "cargo-vendor(1) 供应商化依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-vendor(1) {#cargo-vendor1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-vendor.html](https://doc.rust-lang.org/cargo/commands/cargo-vendor.html)


## 名称 {#name}
cargo-vendor --- 将所有依赖供应商化到本地

## 大纲 {#synopsis}
`cargo vendor` [_options_] [_path_]

## 描述 {#description}
此 cargo 子命令会将项目的所有 crates.io 与 git 依赖供应商化到 `<path>` 指定的目录。
命令完成后，`<path>` 指定的 vendor 目录将包含依赖中指定的所有远程源。
可用 `-s` 选项指定默认清单之外的其他清单。

`cargo vendor` 完成供应商化过程后，使用供应商化源所需的配置会打印到标准输出。
你需要将其添加或重定向到 Cargo 配置文件，
对于当前包通常是本地的 `.cargo/config.toml`。

Cargo 将供应商化源视为只读，就像对待注册表与 git 源一样。
若你打算修改来自远程源的 crate，
请使用 `[patch]` 或指向该 crate 本地副本的 `path` 依赖。
Cargo 随后会在增量重建时正确处理该 crate，
因为它知道它不再是只读依赖。

## 选项 {#options}
### 供应商化选项 {#vendor-options}
<dl>

<dt class="option-term" id="option-cargo-vendor--s"><a class="option-anchor" href="#option-cargo-vendor--s"><code>-s</code> <em>manifest</em></a></dt>
<dt class="option-term" id="option-cargo-vendor---sync"><a class="option-anchor" href="#option-cargo-vendor---sync"><code>--sync</code> <em>manifest</em></a></dt>
<dd class="option-desc"><p>指定额外的 <code>Cargo.toml</code> 清单，其工作空间也应被供应商化并同步到输出。可指定多次。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---no-delete"><a class="option-anchor" href="#option-cargo-vendor---no-delete"><code>--no-delete</code></a></dt>
<dd class="option-desc"><p>供应商化时不删除 “vendor” 目录，而是保留 vendor 目录的所有现有内容</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---respect-source-config"><a class="option-anchor" href="#option-cargo-vendor---respect-source-config"><code>--respect-source-config</code></a></dt>
<dd class="option-desc"><p>默认情况下忽略 <code>.cargo/config.toml</code> 中的 <code>[source]</code> 配置；指定此选项后改为读取并使用它，例如从 crates.io 下载 crate 时</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---versioned-dirs"><a class="option-anchor" href="#option-cargo-vendor---versioned-dirs"><code>--versioned-dirs</code></a></dt>
<dd class="option-desc"><p>通常仅在需要区分同一包的多个版本时才添加版本号。此选项使 “vendor” 目录中的所有目录都带版本，
便于随时间跟踪供应商化包的历史，并在仅有一部分包发生变化时有助于重新供应商化的性能。</p>
</dd>


</dl>

### 清单选项 {#manifest-options}
<dl>

<dt class="option-term" id="option-cargo-vendor---manifest-path"><a class="option-anchor" href="#option-cargo-vendor---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索
<code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---locked"><a class="option-anchor" href="#option-cargo-vendor---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---offline"><a class="option-anchor" href="#option-cargo-vendor---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---frozen"><a class="option-anchor" href="#option-cargo-vendor---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-vendor--v"><a class="option-anchor" href="#option-cargo-vendor--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-vendor---verbose"><a class="option-anchor" href="#option-cargo-vendor---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor--q"><a class="option-anchor" href="#option-cargo-vendor--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-vendor---quiet"><a class="option-anchor" href="#option-cargo-vendor---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---color"><a class="option-anchor" href="#option-cargo-vendor---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-vendor-+toolchain"><a class="option-anchor" href="#option-cargo-vendor-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor---config"><a class="option-anchor" href="#option-cargo-vendor---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor--C"><a class="option-anchor" href="#option-cargo-vendor--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor--h"><a class="option-anchor" href="#option-cargo-vendor--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-vendor---help"><a class="option-anchor" href="#option-cargo-vendor---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-vendor--Z"><a class="option-anchor" href="#option-cargo-vendor--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 将所有依赖供应商化到本地 “vendor” 文件夹

       cargo vendor

2. 将所有依赖供应商化到本地 “third-party/vendor” 文件夹

       cargo vendor third-party/vendor

3. 将当前工作空间以及另一个工作空间供应商化到 “vendor”

       cargo vendor -s ../path/to/Cargo.toml

4. 供应商化并将必要的 vendor 配置重定向到配置文件。

       cargo vendor > path/to/my/cargo/config.toml

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)
