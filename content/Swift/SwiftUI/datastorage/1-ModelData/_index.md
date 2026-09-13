+++
title = "1 模型数据"
date = 2026-09-12T12:47:47+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/model-data](https://developer.apple.com/documentation/swiftui/model-data)

# 1 模型数据

管理驱动应用界面的数据。

## 概述 {#Overview}

SwiftUI 提供了一种声明式的用户界面设计方式。当你组合视图层级时，也同时指明了各个视图的数据依赖。当数据发生变化时——无论是外部事件引起的，还是用户执行某个操作引起的——SwiftUI 都会自动更新界面中受影响的部分。因此，框架会自动完成视图控制器传统上所做的大部分工作。

![](./images/model-data-hero@2x.png)

框架提供了状态变量和绑定等工具，用来把应用的数据连接到用户界面。这些工具有助于你为应用中的每一份数据维护单一数据源，部分原因在于它们减少了你需要编写的胶水逻辑。请选择最适合你手头任务的工具：

- 通过把值类型包装为 [State()](https://developer.apple.com/documentation/swiftui/state()) 属性，在视图内部本地管理临时的界面状态。
- 用 [Binding](https://developer.apple.com/documentation/swiftui/binding) 属性包装器共享对某个数据源（例如本地状态）的引用。
- 把 [Observable()](https://developer.apple.com/documentation/observation/observable()) 宏应用到模型数据类型上，从而在视图中连接并观察引用类型的模型数据。用 [State()](https://developer.apple.com/documentation/swiftui/state()) 属性在视图中直接实例化可观察的模型数据类型。用 [Environment](https://developer.apple.com/documentation/swiftui/environment) 属性包装器把可观察的模型数据共享给层级中的其他视图，而无需传递引用。

## 创建与共享视图状态 {#Creating-and-sharing-view-state}

- [管理用户界面状态](1.1-ManagingUserInterfaceState/) —— 把视图特有的数据封装在应用的视图层级内，让你的视图可复用。
- [State()](https://developer.apple.com/documentation/swiftui/state()) —— 创建一个可以读写由 SwiftUI 管理的值的属性。
- [State(initialValue:)](https://developer.apple.com/documentation/swiftui/state(initialvalue:)) —— 创建一个带初始值、可以读写由 SwiftUI 管理的值的属性。
- [State(wrappedValue:)](https://developer.apple.com/documentation/swiftui/state(wrappedvalue:)) —— 创建一个带被包装值、可以读写由 SwiftUI 管理的值的属性。
- [State](https://developer.apple.com/documentation/swiftui/state) —— 可以读写由 SwiftUI 管理的值的属性包装器类型。
- [Bindable](https://developer.apple.com/documentation/swiftui/bindable) —— 支持为可观察对象的可变属性创建绑定的属性包装器类型。
- [Binding](https://developer.apple.com/documentation/swiftui/binding) —— 可以读写由某个数据源拥有的值的属性包装器类型。

## 创建模型数据 {#Creating-model-data}

- [在应用中管理模型数据](1.3-ManagingModelDataInYourApp/) —— 在应用的数据模型与视图之间建立连接。
- [从 Observable Object 协议迁移到 Observable 宏](1.4-MigratingFromTheObservableObjectProtocolToTheObservableMacro/) —— 更新你已有的应用，以利用 Swift 中 Observation 的好处。
- [Observable()](https://developer.apple.com/documentation/observation/observable()) —— 定义并实现 Observable 协议的遵循性。
- [监控应用中的数据变化](1.5-MonitoringModelDataChangesInYourApp/) —— 使用可观察对象在应用的用户界面中显示数据变化。
- [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) —— 实例化可观察对象的属性包装器类型。
- [ObservedObject](https://developer.apple.com/documentation/swiftui/observedobject) —— 订阅可观察对象、并在该对象变化时使视图失效的属性包装器类型。
- [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) —— 带有发布者、在对象变化之前发出事件的对象类型。

## 响应数据变化 {#Responding-to-data-changes}

- [onChange(of:initial:_:)](https://developer.apple.com/documentation/swiftui/view/onchange(of:initial:_:)) —— 为该视图添加修饰符，在某个特定值变化时触发一个动作。
- [onReceive(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onreceive(_:perform:)) —— 添加当该视图检测到给定发布者发出的数据时要执行的动作。

## 在整个应用中分发模型数据 {#Distributing-model-data-throughout-your-app}

- [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/view/environmentobject(_:)) —— 为视图层级提供一个可观察对象。
- [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/scene/environmentobject(_:)) —— 为视图子层级提供一个 `ObservableObject`。
- [EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject) —— 由父视图或祖先视图提供的、针对可观察对象的属性包装器类型。

## 管理动态数据 {#Managing-dynamic-data}

- [DynamicProperty](https://developer.apple.com/documentation/swiftui/dynamicproperty) —— 用于更新视图外部属性的存储变量的接口。
