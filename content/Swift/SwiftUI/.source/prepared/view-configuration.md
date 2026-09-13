# View configuration

Adjust the characteristics of views in a hierarchy.

## Overview {#Overview}

SwiftUI enables you to tune the appearance and behavior of views using view modifiers.

![](./images/view-configuration-hero@2x.png)

Many modifiers apply to specific kinds of views or behaviors, but some apply more generally. For example, you can conditionally hide any view by dynamically setting its opacity, display contextual help when people hover over a view, or request the light or dark appearance for a view.

## Hiding views {#Hiding-views}

- [opacity(_:)](https://developer.apple.com/documentation/swiftui/view/opacity(_:)) — Sets the transparency of this view.
- [hidden()](https://developer.apple.com/documentation/swiftui/view/hidden()) — Hides this view unconditionally.

## Hiding system elements {#Hiding-system-elements}

- [labelsHidden()](https://developer.apple.com/documentation/swiftui/view/labelshidden()) — Hides the labels of any controls contained within this view.
- [labelsVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/labelsvisibility(_:)) — Controls the visibility of labels of any controls contained within this view.
- [labelsVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/labelsvisibility) — The labels visibility set by [labelsVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/labelsvisibility(_:)).
- [menuIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/menuindicator(_:)) — Sets the menu indicator visibility for controls within this view.
- [statusBarHidden(_:)](https://developer.apple.com/documentation/swiftui/view/statusbarhidden(_:)) — Sets the visibility of the status bar.
- [persistentSystemOverlays(_:)](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:)) — Sets the preferred visibility of the non-transient system views overlaying the app.
- [Visibility](https://developer.apple.com/documentation/swiftui/visibility) — The visibility of a UI element, chosen automatically based on the platform, current context, and other factors.

## Managing view interaction {#Managing-view-interaction}

- [disabled(_:)](https://developer.apple.com/documentation/swiftui/view/disabled(_:)) — Adds a condition that controls whether users can interact with this view.
- [isEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/isenabled) — A Boolean value that indicates whether the view associated with this environment allows user interaction.
- [interactionActivityTrackingTag(_:)](https://developer.apple.com/documentation/swiftui/view/interactionactivitytrackingtag(_:)) — Sets a tag that you use for tracking interactivity.
- [invalidatableContent(_:)](https://developer.apple.com/documentation/swiftui/view/invalidatablecontent(_:)) — Mark the receiver as their content might be invalidated.

## Providing contextual help {#Providing-contextual-help}

- [help(_:)](https://developer.apple.com/documentation/swiftui/view/help(_:)) — Adds help text to a view using a localized string resource that you provide.

## Detecting and requesting the light or dark appearance {#Detecting-and-requesting-the-light-or-dark-appearance}

- [preferredColorScheme(_:)](https://developer.apple.com/documentation/swiftui/view/preferredcolorscheme(_:)) — Sets the preferred color scheme for this presentation.
- [colorScheme](https://developer.apple.com/documentation/swiftui/environmentvalues/colorscheme) — The color scheme of this environment.
- [ColorScheme](https://developer.apple.com/documentation/swiftui/colorscheme) — The possible color schemes, corresponding to the light and dark appearances.

## Getting the color scheme contrast {#Getting-the-color-scheme-contrast}

- [colorSchemeContrast](https://developer.apple.com/documentation/swiftui/environmentvalues/colorschemecontrast) — The contrast associated with the color scheme of this environment.
- [ColorSchemeContrast](https://developer.apple.com/documentation/swiftui/colorschemecontrast) — The contrast between the app’s foreground and background colors.

## Configuring passthrough {#Configuring-passthrough}

- [preferredSurroundingsEffect(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsurroundingseffect(_:)) — Applies an effect to passthrough video.
- [SurroundingsEffect](https://developer.apple.com/documentation/swiftui/surroundingseffect) — Effects that the system can apply to passthrough video.
- [breakthroughEffect(_:)](https://developer.apple.com/documentation/swiftui/view/breakthrougheffect(_:)) — Ensures that the view is always visible to the user, even when other content is occluding it, like 3D models.
- [BreakthroughEffect](https://developer.apple.com/documentation/swiftui/breakthrougheffect)

## Redacting private content {#Redacting-private-content}

- [Designing your app for the Always On state](https://developer.apple.com/documentation/watchos-apps/designing-your-app-for-the-always-on-state) — Customize your watchOS app’s user interface for continuous display.
- [Protecting sensitive content when screen sharing and remote control are active](2.1-ProtectingSensitiveContentWhenScreenSharing/) — Detect active screen capture sessions and respond appropriately to protect sensitive content in your app.
- [privacySensitive(_:)](https://developer.apple.com/documentation/swiftui/view/privacysensitive(_:)) — Marks the view as containing sensitive, private user data.
- [redacted(reason:)](https://developer.apple.com/documentation/swiftui/view/redacted(reason:)) — Adds a reason to apply a redaction to this view hierarchy.
- [unredacted()](https://developer.apple.com/documentation/swiftui/view/unredacted()) — Removes any reason to apply a redaction to this view hierarchy.
- [redactionReasons](https://developer.apple.com/documentation/swiftui/environmentvalues/redactionreasons) — The current redaction reasons applied to the view hierarchy.
- [isSceneCaptured](https://developer.apple.com/documentation/swiftui/environmentvalues/isscenecaptured) — The current capture state.
- [RedactionReasons](https://developer.apple.com/documentation/swiftui/redactionreasons) — The reasons to apply a redaction to data displayed on screen.
