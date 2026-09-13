# UIKit integration

Add UIKit views to your SwiftUI app, or use SwiftUI views in your UIKit app.

## Overview {#Overview}

Integrate SwiftUI with your app’s existing content using hosting controllers to add SwiftUI views into UIKit interfaces. A hosting controller wraps a set of SwiftUI views in a form that you can then add to your storyboard-based app.

![](./images/uikit-integration-hero@2x.png)

You can also add UIKit views and view controllers to your SwiftUI interfaces. A representable object wraps the designated view or view controller, and facilitates communication between the wrapped object and your SwiftUI views.

For design guidance, see the following sections in the Human Interface Guidelines:

- [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)
- [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)
- [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)

## Displaying SwiftUI views in UIKit {#Displaying-SwiftUI-views-in-UIKit}

- [Using SwiftUI with UIKit](https://developer.apple.com/documentation/uikit/using-swiftui-with-uikit) — Learn how to incorporate SwiftUI views into a UIKit app.
- [Unifying your app’s animations](../1-AppkitIntegration/1.1-UnifyingYourAppSAnimations/) — Create a consistent UI animation experience across SwiftUI, UIKit, and AppKit.
- [UIHostingController](https://developer.apple.com/documentation/swiftui/uihostingcontroller) — A UIKit view controller that manages a SwiftUI view hierarchy.
- [UIHostingControllerSizingOptions](https://developer.apple.com/documentation/swiftui/uihostingcontrollersizingoptions) — Options for how a hosting controller tracks its content’s size.
- [UIHostingConfiguration](https://developer.apple.com/documentation/swiftui/uihostingconfiguration) — A content configuration suitable for hosting a hierarchy of SwiftUI views.
- [UIHostingSceneDelegate](https://developer.apple.com/documentation/swiftui/uihostingscenedelegate) — Extends `UIKit/UISceneDelegate` to bridge SwiftUI scenes.

## Adding UIKit views to SwiftUI view hierarchies {#Adding-UIKit-views-to-SwiftUI-view-hierarchies}

- [UIViewRepresentable](https://developer.apple.com/documentation/swiftui/uiviewrepresentable) — A wrapper for a UIKit view that you use to integrate that view into your SwiftUI view hierarchy.
- [UIViewRepresentableContext](https://developer.apple.com/documentation/swiftui/uiviewrepresentablecontext) — Contextual information about the state of the system that you use to create and update your UIKit view.
- [UIViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentable) — A view that represents a UIKit view controller.
- [UIViewControllerRepresentableContext](https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentablecontext) — Contextual information about the state of the system that you use to create and update your UIKit view controller.

## Adding UIKit gesture recognizers into SwiftUI view hierarchies {#Adding-UIKit-gesture-recognizers-into-SwiftUI-view-hierarchies}

- [UIGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/uigesturerecognizerrepresentable) — A wrapper for a `UIGestureRecognizer` that you use to integrate that gesture recognizer into your SwiftUI hierarchy.
- [UIGestureRecognizerRepresentableContext](https://developer.apple.com/documentation/swiftui/uigesturerecognizerrepresentablecontext) — Contextual information about the state of the system that you use to create and update a represented gesture recognizer.
- [UIGestureRecognizerRepresentableCoordinateSpaceConverter](https://developer.apple.com/documentation/swiftui/uigesturerecognizerrepresentablecoordinatespaceconverter) — A proxy structure used to convert locations to/from coordinate spaces in the hierarchy of the SwiftUI view associated with a [UIGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/uigesturerecognizerrepresentable).

## Sharing configuration information {#Sharing-configuration-information}

- [UITraitBridgedEnvironmentKey](https://developer.apple.com/documentation/swiftui/uitraitbridgedenvironmentkey)

## Hosting an ornament in UIKit {#Hosting-an-ornament-in-UIKit}

- [UIHostingOrnament](https://developer.apple.com/documentation/swiftui/uihostingornament) — A model that represents an ornament suitable for being hosted in UIKit.
- [UIOrnament](https://developer.apple.com/documentation/swiftui/uiornament) — The abstract base class that represents an ornament.
