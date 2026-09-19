+++
title = "第8章 元组、类型别名与基础类型判断"
weight = 80
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第八章：元组、类型别名与基础类型判断

> 有时候你只想把两个值捆在一起传出去，为此专门定义一个结构体显得太重。元组就是 Swift 给你的“临时小纸箱”：轻、直接、不需要声明类型。但它也有边界——不是万能容器，更不是结构体的替代品。这一章把元组、`typealias` 和类型判断的入门用法一次说清。

## 8.1 元组：把几个值放进同一个包裹

元组用圆括号创建，元素可以是不同类型：

```swift
let http = (404, "Not Found")
print(http.0, http.1)
// prints: 404 Not Found

let point = (x: 3.0, y: 4.0)
print(point.x, point.y)
// prints: 3.0 4.0
```

带标签的元组既能用名字访问，也能用下标访问：

```swift
print(point.0, point.1)
// prints: 3.0 4.0
```

标签只是元组类型的一部分。下面两个变量的类型并不相同：

```swift
let labeled: (x: Int, y: Int) = (1, 2)
let plain: (Int, Int) = labeled   // 可以赋值：标签不会阻止结构相同的元组互通
print(plain)
// prints: (1, 2)
```

反过来的赋值也成立，只要元素类型和顺序一致：

```swift
let again: (x: Int, y: Int) = plain
print(again.x)
// prints: 1
```

## 8.2 解构与交换：元组的顺手用法

元组可以直接拆成多个常量或变量：

```swift
let (status, message) = http
print(status, message)
// prints: 404 Not Found
```

不需要的值用下划线丢掉：

```swift
let (onlyStatus, _) = http
print(onlyStatus)
// prints: 404
```

交换两个变量是元组最经典的表演：

```swift
var a = 1
var b = 2
(a, b) = (b, a)
print(a, b)
// prints: 2 1
```

这里不是“先擦掉再写”的危险操作：右边的 `(b, a)` 先求值，结果再整体赋给左边。

## 8.3 用元组返回多个结果

函数只能返回一个值，但那个值可以是元组：

```swift
func minMax(_ values: [Int]) -> (min: Int, max: Int)? {
    guard let first = values.first else { return nil }
    var low = first
    var high = first
    for value in values.dropFirst() {
        low = Swift.min(low, value)
        high = Swift.max(high, value)
    }
    return (low, high)
}

if let result = minMax([7, 2, 9, 4]) {
    print(result.min, result.max)
    // prints: 2 9
}
```

这类返回值适合“两个结果天然绑定在一起”的场景，例如坐标、范围和版本号。若这组数据会在很多地方出现，或者需要遵循协议、添加方法，就应该换成结构体。元组是便签纸，不是长期档案。

## 8.4 元组的比较与限制

元组可以逐元素比较，但有两个容易踩的坑。

第一，相等比较最多支持 6 个元素。元素类型都支持 `==` 时，最多 6 元的元组可以比较：

```swift
print((1, "a") == (1, "a"))
// prints: true
print((1, 2, 3, 4, 5, 6) == (1, 2, 3, 4, 5, 6))
// prints: true
```

到了 7 个元素，编译器会拒绝：

```swift
let seven = (1, 2, 3, 4, 5, 6, 7)
print(seven == seven)
```

```text
error: binary operator '==' cannot be applied to two '(Int, Int, Int, Int, Int, Int, Int)' operands
```

更新的工具链会把重复的元素类型折叠起来，写成 `(Int /* ... repeated 7 times ... */)`，意思完全一样。

第二，元组不能遵循 `Hashable`，所以不能直接放进 `Set`，也不能直接当字典的键：

```swift
let pairs: Set<(Int, Int)> = []
```

```text
error: type '(Int, Int)' does not conform to protocol 'Hashable'
```

> 记忆法：元组擅长“临时打包、一次传递”，不擅长“长期身份、去重、排序”。一旦需要这些能力，请定义结构体并让它遵循 `Equatable`、`Hashable` 或 `Comparable`。

## 8.5 类型别名：给类型起一个更顺口的名字

`typealias` 不会创建新类型，只是给现有类型挂一个更可读的名字：

```swift
typealias UserID = Int
typealias Vector = (x: Double, y: Double)

let id: UserID = 42
let velocity: Vector = (x: 1.5, y: -2.0)
print(id, velocity.x, velocity.y)
// prints: 42 1.5 -2.0
```

`UserID` 和 `Int` 是同一个类型，编译器允许它们互相赋值。别把它误认为“更严格的类型包装”：

```swift
let raw: Int = id
print(raw)
// prints: 42
```

类型别名最适合三件事：缩短很长的泛型类型、给元组或闭包类型取有含义的名字、在迁移期间兼容旧名称。

```swift
typealias Handler = (Result<Data, Error>) -> Void
```

## 8.6 类型判断：`is`、`as?` 与 `as!`

当变量被装进 `Any` 或父类类型后，你可能需要问出它的真实身份。`is` 用来判断，结果为 `Bool`：

```swift
let value: Any = 42

print(value is Int)
// prints: true
print(value is String)
// prints: false
```

`as?` 是安全的向下转换：成功得到可选值，失败得到 `nil`：

```swift
let number = value as? Int
print(number ?? -1)
// prints: 42

let text = value as? String
print(text as Any)
// prints: nil
```

可以把它和 `if let` 组合：

```swift
if let number = value as? Int {
    print("整数：\(number)")
    // prints: 整数：42
}
```

`as!` 是强制转换：你向编译器保证“一定是这个类型”，错了就会在运行时崩溃：

```swift
let forced = value as! Int
print(forced)
// prints: 42
```

失败时，程序不会偷偷给你一个默认值，而是直接停下：

```text
Fatal error: Could not cast value of type 'Swift.Int' to 'Swift.String'
```

> 结论很简单：能用 `as?` 就不要用 `as!`；只有“逻辑上绝不可能失败，失败就说明程序有严重 bug”时才考虑强制转换。

`as` 还有一个不带问号和感叹号的版本，用于编译器已经确认安全的转换，最典型的是向上转换——把子类实例当成父类来看（`class` 要到第 18 章才正式登场，这里先借用它的形状看一眼）：

```swift
class Animal {}
class Dog: Animal {}

let dog = Dog()
let animal: Animal = dog      // 向上转换，自动且安全
print(animal is Dog)
// prints: true
```

## 8.7 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 元组 | 用圆括号打包多个值，可带标签，可解构 |
| 多返回值 | 函数借助元组一次返回多个结果 |
| 元组比较 | 最多 6 个元素可用 `==` 比较；不能遵循 `Hashable` |
| 类型别名 | `typealias` 只是别名，不是新类型 |
| 类型判断 | `is` 判断，`as?` 安全转换，`as!` 失败即崩溃 |
| 使用边界 | 长期数据、需要协议能力时改用结构体或类 |

## 8.8 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把元组当成可哈希容器 | 元组不能遵循 `Hashable`，不能做 `Set` 元素或字典键 |
| 用 8 个元素的元组做 `==` | 超过 6 个元素的元组不支持 `==` |
| 以为 `typealias` 会创造新类型 | 它只是原名的新标签，类型完全等价 |
| `as?` 失败后继续用结果 | 失败返回 `nil`，必须先解包 |
| 习惯性使用 `as!` | 失败会触发运行时崩溃，优先使用 `as?` 或 `is` |
| 元组越写越大 | 字段超过三个左右就该考虑结构体 |

## 8.9 下章预告

下一章是很多 Swift 初学者最容易掉进去、也最值得认真学的一章：**可选值**。它不是“可以为空”这么简单，而是一套迫使你处理“没有值”的完整机制。学会它，你的代码会少掉大量隐藏的空指针事故。
