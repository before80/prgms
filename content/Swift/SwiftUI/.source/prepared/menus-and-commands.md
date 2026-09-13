# Menus and commands

Provide space-efficient, context-dependent access to commands and controls.

## Overview {#Overview}

Use a menu to provide people with easy access to common commands. You can add items to a macOS or iPadOS app’s menu bar using the [commands(content:)](https://developer.apple.com/documentation/swiftui/scene/commands(content:)) scene modifier, or create context menus that people reveal near their current task using the [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) view modifier.

![](./images/menus-and-commands-hero@2x.png)

Create submenus by nesting [Menu](https://developer.apple.com/documentation/swiftui/menu) instances inside others. Use a [Divider](https://developer.apple.com/documentation/swiftui/divider) view to create a separator between menu elements.

For design guidance, see [Menus](https://developer.apple.com/design/human-interface-guidelines/menus) in the Human Interface Guidelines.

## Building a menu bar {#Building-a-menu-bar}

- [Building and customizing the menu bar with SwiftUI](../../appstructure/2-Scenes/2.1-BuildingAndCustomizingTheMenuBarWithSwiftui/) — Provide a seamless, cross-platform user experience by building a native menu bar for iPadOS and macOS.

## Creating a menu {#Creating-a-menu}

- [Populating SwiftUI menus with adaptive controls](8.1-PopulatingSwiftuiMenusWithAdaptiveControls/) — Improve your app by populating menus with controls and organizing your content intuitively.
- [Menu](https://developer.apple.com/documentation/swiftui/menu) — A control for presenting a menu of actions.
- [menuStyle(_:)](https://developer.apple.com/documentation/swiftui/view/menustyle(_:)) — Sets the style for menus within this view.

## Creating context menus {#Creating-context-menus}

- [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) — Adds a context menu to a view.
- [contextMenu(menuItems:preview:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:preview:)) — Adds a context menu with a custom preview to a view.
- [contextMenu(forSelectionType:menu:primaryAction:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(forselectiontype:menu:primaryaction:)) — Adds an item-based context menu to a view.

## Defining commands {#Defining-commands}

- [commands(content:)](https://developer.apple.com/documentation/swiftui/scene/commands(content:)) — Adds commands to the scene.
- [commandsRemoved()](https://developer.apple.com/documentation/swiftui/scene/commandsremoved()) — Removes all commands defined by the modified scene.
- [commandsReplaced(content:)](https://developer.apple.com/documentation/swiftui/scene/commandsreplaced(content:)) — Replaces all commands defined by the modified scene with the commands from the builder.
- [Commands](https://developer.apple.com/documentation/swiftui/commands) — Conforming types represent a group of related commands that can be exposed to the user via the main menu on macOS and key commands on iOS.
- [CommandMenu](https://developer.apple.com/documentation/swiftui/commandmenu) — Command menus are stand-alone, top-level containers for controls that perform related, app-specific commands.
- [CommandGroup](https://developer.apple.com/documentation/swiftui/commandgroup) — Groups of controls that you can add to existing command menus.
- [CommandsBuilder](https://developer.apple.com/documentation/swiftui/commandsbuilder) — Constructs command sets from multi-expression closures. Like `ContentBuilder`, it supports up to ten expressions in the closure body.
- [CommandGroupPlacement](https://developer.apple.com/documentation/swiftui/commandgroupplacement) — The standard locations that you can place new command groups relative to.

## Getting built-in command groups {#Getting-built-in-command-groups}

- [SidebarCommands](https://developer.apple.com/documentation/swiftui/sidebarcommands) — A built-in set of commands for manipulating window sidebars.
- [TextEditingCommands](https://developer.apple.com/documentation/swiftui/texteditingcommands) — A built-in group of commands for searching, editing, and transforming selections of text.
- [TextFormattingCommands](https://developer.apple.com/documentation/swiftui/textformattingcommands) — A built-in set of commands for transforming the styles applied to selections of text.
- [ToolbarCommands](https://developer.apple.com/documentation/swiftui/toolbarcommands) — A built-in set of commands for manipulating window toolbars.
- [ImportFromDevicesCommands](https://developer.apple.com/documentation/swiftui/importfromdevicescommands) — A built-in set of commands that enables importing content from nearby devices.
- [InspectorCommands](https://developer.apple.com/documentation/swiftui/inspectorcommands) — A built-in set of commands for manipulating inspectors.
- [EmptyCommands](https://developer.apple.com/documentation/swiftui/emptycommands) — An empty group of commands.

## Showing a menu indicator {#Showing-a-menu-indicator}

- [menuIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/menuindicator(_:)) — Sets the menu indicator visibility for controls within this view.
- [menuIndicatorVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/menuindicatorvisibility) — The menu indicator visibility to apply to controls within a view.

## Configuring menu dismissal {#Configuring-menu-dismissal}

- [menuActionDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/menuactiondismissbehavior(_:)) — Tells a menu whether to dismiss after performing an action.
- [MenuActionDismissBehavior](https://developer.apple.com/documentation/swiftui/menuactiondismissbehavior) — The set of menu dismissal behavior options.

## Setting a preferred order {#Setting-a-preferred-order}

- [menuOrder(_:)](https://developer.apple.com/documentation/swiftui/view/menuorder(_:)) — Sets the preferred order of items for menus presented from this view.
- [menuOrder](https://developer.apple.com/documentation/swiftui/environmentvalues/menuorder) — The preferred order of items for menus presented from this view.
- [MenuOrder](https://developer.apple.com/documentation/swiftui/menuorder) — The order in which a menu presents its content.

## Deprecated types {#Deprecated-types}

- [MenuButton](https://developer.apple.com/documentation/swiftui/menubutton) — A button that displays a menu containing a list of choices when pressed.
- [PullDownButton](https://developer.apple.com/documentation/swiftui/pulldownbutton)
- [ContextMenu](https://developer.apple.com/documentation/swiftui/contextmenu) — A container for views that you present as menu items in a context menu.
