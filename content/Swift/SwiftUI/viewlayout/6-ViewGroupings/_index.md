+++
title = "6 视图分组"
date = 2026-09-12T12:47:47+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/view-groupings](https://developer.apple.com/documentation/swiftui/view-groupings)

# 6 视图分组

用表单、控件组等不同用途驱动的容器来呈现视图。

## 概述 {#Overview}

你可以创建服务于不同目的的视图组。

![](./images/view-groupings-hero@2x.png)

例如，[Group](https://developer.apple.com/documentation/swiftui/group) 构造会把指定的视图当作一个整体来处理，而不附加任何额外的布局或外观特征。[Form](https://developer.apple.com/documentation/swiftui/form) 则以适合收集用户输入的平台特有外观呈现一组元素。

关于设计指导，请参阅 Human Interface Guidelines 中的 [布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

## 把视图分组到容器中 {#Grouping-views-into-a-container}

- [创建自定义容器视图](6.1-CreatingCustomContainerViews/) — 访问各个子视图，以组合出灵活的容器视图。
- [Group](https://developer.apple.com/documentation/swiftui/group) — 一种把内容类型的多个实例（例如视图、场景或命令）汇集为单个单位的类型。
- [GroupElementsOfContent](https://developer.apple.com/documentation/swiftui/groupelementsofcontent) — 把给定视图的子视图转换为结果内容视图。
- [GroupSectionsOfContent](https://developer.apple.com/documentation/swiftui/groupsectionsofcontent) — 把给定视图的区段转换为结果内容视图。

## 把视图组织成区段 {#Organizing-views-into-sections}

- [Section](https://developer.apple.com/documentation/swiftui/section) — 一种可以用来在特定视图内添加层级的容器视图。
- [SectionCollection](https://developer.apple.com/documentation/swiftui/sectioncollection) — 一种不透明集合，表示视图的各个区段。
- [SectionConfiguration](https://developer.apple.com/documentation/swiftui/sectionconfiguration) — 指定某个区段的内容。

## 遍历动态数据 {#Iterating-over-dynamic-data}

- [ForEach](https://developer.apple.com/documentation/swiftui/foreach) — 一种根据底层可标识数据集合按需计算视图的结构。
- [ForEachSectionCollection](https://developer.apple.com/documentation/swiftui/foreachsectioncollection) — 一种集合，允许在 for-each 循环中把视图当作其区段集合来处理。
- [ForEachSubviewCollection](https://developer.apple.com/documentation/swiftui/foreachsubviewcollection) — 一种集合，允许在 for-each 循环中把视图当作其子视图集合来处理。
- [DynamicViewContent](https://developer.apple.com/documentation/swiftui/dynamicviewcontent) — 一种根据底层数据集合生成视图的视图类型。

## 访问容器的子视图 {#Accessing-a-containers-subviews}

- [Subview](https://developer.apple.com/documentation/swiftui/subview) — 表示另一个视图的子视图的不透明值。
- [SubviewsCollection](https://developer.apple.com/documentation/swiftui/subviewscollection) — 一种不透明集合，表示视图的各个子视图。
- [SubviewsCollectionSlice](https://developer.apple.com/documentation/swiftui/subviewscollectionslice) — SubviewsCollection 的一个切片。
- [containerValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/containervalue(_:_:)) — 设置视图的某个特定容器值。
- [ContainerValues](https://developer.apple.com/documentation/swiftui/containervalues) — 与给定视图关联的一组容器值。
- [ContainerValueKey](https://developer.apple.com/documentation/swiftui/containervaluekey) — 用于访问容器值的键。

## 把视图分组到框中 {#Grouping-views-into-a-box}

- [GroupBox](https://developer.apple.com/documentation/swiftui/groupbox) — 一种带可选标签的样式化视图，以视觉方式汇集一组逻辑上相关的内容。
- [groupBoxStyle(_:)](https://developer.apple.com/documentation/swiftui/view/groupboxstyle(_:)) — 设置该视图内分组框的样式。

## 对输入分组 {#Grouping-inputs}

- [Form](https://developer.apple.com/documentation/swiftui/form) — 一种用于对数据录入控件（例如设置或检查器中的控件）分组的容器。
- [formStyle(_:)](https://developer.apple.com/documentation/swiftui/view/formstyle(_:)) — 设置视图层级中表单的样式。
- [LabeledContent](https://developer.apple.com/documentation/swiftui/labeledcontent) — 一种用于把标签附加到承载值的视图上的容器。
- [labeledContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labeledcontentstyle(_:)) — 为带标签的内容设置样式。

## 呈现一组控件 {#Presenting-a-group-of-controls}

- [ControlGroup](https://developer.apple.com/documentation/swiftui/controlgroup) — 一种容器视图，以适合当前上下文的视觉方式显示语义上相关的控件。
- [controlGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/controlgroupstyle(_:)) — 设置该视图内控件组的样式。
