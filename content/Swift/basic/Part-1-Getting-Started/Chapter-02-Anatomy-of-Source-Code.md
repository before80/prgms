+++
title = "第2章 一段 Swift 源码的解剖"
weight = 20
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二章：一段 Swift 源码的解剖

> 语法书里最枯燥的一章通常是"词法"，因为它讲的是注释、空白、下划线这种"看起来根本不重要"的东西。但 Swift 在这一层藏了几件好东西：注释能嵌套、标识符能用中文和 emoji、字符串有"原始模式"、还有一组长得像咒语的 `#file`、`#warning`。这一章把它们一次说清，之后你看到任何 Swift 源码都不会再有"这符号是干嘛的"的困惑。

## 2.1 源文件编码：UTF-8 是硬要求

你在编辑器里看到的是字符，编译器看到的是一串字节。它只认一种解码方式：**UTF-8**。这不是"建议"，是硬要求——文件里有任何一个字节不构成合法的 UTF-8 序列，编译当场停下。

一份用 GBK 保存、里面带中文的源文件，报错长这样：

```text
error: invalid UTF-8 found in source file
```

如果存成了 UTF-16，编译器还专门准备了一句更直白的：

```text
error: input files must be encoded as UTF-8 instead of UTF-16
```

（这句话只在文件带 BOM 时出现。不带 BOM 的 UTF-16 会被当成一堆夹着 `\0` 的乱码，报的是 `nul character embedded in middle of file` 之类让人摸不着头脑的提示——编码问题不总是报得像编码问题。）

关键在于：这条检查覆盖**整份文件**，注释里的一个坏字节同样会让编译失败。所以"代码明明没问题，一加中文注释就炸"，九成是编码问题，不是语法问题。

现代编辑器基本不用操心——VS Code、Xcode、JetBrains 系列新建文件默认就是 UTF-8。真正出事的是两类文件：从旧系统或旧项目里拷贝来的（可能是 GBK、Latin-1），以及在 Windows 上用本地代码页保存出来的。修法只有一句：用编辑器"另存为"UTF-8。

三个值得知道的细节：

- **文件开头的 BOM（U+FEFF）会被忽略。** 存成"UTF-8 with BOM"照样能编过，不必特意去掉。但同一个字符出现在文件中间时，它不再是空白，会把那一行拆坏，而且报的错很误导：`consecutive statements on a line must be separated by ';'`。
- **换行符 LF 与 CRLF 都接受，混着用也行。** 从 Windows 传过来的文件不必先转换。
- **脚本首行的 shebang 合法。** 第一行写 `#!/usr/bin/swift`，再加上执行权限，就能直接 `./hello.swift` 运行。

一句话总结：**看见"中文一出现就编译不过"，先查编码，再查语法。**

## 2.2 空白、分号与注释

Swift 对空白和换行基本不敏感：多敲几个空格、把一行拆成三行，都不影响语义（字符串里面除外，那里每个字符都算数）。**分号可以完全不写**，只有一种情况必须写——你想在同一行里塞两条语句：

```swift
let a = 1; let b = 2
print(a + b)
// prints: 3
```

注释有两种。行注释用 `//`，块注释用 `/* */`，而且**块注释可以嵌套**：

```swift
// 这是行注释

/*
 这是块注释。
 下面这段是"注释里的注释"，在 Swift 里完全合法：
 /* 内层块注释 */
 所以你可以放心地注释掉一整段代码——
 即使那段代码自己带着块注释，也不会提前把注释"关掉"。
*/

print("注释不参与运算")
// prints: 注释不参与运算
```

嵌套这点值得单独夸一句。很多语言的块注释一遇到内部的 `*/` 就结束了，于是"临时注释掉一大段代码"常常变成事故现场；Swift 不会。

## 2.3 标识符：名字能取成什么样

标识符就是你给变量、函数、类型起的名字。规则很少：

- 不能以数字开头（`let 1abc = 1` 会让编译器以为你想写整数）；
- 不能包含空白或运算符字符（`+`、`-`、`*` 这些）；
- 区分大小写（`count` 和 `Count` 是两个名字）；
- 几乎所有 Unicode 字符都可以用——包括中文和 emoji；但**第一个字符**不能取自 Unicode 私用区，否则报 `invalid character in source file`，组合字符（比如重音符号）只能出现在第二个字符之后。

```swift
let 变量 = 42
let 🚀 = "fast"
let `class` = "escaped"

print(变量, 🚀, `class`)
// prints: 42 fast escaped
```

第三行的反引号是"我要拿关键字当名字"的正规手续：`class` 是保留字，加上反引号 \`class\` 就变成一个普通的标识符。同样的手法适用于所有关键字。

还有一条容易忽略的规则：**如果某个成员的名字和关键字一样**（比如 `self`、`Type`、`Protocol`），在"访问成员"的上下文里，不写反引号会被当成关键字，写了才安全。

还有一条比上面所有规则都更容易让人踩坑的：**标识符按字符逐个比较，不做 Unicode 规范化。** 下面这条报错就是这么来的：

```text
error: cannot find 'café' in scope
```

声明时写的是"预组合的 `é`"（一个标量），访问时写的是"`e` 加一个组合重音"（两个标量）。两个写法在屏幕上完全一样，第 5 章会告诉你字符串比较时它们**相等**，但标识符不享受这个待遇——编译器眼里是两个名字。从别处复制标识符时尤其容易中招，复制粘贴名字比手敲更安全。

能起不代表该起。中文名、emoji 名在正式项目里会让代码评审的同事血压升高；知道它合法、偶尔在 REPL 里图个乐就够了。官方风格是：类型用大驼峰（`UserProfile`），方法和属性用小驼峰（`fetchUser`），布尔值读起来像一句断言（`isEmpty`、`isEnabled`）。

## 2.4 关键字：哪些词你不能随便用

Swift 的关键字可以分成几组，不用背，混个脸熟就行（完整总表在附录 C）：

| 分组 | 例子 |
|------|------|
| 声明用 | `class`、`struct`、`enum`、`protocol`、`extension`、`func`、`init`、`deinit`、`subscript`、`let`、`var`、`typealias`、`import`、`static`、`operator`、`precedencegroup` |
| 语句用 | `if`、`else`、`guard`、`switch`、`case`、`default`、`for`、`while`、`repeat`、`in`、`break`、`continue`、`fallthrough`、`return`、`defer`、`throw`、`do`、`catch`、`where` |
| 表达式与类型用 | `as`、`is`、`try`、`throws`、`rethrows`、`await`、`self`、`Self`、`super`、`true`、`false`、`nil`、`Any` |
| 模式用 | `_` |
| 井号开头 | `#if`、`#else`、`#elseif`、`#endif`、`#available`、`#unavailable`、`#selector`、`#keyPath`、`#sourceLocation` |

真正有意思的是**上下文关键字**：`get`、`set`、`willSet`、`didSet`、`lazy`、`final`、`open`、`override`、`required`、`weak`、`unowned`、`mutating`、`nonmutating`、`convenience`、`indirect`、`some`、`any`、`async`、`actor`、`macro`、`package`、`left`、`right`、`none`、`precedence`……这一串词只在特定语法位置有特殊含义，**离开那个位置就是普通名字**：

```swift
let get = 1
let lazy = 2

func make(where value: Int) -> Int { value }

print(get + lazy, make(where: 3))
// prints: 3 3
```

注意 `where` 在参数标签位置可以不加反引号直接用。唯一必须转义的例外是 `inout`、`var` 和 `let`——它们就算当参数名也得写成 `` `inout` `` 这样。

## 2.5 字面量：源码里"直接写出来的值"

字面量就是字面上写出来的值：`42`、`3.14`、`"你好"`、`true`。这里有个关键认知，值得单独强调：

> **字面量本身没有类型。** 它先被当作"无限精度"的值解析，然后由类型推断决定它最终是什么类型；如果上下文没有任何线索，才退回到默认类型。

| 字面量 | 没有上下文时的默认类型 |
|--------|------------------------|
| 整数 | `Int` |
| 浮点数 | `Double` |
| 字符串 | `String` |
| 正则表达式 | `Regex` |
| 布尔值 | `Bool` |

这就是为什么 `let x: Int8 = 42` 合法：`42` 可以是任何"整数类型"，标注说了要 `Int8`，它就变成 `Int8`。

### 2.5.1 整数字面量：四种进制，随便分组

```swift
print(0b1010, 0o17, 0x1F, 1_000_000)
// prints: 10 15 31 1000000
```

| 写法 | 进制 | 例子 |
|------|------|------|
| 直接写 | 十进制 | `42`、`1_000_000` |
| `0b` 前缀 | 二进制 | `0b1010` |
| `0o` 前缀 | 八进制 | `0o17` |
| `0x` 前缀 | 十六进制 | `0x1F`、`0xF_F` |

下划线只是给人看的分隔符，可以插在任意两个数字之间（`1_000_000`、`0xF_F` 都合法），编译器当它不存在。负数里的 `-` 是运算符，不属于字面量。

### 2.5.2 浮点字面量：还有十六进制版本

```swift
print(3.14, 1.25e2, 1_0.5, 0x1p4)
// prints: 3.14 125.0 10.5 16.0
```

- `3.14`：最普通的写法。
- `1.25e2`：科学计数法，等于 1.25 × 10²。
- `1_0.5`：下划线照样能用。
- `0x1p4`：十六进制浮点，等于 1 × 2⁴ = 16.0（`p` 后面是 2 的幂，不是 10 的幂）。这种写法在需要精确表示二进制小数时才用得上。

### 2.5.3 布尔与 nil

```swift
let yes = true
let no = false
let nothing: Int? = nil

print(yes, no)
// prints: true false
print(nothing == nil)
// prints: true
print(nothing as Any)
// prints: nil
```

`nil` 只能出现在**可选类型**里——上面那个 `Int?` 读作"可选类型的 Int"，问号就是"可选"的标记，第 9 章专门讲。`let x = nil` 这种没头没脑的写法编译器会拒绝，因为它不知道你要的是哪种"空"。至于 `print` 里的 `as Any`，是先把值当成"任意类型"再交给打印函数，第 8 章讲类型转换时再说清楚。

### 2.5.4 字符与字符串字面量

双引号里除了普通文字，还能放转义序列：

| 转义 | 含义 |
|------|------|
| `\0` | 空字符（NUL，终端里看不见） |
| `\\` | 一个反斜杠 |
| `\t` | 制表符 |
| `\n` | 换行 |
| `\r` | 回车 |
| `\"` | 双引号 |
| `\'` | 单引号 |
| `\u{n}` | 1 到 8 位十六进制码位，例如 `\u{1F600}` |

```swift
print("tab[\t] quote[\"] apostrophe[\'] backslash[\\] unicode[\u{1F600}]")
// prints: tab[	] quote["] apostrophe['] backslash[\] unicode[😀]
```

**多行字符串**用三个双引号包起来。结尾那三个引号的缩进决定"前面留白砍掉多少"，所以你可以把内容对齐得好看，而不影响结果：

```swift
let poem = """
    第一行
      第二行
    """
print(poem)
// prints: 第一行
// prints:  第二行
```

第二行前面保留了两个空格，算一下就知道为什么：它原本缩进 6 格，结尾的 `"""` 缩进 4 格，减完剩下 2 格。**被剪掉的是"所有行共同拥有的那部分缩进"**，多出来的相对缩进会原样保留——上面第二行比第一行多缩进 2 格，结果就多出 2 个空格。

**原始字符串**是 Swift 的省心设计：在引号外面加井号，内部的反斜杠就不再是转义符。井号越多，"生效门槛"越高：

```swift
let name = "Swift"

print(#"普通反斜杠 \ 是字面量；插值要写 \#(name)"#)
// prints: 普通反斜杠 \ 是字面量；插值要写 Swift
print(##"二级：这里 \#(name) 不插值，要写 \##(name)"##)
// prints: 二级：这里 \#(name) 不插值，要写 Swift
```

什么时候用得上？正则表达式、Windows 路径、命令行片段、要嵌进代码里的 JSON 或 HTML 片段——任何"反斜杠本来就很多"的场合。

### 2.5.5 正则表达式字面量

Swift 5.7 起，正则表达式是一等语言特性，可以像字符串一样直接写：

```swift
let pattern = #/\d{4}-\d{2}-\d{2}/#
print("2026-09-14".wholeMatch(of: pattern) != nil)
// prints: true
```

它有两种定界方式：`#/.../#` 和 `/.../`。**默认情况下你只能用前者**——裸斜杠那一版需要显式开启 upcoming feature `BareSlashRegexLiterals`，否则编译器会直接抱怨 `'/' is not a prefix unary operator`（它以为你要写除法）。本书统一用 `#/.../#`。这块内容不少，第 6 章专门讲。

## 2.6 特殊字面量：#file、#line 和它们的同伴

写日志、写断言、写测试辅助函数时，经常需要知道"当前在哪个文件、第几行"。Swift 给了六个现成的东西：

下面这段假设放在 SwiftPM 可执行目标里运行，模块名 `Loc`、文件名 `loc.swift`：

```swift
func whereAmI() {
    print("file:     \(#file)")
    print("fileID:   \(#fileID)")
    print("filePath: \(#filePath)")
    print("line:     \(#line)")
    print("column:   \(#column)")
    print("function: \(#function)")
}

whereAmI()
// prints: file:     Loc/loc.swift
// prints: fileID:   Loc/loc.swift
// prints: filePath: /Users/you/project/Sources/Loc/loc.swift
// prints: line:     5
// prints: column:   24
// prints: function: whereAmI()
```

三个"文件"的区别是新手最容易搞混的地方：

| 写法 | 给出什么 | 什么时候用 |
|------|----------|------------|
| `#file` | 模块名 + 文件名（形如 `Loc/loc.swift`） | 日志里给人看；别拿它当路径用 |
| `#fileID` | 同样是模块名 + 文件名 | 需要跨机器稳定、又能定位来源的标识 |
| `#filePath` | 完整路径 | 需要点开文件的工具链场景 |
| `#line` / `#column` | 行列号 | 定位到具体位置 |
| `#function` | 当前函数名（含签名） | 日志前缀 |

注意上表里 `#file` 和 `#fileID` 的输出是一样的，这不是笔误。早期 Swift 的 `#file` 给的是**完整路径**，后来 [SE-0274](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0274-magic-file.md) 把完整路径挪给了 `#filePath`，并让 `#file` 只说“哪个模块的哪个文件”。这个切换在 Swift 6 语言模式下默认生效；项目还停留在 Swift 5 模式时，`#file` 仍然是旧行为。所以规律是：**要文件标识用 `#fileID`，要完整路径用 `#filePath`，两个都不要指望 `#file`**。

一个版本细节值得知道：**从 Swift 5.9 起，这一组（以及 `#warning`、`#error`、`#dsohandle`）不再是保留关键字，而是标准库里的宏**。用法完全没变，但它们的身份从"语言内置"变成了"标准库提供"。

如果你在终端里直接 `swift 文件名.swift` 跑这段代码，看到的会是另一番景象：`#file` 和 `#filePath` 都变成 `/tmp/...` 这样的临时路径，`#fileID` 前面会挂一个 `main/`。这不是书里写错了，而是两个原因叠加：单文件脚本没有"模块名"这个概念，而且 `swift` 命令默认按 Swift 5 语言模式编译，`#file` 还是旧行为。把它放进 SwiftPM 目标里、用 Swift 6 模式编译，才会得到上表描述的结果。

## 2.7 #sourceLocation：正当地"骗"编译器

`#sourceLocation` 可以临时改写编译器眼中的"当前文件与行号"，之后再恢复：

```swift
#sourceLocation(file: "Fake.swift", line: 100)
print("重定位后 line = \(#line)，file = \(#fileID)")
#sourceLocation()
print("恢复后 line = \(#line)")
// prints: 重定位后 line = 100，file = Loc/Fake.swift
// prints: 恢复后 line = 4
```

两条输出的规矩是：行号被 `line:` 参数改成了 100；而第二条里的行号是**恢复语句在你文件中的真实行号**（把上面四行单独存成一个文件时，它就是第 4 行）。`#sourceLocation(file:)` 只改 `#filePath`，模块名改不了，`#fileID` 取的是它的最后一段——所以输出里的 `Loc/` 沿用上文的模块名，`Fake.swift` 实际上会“挂”在你自己的模块下面。

日常写业务代码基本用不到它，但代码生成器、模板引擎、DSL 工具离不开：生成出来的代码一旦报错，你希望报错指向**源头模板**，而不是那个谁也没写过的中间文件。

## 2.8 #warning 与 #error：会说话的注释

想留个提醒，又怕注释被人无视？让编译器替你说：

```swift
#warning("这个分支迟早要改")
print("还能继续编译")
```

```bash
$ swift warn.swift
warn.swift:1:10: warning: 这个分支迟早要改
1 | #warning("这个分支迟早要改")
  |          `- warning: 这个分支迟早要改
2 | print("还能继续编译")
3 |
还能继续编译
```

警告归警告，程序照跑。换成 `#error` 就不客气了：

```swift
#error("这一步过不去")
print("看不到这行")
```

```bash
$ swift err.swift
err.swift:1:8: error: 这一步过不去
1 | #error("这一步过不去")
  |        `- error: 这一步过不去
2 | print("看不到这行")
3 |
$ echo $?
1
```

它们的正经用途：尚未实现的平台分支（"这段代码在 iOS 上跑不了"）、必须由使用者替换的占位实现、以及配合 `#if` 的平台检查（第 25 章细讲）。

## 2.9 本章小结

| 你在源码里看到的 | 它的含义 |
|------------------|----------|
| `//`、`/* */` | 行注释、可嵌套的块注释 |
| `;` | 可选，只有同一行写多条语句时必须 |
| `let 变量`、`let 🚀` | 标识符可以用 Unicode，规则很宽 |
| `` `class` `` | 反引号把关键字变成普通名字 |
| `0b` / `0o` / `0x` / `_` | 二进制、八进制、十六进制、视觉分组 |
| `0x1p4` | 十六进制浮点，等于 1 × 2⁴ |
| `\n`、`\u{1F600}` | 转义序列 |
| `#"...\#(x)..."#` | 原始字符串，反斜杠不当转义，插值要 `\#(...)` |
| `/.../`、`#/.../#` | 正则表达式字面量 |
| `#file`、`#fileID`、`#filePath`、`#line`、`#column`、`#function` | 源码位置信息 |
| `#sourceLocation(...)` | 改写编译器眼中的文件与行号 |
| `#warning`、`#error` | 编译期提醒与编译期拦截 |

## 2.10 本章易错点速查

| 容易踩的地方 | 正确认识 |
|--------------|----------|
| "源码用什么编码都行吧？" | 只接受 UTF-8。GBK 会报 `invalid UTF-8 found in source file`，UTF-16 有专门的报错；连注释里的坏字节也会让编译失败 |
| 带 BOM 的 UTF-8 文件不能编译 | 能。文件**开头**的 BOM 会被忽略；但同一个字符出现在文件中间会把那行拆坏，报错还很误导 |
| "Swift 也要写分号吧？" | 不需要。分号只在同一行分隔多条语句时有意义，多余的分号不会报错但也没用 |
| 块注释不能嵌套 | Swift 可以嵌套。这一点在"临时注释掉一大段代码"时特别省事 |
| 标识符只能英文 | 中文、emoji 都合法，但正式项目里别用；能编译不等于该写 |
| 两个看起来一样的名字是同一个 | 标识符**不做 Unicode 规范化**：预组合的 `é` 和 `e` + 组合重音是两个名字，会报 `cannot find ... in scope` |
| 拿关键字当变量名一定报错 | 加反引号就行；而且 `get`、`lazy`、`where` 这类**上下文关键字**在很多位置根本不用转义 |
| `1_000_000` 里的下划线会影响数值 | 不会，下划线纯粹给人看 |
| `0x1p4` 是十六进制整数 | 它带 `p`，是**十六进制浮点**，等于 16.0；十六进制整数是 `0x1F` 这种 |
| `let x = nil` 应该可以 | 不行。`nil` 必须搭配具体的可选类型，否则推断不出类型 |
| 原始字符串里不能插值 | 能，但要升级转义符：`#"..."#` 里写 `\#(值)`，`##"..."##` 里写 `\##(值)` |
| 多行字符串的缩进会被原样保留 | 结尾 `"""` 的缩进决定要砍掉多少前导空白，内容因此可以对齐排版 |
| `#file`、`#line` 是编译器内置的关键字 | 从 Swift 5.9 起它们是标准库宏；用法不变，但身份变了 |
| `#warning` 会让编译失败 | 不会，它只发警告；要拦编译用 `#error` |

## 2.11 下章预告

单个文件玩够了，该开个正经项目了。下一章我们用 SwiftPM 建出第一个包：看懂 `Package.swift`、把代码拆进 target、加上依赖、顺手把该项目的测试跑起来——顺便弄清楚 `swift run`、`swift build`、`swift test` 到底谁在干活。
