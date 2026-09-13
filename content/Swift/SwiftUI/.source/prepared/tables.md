# Tables

Display selectable, sortable data arranged in rows and columns.

## Overview {#Overview}

Use a table to display multiple values across a collection of elements. Each element in the collection appears in a different row of the table, while each value for a given element appears in a different column. Narrow displays may adapt to show only the first column of the table.

![](./images/tables-hero@2x.png)

When you create a table, you provide a collection of elements, and then tell the table how to find the needed value for each column. In simple cases, SwiftUI infers the element for each row, but you can also specify the row elements explicitly in more complex scenarios. With a small amount of additional configuration, you can also make the items in the table selectable, and the columns sortable.

Like a [List](https://developer.apple.com/documentation/swiftui/list), a table includes implicit vertical scrolling that you can configure using the view modifiers described in [Scroll views](../7-ScrollViews/). For design guidance, see [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables) in the Human Interface Guidelines.

## Creating a table {#Creating-a-table}

- [Building a great Mac app with SwiftUI](5.1-BuildingAGreatMacAppWithSwiftui/) — Create engaging SwiftUI Mac apps by incorporating side bars, tables, toolbars, and several other popular user interface elements.
- [Table](https://developer.apple.com/documentation/swiftui/table) — A container that presents rows of data arranged in one or more columns, optionally providing the ability to select one or more members.
- [tableStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tablestyle(_:)) — Sets the style for tables within this view.

## Creating columns {#Creating-columns}

- [TableColumn](https://developer.apple.com/documentation/swiftui/tablecolumn) — A column that displays a view for each row in a table.
- [TableColumnContent](https://developer.apple.com/documentation/swiftui/tablecolumncontent) — A type used to represent columns within a table.
- [TableColumnAlignment](https://developer.apple.com/documentation/swiftui/tablecolumnalignment) — Describes the alignment of the content of a table column.
- [TableColumnBuilder](https://developer.apple.com/documentation/swiftui/tablecolumnbuilder) — A result builder that creates table column content from closures.
- [TableColumnForEach](https://developer.apple.com/documentation/swiftui/tablecolumnforeach) — A structure that computes columns on demand from an underlying collection of identified data.

## Customizing columns {#Customizing-columns}

- [tableColumnHeaders(_:)](https://developer.apple.com/documentation/swiftui/view/tablecolumnheaders(_:)) — Controls the visibility of a `Table`’s column header views.
- [TableColumnCustomization](https://developer.apple.com/documentation/swiftui/tablecolumncustomization) — A representation of the state of the columns in a table.
- [TableColumnCustomizationBehavior](https://developer.apple.com/documentation/swiftui/tablecolumncustomizationbehavior) — A set of customization behaviors of a column that a table can offer to a user.

## Creating rows {#Creating-rows}

- [TableRow](https://developer.apple.com/documentation/swiftui/tablerow) — A row that represents a data value in a table.
- [TableRowContent](https://developer.apple.com/documentation/swiftui/tablerowcontent) — A type used to represent table rows.
- [TableHeaderRowContent](https://developer.apple.com/documentation/swiftui/tableheaderrowcontent) — A table row that displays a single view instead of columned content.
- [TupleTableRowContent](https://developer.apple.com/documentation/swiftui/tupletablerowcontent) — A type of table column content that creates table rows created from a Swift tuple of table rows.
- [TableForEachContent](https://developer.apple.com/documentation/swiftui/tableforeachcontent) — A type of table row content that creates table rows created by iterating over a collection.
- [EmptyTableRowContent](https://developer.apple.com/documentation/swiftui/emptytablerowcontent) — A table row content that doesn’t produce any rows.
- [DynamicTableRowContent](https://developer.apple.com/documentation/swiftui/dynamictablerowcontent) — A type of table row content that generates table rows from an underlying collection of data.
- [TableRowBuilder](https://developer.apple.com/documentation/swiftui/tablerowbuilder) — A result builder that creates table row content from closures.

## Adding progressive disclosure {#Adding-progressive-disclosure}

- [DisclosureTableRow](https://developer.apple.com/documentation/swiftui/disclosuretablerow) — A kind of table row that shows or hides additional rows based on the state of a disclosure control.
- [TableOutlineGroupContent](https://developer.apple.com/documentation/swiftui/tableoutlinegroupcontent) — An opaque table row type created by a table’s hierarchical initializers.
