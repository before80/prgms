+++
title = "49-impl Trait"
date = 2026-08-21T12:46:00+08:00
weight = 50
type = "docs"
description = "impl Trait — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_48.html](https://dhghomon.github.io/easy_rust/Chapter_48.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# impl Trait

`impl Trait`与泛型类似。你还记得，泛型使用一个类型 `T`(或任何其他名称)，然后在程序编译时决定。首先我们来看一个具体的类型:

```rust
fn gives_higher_i32(one: i32, two: i32) {
    let higher = if one > two { one } else { two };
    println!("{} is higher.", higher);
}

fn main() {
    gives_higher_i32(8, 10);
}
```

这个打印:`10 is higher.`.

但是这个只接受`i32`，所以现在我们要把它做成通用的。我们需要比较，我们需要用`{}`打印，所以我们的类型T需要`PartialOrd`和`Display`。记住，这意味着 "只接受已经实现`PartialOrd`和`Display`的类型"。

```rust
use std::fmt::Display;

fn gives_higher_i32<T: PartialOrd + Display>(one: T, two: T) {
    let higher = if one > two { one } else { two };
    println!("{} is higher.", higher);
}

fn main() {
    gives_higher_i32(8, 10);
}
```

现在我们来看看`impl Trait`，它也是类似的。我们可以引入一个类型 `impl Trait`，而不是 `T`。然后它将带入一个实现该特性的类型。这几乎是一样的。

```rust
fn prints_it(input: impl Into<String> + std::fmt::Display) { // 接受任何能转成 String 且实现 Display 的类型
    println!("You can print many things, including {}", input);
}

fn main() {
    let name = "Tuon";
    let string_name = String::from("Tuon");
    prints_it(name);
    prints_it(string_name);
}
```

然而，更有趣的是，我们可以返回 `impl Trait`，这让我们可以返回闭包，因为它们的函数签名是trait。你可以在有它们的方法的签名中看到这一点。例如，这是 `.map()` 的签名。

```rust
fn map<B, F>(self, f: F) -> Map<Self, F>     // 🚧
    where
        Self: Sized,
        F: FnMut(Self::Item) -> B,
    {
        Map::new(self, f)
    }
```

`fn map<B, F>(self, f: F)`的意思是，它需要两个通用类型。`F`是指从实现`.map()`的容器中取一个元素的函数，`B`是该函数的返回类型。然后在`where`之后，我们看到的是trait bound。("trait bound"的意思是 "它必须有这个trait"。)一个是`Sized`，接下来是闭包签名。它必须是一个 `FnMut`，并在 `Self::Item` 上做闭包，也就是你给它的迭代器。然后它返回`B`。

所以我们可以用同样的方法来返回一个闭包。要返回一个闭包，使用 `impl`，然后是闭包签名。一旦你返回它，你就可以像使用一个函数一样使用它。下面是一个函数的小例子，它根据你输入的文本给出一个闭包。如果你输入 "double "或 "triple"，那么它就会把它乘以2或3，否则就会返给你相同的数字。因为它是一个闭包，我们可以做任何我们想做的事情，所以我们也打印一条信息。

```rust
fn returns_a_closure(input: &str) -> impl FnMut(i32) -> i32 {
    match input {
        "double" => |mut number| {
            number *= 2;
            println!("Doubling number. Now it is {}", number);
            number
        },
        "triple" => |mut number| {
            number *= 40;
            println!("Tripling number. Now it is {}", number);
            number
        },
        _ => |number| {
            println!("Sorry, it's the same: {}.", number);
            number
        },
    }
}

fn main() {
    let my_number = 10;

    // 创建三个闭包
    let mut doubles = returns_a_closure("double");
    let mut triples = returns_a_closure("triple");
    let mut quadruples = returns_a_closure("quadruple");

    doubles(my_number);
    triples(my_number);
    quadruples(my_number);
}
```

下面是一个比较长的例子。让我们想象一下，在一个游戏中，你的角色面对的是晚上比较强的怪物。我们可以创建一个叫`TimeOfDay`的枚举来记录一天的情况。你的角色叫西蒙，有一个叫`character_fear`的数字，也就是`f64`。它晚上上升，白天下降。我们将创建一个`change_fear`函数，改变他的恐惧，但也做其他事情，如写消息。它大概是这样的:


```rust
enum TimeOfDay { // 只是一个简单枚举
    Dawn,
    Day,
    Sunset,
    Night,
}

fn change_fear(input: TimeOfDay) -> impl FnMut(f64) -> f64 { // 函数接受 TimeOfDay，返回一个闭包。
                                                             // 用 impl FnMut(f64) -> f64 表示它需要
                                                             // 改变值，并返回相同类型。
    use TimeOfDay::*; // 这样就只需写 Dawn、Day、Sunset、Night
                      // 而不必写 TimeOfDay::Dawn、TimeOfDay::Day 等。
    match input {
        Dawn => |x| { // 这就是我们稍后传入的 character_fear 变量
            println!("The morning sun has vanquished the horrible night. You no longer feel afraid.");
            println!("Your fear is now {}", x * 0.5);
            x * 0.5
        },
        Day => |x| {
            println!("What a nice day. Maybe put your feet up and rest a bit.");
            println!("Your fear is now {}", x * 0.2);
            x * 0.2
        },
        Sunset => |x| {
            println!("The sun is almost down! This is no good.");
            println!("Your fear is now {}", x * 1.4);
            x * 1.4
        },
        Night => |x| {
            println!("What a horrible night to have a curse.");
            println!("Your fear is now {}", x * 5.0);
            x * 5.0
        },
    }
}

fn main() {
    use TimeOfDay::*;
    let mut character_fear = 10.0; // 给 Simon 初始恐惧值 10

    let mut daytime = change_fear(Day); // 在这里创建四个闭包，每次想改 Simon 的恐惧时调用。
    let mut sunset = change_fear(Sunset);
    let mut night = change_fear(Night);
    let mut morning = change_fear(Dawn);

    character_fear = daytime(character_fear); // 对 Simon 的恐惧调用闭包。它们会打印消息并改变恐惧值。
                                              // 实际项目里我们会有 Character 结构体，并把它做成方法，
                                              // 像这样：character_fear.daytime()
    character_fear = sunset(character_fear);
    character_fear = night(character_fear);
    character_fear = morning(character_fear);
}
```

这个打印:

```text
What a nice day. Maybe put your feet up and rest a bit.
Your fear is now 2
The sun is almost down! This is no good.
Your fear is now 2.8
What a horrible night to have a curse.
Your fear is now 14
The morning sun has vanquished the horrible night. You no longer feel afraid.
Your fear is now 7
```
