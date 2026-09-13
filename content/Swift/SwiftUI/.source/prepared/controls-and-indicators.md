# Controls and indicators

Display values and get user selections.

## Overview {#Overview}

SwiftUI provides controls that enable user interaction specific to each platform and context. For example, people can initiate events with buttons and links, or choose among a set of discrete values with different kinds of pickers. You can also display information to the user with indicators like progress views and gauges.

![](./images/controls-and-indicators-hero@2x.png)

Use these built-in controls and indicators when composing custom views, and style them to match the needs of your app’s user interface. For design guidance, see [Menus and actions](https://developer.apple.com/design/human-interface-guidelines/menus-and-actions), [Selection and input](https://developer.apple.com/design/human-interface-guidelines/selection-and-input), and [Status](https://developer.apple.com/design/human-interface-guidelines/status) in the Human Interface Guidelines.

## Creating buttons {#Creating-buttons}

- [Button](https://developer.apple.com/documentation/swiftui/button) — A control that initiates an action.
- [buttonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/buttonstyle(_:)) — Sets the style for buttons within this view to a button style with a custom appearance and standard interaction behavior.
- [buttonBorderShape(_:)](https://developer.apple.com/documentation/swiftui/view/buttonbordershape(_:)) — Sets the border shape for buttons in this view.
- [ButtonBorderShape](https://developer.apple.com/documentation/swiftui/buttonbordershape) — A shape used to draw a button’s border.
- [buttonRepeatBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/buttonrepeatbehavior(_:)) — Sets whether buttons in this view should repeatedly trigger their actions on prolonged interactions.
- [ButtonRepeatBehavior](https://developer.apple.com/documentation/swiftui/buttonrepeatbehavior) — The options for controlling the repeatability of button actions.
- [buttonRepeatBehavior](https://developer.apple.com/documentation/swiftui/environmentvalues/buttonrepeatbehavior) — Whether buttons with this associated environment should repeatedly trigger their actions on prolonged interactions.
- [buttonSizing(_:)](https://developer.apple.com/documentation/swiftui/view/buttonsizing(_:)) — The preferred sizing behavior of buttons in the view hierarchy.
- [ButtonSizing](https://developer.apple.com/documentation/swiftui/buttonsizing) — The sizing behavior of `Button`s and other button-like controls.
- [ButtonRole](https://developer.apple.com/documentation/swiftui/buttonrole) — A value that describes the purpose of a button.

## Creating special-purpose buttons {#Creating-special-purpose-buttons}

- [EditButton](https://developer.apple.com/documentation/swiftui/editbutton) — A button that toggles the edit mode environment value.
- [PasteButton](https://developer.apple.com/documentation/swiftui/pastebutton) — A system button that reads items from the pasteboard and delivers it to a closure.
- [RenameButton](https://developer.apple.com/documentation/swiftui/renamebutton) — A button that triggers a standard rename action.

## Linking to other content {#Linking-to-other-content}

- [Link](https://developer.apple.com/documentation/swiftui/link) — A control for navigating to a URL.
- [ShareLink](https://developer.apple.com/documentation/swiftui/sharelink) — A view that controls a sharing presentation.
- [SharePreview](https://developer.apple.com/documentation/swiftui/sharepreview) — A representation of a type to display in a share preview.
- [TextFieldLink](https://developer.apple.com/documentation/swiftui/textfieldlink) — A control that requests text input from the user when pressed.
- [HelpLink](https://developer.apple.com/documentation/swiftui/helplink) — A button with a standard appearance that opens app-specific help documentation.

## Getting numeric inputs {#Getting-numeric-inputs}

- [Slider](https://developer.apple.com/documentation/swiftui/slider) — A control for selecting a value from a bounded linear range of values.
- [Stepper](https://developer.apple.com/documentation/swiftui/stepper) — A control that performs increment and decrement actions.
- [Toggle](https://developer.apple.com/documentation/swiftui/toggle) — A control that toggles between on and off states.
- [toggleStyle(_:)](https://developer.apple.com/documentation/swiftui/view/togglestyle(_:)) — Sets the style for toggles in a view hierarchy.

## Choosing from a set of options {#Choosing-from-a-set-of-options}

- [Picker](https://developer.apple.com/documentation/swiftui/picker) — A control for selecting from a set of mutually exclusive values.
- [pickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/pickerstyle(_:)) — Sets the style for pickers within this view.
- [horizontalRadioGroupLayout()](https://developer.apple.com/documentation/swiftui/view/horizontalradiogrouplayout()) — Sets the style for radio group style pickers within this view to be horizontally positioned with the radio buttons inside the layout.
- [defaultWheelPickerItemHeight(_:)](https://developer.apple.com/documentation/swiftui/view/defaultwheelpickeritemheight(_:)) — Sets the default wheel-style picker item height.
- [defaultWheelPickerItemHeight](https://developer.apple.com/documentation/swiftui/environmentvalues/defaultwheelpickeritemheight) — The default height of an item in a wheel-style picker, such as a date picker.
- [paletteSelectionEffect(_:)](https://developer.apple.com/documentation/swiftui/view/paletteselectioneffect(_:)) — Specifies the selection effect to apply to a palette item.
- [PaletteSelectionEffect](https://developer.apple.com/documentation/swiftui/paletteselectioneffect) — The selection effect to apply to a palette item.

## Choosing dates {#Choosing-dates}

- [DatePicker](https://developer.apple.com/documentation/swiftui/datepicker) — A control for selecting an absolute date.
- [datePickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/datepickerstyle(_:)) — Sets the style for date pickers within this view.
- [MultiDatePicker](https://developer.apple.com/documentation/swiftui/multidatepicker) — A control for picking multiple dates.
- [calendar](https://developer.apple.com/documentation/swiftui/environmentvalues/calendar) — The current calendar that views should use when handling dates.
- [timeZone](https://developer.apple.com/documentation/swiftui/environmentvalues/timezone) — The current time zone that views should use when handling dates.

## Choosing a color {#Choosing-a-color}

- [ColorPicker](https://developer.apple.com/documentation/swiftui/colorpicker) — A control used to select a color from the system color picker UI.

## Indicating a value {#Indicating-a-value}

- [Gauge](https://developer.apple.com/documentation/swiftui/gauge) — A view that shows a value within a range.
- [gaugeStyle(_:)](https://developer.apple.com/documentation/swiftui/view/gaugestyle(_:)) — Sets the style for gauges within this view.
- [ProgressView](https://developer.apple.com/documentation/swiftui/progressview) — A view that shows the progress toward completion of a task.
- [progressViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/progressviewstyle(_:)) — Sets the style for progress views in this view.
- [DefaultDateProgressLabel](https://developer.apple.com/documentation/swiftui/defaultdateprogresslabel) — The default type of the current value label when used by a date-relative progress view.
- [DefaultButtonLabel](https://developer.apple.com/documentation/swiftui/defaultbuttonlabel) — The default label to use for a button.

## Indicating missing content {#Indicating-missing-content}

- [ContentUnavailableView](https://developer.apple.com/documentation/swiftui/contentunavailableview) — An interface, consisting of a label and additional content, that you display when the content of your app is unavailable to users.

## Providing haptic feedback {#Providing-haptic-feedback}

- [sensoryFeedback(_:trigger:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:)) — Plays the specified `feedback` when the provided `trigger` value changes.
- [sensoryFeedback(trigger:_:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(trigger:_:)) — Plays feedback when returned from the `feedback` closure after the provided `trigger` value changes.
- [sensoryFeedback(_:trigger:condition:)](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:condition:)) — Plays the specified `feedback` when the provided `trigger` value changes and the `condition` closure returns `true`.
- [SensoryFeedback](https://developer.apple.com/documentation/swiftui/sensoryfeedback) — Represents a type of haptic and/or audio feedback that can be played.

## Sizing controls {#Sizing-controls}

- [controlSize(_:)](https://developer.apple.com/documentation/swiftui/view/controlsize(_:)) — Sets the size for controls within this view.
- [controlSize](https://developer.apple.com/documentation/swiftui/environmentvalues/controlsize) — The size to apply to controls within a view.
- [ControlSize](https://developer.apple.com/documentation/swiftui/controlsize) — The size classes, like regular or small, that you can apply to controls within a view.
