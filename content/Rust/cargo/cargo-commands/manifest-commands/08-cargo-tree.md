+++
title = "08-cargo tree"
date = 2026-07-30T14:49:00+08:00
weight = 68
type = "docs"
description = "cargo-tree(1) 显示依赖树"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-tree(1) {#cargo-tree1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-tree.html](https://doc.rust-lang.org/cargo/commands/cargo-tree.html)


## 名称 {#name}
cargo-tree --- 以树形可视化显示依赖图

## 大纲 {#synopsis}
`cargo tree` [_options_]

## 描述 {#description}
此命令会在终端显示依赖树。以下是一个依赖 "rand" 包的简单项目示例：

```
myproject v0.1.0 (/myproject)
└── rand v0.7.3
    ├── getrandom v0.1.14
    │   ├── cfg-if v0.1.10
    │   └── libc v0.2.68
    ├── libc v0.2.68 (*)
    ├── rand_chacha v0.2.2
    │   ├── ppv-lite86 v0.2.6
    │   └── rand_core v0.5.1
    │       └── getrandom v0.1.14 (*)
    └── rand_core v0.5.1 (*)
[build-dependencies]
└── cc v1.0.50
```

标记为 `(*)` 的包已被“去重”。该包的依赖已在图中其他位置显示，因此不会重复。使用 `--no-dedupe` 选项可重复显示重复项。

`-e` 标志可用于选择要显示的依赖种类。"features" 种类会改变输出，显示每个依赖启用的特性。例如 `cargo tree -e features`：

```
myproject v0.1.0 (/myproject)
└── log feature "serde"
    └── log v0.4.8
        ├── serde v1.0.106
        └── cfg-if feature "default"
            └── cfg-if v0.1.10
```

在此树中，`myproject` 依赖启用了 `serde` 特性的 `log`。`log` 又依赖启用了 "default" 特性的 `cfg-if`。使用 `-e features` 时，配合 `-i` 标志查看特性如何流入某个包会很有帮助。更多细节见下方示例。

### 特性统一 {#feature-unification}
此命令显示的图更接近 Cargo 实际构建时经过特性统一后的图，而非你在 `Cargo.toml` 中列出的内容。例如，若你在 `[dependencies]` 与 `[dev-dependencies]` 中都指定了同一依赖但启用了不同特性，此命令可能会合并所有特性，并在其中一个依赖上显示 `(*)` 表示重复。

因此，若要大致等价地了解 `cargo build` 的行为，`cargo tree -e normal,build` 相当接近；若要大致等价地了解 `cargo test` 的行为，`cargo tree` 相当接近。然而，它并不保证与 Cargo 实际构建完全一致，因为编译很复杂并取决于许多不同因素。

要了解更多关于特性统一的内容，请参阅[专门章节](../../../cargo-reference/features/#feature-unification)。

## 选项 {#options}
### 树选项 {#tree-options}
<dl>

<dt class="option-term" id="option-cargo-tree--i"><a class="option-anchor" href="#option-cargo-tree--i"><code>-i</code> <em>spec</em></a></dt>
<dt class="option-term" id="option-cargo-tree---invert"><a class="option-anchor" href="#option-cargo-tree---invert"><code>--invert</code> <em>spec</em></a></dt>
<dd class="option-desc"><p>显示给定包的反向依赖。此标志会反转树，显示依赖该包的包。</p>
<p>请注意，在工作空间中，默认仅显示当前目录下工作空间成员树内该包的反向依赖。可用 <code>--workspace</code> 标志扩展为显示整个工作空间内该包的反向依赖。可用 <code>-p</code> 标志仅显示给定 <code>-p</code> 包子树内该包的反向依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---prune"><a class="option-anchor" href="#option-cargo-tree---prune"><code>--prune</code> <em>spec</em></a></dt>
<dd class="option-desc"><p>从依赖树显示中剪枝掉给定包。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---depth"><a class="option-anchor" href="#option-cargo-tree---depth"><code>--depth</code> <em>depth</em></a></dt>
<dd class="option-desc"><p>依赖树的最大显示深度。例如深度 1 只显示直接依赖。</p>
<p>若给定值为 <code>workspace</code>，则仅显示当前工作空间的成员依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---no-dedupe"><a class="option-anchor" href="#option-cargo-tree---no-dedupe"><code>--no-dedupe</code></a></dt>
<dd class="option-desc"><p>不对重复依赖去重。通常，当某个包已显示过其依赖后，后续出现不会再重复显示其依赖，并会包含 <code>(*)</code> 表示已显示过。此标志会导致重复项再次显示。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--d"><a class="option-anchor" href="#option-cargo-tree--d"><code>-d</code></a></dt>
<dt class="option-term" id="option-cargo-tree---duplicates"><a class="option-anchor" href="#option-cargo-tree---duplicates"><code>--duplicates</code></a></dt>
<dd class="option-desc"><p>仅显示存在多个版本的依赖（隐含 <code>--invert</code>）。与 <code>-p</code> 标志一起使用时，仅显示给定包子树内的重复项。</p>
<p>避免多次构建同一包对构建时间和可执行文件大小都有好处。此标志可帮助识别问题包。随后你可以调查依赖较旧版本的包是否可以更新到较新版本，以便只构建一个实例。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--e"><a class="option-anchor" href="#option-cargo-tree--e"><code>-e</code> <em>kinds</em></a></dt>
<dt class="option-term" id="option-cargo-tree---edges"><a class="option-anchor" href="#option-cargo-tree---edges"><code>--edges</code> <em>kinds</em></a></dt>
<dd class="option-desc"><p>要显示的依赖种类。接受逗号分隔的值列表：</p>
<ul>
<li><code>all</code> — 显示所有边种类。</li>
<li><code>normal</code> — 显示普通依赖。</li>
<li><code>build</code> — 显示构建依赖。</li>
<li><code>dev</code> — 显示开发依赖。</li>
<li><code>features</code> — 显示每个依赖启用的特性。若这是唯一给出的种类，则自动包含其他依赖种类。</li>
<li><code>no-normal</code> — 不包含普通依赖。</li>
<li><code>no-build</code> — 不包含构建依赖。</li>
<li><code>no-dev</code> — 不包含开发依赖。</li>
<li><code>no-proc-macro</code> — 不包含过程宏依赖。</li>
</ul>
<p><code>normal</code>、<code>build</code>、<code>dev</code> 与 <code>all</code> 依赖种类不能与 <code>no-normal</code>、<code>no-build</code> 或 <code>no-dev</code> 依赖种类混用。</p>
<p>默认为 <code>normal,build,dev</code>。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---target"><a class="option-anchor" href="#option-cargo-tree---target"><code>--target</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>过滤匹配给定<a href="../../appendix/01-glossary.md#target">目标三元组</a>的依赖。默认为宿主平台。使用值 <code>all</code> 可包含<em>所有</em>目标。</p>
</dd>


</dl>

### 树格式化选项 {#tree-formatting-options}
<dl>

<dt class="option-term" id="option-cargo-tree---charset"><a class="option-anchor" href="#option-cargo-tree---charset"><code>--charset</code> <em>charset</em></a></dt>
<dd class="option-desc"><p>选择用于树的字符集。有效值为 “utf8” 或 “ascii”。未指定时 cargo 会自动选择。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--f"><a class="option-anchor" href="#option-cargo-tree--f"><code>-f</code> <em>format</em></a></dt>
<dt class="option-term" id="option-cargo-tree---format"><a class="option-anchor" href="#option-cargo-tree---format"><code>--format</code> <em>format</em></a></dt>
<dd class="option-desc"><p>设置每个包的格式字符串。默认为 “{p}”。</p>
<p>这是用于显示每个包的任意字符串。以下字符串会被替换为对应值：</p>
<ul>
<li><code>{p}</code>、<code>{package}</code> — 包名。</li>
<li><code>{l}</code>、<code>{license}</code> — 包许可证。</li>
<li><code>{r}</code>、<code>{repository}</code> — 包仓库 URL。</li>
<li><code>{f}</code>、<code>{features}</code> — 已启用包特性的逗号分隔列表。</li>
<li><code>{lib}</code> — 在 <code>use</code> 语句中使用的包库名称。</li>
</ul>
</dd>


<dt class="option-term" id="option-cargo-tree---prefix"><a class="option-anchor" href="#option-cargo-tree---prefix"><code>--prefix</code> <em>prefix</em></a></dt>
<dd class="option-desc"><p>设置每行的显示方式。<em>prefix</em> 值可以是以下之一：</p>
<ul>
<li><code>indent</code>（默认）— 以树形缩进显示每行。</li>
<li><code>depth</code> — 以列表形式显示，每项前打印数字深度。</li>
<li><code>none</code> — 以扁平列表显示。</li>
</ul>
</dd>


</dl>

### 包选择 {#package-selection}
默认情况下，若未指定包选择选项，所选包取决于所选清单文件（若未指定 `--manifest-path`，则基于当前工作目录）。若清单是工作空间的根，则选择工作空间的默认成员；否则仅选择清单定义的包。

工作空间的默认成员可在根清单中通过 `workspace.default-members` 键显式设置。若未设置，虚拟工作空间将包含所有工作空间成员（等价于传入 `--workspace`），非虚拟工作空间则仅包含根 crate 本身。

<dl>

<dt class="option-term" id="option-cargo-tree--p"><a class="option-anchor" href="#option-cargo-tree--p"><code>-p</code> <em>spec</em>…</a></dt>
<dt class="option-term" id="option-cargo-tree---package"><a class="option-anchor" href="#option-cargo-tree---package"><code>--package</code> <em>spec</em>…</a></dt>
<dd class="option-desc"><p>仅显示指定的包。SPEC 格式见 <a href="06-cargo-pkgid.md">cargo-pkgid(1)</a>。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---workspace"><a class="option-anchor" href="#option-cargo-tree---workspace"><code>--workspace</code></a></dt>
<dd class="option-desc"><p>显示工作空间中的所有成员。</p>
</dd>



<dt class="option-term" id="option-cargo-tree---exclude"><a class="option-anchor" href="#option-cargo-tree---exclude"><code>--exclude</code> <em>SPEC</em>…</a></dt>
<dd class="option-desc"><p>排除指定的包。必须与 <code>--workspace</code> 标志一起使用。此标志可指定多次，并支持常见的 Unix glob 模式，如 <code>*</code>、<code>?</code> 和 <code>[]</code>。不过，为避免 shell 在 Cargo 处理之前意外展开 glob 模式，必须用单引号或双引号括住每个模式。</p>
</dd>


</dl>

### 清单选项 {#manifest-options}
<dl>

<dt class="option-term" id="option-cargo-tree---manifest-path"><a class="option-anchor" href="#option-cargo-tree---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索 <code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---locked"><a class="option-anchor" href="#option-cargo-tree---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---offline"><a class="option-anchor" href="#option-cargo-tree---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---frozen"><a class="option-anchor" href="#option-cargo-tree---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性。若未指定特性选项，每个所选包都会激活 <code>default</code> 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-tree--F"><a class="option-anchor" href="#option-cargo-tree--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-tree---features"><a class="option-anchor" href="#option-cargo-tree---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要激活的特性列表。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，以启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---all-features"><a class="option-anchor" href="#option-cargo-tree---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---no-default-features"><a class="option-anchor" href="#option-cargo-tree---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>

<dt class="option-term" id="option-cargo-tree--v"><a class="option-anchor" href="#option-cargo-tree--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-tree---verbose"><a class="option-anchor" href="#option-cargo-tree---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。也可通过 <code>term.verbose</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--q"><a class="option-anchor" href="#option-cargo-tree--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-tree---quiet"><a class="option-anchor" href="#option-cargo-tree---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。也可通过 <code>term.quiet</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---color"><a class="option-anchor" href="#option-cargo-tree---color"><code>--color</code> <em>when</em></a></dt>
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

<dt class="option-term" id="option-cargo-tree-+toolchain"><a class="option-anchor" href="#option-cargo-tree-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-tree---config"><a class="option-anchor" href="#option-cargo-tree---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--C"><a class="option-anchor" href="#option-cargo-tree--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a> 上可用，且需要 <code>-Z unstable-options</code> 标志才能启用（见 <a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--h"><a class="option-anchor" href="#option-cargo-tree--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-tree---help"><a class="option-anchor" href="#option-cargo-tree---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-tree--Z"><a class="option-anchor" href="#option-cargo-tree--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 显示当前目录中包的树：

       cargo tree

2. 显示所有依赖 `syn` 包的包：

       cargo tree -i syn

3. 显示每个包上启用的特性：

       cargo tree --format "{p} {f}"

4. 显示所有被多次构建的包。若树中出现多个 SemVer 不兼容版本（如 1.0.0 与 2.0.0），就可能发生这种情况。

       cargo tree -d

5. 解释 `syn` 包为何启用了某些特性：

       cargo tree -e features -i syn

   `-e features` 标志用于显示特性。`-i` 标志用于反转图，显示依赖 `syn` 的包。可能的输出示例：

   ```
   syn v1.0.17
   ├── syn feature "clone-impls"
   │   └── syn feature "default"
   │       └── rustversion v1.0.2
   │           └── rustversion feature "default"
   │               └── myproject v0.1.0 (/myproject)
   │                   └── myproject feature "default" (command-line)
   ├── syn feature "default" (*)
   ├── syn feature "derive"
   │   └── syn feature "default" (*)
   ├── syn feature "full"
   │   └── rustversion v1.0.2 (*)
   ├── syn feature "parsing"
   │   └── syn feature "default" (*)
   ├── syn feature "printing"
   │   └── syn feature "default" (*)
   ├── syn feature "proc-macro"
   │   └── syn feature "default" (*)
   └── syn feature "quote"
       ├── syn feature "printing" (*)
       └── syn feature "proc-macro" (*)
   ```

   阅读此图时，你可以从根节点沿每条特性的链追溯其被包含的原因。例如，"full" 特性由 `rustversion` crate 添加，它来自 `myproject`（启用了默认特性），而 `myproject` 是命令行选中的包。所有其他 `syn` 特性都由 "default" 特性添加（"quote" 由 "printing" 和 "proc-macro" 添加，二者都是默认特性）。

   若难以对照去重后的 `(*)` 条目，可尝试使用 `--no-dedupe` 标志获取完整输出。

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-metadata(1)](../05-cargo-metadata/)
