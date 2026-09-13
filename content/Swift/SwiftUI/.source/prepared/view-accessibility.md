# Accessibility modifiers

Make your SwiftUI apps accessible to everyone, including people with disabilities.

## Overview {#Overview}

Like all Apple UI frameworks, SwiftUI comes with built-in accessibility support. The framework introspects common elements like navigation views, lists, text fields, sliders, buttons, and so on, and provides basic accessibility labels and values by default. You don’t have to do any extra work to enable these standard accessibility features.

SwiftUI also provides tools to help you enhance the accessibility of your app. For example, you can explicitly add accessibility labels to elements in your UI using the [accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)) or the [accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)) view modifier.

To learn more about adding accessibility features to your app, see [Accessibility fundamentals](../../../accessibility/1-AccessibilityFundamentals/).

## Labels {#Labels}

- [accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)) — Adds a label to the view that describes its contents.
- [accessibilityLabel(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:isenabled:)) — Adds a label to the view that describes its contents.
- [accessibilityLabel(content:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(content:)) — Adds a label to the view that describes its contents.
- [accessibilityInputLabels(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:)) — Sets alternate input labels with which users identify a view.
- [accessibilityInputLabels(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:isenabled:)) — Sets alternate input labels with which users identify a view.
- [accessibilityLabeledPair(role:id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabeledpair(role:id:in:)) — Pairs an accessibility element representing a label with the element for the matching content.

## Values {#Values}

- [accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)) — Adds a textual description of the value that the view contains.
- [accessibilityValue(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:isenabled:)) — Adds a textual description of the value that the view contains.

## Hints {#Hints}

- [accessibilityHint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)) — Communicates to the user what happens after performing the view’s action.
- [accessibilityHint(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:isenabled:)) — Communicates to the user what happens after performing the view’s action.

## Actions {#Actions}

- [accessibilityAction(_:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(_:_:)) — Adds an accessibility action to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action.
- [accessibilityActions(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityactions(_:)) — Adds multiple accessibility actions to the view.
- [accessibilityActions(category:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityactions(category:_:)) — Adds multiple accessibility actions to the view with a specific category. Actions allow assistive technologies, such as VoiceOver, to interact with the view by invoking the action and are grouped by their category. When multiple action modifiers with an equal category are applied to the view, the actions are combined together.
- [accessibilityAction(named:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)) — Adds an accessibility action to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action.
- [accessibilityAction(action:label:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(action:label:)) — Adds an accessibility action to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action.
- [accessibilityAction(intent:label:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(intent:label:)) — Adds an accessibility action labeled by the contents of `label` to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action. When the action is performed, the `intent` will be invoked.
- [accessibilityAction(_:intent:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(_:intent:)) — Adds an accessibility action representing `actionKind` to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action. When the action is performed, the `intent` will be invoked.
- [accessibilityAction(named:intent:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:intent:)) — Adds an accessibility action labeled `name` to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action. When the action is performed, the `intent` will be invoked.
- [accessibilityAdjustableAction(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityadjustableaction(_:)) — Adds an accessibility adjustable action to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action.
- [accessibilityScrollAction(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityscrollaction(_:)) — Adds an accessibility scroll action to the view. Actions allow assistive technologies, such as the VoiceOver, to interact with the view by invoking the action.
- [accessibilityScrollStatus(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityscrollstatus(_:isenabled:)) — Changes the announcement provided by accessibility technologies when a user scrolls a scroll view within this view.

## Gestures {#Gestures}

- [accessibilityActivationPoint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityactivationpoint(_:)) — The activation point for an element is the location assistive technologies use to initiate gestures.
- [accessibilityActivationPoint(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityactivationpoint(_:isenabled:)) — The activation point for an element is the location assistive technologies use to initiate gestures.
- [accessibilityDragPoint(_:description:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydragpoint(_:description:)) — The point an assistive technology should use to begin a drag interaction.
- [accessibilityDragPoint(_:description:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydragpoint(_:description:isenabled:)) — The point an assistive technology should use to begin a drag interaction.
- [accessibilityDropPoint(_:description:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydroppoint(_:description:)) — The point an assistive technology should use to end a drag interaction.
- [accessibilityDropPoint(_:description:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydroppoint(_:description:isenabled:)) — The point an assistive technology should use to end a drag interaction.
- [accessibilityDirectTouch(_:options:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydirecttouch(_:options:)) — Explicitly set whether this accessibility element is a direct touch area. Direct touch areas passthrough touch events to the app rather than being handled through an assistive technology, such as VoiceOver. The modifier accepts an optional `AccessibilityDirectTouchOptions` option set to customize the functionality of the direct touch area.
- [accessibilityZoomAction(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityzoomaction(_:)) — Adds an accessibility zoom action to the view. Actions allow assistive technologies, such as VoiceOver, to interact with the view by invoking the action.

## Elements {#Elements}

- [accessibilityElement(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:)) — Creates a new accessibility element, or modifies the [AccessibilityChildBehavior](https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior) of the existing accessibility element.
- [accessibilityChildren(children:)](https://developer.apple.com/documentation/swiftui/view/accessibilitychildren(children:)) — Replaces the existing accessibility element’s children with one or more new synthetic accessibility elements.
- [accessibilityHidden(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:)) — Specifies whether to hide this view from system accessibility features.
- [accessibilityHidden(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:isenabled:)) — Specifies whether to hide this view from system accessibility features.

## Custom controls {#Custom-controls}

- [accessibilityRepresentation(representation:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:)) — Replaces one or more accessibility elements for this view with new accessibility elements.
- [accessibilityRespondsToUserInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrespondstouserinteraction(_:)) — Explicitly set whether this Accessibility element responds to user interaction and would thus be interacted with by technologies such as Switch Control, Voice Control or Full Keyboard Access.
- [accessibilityRespondsToUserInteraction(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrespondstouserinteraction(_:isenabled:)) — Explicitly set whether this Accessibility element responds to user interaction and would thus be interacted with by technologies such as Switch Control, Voice Control or Full Keyboard Access.

## Custom content {#Custom-content}

- [accessibilityCustomContent(_:_:importance:)](https://developer.apple.com/documentation/swiftui/view/accessibilitycustomcontent(_:_:importance:)) — Add additional accessibility information to the view.

## Working with rotors {#Working-with-rotors}

- [accessibilityRotor(_:entries:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:)) — Create an Accessibility Rotor with the specified user-visible label, and entries generated from the content closure.
- [accessibilityRotor(_:entries:entryID:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entryid:entrylabel:)) — Create an Accessibility Rotor with the specified user-visible label and entries.
- [accessibilityRotor(_:entries:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entrylabel:)) — Create an Accessibility Rotor with the specified user-visible label and entries.
- [accessibilityRotor(_:textRanges:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:textranges:)) — Create an Accessibility Rotor with the specified user-visible label and entries for each of the specified ranges. The Rotor will be attached to the current Accessibility element, and each entry will go the specified range of that element.

## Configuring rotors {#Configuring-rotors}

- [accessibilityRotorEntry(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotorentry(id:in:)) — Defines an explicit identifier tying an Accessibility element for this view to an entry in an Accessibility Rotor.
- [accessibilityLinkedGroup(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylinkedgroup(id:in:)) — Links multiple accessibility elements so that the user can quickly navigate from one element to another, even when the elements are not near each other in the accessibility hierarchy.
- [accessibilitySortPriority(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)) — Sets the sort priority order for this view’s accessibility element, relative to other elements at the same level.

## Focus {#Focus}

- [accessibilityFocused(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityfocused(_:)) — Modifies this view by binding its accessibility element’s focus state to the given boolean state value.
- [accessibilityFocused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/accessibilityfocused(_:equals:)) — Modifies this view by binding its accessibility element’s focus state to the given state value.
- [accessibilityDefaultFocus(_:_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitydefaultfocus(_:_:)) — Defines a region in which default accessibility focus is evaluated by assigning a value to a given accessibility focus state binding.

## Traits {#Traits}

- [accessibilityAddTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)) — Adds the given traits to the view.
- [accessibilityRemoveTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityremovetraits(_:)) — Removes the given traits from this view.

## Identity {#Identity}

- [accessibilityIdentifier(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:)) — Uses the string you specify to identify the view.
- [accessibilityIdentifier(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:isenabled:)) — Uses the string you specify to identify the view.

## Color inversion {#Color-inversion}

- [accessibilityIgnoresInvertColors(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityignoresinvertcolors(_:)) — Sets whether this view should ignore the system Smart Invert setting.

## Content descriptions {#Content-descriptions}

- [accessibilityTextContentType(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitytextcontenttype(_:)) — Sets an accessibility text content type.
- [accessibilityHeading(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityheading(_:)) — Sets the accessibility level of this heading.

## VoiceOver {#VoiceOver}

- [speechAdjustedPitch(_:)](https://developer.apple.com/documentation/swiftui/view/speechadjustedpitch(_:)) — Raises or lowers the pitch of spoken text.
- [speechAlwaysIncludesPunctuation(_:)](https://developer.apple.com/documentation/swiftui/view/speechalwaysincludespunctuation(_:)) — Sets whether VoiceOver should always speak all punctuation in the text view.
- [speechAnnouncementsQueued(_:)](https://developer.apple.com/documentation/swiftui/view/speechannouncementsqueued(_:)) — Controls whether to queue pending announcements behind existing speech rather than interrupting speech in progress.
- [speechSpellsOutCharacters(_:)](https://developer.apple.com/documentation/swiftui/view/speechspellsoutcharacters(_:)) — Sets whether VoiceOver should speak the contents of the text view character by character.

## Charts {#Charts}

- [accessibilityChartDescriptor(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitychartdescriptor(_:)) — Adds a descriptor to a View that represents a chart to make the chart’s contents accessible to all users.

## Large content {#Large-content}

- [accessibilityShowsLargeContentViewer()](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer()) — Adds a default large content view to be shown by the large content viewer.
- [accessibilityShowsLargeContentViewer(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer(_:)) — Adds a custom large content view to be shown by the large content viewer.

## Quick actions {#Quick-actions}

- [accessibilityQuickAction(style:content:)](https://developer.apple.com/documentation/swiftui/view/accessibilityquickaction(style:content:)) — Adds a quick action to be shown by the system when active.
- [accessibilityQuickAction(style:isActive:content:)](https://developer.apple.com/documentation/swiftui/view/accessibilityquickaction(style:isactive:content:)) — Adds a quick action to be shown by the system when active.

## Using assistive access {#Using-assistive-access}

- [assistiveAccessNavigationIcon(_:)](https://developer.apple.com/documentation/swiftui/view/assistiveaccessnavigationicon(_:)) — Configures the view’s icon for purposes of navigation.
- [assistiveAccessNavigationIcon(systemImage:)](https://developer.apple.com/documentation/swiftui/view/assistiveaccessnavigationicon(systemimage:)) — Configures the view’s icon for purposes of navigation.
