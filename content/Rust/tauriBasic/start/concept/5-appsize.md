+++
title = "5 应用体积"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/concept/size/](https://tauri.app/concept/size/)

Tauri 默认就能生成非常小的二进制文件，不过再压一压也无妨。下面是一些达到最优效果的技巧与诀窍。

## Cargo 配置

对你的项目来说，最简单且与前端无关的体积优化之一，就是添加一个 Cargo profile。

根据你使用的是稳定版还是 nightly 版 Rust 工具链，可用的选项会略有不同。除非你是高级用户，否则建议坚持使用稳定版工具链。

**工具链**

{{< tabpane text=true persist=disabled >}}
{{% tab header="稳定版" %}}

```toml
[profile.dev]
incremental = true # 以更小的步骤编译二进制文件。

[profile.release]
codegen-units = 1 # 让 LLVM 可以做更好的优化。
lto = true # 启用链接时优化。
opt-level = "s" # 优先考虑较小的二进制体积。若更看重速度可使用 `3`。
panic = "abort" # 通过禁用 panic 处理获得更高性能。
strip = true # 确保移除调试符号。
```

{{% /tab %}}

{{% tab header="Nightly" %}}

```toml
[profile.dev]
incremental = true # 以更小的步骤编译二进制文件。
rustflags = ["-Zthreads=8"] # 更好的编译性能。

[profile.release]
codegen-units = 1 # 让 LLVM 可以做更好的优化。
lto = true # 启用链接时优化。
opt-level = "s" # 优先考虑较小的二进制体积。若更看重速度可使用 `3`。
panic = "abort" # 通过禁用 panic 处理获得更高性能。
strip = true # 确保移除调试符号。
trim-paths = "all" # 从二进制文件中移除可能敏感的信息。
rustflags = ["-Cdebuginfo=0", "-Zthreads=8"] # 更好的编译性能。
```

{{% /tab %}}

{{< /tabpane >}}
### 参考

{{% alert title="注意" %}}
这并不是所有可用选项的完整参考，只是我们想特别提醒你关注的几项。
{{% /alert %}}

- [incremental：](https://doc.rust-lang.org/cargo/reference/profiles.html#incremental)以更小的步骤编译二进制文件。
- [codegen-units：](https://doc.rust-lang.org/cargo/reference/profiles.html#codegen-units)以牺牲编译期优化为代价加快编译速度。
- [lto：](https://doc.rust-lang.org/cargo/reference/profiles.html#lto)启用链接时优化。
- [opt-level：](https://doc.rust-lang.org/cargo/reference/profiles.html#opt-level)决定编译器的侧重方向。用 `3` 优化性能，用 `z` 优化体积，`s` 则介于两者之间。
- [panic：](https://doc.rust-lang.org/cargo/reference/profiles.html#panic)通过移除 panic 展开来减小体积。
- [strip：](https://doc.rust-lang.org/cargo/reference/profiles.html#strip)从二进制文件中剥除符号或调试信息。
- [rpath：](https://doc.rust-lang.org/cargo/reference/profiles.html#rpath)通过把信息硬编码进二进制文件，帮助找到它所需的动态库。
- [trim-paths：](https://rust-lang.github.io/rfcs/3127-trim-paths.html)从二进制文件中移除可能敏感的信息。
- [rustflags：](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#profile-rustflags-option)按 profile 分别设置 Rust 编译器标志。
  - `-Cdebuginfo=0`：构建中是否应包含调试信息符号。
  - `-Zthreads=8`：增加编译期间使用的线程数。

## 移除未使用的命令

在 Pull Request [`feat: add a new option to remove unused commands`](https://github.com/tauri-apps/tauri/pull/12890) 中，我们在 tauri 配置文件里新增了一个选项：

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

它用于移除在你的能力（capability）文件（ACL）中从未被允许的命令，这样你就不必为用不到的东西付出代价。

{{% alert title="提示" %}}
要让这个选项收益最大化，请在 ACL 中只包含你实际使用的命令，而不要使用 `defaults`。
{{% /alert %}}

{{% alert title="注意" %}}
此特性需要 `tauri@2.4`、`tauri-build@2.1`、`tauri-plugin@2.1` 和 `tauri-cli@2.4`。
{{% /alert %}}

{{% alert title="注意" %}}
它不会考虑运行时动态添加的 ACL，所以在使用这一选项时请务必留意这一点。
{{% /alert %}}

<details>
<summary>它在底层是如何工作的？</summary>
`tauri-cli` 会通过一个环境变量与 `tauri-build` 以及 `tauri`、`tauri-plugin` 的构建脚本通信，让它们从 ACL 生成一份允许命令的列表。
随后 `generate_handler` 宏会据此移除未使用的命令。

一个内部细节是：这个环境变量目前名为 `REMOVE_UNUSED_COMMANDS`，其值被设为项目目录（通常是 `src-tauri` 目录），构建脚本借此找到能力（capability）文件。虽然不推荐，但如果你无法或不想使用 `tauri-cli`，也可以自己设置这个环境变量来让它工作
（**请注意，由于这是实现细节，我们不保证它的稳定性**）。

</details>
