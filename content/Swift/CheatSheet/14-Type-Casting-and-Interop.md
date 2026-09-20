+++
title = "14 类型转换与互操作"
linkTitle = "14 类型转换"
weight = 140
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "is / as / as? / as! 的分工、Any 与元类型、Mirror 反射，以及与 C、Objective-C 的边界"
isCJKLanguage = true
draft = false
+++

# 14 类型转换与互操作

## 四种写法，先分清谁是谁

| 写法 | 名字 | 干什么 | 失败时 |
| --- | --- | --- | --- |
| `x is T` | 类型检查 | 问一句"它是不是 `T`" | 不会失败，给个 `Bool` |
| `x as? T` | 条件转换 | 是就转，不是就算了 | 给 `T?`，没转成就是 `nil` |
| `x as! T` | 强制转换 | 我确定它是 | **崩** |
| `x as T` | 向上转型 / 桥接 / 字面量标注 | 编译期就成立的事 | 编译期直接报错 |

```swift
let things: [Any] = [1, "two", 3.0, true]

for thing in things {
    if let number = thing as? Int {
        print("整数", number)
    } else if thing is String {
        print("字符串")
    } else {
        print("其他", type(of: thing))
    }
}
// prints:
//   整数 1
//   字符串
//   其他 Double
//   其他 Bool
```

🔥 `is` 和 `as?` 的区别只有一条：你要不要那个转好的值。只要判断就用 `is`，要拿来用就用 `as?`。

⚠️ `as!` 转错的死法是运行时崩溃，错误长这样：

```text
Could not cast value of type 'Swift.String' (0x...) to 'Swift.Int' (0x...)
```

它和 `!` 是一家人：只在"已经用别的方式证明过"的地方用，比如单元测试里对刚构造出来的对象做转换。

## `as` 的三种正经用法

不带 `?` / `!` 的 `as` 不检查运行期类型，它只做编译期就成立的三件事：

| 用途 | 例子 |
| --- | --- |
| 向上转型 | `let a: Animal = dog as Animal` |
| 桥接 | `let n = 1 as NSNumber` |
| 给字面量标注类型 | `let d = 1 as Double` |

```swift
class Animal {}
final class Dog: Animal {}

let dog = Dog()
let upcast: Animal = dog as Animal       // 向上转，永远安全
print(type(of: upcast))
// prints: Dog

let d = 1 as Double
print(d, type(of: d))
// prints: 1.0 Double
```

⚠️ 向下转型必须写 `as?` 或 `as!`。以下面这个 `let dog = Dog()` 为例，写成 `dog as Cat` 编译器直接拦下：`cannot convert value of type 'Dog' to type 'Cat' in coercion`。（如果是声明成 `let dog: Animal = Dog()` 再写 `dog as Cat`，报的会是另一句 `'Animal' is not convertible to 'Cat'`——都指向上转型不能顺手转下来这件事。）

💭 注意上面 `type(of: upcast)` 给的是 `Dog` 而不是 `Animal`：变量声明的类型是静态类型，`type(of:)` 看的是运行期类型。多态就建立在这两者的差别上。

## 在模式里做转换

模式和转换是一家人。`switch` 的 `case is T`、`case let x as T`，和 `if let x = y as? T` 在干同一件事：

```swift
protocol Shape { var area: Double { get } }
struct Circle: Shape { var area: Double { 1 } }

let things: [Any] = [1, "s", Circle()]

for thing in things {
    switch thing {
    case is Int:              print("整型")
    case let s as String:     print("字符串 \(s)")
    case let c as any Shape:  print("形状 \(c.area)")
    default:                  print("未知")
    }
}
// prints:
//   整型
//   字符串 s
//   形状 1.0

let mixed: [Any] = [1, 2, "x"]
for case let n as Int in mixed { print("整数", n) }
// prints:
//   整数 1
//   整数 2
```

💭 `for case let n as Int in mixed` 比"循环里再套两层 `if`"短，也比链式 `compactMap` 更像一句人话——前提是你的同事一眼能看懂。

## Any、AnyObject、AnyHashable

| 类型 | 意思 | 什么时候用 |
| --- | --- | --- |
| `Any` | 任何值，值类型会被装箱 | 异构数组、动态数据、桥接过来的东西 |
| `AnyObject` | 任何类实例 | 与 Objective-C 打交道、老 API 的签名 |
| `AnyHashable` | 能当哈希键的 `Any` | 混合类型的字典键 / 集合元素 |
| `ObjectIdentifier` | 引用对象的**身份**标识 | 想用对象当字典键、又不想强引用它时 |

```swift
let box: Any = 1
print(box is Int, box as? Int ?? 0)
// prints: true 1

let set: Set<AnyHashable> = [AnyHashable(1), AnyHashable("a")]
print(set.contains(AnyHashable(1)), set.contains(AnyHashable("b")))
// prints: true false

// ObjectIdentifier 只认"是不是同一个对象"，拿它当键不会拦住对象释放
final class Session {}
var table: [ObjectIdentifier: String] = [:]
let s = Session()
table[ObjectIdentifier(s)] = "已登录"
print(table[ObjectIdentifier(s)] ?? "没有")
// prints: 已登录
```

💭 `[ObjectIdentifier: T]` 是"给对象挂一张外置表"的经典写法——键是身份，不是相等（要相等得用 `Equatable`）。它自己不持有对象，对象释放后表里那条就成了一条谁也查不到的垃圾，需要清理就配合 `weak` 引用或自己记账。

⚠️ **`Any` 没有 `==`。** 下面两行都编译不过，因为"相等"这件事需要具体类型说了算：

```text
error: binary operator '==' cannot be applied to operands of type 'Any' and 'Int'
error: binary operator '==' cannot be applied to two '[Any]' operands
```

要比较就先把类型转出来（`if let a = x as? Int, let b = y as? Int { a == b }`），或者从一开始就用 `AnyHashable` 装。

⚠️ `Any` 会把值装箱：`let x: Any = 1` 比 `let x = 1` 多一层间接，取出来还要再转一次。能写具体类型就别写 `Any`，泛型往往才是你想要的东西。

## 桥接：Foundation 类型的双面人生

Swift 的 `String`、`Array`、`Dictionary`、`Data` 这些和 Foundation 的 `NSString`、`NSArray`、`NSDictionary`、`NSData` 是**桥接**关系，写 `as` 就能互转：

```swift
import Foundation

let s = "hi" as NSString
let n = 1 as NSNumber
let b = true as NSNumber
let arr = [1, 2] as NSArray
let dict = ["a": 1] as NSDictionary
let data = Data([1]) as NSData
let date = Date(timeIntervalSince1970: 0) as NSDate

print(s.length, n.intValue, b.boolValue, arr.count, dict.count, data.length, date.timeIntervalSince1970)
// prints: 2 1 true 2 1 1 0.0
```

⚠️ 桥接会带来一个反直觉的结果：`NSNumber` 记得自己是哪种数字，所以它能"同时是" `Int` 和 `Double`：

```swift
import Foundation

let n: NSNumber = 1 as NSNumber
print(n.intValue, n is Int, n is Double)
// prints: 1 true true
```

对 `NSNumber` 用 `is` 时，问的不是"它在 Swift 里是什么"，而是"它**能不能**桥接成那个类型"。从 JSON 或 KVC 拿回来的数字尤其容易踩这个坑，需要具体类型时用 `as?` 转出来再用。

## 元类型：类型本身也是值

类型可以当参数传、当返回值返回，写法是 `T.self`：

| 写法 | 类型 | 说明 |
| --- | --- | --- |
| `Int.self` | `Int.Type` | 类型的"引用" |
| `type(of: x)` | `T.Type` | `x` 的**运行期**类型 |
| `any Any.Type` | — | 任意元类型，类型未知时用它 |
| `T.init` | 构造器 | 配合元类型动态构造 |

```swift
protocol Shape { init() }
struct Circle: Shape { init() {} }

func make(_ type: any Shape.Type) -> any Shape {
    type.init()
}

print(type(of: make(Circle.self)))
// prints: Circle

let shape: any Shape = Circle()
print(type(of: shape) == Circle.self)
// prints: true

let t: any Any.Type = String.self
print(t == String.self)
// prints: true
```

⚠️ `type(of:)` 给的是运行期类型，`T.self` 给的是你在源码里写下的类型。判断"这个对象到底是什么"用前者，做静态派发或构造用后者。

🝖 `x.self` 对**值**也合法：`let n = 1; print(n.self)` 打出来的就是 `1`。它几乎只在泛型与元编程里出现，日常代码里见到不必惊讶。

## Mirror：不改一行代码看一眼内部

`Mirror` 是标准库给的只读反射视图，调试和做通用展示（比如自己写一个 `debugDescription`）时很好用：

```swift
struct Point { var x = 1; var y = 2 }

let mirror = Mirror(reflecting: Point())
print(mirror.displayStyle as Any, mirror.children.count)
for child in mirror.children {
    print(child.label ?? "?", child.value)
}
// prints: Optional(Swift.Mirror.DisplayStyle.struct) 2
//         x 1
//         y 2
```

| 成员 | 作用 |
| --- | --- |
| `.children` | 子元素：属性、关联值、元组元素 |
| `.label` | 子元素的名字：结构体给属性名，枚举给 case 名，元组没写标签时给位置名 `.0` `.1`，而数组 / 字典的元素没有名字，这里就是 `nil` |
| `.displayStyle` | `struct` / `class` / `enum` / `tuple` / `optional` … |
| `.superclassMirror` | 顺着父类继续看 |

⚠️ Mirror 只看**存储**属性：计算属性、`lazy` 还没算出来的值都不在 `children` 里；它也拿不到内存布局的细节——那是 `MemoryLayout` 的地盘，见 [10 内存与值语义]({{< relref "10-Memory-and-Value-Semantics.md" >}})。官方给它定的岗位是"调试与展示"，不是序列化——序列化请用 `Codable`。

## 与 Objective-C 互操作

Apple 平台上还能直接和 Objective-C 对话。日常用得到的就这几件事：

| 需求 | 写法 |
| --- | --- |
| 把成员暴露给 ObjC | `@objc func tapped(_ sender: Any?)` |
| 整个类型都暴露 | `@objcMembers final class Handler: NSObject` |
| 拿到选择器 | `#selector(Handler.tapped(_:))` |
| 动态派发 | `dynamic func f()` 🝖 |
| 字符串转选择器 | `NSSelectorFromString("tapped:")` |
| Swift 错误转 NSError | `error as NSError` |

```swift
import Foundation

final class Handler: NSObject {
    @objc func tapped(_ sender: Any?) { print("tapped") }
}

let handler = Handler()
let selector = #selector(Handler.tapped(_:))
print(selector, NSStringFromSelector(selector))
handler.perform(selector, with: nil)
// prints: tapped: tapped:
//         tapped
```

⚠️ `@objc` 要求类型能进 Objective-C 运行时，所以通常是 `NSObject` 的子类；`#selector` 也只能指向 `@objc` 的成员。这套能力**只在 Apple 平台**成立——Linux 上没有 Objective-C 运行时，用到这个章节的内容就说明这段代码只打算跑在 Apple 平台上。🚧

💭 新代码里能不用就不用：Swift 原生的协议、闭包、`Codable` 已经能覆盖绝大多数原来的 ObjC 用途。真需要它的场合基本只剩两类：跟系统框架的 target/action、通知、KVC 打交道，以及给 ObjC 代码提供接口。

### `@objc optional`：可以"不实现"的协议要求

Swift 协议里的要求必须全实现，但 `@objc` 协议可以标 `optional`——这正是老式 delegate 的写法：

```swift
import Foundation

@objc protocol Greeter: AnyObject {
    func requiredGreet() -> String
    @objc optional func optionalGreet() -> String
}

final class Robot: NSObject, Greeter {
    func requiredGreet() -> String { "hi" }        // 只实现必须的那个
}

let r = Robot()
print(r.requiredGreet())
// prints: hi

let g: any Greeter = r
print(g.optionalGreet?() ?? "没实现")
// prints: 没实现

print(r.responds(to: #selector(Greeter.optionalGreet)))
// prints: false
```

⚠️ 三个容易卡住的点：

1. **只能通过协议类型调用可选要求**：`r.optionalGreet?()` 报 `value of type 'Robot' has no member 'optionalGreet'`，得先写 `let g: any Greeter = r`（实测）。
2. **可选要求返回的永远是可选值**，必须自己兜底。
3. **`responds(to:)` 能问"实现了没"**，这在 ObjC 风格的回调里很常用。

### `@convention(c)`：把闭包交给 C

需要把 Swift 闭包当 C 函数指针用时，标上调用约定。这种闭包**不能捕获上下文**——捕获了运行期变量就报 `a C function pointer cannot be formed from a closure that captures context`（实测。注意 `swiftc -typecheck` 漏得掉这条诊断，要完整编译才看得见，这也是 [13 章]({{< relref "13-Tooling.md" >}})里提醒"`-typecheck` 最快但会漏"的实例之一）：

```swift
let compare: @convention(c) (Int, Int) -> Int = { a, b in a - b }
print(compare(3, 1))
// prints: 2
```

💭 一般代码写不到这里；只有和 C 库、`qsort`、回调式系统 API 打交道时才会遇到。想让 Swift 函数被 C 调用，则是另一个方向——用 `@_cdecl("名字")` 导出，它属于非正式特性，用之前先查 [13 章]({{< relref "13-Tooling.md" >}})里的官方资料。

### `@_cdecl`：反过来，让 C 调用 Swift

`@convention(c)` 是"把 C 函数指针收进来"，`@_cdecl` 是"把 Swift 函数交出去"：

```swift
@_cdecl("swift_add")
public func swiftAdd(_ a: Int32, _ b: Int32) -> Int32 { a + b }

print(swiftAdd(2, 3))
// prints: 5
```

C 侧只要声明一下就能直接用（这是实测跑通的完整流程）：

```c
#include <stdint.h>
extern int32_t swift_add(int32_t a, int32_t b);
```

```console
$ swiftc -emit-library -o libadd.dylib add.swift
$ clang -o demo main.c -L. -ladd -Wl,-rpath,.
$ ./demo
5
```

⚠️ 三个实测出来的细节：

1. **要导出成库给别的模块用时，函数得是 `public`。** 忘了写 `public`，符号虽然还在二进制里（`nm libadd.dylib` 能看到 `t _swift_add`，小写 `t` 表示它是本地符号），但它不在导出表里（`nm -gU` 为**空**），链接时照样失败：

   ```console
   $ nm -gU libadd.dylib | grep swift_add      # 没有 public 时：毫无输出
   $ clang -o demo main.c -L. -ladd -Wl,-rpath,.
   Undefined symbols for architecture arm64:
     "_swift_add", referenced from:
         _main in main-xxxx.o
   ld: symbol(s) not found for architecture arm64
   ```

   加上 `public` 之后 `nm -gU` 变成 `T _swift_add`（大写 `T` = 外部可见），链接立刻通过。⚠️ 报错里的符号名是 `_swift_add`，**没有**任何后缀——看到 `_xxx2` 那种名字，那是别的原因（比如两个文件重复导出同名符号）造成的。
2. **参数只能是 C 认识的东西**：定长整数（`Int32`、`UInt8`…）、`Double`、`Float`、`Bool`、指针。`String`、`Array` 这些不能直接跨过去——实测 `@_cdecl` 里写 `String` 参数会报 `global function cannot be marked '@_cdecl' because the type of the parameter cannot be represented in Objective-C`，得改用 `UnsafePointer<CChar>`（用 `strdup` 或 `withCString` 搭桥）。（`Bool` 是可以的，它在 C 侧对应 `stdbool.h` 的 `bool`，实测从 C 调用能正确往返。）
3. **下划线开头意味着"非正式 API"**：它不在官方语言参考的正式特性里，行为可能变。真要用就先固定工具链版本，并写一个 C 侧的冒烟测试。🛑

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 用 `as!` 转换外部数据 | 崩；用 `as?` 加 `guard let` |
| 以为 `as` 会做检查 | 它只做编译期成立的转换，检查得用 `as?` / `is` |
| `Any` 当万能类型用 | 装箱 + 每次取用都要转，热路径上换成泛型 |
| 对 `NSNumber` 做 `is` | 它可能同时"是" `Int` 和 `Double`，要具体类型就 `as?` |
| 对 `[Any]` 用 `==` | 编译不过，`Any` 没有 `==` |
| 用 `type(of:)` 比较源码类型 | 它给的是运行期类型，泛型里尤其容易反着理解 |
| 用 Mirror 做序列化 | 看不到计算属性、也不保证布局，序列化用 `Codable` |
| 忘了 `#selector` 的目标必须 `@objc` | 编译报 `argument of '#selector' refers to instance method 'plain()' that is not exposed to Objective-C` |
| 在 Linux 上照抄 `@objc` | 没有 ObjC 运行时，这段代码只属于 Apple 平台 |
