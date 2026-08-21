+++
title = "58-Crate 和模块"
date = 2026-08-21T12:46:00+08:00
weight = 59
type = "docs"
description = "Crate 和模块 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_57.html](https://dhghomon.github.io/easy_rust/Chapter_57.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Crate 和模块

每次你在 Rust 中写代码时，你都是在 `crate` 中写的。`crate`是一个或多个文件，一起为你的代码服务。在你写的文件里面，你也可以创建一个`mod`。`mod`是存放函数、结构体等的空间，因为这些原因被使用:

- 构建你的代码:它可以帮助你思考代码的总体结构。当你的代码越来越大时，这一点可能很重要。
- 阅读你的代码:人们可以更容易理解你的代码。例如，`std::collections::HashMap`这个名字告诉你，它在`std`的模块`collections`里面。这给了你一个提示，也许`collections`里面还有更多的集合类型，你可以尝试一下。
- 私密性:所有的东西一开始都是私有的。这样可以让你不让用户直接使用函数。

要创建一个`mod`，只需要写`mod`，然后用`{}`开始一个代码块。我们将创建一个名为`print_things`的mod，它有一些打印相关的功能。

```rust
mod print_things {
    use std::fmt::Display;

    fn prints_one_thing<T: Display>(input: T) { // 打印任何实现了 Display 的东西
        println!("{}", input)
    }
}

fn main() {}
```

你可以看到，我们把`use std::fmt::Display;`写在`print_things`里面，因为它是一个独立的空间。如果你把`use std::fmt::Display;`写在`main()`里面，那没用。而且，我们现在也不能从`main()`里面调用。如果在`fn`前面没有`pub`这个关键字，它就会保持私密性。让我们试着在没有`pub`的情况下调用它。这里有一种写法。

```rust
// 🚧
fn main() {
    crate::print_things::prints_one_thing(6);
}
```


`crate`的意思是 "在这个项目里"，但对于我们简单的例子来说，它和 "在这个文件里面"是一样的。接着是`print_things`这个mod，最后是`prints_one_thing()`函数。你可以每次都写这个，也可以写`use`来导入。现在我们可以看到说它是私有的错误:

```rust
// ⚠️
mod print_things {
    use std::fmt::Display;

    fn prints_one_thing<T: Display>(input: T) {
        println!("{}", input)
    }
}

fn main() {
    use crate::print_things::prints_one_thing;

    prints_one_thing(6);
    prints_one_thing("Trying to print a string...".to_string());
}
```

这是错误的。

```text
error[E0603]: function `prints_one_thing` is private
  --> src\main.rs:10:30
   |
10 |     use crate::print_things::prints_one_thing;
   |                              ^^^^^^^^^^^^^^^^ private function
   |
note: the function `prints_one_thing` is defined here
  --> src\main.rs:4:5
   |
4  |     fn prints_one_thing<T: Display>(input: T) {
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
很容易理解，函数`print_one_thing`是私有的。它还用`src\main.rs:4:5`告诉我们在哪里可以找到这个函数。这很有帮助，因为你不仅可以在一个文件中写`mod`，还可以在很多文件中写`mod`。

现在我们只需要写`pub fn`而不是`fn`，一切就都可以了。

```rust
mod print_things {
    use std::fmt::Display;

    pub fn prints_one_thing<T: Display>(input: T) {
        println!("{}", input)
    }
}

fn main() {
    use crate::print_things::prints_one_thing;

    prints_one_thing(6);
    prints_one_thing("Trying to print a string...".to_string());
}
```

这个打印:

```text
6
Trying to print a string...
```

`pub`对结构体、枚举、trait或模块有什么作用？`pub`对它们来说是这样的:

- `pub`对于一个结构：它使结构公开，但成员不是公开的。要想让一个成员公开，你也要为每个成员写`pub`。
- `pub` 对于一个枚举或trait：所有的东西都变成了公共的。这是有意义的，因为traits是给事物赋予相同的行为。而枚举是值之间的选择，你需要看到所有的枚举值才能做选择。
- `pub`对于一个模块来说：一个顶层的模块会是`pub`，因为如果它不是pub，那么根本没有人可以使用里面的任何东西。但是模块里面的模块需要使用`pub`才能成为公共的。

我们在`print_things`里面放一个名为`Billy`的结构体。这个结构体几乎都会是public的，但也不尽然。这个结构是公共的，所以它这样写：`pub struct Billy`。里面会有一个 `name` 和 `times_to_print`。`name`不会是公共的，因为我们只想让用户创建名为`"Billy".to_string()`的结构。但是用户可以选择打印的次数，所以这将是公开的。它的是这样的:

```rust
mod print_things {
    use std::fmt::{Display, Debug};

    #[derive(Debug)]
    pub struct Billy { // Billy 是公开的
        name: String, // 但 name 是私有的。
        pub times_to_print: u32,
    }

    impl Billy {
        pub fn new(times_to_print: u32) -> Self { // 所以用户要用 new 创建 Billy。用户只能改 times_to_print
            Self {
                name: "Billy".to_string(), // 名字由我们定 — 用户改不了
                times_to_print,
            }
        }

        pub fn print_billy(&self) { // 这个函数打印 Billy
            for _ in 0..self.times_to_print {
                println!("{:?}", self.name);
            }
        }
    }

    pub fn prints_one_thing<T: Display>(input: T) {
        println!("{}", input)
    }
}

fn main() {
    use crate::print_things::*; // 现在用 *。从 print_things 导入全部

    let my_billy = Billy::new(3);
    my_billy.print_billy();
}
```

这将打印:

```text
"Billy"
"Billy"
"Billy"
```

对了，导入一切的`*`叫做 "glob运算符"。Glob的意思是 "全局"，所以它意味着一切。

在`mod`里面你可以创建其他mod。一个子 mod(mod里的mod)总是可以使用父 mod 内部的任何东西。你可以在下一个例子中看到这一点，我们在 `mod province` 里面有一个 `mod city`，而`mod province`在 `mod country` 里面。

你可以这样想:即使你在一个国家，你可能不在一个省。而即使你在一个省，你也可能不在一个市。但如果你在一个城市，你就在这个城市的省份和它的国家。


```rust
mod country { // 最外层 mod 不需要 pub
    fn print_country(country: &str) { // 注意：这个函数不是公开的
        println!("We are in the country of {}", country);
    }
    pub mod province { // 把这个 mod 设为公开

        fn print_province(province: &str) { // 注意：这个函数不是公开的
            println!("in the province of {}", province);
        }

        pub mod city { // 把这个 mod 设为公开
            pub fn print_city(country: &str, province: &str, city: &str) {  // 不过这个函数是公开的
                crate::country::print_country(country);
                crate::country::province::print_province(province);
                println!("in the city of {}", city);
            }
        }
    }
}

fn main() {
    crate::country::province::city::print_city("Canada", "New Brunswick", "Moncton");
}
```

有趣的是，`print_city`可以访问`print_province`和`print_country`。这是因为`mod city`在其他mod里面。它不需要在`print_province`前面添加`pub`之后才能使用。这也是有道理的:一个城市不需要做什么，它本来就在一个省里，在一个国家里。

你可能注意到，`crate::country::province::print_province(province);`非常长。当我们在一个模块里面的时候，我们可以用`super`从上面引入元素。其实super这个词本身就是"上面"的意思，比如 "上级"。在我们的例子中，我们只用了一次函数，但是如果你用的比较多的话，那么最好是导入。如果它能让你的代码更容易阅读，那也是个好主意，即使你只用了一次函数。现在的代码几乎是一样的，但更容易阅读一些。

```rust
mod country {
    fn print_country(country: &str) {
        println!("We are in the country of {}", country);
    }
    pub mod province {
        fn print_province(province: &str) {
            println!("in the province of {}", province);
        }

        pub mod city {
            use super::super::*; // 使用「上上层」的全部：也就是 mod country
            use super::*;        // 使用「上一层」的全部：也就是 mod province

            pub fn print_city(country: &str, province: &str, city: &str) {
                print_country(country);
                print_province(province);
                println!("in the city of {}", city);
            }
        }
    }
}

fn main() {
    use crate::country::province::city::print_city; // 引入这个函数

    print_city("Canada", "New Brunswick", "Moncton");
    print_city("Korea", "Gyeonggi-do", "Gwangju"); // 再调用就省事了
}
```
