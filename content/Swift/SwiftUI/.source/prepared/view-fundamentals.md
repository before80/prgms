# View fundamentals

Define the visual elements of your app using a hierarchy of views.

## Overview {#Overview}

Views are the building blocks that you use to declare your app’s user interface. Each view contains a description of what to display for a given state. Every bit of your app that’s visible to the user derives from the description in a view, and any type that conforms to the [View](https://developer.apple.com/documentation/swiftui/view) protocol can act as a view in your app.

![](./images/view-fundamentals-hero@2x.png)

Compose a custom view by combining built-in views that SwiftUI provides with other custom views that you create in your view’s [body](https://developer.apple.com/documentation/swiftui/view/body-8kl5o) computed property. Configure views using the view modifiers that SwiftUI provides, or by defining your own view modifiers using the [ViewModifier](https://developer.apple.com/documentation/swiftui/viewmodifier) protocol and the [modifier(_:)](https://developer.apple.com/documentation/swiftui/view/modifier(_:)) method.

## Creating a view {#Creating-a-view}

- [Declaring a custom view](1.1-DeclaringACustomView/) — Define views and assemble them into a view hierarchy.
- [Wishlist: Planning travel in a SwiftUI app](1.2-WishlistPlanningTravelInASwiftuiApp/) — Build a travel planning app that organizes trips into collections and tracks activity completion.
- [View](https://developer.apple.com/documentation/swiftui/view) — A type that represents part of your app’s user interface and provides modifiers that you use to configure views.
- [ContentBuilder](https://developer.apple.com/documentation/swiftui/contentbuilder) — A custom parameter attribute that constructs views and other content types from closures.
- [ViewBuilder](https://developer.apple.com/documentation/swiftui/viewbuilder) — A custom parameter attribute that constructs views from closures.

## Modifying a view {#Modifying-a-view}

- [Configuring views](1.18-ConfiguringViews/) — Adjust the characteristics of a view by applying view modifiers.
- [Reducing view modifier maintenance](1.19-ReducingViewModifierMaintenance/) — Bundle view modifiers that you regularly reuse into a custom view modifier.
- [modifier(_:)](https://developer.apple.com/documentation/swiftui/view/modifier(_:)) — Applies a modifier to a view and returns a new view.
- [ViewModifier](https://developer.apple.com/documentation/swiftui/viewmodifier) — A modifier that you apply to a view or another view modifier, producing a different version of the original value.
- [EmptyModifier](https://developer.apple.com/documentation/swiftui/emptymodifier) — An empty, or identity, modifier, used during development to switch modifiers at compile time.
- [ModifiedContent](https://developer.apple.com/documentation/swiftui/modifiedcontent) — A value with a modifier applied to it.
- [EnvironmentalModifier](https://developer.apple.com/documentation/swiftui/environmentalmodifier) — A modifier that must resolve to a concrete modifier in an environment before use.
- [ManipulableModifier](https://developer.apple.com/documentation/swiftui/manipulablemodifier)
- [ManipulableResponderModifier](https://developer.apple.com/documentation/swiftui/manipulablerespondermodifier)
- [ManipulableTransformBindingModifier](https://developer.apple.com/documentation/swiftui/manipulabletransformbindingmodifier)
- [ManipulationGeometryModifier](https://developer.apple.com/documentation/swiftui/manipulationgeometrymodifier)
- [ManipulationGestureModifier](https://developer.apple.com/documentation/swiftui/manipulationgesturemodifier)
- [ManipulationUsingGestureStateModifier](https://developer.apple.com/documentation/swiftui/manipulationusinggesturestatemodifier)
- [Manipulable](https://developer.apple.com/documentation/swiftui/manipulable) — A namespace for various manipulable related types.

## Responding to view life cycle updates {#Responding-to-view-life-cycle-updates}

- [onAppear(perform:)](https://developer.apple.com/documentation/swiftui/view/onappear(perform:)) — Adds an action to perform before this view appears.
- [onDisappear(perform:)](https://developer.apple.com/documentation/swiftui/view/ondisappear(perform:)) — Adds an action to perform after this view disappears.

## Assigning tasks {#Assigning-tasks}

- [task(id:name:executorPreference:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(id:name:executorpreference:priority:file:line:_:)) — Adds a task to perform before this view appears or when a specified value changes.
- [task(id:name:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(id:name:priority:file:line:_:)) — Adds a task to perform before this view appears or when a specified value changes.
- [task(name:executorPreference:priority:file:line:action:)](https://developer.apple.com/documentation/swiftui/view/task(name:executorpreference:priority:file:line:action:)) — Adds an asynchronous task to perform before this view appears.
- [task(name:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(name:priority:file:line:_:)) — Adds an asynchronous task to perform before this view appears.

## Managing the view hierarchy {#Managing-the-view-hierarchy}

- [id(_:)](https://developer.apple.com/documentation/swiftui/view/id(_:)) — Binds a view’s identity to the given proxy value.
- [tag(_:includeOptional:)](https://developer.apple.com/documentation/swiftui/view/tag(_:includeoptional:)) — Sets the unique tag value of this view.
- [equatable()](https://developer.apple.com/documentation/swiftui/view/equatable()) — Prevents the view from updating its child view when its new value is the same as its old value.

## Supporting content types {#Supporting-content-types}

- [EmptyContent](https://developer.apple.com/documentation/swiftui/emptycontent) — Content which contains nothing.
- [TupleContent](https://developer.apple.com/documentation/swiftui/tuplecontent) — Content created from a tuple of content to be treated as siblings.

## Supporting view types {#Supporting-view-types}

- [AnyView](https://developer.apple.com/documentation/swiftui/anyview) — A type-erased view.
- [EmptyView](https://developer.apple.com/documentation/swiftui/emptyview) — A view that doesn’t contain any content.
- [EquatableView](https://developer.apple.com/documentation/swiftui/equatableview) — A view type that compares itself against its previous value and prevents its child updating if its new value is the same as its old value.
- [SubscriptionView](https://developer.apple.com/documentation/swiftui/subscriptionview) — A view that subscribes to a publisher with an action.
- [TupleView](https://developer.apple.com/documentation/swiftui/tupleview) — A View created from a swift tuple of View values.
