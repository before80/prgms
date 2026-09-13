# Lists

Display a structured, scrollable column of information.

## Overview {#Overview}

Use a list to display a one-dimensional vertical collection of views.

![](./images/lists-hero@2x.png)

The list is a complex container type that automatically provides scrolling when it grows too large for the current display. You build a list by providing it with individual views for the rows in the list, or by using a [ForEach](https://developer.apple.com/documentation/swiftui/foreach) to enumerate a group of rows. You can also mix these strategies, blending any number of individual views and `ForEach` constructs.

Use view modifiers to configure the appearance and behavior of a list and its rows, headers, sections, and separators. For example, you can apply a style to the list, add swipe gestures to individual rows, or make the list refreshable with a pull-down gesture. You can also use the configuration associated with [Scroll views](../7-ScrollViews/) to control the list’s implicit scrolling behavior.

For design guidance, see [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables) in the Human Interface Guidelines.

## Creating a list {#Creating-a-list}

- [Displaying data in lists](4.1-DisplayingDataInLists/) — Visualize collections of data with platform-appropriate appearance.
- [List](https://developer.apple.com/documentation/swiftui/list) — A container that presents rows of data arranged in a single column, optionally providing the ability to select one or more members.
- [listStyle(_:)](https://developer.apple.com/documentation/swiftui/view/liststyle(_:)) — Sets the style for lists within this view.

## Disclosing information progressively {#Disclosing-information-progressively}

- [OutlineGroup](https://developer.apple.com/documentation/swiftui/outlinegroup) — A structure that computes views and disclosure groups on demand from an underlying collection of tree-structured, identified data.
- [DisclosureGroup](https://developer.apple.com/documentation/swiftui/disclosuregroup) — A view that shows or hides another content view, based on the state of a disclosure control.
- [disclosureGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/disclosuregroupstyle(_:)) — Sets the style for disclosure groups within this view.

## Configuring a list’s layout {#Configuring-a-lists-layout}

- [listRowInsets(_:)](https://developer.apple.com/documentation/swiftui/view/listrowinsets(_:)) — Applies an inset to the rows in a list.
- [listRowInsets(_:_:)](https://developer.apple.com/documentation/swiftui/view/listrowinsets(_:_:)) — Sets the insets of rows in a list on the specified edges.
- [defaultMinListRowHeight](https://developer.apple.com/documentation/swiftui/environmentvalues/defaultminlistrowheight) — The default minimum height of rows in a list.
- [defaultMinListHeaderHeight](https://developer.apple.com/documentation/swiftui/environmentvalues/defaultminlistheaderheight) — The default minimum height of a header in a list.
- [listRowSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/listrowspacing(_:)) — Sets the vertical spacing between two adjacent rows in a List.
- [listSectionSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/listsectionspacing(_:)) — Sets the spacing between adjacent sections in a [List](https://developer.apple.com/documentation/swiftui/list) to a custom value.
- [ListSectionSpacing](https://developer.apple.com/documentation/swiftui/listsectionspacing) — The spacing options between two adjacent sections in a list.
- [listSectionMargins(_:_:)](https://developer.apple.com/documentation/swiftui/view/listsectionmargins(_:_:)) — Set the section margins for the specific edges.

## Configuring rows {#Configuring-rows}

- [listItemTint(_:)](https://developer.apple.com/documentation/swiftui/view/listitemtint(_:)) — Sets a fixed tint color for content in a list.
- [ListItemTint](https://developer.apple.com/documentation/swiftui/listitemtint) — A tint effect configuration that you can apply to content in a list.

## Configuring headers {#Configuring-headers}

- [headerProminence(_:)](https://developer.apple.com/documentation/swiftui/view/headerprominence(_:)) — Sets the header prominence for this view.
- [headerProminence](https://developer.apple.com/documentation/swiftui/environmentvalues/headerprominence) — The prominence to apply to section headers within a view.
- [Prominence](https://developer.apple.com/documentation/swiftui/prominence) — A type indicating the prominence of a view hierarchy.

## Configuring separators {#Configuring-separators}

- [listRowSeparatorTint(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listrowseparatortint(_:edges:)) — Sets the tint color associated with a row.
- [listSectionSeparatorTint(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listsectionseparatortint(_:edges:)) — Sets the tint color associated with a section.
- [listRowSeparator(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listrowseparator(_:edges:)) — Sets the display mode for the separator associated with this specific row.
- [listSectionSeparator(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listsectionseparator(_:edges:)) — Sets whether to hide the separator associated with a list section.

## Configuring backgrounds {#Configuring-backgrounds}

- [listRowBackground(_:)](https://developer.apple.com/documentation/swiftui/view/listrowbackground(_:)) — Places a custom background view behind a list row item.
- [alternatingRowBackgrounds(_:)](https://developer.apple.com/documentation/swiftui/view/alternatingrowbackgrounds(_:)) — Overrides whether lists and tables in this view have alternating row backgrounds.
- [AlternatingRowBackgroundBehavior](https://developer.apple.com/documentation/swiftui/alternatingrowbackgroundbehavior) — The styling of views with respect to alternating row backgrounds.
- [backgroundProminence](https://developer.apple.com/documentation/swiftui/environmentvalues/backgroundprominence) — The prominence of the background underneath views associated with this environment.
- [BackgroundProminence](https://developer.apple.com/documentation/swiftui/backgroundprominence) — The prominence of backgrounds underneath other views.

## Displaying a badge on a list item {#Displaying-a-badge-on-a-list-item}

- [badge(_:)](https://developer.apple.com/documentation/swiftui/view/badge(_:)) — Generates a badge for the view from a localized string resource.
- [badgeProminence(_:)](https://developer.apple.com/documentation/swiftui/view/badgeprominence(_:)) — Specifies the prominence of badges created by this view.
- [badgeProminence](https://developer.apple.com/documentation/swiftui/environmentvalues/badgeprominence) — The prominence to apply to badges associated with this environment.
- [BadgeProminence](https://developer.apple.com/documentation/swiftui/badgeprominence) — The visual prominence of a badge.

## Configuring interaction {#Configuring-interaction}

- [swipeActions(edge:allowsFullSwipe:content:)](https://developer.apple.com/documentation/swiftui/view/swipeactions(edge:allowsfullswipe:content:)) — Adds custom swipe actions to a row in a list.
- [selectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/selectiondisabled(_:)) — Adds a condition that controls whether users can select this view.
- [listRowHoverEffect(_:)](https://developer.apple.com/documentation/swiftui/view/listrowhovereffect(_:)) — Requests that the containing list row use the provided hover effect.
- [listRowHoverEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/listrowhovereffectdisabled(_:)) — Requests that the containing list row have its hover effect disabled.

## Refreshing a list’s content {#Refreshing-a-lists-content}

- [refreshable(action:)](https://developer.apple.com/documentation/swiftui/view/refreshable(action:)) — Adds an asynchronous handler that can update the data the view displays when a person initiates a request, such as by pulling to refresh.
- [refresh](https://developer.apple.com/documentation/swiftui/environmentvalues/refresh) — A refresh action stored in a view’s environment.
- [RefreshAction](https://developer.apple.com/documentation/swiftui/refreshaction) — An action that initiates a refresh operation.

## Editing a list {#Editing-a-list}

- [moveDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/movedisabled(_:)) — Adds a condition for whether the view’s view hierarchy is movable.
- [deleteDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/deletedisabled(_:)) — Adds a condition for whether the view’s view hierarchy is deletable.
- [editMode](https://developer.apple.com/documentation/swiftui/environmentvalues/editmode) — An indication of whether the user can edit the contents of a view associated with this environment.
- [EditMode](https://developer.apple.com/documentation/swiftui/editmode) — A mode that indicates whether the user can edit a view’s content.
- [EditActions](https://developer.apple.com/documentation/swiftui/editactions) — A set of edit actions on a collection of data that a view can offer to a user.
- [EditableCollectionContent](https://developer.apple.com/documentation/swiftui/editablecollectioncontent) — An opaque wrapper view that adds editing capabilities to a row in a list.
- [IndexedIdentifierCollection](https://developer.apple.com/documentation/swiftui/indexedidentifiercollection) — A collection wrapper that iterates over the indices and identifiers of a collection together.

## Configuring a section index {#Configuring-a-section-index}

- [listSectionIndexVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/listsectionindexvisibility(_:)) — Changes the visibility of the list section index.
- [sectionIndexLabel(_:)](https://developer.apple.com/documentation/swiftui/view/sectionindexlabel(_:)) — Sets the label that is used in a section index to point to this section, typically only a single character long.
