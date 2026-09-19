+++
title = "第6章 正则表达式：字面量、Regex 与 RegexBuilder"
weight = 60
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第六章：正则表达式：字面量、Regex 与 RegexBuilder

> 在大多数语言里，正则是一串"写在字符串里的天书"，编译器对它一无所知：写错了、捕获组数错了，只有运行时才告诉你。Swift 从 5.7 起把它变成了一等语言特性——正则有类型、捕获有名字、错误能在编译期发现。这一章讲三件事：怎么写字面量、怎么取捕获结果、以及怕正则的人应该试试的 `RegexBuilder`。

## 6.1 先记住这个默认姿势：`#/.../#`

Swift 的正则有**两种**字面量写法，但默认情况下你只能用带井号的那种：

```swift
let pattern = #/\d{4}-\d{2}-\d{2}/#
print("2026-09-14".wholeMatch(of: pattern) != nil)
// prints: true
```

裸斜杠的版本更清爽，但它是一个**可选开启**的特性，默认不生效：

```swift
let raw = /cat|dog/
```

```text
error: '/' is not a prefix unary operator
```

编译器看到开头的 `/` 就以为你要写除法，于是抱怨"斜杠不是前缀运算符"。想让裸斜杠可用，得显式打开 upcoming feature：

```bash
$ swift -enable-upcoming-feature BareSlashRegexLiterals bare.swift
dog
```

本书统一用 `#/.../#`：它在任何配置下都能用，也不会和除法表达式打架。

## 6.2 字面量是有类型的

正则字面量不是一段“字符串”，它有自己的类型；而且这个类型会跟着你写没写捕获组变化。先看最简单的一种：

```swift
print(type(of: #/\d+/#))
// prints: Regex<Substring>
```

`Regex<Output>` 里的 `Output` 描述"匹配出来给你的东西长什么样"。没有捕获组时，输出就是匹配到的那段文本（`Substring`）；一旦加了捕获组，`Output` 会变成一个"整体加上各个捕获组"的元组。这也意味着：**捕获组的数量和类型是编译期就知道的**，写错取不到的东西编译不过——这是 Swift 正则最舒服的地方。

## 6.3 三种匹配语义，别混着用

同一个正则配上三个不同的方法，含义完全不同。拿一段文本一次全试一遍：

```swift
let dateText = "今天是 2026-09-14，会议在 2026-09-15。"
let pattern = #/(\d{4})-(\d{2})-(\d{2})/#

if let m = dateText.firstMatch(of: pattern) {
    print("firstMatch:", m.0, m.1, m.2, m.3)
}
// prints: firstMatch: 2026-09-14 2026 09 14

if let m = dateText.wholeMatch(of: pattern) {
    print("wholeMatch:", m.0)
} else {
    print("wholeMatch: 不匹配（整个字符串必须完全符合）")
}
// prints: wholeMatch: 不匹配（整个字符串必须完全符合）

for m in dateText.matches(of: pattern) {
    print("matches:", m.0)
}
// prints: matches: 2026-09-14
// prints: matches: 2026-09-15
```

| 方法 | 语义 | 典型用途 |
|------|------|----------|
| `firstMatch(of:)` | 只找**第一处**匹配 | 提取日志里的第一个时间戳 |
| `wholeMatch(of:)` | 整个字符串必须**恰好**匹配 | 校验用户输入格式 |
| `matches(of:)` | 找出所有匹配 | 批量提取 |

`wholeMatch` 特别值得单独记住：它是"校验"和"提取"的分界线。用它判格式，能避免"用户输入里混了脏东西但你的正则仍然匹配到一半"这类问题。

## 6.4 捕获：位置和名字

没有名字的捕获组按位置取，`m.0` 永远是整个匹配：

```swift
let order = "2026-09-14"
if let m = order.wholeMatch(of: #/(\d{4})-(\d{2})-(\d{2})/#) {
    print(m.1, m.2, m.3)
}
// prints: 2026 09 14
```

给捕获组起名字更可读，语法是 `(?<名字>...)`，取值时直接当属性用：

```swift
let log = "user=alice id=42"
let named = #/user=(?<name>\w+)\sid=(?<id>\d+)/#

if let m = log.firstMatch(of: named) {
    print(m.name, m.id)
}
// prints: alice 42
```

## 6.5 替换

提取出来之后想改写文本，用 `replacing`：

```swift
let dateText = "今天是 2026-09-14，会议在 2026-09-15。"
let pattern = #/(\d{4})-(\d{2})-(\d{2})/#

print(dateText.replacing(pattern) { m in "\(m.1)年\(m.2)月\(m.3)日" })
// prints: 今天是 2026年09月14日，会议在 2026年09月15日。
```

闭包版本比"用 `$1`、`$2` 拼替换模板"更安全：捕获组的编号写错会直接报错，而不是悄悄替换成空字符串。

## 6.6 正则也可以是运行时生成的

模式来自配置文件或用户输入时，用 `Regex(_:)`：

```swift
let dynamic = try Regex("\\d+")
print("abc 123".firstMatch(of: dynamic)?.0 ?? "none")
// prints: 123
```

两个注意点：一是它**会抛错**（模式非法就抛），所以要 `try`；二是你用普通字符串写模式时，反斜杠要写两遍（`"\\d+"`）——这正是第 2 章讲原始字符串的用武之地：

```swift
let dynamic = try Regex(#"\d+"#)
```

## 6.7 RegexBuilder：给"看到正则就头疼"的人

`RegexBuilder` 允许你把正则写成一棵结构化的表达式树。它和字面量能力对等，可读性却高一个档次：

```swift
import RegexBuilder

let entry = "id=42"
let field = Regex {
    Capture { OneOrMore(.word) } transform: { String($0) }
    "="
    Capture { OneOrMore(.digit) } transform: { Int($0)! }
}

if let m = entry.wholeMatch(of: field) {
    print(m.1, m.2, type(of: m.2))
}
// prints: id 42 Int
```

注意 `transform:`：它把捕获到的文本**当场转成你想要的类型**。上面第二个捕获直接变成 `Int`，你不用再写 `Int(...)!` 去二次转换（第 9 章会讲比 `!` 更稳的写法）。

常用的积木：

| 积木 | 含义 |
|------|------|
| `OneOrMore { ... }` | 一个或多个 |
| `ZeroOrMore { ... }` | 零个或多个 |
| `Optionally { ... }` | 出现零次或一次 |
| `Repeat(2...) { ... }` | 按次数范围重复 |
| `ChoiceOf { "cat"; "dog" }` | 多选一 |
| `Capture { ... }` | 捕获，可配 `transform:` 转类型 |
| `CharacterClass.digit` / `.word` / `.hexDigit` / `.whitespace` | 常用字符类 |
| `Anchor.startOfLine` / `.endOfLine` / `.wordBoundary` | 位置锚点 |

几个实际效果：

```swift
import RegexBuilder

let hex = Regex { "#"; Capture { OneOrMore(.hexDigit) } transform: { String($0) } }
print("颜色 #1A2B3C", "=>", "颜色 #1A2B3C".firstMatch(of: hex)?.1 ?? "none")
// prints: 颜色 #1A2B3C => 1A2B3C

let signed = Regex { Optionally { "-" }; OneOrMore(.digit) }
print("温度 -5 度".firstMatch(of: signed)?.0 ?? "none")
// prints: -5

let atStart = Regex { Anchor.startOfLine; OneOrMore(.word) }
print("abc def".firstMatch(of: atStart)?.0 ?? "none")
// prints: abc

let ab = Regex { "a"; ZeroOrMore { "b" } }
print((try? ab.wholeMatch(in: "abbb")) != nil, (try? ab.wholeMatch(in: "ba")) != nil)
// prints: true false
```

最后一行顺便暴露了一个细节：**`Regex` 自己提供的 `wholeMatch(in:)` 是抛错的**，所以要用 `try` 或 `try?`；而字符串那一侧的 `"文本".wholeMatch(of:)` 不抛错。左右两边的方向别记反。

## 6.8 什么时候不要用正则

正则很强，但它不是万能刀：

| 想做的事 | 更合适的做法 |
|----------|--------------|
| 找子串、判前后缀 | `contains`、`hasPrefix`、`hasSuffix`（第 5 章） |
| 按固定分隔符切分 | `split(separator:)` |
| 解析 JSON | `JSONDecoder`（第 38 章会用到） |
| 解析 HTML / XML | 用真正的解析器 |
| 校验邮箱"是否完全符合 RFC" | 别用正则硬碰；先想清楚你到底要拦什么 |

一句经验：**正则擅长处理"结构规整的文本"，不擅长处理"嵌套结构"**。一旦你开始往正则里加"再来一层括号"，通常说明该换工具了。

## 6.9 本章小结

| 你想做的事 | 写法 |
|------------|------|
| 写字面量 | `#/.../#`（裸斜杠 `/.../` 需要开 `BareSlashRegexLiterals`） |
| 看类型 | `type(of: #/\d+/#)` → `Regex<Substring>` |
| 找第一处 | `text.firstMatch(of: re)` |
| 整体校验 | `text.wholeMatch(of: re)` |
| 找全部 | `text.matches(of: re)` |
| 取整体 / 捕获组 | `m.0`、`m.1`、`m.2` |
| 命名捕获 | `(?<name>...)`，取 `m.name` |
| 替换 | `text.replacing(re) { m in ... }` |
| 动态模式 | `try Regex(#"\d+"#)` |
| 结构化写正则 | `import RegexBuilder` + `Regex { ... }` |

## 6.10 本章易错点速查

| 容易踩的地方 | 正确认识 |
|--------------|----------|
| `/.../ ` 应该能直接用 | 默认不行，报 `'/' is not a prefix unary operator`；要开 upcoming feature `BareSlashRegexLiterals`，或改用 `#/.../#` |
| `m.0` 是第一个捕获组 | `m.0` 是**整个匹配**，第一个捕获组是 `m.1` |
| `firstMatch` 和 `wholeMatch` 差不多 | 差很远：前者只要能找到一处，后者要求整个字符串恰好匹配。校验格式必须用后者 |
| 正则字面量没有类型 | 有，形如 `Regex<Substring>`；加了捕获组后输出类型会变成元组，捕获组写错编译期就能发现 |
| 命名捕获要这样取：`m["name"]` | 直接当属性：`m.name` |
| `Regex("\\d+")` 不用处理错误 | 它是抛错构造器，要写 `try`；模式非法会抛异常 |
| 用普通字符串写模式时反斜杠写一个就够 | 要写两个，或者直接上原始字符串 `#"\d+"#` |
| `regex.wholeMatch(in:)` 和 `text.wholeMatch(of:)` 一样不用 `try` | 方向不同：`Regex` 那一侧会抛错，要 `try` / `try?` |
| `.` 能匹配一切 | 它默认不含换行符，也不等于"任意字符类"；写之前先想清楚你要匹配的集合 |
| 用正则解析 JSON、HTML | 别。规整文本用正则，嵌套结构用解析器 |

## 6.11 下章预告

文本处理告一段落，下一章回到"算"这件事：算术、比较、逻辑、位运算、区间、三元与空合运算符，以及一个 Swift 特有的玩法——**自定义运算符和优先级组**。顺便还会讲清 `if` / `switch` 直接当表达式用的新姿势。
