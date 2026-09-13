# Input and event modifiers

Supply actions for a view to perform in response to user input and system events.

## Overview {#Overview}

Use input and event modifiers to configure and provide handlers for a wide variety of user inputs or system events. For example, you can detect and control focus, respond to life cycle events like view appearance and disappearance, manage keyboard shortcuts, and much more.

## Interactivity {#Interactivity}

- [disabled(_:)](https://developer.apple.com/documentation/swiftui/view/disabled(_:)) — Adds a condition that controls whether users can interact with this view.
- [interactionActivityTrackingTag(_:)](https://developer.apple.com/documentation/swiftui/view/interactionactivitytrackingtag(_:)) — Sets a tag that you use for tracking interactivity.

## List controls {#List-controls}

- [swipeActions(edge:allowsFullSwipe:content:)](https://developer.apple.com/documentation/swiftui/view/swipeactions(edge:allowsfullswipe:content:)) — Adds custom swipe actions to a row in a list.
- [refreshable(action:)](https://developer.apple.com/documentation/swiftui/view/refreshable(action:)) — Adds an asynchronous handler that can update the data the view displays when a person initiates a request, such as by pulling to refresh.
- [selectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/selectiondisabled(_:)) — Adds a condition that controls whether users can select this view.

## Container controls {#Container-controls}

- [swipeActions(edge:allowsFullSwipe:content:onPresentationChanged:)](https://developer.apple.com/documentation/swiftui/view/swipeactions(edge:allowsfullswipe:content:onpresentationchanged:)) — Adds custom swipe actions to a row in a list or container, notifying you when the actions are revealed or dismissed.
- [swipeActionsContainer()](https://developer.apple.com/documentation/swiftui/view/swipeactionscontainer()) — Coordinates swipe action dismissal and mutual exclusion across rows in a container.

## Scroll controls {#Scroll-controls}

- [scrollPosition(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/scrollposition(_:anchor:)) — Associates a binding to a scroll position with a scroll view within this view.
- [scrollPosition(id:anchor:)](https://developer.apple.com/documentation/swiftui/view/scrollposition(id:anchor:)) — Associates a binding to be updated when a scroll view within this view scrolls.
- [defaultScrollAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/defaultscrollanchor(_:)) — Associates an anchor to control which part of the scroll view’s content should be rendered by default.
- [defaultScrollAnchor(_:for:)](https://developer.apple.com/documentation/swiftui/view/defaultscrollanchor(_:for:)) — Associates an anchor to control the position of a scroll view in a particular circumstance.
- [scrollTargetBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/scrolltargetbehavior(_:)) — Sets the scroll behavior of views scrollable in the provided axes.
- [scrollTargetLayout(isEnabled:)](https://developer.apple.com/documentation/swiftui/view/scrolltargetlayout(isenabled:)) — Configures the outermost layout as a scroll target layout.
- [scrollInputBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/scrollinputbehavior(_:for:)) — Enables or disables scrolling in scrollable views when using particular inputs.
- [scrollTransition(_:axis:transition:)](https://developer.apple.com/documentation/swiftui/view/scrolltransition(_:axis:transition:)) — Applies the given transition, animating between the phases of the transition as this view appears and disappears within the visible region of the containing scroll view.
- [scrollTransition(topLeading:bottomTrailing:axis:transition:)](https://developer.apple.com/documentation/swiftui/view/scrolltransition(topleading:bottomtrailing:axis:transition:)) — Applies the given transition, animating between the phases of the transition as this view appears and disappears within the visible region of the containing scroll view.
- [onScrollGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/onscrollgeometrychange(for:of:action:)) — Adds an action to be performed when a value, created from a scroll geometry, changes.
- [onScrollTargetVisibilityChange(idType:threshold:_:)](https://developer.apple.com/documentation/swiftui/view/onscrolltargetvisibilitychange(idtype:threshold:_:)) — Adds an action to be called with information about what views would be considered visible.
- [onScrollVisibilityChange(threshold:_:)](https://developer.apple.com/documentation/swiftui/view/onscrollvisibilitychange(threshold:_:)) — Adds an action to be called when the view crosses the threshold to be considered on/off screen.
- [onScrollPhaseChange(_:)](https://developer.apple.com/documentation/swiftui/view/onscrollphasechange(_:)) — Adds an action to perform when the scroll phase of the first scroll view in the hierarchy changes.

## Geometry {#Geometry}

- [onGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) — Adds an action to be performed when a value, created from a geometry proxy, changes.
- [onGeometryChange3D(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/ongeometrychange3d(for:of:action:)) — Returns a new view that arranges to call `action(value)` whenever the value computed by `transform(proxy)` changes, where `proxy` provides access to the view’s 3D geometry properties.
- [onInteractiveResizeChange(_:)](https://developer.apple.com/documentation/swiftui/view/oninteractiveresizechange(_:)) — Adds an action to perform when the enclosing window is being interactively resized.

## Taps and gestures {#Taps-and-gestures}

- [onTapGesture(count:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:)) — Adds an action to perform when this view recognizes a tap gesture.
- [onTapGesture(count:coordinateSpace:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:coordinatespace:perform:)) — Adds an action to perform when this view recognizes a tap gesture, and provides the action with the location of the interaction.
- [onTapGesture(count:coordinateSpace:inputKinds:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:coordinatespace:inputkinds:perform:)) — Adds an action to perform when this view recognizes a tap gesture, and provides the action with the location of the interaction.
- [onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongPressGesture(minimumDuration:maximumDistance:inputKinds:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:inputkinds:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongPressGesture(minimumDuration:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongTouchGesture(minimumDuration:perform:onTouchingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongtouchgesture(minimumduration:perform:ontouchingchanged:)) — Adds an action to perform when this view recognizes a remote long touch gesture. A long touch gesture is when the finger is on the remote touch surface without actually pressing.
- [gesture(_:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:)) — Attaches an [NSGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentable) to the view.
- [gesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:isenabled:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [gesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:name:isenabled:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [gesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:including:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [highPriorityGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [highPriorityGesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:isenabled:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [highPriorityGesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:name:isenabled:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [simultaneousGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [simultaneousGesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:isenabled:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [simultaneousGesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:name:isenabled:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [defersSystemGestures(on:)](https://developer.apple.com/documentation/swiftui/view/deferssystemgestures(on:)) — Sets the screen edge from which you want your gesture to take precedence over the system gesture.
- [onPencilDoubleTap(perform:)](https://developer.apple.com/documentation/swiftui/view/onpencildoubletap(perform:)) — Adds an action to perform after the user double-taps their Apple Pencil.
- [onPencilSqueeze(perform:)](https://developer.apple.com/documentation/swiftui/view/onpencilsqueeze(perform:)) — Adds an action to perform when the user squeezes their Apple Pencil.
- [allowsWindowActivationEvents()](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents()) — Configures gestures in this view hierarchy to handle events that activate the containing window.
- [allowsWindowActivationEvents(_:)](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents(_:)) — Configures whether gestures in this view hierarchy can handle events that activate the containing window.

## Keyboard input {#Keyboard-input}

- [onKeyPress(_:action:)](https://developer.apple.com/documentation/swiftui/view/onkeypress(_:action:)) — Performs an action if the user presses a key on a hardware keyboard while the view has focus.
- [onKeyPress(phases:action:)](https://developer.apple.com/documentation/swiftui/view/onkeypress(phases:action:)) — Performs an action if the user presses any key on a hardware keyboard while the view has focus.
- [onKeyPress(_:phases:action:)](https://developer.apple.com/documentation/swiftui/view/onkeypress(_:phases:action:)) — Performs an action if the user presses a key on a hardware keyboard while the view has focus.
- [onKeyPress(characters:phases:action:)](https://developer.apple.com/documentation/swiftui/view/onkeypress(characters:phases:action:)) — Performs an action if the user presses one or more keys on a hardware keyboard while the view has focus.
- [onKeyPress(keys:phases:action:)](https://developer.apple.com/documentation/swiftui/view/onkeypress(keys:phases:action:)) — Performs an action if the user presses one or more keys on a hardware keyboard while the view has focus.
- [onModifierKeysChanged(mask:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onmodifierkeyschanged(mask:initial:_:)) — Performs an action whenever the user presses or releases a hardware modifier key.

## Keyboard shortcuts {#Keyboard-shortcuts}

- [keyboardShortcut(_:)](https://developer.apple.com/documentation/swiftui/view/keyboardshortcut(_:)) — Assigns a keyboard shortcut to the modified control.
- [keyboardShortcut(_:modifiers:)](https://developer.apple.com/documentation/swiftui/view/keyboardshortcut(_:modifiers:)) — Defines a keyboard shortcut and assigns it to the modified control.
- [keyboardShortcut(_:modifiers:localization:)](https://developer.apple.com/documentation/swiftui/view/keyboardshortcut(_:modifiers:localization:)) — Defines a keyboard shortcut and assigns it to the modified control.
- [modifierKeyAlternate(_:_:)](https://developer.apple.com/documentation/swiftui/view/modifierkeyalternate(_:_:)) — Builds a view to use in place of the modified view when the user presses the modifier key(s) indicated by the given set.

## Hand interactions {#Hand-interactions}

- [handGestureShortcut(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/handgestureshortcut(_:isenabled:)) — Assigns a hand gesture shortcut to the modified control.
- [handPointerBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/handpointerbehavior(_:)) — Sets the behavior of the hand pointer while the user is interacting with the view.
- [manipulable(coordinateSpace:operations:inertia:isEnabled:onChanged:)](https://developer.apple.com/documentation/swiftui/view/manipulable(coordinatespace:operations:inertia:isenabled:onchanged:)) — Allows this view to be manipulated using common hand gestures.
- [manipulable(transform:coordinateSpace:operations:inertia:isEnabled:onChanged:)](https://developer.apple.com/documentation/swiftui/view/manipulable(transform:coordinatespace:operations:inertia:isenabled:onchanged:)) — Applies the given 3D affine transform to the view and allows it to be manipulated using common hand gestures.
- [manipulable(using:)](https://developer.apple.com/documentation/swiftui/view/manipulable(using:)) — Allows the view to be manipulated using a manipulation gesture attached to a different view.
- [manipulationGesture(updating:coordinateSpace:operations:inertia:isEnabled:onChanged:)](https://developer.apple.com/documentation/swiftui/view/manipulationgesture(updating:coordinatespace:operations:inertia:isenabled:onchanged:)) — Adds a manipulation gesture to this view without allowing this view to be manipulable itself.

## Hover {#Hover}

- [onHover(perform:)](https://developer.apple.com/documentation/swiftui/view/onhover(perform:)) — Adds an action to perform when the user moves the pointer over or away from the view’s frame.
- [onContinuousHover(coordinateSpace:perform:)](https://developer.apple.com/documentation/swiftui/view/oncontinuoushover(coordinatespace:perform:)) — Adds an action to perform when the pointer enters, moves within, and exits the view’s bounds.
- [hoverEffect(_:)](https://developer.apple.com/documentation/swiftui/view/hovereffect(_:)) — Applies a hover effect to this view.
- [hoverEffect(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/hovereffect(_:isenabled:)) — Applies a hover effect to this view.
- [hoverEffect(_:in:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/hovereffect(_:in:isenabled:)) — Applies a hover effect to this view, optionally adding it to a [HoverEffectGroup](https://developer.apple.com/documentation/swiftui/hovereffectgroup).
- [hoverEffect(in:isEnabled:body:)](https://developer.apple.com/documentation/swiftui/view/hovereffect(in:isenabled:body:)) — Applies a hover effect to this view described by the given closure.
- [hoverEffectGroup()](https://developer.apple.com/documentation/swiftui/view/hovereffectgroup()) — Adds an implicit [HoverEffectGroup](https://developer.apple.com/documentation/swiftui/hovereffectgroup) to all effects defined on descendant views, so that all effects added to subviews activate as a group whenever this view or any descendant views are hovered.
- [hoverEffectGroup(_:)](https://developer.apple.com/documentation/swiftui/view/hovereffectgroup(_:)) — Adds a [HoverEffectGroup](https://developer.apple.com/documentation/swiftui/hovereffectgroup) to all effects defined on descendant views, and activates the group whenever this view or any descendant views are hovered.
- [hoverEffectGroup(id:in:behavior:)](https://developer.apple.com/documentation/swiftui/view/hovereffectgroup(id:in:behavior:)) — Adds a [HoverEffectGroup](https://developer.apple.com/documentation/swiftui/hovereffectgroup) to all effects defined on descendant views, and activates the group whenever this view or any descendant views are hovered.
- [hoverEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/hovereffectdisabled(_:)) — Adds a condition that controls whether this view can display hover effects.
- [defaultHoverEffect(_:)](https://developer.apple.com/documentation/swiftui/view/defaulthovereffect(_:)) — Sets the default hover effect to use for views within this view.
- [listRowHoverEffect(_:)](https://developer.apple.com/documentation/swiftui/view/listrowhovereffect(_:)) — Requests that the containing list row use the provided hover effect.
- [listRowHoverEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/listrowhovereffectdisabled(_:)) — Requests that the containing list row have its hover effect disabled.

## Pointer {#Pointer}

- [pointerVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/pointervisibility(_:)) — Sets the visibility of the pointer when it’s over the view.
- [pointerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/pointerstyle(_:)) — Sets the pointer style to display when the pointer is over the view.

## Focus {#Focus}

- [focused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/focused(_:equals:)) — Modifies this view by binding its focus state to the given state value.
- [focused(_:)](https://developer.apple.com/documentation/swiftui/view/focused(_:)) — Modifies this view by binding its focus state to the given Boolean state value.
- [focusedValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:)) — Sets the focused value for the given object type.
- [focusedValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:_:)) — Modifies this view by injecting a value that you provide for use by other views whose state depends on the focused view hierarchy.
- [focusedSceneValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:)) — Sets the focused value for the given object type at a scene-wide scope.
- [focusedSceneValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:_:)) — Modifies this view by injecting a value that you provide for use by other views whose state depends on the focused scene.
- [focusedObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedobject(_:)) — Creates a new view that exposes the provided object to other views whose whose state depends on the focused view hierarchy.
- [focusedSceneObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedsceneobject(_:)) — Creates a new view that exposes the provided object to other views whose whose state depends on the active scene.
- [prefersDefaultFocus(_:in:)](https://developer.apple.com/documentation/swiftui/view/prefersdefaultfocus(_:in:)) — Indicates that the view should receive focus by default for a given namespace.
- [focusScope(_:)](https://developer.apple.com/documentation/swiftui/view/focusscope(_:)) — Creates a focus scope that SwiftUI uses to limit default focus preferences.
- [focusSection()](https://developer.apple.com/documentation/swiftui/view/focussection()) — Indicates that the view’s frame and cohort of focusable descendants should be used to guide focus movement.
- [focusable(_:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:)) — Specifies if the view is focusable.
- [focusable(_:interactions:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:interactions:)) — Specifies if the view is focusable, and if so, what focus-driven interactions it supports.
- [focusEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/focuseffectdisabled(_:)) — Adds a condition that controls whether this view can display focus effects, such as a default focus ring or hover effect.
- [defaultFocus(_:_:priority:)](https://developer.apple.com/documentation/swiftui/view/defaultfocus(_:_:priority:)) — Defines a region of the window in which default focus is evaluated by assigning a value to a given focus state binding.
- [searchFocused(_:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:)) — Modifies this view by binding the focus state of the search field associated with the nearest searchable modifier to the given Boolean value.
- [searchFocused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:equals:)) — Modifies this view by binding the focus state of the search field associated with the nearest searchable modifier to the given value.

## Copy and paste {#Copy-and-paste}

- [copyable(_:)](https://developer.apple.com/documentation/swiftui/view/copyable(_:)) — Specifies a list of items to copy in response to the system’s Copy command.
- [cuttable(for:action:)](https://developer.apple.com/documentation/swiftui/view/cuttable(for:action:)) — Specifies an action that moves items to the Clipboard in response to the system’s Cut command.
- [pasteDestination(for:action:validator:)](https://developer.apple.com/documentation/swiftui/view/pastedestination(for:action:validator:)) — Specifies an action that adds validated items to a view in response to the system’s Paste command.
- [onCopyCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncopycommand(perform:)) — Adds an action to perform in response to the system’s Copy command.
- [onCutCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncutcommand(perform:)) — Adds an action to perform in response to the system’s Cut command.
- [onPasteCommand(of:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:perform:)) — Adds an action to perform in response to the system’s Paste command.
- [onPasteCommand(of:validator:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:validator:perform:)) — Adds an action to perform in response to the system’s Paste command with items that you validate.

## Drag and drop {#Drag-and-drop}

- [dragConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dragconfiguration(_:)) — Configures a drag session.
- [dragContainer(for:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:in:_:)) — A container with draggable views where the drag payload is based on multiple identifiers of dragged items.
- [dragContainer(for:itemID:in:_:)](https://developer.apple.com/documentation/swiftui/view/dragcontainer(for:itemid:in:_:)) — A container with draggable views.
- [dragContainerSelection(_:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/dragcontainerselection(_:containernamespace:)) — Provides multiple item selection support for drag containers.
- [dragPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/dragpreviewsformation(_:)) — Describes the way dragged previews are visually composed.
- [draggable(_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:)) — Activates this view as the source of a drag and drop operation.
- [draggable(_:preview:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:preview:)) — Activates this view as the source of a drag and drop operation.
- [draggable(_:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:containernamespace:_:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional identifiable payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:id:containerNamespace:_:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:containernamespace:_:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:id:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:id:item:containernamespace:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional payload and specify the namespace of the drag container this view belongs to.
- [draggable(_:item:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(_:item:containernamespace:)) — Activates this view as the source of a drag and drop operation, allowing to provide optional identifiable payload and specify the namespace of the drag container this view belongs to.
- [draggable(containerItemID:containerNamespace:)](https://developer.apple.com/documentation/swiftui/view/draggable(containeritemid:containernamespace:)) — Inside a drag container, activates this view as the source of a drag and drop operation. Supports lazy drag containers.
- [dropConfiguration(_:)](https://developer.apple.com/documentation/swiftui/view/dropconfiguration(_:)) — Configures a drop session.
- [dropDestination(for:isEnabled:action:)](https://developer.apple.com/documentation/swiftui/view/dropdestination(for:isenabled:action:)) — Defines the destination of a drag and drop operation that provides a drop operation proposal and handles the dropped content with a closure that you specify.
- [dropPreviewsFormation(_:)](https://developer.apple.com/documentation/swiftui/view/droppreviewsformation(_:)) — Describes the way previews for a drop are composed.
- [itemProvider(_:)](https://developer.apple.com/documentation/swiftui/view/itemprovider(_:)) — Provides a closure that vends the drag representation to be used for a particular data element.
- [onDrag(_:preview:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:preview:)) — Activates this view as the source of a drag and drop operation.
- [onDrag(_:)](https://developer.apple.com/documentation/swiftui/view/ondrag(_:)) — Activates this view as the source of a drag and drop operation.
- [onDragSessionUpdated(_:)](https://developer.apple.com/documentation/swiftui/view/ondragsessionupdated(_:)) — Specifies an action to perform on each update of an ongoing dragging operation activated by `draggable(_:)` or anther drag modifiers.
- [onDrop(of:isTargeted:perform:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:istargeted:perform:)) — Defines the destination of a drag-and-drop operation that handles the dropped content with a closure that you specify.
- [onDrop(of:delegate:)](https://developer.apple.com/documentation/swiftui/view/ondrop(of:delegate:)) — Defines the destination of a drag and drop operation using behavior controlled by the delegate that you provide.
- [onDropSessionUpdated(_:)](https://developer.apple.com/documentation/swiftui/view/ondropsessionupdated(_:)) — Specifies an action to perform on each update of an ongoing drop operation activated by `dropDestination(_:)` or other drop modifiers.
- [springLoadingBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/springloadingbehavior(_:)) — Sets the spring loading behavior this view.

## Reordering {#Reordering}

- [reorderContainer(for:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:isenabled:move:)) — Defines a container of reorderable views.
- [reorderContainer(for:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:in:isenabled:move:)) — Defines a container of reorderable views, with a type you specify to identify sections.
- [reorderContainer(for:itemID:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:isenabled:move:)) — Defines a container of reorderable views, with a type and keypath you specify to identify items.
- [reorderContainer(for:itemID:in:isEnabled:move:)](https://developer.apple.com/documentation/swiftui/view/reordercontainer(for:itemid:in:isenabled:move:)) — Defines a container of reorderable views, with a type and keypath you use to identify items and a type you use to identify collections.

## Submission {#Submission}

- [onAssignedDocumentDidSubmit(_:)](https://developer.apple.com/documentation/swiftui/view/onassigneddocumentdidsubmit(_:)) — Adds an action to perform after submitting an assigned document.
- [onAssignedDocumentDidWithdraw(_:)](https://developer.apple.com/documentation/swiftui/view/onassigneddocumentdidwithdraw(_:)) — Adds an action to perform after an assigned document submission has been withdrawn.
- [onAssignedDocumentWillSubmit(_:)](https://developer.apple.com/documentation/swiftui/view/onassigneddocumentwillsubmit(_:)) — Adds an action to perform before submitting an assigned document.
- [onAssignedDocumentWillWithdraw(_:)](https://developer.apple.com/documentation/swiftui/view/onassigneddocumentwillwithdraw(_:)) — Adds an action to perform before withdrawing an assigned document submission.
- [onSubmit(of:_:)](https://developer.apple.com/documentation/swiftui/view/onsubmit(of:_:)) — Adds an action to perform when the user submits a value to this view.
- [submitScope(_:)](https://developer.apple.com/documentation/swiftui/view/submitscope(_:)) — Prevents submission triggers originating from this view to invoke a submission action configured by a submission modifier higher up in the view hierarchy.
- [submitLabel(_:)](https://developer.apple.com/documentation/swiftui/view/submitlabel(_:)) — Sets the submit label for this view.

## Movement {#Movement}

- [onMoveCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/onmovecommand(perform:)) — Adds an action to perform in response to a move command, like when the user presses an arrow key on a Mac keyboard, or taps the edge of the Siri Remote when controlling an Apple TV.
- [moveDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/movedisabled(_:)) — Adds a condition for whether the view’s view hierarchy is movable.

## Deletion {#Deletion}

- [onDeleteCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/ondeletecommand(perform:)) — Adds an action to perform in response to the system’s Delete command, or pressing either the ⌫ (backspace) or ⌦ (forward delete) keys while the view has focus.
- [deleteDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/deletedisabled(_:)) — Adds a condition for whether the view’s view hierarchy is deletable.

## Commands {#Commands}

- [pageCommand(value:in:step:)](https://developer.apple.com/documentation/swiftui/view/pagecommand(value:in:step:)) — Steps a value through a range in response to page up or page down commands.
- [onExitCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/onexitcommand(perform:)) — Sets up an action that triggers in response to receiving the exit command while the view has focus.
- [onPlayPauseCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/onplaypausecommand(perform:)) — Adds an action to perform in response to the system’s Play/Pause command.
- [onCommand(_:perform:)](https://developer.apple.com/documentation/swiftui/view/oncommand(_:perform:)) — Adds an action to perform in response to the given selector.

## Digital crown {#Digital-crown}

- [digitalCrownAccessory(_:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownaccessory(_:)) — Specifies the visibility of Digital Crown accessory Views on Apple Watch.
- [digitalCrownAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownaccessory(content:)) — Places an accessory View next to the Digital Crown on Apple Watch.
- [digitalCrownRotation(_:from:through:sensitivity:isContinuous:isHapticFeedbackEnabled:onChange:onIdle:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownrotation(_:from:through:sensitivity:iscontinuous:ishapticfeedbackenabled:onchange:onidle:)) — Tracks Digital Crown rotations by updating the specified binding.
- [digitalCrownRotation(_:onChange:onIdle:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownrotation(_:onchange:onidle:)) — Tracks Digital Crown rotations by updating the specified binding.
- [digitalCrownRotation(detent:from:through:by:sensitivity:isContinuous:isHapticFeedbackEnabled:onChange:onIdle:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownrotation(detent:from:through:by:sensitivity:iscontinuous:ishapticfeedbackenabled:onchange:onidle:)) — Tracks Digital Crown rotations by updating the specified binding.
- [digitalCrownRotation(_:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownrotation(_:)) — Tracks Digital Crown rotations by updating the specified binding.
- [digitalCrownRotation(_:from:through:by:sensitivity:isContinuous:isHapticFeedbackEnabled:)](https://developer.apple.com/documentation/swiftui/view/digitalcrownrotation(_:from:through:by:sensitivity:iscontinuous:ishapticfeedbackenabled:)) — Tracks Digital Crown rotations by updating the specified binding.

## Game controller {#Game-controller}

- [handlesGameControllerEvents(matching:)](https://developer.apple.com/documentation/swiftui/view/handlesgamecontrollerevents(matching:)) — Specifies the game controllers events which should be delivered through the GameController framework when the view, or one of its descendants has focus.
- [handlesGameControllerEvents(matching:withOptions:)](https://developer.apple.com/documentation/swiftui/view/handlesgamecontrollerevents(matching:withoptions:)) — Specifies the game controllers events which should be delivered through the GameController framework when the view or one of its descendants has focus.

## Immersive spaces {#Immersive-spaces}

- [onImmersionChange(initial:_:)](https://developer.apple.com/documentation/swiftui/view/onimmersionchange(initial:_:)) — Performs an action when the immersion state of your app changes.
- [onWorldRecenter(action:)](https://developer.apple.com/documentation/swiftui/view/onworldrecenter(action:)) — Adds an action to perform when recentering the view with the digital crown.
- [immersiveEnvironmentPicker(content:)](https://developer.apple.com/documentation/swiftui/view/immersiveenvironmentpicker(content:)) — Add menu items to open immersive spaces from a media player’s environment picker.

## Volumes {#Volumes}

- [onVolumeViewpointChange(updateStrategy:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onvolumeviewpointchange(updatestrategy:initial:_:)) — Adds an action to perform when the viewpoint of the volume changes.
- [supportedVolumeViewpoints(_:)](https://developer.apple.com/documentation/swiftui/view/supportedvolumeviewpoints(_:)) — Specifies which viewpoints are supported for the window bar and ornaments in a volume.

## User activities {#User-activities}

- [userActivity(_:element:_:)](https://developer.apple.com/documentation/swiftui/view/useractivity(_:element:_:)) — Advertises a user activity type.
- [userActivity(_:isActive:_:)](https://developer.apple.com/documentation/swiftui/view/useractivity(_:isactive:_:)) — Advertises a user activity type.
- [onContinueUserActivity(_:perform:)](https://developer.apple.com/documentation/swiftui/view/oncontinueuseractivity(_:perform:)) — Registers a handler to invoke in response to a user activity that your app receives.
- [handlesExternalEvents(preferring:allowing:)](https://developer.apple.com/documentation/swiftui/view/handlesexternalevents(preferring:allowing:)) — Specifies the external events that the view’s scene handles if the scene is already open.

## View life cycle {#View-life-cycle}

- [onAppear(perform:)](https://developer.apple.com/documentation/swiftui/view/onappear(perform:)) — Adds an action to perform before this view appears.
- [onDisappear(perform:)](https://developer.apple.com/documentation/swiftui/view/ondisappear(perform:)) — Adds an action to perform after this view disappears.
- [onChange(of:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onchange(of:initial:_:)) — Adds a modifier for this view that fires an action when a specific value changes.
- [task(id:name:executorPreference:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(id:name:executorpreference:priority:file:line:_:)) — Adds a task to perform before this view appears or when a specified value changes.
- [task(id:name:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(id:name:priority:file:line:_:)) — Adds a task to perform before this view appears or when a specified value changes.
- [task(name:executorPreference:priority:file:line:action:)](https://developer.apple.com/documentation/swiftui/view/task(name:executorpreference:priority:file:line:action:)) — Adds an asynchronous task to perform before this view appears.
- [task(name:priority:file:line:_:)](https://developer.apple.com/documentation/swiftui/view/task(name:priority:file:line:_:)) — Adds an asynchronous task to perform before this view appears.

## File renaming {#File-renaming}

- [renameAction(_:)](https://developer.apple.com/documentation/swiftui/view/renameaction(_:)) — Sets a closure to run for the rename action.

## URLs {#URLs}

- [onOpenURL(perform:)](https://developer.apple.com/documentation/swiftui/view/onopenurl(perform:)) — Registers a handler to invoke in response to a URL that your app receives.
- [onOpenURL(prefersInApp:)](https://developer.apple.com/documentation/swiftui/view/onopenurl(prefersinapp:)) — Sets an `OpenURLAction` that prefers opening URL with an in-app browser. The `handler` closure takes a URL as input, and returns a `OpenURLAction.Result` that indicates the outcome of the action.
- [widgetURL(_:)](https://developer.apple.com/documentation/swiftui/view/widgeturl(_:)) — Sets the URL to open in the containing app when the user clicks the widget.

## Asynchronous image loading {#Asynchronous-image-loading}

- [asyncImageURLSession(_:)](https://developer.apple.com/documentation/swiftui/view/asyncimageurlsession(_:)) — A modifier that adds a URL session for asynchronous images contained in the view to use when fetching image data.

## Publisher events {#Publisher-events}

- [onReceive(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onreceive(_:perform:)) — Adds an action to perform when this view detects data emitted by the given publisher.

## Hit testing {#Hit-testing}

- [allowsHitTesting(_:)](https://developer.apple.com/documentation/swiftui/view/allowshittesting(_:)) — Configures whether this view participates in hit test operations.

## Content shape {#Content-shape}

- [contentShape(_:eoFill:)](https://developer.apple.com/documentation/swiftui/view/contentshape(_:eofill:)) — Defines the content shape for hit testing.
- [contentShape(_:_:eoFill:)](https://developer.apple.com/documentation/swiftui/view/contentshape(_:_:eofill:)) — Sets the content shape for this view.

## Import and export {#Import-and-export}

- [exportsItemProviders(_:onExport:)](https://developer.apple.com/documentation/swiftui/view/exportsitemproviders(_:onexport:)) — Exports a read-only item provider for consumption by shortcuts, quick actions, and services.
- [exportsItemProviders(_:onExport:onEdit:)](https://developer.apple.com/documentation/swiftui/view/exportsitemproviders(_:onexport:onedit:)) — Exports a read-write item provider for consumption by shortcuts, quick actions, and services.
- [importsItemProviders(_:onImport:)](https://developer.apple.com/documentation/swiftui/view/importsitemproviders(_:onimport:)) — Enables importing item providers from services, such as Continuity Camera on macOS.
- [exportableToServices(_:)](https://developer.apple.com/documentation/swiftui/view/exportabletoservices(_:)) — Exports items for consumption by shortcuts, quick actions, and services.
- [exportableToServices(_:onEdit:)](https://developer.apple.com/documentation/swiftui/view/exportabletoservices(_:onedit:)) — Exports read-write items for consumption by shortcuts, quick actions, and services.
- [importableFromServices(for:action:)](https://developer.apple.com/documentation/swiftui/view/importablefromservices(for:action:)) — Enables importing items from services, such as Continuity Camera on macOS.

## App intents {#App-intents}

- [appEntityIdentifier(_:)](https://developer.apple.com/documentation/swiftui/view/appentityidentifier(_:)) — Associates a SwiftUI view with an app entity to make its content discoverable by Apple Intelligence and Siri.
- [appEntityIdentifier(forSelectionType:identifier:)](https://developer.apple.com/documentation/swiftui/view/appentityidentifier(forselectiontype:identifier:)) — Associates the items in a SwiftUI list view with app entities to make them discoverable by Apple Intelligence and Siri.
- [appEntityUIElements(_:)](https://developer.apple.com/documentation/swiftui/view/appentityuielements(_:)) — Provides the system with additional context to make a custom view’s content discoverable by Apple Intelligence and Siri.
- [onAppIntentExecution(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onappintentexecution(_:perform:)) — Registers a handler to invoke in response to the specified app intent that your app receives.
- [shortcutsLinkStyle(_:)](https://developer.apple.com/documentation/swiftui/view/shortcutslinkstyle(_:)) — Sets the given style for ShortcutsLinks within the view hierarchy
- [siriTipViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/siritipviewstyle(_:)) — Sets the given style for SiriTipView within the view hierarchy

## Camera {#Camera}

- [onCameraCaptureEvent(isEnabled:action:)](https://developer.apple.com/documentation/swiftui/view/oncameracaptureevent(isenabled:action:)) — Used to register an action triggered by system capture events.
- [onCameraCaptureEvent(isEnabled:defaultSoundDisabled:action:)](https://developer.apple.com/documentation/swiftui/view/oncameracaptureevent(isenabled:defaultsounddisabled:action:)) — Used to register an action triggered by system capture events.
- [onCameraCaptureEvent(isEnabled:defaultSoundDisabled:primaryAction:secondaryAction:)](https://developer.apple.com/documentation/swiftui/view/oncameracaptureevent(isenabled:defaultsounddisabled:primaryaction:secondaryaction:)) — Used to register actions triggered by system capture events.
- [onCameraCaptureEvent(isEnabled:primaryAction:secondaryAction:)](https://developer.apple.com/documentation/swiftui/view/oncameracaptureevent(isenabled:primaryaction:secondaryaction:)) — Used to register actions triggered by system capture events.
- [cameraAnchor(isActive:)](https://developer.apple.com/documentation/swiftui/view/cameraanchor(isactive:)) — Specifies the view that should act as the virtual camera for Apple Vision Pro 2D Persona stream.
