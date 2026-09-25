+++
title = "4 Linux"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/sign/linux/](https://tauri.app/distribute/sign/linux/)

本指南提供关于 Linux 软件包代码签名的信息。
虽然把应用部署到 Linux 并不要求对产物签名，
但签名可以用来提升对你所部署应用的信任度。
对二进制文件签名可以让终端用户验证这些文件是真实的，且未被其它不受信任的实体修改过。

## 为 AppImage 签名

AppImage 可以用 gpg 或 gpg2 签名。

### 前置条件

必须准备好一把用于签名的密钥。可以用以下命令生成新的密钥：

```shell
gpg2 --full-gen-key
```

更多信息请参阅 gpg 或 gpg2 的文档。
你应当格外注意把私钥和公钥备份到安全的位置。

### 签名

你可以通过设置以下环境变量把签名嵌入 AppImage：

- **SIGN**：设为 `1` 以对 AppImage 签名。
- **SIGN_KEY**：可选变量，用于指定要使用的 GPG Key ID。
- **APPIMAGETOOL_SIGN_PASSPHRASE**：签名密钥的密码。如果未设置，gpg 会弹出对话框让你输入。在 CI/CD 平台上构建时你必须设置它。
- **APPIMAGETOOL_FORCE_SIGN**：默认情况下即使签名失败也会生成 AppImage。要让出错时退出，可以把该变量设为 `1`。

你可以运行以下命令显示嵌入在 AppImage 中的签名：

```shell
./src-tauri/target/release/bundle/appimage/$APPNAME_$VERSION_amd64.AppImage --appimage-signature
```

注意你需要根据自己的配置把 $APPNAME 和 $VERSION 替换为正确的值。

{{% alert title="警告" color="warning" %}}

**签名不会被自动验证**

AppImage 不会校验签名，因此你不能依赖它来检查文件是否被篡改。
用户必须使用 AppImage 校验工具手动验证签名。
这要求你在一个经过认证的渠道上发布你的密钥 ID（例如通过 TLS 提供的你的网站），
以便终端用户查看并验证。

更多信息请参阅 [AppImage 官方文档](https://docs.appimage.org/packaging-guide/optional/signatures.html)。

{{% /alert %}}

### 验证签名

AppImage 校验工具可以从[这里](https://github.com/AppImageCommunity/AppImageUpdate/releases/tag/continuous)下载。
选择其中一个 `validate-$PLATFORM.AppImage` 文件。

运行以下命令验证签名：

```shell
chmod +x validate-$PLATFORM.AppImage
./validate-$PLATFORM.AppImage $TAURI_OUTPUT.AppImage
```

如果签名有效，输出将会是：

```
Validation result: validation successful
Signatures found with key fingerprints: $KEY_ID
====================
Validator report:
Signature checked for key with fingerprint $KEY_ID:
Validation successful
```
