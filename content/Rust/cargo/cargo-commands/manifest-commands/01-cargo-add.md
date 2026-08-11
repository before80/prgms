+++
title = "01-cargo add"
date = 2026-07-30T14:49:00+08:00
weight = 61
type = "docs"
description = "cargo-add(1) 添加依赖"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-add(1) {#cargo-add1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-add.html](https://doc.rust-lang.org/cargo/commands/cargo-add.html)


## 名称 {#name}
cargo-add --- 向 Cargo.toml 清单文件添加依赖

## 大纲 {#synopsis}
`cargo add` [_options_] _crate_...\
`cargo add` [_options_] `--path` _path_\
`cargo add` [_options_] `--git` _url_ [_crate_...]


## 描述 {#description}
此命令可以添加或修改依赖。

可用以下方式指定依赖的源：

* _crate_`@`_version_：从注册表获取，版本约束为 “_version_”
* `--path` _path_：从指定 _path_ 获取
* `--git` _url_：从 _url_ 处的 git 仓库拉取

若未指定源，将尽最大努力选择一个，包括：

* 其他表中的现有依赖（如 `dev-dependencies`）
* 工作空间成员
* 注册表中的最新发布

当你添加已存在的包时，现有条目将用指定的标志更新。

成功调用后，指定依赖已启用（`+`）与已禁用（`-`）的[特性（features）]将列在命令输出中。

[特性（features）]: ../../../cargo-reference/features/

## 选项 {#options}
### 源选项 {#source-options}
<dl>

<dt class="option-term" id="option-cargo-add---git"><a class="option-anchor" href="#option-cargo-add---git"><code>--git</code> <em>url</em></a></dt>
<dd class="option-desc"><p><a href="../../cargo-reference/specifying-dependencies/#specifying-dependencies-from-git-repositories">要从中添加指定 crate 的 Git URL</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---branch"><a class="option-anchor" href="#option-cargo-add---branch"><code>--branch</code> <em>branch</em></a></dt>
<dd class="option-desc"><p>从 git 添加时使用的分支。</p>
</dd>


<dt class="option-term" id="option-cargo-add---tag"><a class="option-anchor" href="#option-cargo-add---tag"><code>--tag</code> <em>tag</em></a></dt>
<dd class="option-desc"><p>从 git 添加时使用的标签。</p>
</dd>


<dt class="option-term" id="option-cargo-add---rev"><a class="option-anchor" href="#option-cargo-add---rev"><code>--rev</code> <em>sha</em></a></dt>
<dd class="option-desc"><p>从 git 添加时使用的特定提交。</p>
</dd>


<dt class="option-term" id="option-cargo-add---path"><a class="option-anchor" href="#option-cargo-add---path"><code>--path</code> <em>path</em></a></dt>
<dd class="option-desc"><p>要添加的本地 crate 的<a href="../../cargo-reference/specifying-dependencies/#specifying-path-dependencies">文件系统路径</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---base"><a class="option-anchor" href="#option-cargo-add---base"><code>--base</code> <em>base</em></a></dt>
<dd class="option-desc"><p>添加本地 crate 时使用的 <a href="../../cargo-reference/17-unstable-features.md#path-bases">path base</a>。</p>
<p><a href="../../cargo-reference/17-unstable-features.md#path-bases">不稳定（仅 nightly）</a></p>
</dd>


<dt class="option-term" id="option-cargo-add---registry"><a class="option-anchor" href="#option-cargo-add---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置
文件</a>中定义。若未指定，则使用默认注册表，
由 <code>registry.default</code> 配置键定义，默认为
<code>crates-io</code>。</p>
</dd>


</dl>

### 节选项 {#section-options}
<dl>

<dt class="option-term" id="option-cargo-add---dev"><a class="option-anchor" href="#option-cargo-add---dev"><code>--dev</code></a></dt>
<dd class="option-desc"><p>添加为<a href="../../cargo-reference/specifying-dependencies/#development-dependencies">开发依赖</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---build"><a class="option-anchor" href="#option-cargo-add---build"><code>--build</code></a></dt>
<dd class="option-desc"><p>添加为<a href="../../cargo-reference/specifying-dependencies/#build-dependencies">构建依赖</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---target"><a class="option-anchor" href="#option-cargo-add---target"><code>--target</code> <em>target</em></a></dt>
<dd class="option-desc"><p>添加为<a href="../../cargo-reference/specifying-dependencies/#platform-specific-dependencies">给定目标平台</a>的依赖。</p>
<p>为避免意外的 shell 展开，可对每个 target 使用引号，例如 <code>--target 'cfg(unix)'</code>。</p>
</dd>


</dl>

### 依赖选项 {#dependency-options}
<dl>

<dt class="option-term" id="option-cargo-add---dry-run"><a class="option-anchor" href="#option-cargo-add---dry-run"><code>--dry-run</code></a></dt>
<dd class="option-desc"><p>实际上不写入清单</p>
</dd>


<dt class="option-term" id="option-cargo-add---rename"><a class="option-anchor" href="#option-cargo-add---rename"><code>--rename</code> <em>name</em></a></dt>
<dd class="option-desc"><p><a href="../../cargo-reference/specifying-dependencies/#renaming-dependencies-in-cargotoml">重命名</a>依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-add---optional"><a class="option-anchor" href="#option-cargo-add---optional"><code>--optional</code></a></dt>
<dd class="option-desc"><p>将依赖标记为<a href="../../cargo-reference/features/#optional-dependencies">可选</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---no-optional"><a class="option-anchor" href="#option-cargo-add---no-optional"><code>--no-optional</code></a></dt>
<dd class="option-desc"><p>将依赖标记为<a href="../../cargo-reference/features/#optional-dependencies">必需</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---public"><a class="option-anchor" href="#option-cargo-add---public"><code>--public</code></a></dt>
<dd class="option-desc"><p>将依赖标记为公有。</p>
<p>该依赖可在你的库的公共 API 中引用。</p>
<p><a href="../../cargo-reference/17-unstable-features.md#public-dependency">不稳定（仅 nightly）</a></p>
</dd>


<dt class="option-term" id="option-cargo-add---no-public"><a class="option-anchor" href="#option-cargo-add---no-public"><code>--no-public</code></a></dt>
<dd class="option-desc"><p>将依赖标记为私有。</p>
<p>虽然你可以在实现中使用该 crate，但不能在公共 API 中引用它。</p>
<p><a href="../../cargo-reference/17-unstable-features.md#public-dependency">不稳定（仅 nightly）</a></p>
</dd>


<dt class="option-term" id="option-cargo-add---no-default-features"><a class="option-anchor" href="#option-cargo-add---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>禁用<a href="../../cargo-reference/features/#dependency-features">默认特性</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---default-features"><a class="option-anchor" href="#option-cargo-add---default-features"><code>--default-features</code></a></dt>
<dd class="option-desc"><p>重新启用<a href="../../cargo-reference/features/#dependency-features">默认特性</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add--F"><a class="option-anchor" href="#option-cargo-add--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-add---features"><a class="option-anchor" href="#option-cargo-add---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要<a href="../../cargo-reference/features/#dependency-features">激活的特性</a>列表。添加多个
crate 时，可用
<code>package-name/feature-name</code> 语法启用特定 crate 的特性。此标志可指定多次，
以启用所有指定的特性。</p>
</dd>


</dl>


### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-add--v"><a class="option-anchor" href="#option-cargo-add--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-add---verbose"><a class="option-anchor" href="#option-cargo-add---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-add--q"><a class="option-anchor" href="#option-cargo-add--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-add---quiet"><a class="option-anchor" href="#option-cargo-add---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-add---color"><a class="option-anchor" href="#option-cargo-add---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo-add---manifest-path"><a class="option-anchor" href="#option-cargo-add---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索
<code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-add--p"><a class="option-anchor" href="#option-cargo-add--p"><code>-p</code> <em>spec</em></a></dt>
<dt class="option-term" id="option-cargo-add---package"><a class="option-anchor" href="#option-cargo-add---package"><code>--package</code> <em>spec</em></a></dt>
<dd class="option-desc"><p>仅向指定包添加依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-add---ignore-rust-version"><a class="option-anchor" href="#option-cargo-add---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-add---locked"><a class="option-anchor" href="#option-cargo-add---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-add---offline"><a class="option-anchor" href="#option-cargo-add---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-add---frozen"><a class="option-anchor" href="#option-cargo-add---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-add-+toolchain"><a class="option-anchor" href="#option-cargo-add-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如
<code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add---config"><a class="option-anchor" href="#option-cargo-add---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，
或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-add--C"><a class="option-anchor" href="#option-cargo-add--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响
Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及
用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须
出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 上可用，且
需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-add--h"><a class="option-anchor" href="#option-cargo-add--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-add---help"><a class="option-anchor" href="#option-cargo-add---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-add--Z"><a class="option-anchor" href="#option-cargo-add--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 添加依赖 `regex`

       cargo add regex

2. 添加开发依赖 `trybuild`

       cargo add --dev trybuild

3. 添加较旧版本的 `nom` 作为依赖

       cargo add nom@5

4. 添加用 `derive` 将数据结构序列化为 json 的支持

       cargo add serde serde_json -F serde/derive

5. 在 `cfg(windows)` 上添加平台特定依赖 `windows`

       cargo add windows --target 'cfg(windows)'

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-remove(1)](../07-cargo-remove/)
