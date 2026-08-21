+++
title = "01-设计原则"
date = 2026-08-18T22:10:00+08:00
weight = 51
type = "docs"
description = "设计原则 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/additional_resources/design-principles.html](https://rust-unofficial.github.io/patterns/additional_resources/design-principles.html)

# 设计原则

## 常见设计原则概览 {#a-brief-overview-over-common-design-principles}

---

## [SOLID](https://en.wikipedia.org/wiki/SOLID) {#solid}

- [单一职责原则（SRP）](https://en.wikipedia.org/wiki/Single-responsibility_principle)：
  一个类应只有单一职责，也就是说，只有软件规格说明中某一部分的变更应能影响该类的规格说明。
- [开闭原则（OCP）](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)：
  「软件实体……应对扩展开放，对修改封闭。」
- [里氏替换原则（LSP）](https://en.wikipedia.org/wiki/Liskov_substitution_principle)：
  「程序中的对象应可替换为其子类型的实例，而不改变该程序的正确性。」
- [接口隔离原则（ISP）](https://en.wikipedia.org/wiki/Interface_segregation_principle)：
  「多个面向客户端的特定接口优于一个通用接口。」
- [依赖倒置原则（DIP）](https://en.wikipedia.org/wiki/Dependency_inversion_principle)：
  人们应当「依赖于抽象，[而非] 具体。」

## [CRP（组合复用原则）或组合优于继承](https://en.wikipedia.org/wiki/Composition_over_inheritance) {#crp-composite-reuse-principle-or-composition-over-inheritance}

「该原则主张：类应通过组合（包含实现所需功能的其他类的实例）而非从基类或父类继承，来偏好多态行为与代码复用」——
Knoernschild, Kirk (2002). Java Design - Objects, UML, and Process

## [DRY（不要重复自己）](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) {#dry-dont-repeat-yourself}

「系统中的每一条知识都必须有单一、明确、权威的表示」

## [KISS 原则](https://en.wikipedia.org/wiki/KISS_principle) {#kiss-principle}

多数系统在保持简单而非变得复杂时工作得最好；
因此，简单性应是设计的关键目标，应避免不必要的复杂性

## [迪米特法则（LoD）](https://en.wikipedia.org/wiki/Law_of_Demeter) {#law-of-demeter-lod}

给定对象应对其他任何事物（包括其子组件）的结构或属性做尽可能少的假设，以符合「信息隐藏」原则

## [契约式设计（DbC）](https://en.wikipedia.org/wiki/Design_by_contract) {#design-by-contract-dbc}

软件设计者应为软件组件定义形式化、精确且可验证的接口规格说明，它们在抽象数据类型的普通定义之上扩展了前置条件、后置条件与不变量

## [封装](https://en.wikipedia.org/wiki/Encapsulation_(computer_programming)) {#encapsulationhttpsenwikipediaorgwikiencapsulation-computer-programming}

将数据与操作这些数据的方法捆绑在一起，或限制对对象某些组件的直接访问。封装用于把结构化数据对象的值或状态隐藏在类内部，防止未授权方直接访问它们。

## [命令查询分离（CQS）](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation) {#command-query-separation-cqs}

「函数不应产生抽象副作用……只有命令（过程）才被允许产生副作用。」——Bertrand Meyer: Object-Oriented
Software Construction

## [最少惊讶原则（POLA）](https://en.wikipedia.org/wiki/Principle_of_least_astonishment) {#principle-of-least-astonishment-pola}

系统中的组件应以多数用户会预期的方式表现。其行为不应令用户惊讶或意外

## 语言模块单元 {#linguistic-modular-units}

「模块必须对应于所用语言中的句法单元。」——Bertrand
Meyer: Object-Oriented Software Construction

## 自文档化 {#self-documentation}

「模块的设计者应努力使关于该模块的所有信息都成为模块本身的一部分。」——Bertrand Meyer: Object-Oriented Software
Construction

## 统一访问 {#uniform-access}

「模块提供的所有服务都应通过统一的记法可用，该记法不泄露它们是通过存储还是通过计算实现的。」——Bertrand Meyer: Object-Oriented Software Construction

## 单一选择 {#single-choice}

「每当软件系统必须支持一组备选方案时，系统中有且仅有一个模块应知道它们的穷尽列表。」——Bertrand Meyer:
Object-Oriented Software Construction

## 持久化闭包 {#persistence-closure}

「每当存储机制存储一个对象时，它必须连同该对象的依赖一并存储。每当检索机制检索先前存储的对象时，它也必须检索任何尚未检索的该对象的依赖。」——Bertrand Meyer: Object-Oriented Software Construction
