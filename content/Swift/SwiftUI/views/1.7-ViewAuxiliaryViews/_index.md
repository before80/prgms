+++
title = "1.7 辅助视图修饰符"
date = 2026-09-12T12:47:47+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/view-auxiliary-views](https://developer.apple.com/documentation/swiftui/view-auxiliary-views)

# 1.7 辅助视图修饰符

添加并配置工具栏、上下文菜单之类的辅助视图。

## 概述 {#Overview}

用这些修饰符管理呈现上下文相关控件和信息的辅助视图。例如，你可以向导航栏添加标题和按钮、管理状态栏、创建上下文菜单，以及为许多不同种类的视图添加角标。

## 导航标题 {#Navigation-titles}

- [配置应用的导航标题](1.7.1-ConfigureYourAppsNavigationTitles/) —— 用导航标题显示界面当前的导航状态。
- [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:)) —— 用本地化字符串资源为该视图配置用于导航的标题。
- [navigationSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsubtitle(_:)) —— 用本地化字符串资源为该视图配置用于导航的副标题。

## 导航标题配置 {#Navigation-title-configuration}

- [navigationDocument(_:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:)) —— 为该视图配置用于导航的文稿。
- [navigationDocument(_:preview:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:preview:)) —— 为该视图配置用于导航的文稿。

## 导航栏 {#Navigation-bars}

- [navigationBarBackButtonHidden(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbarbackbuttonhidden(_:)) —— 为该视图隐藏导航栏的返回按钮。
- [navigationBarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitledisplaymode(_:)) —— 为该视图配置标题显示模式。

## 导航栈与栏 {#Navigation-stacks-and-columns}

- [navigationDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(for:destination:)) —— 在导航栈中，把目标视图与所呈现的数据类型关联起来。
- [navigationDestination(isPresented:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(ispresented:destination:)) —— 把目标视图与一个绑定关联起来，用该绑定把视图推入 [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)。
- [navigationDestination(item:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(item:destination:)) —— 在导航栈或导航分栏视图中，把目标视图与某个绑定值关联起来
- [navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(_:)) —— 为包含该视图的那一栏设置固定的偏好宽度。
- [navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(min:ideal:max:)) —— 为包含该视图的那一栏设置灵活的偏好宽度。
- [navigationLinkIndicatorVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/navigationlinkindicatorvisibility(_:)) —— 配置导航链接是否显示展开指示符。
- [navigationTransition(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtransition(_:)) —— 为该视图设置导航过渡样式。

## 滚动视图边缘 {#Scroll-view-edges}

- [scrollEdgeEffectStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffectstyle(_:for:)) —— 为该层级中可滚动视图配置滚动边缘效果样式。
- [scrollEdgeEffectHidden(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffecthidden(_:for:)) —— 隐藏该层级中可滚动视图的滚动边缘效果。

## 标签页视图 {#Tab-views}

- [defaultAdaptableTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaultadaptabletabbarplacement(_:)) —— 为使用可自适应侧边栏样式的标签页视图指定标签页的默认放置位置。
- [defaultTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaulttabbarplacement(_:)) —— 在标签栏无法在不同呈现形式之间自适应、只能显示一种形式的平台上，为 [sidebarAdaptable](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable) 样式的 [TabView](https://developer.apple.com/documentation/swiftui/tabview) 中的标签页指定偏好的放置位置。
- [sectionActions(content:)](https://developer.apple.com/documentation/swiftui/view/sectionactions(content:)) —— 为某个分区添加自定义操作。
- [tabBarMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)) —— 设置标签栏最小化的行为。
- [tabViewBottomAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(content:)) —— 把某个视图放置为标签页视图的底部配件。
- [tabViewBottomAccessory(isEnabled:content:)](https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(isenabled:content:)) —— 把某个视图放置为标签页视图的底部配件。用这个修饰符动态显示和隐藏该配件视图。
- [tabViewCustomization(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewcustomization(_:)) —— 指定要应用到标签页视图侧边栏呈现形式上的自定义项。
- [tabViewSearchActivation(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewsearchactivation(_:)) —— 配置搜索标签页中搜索的激活与取消激活行为。
- [tabViewSidebarHeader(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarheader(content:)) —— 为标签页视图的侧边栏添加自定义页眉。
- [tabViewSidebarFooter(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarfooter(content:)) —— 为标签页视图的侧边栏添加自定义页脚。
- [tabViewSidebarBottomBar(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarbottombar(content:)) —— 为标签页视图的侧边栏添加自定义底栏。

## 工具栏 {#Toolbars}

- [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) —— 用指定的条目填充工具栏或导航栏。
- [toolbar(id:content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(id:content:)) —— 用指定的条目填充工具栏或导航栏，并允许用户自定义。
- [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) —— 指定由 SwiftUI 管理的某个栏的可见性。
- [contentToolbar(for:content:)](https://developer.apple.com/documentation/swiftui/view/contenttoolbar(for:content:)) —— 用你提供的视图填充指定内容视图类型的工具栏。
- [toolbar(removing:)](https://developer.apple.com/documentation/swiftui/view/toolbar(removing:)) —— 移除默认存在的工具栏项
- [toolbarVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarvisibility(_:for:)) —— 指定由 SwiftUI 管理的某个栏的可见性。
- [toolbarBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackground(_:for:)) —— 指定由 SwiftUI 管理的某个栏背景的偏好形状样式。
- [toolbarBackgroundVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackgroundvisibility(_:for:)) —— 指定由 SwiftUI 管理的某个栏上背景的偏好可见性。
- [toolbarItemHidden(_:)](https://developer.apple.com/documentation/swiftui/view/toolbaritemhidden(_:)) —— 在控件组工具栏项中隐藏某个视图。
- [toolbarForegroundStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarforegroundstyle(_:for:)) —— 指定由 SwiftUI 管理的各个栏的偏好前景样式。
- [toolbarColorScheme(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarcolorscheme(_:for:)) —— 指定由 SwiftUI 管理的某个栏的偏好配色方案。
- [toolbarOverflowMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbaroverflowmenu(content:)) —— 配置工具栏的溢出菜单。
- [toolbarRole(_:)](https://developer.apple.com/documentation/swiftui/view/toolbarrole(_:)) —— 为填充工具栏的内容配置语义角色。
- [toolbarMinimizationBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:)) —— 为指定的栏设置最小化行为。
- [toolbarMinimizationRestoration(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationrestoration(_:for:)) —— 为指定的栏设置最小化期间的恢复行为。
- [toolbarMinimizationSafeAreaAdjustment(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationsafeareaadjustment(_:for:)) —— 为指定的栏设置最小化期间的安全区域调整。
- [toolbarTitleMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbartitlemenu(content:)) —— 配置工具栏的标题菜单。
- [toolbarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/toolbartitledisplaymode(_:)) —— 为该视图配置工具栏标题显示模式。
- [ornament(visibility:attachmentAnchor:contentAlignment:ornament:)](https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)) —— 呈现一个装饰件。

## 上下文菜单 {#Context-menus}

- [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) —— 为视图添加上下文菜单。
- [contextMenu(menuItems:preview:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:preview:)) —— 为视图添加带自定义预览的上下文菜单。
- [contextMenu(forSelectionType:menu:primaryAction:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(forselectiontype:menu:primaryaction:)) —— 为视图添加基于条目的上下文菜单。

## 角标 {#Badges}

- [badge(_:)](https://developer.apple.com/documentation/swiftui/view/badge(_:)) —— 用本地化字符串资源为视图生成角标。
- [badgeProminence(_:)](https://developer.apple.com/documentation/swiftui/view/badgeprominence(_:)) —— 指定该视图所创建角标的显著程度。

## 列表 {#Lists}

- [sectionIndexLabel(_:)](https://developer.apple.com/documentation/swiftui/view/sectionindexlabel(_:)) —— 设置分区索引中用来指向该分区的标签，通常只有一个字符长。

## 帮助文本 {#Help-text}

- [help(_:)](https://developer.apple.com/documentation/swiftui/view/help(_:)) —— 用你提供的本地化字符串资源为视图添加帮助文本。

## 状态栏 {#Status-bar}

- [statusBarHidden(_:)](https://developer.apple.com/documentation/swiftui/view/statusbarhidden(_:)) —— 设置状态栏的可见性。

## 外部显示器 {#External-displays}

- [sceneAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/sceneaccessory(content:)) —— 定义与 `self` 关联的任何场景配件。

## Touch Bar {#Touch-Bar}

- [touchBar(content:)](https://developer.apple.com/documentation/swiftui/view/touchbar(content:)) —— 设置 Touch Bar 显示的内容。
- [touchBar(_:)](https://developer.apple.com/documentation/swiftui/view/touchbar(_:)) —— 在适用时设置要在 Touch Bar 中显示的 Touch Bar 内容。
- [touchBarItemPrincipal(_:)](https://developer.apple.com/documentation/swiftui/view/touchbaritemprincipal(_:)) —— 设置对这个 Touch Bar 有特殊意义的主要视图。
- [touchBarCustomizationLabel(_:)](https://developer.apple.com/documentation/swiftui/view/touchbarcustomizationlabel(_:)) —— 设置一个用户可见的字符串，用于标识该视图的功能。
- [touchBarItemPresence(_:)](https://developer.apple.com/documentation/swiftui/view/touchbaritempresence(_:)) —— 设置用户自定义视图的行为。
