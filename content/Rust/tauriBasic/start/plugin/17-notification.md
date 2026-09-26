+++
title = "17 Notification"
date = 2026-09-25T21:31:08+08:00
weight = 17
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/notification/](https://tauri.app/plugin/notification/)

使用 notification 插件向用户发送原生通知。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add notification
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add notification
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add notification
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add notification
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add notification
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add notification
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-notification
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_notification::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-notification
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-notification
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-notification
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-notification
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-notification
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

下面是使用 notification 插件的几个示例：

- [向用户发送通知](#发送通知)
- [为通知添加操作](#操作)
- [为通知添加附件](#附件)
- [在特定渠道中发送通知](#渠道)

notification 插件在 JavaScript 和 Rust 中都可以使用。

### 发送通知

按以下步骤发送一条通知：

1. 检查是否已授予权限

2. 如果未授予则请求权限

3. 发送通知

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import {
  isPermissionGranted,
  requestPermission,
  sendNotification,
} from '@tauri-apps/plugin-notification';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { isPermissionGranted, requestPermission, sendNotification, } = window.__TAURI__.notification;

// 你有发送通知的权限吗？
let permissionGranted = await isPermissionGranted();

// 如果没有，我们需要请求它
if (!permissionGranted) {
  const permission = await requestPermission();
  permissionGranted = permission === 'granted';
}

// 一旦获得权限，我们就可以发送通知了
if (permissionGranted) {
  sendNotification({ title: 'Tauri', body: 'Tauri is awesome!' });
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
tauri::Builder::default()
    .plugin(tauri_plugin_notification::init())
    .setup(|app| {
        use tauri_plugin_notification::NotificationExt;
        app.notification()
            .builder()
            .title("Tauri")
            .body("Tauri is awesome")
            .show()
            .unwrap();

        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

{{% /tab %}}

{{< /tabpane >}}

### 操作

{{% alert title="仅移动端" color="warning" %}}
Actions API 仅在移动平台可用。
{{% /alert %}}

操作为通知添加可交互的按钮和输入框。用它们可以为用户创造可响应的体验。

#### 注册操作类型

注册操作类型以定义可交互元素：

```javascript
import { registerActionTypes } from '@tauri-apps/plugin-notification';

await registerActionTypes([
  {
    id: 'messages',
    actions: [
      {
        id: 'reply',
        title: 'Reply',
        input: true,
        inputButtonTitle: 'Send',
        inputPlaceholder: 'Type your reply...',
      },
      {
        id: 'mark-read',
        title: 'Mark as Read',
        foreground: false,
      },
    ],
  },
]);
```

#### 操作属性

| 属性                     | 说明                             |
| ------------------------ | --------------------------------------- |
| `id`                     | 操作的唯一标识符        |
| `title`                  | 操作按钮的显示文本      |
| `requiresAuthentication` | 需要设备认证          |
| `foreground`             | 触发时把应用带到前台 |
| `destructive`            | 在 iOS 上以红色显示该操作              |
| `input`                  | 启用文本输入                      |
| `inputButtonTitle`       | 输入提交按钮的文本            |
| `inputPlaceholder`       | 输入框的占位文本        |

#### 监听操作

监听用户与通知操作的交互：

```javascript
import { onAction } from '@tauri-apps/plugin-notification';

await onAction((notification) => {
  console.log('Action performed:', notification);
});
```

### 附件

附件为通知添加媒体内容。各平台的支持程度不同。

```javascript
import { sendNotification } from '@tauri-apps/plugin-notification';

sendNotification({
  title: 'New Image',
  body: 'Check out this picture',
  attachments: [
    {
      id: 'image-1',
      url: 'asset:///notification-image.jpg',
    },
  ],
});
```

#### 附件属性

| 属性 | 说明                                    |
| -------- | ---------------------------------------------- |
| `id`     | 唯一标识符                              |
| `url`    | 使用 asset:// 或 file:// 协议的内容 URL |

注意：请在目标平台上测试附件以确保兼容性。

### 渠道

渠道（channel）把通知归入具有不同行为的分类。它主要用于 Android，但在各平台上提供一致的 API。

#### 创建渠道

```javascript
import {
  createChannel,
  Importance,
  Visibility,
} from '@tauri-apps/plugin-notification';

await createChannel({
  id: 'messages',
  name: 'Messages',
  description: 'Notifications for new messages',
  importance: Importance.High,
  visibility: Visibility.Private,
  lights: true,
  lightColor: '#ff0000',
  vibration: true,
  sound: 'notification_sound',
});
```

#### 渠道属性

| 属性      | 说明                                    |
| ------------- | ---------------------------------------------- |
| `id`          | 唯一标识符                              |
| `name`        | 显示名称                                   |
| `description` | 用途描述                            |
| `importance`  | 优先级（None、Min、Low、Default、High） |
| `visibility`  | 隐私设置（Secret、Private、Public）      |
| `lights`      | 启用通知 LED（Android）              |
| `lightColor`  | LED 颜色（Android）                            |
| `vibration`   | 启用振动                              |
| `sound`       | 自定义提示音文件名                          |

#### 管理渠道

列出已有渠道：

```javascript
import { channels } from '@tauri-apps/plugin-notification';

const existingChannels = await channels();
```

移除渠道：

```javascript
import { removeChannel } from '@tauri-apps/plugin-notification';

await removeChannel('messages');
```

#### 使用渠道

使用某个渠道发送通知：

```javascript
import { sendNotification } from '@tauri-apps/plugin-notification';

sendNotification({
  title: 'New Message',
  body: 'You have a new message',
  channelId: 'messages',
});
```

注意：在发送引用某渠道的通知之前先创建该渠道。无效的渠道 ID 会导致通知无法显示。

## 安全考量

除了对用户输入进行常规净化处理之外，目前没有已知的安全考量。
