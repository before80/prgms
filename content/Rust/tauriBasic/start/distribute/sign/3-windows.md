+++
title = "3 Windows"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/sign/windows/](https://tauri.app/distribute/sign/windows/)

在 Windows 上，代码签名是让应用能上架 [Microsoft Store](https://apps.microsoft.com/)、以及避免从浏览器下载后被 [SmartScreen](https://en.wikipedia.org/wiki/Microsoft_SmartScreen) 提示应用不受信任无法启动所必需的。

只要你的终端用户愿意忽略 [SmartScreen](https://en.wikipedia.org/wiki/Microsoft_SmartScreen) 警告，或者不是通过浏览器下载，那么在 Windows 上执行应用并不要求签名。
本指南涵盖通过 OV（Organization Validated）证书和 Azure Key Vault 进行签名。
如果你使用这里未记录的其它签名机制，例如 EV（Extended Validation）证书，
请查阅你的证书颁发机构的文档，并参阅[自定义签名命令](#自定义签名命令)一节。

## OV 证书

{{% alert title="危险" color="warning" %}}

本指南只适用于 2023 年 6 月 1 日之前获得的 OV 代码签名证书！对于使用 EV 证书以及该日期之后获得的 OV 证书进行代码签名，请改为查阅你的证书颁发机构的文档。

{{% /alert %}}

{{% alert title="注意" %}}

自 2024 年起，EV 证书不再能让你的应用立即获得 Microsoft SmartScreen 的信誉。Microsoft 在 2024 年从 Trusted Root Program 中移除了对 EV 代码签名证书的特殊待遇，因此 EV 和 OV 证书现在以相同方式积累 SmartScreen 信誉，新签名的版本在两者下都可能显示警告。请参阅 Microsoft 的 [Windows 应用开发者的 SmartScreen 信誉](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)和 [Windows 应用分发功能现状](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/distribution-feature-status#smartscreen-reputation-ev-certificates-no-longer-grant-instant-bypass)。

OV 证书通常更便宜，个人也可以申请。使用任何一种证书时，在文件和证书积累足够信誉之前，Microsoft SmartScreen 都可能向下载应用的用户显示警告。每次发布都用同一张证书签名，可以让这份信誉延续到后续版本。你也可以选择[把应用提交给](https://www.microsoft.com/en-us/wdsi/filesubmission/) Microsoft 人工审核。虽然不保证成功，但如果应用不含任何恶意代码，Microsoft 可能会给予额外信誉，并可能为该特定上传文件移除警告。

关于 OV 与 EV 证书的对比，请参阅[这篇比较](https://www.digicert.com/difference-between-dv-ov-and-ev-ssl-certificates)。

{{% /alert %}}

### 前置条件

- Windows —— 你很可能也能用其它平台，但本教程使用 PowerShell 原生功能。
- 一个可用的 Tauri 应用
- 代码签名证书 —— 你可以在 [Microsoft 文档](https://learn.microsoft.com/en-us/windows-hardware/drivers/dashboard/code-signing-cert-manage)列出的服务上获取。非 EV 证书的颁发机构可能比该列表中包含的更多，请自行比较并自行承担风险选择。
  - 请务必获取**代码签名**证书，SSL 证书不行！

### 入门

要让 Windows 做好代码签名的准备，有几件事要做：把证书转换成特定格式、安装该证书，以及从证书中解码所需信息。

1. **把你的 `.cer` 转换为 `.pfx`**
   - 你需要以下内容：
     - 证书文件（我的是 `cert.cer`）
     - 私钥文件（我的是 `private-key.key`）

   - 打开命令提示符，用 `cd Documents/Certs` 切换到当前目录

   - 用 `openssl pkcs12 -export -in cert.cer -inkey private-key.key -out certificate.pfx` 把你的 `.cer` 转换为 `.pfx`

   - 系统会提示你输入导出密码，**别忘了它！**

2. **把 `.pfx` 文件导入密钥库。**
   - 我们现在需要导入 `.pfx` 文件。

   - 用 `$WINDOWS_PFX_PASSWORD = 'MYPASSWORD'` 把导出密码赋给变量

   - 现在用 `Import-PfxCertificate -FilePath certificate.pfx -CertStoreLocation Cert:\CurrentUser\My -Password (ConvertTo-SecureString -String $WINDOWS_PFX_PASSWORD -Force -AsPlainText)` 导入证书

3. **准备变量**
   - 开始 ➡️ `certmgr.msc` 打开个人证书管理，然后打开 Personal/Certificates。

   - 找到我们刚导入的证书并双击它，然后点击 Details 标签。

   - Signature hash algorithm 就是我们的 `digestAlgorithm`。（提示：很可能是 `sha256`）

   - 向下滚动到 Thumbprint。那里应有一个类似 `A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0` 的值。这就是我们的 `certificateThumbprint`。

   - 我们还需要一个时间戳 URL；这是一个用于验证证书签名时间的授时服务器。我使用的是 `http://timestamp.comodoca.com`，但给你颁发证书的机构很可能也有一个。

### 准备 `tauri.conf.json` 文件

1. 现在我们有了 `certificateThumbprint`、`digestAlgorithm` 和 `timestampUrl`，接下来打开 `tauri.conf.json`。

2. 在 `tauri.conf.json` 中找到 `tauri` -> `bundle` -> `windows` 部分。我们捕获的信息对应三个变量。按下面这样填写。

```json
"windows": {
        "certificateThumbprint": "A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0",
        "digestAlgorithm": "sha256",
        "timestampUrl": "http://timestamp.comodoca.com"
}
```

3. 保存并运行 `tauri build`

4. 在控制台输出中，你应当看到如下内容。

```
info: signing app
info: running signtool "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.19041.0\\x64\\signtool.exe"
info: "Done Adding Additional Store\r\nSuccessfully signed: APPLICATION FILE PATH HERE
```

这表明你已成功签署该 `.exe`。

就是这样！你已成功为 Tauri 应用配置好 Windows 签名。

### 使用 GitHub Actions 为应用签名

我们也可以创建一个 workflow，用 GitHub Actions 为应用签名。

#### GitHub Secrets

我们需要添加几个 GitHub secret 以正确配置该 GitHub Action。它们的命名可以随意。

- 关于如何添加 GitHub secret，请参阅[加密 secret](https://docs.github.com/en/actions/reference/encrypted-secrets)指南。

我们使用的 secret 如下：

|        GitHub Secret        |                                                        变量取值                                                         |
| :--------------------------: | :-------------------------------------------------------------------------------------------------------------------------------: |
|     WINDOWS_CERTIFICATE      | 你的 .pfx 证书的 base64 编码版本，可以用 `certutil -encode certificate.pfx base64cert.txt` 生成 |
| WINDOWS_CERTIFICATE_PASSWORD |                                 创建证书 .pfx 时使用的证书导出密码                                  |

#### 修改 Workflow

1. 我们需要在 workflow 中添加一个步骤，把证书导入 Windows 环境。该 workflow 完成以下工作：
   1. 把 GitHub secret 赋给环境变量
   2. 创建一个新的 `certificate` 目录
   3. 把 `WINDOWS_CERTIFICATE` 写入 tempCert.txt
   4. 用 `certutil` 把 tempCert.txt 从 base64 解码为 `.pfx` 文件。
   5. 删除 tempCert.txt
   6. 把 `.pfx` 文件导入 Windows 的证书存储，并把 `WINDOWS_CERTIFICATE_PASSWORD` 转换为安全字符串以用于导入命令。

2. 我们将使用 [`tauri-action` 发布模板](https://github.com/tauri-apps/tauri-action)。

```yml
name: 'publish'
on:
  push:
    branches:
      - release

jobs:
  publish-tauri:
    strategy:
      fail-fast: false
      matrix:
        platform: [macos-latest, ubuntu-latest, windows-latest]

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v2
      - name: setup node
        uses: actions/setup-node@v1
        with:
          node-version: 12
      - name: install Rust stable
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      - name: install webkit2gtk (ubuntu only)
        if: matrix.platform == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y webkit2gtk-4.0
      - name: install app dependencies and build it
        run: yarn && yarn build
      - uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: app-v__VERSION__ # 该 action 会自动把 __VERSION__ 替换为应用版本
          releaseName: 'App v__VERSION__'
          releaseBody: 'See the assets to download this version and install.'
          releaseDraft: true
          prerelease: false
```

3. 在 `-name: install app dependencies and build it` 正上方添加以下步骤

```yml
- name: import windows certificate
  if: matrix.platform == 'windows-latest'
  env:
    WINDOWS_CERTIFICATE: ${{ secrets.WINDOWS_CERTIFICATE }}
    WINDOWS_CERTIFICATE_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
  run: |
    New-Item -ItemType directory -Path certificate
    Set-Content -Path certificate/tempCert.txt -Value $env:WINDOWS_CERTIFICATE
    certutil -decode certificate/tempCert.txt certificate/certificate.pfx
    Remove-Item -path certificate -include tempCert.txt
    Import-PfxCertificate -FilePath certificate/certificate.pfx -CertStoreLocation Cert:\CurrentUser\My -Password (ConvertTo-SecureString -String $env:WINDOWS_CERTIFICATE_PASSWORD -Force -AsPlainText)
```

4. 保存并推送到你的仓库。

5. 现在你的 workflow 就能导入 Windows 证书并将其导入 GitHub runner，从而实现自动化代码签名！

## Azure Key Vault

你可以通过提供 Azure Key Vault 证书和凭据来为 Windows 可执行文件签名。

{{% alert title="注意" %}}
本指南使用 [relic](https://github.com/sassoftware/relic)，因为它支持基于 secret 的认证，不过如果你愿意也可以配置其它工具。
要下载 relic，请查看它的[发布页面](https://github.com/sassoftware/relic/releases/)，或运行 `go install github.com/sassoftware/relic/v8@latest`。
{{% /alert %}}

1. Key Vault

在 [Azure Portal](https://portal.azure.com) 中前往 [Key vaults 服务](https://portal.azure.com/#browse/Microsoft.KeyVault%2Fvaults)，点击 “Create” 按钮创建一个新的 key vault。
记住 “Key vault name”，因为配置证书 URL 时需要该信息。

2. 证书

创建 key vault 后，选中它并进入 “Objects > Certificates” 页面创建一个新证书，点击 “Generate/Import” 按钮。
记住 “Certificate name”，因为配置证书 URL 时需要该信息。

3. Tauri 配置

[relic](https://github.com/sassoftware/relic) 使用配置文件来决定应使用哪个签名密钥。对于 Azure Key Vault，你还需要证书 URL。
在 `src-tauri` 文件夹中创建 `relic.conf` 文件，并配置 relic 使用你的证书：

```yml
tokens:
  azure:
    type: azure

keys:
  azure:
    token: azure
    id: https://\<KEY_VAULT_NAME\>.vault.azure.net/certificates/\<CERTIFICATE_NAME\>
```

注意你必须把 \<KEY_VAULT_NAME\> 和 \<CERTIFICATE_NAME\> 替换为前面步骤中的相应名称。

要配置 Tauri 使用你的 Azure Key Vault 配置进行签名，请修改 [bundle > windows > signCommand](https://tauri.app/reference/config/#signcommand) 配置值：

```json
{
  "bundle": {
    "windows": {
      "signCommand": "relic sign --file %1 --key azure --config relic.conf"
    }
  }
}
```

4. 凭据

[relic](https://github.com/sassoftware/relic) 必须向 Azure 认证才能加载证书。
在 Azure 门户首页，进入 “Microsoft Entra ID” 服务，前往 “Manage > App registrations” 页面。
点击 “New registration” 创建一个新应用。创建后你会被重定向到应用详情页，在那里可以看到 “Application (client) ID” 和 “Directory (tenant) ID” 值。
把这两个 ID 分别设置为 `AZURE_CLIENT_ID` 和 `AZURE_TENANT_ID` 环境变量。

在 “Manage > Certificates & secrets” 页面点击 “New client secret” 按钮，并把 “Value” 列中的文本设置为 `AZURE_CLIENT_SECRET` 环境变量。

设置好所有凭据后，回到你的 key vault 页面，进入 “Access control (IAM)” 页面。
你必须把 “Key Vault Certificate User” 和 “Key Vault Crypto User” 角色分配给你新建的应用。

设置好所有这些变量之后，运行 `tauri build` 就会生成已签名的 Windows 安装包！

## 自定义签名命令

在上面的 [Azure Key Vault](#azure-key-vault) 文档中，我们使用了一个强大的 Tauri Windows 签名配置，强制 Tauri CLI 使用
特殊的 shell 命令来签署 Windows 安装包可执行文件。[bundle > windows > signCommand](https://tauri.app/reference/config/#signcommand) 配置项可用于任何能够签署 Windows 可执行文件的代码签名工具。

{{% alert title="提示" %}}
从 Linux 和 macOS 机器交叉编译 Windows 安装包时，你**必须**使用自定义签名命令，因为默认实现只在 Windows 机器上有效。
{{% /alert %}}

## Azure Artifact Signing

你可以通过提供 Azure Artifact Signing（以前叫 Azure Code Signing/Azure Trusted Signing）证书和凭据来为 Windows 可执行文件签名。如果你还没有 Azure Artifact Signing 账号，可以按照[这篇教程](https://melatonin.dev/blog/code-signing-on-windows-with-azure-trusted-signing/)操作。

### 前置条件

如果你想用 GitHub Actions 签名，一切都应已安装。

1. [Artifact Signing 账号](https://learn.microsoft.com/en-us/azure/trusted-signing/quickstart?tabs=registerrp-portal,account-portal,certificateprofile-portal,deleteresources-portal)与权限已配置
1. [.NET](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)（推荐 .NET 8）
1. [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli#install-or-update)
1. [Signtool](https://learn.microsoft.com/en-us/dotnet/framework/tools/signtool-exe)（推荐 Windows 11 SDK 10.0.26100.0 或更高）

### 入门

你需要安装 [artifact-signing-cli](https://github.com/Levminer/artifact-signing-cli) 并配置环境变量。

1. **安装 artifact-signing-cli**
   - `cargo install artifact-signing-cli`

2. **配置环境变量**
   - artifact-signing-cli 需要设置以下环境变量，别忘了把它们加入 GitHub Actions 的 [secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)：
     - `AZURE_CLIENT_ID`：你的 [App Registration](https://melatonin.dev/blog/code-signing-on-windows-with-azure-trusted-signing/#step-4-create-app-registration-user-credentials) 的 client ID
     - `AZURE_CLIENT_SECRET`：[App Registration](https://melatonin.dev/blog/code-signing-on-windows-with-azure-trusted-signing/#step-4-create-app-registration-user-credentials) 的 client secret
     - `AZURE_TENANT_ID`：你的 Azure 目录的 tenant ID，也可以从你的 [App Registration](https://melatonin.dev/blog/code-signing-on-windows-with-azure-trusted-signing/#step-4-create-app-registration-user-credentials) 获取

3. **修改你的 `tauri.conf.json` 文件**
   - 你可以修改 `tauri.conf.json`，也可以为 Windows 创建一个专用配置文件。把 URL 和证书名替换为你自己的值。
     - -e：你的 Azure Artifact Signing 账号的端点
     - -a：你的 Azure Artifact Signing 账号名称
     - -c：你的 Azure Artifact Signing 账号中证书配置（Certificate profile）的名称
     - -d：被签名内容的描述（可选）。签署 .msi 安装包时，该描述会作为安装包名称显示在 UAC 提示中；未设置时则显示一串随机字符。

   ```json
   {
     "bundle": {
       "windows": {
         "signCommand": "artifact-signing-cli -e https://wus2.codesigning.azure.net -a MyAccount -c MyProfile -d MyApp %1"
       }
     }
   }
   ```
