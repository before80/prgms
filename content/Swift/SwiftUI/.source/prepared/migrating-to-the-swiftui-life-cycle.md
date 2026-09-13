# Migrating to the SwiftUI life cycle

Use a scene-based life cycle in SwiftUI while keeping your existing codebase.

## Overview {#Overview}

Take advantage of the declarative syntax in SwiftUI and its compatibility with spatial frameworks by moving your app to the SwiftUI life cycle.

Moving to the SwiftUI life cycle requires several steps, including changing your app’s entry point, configuring the launch of your app, and monitoring life-cycle changes with the methods that SwiftUI provides.

### Change your app’s entry point {#Change-your-apps-entry-point}

The [UIKit](https://developer.apple.com/documentation/uikit) framework defines the `AppDelegate` file as the entry point of your app with the annotation `@main`. For more information on `@main`, see the [Attributes](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/attributes/#main) section in The Swift Programming Language. To indicate the entry of a SwiftUI app, you’ll need to create a new file that defines your app’s structure.

1. Open your project in Xcode.
1. Choose File > New > File > Swift file.
1. Name the file `<YourAppName>App.swift`.
1. Add `import SwiftUI` at the top of the file.
1. Annotate the app structure with the `@main` attribute to indicate the entry point of the SwiftUI app, as shown in the code snippet below.

> Important: Remove the `@main` or `@UIApplicationMain` attribute in your app delegate.

Use following code to create the SwiftUI app structure. To learn more about this structure, see [App](https://developer.apple.com/documentation/swiftui/app).

```swift
import SwiftUI

@main
struct MyExampleApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Support app delegate methods {#Support-app-delegate-methods}

To continue using methods in your app delegate, use the [UIApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor) property wrapper. To tell SwiftUI about a delegate that conforms to the [UIApplicationDelegate](https://developer.apple.com/documentation/uikit/uiapplicationdelegate) protocol, place this property wrapper inside your [App](https://developer.apple.com/documentation/swiftui/app) declaration:

```swift
@main
struct MyExampleApp: App {
    @UIApplicationDelegateAdaptor private var appDelegate: MyAppDelegate
    var body: some Scene { ... }
}
```

This example marks a custom app delegate named `MyAppDelegate` as the delegate adaptor. Be sure to implement any necessary delegate methods in that type.

> Note: For AppKit support, use [NSApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/nsapplicationdelegateadaptor). For WatchKit support, use [WKApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/wkapplicationdelegateadaptor).

### Configure the launch of your app {#Configure-the-launch-of-your-app}

If you’re migrating an app that contains storyboards to SwiftUI, make sure to remove them when they’re no longer needed.

1. Open your project in Xcode.
1. Remove `Main.storyboard` from the project navigator.
1. Choose your app’s target.
1. Open the `Info.plist` file.
1. Remove the [UIMainStoryboardFile](https://developer.apple.com/documentation/bundleresources/information-property-list/uimainstoryboardfile) key.
1. Remove the [UISceneStoryboardFile](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest/uisceneconfigurations/uiwindowscenesessionroleapplication/uiscenestoryboardfile) key in the [UIApplicationSceneManifest](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest) > [UISceneConfigurations](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest/uisceneconfigurations) > [UIWindowSceneSessionRoleApplication](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest/uisceneconfigurations/uiwindowscenesessionroleapplication) > `Item 0 (Default Configuration)` dictionary.

This figure shows the structure of the `Info.plist` file before removing these keys.

![A screenshot of the Info.plist file in Xcode, with all of the keys expanded.](./images/Migrating-to-the-SwiftUI-life-cycle-info_plist@2x.png)

The scene delegate continues to be called after removing the keys from the `Info.plist` file, so you can still handle other scene-based life cycle changes in this file. If you were previously launching your app in your scene delegate, remove the [scene(_:willConnectTo:options:)](https://developer.apple.com/documentation/uikit/uiscenedelegate/scene(_:willconnectto:options:)) method from your scene delegate.

If you didn’t previously support scenes in your app and rely on your app delegate to respond to the launch of your app, ensure you’re no longer setting a root view controller in [application(_:didFinishLaunchingWithOptions:)](https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:didfinishlaunchingwithoptions:)). Instead, return `true`.

### Monitor life cycle changes {#Monitor-life-cycle-changes}

You will no longer be able to monitor life-cycle changes in your app delegate due to the scene-based nature of SwiftUI (see [Scene](https://developer.apple.com/documentation/swiftui/scene)). Prefer to handle these changes in [ScenePhase](https://developer.apple.com/documentation/swiftui/scenephase), the life cycle enumeration that SwiftUI provides to monitor the phases of a scene. Observe the [Environment](https://developer.apple.com/documentation/swiftui/environment) value to initiate actions when the phase changes.

```swift
@Environment(\.scenePhase) private var scenePhase
```

Interpret the value differently based on where you read it from. If you read the phase from inside a [View](https://developer.apple.com/documentation/swiftui/view) instance, the value reflects the phase of the scene that contains the view. If you read the phase from within an `App` instance, the value reflects an aggregation of the phases of all of the scenes in your app.

To handle scene-based events with a scene delegate, provide your scene delegate to your SwiftUI app inside your app delegate. For more information, see the “Scene delegates” section of [UIApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor).

For more information on handling scene-based life cycle events, see [Managing your app’s life cycle](https://developer.apple.com/documentation/uikit/managing-your-app-s-life-cycle).
