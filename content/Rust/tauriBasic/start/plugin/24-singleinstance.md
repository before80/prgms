+++
title = "24 Single Instance"
date = 2026-09-25T21:31:08+08:00
weight = 24
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/single-instance/](https://tauri.app/plugin/single-instance/)

使用 Single Instance 插件确保你的 tauri 应用同一时刻只运行一个实例。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 不支持 |  |
| iOS | 不支持 |  |

## 设置

安装 Single Instance 插件即可开始。

**安装方式**

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add single-instance
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add single-instance
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add single-instance
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add single-instance
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add single-instance
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add single-instance
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-single-instance --target 'cfg(any(target_os = "macos", windows, target_os = "linux"))'
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .setup(|app| {
               #[cfg(desktop)]
               app.handle().plugin(tauri_plugin_single_instance::init(|app, args, cwd| {}));
               Ok(())
           })
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```


{{% alert title="注意" %}}

Single Instance 插件必须第一个注册才能正常工作。这样能确保它先于其它插件运行，避免被干扰。

{{% /alert %}}

## 用法

插件安装并初始化之后应当立即就能正常工作。不过我们还可以用 `init()` 方法增强它的功能。

插件的 `init()` 方法接收一个闭包，当新的应用实例被启动、但被插件关闭时，该闭包会被调用。
该闭包有三个参数：

1. **`app`：** 应用的 [AppHandle](https://docs.rs/tauri/2.0.0/tauri/struct.AppHandle.html)。
2. **`args`：** 用户为启动这个新实例所传入的参数列表。
3. **`cwd`：** 当前工作目录，也就是新应用实例被启动时所在的目录。

因此闭包大致如下：

```rust
.plugin(tauri_plugin_single_instance::init(|app, args, cwd| {
  // 在这里写你的代码……
}))
```

### 聚焦到新实例

默认情况下，当应用已在运行而你又启动一个新实例时，不会采取任何动作。如果希望在用户尝试打开新实例时聚焦正在运行实例的窗口，请把回调闭包改成这样：

```rust
use tauri::{AppHandle, Manager};

pub fn run() {
    let mut builder = tauri::Builder::default();
    #[cfg(desktop)]
    {
        builder = builder.plugin(tauri_plugin_single_instance::init(|app, args, cwd| {
            let _ = app.get_webview_window("main")
                       .expect("no main window")
                       .set_focus();
        }));
    }

    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## 在 Snap 与 Flatpak 中的用法

在 Linux 上，Single Instance 插件使用 DBus 来确保只会有一个实例在运行：第一个实例启动时会向 DBus 发布一个服务。随后的实例会尝试发布同一个服务，如果该服务已被发布，它们就向该服务发送请求以通知第一个实例，然后立即退出。

当应用以 deb、rpm 包或 AppImage 形式打包时，这套机制工作得相当好；但对 snap 或 flatpak 包默认不会按预期工作，因为这些包运行在受限的沙箱环境中，如果打包清单中没有显式声明，大部分与 DBus 服务的通信都会被阻止。

下面这个指南展示了如何声明所需权限，以便为 snap 和 flatpak 包启用 Single Instance：

### 获取你的应用 ID

Single Instance 插件会发布一个名为 `org.{id}.SingleInstance` 的服务。

`{id}` 就是你 `tauri.conf.json` 文件中的 `identifier`，但其中的点（`.`）和连字符（`-`）都会被替换为下划线（`_`）。

例如，如果你的标识符是 `net.mydomain.MyApp`：

- 你的应用 `{id}` 是 `net_mydomain_MyApp`
- 你的应用 SingleInstance 服务名是 `org.net_mydomain_MyApp.SingleInstance`

在 snap 和 flatpak 清单中授权你的应用使用该 DBus 服务时，就需要这个服务名，如下所示。

### Snap

在你的 snapcraft.yml 文件中，为 single instance 服务声明一个 plug 和一个 slot，并在应用声明中同时使用它们：

```yaml
# ...
slots:
  single-instance:
    interface: dbus
    bus: session
    name: org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID

plugs:
  single-instance-plug:
    interface: dbus
    bus: session
    name: org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID

# .....
apps:
  my-app:
    # ...
    plugs:
      # ....
      - single-instance-plug
    slots:
      # ...
      - single-instance

    # ....
```

这样你的应用就能按 Single Instance 插件的预期，向该 DBus 服务收发请求。

### Flatpak

在你的 flatpak 清单文件（your.app.id.yml 或 your.app.id.json）中，用服务名声明 `--talk-name` 和 `--own-name` 两个 finish 参数：

```yaml
# ...
finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --device=dri
  - --share=ipc
  # ....
  - --talk-name=org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID
  - --own-name=org.net_mydomain_MyApp.SingleInstance # 记得把 net_mydomain_MyApp 换成你的应用 ID
# ...
```

这样你的应用就能按 Single Instance 插件的预期，向该 DBus 服务收发请求。

## 权限

由于该插件目前没有 JavaScript API，你不需要配置[能力](../../security/4-capabilities/)就能使用它。
