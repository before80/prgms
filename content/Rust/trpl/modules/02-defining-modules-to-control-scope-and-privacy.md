+++
title = "7.2 用模块控制作用域与私有性"
date = 2026-08-05T08:44:00+08:00
weight = 29
type = "docs"
description = "用模块组织代码并控制作用域与私有性"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用模块控制作用域与私有性


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-02-defining-modules-to-control-scope-and-privacy.html](https://doc.rust-lang.org/stable/book/ch07-02-defining-modules-to-control-scope-and-privacy.html)


## 用模块控制作用域与私有性

　　本节我们讨论模块以及模块系统的其他部分，即：用来为项命名的*路径*（paths）、把路径引入作用域的 `use` 关键字，以及让项变为公有的 `pub` 关键字。我们还会谈到 `as` 关键字、外部包，以及 glob 运算符。

### 模块速查表

　　在深入模块与路径的细节之前，这里先给出一份快速参考：编译器如何处理模块、路径、`use` 与 `pub`，以及多数开发者如何组织代码。本章后面会对每条规则举例说明，但需要复习模块用法时，这里是很好的对照点。

- **从 crate 根开始**：编译一个 crate 时，编译器首先在 crate 根文件（库 crate 通常是 *src/lib.rs*，二进制 crate 通常是 *src/main.rs*）里查找要编译的代码。
- **声明模块**：在 crate 根文件中可以声明新模块；例如用 `mod garden;` 声明一个 “garden” 模块。编译器会在这些位置查找该模块的代码：
  - 内联：用花括号代替 `mod garden` 后面的分号
  - 文件 *src/garden.rs*
  - 文件 *src/garden/mod.rs*
- **声明子模块**：在除 crate 根以外的任意文件中，可以声明子模块。例如，你可以在 *src/garden.rs* 里声明 `mod vegetables;`。编译器会在以父模块命名的目录下这些位置查找子模块代码：
  - 内联：紧跟在 `mod vegetables` 之后，用花括号代替分号
  - 文件 *src/garden/vegetables.rs*
  - 文件 *src/garden/vegetables/mod.rs*
- **指向模块中代码的路径**：一旦模块成为 crate 的一部分，只要私有性规则允许，你就可以在同一 crate 的任何其他地方用路径引用该模块中的代码。例如，菜园蔬菜模块里的 `Asparagus` 类型，路径是 `crate::garden::vegetables::Asparagus`。
- **私有与公有**：默认情况下，模块内的代码对其父模块是私有的。要使模块公有，用 `pub mod` 而不是 `mod` 来声明。要使公有模块内的项也公有，在声明前加上 `pub`。
- **`use` 关键字**：在某个作用域内，`use` 关键字可为项创建捷径，减少重复写长路径。在任何能引用 `crate::garden::vegetables::Asparagus` 的作用域里，你可以写 `use crate::garden::vegetables::Asparagus;` 创建捷径，之后在该作用域内只需写 `Asparagus` 即可使用该类型。

　　下面我们创建一个名为 `backyard` 的二进制 crate 来演示这些规则。crate 的目录也叫 *backyard*，其中包含这些文件和目录：

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

　　此例中的 crate 根文件是 *src/main.rs*，内容为：

**文件名：`src/main.rs`**
```rust
use crate::garden::vegetables::Asparagus;

pub mod garden;

fn main() {
    let plant = Asparagus {};
    println!("I'm growing {plant:?}!");
}
```

　　`pub mod garden;` 这一行告诉编译器把在 *src/garden.rs* 中找到的代码包含进来，该文件内容是：

**文件名：`src/garden.rs`**
```rust
pub mod vegetables;
```

　　这里的 `pub mod vegetables;` 表示 *src/garden/vegetables.rs* 中的代码也会被包含进来。那段代码是：

```rust
#[derive(Debug)]
pub struct Asparagus {}
```

　　接下来我们深入这些规则的细节，并用实际例子演示！

### 在模块中把相关代码分组

　　*模块*（modules）让我们能在 crate 内组织代码，以提高可读性和便于复用。模块也让我们能控制项的*私有性*（privacy），因为模块内的代码默认是私有的。私有项是内部实现细节，外部不可用。我们可以选择把模块及其内部的项设为公有，从而暴露它们，让外部代码能够使用并依赖。

　　举个例子，我们来写一个提供餐馆功能的库 crate。我们只定义函数签名，函数体留空，以便把注意力放在代码组织上，而不是餐馆的具体实现。

　　在餐饮业里，餐馆的某些部分称为前厅（front of house），另一些称为后厨（back of house）。*前厅*是顾客所在之处：包括接待安排座位、服务员点单收款、调酒师调制饮品等。*后厨*则是厨师在厨房工作、洗碗工清理、经理做行政事务的地方。

　　要按这种方式组织我们的 crate，可以把函数放进嵌套的模块里。运行 `cargo new restaurant --lib` 创建一个名为 `restaurant` 的新库。然后把示例 7-1 中的代码写入 *src/lib.rs*，定义一些模块和函数签名；这段代码对应前厅部分。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}

        fn seat_at_table() {}
    }

    mod serving {
        fn take_order() {}

        fn serve_order() {}

        fn take_payment() {}
    }
}
```

**示例 7-1：包含其他模块，而这些模块又包含函数的 `front_of_house` 模块**

　　我们用 `mod` 关键字后跟模块名（此处是 `front_of_house`）来定义模块。模块体放在花括号里。模块内部可以再放其他模块，如此处的 `hosting` 和 `serving`。模块也可以容纳其他项的定义，例如结构体、枚举、常量、特征（trait），以及示例 7-1 中的函数。

　　借助模块，我们可以把相关定义归到一起，并用名称说明它们为何相关。使用这段代码的程序员可以按分组浏览，而不必通读所有定义，从而更容易找到与自己相关的部分。要往这段代码里加新功能的程序员也会知道该把代码放在哪里，以保持程序井然有序。

　　前面提到，*src/main.rs* 和 *src/lib.rs* 被称为*crate 根*。之所以这样叫，是因为这两个文件任一者的内容都会形成一个名为 `crate` 的模块，位于该 crate 模块结构的根部，这个结构称为*模块树*（module tree）。

　　示例 7-2 展示了示例 7-1 对应结构的模块树。

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

**示例 7-2：示例 7-1 中代码的模块树**

　　这棵树显示了部分模块如何嵌套在其他模块中；例如，`hosting` 嵌套在 `front_of_house` 里。树也显示了有些模块是*兄弟*（siblings），意思是它们定义在同一模块中：`hosting` 和 `serving` 就是定义在 `front_of_house` 内的兄弟模块。若模块 A 包含在模块 B 内，我们就说模块 A 是模块 B 的*子模块*（child），模块 B 是模块 A 的*父模块*（parent）。注意，整棵模块树都挂在隐式的名为 `crate` 的模块之下。

　　模块树可能会让你想起电脑上文件系统的目录树；这个类比非常贴切！就像文件系统里的目录一样，你用模块来组织代码。也像目录里的文件一样，我们需要一种方式来找到自己的模块。
