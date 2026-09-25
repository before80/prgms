+++
title = "28 Updater"
date = 2026-09-25T21:31:08+08:00
weight = 28
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/updater/](https://tauri.app/plugin/updater/)

用更新服务器或静态 JSON 自动更新你的 Tauri 应用。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 不支持 |  |
| iOS | 不支持 |  |

## 设置

安装 Tauri updater 插件即可开始。

**安装方式**

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add updater
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add updater
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add updater
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add updater
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add updater
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add updater
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-updater --target 'cfg(any(target_os = "macos", windows, target_os = "linux"))'
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .setup(|app| {
               #[cfg(desktop)]
               app.handle().plugin(tauri_plugin_updater::Builder::new().build());
               Ok(())
           })
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 你可以用偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-updater
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-updater
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-updater
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-updater
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-updater
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 为更新签名

Tauri 的更新器需要一个签名来验证更新来自可信来源。这一点无法禁用。

要为更新签名，你需要两把密钥：

1. 公钥：会设置在 `tauri.conf.json` 中，用于在安装前校验产物。只要你的私钥安全，公钥可以安全地上传和分享。
2. 私钥：用于给安装包签名。你**绝不应**把它分享给任何人。另外，如果你丢失了这把密钥，你将**无法**再向已安装该应用的用户发布新更新。把密钥存放在安全的地方非常重要！

Tauri CLI 提供了 `signer generate` 命令来生成密钥。你可以运行它把密钥创建在主目录中：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri signer generate -- -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri signer generate -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri signer generate -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri signer generate -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bunx tauri signer generate -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri signer generate -w ~/.tauri/myapp.key
```

{{% /tab %}}

{{< /tabpane >}}

### 构建

构建更新产物时，你需要在环境变量中放入上面生成的私钥。`.env` 文件**不**起作用！

**操作系统**

{{< tabpane text=true persist=disabled >}}

{{% tab header="Mac/Linux" %}}

```sh
export TAURI_SIGNING_PRIVATE_KEY="Path or content of your private key"
# 可选：也可以加上密码
export TAURI_SIGNING_PRIVATE_KEY_PASSWORD=""
```

{{% /tab %}}

{{% tab header="Windows" %}}

在 `PowerShell` 中运行：

```ps
$env:TAURI_SIGNING_PRIVATE_KEY="Path or content of your private key"
<# 可选：也可以加上密码 #>
$env:TAURI_SIGNING_PRIVATE_KEY_PASSWORD=""
```

{{% /tab %}}

{{< /tabpane >}}

之后你就可以像平常一样运行 tauri build，Tauri 会生成更新包及其签名。
生成哪些文件取决于下面配置的 [`createUpdaterArtifacts`](https://tauri.app/reference/config/#createupdaterartifacts) 取值。

**模式**

{{< tabpane text=true persist=disabled >}}

{{% tab header="v2" %}}

```json
{
  "bundle": {
    "createUpdaterArtifacts": true
  }
}
```

在 Linux 上，Tauri 会在 `target/release/bundle/appimage/` 文件夹中生成普通的 AppImage：

- `myapp.AppImage` —— 标准应用包。更新器会复用它。
- `myapp.AppImage.sig` —— 更新包的签名。

在 macOS 上，Tauri 会在 target/release/bundle/macos/ 文件夹中从应用包生成 .tar.gz 归档：

- `myapp.app` —— 标准应用包。
- `myapp.app.tar.gz` —— 更新包。
- `myapp.app.tar.gz.sig` —— 更新包的签名。

在 Windows 上，Tauri 会在 target/release/bundle/msi/ 和 target/release/bundle/nsis 文件夹中生成普通的 MSI 与 NSIS 安装包：

- `myapp-setup.exe` —— 标准应用包。更新器会复用它。
- `myapp-setup.exe.sig` —— 更新包的签名。
- `myapp.msi` —— 标准应用包。更新器会复用它。
- `myapp.msi.sig` —— 更新包的签名。

{{% /tab %}}

{{% tab header="v1 兼容" %}}

```json
{
  "bundle": {
    "createUpdaterArtifacts": "v1Compatible"
  }
}
```

在 Linux 上，Tauri 会在 `target/release/bundle/appimage/` 文件夹中从 AppImage 生成 .tar.gz 归档：

- `myapp.AppImage` —— 标准应用包。
- `myapp.AppImage.tar.gz` —— 更新包。
- `myapp.AppImage.tar.gz.sig` —— 更新包的签名。

在 macOS 上，Tauri 会在 target/release/bundle/macos/ 文件夹中从应用包生成 .tar.gz 归档：

- `myapp.app` —— 标准应用包。
- `myapp.app.tar.gz` —— 更新包。
- `myapp.app.tar.gz.sig` —— 更新包的签名。

在 Windows 上，Tauri 会在 target/release/bundle/msi/ 和 target/release/bundle/nsis 文件夹中从 MSI 与 NSIS 安装包生成 .zip 归档：

- `myapp-setup.exe` —— 标准应用包。
- `myapp-setup.nsis.zip` —— 更新包。
- `myapp-setup.nsis.zip.sig` —— 更新包的签名。
- `myapp.msi` —— 标准应用包。
- `myapp.msi.zip` —— 更新包。
- `myapp.msi.zip.sig` —— 更新包的签名。

{{% /tab %}}

{{< /tabpane >}}

## Tauri 配置

按以下格式设置 `tauri.conf.json`，更新器才能开始工作。

| 键                                 | 说明                                                                                                                                                                                                                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `createUpdaterArtifacts`             | 设为 `true` 会告诉 Tauri 的应用打包器生成更新产物。如果你要把应用从更旧的 Tauri 版本迁移过来，请改为设为 `"v1Compatible"`。**该设置会在 v3 中移除**，所以请在你的用户全部迁移到 v2 之后把它改为 `true`。 |
| `pubkey`                             | 必须是上一步中用 Tauri CLI 生成的公钥。它**不能**是文件路径！                                                                                                                                                                                    |
| `endpoints`                          | 这必须是字符串形式的端点 URL 数组。生产模式下强制使用 TLS。Tauri 只有在返回非 2XX 状态码时才会继续尝试下一个 URL！                                                                                                                          |
| `dangerousInsecureTransportProtocol` | 设为 `true` 允许更新器接受非 HTTPS 端点。请谨慎使用该配置！                                                                                                                                                                                  |

每个更新器 URL 都可以包含以下动态变量，让你可以在服务端判断是否有可用更新。

- `current_version`：请求更新的应用版本（在 URL 中写作 `{{变量名}}`）。
- `target`：操作系统名称（`linux`、`windows` 或 `darwin` 之一）。
- `arch`：机器架构（`x86_64`、`i686`、`aarch64` 或 `armv7` 之一）。

```json
{
  "bundle": {
    "createUpdaterArtifacts": true
  },
  "plugins": {
    "updater": {
      "pubkey": "CONTENT FROM PUBLICKEY.PEM",
      "endpoints": [
        "https://releases.myapp.com/<target>/<arch>/<current_version>",
        // 或者一个静态的 github json 文件
        "https://github.com/user/repo/releases/latest/download/latest.json"
      ]
    }
  }
}
```

{{% alert title="提示" %}}
不支持自定义变量，但你可以定义[自定义 `target`](#自定义目标)。
{{% /alert %}}

### Windows 上的 `installMode`

在 Windows 上还有一个可选的 `"installMode"` 配置，用于改变更新的安装方式。

```json
{
  "plugins": {
    "updater": {
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

- `"passive"`：会有一个带进度条的小窗口。更新会在不需要用户任何交互的情况下安装。通常推荐使用，也是默认模式。
- `"basicUi"`：会显示一个基础用户界面，需要用户交互才能完成安装。
- `"quiet"`：不会向用户提供任何进度反馈。使用这种模式时安装程序无法自行请求管理员权限，因此它只适用于用户级安装，或者你的应用本身已经以管理员权限运行。通常不推荐。

## 服务器支持

更新器插件有两种使用方式：配合动态更新服务器，或使用静态 JSON 文件（用于 S3 或 GitHub gist 之类的服务）。

### 静态 JSON 文件

使用静态方式时，你只需返回包含所需信息的 JSON。

| 键        | 说明                                                                                                                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `version`   | 必须是合法的 [SemVer](https://semver.org/)，可以有或没有前导 `v`，也就是说 `1.0.0` 和 `v1.0.0` 都合法。                                 |
| `notes`     | 关于该更新的说明。                                                                                                                                         |
| `pub_date`  | 如果存在，日期必须按 [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) 格式化。                                                   |
| `platforms` | 每个平台键采用 `OS-ARCH` 格式，其中 `OS` 是 `linux`、`darwin` 或 `windows` 之一，`ARCH` 是 `x86_64`、`aarch64`、`i686` 或 `armv7` 之一。 |
| `signature` | 生成的 `.sig` 文件内容，它可能随每次构建而变化。路径或 URL 不行！                                                        |

{{% alert title="注意" %}}
使用[自定义目标](#自定义目标)时，所提供的目标字符串会与 `platforms` 键匹配，而不是默认的 `OS-ARCH` 值。
{{% /alert %}}

必需的键是 `"version"`、`"platforms.[target].url"` 和 `"platforms.[target].signature"`，其它都是可选的。

```json
{
  "version": "",
  "notes": "",
  "pub_date": "",
  "platforms": {
    "linux-x86_64": {
      "signature": "",
      "url": ""
    },
    "windows-x86_64": {
      "signature": "",
      "url": ""
    },
    "darwin-x86_64": {
      "signature": "",
      "url": ""
    }
  }
}
```

注意 Tauri 在校验 version 字段之前会先校验整个文件，因此请确保所有已存在的平台配置都合法且完整。

{{% alert title="提示" %}}
[Tauri Action](https://github.com/tauri-apps/tauri-action) 会为你生成一个静态 JSON 文件，可用于 GitHub Releases 之类的 CDN。
{{% /alert %}}

### 动态更新服务器

使用动态更新服务器时，Tauri 会遵循服务器的指示。要禁用内部版本检查，你可以覆盖[插件的版本比较逻辑](https://docs.rs/tauri-plugin-updater/latest/tauri_plugin_updater/struct.UpdaterBuilder.html#method.version_comparator)，这样就会直接安装服务器发来的版本（在你需要回滚应用时很有用）。

你的服务器可以使用上面 `endpoint` URL 中定义的变量来判断是否需要更新。如果你需要更多数据，可以按需在 [Rust 中加入额外的请求头](https://docs.rs/tauri-plugin-updater/latest/tauri_plugin_updater/struct.UpdaterBuilder.html#method.header)。

如果没有可用更新，你的服务器应当返回 [`204 No Content`](https://datatracker.ietf.org/doc/html/rfc2616#section-10.2.5) 状态码。

如果需要更新，你的服务器应当返回 [`200 OK`](http://tools.ietf.org/html/rfc2616#section-10.2.1) 状态码，并附上以下格式的 JSON 响应：

| 键        | 说明                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `version`   | 必须是合法的 [SemVer](https://semver.org/)，可以有或没有前导 `v`，也就是说 `1.0.0` 和 `v1.0.0` 都合法。 |
| `notes`     | 关于该更新的说明。                                                                                                              |
| `pub_date`  | 如果存在，日期必须按 [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) 格式化。                        |
| `url`       | 必须是更新包的合法 URL。                                                                                       |
| `signature` | 生成的 `.sig` 文件内容，它可能随每次构建而变化。路径或 URL 不行！                             |

必需的键是 `"url"`、`"version"` 和 `"signature"`，其它都是可选的。

```json
{
  "version": "",
  "pub_date": "",
  "url": "",
  "signature": "",
  "notes": ""
}
```

{{% alert title="提示" %}}
CrabNebula 是 Tauri 的官方合作伙伴，提供了动态更新服务器。更多信息请参阅[使用 CrabNebula Cloud 分发](../../distribute/4-crabnebulacloud/)文档。
{{% /alert %}}

## 检查更新

用于检查并安装更新的默认 API 会使用所配置的端点，
JavaScript 和 Rust 代码都可以访问它。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```js
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update) {
  console.log(
    `found update ${update.version} from ${update.date} with notes ${update.body}`
  );
  let downloaded = 0;
  let contentLength = 0;
  // 我们也可以分别调用 update.download() 和 update.install()
  await update.downloadAndInstall((event) => {
    switch (event.event) {
      case 'Started':
        contentLength = event.data.contentLength;
        console.log(`started downloading ${event.data.contentLength} bytes`);
        break;
      case 'Progress':
        downloaded += event.data.chunkLength;
        console.log(`downloaded ${downloaded} from ${contentLength}`);
        break;
      case 'Finished':
        console.log('download finished');
        break;
    }
  });

  console.log('update installed');
  await relaunch();
}
```

更多信息请参阅 [JavaScript API 文档](https://tauri.app/reference/javascript/updater/)。

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_updater::UpdaterExt;

pub fn run() {
  tauri::Builder::default()
    .setup(|app| {
      let handle = app.handle().clone();
      tauri::async_runtime::spawn(async move {
        update(handle).await.unwrap();
      });
      Ok(())
    })
    .run(tauri::generate_context!())
    .unwrap();
}

async fn update(app: tauri::AppHandle) -> tauri_plugin_updater::Result<()> {
  if let Some(update) = app.updater()?.check().await? {
    let mut downloaded = 0;

    // 我们也可以分别调用 update.download() 和 update.install()
    update
      .download_and_install(
        |chunk_length, content_length| {
          downloaded += chunk_length;
          println!("downloaded {downloaded} from {content_length:?}");
        },
        || {
          println!("download finished");
        },
      )
      .await?;

    println!("update installed");
    app.restart();
  }

  Ok(())
}
```

{{% alert title="提示" %}}
要把下载进度通知给前端，可以考虑使用带[通道](../../develop/4-callingfrontend/#通道)的命令。

<details>
  <summary>更新器命令</summary>

```rust
#[cfg(desktop)]
mod app_updates {
    use std::sync::Mutex;
    use serde::Serialize;
    use tauri::{ipc::Channel, AppHandle, State};
    use tauri_plugin_updater::{Update, UpdaterExt};

    #[derive(Debug, thiserror::Error)]
    pub enum Error {
        #[error(transparent)]
        Updater(#[from] tauri_plugin_updater::Error),
        #[error("there is no pending update")]
        NoPendingUpdate,
    }

    impl Serialize for Error {
        fn serialize<S>(&self, serializer: S) -> std::result::Result<S::Ok, S::Error>
        where
            S: serde::Serializer,
        {
            serializer.serialize_str(self.to_string().as_str())
        }
    }

    type Result<T> = std::result::Result<T, Error>;

    #[derive(Clone, Serialize)]
    #[serde(tag = "event", content = "data")]
    pub enum DownloadEvent {
        #[serde(rename_all = "camelCase")]
        Started {
            content_length: Option<u64>,
        },
        #[serde(rename_all = "camelCase")]
        Progress {
            chunk_length: usize,
        },
        Finished,
    }

    #[derive(Serialize)]
    #[serde(rename_all = "camelCase")]
    pub struct UpdateMetadata {
        version: String,
        current_version: String,
    }

    #[tauri::command]
    pub async fn fetch_update(
        app: AppHandle,
        pending_update: State<'_, PendingUpdate>,
    ) -> Result<Option<UpdateMetadata>> {
        let channel = "stable";
        let url = url::Url::parse(&format!(
            "https://cdn.myupdater.com/<target>-<arch>/<current_version>?channel={channel}",
        )).expect("invalid URL");

      let update = app
          .updater_builder()
          .endpoints(vec![url])?
          .build()?
          .check()
          .await?;

      let update_metadata = update.as_ref().map(|update| UpdateMetadata {
          version: update.version.clone(),
          current_version: update.current_version.clone(),
      });

      *pending_update.0.lock().unwrap() = update;

      Ok(update_metadata)
    }

    #[tauri::command]
    pub async fn install_update(pending_update: State<'_, PendingUpdate>, on_event: Channel<DownloadEvent>) -> Result<()> {
        let Some(update) = pending_update.0.lock().unwrap().take() else {
            return Err(Error::NoPendingUpdate);
        };

        let started = false;

        update
            .download_and_install(
                |chunk_length, content_length| {
                    if !started {
                        let _ = on_event.send(DownloadEvent::Started { content_length });
                        started = true;
                    }

                    let _ = on_event.send(DownloadEvent::Progress { chunk_length });
                },
                || {
                    let _ = on_event.send(DownloadEvent::Finished);
                },
            )
            .await?;

        Ok(())
    }

    struct PendingUpdate(Mutex<Option<Update>>);
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_process::init())
        .setup(|app| {
            #[cfg(desktop)]
            {
                app.handle().plugin(tauri_plugin_updater::Builder::new().build());
                app.manage(app_updates::PendingUpdate(Mutex::new(None)));
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            #[cfg(desktop)]
            app_updates::fetch_update,
            #[cfg(desktop)]
            app_updates::install_update
        ])
}
```

</details>
{{% /alert %}}

更多信息请参阅 [Rust API 文档](https://docs.rs/tauri-plugin-updater)。

{{% /tab %}}

{{< /tabpane >}}

注意安装更新之后并不需要立即重启应用，你可以自行选择如何处理更新：等到用户手动重启应用，或者提示他们选择何时重启。

{{% alert title="注意" %}}
在 Windows 上，由于 Windows 安装程序的限制，执行安装步骤时应用会被自动退出。
{{% /alert %}}

检查和下载更新时，可以定义自定义的请求超时、代理和请求头。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```js
import { check } from '@tauri-apps/plugin-updater';

const update = await check({
  proxy: '<proxy url>',
  timeout: 30000 /* 毫秒 */,
  headers: {
    Authorization: 'Bearer <token>',
  },
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_updater::UpdaterExt;
let update = app
  .updater_builder()
  .timeout(std::time::Duration::from_secs(30))
  .proxy("<proxy-url>".parse().expect("invalid URL"))
  .header("Authorization", "Bearer <token>")
  .build()?
  .check()
  .await?;
```

{{% /tab %}}

{{< /tabpane >}}

### 运行时配置

更新器 API 也允许在运行时配置更新器，以获得更大的灵活性。
出于安全原因，有些 API 只在 Rust 中可用。

#### 端点

在运行时设置用于检查更新的 URL，可以实现更动态的更新，例如分离的发布渠道：

```rust
use tauri_plugin_updater::UpdaterExt;
let channel = if beta { "beta" } else { "stable" };
let update_url = format!("https://{channel}.myserver.com/<target>-<arch>/<current_version>");

let update = app
  .updater_builder()
  .endpoints(vec![update_url])?
  .build()?
  .check()
  .await?;
```

{{% alert title="提示" %}}
注意使用 format!() 插值更新 URL 时，变量需要双重转义，
例如 `target`。
{{% /alert %}}

#### 公钥

在运行时设置公钥对实现密钥轮换逻辑很有用。
它既可以通过插件 builder 设置，也可以通过更新器 builder 设置：

```rust
tauri_plugin_updater::Builder::new().pubkey("<your public key>").build()
```

```rust
use tauri_plugin_updater::UpdaterExt;

let update = app
  .updater_builder()
  .pubkey("<your public key>")
  .build()?
  .check()
  .await?;
```

#### 自定义目标

默认情况下，更新器让你使用 `target` 和 `arch` 变量来决定必须投递哪个更新资源。
如果你需要关于更新的更多信息（例如分发 Universal macOS 二进制版本，或有更多构建变体时），
你可以设置自定义目标。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```js
import { check } from '@tauri-apps/plugin-updater';

const update = await check({
  target: 'macos-universal',
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

自定义目标既可以通过插件 builder 设置，也可以通过更新器 builder 设置：

```rust
tauri_plugin_updater::Builder::new().target("macos-universal").build()
```

```rust
use tauri_plugin_updater::UpdaterExt;
let update = app
  .updater_builder()
  .target("macos-universal")
  .build()?
  .check()
  .await?;
```

{{% alert title="提示" %}}
默认的 `$target-$arch` 键可以用 `tauri_plugin_updater::target()` 获取，
它返回一个 `Option<String>`，当当前平台不支持更新器时为 `None`。
{{% /alert %}}

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}

- 使用自定义目标时，可能更容易只用它来确定更新平台，
  这样你就可以去掉 `arch` 变量。
- 所提供的目标值在使用[静态 JSON 文件](#静态-json-文件)时就是与平台键匹配的键。

{{% /alert %}}

#### 允许降级

默认情况下，Tauri 会检查更新版本是否大于当前应用版本来判断是否应该更新。
要允许降级，你必须使用更新器 builder 的 `version_comparator` API：

```rust
use tauri_plugin_updater::UpdaterExt;

let update = app
  .updater_builder()
  .version_comparator(|current, update| {
    // 默认比较：`update.version > current`
    update.version != current
  })
  .build()?
  .check()
  .await?;
```

#### Windows 退出前钩子

由于 Windows 安装程序的限制，Tauri 在 Windows 上安装更新前会自动退出你的应用。
要在那之前执行某个动作，请使用 `on_before_exit` 函数：

```rust
use tauri_plugin_updater::UpdaterExt;

let update = app
  .updater_builder()
  .on_before_exit(|| {
    println!("app is about to exit on Windows!");
  })
  .build()?
  .check()
  .await?;
```

{{% alert title="注意" %}}
如果 builder 的某些值没有设置，会回退使用[配置](#tauri-配置)中的值。
{{% /alert %}}

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "updater:default",
  ]
}
```