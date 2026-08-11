+++
title = "04-cargo package"
date = 2026-07-30T14:49:00+08:00
weight = 81
type = "docs"
description = "cargo-package(1) 打包分发包"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-package(1) {#cargo-package1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-package.html](https://doc.rust-lang.org/cargo/commands/cargo-package.html)


## 名称 {#name}
cargo-package --- 将本地包组装为可分发压缩包

## 大纲 {#synopsis}
`cargo package` [_options_]

## 描述 {#description}
此命令会为当前目录中的包创建可分发、压缩的 `.crate` 文件（含源代码）。生成的文件保存在 `target/package` 目录中。执行步骤如下：

1. 加载并检查当前工作空间，执行一些基本检查。
    - 除非路径依赖带有 version 键，否则不允许使用路径依赖。Cargo 在已发布包中会忽略依赖的 path 键。`dev-dependencies` 不受此限制。
2. 创建压缩的 `.crate` 文件。
    - 原始 `Cargo.toml` 文件会被重写并规范化。
    - 清单中的 `[patch]`、`[replace]` 与 `[workspace]` 节会被移除。
    - 始终包含 `Cargo.lock`。若缺失，将生成新的锁文件，除非使用了 `--exclude-lockfile` 标志。若使用 `--locked` 标志，[cargo-install(1)](../../package-commands/02-cargo-install/) 会使用打包的锁文件。
    - 包含 `.cargo_vcs_info.json` 文件，其中记录当前 VCS 检出哈希（若可用），以及工作树是否 dirty 的标志。
    - 符号链接会被展平为其目标文件。
    - 根据[ `[include]` 与 `[exclude]` 字段](../../../cargo-reference/the-manifest-format/#the-exclude-and-include-fields) 中的规则包含或排除文件与目录。

3. 解压 `.crate` 文件并构建，以验证其可以构建。
    - 这会从头重新构建你的包，确保可以从干净状态构建。可用 `--no-verify` 标志跳过此步骤。
4. 检查构建脚本是否修改了任何源文件。

包含的文件列表可通过清单中的 `include` 与 `exclude` 字段控制。

关于打包与发布的更多细节，见[参考文档](../../../cargo-guide/09-publishing-on-crates-io/)。

### .cargo_vcs_info.json 格式 {#cargo_vcs_infojson-format}
将生成如下格式的 `.cargo_vcs_info.json`：

```javascript
{
 "git": {
   "sha1": "aac20b6e7e543e6dd4118b246c77225e3a3a1302",
   "dirty": true
 },
 "path_in_vcs": ""
}
```

`dirty` 表示打包时 Git 工作树处于 dirty 状态。

`path_in_vcs` 对于版本控制仓库子目录中的包，会设置为相对于仓库的路径。

此文件的兼容性策略与 [cargo-metadata(1)](../../manifest-commands/05-cargo-metadata/) 的 JSON 输出相同。

请注意，此文件提供的是 VCS 信息的最佳努力快照。然而，包的来源并未被验证。无法保证压缩包中的源代码与 VCS 信息一致。

## 选项 {#options}
### 打包选项 {#package-options}
<dl>

<dt class="option-term" id="option-cargo-package--l"><a class="option-anchor" href="#option-cargo-package--l"><code>-l</code></a></dt>
<dt class="option-term" id="option-cargo-package---list"><a class="option-anchor" href="#option-cargo-package---list"><code>--list</code></a></dt>
<dd class="option-desc"><p>列出包中将包含的文件，但不实际创建包。</p>
</dd>


<dt class="option-term" id="option-cargo-package---no-verify"><a class="option-anchor" href="#option-cargo-package---no-verify"><code>--no-verify</code></a></dt>
<dd class="option-desc"><p>不通过构建来验证内容。</p>
</dd>


<dt class="option-term" id="option-cargo-package---no-metadata"><a class="option-anchor" href="#option-cargo-package---no-metadata"><code>--no-metadata</code></a></dt>
<dd class="option-desc"><p>忽略缺少人类可读元数据（如 description 或 license）的警告。</p>
</dd>


<dt class="option-term" id="option-cargo-package---allow-dirty"><a class="option-anchor" href="#option-cargo-package---allow-dirty"><code>--allow-dirty</code></a></dt>
<dd class="option-desc"><p>允许打包含有未提交 VCS 变更的工作目录。</p>
</dd>


<dt class="option-term" id="option-cargo-package---exclude-lockfile"><a class="option-anchor" href="#option-cargo-package---exclude-lockfile"><code>--exclude-lockfile</code></a></dt>
<dd class="option-desc"><p>打包时不包含锁文件。</p>
<p>此标志并非供一般使用。某些工具可能期望存在锁文件（例如 <code>cargo install --locked</code>）。使用前请考虑其他选项。</p>
</dd>


<dt class="option-term" id="option-cargo-package---index"><a class="option-anchor" href="#option-cargo-package---index"><code>--index</code> <em>index</em></a></dt>
<dd class="option-desc"><p>要使用的注册表索引 URL。</p>
</dd>


<dt class="option-term" id="option-cargo-package---registry"><a class="option-anchor" href="#option-cargo-package---registry"><code>--registry</code> <em>registry</em></a></dt>
<dd class="option-desc"><p>要为其打包的注册表名称；注册表名称的配置详见 <code>cargo publish --help</code>。包不会发布到该注册表，但若我们在打包多个相互依赖的 crate，锁文件将在假设依赖将发布到该注册表的前提下生成。</p>
</dd>


<dt class="option-term" id="option-cargo-package---message-format"><a class="option-anchor" href="#option-cargo-package---message-format"><code>--message-format</code> <em>fmt</em></a></dt>
<dd class="option-desc"><p>指定输出消息格式。目前仅与 <code>--list</code> 配合使用，并影响文件列表格式。此功能不稳定，需要 <code>-Zunstable-options</code>。有效输出格式：</p>
<ul>
<li><code>human</code>（默认）：每行一个文件的格式显示。</li>
<li><code>json</code>：输出关于每个包的机器可读 JSON 信息。每个包一行 JSON（换行分隔的 JSON）。
<pre><code class="language-javascript">{
  /* 包的 Package ID Spec。 */
  "id": "path+file:///home/foo#0.0.0",
  /* 此包的文件 */
  "files" {
    /* 归档文件中的相对路径。 */
    "Cargo.toml.orig": {
      /* 文件来源。
         - "generate" 表示打包过程中生成的文件
         - "copy" 表示从其他位置复制的文件
      */
      "kind": "copy",
      /* 对于 "copy" 类型，
         为实际文件内容的绝对路径。
         对于 "generate" 类型，
         为生成文件所基于的原始文件。
      */
      "path": "/home/foo/Cargo.toml"
    },
    "Cargo.toml": {
      "kind": "generate",
      "path": "/home/foo/Cargo.toml"
    },
    "src/main.rs": {
      "kind": "copy",
      "path": "/home/foo/src/main.rs"
    }
  }
}
</code></pre>
</li>
</ul>
</dd>


</dl>

### 包选择 {#package-selection}
默认情况下，若未指定包选择选项，所选包取决于所选清单文件（若未指定 `--manifest-path`，则基于当前工作目录）。若清单是工作空间的根，则选择工作空间的默认成员；否则仅选择清单定义的包。

工作空间的默认成员可在根清单中通过 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间则仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-package--p"><a class="option-anchor" href="#option-cargo-package--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-package---package"><a class="option-anchor" href="#option-cargo-package---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>仅打包指定的包。SPEC 格式见 <a href="../manifest-commands/06-cargo-pkgid.md">cargo-pkgid(1)</a>。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-package---workspace"><a class="option-anchor" href="#option-cargo-package---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>打包工作空间中的所有成员。</p>
</dd>



<dt class="option-term" id="option-cargo-package---exclude"><a class="option-anchor" href="#option-cargo-package---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 编译选项 {#compilation-options}
<dl>

<dt class="option-term" id="option-cargo-package---target"><a class="option-anchor" href="#option-cargo-package---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>为指定目标架构打包。此标志可指定多次。默认为宿主架构。三元组的一般格式为 <code>&lt;arch&gt;&lt;sub&gt;-&lt;vendor&gt;-&lt;sys&gt;-&lt;abi&gt;</code>。</p>
<p>可能的值：</p>
<ul>
<li><code>rustc --print target-list</code> 中支持的任意目标。</li>
<li><code>"host-tuple"</code>，内部将替换为宿主目标。若你在交叉编译某些 crate，且不想将宿主机器指定为目标（例如多人协作的共享项目中的 <code>xtask</code>），这会特别有用。</li>
<li>自定义目标规范的路径。更多信息见 <a href="https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path">Custom Target Lookup Path</a>。</li>
</ul>
<p>也可通过 <code>build.target</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
<p>请注意，指定此标志会使 Cargo 以不同模式运行，目标产物将放在单独的目录中。更多细节见 <a href="../../cargo-reference/09-build-cache.md">构建缓存</a>文档。</p>
</dd>


<dt class="option-term" id="option-cargo-package---target-dir"><a class="option-anchor" href="#option-cargo-package---target-dir"><code>--target-dir</code> <em>directory</em></a></dt>
<dd class="option-desc"><p>所有生成产物与中间文件的目录。也可通过 <code>CARGO_TARGET_DIR</code> 环境变量或 <code>build.target-dir</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为工作空间根目录下的 <code>target</code>。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性。若未指定特性选项，每个所选包都会激活 <code>default</code> 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-package--F"><a class="option-anchor" href="#option-cargo-package--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-package---features"><a class="option-anchor" href="#option-cargo-package---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要激活的特性列表。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，以启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-package---all-features"><a class="option-anchor" href="#option-cargo-package---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-package---no-default-features"><a class="option-anchor" href="#option-cargo-package---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 清单选项 {#manifest-options}
<dl>

<dt class="option-term" id="option-cargo-package---manifest-path"><a class="option-anchor" href="#option-cargo-package---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索 <code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-package---locked"><a class="option-anchor" href="#option-cargo-package---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-package---offline"><a class="option-anchor" href="#option-cargo-package---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-package---frozen"><a class="option-anchor" href="#option-cargo-package---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>



</dl>

### 其他选项 {#miscellaneous-options}
<dl>
<dt class="option-term" id="option-cargo-package--j"><a class="option-anchor" href="#option-cargo-package--j"><code>-j</code> <em>N</em></a></dt>
<dt class="option-term" id="option-cargo-package---jobs"><a class="option-anchor" href="#option-cargo-package---jobs"><code>--jobs</code> <em>N</em></a></dt>
<dd class="option-desc"><p>并行作业数。也可通过 <code>build.jobs</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。默认为逻辑 CPU 数量。若为负数，则最大并行作业数为逻辑 CPU 数加上该值。若提供字符串 <code>default</code>，则恢复为默认值。不应为 0。</p>
</dd>

<dt class="option-term" id="option-cargo-package---keep-going"><a class="option-anchor" href="#option-cargo-package---keep-going"><code>--keep-going</code></a></dt>
<dd class="option-desc"><p>尽可能构建依赖图中的更多 crate，而不是在第一个构建失败的 crate 处中止。</p>
<p>例如，若当前包依赖 <code>fails</code> 与 <code>works</code>，其中一个构建失败，<code>cargo package -j1</code> 可能会也可能不会构建成功的那一个（取决于 Cargo 先运行哪一个），而 <code>cargo package -j1 --keep-going</code> 则一定会运行两次构建，即便先运行的那个失败。</p>
</dd>

</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-package--v"><a class="option-anchor" href="#option-cargo-package--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-package---verbose"><a class="option-anchor" href="#option-cargo-package---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。也可通过 <code>term.verbose</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-package--q"><a class="option-anchor" href="#option-cargo-package--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-package---quiet"><a class="option-anchor" href="#option-cargo-package---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。也可通过 <code>term.quiet</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-package---color"><a class="option-anchor" href="#option-cargo-package---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-package-+toolchain"><a class="option-anchor" href="#option-cargo-package-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-package---config"><a class="option-anchor" href="#option-cargo-package---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-package--C"><a class="option-anchor" href="#option-cargo-package--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a> 上可用，且需要 <code>-Z unstable-options</code> 标志才能启用（见 <a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-package--h"><a class="option-anchor" href="#option-cargo-package--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-package---help"><a class="option-anchor" href="#option-cargo-package---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-package--Z"><a class="option-anchor" href="#option-cargo-package--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 为当前包创建压缩的 `.crate` 文件：

       cargo package

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-publish(1)](../05-cargo-publish/)
