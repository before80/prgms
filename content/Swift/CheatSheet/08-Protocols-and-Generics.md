+++
title = "08 协议与泛型"
linkTitle = "08 协议与泛型"
weight = 80
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "协议、关联类型、主关联类型、some 与 any、协议扩展与自动合成的完整速查"
isCJKLanguage = true
draft = false
+++

# 08 协议与泛型

## 协议：一份能力清单

协议只描述"能做什么"，不描述"是什么"。任何类型——结构体、类、枚举、actor——都能遵守协议。

```swift
protocol Shape {
    var area: Double { get }          // 只要求可读
    var name: String { get set }      // 要求可读可写
    func scaled(by factor: Double) -> Self
}

struct Circle: Shape {
    var r: Double
    var name = "圆"
    var area: Double { .pi * r * r }
    func scaled(by factor: Double) -> Circle { Circle(r: r * factor) }
}

var c = Circle(r: 2)
c.name = "大圆"
print(c.name, c.area)
// prints: 大圆 12.566370614359172
```

| 协议里能写 | 说明 |
| --- | --- |
| 属性要求 | 只写 `{ get }` / `{ get set }`，不写实现 |
| 方法要求 | 签名，不写方法体 |
| 初始化器要求 | `init(...)`；非 `final` 的类实现时要写 `required`，结构体和枚举不用 |
| 关联类型 | `associatedtype Element`，可以顺带加约束：`associatedtype Element: Hashable` |
| `async` 要求 | `func fetch() async throws -> Data`，写法就是普通函数签名 |
| 静态要求 | `static func ...` |
| `mutating` 要求 | 值类型实现时可以省掉 `mutating` |
| 默认实现 | 只能写在 `extension` 里 |

⚠️ **`async` 要求是单向放宽的**：要求写成 `async`，实现方可以写成同步；要求写成同步，实现方**不能**加 `async`。这条规则很实用——同一个协议，有人用同步方式满足、有人用真异步满足，调用方都当异步调：

```swift
protocol Fetcher { func fetch() async -> Int }

struct Cached: Fetcher {
    func fetch() -> Int { 7 }          // ✅ 同步实现满足 async 要求
}

struct Remote: Fetcher {
    func fetch() async -> Int { 42 }   // ✅ 真异步也可以
}

print(await Cached().fetch(), await Remote().fetch())
// prints: 7 42
```

反过来写就会被打回：`struct S: F { func fetch() async -> Int { 1 } }` 报 `type 'S' does not conform to protocol 'F'`，下面还附一句非常好懂的注解 `candidate is 'async', but protocol requirement is not`。

### 协议组合

```swift
protocol Named { var name: String { get } }
protocol Aged { var age: Int { get } }

func describe(_ item: any Named & Aged) -> String {
    "\(item.name)（\(item.age) 岁）"
}

struct Cat: Named, Aged { var name = "咪咪"; var age = 3 }
print(describe(Cat()))
// prints: 咪咪（3 岁）
```

💭 组合里最多塞**一个类**，写法是 `any SomeClass & Named`（"某个继承自 `SomeClass`、同时遵守 `Named` 的类型"）；塞第二个类会被拒绝：`protocol-constrained type cannot contain class 'B' because it already contains class 'A'`。想表达"随便哪个遵守协议的类"，才用 `protocol P: AnyObject`。

### 协议继承：协议也能遵守协议

`protocol P: A, B` 不是"多重继承"，而是"想遵守 `P`，就得先把 `A`、`B` 也遵守了"：

```swift
protocol Named { var name: String { get } }
protocol Aged { var age: Int { get } }

protocol Person: Named, Aged {}      // Person 的要求 = Named 的要求 + Aged 的要求

struct Student: Person {             // 只写 Person，但三个协议的要求全得实现
    var name: String
    var age: Int
}

func show(_ p: any Person) -> String { "\(p.name) \(p.age)" }
print(show(Student(name: "小明", age: 12)))
// prints: 小明 12
```

**继承和组合该怎么选？** 两者都能表达"同时具备这些能力"，区别在于要不要留下一个可复用的名字：

| 写法 | 出现在哪 | 什么时候用 |
| --- | --- | --- |
| `any Named & Aged` | 类型位置（参数、变量） | 临时拼一次，用完就走 |
| `protocol Person: Named, Aged` | 声明位置 | 这个名字你打算反复用，或者想给它加扩展方法 |

💭 还有一条硬限制：**协议只能继承协议**，不能继承类。想要"某个类的子类 + 额外能力"，写法是类型位置的 `any SomeClass & Named`。

## 关联类型

协议里想提到"某个还没确定的类型"时，用 `associatedtype`：

```swift
protocol Container {
    associatedtype Element
    var items: [Element] { get }
    mutating func append(_ item: Element)
}
```

关联类型可以顺带加约束，把"元素随便什么类型"收紧成"元素必须能哈希"：

```swift
protocol Repository {
    associatedtype Item: Hashable          // 紧凑写法
    func all() -> [Item]
}

// 等价的另一种写法：把约束挪进 where 子句
protocol Repository2 {
    associatedtype Item where Item: Hashable
    func all() -> [Item]
}

struct IntRepo: Repository {
    func all() -> [Int] { [1, 2, 3] }
}

let repo: any Repository = IntRepo()
print(repo.all().count)
// prints: 3
```

🔥 约束写在协议里，实现方就不用在每个方法上重复 `where` ——这比"在 `extension` 里给每个方法补约束"干净得多。

Swift 5.7 起可以给它起个**主关联类型**的名字，之后就能直接写 `any Container<Int>`：

```swift
protocol Container<Element> {
    associatedtype Element
    var items: [Element] { get }
}

struct Box<T>: Container {
    var items: [T]
}

func firstOf(_ c: any Container<Int>) -> Int? {
    c.items.first
}

print(firstOf(Box(items: [7, 8])) ?? -1)
// prints: 7
```

🔥 主关联类型解决了 Swift 长期以来的一个痛点：以前 `Container<Int>` 只能出现在泛型约束里，不能当参数类型。现在两者都行。

## 泛型

```swift
func sumOf<E: Numeric>(_ items: [E]) -> E {
    items.reduce(0, +)
}
print(sumOf([1, 2, 3]))
// prints: 6
print(sumOf([1.5, 2.5]))
// prints: 4.0

struct Stack<Element> {
    private var storage: [Element] = []
    mutating func push(_ e: Element) { storage.append(e) }
    mutating func pop() -> Element? { storage.popLast() }
    var peek: Element? { storage.last }
}
```

| 约束写法 | 含义 |
| --- | --- |
| `<T>` | 任意类型 |
| `<T: Equatable>` | 必须遵守协议 |
| `<T: AnyObject>` | 必须是类 |
| `where T.Element == Int` | 精确匹配 |
| `where T: Sequence, T.Element: Hashable` | 多条件 |
| `where T.Element: Comparable` | 关联类型上的约束 🔥 |
| `some P` | 不透明类型，具体类型对调用方隐藏 |
| `any P` | 存在类型，运行期容器 |

```swift
extension Sequence where Element: Numeric {
    func total() -> Element { reduce(0, +) }
}
print([1, 2, 3].total())
// prints: 6
```

### 变参泛型：参数包

老问题：`func f(_ a: Int, _ b: String, _ c: Double)` 这种"类型各不相同但个数不定"的函数没法用泛型表达。Swift 5.9 起用**参数包**解决，关键字就是那个 `each`：

```swift
func describe<each T>(_ values: repeat each T) -> String {
    var parts: [String] = []
    repeat parts.append(String(describing: each values))   // 对每个值各执行一次
    return parts.joined(separator: " | ")
}

print(describe(1, "two", 3.0))
// prints: 1 | two | 3.0

struct Pair<each T> { let values: (repeat each T) }        // 元组里也能装
let p = Pair(values: (1, "a"))
print(p.values.0, p.values.1)
// prints: 1 a
```

| 写法 | 意思 |
| --- | --- |
| `<each T>` | 声明一个类型包（个数不定的一串类型） |
| `repeat each T` | 展开成"每个类型各来一个" |
| `repeat { ... each values ... }` | 对包里的每个值各执行一次 |
| `(repeat each T)` | 元组类型，可按下标取出 |

⚠️ 能用参数包的位置是有限的：函数参数、元组类型、`repeat` 语句里可以；字符串插值里不行——`"\(each values)"` 实测报 `pack reference 'each T' can only appear in pack expansion`，套一层 `String(describing:)` 就解决了。

💭 日常开发很少需要它，但读标准库和库的签名时会遇到，认识 `each` 和 `repeat` 这两个词就够了。

## `some` 与 `any`

这两个关键字是 Swift 5.7 之后最容易混淆的一对。

```swift
struct Square: Shape { var side: Double; var area: Double { side * side } }

// some：返回一个确定的、但对外隐藏的具体类型
func makeShape() -> some Shape { Circle(r: 1) }

// any：返回一个"装着某种 Shape"的盒子
func makeAnyShape(_ flag: Bool) -> any Shape {
    flag ? Circle(r: 1) : Square(side: 2)
}

let shapes: [any Shape] = [Circle(r: 1), Square(side: 2)]
print(shapes.map(\.area).reduce(0, +))
// prints: 7.141592653589793
```

| | `some P`（不透明类型） | `any P`（存在类型） |
| --- | --- | --- |
| 具体类型 | 编译期确定，但对外隐藏 | 运行期才知道 |
| 能返回不同类型吗 | ❌ 同一函数只能返回一种 | ✅ 可以按分支返回不同实现 |
| 性能 | 与直接使用具体类型相同 | 需要装箱与动态派发，慢一些 |
| 能当泛型参数用吗 | ✅ 直接传进 `func f<S: Shape>(_: S)` | 🚧 只在一个位置上"能"：单个值传进去时，Swift 会**隐式打开**这个盒子（implicitly opened existential），把 `S` 推成里面那个具体类型，于是编译通过。但只要这个 `S` 还要同时对上别的东西——`f(boxed, boxed)`、`[boxed, boxed]`、`[any Shape]` 传给 `[S]`——就露馅：`type 'any Shape' cannot conform to 'Shape' [#ProtocolTypeNonConformance]` |
| `-> Self` 的方法 | 返回的还是同一个具体类型 | 也能调用（Swift 5.7 起），但返回的是 `any Shape`，类型身份丢了 |
| 什么时候用 | 返回单一时——**默认选它** | 需要异构集合时 |

💭 一句话记法：**`some` 是"我说了算，但我不告诉你"，`any` 是"我不知道是谁，先装起来"。** 优先 `some`，需要把不同类型塞进同一个数组时才用 `any`。

两者都能用 `&` 拼多个协议，写法一样、含义不同：

```swift
protocol Named { var name: String { get } }
protocol Aged { var age: Int { get } }
struct Cat: Named, Aged { var name = "咪咪"; var age = 3 }

func makePet() -> some Named & Aged { Cat() }                  // 隐藏成一个具体类型
func describe(_ pet: any Named & Aged) -> String { "\(pet.name) \(pet.age)" }

print(makePet().name, makePet().age)
// prints: 咪咪 3
print(describe(Cat()))
// prints: 咪咪 3
```

同一个"算总面积"的需求，三种写法的差别值得看清：

{{< tabpane text=true persist=disabled >}}

{{% tab header="泛型（最快）" %}}

```swift
// 承接上文：protocol Shape、struct Circle、struct Square 都已定义
func totalArea<S: Shape>(_ shapes: [S]) -> Double {
    shapes.reduce(0) { $0 + $1.area }
}

print(totalArea([Circle(r: 1), Circle(r: 2)]))
// prints: 15.707963267948966
```

编译期就把类型定死，没有装箱也没有动态派发。代价是数组里只能放**同一种**具体类型。

{{% /tab %}}

{{% tab header="some（返回单一时）" %}}

```swift
// 承接上文：protocol Shape、struct Circle 已定义
func makeCircle() -> some Shape {
    Circle(r: 3)
}

print(makeCircle().area)
// prints: 28.274333882308138
```

对调用方隐藏了具体类型，但内部依然是具体类型，性能与泛型相同。

💭 它不只出现在函数上：属性也能用，SwiftUI 那句天天见的 `var body: some View { ... }` 就是同一个机制——"我保证返回某个具体的 `View`，但具体是谁不方便说"。

{{% /tab %}}

{{% tab header="any（异构集合）" %}}

```swift
// 承接上文：protocol Shape、struct Circle、struct Square 已定义
let shapes: [any Shape] = [Circle(r: 1), Square(side: 2)]
print(shapes.map(\.area).reduce(0, +))
// prints: 7.141592653589793
```

能混装不同实现，代价是每个 `area` 访问都要查一次表。

{{% /tab %}}

{{< /tabpane >}}

⚠️ `any` 会让关联类型跟着退化。写 `let s: any Sequence = [1, 2, 3]` 时元素类型变成**实打实的 `Any`**——`s.map { $0 }` 的闭包参数拿到的是 `Any`，`Array(s)` 得到 `[Any]`，只是这些算法本身照样跑得动。

⚠️ 但**依赖 `Element: Equatable` 的那批 API 会跟着失效**，这是 `any` 最容易被忽略的代价：

```swift
let s: any Sequence = [1, 2, 3]

print(s.contains { ($0 as? Int) == 2 })   // ✅ 谓词版本能编译，得自己转型
// prints: true
// print(s.contains(2))                   // 🛑 missing argument label 'where:' in call
//                                        //    元素是 Any，Any 不 Equatable，只能给谓词
// print(s.firstIndex(of: 2))             // 🛑 另外 firstIndex(of:) 是 Collection 的成员，
//                                        //    Sequence 上本来就没有，和 any 无关
```

把主关联类型写全——`any Sequence<Int>`——元素类型才保得住，`contains(2)` 这类"按值找"的重载也就回来了。至于 `count` 这种能力，它属于 `Collection` 而不是 `Sequence`，`any Sequence` 上本来就没有，别把这笔账算到 `any` 头上。真遇到"套上 `any` 就编译不过"，通常说明这里该用 `some`，或者把泛型参数一路写下去。

## 协议扩展与默认实现

协议本身不能写实现，但它的扩展可以：

```swift
protocol Greeter {
    var name: String { get }
    func greet() -> String
}

extension Greeter {
    func greet() -> String { "你好，我是 \(name)" }     // 默认实现
    func greetLoudly() -> String { greet().uppercased() + "!" }
}

struct Guest: Greeter { let name: String }                        // 用默认实现
struct Vip: Greeter {
    let name: String
    func greet() -> String { "尊贵的 \(name)，你好" }              // 覆盖默认实现
}

print(Guest(name: "小明").greetLoudly())
// prints: 你好，我是 小明!
print(Vip(name: "老王").greetLoudly())
// prints: 尊贵的 老王，你好!
```

⚠️ **这是一块很容易踩空的地方。** 只有当方法是**协议要求**时，通过 `any` 调用才会走动态派发：

```swift
protocol P {}
extension P { func f() -> String { "扩展里的实现" } }   // 不是协议要求
struct S: P { func f() -> String { "结构体里的实现" } }

let s = S()
print(s.f())
// prints: 结构体里的实现
let boxed: any P = s
print(boxed.f())
// prints: 扩展里的实现     ← 只写在扩展里、没进协议要求的默认实现会被静态派发
```

结论只有一句：**想让默认实现在 `any` 上也生效，就必须把它同时写进协议要求里。** 💭

## 条件遵循

一个类型只在特定条件下才遵守某协议：

```swift
struct Wrapper<T> { var value: T }

extension Wrapper: Equatable where T: Equatable {}

print(Wrapper(value: 1) == Wrapper(value: 1))
// prints: true
```

`Array` 本身就是这么干的：`Array` 在 `Element: Equatable` 时才 `Equatable`，在 `Element: Hashable` 时才 `Hashable`。

```swift
extension Array where Element: Comparable {
    var isSorted: Bool { self == sorted() }
}
print([1, 2, 3].isSorted, [3, 1].isSorted)
// prints: true false
```

## 编译器能替你合成的协议

这几个协议在条件满足时会自动生成实现，不需要手写：

| 协议 | 合成条件 | 备注 |
| --- | --- | --- |
| `Equatable` | 所有存储属性都是 `Equatable` | 结构体与枚举都能合成 |
| `Hashable` | 所有存储属性都是 `Hashable` | 合成 `==` 与 `hash(into:)` |
| `Codable` | 所有存储属性都是 `Codable` | 键名默认等于属性名 |
| `CaseIterable` | 枚举没有关联值 | 生成 `allCases` |
| `RawRepresentable` | 枚举有原始值 | 自带 `init?(rawValue:)` |

```swift
enum Status: Equatable, Hashable { case ok(Int), failed(String) }

print(Status.ok(200) == Status.ok(200))
// prints: true
print(Set([Status.ok(1), Status.ok(1), .failed("x")]).count)
// prints: 2
```

⚠️ `Comparable` **不会**自动合成。`<` 只是标准库给数值、字符串、元组这些内置类型准备好的，你自己的类型要排序，得手写 `<`。

## 类型擦除

需要把"不同具体类型、同一种能力"装进同一个容器时，用 `any` 通常就够了。只有当你还需要泛型能力时，才需要手写擦除包装：

```swift
protocol ShapeLike {
    var area: Double { get }
    var name: String { get }
}

struct AnyShapeLike: ShapeLike {
    private let _area: () -> Double
    private let _name: () -> String

    init<S: ShapeLike>(_ shape: S) {
        _area = { shape.area }
        _name = { shape.name }
    }

    var area: Double { _area() }
    var name: String { _name() }
}

struct CircleLike: ShapeLike {
    var r: Double
    var name = "圆"
    var area: Double { .pi * r * r }
}

print(AnyShapeLike(CircleLike(r: 1)).name, AnyShapeLike(CircleLike(r: 1)).area)
// prints: 圆 3.141592653589793
```

💭 现在这个手艺的用武之地大幅减少了：`any` 已经能做大部分事，`some` 解决了返回类型的问题。手写擦除只在"要隐藏泛型参数、又必须保留强类型"时才值得。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 默认实现没进协议要求 | 通过 `any` 调用时会被静态派发，走到扩展版本 |
| `let` 满足 `{ get set }` | 不行，必须是 `var` |
| 协议里的 `init` 要求与类 | 非 `final` 的类实现时必须写 `required`；结构体和枚举不用 |
| 用 `any` 装异构类型 | 每个方法调用都有装箱成本，热路径上先考虑泛型 |
| 关联类型被 `any` 擦掉 | 需要关联类型参与运算时用 `some` 或泛型 |
| 忘记 `Self` 的含义 | `-> Self` 的方法在 `any` 上能调用，但返回的也只是一个 `any` 盒子，类型关系已经丢了 |
| 协议扩展里放存储属性 | 不允许，扩展不能加存储 |
| 滥用继承代替协议 | 优先协议 + 组合，继承只在确实有"是一个"关系时用 |
