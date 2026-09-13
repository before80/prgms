# Navigation

Enable people to move between different parts of your app’s view hierarchy within a scene.

## Overview {#Overview}

Use navigation containers to provide structure to your app’s user interface, enabling people to easily move among the parts of your app.

![](./images/navigation-hero@2x.png)

For example, people can move forward and backward through a stack of views using a [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack), or choose which view to display from a tab bar using a [TabView](https://developer.apple.com/documentation/swiftui/tabview).

Configure navigation containers by adding view modifiers like [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) to the container. Use other modifiers on the views inside the container to affect the container’s behavior when showing that view. For example, you can use [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:)) on a view to provide a toolbar title to display when showing that view.

## Essentials {#Essentials}

- [Understanding the navigation stack](6.1-UnderstandingTheNavigationStack/) — Learn about the navigation stack, links, and how to manage navigation types in your app’s structure.

## Presenting views in columns {#Presenting-views-in-columns}

- [Bringing robust navigation structure to your SwiftUI app](6.2-BringingRobustNavigationStructureToYourSwiftuiApp/) — Use navigation links, stacks, destinations, and paths to provide a streamlined experience for all platforms, as well as behaviors such as deep linking and state restoration.
- [Migrating to new navigation types](6.3-MigratingToNewNavigationTypes/) — Improve navigation behavior in your app by replacing navigation views with navigation stacks and navigation split views.
- [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview) — A view that presents views in two or three columns, where selections in leading columns control presentations in subsequent columns.
- [navigationSplitViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewstyle(_:)) — Sets the style for navigation split views within this view.
- [navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(_:)) — Sets a fixed, preferred width for the column containing this view.
- [navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/navigationsplitviewcolumnwidth(min:ideal:max:)) — Sets a flexible, preferred width for the column containing this view.
- [NavigationSplitViewVisibility](https://developer.apple.com/documentation/swiftui/navigationsplitviewvisibility) — The visibility of the leading columns in a navigation split view.
- [NavigationLink](https://developer.apple.com/documentation/swiftui/navigationlink) — A view that controls a navigation presentation.

## Stacking views in one column {#Stacking-views-in-one-column}

- [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack) — A view that displays a root view and enables you to present additional views over the root view.
- [NavigationPath](https://developer.apple.com/documentation/swiftui/navigationpath) — A type-erased list of data representing the content of a navigation stack.
- [navigationDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(for:destination:)) — Associates a destination view with a presented data type for use within a navigation stack.
- [navigationDestination(isPresented:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(ispresented:destination:)) — Associates a destination view with a binding that can be used to push the view onto a [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack).
- [navigationDestination(item:destination:)](https://developer.apple.com/documentation/swiftui/view/navigationdestination(item:destination:)) — Associates a destination view with a bound value for use within a navigation stack or navigation split view

## Managing column collapse {#Managing-column-collapse}

- [NavigationSplitViewColumn](https://developer.apple.com/documentation/swiftui/navigationsplitviewcolumn) — A view that represents a column in a navigation split view.

## Setting titles for navigation content {#Setting-titles-for-navigation-content}

- [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:)) — Configures the view’s title for purposes of navigation, using a localized string resource.
- [navigationSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationsubtitle(_:)) — Configures the view’s subtitle for purposes of navigation, using a localized string resource.
- [navigationDocument(_:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:)) — Configures the view’s document for purposes of navigation.
- [navigationDocument(_:preview:)](https://developer.apple.com/documentation/swiftui/view/navigationdocument(_:preview:)) — Configures the view’s document for purposes of navigation.

## Configuring the navigation bar {#Configuring-the-navigation-bar}

- [navigationBarBackButtonHidden(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbarbackbuttonhidden(_:)) — Hides the navigation bar back button for the view.
- [navigationBarTitleDisplayMode(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitledisplaymode(_:)) — Configures the title display mode for this view.
- [NavigationBarItem](https://developer.apple.com/documentation/swiftui/navigationbaritem) — A configuration for a navigation bar that represents a view at the top of a navigation stack.

## Configuring the sidebar {#Configuring-the-sidebar}

- [sidebarRowSize](https://developer.apple.com/documentation/swiftui/environmentvalues/sidebarrowsize) — The current size of sidebar rows.
- [SidebarRowSize](https://developer.apple.com/documentation/swiftui/sidebarrowsize) — The standard sizes of sidebar rows.

## Presenting views in tabs {#Presenting-views-in-tabs}

- [Enhancing your app’s content with tab navigation](6.5-EnhancingYourAppContentWithTabNavigation/) — Keep your app content front and center while providing quick access to navigation using the tab bar.
- [TabView](https://developer.apple.com/documentation/swiftui/tabview) — A view that switches between multiple child views using interactive user interface elements.
- [Tab](https://developer.apple.com/documentation/swiftui/tab) — The content for a tab and the tab’s associated tab item in a tab view.
- [TabRole](https://developer.apple.com/documentation/swiftui/tabrole) — A value that defines the purpose of the tab.
- [TabSection](https://developer.apple.com/documentation/swiftui/tabsection) — A container that you can use to add hierarchy within a tab view.
- [tabViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewstyle(_:)) — Sets the style for the tab view within the current environment.

## Configuring a tab bar {#Configuring-a-tab-bar}

- [defaultAdaptableTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaultadaptabletabbarplacement(_:)) — Specifies the default placement for the tabs in a tab view using the adaptable sidebar style.
- [defaultTabBarPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/defaulttabbarplacement(_:)) — Specifies the preferred placement for the tabs of a [TabView](https://developer.apple.com/documentation/swiftui/tabview) in the [sidebarAdaptable](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable) style on platforms where the tab bar cannot adapt between different representations, and only one representation can be shown.
- [tabViewSidebarHeader(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarheader(content:)) — Adds a custom header to the sidebar of a tab view.
- [tabViewSidebarFooter(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarfooter(content:)) — Adds a custom footer to the sidebar of a tab view.
- [tabViewSidebarBottomBar(content:)](https://developer.apple.com/documentation/swiftui/view/tabviewsidebarbottombar(content:)) — Adds a custom bottom bar to the sidebar of a tab view.
- [AdaptableTabBarPlacement](https://developer.apple.com/documentation/swiftui/adaptabletabbarplacement) — A placement for tabs in a tab view using the adaptable sidebar style.
- [tabBarPlacement](https://developer.apple.com/documentation/swiftui/environmentvalues/tabbarplacement) — The current placement of the tab bar.
- [TabBarPlacement](https://developer.apple.com/documentation/swiftui/tabbarplacement) — A placement for tabs in a tab view.
- [isTabBarShowingSections](https://developer.apple.com/documentation/swiftui/environmentvalues/istabbarshowingsections) — A Boolean value that determines whether a tab view shows the expanded contents of a tab section.
- [tabBarMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)) — Sets the behavior for tab bar minimization.
- [TabBarMinimizeBehavior](https://developer.apple.com/documentation/swiftui/tabbarminimizebehavior)
- [TabViewBottomAccessoryPlacement](https://developer.apple.com/documentation/swiftui/tabviewbottomaccessoryplacement) — A placement of the bottom accessory in a tab view. You can use this to adjust the content of the accessory view based on the placement.

## Configuring a tab {#Configuring-a-tab}

- [sectionActions(content:)](https://developer.apple.com/documentation/swiftui/view/sectionactions(content:)) — Adds custom actions to a section.
- [TabPlacement](https://developer.apple.com/documentation/swiftui/tabplacement) — A place that a tab can appear.
- [TabContentBuilder](https://developer.apple.com/documentation/swiftui/tabcontentbuilder) — A result builder that constructs tabs for a tab view that supports programmatic selection. This builder requires that all tabs in the tab view have the same selection type.
- [TabContent](https://developer.apple.com/documentation/swiftui/tabcontent) — A type that provides content for programmatically selectable tabs in a tab view.
- [AnyTabContent](https://developer.apple.com/documentation/swiftui/anytabcontent) — Type erased tab content.

## Enabling tab customization {#Enabling-tab-customization}

- [tabViewCustomization(_:)](https://developer.apple.com/documentation/swiftui/view/tabviewcustomization(_:)) — Specifies the customizations to apply to the sidebar representation of the tab view.
- [TabViewCustomization](https://developer.apple.com/documentation/swiftui/tabviewcustomization) — The customizations a person makes to an adaptable sidebar tab view.
- [TabCustomizationBehavior](https://developer.apple.com/documentation/swiftui/tabcustomizationbehavior) — The customization behavior of customizable tab view content.

## Displaying views in multiple panes {#Displaying-views-in-multiple-panes}

- [HSplitView](https://developer.apple.com/documentation/swiftui/hsplitview) — A layout container that arranges its children in a horizontal line and allows the user to resize them using dividers placed between them.
- [VSplitView](https://developer.apple.com/documentation/swiftui/vsplitview) — A layout container that arranges its children in a vertical line and allows the user to resize them using dividers placed between them.

## Deprecated Types {#Deprecated-Types}

- [NavigationView](https://developer.apple.com/documentation/swiftui/navigationview) — A view for presenting a stack of views that represents a visible path in a navigation hierarchy.
- [tabItem(_:)](https://developer.apple.com/documentation/swiftui/view/tabitem(_:)) — Sets the tab bar item associated with this view.
