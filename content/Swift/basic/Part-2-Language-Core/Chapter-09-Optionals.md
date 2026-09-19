+++
title = "第9章 可选值：Swift 安全感的源头"
weight = 90
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第九章：可选值：Swift 安全感的源头

> 几乎所有语言都被“这个值可能不存在”折磨过。Swift 选择把这种可能性写进类型系统：`Int` 和 `Int?` 是两个不同的类型。编译器不会让你忘记处理“没有值”的情况，这就是 Swift 让人安心的核心原因之一。

## 9.1 `nil` 不是空对象，而是“没有值”

只有可选类型才能赋值为 `nil`：

```swift
var nickname: String? = "Kai"
print(nickname as Any)
// prints: Optional("Kai")

nickname = nil
print(nickname as Any)
// prints: nil
```

下面的写法不能通过编译，因为 `String` 类型的变量不允许缺席：

```text
error: 'nil' cannot initialize specified type 'String'
```

问号紧贴类型，不是紧贴变量名。两种写法等价：

```swift
var a: Int? = nil
var b: Optional<Int> = nil
print(a as Any, b as Any)
// prints: nil nil
```

`Int?` 只是 `Optional<Int>` 的语法糖。完整定义会在第 16 章揭开：可选值本质上是一个枚举，有 `.some(value)` 和 `.none` 两个分支。现在只要先记住：可选值是“盒子”，里面要么装着一个值，要么什么都没有。

## 9.2 读取可选值：先证明它存在

直接拿 `String?` 去调用 `String` 的方法会失败：

```text
error: value of optional type 'String?' must be unwrapped
```

最小心的做法是可选绑定：

```swift
if let name = nickname {
    print("Hello, \(name)")
} else {
    print("还没有昵称")
}
// prints: 还没有昵称
```

常用的简写方式省掉重复的名字：

```swift
nickname = "Kai"
if let nickname {
    print(nickname.uppercased())
    // prints: KAI
}
```

这种省掉重复名字的绑定简写不只用在 `if let` 上，`guard let`、`while case let x?` 都有对应形式，统一整理在第 15B.8 节。

可选绑定还能同时检查多个值，任意一个为 `nil` 就进入 `else`：

```swift
let first: String? = "A"
let second: String? = "B"

if let first, let second {
    print(first + second)
    // prints: AB
}
```

也可以用 `,` 追加布尔条件：

```swift
let age: Int? = 20
if let age, age >= 18 {
    print("成年：\(age)")
    // prints: 成年：20
}
```

## 9.3 `guard let`：提前退场，主干更清爽

当函数必须在参数缺失时立刻返回，`guard` 比层层嵌套的 `if` 更合适：

```swift
func greet(_ name: String?) {
    guard let name, !name.isEmpty else {
        print("名字无效")
        return
    }
    print("你好，\(name)")
}

greet(nil)
// prints: 名字无效
greet("Mia")
// prints: 你好，Mia
```

`guard` 的硬规则：`else` 块必须离开当前作用域，可以 `return`、`break`、`continue` 或 `throw`。绑定成功的值在 `guard` 之后的整个作用域都能用，这也是它比 `if let` 更适合参数校验的原因。

## 9.4 空合运算符：给缺席的值准备替补

`??` 在左边有值时取左边，否则取右边：

```swift
let input: String? = nil
print(input ?? "默认值")
// prints: 默认值

let saved: String? = "已保存"
print(saved ?? "默认值")
// prints: 已保存
```

右边可以是另一个可选值，于是能连续兜底：

```swift
let a: Int? = nil
let b: Int? = nil
let c: Int? = 3
print(a ?? b ?? c ?? 0)
// prints: 3
```

`??` 会短路：左边一旦有值，右边不会求值。

```swift
func fallback() -> Int {
    print("fallback 被调用")
    return 0
}

let value: Int? = 10
print(value ?? fallback())
// prints: 10
```

## 9.5 可选链：一路问号，一路安全

在可能为 `nil` 的属性、方法或下标后面写 `?`，就形成可选链。链中任何一环断裂，整个表达式返回 `nil`，不会崩溃：

```swift
struct Address {
    var city: String
}

struct User {
    var name: String
    var address: Address?
}

let user = User(name: "Lin", address: nil)
print(user.address?.city as Any)
// prints: nil
print(user.address?.city ?? "未填写城市")
// prints: 未填写城市
```

可选链的方法调用也能返回可选值：

```swift
let upper = user.address?.city.uppercased()
print(upper as Any)
// prints: nil
```

注意 `.city` 后面不必再写问号：可选链一旦开始，后续访问都会继承“可能失败”的性质。

## 9.6 `map` 与 `flatMap`：在盒子里做变换

可选值也有 `map`：有值时对内容变换，没值时原样保持 `nil`：

```swift
let count: Int? = 3
print(count.map { $0 * 2 } as Any)
// prints: Optional(6)

let empty: Int? = nil
print(empty.map { $0 * 2 } as Any)
// prints: nil
```

如果变换本身又返回可选值，`map` 会得到嵌套可选值，`flatMap` 则会压平：

```swift
func parseEven(_ text: String) -> Int? {
    guard let value = Int(text), value.isMultiple(of: 2) else { return nil }
    return value
}

let text: String? = "42"
print(text.map(parseEven) as Any)
// prints: Optional(Optional(42))
print(text.flatMap(parseEven) as Any)
// prints: Optional(42)
```

## 9.7 强制解包与隐式解包：能不用就别用

`!` 表示“我确定盒子里一定有值”：

```swift
let definite: Int? = 7
print(definite!)
// prints: 7
```

一旦判断错误，程序立即崩溃：

```text
Fatal error: Unexpectedly found nil while unwrapping an Optional value
```

`try!` 和 `as!` 也是同一类危险动作。它们不是禁止使用，而是应该稀有。

隐式解包可选类型写作 `Type!`，常用于“初始化时暂时为空，之后一定会有值”的场景：

```swift
class View {
    var title: String!

    func render() {
        print(title)
        print(title.count)
        let explicit: String = title
        print(explicit)
    }
}

let view = View()
view.title = "首页"
view.render()
// prints: Optional("首页")
// prints: 2
// prints: 首页
```

第一行输出会让很多人愣住：**`print(title)` 打出来的是 `Optional("首页")`，编译器还会顺带警告** `coercion of implicitly unwrappable value of type 'String?' to 'Any' does not unwrap optional`。原因在于 `print` 的参数类型是 `Any`，不属于“需要具体类型”的位置，隐式解包在这里不触发。

真正需要 `String` 的地方才会自动解包：`title.count` 能用，`let explicit: String = title` 也能用。想安心打印，就写成 `print(title!)` 或 `print(title ?? "")`。

不管怎样，它仍然是可选类型，只是编译器允许你省略 `!`。在现代 Swift 代码里，能用正常可选值和构造器解决的，就不要依赖隐式解包。

## 9.8 嵌套可选与可选模式

可选值可以嵌套，虽然日常少见：

```swift
let nested: Int?? = 5
print(nested as Any)
// prints: Optional(Optional(5))
```

`switch` 能直接匹配可选值：

```swift
let maybe: Int? = 42
switch maybe {
case .some(let value):
    print("有值：\(value)")
    // prints: 有值：42
case .none:
    print("没有值")
}
```

更常见的是可选值模式 `.some` 的简写：

```swift
if case let value? = maybe {
    print(value)
    // prints: 42
}
```

## 9.9 本章小结

| 写法 | 含义 |
| --- | --- |
| `T?` | 可能没有值的 `T` |
| `if let` | 有值才进入分支，适合局部处理 |
| `guard let` | 没值就提前离开，适合参数校验 |
| `??` | 提供默认值，且会短路 |
| `?.` | 可选链，任一环缺失就返回 `nil` |
| `map` / `flatMap` | 在可选值内部做变换 |
| `!` | 强制解包，失败即崩溃 |
| `T!` | 隐式解包可选值，仍可能崩溃 |

## 9.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 认为 `Int?` 和 `Int` 可以随意混用 | 它们是不同类型，必须先解包 |
| 用 `??` 代替所有可选绑定 | 需要处理失败分支时，`if let`/`guard let` 更清楚 |
| `guard let` 的 `else` 里不退出 | 编译器会强制你 `return`、`throw` 或跳转 |
| 在可选链里继续写很多 `?` | 开头一个 `?` 之后，后续访问自动纳入链条 |
| `map` 里又返回可选值 | 会产生嵌套可选；需要压平时用 `flatMap` |
| 到处使用 `!` | 每个 `!` 都是一张可能兑现的崩溃彩票 |
| 把 `nil` 当作 0、空字符串 | `nil` 表示没有值，不是某种默认值 |

## 9.11 下章预告

下一章进入集合：`Array`、`Dictionary` 和 `Set`。它们看似普通，却会把你第一次带到 Swift 最核心的设计思想之一——**值语义**：你复制的是一个集合，不是指向同一个集合的遥控器。
