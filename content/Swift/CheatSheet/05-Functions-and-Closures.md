+++
title = "05 函数与闭包"
linkTitle = "05 函数与闭包"
weight = 50
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "参数标签、可变参数、inout、闭包简写、捕获列表与 @escaping 的完整速查"
isCJKLanguage = true
draft = false
+++

# 05 函数与闭包

## 函数声明的解剖

```swift
func greet(_ name: String, from city: String = "北京", times: Int = 1) -> String {
    Array(repeating: "你好，\(name)（来自 \(city)）", count: times).joined(separator: "\n")
}

print(greet("Swift"))
// prints: 你好，Swift（来自 北京）
print(greet("Kotlin", from: "上海", times: 2))
// prints: 你好，Kotlin（来自 上海）
//         你好，Kotlin（来自 上海）
```

读法要按这个顺序：

| 位置 | 名称 | 说明 |
| --- | --- | --- |
| `greet` | 函数名 | |
| `_ name` | 外部标签 `_` + 内部名 `name` | `_` 表示调用时**不写标签** |
| `from city` | 外部标签 `from` + 内部名 `city` | 调用时写 `from:` |
| `= "北京"` | 默认值 | 有默认值的参数可以省略 |
| `-> String` | 返回类型 | 省略表示返回 `Void` |

🔥 参数标签是为了让调用点读起来像句子：`greet("A", from: "B")` 比 `greet("A", "B")` 多花三个字符，但半年后你还能看懂。

⚠️ 外部标签在函数**第一版发布**后就属于 API 的一部分。改标签会破坏所有调用方，所以命名时多想两秒。

## 参数玩法

| 需求 | 写法 |
| --- | --- |
| 省略标签 | `func f(_ x: Int)` |
| 只写一个名字（内外同名） | `func f(x: Int)` |
| 只在内部换名 | `func f(printable value: Int)` |
| 默认值 | `func f(x: Int = 0)` |
| 可变参数 | `func f(_ values: Int...)` |
| 传入并回写 | `func f(_ x: inout Int)` |
| 泛型参数 | `func f<T: Equatable>(_ x: T)` |
| 不透明参数（5.7+） | `func f(_ x: some Equatable)` |
| 存在类型参数 | `func f(_ x: any Equatable)` |

```swift
func sum(_ values: Int...) -> Int {
    values.reduce(0, +)
}
print(sum(1, 2, 3))
// prints: 6

func double(_ x: inout Int) {
    x *= 2
}
var v = 21
double(&v)
print(v)
// prints: 42
```

⚠️ 参数上的四个坑，全都在编译期就被拦下，不会拖到运行时：

- 第一个可变参数之后的所有参数**必须带标签**。`func f(_ v: Int..., w: String...)` 合法，`func f(_ v: Int..., _ w: String...)` 报 `a parameter following a variadic parameter requires a label`。
- 可变参数不能设默认值，也不能写成 `inout`。`func f(_ v: Int... = [])` 报 `variadic parameter cannot have a default value`，`func f(_ v: inout Int...)` 报 `'inout' must not be used on variadic parameters`。
- `inout` 参数不能有默认值。`func f(_ v: inout Int = 0)` 报 `cannot provide default value to inout parameter 'v'`。
- `inout` 参数不能被**逃逸**闭包捕获。`let c = { x }` 报 `escaping closure captures 'inout' parameter 'x'`；只有不存在逃逸风险的场景，例如把闭包交给 `() -> Int` 这样的非逃逸参数当场用完，才写得通。

💭 `some Equatable` 与 `any Equatable` 的区别是编译期类型擦除与运行期容器，细节见 [08 协议与泛型]({{< relref "08-Protocols-and-Generics.md" >}})。

## 返回值

```swift
// 单一返回值
func square(_ x: Int) -> Int { x * x }

// 元组：一次返回多个值
func minMax(_ a: [Int]) -> (min: Int, max: Int)? {
    guard let lo = a.min(), let hi = a.max() else { return nil }
    return (lo, hi)
}

if let result = minMax([3, 1, 4]) {
    print(result.min, result.max)
}
// prints: 1 4

// 不关心返回值时可以丢弃，但默认会给出警告：
@discardableResult
func log(_ s: String) -> Int { s.count }
log("这行不会产生警告")
```

🔥 单表达式函数可以省略 `return`。多行函数不行——这是 Swift 5.1 起就有的老规矩，但写法上很容易混。

## 函数是值

函数可以赋给变量、作为参数、作为返回值，类型写成 `(参数类型) -> 返回类型`。

```swift
let add: (Int, Int) -> Int = { $0 + $1 }
print(add(2, 3))
// prints: 5

func apply(_ x: Int, transform: (Int) -> Int) -> Int {
    transform(x)
}
print(apply(5) { $0 * $0 })
// prints: 25
print(apply(5, transform: { $0 + 1 }))
// prints: 6

// 嵌套函数：只在外部函数里可见
func outer(_ n: Int) -> Int {
    func twice(_ x: Int) -> Int { x * 2 }
    return twice(n) + 1
}
print(outer(10))
// prints: 21
```

## 闭包：从完整写法到一行简写

闭包和函数是同一件事，只是把 `func` 换成了花括号。Swift 允许你层层删掉冗余部分，下面五个版本**完全等价**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="① 最完整" %}}

```swift
let squares = [1, 2, 3].map { (n: Int) -> Int in
    return n * n
}
print(squares)
// prints: [1, 4, 9]
```

类型、参数名、`return` 全都写着。看不出任何歧义，也最啰嗦。

{{% /tab %}}

{{% tab header="② 省类型" %}}

```swift
let squares = [1, 2, 3].map { n -> Int in
    return n * n
}
```

编译器能从 `map` 的签名推出 `n` 是 `Int`。

{{% /tab %}}

{{% tab header="③ 省 return" %}}

```swift
let squares = [1, 2, 3].map { n in
    n * n
}
```

闭包体只有一条表达式时，它本身就是返回值。

{{% /tab %}}

{{% tab header="④ 用 $0" %}}

```swift
let squares = [1, 2, 3].map { $0 * $0 }
```

`$0`、`$1` 是按位置编号的隐式参数。参数超过两个、或者嵌套闭包时，请退回给参数起名字。

{{% /tab %}}

{{% tab header="⑤ 用方法/运算符" %}}

```swift
let values = ["1", "2", "3"].compactMap(Int.init)
let total = values.reduce(0, +)
print(values, total)
// prints: [1, 2, 3] 6
```

已经有现成函数能表达意图时，直接传函数或运算符，比再写一个闭包更短也更清楚。

{{% /tab %}}

{{< /tabpane >}}

### 尾随闭包

闭包是**最后一个参数**时，可以把它提到括号外面：

```swift
func retry(times: Int, task: () -> Void) { for _ in 0..<times { task() } }

retry(times: 3) { print("尝试") }        // 尾随闭包
retry(times: 3, task: { print("尝试") }) // 等价写法
```

Swift 5.3 起支持**多个尾随闭包**，第一个不带标签，后面都带：

```swift
func configure(setup: () -> Void, completion: () -> Void) {
    setup(); completion()
}

configure {
    print("setup")
} completion: {
    print("completion")
}
// prints: setup
//         completion
```

⚠️ **在 `if` / `while` / `guard` / `switch` 的条件里写尾随闭包会换来一条警告。** 这些位置的花括号已经被语句体占用了，编译器得猜你那个 `{ }` 到底是参数还是代码块，于是干脆抱怨一句：

```swift
func isReady() -> Bool { true }
func check(_ body: () -> Bool) -> Bool { body() }

if isReady() {
    print("这是 if 的代码块")
}

if check({ true }) {          // 想传闭包就老老实实写进括号里
    print("显式传参才没有歧义")
}
// prints: 这是 if 的代码块
//         显式传参才没有歧义
```

写成 `if check { true } { print("ok") }` 其实也能编过（实测行为与显式传参完全一致），代价是这样一条警告：

```console
tc.swift:2:10: warning: trailing closure in this context is confusable with the body of the statement; pass as a parenthesized argument to silence this warning
```

💭 Swift 5.3 之前这里是**硬错误**，SE-0286 之后放宽成警告。所以别看到网上老教程说"编译不过"就觉得新编译器坏了——语法是刻意放开的，但把它写进括号仍然是最省事的做法。

## 捕获：闭包会记住它看到的东西

闭包会**捕获**它引用到的外部变量，而不是复制一份值。这意味着闭包让一个变量的生命周期超出了它的作用域：

```swift
func makeCounter() -> () -> Int {
    var count = 0
    return { count += 1; return count }
}
let counter = makeCounter()
print(counter(), counter(), counter())
// prints: 1 2 3
```

`count` 本该在 `makeCounter` 返回时消失，但因为有闭包引用它，编译器把它搬到了堆上。这就是"闭包捕获"的字面含义。

### 捕获列表

当闭包持有对象、又可能长期存活时，需要显式控制引用关系，否则就是循环引用。

{{< tabpane text=true persist=disabled >}}

{{% tab header="强引用（默认）" %}}

```swift
final class Counter {
    var value = 0
    func increment() { value += 1 }
}

let c = Counter()
let block = { c.increment() }   // 闭包强持有 c
block()
print(c.value)
// prints: 1
```

闭包和对象互相持有就是循环引用，谁都不会被释放。UI 回调里这是常见泄漏源。

{{% /tab %}}

{{% tab header="[weak self]" %}}

```swift
final class Counter {
    var value = 0
    func makeIncrementer(by step: Int) -> () -> Void {
        { [weak self] in
            guard let self else { return }   // 对象没了就直接退出
            self.value += step
        }
    }
}

let c = Counter()
let inc = c.makeIncrementer(by: 5)
inc(); inc()
print(c.value)
// prints: 10
```

🔥 90% 的场景都用它。`guard let self else { return }` 是标准起手式。

{{% /tab %}}

{{% tab header="[unowned self]" %}}

```swift
final class Node {
    var name = "root"
    lazy var describe: () -> String = { [unowned self] in self.name }
}

let n = Node()
print(n.describe())
// prints: root
```

不持有、也不判空，直接用。**前提是你能保证两者同生共死**，否则访问已释放对象会当场崩溃。不确定就用 `weak`。

{{% /tab %}}

{{% tab header="按值捕获 [x]" %}}

```swift
var message = "初始值"
let snapshot = { [message] in message }
message = "改过了"
print(snapshot())
// prints: 初始值
```

想冻结某一刻的值（比如循环里创建一堆回调），把变量写进捕获列表即可。省略它的话，所有闭包看到的都是同一份最新值。

{{% /tab %}}

{{< /tabpane >}}

## @escaping 与非逃逸

闭包参数默认是**非逃逸**的：它必须在函数返回前用完。这允许编译器省掉一堆开销，也禁止了"把参数存起来以后再用"。

```swift
func perform(_ body: @escaping () -> Void) { body() }

func store(_ body: @escaping () -> Void) -> () -> Void {
    body              // 存起来以后再调用，必须标 @escaping
}
```

| 标记 | 含义 | 后果 |
| --- | --- | --- |
| 默认（非逃逸） | 函数返回前用完 | 性能更好，无引用环风险 |
| `@escaping` | 可能被存起来或异步调用 | 捕获 `self` 时要显式写 `self.`，容易形成循环引用 |
| `@Sendable` | 可以跨并发域传递 | 捕获的值必须本身是 `Sendable` 🔥 |

```swift
func perform(_ body: @escaping @Sendable () -> Void) { body() }
perform { print("sendable ok") }
// prints: sendable ok
```

⚠️ 从 `@escaping` 闭包里访问属性，编译器**强制**你写 `self.value`，就是提醒你"注意，这里会持有 self"。

两个和"捕获"有关的对照实验，都很容易想反：

```swift
// 1. 默认值每次调用都重算
func demo() {
    final class Ticker {                     // 局部类，只为让输出可预测
        var n = 0
        func next() -> Int { n += 1; return n }
    }
    let ticker = Ticker()

    func f(x: Int = ticker.next()) -> Int { x }
    print(f(), f(), f())
}
demo()
// prints: 1 2 3      每调一次 f()，默认值表达式就重新求值一次

// 2. for-in 的循环变量每轮都是新的
var fns: [() -> Void] = []
for i in 0..<3 { fns.append { print(i) } }
fns.forEach { $0() }
// prints:
//   0
//   1
//   2

// 对照：循环外那个 var 才是共享的
var shared = 0
var fns2: [() -> Void] = []
for _ in 0..<3 { fns2.append { print(shared) }; shared += 1 }
fns2.forEach { $0() }
// prints:
//   3
//   3
//   3
```

## @autoclosure：把表达式包成闭包

```swift
func assertTrue(_ condition: @autoclosure () -> Bool, _ message: String = "") {
    if !condition() {
        print("断言失败: \(message)")
    }
}

assertTrue(1 + 1 == 2)                    // 传表达式的样子
assertTrue(1 + 1 == 3, "数学崩了")
// prints: 断言失败: 数学崩了
```

`@autoclosure` 让调用方写 `assertTrue(x > 0)` 而不是 `assertTrue { x > 0 }`。副作用是**求值时机被推迟**——表达式不会先求值再传参。仅在你确实需要延迟求值（断言、日志、`??`）时使用，滥用会让调用点看起来像普通传参，实际却在做延迟计算。💭

## 把 KeyPath 和运算符当参数

```swift
let people = [(name: "Bob", age: 25), (name: "Alice", age: 30)]

print(people.map(\.name))
// prints: ["Bob", "Alice"]
print(people.map(\.name).sorted())
// prints: ["Alice", "Bob"]
print([3, 1, 2].sorted(by: >))
// prints: [3, 2, 1]
print([3, 1, 2].reduce(0, +))
// prints: 6
```

`\.name` 是 `KeyPath<Element, String>`，它能直接当 `(Element) -> String` 用。更细的 KeyPath 玩法见 [11 标准库速查]({{< relref "11-Standard-Library.md" >}})。

## rethrows：只转发别人的错误

有些函数自己永远不会出错，只是"替你把闭包跑一遍"。这种函数不该逼调用方 `try`，正确写法是 `rethrows`：

```swift
enum ParseError: Error { case bad }

func measure(_ work: () throws -> Int) rethrows -> Int {
    try work()
}

print(measure { 42 })
// prints: 42               闭包不抛错，调用点连 try 都不用写

do {
    let n = try measure { throw ParseError.bad }
    print(n)
} catch {
    print("接住了 \(error)")
}
// prints: 接住了 bad       闭包抛错，调用点就必须 try
```

三个关键字的区别：

| 关键字 | 含义 | 调用点 |
| --- | --- | --- |
| `throws` | 我自己可能抛错 | 必须 `try` |
| `rethrows` | **只有**参数里的闭包抛错时我才抛错 | 传的闭包不抛错就不用 `try` |
| `try!` / `try?` | 把抛错压平 | 见 [09 章]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |

⚠️ 两条硬规则，都实测过：

1. **`rethrows` 函数至少要收一个会抛错的闭包参数**，否则报 `'rethrows' function must take a throwing function argument`。
2. **函数体里不能自己 `throw`**，只能原样转发别人抛的错，否则报 `a function declared 'rethrows' may only throw if its parameter does`。

💭 标准库里 `map`、`filter`、`reduce`、`sorted` 的闭包版本全是 `rethrows`——这也解释了为什么给它们传一个不抛错的闭包时，你从来不用写 `try`。

## withoutActuallyEscaping：暂时借它一个"逃逸"身份

有些 API 的签名写死了 `@escaping`，实际上却在函数返回前就用完了。这时可以把一个非逃逸闭包"临时借出去"，条件是**你保证它没有真的逃逸**：

```swift
// 一个"老"函数：签名写的是 @escaping，其实只在内部同步用完
func legacyMap(_ values: [Int], _ transform: @escaping (Int) -> Int) -> [Int] {
    values.map(transform)
}

// 我们的参数是非逃逸的，直接转发会编译不过
func doubled(_ values: [Int], using transform: (Int) -> Int) -> [Int] {
    withoutActuallyEscaping(transform) { escaping in
        legacyMap(values, escaping)
    }
}

print(doubled([1, 2, 3], using: { $0 * 2 }))
// prints: [2, 4, 6]
```

不做这层包装，直接写 `legacyMap(values, transform)` 会报 `passing non-escaping parameter 'transform' to function expecting an '@escaping' closure`（实测）。

🛑 **`withoutActuallyEscaping` 是一句承诺，不是免死金牌。** 只要闭包真的活过了这次调用（被存进全局变量、扔进异步队列、塞给别的线程），运行期就是未定义行为，崩溃点可能在几个文件之外。拿不准的时候，把函数签名改成 `@escaping` 更安全。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 忘记外部标签 | Swift 默认要求写标签，只有 `_` 才省略 |
| 以为默认参数只算一次 | 默认值在**每次调用**时求值，写 `= Int.random(in: 1...6)` 每次都是新值 |
| 在闭包里改 `let` | 捕获的 `let` 不能改，需要的是 `var` |
| 循环里捕获循环变量 | `for i in 0..<3` 里的 `i` 每轮都是新的，闭包各拿各的；真正会串的是循环外那个 `var` |
| `@escaping` 忘了 `self.` | 编译器会报错，这是保护不是刁难 |
| `weak self` 后忘了解包 | 解开后统一用 `guard let self`，别到处 `self?.` |
| 非逃逸闭包想存起来 | 加 `@escaping`，或者改为返回闭包 |
| 闭包与协议混用 | 闭包不能遵守协议，需要包装成 `struct` |
