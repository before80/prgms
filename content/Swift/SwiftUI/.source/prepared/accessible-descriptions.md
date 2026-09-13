# Accessible descriptions

Describe interface elements to help people understand what they represent.

## Overview {#Overview}

SwiftUI can often infer some information about your user interface elements, but you can use accessibility modifiers to provide even more information for users that need it.

![](./images/accessible-descriptions-hero@2x.png)

For design guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) in the Accessibility section of the Human Interface Guidelines.

## Applying labels {#Applying-labels}

- [accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)) — Adds a label to the view that describes its contents.
- [accessibilityLabel(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:isenabled:)) — Adds a label to the view that describes its contents.
- [accessibilityLabel(content:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(content:)) — Adds a label to the view that describes its contents.
- [accessibilityInputLabels(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:)) — Sets alternate input labels with which users identify a view.
- [accessibilityInputLabels(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:isenabled:)) — Sets alternate input labels with which users identify a view.
- [accessibilityLabeledPair(role:id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabeledpair(role:id:in:)) — Pairs an accessibility element representing a label with the element for the matching content.
- [AccessibilityLabeledPairRole](https://developer.apple.com/documentation/swiftui/accessibilitylabeledpairrole) — The role of an accessibility element in a label / content pair.

## Describing values {#Describing-values}

- [accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)) — Adds a textual description of the value that the view contains.
- [accessibilityValue(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:isenabled:)) — Adds a textual description of the value that the view contains.

## Describing content {#Describing-content}

- [accessibilityTextContentType(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitytextcontenttype(_:)) — Sets an accessibility text content type.
- [accessibilityHeading(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityheading(_:)) — Sets the accessibility level of this heading.
- [AccessibilityHeadingLevel](https://developer.apple.com/documentation/swiftui/accessibilityheadinglevel) — The hierarchy of a heading in relation to other headings.
- [AccessibilityTextContentType](https://developer.apple.com/documentation/swiftui/accessibilitytextcontenttype) — Textual context that assistive technologies can use to improve the presentation of spoken text.

## Describing charts {#Describing-charts}

- [accessibilityChartDescriptor(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitychartdescriptor(_:)) — Adds a descriptor to a View that represents a chart to make the chart’s contents accessible to all users.
- [AXChartDescriptorRepresentable](https://developer.apple.com/documentation/swiftui/axchartdescriptorrepresentable) — A type to generate an `AXChartDescriptor` object that you use to provide information about a chart and its data for an accessible experience in VoiceOver or other assistive technologies.

## Adding custom descriptions {#Adding-custom-descriptions}

- [accessibilityCustomContent(_:_:importance:)](https://developer.apple.com/documentation/swiftui/view/accessibilitycustomcontent(_:_:importance:)) — Add additional accessibility information to the view.
- [AccessibilityCustomContentKey](https://developer.apple.com/documentation/swiftui/accessibilitycustomcontentkey) — Key used to specify the identifier and label associated with an entry of additional accessibility information.

## Assigning traits to content {#Assigning-traits-to-content}

- [accessibilityAddTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)) — Adds the given traits to the view.
- [accessibilityRemoveTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityremovetraits(_:)) — Removes the given traits from this view.
- [AccessibilityTraits](https://developer.apple.com/documentation/swiftui/accessibilitytraits) — A set of accessibility traits that describe how an element behaves.

## Offering hints {#Offering-hints}

- [accessibilityHint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)) — Communicates to the user what happens after performing the view’s action.
- [accessibilityHint(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:isenabled:)) — Communicates to the user what happens after performing the view’s action.

## Configuring VoiceOver {#Configuring-VoiceOver}

- [speechAdjustedPitch(_:)](https://developer.apple.com/documentation/swiftui/view/speechadjustedpitch(_:)) — Raises or lowers the pitch of spoken text.
- [speechAlwaysIncludesPunctuation(_:)](https://developer.apple.com/documentation/swiftui/view/speechalwaysincludespunctuation(_:)) — Sets whether VoiceOver should always speak all punctuation in the text view.
- [speechAnnouncementsQueued(_:)](https://developer.apple.com/documentation/swiftui/view/speechannouncementsqueued(_:)) — Controls whether to queue pending announcements behind existing speech rather than interrupting speech in progress.
- [speechSpellsOutCharacters(_:)](https://developer.apple.com/documentation/swiftui/view/speechspellsoutcharacters(_:)) — Sets whether VoiceOver should speak the contents of the text view character by character.
