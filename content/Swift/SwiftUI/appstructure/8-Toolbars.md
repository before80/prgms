+++
title = "8 工具栏"
date = 2026-09-12T12:47:47+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/toolbars](https://developer.apple.com/documentation/swiftui/toolbars)

# 8 工具栏

为常用命令和控件提供即时访问入口。

## 概述 {#Overview}

依据平台和上下文的不同，系统可能把工具栏放在应用内容的上方或下方。

![](./images/toolbars-hero@2x.png)

通过把 [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) 视图修饰符应用到应用中的某个视图上，为工具栏添加条目。你也可以用视图修饰符配置工具栏，例如用 [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) 修饰符设置工具栏的可见性。

关于设计指导，参见 Human Interface Guidelines 中的[工具栏](https://developer.apple.com/design/human-interface-guidelines/toolbars)。

## 填充工具栏 {#Populating-a-toolbar}

- [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) —— 用指定的条目填充工具栏或导航栏。
- [ToolbarItem](https://developer.apple.com/documentation/swiftui/toolbaritem) —— 表示可以放进工具栏或导航栏的条目的模型。
- [ToolbarItemGroup](https://developer.apple.com/documentation/swiftui/toolbaritemgroup) —— 表示可以放进工具栏或导航栏的一组 `ToolbarItem` 的模型。
- [ToolbarItemPlacement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement) —— 定义工具栏项放置位置的结构体。
- [toolbarOverflowMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbaroverflowmenu(content:)) —— 配置工具栏的溢出菜单。
- [ToolbarOverflowMenu](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu) —— 工具栏的溢出菜单。
- [ToolbarContent](https://developer.apple.com/documentation/swiftui/toolbarcontent) —— 遵循该协议的类型表示可以放在工具栏中各个位置的条目。
- [ToolbarContentBuilder](https://developer.apple.com/documentation/swiftui/toolbarcontentbuilder) —— 从多表达式闭包构造工具栏项集合。
- [ToolbarSpacer](https://developer.apple.com/documentation/swiftui/toolbarspacer) —— 工具栏中的标准间隔项。
- [DefaultToolbarItem](https://developer.apple.com/documentation/swiftui/defaulttoolbaritem) —— 表示某个系统组件的工具栏项。

## 填充可自定义的工具栏 {#Populating-a-customizable-toolbar}

- [toolbar(id:content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(id:content:)) —— 用指定的条目填充工具栏或导航栏，并允许用户自定义。
- [toolbarItemHidden(_:)](https://developer.apple.com/documentation/swiftui/view/toolbaritemhidden(_:)) —— 在控件组工具栏项中隐藏某个视图。
- [CustomizableToolbarContent](https://developer.apple.com/documentation/swiftui/customizabletoolbarcontent) —— 遵循该协议的类型表示可以放在可自定义工具栏中各个位置的条目。
- [ToolbarCustomizationBehavior](https://developer.apple.com/documentation/swiftui/toolbarcustomizationbehavior) —— 可自定义工具栏内容的自定义行为。
- [ToolbarCustomizationOptions](https://developer.apple.com/documentation/swiftui/toolbarcustomizationoptions) —— 影响可自定义工具栏内容默认自定义行为的选项。
- [SearchToolbarBehavior](https://developer.apple.com/documentation/swiftui/searchtoolbarbehavior) —— 搜索框在工具栏中的行为。

## 移除默认条目 {#Removing-default-items}

- [toolbar(removing:)](https://developer.apple.com/documentation/swiftui/view/toolbar(removing:)) —— 移除默认存在的工具栏项
- [ToolbarDefaultItemKind](https://developer.apple.com/documentation/swiftui/toolbardefaultitemkind) —— `View` 默认添加的工具栏项的种类。

## 设置工具栏可见性 {#Setting-toolbar-visibility}

- [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) —— 指定由 SwiftUI 管理的某个栏的可见性。
- [toolbarVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarvisibility(_:for:)) —— 指定由 SwiftUI 管理的某个栏的可见性。
- [toolbarBackgroundVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackgroundvisibility(_:for:)) —— 指定由 SwiftUI 管理的某个栏上背景的偏好可见性。
- [ToolbarPlacement](https://developer.apple.com/documentation/swiftui/toolbarplacement) —— 工具栏的放置位置。
- [ContentToolbarPlacement](https://developer.apple.com/documentation/swiftui/contenttoolbarplacement)

## 指定工具栏内容的角色 {#Specifying-the-role-of-toolbar-content}

- [toolbarRole(_:)](https://developer.apple.com/documentation/swiftui/view/toolbarrole(_:)) —— 为填充工具栏的内容配置语义角色。
- [ToolbarRole](https://developer.apple.com/documentation/swiftui/toolbarrole) —— 填充工具栏的内容的用途。

## 设置工具栏样式 {#Styling-a-toolbar}

- [toolbarBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackground(_:for:)) —— 指定由 SwiftUI 管理的某个栏背景的偏好形状样式。
- [toolbarColorScheme(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarcolorscheme(_:for:)) —— 指定由 SwiftUI 管理的某个栏的偏好配色方案。
- [toolbarForegroundStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarforegroundstyle(_:for:)) —— 指定由 SwiftUI 管理的各个栏的偏好前景样式。
- [windowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarstyle(_:)) —— 设置该场景内所定义工具栏的样式。
- [WindowToolbarStyle](https://developer.apple.com/documentation/swiftui/windowtoolbarstyle) —— 对窗口工具栏外观与行为的规范说明。
- [toolbarLabelStyle](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarlabelstyle) —— 要应用于工具栏内各控件的标签样式。
- [ToolbarLabelStyle](https://developer.apple.com/documentation/swiftui/toolbarlabelstyle) —— 工具栏的标签样式。
- [SpacerSizing](https://developer.apple.com/documentation/swiftui/spacersizing) —— 定义间隔元素应如何确定自身大小的类型。

## 配置工具栏标题显示模式 {#Configuring-the-toolbar-title-display-mode}

- [toolbarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/toolbartitledisplaymode(_:)) —— 为该视图配置工具栏标题显示模式。
- [ToolbarTitleDisplayMode](https://developer.apple.com/documentation/swiftui/toolbartitledisplaymode) —— 定义工具栏标题行为的类型。

## 设置工具栏标题菜单 {#Setting-the-toolbar-title-menu}

- [toolbarTitleMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbartitlemenu(content:)) —— 配置工具栏的标题菜单。
- [ToolbarTitleMenu](https://developer.apple.com/documentation/swiftui/toolbartitlemenu) —— 工具栏的标题菜单。

## 创建装饰件 {#Creating-an-ornament}

- [ornament(visibility:attachmentAnchor:contentAlignment:ornament:)](https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)) —— 呈现一个装饰件。
- [OrnamentAttachmentAnchor](https://developer.apple.com/documentation/swiftui/ornamentattachmentanchor) —— 装饰件的附着锚点。

## 控制条目可见性 {#Controlling-item-visibility}

- [visibilityPriority(_:)](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)) —— 定义某个工具栏项的可见性优先级。
- [ToolbarItemVisibilityPriority](https://developer.apple.com/documentation/swiftui/toolbaritemvisibilitypriority) —— 定义工具栏项可见性优先级的值。

## 最小化工具栏 {#Minimizing-a-toolbar}

- [toolbarMinimizationBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:)) —— 为指定的栏设置最小化行为。
- [ToolbarMinimizationBehavior](https://developer.apple.com/documentation/swiftui/toolbarminimizationbehavior) —— 工具栏的最小化行为。
- [toolbarMinimizationRestoration(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationrestoration(_:for:)) —— 为指定的栏设置最小化期间的恢复行为。
- [ToolbarMinimizationRestoration](https://developer.apple.com/documentation/swiftui/toolbarminimizationrestoration) —— 工具栏最小化期间的恢复行为。
- [toolbarMinimizationSafeAreaAdjustment(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationsafeareaadjustment(_:for:)) —— 为指定的栏设置最小化期间的安全区域调整。
- [ToolbarMinimizationSafeAreaAdjustment](https://developer.apple.com/documentation/swiftui/toolbarminimizationsafeareaadjustment) —— 工具栏最小化期间的安全区域调整。
