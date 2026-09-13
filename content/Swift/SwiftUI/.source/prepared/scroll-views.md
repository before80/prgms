# Scroll views

Enable people to scroll to content that doesn’t fit in the current display.

## Overview {#Overview}

When the content of a view doesn’t fit in the display, you can wrap the view in a [ScrollView](https://developer.apple.com/documentation/swiftui/scrollview) to enable people to scroll on one or more axes. Configure the scroll view using view modifiers. For example, you can set the visibility of the scroll indicators or the availability of scrolling in a given dimension.

![](./images/scroll-views-hero@2x.png)

You can put any view type in a scroll view, but you most often use a scroll view for a layout container with too many elements to fit in the display. For some container views that you put in a scroll view, like lazy stacks, the container doesn’t load views until they are visible or almost visible. For others, like regular stacks and grids, the container loads the content all at once, regardless of the state of scrolling.

[Lists](../4-Lists/) and [Tables](../5-Tables/) implicitly include a scroll view, so you don’t need to add scrolling to those container types. However, you can configure their implicit scroll views with the same view modifiers that apply to explicit scroll views.

For design guidance, see [Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views) in the Human Interface Guidelines.

## Creating a scroll view {#Creating-a-scroll-view}

- [ScrollView](https://developer.apple.com/documentation/swiftui/scrollview) — A scrollable view.
- [ScrollViewReader](https://developer.apple.com/documentation/swiftui/scrollviewreader) — A view that provides programmatic scrolling, by working with a proxy to scroll to known child views.
- [ScrollViewProxy](https://developer.apple.com/documentation/swiftui/scrollviewproxy) — A proxy value that supports programmatic scrolling of the scrollable views within a view hierarchy.

## Managing scroll position {#Managing-scroll-position}

- [scrollPosition(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/scrollposition(_:anchor:)) — Associates a binding to a scroll position with a scroll view within this view.
- [scrollPosition(id:anchor:)](https://developer.apple.com/documentation/swiftui/view/scrollposition(id:anchor:)) — Associates a binding to be updated when a scroll view within this view scrolls.
- [defaultScrollAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/defaultscrollanchor(_:)) — Associates an anchor to control which part of the scroll view’s content should be rendered by default.
- [defaultScrollAnchor(_:for:)](https://developer.apple.com/documentation/swiftui/view/defaultscrollanchor(_:for:)) — Associates an anchor to control the position of a scroll view in a particular circumstance.
- [ScrollAnchorRole](https://developer.apple.com/documentation/swiftui/scrollanchorrole) — A type defining the role of a scroll anchor.
- [ScrollPosition](https://developer.apple.com/documentation/swiftui/scrollposition) — A type that defines the semantic position of where a scroll view is scrolled within its content.

## Defining scroll targets {#Defining-scroll-targets}

- [scrollTargetBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/scrolltargetbehavior(_:)) — Sets the scroll behavior of views scrollable in the provided axes.
- [scrollTargetLayout(isEnabled:)](https://developer.apple.com/documentation/swiftui/view/scrolltargetlayout(isenabled:)) — Configures the outermost layout as a scroll target layout.
- [ScrollTarget](https://developer.apple.com/documentation/swiftui/scrolltarget) — A type defining the target in which a scroll view should try and scroll to.
- [ScrollTargetBehavior](https://developer.apple.com/documentation/swiftui/scrolltargetbehavior) — A type that defines the scroll behavior of a scrollable view.
- [ScrollTargetBehaviorContext](https://developer.apple.com/documentation/swiftui/scrolltargetbehaviorcontext) — The context in which a scroll target behavior updates its scroll target.
- [PagingScrollTargetBehavior](https://developer.apple.com/documentation/swiftui/pagingscrolltargetbehavior) — The scroll behavior that aligns scroll targets to container-based geometry.
- [ViewAlignedScrollTargetBehavior](https://developer.apple.com/documentation/swiftui/viewalignedscrolltargetbehavior) — The scroll behavior that aligns scroll targets to view-based geometry.
- [AnyScrollTargetBehavior](https://developer.apple.com/documentation/swiftui/anyscrolltargetbehavior) — A type-erased scroll target behavior.
- [ScrollTargetBehaviorProperties](https://developer.apple.com/documentation/swiftui/scrolltargetbehaviorproperties) — Properties influencing the scroll view a scroll target behavior applies to.
- [ScrollTargetBehaviorPropertiesContext](https://developer.apple.com/documentation/swiftui/scrolltargetbehaviorpropertiescontext) — The context in which a scroll target behavior can decide its properties.

## Animating scroll transitions {#Animating-scroll-transitions}

- [scrollTransition(_:axis:transition:)](https://developer.apple.com/documentation/swiftui/view/scrolltransition(_:axis:transition:)) — Applies the given transition, animating between the phases of the transition as this view appears and disappears within the visible region of the containing scroll view.
- [scrollTransition(topLeading:bottomTrailing:axis:transition:)](https://developer.apple.com/documentation/swiftui/view/scrolltransition(topleading:bottomtrailing:axis:transition:)) — Applies the given transition, animating between the phases of the transition as this view appears and disappears within the visible region of the containing scroll view.
- [ScrollTransitionPhase](https://developer.apple.com/documentation/swiftui/scrolltransitionphase) — The phases that a view transitions between when it scrolls among other views.
- [ScrollTransitionConfiguration](https://developer.apple.com/documentation/swiftui/scrolltransitionconfiguration) — The configuration of a scroll transition that controls how a transition is applied as a view is scrolled through the visible region of a containing scroll view or other container.

## Responding to scroll view changes {#Responding-to-scroll-view-changes}

- [onScrollGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/onscrollgeometrychange(for:of:action:)) — Adds an action to be performed when a value, created from a scroll geometry, changes.
- [onScrollTargetVisibilityChange(idType:threshold:_:)](https://developer.apple.com/documentation/swiftui/view/onscrolltargetvisibilitychange(idtype:threshold:_:)) — Adds an action to be called with information about what views would be considered visible.
- [onScrollVisibilityChange(threshold:_:)](https://developer.apple.com/documentation/swiftui/view/onscrollvisibilitychange(threshold:_:)) — Adds an action to be called when the view crosses the threshold to be considered on/off screen.
- [onScrollPhaseChange(_:)](https://developer.apple.com/documentation/swiftui/view/onscrollphasechange(_:)) — Adds an action to perform when the scroll phase of the first scroll view in the hierarchy changes.
- [ScrollGeometry](https://developer.apple.com/documentation/swiftui/scrollgeometry) — A type that defines the geometry of a scroll view.
- [ScrollPhase](https://developer.apple.com/documentation/swiftui/scrollphase) — A type that describes the state of a scroll gesture of a scrollable view like a scroll view.
- [ScrollPhaseChangeContext](https://developer.apple.com/documentation/swiftui/scrollphasechangecontext) — A type that provides you with more content when the phase of a scroll view changes.

## Showing scroll indicators {#Showing-scroll-indicators}

- [scrollIndicatorsFlash(onAppear:)](https://developer.apple.com/documentation/swiftui/view/scrollindicatorsflash(onappear:)) — Flashes the scroll indicators of a scrollable view when it appears.
- [scrollIndicatorsFlash(trigger:)](https://developer.apple.com/documentation/swiftui/view/scrollindicatorsflash(trigger:)) — Flashes the scroll indicators of scrollable views when a value changes.
- [scrollIndicators(_:axes:)](https://developer.apple.com/documentation/swiftui/view/scrollindicators(_:axes:)) — Sets the visibility of scroll indicators within this view.
- [horizontalScrollIndicatorVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/horizontalscrollindicatorvisibility) — The visibility to apply to scroll indicators of any horizontally scrollable content.
- [verticalScrollIndicatorVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/verticalscrollindicatorvisibility) — The visiblity to apply to scroll indicators of any vertically scrollable content.
- [ScrollIndicatorVisibility](https://developer.apple.com/documentation/swiftui/scrollindicatorvisibility) — The visibility of scroll indicators of a UI element.

## Managing content visibility {#Managing-content-visibility}

- [scrollContentBackground(_:)](https://developer.apple.com/documentation/swiftui/view/scrollcontentbackground(_:)) — Specifies the visibility of the background for scrollable views within this view.
- [scrollClipDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/scrollclipdisabled(_:)) — Sets whether a scroll view clips its content to its bounds.
- [ScrollContentOffsetAdjustmentBehavior](https://developer.apple.com/documentation/swiftui/scrollcontentoffsetadjustmentbehavior) — A type that defines the different kinds of content offset adjusting behaviors a scroll view can have.

## Disabling scrolling {#Disabling-scrolling}

- [scrollDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldisabled(_:)) — Disables or enables scrolling in scrollable views.
- [isScrollEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/isscrollenabled) — A Boolean value that indicates whether any scroll views associated with this environment allow scrolling to occur.

## Configuring scroll bounce behavior {#Configuring-scroll-bounce-behavior}

- [scrollBounceBehavior(_:axes:)](https://developer.apple.com/documentation/swiftui/view/scrollbouncebehavior(_:axes:)) — Configures the bounce behavior of scrollable views along the specified axis.
- [horizontalScrollBounceBehavior](https://developer.apple.com/documentation/swiftui/environmentvalues/horizontalscrollbouncebehavior) — The scroll bounce mode for the horizontal axis of scrollable views.
- [verticalScrollBounceBehavior](https://developer.apple.com/documentation/swiftui/environmentvalues/verticalscrollbouncebehavior) — The scroll bounce mode for the vertical axis of scrollable views.
- [ScrollBounceBehavior](https://developer.apple.com/documentation/swiftui/scrollbouncebehavior) — The ways that a scrollable view can bounce when it reaches the end of its content.

## Configuring scroll edge effects {#Configuring-scroll-edge-effects}

- [scrollEdgeEffectStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffectstyle(_:for:)) — Configures the scroll edge effect style for scroll views within this hierarchy.
- [scrollEdgeEffectHidden(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffecthidden(_:for:)) — Hides any scroll edge effects for scroll views within this hierarchy.
- [ScrollEdgeEffectStyle](https://developer.apple.com/documentation/swiftui/scrolledgeeffectstyle) — A structure that specifies blur transitions between scrolling content and an area with controls, such as toolbars.
- [safeAreaBar(edge:alignment:spacing:content:)](https://developer.apple.com/documentation/swiftui/view/safeareabar(edge:alignment:spacing:content:)) — Shows the specified content as a custom bar beside the modified view.

## Interacting with a software keyboard {#Interacting-with-a-software-keyboard}

- [scrollDismissesKeyboard(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldismisseskeyboard(_:)) — Configures the behavior in which scrollable content interacts with the software keyboard.
- [scrollDismissesKeyboardMode](https://developer.apple.com/documentation/swiftui/environmentvalues/scrolldismisseskeyboardmode) — The way that scrollable content interacts with the software keyboard.
- [ScrollDismissesKeyboardMode](https://developer.apple.com/documentation/swiftui/scrolldismisseskeyboardmode) — The ways that scrollable content can interact with the software keyboard.

## Managing scrolling for different inputs {#Managing-scrolling-for-different-inputs}

- [scrollInputBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrollinputbehavior(_:for:)) — Enables or disables scrolling in scrollable views when using particular inputs.
- [ScrollInputKind](https://developer.apple.com/documentation/swiftui/scrollinputkind) — Inputs used to scroll views.
- [ScrollInputBehavior](https://developer.apple.com/documentation/swiftui/scrollinputbehavior) — A type that defines whether input should scroll a view.
