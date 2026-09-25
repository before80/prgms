+++
title = "2 iOS"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/sign/ios/](https://tauri.app/distribute/sign/ios/)

在 iOS 上进行代码签名，是通过官方 [Apple App Store](https://www.apple.com/app-store/) 或欧盟可能的替代市场分发应用所必需的，一般来说也是在终端用户设备上安装并执行所必需的。

## 前置条件

iOS 的代码签名需要注册 [Apple Developer](https://developer.apple.com) 计划，撰写本文时费用为每年 99 美元。
你还需要一台用于执行代码签名的 Apple 设备。这是签名流程和 Apple 条款与条件所要求的。

要分发 iOS 应用，你必须在 App Store Connect 中注册你的 bundle 标识符、
拥有合适的 iOS 代码签名证书，以及一个把两者关联起来并启用应用所用 iOS 能力的移动端描述文件（provisioning profile）。
这些要求既可以由 Xcode 自动管理，也可以手动提供。

## 自动签名

让 Xcode 管理应用的签名与描述文件，是把 iOS 应用导出以进行分发最方便的方式。
它会自动注册你的 bundle 标识符、管理 iOS 能力变更，并根据你的导出方式配置合适的证书。

自动签名默认启用，在本地机器上使用时会用 Xcode 中配置的账号进行认证。\
要注册账号，请打开 Xcode 应用，在 `Xcode > Settings` 菜单中打开设置页，切换到 Accounts 标签并点击 `+` 图标。

要在 CI/CD 平台使用自动签名，你必须创建一个 App Store Connect API 密钥，
并定义 `APPLE_API_ISSUER`、`APPLE_API_KEY` 和 `APPLE_API_KEY_PATH` 环境变量。\
打开 [App Store Connect 的 Users and Access 页面](https://appstoreconnect.apple.com/access/users)，选择 Integrations 标签，点击 Add 按钮，选择名称与 Admin 权限。
`APPLE_API_ISSUER`（Issuer ID）显示在密钥表格上方，`APPLE_API_KEY` 是该表格 Key ID 列中的值。
你还需要下载私钥，这只能做一次，并且只在页面重新加载后可见（按钮显示在新建密钥所在表格行上）。
私钥文件路径必须通过 `APPLE_API_KEY_PATH` 环境变量设置。

## 手动签名

要手动为 iOS 应用签名，你可以通过环境变量提供证书和移动端描述文件：

- **IOS_CERTIFICATE**：从钥匙串导出的证书的 base64 表示。
- **IOS_CERTIFICATE_PASSWORD**：从钥匙串导出该证书时设置的密码。
- **IOS_MOBILE_PROVISION**：描述文件的 base64 表示。

下面几节说明如何获取这些值。

### 签名证书

注册之后，前往 [Certificates](https://developer.apple.com/account/resources/certificates/list) 页面创建一个新的 Apple Distribution 证书。
下载新证书并把它安装到 macOS 钥匙串。

要导出证书密钥，请打开 “Keychain Access” 应用，展开该证书条目，
右键点击密钥项并选择 “Export \<key-name\>” 项。
选择导出的 .p12 文件路径并记住它的密码。

运行以下 `base64` 命令把证书转换为 base64 并复制到剪贴板：

```
base64 -i <path-to-certificate.p12> | pbcopy
```

剪贴板中的值现在就是签名证书的 base64 表示。
保存它并作为 `IOS_CERTIFICATE` 环境变量的值使用。

证书密码必须设置到 `IOS_CERTIFICATE_PASSWORD` 变量。

{{% alert title="选择合适的证书类型" %}}
你必须为每种导出方式使用合适的证书类型：

- **debugging**：Apple Development 或 iOS App Development
- **app-store-connect**：Apple Distribution 或 iOS Distribution（App Store Connect 与 Ad Hoc）
- **ad-hoc**：Apple Distribution 或 iOS Distribution（App Store Connect 与 Ad Hoc）

{{% /alert %}}

### 描述文件

此外，你必须为你的应用提供描述文件。
在 [Identifiers](https://developer.apple.com/account/resources/identifiers/list) 页面中，
创建一个新的 App ID，并确保它的 “Bundle ID” 值与 [`identifier`](https://tauri.app/reference/config/#identifier) 配置中设置的标识符一致。

前往 [Profiles](https://developer.apple.com/account/resources/profiles/list) 页面创建一个新的描述文件。
对于 App Store 分发，它必须是 “App Store Connect” 描述文件。
选择恰当的 App ID，并关联你之前创建的证书。

创建描述文件之后，下载它并运行以下 `base64` 命令转换该描述文件并复制到剪贴板：

```
base64 -i <path-to-profile.mobileprovision> | pbcopy
```

剪贴板中的值现在就是描述文件的 base64 表示。
保存它并作为 `IOS_MOBILE_PROVISION` 环境变量的值使用。

现在你就可以构建 iOS 应用并分发到 App Store 了！
