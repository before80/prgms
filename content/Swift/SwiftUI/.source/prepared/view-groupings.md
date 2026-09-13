# View groupings

Present views in different kinds of purpose-driven containers, like forms or control groups.

## Overview {#Overview}

You can create groups of views that serve different purposes.

![](./images/view-groupings-hero@2x.png)

For example, a [Group](https://developer.apple.com/documentation/swiftui/group) construct treats the specified views as a unit without imposing any additional layout or appearance characteristics. A [Form](https://developer.apple.com/documentation/swiftui/form) presents a group of elements with a platform-specific appearance that’s suitable for gathering input from people.

For design guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) in the Human Interface Guidelines.

## Grouping views into a container {#Grouping-views-into-a-container}

- [Creating custom container views](6.1-CreatingCustomContainerViews/) — Access individual subviews to compose flexible container views.
- [Group](https://developer.apple.com/documentation/swiftui/group) — A type that collects multiple instances of a content type — like views, scenes, or commands — into a single unit.
- [GroupElementsOfContent](https://developer.apple.com/documentation/swiftui/groupelementsofcontent) — Transforms the subviews of a given view into a resulting content view.
- [GroupSectionsOfContent](https://developer.apple.com/documentation/swiftui/groupsectionsofcontent) — Transforms the sections of a given view into a resulting content view.

## Organizing views into sections {#Organizing-views-into-sections}

- [Section](https://developer.apple.com/documentation/swiftui/section) — A container view that you can use to add hierarchy within certain views.
- [SectionCollection](https://developer.apple.com/documentation/swiftui/sectioncollection) — An opaque collection representing the sections of view.
- [SectionConfiguration](https://developer.apple.com/documentation/swiftui/sectionconfiguration) — Specifies the contents of a section.

## Iterating over dynamic data {#Iterating-over-dynamic-data}

- [ForEach](https://developer.apple.com/documentation/swiftui/foreach) — A structure that computes views on demand from an underlying collection of identified data.
- [ForEachSectionCollection](https://developer.apple.com/documentation/swiftui/foreachsectioncollection) — A collection which allows a view to be treated as a collection of its sections in a for each loop.
- [ForEachSubviewCollection](https://developer.apple.com/documentation/swiftui/foreachsubviewcollection) — A collection which allows a view to be treated as a collection of its subviews in a for each loop.
- [DynamicViewContent](https://developer.apple.com/documentation/swiftui/dynamicviewcontent) — A type of view that generates views from an underlying collection of data.

## Accessing a container’s subviews {#Accessing-a-containers-subviews}

- [Subview](https://developer.apple.com/documentation/swiftui/subview) — An opaque value representing a subview of another view.
- [SubviewsCollection](https://developer.apple.com/documentation/swiftui/subviewscollection) — An opaque collection representing the subviews of view.
- [SubviewsCollectionSlice](https://developer.apple.com/documentation/swiftui/subviewscollectionslice) — A slice of a SubviewsCollection.
- [containerValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/containervalue(_:_:)) — Sets a particular container value of a view.
- [ContainerValues](https://developer.apple.com/documentation/swiftui/containervalues) — A collection of container values associated with a given view.
- [ContainerValueKey](https://developer.apple.com/documentation/swiftui/containervaluekey) — A key for accessing container values.

## Grouping views into a box {#Grouping-views-into-a-box}

- [GroupBox](https://developer.apple.com/documentation/swiftui/groupbox) — A stylized view, with an optional label, that visually collects a logical grouping of content.
- [groupBoxStyle(_:)](https://developer.apple.com/documentation/swiftui/view/groupboxstyle(_:)) — Sets the style for group boxes within this view.

## Grouping inputs {#Grouping-inputs}

- [Form](https://developer.apple.com/documentation/swiftui/form) — A container for grouping controls used for data entry, such as in settings or inspectors.
- [formStyle(_:)](https://developer.apple.com/documentation/swiftui/view/formstyle(_:)) — Sets the style for forms in a view hierarchy.
- [LabeledContent](https://developer.apple.com/documentation/swiftui/labeledcontent) — A container for attaching a label to a value-bearing view.
- [labeledContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labeledcontentstyle(_:)) — Sets a style for labeled content.

## Presenting a group of controls {#Presenting-a-group-of-controls}

- [ControlGroup](https://developer.apple.com/documentation/swiftui/controlgroup) — A container view that displays semantically-related controls in a visually-appropriate manner for the context
- [controlGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/controlgroupstyle(_:)) — Sets the style for control groups within this view.
