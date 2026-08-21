+++
title = "24-控制流"
date = 2026-08-21T12:46:00+08:00
weight = 25
type = "docs"
description = "控制流 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_23.html](https://dhghomon.github.io/easy_rust/Chapter_23.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 控制流

控制流的意思是告诉你的代码在不同的情况下该怎么做。最简单的控制流是`if`。

```rust
fn main() {
    let my_number = 5;
    if my_number == 7 {
        println!("It's seven");
    }
}
```

另外注意，你用的是`==`而不是`=`。`==`是用来比较的，`=`是用来*赋值*的(给一个值)。另外注意，我们写的是`if my_number == 7`而不是`if (my_number == 7)`。在Rust中，你不需要用`if`的括号。

`else if`和`else`给你更多的控制:

```rust
fn main() {
    let my_number = 5;
    if my_number == 7 {
        println!("It's seven");
    } else if my_number == 6 {
        println!("It's six")
    } else {
        println!("It's a different number")
    }
}
```

这打印出`It's a different number`，因为它不等于7或6。


您可以使用 `&&`(和)和 `||`(或)添加更多条件。

```rust
fn main() {
    let my_number = 5;
    if my_number % 2 == 1 && my_number > 0 { // % 2 表示除以 2 后的余数
        println!("It's a positive odd number");
    } else if my_number == 6 {
        println!("It's six")
    } else {
        println!("It's a different number")
    }
}
```

这打印出的是`It's a positive odd number`，因为当你把它除以2时，你有一个1的余数，它大于0。


你可以看到，过多的`if`、`else`和`else if`会很难读。在这种情况下，你可以使用`match`来代替，它看起来更干净。但是您必须为每一个可能的结果进行匹配。例如，这将无法工作:

```rust
fn main() {
    let my_number: u8 = 5;
    match my_number {
        0 => println!("it's zero"),
        1 => println!("it's one"),
        2 => println!("it's two"),
        // ⚠️
    }
}
```

编译器说:

```text
error[E0004]: non-exhaustive patterns: `3u8..=std::u8::MAX` not covered
 --> src\main.rs:3:11
  |
3 |     match my_number {
  |           ^^^^^^^^^ pattern `3u8..=std::u8::MAX` not covered
```

这就意味着 "你告诉我0到2，但`u8`可以到255。那3呢？那4呢？5呢？" 以此类推。所以你可以加上`_`，意思是 "其他任何东西"。

```rust
fn main() {
    let my_number: u8 = 5;
    match my_number {
        0 => println!("it's zero"),
        1 => println!("it's one"),
        2 => println!("it's two"),
        _ => println!("It's some other number"),
    }
}
```

那打印`It's some other number`。

记住匹配的规则:

- 你写下`match`，然后创建一个`{}`的代码块。
- 在左边写上*模式*，用`=>`胖箭头说明匹配时该怎么做。
- 每一行称为一个 "arm"。
- 在arm之间放一个逗号(不是分号)。

你可以用匹配来声明一个值。

```rust
fn main() {
    let my_number = 5;
    let second_number = match my_number {
        0 => 0,
        5 => 10,
        _ => 2,
    };
}
```

`second_number`将是10。你看到最后的分号了吗？那是因为，在match结束后，我们实际上告诉了编译器这个信息:`let second_number = 10;`


你也可以在更复杂的事情上进行匹配。你用一个元组来做。

```rust
fn main() {
    let sky = "cloudy";
    let temperature = "warm";

    match (sky, temperature) {
        ("cloudy", "cold") => println!("It's dark and unpleasant today"),
        ("clear", "warm") => println!("It's a nice day"),
        ("cloudy", "warm") => println!("It's dark but not bad"),
        _ => println!("Not sure what the weather is."),
    }
}
```

这打印了`It's dark but not bad`，因为它与`sky`和`temperature`的 "多云"和 "温暖"相匹配。

你甚至可以把`if`放在`match`里面。这就是所谓的 "match guard"。

```rust
fn main() {
    let children = 5;
    let married = true;

    match (children, married) {
        (children, married) if married == false => println!("Not married with {} children", children),
        (children, married) if children == 0 && married == true => println!("Married but no children"),
        _ => println!("Married? {}. Number of children: {}.", married, children),
    }
}
```

这将打印`Married? true. Number of children: 5.`

在一次匹配中，你可以随意使用 _ 。在这个关于颜色的匹配中，我们有三个颜色，但一次只能选中一个。

```rust
fn match_colours(rbg: (i32, i32, i32)) {
    match rbg {
        (r, _, _) if r < 10 => println!("Not much red"),
        (_, b, _) if b < 10 => println!("Not much blue"),
        (_, _, g) if g < 10 => println!("Not much green"),
        _ => println!("Each colour has at least 10"),
    }
}

fn main() {
    let first = (200, 0, 0);
    let second = (50, 50, 50);
    let third = (200, 50, 0);

    match_colours(first);
    match_colours(second);
    match_colours(third);

}
```

这个将打印:

```text
Not much blue
Each colour has at least 10
Not much green
```

这也说明了`match`语句的作用，因为在第一个例子中，它只打印了`Not much blue`。但是`first`也没有多少绿色。`match`语句总是在找到一个匹配项时停止，而不检查其他的。这就是一个很好的例子，代码编译得很好，但不是你想要的代码。

你可以创建一个非常大的 `match` 语句来解决这个问题，但是使用 `for` 循环可能更好。我们将很快讨论循环。

匹配必须返回相同的类型。所以你不能这样做:

```rust
fn main() {
    let my_number = 10;
    let some_variable = match my_number {
        10 => 8,
        _ => "Not ten", // ⚠️
    };
}
```

编译器告诉你:

```text
error[E0308]: `match` arms have incompatible types
  --> src\main.rs:17:14
   |
15 |       let some_variable = match my_number {
   |  _________________________-
16 | |         10 => 8,
   | |               - this is found to be of type `{integer}`
17 | |         _ => "Not ten",
   | |              ^^^^^^^^^ expected integer, found `&str`
18 | |     };
   | |_____- `match` arms have incompatible types
```

这样也不行，原因同上。

```rust
fn main() {
    let some_variable = if my_number == 10 { 8 } else { "something else "}; // ⚠️
}
```

但是这样就可以了，因为不是`match`，所以你每次都有不同的`let`语句。

```rust
fn main() {
    let my_number = 10;

    if my_number == 10 {
        let some_variable = 8;
    } else {
        let some_variable = "Something else";
    }
}
```

你也可以使用 `@` 给 `match` 表达式的值起一个名字，然后你就可以使用它。在这个例子中，我们在一个函数中匹配一个 `i32` 输入。如果是4或13，我们要在`println!`语句中使用这个数字。否则，我们不需要使用它。

```rust
fn match_number(input: i32) {
    match input {
    number @ 4 => println!("{} is an unlucky number in China (sounds close to 死)!", number),
    number @ 13 => println!("{} is unlucky in North America, lucky in Italy! In bocca al lupo!", number),
    _ => println!("Looks like a normal number"),
    }
}

fn main() {
    match_number(50);
    match_number(13);
    match_number(4);
}
```

这个打印:

```text
Looks like a normal number
13 is unlucky in North America, lucky in Italy! In bocca al lupo!
4 is an unlucky number in China (sounds close to 死)!
```
