+++
title = "1 布局基础"
date = 2026-09-12T12:47:47+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/layout-fundamentals](https://developer.apple.com/documentation/swiftui/layout-fundamentals)

# 1 布局基础

在栈、网格等内置布局容器中排列视图。

## 概述 {#Overview}

使用布局容器来排列用户界面中的各个元素。栈和网格会随内容或界面尺寸的变化而更新并调整其包含的子视图位置。你可以把布局容器嵌套进其他布局容器，嵌套深度不限，从而实现复杂的布局效果。

![](./images/layout-fundamentals-hero@2x.png)

要微调用布局容器视图构建的布局的位置、对齐方式以及其他方面，请参阅 [布局调整](../2-LayoutAdjustments/)。要定义自定义布局容器，请参阅 [自定义布局](../3-CustomLayout/)。关于设计指导，请参阅 Human Interface Guidelines 中的 [布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

## 选择布局 {#Choosing-a-layout}

- [为你的内容选择合适的容器视图](1.1-PickingContainerViewsForYourContent/) — 使用栈、网格、列表和表单构建灵活的用户界面。

## 在一维中静态排列视图 {#Statically-arranging-views-in-one-dimension}

- [用栈视图构建布局](1.2-BuildingLayoutsWithStackViews/) — 用基础容器视图组合出复杂的布局。
- [HStack](https://developer.apple.com/documentation/swiftui/hstack) — 一种把其子视图排成水平一行的视图。
- [VStack](https://developer.apple.com/documentation/swiftui/vstack) — 一种把其子视图排成垂直一列的视图。

## 在一维中动态排列视图 {#Dynamically-arranging-views-in-one-dimension}

- [用惰性栈视图对数据分组](1.3-GroupingDataWithLazyStackViews/) — 在惰性栈视图中把内容拆分为多个逻辑区段。
- [创建高性能的可滚动栈](1.4-CreatingPerformantScrollableStacks/) — 借助滚动视图、栈视图和惰性栈，高效地显示大量重复视图。
- [LazyHStack](https://developer.apple.com/documentation/swiftui/lazyhstack) — 一种把其子视图排成向水平方向延伸的一行、并按需创建项目的视图。
- [LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack) — 一种把其子视图排成向垂直方向延伸的一列、并按需创建项目的视图。
- [PinnedScrollableViews](https://developer.apple.com/documentation/swiftui/pinnedscrollableviews) — 一组可以被固定在滚动视图边界上的视图类型。

## 在二维中静态排列视图 {#Statically-arranging-views-in-two-dimensions}

- [Grid](https://developer.apple.com/documentation/swiftui/grid) — 一种把其他视图排列成二维布局的容器视图。
- [GridRow](https://developer.apple.com/documentation/swiftui/gridrow) — 二维网格容器中的水平一行。
- [gridCellColumns(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellcolumns(_:)) — 让充当网格单元格的视图跨越指定的列数。
- [gridCellAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellanchor(_:)) — 为充当网格单元格的视图指定自定义对齐锚点。
- [gridCellUnsizedAxes(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellunsizedaxes(_:)) — 请求网格布局不要在指定轴向上给该视图提供额外尺寸。
- [gridColumnAlignment(_:)](https://developer.apple.com/documentation/swiftui/view/gridcolumnalignment(_:)) — 覆盖该视图所在网格列默认的水平对齐方式。

## 在二维中动态排列视图 {#Dynamically-arranging-views-in-two-dimensions}

- [LazyHGrid](https://developer.apple.com/documentation/swiftui/lazyhgrid) — 一种把其子视图排列成向水平方向延伸的网格、并按需创建项目的容器视图。
- [LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid) — 一种把其子视图排列成向垂直方向延伸的网格、并按需创建项目的容器视图。
- [GridItem](https://developer.apple.com/documentation/swiftui/griditem) — 对惰性网格中某一行或某一列的说明。

## 层叠视图 {#Layering-views}

- [为视图添加背景](1.5-AddingABackgroundToYourView/) — 在视图后面组合出一个背景，并把它延伸到安全区域内边距之外。
- [ZStack](https://developer.apple.com/documentation/swiftui/zstack) — 一种把其子视图叠加在一起、并在两个轴向上对齐它们的视图。
- [zIndex(_:)](https://developer.apple.com/documentation/swiftui/view/zindex(_:)) — 控制重叠视图的显示顺序。
- [background(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/background(alignment:content:)) — 把你指定的视图层叠在该视图后面。
- [background(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(_:ignoressafeareaedges:)) — 把视图的背景设置为某种样式。
- [background(ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(ignoressafeareaedges:)) — 把视图的背景设置为默认背景样式。
- [background(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(_:in:fillstyle:)) — 把视图的背景设置为用某种样式填充的可内缩形状。
- [background(in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(in:fillstyle:)) — 把视图的背景设置为用默认背景样式填充的可内缩形状。
- [overlay(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/overlay(alignment:content:)) — 把你指定的视图层叠在该视图前面。
- [overlay(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:ignoressafeareaedges:)) — 把指定的样式层叠在该视图前面。
- [overlay(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:in:fillstyle:)) — 把你指定的形状层叠在该视图前面。
- [backgroundMaterial](https://developer.apple.com/documentation/swiftui/environmentvalues/backgroundmaterial) — 当前视图下方的材质。
- [containerBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(_:for:)) — 用某个视图设置所属容器的容器背景。
- [containerBackground(for:alignment:content:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:)) — 用某个视图设置所属容器的容器背景。
- [ContainerBackgroundPlacement](https://developer.apple.com/documentation/swiftui/containerbackgroundplacement) — 容器背景的位置。

## 自动选择适配的布局 {#Automatically-choosing-the-layout-that-fits}

- [ViewThatFits](https://developer.apple.com/documentation/swiftui/viewthatfits) — 一种通过提供第一个能够放下的子视图来适应可用空间的视图。

## 分隔符 {#Separators}

- [Spacer](https://developer.apple.com/documentation/swiftui/spacer) — 一段灵活的空间，它会沿所属栈布局的主轴扩展；如果不包含在栈中，则在两个轴向上扩展。
- [Divider](https://developer.apple.com/documentation/swiftui/divider) — 一种可用于分隔其他内容的视觉元素。
