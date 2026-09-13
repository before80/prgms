# App organization

Define the entry point and top-level structure of your app.

## Overview {#Overview}

Describe your app’s structure declaratively, much like you declare a view’s appearance. Create a type that conforms to the [App](https://developer.apple.com/documentation/swiftui/app) protocol and use it to enumerate the [Scenes](../2-Scenes/) that represent aspects of your app’s user interface.

![](./images/app-organization-hero@2x.png)

SwiftUI enables you to write code that works across all of Apple’s platforms. However, it also enables you to tailor your app to the specific capabilities of each platform. For example, if you need to respond to the callbacks that the system traditionally makes on a UIKit, AppKit, or WatchKit app’s delegate, define a delegate object and instantiate it in your app structure using an appropriate delegate adaptor property wrapper, like [UIApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor).

For platform-specific design guidance, see [Getting started](https://developer.apple.com/design/human-interface-guidelines/getting-started) in the Human Interface Guidelines.

## Creating an app {#Creating-an-app}

- [Destination Video](https://developer.apple.com/documentation/visionos/destination-video) — Leverage SwiftUI to build an immersive media experience in a multiplatform app.
- [Hello World](https://developer.apple.com/documentation/visionos/world) — Use windows, volumes, and immersive spaces to teach people about the Earth.
- [Backyard Birds: Building an app with SwiftData and widgets](1.1-BackyardBirdsSample/) — Create an app with persistent data, interactive widgets, and an all new in-app purchase experience.
- [Food Truck: Building a SwiftUI multiplatform app](1.2-FoodTruckBuildingASwiftuiMultiplatformApp/) — Create a single codebase and app target for Mac, iPad, and iPhone.
- [Fruta: Building a feature-rich app with SwiftUI](https://developer.apple.com/documentation/appclip/fruta-building-a-feature-rich-app-with-swiftui) — Create a shared codebase to build a multiplatform app that offers widgets and an App Clip.
- [Migrating to the SwiftUI life cycle](1.3-MigratingToTheSwiftuiLifeCycle/) — Use a scene-based life cycle in SwiftUI while keeping your existing codebase.
- [App](https://developer.apple.com/documentation/swiftui/app) — A type that represents the structure and behavior of an app.

## Targeting iOS and iPadOS {#Targeting-iOS-and-iPadOS}

- [UILaunchScreen](https://developer.apple.com/documentation/bundleresources/information-property-list/uilaunchscreen) — The user interface to show while an app launches.
- [UILaunchScreens](https://developer.apple.com/documentation/bundleresources/information-property-list/uilaunchscreens) — The user interfaces to show while an app launches in response to different URL schemes.
- [UIApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor) — A property wrapper type that you use to create a UIKit app delegate.

## Targeting macOS {#Targeting-macOS}

- [NSApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/nsapplicationdelegateadaptor) — A property wrapper type that you use to create an AppKit app delegate.

## Targeting watchOS {#Targeting-watchOS}

- [WKApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/wkapplicationdelegateadaptor) — A property wrapper that is used in `App` to provide a delegate from WatchKit.
- [WKExtensionDelegateAdaptor](https://developer.apple.com/documentation/swiftui/wkextensiondelegateadaptor) — A property wrapper type that you use to create a WatchKit extension delegate.

## Targeting tvOS {#Targeting-tvOS}

- [Creating a tvOS media catalog app in SwiftUI](1.4-CreatingATvosMediaCatalogAppInSwiftui/) — Build standard content lockups and rows of content shelves for your tvOS app.

## Handling system recenter events {#Handling-system-recenter-events}

- [WorldRecenterPhase](https://developer.apple.com/documentation/swiftui/worldrecenterphase) — A type that represents information associated with a phase of a system recenter event. Values of this type are passed to the closure specified in View.onWorldRecenter(action:).
