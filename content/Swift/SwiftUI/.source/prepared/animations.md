# Animations

Create smooth visual updates in response to state changes.

## Overview {#Overview}

You tell SwiftUI how to draw your app’s user interface for different states, and then rely on SwiftUI to make interface updates when the state changes.

![](./images/animations-hero@2x.png)

To avoid abrupt visual transitions when the state changes, add animation in one of the following ways:

- Animate all of the visual changes for a state change by changing the state inside a call to the [withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:)) global function.
- Add animation to a particular view when a specific value changes by applying the [animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:)) view modifier to the view.
- Animate changes to a [Binding](https://developer.apple.com/documentation/swiftui/binding) by using the binding’s [animation(_:)](https://developer.apple.com/documentation/swiftui/binding/animation(_:)) method.

SwiftUI animates the effects that many built-in view modifiers produce, like those that set a scale or opacity value. You can animate other values by making your custom views conform to the [Animatable](https://developer.apple.com/documentation/swiftui/animatable) protocol, and telling SwiftUI about the value you want to animate.

When an animated state change results in adding or removing a view to or from the view hierarchy, you can tell SwiftUI how to transition the view into or out of place using built-in transitions that [AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition) defines, like [slide](https://developer.apple.com/documentation/swiftui/anytransition/slide) or [scale](https://developer.apple.com/documentation/swiftui/anytransition/scale). You can also create custom transitions.

For design guidance, see [Motion](https://developer.apple.com/design/human-interface-guidelines/motion) in the Human Interface Guidelines.

## Adding state-based animation to an action {#Adding-state-based-animation-to-an-action}

- [withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:)) — Returns the result of recomputing the view’s body with the provided animation.
- [withAnimation(_:completionCriteria:_:completion:)](https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:)) — Returns the result of recomputing the view’s body with the provided animation, and runs the completion when all animations are complete.
- [AnimationCompletionCriteria](https://developer.apple.com/documentation/swiftui/animationcompletioncriteria) — The criteria that determines when an animation is considered finished.
- [Animation](https://developer.apple.com/documentation/swiftui/animation) — The way a view changes over time to create a smooth visual transition from one state to another.

## Adding state-based animation to a view {#Adding-state-based-animation-to-a-view}

- [animation(_:)](https://developer.apple.com/documentation/swiftui/view/animation(_:)) — Applies the given animation to this view when this view changes.
- [animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:)) — Applies the given animation to this view when the specified value changes.
- [animation(_:body:)](https://developer.apple.com/documentation/swiftui/view/animation(_:body:)) — Applies the given animation to all animatable values within the `body` closure.

## Creating phase-based animation {#Creating-phase-based-animation}

- [Controlling the timing and movements of your animations](4.1-ControllingTheTimingAndMovementsOfYourAnimations/) — Build sophisticated animations that you control using phase and keyframe animators.
- [phaseAnimator(_:content:animation:)](https://developer.apple.com/documentation/swiftui/view/phaseanimator(_:content:animation:)) — Animates effects that you apply to a view over a sequence of phases that change continuously.
- [phaseAnimator(_:trigger:content:animation:)](https://developer.apple.com/documentation/swiftui/view/phaseanimator(_:trigger:content:animation:)) — Animates effects that you apply to a view over a sequence of phases that change based on a trigger.
- [PhaseAnimator](https://developer.apple.com/documentation/swiftui/phaseanimator) — A container that animates its content by automatically cycling through a collection of phases that you provide, each defining a discrete step within an animation.

## Creating keyframe-based animation {#Creating-keyframe-based-animation}

- [keyframeAnimator(initialValue:repeating:content:keyframes:)](https://developer.apple.com/documentation/swiftui/view/keyframeanimator(initialvalue:repeating:content:keyframes:)) — Loops the given keyframes continuously, updating the view using the modifiers you apply in `body`.
- [keyframeAnimator(initialValue:trigger:content:keyframes:)](https://developer.apple.com/documentation/swiftui/view/keyframeanimator(initialvalue:trigger:content:keyframes:)) — Plays the given keyframes when the given trigger value changes, updating the view using the modifiers you apply in `body`.
- [KeyframeAnimator](https://developer.apple.com/documentation/swiftui/keyframeanimator) — A container that animates its content with keyframes.
- [Keyframes](https://developer.apple.com/documentation/swiftui/keyframes) — A type that defines changes to a value over time.
- [KeyframeTimeline](https://developer.apple.com/documentation/swiftui/keyframetimeline) — A description of how a value changes over time, modeled using keyframes.
- [KeyframeTrack](https://developer.apple.com/documentation/swiftui/keyframetrack) — A sequence of keyframes animating a single property of a root type.
- [KeyframeTrackContentBuilder](https://developer.apple.com/documentation/swiftui/keyframetrackcontentbuilder) — The builder that creates keyframe track content from the keyframes that you define within a closure.
- [KeyframesBuilder](https://developer.apple.com/documentation/swiftui/keyframesbuilder) — A builder that combines keyframe content values into a single value.
- [KeyframeTrackContent](https://developer.apple.com/documentation/swiftui/keyframetrackcontent) — A group of keyframes that define an interpolation curve of an animatable value.
- [CubicKeyframe](https://developer.apple.com/documentation/swiftui/cubickeyframe) — A keyframe that uses a cubic curve to smoothly interpolate between values.
- [LinearKeyframe](https://developer.apple.com/documentation/swiftui/linearkeyframe) — A keyframe that uses simple linear interpolation.
- [MoveKeyframe](https://developer.apple.com/documentation/swiftui/movekeyframe) — A keyframe that immediately moves to the given value without interpolating.
- [SpringKeyframe](https://developer.apple.com/documentation/swiftui/springkeyframe) — A keyframe that uses a spring function to interpolate to the given value.

## Creating custom animations {#Creating-custom-animations}

- [CustomAnimation](https://developer.apple.com/documentation/swiftui/customanimation) — A type that defines how an animatable value changes over time.
- [AnimationContext](https://developer.apple.com/documentation/swiftui/animationcontext) — Contextual values that a custom animation can use to manage state and access a view’s environment.
- [AnimationState](https://developer.apple.com/documentation/swiftui/animationstate) — A container that stores the state for a custom animation.
- [AnimationStateKey](https://developer.apple.com/documentation/swiftui/animationstatekey) — A key for accessing animation state values.
- [UnitCurve](https://developer.apple.com/documentation/swiftui/unitcurve) — A  function defined by a two-dimensional curve that maps an input progress in the range [0,1] to an output progress that is also in the range [0,1]. By changing the shape of the curve, the effective speed of an animation or other interpolation can be changed.
- [Spring](https://developer.apple.com/documentation/swiftui/spring) — A representation of a spring’s motion.

## Making data animatable {#Making-data-animatable}

- [Animatable](https://developer.apple.com/documentation/swiftui/animatable) — A type that describes how to animate a property of a view.
- [AnimatableValues](https://developer.apple.com/documentation/swiftui/animatablevalues)
- [AnimatablePair](https://developer.apple.com/documentation/swiftui/animatablepair) — A pair of animatable values, which is itself animatable.
- [VectorArithmetic](https://developer.apple.com/documentation/swiftui/vectorarithmetic) — A type that can serve as the animatable data of an animatable type.
- [EmptyAnimatableData](https://developer.apple.com/documentation/swiftui/emptyanimatabledata) — An empty type for animatable data.

## Updating a view on a schedule {#Updating-a-view-on-a-schedule}

- [Updating watchOS apps with timelines](https://developer.apple.com/documentation/watchos-apps/updating-watchos-apps-with-timelines) — Seamlessly schedule updates to your user interface, even while it’s inactive.
- [TimelineView](https://developer.apple.com/documentation/swiftui/timelineview) — A view that updates according to a schedule that you provide.
- [TimelineSchedule](https://developer.apple.com/documentation/swiftui/timelineschedule) — A type that provides a sequence of dates for use as a schedule.
- [TimelineViewDefaultContext](https://developer.apple.com/documentation/swiftui/timelineviewdefaultcontext) — Information passed to a timeline view’s content callback.

## Synchronizing geometries {#Synchronizing-geometries}

- [matchedGeometryEffect(id:in:properties:anchor:isSource:)](https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)) — Defines a group of views with synchronized geometry using an identifier and namespace that you provide.
- [MatchedGeometryProperties](https://developer.apple.com/documentation/swiftui/matchedgeometryproperties) — A set of view properties that may be synchronized between views using the `View.matchedGeometryEffect()` function.
- [GeometryEffect](https://developer.apple.com/documentation/swiftui/geometryeffect) — An effect that changes the visual appearance of a view, largely without changing its ancestors or descendants.
- [Namespace](https://developer.apple.com/documentation/swiftui/namespace) — A dynamic property type that allows access to a namespace defined by the persistent identity of the object containing the property (e.g. a view).
- [geometryGroup()](https://developer.apple.com/documentation/swiftui/view/geometrygroup()) — Isolates the geometry (e.g. position and size) of the view from its parent view.

## Defining transitions {#Defining-transitions}

- [transition(_:)](https://developer.apple.com/documentation/swiftui/view/transition(_:)) — Associates a transition with the view.
- [Transition](https://developer.apple.com/documentation/swiftui/transition) — A description of view changes to apply when a view is added to and removed from the view hierarchy.
- [TransitionProperties](https://developer.apple.com/documentation/swiftui/transitionproperties) — The properties a `Transition` can have.
- [TransitionPhase](https://developer.apple.com/documentation/swiftui/transitionphase) — An indication of which the current stage of a transition.
- [AsymmetricTransition](https://developer.apple.com/documentation/swiftui/asymmetrictransition) — A composite `Transition` that uses a different transition for insertion versus removal.
- [AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition) — A type-erased transition.
- [contentTransition(_:)](https://developer.apple.com/documentation/swiftui/view/contenttransition(_:)) — Modifies the view to use a given transition as its method of animating changes to the contents of its views.
- [contentTransition](https://developer.apple.com/documentation/swiftui/environmentvalues/contenttransition) — The current method of animating the contents of views.
- [contentTransitionAddsDrawingGroup](https://developer.apple.com/documentation/swiftui/environmentvalues/contenttransitionaddsdrawinggroup) — A Boolean value that controls whether views that render content transitions use GPU-accelerated rendering.
- [ContentTransition](https://developer.apple.com/documentation/swiftui/contenttransition) — A kind of transition that applies to the content within a single view, rather than to the insertion or removal of a view.
- [PlaceholderContentView](https://developer.apple.com/documentation/swiftui/placeholdercontentview) — A placeholder used to construct an inline modifier, transition, or other helper type.

## Defining matched transitions {#Defining-matched-transitions}

- [matchedTransitionSource(id:in:)](https://developer.apple.com/documentation/swiftui/view/matchedtransitionsource(id:in:)) — Identifies this view as the source of a navigation transition, such as a zoom transition.
- [matchedTransitionSource(id:in:configuration:)](https://developer.apple.com/documentation/swiftui/view/matchedtransitionsource(id:in:configuration:)) — Identifies this view as the source of a navigation transition, such as a zoom transition.
- [MatchedTransitionSourceConfiguration](https://developer.apple.com/documentation/swiftui/matchedtransitionsourceconfiguration) — A configuration that defines the appearance of a matched transition source.
- [EmptyMatchedTransitionSourceConfiguration](https://developer.apple.com/documentation/swiftui/emptymatchedtransitionsourceconfiguration) — An unstyled matched transition source configuration.

## Defining navigation transitions {#Defining-navigation-transitions}

- [navigationTransition(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtransition(_:)) — Sets the navigation transition style for this view.
- [NavigationTransition](https://developer.apple.com/documentation/swiftui/navigationtransition) — A type that defines the transition to use when navigating to a view.
- [AnyNavigationTransition](https://developer.apple.com/documentation/swiftui/anynavigationtransition) — A type-erasing navigation transition that allows for providing any navigation transition value dynamically.
- [CrossFadeNavigationTransition](https://developer.apple.com/documentation/swiftui/crossfadenavigationtransition) — A navigation transition that cross-fades between the appearing view and the disappearing view.

## Moving an animation to another view {#Moving-an-animation-to-another-view}

- [withTransaction(_:_:)](https://developer.apple.com/documentation/swiftui/withtransaction(_:_:)) — Executes a closure with the specified transaction and returns the result.
- [withTransaction(_:_:_:)](https://developer.apple.com/documentation/swiftui/withtransaction(_:_:_:)) — Executes a closure with the specified transaction key path and value and returns the result.
- [transaction(_:)](https://developer.apple.com/documentation/swiftui/view/transaction(_:)) — Applies the given transaction mutation function to all animations used within the view.
- [transaction(value:_:)](https://developer.apple.com/documentation/swiftui/view/transaction(value:_:)) — Applies the given transaction mutation function to all animations used within the view.
- [transaction(_:body:)](https://developer.apple.com/documentation/swiftui/view/transaction(_:body:)) — Applies the given transaction mutation function to all animations used within the `body` closure.
- [Transaction](https://developer.apple.com/documentation/swiftui/transaction) — The context of the current state-processing update.
- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) — Creates an environment values, transaction, container values, or focused values entry.
- [TransactionKey](https://developer.apple.com/documentation/swiftui/transactionkey) — A key for accessing values in a transaction.

## Deprecated types {#Deprecated-types}

- [AnimatableModifier](https://developer.apple.com/documentation/swiftui/animatablemodifier) — A modifier that can create another modifier with animation.
