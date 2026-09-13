# Scenes

Declare the user interface groupings that make up the parts of your app.

## Overview {#Overview}

A scene represents a part of your app’s user interface that has a life cycle that the system manages. An [App](https://developer.apple.com/documentation/swiftui/app) instance presents the scenes it contains, while each [Scene](https://developer.apple.com/documentation/swiftui/scene) acts as the root element of a [View](https://developer.apple.com/documentation/swiftui/view) hierarchy.

![](./images/scenes-hero@2x.png)

The system presents scenes in different ways depending on the type of scene, the platform, and the context. A scene might fill the entire display, part of the display, a window, a tab in a window, or something else. In some cases, your app might also be able to display more than one instance of the scene at a time, like when a user simultaneously opens multiple windows based on a single [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup) declaration in your app. For more information about the primary built-in scene types, see [Windows](../3-Windows/) and [Documents](../5-Documents/).

You configure scenes using modifiers, similar to how you configure views. For example, you can adjust the appearance of the window that contains a scene — if the scene happens to appear in a window — using the [windowStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowstyle(_:)) modifier. Similarly, you can add menu commands that become available when the scene is in the foreground on certain platforms using the [commands(content:)](https://developer.apple.com/documentation/swiftui/scene/commands(content:)) modifier.

## Creating scenes {#Creating-scenes}

- [Scene](https://developer.apple.com/documentation/swiftui/scene) — A part of an app’s user interface with a life cycle managed by the system.
- [SceneBuilder](https://developer.apple.com/documentation/swiftui/scenebuilder) — A result builder for composing a collection of scenes into a single composite scene.

## Monitoring scene life cycle {#Monitoring-scene-life-cycle}

- [scenePhase](https://developer.apple.com/documentation/swiftui/environmentvalues/scenephase) — The current phase of the scene.
- [ScenePhase](https://developer.apple.com/documentation/swiftui/scenephase) — An indication of a scene’s operational state.

## Managing a settings window {#Managing-a-settings-window}

- [Settings](https://developer.apple.com/documentation/swiftui/settings) — A scene that presents an interface for viewing and modifying an app’s settings.
- [SettingsLink](https://developer.apple.com/documentation/swiftui/settingslink) — A view that opens the Settings scene defined by an app.
- [OpenSettingsAction](https://developer.apple.com/documentation/swiftui/opensettingsaction) — An action that presents the settings scene for an app.
- [openSettings](https://developer.apple.com/documentation/swiftui/environmentvalues/opensettings) — A Settings presentation action stored in a view’s environment.

## Building a menu bar {#Building-a-menu-bar}

- [Building and customizing the menu bar with SwiftUI](2.1-BuildingAndCustomizingTheMenuBarWithSwiftui/) — Provide a seamless, cross-platform user experience by building a native menu bar for iPadOS and macOS.

## Creating a menu bar extra {#Creating-a-menu-bar-extra}

- [MenuBarExtra](https://developer.apple.com/documentation/swiftui/menubarextra) — A scene that renders itself as a persistent control in the system menu bar.
- [menuBarExtraStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/menubarextrastyle(_:)) — Sets the style for menu bar extra created by this scene.
- [MenuBarExtraStyle](https://developer.apple.com/documentation/swiftui/menubarextrastyle) — A specification for the appearance and behavior of a menu bar extra scene.

## Creating watch notifications {#Creating-watch-notifications}

- [WKNotificationScene](https://developer.apple.com/documentation/swiftui/wknotificationscene) — A scene which appears in response to receiving the specified category of remote or local notifications.

## Presenting content on an external display {#Presenting-content-on-an-external-display}

- [sceneAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/sceneaccessory(content:)) — Defines any scene accessories associated with `self`.
- [SceneAccessoryContent](https://developer.apple.com/documentation/swiftui/sceneaccessorycontent) — Conforming types represent items which define content for scene accessories.
- [ExternalNonInteractiveAccessory](https://developer.apple.com/documentation/swiftui/externalnoninteractiveaccessory) — A scene accessory that presents non-interactive content on an external display.
