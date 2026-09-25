+++
title = "5 资源协议作用域"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/asset-protocol/](https://tauri.app/security/asset-protocol/)

Tauri 可以通过 **asset** 自定义协议把磁盘文件提供给 WebView（例如当你在前端使用 [`convertFileSrc`](https://tauri.app/reference/javascript/api/namespacecore/#convertfilesrc) 时）。某个路径是否被允许由 `tauri.conf.json` 中的 **`app.security.assetProtocol`** 控制。

你必须把 **`enable`** 设为 `true`，并定义一个 **`scope`**，列出允许暴露的文件系统路径。运行时解析出的路径必须匹配该作用域，否则 WebView 会拒绝加载（通常伴随类似 “asset protocol not configured to allow the path” 的错误）。

针对 `asset:` 来源的内容安全策略记录在[内容安全策略（CSP）](../6-csp/)页面。本页聚焦于**作用域**，以及它与 glob 和隐藏路径段的交互方式。

## `scope` 是如何定义的

`assetProtocol.scope` 与其它地方与文件系统相关的配置使用同一个 **`FsScope`** 类型：要么是允许的 glob 模式组成的 **JSON 数组**，要么是一个包含 `allow`、可选 `deny` 和可选 `requireLiteralLeadingDot` 的 **JSON 对象**。关于“作用域”在 Tauri 安全模型中更宏观的定位，请参阅[命令作用域](../3-scope/)。

模式可以以**基础目录变量**开头（例如 `$HOME`、`$CACHE`、`$APPCACHE`、`$APPDATA`、`$RESOURCE`）。你的应用可以依赖的全部变量见[路径／基础目录 API](https://tauri.app/reference/javascript/api/namespacepath/#basedirectory)。

加载资源时解析出的路径通常是**绝对路径**（在 Linux 上往往位于 `/home/...` 之下）。像 `["*/**"]` 这样的模式通常**不会**匹配这些路径，因为它与开头的 `/` 或基础目录变量对不上。请优先使用 `$HOME/**/*`、`/home/username/**/*` 之类的模式，或其它与解析后路径相符的形式。

### 数组形式（只允许路径）

当你只需要一份固定的允许清单，且默认的 glob 行为已足够时，使用列表：

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": ["$APPCACHE/**/*", "$RESOURCE/**/*"]
      }
    }
  }
}
```

使用数组形式时你**无法**设置 `requireLiteralLeadingDot`；那需要下面的对象形式。

### 对象形式（`allow`、`deny`、`requireLiteralLeadingDot`）

当你需要 **deny** 规则，或想改变**前导点**的匹配方式时，使用对象形式：

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": {
          "allow": ["$APPCACHE/**/*"],
          "deny": ["$APPCACHE/**/secrets/**"]
        }
      }
    }
  }
}
```

当 `allow` 与 `deny` 都匹配时，`deny` 优先。

## Unix：以 `.` 开头的路径段

在 Unix 上，`requireLiteralLeadingDot` 默认为 **`true`**。此时 `*`、`?`、`**` 和 `[...]` 之类的通配符**不会匹配以** `.` 开头的路径组件（也就是 `.cache`、`.ssh` 这类点文件和点目录）。

因此像 `$HOME/**` 这样的模式可以允许 `/home/user/Documents/file.png`，但**不会**允许 `/home/user/.cache/myapp/preview.png`，因为 `.cache` 是点开头的组件。字面写出该段的模式（例如 `$HOME/.cache/myapp/**`）则**可以**匹配。

若要在宽泛的 glob 下允许点开头的组件，你可以在**对象**形式的 `scope` 中把 **`requireLiteralLeadingDot`** 设为 **`false`**（这会放宽 WebView 能加载的内容，请仔细评估）：

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": {
          "requireLiteralLeadingDot": false,
          "allow": ["$HOME/**/*"]
        }
      }
    }
  }
}
```

{{% alert title="在 Linux 风格路径上仍然被阻止？" %}}

社区成员常常在路径经过**点目录**（例如 `~/.cache/...`）时遇到这种情况，而允许模式只用了 `$HOME` 下的 `**`。具体示例和修复办法见 [tauri#13788](https://github.com/tauri-apps/tauri/issues/13788) 中的讨论。

{{% /alert %}}

## “此处之下所有文件”请优先用 `**/*` 而不是裸 `**`

对于应当匹配某个目录树下**文件**的 glob，请优先使用 `**/*`（以及 `$DIR/**/*` 之类的变体），而不是裸 `**`，这与 Tauri 其它路径示例保持一致。当你想要“递归包含此目录下的所有内容”时，裸 `**` 很容易被误用。

## 高度宽松的配置（务必极其谨慎）

如果你确实需要最宽泛的访问权限**并且**需要点开头的路径段，维护者建议的形式如下。**这不是默认推荐**；它会增加隐藏文件和敏感文件的暴露风险。

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": {
          "requireLiteralLeadingDot": false,
          "allow": ["**/*"]
        }
      }
    }
  }
}
```

{{% alert title="警告" color="warning" %}}

请优先使用**更窄**的目录（`$APPCACHE`、`$RESOURCE`、`$HOME` 下的单个应用子文件夹等），而不是宽泛的 `$HOME/**/*` 或 `**/*`，除非你有充分的理由并且理解其中的安全取舍。

{{% /alert %}}

## 静态配置与动态选择的路径

**`tauri.conf.json`** 中的条目描述的是**静态**允许／拒绝模式。它们不能替代用户在运行时选择任意文件夹或文件的工作流（例如使用 **dialog** 插件）：这些路径可能需要用 [**persisted-scope**](../../plugin/20-persistedscope/) 插件在重启后**持久化**。

要用该插件持久化**资源**／协议相关的作用域，请在 `src-tauri/Cargo.toml` 中启用它的 **`protocol-asset`** Cargo 特性，例如：

```toml
tauri-plugin-persisted-scope = { version = "2", features = ["protocol-asset"] }
```

请按插件指南所述，在 **`tauri_plugin_persisted_scope`** 之前注册 **`tauri_plugin_fs`**。

## 故障排除

| 现象                                                             | 需要检查的内容                                                                                                                                                                                                                                |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| “asset protocol not configured to allow the path”                   | 路径必须匹配某个 **`allow`** 模式；**`deny`** 会覆盖 **`allow`**。请使用**绝对**模式，或使用与磁盘上路径解析方式一致的 **`$VAR`/`$HOME`** 风格变量。                                                         |
| 普通文件夹可以，但 **`.cache`** / **`.config`** 下不行 | 这是 Unix 上 **`requireLiteralLeadingDot`** 的默认行为：在模式中字面写出 `.segment`，或在对象 `scope` 中把 **`requireLiteralLeadingDot`** 设为 **`false`**（见 [tauri#13788](https://github.com/tauri-apps/tauri/issues/13788)）。 |
| 用户在运行时选择了文件夹；重启后仍被阻止        | 你可能需要带 **`protocol-asset`** 特性的 [**persisted-scope**](../../plugin/20-persistedscope/)，而不仅是 `tauri.conf.json` 中的条目。                                                                                                        |
| 宽泛的 `**` 似乎不对                                              | 面向文件的 glob 请尝试 `**/*`；关于打包资源中类似的 `**` 与 `**/*` 指南，请参阅[嵌入附加文件](../../develop/6-resources/)。                                                                                           |
| 形如 `["*/**"]` 的作用域在 Linux 上从不匹配                        | 解析出的路径是**绝对路径**；请使用 **`$...` 变量**、开头的 **`/`**，或其它能匹配真实路径的模式（见上文）。                                                                                                       |

`assetProtocol` 和 `FsScope` 的权威 Rust 类型位于 Tauri 的 [`config.rs`](https://github.com/tauri-apps/tauri/blob/dev/crates/tauri-utils/src/config.rs)（`AssetProtocolConfig`、`FsScope`）。生成的[配置参考](https://tauri.app/reference/config/)可能会以紧凑或难以阅读的方式渲染嵌套的 `FsScope` 字段；如果那里有不清楚的地方，请与本页以及[文件系统插件](../../plugin/9-filesystem/)的 `requireLiteralLeadingDot` 部分交叉核对（插件配置对自身作用域使用相同的选项名）。如果参考文档仍未清晰记录这些字段，可以考虑在 **tauri-docs** 仓库提 issue，以便改进配置生成器。
