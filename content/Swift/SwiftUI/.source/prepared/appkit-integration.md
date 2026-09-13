# AppKit integration

Add AppKit views to your SwiftUI app, or use SwiftUI views in your AppKit app.

## Overview {#Overview}

Integrate SwiftUI with your app’s existing content using hosting controllers to add SwiftUI views into AppKit interfaces. A hosting controller wraps a set of SwiftUI views in a form that you can then add to your storyboard-based app.

![](./images/appkit-integration-hero@2x.png)

You can also add AppKit views and view controllers to your SwiftUI interfaces. A representable object wraps the designated view or view controller, and facilitates communication between the wrapped object and your SwiftUI views.

For design guidance, see [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos) in the Human Interface Guidelines.

## Displaying SwiftUI views in AppKit {#Displaying-SwiftUI-views-in-AppKit}

- [Unifying your app’s animations](1.1-UnifyingYourAppSAnimations/) — Create a consistent UI animation experience across SwiftUI, UIKit, and AppKit.
- [NSHostingController](https://developer.apple.com/documentation/swiftui/nshostingcontroller) — An AppKit view controller that hosts SwiftUI view hierarchy.
- [NSHostingView](https://developer.apple.com/documentation/swiftui/nshostingview) — An AppKit view that hosts a SwiftUI view hierarchy.
- [NSHostingMenu](https://developer.apple.com/documentation/swiftui/nshostingmenu) — An AppKit menu with menu items that are defined by a SwiftUI View.
- [NSHostingSizingOptions](https://developer.apple.com/documentation/swiftui/nshostingsizingoptions) — Options for how hosting views and controllers reflect their content’s size into Auto Layout constraints.
- [NSHostingSceneRepresentation](https://developer.apple.com/documentation/swiftui/nshostingscenerepresentation) — An AppKit type that hosts and can present SwiftUI scenes
- [NSHostingSceneBridgingOptions](https://developer.apple.com/documentation/swiftui/nshostingscenebridgingoptions) — Options for how hosting views and controllers manage aspects of the associated window.

## Adding AppKit views to SwiftUI view hierarchies {#Adding-AppKit-views-to-SwiftUI-view-hierarchies}

- [NSViewRepresentable](https://developer.apple.com/documentation/swiftui/nsviewrepresentable) — A wrapper that you use to integrate an AppKit view into your SwiftUI view hierarchy.
- [NSViewRepresentableContext](https://developer.apple.com/documentation/swiftui/nsviewrepresentablecontext) — Contextual information about the state of the system that you use to create and update your AppKit view.
- [NSViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/nsviewcontrollerrepresentable) — A wrapper that you use to integrate an AppKit view controller into your SwiftUI interface.
- [NSViewControllerRepresentableContext](https://developer.apple.com/documentation/swiftui/nsviewcontrollerrepresentablecontext) — Contextual information about the state of the system that you use to create and update your AppKit view controller.

## Adding AppKit gesture recognizers into SwiftUI view hierarchies {#Adding-AppKit-gesture-recognizers-into-SwiftUI-view-hierarchies}

- [NSGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentable) — A wrapper for an `NSGestureRecognizer` that you use to integrate that gesture recognizer into your SwiftUI hierarchy.
- [NSGestureRecognizerRepresentableContext](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentablecontext) — Contextual information about the state of the system that you use to create and update a represented gesture recognizer.
- [NSGestureRecognizerRepresentableCoordinateSpaceConverter](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentablecoordinatespaceconverter) — A structure used to convert locations to and from coordinate spaces in the hierarchy of the SwiftUI view associated with an [NSGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentable).
