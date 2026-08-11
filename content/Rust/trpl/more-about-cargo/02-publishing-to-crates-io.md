+++
title = "14.2 将 Crate 发布到 Crates.io"
date = 2026-08-05T08:44:00+08:00
weight = 63
type = "docs"
description = "编写文档注释、设计公开 API、配置元数据并将 crate 发布到 crates.io"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 将 Crate 发布到 Crates.io {#crate-crates-io}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch14-02-publishing-to-crates-io.html](https://doc.rust-lang.org/stable/book/ch14-02-publishing-to-crates-io.html)


## 将 Crate 发布到 Crates.io

　　我们一直把 [crates.io](https://crates.io/) 上的包当作项目依赖来用，其实也可以通过发布自己的包，把代码分享给别人。[crates.io](https://crates.io/) 上的 crate 注册表会分发你的包的源码，因此它主要托管开源代码。

　　Rust 和 Cargo 提供了一些特性，让已发布的包更容易被发现和使用。接下来我们先看其中几项，再说明如何发布包。

### 编写有用的文档注释

　　准确记录你的包，能帮助其他用户知道何时、如何使用它们，因此值得花时间写文档。第 3 章讨论过用两个斜杠 `//` 为 Rust 代码写注释。Rust 还有一类专门用于文档的注释，恰如其名叫做*文档注释*（documentation comment），可以生成 HTML 文档。这些 HTML 展示的是公开 API 项的文档注释内容，面向想了解如何*使用*你的 crate 的程序员，而不是关心 crate 如何*实现*的人。

　　文档注释使用三个斜杠 `///`（而不是两个），并支持用 Markdown 格式化文本。把文档注释放在它所说明的项的正上方。示例 14-1 展示了名为 `my_crate` 的 crate 中，为 `add_one` 函数编写的文档注释。

**文件名：`src/lib.rs`**
```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

**示例 14-1：函数的文档注释**

　　这里我们描述了 `add_one` 函数的作用，用标题 `Examples` 开了一个小节，并给出演示如何使用 `add_one` 的代码。运行 `cargo doc` 即可从这些文档注释生成 HTML 文档。该命令会调用随 Rust 分发的 `rustdoc` 工具，并把生成的 HTML 放在 *target/doc* 目录中。

　　为了方便，运行 `cargo doc --open` 会为当前 crate（以及它的所有依赖）构建 HTML 文档，并在浏览器中打开结果。导航到 `add_one` 函数，就能看到文档注释中的文本如何被渲染，如图 14-1 所示。

<img alt="`my_crate` 的 `add_one` 函数渲染后的 HTML 文档" src="img/trpl14-01.png" class="center" />

<span class="caption">图 14-1：`add_one` 函数的 HTML 文档</span>

#### 常用小节

　　我们在示例 14-1 里用了 Markdown 标题 `# Examples`，从而在 HTML 中生成标题为 “Examples” 的小节。crate 作者在文档中还常用这些小节：

- **Panics**：说明被文档化的函数在哪些情形下可能 panic。不想让程序 panic 的调用者，应确保不要在这些情形下调用该函数。
- **Errors**：若函数返回 `Result`，描述可能出现的错误种类以及何种条件会触发这些错误，有助于调用者针对不同错误编写不同的处理逻辑。
- **Safety**：若调用该函数是 `unsafe` 的（我们在第 20 章讨论不安全），应有一节解释为何不安全，并写明函数期望调用者维护的不变量。

　　多数文档注释并不需要这些小节全都写上，但这份清单能提醒你：用户通常关心代码的哪些方面。

#### 把文档注释当作测试 {#documentation-comments-as-tests}

　　在文档注释里加入示例代码块，既能演示如何使用库，还有额外好处：运行 `cargo test` 时，文档中的代码示例会作为测试执行！有示例的文档最好不过；但若代码已变、示例却失效，那也糟糕不过。若对示例 14-1 中 `add_one` 的文档运行 `cargo test`，测试结果里会出现类似这样的一节：


```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

　　现在，若改动函数或示例，使得示例中的 `assert_eq!` 发生 panic，再运行 `cargo test`，文档测试就会发现示例与代码已经不同步！

#### 为包含项添加注释

　　`//!` 这种文档注释样式，是给*包含*这些注释的项添加文档，而不是给注释*后面*的项。我们通常在 crate 根文件（按约定是 *src/lib.rs*）或模块内部使用这类注释，为整个 crate 或模块写文档。

　　例如，要为包含 `add_one` 函数的 `my_crate` crate 添加说明其用途的文档，可以在 *src/lib.rs* 文件开头加入以 `//!` 开头的文档注释，如示例 14-2 所示。

**文件名：`src/lib.rs`**
```rust
//! # My Crate
//!
//! `my_crate` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
// --snip--
```

**示例 14-2：`my_crate` crate 整体的文档**

　　注意：最后一行以 `//!` 开头的注释后面没有任何代码。因为注释以 `//!` 而不是 `///` 开头，我们是在为包含这条注释的项写文档，而不是为它后面的项。这里这个项就是 *src/lib.rs* 文件，也就是 crate 根。这些注释描述的是整个 crate。

　　运行 `cargo doc --open` 时，这些注释会出现在 `my_crate` 文档首页、公开项列表的上方，如图 14-2 所示。

　　项内部的文档注释特别适合描述 crate 和模块。用它们说明“容器”的整体用途，能帮助用户理解 crate 的组织结构。

<img alt="包含 crate 整体注释的渲染后 HTML 文档" src="img/trpl14-02.png" class="center" />

<span class="caption">图 14-2：`my_crate` 渲染后的文档，含描述整个 crate 的注释</span>

### 导出便于使用的公开 API {#exporting-a-convenient-public-api}

　　发布 crate 时，公开 API 的结构是重要考量。使用你 crate 的人对结构不如你熟悉；若模块层级很深，他们可能很难找到想用的部分。

　　第 7 章讲过如何用 `pub` 关键字把项设为公开，以及如何用 `use` 关键字把项引入作用域。不过，开发时对你合理的结构，对用户未必方便。你可能希望把结构体组织成多层层级，但想使用深层类型的人可能很难发现该类型存在，也会对不得不写 `use my_crate::some_module::another_module::UsefulType;` 而不是 `use my_crate::UsefulType;` 感到烦恼。

　　好消息是：即便内部结构对其他库的用户不够方便，你也不必重排内部组织——可以用 `pub use` 重新导出项，使公开结构与私有结构不同。*重新导出*（re-exporting）会把某一位置的公开项，在另一位置也变成公开的，就好像它是在另一位置定义的一样。

　　例如，假设我们做了一个名为 `art` 的库，用来建模艺术相关概念。库里有两个模块：`kinds` 模块包含名为 `PrimaryColor` 与 `SecondaryColor` 的两个枚举，`utils` 模块包含名为 `mix` 的函数，如示例 14-3 所示。

**文件名：`src/lib.rs`**
```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub mod kinds {
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        // --snip--

    }
}
```

**示例 14-3：把项组织在 `kinds` 与 `utils` 模块中的 `art` 库**

　　图 14-3 展示了用 `cargo doc` 为这个 crate 生成的文档首页大致样子。

<img alt="`art` crate 渲染后的文档，列出 `kinds` 与 `utils` 模块" src="img/trpl14-03.png" class="center" />

<span class="caption">图 14-3：`art` 文档首页，列出了 `kinds` 与 `utils` 模块</span>

　　注意：`PrimaryColor` 与 `SecondaryColor` 类型并未出现在首页，`mix` 函数也没有。我们得点击 `kinds` 和 `utils` 才能看到它们。

　　依赖这个库的另一个 crate，需要用体现当前模块结构的 `use` 语句，把 `art` 中的项引入作用域。示例 14-4 展示了一个使用 `art` crate 中 `PrimaryColor` 与 `mix` 的 crate。

**文件名：`src/main.rs`**
```rust
use art::kinds::PrimaryColor;
use art::utils::mix;

fn main() {
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

**示例 14-4：使用导出了内部结构的 `art` crate 中各项的 crate**

　　编写示例 14-4 这类使用 `art` crate 的代码的人，必须搞清楚 `PrimaryColor` 在 `kinds` 模块、`mix` 在 `utils` 模块。`art` crate 的模块结构对维护它的开发者更有意义，对使用者则不然。内部结构对想学会如何使用 `art` 的人并无多少有用信息，反而造成困扰：使用者得弄清该看哪里，还要在 `use` 语句里写出模块名。

　　要从公开 API 中抹去内部组织，可以修改示例 14-3 中的 `art` crate 代码，加入 `pub use` 语句，在顶层重新导出这些项，如示例 14-5 所示。

**文件名：`src/lib.rs`**
```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor;
pub use self::kinds::SecondaryColor;
pub use self::utils::mix;

pub mod kinds {
    // --snip--

}

pub mod utils {
    // --snip--

}
```

**示例 14-5：添加 `pub use` 语句以重新导出项**

　　现在 `cargo doc` 为该 crate 生成的 API 文档会在首页列出并链接重新导出的项，如图 14-4 所示，从而更容易找到 `PrimaryColor`、`SecondaryColor` 类型以及 `mix` 函数。

<img alt="`art` crate 渲染后的文档，首页含重新导出的项" src="img/trpl14-04.png" class="center" />

<span class="caption">图 14-4：`art` 文档首页，列出了重新导出的项</span>

　　`art` crate 的用户仍可像示例 14-4 那样看到并使用示例 14-3 中的内部结构，也可以使用示例 14-5 中更方便的结构，如示例 14-6 所示。

**文件名：`src/main.rs`**
```rust
use art::PrimaryColor;
use art::mix;

fn main() {
    // --snip--

}
```

**示例 14-6：使用从 `art` crate 重新导出的项的程序**

　　当嵌套模块很多时，用 `pub use` 在顶层重新导出类型，能显著改善使用者体验。`pub use` 的另一个常见用途，是把依赖中的定义重新导出到当前 crate，使那些定义成为你 crate 公开 API 的一部分。

　　设计好用的公开 API 结构，更像艺术而非科学；你可以迭代，找到最适合用户的 API。选择 `pub use` 能让你灵活安排内部结构，并把它与呈现给用户的外观解耦。不妨看看你安装过的一些 crate 的源码，它们的内部结构是否与公开 API 不同。

### 注册 Crates.io 账户

　　发布任何 crate 之前，需要先在 [crates.io](https://crates.io/) 创建账户并取得 API 令牌。访问 [crates.io](https://crates.io/) 首页，用 GitHub 账户登录即可。（目前需要 GitHub 账户，将来站点可能会支持其他注册方式。）登录后，打开账户设置页 [https://crates.io/me/](https://crates.io/me/) 获取 API 密钥。然后运行 `cargo login`，按提示粘贴 API 密钥，例如：

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

　　该命令会把你的 API 令牌告知 Cargo，并保存在本地的 *~/.cargo/credentials.toml*。注意：这个令牌是机密，不要与任何人分享。若因任何原因已经分享出去，应立即在 [crates.io](https://crates.io/) 上吊销并生成新令牌。

### 为新 Crate 添加元数据

　　假设你有一个想发布的 crate。发布前，需要在该 crate 的 *Cargo.toml* 的 `[package]` 小节中加入一些元数据。

　　你的 crate 需要一个唯一名称。本地开发时，名字可以随意起。但 [crates.io](https://crates.io/) 上的 crate 名称按先到先得分配：名字一旦被占用，别人就不能再发布同名 crate。尝试发布前，先搜索你想用的名字。若已被占用，就得另找名字，并编辑 *Cargo.toml* 中 `[package]` 小节的 `name` 字段，以便用新名字发布，例如：

<span class="filename">文件名：Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

　　即便选了唯一名称，此时若运行 `cargo publish` 发布，也会先看到警告，再看到错误：


```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

　　报错是因为缺少关键信息：必须提供描述与许可证，别人才能知道你的 crate 做什么、在何种条款下可以使用。在 *Cargo.toml* 中加入一两句描述即可，因为它会出现在搜索结果里。对于 `license` 字段，需要给出一个*许可证标识符*（license identifier value）。[Linux 基金会的 Software Package Data Exchange（SPDX）][spdx] 列出了可用的标识符。例如，要声明你的 crate 使用 MIT 许可证，就加入 `MIT` 标识符：

<span class="filename">文件名：Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

　　若想使用不在 SPDX 中的许可证，需要把许可证全文放进一个文件、纳入项目，然后用 `license-file` 指定该文件名，而不是使用 `license` 键。

　　选择何种许可证适合你的项目，超出了本书范围。Rust 社区很多人像 Rust 一样采用双重许可 `MIT OR Apache-2.0`。这也能说明：可以用 `OR` 分隔多个许可证标识符，为项目指定多种许可证。

　　有了唯一名称、版本、描述和许可证后，一个准备发布的项目的 *Cargo.toml* 可能类似这样：

<span class="filename">文件名：Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

　　[Cargo 文档](https://doc.rust-lang.org/cargo/) 还介绍了其他可指定的元数据，便于别人更容易发现和使用你的 crate。

### 发布到 Crates.io

　　创建了账户、保存了 API 令牌、选定了 crate 名称并填写了必要元数据后，就可以发布了！发布 crate 会把某个具体版本上传到 [crates.io](https://crates.io/)，供他人使用。

　　务必谨慎：发布是*永久*的。版本永远不能被覆盖，代码除特定情形外也不能删除。Crates.io 的一大目标是充当代码的永久归档，使所有依赖 [crates.io](https://crates.io/) 上 crate 的项目构建都能继续工作。若允许删除版本，这个目标就无法实现。不过，你可以发布的 crate 版本数量没有限制。

　　再次运行 `cargo publish`，现在应当能成功：


```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

　　恭喜！你已经把代码分享给了 Rust 社区，任何人都可以轻松把你的 crate 加为自己项目的依赖。

### 发布已有 Crate 的新版本

　　当你修改了 crate 并准备发布新版本时，更改 *Cargo.toml* 中指定的 `version` 值，再重新发布。根据改动的类型，按 [语义化版本规则][semver] 决定合适的下一版本号。然后运行 `cargo publish` 上传新版本。

### 从 Crates.io 弃用版本

　　虽然不能删除 crate 的旧版本，但可以阻止未来的新项目把它们加为依赖。当某个版本因故损坏时，这很有用。在这种情形下，Cargo 支持 yank（撤回）某个 crate 版本。

　　*Yank* 某个版本后，新项目不能再依赖该版本，但所有已经依赖它的既有项目可以继续使用。本质上，yank 意味着带有 *Cargo.lock* 的项目不会因此损坏，而将来新生成的 *Cargo.lock* 不会再选用被 yank 的版本。

　　要 yank 某个已发布 crate 的版本，在该 crate 的目录中运行 `cargo yank` 并指定版本。例如，若我们发布过名为 `guessing_game` 的 1.0.1 版本并想 yank 它，就在 `guessing_game` 的项目目录中运行：


```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

　　在命令中加上 `--undo`，还可以撤销 yank，再次允许项目依赖该版本：

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

　　Yank *不会*删除任何代码。例如，它无法删除不小心上传的机密信息。若发生这种情况，必须立即重置那些机密。

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/
