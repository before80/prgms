+++
title = "02-cargo install"
date = 2026-07-30T14:49:00+08:00
weight = 73
type = "docs"
description = "cargo-install(1) 安装二进制 crate"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-install(1) {#cargo-install1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-install.html](https://doc.rust-lang.org/cargo/commands/cargo-install.html)


## 名称 {#name}
cargo-install --- 构建并安装 Rust 二进制程序

## 大纲 {#synopsis}
`cargo install` [_options_] _crate_[@_version_]...\
`cargo install` [_options_] `--path` _path_\
`cargo install` [_options_] `--git` _url_ [_crate_...]\
`cargo install` [_options_] `--list`

## 描述 {#description}
此命令管理 Cargo 本地已安装的二进制 crate 集合。仅含可执行 `[[bin]]` 或 `[[example]]` 目标的包可以安装，所有可执行文件都安装到安装根的 `bin` 文件夹中。默认只安装二进制文件，不安装示例。

安装根按以下优先级确定：

- `--root` 选项
- `CARGO_INSTALL_ROOT` 环境变量
- `install.root` Cargo [配置值](../../../cargo-reference/06-configuration/)
- `CARGO_HOME` 环境变量
- `$HOME/.cargo`

crate 可从多个来源安装。默认来源是 crates.io，但 `--git`、`--path` 与 `--registry` 标志可更改来源。若来源包含多个包（如 crates.io 或含多个 crate 的 git 仓库），必须提供 _crate_ 参数以指定要安装的 crate。

来自 crates.io 的 crate 可通过 `--version` 标志可选指定要安装的版本；同样，来自 git 仓库的包也可选指定分支、标签或 revision。若 crate 有多个二进制文件，可用 `--bin` 参数选择性只安装其中一个；若要安装示例，可使用 `--example` 参数。

若包已安装，当已安装版本似乎不是最新时 Cargo 会重新安装。若以下任一值发生变化，Cargo 将重新安装该包：

- 包版本与来源。
- 已安装的二进制名称集合。
- 所选特性。
- 配置文件（`--profile`）。
- 目标（`--target`）。

使用 `--path` 安装时总会构建并安装，除非与来自其他包的二进制文件冲突。可用 `--force` 标志强制 Cargo 始终重新安装该包。

若来源是 crates.io 或 `--git`，默认会在临时目标目录中构建 crate。为避免此行为，可将 `CARGO_TARGET_DIR` 环境变量设为路径以指定目标目录。这在持续集成系统上缓存构建产物时尤其有用。

### 处理锁文件 {#dealing-with-the-lockfile}
默认情况下，包附带的 `Cargo.lock` 文件会被忽略。这意味着 Cargo 会重新计算使用哪些依赖版本，可能使用自包发布以来更新的版本。可用 `--locked` 标志强制 Cargo 使用打包的 `Cargo.lock` 文件（若可用）。这对确保可重现构建、使用包发布时可用的完全相同依赖集合可能有用。若发布了不再能在你的系统上构建或有其他问题的新版依赖，也可能有用。使用 `--locked` 的缺点是，你不会收到任何依赖的修复或更新。请注意，Cargo 直到 1.37 版本才开始发布 `Cargo.lock` 文件，这意味着更早版本发布的包不会有可用的 `Cargo.lock` 文件。

### 配置发现 {#configuration-discovery}
此命令在系统或用户级别运行，而非项目级别。这意味着本地[配置发现]会被忽略。配置发现从 `$CARGO_HOME/config.toml` 开始。若使用 `--path $PATH` 安装包，将使用本地配置，从 `$PATH/.cargo/config.toml` 开始发现。

[配置发现]: ../../../cargo-reference/06-configuration/#hierarchical-structure

## 选项 {#options}
### 安装选项 {#install-options}
<dl>

<dt class="option-term" id="option-cargo-install---vers"><a class="option-anchor" href="#option-cargo-install---vers"><code>--vers</code> <em>version</em></a></dt>
<dt class="option-term" id="option-cargo-install---version"><a class="option-anchor" href="#option-cargo-install---version"><code>--version</code> <em>version</em></a></dt>
<dd class="option-desc"><p>指定要安装的版本。可以是<a href="../../cargo-reference/specifying-dependencies/_index.md">版本要求</a>，如 <code>~1.2</code>，让 Cargo 从给定要求中选择最新版本。若版本没有要求运算符（如 <code>^</code> 或 <code>~</code>），则必须是 <em>MAJOR.MINOR.PATCH</em> 形式，将精确安装该版本；<em>不会</em>像 Cargo 依赖那样被视为 caret 要求。</p>
</dd>


<dt class="option-term" id="option-cargo-install---git"><a class="option-anchor" href="#option-cargo-install---git"><code>--git</code> <em>url</em></a></dt>
<dd class="option-desc"><p>从中安装指定 crate 的 Git URL。</p>
</dd>


<dt class="option-term" id="option-cargo-install---branch"><a class="option-anchor" href="#option-cargo-install---branch"><code>--branch</code> <em>branch</em></a></dt>
<dd class="option-desc"><p>从 git 安装时使用的分支。</p>
</dd>


<dt class="option-term" id="option-cargo-install---tag"><a class="option-anchor" href="#option-cargo-install---tag"><code>--tag</code> <em>tag</em></a></dt>
<dd class="option-desc"><p>从 git 安装时使用的标签。</p>
</dd>


<dt class="option-term" id="option-cargo-install---rev"><a class="option-anchor" href="#option-cargo-install---rev"><code>--rev</code> <em>sha</em></a></dt>
<dd class="option-desc"><p>从 git 安装时使用的特定提交。</p>
</dd>


<dt class="option-term" id="option-cargo-install---path"><a class="option-anchor" href="#option-cargo-install---path"><code>--path</code> <em>path</em></a></dt>
<dd class="option-desc"><p>要从中安装的本地 crate 的文件系统路径。</p>
</dd>


<dt class="option-term" id="option-cargo-install---list"><a class="option-anchor" href="#option-cargo-install---list"><code>--list</code></a></dt>
<dd class="option-desc"><p>列出所有已安装的包及其版本。</p>
</dd>


<dt class="option-term" id="option-cargo-install--n"><a class="option-anchor" href="#option-cargo-install--n"><code>-n</code></a></dt>
<dt class="option-term" id="option-cargo-install---dry-run"><a class="option-anchor" href="#option-cargo-install---dry-run"><code>--dry-run</code></a></dt>
<dd class="option-desc"><p>（不稳定）执行所有检查但不实际安装。</p>
</dd>


<dt class="option-term" id="option-cargo-install--f"><a class="option-anchor" href="#option-cargo-install--f"><code>-f</code></a></dt>
<dt class="option-term" id="option-cargo-install---force"><a class="option-anchor" href="#option-cargo-install---force"><code>--force</code></a></dt>
<dd class="option-desc"><p>强制覆盖现有 crate 或二进制文件。若某包安装的二进制与另一包同名，这很有用。若系统上发生了变化而你想重新构建（例如更新了 <code>rustc</code> 版本），这也很有用。</p>
</dd>


<dt class="option-term" id="option-cargo-install---no-track"><a class="option-anchor" href="#option-cargo-install---no-track"><code>--no-track</code></a></dt>
<dd class="option-desc"><p>默认情况下，Cargo 通过存储在安装根目录的元数据文件跟踪已安装的包。此标志告诉 Cargo 不使用或创建该文件。使用此标志时，除非使用 <code>--force</code> 标志，否则 Cargo 将拒绝覆盖任何现有文件。这也会禁用 Cargo 防止多个并发 Cargo 安装同时进行的能力。</p>
</dd>


<dt class="option-term" id="option-cargo-install---bin"><a class="option-anchor" href="#option-cargo-install---bin"><code>--bin</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>仅安装指定的二进制文件。</p>
</dd>


<dt class="option-term" id="option-cargo-install---bins"><a class="option-anchor" href="#option-cargo-install---bins"><code>--bins</code></a></dt>
<dd class="option-desc"><p>安装所有二进制文件。这是默认行为。</p>
</dd>


<dt class="option-term" id="option-cargo-install---example"><a class="option-anchor" href="#option-cargo-install---example"><code>--example</code> <em>name</em>…</a></dt>
<dd class="option-desc"><p>仅安装指定的示例。</p>
</dd>


<dt class="option-term" id="option-cargo-install---examples"><a class="option-anchor" href="#option-cargo-install---examples"><code>--examples</code></a></dt>
<dd class="option-desc"><p>安装所有示例。</p>
</dd>


<dt class="option-term" id="option-cargo-install---root"><a class="option-anchor" href="#option-cargo-install---root"><code>--root</code> <em>dir</em></a></dt>
<dd class="option-desc"><p>安装包的目标目录。</p>
</dd>


<dt class="option-term" id="option-cargo-install---registry"><a class="option-anchor" href="#option-cargo-install---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要使用的注册表名称。注册表名称在 <a href="../../cargo-reference/06-configuration.md">Cargo 配置文件</a>中定义。若未指定，则使用默认注册表，由 <code>registry.default</code> 配置键定义，默认为 <code>crates-io</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-install---index"><a class="option-anchor" href="#option-cargo-install---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性。若未指定特性选项，每个所选包都会激活 <code>default</code> 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-install--F"><a class="option-anchor" href="#option-cargo-install--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-install---features"><a class="option-anchor" href="#option-cargo-install---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要激活的特性列表。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，以启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-install---all-features"><a class="option-anchor" href="#option-cargo-install---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-install---no-default-features"><a class="option-anchor" href="#option-cargo-install---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-install---target"><a class="option-anchor" href="#option-cargo-install---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>为指定目标架构安装。默认为宿主架构。三元组的一般格式为 <code>&lt;arch&gt;&lt;sub&gt;-&lt;vendor&gt;-&lt;sys&gt;-&lt;abi&gt;</code>。</p>
<p>可能的值：</p>
<ul>
<li><code>rustc --print target-list</code> 中支持的任意目标。</li>
<li><code>"host-tuple"</code>，内部将替换为宿主目标。若你在交叉编译某些 crate，且不想将宿主机器指定为目标（例如多人协作的共享项目中的 <code>xtask</code>），这会特别有用。</li>
<li>自定义目标规范的路径。更多信息见 <a href="https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path">Custom Target Lookup Path</a>。</li>
</ul>
<p>也可通过 <code>build.target</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
<p>请注意，指定此标志会使 Cargo 以不同模式运行，目标产物将放在单独的目录中。更多细节见 <a href="../../cargo-reference/09-build-cache.md">构建缓存</a>文档。</p>
</dd>


<dt class="option-term" id="option-cargo-install---target-dir"><a class="option-anchor" href="#option-cargo-install---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或 <code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为平台临时目录中的新临时文件夹。</p>
<p>使用 <code>--path</code> 时，默认使用本地 crate 工作空间中的 <code>target</code> 目录，除非指定了 <code>--target-dir</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-install---debug"><a class="option-anchor" href="#option-cargo-install---debug"><code>--debug</code></a></dt>
<dd class="option-desc"><p>使用 <code>dev</code> 配置文件构建，而非 <code>release</code> 配置文件。也可参见 <code>--profile</code> 选项以按名称选择特定配置文件。</p>
</dd>


<dt class="option-term" id="option-cargo-install---profile"><a class="option-anchor" href="#option-cargo-install---profile"><code>--profile</code> <em>name</em></a></dt>
<dd class="option-desc"><p>使用给定配置文件安装。关于配置文件的更多细节，见<a href="../../cargo-reference/05-profiles.md">参考文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-install---timings"><a class="option-anchor" href="#option-cargo-install---timings"><code>--timings</code></a></dt>
<dd class="option-desc"><p>输出每次编译耗时信息，并随时间跟踪并发信息。</p>
<p>构建结束时会将文件 <code>cargo-timing.html</code> 写入 <code>target/cargo-timings</code> 目录。若你想查看之前的运行，还会写入文件名带时间戳的额外报告。这些报告仅供人类阅读，不提供机器可读的计时数据。</p>
</dd>



</dl>

### 清单选项 {#manifest-options}
<dl>
<dt class="option-term" id="option-cargo-install---ignore-rust-version"><a class="option-anchor" href="#option-cargo-install---ignore-rust-version"><code>--ignore-rust-version</code></a></dt>
<dd class="option-desc"><p>忽略包中的 <code>rust-version</code> 规范。</p>
</dd>


<dt class="option-term" id="option-cargo-install---locked"><a class="option-anchor" href="#option-cargo-install---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-install---offline"><a class="option-anchor" href="#option-cargo-install---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-install---frozen"><a class="option-anchor" href="#option-cargo-install---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>

</dl>

### 其他选项 {#miscellaneous-options}
<dl>
<dt class="option-term" id="option-cargo-install--j"><a class="option-anchor" href="#option-cargo-install--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-install---jobs"><a class="option-anchor" href="#option-cargo-install---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为逻辑 CPU 数量。若为负数，则最大并行作业数为逻辑 CPU 数加上该值。若提供字符串 <code>default</code>，则恢复为默认值。不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-install---keep-going"><a class="option-anchor" href="#option-cargo-install---keep-going"><code>--keep-going</code></a></dt>
<dd class="option-desc"><p>尽可能构建依赖图中的更多 crate，而不是在第一个构建失败的 crate 处中止。</p>
<p>例如，若当前包依赖 <code>fails</code> 与 <code>works</code>，其中一个构建失败，<code>cargo install -j1</code> 可能会也可能不会构建成功的那一个（取决于 Cargo 先运行哪一个），而 <code>cargo install -j1 --keep-going</code> 则一定会运行两次构建，即便先运行的那个失败。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-install--v"><a class="option-anchor" href="#option-cargo-install--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-install---verbose"><a class="option-anchor" href="#option-cargo-install---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。也可通过 <code>term.verbose</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-install--q"><a class="option-anchor" href="#option-cargo-install--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-install---quiet"><a class="option-anchor" href="#option-cargo-install---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。也可通过 <code>term.quiet</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-install---color"><a class="option-anchor" href="#option-cargo-install---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code>（默认）：自动检测终端是否支持颜色。</li>
<li><code>always</code>：始终显示颜色。</li>
<li><code>never</code>：从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-install---message-format"><a class="option-anchor" href="#option-cargo-install---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
<dd class="option-desc"><p>诊断消息的输出格式。可指定多次，由逗号分隔的值组成。有效值：</p>
<ul>
<li><code>human</code>（默认）：以人类可读的文本格式显示。与 <code>short</code> 和 <code>json</code> 冲突。</li>
<li><code>short</code>：输出更短的人类可读文本消息。与 <code>human</code> 和 <code>json</code> 冲突。</li>
<li><code>json</code>：向 stdout 输出 JSON 消息。更多细节见<a href="../../cargo-reference/11-external-tools.md#json-messages">参考文档</a>。与 <code>human</code> 和 <code>short</code> 冲突。</li>
<li><code>json-diagnostic-short</code>：确保 JSON 消息的 <code>rendered</code> 字段包含来自 rustc 的“short”渲染。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-diagnostic-rendered-ansi</code>：确保 JSON 消息的 <code>rendered</code> 字段包含嵌入式 ANSI 颜色代码，以遵循 rustc 的默认配色方案。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
<li><code>json-render-diagnostics</code>：指示 Cargo 不在输出的 JSON 消息中包含 rustc 诊断，而是由 Cargo 自身渲染来自 rustc 的 JSON 诊断。Cargo 自身的 JSON 诊断以及来自 rustc 的其他诊断仍会输出。不能与 <code>human</code> 或 <code>short</code> 一起使用。</li>
</ul>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-install-+toolchain"><a class="option-anchor" href="#option-cargo-install-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-install---config"><a class="option-anchor" href="#option-cargo-install---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-install--C"><a class="option-anchor" href="#option-cargo-install--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a> 上可用，且需要 <code>-Z unstable-options</code> 标志才能启用（见 <a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-install--h"><a class="option-anchor" href="#option-cargo-install--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-install---help"><a class="option-anchor" href="#option-cargo-install---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-install--Z"><a class="option-anchor" href="#option-cargo-install--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 从 crates.io 安装或升级包：

       cargo install ripgrep

2. 安装或重新安装当前目录中的包：

       cargo install --path .

3. 查看已安装包列表：

       cargo install --list

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-uninstall(1)](../05-cargo-uninstall/), [cargo-search(1)](../04-cargo-search/), [cargo-publish(1)](../../publishing-commands/05-cargo-publish/)
