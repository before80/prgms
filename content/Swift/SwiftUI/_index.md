+++
title = "SwiftUI"
date = 2026-09-12T12:47:47+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui](https://developer.apple.com/documentation/swiftui)

# SwiftUI

在每一个平台上声明应用的用户界面与行为。

## 概述 {#Overview}

SwiftUI 提供用于声明应用界面的视图、控件和布局结构。框架提供事件处理器，把点按、手势和其他类型的输入传递给应用，并提供一些工具来管理数据从应用模型流向用户看到并与之交互的视图和控件的过程。

用 [App](https://developer.apple.com/documentation/swiftui/app) 协议定义应用结构，并用场景来填充它，场景中包含构成应用界面的各个视图。创建遵循 [View](https://developer.apple.com/documentation/swiftui/view) 协议的自定义视图，并把它们与 SwiftUI 的视图组合起来，用栈、列表等展示文本、图像和自定义形状。为内置视图和自己的视图应用强大的修饰符，自定义它们的渲染方式和交互行为。借助会随上下文与呈现方式自适应的视图和控件，在多个平台的 app 之间共享代码。

![Mac、iPad 和 iPhone 上 Landmarks 示例应用显示富士山景点的图像。](./images/landmarks-app-article-hero@2x.png)

你可以把 SwiftUI 视图与 [UIKit](https://developer.apple.com/documentation/uikit)、[AppKit](https://developer.apple.com/documentation/appkit)、[WatchKit](https://developer.apple.com/documentation/watchkit) 框架中的对象集成起来，从而进一步利用平台特有的能力。你也可以自定义 SwiftUI 的无障碍支持，并为不同的语言、国家或文化区域本地化应用的界面。

> 提示：如果你是 SwiftUI 新手，可以访问 [SwiftUI Pathway](https://developer.apple.com/swiftui/get-started/)。它汇集了教程、文章和示例项目，帮助你上手 SwiftUI。

### 精选示例 {#Featured-samples}

- [Landmarks：用 Liquid Glass 构建应用](essentials/1-LandmarksBuildingAnAppWithLiquidGlass/)
- [Wishlist：在 SwiftUI 应用中规划旅行](views/1-ViewFundamentals/1.2-WishlistPlanningTravelInASwiftuiApp/)
- [Destination Video](https://developer.apple.com/documentation/visionos/destination-video)
- [用 SwiftUI 构建基于文稿的应用](appstructure/5-Documents/5.4-BuildingADocumentBasedAppWithSwiftui/)

## 基础 {#Essentials}

- [采用 Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) —— 了解如何把这种新材质引入你的应用。
- [Develop in Swift](https://developer.apple.com/tutorials/develop-in-swift) —— Develop in Swift 教程面向任何想学习为 Apple 平台构建应用的人，介绍如何使用 Swift 和 Xcode 开发应用。
- [SwiftUI 更新](https://developer.apple.com/documentation/updates/swiftui) —— 了解 SwiftUI 的重要变更。
- [Landmarks：用 Liquid Glass 构建应用](essentials/1-LandmarksBuildingAnAppWithLiquidGlass/) —— 用系统提供的和自定义的 Liquid Glass 增强你的应用体验。

## 应用结构 {#App-structure}

- [应用组织](appstructure/1-AppOrganization/) —— 定义应用的入口点和顶层结构。
- [场景](appstructure/2-Scenes/) —— 声明构成应用各个部分的界面分组。
- [窗口](appstructure/3-Windows/) —— 在窗口或一组窗口中显示界面内容。
- [沉浸式空间](appstructure/4-ImmersiveSpaces/) —— 在人的周围环境中显示无边界的沉浸内容。
- [文稿](appstructure/5-Documents/) —— 让人们能够打开和管理文稿。
- [导航](appstructure/6-Navigation/) —— 让人们能在场景中应用视图层级的不同部分之间移动。
- [模态呈现](appstructure/7-ModalPresentations/) —— 在单独的视图中呈现内容，提供聚焦的交互。
- [工具栏](appstructure/8-Toolbars/) —— 为常用命令和控件提供即时访问入口。
- [搜索](appstructure/9-Search/) —— 让人们可以在应用中搜索文本或其他内容。
- [应用扩展](appstructure/10-AppExtensions/) —— 把应用的基本功能扩展到系统的其他部分，例如添加小组件。

## 数据与存储 {#Data-and-storage}

- [模型数据](datastorage/1-ModelData/) —— 管理驱动应用界面的数据。
- [环境值](datastorage/2-EnvironmentValues/) —— 使用环境在整个视图层级中共享数据。
- [偏好设置](datastorage/3-Preferences/) —— 把配置偏好从视图向上传递给容纳它的视图。
- [持久化存储](datastorage/4-PersistentStorage/) —— 存储数据，供应用多次会话之间使用。

## 视图 {#Views}

- [视图基础](views/1-ViewFundamentals/) —— 用视图层级定义应用的视觉元素。
- [视图配置](views/2-ViewConfiguration/) —— 调整层级中各视图的特征。
- [视图样式](views/3-ViewStyles/) —— 为不同类型的视图应用内置的和自定义的外观与行为。
- [动画](views/4-Animations/) —— 响应状态变化创建平滑的视觉更新。
- [文本输入与输出](views/5-TextInputAndOutput/) —— 显示格式化文本并获取用户输入的文本。
- [图像](views/6-Images/) —— 在应用界面中添加图像和符号。
- [控件与指示器](views/7-ControlsAndIndicators/) —— 显示数值并获取用户的选择。
- [菜单与命令](views/8-MenusAndCommands/) —— 以节省空间、依赖上下文的方式访问命令和控件。
- [形状](views/9-Shapes/) —— 用颜色、渐变或其他图案描边并填充内置和自定义形状。
- [绘图与图形](views/10-DrawingAndGraphics/) —— 用图形效果和自定义绘图增强视图。

## 视图布局 {#View-layout}

- [布局基础](viewlayout/1-LayoutFundamentals/) —— 在栈、网格等内置布局容器中排列视图。
- [布局调整](viewlayout/2-LayoutAdjustments/) —— 对对齐、间距、内边距等布局参数做细致调整。
- [自定义布局](viewlayout/3-CustomLayout/) —— 以自定义方式排列视图，并在不同布局类型之间创建动画过渡。
- [列表](viewlayout/4-Lists/) —— 显示结构化的、可滚动的信息列。
- [表格](viewlayout/5-Tables/) —— 显示按行和列排列的、可选择可排序的数据。
- [视图分组](viewlayout/6-ViewGroupings/) —— 在不同类型的用途驱动容器（如表单或控件组）中呈现视图。
- [滚动视图](viewlayout/7-ScrollViews/) —— 让人们能够滚动到当前显示区域放不下的内容。

## 事件处理 {#Event-handling}

- [手势](eventhandling/1-Gestures/) —— 定义从点按、点击、轻扫到细粒度手势的各种交互。
- [输入事件](eventhandling/2-InputEvents/) —— 响应来自键盘、Touch Bar 等硬件设备的输入。
- [剪贴板](eventhandling/3-Clipboard/) —— 让人们通过「拷贝」和「粘贴」命令移动或复制条目。
- [拖放](eventhandling/4-DragAndDrop/) —— 让人们把条目从一个位置拖到另一个位置来移动或复制它们。
- [焦点](eventhandling/5-Focus/) —— 确定并控制哪个可见对象响应用户交互。
- [系统事件](eventhandling/6-SystemEvents/) —— 响应打开 URL 之类的系统事件。

## 无障碍 {#Accessibility}

- [无障碍基础](accessibility/1-AccessibilityFundamentals/) —— 让 SwiftUI 应用对所有人可用，包括有身体障碍的人。
- [无障碍外观](accessibility/2-AccessibleAppearance/) —— 提升应用界面中内容的易读性。
- [无障碍控件](accessibility/3-AccessibleControls/) —— 改善对应用可执行操作的访问。
- [无障碍描述](accessibility/4-AccessibleDescriptions/) —— 描述界面元素，帮助人们理解它们代表什么。
- [无障碍导航](accessibility/5-AccessibleNavigation/) —— 让人们使用转子（rotor）导航到特定的界面元素。

## 框架集成 {#Framework-integration}

- [AppKit 集成](frameworkintegration/1-AppkitIntegration/) —— 在 SwiftUI 应用中加入 AppKit 视图，或者在 AppKit 应用中使用 SwiftUI 视图。
- [UIKit 集成](frameworkintegration/2-UikitIntegration/) —— 在 SwiftUI 应用中加入 UIKit 视图，或者在 UIKit 应用中使用 SwiftUI 视图。
- [WatchKit 集成](frameworkintegration/3-WatchkitIntegration/) —— 在 SwiftUI 应用中加入 WatchKit 视图，或者在 WatchKit 应用中使用 SwiftUI 视图。
- [技术专用视图](frameworkintegration/4-TechnologySpecificViews/) —— 使用其他 Apple 框架提供的 SwiftUI 视图。

## 工具支持 {#Tool-support}

- [Xcode 中的预览](views/1.3-PreviewsInXcode/) —— 为自定义视图生成动态、可交互的预览。
- [Xcode 资源库自定义](toolsupport/1-XcodeLibraryCustomization/) —— 在 Xcode 资源库中公开自定义视图和修饰符。
- [性能分析](toolsupport/2-PerformanceAnalysis/) —— 衡量并改进应用的响应能力。
