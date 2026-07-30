+++
title = "24-testing"
date = 2026-07-28T14:49:00+08:00
weight = 240
type = "docs"
description = "面向 Go 用户讲清 Rust 单元/集成/文档测试、断言、cargo test 过滤与表驱动写法"
isCJKLanguage = true
draft = false

+++

# 测试 (Testing)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会分不清：单元测试、集成测试、文档测试该写在哪、能不能测私有函数？
- 你是否想知道：`#[cfg(test)] mod tests` 怎么写，和 Go 的 `_test.go` 差在哪？
- 你是否分不清 `assert!` / `assert_eq!` / `assert_ne!` / `debug_assert!` 该用哪个？
- 你是否想只跑一个测试、看 `println!` 输出，却不知道 `cargo test` 的过滤与 `--` 参数？
- 你是否想把 Go 的表驱动测试平移到 Rust，或写回归测试锁住修过的 bug？
- 你会不会在 CI 里 `cargo test` 偶发失败、锁文件漂移，不知道该加哪些开关？
- 你是否想做属性测试、mock HTTP 上游、或测 CLI 二进制（`proptest` / wiremock / `assert_cmd`）？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| unit test | — | 单元测试 | 通常写在源码旁，可测私有项 | 同包 `_test.go` |
| integration test | — | 集成测试 | `tests/` 下独立 crate，只测公共 API | 外部测试包 `package foo_test` |
| doctest | documentation test | 文档测试 | 文档注释里的代码块会被编译执行 | `ExampleXxx` |
| test harness | — | 测试运行器 | `cargo test` 背后收集并跑 `#[test]` 的程序 | `go test` 运行器 |
| `#[cfg(test)]` | configuration attribute | 仅测试配置 | 只在 `cargo test` 时编译该块 | 类似 `//go:build` 限定测试文件 |
| `assert_eq!` | — | 相等断言宏 | 失败时打印左右两边的值 | `if got != want { t.Fatalf(...) }` |
| `should_panic` | — | 期望 panic | 声明测试按设计应 panic | `defer` + `recover` |
| `nocapture` | — | 不捕获输出 | 让测试的 stdout/stderr 实时打印 | `go test -v` 的一部分效果 |
| table-driven | — | 表驱动测试 | 一组输入/期望值循环跑同一逻辑 | Go 经典表驱动 |
| CI | Continuous Integration | 持续集成 | 推送/PR 时自动跑测试的流水线 | 同概念 |
| mock / test double | — | 测试替身 | 测试里替换真实依赖的假实现 | interface + fake / gomock |
| `mockall` | — | mock 生成库 | 从 trait 生成可编排的 mock 类型 | gomock / testify/mock |
| **proptest** | — | 属性测试库 | 随机生成输入验证不变量 | testing/quickcheck 一类 |
| **wiremock** | — | HTTP mock 服务 | 测试里起假 HTTP 上游 | `httptest` + 自研 mock server |
| **assert_cmd** | — | CLI 断言库 | 跑二进制并断言退出码/输出 | 测 `main` 的黑盒方式 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q8](#q8), [Q10](#q10), [Q21](#q21), [Q22](#q22) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q11](#q11), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q19](#q19), [Q20](#q20), [Q23](#q23) |
| `occasional` | [Q12](#q12), [Q18](#q18) |
| `advanced` | — |

---

## Q1. 单元测试、集成测试、文档测试分别放哪？可见性有什么差别？ {#q1}
**Tags:** `hot` `beginner` `unit-test` `integration-test` `doctest`
**适用版本:** Rust 1.0+

**一句话答案：**
单元测试写在源码旁（常放 `#[cfg(test)] mod tests`），能测私有项；集成测试放 `tests/`，是独立 crate，只能测公共 API；文档测试写在 `///` 代码块里，随 `cargo test` 一起跑。

**解答：**
三者的差别不只是“文件放哪儿”，更是**可见性边界**不同。

| 种类 | 常见位置 | 可见性 | 和被测代码的关系 |
|------|----------|--------|------------------|
| 单元测试 | `src/*.rs` 内 | 可访问 `pub(crate)` / 私有项（同模块树） | 同一 crate |
| 集成测试 | `tests/*.rs` | 只能 `use` 公共 API | 每个文件 ≈ 独立 crate |
| 文档测试 | `///` / `//!` 里的 markdown 代码块 | 只能用文档里能写出来的公共用法 | 像“用户复制粘贴” |

典型布局：

```text
my_crate/
  src/
    lib.rs          # 可写 #[cfg(test)] mod tests { ... }
    math.rs         # 也可就近放单元测试
  tests/
    api.rs          # 集成测试：只能 use my_crate::...
```

源码内单元测试示意（完整可测片段需放在 lib/crate 里；下面是常见写法）：

```rust
// 测试片段：放在 src/lib.rs 或模块文件末尾
fn private_add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn private_add_works() {
        assert_eq!(private_add(2, 3), 5);
    }
}
```

文档测试同时是示例和回归：

```rust
/// 把两个 `i32` 相加。
///
/// ```
/// assert_eq!(2 + 2, 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

**Go 对比：**
- **Go 怎么做**：同包 `_test.go` 可测未导出符号；`package foo_test` 只能测导出 API；另有 `Example` 函数。
- **Rust 为什么不同**：把“源码内测试 / `tests/` 黑盒 / 文档即测试”三套路径都挂在统一的 `cargo test` 上。
- **Go 程序员易踩的坑**：以为 `tests/` 里也能测私有函数——不能，那是独立 crate。

**记忆点：**
- 私有实现细节 → 源码内单元测试。
- 公共契约 → `tests/` 集成测试。
- 给用户看的最小用法 → 文档测试。

---

## Q2. `#[cfg(test)] mod tests` 标准写法是什么？ {#q2}
**Tags:** `hot` `beginner` `cfg(test)`
**适用版本:** Rust 1.0+

**一句话答案：**
在模块末尾加 `#[cfg(test)] mod tests { use super::*; #[test] fn ... }`：只在跑测试时编译，并用 `super::*` 引入被测项。

**解答：**
**`#[cfg(test)]`**（configuration attribute，配置属性）表示：这段代码只在 **测试配置** 下编译——`cargo build` / `cargo run` 不会带上它，`cargo test` 才会。

```rust
pub fn clamp(n: i32, lo: i32, hi: i32) -> i32 {
    n.max(lo).min(hi)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clamps_below_lo() {
        assert_eq!(clamp(-1, 0, 10), 0);
    }

    #[test]
    fn clamps_above_hi() {
        assert_eq!(clamp(99, 0, 10), 10);
    }
}
```

`#[test]` 标记的函数由 **test harness**（测试运行器）发现并执行；函数名会出现在 `cargo test` 输出里，也是过滤用的名字。

「❌ 错误写法」——把 `mod tests` 写成普通模块却忘记 `#[cfg(test)]`：正式构建也会编译测试代码，还可能拉进仅测试用的依赖。

「✅ 正确写法」——始终加 `#[cfg(test)]`；需要共享测试辅助函数时，可再拆 `#[cfg(test)] mod common;` 之类，同样只在测试时编译。

**Go 对比：**
- **Go 怎么做**：文件名以 `_test.go` 结尾，构建时自动排除出普通包。
- **Rust 为什么不同**：测试可以嵌在同一 `.rs` 文件里，所以用属性控制“何时编译”，而不是靠文件名后缀。
- **Go 程序员易踩的坑**：到处新建 `*_test.rs` 文件名——Rust 不认这个约定；集成测试目录才是 `tests/`。

**记忆点：**
- `#[cfg(test)]` + `mod tests` + `use super::*` + `#[test]`。
- 测试模块默认是子模块，能访问父模块私有项。

---

## Q3. `assert!`、`assert_eq!`、`assert_ne!`、`debug_assert!` 怎么选？ {#q3}
**Tags:** `hot` `assert`
**适用版本:** Rust 1.0+

**一句话答案：**
布尔条件用 `assert!`；比相等用 `assert_eq!`；比不等用 `assert_ne!`；只想在 debug 构建保留的内部检查用 `debug_assert!`（release 默认关掉）。

**解答：**
失败时 `assert_eq!` / `assert_ne!` 会打印左右值，排查通常比纯布尔 `assert!` 更省事。

```rust
fn main() {
    let xs = [2, 4, 6];
    assert!(xs.iter().all(|n| n % 2 == 0));
    assert_eq!(xs.len(), 3);
    assert_ne!(xs[0], xs[1]);
}
```

`debug_assert!` 适合“开发期自检、生产期嫌贵”的不变量；**不能**把它当成业务正确性的唯一保障。

```rust
fn sorted_ok(values: &[i32]) -> bool {
    for w in values.windows(2) {
        debug_assert!(w[0] <= w[1], "helper assumes sorted input");
    }
    true
}

fn main() {
    assert!(sorted_ok(&[1, 2, 3]));
}
```

在测试里一般直接用 `assert!` / `assert_eq!`：测试本来就该在所有配置下执行断言。`debug_assert!` 更适合库内部热路径上的可选检查。

**Go 对比：**
- **Go 怎么做**：常见 `if got != want { t.Fatalf("got %v want %v", got, want) }`。
- **Rust 为什么不同**：标准库宏统一了相等/不等失败信息格式。
- **Go 程序员易踩的坑**：习惯写 `assert!(a == b)`——能用，但失败时看不到 `a`/`b` 的值；优先 `assert_eq!`。

**记忆点：**
- 比两个值 → `assert_eq!` / `assert_ne!`。
- 比条件 → `assert!`。
- `debug_assert!` ≠ 生产业务断言。

---

## Q4. 怎么只跑一个测试？`--exact`、`--nocapture`、`--test-threads=1` 分别干什么？ {#q4}
**Tags:** `hot` `cargo-test` `filter`
**适用版本:** Cargo（随 rustup 工具链）

**一句话答案：**
用名字子串过滤；`-- --exact` 精确匹配全名；`-- --nocapture` 实时看 stdout；`-- --test-threads=1` 强制串行。注意：`--` 后面才是传给测试 harness 的参数。

**解答：**
`cargo test` 的参数分两段：Cargo 自己的选项，以及 `--` 之后转发给 harness 的选项。

```bash
# 名字里带 parser 的都跑（子串匹配）
cargo test parser

# 精确匹配完整测试名（含模块路径时要写全）
cargo test tests::handles_empty -- --exact

# 看 println! / dbg! 输出
cargo test handles_empty -- --nocapture

# 强制单线程，排查测试互相抢文件/端口
cargo test -- --test-threads=1
```

组合也很常见：

```bash
cargo test parser::case_a -- --exact --nocapture
```

对应 Go 的肌肉记忆：`go test -run '^TestFoo$' -v` ≈ 过滤 + 详细输出；Rust 把“详细输出”拆成了默认捕获 + 可选 `nocapture`。

**Go 对比：**
- **Go 怎么做**：`go test -run TestName`、`-v`、`-parallel 1` / `t.Parallel()` 控制。
- **Rust 为什么不同**：Cargo 与 harness 参数用 `--` 分隔，初学者常把 `--nocapture` 写在 `--` 前面导致无效。
- **Go 程序员易踩的坑**：写成 `cargo test --nocapture`（少了中间的 `--`）。

**记忆点：**
- 过滤名在 `cargo test <filter>`。
- harness 开关一律 `cargo test -- <flags>`。
- 串行是排查共享状态的手段，不是长期默认。

---

## Q5. `#[should_panic]` 适合测什么？怎么写 `expected`？ {#q5}
**Tags:** `common` `should_panic`
**适用版本:** Rust 1.0+

**一句话答案：**
只适合“按 API 契约就应该 panic”的路径；用 `expected = "..."` 锁定 panic 消息片段，避免“换了个无关 panic 却仍算通过”。

**解答：**
普通业务失败应测 `Result::Err`，不要用 panic 冒充错误处理。

```rust
// 测试片段
fn boom(msg: &str) -> ! {
    panic!("{msg}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "bad index")]
    fn panics_with_message() {
        boom("bad index");
    }
}
```

边界检查类 panic：

```rust
// 测试片段
#[test]
#[should_panic(expected = "index out of bounds")]
fn slice_index_panics() {
    let xs = [1, 2, 3];
    let _ = xs[10];
}
```

**Go 对比：**
- **Go 怎么做**：`defer func(){ if recover() == nil { t.Fatal(...) } }()`。
- **Rust 为什么不同**：把“期望崩溃”做成一等测试属性。
- **Go 程序员易踩的坑**：把所有 `Err` 路径都改成 panic 再 `should_panic`——风格和可测试性都会变差。

**记忆点：**
- 契约是 panic → `#[should_panic(expected = "...")]`。
- 契约是错误值 → 测 `Result`。

---

## Q6. `#[ignore]` 干什么？怎么跑被忽略的测试？ {#q6}
**Tags:** `common` `ignore`
**适用版本:** Rust 1.0+；`--include-ignored` 为较新 harness 行为（日常 Cargo 均支持）

**一句话答案：**
`#[ignore]` 标记默认不跑的慢测/需外部资源的测；需要时用 `cargo test -- --ignored` 或 `-- --include-ignored`。

**解答：**

```rust
// 测试片段
#[test]
#[ignore = "需要真实数据库，本地默认跳过"]
fn talks_to_real_db() {
    // 连接真实 DB 的集成场景…
}
```

```bash
# 只跑被 ignore 的
cargo test -- --ignored

# 普通 + ignored 一起跑
cargo test -- --include-ignored
```

适合：慢、贵、依赖密钥/真机服务、或会污染环境的用例。日常 `cargo test` 应保持快反馈。

**Go 对比：**
- **Go 怎么做**：`testing.Short()`、build tag、或手写 `t.Skip`。
- **Rust 为什么不同**：用属性 + harness 开关集中控制，入口统一。
- **Go 程序员易踩的坑**：把不该默认跑的重测留在主路径，拖慢每个人的本地循环。

**记忆点：**
- 慢测 / 外依赖 → `#[ignore]`。
- CI 夜间任务可显式 `--ignored`。

---

## Q7. 测试函数可以返回 `Result` 吗？为什么方便？ {#q7}
**Tags:** `common` `Result` `?`
**适用版本:** Rust 1.0+（测试里用 `?` 的习惯随时代普及）

**一句话答案：**
可以：`fn test_foo() -> Result<(), E>`，失败时 harness 会把 `Err` 当成测试失败；这样能在测试里直接用 `?`，少写一堆 `unwrap`。

**解答：**

```rust
fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.trim().parse()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_trimmed() -> Result<(), std::num::ParseIntError> {
        let port = parse_port(" 8080 ")?;
        assert_eq!(port, 8080);
        Ok(())
    }

    #[test]
    fn rejects_garbage() {
        assert!(parse_port("nope").is_err());
    }
}
```

注意：返回 `Result` 适合“设置阶段可能失败”的测试；断言失败仍用 `assert_*!`（它们是 panic，不是 `Err`）。

**Go 对比：**
- **Go 怎么做**：`got, err := f(); if err != nil { t.Fatal(err) }`。
- **Rust 为什么不同**：测试签名允许 `Result`，`?` 直接把错误冒泡给 harness。
- **Go 程序员易踩的坑**：全程 `unwrap()`，失败信息只剩 panic，不如 `?` + 明确 `Err` 清晰。

**记忆点：**
- 准备数据用 `?`；断言用 `assert_*!`；最后 `Ok(())`。

---

## Q8. 为什么集成测试只能测公共 API？私有函数测不了怎么办？ {#q8}
**Tags:** `hot` `integration-test` `visibility`
**适用版本:** Rust 1.0+

**一句话答案：**
`tests/*.rs` 每个文件都是依赖你库的**独立 crate**，和外部用户一样，只能 `use` 你的 `pub` 项；私有逻辑请放单元测试，或抽成可测的小 `pub(crate)` / 子模块 API。

**解答：**
假设库名是 `billing`：

```rust
// src/lib.rs
pub fn invoice_total(cents: &[u32]) -> u32 {
    cents.iter().sum()
}

fn secret_discount(_: u32) -> u32 {
    0 // 私有，集成测试碰不到
}
```

```rust
// tests/invoice.rs —— 集成测试片段
use billing::invoice_total;

#[test]
fn sums_line_items() {
    assert_eq!(invoice_total(&[100, 250]), 350);
}
```

「❌」在 `tests/` 里写 `use billing::secret_discount`——私有项不可见，编译失败。

「✅」两种合法策略：
1. 私有细节用 `src` 内 `[cfg(test)]` 单元测试覆盖（见 [Q2](#q2)）。
2. 若必须从外部测，把它提升为有意的公共（或 `pub(crate)` 再配合单元测试）API，并写清文档。

**Go 对比：**
- **Go 怎么做**：`package billing_test` 同样只能测导出符号；同包测试可测未导出。
- **Rust 为什么不同**：`tests/` ≈ 永远是外部测试包；同文件/子模块单元测试承担“白盒”角色。
- **Go 程序员易踩的坑**：把所有测试都扔进 `tests/`，结果大量实现细节测不到。

**记忆点：**
- 集成测试 = 黑盒用户视角。
- 白盒 = 源码内 `#[cfg(test)]`。

---

## Q9. 文档测试最值得测什么？`ignore` / `no_run` 何时用？ {#q9}
**Tags:** `common` `doctest`
**适用版本:** Rust 1.0+

**一句话答案：**
最值得测公共 API 的**最短正确用法**；`ignore` 跳过执行（仍可文档展示），`no_run` 只编译不运行（适合会阻塞或需环境的示例）。

**解答：**
文档测试失败 = 用户复制的第一段示例就挂了，信任成本很高。

文档注释里写可执行示例（以下为库代码示意；真正的文档测试代码块写在 `///` 下面）：

```rust
/// 返回平方。
///
/// 文档里放一段可运行示例，例如：
/// assert_eq!(square(4), 16);
/// 以 `# ` 开头的辅助行可在渲染文档时隐藏，但仍参与编译。
pub fn square(n: i32) -> i32 {
    n * n
}
```

特殊标记写在文档代码块的语言标签旁：

- `ignore`：跳过该示例（仍可展示在文档里）
- `no_run`：只编译、不执行（适合会阻塞或依赖外部环境的示例）
- 默认可跑：最短公共 API 用法，随 `cargo test` / `cargo test --doc` 执行

例如：需要网络的示例标 `ignore`；只想证明 `TcpListener::bind` 能编译、不要真 listen 的示例标 `no_run`。

还有 `compile_fail`（故意展示编译失败示例）等，日常库文档最常用的是默认可跑、`no_run`、`ignore`。

**Go 对比：**
- **Go 怎么做**：`Example` 函数，输出用注释里的 `// Output:` 比对。
- **Rust 为什么不同**：几乎任何 `///` 代码块默认可测，社区更强调“文档能编译”。
- **Go 程序员易踩的坑**：文档里贴伪代码，Rust 里默认会挂 `cargo test`。

**记忆点：**
- 文档示例要短、真、跟 API 同步。
- 编译即可 / 别执行 → `no_run`；完全跳过 → `ignore`。

---

## Q10. 怎么写表驱动测试？和 Go 的 table-driven 怎么对应？ {#q10}
**Tags:** `hot` `table-driven`
**适用版本:** Rust 1.0+

**一句话答案：**
用数组/切片存 `(输入, 期望)`，`for` 循环里 `assert_eq!`；失败时在断言消息里带上 case 名，定位方式和 Go 几乎一样。

**解答：**

```rust
fn is_even(n: i32) -> bool {
    n % 2 == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn evenness_cases() {
        let cases = [
            ("zero", 0, true),
            ("two", 2, true),
            ("three", 3, false),
            ("neg", -4, true),
        ];
        for (name, input, want) in cases {
            assert_eq!(is_even(input), want, "case {name}");
        }
    }
}
```

也可以每个 case 一个小闭包/结构体字段，但“一张表 + 循环”对 Go 转来的人最熟。

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn parse_ok_cases() {
        struct Case {
            name: &'static str,
            input: &'static str,
            want: u16,
        }
        let cases = [
            Case { name: "plain", input: "80", want: 80 },
            Case { name: "trim", input: " 443 ", want: 443 },
        ];
        for c in cases {
            let got: u16 = c.input.trim().parse().expect(c.name);
            assert_eq!(got, c.want, "{}", c.name);
        }
    }
}
```

**Go 对比：**
- **Go 怎么做**：

```go
func TestEven(t *testing.T) {
    cases := []struct {
        name  string
        input int
        want  bool
    }{
        {"zero", 0, true},
        {"three", 3, false},
    }
    for _, c := range cases {
        t.Run(c.name, func(t *testing.T) {
            if got := c.input%2 == 0; got != c.want {
                t.Fatalf("got %v want %v", got, c.want)
            }
        })
    }
}
```

- **Rust 为什么不同**：没有内建 `t.Run` 子测试分层（可用第三方或宏，但标准库够用就是循环 + 消息）。
- **Go 程序员易踩的坑**：忘了在 `assert_eq!` 里带 case 名，失败时不知道是哪一行数据。

**记忆点：**
- 表 = 数据；循环 = 同一断言。
- 断言消息带上 `name`。

---

## Q11. `cargo test --lib` / `--test` / `--doc` 分别跑哪些？ {#q11}
**Tags:** `common` `cargo-test` `filter-target`
**适用版本:** Cargo

**一句话答案：**
`--lib` 只跑库的单元测试；`--test <name>` 只跑 `tests/<name>.rs` 那个集成测试目标；`--doc` 只跑文档测试。用来缩小范围、加快反馈。

**解答：**

```bash
# 默认：单元 + 集成 + 文档（按项目目标而定）
cargo test

# 只跑 src 里的单元测试（库）
cargo test --lib

# 只跑名为 api 的集成测试（对应 tests/api.rs）
cargo test --test api

# 只跑文档测试
cargo test --doc

# 二进制目标上的单元测试（若有）
cargo test --bin mybin
```

过滤名仍可叠加：

```bash
cargo test --lib parser
cargo test --doc square
```

**Go 对比：**
- **Go 怎么做**：`go test ./...`、指定包路径、`-run` 过滤。
- **Rust 为什么不同**：Cargo 按 **target**（lib / bin / test / example / doc）切开，比“按目录包”更细。
- **Go 程序员易踩的坑**：文档测试挂了却一直只跑 `--lib`，误以为全绿。

**记忆点：**
- 改实现细节 → `--lib`。
- 改公共 API 契约 → `--test` / 全量。
- 改文档示例 → `--doc`。

---

## Q12. 异步测试怎么写？一定要 tokio 吗？ {#q12}
**Tags:** `occasional` `async`
**适用版本:** 稳定 Rust 本身不提供 async test 属性；需选运行时生态（如 Tokio）

**一句话答案：**
标准库没有 `#[async_test]`；常见做法是依赖 **Tokio** 等运行时的 `#[tokio::test]`，或自己在同步 `#[test]` 里 `block_on`。这是生态选择，不是语言内建。

**解答：**
最小依赖示意（需在 `Cargo.toml` 加 dev-dependency）：

```toml
# Cargo.toml 片段
[dev-dependencies]
tokio = { version = "1", features = ["macros", "rt"] }
```

```rust
// 测试片段：需要上述 tokio dev-dependency
#[tokio::test]
async fn adds_async() {
    async fn add(a: i32, b: i32) -> i32 { a + b }
    assert_eq!(add(1, 2).await, 3);
}
```

若不想在测试里拉宏，也可以：

```bash
# 命令级思路：同步测试里手动跑 runtime（伪流程，按你选的 runtime 改）
# 1) cargo add --dev tokio --features rt,macros
# 2) #[test] fn t() { tokio::runtime::Runtime::new().unwrap().block_on(async { ... }) }
```

异步主题细节见 [31-async-programming](../31-async-programming.md)；本篇只强调：**测 async 代码 = 先选定 runtime，再按其测试宏/阻塞 API 写**。

**Go 对比：**
- **Go 怎么做**：测试里直接调返回的函数；goroutine 测试用 channel/`WaitGroup`，无单独 async 关键字。
- **Rust 为什么不同**：`async fn` 产生 Future，必须有执行器驱动。
- **Go 程序员易踩的坑**：写了 `async fn` 测试却不加 runtime，结果 Future 根本没跑。

**记忆点：**
- Async 测试是生态能力，不是 `cargo test` 内建。
- 选 Tokio 就用 `#[tokio::test]`（或等价 `block_on`）。

---

## Q13. 修完 bug 后怎样写一条有价值的回归测试？ {#q13}
**Tags:** `common` `regression`
**适用版本:** Rust 1.0+

**一句话答案：**
把**当初触发 bug 的最小输入**固化成 `#[test]`，断言只锁住这次修复的行为；别塞进 `main`，也别顺手断言半个系统。

**解答：**
「❌」只在 `main` 里临时试跑——`cargo test` 不会当回归：

```rust
fn normalize_port(input: &str) -> Result<u16, std::num::ParseIntError> {
    input.trim().parse()
}

fn main() {
    // 手动试跑 ≠ 回归测试
    assert_eq!(normalize_port(" 8080 ").unwrap(), 8080);
}
```

「✅」用 `#[test]` 锁最小复现：

```rust
fn normalize_port(input: &str) -> Result<u16, std::num::ParseIntError> {
    input.trim().parse()
}

#[cfg(test)]
mod tests {
    use super::*;

    // 历史 bug：首尾空格导致解析失败
    #[test]
    fn trims_whitespace_before_parse() {
        assert_eq!(normalize_port(" 8080 ").unwrap(), 8080);
    }
}
```

```bash
cargo test trims_whitespace_before_parse -- --exact
```

**Go 对比：**
- **Go 怎么做**：同样把事故输入做成 `TestXxx` / 表驱动一行。
- **Rust 为什么不同**：额外常把边界压进类型系统，但**行为回归仍要靠测试**。
- **Go 程序员易踩的坑**：修复 PR 不带复现用例，几周后同样输入再破一次。

**记忆点：**
- 最小输入 + 相关断言 + `#[test]`。
- 回归测试名字最好能读出“曾经坏在哪”。

---

## Q14. 测试里为什么看不到 `println!`？`dbg!` 该怎么用？ {#q14}
**Tags:** `common` `nocapture` `dbg!`
**适用版本:** `dbg!` 需 Rust 1.32+；输出捕获为 Cargo 测试 harness 行为

**一句话答案：**
harness **默认捕获** stdout/stderr，通过的测试通常不展示打印；要实时看输出用 `-- --nocapture`。临时观察表达式优先 `dbg!`（带文件位置且返回原值）。

**解答：**

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn inspect_values() {
        let xs = vec![1, 2, 3];
        let doubled: Vec<_> = dbg!(xs.iter().map(|n| n * 2).collect());
        assert_eq!(doubled, vec![2, 4, 6]);
        println!("also here: {doubled:?}");
    }
}
```

```bash
cargo test inspect_values -- --nocapture
```

失败时 harness 常会把捕获到的输出一并展示，所以“先让断言失败”有时也能看到日志；但主动排查时 `nocapture` 更直接。

`dbg!` 是开发期探针，测完应删或改成正式断言；不要把 `dbg!` 留在库的非测试路径当日志系统。

**Go 对比：**
- **Go 怎么做**：`t.Log` / `t.Logf`，配合 `go test -v` 才稳定可见。
- **Rust 为什么不同**：默认捕获所有 stdout，行为更“安静”。
- **Go 程序员易踩的坑**：以为没执行到 `println!`，其实只是被捕获了。

**记忆点：**
- 看不见打印 → 先加 `-- --nocapture`。
- 看中间值 → `dbg!`；看完就删。

---

## Q15. CI 里跑 `cargo test` 要注意什么？（`--locked` 等） {#q15}
**Tags:** `common` `CI` `locked`
**适用版本:** Cargo

**一句话答案：**
CI 应用锁文件复现构建：`cargo test --locked`（或 `--frozen`）；固定工具链；需要时分开 `--lib` / `--doc`；对共享状态测试考虑 `--test-threads=1`；别在 CI 默默 `cargo update`。

**解答：**
常见稳健命令组合：

```bash
# 按 Cargo.lock 解析依赖；锁文件与 Cargo.toml 不一致则失败
cargo test --locked

# 更严：禁止更新锁文件，也不许联网改依赖（视 CI 网络策略）
cargo test --frozen

# 工作区
cargo test --workspace --locked

# 输出与串行（排障 job 用）
cargo test --locked -- --nocapture --test-threads=1
```

实务建议：
1. **提交 `Cargo.lock`**（对应用/bin 几乎总是；对纯库团队可另有约定，但 CI 仍应可复现）。
2. **固定 rust 版本**（`rust-toolchain.toml` 或 CI image 钉死 1.97.1 一类）。
3. **缓存** `target/` / registry 时，仍要用 `--locked` 防止“我机器能过、CI 解析出另一组依赖”。
4. 文档测试、忽略测试：按需加 `cargo test --doc`、夜间 `-- --ignored`。

**Go 对比：**
- **Go 怎么做**：`go test ./...`，依赖 `go.sum`；CI 常用 `go test -count=1` 关缓存。
- **Rust 为什么不同**：强调 `Cargo.lock` + `--locked`，和 feature / target 矩阵更复杂。
- **Go 程序员易踩的坑**：CI 不带 `--locked`，某天传递依赖静默升级导致红。

**记忆点：**
- CI：`cargo test --locked`（或 `--frozen`）。
- 钉工具链 + 可复现依赖 = 少见鬼。

---

## Q16. 二进制项目（有 `main`）的测试写在哪？ {#q16}
**Tags:** `common` `bin` `lib`
**适用版本:** Rust 1.0+

**一句话答案：**
逻辑尽量放进 `src/lib.rs`（或模块），用 `--lib` 测；`src/main.rs` 只做薄封装。若坚持测 bin，可用 `tests/` 调公共 API，或 `#[cfg(test)]` 写在可引用的模块里。

**解答：**
推荐结构：

```text
src/
  lib.rs     # 业务函数 + 单元测试
  main.rs    # fn main() { app::run() }
tests/
  cli_smoke.rs
```

```rust
// src/lib.rs
pub fn greet(name: &str) -> String {
    format!("hello, {name}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greet_formats() {
        assert_eq!(greet("rust"), "hello, rust");
    }
}
```

```text
// src/main.rs —— crate 名按 Cargo.toml 的 [package].name 替换
fn main() {
    println!("{}", my_app::greet("world"));
}
```

（上例仅示意“main 调用 lib”；真正工程里把 `my_app` 换成你的包名。）

只把代码堆在 `main.rs` 且不拆 lib 时，单元测试与复用都会别扭——这是 Go 里 “把逻辑放出 `main` 包” 的同一类建议。

**Go 对比：**
- **Go 怎么做**：`package main` 可测，但大项目常拆内部包。
- **Rust 为什么不同**：`main` 二进制 crate 对集成测试的暴露方式与 lib 不同，**先 lib 后 bin** 最省心。
- **Go 程序员易踩的坑**：全部写在 `main.rs`，然后奇怪为什么不好写 `tests/`。

**记忆点：**
- 可测逻辑进 lib；main 保持瘦。

---

## Q17. 一个测试里失败了，怎样快速定位是断言还是 panic？ {#q17}
**Tags:** `common` `failure` `backtrace`
**适用版本:** Rust 1.0+

**一句话答案：**
断言失败通常带 `assertion failed` / `left == right`；未捕获 panic 是另一类。需要调用栈时设 `RUST_BACKTRACE=1`（或 `full`）再跑该测试。

**解答：**

```bash
# 只跑失败用例并看输出
cargo test path::to::failing -- --exact --nocapture

# Windows PowerShell
$env:RUST_BACKTRACE=1; cargo test path::to::failing -- --exact

# Unix
RUST_BACKTRACE=1 cargo test path::to::failing -- --exact
```

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn shows_eq_failure() {
        // 失败时会看到 left/right
        assert_eq!(1 + 1, 3);
    }
}
```

`RUST_BACKTRACE` 只影响 **panic** 报告；普通 `Result` 错误返回不会因此多出栈。测试失败本质常是断言宏内部 `panic!`，所以 backtrace 对深嵌套辅助函数很有用。

**Go 对比：**
- **Go 怎么做**：失败默认带文件:行号；panic 自带栈。
- **Rust 为什么不同**：默认 panic 报告更短，要栈就开环境变量。
- **Go 程序员易踩的坑**：只看最后一行 panic 文案，不打开 backtrace，找不到真正调用点。

**记忆点：**
- 先缩到单个测试 + `nocapture`。
- panic / 断言搞不清时开 `RUST_BACKTRACE=1`。

---

## Q18. 测试之间如何共享夹具？有没有“全局 Setup”？ {#q18}
**Tags:** `occasional` `fixture`
**适用版本:** Rust 1.0+

**一句话答案：**
标准库没有 JUnit 式全局 `@BeforeAll`；用普通函数/模块当夹具，或在每个测试开头调用。跨测试共享可变全局态要非常谨慎，优先每个测试自建数据。

**解答：**

```rust
fn sample_users() -> Vec<String> {
    vec!["alice".into(), "bob".into()]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn user_count() {
        let users = sample_users();
        assert_eq!(users.len(), 2);
    }

    #[test]
    fn first_user() {
        let users = sample_users();
        assert_eq!(users[0], "alice");
    }
}
```

需要临时目录等资源时，优先看 [Q19](#q19)；并行默认开启时，共享文件名/端口容易 flaky——要么隔离资源名，要么临时 `-- --test-threads=1`（见 [Q4](#q4)）。

**Go 对比：**
- **Go 怎么做**：`TestMain`、子测试 `t.Run`、或自行 `setup()`。
- **Rust 为什么不同**：保持测试为普通函数 + 属性，夹具即语言层函数复用。
- **Go 程序员易踩的坑**：用 `static mut` / 懒加载全局客户端且不加锁，并行下偶发失败。

**记忆点：**
- 夹具 = 函数；每个测试自建数据更稳。
- 共享可变全局是 flaky 重灾区。

---

## Q19. 测试里写临时文件 / 临时目录怎么做？ {#q19}
**Tags:** `common` `tempfile` `filesystem`
**适用版本:** Rust 1.0+（标准库路径）；`tempfile` crate 为第三方

**一句话答案：**

标准库可用 `std::env::temp_dir()` + 唯一子路径，测完再 `remove_file` / `remove_dir_all`；也可以自制极简 `TempDir`（`Drop` 里清理）。生产测试更常把 `tempfile` 写进 `[dev-dependencies]`（本篇用 text 点到为止）。

**解答：**

最小自制临时目录（可编译）：

```rust
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

struct TempDir {
    path: PathBuf,
}

impl TempDir {
    fn new(prefix: &str) -> std::io::Result<Self> {
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let path = std::env::temp_dir().join(format!("{prefix}-{nanos}"));
        fs::create_dir_all(&path)?;
        Ok(Self { path })
    }

    fn path(&self) -> &Path {
        &self.path
    }
}

impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn writes_temp_file() {
        let dir = TempDir::new("demo-test").unwrap();
        let file = dir.path().join("out.txt");
        fs::write(&file, b"hello").unwrap();
        assert_eq!(fs::read_to_string(&file).unwrap(), "hello");
        // dir Drop 时清掉整个目录
    }
}
```

更短的“只借系统临时目录拼唯一文件”写法：

```rust
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() -> std::io::Result<()> {
    let nanos = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    let path = std::env::temp_dir().join(format!("demo-{nanos}.txt"));
    fs::write(&path, b"hi")?;
    assert_eq!(fs::read_to_string(&path)?, "hi");
    fs::remove_file(&path)?; // 记得清理；panic 路径上不如 TempDir 稳
    Ok(())
}
```

注意点：

- 路径要**唯一**（时间戳、进程 id、随机串），否则并行测试抢同一路径会 flaky（见 [Q4](#q4)、[Q18](#q18)）。
- panic 时只要 `TempDir` 还在栈上，`Drop` 仍会跑；手动 `temp_dir()` 拼路径却忘了清理，容易在 CI 机器上堆垃圾。
- 只测纯逻辑时尽量别碰真实磁盘；非碰不可再上临时目录。

第三方 crate（text，避免本仓强绑版本）：

```text
# Cargo.toml
# [dev-dependencies]
# tempfile = "3"
#
# let dir = tempfile::tempdir()?;
# let path = dir.path().join("x.txt");
# std::fs::write(&path, b"hi")?;
# // TempDir Drop 时自动清理
```

**Go 对比：**

```go
package demo_test

import (
	"os"
	"path/filepath"
	"testing"
)

func TestTemp(t *testing.T) {
	dir := t.TempDir() // 测完自动清理
	_ = os.WriteFile(filepath.Join(dir, "out.txt"), []byte("hello"), 0o644)
}
```

- **Go 怎么做**：`t.TempDir()` / `os.CreateTemp` 很省事。
- **Rust 为什么不同**：标准测试框架不内置等价 API，常见是自制 RAII 或 `tempfile`。
- **Go 程序员易踩的坑**：固定写死 `/tmp/mytest` 或仓库内相对路径，并行一开就互相踩。

**记忆点：**

- std：`temp_dir` + 唯一名 + `Drop`/显式清理。
- 省事：`tempfile` 作 dev-dependency。
- 并行下路径必须隔离。

---

## Q20. 怎么 mock 依赖？（trait + 测试替身；mockall 用 text 一笔） {#q20}
**Tags:** `common` `mock` `trait` `test-double`
**适用版本:** Rust 1.0+（手写替身）；`mockall` 为可选第三方

**一句话答案：**
把依赖收成 **trait**，生产代码依赖 `impl Trait` / 泛型；测试里给一个假实现（**test double** / 测试替身）。需要录制调用次数、按参数返回时，再用 **`mockall`** 一类库生成 mock——多数项目手写假类型就够。

**解答：**
手写替身（推荐默认路径）：

```rust
trait Clock {
    fn now_secs(&self) -> u64;
}

struct Greeter<C: Clock> {
    clock: C,
}

impl<C: Clock> Greeter<C> {
    fn greet(&self, name: &str) -> String {
        format!("hello {name} @{}", self.clock.now_secs())
    }
}

struct FixedClock(u64);
impl Clock for FixedClock {
    fn now_secs(&self) -> u64 {
        self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets_with_fixed_time() {
        let g = Greeter {
            clock: FixedClock(42),
        };
        assert_eq!(g.greet("a"), "hello a @42");
    }
}
```

只在测试里需要假类型时，可把假实现放进 `#[cfg(test)]` 模块，避免污染正式 API。动态派发也行：`Box<dyn Clock>`，测起来同样塞假对象。

需要「断言被调用了几次 / 按参数返回」时再用生成库（text 一笔，不绑死版本）：

```text
# Cargo.toml
# [dev-dependencies]
# mockall = "0.13"
#
# #[cfg_attr(test, mockall::automock)]
# trait Clock {
#     fn now_secs(&self) -> u64;
# }
#
# let mut clock = MockClock::new();
# clock.expect_now_secs().return_const(42u64);
```

别 mock 一切：纯函数、本地可造的数据（见 [Q10](#q10) 表驱动）优先真输入；I/O、时间、远端服务才值得替身。异步依赖同理——trait 方法返回 `Future` / 用 async trait，测试里给立即完成的假实现（异步测试见 [Q12](#q12)）。

**Go 对比：**
```go
type Clock interface{ NowSecs() int64 }
// 测试里塞 fake；或用 gomock 生成
```
- **Go 怎么做**：interface + fake / gomock。
- **Rust 为什么不同**：同样靠 trait 边界；无全局 monkey-patch 常规路径。
- **Go 程序员易踩的坑**：找「给任意函数打桩」的框架——Rust 更偏向设计可替换的 trait。

**记忆点：**
- 先 trait + 手写假实现。
- 编排复杂再 `mockall`；能表驱动就别 mock。

---

## Q21. `proptest` 属性测试最小怎么写？（对标 quickcheck） {#q21}
**Tags:** `hot` `proptest` `property-based` `quickcheck`
**适用版本:** proptest 1.x（以 crates.io 为准）

**一句话答案：**
用 **proptest** 随机生成输入，断言「对任意合法输入都成立」的不变量——比手写几组表驱动更能挖边界。对标 Go 生态的 quickcheck 一类，不是替代单元测试，而是补强。

**解答：**
```toml
[dev-dependencies]
proptest = "1"
```

```text
use proptest::prelude::*;

proptest! {
    fn reverse_twice_is_id(xs: Vec<i32>) {
        let mut ys = xs.clone();
        ys.reverse();
        ys.reverse();
        prop_assert_eq!(xs, ys);
    }
}
```

```rust
fn main() {
    // 适合：解析往返、编解码、集合不变量
    // 不适合：强依赖外部时钟/网络且无替身的逻辑
    println!("property tests find the case you forgot to table");
}
```

失败时 proptest 会尝试「缩小」输入到更小反例，便于修。和 [Q10](#q10) 表驱动搭配：表驱动锁已知案例，proptest 扫未知空间。

**Go 对比：**
- Go 标准库无内建属性测试；社区有 quickcheck 移植。
- **Rust 为什么不同**：`proptest!` 宏是社区事实标准之一。
- **Go 程序员易踩的坑**：用属性测试测「实现细节顺序」——应测不变量。

**记忆点：**
- 不变量 + 随机输入 → proptest。
- 与表驱动互补，不互斥。

---

## Q22. 集成测试怎么 mock HTTP 上游？（wiremock / 假服务） {#q22}
**Tags:** `hot` `wiremock` `httptest` `HTTP` `mock`
**适用版本:** wiremock 等；以文档为准

**一句话答案：**
测「调用下游 HTTP」时，在测试里起一个 **假 HTTP 服务**（常见 **wiremock**），把客户端 base URL 指过去；不要打真实外网。对标 Go 里自建 `httptest` 服务器或 mock。

**解答：**
```toml
[dev-dependencies]
wiremock = "0.6"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

```text
// 示意
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path};

#[tokio::test]
async fn fetches_ok() {
    let server = MockServer::start().await;
    Mock::given(method("GET")).and(path("/v1/x"))
        .respond_with(ResponseTemplate::new(200).set_body_string("ok"))
        .mount(&server).await;
    // let client = MyClient::new(server.uri());
    // assert_eq!(client.get_x().await.unwrap(), "ok");
}
```

```rust
fn main() {
    // 进程内 oneshot 测自己的 axum：见 52-http Q10
    // mock 别人的 HTTP：本问答的 wiremock 路径
    println!("fake upstream ≠ in-process Router oneshot");
}
```

测**自己的** axum handler 用 Tower `oneshot`（见 [52-http Q10](../52-http-advanced-and-realtime/#q10)）；测**依赖的上游**用 wiremock。

**Go 对比：**
```go
srv := httptest.NewServer(http.HandlerFunc(...))
defer srv.Close()
```
- **Go 怎么做**：`httptest.NewServer` 很常见。
- **Rust 为什么不同**：crate 名不同，模式相同。
- **Go 程序员易踩的坑**：集成测试直连生产 URL。

**记忆点：**
- 上游假服务 → wiremock。
- 本服务 handler → `oneshot`（52）。

---

## Q23. CLI 二进制怎么做黑盒测试？（`assert_cmd` / 快照） {#q23}
**Tags:** `common` `assert_cmd` `CLI` `insta` `snapshot`
**适用版本:** assert_cmd；可选 insta

**一句话答案：**
用 **`assert_cmd`** 找到并运行 `CARGO_BIN_EXE_<name>`，断言退出码与 stdout/stderr。输出易变时再用 **insta** 快照。对标「把编好的 CLI 当黑盒跑」。

**解答：**
```toml
[dev-dependencies]
assert_cmd = "2"
predicates = "3"
# insta = "1"   # 需要快照时再加
```

```text
use assert_cmd::Command;

#[test]
fn prints_help() {
    Command::cargo_bin("mycli").unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicates::str::contains("Usage"));
}
```

```rust
fn main() {
    // 单元测试测纯函数；assert_cmd 测「用户真敲的那条命令」
    println!("black-box CLI ≈ go test + exec.Command");
}
```

帮助文本、子命令路由、非法参数退出码（见 [38-cli](../38-cli-with-clap/)）特别适合这条路径。

**Go 对比：**
```go
cmd := exec.Command(bin, "--help")
out, err := cmd.CombinedOutput()
```
- 心智相同。
- **Go 程序员易踩的坑**：只测库函数、从不跑真正二进制。

**记忆点：**
- `Command::cargo_bin` + 断言退出码/输出。
- 大段输出 → insta 快照。
