+++
title = "4 系统托盘"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/system-tray/](https://tauri.app/learn/system-tray/)

Tauri 允许你为应用创建并自定义系统托盘。
它可以通过提供常用操作的快捷入口来提升用户体验。

## 配置

首先，更新你的 `Cargo.toml`，加入系统托盘所需的功能特性。

```toml
tauri = { version = "2.0.0", features = [ "tray-icon" ] }
```

## 用法

托盘 API 在 JavaScript 和 Rust 中都可以使用。

### 创建托盘图标

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

使用 [`TrayIcon.new`](https://tauri.app/reference/javascript/api/namespacetray/#new) 静态函数创建新的托盘图标：

```javascript
import { TrayIcon } from '@tauri-apps/api/tray';

const options = {
  // 在这里你可以添加托盘菜单、标题、工具提示、事件处理器等
};

const tray = await TrayIcon.new(options);
```

关于可自定义的选项，更多信息见 [`TrayIconOptions`](https://tauri.app/reference/javascript/api/namespacetray/#trayiconoptions)。

{{% /tab %}}

{{% tab header="Rust" %}}

```rust

tauri::Builder::default()
    .setup(|app| {
        let tray = TrayIconBuilder::new().build(app)?;
        Ok(())
    })

```

关于可自定义的选项，更多信息见 [`TrayIconBuilder`](https://docs.rs/tauri/2.0.0/tauri/tray/struct.TrayIconBuilder.html)。

{{% /tab %}}

{{< /tabpane >}}
### 更换托盘图标

创建托盘时，你可以把应用图标用作托盘图标：

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { TrayIcon } from '@tauri-apps/api/tray';
import { defaultWindowIcon } from '@tauri-apps/api/app';

const options = {
  icon: await defaultWindowIcon(),
};

const tray = await TrayIcon.new(options);
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
  .icon(app.default_window_icon().unwrap().clone())
  .build(app)?;
```

{{% /tab %}}

{{< /tabpane >}}
### 添加菜单

要附加一个在托盘被点击时显示的菜单，你可以使用 `menu` 选项。

{{% alert title="注意" %}}
默认情况下，左键和右键点击都会显示菜单。

要阻止左键点击时弹出菜单，请调用 [`show_menu_on_left_click(false)`](https://docs.rs/tauri/latest/tauri/tray/struct.TrayIconBuilder.html#method.show_menu_on_left_click) Rust 函数，
或把 [`menuOnLeftClick`](https://tauri.app/reference/javascript/api/namespacetray/#properties-1) JavaScript 选项设为 `false`。
{{% /alert %}}

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { TrayIcon } from '@tauri-apps/api/tray';
import { Menu } from '@tauri-apps/api/menu';

const menu = await Menu.new({
  items: [
    {
      id: 'quit',
      text: 'Quit',
    },
  ],
});

const options = {
  menu,
  menuOnLeftClick: true,
};

const tray = await TrayIcon.new(options);
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri::{
  menu::{Menu, MenuItem},
  tray::TrayIconBuilder,
};

let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
let menu = Menu::with_items(app, &[&quit_i])?;

let tray = TrayIconBuilder::new()
  .menu(&menu)
  .show_menu_on_left_click(true)
  .build(app)?;
```

{{% /tab %}}

{{< /tabpane >}}
#### 监听菜单事件

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

在 JavaScript 中，你可以把菜单点击事件监听器直接附加到菜单项上：

- 使用共享的菜单点击处理函数

  ```javascript
  import { Menu } from '@tauri-apps/api/menu';

  function onTrayMenuClick(itemId) {
    // itemId === 'quit'
  }

  const menu = await Menu.new({
    items: [
      {
        id: 'quit',
        text: 'Quit',
        action: onTrayMenuClick,
      },
    ],
  });
  ```

- 使用专用的菜单点击处理函数

  ```javascript
  import { Menu } from '@tauri-apps/api/menu';

  const menu = await Menu.new({
    items: [
      {
        id: 'quit',
        text: 'Quit',
        action: () => {
          console.log('quit pressed');
        },
      },
    ],
  });
  ```

{{% /tab %}}

{{% tab header="Rust" %}}

使用 [`TrayIconBuilder::on_menu_event`](https://docs.rs/tauri/2.0.0/tauri/tray/struct.TrayIconBuilder.html#method.on_menu_event) 方法附加托盘菜单点击事件监听器：

```rust

TrayIconBuilder::new()
  .on_menu_event(|app, event| match event.id.as_ref() {
    "quit" => {
      println!("quit menu item was clicked");
      app.exit(0);
    }
    _ => {
      println!("menu item {:?} not handled", event.id);
    }
  })
```

{{% /tab %}}

{{< /tabpane >}}
### 监听托盘事件

托盘图标会为以下鼠标事件发出事件：

- click：光标收到单次左键、右键或中键点击时触发，其中包含鼠标按下是否已释放的信息
- Double click：光标收到双击左键、右键或中键时触发
- Enter：光标进入托盘图标区域时触发
- Move：光标在托盘图标区域内移动时触发
- Leave：光标离开托盘图标区域时触发

{{% alert title="注意" %}}
Linux：不支持。即使图标已显示，该事件也不会发出，右键仍会显示上下文菜单。
{{% /alert %}}

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { TrayIcon } from '@tauri-apps/api/tray';

const options = {
  action: (event) => {
    switch (event.type) {
      case 'Click':
        console.log(
          `mouse ${event.button} button pressed, state: ${event.buttonState}`
        );
        break;
      case 'DoubleClick':
        console.log(`mouse ${event.button} button pressed`);
        break;
      case 'Enter':
        console.log(
          `mouse hovered tray at ${event.rect.position.x}, ${event.rect.position.y}`
        );
        break;
      case 'Move':
        console.log(
          `mouse moved on tray at ${event.rect.position.x}, ${event.rect.position.y}`
        );
        break;
      case 'Leave':
        console.log(
          `mouse left tray at ${event.rect.position.x}, ${event.rect.position.y}`
        );
        break;
    }
  },
};

const tray = await TrayIcon.new(options);
```

关于事件负载的更多信息，见 [`TrayIconEvent`](https://tauri.app/reference/javascript/api/namespacetray/#trayiconevent)。

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri::{
    Manager,
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent}
};

TrayIconBuilder::new()
  .on_tray_icon_event(|tray, event| match event {
    TrayIconEvent::Click {
      button: MouseButton::Left,
      button_state: MouseButtonState::Up,
      ..
    } => {
      println!("left click pressed and released");
      // 在这个示例中，我们在托盘被点击时显示并聚焦主窗口
      let app = tray.app_handle();
      if let Some(window) = app.get_webview_window("main") {
        let _ = window.unminimize();
        let _ = window.show();
        let _ = window.set_focus();
      }
    }
    _ => {
      println!("unhandled event {event:?}");
    }
  })
```

关于事件类型的更多信息，见 [`TrayIconEvent`](https://docs.rs/tauri/2.0.0/tauri/tray/enum.TrayIconEvent.html)。

{{% /tab %}}

{{< /tabpane >}}
关于创建菜单（包括菜单项、子菜单和动态更新）的详细信息，请参阅[窗口菜单](../6-windowmenu/)文档。
