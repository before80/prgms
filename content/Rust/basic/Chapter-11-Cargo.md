+++
title = "第 11 章 Cargo 与项目管理"
weight = 110
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 11 章 Cargo 与项目管理

> "如果 Rust 是一门武侠小说，那 Cargo 就是那个帮你打怪升级、买装备、加buff的超级NPC。没有 Cargo，你得自己造剑、自己磨刀、自己找秘籍。有了 Cargo，你只需要喊一声'cargo build'，装备就到手了！"

在 Rust 的世界里，Cargo 就是你的贴身管家。它帮你：

- 下载和管理依赖（不需要再手动去官网下载 .zip 包了！）
- 编译项目（不需要记那些复杂的 `rustc` 参数）
- 运行测试（点点手指，自动帮你跑测试）
- 生成文档（一键导出注释文档）
- 发布到 crates.io（让全世界都用你的代码）

这一章，我们就来深入了解 Cargo 的各种骚操作——不是那种表面的 `cargo build`，而是**真正的高手用法**。准备好了吗？

---

## 11.1 Cargo 深度使用

### 11.1.1 Cargo.toml 完整字段解析

#### 11.1.1.1 [package] 完整字段

`[package]` 是 Cargo.toml 的"户口本"，记录了一个 Package 的所有基本信息：

```toml
[package]
# ============ 必填字段 ============
name = "awesome-project"        # 包名，全宇宙唯一（小写 + 横线）
version = "0.1.0"               # 语义化版本（SemVer）
edition = "2021"                # Rust 版本（2015/2018/2021/2024）

# ============ 可选元数据 ============
authors = ["Alice <alice@example.com>", "Bob <bob@example.com>"]
description = "这是一个超级 awesome 的项目！"  # 一句话描述
license = "MIT OR Apache-2.0"   # 许可证（可用 OR 组合）
license-file = "LICENSE.txt"    # 如果不用标准许可证
readme = "README.md"            # README 文件路径
homepage = "https://example.com" # 项目主页
repository = "https://github.com/example/awesome-project" # 仓库地址
documentation = "https://docs.rs/awesome-project"  # 文档地址
categories = ["development-tools", "utility"]  # crates.io 分类
keywords = ["cli", "tool", "utility"]   # 搜索关键字
rust-version = "1.70"           # 最低支持版本（Rust 1.56+）

# ============ 发布相关 ============
exclude = ["*.md", "tests/"]     # 发布时排除的文件
include = ["src/", "Cargo.toml"] # 强制包含的文件
autobenches = true               # 自动检测 benches/ 目录作为基准测试（无 [[bench]] 时）
```

> **命名规范**：Cargo 包的命名必须是 lowercase-with-kebab-case（全是小写，单词用横线连接）。比如 `my-awesome-tool`，而不是 `MyAwesomeTool` 或 `my_awesome_tool`。

#### 11.1.1.2 [lib] / [[bin]] 完整字段

当你的 Package 包含库或多个二进制时：

```toml
# 库 Crate 配置
[lib]
name = "mylib"                    # 库的名字（影响依赖引用）
crate-type = ["lib", "cdylib", "rlib"]  # 产生的库类型
path = "src/lib.rs"               # 入口文件

# 多个二进制
[[bin]]
name = "my-app"                   # 二进制名字（生成 my-app.exe）
path = "src/main.rs"              # 入口文件
required-features = ["full"]     # 构建此二进制需要的 features

[[bin]]
name = "my-tool"
path = "src/bin/tool.rs"
```

#### 11.1.1.3 [workspace] 完整字段

```toml
[workspace]
members = ["crate-a", "crate-b"]  # workspace 成员
exclude = ["crate-c"]            # 排除的包
resolver = "2"                    # 依赖解析器版本（"1" 或 "2"）
```

#### 11.1.1.4 [patch] / [replace]（依赖覆盖）

有时候你需要临时修改某个依赖的版本或源码（比如修 bug），这时候可以用 `patch`：

```toml
[workspace]
members = ["my-app", "my-lib"]

[patch.crates-io]
# 临时覆盖 crates.io 上的某个依赖
some-crate = { path = "../some-crate" }  # 使用本地路径
another-crate = { git = "https://github.com/...", branch = "master" }

[patch.https://github.com/example/repo]
# 也可以 patch 某个 git 依赖
fix-crate = { path = "./fixes/fix-crate" }
```

> **warning**：`[replace]` 已经被废弃了，现在统一使用 `[patch]`。

---

### 11.1.2 Cargo.lock 管理

#### 11.1.2.1 Cargo.lock 的作用（记录精确依赖版本）

`Cargo.lock` 是 Cargo 自动生成的文件，它记录了**每个依赖的精确版本**，确保每次构建结果一致。

```toml
# Cargo.lock 示例（实际是 TOML 格式）
version = 3

[[package]]
name = "serde"
version = "1.0.193"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "25dd9975e68d0cb5aa1120c288333fc98731bd1dd12bb1cf1f6e1002e22e803c"

[[package]]
name = "tokio"
version = "1.32.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
dependencies = [
    { name = "bytes" },
    { name = "memchr" },
    { name = "serde" },
]
```

#### 11.1.2.2 cargo update（更新依赖版本）

```bash
# 更新所有依赖到符合 Cargo.toml 约束的最新版本
cargo update

# 更新特定依赖
cargo update serde

# 更新某个 git 依赖到最新的 commit
cargo update -p some-crate --git https://github.com/example/repo

# 更新到某个版本（如果有新版本符合 semver 约束）
cargo update -p serde --precise 1.0.200
```

#### 11.1.2.3 Cargo.lock 的提交（应提交到版本控制）

**重要的事情说三遍**：`Cargo.lock` **必须**提交到 Git（或其他版本控制）！

```bash
# .gitignore 中不要忽略 Cargo.lock
# 如果不小心忽略了，可以恢复：
git checkout HEAD -- Cargo.lock
```

> **为什么？** 因为 `Cargo.lock` 保证了团队成员和 CI/CD 构建使用**完全相同**的依赖版本。没有它，`cargo build` 可能会拉取不同的小版本，导致"在我机器上能跑"（Works On My Machine）的尴尬局面。

---

### 11.1.3 依赖版本规范

#### 11.1.3.1 ^ 版本约束（默认，^1.0.0 → >=1.0.0 <2.0.0）

Cargo 默认使用 **caret**（^）约束，意思是"只要主版本号不变，任何更新都行"：

```toml
[dependencies]
# ^1.0.0 表示 >=1.0.0 且 <2.0.0
# 1.2.3、1.9.9 都可以，但 2.0.0 不行
serde = "^1.0"

# 相当于
serde = ">=1.0.0, <2.0.0"
```

#### 11.1.3.2 ~ 版本约束（~1.0.0 → >=1.0.0 <1.1.0）

**Tilde** 约束更保守一些，只允许补丁版本更新：

```toml
[dependencies]
# ~1.0.0 表示 >=1.0.0 且 <1.1.0
# 1.0.0、1.0.5 可以，但 1.1.0 不行
small-patch = "~1.0.0"

# ~1.0 表示 >=1.0.0 且 <2.0.0（同 ^）
relaxed = "~1.0"
```

#### 11.1.3.3 >= / <= / * 约束

```toml
[dependencies]
# 允许任意版本（不推荐，可能有 breaking changes）
any-version = "*"

# 最低版本要求
min-version = ">=1.0.0"

# 版本范围
range = ">=1.0.0, <2.0.0"

# 多个不连续版本
alternatives = "1.0.0 || 2.0.0"

# 精确版本（锁定到某个具体版本）
exact = "=1.0.0"
```

#### 11.1.3.4 git 依赖：git = "..." / branch / tag / rev

```toml
[dependencies]
# 从 git 仓库拉取
git-crate = { git = "https://github.com/example/repo.git" }

# 指定分支（默认是仓库的默认分支，通常是 main）
branch-crate = { git = "https://github.com/example/repo.git", branch = "develop" }

# 指定标签
tag-crate = { git = "https://github.com/example/repo.git", tag = "v1.0.0" }

# 指定具体 commit（最精确）
rev-crate = { git = "https://github.com/example/repo.git", rev = "abc123def" }

# 带 features 的 git 依赖
feature-crate = { git = "https://github.com/example/repo.git", default-features = false, features = ["full"] }
```

#### 11.1.3.5 path 依赖：path = "..."（本地 crate 依赖）

在 workspace 中经常用到：

```toml
# 依赖本地的另一个 crate
local-crate = { path = "../my-utils" }

# 带版本约束的 path 依赖
pinned-local = { path = "../my-lib", version = "0.1.0" }

# 带 features 的 path 依赖
configured-local = { path = "../my-lib", features = ["derive"] }
```

---

### 11.1.4 dev / build / proc-macro 依赖

#### 11.1.4.1 [dev-dependencies]（仅 cargo test 时编译）

```toml
[dev-dependencies]
# 测试辅助
criterion = "0.5"          # 性能基准测试
proptest = "1.0"            # 属性测试
quickcheck = "1.0"           # 随机属性测试

# Mock 库
mockall = "0.11"            # 静态 mock
fake = { version = "2.0", features = ["derive"] }  # 假数据生成

# 测试框架
rstest = "0.17"            # 参数化测试
tokio-test = "0.4"         # async 测试

# 其他测试工具
tempfile = "3.0"            # 临时文件/目录
assert_cmd = "2.0"          # 测试命令行程序
predicates = "3.0"         # 断言辅助
```

#### 11.1.4.2 [build-dependencies]（仅 build.rs 编译）

```toml
[build-dependencies]
# 代码生成
quote = "1.0"
syn = { version = "2.0", features = ["full", "parsing"] }
proc-macro2 = "1.0"
paste = "1.0"

# 构建辅助
version_check = "0.9"
rustc_version = "0.4"
```

#### 11.1.4.3 [proc-macro]（过程宏 crate）

如果你的 crate 是专门用来写过程宏的：

```toml
[lib]
proc-macro = true  # 告诉 Cargo 这个 crate 是过程宏

# 过程宏 crate 只能依赖这些
[dependencies]
proc-macro2 = "1.0"
quote = "1.0"
syn = { version = "2.0", features = ["full", "parsing", "extra-traits"] }
```

---

### 11.1.5 [features]（条件编译）

#### 11.1.5.1 features 基础（条件编译与可选依赖）

`[features]` 允许你定义**特性标志**，用于条件编译和可选依赖：

```toml
[features]
# 定义一个空 feature（无依赖）
derive = []

# 组合多个 features
full = ["derive", "serde", "random"]
```

然后在代码中使用 `#[cfg(feature = "...")]`：

```rust
// 只有启用 derive feature 时才编译这个模块
#[cfg(feature = "derive")]
pub mod derive_gen;

#[cfg(feature = "serde")]
use serde::{Serialize, Deserialize};
```

#### 11.1.5.2 optional 依赖（隐式 feature）

把依赖标记为 `optional = true`，Cargo 会自动创建同名 feature：

```toml
[dependencies]
# 这个依赖默认不编译，除非启用对应的 feature
toml = { version = "0.8", optional = true }

[features]
# 启用 toml 支持（自动启用 toml 依赖）
toml-support = ["dep:toml"]  # dep: 前缀是 Rust 1.60+ 语法
```

> **小技巧**：如果你不想暴露内部依赖名，可以用 `dep:xxx` 语法来禁用隐式 feature。比如 `my-internal-dep = { version = "1.0", optional = true }`，然后在 features 中用 `cool-feature = ["dep:my-internal-dep"]` 而不是 `cool-feature = ["my-internal-dep"]`。

#### 11.1.5.3 default feature（默认启用的特性）

```toml
[dependencies]
log = { version = "0.4", optional = true }
serde = { version = "1.0", optional = true }

[features]
# 默认启用的 features（用户不指定时会启用这些）
default = ["full", "logging"]

# 基础 features
logging = ["dep:log"]
derive = ["dep:serde"]
serde = ["dep:serde"]

# 组合型 feature
full = ["derive", "serde", "logging"]
```

```bash
# 禁用默认 features
cargo build --no-default-features

# 只启用特定 feature
cargo build --no-default-features --features derive
```

#### 11.1.5.4 依赖的 features（开启依赖的特定特性）

```toml
[dependencies]
serde = { version = "1.0", optional = true }

[features]
# 这里的 dep: 前缀告诉 Cargo serde 是可选依赖
derive = ["dep:serde"]  # dep: 前缀是 Rust 1.60+ 语法
```

还可以用 `package/feature` 语法：

```toml
[dependencies]
jpeg-decoder = { version = "0.1", default-features = false }

[features]
# 让我们的 parallel feature 也启用 jpeg-decoder 的 rayon feature
parallel = ["jpeg-decoder/rayon"]
```

#### 11.1.5.5 相斥 features（互斥特性）

虽然**强烈不推荐**使用互斥 features（因为 feature 统一机制），但如果你真的需要：

```toml
[dependencies]
critical-section = { version = "1.0", optional = true }

[features]
std = ["critical-section"]
no_std = []  # 互斥！启用此特性时不应启用 std
```

> **警告**：互斥 features 是高级操作，99% 的情况你不需要。如果你的场景真的需要互斥，考虑是否应该拆成两个 crate。

---

### 11.1.6 Cargo 子命令

#### 11.1.6.1 cargo build / cargo check / cargo rustc

```bash
# 构建项目（生成 target/debug/ 可执行文件）
cargo build

# 快速检查代码是否能编译（不生成文件，比 build 快很多）
# 适合在编写代码时频繁检查
cargo check

# 直接调用 rustc，传递额外参数
cargo rustc -- -C opt-level=3
```

#### 11.1.6.2 cargo run（运行二进制）

```bash
# 运行主二进制
cargo run

# 运行指定的二进制
cargo run --bin my-binary

# 传递参数给程序
cargo run -- "arg1" "arg2"
cargo run -- --config config.toml  # 程序自己的参数

# 开发时启用 debug features
cargo run --features "debug,ssl"
```

#### 11.1.6.3 cargo test / cargo bench

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test test_name

# 运行 doc tests
cargo test --doc

# 运行集成测试
cargo test --test integration

# 详细输出（显示 println!）
cargo test -- --nocapture

# 运行基准测试（需要先在 Cargo.toml 中配置 [[bench]] 或 benches/ 目录）
cargo bench

# 基准测试结果会输出到 target/criterion/ 目录
# 可以用 cargo-benchmark-support 或其他工具生成可视化报告
```

#### 11.1.6.4 cargo doc / cargo doc --open

```bash
# 生成文档（输出到 target/doc/）
cargo doc

# 生成文档并自动打开浏览器
cargo doc --open

# 只生成当前 crate 的文档（不包含依赖）
cargo doc --no-deps

# 包含私有项的文档
cargo doc --document-private-items
```

#### 11.1.6.5 cargo clean / cargo fmt / cargo clippy

```bash
# 清理构建产物
cargo clean

# 格式化代码（按照 Rust 风格指南）
cargo fmt

# 检查格式（不修改，只报告）
cargo fmt -- --check

# 运行 clippy（Rust linter，比默认检查更严格）
cargo clippy

# clippy 警告当错误
cargo clippy -- -D warnings

# 自动修复 clippy 警告
cargo clippy --fix --allow-dirty
```

#### 11.1.6.6 cargo install（安装工具到 ~/.cargo/bin）

```bash
# 安装二进制工具到 ~/.cargo/bin/
cargo install cargo-watch     # 文件监控，自动重新编译
cargo install cargo-edit       # 增删依赖命令：cargo add/rm
cargo install cargo-outdated   # 检查过时依赖
cargo install bat             # cat 的替代品，支持语法高亮
cargo install exa              # ls 的替代品

# 安装后确保 ~/.cargo/bin 在 PATH 中
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 11.1.6.7 cargo search / cargo info（ crates.io 搜索）

```bash
# 搜索 crates.io
cargo search serde
# Output:
# serde - 通用序列化框架 (version: 1.0.193)
# serde_json - JSON 序列化 (version: 1.0.108)
# serde_yaml - YAML 序列化 (version: 0.9.27)

# 查看 crate 详细信息
cargo info serde
```

#### 11.1.6.8 cargo tree（依赖树可视化）

```bash
# 查看完整依赖树
cargo tree

# 反向依赖（谁依赖了我）- 注意需要用 -p 指定包
cargo tree --invert -p serde

# 查看整个 workspace 的反向依赖
cargo tree --invert --workspace -p serde

# 只显示特定 crate 的依赖
cargo tree -p tokio

# 去重显示（合并重复的依赖）
cargo tree -d

# 显示依赖的平台
cargo tree -p serde --features derive
```

---

## 11.2 工作空间高级主题

### 11.2.1 Workspace 成员配置

#### 11.2.1.1 members / exclude

```toml
[workspace]
members = [
    "packages/core",
    "packages/api",
    "packages/cli",
    "tools/migrate",
    "examples/web-app",
]

# 排除某些包（即使它们在 members 里）
exclude = ["packages/deprecated"]
```

#### 11.2.1.2 resolver = "2"（解决依赖冲突）

`resolver = "2"` 是 Rust 2021 edition 的默认值（也是推荐值）。它解决了以前 resolver 的一些问题：

```toml
[workspace]
resolver = "2"

# resolver = "1" 遗留的行为：
# - dev-dependencies 也会被解析，即使不用 test
# - build-dependencies 也会被解析，即使不用 build
```

> **推荐**：始终使用 `resolver = "2"`，它更智能，解析更快。

---

### 11.2.2 跨 Crate 依赖

#### 11.2.2.1 workspace 成员依赖（path = "../sibling"）

```toml
# packages/core/Cargo.toml
[package]
name = "core"
version = "0.1.0"

[dependencies]
# 依赖 workspace 内的其他成员
api = { path = "../api" }
utils = { path = "../utils" }

# 继承 workspace 级别的依赖
log = "0.4"
serde = "1.0"
```

#### 11.2.2.2 版本提升规则

在 workspace 中，所有成员的共享依赖版本会自动"提升"到 workspace 级别：

```toml
# 假设 core/Cargo.toml:
# [dependencies]
# serde = "1.0"
#
# api/Cargo.toml:
# [dependencies]
# serde = "1.0"
#
# Cargo 会在 workspace 根目录使用 serde = "1.0"
# Cargo.lock 中只有一个 serde 条目
```

---

### 11.2.3 MSRV（Minimum Supported Rust Version）策略

#### 11.2.3.1 rust-version 字段（package 级别）

```toml
[package]
name = "my-project"
version = "0.1.0"
rust-version = "1.70"  # 最低支持 Rust 1.70

# 这意味着：
# - 你的包不保证能在 Rust 1.69 或更早版本编译
# - Cargo 会检查工具链版本
```

#### 11.2.3.2 CI 中的 MSRV 检查（msrv-ci）

在 GitHub Actions 中添加 MSRV 检查：

```yaml
# .github/workflows/msrv.yml
name: MSRV Check

on:
  push:
    branches: [main]
  pull_request:

jobs:
  msrv:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        # 要测试的 Rust 版本
        rust:
          - "1.70"  # MSRV
          - "stable"
          - "nightly"
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust ${{ matrix.rust }}
        uses: dtolnay/rust-toolchain@master
        with:
          toolchain: ${{ matrix.rust }}
      
      - name: Check
        run: cargo check
        
      - name: Test
        run: cargo test
```

#### 11.2.3.3 cargo-msrv（自动化 MSRV 测试）

```bash
# 安装
cargo install cargo-msrv

# 自动测试 MSRV
cargo msrv verify

# 搜索最低支持版本
cargo msrv search

# 输出：
# 1.70.0: ✓ buildable
# 1.69.0: ✗ build failed
# 最低支持版本: 1.70.0
```

---

## 11.3 发布与版本管理

### 11.3.1 crates.io 上传

#### 11.3.1.1 cargo login（认证）

```bash
# 1. 去 https://crates.io/new 申请 API Token
# 2. 登录
cargo login <your-api-token>

# Token 会被保存到 ~/.cargo/credentials.toml
# 格式：
# [registry]
# token = "..."
```

#### 11.3.1.2 cargo publish（上传）

```bash
# 确认 Cargo.toml 信息正确
# 确保 version 是新版本号
# 确保 README 完整

# 上传到 crates.io
cargo publish

# 如果有 workspace，只发布特定 crate
cargo publish -p my-crate

# 覆盖检查（用于修复小问题后立即重新发布）
# 仅在版本发布后 24 小时内有效
cargo publish --dry-run  # 先检查
cargo publish --allow-dirty  # 允许 dirty 状态发布（不推荐）
```

#### 11.3.1.3 cargo logout

```bash
# 登出，清除保存的 token
cargo logout
```

#### 11.3.1.4 cargo yank --version（撤销版本）

当某个版本有严重 bug 需要撤回时：

```bash
# 撤销版本 0.1.1（已经下载的用户不受影响，但新项目不能依赖这个版本）
cargo yank --vers 0.1.1

# 撤销后，原有项目仍然可以正常使用
# 但新的 Cargo.toml 不能写 serde = "=0.1.1"
# 这是"软删除"，不是真的删除

# 取消 yank
cargo yank --vers 0.1.1 --undo
```

#### 11.3.1.5 发布流程（version bump → cargo publish → git tag）

标准发布流程：

```bash
# 1. 确保所有测试通过
cargo test --all
cargo clippy --all
cargo fmt -- --check

# 2. 更新版本号
# 手动修改 Cargo.toml，或者使用 cargo-release
# patch: 0.1.0 -> 0.1.1
# minor: 0.1.0 -> 0.2.0
# major: 0.1.0 -> 1.0.0

# 3. 提交更改
git add -A
git commit -m "Release v0.2.0"
git tag v0.2.0
git push origin main --tags

# 4. 发布
cargo publish

# 5. 创建 GitHub Release（如果用 GitHub）
gh release create v0.2.0 \
  --title "Version 0.2.0" \
  --notes "See CHANGELOG for details"
```

> **cargo-release**：自动化发布工具
> ```bash
> cargo install cargo-release
> cargo release --execute  # 交互式发布
> cargo release patch --execute  # 自动 bump patch 版本
> ```

---

## 本章小结

这一章我们深入探索了 Cargo 的各种高级用法：

1. **Cargo.toml 完整配置**：package、lib、bin、workspace、patch、features
2. **Cargo.lock**：精确版本锁定，必须提交到版本控制
3. **依赖版本规范**：^、~、>=、git、path
4. **四类依赖**：`[dependencies]`、`[dev-dependencies]`、`[build-dependencies]`、`[proc-macro]`
5. **Features 特性**：条件编译、可选依赖、default feature、依赖 features
6. **Cargo 子命令**：build、check、run、test、bench、doc、fmt、clippy、tree、install、search
7. **Workspace 进阶**：resolver = "2"、成员依赖共享
8. **MSRV 策略**：`rust-version` 字段、CI 检查、cargo-msrv
9. **发布流程**：login、publish、yank、版本管理

**记住**：Cargo 不仅仅是一个包管理器，它是 Rust 生态系统的核心。熟练掌握 Cargo，你就能在这个生态里游刃有余。从今天起，把 `cargo build` 练成肌肉记忆，把 `cargo test` 当成每日三省吾身，你会发现——原来写 Rust 代码可以这么爽！

> "在 Rust 的世界里，Cargo 就是你的超级英雄披风。不会用它？你永远不知道自己能飞多高！"

