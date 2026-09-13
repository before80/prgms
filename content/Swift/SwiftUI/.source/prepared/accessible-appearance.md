# Accessible appearance

Enhance the legibility of content in your app’s interface.

## Overview {#Overview}

Make content easier for people to see by making it larger, giving it greater contrast, or reducing the amount of distracting motion.

![](./images/accessible-appearance-hero@2x.png)

For design guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) in the Accessibility section of the Human Interface Guidelines.

## Managing color {#Managing-color}

- [accessibilityIgnoresInvertColors(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityignoresinvertcolors(_:)) — Sets whether this view should ignore the system Smart Invert setting.
- [accessibilityInvertColors](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityinvertcolors) — Whether the system preference for Invert Colors is enabled.
- [accessibilityDifferentiateWithoutColor](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilitydifferentiatewithoutcolor) — Whether the system preference for Differentiate without Color is enabled.

## Enlarging content {#Enlarging-content}

- [accessibilityShowsLargeContentViewer()](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer()) — Adds a default large content view to be shown by the large content viewer.
- [accessibilityShowsLargeContentViewer(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer(_:)) — Adds a custom large content view to be shown by the large content viewer.
- [accessibilityLargeContentViewerEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilitylargecontentviewerenabled) — Whether the Large Content Viewer is enabled.

## Improving legibility {#Improving-legibility}

- [accessibilityShowButtonShapes](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityshowbuttonshapes) — Whether the system preference for Show Button Shapes is enabled.
- [accessibilityReduceTransparency](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency) — Whether the system preference for Reduce Transparency is enabled.
- [legibilityWeight](https://developer.apple.com/documentation/swiftui/environmentvalues/legibilityweight) — The font weight to apply to text.
- [LegibilityWeight](https://developer.apple.com/documentation/swiftui/legibilityweight) — The Accessibility Bold Text user setting options.

## Minimizing motion {#Minimizing-motion}

- [accessibilityDimFlashingLights](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilitydimflashinglights) — Whether the setting to reduce flashing or strobing lights in video content is on. This setting can also be used to determine if UI in playback controls should be shown to indicate upcoming content that includes flashing or strobing lights.
- [accessibilityPlayAnimatedImages](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityplayanimatedimages) — Whether the setting for playing animations in an animated image is on. When this value is false, any presented image that contains animation should not play automatically.
- [accessibilityReduceMotion](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion) — Whether the system preference for Reduce Motion is enabled.

## Using assistive access {#Using-assistive-access}

- [accessibilityAssistiveAccessEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityassistiveaccessenabled) — A Boolean value that indicates whether Assistive Access is in use.
- [AssistiveAccess](https://developer.apple.com/documentation/swiftui/assistiveaccess) — A scene that presents an interface appropriate for Assistive Access on iOS and iPadOS. On other platforms, this scene is unused.
- [assistiveAccessNavigationIcon(_:)](https://developer.apple.com/documentation/swiftui/view/assistiveaccessnavigationicon(_:)) — Configures the view’s icon for purposes of navigation.
- [assistiveAccessNavigationIcon(systemImage:)](https://developer.apple.com/documentation/swiftui/view/assistiveaccessnavigationicon(systemimage:)) — Configures the view’s icon for purposes of navigation.
