+++
title = "Rust 设计模式"
date = 2026-08-18T22:10:00+08:00
weight = 1
type = "docs"
description = "Rust Design Patterns（Rust 设计模式）"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/intro.html](https://rust-unofficial.github.io/patterns/intro.html)

# Rust 设计模式

一本关于 Rust 惯用法、设计模式与反模式的开源手册。

源码仓库：[https://github.com/rust-unofficial/patterns](https://github.com/rust-unofficial/patterns)

在线阅读：[https://rust-unofficial.github.io/patterns/](https://rust-unofficial.github.io/patterns/)

## 章节导航

- [引言](introduction/)
  - [01-译本](introduction/01-translations/)
- [第1章 惯用法](idioms/)
  - [01-参数使用借用类型](idioms/01-use-borrowed-types-for-arguments/)
  - [02-用 format! 拼接字符串](idioms/02-concatenating-strings-with-format/)
  - [03-构造器](idioms/03-constructor/)
  - [04-Default Trait](idioms/04-the-default-trait/)
  - [05-集合是智能指针](idioms/05-collections-are-smart-pointers/)
  - [06-析构器中的收尾](idioms/06-finalisation-in-destructors/)
  - [07-`mem::{take(_), replace(_)}`](idioms/07-mem-take-replace/)
  - [08-栈上动态分发](idioms/08-on-stack-dynamic-dispatch/)
  - [09-外部函数接口（FFI）](idioms/09-foreign-function-interface-ffi/)
    - [01-地道的错误处理](idioms/09-foreign-function-interface-ffi/01-idiomatic-errors/)
    - [02-接受字符串](idioms/09-foreign-function-interface-ffi/02-accepting-strings/)
    - [03-传递字符串](idioms/09-foreign-function-interface-ffi/03-passing-strings/)
  - [10-遍历 Option](idioms/10-iterating-over-an-option/)
  - [11-向闭包传递变量](idioms/11-pass-variables-to-closure/)
  - [12-用私有性保证可扩展性](idioms/12-privacy-for-extensibility/)
  - [13-简便的文档初始化](idioms/13-easy-doc-initialization/)
  - [14-临时可变性](idioms/14-temporary-mutability/)
  - [15-出错时归还已消耗的参数](idioms/15-return-consumed-arg-on-error/)
- [第2章 设计模式](design-patterns/)
  - [01-行为型](design-patterns/01-behavioural/)
    - [01-命令](design-patterns/01-behavioural/01-command/)
    - [02-解释器](design-patterns/01-behavioural/02-interpreter/)
    - [03-Newtype](design-patterns/01-behavioural/03-newtype/)
    - [04-RAII 守卫](design-patterns/01-behavioural/04-raii-guards/)
    - [05-策略](design-patterns/01-behavioural/05-strategy/)
    - [06-访问者](design-patterns/01-behavioural/06-visitor/)
  - [02-创建型](design-patterns/02-creational/)
    - [01-构建器](design-patterns/02-creational/01-builder/)
    - [02-Fold](design-patterns/02-creational/02-fold/)
  - [03-结构型](design-patterns/03-structural/)
    - [01-组合结构体](design-patterns/03-structural/01-compose-structs/)
    - [02-偏好小型 crate](design-patterns/03-structural/02-prefer-small-crates/)
    - [03-把不安全封装在小模块中](design-patterns/03-structural/03-contain-unsafety-in-small-modules/)
    - [04-用自定义 trait 避免复杂类型约束](design-patterns/03-structural/04-avoid-complex-type-bounds-with-custom-traits/)
  - [04-外部函数接口（FFI）](design-patterns/04-foreign-function-interface-ffi/)
    - [01-基于对象的 API](design-patterns/04-foreign-function-interface-ffi/01-object-based-apis/)
    - [02-将类型收拢到包装器中](design-patterns/04-foreign-function-interface-ffi/02-type-consolidation-into-wrappers/)
- [第3章 反模式](anti-patterns/)
  - [01-为通过借用检查而 Clone](anti-patterns/01-clone-to-satisfy-the-borrow-checker/)
  - [02-`#[deny(warnings)]`](anti-patterns/02-deny-warnings/)
  - [03-Deref 多态](anti-patterns/03-deref-polymorphism/)
- [第4章 函数式编程](functional-programming/)
  - [01-编程范式](functional-programming/01-programming-paradigms/)
  - [02-用泛型模拟类型类](functional-programming/02-generics-as-type-classes/)
  - [03-函数式光学](functional-programming/03-functional-optics/)
- [第5章 更多资源](additional-resources/)
  - [01-设计原则](additional-resources/01-design-principles/)
