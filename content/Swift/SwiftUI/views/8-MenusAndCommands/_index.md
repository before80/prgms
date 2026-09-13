+++
title = "8 菜单与命令"
date = 2026-09-12T12:47:47+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/menus-and-commands](https://developer.apple.com/documentation/swiftui/menus-and-commands)

# 8 菜单与命令

以节省空间、依赖上下文的方式访问命令和控件。

## 概述 {#Overview}

用菜单为人们提供对常用命令的便捷访问。你可以用 [commands(content:)](https://developer.apple.com/documentation/swiftui/scene/commands(content:)) 场景修饰符向 macOS 或 iPadOS 应用的菜单栏添加条目，也可以用 [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) 视图修饰符创建在人们当前任务附近展开的上下文菜单。

![](./images/menus-and-commands-hero@2x.png)

把 [Menu](https://developer.apple.com/documentation/swiftui/menu) 实例嵌套在其他实例中，即可创建子菜单。用 [Divider](https://developer.apple.com/documentation/swiftui/divider) 视图在菜单元素之间创建分隔线。

关于设计指导，参见 Human Interface Guidelines 中的[菜单](https://developer.apple.com/design/human-interface-guidelines/menus)。

## 构建菜单栏 {#Building-a-menu-bar}

- [用 SwiftUI 构建并自定义菜单栏](../../appstructure/2-Scenes/2.1-BuildingAndCustomizingTheMenuBarWithSwiftui/) —— 为 iPadOS 和 macOS 构建原生菜单栏，提供无缝的跨平台体验。

## 创建菜单 {#Creating-a-menu}

- [用自适应控件填充 SwiftUI 菜单](8.1-PopulatingSwiftuiMenusWithAdaptiveControls/) —— 用控件填充菜单并直观地组织内容，改进你的应用。
- [Menu](https://developer.apple.com/documentation/swiftui/menu) —— 呈现操作菜单的控件。
- [menuStyle(_:)](https://developer.apple.com/documentation/swiftui/view/menustyle(_:)) —— 设置该视图内菜单的样式。

## 创建上下文菜单 {#Creating-context-menus}

- [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) —— 为视图添加上下文菜单。
- [contextMenu(menuItems:preview:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:preview:)) —— 为视图添加带自定义预览的上下文菜单。
- [contextMenu(forSelectionType:menu:primaryAction:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(forselectiontype:menu:primaryaction:)) —— 为视图添加基于条目的上下文菜单。

## 定义命令 {#Defining-commands}

- [commands(content:)](https://developer.apple.com/documentation/swiftui/scene/commands(content:)) —— 为场景添加命令。
- [commandsRemoved()](https://developer.apple.com/documentation/swiftui/scene/commandsremoved()) —— 移除被修改场景所定义的所有命令。
- [commandsReplaced(content:)](https://developer.apple.com/documentation/swiftui/scene/commandsreplaced(content:)) —— 用构建器中的命令替换被修改场景所定义的所有命令。
- [Commands](https://developer.apple.com/documentation/swiftui/commands) —— 遵循该协议的类型表示一组相关命令，可以通过 macOS 的主菜单或 iOS 的按键命令暴露给用户。
- [CommandMenu](https://developer.apple.com/documentation/swiftui/commandmenu) —— 命令菜单是独立、顶层的容器，用来放置执行相关应用专属命令的控件。
- [CommandGroup](https://developer.apple.com/documentation/swiftui/commandgroup) —— 你可以添加到已有命令菜单中的一组控件。
- [CommandsBuilder](https://developer.apple.com/documentation/swiftui/commandsbuilder) —— 从多表达式闭包构造命令集。与 `ContentBuilder` 一样，它支持闭包体中最多的十个表达式。
- [CommandGroupPlacement](https://developer.apple.com/documentation/swiftui/commandgroupplacement) —— 你可以把新命令组放在相对于它们的标准位置。

## 获取内置命令组 {#Getting-built-in-command-groups}

- [SidebarCommands](https://developer.apple.com/documentation/swiftui/sidebarcommands) —— 用于操作窗口侧边栏的内置命令集。
- [TextEditingCommands](https://developer.apple.com/documentation/swiftui/texteditingcommands) —— 用于搜索、编辑和转换文本选区的内置命令组。
- [TextFormattingCommands](https://developer.apple.com/documentation/swiftui/textformattingcommands) —— 用于转换应用于文本选区的样式的内置命令集。
- [ToolbarCommands](https://developer.apple.com/documentation/swiftui/toolbarcommands) —— 用于操作窗口工具栏的内置命令集。
- [ImportFromDevicesCommands](https://developer.apple.com/documentation/swiftui/importfromdevicescommands) —— 可以从附近设备导入内容的内置命令集。
- [InspectorCommands](https://developer.apple.com/documentation/swiftui/inspectorcommands) —— 用于操作检查器的内置命令集。
- [EmptyCommands](https://developer.apple.com/documentation/swiftui/emptycommands) —— 空的命令组。

## 显示菜单指示器 {#Showing-a-menu-indicator}

- [menuIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/menuindicator(_:)) —— 设置该视图内控件的菜单指示器可见性。
- [menuIndicatorVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/menuindicatorvisibility) —— 要应用到视图内控件的菜单指示器可见性。

## 配置菜单关闭行为 {#Configuring-menu-dismissal}

- [menuActionDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/menuactiondismissbehavior(_:)) —— 告诉菜单在执行动作后是否关闭。
- [MenuActionDismissBehavior](https://developer.apple.com/documentation/swiftui/menuactiondismissbehavior) —— 菜单关闭行为的选项集合。

## 设置偏好顺序 {#Setting-a-preferred-order}

- [menuOrder(_:)](https://developer.apple.com/documentation/swiftui/view/menuorder(_:)) —— 设置从该视图呈现的菜单中条目的偏好顺序。
- [menuOrder](https://developer.apple.com/documentation/swiftui/environmentvalues/menuorder) —— 从该视图呈现的菜单中条目的偏好顺序。
- [MenuOrder](https://developer.apple.com/documentation/swiftui/menuorder) —— 菜单呈现其内容的顺序。

## 已弃用的类型 {#Deprecated-types}

- [MenuButton](https://developer.apple.com/documentation/swiftui/menubutton) —— 按下时显示包含一组选项的菜单的按钮。
- [PullDownButton](https://developer.apple.com/documentation/swiftui/pulldownbutton)
- [ContextMenu](https://developer.apple.com/documentation/swiftui/contextmenu) —— 把视图作为菜单项在上下文菜单中呈现的容器。
