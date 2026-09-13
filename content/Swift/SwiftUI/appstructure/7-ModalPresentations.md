+++
title = "7 模态呈现"
date = 2026-09-12T12:47:47+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/modal-presentations](https://developer.apple.com/documentation/swiftui/modal-presentations)

# 7 模态呈现

在单独的视图中呈现内容，提供聚焦的交互。

## 概述 {#Overview}

为了聚焦于一个重要的、范围有限的任务，你会显示一种模态呈现，例如提醒框、弹出视图（popover）、表单（sheet）或确认对话框。

![](./images/modal-presentations-hero@2x.png)

在 SwiftUI 中，你用一个视图修饰符来创建模态呈现，该修饰符定义了呈现的外观，以及 SwiftUI 在什么条件下呈现它。SwiftUI 会检测条件的变化，并为你完成呈现。由于你为触发呈现的条件提供了一个 [Binding](https://developer.apple.com/documentation/swiftui/binding)，SwiftUI 就能在用户关闭呈现时重置底层值。

关于设计指导，参见 Human Interface Guidelines 中的[模态](https://developer.apple.com/design/human-interface-guidelines/modality)。

## 配置对话框 {#Configuring-a-dialog}

- [DialogSeverity](https://developer.apple.com/documentation/swiftui/dialogseverity) —— 提醒框或确认对话框的严重程度。

## 显示表单、全屏封面或弹出视图 {#Showing-a-sheet-cover-or-popover}

- [sheet(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(ispresented:ondismiss:content:)) —— 当你提供的布尔值绑定为 true 时呈现一个表单。
- [sheet(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(item:ondismiss:content:)) —— 用给定条目作为表单内容的数据源来呈现表单。
- [fullScreenCover(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(ispresented:ondismiss:content:)) —— 当你提供的布尔值绑定为 true 时，呈现一个尽可能覆盖整个屏幕的模态视图。
- [fullScreenCover(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(item:ondismiss:content:)) —— 用你提供的绑定作为表单内容的数据源，呈现一个尽可能覆盖整个屏幕的模态视图。
- [popover(item:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(item:attachmentanchor:arrowedge:content:)) —— 用给定条目作为弹出视图内容的数据源来呈现弹出视图。
- [popover(isPresented:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(ispresented:attachmentanchor:arrowedge:content:)) —— 当给定条件为 true 时呈现弹出视图。
- [PopoverAttachmentAnchor](https://developer.apple.com/documentation/swiftui/popoverattachmentanchor) —— 弹出视图的附着锚点。

## 适配呈现大小 {#Adapting-a-presentation-size}

- [presentationCompactAdaptation(horizontal:vertical:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(horizontal:vertical:)) —— 指定呈现如何适配水平与垂直紧凑尺寸类别。
- [presentationCompactAdaptation(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(_:)) —— 指定呈现如何适配紧凑尺寸类别。
- [PresentationAdaptation](https://developer.apple.com/documentation/swiftui/presentationadaptation) —— 把呈现适配到不同尺寸类别的策略。
- [presentationSizing(_:)](https://developer.apple.com/documentation/swiftui/view/presentationsizing(_:)) —— 设置所在呈现的大小。
- [PresentationSizing](https://developer.apple.com/documentation/swiftui/presentationsizing) —— 定义呈现内容大小的类型，以及呈现大小如何随其内容大小变化而调整。
- [PresentationSizingRoot](https://developer.apple.com/documentation/swiftui/presentationsizingroot) —— 提供给呈现、且带有已定义呈现大小的视图代理。
- [PresentationSizingContext](https://developer.apple.com/documentation/swiftui/presentationsizingcontext) —— 关于某个呈现的上下文信息。

## 配置表单的高度与放置 {#Configuring-a-sheets-height-and-placement}

- [presentationDetents(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:)) —— 设置所在表单可用的停靠高度。
- [presentationDetents(_:selection:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:selection:)) —— 设置所在表单可用的停靠高度，并让你以编程方式控制当前选中的停靠高度。
- [presentationContentInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcontentinteraction(_:)) —— 配置呈现上轻扫手势的行为。
- [presentationDragIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdragindicator(_:)) —— 设置表单顶部拖动指示器的可见性。
- [PresentationDetent](https://developer.apple.com/documentation/swiftui/presentationdetent) —— 表示表单自然停留高度的类型。
- [CustomPresentationDetent](https://developer.apple.com/documentation/swiftui/custompresentationdetent) —— 带计算高度的自定义停靠高度定义。
- [PresentationContentInteraction](https://developer.apple.com/documentation/swiftui/presentationcontentinteraction) —— 可用来影响呈现如何响应轻扫手势的行为。
- [presentationPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)) —— 设置呈现相对呈现它的视图的放置位置。
- [PresentationPlacement](https://developer.apple.com/documentation/swiftui/presentationplacement) —— 呈现相对呈现它的视图的放置位置。

## 设置表单及其背景的样式 {#Styling-a-sheet-and-its-background}

- [presentationCornerRadius(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcornerradius(_:)) —— 请求呈现使用指定的圆角半径。
- [presentationBackground(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(_:)) —— 用形状样式设置所在表单的呈现背景。
- [presentationBackground(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(alignment:content:)) —— 把所在表单的呈现背景设置为自定义视图。
- [presentationBackgroundInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackgroundinteraction(_:)) —— 控制人们能否与呈现背后的视图交互。
- [PresentationBackgroundInteraction](https://developer.apple.com/documentation/swiftui/presentationbackgroundinteraction) —— 呈现背后的视图可用的交互种类。

## 呈现提醒框 {#Presenting-an-alert}

- [AlertScene](https://developer.apple.com/documentation/swiftui/alertscene) —— 把自身渲染为独立提醒对话框的场景。
- [alert(_:isPresented:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:)) —— 当给定条件为 true 时呈现提醒框，标题使用本地化字符串资源。
- [alert(_:isPresented:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:)) —— 用给定数据生成提醒框内容、并用本地化字符串资源作为标题来呈现提醒框。
- [alert(_:item:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:)) —— 用给定数据生成提醒框内容、并用文本视图作为标题来呈现提醒框。
- [alert(error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:)) —— 当存在错误时呈现提醒框。
- [alert(isPresented:error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:)) —— 当存在错误时呈现提醒框。
- [alert(_:isPresented:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:message:)) —— 当给定条件为 true 时呈现带消息的提醒框，标题使用本地化字符串资源。
- [alert(_:isPresented:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:message:)) —— 用给定数据生成提醒框内容、并用本地化字符串资源作为标题，呈现带消息的提醒框。
- [alert(_:item:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:message:)) —— 用给定数据生成提醒框内容、并用本地化字符串键作为标题，呈现带消息的提醒框。
- [alert(error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:message:)) —— 当存在错误时呈现带消息的提醒框。
- [alert(isPresented:error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:message:)) —— 当存在错误时呈现带消息的提醒框。

## 为操作获取确认 {#Getting-confirmation-for-an-action}

- [confirmationDialog(_:isPresented:titleVisibility:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:)) —— 当给定条件为 true 时呈现确认对话框，标题使用本地化字符串资源。
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:)) —— 用数据生成对话框内容、并用本地化字符串资源作为标题来呈现确认对话框。
- [dismissalConfirmationDialog(_:shouldPresent:actions:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:)) —— 当关闭动作被触发时呈现确认对话框。

## 显示带消息的确认对话框 {#Showing-a-confirmation-dialog-with-a-message}

- [confirmationDialog(_:isPresented:titleVisibility:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:message:)) —— 当给定条件为 true 时呈现带消息的确认对话框，标题使用本地化字符串资源。
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:message:)) —— 用数据生成对话框内容、并用本地化字符串资源作为标题，呈现带消息的确认对话框。
- [dismissalConfirmationDialog(_:shouldPresent:actions:message:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:message:)) —— 当关闭动作被触发时呈现确认对话框。

## 配置对话框 {#Configuring-a-dialog}

- [dialogIcon(_:)](https://developer.apple.com/documentation/swiftui/view/dialogicon(_:)) —— 配置该视图内对话框所使用的图标。
- [dialogIcon(_:)](https://developer.apple.com/documentation/swiftui/scene/dialogicon(_:)) —— 配置提醒框所使用的图标。
- [dialogSeverity(_:)](https://developer.apple.com/documentation/swiftui/view/dialogseverity(_:))
- [dialogSeverity(_:)](https://developer.apple.com/documentation/swiftui/scene/dialogseverity(_:)) —— 设置提醒框的严重程度。
- [dialogSuppressionToggle(isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(issuppressed:)) —— 让用户可以抑制在 `self` 内呈现的对话框和提醒框，在 macOS 上带默认的抑制消息。其他平台不使用。
- [dialogSuppressionToggle(isSuppressed:)](https://developer.apple.com/documentation/swiftui/scene/dialogsuppressiontoggle(issuppressed:)) —— 让用户可以用自定义的抑制消息抑制提醒框。
- [dialogSuppressionToggle(_:isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(_:issuppressed:)) —— 让用户可以抑制在 `self` 内呈现的对话框和提醒框，在 macOS 上带自定义的抑制消息。其他平台不使用。
- [dialogSuppressionToggle(_:isSuppressed:)](https://developer.apple.com/documentation/swiftui/scene/dialogsuppressiontoggle(_:issuppressed:)) —— 让用户可以用自定义的抑制消息抑制提醒框。
- [dialogPreventsAppTermination(_:)](https://developer.apple.com/documentation/swiftui/view/dialogpreventsapptermination(_:)) —— 提醒框或确认对话框是否阻止系统或应用退出菜单项终止应用。

## 导出到文件 {#Exporting-to-file}

- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把某个 `WritableDocument` 导出到磁盘上的文件。
- [fileExporter(isPresented:documents:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttypes:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把一组遵循 `WritableDocument` 的对象导出到磁盘上的文件。
- [fileExporter(isPresented:item:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:item:contenttypes:defaultfilename:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把某个 `Transferable` 条目导出到磁盘上的文件。
- [fileExporter(isPresented:items:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:items:contenttypes:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把一组 `Transferable` 条目导出到磁盘上的文件。
- [fileExporterFilenameLabel(_:)](https://developer.apple.com/documentation/swiftui/view/fileexporterfilenamelabel(_:)) —— 在 macOS 上，为 `fileExporter` 配置文件名输入框的标签。

## 从文件导入 {#Importing-from-file}

- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)) —— 呈现系统对话框，允许用户导入多个文件。
- [fileImporter(isPresented:allowedContentTypes:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:oncompletion:)) —— 呈现系统对话框，允许用户导入一个已有文件。
- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户导入多个文件。

## 移动文件 {#Moving-a-file}

- [fileMover(isPresented:file:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:)) —— 呈现系统对话框，允许用户把已有文件移动到新位置。
- [fileMover(isPresented:files:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:)) —— 呈现系统对话框，允许用户把一组已有文件移动到新位置。
- [fileMover(isPresented:file:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把已有文件移动到新位置。
- [fileMover(isPresented:files:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把一组已有文件移动到新位置。

## 配置文件对话框 {#Configuring-a-file-dialog}

- [fileDialogBrowserOptions(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogbrowseroptions(_:)) —— 在 macOS 上，配置 `fileExporter`、`fileImporter` 或 `fileMover`，提供更精细的 URL 搜索体验：包含或排除隐藏文件、允许按标签搜索等。
- [fileDialogConfirmationLabel(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogconfirmationlabel(_:)) —— 在 macOS 上，为 `fileExporter`、`fileImporter` 或 `fileMover` 配置自定义的确认按钮标签。
- [fileDialogCustomizationID(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogcustomizationid(_:)) —— 在 macOS 上，配置 `fileExporter`、`fileImporter` 或 `fileMover` 以持久保存并恢复文件对话框配置。
- [fileDialogDefaultDirectory(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogdefaultdirectory(_:)) —— 配置 `fileExporter`、`fileImporter` 或 `fileMover` 以指定的默认目录打开。
- [fileDialogImportsUnresolvedAliases(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogimportsunresolvedaliases(_:)) —— 在 macOS 上，配置用户选择别名时 `fileExporter`、`fileImporter` 或 `fileMover` 的行为。
- [fileDialogMessage(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogmessage(_:)) —— 在 macOS 上，为 `fileExporter`、`fileImporter` 或 `fileMover` 配置一条呈现给用户的自定义消息，类似标题。
- [fileDialogURLEnabled(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogurlenabled(_:)) —— 在 macOS 上，配置 `fileImporter` 或 `fileMover` 有条件地禁用所呈现的 URL。
- [FileDialogBrowserOptions](https://developer.apple.com/documentation/swiftui/filedialogbrowseroptions) —— 文件对话框呈现文件系统的方式。

## 呈现检查器 {#Presenting-an-inspector}

- [inspector(isPresented:content:)](https://developer.apple.com/documentation/swiftui/view/inspector(ispresented:content:)) —— 在视图层级中应用修饰符的位置插入一个检查器。
- [inspectorColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(_:)) —— 当检查器作为后置栏呈现时，为包含该视图的检查器设置固定的偏好宽度。
- [inspectorColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(min:ideal:max:)) —— 在后置栏呈现中为检查器设置灵活的偏好宽度。

## 关闭呈现 {#Dismissing-a-presentation}

- [isPresented](https://developer.apple.com/documentation/swiftui/environmentvalues/ispresented) —— 表示与该环境关联的视图当前是否已呈现的布尔值。
- [dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss) —— 关闭当前呈现的动作。
- [DismissAction](https://developer.apple.com/documentation/swiftui/dismissaction) —— 关闭呈现的动作。
- [interactiveDismissDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/interactivedismissdisabled(_:)) —— 有条件地阻止通过交互关闭弹出视图、表单和检查器等呈现。

## 已弃用 {#Deprecated}

- [Alert](https://developer.apple.com/documentation/swiftui/alert) —— 提醒框呈现的表示形式。
- [ActionSheet](https://developer.apple.com/documentation/swiftui/actionsheet) —— 操作表单呈现的表示形式。
- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:)) —— 呈现系统对话框，用于把存储在值类型（如结构体）中的文稿导出到磁盘上的文件。
- [fileExporter(isPresented:documents:contentType:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttype:oncompletion:)) —— 呈现系统对话框，用于把一组值类型文稿导出到磁盘上的文件。
- [fileExporter(isPresented:document:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttypes:defaultfilename:oncompletion:oncancellation:)) —— 呈现系统对话框，允许用户把某个 `FileDocument` 导出到磁盘上的文件。
