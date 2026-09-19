+++
title = "第27章 值语义、写时复制与 ARC"
weight = 270
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十七章：值语义、写时复制与 ARC

> 结构体复制起来为什么没有把数组里的几百万个元素全抄一遍？类实例释放时，Swift 又是怎么知道该调用 `deinit`？答案分别在写时复制（COW）和自动引用计数（ARC）里。它们不是语法糖，而是 Swift 性能与内存模型的地基。

## 27.1 值语义与引用语义再对照

同一段赋值写法，放在结构体和类上，结果完全不同。并排看一次：

```swift
struct PointValue { var x = 0 }
final class PointRef { var x = 0 }

var a = PointValue()
var b = a
b.x = 10
print(a.x, b.x)
// prints: 0 10

let c = PointRef()
let d = c
d.x = 10
print(c.x)
// prints: 10
```

值类型在赋值时表现为独立副本；引用类型在赋值时复制引用。这个语义的区别，比“结构体还是类”这个名称更重要。

## 27.2 写时复制：先共享，修改再分开

标准库的数组、字典、字符串和集合都使用 COW。赋值时先共享底层存储，某一方修改时才复制：

```swift
var original = [1, 2, 3]
var copy = original          // 此刻底层可能还是同一份存储
copy.append(4)               // 修改发生，copy 分离出自己的存储
print(original, copy)
// prints: [1, 2, 3] [1, 2, 3, 4]
```

这就是为什么 `Array` 既是值语义，又不会傻乎乎地每次赋值都全量复制。你看到的是“复制”，运行时做的是“延迟复制”。

## 27.3 自己实现一个 COW 盒子

COW 的核心是：判断引用是否唯一，不唯一就复制。

```swift
final class Storage<T> {
    var value: T
    init(_ value: T) { self.value = value }
}

struct COWBox<T> {
    private var storage: Storage<T>

    init(_ value: T) { storage = Storage(value) }

    var value: T {
        get { storage.value }
        set {
            if !isKnownUniquelyReferenced(&storage) {
                storage = Storage(storage.value)
            }
            storage.value = newValue
        }
    }
}

var a = COWBox([1, 2])
var b = a
b.value.append(3)
print(a.value, b.value)
// prints: [1, 2] [1, 2, 3]
```

`isKnownUniquelyReferenced` 判断传入的引用是否只有一个持有者。为 `true` 时可以直接复用存储；为 `false` 时先复制一份，避免把共享状态改坏。

真实库还要处理线程安全、性能、异常和更多访问器。理解模式即可，不要在生产代码里重复造一个未经验证的容器。

## 27.4 ARC：类实例的自动引用计数

每次创建一个类实例，都会有一个强引用计数。新引用指向对象时计数增加，引用离开作用域时计数减少，归零后实例释放并调用 `deinit`：

```swift
final class Resource {
    let name: String

    init(name: String) {
        self.name = name
        print("创建 \(name)")
    }

    deinit {
        print("释放 \(name)")
    }
}

func use() {
    let resource = Resource(name: "db")
    print("使用 \(resource.name)")
}

use()
// prints: 创建 db
// prints: 使用 db
// prints: 释放 db
```

ARC 只管理引用计数，不负责扫描整个堆。它比垃圾回收器更容易预测，但也允许循环引用把对象永久留住，这正是下一章的主题。

## 27.5 强引用、弱引用和无主引用预览

属性默认是强引用：

```swift
final class Parent {
    var child: Child?
}

final class Child {}

var parent: Parent? = Parent()
parent?.child = Child()
parent = nil
print("parent 已置空")
// prints: parent 已置空
```

如果两个对象互相强引用，计数都不会归零。解决方式是让其中一边变成 `weak` 或 `unowned`：

```swift
final class Node {
    var next: Node?
}
```

`weak` 不能用于非可选引用，因为对象释放后引用必须自动变成 `nil`。下一章会详细区分 `weak` 和 `unowned` 的使用场景。

## 27.6 引用计数的性能直觉

ARC 的每次 retain/release 都很便宜，但热路径里成千上万次也会累积成本。常见优化方式包括：

- 能用值类型表达的数据，优先用结构体。
- 对闭包捕获列表和委托引用保持清晰的所有权。
- 在性能敏感的代码中减少不必要的长生命周期强引用。
- 使用 Instruments 或性能测试确认瓶颈，而不是凭感觉猜。

ARC 的规则不需要你手动写 retain/release，但你必须知道“谁持有谁”，否则内存问题会以最隐蔽的方式出现。

## 27.7 本章小结

| 主题 | 结论 |
| --- | --- |
| 值语义 | 赋值表现为独立副本 |
| 引用语义 | 赋值复制引用，实例共享 |
| COW | 先共享存储，修改时才分离 |
| `isKnownUniquelyReferenced` | 判断引用是否唯一，是手写 COW 的关键 |
| ARC | 自动维护类实例的强引用计数 |
| `deinit` | 计数归零、实例释放时调用 |
| 循环引用 | 互相强引用会导致对象无法释放 |

## 27.8 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 认为 COW 是语言自动对任意类型生效 | 需要容器或自定义类型主动实现 |
| 把结构性修改当作值复制 | 只有修改时才可能触发存储分离 |
| 以为 ARC 会解决循环引用 | 它只计数，不会替你打破循环 |
| 在热路径随意复制大对象 | 先测量，再考虑 COW 或引用类型 |
| 在 `deinit` 里依赖全局可变状态 | 释放时机虽然可预测，但顺序仍可能复杂 |
| 把值类型等同于“没有引用” | 值类型内部可以持有类引用 |

## 27.9 下章预告

下一章专门处理 ARC 最著名的坑：循环引用。`weak`、`unowned`、闭包捕获列表和委托模式会在这一章彻底说清。
