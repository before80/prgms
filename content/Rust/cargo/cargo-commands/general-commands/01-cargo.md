+++
title = "01-cargo"
date = 2026-07-30T14:49:00+08:00
weight = 42
type = "docs"
description = "cargo(1) 主命令说明"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo(1) {#cargo1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo.html](https://doc.rust-lang.org/cargo/commands/cargo.html)


## 名称 {#name}
cargo --- Rust 包管理器

## 大纲 {#synopsis}
`cargo` [_options_] _command_ [_args_]\
`cargo` [_options_] `--version`\
`cargo` [_options_] `--list`\
`cargo` [_options_] `--help`\
`cargo` [_options_] `--explain` _code_

## 描述 {#description}
本程序是 Rust 语言的包管理器与构建工具，可在 <https://rust-lang.org> 获取。

_command_ 可以是以下之一：
- 内置命令，见下文
- [别名（aliases）]
- [外部工具]

[别名（aliases）]: ../../../cargo-reference/06-configuration/#alias
[外部工具]: ../../../cargo-reference/11-external-tools/#custom-subcommands

## 命令 {#commands}
### 构建命令 {#build-commands}
[cargo-bench(1)](../../build-commands/01-cargo-bench/)\
&nbsp;&nbsp;&nbsp;&nbsp;执行包的基准测试。

[cargo-build(1)](../../build-commands/02-cargo-build/)\
&nbsp;&nbsp;&nbsp;&nbsp;编译一个包。

[cargo-check(1)](../../build-commands/03-cargo-check/)\
&nbsp;&nbsp;&nbsp;&nbsp;检查本地包及其所有依赖是否有错误。

[cargo-clean(1)](../../build-commands/04-cargo-clean/)\
&nbsp;&nbsp;&nbsp;&nbsp;移除 Cargo 过去生成的产物。

[cargo-doc(1)](../../build-commands/06-cargo-doc/)\
&nbsp;&nbsp;&nbsp;&nbsp;构建包的文档。

[cargo-fetch(1)](../../build-commands/07-cargo-fetch/)\
&nbsp;&nbsp;&nbsp;&nbsp;从网络获取包的依赖。

[cargo-fix(1)](../../build-commands/08-cargo-fix/)\
&nbsp;&nbsp;&nbsp;&nbsp;自动修复 rustc 报告的 lint 警告。

[cargo-run(1)](../../build-commands/11-cargo-run/)\
&nbsp;&nbsp;&nbsp;&nbsp;运行本地包的二进制目标或示例。

[cargo-rustc(1)](../../build-commands/12-cargo-rustc/)\
&nbsp;&nbsp;&nbsp;&nbsp;编译包，并向编译器传递额外选项。

[cargo-rustdoc(1)](../../build-commands/13-cargo-rustdoc/)\
&nbsp;&nbsp;&nbsp;&nbsp;使用指定的自定义标志构建包的文档。

[cargo-test(1)](../../build-commands/14-cargo-test/)\
&nbsp;&nbsp;&nbsp;&nbsp;执行包的单元测试与集成测试。

### Manifest 命令 {#manifest-commands}
[cargo-add(1)](../../manifest-commands/01-cargo-add/)\
&nbsp;&nbsp;&nbsp;&nbsp;向 `Cargo.toml` 清单文件添加依赖。

[cargo-generate-lockfile(1)](../../manifest-commands/02-cargo-generate-lockfile/)\
&nbsp;&nbsp;&nbsp;&nbsp;为项目生成 `Cargo.lock`。

[cargo-info(1)](../../manifest-commands/03-cargo-info/)\
&nbsp;&nbsp;&nbsp;&nbsp;显示注册表中包的信息。默认注册表为 crates.io。

[cargo-locate-project(1)](../../manifest-commands/04-cargo-locate-project/)\
&nbsp;&nbsp;&nbsp;&nbsp;以 JSON 形式打印 `Cargo.toml` 文件的位置。

[cargo-metadata(1)](../../manifest-commands/05-cargo-metadata/)\
&nbsp;&nbsp;&nbsp;&nbsp;以机器可读格式输出包的已解析依赖。

[cargo-pkgid(1)](../../manifest-commands/06-cargo-pkgid/)\
&nbsp;&nbsp;&nbsp;&nbsp;打印完全限定的包规范。

[cargo-remove(1)](../../manifest-commands/07-cargo-remove/)\
&nbsp;&nbsp;&nbsp;&nbsp;从 `Cargo.toml` 清单文件移除依赖。

[cargo-tree(1)](../../manifest-commands/08-cargo-tree/)\
&nbsp;&nbsp;&nbsp;&nbsp;以树形可视化显示依赖图。

[cargo-update(1)](../../manifest-commands/09-cargo-update/)\
&nbsp;&nbsp;&nbsp;&nbsp;按本地锁文件记录更新依赖。

[cargo-vendor(1)](../../manifest-commands/10-cargo-vendor/)\
&nbsp;&nbsp;&nbsp;&nbsp;将所有依赖供应商化到本地。

### 包命令 {#package-commands}
[cargo-init(1)](../../package-commands/01-cargo-init/)\
&nbsp;&nbsp;&nbsp;&nbsp;在已有目录中创建新的 Cargo 包。

[cargo-install(1)](../../package-commands/02-cargo-install/)\
&nbsp;&nbsp;&nbsp;&nbsp;构建并安装 Rust 二进制程序。

[cargo-new(1)](../../package-commands/03-cargo-new/)\
&nbsp;&nbsp;&nbsp;&nbsp;创建新的 Cargo 包。

[cargo-search(1)](../../package-commands/04-cargo-search/)\
&nbsp;&nbsp;&nbsp;&nbsp;在 crates.io 中搜索包。

[cargo-uninstall(1)](../../package-commands/05-cargo-uninstall/)\
&nbsp;&nbsp;&nbsp;&nbsp;移除 Rust 二进制程序。

### 发布命令 {#publishing-commands}
[cargo-login(1)](../../publishing-commands/01-cargo-login/)\
&nbsp;&nbsp;&nbsp;&nbsp;将注册表的 API token 保存到本地。

[cargo-logout(1)](../../publishing-commands/02-cargo-logout/)\
&nbsp;&nbsp;&nbsp;&nbsp;从本地移除注册表的 API token。

[cargo-owner(1)](../../publishing-commands/03-cargo-owner/)\
&nbsp;&nbsp;&nbsp;&nbsp;管理注册表上 crate 的所有者。

[cargo-package(1)](../../publishing-commands/04-cargo-package/)\
&nbsp;&nbsp;&nbsp;&nbsp;将本地包组装为可分发的 tarball。

[cargo-publish(1)](../../publishing-commands/05-cargo-publish/)\
&nbsp;&nbsp;&nbsp;&nbsp;将包上传到注册表。

[cargo-yank(1)](../../publishing-commands/06-cargo-yank/)\
&nbsp;&nbsp;&nbsp;&nbsp;从索引中移除已推送的 crate。

### 报告命令 {#report-commands}
[cargo-report(1)](../../report-commands/01-cargo-report/)\
&nbsp;&nbsp;&nbsp;&nbsp;生成并显示各类报告。

[cargo-report-future-incompatibilities(1)](../../report-commands/02-cargo-report-future-incompatibilities/)\
&nbsp;&nbsp;&nbsp;&nbsp;报告最终将无法编译的任何 crate。

### 通用命令 {#general-commands}
[cargo-help(1)](../02-cargo-help/)\
&nbsp;&nbsp;&nbsp;&nbsp;显示关于 Cargo 的帮助信息。

[cargo-version(1)](../03-cargo-version/)\
&nbsp;&nbsp;&nbsp;&nbsp;显示版本信息。

## 选项 {#options}
### 特殊选项 {#special-options}
<dl>

<dt class="option-term" id="option-cargo--V"><a class="option-anchor" href="#option-cargo--V"><code>-V</code></a></dt>
<dt class="option-term" id="option-cargo---version"><a class="option-anchor" href="#option-cargo---version"><code>--version</code></a></dt>
<dd class="option-desc"><p>打印版本信息并退出。若与 <code>--verbose</code> 一起使用，会打印额外信息。</p>
</dd>


<dt class="option-term" id="option-cargo---list"><a class="option-anchor" href="#option-cargo---list"><code>--list</code></a></dt>
<dd class="option-desc"><p>列出所有已安装的 Cargo 子命令。若与 <code>--verbose</code> 一起使用，会打印额外信息。</p>
</dd>


<dt class="option-term" id="option-cargo---explain"><a class="option-anchor" href="#option-cargo---explain"><code>--explain</code> <em>code</em></a></dt>
<dd class="option-desc"><p>运行 <code>rustc --explain CODE</code>，打印错误消息的详细说明（例如 <code>E0004</code>）。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>

<dt class="option-term" id="option-cargo--v"><a class="option-anchor" href="#option-cargo--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo---verbose"><a class="option-anchor" href="#option-cargo---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得「非常详细」的输出，其中包括依赖警告与构建脚本输出等额外信息。
也可通过 <code>term.verbose</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo--q"><a class="option-anchor" href="#option-cargo--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo---quiet"><a class="option-anchor" href="#option-cargo---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。
也可通过 <code>term.quiet</code>
<a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo---color"><a class="option-anchor" href="#option-cargo---color"><code>--color</code> <em>when</em></a></dt>
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
<dt class="option-term" id="option-cargo---locked"><a class="option-anchor" href="#option-cargo---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用与生成现有 <code>Cargo.lock</code> 文件时完全相同的依赖与版本。出现以下任一情况时，Cargo 将以错误退出：</p>
<ul>
<li>缺少锁文件。</li>
<li>由于依赖解析不同，Cargo 试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo---offline"><a class="option-anchor" href="#option-cargo---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>禁止 Cargo 因任何原因访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能的情况下尝试在无网络时继续。</p>
<p>注意：这可能导致与在线模式不同的依赖解析结果。Cargo 将仅使用本地已下载的 crate，即使本地索引副本表明可能有更新版本。
可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线使用。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo---frozen"><a class="option-anchor" href="#option-cargo---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>

</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-+toolchain"><a class="option-anchor" href="#option-cargo-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。
关于工具链覆盖的工作方式，请参阅 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo---config"><a class="option-anchor" href="#option-cargo---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。
更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo--C"><a class="option-anchor" href="#option-cargo--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响诸如 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly
通道</a> 可用，
并需要 <code>-Z unstable-options</code> 标志才能启用（见
<a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo--h"><a class="option-anchor" href="#option-cargo--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo---help"><a class="option-anchor" href="#option-cargo---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo--Z"><a class="option-anchor" href="#option-cargo--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境变量 {#environment}
参见[参考文档](../../../cargo-reference/07-environment-variables/)了解 Cargo 读取的环境变量详情。

## 退出状态 {#exit-status}
* `0`：Cargo 成功完成。
* `101`：Cargo 未能完成。

## 文件 {#files}
`~/.cargo/`\
&nbsp;&nbsp;&nbsp;&nbsp;Cargo「主目录」的默认位置，用于存储各类文件。可通过 `CARGO_HOME`
环境变量更改位置。

`$CARGO_HOME/bin/`\
&nbsp;&nbsp;&nbsp;&nbsp;由 [cargo-install(1)](../../package-commands/02-cargo-install/) 安装的二进制程序位于此处。若使用
[rustup]，随 Rust 分发的可执行文件也位于此处。

`$CARGO_HOME/config.toml`\
&nbsp;&nbsp;&nbsp;&nbsp;全局配置文件。关于配置文件的更多信息见[参考文档](../../../cargo-reference/06-configuration/)。

`.cargo/config.toml`\
&nbsp;&nbsp;&nbsp;&nbsp;Cargo 会自动在当前目录及其所有父目录中搜索名为 `.cargo/config.toml` 的文件。这些配置文件
将与全局配置文件合并。

`$CARGO_HOME/credentials.toml`\
&nbsp;&nbsp;&nbsp;&nbsp;用于登录注册表的私有认证信息。

`$CARGO_HOME/registry/`\
&nbsp;&nbsp;&nbsp;&nbsp;此目录包含注册表索引与任何已下载依赖的缓存。

`$CARGO_HOME/git/`\
&nbsp;&nbsp;&nbsp;&nbsp;此目录包含 git 依赖的缓存下载。

请注意，`$CARGO_HOME` 目录的内部结构尚不稳定，可能会变更。

[rustup]: https://rust-lang.github.io/rustup/

## 示例 {#examples}
1. 构建本地包及其所有依赖：

       cargo build

2. 以优化方式构建包：

       cargo build --release

3. 为交叉编译目标运行测试：

       cargo test --target i686-unknown-linux-gnu

4. 创建构建可执行文件的新包：

       cargo new foobar

5. 在当前目录创建包：

       mkdir foo && cd foo
       cargo init .

6. 了解命令的选项与用法：

       cargo help clean

## 缺陷 {#bugs}
问题跟踪见 <https://github.com/rust-lang/cargo/issues>。

## 参见 {#see-also}
[rustc(1)](https://doc.rust-lang.org/rustc/index.html)、[rustdoc(1)](https://doc.rust-lang.org/rustdoc/index.html)
