# Layout fundamentals

Arrange views inside built-in layout containers like stacks and grids.

## Overview {#Overview}

Use layout containers to arrange the elements of your user interface. Stacks and grids update and adjust the positions of the subviews they contain in response to changes in content or interface dimensions. You can nest layout containers inside other layout containers to any depth to achieve complex layout effects.

![](./images/layout-fundamentals-hero@2x.png)

To fine-tune the position, alignment, and other elements of a layout that you build with layout container views, see [Layout adjustments](../2-LayoutAdjustments/). To define custom layout containers, see [Custom layout](../3-CustomLayout/). For design guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) in the Human Interface Guidelines.

## Choosing a layout {#Choosing-a-layout}

- [Picking container views for your content](1.1-PickingContainerViewsForYourContent/) — Build flexible user interfaces by using stacks, grids, lists, and forms.

## Statically arranging views in one dimension {#Statically-arranging-views-in-one-dimension}

- [Building layouts with stack views](1.2-BuildingLayoutsWithStackViews/) — Compose complex layouts from primitive container views.
- [HStack](https://developer.apple.com/documentation/swiftui/hstack) — A view that arranges its subviews in a horizontal line.
- [VStack](https://developer.apple.com/documentation/swiftui/vstack) — A view that arranges its subviews in a vertical line.

## Dynamically arranging views in one dimension {#Dynamically-arranging-views-in-one-dimension}

- [Grouping data with lazy stack views](1.3-GroupingDataWithLazyStackViews/) — Split content into logical sections inside lazy stack views.
- [Creating performant scrollable stacks](1.4-CreatingPerformantScrollableStacks/) — Display large numbers of repeated views efficiently with scroll views, stack views, and lazy stacks.
- [LazyHStack](https://developer.apple.com/documentation/swiftui/lazyhstack) — A view that arranges its children in a line that grows horizontally, creating items only as needed.
- [LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack) — A view that arranges its children in a line that grows vertically, creating items only as needed.
- [PinnedScrollableViews](https://developer.apple.com/documentation/swiftui/pinnedscrollableviews) — A set of view types that may be pinned to the bounds of a scroll view.

## Statically arranging views in two dimensions {#Statically-arranging-views-in-two-dimensions}

- [Grid](https://developer.apple.com/documentation/swiftui/grid) — A container view that arranges other views in a two dimensional layout.
- [GridRow](https://developer.apple.com/documentation/swiftui/gridrow) — A horizontal row in a two dimensional grid container.
- [gridCellColumns(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellcolumns(_:)) — Tells a view that acts as a cell in a grid to span the specified number of columns.
- [gridCellAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellanchor(_:)) — Specifies a custom alignment anchor for a view that acts as a grid cell.
- [gridCellUnsizedAxes(_:)](https://developer.apple.com/documentation/swiftui/view/gridcellunsizedaxes(_:)) — Asks grid layouts not to offer the view extra size in the specified axes.
- [gridColumnAlignment(_:)](https://developer.apple.com/documentation/swiftui/view/gridcolumnalignment(_:)) — Overrides the default horizontal alignment of the grid column that the view appears in.

## Dynamically arranging views in two dimensions {#Dynamically-arranging-views-in-two-dimensions}

- [LazyHGrid](https://developer.apple.com/documentation/swiftui/lazyhgrid) — A container view that arranges its child views in a grid that grows horizontally, creating items only as needed.
- [LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid) — A container view that arranges its child views in a grid that grows vertically, creating items only as needed.
- [GridItem](https://developer.apple.com/documentation/swiftui/griditem) — A description of a row or a column in a lazy grid.

## Layering views {#Layering-views}

- [Adding a background to your view](1.5-AddingABackgroundToYourView/) — Compose a background behind your view and extend it beyond the safe area insets.
- [ZStack](https://developer.apple.com/documentation/swiftui/zstack) — A view that overlays its subviews, aligning them in both axes.
- [zIndex(_:)](https://developer.apple.com/documentation/swiftui/view/zindex(_:)) — Controls the display order of overlapping views.
- [background(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/background(alignment:content:)) — Layers the views that you specify behind this view.
- [background(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(_:ignoressafeareaedges:)) — Sets the view’s background to a style.
- [background(ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(ignoressafeareaedges:)) — Sets the view’s background to the default background style.
- [background(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(_:in:fillstyle:)) — Sets the view’s background to an insettable shape filled with a style.
- [background(in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(in:fillstyle:)) — Sets the view’s background to an insettable shape filled with the default background style.
- [overlay(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/overlay(alignment:content:)) — Layers the views that you specify in front of this view.
- [overlay(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:ignoressafeareaedges:)) — Layers the specified style in front of this view.
- [overlay(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:in:fillstyle:)) — Layers a shape that you specify in front of this view.
- [backgroundMaterial](https://developer.apple.com/documentation/swiftui/environmentvalues/backgroundmaterial) — The material underneath the current view.
- [containerBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(_:for:)) — Sets the container background of the enclosing container using a view.
- [containerBackground(for:alignment:content:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:)) — Sets the container background of the enclosing container using a view.
- [ContainerBackgroundPlacement](https://developer.apple.com/documentation/swiftui/containerbackgroundplacement) — The placement of a container background.

## Automatically choosing the layout that fits {#Automatically-choosing-the-layout-that-fits}

- [ViewThatFits](https://developer.apple.com/documentation/swiftui/viewthatfits) — A view that adapts to the available space by providing the first child view that fits.

## Separators {#Separators}

- [Spacer](https://developer.apple.com/documentation/swiftui/spacer) — A flexible space that expands along the major axis of its containing stack layout, or on both axes if not contained in a stack.
- [Divider](https://developer.apple.com/documentation/swiftui/divider) — A visual element that can be used to separate other content.
