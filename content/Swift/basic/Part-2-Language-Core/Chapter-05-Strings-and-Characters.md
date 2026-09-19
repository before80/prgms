+++
title = "第5章 字符串与字符：Unicode 的温柔陷阱"
weight = 50
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第五章：字符串与字符：Unicode 的温柔陷阱

> 刚上手 Swift 的人，几乎都会在同一个地方撞一下：`str[0]` 报错。报错信息还挺不客气——"不能用 `Int` 给 `String` 下标"。这不是编译器找茬，而是 Swift 在逼你面对一个很多语言都假装不存在的问题：**在 Unicode 世界里，"第 0 个字符"到底是什么？** 这一章我们把这件事讲透。

## 5.1 Character 和 String 是两个类型

一个汉字、一个表情、一个字母都可能是 `Character`；把它们串起来才是 `String`。看清这两个类型的边界，后面很多"为什么这个 API 不认"的问题会自动消失：

```swift
let c: Character = "语"
let s: String = "语"

print(c, s, type(of: c), type(of: s))
// prints: 语 语 Character String
```

`Character` 表示"恰好一个扩展字形簇"——也就是用户眼里看到的一个字符。多写一个字符就会立刻报错：

```swift
let bad: Character = "ab"
```

```text
error: cannot convert value of type 'String' to specified type 'Character'
```

平时写 `let greeting = "hello"` 得到的是 `String`，因为字符串字面量的默认类型就是 `String`。只有你明确需要"单个字符"时才标注 `Character`——遍历字符串时拿到的是 `Character`，这个后面会见到。

## 5.2 count 数的不是字节

这是本章最重要的一张表，全部实测：

| 字符串 | `count` | `utf8.count` | 说明 |
|--------|---------|--------------|------|
| `"语"` | 1 | 3 | 一个汉字占 3 个 UTF-8 字节 |
| `"é"` | 1 | 2 | 它是**一个** Unicode 标量 |
| `"🇨🇳"` | 1 | 8 | 两个区域指示符拼成的旗子，用户看到 1 个字符 |
| `"👨‍👩‍👧‍👦"` | 1 | 25 | 四个人的 ZWJ 序列，用户仍然看到 1 个字符 |

```swift
print("语".count, "语".utf8.count)
// prints: 1 3
print("👨‍👩‍👧‍👦".count, "👨‍👩‍👧‍👦".utf8.count)
// prints: 1 25
```

`count` 数的是**扩展字形簇**（用户感知的字符），`utf8.count` 数的是**字节**。两者完全不是一回事。

更反直觉的是：**拼接字符串不一定改变字符数**。官方语言指南里那个经典例子——

```swift
var word = "cafe"
print(word.count, word)
// prints: 4 cafe

word += "\u{301}"        // 追加一个组合用的重音符号
print(word.count, word, word.utf8.count)
// prints: 4 café 6
```

字符数还是 4，因为那个重音符号"贴"到了前面的 `e` 上，合成出用户眼里的一个字符。这里还有个肉眼看不见的细节：打印出来的 `é` 是"`e` + 组合重音"这个**分解形式**，而第 5.6 节里那个手写的 `é` 是**预组合形式**——屏幕上一样，字节不一样，`==` 却认为它们相等。这也解释了为什么 `word.utf8.count` 是 6 而不是 5：`cafe` 四个字节，加上重音符号的两个字节。

官方语言指南里还有一句提醒，值得原样记住：**必须遍历整个字符串才能确定其扩展字形簇的边界**。所以对特别长的字符串，`count` 不是"看一眼就知道"的操作——这也是 Slice 与索引设计背后的原因。

## 5.3 为什么 `str[0]` 不合法

几乎所有从别的语言过来的人都会先写这一行，然后被编译器拦下：

```swift
let s = "abc"
print(s[0])
```

```text
error: 'subscript(_:)' is unavailable: cannot subscript String with an Int, use a String.Index instead.
```

如果你的字符串里全是 ASCII，第 0 个字节确实是 `a`；但只要出现一个汉字或一个 emoji，第 0 个字节里的内容就不是你可能预期的东西了。Swift 因此干脆堵死了"用整数下标"这条路——它不知道你想数的是字节、码位还是用户感知的字符。

正确的做法是用 `String.Index`：

```swift
let welcome = "Hello, 世界"

print(welcome[welcome.startIndex])
// prints: H

let idx = welcome.index(welcome.startIndex, offsetBy: 7)
print(welcome[idx])
// prints: 世
```

| 写法 | 含义 |
|------|------|
| `str.startIndex` | 第一个字符的位置 |
| `str.endIndex` | **最后一个字符之后**的位置（不是最后一个字符） |
| `str.index(after: i)` | 往后挪一格 |
| `str.index(before: i)` | 往前挪一格 |
| `str.index(i, offsetBy: n)` | 挪 n 格，要一格一格走过去 |
| `str.firstIndex(of: ch)` | 找某个字符，返回可选值 |

表格里最常用的是"前后各挪一格"这对组合，因为它们是取首尾字符的标准姿势：

```swift
let word = "Swift"
print(word[word.startIndex], word[word.index(before: word.endIndex)])
// prints: S t
```

`word.endIndex` 指向末尾之后那格，所以往后退一格才是真正的最后一个字符 `t`。

两个必须知道的后果：

1. **`endIndex` 不是"最后一个字符"**，拿它取值会崩：

```swift
let s = "abc"
print(s[s.endIndex])
// 运行期崩溃：Fatal error: String index is out of bounds
// prints: （无输出，程序终止）
```

2. **`offsetBy` 是老实地一格一格走的**，所以别在循环里用 `str[str.index(startIndex, offsetBy: i)]` 写遍历——那是把线性的操作套进了循环里。要遍历就直接遍历：

```swift
for (i, ch) in "swift".enumerated() {
    print(i, ch)
}
// prints: 0 s
// prints: 1 w
// prints: 2 i
// prints: 3 f
// prints: 4 t
```

## 5.4 切片是 Substring，不是 String

这是新手第二个高频困惑点：`prefix`、`dropFirst` 这类操作**返回的不是 `String`**，而是 `Substring`。

```swift
let sentence = "The quick brown fox"

let firstWord = sentence.prefix(3)
print(firstWord, type(of: firstWord))
// prints: The Substring

print(String(firstWord), type(of: String(firstWord)))
// prints: The String
```

为什么要专门搞一个类型？因为 `Substring` 和原来的 `String` **共享底层存储**——切片不复制内容，代价很小。代价是它会让那份存储一直活着，所以只适合"临时用一下"。要长期保存（放进数组、属性、返回给调用方），就显式转换：

```swift
let stored: String = String(sentence.prefix(3))
```

```swift
let word = "Swift"
print(word.dropFirst(2), word.dropLast())
// prints: ift Swif
```

`dropFirst`、`dropLast`、`prefix` 是一家人：都返回 `Substring`，都不复制内容。

切片和原串的索引是通用的，所以可以拿 `firstIndex(of:)` 找到分隔位置后，用两段切片把字符串劈开：

```swift
let text = "one two three"
if let space = text.firstIndex(of: " ") {
    print("前半段:", text[..<space])
    print("后半段:", text[text.index(after: space)...])
}
// prints: 前半段: one
// prints: 后半段: two three
```

`text[..<space]`、`text[...space]`、`text[space...]` 这些"单边区间"就是给这种场景准备的。

## 5.5 常用操作速查

先看纯标准库的部分：

```swift
var text = "Hello"
text += ", world"
text.append("!")
print(text)
// prints: Hello, world!

var line = "hello"
line.insert("!", at: line.endIndex)
line.remove(at: line.startIndex)
print(line)
// prints: ello!

print("Swift".hasPrefix("Swi"), "Swift".hasSuffix("ift"), "Swift".contains("if"))
// prints: true true true

print(String(repeating: "ab", count: 3))
// prints: ababab

let parts = ["2026", "09", "14"]
print(parts.joined(separator: "-"))
// prints: 2026-09-14
```

上面第一组是字符串上最常用的"问一问"：`hasPrefix` 看开头、`hasSuffix` 看结尾、`contains` 问"有没有出现过"。三个都返回 `Bool`，比的是规范等价后的文本（第 5.6 节）。`String(repeating:count:)` 则是"把一小段重复成一段"的构造器，写分隔线、生成占位文本时很顺手。

拆分字符串用 `split`，它直接给你一组 `Substring`：

```swift
let csv = "a,b,,c"
print(csv.split(separator: ","))
// prints: ["a", "b", "c"]
print(csv.split(separator: ",", omittingEmptySubsequences: false))
// prints: ["a", "b", "", "c"]
```

注意第一行的默认行为：**连续的分隔符会被当成一个**，空字段直接消失。要保留空字段就显式写 `omittingEmptySubsequences: false`。这个差异在解析 CSV 时能救命。

最后几个常用的，需要 `import Foundation`：

```swift
import Foundation

let messy = "  Swift 6.3  "
print("[\(messy.trimmingCharacters(in: .whitespaces))]")
// prints: [Swift 6.3]

print("a-b-c".replacingOccurrences(of: "-", with: "+"))
// prints: a+b+c
```

本章用的是最基础的字符串写法。需要跨行文本、或者不想把反斜杠写成 `\\` 时，多行字符串 `"""` 与原始字符串 `#"..."#` 会更好用，写法与常见坑在 第 15B.3 节。

## 5.6 比较：`==` 判的是"用户眼中的相等"

同一个字符可以用不同的 Unicode 写法表达，但用户看到的、以及 `==` 判断的，都是同一个字：

```swift
print("é" == "e\u{301}")
// prints: true
```

左边是"已经合成好的 é"（一个标量），右边是"e 加一个组合重音"（两个标量）。它们字节不同、长度不同，但 Swift 认为它们**相等**——因为这符合用户对"相同文本"的理解。这种比较叫规范等价，它意味着字符串的 `==` 比字节比较要慢一点，但结果对得多。

排序是另一回事。标准库的 `<` 和 `sorted()` 按码点走，结果有时候跟人的直觉不一致：

```swift
print(["b", "a", "B", "A"].sorted())
// prints: ["A", "B", "a", "b"]
```

要按"当地人习惯"排序（比如忽略大小写、处理带重音的词、给中日文排序），用 Foundation 的本地化比较：

```swift
import Foundation

print(["b", "a", "B", "A"].sorted { $0.localizedStandardCompare($1) == .orderedAscending })
// prints: ["a", "A", "b", "B"]
```

那对大括号里的东西是**闭包**：`sorted` 要求你给一个"怎么比较两个元素"的规则，于是我们把规则写成一小段代码递过去；`$0` 和 `$1` 是"第一个参数、第二个参数"的简写。闭包要到第 14 章才正式讲，这里先认得这个形状就够——看到 `$0`，就当它是"当前正在处理的那个元素"。

顺带认一下 `localizedStandardCompare` 的返回值：它是 `ComparisonResult`，一个只有"小于、相等、大于"三档的小枚举，`.orderedAscending` 就是其中的"小于"。所以整句话读作"按本地习惯比较，结果为小于时排在前面"。

## 5.7 本章小结

| 你想做的事 | 写法 |
|------------|------|
| 一个字符 | `let c: Character = "语"` |
| 字符数 | `str.count` |
| 字节数 | `str.utf8.count` |
| 取首字符 | `str[str.startIndex]` |
| 取第 n 个字符 | `str[str.index(str.startIndex, offsetBy: n)]` |
| 找位置 | `str.firstIndex(of: " ")` |
| 取前 n 个字符 | `str.prefix(n)`（返回 `Substring`） |
| 转成真正的 String | `String(slice)` |
| 拆分 | `str.split(separator: ",")` |
| 合并 | `array.joined(separator: "-")` |
| 去掉首尾空白 | `str.trimmingCharacters(in: .whitespaces)`（Foundation） |
| 本地化排序 | `localizedStandardCompare`（Foundation） |

## 5.8 本章易错点速查

| 容易踩的地方 | 正确认识 |
|--------------|----------|
| `str[0]` 应该能用 | 不行，编译期就报错。String 的下标是 `String.Index`，不是整数 |
| `count` 返回字节数 | 返回的是扩展字形簇数量。`"语".count` 是 1，`"语".utf8.count` 才是 3 |
| `.count` 是廉价操作 | 官方文档明确提醒：确定字形簇边界必须遍历整个字符串，长字符串上别反复算 |
| `endIndex` 是最后一个字符的位置 | 它是"最后一个字符之后"，取它会崩。最后一个是 `index(before: endIndex)` |
| `prefix`、`split` 返回 `String` | 它们返回 `Substring`。要长期保存就 `String(...)` 转换 |
| `Substring` 是独立的一份字符串 | 它和原字符串共享存储，所以便宜，但也因此不能随便长期持有 |
| 拼接字符串一定会加长字符数 | 不一定。`"cafe" + 组合重音` 仍然是 4 个字符 |
| `==` 比较的是字节 | 比较的是规范等价的文本：`"é" == "e\u{301}"` 为 `true` |
| `sorted()` 能按人类习惯排序 | 它按码点排。`["b","a","B","A"].sorted()` 得到 `["A","B","a","b"]`，想要本地化顺序得用 Foundation 的比较方法 |
| `split(separator:)` 会保留空字段 | 默认不保留（连续分隔符合并）；要保留得写 `omittingEmptySubsequences: false` |
| 在循环里用 `index(_:offsetBy:)` 逐个取值 | 那是把线性操作塞进循环。遍历就用 `for ... in str` 或 `str.enumerated()` |

## 5.9 下章预告

字符串里最容易写错的第二件事，是"从一堆文本里挑出想要的部分"。下一章讲正则表达式：`/.../` 字面量、`firstMatch` 与 `wholeMatch` 的区别、类型化捕获、以及 `RegexBuilder` 那套"像搭积木一样写正则"的 DSL。
