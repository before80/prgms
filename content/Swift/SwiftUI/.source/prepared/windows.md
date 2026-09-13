# Windows

Display user interface content in a window or a collection of windows.

## Overview {#Overview}

The most common way to present a view hierarchy in your app’s interface is with a [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup), which produces a platform-specific behavior and appearance.

![](./images/windows-hero@2x.png)

On platforms that support it, people can open multiple windows from the group simultaneously. Each window relies on the same root view definition, but retains its own view state. On some platforms, you can also supplement your app’s user interface with a single-instance window using the [Window](https://developer.apple.com/documentation/swiftui/window) scene type.

Configure windows using scene modifiers that you add to the window declaration, like [windowStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowstyle(_:)) or [defaultPosition(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultposition(_:)). You can also indicate how to configure new windows that you present from a view hierarchy by adding the [presentedWindowStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowstyle(_:)) view modifier to a view in the hierarchy.

For design guidance, see [Windows](https://developer.apple.com/design/human-interface-guidelines/windows) in the Human Interface Guidelines.

## Essentials {#Essentials}

- [Customizing window styles and state-restoration behavior in macOS](3.1-CustomizingWindowStylesAndStateRestorationBehaviorInMacos/) — Configure how your app’s windows look and function in macOS to provide an engaging and more coherent experience.
- [Bringing multiple windows to your SwiftUI app](3.2-BringingMultipleWindowsToYourSwiftuiApp/) — Compose rich views by reacting to state changes and customize your app’s scene presentation and behavior on iPadOS and macOS.

## Creating windows {#Creating-windows}

- [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup) — A scene that presents a group of identically structured windows.
- [Window](https://developer.apple.com/documentation/swiftui/window) — A scene that presents its content in a single, unique window.
- [UtilityWindow](https://developer.apple.com/documentation/swiftui/utilitywindow) — A specialized window scene that provides secondary utility to the content of the main scenes of an application.
- [WindowStyle](https://developer.apple.com/documentation/swiftui/windowstyle) — A specification for the appearance and interaction of a window.
- [windowStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowstyle(_:)) — Sets the style for windows created by this scene.

## Styling the associated toolbar {#Styling-the-associated-toolbar}

- [windowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarstyle(_:)) — Sets the style for the toolbar defined within this scene.
- [windowToolbarLabelStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarlabelstyle(_:)) — Sets the label style of items in a toolbar and enables user customization.
- [windowToolbarLabelStyle(fixed:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarlabelstyle(fixed:)) — Sets the label style of items in a toolbar.
- [WindowToolbarStyle](https://developer.apple.com/documentation/swiftui/windowtoolbarstyle) — A specification for the appearance and behavior of a window’s toolbar.

## Opening windows {#Opening-windows}

- [Presenting windows and spaces](https://developer.apple.com/documentation/visionos/presenting-windows-and-spaces) — Open and close the scenes that make up your app’s interface.
- [supportsMultipleWindows](https://developer.apple.com/documentation/swiftui/environmentvalues/supportsmultiplewindows) — A Boolean value that indicates whether the current platform supports opening multiple windows.
- [openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow) — A window presentation action stored in a view’s environment.
- [OpenWindowAction](https://developer.apple.com/documentation/swiftui/openwindowaction) — An action that presents a window.
- [PushWindowAction](https://developer.apple.com/documentation/swiftui/pushwindowaction) — An action that opens the requested window in place of the window the action is called from.

## Closing windows {#Closing-windows}

- [dismissWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisswindow) — A window dismissal action stored in a view’s environment.
- [DismissWindowAction](https://developer.apple.com/documentation/swiftui/dismisswindowaction) — An action that dismisses a window associated to a particular scene.
- [dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss) — An action that dismisses the current presentation.
- [DismissAction](https://developer.apple.com/documentation/swiftui/dismissaction) — An action that dismisses a presentation.
- [DismissBehavior](https://developer.apple.com/documentation/swiftui/dismissbehavior) — Programmatic window dismissal behaviors.

## Sizing a window {#Sizing-a-window}

- [Positioning and sizing windows](https://developer.apple.com/documentation/visionos/positioning-and-sizing-windows) — Influence the initial geometry of windows that your app presents.
- [defaultSize(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(_:)) — Sets a default size for a window.
- [defaultSize(width:height:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:)) — Sets a default width and height for a window.
- [defaultSize(width:height:depth:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:depth:)) — Sets a default size for a volumetric window.
- [defaultSize(_:in:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(_:in:)) — Sets a default size for a volumetric window.
- [defaultSize(width:height:depth:in:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:depth:in:)) — Sets a default size for a volumetric window.
- [windowResizability(_:)](https://developer.apple.com/documentation/swiftui/scene/windowresizability(_:)) — Sets the kind of resizability to use for a window.
- [WindowResizability](https://developer.apple.com/documentation/swiftui/windowresizability) — The resizability of a window.
- [windowIdealSize(_:)](https://developer.apple.com/documentation/swiftui/scene/windowidealsize(_:)) — Specifies how windows derived form this scene should determine their size when zooming.
- [WindowIdealSize](https://developer.apple.com/documentation/swiftui/windowidealsize) — A type which defines the size a window should use when zooming.

## Positioning a window {#Positioning-a-window}

- [defaultPosition(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultposition(_:)) — Sets a default position for a window.
- [WindowLevel](https://developer.apple.com/documentation/swiftui/windowlevel) — The level of a window.
- [windowLevel(_:)](https://developer.apple.com/documentation/swiftui/scene/windowlevel(_:)) — Sets the window level of this scene.
- [WindowLayoutRoot](https://developer.apple.com/documentation/swiftui/windowlayoutroot) — A proxy which represents the root contents of a window.
- [WindowPlacement](https://developer.apple.com/documentation/swiftui/windowplacement) — A type which represents a preferred size and position for a window.
- [defaultWindowPlacement(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultwindowplacement(_:)) — Defines a function used for determining the default placement of windows.
- [windowIdealPlacement(_:)](https://developer.apple.com/documentation/swiftui/scene/windowidealplacement(_:)) — Provides a function which determines a placement to use when windows of a scene zoom.
- [WindowPlacementContext](https://developer.apple.com/documentation/swiftui/windowplacementcontext) — A type which represents contextual information used for sizing and positioning windows.
- [WindowProxy](https://developer.apple.com/documentation/swiftui/windowproxy) — The proxy for an open window in the app.
- [DisplayProxy](https://developer.apple.com/documentation/swiftui/displayproxy) — A type which provides information about display hardware.

## Configuring window visibility {#Configuring-window-visibility}

- [WindowVisibilityToggle](https://developer.apple.com/documentation/swiftui/windowvisibilitytoggle) — A specialized button for toggling the visibility of a window.
- [defaultLaunchBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultlaunchbehavior(_:)) — Sets the default launch behavior for this scene.
- [restorationBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/restorationbehavior(_:)) — Sets the restoration behavior for this scene.
- [SceneLaunchBehavior](https://developer.apple.com/documentation/swiftui/scenelaunchbehavior) — The launch behavior for a scene.
- [SceneRestorationBehavior](https://developer.apple.com/documentation/swiftui/scenerestorationbehavior) — The restoration behavior for a scene.
- [persistentSystemOverlays(_:)](https://developer.apple.com/documentation/swiftui/scene/persistentsystemoverlays(_:)) — Sets the preferred visibility of the non-transient system views overlaying the app.
- [windowToolbarFullScreenVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/windowtoolbarfullscreenvisibility(_:)) — Configures the visibility of the window toolbar when the window enters full screen mode.
- [WindowToolbarFullScreenVisibility](https://developer.apple.com/documentation/swiftui/windowtoolbarfullscreenvisibility) — The visibility of the window toolbar with respect to full screen mode.

## Managing window behavior {#Managing-window-behavior}

- [WindowManagerRole](https://developer.apple.com/documentation/swiftui/windowmanagerrole) — Options for defining how a scene’s windows behave when used within a managed window context, such as full screen mode and Stage Manager.
- [windowManagerRole(_:)](https://developer.apple.com/documentation/swiftui/scene/windowmanagerrole(_:)) — Configures the role for windows derived from `self` when participating in a managed window context, such as full screen or Stage Manager.
- [WindowInteractionBehavior](https://developer.apple.com/documentation/swiftui/windowinteractionbehavior) — Options for enabling and disabling window interaction behaviors.
- [windowDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowdismissbehavior(_:)) — Configures the dismiss functionality for the window enclosing `self`.
- [windowFullScreenBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowfullscreenbehavior(_:)) — Configures the full screen functionality for the window enclosing `self`.
- [windowMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowminimizebehavior(_:)) — Configures the minimize functionality for the window enclosing `self`.
- [windowResizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowresizebehavior(_:)) — Configures the resize functionality for the window enclosing `self`.
- [windowBackgroundDragBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/windowbackgrounddragbehavior(_:)) — Configures the behavior of dragging a window by its background.
- [allowsWindowActivationEvents()](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents()) — Configures gestures in this view hierarchy to handle events that activate the containing window.
- [allowsWindowActivationEvents(_:)](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents(_:)) — Configures whether gestures in this view hierarchy can handle events that activate the containing window.

## Interacting with volumes {#Interacting-with-volumes}

- [onVolumeViewpointChange(updateStrategy:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onvolumeviewpointchange(updatestrategy:initial:_:)) — Adds an action to perform when the viewpoint of the volume changes.
- [supportedVolumeViewpoints(_:)](https://developer.apple.com/documentation/swiftui/view/supportedvolumeviewpoints(_:)) — Specifies which viewpoints are supported for the window bar and ornaments in a volume.
- [VolumeViewpointUpdateStrategy](https://developer.apple.com/documentation/swiftui/volumeviewpointupdatestrategy) — A type describing when the action provided to [onVolumeViewpointChange(updateStrategy:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onvolumeviewpointchange(updatestrategy:initial:_:)) should be called.
- [Viewpoint3D](https://developer.apple.com/documentation/swiftui/viewpoint3d) — A type describing what direction something is being viewed from.
- [SquareAzimuth](https://developer.apple.com/documentation/swiftui/squareazimuth) — A type describing what direction something is being viewed from along the horizontal plane and snapped to 4 directions.
- [WorldAlignmentBehavior](https://developer.apple.com/documentation/swiftui/worldalignmentbehavior) — A type representing the world alignment behavior for a scene.
- [volumeWorldAlignment(_:)](https://developer.apple.com/documentation/swiftui/scene/volumeworldalignment(_:)) — Specifies how a volume should be aligned when moved in the world.
- [WorldScalingBehavior](https://developer.apple.com/documentation/swiftui/worldscalingbehavior) — Specifies the scaling behavior a window should have within the world.
- [defaultWorldScaling(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultworldscaling(_:)) — Specify the world scaling behavior for the window.
- [WorldScalingCompensation](https://developer.apple.com/documentation/swiftui/worldscalingcompensation) — Indicates whether returned metrics will take dynamic scaling into account.
- [worldTrackingLimitations](https://developer.apple.com/documentation/swiftui/environmentvalues/worldtrackinglimitations) — The current limitations of the device tracking the user’s surroundings.
- [WorldTrackingLimitation](https://developer.apple.com/documentation/swiftui/worldtrackinglimitation) — A structure to represent limitations of tracking the user’s surroundings.
- [SurfaceSnappingInfo](https://developer.apple.com/documentation/swiftui/surfacesnappinginfo) — A type representing information about the window scenes snap state.

## Deprecated Types {#Deprecated-Types}

- [ControlActiveState](https://developer.apple.com/documentation/swiftui/controlactivestate) — The active appearance expected of controls in a window.
