+++
title = "2 环境值"
date = 2026-09-12T12:47:47+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/environment-values](https://developer.apple.com/documentation/swiftui/environment-values)

# 2 环境值

使用环境在整个视图层级中共享数据。

## 概述 {#Overview}

SwiftUI 中的视图可以响应它们通过 [Environment](https://developer.apple.com/documentation/swiftui/environment) 属性包装器从环境中读取的配置信息。

![](./images/environment-values-hero@2x.png)

视图从其容器视图继承环境，但可以被 [environment(_:_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:_:)) 视图修饰符显式改变，也可以被众多作用于环境值的修饰符隐式改变。因此，你可以通过修改某个视图组容器的环境，来配置整个视图层级。

你可以在 [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) 结构体中找到许多内置环境值。你也可以通过在环境值结构的扩展中定义新属性，并对该变量声明应用 [Entry()](https://developer.apple.com/documentation/swiftui/entry()) 宏，来创建自定义的 [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) 属性。

## 访问环境值 {#Accessing-environment-values}

- [Environment](https://developer.apple.com/documentation/swiftui/environment) —— 从视图环境中读取值的属性包装器。
- [EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) —— 在视图层级中传播的一组环境值。

## 创建自定义环境值 {#Creating-custom-environment-values}

- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) —— 创建环境值、事务、容器值或焦点值的条目。
- [EnvironmentKey](https://developer.apple.com/documentation/swiftui/environmentkey) —— 用于访问环境中值的键。

## 修改视图的环境 {#Modifying-the-environment-of-a-view}

- [environment(_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:)) —— 把一个可观察对象放入视图的环境中。
- [environment(_:_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:_:)) —— 把指定键路径的环境值设为给定值。
- [transformEnvironment(_:transform:)](https://developer.apple.com/documentation/swiftui/view/transformenvironment(_:transform:)) —— 用给定函数转换指定键路径的环境值。

## 修改场景的环境 {#Modifying-the-environment-of-a-scene}

- [environment(_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:)) —— 把一个可观察对象放入场景的环境中。
- [environment(_:_:)](https://developer.apple.com/documentation/swiftui/scene/environment(_:_:)) —— 把指定键路径的环境值设为给定值。
- [transformEnvironment(_:transform:)](https://developer.apple.com/documentation/swiftui/scene/transformenvironment(_:transform:)) —— 用给定函数转换指定键路径的环境值。
