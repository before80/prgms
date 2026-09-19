+++
title = "第17章 结构体与值语义：复制之后互不打扰"
weight = 170
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十七章：结构体与值语义：复制之后互不打扰

> 结构体是 Swift 写业务模型时最常拿起的工具。原因不是它“比类快”这种口号，而是它默认带来清晰的复制语义：把值交给别人之后，对方改自己的副本，不会顺手改坏你手里的那份。

## 17.1 定义与成员逐一初始化

定义一个结构体，要做的只是把它的存储属性列出来：

```swift
struct Point {
    var x: Int
    var y: Int
}

let origin = Point(x: 0, y: 0)
var point = Point(x: 3, y: 4)
print(origin.x, point.y)
// prints: 0 4
```

结构体自动获得成员逐一初始化器 `init(x:y:)`，参数顺序和属性声明顺序一致。只要没有自定义初始化器，编译器就会生成它。

这个初始化器还能“变形”：属性有初值时对应参数会带默认值，全部属性都有初值时 `Point()` 直接可用，而 `private` 属性会改变它的可见性。这些变化连同只读计算属性、观察器隐式参数名、`Self` 等写法，集中在第 15B.6 节。

## 17.2 值语义：赋值得到新的一份

上面的定义里一个字都没提“复制”，但复制确实发生了。看这段：

```swift
var a = Point(x: 1, y: 2)
var b = a
b.x = 99

print(a.x, b.x)
// prints: 1 99
```

`b = a` 之后，`b` 拥有独立的一份值。修改 `b` 不会影响 `a`。函数传参时也一样：

```swift
func moveRight(_ point: Point) -> Point {
    var copy = point
    copy.x += 1
    return copy
}

let start = Point(x: 0, y: 0)
let end = moveRight(start)
print(start.x, end.x)
// prints: 0 1
```

参数 `point` 是常量，不能直接改它的属性；想改就先复制成 `var`，或者把方法写成 `mutating`。

## 17.3 `mutating` 方法：原地修改值

结构体方法只有标记为 `mutating` 才能修改属性：

```swift
struct Counter {
    var value = 0

    mutating func increment() {
        value += 1
    }

    mutating func add(_ amount: Int) {
        self.value += amount
    }
}

var counter = Counter()
counter.increment()
counter.add(4)
print(counter.value)
// prints: 5
```

为什么需要 `mutating`？因为结构体方法默认把 `self` 当成不可变值。`mutating` 明确告诉编译器：调用这个方法会改变实例本身。

常量实例不能调用 `mutating` 方法：

```swift
let fixed = Counter()
// fixed.increment()   // 编译错误
```

## 17.4 常量结构体与可变属性的关系

结构体实例声明为 `let` 后，即使属性是 `var`，也不能修改：

```swift
struct Settings {
    var volume = 50
}

let settings = Settings()
// settings.volume = 60   // 编译错误
```

这和类不同。类实例的 `let` 只锁住引用本身，不锁住对象的属性。结构体的 `let` 锁住的是整个值。

## 17.5 自定义初始化器

自定义初始化器会替代自动生成的成员逐一初始化器：

```swift
struct Temperature {
    var celsius: Double

    init(celsius: Double) {
        self.celsius = celsius
    }

    init(fahrenheit: Double) {
        self.celsius = (fahrenheit - 32) * 5 / 9
    }
}

let t1 = Temperature(celsius: 25)
let t2 = Temperature(fahrenheit: 77)
print(t1.celsius, t2.celsius)
// prints: 25.0 25.0
```

如果还想要成员逐一初始化器，可以把它放到扩展里，或者不自定义初始化器。初始化器不能像普通方法那样用 `.init` 链随意转弯，必须保证所有存储属性在结束时都有值。

## 17.6 嵌套的值语义

结构体嵌套结构体时，复制会沿着整棵值树进行：

```swift
struct Size {
    var width: Int
    var height: Int
}

struct Rectangle {
    var origin: Point
    var size: Size
}

var r1 = Rectangle(origin: Point(x: 0, y: 0), size: Size(width: 10, height: 5))
var r2 = r1
r2.origin.x = 20
r2.size.width = 30
print(r1.origin.x, r1.size.width)
// prints: 0 10
```

值语义会一路复制，修改 `r2` 内外层都不会影响 `r1`。

## 17.7 结构体里放类的陷阱

结构体是值类型，不代表它里面的所有东西都会被值复制：

```swift
final class Box {
    var value = 1
}

struct Holder {
    var box: Box
}

let h1 = Holder(box: Box())
let h2 = h1
h2.box.value = 99
print(h1.box.value)
// prints: 99
```

`Holder` 被复制了，但复制的是同一个 `Box` 引用。两个结构体各自持有一个引用，却指向同一个对象。写值类型模型时，看见引用类型属性就要多想一步。

## 17.8 结构体适合什么

结构体最适合：

- 坐标、尺寸、范围、配置这类小而独立的数据。
- 需要值语义、可安全复制的数据。
- 作为模型值传递，不希望调用方共享可变状态。

类更适合：

- 有明确身份、生命周期和共享引用需求的实体。
- 需要继承和运行时多态的对象图。
- 需要 `deinit` 清理资源的对象。

SwiftUI 的状态模型大量使用结构体，正是因为“重现一个值”比“追踪一个被改来改去的对象”容易得多。

## 17.9 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 自动初始化器 | 属性没有默认值时生成成员逐一初始化器 |
| 值语义 | 赋值、传参得到独立副本 |
| `mutating` | 结构体修改自身属性的方法必须标注 |
| `let` 实例 | 整个结构体值不可变 |
| 自定义初始化器 | 可能替代自动生成的成员逐一初始化器 |
| 引用属性 | 结构体复制时，类属性复制的是引用 |

## 17.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 以为结构体永远没有共享 | 内嵌类属性仍会共享对象 |
| 在方法里直接改 `var` 属性 | 必须把方法声明为 `mutating` |
| 以为 `let` 属性不能有变化 | `let` 锁整个值，属性级别可读不可改 |
| 自定义初始化器后找不到成员逐一初始化器 | 自定义会替代自动生成，必要时放扩展 |
| 结构体和类混着建模却不区分语义 | 先问“这是值还是身份”，再选类型 |

## 17.11 下章预告

下一章讲类。它带来共享引用、继承和生命周期，也带来别名、循环引用等必须负责的后果。结构体给你独立副本，类给你身份；两者都不是“更高级”的替代。
