+++
title = "05-comments"
date = 2026-07-28T14:49:00+08:00
weight = 50
type = "docs"
description = "讲清 Rust 注释、文档注释、doctest 与 rustdoc 的核心用法。"
isCJKLanguage = true
draft = false

+++

# 注释与文档 (Comments)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会把 `//`、`///`、`//!` 混用，结果文档位置放错了？
- 你是否想知道：Rust 的文档注释为什么还能顺手跑测试？
- 你会不会在函数体里写了 `///`，然后撞上奇怪的编译错误？
- 你是否不清楚 `rustdoc`、doctest、属性 `#[doc(...)]` 之间是什么关系？
- 你会不会在条件编译、私有项文档和文档链接上踩坑？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| comment | — | 注释 | 给人看的说明，不参与运行 | 同概念 |
| doc comment | — | 文档注释 | 会被 `rustdoc` 收集成 API 文档的注释 | Go 的 doc comment |
| `rustdoc` | — | Rust 文档工具 | 把源码文档注释生成 HTML 文档 | `go doc` / pkgsite 近亲 |
| doctest | documentation test | 文档测试 | 从文档代码块里抽取并编译/运行的测试 | Go 示例测试近亲 |
| attribute | — | 属性 | 编译器指令，写成 `#[...]` 或 `#![...]` | Go 无直接对应 |
| intra-doc link | — | 文档内链接 | 文档里用 ``[`Type`]`` 这类方式指向符号 | pkgsite 符号链接近亲 |
| `cfg` | configuration | 条件编译 | 按平台或 feature 选择性编译 | build tags 近亲 |
| docs.rs | — | Rust 在线文档站 | 公共 crate 文档托管站 | pkg.go.dev 近亲 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5) |
| `common` | [Q4](#q4), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q13](#q13), [Q14](#q14), [Q15](#q15) |
| `occasional` | [Q10](#q10), [Q11](#q11) |
| `advanced` | [Q12](#q12) |

---

## Q1. `//`、`/* */`、`///`、`//!` 分别是什么？ {#q1}
**Tags:** `hot` `beginner` `comments`
**适用版本:** Rust 1.0+

**一句话答案：**
`//` 和 `/* */` 是普通注释；`///` 给“下一项”写文档；`//!` 给“当前模块或 crate 本身”写文档。

**详细解答：**
```rust
fn main() {
    // 单行注释
    let x = 1; /* 块注释 */
    println!("{x}");
}
```

```rust
//! 这是模块文档

/// 这是函数文档
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(1, 2));
}
```

普通说明写 //，对外 API 文档写 ///

**🐹 Go 对比：**
```go
package main

import "fmt"

// Add adds two integers.
func Add(a, b int) int { return a + b }

func main() {
	fmt.Println(Add(1, 2))
}
```

- **Go 怎么做**：普通注释和导出符号文档注释都靠 `//`，位置规则较简单。
- **Rust 为什么不同**：Rust 把“普通注释”和“生成文档的注释”语义分开了。
- **Go 程序员易踩的坑**：在 Rust 里看到三个斜杠就当成“只是更醒目的注释”，其实它会进入文档系统。

**小结 / 记忆点：**
- `//` 给人看。
- `///` 给下一项生成文档。
- `//!` 给当前模块或 crate 生成文档。

---

## Q2. 为什么我在函数体里写 `///` 会报错？ {#q2}
**Tags:** `hot` `beginner` `doc`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 `///` 只能修饰“项”（如函数、结构体、模块），不能修饰函数体里的普通语句。

**详细解答：**
```rust
fn main() {
    // 函数体里的说明应该用普通注释
    let x = 1;
    println!("{x}");
}
```

```rust
/// 给下一项写文档
fn show() {
    println!("ok");
}

fn main() {
    show();
}
```

「❌ 错误写法」——把 `///` 放在语句前面：

```rust
fn main() {
    /// 想给语句写说明
    // error[E0585]: found a documentation comment that doesn't document anything
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

func main() {
	// Go 里函数体内外都还是普通注释
	x := 1
	fmt.Println(x)
}
```

- **Go 怎么做**：函数体里写 `//` 很自然，不会额外触发文档系统。
- **Rust 为什么不同**：Rust 需要区分“文档项说明”和“实现细节说明”。
- **Go 程序员易踩的坑**：把 `///` 当成“更正式的注释样式”乱用。

**小结 / 记忆点：**
- 函数体内一律优先 `//`。

---

## Q3. `///` 和 `//!` 到底怎么分？ {#q3}
**Tags:** `hot` `beginner` `module`
**适用版本:** Rust 1.0+

**一句话答案：**
`///` 是“外部文档注释”，作用于紧随其后的项；`//!` 是“内部文档注释”，作用于包围它的模块或 crate。

**详细解答：**
```rust
//! 数学工具模块

/// 返回平方
fn square(x: i32) -> i32 {
    x * x
}

fn main() {
    println!("{}", square(4));
}
```

```rust
/// 用户类型
struct User {
    id: u64,
}

fn main() {
    let u = User { id: 1 };
    println!("{}", u.id);
}
```

记忆法：/// 看下面；//! 看外层

**🐹 Go 对比：**
```go
package main

import "fmt"

// Package-level explanation usually lives in package comments.
func main() {
	fmt.Println("Go 没有 /// 和 //! 这组语法分工")
}
```

- **Go 怎么做**：包注释和符号注释都靠位置约定完成。
- **Rust 为什么不同**：Rust 用语法区分“注释谁”。
- **Go 程序员易踩的坑**：把 `//!` 放在函数前，期待它像 `///` 一样修饰下一项。

**小结 / 记忆点：**
- `///` 给下一项。
- `//!` 给外层模块或 crate。

---

## Q4. 文档注释支持哪些 Markdown？怎么生成 HTML？ {#q4}
**Tags:** `common` `rustdoc`
**适用版本:** rustdoc

**一句话答案：**
文档注释支持常见 Markdown；生成 HTML 文档用 `cargo doc`，想自动打开可加 `--open`。

**详细解答：**
文档注释里可以写 Markdown（标题、列表、代码块等）。下面这个程序里，`///` 下的 `# Examples` 与代码块会进入生成的 HTML：

```rust
/// 加法函数
///
/// # Examples
///
/// ```
/// assert_eq!(add(1, 2), 3);
/// ```
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(1, 2));
}
```

生成 / 预览 HTML 文档：

```bash
cargo doc
cargo doc --open
```

**🐹 Go 对比：**
```go
package main

import "fmt"

// Add adds two integers.
func Add(a, b int) int { return a + b }

func main() {
	fmt.Println(Add(1, 2))
}
```

- **Go 怎么做**：注释会进入 `go doc` / pkgsite。
- **Rust 为什么不同**：Rust 的 Markdown 代码块还能进一步变成 doctest。
- **Go 程序员易踩的坑**：以为 Rust 文档只是“渲染好看”，没意识到示例代码还能被编译检查。

**小结 / 记忆点：**
- `cargo doc --open` 是最省事的本地预览方式。

---

## Q5. doctest 是什么？为什么文档里的代码还能测？ {#q5}
**Tags:** `hot` `beginner` `doctest`
**适用版本:** cargo test 集成 rustdoc

**一句话答案：**
doctest 会从文档代码块里抽出 Rust 示例，再像测试一样编译甚至运行；所以文档示例不仅是“说明”，还是“可验证的说明”。

**详细解答：**
**doctest**（documentation test，文档测试）会从文档注释里的 Markdown 代码块抽出 Rust 示例，再像测试一样编译甚至运行。

**1. 被测 API + 文档注释里的写法**（注意：`///` 下面带 ` ``` ` 的那几行，是**写在文档注释里**的示例，不是独立 `.rs` 文件）：

```rust
/// 返回平方
///
/// ```
/// assert_eq!(square(3), 9);
/// ```
fn square(x: i32) -> i32 {
    x * x
}

fn main() {
    println!("{}", square(3));
}
```

**2. 运行文档测试：**

```bash
cargo test --doc
```

`rustdoc` 会把文档注释里的 ` ``` ` 代码块抽成独立 crate 再编译/运行；示例过时会直接变成测试失败，而不是静默骗人。

**🐹 Go 对比：**

- **Go 怎么做**：可写 `ExampleXxx` 风格测试。
- **Rust 为什么不同**：Rust 直接把示例代码放回文档注释里，离 API 更近。
- **Go 程序员易踩的坑**：把 Rust 文档示例当“随手写的伪代码”，结果过时后没人发现。

**小结 / 记忆点：**
- 能写 doctest 时，就尽量写真实可编译示例。

---

## Q6. doctest 想隐藏准备代码，但又想让它参与编译，怎么做？ {#q6}
**Tags:** `common` `doctest`
**适用版本:** rustdoc

**一句话答案：**
在 doctest 代码块里，把辅助行写成以 `#` 开头；它会参与编译，但渲染文档时默认隐藏。

**详细解答：**
doctest 里可用 `#` 隐藏准备代码：以 `#` 开头的行会参与编译，但渲染 HTML 时默认不显示。

**1. 被测 API（普通可编译程序）：**

```rust
/// 把两个数相加。
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    assert_eq!(add(2, 3), 5);
    println!("{}", add(2, 3));
}
```

**2. 文档注释里的完整 doctest 写法**（下面是 `///` 文档注释内容的示意，不是独立源文件；`#` 行在 HTML 里默认隐藏，但仍参与 `cargo test --doc`）：

```text
/// ```
/// # use my_crate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
```

读者只看到 `assert_eq!(...)`；`# use ...` 负责把示例补成可编译程序。

**🐹 Go 对比：**

- **Go 怎么做**：示例函数通常显式写完整上下文。
- **Rust 为什么不同**：Rust 文档希望既简洁可读，又能实际编译。
- **Go 程序员易踩的坑**：把隐藏行理解成 markdown 注释；其实它仍会进编译。

**小结 / 记忆点：**
- `#` 隐藏的是“展示”，不是“编译”。

---

## Q7. `#[...]` 和 `#![...]` 算注释吗？ {#q7}
**Tags:** `common` `attribute`
**适用版本:** Rust 1.0+

**一句话答案：**
不算。它们是属性（attribute），是给编译器看的指令，不是给人读的说明文字。

**详细解答：**
```rust
#![allow(dead_code)]

#[derive(Debug, Clone)]
struct User;

fn main() {
    println!("{:?}", User);
}
```

注释讲“为什么”，属性讲“编译器该怎么处理”

**🐹 Go 对比：**

- **Go 怎么做**：更多靠关键字、构建标记或工具约定表达。
- **Rust 为什么不同**：Rust 把很多编译器开关、派生、条件编译都收进了 attribute 语法。
- **Go 程序员易踩的坑**：把 `#[derive(...)]` 看成“特殊注释”；它其实会直接改变编译行为。

**小结 / 记忆点：**
- 注释解释给人看。
- 属性告诉编译器做什么。

---

## Q8. 想给私有函数也写文档，可以吗？ {#q8}
**Tags:** `common` `private`
**适用版本:** rustdoc

**一句话答案：**
可以；只是 `cargo doc` 默认主要展示公有 API，想把私有项也生成出来可用 `cargo doc --document-private-items`。

**详细解答：**
```rust
/// 私有帮助函数的说明
fn helper(x: i32) -> i32 {
    x + 1
}

fn main() {
    println!("{}", helper(1));
}
```

需要看私有项文档时：

```bash
cargo doc --document-private-items
```

**🐹 Go 对比：**

- **Go 怎么做**：对外 pkg 文档主要看导出符号。
- **Rust 为什么不同**：Rust 同样区分对外 API 和内部维护文档，但也给了显式开关查看私有项。
- **Go 程序员易踩的坑**：以为“私有函数不值得写文档”；实际复杂内部约束也常需要说明。

**小结 / 记忆点：**
- 私有项也能写文档，只是默认不总展示。

---

## Q9. 文档里怎么链接到别的类型、函数或方法？ {#q9}
**Tags:** `common` `intra-doc-links`
**适用版本:** rustdoc

**一句话答案：**
用文档内链接语法，例如 ``[`String`]``、``[`crate::foo`]``、`[Type::method]`；`rustdoc` 会尽量解析成符号链接。

**详细解答：**
```rust
/// 参见 [`String`]。
/// 也可看 [`crate::helper`]。
fn helper() {}

fn main() {
    helper();
}
```

文档断链时，rustdoc 通常会给警告

**🐹 Go 对比：**

- **Go 怎么做**：pkgsite 会帮部分符号生成导航。
- **Rust 为什么不同**：Rust 把“符号链接”直接做成文档语法习惯。
- **Go 程序员易踩的坑**：用普通 URL 链接符号名，结果重构后就失效；符号链接通常更稳。

**小结 / 记忆点：**
- 优先用符号链接，不要手写易过期的网址。

---

## Q10. 条件编译的项，文档里会怎么显示？ {#q10}
**Tags:** `occasional` `cfg`
**适用版本:** rustdoc

**一句话答案：**
会不会显示，取决于你生成文档时启用了哪些 feature / cfg；文档构建环境本身就是一次编译。

**详细解答：**
```rust
#[cfg(feature = "serde")]
fn with_serde() {}

fn main() {
    #[cfg(feature = "serde")]
    with_serde();
}
```

生成带 feature 的文档：

```bash
cargo doc --features serde
```

**🐹 Go 对比：**

- **Go 怎么做**：构建标签会影响参与编译的文件。
- **Rust 为什么不同**：Rust 通过 `cfg` 和 feature 更细粒度地控制“文档里能看到谁”。
- **Go 程序员易踩的坑**：以为文档总是“全量视图”；其实 feature 不同，文档内容也会不同。

**小结 / 记忆点：**
- 文档输出受 feature / cfg 影响。

---

## Q11. 想临时“注释掉一大块实现”，是用 `/* ... */` 还是 `cfg` 更好？ {#q11}
**Tags:** `occasional` `cfg`
**适用版本:** Rust 1.0+

**一句话答案：**
短期临时注释可以用 `/* ... */`，但要保留可编译备用实现时，通常 `#[cfg(...)]` 或 feature 开关更好。

**详细解答：**
```rust
#[cfg(feature = "experimental")]
fn experimental() {
    println!("on");
}

fn main() {
    println!("长期保留的备用实现，通常别靠大段注释");
}
```

```rust
fn main() {
    /* 临时注释少量代码还行 */
    println!("done");
}
```

**🐹 Go 对比：**

- **Go 怎么做**：长期条件差异通常靠 build tags 或不同文件。
- **Rust 为什么不同**：Rust 的 `cfg` / feature 更适合让“备用路径”保持可编译。
- **Go 程序员易踩的坑**：把过时代码整段注释着留仓库里，最后谁都不敢删。

**小结 / 记忆点：**
- 临时注释没问题，长期方案优先 `cfg`。

---

## Q12. `#[doc(hidden)]`、`#[doc(alias = ...)]` 这些进阶文档属性值得知道吗？ {#q12}
**Tags:** `advanced` `doc-attr`
**适用版本:** rustdoc

**一句话答案：**
值得知道，但不用一上来就到处用；它们适合在公共库里微调文档展示和搜索体验。

**详细解答：**
```rust
#[doc(hidden)]
fn internal_helper() {}

fn main() {
    internal_helper();
}
```

```rust
#[doc(alias = "connexion")]
fn connection() {}

fn main() {
    connection();
}
```

**🐹 Go 对比：**

- **Go 怎么做**：更多依赖导出命名和站点默认展示。
- **Rust 为什么不同**：Rust 文档系统可让库作者更细致地控制文档体验。
- **Go 程序员易踩的坑**：看到这些属性就过度设计；多数业务项目先把基础文档写清楚更重要。

**小结 / 记忆点：**
- 先把 `///`、`//!`、doctest 用好，再考虑进阶文档属性。

---

## Q13. `//!` 的 crate / 模块文档到底写在哪？ {#q13}
**Tags:** `common` `beginner` `module` `crate`
**适用版本:** Rust 1.0+

**一句话答案：**
crate 级文档写在 crate 根文件（`lib.rs` / `main.rs`）最顶部的 `//!`；模块级文档写在该模块文件顶部，或写在 `mod` 块内部开头——`//!` 注释的是“包围它的那一层”，不是后面那一项。

**详细解答：**
和 [Q3](#q3) 的分工一致：`//!` 看外层。实践里最常见的两个落点是：

**1. crate 根文档**——放在 `lib.rs`（或二进制 crate 的 `main.rs`）文件最上方：

```rust
//! 这是当前 crate 的总览文档。
//!
//! 读者打开 docs.rs / `cargo doc` 首页时，通常先看到这里。

fn helper() -> i32 {
    1
}

fn main() {
    println!("{}", helper());
}
```

**2. 模块文档**——放在模块文件开头，或内联 `mod` 块内部：

```rust
mod math {
    //! 数学小工具模块的说明写在这里。

    /// 平方函数（给下一项）
    pub fn square(x: i32) -> i32 {
        x * x
    }
}

fn main() {
    println!("{}", math::square(3));
}
```

「❌ 错误写法」——把 `//!` 放在函数前，指望它像 `///` 一样修饰函数：

```rust
//! 想给函数写文档，但位置错了：这会变成当前模块/crate 文档的一部分
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(1, 2));
}
```

这段往往能编译，但文档挂错对象：首页/模块页多了一段“函数说明”，而 `add` 自己反而没有 `///` 文档。

**🐹 Go 对比：**
```go
package main

import "fmt"

// Package-level comments in Go usually sit above `package` in a file.
func main() {
	fmt.Println("Go 靠文件位置约定，没有 //! 这种语法标记")
}
```

- **Go 怎么做**：包注释靠“放在 `package` 声明附近”的约定。
- **Rust 为什么不同**：用 `//!` / `///` 把“注释谁”写进语法，减少靠位置猜。
- **Go 程序员易踩的坑**：以为“文件顶部随便写 `//!` 就一定是 crate 文档”；若你其实在子模块文件里，那是模块文档。

**小结 / 记忆点：**
- crate 总览 → 根文件顶部 `//!`。
- 模块说明 → 模块内顶部 `//!`。
- 给函数/类型 → 用 `///`，别用 `//!`。

---

## Q14. `cargo doc --open` 和 README 谁算“正式文档”？ {#q14}
**Tags:** `common` `rustdoc` `readme`
**适用版本:** rustdoc / Cargo

**一句话答案：**
API 的正式文档是源码里的 `///` / `//!`（经 `rustdoc` / `cargo doc` 生成，公共库常见于 docs.rs）；README 是给人快速上手的项目说明。两者互补，不要互相替代。

**详细解答：**
[Q4](#q4) 说过：`cargo doc` / `cargo doc --open` 用来生成并预览 HTML。那份 HTML 来自代码旁的文档注释，反映的是**可链接、可检索、常带 doctest 的 API 契约**。

README（常见是仓库根目录的 `README.md`）回答另一类问题：这个 crate 是干什么的、怎么安装、最小示例、许可证与贡献指引。crates.io 页面会展示 README；docs.rs 主要展示 rustdoc。

```rust
//! 小型工具 crate：提供加法。

/// 把两个整数相加。
///
/// # Examples
///
/// ```
/// assert_eq!(add(1, 2), 3);
/// ```
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(1, 2));
}
```

本地预览 API 文档：

```bash
cargo doc --open
```

习惯分工可以记成：

| 载体 | 主要读者 | 典型内容 |
|------|----------|----------|
| `///` / `//!` + `cargo doc` | 库使用者查 API | 类型、函数签名、参数约束、示例测试 |
| `README.md` | 刚点进仓库 / crates.io 的人 | 动机、安装、快速开始、链接到 docs.rs |

「❌ 错误写法」——只在 README 里手写一份“伪 API 列表”，源码完全不写 `///`：重构后 README 过期，`cargo test --doc` 也帮不上忙。

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    // 能跑，但 API 文档几乎是空的；正式契约不该只活在 README 里
    println!("{}", add(2, 3));
}
```

**🐹 Go 对比：**

- **Go 怎么做**：`go doc` / pkgsite 吃源码注释；README 同样负责项目叙事。
- **Rust 为什么不同**：Rust 还把示例推进 doctest，API 文档更容易“过期即红”。
- **Go 程序员易踩的坑**：觉得“有 README 就够了”；对库作者来说，rustdoc 才是 API 主场。

**小结 / 记忆点：**
- API 正式文档 → 源码注释 + `cargo doc` / docs.rs。
- README → 上手与项目叙事。
- 两者都要，但职责不同。

---

## Q15. `[crate::...]` 文档内链写错了会怎样？怎么检查？ {#q15}
**Tags:** `common` `intra-doc-links` `rustdoc` `broken-link`
**适用版本:** rustdoc（建议配合 `RUSTDOCFLAGS`）

**一句话答案：**
链接目标解析失败时，**默认多半是 rustdoc 警告**（文档仍生成，但链是坏的或退化成普通文本）。把警告当错误：`RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links" cargo doc`，或在 crate 根 `#![deny(rustdoc::broken_intra_doc_links)]`。写法见 [Q9](#q9)。

**详细解答：**
写错路径的常见原因：模块路径过时、私有项默认不可链、拼错名字、`[`Foo`]` 有歧义未写全路径。

```rust
/// 错误示例：指向不存在的符号（跑 cargo doc 时会警告）
///
/// 参见 [`crate::does_not_exist`]。
pub fn demo() {}

fn main() {
    demo();
}
```

正确内链（目标真实存在）：

```rust
/// 参见 [`crate::helper`]。
pub fn helper() {}

/// 调用 [`helper`]。
pub fn run() {
    helper();
}

fn main() {
    run();
}
```

本地检查：

```bash
cargo doc
# 把断链当失败（CI 常用）：
# RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links" cargo doc --no-deps
```

crate 根也可以：

```rust
//! 示例 crate 文档。
#![deny(rustdoc::broken_intra_doc_links)]

fn main() {}
```

「❌ 错误预期」——以为「文档能打开就等于链接都对」：HTML 生成成功仍可能满屏 unresolved link 警告。

**🐹 Go 对比：**

- **Go 怎么做**：注释里的标识符不会像 rustdoc 这样系统解析；坏链接更常靠人工点 pkgsite。
- **Rust 为什么不同**：intra-doc link 是一等语法，工具能在构建文档时验。
- **Go 程序员易踩的坑**：忽略 `cargo doc` 警告，合并后 docs.rs 上才发现断链。

**小结 / 记忆点：**
- 写错 → 通常警告，不是默默「编译失败」。
- CI / 本地用 `-D rustdoc::broken_intra_doc_links` 验。
- 重构模块路径后记得重跑 `cargo doc`。

---
