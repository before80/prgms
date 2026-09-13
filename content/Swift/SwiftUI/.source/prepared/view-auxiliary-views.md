# Auxiliary view modifiers

Add and configure supporting views, like toolbars and context menus.

## Overview {#Overview}

Use these modifiers to manage supplemental views that present context-specific controls and information. For example, you can add titles and buttons to navigation bars, manage the status bar, create context menus, and add badges to many different kinds of views.

## Navigation titles {#Navigation-titles}

- [Configure your apps navigation titles](1.7.1-ConfigureYourAppsNavigationTitles/) — Use a navigation title to display the current navigation state of an interface.
- [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:)) — Configures the view’s title for purposes of navigation, using a localized string resource.
- [navigationSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsubtitle(_:)) — Configures the view’s subtitle for purposes of navigation, using a localized string resource.

## Navigation title configuration {#Navigation-title-configuration}

- [navigationDocument(_:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:)) — Configures the view’s document for purposes of navigation.
- [navigationDocument(_:preview:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:preview:)) — Configures the view’s document for purposes of navigation.

## Navigation bars {#Navigation-bars}

- [navigationBarBackButtonHidden(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbarbackbuttonhidden(_:)) — Hides the navigation bar back button for the view.
- [navigationBarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitledisplaymode(_:)) — Configures the title display mode for this view.

## Navigation stacks and columns {#Navigation-stacks-and-columns}

- [navigationDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(for:destination:)) — Associates a destination view with a presented data type for use within a navigation stack.
- [navigationDestination(isPresented:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(ispresented:destination:)) — Associates a destination view with a binding that can be used to push the view onto a [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack).
- [navigationDestination(item:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(item:destination:)) — Associates a destination view with a bound value for use within a navigation stack or navigation split view
- [navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(_:)) — Sets a fixed, preferred width for the column containing this view.
- [navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(min:ideal:max:)) — Sets a flexible, preferred width for the column containing this view.
- [navigationLinkIndicatorVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/navigationlinkindicatorvisibility(_:)) — Configures whether navigation links show a disclosure indicator.
- [navigationTransition(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtransition(_:)) — Sets the navigation transition style for this view.

## Scroll view edges {#Scroll-view-edges}

- [scrollEdgeEffectStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffectstyle(_:for:)) — Configures the scroll edge effect style for scroll views within this hierarchy.
- [scrollEdgeEffectHidden(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrolledgeeffecthidden(_:for:)) — Hides any scroll edge effects for scroll views within this hierarchy.

## Tab views {#Tab-views}

- [defaultAdaptableTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaultadaptabletabbarplacement(_:)) — Specifies the default placement for the tabs in a tab view using the adaptable sidebar style.
- [defaultTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaulttabbarplacement(_:)) — Specifies the preferred placement for the tabs of a [TabView](https://developer.apple.com/documentation/swiftui/tabview) in the [sidebarAdaptable](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable) style on platforms where the tab bar cannot adapt between different representations, and only one representation can be shown.
- [sectionActions(content:)](https://developer.apple.com/documentation/swiftui/view/sectionactions(content:)) — Adds custom actions to a section.
- [tabBarMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)) — Sets the behavior for tab bar minimization.
- [tabViewBottomAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(content:)) — Places a view as the bottom accessory of the tab view.
- [tabViewBottomAccessory(isEnabled:content:)](https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(isenabled:content:)) — Places a view as the bottom accessory of the tab view. Use this modifier to dynamically show and hide the accessory view.
- [tabViewCustomization(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewcustomization(_:)) — Specifies the customizations to apply to the sidebar representation of the tab view.
- [tabViewSearchActivation(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewsearchactivation(_:)) — Configures the activation and deactivation behavior of search in the search tab.
- [tabViewSidebarHeader(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarheader(content:)) — Adds a custom header to the sidebar of a tab view.
- [tabViewSidebarFooter(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarfooter(content:)) — Adds a custom footer to the sidebar of a tab view.
- [tabViewSidebarBottomBar(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarbottombar(content:)) — Adds a custom bottom bar to the sidebar of a tab view.

## Toolbars {#Toolbars}

- [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) — Populates the toolbar or navigation bar with the specified items.
- [toolbar(id:content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(id:content:)) — Populates the toolbar or navigation bar with the specified items, allowing for user customization.
- [toolbar(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:)) — Specifies the visibility of a bar managed by SwiftUI.
- [contentToolbar(for:content:)](https://developer.apple.com/documentation/swiftui/view/contenttoolbar(for:content:)) — Populates the toolbar of the specified content view type with the views you provide.
- [toolbar(removing:)](https://developer.apple.com/documentation/swiftui/view/toolbar(removing:)) — Remove a toolbar item present by default
- [toolbarVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarvisibility(_:for:)) — Specifies the visibility of a bar managed by SwiftUI.
- [toolbarBackground(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackground(_:for:)) — Specifies the preferred shape style of the background of a bar managed by SwiftUI.
- [toolbarBackgroundVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarbackgroundvisibility(_:for:)) — Specifies the preferred visibility of backgrounds on a bar managed by SwiftUI.
- [toolbarItemHidden(_:)](https://developer.apple.com/documentation/swiftui/view/toolbaritemhidden(_:)) — Hides an individual view within a control group toolbar item.
- [toolbarForegroundStyle(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarforegroundstyle(_:for:)) — Specifies the preferred foreground style of bars managed by SwiftUI.
- [toolbarColorScheme(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarcolorscheme(_:for:)) — Specifies the preferred color scheme of a bar managed by SwiftUI.
- [toolbarOverflowMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbaroverflowmenu(content:)) — Configures the overflow menu of a toolbar.
- [toolbarRole(_:)](https://developer.apple.com/documentation/swiftui/view/toolbarrole(_:)) — Configures the semantic role for the content populating the toolbar.
- [toolbarMinimizationBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:)) — Sets the minimize behavior for the specified bars.
- [toolbarMinimizationRestoration(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationrestoration(_:for:)) — Sets the restoration behavior for the specified bars during minimization.
- [toolbarMinimizationSafeAreaAdjustment(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationsafeareaadjustment(_:for:)) — Sets the safe area adjustment for the specified bars during minimization.
- [toolbarTitleMenu(content:)](https://developer.apple.com/documentation/swiftui/view/toolbartitlemenu(content:)) — Configure the title menu of a toolbar.
- [toolbarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/toolbartitledisplaymode(_:)) — Configures the toolbar title display mode for this view.
- [ornament(visibility:attachmentAnchor:contentAlignment:ornament:)](https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)) — Presents an ornament.

## Context menus {#Context-menus}

- [contextMenu(menuItems:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:)) — Adds a context menu to a view.
- [contextMenu(menuItems:preview:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(menuitems:preview:)) — Adds a context menu with a custom preview to a view.
- [contextMenu(forSelectionType:menu:primaryAction:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(forselectiontype:menu:primaryaction:)) — Adds an item-based context menu to a view.

## Badges {#Badges}

- [badge(_:)](https://developer.apple.com/documentation/swiftui/view/badge(_:)) — Generates a badge for the view from a localized string resource.
- [badgeProminence(_:)](https://developer.apple.com/documentation/swiftui/view/badgeprominence(_:)) — Specifies the prominence of badges created by this view.

## Lists {#Lists}

- [sectionIndexLabel(_:)](https://developer.apple.com/documentation/swiftui/view/sectionindexlabel(_:)) — Sets the label that is used in a section index to point to this section, typically only a single character long.

## Help text {#Help-text}

- [help(_:)](https://developer.apple.com/documentation/swiftui/view/help(_:)) — Adds help text to a view using a localized string resource that you provide.

## Status bar {#Status-bar}

- [statusBarHidden(_:)](https://developer.apple.com/documentation/swiftui/view/statusbarhidden(_:)) — Sets the visibility of the status bar.

## External displays {#External-displays}

- [sceneAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/sceneaccessory(content:)) — Defines any scene accessories associated with `self`.

## Touch Bar {#Touch-Bar}

- [touchBar(content:)](https://developer.apple.com/documentation/swiftui/view/touchbar(content:)) — Sets the content that the Touch Bar displays.
- [touchBar(_:)](https://developer.apple.com/documentation/swiftui/view/touchbar(_:)) — Sets the Touch Bar content to be shown in the Touch Bar when applicable.
- [touchBarItemPrincipal(_:)](https://developer.apple.com/documentation/swiftui/view/touchbaritemprincipal(_:)) — Sets principal views that have special significance to this Touch Bar.
- [touchBarCustomizationLabel(_:)](https://developer.apple.com/documentation/swiftui/view/touchbarcustomizationlabel(_:)) — Sets a user-visible string that identifies the view’s functionality.
- [touchBarItemPresence(_:)](https://developer.apple.com/documentation/swiftui/view/touchbaritempresence(_:)) — Sets the behavior of the user-customized view.
