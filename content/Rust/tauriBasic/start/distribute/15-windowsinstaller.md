+++
title = "15 Windows 安装包"
date = 2026-09-25T21:31:08+08:00
weight = 15
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/windows-installer/](https://tauri.app/distribute/windows-installer/)

Windows 上的 Tauri 应用要么以 Microsoft Installer（`.msi` 文件）形式分发，使用 [WiX Toolset v3](https://wixtoolset.org/documentation/manual/v3/)，要么以安装可执行文件（`-setup.exe` 文件）形式分发，使用 [NSIS](https://nsis.sourceforge.io/Main_Page)。

请注意 `.msi` 安装包**只能在 Windows 上创建**，因为 WiX 只能在 Windows 系统上运行。NSIS 安装包的交叉编译见下文。

本指南提供关于安装包可用自定义选项的信息。

## 构建

要构建并打包为 Windows 安装包，你可以在 Windows 电脑上使用 Tauri CLI 运行 `tauri build` 命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="MSI 包对 VBSCRIPT 的要求" %}}

构建 MSI 包（`tauri.conf.json` 中的 `"targets": "msi"` 或 `"targets": "all"`）需要在 Windows 上启用 VBSCRIPT 可选功能。该功能在大多数 Windows 安装中默认启用，但如果你遇到 `failed to run light.exe` 之类的错误，可能需要通过 **设置** → **应用** → **可选功能** → **更多 Windows 功能** 手动启用它。详细说明请参阅[前置条件指南](../../quickstart/2-prerequisites/#vbscript用于-msi-安装包)。

{{% /alert %}}

### 在 Linux 和 macOS 上构建 Windows 应用

在 Linux 和 macOS 主机上交叉编译 Windows 应用使用 [NSIS](https://nsis.sourceforge.io/Main_Page) 时是可行的，但有一些注意事项。
它不像直接在 Windows 上编译那样直接，测试也没那么充分。
因此只应在本地虚拟机或 GitHub Actions 之类的 CI 方案对你不可用时，作为最后手段使用。

{{% alert title="注意" %}}

为交叉编译出的 Windows 安装包签名需要外部签名工具。
更多信息请参阅[签名文档](../sign/3-windows/)。

{{% /alert %}}

由于 Tauri 官方只支持 MSVC Windows 目标，配置会稍微复杂一些。

#### 安装 NSIS

**操作系统**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Linux" %}}

有些 Linux 发行版的仓库中有 NSIS，例如在 Ubuntu 上你可以运行以下命令安装：

```sh
sudo apt install nsis
```

但在其它许多发行版上，你必须自行编译 NSIS，或手动下载发行版二进制包中未包含的 Stubs 与 Plugins。
例如 Fedora 只提供二进制文件，不提供 Stubs 与 Plugins：

```sh
sudo dnf in mingw64-nsis
wget https://github.com/tauri-apps/binary-releases/releases/download/nsis-3/nsis-3.zip
unzip nsis-3.zip
sudo cp nsis-3.08/Stubs/* /usr/share/nsis/Stubs/
sudo cp -r nsis-3.08/Plugins/** /usr/share/nsis/Plugins/
```

{{% /tab %}}

{{% tab header="macOS" %}}

在 macOS 上你需要 [Homebrew](https://brew.sh) 来安装 NSIS：

```sh
brew install nsis
```

{{% /tab %}}

{{< /tabpane >}}

#### 安装 LLVM 与 LLD 链接器

由于默认的 Microsoft 链接器只在 Windows 上工作，我们还需要安装新的链接器。
为了编译用于设置应用图标等内容的 Windows 资源文件，我们还需要 LLVM 项目中的 `llvm-rc` 二进制文件。

**操作系统**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Linux" %}}

```sh
sudo apt install lld llvm
```

在 Linux 上，如果你的依赖中包含在构建脚本里编译 C/C++ 依赖的包，你还需要安装 `clang` 包。
默认的 Tauri 应用不应需要它。

{{% /tab %}}

{{% tab header="macOS" %}}

```sh
brew install llvm
```

在 macOS 上，你还必须按安装输出中的建议把 `/opt/homebrew/opt/llvm/bin` 加入 `$PATH`。

{{% /tab %}}

{{< /tabpane >}}

#### 安装 Windows Rust 目标

假设你为 64 位 Windows 系统构建：

```sh
rustup target add x86_64-pc-windows-msvc
```

#### 安装 `cargo-xwin`

为了避免手动配置 Windows SDK，我们将使用 [`cargo-xwin`](https://github.com/rust-cross/cargo-xwin) 作为 Tauri 的“runner”：

```sh
cargo install --locked cargo-xwin
```

默认情况下 `cargo-xwin` 会把 Windows SDK 下载到项目本地文件夹。
如果你有多个项目并希望共享这些文件，可以设置 `XWIN_CACHE_DIR` 环境变量指向偏好位置。

#### 构建应用

现在只需在 `tauri build` 命令中加入 runner 和目标即可：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc
```

{{% /tab %}}

{{< /tabpane >}}

构建输出随后位于 `target/x86_64-pc-windows-msvc/release/bundle/nsis/`。

### 为 32 位或 ARM 构建

Tauri CLI 默认使用你机器的架构编译可执行文件。
假设你在 64 位机器上开发，CLI 会生成 64 位应用。

如果你需要支持 **32 位**机器，可以用 `--target` 参数为**不同的** [Rust 目标](https://doc.rust-lang.org/nightly/rustc/platform-support.html)编译应用：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --target i686-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --target i686-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --target i686-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --target i686-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --target i686-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --target i686-pc-windows-msvc
```

{{% /tab %}}

{{< /tabpane >}}

默认情况下 Rust 只为你机器的目标安装工具链，
因此你需要先安装 32 位 Windows 工具链：`rustup target add i686-pc-windows-msvc`。

如果你需要为 **ARM64** 构建，首先需要安装额外的构建工具。
为此请打开 `Visual Studio Installer`，点击 “Modify”，在 “Individual Components” 标签中安装 “C++ ARM64 build tools”。
撰写本文时，VS2022 中的确切名称是 `MSVC v143 - VS 2022 C++ ARM64 build tools (Latest)`。
现在你可以用 `rustup target add aarch64-pc-windows-msvc` 添加 Rust 目标，然后用上述方法编译应用：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --target aarch64-pc-windows-msvc
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}

注意 NSIS 安装包本身在 ARM 机器上仍是通过模拟运行的 x86 程序。应用本身则是原生 ARM64 二进制文件。

{{% /alert %}}

## 支持 Windows 7

默认情况下，Microsoft Installer（`.msi`）在 Windows 7 上无法工作，因为如果未安装 WebView2 引导程序，它需要下载该引导程序
（如果操作系统中未启用 TLS 1.2，这可能失败）。Tauri 提供了嵌入 WebView2 引导程序的选项
（见下文[嵌入 WebView2 引导程序](#嵌入-webview2-引导程序)一节）。
基于 NSIS 的安装包（`-setup.exe`）在 Windows 7 上也支持 `downloadBootstrapper` 模式。

此外，要在 Windows 7 上使用 Notification API，你需要启用 `windows7-compat` Cargo 特性：

```toml
[dependencies]
tauri-plugin-notification = { version = "2.0.0", features = [ "windows7-compat" ] }
```

## FIPS 合规

如果你的系统要求 MSI 包符合 FIPS，你可以在运行 `tauri build` 之前把 `TAURI_BUNDLER_WIX_FIPS_COMPLIANT` 环境变量设为 `true`。在 PowerShell 中，你可以像这样为当前终端会话设置它：

```powershell
$env:TAURI_BUNDLER_WIX_FIPS_COMPLIANT="true"
```

## WebView2 安装选项

安装包默认会下载 WebView2 引导程序，并在运行时未安装时执行它。
或者，你也可以嵌入引导程序、嵌入离线安装包，或使用固定版本的 WebView2 运行时。
下表对比了这些方式：

| 安装方式                                | 需要联网？ | 安装包额外体积 | 说明                                                                                                                   |
| :------------------------------------------------- | :---------------------------- | :------------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| [`downloadBootstrapper`](#已下载的引导程序) | 是                           | 0MB                       | `Default` <br /> 安装包体积更小，但不推荐用于通过 `.msi` 向 Windows 7 部署。 |
| [`embedBootstrapper`](#嵌入-webview2-引导程序)      | 是                           | ~1.8MB                    | 对 `.msi` 安装包在 Windows 7 上有更好的支持。                                                                      |
| [`offlineInstaller`](#离线安装包)           | 否                            | ~127MB                    | 嵌入 WebView2 安装包。推荐用于离线环境。                                                        |
| [`fixedVersion`](#固定版本)           | 否                            | ~180MB                    | 嵌入固定的 WebView2 版本。                                                                                        |
| [`skip`](#跳过安装)                   | 否                            | 0MB                       | ⚠️ 不推荐 <br /> 不在 Windows 安装包中安装 WebView2。                               |

{{% alert title="注意" %}}

在 Windows 10（2018 年 4 月版或更高）和 Windows 11 上，WebView2 运行时作为操作系统的一部分分发。

{{% /alert %}}

### 已下载的引导程序

这是构建 Windows 安装包时的默认设置。它会下载引导程序并运行它。
需要联网，但安装包体积更小。
如果你要通过 `.msi` 安装包面向 Windows 7 分发，则不推荐使用。

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "downloadBootstrapper"
      }
    }
  }
}
```

### 嵌入 WebView2 引导程序

要嵌入 WebView2 引导程序，请把 [webviewInstallMode](https://tauri.app/reference/config/#webviewinstallmode) 设为 `embedBootstrapper`。
这会使安装包体积增加约 1.8MB，但提升了对 Windows 7 系统的兼容性。

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "embedBootstrapper"
      }
    }
  }
}
```

### 离线安装包

要嵌入 WebView2 离线安装包，请把 [webviewInstallMode](https://tauri.app/reference/config/#webviewinstallmode) 设为 `offlineInstaller`。
这会使安装包体积增加约 127MB，但即便没有网络连接也能安装你的应用。

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "offlineInstaller"
      }
    }
  }
}
```

### 固定版本

使用系统提供的运行时对安全性很有好处，因为 webview 的漏洞补丁由 Windows 管理。
如果你想在每个应用上自行控制 WebView2 的分发
（要么自己管理补丁发布，要么在可能没有网络连接的环境中分发应用），
Tauri 可以为你打包运行时文件。

{{% alert title="警告" color="warning" %}}

分发固定版本的 WebView2 运行时会使用 Windows 安装包增大约 180MB。

{{% /alert %}}

1. 从 [Microsoft 网站](https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section)下载 WebView2 固定版本运行时。
   在本例中，下载的文件名是 `Microsoft.WebView2.FixedVersionRuntime.128.0.2739.42.x64.cab`
2. 把该文件解压到核心文件夹：

```powershell
Expand .\Microsoft.WebView2.FixedVersionRuntime.128.0.2739.42.x64.cab -F:* ./src-tauri
```

3. 在 `tauri.conf.json` 中配置 WebView2 运行时路径：

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "fixedRuntime",
        "path": "./Microsoft.WebView2.FixedVersionRuntime.98.0.1108.50.x64/"
      }
    }
  }
}
```

4. 运行 `tauri build` 生成带固定 WebView2 运行时的 Windows 安装包。

### 跳过安装

你可以通过把 [webviewInstallMode](https://tauri.app/reference/config/#webviewinstallmode) 设为 `skip` 来从安装包中移除 WebView2 运行时下载检查。
如果用户未安装该运行时，你的应用**将无法**工作。

{{% alert title="警告" color="warning" %}}

如果用户未安装该运行时，你的应用**将无法**工作，安装包也不会尝试安装它。

{{% /alert %}}

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "skip"
      }
    }
  }
}
```

## 最低 Webview2 版本

如果你的应用需要仅在较新 Webview2 版本中才有的特性（例如自定义 URI scheme），你可以让 Windows 安装包
校验当前 Webview2 版本，并在不匹配目标版本时运行 Webview2 引导程序。

```json
{
  "bundle": {
    "windows": {
      "minimumWebview2Version": "110.0.1531.0"
    }
  }
}
```

## 自定义 WiX 安装包

完整的自定义选项列表请参阅 [WiX 配置](https://tauri.app/reference/config/#wixconfig)。

### 安装包模板

`.msi` Windows 安装包使用 [WiX Toolset v3](https://wixtoolset.org/documentation/manual/v3/) 构建。
目前，除了预定义的[配置](https://tauri.app/reference/config/#wixconfig)之外，你还可以通过自定义 WiX 源代码
（扩展名为 `.wxs` 的 XML 文件）或 WiX fragment 来修改它。

#### 用自定义 WiX 文件替换安装包代码

Tauri 定义的 Windows Installer XML 已针对简单的基于 webview 应用的常见用例做了配置
（你可以在[这里](https://github.com/tauri-apps/tauri/blob/dev/crates/tauri-bundler/src/bundle/windows/msi/main.wxs)找到它）。
它使用 [handlebars](https://docs.rs/handlebars/latest/handlebars/)，因此 Tauri CLI 可以根据你的 `tauri.conf.json` 定义来为安装包打上品牌信息。
如果你需要完全不同的安装包，可以在 [`tauri.bundle.windows.wix.template`](https://tauri.app/reference/config/#template-2) 上配置自定义模板文件。

#### 用 WiX Fragment 扩展安装包

[WiX fragment](https://wixtoolset.org/documentation/manual/v3/xsd/wix/fragment.html) 是一个容器，你几乎可以在其中配置 WiX 提供的一切。
在这个示例中，我们将定义一个写入两条注册表项的 fragment：

```xml
<?xml version="1.0" encoding="utf-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Fragment>
    <!-- 这些注册表项应被安装
		 到目标用户的机器上 -->
    <DirectoryRef Id="TARGETDIR">
      <!-- 把要安装的注册表项归组在一起 -->
      <!-- 注意我们在这里提供了唯一的 `Id` -->
      <Component Id="MyFragmentRegistryEntries" Guid="*">
        <!-- 注册表键将位于
			 HKEY_CURRENT_USER\Software\MyCompany\MyApplicationName 下 -->
        <!-- Tauri 使用 bundle 标识符的第二部分作为 `MyCompany` 名称
			 （例如 `com.tauri-apps.test` 中的 `tauri-apps`） -->
        <RegistryKey
          Root="HKCU"
          Key="Software\MyCompany\MyApplicationName"
          Action="createAndRemoveOnUninstall"
        >
          <!-- 要持久化到注册表中的值 -->
          <RegistryValue
            Type="integer"
            Name="SomeIntegerValue"
            Value="1"
            KeyPath="yes"
          />
          <RegistryValue Type="string" Value="Default Value" />
        </RegistryKey>
      </Component>
    </DirectoryRef>
  </Fragment>
</Wix>
```

把该 fragment 文件以 `.wxs` 扩展名保存到 `src-tauri/windows/fragments` 文件夹，并在 `tauri.conf.json` 中引用它：

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "fragmentPaths": ["./windows/fragments/registry.wxs"],
        "componentRefs": ["MyFragmentRegistryEntries"]
      }
    }
  }
}
```

注意 `ComponentGroup`、`Component`、`FeatureGroup`、`Feature` 和 `Merge` 元素的 id 必须分别在 `tauri.conf.json` 的 `wix` 对象中
通过 `componentGroupRefs`、`componentRefs`、`featureGroupRefs`、`featureRefs` 和 `mergeRefs` 引用，才能被包含进安装包。

### 国际化

WiX 安装包默认使用 `en-US` 语言构建。
国际化（i18n）可以通过 [`tauri.bundle.windows.wix.language`](https://tauri.app/reference/config/#language) 属性配置，
定义 Tauri 应为哪些语言构建安装包。
你可以在 [Microsoft 网站](https://docs.microsoft.com/en-us/windows/win32/msi/localizing-the-error-and-actiontext-tables)的 Language-Culture 列中找到可用的语言名称。

#### 为单一语言编译 WiX 安装包

要创建面向特定语言的单个安装包，请把 `language` 值设为字符串：

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "language": "fr-FR"
      }
    }
  }
}
```

#### 为列表中的每种语言各编译一个 WiX 安装包

要编译面向一组语言的安装包，请使用数组。
会为每种语言各创建一个安装包，并以语言键作为后缀：

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "language": ["en-US", "pt-BR", "fr-FR"]
      }
    }
  }
}
```

#### 为每种语言配置 WiX 安装包字符串

可以为每种语言定义配置对象来配置本地化字符串：

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "language": {
          "en-US": null,
          "pt-BR": {
            "localePath": "./wix/locales/pt-BR.wxl"
          }
        }
      }
    }
  }
}
```

`localePath` 属性定义语言文件的路径，这是一个配置语言文化的 XML：

```xml
<WixLocalization
  Culture="en-US"
  xmlns="http://schemas.microsoft.com/wix/2006/localization"
>
  <String Id="LaunchApp"> Launch MyApplicationName </String>
  <String Id="DowngradeErrorMessage">
    A newer version of MyApplicationName is already installed.
  </String>
  <String Id="PathEnvVarFeature">
    Add the install location of the MyApplicationName executable to
    the PATH system environment variable. This allows the
    MyApplicationName executable to be called from any location.
  </String>
  <String Id="InstallAppFeature">
    Installs MyApplicationName.
  </String>
</WixLocalization>
```

{{% alert title="注意" %}}

`WixLocalization` 元素的 `Culture` 字段必须与所配置的语言一致。

{{% /alert %}}

目前 Tauri 引用以下本地化字符串：`LaunchApp`、`DowngradeErrorMessage`、`PathEnvVarFeature` 和 `InstallAppFeature`。
你可以定义自己的字符串，并在自定义模板或 fragment 中用 `"!(loc.TheStringId)"` 引用它们。
更多信息请参阅 [WiX 本地化文档](https://wixtoolset.org/documentation/manual/v3/howtos/ui_and_localization/make_installer_localizable.html)。

## 自定义 NSIS 安装包

完整的自定义选项列表请参阅 [NSIS 配置](https://tauri.app/reference/config/#nsisconfig)。

### 安装包模板

Tauri 定义的 NSIS 安装包 `.nsi` 脚本已针对简单的基于 webview 应用的常见用例做了配置
（你可以在[这里](https://github.com/tauri-apps/tauri/blob/dev/crates/tauri-bundler/src/bundle/windows/nsis/installer.nsi)找到它）。
它使用 [handlebars](https://docs.rs/handlebars/latest/handlebars/)，因此 Tauri CLI 可以根据你的 `tauri.conf.json` 定义来为安装包打上品牌信息。
如果你需要完全不同的安装包，可以在 [`tauri.bundle.windows.nsis.template`](https://tauri.app/reference/config/#template-1) 上配置自定义模板文件。

### 扩展安装包

如果你只需要扩展某些安装步骤，也许可以使用安装包 hook，而不必替换整个安装包模板。

支持的 hook 有：

- `NSIS_HOOK_PREINSTALL`：在复制文件、设置注册表键值和创建快捷方式之前运行。
- `NSIS_HOOK_POSTINSTALL`：在安装包完成所有文件复制、注册表键设置和快捷方式创建之后运行。
- `NSIS_HOOK_PREUNINSTALL`：在移除任何文件、注册表键和快捷方式之前运行。
- `NSIS_HOOK_POSTUNINSTALL`：在文件、注册表键和快捷方式被移除之后运行。

例如，在 `src-tauri/windows` 文件夹中创建 `hooks.nsh` 文件，并定义你需要的 hook：

```nsh
!macro NSIS_HOOK_PREINSTALL
  MessageBox MB_OK "PreInstall"
!macroend

!macro NSIS_HOOK_POSTINSTALL
  MessageBox MB_OK "PostInstall"
!macroend

!macro NSIS_HOOK_PREUNINSTALL
  MessageBox MB_OK "PreUnInstall"
!macroend

!macro NSIS_HOOK_POSTUNINSTALL
  MessageBox MB_OK "PostUninstall"
!macroend
```

然后你必须配置 Tauri 使用该 hook 文件：

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "installerHooks": "./windows/hooks.nsh"
      }
    }
  }
}
```

#### 在 hook 旁边包含文件

Tauri 通过 `!include` 从它生成的 NSIS 脚本中引入你的 hook 文件。在 hook 文件的顶层，`${__FILEDIR__}` 指向 hook 文件所在目录，因此你可以直接包含它旁边的文件。

然而，宏体会在 Tauri 把它们插入生成脚本的位置展开。因此在 hook 宏内部，`${__FILEDIR__}` 指向的是生成脚本所在目录。如果某个宏需要 hook 旁边的文件，请先在顶层用 `!define` 捕获 hook 目录：

```nsh
!include "${__FILEDIR__}\adjacent.nsh"
!define HOOK_FILE_DIR "${__FILEDIR__}"

!macro NSIS_HOOK_PREINSTALL
  File "${HOOK_FILE_DIR}\example.txt"
!macroend
```

#### 用 hook 安装依赖

你可以用安装包 hook 自动安装应用所需的系统依赖。这对 Visual C++ 可再发行组件、DirectX、OpenSSL 或其它系统库之类的运行时依赖特别有用，因为它们可能并未安装在所有 Windows 系统上。

**MSI 安装包示例（Visual C++ 可再发行组件）：**

```nsh
!macro NSIS_HOOK_POSTINSTALL
  ; 检查是否已安装 Visual C++ 2019 可再发行组件（通过 Windows 注册表）
  ReadRegDWord $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Installed"

  ${If} $0 == 1
    DetailPrint "Visual C++ Redistributable already installed"
    Goto vcredist_done
  ${EndIf}

  ; 如果未安装，则从打包的 MSI 安装
  ${If} ${FileExists} "$INSTDIR\resources\vc_redist.x64.msi"
    DetailPrint "Installing Visual C++ Redistributable..."
    ; 先复制到 TEMP 文件夹再执行安装程序
    CopyFiles "$INSTDIR\resources\vc_redist.x64.msi" "$TEMP\vc_redist.x64.msi"
    ExecWait 'msiexec /i "$TEMP\vc_redist.x64.msi" /passive /norestart' $0

    ; 检查安装进程是否成功退出（代码 0）
    ${If} $0 == 0
      DetailPrint "Visual C++ Redistributable installed successfully"
    ${Else}
      MessageBox MB_ICONEXCLAMATION "Visual C++ installation failed. Some features may not work."
    ${EndIf}

    ; 清理 TEMP 与已安装应用中的安装文件
    Delete "$TEMP\vc_redist.x64.msi"
    Delete "$INSTDIR\resources\vc_redist.x64.msi"
  ${EndIf}

  vcredist_done:
!macroend
```

**关键注意事项：**

- 良好的做法是始终通过注册表键、文件是否存在或 Windows 的 [where](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/where) 命令检查依赖是否已安装。
- 使用 `/passive`、`/quiet` 或 `/silent` 参数，避免打断安装流程。`.msi` 文件的选项见 [msiexec](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/msiexec)，应用特定的参数见其安装手册
- 加入 `/norestart`，防止会重启用户设备的安装程序在安装过程中自动重启系统
- 清理临时文件和打包的安装程序，避免应用体积膨胀
- 卸载时要考虑到依赖可能与其他应用共享
- 安装失败时提供有意义的错误信息

请确保把依赖安装程序打包进 `src-tauri/resources` 文件夹，并加入 `tauri.conf.json` 以便它们被打包，且在安装期间可从 `$INSTDIR\resources\` 访问：

```json
{
  "bundle": {
    "resources": [
      "resources/my-dependency.exe",
      "resources/another-one.msi
    ]
  }
}
```

### 安装模式

默认情况下，安装包只为当前用户安装你的应用。
这种方式的优点是不需要管理员权限即可运行安装包，
但应用会安装在 `%LOCALAPPDATA%` 文件夹而不是 `C:/Program Files` 中。

如果你希望应用安装后对全系统可用（需要管理员权限），
可以把 [installMode](https://tauri.app/reference/config/#installmode) 设为 `perMachine`：

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "installMode": "perMachine"
      }
    }
  }
}
```

或者，你可以把 [installMode](https://tauri.app/reference/config/#installmode) 设为 `both`，让用户自己选择是只为当前用户安装还是全系统安装。
注意这样安装包执行时会需要管理员权限。

更多信息请参阅 [NSISInstallerMode](https://tauri.app/reference/config/#nsisinstallermode)。

### 国际化

NSIS 安装包是多语言安装包，也就是说你始终只会有单个安装包，其中包含所有选定的翻译。

你可以用 [`tauri.bundle.windows.nsis.languages`](https://tauri.app/reference/config/#languages) 属性指定要包含哪些语言。
NSIS 支持的语言列表见 [NSIS GitHub 项目](https://github.com/kichik/nsis/tree/9465c08046f00ccb6eda985abbdbf52c275c6c4d/Contrib/Language%20files)。
其中有一些 [Tauri 特有的翻译](https://github.com/tauri-apps/tauri/tree/dev/crates/tauri-bundler/src/bundle/windows/nsis/languages)是必需的，所以如果你看到未翻译的文本，欢迎在 [Tauri 主仓库](https://github.com/tauri-apps/tauri/issues/new?assignees=&labels=type%3A+feature+request&template=feature_request.yml&title=%5Bfeat%5D+)提 feature request。
你也可以提供[自定义翻译文件](https://tauri.app/reference/config/#customlanguagefiles)。

默认使用操作系统的默认语言来决定安装包语言。
你也可以配置安装包在渲染安装包内容之前显示语言选择器：

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "displayLanguageSelector": true
      }
    }
  }
}
```
