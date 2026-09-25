+++
title = "8 更新依赖"
date = 2026-09-25T21:31:08+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/updating-dependencies/](https://tauri.app/develop/updating-dependencies/)

## 更新 npm 包

如果你使用 `tauri` 包：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @tauri-apps/cli@latest @tauri-apps/api@latest
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn up @tauri-apps/cli @tauri-apps/api
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm update @tauri-apps/cli @tauri-apps/api --latest
```

{{% /tab %}}

{{< /tabpane >}}
你也可以在命令行中查看 Tauri 的最新版本：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm outdated @tauri-apps/cli
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn outdated @tauri-apps/cli
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm outdated @tauri-apps/cli
```

{{% /tab %}}

{{< /tabpane >}}
## 更新 Cargo 包

你可以用 [`cargo outdated`](https://github.com/kbknapp/cargo-outdated) 检查过时的包，或者查看 crates.io 页面：[tauri](https://crates.io/crates/tauri/versions) / [tauri-build](https://crates.io/crates/tauri-build/versions)。

进入 `src-tauri/Cargo.toml`，把 `tauri` 和 `tauri-build` 改为

```toml
tauri-build = "%version%"

[dependencies]
tauri = { version = "%version%" }
```

其中 `%version%` 是上面看到的对应版本号。

然后执行以下操作：

```shell
cargo update
```

或者，你也可以运行 [cargo-edit](https://github.com/killercup/cargo-edit) 提供的 `cargo upgrade` 命令，它会自动完成这一切。

## 同步 npm 包与 Cargo crate 版本

由于 JavaScript API 依赖后端的 Rust 代码，新增功能需要同时升级两侧以保证兼容性。请确保 npm 包 `@tauri-apps/api` 与 cargo crate `tauri` 处于相同的次要版本。

对于插件，我们可能会在补丁版本中引入这类变更，因此我们会同时提升 npm 包和 cargo crate 的版本，你需要保持精确版本同步。例如，npm 包 `@tauri-apps/plugin-fs` 与 cargo crate `tauri-plugin-fs` 需要相同版本（例如 `2.2.1`）。
