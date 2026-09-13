+++
title = "3 窗口"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/windows](https://developer.apple.com/documentation/swiftui/windows)

# 3 窗口

在窗口或一组窗口中显示界面内容。

## 概述 {#Overview}

在应用界面中呈现视图层级最常见的方式是使用 [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup)，它会依据平台产生相应的行为与外观。

![](./images/windows-hero@2x.png)

在支持多个窗口的平台上，人们可以从同一个组同时打开多个窗口。每个窗口都基于相同的根视图定义，但各自保留自己的视图状态。在某些平台上，你还可以用 [Window](https://developer.apple.com/documentation/swiftui/window) 场景类型，为应用界面补充一个单实例窗口。

通过向窗口声明添加场景修饰符来配置窗口，例如 [windowStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowstyle(_:)) 或 [defaultPosition(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultposition(_:))。你也可以给视图层级中的某个视图添加 [presentedWindowStyle(_:)](https://developer.apple.com/documentation/swiftui/view/presentedwindowstyle(_:)) 视图修饰符，以此指明如何配置从该视图层级呈现的新窗口。

关于设计指导，参见 Human Interface Guidelines 中的[窗口](https://developer.apple.com/design/human-interface-guidelines/windows)。

## 基础 {#Essentials}

- [在 macOS 中自定义窗口样式与状态恢复行为](3.1-CustomizingWindowStylesAndStateRestorationBehaviorInMacos/) —— 配置应用窗口在 macOS 中的外观与行为，提供更有吸引力、更连贯的体验。
- [为 SwiftUI 应用引入多个窗口](3.2-BringingMultipleWindowsToYourSwiftuiApp/) —— 通过响应状态变化来组合丰富的视图，并在 iPadOS 和 macOS 上定制应用的场景呈现与行为。

## 创建窗口 {#Creating-windows}

- [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup) —— 呈现一组结构相同的窗口的场景。
- [Window](https://developer.apple.com/documentation/swiftui/window) —— 在单个唯一窗口中呈现其内容的场景。
- [UtilityWindow](https://developer.apple.com/documentation/swiftui/utilitywindow) —— 一种专门的窗口场景，为应用主要场景的内容提供辅助工具。
- [WindowStyle](https://developer.apple.com/documentation/swiftui/windowstyle) —— 对窗口外观与交互方式的规范说明。
- [windowStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowstyle(_:)) —— 设置由该场景创建的窗口的样式。

## 设置关联工具栏的样式 {#Styling-the-associated-toolbar}

- [windowToolbarStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarstyle(_:)) —— 设置该场景内所定义工具栏的样式。
- [windowToolbarLabelStyle(_:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarlabelstyle(_:)) —— 设置工具栏中各项的标签样式，并启用用户自定义。
- [windowToolbarLabelStyle(fixed:)](https://developer.apple.com/documentation/swiftui/scene/windowtoolbarlabelstyle(fixed:)) —— 设置工具栏中各项的标签样式。
- [WindowToolbarStyle](https://developer.apple.com/documentation/swiftui/windowtoolbarstyle) —— 对窗口工具栏外观与行为的规范说明。

## 打开窗口 {#Opening-windows}

- [呈现窗口与空间](https://developer.apple.com/documentation/visionos/presenting-windows-and-spaces) —— 打开和关闭构成应用界面的各个场景。
- [supportsMultipleWindows](https://developer.apple.com/documentation/swiftui/environmentvalues/supportsmultiplewindows) —— 一个布尔值，表示当前平台是否支持打开多个窗口。
- [openWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/openwindow) —— 存储在视图环境中的窗口呈现动作。
- [OpenWindowAction](https://developer.apple.com/documentation/swiftui/openwindowaction) —— 呈现窗口的动作。
- [PushWindowAction](https://developer.apple.com/documentation/swiftui/pushwindowaction) —— 在调用该动作的窗口位置打开所请求窗口的动作。

## 关闭窗口 {#Closing-windows}

- [dismissWindow](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisswindow) —— 存储在视图环境中的窗口关闭动作。
- [DismissWindowAction](https://developer.apple.com/documentation/swiftui/dismisswindowaction) —— 关闭与某个特定场景关联的窗口的动作。
- [dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss) —— 关闭当前呈现的动作。
- [DismissAction](https://developer.apple.com/documentation/swiftui/dismissaction) —— 关闭呈现的动作。
- [DismissBehavior](https://developer.apple.com/documentation/swiftui/dismissbehavior) —— 以编程方式关闭窗口的行为。

## 调整窗口大小 {#Sizing-a-window}

- [定位与调整窗口大小](https://developer.apple.com/documentation/visionos/positioning-and-sizing-windows) —— 影响应用所呈现窗口的初始几何形状。
- [defaultSize(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(_:)) —— 设置窗口的默认大小。
- [defaultSize(width:height:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:)) —— 设置窗口的默认宽度和高度。
- [defaultSize(width:height:depth:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:depth:)) —— 设置体（volumetric）窗口的默认大小。
- [defaultSize(_:in:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(_:in:)) —— 设置体窗口的默认大小。
- [defaultSize(width:height:depth:in:)](https://developer.apple.com/documentation/swiftui/scene/defaultsize(width:height:depth:in:)) —— 设置体窗口的默认大小。
- [windowResizability(_:)](https://developer.apple.com/documentation/swiftui/scene/windowresizability(_:)) —— 设置窗口使用的可调整大小方式。
- [WindowResizability](https://developer.apple.com/documentation/swiftui/windowresizability) —— 窗口的可调整大小特性。
- [windowIdealSize(_:)](https://developer.apple.com/documentation/swiftui/scene/windowidealsize(_:)) —— 指定从该场景派生的窗口在缩放时应如何确定大小。
- [WindowIdealSize](https://developer.apple.com/documentation/swiftui/windowidealsize) —— 定义窗口缩放时所应使用大小的类型。

## 定位窗口 {#Positioning-a-window}

- [defaultPosition(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultposition(_:)) —— 设置窗口的默认位置。
- [WindowLevel](https://developer.apple.com/documentation/swiftui/windowlevel) —— 窗口的层级。
- [windowLevel(_:)](https://developer.apple.com/documentation/swiftui/scene/windowlevel(_:)) —— 设置该场景的窗口层级。
- [WindowLayoutRoot](https://developer.apple.com/documentation/swiftui/windowlayoutroot) —— 表示窗口根内容的代理。
- [WindowPlacement](https://developer.apple.com/documentation/swiftui/windowplacement) —— 表示窗口偏好的大小与位置的类型。
- [defaultWindowPlacement(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultwindowplacement(_:)) —— 定义一个用于确定窗口默认放置位置的函数。
- [windowIdealPlacement(_:)](https://developer.apple.com/documentation/swiftui/scene/windowidealplacement(_:)) —— 提供一个函数，用于确定某个场景的窗口缩放时应采用的放置位置。
- [WindowPlacementContext](https://developer.apple.com/documentation/swiftui/windowplacementcontext) —— 表示用于调整和定位窗口的上下文信息的类型。
- [WindowProxy](https://developer.apple.com/documentation/swiftui/windowproxy) —— 应用中某个已打开窗口的代理。
- [DisplayProxy](https://developer.apple.com/documentation/swiftui/displayproxy) —— 提供显示硬件相关信息的类型。

## 配置窗口可见性 {#Configuring-window-visibility}

- [WindowVisibilityToggle](https://developer.apple.com/documentation/swiftui/windowvisibilitytoggle) —— 用于切换窗口可见性的专门按钮。
- [defaultLaunchBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultlaunchbehavior(_:)) —— 设置该场景的默认启动行为。
- [restorationBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/restorationbehavior(_:)) —— 设置该场景的恢复行为。
- [SceneLaunchBehavior](https://developer.apple.com/documentation/swiftui/scenelaunchbehavior) —— 场景的启动行为。
- [SceneRestorationBehavior](https://developer.apple.com/documentation/swiftui/scenerestorationbehavior) —— 场景的恢复行为。
- [persistentSystemOverlays(_:)](https://developer.apple.com/documentation/swiftui/scene/persistentsystemoverlays(_:)) —— 设置覆盖在应用之上、非瞬态系统视图的偏好可见性。
- [windowToolbarFullScreenVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/windowtoolbarfullscreenvisibility(_:)) —— 配置窗口进入全屏模式时窗口工具栏的可见性。
- [WindowToolbarFullScreenVisibility](https://developer.apple.com/documentation/swiftui/windowtoolbarfullscreenvisibility) —— 窗口工具栏相对于全屏模式的可见性。

## 管理窗口行为 {#Managing-window-behavior}

- [WindowManagerRole](https://developer.apple.com/documentation/swiftui/windowmanagerrole) —— 定义场景窗口在受管理的窗口上下文（例如全屏模式和「舞台管理器」）中如何表现的选项。
- [windowManagerRole(_:)](https://developer.apple.com/documentation/swiftui/scene/windowmanagerrole(_:)) —— 配置从 `self` 派生的窗口在参与受管理的窗口上下文（例如全屏或「舞台管理器」）时的角色。
- [WindowInteractionBehavior](https://developer.apple.com/documentation/swiftui/windowinteractionbehavior) —— 用于启用和禁用窗口交互行为的选项。
- [windowDismissBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowdismissbehavior(_:)) —— 配置包含 `self` 的窗口的关闭功能。
- [windowFullScreenBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowfullscreenbehavior(_:)) —— 配置包含 `self` 的窗口的全屏功能。
- [windowMinimizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowminimizebehavior(_:)) —— 配置包含 `self` 的窗口的最小化功能。
- [windowResizeBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/windowresizebehavior(_:)) —— 配置包含 `self` 的窗口的调整大小功能。
- [windowBackgroundDragBehavior(_:)](https://developer.apple.com/documentation/swiftui/scene/windowbackgrounddragbehavior(_:)) —— 配置通过窗口背景拖动窗口时的行为。
- [allowsWindowActivationEvents()](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents()) —— 配置该视图层级中的手势，使其能处理激活所在窗口的事件。
- [allowsWindowActivationEvents(_:)](https://developer.apple.com/documentation/swiftui/view/allowswindowactivationevents(_:)) —— 配置该视图层级中的手势能否处理激活所在窗口的事件。

## 与立体空间交互 {#Interacting-with-volumes}

- [onVolumeViewpointChange(updateStrategy:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onvolumeviewpointchange(updatestrategy:initial:_:)) —— 添加当立体空间的视点发生变化时要执行的动作。
- [supportedVolumeViewpoints(_:)](https://developer.apple.com/documentation/swiftui/view/supportedvolumeviewpoints(_:)) —— 指定立体空间中窗口栏和装饰件支持哪些视点。
- [VolumeViewpointUpdateStrategy](https://developer.apple.com/documentation/swiftui/volumeviewpointupdatestrategy) —— 描述何时应当调用传给 [onVolumeViewpointChange(updateStrategy:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onvolumeviewpointchange(updatestrategy:initial:_:)) 的动作的类型。
- [Viewpoint3D](https://developer.apple.com/documentation/swiftui/viewpoint3d) —— 描述某物正从哪个方向被观察的类型。
- [SquareAzimuth](https://developer.apple.com/documentation/swiftui/squareazimuth) —— 描述某物在水平面上从哪个方向被观察、并对齐到 4 个方向的类型。
- [WorldAlignmentBehavior](https://developer.apple.com/documentation/swiftui/worldalignmentbehavior) —— 表示场景世界对齐行为的类型。
- [volumeWorldAlignment(_:)](https://developer.apple.com/documentation/swiftui/scene/volumeworldalignment(_:)) —— 指定立体空间在世界中移动时应如何对齐。
- [WorldScalingBehavior](https://developer.apple.com/documentation/swiftui/worldscalingbehavior) —— 指定窗口在世界上应具有的缩放行为。
- [defaultWorldScaling(_:)](https://developer.apple.com/documentation/swiftui/scene/defaultworldscaling(_:)) —— 指定窗口的世界缩放行为。
- [WorldScalingCompensation](https://developer.apple.com/documentation/swiftui/worldscalingcompensation) —— 表示返回的度量值是否会考虑动态缩放。
- [worldTrackingLimitations](https://developer.apple.com/documentation/swiftui/environmentvalues/worldtrackinglimitations) —— 设备追踪用户周围环境的当前限制。
- [WorldTrackingLimitation](https://developer.apple.com/documentation/swiftui/worldtrackinglimitation) —— 表示追踪用户周围环境所存限制的结构体。
- [SurfaceSnappingInfo](https://developer.apple.com/documentation/swiftui/surfacesnappinginfo) —— 表示窗口场景吸附状态相关信息的类型。

## 已弃用的类型 {#Deprecated-Types}

- [ControlActiveState](https://developer.apple.com/documentation/swiftui/controlactivestate) —— 窗口中控件预期的活动外观。
