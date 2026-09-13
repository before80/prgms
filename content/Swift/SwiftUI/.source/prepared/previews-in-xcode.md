# Previews in Xcode

Generate dynamic, interactive previews of your custom views.

## Overview {#Overview}

When you create a custom [View](https://developer.apple.com/documentation/swiftui/view) with SwiftUI, Xcode can display a preview of the view’s content that stays up-to-date as you make changes to the view’s code. You use one of the preview macros — like [Preview(_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:body:)) — to tell Xcode what to display. Xcode shows the preview in a canvas beside your code.

![](./images/previews-in-xcode-hero@2x.png)

Different preview macros enable different kinds of configuration. For example, you can add traits that affect the preview’s appearance using the [Preview(_:traits:_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:_:body:)) macro or add custom viewpoints for the preview using the [Preview(_:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:body:cameras:)) macro. You can also check how your view behaves inside a specific scene type. For example, in visionOS you can use the [Preview(_:immersionStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:)) macro to preview your view inside an [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace).

## Essentials {#Essentials}

- [Adding previews to your interface files](https://developer.apple.com/documentation/xcode/adding-previews-to-your-interface-files) — Write code to test your views on different devices and configurations without needing to run your app.

## Creating a preview {#Creating-a-preview}

- [Preview(_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:body:)) — Creates a preview of a SwiftUI view.
- [Preview(_:traits:_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:_:body:)) — Creates a preview of a SwiftUI view using the specified traits.
- [Preview(_:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:body:cameras:)) — Creates a preview of a SwiftUI view using the specified traits and custom viewpoints.
- [Preview(_:traits:arguments:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:arguments:body:)) — Creates a group of previews of a parameterized SwiftUI view, varying its inputs over the provided arguments.

## Customizing a preview {#Customizing-a-preview}

- [Previewable()](https://developer.apple.com/documentation/swiftui/previewable()) — Tag allowing a dynamic property to appear inline in a preview.
- [PreviewModifier](https://developer.apple.com/documentation/swiftui/previewmodifier) — A type that defines an environment in which previews can appear.
- [PreviewModifierContent](https://developer.apple.com/documentation/swiftui/previewmodifiercontent) — The type-erased content of a preview.

## Creating a preview in the context of a scene {#Creating-a-preview-in-the-context-of-a-scene}

- [Preview(_:immersionStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:)) — Creates a preview of a SwiftUI view in an immersive space.
- [Preview(_:immersionStyle:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:cameras:)) — Creates a preview of a SwiftUI view in an immersive space with custom viewpoints.
- [Preview(_:windowStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:windowstyle:traits:body:)) — Creates a preview of a SwiftUI view in a window.
- [Preview(_:windowStyle:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:windowstyle:traits:body:cameras:)) — Creates a preview of a SwiftUI view in a window with custom viewpoints.

## Building in debug mode {#Building-in-debug-mode}

- [DebugReplaceableView](https://developer.apple.com/documentation/swiftui/debugreplaceableview) — Erases view opaque result types in debug builds.

## Deprecated {#Deprecated}

- [Deprecated](1.3.1-PreviewsDeprecated/) — Review deprecated preview symbols and their replacements.
