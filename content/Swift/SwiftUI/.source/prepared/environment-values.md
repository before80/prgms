# Environment values

Share data throughout a view hierarchy using the environment.

## Overview {#Overview}

Views in SwiftUI can react to configuration information that they read from the environment using an [Environment](https://developer.apple.com/documentation/swiftui/environment) property wrapper.

![](./images/environment-values-hero@2x.png)

A view inherits its environment from its container view, subject to explicit changes from an [environment(_:_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:_:)) view modifier, or by implicit changes from one of the many modifiers that operate on environment values. As a result, you can configure a entire hierarchy of views by modifying the environment of the group’s container.

You can find many built-in environment values in the [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) structure. You can also create a custom [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) property by defining a new property in an extension to the environment values structure and applying the [Entry()](https://developer.apple.com/documentation/swiftui/entry()) macro to the variable declaration.

## Accessing environment values {#Accessing-environment-values}

- [Environment](https://developer.apple.com/documentation/swiftui/environment) — A property wrapper that reads a value from a view’s environment.
- [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) — A collection of environment values propagated through a view hierarchy.

## Creating custom environment values {#Creating-custom-environment-values}

- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) — Creates an environment values, transaction, container values, or focused values entry.
- [EnvironmentKey](https://developer.apple.com/documentation/swiftui/environmentkey) — A key for accessing values in the environment.

## Modifying the environment of a view {#Modifying-the-environment-of-a-view}

- [environment(_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:)) — Places an observable object in the view’s environment.
- [environment(_:_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:_:)) — Sets the environment value of the specified key path to the given value.
- [transformEnvironment(_:transform:)](https://developer.apple.com/documentation/swiftui/view/transformenvironment(_:transform:)) — Transforms the environment value of the specified key path with the given function.

## Modifying the environment of a scene {#Modifying-the-environment-of-a-scene}

- [environment(_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:)) — Places an observable object in the scene’s environment.
- [environment(_:_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:_:)) — Sets the environment value of the specified key path to the given value.
- [transformEnvironment(_:transform:)](https://developer.apple.com/documentation/swiftui/scene/transformenvironment(_:transform:)) — Transforms the environment value of the specified key path with the given function.
