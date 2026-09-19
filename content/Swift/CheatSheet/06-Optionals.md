+++
title = "06 可选值"
linkTitle = "06 可选值"
weight = 60
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "T? 的本质、五种解包方式、可选链、?? 与 map/flatMap 的完整用法"
isCJKLanguage = true
draft = false
+++

# 06 可选值

## 它到底是什么

`Optional` 不是什么特殊关键字，它就是一个普通的枚举：

```swift
enum Optional<Wrapped> {
    case none          // 也就是 nil
    case some(Wrapped) // 有值
}
```

于是三件事一次性成立：`Int?` 就是 `Optional<Int>`；`nil` 就是 `.none`；所有能作用在枚举上的手段（模式匹配、`switch`、`map`）都能用在可选值上。

```swift
let a: Int? = 5          // 有值
let b: Int? = nil        // 没有值
let c: Optional<Int> = .some(7)
let d = Int("42")        // 解析可能失败，所以返回 Int?
let e = Int("abc")       // nil

print(a ?? 0, c ?? 0, d ?? 0, e ?? 0)
// prints: 5 7 42 0
```

| 写法 | 含义 | 建议 |
| --- | --- | --- |
| `Int?` | 普通可选值 | 默认用它 |
| `Optional<Int>` | 完全相同的类型 | 只在泛型上下文里写 |
| `Int!` | 隐式解包可选值 | 🚫 只留给 IBOutlet 一类历史 API |

⚠️ `Int!` 不是"不会为空"，它只是"用的时候帮我自动加个 `!`"。一旦真的是 `nil`，程序立刻崩溃。新代码里基本没有理由用它。

### `.some` 前面那个点是什么？

上面 `let c: Optional<Int> = .some(7)` 里，`some` 前面只有一个孤零零的点——那是因为**类型已经被上下文说清楚了**，不用再写第二遍：

```swift
let c: Optional<Int> = .some(7)     // 左边写了 Optional<Int>，右边只留个点
let c2 = Optional<Int>.some(7)      // 完整写法，和上面完全等价
let c3: Int? = .some(7)             // Int? 就是 Optional<Int>，照样管用
```

这种写法叫**前导点**，写出来的表达式叫**隐式成员表达式**（implicit member expression）。规则一句话：**上下文已经确定了类型，右边就可以只写 `.成员名`**。

💭 它不是"文本替换"。编译器在解析阶段留下的是 `unresolved_member_expr name="some"`——一个还没定型的节点，等类型检查阶段才拿上下文类型把 `Optional<Int>.` 补上去。所以点前面那个类型名是真的省掉了，不是偷偷写好了。

那"上下文"都能从哪儿来？凡是编译器**已经知道该填什么类型**的位置都算：

| 位置 | 例子 |
| --- | --- |
| 带类型标注的声明 | `let c: Optional<Int> = .some(7)` |
| 函数实参 | `take(.some(1))`——参数类型是 `Int?` |
| 返回值 | `func f() -> Direction { .south }` |
| 数组 / 字典字面量 | `let d: [String: Direction] = ["a": .north]` |
| 比较的另一边 | `x == .some(5)` |
| `switch` 的 `case` | `case .some(let n):`——上下文来自被匹配的那个值 |

同一套规则不只认枚举的 `case`，静态属性、构造器都吃这一套：

```swift
let m: Int = .max                    // 静态属性
let i: Optional<Int> = .init(9)      // 构造器
let col: Color = .red                // 自定义类型的静态成员，比如 SwiftUI 的 Color.red
```

⚠️ 反过来，**没有上下文就写不出来**，这是它最容易踩的地方：

```swift
let x = .some(7)        // 🛑 error: reference to member 'some' cannot be resolved without a contextual type
let y: Any = .some(7)   // 🛑 error: type 'Any' has no member 'some'（Any 上没有 some 这个成员）
let t = (1, .north)     // 🛑 error: cannot infer contextual base in reference to member 'north'
let t2: (Int, Direction) = (1, .north)   // ✅ 把类型补上就成了
```

💭 最后一件事：下面三种写法是同一件事，按"谁更好读"挑一个就行。字面量能自动提升成可选值，所以第一行最短；第三行把类型写在右边，泛型代码里反而更清楚。

```swift
let a: Int? = 7
let b: Int? = .some(7)
let c = Optional<Int>(7)
```

## 五种解包方式

同一件事，Swift 给了你五种选择。选错不会报错，只会在某个深夜给你一个崩溃日志。

💭 这一节只讲"解包"。`if let` 的兄弟们——`while let`、`guard var`、`if case let x?`、`for case let x? in`——是同一套绑定语法在别处的用法，全家福见 [02 语言主干]({{< relref "02-Language-Basics.md" >}})。

{{< tabpane text=true persist=disabled >}}

{{% tab header="if let（最常用）" %}}

```swift
let input: String? = "42"

if let value = Int(input ?? "") {
    print("解析成功：\(value)")
} else {
    print("解析失败")
}
// prints: 解析成功：42
```

Swift 5.7 起可以省略赋值右边，直接写 `if let input`（变量同名时）：

```swift
let input: String? = "42"

if let input, let value = Int(input) {
    print(value)
}
// prints: 42
```

这里的 `if let input` 是 `if let input = input` 的简写：左边那个 `input` 是**新的非可选常量**，右边那个是被解包的可选值，同名也不冲突。

🔥 多个 `let` 用逗号连起来，任何一个失败都走 `else`，比嵌套三层 `if` 好读得多。

{{% /tab %}}

{{% tab header="guard let（提前退出）" %}}

```swift
func greet(_ name: String?) {
    guard let name else {
        print("没有名字")
        return
    }
    // 从这里往下 name 都是非可选，不用再解包
    print("你好，\(name)")
}

greet("Swift")
greet(nil)
// prints: 你好，Swift
//         没有名字
```

解包出来的值作用域覆盖**后续整个作用域**，这就是 `guard` 存在的理由。函数开头把几个前置条件一次清干净，函数体就再也不会被 `?` 淹没。

{{% /tab %}}

{{% tab header="?? 空合并" %}}

```swift
let userInput: String? = nil
print(userInput ?? "默认值")
// prints: 默认值

let port: Int? = nil
print(port ?? Int("8080") ?? 80)
// prints: 8080
```

`??` 返回的**不是**可选值，是兜底后的实体值。可以链式串下去，左边的 `nil` 会一路往后掉。

⚠️ 注意优先级：`??` 比 `+` **低**，所以 `a ?? 0 + 1` 是 `a ?? (0 + 1)`。

{{% /tab %}}

{{% tab header="switch / 模式匹配" %}}

```swift
let code: Int? = 404

switch code {
case .some(let v): print("有值：\(v)")
case .none:        print("没有值")
}
// prints: 有值：404

// 更短的写法：后缀 ?
switch code {
case let v?: print("有值：\(v)")
case nil:    print("没有值")
}
// prints: 有值：404
```

需要区分"值为 0"和"没有值"时，`switch` 比 `??` 更合适。

{{% /tab %}}

{{% tab header="强制解包 !" %}}

```swift
let definitelyThere: String? = "abc"
print(definitelyThere!.count)
// prints: 3

let missing: String? = nil
// print(missing!.count)   🛑 运行时崩溃：Unexpectedly found nil
```

只有一种情况应该用 `!`：**你刚刚亲手检查过**，或者编译器已经保证了它非空。其他情况一律用 `if let` / `guard let` / `??`。单元测试里用 `!` 可以接受，生产代码里它是定时炸弹。💭

{{% /tab %}}

{{< /tabpane >}}

## 可选链

在 `?` 后面接着访问属性、调方法、取下标，任何一环是 `nil`，整条链就短路返回 `nil`，不会崩溃。

```swift
let dict = ["key": "value"]

print(dict["key"]?.count ?? 0)
// prints: 5
print(dict["missing"]?.count ?? 0)
// prints: 0

let name: String? = nil
print(name?.count ?? -1)
// prints: -1
```

链式访问可以叠很多层：

```swift
struct Address { var city: String }
struct Person { var address: Address? }

let p = Person(address: Address(city: "上海"))
print(p.address?.city ?? "未知")
// prints: 上海
```

⚠️ 链式调用返回的类型会被**自动包一层可选**。方法本身返回 `Int?` 时，可选链的结果可能是 `Int??`：

```swift
let nested: Int?? = .some(.some(3))
print(nested as Any)
// prints: Optional(Optional(3))
print(nested.flatMap { $0 } as Any)   // flatMap 压平一层
// prints: Optional(3)
```

普通情况下不用操心这一点；只有出现"为什么这个值是 `Int??`"时才需要想起来。

## map 与 flatMap（可选值版本）

可选值也有 `map`，含义是"有值就变换，没值就原样传下去"：

```swift
let text: String? = "42"
let doubled: Int? = text.map { Int($0) ?? 0 }.map { $0 * 2 }
print(doubled ?? -1)
// prints: 84

let nothing: String? = nil
print(nothing.map { $0.count } as Any)
// prints: nil
```

区别只有一句话：

| 函数 | 闭包返回值 | 最终类型 |
| --- | --- | --- |
| `map` | `T` | `T?` |
| `flatMap` | `T?` | `T?`，不会套两层 |

```swift
import Foundation

let url = "https://example.com"
let host = URL(string: url).flatMap { $0.host() }
print(host ?? "无")
// prints: example.com
```

## 从"一堆可选值"里筛出有值的

数组里的 `Int?` 是最常见的形态（比如解析 CSV 后某几列解析失败）：

```swift
let parsed = [1, nil, 3]

print(parsed.map { $0 ?? 0 })
// prints: [1, 0, 3]
print(parsed.compactMap { $0 })
// prints: [1, 3]
```

`compactMap` 是"变换 + 丢掉 `nil`"的组合技，配合 `Int.init` 特别好用：

```swift
print(["1", "x", "3"].compactMap(Int.init))
// prints: [1, 3]
```

## 可选值与类型转换

`as?` 和 `try?` 也是可选值的来源，各有一个容易忽略的细节：

```swift
let any: Any = "字符串"

if let s = any as? String {
    print(s.count)
}
// prints: 3

if let n = any as? Int {
    print(n)
} else {
    print("不是 Int")
}
// prints: 不是 Int
```

⚠️ **`try?` 会把嵌套可选压平一层。** 这属于"修好了但看起来没修"的那类改动（SE-0230）：

```swift
import Foundation

let result = try? JSONSerialization.jsonObject(with: Data("{}".utf8)) as? [String: Any]
print(type(of: result))
// prints: Optional<Dictionary<String, Any>>
```

你以为会得到 `[String: Any]??`，实际上只有一个 `?`。

## 什么时候不该用可选值

可选值是"这个值可能不存在"的诚实表达，但它也会污染调用方。四条经验：

| 场景 | 建议 |
| --- | --- |
| 集合为空 | 用空集合，别用 `nil` 表示"没有元素" |
| 状态机中的非法状态 | 用 `enum` 建模，别用一堆可选值 |
| 初始化之后一定存在的属性 | 用非可选 + 初始化器，别用 `var x: Int?` |
| 只在极少数地方缺失 | 可选值是合适的，正常使用 |

💭 一个类型里出现三个以上的可选属性，通常说明这个类型被当成了"什么都能装"的容器，该拆了。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| `!` 用在没验证过的地方 | 崩溃的经典来源 |
| 可选值写进字符串插值 | 会打印 `Optional(5)`，用 `??` 或者 `if let` 先解包 |
| `Optional` 参与算术 | `a + b` 两边都不能是可选的 |
| 字典取值直接当非可选用 | `dict[key]` 永远是可选值，元素类型也是可选时是 `T??` |
| `try?` 忘记压平 | 类型比你以为的少一层 `?` |
| 把 `nil` 当"空字符串"用 | 语义不同：`""` 有值，`nil` 没有值 |
| 比较两个可选值 | `==` 可用（`Wrapped: Equatable` 时），`<` 不行 |
| 用 `!` 图快 | 写 `guard let ... else { return }` 只多一行 |
| 写 `.some(x)` 却没给上下文 | 前导点靠类型推断撑着：`let x = .some(7)` 报 `reference to member 'some' cannot be resolved without a contextual type`。补上左边类型，或改用 `Optional(7)`。详见上面「[`.some` 前面那个点是什么？](#some-前面那个点是什么)」 |
