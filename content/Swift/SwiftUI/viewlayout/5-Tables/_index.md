+++
title = "5 表格"
date = 2026-09-12T12:47:47+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/tables](https://developer.apple.com/documentation/swiftui/tables)

# 5 表格

显示按行和列排列的、可选择且可排序的数据。

## 概述 {#Overview}

使用表格可以在一组元素上显示多个值。集合中的每个元素分别显示在表格的不同行中，而某个元素的每个值则分别显示在不同的列中。窄屏设备可能会调整为只显示表格的第一列。

![](./images/tables-hero@2x.png)

创建表格时，你提供一个元素集合，然后告诉表格如何为每一列找到所需的值。在简单情况下，SwiftUI 会自动推断每一行的元素，但在更复杂的场景中，你也可以显式指定各行元素。只需少量额外配置，你还可以让表格中的项目可被选中，并让各列可排序。

与 [List](https://developer.apple.com/documentation/swiftui/list) 类似，表格包含可由 [滚动视图](../7-ScrollViews/) 中描述的视图修饰符来配置的隐式垂直滚动。关于设计指导，请参阅 Human Interface Guidelines 中的 [列表与表格](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)。

## 创建表格 {#Creating-a-table}

- [用 SwiftUI 构建出色的 Mac 应用](5.1-BuildingAGreatMacAppWithSwiftui/) — 通过融入边栏、表格、工具栏以及其他几种常见的用户界面元素，构建引人入胜的 SwiftUI Mac 应用。
- [Table](https://developer.apple.com/documentation/swiftui/table) — 一种以一列或多列形式呈现数据行的容器，可选择支持选中一个或多个成员。
- [tableStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tablestyle(_:)) — 设置该视图内表格的样式。

## 创建列 {#Creating-columns}

- [TableColumn](https://developer.apple.com/documentation/swiftui/tablecolumn) — 为表格中的每一行显示一个视图的一列。
- [TableColumnContent](https://developer.apple.com/documentation/swiftui/tablecolumncontent) — 用于表示表格中各列的类型。
- [TableColumnAlignment](https://developer.apple.com/documentation/swiftui/tablecolumnalignment) — 描述表格列内容的对齐方式。
- [TableColumnBuilder](https://developer.apple.com/documentation/swiftui/tablecolumnbuilder) — 一种结果构建器，根据闭包创建表格列内容。
- [TableColumnForEach](https://developer.apple.com/documentation/swiftui/tablecolumnforeach) — 一种根据底层可标识数据集合按需计算各列的结构。

## 自定义列 {#Customizing-columns}

- [tableColumnHeaders(_:)](https://developer.apple.com/documentation/swiftui/view/tablecolumnheaders(_:)) — 控制 `Table` 列页眉视图的可见性。
- [TableColumnCustomization](https://developer.apple.com/documentation/swiftui/tablecolumncustomization) — 表格中各列状态的一种表示。
- [TableColumnCustomizationBehavior](https://developer.apple.com/documentation/swiftui/tablecolumncustomizationbehavior) — 表格可以向用户提供的某列的一组自定义行为。

## 创建行 {#Creating-rows}

- [TableRow](https://developer.apple.com/documentation/swiftui/tablerow) — 表示表格中某个数据值的一行。
- [TableRowContent](https://developer.apple.com/documentation/swiftui/tablerowcontent) — 用于表示表格各行的类型。
- [TableHeaderRowContent](https://developer.apple.com/documentation/swiftui/tableheaderrowcontent) — 显示单个视图而不是分列内容的表格行。
- [TupleTableRowContent](https://developer.apple.com/documentation/swiftui/tupletablerowcontent) — 一种表格列内容类型，可根据由表格行组成的 Swift 元组创建表格行。
- [TableForEachContent](https://developer.apple.com/documentation/swiftui/tableforeachcontent) — 一种表格行内容类型，可通过遍历集合创建表格行。
- [EmptyTableRowContent](https://developer.apple.com/documentation/swiftui/emptytablerowcontent) — 不产生任何行的表格行内容。
- [DynamicTableRowContent](https://developer.apple.com/documentation/swiftui/dynamictablerowcontent) — 一种表格行内容类型，可根据底层数据集合生成表格行。
- [TableRowBuilder](https://developer.apple.com/documentation/swiftui/tablerowbuilder) — 一种结果构建器，根据闭包创建表格行内容。

## 添加逐级展开 {#Adding-progressive-disclosure}

- [DisclosureTableRow](https://developer.apple.com/documentation/swiftui/disclosuretablerow) — 一种根据展开控件状态显示或隐藏额外行的表格行。
- [TableOutlineGroupContent](https://developer.apple.com/documentation/swiftui/tableoutlinegroupcontent) — 由表格的层级式初始化器创建的一种不透明表格行类型。
