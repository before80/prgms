+++
title = "7.4 用 use 关键字导入路径"
date = 2026-08-05T08:44:00+08:00
weight = 31
type = "docs"
description = "用 use、as、pub use 与嵌套路径简化作用域内的路径引用"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 use 关键字导入路径 {#use}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html](https://doc.rust-lang.org/stable/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html)


## 用 `use` 关键字导入路径

　　每次调用函数都把路径写全，会显得既麻烦又重复。在示例 7-7 中，无论我们选择绝对路径还是相对路径去调用 `add_to_waitlist`，每次调用时都还得写出 `front_of_house` 和 `hosting`。幸好有办法简化：可以用 `use` 关键字导入路径，然后在该作用域的其他地方使用更短的名字。

　　在示例 7-11 中，我们把 `crate::front_of_house::hosting` 模块导入 `eat_at_restaurant` 函数的作用域，这样在 `eat_at_restaurant` 里只需写 `hosting::add_to_waitlist` 即可调用 `add_to_waitlist`。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

**示例 7-11：用 `use` 导入模块**

　　在作用域中添加 `use` 和一条路径，类似于在文件系统中创建符号链接。在 crate 根添加 `use crate::front_of_house::hosting` 后，`hosting` 就成为该作用域中的有效名字，就好像 `hosting` 模块是在 crate 根定义的一样。用 `use` 导入的路径也会像其他路径一样检查私有性。

　　注意，`use` 只在它出现的那个特定作用域内生效。示例 7-12 把 `eat_at_restaurant` 函数移进了名为 `customer` 的新子模块，那是与 `use` 语句不同的作用域，因此函数体无法编译。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;

mod customer {
    pub fn eat_at_restaurant() {
        hosting::add_to_waitlist();
    }
}
```

**示例 7-12：`use` 语句只在它所在的作用域内生效。**

　　编译器错误显示，该导入在 `customer` 模块内不再可用：

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0433]: cannot find module or crate `hosting` in this scope
  --> src/lib.rs:11:9
   |
11 |         hosting::add_to_waitlist();
   |         ^^^^^^^ use of unresolved module or unlinked crate `hosting`
   |
   = help: if you wanted to use a crate named `hosting`, use `cargo add hosting` to add it to your `Cargo.toml`
help: consider importing this module through its public re-export
   |
10 +     use crate::hosting;
   |

warning: unused import: `crate::front_of_house::hosting`
 --> src/lib.rs:7:5
  |
7 | use crate::front_of_house::hosting;
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

For more information about this error, try `rustc --explain E0433`.
warning: `restaurant` (lib) generated 1 warning
error: could not compile `restaurant` (lib) due to 1 previous error; 1 warning emitted
```

　　注意还有一条警告：`use` 在其所在作用域中已不再被使用！要解决这个问题，可以把 `use` 也移进 `customer` 模块，或者在子模块 `customer` 中用 `super::hosting` 引用父模块中的导入。

### 编写符合习惯的 `use` 路径 {#creating-idiomatic-use-paths}

　　在示例 7-11 中，你可能想过：为什么我们指定 `use crate::front_of_house::hosting`，然后在 `eat_at_restaurant` 里调用 `hosting::add_to_waitlist`，而不是像示例 7-13 那样把 `use` 路径一直写到 `add_to_waitlist` 函数，以达到同样效果？

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting::add_to_waitlist;

pub fn eat_at_restaurant() {
    add_to_waitlist();
}
```

**示例 7-13：用 `use` 导入 `add_to_waitlist` 函数（不符合习惯）**

　　虽然示例 7-11 和示例 7-13 完成的是同一件事，但示例 7-11 才是用 `use` 导入函数的惯用写法。用 `use` 导入函数的父模块，意味着调用函数时仍需写出父模块。调用时写出父模块，既能表明该函数并非本地定义，又能尽量减少完整路径的重复。示例 7-13 中的代码则不清楚 `add_to_waitlist` 定义在哪里。

　　另一方面，用 `use` 导入结构体、枚举和其他项时，惯用做法是指定完整路径。示例 7-14 展示了在二进制 crate 中把标准库的 `HashMap` 结构体导入当前作用域的惯用写法。

**文件名：`src/main.rs`**
```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.insert(1, 2);
}
```

**示例 7-14：以惯用方式将 `HashMap` 导入当前作用域**

　　这种习惯并没有特别强硬的理由：它只是逐渐形成的约定，人们已经习惯这样读写 Rust 代码。

　　这一习惯的例外是：若我们用 `use` 语句把两个同名项导入同一作用域——Rust 不允许这样做。示例 7-15 展示了如何把两个名称相同但父模块不同的 `Result` 类型导入同一作用域，以及如何引用它们。

**文件名：`src/lib.rs`**
```rust
use std::fmt;
use std::io;

fn function1() -> fmt::Result {
    // --snip--

}

fn function2() -> io::Result<()> {
    // --snip--

}
```

**示例 7-15：把两个同名类型引入同一作用域时，需要借助它们的父模块。**

　　如你所见，使用父模块可以区分这两个 `Result` 类型。若我们分别写 `use std::fmt::Result` 和 `use std::io::Result`，同一作用域里就会有两个 `Result`，Rust 就不知道我们写 `Result` 时指的是哪一个。

### 用 `as` 关键字提供新名称

　　把两个同名类型用 `use` 引入同一作用域时，还有另一种解法：在路径后面可以写 `as` 和一个新的本地名称，也就是该类型的*别名*（alias）。示例 7-16 展示了另一种编写示例 7-15 代码的方式：用 `as` 重命名其中一个 `Result` 类型。

**文件名：`src/lib.rs`**
```rust
use std::fmt::Result;
use std::io::Result as IoResult;

fn function1() -> Result {
    // --snip--

}

fn function2() -> IoResult<()> {
    // --snip--

}
```

**示例 7-16：用 `as` 关键字导入时重命名类型**

　　在第二条 `use` 语句中，我们为 `std::io::Result` 类型选择了新名称 `IoResult`，这样就不会与同样导入的 `std::fmt` 中的 `Result` 冲突。示例 7-15 和示例 7-16 都被视为惯用写法，选择权在你！

### 用 `pub use` 再导出名称

　　当我们用 `use` 关键字导入名称时，该名称对其导入到的作用域是私有的。若要让该作用域之外的代码也能像该项定义在此作用域中一样引用它，可以把 `pub` 与 `use` 结合起来。这种技巧称为*再导出*（re-exporting），因为我们既把项导入了作用域，又让别人也能导入它。

　　示例 7-17 是示例 7-11 的代码，只是把根模块中的 `use` 改成了 `pub use`。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

pub use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

**示例 7-17：用 `pub use` 让任意代码都能从新作用域使用某个名称**

　　在此改动之前，外部代码必须用路径 `restaurant::front_of_house::hosting::add_to_waitlist()` 来调用 `add_to_waitlist` 函数，这还要求 `front_of_house` 模块被标为 `pub`。现在这个 `pub use` 已从根模块再导出了 `hosting` 模块，外部代码可以改用路径 `restaurant::hosting::add_to_waitlist()`。

　　当代码的内部结构与调用方对问题域的思考方式不一致时，再导出很有用。例如，在这个餐馆比喻里，经营餐馆的人会想到「前厅」和「后厨」。但来吃饭的顾客大概不会用这些术语来想餐馆的各个部分。借助 `pub use`，我们可以按一种结构编写代码，却对外暴露另一种结构。这样既能让维护库的程序员感到组织良好，也能让调用库的程序员用起来顺手。我们会在第 14 章的[「导出便捷的公共 API」][ch14-pub-use]中再看一个 `pub use` 的例子，以及它如何影响 crate 的文档。

### 使用外部包

　　在第 2 章，我们编写的猜数字游戏项目使用了一个名为 `rand` 的外部包来获取随机数。要在项目中使用 `rand`，我们在 *Cargo.toml* 中加入了这一行：


**文件名：`Cargo.toml`**
```toml
rand = "0.10.1"
```

　　在 *Cargo.toml* 中把 `rand` 加为依赖，会告诉 Cargo 从 [crates.io](https://crates.io/) 下载 `rand` 包及其依赖，并让 `rand` 对我们的项目可用。

　　然后，为了把 `rand` 的定义导入我们包的作用域，我们添加了一行以 crate 名 `rand` 开头的 `use`，并列出想导入的项。回想第 2 章[「生成一个随机数」][rand]中，我们把 `rand::prelude` 模块中的项导入了作用域，并调用了 `rand::rng` 函数：

```rust
use rand::prelude::*;

fn main() {

    let secret_number = rand::rng().random_range(1..=100);

}
```

　　Rust 社区在 [crates.io](https://crates.io/) 上提供了许多包，把其中任何一个拉进你的包都遵循同样的步骤：在包的 *Cargo.toml* 文件中列出它们，并用 `use` 把其 crate 中的项导入作用域。

　　注意，标准库 `std` 也是一个对我们包而言外部的 crate。因为标准库随 Rust 语言一起提供，我们不必改 *Cargo.toml* 来包含 `std`。但我们仍需要用 `use` 引用它，才能把其中的项导入我们包的作用域。例如，对 `HashMap` 我们会写：

```rust
use std::collections::HashMap;
```

　　这是一条以标准库 crate 名 `std` 开头的绝对路径。

### 用嵌套路径整理 `use` 列表

　　若我们使用的多个项定义在同一个 crate 或同一个模块中，把每一项各写一行会占用大量纵向空间。例如，猜数字游戏示例 2-4 里这两条 `use` 语句把来自 `std` 的项导入了作用域：

**文件名：`src/main.rs`**
```rust
// --snip--
use std::cmp::Ordering;
use std::io;
// --snip--
```

　　我们也可以用嵌套路径在一行里导入相同的项。做法是先写出路径的公共部分，后跟两个冒号，再用花括号包住路径中彼此不同的部分，如示例 7-18 所示。

**文件名：`src/main.rs`**
```rust
// --snip--
use std::{cmp::Ordering, io};
// --snip--
```

**示例 7-18：指定嵌套路径，把具有相同前缀的多个项导入当前作用域**

　　在更大的程序里，用嵌套路径从同一 crate 或模块导入许多项，可以大幅减少所需的独立 `use` 语句数量！

　　我们可以在路径的任意层级使用嵌套路径，这在合并两条共享子路径的 `use` 语句时很有用。例如，示例 7-19 展示了两条 `use`：一条导入 `std::io`，另一条导入 `std::io::Write`。

**文件名：`src/lib.rs`**
```rust
use std::io;
use std::io::Write;
```

**示例 7-19：两条 `use` 语句，其中一条是另一条的子路径**

　　这两条路径的公共部分是 `std::io`，而它也是第一条路径的完整内容。要把这两条路径合并成一条 `use` 语句，可以在嵌套路径中使用 `self`，如示例 7-20 所示。

**文件名：`src/lib.rs`**
```rust
use std::io::{self, Write};
```

**示例 7-20：把示例 7-19 中的路径合并为一条 `use` 语句**

　　这一行把 `std::io` 和 `std::io::Write` 都导入了作用域。

### 用 glob 运算符导入项

　　若想把某个路径下定义的*所有*公有项都导入作用域，可以在该路径后加上 `*` glob 运算符：

```rust
use std::collections::*;
```

　　这条 `use` 语句会把 `std::collections` 中定义的所有公有项引入当前作用域。使用 glob 运算符时要小心！它会让人更难判断作用域里有哪些名字、以及程序中某个名字定义在何处。此外，若依赖更改了其定义，你导入的内容也会跟着变；例如，升级依赖时若依赖新增了一个与你在同一作用域中某个定义同名的定义，就可能导致编译错误。

　　glob 运算符常在测试时用来把被测的一切都引入 `tests` 模块；我们会在第 11 章[「如何编写测试」][writing-tests]中讨论。glob 运算符有时也作为 prelude 模式的一部分使用：关于该模式的更多信息，请参阅[标准库文档](https://doc.rust-lang.org/stable/std/prelude/index.html#other-preludes)。

[ch14-pub-use]: /trpl/more-about-cargo/02-publishing-to-crates-io/#exporting-a-convenient-public-api
[rand]: /trpl/guessing-game/#generating-a-random-number
[writing-tests]: /trpl/testing/01-writing-tests/#how-to-write-tests
