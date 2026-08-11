+++
title = "22-包、Crate 与模块"
date = 2026-07-28T14:49:00+08:00
weight = 220
type = "docs"
description = "面向 Go 用户讲清 package、crate、module、可见性和 workspace 的边界"
isCJKLanguage = true
draft = false

+++

# 包、Crate 与模块 (Packages, Crates and Modules)

> 面向 **Rust 1.97.1** (stable, 2026-07)。如果你习惯了 Go 的“目录 + package 名 + 首字母大写导出”，这一篇最重要的任务就是帮你把 Rust 的三层概念拆开。
>
> 先别急着背语法。只要先分清 package、crate、module 分别在管什么，`mod`、`use`、`pub` 的很多报错就会自己变得顺眼。

Rust 的工程组织比 Go 更显式：`Cargo.toml` 描述 package，crate 是编译单元，module 是命名空间和可见性边界。文件系统只是默认映射方式，不是唯一真相。

## Q1. package、crate、module 分别是什么？ {#q1}
**Tags:** `hot` `package` `crate` `module`
**适用版本:** Rust 1.0+

**一句话答案：** package 是 Cargo 管理单位，crate 是编译单位，module 是 crate 内部的命名空间与可见性边界。

**解答：** 一个 package 对应一份 `Cargo.toml`；一个 package 最多有一个 library crate，但可以有多个 binary crate；module 则是 crate 内部的树状结构，用来组织代码和控制哪些符号能穿过边界被访问。

```rust
mod net {
    pub fn ping() -> &'static str {
        "pong"
    }
}

fn main() {
    println!("{}", net::ping());
}
```

```text
my_app/
|- Cargo.toml          # package
|- src/lib.rs          # library crate root
|- src/main.rs         # default binary crate root
|- src/bin/admin.rs    # another binary crate
`- src/net.rs          # module file
```

第一段代码只展示 module 的概念；第二段目录树展示 package 和 crate 的落点。不要把“一个目录”自动等同于“一个 crate”。

**Go 对比：**
- Go 更强调目录和 package 名的对应关系。
- Rust 额外多了 crate 这层编译单元，因此同一个 package 可以同时产出库和多个二进制。
- `use` 路径看的首先是模块树和 crate 名，不只是物理目录名。

**记忆点：**
- package 管 Cargo 工程。
- crate 管编译产物。
- module 管命名空间和可见性。

## Q2. `lib.rs` 和 `main.rs` 到底是什么关系？ {#q2}
**Tags:** `hot` `lib.rs` `main.rs`
**适用版本:** Rust 1.0+

**一句话答案：** 它们是两个不同 crate 的根文件；同一个 package 里可以同时存在，而且 `main.rs` 可以通过包名引用 `lib.rs` 暴露的公共 API。

**解答：** `src/lib.rs` 是 library crate root，`src/main.rs` 是默认 binary crate root。最常见的组织方式是：把可复用逻辑放进 `lib.rs`，把命令行解析、进程退出码这类入口逻辑放进 `main.rs`。

```rust
mod my_app {
    pub fn greet(name: &str) -> String {
        format!("hello, {name}")
    }
}

use my_app::greet;

fn main() {
    println!("{}", greet("Rust"));
}
```

真实项目里，这段通常会拆成 `src/lib.rs` 和 `src/main.rs` 两个文件；这里写成单文件只是为了让行为能直接编译验证。代码里的 `my_app` 对应真实项目中的包名；如果包名里有连字符，比如 `my-app`，代码里要写成 `my_app`。

**Go 对比：**
- Go 的 `package main` 和可导入包不会共存在同一个目录里扮演两种角色。
- Rust 则允许一个 package 同时提供“库接口”和“命令行入口”，这一点对工具型项目很方便。
- 想测试和复用都更顺手时，优先把核心逻辑放进库 crate。

**记忆点：**
- `lib.rs` 和 `main.rs` 不是“同一文件的两种模式”，而是两个 crate。
- 入口逻辑放 `main.rs`，业务逻辑放 `lib.rs`。
- `main.rs` 引用库时用包名路径。

## Q3. `mod foo;` 为什么老报 `file not found for module`？ {#q3}
**Tags:** `hot` `mod` `E0583`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 `mod foo;` 不是“导入符号”，而是“把某个文件纳入模块树”，Cargo 会按固定文件名约定去找它。

**解答：** 在某个文件里写 `mod foo;` 后，编译器会去这个文件的同级位置寻找 `foo.rs` 或 `foo/mod.rs`。找不到时就会报 `E0583`。很多人是把 `mod` 和 `use` 的职责弄混了：前者建模块树，后者只是在当前作用域引入路径别名。

```text
// src/main.rs
mod foo;
```

```text
error[E0583]: file not found for module `foo`
= help: to create the module `foo`, create file "src/foo.rs"
        or "src/foo/mod.rs"
```

第二段不是伪代码，而是你真正会在终端里看到的核心报错信息。先补对文件位置，再看导出问题。

**Go 对比：**
- Go 没有 `mod` 这一步，文件放进同一 package 目录就自动参与构建。
- Rust 更显式，因此模块树是“你声明了什么”而不是“目录里恰好有什么”。
- 一看到 `E0583`，先查文件路径和声明位置，不要急着改 `pub`。

**记忆点：**
- `mod` 负责纳入模块树。
- `use` 负责把路径带进当前作用域。
- `E0583` 优先检查文件命名和层级。

## Q4. `use`、`crate::`、`self::`、`super::` 什么时候用？ {#q4}
**Tags:** `common` `use` `path`
**适用版本:** Edition 2018+

**一句话答案：** `crate::` 从当前 crate 根开始，`self::` 从当前模块开始，`super::` 从父模块开始；`use` 只是把这些路径引进当前作用域。

**解答：** 这套路径系统的关键不是死记，而是先判断“我要从哪里出发找这个符号”。绝对路径更稳，尤其是库代码里；相对路径适合局部模块内部短跳转。

```rust
mod outer {
    pub fn hello() -> &'static str {
        "hello"
    }

    pub mod inner {
        use super::hello;

        pub fn call() -> &'static str {
            hello()
        }
    }
}

fn main() {
    println!("{}", outer::inner::call());
}
```

```rust
mod tools {
    pub fn name() -> &'static str {
        "tools"
    }
}

use crate::tools::name;

fn main() {
    println!("{}", name());
}
```

如果你在大型 crate 里频繁改模块位置，优先用 `crate::` 会更不容易被局部重构影响。

**Go 对比：**
- Go 的 import 基本都是包级绝对路径，没有 `super` 这种相对层级引用。
- Rust 模块树更像文件系统，但仍是语言级命名空间，不完全等于磁盘目录。
- 绝对路径心智更稳，相对路径写起来更短，二者各有场景。

**记忆点：**
- 稳定引用优先 `crate::`。
- 父子模块短路径可用 `super::` / `self::`。
- `use` 不改变可见性，只是起别名。

## Q5. `pub`、`pub(crate)`、`pub(super)` 有什么区别？ {#q5}
**Tags:** `common` `visibility`
**适用版本:** Rust 1.18+

**一句话答案：** 它们都在放宽默认私有规则，但放开的边界不同：对所有外部可见、对当前 crate 可见、或只对父模块可见。

**解答：** Rust 默认一切私有，这和 Go 的“大写导出”完全不同。你需要主动决定一个符号要暴露到多远。最实用的经验是：能收窄就收窄，不要一上来全写 `pub`。

```rust
mod service {
    pub fn api() -> &'static str {
        helper()
    }

    pub(crate) fn helper() -> &'static str {
        "ok"
    }
}

fn main() {
    println!("{}", service::api());
    println!("{}", service::helper());
}
```

```rust
mod parent {
    pub mod child {
        pub(super) fn only_parent_can_use() -> &'static str {
            "secret"
        }
    }

    pub fn reveal() -> &'static str {
        child::only_parent_can_use()
    }
}

fn main() {
    println!("{}", parent::reveal());
}
```

如果你把内部 helper 也随手公开，后面就很难安全重构，因为外部代码可能已经依赖上这些实现细节。

**Go 对比：**
- Go 只有包内私有和包外公开两层，规则靠标识符首字母控制。
- Rust 把可见范围做成了语法的一部分，因此能更细粒度地收紧 API 面。
- 大多数内部工具函数在 Rust 里适合 `pub(crate)`，而不是直接 `pub`。

**记忆点：**
- 默认私有，不是默认公开。
- `pub(crate)` 很适合 crate 内部共享实现。
- 公开范围越小，未来越好重构。

## Q6. 为什么写了 `pub fn` 还是“外部看不见”？ {#q6}
**Tags:** `common` `pub`
**适用版本:** Rust 1.0+

**一句话答案：** 因为 Rust 看的是整条路径是否都公开，不是只看最终那个函数有没有 `pub`；外部 crate 尤其进不了非 `pub` 的中间模块。

**解答：** 如果父模块本身是私有的，那么里面就算有 `pub fn`，**外部 crate** 也还是进不去。这个规则经常让 Go 用户困惑，因为 Go 的导出只看名字，不看路径中间层是否“通路打通”。

先看库 crate（`provider`）里的写法：同 crate 内，父模块可以走进私有子模块；但这对外部消费者没有任何帮助。

```rust
// 模拟 provider/src/lib.rs 的可见性关系（同 crate 内演示）
mod private_mod {
    pub fn greet() -> &'static str {
        "hi"
    }
}

pub mod public_mod {
    pub fn greet() -> &'static str {
        "hi"
    }
}

fn main() {
    // 同 crate：父模块能访问 private_mod::greet
    assert_eq!(private_mod::greet(), "hi");
    // 对外真正可依赖的是公开路径
    assert_eq!(public_mod::greet(), "hi");
}
```

换到另一个 crate（`consumer` 依赖 `provider`）时，非 `pub` 路径直接不可见：

```text
// consumer/src/main.rs
fn main() {
    println!("{}", provider::private_mod::greet());
}

error[E0603]: module `private_mod` is private
 --> src/main.rs:2:30
  |
2 |     println!("{}", provider::private_mod::greet());
  |                              ^^^^^^^^^^^  ----- function `greet` is not publicly re-exported
  |                              |
  |                              private module
```

外部 crate 只能走整条都公开的路径。末端写了 `pub fn` 不够；`private_mod` 这扇门没开，外面就进不去。正确写法是只依赖公开导出：

```rust
// 外部 crate 视角：只能调用公开路径（这里用同文件 pub mod 模拟已导出 API）
pub mod public_mod {
    pub fn greet() -> &'static str {
        "hi"
    }
}

fn main() {
    println!("{}", public_mod::greet());
}
```

**Go 对比：**
- Go 只要名字大写且包被 import 到了，基本就能访问。
- Rust 则要求“路径上每一层门都打开”，而且要跨过 crate 边界。
- 一旦外部访问不到，别只盯着末端函数，先沿模块路径逐层检查 `pub`。

**记忆点：**
- `pub` 不是单点开关，要看整条路径。
- 同 crate 可见不等于外部 crate 可见。
- 排查导出问题时，从外到内看路径层级。

## Q7. `pub use` 重导出到底解决了什么问题？ {#q7}
**Tags:** `common` `pub use`
**适用版本:** Rust 1.0+

**一句话答案：** 它能把深层模块里的类型或函数提升到更稳定、更好用的公共入口，而不暴露整棵内部树结构。

**解答：** 这对库设计尤其重要。你可以在内部自由调整模块分层，但对外只承诺一层更短、更稳定的路径。很多成熟 crate 都会在根模块或 `prelude` 里做这样的重导出。

```rust
mod internal {
    pub struct Client {
        pub id: u64,
    }
}

pub use internal::Client;

fn main() {
    let c = Client { id: 1 };
    println!("{}", c.id);
}
```

```rust
mod a {
    pub mod b {
        pub fn ping() -> &'static str {
            "pong"
        }
    }
}

pub use a::b::ping;

fn main() {
    println!("{}", ping());
}
```

如果没有 `pub use`，使用者就必须依赖更深的内部路径，一旦你重构模块布局，外部 API 也会被迫破坏性变更。

**Go 对比：**
- Go 没有语言级重导出；通常是再包一层函数或重新定义类型别名来做 API 整理。
- Rust 的 `pub use` 更直接，特别适合给库提供“短入口”。
- 设计公共 API 时，别让用户被迫记住深层内部模块路径。

**记忆点：**
- `pub use` 用来稳定公共入口。
- 内部结构可深，对外路径最好短。
- 重导出不是多余包装，而是 API 设计工具。

## Q8. 同一个 package 里放多个二进制该怎么组织？ {#q8}
**Tags:** `common` `bin`
**适用版本:** Rust 1.0+

**一句话答案：** 默认二进制放 `src/main.rs`，其他二进制放 `src/bin/*.rs`，共享逻辑优先放进 `src/lib.rs`。

**解答：** 这类布局在“一个库配多个小工具”场景里很好用。例如一个项目既有主 CLI，又有导入器、诊断工具、一次性管理脚本。共享逻辑如果写在各自的 `main.rs` 里，后面会很难测试和复用。

```text
src/
|- lib.rs
|- main.rs
`- bin/
   |- doctor.rs
   `- import_data.rs
```

```bash
cargo run
cargo run --bin doctor
cargo run --bin import_data
```

如果一个工具已经长成独立产品，再考虑拆成 workspace 成员 crate；在那之前，`src/bin` 往往足够清晰。

**Go 对比：**
- Go 里常见做法是 `cmd/app1`、`cmd/app2` 目录下各放一个 `main` 包。
- Rust 的 `src/bin` 很像这个思路，只是共享逻辑更自然地回到 `lib.rs`。
- 命令越多，越要警惕把共享逻辑复制到多个入口文件里。

**记忆点：**
- 单 package 多命令：优先 `src/bin`。
- 共享逻辑放 `lib.rs`。
- 入口只做参数解析和调度最清爽。

## Q9. 什么是 workspace，和普通 package 有什么本质区别？ {#q9}
**Tags:** `common` `workspace`
**适用版本:** Cargo workspace

**一句话答案：** workspace 让多个 package 共用一份依赖解析图和锁文件，适合把大型项目拆成多个相互协作的 crate。

**解答：** 当一个仓库里开始出现“核心库”“CLI”“服务端”“测试工具”这些边界时，workspace 比一个超大 package 更容易维护。它共享 `Cargo.lock` 和 `target/`，并允许统一依赖版本和 metadata。

```toml
[workspace]
members = ["crates/core", "crates/cli"]
resolver = "3"
```

```bash
cargo build --workspace
cargo test -p core
cargo run -p cli
```

workspace 不是模块系统的替代品，而是更高一层的仓库组织手段：crate 之间依然是明确依赖关系，不会因为“在同一个仓库里”就自动互相可见。

**Go 对比：**
- 它和 `go work` 最像的一点是“在一个仓库里协调多个模块/包集合”。
- 但 Cargo workspace 对依赖解析、锁文件、统一命令入口的参与更深。
- 如果你只是想拆文件，用 module；如果你要拆编译边界，用 crate / workspace。

**记忆点：**
- module 是 crate 内部组织。
- workspace 是多 package 协作组织。
- 同仓库不等于自动可见，依赖仍要显式声明。

## Q10. `path`、`git`、crates.io 依赖分别怎么选？ {#q10}
**Tags:** `common` `dependencies`
**适用版本:** Cargo

**一句话答案：** 团队本地协作优先 `path`，临时跟远程仓库提交可用 `git`，正式发布和稳定复用优先 crates.io 版本依赖。

**解答：** 这三种写法分别对应不同成熟度阶段。`path` 最适合同仓库或本地联调；`git` 适合“还没发版但必须引用某个提交”；真正对外发布的库，最好尽量依赖 crates.io 上已经发布的版本。

```toml
[dependencies]
serde = "1"
my_local = { path = "../my_local" }
my_git = { git = "https://github.com/org/repo", rev = "abc1234" }
```

公开发布到 crates.io 时，如果你的库还依赖未发布的本地 path crate，通常会直接卡住发布流程。因此内部联调用 `path` 没问题，但准备发布前要规划好依赖边界。

**Go 对比：**
- Go 依赖更倾向于模块路径加版本，直接引用本地目录的日常感没有 Cargo 这么强。
- Cargo 的 `path` 对 monorepo 联调非常方便，但也更容易让人忘记发布边界。
- `git` 依赖不是长期解法，通常只是过渡状态。

**记忆点：**
- 联调用 `path`，过渡用 `git`，稳定复用用 crates.io。
- 发布前检查是否仍残留 path 依赖。
- 依赖来源会影响可复现性和发布流程。

## Q11. Cargo feature 是模块系统的一部分吗？ {#q11}
**Tags:** `common` `features`
**适用版本:** Cargo features

**一句话答案：** 不是。feature 是构建期开关，用来控制依赖和条件编译；module 是命名空间，它们解决的问题完全不同。

**解答：** 很多人第一次接触 feature 时，会把它想成“按需加载模块”。更准确的说法是：feature 决定某段代码在这次构建里要不要参与编译，而 module 决定这些代码在 crate 里如何命名和暴露。

```toml
[features]
default = ["std"]
std = []
serde = ["dep:serde"]

[dependencies]
serde = { version = "1", optional = true, features = ["derive"] }
```

```rust
#[cfg(feature = "serde")]
fn encode() -> &'static str {
    "serde enabled"
}

#[cfg(not(feature = "serde"))]
fn encode() -> &'static str {
    "serde disabled"
}

fn main() {
    println!("{}", encode());
}
```

feature 设计应尽量“只加不减”，因为 Cargo 会对同一依赖做 feature 并集统一，不能指望不同下游把它编译成两份互斥版本。

**Go 对比：**
- Go 的 build tags 更像 feature 的一部分用途，但没有 Cargo 这种依赖图级别的统一机制。
- Rust feature 会影响依赖解析和 `cfg` 条件编译，参与范围更大。
- 需要组织命名空间时别找 feature；那是 module 的工作。

**记忆点：**
- feature 管“编不编进来”。
- module 管“编进来以后怎么组织”。
- 不要把两者混成一个概念。

## Q12. `resolver = "2"` 和 `resolver = "3"` 需要知道到什么程度？ {#q12}
**Tags:** `common` `resolver`
**适用版本:** resolver 2 自 Rust/Cargo 1.51+；resolver 3 自 1.84+

**一句话答案：** 日常使用只需记住：新 workspace 尤其是 Edition 2024 项目优先用 `resolver = "3"`，它在现代依赖解析和 `rust-version` 兼容性上更合理。

**解答：** resolver 影响 Cargo 如何在整个依赖图里统一 features、选择兼容版本。对大多数业务代码来说，不必把实现细节背成面试题，但至少要知道它是 workspace 级设置，不能随便在子 crate 各写各的。

```toml
[workspace]
members = ["crates/*"]
resolver = "3"
```

如果你的项目还是旧 workspace，先确认团队工具链版本，再决定是否升级。升级 resolver 通常比升级 edition 风险小，但仍建议放进 CI 验证，而不是拍脑袋改。

**Go 对比：**
- Go 工具链里没有一个和 Cargo resolver 一一对应的日常显式旋钮。
- 这也是 Cargo 比 Go 暴露更多“依赖图控制面”的体现。
- 你不用天天改它，但知道它存在，能少踩很多 workspace 怪坑。

**记忆点：**
- resolver 是 workspace 级配置。
- 新项目优先 `resolver = "3"`。
- 版本升级前先看团队工具链和 CI。

## Q13. Rust module 和 Go package 为什么老对不上号？ {#q13}
**Tags:** `hot` `module` `package`
**适用版本:** Rust 1.0+

**一句话答案：** Go 的 package 大致等于“一个目录里的编译命名空间”；Rust 把工程拆成 package（Cargo）、crate（编译单元）、module（命名空间）三层，拿 Go 的“目录=包”去套会处处错位。

**解答：** 对不上号通常不是语法记错，而是映射错了层级。Go 里你说“这个 package”，往往同时指目录、导入路径和可见性边界；Rust 里这三件事被拆开了。

```text
Go 习惯映射（容易错）：
  一个目录          ≈  一个 package
  首字母大写        ≈  导出

Rust 实际分层：
  Cargo.toml        →  package（工程/依赖单位）
  lib.rs / main.rs  →  crate root（编译单位）
  mod / 文件树      →  module（命名空间 + 可见性）
```

结果是：同目录多个文件不会自动进同一个模块；`pub` 也不等于“只要大写就全仓库可见”。你要先问“这是哪个 crate 的模块树”，再问“路径上每一层有没有 `pub`”。

**Go 对比：**
- Go：目录进 package，导入路径几乎就是目录约定。
- Rust：文件进模块树靠 `mod` 声明；导入路径是模块路径，不是单纯文件夹名。
- 用 Go 心智读 Rust，最常见症状是“文件放对了却找不到符号 / 外部看不见”。

**记忆点：**
- 别把 Go package 一对一翻译成 Rust module。
- 先分清 package / crate / module。
- 可见性看模块路径上的 `pub`，不看文件名大小写。

## Q14. 到底用 `foo.rs` 还是 `foo/mod.rs`？ {#q14}
**Tags:** `common` `mod.rs`
**适用版本:** Rust 1.0+；子模块文件布局自 Edition 2018 更灵活

**一句话答案：** 模块只有自己、没有子模块时用 `foo.rs`；需要 `foo/bar.rs` 这类子树时，用 `foo.rs` + `foo/` 目录，或传统的 `foo/mod.rs`，二者等价，团队选一种即可。

**解答：** `mod foo;` 会找 `foo.rs` 或 `foo/mod.rs`，二选一，不要同时存在。现代风格更推荐“父模块用 `foo.rs`，子模块文件放进 `foo/`”，避免深层全是 `mod.rs` 不好搜索。

```text
# 无子模块
src/
|- main.rs      # mod net;
`- net.rs

# 有子模块（推荐）
src/
|- main.rs      # mod net;
|- net.rs       # mod tcp; mod udp;
`- net/
   |- tcp.rs
   `- udp.rs

# 有子模块（传统）
src/
|- main.rs
`- net/
   |- mod.rs    # 内容相当于上面的 net.rs
   |- tcp.rs
   `- udp.rs
```

有子模块时不要只建 `net/` 却漏掉 `net.rs`/`net/mod.rs`：父模块文件才是 `mod net;` 的落点。

**Go 对比：**
- Go 没有“父文件声明子文件”这一步，同目录 `.go` 文件自动同包。
- Rust 必须显式 `mod`，所以才有 `foo.rs` vs `foo/mod.rs` 的选择。
- 选哪种布局不影响语义，影响的是可读性和文件搜索体验。

**记忆点：**
- `foo.rs` 与 `foo/mod.rs` 互斥，语义相同。
- 有子树时优先 `foo.rs` + `foo/`。
- 先保证父模块文件存在，再谈子模块。

## Q15. 为什么写了 `mod` 还要再 `use`？ {#q15}
**Tags:** `hot` `mod` `use`
**适用版本:** Edition 2018+

**一句话答案：** `mod` 把文件挂进模块树；`use` 只是在当前作用域给已有路径起短名。前者建树，后者省字，职责不同。

**解答：** 很多人把 `mod` 当成 Go 的 `import`。其实 `mod foo;` 之后，符号已经在 `foo::...`（或 `crate::foo::...`）下可用了；再写 `use` 只是为了少敲前缀，或者把深层路径提到当前作用域。

```rust
mod math {
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }
}

// 可以不用 use，直接完整路径调用
fn with_path() -> i32 {
    math::add(1, 2)
}

use math::add;

fn with_use() -> i32 {
    add(3, 4)
}

fn main() {
    assert_eq!(with_path(), 3);
    assert_eq!(with_use(), 7);
}
```

反过来：只写 `use crate::math::add;` 却从没 `mod math;`（或从未在祖先模块声明），树里根本没有这个节点，`use` 也会失败。外部依赖同理——`use serde::Serialize;` 之前要先在 `Cargo.toml` 声明依赖，那是 crate 级引入，不是 `mod`。

**Go 对比：**
- Go 的 `import` 同时完成“依赖这个包”和“把名字引进来”。
- Rust 拆成：依赖进 `Cargo.toml`，本 crate 文件进 `mod`，短名再 `use`。
- 记口诀：`mod` 建树，`use` 取别名。

**记忆点：**
- `mod` ≠ `import`。
- 没 `mod`（或没依赖）就没有可 `use` 的路径。
- `use` 可省略，只是写法更啰嗦。

## Q16. `lib` + 多个 `bin` 的目录怎么摆？ {#q16}
**Tags:** `common` `lib` `bin`
**适用版本:** Rust 1.0+

**一句话答案：** 共享逻辑放 `src/lib.rs`，默认入口放 `src/main.rs`，其余命令放 `src/bin/*.rs`；各 binary 通过 package 名调用 library，而不是互相 `mod` 抄代码。

**解答：** 这是单 package 多命令的标准骨架。和“只有多个 bin、没有 lib”相比，多一个 `lib.rs` 的好处是：业务逻辑可单测、可被多个入口复用，bin 文件只保留参数解析和进程边界。

```text
my_tools/
|- Cargo.toml          # name = "my_tools"
`- src/
   |- lib.rs           # pub fn run_job() { ... }
   |- main.rs          # 默认 bin：调用 my_tools::...
   `- bin/
      |- doctor.rs
      `- import_data.rs
```

```text
// src/bin/doctor.rs（示意；需在真实 package 中编译）
fn main() {
    if let Err(e) = my_tools::run_job("doctor") {
        eprintln!("{e}");
        std::process::exit(1);
    }
}
```

```bash
cargo run                  # src/main.rs
cargo run --bin doctor
cargo test                 # 主要测 lib
```

只有当某个 bin 路径/名字特殊时，才在 `Cargo.toml` 里写 `[[bin]]`；常规 `src/bin/*.rs` 不必手写。命令长成独立产品后再拆 workspace。

**Go 对比：**
- 对应 Go 的 `pkg/` 或内部库 + `cmd/app1`、`cmd/app2`。
- Rust 默认约定更死：`lib.rs` / `main.rs` / `bin/` 路径即约定。
- 共享代码进 lib，是避免多个 `main` 互相复制的关键。

**记忆点：**
- lib 承载逻辑，bin 承载入口。
- 其他命令默认丢进 `src/bin/`。
- binary 用 package 名引用 library API。

## Q17. 结构体字段的 `pub` 和模块的 `pub` 怎么配合？ {#q17}
**Tags:** `hot` `pub` `struct` `visibility`
**适用版本:** Rust 1.0+

**一句话答案：** 路径上每一层模块都要 `pub`，类型本身要 `pub`，字段还要单独标 `pub` 才能从外部读写；缺任何一环，外部都只能看见“有这个类型”或干脆看不见。

**解答：** 可见性是**逐项、逐层**的。`pub struct User` 只表示类型名可被路径指到；字段默认仍私有，外部不能写 `user.id`，通常要通过构造函数或方法访问。模块若未 `pub`，外面连这条路径都走不通（见 [Q6](#q6)）。

```rust
mod domain {
    pub struct User {
        pub name: String, // 字段公开：外部可读可写
        id: u64,          // 字段私有：外部碰不到
    }

    impl User {
        pub fn new(name: String, id: u64) -> Self {
            Self { name, id }
        }

        pub fn id(&self) -> u64 {
            self.id
        }
    }
}

fn main() {
    let mut user = domain::User::new(String::from("Ada"), 7);
    user.name.push_str(" Lovelace");
    assert_eq!(user.id(), 7);
    // user.id; // 编译失败：id 是私有字段
}
```

```rust
mod api {
    mod internal {
        pub struct Token(pub String); // 元组结构体：元素也要 pub 才能从外部解构/读取
    }

    // 模块 internal 非 pub，外部不能写 api::internal::Token
    // 用 pub use 把类型提到 api 边界（见 [Q7](#q7)）
    pub use internal::Token;

    pub fn issue() -> Token {
        Token(String::from("secret"))
    }
}

fn main() {
    let token = api::issue();
    assert_eq!(token.0, "secret");
}
```

常见组合：
- **类型 pub + 字段全私有**：最稳的封装，只暴露方法。
- **类型 pub + 部分字段 pub**：DTO / 纯数据配置很常见。
- **模块不 pub + 类型 pub**：只给父模块用，再由父模块 `pub use` 精选导出。

**Go 对比：**
- Go 靠字段名首字母大小写控制导出，和文件所在 package 绑定。
- Rust 把“模块路径是否公开”和“字段是否公开”拆成两套开关。
- Go 程序员常漏掉“字段还要再写一次 `pub`”，结果类型能提到、字段全红。

**记忆点：**
- 模块路径、类型、字段，三层各自要 `pub`。
- 默认字段私有，不等于类型私有。
- 对外 API 优先“类型公开、字段私有”。

## Q18. 为什么单元测试能测 private，集成测试不能？ {#q18}
**Tags:** `hot` `unit-test` `integration-test` `privacy`
**适用版本:** Rust 1.0+

**一句话答案：** 单元测试编译进**同一个 crate**，和被测代码共享私有可见性；`tests/` 下的集成测试是**另一个 crate**，只能走你的公共 API。

**解答：** 写在 `src/` 里、通常包在 `#[cfg(test)] mod tests` 中的测试，是当前 crate 的子模块，因此 `use super::*` 后能调用私有函数、读私有字段。`tests/foo.rs` 则像外部用户：`use my_crate::...`，看不见非 `pub` 项。这和“测没测到”无关，是**编译单元边界**决定的。

```rust
// 示意：同一文件内的单元测试可碰私有项
fn helper_sum(a: i32, b: i32) -> i32 {
    a + b
}

pub fn add(a: i32, b: i32) -> i32 {
    helper_sum(a, b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn private_helper_is_visible() {
        assert_eq!(helper_sum(2, 3), 5);
    }
}

fn main() {
    assert_eq!(add(2, 3), 5);
}
```

```text
my_lib/
|- Cargo.toml          # name = "my_lib"
|- src/lib.rs          # pub fn add；fn helper_sum 私有
`- tests/
   `- api.rs           # 独立 crate：只能 my_lib::add，不能 my_lib::helper_sum
```

```rust
// 签名示意，非完整程序（集成测试 crate）
// use my_lib::add;
// #[test]
// fn public_api_works() {
//     assert_eq!(add(2, 3), 5);
// }
// // use my_lib::helper_sum; // 错误：私有项对外部 crate 不可见
```

实践上：内部算法、不变量用单元测试白盒覆盖；对外契约、示例用法用集成测试黑盒锁住。想测“半内部”API，用 `pub(crate)` 并在同 crate 单测，而不是为了测试强行 `pub`。

**Go 对比：**
- Go 的 `_test.go` 同 package 可测未导出符号；`package foo_test` 则只能测导出 API。
- Rust 的单元/集成测试大致对应这两种模式，但集成测试目录约定更死。
- 两边都成立：测试便利不能压过 API 边界设计。

**记忆点：**
- 同 crate → 能测 private。
- `tests/` → 外部 crate，只能 pub。
- 别为了测试把内部细节全部公开。

## Q19. `#[cfg(test)]` 模块该怎么组织？ {#q19}
**Tags:** `common` `cfg(test)` `tests`
**适用版本:** Rust 1.0+

**一句话答案：** 默认在被测模块文件末尾放 `#[cfg(test)] mod tests { use super::*; ... }`；测试辅助代码也加 `#[cfg(test)]`，需要跨文件共享时再拆 `#[cfg(test)] mod test_support;`。

**解答：** **`#[cfg(test)]`**（configuration attribute，配置属性）保证这些模块只在 `cargo test` 时编译，正式 `cargo build` 不会带上断言和测试夹具。组织原则：测试离被测代码近、辅助代码不要泄漏进发布构建、避免和 `tests/` 集成测试目录搞混。

```rust
pub fn normalize(name: &str) -> String {
    name.trim().to_lowercase()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn trims_and_lowercases() {
        assert_eq!(normalize("  Ada  "), "ada");
    }
}

fn main() {
    assert_eq!(normalize(" X "), "x");
}
```

```rust
// 同一模块树里拆测试辅助：辅助模块本身也要 cfg(test)
pub fn max_len(items: &[&str]) -> usize {
    items.iter().map(|s| s.len()).max().unwrap_or(0)
}

#[cfg(test)]
mod fixtures {
    pub fn sample_names() -> Vec<&'static str> {
        vec!["a", "bb", "ccc"]
    }
}

#[cfg(test)]
mod tests {
    use super::{fixtures, max_len};

    #[test]
    fn uses_shared_fixture() {
        assert_eq!(max_len(&fixtures::sample_names()), 3);
    }
}

fn main() {
    assert_eq!(max_len(&["hi"]), 2);
}
```

多文件时常见摆法：`src/lib.rs` 写 `#[cfg(test)] mod tests;` 并配 `src/tests.rs`（注意这是**源码树内**测试子模块，不是根目录 `tests/`）。根目录 `tests/*.rs` 专留给跨 crate 集成测试（见 [Q18](#q18)）。

**Go 对比：**
- 近似 `foo_test.go` 与同包辅助函数；Rust 用属性把测试代码从正式构建剔除得更干净。
- Go 没有“源码旁 cfg 模块 / 根目录 tests 集成箱”这套双轨目录约定。
- 共享测试夹具时两边都要避免污染生产包。

**记忆点：**
- 文件末尾：`#[cfg(test)] mod tests`。
- 辅助模块同样要 `cfg(test)`。
- `src` 内单测 ≠ 根目录 `tests/` 集成测。

## Q20. 模块互相 `use` 不上、像循环依赖时怎么改？ {#q20}
**Tags:** `hot` `use` `module` `cycle`
**适用版本:** Rust 1.0+

**一句话答案：** Rust 允许模块树里互相引用路径，但“类型/函数定义形成环”时要拆：把共享定义抽到第三模块，或让依赖单向流动（父用子、子通过参数/回调回传），不要两个子模块彼此硬耦。

**解答：** 报错常见形态是：`a` 里 `use crate::b::...`，`b` 里又 `use crate::a::...`，再在类型字段或默认实现里真正咬死对方，编译器就会在类型检查阶段抱怨。`use` 本身不是 Go 那种 package import cycle 的同款规则，但**逻辑环**一样难维护。改法优先“抽出共享层”。

```rust
// ✅ 抽出共享类型，打断 a <-> b 环
mod types {
    pub struct UserId(pub u64);
}

mod auth {
    use crate::types::UserId;

    pub fn current_user() -> UserId {
        UserId(1)
    }
}

mod billing {
    use crate::types::UserId;

    pub fn invoice_owner() -> UserId {
        UserId(1)
    }
}

fn main() {
    assert_eq!(auth::current_user().0, billing::invoice_owner().0);
}
```

```rust
// ✅ 依赖单向：policy 依赖 store；store 不反向 use policy
mod store {
    pub fn load_limit() -> u32 {
        10
    }
}

mod policy {
    use crate::store;

    pub fn allow(count: u32) -> bool {
        count <= store::load_limit()
    }
}

fn main() {
    assert!(policy::allow(3));
    assert!(!policy::allow(99));
}
```

若必须“子模块回调父逻辑”，用函数参数/`Fn` 闭包注入，或把编排放在父模块，而不是让子模块 `use super::brother`。也可合并成一个模块再 `pub use` 拆路径（见 [Q7](#q7)），避免为了目录好看切出真环。

**Go 对比：**
- Go 直接禁止 import cycle，编译器硬拒绝。
- Rust 更常见是类型层环或设计上的环；解法同样是抽 `types`/`common`、倒转依赖。
- 两边都成立：共享定义上移，业务依赖单向。

**记忆点：**
- 共享类型抽到第三模块。
- 依赖单向，编排放父层。
- 目录拆分服从依赖方向，不要反过来。
