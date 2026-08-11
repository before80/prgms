+++
title = "05-cargo metadata"
date = 2026-07-30T14:49:00+08:00
weight = 65
type = "docs"
description = "cargo-metadata(1) 机器可读元数据"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# cargo-metadata(1) {#cargo-metadata1}


> 原文链接: [https://doc.rust-lang.org/cargo/commands/cargo-metadata.html](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html)


## 名称 {#name}
cargo-metadata --- 关于当前包的机器可读元数据

## 大纲 {#synopsis}
`cargo metadata` [_options_]

## 描述 {#description}
向 stdout 输出 JSON，其中包含当前包的工作空间成员与已解析依赖的信息。

输出格式可能在 Cargo 未来版本中变更。建议包含 `--format-version` 标志以使代码面向未来，并确保输出符合预期格式。关于预期，见[「兼容性」](#compatibility)。

参见 [cargo_metadata crate](https://crates.io/crates/cargo_metadata) 获取用于读取元数据的 Rust API。

## 输出格式 {#output-format}
### 兼容性 {#compatibility}

在同一输出格式版本内，兼容性会得以保持，但某些场景除外。以下是不被视为不兼容变更的非穷尽列表：

* **添加新字段** — 需要时会添加新字段。保留此能力有助于 Cargo 演进，而无需过于频繁地提升格式版本。
* **为类枚举字段添加新值** — 与添加新字段相同。这使元数据能够演进而不停滞。
* **更改不透明表示** — 某些字段的内部表示是实现细节。例如，与「Source ID」相关的字段被视为不透明标识符，用于区分包或来源。除非另有说明，消费者不应依赖这些表示。

### JSON 格式 {#json-format}
JSON 输出具有以下格式：

```javascript
{
    /* 工作空间中所有包的数组。
       除非使用 --no-deps，否则还包括所有启用了特性的依赖。
    */
    "packages": [
        {
            /* 包的名称。 */
            "name": "my-package",
            /* 包的版本。 */
            "version": "0.1.0",
            /* 用于在文档内引用该包以及作为许多命令的 `--package` 参数的 Package ID。 */
            "id": "file:///path/to/my-package#0.1.0",
            /* 清单中的 license 值，或 null。 */
            "license": "MIT/Apache-2.0",
            /* 清单中的 license-file 值，或 null。 */
            "license_file": "LICENSE",
            /* 清单中的 description 值，或 null。 */
            "description": "Package description.",
            /* 包的 source ID，表示包来源的「不透明」标识符。稳定性保证见上文「兼容性」。

               路径依赖与工作空间成员为 null。

               对于其他依赖，它是如下格式的字符串：
               - 基于注册表的依赖为 "registry+URL"。
                 示例："registry+https://github.com/rust-lang/crates.io-index"
               - 基于 git 的依赖为 "git+URL"。
                 示例："git+https://github.com/rust-lang/cargo?rev=5e85ba14aaa20f8133863373404cb0af69eeef2c#5e85ba14aaa20f8133863373404cb0af69eeef2c"
               - 来自 sparse 注册表的依赖为 "sparse+URL"。
                 示例："sparse+https://my-sparse-registry.org"

               `+` 之后的值没有明确定义，可能在 Cargo 版本之间变化，
               且不一定与配置文件中的注册表定义等其他内容直接对应。
               未来可能添加具有不同 `+` 前缀标识符的新来源种类。
            */
            "source": null,
            /* 包清单中声明的依赖数组。 */
            "dependencies": [
                {
                    /* 依赖的名称。 */
                    "name": "bitflags",
                    /* 依赖的 source ID。可能为 null，见包的 source 说明。 */
                    "source": "registry+https://github.com/rust-lang/crates.io-index",
                    /* 依赖的版本要求。
                       没有版本要求的依赖值为 "*"。
                    */
                    "req": "^1.0",
                    /* 依赖种类。
                       "dev"、"build"，或普通依赖为 null。
                    */
                    "kind": null,
                    /* 若依赖被重命名，此为依赖的新名称字符串。未重命名则为 null。 */
                    "rename": null,
                    /* 是否为可选依赖的布尔值。 */
                    "optional": false,
                    /* 是否启用默认特性的布尔值。 */
                    "uses_default_features": true,
                    /* 已启用的特性数组。 */
                    "features": [],
                    /* 依赖的目标平台。
                       非目标依赖时为 null。
                    */
                    "target": "cfg(windows)",
                    /* 本地路径依赖的文件系统路径。
                       非路径依赖时不存在。
                    */
                    "path": "/path/to/dep",
                    /* 此依赖所属注册表 URL 的字符串。
                       未指定或为 null 时，依赖来自默认注册表（crates.io）。
                    */
                    "registry": null,
                    /* （不稳定）是否为 public 依赖的布尔标志。
                       仅在启用 `-Zpublic-dependency` 时出现此字段。
                    */
                    "public": false
                }
            ],
            /* Cargo 目标数组。 */
            "targets": [
                {
                    /* 目标种类数组。
                       - lib 目标列出清单中的 `crate-type` 值，如 "lib"、"rlib"、"dylib"、"proc-macro" 等（默认 ["lib"]）
                       - binary 为 ["bin"]
                       - example 为 ["example"]
                       - 集成测试为 ["test"]
                       - benchmark 为 ["bench"]
                       - 构建脚本为 ["custom-build"]
                    */
                    "kind": [
                        "bin"
                    ],
                    /* crate 类型数组。
                       - lib 与 example 库列出清单中的 `crate-type` 值，如 "lib"、"rlib"、"dylib"、"proc-macro" 等（默认 ["lib"]）
                       - 所有其他目标种类为 ["bin"]
                    */
                    "crate_types": [
                        "bin"
                    ],
                    /* 目标名称。
                       对于 lib 目标，连字符会替换为下划线。
                    */
                    "name": "my-package",
                    /* 目标根源文件的绝对路径。 */
                    "src_path": "/path/to/my-package/src/main.rs",
                    /* 目标的 Rust edition。
                       默认为包的 edition。
                    */
                    "edition": "2018",
                    /* 必需特性数组。
                       若未设置必需特性，则不包含此属性。
                    */
                    "required-features": ["feat1"],
                    /* 该目标是否应由 `cargo doc` 生成文档。 */
                    "doc": true,
                    /* 该目标是否启用了 doc 测试，且目标与 doc 测试兼容。 */
                    "doctest": false,
                    /* 该目标是否应使用 `--test` 构建并运行。 */
                    "test": true
                }
            ],
            /* 为包定义的特性集合。
               每个特性映射到它启用的特性或依赖数组。
            */
            "features": {
                "default": [
                    "feat1"
                ],
                "feat1": [],
                "feat2": []
            },
            /* 此包清单的绝对路径。 */
            "manifest_path": "/path/to/my-package/Cargo.toml",
            /* 包元数据。
               未指定元数据时为 null。
            */
            "metadata": {
                "docs": {
                    "rs": {
                        "all-features": true
                    }
                }
            },
            /* 此包可发布到的注册表列表。
               为 null 表示发布不受限制，为空数组表示禁止发布。 */
            "publish": [
                "crates-io"
            ],
            /* 清单中的作者数组。
               未指定作者时为空数组。
            */
            "authors": [
                "Jane Doe <user@example.com>"
            ],
            /* 清单中的类别数组。 */
            "categories": [
                "command-line-utilities"
            ],
            /* 可选字符串，为 cargo run 默认选择的二进制文件。 */
            "default_run": null,
            /* 可选字符串，为最低支持的 rust 版本。 */
            "rust_version": "1.56",
            /* 清单中的关键词数组。 */
            "keywords": [
                "cli"
            ],
            /* 清单中的 readme 值，未指定时为 null。 */
            "readme": "README.md",
            /* 清单中的 repository 值，未指定时为 null。 */
            "repository": "https://github.com/rust-lang/cargo",
            /* 清单中的 homepage 值，未指定时为 null。 */
            "homepage": "https://rust-lang.org",
            /* 清单中的 documentation 值，未指定时为 null。 */
            "documentation": "https://doc.rust-lang.org/stable/std",
            /* 包的默认 edition。
               请注意，单个目标可能有不同的 edition。
            */
            "edition": "2018",
            /* 可选字符串，为包链接到的原生库名称。 */
            "links": null,
        }
    ],
    /* 工作空间成员数组。
       每项为包的 Package ID。
    */
    "workspace_members": [
        "file:///path/to/my-package#0.1.0",
    ],
    /* 工作空间默认成员数组。
       每项为包的 Package ID。
    */
    "workspace_default_members": [
        "file:///path/to/my-package#0.1.0",
    ],
    // 整个工作空间的已解析依赖图。启用的特性基于「当前」包启用的特性。
    // 未激活的可选依赖不会列出。
    //
    // 若指定 --no-deps，则为 null。
    //
    // 默认包含所有目标平台的所有依赖。
    // 可用 --filter-platform 标志缩小到特定目标三元组。
    "resolve": {
        /* 依赖图中的节点数组。
           每个节点是一个包。
        */
        "nodes": [
            {
                /* 此节点的 Package ID。 */
                "id": "file:///path/to/my-package#0.1.0",
                /* 此包的依赖，Package ID 数组。 */
                "dependencies": [
                    "https://github.com/rust-lang/crates.io-index#bitflags@1.0.4"
                ],
                /* 此包的依赖。这是 "dependencies" 的替代形式，包含额外信息。
                   特别是，它处理重命名的依赖。
                */
                "deps": [
                    {
                        /* 依赖库目标的名称。
                           若这是重命名依赖，则为新名称。
                        */
                        "name": "bitflags",
                        /* 依赖的 Package ID。 */
                        "pkg": "https://github.com/rust-lang/crates.io-index#bitflags@1.0.4"
                        /* 依赖种类数组。Cargo 1.40 中添加。 */
                        "dep_kinds": [
                            {
                                /* 依赖种类。
                                   "dev"、"build"，或普通依赖为 null。
                                */
                                "kind": null,
                                /* 依赖的目标平台。
                                   非目标依赖时为 null。
                                */
                                "target": "cfg(windows)"
                            }
                        ]
                    }
                ],
                /* 此包上启用的特性数组。 */
                "features": [
                    "default"
                ]
            }
        ],
        /* 当前工作目录中的包（若未指定 --manifest-path）。
           虚拟工作空间时为 null。否则为包的 Package ID。
        */
        "root": "file:///path/to/my-package#0.1.0",
    },
    /* Cargo 放置输出的目标目录绝对路径。 */
    "target_directory": "/path/to/my-package/target",
    /* Cargo 放置中间构建产物的构建目录绝对路径。（不稳定） */
    "build_directory": "/path/to/my-package/build-dir",
    /* 此元数据结构的 schema 版本。
       若做出不兼容变更，此值会改变。
    */
    "version": 1,
    /* 工作空间根的绝对路径。 */
    "workspace_root": "/path/to/my-package"
    /* 工作空间元数据。
       未指定元数据时为 null。 */
    "metadata": {
        "docs": {
            "rs": {
                "all-features": true
            }
        }
    }
}
```

说明：

- 关于 `"id"` 字段语法，见参考文档中的[包 ID 规范]。

## 选项 {#options}
### 输出选项 {#output-options}
<dl>

<dt class="option-term" id="option-cargo-metadata---no-deps"><a class="option-anchor" href="#option-cargo-metadata---no-deps"><code>--no-deps</code></a></dt>
<dd class="option-desc"><p>仅输出工作空间成员的信息，不获取依赖。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---format-version"><a class="option-anchor" href="#option-cargo-metadata---format-version"><code>--format-version</code> <em>version</em></a></dt>
<dd class="option-desc"><p>指定要使用的输出格式版本。目前 <code>1</code> 是唯一可能的值。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---filter-platform"><a class="option-anchor" href="#option-cargo-metadata---filter-platform"><code>--filter-platform</code> <em>triple</em></a></dt>
<dd class="option-desc"><p>将 <code>resolve</code> 输出过滤为仅包含给定<a href="../../appendix/01-glossary.md#target">目标三元组</a>的依赖。可使用字面量 <code>"host-tuple"</code>，内部将替换为宿主目标。未使用此标志时，resolve 包含所有目标。</p>
<p>请注意，「packages」数组中列出的依赖仍包含所有依赖。每个包定义旨在完整再现 <code>Cargo.toml</code> 中的信息。</p>
</dd>


</dl>

### 特性选择 {#feature-selection}
特性标志用于控制启用哪些特性。若未指定特性选项，每个所选包都会激活 <code>default</code> 特性。

参见[特性文档](../../../cargo-reference/features/#command-line-feature-options)了解更多详情。

<dl>

<dt class="option-term" id="option-cargo-metadata--F"><a class="option-anchor" href="#option-cargo-metadata--F"><code>-F</code> <em>features</em></a></dt>
<dt class="option-term" id="option-cargo-metadata---features"><a class="option-anchor" href="#option-cargo-metadata---features"><code>--features</code> <em>features</em></a></dt>
<dd class="option-desc"><p>空格或逗号分隔的要激活的特性列表。工作空间成员的特性可用 <code>package-name/feature-name</code> 语法启用。此标志可指定多次，以启用所有指定的特性。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---all-features"><a class="option-anchor" href="#option-cargo-metadata---all-features"><code>--all-features</code></a></dt>
<dd class="option-desc"><p>激活所有所选包的全部可用特性。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---no-default-features"><a class="option-anchor" href="#option-cargo-metadata---no-default-features"><code>--no-default-features</code></a></dt>
<dd class="option-desc"><p>不激活所选包的 <code>default</code> 特性。</p>
</dd>


</dl>

### 显示选项 {#display-options}
<dl>
<dt class="option-term" id="option-cargo-metadata--v"><a class="option-anchor" href="#option-cargo-metadata--v"><code>-v</code></a></dt>
<dt class="option-term" id="option-cargo-metadata---verbose"><a class="option-anchor" href="#option-cargo-metadata---verbose"><code>--verbose</code></a></dt>
<dd class="option-desc"><p>使用详细输出。可指定两次以获得“非常详细”的输出，其中包含依赖警告与构建脚本输出等额外信息。也可通过 <code>term.verbose</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata--q"><a class="option-anchor" href="#option-cargo-metadata--q"><code>-q</code></a></dt>
<dt class="option-term" id="option-cargo-metadata---quiet"><a class="option-anchor" href="#option-cargo-metadata---quiet"><code>--quiet</code></a></dt>
<dd class="option-desc"><p>不打印 cargo 日志消息。也可通过 <code>term.quiet</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---color"><a class="option-anchor" href="#option-cargo-metadata---color"><code>--color</code> <em>when</em></a></dt>
<dd class="option-desc"><p>控制何时使用彩色输出。有效值：</p>
<ul>
<li><code>auto</code>（默认）：自动检测终端是否支持颜色。</li>
<li><code>always</code>：始终显示颜色。</li>
<li><code>never</code>：从不显示颜色。</li>
</ul>
<p>也可通过 <code>term.color</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>

</dl>

### 清单选项 {#manifest-options}
<dl>
<dt class="option-term" id="option-cargo-metadata---manifest-path"><a class="option-anchor" href="#option-cargo-metadata---manifest-path"><code>--manifest-path</code> <em>path</em></a></dt>
<dd class="option-desc"><p><code>Cargo.toml</code> 文件的路径。默认情况下，Cargo 在当前目录或任意父目录中搜索 <code>Cargo.toml</code> 文件。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---locked"><a class="option-anchor" href="#option-cargo-metadata---locked"><code>--locked</code></a></dt>
<dd class="option-desc"><p>断言使用的依赖与版本与最初生成现有 <code>Cargo.lock</code> 文件时完全相同。出现以下任一情况时 Cargo 将以错误退出：</p>
<ul>
<li>锁文件缺失。</li>
<li>Cargo 因不同的依赖解析而试图更改锁文件。</li>
</ul>
<p>可用于需要确定性构建的环境，例如 CI 流水线。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---offline"><a class="option-anchor" href="#option-cargo-metadata---offline"><code>--offline</code></a></dt>
<dd class="option-desc"><p>阻止 Cargo 以任何理由访问网络。若未指定此标志，当 Cargo 需要访问网络而网络不可用时会以错误停止。指定此标志后，Cargo 会在可能时尝试在无网络情况下继续。</p>
<p>请注意，这可能导致与在线模式不同的依赖解析。Cargo 会将自身限制为本地已下载的 crate，即便本地索引副本表明可能有更新版本。可先使用 <a href="../build-commands/07-cargo-fetch.md">cargo-fetch(1)</a> 命令下载依赖再离线。</p>
<p>也可通过 <code>net.offline</code> <a href="../../cargo-reference/06-configuration.md">配置值</a> 指定。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---frozen"><a class="option-anchor" href="#option-cargo-metadata---frozen"><code>--frozen</code></a></dt>
<dd class="option-desc"><p>等价于同时指定 <code>--locked</code> 与 <code>--offline</code>。</p>
</dd>


</dl>

### 通用选项 {#common-options}
<dl>

<dt class="option-term" id="option-cargo-metadata-+toolchain"><a class="option-anchor" href="#option-cargo-metadata-+toolchain"><code>+</code><em>toolchain</em></a></dt>
<dd class="option-desc"><p>若 Cargo 通过 rustup 安装，且传给 <code>cargo</code> 的第一个参数以 <code>+</code> 开头，则会被解释为 rustup 工具链名称（例如 <code>+stable</code> 或 <code>+nightly</code>）。关于工具链覆盖如何工作，见 <a href="https://rust-lang.github.io/rustup/overrides.html">rustup 文档</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata---config"><a class="option-anchor" href="#option-cargo-metadata---config"><code>--config</code> <em>KEY=VALUE</em> or <em>PATH</em></a></dt>
<dd class="option-desc"><p>覆盖 Cargo 配置值。参数应为 TOML 语法的 <code>KEY=VALUE</code>，或指向额外配置文件的路径。此标志可指定多次。更多信息见 <a href="../../cargo-reference/06-configuration.md#command-line-overrides">命令行覆盖一节</a>。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata--C"><a class="option-anchor" href="#option-cargo-metadata--C"><code>-C</code> <em>PATH</em></a></dt>
<dd class="option-desc"><p>在执行任何指定操作之前更改当前工作目录。这会影响 Cargo 默认查找项目清单（<code>Cargo.toml</code>）的位置，以及用于发现 <code>.cargo/config.toml</code> 的目录搜索等。此选项必须出现在命令名称之前，例如 <code>cargo -C path/to/my-project build</code>。</p>
<p>此选项仅在 <a href="https://doc.rust-lang.org/book/appendix-07-nightly-rust.html">nightly 通道</a> 上可用，且需要 <code>-Z unstable-options</code> 标志才能启用（见 <a href="https://github.com/rust-lang/cargo/issues/10098">#10098</a>）。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata--h"><a class="option-anchor" href="#option-cargo-metadata--h"><code>-h</code></a></dt>
<dt class="option-term" id="option-cargo-metadata---help"><a class="option-anchor" href="#option-cargo-metadata---help"><code>--help</code></a></dt>
<dd class="option-desc"><p>打印帮助信息。</p>
</dd>


<dt class="option-term" id="option-cargo-metadata--Z"><a class="option-anchor" href="#option-cargo-metadata--Z"><code>-Z</code> <em>flag</em></a></dt>
<dd class="option-desc"><p>Cargo 的不稳定（仅 nightly）标志。运行 <code>cargo -Z help</code> 查看详情。</p>
</dd>


</dl>

## 环境 {#environment}
关于 Cargo 读取的环境变量详情，见[参考文档](../../../cargo-reference/07-environment-variables/)。

## 退出状态 {#exit-status}
* `0`：Cargo 成功。
* `101`：Cargo 未能完成。

## 示例 {#examples}
1. 输出当前包的 JSON：

       cargo metadata --format-version=1

## 参见 {#see-also}
[cargo(1)](../../general-commands/01-cargo/), [cargo-pkgid(1)](../06-cargo-pkgid/), [包 ID 规范], [JSON 消息]

[包 ID 规范]: ../../../cargo-reference/10-package-id-specifications/
[JSON 消息]: ../../../cargo-reference/11-external-tools/#json-messages
