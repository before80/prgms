+++
title = "10 应用扩展"
date = 2026-09-12T12:47:47+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/app-extensions](https://developer.apple.com/documentation/swiftui/app-extensions)

# 10 应用扩展

把应用的基本功能扩展到系统的其他部分，例如通过添加小组件。

## 概述 {#Overview}

把 SwiftUI 与 [WidgetKit](https://developer.apple.com/documentation/widgetkit) 结合使用，为你的应用添加小组件。

![](./images/app-extensions-hero@2x.png)

小组件让你可以快速访问应用中的相关内容。定义一个遵循 [Widget](https://developer.apple.com/documentation/swiftui/widget) 协议的结构体，并为该小组件声明视图层级。小组件内部的视图和其他 SwiftUI 视图一样，使用视图修饰符来配置，只是还会用到少数小组件专用的修饰符。

关于设计指导，参见 Human Interface Guidelines 中的[小组件](https://developer.apple.com/design/human-interface-guidelines/widgets)。

## 创建小组件 {#Creating-widgets}

- [用 WidgetKit 和 SwiftUI 构建小组件](https://developer.apple.com/documentation/widgetkit/building-widgets-using-widgetkit-and-swiftui) —— 创建小组件，在主屏幕上显示应用内容，并通过自定义意图提供用户可配置的设置。
- [创建小组件扩展](https://developer.apple.com/documentation/widgetkit/creating-a-widget-extension) —— 在各种设备上以便捷、信息丰富的小组件显示应用内容。
- [让小组件保持最新](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date) —— 规划小组件的时间线，用动态视图显示及时、相关的信息，并在情况变化时更新时间线。
- [制作可配置的小组件](https://developer.apple.com/documentation/widgetkit/making-a-configurable-widget) —— 通过向项目加入自定义应用意图，让人们可以自定义自己的小组件。
- [Widget](https://developer.apple.com/documentation/swiftui/widget) —— 在主屏幕或通知中心显示的小组件的配置与内容。
- [WidgetBundle](https://developer.apple.com/documentation/swiftui/widgetbundle) —— 用于从单个小组件扩展中公开多个小组件的容器。
- [LimitedAvailabilityConfiguration](https://developer.apple.com/documentation/swiftui/limitedavailabilityconfiguration) —— 类型擦除的小组件配置。
- [WidgetConfiguration](https://developer.apple.com/documentation/swiftui/widgetconfiguration) —— 描述小组件内容的类型。
- [EmptyWidgetConfiguration](https://developer.apple.com/documentation/swiftui/emptywidgetconfiguration) —— 空的小组件配置。

## 组合控制小组件 {#Composing-control-widgets}

- [ControlWidget](https://developer.apple.com/documentation/swiftui/controlwidget) —— 在控制中心、锁定屏幕和操作按钮等系统空间中显示的控制小组件的配置与内容。
- [ControlWidgetConfiguration](https://developer.apple.com/documentation/swiftui/controlwidgetconfiguration) —— 描述控制小组件内容的类型。
- [EmptyControlWidgetConfiguration](https://developer.apple.com/documentation/swiftui/emptycontrolwidgetconfiguration) —— 空的控制小组件配置。
- [ControlWidgetConfigurationBuilder](https://developer.apple.com/documentation/swiftui/controlwidgetconfigurationbuilder) —— 用于构造控制小组件 body 的自定义属性。
- [ControlWidgetTemplate](https://developer.apple.com/documentation/swiftui/controlwidgettemplate) —— 描述控制小组件内容的类型。
- [EmptyControlWidgetTemplate](https://developer.apple.com/documentation/swiftui/emptycontrolwidgettemplate) —— 空的控制小组件模板。
- [ControlWidgetTemplateBuilder](https://developer.apple.com/documentation/swiftui/controlwidgettemplatebuilder) —— 用于构造控制小组件模板 body 的自定义属性。
- [controlWidgetActionHint(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetactionhint(_:)) —— 由被修改的标签所描述的控制项的动作提示。
- [controlWidgetStatus(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetstatus(_:)) —— 由被修改的标签所描述的控制项的状态。

## 为小组件添加标签 {#Labeling-a-widget}

- [widgetLabel(_:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(_:)) —— 返回一个本地化文本标签，在附属系列小组件的主 SwiftUI 视图之外显示附加内容。
- [widgetLabel(label:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(label:)) —— 创建一个标签，用于在附属系列小组件的主 SwiftUI 视图之外显示附加内容。

## 设置小组件分组样式 {#Styling-a-widget-group}

- [accessoryWidgetGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/accessorywidgetgroupstyle(_:)) —— 可应用于 `AccessoryWidgetGroup` 的视图修饰符，用于指定这三个内容视图将被遮罩成的形状。`style` 的值设为 `.automatic`，默认即 `.circular`。

## 控制强调分组 {#Controlling-the-accented-group}

- [widgetAccentable(_:)](https://developer.apple.com/documentation/swiftui/view/widgetaccentable(_:)) —— 把该视图及其所有子视图加入强调分组。

## 管理在灵动岛中的放置 {#Managing-placement-in-the-Dynamic-Island}

- [dynamicIsland(verticalPlacement:)](https://developer.apple.com/documentation/swiftui/view/dynamicisland(verticalplacement:)) —— 指定出现在灵动岛中的展开式实时活动视图的垂直放置位置。
