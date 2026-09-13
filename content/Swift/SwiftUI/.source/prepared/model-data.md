# Model data

Manage the data that your app uses to drive its interface.

## Overview {#Overview}

SwiftUI offers a declarative approach to user interface design. As you compose a hierarchy of views, you also indicate data dependencies for the views. When the data changes, either due to an external event or because of an action that the user performs, SwiftUI automatically updates the affected parts of the interface. As a result, the framework automatically performs most of the work that view controllers traditionally do.

![](./images/model-data-hero@2x.png)

The framework provides tools, like state variables and bindings, for connecting your app’s data to the user interface. These tools help you maintain a single source of truth for every piece of data in your app, in part by reducing the amount of glue logic you write. Select the tool that best suits the task you need to perform:

- Manage transient UI state locally within a view by wrapping value types as [State()](https://developer.apple.com/documentation/swiftui/state()) properties.
- Share a reference to a source of truth, like local state, using the [Binding](https://developer.apple.com/documentation/swiftui/binding) property wrapper.
- Connect to and observe reference model data in views by applying the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro to the model data type. Instantiate an observable model data type directly in a view with a [State()](https://developer.apple.com/documentation/swiftui/state()) property. Share the observable model data with other views in the hierarchy without passing a reference using the [Environment](https://developer.apple.com/documentation/swiftui/environment) property wrapper.

## Creating and sharing view state {#Creating-and-sharing-view-state}

- [Managing user interface state](1.1-ManagingUserInterfaceState/) — Encapsulate view-specific data within your app’s view hierarchy to make your views reusable.
- [State()](https://developer.apple.com/documentation/swiftui/state()) — Creates a property that can read and write a value managed by SwiftUI.
- [State(initialValue:)](https://developer.apple.com/documentation/swiftui/state(initialvalue:)) — Creates a property with an initial value that can read and write a value managed by SwiftUI.
- [State(wrappedValue:)](https://developer.apple.com/documentation/swiftui/state(wrappedvalue:)) — Creates a property with a wrapped value that can read and write a value managed by SwiftUI.
- [State](https://developer.apple.com/documentation/swiftui/state) — A property wrapper type that can read and write a value managed by SwiftUI.
- [Bindable](https://developer.apple.com/documentation/swiftui/bindable) — A property wrapper type that supports creating bindings to the mutable properties of observable objects.
- [Binding](https://developer.apple.com/documentation/swiftui/binding) — A property wrapper type that can read and write a value owned by a source of truth.

## Creating model data {#Creating-model-data}

- [Managing model data in your app](1.3-ManagingModelDataInYourApp/) — Create connections between your app’s data model and views.
- [Migrating from the Observable Object protocol to the Observable macro](1.4-MigratingFromTheObservableObjectProtocolToTheObservableMacro/) — Update your existing app to leverage the benefits of Observation in Swift.
- [Observable()](https://developer.apple.com/documentation/observation/observable()) — Defines and implements conformance of the Observable protocol.
- [Monitoring data changes in your app](1.5-MonitoringModelDataChangesInYourApp/) — Show changes to data in your app’s user interface by using observable objects.
- [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) — A property wrapper type that instantiates an observable object.
- [ObservedObject](https://developer.apple.com/documentation/swiftui/observedobject) — A property wrapper type that subscribes to an observable object and invalidates a view whenever the observable object changes.
- [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) — A type of object with a publisher that emits before the object has changed.

## Responding to data changes {#Responding-to-data-changes}

- [onChange(of:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onchange(of:initial:_:)) — Adds a modifier for this view that fires an action when a specific value changes.
- [onReceive(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onreceive(_:perform:)) — Adds an action to perform when this view detects data emitted by the given publisher.

## Distributing model data throughout your app {#Distributing-model-data-throughout-your-app}

- [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/view/environmentobject(_:)) — Supplies an observable object to a view’s hierarchy.
- [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/scene/environmentobject(_:)) — Supplies an `ObservableObject` to a view subhierarchy.
- [EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject) — A property wrapper type for an observable object that a parent or ancestor view supplies.

## Managing dynamic data {#Managing-dynamic-data}

- [DynamicProperty](https://developer.apple.com/documentation/swiftui/dynamicproperty) — An interface for a stored variable that updates an external property of a view.
