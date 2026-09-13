+++
title = "4 拖放"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/drag-and-drop](https://developer.apple.com/documentation/swiftui/drag-and-drop)

# 4 拖放

让大家可以通过把项目从一个位置拖到另一个位置来移动或复制它们。

## 概述 {#Overview}

拖放为大家提供了一种便捷方式，可以把内容从应用的一部分移动到另一部分、从一个应用移动到另一个应用，或者用直观的拖拽手势重新排列内容。为应用界面中可能的源视图和目标视图添加视图修饰符，即可在你的应用中支持这一功能。

![](./images/drag-and-drop-hero@2x.png)

在你的修饰符中，提供或接受遵循 [Transferable](https://developer.apple.com/documentation/coretransferable/transferable) 协议的类型，或者遵循 [NSItemProviderReading](https://developer.apple.com/documentation/foundation/nsitemproviderreading) 和/或 [NSItemProviderWriting](https://developer.apple.com/documentation/foundation/nsitemproviderwriting) 的类型。在 Swift 中，优先使用可传输项目。

关于设计指导，请参阅 Human Interface Guidelines 中的 [拖放](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop)。

## 基础 {#Essentials}

- [在 SwiftUI 中采用拖放](4.1-AdoptingDragAndDropUsingSwiftui/) — 在列表、表格和自定义视图里启用拖放交互。
- [把视图变成拖拽源](4.2-MakingAViewIntoADragSource/) — 采用 draggable API 为拖放操作提供项目。
- [在列表、栈、网格和自定义布局中重新排序项目](4.3-ReorderingItemsInListsStacksGridsAndCustomLayouts/) — 使用重新排序修饰符为 SwiftUI 布局添加拖拽重新排序的交互。

## 配置拖放行为 {#Configuring-drag-and-drop-behavior}

- [dragConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dragconfiguration(_:)) — 配置一次拖拽会话。
- [DragConfiguration](https://developer.apple.com/documentation/swiftui/dragconfiguration) — 由拖拽源提议的拖拽行为。一个值，描述拖拽源支持哪些拖拽操作。
- [dropConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dropconfiguration(_:)) — 配置一次放置会话。
- [DropConfiguration](https://developer.apple.com/documentation/swiftui/dropconfiguration) — 描述放置的行为。
- [dragContainer(for:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:in:_:)) — 一个包含可拖拽视图的容器，其拖拽负载基于多个被拖拽项目的标识符。
- [dragContainer(for:itemID:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:itemid:in:_:)) — 一个包含可拖拽视图的容器。
- [dragContainerSelection(_:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/dragcontainerselection(_:containernamespace:)) — 为拖拽容器提供多项目选择支持。

## 移动项目 {#Moving-items}

- [DragSession](https://developer.apple.com/documentation/swiftui/dragsession) — 描述正在进行中的拖拽会话。
- [DropSession](https://developer.apple.com/documentation/swiftui/dropsession)

## 移动可传输项目 {#Moving-transferable-items}

- [draggable(_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:)) — 把该视图激活为拖放操作的源。
- [draggable(_:preview:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:preview:)) — 把该视图激活为拖放操作的源。
- [draggable(_:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:containernamespace:_:)) — 把该视图激活为拖放操作的源，并可以提供一个可选的可标识负载，同时指定该视图所属拖拽容器的命名空间。
- [draggable(_:id:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:containernamespace:_:)) — 把该视图激活为拖放操作的源，并可以提供一个可选负载，同时指定该视图所属拖拽容器的命名空间。
- [draggable(_:id:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:item:containernamespace:)) — 把该视图激活为拖放操作的源，并可以提供一个可选负载，同时指定该视图所属拖拽容器的命名空间。
- [draggable(_:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:item:containernamespace:)) — 把该视图激活为拖放操作的源，并可以提供一个可选的可标识负载，同时指定该视图所属拖拽容器的命名空间。
- [draggable(containerItemID:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(containeritemid:containernamespace:)) — 在拖拽容器内部把该视图激活为拖放操作的源。支持惰性拖拽容器。

## 使用项目提供者移动项目 {#Moving-items-using-item-providers}

- [itemProvider(_:)](https://developer.apple.com/documentation/swiftui/view/itemprovider(_:)) — 提供一个闭包，为某个特定数据元素给出拖拽表示。
- [onDrag(_:preview:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:preview:)) — 把该视图激活为拖放操作的源。
- [onDrag(_:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:)) — 把该视图激活为拖放操作的源。
- [onDrop(of:isTargeted:perform:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:istargeted:perform:)) — 定义一个拖放操作的目标，用你指定的闭包处理被放置的内容。
- [onDrop(of:delegate:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:delegate:)) — 使用你提供的代理所控制的行为，定义一个拖放操作的目标。
- [DropDelegate](https://developer.apple.com/documentation/swiftui/dropdelegate) — 一种接口，你实现它来与一个被修改为接受放置的视图中的放置操作交互。
- [DropProposal](https://developer.apple.com/documentation/swiftui/dropproposal) — 一次放置的行为。
- [DropOperation](https://developer.apple.com/documentation/swiftui/dropoperation) — 一些操作类型，决定用户放下被拖拽项目时拖放会话如何结束。
- [DropInfo](https://developer.apple.com/documentation/swiftui/dropinfo) — 一次放置的当前状态。

## 重新排序项目 {#Reordering-items}

- [用 SwiftUI 制作带拖放与重排的纸牌游戏](4.4-MakingACardGameWithDragDropAndReorderingInSwiftui/) — 使用拖放与重排修饰符在纸牌游戏中的不同位置之间移动纸牌。
- [reorderable()](https://developer.apple.com/documentation/swiftui/dynamicviewcontent/reorderable()) — 允许在可重排容器修饰符的作用范围内对来自该内容的视图重新排序。
- [reorderable(collectionID:)](https://developer.apple.com/documentation/swiftui/dynamicviewcontent/reorderable(collectionid:)) — 允许在可重排容器修饰符的作用范围内，在同一区段内以及不同区段之间对来自该内容的视图重新排序。
- [ReorderableSingleCollectionIdentifier](https://developer.apple.com/documentation/swiftui/reorderablesinglecollectionidentifier) — 一种不透明的空类型，用于标识只包含单个集合的可重排容器和修饰符。
- [reorderContainer(for:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:isenabled:move:)) — 定义一个由可重排视图组成的容器。
- [reorderContainer(for:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:in:isenabled:move:)) — 定义一个由可重排视图组成的容器，并可用你指定的类型来标识区段。
- [reorderContainer(for:itemID:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:isenabled:move:)) — 定义一个由可重排视图组成的容器，并可用你指定的类型和键路径来标识项目。
- [reorderContainer(for:itemID:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:in:isenabled:move:)) — 定义一个由可重排视图组成的容器，并可用你指定的类型和键路径来标识项目，以及用某个类型来标识集合。
- [reorderDestination(for:in:)](https://developer.apple.com/documentation/swiftui/dropsession/reorderdestination(for:in:)) — 给出在与该放置目标修饰符关联的容器中发生的重新排序操作的目标值。
- [reorderDestination(for:itemID:in:)](https://developer.apple.com/documentation/swiftui/dropsession/reorderdestination(for:itemid:in:)) — 给出在与该放置目标修饰符关联的容器中发生的重新排序操作的目标值。
- [ReorderDifference](https://developer.apple.com/documentation/swiftui/reorderdifference) — 一次重新排序操作所产生的差异。

## 描述预览的排布方式 {#Describing-preview-formations}

- [dragPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/dragpreviewsformation(_:)) — 描述被拖拽的各个预览在视觉上是如何组合的。
- [dropPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/droppreviewsformation(_:)) — 描述放置时的各个预览是如何组合的。
- [DragDropPreviewsFormation](https://developer.apple.com/documentation/swiftui/dragdroppreviewsformation) — 在 macOS 上描述被拖拽的各个预览在视觉上是如何组合的。拖拽源和放置目标都可以指定自己期望的预览排布方式。

## 配置弹性加载 {#Configuring-spring-loading}

- [springLoadingBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/springloadingbehavior(_:)) — 设置该视图的弹性加载行为。
- [springLoadingBehavior](https://developer.apple.com/documentation/swiftui/environmentvalues/springloadingbehavior) — 与该环境关联的视图在弹性加载交互方面的行为。
- [SpringLoadingBehavior](https://developer.apple.com/documentation/swiftui/springloadingbehavior) — 用于控制视图弹性加载行为的选项。
