+++
title = "10 内存与值语义"
linkTitle = "10 内存与值语义"
weight = 100
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "值传递还是引用传递、写时复制、独占访问、ARC 与循环引用、不可复制类型与内存布局"
isCJKLanguage = true
draft = false
+++

# 10 内存与值语义

## 赋值的时候到底发生了什么

这个问题决定了 Swift 里 90% 的意外行为。

| | 值类型（`struct` `enum` 集合 基本类型） | 引用类型（`class` `actor` 闭包） |
| --- | --- | --- |
| 赋值 | 逻辑上复制一份 | 复制一个指针 |
| 传参 | 逻辑上复制一份 | 传指针 |
| 放进数组 | 逻辑上复制一份 | 传指针 |
| 改一个会影响另一个吗 | ❌ | ✅ |
| 内存布局 | 通常内联在容器里 | 堆上一个独立对象 |

{{< tabpane text=true persist=disabled >}}

{{% tab header="值类型" %}}

```swift
struct Score { var value: Int }

var a = Score(value: 1)
var b = a
b.value = 99

print(a.value, b.value)
// prints: 1 99
```

两个变量各有一份数据。函数参数同理：

```swift
struct Score { var value: Int }

func bump(_ s: Score) -> Score {
    var copy = s
    copy.value += 1
    return copy
}

let a = Score(value: 1)
print(bump(a).value, a.value)
// prints: 2 1
```

{{% /tab %}}

{{% tab header="引用类型" %}}

```swift
final class Score { var value: Int; init(_ v: Int) { value = v } }

let a = Score(1)
let b = a
b.value = 99

print(a.value, b.value)
// prints: 99 99
```

哪怕 `a` 是 `let`，`a.value` 依然能改——`let` 锁的是指针，不是对象内部。

{{% /tab %}}

{{% tab header="集合里的元素" %}}

```swift
struct Point { var x: Int }
final class Marker { var x: Int; init(_ v: Int) { x = v } }

var points = [Point(x: 1)]
var markers = [Marker(1)]

var pointsCopy = points
var markersCopy = markers

pointsCopy[0].x = 99
markersCopy[0].x = 99

print(points[0].x, pointsCopy[0].x)
// prints: 1 99
print(markers[0].x, markersCopy[0].x)
// prints: 99 99     元素是引用类型时，拷贝数组不会拷贝元素
```

🔥 一个数组里装引用类型，数组本身的"值语义"就名存实亡了——拷贝数组只拷贝了指针。

{{% /tab %}}

{{< /tabpane >}}

## 写时复制（Copy-on-Write）

"逻辑上复制一份"如果真每次都复制，性能会很糟。所以标准库的 `Array`、`Dictionary`、`Set`、`String` 用了写时复制：**只有在你真的改了，而且还有别人共享时，才复制。**

```swift
var a = Array(repeating: 0, count: 1_000_000)
var b = a          // 此刻并没有复制 100 万个整数
b.append(1)        // 到了这一步，才真正复制
print(a.count, b.count)
// prints: 1000000 1000001
```

代价是：`isKnownUniquelyReferenced` 这种判断带一点开销，而且多线程共享同一份底层缓冲时，一旦复制，内存峰值会翻倍。

### 给自己的类型实现 COW

```swift
struct Buffer {
    private final class Box {
        var values: [Int]
        init(_ v: [Int]) { values = v }
    }

    private var box: Box
    init(_ values: [Int]) { box = Box(values) }

    var values: [Int] {
        get { box.values }
        set {
            if !isKnownUniquelyReferenced(&box) {
                print("共享中，先复制一份")
                box = Box(box.values)
            }
            box.values = newValue
        }
    }
}

var a = Buffer([1, 2, 3])
var b = a              // 共享同一份数据
b.values = [9]         // 第一次写，触发复制
print(a.values, b.values)
// prints: 共享中，先复制一份
//         [1, 2, 3] [9]
```

💭 需要写 COW 的场合其实很少：容器装的是大块数据（大数组、图片缓冲）才值得。普通小结构体直接复制更简单。

## 独占访问：写的时候别人不许碰

Swift 有一条平时不出声、出事时很难查的规则：**同一块内存，写访问必须独占**。读可以大家一起读，但只要有人在写，就不许别人同时读或写它。

`inout` 参数是这条规则最常见的入口：它的写访问**从实参求值完开始，一直持续到函数返回**。下面几种写法都会炸。

把同一个变量传给两个 `inout` 参数，编译器当场拦下：

```text
error: inout arguments are not allowed to alias each other
error: overlapping accesses to 'p.health', but modification requires exclusive access; consider copying to a local variable [#ExclusivityViolation]
```

而下面这种"看着挺正常"的写法，编译器**有时证明得了、有时证明不了**：

```swift
struct Player { var health = 1; var energy = 2 }

func balance(_ a: inout Int, _ b: inout Int) { a += b }

func localCase() {
    var oscar = Player()
    balance(&oscar.health, &oscar.energy)   // ✅ 局部变量的两个存储属性，编译器能证明互不相干
    print("OK", oscar.health, oscar.energy)
}
localCase()
// prints: OK 3 2
```

把 `oscar` 换成全局变量、或者把元组的两个元素传进去，编译器就证明不了了——本机实测是运行期直接崩：

```text
Simultaneous accesses to 0x..., but modification requires exclusive access.
Fatal access conflict detected.
```

⚠️ 判断标准不是"这两块内存有没有关系"，而是"**编译器能不能证明**没有关系"。局部变量的存储属性它证明得了；全局变量、类实例的属性、元组元素常常证明不了，于是改用运行期检查——检查失败就是上面那句致命错误。[14 类型转换]({{< relref "14-Type-Casting-and-Interop.md" >}}) 里 `NSNumber` 那种"看起来是 A 其实是 B"的坑，和这里是同一种味道：**别问直觉，问编译器**。

真碰上冲突，解法只有一个：把要读的值先抄到局部变量里，让读访问在写访问开始之前结束。

```swift
var stepSize = 1
func increment(_ number: inout Int, by step: Int) { number += step }

var copyOfStepSize = stepSize          // 先抄出来
increment(&stepSize, by: copyOfStepSize)
print(stepSize)
// prints: 2
```

⚠️ 同一个值既是 `mutating` 方法的 `self`、又是它的 `inout` 参数时也报同样的错：`oscar.share(with: &oscar)` → `inout arguments are not allowed to alias each other`。

📘 完整的规则与示意图在官方语言指南的 [Memory Safety](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/) 一章。

## ARC：引用计数

类实例靠自动引用计数（ARC）管理生命周期。每次赋值、传参、存进属性，计数 +1；离开作用域，计数 -1；归零就销毁并调用 `deinit`。

| 引用种类 | 会 +1 吗 | 为 `nil` 时访问 | 什么时候用 |
| --- | --- | --- | --- |
| `strong`（默认） | ✅ | 对象不会为 `nil` | 默认，表示"我拥有它" |
| `weak` | ❌ | 自动变成 `nil`，所以类型必须是 `T?` | 反向引用、代理、闭包里的 `self` 🔥 |
| `unowned` | ❌ | 崩溃 | 你能保证生命周期不短于自己 |

```swift
final class Node {
    let name: String
    var parent: Node?
    weak var child: Node?
    init(_ name: String) { self.name = name }
    deinit { print("释放 \(name)") }
}

var root: Node? = Node("root")
var leaf: Node? = Node("leaf")
root?.child = leaf
leaf?.parent = root

root = nil
leaf = nil
// prints: 释放 leaf
//         释放 root       leaf 释放时，它强引用的 parent 才跟着释放
```

把 `weak var child` 改回 `var child`（强引用），上面两个对象会互相持有，谁都不会被释放——这就是**循环引用**。

### 循环引用的三种典型形态

| 形态 | 症状 | 修法 |
| --- | --- | --- |
| 两个对象互相强引用 | 两个 `deinit` 都不执行 | 一侧改 `weak` |
| 闭包捕获 `self`，`self` 又持有闭包 | 控制器不释放 | `[weak self]` |
| 代理属性写成强引用 | 视图控制器不释放 | `weak var delegate` |

```swift
final class Downloader {
    var onFinish: (() -> Void)?
    var data = "数据"
    func start() {
        onFinish = { [weak self] in
            print(self?.data ?? "已释放")
        }
    }
}
```

⚠️ `weak` 只对类有效。结构体、枚举、元组里写 `weak` 是编译错误，因为它们本来就不会造成引用环。

### deinit 与销毁顺序

```swift
final class Resource {
    let name: String
    init(_ name: String) { self.name = name; print("创建 \(name)") }
    deinit { print("销毁 \(name)") }
}

func scope() {
    let a = Resource("A")
    let b = Resource("B")
    _ = (a, b)
}
scope()
// prints: 创建 A
//         创建 B
//         销毁 B
//         销毁 A      同一作用域内按声明的逆序释放
```

⚠️ `deinit` 里**不能**调用异步代码，也不应该做需要 `await` 的清理。真正的异步资源释放要另想办法（比如显式 `close()`）。

### 两个"管生命周期"的工具

ARC 的规则是"最后一次用到之后就可以释放"，所以下面这两件事偶尔会需要你插手：

```swift
import Foundation

final class Resource {
    let id: Int
    init(id: Int) { self.id = id; print("创建 \(id)") }
    deinit { print("释放 \(id)") }
}

// withExtendedLifetime：把对象的生命周期强行拖到块结束
// （编译器有权在"最后一次使用"之后立刻放掉，这个函数就是用来按住它的）
let r = Resource(id: 1)
withExtendedLifetime(r) {
    print("用一下 \(r.id)")
}

// autoreleasepool：循环里大量创建 Objective-C 对象时，手动把临时对象及时清掉
for i in 0..<2 {
    autoreleasepool {
        _ = Resource(id: 100 + i)
    }
}
// prints: 创建 1
//         用一下 1
//         创建 100
//         释放 100
//         创建 101
//         释放 101
```

| 工具 | 什么时候用 |
| --- | --- |
| `withExtendedLifetime(x) { ... }` | 对象的释放时机被优化得过早，而它恰好持有 C 指针、文件描述符一类资源 |
| `autoreleasepool { ... }` | Apple 平台上循环创建大量临时 Objective-C 对象（例如 `NSString`、`UIImage`），内存峰值压不下去 |

💭 `autoreleasepool` 只和 Objective-C 的自动释放池有关——纯 Swift 对象的生命周期由 ARC 在编译期插桩，不进那个池子。所以它是个"边界工具"，不是日常清理手段。

## 闭包捕获的是值还是引用

```swift
final class Counter { var value = 0 }

var number = 1                 // 值类型变量
let counter = Counter()        // 引用类型实例

let snapshot = { print(number, counter.value) }

number = 100
counter.value = 100
snapshot()
// prints: 100 100
```

两者输出的都是 `100`，但原因不同：闭包捕获的是**变量本身**（`number` 被搬到堆上共享），而 `counter` 捕获的是指针，指向的对象的属性当然也变了。

想在闭包里冻结那一刻的值，用捕获列表：

```swift
var number = 1
let frozen = { [number] in number }
number = 100
print(frozen())
// prints: 1
```

## 所有权与不可复制类型 🆕

Swift 5.9 起支持显式的所有权标注，Swift 6 里逐渐可用：

```swift
struct File: ~Copyable {
    let name: String
    deinit { print("关闭 \(name)") }
}

func use() {
    let f = File(name: "test.txt")
    print("使用", f.name)
}
use()
// prints: 使用 test.txt
//         关闭 test.txt
```

| 写法 | 含义 |
| --- | --- |
| `~Copyable` | 这个类型不能被复制，只能移动 |
| `consuming func` | 调用后把 `self` 吃掉 |
| `borrowing func` | 只借用，不取得所有权（默认行为） |
| `consuming` 参数 | 参数被函数吃掉，调用方不能再使用 |

🚧 这套机制的生态还在成形。写库、做零拷贝、封装文件句柄与锁时它很有价值；日常业务代码知道有这回事就够了。

## MemoryLayout：内存里到底占多大

```swift
print(MemoryLayout<Int>.size, MemoryLayout<Int>.stride, MemoryLayout<Int>.alignment)
// prints: 8 8 8

struct WithPadding { var b: Bool; var i: Int }
print(MemoryLayout<Bool>.size)
// prints: 1
print(MemoryLayout<WithPadding>.size, MemoryLayout<WithPadding>.stride)
// prints: 16 16      为了对齐，Bool 后面塞了 7 个填充字节
```

| 类型 | `size` | `stride` |
| --- | --- | --- |
| `Int` | 8 | 8 |
| `Bool` | 1 | 1 |
| `(Int8, Int8)` 结构体 | 2 | 2 |
| `{ Bool, Int }` 结构体 | 16 | 16 |
| `String` | 16 | 16 |
| `[Int]` | 8 | 8 |
| 无关联值的 `enum`（3 个 case） | 1 | 1 |
| 带 `Int` 关联值的 `enum` | 9 | 16 |
| `class` 的引用本身 | 8 | 8 |

关键区别：**`size` 是实际用到的字节，`stride` 是数组里每个元素占的间隔。** 两者的差额就是编译器塞进去的填充。写跨平台二进制格式时别拿结构体布局当协议：成员顺序、填充位置都不保证，`size` 也不等于"各字段加起来"。要序列化就老老实实按字节逐个字段写。

## 指针与 unsafe API

需要读原始字节、和 C 交互、或者做极致优化时，才用这一层：

```swift
struct WithPadding { var b: Bool; var i: Int }

let bytes = withUnsafeBytes(of: UInt16(0x0102)) { Array($0) }
print(bytes)
// prints: [2, 1]      小端序：低字节在前

var values = [10, 20, 30]
print(values.withUnsafeBufferPointer { $0.map { $0 * 2 } })
// prints: [20, 40, 60]

print(MemoryLayout<WithPadding>.offset(of: \.i) ?? -1)
// prints: 8
```

⚠️ `offset(of:)` 在**哪个类型的 `MemoryLayout` 上调**，key path 的根类型就必须是那个类型：`MemoryLayout<Int>.offset(of: \WithPadding.i)` 会报 "cannot convert value of type `PartialKeyPath<WithPadding>` to expected argument type `PartialKeyPath<Int>`"。上面写成 `\.i` 能省掉根类型，是因为上下文已经把它推成 `WithPadding` 了。

| API | 用途 |
| --- | --- |
| `withUnsafeBytes(of:)` | 看某个值的原始字节 |
| `withUnsafeBufferPointer(_:)` | 只读访问数组底层缓冲 |
| `withUnsafeMutableBufferPointer(_:)` | 可写访问 |
| `withUnsafePointer(to:)` | 取某个变量的地址 |
| `UnsafeMutableRawPointer.allocate` | 手工分配内存，**必须配对释放** 🛑 |
| `MemoryLayout<T>.offset(of:)` | 某个属性在结构体里的字节偏移 |
| `ObjectIdentifier(x)` | 引用类型的身份标识，可哈希、可比较 |
| `Unmanaged<T>` | 不参与 ARC 的引用，给 C / 老 API 传对象指针时用 🝖 |
| `x.bitPattern` / `Double(bitPattern:)` | 浮点与整数的位模式互转，安全且无开销 |
| `unsafeBitCast(_:to:)` | 强行按位重解释，编译器多半会建议你换别的写法 🛑 |

```swift
final class Node {}
let a = Node()
let b = Node()

print(ObjectIdentifier(a) == ObjectIdentifier(a), ObjectIdentifier(a) == ObjectIdentifier(b))
// prints: true false

let boxed = Unmanaged.passUnretained(a)
print(boxed.takeUnretainedValue() === a)
// prints: true

print(Double(1.0).bitPattern == 0x3FF0_0000_0000_0000)
// prints: true
```

⚠️ 三句提醒：

1. **`ObjectIdentifier` 问的是"是不是同一个对象"，不是"两个对象相等吗"**。后者要 `Equatable`，一个对象可以"相等但不同一"。
2. **`Unmanaged` 的引用计数归你管**：`passRetained` 之后你得负责 `release`，`takeRetainedValue` 会吃掉一次引用。用错方向就是过度释放，崩溃现场通常在几百行之外。
3. 想"看浮点的位"就写 `.bitPattern`，别上 `unsafeBitCast`——实测编译器会直接给出 `'unsafeBitCast' from 'Double' to 'UInt64' can be replaced with 'bitPattern' property on 'Double'` 这条警告。`unsafeBitCast` 留给真的没有安全替代品的时候。

⚠️ 指针不能逃逸出 `withUnsafe...` 闭包。存下来以后再用，指向的可能是已经被回收或搬走的内存，这类 bug 表现为"偶尔算错一个数"，极难定位。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 以为 `let` 类实例不可改 | `let` 锁的是指针，属性照样能改 |
| 用类做本该用结构体的东西 | 无意间的共享修改，是这类 bug 的头号来源 |
| 数组装引用类型 | 拷贝数组 ≠ 拷贝元素 |
| 代理属性写成强引用 | 典型的循环引用 |
| 闭包忘记 `[weak self]` | 控制器、视图永远不释放 |
| `unowned` 用错 | 访问已释放对象直接崩溃，不确定就用 `weak` |
| COW 与多线程 | 共享缓冲被两侧同时改写会触发多次复制，性能反而更差 |
| 同一个变量传进两个 `inout` | 编译不过：`inout arguments are not allowed to alias each other`，先复制到局部变量 |
| 全局变量 / 元组的两个属性做 `inout` | 编译器证明不了独占性，改成局部变量，或先复制再写回 |
| `size` 当 `stride` 用 | 数组下标计算出错，通常表现为"数据错位一格" |
| 指针逃逸 | 未定义行为，比崩溃更难查 |
