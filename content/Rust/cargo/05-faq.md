+++
title = "05-常见问题"
date = 2026-07-30T14:49:00+08:00
weight = 50
type = "docs"
description = "Cargo 常见问题解答"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 常见问题 {#frequently-asked-questions}


> 原文链接: [https://doc.rust-lang.org/cargo/faq.html](https://doc.rust-lang.org/cargo/faq.html)


## 计划使用 GitHub 作为包仓库吗？ {#is-the-plan-to-use-github-as-a-package-repository}
不会。Cargo 计划使用 [crates.io]，就像 npm 或 Rubygems 分别使用
[npmjs.com][1] 和 [rubygems.org][3] 一样。

我们计划永久支持将 git 仓库作为包的来源，
因为它们可用于早期开发与临时补丁，
即便人们以注册表作为包的主要来源时也是如此。

## 为什么要自建 crates.io，而不是用 GitHub 当注册表？ {#why-build-cratesio-rather-than-use-github-as-a-registry}
我们认为支持多种下载包的方式非常重要，
包括从 GitHub 下载，以及把包复制进你自己的包中。

话虽如此，我们认为 [crates.io] 提供了若干重要优势，
并且很可能成为人们通过 Cargo 下载包的主要方式。

作为先例，Node.js 的 [npm][1] 与 Ruby 的 [bundler][2] 都同时支持
中心注册表模型与基于 Git 的模型；在这些生态中，
大多数包通过注册表下载，同时也有重要的一小部分包使用基于 git 的包。

[1]: https://www.npmjs.com
[2]: https://bundler.io
[3]: https://rubygems.org

使中心注册表在其他语言中流行的一些优点包括：

* **可发现性**。中心注册表提供了查找现有包的便捷入口。
  再配合标签，注册表还能提供生态级别的信息，例如
  最受欢迎或被依赖最多的包列表。
* **速度**。中心注册表可以快速高效地只获取包的元数据，
  然后高效地下载已发布的包本身，而不是仓库里碰巧存在的其他冗余内容。
  这会显著提升依赖解析与获取的速度。随着依赖图扩大，
  下载全部 git 仓库会很快变慢。也请记住，并非人人都有高速、
  低延迟的互联网连接。

## Cargo 能与 C 代码（或其他语言）一起工作吗？ {#will-cargo-work-with-c-code-or-other-languages}
能！

Cargo 负责编译 Rust 代码，但我们知道许多 Rust 包会链接 C 代码。
我们也知道，围绕编译非 Rust 语言已积累了数十年的工具链。

我们的方案：Cargo 允许包在调用 `rustc` 之前[指定一个脚本](../cargo-reference/build-scripts/)
（用 Rust 编写）。借助 Rust 实现平台相关的配置，
并在各包之间抽取共用的构建功能。

## 能在 `make`（或 `ninja`，或其他工具）里使用 Cargo 吗？ {#can-cargo-be-used-inside-of-make-or-ninja-or}
当然可以。虽然我们希望 Cargo 能作为顶层独立编译 Rust 包的方式，
但我们知道有些人会想从其他构建工具中调用 Cargo。

我们从一开始就按这些场景设计 Cargo，关注诸如错误码与机器可读输出模式等细节。
这些方面仍有工作要做，但在传统脚本环境中使用 Cargo
是我们从一开始就设计并会持续优先考虑的目标。

## Cargo 是否支持多平台包或交叉编译？ {#does-cargo-handle-multi-platform-packages-or-cross-compilation}
Rust 本身提供了按平台配置代码段的机制。
Cargo 也支持[平台特定依赖][target-deps]，
我们还计划在未来于 `Cargo.toml` 中支持更多按平台的配置。

[target-deps]: ../cargo-reference/specifying-dependencies/#platform-specific-dependencies

从更长远看，我们正在探索如何用 Cargo 更方便地交叉编译包。

## Cargo 是否支持类似 `production` 或 `test` 的环境？ {#does-cargo-support-environments-like-production-or-test}
我们通过[配置文件（profiles）][profiles]支持环境相关行为，包括：

[profiles]: ../cargo-reference/05-profiles/

* 环境特定标志（例如开发用 `-g --opt-level=0`，
  生产用 `--opt-level=3`）。
* 环境特定依赖（例如测试断言用的 `hamcrest`）。
* 环境特定的 `#[cfg]`
* `cargo test` 命令

## Cargo 能在 Windows 上工作吗？ {#does-cargo-work-on-windows}
能！

提交到 Cargo 的所有变更都必须在 Windows 上通过本地测试套件。
若你在 Windows 上运行时遇到问题，我们会将其视为缺陷，因此请[提交 issue][cargo-issues]。

[cargo-issues]: https://github.com/rust-lang/cargo/issues

## 为什么要把 `Cargo.lock` 纳入版本控制？ {#why-have-cargolock-in-version-control}
虽然 [`cargo new`] 默认会跟踪版本控制中的 `Cargo.lock`，
是否这样做取决于你的包的需求。

`Cargo.lock` 锁文件的目的是描述一次成功构建时的世界状态。
Cargo 使用锁文件，在不同时间、不同系统上提供确定性构建，
确保使用的依赖与版本与最初生成 `Cargo.lock` 时完全相同。

确定性构建有助于：
- 运行 `git bisect` 定位缺陷根因
- 确保 CI 仅因新提交失败，而非外部因素
- 减少贡献者之间（或与 CI 之间）行为不一致带来的困惑

这份依赖快照在需要按一致依赖版本做验证时也很有用，例如：
- 验证最低支持的 Rust 版本（MSRV）低于某依赖最新版本所要求的版本
- 验证没有兼容性保证的人类可读输出（例如对错误信息进行快照测试，
  以确保它们“可理解”——这类指标过于模糊，难以自动化）

不过，这种确定性可能带来虚假的安全感，因为
`Cargo.lock` 不影响你包的消费者，只有 `Cargo.toml` 会。
例如：
- [`cargo install`] 会选择最新依赖，除非传入
[`--locked`](../cargo-commands/general-commands/01-cargo/#option-cargo---locked)。
- 新依赖（例如用 [`cargo add`] 添加的）会被锁定到最新版本

锁文件也可能成为合并冲突的来源。

关于通过 CI 验证更新依赖版本的策略，
见[验证最新依赖](../cargo-guide/08-continuous-integration/#verifying-latest-dependencies)。

[`cargo new`]: ../cargo-commands/package-commands/03-cargo-new/
[`cargo add`]: ../cargo-commands/manifest-commands/01-cargo-add/
[`cargo install`]: ../cargo-commands/package-commands/02-cargo-install/

## 库能否用 `*` 作为依赖版本？ {#can-libraries-use-as-a-version-for-their-dependencies}
**自 2016 年 1 月 22 日起，[crates.io] 会拒绝所有带有通配符依赖约束的包
（不仅是库）。**

严格来说库*可以*这么做，但不应该。版本需求 `*` 表示
“这能与曾经存在的每个版本一起工作”，而这永远不会成立。
库应始终给出它们确实可用的版本范围，
哪怕只是像“每一个 1.x.y 版本”这样宽泛的范围。

## 为什么叫 `Cargo.toml`？ {#why-cargotoml}
作为与 Cargo 最频繁交互的文件之一，配置文件为何叫 `Cargo.toml`
这个问题时不时会出现。开头的大写 `C` 是为了在目录列表中
把清单与其他类似配置文件归在一起。文件排序常把大写字母排在小写之前，
从而让 `Makefile` 与 `Cargo.toml` 这类文件相邻。尾缀 `.toml` 则用来强调
该文件采用 [TOML 配置格式](https://toml.io/)。

Cargo 不允许使用 `cargo.toml` 或 `Cargofile` 等其他名称，
以强调识别 Cargo 仓库的简便性。历史上若允许许多可能的名字，
会导致只处理了一种大小写/拼写、却意外遗漏其他情况的混淆。

[crates.io]: https://crates.io/

## Cargo 如何离线工作？ {#how-can-cargo-work-offline}
[`--offline`](../cargo-commands/general-commands/01-cargo/#option-cargo---offline) 或
 [`--frozen`](../cargo-commands/general-commands/01-cargo/#option-cargo---frozen) 标志告诉 Cargo 不要
 访问网络。若本应访问网络，则会返回错误。
你可以在一个项目中使用 [`cargo fetch`] 先下载依赖，再离线，
然后在另一个项目中使用相同依赖。也可通过 [配置值][offline config]
在 Cargo 配置中设置。



供应商化（vendoring）也与此相关，更多信息见[源替换][replace]文档。

[replace]: ../cargo-reference/specifying-dependencies/02-source-replacement/
[`cargo fetch`]: ../cargo-commands/build-commands/07-cargo-fetch/
[offline config]: ../cargo-reference/06-configuration/#netoffline

## 为什么 Cargo 在重新构建我的代码？ {#why-is-cargo-rebuilding-my-code}
Cargo 负责对项目中的 crate 做增量编译。这意味着如果你连续输入两次
`cargo build`，第二次通常不应重新构建 crates.io 依赖。尽管如此，缺陷仍可能出现，
Cargo 有时会在你未预期时重新构建代码！

我们长期以来[希望提供更好的相关诊断](https://github.com/rust-lang/cargo/issues/2904)，
但很遗憾在这个问题上进展有限。与此同时，
你至少可以通过设置 `CARGO_LOG` 环境变量来调试重建：

```sh
$ CARGO_LOG=cargo::compiler::fingerprint=info cargo build
```

这会让 Cargo 打印大量关于诊断与重建的信息。其中往往包含为何项目被重建的线索，
尽管你通常需要自己把点连起来，因为这些输出目前还不太好读。注意：需要在你认为
*不应*重建却发生了重建的那条命令上设置 `CARGO_LOG`。可惜 Cargo 目前还无法事后调试
“刚才为什么重建了？”

历史上我们见过的一些会导致 crate 被重建的问题包括：

* 构建脚本打印 `cargo::rerun-if-changed=foo`，而 `foo` 是一个不存在、
  也没有任何东西生成它的文件。此时 Cargo 会一直运行构建脚本，以为它会生成该文件，
  但永远不会。修复方法是在这种场景下避免打印 `rerun-if-changed`。

* 两次连续的 Cargo 构建可能对某些依赖启用了不同的特性集。例如第一次命令构建整个
  工作空间，第二次只构建一个 crate，可能导致 crates.io 依赖启用了不同的特性集，
  从而使其以及依赖它的一切被重建。对此目前没有很好的通用修复，不过若可能，
  最好让某个 crate 上启用的特性集保持恒定，而不论你在工作空间中构建什么。

* 某些文件系统在时间戳方面行为异常。Cargo 主要使用文件时间戳来决定是否需要重建，
  若你使用非标准文件系统，可能以某种方式影响时间戳（例如截断、漂移等）。
  在这种情况下，欢迎提交 issue，我们可以看看能否适配该文件系统。

* 并发的构建过程正在删除产物或修改文件。有时你可能有后台进程在尝试构建或检查项目。
  这些后台进程可能出人意料地删除一些构建产物或触碰文件（也可能只是意外），
  从而导致看似无谓的重建！最好的修复是管束后台进程，避免与你的工作冲突。

若在尝试调试后仍有问题，欢迎[提交 issue](https://github.com/rust-lang/cargo/issues/new)！

## “版本冲突”是什么意思，如何解决？ {#what-does-version-conflict-mean-and-how-to-resolve-it}
> failed to select a version for `x` which could resolve this conflict

你见过上面的错误信息吗？

这是 Cargo 用户最恼人的错误信息之一。有多种情况可能导致版本冲突。下面我们梳理可能原因，
并提供诊断技巧帮你排查：

- 项目及其依赖使用 [links] 重复链接本地库。Cargo 禁止链接两个带有相同原生库的包，
  因此即便隔着多层依赖也不允许。此时错误信息会提示：
  `Only one package in the dependency graph may specify the same links value`，
  你可能需要手动检查并删除重复的 link 值。社区也有[既有约定][conventions in place]来缓解此问题。

- 当项目依赖不同 crate，而这些 crate 使用同一依赖库，但版本被限制到无法确定正确版本时，
  也会导致冲突。错误信息会提示：
  `all possible versions conflict with previously selected packages`。
  你可能需要修改版本需求，使其一致。

- 若项目中存在多版本依赖，在使用 [`direct-minimal-versions`] 时无法满足最低版本需求，
  也会导致冲突。你可能需要相应修改直接依赖的版本需求，以满足最低 SemVer 版本。

- 若依赖的 crate 没有你选择的特性，也会导致冲突。此时需要检查依赖版本及其特性。

- 合并分支或 PR 时也可能发生冲突；若有非平凡冲突，可以重置所有“你的”变更，
  先修好分支中的其他冲突，然后运行某些 cargo 命令（如 `cargo tree` 或 `cargo check`），
  这通常会用你自己的本地变更重新更新锁文件。若你之前在分支上运行过一些
  `cargo update` 命令，可以再运行一遍。社区一直在寻找用[自定义合并工具]
  解决 `Cargo.lock` 与 `Cargo.toml` 合并冲突的方案。


[links]: ../cargo-reference/specifying-dependencies/03-dependency-resolution/#links
[conventions in place]: ../cargo-reference/build-scripts/#-sys-packages
[`direct-minimal-versions`]: https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#direct-minimal-versions
[custom merge tool]: https://github.com/rust-lang/cargo/issues/1818

## 为什么我的构建占用这么多空间？ {#why-does-my-build-take-up-so-much-space}
Cargo 用磁盘空间换取更快构建，包括：
- 维护中间构建产物的[缓存][cache]，以便在修改一个包时避免全部重建
- 为不同工具链版本、包版本、特性等组合维护不同的[缓存][cache]条目，
  以便在配置间来回切换时避免重建包
- 为本地包启用[增量编译]，以便更快地重建发生变化的包
- 在 [`dev` 配置文件][`dev` profile]中启用 [debuginfo]，以便你使用调试器

[incremental compilation]: ../cargo-reference/05-profiles/#incremental
[debuginfo]: ../cargo-reference/05-profiles/#debug
[`dev` profile]: ../cargo-reference/05-profiles/#dev
[cache]: ../cargo-reference/09-build-cache/
