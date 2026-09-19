+++
title = "第12章 控制流（二）：switch 与八类模式"
weight = 120
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十二章：控制流（二）：switch 与八类模式

> 很多语言的 `switch` 只是“值等于多少”的多分支写法。Swift 把它升级成了模式匹配系统：你可以检查范围、拆开元组、提取枚举关联值、匹配可选值、判断类型，甚至调用自定义匹配函数。更省心的是，每个 `case` 匹配后自动结束，不需要 `break` 防穿透。

## 12.1 基本形态：必须穷尽

`switch` 在 Swift 里最"硬"的一条规则是：**所有可能的情况都必须在代码里出现**，编译器会替你数：

```swift
let grade = "B"

switch grade {
case "A":
    print("优秀")
case "B", "C":
    print("合格")
default:
    print("需要努力")
}
// prints: 合格
```

`switch` 必须覆盖所有可能情况。对字符串这类无穷集合，通常要靠 `default` 兜底；对枚举，编译器能检查你是否列出了全部 `case`。

多个值用逗号并列，等价于“这些值都走同一分支”。

## 12.2 区间匹配

分支里可以直接写范围，不用写成 `case x where x < 60` 那种绕的写法：

```swift
let score = 86

switch score {
case ..<60:
    print("不及格")
case 60..<80:
    print("及格")
case 80..<90:
    print("良好")
default:
    print("优秀")
}
// prints: 良好
```

区间模式既可以写半开 `..<`，也可以写闭区间 `...`。如果范围重叠，只会执行最先匹配到的 `case`，顺序就变得很重要。

## 12.3 值绑定与 `where`

在 `case` 中用 `let` 或 `var` 把匹配到的值接住：

```swift
switch score {
case let value where value >= 90:
    print("高分：\(value)")
case let value:
    print("普通分：\(value)")
}
// prints: 普通分：86
```

第一个 `case` 先绑定，再用 `where` 加条件；第二个 `case` 兜住剩下的所有值，所以不需要 `default`。

## 12.4 元组模式

元组可以在 `case` 中逐项匹配：

```swift
let point = (2, 0)

switch point {
case (0, 0):
    print("原点")
case (_, 0):
    print("在 x 轴上")
case (0, _):
    print("在 y 轴上")
default:
    print("普通点")
}
// prints: 在 x 轴上
```

`_` 是通配模式，表示“这里是什么都接受，但我不关心”。元组模式里还能嵌套值绑定：

```swift
switch point {
case (let x, 0):
    print("x = \(x)")
default:
    break
}
// prints: x = 2
```

## 12.5 枚举关联值模式

枚举可以在 `case` 中一次性拆开关联值：

```swift
enum NetworkEvent {
    case connected(host: String)
    case failed(code: Int)
    case disconnected
}

let event = NetworkEvent.connected(host: "example.com")

switch event {
case .connected(let host):
    print("已连接：\(host)")
case .failed(let code):
    print("失败：\(code)")
case .disconnected:
    print("已断开")
}
// prints: 已连接：example.com
```

枚举是模式匹配最亲密的伙伴。加上 `where` 后，可以只处理某类关联值：

```swift
switch event {
case .failed(let code) where code >= 500:
    print("服务端错误")
default:
    print("其他事件")
}
// prints: 其他事件
```

## 12.6 可选值模式

可选值本质上是枚举，因此也可以用 `case .some` / `case .none`，或者更简洁的 `?`：

```swift
let name: String? = "Nova"

switch name {
case let value?:
    print("名字：\(value)")
case nil:
    print("没有名字")
}
// prints: 名字：Nova
```

`case let value?` 等价于 `case .some(let value)`。

## 12.7 类型转换模式：`is` 与 `as`

`switch` 可以顺带完成类型判断和向下转换：

```swift
let things: [Any] = [1, "two", 3.0]

for thing in things {
    switch thing {
    case is Int:
        print("整数")
    case let text as String:
        print("字符串：\(text)")
    case let value as Double:
        print("小数：\(value)")
    default:
        print("其他")
    }
}
// prints: 整数
// prints: 字符串：two
// prints: 小数：3.0
```

`case is T` 只判断类型，`case let x as T` 判断并绑定转换后的值。后者失败时不会崩溃，因为匹配本来就可能失败。

## 12.8 表达式模式：`~=` 背后的魔法

范围、字符串、枚举能出现在 `case` 中，是因为它们支持表达式模式匹配运算符 `~=`。你可以为自定义类型定义这个运算符：

```swift
struct EvenNumber {
    let value: Int
}

func ~= (pattern: EvenNumber.Type, value: Int) -> Bool {
    value.isMultiple(of: 2)
}

switch 42 {
case EvenNumber.self:
    print("偶数")
default:
    print("奇数")
}
// prints: 偶数
```

这段代码不是在教你滥用运算符，而是说明 `case` 的匹配规则可以扩展。日常代码中，`where` 通常比自定义 `~=` 更易读。

## 12.9 复合模式、`fallthrough` 与 `@unknown default`

同一个 `case` 可以捆绑多个模式：

```swift
let char: Character = "y"
switch char {
case "a", "e", "i", "o", "u", "A", "E", "I", "O", "U":
    print("元音")
default:
    print("辅音或其它")
}
// prints: 辅音或其它
```

默认情况下匹配结束就离开 `switch`。如果你确实想继续执行下一个分支，必须显式写 `fallthrough`：

```swift
switch 1 {
case 1:
    print("一")
    fallthrough
case 2:
    print("继续到二")
default:
    break
}
// prints: 一
// prints: 继续到二
```

`fallthrough` 不会重新检查下一个 `case` 的条件，它只是继续往下执行。因此它更像“主动跳进下一格”，不是“继续匹配”。

模式不只在 `switch` 里出现，也能直接写进 `if`、`guard` 和 `for`：

```swift
let values: [Int?] = [1, nil, 2]

for case let value? in values {
    print(value)
}
// prints: 1
// prints: 2

if case .some(.some(let value)) = values.first {
    print("第一个：\(value)")
}
// prints: 第一个：1
```

`for case let value?` 会自动跳过 `nil`，只把有值的元素绑定给 `value`。`guard case` 则适合在条件不满足时提前离开函数。它们和 `switch` 使用的是同一套模式语言。

`guard case` 的形状和 `guard let` 一样，只是把"取值"换成了"匹配模式"，失败时走 `else` 离开：

```swift
func describe(_ value: Int?) -> String {
    guard case let .some(x) = value else { return "空" }
    return "有 \(x)"
}
print(describe(3), describe(nil))
// prints: 有 3 空
```

它和 `if case` 的差别只在"失败之后怎么办"：`guard` 要求你在 `else` 里离开当前作用域（`return`、`break`、`continue`、`throw` 都行），好处是成功路径不用再缩进一层。

处理未来可能新增 `case` 的枚举时，可以用 `@unknown default`：

```swift
enum Direction { case north, south }

func advise(_ direction: Direction) -> String {
    switch direction {
    case .north: return "向北"
    case .south: return "向南"
    @unknown default: return "未知方向"      // 为将来新增的 case 兜底
    }
}

print(advise(.north), advise(.south))
// prints: 向北 向南
```

它和普通 `default` 的分工是这样的：`default` 的意思是"剩下的我全包了，以后有事也别叫我"；`@unknown default` 的意思是"现在这些我全处理了，但将来新增的分支请提醒我"。

这个差别只在**跨模块**时才真正发挥作用。你依赖的那个库如果把枚举加了一个用例，你用普通 `default` 写的 `switch` 会一声不吭地继续编译（新用例悄悄落进 `default`），而你写了 `@unknown default` 的 `switch` 会在重新编译时报一条警告，把你叫回来看一眼：

```text
warning: switch must be exhaustive
  | `- note: add missing case: '.east'
```

注意它**不会**因为"你还没列全"而免掉穷尽检查——`@unknown default` 不是偷懒的挡箭牌，而是"预防未来的提醒开关"。自己模块里定义的枚举本来就在你手里，写它也没错，只是通常用不上。

## 12.10 `switch` 表达式

当每个分支返回同类型值时，`switch` 也能直接产出结果：

```swift
let code = 404
let message = switch code {
case 200: "成功"
case 404: "找不到"
default: "其他错误"
}
print(message)
// prints: 找不到
```

每个分支都必须是单个表达式（或者以 `throw`、`fallthrough` 结尾），这条硬性规则和更多例子见第 15B.12 节。

## 12.11 八类模式速查

| 模式 | 示例 | 作用 |
| --- | --- | --- |
| 通配模式 | `_` | 接受任何值，不绑定 |
| 标识符模式 | `let x` | 绑定一个值 |
| 值绑定模式 | `.some(let x)` | 在复杂模式内部绑定 |
| 元组模式 | `(0, let y)` | 拆开元组 |
| 枚举用例模式 | `.failed(let code)` | 匹配枚举及关联值 |
| 可选模式 | `let x?`、`nil` | 匹配可选值 |
| 类型转换模式 | `is Int`、`as? String` | 匹配类型并可选绑定 |
| 表达式模式 | `1...10`、`"A"` | 借助 `~=` 做值匹配 |

## 12.12 本章小结

| 能力 | 关键结论 |
| --- | --- |
| 穷尽性 | 必须覆盖所有情况，枚举由编译器检查 |
| 自动结束 | 每个 `case` 默认不穿透，无需 `break` |
| `where` | 在匹配后再加条件 |
| 模式 | 通配、标识符、值绑定、元组、枚举、可选、类型、表达式 |
| `fallthrough` | 显式继续到下一个分支，不重新匹配 |
| `switch` 表达式 | 每个分支都产生值，可赋值 |

## 12.13 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 忘记 `default` | 非穷尽类型必须兜底，枚举除外 |
| 以为 `case` 会像 C 一样穿透 | Swift 默认自动结束 |
| 把 `fallthrough` 当成重新匹配 | 它直接执行下一个分支，不检查条件 |
| 顺序写反导致区间失效 | 前面的 `case` 先匹配，特殊范围要放前面 |
| 用 `as!` 做 `case` 匹配 | 类型转换模式使用 `is` 或 `as?` 风格 |
| 需要绑定却写 `_` | `_` 不产生变量，后续无法使用该值 |

## 12.14 下章预告

下一章开始讲函数。Swift 函数的参数标签、默认值、可变参数和 `inout` 都有自己的规则；函数本身还能像值一样传递。把这一章学明白，后面闭包和函数式风格的代码就不会突然变得陌生。
