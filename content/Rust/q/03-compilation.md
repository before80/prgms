+++
title = "03-编译"
date = 2026-07-28T14:49:00+08:00
weight = 30
type = "docs"
description = "讲清 Cargo 编译流程、profile、feature、target 与常见编译诊断。"
isCJKLanguage = true
draft = false

+++

# 编译 (Compilation)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会分不清 `cargo check`、`cargo build`、`cargo build --release`？
- 你是否想知道：Rust 的 debug / release 为什么不只是“快慢不同”，连行为都可能不同？
- 你会不会想给编译器传额外参数，却不知道该改 `RUSTFLAGS`、profile 还是 target 配置？
- 你是否不清楚 feature、target、profile、incremental cache 各自影响哪一层？
- 你会不会看到 `E0308`、`E0382`、链接错误、找不到链接器，却不知道该先查哪里？
- Windows 上用 `*-gnu` / `*-msvc` 编译时，命令、链接器配置和产物目录有何不同？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| profile | — | 构建配置 | 决定优化级别、调试信息等 | build flags 近亲 |
| debug build | — | 调试构建 | 默认开发构建，编得快、便于调试 | 默认 `go build` 近亲 |
| release build | — | 发布构建 | 优化更多、运行更快 | `-ldflags` / 发布优化近亲 |
| `RUSTFLAGS` | — | 编译器参数环境变量 | 给 rustc 追加底层参数 | `GOFLAGS` 近亲 |
| `LTO` | Link-Time Optimization | 链接时优化 | 链接阶段跨 crate 优化 | 链接期优化 |
| incremental | — | 增量编译 | 复用中间产物，加快二次编译 | build cache 近亲 |
| feature | — | Cargo 特性 | 编译期开关，控制代码和依赖 | build tags / 可选依赖近亲 |
| target triple | — | 目标三元组 | 目标平台标识，如 `x86_64-pc-windows-msvc` | `GOOS` + `GOARCH` 近亲 |
| linker | — | 链接器 | 把目标文件和库连成最终程序 | 外部链接器 |
| `CGU` | codegen unit | 代码生成单元 | 编译器切分代码生成工作的粒度 | 无直接对应 |
| `MSVC` | Microsoft Visual C++ | 微软 C/C++ 工具链 | Windows 默认链接生态 | 无直接对应 |
| `GNU` / MinGW-w64 | — | GNU 工具链 | Windows 上另一套链接生态 | 无直接对应 |
| `ABI` | Application Binary Interface | 应用二进制接口 | 二进制兼容约定；msvc/gnu 不通用 | 类似 CGO 与外部 C 约定 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5), [Q8](#q8), [Q15](#q15) |
| `common` | [Q4](#q4), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q16](#q16), [Q17](#q17) |
| `occasional` | [Q13](#q13), [Q18](#q18) |
| `advanced` | [Q14](#q14) |

---

## Q1. `cargo build` 和 `cargo build --release` 只是快慢不同吗？ {#q1}
**Tags:** `hot` `beginner` `profile`
**适用版本:** Rust 1.0+

**一句话答案：**
不只是快慢不同；它们连优化级别、调试信息、整数溢出行为、`debug_assert!` 是否生效都可能不同。

**详细解答：**
默认 `cargo build` 走 **debug** profile（产物在 `target/debug/`）；`cargo build --release` 走 **release** profile（产物在 `target/release/`）。除了 `opt-level` 和调试信息，整数溢出检查与 `debug_assert!` 的默认行为也不一样。

用**同一段程序**分别跑两次就能看出来。把下面代码放进 `src/main.rs`：

```rust
fn bump(x: u8) -> u8 {
    x + 1
}

fn main() {
    let x: u8 = "255".parse().unwrap();
    debug_assert!(x == 255, "debug_assert 只在 debug 生效");
    println!("{}", bump(x));
}
```

然后在项目根执行：

```bash
# 第一次：debug（默认）
cargo run
```

典型失败输出（debug 下 `255u8 + 1` 会溢出检查并 panic）：

```text
thread 'main' panicked at src/main.rs:2:5:
attempt to add with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

再跑 release：

```bash
# 第二次：同一程序，release
cargo run --release
```

release 默认**不做**溢出 panic，而是环绕成 `0`，并跳过 `debug_assert!`，因此通常会打印：

```text
0
```

PowerShell 等价：

```powershell
cargo run
cargo run --release
```

若希望 release 也检查溢出，在 `Cargo.toml` 里显式打开：

```toml
[profile.release]
overflow-checks = true
```

| | Debug（默认） | Release |
|--|---------------|---------|
| 命令 | `cargo build` / `cargo run` | `cargo build --release` / `cargo run --release` |
| 输出目录 | `target/debug/` | `target/release/` |
| 优化 | 少（`opt-level = 0`） | 多（`opt-level = 3`） |
| 整数溢出 | 默认检查 → panic | 默认环绕（wrapping） |
| `debug_assert!` | 生效 | 默认不执行 |

**🐹 Go 对比：**

- **Go 怎么做**：大多数情况下，`go build` 的“开发/发布”二分没有 Rust 这么强。
- **Rust 为什么不同**：Rust 把更多优化和检查行为放进 profile。
- **Go 程序员易踩的坑**：用 debug 构建测性能，或者只在 debug 下验证发布行为。

**小结 / 记忆点：**
- 同一程序，debug 可能 panic，release 可能静默环绕——发布前必须 `--release` 再验一遍。

---

## Q2. `cargo check` 和 `cargo build` 应该怎么选？ {#q2}
**Tags:** `hot` `beginner` `check`
**适用版本:** Rust 1.0+

**一句话答案：**
写代码时优先 `cargo check`，因为它更快；需要真实产物或验证链接阶段问题时，再用 `cargo build`。

**详细解答：**
两者检查的“深度”不同：

- **`cargo check`**：类型检查与借用检查，**不生成**完整可执行文件（或只做极少代码生成），反馈更快。
- **`cargo build`**：完整编译 + 链接，得到 `target/debug/`（或 `--release` 时的 `target/release/`）里的产物。

日常编辑循环：

```bash
# 边改边验证：快
cargo check
cargo check --all-targets

# 需要跑程序、测链接、看产物：完整构建
cargo build
cargo build --release
```

PowerShell 同理：

```powershell
cargo check
cargo build
```

| | `cargo check` | `cargo build` | `cargo clippy` |
|--|---------------|---------------|----------------|
| 类型 / 借用错误 | ✅ | ✅ | ✅ |
| 链接错误（缺系统库、找不到链接器） | ❌ | ✅ | ❌ |
| 产出可执行文件 | ❌ | ✅ | ❌ |
| 额外 lint | ❌ | ❌ | ✅ |

「❌ 错误场景」——链接器缺失时，只跑 `check` 会误以为一切正常：

```bash
# 假设本机缺 link.exe / 系统库（Windows 未装 VS Build Tools 等）
cargo check
# 可能：Finished `dev` profile ...  ← 类型检查过了

cargo build
# error: linker `link.exe` not found
# note: the msvc targets depend on the msvc linker...
```

这是**链接阶段**失败；`check` 抓不到，只有 `build`（或 `run`）才会暴露。

常见节奏：编辑循环用 `check`（或 rust-analyzer），提交前 `clippy` + `test`，部署前 `build --release`。

**🐹 Go 对比：**

- **Go 怎么做**：很多团队靠 `go build` / `go test` 驱动迭代。
- **Rust 为什么不同**：Rust 编译更重，所以“先快速检查、再完整构建”很常见。
- **Go 程序员易踩的坑**：每次都 `cargo build --release`，把开发循环拖得很慢。

**小结 / 记忆点：**
- 编辑循环：`cargo check`
- 要产物 / 查链接：`cargo build`

---

## Q3. `RUSTFLAGS` 是干什么的？ {#q3}
**Tags:** `hot` `beginner` `RUSTFLAGS`
**适用版本:** Rust 1.0+

**一句话答案：**
`RUSTFLAGS` 是给 rustc 追加底层参数的环境变量，适合临时试验编译选项；长期项目配置更常放进 `.cargo/config.toml` 或 profile。

**详细解答：**
临时试参数时常用 `RUSTFLAGS`。PowerShell：

```powershell
$env:RUSTFLAGS = "-C target-cpu=native"
cargo build --release
Remove-Item Env:RUSTFLAGS
```

bash：

```bash
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

长期稳定配置更适合写进项目配置，而不是全局环境变量。例如 `.cargo/config.toml`：

```toml
[build]
rustflags = ["-C", "link-arg=-s"]
```

或在 `Cargo.toml` 的 profile 里调优化，而不是把 `RUSTFLAGS` 永久挂在 shell 配置里。

**🐹 Go 对比：**

- **Go 怎么做**：可用 `GOFLAGS` 统一加一些参数。
- **Rust 为什么不同**：Rust 允许你更直接地把参数透传到底层编译器。
- **Go 程序员易踩的坑**：把全局 `RUSTFLAGS` 长期挂着，结果污染所有项目缓存和构建结果。

**小结 / 记忆点：**
- 临时试验：`RUSTFLAGS`
- 长期项目习惯：项目配置

---

## Q4. 增量编译（incremental）是什么？ {#q4}
**Tags:** `common` `incremental`
**适用版本:** Rust 1.0+

**一句话答案：**
增量编译会缓存中间结果，让你改一小处时不必从头编到尾；它主要有利于开发态，不一定适合追求极致发布优化的构建。

**详细解答：**
incremental 主要目标是减少重复编译成本。开发期默认 debug profile 通常开着增量；发布档常会关掉，换取更干净的优化结果。

在 `Cargo.toml` 里可显式控制：

```toml
[profile.dev]
incremental = true

[profile.release]
incremental = false
```

临时关掉增量排查“像是没编进去”：

```bash
CARGO_INCREMENTAL=0 cargo build
cargo clean
```

PowerShell：

```powershell
$env:CARGO_INCREMENTAL = "0"
cargo build
Remove-Item Env:CARGO_INCREMENTAL
cargo clean
```

**🐹 Go 对比：**

- **Go 怎么做**：工具链内部也会利用缓存。
- **Rust 为什么不同**：Rust 项目里你更常直接接触 incremental 开关和缓存行为。
- **Go 程序员易踩的坑**：遇到“像是没重新编进去”时，不知道先清 `target/` 或关掉增量排查。

**小结 / 记忆点：**
- 增量编译服务开发速度，不是永远越开越好。

---

## Q5. `LTO` 和 `codegen-units` 为什么会影响体积和速度？ {#q5}
**Tags:** `hot` `optimization` `LTO`
**适用版本:** Rust 1.0+

**一句话答案：**
`LTO` 让链接阶段做跨 crate 优化；`codegen-units`（代码生成单元，CGU）越少，优化空间通常越大，但编译也越慢。

**详细解答：**
更强优化通常意味着更长编译时间。release 里常会调 `lto` / `codegen-units` / `opt-level`，写在 `Cargo.toml`：

```toml
[profile.release]
lto = "thin"
codegen-units = 1
opt-level = 3
```

`thin` LTO 常是体积与编译时间之间较稳的折中；`codegen-units = 1` 往往更利于优化，但会让并行编译变少、编得更慢。

| 选项 | 效果 |
|------|------|
| `lto = "thin"` | 较好优化，编译时间可接受 |
| `lto = "fat"` / `true` | 往往更强优化，编译最慢 |
| `codegen-units = 1` | 单 CGU，利于优化 |
| 默认多 CGU | 并行编译快，优化略弱 |

**🐹 Go 对比：**

- **Go 怎么做**：多数优化策略由工具链默认决定。
- **Rust 为什么不同**：Rust 给了你更多显式调优空间。
- **Go 程序员易踩的坑**：一上来把所有优化开满，却没意识到编译时间会明显上涨。

**小结 / 记忆点：**
- `thin` LTO 常是不错的折中。

---

## Q6. `--target` 交叉编译时，为什么经常不是“装了 target 就结束”？ {#q6}
**Tags:** `common` `target`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 target 只解决“这个平台的 Rust 标准库是否可用”；真正连成可执行文件时，还常要目标平台自己的链接器、sysroot 或 SDK。

**详细解答：**
`rustup target add` 解决的是 Rust 标准库层；链接器和系统库仍可能是下一关。

```bash
rustup target add aarch64-unknown-linux-gnu
cargo build --target aarch64-unknown-linux-gnu
```

若缺链接器，还要在 `.cargo/config.toml` 里配，例如：

```toml
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

「❌ 错误场景」——只装了 target，没有交叉链接器：

```bash
rustup target add aarch64-unknown-linux-gnu
cargo build --target aarch64-unknown-linux-gnu
# error: linker `cc` not found
# 或：error: linking with `cc` failed: exit status: 1
```

「✅ 正确修法」：安装对应交叉工具链，并在 `.cargo/config.toml` 指定 `linker`（如上），或使用 `cross` / `cargo-zigbuild`。

**🐹 Go 对比：**

- **Go 怎么做**：纯 Go 工程常只切 `GOOS` / `GOARCH`。
- **Rust 为什么不同**：Rust 更频繁连接目标平台原生环境。
- **Go 程序员易踩的坑**：看到 `rustup target add` 就以为交叉编译全搞定了。

**小结 / 记忆点：**
- target 是第一步，不是全部。

---

## Q7. `cfg` 条件编译是在哪一层生效的？ {#q7}
**Tags:** `common` `cfg`
**适用版本:** Rust 1.0+

**一句话答案：**
`cfg` 是编译期条件选择；它决定哪些代码会进入本次编译，而不是运行时再 `if` 一次。

**详细解答：**
```rust
#[cfg(target_os = "windows")]
fn sep() -> char {
    '\\'
}

#[cfg(not(target_os = "windows"))]
fn sep() -> char {
    '/'
}

fn main() {
    println!("{}", sep());
}
```

也可用命令行 / 环境变量注入自定义 cfg：

```bash
RUSTFLAGS='--cfg my_flag' cargo build
```

PowerShell：

```powershell
$env:RUSTFLAGS = "--cfg my_flag"
cargo build
Remove-Item Env:RUSTFLAGS
```

cfg 是编译期裁剪，不是运行期分支。

**🐹 Go 对比：**

- **Go 怎么做**：更多通过 build tags 或按平台拆文件。
- **Rust 为什么不同**：Rust 常直接在项上写 `#[cfg(...)]`。
- **Go 程序员易踩的坑**：把 `cfg` 当成运行时条件；它其实会把整段代码直接裁掉。

**小结 / 记忆点：**
- `cfg` 是“编译期 if”。

---

## Q8. Cargo feature 到底是什么，为什么总被说要“保持加性”？ {#q8}
**Tags:** `hot` `feature`
**适用版本:** Cargo features

**一句话答案：**
feature 是编译期开关；“保持加性”指启用更多 feature 应该只增加能力，不该互相打架或改变基础语义。

**详细解答：**
在 `Cargo.toml` 里声明：

```toml
[features]
default = []
extra = []
```

代码用 `#[cfg(feature = "...")]` 配合：

```rust
#[cfg(feature = "extra")]
fn extra() {
    println!("extra enabled");
}

fn main() {
    #[cfg(feature = "extra")]
    extra();
}
```

启用方式：

```bash
cargo build --features extra
cargo build --no-default-features
cargo build --all-features
```

feature 最适合表达可选能力，而不是互斥人格分裂。

**🐹 Go 对比：**

- **Go 怎么做**：可选能力更多靠文件拆分和 build tags。
- **Rust 为什么不同**：Cargo feature 是依赖图和代码条件编译的统一入口。
- **Go 程序员易踩的坑**：把 feature 用成“互斥配置地狱”，让下游无法稳定组合。

**小结 / 记忆点：**
- feature 最好是“越开越多”，不是“二选一大战”。

---

## Q9. 自定义 profile 值得用吗？ {#q9}
**Tags:** `common` `profile`
**适用版本:** 自定义 profile 已稳定可用

**一句话答案：**
值得，特别是你需要“比 debug 更快、但又不想像 full release 那么慢”的中间档时。

**详细解答：**
自定义 profile 适合做团队构建折中。在 `Cargo.toml`：

```toml
[profile.release-lto]
inherits = "release"
lto = "thin"
codegen-units = 1
```

使用：

```bash
cargo build --profile release-lto
```

产物目录对应为 `target/release-lto/`。

**🐹 Go 对比：**

- **Go 怎么做**：大多数团队少有“自定义构建 profile”这一层。
- **Rust 为什么不同**：profile 是 Cargo 的一等概念。
- **Go 程序员易踩的坑**：以为只有 debug / release 两档，忽略自定义 profile 的折中价值。

**小结 / 记忆点：**
- 有稳定需求时，profile 可以项目化沉淀。

---

## Q10. 编译太慢，第一反应该看什么？ {#q10}
**Tags:** `common` `performance`
**适用版本:** Rust 1.0+

**一句话答案：**
先看自己是不是在开发态误用了 `--release`、全局 `RUSTFLAGS`、重依赖、大 workspace 全量编译或慢链接器。

**详细解答：**
先排最常见的人为放大器：

1. 开发循环误用了 `cargo build --release`
2. shell 里长期挂着全局 `RUSTFLAGS`
3. 一次编整个大 workspace，而不是 `-p <pkg>`
4. 依赖树过重（先看 `cargo tree`）
5. Windows 上链接慢，可试更快链接器或缩小编译范围

PowerShell 快速自检：

```powershell
# 开发期：只检查当前包
cargo check -p my_crate
# 看依赖树是否过重
cargo tree -p my_crate --depth 1
# 看 PATH / 环境是否被 RUSTFLAGS 污染
Get-ChildItem Env:RUSTFLAGS -ErrorAction SilentlyContinue
```

bash：

```bash
cargo check -p my_crate
cargo tree -p my_crate --depth 1
echo "$RUSTFLAGS"
```

**🐹 Go 对比：**

- **Go 怎么做**：先看缓存和依赖。
- **Rust 为什么不同**：Rust 的类型系统和泛型展开让“重依赖 + 高优化”成本更显著。
- **Go 程序员易踩的坑**：拿 release 全量构建当开发循环默认。

**小结 / 记忆点：**
- 先缩小构建范围，再谈高级优化。

---

## Q11. 最常见的编译错误，应该怎么读？ {#q11}
**Tags:** `common` `errors`
**适用版本:** Rust 1.0+

**一句话答案：**
先读错误码和第一句结论，再看 `help:` / `note:`；Rust 编译器常常已经把修复方向写在下面了。

**详细解答：**
常见错误与处理方向：

| 错误 | 含义 | 处理 |
|------|------|------|
| `cannot find crate` | 未声明依赖或改名 | 查 `Cargo.toml`，`cargo add` |
| E0308 mismatched types | 类型不一致 | 按期望类型改或转换 |
| E0382 use of moved value | 所有权移走 | clone、引用、或重构 |
| E0499 / E0502 借用 | 可变/不可变借用冲突 | 缩小借用范围 |
| `undefined reference` / link error | 链接 C 库失败 | 装系统库、配 `build.rs` |
| `linker not found` | 无链接器 | Windows 装 MSVC；Linux 装 `build-essential` |

读完整输出时：

```bash
cargo build 2>&1 | less
```

「❌ 错误写法」——类型不匹配（**会真实编译失败**）：

```rust
fn main() {
    let s: i32 = "hi";
    // error[E0308]: mismatched types
    // expected `i32`, found `&str`
    println!("{s}");
}
```

真实 stderr 片段：

```text
error[E0308]: mismatched types
 --> src/main.rs:2:18
  |
2 |     let s: i32 = "hi";
  |            ---   ^^^^ expected `i32`, found `&str`
  |            |
  |            expected due to this
```

「❌ 错误写法」——值已 move 再使用（**会真实编译失败**）：

```rust
fn main() {
    let s = String::from("x");
    let t = s;
    println!("{t}");
    println!("{s}");
    // error[E0382]: borrow of moved value: `s`
}
```

真实 stderr 片段（含 `help:`）：

```text
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:5:16
  |
2 |     let s = String::from("x");
  |         - move occurs because `s` has type `String`...
3 |     let t = s;
  |             - value moved here
5 |     println!("{s}");
  |                ^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let t = s.clone();
  |              ++++++++
```

「✅ 正确修法」示例：按 `help:` 显式转换或 clone。

**🐹 Go 对比：**

- **Go 怎么做**：编译器报错也值得完整读。
- **Rust 为什么不同**：Rust 错误信息通常更长，但也更有“教学性”。
- **Go 程序员易踩的坑**：只盯错误码，不看 `help:` 给的修法。

**小结 / 记忆点：**
- 先结论，后 help，再回源码。

---

## Q12. 只编译 workspace 里的一个包，怎么做？ {#q12}
**Tags:** `common` `workspace`
**适用版本:** Cargo workspace

**一句话答案：**
在 workspace 根目录下，用 `-p <package>` 指定包名；别默认每次都编整个 workspace。

**详细解答：**
大 workspace 下，只编一个包能明显缩短反馈时间：

```bash
cargo check -p my_crate
cargo build -p my_crate
cargo test -p my_crate
cargo build --workspace --exclude slow_crate
```

PowerShell 同理：

```powershell
cargo build -p my_crate --release
```

**🐹 Go 对比：**

- **Go 怎么做**：构建时也可只针对某个包或目录。
- **Rust 为什么不同**：workspace 常更大、更重，精准缩范围收益更明显。
- **Go 程序员易踩的坑**：每次都 `cargo build --workspace`，浪费大量时间。

**小结 / 记忆点：**
- 大 workspace 下，范围控制很重要。

---

## Q13. `cargo rustc` 什么时候值得用？ {#q13}
**Tags:** `occasional` `cargo-rustc`
**适用版本:** Cargo

**一句话答案：**
当你只想对“当前包”临时透传某些 rustc 参数时，`cargo rustc` 很方便；但它不是日常默认入口。

**详细解答：**
`cargo rustc` 适合一次性实验。`--` 后面的参数会传给 rustc：

```bash
cargo rustc --release -- -C target-cpu=native
cargo rustc --bin my_app -- -C opt-level=1
```

查看实际 rustc 命令行可用：

```bash
cargo build -v
cargo build -vv
```

（nightly 的 `-Z` 选项仅作临时试验，不要写进日常脚本。）

**🐹 Go 对比：**

- **Go 怎么做**：偶尔也会有临时底层参数透传需求。
- **Rust 为什么不同**：`cargo rustc` 明确区分了“项目入口”和“底层编译器试验入口”。
- **Go 程序员易踩的坑**：把它当成常规命令使用，导致命令行越来越难维护。

**小结 / 记忆点：**
- 临时试验用 `cargo rustc`，长期配置别滥用。

---

## Q14. `target-cpu=native` 为什么不能随便拿去发布？ {#q14}
**Tags:** `advanced` `cpu`
**适用版本:** Rust 1.0+

**一句话答案：**
因为它会针对“当前机器 CPU”开特定指令集；你本机更快，但放到更老的 CPU 上可能直接跑不了。

**详细解答：**
`native` 更像“为我这台机器定制”，不是“给所有用户的通用包”。本机 benchmark 可以临时开：

```powershell
$env:RUSTFLAGS = "-C target-cpu=native"
cargo build --release
Remove-Item Env:RUSTFLAGS
```

```bash
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

通用发布请不要默认写 `target-cpu=native`；应选明确、可移植的目标 CPU，或保持工具链默认：

```bash
RUSTFLAGS="-C target-cpu=x86-64-v2" cargo build --release
```

**🐹 Go 对比：**

- **Go 怎么做**：也会有 CPU 特性相关优化边界。
- **Rust 为什么不同**：这类优化选项常更直接暴露在用户面前。
- **Go 程序员易踩的坑**：本机 benchmark 很漂亮，就直接把同一产物发给所有机器。

**小结 / 记忆点：**
- 本机 benchmark 可以 `native`，通用发布要保守。

---

## Q15. Windows 上要用 `*-gnu` 编译，日常命令怎么写？ {#q15}
**Tags:** `hot` `windows` `gnu` `cargo`
**适用版本:** Rust 1.0+

**一句话答案：**
先保证 MinGW-w64 的 `gcc` 在 `PATH` 里；然后用 `rustup default ...-gnu`，或 `cargo +stable-x86_64-pc-windows-gnu build`，或 `cargo build --target x86_64-pc-windows-gnu`。

**解答：**

```powershell
# 前置：where.exe gcc 必须成功（见 01-installation Q15/Q17）

# 写法 A：默认工具链就是 gnu
rustup default stable-x86_64-pc-windows-gnu
cargo build
cargo build --release
cargo check

# 写法 B：不改 default，临时指定工具链
cargo +stable-x86_64-pc-windows-gnu build --release

# 写法 C：默认仍是 msvc，额外编 gnu target
rustup target add x86_64-pc-windows-gnu
cargo build --target x86_64-pc-windows-gnu
# 产物：target\x86_64-pc-windows-gnu\debug\<name>.exe
```

「❌ 错误场景」：

```powershell
cargo +stable-x86_64-pc-windows-gnu build
# error: linker `gcc` not found
```

「✅ 修法」：先装 MinGW 并配置 PATH，再编。完整安装步骤见 [01-installation Q15](01-installation.md#q15)。

**Go 对比：**
- **Go 怎么做**：`go build` 较少在 Windows 上再选一套 ABI。
- **Rust 为什么不同**：编译命令相同，差异在 toolchain / target。
- **Go 程序员易踩的坑**：只记 `cargo build`，却忘了当前 host 是不是 gnu。

**记忆点：**
- 命令仍是 cargo；先确认 `rustc -vV` 的 host / 你传的 `--target`。

---

## Q16. 如何在 `.cargo/config.toml` 里指定 `windows-gnu` 的链接器？ {#q16}
**Tags:** `common` `windows` `gnu` `linker`
**适用版本:** Cargo

**一句话答案：**
在项目（或用户级）`.cargo/config.toml` 的 `[target.x86_64-pc-windows-gnu]` 里设置 `linker`，指向 `gcc` 或它的绝对路径。

**解答：**
项目根创建 `.cargo/config.toml`：

```toml
[target.x86_64-pc-windows-gnu]
linker = "gcc"
# 若 PATH 不稳定，写绝对路径更稳：
# linker = "C:\\msys64\\mingw64\\bin\\gcc.exe"
```

然后：

```powershell
cargo build --target x86_64-pc-windows-gnu
# 或已 default 到 gnu 时直接：
cargo build
```

「❌ 错误场景」——linker 指错目录：

```toml
# 错误示例：指到了不存在的路径
linker = "C:\\wrong\\mingw64\\bin\\gcc.exe"
```

会在链接阶段失败。用 `where.exe gcc` / 资源管理器确认真实路径后再写。

**Go 对比：**
- **Go 怎么做**：较少为 Windows 单独写 linker 配置文件。
- **Rust 为什么不同**：外部链接器常通过 Cargo target 配置注入。
- **Go 程序员易踩的坑**：把 linker 配进 `Cargo.toml`（那里不是放这个的地方）。

**记忆点：**
- linker 写在 `.cargo/config.toml` 的 `[target.<triple>]`。

---

## Q17. 同一台机器上，`msvc` 与 `gnu` 的产物目录有何不同？能混用原生库吗？ {#q17}
**Tags:** `common` `windows` `abi`
**适用版本:** Rust 1.0+

**一句话答案：**
默认 host 编进 `target/debug` 或 `target/release`；显式 `--target` 时进 `target/<triple>/...`。两套 **ABI**（应用二进制接口）不同，预编译的 `.lib` / `.a` / 某些 FFI 绑定不能想当然混链。

**解答：**

| 构建方式 | 典型产物路径 |
|----------|----------------|
| default = msvc，`cargo build` | `target\debug\app.exe` |
| default = gnu，`cargo build` | `target\debug\app.exe`（同名目录，但是另一套工具链产物） |
| `cargo build --target x86_64-pc-windows-gnu` | `target\x86_64-pc-windows-gnu\debug\app.exe` |
| `cargo build --target x86_64-pc-windows-msvc` | `target\x86_64-pc-windows-msvc\debug\app.exe` |

因此：

1. 切换 default host 后，先 `cargo clean` 再编，避免“目录还在、ABI 已换”的错觉。
2. 为 MSVC 编的静态库，不要硬塞进 gnu 链接；反之亦然。
3. 必须双目标时，分两套构建脚本 / CI job。

详见 [01-installation Q22](01-installation.md#q22)。

**Go 对比：**
- **Go 怎么做**：同 `GOOS/GOARCH` 下通常一套约定。
- **Rust 为什么不同**：Windows 上 msvc/gnu 是两个一等公民目标。
- **Go 程序员易踩的坑**：看见都是 `target\debug\*.exe` 就以为可以混用依赖。

**记忆点：**
- 同目录名 ≠ 同 ABI；换工具链先 `cargo clean`。

---

## Q18. 源码里怎么按 `msvc` / `gnu` 做条件编译？ {#q18}
**Tags:** `occasional` `windows` `cfg`
**适用版本:** Rust 1.0+

**一句话答案：**
用 `#[cfg(target_env = "msvc")]` / `#[cfg(target_env = "gnu")]`（常再叠 `target_os = "windows"`）；这是编译期分支，不是运行时 if。

**解答：**

```rust
#[cfg(all(target_os = "windows", target_env = "msvc"))]
fn linker_family() -> &'static str {
    "msvc"
}

#[cfg(all(target_os = "windows", target_env = "gnu"))]
fn linker_family() -> &'static str {
    "gnu"
}

#[cfg(not(target_os = "windows"))]
fn linker_family() -> &'static str {
    "non-windows"
}

fn main() {
    println!("{}", linker_family());
}
```

只在确有 ABI / 系统调用差异时使用；日常业务逻辑尽量保持 target 无关。

**Go 对比：**
- **Go 怎么做**：`//go:build windows` 等 build tag。
- **Rust 为什么不同**：`cfg` 还能区分 `target_env`。
- **Go 程序员易踩的坑**：用运行时检测“我是不是 gnu 编的”，却忘了这是编译期就定死的。

**记忆点：**
- Windows 链接族差异用 `target_env`，不要滥用。

---
