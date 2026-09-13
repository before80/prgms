# Focus

Identify and control which visible object responds to user interaction.

## Overview {#Overview}

Focus indicates which element in the display receives the next input. Use view modifiers to indicate which views can receive focus, to detect which view has focus, and to programmatically control focus state.

![](./images/focus-hero@2x.png)

For design guidance, see [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) in the Human Interface Guidelines.

## Essentials {#Essentials}

- [Focus Cookbook: Supporting and enhancing focus-driven interactions in your SwiftUI app](5.1-FocusCookbookSample/) — Create custom focusable views with key-press handlers that accelerate keyboard input and support movement, and control focus programmatically.

## Indicating that a view can receive focus {#Indicating-that-a-view-can-receive-focus}

- [focusable(_:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:)) — Specifies if the view is focusable.
- [focusable(_:interactions:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:interactions:)) — Specifies if the view is focusable, and if so, what focus-driven interactions it supports.
- [FocusInteractions](https://developer.apple.com/documentation/swiftui/focusinteractions) — Values describe different focus interactions that a view can support.

## Managing focus state {#Managing-focus-state}

- [focused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/focused(_:equals:)) — Modifies this view by binding its focus state to the given state value.
- [focused(_:)](https://developer.apple.com/documentation/swiftui/view/focused(_:)) — Modifies this view by binding its focus state to the given Boolean state value.
- [isFocused](https://developer.apple.com/documentation/swiftui/environmentvalues/isfocused) — Returns whether the nearest focusable ancestor has focus.
- [FocusState](https://developer.apple.com/documentation/swiftui/focusstate) — A property wrapper type that can read and write a value that SwiftUI updates as the placement of focus within the scene changes.
- [FocusedValue](https://developer.apple.com/documentation/swiftui/focusedvalue) — A property wrapper for observing values from the focused view or one of its ancestors.
- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) — Creates an environment values, transaction, container values, or focused values entry.
- [FocusedValueKey](https://developer.apple.com/documentation/swiftui/focusedvaluekey) — A protocol for identifier types used when publishing and observing focused values.
- [FocusedBinding](https://developer.apple.com/documentation/swiftui/focusedbinding) — A convenience property wrapper for observing and automatically unwrapping state bindings from the focused view or one of its ancestors.
- [searchFocused(_:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:)) — Modifies this view by binding the focus state of the search field associated with the nearest searchable modifier to the given Boolean value.
- [searchFocused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:equals:)) — Modifies this view by binding the focus state of the search field associated with the nearest searchable modifier to the given value.

## Exposing value types to focused views {#Exposing-value-types-to-focused-views}

- [focusedValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:)) — Sets the focused value for the given object type.
- [focusedValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:_:)) — Modifies this view by injecting a value that you provide for use by other views whose state depends on the focused view hierarchy.
- [focusedSceneValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:)) — Sets the focused value for the given object type at a scene-wide scope.
- [focusedSceneValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:_:)) — Modifies this view by injecting a value that you provide for use by other views whose state depends on the focused scene.
- [FocusedValues](https://developer.apple.com/documentation/swiftui/focusedvalues) — A collection of state exported by the focused scene or view and its ancestors.

## Exposing reference types to focused views {#Exposing-reference-types-to-focused-views}

- [focusedObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedobject(_:)) — Creates a new view that exposes the provided object to other views whose whose state depends on the focused view hierarchy.
- [focusedSceneObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedsceneobject(_:)) — Creates a new view that exposes the provided object to other views whose whose state depends on the active scene.
- [FocusedObject](https://developer.apple.com/documentation/swiftui/focusedobject) — A property wrapper type for an observable object supplied by the focused view or one of its ancestors.

## Setting focus scope {#Setting-focus-scope}

- [focusScope(_:)](https://developer.apple.com/documentation/swiftui/view/focusscope(_:)) — Creates a focus scope that SwiftUI uses to limit default focus preferences.
- [focusSection()](https://developer.apple.com/documentation/swiftui/view/focussection()) — Indicates that the view’s frame and cohort of focusable descendants should be used to guide focus movement.

## Controlling default focus {#Controlling-default-focus}

- [prefersDefaultFocus(_:in:)](https://developer.apple.com/documentation/swiftui/view/prefersdefaultfocus(_:in:)) — Indicates that the view should receive focus by default for a given namespace.
- [defaultFocus(_:_:priority:)](https://developer.apple.com/documentation/swiftui/view/defaultfocus(_:_:priority:)) — Defines a region of the window in which default focus is evaluated by assigning a value to a given focus state binding.
- [DefaultFocusEvaluationPriority](https://developer.apple.com/documentation/swiftui/defaultfocusevaluationpriority) — Prioritizations for default focus preferences when evaluating where to move focus in different circumstances.

## Resetting focus {#Resetting-focus}

- [resetFocus](https://developer.apple.com/documentation/swiftui/environmentvalues/resetfocus) — An action that requests the focus system to reevaluate default focus.
- [ResetFocusAction](https://developer.apple.com/documentation/swiftui/resetfocusaction) — An environment value that provides the ability to reevaluate default focus.

## Configuring effects {#Configuring-effects}

- [focusEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/focuseffectdisabled(_:)) — Adds a condition that controls whether this view can display focus effects, such as a default focus ring or hover effect.
- [isFocusEffectEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/isfocuseffectenabled) — A Boolean value that indicates whether the view associated with this environment allows focus effects to be displayed.
