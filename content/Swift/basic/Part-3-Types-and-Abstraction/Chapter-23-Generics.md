+++
title = "第23章 泛型：写一次，适配很多类型"
weight = 230
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十三章：泛型：写一次，适配很多类型

> 泛型的价值不是少写几行，而是让代码表达“对任意满足条件的类型都成立”。它把重复逻辑提升成通用工具，还能在编译期保留类型信息。代价是抽象层级提高，约束写得太宽或太窄都会让 API 变难用。

## 23.1 泛型函数

泛型函数的写法：在函数名后面加一对尖括号，给“暂时先不定的那个类型”起个名字。

```swift
func firstOrNil<T>(_ values: [T]) -> T? {
    values.first
}

print(firstOrNil([1, 2, 3]) as Any)
// prints: Optional(1)
print(firstOrNil(["a", "b"]) as Any)
// prints: Optional("a")
```

`<T>` 是类型参数。编译器会根据实参推断 `T`，调用方通常不需要手写类型。

注意调用处写的是 `firstOrNil([1, 2, 3])` 而不是 `firstOrNil<Int>([1, 2, 3])`，两种都能编译，但**能推断就别显式写**：显式写类型参数既啰嗦，又会在类型改动的将来多一处要改的地方。

类型参数的名字也有惯例，读别人的代码时会反复遇到：`T`（最泛的"某某类型"）、`Element` / `Item`（集合元素）、`Key` / `Value`（映射关系）、`Wrapped`（包装的那个东西）、`Content`（视图内容）。

泛型参数可以有多个：

```swift
func pair<A, B>(_ first: A, _ second: B) -> (A, B) {
    (first, second)
}
print(pair(1, "one"))
// prints: (1, "one")
```

## 23.2 泛型类型

结构体、类和枚举都可以泛型化：

```swift
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        items.popLast()
    }

    var count: Int { items.count }
}

var stack = Stack<Int>()
stack.push(10)
stack.push(20)
print(stack.pop() as Any, stack.count)
// prints: Optional(20) 1
```

泛型类型保存的是具体类型信息：`Stack<Int>` 和 `Stack<String>` 是不同类型，不能混用。

这里有一个和"类型擦除"密切相关的推论：既然 `Stack<Int>` 和 `Stack<String>` 是两个不同的具体类型，那么"把它们的实例放进同一个数组"就需要 `any`（23.6 节会讲）。反过来，如果只是想写"能装东西的栈"，把类型参数留给调用方，就得到了编译期零开销的泛型版本。**这两条路不是优劣关系，而是"要不要在编译期知道具体类型"的取舍。**

## 23.3 约束：把范围收窄到可操作的类型

在类型参数后写冒号，就能要求它遵循协议：

```swift
func largest<T: Comparable>(_ values: [T]) -> T? {
    values.max()
}

print(largest([3, 1, 4, 2]) as Any)
// prints: Optional(4)
```

没有 `Comparable` 约束时，泛型函数不知道 `>` 是否存在。约束不是限制自由，而是给代码提供可依赖的能力。

约束写得太宽（什么都不要求）会让函数体里什么也做不了；写得太窄（要求一堆具体协议）会把 API 焊死。判断标准很简单：**函数体里真正用到的能力，才写进约束。**

多个约束可以用 `where`：

```swift
func joined<T>(_ values: [T]) -> String
where T: CustomStringConvertible, T: Equatable {
    values.map(\.description).joined(separator: ",")
}

print(joined([1, 2, 3]))
// prints: 1,2,3
```

`where` 也可以约束关联类型：

```swift
import Foundation

protocol CollectionLike {
    associatedtype Element
    var elements: [Element] { get }
}

func firstMatch<C: CollectionLike>(in collection: C, matching target: C.Element) -> C.Element?
where C.Element: Equatable {
    collection.elements.first { $0 == target }
}

struct Bag<Element>: CollectionLike {
    var elements: [Element]
}

print(firstMatch(in: Bag(elements: [1, 2, 3]), matching: 2) as Any)
// prints: Optional(2)
```

这段代码把泛型的"约束"用到了实处：函数不知道 `C` 是什么类型，但通过 `CollectionLike` 知道它有 `elements`，通过 `where C.Element: Equatable` 才知道可以用 `==`。**泛型函数的每一次能力扩张，都要在签名里明码标价。** 这也是为什么泛型函数签名常常一眼看不出实现——它把"我依赖什么"写全了。

## 23.4 泛型下标与泛型方法

方法可以拥有自己的类型参数：

```swift
struct Box<Value> {
    var value: Value

    func mapped<T>(_ transform: (Value) -> T) -> Box<T> {
        Box<T>(value: transform(value))
    }
}

let box = Box(value: 3)
print(box.mapped { $0 * 2 }.value)
// prints: 6
```

下标也可以泛型化：

```swift
struct DictionaryView<Key: Hashable, Value> {
    var storage: [Key: Value] = [:]

    subscript(key: Key) -> Value? {
        get { storage[key] }
        set { storage[key] = newValue }
    }
}
```

## 23.5 关联类型与泛型的配合

协议里的 `associatedtype` 经常与泛型约束一起出现：

```swift
protocol Producer {
    associatedtype Output
    func produce() -> Output
}

func consume<P: Producer>(_ producer: P) -> P.Output {
    producer.produce()
}
```

Swift 支持主关联类型，让 `any` 写法更短：

```swift
protocol Producer<Output> {
    associatedtype Output
    func produce() -> Output
}

let producers: [any Producer<Int>] = []
print(producers.count)
// prints: 0
```

## 23.6 `some` 与 `any` 的选择

回到第 22 章的两个关键词，现在可以给出更完整的判断：

- `some`：具体类型对调用者隐藏，但编译器知道它，适合返回值和链式接口。
- `any`：运行时可容纳不同类型，适合集合、参数和需要擦除类型的位置。

```swift
import Foundation

protocol Container {
    var count: Int { get }
}

struct IntBox: Container {
    var count: Int { 3 }
}

func makeContainer() -> some Container {
    IntBox()                       // 返回类型对调用者不可见
}

let containers: [any Container] = [IntBox(), IntBox()]   // 盒子里装不同实现
print(makeContainer().count, containers.count)
// prints: 3 2
```

两者的差别可以浓缩成一句话：**`some` 是"我知道，但你不用知道"；`any` 是"运行时才知道是谁"。** 前者的代价是"同一函数只能有一种返回类型"，后者的代价是每次调用都要经过一层动态派发，而且很多泛型约束（比如 `==`）在 `any` 上用不了。

如果一个函数有多种返回类型分支，`some` 就会失败：

```text
error: function declares an opaque return type 'some Container', but the return statements in its body do not have matching underlying types
```

这时应该返回 `any`，或者用泛型设计让具体类型由调用方决定。

`some` 也可以出现在参数位置，表示“调用者传入某个具体类型，函数内部只把它当作协议使用”：

```swift
func describe(_ value: some CustomStringConvertible) -> String {
    value.description
}

print(describe(42))
// prints: 42
```

参数位置的 `some` 等价于一个被编译器悄悄补上的泛型参数。它适合“我只关心能力，不需要知道具体类型”的函数签名。

## 23.7 值泛型与参数包

Swift 6 系列继续扩展泛型能力。值泛型允许把整数等值作为类型参数：

```swift
struct Vector<let Count: Int> {
    var storage = InlineArray<Count, Double>(repeating: 0)
}

var v = Vector<3>()
v.storage[0] = 1.5
v.storage[2] = 2.5
print(v.storage.count, v.storage[0], v.storage[2])
// prints: 3 1.5 2.5
```

`Vector<3>` 里的 `3` 是**类型参数**，不是构造参数。`Vector<3>` 和 `Vector<4>` 是两个不同的类型，各自长度在编译期就定死，因此不需要堆分配，也没有“长度意外变了”这回事。函数可以继续把长度参数化：

```swift
func total<let N: Int>(_ vector: Vector<N>) -> Double {
    var sum = 0.0
    for i in 0..<vector.storage.count {   // 循环上界来自类型参数，编译器一清二楚
        sum += vector.storage[i]
    }
    return sum
}

print(total(v))
// prints: 4.0
```

`InlineArray` 是 Swift 6.2 起提供的固定大小数组，适合需要避免堆分配的场景。参数包则允许函数接收数量可变的类型参数：

```swift
func tuple<each T>(_ values: repeat each T) -> (repeat each T) {
    (repeat each values)
}

print(tuple(1, "two", 3.0))
// prints: (1, "two", 3.0)
```

`repeat each` 不只是拼元组的语法糖，它也能用在循环里——循环体会对每个实参各执行一次：

```swift
func howMany<each T>(_ values: repeat each T) -> Int {
    var n = 0
    for _ in repeat each values { n += 1 }
    return n
}

print(howMany(1, "two", 3.0, true))
// prints: 4
```

把两个例子放在一起看就明白参数包想解决什么了：以前要写 `tuple2`、`tuple3`、`tuple4` 这类同构重载，现在一个 `tuple` 就能覆盖任意个数与任意类型组合。

值泛型和参数包属于进阶工具。能清楚表达"固定大小"或"任意数量类型"时再用，不要为了展示语法而把简单问题复杂化。

### 什么时候不该用泛型

泛型是有价格的：签名更长、错误信息更难读、调用方要花更多脑力。出现下面几种情况时，用具体类型往往更好：

| 情况 | 更合适的做法 |
| --- | --- |
| 类型参数在函数体里一次都没用到 | 删掉它，或者用 `_ =` 明确表示不关心 |
| 只有两三个固定类型 | 直接写重载，编译器错误信息会友好得多 |
| 需要的是"运行时可换" | 用协议 + `any`，而不是泛型 |
| 约束堆了三四个协议 | 先定义一个协议把能力打包，再约束那一个协议 |

判断的实用标准：**如果你发现自己要为用户解释这个泛型怎么用超过一句话，它可能抽象过头了。**

## 23.8 类型化抛出与泛型

泛型函数也可以声明自己抛出哪一种错误：

```swift
enum ReadError: Error { case missing }

func require<T>(_ value: T?) throws(ReadError) -> T {
    guard let value else { throw .missing }
    return value
}

do {
    print(try require(Optional(42)))
    // prints: 42
} catch {
    print(error)
}
```

`throws(E)` 可以和泛型一起使用，但错误类型会成为签名的一部分。泛型 API 越是公共，越要谨慎把错误类型收得过窄，否则以后新增错误会破坏调用者代码。

## 23.9 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 泛型函数 | 用 `<T>` 声明可替换类型 |
| 泛型类型 | 结构体、类、枚举都可以泛型化 |
| 约束 | 冒号与 `where` 提供可依赖能力 |
| 关联类型 | 协议中的泛型占位符 |
| `some` | 隐藏具体类型但保留编译期身份 |
| `any` | 运行时承载任意符合协议的类型 |
| 值泛型 | 把值作为类型参数，适合固定大小结构 |
| 参数包 | 处理任意数量类型参数 |

## 23.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 泛型参数没有约束却直接调用 `==` | 需要 `Equatable` 等约束 |
| 以为 `any` 和 `some` 可以随意互换 | 前者擦除类型，后者保留具体类型 |
| 用 `some` 返回多个具体类型 | 必须始终返回同一种类型 |
| 把值泛型当成运行期长度 | 它是编译期类型信息 |
| 在简单函数上滥用参数包 | 复杂度上升，收益很小 |
| 公共 API 过度使用类型化抛出 | 新错误会破坏兼容性 |

## 23.11 下章预告

泛型已经把你带到类型系统的中段。下一章补齐存在类型、类型擦除、元类型、`Self`、`Any`、`KeyPath`、`callAsFunction` 等零碎但重要的拼图，让整套类型地图完整起来。
