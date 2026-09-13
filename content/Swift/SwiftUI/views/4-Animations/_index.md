+++
title = "4 动画"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/animations](https://developer.apple.com/documentation/swiftui/animations)

# 4 动画

响应状态变化创建平滑的视觉更新。

## 概述 {#Overview}

你告诉 SwiftUI 如何在不同的状态下绘制应用的用户界面，然后由 SwiftUI 在状态变化时负责更新界面。

![](./images/animations-hero@2x.png)

为避免状态变化时出现突兀的视觉过渡，请用下列方式之一添加动画：

- 在调用全局函数 [withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:)) 时改变状态，从而为该状态变化的所有视觉改动添加动画。
- 给视图应用 [animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:)) 视图修饰符，从而在特定值变化时为该视图添加动画。
- 使用绑定的 [animation(_:)](https://developer.apple.com/documentation/swiftui/binding/animation(_:)) 方法，为 [Binding](https://developer.apple.com/documentation/swiftui/binding) 的变化添加动画。

SwiftUI 会为许多内置视图修饰符产生的效果添加动画，例如设置缩放或不透明度的那些修饰符。你可以让自己的自定义视图遵循 [Animatable](https://developer.apple.com/documentation/swiftui/animatable) 协议，并把你想要添加动画的值告诉 SwiftUI，从而为其他值添加动画。

当某个带动画的状态变化导致视图被加入或移出视图层级时，你可以用 [AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition) 定义的内置过渡（例如 [slide](https://developer.apple.com/documentation/swiftui/anytransition/slide) 或 [scale](https://developer.apple.com/documentation/swiftui/anytransition/scale)）告诉 SwiftUI 该视图如何进入或离开。你也可以创建自定义过渡。

关于设计指导，参见 Human Interface Guidelines 中的[动态效果](https://developer.apple.com/design/human-interface-guidelines/motion)。

## 为动作添加基于状态的动画 {#Adding-state-based-animation-to-an-action}

- [withAnimation(_:_:)](https://developer.apple.com/documentation/swiftui/withanimation(_:_:)) —— 用所提供的动画重新计算视图 body，并返回结果。
- [withAnimation(_:completionCriteria:_:completion:)](https://developer.apple.com/documentation/swiftui/withanimation(_:completioncriteria:_:completion:)) —— 用所提供的动画重新计算视图 body 并返回结果，同时在所有动画完成时运行完成回调。
- [AnimationCompletionCriteria](https://developer.apple.com/documentation/swiftui/animationcompletioncriteria) —— 判定动画何时算作结束的标准。
- [Animation](https://developer.apple.com/documentation/swiftui/animation) —— 视图随时间变化的方式，用来从一种状态平滑过渡到另一种状态。

## 为视图添加基于状态的动画 {#Adding-state-based-animation-to-a-view}

- [animation(_:)](https://developer.apple.com/documentation/swiftui/view/animation(_:)) —— 当该视图变化时，对它应用给定的动画。
- [animation(_:value:)](https://developer.apple.com/documentation/swiftui/view/animation(_:value:)) —— 当指定值变化时，对该视图应用给定的动画。
- [animation(_:body:)](https://developer.apple.com/documentation/swiftui/view/animation(_:body:)) —— 对 `body` 闭包内所有可动画的值应用给定的动画。

## 创建基于阶段的动画 {#Creating-phase-based-animation}

- [控制动画的时序与运动](4.1-ControllingTheTimingAndMovementsOfYourAnimations/) —— 用阶段动画器和关键帧动画器构建更精细的可控动画。
- [phaseAnimator(_:content:animation:)](https://developer.apple.com/documentation/swiftui/view/phaseanimator(_:content:animation:)) —— 在一系列连续变化的阶段中，对你应用到视图上的效果添加动画。
- [phaseAnimator(_:trigger:content:animation:)](https://developer.apple.com/documentation/swiftui/view/phaseanimator(_:trigger:content:animation:)) —— 在一系列基于触发器变化的阶段中，对你应用到视图上的效果添加动画。
- [PhaseAnimator](https://developer.apple.com/documentation/swiftui/phaseanimator) —— 通过自动循环你提供的一组阶段来为其内容添加动画的容器，每个阶段定义动画中的一个离散步骤。

## 创建基于关键帧的动画 {#Creating-keyframe-based-animation}

- [keyframeAnimator(initialValue:repeating:content:keyframes:)](https://developer.apple.com/documentation/swiftui/view/keyframeanimator(initialvalue:repeating:content:keyframes:)) —— 连续循环给定的关键帧，并用你在 `body` 中应用的修饰符更新视图。
- [keyframeAnimator(initialValue:trigger:content:keyframes:)](https://developer.apple.com/documentation/swiftui/view/keyframeanimator(initialvalue:trigger:content:keyframes:)) —— 当给定触发值变化时播放给定的关键帧，并用你在 `body` 中应用的修饰符更新视图。
- [KeyframeAnimator](https://developer.apple.com/documentation/swiftui/keyframeanimator) —— 用关键帧为其内容添加动画的容器。
- [Keyframes](https://developer.apple.com/documentation/swiftui/keyframes) —— 定义某个值随时间变化的类型。
- [KeyframeTimeline](https://developer.apple.com/documentation/swiftui/keyframetimeline) —— 用关键帧建模的、对某个值如何随时间变化的描述。
- [KeyframeTrack](https://developer.apple.com/documentation/swiftui/keyframetrack) —— 为根类型的单个属性添加动画的一系列关键帧。
- [KeyframeTrackContentBuilder](https://developer.apple.com/documentation/swiftui/keyframetrackcontentbuilder) —— 从你在闭包中定义的关键帧创建关键帧轨道内容的构建器。
- [KeyframesBuilder](https://developer.apple.com/documentation/swiftui/keyframesbuilder) —— 把多个关键帧内容值组合成单个值的构建器。
- [KeyframeTrackContent](https://developer.apple.com/documentation/swiftui/keyframetrackcontent) —— 定义某个可动画值插值曲线的一组关键帧。
- [CubicKeyframe](https://developer.apple.com/documentation/swiftui/cubickeyframe) —— 使用三次曲线在值之间平滑插值的关键帧。
- [LinearKeyframe](https://developer.apple.com/documentation/swiftui/linearkeyframe) —— 使用简单线性插值的关键帧。
- [MoveKeyframe](https://developer.apple.com/documentation/swiftui/movekeyframe) —— 直接移动到给定值而不做插值的关键帧。
- [SpringKeyframe](https://developer.apple.com/documentation/swiftui/springkeyframe) —— 使用弹簧函数插值到给定值的关键帧。

## 创建自定义动画 {#Creating-custom-animations}

- [CustomAnimation](https://developer.apple.com/documentation/swiftui/customanimation) —— 定义某个可动画值如何随时间变化的类型。
- [AnimationContext](https://developer.apple.com/documentation/swiftui/animationcontext) —— 自定义动画可用于管理状态并访问视图环境的上下文值。
- [AnimationState](https://developer.apple.com/documentation/swiftui/animationstate) —— 为自定义动画存储状态的容器。
- [AnimationStateKey](https://developer.apple.com/documentation/swiftui/animationstatekey) —— 访问动画状态值的键。
- [UnitCurve](https://developer.apple.com/documentation/swiftui/unitcurve) —— 由二维曲线定义的函数，把 [0,1] 范围内的输入进度映射到同样在 [0,1] 范围内的输出进度。改变曲线形状即可改变动画或其他插值的实际速度。
- [Spring](https://developer.apple.com/documentation/swiftui/spring) —— 对弹簧运动的表示。

## 让数据可动画 {#Making-data-animatable}

- [Animatable](https://developer.apple.com/documentation/swiftui/animatable) —— 描述如何为视图的某个属性添加动画的类型。
- [AnimatableValues](https://developer.apple.com/documentation/swiftui/animatablevalues)
- [AnimatablePair](https://developer.apple.com/documentation/swiftui/animatablepair) —— 一对可动画的值，它本身也是可动画的。
- [VectorArithmetic](https://developer.apple.com/documentation/swiftui/vectorarithmetic) —— 可以充当可动画类型其可动画数据的类型。
- [EmptyAnimatableData](https://developer.apple.com/documentation/swiftui/emptyanimatabledata) —— 可动画数据的空类型。

## 按计划更新视图 {#Updating-a-view-on-a-schedule}

- [用时间线更新 watchOS 应用](https://developer.apple.com/documentation/watchos-apps/updating-watchos-apps-with-timelines) —— 无缝地为用户界面安排更新，即使它处于非活跃状态。
- [TimelineView](https://developer.apple.com/documentation/swiftui/timelineview) —— 按你提供的时间表更新的视图。
- [TimelineSchedule](https://developer.apple.com/documentation/swiftui/timelineschedule) —— 提供一串日期作为时间表的类型。
- [TimelineViewDefaultContext](https://developer.apple.com/documentation/swiftui/timelineviewdefaultcontext) —— 传给时间线视图内容回调的信息。

## 同步几何信息 {#Synchronizing-geometries}

- [matchedGeometryEffect(id:in:properties:anchor:isSource:)](https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)) —— 用你提供的标识符和命名空间定义一组几何信息同步的视图。
- [MatchedGeometryProperties](https://developer.apple.com/documentation/swiftui/matchedgeometryproperties) —— 一组可以用 `View.matchedGeometryEffect()` 函数在视图之间同步的视图属性。
- [GeometryEffect](https://developer.apple.com/documentation/swiftui/geometryeffect) —— 改变视图视觉外观的效果，基本不改变它的祖先或后代。
- [Namespace](https://developer.apple.com/documentation/swiftui/namespace) —— 允许访问某个命名空间的动态属性类型，该命名空间由包含该属性的对象（例如视图）的持久身份定义。
- [geometryGroup()](https://developer.apple.com/documentation/swiftui/view/geometrygroup()) —— 把视图的几何信息（例如位置和大小）与其父视图隔离。

## 定义过渡 {#Defining-transitions}

- [transition(_:)](https://developer.apple.com/documentation/swiftui/view/transition(_:)) —— 把一个过渡与该视图关联起来。
- [Transition](https://developer.apple.com/documentation/swiftui/transition) —— 对视图被加入或移出视图层级时要应用的视图改动的描述。
- [TransitionProperties](https://developer.apple.com/documentation/swiftui/transitionproperties) —— `Transition` 可以具有的属性。
- [TransitionPhase](https://developer.apple.com/documentation/swiftui/transitionphase) —— 对过渡当前阶段的指示。
- [AsymmetricTransition](https://developer.apple.com/documentation/swiftui/asymmetrictransition) —— 对插入和移除使用不同过渡的复合 `Transition`。
- [AnyTransition](https://developer.apple.com/documentation/swiftui/anytransition) —— 类型擦除的过渡。
- [contentTransition(_:)](https://developer.apple.com/documentation/swiftui/view/contenttransition(_:)) —— 修改视图，让它用给定的过渡作为其内容变化的动画方式。
- [contentTransition](https://developer.apple.com/documentation/swiftui/environmentvalues/contenttransition) —— 当前为视图内容添加动画的方式。
- [contentTransitionAddsDrawingGroup](https://developer.apple.com/documentation/swiftui/environmentvalues/contenttransitionaddsdrawinggroup) —— 控制渲染内容过渡的视图是否使用 GPU 加速渲染的布尔值。
- [ContentTransition](https://developer.apple.com/documentation/swiftui/contenttransition) —— 作用于单个视图内部内容、而不是视图插入或移除的过渡类型。
- [PlaceholderContentView](https://developer.apple.com/documentation/swiftui/placeholdercontentview) —— 用于构造内联修饰符、过渡或其他辅助类型的占位符。

## 定义匹配过渡 {#Defining-matched-transitions}

- [matchedTransitionSource(id:in:)](https://developer.apple.com/documentation/swiftui/view/matchedtransitionsource(id:in:)) —— 把该视图标识为导航过渡（例如缩放过渡）的来源。
- [matchedTransitionSource(id:in:configuration:)](https://developer.apple.com/documentation/swiftui/view/matchedtransitionsource(id:in:configuration:)) —— 把该视图标识为导航过渡（例如缩放过渡）的来源。
- [MatchedTransitionSourceConfiguration](https://developer.apple.com/documentation/swiftui/matchedtransitionsourceconfiguration) —— 定义匹配过渡来源外观的配置。
- [EmptyMatchedTransitionSourceConfiguration](https://developer.apple.com/documentation/swiftui/emptymatchedtransitionsourceconfiguration) —— 无样式的匹配过渡来源配置。

## 定义导航过渡 {#Defining-navigation-transitions}

- [navigationTransition(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtransition(_:)) —— 为该视图设置导航过渡样式。
- [NavigationTransition](https://developer.apple.com/documentation/swiftui/navigationtransition) —— 定义导航到某个视图时所用过渡的类型。
- [AnyNavigationTransition](https://developer.apple.com/documentation/swiftui/anynavigationtransition) —— 类型擦除的导航过渡，允许动态提供任意导航过渡值。
- [CrossFadeNavigationTransition](https://developer.apple.com/documentation/swiftui/crossfadenavigationtransition) —— 在出现的视图与消失的视图之间交叉淡入淡出的导航过渡。

## 把动画移到另一个视图 {#Moving-an-animation-to-another-view}

- [withTransaction(_:_:)](https://developer.apple.com/documentation/swiftui/withtransaction(_:_:)) —— 用指定的事务执行闭包并返回结果。
- [withTransaction(_:_:_:)](https://developer.apple.com/documentation/swiftui/withtransaction(_:_:_:)) —— 用指定的事务键路径和值执行闭包并返回结果。
- [transaction(_:)](https://developer.apple.com/documentation/swiftui/view/transaction(_:)) —— 把给定的事务变更函数应用到该视图内使用的所有动画。
- [transaction(value:_:)](https://developer.apple.com/documentation/swiftui/view/transaction(value:_:)) —— 把给定的事务变更函数应用到该视图内使用的所有动画。
- [transaction(_:body:)](https://developer.apple.com/documentation/swiftui/view/transaction(_:body:)) —— 把给定的事务变更函数应用到 `body` 闭包内使用的所有动画。
- [Transaction](https://developer.apple.com/documentation/swiftui/transaction) —— 当前状态处理更新的上下文。
- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) —— 创建环境值、事务、容器值或焦点值的条目。
- [TransactionKey](https://developer.apple.com/documentation/swiftui/transactionkey) —— 访问事务中值的键。

## 已弃用的类型 {#Deprecated-types}

- [AnimatableModifier](https://developer.apple.com/documentation/swiftui/animatablemodifier) —— 可以创建另一个带动画的修饰符的修饰符。
