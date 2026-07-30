+++
title = "36-serde-and-serialization"
date = 2026-07-28T14:49:00+08:00
weight = 360
type = "docs"
description = "面向 Go 用户讲清 serde/serde_json 与 encoding/json 的 derive、标签、Option 与错误对照"
isCJKLanguage = true
draft = false

+++

# Serde 与序列化 (Serde and Serialization)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否刚接触 Rust 就听说「序列化用 serde」，却分不清它和 `serde_json` 各自干什么？
- 你是否想把 Go 的 `json:"xxx,omitempty"` 习惯平移过来，却不知道 `rename` / `skip_serializing_if` 怎么写？
- 你是否遇到过 `Option` 字段变成 `null`、缺字段、或反序列化报错却读不懂 `Error` 信息？
- 你是否分不清该用强类型 struct，还是 `serde_json::Value` 先摸结构？
- 你是否要给 enum、外部类型或二进制格式选型，却不知道从哪几个开关下手？
- 你是否想用 serde 读 `toml` 配置，并用 `deny_unknown_fields` 把配置打严格？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| serialization | — | 序列化 | 把内存里的值写成字节/文本（如 JSON） | `json.Marshal` |
| deserialization | — | 反序列化 | 从字节/文本还原成类型化的值 | `json.Unmarshal` |
| **serde** | SERialize / DEserialize | 序列化框架 | 与格式无关的 Serialize/Deserialize 生态核心 | 无单一等价物；习惯对比 `encoding/json` |
| `serde_json` | — | JSON 后端 | 在 serde 之上读写 JSON 的常用 crate | `encoding/json` |
| `Serialize` | — | 可序列化 trait | 类型能写出为某种格式 | 实现了可被 `Marshal` 的形状 |
| `Deserialize` | — | 可反序列化 trait | 类型能从某种格式读入 | 实现了可被 `Unmarshal` 的形状 |
| derive | — | 派生宏 | `#[derive(...)]` 自动生成 trait 实现 | 结构体 tag + 反射，无需手写大部分样板 |
| `rename` / `rename_all` | — | 字段重命名属性 | 控制 JSON 键名与 Rust 字段名的映射 | `json:"snake_case"` 等 tag |
| `skip_serializing_if` | — | 条件跳过序列化 | 谓词为真时不写该字段 | `omitempty` 的可编程版 |
| `Value` | — | 动态 JSON 树 | 未绑定到具体 struct 的 JSON 值 | `json.RawMessage` / `map[string]any` |
| newtype | — | 新类型包装 | `struct Id(u64)` 这类单字段包装，用于挂自定义逻辑 | 自定义类型 + 自定义 Marshal |
| feature | Cargo feature | 特性开关 | `Cargo.toml` 里可选编译功能 | build tag / 可选依赖的近似 |
| `toml` crate | — | TOML 后端 | 用 serde 读写 `.toml` 配置的常见 crate | 第三方 TOML 库 |
| `deny_unknown_fields` | — | 拒绝未知字段 | 反序列化时遇到未声明键就报错 | 需手写严格校验 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q10](#q10), [Q12](#q12), [Q16](#q16) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q13](#q13), [Q15](#q15), [Q17](#q17) |
| `occasional` | [Q11](#q11), [Q14](#q14) |
| `advanced` | — |

---

## Q1. 为什么 Rust 生态几乎都用 serde，而不是像 Go 那样直接 `encoding/json`？ {#q1}
**Tags:** `hot` `beginner` `serde`
**适用版本:** serde 1.x（配合当前 stable）

**一句话答案：**
**serde**（SERialize/DEserialize，序列化框架）把「类型怎么变成数据」和「JSON/二进制等具体格式」拆开：你 derive 一次，就能接 `serde_json`、MessagePack、Bincode 等后端；Go 的 `encoding/json` 则是格式与 API 绑在一起。

**解答：**
心智模型：

| 层 | 负责什么 | 常见 crate |
|----|----------|------------|
| 数据模型 | `Serialize` / `Deserialize` | `serde`（+ derive） |
| 格式后端 | 真正读写 JSON 等 | `serde_json`、`rmp-serde`、`bincode`… |

Cargo 里通常两行依赖都要：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

没有 `serde` 时，你手里只有「某种格式的专用 API」；有了 serde，HTTP 体、配置文件、消息队列载荷可以共用同一套 struct。

对比「只解析字符串数字」这类纯 std 问题——那不需要 serde：

```rust
fn main() {
    let n: i32 = "42".parse().expect("not an int");
    println!("{n}");
}
```

**Go 对比：**
```go
package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	Name string `json:"name"`
}

func main() {
	b, _ := json.Marshal(User{Name: "Ada"})
	fmt.Println(string(b))
}
```
- **Go 怎么做**：标准库直接提供 JSON；别的格式另找库，API 各写各的。
- **Rust 为什么不同**：stdlib 不内置 JSON；社区把「格式无关的 trait」做成基础设施。
- **Go 程序员易踩的坑**：以为 `serde_json` 单独就能 `#[derive(Serialize)]`——derive 在 `serde` 的 `derive` feature 里。

**记忆点：**
- serde = 协议；`serde_json` = JSON 实现。
- 一个 struct，多种格式后端。

---

## Q2. `Serialize` / `Deserialize` 的 derive 怎么写？缺 feature 会怎样？ {#q2}
**Tags:** `hot` `beginner` `derive` `Serialize` `Deserialize`
**适用版本:** serde 1.x

**一句话答案：**
在类型上写 `#[derive(Serialize, Deserialize)]`，并在 `Cargo.toml` 给 `serde` 打开 **feature**（Cargo 特性开关）`derive`；否则宏根本不存在，编译直接失败。

**解答：**
最小依赖与类型：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
```

```text
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    name: String,
    age: u32,
}
```

只序列化、不反序列化时可以只 derive `Serialize`；配置/API 往返通常两个都要。

「❌ 常见失败」——依赖写成 `serde = "1"` 却没开 `derive`，再写 `#[derive(Serialize)]`：编译器会报找不到 derive 宏（提示里常出现 `Serialize` / `serde` / feature 相关字样）。

「✅ 正确写法」——始终 `features = ["derive"]`，或 `cargo add serde -F derive`。

纯 std 侧你已经熟悉的「给类型挂行为」是 trait；serde 只是把那套用宏生成了：

```rust
trait Demo {
    fn name(&self) -> &str;
}

struct A;
impl Demo for A {
    fn name(&self) -> &str {
        "A"
    }
}

fn main() {
    println!("{}", A.name());
}
```

**Go 对比：**
- **Go 怎么做**：导出字段 + `json` tag，靠反射，无需 derive。
- **Rust 为什么不同**：默认不要运行时反射填字段；用过程宏在编译期生成代码。
- **Go 程序员易踩的坑**：字段必须是 `pub` 才——不对，serde 可以序列化私有字段（同模块/同 crate 的 derive 实现能访问）。

**记忆点：**
- `#[derive(Serialize, Deserialize)]` + `features = ["derive"]`。
- derive 在编译期生成，不是反射。

---

## Q3. `serde_json::to_string` / `from_str` 怎么用？和 Go 的 Marshal/Unmarshal 怎么对？ {#q3}
**Tags:** `hot` `serde_json` `to_string` `from_str`
**适用版本:** serde_json 1.x

**一句话答案：**
`to_string` / `to_vec` 把实现了 `Serialize` 的值写成 JSON；`from_str` / `from_slice` 把 JSON 读进实现了 `Deserialize` 的类型；返回的是 `Result`，不是「静默零值」。

**解答：**
往返示例：

```text
use serde::{Deserialize, Serialize};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct Point {
    x: i32,
    y: i32,
}

fn main() -> Result<(), serde_json::Error> {
    let p = Point { x: 1, y: 2 };
    let s = serde_json::to_string(&p)?;
    // s == "{\"x\":1,\"y\":2}"
    let q: Point = serde_json::from_str(&s)?;
    assert_eq!(p, q);
    Ok(())
}
```

常用 API 对照：

| Rust | 作用 | Go |
|------|------|-----|
| `serde_json::to_string` | 值 → `String` | `json.Marshal` 再 `string(b)` |
| `serde_json::to_vec` | 值 → `Vec<u8>` | `json.Marshal` |
| `serde_json::from_str` | `&str` → `T` | `json.Unmarshal` |
| `serde_json::from_slice` | `&[u8]` → `T` | `json.Unmarshal` |
| `serde_json::to_writer` | 写到 `Write` | `json.NewEncoder` |

美化输出用 `to_string_pretty`。失败时用 `?` 或匹配 `Err`，不要 `.unwrap()` 吞掉线上输入。

不依赖 serde 时，字符串拼接「看起来像 JSON」很容易错——这也是为什么要用库：

```rust
fn main() {
    let name = "Ada";
    // 手写转义极易漏掉引号/反斜杠；生产代码请走 serde_json
    let rough = format!("{{\"name\":\"{name}\"}}");
    println!("{rough}");
}
```

**Go 对比：**
```go
b, err := json.Marshal(p)
if err != nil { /* ... */ }
err = json.Unmarshal(b, &p2)
```
- **Go 怎么做**：`Marshal` / `Unmarshal`，目标用指针。
- **Rust 为什么不同**：`from_str` 返回新的 `T`（或你提供的收集器），所有权更清晰。
- **Go 程序员易踩的坑**：忘了 `?` / `Result`，或把 `&str` 和 `String` 混用导致多余 clone。

**记忆点：**
- 写出：`to_string` / `to_vec`。
- 读入：`from_str` / `from_slice`。
- 一律处理 `Result`。

---

## Q4. `rename` 和 `rename_all` 怎么对齐 Go 的 `json` tag？ {#q4}
**Tags:** `hot` `rename` `json-tag`
**适用版本:** serde 1.x

**一句话答案：**
单字段用 `#[serde(rename = "...")]`；整类型统一风格用 `#[serde(rename_all = "camelCase")]` 等，效果接近 Go 结构体字段上的 `` `json:"..."` ``。

**解答：**
字段级与类型级：

```text
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    display_name: String,
    #[serde(rename = "user_id")]
    id: u64,
}
```

序列化后键名大致是 `displayName` 与 `user_id`（字段级 `rename` 覆盖 `rename_all`）。

常见 `rename_all` 取值：`snake_case`、`camelCase`、`PascalCase`、`SCREAMING_SNAKE_CASE`、`kebab-case` 等。

Go 侧常见写法：

```go
type User struct {
	DisplayName string `json:"displayName"`
	ID          uint64 `json:"user_id"`
}
```

只改序列化名、反序列化仍接受别名时，还可看 `alias` / `serialize_with`（进阶）；入门先掌握 `rename` / `rename_all` 就够。

**Go 对比：**
- **Go 怎么做**：每个字段一个 tag 字符串。
- **Rust 为什么不同**：属性可以挂在类型上批量改，减少重复。
- **Go 程序员易踩的坑**：Rust 默认 JSON 键是字段名原文（常是 `snake_case`）；对接前端 camelCase 时忘了 `rename_all`。

**记忆点：**
- 批量风格 → `rename_all`。
- 个别例外 → 字段 `rename`。

---

## Q5. `Option` 字段和 `skip_serializing_if` 怎么对应 Go 的 `omitempty`？ {#q5}
**Tags:** `hot` `Option` `omitempty` `skip_serializing_if`
**适用版本:** serde 1.x

**一句话答案：**
缺省/可空用 `Option<T>`：JSON 缺字段或 `null` 常映射为 `None`；若不想把 `None` 写成 `null`，用 `skip_serializing_if = "Option::is_none"`，这比 Go 的 `omitempty` 更明确、也可用于非 Option。

**解答：**
可空字段：

```text
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Patch {
    title: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    note: Option<String>,
}
```

要点：
- **反序列化**：字段缺失时，若有 `#[serde(default)]` 或 `Option` 的默认行为，可得 `None`（具体以你用的属性组合为准；`Option` 对缺失字段通常很友好）。
- **序列化**：默认 `None` 往往变成 JSON `null`；加了 `skip_serializing_if = "Option::is_none"` 则整键省略，更像 `omitempty`。

非 Option 也可跳过，例如空 `Vec`：

```text
#[derive(Serialize)]
struct Bag {
    #[serde(skip_serializing_if = "Vec::is_empty")]
    items: Vec<String>,
}
```

Go：

```go
type Patch struct {
	Title *string `json:"title,omitempty"`
	Note  *string `json:"note,omitempty"`
}
```

**Go 对比：**
- **Go 怎么做**：`omitempty` 对「零值」省略；指针/`*` 常用来区分「没设」和「设成零值」。
- **Rust 为什么不同**：`Option` 显式表达有无；跳过规则用函数名字符串写清，不靠「零值魔法」一刀切。
- **Go 程序员易踩的坑**：以为 `Option` 默认就 omit——不，常需要 `skip_serializing_if`。

**记忆点：**
- 可空 → `Option<T>`。
- 省略 `None` → `skip_serializing_if = "Option::is_none"`。

---

## Q6. serde_json 的错误信息怎么读？常见失败原因有哪些？ {#q6}
**Tags:** `common` `error` `Error`
**适用版本:** serde_json 1.x

**一句话答案：**
`serde_json::Error` 会告诉你「在哪个路径/行列、期望什么类型」；先看是类型不匹配、缺必填字段、还是 JSON 本身非法，再对照 struct 定义。

**解答：**
典型处理：

```text
fn parse_user(s: &str) -> Result<User, serde_json::Error> {
    serde_json::from_str(s)
}

// 调用处：
match serde_json::from_str::<User>(raw) {
    Ok(u) => { /* ... */ }
    Err(e) => {
        // Display: 人类可读；e.line()/column() 便于定位
        eprintln!("json error at {}:{}: {e}", e.line(), e.column());
    }
}
```

常见原因对照：

| 现象 | 优先检查 |
|------|----------|
| expected map / struct | 根不是对象，或字段类型整体错了 |
| invalid type: integer, expected string | JSON 数字对上了 Rust `String`（或相反） |
| missing field `foo` | 必填字段没来；可改 `Option` 或 `#[serde(default)]` |
| trailing characters | 字符串里 JSON 后面还有垃圾 |
| EOF while parsing | 截断的 JSON |

调试期可先 `from_str::<serde_json::Value>` 看树形结构，再收紧到强类型（见 [Q7](#q7)）。

**Go 对比：**
```go
if err := json.Unmarshal(b, &u); err != nil {
    fmt.Println(err)
}
```
- **Go 怎么做**：`Unmarshal` 返回 `error`，信息相对短。
- **Rust 为什么不同**：路径（如 `user.address.zip`）和位置信息更常出现在消息里。
- **Go 程序员易踩的坑**：用 `unwrap()` 直接崩在请求处理里；应返回/记录 `Error`。

**记忆点：**
- 读 `Display` + `line`/`column`。
- 缺字段 / 类型错 / JSON 坏 —— 三类分开查。

---

## Q7. 什么时候用 `serde_json::Value`，什么时候用强类型？ {#q7}
**Tags:** `common` `Value` `typed`
**适用版本:** serde_json 1.x

**一句话答案：**
协议稳定、要编译期保证形状 → 强类型 `struct`/`enum`；协议未知、只抽几个键、或做透传代理 → `Value`（动态 JSON 树）或两者混用。

**解答：**
强类型：

```text
#[derive(Deserialize)]
struct Config {
    host: String,
    port: u16,
}
let cfg: Config = serde_json::from_str(s)?;
```

动态：

```text
let v: serde_json::Value = serde_json::from_str(s)?;
let port = v["port"].as_u64();
```

混用：结构体里留一个 `Value` 字段接「扩展属性」，或先 `Value` 再 `serde_json::from_value::<T>(v)`。

| 场景 | 建议 |
|------|------|
| 对外 API 契约 | 强类型 |
| 日志/Webhook 字段常变 | `Value` 或 `HashMap<String, Value>` |
| 只读一两个键 | `Value` 可接受，注意类型判断 |

`Value` 类似 Go 的 `map[string]any` / `json.RawMessage` 路线，失去编译期字段检查。

**Go 对比：**
- **Go 怎么做**：`struct` vs `map[string]any` / `json.RawMessage`。
- **Rust 为什么不同**：同样二分；Rust 更鼓励边界处尽早 `Deserialize` 进强类型。
- **Go 程序员易踩的坑**：全项目 `Value` 满天飞，错误拖到运行时才发现。

**记忆点：**
- 边界校验用强类型；探索/透传用 `Value`。

---

## Q8. enum 的 JSON 标签形式有哪些？怎么选？ {#q8}
**Tags:** `common` `enum` `tag` `internally_tagged`
**适用版本:** serde 1.x

**一句话答案：**
默认常是外部标签（`{"Variant": {...}}`）；也可用 `internally_tagged` / `adjacently_tagged` / `untagged` 对齐不同 API 习惯，对应 Go 里「用字段区分类型」的手工约定。

**解答：**
四种常见策略（属性挂在 enum 上）：

```text
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")] // internally tagged
enum Event {
    Login { user: String },
    Logout { user: String },
}
// 形状接近：{"type":"Login","user":"ada"}
```

```text
#[derive(Serialize, Deserialize)]
#[serde(tag = "t", content = "c")] // adjacently tagged
enum Msg {
    Text(String),
    Bin(Vec<u8>),
}
```

```text
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum Id {
    Num(u64),
    Str(String),
}
```

选型直觉：
- 对接已有 JSON → 看样例选 tag 形式，不要硬改对方。
- 自控协议 → `internally_tagged` 往往最易读。
- `untagged` 靠类型猜测，歧义时难排查，慎用。

**Go 对比：**
```go
type Event struct {
	Type string `json:"type"`
	User string `json:"user"`
}
```
- **Go 怎么做**：通常一个 struct + `Type` 字段，再 `switch`。
- **Rust 为什么不同**：enum 变体是类型系统的一等公民，serde 用属性生成标签策略。
- **Go 程序员易踩的坑**：默认外部标签长得和前端习惯的 `{type:...}` 不一样，对接失败却怪「serde 坏了」。

**记忆点：**
- 先看 JSON 样例，再选 tag 策略。
- `untagged` 最后才考虑。

---

## Q9. 外部类型不能 derive 时怎么办？newtype 怎么用？ {#q9}
**Tags:** `common` `newtype` `remote` `from`
**适用版本:** serde 1.x

**一句话答案：**
不能改的外部类型：用 **newtype**（新类型包装）包一层再 derive，或手写/用 `serde_with`、remote derive；核心是「在你控制的类型上实现 Serialize/Deserialize」。

**解答：**
newtype 包装：

```text
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct UserId(u64);

#[derive(Serialize, Deserialize)]
struct User {
    id: UserId,
    name: String,
}
```

需要与外部 crate 的类型互通时，常见手法：
- 在自己的 DTO struct 里用可 derive 的字段，边界再 `From`/`Into` 转换。
- `#[serde(from = "...", into = "...")]` 委托转换。
- remote derive（`#[serde(remote = "...")]`）给外部类型「隔空」生成实现（进阶，查 serde 文档）。

不要试图给别人的类型直接 `impl Serialize`（孤儿规则会拦你），除非用 newtype。

**Go 对比：**
```go
type UserId uint64

func (id UserId) MarshalJSON() ([]byte, error) { /* ... */ }
```
- **Go 怎么做**：给命名类型实现 `json.Marshaler` / `Unmarshaler`。
- **Rust 为什么不同**：有孤儿规则；外部类型上直接 impl 外来 trait 通常不行，故用 newtype。
- **Go 程序员易踩的坑**：以为和 Go 一样随便在外部类型上挂方法——Rust 要包装或转换。

**记忆点：**
- 控制边界 DTO；外部类型用 newtype / 转换。
- 不要硬 derive 别人的类型。

---

## Q10. 和 Go 的 `omitempty`、`json` tag 总对照表是什么？ {#q10}
**Tags:** `hot` `go` `omitempty` `json-tag`
**适用版本:** serde 1.x

**一句话答案：**
把 Go tag 拆成 Rust 的若干属性：改名用 `rename`/`rename_all`，可空用 `Option`，省略用 `skip_serializing_if`，忽略用 `skip`，默认值用 `default`。

**解答：**
对照表：

| Go `json` tag | Rust serde 属性 | 说明 |
|---------------|-----------------|------|
| `json:"name"` | `rename = "name"` | 字段键名 |
| 批量 camelCase | `rename_all = "camelCase"` | 挂在类型上 |
| `omitempty` | `skip_serializing_if = "..."` | 常配 `Option::is_none` |
| `-` | `skip` | 永不（反）序列化 |
| 指针表示可选 | `Option<T>` | 显式有无 |
| `string` 等特殊选项 | 自定义 / `with` | 按需查文档 |

完整示例：

```text
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Article {
    title: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    subtitle: Option<String>,
    #[serde(skip)]
    cache_key: String,
}
```

Go：

```go
type Article struct {
	Title    string  `json:"title"`
	Subtitle *string `json:"subtitle,omitempty"`
	CacheKey string  `json:"-"`
}
```

**Go 对比：**
- **Go 怎么做**：一个 tag 字符串塞多项。
- **Rust 为什么不同**：属性正交组合，意图更直白，也更啰嗦一点。
- **Go 程序员易踩的坑**：只写了 `Option` 就以为等于 `omitempty`。

**记忆点：**
- rename ≈ 改名；skip_serializing_if ≈ omitempty；skip ≈ `-`。

---

## Q11. 什么时候该用二进制格式而不是 JSON？ {#q11}
**Tags:** `occasional` `bincode` `messagepack` `binary`
**适用版本:** 生态常见 crate（选型级说明）

**一句话答案：**
人要读、跨语言 HTTP API → JSON（或类似文本）；机器对机器、要更小更快、同生态可控 → 考虑 MessagePack、CBOR、Bincode 等，仍走 serde 的 `Serialize`/`Deserialize`。

**解答：**
粗规则：

| 需求 | 更合适 |
|------|--------|
| 浏览器 / 运维可读 | JSON |
| 日志排查友好 | JSON |
| 内网高 QPS、载荷大 | 二进制（MessagePack/CBOR 等） |
| 仅 Rust ↔ Rust 且可共版本 | 也可 Bincode 一类（注意版本兼容） |

serde 的好处是：**同一套 struct**，换后端 crate，不必重写业务模型。代价是：二进制不适合当「契约文档」给人看；跨语言要选有多语言实现的格式。

```toml
# 仍需 serde；二进制后端按项目从 crates.io 选用
[dependencies]
serde = { version = "1", features = ["derive"] }
# serde_json = "1"
# 再加所选二进制格式对应的 serde 后端 crate
```

**Go 对比：**
- **Go 怎么做**：`encoding/json` + `encoding/gob`（偏 Go 内部）或 protobuf 等。
- **Rust 为什么不同**：serde 让「换格式」成本更低；gob 的近亲不是 serde 本身，而是具体后端。
- **Go 程序员易踩的坑**：内网图省事上了无模式二进制，却忘了版本演进与跨语言。

**记忆点：**
- 对外可读 → JSON；对内性能 → 二进制后端。
- 模型仍用 serde derive。

---

## Q12. `Cargo.toml` 里怎么打开 serde 的 `derive` feature？ {#q12}
**Tags:** `hot` `Cargo.toml` `feature` `derive`
**适用版本:** Cargo / serde 1.x

**一句话答案：**
写成 `serde = { version = "1", features = ["derive"] }`，或 `cargo add serde --features derive`；只要写 `#[derive(Serialize)]` 就几乎总需要它。

**解答：**
推荐写法：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

等价命令：

```bash
cargo add serde -F derive
cargo add serde_json
```

只要 `serde`、不要宏时（极少见，手写 impl）可以不开 `derive`。Web/API 项目里 99% 情况要开。

`default-features` / 精简体积是进阶话题；入门先保证 `derive` 打开、能编译通过。

**Go 对比：**
- **Go 怎么做**：标准库 `encoding/json`，无 feature 开关。
- **Rust 为什么不同**：宏与运行时库可拆；feature 控制是否拉进 derive 宏。
- **Go 程序员易踩的坑**：`cargo add serde` 后直接 derive，忘了 `-F derive`。

**记忆点：**
- `features = ["derive"]` 是标配。
- 同时加上 `serde_json` 才能 `to_string`/`from_str`。

---

## Q13. 字段默认值、`flatten`、忽略未知字段怎么处理？ {#q13}
**Tags:** `common` `default` `flatten` `deny_unknown_fields`
**适用版本:** serde 1.x

**一句话答案：**
缺字段补默认用 `#[serde(default)]`；把嵌套「摊平」到同层键用 `flatten`；想严格拒绝未知键用 `deny_unknown_fields`（默认往往是忽略未知键，与 Go 默认忽略额外字段类似）。

**解答：**

```text
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Strict {
    #[serde(default)]
    retries: u32, // 缺省为 0
    #[serde(flatten)]
    extra: Extra,
}

#[derive(Deserialize)]
struct Extra {
    region: String,
}
```

| 属性 | 作用 |
|------|------|
| `default` | 缺字段时用 `Default::default()` 或指定路径 |
| `flatten` | 子结构字段提升到父级 JSON 对象 |
| `deny_unknown_fields` | 多未知键就报错 |

Go 默认 `Unmarshal` 也忽略未知字段；要严格校验需额外逻辑。Rust 用属性一键收紧。

**Go 对比：**
- **Go 怎么做**：零值即默认；未知字段默认丢弃。
- **Rust 为什么不同**：可用 `default` / `deny_unknown_fields` 把策略写在类型上。
- **Go 程序员易踩的坑**：以为 Rust 默认「严格模式」——不，常要自己加 `deny_unknown_fields`。

**记忆点：**
- 宽松 API：默认忽略未知键。
- 严格配置：`deny_unknown_fields`。

---

## Q14. 序列化时借用与生命周期要注意什么？（`Deserialize` 进 `&str`） {#q14}
**Tags:** `occasional` `lifetime` `Cow` `borrow`
**适用版本:** serde 1.x

**一句话答案：**
`Deserialize` 到 `&str` / `&[u8]` 需要输入缓冲活得够久（常要 `Deserialize<'de>`）；多数应用直接用 `String`/`Vec<u8>` 更省心；要零拷贝再考虑借用或 `Cow`。

**解答：**
拥有数据（最常见、最好教）：

```text
#[derive(Deserialize)]
struct Line {
    text: String,
}
```

借用（高级：生命周期与输入缓冲绑在一起）：

```text
#[derive(Deserialize)]
struct Line<'a> {
    text: &'a str, // 要求反序列化输入在 'a 内有效，且格式支持借用
}
```

对 JSON 数字、需要分配转义的字符串等，借用可能失败或根本不可用，这时必须 `String`。

纯 std 侧「拥有 vs 借用」你已见过：

```rust
fn takes_owned(s: String) {
    println!("{s}");
}

fn takes_borrow(s: &str) {
    println!("{s}");
}

fn main() {
    let owned = String::from("hi");
    takes_borrow(&owned);
    takes_owned(owned);
}
```

**Go 对比：**
- **Go 怎么做**：`Unmarshal` 进 `string` 通常都是拷贝后的值；少纠结 lifetime。
- **Rust 为什么不同**：借用要挂在输入缓冲的生命周期上。
- **Go 程序员易踩的坑**：一上来全用 `&str` 字段，被生命周期和 JSON 转义卡住。

**记忆点：**
- 默认 `String`；确认零拷贝收益再借用。
- 借用失败就改回拥有类型。

---

## Q15. 时间字段怎么用 serde？（timestamp / RFC3339） {#q15}
**Tags:** `common` `chrono` `time` `RFC3339` `timestamp`
**适用版本:** serde 1.x；`chrono` / `time` crate 的 serde feature（以当前文档为准）

**一句话答案：**
JSON 里时间常见两种：**RFC3339 字符串**（如 `2026-07-28T14:49:00+08:00`）和**数字时间戳**（秒/毫秒）。Rust 侧用 `chrono` 或 `time` 类型 + 对应 `serde` feature / helper，不要把时间当“普通 String”长期放着。更系统的日期时间专题见 [41-time-and-dates](41-time-and-dates.md)。

**解答：**
RFC3339 字符串（text，需 chrono + serde feature）：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", features = ["serde"] }
```

```text
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Event {
    // chrono 开了 serde feature 后，DateTime 默认常按 RFC3339 字符串（具体以文档为准）
    at: DateTime<Utc>,
}
```

Unix 时间戳（秒）示意：

```text
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Event {
    #[serde(with = "chrono::serde::ts_seconds")]
    at: DateTime<Utc>,
}
// 也有 ts_milliseconds / 选项型 helper；对接前端时先约定单位
```

无依赖侧：先当字符串过手，真正业务再解析（仅示意分工，不是推荐长期模型）：

```rust
fn main() {
    let raw = "2026-07-28T14:49:00+08:00";
    assert!(raw.contains('T'));
    // 生产代码：交给 chrono/time 解析进强类型，再 serde
    println!("{raw}");
}
```

选型：

| 线缆格式 | 常见做法 |
|----------|----------|
| RFC3339 / ISO8601 字符串 | `DateTime` + serde（可读、可跨时区标注） |
| 整数秒 / 毫秒 | `serde(with = "…ts_seconds")` 一类；**先和前端约定单位** |
| 只要展示、不做计算 | 暂时 `String`，但校验薄弱 |

**Go 对比：**

```go
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type Event struct {
	At time.Time `json:"at"`
}

func main() {
	var e Event
	_ = json.Unmarshal([]byte(`{"at":"2026-07-28T06:49:00Z"}`), &e)
	fmt.Println(e.At)
}
```

- **Go 怎么做**：`time.Time` 默认按 RFC3339 文本与 `encoding/json` 协作；时间戳常要自定义或别的 tag 策略。
- **Rust 为什么不同**：标准库无开箱 `DateTime`；用 `chrono`/`time` + serde feature / `with` 模块。
- **Go 程序员易踩的坑**：字段写成 `String` 然后到处手解析；或时间戳单位（秒 vs 毫秒）和前端不一致。

**记忆点：**
- 字符串时间 → RFC3339 + `DateTime`。
- 数字时间 → 明确秒/毫秒 helper。
- 细节与坑见 [41-time-and-dates](41-time-and-dates.md)。

---

## Q16. 怎么用 serde 读 TOML 配置？ {#q16}
**Tags:** `hot` `toml` `config` `Deserialize`
**适用版本:** serde 1.x；`toml` crate 0.8+（或以当前维护版本为准）

**一句话答案：**
定义 `#[derive(Deserialize)]` 的配置结构体，`fs::read_to_string` 读文件，再 `toml::from_str(&text)`（或 `toml::from_slice`）——serde 负责类型，**toml** crate 负责 TOML 语法。和 JSON 同一套 derive，只换后端。

**解答：**

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
toml = "0.8"
```

```text
use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
struct Config {
    host: String,
    port: u16,
    #[serde(default)]
    debug: bool,
}

fn load(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let text = fs::read_to_string(path)?;
    let cfg: Config = toml::from_str(&text)?;
    Ok(cfg)
}
```

示例 `app.toml`：

```toml
host = "127.0.0.1"
port = 8080
debug = true
```

要点：
- 字段名默认对应 TOML 键；要改名用 `rename` / `rename_all`（见 [Q3](#q3)）
- 缺省字段用 `#[serde(default)]` 或 `Option<T>`（见 [Q13](#q13)）
- 严格配置再加 `deny_unknown_fields`（见 [Q17](#q17)）

**Go 对比：**
```go
// 第三方 toml 库 + struct tag；标准库没有 encoding/toml
```
- **Go 怎么做**：第三方 TOML + 反射 tag。
- **Rust 为什么不同**：同一套 serde derive，JSON/TOML/YAML 换 crate。
- **Go 程序员易踩的坑**：以为要用和 `encoding/json` 完全不同的一套属性——键映射仍是 serde 属性。

**记忆点：**
- derive + `toml::from_str`。
- 配置文件 ≈ 反序列化，不是手写解析器。

---

## Q17. 配置场景下 `deny_unknown_fields` 为什么特别有用？ {#q17}
**Tags:** `common` `deny_unknown_fields` `config` `toml`
**适用版本:** serde 1.x（JSON/TOML 等后端通用）

**一句话答案：**
配置里多一个拼错的键（`prot` 而不是 `port`），默认会被**默默忽略**，程序用默认值跑——极难查。给配置 struct 加 `#[serde(deny_unknown_fields)]`，拼错立刻反序列化失败。这是 [Q13](#q13) 在「读配置」场景的强化版。

**解答：**

```text
use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Config {
    host: String,
    port: u16,
}
```

```text
// typo.toml
// host = "127.0.0.1"
// prot = 8080          ← 拼错

// toml::from_str::<Config>(...)  → Err（未知字段 prot）
```

对比策略：

| 场景 | 建议 |
|------|------|
| 对外 JSON API | 常保持宽松（忽略未知字段），方便演进 |
| 本地 / 部署配置 TOML | **强烈建议** `deny_unknown_fields` |
| 需要扩展字段 | 显式 `#[serde(flatten)]` 到 `HashMap` 或嵌套表，而不是靠「静默忽略」 |

和 [Q16](#q16) 组合：读 TOML 配置时，derive + `deny_unknown_fields` + 清晰的 `context`（见 [21-error-handling](../21-error-handling/)）是稳妥默认。

**Go 对比：**
- **Go 怎么做**：默认也忽略未知字段；严格模式要自己校验或用额外库。
- **Rust 为什么不同**：一个属性即可在类型上收紧。
- **Go 程序员易踩的坑**：从 JSON API 习惯带到配置文件，拼错键却「看起来启动成功」。

**记忆点：**
- API 可宽松；配置宜严格。
- 拼错键失败 > 静默用默认值。

---
