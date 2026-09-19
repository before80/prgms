+++
title = "regex"
date = 2026-09-19T21:00:00+08:00
weight = 20
type = "docs"
description = "18 种语言的正则表达式对照：引擎与方言、匹配与查找、捕获组与替换、性能安全与陷阱"
isCJKLanguage = true
draft = false
+++

# 正则表达式：18 种语言对照

"正则"这个词掩盖了三件完全不同的事：**有的语言根本没有正则**（C 只借用了 POSIX 的 `<regex.h>`，Zig 的 `std` 里连这个词都不存在），**有的语言给的是另一套模式语法**（Lua 的 `string.find` 系列是 Lua pattern，没有 `|` 交替也没有环视），**剩下的语言才在真正的正则引擎之间分岔**——一边是回溯引擎（Python、Java、.NET、PHP 的 PCRE2、Ruby 的 Onigmo、JavaScript），功能全但可以被一个嵌套量词写成指数级；另一边是有限自动机的线性时间引擎（Rust 的 `regex`、Go 的 `regexp`），永远不会被 ReDoS 打穿，代价是彻底放弃反向引用与环视。本页按四个主题组织：**引擎与方言 → 匹配与查找 → 捕获组与替换 → 性能安全与陷阱**，每个主题一套 18 语言标签页。

**一页速览**

| 语言 | 引擎 / 方言 | 字面量写法 | 关键差异 |
| --- | --- | --- | --- |
| Rust | `regex` crate：有限自动机，线性时间 | `Regex::new(r"...")`, `RegexBuilder` | 不支持反向引用与环视（要它们得换 `fancy-regex`）；`\d`/`\w` 默认 Unicode |
| Swift | 自研 `Regex`（SE-0355 方言）与 `NSRegularExpression`（ICU）两套 | `/.../` 字面量, `try Regex("...")`, `Regex { }` | 字面量自 5.7 起；自研引擎在 6.4 仍不支持后向环视，ICU 那套支持 |
| Go | `regexp`：RE2，线性时间 | `regexp.MustCompile("...")` | 不支持反向引用与环视；`\d`/`\w`/`\s` 只有 ASCII 语义；1.27 无新 API |
| Python | `re`：回溯 | `re.compile(r"...")` | 支持反向引用与环视；**不支持 `\p{...}`**（那是第三方 `regex` 模块）；原子组自 3.11 起 |
| Kotlin | JVM 上包装 `java.util.regex`，其它平台各有实现 | `Regex("...")`, `"""...""".toRegex()` | `RegexOption` 共 7 个且 JS 目标只有 2 个；命名组沿用 Java 的 `(?<name>...)` |
| Java | `java.util.regex`：回溯 | `Pattern.compile("...")` | 命名组是 `(?<name>...)`；`\d`/`\w` 默认 ASCII，加 `(?U)` 才是 Unicode 语义 |
| C++ | `std::regex`：回溯，默认 ECMAScript 语法 | `std::regex("...")` | **没有命名组**；11 个语法选项、13 个匹配标志；性能差且易栈溢出 |
| C | 标准库没有正则；`<regex.h>` 是 POSIX 接口 | `regcomp(&re, "...", REG_EXTENDED)` | BRE 与 ERE 两套；ERE 没有反向引用、没有 `\d`、没有命名组、没有环视 |
| Julia | PCRE2 | `r"..."` 字面量 | 标志只有 `i`, `m`, `s`, `x`, `a`；默认开 UTF+UCP，所以 `\d` 是 Unicode 语义 |
| C# | `System.Text.RegularExpressions`：默认回溯 | `new Regex(@"...")`, `[GeneratedRegex]` | 支持变长后向环视、条件、平衡组；`NonBacktracking` 引擎则相反，不支持环视与反向引用 |
| Dart | 自研引擎（Irregexp 移植），ECMAScript 方言 | `RegExp(r"...")` | `unicode` 标志决定按码元还是码点匹配，也是 `\p{...}` 的开关 |
| R | 默认 TRE（POSIX ERE 加扩展），`perl = TRUE` 切 PCRE2 | `grepl("...", x)`, `regexpr("...", x)` | 两套语法不同：命名组、环视、`\U`/`\L` 只在 Perl 模式下有 |
| Zig | 标准库没有正则 | 没有 | 只有 `std.mem` 的 `indexOfScalar`、`tokenizeScalar`、`trim` 等；正则要第三方库或 C 互操作 |
| Lua | Lua pattern，**不是正则** | `string.match(s, "...")` | 没有 `|` 交替、没有环视，`-` 才是非贪婪；`%b`, `%f`, `%1`-`%9` 是它独有的 |
| TypeScript | 同 JavaScript（类型全部编译期擦除） | `/.../`, `new RegExp("...")` | 类型只有 `RegExp`；`lib` 低于 `ES2018` 时连命名组的类型都拿不到 |
| JavaScript | ECMAScript `RegExp`（V8 自研） | `/.../`, `new RegExp("...")` | `d` 标志 ES2022、`v` 标志 ES2024、`RegExp.escape` ES2025；`g` 会带 `lastIndex` 状态 |
| PHP | PCRE2（`preg_*` 一套） | `preg_match('/.../', $s)` | 模式必须写分隔符；13 个修饰符；按名字做替换得改用 `preg_replace_callback` |
| Ruby | Onigmo | `/.../` 字面量, `Regexp.new` | 后向环视必须定长；`Regexp.timeout` 与 `Regexp.linear_time?` 自 3.2 起可用 |

## 正则表达式

### 引擎、方言与语法支持

正则表达式的分歧从引擎就开始了。Rust `regex`、Go `regexp` 与 Google 的 RE2 同属**有限自动机**一脉（Thompson NFA + DFA 混合，匹配时间与输入长度成正比，**不会**灾难性回溯）；Python、Java、Kotlin、C#、JavaScript/TypeScript、PHP、Ruby、Julia、Swift 的原生 `Regex`、Dart、C++ `std::regex`、R 的 `perl = TRUE` 模式则是**回溯 NFA**，语法自由但能写出指数级 ReDoS。方言来源又是另一个维度：PCRE2（PHP、Julia、R 的可选引擎）、Onigmo（Ruby）、ICU（Swift 的 `NSRegularExpression`）、RE2 语法（Go）、ECMAScript（C++ `std::regex` 的默认语法，也是 JS/TS 与 Dart 的规范来源）、POSIX BRE/ERE（C），外加 Python `re`、Java `Pattern`、.NET 这些自研方言。三个"没有正则"或"不是正则"的例外也必须点名：C 只有 POSIX `<regex.h>`，Zig 标准库没有正则，Lua 的 `string.find`/`match`/`gmatch`/`gsub` 用的是 **Lua pattern**。本节按「引擎分类 → 方言来源 → 高级特性支持 → 字面量与标志全枚举 → Unicode 默认性」逐语言对照，匹配函数与替换函数留给后面的子主题。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `regex` crate 是纯自动机引擎，用 Thompson NFA 构造后按需提升为 DFA，**单趟扫描、时间线性于输入长度**，官方文档明确承诺不会灾难性回溯，代价是**语法上直接砍掉**反向引用与环视这一类需要回溯才能实现的结构。它的方言是自研的，语法近似 RE2/PCRE 的公共子集，但额外提供 PCRE 也没有的字符类集合运算，以及 `(?U)` 交换贪婪性这样的扩展。最该先知道的两件事：`\d`/`\w`/`\s` **默认就是 Unicode 语义**，要 ASCII 得显式写 `(?-u)`；需要环视或反向引用时必须换 crate（`fancy-regex` 或 `pcre2`），不是加个开关的问题。

```rust
// Cargo.toml: regex = "1"（本文实测 1.13.1）
use regex::Regex;

fn main() {
    // ① \d \w \s 默认 Unicode 语义：阿拉伯-印度数字也算 \d
    println!("{}", Regex::new(r"^\d+$").unwrap().is_match("١٢٣"));       // true
    println!("{}", Regex::new(r"(?-u)^\d+$").unwrap().is_match("١٢٣"));  // false（(?-u) 退回 ASCII）

    // ② \p{...} Unicode 属性可用
    println!("{}", Regex::new(r"^\p{Greek}+$").unwrap().is_match("αβγ")); // true
    println!("{}", Regex::new(r"^\p{Han}+$").unwrap().is_match("汉字"));   // true

    // ③ 命名组：(?P<name>...) 与 (?<name>...) 两种拼写都接受
    let g = Regex::new(r"(?P<y>\d{4})-(?<m>\d{2})").unwrap();
    let c = g.captures("2026-09").unwrap();
    println!("{} {}", &c["y"], &c["m"]);                                 // 2026 09

    // ④ 内联标志 (?i)(?m)(?s)(?x)(?U)(?-u)，也有作用域写法 (?i:...)
    println!("{}", Regex::new(r"(?i)rust").unwrap().is_match("RUST"));           // true
    println!("{}", Regex::new(r"(?x) \d+ \s+ \w+ ").unwrap().is_match("12 ab")); // true
    println!("{:?}", Regex::new(r"(?U)a+").unwrap().find("aaa").unwrap().as_str()); // "a"

    // ⑤ 字符类集合运算：交集 &&、差集 --、对称差 ~~
    println!("{}", Regex::new(r"^[\w&&\d]+$").unwrap().is_match("1"));   // true
    println!("{}", Regex::new(r"^[\w--\d]+$").unwrap().is_match("a"));   // true
    println!("{}", Regex::new(r"^[\w~~\d]+$").unwrap().is_match("a"));   // true

    // ⑥ 环视 / 反向引用 / 原子组 / 注释组：编译期直接报错
    for p in [r"foo(?=bar)", r"(?<=foo)bar", r"(a)\1", r"(?>a)", r"(?#x)a"] {
        println!("{} => {}", p, Regex::new(p).unwrap_err().to_string().lines().last().unwrap().trim());
    }
    // ⚠️ a*+ 不是占有量词：线性引擎把它读成嵌套重复 (a*)+，仍然贪婪
    println!("{:?}", Regex::new(r"a*+").unwrap().find("aaa").unwrap().as_str()); // "aaa"
}
```

Rust `regex` 支持：命名组 `(?P<name>...)` 与 `(?<name>...)`、`\p{...}` Unicode 属性、内联标志 `(?i)`、`(?m)`、`(?s)`、`(?x)`、`(?U)`、`(?-u)` 及其作用域形式、懒惰量词 `*?`、字符类交集 `&&`、差集 `--`、对称差 `~~`、Unicode 默认开启。**不支持**：反向引用、前向环视、后向环视、原子组 `(?>...)`、占有量词、条件分支、递归模式、注释组 `(?#...)`。这里有两个容易踩的坑。第一，`a*+`、`a**`、`a++` **不会报错**，因为它们被解析成合法的嵌套重复 `(a*)+` 之类，结果仍是贪婪匹配——所以别以为 Rust 悄悄支持了占有量词，真正需要"不回溯的子匹配"只能靠重写模式或换引擎。第二，`[a-z&&[^aeiou]]` 这种 PCRE 风格写法在 Rust 里**含义不同**：Rust 的 `&&` 是**交集**运算符（并集写 `||`、差集写 `--`、对称差写 `~~`），`[a-z&&[^aeiou]]` 求的是 `a-z` 与"非元音"的交集，语义上恰好和 PCRE 的写法相近，但优先级规则要按 Rust 的集合代数读。要环视或反向引用时用 `fancy-regex`（回溯但保留线性引擎作为快速路径）或 `pcre2` crate 直接绑定 PCRE2；`RegexBuilder` 的 `size_limit`/`dfa_size_limit` 是限制编译期内存膨胀的防御旋钮，不是运行时超时。统计口径：本主题固定的 12 项高级特性（反向引用、前向环视、后向环视、命名组、`\p{...}`、原子组、占有量词、条件分支、递归模式、内联标志、懒惰量词、字符类交集/减法）中，Rust 原生支持 5 项（命名组、`\p{...}`、内联标志、懒惰量词、字符类交集/减法，后者还额外多了对称差 `~~`），不支持 7 项（反向引用、前向环视、后向环视、原子组、占有量词、条件分支、递归模式）。

📘 [docs.rs · regex 语法](https://docs.rs/regex/latest/regex/#syntax)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 有两套完全独立的引擎，必须先分清。Swift 5.7 起加入的 `Regex`（`/.../` 字面量与 `RegexBuilder`）是 Swift 标准库自研的**回溯**引擎，出典是 swift-experimental-string-processing，不是 ICU；老的 `NSRegularExpression` 才是 Foundation 包着的 **ICU**。两者能力有真实差异：自研 `Regex` 支持前向环视、反向引用、原子组、占有量词、字符类交集与差集，但**到 Swift 6.4 为止还不支持后向环视**（SE-0448 已接受，实现尚未进入发布工具链），也不支持条件分支与递归；`NSRegularExpression` 反而支持后向环视，却不支持递归。选型时先问"要不要后向环视"比问"哪个更现代"更实际。

```swift
import Foundation

// ① 字面量 /.../（Swift 5.7+；Swift 6 语言模式默认开启，Swift 5 模式要 -enable-bare-slash-regex）
//    扩展定界符 #/.../# 可以少写反斜杠
let date = /(?<y>\d{4})-(?<m>\d{2})/
if let m = try? date.wholeMatch(in: "2026-09") {
    print(m.output.y, m.output.m)                              // 2026 09
}
let hash = #/\d+/#
print(try! hash.firstMatch(in: "ab12") != nil)                 // true

// ② 自研 Regex 是回溯引擎：前向环视、反向引用、原子组、占有量词都有
print(try! Regex(#"(a)\1"#).firstMatch(in: "aa") != nil)       // true
print(try! Regex(#"(?=foo)foo"#).firstMatch(in: "foo") != nil) // true
print(try! Regex(#"(?>a*)a"#).firstMatch(in: "aaa") != nil)    // false（原子组阻断回溯）
print(try! Regex(#"a*+a"#).firstMatch(in: "aaa") != nil)       // false（占有量词）

// ③ 但后向环视在 Swift 6.4 仍未落地（SE-0448 已接受，引擎尚未实现）
do { _ = try Regex(#"(?<=foo)bar"#) }
catch { print("lookbehind:", error) }                          // lookbehind is not currently supported

// ④ \p{...} 可用；\d 是 Unicode 语义
print(try! Regex(#"^\p{Greek}+$"#).firstMatch(in: "αβγ") != nil) // true
print(try! Regex(#"^\d+$"#).firstMatch(in: "٣") != nil)          // true

// ⑤ 字符类集合运算：交集 && 与差集 --（ICU 风格）
print(try! Regex(#"^[\w--\d]+$"#).wholeMatch(in: "x") != nil)            // true
print(try! Regex(#"^[\w--\d]+$"#).wholeMatch(in: "5") != nil)            // false
print(try! Regex(#"^[a-z&&[^aeiou]]+$"#).wholeMatch(in: "bcdfg") != nil) // true

// ⑥ 条件分支与递归：不支持
for p in [#"(?(1)a|b)"#, #"(?R)"#] {
    do { _ = try Regex(p); print(p, "=> OK") } catch { print(p, "=> ERR") }
}

// ⑦ 另一套引擎：NSRegularExpression 走 ICU，后向环视可用
let icu = try! NSRegularExpression(pattern: #"(?<=foo)bar"#)
let text = "foobar"
print(icu.firstMatch(in: text, range: NSRange(text.startIndex..., in: text)) != nil) // true
```

字面量有四种可用形态：`/.../`（需要 `-enable-bare-slash-regex`，Swift 6 语言模式默认开启）、`#/.../#`（扩展定界符，反斜杠不用双写）、`try Regex("...")`（运行时构造，失败抛错）、以及 `Regex { ... }` 的 `RegexBuilder` 结果构建器。内联标志沿 ICU 习惯：`(?i)` 忽略大小写、`(?m)` 多行、`(?s)` 让 `.` 匹配换行、`(?x)` 扩展模式忽略空白、`(?U)` 交换贪婪与懒惰语义，作用域写法是 `(?i:...)`。`\d`/`\w`/`\s` 以及显式字符类都按 **Unicode 语义**工作，不需要额外开关，这是它和 Go、JavaScript 最大的区别；`\p{...}` 支持的属性名走 ICU 表，所以 `\p{Greek}`、`\p{Han}`、`\p{Lu}` 都能用，但**简写形式 `\pN` 不行**，会报 `invalid escape sequence '\p'`。命名组是 `(?<name>...)`，具名反向引用写 `\k<name>`，数字反向引用写 `\1`。⚠️ 最容易吃亏的一点：把 `NSRegularExpression` 的用法直接搬进 `Regex` 会在 `(?<=...)` 上炸掉；反过来，依赖 `.output.y` 这种**类型化捕获**（`NSRegularExpression` 没有）就只能用新 `Regex`。统计口径同上一节（12 项固定清单）：自研 `Regex` 支持 9 项（反向引用、前向环视、命名组、`\p{...}`、原子组、占有量词、内联标志、懒惰量词、字符类交集/减法），不支持 3 项（后向环视、条件分支、递归模式）。

📘 [Swift Evolution · Regex 语法（SE-0355）](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0355-regex-syntax-run-time-construction.md)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `regexp` 包是 **RE2 语法的原生 Go 实现**，用自动机（Thompson NFA 加一层 DFA 缓存）保证线性时间，因此和 Rust 一样**没有反向引用、没有环视**——`regexp/syntax` 页把它标为 RE2 语法，并明确说明反向引用与环视这类 Perl 扩展不在支持范围内。它比 Rust 更保守的一点是 `\d`/`\w`/`\s` **只有 ASCII 语义**且没有关不掉的开关——想要 Unicode 语义必须显式写 `\p{Nd}`、`\p{L}`、`\p{Zs}` 这类属性。还有一个独家工具：`regexp` 同时内置 POSIX ERE 方言（`CompilePOSIX`），匹配策略从"最左最先"变成"最左最长"。

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	// ① \d \w \s 只有 ASCII 语义，\p{...} 才认 Unicode
	fmt.Println(regexp.MustCompile(`^\d+$`).MatchString("٣"))         // false
	fmt.Println(regexp.MustCompile(`^\w+$`).MatchString("汉字"))       // false
	fmt.Println(regexp.MustCompile(`^\s$`).MatchString("\u00a0"))     // false
	fmt.Println(regexp.MustCompile(`^\p{Han}+$`).MatchString("汉字"))  // true

	// ② 命名组 (?P<name>...) 与 (?<name>...) 都接受
	re := regexp.MustCompile(`(?P<y>\d{4})-(?<m>\d{2})`)
	fmt.Println(re.SubexpNames()[1:], re.FindStringSubmatch("2026-09")) // [y m] [2026-09 2026 09]

	// ③ 内联标志 (?i)(?m)(?s)(?U)
	fmt.Println(regexp.MustCompile(`(?i)go`).MatchString("GO"))       // true
	fmt.Println(regexp.MustCompile(`(?s)^a.b$`).MatchString("a\nb"))  // true
	fmt.Println(regexp.MustCompile(`(?U)a+`).FindString("aaa"))       // a

	// ④ 环视 / 反向引用 / 原子组 / 占有量词 / 嵌套重复：编译期报错
	for _, p := range []string{`(?=x)`, `(?<=x)`, `(a)\1`, `(?>a)`, `a*+`} {
		_, err := regexp.Compile(p)
		fmt.Println(p, "=>", err)
	}
	// ⚠️ && 不是交集：Go 当普通字符处理，连 ] 都变成字面量，悄悄编译通过
	fmt.Println(regexp.MustCompile(`[a-z&&[^aeiou]]`).MatchString("q]")) // true

	// ⑤ POSIX 方言：CompilePOSIX 走 ERE 且取最左最长
	fmt.Println(regexp.MustCompilePOSIX(`a|ab`).FindString("ab")) // ab
	fmt.Println(regexp.MustCompile(`a|ab`).FindString("ab"))      // a
}
```

Go 在 12 项固定清单里只支持 4 项：命名组（`(?P<name>...)` 与 `(?<name>...)` 两种拼写都认）、`\p{...}` Unicode 属性、内联标志 `(?i)`、`(?m)`、`(?s)`、`(?U)`、懒惰量词，另外还支持 POSIX 字符类 `[[:alpha:]]`、`[[:digit:]]`、`[[:space:]]` 这些 POSIX 特有写法。**不支持**：反向引用、前向环视、后向环视、原子组、占有量词、条件分支、递归模式、字符类交集/减法。⚠️ 最大的两个陷阱都在"不报错"上。其一，`[a-z&&[^aeiou]]` 能编译通过，因为 RE2 把 `&&`、`[`、`^` 当普通字符，整个模式实际是字符集 `a-z` 加字面量 `]`——想表达减法只能用 `[^...]` 取反或匹配后用代码二次过滤。其二，嵌套重复 `a*+`、`a**` 在 Go 里是**硬错误**（`invalid nested repetition operator`），和 Rust 的宽松处理正好相反，跨语言移植正则时这里是真实的踩雷点。版本方面，Go 1.27 的 `regexp` 包**没有任何新 API**，唯一相关变化是标准库 `unicode` 包从 Unicode 15 升级到 **Unicode 17**，这会让 `\p{...}` 的属性表跟着变宽。字面量写法上没有正则字面量，惯例是用反引号原始字符串 `regexp.MustCompile(\`...\`)` 避免双写反斜杠，动态模式用 `regexp.Compile` 拿 error。

📘 [pkg.go.dev · regexp 语法总览](https://pkg.go.dev/regexp/syntax)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `re` 模块是**回溯**引擎，所以反向引用、环视、原子组这类需要回溯的写法的支持面比 Go、Rust 宽得多，代价是**灾难性回溯真实存在**且没有内置超时，线上服务要自己加超时或改用第三方 `regex` 模块的 `timeout`。它属于自研方言，语法接近 Perl/PCRE 但处处不同：命名组是 `(?P<name>...)` 而不是 PCRE 的 `(?<name>...)`，`\p{...}` Unicode 属性**完全不支持**，字符类也没有交集与减法。最该先知道的是 `\d`/`\w`/`\s` 对 `str` 默认按 **Unicode 语义**匹配——这和 Go、JavaScript 恰好相反。

```python
import re

# ① \d \w \s 对 str 默认就是 Unicode 语义，re.ASCII / (?a) 才退回 ASCII
print(bool(re.match(r"^\d+$", "٣")))            # True
print(bool(re.match(r"^\w+$", "汉字")))          # True
print(bool(re.match(r"^\d+$", "٣", re.ASCII)))   # False

# ② \p{...} 不支持：那是第三方 regex 模块的能力
try:
    re.compile(r"\p{Greek}")
except re.error as e:
    print("p-brace:", e)                        # p-brace: bad escape \p at position 0

# ③ 反向引用、命名组、环视都支持；后向环视必须定长
print(bool(re.match(r"(a)\1", "aa")))                 # True
print(bool(re.match(r"(?P<w>\w+) (?P=w)", "ha ha")))  # True
print(bool(re.match(r"(?<=x)y", "xy")))               # True

# ④ 原子组 (?>...) 与占有量词 *+ 自 Python 3.11 起可用
print(re.match(r"(?>a*)a", "aaa"))   # None
print(re.match(r"a*+a", "aaa"))      # None

# ⑤ 条件分支、递归：编译期报错；字符类减集在 3.14 只给 FutureWarning，仍按字面量解析
for p in [r"(?(1)a|b)", r"(?R)", r"[\w--\d]"]:
    try:
        re.compile(p)
        print(p, "=> OK")
    except re.error as e:
        print(p, "=>", e)

# ⑥ 标志位全枚举：A/ASCII、DEBUG、I/IGNORECASE、L/LOCALE、M/MULTILINE、NOFLAG、S/DOTALL、U/UNICODE、X/VERBOSE
print(bool(re.match(r"(?i)abc", "ABC")), bool(re.match(r"(?a)\d", "٣")))  # True False
```

标志位一共 9 个：`re.A`/`re.ASCII`、`re.DEBUG`、`re.I`/`re.IGNORECASE`、`re.L`/`re.LOCALE`、`re.M`/`re.MULTILINE`、`re.NOFLAG`、`re.S`/`re.DOTALL`、`re.U`/`re.UNICODE`、`re.X`/`re.VERBOSE`。除 `re.DEBUG` 与 `re.NOFLAG` 之外的 7 个都能写成内联形式 `(?aiLmsux)`，用减号关闭写作 `(?-i)`，作用域写法是 `(?i:...)`；`re.DEBUG` 与 `re.NOFLAG` 没有内联字母。⚠️ 两个陷阱：其一，`re.L` 只对 `bytes` 模式合法，对 `str` 模式传 `re.LOCALE` 会直接抛 `ValueError`（inline 的 `(?L)` 则报 `re.error`）；对 `str` 来说 `re.U` 是默认值，写不写都一样。其二，后向环视要求**定长**，而且同一组分支必须**等长**：`(?<=ab|cd)` 合法，`(?<=a|bc)` 与 `(?<=a{2,3})` 都会报 `look-behind requires fixed-width pattern`，`(?<=a+)b` 同样报错，需要变长后向环视时只能上第三方 `regex` 模块。字符类减集 `[\w--\d]` 在 3.14 里**不会报错**，只给一条 `FutureWarning`（"Possible set difference"），实际仍按普通字符解析，不表示减法。第三方 `regex` 模块补齐了 `re` 缺的三块：`\p{...}` Unicode 属性、任意长度后向环视、`(?V1)` 新行为，还带 `timeout` 与模糊匹配——但它是独立项目，不在标准库。版本方面，Python 3.14 的 What's New 里没有 `re` 条目（上一次接口变化是 3.13 把 `re.error` 更名为 `re.PatternError`，旧名保留），所以以上结论对 3.14 成立。统计口径同上：12 项固定清单中 `re` 支持 8 项（反向引用、前向环视、定长后向环视、命名组、原子组、占有量词、内联标志、懒惰量词），不支持 4 项（`\p{...}`、条件分支、递归模式、字符类交集/减法）。

📘 [docs.python.org · re 模块](https://docs.python.org/3/library/re.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `kotlin.text.Regex` 是一个 **expect/actual 的多平台抽象**，本身不是引擎：JVM 上它直接包装 `java.util.regex.Pattern`，JS 上构造 JavaScript `RegExp`（并且固定加 `u` 标志），Native 与 Wasm 上用的是 stdlib 自带的纯 Kotlin 引擎（Apache Harmony 正则引擎的移植）。这意味着同一段正则在不同目标上**方言不同**，官方 API 文档也就只能写明"每个平台的模式语法与选项集合都有差异"。最该先知道的是：写 JVM/Android 代码时把 `Regex` 当作 Java `Pattern` 用即可，命名组、环视、原子组、占有量词全都在；但如果代码要编译到 JS，`RegexOption` 里只剩 `IGNORE_CASE` 与 `MULTILINE` 两个值可用。

```kotlin
// ① 没有正则字面量：用 Regex("...") 或 String.toRegex()
val re = Regex("""(?<y>\d{4})-(?<m>\d{2})""")   // 原始字符串可少写反斜杠
re.find("2026-09")!!.groups["y"]!!.value          // 2026
"^\\d+$".toRegex().matches("123")                 // true

// ② 选项是 RegexOption 枚举（全 7 个：IGNORE_CASE, MULTILINE, LITERAL,
//    UNIX_LINES, COMMENTS, DOT_MATCHES_ALL, CANON_EQ）；JS 目标只有前两个
Regex("abc", RegexOption.IGNORE_CASE).matches("ABC")                  // true
Regex("a.b", setOf(RegexOption.DOT_MATCHES_ALL)).matches("a\nb")      // true

// ③ \d \w \s 的语义随平台走：JVM 沿用 Java，默认 ASCII
Regex("""^\d+$""").matches("٣")        // false
Regex("""(?U)^\d+$""").matches("٣")    // true（(?U) 是 Java 的 Unicode 字符类标志）

// ④ 支持：反向引用、环视、原子组、占有量词、\p{...}、字符类交集（JVM/Native 上）
Regex("""(a)\1""").matches("aa")                     // true
Regex("""(?<=x)y""").containsMatchIn("xy")           // true
Regex("""(?>a*)a""").matches("aaa")                  // false
Regex("""a*+a""").matches("aaa")                     // false
Regex("""\p{Greek}+""").containsMatchIn("αβγ")       // true
Regex("""[a-z&&[^aeiou]]""").matches("b")            // true

// ⑤ 不支持（继承 Java Pattern）：条件分支、递归；也没有超时参数
// Regex("""(?(1)a|b)""")   // 🛑 PatternSyntaxException（JVM 上）
```

`Regex` 的三个构造函数分别是 `Regex(pattern)`、`Regex(pattern, option)`、`Regex(pattern, options: Set<RegexOption>)`，**没有 timeout 参数**，也没有对应的属性或方法；想做 ReDoS 防护只能在 `kotlinx.coroutines` 里用 `withTimeout` 把匹配包起来再取消线程，或者先把危险模式改写成无嵌套量词的形式。选项枚举一共 7 个，其中 `IGNORE_CASE`（官方 API 在 JVM/Native/Wasm 上写的是 "Case comparison is Unicode-aware"，Kotlin/JS 上只写 "Enables case-insensitive matching"）与 `MULTILINE` 是"Common"级别，`LITERAL`、`UNIX_LINES`、`COMMENTS`、`DOT_MATCHES_ALL`、`CANON_EQ` 只在 JVM、Native、Wasm-JS、Wasm-WASI 上存在。命名组语法跟随 Java，是 `(?<name>...)` 而不是 Python 的 `(?P<name>...)`；`matchEntire` 是"整串匹配"、`matches` 也是整串匹配，`find`/`containsMatchIn` 才是"任意位置命中"，这组命名和 Java 的 `matches()`/`find()` 对应关系容易记混。⚠️ 跨平台项目要特别小心：同一份 `RegexOption` 集合在 JS 目标上会因为枚举值缺失而直接编译不过，而 `(?U)`、`\p{...}`、`[a-z&&[^aeiou]]` 这些 JVM 语法在 JS 目标上会变成非法模式。统计口径沿用 12 项固定清单：JVM 目标支持 10 项（除条件分支与递归之外全部），JS 目标与 ECMAScript 一致（见 TypeScript/JavaScript 标签页）。

📘 [kotlinlang.org · kotlin.text.Regex](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/-regex/)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `java.util.regex.Pattern` 与 `Matcher` 是官方文档自己承认的**传统 NFA 回溯引擎**（原话是"performs traditional NFA-based matching with ordered alternation as occurs in Perl 5"），特性面因此非常宽：反向引用、前后向环视、原子组、占有量词、字符类交集与减法全都在，缺的只有条件分支与递归模式。代价有两个：嵌套量词会造成灾难性回溯，而 `Pattern`/`Matcher` **没有任何超时或步数上限 API**；此外 `\d`/`\w`/`\s` 默认是 **ASCII 语义**，必须显式加 `UNICODE_CHARACTER_CLASS` 或内联 `(?U)` 才会切到 Unicode。

```java
import java.util.regex.*;

// ① 命名组是 (?<name>...)，不是 Python 的 (?P<name>...)
Matcher m = Pattern.compile("(?<y>\\d{4})-(?<m>\\d{2})").matcher("2026-09");
m.matches();
m.group("y");                                                    // 2026

// ② \d \w \s 默认 ASCII；UNICODE_CHARACTER_CLASS 或 (?U) 才 Unicode
Pattern.compile("^\\d+$").matcher("٣").matches();                 // false
Pattern.compile("^\\d+$", Pattern.UNICODE_CHARACTER_CLASS)
       .matcher("٣").matches();                                   // true
Pattern.compile("(?U)^\\d+$").matcher("٣").matches();             // true

// ③ 回溯引擎的全套：反向引用、环视、原子组、占有量词、字符类集合运算
Pattern.compile("(a)\\1").matcher("aa").matches();                // true
Pattern.compile("(?<=x)y").matcher("xy").find();                  // true
Pattern.compile("(?>a*)a").matcher("aaa").matches();              // false（原子组）
Pattern.compile("a*+a").matcher("aaa").matches();                 // false（占有量词）
Pattern.compile("[a-z&&[^aeiou]]").matcher("b").matches();        // true（交集写法）

// ④ 内联标志 (?idmsuxU-idmsuxU) 与作用域写法 (?i:...)
Pattern.compile("(?i)abc").matcher("ABC").matches();              // true
Pattern.compile("(?idmsuxU-idmsuxU:x)").matcher("x").matches();   // true

// ⑤ 官方明确列为"不支持"的 Perl 构造：条件分支
Pattern.compile("(?(1)a|b)");   // 🛑 PatternSyntaxException

// ⑥ 编译标志共 9 个
int f = Pattern.CANON_EQ | Pattern.CASE_INSENSITIVE | Pattern.COMMENTS | Pattern.DOTALL
      | Pattern.LITERAL | Pattern.MULTILINE | Pattern.UNICODE_CASE
      | Pattern.UNICODE_CHARACTER_CLASS | Pattern.UNIX_LINES;
```

内联标志字母共 7 个：`i` = `CASE_INSENSITIVE`、`d` = `UNIX_LINES`、`m` = `MULTILINE`、`s` = `DOTALL`、`u` = `UNICODE_CASE`、`x` = `COMMENTS`、`U` = `UNICODE_CHARACTER_CLASS`；`LITERAL` 与 `CANON_EQ` **没有**内联字母，只能当编译标志传。注意 `u`（`UNICODE_CASE`，让大小写折叠按 Unicode 做）和 `U`（`UNICODE_CHARACTER_CLASS`，让 `\d`/`\w`/`\s` 按 Unicode 做，并顺带隐含 `UNICODE_CASE`）是两个不同的东西，大小写敏感的代码里把它们搞反是常见 bug。官方文档在"Comparison to Perl 5"一节里显式列出**不支持**的条件构造 `(?(condition)X)` 与 `(?(condition)X|Y)`，递归模式 `(?R)`/`(?0)` 在语法总表里也不存在；此外 Java 的字符类集合运算是 **ICU 风格的 `&&`**：`[a-z&&[def]]` 是交集，`[a-z&&[^bc]]` 是减法，这一点和 Rust 的 `&&`/`--`/`~~` 写法不同。ReDoS 防护方面 `Matcher` 没有超时、没有步数限制，Oracle 的官方安全编码指南专门把"正则灾难性回溯"列为一条，实践中的做法是把匹配放到可中断的线程里加超时，或者改写模式去掉嵌套量词。版本方面，JDK 25 的发布说明**没有** `java.util.regex` 条目；JDK 26 随 Unicode 17.0 的数据更新，让 `\X` 扩展字素簇按 UAX #29 的最新数据匹配。统计口径沿用 12 项固定清单：Java 支持 10 项（除条件分支与递归模式之外全部），不支持 2 项。

📘 [docs.oracle.com · java.util.regex.Pattern](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Pattern.html)

{{% /tab %}}

{{% tab header="C++" %}}

`std::basic_regex` 是 C++11 引入的标准正则库，默认语法是 **Modified ECMAScript**（`<regex>` 有自己的语法页面，和 JavaScript 的 `RegExp` 相似但少了几个构造），实现方式是**回溯**——而且标准只要求正确性、不约束复杂度，主流实现（libstdc++、libc++）在这上面出了名的慢，模式一长还可能因为递归回溯把栈打爆。它的方言是 2000 年代早期的 ECMAScript 子集：有前向环视与反向引用，**没有**命名组、没有后向环视、没有 `\p{...}`、没有内联标志、没有原子组与占有量词。这些限制共同导致一个结论：新项目要正则时，官方标准库通常不是第一选择，RE2、Boost.Regex、CTRE 才是常见替代。

```cpp
#include <iostream>
#include <regex>
#include <string>
using namespace std;

// 默认语法是 ECMAScript；换方言只要给构造函数传第二个参数
static bool ok(const string& p) { try { regex r(p); return true; } catch (const regex_error&) { return false; } }

int main() {
    // ① 支持：前向环视、反向引用、懒惰量词
    cout << regex_search("a",  regex("(?=a)a"))        << "\n";  // 1
    cout << regex_search("aa", regex("(a)\\1"))        << "\n";  // 1
    cout << regex_search("abc", regex("a.*?b"))        << "\n";  // 1

    // ② 不支持：命名组、后向环视、\p{...}、内联标志、原子组、占有量词、字符类交集
    cout << ok("(?<n>a)") << ok("(?<=a)b") << ok("\\p{L}") << ok("(?i)abc")
         << ok("(?>a*)a") << ok("a*+a") << ok("[a-z&&[^aeiou]]") << "\n";  // 0000000

    // ③ \d \w \s 是 ASCII 语义，也没有 Unicode 开关
    cout << regex_search("5", regex("\\d")) << regex_search("٣", regex("\\d"))
         << regex_search("汉", regex("\\w")) << "\n";           // 100

    // ④ 语法选项 11 个：ECMAScript、basic、extended、awk、grep、egrep、
    //    icase、nosubs、optimize、collate、multiline（multiline 自 C++17 起）
    cout << regex_search("aaa", regex("^a+$", regex::extended)) << "\n";  // 1
    cout << regex_search("aaa", regex("^a+$", regex::grep))     << "\n";  // 0（grep 是 BRE，+ 是字面量）
    cout << regex_search("ABC", regex("abc", regex::icase))     << "\n";  // 1
    cout << regex_search("a\nb", regex("^b", regex::multiline)) << "\n";  // 1
}
```

`std::regex_constants::syntax_option_type` 一共 11 个值：`ECMAScript`、`basic`、`extended`、`awk`、`grep`、`egrep` 六个语法选择，加 `icase`、`nosubs`、`optimize`、`collate` 四个行为选项（都是 C++11），再加 `multiline`（C++17）。`icase` 相当于内联的 `(?i)`，但它只能在构造时传、不能写进模式里，所以模式必须写成编译期常量才享受得到。`\d`/`\w`/`\s` 是 **ASCII 语义且没有开关**，C++ 标准库提供的 `std::regex_traits` 默认面向 `char` 的窄字符集；想要 Unicode 只能换 `std::wregex` 配合自定义 traits（仍然不认 Unicode 属性），或者干脆用 Boost.Regex/PCRE2。⚠️ 三个真实陷阱：其一，`std::regex` 的 ECMAScript 方言**不认** `(?i)`，`(?i)abc` 会直接抛 `regex_error`，很多从 PCRE 迁移过来的模式都会在这里翻车；其二，`\p{...}` 报的是 `error_escape`，而不是"不支持 Unicode 属性"这种明确提示；其三，`std::regex_match` 是整串匹配、`std::regex_search` 才是子串搜索，名字和多数语言相反，用错了会得到"永远不匹配"的假象。版本方面，`<regex>` 接口的最后一次变化是 C++17 加入 `multiline`，此后没有再动过：cppreference 的 C++23 库特性页里 **"regex" 出现 0 次**（C++26 页目前只列了新增头文件，其中也没有 regex），也就是说 C++23、C++26 都没有为它加新接口，也没有修掉性能问题；想避免它的开销，常用替代是 RE2（线性时间、语法接近 Go）、Boost.Regex（PCRE 风格、支持 `\p{...}` 与命名组）、以及把模式在编译期变成机器码的 CTRE。WG21 层面 P1433R0 用实测数据论证了 `std::regex` 的慢（1.3 GB CSV 上 libstdc++ 33.6 秒、libc++ 1655 秒，而 CTRE 分别只要 3.2 秒与 11.1 秒），P1844R0 则明确主张"保留现有 `std::regex`，另行新增一个贴合新版 ECMAScript 的语法选项"，两份提案都没有提出移除或替换现有接口。统计口径沿用 12 项固定清单：C++ 支持 3 项（反向引用、前向环视、懒惰量词），不支持 9 项。

📘 [cppreference · std::basic_regex](https://en.cppreference.com/w/cpp/regex/basic_regex)

{{% /tab %}}

{{% tab header="C" %}}

**C 没有标准正则库。** C23 也没有加入——标准里能用的只有 POSIX 的 `<regex.h>`，也就是 `regcomp`/`regexec`/`regerror`/`regfree` 这一套接口，它在 POSIX 系统（Linux、macOS、BSD）上是系统调用封装，在 Windows 上则要么没有、要么是残缺实现。这套接口的方言是 **POSIX BRE 与 POSIX ERE**，两者的元字符集**不一样**：BRE 里 `+`、`?`、`|`、`(`、`)`、`{`、`}` 全是普通字符，要写 `\(`、`\)`、`\{`、`\}` 才有分组与区间含义；ERE（加 `REG_EXTENDED`）才把 `(`、`)`、`+`、`?`、`|`、`{}` 变成元字符。最该先知道的是：POSIX 方言**没有**命名组、非贪婪量词、环视、`\d`、Unicode 属性，字符类只能用 `[[:alpha:]]` 这种 POSIX 名字。

```c
#include <stdio.h>
#include <regex.h>

/* 0 表示匹配成功，REG_NOMATCH 表示不匹配，regcomp 非 0 表示模式非法 */
static void t(const char *pat, int flags, const char *s) {
    regex_t re;
    int rc = regcomp(&re, pat, flags);
    if (rc != 0) {
        char e[128]; regerror(rc, &re, e, sizeof e);
        printf("%-16s => regcomp 失败: %s\n", pat, e);
        return;
    }
    printf("%-16s vs %-6s => %s\n", pat, s,
           regexec(&re, s, 0, NULL, 0) == 0 ? "匹配" : "不匹配");
    regfree(&re);
}

int main(void) {
    /* ① BRE（默认语法）：分组写 \( \)，反向引用 \1 可用 */
    t("^\\(a\\)\\1$", 0, "aa");
    /* ② BRE 里 + 是普通字符，^a+$ 只匹配字面量 a+ */
    t("^a+$", 0, "aaa");
    /* ③ ERE（REG_EXTENDED）：() + ? | {} 才是元字符 */
    t("^(ab)+$", REG_EXTENDED, "abab");
    /* ④ ERE 没有反向引用：\1 退化成八进制转义 */
    t("^(a)\\1$", REG_EXTENDED, "aa");
    /* ⑤ 没有 \d：ERE 里 \d 就是字面量 d */
    t("^\\d+$", REG_EXTENDED, "123");
    t("^\\d+$", REG_EXTENDED, "d");
    /* ⑥ 没有命名组 / 非贪婪 / 环视 / 内联标志 */
    t("(?<n>a)", REG_EXTENDED, "a");
    t("a*?b", REG_EXTENDED, "aab");
    t("(?=a)a", REG_EXTENDED, "a");
    t("(?i)abc", REG_EXTENDED, "ABC");
    /* ⑦ regcomp 的编译标志只有四个，另有 REG_NOTBOL / REG_NOTEOL 供 regexec 使用 */
    t("^abc$", REG_EXTENDED | REG_ICASE, "ABC");
    printf("REG_EXTENDED=%d REG_ICASE=%d REG_NEWLINE=%d REG_NOSUB=%d REG_NOTBOL=%d REG_NOTEOL=%d\n",
           REG_EXTENDED, REG_ICASE, REG_NEWLINE, REG_NOSUB, REG_NOTBOL, REG_NOTEOL);
    return 0;
}
```

完整的标志集合是 `REG_EXTENDED`（切到 ERE）、`REG_ICASE`（忽略大小写）、`REG_NEWLINE`（让 `^`/`$` 与 `.` 按行处理）、`REG_NOSUB`（只关心是否匹配、不保存子表达式位置，能省一次匹配开销），加上只对 `regexec` 有效的 `REG_NOTBOL`、`REG_NOTEOL`（告诉引擎当前位置不是行首/行尾）。POSIX 还定义了 `regex_t` 里的 `re_nsub` 与 `regmatch_t` 数组来做分组捕获，但捕获上限、嵌套深度上限都是实现定义的（glibc 有 `RE_DUP_MAX` 之类的上限，`regerror` 会把超限报出来）。⚠️ 最大的陷阱就是上面第 ⑤ 行演示的：**`\d` 不是数字类**，在 ERE 里它被解释成字面量 `d`，于是 `"^\d+$"` 会去匹配字符串 `"d"`，而且**不报错**——从 PCRE 迁过来的模式必须逐个查。反向引用也要注意：POSIX 只在 **BRE** 里定义 `\1`–`\9`，加到 `REG_EXTENDED` 后 `\1` 就不再是反向引用，实测在 macOS 上它退化成八进制转义。另外 `\{n,m\}` 的上界是 `RE_DUP_MAX`（POSIX 要求至少 255），贪婪是唯一选择，没有 `*?` 这种写法。要真正的 PCRE 能力，标准路径是引入 **PCRE2**（`pcre2_compile`/`pcre2_match`）或 RE2、Oniguruma 的 C 库，或者退一步：只用 `<string.h>` 的 `strstr`/`strspn`/`sscanf` 自己搭。统计口径：12 项固定清单里 C 支持 1 项（反向引用，且只在 BRE 语法下），不支持 11 项。

📘 [pubs.opengroup.org · regcomp / regexec](https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Regex` 直接绑定 **PCRE2**，官方手册的原话是"Julia uses version 2 of Perl-compatible regular expressions (regexes), as provided by the PCRE library"，所以它继承的是 PCRE 家族里最完整的一套方言：反向引用、前后向环视、命名组、`\p{...}`、原子组、占有量词、条件分支、递归子模式一应俱全，代价自然是**回溯**引擎，嵌套量词照样能炸。它最有意思的一点是 **Unicode 默认性**：PCRE2 通常要显式开 UTF 与 UCP 才让 `\d`/`\w`/`\s` 认 Unicode，而 Julia 默认就把两者都开了，`\d` 能匹配阿拉伯-印度数字；只有加 `a` 标志才退回 ASCII（顺带关掉 UTF 与 UCP）。

```julia
# ① r"..." 字面量，标志写在结尾引号之后；也可以用 Regex(pattern, flags)
r"^a+$"                       # 无标志
r"^a+$"i                      # i = 大小写不敏感
r"^a.b$"s                     # s = 让 . 匹配换行
r"^a+$"im                     # 可以连写多个标志
Regex(raw"^\d+$", "im")       # 构造函数写法，pattern 需要转义（raw"" 省事）

# ② Unicode 默认开启（PCRE2 以 UTF + UCP 编译）：\d \w \s 都是 Unicode 语义
occursin(r"^\d+$", "٣")              # true
occursin(Regex(raw"^\d+$", "a"), "٣") # false（a = ASCII 模式，关掉 UTF 与 UCP）

# ③ \p{...} 可用；命名组三种拼写都认，取组用 m[:name]
occursin(r"^\p{Greek}+$", "αβγ")                       # true
match(r"(?<y>\d{4})-(?<m>\d{2})", "2026-09")[:y]       # "2026"

# ④ PCRE2 全套：反向引用、环视、原子组、占有量词、条件分支、递归子模式
occursin(r"(a)\1", "aa")                        # true
occursin(r"(?<=x)y", "xy")                      # true
occursin(r"(?>a*)a", "aaa")                     # false（原子组阻断回溯）
occursin(r"a*+a", "aaa")                        # false（占有量词）
occursin(r"(a)(?(1)b|c)", "ab")                 # true（条件分支）
occursin(r"^(\((?:[^()]|(?1))*\))$", "(a(b))")  # true（(?1) 递归子模式）

# ⑤ 字符类交集/减法：PCRE2 10.45 起才有，且必须开 PCRE2_ALT_EXTENDED_CLASS
#    编译选项（没有对应的 (*VERB)）；Julia 只暴露 i m s x a，开不了，
#    所以这里的 && 是普通字符，和 Go / JavaScript 是同一个坑
occursin(r"^[a-z&&[^aeiou]]$", "&]")            # true（不是减法！）
occursin(r"^[a-z&&[^aeiou]]$", "b")             # false
```

标志一共只有 5 个：`i`（忽略大小写）、`m`（让 `^`/`$` 匹配每行的首尾而不是整串首尾）、`s`（让 `.` 匹配换行）、`x`（free-spacing：忽略 token 之间的空白，`#` 起行注释）、`a`（ASCII 模式，关掉 UTF 与 UCP，并且允许把无效 UTF-8 当 Latin-1 字节处理，常与 `s` 搭配）。两种写法是等价的：字面量后缀 `r"..."im` 与构造函数 `Regex(pattern, "im")`；需要插值时必须用构造函数，并用 `\Q`/`\E` 包住插值变量（官方文档特别提示 `Regex("\\Q$x\\E")`）。⚠️ 两个容易踩的点。第一，`m` 只影响 `^`/`$`（按行锚定），让 `.` 匹配换行的是 `s`——这两者的分工和 PCRE、JavaScript 一致，真正容易记混的是 Ruby（Ruby 的 `m` 才是 dot-all）。第二，`a` 不是"只影响 `\d`"这么简单，它会同时关掉 UTF 与 UCP，于是 `\p{...}` 也不可用、`\u` 直接按字节写，这在处理二进制数据时反而是特性。递归要用子模式调用 `(?1)`、`(?&name)`，直接写 `(?R)` 会把整个模式（含锚点）递归进去，通常不是想要的效果。统计口径沿用 12 项固定清单：Julia 支持 11 项，唯一算"不可用"的是字符类交集/减法（PCRE2 需要编译选项，而 Julia 的 `Regex` 传不进去，`&&` 会退化成普通字符）。Julia 1.13 的 NEWS 里没有 `Regex` 相关条目；它通过 `stdlib/PCRE2_jll` 固定的 PCRE2 版本是 **10.46.0**（v1.12.0 是 10.44.0），也就是说 `PCRE2_ALT_EXTENDED_CLASS` 这个选项在库里存在，只是 Julia 的 `Regex` 接口传不进去。

📘 [docs.julialang.org · Regular Expressions](https://docs.julialang.org/en/v1/manual/strings/#Regular-Expressions)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `System.Text.RegularExpressions.Regex` 默认是**回溯**引擎，官方文档专门有一篇讲回溯机制，并给了嵌套可选量词导致 O(2ⁿ) 的例子；但它也是主流语言里少见的"同一个类里内置两套引擎"的实现：`RegexOptions.NonBacktracking`（.NET 7 起）换成保证线性时间的非回溯引擎。方言是自研的，特性和 PCRE 高度重合但不完全一样：有变长后向环视、平衡组、条件分支、字符类减法 `[a-z-[aeiou]]`，**没有**占有量词、没有递归模式、没有 `&&` 交集。最该先知道的是它内联选项字母只有 `i`、`m`、`n`、`s`、`x` 五个，以及 `MatchTimeout` 默认是无限但要主动设。

```csharp
using System.Text.RegularExpressions;

// ① 命名组两种拼写：(?<name>...) 与 (?'name'...)
var re = new Regex(@"(?<y>\d{4})-(?<m>\d{2})");
re.Match("2026-09").Groups["y"].Value;                    // 2026

// ② 默认回溯；RegexOptions.NonBacktracking 换成线性时间引擎（.NET 7+）
var linear = new Regex(@"a+", RegexOptions.NonBacktracking);

// ③ 后向环视允许变长（官方快速参考就举了 (?<=.+and.+) 这样的例子）
Regex.IsMatch("Tom and Jane", @"(?<=Tom and )Jane");       // true

// ④ \p{...}、原子组、条件分支、平衡组都在
Regex.IsMatch("αβγ", @"^\p{Greek}+$");                     // true
Regex.IsMatch("aaa", @"(?>a*)a");                          // false（原子组）
Regex.IsMatch("ab", @"(a)(?(1)b|c)");                      // true（条件分支）
Regex.IsMatch("m", @"^[a-z-[djp]]$");                      // true（字符类减法）

// ⑤ 不支持占有量词（会当成非法的嵌套量词抛 ArgumentException）
// new Regex(@"a*+a");                                     // 🛑 不支持

// ⑥ 内联选项字母只有 i m n s x（n = ExplicitCapture）
Regex.IsMatch("ABC", @"(?i)abc");                          // true
Regex.IsMatch("a b", @"(?x)a b");                          // true

// ⑦ 超时：默认 Regex.InfiniteMatchTimeout，必须显式设置才有效
var bounded = new Regex(@"a+", RegexOptions.None, TimeSpan.FromSeconds(1));

// ⑧ RegexOptions 在 .NET 10 共 11 个
var opts = RegexOptions.IgnoreCase | RegexOptions.Multiline | RegexOptions.ExplicitCapture
         | RegexOptions.Compiled | RegexOptions.Singleline | RegexOptions.IgnorePatternWhitespace
         | RegexOptions.RightToLeft | RegexOptions.ECMAScript | RegexOptions.CultureInvariant
         | RegexOptions.NonBacktracking;
```

`RegexOptions` 完整枚举 11 个：`None`、`IgnoreCase`、`Multiline`、`ExplicitCapture`、`Compiled`、`Singleline`、`IgnorePatternWhitespace`、`RightToLeft`、`ECMAScript`、`CultureInvariant`、`NonBacktracking`（.NET 7 起）；官方选项文章里还有一个 `AnyNewLine`，但标注的是".NET 11 及以后"，所以按 .NET 10 基线它不在集合里。内联选项字母与枚举的对应是 `i` = IgnoreCase、`m` = Multiline、`n` = ExplicitCapture、`s` = Singleline、`x` = IgnorePatternWhitespace，关闭用 `-`（例如 `(?i-s:...)`）；`RightToLeft`、`Compiled`、`NonBacktracking`、`ECMAScript`、`CultureInvariant` 这些**没有**内联字母，只能作为构造参数传。和 PCRE 家族最实质的差异有四处：**字符类减法写作 `[a-z-[djp]]` 而不是 `[a-z&&[^djp]]`**，且只能做减法、没有交集；**占有量词完全不存在**（`a*+a` 会被当成嵌套量词报错，要"不回溯"只能用原子组 `(?>...)` 或 .NET 独有的 `RegexOptions.NonBacktracking`）；**没有递归子模式**；**有平衡组** `(?<a-b>...)`，这是 .NET 用来配对括号、XML 标签的独门工具，PCRE 里没有对应物。`[GeneratedRegex]` 源生成器自 .NET 7 起把模式在编译期变成代码，能省掉运行时的解析开销；要注意它既不支持 `NonBacktracking`（会退回成缓存 `Regex`），也处理不了 `IgnoreCase` 的反向引用。最后是一个版本敏感的真实坑：`new Regex(@"a(b.*?c)?d")` 匹配 `"abccd"` 在 .NET 9 返回成功、在早期的 .NET 10 返回失败，原因是"把循环原子化"的优化没有考虑循环体内部还要回溯，修复已并入 10.0.4 服务版本，官方兼容性索引里**没有**为它建条目——所以这类行为差异只能靠回归测试发现。统计口径沿用 12 项固定清单：.NET 10 支持 10 项（反向引用、前向环视、后向环视、命名组、`\p{...}`、原子组、条件分支、内联标志、懒惰量词、字符类减法），不支持 2 项（占有量词、递归模式），交集算子 `&&` 也不存在。

📘 [MS Learn · 正则表达式语言快速参考](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `dart:core` `RegExp` 走的是 **ECMAScript 方言**：官方文档写得非常直接——"Dart regexps implement the ECMAScript RegExp specification"，而 VM 端引擎是从 **V8 的 Irregexp 移植**过来的（Irregexp 的字节码编译器与解释器当年是整包从 V8 移植进 Dart VM 的；V8 那个实验性的非回溯线性引擎并没有跟着进来，VM 的正则相关启动开关只有 `trace_irregexp`），编译到 Web 时则直接用宿主浏览器的正则实现。所以它的能力面和 JavaScript 几乎一模一样：有反向引用、前后向环视、命名组、`\p{...}`，没有原子组、占有量词、条件分支与递归；因为是回溯引擎，ReDoS 同样存在且**没有超时或步数上限**。最该先知道的差异只有一个标志：`unicode` 决定按 **UTF-16 码元**还是按**码点**匹配，而且是拿到 `\p{...}` 的唯一途径。

```dart
// ① 构造：RegExp(source, {multiLine, caseSensitive, unicode, dotAll})
//    惯例是传 raw string，避免 Dart 自己先吃掉一层反斜杠
final re = RegExp(r'(\w+)');
re.firstMatch('Parse my string')![0];                 // Parse

// ② unicode 标志：默认按 UTF-16 码元，开了才按码点（代理对算一个字符）
RegExp(r'^..$').hasMatch('😀');                        // true（代理对 = 2 个码元）
RegExp(r'^.$').hasMatch('😀');                         // false
RegExp(r'^.$', unicode: true).hasMatch('😀');          // true
// \p{...} 只在 unicode: true 下可用
RegExp(r'^\p{L}$', unicode: true).hasMatch('汉');      // true
RegExp(r'^\p{L}$', unicode: false).hasMatch('汉');     // false
// ⚠️ 但 \d \w \s 即使在 unicode: true 下仍是 ASCII 语义（ECMAScript 规定）
RegExp(r'^\d+$', unicode: true).hasMatch('٣');         // false

// ③ 支持：反向引用、前后向环视、命名组、懒惰量词
RegExp(r'(a)\1').hasMatch('aa');                       // true
RegExp(r'(?<=foo)bar').hasMatch('foobar');             // true
RegExp(r'(?<y>\d{4})').firstMatch('2026')!.namedGroup('y');  // 2026
RegExp(r'a+?b').firstMatch('aaab')![0];                // aaab

// ④ Dart 3.12 起支持 modifier spans 与重复命名组（ECMAScript 2025 语法）
RegExp(r'(?i:abc)').hasMatch('ABC');                   // true
RegExp(r'(?<x>a)|(?<x>b)').hasMatch('b');              // true

// ⑤ 不支持：原子组、占有量词、条件分支、递归、字符类交集
//    官方文档原话："Neither Dart nor ECMAScript have general 'atomic grouping'"
// RegExp(r'(?>a)');    // 🛑 FormatException
// RegExp(r'a*+');      // 🛑 FormatException

// ⑥ RegExp.escape 自 Dart 2.0.0 起；先把字面量转义再嵌进模式
final escaped = RegExp.escape('a.b*c');
RegExp('^$escaped\$').hasMatch('a.b*c');                // true
```

四个命名参数就是全部开关：`multiLine`（默认 `false`）、`caseSensitive`（默认 `true`，注意它是"正向"命名，和其他语言的 `i` 标志相反）、`unicode`（默认 `false`）、`dotAll`（默认 `false`）；只读属性 `isMultiLine`、`isCaseSensitive`、`isUnicode`、`isDotAll`、`pattern` 可以反查当前状态。`unicode: true` 不只是"多认几个字符"，它会同时收紧模式语法（多余的身份转义会报错，例如 `\\-` 这种只在非 Unicode 模式下合法的写法），并把 `\p{...}`、`\u{...}` 打开。⚠️ 最反直觉的一点是 `\d`/`\w` 在 Dart 里**永远**是 ASCII，开了 `unicode` 也一样——这是 ECMAScript 规范的行为，和 Python、Julia 的"Unicode 默认"正好相反；想要 Unicode 数字只能写 `\p{Nd}`（且必须 `unicode: true`）。另外 `unicode: true` 只映射到 ECMAScript 的 `u` 标志，Dart 的公开 API **没有暴露** `v`（unicodeSets）标志，所以 `v` 才有的字符类交集 `&&` 与减法 `--` 在 Dart 里拿不到。版本方面，Dart 3.13 的 `dart:core` **没有**任何 `RegExp` 改动（3.13.0 只加了 `List.unmodifiableOf`、`Map.unmodifiableOf` 与整数的位计数 getter）；最近一次 RegExp 能力变化是 **3.12.0** 的"modifier spans 与重复命名捕获组"。统计口径沿用 12 项固定清单：Dart 支持 7 项（反向引用、前向环视、后向环视、命名组、`\p{...}`、内联标志（仅 3.12+ 的 `(?i:...)` 形式）、懒惰量词），不支持 5 项（原子组、占有量词、条件分支、递归模式、字符类交集/减法）。

📘 [api.dart.dev · RegExp](https://api.dart.dev/dart-core/RegExp-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的 base 正则**有两套引擎，靠参数按次切换**：默认是 **TRE**（POSIX 1003.2 extended 的一个实现，加了一批扩展），传 `perl = TRUE` 才切到 **PCRE2**（R 4.0.0 起优先链接 PCRE2，只有构建时找不到才退回 PCRE1，用 `extSoftVersion()` 可以查实际版本）。第三个选项 `fixed = TRUE` 干脆不用正则，把模式当字面量。最该先知道的是这条分界线：**默认引擎已经支持 `\d`、`\w`、`\s`、`\b`、懒惰量词和 `\1`–`\9` 反向引用**（都是 R 的扩展，POSIX 本身不要求），但**环视、`\p{...}`、命名捕获、内联标志、`(*UCP)` 只在 `perl = TRUE` 下存在**。

```r
# ① 默认引擎是 TRE（POSIX ERE + 扩展）；perl = TRUE 才切到 PCRE2
grep("[0-9]+", c("a1", "bb"))                  # [1] 1        ERE 语法
grep("\\d+",   c("a1", "bb"))                  # [1] 1        \d 是 TRE 的扩展
grepl("(?<=a)b", c("ab", "cb"))                # 🛑 TRE 不支持环视，报 invalid regular expression
grepl("(?<=a)b", c("ab", "cb"), perl = TRUE)   # [1]  TRUE FALSE

# ② perl = TRUE 才有的：环视、\p{...}、命名捕获、内联标志
grepl("^\\p{Greek}+$", "αβγ", perl = TRUE)     # [1] TRUE
grepl("(?i)^abc$", "ABC", perl = TRUE)         # [1] TRUE

# ③ perl = TRUE 默认仍然不做 Unicode 属性匹配：\d \w \s 还是 ASCII
grepl("^\\d+$", "٣", perl = TRUE)              # [1] FALSE
grepl("^(*UCP)\\d+$", "٣", perl = TRUE)        # [1] TRUE（模式开头加 (*UCP) 才切到 Unicode）

# ④ 默认引擎自带懒惰量词与 \1-\9 反向引用（R 对 POSIX 的扩展）
sub("a+?", "X", "aaa")                         # [1] "Xaa"
sub("a+",  "X", "aaa")                         # [1] "X"
grep("^(a)\\1$", "aa")                         # [1] 1

# ⑤ fixed = TRUE 退化成字面量匹配；useBytes = TRUE 退化成逐字节
grep("a.b", c("axb", "a.b"), fixed = TRUE)     # [1] 2
grep("a.b", c("axb", "a.b"))                   # [1] 1 2
```

参数并不是全局的，而是一套按函数分布的矩阵：`grep`/`grepv` 接受 `ignore.case`、`perl`、`value`、`fixed`、`useBytes`、`invert`；`grepl` 少了 `value` 与 `invert`；`sub`/`gsub` 多了 `replacement`；`regexpr`、`gregexpr`、`regexec`、`gregexec` 接受 `ignore.case`、`perl`、`fixed`、`useBytes`；`strsplit` 只有 `fixed`、`perl`、`useBytes`；`regmatches` 只有 `invert`；`grepRaw` 有 `ignore.case`、`fixed`、`all`、`invert` 但**没有** `perl`；`agrep`/`agrepl` 走的是模糊匹配（`max.distance`、`costs`），也没有 `perl`。⚠️ 三个真实的坑。第一，**没有 `extended` 这个参数**——"extended" 是默认引擎的名字而不是开关，从别的语言猜出来的 `extended = TRUE` 会直接报"unused argument"。第二，`perl = TRUE` 下的 `\d`/`\w`/`\s` **默认仍是 ASCII**，官方文档的原话是"In UTF-8 mode the named character classes only match ASCII characters"，要 Unicode 语义必须在模式最前面写 `(*UCP)`；这一点和 PHP 的 `/u`（它顺带开了 UCP）刚好相反。第三，R 的 `\` 在字符串字面量里会被 R 的 parser 先解释一次，所以模式里的反斜杠一律要写两遍，`"\\d"` 才等于正则里的 `\d`。另一个容易忽略的细节：R 的 TRE 默认引擎**没有**原子组、占有量词、条件分支、递归（`?regex` 在 Perl 段的末尾把这些标为 "Atomic grouping, possessive qualifiers and conditional and recursive patterns are not covered here"，默认 ERE 段自然更不提供）；而 `perl = TRUE` 下这些都回来了，但**字符类交集/减法**需要 PCRE2 10.45 起的 `PCRE2_ALT_EXTENDED_CLASS` 编译选项，R 的 `perl` 只是一个逻辑值、传不进这个选项，所以按不可用计。统计口径沿用 12 项固定清单：默认 TRE 引擎支持 2 项（反向引用 `\1`–`\9`、懒惰量词），`perl = TRUE` 的 PCRE2 支持 11 项，差别就在字符类交集/减法。

📘 [stat.ethz.ch · Regular Expressions as used in R](https://stat.ethz.ch/R-manual/R-devel/library/base/html/regex.html)

{{% /tab %}}

{{% tab header="Zig" %}}

**Zig 标准库没有正则引擎。** `lib/std/std.zig` 的导入列表里没有 `regex`，`lib/std` 目录下也不存在 `regex.zig`——0.15 里能用的只有字符串原语：`std.mem` 的子串查找与切分、`std.ascii` 的 ASCII 字符判定、`std.unicode` 的 UTF-8/UTF-16 编解码。从头翻到尾都是 `std.mem`、`std.ascii`、`std.unicode` 这类原语，没有任何模式匹配模块——正则被明确留给生态。所以 Zig 里做模式匹配只有三条路：用 `std.mem` 手写状态机、通过 C 互操作调用 PCRE2 或 POSIX `<regex.h>`、或者引第三方纯 Zig 引擎。

| 需求 | Zig 0.15 标准库里的对应 API | 说明 |
| --- | --- | --- |
| 找一个子串 | `std.mem.indexOf`、`std.mem.indexOfScalar`、`std.mem.indexOfAny`、`std.mem.indexOfNone` | 全部是精确匹配，没有量词与通配 |
| 判断前后缀 | `std.mem.startsWith`、`std.mem.endsWith`、`std.mem.eql` | 字面量比较 |
| 计数 | `std.mem.count` | 计子串出现次数，不懂模式 |
| 按分隔符切分 | `std.mem.splitSequence`、`std.mem.splitScalar`、`std.mem.splitAny`、`std.mem.splitBackwardsSequence`、`std.mem.splitBackwardsScalar`、`std.mem.splitBackwardsAny` | 保留空片段 |
| 分词（丢弃空片段） | `std.mem.tokenizeSequence`、`std.mem.tokenizeScalar`、`std.mem.tokenizeAny` | ⚠️ 裸的 `std.mem.split` / `std.mem.tokenize` 自 0.14 起已废弃，写出来会触发 `@compileError` |
| ASCII 字符类 | `std.ascii.isAlphabetic`、`std.ascii.isAlphanumeric`、`std.ascii.isDigit`、`std.ascii.isHex`、`std.ascii.isControl`、`std.ascii.isPrint`、`std.ascii.isWhitespace`、`std.ascii.isLower`、`std.ascii.isUpper`、`std.ascii.isAscii` | 只认 ASCII，`std.ascii.isAlphabetic('汉')` 是 `false` |
| 大小写 | `std.ascii.toLower`、`std.ascii.toUpper`、`std.ascii.lowerString`、`std.ascii.upperString`、`std.ascii.allocLowerString`、`std.ascii.allocUpperString`、`std.ascii.eqlIgnoreCase` | 同样是 ASCII 范围 |
| 忽略大小写查找 | `std.ascii.indexOfIgnoreCase`、`std.ascii.startsWithIgnoreCase`、`std.ascii.endsWithIgnoreCase` | 没有正则，只能逐字比较 |
| UTF-8 处理 | `std.unicode.utf8Decode`、`std.unicode.utf8Encode`、`std.unicode.utf8ByteSequenceLength`、`std.unicode.utf8CountCodepoints`、`std.unicode.utf8ValidateSlice`、`std.unicode.Utf8Iterator` | 编解码与校验，不含任何模式能力 |

真正要正则时的两条路要分清楚。**C 互操作**是官方支持的路径：`const c = @cImport({ @cInclude("pcre2.h"); });` 之后直接调 `pcre2_compile`/`pcre2_match`，或者用 POSIX 的 `<regex.h>`（就等于把 C 的 BRE/ERE 方言、以及它的全部限制一起搬进来）；社区有 `pcre2-zig` 这样的封装示例。**第三方纯 Zig 引擎**目前最知名的是 `zig-regex`（自动机实现，README 声明支持 Zig 0.15.1，并自述仍是 work-in-progress、暂无 UTF-8 支持）。⚠️ 三个坑值得先记住：其一，`std.mem` 的查找都是"精确匹配 + 可指定起始位置"，想做 `a.*b` 这种模式必须自己写循环；其二，`std.ascii` 的一切判定都是**字节级 ASCII**，处理中文文本时 `isAlphabetic`、`toUpper` 都不会给出 Unicode 结果，必须自己走 `std.unicode`；其三，0.15 把 `std.mem.split`、`std.mem.tokenize` 这类不带后缀的名字删掉了，从旧代码抄片段会直接编译不过，要改成 `splitScalar`/`splitSequence`/`tokenizeAny` 这类显式版本。统计口径沿用 12 项固定清单：Zig 标准库支持 0 项——它连正则引擎都没有。

📘 [ziglang.org · Zig 0.15.1 标准库文档索引](https://ziglang.org/documentation/0.15.1/std/)

{{% /tab %}}

{{% tab header="Lua" %}}

**Lua 的 `string.find`/`string.match`/`string.gmatch`/`string.gsub` 用的是 Lua pattern，不是正则表达式。** 它是一套更小、更"字节化"的模式语言：转义用 `%` 而不是 `\`，量词只有四个，没有交替与环视。最反直觉的一条是量词的含义：`*`、`+`、`?` 取最长，而 **`-` 才是取最短**（也就是其他语言里的懒惰量词），所以 `a-` 永远先尝试匹配空串。它也确实有"反向引用"，但形态是本模式内的 `%1`–`%9`；`%b`（配对匹配）与 `%f`（frontier）则是其他语言根本没有的独有构造。

```lua
-- ① 字符类用 % 前缀：%d %a %w %s 是 Lua 写法，不是 \d \w \s
print(("a1b2"):match("%a%d"))                    -- a1
print(("  42"):match("^%s*(%d+)$"))              -- 42（有捕获时 match 返回捕获值）

-- ② * + ? 取最长，- 取最短（Lua 的非贪婪写法）
print(("aaa"):match("a*"))                       -- aaa
print(("aaa"):match("a-"))                       -- （空串）

-- ③ %n 是本模式内的"匹配第 n 个捕获到的子串"，gsub 替换串里用 %n 与 %0
print(("ha ha"):match("(%a+) %1"))               -- ha
print(("2026-09"):gsub("(%d+)-(%d+)", "%2/%1"))  -- 09/2026	1

-- ④ %b（配对匹配）与 %f（frontier 边界）是 Lua 独有
print(("(a(b)c)"):match("%b()"))                 -- (a(b)c)
print(("THE (quick) fox"):match("%f[%a]%a+"))    -- THE

-- ⑤ 没有 | 交替：竖线是普通字符，模式只能匹配字面量
print(("cat"):match("cat|dog"))                  -- nil
print(("cat|dog"):match("cat|dog"))              -- cat|dog

-- ⑥ 按字节工作、字符类按当前 locale，不认 Unicode
print(("汉"):match("%a"))                        -- nil
print(("汉"):match("."))                         -- 一个字节（UTF-8 三个字节里的第一个）
print(#("汉"))                                   -- 3
```

完整清单可以按四层记：**魔术字符**共 12 个，`^`、`$`、`(`、`)`、`%`、`.`、`[`、`]`、`*`、`+`、`-`、`?`；**字符类**共 10 个，`%a`（字母）、`%c`（控制符）、`%d`（数字）、`%g`（可打印且非空格）、`%l`（小写字母）、`%p`（标点）、`%s`（空白）、`%u`（大写字母）、`%w`（字母数字）、`%x`（十六进制位），每个单字母类的大写形式是它的补集（`%S` 是非空白）；**集合**是 `[set]` 与 `[^set]`，内部可以写范围与上面的 `%` 类；**pattern item** 共 8 类——单个字符类、字符类加 `*`（零或多次、最长）、加 `+`（一或多次、最长）、加 `-`（零或多次、最短）、加 `?`（零或一次、优先一次）、`%n`（n 为 1–9，匹配第 n 个捕获）、`%b xy`（从 x 到配对的 y）、`%f[set]`（frontier：下一字符属于 set 且前一字符不属于时匹配空串）。⚠️ 四个必须记住的差异：其一**没有 `|`**，想做"或"只能调用两次或改用 `%b`/多次匹配；其二**没有环视、没有命名组、没有原子组/占有量词/条件分支/递归/内联标志**；其三**没有 `\d`**，写 `\d` 会去匹配字面量 `d`（而且不报错），要用 `%d`；其四**没有 `%z`**（Lua 5.2 起已废弃，5.5 手册的字符类表里已经没有它），要匹配零字节得把 `string.char(0)` 显式拼进模式。数字上的限制来自实现而不是手册：`LUA_MAXCAPTURES` 是 **32**（超出会报 "too many captures"），模式匹配的调用深度上限 `MAXCCALLS` 是 **200**。版本上，Lua 5.5 的 §8 "Incompatibilities" 里**没有任何 pattern 相关条目**，那里列的是 `global` 变成保留字（可用编译选项 `LUA_COMPAT_GLOBAL` 关掉）、`for` 循环控制变量变成只读这类语言层面的改动。真需要正则时，官方生态里的两条路是 **LPeg**（Roberto Ierusalimschy 自己的 PEG 库，语义比正则更强但需要另学一套）与 **lrexlib**（绑定 PCRE2、POSIX、Oniguruma、TRE 等），或者照 C API 写一个 PCRE2 模块。统计口径沿用 12 项固定清单：Lua pattern 支持 2 项（反向引用 `%1`–`%9`、懒惰量词 `-`），不支持 10 项。

📘 [lua.org · Lua 5.5 手册 §6.5.1 Patterns](https://www.lua.org/manual/5.5/manual.html#6.5.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript **没有自己的正则运行时**：`RegExp` 就是 JavaScript 的 `RegExp`，类型声明来自 `lib.es*.d.ts`，编译产物里正则字面量原样保留、不做降级。它只在一个方面比其他语言多做了一步——**自 TypeScript 5.5 起会对正则字面量做语法检查**，不仅是括号不配对这类语法问题，还包括"反向引用指向了不存在的捕获组"这类语义问题，这在主流语言里相当少见。因此这一页的内容基本等同于 JavaScript：方言是 **ECMAScript**，引擎是运行时的（V8 的 Irregexp、SpiderMonkey、JavaScriptCore），属于**回溯**引擎，ReDoS 可能且没有超时 API。最该先知道的是 TS 特有的那条边界：TS **从不把正则语法降级输出**，能不能跑最终由运行时决定；而 5.5 起的检查只把**一部分**特性与 `target` 对照（命名组要求 `ES2018` 或更高），ES2025 的重复命名组与修饰符组目前**不受 `target` 限制**（TypeScript#63682），旧 `target` 下照样通过。

```typescript
// ① 字面量就是 JS 的；TypeScript 5.5 起会对正则做语法检查
const re: RegExp = /(?<y>\d{4})-(?<m>\d{2})/u;
const m = re.exec("2026-09")!;
m.groups!.y;                                   // "2026"

// TS 5.5+ 能抓到的两类错（运行时才报的错前移到编译期）：
// const bad = /@robot(\s+(please|immediately)))?/;  // 🛑 Unexpected ')'
// const br  = /(a)\2/u;                             // 🛑 反向引用指向不存在的组

// ② 标志位与 JavaScript 完全一致：d g i m s u v y，u 与 v 互斥
"a1".match(/(?<x>\d)/d)!.indices!.groups!.x;         // [1, 2]（d = ES2022）
/^[\p{Lowercase}&&\p{Script=Greek}]+$/v.test("αβ");  // true（v = ES2024）
RegExp.escape("a.b*c");                              // ES2025 标准方法
// new RegExp("a", "uv");                            // 🛑 SyntaxError: u 与 v 不能同时用

// ③ ES2025 的修饰符组：只支持 i m s，且必须带作用域
new RegExp("(?i:abc)").test("ABC");                  // true
new RegExp("(?-i:abc)").test("ABC");                 // false
// new RegExp("(?i)abc");                            // 🛑 SyntaxError（无作用域的 (?i) 非法）

// ④ \d \w 永远是 ASCII，\s 不是；\p{...} 需要 u 或 v
/^\d+$/u.test("٣");                                   // false
/^\w+$/u.test("汉字");                                // false
/^\s$/.test("\u00a0");                                // true（NBSP 属于 ECMAScript 的 WhiteSpace）
/^\p{Script=Han}+$/u.test("汉字");                    // true

// ⑤ TS 不降级正则；target 只被部分检查使用（命名组要 ES2018+），
//    ES2025 的重复命名组与修饰符组不看 target（TypeScript#63682）
```

标志位共有 8 个，且每个都有明确的规范版本：`g`（全局）、`i`（忽略大小写）、`m`（多行）来自最早的 ES3 时代并被 ES5.1 规范固定；`u`（Unicode 模式）与 `y`（sticky）是 **ES2015** 加入的；`s`（dotAll）是 **ES2018**；`d`（hasIndices，给 `match` 结果加 `indices`）是 **ES2022**；`v`（unicodeSets，带来字符类交集 `&&`、减法 `--` 与字符串属性）是 **ES2024**。`u` 与 `v` **互斥**，同时写会抛 `SyntaxError`，这一点在 TS 里也是运行时报错而不是类型错误。⚠️ 四个容易踩的点。第一，**无作用域的内联标志是非法语法**：`(?i)abc` 在 JS/TS 里是 `SyntaxError`，ES2025 只允许带作用域的 `(?i:...)`、`(?ims-ims:...)` 这一种形式（只支持 `i`、`m`、`s` 三个字母），从 Python/PCRE 迁移模式时必须改写。第二，`\d` 与 `\w` 在**任何模式下**都是 ASCII（`unicode` 模式也不例外），只有 `\s` 不是——`\s` 匹配 ECMAScript 的 WhiteSpace 与 LineTerminator 集合，包含 U+00A0、U+2028、U+FEFF 等，所以"JS 的 `\s` 也只认 ASCII"是个常见误传。第三，`RegExp.escape` 是 **ES2025** 的标准静态方法，但它生成的字符串只保证可作为 `new RegExp()` 的**字面量模式**安全使用，不能拿去拼字符类内部。第四，`target` 只被部分正则检查使用——TS 5.5 起命名组等特性会要求 `target` 够新（`ES2018` 以上），但 ES2025 的重复命名组与修饰符组不受 `target` 限制（TypeScript#63682），旧 `target` 下也照样通过；TS 从不把正则降级输出，真正决定能不能跑的是运行时版本。版本方面，TypeScript 7.0 的 Beta 与 RC 公告里**没有**任何正则相关条目，Go 重写带来的是编译速度而不是正则语义变化；Node 侧本次实际运行环境是 **Node 24.20.0**（`RegExp.escape` 由 Node 24 / V8 13.6 引入，`v` 标志由 Node 20 / V8 11.3 引入），文档基线 Node 26.0.0（V8 14.6）两者都具备。统计口径沿用 12 项固定清单：TypeScript 所依赖的 ECMAScript 支持 8 项（反向引用、前向环视、后向环视、命名组、`\p{...}`、懒惰量词、字符类交集/减法，以及内联标志——但只有 ES2025 带作用域的修饰符组 `(?i:...)`，且字母仅限 `i`/`m`/`s`），不支持 4 项（原子组、占有量词、条件分支、递归模式）。

📘 [MDN · 正则表达式参考](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的正则由宿主引擎提供，规范侧是 **ECMAScript**：V8 用 **Irregexp**（一个回溯引擎，另有一个实验性的非回溯后端但默认关闭），SpiderMonkey 与 JavaScriptCore 各有自己的实现，但都必须满足同一份规范，所以方言是统一的。它和 TypeScript 的差别只在于没有编译期检查，正则写错只能等到运行时抛 `SyntaxError`。最该先知道的是 ES2025 补齐了两块长期缺失的能力：**带作用域的修饰符组 `(?i:...)`** 与 **`RegExp.escape`**，但**原子组、占有量词、条件分支、递归**依然没有，ReDoS 也依然没有超时 API。

```javascript
// ① 字面量 /.../ 与 RegExp 构造；命名组、前后向环视、反向引用都有
const re = /(?<y>\d{4})-(?<m>\d{2})/;
re.exec("2026-09").groups.y;                     // "2026"
/(?<=a)b/.test("ab");                             // true（后向环视，长度可变）
/(a)\1/.test("aa");                               // true

// ② 标志位 d g i m s u v y 与各自加入的规范版本
"a1".match(/(?<x>\d)/d).indices.groups.x;        // [1, 2]（d = ES2022）
"xy".match(/y/y);                                 // null（y = 粘性，只从 lastIndex 处开始匹配）
/^[\p{Lowercase}&&\p{Script=Greek}]+$/v.test("αβ"); // true（v = ES2024）
RegExp.escape("a.b*c");                           // "\x61\.b\*c"（ES2025；Node 24 实测）

// ③ ES2025 修饰符组：只有带作用域的形式才合法
new RegExp("(?i:abc)").test("ABC");               // true
new RegExp("(?-i:abc)").test("ABC");              // false
// new RegExp("(?i)abc");                         // 🛑 SyntaxError: Invalid group

// ④ 不支持：原子组、占有量词、条件分支、递归
// new RegExp("(?>a)");        // 🛑 Invalid group
// new RegExp("a*+");          // 🛑 Nothing to repeat
// new RegExp("(?(1)a|b)");    // 🛑 Invalid group

// ⑤ \d \w 永远 ASCII，\s 不是；\p{...} 要 u 或 v
/^\d+$/.test("٣");                                // false
/^\w+$/u.test("汉字");                            // false
/^\s$/.test("\u00a0");                            // true（NBSP 属于 WhiteSpace）
/^\d+$/u.test("٣");                               // false（加了 u 也一样）
```

八个标志的完整语义值得逐个对上：`g` 全局（配合 `lastIndex` 迭代，`String.prototype.match` 在 `g` 下返回全部匹配且**不带捕获组**）、`i` 忽略大小写、`m` 让 `^`/`$` 匹配每行、`s` 让 `.` 匹配行终止符、`u` 开启 Unicode 模式（码点语义、`\p{...}`、严格的转义规则）、`v` 取代 `u` 并额外提供字符类的交集 `&&`、减法 `--` 与字符串属性、`y` 从 `lastIndex` 位置起必须立即匹配（"粘性"）、`d` 在结果里附加 `indices`。`v` 模式下 `&&` 与 `--` **不能在同一层混用**，`[a-z&&[^aeiou]]` 这种混写会报错，要写成 `[[a-z]--[aeiou]]` 或加嵌套括号。⚠️ 三个真实陷阱。第一，`g` 标志会让 `RegExp` 对象**带状态**（`lastIndex`），同一个正则对象在两次 `test`/`exec` 之间会互相影响，这是 JS 独有的坑，函数内反复用同一个带 `g` 的正则逐行判断会得到交替的真假结果。第二，`[a-z&&[^aeiou]]` 在**不带 `v`** 时能编译通过，因为 `&`、`[`、`^` 都退化成普通字符，整个模式变成"一个字符类 + 一个字面量 `]`"，语义和意图完全不同。第三，`RegExp.escape` 对首字符是字母或数字时用 `\x61` 这样的十六进制转义（这是 ES2025 规范为了兼容 `v` 模式字符类而定的规则），所以它的输出不能拿来做字符串相等比较。版本方面，`RegExp.escape` 由 **Node 24**（V8 13.6）引入，`v` 标志由 **Node 20**（V8 11.3）引入；本次代码在 **Node 24.20.0** 上实际运行通过，Node 26.0.0（V8 14.6）同样包含两者。ReDoS 防护方面，V8 只提供了实验性、非标准的命令行开关（`--enable-experimental-regexp_engine-on-excessive-backtracks` 在回溯超限时回退到非回溯引擎、`--regexp-backtracks-before-fallback N` 设定阈值，默认 50000；另有 `--enable-experimental-regexp-engine` 打开非标准的 `l` 标志），没有语言级超时 API。统计口径沿用 12 项固定清单：JavaScript 支持 8 项（反向引用、前向环视、后向环视、命名组、`\p{...}`、懒惰量词、字符类交集/减法，以及内联标志——但只有 ES2025 带作用域的修饰符组 `(?i:...)`，且字母仅限 `i`/`m`/`s`），不支持 4 项（原子组、占有量词、条件分支、递归模式）。

📘 [MDN · RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `preg_*` 系列直接绑定 **PCRE2**，是主流语言里最"原汁原味"的 PCRE 方言：反向引用、变长后向环视、命名组三种拼写、`\p{...}`、原子组、占有量词、条件分支、递归、`\K` 全都在，只有字符类交集与减法例外。它的写法是**定界符加修饰符**（`/pattern/flags`），修饰符一共 13 个，其中 `u` 最关键——它同时打开 UTF-8 与 UCP，是 PHP 里让 `\d`/`\w`/`\s` 变成 Unicode 语义的开关。执行时间方面 PHP 是少数几个把 PCRE 限制暴露成配置项的语言：`pcre.backtrack_limit`（默认 1000000）、`pcre.recursion_limit`（默认 100000）与 `pcre.jit`（默认 1）都可以在 php.ini 或运行时设置，超限时 `preg_last_error()` 会给出 `PREG_BACKTRACK_LIMIT_ERROR` 之类的错误码。

```php
// ① 定界符 + 修饰符：/pattern/flags
preg_match('/^(?<y>\d{4})-(?<m>\d{2})$/', '2026-09', $m);
echo $m['y'];                                     // 2026

// ② 修饰符 13 个：i m s x A D S U X J u n r
preg_match('/abc/i', 'ABC');                      // 1    忽略大小写
preg_match('/^b/m', "a\nb");                      // 1    多行
preg_match('/a.b/s', "a\nb");                     // 1    . 匹配换行
preg_match('/a b/x', 'ab');                       // 1    扩展模式
preg_match('/\w/u', '汉');                        // 1    u = UTF-8 + UCP
preg_match('/\w/', '汉');                         // 0    不加 u 时 \w 是 ASCII

// ③ PCRE2 全套：环视、原子组、占有量词、条件分支、递归
preg_match('/(?<=foo)bar/', 'foobar');            // 1    后向环视（可以变长）
preg_match('/(?>a*)a/', 'aaa');                   // 0    原子组
preg_match('/a*+a/', 'aaa');                      // 0    占有量词
preg_match('/(a)(?(1)b|c)/', 'ab');               // 1    条件分支
preg_match('/^(\((?:[^()]|(?1))*\))$/', '(a(b))'); // 1  递归子模式

// ④ PHP 8.5 起 \K 不能再出现在环视里（扩展的默认编译选项不再包含 PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK）
// preg_match('/(?=a\K)/', 'a');                  // 🛑 编译错误

// ⑤ 字符类交集/减法：PHP 8.5 打包 PCRE2 10.44，而 && -- ~~ 要 PCRE2 10.45+
preg_match('/^[a-z&&[^aeiou]]$/', '&]');          // 1（&& 被当普通字符，不是减法）
```

13 个修饰符的含义分别是：`i`（`PCRE_CASELESS`，忽略大小写）、`m`（`PCRE_MULTILINE`，`^`/`$` 匹配每行）、`s`（`PCRE_DOTALL`，`.` 匹配换行）、`x`（`PCRE_EXTENDED`，忽略未转义空白、`#` 起注释）、`A`（`PCRE_ANCHORED`，强制从头匹配）、`D`（`PCRE_DOLLAR_ENDONLY`，`$` 只在绝对末尾生效）、`S`（**PHP 7.3 起已是空操作**，早期用于额外模式研究）、`U`（`PCRE_UNGREEDY`，反转贪婪性）、`X`（`PCRE_EXTRA`，把无意义反斜杠转义变成错误）、`J`（`PCRE_INFO_JCHANGED`，允许重名子组，PHP 7.2 起可作修饰符）、`u`（`PCRE_UTF8`，并把模式与主语当 UTF-8）、`n`（`PCRE_NO_AUTO_CAPTURE`，PHP 8.2 起，普通 `(...)` 变成非捕获）、`r`（`PCRE2_EXTRA_CASELESS_RESTRICT`，PHP 8.4 起，`u`+`i` 下禁止 ASCII 与非 ASCII 之间跨类匹配，比如 Kelvin 符号）。**没有 `e`**（早已移除，现在只报 "Unknown modifier"），**没有 `g`**（要全部匹配用 `preg_match_all`）。⚠️ 三个坑。第一，**`u` 不只是编码开关**：php-src 里 `case 'u'` 同时设置了 `PCRE2_UTF` 与 `PCRE2_UCP`，所以加了 `u` 之后 `\d`/`\w`/`\s` 才变 Unicode 语义，不加就永远是 ASCII——这一点与 R 的 `perl = TRUE`（默认不开 UCP，要写 `(*UCP)`）正好相反，而 php.net 的修饰符页面本身只写了 `PCRE_UTF8`，光看手册会漏掉 UCP 那半句。第二，字符类交集/减法在 PHP 8.5 里**不可用**：php-src 的 `PHP-8.5` 分支打包的是 **PCRE2 10.44**（`pcre2.h` 里 `PCRE2_MINOR 44`，日期 2024-06-07），而 UTS#18 的 `&&`/`--`/`~~`（`PCRE2_ALT_EXTENDED_CLASS`）是 **10.45** 才加入的。第三，PHP 8.5 有一条真正的向后不兼容变更：PCRE 扩展的默认编译选项里不再包含 `PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK`（8.5 的 UPGRADING 原话是 "compiled without semi-deprecated PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK compile option"），而那个选项是 PCRE2 10.38 起禁止 `\K` 出现在环视断言里之后留下的唯一逃生口，因此原本能在 `(?=a\K)` 里用 `\K` 的代码在 8.5 会直接编译失败。函数面没有变化，仍是 11 个：`preg_filter`、`preg_grep`、`preg_last_error`、`preg_last_error_msg`、`preg_match`、`preg_match_all`、`preg_quote`、`preg_replace`、`preg_replace_callback`、`preg_replace_callback_array`、`preg_split`。统计口径沿用 12 项固定清单：PHP 8.5 支持 11 项，唯一不支持的是字符类交集/减法（受打包的 PCRE2 版本限制）。

📘 [php.net · PCRE 模式修饰符](https://www.php.net/manual/en/reference.pcre.pattern.modifiers.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的正则是**回溯**引擎，实现是 **Onigmo**（Oniguruma 的一个分支，Ruby 2.0 起成为默认引擎；`regcomp.c` 的文件头就写着 "Onigmo (Oniguruma-mod)"）。它的特性面是主流语言里最宽的之一：反向引用、前后向环视、命名组、`\p{...}`、原子组、占有量词、条件分支、子表达式递归、字符类交集全都支持；唯一收紧的地方是**后向环视必须定长**（顶层分支可以长度不同，例如 `(?<=a|bc)` 合法而 `(?<=a+)` 非法）。Ruby 还有两个别处少见的配套工具：`Regexp.timeout` 用来给正则加超时，`Regexp.linear_time?` 用来判断某个模式是否落在引擎的线性时间优化范围内。

```ruby
# ① 字面量 /.../ 与 Regexp.new；引擎是 Onigmo
re = /(?<y>\d{4})-(?<m>\d{2})/
re.match("2026-09")[:y]                        # "2026"
Regexp.new("a+", Regexp::IGNORECASE)           # /a+/i

# ② \d \w \s 默认是 ASCII；Unicode 只能走 \p{...}
/\d/.match?("٣")                               # false
/\w/.match?("汉")                              # false
/\s/.match?("\u00a0")                          # false
/\p{Greek}+/.match?("αβγ")                     # true
/\p{Han}+/.match?("汉字")                      # true

# ③ 回溯引擎的全套
/(a)\1/.match?("aa")                           # true
/(?<=foo)bar/.match?("foobar")                 # true
/(?>a*)a/.match?("aaa")                        # false（原子组阻断回溯）
/a*+a/.match?("aaa")                           # false（占有量词）
/(a)(?(1)b|c)/.match?("ab")                    # true（条件分支）
/\A(\((?:(\g<1>)?\)))\z/.match?("(())")        # true（\g<1> 子表达式调用）
/[a-z&&[^aeiou]]/.match?("b")                  # true（字符类交集）
/[a-z&&[^aeiou]]/.match?("a")                  # false

# ④ 后向环视必须定长
# /(?<=a+)b/                                   # 🛑 SyntaxError: invalid pattern in look-behind

# ⑤ 模式修饰符 i m x o 与常量
/abc/imx.options                               # 7（IGNORECASE=1 | EXTENDED=2 | MULTILINE=4）
Regexp::FIXEDENCODING; Regexp::NOENCODING      # 编码相关常量

# ⑥ 超时与线性时间判定（均自 Ruby 3.2 起）
Regexp.timeout                                 # nil（默认不超时）
Regexp.new("a+", timeout: 1.5).timeout         # 1.5
Regexp.linear_time?(/a/)                       # true
Regexp.linear_time?(/(a)\1/)                   # false
```

模式修饰符只有四个：`i`（忽略大小写）、`m`（**dot-all**，让 `.` 匹配换行——注意 Ruby 的 `m` 不是"多行"，因为 `^`/`$` 在 Ruby 里**永远**按行边界工作）、`x`（扩展模式，忽略空白并允许 `#` 注释）、`o`（插值模式，字面量里含插值时代码只求值一次并复用同一个 `Regexp` 对象）。对应的常量是 `Regexp::IGNORECASE`（1）、`Regexp::EXTENDED`（2）、`Regexp::MULTILINE`（4），另有编码相关的 `Regexp::FIXEDENCODING` 与 `Regexp::NOENCODING`；子表达式级别的开关写成 `(?i)`、`(?-i)`、`(?i:...)`，`Regexp#to_s` 输出的就是这种形式（例如 `/ab+c/ix.to_s` 得到 `"(?ix-m:ab+c)"`）。命名组语法是 `(?<name>...)`，也接受 `(?'name'...)`；命名反向引用写 `\k<name>`，数字反向引用写 `\1`（`\0` 是整个匹配）；递归要用子表达式调用 `\g<1>`、`\g<name>`，而不是 PCRE 的 `(?1)`。⚠️ 三个坑。第一，**后向环视定长**这条限制比 PHP/JS/.NET 严，从那些语言搬 `(?<=a+)` 会直接语法错误，需要改写或用 `\K`。第二，**占有量词的 `{n,m}` 变体不支持**：官方文档明确写了"`{min, max}` and its variants do not support possessive matching"，`a{2,3}+` 不是占有量词，只有 `*+`、`++`、`?+` 三个才是。第三，`Regexp.linear_time?` 的结论**不是关于这个模式的绝对性质**，官方文档特别说明它是"关于 Ruby 解释器的性质，不是关于参数正则的性质"，同一份正则在不同 Ruby 二进制上可能给出不同答案，当前算法来自一篇论文，将来可能改变——所以它只能当作粗略信号，不能当作安全保证。版本方面，Ruby 4.0 的 NEWS 里唯一与 Regexp 相关的变化是**升级到 Unicode 17.0（含 Emoji 17.0）**，属性表随之更新；此前有报告说"以 k 或 s 开头的正则（例如 `/\bslackware\b/i` 遇到非 ASCII 主语）在 4.0 变慢"，那是一次优化引入的**性能回归**（Bug #21824）：主分支已修复、issue 于 2026-01 关闭，但 4.0.x 的发布说明里没有它，本次在 Ruby 4.0.6 上实测仍可复现（同一非 ASCII 主语下比 `/\bzzz\b/i` 慢约 2.4 倍，去掉 `i` 标志即恢复正常）。这条与方言或特性无关。统计口径沿用 12 项固定清单：Ruby 支持 12 项全部（反向引用、前向环视、定长后向环视、命名组、`\p{...}`、原子组、占有量词（仅 `*+ ++ ?+`）、条件分支、递归子表达式调用、内联标志、懒惰量词、字符类交集），只是在后向环视的定长约束与 `{n,m}+` 的缺失上比其他 PCRE 系语言更严格一些。

📘 [docs.ruby-lang.org · Regexp](https://docs.ruby-lang.org/en/4.0/Regexp.html)

{{% /tab %}}

{{< /tabpane >}}

### 匹配与查找

匹配这件事的第一道分岔不是引擎，而是**语义**：你要的是"串里有没有"，还是"整串是不是"，还是"从头开始的一段是不是"。Python 把这三种拆成 `search`/`fullmatch`/`match`，Java 拆成 `find`/`matches`/`lookingAt`，Go 与 C 只给部分匹配、全匹配全靠锚点，而 Swift 干脆把三种各起一个名字（`firstMatch`/`wholeMatch`/`prefixMatch`）。第二道分岔是**位置单位**：同一句 `m.start()`，在 Rust 里是字节、在 Python 里是码点、在 JavaScript 与 C# 里是 UTF-16 码元、在 Ruby 里默认是字符而 `byteoffset` 才是字节——弄错这一层，切片就会切在半个字符上。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 标准库没有正则，社区事实标准是 `regex` crate：它用有限自动机实现，对任意输入都保证线性时间，代价是**不支持** backreference 与 lookaround（要这两样得换 `fancy-regex` 或 `pcre2` crate）。它的 API 只有"部分匹配"一种语义：`is_match` 判断串里任意位置是否命中，`find` 返回第一个 `Match`，要全匹配必须自己加 `^...$` 或 `\A...\z` 锚点。返回值上的偏移一律是**字节偏移**，且保证落在 UTF-8 码点边界上，所以可以直接拿去切 `&str` 而不会 panic。

```rust
use regex::{Regex, RegexBuilder};
use std::sync::LazyLock;

static RE: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\d+").unwrap());

fn main() {
    let s = "订单 A12 与 B7";

    println!("is_match={}", RE.is_match(s));           // is_match=true   部分匹配：任意位置命中即可

    let m = RE.find(s).unwrap();
    println!("find={} range={:?}", m.as_str(), m.range());  // find=12 range=8..10   字节偏移

    let full = Regex::new(r"^\d+$").unwrap();
    println!("full={} {}", full.is_match("12"), full.is_match("12a"));   // full=true false

    let lines = Regex::new(r"^\w+$").unwrap();
    let ml = RegexBuilder::new(r"^\w+$").multi_line(true).build().unwrap();
    println!("m={} {}", lines.find_iter("a\nb").count(), ml.find_iter("a\nb").count());  // m=0 2

    println!("all={:?}", RE.find_iter(s).map(|m| m.as_str()).collect::<Vec<_>>());
    // all=["12", "7"]
    println!("ranges={:?}", RE.find_iter(s).map(|m| (m.start(), m.end())).collect::<Vec<_>>());
    // ranges=[(8, 10), (16, 17)]

    let empty = Regex::new(r"\d*").unwrap();
    println!("empty={:?}", empty.find_iter("a1").map(|m| (m.start(), m.end())).collect::<Vec<_>>());
    // empty=[(0, 0), (1, 2)]   紧贴前一个匹配末尾的空匹配被丢弃

    let ci = RegexBuilder::new(r"abc").case_insensitive(true).build().unwrap();
    let dot = RegexBuilder::new(r"a.b").dot_matches_new_line(true).build().unwrap();
    println!("flags={} {} {}", ci.is_match("ABC"), Regex::new(r"a.b").unwrap().is_match("a\nb"), dot.is_match("a\nb"));
    // flags=true false true

    let u = Regex::new(r"\w+").unwrap();
    println!("unicode={} bytes={}", u.find("中").unwrap().as_str(), u.find("中").unwrap().end());
    // unicode=中 bytes=3   位置按字节算

    let ascii = Regex::new(r"(?-u)\w+").unwrap();
    println!("ascii-only={}", ascii.is_match("中"));   // ascii-only=false
}
```

`regex` crate 的 `Regex` 类型文档里明确写着"所有匹配都相当于在模式两端各加了一个隐式的 `(?s:.)*?`"——这句话就是"只有部分匹配"的正式表述，所以 `^\d+$` 与 `\A\d+\z` 是仅有的全匹配手段，前者受 `(?m)` 影响而后者不受。位置单位是字节这点在纯 ASCII 上看不出来，一旦串里有汉字，`find("中").end()` 就会返回 3 而不是 1；反过来，如果你确实想按字节把 `\w` 限制成 ASCII，就用 `(?-u)` 内联关掉 Unicode，或者换成 `regex::bytes::Regex`。

预编译复用是 Rust 最需要注意的地方：`Regex::new` 的开销不小，而且**不像高层语言那样有自动缓存**，所以文档直接说"在循环里重复编译同一个正则是坏主意"。惯用做法是用 `OnceLock`/`LazyLock` 存成静态量（如上例），或者把 `Regex` 放在结构体里只编译一次。空匹配方面，`find_iter` 迭代时会把"紧贴上一个匹配末尾的空匹配"丢掉，因此 `\d*` 扫 `"a1"` 只得到 `[(0, 0), (1, 2)]`，而扫 `"ab"` 会得到 `[(0, 0), (1, 1), (2, 2)]`——这个规则与 Go 一致，跟 Python 不一致。

📘 [Rust `regex` 1.13.1 · `struct Regex`](https://docs.rs/regex/latest/regex/struct.Regex.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 从 5.7 起有了真正的正则字面量（`/.../`，无歧义写法是 `#/.../#`）和一套强类型的 `Regex` API，底层是自研引擎，与 Foundation 里那套 `NSRegularExpression` 是彼此独立的两个实现。它的三分为 `contains`（部分匹配）、`wholeMatch(of:)`（全匹配）、`prefixMatch(of:)`（前缀匹配），而 `firstMatch(of:)` 只是"找第一个、从哪开始都行"。匹配结果的位置用 `Range<String.Index>` 表示，所以和 `String` 的索引体系天然对齐，不需要手工换算下标。

```swift
import Foundation

let s = "订单 A12 与 B7"
let re = #/\d+/#                                             // #/.../# 是无歧义的正则字面量

print(s.contains(re))                                        // true   部分匹配
print(s.wholeMatch(of: re) != nil, "12".wholeMatch(of: re) != nil)          // false true
print("12ab".prefixMatch(of: re) != nil, "a12".prefixMatch(of: re) != nil)  // true false

if let m = s.firstMatch(of: re) {                            // 返回 Regex<Output>.Match
    print(m.0, m.range.lowerBound.utf16Offset(in: s), m.range.upperBound.utf16Offset(in: s))
}                                                            // 12 4 6
print(s.matches(of: re).map { String($0.0) })                // ["12", "7"]
print(s.ranges(of: re).map { s.distance(from: s.startIndex, to: $0.lowerBound) })   // [4, 10]

print("a1".matches(of: #/\d*/#).map { ($0.range.lowerBound.utf16Offset(in: "a1"), String($0.0)) })
// [(0, ""), (1, "1"), (2, "")]   空匹配在推进时也算一次结果

print("a\nb".matches(of: #/^\w+$/#.anchorsMatchLineEndings()).count)                // 2
print("a\nb".contains(#/a.b/#), "a\nb".contains(#/a.b/#.dotMatchesNewlines()))      // false true
print("ABC".contains(#/abc/#.ignoresCase()))                                        // true

let ns = try! NSRegularExpression(pattern: "[0-9]+")                                // 另一套老 API
let hits = ns.matches(in: s, range: NSRange(s.startIndex..., in: s))
print(hits.map { ($0.range.location, $0.range.length) })                            // [(4, 2), (10, 1)]
```

`Regex` 的匹配结果 `.0` 是整个匹配（多捕获组时依次是 `.1`、`.2`），位置则通过 `.range` 给出的 `Range<String.Index>` 访问；因为它是真正的 `String.Index`，跨 emoji 和组合字符都不会切错，代价是不能直接当整数用，要显式 `distance(from:to:)` 或 `utf16Offset(in:)` 换算。`matches(of:)` 是**集合式**接口（一次性返回 `[Match]`），`ranges(of:)` 只给区间，二者都不需要你自己推 `lastIndex`；空匹配在 Swift 里同样会出现在每个位置，包括空串尾部。

⚠️ 最容易踩的是 Swift 同时存在两套正则：新的 `Regex`/`RegexComponent`（支持字面量、类型化捕获、Builder）与老的 `NSRegularExpression`（返回 `NSTextCheckingResult`，`NSRange` 用 **UTF-16 码元**计数）。选择上，纯 Swift 项目一律用新 API；只有在需要与 Foundation 老代码互通、或者需要 `NSRegularExpression` 独有的选项时才用老的。标志位方面，新 API 走链式方法（`.ignoresCase()`、`.anchorsMatchLineEndings()`、`.dotMatchesNewlines()`），老 API 走 `NSRegularExpression.Options`。

📘 [Apple Developer · Swift `Regex`](https://developer.apple.com/documentation/swift/regex)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `regexp` 包用 RE2 的语法与自动机实现，因此**不支持** backreference 与 lookaround，但对任意输入保证线性时间，从设计上免疫 ReDoS。匹配语义只有部分匹配一种：`MatchString` 是布尔判断，`FindString`/`FindStringIndex` 给第一个匹配，全匹配要靠 `^...$` 锚点。位置一律是**字节下标**，返回结构是 `[]int` 或 `[]int` 的切片。

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	s := "订单 A12 与 B7"
	re := regexp.MustCompile(`\d+`)

	fmt.Println(re.MatchString(s))            // true    部分匹配
	fmt.Println(re.FindString(s))             // 12
	fmt.Println(re.FindStringIndex(s))        // [8 10]  字节下标
	fmt.Println(re.FindAllString(s, -1))      // [12 7]  n < 0 表示全部
	fmt.Println(re.FindAllString(s, 1))       // [12]    n >= 0 表示最多 n 个
	fmt.Println(re.FindAllStringIndex(s, -1)) // [[8 10] [16 17]]

	full := regexp.MustCompile(`^\d+$`)                // Go 没有 fullmatch，只能锚定
	fmt.Println(full.MatchString("12"), full.MatchString("12a"))   // true false

	empty := regexp.MustCompile(`\d*`)
	fmt.Println(empty.FindAllStringIndex("a1", -1))   // [[0 0] [1 2]]
	fmt.Println(empty.FindAllStringIndex("ab", -1))   // [[0 0] [1 1] [2 2]]

	ci := regexp.MustCompile(`(?i)abc`)
	ml := regexp.MustCompile(`(?m)^\w+$`)
	fmt.Println(ci.MatchString("ABC"), len(ml.FindAllString("a\nb", -1)))   // true 2

	u := regexp.MustCompile(`\w+`)
	fmt.Println(u.FindString("中"), u.FindStringIndex("中"))   // (空) []   \w 在 Go 里只含 ASCII

	fmt.Println(regexp.MustCompile(`a|ab`).FindString("ab"))   // a   左边优先（leftmost-first）
}
```

Go 的 API 命名很有规律：包文档说那 24 个匹配方法的名字都匹配 `(All|Find|FindAll)(String)?(Submatch)?(Index)?` 这个式子——`Find` 系返回第一个匹配，`FindAll` 系一次返回切片且 `n < 0` 表示要全部；带 `String` 的接字符串、不带 `String` 的接 `[]byte`，带 `Submatch` 的返回捕获组数组，带 `Index` 的返回字节下标而不是子串。（包文档把 `All` 也写进了命名式子，但实际导出的方法里只有 `Find`/`FindAll` 两族，并没有单独的 `All*` 方法，所以"全部匹配"这条路上 Go 只给切片，没有惰性迭代器。）文档对返回值有一句必须记住的话：对字符串版本而言"空字符串既可能表示没有匹配，也可能表示空匹配"，所以**判断有没有匹配要用 `MatchString` 或 `Index` 版本，不要用 `FindString` 的结果是否为空串**。

空匹配的规则写在包文档里："Empty matches abutting a preceding match are ignored."。这正是 `\d*` 扫 `"a1"` 得到 `[[0 0] [1 2]]`（末尾的 `[2 2]` 紧贴前一个匹配的结束位置，被忽略）而扫 `"ab"` 得到 `[[0 0] [1 1] [2 2]]` 的原因。另外要注意 Go 的 `\w`、`\d`、`\s` 都是 **ASCII-only** 的字符类，想匹配 Unicode 字母要写 `\p{L}` 或 `[\p{L}\p{N}_]`；`regexp` 本身没有为 Go 1.27 增加新 API，仍是这套编译/查找模型。

📘 [Go · `regexp` 包文档](https://pkg.go.dev/regexp)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `re` 是回溯引擎，支持 backreference、lookaround、命名组、原子组与占有量词（后两者自 3.11 起），但**不支持** `\p{...}` Unicode 属性——那是第三方 `regex` 模块的能力。三种语义有正式名字：`re.search` 是部分匹配、`re.match` 只要求从下标 0 开始（**不要求到结尾**）、`re.fullmatch` 才要求整串。返回值统一是 `Match` 对象或 `None`，位置按**码点**计。

```python
import re

s = "订单 A12 与 B7"
re.search(r"\d+", s).group()        # '12'   部分匹配：任意位置命中
re.match(r"\d+", s)                  # None   match 只从下标 0 开始，且不要求到结尾
re.match(r"\d+", "12abc").group()    # '12'
re.fullmatch(r"\d+", "12abc")        # None   fullmatch 才要求整串
re.fullmatch(r"\d+", "12").group()   # '12'
re.search(r"\d+\z", "12\n")          # None   \z 是 3.14 新增的串尾锚，\Z 现在与它同义

m = re.search(r"\d+", s)
(m.span(), m.start(), m.end())       # ((4, 6), 4, 6)   按码点计，不是字节
re.findall(r"\d+", s)                # ['12', '7']
[x.span() for x in re.finditer(r"\d+", s)]      # [(4, 6), (10, 11)]
[x.span() for x in re.finditer(r"\d*", "a1")]   # [(0, 0), (1, 2), (2, 2)]

bool(re.search(r"abc", "ABC", re.I))        # True   忽略大小写
len(re.findall(r"^\w+$", "a\nb", re.M))     # 2      多行：^ $ 按行
len(re.findall(r"^\w+$", "a\nb"))           # 0      默认 ^ $ 只匹配串首尾
bool(re.search(r"a.b", "a\nb", re.S))       # True   dotall
bool(re.search(r"a b  # 注释", "ab", re.X))  # True   扩展模式：空白与注释被忽略
re.fullmatch(r"\w", "中", re.A)             # None   关掉 Unicode 后 \w 只剩 ASCII
bool(re.fullmatch(r"\w", "中"))             # True   str 模式默认就是 Unicode

p = re.compile(r"\d+")               # 预编译一次，反复复用
(p.pattern, bool(p.flags & re.UNICODE))     # ('\\d+', True)
re.escape("a.b*c")                   # 'a\\.b\\*c'
re.search(r"(\d)(\d)", "x12").regs   # ((1, 3), (1, 2), (2, 3))   每个组的 (start, end)
```

`re.match` 是最容易被误当成"全匹配"的 API：它只锚定开头，所以 `re.match(r"\d+", "12abc")` 会成功匹配 `'12'`；要整串匹配只能用 `re.fullmatch`（3.4+）或者在模式两端都写锚点。`Match` 对象给三套位置访问：`start()`/`end()`/`span()`、`regs`（所有组的 `(start, end)` 元组）、以及 `groupdict()`/`groups()` 取内容；位置单位是码点，所以 `"中"` 的 `end()` 是 1 而不是 3。

预编译方面，`re.compile` 返回的 `Pattern` 对象可以反复 `search`/`finditer`，模块级的 `re.search` 等函数则走内部缓存——缓存由 `re._MAXCACHE` 控制（默认 512 条，3.7 起满时按 LRU 淘汰最久未用的一条，不再是整体清空），所以热路径上显式 `compile` 更稳。空匹配的规则是 Python 与 Rust/Go 分歧最大的地方：文档写明"空匹配会包含在结果里"，但"相邻的空匹配不可能出现，空匹配可以紧跟在非空匹配之后"，所以 `finditer(r"\d*", "a1")` 会给出 `[(0, 0), (1, 2), (2, 2)]`——末尾那个 `(2, 2)` 紧贴上一个匹配的结束位置，却**不会**被丢掉。3.14 对 `re` 的改动很小，只有两处：新增 `\z`（并使 `\Z` 与它同义），以及 `\B` 现在能匹配空输入串。

📘 [Python 3.14 · `re` —— 正则表达式操作](https://docs.python.org/3/library/re.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `Regex` 是 kotlin-stdlib 里的 `expect class`：JVM 上的模式语法直接就是 `java.util.regex.Pattern` 那一套（官方 JVM 页面写的是"For pattern syntax reference see `Pattern`"），Native/Wasm 上则是另一套实现，API 页还明确提示"模式语法与选项集合在各平台上有差异"，所以跨平台项目不能默认为 JVM 方言。它的语义三分是 `containsMatchIn`（部分匹配，返回 `Boolean`）、`matches`（全匹配，声明成 `infix fun`）、`matchEntire`（同样全匹配但返回 `MatchResult?`），另有 `matchAt(input, index)` 只在指定下标处尝试。全局查找用 `findAll`，它返回惰性的 `Sequence<MatchResult>`，这是它比 Java 的 `Matcher` 游标更好用的地方。

```kotlin
val s = "订单 A12 与 B7"
val re = Regex("""\d+""")                  // 三引号里反斜杠不必再转义

re.containsMatchIn(s)                      // true        部分匹配
re matches s                               // false       全匹配：整个输入都算
re matches "12"                            // true
re.matchEntire(s)                          // null        全匹配，返回 MatchResult?
re.matchEntire("12")?.value                // "12"
re.matchAt("a12", 1)?.value                // "12"        只在 index 处尝试
re.matchAt("a12", 0)                       // null

re.find(s)?.value                          // "12"
re.find(s, startIndex = 5)?.value          // "7"
re.findAll(s).map { it.value }.toList()    // ["12", "7"]  惰性 Sequence
re.findAll(s).map { it.range }.toList()    // [4..5, 10..10]

// 选项：Set<RegexOption>
Regex("abc", RegexOption.IGNORE_CASE).containsMatchIn("ABC")        // true
Regex("^b$", setOf(RegexOption.MULTILINE)).containsMatchIn("a\nb")  // true
Regex("a.b", RegexOption.DOT_MATCHES_ALL).containsMatchIn("a\nb")   // true
Regex("a b # 注释", RegexOption.COMMENTS).containsMatchIn("ab")      // true
Regex(Regex.escape("a.b*c")).containsMatchIn("a.b*c")               // true   把字面串量化

val NUMBER = Regex("""\d+""")              // 顶层 val：只编译一次，反复复用
NUMBER.findAll(s).count()                  // 2
NUMBER.pattern                             // "\\d+"（`Regex.pattern` 属性，自 1.0 起就有）
```

`matches` 是 `infix`，所以写成 `re matches "12"` 而不是 `re.matches("12")`；同义的 `matchEntire` 返回 `MatchResult?`，需要取值时少一次查找。`MatchResult` 给 `value`、`range`（`IntRange`）、`groupValues`、`groups`，位置单位与 Java 一致是 UTF-16 下标；空匹配对应的是"首大于尾"的空区间（如 `0..-1`），含义等同于 Java 的 `start == end`，只是表示法不同。`findAll` 返回 `Sequence` 意味着默认惰性求值，可以随意 `first()`/`take(n)` 而不会把整串扫完，这正是它相对 Java `Matcher` 显式循环的优势。

⚠️ 出了 JVM 就要当心：JVM 上 `RegexOption` 一共 7 个值，其中 `LITERAL`、`UNIX_LINES`、`COMMENTS`、`DOT_MATCHES_ALL`、`CANON_EQ` 在官方 API 页上只有 JVM/Native/Wasm 声明、没有 Common/JS 声明，也就是 **Kotlin/JS 上只有 `IGNORE_CASE` 与 `MULTILINE` 可用**；Native 与 Wasm 的 `Regex` 页面还专门写着两者的匹配与替换行为可以按标志向 JVM 实现对齐，说明引擎之间仍有差异。跨平台代码应把选项限制在最基础的这两个上，并靠测试而非假设来保证行为一致。

📘 [Kotlin stdlib 2.4 · `kotlin.text.Regex`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/-regex/)

{{% /tab %}}

{{% tab header="Java" %}}

`java.util.regex` 沿用 Perl 5 风格的语义（`Pattern` 文档里专门有一节 "Comparison to Perl 5"），模型是"编译一次的模式 + 带游标的匹配器"：`Pattern` 是不可变的编译结果，`Matcher` 保存当前匹配状态。三种语义由官方文档亲自命名：`matches()` 要求整个输入、`lookingAt()` 只要求从头开始的一段、`find()` 扫描下一个可匹配的子串。所有下标都是 **UTF-16 码元**（`char`）为单位，所以 BMP 之外的字符会占两个下标。

```java
import java.util.regex.*;

String s = "订单 A12 与 B7";
Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher(s);

m.matches();                 // false  整个输入
m.lookingAt();               // false  从下标 0 开始的一段
m.find();                    // true   扫描到下一个匹配
m.group();                   // "12"
m.start();                   // 4      UTF-16 码元下标
m.end();                     // 6
m.find();                    // true
m.group() + " " + m.start(); // "7 10"

p.matcher("12").matches();       // true
p.matcher("12a").lookingAt();    // true    前缀匹配
p.matcher("a12").lookingAt();    // false

// 全局迭代：Java 9+ 的 results() 直接给 Stream<MatchResult>
p.matcher(s).results().map(MatchResult::group).toList();     // [12, 7]
// 传统写法：Matcher 游标可反复 find()
Matcher it = p.matcher(s);
while (it.find()) { it.group(); it.start(); it.end(); }

// 区域（region）与边界感知
Matcher r = p.matcher("xx12yy");
r.region(2, 6).matches();        // true
r.regionStart() + " " + r.regionEnd();   // "2 6"

// 标志位
Pattern.compile("\\d").matcher("٣").find();                                  // false  默认 \d 只认 [0-9]
Pattern.compile("\\d", Pattern.UNICODE_CHARACTER_CLASS).matcher("٣").find();  // true   开了才是 Unicode 数字
Pattern.compile("^b$", Pattern.MULTILINE).matcher("a\nb").find();             // true
Pattern.compile("a.b", Pattern.DOTALL).matcher("a\nb").find();                // true
Pattern.compile("a b # 注释", Pattern.COMMENTS).matcher("ab").find();          // true
Pattern.compile("[0-9]+", Pattern.LITERAL).matcher("[0-9]+").find();          // true   模式按字面理解
Pattern.quote("a.b*c");                                                        // \Qa.b*c\E
```

`Matcher` 的 `find()` 是有状态的：每次调用都从上次匹配的结束位置继续，因此它天然就是全局迭代器；`matches()` 与 `lookingAt()` 则是一次性判定，但调用之后 `start()`/`end()` 仍然可用。`results()`（Java 9+）把游标循环包装成 `Stream<MatchResult>`，写函数式流水线时更省事；`MatchResult` 接口自身在 Java 20 增加了 `hasMatch()`，用来替代 `start() >= 0` 这种老写法。⚠️ 最容易踩的是 `\d`/`\w`/`\s` 默认**只认 ASCII**，要 Unicode 语义必须显式加 `UNICODE_CHARACTER_CLASS`（或用内联 `(?U)`）；另一个是 `region()` 只改变搜索范围，默认对 `^`/`$` 是"锚定边界"，想让环视看到区域外的字符要 `useTransparentBounds(true)`。命名组语法是 `(?<name>...)`，与 Python 的 `(?P<name>...)` 不同。版本上，`\X`（Unicode extended grapheme cluster）与 `\b{g}`（对应边界）自 JDK 9 起就支持，Java 26 只是把 Unicode 数据升到 17.0（Release Note JDK-8346945 顺带重申了 `java.util.regex` 基于 UAX #29 的这套支持）；Java 25 没有改动 `java.util.regex`，Java 26 的公开 API 集合本身也没有增删。

📘 [Java SE 25 · `java.util.regex.Matcher`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Matcher.html)

{{% /tab %}}

{{% tab header="C++" %}}

`std::regex` 自 C++11 起进入标准库，默认语法是"Modified ECMAScript-262"，实现是回溯的，长期以来饱受编译慢、体积大、缺命名组的批评；实际工程里更常用 RE2、Boost.Regex 或编译期匹配的 CTRE。它的入口只有两个算法：`std::regex_match` 要求整个区间、`std::regex_search` 接受任意位置的匹配；想"只在前缀处匹配"要用 `match_continuous` 这个 flag 位。全局迭代交给 `std::sregex_iterator`，位置单位是迭代器差值（对 `std::string` 就是字节下标）。

```cpp
#include <iostream>
#include <regex>
#include <string>

int main() {
    std::string s = "订单 A12 与 B7";
    std::regex re(R"(\d+)");
    std::smatch m;

    std::regex_search(s, m, re);                     // 部分匹配
    std::cout << m.str() << ' ' << m.position() << ' ' << m.length() << '\n';  // 12 8 2
    std::cout << m.prefix().str() << '\n';           // 订单 A

    std::string twelve = "12";
    std::cout << std::regex_match(s, re) << ' '           // 0  必须整串
              << std::regex_match(twelve, re) << '\n';    // 1

    std::string twelveab = "12ab";
    std::smatch a;
    std::cout << std::regex_search(s, a, re, std::regex_constants::match_continuous) << ' '  // 0
              << std::regex_search(twelveab, a, re,
                                   std::regex_constants::match_continuous) << '\n';          // 1

    for (auto it = std::sregex_iterator(s.begin(), s.end(), re), end = std::sregex_iterator();
         it != end; ++it) {
        std::cout << it->str() << ' ' << it->position() << ' ';   // 12 8 7 16
    }
    std::cout << '\n';

    std::string ABC = "ABC", a12 = "a12", anb = "a\nb", digits = "12";
    std::regex ci("abc", std::regex::icase);
    std::cout << std::regex_search(ABC, ci) << ' ';                        // 1
    std::regex base("[0-9]+", std::regex::extended);                       // 换 POSIX ERE 语法
    std::cout << std::regex_search(a12, base) << ' ';                      // 1
    std::regex ml("^[a-z]+$", std::regex::ECMAScript | std::regex::multiline);  // multiline 是 C++17
    std::cout << std::regex_search(anb, ml) << '\n';                       // 1

    std::regex ns(R"((\d)(\d))", std::regex::nosubs);                      // 不记录子匹配
    std::smatch nm;
    std::regex_search(digits, nm, ns);
    std::cout << nm.size() << '\n';                                        // 1：只剩整个匹配
    return 0;
}
```

`match_results` 给 `position(i)`、`length(i)`、`str(i)` 三个取值方法，另有 `prefix()`/`suffix()` 拿匹配前后的片段；`position()` 是"匹配起点相对搜索起点的距离"，对 `std::string` 而言是字节数而不是字符数，所以上面 `\d+` 在含汉字串里的 `position()` 是 8 而不是 4。语法方言由 `syntax_option_type` 选择：`ECMAScript`、`basic`、`extended`、`awk`、`grep`、`egrep` 六种语法（至多选一个，不选则默认 `ECMAScript`）加上 `icase`、`nosubs`、`optimize`、`collate` 与 C++17 加入的 `multiline` 五个选项位，共 11 个标准常量；匹配行为则由 `match_flag_type` 控制，共 13 个常量：`match_default`、`match_not_bol`、`match_not_eol`、`match_not_bow`、`match_not_eow`、`match_any`、`match_not_null`、`match_continuous`、`match_prev_avail`、`format_default`、`format_sed`、`format_no_copy`、`format_first_only`。

⚠️ 两个实际坑：`std::regex_search` 不能直接接临时 `std::string`（右值重载被显式删除），必须先把串存成变量，这在把多个调用写进一条 `cout` 链时特别容易踩；另外 `std::sregex_iterator` 对空匹配的处理有明文规则——`operator++` 会先带 `match_not_null | match_continuous` 重跑一次 `regex_search`，只有这次也失败才把起点前移一位，因此空匹配会被跳过，这一点与 Rust/Go 一致，而 Python 会把它留在结果里。C++23 与 C++26 都没有改动 `<regex>` 的接口——`syntax_option_type` 的最新条目停在 C++17（就是 `multiline`），`match_flag_type` 的 13 个常量则全部来自 C++11（只有整组常量本身在 C++17 变成 `inline`），engine 依然是 ECMAScript 的 "depth first search" 回溯实现，`<regex>` 还是那个"能用但别指望它变好"的库。

📘 [cppreference · `std::regex_search`](https://en.cppreference.com/w/cpp/regex/regex_search)

{{% /tab %}}

{{% tab header="C" %}}

C 的标准库**没有正则**，C23 也没有加入；能用的只有 POSIX 1003.2 的 `<regex.h>`，接口是 `regcomp`/`regexec`/`regfree`/`regerror` 四个函数加一个 `regex_t` 结构。它有两种方言：默认是 BRE（basic regular expression），加 `REG_EXTENDED` 才切到 ERE；两者都没有命名组、没有 `\d` 与 `\s` 这类简写、没有 lookaround，非贪婪量词在目前各实现遵循的 POSIX Issue 7 里也没有（Issue 8 才加入 `*?` 这类重复修饰符与 `REG_MINIMAL` 旗标）。`regexec` 一次只给**第一个**匹配，全局迭代必须自己写循环。

```c
#include <regex.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *s = "订单 A12 与 B7";
    regex_t re;
    regcomp(&re, "[0-9]+", REG_EXTENDED);          /* 不写 REG_EXTENDED 就是 BRE 方言 */

    regmatch_t m[1];
    int rc = regexec(&re, s, 1, m, 0);             /* 只找第一个匹配 */
    printf("%d %d %d %.*s\n", rc, (int)m[0].rm_so, (int)m[0].rm_eo,
           (int)(m[0].rm_eo - m[0].rm_so), s + m[0].rm_so);   /* 0 8 10 12 */
    regfree(&re);

    /* 全匹配只能靠锚点 */
    regex_t full;
    regcomp(&full, "^[0-9]+$", REG_EXTENDED);
    printf("%d %d\n", regexec(&full, "12", 0, NULL, 0) == 0,
                      regexec(&full, "12a", 0, NULL, 0) == 0);   /* 1 0 */
    regfree(&full);

    /* REG_NEWLINE：^ $ 从整串首尾变成行锚点 */
    regex_t nl, nl2;
    regcomp(&nl, "^[a-z]+$", REG_EXTENDED);
    regcomp(&nl2, "^[a-z]+$", REG_EXTENDED | REG_NEWLINE);
    printf("%d %d\n", regexec(&nl, "ab\ncd", 0, NULL, 0) == 0,
                      regexec(&nl2, "ab\ncd", 0, NULL, 0) == 0);  /* 0 1 */
    regfree(&nl); regfree(&nl2);

    /* REG_ICASE 忽略大小写；REG_NOSUB 只问"有没有"，不填 regmatch_t */
    regex_t ic;
    regcomp(&ic, "^abc$", REG_EXTENDED | REG_ICASE);
    printf("%d\n", regexec(&ic, "ABC", 0, NULL, 0) == 0);         /* 1 */
    regfree(&ic);

    /* 全局迭代：POSIX 不提供，得自己写；空匹配必须手动前进一个字节 */
    regex_t any;
    regcomp(&any, "[0-9]*", REG_EXTENDED);
    const char *t = "a1", *p = t;
    while (p <= t + strlen(t) && regexec(&any, p, 1, m, 0) == 0) {
        printf("[%ld,%ld) ", (long)(p - t + m[0].rm_so), (long)(p - t + m[0].rm_eo));
        if (m[0].rm_eo == 0) p++;      /* ⚠️ 少了这一行就是死循环 */
        else p += m[0].rm_eo;
    }
    putchar('\n');                                                /* [0,0) [1,2) [2,2) */
    regfree(&any);
    return 0;
}
```

位置单位是**字节**，`rm_so`/`rm_eo` 直接就是 `char` 数组下标；整个匹配失败时以 `regexec` 返回的 `REG_NOMATCH` 为准（此时 `regmatch_t` 的内容没有保证），只有在匹配成功时，没参与的子表达式才会被填成 `-1`。因为没有库级迭代，空匹配的规则完全由你自己的循环决定：上面的写法在空匹配时前进一个字节，于是 `[0-9]*` 扫 `"a1"` 会得到 `[0,0) [1,2) [2,2)`——包括末尾那个紧贴前一个匹配的空匹配；Rust 与 Go 的库会把这一类丢掉。这正是 C 的正则最需要小心的地方：语义不在库里，在你的循环里。

⚠️ 另外三点必须记住：BRE 里 `+`、`?`、`|`、`()` 都是普通字符，要写成 `\+`、`\?`、`\|`、`\(...\)` 才有特殊含义，而 ERE 里反过来；POSIX 的 ERE **没有**反向引用（BRE 才有 `\1`-`\9`），在 glibc、macOS、musl 目前实现的 Issue 7 里也没有最小匹配——`*?` 里的 `?` 只是把 `*` 变成普通字符加问号（Issue 8 才加入 `*?`/`+?`/`??`/`{m,n}?` 后缀与 `REG_MINIMAL`）；`REG_STARTEND` 这个常用的"在子区间里匹配"标志是 BSD/glibc 的扩展，不属于 POSIX，写了就失去可移植性。要 Unicode、命名组、环视或 ReDoS 防护，只能引 PCRE2、Oniguruma 或 RE2 这类第三方库。

📘 [POSIX · `regcomp` / `regexec`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Regex` 用 PCRE2 作后端，写法是非标准字符串字面量 `r"..."`，标志位直接跟在字面量后面（`r"..."i`）。匹配语义只有部分匹配一种：`occursin` 是布尔判断，`match` 返回 `RegexMatch` 或 `nothing`，全匹配要靠 PCRE 的 `\A...\z` 锚点。返回值结构是 `RegexMatch` 对象，位置字段 `offset`/`offsets` 的单位是**字节**——因为 Julia 的字符串下标本身就是"码元"下标（UTF-8 下即字节），这一点和 Python 的码点下标差别很大。

```julia
s = "订单 A12 与 B7"
re = r"\d+"                       # 等价于 Regex("\\d+")

occursin(re, s)                   # true                部分匹配，只看有没有
match(re, s)                      # RegexMatch("12")
match(re, s).offset               # 9                   字节下标（1 起算）
match(re, s, 11)                  # RegexMatch("7")     从第 11 个字节起找
match(re, "abc")                  # nothing

# 全匹配：PCRE 锚点 \A ... \z，没有 fullmatch
occursin(r"\A\d+\z", "12")        # true
occursin(r"\A\d+\z", "12a")       # false

# 全局迭代：eachmatch 是迭代器，findall 给范围
collect(eachmatch(re, s))                 # 2-element Vector{RegexMatch}："12"、"7"
[m.match for m in eachmatch(re, s)]       # ["12", "7"]
[m.offset for m in eachmatch(re, s)]      # [9, 17]
findall(re, s)                            # [9:10, 17:17]
findfirst(re, s)                          # 9:10

# overlap 开关：默认要求各匹配落在互不重叠的字符范围里
length(collect(eachmatch(r"a.a", "a1a2a3a")))                  # 2
length(collect(eachmatch(r"a.a", "a1a2a3a", overlap = true)))  # 3

# 标志位写在字面量后面：i m s x a
occursin(r"abc"i, "ABC")          # true
occursin(r"^b$"m, "a\nb")         # true                多行
occursin(r"a.b"s, "a\nb")         # true                dotall
occursin(r"a b  # 注释"x, "ab")   # true                扩展模式
occursin(r"\w"a, "中")            # false               a = ASCII/按字节模式
occursin(r"\w", "中")             # true                默认 Unicode

# 预编译复用：字面量每次求值都会编译，要复用就存成变量或 const
const NUM = r"\d+"                # 只编译一次
length(collect(eachmatch(NUM, s)))   # 2
```

`match(r, s, idx)` 的第三个参数是**字节下标**，且默认的 UTF 模式下必须落在某个字符的首字节上，否则 PCRE2 会以 UTF 偏移错误失败——这是 Julia 把字符串下标定义成码元的直接后果。`RegexMatch` 暴露 `match`（整个匹配）、`captures`（各组的 `SubString`）、`offset`（整个匹配起点）、`offsets`（各组起点，未参与匹配的组为 0），并且可以按组名或组号索引；`keys`、`iterate`、`length` 也都有定义，所以能直接解构。

`eachmatch` 的 `overlap` 关键字是 Julia 独有的：默认为 `false`，文档要求各匹配来自互不重叠的字符范围；设为 `true` 后就允许重叠，像 `r"a.a"` 扫 `"a1a2a3a"` 会从 2 个变成 3 个。要拿"所有匹配的位置"就用 `findall`，它返回基于字节下标的 `UnitRange` 向量。⚠️ 一个容易误传的点是"Julia 的 offset 是字符下标"——官方手册明确写的是"String indices in Julia refer to code units (= bytes for UTF-8)"，所以下标就是字节下标。Julia 1.13 没有 Regex 相关变更；1.12 增加了用 `RegexMatch` 构造 `NamedTuple`/`Dict` 的能力。

📘 [Julia 1.13 · `eachmatch` 与正则函数](https://docs.julialang.org/en/v1/base/strings/#Base.eachmatch)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的 `System.Text.RegularExpressions` 默认是回溯引擎（官方文档原话是"By default, .NET's regex engine uses backtracking"），自 .NET 7 起另有保证线性时间的 `RegexOptions.NonBacktracking` 模式可选。它的 API 分成三层：`Regex.IsMatch` 只回布尔、`Regex.Match` 返回 `Match` 对象（部分匹配，用 `Success` 判断有没有）、`Regex.Matches` 返回 `MatchCollection`；`Match` 自己就是游标，`NextMatch()` 直接往后走。`Match.Index`/`Length` 的单位是 UTF-16 码元。

```csharp
using System.Text.RegularExpressions;

string s = "订单 A12 与 B7";
var re = new Regex(@"\d+");

re.IsMatch(s);                    // true        部分匹配
Match m = re.Match(s);
m.Success;                        // true
m.Value;                          // "12"
m.Index;                          // 4           UTF-16 码元下标
m.Length;                         // 2
m.NextMatch().Value;              // "7"         Match 自带游标

// 全匹配：没有 fullmatch，用 \A ... \z
new Regex(@"\A\d+\z").IsMatch("12");     // true
new Regex(@"\A\d+\z").IsMatch("12a");    // false

// 全局迭代
re.Matches(s).Count;                                       // 2
re.Matches(s).Select(x => (x.Value, x.Index));             // [("12",4), ("7",10)]
foreach (ValueMatch v in re.EnumerateMatches(s))           // .NET 7+：不分配 Match 对象
    Console.WriteLine((v.Index, v.Length));                // (4,2) 然后 (10,1)

// 选项
new Regex("^b$", RegexOptions.Multiline).IsMatch("a\nb");                     // true
new Regex("a.b", RegexOptions.Singleline).IsMatch("a\nb");                    // true
new Regex("a b # 注释", RegexOptions.IgnorePatternWhitespace).IsMatch("ab");   // true
new Regex(@"(\d)(\d)", RegexOptions.ExplicitCapture).GetGroupNumbers();       // 只剩 [0]
new Regex(@"\d+", RegexOptions.NonBacktracking).IsMatch("12");                // true 且线性时间

// 源生成器：编译期生成匹配代码，类与方法都要 partial（.NET 7+）
public partial class Patterns
{
    [GeneratedRegex(@"\d+")]
    public static partial Regex Digits();
}

// .NET 10 的行为变更：可选组里的懒惰量词
new Regex(@"a(b.*?c)?d").Match("abccd").Success;
// .NET 9 → true；.NET 10 GA（10.0.0–10.0.3）→ false；10.0.4 起修复回 true
```

`Match` 与 `MatchCollection` 的区别在返回时机：`Match` 是即时求值的结果，需要一个一个 `NextMatch()` 往前走；`MatchCollection` 是惰性填充的集合，遍历到哪个才算到哪个。真正追求零分配的场景要用 `EnumerateMatches`（.NET 7+），它返回 `ValueMatchEnumerator`，里面的 `ValueMatch` 是 `ref struct`，只在 `MoveNext()` 时报告 `Index`/`Length`，不构造 `Match`；.NET 9 又补了对称的 `EnumerateSplits`。

选项在 .NET 10 里一共 11 个成员：`None`、`IgnoreCase`、`Multiline`、`ExplicitCapture`、`Compiled`、`Singleline`、`IgnorePatternWhitespace`、`RightToLeft`、`ECMAScript`、`CultureInvariant`、`NonBacktracking`。⚠️ `AnyNewLine`（值 2048）是 .NET 11 才加入的第 12 个成员：Learn 的 `?view=net-10.0` 字段表里能看到它，是文档站没有按版本过滤字段表造成的假象（`?view=net-9.0` 也照样列它），以 dotnet/runtime `v10.0.0` 的源码和选项指南里标注的 .NET 11 为准，按 10 写代码时不要依赖它。⚠️ `NonBacktracking` 有限制：它不能与 `RightToLeft`、`ECMAScript`、`AnyNewLine` 组合，也不支持 backreference、lookaround、原子组、条件表达式、平衡组与 `\G`——换来的是对任意输入都线性时间。

⚠️ 最后是一条必须写明的版本坑：.NET 10 给回溯引擎加的"原子循环优化"一度做错了判断，表现就是可选组里的懒惰量词行为变了（PR dotnet/runtime#124254 是修复它的补丁，该优化本身只在 .NET 10 引入）。最小复现是 `new Regex(@"a(b.*?c)?d").Match("abccd").Success`——.NET 9 为 `true`，.NET 10 的 10.0.0–10.0.3 变成 `false`，修复已回移到 10.0.4 服务版本（PR #124287，milestone 就是 10.0.4），所以**升到 10.0.4 及以上就恢复一致**；这件事没有 Microsoft Learn 的官方破坏性变更页，只有 [dotnet/runtime#125321](https://github.com/dotnet/runtime/issues/125321)。另有一个相关的 [dotnet/runtime#129511](https://github.com/dotnet/runtime/issues/129511)（嵌套可选组 + 懒惰捕获循环在 `Compiled`/`[GeneratedRegex]` 下抛 `IndexOutOfRangeException`），该 issue 已按 11.0.0 里程碑关闭，不会回移到 10.0.x。

📘 [MS Learn · `System.Text.RegularExpressions.Regex`](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regex?view=net-10.0)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `RegExp` 是自研引擎（历史渊源是 V8 的 Irregexp），官方文档写明它"implements the ECMAScript RegExp specification"，因此语义与 JavaScript 一致、实现是回溯的——API 页甚至用 `^(a*|b)*c` 这个经典例子专门警告过回溯爆炸。它的语义三分是 `hasMatch`（部分匹配布尔）、`matchAsPrefix`（只在开头/指定位置尝试）、以及"整串"要靠自己写 `^...$`；`firstMatch` 返回 `RegExpMatch?`，`allMatches` 返回 `Iterable<RegExpMatch>`。位置单位默认是 UTF-16 码元，构造时打开 `unicode:` 才按码点匹配。

```dart
final s = '订单 A12 与 B7';
final re = RegExp(r'\d+');             // raw string，省掉一层转义

re.hasMatch(s);                        // true        部分匹配
final m = re.firstMatch(s);            // RegExpMatch?
m?.start;                              // 4           UTF-16 码元下标
m?.end;                                // 6
m?.group(0);                           // '12'
m?.groupCount;                         // 0
re.stringMatch(s);                     // '12'

re.allMatches(s).map((x) => x[0]).toList();      // ['12', '7']
re.allMatches(s).map((x) => x.start).toList();   // [4, 10]

re.matchAsPrefix('12ab')?.end;         // 2     只在开头匹配（返回 Match?）
re.matchAsPrefix('a12');               // null

// 全匹配：没有 fullmatch，用 ^...$ 锚点
RegExp(r'^\d+$').hasMatch('12');       // true
RegExp(r'^\d+$').hasMatch('12a');      // false

// 构造参数与选项：multiLine、caseSensitive、unicode、dotAll
RegExp(r'abc', caseSensitive: false).hasMatch('ABC');   // true
RegExp(r'^b$', multiLine: true).hasMatch('a\nb');       // true
RegExp(r'a.b', dotAll: true).hasMatch('a\nb');          // true
RegExp(r'^.$').hasMatch('😀');                          // false  默认一个码元只匹配一个 UTF-16 单元
RegExp(r'^.$', unicode: true).hasMatch('😀');           // true   代理对算一个码点

// 预编译复用：RegExp 对象可反复使用；编译到 Web 时退化为浏览器引擎
final num = RegExp(r'\d+');
num.allMatches(s).length;              // 2
RegExp.escape('a.b*c');                // 'a\.b\*c'
```

`matchAsPrefix` 是这套 API 里的原语：它把"从这个下标开始能不能匹配"这件事单独暴露出来，`hasMatch`、`firstMatch`、`allMatches` 都可以看作它的封装，所以想在指定位置锚定匹配就直接用它，而不是自己拼 `^`。`unicode:` 开关不只是让 `.` 认代理对，文档还说明开启后会收紧模式语法（Unicode 属性转义等只在 Unicode 模式可用），因此在处理 emoji 或罕见字符时应默认打开；代价是引擎要做码点级处理。

⚠️ 三个容易记错的细节：`allMatches` 的返回类型是 `Iterable<RegExpMatch>` 而不是 `Iterable<Match>`；`namedGroup` 只在 `RegExpMatch` 上有，普通 `Match` 没有；`groups` 是 `Match` 上的一个**方法**（签名是 `List<String?> groups(List<int> groupIndices)`）而不是属性，这与 .NET、Java 的习惯相反。版本上，`RegExp.escape` 是 **Dart 2.0.0** 就有的（不是 2.19），Dart 3.12 给 VM 引擎加了 modifier spans 与重复命名捕获组，而 Dart 3.13 没有任何 RegExp/Match 变更。

📘 [Dart 3.13 · `dart:core` `RegExp` 类](https://api.dart.dev/stable/latest/dart-core/RegExp-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的正则不在扩展包里，而是 `base` 的一组函数：`grep`/`grepl`/`regexpr`/`gregexpr`/`regexec`/`sub`/`gsub`/`strsplit`。默认引擎是 POSIX ERE 的 TRE 实现（文档在讲近似匹配时直接指向 TRE 文档），`perl = TRUE` 才切到 PCRE（当前是 PCRE2）语义，`fixed = TRUE` 则退化成字面查找。它的返回结构在 18 门语言里最杂：`grep` 给下标、`grepl` 给逻辑值、`regexpr` 给起始位置加 `match.length` 属性、`gregexpr` 给列表、`regexec` 给"整个匹配加各组起点"的列表。

```r
s <- "订单 A12 与 B7"

grep("[0-9]+", s)                # [1] 1      命中元素的下标（输入本来就是向量）
grepl("[0-9]+", s)               # [1] TRUE   逻辑值版本
regexpr("[0-9]+", s)             # [1] 5      attr(,"match.length") [1] 2
gregexpr("[0-9]+", s)            # [[1]] [1] 5 11   attr(,"match.length") [1] 2 1
regmatches(s, gregexpr("[0-9]+", s))   # [[1]] "12" "7"
regexec("([0-9])([0-9])", "x12")       # [[1]] [1] 2 2 3  attr(,"match.length") [1] 2 1 1

# 全匹配只能靠锚点
grepl("^[0-9]+$", "12")          # [1] TRUE
grepl("^[0-9]+$", "12a")         # [1] FALSE

# 默认的 TRE/ERE 引擎已经带了一批扩展
grepl("\\d+", s)                 # [1] TRUE   \d \w \s \D \S 都是 R 对 POSIX ERE 的扩展
grepl("\\w+", s)                 # [1] TRUE   \w 等价于 [[:alnum:]_]
grepl("a.*?b", "axxb")           # [1] TRUE   给量词加 ? 得到最小匹配，ERE 下也支持

# perl = TRUE 才切到 PCRE2：断言、命名组这些 Perl 语义只有它有
grepl("(?<=A)\\d+", s, perl = TRUE)     # [1] TRUE   后行断言
grepl("(?<num>\\d+)", s, perl = TRUE)   # [1] TRUE   命名组
regexpr("(?<=A)\\d+", s, perl = TRUE)   # [1] 5      attr(,"match.length") [1] 2

# 位置单位：默认按字符，useBytes = TRUE 才按字节
regexpr("[0-9]+", s)                    # [1] 5
regexpr("[0-9]+", s, useBytes = TRUE)   # [1] 9      前 4 个字符在 UTF-8 下占 8 字节
```

`regexpr` 与 `gregexpr` 的位置默认按**字符**计，`useBytes = TRUE` 才变成字节，而且这时结果上会带一个 `useBytes` 属性；文档还提醒 `useBytes` 的主要作用是避免多字节 locale 下的编码告警与错配，但它会抑制输入编码转换，所以不要把它当成纯粹的"换个计数单位"开关。`regexec` 返回的是每个输入元素对应的整数向量：第 1 个数是整个匹配的起点，后面依次是各捕获组的起点，没参与的组给 `-1`。

⚠️ 这里有一条与网上常见说法相反的细节：**`\d`、`\w`、`\s` 这些简写类在 R 的默认引擎里就能用**，官方 `regex` 帮助页把它们明确列为 R 对 POSIX ERE 的扩展；真正只有 `perl = TRUE` 才有的，是 `(?=...)`、`(?<=...)` 这类 lookaround 断言以及命名组。另外文档说默认引擎里 `^`/`$` 匹配的是"行的"首尾，所以喂进来的字符串含换行时，"全匹配"的判断要格外小心。R 4.4 让 PCRE 命名捕获支持超过 127 个命名组，R 4.5 增加了 `grepv()`（并把 `grep`/`strsplit` 等对非 TRUE/FALSE 逻辑参数的处理改成报 `NA`）；R 4.6 没有任何正则相关改动。

📘 [R 4.6 · Pattern Matching and Replacement（`grep` 及其家族）](https://stat.ethz.ch/R-manual/R-devel/library/base/html/grep.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的**标准库没有正则**：`std` 里既没有 `std.regex` 也没有任何模式语言，只有 `std.mem` 这一组字节级查找与切分工具（`indexOf`、`startsWith`、`tokenizeAny` 等）。所以"匹配与查找"在 Zig 里就是"找子串、找字节、按分隔符切分"，没有捕获组、没有重复量词、没有回溯；要用真正的正则只能引第三方库、在编译期用 `@cImport` 接 C 的正则库，或者用 `comptime` 自己写一个小匹配器。所有下标都是 `usize` 字节下标，找不到统一返回 `?usize` 的 `null`。

```zig
const std = @import("std");

pub fn main() void {
    const s = "订单 A12 与 B7";

    // 唯一的"匹配"手段是字节级查找，返回 ?usize
    _ = std.mem.indexOf(u8, s, "12");             // 8     0 起的字节下标
    _ = std.mem.lastIndexOf(u8, s, "7");          // 16
    _ = std.mem.indexOfPos(u8, s, 9, "7");        // 16    从第 9 个字节继续找
    _ = std.mem.indexOfScalar(u8, s, 'A');        // 7
    _ = std.mem.indexOfAny(u8, s, "0123456789");  // 8     集合里任意一个字节
    _ = std.mem.indexOfNone(u8, s, "0123456789"); // 0     第一个不在集合里的字节

    // 前缀、后缀、相等：都是布尔判断
    _ = std.mem.startsWith(u8, s, "订单");         // true
    _ = std.mem.endsWith(u8, s, "B7");            // true
    _ = std.mem.eql(u8, s, s);                    // true

    // "数一数匹配了几次"用 count
    _ = std.mem.count(u8, s, "1");                // 1

    // 全局迭代：自己用 indexOfPos 推进
    var i: usize = 0;
    while (std.mem.indexOfPos(u8, s, i, " ")) |p| {
        std.debug.print("{d} ", .{p});            // 6 10 14
        i = p + 1;
    }

    // 切分与分词
    var it = std.mem.tokenizeScalar(u8, "a1b22c", 'b');
    while (it.next()) |tok| std.debug.print("{s} ", .{tok});   // a1 22c
}
```

因为没有模式语言，"匹配"这件事必须拆成你真正需要的那一步：只问"有没有"就用 `indexOf` 判 `!= null`；要找所有出现位置就自己用 `indexOfPos` 循环（注意每次把起点推进到 `p + 1`，否则空 needle 会原地打转）；要按分隔符拆就用 `splitSequence`/`splitAny`（保留空片段）或 `tokenizeAny`/`tokenizeScalar`（跳过空片段），这两组的选择规则与很多语言的 `split` 与 `split + filter` 之分一样。

⚠️ 由此带来的两个现实结论：一是别指望在 Zig 里写 `\d+` 或环视，遇到"用正则更方便"的需求要早点决定是引依赖还是换成手写状态机；二是 Zig 把"查找"和"切分"分得很清楚，`std.mem` 里没有正则那种"一次调用同时给出位置与捕获"的复合结构，所有上下文都得你自己带着走。这些 `std.mem` 函数在 0.13 时就已经是现在的名字，0.14 只是把旧的 `tokenize`/`split` 别名改成会报废弃错误的 `@compileError`（按分隔符分词用 `tokenizeAny`/`tokenizeSequence`/`tokenizeScalar`，保留空片段用 `splitSequence`/`splitAny`），0.15 没有再做 `std.mem` 的改名或新增，照上表列出的函数名写即可。

📘 [Zig 0.15 · `std.mem` 标准库文档](https://ziglang.org/documentation/master/#std.mem)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有正则，`string.find`/`string.match`/`string.gmatch`/`string.gsub` 用的是 **Lua pattern**——一门比正则小得多的模式语言。它**没有** `|` 交替、**没有** lookaround，量词非贪婪要写 `-` 而不是 `*?`；它独有的东西是 `%b`（平衡匹配）、`%f`（frontier 模式）以及 `%1`-`%9` 反向引用。位置一律是 **1 起的字节下标**，因为 Lua 的字符串就是一串字节。

```lua
local s = "订单 A12 与 B7"

-- string.find 给起止下标（1 起、字节），找不到返回 nil
print(string.find(s, "%d+"))            -- 9  10
print(string.find(s, "12", 1, true))    -- 9  10   第四个参数 true = 纯文本查找
print(string.find(s, "z"))              -- nil

-- string.match 直接给内容；有捕获时只给捕获
print(string.match(s, "%d+"))           -- 12
print(string.match(s, "(%d)(%d)"))      -- 1      只返回捕获
print(string.match("A12", "A(%d+)"))    -- 12
print(string.match(s, "%d+", 11))       -- 7      第三个参数指定 1 起的字节起点

-- 全局迭代：gmatch 是迭代器
for n in string.gmatch(s, "%d+") do io.write(n, " ") end   -- 12 7
print()

-- 全匹配只能靠 ^ $ 锚点
print(s:match("^%d+$") ~= nil)          -- false
print(("12"):match("^%d+$") ~= nil)     -- true

-- 字符类是"一个字母 + 大写取反"，且都是字节层面的 ASCII 类
print(("a1"):match("%a"))               -- a
print(("中"):match("%a"))               -- nil     %a 只认 ASCII 字母
print(#"中")                            -- 3       # 数的是字节
print(#(("中"):match(".")))             -- 1       . 一次只吃一个字节

-- 贪婪 / 非贪婪 / 平衡 / frontier
print(("<a><b>"):match("<.->"))         -- <a>      - 是最短匹配
print(("<a><b>"):match("<.*>"))         -- <a><b>   * 是最长匹配
print(("(a(b)c)"):match("%b()"))        -- (a(b)c)
print(("THE (quick) fox"):match("%f[%a]%a+%f[%A]"))   -- THE

-- %1-%9 反向引用是支持的
print(("hello hello"):match("(%a+) %1"))   -- hello
```

pattern 的完整语法只有八个条目：字符类、`类*`、`类+`、`类-`、`类?`、`%n`、`%bxy`、`%f[set]`，魔术字符恰好是 `^$()%.[]*+-?`——所以 `|` 在 Lua 里就是普通字符，写不出"或"的分支，要交替只能拆成多次匹配或用 `gsub` 配合函数。字符类一共 11 个（`%a` 字母、`%c` 控制符、`%d` 数字、`%g` 可打印非空白、`%l` 小写、`%p` 标点、`%s` 空白、`%u` 大写、`%w` 字母数字、`%x` 十六进制、加上 `.` 任意字符），把字母大写就得到补集（`%A`、`%C`、`%D`、`%G`、`%L`、`%P`、`%S`、`%U`、`%W`、`%X`）。

⚠️ 三条最容易出错的规则：第一，位置是字节而不是字符，`print(#"中")` 是 3，`("中"):match(".")` 只拿到一个字节，所以处理 UTF-8 文本时 `string.find` 返回的下标不能直接当"第几个字符"用；第二，`^` 与 `$` 只在模式的开头与结尾才有锚定含义，写在中间就是字面字符；第三，要查找含 `%`、`.`、`*` 等魔术字符的字面文本，要么用 `string.find(s, text, 1, true)` 走 `plain` 模式，要么用 `%` 逐个转义。Lua 5.5 把字符串库挪到了手册 §6.5、模式一节挪到 §6.5.1（5.4 里是 §6.4/§6.4.1），但模式语法本身与 5.4 逐字相同，§8 的三节不兼容清单里没有任何 pattern 相关条目。

📘 [Lua 5.5 · Patterns（§6.5.1）](https://www.lua.org/manual/5.5/manual.html#6.5.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript **没有自己的正则引擎**：`/.../ ` 字面量与 `new RegExp(...)` 都是 JavaScript 的 `RegExp`，匹配、查找、迭代的全部语义都由 ECMAScript 规定，TypeScript 只额外提供静态类型（`RegExp`、`RegExpMatchArray`、`RegExpExecArray`，以及 `groups`/`indices` 的索引签名）。因此这一页里 TS 与 JS 的差别不在运行时行为，而在类型标注与 `lib` 配置。TypeScript 7 是编译器的原生（Go）重写版，编译速度大幅提升，但不改变任何运行时正则语义。

```typescript
const s: string = "订单 A12 与 B7";

// 部分匹配：test 是布尔入口
/\d+/.test(s);                     // true

// exec 的结果类型是 RegExpExecArray | null，带 index / input / groups
const g: RegExp = /\d+/g;
const m: RegExpExecArray | null = g.exec(s);
m?.[0];                            // '12'
m?.index;                          // 4        UTF-16 码元下标

// matchAll 的结果是 IterableIterator<RegExpMatchArray>，要求带 g
const all: RegExpMatchArray[] = [...s.matchAll(/\d+/g)];
all.map((x) => [x[0], x.index]);   // [['12', 4], ['7', 10]]

// 全匹配：只能靠 ^...$ 锚点
/^\d+$/.test("12");                // true
/^\d+$/.test("12a");               // false

// d 标志（ES2022）：indices 是每个捕获组的 [start, end)
const d = /(?<num>\d+)/d.exec(s);
d?.indices?.[0];                   // [4, 6]
d?.indices?.groups?.num;           // [4, 6]

// 字符串侧的方法同样可用，注意 match 加不加 g 结果形状不同
s.match(/\d+/g);                   // ['12', '7']
s.match(/\d+/);                    // ['12', index: 4, input: '...']  只给第一个
s.search(/\d+/);                   // 4

// TS 特有的部分：类型标注与 lib 版本
const named: RegExp = /(?<num>\d+)/;
const num: string | undefined = named.exec(s)?.groups?.num;   // '12'
RegExp.escape("a.b*c");            // ES2025 的新标准方法，需 lib 包含对应版本才有类型
```

类型层面最值得注意的是 `exec` 与 `match` 的返回类型差别：`exec` 给 `RegExpExecArray | null`（`index` 与 `input` 非可选），而 `String.prototype.match` 在带 `g` 时给 `RegExpMatchArray | null`、不带 `g` 时给带 `index` 的 `RegExpMatchArray | null`，类型上无法区分这两种形状，所以严格模式下更推荐 `matchAll`（`IterableIterator<RegExpMatchArray>`，元素一定带 `index`）或 `exec` 循环。

⚠️ 两个纯 TypeScript 侧的坑：`String.prototype.matchAll` 在运行时会校验标志，传一个不带 `g` 的正则直接抛 `TypeError: String.prototype.matchAll called with a non-global RegExp argument`，而类型系统拦不住这件事；另一个是 `RegExp.escape`（ES2025）与 `v` 标志（ES2024，unicodeSets）都属于新的标准库，`tsconfig` 的 `lib` 里没有对应版本时编译器会报"属性不存在"，此时要么升级 `lib` 要么在类型上做局部声明——不要以为是运行时没有。

📘 [MDN · JavaScript 正则表达式语法（ECMAScript 规范）](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Regular_expressions)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `RegExp` 是 ECMAScript 规范定义的那一套，也是本页其他语言反复对照的基准。它的入口是 `test`（布尔）、`exec`（返回带 `index`/`input`/`groups`/`indices` 的数组）以及字符串侧的 `match`/`matchAll`/`search`。最需要先知道的是**带 `g`（或 `y`）的正则对象是有状态的**：它把上次匹配的结束位置记在 `lastIndex` 上，于是同一个对象连续调用会"接力"，这是 JS 正则最常见的 bug 来源。下标单位是 UTF-16 码元。

```javascript
const s = "订单 A12 与 B7";

// test：带 g 时会被 lastIndex 影响
const g = /\d+/g;
g.test(s);            // true    lastIndex 变成 6
g.test(s);            // true    lastIndex 变成 11
g.test(s);            // false   已到串尾，lastIndex 归 0
g.lastIndex = 0;      // ⚠️ 想重新开始必须手动归零

// exec：返回 RegExpExecArray，带 index / input / groups
const m = g.exec(s);
m[0];                 // "12"
m.index;              // 4       UTF-16 码元下标
m.input === s;        // true

// 全匹配只能靠锚点
/^\d+$/.test("12");   // true
/^\d+$/.test("12a");  // false

// 全局迭代：match(带 g) 与 matchAll(必须带 g)
s.match(/\d+/g);                                     // ["12", "7"]
[...s.matchAll(/\d+/g)].map((x) => [x[0], x.index]);  // [["12",4], ["7",10]]
s.match(/\d+/);                                       // 只给第一个匹配的数组

// d 标志（ES2022）：indices 给每个组的 [start, end)
const d = /(?<num>\d+)/d.exec(s);
d.indices[0];              // [4, 6]
d.indices.groups.num;      // [4, 6]

// y（sticky）：只在上次结束处匹配
const y = /\d+/y;
y.lastIndex = 4;
y.test(s);                 // true
y.test(s);                 // false   下标 6 处不是数字

// 空匹配：matchAll 逐位给出空匹配，不会死循环
[..."a1".matchAll(/\d*/g)].map((x) => [x.index, x[0]]);   // [[0,""],[1,"1"],[2,""]]

// 预编译复用与转义
const pre = new RegExp("\\d+", "g");
s.match(pre);                             // ["12", "7"]
/\d+/gimsy.flags;                         // "gimsy"  规范规定按 dgimsuvy 顺序输出
RegExp.escape("a.b*c");                   // "\x61\.b\*c"（ES2025）
new RegExp("[\\p{L}--[a]]", "v").test("中");   // true（v 标志，ES2024）
```

`test` 与 `exec` 共享同一套游标：`exec` 成功时把 `lastIndex` 推到匹配末尾，失败时复位为 0；`test` 内部就是调用 `exec`，所以两者对同一对象的调用顺序会互相影响。字符串侧的 `match` 则不受调用者影响——带 `g` 时它内部会把 `lastIndex` 归零并返回所有匹配的字符串数组（**不给 `index`、不给捕获组**），不带 `g` 时等价于一次 `exec`。要同时拿到所有匹配和它们的位置，正确的做法是 `matchAll`（必须带 `g`，否则抛 `TypeError`）或自己写 `exec` 循环。

⚠️ 三个必须记住的陷阱：第一，`lastIndex` 是**对象属性**而不是调用参数，模块级共享一个带 `g` 的正则会让不同调用互相干扰，函数内应该新建或用 `matchAll`；第二，`v` 标志（ES2024）与 `u` 标志互斥，`v` 开启字符类集合运算（如 `[\p{L}--[a]]`）并收紧语法；第三，`RegExp.escape`（ES2025）会把首个字母数字转义成 `\xHH`、把 `-`、`=`、`&` 这类标点转义成 `\xHH`，所以它的输出形状与手写的转义不同，但它是唯一在各种上下文里都安全的重写方式。空匹配方面，`matchAll`/`replaceAll` 规范规定在空匹配处必须前进一个位置（`u`/`v` 模式下前进一个码点），所以 `\d*` 扫 `"a1"` 会给出 `[[0,""],[1,"1"],[2,""]]` 而不会死循环。

📘 [MDN · `RegExp`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/RegExp)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 PCRE2，入口是 `preg_*` 一族函数，模式是带定界符的字符串（`'/.../'`）。`preg_match` 是部分匹配，返回 `1`/`0`/`false`；`preg_match_all` 一次算完全局匹配并返回个数。结果不是对象而是一个数组：`$matches[0]` 是整个匹配、`$matches[1]` 起是各捕获组；要位置必须显式传 `PREG_OFFSET_CAPTURE`，拿到的偏移量是**字节**偏移。PHP 没有 `fullmatch`，全匹配靠 `^...$` 锚点。

```php
$s = "订单 A12 与 B7";

// preg_match：部分匹配，返回 1 / 0 / false，必须用 === 判断
preg_match('/\d+/', $s, $m);          // 1
$m[0];                                // '12'
preg_match('/\d+/', 'abc', $m2);      // 0，$m2 退化为空数组
preg_match('/\d+/', 'abc');           // 0

// 全匹配：没有 fullmatch，用 ^ ... $
preg_match('/^\d+$/', '12');          // 1
preg_match('/^\d+$/', '12a');         // 0

// 位置：字节偏移，且必须开 PREG_OFFSET_CAPTURE
preg_match('/(\d+)/', $s, $o, PREG_OFFSET_CAPTURE);
$o[0];                                // ['12', 8]   匹配文本 + 字节偏移
$o[1];                                // ['12', 8]   第 1 个捕获组

// 未参与匹配的组：默认补空串，PREG_UNMATCHED_AS_NULL 则给 null
preg_match('/(a)(b)*(c)/', 'ac', $u);
$u;                                   // [0=>'ac', 1=>'a', 2=>'', 3=>'c']
preg_match('/(a)(b)*(c)/', 'ac', $v, PREG_UNMATCHED_AS_NULL);
$v;                                   // [0=>'ac', 1=>'a', 2=>null, 3=>'c']

// 全局迭代：preg_match_all 一次算完并返回个数
$cnt = preg_match_all('/\d+/', $s, $all);        // 2
$all[0];                                         // ['12', '7']（默认 PREG_PATTERN_ORDER）
preg_match_all('/\d+/', $s, $byMatch, PREG_SET_ORDER);
$byMatch;                                        // [['12'], ['7']]

// 从指定字节起点继续找
preg_match('/\d+/', $s, $t, PREG_OFFSET_CAPTURE, 11);
$t[0];                                           // ['7', 16]

// 修饰符
preg_match('/abc/i', 'ABC');        // 1    大小写不敏感
preg_match('/^b$/m', "a\nb");       // 1    ^ $ 按行
preg_match('/a.b/s', "a\nb");       // 1    dotall
preg_match('/a b # 注释/x', 'ab');   // 1    扩展模式
preg_match('/\w/u', '中');          // 1    UTF-8 语义
preg_match('/\d+/A', 'a12');        // 0    A = 强制锚定在串首
preg_match('/\d+/', 'a12');         // 1

// 复用与自省
function digits(string $t): array { return preg_match_all('/\d+/', $t, $r) ? $r[0] : []; }
digits($s);                         // ['12', '7']
preg_quote('a.b*c', '/');           // 'a\.b\*c'
preg_last_error();                  // PREG_NO_ERROR
preg_last_error_msg();              // 'No error'
```

`preg_match` 的返回值必须用 `===` 判断，因为模式出错时它返回 `false` 而 `false == 0`：写成 `if (preg_match(...))` 会把"没匹配"和"编译失败"混在一起，出错时要靠 `preg_last_error()`/`preg_last_error_msg()` 拿具体原因（回溯超限是 `PREG_BACKTRACK_LIMIT_ERROR`，递归超限是 `PREG_RECURSION_LIMIT_ERROR`，UTF-8 非法是 `PREG_BAD_UTF8_ERROR`）。`preg_match_all` 里的 `$matches` 形状由顺序标志决定：默认 `PREG_PATTERN_ORDER` 是"按组分层"（`$all[0]` 是全部整个匹配、`$all[1]` 是全部第 1 组），`PREG_SET_ORDER` 则是"按次分组"（`$byMatch[0]` 是第一次匹配的各组）；不显式传时默认就是前者。

修饰符一共 13 个：`i`（忽略大小写）、`m`（`^`/`$` 按行）、`s`（`.` 匹配换行）、`x`（忽略空白与 `#` 注释）、`A`（强制锚定串首）、`D`（`$` 只匹配串尾，`m` 生效时被忽略）、`S`（PHP 7.3 起已无效果）、`U`（反转贪婪性）、`X`（PCRE_EXTRA，未定义含义的反斜杠转义报错）、`J`（允许重复命名组）、`u`（UTF-8 模式）、`n`（PHP 8.2 起，普通括号不再自动捕获）、`r`（PHP 8.4 起，`PCRE2_EXTRA_CASELESS_RESTRICT`，阻止 ASCII 与非 ASCII 在忽略大小写时互配，例如 `/\x{212A}/iu` 会匹配 `"K"` 而加上 `r` 就不会）。

⚠️ 版本相关的两点：PHP 8.5 的 PCRE 扩展改成**不带 `PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK` 编译**，也就是 lookaround 里的 `\K` 不再被允许，这是 8.5 唯一一条 PCRE 相关的兼容性变更；打包的 PCRE2 版本以 php-src 的 `pcre2.h` 为准是 10.44（php.net 的迁移指南写成 10.46，但 10.45/10.46 的两次升级在发布前都被回退了，存在文档与源码不一致的情况）。另外 PHP 8.5.10 起，UTF-8 模式下的 `\C` 被明确禁止（它会对多字节字符做半字节匹配）。PHP 8.5 没有 `preg_*` 的弃用项。

📘 [PHP 8.5 · `preg_match`](https://www.php.net/manual/en/function.preg-match.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Regexp` 用 Onigmo 引擎，语法能力很全（命名组、环视、原子组、占有量词都有）。三个入口要分清：`match` 返回 `MatchData` 或 `nil`，`match?` 只返回布尔而且**不更新 `$~` 等全局变量**（只想知道"有没有"时用它，快且不污染环境），`=~` 返回第一个匹配的**字符**下标。另外 `^`/`$` 在 Ruby 里天生就是**行**锚点，串首尾要用 `\A`/`\z`。位置默认按字符，字节要用 `byteoffset`。

```ruby
s = "订单 A12 与 B7"
re = /\d+/

re.match(s).to_s              # "12"         MatchData#to_s 就是整个匹配
re.match?(s)                  # true         只回布尔，不设置 $~
re.match?("abc")              # false
re =~ s                       # 4            字符下标（同时设置 $~）
s.match?(/\d+/, 6)            # true         第二个参数是按字符的起点

# 全匹配：没有 fullmatch，用 \A ... \z
/\A\d+\z/.match?("12")        # true
/\A\d+\z/.match?("12a")       # false
/\d+/.match?("12a")           # true         不加锚点就是部分匹配

# 全局迭代：scan 一次给所有匹配；带捕获时给"数组的数组"
s.scan(/\d+/)                 # ["12", "7"]
s.scan(/(\d)(\d)/)            # [["1", "2"]]
s.enum_for(:scan, /\d+/).map { Regexp.last_match.begin(0) }   # [4, 10]

# MatchData 的位置：字符 vs 字节
m = re.match(s)
[m.begin(0), m.end(0), m.offset(0)]   # [4, 6, [4, 6]]
m.byteoffset(0)                       # [8, 10]    字节偏移（3.2+）
m.string.equal?(s)                    # false      返回的是冻结副本，不是原对象

# 标志位：i 忽略大小写，m 是 dotall（不是多行锚点），x 扩展模式
/abc/i.match?("ABC")          # true
/a.b/m.match?("a\nb")         # true        Ruby 的 m 等于别家的 s
/^b$/.match?("a\nb")          # true        ^ $ 天生是行锚点
/\Ab\z/.match?("a\nb")        # false       \A \z 才是串首尾
/a b  # 注释/x.match?("ab")    # true

# 空匹配：scan 会在每个位置给出空匹配
"a1".scan(/\d*/)              # ["", "1", ""]

# 预编译复用与超时防护
NUM = /\d+/
NUM.match?(s)                 # true
Regexp.escape("a.b*c")        # "a\\.b\\*c"
Regexp.union("a", "b")        # /a|b/
Regexp.linear_time?(/\d+/)    # true        能否保证线性时间
Regexp.timeout                # nil         默认不限制匹配耗时
```

`MatchData` 是唯一同时给出字符与字节两套位置的对象：`begin`/`end`/`offset` 按**字符**计，`byteoffset`（Ruby 3.2 起）按**字节**计，编解码或做字节级协议时要显式选后者。`scan` 是"只要匹配内容"的快捷方式，但它不给你位置——要位置就用 `enum_for(:scan, ...)` 配合 `Regexp.last_match`，或者直接写 `while m = re.match(s, pos)` 的循环自己推进。⚠️ `MatchData#string` 返回的是**冻结副本**而不是原字符串（文档原话是"Returns the target string if it was frozen; otherwise, returns a frozen copy"），所以 `m.string.equal?(s)` 是 `false`，别拿 `equal?` 去比对。

⚠️ 三个 Ruby 特有的坑：第一，`/m` 的含义与大多数语言相反，它是 dotall（`.` 匹配换行），锚点行为不受它影响；第二，`^`/`$` 默认就是行锚点，写"整串校验"必须用 `\A...\z`，用 `^...$` 会在多行输入上误判；第三，`Regexp.timeout`/`Regexp.timeout=` 与 `Regexp.linear_time?` 都是 Ruby 3.2 引入的，前者可以给匹配设一个墙钟上限（默认 `nil` 即不限），后者只判断"这个模式能否用线性时间算法保证"——两者都不改变语义，只影响失控时的表现。版本上，Ruby 4.0 的 NEWS 里没有任何 Regexp 或 MatchData 的行为条目（只有"Unicode 升到 17.0，也适用于 Regexp"），把 `Regexp` 实例全部冻结、以及新增 `MatchData#integer_at` 是 4.1 的事，不要写进 4.0。

📘 [Ruby 4.0 · `Regexp`](https://docs.ruby-lang.org/en/4.0/Regexp.html)

{{% /tab %}}

{{< /tabpane >}}

### 捕获组、替换与切分

捕获组、替换与切分是正则表达式里最常用的三件事，也最容易在语言之间搬错：命名组在 Python 里只认 `(?P<name>...)`，在 .NET、Java、PCRE、Ruby 里是 `(?<name>...)` 或 `(?'name'...)`，Rust 两种都收，而 C++ 的 `std::regex` 与 POSIX 干脆没有命名组；替换模板更是一家一套，`$1` 与 `\1` 各有拥趸，`$&`、`` $` ``、`$'` 只有 JavaScript、C# 与 C++ 认，Python 与 Ruby 走 `\g<name>`、`\k<name>` 这条线；切分则要盯住两件事——分隔符会不会留在结果里、尾部空字段会不会被丢掉。本节按**捕获组语法 → 反向引用与条件模式 → 替换模板与回调 → 切分与转义函数**这四类顺序逐语言给出可直接套用的写法。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的 `regex` crate 是**线性时间**的自动机引擎，它没有反向引用、没有环视、没有原子组，所以本节里它只能演示捕获组、替换、切分与转义。命名组两种写法 `(?P<name>...)` 与 `(?<name>...)` 都接受，取值走 `Captures` 的 `name()`、`&caps["name"]` 或下标；替换既可以用 `$1`、`$name`、`${name}` 模板，也可以直接传一个 `|&Captures| -> String` 的闭包。

```rust
use regex::{escape, Captures, NoExpand, Regex};

fn main() {
    // 命名组：(?P<name>...) 与 (?<name>...) 两种写法等价
    let re = Regex::new(r"(?P<y>\d{4})-(?<m>\d{2})").unwrap();
    let caps = re.captures("2026-09").unwrap();
    println!("{} {} {} {}", &caps["y"], &caps["m"], &caps[1], &caps[2]);
    // 2026 09 2026 09
    println!("{:?}", re.capture_names().collect::<Vec<_>>());
    // [None, Some("y"), Some("m")]

    // 替换模板：$1、$name、${name}、$$；NoExpand 关掉模板展开
    let re2 = Regex::new(r"(?<last>\w+),\s*(?<first>\w+)").unwrap();
    println!("{}", re2.replace("Doe, John", "$first $last"));       // John Doe
    println!("{}", re2.replace("Doe, John", "${first}_$last"));     // John_Doe
    println!("{}", re2.replace("Doe, John", "$$$first"));           // $John
    println!("{}", re2.replace("Doe, John", NoExpand("$first")));   // $first

    // 闭包替换：拿到 &Captures，可以自由计算后再拼回去
    let out = re2.replace_all("Doe, John; Smith, Ann", |c: &Captures| {
        format!("{}|{}", &c["first"].to_uppercase(), &c["last"].to_lowercase())
    });
    println!("{out}");   // JOHN|doe; ANN|smith

    // 切分：split 会产出空字段，splitn 带 limit（limit 0 得到空迭代器）
    let sp = Regex::new(r",\s*").unwrap();
    println!("{:?}", sp.split("a, b,c").collect::<Vec<_>>());       // ["a", "b", "c"]
    println!("{:?}", sp.splitn("a, b,c", 2).collect::<Vec<_>>());   // ["a", "b,c"]
    println!("{:?}", Regex::new("X").unwrap().split("lionXXtigerXleopard").collect::<Vec<_>>());
    // ["lion", "", "tiger", "leopard"]

    // 转义：把任意字符串变成只匹配自身的模式
    println!("{}", escape("a.b*c(d)"));                            // a\.b\*c\(d\)

    // ⚠️ 反向引用不是 regex crate 的语法，编译期就报错
    println!("{}", Regex::new(r"(a)\1").unwrap_err());
    // 实测输出是三行：首行 "regex parse error:"，第二行回显 "(a)\1" 并标出 ^^，
    // 末行才是原因 error: backreferences are not supported
}
```

替换模板的名字取「最长匹配」：`$1a` 会被当成名为 `1a` 的组，要写 `${1}a` 才能断开；引用不存在的组或名字会替换成空串，想输出字面 `$` 就写 `$$`。当替换内容来自用户输入时用 `NoExpand("...")`，否则用户串里的 `$1` 会被展开成捕获内容——这类「替换内容里的注入」是很容易踩的坑。切分默认保留空字段（连续分隔符产生空串，`"lionXXtigerXleopard"` 里的 `XX` 就产出一个空串），要压掉空字段得自己过滤或用 `[ \t]+` 这类写法定住分隔符；`splitn` 的 `limit` 是**输出片段数**而不是分隔符次数。`escape()` 生成的模式只匹配原字符串本身，`Regex::new(&escape(user_input))` 是把用户输入安全拼进模式的唯一推荐做法。需要反向引用或环视时不能硬凑，得换 `fancy-regex` 或 `pcre2` crate，代价是放弃线性时间保证。

📘 [docs.rs · regex::Regex（captures / replace_all / split / escape）](https://docs.rs/regex/latest/regex/struct.Regex.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 从 5.7 起有了原生的 `Regex` 类型，可以直接写 `/.../` 字面量或 `RegexBuilder` 风格的 DSL，命名组写 `(?<name>...)`，捕获值通过 `Match.output` 用 `.name` 或 `.1` 取。最需要先记住的一条反直觉规则是：`String.replacing(_:with:)` 传字符串时做的是**字面替换**，`$1`、`${name}` 不会被展开，要引用捕获必须传闭包；ICU 那套 `NSRegularExpression` 才是认 `$0`–`$9` 模板的世界。

```swift
import Foundation

// 命名组 (?<name>...)：取值走 output 的成员，也可按下标
let re = /(?<y>\d{4})-(?<m>\d{2})/
if let m = "2026-09".wholeMatch(of: re) {
    print(m.output.y, m.output.m)            // 2026 09
    print(m.output.1, m.output.2)            // 2026 09
}

// 替换：with: 传字符串是字面替换，引用捕获要传闭包
print("2026-09".replacing(re, with: "${m}/${y}"))   // ${m}/${y} ← 不展开，原样输出
print("hi there".replacing(/\w+/, with: { (mm: Regex<Substring>.Match) -> String in
    mm.output.uppercased() }))                      // HI THERE
print("a-b-c".replacing(/-/, with: "+"))            // a+b+c
print("a-b-c".replacing(/-/, maxReplacements: 1, with: { (_: Regex<Substring>.Match) -> String in "+" }))
// a+b-c

// 切分：split(separator:) 可以收一个 Regex
print("a, b,c".split(separator: ","))       // ["a", " b", "c"]
print("a, b,c".split(separator: /,\s*/))    // ["a", "b", "c"]

// 转义只有 Foundation 版本：escapedPattern(for:)
print(NSRegularExpression.escapedPattern(for: "a.b*c(d)"))   // a\.b\*c\(d\)

// NSRegularExpression：模板只认 $0–$9，${name} 不会被展开
let ns = try! NSRegularExpression(pattern: "(?<y>\\d{4})-(?<m>\\d{2})")
let r = NSRange(location: 0, length: 7)
print(ns.stringByReplacingMatches(in: "2026-09", range: r, withTemplate: "$1"))   // 2026
print(ns.stringByReplacingMatches(in: "2026-09", range: r, withTemplate: "${y}")) // ${y}
let hit = ns.firstMatch(in: "2026-09", range: r)!
print((("2026-09" as NSString).substring(with: hit.range(withName: "y"))))        // 2026

// 反向引用是 Swift Regex 的原生语法
print("aabb".firstMatch(of: /(\w)\1/) != nil)   // true
```

Swift 的 `Regex` 与 `NSRegularExpression` 是两套完全独立的 API，混用时的第一道坎就是替换模板：`replacing(_:with:)` 的字符串重载是字面替换（模板展开根本没有实现），`NSRegularExpression` 的 `withTemplate:` 只认 `$0`–`$9`（`${y}` 实测原样输出，`\1` 会被当成转义的 `1`），所以命名组在 Foundation 路线上只能先 `range(withName:)` 取范围再手动拼。切分要注意 `String.split(separator:)` 收字符串字面量时不会合并连续分隔符也不去空白，收 `Regex` 才按模式切，并且它默认丢弃空字段（`omittingEmptySubsequences: false` 才保留）。⚠️ 裸斜杠正则字面量需要 Swift 6 语言模式（`-swift-version 6`）；在 Swift 5 模式下要显式打开 `-enable-bare-slash-regex`，本次实测用的正是 `swift -swift-version 6 cap.swift`。

📘 [Apple Developer · Swift Regex](https://developer.apple.com/documentation/swift/regex)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `regexp` 是 RE2 语法、线性时间引擎，因此和 Rust 一样没有反向引用与环视。命名组在 RE2 里两种写法 `(?P<name>...)` 与 `(?<name>...)` 都合法，取值要靠 `FindStringSubmatch` 返回的切片配 `SubexpIndex`、`SubexpNames`，没有 `Match` 对象；替换模板是 `$name`/`${name}`/`$1`，需要字面替换时用 `ReplaceAllLiteralString`，需要计算时用 `ReplaceAllStringFunc`（只给整段匹配，不给捕获）。

```go
package main

import (
	"fmt"
	"regexp"
	"strings"
)

func main() {
	// 命名组：RE2 同时接受 (?P<name>...) 与 (?<name>...)
	re := regexp.MustCompile(`(?P<y>\d{4})-(?<m>\d{2})`)
	m := re.FindStringSubmatch("2026-09")
	fmt.Println(m[0], m[1], m[re.SubexpIndex("m")])   // 2026-09 2026 09
	fmt.Println(re.SubexpNames(), re.NumSubexp())     // [ y m] 2

	// 替换模板：$1、$name、${name}；字面 $ 要写 $$
	d := regexp.MustCompile(`(?P<last>\w+),\s*(?P<first>\w+)`)
	fmt.Println(d.ReplaceAllString("Doe, John", "$first $last"))      // John Doe
	fmt.Println(d.ReplaceAllString("Doe, John", "${first}_$last"))    // John_Doe
	fmt.Println(d.ReplaceAllLiteralString("Doe, John", "$first"))     // $first

	// 函数替换：参数是整段匹配字符串，需要捕获就在函数里再跑一次
	fmt.Println(d.ReplaceAllStringFunc("Doe, John", strings.ToUpper)) // DOE, JOHN

	// 切分：n < 0 全切，n == 0 返回 nil，分隔符一律不保留
	sp := regexp.MustCompile(`,\s*`)
	fmt.Println(sp.Split("a, b,c", -1))   // [a b c]
	fmt.Println(sp.Split("a, b,c", 2))    // [a b,c]
	fmt.Println(sp.Split("a, b,c", 0))    // []

	// 转义
	fmt.Println(regexp.QuoteMeta(`a.b*c(d)`))   // a\.b\*c\(d\)

	// ⚠️ 反向引用与环视都是编译期错误
	_, err := regexp.Compile(`(a)\1`)
	fmt.Println(err)   // error parsing regexp: invalid escape sequence: `\1`
}
```

模板里变量名同样取最长匹配：`$1x` 等价于 `${1x}` 而不是 `${1}x`，`$10` 是第 10 组而不是「第 1 组后面跟个 0」。越界或不存在的组名会被替换成空串，所以拼接时最好一律写 `${1}`、`${name}`。`ReplaceAllStringFunc` 拿不到捕获组，这是 Go API 的一个硬伤：要么把 `FindAllStringSubmatchIndex` 的结果配 `ExpandString` 自己拼，要么把函数写成先收整段再用子正则解析。切分的 `n` 语义容易记反——`0` 不是「不限制」而是返回 `nil`，要全切必须传负数；`Split` 不保留分隔符也不去空字段，连续分隔符会产出空串。`QuoteMeta` 是把用户输入锚成字面量的标准手段，等价于其他语言的 `re.escape`。

📘 [pkg.go.dev · regexp（ReplaceAllString / SubexpIndex / Split / QuoteMeta）](https://pkg.go.dev/regexp)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `re` 是回溯引擎，捕获组、反向引用、条件模式、原子组、占有量词一应俱全，但它把命名组的语法定成了独有的 `(?P<name>...)`，`(?<name>...)` 只会得到 `unknown extension` 错误，这是从别的语言搬过来时最常见的一次翻车。取值用 `Match.group()`/`groupdict()`/`expand()`，替换模板是 `\1`、`\g<name>`、`\g<0>`（注意是反斜杠不是 `$`），切分用 `re.split`，转义用 `re.escape`。

```python
import re

# 命名组：只有 (?P<name>...) 一种写法
m = re.match(r"(?P<y>\d{4})-(?P<m>\d{2})", "2026-09")
print(m.group("y"), m.group(1), m.groupdict())   # 2026 2026 {'y': '2026', 'm': '09'}
print(m.expand(r"\g<m>/\g<y>"))                   # 09/2026

# (?<name>...) 不是 Python 语法
try:
    re.compile(r"(?<y>\d)")
except re.error as e:
    print(e)                                      # unknown extension ?<y at position 1

# 替换模板：\1、\g<name>、\g<0>；\10 会被解析成第 10 组
print(re.sub(r"(\w+), (\w+)", r"\2 \1", "Doe, John"))       # John Doe
print(re.sub(r"(?P<last>\w+), (?P<first>\w+)", r"\g<first>_\g<last>", "Doe, John"))  # John_Doe
print(re.sub(r"\d+", r"[\g<0>]", "a1b22"))                   # a[1]b[22]
print(re.sub(r"(\d)", r"\g<1>0", "5"))                       # 50
try:
    re.sub(r"(\d)", r"\10", "5")
except re.error as e:
    print(e)                                      # invalid group reference 10 at position 1

# 函数替换 + count
print(re.sub(r"\w+", lambda x: x.group(0).upper(), "hi there"))   # HI THERE
print(re.sub(r"o", "0", "foo boo", count=1))                      # f0o boo

# split：带捕获组会保留分隔符，maxsplit 限制切分次数
print(re.split(r",\s*", "a, b,c"))            # ['a', 'b', 'c']
print(re.split(r"(\d)", "a1b2c"))             # ['a', '1', 'b', '2', 'c']
print(re.split(r",", "a,b,c", maxsplit=1))    # ['a', 'b,c']

# 转义
print(re.escape("a.b*c(d)"))                  # a\.b\*c\(d\)

# 反向引用、条件模式；原子组与占有量词自 3.11 起
print(re.findall(r"(\w)\1", "aabbc"))                        # ['a', 'b']
print(re.sub(r"(a)?b(?(1)c|d)", "X", "abc abd bd"))           # X aX X
print(re.findall(r"(?>a+)a", "aaaa"))                         # []
print(re.findall(r"a++a", "aaaa"))                            # []
```

替换字符串里 `\1` 后面紧跟数字会被读成更大的组号，`\10` 会被当成第 10 组并抛 `invalid group reference`，所以**永远优先写 `\g<1>`、`\g<name>`**，它们没有歧义；`\g<0>` 就是整段匹配。引用一个匹配失败的可选组得到的是空串，不会报错，这一点常被用来做「有就带上」的拼接。`re.split` 的行为值得单独记：模式里只要有捕获组，分隔符本身也会出现在结果里（这是保留分隔符的官方写法），而 `maxsplit` 是切分次数不是结果个数。Python 明确不支持的几件事：同名组（`(?P<n>a)(?P<n>b)` 报 redefinition）、分支重置 `(?|...)`、以及 `\p{...}` Unicode 属性（要装第三方 `regex` 模块）。`re.error` 在 3.13 起同时有别名 `re.PatternError`，捕获异常时写 `re.error` 仍然可用。

📘 [Python 3.14 · re — Regular expression operations](https://docs.python.org/3/library/re.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `Regex` 在 JVM 上直接包装 `java.util.regex`，所以命名组的写法与 Java 完全一致（`(?<name>...)` 与 `\k<name>`），另外在 JS 与 Native 后端有各自实现，官方明确提示这些后端的行为将来可能向 JVM 靠拢。Kotlin 的取值 API 很好用：`MatchResult` 有 `groupValues`、`groups`，还有 `destructured` 支持解构声明；替换既可以给 `$index`/`${name}` 模板，也可以传 `(MatchResult) -> CharSequence` 的 lambda；`Regex.escape` 转义模式（JVM 上直接委托 `Pattern.quote`，返回的是 `\Q...\E` 形式）、`Regex.escapeReplacement` 转义替换串（委托 `Matcher.quoteReplacement`）。

```kotlin
// 命名组 (?<name>...)：取值用 groups["name"]、groupValues 或 destructured
val date = "(?<day>\\d{2})-(?<month>\\d{2})-(?<year>\\d{4})".toRegex()
val m = date.find("on 15-09-2024")!!
println("${m.groups["day"]?.value} ${m.groupValues[1]} ${m.value}")
// 15 15 15-09-2024
val (d, mo, y) = date.find("15-09-2024")!!.destructured   // 解构前三个捕获组
println("$y-$mo-$d")                                       // 2024-09-15

// 字符串替换：$index 与 ${name} 会被代入，$0 是整段匹配
val text = "The events are on 15-09-2024 and 16-10-2024."
println(date.replace(text, "\${year}-\${month}-\${day}"))
// The events are on 2024-09-15 and 2024-10-16.
println(date.replace(text, "$3-$2-$1"))
// The events are on 2024-09-15 and 2024-10-16.

// 函数替换：拿到 MatchResult 自己算，返回什么就替换成什么
println(date.replace(text) { "${it.groups["year"]!!.value}/${it.groups["month"]!!.value}" })
// The events are on 2024/09 and 2024/10.

// 替换串里有字面 $ 时用 Regex.escapeReplacement 转义
println(Regex("b").replace("abc", Regex.escapeReplacement("$1")))   // a$1c

// 转义：Regex.escape 把字面串变成模式（JVM 上就是 Pattern.quote，故返回 \Q...\E）
println(Regex.escape("a.b*c(d)"))                                   // \Qa.b*c(d)\E

// 切分：limit 是结果片段数上限，分隔符不保留
println(Regex(",\\s*").split("a, b,c"))              // [a, b, c]
println(Regex(",\\s*").split("a, b,c", limit = 2))   // [a, b,c]
```

`Regex.replace(input, replacement)` 的模板规则和 Java 一致但有两处值得单独记：`$index` 的**第一个数字总属于组号**，后续数字只有在能构成合法组号时才并入（所以 `$12` 的解析依赖上下文，写 `${1}2` 最稳）；引用不存在的组或名字不会静默变成空串，而是抛异常——JVM 后端上编号越界抛 `IndexOutOfBoundsException`、名字不存在抛 `IllegalArgumentException`，二者都是 `RuntimeException` 的子类（Python 遇到不存在的组引用同样报错，Go、JS、.NET 则是静默给空串或原样保留），动态拼模板时要格外小心。替换串里出现用户数据时用 `Regex.escapeReplacement`（它专门转义 `$` 与 `\`），别拿 `Regex.escape` 顶替，后者是给模式用的；另外 `Regex.escape` 的输出形态依赖平台（JVM 给 `\Q...\E`，JS/Native 后端是各自实现），只把它当作「能按字面匹配的模式」使用、不要去解析它的返回值。`destructured` 最多解构 10 个组，组没参与匹配时拿到的是空串；需要区分「空匹配」与「没匹配」就直接读 `groups[i]?.value`（为 `null` 表示该组没参与匹配）。`Regex.split` 的 `limit` 是结果片段数上限而不是切分次数，分隔符一律丢弃。⚠️ 在 JS 与 Native 后端上，`Regex` 是另一套实现，正则语法与替换行为都可能和 JVM 有细微差别，跨平台代码不要假设完全一致。

📘 [Kotlin 2.4 · kotlin.text.Regex](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/-regex/)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `java.util.regex` 是传统 NFA 回溯引擎，命名组语法是 `(?<name>...)`（**不是** Python 的 `(?P<name>...)`），命名组同时也有编号，`Matcher.group("name")` 与 `Matcher.group(1)` 都能取值。替换走 `replaceAll` 家族：模板认 `$1` 与 `${name}`，字面 `$` 要写 `\$`；需要计算时用 Java 9 起的 `replaceAll(Function<MatchResult,String>)`；切分有 `Pattern.split`，Java 21 起还有能保留分隔符的 `splitWithDelimiters`。

```java
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Capture {
    public static void main(String[] args) {
        // 命名组只有 (?<name>...)：名字必须以字母开头，后面是字母或数字
        Pattern p = Pattern.compile("(?<y>\\d{4})-(?<m>\\d{2})");
        Matcher m = p.matcher("2026-09");
        if (m.find()) {
            System.out.println(m.group("y") + " " + m.group(2) + " " + m.group());
            // 2026 09 2026-09
        }
        System.out.println(p.namedGroups());                  // {y=1, m=2}

        // 替换模板：$1、${name}；字面 $ 写 \$（Java 没有 $&、$`、$'、$$）
        System.out.println("Doe, John".replaceAll("(?<last>\\w+), (?<first>\\w+)",
                "${first} ${last}"));                          // John Doe
        System.out.println("abc".replaceAll("b", "\\$"));      // a$c

        // 函数替换（Java 9+）：参数是 MatchResult
        System.out.println("hi there".replaceAll("\\w+", r -> r.group().toUpperCase()));
        // HI THERE

        // 替换串整体当作字面量：Matcher.quoteReplacement
        System.out.println("a.b".replaceAll("\\.", Matcher.quoteReplacement("$")));   // a$b

        // 切分：limit 0 丢弃尾部空串，负值全部保留；Java 21 起可保留分隔符
        System.out.println(Arrays.toString("a,b,".split(",")));       // [a, b]
        System.out.println(Arrays.toString("a,b,".split(",", -1)));   // [a, b, ]
        System.out.println(Arrays.toString(Pattern.compile(",").splitWithDelimiters("a,b", 0)));
        // [a, ,, b]

        // 转义：Pattern.quote 返回 \Q...\E
        System.out.println(Pattern.quote("a.b*c"));            // \Qa.b*c\E

        // 反向引用 \1 与 \k<name> 都可用；条件模式 (?(1)a|b) 明确不支持
        System.out.println("abab".matches("(ab)\\1"));         // true
        System.out.println("aa".matches("(?<x>a)\\k<x>"));     // true
    }
}
```

Java 的替换模板有个容易吃亏的地方：`$` 后面只接一位或两位数字，`$12` 会先尝试第 12 组，组不存在时行为并不友好，所以拼接时一律写 `${1}`、`${name}`。另一个反直觉点是 Java **不支持** `$&`、`` $` ``、`$'`、`$$` 这些 Perl/JS 风格的写法，要插入整段匹配得自己用 `Matcher.appendReplacement` 配 `group()`，或者在函数式替换里 `r.group()`；替换串里出现用户数据时用 `Matcher.quoteReplacement`，它会把 `$` 和 `\` 转义掉，比手工替换可靠。切分的 `limit` 语义要背下来：正数是片段数上限、`0` 丢弃尾部空串、负值全保留——`"a,b,".split(",")` 与 `"a,b,".split(",", -1)` 结果不同就是这么来的。此外 Java 明确不支持条件模式 `(?(1)a|b)`、`(?|...)` 分支重置、`\g<n>` 引用与 `(?#...)` 注释，但支持原子组 `(?>...)` 与占有量词 `a++`；`Pattern.namedGroups()` 可以把「名字 → 编号」映射一次取出，便于按编号二次处理。

📘 [Java SE 25 · Pattern](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Pattern.html) · [Matcher](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Matcher.html)

{{% /tab %}}

{{% tab header="C++" %}}

`std::regex` 默认使用 ECMAScript 语法、由回溯实现，它的短板在本节暴露得最明显：**没有命名捕获组**，写 `(?<name>...)` 会直接抛 `std::regex_error`；替换只有 `std::regex_replace` 加一套格式标志，回调替换要自己用 `regex_iterator` 拼；切分只能靠 `regex_token_iterator`。好的方面是反向引用 `\1` 与 ECMAScript 的 `$1`、`$&`、`` $` ``、`$'`、`$$` 都齐全，`format_sed` 与 `format_no_copy`、`format_first_only` 也提供了几种现成的替换模式。

```cpp
#include <iostream>
#include <regex>
#include <string>

int main() {
    std::string s = "2026-09-19";
    std::regex re(R"((\d{4})-(\d{2}))");
    std::smatch m;
    if (std::regex_search(s, m, re))
        std::cout << m[1] << " " << m[2] << " " << m[0] << "\n";   // 2026 09 2026-09

    // ECMAScript 替换格式：$1 $& $` $' $$
    std::cout << std::regex_replace(s, re, "$2/$1") << "\n";       // 09/2026-19
    std::cout << std::regex_replace(s, re, "[$&]") << "\n";        // [2026-09]-19
    std::cout << std::regex_replace(s, re, "$$") << "\n";          // $-19
    // sed 格式用 \1；format_no_copy 只留替换结果；format_first_only 只换第一处
    std::cout << std::regex_replace(s, re, R"(\2/\1)",
                                    std::regex_constants::format_sed) << "\n";        // 09/2026-19
    std::cout << std::regex_replace(s, re, "X",
                                    std::regex_constants::format_no_copy) << "\n";    // X
    std::cout << std::regex_replace(s, re, "X",
                                    std::regex_constants::format_first_only) << "\n"; // X-19

    // 命名组不是 ECMAScript 语法，构造 std::regex 就抛异常
    try { std::regex n(R"((?<y>\d{4}))"); }
    catch (const std::regex_error& e) { std::cout << "named: " << e.what() << "\n"; }
    // named: One of *?+{ was not preceded by a valid regular expression.

    // 反向引用在 ECMAScript 语法里可用
    std::cout << std::regex_search(std::string("aabb"), std::regex(R"((\w)\1)")) << "\n";  // 1

    // 切分：只有 regex_token_iterator，-1 表示取「不匹配的部分」
    std::regex sep(R"(,\s*)");
    std::string csv = "a, b,c";
    std::sregex_token_iterator it(csv.begin(), csv.end(), sep, -1), end;
    for (; it != end; ++it) std::cout << "[" << it->str() << "]";   // [a][b][c]
    std::cout << "\n";
}
```

替换格式细节值得留意：`$` 后面的组号越界时，libc++ 会替换成**空串**（`std::regex_replace("ab", std::regex("(a)"), "$2")` 得到 `"b"`），而 V8/Node 对同样越界的 `$2` 会原样保留字面 `$2`——跨引擎迁移模板时要重新验证，不要假设行为一致。`std::regex_replace` 没有「回调」概念，需要按捕获计算就必须用 `std::sregex_iterator` 自己遍历、把 `m[i].str()` 转换后再拼，这也是 `std::regex` 在生产代码里常被 RE2、Boost.Regex、CTRE 取代的原因之一（性能与 API 都更好）。切分用 `regex_token_iterator` 时最后一个参数是「要取哪些子匹配」：`-1` 取未匹配片段（等价于 split）、`0` 取整段匹配（等价于保留分隔符）、也可以传 `{1, 2}` 这样的下标列表取特定捕获组，一物多用但可读性差。⚠️ `std::regex` 没有标准的转义函数，把用户输入当字面量时要自己遍历加反斜杠，或者改用第三方库提供的 `escape`。

📘 [cppreference · std::regex_replace](https://en.cppreference.com/w/cpp/regex/regex_replace)

{{% /tab %}}

{{% tab header="C" %}}

C 标准库没有正则表达式，`<regex.h>` 是 POSIX 接口：`regcomp`、`regexec`、`regerror`、`regfree` 四个函数，匹配结果是一组 `regmatch_t` 偏移量。它没有命名组、没有替换 API、没有切分 API、没有转义函数，`\d`/`\w` 这类简写也不存在（要用 `[0-9]`、`[[:alpha:]]`），所以本节里 C 能演示的只有「用偏移量手工取值」和「自己拼替换」。

```c
#include <regex.h>
#include <stdio.h>

int main(void) {
    regex_t re;
    regmatch_t pm[3];
    const char *s = "2026-09-19";

    /* ERE：没有命名组，只有编号捕获，取值靠 rm_so/rm_eo 偏移量 */
    regcomp(&re, "([0-9]{4})-([0-9]{2})", REG_EXTENDED);
    if (regexec(&re, s, 3, pm, 0) == 0) {
        printf("%.*s | %.*s | %.*s\n",
               (int)(pm[0].rm_eo - pm[0].rm_so), s + pm[0].rm_so,
               (int)(pm[1].rm_eo - pm[1].rm_so), s + pm[1].rm_so,
               (int)(pm[2].rm_eo - pm[2].rm_so), s + pm[2].rm_so);
    }
    /* 2026-09 | 2026 | 09 */
    regfree(&re);

    /* 没有替换 API：只能拿偏移量当切点自己拼 */
    regcomp(&re, "-", REG_EXTENDED);
    regexec(&re, s, 1, pm, 0);
    printf("%.*s\n", (int)pm[0].rm_so, s);          /* 2026（第一个 '-' 之前的片段） */
    regfree(&re);

    /* 反向引用只在 BRE 里有定义；ERE 里的 \1 属未定义行为 */
    regcomp(&re, "\\(a\\)\\1", 0);                  /* 默认就是 BRE */
    printf("%d\n", regexec(&re, "aa", 0, NULL, 0) == 0);   /* 1 */
    regfree(&re);

    /* 没有转义函数；regerror 只把错误码翻成英文 */
    regex_t bad;
    int rc = regcomp(&bad, "([0-9", REG_EXTENDED);
    char buf[128];
    regerror(rc, &bad, buf, sizeof buf);
    printf("%s\n", buf);    /* brackets ([ ]) not balanced */
    return 0;
}
```

POSIX 的捕获值一律用 `regmatch_t` 的 `rm_so`/`rm_eo` 表示，未参与匹配的组两个字段都是 `-1`，取值时先判 `rm_so != -1` 再用 `%.*s` 加偏移量打印（`pm[0]` 是整段匹配，编号从 1 开始才是捕获组）。要在 C 里做替换，标准做法是遍历所有匹配、把「匹配之间的原文」与「替换文本」依次写进目标缓冲区：`regexec` 支持 `REG_NOTBOL` 之类的标志做续扫，但「上一次匹配结束位置」得自己维护，这也是为什么 C 项目里通常直接引 PCRE2 或 RE2，而不是硬写 POSIX 版本。`REG_EXTENDED` 决定 ERE 还是 BRE：ERE 支持 `+`、`?`、`|`、`()`，BRE 要写 `\+`、`\?`、`\|`、`\(`；POSIX 只在 BRE 里定义反向引用，所以上面例子用 BRE 演示 `\1`。⚠️ 想按字面量匹配用户输入在 C 里没有现成函数，必须自己把 `. ^ $ * + ? ( ) [ ] { } | \` 这些字符逐个加反斜杠，且注意 BRE 与 ERE 的元字符集合不同。

📘 [POSIX · regcomp / regexec](https://pubs.opengroup.org/onlinepubs/9699919799/functions/regcomp.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Regex` 底层是 PCRE2，套了一层很「Julia」的语法糖：模式字面量 `r"..."`，替换用专门的 `s"..."`（类型是 `SubstitutionString`），匹配结果是 `RegexMatch`，可以按名字 `m[:name]`、按下标 `m[1]`、甚至按捕获组顺序解构成元组。取值 API 是本节里最丰富的：`m.match`、`m.captures`、`m.offsets`、`keys(m)`、`Tuple(m)`、`NamedTuple(m)`、`Dict(m)` 想用哪个用哪个。

```julia
# 命名组 (?<name>...)：RegexMatch 既能按名字也能按下标取值
m = match(r"(?<hour>\d+):(?<minute>\d+)(am|pm)?", "11:30 in the morning")
m.match                      # "11:30"
m.captures                   # ["11", "30", nothing]  ← 没参与匹配的组是 nothing
m["minute"]                  # "30"
keys(m)                      # ["hour", "minute", 3]  ← 名字与下标混在一起
hr, min, ampm = m            # 按捕获组顺序解构；NamedTuple(m)/Dict(m) 需要 1.11 起
hr                           # "11"

# 替换：s"..." 里 \1 是编号组，\g<name> 是命名组
replace("#Hello# from Julia", r"#(.+)# from (?<from>\w+)" => s"FROM: \g<from>; MESSAGE: \1")
# "FROM: Julia; MESSAGE: Hello"
replace("a-b-c", r"-" => "+"; count = 1)   # "a+b-c"  ← count 限制替换次数

# 切分：split 收正则，分隔符不保留
split("a, b,c", r",\s*")      # ["a", "b", "c"]

# 转义：没有 re.escape 式函数，用 PCRE2 的 \Q...\E 把插值包起来
x = "a.b*c"
occursin(Regex("\\Q$x\\E"), x)     # true
```

`m.captures` 对未参与匹配的可选组给 `nothing`（不是空串），这正是区分「匹配了空串」与「压根没匹配」的手段；而 `m[:name]` 在组没匹配时同样给 `nothing`，直接拿去拼字符串会得到 `"nothing"` 或报错，稳妥写法是 `something(m[:name], "")`。`s"..."` 是 `SubstitutionString` 字面量：`\1`–`\9` 是编号组，`\g<name>` 是命名组，注意它不会做变量插值，要拼动态内容得先构造字符串再转 `SubstitutionString`。Julia 没有内置的正则转义函数，官方给的做法是 `\Q...\E`：把要当字面量的部分包在 `Regex("\\Q$var\\E")` 里（`r"..."` 字面量不插值，这条路只能走 `Regex(str)`）。切分的 `split(str, regex)` 会丢弃分隔符、保留中间的空字段，`split(str, regex; keepempty=false)` 可以压掉空字段。⚠️ 匹配失败时 `match` 返回 `nothing`，而 `m.captures`/`m[i]` 在组未参与匹配时给 `nothing`，这两种 `nothing` 含义不同，代码里别混。

📘 [Julia 1.13 · Strings（Regex / RegexMatch / SubstitutionString）](https://docs.julialang.org/en/v1/base/strings/)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的 `System.Text.RegularExpressions` 是回溯引擎，命名组支持 `(?<name>...)` 与 `(?'name'...)` 两种写法，取值用 `Match.Groups["name"]` 或 `Groups[1].Value`，命名组同时也有编号。它最大的优点是替换模板最全：`$1`、`${name}`、`$$`、`$&`、`` $` ``、`$'`、`$+`、`$_` 一应俱全；需要计算时用 `Regex.Replace` 的 `MatchEvaluator` 重载；切分用 `Regex.Split`（会把捕获组也放进结果）；转义用 `Regex.Escape`。

```csharp
using System;
using System.Text.RegularExpressions;

class CaptureDemo {
    static void Main() {
        // 命名组两种写法都行；Groups 既能按名字也能按下标取
        var re = new Regex(@"(?<y>\d{4})-(?'m'\d{2})");
        var m = re.Match("2026-09");
        var gy = m.Groups["y"].Value;         // 按名字取
        var gm = m.Groups["m"].Value;
        Console.WriteLine($"{gy} {gm} {m.Groups[2].Value}");   // 2026 09 09

        // 替换模板：$1、${name}、$$、$&、$`、$'、$+、$_
        Console.WriteLine(Regex.Replace("Doe, John", @"(?<last>\w+), (?<first>\w+)",
                                        "${first} ${last}"));                 // John Doe
        Console.WriteLine(Regex.Replace("abc", "b", "[$&]"));                 // a[b]c
        Console.WriteLine(Regex.Replace("abc", "b", "[$`]"));                 // a[a]c
        Console.WriteLine(Regex.Replace("abc", "b", "[$']"));                 // a[c]c
        Console.WriteLine(Regex.Replace("abc", "b", "$$"));                   // a$c
        Console.WriteLine(Regex.Replace("The the dog jumped over the fence fence.",
                          @"\b(\w+)\s\1\b", "$+", RegexOptions.IgnoreCase));
        // The dog jumped over the fence.

        // MatchEvaluator：拿 Match 自己算，返回值就是替换文本
        Console.WriteLine(Regex.Replace("hi there", @"\w+",
                          mm => mm.Value.ToUpperInvariant()));                // HI THERE

        // 切分：捕获组会留在结果数组里
        Console.WriteLine(string.Join("|", Regex.Split("a1b2c", @"(\d)")));
        // a|1|b|2|c

        // 转义与反向引用
        Console.WriteLine(Regex.Escape("a.b*c(d)"));                          // a\.b\*c\(d\)
        Console.WriteLine(Regex.IsMatch("aa", @"(?<x>a)\k<x>"));              // True
    }
}
```

上面 `$+` 那行是这套模板里最容易记混的一个：`$+` 是「最后一个被捕获的组」，`$_` 是「整段输入」，而 `$&` 是「整段匹配」，三者不是一回事，用之前建议先拿最小样例验一遍。⚠️ .NET 对不存在的组号或名字**不报错**，而是把 `$99`、`${ghost}` 原样当字面文本输出，所以模板拼错时往往没有异常、只有产物不对。`Regex.Split` 把捕获括号里的内容也当作结果元素返回，这一点和 Python 的 `re.split`、Ruby 的 `split` 一致，但与 Java、Go 的 `split` 默认行为不同，想切干净就不要在模式里加捕获组（或用 `(?:...)`）。要在替换里做大小写转换，.NET 没有内置的 `\U`/`\L`，只能用 `MatchEvaluator` 或 `$&` 加后处理。关于版本行为：官方 .NET 10 破坏性变更清单里**没有**正则相关条目，但社区报告（dotnet/runtime#125321，已关闭为重复）指出 `a(b.*?c)?d` 在 `"abccd"` 上 .NET 9 能匹配、.NET 10 不能，根因是「可选组里的懒惰量词」的回溯行为变化——如果你依赖可选组捕获，升级到 .NET 10 时值得补一条回归用例。追求可预测性时可以考虑 `RegexOptions.NonBacktracking`（.NET 7 起），代价是不支持反向引用与环视。

📘 [.NET · Substitutions in Regular Expressions](https://learn.microsoft.com/en-us/dotnet/standard/base-types/substitutions-in-regular-expressions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `RegExp` 是自研引擎（源自 V8 的 Irregexp），语法与语义都照 ECMAScript 规范走，因此命名组是 `(?<name>...)`，`unicode` 标志决定按 UTF-16 码元还是码点匹配。最需要注意的是替换：Dart 的 `String.replaceAll` 参数是普通字符串，**不做** `$1` 模板展开，要引用捕获必须用 `replaceAllMapped`/`replaceFirstMapped` 传回调；取值用 `RegExpMatch.namedGroup` 与 `groupNames`，转义用 `RegExp.escape`。

```dart
void main() {
  // 命名组 (?<name>...)：按名字取值用 namedGroup，也能按下标
  final re = RegExp(r'(?<y>\d{4})-(?<m>\d{2})');
  final m = re.firstMatch('2026-09')!;
  final yy = m.namedGroup('y');      // 按名字取
  final mm = m.namedGroup('m');
  print('$yy $mm ${m[1]} ${m[2]}');  // 2026 09 2026 09
  print(m.groupNames.toList());      // [y, m]

  // 替换：replaceAll 收字符串时不会展开 $1，要引用捕获必须用 Mapped 回调
  print('Doe, John'.replaceAll(RegExp(r'(?<last>\w+), (?<first>\w+)'), r'$2 $1'));
  // $2 $1
  print('Doe, John'.replaceAllMapped(
      RegExp(r'(?<last>\w+), (?<first>\w+)'),
      (Match hit) {
        final first = hit.namedGroup('first');
        final last = hit.namedGroup('last');
        return '$first $last';
      }));
  // John Doe
  print('hi there'.replaceAllMapped(RegExp(r'\w+'), (Match mm) => mm[0]!.toUpperCase()));
  // HI THERE

  // 切分：split 收 Pattern，分隔符不保留，连续分隔符产生空字段
  print('a, b,c'.split(RegExp(r',\s*')));    // [a, b, c]
  print('a1b2c'.split(RegExp(r'\d')));       // [a, b, c]
  print('a,,b'.split(','));                  // [a, , b]

  // 转义：RegExp.escape 返回可以当字面量用的模式
  print(RegExp.escape('a.b*c(d)'));
  print(RegExp(r'a\.b\*c\(d\)').hasMatch('a.b*c(d)'));   // true

  // 反向引用可用；条件模式 (?(1)a|b) 与分支重置 (?|...) 都不是 ECMAScript 语法
  print(RegExp(r'(\w)\1').hasMatch('aabb'));             // true
}
```

Dart 把「替换模板」这一层完全交给回调，好处是没有 `$1` 与 Dart 字符串插值 `$name` 互相打架的问题，坏处是简单替换也得写个闭包；`replaceAllMapped` 的闭包参数只有 `Match`，没有其他语言那种 `p1, p2, offset` 平铺参数，所以要多取几组就在闭包里用 `namedGroup` 或 `mm[i]`。`groupNames` 只列出命名组（顺序按模式里出现的次序），`Match.groupCount` 才是捕获组总数，两者不等价。切分只支持 `String.split(Pattern)`，分隔符一律不保留也没有 limit 参数，需要保留分隔符就得用 `allMatches` 自己沿偏移量切。`RegExp.escape` 是 Dart 内置的字面量转义入口（自 Dart 2.0 起就有），不要自己用 `replaceAll` 拼反斜杠来替代——手写版本在 `/`、`-`、换行、孤立代理项这些边角上几乎必错。⚠️ Dart 编译到 Web 时正则由浏览器引擎执行，语法支持面可能比 VM 窄（`unicode` 标志、部分转义在旧浏览器上会有差异），跨端代码要实测。

📘 [Dart 3.13 · RegExp](https://api.dart.dev/stable/latest/dart-core/RegExp-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的字符串函数默认用 TRE 实现的 POSIX ERE（外加一些扩展），加 `perl = TRUE` 才切到 PCRE2；这是本节里「一个开关切换两套引擎」最典型的例子，`\d`、`\w`、非贪婪、环视、命名组都只在 PCRE2 模式下才有。替换用 `sub`（第一处）与 `gsub`（全部），replacement 里的 `\1`–`\9` 是反向引用，`perl = TRUE` 时还能用 `\U`/`\L`/`\E` 做大小写转换；切分用 `strsplit`；要按字面量匹配就加 `fixed = TRUE`，或者在 PCRE 模式下用 `\Q...\E`。

```r
# 替换：sub 只换第一处，gsub 换所有；replacement 里的 \1-\9 是反向引用
sub("([a-z]+) ([a-z]+)", "\\2 \\1", "john doe")          # "doe john"
gsub("([ab])", "\\1_\\1_", "abc")                        # "a_a_b_b_c"

# perl = TRUE 才有 \U \L \E 大小写控制（PCRE2 专属）
gsub("(\\w)(\\w*)", "\\U\\1\\L\\2", "a test", perl = TRUE)   # "A Test"

# 命名组只在 perl = TRUE 下可用，取值走 regexpr/gregexpr 的属性
name.rex <- "(?<first>[[:upper:]][[:lower:]]+) (?<last>[[:upper:]][[:lower:]]+)"
r <- regexpr(name.rex, "Ben Franklin", perl = TRUE)
attr(r, "capture.names")            # "first" "last"
attr(r, "capture.start")            # 两个组的起始位置
regmatches("Ben Franklin", r)[[1]]  # "Ben Franklin"

# 切分：尾部空字段被丢掉，分隔符永远不保留；fixed=TRUE 才是字面量
strsplit("a, b,c", ",\\s*")[[1]]                  # "a" "b" "c"
strsplit("a,b,", ",")[[1]]                        # "a" "b"
strsplit("", " ")[[1]]                            # character(0)
strsplit("a.b.c", ".", fixed = TRUE)[[1]]         # "a" "b" "c"
strsplit("a.b.c", ".")[[1]]                       # "" "" "" "" ""（"." 是任意字符）

# 转义：没有 escape 函数，用 fixed=TRUE 或 \Q...\E
grep("a.b", c("a.b", "axb"), fixed = TRUE)        # 1
grep("\\Qa.b\\E", c("a.b", "axb"), perl = TRUE)   # 1
```

`sub`/`gsub` 的 replacement 里反斜杠必须写双份（`"\\1"`），因为 R 字符串字面量自己会先吃一层转义；只要 replacement 里出现 `\1` 这种引用，R 就会把它当组引用而不是字面文本，想输出字面反斜杠要写 `"\\\\"`。命名组这条线要特别注意：官方明确写了「named backreferences are not supported by `sub`」，也就是说 `gsub` 的 replacement 里没有 `\k<name>` 可用，命名组只能通过 `regexpr`/`gregexpr`/`regexec` 返回的 `capture.start`、`capture.length`、`capture.names` 属性手工取子串（或改用编号反向引用）。`strsplit` 的切分算法是「从左往右找到匹配就切一刀」，因此**开头**匹配会产出一个空字段，**结尾**匹配不会产出空字段，`strsplit("a,b,", ",")` 只有两个元素；此外 `perl = TRUE` 与 `fixed = TRUE` 可以共存，但 `fixed` 优先。⚠️ 默认 POSIX 模式下 `\d`、`\w` 是 TRE 的扩展而非标准 POSIX，跨平台移植到别的 ERE 实现时不要依赖。

📘 [R 4.6 · Regular Expressions as used in R](https://stat.ethz.ch/R-manual/R-devel/library/base/html/regex.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 标准库**没有正则表达式**：`std` 里没有 regex 模块，只有 `std.mem` 系列的字面量查找与切分（`splitScalar`/`splitSequence`、`tokenizeScalar`/`tokenizeSequence`、`indexOf`、`indexOfScalar`、`eql`、`trim`）。因此「捕获组、替换模板、转义函数」这三件事在 Zig 里都没有语言级答案：要正则就得引第三方库，或者用 `@cImport` 接 POSIX `<regex.h>`、PCRE2；纯字面量需求则直接用 `std.mem`，反而比正则更快更清楚。

```zig
const std = @import("std");

pub fn main() !void {
    const text = "a, b,c";

    // 切分：std.mem 按字面分隔符切，没有「捕获组」这个概念
    var it = std.mem.splitScalar(u8, text, ',');
    var parts: usize = 0;
    while (it.next()) |part| {
        std.debug.print("[{s}]", .{std.mem.trim(u8, part, " ")});
        parts += 1;
    }
    std.debug.print(" parts={d}\n", .{parts});
    // [a][b][c] parts=3

    // tokenizeScalar 会跳过连续分隔符产生的空片段
    var ti = std.mem.tokenizeScalar(u8, ",a,,b,", ',');
    var tokens: usize = 0;
    while (ti.next()) |_| tokens += 1;
    std.debug.print("tokens={d}\n", .{tokens});          // tokens=2

    // 查找与比较都是字面量语义，不需要任何转义
    const i = std.mem.indexOfScalar(u8, text, ',').?;
    std.debug.print("first-comma={d}\n", .{i});          // first-comma=1
    std.debug.print("lit={}\n", .{std.mem.eql(u8, "a.b", "a.b")});   // lit=true

    // 没有「把字面量转义成模式」的函数，因为没有模式这层概念
    // 需要正则时的常规做法：@cImport("regex.h") 或引第三方库
}
```

`splitScalar` 与 `tokenizeScalar` 的差别恰好对应其他语言里 `split` 的两种流派：前者保留连续分隔符产生的空片段（`"a,,b"` 切出三段，中间是空串），后者像「按空白分词」一样跳过空片段；按子串切分则换成 `splitSequence` 与 `tokenizeSequence`，命名规则是「分隔符种类的后缀」而不是重载。Zig 的 `std.mem` 全部是字面量语义，所以本节讨论的 `re.escape`、`QuoteMeta`、`preg_quote` 在 Zig 里没有对应物——这也意味着用户输入可以直接交给 `indexOf`/`eql`，不存在「拼模式时被注入」的问题。⚠️ 用 `@cImport` 接 `<regex.h>` 时，`regmatch_t` 里的偏移量是字节偏移，Zig 侧再切 `[]u8` 时要自己做边界检查；`regexec` 也不会分配内存，输出缓冲全部由调用者准备，这是 Zig 里用 C 正则最容易写错的地方。

📘 [Zig · std.mem](https://ziglang.org/documentation/master/std/#std.mem)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的 `string.find`/`match`/`gmatch`/`gsub` 用的是 Lua pattern，不是正则表达式：没有 `|` 交替、没有环视、没有非捕获组与命名组，元字符表也只有 `^ $ ( ) % . [ ] * + - ?` 这 12 个（口径：Lua 5.5 手册列出的 magic characters，即 `^$()%.[]*+-?`）；不过它有编号反向引用 `%1`–`%9`，以及正则里没有的 `%b`（配对）与 `%f`（边界）。`gsub` 的替换串用 `%1`–`%9` 与 `%0` 引用捕获、`%%` 表示字面百分号，替换还可以直接给函数或表；Lua 没有 `split` 函数，切分靠 `gmatch` 或 `string.find` 手动做。

```lua
-- 捕获用 ()：取值靠 string.match 的多返回值
local y, m = string.match("2026-09", "(%d%d%d%d)-(%d%d)")
print(y, m)                                   -- 2026	09

-- gsub 替换串：%0 是整段，%1-%9 是捕获，%% 才是字面 %
print(string.gsub("Doe, John", "(%w+), (%w+)", "%2 %1"))   -- John Doe	1
print(string.gsub("abc", "b", "[%0]"))                     -- a[b]c	1

-- 替换也可以是函数（捕获按顺序作实参）或表（用第 1 个捕获当键）
print(string.gsub("hi there", "%w+", string.upper))        -- HI THERE	2
print(string.gsub("$name is $age", "%$(%w+)", { name = "Ada", age = "36" }))
-- Ada is 36	2

-- Lua pattern 独有：%b 配对、%f 边界
print(string.match("(nested (x))", "%b()"))                -- (nested (x))
print(string.gsub("the cat", "%f[%a]cat", "dog"))          -- the dog	1

-- 编号反向引用：%1 引用第 1 个捕获
print(string.match("abcabc", "(abc)%1"))                   -- abc

-- 没有 split：用 gmatch 按非分隔符切
local parts = {}
for p in string.gmatch("a, b,c", "[^,]+") do parts[#parts + 1] = p end
print(table.concat(parts, "|"))                            -- a| b|c
```

`gsub` 的返回值是「新字符串 + 替换次数」两个值，所以 `print` 出来总带一个计数，只想取结果就写 `local s = string.gsub(...)`。替换若用函数或表，返回 `nil` 或 `false` 表示**不替换**（原文保留），这个特性常被用来做条件替换：例如表里查不到就原样留下。`%bxy` 与 `%f[set]` 是 Lua pattern 的独家能力：前者匹配配对括号之类的嵌套结构（`%b()` 能吃掉任意深的括号），后者匹配「前一个字符不在集合内、后一个字符在集合内」的零宽边界，用来做「按单词边界匹配」很顺手。⚠️ 三个最容易踩的坑：`-` 才是非贪婪（`.*` 贪婪、`.-` 最短），字符类里 `%` 是转义符（匹配字面百分号写 `%%`），以及 pattern 里没有交替能力，`a|b` 只会匹配字面的竖线——需要交替时得写成 `[ab]` 或用 `string.find` 循环试多个模式。Lua pattern 也没有环视与命名组，这两件事只能靠多次 `string.find` 组合实现。

📘 [Lua 5.5 · Patterns 与 string.gsub](https://www.lua.org/manual/5.5/manual.html#6.4.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有自己的正则实现，`RegExp` 就是 JavaScript 那个，TypeScript 做的只是给捕获组、替换回调与 `indices` 补类型：`m.groups` 的类型是 `Record<string, string> | undefined`，`replace` 的回调签名是 `(substring: string, ...args: any[]) => string`，`RegExp.escape`（ES2025）与 `d` 标志带来的 `indices`（ES2022）只有在 `tsconfig.json` 的 `lib` 包含对应标准库时才认识。所以本节的语法与 JavaScript 完全一致，差别只在「编译器会不会替你拦住错误」：命名组写错名字、`groups` 忘记判空，在 TypeScript 里能编译期发现一部分。

```typescript
// RegExp 就是 JS 的；命名组会反映到 groups 的类型上
const re = /(?<y>\d{4})-(?<m>\d{2})/;
const m = re.exec("2026-09")!;
const y: string | undefined = m.groups?.y;      // string | undefined，必须判空
console.log(m[1], y);                            // 2026 2026

// 替换模板：$1 $<name>、$& $` $' $$
console.log("Doe, John".replace(/(\w+), (\w+)/, "$2 $1"));                    // John Doe
console.log("Doe, John".replace(/(?<last>\w+), (?<first>\w+)/, "$<first> $<last>"));
// John Doe
console.log("abc".replace(/b/, "[$&][$`][$']"));   // a[b][a][c]c

// 回调替换：TypeScript 把参数标成 (substring, ...args)
console.log("hi there".replace(/\w+/g, (s: string) => s.toUpperCase()));      // HI THERE

// split：捕获组会留在结果里
console.log("a1b2c".split(/(\d)/));      // ['a', '1', 'b', '2', 'c']

// ES2025 的 RegExp.escape 与 ES2022 的 d 标志（类型取决于 tsconfig 的 lib）
console.log(RegExp.escape("a.b"));       // \x61\.b
const ind = /(?<y>\d{4})/d.exec("x2026")!;
console.log(ind.indices?.groups?.y);     // [1, 5]

// 反向引用可用；条件模式与分支重置都不是 JS 语法
console.log(/(\w)\1/.test("aabb"));      // true
```

TypeScript 里最实用的类型细节有两条：一是 `m.groups` 可能为 `undefined`（模式里没有命名组，或者匹配失败后 `exec` 返回 `null`），所以 `m.groups?.y` 与 `?? ""` 这类处理几乎躲不掉；二是 `String.prototype.replace` 的回调在标准库里被标成 `(substring: string, ...args: any[]) => string`，捕获组参数没有逐个的类型信息，想强类型就得自己包一层断言，或者写一个显式的包装函数。⚠️ `RegExp.escape` 是 ES2025 才进标准的方法，`d` 标志是 ES2022、`v`（unicodeSets）标志是 ES2024：`tsconfig.json` 里的 `lib` 或 `target` 太旧时，`RegExp.escape` 会报「属性不存在」，`indices` 也取不到类型，这时要么把 `lib` 提上去，要么在 `d.ts` 里自己补声明。运行时另说：Node 26 与主流浏览器都已实现这三者，但老环境的 `RegExp.escape` 缺失只能在运行时兜底。

📘 [TypeScript · tsconfig 的 lib 选项](https://www.typescriptlang.org/tsconfig/lib.html) · [MDN · RegExp.escape()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `RegExp` 是 ECMAScript 规范定义的回溯引擎，命名组 `(?<name>...)` 从 ES2018 起可用，捕获对象挂在 `exec` 结果的 `groups` 属性上；替换模板认 `$1`、`$<name>`、`$&`、`` $` ``、`$'`、`$$` 六种形式，需要计算时传回调。`split` 会用捕获组保留分隔符，`replaceAll` 与 ES2025 的 `RegExp.escape` 补齐了日常最常用的两块。

```javascript
// 命名组 (?<name>...)：取值走 groups 对象
const re = /(?<y>\d{4})-(?<m>\d{2})/;
const m = re.exec("2026-09");
console.log(m.groups.y, m[1], m.index);        // 2026 2026 0
console.log(/(?<y>\d{4})/d.exec("x2026").indices.groups.y);   // [ 1, 5 ]

// 替换模板：$1 $<name> $& $` $' $$
console.log("Doe, John".replace(/(\w+), (\w+)/, "$2 $1"));    // John Doe
console.log("abc".replace(/b/, "[$&]"));       // a[b]c
console.log("abc".replace(/b/, "[$`]"));       // a[a]c
console.log("abc".replace(/b/, "[$']"));       // a[c]c
console.log("abc".replace(/b/, "$$"));         // a$c
console.log("ab".replace(/(a)/, "$2"));        // $2b ← 组号越界时原样保留

// 回调替换：参数是 (match, p1, p2, offset, string)
console.log("hi there".replace(/\w+/g, (s) => s.toUpperCase()));   // HI THERE

// split：捕获组保留、limit 截断
console.log("a, b,c".split(/,\s*/));           // [ 'a', 'b', 'c' ]
console.log("a1b2c".split(/(\d)/));            // [ 'a', '1', 'b', '2', 'c' ]
console.log("a,b,c".split(/,/, 2));            // [ 'a', 'b' ]

// 全局替换要带 g；replaceAll 要求模式必须全局
console.log("a-b-c".replaceAll("-", "+"));     // a+b+c
try { "a-b".replaceAll(/-/, "+"); } catch (e) { console.log(e.constructor.name); }
// TypeError

// 转义（ES2025）：首字符是字母数字时会被转成 \xNN，避免粘到前一个转义序列上
console.log(RegExp.escape("a.b*c(d)"));        // \x61\.b\*c\(d\)
console.log(RegExp.escape("1a"));              // \x31a

// 反向引用可用；条件模式与分支重置不是 JS 语法
console.log(/(\w)\1/.test("aabb"));            // true
```

替换模板有两处必须记牢：`$n` 的组号**越界**时，V8/Node 会把 `$2` 原样留着（上面的 `"ab".replace(/(a)/, "$2")` 得到 `"$2b"`），而 `$<name>` 只在「模式里有命名组、但名字写错」时替换成空串（`"ab".replace(/(?<x>a)/, "$<ghost>")` 得到 `"b"`），模式里完全没有命名组时整个 `$<ghost>` 会原样保留——两组规则并不对称；同时 `$&`、`` $` ``、`$'` 会把整段匹配、匹配前的全文、匹配后的全文插进结果，`"abc".replace(/b/, "[$`][$']")` 会得到 `"a[a][c]c"`，用在多匹配场景下输出会迅速膨胀（每次替换都复制整段输入），这是别名替换最常见的性能陷阱。`split` 的捕获组保留特性常被拿来顺手取分隔符，但要注意 `limit` 是**结果数组长度上限**，超出部分被丢弃而不是合并到最后一项（与 Java 的正数 limit 语义相反）。`replaceAll` 的第一个参数如果是正则，必须带 `g` 标志，否则抛 `TypeError`；传字符串则总是全替换。`RegExp.escape` 只负责「把字符串变成安全字面量」，不会给你加锚点或分组，把它拼进更大的模式时才需要留意首字符被写成 `\xNN` 的形式（这是规范要求，用来防止它紧跟在 `\1`、`\u00` 之类的转义后面被误解析）。

📘 [MDN · String.prototype.replace()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `preg_*` 系列基于 PCRE2，因此命名组三种写法 `(?P<name>...)`、`(?<name>...)`、`(?'name'...)` 与反向引用 `\k<name>`、条件模式 `(?(1)a|b)`、原子组、分支重置都原生可用；取值就是 `$matches['name']` 或 `$matches[1]`。替换这一环 PHP 比较特别：`preg_replace` 的 replacement 只认数字引用 `\0`–`\99` 与 `$0`–`$99`，要按名字引用捕获必须改用 `preg_replace_callback`；切分用 `preg_split`，三个 flag 分别控制保留分隔符、去空字段与带偏移量。

```php
<?php
// 命名组三种写法 PCRE2 都认，取值用 $matches['name']
preg_match('/(?<y>\d{4})-(?P<m>\d{2})/', '2026-09', $m);
echo $m['y'], ' ', $m['m'], ' ', $m[1], "\n";        // 2026 09 2026

// 替换模板只有数字引用：\0-\99 或 $0-$99；\11 有歧义，用 ${1}1 断开
echo preg_replace('/(\w+) (\d+)/', '${1}1-$2', 'April 15'), "\n";   // April1-15
echo preg_replace('/(\d)/', '\1\1', '12'), "\n";                    // 1122
echo preg_replace('/(b)/', '\0\0', 'abc'), "\n";                    // abbc

// 要按名字引用捕获只能走回调（PHP 8 的箭头函数最省事）
echo preg_replace_callback('/(?<last>\w+), (?<first>\w+)/',
    fn(array $mm) => strtoupper($mm['first']) . ' ' . $mm['last'],
    'Doe, John'), "\n";                                             // JOHN Doe

// preg_split：保留分隔符捕获、去空字段、带偏移量
print_r(preg_split('/,\s*/', 'a, b,c'));                            // [a, b, c]
print_r(preg_split('/(\d)/', 'a1b2c', -1, PREG_SPLIT_DELIM_CAPTURE));
// [a, 1, b, 2, c]
print_r(preg_split('/,/', ',a,,b', -1, PREG_SPLIT_NO_EMPTY));       // [a, b]
print_r(preg_split('/,/', 'a,b', -1, PREG_SPLIT_OFFSET_CAPTURE));
// [[a,0],[b,2]]

// 转义：preg_quote，第二个参数会连同自定义分隔符一起转义
echo preg_quote('a.b*c(d)', '/'), "\n";              // a\.b\*c\(d\)

// 反向引用与条件模式都是 PCRE2 原生支持
echo preg_match('/(\w)\1/', 'aabb'), "\n";           // 1
echo preg_replace('/(a)?b(?(1)c|d)/', 'X', 'abc abd bd'), "\n";     // X aX X
```

`preg_replace` 的 `\n`/`$n` 引用最大的坑是「紧跟数字」：`\11` 会被理解成第 11 组而不是「第 1 组后面跟个 1」，官方给的解法是写 `${1}1`；同理 `$1` 后面直接跟数字也不安全。另一个必须知道的事实是 replacement 里**没有**命名组引用（官方文档只列数字形式，用户注释与 bug #81469 也都报告 `\g<name>`、`$name` 在 replacement 里不生效），所以「按名字替换」这条路的正解就是 `preg_replace_callback`，PHP 8 的箭头函数让它只多一行。`preg_split` 的 flag 组合有几个反直觉点：用 `PREG_SPLIT_DELIM_CAPTURE` 时**必须**在模式里写捕获括号，否则分隔符不会被返回；`PREG_SPLIT_NO_EMPTY` 只丢弃空片段，对空输入串返回的是空数组；流传很广的「加了 NO_EMPTY 仍返回一个空元素」的例子其实把 flag 当成了 `limit` 传（`PREG_SPLIT_NO_EMPTY` 的常量值是 1），属于参数错位而不是该 flag 的行为；`limit` 与 flag 是不同参数，只想用 flag 时必须显式传 `-1` 或 `0`，否则常量会被当成 limit。`preg_quote` 的第二个参数用于把分隔符本身也转义，用 `#`、`~` 这类自定义分隔符时要把它传进去，否则用户输入里的分隔符会截断模式。⚠️ PHP 8.5 还带来一条 PCRE 层面的行为变更：不再以 `PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK` 编译（PHP 8.4 会打开该选项，更早的 PHP 所配 PCRE2 也还没有这条限制，效果都是允许），于是「环视里用 `\K`」在 PHP 8.5 从允许变成编译失败，PCRE2 的报错文案是 `\K is not allowed in lookarounds`，靠 `(?=...\K...)` 改写匹配起点的老代码要改用捕获组或自己维护偏移量。另外实际打包的 PCRE2 版本随 PHP 版本变化（PHP 8.5 打包的是 PCRE2 10.44），可以在运行时用 `PCRE_VERSION` 常量确认；模式里写了 PCRE2 新语法而目标环境版本偏旧时，`preg_last_error()` 返回的 `PREG_BAD_UTF8_ERROR`、`PREG_INTERNAL_ERROR` 之类的错误码是唯一线索，养成检查它的习惯。

📘 [PHP 8.5 · preg_replace](https://www.php.net/manual/en/function.preg-replace.php) · [preg_split](https://www.php.net/manual/en/function.preg-split.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的 `Regexp` 用 Onigmo 引擎，命名组写 `(?<name>...)`，取值走 `MatchData`：`m[:name]`、`m["name"]`、`m.named_captures`、`m.names` 都能用；替换用 `sub`（第一处）与 `gsub`（全部），模板里的引用是反斜杠家族——`\1`、`\k<name>`、`\&`（或 `\0`）、`` \` ``、`\'`、`\+`、`\\`，而 `$1`、`$&`、`` $` ``、`$'` 在 Ruby 里是**全局变量**，写进替换字符串不会展开。切分用 `split`（带 limit、会保留捕获组），转义用 `Regexp.escape` 与 `Regexp.union`。

```ruby
# 命名组 (?<name>...)：MatchData 可以按名字或下标取
re = /(?<y>\d{4})-(?<m>\d{2})/
m = re.match("2026-09")
p [m[:y], m[:m], m[1], m[2]]        # ["2026", "09", "2026", "09"]
p m.named_captures                  # {"y" => "2026", "m" => "09"}
p m.names                           # ["y", "m"]

# 替换模板用反斜杠：\1 \k<name> \& / \0；$ 系列在模板里不生效
puts "Doe, John".sub(/(\w+), (\w+)/, '\2 \1')                                # John Doe
puts "Doe, John".gsub(/(?<last>\w+), (?<first>\w+)/, '\k<first>_\k<last>')   # John_Doe
puts "abc".sub(/b/, '[\&]')          # a[b]c
puts "abc".sub(/b/, '[\0]')          # a[b]c
puts "abc".sub(/b/, '[$&]')          # a[$&]c ← $& 不是替换模板语法

# 块替换：块参数是整段匹配，$~ 是当前 MatchData
puts "Doe, John".sub(/(?<last>\w+), (?<first>\w+)/) { "#{$~[:first]} #{$~[:last]}" }
# John Doe

# split：默认丢尾部空串，limit 为负则保留；捕获组会留在结果里
p "a, b,c".split(/,\s*/)        # ["a", "b", "c"]
p "a1b2c".split(/(\d)/)         # ["a", "1", "b", "2", "c"]
p "a,b,,".split(",", -1)        # ["a", "b", "", ""]
p "a,b,,".split(",")            # ["a", "b"]

# 转义与 union
p Regexp.escape("a.b*c(d)")     # "a\\.b\\*c\\(d\\)"
p Regexp.union("a.b", "c*d")    # /a\.b|c\*d/

# 同名组允许（取最后匹配的那个），分支重置不支持
p /(?<n>a)(?<n>b)/.match("ab")[:n]      # "b"
begin
  Regexp.new("(?|(a)|(b))")
rescue RegexpError => e
  puts e.message                        # undefined group option: /(?|(a)|(b))/
end

# 占有量词与条件模式是 Onigmo 原生支持
p "aaaa".scan(/a++a/)                          # []
p "abc abd bd".gsub(/(a)?b(?(1)c|d)/, "X")     # "X aX X"
```

`sub`/`gsub` 的替换字符串要用单引号写（`'\1'`），因为双引号字面量里 `\1` 会被 Ruby 先解释成八进制转义；模板里想输出字面反斜杠要写 `'\\\\'`（单引号下两个反斜杠）。`\&` 与 `\0` 都表示整段匹配，`` \` `` 与 `\'` 是匹配前、匹配后的文本，`\+` 是「最后一个被捕获的组」——这一组反斜杠记号是 Ruby 独有的，从 JavaScript 或 C# 搬代码时最容易照抄成 `$1` 而悄悄失效（不报错，只是原样输出 `$1`）。取值的另一条路是块替换：块里可以直接读 `$~`（当前的 `MatchData`）或 `Regexp.last_match`，还可以用它的 `pre_match`、`post_match` 做上下文相关替换，比模板灵活得多。Ruby 是少数**允许同名捕获组**的实现：`/(?<n>a)(?<n>b)/` 合法，`m[:n]` 给最后一个参与匹配的组，此时 `m.names` 只会出现一个 `n`，按组数遍历时不能假设名字唯一。⚠️ 分支重置 `(?|...)` 在 Onigmo 里不支持（报 `undefined group option`），默认也没有超时保护——Ruby 3.2 起才有 `Regexp.timeout` 与 `Regexp.linear_time?`（Ruby 4.0 没有新增 Regexp API，只是把 Unicode 数据更新到 17.0），面对用户输入时要主动设置超时。

📘 [Ruby · Regexp](https://docs.ruby-lang.org/en/master/Regexp.html)

{{% /tab %}}

{{< /tabpane >}}

### 性能、安全与常见陷阱

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 标准库本身没有正则，生态里的 `regex` crate 是自动机实现（内部用 NFA/DFA 混合），对任意模式都保证线性时间匹配，因此**根本不存在 ReDoS**，也不提供超时参数。代价同样明确：它不支持反向引用与环视，`(?<=a)b` 与 `(a)\1` 会在编译期直接报错；要这些能力得换 `fancy-regex` 或 `pcre2` crate，那时就重新回到回溯世界。使用前最该记住的两件事是：把编译好的 `Regex` 存起来复用，以及可以用 `RegexBuilder::size_limit` 给编译产物设上限。

```rust
use regex::{Regex, RegexBuilder};
use std::sync::LazyLock;
use std::time::Instant;

fn main() {
    // ① 同样的 ReDoS 形状：回溯引擎指数爆炸，regex crate 保持线性
    let re = Regex::new(r"^(([A-Za-z])+)+$").unwrap();
    for n in [20usize, 2000, 200_000] {
        let s = "A".repeat(n) + "!";                 // 末尾 "!" 让整条匹配失败，这是回溯引擎最坏的输入
        let t = Instant::now();
        let m = re.is_match(&s);
        println!("len={n:>7} matched={m} elapsed={:?}", t.elapsed());
    }
    // len=     20 matched=false elapsed=136.083µs
    // len=   2000 matched=false elapsed=60.542µs
    // len= 200000 matched=false elapsed=7.9365ms     ← 输入长 1 万倍，时间只长 100 倍量级

    // ② 不支持环视与反向引用：编译期即失败，不会留到运行时
    for pat in [r"(?<=a)b", r"(a)\1"] {
        match Regex::new(pat) {
            Ok(_) => println!("{pat} ok"),
            Err(e) => println!("{pat} -> {e:?}"),
        }
    }
    // (?<=a)b -> error: look-around, including look-ahead and look-behind, is not supported
    // (a)\1   -> error: backreferences are not supported

    // ③ 编译期 NFA 大小上限：默认 nfa_size_limit 是 10 MiB，可以调小以拒绝巨型模式
    match RegexBuilder::new(r"\w").size_limit(45_000).build() {
        Ok(_) => println!("size_limit=45000 ok"),
        Err(e) => println!("size_limit=45000 -> {e:?}"),   // size_limit=45000 -> CompiledTooBig(45000)
    }

    // ④ 缓存：把编译结果放进程级静态变量，别在热点路径里 Regex::new
    static WORD: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\w+").unwrap());
    println!("{}", WORD.find("hi there").unwrap().as_str());   // hi
}
```

线性时间是「模式无关」的：`(a+)+`、`(a|aa)+`、`([a-z]+)*$` 这些在 Java、Node、Python 里能让进程挂死的形状，在 `regex` crate 里都只是普通的自动机状态转移，输入越长越慢但始终成正比，`200_000` 字符也只要几毫秒。`size_limit` 限制的是编译期的 NFA 堆内存而不是匹配时间，它防的是「一条恶意模式在编译阶段就把内存吃掉」，所以拿到用户提供的模式时值得把它调小并配合 `is_match` 的超时上层逻辑（Rust 没有内建匹配超时）。缓存方面，`LazyLock<Regex>`（1.80 起稳定）或 `OnceLock<Regex>` 都能满足，原则是每个模式全进程只编译一次；`Regex::new` 在循环里比 `is_match` 贵几个数量级。⚠️ 最后两个 Rust 专属坑：字符串字面量里 `\d`、`\b`、`\w` 都不是合法转义（rustc 会报 `unknown character escape`），正则一律用 `r"..."` 原始字符串；特别注意 `r"\b"` 是词边界，而不加 `r` 的 `"\b"` 连退格符都不是——Rust 根本没有 `\b` 这个字符串转义，写错时是编译期报错，不要把它当成 Java/C 的退格符。

📘 [docs.rs · regex crate（线性时间与语法限制）](https://docs.rs/regex/latest/regex/)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 5.7 引入的 `Regex` 字面量 `/.../` 与 `RegexBuilder` 底层走的是回溯式匹配，所以它会灾难性回溯：把 `^([A-Za-z]+)+$` 套到一个 14 个字符的失败输入上就要 0.3 秒，18 个字符以上基本等于挂起。`NSRegularExpression` 是另一套（ICU 实现），同样是回溯引擎。Swift 也没有内建的正则超时 API，防 ReDoS 只能靠限制输入长度、把模式改写成无回溯形状，或者干脆换掉引擎。

```swift
import Foundation

// ① 回溯引擎：n 每加 2，耗时大约翻两番；n=14 已经 0.3s
let re = try! Regex(#"^([A-Za-z]+)+$"#)
for n in [10, 12, 14] {
    let s = String(repeating: "A", count: n) + "!"   // "!" 让匹配必然失败
    let t0 = Date()
    _ = try? re.wholeMatch(in: s)
    print("n=\(n) \(String(format: "%.4f", Date().timeIntervalSince(t0)))s")
}
// n=10 0.0044s
// n=12 0.0274s
// n=14 0.3059s

// ② 同样语义的无回溯写法：一个字符类加一个 + 就够，耗时与长度成正比
let safe = try! Regex(#"^[A-Za-z]+$"#)
for n in [14, 100_000] {
    let s = String(repeating: "A", count: n) + "!"
    let t0 = Date()
    _ = try? safe.wholeMatch(in: s)
    print("safe n=\(n) \(String(format: "%.5f", Date().timeIntervalSince(t0)))s")
}

// ③ 缓存：Regex 是值类型，可以放进静态属性只构造一次
enum Patterns {
    static let word = try! Regex(#"\w+"#)
}
print(try! Patterns.word.firstMatch(in: "hi there")!.0)   // hi（Match.0 是整段匹配）
```

Swift 的正则字面量在编译期就要能构造，所以 `/.../` 里的语法错误是编译错误；运行时用 `try Regex(_:)` 构造时才会抛错，因此模式来自用户输入时必须用 `try` 版本并处理失败。⚠️ 两个默认值要记牢：Swift 的 `^` 与 `$` 默认只认整串首尾（实测 `^b$` 匹配不上 `"a\nb"`，要按行匹配得显式加 `(?m)`，`\A` 与 `\z` 则始终是整串首尾）；`.` 默认也不匹配换行，要让 `.` 匹配换行得加 `(?s)`。要写「整串匹配」时优先用 `wholeMatch(in:)` 而不是自己加锚点，这样语义不依赖锚点的默认值。`RegexBuilder` 的 `try?` 与 `First`/`OneOrMore` 组合在可读性上有优势，但它不会改变引擎的回溯本质，危险的嵌套量词换成 `OneOrMore(OneOrMore(...))` 一样会爆炸。

📘 [Apple Developer · Swift Regex](https://developer.apple.com/documentation/swift/regex)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `regexp` 包是 RE2 风格的自动机实现，匹配时间与输入长度成线性关系（与模式无关），因此**不存在灾难性回溯**，也正因为如此它刻意不支持反向引用与环视——`regexp.Compile` 遇到 `(a)\1` 或 `(?<=a)b` 会返回 error。`regexp` 没有任何超时或步数上限参数，因为线性时间下不需要；Go 1.27 也没有给 `regexp` 带来新 API。真正需要注意的反而是「编译本身」：`regexp.MustCompile` 放进热路径同样是浪费。

```go
package main

import (
	"fmt"
	"regexp"
	"strings"
	"time"
)

var nested = regexp.MustCompile(`^(([A-Za-z])+)+$`) // 回溯引擎的经典炸弹形状

func main() {
	// ① 线性时间：输入 20 → 200000 字符，耗时只涨到毫秒级
	for _, n := range []int{20, 2000, 200000} {
		s := strings.Repeat("A", n) + "!"
		t := time.Now()
		m := nested.MatchString(s)
		fmt.Printf("len=%7d matched=%v %v\n", n, m, time.Since(t))
	}
	// len=     20 matched=false 79.417µs
	// len=   2000 matched=false 119.125µs
	// len= 200000 matched=false 5.55625ms

	// ② 不支持的构造在编译期就返回 error
	for _, pat := range []string{`(?<=a)b`, `(a)\1`, `(?P<n>a)+`, `\p{Greek}+`} {
		_, err := regexp.Compile(pat)
		fmt.Printf("%-12s err=%v\n", pat, err != nil)
	}
	// (?<=a)b     err=true
	// (a)\1       err=true
	// (?P<n>a)+   err=false   ← 命名组语法是 (?P<name>...)
	// \p{Greek}+  err=false   ← Unicode 属性可以放心用

	// ③ 缓存：包级变量只编译一次；不要在每个请求里 MustCompile
	fmt.Println(regexp.MustCompile(`\w+`).FindString("hi there")) // hi
}
```

Go 的 RE2 保证是「对任意模式与任意输入，匹配时间都是输入长度的线性函数，系数由模式编译出的自动机规模决定」，所以 `(a+)+$`、`(a|aa)+$`、`(\w+\s?)*` 这些在其他语言里要命的形状在 Go 里是安全的，可以直接处理不受信任的用户输入。代价是表达力：需要反向引用、环视、条件分支或递归模式时，`regexp` 给不了答案，只能退回到手写状态机、`strings` 系列函数，或者引入第三方回溯引擎（那就得自己承担 ReDoS 风险）。⚠️ 另外一个容易被忽视的性能点：`regexp.MustCompile` 每次调用都要解析并编译整个模式，代价是微秒到毫秒量级，所以它只应该出现在包级变量初始化或 `init` 里；确实无法预定义时用 `sync.Once` 或 `sync.Map` 做缓存。`regexp.QuoteMeta` 用于把用户输入安全地拼进模式，等价于其他语言的 `escape`。

📘 [pkg.go.dev · regexp（线性时间与语法说明）](https://pkg.go.dev/regexp)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的 `re` 是典型的回溯引擎，支持反向引用、环视、原子组与占有量词，也因此会灾难性回溯，而且**没有内建超时**。最容易踩的炸弹形状是「外层量词套内层量词」：`([A-Za-z]+)+$` 在 22 个字符上已经要 0.29 秒，长度再多几个就是分钟级。`re` 还有一层隐式缓存在帮忙——最近 512 个模式会被缓存（`re._MAXCACHE` 硬上限 512），所以短小的直接 `re.match(pattern, ...)` 未必慢；真正的开销来自「模式本身很复杂」或「模式由字符串拼接生成」。

```python
import re, time

# ① 灾难性回溯：嵌套量词 + 失败输入
for n in (10, 14, 18, 22):
    s = "A" * n + "!"
    t = time.perf_counter()
    re.search(r"([A-Za-z]+)+$", s)
    print(n, "%.4f s" % (time.perf_counter() - t))
# 10 0.0003 s
# 14 0.0010 s
# 18 0.0161 s
# 22 0.2921 s          ← 长度 +4，耗时 ×18

# ② 改写为等价的无回溯形状：一个字符类 + 一个 +，线性时间
t = time.perf_counter()
re.search(r"[A-Za-z]+$", "A" * 22 + "!")
print("%.4f s" % (time.perf_counter() - t))          # 0.0000 s

# ③ 原子组与占有量词（3.11+）是「禁止回溯」的开关
print(re.search(r"(?>a+)a", "aaaa"))                  # None：原子组吃掉全部 a 后不再吐出
print(re.search(r"a++a", "aaaa"))                     # None：占有量词同理

# ④ 隐含缓存：同一模式重复使用时不必手工 compile
print(re._MAXCACHE, len(re._cache))                   # 512 4（值随进程内已用模式数变化）

# ⑤ 拼接用户输入必须先 escape
user = "a+b"
print(re.escape(user), re.search(re.escape(user), "xa+by") is not None)   # a\+b True
```

`re` 没有超时参数是一处硬伤：官方文档只提供「限制输入长度」「写无回溯模式」「用第三方 `regex` 模块的 `timeout` 参数」这几条路。实践中最可靠的做法是把输入先按业务上限截断（比如超过 10 KB 的字段不进正则），再把高风险模式改写成无嵌套的形状；确实必须保留嵌套时，可以给整段匹配套上 `signal.alarm`（仅主线程、类 Unix）或在子进程里跑。⚠️ 三个默认语义差异经常导致误判：`$` 在默认模式下也会匹配「结尾换行之前」的位置（`re.search(r"abc$", "abc\n")` 成立，要只匹配真正的串尾得用 `\Z`）；`^`/`$` 默认只认整串首尾，多行锚点必须加 `re.M`；`\d`/`\w` 默认是 Unicode 语义（要 ASCII 语义加 `re.ASCII` 或 `(?a)`）。此外 `re.escape` 之后直接做字符串拼接是安全的，但自己写 `replace(".", "\\.")` 一定会漏字符。

📘 [Python 3 · re 模块（回溯、原子组、缓存）](https://docs.python.org/3/library/re.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的 `Regex` 在 JVM 上就是 `java.util.regex.Pattern` 的包装，语法与陷阱和 Java 完全一致：回溯引擎、支持反向引用与环视、**没有超时**，`(a+)+$` 一样能把线程钉死。多平台场景要额外注意实现并不统一——JS 后端复用 `RegExp`（并且强制带 `u` 标志），Native 与 Wasm（wasm-js、wasm-wasi）共用 stdlib 里的另一套实现，`RegexOption` 的可用取值也按平台不同。因此跨平台代码不要依赖某个平台独有的语法细节。

```kotlin
import kotlin.system.measureTimeMillis
import java.util.regex.Pattern

fun main() {
    // ① 回溯炸弹：与 Java 完全相同
    val bomb = Regex("^([A-Za-z]+)+$")
    for (n in listOf(18, 22)) {
        val s = "A".repeat(n) + "!"
        val ms = measureTimeMillis { bomb.matches(s) }
        println("n=$n ${ms}ms")
    }
    // n=18 约 20ms，n=22 约 300ms（线性增长的那部分是编译；指数部分来自回溯）
    // ⚠️ n 到 26 以上可能长到分钟级，不要在本机随手试

    // ② 改写：单层量词
    println(Regex("^[A-Za-z]+$").matches("A".repeat(22) + "!"))   // false，微秒级

    // ③ 需要 Java 级选项时直接拿到底层 Pattern（命名组写法、UNICODE_CHARACTER_CLASS 等）
    val p = Pattern.compile("\\w+", Pattern.UNICODE_CHARACTER_CLASS)
    println(p.matcher("héllo").find())                             // true

    // ④ 缓存：顶层 val 只构造一次；不要在函数里反复 Regex("...")
    println(WORD.findAll("hi there").map { it.value }.toList())     // [hi, there]
}

val WORD = Regex("\\w+")
```

Kotlin 把 `Pattern.compile` 藏进 `Regex` 构造函数里，这让代码更短，也更容易犯「在循环里 new 一个 `Regex`」的错——JVM 上每次构造都要重新解析并编译模式。常见做法是写成顶层 `val`、`companion object` 属性或用 `by lazy`，语义上与 Java 里 `private static final Pattern` 等价。`RegexOption` 在 JVM 上提供 7 个取值：`IGNORE_CASE`、`MULTILINE`、`DOT_MATCHES_ALL`、`LITERAL`、`COMMENTS`、`UNIX_LINES`、`CANON_EQ`，但它**没有** `UNICODE_CHARACTER_CLASS`，要让 `\d`/`\w` 变成 Unicode 语义得用内联标志 `(?U)`，或直接使用 `Pattern.compile`（这 7 个取值是 JVM 的集合，官方文档提醒各平台不同，例如 `LITERAL` 在 Kotlin/JS 上就不存在）。⚠️ 超时同样缺失：Android 与服务端都只能靠限制输入长度、把模式改成无回溯形状，或把匹配放进可中断的线程并在外部加 `Future.get(timeout)`；后者只是让调用方不再等待，被回溯占满的线程不会自动停下，所以这不是真正的解法。

📘 [Kotlin API · kotlin.text.Regex](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/-regex/)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的 `java.util.regex` 是传统的 NFA 回溯引擎，官方文档明确写了「performs traditional NFA-based matching with ordered alternation as occurs in Perl 5」，因此它会灾难性回溯，而 `Pattern`/`Matcher` **没有提供任何超时 API**。Java 能自救的手段是语法层面的：占有量词 `*+`、`++`、`?+`、`{n,m}+` 与原子组 `(?>...)` 可以切断回溯，把指数级路径直接掐掉。另一个细节是 `\d`/`\w` 默认只认 US-ASCII，要 Unicode 语义得加 `UNICODE_CHARACTER_CLASS`。

```java
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Perf {
    public static void main(String[] args) {
        // ① 回溯炸弹：嵌套量词 + 失败输入
        Pattern bomb = Pattern.compile("^([A-Za-z]+)+$");
        for (int n : new int[]{18, 22}) {
            String s = "A".repeat(n) + "!";
            long t0 = System.nanoTime();
            boolean m = bomb.matcher(s).matches();
            System.out.printf("n=%d matched=%b %.1fms%n", n, m, (System.nanoTime() - t0) / 1e6);
        }
        // n=18 大致几十毫秒，n=22 大致数百毫秒；n=30 以上会长到分钟甚至小时级

        // ② 用原子组切断回溯：先独占吃掉所有 a，再发现后面没有 b 就直接失败
        Pattern atomic = Pattern.compile("^(?>a+)b$");
        long t1 = System.nanoTime();
        System.out.println(atomic.matcher("a".repeat(30) + "!").matches());   // false，微秒级
        System.out.printf("%.3fms%n", (System.nanoTime() - t1) / 1e6);

        // ③ 占有量词同理
        System.out.println(Pattern.compile("^a++b$").matcher("a".repeat(30) + "!").matches());  // false

        // ④ \d \w 默认 ASCII；UNICODE_CHARACTER_CLASS 才是 Unicode 语义
        System.out.println(Pattern.compile("\\d").matcher("٣").find());                        // false
        System.out.println(Pattern.compile("\\d", Pattern.UNICODE_CHARACTER_CLASS).matcher("٣").find()); // true

        // ⑤ 缓存：编译一次，Matcher 每次新建；Matcher 不是线程安全的
        System.out.println(Pattern.compile("\\w+").matcher("hi there").results().count());     // 2
    }
}
```

官方文档在 `Pattern` 类里明确提醒「如果一个模式要被多次使用，编译一次并复用比每次调用 `Pattern.matches` 更高效」，因为 `Pattern.matches(regex, input)` 每次都会重新编译。工程上的标准写法是把 `Pattern` 存成 `private static final` 字段，这一点和 .NET 的 `Regex` 复用是同一个道理。⚠️ Java 没有内建超时，所以面对用户提供的模式或输入，可选项只有：限制输入长度、用 `(?>`/占有量词把所有嵌套量词改写成无回溯形状、或者换成 RE2/J 这类线性时间库；把匹配丢进线程再用 `Future.get(timeout)` 只是让调用方提前返回，被回溯占满的线程仍在燃烧 CPU，属于「看起来能超时」的假解法。`Matcher` 每次匹配都要重新 `pattern.matcher(input)`，且 `Matcher` 有可变状态，不能跨线程共享。

📘 [Java SE 25 · java.util.regex.Pattern](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/regex/Pattern.html)

{{% /tab %}}

{{% tab header="C++" %}}

`std::regex`（C++11）默认使用 ECMAScript 语法，是回溯实现，性能长期被诟病：同一个匹配动辄比手写解析慢一两个数量级，编译模式也慢，而且嵌套量词会指数爆炸。相对友好的一点是 libc++ 给了逃生舱——回溯复杂度超过预设上限时抛 `std::regex_error`，`code()` 是 `error_complexity`，而不是无限挂起（本节实测用的就是 Apple libc++）。⚠️ 但这道闸门**只有 libc++ 有**：libstdc++ 的 `_Executor` 里没有复杂度上限，GCC 的 `std::regex` 在同类输入上会一直算下去，甚至把栈用爆（见 GCC bug 61601「C++11 regex resource exhaustion」与 86164「std::regex crashes when matching long lines」），所以「标准库会替你踩刹车」这个假设不能跨实现推广。要真正的高性能与安全，社区共识是换 RE2、Boost.Regex、CTRE（编译期正则）或 `std::regex` 之外的解析方案。

```cpp
#include <chrono>
#include <iostream>
#include <regex>
#include <string>

int main() {
    std::regex re(R"(^([A-Za-z]+)+$)", std::regex::ECMAScript);
    for (int n : {6, 8, 10, 12, 14}) {
        std::string s(size_t(n), 'A');
        s += "!";
        auto t0 = std::chrono::steady_clock::now();
        try {
            bool m = std::regex_search(s, re);
            auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                          std::chrono::steady_clock::now() - t0).count();
            std::cout << "n=" << n << " matched=" << m << " " << ms << "ms\n";
        } catch (const std::regex_error& e) {
            // error_complexity：回溯复杂度超限；error_stack：栈空间不足
            std::cout << "n=" << n << " regex_error code=" << e.code()
                      << " what=" << e.what() << "\n";
        }
    }
    // 实测（Apple libc++，clang -std=c++23 -O2）：
    // n=6 matched=0 0ms
    // n=8 matched=0 0ms
    // n=10 matched=0 0ms
    // n=12 matched=0 1ms
    // n=14 regex_error code=12 what=The complexity of an attempted match against a regular expression exceeded a pre-set level.

    // 缓存：std::regex 构造昂贵，声明为 static const 只构造一次
    static const std::regex word(R"(\w+)");
    std::cout << std::regex_search(std::string("hi there"), word) << "\n";   // 1

    // 无回溯写法：把嵌套量词压成单层
    static const std::regex safe(R"(^[A-Za-z]+$)");
    std::cout << std::regex_search(std::string(30, 'A') + "!", safe) << "\n"; // 0
}
```

这段实测最能说明问题：同样是 `^([A-Za-z]+)+$`，libc++ 在 n=12 时还能给出结果（1 毫秒），到 n=14 就直接抛 `std::regex_error`，`what()` 里的文案正是「匹配复杂度超过预设上限」。这正是 libc++ 内置的保护：它不给你无限回溯的机会，但也意味着**不能依赖 `std::regex` 去处理不受信任的模式**——异常虽然保住了进程，捕获之后你也只有「拒绝这次匹配」一条路；而 libstdc++ 连这道保护都没有，同样的模式会一直算下去或把栈用爆。⚠️ 标准的 `error_type` 里 `error_complexity`、`error_stack`、`error_space` 三个值都是实现定义的，不同标准库在同样的输入上可能抛不同的码甚至都不抛；如果非要用 `std::regex`，请务必把 `catch (const std::regex_error&)` 写全，并把 `static const std::regex` 提到函数外只构造一次。真正对性能有要求的项目应该用 CTRE 做编译期生成，或用 RE2/Boost.Regex 换取可预测的时间上界。

📘 [cppreference · std::regex_constants::error_type](https://en.cppreference.com/w/cpp/regex/error_type)

{{% /tab %}}

{{% tab header="C" %}}

C 的标准库没有正则；`<regex.h>` 是 POSIX 接口（`regcomp`、`regexec`、`regerror`、`regfree`），ISO C 到 C23 都没有把它纳入标准。POSIX 只规定接口语义，**不规定引擎算法与时间复杂度**，也不提供超时或回溯步数上限：`regcomp` 的标志只有 `REG_EXTENDED`、`REG_ICASE`、`REG_NEWLINE`、`REG_NOSUB`，以及 Issue 8（POSIX.1-2024）新增的 `REG_MINIMAL`。所以在 C 里谈 ReDoS，结论是「取决于底层 libc 实现，你没有统一的刹车」。下面的实测用的是 macOS 的 BSD 实现，它在这几个模式上不呈指数爆炸，但这不能推广到其他平台。

```c
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(void) {
    regex_t re;
    if (regcomp(&re, "^([A-Za-z]+)+$", REG_EXTENDED | REG_NOSUB) != 0) return 1;  /* 0 = 成功 */

    /* 实测（macOS libSystem 的 BSD regex）：没有指数爆炸，但 POSIX 不保证这一点 */
    int lens[] = {26, 2000, 200000, 2000000};
    for (int i = 0; i < 4; i++) {
        int n = lens[i];
        char *s = malloc((size_t)n + 2);
        memset(s, 'A', (size_t)n);
        s[n] = '!'; s[n + 1] = '\0';            /* 末尾 ! 让匹配失败 */
        clock_t t0 = clock();
        int rc = regexec(&re, s, 0, NULL, 0);
        printf("len=%8d rc=%d %.4fs\n", n, rc, (double)(clock() - t0) / CLOCKS_PER_SEC);
        free(s);
    }
    /* len=      26 rc=1 0.0000s
       len=    2000 rc=1 0.0004s
       len=  200000 rc=1 0.0174s
       len= 2000000 rc=1 0.0858s   ← 线性 */
    regfree(&re);

    /* POSIX ERE 的硬性缺失：非贪婪、命名组、\d、环视、反向引用统统没有 */
    regex_t t;
    printf("a+?      rc=%d\n", regcomp(&t, "a+?", REG_EXTENDED));      /* 13 = REG_BADRPT（无效的重复运算符） */
    printf("(?<n>a)  rc=%d\n", regcomp(&t, "(?<n>a)", REG_EXTENDED));  /* 13 = REG_BADRPT（同上，macOS 上两者同码） */
    printf("\\d       rc=%d\n", regcomp(&t, "\\d", REG_EXTENDED));     /*  0：被当成字面 d */
    return 0;
}
```

C 用户面对正则时的现实选项有三条。第一条是接受 POSIX 的表达力：没有非贪婪（只有 Issue 8 新增的 `REG_MINIMAL`，且各平台实现进度不一）、没有命名组、没有 `\d` 与 `\w`（`\d` 会被当成字面 `d`，`[[:digit:]]` 才是正确写法）、没有环视与反向引用，需要这些就得引 PCRE2 或 RE2 的 C 库。第二条是接受「没有超时」这件事，用输入长度上限与进程级看门狗（`alarm` + 信号，或把匹配放进子进程）兜住最坏情况，因为 `regexec` 一旦进入坏路径就无法中断。第三条是干脆不用正则：C 里很多「正则需求」其实是 `strtok`、`strchr`、`sscanf`、`fnmatch` 或一个十几行的状态机就能解决的。⚠️ 还有一个 ABI 层面的坑：`regex_t` 的大小与内容是实现定义的，跨库传递或复制它是 UB，必须始终用同一份 libc 编译的正则对象。

📘 [POSIX.1-2024 · regcomp / regexec](https://pubs.opengroup.org/onlinepubs/9799919799/functions/regcomp.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的 `Regex` 是 PCRE2 的绑定，`r"..."` 字面量在第一次求值时编译，之后被缓存复用；它属于回溯引擎，支持反向引用、环视、原子组与占有量词，**因此有 ReDoS 风险，而且 Julia 层没有暴露超时参数**。Julia 特有的一个性能细节是：`r"..."` 字面量在同一个方法里只构造一次，所以在函数体内写 `r"..."` 并不会每次都重新编译；但用 `Regex(str)` 或 `Regex(str, flags)` 动态构造就会，热点路径上要自己缓存。

```julia
# ① 回溯炸弹：PCRE2 与 Python/Java 一样会指数爆炸
bomb = Regex("^([A-Za-z]+)+$")
for n in (10, 14, 18)
    s = "A"^n * "!"
    t = @elapsed match(bomb, s)
    println("n=$n $(round(t, digits=4))s")
end
# n=10 约 0.0002s，n=14 约 0.003s，n=18 约 0.05s（n 再大就会明显卡住）

# ② 无回溯写法：单层量词
@time match(r"^[A-Za-z]+$", "A"^18 * "!")   # 微秒级

# ③ 原子组（PCRE 语法）可以切断回溯
println(match(r"^(?>a+)b$", "a"^40 * "!"))   # nothing，微秒级

# ④ 字面量 r"..." 被缓存：同一方法内重复使用不会重复编译
f() = (for _ in 1:1000; occursin(r"\d+", "abc123"); end)
@time f()                                    # 只有第一次编译

# ⑤ 动态构造的模式要自己缓存
const WORD = Regex("\\w+")
println(join(m.match for m in eachmatch(WORD, "hi there"), ","))   # hi,there
```

PCRE2 的运行时资源限制在 Julia 里没有对应的公开 API，所以 Julia 的防线和其他回溯语言一样：截断输入、改写模式、把 `r"..."` 而不是 `Regex("...")` 写进热路径。`r"..."` 字面量的缓存是按方法实例生效的，这一点在写库函数时很有用——只要模式是常量，就不必自己包一层 `const`；反过来，`Regex("$prefix\\d+")` 这种拼出来的模式每次调用都会走完整的编译流程，PCRE2 编译一个中等复杂的模式通常在几微秒到几十微秒，循环一亿次就是几十分钟。⚠️ 另外两个 Julia 专属提醒：`r"..."` 里不做转义处理（`r"\x"` 是合法的两个字符），所以反斜杠不需要写双份；正则的 `m` 标志在 Julia 里是「多行」，与 Ruby 的 `/m`（让 `.` 匹配换行）含义不同，Julia 让 `.` 匹配换行的是 `s` 标志。

📘 [Julia 文档 · Regular Expressions（PCRE2）](https://docs.julialang.org/en/v1/manual/strings/#Regular-Expressions)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的正则默认是回溯引擎，但它是主流语言里「刹车」做得最全的：`new Regex(pattern, options, TimeSpan)` 可以设置单次匹配超时并抛 `RegexMatchTimeoutException`，`RegexOptions.NonBacktracking`（.NET 7 起）能把引擎切换成线性时间实现，`[GeneratedRegex]` 源码生成器（.NET 7 起，.NET 9 起还能用在 partial 属性上）则把编译成本从运行时挪到编译期。需要注意的是用户没设超时时默认是 `Regex.InfiniteMatchTimeout`，也就是**永不超时**。

```csharp
using System;
using System.Diagnostics;
using System.Text.RegularExpressions;

public partial class Perf
{
    // ① 源码生成器：模式在编译期变成专门的 C# 代码，运行时零解析零 JIT
    [GeneratedRegex(@"\w+")]
    private static partial Regex WordRegex();

    public static void Main()
    {
        // ② 内建超时：1 秒后抛 RegexMatchTimeoutException 而不是一直烧 CPU
        var bomb = new Regex(@"^([A-Za-z]+)+$", RegexOptions.None, TimeSpan.FromSeconds(1));
        try
        {
            var sw = Stopwatch.StartNew();
            bool m = bomb.IsMatch(new string('A', 30) + "!");
            Console.WriteLine($"matched={m} {sw.ElapsedMilliseconds}ms");
        }
        catch (RegexMatchTimeoutException e)
        {
            Console.WriteLine($"timeout after {e.MatchTimeout}");   // timeout after 00:00:01
        }

        // ③ NonBacktracking：用表达力换线性时间（不支持环视、反向引用、原子组）
        try
        {
            var lin = new Regex(@"^([A-Za-z]+)+$", RegexOptions.NonBacktracking);
            var sw = Stopwatch.StartNew();
            bool m = lin.IsMatch(new string('A', 200_000) + "!");
            Console.WriteLine($"linear matched={m} {sw.ElapsedMilliseconds}ms");
        }
        catch (NotSupportedException e)
        {
            Console.WriteLine(e.Message);
        }

        // ④ 编译缓存：静态方法走全局缓存（默认 15 条）；实例字段自己复用
        Console.WriteLine(Regex.CacheSize);                 // 15
        Console.WriteLine(WordRegex().Match("hi there").Value);   // hi
    }
}
```

.NET 的三件工具各有取舍。`RegexOptions.Compiled` 把模式编译成 IL，匹配吞吐最高但构造昂贵、首次使用还要再 JIT，且在禁止动态代码的平台上会退化成空操作；`[GeneratedRegex]` 在编译期就把等价逻辑生成成 C# 源码，既拿到 `Compiled` 的吞吐又省掉启动开销，官方建议是「能用源码生成器就用，不要用 `RegexOptions.Compiled`」。⚠️ 源码生成器有两个边界：它**不支持** `RegexOptions.NonBacktracking`（遇到时会退回缓存一个普通 `Regex` 实例），也不支持带忽略大小写的反向引用。`Regex.CacheSize` 默认 15，缓存只对静态方法生效，实例方法构造的 `Regex` 不进缓存，所以 `Regex.IsMatch(s, pattern)` 这种写法在模式多于 15 个时会持续发生淘汰与重编译。关于超时还要留意文档的提醒：`RegexMatchTimeoutException` 只说明「超了」，不保证原因一定是回溯，也可能是超时值设得太紧。

📘 [MS Learn · .NET 正则表达式中的回溯（超时与 NonBacktracking）](https://learn.microsoft.com/en-us/dotnet/standard/base-types/backtracking-in-regular-expressions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `RegExp` 在 VM 上是自研实现（V8 Irregexp 的移植），Web 编译目标则允许复用浏览器的 `RegExp`；官方文档明确说 Dart 必须实现 ECMAScript 规定的回溯语义，**不能用别的算法替换，也没有超时 API**；`^(a*|b)*c` 这类模式每多一个字符输入，失败判定所需的尝试次数就翻一倍。Dart 官方文档甚至专门写了一节「Performance Notice」讲这个问题，并给出改写建议，这在各语言文档里是少见的坦诚。所以 Dart 里防 ReDoS 只能靠模式写法与输入长度控制。

```dart
void main() {
  // ① 官方文档举的例子：嵌套量词 + 失败输入 = 指数时间
  final bomb = RegExp(r'^(a*|b)*c');
  for (final n in [10, 14, 18, 22]) {
    final s = List.filled(n, 'a').join();      // 没有 c，必然失败
    final sw = Stopwatch()..start();
    bomb.hasMatch(s);
    print('n=$n ${sw.elapsedMicroseconds}µs');
  }
  // n 每 +1 耗时约翻倍；20 个字符以上就会明显卡顿

  // ② 改写：让每次迭代无法匹配同一个字符串，退化情况就消失了
  final safe = RegExp(r'^[ab]*c');
  final sw = Stopwatch()..start();
  print(safe.hasMatch(List.filled(200000, 'a').join()));   // false
  print('${sw.elapsedMilliseconds}ms');        // 个位数毫秒

  // ③ RegExp.escape（dart:core 自 2.0 起就有）用于把用户输入安全拼进模式
  print(RegExp.escape('a+b'));                 // a\+b

  // ④ 缓存：顶层 final 只构造一次
  print(wordPattern.allMatches('hi there').map((m) => m[0]).toList());  // [hi, there]
}

final wordPattern = RegExp(r'\w+');
```

文档给出的三条经验规则值得直接背下来：让选择尽量由下一个字符决定；确保量词的「一次迭代匹配的串」和「多次迭代匹配的串」不重叠（`(a*|b)*` 之所以危险，是因为 `"aa"` 既能匹配一次也能匹配两次）；以及避免用 `.*` 开头做搜索，因为 `firstMatch` 对未锚定的模式相当于前面隐含了 `[^]*`，会让失败路径变成平方级。⚠️ 在 Web 上编译时 Dart 允许直接复用浏览器/JS 引擎的 `RegExp` 实现（官方原话是"the compiled code can use the browser's regexp implementation"，dart2wasm 是另一条路径），运行时行为与 VM 一致（都遵循 ECMAScript 回溯语义），所以「本机不卡、浏览器卡」的差异主要来自实现常数而不是算法。另外 Dart 也没有内建超时，服务端（`dart:io`）同样只能靠 `Isolate` + 外部超时来兜底，而 Isolate 里被回溯卡住的代码同样无法被强杀。

📘 [Dart API · RegExp（Performance Notice）](https://api.dart.dev/stable/latest/dart-core/RegExp-class.html)

{{% /tab %}}

{{% tab header="R" %}}

R 有两套引擎：默认是 TRE（POSIX ERE 加一些扩展），`perl = TRUE` 才切到 PCRE2。两者的语法与陷阱必须分开记：默认引擎里 `\d`、`\w`、`\s` 只是 TRE 的扩展而非 POSIX 标准，环视、原子组、命名组、递归这些 PCRE 语法一概没有；而忘记 `perl = TRUE` 是 R 用户最常见的一类 bug——模式不报错，只是静默地按另一套语义解释。性能上默认引擎实现较老、可用的回溯控制手段少，PCRE2 更快也更强，但两者**都没有暴露超时参数**。

```r
s <- paste0(strrep("A", 20), "!")

# ① 默认引擎（TRE）：\d 是 R 对 POSIX 的扩展，可以直接用，不必加 perl = TRUE
print(grepl("\\d+", "abc123"))                 # TRUE ← TRE 的 \d 就是数字类，不是字面 d
print(grepl("\\d+", "abc123", perl = TRUE))    # TRUE
print(grepl("(?<=a)b", "ab", perl = TRUE))     # TRUE：环视只有 PCRE2 才有
# grepl("(?<=a)b", "ab")                       # 🛑 TRE 不支持环视，报 invalid regular expression

# ② 非贪婪在默认引擎（TRE）里是扩展支持，但 perl = TRUE 才是完整 PCRE 语义
print(grepl("a.*?b", "axxbxxb"))                          # TRUE（TRE 也接受 .*? 这个扩展）
print(grepl("a.*?b", "axxbxxb", perl = TRUE))             # TRUE（PCRE 的非贪婪）
print(grepl("[[:digit:]]", "abc1"))                       # TRUE：默认引擎推荐写成 POSIX 字符类

# ③ 同一个模式在两套引擎下的行为要分开验：perl = TRUE 才走 PCRE2
print(regexpr("^([A-Za-z]+)+$", s, perl = TRUE))          # -1（无匹配，PCRE2 回溯）

# ④ 向量化匹配是 R 的强项，批量文本一次调用
v <- c("a1", "b2", "cc")
print(regmatches(v, regexpr("[0-9]", v)))      # "1" "2"（cc 无匹配，被丢掉）
print(grepl("[0-9]", v))                       # TRUE TRUE FALSE

# ⑤ extSoftVersion() 可以打印实际链接的 PCRE 版本（组件名就叫 PCRE，>= 10.00 即 PCRE2）
print(extSoftVersion()[["PCRE"]])
```

R 里不要用正则的场景特别多，因为基础包已经提供了更合适的工具：固定分隔符用 `strsplit(..., fixed = TRUE)`、固定子串查找用 `grepl(..., fixed = TRUE)`、固定子串替换用 `gsub(..., fixed = TRUE)`，这些都跳过正则解析；精确匹配整串用 `==` 或 `%in%`；读取表格用 `read.table`/`read.csv` 而不是用正则切列。⚠️ 三条 R 专属陷阱要记牢：`\d`、`\w`、`\s` 是 TRE 的扩展而不是 POSIX 标准，不同平台的默认引擎版本可能表现不同，跨平台代码可以写 `[[:digit:]]` 这类 POSIX 字符类，或者显式加 `perl = TRUE`；环视、命名反向引用、`(?>...)` 原子组只在 `perl = TRUE` 下可用，而 `perl = TRUE` 在 UTF-8 模式下 `\d`、`\w`、`\s` 与 POSIX 字符类默认也只认 ASCII，要 Unicode 语义必须在模式最前面加 `(*UCP)`（和 PHP 的 `/u` 顺带打开 UCP 正好相反，官方原话是"In UTF-8 mode the named character classes only match ASCII characters"）；`perl = TRUE` 会显著增加单次调用的固定开销，所以在紧密循环里要对小输入做批量向量化，而不是逐个元素调用。

📘 [R 4.6 · regex {base}（TRE 与 perl = TRUE）](https://stat.ethz.ch/R-manual/R-devel/library/base/html/regex.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 标准库**没有正则**：`std` 里没有 regex 模块，也没有 `std.regex`，只有 `std.mem`、`std.ascii`、`std.unicode`、`std.fmt` 这些字节与文本工具。因此 Zig 里的首要原则不是「怎么把正则写快」，而是「**不要自己手写一个正则状态机**」——手写解析器一旦处理回溯、Unicode、零宽断言，很快会变成一个比正则引擎本身还难维护、还容易有安全漏洞的组件。需要正则时正确做法是绑定 C 库：PCRE2 或 RE2 都有稳定的 C API，正好能用 `@cImport` 直接调用。

```zig
const std = @import("std");

pub fn main() !void {
    const text = "user_42@example.com";

    // ① 用 std.mem 做「固定分隔符」的活：零分配、无回溯、可审计
    const at = std.mem.indexOfScalar(u8, text, '@') orelse return error.NoAt;
    const user = text[0..at];
    const host = text[at + 1 ..];
    std.debug.print("user={s} host={s}\n", .{ user, host });   // user=user_42 host=example.com

    // ② stripPrefix / tokenizeScalar / splitScalar 覆盖大部分「原来想用正则」的场景
    if (std.mem.startsWith(u8, host, "example.")) {
        std.debug.print("domain ok\n", .{});                    // domain ok
    }
    var it = std.mem.tokenizeScalar(u8, "a,b,,c", ',');
    while (it.next()) |piece| std.debug.print("[{s}]", .{piece});  // [a][b][c]
    std.debug.print("\n", .{});

    // ③ 字符类判断用 std.ascii，显式、无隐藏分配
    std.debug.print("{}\n", .{std.ascii.isDigit('7')});         // true
    std.debug.print("{}\n", .{std.ascii.isAlphanumeric('_')});  // false（下划线不是 alnum）

    // ④ 真要正则：链接 PCRE2/RE2，用 @cImport 调它们的 C API
    // const c = @cImport({ @cInclude("pcre2.h"); });
    // 这样超时、match_limit、depth_limit 都由 PCRE2 提供（pcre2_set_match_limit 等）
    _ = std.unicode;
}
```

上面四步能覆盖绝大多数「看起来需要正则」的需求：固定分隔符切分用 `std.mem.splitScalar`/`tokenizeScalar`，前缀后缀判断用 `std.mem.startsWith`/`endsWith`，子串查找用 `std.mem.indexOf`，字符分类用 `std.ascii` 系列；这些函数的复杂度都是线性的，且不分配内存。⚠️ 明确不该做的是：用 `std.mem` 拼一个带量词与回溯的迷你引擎、用 `while` 循环加递归去模拟 `.*` 的贪婪匹配、或者为了「通用性」把 Zig 代码里所有字符串处理都塞进一个自研 DSL——这几条路最终都会遇到同样的三个问题（指数级回溯、Unicode 边界错误、栈溢出），而且没有任何工具链能帮你发现。如果确实需要正则的表达力（环视、反向引用、Unicode 属性），请直接绑定 PCRE2，并同时使用它提供的 `pcre2_set_match_limit`、`pcre2_set_depth_limit`、`pcre2_set_heap_limit` 作为刹车。

📘 [Zig 文档 · std.mem（标准库参考）](https://ziglang.org/documentation/master/std/#std.mem)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的 `string.find`、`string.match`、`string.gmatch`、`string.gsub` 用的是 **Lua pattern，不是正则**：没有 `|` 交替、没有环视、没有 `\d`、没有命名组，量词也少（只有 `*`、`+`、`-`、`?`）。它有几条自己的规则必须记牢：`-` 才是非贪婪（`*`、`+`、`?` 都是贪婪），`%b` 匹配配对结构，`%f` 是 frontier 模式，`%1`-`%9` 写在模式里就是反向引用（引用前面捕获到的子串，注意 `%0` 在模式里非法，它只在替换串里有意义）。正因为没有交替与环视这类组合爆炸的构造，Lua pattern 在常见场景下性能可预测，但 `.-` 与带反向引用的模式仍然可能退化。

```lua
-- ① 固定分隔符与子串：明显比 pattern 快，也不会有回溯问题
print(string.find("a.b.c", ".", 1, true))         -- 2 2（第 4 个参数 true 表示纯文本，不解释 pattern）
print(string.find("a.b.c", "."))                  -- 1 1（不加 true 时 . 是通配符）

-- ② - 才是非贪婪；* 是贪婪
print(string.match("axxbxxb", "a.*b"))            -- axxbxxb
print(string.match("axxbxxb", "a.-b"))            -- axxb

-- ③ %b 匹配配对括号，这是 Lua 独有的能力
print(string.match("f(a(b)c)z", "%b()"))          -- (a(b)c)

-- ④ %f 前后缀模式：匹配「从非字母进入字母」的边界
print(string.match("  hello", "%f[%a]%a+"))       -- hello

-- ⑤ 捕获、替换与模式内的反向引用
print(string.gsub("k=v", "(%w+)=(%w+)", "%2=%1")) -- v=k 1
print(string.match("abcabc", "(abc)%1"))          -- abc（%1 引用第 1 个捕获，模式里合法）

-- ⑥ 大文本上避免用 .- 反复扫描；能用显式字符类就别用通配符
local n = 0
for _ in string.gmatch(string.rep("ab", 50000), "a") do n = n + 1 end
print(n)                                          -- 50000
```

Lua pattern 的性能特征与标准回溯引擎不同：它实现的是一个带回溯的简单匹配器，但语法里没有交替与环视，`(a+)+$` 这类靠交替嵌套堆出来的经典炸弹很难表达；不过 `%1`-`%9` 反向引用会让匹配重新变成非正则问题，所以真正需要警惕的是两类形状——`.-` 在大文本里反复扫描，以及带多个捕获加反向引用的模式（它们没有自动机那套线性时间保证）；此外 `gsub` 里用函数做替换时的闭包分配也要算进开销。⚠️ 从别的语言迁移过来时最容易犯的四个错：误以为 `|` 是交替（Lua 里它是字面竖线，要用 `%|` 转义）；误以为 `+`/`*` 默认非贪婪（要显式写 `-`）；误以为 `\d`、`\w`、`\s` 存在（要用 `%d`、`%w`、`%s`，且大小写语义相反）；误以为 Lua 没有反向引用（`%1`-`%9` 写在模式里就引用前面捕获的子串，例如 `string.match("abcabc", "(abc)%1")` 得到 `abc`；而替换串里的 `%1`-`%9` 是「取第 n 个捕获」，`%0` 才是整段匹配，两处含义要分清）。需要真正的正则时应引 `lrexlib`（绑定 PCRE/Oniguruma）或 `lpeg`（PEG，无回溯），不要试图用 Lua pattern 模拟。

📘 [Lua 5.5 手册 · Patterns（§6.5.1）](https://www.lua.org/manual/5.5/manual.html#6.5.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `RegExp` 类型就是 JavaScript 运行时那个 `RegExp`：ECMAScript 规定的回溯引擎，因此灾难性回溯与 ReDoS 的结论与 JS 完全一致，**运行时没有超时 API**。TypeScript 这一层唯一相关的事情是「类型定义跟不跟得上」：`RegExp.escape` 属于 ES2025，需要 `lib` 配到 `es2025`（或更新的 `esnext`）才有类型声明，而这个 lib 目标是 **TypeScript 6.0 才新增的**，6.0 起 `target` 也接受 `es2025`；`v` 标志（unicodeSets）属于 ES2024，`d` 标志（indices）属于 ES2022。类型缺了不代表运行时没有，只代表编译器不认。

```typescript
// tsconfig: "target": "es2025", "lib": ["es2025", "dom"]

// ① ES2025：RegExp.escape 有类型，且返回值可以安全拼进模式
const userInput = "a+b*c";
const re = new RegExp(`^${RegExp.escape(userInput)}$`);
console.log(re.test("a+b*c"));                    // true
console.log(RegExp.escape("a.b*c"));              // \x61\.b\*c

// ② ES2024：v 标志支持集合运算（并、交、差）
console.log(/[\p{ASCII}&&\p{Letter}]/v.test("A"));   // true
// ③ ES2022：d 标志给出每个捕获组的下标
console.log(/(b)(c)/d.exec("abc")!.indices);      // [ [1,3], [1,2], [2,3], groups: undefined ]

// ④ 陷阱：g 标志是有状态的，lastIndex 会跨调用残留
const g = /\d/g;
console.log(g.exec("a1b2")!.index, g.lastIndex);  // 1 2
console.log(g.exec("a1b2")!.index, g.lastIndex);  // 3 4
console.log(g.exec("a1b2"), g.lastIndex);         // null 0（匹配失败后自动重置）
const st = /\d/g;
console.log(st.test("a1"), st.test("a1"));   // true false ← 同一个对象复用 test 的经典坑
// 正确做法：要么每次新建字面量，要么用 matchAll / 手动把 lastIndex 归零
console.log([..."a1b2".matchAll(/\d/g)].length);  // 2

// ⑤ \d 永远是 ASCII，Unicode 要用 \p{...} 且必须带 u/v 标志
console.log(/\d/.test("٣"), /\p{Nd}/u.test("٣"));  // false true
```

把 `RegExp` 对象存在模块级常量里是 JS 的常见优化（避免每次调用重新解析模式），但一旦带 `g` 或 `y` 标志，这个对象就变成有状态的：`lastIndex` 会在两次 `exec` 之间保留，甚至 `test` 也会推进它，于是「第二次调用返回 false」这种 bug 就出现了。安全写法是：需要遍历时用 `matchAll`（它内部会克隆正则、不污染原对象）、或者每次用字面量新建、或者在 `exec` 返回 `null` 后确认 `lastIndex` 已归零。⚠️ 另外三个默认语义要对照记忆：`^`/`$` 只在整串首尾匹配，多行要加 `m`；`.` 默认不匹配换行（`\n`、`\r`、`\u2028`、`\u2029`），要匹配全部加 `s`；`\d`/`\w` 是纯 ASCII，只有显式写 `\p{Nd}`、`\p{L}` 并开启 `u`（或 `v`）才是 Unicode 语义。TypeScript 从 5.5 起会检查正则**字面量**的语法（能报出未转义的 `)`、不存在的反向引用、命名组等特性与 `target` 不匹配这类问题），但它的检查只覆盖字面量：`new RegExp("...")` 里的字符串不会被检查，灾难性回溯这类运行时性能问题更不在检查范围内，所以模式一旦来自字符串拼接，还是只能靠测试和输入限制兜底。

📘 [MDN · RegExp.escape（ES2025，含转义规则）](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `RegExp` 由 ECMAScript 规范定义，实现必须是回溯引擎（V8 的 Irregexp 就是），所以它是 ReDoS 的经典受害者：`^([A-Za-z]+)+$` 在 24 个字符上要 425 毫秒，25 个字符就直接卡死到超时。Node 里**没有任何正则超时 API**，唯一可靠的刹车是把匹配放进 Worker 线程，主线程超时后 `terminate()` 掉它——`AbortSignal` 无法抢占同步执行的正则，这一点必须说清楚。

```javascript
// 主线程：用 Worker 隔离炸弹，超时就 terminate
import { Worker } from "node:worker_threads";

function testWithTimeout(pattern, input, ms) {
  return new Promise((resolve) => {
    const w = new Worker(new URL("./regex-worker.mjs", import.meta.url), {
      workerData: { pattern, input },
    });
    const timer = setTimeout(async () => {
      await w.terminate();                       // 真正杀掉正在回溯的线程
      resolve("TIMEOUT");
    }, ms);
    w.on("message", async (m) => { clearTimeout(timer); await w.terminate(); resolve(m); });
  });
}

console.log(await testWithTimeout("^([A-Za-z]+)+$", "A".repeat(25) + "!", 200));  // TIMEOUT
console.log(await testWithTimeout("^[A-Za-z]+$",     "A".repeat(25) + "!", 200));  // false

// regex-worker.mjs：
// import { workerData, parentPort } from "node:worker_threads";
// const re = new RegExp(workerData.pattern);
// parentPort.postMessage(re.test(workerData.input));

// 反例：同步阻塞时 AbortSignal 完全无效
const re2 = /^([A-Za-z]+)+$/;
try {
  await new Promise((res, rej) => {
    const t = setTimeout(() => rej(new Error("aborted")), 150);
    re2.test("A".repeat(25) + "!");              // 同步阻塞，定时器回调没有机会执行
    clearTimeout(t);
    res();
  });
  console.log("同步 test 结束");
} catch {
  console.log("AbortSignal 无法抢占同步正则");
}
```

Node 里防 ReDoS 的实际策略分三层。第一层是模式层：把嵌套量词压平（`([A-Za-z]+)+` → `[A-Za-z]+`）、用原子组式的写法规避、给量词加上更严格的字符类；第二层是输入层：在进正则之前按业务上限截断，通常「字段长度不超过 1 KB」这一条就能挡掉绝大多数炸弹；第三层是隔离层：确有必要匹配用户提供的模式或极长输入时，放进 `worker_threads`（或 `child_process`）并设硬性超时，因为只有独立线程/进程被杀掉才能真正停止回溯。⚠️ 除了 ReDoS，JS 还有三个高频陷阱：带 `g`/`y` 的 `RegExp` 对象是有状态的（`lastIndex` 残留导致 `test` 第二次返回 `false`），共享一个模块级 `RegExp` 时尤其危险；`^`/`$` 默认只匹配整串首尾，多行要 `m`（与之相反，Ruby 的 `^`/`$` 默认就是行锚点）；`\d`/`\w` 是 ASCII，Unicode 属性必须用 `\p{...}` 且带 `u` 标志。另外 `RegExp.escape`（ES2025，Node 26 已内建）是拼接用户输入的正确工具，手写 `replace(/[.*+?^${}()|[\]\\]/g, "\\$&")` 会漏掉 `/` 与部分边界字符。

📘 [MDN · 正则表达式（回溯、标志与 Unicode 语义）](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 `preg_*` 系列绑定 PCRE2，是回溯引擎，但它自带两道运行时闸门：`pcre.backtrack_limit`（默认 1000000）限制回溯步数，`pcre.recursion_limit`（默认 100000）限制递归深度，超限时函数返回 `false` 并把 `preg_last_error()` 设成 `PREG_BACKTRACK_LIMIT_ERROR` 或 `PREG_RECURSION_LIMIT_ERROR`。这意味着 PHP 不会像 Java/Python 那样无声地烧 CPU，但错误是「静默失败」——不检查返回值就会把 `false` 当成「不匹配」。另外 `pcre.jit` 默认开启，可以整体关掉来回避 JIT 栈限制类的怪异错误。

```php
<?php
// ① 默认闸门值（php.ini 可改，也可用 ini_set 在运行时调整）
echo ini_get('pcre.backtrack_limit'), ' ', ini_get('pcre.recursion_limit'), ' ', ini_get('pcre.jit'), "\n";
// 1000000 100000 1

// ② 触发回溯上限：嵌套量词 + 失败输入
ini_set('pcre.backtrack_limit', '10000');            // 调小便于演示
$r = preg_match('/^([A-Za-z]+)+$/', str_repeat('A', 30) . '!');
var_dump($r);                                        // bool(false) ← 不是"不匹配"，而是出错
echo preg_last_error() === PREG_BACKTRACK_LIMIT_ERROR ? "backtrack limit\n" : "other\n";
// backtrack limit

// ③ 必须区分「不匹配」和「出错」：返回值 false 且 preg_last_error() != 0 才是出错
ini_set('pcre.backtrack_limit', '1000000');
$m = preg_match('/^[A-Za-z]+$/', str_repeat('A', 30) . '!');
var_dump($m);                                        // int(0) ← 真正的不匹配
echo preg_last_error() === PREG_NO_ERROR ? "no error\n" : "error\n";   // no error

// ④ preg_last_error() 的 7 个错误常量：PREG_NO_ERROR、PREG_INTERNAL_ERROR、
//    PREG_BACKTRACK_LIMIT_ERROR、PREG_RECURSION_LIMIT_ERROR、PREG_BAD_UTF8_ERROR、
//    PREG_BAD_UTF8_OFFSET_ERROR、PREG_JIT_STACKLIMIT_ERROR

// ⑤ 缓存：ext/pcre 自己维护编译缓存（每线程一个，上限 4096 条且不可配置），
//    但缓存键是「模式串 + 标志」，循环里动态拼出来的新字符串照样要重新编译
define('WORD_RE', '/\w+/');
preg_match_all(WORD_RE, 'hi there', $out);
print_r($out[0]);                                    // Array ( [0] => hi [1] => there )
```

PHP 的这套限制机制带来一个非常实际的编码要求：**每一次 `preg_*` 调用都要检查返回值与 `preg_last_error()`**。`preg_match` 的三态是 1（匹配）、0（不匹配）、`false`（出错），把 `false` 当 0 用会让「回溯超限」悄悄变成「格式校验不通过」，从而放过非法输入或拒绝合法输入。`pcre.recursion_limit` 还要小心文档里明确警告的那一点：调得太高可能耗尽进程栈并直接让 PHP 崩溃，因为它限制的是 PCRE 的递归深度，而递归深度对应真实的 C 栈消耗。⚠️ PHP 8.5 打包的是 PCRE2 10.44，UPGRADING 里 PCRE 一节只有一条行为变更：扩展改为在不启用半废弃的 `PCRE2_EXTRA_ALLOW_LOOKAROUND_BSK` 编译选项的情况下构建（这会影响某些在环视内部使用 `\K` 的模式），`preg_*` 的函数签名与常量没有变化。另外 PHP 的编译缓存是 ext/pcre 自己维护的：PHP 手册写明「每个线程一个专用缓存，最多容纳 4096 条」，且「缓存大小不可配置」（PCRE2 本身不缓存编译结果，缓存表是 PHP 建的，条目超出上限时按最旧且未在使用中的顺序淘汰）。这个上限比 Python 的 512 条、.NET 的 15 条都大，也没有公开可调的 API；所以最省事也最稳妥的写法仍然是把模式定义成 `const` 或静态属性，避免在循环里动态拼接模式字符串（每次拼接都会产生新的模式串，缓存键随之变化，从而触发重新编译甚至挤掉热点模式）。

📘 [PHP 手册 · PCRE 运行时配置（backtrack_limit / recursion_limit / jit）](https://www.php.net/manual/en/pcre.configuration.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用的是 Onigmo（Oniguruma 的分支），属于回溯引擎，但 Ruby 3.2 起加了两件别家没有的工具：`Regexp.timeout`（全局或按实例设置匹配超时，超时抛 `Regexp::TimeoutError`）与 `Regexp.linear_time?`（判断某个模式是否满足线性时间保证）。`Regexp.timeout` **默认为 `nil`**，也就是默认不超时，必须显式设置才生效；`Regexp.linear_time?` 对反向引用返回 `false`，对普通的嵌套量词模式则返回 `true`，这说明 Onigmo 对多数模式已经能在不回溯爆炸的前提下求解。

```ruby
# ① 引擎与默认状态
puts RUBY_ENGINE, RUBY_VERSION          # ruby 4.0.6
puts Regexp.timeout.inspect             # nil ← 默认不超时

# ② 哪些模式没有线性时间保证
[%q{(a)\1}, %q{(?<=a)b}, %q{([A-Za-z]+)+$}].each do |p|
  puts "#{p} linear=#{Regexp.linear_time?(p)}"
end
# (a)\1 linear=false          ← 反向引用
# (?<=a)b linear=true
# ([A-Za-z]+)+$ linear=true   ← 经典炸弹形状也满足线性时间保证

# ③ 线性时间保证在实测上也成立：100 万字符仍在线性范围内
re = /\A([A-Za-z]+)+\z/
[100, 10_000, 1_000_000].each do |n|
  s = "A" * n + "!"
  t = Time.now
  re =~ s
  puts "#{n} #{(Time.now - t).round(5)}s"
end
# 100 1.0e-05s / 10000 0.00049s / 1000000 0.05952s

# ④ 按实例设置超时
begin
  slow = Regexp.new(%q{\A(a+)+\1z\z}, timeout: 0.002)   # 反向引用，不在线性时间范畴
  slow =~ ("a" * 60) + "!"
rescue Regexp::TimeoutError
  puts "per-instance: Regexp::TimeoutError"
end

# ⑤ 全局超时：影响之后新建的所有 Regexp，也约束 =~ 这类内建操作
Regexp.timeout = 0.001
begin
  ("a" * 200) =~ /\A(a+)+\1z\z/
rescue Regexp::TimeoutError
  puts "global: Regexp::TimeoutError"
ensure
  Regexp.timeout = nil                  # 记得还原，默认是不超时
end

# ⑥ 缓存：Ruby 的字面量 /.../ 在解析期就编译好并按对象缓存，不会每次重新编译
WORD = /\w+/
puts "hi there".scan(WORD).inspect       # ["hi", "there"]
```

Ruby 的这套设计让「防 ReDoS」有了语言级答案：先用 `Regexp.linear_time?` 在开发期筛掉不满足线性时间的模式（主要是带反向引用的），再给剩余的高风险模式配 `Regexp.timeout`，最后在全局设一个宽松的兜底值。实测中 `\A(a+)+\1z\z` 这类含反向引用的模式才是真正需要超时兜底的形状，而 `([A-Za-z]+)+$` 这种在其他语言里必然爆炸的模式，Onigmo 在 100 万字符的失败输入上只要 0.06 秒且保持线性——所以不要把 Python/Java 的经验直接套到 Ruby 上，先测 `Regexp.linear_time?` 再决定要不要设超时。⚠️ 两个使用上的注意点：`Regexp.timeout` 是全局可变状态，在库代码里改它会影响同进程的其他代码，设置后必须在 `ensure` 里还原；`Regexp.linear_time?` 的签名是 `Regexp.linear_time?(re)` 与 `Regexp.linear_time?(string, options = 0)`，`Regexp` 对象和模式字符串都收（传 `Regexp` 不会抛 `ArgumentError`），它判断的是「该模式是否存在线性时间的匹配算法」，返回 `true` 不等于「实测一定快」，仍然要以基准测试为准。Ruby 的正则字面量在解析阶段完成编译并按对象缓存，所以热路径里写 `/.../` 是安全的，而 `Regexp.new(动态字符串)` 每次都会重新编译。

📘 [Ruby 4.0 · Regexp（timeout、linear_time?、TimeoutError）](https://docs.ruby-lang.org/en/4.0/Regexp.html)

{{% /tab %}}

{{< /tabpane >}}

**最后，什么场景不该用正则。** 第一类是嵌套结构，HTML, XML, JSON, YAML 里的括号与引号可以任意深度地互相嵌套，正则引擎没有计数器，无法保证左右配对，用正则去匹配标签或对象边界迟早会在畸形或深层输入上出错。第二类是需要递归或上下文无关文法的结构，例如表达式求值, 括号配平, 缩进敏感的层级，正则只能描述正则语言，这类问题必须交给递归下降解析器或现成的语法分析器。第三类是纯字符串切分，只要存在稳定的定界符，`split` 或语言自带的切分函数就比正则更快也更清楚，正则在这里只会白白付出编译和回溯的代价。换句话说，解析器负责理解结构，切分函数负责拆开文本，正则只负责在扁平的、没有嵌套语义的文本里描述模式。

| 语言 | 替代 HTML/XML | 替代 JSON | 无正则时的字符串处理 |
| --- | --- | --- | --- |
| Rust | `scraper`, `quick-xml` | `serde_json` | `str::split`, `str::split_once` |
| Swift | `XMLParser`（Foundation） | `JSONDecoder`（Foundation） | `String.split(separator:)`, `hasPrefix` |
| Go | `encoding/xml` | `encoding/json` | `strings.Split`, `strings.Cut` |
| Python | `html.parser`, `lxml` | `json` | `str.split`, `str.removeprefix` |
| Kotlin | `jsoup` | `kotlinx.serialization.json` | `String.split`, `String.substringBefore` |
| Java | `jsoup` | `Jackson`, `Gson` | `String.split`, `String.indexOf` |
| C++ | `libxml2`, `pugixml` | `nlohmann/json`, `JsonCpp` | `std::string::find`, `std::string_view::substr` |
| C | `libxml2` | `cJSON`, `jansson` | `strtok`, `strchr` |
| Julia | `EzXML.jl` | `JSON.jl`（官方注册表常用） | `split`, `startswith` |
| C# | `System.Xml`, `HtmlAgilityPack` | `System.Text.Json` | `String.Split`, `String.StartsWith` |
| Dart | `package:html` | `dart:convert` 的 `jsonDecode` | `String.split`, `String.startsWith` |
| R | `xml2` | `jsonlite` | `strsplit`, `substr` |
| Zig | 无标准库，用 C 互操作 | `std.json` | `std.mem.splitScalar`, `std.mem.tokenizeScalar` |
| Lua | 无内建，用 `luaexpat` 或 C 互操作 | 无内建，用 `dkjson`, `cjson` | `string.find`, `string.gsub` |
| TypeScript | `DOMParser`, `parse5` | `JSON.parse`（内建） | `String.prototype.split`, `String.prototype.startsWith` |
| JavaScript | `DOMParser`, `parse5` | `JSON.parse`（内建） | `String.prototype.split`, `String.prototype.startsWith` |
| PHP | `DOMDocument` | `json_decode` | `explode`, `str_starts_with` |
| Ruby | `Nokogiri` | `JSON.parse` | `String#split`, `String#start_with?` |

统计口径说明：表中每门语言都给出三类替代各 1 个条目，共 3 个条目，因此横向可直接比较同一门语言在这三类任务上的首选工具。选择原则是：HTML/XML 一列列出的第三方库在该语言生态中属于事实标准，能覆盖绝大多数文档解析需求，语言自带解析器时优先写自带的；JSON 一列优先给语言内建或官方推荐的实现，没有内建的（如 Lua）明确写出这一点并给出常见第三方库；字符串处理一列只列基础包或标准库中可直接调用的函数，不引入额外依赖。使用原则是：能用定界符切分就不要用正则，能用 `starts_with` 或 `indexOf` 判断就不要用正则，需要嵌套结构就引入解析器，只有在模式确实有歧义, 需要量词或字符类描述时才动用正则，并优先选本语言里线性时间的那套引擎。
