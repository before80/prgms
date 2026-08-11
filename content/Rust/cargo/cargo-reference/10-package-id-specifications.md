+++
title = "10-包 ID 规范"
date = 2026-07-30T14:49:00+08:00
weight = 47
type = "docs"
description = "Package ID Specification（SPEC）语法"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 包 ID 规范 {#package-id-specifications}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/pkgid-spec.html](https://doc.rust-lang.org/cargo/reference/pkgid-spec.html)


## 包 ID 规范 {#package-id-specifications}
Cargo 的子命令经常需要在依赖图中引用某个特定包，以执行更新、清理、构建等操作。为解决此问题，Cargo 支持 *包 ID 规范（Package ID Specifications）*。规范是一个字符串，用于在包图中唯一地引用某一个包。

规范可以是完全限定的，例如 `registry+https://github.com/rust-lang/crates.io-index#regex@1.4.3`，也可以是缩写形式，例如 `regex`。只要缩写形式能在依赖图中唯一标识一个包，就可以使用。若存在歧义，可添加额外限定符使其唯一。例如，若图中有两个版本的 `regex` 包，则可用版本加以限定，如 `regex@1.4.3`。

Cargo 输出的包 ID 规范（例如在 [cargo metadata](../../cargo-commands/manifest-commands/05-cargo-metadata/) 的输出中）是完全限定的。

### 规范语法 {#specification-grammar}
包 ID 规范的形式语法为：

```notrust
spec := pkgname |
        [ kind "+" ] proto "://" hostname-and-path [ "?" query] [ "#" ( pkgname | semver ) ]
query = ( "branch" | "tag" | "rev" ) "=" ref
pkgname := name [ ("@" | ":" ) semver ]
semver := digits [ "." digits [ "." digits [ "-" prerelease ] [ "+" build ]]]

kind = "registry" | "git" | "path"
proto := "http" | "git" | "file" | ...
```

此处方括号表示内容可选。

URL 形式可用于 git 依赖，或用于区分来自不同源（例如不同注册表）的包。

### 规范示例 {#example-specifications}
以下是对 `crates.io` 上 `regex` 包的引用：

| 规范                                                              | 名称    | 版本 |
|:------------------------------------------------------------------|:-------:|:-------:|
| `regex`                                                           | `regex` | `*`     |
| `regex@1.4`                                                       | `regex` | `1.4.*` |
| `regex@1.4.3`                                                     | `regex` | `1.4.3` |
| `https://github.com/rust-lang/crates.io-index#regex`              | `regex` | `*`     |
| `https://github.com/rust-lang/crates.io-index#regex@1.4.3`        | `regex` | `1.4.3` |
| `registry+https://github.com/rust-lang/crates.io-index#regex@1.4.3` | `regex` | `1.4.3` |

以下是若干不同 git 依赖的规范示例：

| 规范                                                       | 名称             | 版本  |
|:-----------------------------------------------------------|:----------------:|:--------:|
| `https://github.com/rust-lang/cargo#0.52.0`                | `cargo`          | `0.52.0` |
| `https://github.com/rust-lang/cargo#cargo-platform@0.1.2`  | <nobr>`cargo-platform`</nobr> | `0.1.2`  |
| `ssh://git@github.com/rust-lang/regex.git#regex@1.4.3`     | `regex`          | `1.4.3`  |
| `git+ssh://git@github.com/rust-lang/regex.git#regex@1.4.3` | `regex`          | `1.4.3`  |
| `git+ssh://git@github.com/rust-lang/regex.git?branch=dev#regex@1.4.3` | `regex`          | `1.4.3`  |

文件系统上的本地包可使用 `file://` URL 引用：

| 规范                                        | 名称  | 版本 |
|:--------------------------------------------|:-----:|:-------:|
| `file:///path/to/my/project/foo`            | `foo` | `*`     |
| `file:///path/to/my/project/foo#1.1.8`      | `foo` | `1.1.8` |
| `path+file:///path/to/my/project/foo#1.1.8` | `foo` | `1.1.8` |

### 规范的简洁性 {#brevity-of-specifications}
其目标是同时支持简洁与完备的语法，以便在依赖图中引用包。有歧义的引用可能对应一个或多个包。若同一规范可能引用多个包，大多数命令会报错。
