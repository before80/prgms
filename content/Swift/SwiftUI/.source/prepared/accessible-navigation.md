# Accessible navigation

Enable users to navigate to specific user interface elements using rotors.

## Overview {#Overview}

An accessibility rotor is a shortcut that enables users to quickly navigate to specific elements of the user interface, and, optionally, to specific ranges of text within those elements.

![](./images/accessible-navigation-hero@2x.png)

The system automatically provides rotors for many navigable elements, but you can supply additional rotors for specific purposes, or replace system rotors when they don’t automatically pick up off-screen elements, like those far down in a [LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack) or a [List](https://developer.apple.com/documentation/swiftui/list).

For design guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) in the Accessibility section of the Human Interface Guidelines.

## Working with rotors {#Working-with-rotors}

- [accessibilityRotor(_:entries:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:)) — Create an Accessibility Rotor with the specified user-visible label, and entries generated from the content closure.
- [accessibilityRotor(_:entries:entryID:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entryid:entrylabel:)) — Create an Accessibility Rotor with the specified user-visible label and entries.
- [accessibilityRotor(_:entries:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entrylabel:)) — Create an Accessibility Rotor with the specified user-visible label and entries.
- [accessibilityRotor(_:textRanges:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:textranges:)) — Create an Accessibility Rotor with the specified user-visible label and entries for each of the specified ranges. The Rotor will be attached to the current Accessibility element, and each entry will go the specified range of that element.

## Creating rotors {#Creating-rotors}

- [AccessibilityRotorContent](https://developer.apple.com/documentation/swiftui/accessibilityrotorcontent) — Content within an accessibility rotor.
- [AccessibilityRotorContentBuilder](https://developer.apple.com/documentation/swiftui/accessibilityrotorcontentbuilder) — Result builder you use to generate rotor entry content.
- [AccessibilityRotorEntry](https://developer.apple.com/documentation/swiftui/accessibilityrotorentry) — A struct representing an entry in an Accessibility Rotor.

## Replacing system rotors {#Replacing-system-rotors}

- [AccessibilitySystemRotor](https://developer.apple.com/documentation/swiftui/accessibilitysystemrotor) — Designates a Rotor that replaces one of the automatic, system-provided Rotors with a developer-provided Rotor.

## Configuring rotors {#Configuring-rotors}

- [accessibilityRotorEntry(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotorentry(id:in:)) — Defines an explicit identifier tying an Accessibility element for this view to an entry in an Accessibility Rotor.
- [accessibilityLinkedGroup(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylinkedgroup(id:in:)) — Links multiple accessibility elements so that the user can quickly navigate from one element to another, even when the elements are not near each other in the accessibility hierarchy.
- [accessibilitySortPriority(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)) — Sets the sort priority order for this view’s accessibility element, relative to other elements at the same level.
