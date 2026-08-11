+++
title = "04-运行"
date = 2026-07-28T14:49:00+08:00
weight = 40
type = "docs"
description = "讲清 cargo run、参数传递、环境变量、回溯与进程退出码等运行期问题。"
isCJKLanguage = true
draft = false

+++

# 运行 (Running)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会刚学 Rust 时不知道 `cargo run` 到底帮你做了什么？
- 你是否总忘记命令行参数前面的 `--`，结果参数被 Cargo 吃掉？
- 你会不会分不清程序参数、环境变量、工作目录、退出码分别在哪一层起作用？
- 你是否想知道：为什么 debug 跑得好好的，release 下行为却不一样？
- 你会不会看到 panic 提示你开 `RUST_BACKTRACE=1`，却不清楚它具体能帮你什么？
- Windows 上 `*-msvc` / `*-gnu` 编出的程序，运行时缺 DLL / 缺运行库该怎么查？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| `cargo run` | — | 运行命令 | 需要时先构建，再执行程序 | `go run` 近亲 |
| argument | — | 命令行参数 | 启动进程时附带的参数 | `os.Args` |
| environment variable | — | 环境变量 | 启动进程时继承的键值对 | `os.Getenv` |
| cwd | current working directory | 当前工作目录 | 进程启动时所在目录 | 同概念 |
| panic | — | 恐慌退出 | 程序在不可恢复错误时中止 | `panic` |
| backtrace | — | 栈回溯 | 出错时打印调用栈 | stack trace |
| `ExitCode` | — | 退出码类型 | 显式返回进程退出码 | `os.Exit(code)` 近亲 |
| `RUST_LOG` | — | 日志环境变量 | 常被日志库读取，用于过滤日志 | `LOG_LEVEL` 类环境变量 |
| `RUST_BACKTRACE` | — | 回溯环境变量 | 控制 panic 时是否打印栈回溯 | 调试开关近亲 |
| `MSVC` / VC++ Redistributable | — | 微软运行库 | `*-msvc` 动态链接时常需的运行时 | 无直接对应 |
| MinGW runtime | — | MinGW 运行库 | `*-gnu` 视链接方式可能依赖的 DLL | 无直接对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q5](#q5), [Q8](#q8), [Q15](#q15) |
| `common` | [Q4](#q4), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q16](#q16), [Q18](#q18) |
| `occasional` | [Q13](#q13), [Q17](#q17) |
| `advanced` | [Q14](#q14) |

---

## Q1. `cargo run` 到底帮我做了什么？ {#q1}
**Tags:** `hot` `beginner` `cargo`
**适用版本:** Rust 1.0+

**一句话答案：**
`cargo run` 会在需要时先构建项目，然后执行对应二进制；如果源码没变，它会尽量复用已有产物。

**详细解答：**
可以把它理解成“需要时先 `build`，再 execute”。默认跑 **debug** profile（`target/debug/`）；要跑优化版加 `--release`。

```bash
cargo run
cargo run --release
cargo run --bin server
cargo run --example hello
```

典型输出（Cargo 状态走 stderr，程序输出在其后）：

```text
   Compiling my-app v0.1.0 (E:\dev\my-app)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.85s
     Running `target\debug\my-app.exe`
Hello, world!
```

实用细节：

- `cargo run -q`：安静模式，少打 Compiling/Finished 行。
- 程序参数必须放在 `--` 之后（见 [Q2](#q2)）。
- 程序非 0 退出时，Cargo 会附加 `process didn't exit successfully`。
- 只想确认能编译、不想运行 → `cargo build` 或 `cargo check`。

**🐹 Go 对比：**

- **Go 怎么做**：`go run` 更偏“临时编译这个入口”。
- **Rust 为什么不同**：Rust 默认从 Cargo 项目结构出发，产物管理更明确。
- **Go 程序员易踩的坑**：把 `cargo run` 想成“只运行、不构建”；它其实仍建立在构建之上。

**小结 / 记忆点：**
- `cargo run` = 按需构建 + 执行产物。

---

## Q2. 程序参数为什么前面总要写一个 `--`？ {#q2}
**Tags:** `hot` `beginner` `args`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 `--` 用来分隔“Cargo 自己的参数”和“你的程序参数”；没有它，Cargo 会把后面的东西当成自己的选项。

**详细解答：**
程序里这样读参数：

```rust
fn main() {
    let args: Vec<String> = std::env::args().collect();
    println!("{args:?}");
}
```

正确传参（`--` 后面才是程序参数）：

```bash
cargo run -- --port 8080
cargo run --release -- -v --config=app.toml
```

PowerShell：

```powershell
cargo run -- --port 8080
```

「❌ 错误写法」——漏写 `--`，Cargo 把 `--port` 当成自己的未知选项：

```bash
cargo run --port 8080
```

典型失败输出：

```text
error: unexpected argument '--port' found

Usage: cargo.exe run [OPTIONS] [ARGS]...

For more information, try '--help'.
```

此时程序根本没启动，自然也收不到参数。

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println(os.Args)
}
```

- **Go 怎么做**：直接 `go run . --port 8080` 一类形式更常见。
- **Rust 为什么不同**：Cargo 本身也有很多命令行参数，所以需要明确分隔。
- **Go 程序员易踩的坑**：忘写 `--`，然后以为程序没收到参数。

**小结 / 记忆点：**
- Cargo 参数在前，程序参数在 `--` 后。

---

## Q3. 环境变量和命令行参数怎么分工？ {#q3}
**Tags:** `hot` `beginner` `env`
**适用版本:** Rust 1.0+

**一句话答案：**
命令行参数更适合“本次执行的显式输入”，环境变量更适合“外部配置或运行环境状态”。

**详细解答：**
```rust
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let url = std::env::var("MY_URL").unwrap_or_else(|_| "(unset)".into());
    println!("args={args:?}");
    println!("MY_URL={url}");
}
```

PowerShell：

```powershell
$env:MY_URL = "https://example.com"
cargo run -- --verbose
Remove-Item Env:MY_URL
```

bash：

```bash
MY_URL=https://example.com cargo run -- --verbose
```

参数更显式；环境变量更隐式。`.env` 文件不会被标准库自动加载，需要 `dotenvy` 等自行处理。

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println(os.Args)
	fmt.Println(os.Getenv("MY_URL"))
}
```

- **Go 怎么做**：同样会在 `os.Args` 和 `os.Getenv` 之间分工。
- **Rust 为什么不同**：语义几乎一致，只是 Cargo 层还多了一层参数分隔。
- **Go 程序员易踩的坑**：把环境变量当参数替代品，导致命令不可复现或不透明。

**小结 / 记忆点：**
- 显式输入优先参数；环境约定再考虑环境变量。

---

## Q4. 二进制名字是怎么来的？ {#q4}
**Tags:** `common` `bin`
**适用版本:** Cargo

**一句话答案：**
默认来自 `[package].name`；如果你写了 `[[bin]]`，则按 `name` 和 `path` 配置决定。

**详细解答：**
未写 `[[bin]]` 时，可执行文件名通常等于 `[package].name`。多入口或要改名时，在 `Cargo.toml` 显式声明：

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"

[[bin]]
name = "custom_name"
path = "src/main.rs"

[[bin]]
name = "admin"
path = "src/bin/admin.rs"
```

运行指定二进制：

```bash
cargo run --bin custom_name
cargo run --bin admin -- --help
```

直接跑产物：

```bash
# Linux / macOS
./target/debug/custom_name
./target/release/custom_name

# Windows PowerShell
.\target\debug\custom_name.exe
.\target\release\custom_name.exe
```

「❌ 错误场景」——项目里有多个 `[[bin]]`，却直接 `cargo run`：

```bash
cargo run
# error: `cargo run` could not determine which binary to run.
# Use the `--bin` option to specify a binary,
# or the `default-run` key in Cargo.toml.
```

「✅ 正确修法」：`cargo run --bin <name>`，或在 `Cargo.toml` 设 `default-run = "custom_name"`。

**🐹 Go 对比：**

- **Go 怎么做**：常直接通过输出参数或目录名控制二进制名。
- **Rust 为什么不同**：Cargo 把多目标管理也纳入项目元数据。
- **Go 程序员易踩的坑**：项目里有多个 bin 时还直接 `cargo run`，结果跑错或歧义。

**小结 / 记忆点：**
- 多二进制时，显式 `--bin` 更稳。

---

## Q5. `RUST_BACKTRACE=1` 到底有啥用？ {#q5}
**Tags:** `hot` `beginner` `backtrace`
**适用版本:** Rust 1.0+

**一句话答案：**
它会在 panic 时打印调用栈，让你知道程序是沿着哪条调用链炸掉的；调试“在哪崩的”时非常有用。

**详细解答：**
```rust
fn boom() {
    let v: Vec<i32> = vec![];
    let _ = v[0];
}

fn main() {
    boom();
}
```

不开 `RUST_BACKTRACE` 时，通常只有 panic 点和一句提示：

```text
thread 'main' panicked at src/main.rs:3:14:
index out of bounds: the len is 0 but the index is 0
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

开了之后会多出调用栈。PowerShell：

```powershell
$env:RUST_BACKTRACE = "1"
cargo run
Remove-Item Env:RUST_BACKTRACE
```

需要更完整栈时用 `RUST_BACKTRACE=full`：

```powershell
$env:RUST_BACKTRACE = "full"
cargo run
```

bash：

```bash
RUST_BACKTRACE=1 cargo run
RUST_BACKTRACE=full cargo run
```

开启后会看到类似 `boom` → `main` 的帧（路径/行号随平台与版本变化）。

**🐹 Go 对比：**

- **Go 怎么做**：panic 默认会打印栈信息。
- **Rust 为什么不同**：Rust 让你显式通过环境变量控制回溯详细程度。
- **Go 程序员易踩的坑**：看到提示后不去开 `RUST_BACKTRACE=1`，错过最值钱的上下文。

**小结 / 记忆点：**
- panic 排查第一反应：先开回溯。

---

## Q6. `RUST_LOG` 是标准库功能吗？ {#q6}
**Tags:** `common` `logging`
**适用版本:** 生态约定

**一句话答案：**
不是。`RUST_LOG` 只是一个普通环境变量；只有你的日志库或 subscriber 主动读取它时，它才有意义。

**详细解答：**
```rust
fn main() {
    let value = std::env::var("RUST_LOG").unwrap_or_else(|_| "(unset)".into());
    println!("RUST_LOG={value}");
}
```

没有日志框架读取它时，`RUST_LOG` 只是个普通字符串。常见用法是先接入 `env_logger` / `tracing-subscriber` 之类库，再设：

```powershell
$env:RUST_LOG = "info"
cargo run
Remove-Item Env:RUST_LOG
```

```bash
RUST_LOG=info cargo run
RUST_LOG=my_crate=debug,hyper=warn cargo run
```

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println(os.Getenv("LOG_LEVEL"))
}
```

- **Go 怎么做**：很多项目也约定 `LOG_LEVEL` 一类环境变量，但不属于语言标准库。
- **Rust 为什么不同**：Rust 社区把 `RUST_LOG` 约定得更统一，所以新手容易误以为它是内建功能。
- **Go 程序员易踩的坑**：只设环境变量，不初始化日志系统，就期待日志级别自动生效。

**小结 / 记忆点：**
- 先有日志库，再谈 `RUST_LOG`。

---

## Q7. examples 和 benches 怎么运行？ {#q7}
**Tags:** `common` `examples`
**适用版本:** Cargo

**一句话答案：**
`examples/*.rs` 用 `cargo run --example name`；基准测试通常用 `cargo bench` 或第三方基准框架。

**详细解答：**
Cargo 约定目录：

```text
my-app/
├── Cargo.toml
├── src/
│   └── main.rs
├── examples/
│   └── hello.rs          →  cargo run --example hello
└── benches/
    └── foo.rs            →  cargo bench --bench foo
```

`examples/hello.rs` 是独立可执行目标，不是 `src/main.rs` 的替身：

```rust
fn main() {
    println!("这是一个独立示例程序");
}
```

运行 example（也可再传程序参数）：

```bash
cargo run --example hello
cargo run --example hello -- --arg 1
```

PowerShell：

```powershell
cargo run --example hello -- --arg 1
```

基准目标常在 `Cargo.toml` 里声明（尤其是用 criterion 等第三方 harness 时）：

```toml
[[bench]]
name = "foo"
harness = false
```

`benches/foo.rs` 示例骨架（`harness = false` 时自己写测量逻辑；第三方框架另有模板）：

```rust
fn main() {
    // 仅示意：真实基准请用 criterion 等框架
    let start = std::time::Instant::now();
    let _ = (0..1_000_000).sum::<u64>();
    println!("elapsed = {:?}", start.elapsed());
}
```

运行：

```bash
cargo bench
cargo bench --bench foo
```

**🐹 Go 对比：**

- **Go 怎么做**：示例和 benchmark 更常通过测试文件组织。
- **Rust 为什么不同**：Cargo 把 `examples/` 和 `benches/` 作为显式目标目录。
- **Go 程序员易踩的坑**：把 example 当成主程序源码的一部分改，结果影响教学示例和主入口分工。

**小结 / 记忆点：**
- example：`cargo run --example <name>`；bench：`cargo bench [--bench <name>]`。

---

## Q8. 为什么 debug 跑得好好的，release 却不一样？ {#q8}
**Tags:** `hot` `beginner` `debug` `release`
**适用版本:** Rust 1.0+

**一句话答案：**
因为 debug / release 不只是优化级别不同；整数溢出检查、`debug_assert!` 和优化器行为都会影响最终结果。

**详细解答：**
用**同一程序**分别跑 debug 与 release。先看溢出：

```rust
fn main() {
    let x: u8 = "255".parse().unwrap();
    println!("{}", x + 1);
}
```

```bash
cargo run
# thread 'main' panicked at ...: attempt to add with overflow

cargo run --release
# 0
```

再看 `debug_assert!`（只在 debug 构建执行）：

```rust
fn main() {
    debug_assert!(false, "only checked in debug");
    println!("继续执行");
}
```

```bash
cargo run
# panic: only checked in debug

cargo run --release
# 继续执行
```

因此不要把**必须执行**的校验（如用户输入验证）写进 `debug_assert!`。若希望 release 也检查溢出：

```toml
[profile.release]
overflow-checks = true
```

**🐹 Go 对比：**

- **Go 怎么做**：通常没有这样强烈的默认构建语义分层。
- **Rust 为什么不同**：profile 是 Rust 工作流核心，语义差异更明显。
- **Go 程序员易踩的坑**：只在 debug 跑通就认定发布也没问题。

**小结 / 记忆点：**
- 发布行为要在发布档位验证。

---

## Q9. Windows 上运行时缺 DLL，先怀疑什么？ {#q9}
**Tags:** `common` `windows`
**适用版本:** Windows

**一句话答案：**
先怀疑动态依赖没跟着带上，或者目标工具链 / 运行库不匹配；问题通常不在 Rust 语法，而在运行环境。

**详细解答：**
缺 DLL 多半是部署和依赖问题，不是语法错误。先确认编的是 msvc 还是 gnu，再查依赖。

查看当前工具链：

```powershell
rustup show
rustc -vV
# 关注 host / 默认 target，例如 x86_64-pc-windows-msvc
```

```bash
rustup show
rustc -vV
```

用 Visual Studio 自带的 `dumpbin` 看 `.exe` 依赖哪些 DLL（需已装 VS Build Tools，并在“Developer PowerShell / x64 Native Tools”环境里）：

```powershell
# 先编出产物
cargo build --release

# 查看依赖的 DLL 列表
dumpbin /dependents .\target\release\my-app.exe
```

若没有 `dumpbin`，可确认是否在 VS 开发者环境：

```powershell
Get-Command dumpbin -ErrorAction SilentlyContinue
where.exe dumpbin
```

「❌ 错误场景」——目标机器缺运行库 / DLL：

```text
# 双击或命令行启动时常见提示：
# 由于找不到 VCRUNTIME140.dll，无法继续执行代码。
# 或：The code execution cannot proceed because xxx.dll was not found.
```

「✅ 正确修法」：

1. 把缺的 DLL 放到与 `.exe` 同目录，或加入 `PATH`。
2. 确认编的是 `*-msvc` 还是 `*-gnu`，勿混用运行时。
3. 若 crate 支持，改用静态链接相关 feature。
4. 纯 Rust + 默认 MSVC 动态 CRT 的程序，目标机通常需要对应 VC 运行库。
5. 更细的 msvc/gnu 运行差异见本篇 [Q15](#q15)、[Q16](#q16)；安装与许可见 [01-installation Q18](01-installation.md#q18)。

**🐹 Go 对比：**

- **Go 怎么做**：纯 Go 程序多数依赖更少。
- **Rust 为什么不同**：Rust 和系统库、C 生态结合更频繁。
- **Go 程序员易踩的坑**：一看到缺 DLL 就回去改 Rust 代码；其实应先查部署包和依赖链。

**小结 / 记忆点：**
- 先 `rustup show` / `dumpbin /dependents`，再谈改代码。

---

## Q10. 程序的工作目录到底是谁决定的？ {#q10}
**Tags:** `common` `cwd`
**适用版本:** Rust 1.0+

**一句话答案：**
是启动进程时的当前工作目录，不一定是 `src/`，也不一定总是 `Cargo.toml` 所在目录。

**详细解答：**
```rust
fn main() -> std::io::Result<()> {
    println!("{:?}", std::env::current_dir()?);
    Ok(())
}
```

`cargo run` **不会**帮你改 cwd：cwd 就是你敲命令时所在的目录。

```bash
# 在项目根
cargo run
# 打印：.../my-app

# 在别的目录指定清单再跑
cd /tmp
cargo run --manifest-path /path/to/my-app/Cargo.toml
# 打印：/tmp   ← 不是 my-app 目录
```

PowerShell：

```powershell
Set-Location $env:TEMP
cargo run --manifest-path E:\dev\my-app\Cargo.toml
```

相对路径永远相对 cwd。需要“包所在目录”时，开发期可用编译期常量 `env!("CARGO_MANIFEST_DIR")`；发布程序应把资源打进二进制或装到明确数据目录。

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	dir, _ := os.Getwd()
	fmt.Println(dir)
}
```

- **Go 怎么做**：工作目录概念完全一样。
- **Rust 为什么不同**：很多新手以为 `cargo run` 会“帮你切到项目根”，其实它通常不会改变 cwd 语义。
- **Go 程序员易踩的坑**：把“我总是在项目根启动”误当成语言保证。

**小结 / 记忆点：**
- 相对路径永远看 cwd。

---

## Q11. 不经过 Cargo，怎么直接运行已经编好的二进制？ {#q11}
**Tags:** `common` `binary`
**适用版本:** Rust 1.0+

**一句话答案：**
先 `cargo build` 或 `cargo build --release`，然后直接运行 `target/...` 里的可执行文件即可。

**详细解答：**
先构建：

```bash
cargo build
cargo build --release
```

再直接跑产物（把 `my-app` 换成你的 `[package].name` 或 `[[bin]].name`）：

```bash
# Linux / macOS
./target/debug/my-app
./target/debug/my-app --port 8080
./target/release/my-app arg1 arg2
```

Windows PowerShell：

```powershell
cargo build --release
.\target\debug\my-app.exe
.\target\release\my-app.exe --port 8080
```

直接运行时：

- 环境变量由当前 shell 决定（`$env:RUST_LOG = "info"` / `RUST_LOG=info`）。
- cwd 仍是你敲命令的目录。
- 参数前面**不需要**再写 Cargo 的 `--` 分隔符。

多 bin 时路径对应 `[[bin]].name`：

```powershell
.\target\release\custom_name.exe
.\target\release\admin.exe
```

**🐹 Go 对比：**

- **Go 怎么做**：`go build` 后直接运行产物。
- **Rust 为什么不同**：Cargo 把产物目录约定得更明显（`target/debug` vs `target/release`）。
- **Go 程序员易踩的坑**：习惯了 `cargo run`，忘了真正部署时运行的是编译产物，不是 Cargo。

**小结 / 记忆点：**
- 开发用 `cargo run`；部署常直接跑 `target/...` 二进制。

---

## Q12. `main` 可以返回 `Result` 吗？ {#q12}
**Tags:** `common` `main`
**适用版本:** `main -> Result` 已稳定

**一句话答案：**
可以，这在命令行工具里很常见；它能让你直接用 `?`，出错时返回非零退出并打印错误。

**详细解答：**
```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string("Cargo.toml")?;
    println!("{}", text.len());
    Ok(())
}
```

`Ok(())` → 退出码 0；`Err` → 非 0 并打印错误。脚本里可用退出码判断成败：

```bash
cargo run
echo $?
```

```powershell
cargo run
echo $LASTEXITCODE
```

**🐹 Go 对比：**

- **Go 怎么做**：错误通常在 `main` 里手动打印并 `os.Exit`。
- **Rust 为什么不同**：Rust 允许 `main -> Result`，CLI 程序写起来更利落。
- **Go 程序员易踩的坑**：延续 Go 习惯，所有错误都手写 `match`，错过 `?` 的可读性收益。

**小结 / 记忆点：**
- CLI 小工具里，`main -> Result` 很实用。

---

## Q13. 脚本或 CI 里批量跑 Rust 程序，要特别注意什么？ {#q13}
**Tags:** `occasional` `scripts`
**适用版本:** Rust 1.0+

**一句话答案：**
重点看退出码、环境变量和工作目录；别只看终端上“打印了点东西”，要确认进程最终是否成功退出。

**详细解答：**
bash：

```bash
#!/usr/bin/env bash
set -euo pipefail
export RUST_BACKTRACE=1
cargo test
cargo run --release -- --batch
```

PowerShell：

```powershell
$ErrorActionPreference = "Stop"
$env:RUST_LOG = "info"
cargo run --release -- --batch
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

也可用 `ExitCode` 显式表达成功：

```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    ExitCode::SUCCESS
}
```

脚本里最该信的是退出码，而不是零散输出。注意：`cargo run` 成功编译但程序返回非 0 时，要用进程退出码判断失败（PowerShell 尤甚）。

**🐹 Go 对比：**

- **Go 怎么做**：CI 里同样依赖进程退出码。
- **Rust 为什么不同**：很多新手还停留在 `cargo run` 视角，没切换到“真正的进程管理”思维。
- **Go 程序员易踩的坑**：把 Cargo 输出和程序输出混在一起看，忽略最后的退出状态。

**小结 / 记忆点：**
- 自动化环境里，退出码比日志更可靠。

---

## Q14. 怎么显式控制进程退出码？ {#q14}
**Tags:** `advanced` `ExitCode`
**适用版本:** `ExitCode` 稳定可用

**一句话答案：**
最直接的办法是让 `main` 返回 `std::process::ExitCode`；需要更细粒度时，再考虑 `std::process::exit`，但后者会跳过局部变量的 `Drop`。

**详细解答：**
```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    if std::env::args().len() < 2 {
        eprintln!("usage: app <arg>");
        return ExitCode::from(2);
    }
    ExitCode::SUCCESS
}
```

验证退出码：

```bash
cargo run
echo $?          # 无参数时应为 2

cargo run -- hello
echo $?          # 应为 0
```

```powershell
cargo run
echo $LASTEXITCODE

cargo run -- hello
echo $LASTEXITCODE
```

| 方式 | 说明 |
|------|------|
| `main() -> ()` | 成功 0；`panic` 非 0 |
| `main() -> Result<T, E>` | `Ok` → 0；`Err` → 非 0 |
| `ExitCode` | 精确控制码 |
| `std::process::exit(code)` | 立即退出，**跳过**局部 Drop（尽量少用） |

**🐹 Go 对比：**
```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("exit 2")
	os.Exit(2)
}
```

- **Go 怎么做**：常直接 `os.Exit(code)`。
- **Rust 为什么不同**：Rust 额外提供了更“表达式化”的 `ExitCode` 返回方式。
- **Go 程序员易踩的坑**：一上来就 `process::exit`，忽略了它会跳过一些自动清理。

**小结 / 记忆点：**
- 能返回 `ExitCode` 时，通常比直接 `process::exit` 更稳。

---

## Q15. `*-msvc` 编出来的程序，客户机缺什么会跑不起来？ {#q15}
**Tags:** `hot` `windows` `msvc`
**适用版本:** Windows

**一句话答案：**
最常见是缺少 **Microsoft Visual C++ Redistributable**（例如提示找不到 `VCRUNTIME140.dll` / `MSVCP140.dll`）；这是运行库问题，不是“Rust 没装上”。

**解答：**

```text
# 典型弹窗 / 控制台信息：
# 由于找不到 VCRUNTIME140.dll，无法继续执行代码。
```

排查顺序：

```powershell
rustc -vV
# host 应为 x86_64-pc-windows-msvc（或你指定的 msvc target）

cargo build --release
# 在开发者环境中：
dumpbin /dependents .\target\release\my-app.exe
```

「✅ 修法」：

1. 在目标机器安装对应架构（x64/x86/ARM64）的 VC++ Redistributable。
2. 或把再发行规则允许的运行库 DLL 随安装包分发。
3. 开发机有 VS、客户机没有时，尤其容易踩这个坑。

许可 / 商业侧注意点见 [01-installation Q18](01-installation.md#q18)（非法律意见）。

**Go 对比：**
- **Go 怎么做**：纯 Go 二进制对外部 CRT 依赖通常更少。
- **Rust 为什么不同**：`*-msvc` 常动态链接微软 CRT。
- **Go 程序员易踩的坑**：开发机双击能跑，就以为拷贝到裸机 Windows 也一定能跑。

**记忆点：**
- msvc 发布清单里要有“运行库怎么解决”这一项。

---

## Q16. `*-gnu` 编出来的程序，拷到没装 MinGW 的机器上能跑吗？ {#q16}
**Tags:** `common` `windows` `gnu`
**适用版本:** Windows

**一句话答案：**
不一定。取决于你是否静态链接了相关运行库；若动态依赖 `libgcc_s_seh-1.dll`、`libstdc++-6.dll` 等，目标机也得有这些 DLL（或你把它们一并带上）。

**解答：**

```powershell
rustup default stable-x86_64-pc-windows-gnu
cargo build --release

# 用能查看依赖的工具检查（有 dumpbin / Dependencies / ldd 类工具时）
# 关注是否依赖 MinGW 相关 DLL
```

实务建议：

1. 在**干净的虚拟机 / 另一台没装 MSYS2 的 Windows**上试跑，最靠谱。
2. 需要便携分发时，查清动态依赖，按许可把必需 DLL 放进同目录，或调整链接方式减少依赖。
3. 不要假设“gnu 比 msvc 更免安装”——只是依赖从 VC 红包换成了 MinGW 生态。

「❌ 错误场景」——开发机 PATH 里有 `mingw64\bin`，程序“碰巧能跑”；客户机没有，双击就报缺 DLL。

**Go 对比：**
- **Go 怎么做**：更常得到依赖面较窄的单一可执行文件。
- **Rust 为什么不同**：链接器族决定运行时依赖面。
- **Go 程序员易踩的坑**：在开发机验证“能跑”就当部署完成。

**记忆点：**
- gnu 产物也要做“干净机器试跑”；别只在装了 MinGW 的开发机上自测。

---

## Q17. 能把 `msvc` 编的 exe 和 `gnu` 编的 DLL（或反过来）混着加载吗？ {#q17}
**Tags:** `occasional` `windows` `abi`
**适用版本:** Windows / FFI

**一句话答案：**
高风险，默认当作**不行**。两套 Windows ABI / 异常 / 部分调用约定与 C 运行库约定不同，混用极易在边界上炸掉。

**解答：**
同一进程里混用不同工具链编出来的原生组件，常见问题包括：

- 分配器 / CRT 不一致（一边 `malloc`、一边另一套释放）
- 异常与 unwind 边界
- 结构体布局与调用约定细微差异

「✅ 正确做法」：

1. 主程序与所有原生依赖统一用同一套：全 msvc 或全 gnu。
2. 必须对接外部预编译库时，按**该库的工具链**选择 Rust target。
3. 团队文档写明“本仓库 Windows 目标 = …”，CI 与本地一致。

详见 [01-installation Q22](01-installation.md#q22)、[03-compilation Q17](03-compilation.md#q17)。

**Go 对比：**
- **Go 怎么做**：CGO 时也会强调外部 C 编译器与标志一致。
- **Rust 为什么不同**：Windows 上两套目标都是一等公民，混用诱惑更大。
- **Go 程序员易踩的坑**：觉得“都是 x64 Windows 的 `.dll`，加载就行”。

**记忆点：**
- 运行期混 ABI ≈ 埋雷；先统一工具链再谈加载。

---

## Q18. criterion 最小 bench 怎么写、怎么跑？ {#q18}
**Tags:** `common` `criterion` `bench`
**适用版本:** Cargo；criterion 0.5.x（API 以当前文档为准）

**一句话答案：**
用 **criterion**（常用基准框架）写 `benches/*.rs`，在 `Cargo.toml` 里声明 `[[bench]]` 且 `harness = false`，然后 `cargo bench`。目录约定见 [Q7](#q7)；这里补最小可抄模板。

**解答：**
依赖与 bench 目标：

```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "sum"
harness = false
```

`benches/sum.rs`（text，需 criterion）：

```text
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn sum_bench(c: &mut Criterion) {
    c.bench_function("sum 1e6", |b| {
        b.iter(|| {
            let n: u64 = (0..1_000_000).map(|x| black_box(x)).sum();
            black_box(n)
        })
    });
}

criterion_group!(benches, sum_bench);
criterion_main!(benches);
```

运行：

```bash
cargo bench
cargo bench --bench sum
# 只跑名字匹配的：
cargo bench --bench sum -- sum
```

PowerShell 相同。首次会编译较久；报告常在 `target/criterion/`。

无依赖时只能手搓计时（不适合严肃对比，仅示意）：

```rust
fn main() {
    let start = std::time::Instant::now();
    let n: u64 = (0..1_000_000).sum();
    println!("sum={n} elapsed={:?}", start.elapsed());
}
```

`black_box` 防止优化器把被测计算整段消掉；`harness = false` 是因为改用 criterion 自己的 main，而不是 libtest 的 bench harness。

**Go 对比：**

```go
package main

import "testing"

func BenchmarkSum(b *testing.B) {
	for i := 0; i < b.N; i++ {
		var n uint64
		for j := uint64(0); j < 1_000_000; j++ {
			n += j
		}
		_ = n
	}
}
```

- **Go 怎么做**：`go test -bench` + `testing.B`。
- **Rust 为什么不同**：Cargo 用 `benches/` + 常换 criterion；需显式 `harness = false`。
- **Go 程序员易踩的坑**：写了 `benches/foo.rs` 却忘了 `[[bench]]` / `harness = false`，或用 `cargo test` 当 bench。

**记忆点：**
- `dev-dependencies` + `[[bench]] harness = false` + `cargo bench`。
- 严肃测量用 criterion，别只靠 `Instant`。

---
