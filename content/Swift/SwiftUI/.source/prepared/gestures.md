# Gestures

Define interactions from taps, clicks, and swipes to fine-grained gestures.

## Overview {#Overview}

Respond to gestures by adding gesture modifiers to your views. You can listen for taps, drags, pinches, and other standard gestures.

![](./images/gestures-hero@2x.png)

You can also compose custom gestures from individual gestures using the [simultaneously(with:)](https://developer.apple.com/documentation/swiftui/gesture/simultaneously(with:)), [sequenced(before:)](https://developer.apple.com/documentation/swiftui/gesture/sequenced(before:)), or [exclusively(before:)](https://developer.apple.com/documentation/swiftui/gesture/exclusively(before:)) modifiers, or combine gestures with keyboard modifiers using the [modifiers(_:)](https://developer.apple.com/documentation/swiftui/gesture/modifiers(_:)) modifier.

> Important: When you need a button, use a [Button](https://developer.apple.com/documentation/swiftui/button) instance rather than a tap gesture. You can use any view as the button’s label, and the button type automatically provides many of the standard behaviors that users expect from a button, like accessibility labels and hints.

For design guidance, see [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) in the Human Interface Guidelines.

## Essentials {#Essentials}

- [Adding interactivity with gestures](1.1-AddingInteractivityWithGestures/) — Use gesture modifiers to add interactivity to your app.

## Recognizing tap gestures {#Recognizing-tap-gestures}

- [onTapGesture(count:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:perform:)) — Adds an action to perform when this view recognizes a tap gesture.
- [onTapGesture(count:coordinateSpace:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:coordinatespace:perform:)) — Adds an action to perform when this view recognizes a tap gesture, and provides the action with the location of the interaction.
- [onTapGesture(count:coordinateSpace:inputKinds:perform:)](https://developer.apple.com/documentation/swiftui/view/ontapgesture(count:coordinatespace:inputkinds:perform:)) — Adds an action to perform when this view recognizes a tap gesture, and provides the action with the location of the interaction.
- [TapGesture](https://developer.apple.com/documentation/swiftui/tapgesture) — A gesture that recognizes one or more taps.
- [SpatialTapGesture](https://developer.apple.com/documentation/swiftui/spatialtapgesture) — A gesture that recognizes one or more taps and reports their location.

## Recognizing long-press gestures {#Recognizing-long-press-gestures}

- [onLongPressGesture(minimumDuration:maximumDistance:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongPressGesture(minimumDuration:maximumDistance:inputKinds:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:maximumdistance:inputkinds:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongPressGesture(minimumDuration:perform:onPressingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongpressgesture(minimumduration:perform:onpressingchanged:)) — Adds an action to perform when this view recognizes a long press gesture.
- [onLongTouchGesture(minimumDuration:perform:onTouchingChanged:)](https://developer.apple.com/documentation/swiftui/view/onlongtouchgesture(minimumduration:perform:ontouchingchanged:)) — Adds an action to perform when this view recognizes a remote long touch gesture. A long touch gesture is when the finger is on the remote touch surface without actually pressing.
- [LongPressGesture](https://developer.apple.com/documentation/swiftui/longpressgesture) — A gesture that succeeds when the user performs a long press.

## Recognizing spatial events {#Recognizing-spatial-events}

- [SpatialEventGesture](https://developer.apple.com/documentation/swiftui/spatialeventgesture) — A gesture that provides information about ongoing spatial events like clicks and touches.
- [SpatialEventCollection](https://developer.apple.com/documentation/swiftui/spatialeventcollection) — A collection of spatial input events that target a specific view.
- [Chirality](https://developer.apple.com/documentation/swiftui/chirality) — The chirality, or handedness, of a pose.

## Recognizing gestures that change over time {#Recognizing-gestures-that-change-over-time}

- [gesture(_:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:)) — Attaches an [NSGestureRecognizerRepresentable](https://developer.apple.com/documentation/swiftui/nsgesturerecognizerrepresentable) to the view.
- [gesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:isenabled:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [gesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:name:isenabled:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [gesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/gesture(_:including:)) — Attaches a gesture to the view with a lower precedence than gestures defined by the view.
- [DragGesture](https://developer.apple.com/documentation/swiftui/draggesture) — A dragging motion that invokes an action as the drag-event sequence changes.
- [WindowDragGesture](https://developer.apple.com/documentation/swiftui/windowdraggesture) — A gesture that recognizes the motion of and handles dragging a window.
- [MagnifyGesture](https://developer.apple.com/documentation/swiftui/magnifygesture) — A gesture that recognizes a magnification motion and tracks the amount of magnification.
- [RotateGesture](https://developer.apple.com/documentation/swiftui/rotategesture) — A gesture that recognizes a rotation motion and tracks the angle of the rotation.
- [RotateGesture3D](https://developer.apple.com/documentation/swiftui/rotategesture3d) — A gesture that recognizes 3D rotation motion and tracks the angle and axis of the rotation.
- [GestureMask](https://developer.apple.com/documentation/swiftui/gesturemask) — Options that control how adding a gesture to a view affects other gestures recognized by the view and its subviews.

## Recognizing Apple Pencil gestures {#Recognizing-Apple-Pencil-gestures}

- [onPencilDoubleTap(perform:)](https://developer.apple.com/documentation/swiftui/view/onpencildoubletap(perform:)) — Adds an action to perform after the user double-taps their Apple Pencil.
- [onPencilSqueeze(perform:)](https://developer.apple.com/documentation/swiftui/view/onpencilsqueeze(perform:)) — Adds an action to perform when the user squeezes their Apple Pencil.
- [preferredPencilDoubleTapAction](https://developer.apple.com/documentation/swiftui/environmentvalues/preferredpencildoubletapaction) — The action that the user prefers to perform after double-tapping their Apple Pencil, as selected in the Settings app.
- [preferredPencilSqueezeAction](https://developer.apple.com/documentation/swiftui/environmentvalues/preferredpencilsqueezeaction) — The action that the user prefers to perform when squeezing their Apple Pencil, as selected in the Settings app.
- [PencilPreferredAction](https://developer.apple.com/documentation/swiftui/pencilpreferredaction) — An action that the user prefers to perform after double-tapping their Apple Pencil.
- [PencilDoubleTapGestureValue](https://developer.apple.com/documentation/swiftui/pencildoubletapgesturevalue) — Describes the value of an Apple Pencil double-tap gesture.
- [PencilSqueezeGestureValue](https://developer.apple.com/documentation/swiftui/pencilsqueezegesturevalue) — Describes the value of an Apple Pencil squeeze gesture.
- [PencilSqueezeGesturePhase](https://developer.apple.com/documentation/swiftui/pencilsqueezegesturephase) — Describes the phase and value of an Apple Pencil squeeze gesture.
- [PencilHoverPose](https://developer.apple.com/documentation/swiftui/pencilhoverpose) — A value describing the location and distance of an Apple Pencil hovering in the area above a view’s bounds.

## Combining gestures {#Combining-gestures}

- [Composing SwiftUI gestures](1.2-ComposingSwiftuiGestures/) — Combine gestures to create complex interactions.
- [simultaneousGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:including:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [simultaneousGesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:isenabled:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [simultaneousGesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/simultaneousgesture(_:name:isenabled:)) — Attaches a gesture to the view to process simultaneously with gestures defined by the view.
- [SequenceGesture](https://developer.apple.com/documentation/swiftui/sequencegesture) — A gesture that’s a sequence of two gestures.
- [SimultaneousGesture](https://developer.apple.com/documentation/swiftui/simultaneousgesture) — A gesture containing two gestures that can happen at the same time with neither of them preceding the other.
- [ExclusiveGesture](https://developer.apple.com/documentation/swiftui/exclusivegesture) — A gesture that consists of two gestures where only one of them can succeed.

## Customizing gestures {#Customizing-gestures}

- [GestureInputKinds](https://developer.apple.com/documentation/swiftui/gestureinputkinds) — An option set that specifies which input kinds a gesture should recognize.

## Defining custom gestures {#Defining-custom-gestures}

- [highPriorityGesture(_:including:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:including:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [highPriorityGesture(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:isenabled:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [highPriorityGesture(_:name:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/highprioritygesture(_:name:isenabled:)) — Attaches a gesture to the view with a higher precedence than gestures defined by the view.
- [handGestureShortcut(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/handgestureshortcut(_:isenabled:)) — Assigns a hand gesture shortcut to the modified control.
- [defersSystemGestures(on:)](https://developer.apple.com/documentation/swiftui/view/deferssystemgestures(on:)) — Sets the screen edge from which you want your gesture to take precedence over the system gesture.
- [Gesture](https://developer.apple.com/documentation/swiftui/gesture) — An instance that matches a sequence of events to a gesture, and returns a stream of values for each of its states.
- [AnyGesture](https://developer.apple.com/documentation/swiftui/anygesture) — A type-erased gesture.
- [HandActivationBehavior](https://developer.apple.com/documentation/swiftui/handactivationbehavior) — An activation behavior specific to hand-driven input.
- [HandGestureShortcut](https://developer.apple.com/documentation/swiftui/handgestureshortcut) — Hand gesture shortcuts describe finger and wrist movements that the user can perform in order to activate a button or toggle.

## Managing gesture state {#Managing-gesture-state}

- [GestureState](https://developer.apple.com/documentation/swiftui/gesturestate) — A property wrapper type that updates a property while the user performs a gesture and resets the property back to its initial state when the gesture ends.
- [GestureStateGesture](https://developer.apple.com/documentation/swiftui/gesturestategesture) — A gesture that updates the state provided by a gesture’s updating callback.

## Handling activation events {#Handling-activation-events}

- [allowsWindowActivationEvents(_:)](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents(_:)) — Configures whether gestures in this view hierarchy can handle events that activate the containing window.

## Deprecated gestures {#Deprecated-gestures}

- [MagnificationGesture](https://developer.apple.com/documentation/swiftui/magnificationgesture) — A gesture that recognizes a magnification motion and tracks the amount of magnification.
- [RotationGesture](https://developer.apple.com/documentation/swiftui/rotationgesture) — A gesture that recognizes a rotation motion and tracks the angle of the rotation.
