+++
title = "42-regex"
date = 2026-07-28T14:49:00+08:00
weight = 420
type = "docs"
description = "面向 Go 用户讲清 regex crate、编译复用、捕获替换、与 RE2/字符串 API 分工"
isCJKLanguage = true
draft = false

+++

# 正则表达式 (Regular Expressions)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会想直接 `use regex` 却发现标准库没有正则，不知道该用哪个 crate？
- 你是否每次匹配都 `Regex::new`，热路径又慢又吵编译错误？
- 你是否分不清 `is_match` / `find` / `captures`，以及命名捕获、`replace` 怎么写？
- 你会不会把 Perl/PCRE 写法原样搬过来，结果 Rust `regex` 直接拒绝？
- 你是否想对照 Go 的 `regexp`（RE2 风格），或知道何时该用 `split`/`contains` 而不是正则？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| regex | regular expression | 正则表达式 | 用模式描述字符串集合的微型语言 | `regexp` |
| `regex` crate | — | Rust 正则库 | 生态默认、保证线性时间的正则实现 | `regexp` 包 |
| DFA | Deterministic Finite Automaton | 确定有限自动机 | 一类可保证线性扫描的匹配引擎 | RE2 的思路之一 |
| RE2 | — | Google RE2 引擎 | 禁回溯、强调安全性的正则实现 | Go `regexp` 基于 RE2 |
| PCRE | Perl Compatible Regular Expressions | Perl 兼容正则 | 功能很全、常含回溯的经典方言 | 部分第三方库 |
| capture | — | 捕获组 | 匹配中抽出的子串（编号或命名） | `Subexp` / `FindStringSubmatch` |
| LazyLock | — | 懒初始化锁 | 首次访问时初始化，之后只读共享 | `sync.Once` + 包级变量 |
| haystack | — | 干草堆/被搜文本 | 要在其上匹配的字符串或字节 | 被 `Find` 的输入 |
| backtracking | — | 回溯 | 失败后回退重试路径；可导致超线性耗时 | RE2 刻意避免 |
| `bytes` API | — | 字节串匹配 | 在 `&[u8]` 上匹配，不强制 UTF-8 | `[]byte` + `regexp` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q6](#q6), [Q7](#q7), [Q11](#q11), [Q12](#q12) |
| `common` | [Q4](#q4), [Q5](#q5), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q13](#q13) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. 为什么要用 `regex` crate，而不是标准库？ {#q1}
**Tags:** `hot` `beginner` `regex` `crate`
**适用版本:** `regex` crate（生态默认）；Rust 标准库不提供正则

**一句话答案：**
Rust **标准库没有**正则表达式 API；社区默认用 **`regex` crate**（正则库）：保证线性时间、API 清晰、文档成熟。对标 Go 的 `regexp` 包，只是 Rust 把它放在 crates.io 而不是 `std`。

**解答：**
加依赖：

```toml
[dependencies]
regex = "1"
```

最小用法（text，需依赖）：

```text
use regex::Regex;

fn main() {
    let re = Regex::new(r"\d+").unwrap();
    assert!(re.is_match("abc123"));
}
```

无依赖时，字符串“子串/前缀”用标准库就够（不必硬上正则）：

```rust
fn main() {
    let s = "abc123";
    assert!(s.contains("123"));
    assert!(s.starts_with("abc"));
    println!("{s}");
}
```

选型直觉：

| 需求 | 选择 |
|------|------|
| 固定子串 / 前缀 / 空白切分 | `str` API（见 [Q12](#q12)、[14-strings-and-text](14-strings-and-text.md)） |
| 模式匹配、捕获、替换 | `regex` crate |
| 要“完整 Perl/PCRE”方言 | 先看 [Q6](#q6)；通常不要强求 |

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	re := regexp.MustCompile(`\d+`)
	fmt.Println(re.MatchString("abc123"))
}
```

- **Go 怎么做**：标准库就有 `regexp`。
- **Rust 为什么不同**：`std` 保持精简；正则放在独立 crate，版本与功能可独立演进。
- **Go 程序员易踩的坑**：搜 `std::regex` 或以为像 C++ `<regex>` 那样在标准库里。

**记忆点：**
- 正则 → `regex` crate，不是 `std`。
- 简单子串 → 先想 `contains` / `split`。

---

## Q2. 为什么要“编译一次”，还常用 `LazyLock`？ {#q2}
**Tags:** `hot` `beginner` `LazyLock` `Regex::new`
**适用版本:** `regex` 1.x；`std::sync::LazyLock` 需 Rust 1.80+

**一句话答案：**
`Regex::new` 会解析并编译模式，有成本；热路径上应**编译一次、反复使用**。包级常量场景用 **`LazyLock`**（懒初始化锁：首次访问时初始化，之后共享只读）包住 `Regex`，对标 Go 的包级 `MustCompile` + `sync.Once` 直觉。

**解答：**
「❌ 错误写法」——每次调用都编译：

```text
fn has_digit(s: &str) -> bool {
    // 每次 new：重复解析模式，热路径浪费
    Regex::new(r"\d+").unwrap().is_match(s)
}
```

「✅ 正确写法」——函数内复用局部编译结果，或用 `LazyLock` 做全局一次：

```text
use std::sync::LazyLock;
use regex::Regex;

static DIGIT: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\d+").unwrap());

fn has_digit(s: &str) -> bool {
    DIGIT.is_match(s)
}
```

`once_cell::sync::Lazy` 是旧生态常见写法；Rust 1.80+ 优先 `std::sync::LazyLock`。

无依赖对照：编译期能确定的“模式”若只是字面量子串，根本不必 `Regex`：

```rust
fn main() {
    let needle = "err";
    assert!("error: boom".contains(needle));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

var digit = regexp.MustCompile(`\d+`)

func HasDigit(s string) bool {
	return digit.MatchString(s)
}

func main() {
	fmt.Println(HasDigit("ab12"))
}
```

- **Go 怎么做**：包级 `MustCompile` 很常见。
- **Rust 为什么不同**：`Regex` 不是 `const` 可构造；用 `LazyLock` / `OnceLock` 表达“进程内只建一次”。
- **Go 程序员易踩的坑**：把 `Regex::new` 塞进每个请求处理器里当本地变量反复创建。

**记忆点：**
- 热路径：一次 `Regex::new`，多次 `is_match`/`find`。
- 包级：`LazyLock<Regex>`。

---

## Q3. `is_match`、`find`、`captures` 怎么选？ {#q3}
**Tags:** `hot` `beginner` `is_match` `find` `captures`
**适用版本:** `regex` 1.x

**一句话答案：**
只要是/否 → `is_match`；要整段匹配的起止与文本 → `find` / `find_iter`；要分组子串 → `captures` / `captures_iter`。

**解答：**

```text
use regex::Regex;

fn demo(hay: &str) {
    let re = Regex::new(r"(\w+)@(\w+)").unwrap();

    // 1) 是否匹配
    assert!(re.is_match(hay));

    // 2) 整段匹配（不含分组细节）
    if let Some(m) = re.find(hay) {
        // m.as_str() / m.start() / m.end()
        let _ = m.as_str();
    }

    // 3) 捕获组：0 = 整段，1.. = 各括号
    if let Some(c) = re.captures(hay) {
        let _user = c.get(1).map(|m| m.as_str());
        let _host = c.get(2).map(|m| m.as_str());
    }
}
```

和“只找固定子串”对比（无依赖）：

```rust
fn main() {
    let hay = "user@host";
    assert!(hay.contains('@'));
    if let Some(i) = hay.find('@') {
        println!("at byte {i}");
    }
}
```

`find_iter` / `captures_iter` 用于多处匹配；只要布尔结果别无谓建 `Captures`。

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	re := regexp.MustCompile(`(\w+)@(\w+)`)
	fmt.Println(re.MatchString("a@b"))
	fmt.Println(re.FindString("a@b"))
	fmt.Println(re.FindStringSubmatch("a@b"))
}
```

- **Go 怎么做**：`MatchString` / `FindString` / `FindStringSubmatch`。
- **Rust 为什么不同**：拆成 `is_match` / `find` / `captures`，类型更明确（`Match` vs `Captures`）。
- **Go 程序员易踩的坑**：一律 `captures` 再丢弃分组，多分配、多工作。

**记忆点：**
- 是否 → `is_match`；位置/整段 → `find`；分组 → `captures`。

---

## Q4. 命名捕获怎么写、怎么取？ {#q4}
**Tags:** `common` `intermediate` `named-capture`
**适用版本:** `regex` 1.x

**一句话答案：**
用 `(?P<name>...)`（或文档支持的命名语法）声明；用 `captures.name("name")` 取出。比硬记编号更稳，尤其模式会改时。

**解答：**

```text
use regex::Regex;

fn parse_pair(s: &str) -> Option<(String, String)> {
    let re = Regex::new(r"(?P<key>\w+)=(?P<val>\w+)").unwrap();
    let c = re.captures(s)?;
    Some((
        c.name("key")?.as_str().to_string(),
        c.name("val")?.as_str().to_string(),
    ))
}
```

编号仍可用：`c.get(1)`；命名适合对外协议字段、日志解析。

无依赖时，极简 `k=v` 不必上正则：

```rust
fn main() {
    let s = "key=val";
    let (k, v) = s.split_once('=').unwrap();
    assert_eq!((k, v), ("key", "val"));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	re := regexp.MustCompile(`(?P<key>\w+)=(?P<val>\w+)`)
	m := re.FindStringSubmatch("a=b")
	names := re.SubexpNames()
	fmt.Println(m, names)
}
```

- **Go 怎么做**：同样支持 `(?P<name>...)`，再用 `SubexpNames` 对齐下标。
- **Rust 为什么不同**：`name("key")` 直接按名取，少自己维护 name→index 表。
- **Go 程序员易踩的坑**：只记编号，模式插入一组后全盘错位。

**记忆点：**
- 声明：`(?P<name>...)`；读取：`captures.name("name")`。
- 简单分隔优先 `split_once`。

---

## Q5. `replace` / `replace_all` 怎么用？ {#q5}
**Tags:** `common` `replace`
**适用版本:** `regex` 1.x

**一句话答案：**
`replace` 换第一处，`replace_all` 换全部；替换串里可用 `$1` / `$name` 引用捕获。固定子串替换优先 `str::replace`，不必编译正则。

**解答：**

```text
use regex::Regex;

fn redact_emails(s: &str) -> String {
    let re = Regex::new(r"\b\w+@\w+\.\w+\b").unwrap();
    re.replace_all(s, "[email]").into_owned()
}

fn swap_pair(s: &str) -> String {
    let re = Regex::new(r"(?P<a>\w+)-(?P<b>\w+)").unwrap();
    re.replace(s, "$b-$a").into_owned()
}
```

固定字面量（无依赖）：

```rust
fn main() {
    let s = "foo-bar-foo";
    assert_eq!(s.replace("foo", "x"), "x-bar-x");
    assert_eq!(s.replacen("foo", "x", 1), "x-bar-foo");
}
```

`Regex::replace` 返回 `Cow<str>`：无改动时可借用原串，有改动则拥有 `String`；要 `String` 时 `.into_owned()`。

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	re := regexp.MustCompile(`\d+`)
	fmt.Println(re.ReplaceAllString("a1b2", "#"))
}
```

- **Go 怎么做**：`ReplaceAllString` / `ReplaceAllStringFunc`。
- **Rust 为什么不同**：`replace` vs `replace_all` 分开；字面量替换走 `str` 方法。
- **Go 程序员易踩的坑**：字面量全局替换也写正则，白白编译模式。

**记忆点：**
- 模式替换 → `regex` 的 `replace(_all)`。
- 字面量 → `str::replace` / `replacen`。

---

## Q6. 为什么说 Rust `regex` 不是完整 PCRE？ {#q6}
**Tags:** `hot` `intermediate` `PCRE` `backtracking`
**适用版本:** `regex` 1.x

**一句话答案：**
`regex` crate 走 **RE2/线性时间**路线，刻意不支持完整 **PCRE**（Perl Compatible Regular Expressions，Perl 兼容正则）里一批依赖**回溯**（backtracking）的特性（如任意环视、反向引用做复杂匹配等）。换来的是：恶意或含糊模式更不容易把 CPU 打满。

**解答：**
你会在文档/报错里看到“不支持某某特性”——这不是 bug，是引擎边界。需要“完整 Perl 方言”时，要换别的 crate 并**自己承担**回溯风险与安全审计，而不是抱怨 `regex` “不全”。

概念对照（text）：

```text
PCRE 风格（很多语言默认）：功能全，常含回溯 → 最坏情况可超线性
Rust regex / Go regexp：偏 RE2 → 优先保证匹配时间与输入长度大致成线性
```

无依赖侧：复杂校验若只是“固定格式”，手写解析往往更清晰：

```rust
fn is_three_digits(s: &str) -> bool {
    s.len() == 3 && s.bytes().all(|b| b.is_ascii_digit())
}

fn main() {
    assert!(is_three_digits("123"));
    assert!(!is_three_digits("4a2"));
}
```

**Go 对比：**
- **Go 怎么做**：标准 `regexp` 也是 RE2 风格，同样不是完整 PCRE。
- **Rust 为什么不同**：和 Go 站同一边；和“Perl/Python 默认正则直觉”可能不同。
- **Go 程序员易踩的坑**：从 Python/`re` 或 JS 复制带 `(?<=...)` 等写法，两边都会炸——先查引擎支持表。

**记忆点：**
- `regex` ≈ 安全优先，不是 PCRE 全集。
- 缺特性时先问：是否该用手写解析，而不是换“更危险”的引擎。

---

## Q7. 和 Go `regexp` / RE2 怎么对照？ {#q7}
**Tags:** `hot` `beginner` `RE2` `Go`
**适用版本:** `regex` 1.x；Go 1.x `regexp`

**一句话答案：**
心智模型高度接近：**都偏 RE2**、强调线性时间、很多 PCRE 特性没有。API 名字不同，但 `Match`≈`is_match`，`Find`≈`find`，`Submatch`≈`captures`，包级 `MustCompile`≈`LazyLock`+`Regex::new`。

**解答：**

| Go | Rust `regex` |
|----|----------------|
| `regexp.Compile` / `MustCompile` | `Regex::new` / `Regex::new(...).unwrap()` |
| 包级 `MustCompile` | `LazyLock<Regex>`（见 [Q2](#q2)） |
| `MatchString` | `is_match` |
| `FindString` | `find` → `Match::as_str` |
| `FindStringSubmatch` | `captures` |
| `ReplaceAllString` | `replace_all` |
| `[]byte` API | `regex::bytes::Regex`（见 [Q8](#q8)） |

```text
// Rust
let re = Regex::new(r"foo|bar").unwrap();
assert!(re.is_match("bar"));
```

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	re := regexp.MustCompile(`foo|bar`)
	fmt.Println(re.MatchString("bar"))
}
```

**Go 对比：**
- **Go 怎么做**：标准库 `regexp`。
- **Rust 为什么不同**：同哲学，不同封装位置（crate vs std）。
- **Go 程序员易踩的坑**：以为 Rust 会更“Perl”，其实两边都偏 RE2。

**记忆点：**
- 从 Go 迁：改 API 名，少改引擎预期。
- 两端都不是完整 PCRE。

---

## Q8. 字节串上怎么匹配？和 `&str` 有什么差别？ {#q8}
**Tags:** `common` `bytes` `utf8`
**适用版本:** `regex` 1.x（`regex::bytes`）

**一句话答案：**
处理任意 `&[u8]`（可能非 UTF-8）用 **`regex::bytes::Regex`**；合法 Unicode 文本用普通 `regex::Regex`（`&str`）。别把非法 UTF-8 硬转 `String` 再匹配。

**解答：**

```text
use regex::bytes::Regex as BytesRegex;

fn has_ff_prefix(data: &[u8]) -> bool {
    // 示意：按字节语义写模式；具体元字符语义见 bytes 模块文档
    let re = BytesRegex::new(r"(?-u)\xFF\xD8").unwrap(); // 例：JPEG SOI 一类
    re.is_match(data)
}
```

UTF-8 文本路径：

```text
use regex::Regex;

fn has_word(s: &str) -> bool {
    Regex::new(r"\w+").unwrap().is_match(s)
}
```

无依赖：只查原始字节：

```rust
fn main() {
    let data: &[u8] = &[0xff, 0xd8, 0x00];
    assert_eq!(data[0], 0xff);
    assert!(data.starts_with(&[0xff, 0xd8]));
}
```

**Go 对比：**

```go
package main

import "regexp"

func main() {
	re := regexp.MustCompile(`\xff\xd8`)
	_ = re.Match([]byte{0xff, 0xd8})
}
```

- **Go 怎么做**：同一套 `regexp`，`Match([]byte)` / `MatchString`。
- **Rust 为什么不同**：`str` 与 `bytes` 分成两个类型模块，逼你想清楚 Unicode 假设。
- **Go 程序员易踩的坑**：对二进制缓冲用 `&str` 正则，先 `from_utf8` 失败或悄悄 lossy。

**记忆点：**
- 文本 → `regex::Regex`；原始字节 → `regex::bytes::Regex`。
- 固定魔数优先 `starts_with`，未必要正则。

---

## Q9. 性能上最该注意什么？ {#q9}
**Tags:** `common` `performance`
**适用版本:** `regex` 1.x

**一句话答案：**
**编译一次、复用 `Regex`**；避免在热循环里 `new`；能用字面量/`contains`/`split` 就别上正则；超大 haystack 注意迭代器与分配（`captures` 比 `is_match` 重）。引擎本身偏线性，但滥用 API 仍会慢。

**解答：**
清单：

1. `LazyLock` / 结构体字段里持有 `Regex`（见 [Q2](#q2)）。
2. 只要布尔 → `is_match`，不要 `captures`。
3. 字面量替换 → `str::replace`（见 [Q5](#q5)）。
4. 多模式时可查 `regex::RegexSet`（多模式是否匹配），避免反复编译几十个小正则——详见 [Q13](#q13)。
5. 基准用 `cargo bench` / criterion（见 [04-running Q18](04-running.md#q18)），别凭感觉。

```rust
fn main() {
    // 热路径上：子串检查几乎总是比正则便宜
    let log = "ERROR failed to connect";
    assert!(log.contains("ERROR"));
}
```

```text
// 贵：每次请求 Regex::new
// 便宜：static LazyLock<Regex> + is_match
// 更便宜：固定针 → hay.contains(needle)
```

**Go 对比：**
- **Go 怎么做**：同样应复用 `*Regexp`；`MustCompile` 放包级。
- **Rust 为什么不同**：同一纪律；另多分出 `str` 捷径 API。
- **Go 程序员易踩的坑**：以为“反正 RE2 很快”就在循环里编译。

**记忆点：**
- 慢的头号原因：重复编译 + 不必要的 `captures`。
- 第二号：本可用 `contains`/`split` 却上了正则。

---

## Q10. `Regex::new` 编译错误怎么读？ {#q10}
**Tags:** `common` `beginner` `error`
**适用版本:** `regex` 1.x

**一句话答案：**
`Regex::new` 返回 `Result`；`Err` 里是**模式语法/不支持特性**说明，不是 Rust 借用检查。读错误文本里的“unsupported”“unclosed group”等，对照 [Q6](#q6) 的引擎边界；生产代码用 `expect`/`?` 明确失败，调试期可 `unwrap`。

**解答：**

```text
match Regex::new(r"(?<=foo)bar") {
    Ok(re) => { let _ = re; }
    Err(e) => {
        // e.to_string() 会说明：该构造不被支持 / 语法问题
        eprintln!("regex compile failed: {e}");
    }
}
```

常见原因：

| 现象 | 排查 |
|------|------|
| unclosed group / empty group | 括号不配、多余 `|` |
| unsupported look-around / backref | 你在写 PCRE，引擎不收（[Q6](#q6)） |
| invalid UTF-8 in pattern | 模式字符串本身非法 |
| 运行期才炸 | 模式来自配置/用户：用 `Regex::new` 的 `Err`，别 `unwrap` 进生产 |

无依赖：先确认你是不是根本不需要正则：

```rust
fn main() {
    let pat = "todo:";
    assert!("todo: ship".starts_with(pat));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	_, err := regexp.Compile(`(`)
	fmt.Println(err)
}
```

- **Go 怎么做**：`Compile` 返回 `error`；`MustCompile` panic。
- **Rust 为什么不同**：`Regex::new` → `Result`；`unwrap`/`expect` 对标 `MustCompile`。
- **Go 程序员易踩的坑**：把所有模式都 `unwrap`，配置文件一错进程直接崩。

**记忆点：**
- 编译失败先读 `Err` 字符串，再查是否用了不支持特性。
- 用户输入的模式：必须处理 `Err`。

---

## Q11. 什么时候不该用正则？ {#q11}
**Tags:** `hot` `beginner` `design`
**适用版本:** 通用

**一句话答案：**
固定子串、空白分词、简单前缀后缀、HTML/JSON/CSV 整文档解析、需要完整上下文文法时——**别用正则**。正则擅长“局部模式”，不擅长“真正的语言/格式”。

**解答：**
不该用的信号：

- 你只是在找 `"ERROR"` / 去掉首尾空格 → `contains` / `trim`
- 你在“解析 JSON/HTML” → `serde_json` / 专用解析器（见 [36-serde-and-serialization](36-serde-and-serialization.md)）
- 模式开始叠很多 `(.*)` 回溯味 → 手写扫描或 parser
- 要验证邮箱/URL 的“完整 RFC” → 专用 crate 或保守校验，而不是复制网上巨型正则

```rust
fn main() {
    let line = "  a,b,c  ";
    let parts: Vec<_> = line.trim().split(',').collect();
    assert_eq!(parts, ["a", "b", "c"]);
}
```

```rust
fn main() {
    let path = "foo/bar.txt";
    assert!(path.ends_with(".txt"));
    assert!(path.contains('/'));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	fmt.Println(strings.Contains("a,b", ","))
	fmt.Println(strings.Split("a,b", ","))
}
```

- **Go 怎么做**：`strings` 包扛日常；`regexp` 留给真模式。
- **Rust 为什么不同**：同样分工；`str` 方法 + 解析库优先。
- **Go 程序员易踩的坑**：用正则“切 CSV / 拔 HTML 标签”，两端都难维护。

**记忆点：**
- 正则是手术刀，不是瑞士军刀。
- 格式越正经，越该用解析器。

---

## Q12. 和 `split` / `contains` / `trim` 怎么分工？ {#q12}
**Tags:** `hot` `beginner` `str` `split` `contains`
**适用版本:** Rust 1.0+（`str` API）；正则见 `regex` crate

**一句话答案：**
**字面量与简单分隔**用 `str`（`contains`/`split`/`trim`/`replace`…）；**真正的模式**才用 `regex`。先写 `str`，写不动再升级——对标 Go 里 `strings` vs `regexp`。更多日常 API 见 [14-strings-and-text Q21](14-strings-and-text.md#q21)。

**解答：**

```rust
fn main() {
    let s = "  Hello, Rust  ";
    assert!(s.contains("Rust"));
    assert_eq!(s.trim(), "Hello, Rust");
    let parts: Vec<_> = "a|b|c".split('|').collect();
    assert_eq!(parts, ["a", "b", "c"]);
    assert_eq!("Ab".to_lowercase(), "ab");
}
```

```text
// 需要模式时再上 regex：
// Regex::new(r"\s*,\s*")?.split(text)  // 空白可选的逗号分隔
// 固定 ',' → 直接 str::split(',')
```

决策表：

| 任务 | 优先 |
|------|------|
| 子串是否存在 | `contains` |
| 按固定字符/子串切开 | `split` / `split_once` |
| 去空白 | `trim` / `trim_start` / `trim_end` |
| 字面量替换 | `replace` / `replacen` |
| `\d+`、邮箱状、多选一模式 | `regex` |
| 命名捕获、模式替换 | `regex`（[Q4](#q4)、[Q5](#q5)） |

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "  Hello, Rust  "
	fmt.Println(strings.Contains(s, "Rust"))
	fmt.Println(strings.TrimSpace(s))
	fmt.Println(strings.Split("a|b", "|"))
}
```

- **Go 怎么做**：`strings` 日常，`regexp` 模式。
- **Rust 为什么不同**：同一分工；Rust 正则在 crate，字符串方法在 `str`/`String`。
- **Go 程序员易踩的坑**：一上来就 `Regex::new`，把 Go 里该用 `strings` 的活也正则化。

**记忆点：**
- `strings` 包直觉 → Rust `str` 方法。
- `regexp` 直觉 → `regex` crate。
- 能 `contains`/`split` 解决的，别编译正则。

---

## Q13. `RegexSet` 多模式匹配什么时候用？ {#q13}
**Tags:** `common` `RegexSet` `multi-pattern`
**适用版本:** `regex` 1.x

**一句话答案：**
当你有**很多模式**，只关心「命中了哪些 / 有没有命中」，不需要每个模式各自抽捕获组时，用 **`RegexSet`**：一次扫描 haystack，返回匹配到的模式下标集合。比「几十个 `Regex` 轮流 `is_match`」更省编译与重复扫描。

**解答：**
典型场景：日志分类（ERROR/WARN/…）、简易路由、敏感词命中检测——**布尔/下标**够用，不要捕获。

```toml
[dependencies]
regex = "1"
```

```text
use regex::RegexSet;

fn main() {
    let set = RegexSet::new(&[
        r"(?i)error",
        r"(?i)warn",
        r"\b\d{3}-\d{4}\b",
    ]).unwrap();

    let hay = "WARN: ticket 555-1212";
    let matches: Vec<_> = set.matches(hay).into_iter().collect();
    // 命中下标 1（warn）与 2（电话状）
    assert_eq!(matches, vec![1, 2]);
    assert!(set.is_match(hay));
}
```

和「多个 `Regex`」怎么选：

| 需求 | 用什么 |
|------|--------|
| 只要「哪些模式命中」 | `RegexSet` |
| 要捕获组 / 替换 / 迭代匹配位置 | 普通 `Regex`（可再按 set 结果挑一个） |
| 只有 1～2 个模式 | 直接 `Regex` 更简单 |

「❌ 误用」——为了抽邮箱本地部分而用 `RegexSet`：它**不提供** captures；命中后再对对应 `Regex` 跑一次才有组。

```rust
fn main() {
    // 示意决策：单模式 + 捕获 → 别上 RegexSet
    let log = "user=ada";
    assert!(log.contains("user="));
}
```

性能提醒见 [Q9](#q9)：set 也要编译一次、复用（`LazyLock` / 字段持有），别在热循环里 `RegexSet::new`。

**Go 对比：**

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	patterns := []*regexp.Regexp{
		regexp.MustCompile(`(?i)error`),
		regexp.MustCompile(`(?i)warn`),
	}
	hay := "WARN: ok"
	for i, re := range patterns {
		if re.MatchString(hay) {
			fmt.Println("hit", i)
		}
	}
}
```

- **Go 怎么做**：通常自己维护 `[]*Regexp` 循环 `MatchString`；标准库没有同款「一次扫描多模式」API。
- **Rust 为什么不同**：`regex` 提供 `RegexSet`，专为多模式命中集合优化。
- **Go 程序员易踩的坑**：把 `RegexSet` 当成「带捕获的多正则」——它只回答命中下标。

**记忆点：**
- 多模式 + 只要命中集合 → `RegexSet`。
- 要捕获/替换 → 普通 `Regex`（可与 set 配合）。
- 同样：编译一次、热路径复用。
