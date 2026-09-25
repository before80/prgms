+++
title = "5 窗口自定义"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/window-customization/](https://tauri.app/learn/window-customization/)

Tauri 提供了大量选项来自定义应用窗口的外观与感觉。你可以创建自定义标题栏、使用透明窗口、强制尺寸约束等等。

## 配置

有三种方式可以修改窗口配置：

- [通过 tauri.conf.json](https://tauri.app/reference/config/#windowconfig)
- [通过 JavaScript API](https://tauri.app/reference/javascript/api/namespacewindow/#window)
- [通过 Rust 中的 Window](https://docs.rs/tauri/2.0.0/tauri/window/struct.Window.html)

## 用法

- [创建自定义标题栏](#创建自定义标题栏)
- [（macOS）透明标题栏 + 自定义窗口背景色](#macos透明标题栏--自定义窗口背景色)

### 创建自定义标题栏

这些窗口特性的一种常见用法是创建自定义标题栏。下面这个简短的教程将带你完成该过程。

{{% alert title="注意" %}}
在 macOS 上，使用自定义标题栏也会失去系统提供的一些功能，例如[移动窗口或对齐窗口](https://support.apple.com/guide/mac-help/work-with-app-windows-mchlp2469/mac)。另一种既能自定义标题栏又能保留原生功能的方式，是把标题栏设为透明并设置窗口背景色。参见用法[（macOS）透明标题栏 + 自定义窗口背景色](#macos透明标题栏--自定义窗口背景色)。
{{% /alert %}}

#### tauri.conf.json

在你的 `tauri.conf.json` 中把 `decorations` 设为 `false`：

```json
"tauri": {
	"windows": [
		{
			"decorations": false
		}
	]
}
```

#### 权限

在能力（capability）文件中添加窗口权限。

默认情况下，所有插件命令都被阻止、无法访问。你必须在 `capabilities` 配置中定义权限列表。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../security/1-usingpluginpermissions/)。

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:window:default",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-toggle-maximize",
    "core:window:allow-start-dragging"
  ]
}
```

| 权限                                   | 说明                                                                                     |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `core:window:default`                        | 该插件的默认权限。其中包含 `core:window:allow-internal-toggle-maximize`。 |
| `core:window:allow-close`                    | 在没有预配置作用域的情况下启用 close 命令。                                     |
| `core:window:allow-minimize`                 | 在没有预配置作用域的情况下启用 minimize 命令。                                  |
| `core:window:allow-start-dragging`           | 在没有预配置作用域的情况下启用 start_dragging 命令。                            |
| `core:window:allow-toggle-maximize`          | 在没有预配置作用域的情况下启用 toggle_maximize 命令。                           |
| `core:window:allow-internal-toggle-maximize` | 在没有预配置作用域的情况下启用 internal_toggle_maximize 命令。                  |

#### CSS

添加这段 CSS 示例，让它固定在屏幕顶部，并为按钮设置样式：

```css
.titlebar {
  height: 30px;
  background: #329ea3;
  user-select: none;
  display: grid;
  grid-template-columns: auto max-content;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}
.titlebar > .controls {
  display: flex;
}
.titlebar button {
  appearance: none;
  padding: 0;
  margin: 0;
  border: none;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  background-color: transparent;
}
.titlebar button:hover {
  background: #5bbec3;
}
```

#### HTML

把它放到 `<body>` 标签的顶部：

```html
  <div data-tauri-drag-region></div>
  <div class="controls">
    <button id="titlebar-minimize" title="minimize">
      <!-- https://api.iconify.design/mdi:window-minimize.svg -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path fill="currentColor" d="M19 13H5v-2h14z" />
      </svg>
    </button>
    <button id="titlebar-maximize" title="maximize">
      <!-- https://api.iconify.design/mdi:window-maximize.svg -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path fill="currentColor" d="M4 4h16v16H4zm2 4v10h12V8z" />
      </svg>
    </button>
    <button id="titlebar-close" title="close">
      <!-- https://api.iconify.design/mdi:close.svg -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path
          fill="currentColor"
          d="M13.46 12L19 17.54V19h-1.46L12 13.46L6.46 19H5v-1.46L10.54 12L5 6.46V5h1.46L12 10.54L17.54 5H19v1.46z"
        />
      </svg>
    </button>
  </div>
</div>
```

注意你可能需要把其余内容向下移动，以免标题栏遮住它们。

{{% alert title="提示" %}}

在 Windows 上，如果你只是想要一个不需要自定义交互的标题栏，可以使用

```css
*[data-tauri-drag-region] {
  app-region: drag;
}
```

让标题栏支持触摸和手写笔输入。

{{% /alert %}}

#### JavaScript

使用这段代码让按钮生效：

```javascript
import { getCurrentWindow } from '@tauri-apps/api/window';

// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { getCurrentWindow } = window.__TAURI__.window;

const appWindow = getCurrentWindow();

document
  .getElementById('titlebar-minimize')
  ?.addEventListener('click', () => appWindow.minimize());
document
  .getElementById('titlebar-maximize')
  ?.addEventListener('click', () => appWindow.toggleMaximize());
document
  .getElementById('titlebar-close')
  ?.addEventListener('click', () => appWindow.close());
```

注意如果你使用基于 Rust 的前端，可以把上面的代码复制到 `index.html` 文件中的 `<script>` 元素里。

{{% alert title="注意" %}}
`data-tauri-drag-region` 只在直接应用它的元素上生效。如果你希望拖动行为也作用于子元素，需要给每个子元素单独添加它。

保留这种行为是为了让按钮、输入框之类的交互元素能正常工作。
{{% /alert %}}

### 手动实现 `data-tauri-drag-region`

对于需要自定义拖动行为的场景，你可以改为手动用 `window.startDragging` 添加事件监听器，而不使用 `data-tauri-drag-region`。

#### HTML

基于上一节的代码，我们去掉 `data-tauri-drag-region` 并添加一个 `id`：

```html
  <!-- ... -->
</div>
```

#### Javascript

为标题栏元素添加事件监听器：

```js
document.getElementById('titlebar')?.addEventListener('mousedown', (e) => {
  if (e.buttons === 1) {
    // 主（左）键
    e.detail === 2
      ? appWindow.toggleMaximize() // 双击时最大化
      : appWindow.startDragging(); // 否则开始拖动
  }
});
```

### （macOS）透明标题栏 + 自定义窗口背景色

我们将在 Rust 侧创建主窗口并修改它的背景色。

从 `tauri.conf.json` 文件中移除主窗口：

```json
"tauri": {
	"windows": [
		{
			"title": "Transparent Titlebar Window",
			"width": 800,
			"height": 600
		}
	],
}
```

把 `objc2-app-kit` crate 加入依赖，这样我们就能用它调用 macOS 原生 API：

```toml
objc2-app-kit = { version = "0.3.2", features = ["NSColor", "NSWindow", "objc2-core-foundation"] }
```

创建主窗口并修改它的背景色：

```rust
use tauri::{TitleBarStyle, WebviewUrl, WebviewWindowBuilder};

pub fn run() {
	tauri::Builder::default()
		.setup(|app| {
			let win_builder =
				WebviewWindowBuilder::new(app, "main", WebviewUrl::default())
					.title("Transparent Titlebar Window")
					.inner_size(800.0, 600.0);

			// 仅在为 macOS 构建时设置透明标题栏
			#[cfg(target_os = "macos")]
			let win_builder = win_builder.title_bar_style(TitleBarStyle::Transparent);

			let window = win_builder.build().unwrap();

			// 仅在为 macOS 构建时设置背景色
			#[cfg(target_os = "macos")]
			{
				use objc2_app_kit::{NSColor, NSWindow};

				let ns_window_ptr = window.ns_window().unwrap() as *mut NSWindow;
				let ns_window = unsafe { &*ns_window_ptr };
				let bg_color = NSColor::colorWithRed_green_blue_alpha(
					50.0 / 255.0,
					158.0 / 255.0,
					163.5 / 255.0,
					1.0,
				);
				ns_window.setBackgroundColor(Some(&bg_color));
			}

			Ok(())
		})
		.run(tauri::generate_context!())
		.expect("error while running tauri application");
}
```
