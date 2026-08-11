+++
title = "07-cargo fetch"
date = 2026-07-30T14:49:00+08:00
weight = 52
type = "docs"
description = "cargo-fetch(1) 下载依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-fetch(1) {#cargo-fetch1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-fetch.html](https://doc.rust-lang.org/cargo/commands/cargo-fetch.html)


## 名称 {#name}
cargo-fetch --- 从网络获取包的依赖

## 大纲 {#synopsis}
`cargo fetch` [_options_]

## 描述 {#description}
若存在 `Cargo.lock` 文件，此命令将确保所有 git 依赖和/或注册表依赖均已下载并可在本地使用。在 `cargo fetch` 之后，除非锁文件发生变化，后续 Cargo 命令可离线运行。

若锁文件不可用，则此命令会在获取依赖之前先生成锁文件。

若未指定 `--target`，则获取所有目标架构的依赖。

## 选项 {#options}
### Fetch 选项 {#fetch-options}
<dl>
<dt class="option-term" id="option-cargo-fetch---target"><a class="option-anchor" href="#option-cargo-fetch---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>为指定的目标架构获取依赖。此标志可指定多次。默认为所有架构。triple 的一般格式为
<code>&lt;arch&gt;&lt;sub&gt;-&lt;vendor&gt;-&lt;sys&gt;-&lt;abi&gt;</code>。</p>
<p>可能的值：</p>
<ul>
<li><code>rustc --print target-list</code> 中任何受支持的目标。</li>
<li><code>"host-tuple"</code>，内部会替换为主机目标。若你在交叉编译某些 crate，又不想把主机机器指定为目标（例如可能由多台主机协作的共享项目中的 <code>xtask</code>），这会特别有用。</li>
<li>自定义目标规范的路径。更多信息见 <a href="https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path">自定义目标查找路径</a>。</li>
</ul>
<p>也可通过 <code>build.target</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
<p>注意：指定此标志会使 Cargo 以不同模式运行，目标产物会放在单独目录中。详情见
<a href="../../cargo-reference/09-build-cache.md">构建缓存</a>文档。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-fetch--v"><a class="option-anchor" href="#option-cargo-fetch--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-fetch---verbose"><a class="option-anchor" href="#option-cargo-fetch---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch--q"><a class="option-anchor" href="#option-cargo-fetch--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-fetch---quiet"><a class="option-anchor" href="#option-cargo-fetch---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch---color"><a class="option-anchor" href="#option-cargo-fetch---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo-fetch---manifest-path"><a class="option-anchor" href="#option-cargo-fetch---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 会在当前目录或其任意父目录中搜索 <code>Cargo.toml</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch---locked"><a class="option-anchor" href="#option-cargo-fetch---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch---offline"><a class="option-anchor" href="#option-cargo-fetch---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch---frozen"><a class="option-anchor" href="#option-cargo-fetch---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-fetch-+toolchain"><a class="option-anchor" href="#option-cargo-fetch-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch---config"><a class="option-anchor" href="#option-cargo-fetch---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch--C"><a class="option-anchor" href="#option-cargo-fetch--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch--h"><a class="option-anchor" href="#option-cargo-fetch--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-fetch---help"><a class="option-anchor" href="#option-cargo-fetch---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-fetch--Z"><a class="option-anchor" href="#option-cargo-fetch--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/)了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`：Cargo 成功完成。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 获取所有依赖：

       cargo fetch

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/)、[cargo-update(1)](../../manifest-commands/09-cargo-update/)、[cargo-generate-lockfile(1)](../../manifest-commands/02-cargo-generate-lockfile/)
