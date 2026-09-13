# Appearance modifiers

Configure a view’s foreground and background styles, controls, and visibility.

## Overview {#Overview}

Use these modifiers to configure the appearance of a view, including the use of color and tint, and the application of overlays and background elements. Control the visibility of a view and specific elements within a view. Manage the shape and size of various controls.

For information about configuring views, see [View configuration](../../2-ViewConfiguration/).

## Colors and patterns {#Colors-and-patterns}

- [backgroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/backgroundstyle(_:)) — Sets the specified style to render backgrounds within the view.
- [foregroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:)) — Sets a view’s foreground elements to use a given style.
- [foregroundStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:)) — Sets the primary and secondary levels of the foreground style in the child view.
- [foregroundStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)) — Sets the primary, secondary, and tertiary levels of the foreground style.
- [allowedDynamicRange(_:)](https://developer.apple.com/documentation/swiftui/view/alloweddynamicrange(_:)) — Returns a new view configured with the specified allowed dynamic range.

## Tint {#Tint}

- [tint(_:)](https://developer.apple.com/documentation/swiftui/view/tint(_:)) — Sets the tint color within this view.
- [listRowSeparatorTint(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listrowseparatortint(_:edges:)) — Sets the tint color associated with a row.
- [listSectionSeparatorTint(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listsectionseparatortint(_:edges:)) — Sets the tint color associated with a section.
- [listItemTint(_:)](https://developer.apple.com/documentation/swiftui/view/listitemtint(_:)) — Sets a fixed tint color for content in a list.

## Light and dark appearance {#Light-and-dark-appearance}

- [preferredColorScheme(_:)](https://developer.apple.com/documentation/swiftui/view/preferredcolorscheme(_:)) — Sets the preferred color scheme for this presentation.
- [preferredSurroundingsEffect(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsurroundingseffect(_:)) — Applies an effect to passthrough video.

## Foreground elements {#Foreground-elements}

- [border(_:width:)](https://developer.apple.com/documentation/swiftui/view/border(_:width:)) — Adds a border to this view with the specified style and width.
- [overlay(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/overlay(alignment:content:)) — Layers the views that you specify in front of this view.
- [overlay(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:ignoressafeareaedges:)) — Layers the specified style in front of this view.
- [overlay(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:in:fillstyle:)) — Layers a shape that you specify in front of this view.
- [spatialOverlay(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/spatialoverlay(alignment:content:)) — Adds secondary views within the 3D bounds of this view.
- [spatialOverlayPreferenceValue(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/spatialoverlaypreferencevalue(_:alignment:_:)) — Uses the specified preference value from the view to produce another view occupying the same 3D space of the first view.

## Background elements {#Background-elements}

- [background(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/background(alignment:content:)) — Layers the views that you specify behind this view.
- [background(_:ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(_:ignoressafeareaedges:)) — Sets the view’s background to a style.
- [background(ignoresSafeAreaEdges:)](https://developer.apple.com/documentation/swiftui/view/background(ignoressafeareaedges:)) — Sets the view’s background to the default background style.
- [background(_:in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(_:in:fillstyle:)) — Sets the view’s background to an insettable shape filled with a style.
- [background(in:fillStyle:)](https://developer.apple.com/documentation/swiftui/view/background(in:fillstyle:)) — Sets the view’s background to an insettable shape filled with the default background style.
- [alternatingRowBackgrounds(_:)](https://developer.apple.com/documentation/swiftui/view/alternatingrowbackgrounds(_:)) — Overrides whether lists and tables in this view have alternating row backgrounds.
- [listRowBackground(_:)](https://developer.apple.com/documentation/swiftui/view/listrowbackground(_:)) — Places a custom background view behind a list row item.
- [scrollContentBackground(_:)](https://developer.apple.com/documentation/swiftui/view/scrollcontentbackground(_:)) — Specifies the visibility of the background for scrollable views within this view.
- [containerBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(_:for:)) — Sets the container background of the enclosing container using a view.
- [containerBackground(for:alignment:content:)](https://developer.apple.com/documentation/swiftui/view/containerbackground(for:alignment:content:)) — Sets the container background of the enclosing container using a view.
- [glassBackgroundEffect(displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(displaymode:)) — Fills the view’s background with an automatic glass background effect and container-relative rounded rectangle shape.
- [glassBackgroundEffect(_:displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(_:displaymode:)) — Fills the view’s background with a custom glass background effect and container-relative rounded rectangle shape.
- [glassBackgroundEffect(in:displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(in:displaymode:)) — Fills the view’s background with an automatic glass background effect and a shape that you specify.
- [glassBackgroundEffect(_:in:displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(_:in:displaymode:)) — Fills the view’s background with a custom glass background effect and a shape that you specify.
- [backgroundExtensionEffect()](https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect()) — Adds the background extension effect to the view. The view will be duplicated into mirrored copies which will be placed around the view on any edge with available safe area. Additionally, a blur effect will be applied on top to blur out the copies.
- [backgroundExtensionEffect(isEnabled:)](https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect(isenabled:)) — Adds the background extension effect to the view. The view will be duplicated into mirrored copies which will be placed around the view on any edge with available safe area. Additionally, a blur effect will be applied on top to blur out the copies.

## Passthrough {#Passthrough}

- [breakthroughEffect(_:)](https://developer.apple.com/documentation/swiftui/view/breakthrougheffect(_:)) — Ensures that the view is always visible to the user, even when other content is occluding it, like 3D models.

## Control configuration {#Control-configuration}

- [defaultWheelPickerItemHeight(_:)](https://developer.apple.com/documentation/swiftui/view/defaultwheelpickeritemheight(_:)) — Sets the default wheel-style picker item height.
- [horizontalRadioGroupLayout()](https://developer.apple.com/documentation/swiftui/view/horizontalradiogrouplayout()) — Sets the style for radio group style pickers within this view to be horizontally positioned with the radio buttons inside the layout.
- [controlSize(_:)](https://developer.apple.com/documentation/swiftui/view/controlsize(_:)) — Sets the size for controls within this view.
- [buttonBorderShape(_:)](https://developer.apple.com/documentation/swiftui/view/buttonbordershape(_:)) — Sets the border shape for buttons in this view.
- [buttonRepeatBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/buttonrepeatbehavior(_:)) — Sets whether buttons in this view should repeatedly trigger their actions on prolonged interactions.
- [headerProminence(_:)](https://developer.apple.com/documentation/swiftui/view/headerprominence(_:)) — Sets the header prominence for this view.
- [scrollDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldisabled(_:)) — Disables or enables scrolling in scrollable views.
- [scrollBounceBehavior(_:axes:)](https://developer.apple.com/documentation/swiftui/view/scrollbouncebehavior(_:axes:)) — Configures the bounce behavior of scrollable views along the specified axis.
- [scrollIndicatorsFlash(onAppear:)](https://developer.apple.com/documentation/swiftui/view/scrollindicatorsflash(onappear:)) — Flashes the scroll indicators of a scrollable view when it appears.
- [scrollIndicatorsFlash(trigger:)](https://developer.apple.com/documentation/swiftui/view/scrollindicatorsflash(trigger:)) — Flashes the scroll indicators of scrollable views when a value changes.
- [menuOrder(_:)](https://developer.apple.com/documentation/swiftui/view/menuorder(_:)) — Sets the preferred order of items for menus presented from this view.
- [menuActionDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/menuactiondismissbehavior(_:)) — Tells a menu whether to dismiss after performing an action.
- [paletteSelectionEffect(_:)](https://developer.apple.com/documentation/swiftui/view/paletteselectioneffect(_:)) — Specifies the selection effect to apply to a palette item.
- [typeSelectEquivalent(_:)](https://developer.apple.com/documentation/swiftui/view/typeselectequivalent(_:)) — Sets an explicit type select equivalent text in a collection, such as a list or table.

## Symbol effects {#Symbol-effects}

- [symbolEffect(_:options:isActive:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:isactive:)) — Returns a new view with a symbol effect added to it.
- [symbolEffect(_:options:value:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:value:)) — Returns a new view with a symbol effect added to it.
- [symbolEffectsRemoved(_:)](https://developer.apple.com/documentation/swiftui/view/symboleffectsremoved(_:)) — Returns a new view with its inherited symbol image effects either removed or left unchanged.

## Privacy and redaction {#Privacy-and-redaction}

- [privacySensitive(_:)](https://developer.apple.com/documentation/swiftui/view/privacysensitive(_:)) — Marks the view as containing sensitive, private user data.
- [redacted(reason:)](https://developer.apple.com/documentation/swiftui/view/redacted(reason:)) — Adds a reason to apply a redaction to this view hierarchy.
- [unredacted()](https://developer.apple.com/documentation/swiftui/view/unredacted()) — Removes any reason to apply a redaction to this view hierarchy.
- [invalidatableContent(_:)](https://developer.apple.com/documentation/swiftui/view/invalidatablecontent(_:)) — Mark the receiver as their content might be invalidated.
- [contentCaptureProtected(_:)](https://developer.apple.com/documentation/swiftui/view/contentcaptureprotected(_:))

## Visibility {#Visibility}

- [hidden()](https://developer.apple.com/documentation/swiftui/view/hidden()) — Hides this view unconditionally.
- [labelsHidden()](https://developer.apple.com/documentation/swiftui/view/labelshidden()) — Hides the labels of any controls contained within this view.
- [labelsVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/labelsvisibility(_:)) — Controls the visibility of labels of any controls contained within this view.
- [menuIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/menuindicator(_:)) — Sets the menu indicator visibility for controls within this view.
- [listRowSeparator(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listrowseparator(_:edges:)) — Sets the display mode for the separator associated with this specific row.
- [listSectionSeparator(_:edges:)](https://developer.apple.com/documentation/swiftui/view/listsectionseparator(_:edges:)) — Sets whether to hide the separator associated with a list section.
- [listSectionIndexVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/listsectionindexvisibility(_:)) — Changes the visibility of the list section index.
- [persistentSystemOverlays(_:)](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:)) — Sets the preferred visibility of the non-transient system views overlaying the app.
- [scrollIndicators(_:axes:)](https://developer.apple.com/documentation/swiftui/view/scrollindicators(_:axes:)) — Sets the visibility of scroll indicators within this view.
- [scrollClipDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/scrollclipdisabled(_:)) — Sets whether a scroll view clips its content to its bounds.
- [sliderThumbVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/sliderthumbvisibility(_:)) — Sets the thumb visibility for `Slider`s within this view.
- [tableColumnHeaders(_:)](https://developer.apple.com/documentation/swiftui/view/tablecolumnheaders(_:)) — Controls the visibility of a `Table`’s column header views.
- [upperLimbVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/upperlimbvisibility(_:)) — Sets the preferred visibility of the user’s upper limbs, while an [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace) scene is presented.
- [volumeBaseplateVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/volumebaseplatevisibility(_:)) — Sets the visibility of the baseplate of a volume, which appears when a user looks towards the ‘floor’ of a volume and during resize. Both `automatic` and `visible` will show the baseplate. `hidden` will never show it.

## Sensory feedback {#Sensory-feedback}

- [sensoryFeedback(_:trigger:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:)) — Plays the specified `feedback` when the provided `trigger` value changes.
- [sensoryFeedback(trigger:_:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(trigger:_:)) — Plays feedback when returned from the `feedback` closure after the provided `trigger` value changes.
- [sensoryFeedback(_:trigger:condition:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:condition:)) — Plays the specified `feedback` when the provided `trigger` value changes and the `condition` closure returns `true`.

## Widget configuration {#Widget-configuration}

- [widgetAccentable(_:)](https://developer.apple.com/documentation/swiftui/view/widgetaccentable(_:)) — Adds the view and all of its subviews to the accented group.
- [widgetCurvesContent(_:)](https://developer.apple.com/documentation/swiftui/view/widgetcurvescontent(_:)) — Displays the widget’s content along a curve if the context allows it.
- [widgetLabel(_:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(_:)) — Returns a localized text label that displays additional content outside the accessory family widget’s main SwiftUI view.
- [widgetLabel(label:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(label:)) — Creates a label for displaying additional content outside an accessory family widget’s main SwiftUI view.
- [dynamicIsland(verticalPlacement:)](https://developer.apple.com/documentation/swiftui/view/dynamicisland(verticalplacement:)) — Specifies the vertical placement for a view of an expanded Live Activity that appears in the Dynamic Island.
- [accessoryWidgetGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/accessorywidgetgroupstyle(_:)) — The view modifier that can be applied to `AccessoryWidgetGroup` to specify the shape the three content views will be masked with. The value of `style` is set to `.automatic`, which is `.circular` by default.
- [controlWidgetActionHint(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetactionhint(_:)) — The action hint of the control described by the modified label.
- [controlWidgetStatus(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetstatus(_:)) — The status of the control described by the modified label.

## Window behaviors {#Window-behaviors}

- [windowDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowdismissbehavior(_:)) — Configures the dismiss functionality for the window enclosing `self`.
- [windowFullScreenBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowfullscreenbehavior(_:)) — Configures the full screen functionality for the window enclosing `self`.
- [windowToolbarFullScreenVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/windowtoolbarfullscreenvisibility(_:)) — Configures the visibility of the window toolbar when the window enters full screen mode.
- [windowMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowminimizebehavior(_:)) — Configures the minimize functionality for the window enclosing `self`.
- [windowResizeAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/windowresizeanchor(_:)) — Sets the window anchor point used when the size of the view changes such that the window must resize.
- [windowResizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowresizebehavior(_:)) — Configures the resize functionality for the window enclosing `self`.
- [preferredWindowClippingMargins(_:_:)](https://developer.apple.com/documentation/swiftui/view/preferredwindowclippingmargins(_:_:)) — Requests additional margins for drawing beyond the bounds of the window.
