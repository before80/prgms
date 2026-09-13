# Custom layout

Place views in custom arrangements and create animated transitions between layout types.

## Overview {#Overview}

You can create complex view layouts using the built-in layout containers and layout view modifiers that SwiftUI provides. However, if you need behavior that you can’t achieve with the built-in layout tools, create a custom layout container type using the [Layout](https://developer.apple.com/documentation/swiftui/layout) protocol. A container that you define asks for the sizes of all its subviews, and then indicates where to place the subviews within its own bounds.

![](./images/custom-layout-hero@2x.png)

You can also create animated transitions among layout types that conform to the [Layout](https://developer.apple.com/documentation/swiftui/layout) procotol, including both built-in and custom layouts.

For design guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) in the Human Interface Guidelines.

## Creating a custom layout container {#Creating-a-custom-layout-container}

- [Composing custom layouts with SwiftUI](3.1-ComposingCustomLayoutsWithSwiftui/) — Arrange views in your app’s interface using layout tools that SwiftUI provides.
- [Layout](https://developer.apple.com/documentation/swiftui/layout) — A type that defines the geometry of a collection of views.
- [LayoutSubview](https://developer.apple.com/documentation/swiftui/layoutsubview) — A proxy that represents one subview of a layout.
- [LayoutSubviews](https://developer.apple.com/documentation/swiftui/layoutsubviews) — A collection of proxy values that represent the subviews of a layout view.

## Configuring a custom layout {#Configuring-a-custom-layout}

- [LayoutProperties](https://developer.apple.com/documentation/swiftui/layoutproperties) — Layout-specific properties of a layout container.
- [ProposedViewSize](https://developer.apple.com/documentation/swiftui/proposedviewsize) — A proposal for the size of a view.
- [ViewSpacing](https://developer.apple.com/documentation/swiftui/viewspacing) — A collection of the geometric spacing preferences of a view.

## Associating values with views in a custom layout {#Associating-values-with-views-in-a-custom-layout}

- [layoutValue(key:value:)](https://developer.apple.com/documentation/swiftui/view/layoutvalue(key:value:)) — Associates a value with a custom layout property.
- [LayoutValueKey](https://developer.apple.com/documentation/swiftui/layoutvaluekey) — A key for accessing a layout value of a layout container’s subviews.

## Transitioning between layout types {#Transitioning-between-layout-types}

- [AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout) — A type-erased instance of the layout protocol.
- [HStackLayout](https://developer.apple.com/documentation/swiftui/hstacklayout) — A horizontal container that you can use in conditional layouts.
- [VStackLayout](https://developer.apple.com/documentation/swiftui/vstacklayout) — A vertical container that you can use in conditional layouts.
- [ZStackLayout](https://developer.apple.com/documentation/swiftui/zstacklayout) — An overlaying container that you can use in conditional layouts.
- [GridLayout](https://developer.apple.com/documentation/swiftui/gridlayout) — A grid that you can use in conditional layouts.
