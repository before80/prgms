# Deprecated initializers

Review deprecated text field initializers.

## Overview {#Overview}

Use view modifiers to specify change and commit behaviors for a text field when replacing these initializers. Use the [onSubmit(of:_:)](https://developer.apple.com/documentation/swiftui/view/onsubmit(of:_:)) view modifier to get the behavior provided by the `onCommit` parameter. Use [focused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/focused(_:equals:)) and [FocusState](https://developer.apple.com/documentation/swiftui/focusstate) to get the behavior provided by the `onEditingChanged` parameter.

## Creating a text field with a string {#Creating-a-text-field-with-a-string}

- [init(_:text:onEditingChanged:onCommit:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:text:oneditingchanged:oncommit:)) — Creates a text field with a text label generated from a localized title string.
- [init(_:text:onCommit:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:text:oncommit:)) — Creates a text field with a text label generated from a localized title string.
- [init(_:text:onEditingChanged:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:text:oneditingchanged:)) — Creates a text field with a text label generated from a localized title string.

## Creating a text field with a value {#Creating-a-text-field-with-a-value}

- [init(_:value:formatter:onEditingChanged:onCommit:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:value:formatter:oneditingchanged:oncommit:)) — Create an instance which binds over an arbitrary type, `V`.
- [init(_:value:formatter:onCommit:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:value:formatter:oncommit:)) — Create an instance which binds over an arbitrary type, `V`.
- [init(_:value:formatter:onEditingChanged:)](https://developer.apple.com/documentation/swiftui/textfield/init(_:value:formatter:oneditingchanged:)) — Create an instance which binds over an arbitrary type, `V`.
