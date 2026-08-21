+++
title = "25-结构体"
date = 2026-08-21T12:46:00+08:00
weight = 26
type = "docs"
description = "结构体 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_24.html](https://dhghomon.github.io/easy_rust/Chapter_24.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 结构体

有了结构体，你可以创建自己的类型。在 Rust 中，你会一直使用结构体，因为它们非常方便。结构体是用关键字 `struct` 创建的。结构体的名称应该用UpperCamelCase(每个字用大写字母，不要用空格)。如果你用全小写的结构，编译器会告诉你。

有三种类型的结构。一种是 "单元结构"。单元的意思是 "没有任何东西"。对于一个单元结构，你只需要写名字和一个分号。

```rust
struct FileDirectory;
fn main() {}
```

接下来是一个元组结构，或者说是一个未命名结构。之所以是 "未命名"，是因为你只需要写类型，而不是字段名。当你需要一个简单的结构，并且不需要记住名字时，元组结构是很好的选择。

```rust
struct Colour(u8, u8, u8);

fn main() {
    let my_colour = Colour(50, 0, 50); // 用 RGB（红、绿、蓝）构造颜色
    println!("The second part of the colour is: {}", my_colour.1);
}
```

这时打印出`The second part of the colour is: 0`。

第三种类型是命名结构。这可能是最常见的结构。在这个结构中，你在一个 `{}` 代码块中声明字段名和类型。请注意，在命名结构后面不要写分号，因为后面有一整个代码块。

```rust
struct Colour(u8, u8, u8); // 声明同一个 Colour 元组结构体

struct SizeAndColour {
    size: u32,
    colour: Colour, // 并放入我们新的具名字段结构体
}

fn main() {
    let my_colour = Colour(50, 0, 50);

    let size_and_colour = SizeAndColour {
        size: 150,
        colour: my_colour
    };
}
```

在一个命名结构中，你也可以用逗号来分隔字段。对于最后一个字段，你可以加一个逗号或不加--这取决于你。`SizeAndColour` 在 `colour` 后面有一个逗号。

```rust
struct Colour(u8, u8, u8); // 声明同一个 Colour 元组结构体

struct SizeAndColour {
    size: u32,
    colour: Colour, // 并放入我们新的具名字段结构体
}

fn main() {}
```

但你不需要它。但总是放一个逗号可能是个好主意，因为有时你会改变字段的顺序。

```rust
struct Colour(u8, u8, u8); // 声明同一个 Colour 元组结构体

struct SizeAndColour {
    size: u32,
    colour: Colour // 这里没有逗号
}

fn main() {}
```

然后我们决定改变顺序...

```rust
struct SizeAndColour {
    colour: Colour // ⚠️ 糟糕！现在这里没有逗号了。
    size: u32,
}

fn main() {}
```

但无论哪种方式都不是很重要，所以你可以选择是否使用逗号。


我们创建一个`Country`结构来举例说明。`Country`结构有`population`、`capital`和`leader_name`三个字段。

```rust
struct Country {
    population: u32,
    capital: String,
    leader_name: String
}

fn main() {
    let population = 500_000;
    let capital = String::from("Elista");
    let leader_name = String::from("Batu Khasikov");

    let kalmykia = Country {
        population: population,
        capital: capital,
        leader_name: leader_name,
    };
}
```

你有没有注意到，我们把同样的东西写了两次？我们写了`population: population`、`capital: capital`和`leader_name: leader_name`。实际上，你不需要这样做:如果字段名和变量名是一样的，你就不用写两次。

```rust
struct Country {
    population: u32,
    capital: String,
    leader_name: String
}

fn main() {
    let population = 500_000;
    let capital = String::from("Elista");
    let leader_name = String::from("Batu Khasikov");

    let kalmykia = Country {
        population,
        capital,
        leader_name,
    };
}
```
