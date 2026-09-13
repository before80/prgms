# App extensions

Extend your app’s basic functionality to other parts of the system, like by adding a Widget.

## Overview {#Overview}

Use SwiftUI along with [WidgetKit](https://developer.apple.com/documentation/widgetkit) to add widgets to your app.

![](./images/app-extensions-hero@2x.png)

Widgets provide quick access to relevant content from your app. Define a structure that conforms to the [Widget](https://developer.apple.com/documentation/swiftui/widget) protocol, and declare a view hierarchy for the widget. Configure the views inside the widget as you do other SwiftUI views, using view modifiers, including a few widget-specific modifiers.

For design guidance, see [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets) in the Human Interface Guidelines.

## Creating widgets {#Creating-widgets}

- [Building Widgets Using WidgetKit and SwiftUI](https://developer.apple.com/documentation/widgetkit/building-widgets-using-widgetkit-and-swiftui) — Create widgets to show your app’s content on the Home screen, with custom intents for user-customizable settings.
- [Creating a widget extension](https://developer.apple.com/documentation/widgetkit/creating-a-widget-extension) — Display your app’s content in a convenient, informative widget on various devices.
- [Keeping a widget up to date](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date) — Plan your widget’s timeline to show timely, relevant information using dynamic views, and update the timeline when things change.
- [Making a configurable widget](https://developer.apple.com/documentation/widgetkit/making-a-configurable-widget) — Give people the option to customize their widgets by adding a custom app intent to your project.
- [Widget](https://developer.apple.com/documentation/swiftui/widget) — The configuration and content of a widget to display on the Home screen or in Notification Center.
- [WidgetBundle](https://developer.apple.com/documentation/swiftui/widgetbundle) — A container used to expose multiple widgets from a single widget extension.
- [LimitedAvailabilityConfiguration](https://developer.apple.com/documentation/swiftui/limitedavailabilityconfiguration) — A type-erased widget configuration.
- [WidgetConfiguration](https://developer.apple.com/documentation/swiftui/widgetconfiguration) — A type that describes a widget’s content.
- [EmptyWidgetConfiguration](https://developer.apple.com/documentation/swiftui/emptywidgetconfiguration) — An empty widget configuration.

## Composing control widgets {#Composing-control-widgets}

- [ControlWidget](https://developer.apple.com/documentation/swiftui/controlwidget) — The configuration and content of a control widget to display in system spaces such as Control Center, the Lock Screen, and the Action Button.
- [ControlWidgetConfiguration](https://developer.apple.com/documentation/swiftui/controlwidgetconfiguration) — A type that describes a control widget’s content.
- [EmptyControlWidgetConfiguration](https://developer.apple.com/documentation/swiftui/emptycontrolwidgetconfiguration) — An empty control widget configuration.
- [ControlWidgetConfigurationBuilder](https://developer.apple.com/documentation/swiftui/controlwidgetconfigurationbuilder) — A custom attribute that constructs a control widget’s body.
- [ControlWidgetTemplate](https://developer.apple.com/documentation/swiftui/controlwidgettemplate) — A type that describes a control widget’s content.
- [EmptyControlWidgetTemplate](https://developer.apple.com/documentation/swiftui/emptycontrolwidgettemplate) — An empty control widget template.
- [ControlWidgetTemplateBuilder](https://developer.apple.com/documentation/swiftui/controlwidgettemplatebuilder) — A custom attribute that constructs a control widget template’s body.
- [controlWidgetActionHint(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetactionhint(_:)) — The action hint of the control described by the modified label.
- [controlWidgetStatus(_:)](https://developer.apple.com/documentation/swiftui/view/controlwidgetstatus(_:)) — The status of the control described by the modified label.

## Labeling a widget {#Labeling-a-widget}

- [widgetLabel(_:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(_:)) — Returns a localized text label that displays additional content outside the accessory family widget’s main SwiftUI view.
- [widgetLabel(label:)](https://developer.apple.com/documentation/swiftui/view/widgetlabel(label:)) — Creates a label for displaying additional content outside an accessory family widget’s main SwiftUI view.

## Styling a widget group {#Styling-a-widget-group}

- [accessoryWidgetGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/accessorywidgetgroupstyle(_:)) — The view modifier that can be applied to `AccessoryWidgetGroup` to specify the shape the three content views will be masked with. The value of `style` is set to `.automatic`, which is `.circular` by default.

## Controlling the accented group {#Controlling-the-accented-group}

- [widgetAccentable(_:)](https://developer.apple.com/documentation/swiftui/view/widgetaccentable(_:)) — Adds the view and all of its subviews to the accented group.

## Managing placement in the Dynamic Island {#Managing-placement-in-the-Dynamic-Island}

- [dynamicIsland(verticalPlacement:)](https://developer.apple.com/documentation/swiftui/view/dynamicisland(verticalplacement:)) — Specifies the vertical placement for a view of an expanded Live Activity that appears in the Dynamic Island.
