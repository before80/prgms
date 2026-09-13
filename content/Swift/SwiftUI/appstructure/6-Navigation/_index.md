+++
title = "6 导航"
date = 2026-09-12T12:47:47+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/navigation](https://developer.apple.com/documentation/swiftui/navigation)

# 6 导航

让人们可以在场景中应用视图层级的不同部分之间移动。

## 概述 {#Overview}

用导航容器为应用界面提供结构，让人们能轻松在应用的各个部分之间切换。

![](./images/navigation-hero@2x.png)

例如，人们可以用 [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack) 在一个视图栈中前进和后退，或者用 [TabView](https://developer.apple.com/documentation/swiftui/tabview) 从标签栏中选择要显示哪个视图。

通过给容器添加 [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) 这样的视图修饰符来配置导航容器。对容器内部的视图使用其他修饰符，可以影响容器在显示该视图时的行为。例如，你可以在某个视图上使用 [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:))，为显示该视图时的工具栏提供标题。

## 基础 {#Essentials}

- [理解导航栈](6.1-UnderstandingTheNavigationStack/) —— 了解导航栈、导航链接，以及如何在应用结构中管理导航类型。

## 在多栏中呈现视图 {#Presenting-views-in-columns}

- [为 SwiftUI 应用引入健壮的导航结构](6.2-BringingRobustNavigationStructureToYourSwiftuiApp/) —— 使用导航链接、栈、目标和路径，为所有平台提供流畅的体验，并支持深度链接、状态恢复等行为。
- [迁移到新的导航类型](6.3-MigratingToNewNavigationTypes/) —— 用导航栈和导航分栏视图替换导航视图，改善应用的导航行为。
- [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview) —— 以两栏或三栏呈现视图的视图，其中前导栏中的选择控制后续栏中呈现的内容。
- [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) —— 设置该视图内导航分栏视图的样式。
- [navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(_:)) —— 为包含该视图的那一栏设置固定的偏好宽度。
- [navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(min:ideal:max:)) —— 为包含该视图的那一栏设置灵活的偏好宽度。
- [NavigationSplitViewVisibility](https://developer.apple.com/documentation/swiftui/navigationsplitviewvisibility) —— 导航分栏视图中前导各栏的可见性。
- [NavigationLink](https://developer.apple.com/documentation/swiftui/navigationlink) —— 控制导航呈现的视图。

## 在单栏中堆叠视图 {#Stacking-views-in-one-column}

- [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack) —— 显示根视图、并让你能在根视图之上呈现其他视图的视图。
- [NavigationPath](https://developer.apple.com/documentation/swiftui/navigationpath) —— 表示导航栈内容的类型擦除数据列表。
- [navigationDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(for:destination:)) —— 在导航栈中，把目标视图与所呈现的数据类型关联起来。
- [navigationDestination(isPresented:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(ispresented:destination:)) —— 把目标视图与一个绑定关联起来，用该绑定把视图推入 [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)。
- [navigationDestination(item:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(item:destination:)) —— 在导航栈或导航分栏视图中，把目标视图与某个绑定值关联起来

## 管理栏的折叠 {#Managing-column-collapse}

- [NavigationSplitViewColumn](https://developer.apple.com/documentation/swiftui/navigationsplitviewcolumn) —— 表示导航分栏视图中某一栏的视图。

## 为导航内容设置标题 {#Setting-titles-for-navigation-content}

- [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:)) —— 用本地化字符串资源为该视图配置用于导航的标题。
- [navigationSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsubtitle(_:)) —— 用本地化字符串资源为该视图配置用于导航的副标题。
- [navigationDocument(_:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:)) —— 为该视图配置用于导航的文稿。
- [navigationDocument(_:preview:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:preview:)) —— 为该视图配置用于导航的文稿。

## 配置导航栏 {#Configuring-the-navigation-bar}

- [navigationBarBackButtonHidden(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbarbackbuttonhidden(_:)) —— 为该视图隐藏导航栏的返回按钮。
- [navigationBarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitledisplaymode(_:)) —— 为该视图配置标题显示模式。
- [NavigationBarItem](https://developer.apple.com/documentation/swiftui/navigationbaritem) —— 导航栏的配置，表示导航栈顶部的某个视图。

## 配置侧边栏 {#Configuring-the-sidebar}

- [sidebarRowSize](https://developer.apple.com/documentation/swiftui/environmentvalues/sidebarrowsize) —— 侧边栏行的当前大小。
- [SidebarRowSize](https://developer.apple.com/documentation/swiftui/sidebarrowsize) —— 侧边栏行的标准大小。

## 在标签页中呈现视图 {#Presenting-views-in-tabs}

- [用标签页导航增强应用内容](6.5-EnhancingYourAppContentWithTabNavigation/) —— 用标签栏提供快捷导航的同时，让应用内容始终处于醒目位置。
- [TabView](https://developer.apple.com/documentation/swiftui/tabview) —— 使用可交互的界面元素在多个子视图之间切换的视图。
- [Tab](https://developer.apple.com/documentation/swiftui/tab) —— 标签页的内容，以及它在标签页视图中关联的标签项。
- [TabRole](https://developer.apple.com/documentation/swiftui/tabrole) —— 定义标签页用途的值。
- [TabSection](https://developer.apple.com/documentation/swiftui/tabsection) —— 可用于在标签页视图中添加层级的容器。
- [tabViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewstyle(_:)) —— 设置当前环境中标签页视图的样式。

## 配置标签栏 {#Configuring-a-tab-bar}

- [defaultAdaptableTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaultadaptabletabbarplacement(_:)) —— 为使用可自适应侧边栏样式的标签页视图指定标签页的默认放置位置。
- [defaultTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaulttabbarplacement(_:)) —— 在标签栏无法在不同呈现形式之间自适应、只能显示一种形式的平台上，为 [sidebarAdaptable](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable) 样式的 [TabView](https://developer.apple.com/documentation/swiftui/tabview) 中的标签页指定偏好的放置位置。
- [tabViewSidebarHeader(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarheader(content:)) —— 为标签页视图的侧边栏添加自定义页眉。
- [tabViewSidebarFooter(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarfooter(content:)) —— 为标签页视图的侧边栏添加自定义页脚。
- [tabViewSidebarBottomBar(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarbottombar(content:)) —— 为标签页视图的侧边栏添加自定义底栏。
- [AdaptableTabBarPlacement](https://developer.apple.com/documentation/swiftui/adaptabletabbarplacement) —— 使用可自适应侧边栏样式的标签页视图中标签页的放置位置。
- [tabBarPlacement](https://developer.apple.com/documentation/swiftui/environmentvalues/tabbarplacement) —— 标签栏当前的放置位置。
- [TabBarPlacement](https://developer.apple.com/documentation/swiftui/tabbarplacement) —— 标签页视图中标签页的放置位置。
- [isTabBarShowingSections](https://developer.apple.com/documentation/swiftui/environmentvalues/istabbarshowingsections) —— 一个布尔值，决定标签页视图是否显示某个标签分区的展开内容。
- [tabBarMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)) —— 设置标签栏最小化的行为。
- [TabBarMinimizeBehavior](https://developer.apple.com/documentation/swiftui/tabbarminimizebehavior)
- [TabViewBottomAccessoryPlacement](https://developer.apple.com/documentation/swiftui/tabviewbottomaccessoryplacement) —— 标签页视图中底部配件的放置位置。你可以用它根据放置位置调整配件视图的内容。

## 配置标签页 {#Configuring-a-tab}

- [sectionActions(content:)](https://developer.apple.com/documentation/swiftui/view/sectionactions(content:)) —— 为某个分区添加自定义操作。
- [TabPlacement](https://developer.apple.com/documentation/swiftui/tabplacement) —— 标签页可以出现的位置。
- [TabContentBuilder](https://developer.apple.com/documentation/swiftui/tabcontentbuilder) —— 为支持编程式选择的标签页视图构造标签页的结果构建器。该构建器要求标签页视图中的所有标签页具有相同的选择类型。
- [TabContent](https://developer.apple.com/documentation/swiftui/tabcontent) —— 为标签页视图中可编程选择的标签页提供内容的类型。
- [AnyTabContent](https://developer.apple.com/documentation/swiftui/anytabcontent) —— 类型擦除的标签页内容。

## 启用标签页自定义 {#Enabling-tab-customization}

- [tabViewCustomization(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewcustomization(_:)) —— 指定要应用到标签页视图侧边栏呈现形式上的自定义项。
- [TabViewCustomization](https://developer.apple.com/documentation/swiftui/tabviewcustomization) —— 人们对可自适应侧边栏标签页视图所做的自定义。
- [TabCustomizationBehavior](https://developer.apple.com/documentation/swiftui/tabcustomizationbehavior) —— 可自定义标签页视图内容的自定义行为。

## 在多窗格中显示视图 {#Displaying-views-in-multiple-panes}

- [HSplitView](https://developer.apple.com/documentation/swiftui/hsplitview) —— 把子视图排成水平一行的布局容器，允许用户通过放在它们之间的分隔条调整大小。
- [VSplitView](https://developer.apple.com/documentation/swiftui/vsplitview) —— 把子视图排成垂直一列的布局容器，允许用户通过放在它们之间的分隔条调整大小。

## 已弃用的类型 {#Deprecated-Types}

- [NavigationView](https://developer.apple.com/documentation/swiftui/navigationview) —— 用于呈现视图栈、表示导航层级中可见路径的视图。
- [tabItem(_:)](https://developer.apple.com/documentation/swiftui/view/tabitem(_:)) —— 设置与该视图关联的标签栏项。
