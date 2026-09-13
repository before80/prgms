# Layout adjustments

Make fine adjustments to alignment, spacing, padding, and other layout parameters.

## Overview {#Overview}

Layout containers like stacks and grids provide a great starting point for arranging views in your app’s user interface. When you need to make fine adjustments, use layout view modifiers. You can adjust or constrain the size, position, and alignment of a view. You can also add padding around a view, and indicate how the view interacts with system-defined safe areas.

![](./images/layout-adjustments-hero@2x.png)

To get started with a basic layout, see [Layout fundamentals](../1-LayoutFundamentals/). For design guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) in the Human Interface Guidelines.

## Fine-tuning a layout {#Fine-tuning-a-layout}

- [Laying out a simple view](2.1-LayingOutASimpleView/) — Create a view layout by adjusting the size of views.
- [Inspecting view layout](2.2-InspectingViewLayout/) — Determine the position and extent of a view using Xcode previews or by adding temporary borders.

## Adding padding around a view {#Adding-padding-around-a-view}

- [padding(_:)](https://developer.apple.com/documentation/swiftui/view/padding(_:)) — Adds a different padding amount to each edge of this view.
- [padding(_:_:)](https://developer.apple.com/documentation/swiftui/view/padding(_:_:)) — Adds an equal padding amount to specific edges of this view.
- [padding3D(_:)](https://developer.apple.com/documentation/swiftui/view/padding3d(_:)) — Pads this view using the edge insets you specify.
- [padding3D(_:_:)](https://developer.apple.com/documentation/swiftui/view/padding3d(_:_:)) — Pads this view using the edge insets you specify.
- [scenePadding(_:)](https://developer.apple.com/documentation/swiftui/view/scenepadding(_:)) — Adds padding to the specified edges of this view using an amount that’s appropriate for the current scene.
- [scenePadding(_:edges:)](https://developer.apple.com/documentation/swiftui/view/scenepadding(_:edges:)) — Adds a specified kind of padding to the specified edges of this view using an amount that’s appropriate for the current scene.
- [ScenePadding](https://developer.apple.com/documentation/swiftui/scenepadding) — The padding used to space a view from its containing scene.

## Influencing a view’s size {#Influencing-a-views-size}

- [frame(width:height:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(width:height:alignment:)) — Positions this view within an invisible frame with the specified size.
- [frame(depth:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(depth:alignment:)) — Positions this view within an invisible frame with the specified depth.
- [frame(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(minwidth:idealwidth:maxwidth:minheight:idealheight:maxheight:alignment:)) — Positions this view within an invisible frame having the specified size constraints.
- [frame(minDepth:idealDepth:maxDepth:alignment:)](https://developer.apple.com/documentation/swiftui/view/frame(mindepth:idealdepth:maxdepth:alignment:)) — Positions this view within an invisible frame having the specified depth constraints.
- [containerRelativeFrame(_:alignment:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:)) — Positions this view within an invisible frame with a size relative to the nearest container.
- [containerRelativeFrame(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:_:)) — Positions this view within an invisible frame with a size relative to the nearest container.
- [containerRelativeFrame(_:count:span:spacing:alignment:)](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:count:span:spacing:alignment:)) — Positions this view within an invisible frame with a size relative to the nearest container.
- [fixedSize()](https://developer.apple.com/documentation/swiftui/view/fixedsize()) — Fixes this view at its ideal size.
- [fixedSize(horizontal:vertical:)](https://developer.apple.com/documentation/swiftui/view/fixedsize(horizontal:vertical:)) — Fixes this view at its ideal size in the specified dimensions.
- [layoutPriority(_:)](https://developer.apple.com/documentation/swiftui/view/layoutpriority(_:)) — Sets the priority by which a parent layout should apportion space to this child.

## Adjusting a view’s position {#Adjusting-a-views-position}

- [Making fine adjustments to a view’s position](2.3-MakingFineAdjustmentsToAViewSPosition/) — Shift the position of a view by applying the offset or position modifier.
- [position(_:)](https://developer.apple.com/documentation/swiftui/view/position(_:)) — Positions the center of this view at the specified point in its parent’s coordinate space.
- [position(x:y:)](https://developer.apple.com/documentation/swiftui/view/position(x:y:)) — Positions the center of this view at the specified coordinates in its parent’s coordinate space.
- [offset(_:)](https://developer.apple.com/documentation/swiftui/view/offset(_:)) — Offset this view by the horizontal and vertical amount specified in the offset parameter.
- [offset(x:y:)](https://developer.apple.com/documentation/swiftui/view/offset(x:y:)) — Offset this view by the specified horizontal and vertical distances.
- [offset(z:)](https://developer.apple.com/documentation/swiftui/view/offset(z:)) — Brings a view forward in Z by the provided distance in points.

## Aligning views {#Aligning-views}

- [Aligning views within a stack](2.4-AligningViewsWithinAStack/) — Position views inside a stack using alignment guides.
- [Aligning views across stacks](2.5-AligningViewsAcrossStacks/) — Create a custom alignment and use it to align views across multiple stacks.
- [alignmentGuide(_:computeValue:)](https://developer.apple.com/documentation/swiftui/view/alignmentguide(_:computevalue:)) — Sets the view’s horizontal alignment.
- [Alignment](https://developer.apple.com/documentation/swiftui/alignment) — An alignment in both axes.
- [HorizontalAlignment](https://developer.apple.com/documentation/swiftui/horizontalalignment) — An alignment position along the horizontal axis.
- [VerticalAlignment](https://developer.apple.com/documentation/swiftui/verticalalignment) — An alignment position along the vertical axis.
- [DepthAlignment](https://developer.apple.com/documentation/swiftui/depthalignment) — An alignment position along the depth axis.
- [AlignmentID](https://developer.apple.com/documentation/swiftui/alignmentid) — A type that you use to create custom alignment guides.
- [ViewDimensions](https://developer.apple.com/documentation/swiftui/viewdimensions) — A view’s size and alignment guides in its own coordinate space.
- [ViewDimensions3D](https://developer.apple.com/documentation/swiftui/viewdimensions3d) — A view’s 3D size and alignment guides in its own coordinate space.
- [SpatialContainer](https://developer.apple.com/documentation/swiftui/spatialcontainer) — A layout container that aligns overlapping content in 3D space.

## Setting margins {#Setting-margins}

- [contentMargins(_:for:)](https://developer.apple.com/documentation/swiftui/view/contentmargins(_:for:)) — Configures the content margin for a provided placement.
- [contentMargins(_:_:for:)](https://developer.apple.com/documentation/swiftui/view/contentmargins(_:_:for:)) — Configures the content margin for a provided placement.
- [ContentMarginPlacement](https://developer.apple.com/documentation/swiftui/contentmarginplacement) — The placement of margins.

## Staying in the safe areas {#Staying-in-the-safe-areas}

- [ignoresSafeArea(_:edges:)](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)) — Expands the safe area of a view.
- [ignoresSafeArea(_:edges:alignment:)](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:alignment:)) — Expands the safe area of a view aligning content within the new bounds using the provided alignment.
- [safeAreaInset(edge:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/safeareainset(edge:alignment:spacing:content:)) — Shows the specified content beside the modified view.
- [safeAreaPadding(_:)](https://developer.apple.com/documentation/swiftui/view/safeareapadding(_:)) — Adds the provided insets into the safe area of this view.
- [safeAreaPadding(_:_:)](https://developer.apple.com/documentation/swiftui/view/safeareapadding(_:_:)) — Adds the provided insets into the safe area of this view.
- [SafeAreaRegions](https://developer.apple.com/documentation/swiftui/safearearegions) — A set of symbolic safe area regions.

## Setting a layout direction {#Setting-a-layout-direction}

- [layoutDirectionBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/layoutdirectionbehavior(_:)) — Sets the behavior of this view for different layout directions.
- [LayoutDirectionBehavior](https://developer.apple.com/documentation/swiftui/layoutdirectionbehavior) — A description of what should happen when the layout direction changes.
- [layoutDirection](https://developer.apple.com/documentation/swiftui/environmentvalues/layoutdirection) — The layout direction associated with the current environment.
- [LayoutDirection](https://developer.apple.com/documentation/swiftui/layoutdirection) — A direction in which SwiftUI can lay out content.
- [LayoutRotationUnaryLayout](https://developer.apple.com/documentation/swiftui/layoutrotationunarylayout)

## Reacting to interface characteristics {#Reacting-to-interface-characteristics}

- [isLuminanceReduced](https://developer.apple.com/documentation/swiftui/environmentvalues/isluminancereduced) — A Boolean value that indicates whether the display or environment currently requires reduced luminance.
- [displayScale](https://developer.apple.com/documentation/swiftui/environmentvalues/displayscale) — The display scale of this environment.
- [pixelLength](https://developer.apple.com/documentation/swiftui/environmentvalues/pixellength) — The size of a pixel on the screen.
- [horizontalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/horizontalsizeclass) — The horizontal size class of this environment.
- [verticalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/verticalsizeclass) — The vertical size class of this environment.
- [UserInterfaceSizeClass](https://developer.apple.com/documentation/swiftui/userinterfacesizeclass) — A set of values that indicate the visual size available to the view.

## Accessing edges, regions, and layouts {#Accessing-edges-regions-and-layouts}

- [Edge](https://developer.apple.com/documentation/swiftui/edge) — An enumeration to indicate one edge of a rectangle.
- [Edge3D](https://developer.apple.com/documentation/swiftui/edge3d) — An edge or face of a 3D volume.
- [HorizontalEdge](https://developer.apple.com/documentation/swiftui/horizontaledge) — An edge on the horizontal axis.
- [VerticalEdge](https://developer.apple.com/documentation/swiftui/verticaledge) — An edge on the vertical axis.
- [EdgeInsets](https://developer.apple.com/documentation/swiftui/edgeinsets) — The inset distances for the sides of a rectangle.
- [EdgeInsets3D](https://developer.apple.com/documentation/swiftui/edgeinsets3d) — The inset distances for the faces of a 3D volume.
