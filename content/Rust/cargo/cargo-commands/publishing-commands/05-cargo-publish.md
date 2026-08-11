+++
title = "05-cargo publish"
date = 2026-07-30T14:49:00+08:00
weight = 82
type = "docs"
description = "cargo-publish(1) 上传包到注册表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-publish(1) {#cargo-publish1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-publish.html](https://doc.rust-lang.org/cargo/commands/cargo-publish.html)


## 名称 {#name}
cargo-publish --- 将包上传到注册表

## 大纲 {#synopsis}
`cargo publish` [_options_]

## 描述 {#description}
此命令会为当前目录中的包创建可分发、压缩的 `.crate` 文件（含源代码），并将其上传到注册表。默认注册表为 <https://crates.io>。执行步骤如下：

1. 执行若干检查，包括：
   - 检查清单中的 `package.publish` 键，确认允许发布到哪些注册表。
2. 按 [cargo-package(1)](../04-cargo-package/) 中的步骤创建 `.crate` 文件。
3. 将 crate 上传到注册表。服务器会对 crate 执行额外检查。
4. 客户端会轮询等待包出现在索引中，可能会超时。若超时，你需要手动检查是否完成。此超时不会影响上传本身。

此命令要求你通过 [cargo-login(1)](../01-cargo-login/) 或 [`registry.token`](../../../cargo-reference/06-configuration/#registrytoken) 与 [`registries.<name>.token`](../../../cargo-reference/06-configuration/#registriesnametoken) 配置字段对应的环境变量完成身份验证。

关于打包与发布的更多细节，见[参考文档](../../../cargo-guide/09-publishing-on-crates-io/)。

## 选项 {#options}
### 发布选项 {#publish-options}
<dl>

<dt class="option-term" id="option-cargo-publish---dry-run"><a class="option-anchor" href="#option-cargo-publish---dry-run"><code>--dry-run</code></a></dt>
<dd class="option-desc"><p>执行所有检查但不实际上传。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---no-verify"><a class="option-anchor" href="#option-cargo-publish---no-verify"><code>--no-verify</code></a></dt>
<dd class="option-desc"><p>不通过构建来验证内容。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---allow-dirty"><a class="option-anchor" href="#option-cargo-publish---allow-dirty"><code>--allow-dirty</code></a></dt>
<dd class="option-desc"><p>允许打包含有未提交 VCS 变更的工作目录。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---index"><a class="option-anchor" href="#option-cargo-publish---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---registry"><a class="option-anchor" href="#option-cargo-publish---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要发布到的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置文件</a>中定义。若未指定，且 <code>Cargo.toml</code> 中的 <a href="../../cargo-reference/the-manifest-format/_index.md#the-publish-field"><code>package.publish</code></a> 字段仅包含单个注册表，则发布到该注册表。否则使用默认注册表，由 <a href="../../cargo-reference/06-configuration.md#registrydefault"><code>registry.default</code></a> 配置键定义，默认为 <code>crates-io</code>。</p>
</dd>


</dl>

### 包选择 {#package-selection}
默认情况下，若未指定包选择选项，所选包取决于所选清单文件（若未指定 `--manifest-path`，则基于当前工作目录）。若清单是工作空间的根，则选择工作空间的默认成员；否则仅选择清单定义的包。

工作空间的默认成员可在根清单中通过 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间则仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-publish--p"><a class="option-anchor" href="#option-cargo-publish--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-publish---package"><a class="option-anchor" href="#option-cargo-publish---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>仅发布指定的包。SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---workspace"><a class="option-anchor" href="#option-cargo-publish---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>发布工作空间中的所有成员。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---all"><a class="option-anchor" href="#option-cargo-publish---all"><code>--all</code></a></dt>
<dd class="option-desc"><p>已弃用，为 <code>--workspace</code> 的别名。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---exclude"><a class="option-anchor" href="#option-cargo-publish---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-publish---target"><a class="option-anchor" href="#option-cargo-publish---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>为指定目标架构发布。此标志可指定多次。默认为宿主架构。三元组的一般格式为 <code>&lt;arch&gt;&lt;sub&gt;-&lt;vendor&gt;-&lt;sys&gt;-&lt;abi&gt;</code>。</p>
<p>可能的值：</p>
<ul>
<li><code>rustc --print target-list</code> 中支持的任意目标。</li>
<li><code>"host-tuple"</code>，内部将替换为宿主目标。若你在交叉编译某些 crate，且不想将宿主机器指定为目标（例如多人协作的共享项目中的 <code>xtask</code>），这会特别有用。</li>
<li>自定义目标规范的路径。更多信息见 <a href="https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path">Custom Target Lookup Path</a>。</li>
</ul>
<p>也可通过 <code>build.target</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
<p>请注意，指定此标志会使 Cargo 以不同模式运行，目标产物将放在单独的目录中。更多细节见 <a href="../../cargo-reference/09-build-cache.md">构建缓存</a>文档。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---target-dir"><a class="option-anchor" href="#option-cargo-publish---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或 <code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为工作空间根目录下的 <code>target</code>。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性。若未指定特性选项，每个所选包都会激活 <code>default</code> 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-publish--F"><a class="option-anchor" href="#option-cargo-publish--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-publish---features"><a class="option-anchor" href="#option-cargo-publish---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要激活的特性列表。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，以启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---all-features"><a class="option-anchor" href="#option-cargo-publish---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---no-default-features"><a class="option-anchor" href="#option-cargo-publish---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 清单选项 {#manifest-options}
<dl>

<dt class="option-term" id="option-cargo-publish---manifest-path"><a class="option-anchor" href="#option-cargo-publish---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索 <code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---locked"><a class="option-anchor" href="#option-cargo-publish---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---offline"><a class="option-anchor" href="#option-cargo-publish---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---frozen"><a class="option-anchor" href="#option-cargo-publish---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 其他选项 {#miscellaneous-options}
<dl>
<dt class="option-term" id="option-cargo-publish--j"><a class="option-anchor" href="#option-cargo-publish--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-publish---jobs"><a class="option-anchor" href="#option-cargo-publish---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为逻辑 CPU 数量。若为负数，则最大并行作业数为逻辑 CPU 数加上该值。若提供字符串 <code>default</code>，则恢复为默认值。不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-publish---keep-going"><a class="option-anchor" href="#option-cargo-publish---keep-going"><code>--keep-going</code></a></dt>
<dd class="option-desc"><p>尽可能构建依赖图中的更多 crate，而不是在第一个构建失败的 crate 处中止。</p>
<p>例如，若当前包依赖 <code>fails</code> 与 <code>works</code>，其中一个构建失败，<code>cargo publish -j1</code> 可能会也可能不会构建成功的那一个（取决于 Cargo 先运行哪一个），而 <code>cargo publish -j1 --keep-going</code> 则一定会运行两次构建，即便先运行的那个失败。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-publish--v"><a class="option-anchor" href="#option-cargo-publish--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-publish---verbose"><a class="option-anchor" href="#option-cargo-publish---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。也可通过 <code>term.verbose</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-publish--q"><a class="option-anchor" href="#option-cargo-publish--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-publish---quiet"><a class="option-anchor" href="#option-cargo-publish---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。也可通过 <code>term.quiet</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---color"><a class="option-anchor" href="#option-cargo-publish---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code>（默认）：自动检测终端是否支持颜色。</li>
<li><code>always</code>：始终显示颜色。</li>
<li><code>never</code>：从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-publish-+toolchain"><a class="option-anchor" href="#option-cargo-publish-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-publish---config"><a class="option-anchor" href="#option-cargo-publish---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-publish--C"><a class="option-anchor" href="#option-cargo-publish--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a> 上可用，且需要 <code>-Z unstable-options</code> 标志才能启用（见 <a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-publish--h"><a class="option-anchor" href="#option-cargo-publish--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-publish---help"><a class="option-anchor" href="#option-cargo-publish---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-publish--Z"><a class="option-anchor" href="#option-cargo-publish--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 发布当前包：

       cargo publish

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-package(1)](../04-cargo-package/), [cargo-login(1)](../01-cargo-login/)
