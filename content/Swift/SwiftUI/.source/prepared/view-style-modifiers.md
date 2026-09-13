# Style modifiers

Apply built-in styles to different types of views.

## Overview {#Overview}

SwiftUI defines built-in styles for certain kinds of views, and chooses the appropriate style for a particular presentation context. For example, a [Label](https://developer.apple.com/documentation/swiftui/label) might appear as an icon, a string title, or both, depending on factors like the platform, whether the view appears in a toolbar, and so on.

You can override the automatic style by using one of the style modifiers. These modifiers typically propagate through container views, so you can wrap an entire view hierarchy in a style modifier to affect all the views of the given type within the hierarchy. Some view types enable you to create custom styles, which you also apply using style modifiers.

For more information about styling views, see [View styles](../../3-ViewStyles/).

## Liquid Glass {#Liquid-Glass}

- [glassEffect(_:in:)](https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)) — Applies the Liquid Glass effect to a view.
- [glassEffectID(_:in:)](https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)) — Associates an identity value to Liquid Glass effects defined within this view.
- [glassEffectTransition(_:)](https://developer.apple.com/documentation/swiftui/view/glasseffecttransition(_:)) — Associates a glass effect transition with any glass effects defined within this view.
- [glassEffectUnion(id:namespace:)](https://developer.apple.com/documentation/swiftui/view/glasseffectunion(id:namespace:)) — Associates any Liquid Glass effects defined within this view to a union with the provided identifier.

## Controls {#Controls}

- [buttonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/buttonstyle(_:)) — Sets the style for buttons within this view to a button style with a custom appearance and standard interaction behavior.
- [buttonSizing(_:)](https://developer.apple.com/documentation/swiftui/view/buttonsizing(_:)) — The preferred sizing behavior of buttons in the view hierarchy.
- [datePickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/datepickerstyle(_:)) — Sets the style for date pickers within this view.
- [menuStyle(_:)](https://developer.apple.com/documentation/swiftui/view/menustyle(_:)) — Sets the style for menus within this view.
- [pickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/pickerstyle(_:)) — Sets the style for pickers within this view.
- [toggleStyle(_:)](https://developer.apple.com/documentation/swiftui/view/togglestyle(_:)) — Sets the style for toggles in a view hierarchy.

## Indicators {#Indicators}

- [gaugeStyle(_:)](https://developer.apple.com/documentation/swiftui/view/gaugestyle(_:)) — Sets the style for gauges within this view.
- [progressViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/progressviewstyle(_:)) — Sets the style for progress views in this view.

## Text {#Text}

- [labelStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labelstyle(_:)) — Sets the style for labels within this view.
- [labeledContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labeledcontentstyle(_:)) — Sets a style for labeled content.
- [textFieldStyle(_:)](https://developer.apple.com/documentation/swiftui/view/textfieldstyle(_:)) — Sets the style for text fields within this view.
- [textEditorStyle(_:)](https://developer.apple.com/documentation/swiftui/view/texteditorstyle(_:)) — Sets the style for text editors within this view.

## Collections {#Collections}

- [listStyle(_:)](https://developer.apple.com/documentation/swiftui/view/liststyle(_:)) — Sets the style for lists within this view.
- [tableStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tablestyle(_:)) — Sets the style for tables within this view.
- [disclosureGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/disclosuregroupstyle(_:)) — Sets the style for disclosure groups within this view.

## Presentation {#Presentation}

- [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) — Sets the style for navigation split views within this view.
- [tabViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewstyle(_:)) — Sets the style for the tab view within the current environment.
- [presentedWindowStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowstyle(_:)) — Sets the style for windows created by interacting with this view.
- [presentedWindowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowtoolbarstyle(_:)) — Sets the style for the toolbar in windows created by interacting with this view.

## Groups {#Groups}

- [controlGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/controlgroupstyle(_:)) — Sets the style for control groups within this view.
- [formStyle(_:)](https://developer.apple.com/documentation/swiftui/view/formstyle(_:)) — Sets the style for forms in a view hierarchy.
- [groupBoxStyle(_:)](https://developer.apple.com/documentation/swiftui/view/groupboxstyle(_:)) — Sets the style for group boxes within this view.
- [indexViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/indexviewstyle(_:)) — Sets the style for the index view within the current environment.
