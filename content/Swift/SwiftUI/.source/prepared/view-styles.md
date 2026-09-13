# View styles

Apply built-in and custom appearances and behaviors to different types of views.

## Overview {#Overview}

SwiftUI defines built-in styles for certain kinds of views and automatically selects the appropriate style for a particular presentation context. For example, a [Label](https://developer.apple.com/documentation/swiftui/label) might appear as an icon, a string title, or both, depending on factors like the platform, whether the view appears in a toolbar, and so on.

![](./images/view-styles-hero@2x.png)

You can override the automatic style by using one of the style view modifiers. These modifiers typically propagate throughout a container view, so that you can wrap a view hierarchy in a style modifier to affect all the views of the given type within the hierarchy.

Any of the style protocols that define a `makeBody(configuration:)` method, like [ToggleStyle](https://developer.apple.com/documentation/swiftui/togglestyle), also enable you to define custom styles. Create a type that conforms to the corresponding style protocol and implement its `makeBody(configuration:)` method. Then apply the new style using a style view modifier exactly like a built-in style.

## Styling views with Liquid Glass {#Styling-views-with-Liquid-Glass}

- [Applying Liquid Glass to custom views](3.1-ApplyingLiquidGlassToCustomViews/) — Configure, combine, and morph views using Liquid Glass effects.
- [Landmarks: Building an app with Liquid Glass](../../essentials/1-LandmarksBuildingAnAppWithLiquidGlass/) — Enhance your app experience with system-provided and custom Liquid Glass.
- [glassEffect(_:in:)](https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)) — Applies the Liquid Glass effect to a view.
- [glassEffectID(_:in:)](https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)) — Associates an identity value to Liquid Glass effects defined within this view.
- [glassEffectTransition(_:)](https://developer.apple.com/documentation/swiftui/view/glasseffecttransition(_:)) — Associates a glass effect transition with any glass effects defined within this view.
- [glassEffectUnion(id:namespace:)](https://developer.apple.com/documentation/swiftui/view/glasseffectunion(id:namespace:)) — Associates any Liquid Glass effects defined within this view to a union with the provided identifier.
- [interactive(_:)](https://developer.apple.com/documentation/swiftui/glass/interactive(_:)) — Returns a copy of the structure configured to be interactive.
- [GlassEffectContainer](https://developer.apple.com/documentation/swiftui/glasseffectcontainer) — A view that combines multiple Liquid Glass shapes into a single shape that can morph individual shapes into one another.
- [GlassEffectTransition](https://developer.apple.com/documentation/swiftui/glasseffecttransition) — A structure that describes changes to apply when a glass effect is added or removed from the view hierarchy.
- [GlassButtonStyle](https://developer.apple.com/documentation/swiftui/glassbuttonstyle) — A button style that applies glass border artwork based on the button’s context.
- [GlassProminentButtonStyle](https://developer.apple.com/documentation/swiftui/glassprominentbuttonstyle) — A button style that applies prominent glass border artwork based on the button’s context.
- [DefaultGlassEffectShape](https://developer.apple.com/documentation/swiftui/defaultglasseffectshape) — The default shape applied by glass effects, a capsule.

## Styling buttons {#Styling-buttons}

- [buttonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/buttonstyle(_:)) — Sets the style for buttons within this view to a button style with a custom appearance and standard interaction behavior.
- [ButtonStyle](https://developer.apple.com/documentation/swiftui/buttonstyle) — A type that applies standard interaction behavior and a custom appearance to all buttons within a view hierarchy.
- [ButtonStyleConfiguration](https://developer.apple.com/documentation/swiftui/buttonstyleconfiguration) — The properties of a button.
- [PrimitiveButtonStyle](https://developer.apple.com/documentation/swiftui/primitivebuttonstyle) — A type that applies custom interaction behavior and a custom appearance to all buttons within a view hierarchy.
- [PrimitiveButtonStyleConfiguration](https://developer.apple.com/documentation/swiftui/primitivebuttonstyleconfiguration) — The properties of a button.
- [signInWithAppleButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/signinwithapplebuttonstyle(_:)) — Sets the style used for displaying the control (see `SignInWithAppleButton.Style`).
- [buttonSizing(_:)](https://developer.apple.com/documentation/swiftui/view/buttonsizing(_:)) — The preferred sizing behavior of buttons in the view hierarchy.
- [ButtonSizing](https://developer.apple.com/documentation/swiftui/buttonsizing) — The sizing behavior of `Button`s and other button-like controls.

## Styling pickers {#Styling-pickers}

- [pickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/pickerstyle(_:)) — Sets the style for pickers within this view.
- [PickerStyle](https://developer.apple.com/documentation/swiftui/pickerstyle) — A type that specifies the appearance and interaction of all pickers within a view hierarchy.
- [datePickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/datepickerstyle(_:)) — Sets the style for date pickers within this view.
- [DatePickerStyle](https://developer.apple.com/documentation/swiftui/datepickerstyle) — A type that specifies the appearance and interaction of all date pickers within a view hierarchy.

## Styling menus {#Styling-menus}

- [menuStyle(_:)](https://developer.apple.com/documentation/swiftui/view/menustyle(_:)) — Sets the style for menus within this view.
- [MenuStyle](https://developer.apple.com/documentation/swiftui/menustyle) — A type that applies standard interaction behavior and a custom appearance to all menus within a view hierarchy.
- [MenuStyleConfiguration](https://developer.apple.com/documentation/swiftui/menustyleconfiguration) — A configuration of a menu.

## Styling toggles {#Styling-toggles}

- [toggleStyle(_:)](https://developer.apple.com/documentation/swiftui/view/togglestyle(_:)) — Sets the style for toggles in a view hierarchy.
- [ToggleStyle](https://developer.apple.com/documentation/swiftui/togglestyle) — The appearance and behavior of a toggle.
- [ToggleStyleConfiguration](https://developer.apple.com/documentation/swiftui/togglestyleconfiguration) — The properties of a toggle instance.

## Styling indicators {#Styling-indicators}

- [gaugeStyle(_:)](https://developer.apple.com/documentation/swiftui/view/gaugestyle(_:)) — Sets the style for gauges within this view.
- [GaugeStyle](https://developer.apple.com/documentation/swiftui/gaugestyle) — Defines the implementation of all gauge instances within a view hierarchy.
- [GaugeStyleConfiguration](https://developer.apple.com/documentation/swiftui/gaugestyleconfiguration) — The properties of a gauge instance.
- [progressViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/progressviewstyle(_:)) — Sets the style for progress views in this view.
- [ProgressViewStyle](https://developer.apple.com/documentation/swiftui/progressviewstyle) — A type that applies standard interaction behavior to all progress views within a view hierarchy.
- [ProgressViewStyleConfiguration](https://developer.apple.com/documentation/swiftui/progressviewstyleconfiguration) — The properties of a progress view instance.

## Styling views that display text {#Styling-views-that-display-text}

- [labelStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labelstyle(_:)) — Sets the style for labels within this view.
- [LabelStyle](https://developer.apple.com/documentation/swiftui/labelstyle) — A type that applies a custom appearance to all labels within a view.
- [LabelStyleConfiguration](https://developer.apple.com/documentation/swiftui/labelstyleconfiguration) — The properties of a label.
- [textFieldStyle(_:)](https://developer.apple.com/documentation/swiftui/view/textfieldstyle(_:)) — Sets the style for text fields within this view.
- [TextFieldStyle](https://developer.apple.com/documentation/swiftui/textfieldstyle) — A specification for the appearance and interaction of a text field.
- [textEditorStyle(_:)](https://developer.apple.com/documentation/swiftui/view/texteditorstyle(_:)) — Sets the style for text editors within this view.
- [TextEditorStyle](https://developer.apple.com/documentation/swiftui/texteditorstyle) — A specification for the appearance and interaction of a text editor.
- [TextEditorStyleConfiguration](https://developer.apple.com/documentation/swiftui/texteditorstyleconfiguration) — The properties of a text editor.

## Styling collection views {#Styling-collection-views}

- [listStyle(_:)](https://developer.apple.com/documentation/swiftui/view/liststyle(_:)) — Sets the style for lists within this view.
- [ListStyle](https://developer.apple.com/documentation/swiftui/liststyle) — A protocol that describes the behavior and appearance of a list.
- [tableStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tablestyle(_:)) — Sets the style for tables within this view.
- [TableStyle](https://developer.apple.com/documentation/swiftui/tablestyle) — A type that applies a custom appearance to all tables within a view.
- [TableStyleConfiguration](https://developer.apple.com/documentation/swiftui/tablestyleconfiguration) — The properties of a table.
- [disclosureGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/disclosuregroupstyle(_:)) — Sets the style for disclosure groups within this view.
- [DisclosureGroupStyle](https://developer.apple.com/documentation/swiftui/disclosuregroupstyle) — A type that specifies the appearance and interaction of disclosure groups within a view hierarchy.

## Styling navigation views {#Styling-navigation-views}

- [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) — Sets the style for navigation split views within this view.
- [NavigationSplitViewStyle](https://developer.apple.com/documentation/swiftui/navigationsplitviewstyle) — A type that specifies the appearance and interaction of navigation split views within a view hierarchy.
- [tabViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewstyle(_:)) — Sets the style for the tab view within the current environment.
- [TabViewStyle](https://developer.apple.com/documentation/swiftui/tabviewstyle) — A specification for the appearance and interaction of a tab view.

## Styling groups {#Styling-groups}

- [controlGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/controlgroupstyle(_:)) — Sets the style for control groups within this view.
- [ControlGroupStyle](https://developer.apple.com/documentation/swiftui/controlgroupstyle) — Defines the implementation of all control groups within a view hierarchy.
- [ControlGroupStyleConfiguration](https://developer.apple.com/documentation/swiftui/controlgroupstyleconfiguration) — The properties of a control group.
- [formStyle(_:)](https://developer.apple.com/documentation/swiftui/view/formstyle(_:)) — Sets the style for forms in a view hierarchy.
- [FormStyle](https://developer.apple.com/documentation/swiftui/formstyle) — The appearance and behavior of a form.
- [FormStyleConfiguration](https://developer.apple.com/documentation/swiftui/formstyleconfiguration) — The properties of a form instance.
- [groupBoxStyle(_:)](https://developer.apple.com/documentation/swiftui/view/groupboxstyle(_:)) — Sets the style for group boxes within this view.
- [GroupBoxStyle](https://developer.apple.com/documentation/swiftui/groupboxstyle) — A type that specifies the appearance and interaction of all group boxes within a view hierarchy.
- [GroupBoxStyleConfiguration](https://developer.apple.com/documentation/swiftui/groupboxstyleconfiguration) — The properties of a group box instance.
- [indexViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/indexviewstyle(_:)) — Sets the style for the index view within the current environment.
- [IndexViewStyle](https://developer.apple.com/documentation/swiftui/indexviewstyle) — Defines the implementation of all `IndexView` instances within a view hierarchy.
- [labeledContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labeledcontentstyle(_:)) — Sets a style for labeled content.
- [LabeledContentStyle](https://developer.apple.com/documentation/swiftui/labeledcontentstyle) — The appearance and behavior of a labeled content instance..
- [LabeledContentStyleConfiguration](https://developer.apple.com/documentation/swiftui/labeledcontentstyleconfiguration) — The properties of a labeled content instance.

## Styling windows from a view inside the window {#Styling-windows-from-a-view-inside-the-window}

- [presentedWindowStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowstyle(_:)) — Sets the style for windows created by interacting with this view.
- [presentedWindowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowtoolbarstyle(_:)) — Sets the style for the toolbar in windows created by interacting with this view.

## Adding a glass background on views in visionOS {#Adding-a-glass-background-on-views-in-visionOS}

- [glassBackgroundEffect(displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(displaymode:)) — Fills the view’s background with an automatic glass background effect and container-relative rounded rectangle shape.
- [glassBackgroundEffect(in:displayMode:)](https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(in:displaymode:)) — Fills the view’s background with an automatic glass background effect and a shape that you specify.
- [GlassBackgroundDisplayMode](https://developer.apple.com/documentation/swiftui/glassbackgrounddisplaymode) — The display mode of a glass background.
- [GlassBackgroundEffect](https://developer.apple.com/documentation/swiftui/glassbackgroundeffect) — A specification for the appearance of a glass background.
- [AutomaticGlassBackgroundEffect](https://developer.apple.com/documentation/swiftui/automaticglassbackgroundeffect) — The automatic glass background effect.
- [GlassBackgroundEffectConfiguration](https://developer.apple.com/documentation/swiftui/glassbackgroundeffectconfiguration) — A configuration used to build a custom effect.
- [FeatheredGlassBackgroundEffect](https://developer.apple.com/documentation/swiftui/featheredglassbackgroundeffect) — The feathered glass background effect.
- [PlateGlassBackgroundEffect](https://developer.apple.com/documentation/swiftui/plateglassbackgroundeffect) — The plate glass background effect.
