+++
title = "02-updating"
date = 2026-07-28T14:49:00+08:00
weight = 20
type = "docs"
description = "讲清 Rust 工具链更新、锁版本、channel 与团队协作的关键问题。"
isCJKLanguage = true
draft = false

+++

# 更新与版本管理 (Updating)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会把 `rustup update` 和 `cargo update` 混成一件事？
- 你是否想知道：怎么把项目固定在某个 Rust 版本，而不是让大家各用各的？
- 你会不会更新了 stable，却发现项目里 `rustc --version` 还是老版本？
- 你是否分不清 stable / beta / nightly 该在哪些场景用？
- 你会不会在升级 edition 或 nightly 日期版时，不知道怎么安全回退？
- 本机同时装了 `*-msvc` 和 `*-gnu` 时，更新到底更新谁？工具链文件该怎么写？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| channel | — | 发布通道 | `stable` / `beta` / `nightly` 这类版本轨道 | Go 发行版分支 |
| stable | — | 稳定通道 | 适合学习和生产的官方稳定版本 | 正式 Go 版本 |
| beta | — | 测试通道 | 下一版 stable 的预览 | RC / 预发布测试 |
| nightly | — | 夜间通道 | 每天构建，包含未稳定特性 | tip / 开发分支近亲 |
| override | — | 目录级覆盖 | 在某目录强制用指定工具链 | 本地目录级版本覆盖 |
| `Cargo.lock` | — | 锁文件 | 记录依赖的确切版本 | `go.sum` + 实际 module 解析结果近亲 |
| semver | Semantic Versioning | 语义化版本 | 用主次修规则描述兼容性 | Go module 版本规则 |
| edition | — | 语言版本世代 | 一组语法/默认行为选择，不等同于 rustc 版本 | Go 无直接对应 |
| `MSRV` | Minimum Supported Rust Version | 最低支持 Rust 版本 | 项目承诺支持的最低 rustc 版本 | 最低 Go 版本要求 |
| `CI` | Continuous Integration | 持续集成 | 自动跑构建和测试的流水线 | 同概念 |
| toolchain file | — | 工具链文件 | `rust-toolchain.toml`，项目级锁定工具链 | `go.mod` 里声明 Go 版本的近亲 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q4](#q4), [Q6](#q6), [Q8](#q8) |
| `common` | [Q3](#q3), [Q5](#q5), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q13](#q13), [Q14](#q14) |
| `occasional` | [Q11](#q11), [Q15](#q15) |
| `advanced` | [Q12](#q12) |

---

## Q1. 想升级 Rust，本机到底该敲什么命令？ {#q1}
**Tags:** `hot` `beginner` `rustup`
**适用版本:** rustup 管理的安装

**一句话答案：**
升级 Rust 本身用 `rustup update`；它会更新你已安装的 channel 及其组件。

**详细解答：**
最常见两种写法是“全量更新已安装通道”和“只更新 stable”：

```bash
rustup update
rustup update stable
```

更新后再跑下面两条命令确认实际生效的版本：

```bash
rustc --version
rustup show
```

**🐹 Go 对比：**

- **Go 怎么做**：通常安装新 Go 发行版，或让 `goenv` / `asdf` 切到新版。
- **Rust 为什么不同**：Rust 官方把版本管理交给 `rustup`，所以升级入口统一。
- **Go 程序员易踩的坑**：别拿 `cargo update` 当“升级 Rust”；那只管项目依赖，不管编译器。

**小结 / 记忆点：**
- 升 Rust：`rustup update`
- 升依赖：看 [Q2](#q2)

---

## Q2. `rustup update` 和 `cargo update` 到底差在哪？ {#q2}
**Tags:** `hot` `beginner` `cargo`
**适用版本:** Rust 1.0+

**一句话答案：**
`rustup update` 更新工具链；`cargo update` 更新当前项目的依赖解析结果，两者完全不是一层东西。

**详细解答：**
可以把它理解成两层更新：`rustup update` 更新编译器和组件，`cargo update` 更新 `Cargo.lock` 里的依赖解析结果。前者作用在工具链，后者作用在项目。

```bash
rustup update
cargo update
cargo update -p serde
```

**🐹 Go 对比：**

- **Go 怎么做**：升级 Go 自身是一件事，升级项目依赖又是另一件事。
- **Rust 为什么不同**：Rust 把这两层分得更明确，所以命令也分在 `rustup` 和 `cargo`。
- **Go 程序员易踩的坑**：看到项目编不过，以为先升级 rustc；其实很多时候只是依赖锁文件需要更新。

**小结 / 记忆点：**
- `rustup` 管工具链。
- `cargo` 管项目依赖。

---

## Q3. 为什么我明明更新了 stable，进项目后还是老版本？ {#q3}
**Tags:** `common` `override`
**适用版本:** rustup

**一句话答案：**
因为当前目录可能被 `rust-toolchain.toml`、`rustup override` 或 `cargo +toolchain` 临时覆盖了，目录里的“生效版本”不一定等于全局 default。

**详细解答：**
先看 `rustup show active-toolchain` 或 `rustup show`，它会告诉你当前目录到底在用谁。最常见的覆盖来源就是 `rust-toolchain.toml`、`rustup override`，或者临时的 `cargo +nightly ...`。

```bash
rustup show active-toolchain
rustup show
```

**🐹 Go 对比：**

- **Go 怎么做**：`go.mod` 会表达版本要求，但编译器切换通常不那么“目录自动化”。
- **Rust 为什么不同**：Rust 把“项目应使用哪套工具链”前置成了第一等问题。
- **Go 程序员易踩的坑**：只看全局 `rustup default`，不看项目目录里的工具链文件。

**小结 / 记忆点：**
- “我本机是什么版本”与“这个项目现在用什么版本”是两件事。

---

## Q4. 项目里该怎么锁死 Rust 版本？ {#q4}
**Tags:** `hot` `beginner` `toolchain-file`
**适用版本:** rustup

**一句话答案：**
最推荐的做法是在仓库根目录提交 `rust-toolchain.toml`；这样本地、CI、编辑器都会更容易对齐到同一版本。

**详细解答：**
一个最小的 `rust-toolchain.toml` 通常长这样：

```toml
[toolchain]
channel = "1.97.1"
components = ["clippy", "rustfmt"]
```

把它提交进仓库后，开发者进入目录时，`rustup` 就会自动按这个文件选工具链。

**🐹 Go 对比：**

- **Go 怎么做**：常用 `go.mod` 声明项目面向的 Go 版本。
- **Rust 为什么不同**：Rust 常需要连具体工具链一起锁住，而不是只写一个“最低版本意图”。
- **Go 程序员易踩的坑**：靠团队口头约定版本，不把版本文件提交进仓库。

**小结 / 记忆点：**
- 团队协作优先提交 `rust-toolchain.toml`。

---

## Q5. `rustup override` 又是什么？跟工具链文件哪个好？ {#q5}
**Tags:** `common` `override`
**适用版本:** rustup

**一句话答案：**
`rustup override` 是你本地目录级覆盖；团队协作一般优先 `rust-toolchain.toml`，因为后者能进 Git、别人也能看到。

**详细解答：**
`rustup override` 只写在你本机的 rustup 设置里，不会进 Git；`rust-toolchain.toml` 会随仓库走，别人 `cd` 进来就能对齐。

常用命令：

```bash
# 当前目录强制用某工具链
rustup override set 1.97.1
# 或：rustup override set nightly-2026-07-01

# 查看本机所有目录级覆盖
rustup override list

# 取消当前目录的覆盖（恢复看 default / toolchain 文件）
rustup override unset
```

override 更像你的本地临时设置；toolchain file 更像项目对团队的公开约定。两者同时存在时，以 `rustup show` 显示的 active toolchain 为准。

**🐹 Go 对比：**

- **Go 怎么做**：本地临时切版本常见，但团队规范最好也要有仓库内文件承载。
- **Rust 为什么不同**：Rust 的 override 完全可能只在你机子上生效，别人根本不知道。
- **Go 程序员易踩的坑**：以为本地 override 就等于“项目已经锁版本”。

**小结 / 记忆点：**
- 自己临时玩：`override set` / `unset` / `list`
- 团队长期用：`rust-toolchain.toml`

---

## Q6. stable / beta / nightly 应该怎么选？ {#q6}
**Tags:** `hot` `beginner` `channel`
**适用版本:** Rust 1.0+

**一句话答案：**
学习和生产默认用 stable；想提前验证下个稳定版用 beta；只有确实要未稳定特性时才用 nightly，并且要把“仅 nightly”写进工具链文件、源码和文档三处，别靠口头约定。

**详细解答：**
- **stable**：默认答案，学习和生产都优先它。
- **beta**：提前试下一个 stable，适合 CI 里加一条“预览通道”任务。
- **nightly**：只适合需要 `#![feature(...)]` 的实验性代码，或验证编译器前沿行为；它不是“更高级的 stable”。

若项目必须依赖 nightly，至少把依赖点写清楚：

1. 项目根 `rust-toolchain.toml` 锁日期通道：

```toml
[toolchain]
channel = "nightly-2026-07-01"
components = ["clippy", "rustfmt"]
```

2. 在 crate 根（`src/main.rs` 或 `src/lib.rs`）顶部声明未稳定特性：

```rust
#![feature(try_blocks)] // 仅示意：具体 feature 名换成你真正用到的

fn main() {
    let result: Result<i32, &str> = try {
        Err("boom")?;
        1
    };
    let _ = result;
}
```

3. README / 项目文档里单独用二级标题标明 **Nightly only**，正文例如：

```text
本仓库依赖 nightly 工具链与 #![feature(...)]，请使用
rust-toolchain.toml 中的 nightly-YYYY-MM-DD，不要用漂移的 nightly。
```

**🐹 Go 对比：**

- **Go 怎么做**：大多数团队默认正式版；实验性功能一般不会进主线生产。
- **Rust 为什么不同**：Rust 明确把未稳定特性放进 nightly，边界很清楚。
- **Go 程序员易踩的坑**：为了图新鲜把 nightly 设成 default，结果每隔几天就被破坏性变化绊住。

**小结 / 记忆点：**
- 默认 stable。
- nightly 要锁日期，并在工具链文件、源码、文档三处写明。

---

## Q7. 什么是 edition？升级 `2021` 到 `2024` 等于升级 rustc 吗？ {#q7}
**Tags:** `common` `edition`
**适用版本:** Edition 2024 需 Rust 1.85+

**一句话答案：**
不是。edition 是一组语法和默认行为选择；升级 edition 不等于升级编译器版本，但新 edition 需要足够新的 rustc 支持。

**详细解答：**
edition 关注源码语义，不是编译器发行号。就算两个项目都用同一个 `rustc`，也可能一个写 `edition = "2021"`，另一个写 `edition = "2024"`。

edition 写在 `Cargo.toml` 的 `[package]` 里，例如：

```toml
[package]
name = "demo"
version = "0.1.0"
edition = "2024"
```

同一工具链下，把这里的 `"2024"` 换成 `"2021"`，语言默认行为会跟着变；这和把 `rustc` 从 1.85 升到 1.97 **不是一回事**。新 edition 只是要求足够新的 rustc 才能编译（例如 Edition 2024 需要 Rust 1.85+）。

**🐹 Go 对比：**

- **Go 怎么做**：语义变化更多直接跟 Go 版本前进。
- **Rust 为什么不同**：Rust 用 edition 让新写法逐步演进，同时尽量保住旧代码兼容。
- **Go 程序员易踩的坑**：把 `edition = "2024"` 理解成“我项目就只能在 2024 年的编译器上跑”。

**小结 / 记忆点：**
- edition 不是 rustc 版本号。

---

## Q8. 升级 edition 时，最稳的步骤是什么？ {#q8}
**Tags:** `hot` `beginner` `edition`
**适用版本:** `cargo fix --edition`

**一句话答案：**
先确认测试是绿的，再跑 `cargo fix --edition`，然后改 `Cargo.toml` 里的 `edition`，最后重新 `clippy` 和 `test`。

**详细解答：**
升级 edition 前，先保证当前分支干净且测试通过。更稳妥的步骤通常是：

```bash
cargo fix --edition
```

然后把 `Cargo.toml` 里的 edition 改成目标世代，例如从 `2021` 升到 `2024`：

```toml
[package]
name = "demo"
version = "0.1.0"
edition = "2024"
```

最后再全量验证：

```bash
cargo clippy
cargo test
```

升级 edition 是代码迁移，不只是改一行字符串。

**🐹 Go 对比：**

- **Go 怎么做**：升级语言版本后同样要完整回归测试。
- **Rust 为什么不同**：edition 迁移有专门工具 `cargo fix --edition` 可辅助机械修改。
- **Go 程序员易踩的坑**：只改 `Cargo.toml`，不跑自动修复和测试。

**小结 / 记忆点：**
- 先 `fix`，再改 edition，最后全量验证。

---

## Q9. `Cargo.lock` 该不该提交？ {#q9}
**Tags:** `common` `Cargo.lock`
**适用版本:** Rust 1.0+

**一句话答案：**
二进制 / 可执行应用默认提交 `Cargo.lock`；发布到 crates.io 的纯库通常不提交；workspace 里若含应用或要固定 CI，也可以提交。

**详细解答：**
`Cargo.lock` 的核心价值是可复现构建：同事和 CI 拿到同一套依赖解析结果，而不是每次重新“猜”兼容版本。

默认可执行建议：

| 项目类型 | 是否提交 `Cargo.lock` | 原因 |
|---|---|---|
| 二进制应用（CLI / 服务） | **提交** | 部署与 CI 要可复现 |
| 发布到 crates.io 的纯库 | **通常不提交** | 下游会按自己的锁文件解析；库侧不锁死用户依赖图 |
| workspace（含 bin / 多包） | **可提交** | 固定工作区整体构建与 CI 结果 |

库作者仍应在文档里写清 MSRV，并在 CI 里用 `cargo generate-lockfile` + `cargo test` 验证某组依赖能编过。

**🐹 Go 对比：**

- **Go 怎么做**：团队通常会提交 `go.sum`，保持依赖解析可追踪。
- **Rust 为什么不同**：Rust 里 `Cargo.lock` 直接锁定了解析结果，尤其对应用程序价值很大。
- **Go 程序员易踩的坑**：把 lock 文件当“缓存”删掉不管，导致团队和 CI 依赖版本漂移。

**小结 / 记忆点：**
- 应用提交；纯库通常不提交；workspace 可提交。

---

## Q10. 项目要声明最低支持 Rust 版本，应该写哪？ {#q10}
**Tags:** `common` `MSRV`
**适用版本:** `rust-version` 已稳定多年

**一句话答案：**
在 `Cargo.toml` 的 `[package]` 下写 `rust-version`；这表达的是 **MSRV**（Minimum Supported Rust Version，最低支持 Rust 版本）。

**详细解答：**
在 `Cargo.toml` 里这样声明：

```toml
[package]
name = "demo"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"
```

MSRV 是“至少支持到哪”，不一定等于团队当前日常开发版本。日常开发版本更常写在 `rust-toolchain.toml` 里。

**🐹 Go 对比：**

- **Go 怎么做**：在 `go.mod` 里表达项目面向的 Go 版本。
- **Rust 为什么不同**：Rust 既可用 `rust-version` 表达最低版本，也常用 `rust-toolchain.toml` 锁当前开发版本。
- **Go 程序员易踩的坑**：把 `rust-version` 当成自动切版本工具；它主要是声明兼容要求。

**小结 / 记忆点：**
- `rust-version` 管最低支持版本。
- `rust-toolchain.toml` 更像当前开发版本约定。

---

## Q11. nightly 日期版怎么固定？坏了又怎么退？ {#q11}
**Tags:** `occasional` `nightly`
**适用版本:** nightly；不可当作稳定生产承诺

**一句话答案：**
用 `nightly-YYYY-MM-DD` 这种日期版锁住；如果某天坏了，就换到前一天或回 stable。

**详细解答：**
nightly 适合锁日期，不适合只写一个会漂移的 `nightly`。项目根放：

```toml
[toolchain]
channel = "nightly-2026-07-01"
components = ["clippy", "rustfmt", "rust-src"]
```

某天坏了时，把 `channel` 改成前一天（如 `nightly-2026-06-30`），或临时回 `stable` / 具体版本号；改完后本地与 CI 都会跟着同一文件走。

也可用命令临时试：

```bash
rustup toolchain install nightly-2026-07-01
cargo +nightly-2026-07-01 test
```

**🐹 Go 对比：**

- **Go 怎么做**：试验 tip 时也常要固定到某个提交，便于复现。
- **Rust 为什么不同**：nightly 每天都可能变，所以锁日期非常重要。
- **Go 程序员易踩的坑**：只写 `nightly`，导致今天能编、明天不能编。

**小结 / 记忆点：**
- nightly 用 `nightly-YYYY-MM-DD` 写进 `rust-toolchain.toml`。

---

## Q12. CI 里怎么避免“我本机能过，流水线过不了”的版本漂移？ {#q12}
**Tags:** `advanced` `CI`
**适用版本:** Rust 1.0+

**一句话答案：**
让 CI 读同一个 `rust-toolchain.toml`，或显式安装同版本工具链；不要让本地和流水线各自“猜”要用哪版。

**详细解答：**
CI 最怕版本漂移。做法是让流水线读仓库里同一份 `rust-toolchain.toml`（`dtolnay/rust-toolchain` 等 action 会自动读它），并提交应用侧的 `Cargo.lock`。

最小 GitHub Actions 示例：

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@master
        # 无 toolchain 参数时，会读取仓库根的 rust-toolchain.toml
        with:
          components: clippy, rustfmt
      - run: rustc --version
      - run: cargo test --locked
      - run: cargo clippy --all-targets -- -D warnings
```

本地与 CI 都读同一工具链文件后，再锁依赖、跑 test / clippy，版本漂移会少很多。

**🐹 Go 对比：**

- **Go 怎么做**：流水线里显式安装某个 Go 版本。
- **Rust 为什么不同**：Rust 除编译器外，组件与 target 也要跟版本配套。
- **Go 程序员易踩的坑**：本地用 1.97.1，CI 却在用漂移中的 stable。

**小结 / 记忆点：**
- CI 读同一份 `rust-toolchain.toml`，并用 `--locked` 固定依赖。

---

## Q13. 本机同时装了 `*-msvc` 和 `*-gnu`，`rustup update` 会更新谁？ {#q13}
**Tags:** `common` `windows` `gnu` `msvc`
**适用版本:** rustup

**一句话答案：**
`rustup update` 会更新**本机已安装的各条工具链**；但你当前 `default` / 目录覆盖决定“进项目后实际用哪条”，不会自动把你从 msvc 切到 gnu。

**解答：**
先看自己装了什么：

```powershell
rustup toolchain list
rustup show
```

常见情况：

```text
stable-x86_64-pc-windows-msvc (default)
stable-x86_64-pc-windows-gnu
```

此时：

```powershell
rustup update
# 通常会把已安装的 stable-msvc、stable-gnu 等都拉到最新 stable
```

若只想更新其中一条：

```powershell
rustup update stable-x86_64-pc-windows-gnu
rustup update stable-x86_64-pc-windows-msvc
```

「❌ 错误场景」——更新后以为“已经切到 gnu”：

```powershell
rustup update
rustc -vV
# host 仍可能是 x86_64-pc-windows-msvc（因为 default 没改）
```

「✅ 正确做法」——更新归更新，切换归切换：

```powershell
rustup default stable-x86_64-pc-windows-gnu
# 或项目里用 rust-toolchain.toml / cargo +stable-x86_64-pc-windows-gnu ...
```

安装与 MinGW / VS 前置条件见 [01-installation Q15](01-installation.md#q15) 起。

**Go 对比：**
- **Go 怎么做**：通常只有一套本机 Go，较少“同 OS 两套 ABI 工具链并排更新”。
- **Rust 为什么不同**：Windows 上 msvc/gnu 是两条可同时存在的工具链。
- **Go 程序员易踩的坑**：把 `update` 理解成“顺便改默认 host”。

**记忆点：**
- `update` 管版本新旧；`default` / toolchain 文件管用哪条。

---

## Q14. `rust-toolchain.toml` 写成带 `windows-gnu` / `windows-msvc` 时要注意什么？ {#q14}
**Tags:** `common` `windows` `toolchain-file`
**适用版本:** rustup toolchain file

**一句话答案：**
可以写 `channel = "stable-x86_64-pc-windows-gnu"`（或 msvc）来钉死 host；但 CI / 同事机器仍须自备对应链接器（MinGW 或 VS Build Tools），文件本身不会替你装系统工具。

**解答：**
项目根示例：

```toml
[toolchain]
channel = "stable-x86_64-pc-windows-gnu"
components = ["rustfmt", "clippy"]
```

或：

```toml
[toolchain]
channel = "stable-x86_64-pc-windows-msvc"
components = ["rustfmt", "clippy"]
```

注意：

1. **跨平台仓库**若也要在 Linux/macOS 开发，不要把 Windows 专用 host 写死进公共 `rust-toolchain.toml`；可改用只钉 `stable`（或日期版），Windows ABI 选择交给本机 default / 文档约定。
2. **Windows 专用仓库**才适合钉死 `...-windows-gnu` / `...-windows-msvc`。
3. 换工具链后建议：

```powershell
cargo clean
rustup show active-toolchain
cargo build
```

更完整的固定方式见 [01-installation Q21](01-installation.md#q21)。

**Go 对比：**
- **Go 怎么做**：`go` 指令版本主要约束语言版本，较少钉死 Windows 链接器族。
- **Rust 为什么不同**：channel 名可以带 host 三元组。
- **Go 程序员易踩的坑**：在多 OS 仓库里写死 `windows-gnu`，导致 Linux CI 直接装错工具链。

**记忆点：**
- Windows 专用仓可以钉 host；跨平台仓优先只钉 `stable` / 日期。

---

## Q15. 从默认 `msvc` 改到 `gnu` 之后，组件和更新怎么对齐？ {#q15}
**Tags:** `occasional` `windows` `gnu`
**适用版本:** rustup

**一句话答案：**
组件是**按工具链分别安装**的；切到 gnu 后要在该工具链上再 `component add`，以后更新也要确认 active toolchain 仍是你想要的那条。

**解答：**

```powershell
rustup default stable-x86_64-pc-windows-gnu

# 在“当前默认工具链”上装组件
rustup component add clippy rustfmt rust-src

# 确认
rustup component list --installed
rustc -vV
```

临时用另一条时：

```powershell
cargo +stable-x86_64-pc-windows-msvc clippy
cargo +stable-x86_64-pc-windows-gnu test
```

「❌ 错误场景」——只在 msvc 上装过 clippy，切到 gnu 后：

```powershell
cargo clippy
# error: 'cargo-clippy' is not installed for the toolchain ...
```

「✅ 修法」——对当前工具链再装一次组件。

**Go 对比：**
- **Go 怎么做**：工具大体跟 Go 安装绑定，较少“同一 major 两套 host 各装一遍”。
- **Rust 为什么不同**：每条 toolchain 有自己的组件集合。
- **Go 程序员易踩的坑**：以为装过一次 clippy 就全局永远可用。

**记忆点：**
- 换 Windows host 工具链 = 重新确认组件；更新前先 `rustup show`。

---
