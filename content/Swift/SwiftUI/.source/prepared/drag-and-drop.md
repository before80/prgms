# Drag and drop

Enable people to move or duplicate items by dragging them from one location to another.

## Overview {#Overview}

Drag and drop offers people a convenient way to move content from one part of your app to another, from one app to another, or to reorder content using an intuitive dragging gesture. Support this feature in your app by adding view modifiers to potential source and destination views within your app’s interface.

![](./images/drag-and-drop-hero@2x.png)

In your modifiers, provide or accept types that conform to the [Transferable](https://developer.apple.com/documentation/coretransferable/transferable) protocol, or that conform to [NSItemProviderReading](https://developer.apple.com/documentation/foundation/nsitemproviderreading) and/or [NSItemProviderWriting](https://developer.apple.com/documentation/foundation/nsitemproviderwriting). In Swift, prefer using transferable items.

For design guidance, see [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop) in the Human Interface Guidelines.

## Essentials {#Essentials}

- [Adopting drag and drop using SwiftUI](4.1-AdoptingDragAndDropUsingSwiftui/) — Enable drag-and-drop interactions in lists, tables and custom views.
- [Making a view into a drag source](4.2-MakingAViewIntoADragSource/) — Adopt draggable API to provide items for drag-and-drop operations.
- [Reordering items in lists, stacks, grids, and custom layouts](4.3-ReorderingItemsInListsStacksGridsAndCustomLayouts/) — Add drag-to-reorder interactions to SwiftUI layouts using reordering modifiers.

## Configuring drag-and-drop behavior {#Configuring-drag-and-drop-behavior}

- [dragConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dragconfiguration(_:)) — Configures a drag session.
- [DragConfiguration](https://developer.apple.com/documentation/swiftui/dragconfiguration) — The behavior of the drag, proposed by the dragging source. A value that describes the drag operations a drag source supports.
- [dropConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dropconfiguration(_:)) — Configures a drop session.
- [DropConfiguration](https://developer.apple.com/documentation/swiftui/dropconfiguration) — Describes the behavior of the drop.
- [dragContainer(for:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:in:_:)) — A container with draggable views where the drag payload is based on multiple identifiers of dragged items.
- [dragContainer(for:itemID:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:itemid:in:_:)) — A container with draggable views.
- [dragContainerSelection(_:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/dragcontainerselection(_:containernamespace:)) — Provides multiple item selection support for drag containers.

## Moving items {#Moving-items}

- [DragSession](https://developer.apple.com/documentation/swiftui/dragsession) — Describes the ongoing dragging session.
- [DropSession](https://developer.apple.com/documentation/swiftui/dropsession)

## Moving transferable items {#Moving-transferable-items}

- [draggable(_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:)) — Activates this view as the source of a drag and drop operation.
- [draggable(_:preview:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:preview:)) — Activates this view as the source of a drag and drop operation.
- [draggable(_:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:containernamespace:_:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional identifiable payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:id:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:containernamespace:_:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:id:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:item:containernamespace:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:item:containernamespace:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional identifiable payload and specify the namespace of the drag container this view belongs to.
- [draggable(containerItemID:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(containeritemid:containernamespace:)) — Inside a drag container, activates this view as the source of a drag and drop operation. Supports lazy drag containers.

## Moving items using item providers {#Moving-items-using-item-providers}

- [itemProvider(_:)](https://developer.apple.com/documentation/swiftui/view/itemprovider(_:)) — Provides a closure that vends the drag representation to be used for a particular data element.
- [onDrag(_:preview:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:preview:)) — Activates this view as the source of a drag and drop operation.
- [onDrag(_:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:)) — Activates this view as the source of a drag and drop operation.
- [onDrop(of:isTargeted:perform:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:istargeted:perform:)) — Defines the destination of a drag-and-drop operation that handles the dropped content with a closure that you specify.
- [onDrop(of:delegate:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:delegate:)) — Defines the destination of a drag and drop operation using behavior controlled by the delegate that you provide.
- [DropDelegate](https://developer.apple.com/documentation/swiftui/dropdelegate) — An interface that you implement to interact with a drop operation in a view modified to accept drops.
- [DropProposal](https://developer.apple.com/documentation/swiftui/dropproposal) — The behavior of a drop.
- [DropOperation](https://developer.apple.com/documentation/swiftui/dropoperation) — Operation types that determine how a drag and drop session resolves when the user drops a drag item.
- [DropInfo](https://developer.apple.com/documentation/swiftui/dropinfo) — The current state of a drop.

## Reordering items {#Reordering-items}

- [Making a card game with drag, drop, and reordering in SwiftUI](4.4-MakingACardGameWithDragDropAndReorderingInSwiftui/) — Move cards between positions in a card game using drag, drop, and reordering modifiers.
- [reorderable()](https://developer.apple.com/documentation/swiftui/dynamicviewcontent/reorderable()) — Enables reordering of views from this content inside the scope of a reorderable container modifier.
- [reorderable(collectionID:)](https://developer.apple.com/documentation/swiftui/dynamicviewcontent/reorderable(collectionid:)) — Enables reordering views from this content within and between sections in the scope of a reorderable container modifier.
- [ReorderableSingleCollectionIdentifier](https://developer.apple.com/documentation/swiftui/reorderablesinglecollectionidentifier) — An opaque, empty type used to identify reorderable containers and modifiers with only a single collection.
- [reorderContainer(for:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:isenabled:move:)) — Defines a container of reorderable views.
- [reorderContainer(for:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:in:isenabled:move:)) — Defines a container of reorderable views, with a type you specify to identify sections.
- [reorderContainer(for:itemID:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:isenabled:move:)) — Defines a container of reorderable views, with a type and keypath you specify to identify items.
- [reorderContainer(for:itemID:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:in:isenabled:move:)) — Defines a container of reorderable views, with a type and keypath you use to identify items and a type you use to identify collections.
- [reorderDestination(for:in:)](https://developer.apple.com/documentation/swiftui/dropsession/reorderdestination(for:in:)) — Provides the destination value of a reordering operation that occurred in the container associated with this drop destination modifier.
- [reorderDestination(for:itemID:in:)](https://developer.apple.com/documentation/swiftui/dropsession/reorderdestination(for:itemid:in:)) — Provides the destination value of a reordering operation that occurred in the container associated with this drop destination modifier.
- [ReorderDifference](https://developer.apple.com/documentation/swiftui/reorderdifference) — The difference that a reordering operation produces.

## Describing preview formations {#Describing-preview-formations}

- [dragPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/dragpreviewsformation(_:)) — Describes the way dragged previews are visually composed.
- [dropPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/droppreviewsformation(_:)) — Describes the way previews for a drop are composed.
- [DragDropPreviewsFormation](https://developer.apple.com/documentation/swiftui/dragdroppreviewsformation) — On macOS, describes the way the dragged previews are visually composed. Both drag sources and drop destination can specify their desired preview formation.

## Configuring spring loading {#Configuring-spring-loading}

- [springLoadingBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/springloadingbehavior(_:)) — Sets the spring loading behavior this view.
- [springLoadingBehavior](https://developer.apple.com/documentation/swiftui/environmentvalues/springloadingbehavior) — The behavior of spring loaded interactions for the views associated with this environment.
- [SpringLoadingBehavior](https://developer.apple.com/documentation/swiftui/springloadingbehavior) — The options for controlling the spring loading behavior of views.
