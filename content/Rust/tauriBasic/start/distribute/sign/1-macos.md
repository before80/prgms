+++
title = "1 macOS"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/sign/macos/](https://tauri.app/distribute/sign/macos/)

在 macOS 上，代码签名是让应用能上架 [Apple App Store](https://www.apple.com/app-store/)、以及避免从浏览器下载后被提示应用已损坏无法启动所必需的。

## 前置条件

macOS 上的代码签名需要一个 [Apple Developer](https://developer.apple.com) 账号，可以是付费的（每年 99 美元）或免费计划（仅用于测试和开发目的）。你还需要一台用于执行代码签名的 Apple 设备。这是签名流程和 Apple 条款与条件所要求的。

{{% alert title="注意" %}}
注意使用免费 Apple Developer 账号时，你将无法对应用进行公证，打开应用时仍会显示为未验证。
{{% /alert %}}

## 签名

要为 macOS 设置代码签名，你必须创建一个 Apple 代码签名证书，
并把它安装到 Mac 电脑的钥匙串中，或导出以便在 CI/CD 平台使用。

### 创建签名证书

要创建新的签名证书，你必须在 Mac 电脑上生成一个证书签名请求（CSR）文件。
关于如何为代码签名创建 CSR，请参阅[创建证书签名请求](https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request)。

在你的 Apple Developer 账号中，前往 [Certificates, IDs & Profiles 页面](https://developer.apple.com/account/resources/certificates/list)，
点击 `Create a certificate` 按钮打开创建新证书的界面。
选择合适的证书类型（`Apple Distribution` 用于把应用提交到 App Store，`Developer ID Application` 用于在 App Store 之外分发应用）。
上传你的 CSR，证书就会被创建。

{{% alert title="注意" %}}

只有 Apple Developer 的 `Account Holder` 才能创建 _Developer ID Application_ 证书。但可以通过使用不同的用户邮箱地址创建 CSR，把它关联到另一个 Apple ID。

{{% /alert %}}

### 下载证书

在 [Certificates, IDs & Profiles 页面](https://developer.apple.com/account/resources/certificates/list)中，点击你想使用的证书，然后点击 `Download` 按钮。
它会保存一个 `.cer` 文件，打开后会把证书安装到钥匙串中。

### 配置 Tauri

你可以配置 Tauri，使其在本地机器或 CI/CD 平台上构建 macOS 应用时使用你的证书。

#### 本地签名

把证书安装到 Mac 电脑的钥匙串后，你就可以配置 Tauri 用它进行代码签名。

证书钥匙串条目的名称就是 `signing identity`，也可以通过执行以下命令找到：

```sh
security find-identity -v -p codesigning
```

该 identity 可以在 [`tauri.conf.json > bundle > macOS > signingIdentity`](https://tauri.app/reference/config/#signingidentity) 配置项中提供，
也可以通过 `APPLE_SIGNING_IDENTITY` 环境变量提供。

{{% alert title="注意" %}}

签名证书只有与你的 Apple ID 关联时才有效。
无效证书不会列在 _Keychain Access > My Certificates_ 标签页中，
也不会出现在 _security find-identity -v -p codesigning_ 的输出中。
如果证书没有下载到正确位置，请确保在下载 .cer 文件时，_Keychain Access_ 的 “Default Keychains” 下选中了 “login” 选项。

{{% /alert %}}

#### 在 CI/CD 平台签名

要在 CI/CD 平台使用该证书，你必须把证书导出为 base64 字符串，
并配置 `APPLE_CERTIFICATE` 和 `APPLE_CERTIFICATE_PASSWORD` 环境变量：

1. 打开 `Keychain Access` 应用，点击 _login_ 钥匙串中的 _My Certificates_ 标签页，找到你的证书条目。
2. 展开该条目，右键点击密钥项，选择 `Export "$KEYNAME"`。
3. 选择保存证书 `.p12` 文件的路径，并为导出的证书定义密码。
4. 在终端运行以下脚本把 `.p12` 文件转换为 base64：

```sh
openssl base64 -A -in /path/to/certificate.p12 -out certificate-base64.txt
```

5. 把 `certificate-base64.txt` 文件的内容设置为 `APPLE_CERTIFICATE` 环境变量。
6. 把证书密码设置为 `APPLE_CERTIFICATE_PASSWORD` 环境变量。

<br />

<details>
<summary>GitHub Actions 配置示例</summary>

需要的 secret：

- `APPLE_ID` —— 你的 Apple ID 邮箱
- `APPLE_PASSWORD` —— 你的 Apple ID 密码
- `APPLE_CERTIFICATE` —— base64 编码的 `.p12` 文件
- `APPLE_CERTIFICATE_PASSWORD` —— 你导出的 `.p12` 文件的密码
- `KEYCHAIN_PASSWORD` —— 你的钥匙串密码

请查看 GitHub 官方指南了解[如何设置 secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)。

```yaml
name: 'build'

on:
  push:
    branches:
      - main

jobs:
  build-macos:
    needs: prepare
    strategy:
      matrix:
        include:
          - args: '--target aarch64-apple-darwin'
            arch: 'silicon'
          - args: '--target x86_64-apple-darwin'
            arch: 'intel'
    runs-on: macos-latest
    env:
      APPLE_ID: ${{ secrets.APPLE_ID }}
      APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
    steps:
      - name: Import Apple Developer Certificate
        env:
          APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
          APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          echo $APPLE_CERTIFICATE | base64 --decode > certificate.p12
          security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security set-keychain-settings -t 3600 -u build.keychain
          security import certificate.p12 -k build.keychain -P "$APPLE_CERTIFICATE_PASSWORD" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PASSWORD" build.keychain
          security find-identity -v -p codesigning build.keychain
      - name: Verify Certificate
        run: |
          CERT_INFO=$(security find-identity -v -p codesigning build.keychain | grep "Apple Development")
          CERT_ID=$(echo "$CERT_INFO" | awk -F'"' '{print $2}')
          echo "CERT_ID=$CERT_ID" >> $GITHUB_ENV
          echo "Certificate imported."
      - uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
          APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
          APPLE_SIGNING_IDENTITY: ${{ env.CERT_ID }}
        with:
          args: ${{ matrix.args }}
```

</details>

## 公证

要对应用进行公证，你必须提供凭据让 Tauri 向 Apple 认证。这可以通过 App Store Connect API，或通过你的 Apple ID 完成。

**方式**

{{< tabpane text=true persist=disabled >}}

{{% tab header="App Store Connect" %}}

1. 打开 [App Store Connect 的 Users and Access 页面](https://appstoreconnect.apple.com/access/users)，选择 Integrations 标签，点击 Add 按钮，选择名称与 Developer 权限。
2. 把 `APPLE_API_ISSUER` 环境变量设为密钥表格上方显示的值。
3. 把 `APPLE_API_KEY` 环境变量设为该表格 Key ID 列中的值。
4. 下载私钥，这只能做一次，并且只在页面重新加载后可见（按钮显示在新建密钥所在表格行上）。
5. 把 `APPLE_API_KEY_PATH` 环境变量设为所下载私钥的文件路径。

{{% /tab %}}

{{% tab header="Apple ID" %}}

1. 把 `APPLE_ID` 环境变量设为你的 Apple 账号邮箱。
2. 把 `APPLE_PASSWORD` 环境变量设为你的 Apple 账号的[应用专用密码](https://support.apple.com/en-ca/HT204397)。
3. 把 `APPLE_TEAM_ID` 环境变量设为你的 Apple Team ID。你可以在[你账号的会员页面](https://developer.apple.com/account#MembershipDetailsCard)中找到 Team ID。

{{% /tab %}}

{{< /tabpane >}}

设置好这些环境变量之后，重新运行你的 Tauri build 或 bundle 命令。例如，要用 pnpm 构建 DMG，请再次运行 `pnpm tauri build --bundles dmg`。如果你需要在首次公证时跳过 stapling，可以直接在 Tauri 命令后追加 `--skip-stapling`，例如 `pnpm tauri build --bundles dmg --skip-stapling`。

{{% alert title="注意" %}}
使用 _Developer ID Application_ 证书时必须进行公证。
{{% /alert %}}

## Ad-Hoc 签名

如果你不想提供经过 Apple 认证的身份，但仍希望为应用签名，你可以配置 _ad-hoc_ 签名。

这在 ARM（Apple Silicon）设备上很有用，因为那里所有来自互联网的应用都要求代码签名。

{{% alert title="警告" color="warning" %}}
Ad-hoc 代码签名并不能阻止 macOS 要求用户[在“隐私与安全性”设置中把该安装加入白名单](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac)。
{{% /alert %}}

要配置 ad-hoc 签名，请向 Tauri 提供伪标识 `-`，例如：

```json
"signingIdentity": "-"
```

关于配置 Tauri 签名身份的细节，见[上文](#配置-tauri)。
