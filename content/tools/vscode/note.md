+++
title = "个人笔记"
date = 2026-11-06T18:54:58+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++





## 新开标签

​	点击资源管理器中的文件名时，是【替换当前标签】还是【新开标签】？

​	进入设置，输入：`workbench.editor.enablePreview`

​	**去掉勾选**！

Controls whether preview mode is used when editors open. There is a maximum of one preview mode editor per editor group. This editor displays its filename in italics on its tab or title label and in the Open Editors view. Its contents will be replaced by the next editor opened in preview mode. Making a change in a preview mode editor will persist it, as will a double-click on its label, or the 'Keep Open' option in its label context menu. Opening a file from Explorer with a double-click persists its editor immediately.

​	控制在编辑器打开时是否使用预览模式。每个编辑器组最多只能有一个预览模式编辑景。此编辑景在其选项卡或标题标签和”打开编辑器“视图中以斜体显示其文件名。其内容将替换为在预览模式下打开的下一个编辑器。在预览模式编辑器中进行更改将保留它，就像双击其标签或其标签上下文菜单中的“保持打开“选项一样。通过双击从资源管理景打开文件会立即保留其编辑器。



Controls whether editors remain in preview when a code navigation is started from them. Preview editors do not stay open, and are reused until explicitly set to be kept open (via double-click or editing). This value is ignored when Workbench › Editor: Show Tabs is not set to multiple.

​	控制当从编辑器开始进行代码导航时，编辑器是否保持为预览状态。预览编辑器不会保持打开状态，在将其显式设置为保持打开（通过双击或编辑）前将会重用。如果未将 `Workbench> Editor:Show Tabs` 设置为 `multiple`，则会忽略此值。



Controls whether editors opened from Quick Open show as preview editors. Preview editors do not stay open, and are reused until explicitly set to be kept open (via double-click or editing). When enabled, hold Ctrl before selection to open an editor as a non-preview. This value is ignored when Workbench › Editor: Show Tabs is not set to multiple.

​	控制通过 `Quick Open` 打开的编辑器是否显示为预览编辑器。预览编辑器不会保持打开状态，在将其显式设置为保持打开（通过双击或编辑）前将会重用。启用后，在选择前按住 `Ctrl`可在非预览模式下打开编辑器。如果未将 `Workbench，Editor: Show Tabs `设置为 `multiple`，则会忽略此值。



## 紧凑标签

​	进入设置，输入：`window.density.editorTabHeight`

​	选择：`compact`

​	

​	控制编辑器选项卡的高度。当 Workbench, Editor: Show Tabs 未设置为 multiple时，也适用于标题控件栏。



## 隐藏编辑器icon

​	去掉icon可以在一行上显示更多打开的文件名。

​	进入设置，输入：`workbench.editor.showIncons`

​	**去掉勾选**！

Controls whether opened editors should show with an icon or not. This requires a file icon theme to be enabled as well.

​	控制打开的编辑器是否应该显示图标。这还需要启用文件图标主题。



设置编辑区字体和字号

