# Deprecated modifiers

Review unsupported modifiers and their replacements.

## Overview {#Overview}

Avoid using deprecated modifiers in your app. Select a modifier to see the replacement that you should use instead.

## Accessibility modifiers {#Accessibility-modifiers}

- [accessibility(label:)](https://developer.apple.com/documentation/swiftui/view/accessibility(label:)) — Adds a label to the view that describes its contents.
- [accessibility(value:)](https://developer.apple.com/documentation/swiftui/view/accessibility(value:)) — Adds a textual description of the value that the view contains.
- [accessibility(hidden:)](https://developer.apple.com/documentation/swiftui/view/accessibility(hidden:)) — Specifies whether to hide this view from system accessibility features.
- [accessibility(identifier:)](https://developer.apple.com/documentation/swiftui/view/accessibility(identifier:)) — Uses the specified string to identify the view.
- [accessibility(selectionIdentifier:)](https://developer.apple.com/documentation/swiftui/view/accessibility(selectionidentifier:)) — Sets a selection identifier for this view’s accessibility element.
- [accessibility(hint:)](https://developer.apple.com/documentation/swiftui/view/accessibility(hint:)) — Communicates to the user what happens after performing the view’s action.
- [accessibility(activationPoint:)](https://developer.apple.com/documentation/swiftui/view/accessibility(activationpoint:)) — Specifies the point where activations occur in the view.
- [accessibility(inputLabels:)](https://developer.apple.com/documentation/swiftui/view/accessibility(inputlabels:)) — Sets alternate input labels with which users identify a view.
- [accessibility(addTraits:)](https://developer.apple.com/documentation/swiftui/view/accessibility(addtraits:)) — Adds the given traits to the view.
- [accessibility(removeTraits:)](https://developer.apple.com/documentation/swiftui/view/accessibility(removetraits:)) — Removes the given traits from this view.
- [accessibility(sortPriority:)](https://developer.apple.com/documentation/swiftui/view/accessibility(sortpriority:)) — Sets the sort priority order for this view’s accessibility element, relative to other elements at the same level.

## Appearance modifiers {#Appearance-modifiers}

- [colorScheme(_:)](https://developer.apple.com/documentation/swiftui/view/colorscheme(_:)) — Sets this view’s color scheme.
- [listRowPlatterColor(_:)](https://developer.apple.com/documentation/swiftui/view/listrowplattercolor(_:)) — Sets the color that the system applies to the row background when this view is placed in a list.
- [background(_:alignment:)](https://developer.apple.com/documentation/swiftui/view/background(_:alignment:)) — Layers the given view behind this view.
- [overlay(_:alignment:)](https://developer.apple.com/documentation/swiftui/view/overlay(_:alignment:)) — Layers a secondary view in front of this view.
- [foregroundColor(_:)](https://developer.apple.com/documentation/swiftui/view/foregroundcolor(_:)) — Sets the color of the foreground elements displayed by this view.
- [complicationForeground()](https://developer.apple.com/documentation/swiftui/view/complicationforeground()) — Promotes this view to the foreground in a complication.

## Text modifiers {#Text-modifiers}

- [autocapitalization(_:)](https://developer.apple.com/documentation/swiftui/view/autocapitalization(_:)) — Sets whether to apply auto-capitalization to this view.
- [disableAutocorrection(_:)](https://developer.apple.com/documentation/swiftui/view/disableautocorrection(_:)) — Sets whether to disable autocorrection for this view.

## Auxiliary view modifiers {#Auxiliary-view-modifiers}

- [navigationBarTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitle(_:)) — Sets the title in the navigation bar for this view.
- [navigationBarTitle(_:displayMode:)](https://developer.apple.com/documentation/swiftui/view/navigationbartitle(_:displaymode:)) — Sets the title and display mode in the navigation bar for this view.
- [navigationBarItems(leading:)](https://developer.apple.com/documentation/swiftui/view/navigationbaritems(leading:)) — Sets the navigation bar items for this view.
- [navigationBarItems(leading:trailing:)](https://developer.apple.com/documentation/swiftui/view/navigationbaritems(leading:trailing:)) — Sets the navigation bar items for this view.
- [navigationBarItems(trailing:)](https://developer.apple.com/documentation/swiftui/view/navigationbaritems(trailing:)) — Configures the navigation bar items for this view.
- [navigationBarHidden(_:)](https://developer.apple.com/documentation/swiftui/view/navigationbarhidden(_:)) — Hides the navigation bar for this view.
- [statusBar(hidden:)](https://developer.apple.com/documentation/swiftui/view/statusbar(hidden:)) — Sets the visibility of the status bar.
- [contextMenu(_:)](https://developer.apple.com/documentation/swiftui/view/contextmenu(_:)) — Adds a context menu to the view.

## Style modifiers {#Style-modifiers}

- [menuButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/menubuttonstyle(_:)) — Sets the style for menu buttons within this view.
- [navigationViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationviewstyle(_:)) — Sets the style for navigation views within this view.

## Layout modifiers {#Layout-modifiers}

- [frame()](https://developer.apple.com/documentation/swiftui/view/frame()) — Positions this view within an invisible frame.
- [edgesIgnoringSafeArea(_:)](https://developer.apple.com/documentation/swiftui/view/edgesignoringsafearea(_:)) — Changes the view’s proposed area to extend outside the screen’s safe areas.
- [coordinateSpace(name:)](https://developer.apple.com/documentation/swiftui/view/coordinatespace(name:)) — Assigns a name to the view’s coordinate space, so other code can operate on dimensions like points and sizes relative to the named space.

## Graphics and rendering modifiers {#Graphics-and-rendering-modifiers}

- [accentColor(_:)](https://developer.apple.com/documentation/swiftui/view/accentcolor(_:)) — Sets the accent color for this view and the views it contains.
- [mask(_:)](https://developer.apple.com/documentation/swiftui/view/mask(_:)) — Masks this view using the alpha channel of the given view.
- [animation(_:)](https://developer.apple.com/documentation/swiftui/view/animation(_:)-1hc0p) — Applies the given animation to all animatable values within this view.
- [cornerRadius(_:antialiased:)](https://developer.apple.com/documentation/swiftui/view/cornerradius(_:antialiased:)) — Clips this view to its bounding frame, with the specified corner radius.

## Input and events modifiers {#Input-and-events-modifiers}

- [dropDestination(for:action:isTargeted:)](https://developer.apple.com/documentation/swiftui/view/dropdestination(for:action:istargeted:)) — Defines the destination of a drag and drop operation that handles the dropped content with a closure that you specify.
- [onChange(of:perform:)](https://developer.apple.com/documentation/swiftui/view/onchange(of:perform:)) — Adds an action to perform when the given value changes.
- [onTapGesture(count:coordinateSpace:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:coordinatespace:perform:)-36x9h) — Adds an action to perform when this view recognizes a tap gesture, and provides the action with the location of the interaction.
- [onLongPressGesture(minimumDuration:maximumDistance:pressing:perform:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:pressing:perform:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongPressGesture(minimumDuration:pressing:perform:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:pressing:perform:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onPasteCommand(of:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:perform:)-4f78f) — Adds an action to perform in response to the system’s Paste command.
- [onPasteCommand(of:validator:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:validator:perform:)-964k1) — Adds an action to perform in response to the system’s Paste command with items that you validate.
- [onDrop(of:delegate:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:delegate:)-2vr9o) — Defines the destination for a drag and drop operation with the same size and position as this view, with behavior controlled by the given delegate.
- [onDrop(of:isTargeted:perform:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:istargeted:perform:)) — Defines the destination of a drag-and-drop operation that handles the dropped content with a closure that you specify.
- [focusable(_:onFocusChange:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:onfocuschange:)) — Specifies if the view is focusable and, if so, adds an action to perform when the view comes into focus.
- [onContinuousHover(coordinateSpace:perform:)](https://developer.apple.com/documentation/swiftui/view/oncontinuoushover(coordinatespace:perform:)-8gyrl) — Adds an action to perform when the pointer enters, moves within, and exits the view’s bounds.

## View presentation modifiers {#View-presentation-modifiers}

- [actionSheet(isPresented:content:)](https://developer.apple.com/documentation/swiftui/view/actionsheet(ispresented:content:)) — Presents an action sheet when a given condition is true.
- [actionSheet(item:content:)](https://developer.apple.com/documentation/swiftui/view/actionsheet(item:content:)) — Presents an action sheet using the given item as a data source for the sheet’s content.
- [alert(isPresented:content:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:content:)) — Presents an alert to the user.
- [alert(item:content:)](https://developer.apple.com/documentation/swiftui/view/alert(item:content:)) — Presents an alert to the user.

## Search modifiers {#Search-modifiers}

- [searchable(text:placement:prompt:suggestions:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:placement:prompt:suggestions:)) — Marks this view as searchable, which configures the display of a search field.

## Tab modifiers {#Tab-modifiers}

- [tabItem(_:)](https://developer.apple.com/documentation/swiftui/view/tabitem(_:)) — Sets the tab bar item associated with this view.

## Generating image modifiers {#Generating-image-modifiers}

- [imagePlaygroundPersonalizationPolicy(_:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundpersonalizationpolicy(_:)) — Policy determining whether to support the usage of people in the playground or not.

## Technology-specific modifiers {#Technology-specific-modifiers}

- [postToPhotosSharedAlbumSheet(isPresented:items:photoLibrary:defaultAlbumIdentifier:completion:)](https://developer.apple.com/documentation/swiftui/view/posttophotossharedalbumsheet(ispresented:items:photolibrary:defaultalbumidentifier:completion:)) — Presents an “Add to Shared Album” sheet that allows the user to post the given items to a shared album.
- [offerCodeRedemption(isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/offercoderedemption(ispresented:oncompletion:))
- [subscriptionPromotionalOffer(offer:signature:)](https://developer.apple.com/documentation/swiftui/view/subscriptionpromotionaloffer(offer:signature:)) — Selects a promotional offer to apply to a purchase a customer makes from a subscription store view.
