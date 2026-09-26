+++
title = "3 App Store"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/app-store/](https://tauri.app/distribute/app-store/)

[Apple App Store](https://www.apple.com/store) 是 Apple 维护的应用市场。
你可以通过该 App Store 分发面向 macOS 和 iOS 的 Tauri 应用。

本指南只涵盖把应用直接分发到 App Store 的细节。
关于 macOS 分发选项与配置的更多信息，请参阅通用的 [App Bundle 分发指南](../10-macosapplicationbundle/)。

## 要求

分发 iOS 和 macOS 应用需要注册 [Apple Developer](https://developer.apple.com) 计划。

此外，你还必须为 [macOS](../sign/1-macos/) 和 [iOS](../sign/2-ios/) 设置代码签名。

## 更换应用图标

运行 `tauri ios init` 设置好 Xcode 项目之后，你可以使用 `tauri icon` 命令更新应用图标。

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri icon /path/to/app-icon.png -- --ios-color '#fff'
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri icon /path/to/app-icon.png --ios-color '#fff'
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri icon /path/to/app-icon.png --ios-color '#fff'
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri icon /path/to/app-icon.png --ios-color '#fff'
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri icon /path/to/app-icon.png --ios-color '#fff'
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri icon /path/to/app-icon.png --ios-color '#fff'
```

{{% /tab %}}

{{< /tabpane >}}

`--ios-color` 参数定义 iOS 图标的背景色。

## 配置

注册 Apple Developer 计划之后，在 App Store 中分发 Tauri 应用的第一步
是在 [App Store Connect](https://appstoreconnect.apple.com/apps) 中注册你的应用。

{{% alert title="注意" %}}
_Bundle ID_ 字段中提供的值**必须**与 [`tauri.conf.json > identifier`](https://tauri.app/reference/config/#identifier) 中定义的标识符一致。
{{% /alert %}}

## 构建与上传

Tauri CLI 可以为 macOS 和 iOS 打包你的应用。必须在 macOS 机器上运行。

Tauri 会从 [`tauri.conf.json > version`](https://tauri.app/reference/config/#version) 中定义的值推导 [`CFBundleVersion`](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleversion)。
如果你需要不同的 bundle 版本方案（例如顺序编号），可以在 [`tauri.conf.json > bundle > iOS > bundleVersion`](https://tauri.app/reference/config/#bundleversion-1) 或 [`tauri.conf.json > bundle > macOS > bundleVersion`](https://tauri.app/reference/config/#bundleversion) 配置中设置自定义 bundle 版本：

```json
{
  "bundle": {
    "iOS": {
      "bundleVersion": "100"
    }
  }
}
```

{{% alert title="警告" color="warning" %}}
代码签名是必需的。请参阅 [macOS](../sign/1-macos/) 和 [iOS](../sign/2-ios/) 的文档。
{{% /alert %}}

注意 Tauri 为 iOS 应用借助了 Xcode，因此你也可以用 Xcode 归档并分发 iOS 应用，而不使用 Tauri CLI。
要在 Xcode 中打开 iOS 项目以进行构建，你必须运行以下命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri ios build -- --open
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri ios build --open
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri ios build --open
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri ios build --open
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri ios build --open
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri ios build --open
```

{{% /tab %}}

{{< /tabpane >}}

### macOS

要把应用上传到 App Store，你首先必须确保所有必需的配置项都已设置，
以便你可以打包 App Bundle、创建已签名的 `.pkg` 文件并上传它。

下面几节将带你完成该过程。

#### 设置

你的应用必须包含一些配置，才能被 App Store 的验证系统接受。

{{% alert title="提示" %}}
下面几节将指导你为 App Store 提交配置应用。

要只在为 App Store 构建时应用以下配置变更，你可以创建一个单独的 Tauri 配置文件：

```json
{
  "bundle": {
    "macOS": {
      "entitlements": "./Entitlements.plist",
      "files": {
        "embedded.provisionprofile": "path/to/profile-name.provisionprofile"
      }
    }
  }
}
```

然后在为 App Store 打包 Tauri 应用时，把该配置文件与主配置合并：
{{% /alert %}}

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --no-bundle
npm run tauri bundle -- --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --no-bundle
yarn tauri bundle --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --no-bundle
pnpm tauri bundle --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --no-bundle
deno task tauri bundle --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --no-bundle
bun tauri bundle --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --no-bundle
cargo tauri bundle --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{< /tabpane >}}

当你在 CI/CD 中把应用上传到 App Store，而本地不需要描述文件，或者还要为 App Store 之外的分发编译应用时，这尤其有用。

- 分类

你的应用必须定义 [`tauri.conf.json > bundle > category`](https://tauri.app/reference/config/#category) 才能显示在 App Store 中：

```json
{
  "bundle": {
    "category": "Utility"
  }
}
```

- 描述文件

你还必须为应用创建描述文件，才能被 Apple 接受。

在 [Identifiers](https://developer.apple.com/account/resources/identifiers/list) 页面中，
创建一个新的 App ID，并确保它的 “Bundle ID” 值与 [`tauri.conf.json > identifier`](https://tauri.app/reference/config/#identifier) 中设置的标识符一致。

前往 [Profiles](https://developer.apple.com/account/resources/profiles/list) 页面创建一个新的描述文件。
对于 macOS 的 App Store 分发，它必须是 “Mac App Store Connect” 描述文件。
选择恰当的 App ID，并关联你用于代码签名的证书。

创建描述文件之后，下载它并保存到已知位置，然后配置 Tauri 将其包含进应用程序包：

```json
{
  "bundle": {
    "macOS": {
      "files": {
        "embedded.provisionprofile": "path/to/profile-name.provisionprofile"
      }
    }
  }
}
```

- Info.plist

你的应用必须遵守加密出口法规。
更多信息请参阅[官方文档](https://developer.apple.com/documentation/security/complying-with-encryption-export-regulations?language=objc)。

在 src-tauri 文件夹中创建 Info.plist 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>ITSAppUsesNonExemptEncryption</key>
	<false/> # 如果你的应用使用加密，请改为 `true`
</dict>
</plist>
```

- 授权

你的应用必须包含 App Sandbox 能力才能在 App Store 中分发。
此外，你还必须在代码签名授权中设置 App ID 和 Team ID。

在 `src-tauri` 文件夹中创建 `Entitlements.plist` 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.application-identifier</key>
    <string>$TEAM_ID.$IDENTIFIER</string>
    <key>com.apple.developer.team-identifier</key>
    <string>$TEAM_ID</string>
</dict>
</plist>
```

注意你必须把 `$IDENTIFIER` 替换为 [`tauri.conf.json > identifier`](https://tauri.app/reference/config/#identifier) 的值，
把 `$TEAM_ID` 替换为你的 Apple Developer team ID，它可以在你为描述文件创建的
[Identifier](https://developer.apple.com/account/resources/identifiers/list) 的 `App ID Prefix` 部分找到。

并在 macOS 打包配置 [`tauri.conf.json > bundle > macOS > entitlements`](https://tauri.app/reference/config/#entitlements) 中引用该文件：

```json
{
  "bundle": {
    "macOS": {
      "entitlements": "./Entitlements.plist"
    }
  }
}
```

现在你必须在启用代码签名的情况下构建应用，授权才会生效。

请确保你的应用在 App Sandbox 环境中能正常工作。

#### 构建

你必须把 macOS 应用以 `.pkg` 文件上传到 App Store。
运行以下命令把你的应用打包为 macOS App Bundle（`.app` 扩展名）：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --bundles app --target universal-apple-darwin
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}
上面的命令会创建一个 Universal App Binary 应用，同时支持 Apple Silicon 和 Intel 处理器。

如果你更希望只支持 Apple Silicon，必须把 [`tauri.conf.json > bundle > macOS > minimumSystemVersion`](https://tauri.app/reference/config/#minimumsystemversion) 改为 `12.0`：

```json
{
  "bundle": {
    "macOS": {
      "minimumSystemVersion": "12.0"
    }
  }
}
```

并根据你运行的 Mac 系统修改 CLI 命令和输出路径：

- 如果你的构建系统使用 Apple Silicon 芯片，请去掉 `--target universal-apple-darwin` 参数，并在下面引用的路径中用 `target/release`
  代替 `target/universal-apple-darwin/release`。
- 如果你的构建系统使用 Intel 芯片：
  - 安装 Rust 的 Apple Silicon 目标：
    ```
    rustup target add aarch64-apple-darwin
    ```
  - 把 `universal-apple-darwin` 参数改为 `aarch64-apple-darwin`，
    并在下面引用的路径中用 `target/aarch64-apple-darwin/release` 代替 `target/universal-apple-darwin/release`。

{{% /alert %}}

关于配置选项的更多信息，请参阅 [App Bundle 分发指南](../10-macosapplicationbundle/)。

要从应用包生成已签名的 `.pkg`，请运行以下命令：

```
xcrun productbuild --sign "<certificate signing identity>" --component "target/universal-apple-darwin/release/bundle/macos/$APPNAME.app" /Applications "$APPNAME.pkg"
```

注意你必须把 _$APPNAME_ 替换为你的应用名。

{{% alert title="注意" %}}
你必须用 _Mac Installer Distribution_ 签名证书为该 PKG 签名。
{{% /alert %}}

#### 上传

现在你可以使用 [`altool`](https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126) CLI 把应用的 PKG 上传到 App Store：

```
xcrun altool --upload-app --type macos --file "$APPNAME.pkg" --apiKey $APPLE_API_KEY_ID --apiIssuer $APPLE_API_ISSUER
```

注意 `altool` 需要 App Store Connect API 密钥才能上传应用。
更多信息请参阅[认证一节](#认证)。

随后你的应用会由 Apple 验证，若通过则在 TestFlight 中可用。

### iOS

要构建 iOS 应用，请运行 `tauri ios build` 命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri ios build -- --export-method app-store-connect
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri ios build --export-method app-store-connect
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri ios build --export-method app-store-connect
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri ios build --export-method app-store-connect
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri ios build --export-method app-store-connect
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri ios build --export-method app-store-connect
```

{{% /tab %}}

{{< /tabpane >}}

生成的 IPA 文件可以在 `src-tauri/gen/apple/build/arm64/$APPNAME.ipa` 找到。

注意你必须把 _$APPNAME_ 替换为你的应用名。

现在你可以使用 `altool` CLI 把 iOS 应用上传到 App Store：

```
xcrun altool --upload-app --type ios --file "src-tauri/gen/apple/build/arm64/$APPNAME.ipa" --apiKey $APPLE_API_KEY_ID --apiIssuer $APPLE_API_ISSUER
```

注意 `altool` 需要 App Store Connect API 密钥才能上传应用。
更多信息请参阅[认证一节](#认证)。

随后你的应用会由 Apple 验证，若通过则在 TestFlight 中可用。

### 认证

iOS 和 macOS 应用通过 `altool` 上传，它使用 App Store Connect API 密钥进行认证。

要创建新的 API 密钥，请打开 [App Store Connect 的 Users and Access 页面](https://appstoreconnect.apple.com/access/users)，选择 Integrations > Individual Keys 标签，点击 Add 按钮，选择名称与 Developer 权限。
`APPLE_API_ISSUER`（Issuer ID）显示在密钥表格上方，`APPLE_API_KEY_ID` 是该表格 Key ID 列中的值。
你还需要下载私钥，这只能做一次，并且只在页面重新加载后可见（按钮显示在新建密钥所在表格行上）。
私钥文件路径必须保存为 `AuthKey\_<APPLE_API_KEY_ID>.p8`，并放在以下目录之一：`<current-working-directory>/private_keys`、`~/private_keys`、`~/.private_keys` 或 `~/.appstoreconnect/private_keys`。
