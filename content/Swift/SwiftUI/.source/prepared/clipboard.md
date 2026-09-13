# Clipboard

Enable people to move or duplicate items by issuing Copy and Paste commands.

## Overview {#Overview}

When people issue standard Copy and Cut commands, they expect to move items to the system’s Clipboard, from which they can paste the items into another place in the same app or into another app. Your app can participate in this activity if you add view modifiers that indicate how to respond to the standard commands.

![](./images/clipboard-hero@2x.png)

In your copy and paste modifiers, provide or accept types that conform to the [Transferable](https://developer.apple.com/documentation/coretransferable/transferable) protocol, or that inherit from the [NSItemProvider](https://developer.apple.com/documentation/foundation/nsitemprovider) class. When possible, prefer using transferable items.

## Copying transferable items {#Copying-transferable-items}

- [copyable(_:)](https://developer.apple.com/documentation/swiftui/view/copyable(_:)) — Specifies a list of items to copy in response to the system’s Copy command.
- [cuttable(for:action:)](https://developer.apple.com/documentation/swiftui/view/cuttable(for:action:)) — Specifies an action that moves items to the Clipboard in response to the system’s Cut command.
- [pasteDestination(for:action:validator:)](https://developer.apple.com/documentation/swiftui/view/pastedestination(for:action:validator:)) — Specifies an action that adds validated items to a view in response to the system’s Paste command.

## Copying items using item providers {#Copying-items-using-item-providers}

- [onCopyCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncopycommand(perform:)) — Adds an action to perform in response to the system’s Copy command.
- [onCutCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncutcommand(perform:)) — Adds an action to perform in response to the system’s Cut command.
- [onPasteCommand(of:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:perform:)) — Adds an action to perform in response to the system’s Paste command.
- [onPasteCommand(of:validator:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:validator:perform:)) — Adds an action to perform in response to the system’s Paste command with items that you validate.
