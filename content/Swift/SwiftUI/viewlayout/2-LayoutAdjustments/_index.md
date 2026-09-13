+++
title = "2 布局调整"
date = 2026-09-12T12:47:47+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/layout-adjustments](https://developer.apple.com/documentation/swiftui/layout-adjustments)

# 2 布局调整

对对齐方式、间距、内边距以及其他布局参数做微调。

## 概述 {#Overview}

栈和网格这类布局容器为在应用用户界面中排列视图提供了很好的起点。当你需要做微调时，请使用布局视图修饰符。你可以调整或约束视图的尺寸、位置和对齐方式，也可以在视图周围添加内边距，并指明视图如何与系统定义的安全区域交互。

![](./images/layout-adjustments-hero@2x.png)

要了解基本布局的入门知识，请参阅 [布局基础](../1-LayoutFundamentals/)。关于设计指导，请参阅 Human Interface Guidelines 中的 [布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

## 微调布局 {#Fine-tuning-a-layout}

- [布局一个简单视图](2.1-LayingOutASimpleView/) — 通过调整视图尺寸来创建视图布局。
- [检查视图布局](2.2-InspectingViewLayout/) — 使用 Xcode 预览或添加临时边框来确定视图的位置与范围。

## 为视图添加内边距 {#Adding-padding-around-a-view}

- [padding(_:)](https://developer.apple.com/documentation/swiftui/view/padding(_:)) — 为该视图的每条边添加不同的内边距。
- [padding(_:_:)](https://developer.apple.com/documentation/swiftui/view/padding(_:_:)) — 为该视图的特定边缘添加相同的内边距。
- [padding3D(_:)](https://developer.apple.com/documentation/swiftui/view/padding3d(_:)) — 使用你指定的边缘内边距为该视图添加内边距。
- [padding3D(_:_:)](https://developer.apple.com/documentation/swiftui/view/padding3d(_:_:)) — 使用你指定的边缘内边距为该视图添加内边距。
- [scenePadding(_:)](https://developer.apple.com/documentation/swiftui/view/scenepadding(_:)) — 使用适合当前场景的量，为该视图的指定边缘添加内边距。
- [scenePadding(_:edges:)](https://developer.apple.com/documentation/swiftui/view/scenepadding(_:edges:)) — 使用适合当前场景的量，为该视图的指定边缘添加指定类型的内边距。
- [ScenePadding](https://developer.apple.com/documentation/swiftui/scenepadding) — 用于把视图与其所属场景分隔开的内边距。

## 影响视图的尺寸 {#Influencing-a-views-size}

- [frame(width:height:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(width:height:alignment:)) — 把该视图放置在一个指定尺寸的不可见框架中。
- [frame(depth:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(depth:alignment:)) — 把该视图放置在一个指定深度的不可见框架中。
- [frame(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(minwidth:idealwidth:maxwidth:minheight:idealheight:maxheight:alignment:)) — 把该视图放置在一个具有指定尺寸约束的不可见框架中。
- [frame(minDepth:idealDepth:maxDepth:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(mindepth:idealdepth:maxdepth:alignment:)) — 把该视图放置在一个具有指定深度约束的不可见框架中。
- [containerRelativeFrame(_:alignment:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:)) — 把该视图放置在一个不可见框架中，其尺寸相对于最近的容器。
- [containerRelativeFrame(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:_:)) — 把该视图放置在一个不可见框架中，其尺寸相对于最近的容器。
- [containerRelativeFrame(_:count:span:spacing:alignment:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:count:span:spacing:alignment:)) — 把该视图放置在一个不可见框架中，其尺寸相对于最近的容器。
- [fixedSize()](https://developer.apple.com/documentation/swiftui/view/fixedsize()) — 把该视图固定在其理想尺寸上。
- [fixedSize(horizontal:vertical:)](https://developer.apple.com/documentation/swiftui/view/fixedsize(horizontal:vertical:)) — 在指定维度上把该视图固定在其理想尺寸上。
- [layoutPriority(_:)](https://developer.apple.com/documentation/swiftui/view/layoutpriority(_:)) — 设置父布局应为此子视图分配空间的优先级。

## 调整视图的位置 {#Adjusting-a-views-position}

- [微调视图的位置](2.3-MakingFineAdjustmentsToAViewSPosition/) — 通过应用 offset 或 position 修饰符来移动视图的位置。
- [position(_:)](https://developer.apple.com/documentation/swiftui/view/position(_:)) — 把该视图的中心放在其父视图坐标空间中的指定点。
- [position(x:y:)](https://developer.apple.com/documentation/swiftui/view/position(x:y:)) — 把该视图的中心放在其父视图坐标空间中的指定坐标处。
- [offset(_:)](https://developer.apple.com/documentation/swiftui/view/offset(_:)) — 按 offset 参数中指定的水平和垂直量偏移该视图。
- [offset(x:y:)](https://developer.apple.com/documentation/swiftui/view/offset(x:y:)) — 按指定的水平和垂直距离偏移该视图。
- [offset(z:)](https://developer.apple.com/documentation/swiftui/view/offset(z:)) — 按给定的以点表示的距离把视图在 Z 轴方向前移。

## 对齐视图 {#Aligning-views}

- [在栈内对齐视图](2.4-AligningViewsWithinAStack/) — 使用对齐参考线在栈内定位视图。
- [跨栈对齐视图](2.5-AligningViewsAcrossStacks/) — 创建自定义对齐方式，并用它在多个栈之间对齐视图。
- [alignmentGuide(_:computeValue:)](https://developer.apple.com/documentation/swiftui/view/alignmentguide(_:computevalue:)) — 设置视图的水平对齐方式。
- [Alignment](https://developer.apple.com/documentation/swiftui/alignment) — 在两个轴向上的对齐方式。
- [HorizontalAlignment](https://developer.apple.com/documentation/swiftui/horizontalalignment) — 沿水平轴的对齐位置。
- [VerticalAlignment](https://developer.apple.com/documentation/swiftui/verticalalignment) — 沿垂直轴的对齐位置。
- [DepthAlignment](https://developer.apple.com/documentation/swiftui/depthalignment) — 沿深度轴的对齐位置。
- [AlignmentID](https://developer.apple.com/documentation/swiftui/alignmentid) — 用于创建自定义对齐参考线的类型。
- [ViewDimensions](https://developer.apple.com/documentation/swiftui/viewdimensions) — 视图在自身坐标空间中的尺寸和对齐参考线。
- [ViewDimensions3D](https://developer.apple.com/documentation/swiftui/viewdimensions3d) — 视图在自身坐标空间中的三维尺寸和对齐参考线。
- [SpatialContainer](https://developer.apple.com/documentation/swiftui/spatialcontainer) — 一种在三维空间中排列重叠内容的布局容器。

## 设置边距 {#Setting-margins}

- [contentMargins(_:for:)](https://developer.apple.com/documentation/swiftui/view/contentmargins(_:for:)) — 为给定的位置配置内容边距。
- [contentMargins(_:_:for:)](https://developer.apple.com/documentation/swiftui/view/contentmargins(_:_:for:)) — 为给定的位置配置内容边距。
- [ContentMarginPlacement](https://developer.apple.com/documentation/swiftui/contentmarginplacement) — 边距的位置。

## 保持在安全区域内 {#Staying-in-the-safe-areas}

- [ignoresSafeArea(_:edges:)](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)) — 扩展视图的安全区域。
- [ignoresSafeArea(_:edges:alignment:)](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:alignment:)) — 扩展视图的安全区域，并使用提供的对齐方式在新边界内对齐内容。
- [safeAreaInset(edge:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:)) — 在修改后的视图旁边显示指定内容。
- [safeAreaPadding(_:)](https://developer.apple.com/documentation/swiftui/view/safeareapadding(_:)) — 把提供的内边距加入该视图的安全区域。
- [safeAreaPadding(_:_:)](https://developer.apple.com/documentation/swiftui/view/safeareapadding(_:_:)) — 把提供的内边距加入该视图的安全区域。
- [SafeAreaRegions](https://developer.apple.com/documentation/swiftui/safearearegions) — 一组符号化的安全区域。

## 设置布局方向 {#Setting-a-layout-direction}

- [layoutDirectionBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/layoutdirectionbehavior(_:)) — 设置该视图在不同布局方向下的行为。
- [LayoutDirectionBehavior](https://developer.apple.com/documentation/swiftui/layoutdirectionbehavior) — 描述布局方向变化时应该发生什么。
- [layoutDirection](https://developer.apple.com/documentation/swiftui/environmentvalues/layoutdirection) — 与当前环境关联的布局方向。
- [LayoutDirection](https://developer.apple.com/documentation/swiftui/layoutdirection) — SwiftUI 可以用于排布内容的方向。
- [LayoutRotationUnaryLayout](https://developer.apple.com/documentation/swiftui/layoutrotationunarylayout)

## 响应界面特征 {#Reacting-to-interface-characteristics}

- [isLuminanceReduced](https://developer.apple.com/documentation/swiftui/environmentvalues/isluminancereduced) — 一个布尔值，指示显示器或环境当前是否要求降低亮度。
- [displayScale](https://developer.apple.com/documentation/swiftui/environmentvalues/displayscale) — 该环境的显示比例。
- [pixelLength](https://developer.apple.com/documentation/swiftui/environmentvalues/pixellength) — 屏幕上单个像素的尺寸。
- [horizontalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/horizontalsizeclass) — 该环境的水平尺寸类别。
- [verticalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/verticalsizeclass) — 该环境的垂直尺寸类别。
- [UserInterfaceSizeClass](https://developer.apple.com/documentation/swiftui/userinterfacesizeclass) — 一组值，指示视图可用的视觉尺寸。

## 访问边缘、区域和布局 {#Accessing-edges-regions-and-layouts}

- [Edge](https://developer.apple.com/documentation/swiftui/edge) — 一个枚举，用于指示矩形的某条边。
- [Edge3D](https://developer.apple.com/documentation/swiftui/edge3d) — 三维体积的一条边或一个面。
- [HorizontalEdge](https://developer.apple.com/documentation/swiftui/horizontaledge) — 水平轴上的某条边。
- [VerticalEdge](https://developer.apple.com/documentation/swiftui/verticaledge) — 垂直轴上的某条边。
- [EdgeInsets](https://developer.apple.com/documentation/swiftui/edgeinsets) — 矩形各边的内缩距离。
- [EdgeInsets3D](https://developer.apple.com/documentation/swiftui/edgeinsets3d) — 三维体积各面的内缩距离。
