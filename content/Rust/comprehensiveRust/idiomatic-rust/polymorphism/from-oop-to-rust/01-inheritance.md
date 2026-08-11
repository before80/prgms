+++
title = "4.2.1 继承"
date = 2026-08-11T11:30:00+08:00
weight = 481
type = "docs"
description = "01-继承 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/inheritance.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/inheritance.html)

# 4.2.1 继承

```cpp,editable
// 基类
class Vehicle {
public:
    void accelerate() { }
    void brake() { }
};

// 继承类
class Car : public Vehicle {
public:
    void honk() { }
};

int main() {
    Car myCar;                  // 创建 Car 对象
    myCar.accelerate();         // 继承的方法
    myCar.honk();               // Car 自己的方法
    myCar.brake();              // 继承的方法
    return 0;
}
```

> - 这应是对学员在其它语言中「继承是什么」的简短提醒。
>
> - 继承是一种机制：子类型获得它所继承的父类型的字段和方法。
>
> - 方法可按需被子类型覆盖（override）。
>
> - 可用 `super` 调用被继承类的方法。

