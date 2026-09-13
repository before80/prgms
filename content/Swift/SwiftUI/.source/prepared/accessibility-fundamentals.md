# Accessibility fundamentals

Make your SwiftUI apps accessible to everyone, including people with disabilities.

## Overview {#Overview}

Like all Apple UI frameworks, SwiftUI comes with built-in accessibility support. The framework introspects common elements like navigation views, lists, text fields, sliders, buttons, and so on, and provides basic accessibility labels and values by default. You don’t have to do any extra work to enable these standard accessibility features.

![](./images/accessibility-fundamentals-hero@2x.png)

SwiftUI also provides tools to help you enhance the accessibility of your app. To find out what enhancements you need, try using your app with accessibility features like VoiceOver, Voice Control, and Switch Control, or get feedback from users of your app that regularly use these features. Then use the accessibility view modifiers that SwiftUI provides to improve the experience. For example, you can explicitly add accessibility labels to elements in your UI using the [accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)) or the [accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)) view modifier.

Customize your use of accessibility modifiers for all the platforms that your app runs on. For example, you may need to adjust the accessibility elements for a companion Apple Watch app that shares a common code base with an iOS app. If you integrate AppKit or UIKit controls in SwiftUI, expose any accessibility labels and make them accessible from your [NSViewRepresentable](https://developer.apple.com/documentation/swiftui/nsviewrepresentable) or [UIViewRepresentable](https://developer.apple.com/documentation/swiftui/uiviewrepresentable) views, or provide custom accessibility information if the underlying accessibility labels aren’t available.

For design guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) in the Human Interface Guidelines.

## Essentials {#Essentials}

- [Creating accessible views](1.1-CreatingAccessibleViews/) — Make your app accessible to everyone by applying accessibility modifiers to your SwiftUI views.

## Creating accessible elements {#Creating-accessible-elements}

- [accessibilityElement(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:)) — Creates a new accessibility element, or modifies the [AccessibilityChildBehavior](https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior) of the existing accessibility element.
- [accessibilityChildren(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilitychildren(children:)) — Replaces the existing accessibility element’s children with one or more new synthetic accessibility elements.
- [accessibilityRepresentation(representation:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:)) — Replaces one or more accessibility elements for this view with new accessibility elements.
- [AccessibilityChildBehavior](https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior) — Defines the behavior for the child elements of the new parent element.

## Identifying elements {#Identifying-elements}

- [accessibilityIdentifier(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:)) — Uses the string you specify to identify the view.
- [accessibilityIdentifier(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:isenabled:)) — Uses the string you specify to identify the view.

## Hiding elements {#Hiding-elements}

- [accessibilityHidden(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:)) — Specifies whether to hide this view from system accessibility features.
- [accessibilityHidden(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:isenabled:)) — Specifies whether to hide this view from system accessibility features.

## Supporting types {#Supporting-types}

- [AccessibilityTechnologies](https://developer.apple.com/documentation/swiftui/accessibilitytechnologies) — Accessibility technologies available to the system.
- [AccessibilityAttachmentModifier](https://developer.apple.com/documentation/swiftui/accessibilityattachmentmodifier) — A view modifier that adds accessibility properties to the view
