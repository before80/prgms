# Toolbars

Provide immediate access to frequently used commands and controls.

## Overview {#Overview}

The system might present toolbars above or below your app’s content, depending on the platform and the context.

![](./images/toolbars-hero@2x.png)

Add items to a toolbar by applying the [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) view modifier to a view in your app. You can also configure the toolbar using view modifiers. For example, you can set the visibility of a toolbar with the [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) modifier.

For design guidance, see [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) in the Human Interface Guidelines.

## Populating a toolbar {#Populating-a-toolbar}

- [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) — Populates the toolbar or navigation bar with the specified items.
- [ToolbarItem](https://developer.apple.com/documentation/swiftui/toolbaritem) — A model that represents an item which can be placed in the toolbar or navigation bar.
- [ToolbarItemGroup](https://developer.apple.com/documentation/swiftui/toolbaritemgroup) — A model that represents a group of `ToolbarItem`s which can be placed in the toolbar or navigation bar.
- [ToolbarItemPlacement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement) — A structure that defines the placement of a toolbar item.
- [toolbarOverflowMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbaroverflowmenu(content:)) — Configures the overflow menu of a toolbar.
- [ToolbarOverflowMenu](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu) — The overflow menu of a toolbar.
- [ToolbarContent](https://developer.apple.com/documentation/swiftui/toolbarcontent) — Conforming types represent items that can be placed in various locations in a toolbar.
- [ToolbarContentBuilder](https://developer.apple.com/documentation/swiftui/toolbarcontentbuilder) — Constructs a toolbar item set from multi-expression closures.
- [ToolbarSpacer](https://developer.apple.com/documentation/swiftui/toolbarspacer) — A standard space item in toolbars.
- [DefaultToolbarItem](https://developer.apple.com/documentation/swiftui/defaulttoolbaritem) — A toolbar item that represents a system component.

## Populating a customizable toolbar {#Populating-a-customizable-toolbar}

- [toolbar(id:content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(id:content:)) — Populates the toolbar or navigation bar with the specified items, allowing for user customization.
- [toolbarItemHidden(_:)](https://developer.apple.com/documentation/swiftui/view/toolbaritemhidden(_:)) — Hides an individual view within a control group toolbar item.
- [CustomizableToolbarContent](https://developer.apple.com/documentation/swiftui/customizabletoolbarcontent) — Conforming types represent items that can be placed in various locations in a customizable toolbar.
- [ToolbarCustomizationBehavior](https://developer.apple.com/documentation/swiftui/toolbarcustomizationbehavior) — The customization behavior of customizable toolbar content.
- [ToolbarCustomizationOptions](https://developer.apple.com/documentation/swiftui/toolbarcustomizationoptions) — Options that influence the default customization behavior of customizable toolbar content.
- [SearchToolbarBehavior](https://developer.apple.com/documentation/swiftui/searchtoolbarbehavior) — The behavior of a search field in a toolbar.

## Removing default items {#Removing-default-items}

- [toolbar(removing:)](https://developer.apple.com/documentation/swiftui/view/toolbar(removing:)) — Remove a toolbar item present by default
- [ToolbarDefaultItemKind](https://developer.apple.com/documentation/swiftui/toolbardefaultitemkind) — A kind of toolbar item a `View` adds by default.

## Setting toolbar visibility {#Setting-toolbar-visibility}

- [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) — Specifies the visibility of a bar managed by SwiftUI.
- [toolbarVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarvisibility(_:for:)) — Specifies the visibility of a bar managed by SwiftUI.
- [toolbarBackgroundVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackgroundvisibility(_:for:)) — Specifies the preferred visibility of backgrounds on a bar managed by SwiftUI.
- [ToolbarPlacement](https://developer.apple.com/documentation/swiftui/toolbarplacement) — The placement of a toolbar.
- [ContentToolbarPlacement](https://developer.apple.com/documentation/swiftui/contenttoolbarplacement)

## Specifying the role of toolbar content {#Specifying-the-role-of-toolbar-content}

- [toolbarRole(_:)](https://developer.apple.com/documentation/swiftui/view/toolbarrole(_:)) — Configures the semantic role for the content populating the toolbar.
- [ToolbarRole](https://developer.apple.com/documentation/swiftui/toolbarrole) — The purpose of content that populates the toolbar.

## Styling a toolbar {#Styling-a-toolbar}

- [toolbarBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackground(_:for:)) — Specifies the preferred shape style of the background of a bar managed by SwiftUI.
- [toolbarColorScheme(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarcolorscheme(_:for:)) — Specifies the preferred color scheme of a bar managed by SwiftUI.
- [toolbarForegroundStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarforegroundstyle(_:for:)) — Specifies the preferred foreground style of bars managed by SwiftUI.
- [windowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarstyle(_:)) — Sets the style for the toolbar defined within this scene.
- [WindowToolbarStyle](https://developer.apple.com/documentation/swiftui/windowtoolbarstyle) — A specification for the appearance and behavior of a window’s toolbar.
- [toolbarLabelStyle](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarlabelstyle) — The label style to apply to controls within a toolbar.
- [ToolbarLabelStyle](https://developer.apple.com/documentation/swiftui/toolbarlabelstyle) — The label style of a toolbar.
- [SpacerSizing](https://developer.apple.com/documentation/swiftui/spacersizing) — A type which defines how spacers should size themselves.

## Configuring the toolbar title display mode {#Configuring-the-toolbar-title-display-mode}

- [toolbarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/toolbartitledisplaymode(_:)) — Configures the toolbar title display mode for this view.
- [ToolbarTitleDisplayMode](https://developer.apple.com/documentation/swiftui/toolbartitledisplaymode) — A type that defines the behavior of title of a toolbar.

## Setting the toolbar title menu {#Setting-the-toolbar-title-menu}

- [toolbarTitleMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbartitlemenu(content:)) — Configure the title menu of a toolbar.
- [ToolbarTitleMenu](https://developer.apple.com/documentation/swiftui/toolbartitlemenu) — The title menu of a toolbar.

## Creating an ornament {#Creating-an-ornament}

- [ornament(visibility:attachmentAnchor:contentAlignment:ornament:)](https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)) — Presents an ornament.
- [OrnamentAttachmentAnchor](https://developer.apple.com/documentation/swiftui/ornamentattachmentanchor) — An attachment anchor for an ornament.

## Controlling item visibility {#Controlling-item-visibility}

- [visibilityPriority(_:)](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)) — Defines the visibility priority for a toolbar item.
- [ToolbarItemVisibilityPriority](https://developer.apple.com/documentation/swiftui/toolbaritemvisibilitypriority) — A value that defines the visibility priority of a toolbar item.

## Minimizing a toolbar {#Minimizing-a-toolbar}

- [toolbarMinimizationBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:)) — Sets the minimize behavior for the specified bars.
- [ToolbarMinimizationBehavior](https://developer.apple.com/documentation/swiftui/toolbarminimizationbehavior) — The minimization behavior of a toolbar.
- [toolbarMinimizationRestoration(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationrestoration(_:for:)) — Sets the restoration behavior for the specified bars during minimization.
- [ToolbarMinimizationRestoration](https://developer.apple.com/documentation/swiftui/toolbarminimizationrestoration) — The restoration behavior during toolbar minimization.
- [toolbarMinimizationSafeAreaAdjustment(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationsafeareaadjustment(_:for:)) — Sets the safe area adjustment for the specified bars during minimization.
- [ToolbarMinimizationSafeAreaAdjustment](https://developer.apple.com/documentation/swiftui/toolbarminimizationsafeareaadjustment) — The safe area adjustment during toolbar minimization.
