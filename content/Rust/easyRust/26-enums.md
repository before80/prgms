+++
title = "26-枚举"
date = 2026-08-21T12:46:00+08:00
weight = 27
type = "docs"
description = "枚举 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_25.html](https://dhghomon.github.io/easy_rust/Chapter_25.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 枚举

`enum`是enumerations的简称。它们看起来与结构体非常相似，但又有所不同。这就是区别:

- 当你想要一个东西**和**另一个东西时，使用`struct`.
- 当你想要一个东西**或**另一个东西时，请使用 `enum`。

所以，结构体是用于**多个事物**在一起，而枚举则是用于**多个选择**在一起。


要声明一个枚举，请写`enum`，并使用一个包含选项的代码块，用逗号分隔。就像 `struct` 一样，最后一部分可以有逗号，也可以没有。我们将创建一个名为 `ThingsInTheSky` 的枚举。

```rust
enum ThingsInTheSky {
    Sun,
    Stars,
}

fn main() {}
```

这是一个枚举，因为你可以看到太阳，**或**星星:你必须选择一个。这些叫做**变体**。

```rust
// 创建有两个选项的枚举
enum ThingsInTheSky {
    Sun,
    Stars,
}

// 用这个函数可以用 i32 创建 ThingsInTheSky。
fn create_skystate(time: i32) -> ThingsInTheSky {
    match time {
        6..=18 => ThingsInTheSky::Sun, // 6 到 18 点之间能看到太阳
        _ => ThingsInTheSky::Stars, // 否则能看到星星
    }
}

// 用这个函数可以对 ThingsInTheSky 的两个选项做匹配。
fn check_skystate(state: &ThingsInTheSky) {
    match state {
        ThingsInTheSky::Sun => println!("I can see the sun!"),
        ThingsInTheSky::Stars => println!("I can see the stars!")
    }
}

fn main() {
    let time = 8; // 现在是 8 点
    let skystate = create_skystate(time); // create_skystate 返回一个 ThingsInTheSky
    check_skystate(&skystate); // 传入引用，以便读取变量 skystate
}
```

这将打印出`I can see the sun!`。

你也可以将数据添加到一个枚举中。

```rust
enum ThingsInTheSky {
    Sun(String), // 现在每个变体都带有一个字符串
    Stars(String),
}

fn create_skystate(time: i32) -> ThingsInTheSky {
    match time {
        6..=18 => ThingsInTheSky::Sun(String::from("I can see the sun!")), // 在这里写入字符串
        _ => ThingsInTheSky::Stars(String::from("I can see the stars!")),
    }
}

fn check_skystate(state: &ThingsInTheSky) {
    match state {
        ThingsInTheSky::Sun(description) => println!("{}", description), // 给字符串起名 description，以便使用
        ThingsInTheSky::Stars(n) => println!("{}", n), // 也可以叫 n，或其他任何名字——无所谓
    }
}

fn main() {
    let time = 8; // 现在是 8 点
    let skystate = create_skystate(time); // create_skystate 返回一个 ThingsInTheSky
    check_skystate(&skystate); // 传入引用，以便读取变量 skystate
}
```

这样打印出来的结果是一样的:`I can see the sun!`。

你也可以 "导入"一个枚举，这样你就不用打那么多字了。下面是一个例子，我们每次在心情上匹配时都要输入 `Mood::`。

```rust
enum Mood {
    Happy,
    Sleepy,
    NotBad,
    Angry,
}

fn match_mood(mood: &Mood) -> i32 {
    let happiness_level = match mood {
        Mood::Happy => 10, // 这里每次都要写 Mood::
        Mood::Sleepy => 6,
        Mood::NotBad => 7,
        Mood::Angry => 2,
    };
    happiness_level
}

fn main() {
    let my_mood = Mood::NotBad;
    let happiness_level = match_mood(&my_mood);
    println!("Out of 1 to 10, my happiness is {}", happiness_level);
}
```

它打印的是`Out of 1 to 10, my happiness is 7`。让我们导入，这样我们就可以少打点字了。要导入所有的东西，写`*`。注意:它和`*`的解引用键是一样的，但完全不同。

```rust
enum Mood {
    Happy,
    Sleepy,
    NotBad,
    Angry,
}

fn match_mood(mood: &Mood) -> i32 {
    use Mood::*; // 导入了 Mood 中的全部内容。现在可以直接写 Happy、Sleepy 等。
    let happiness_level = match mood {
        Happy => 10, // 不必再写 Mood:: 了
        Sleepy => 6,
        NotBad => 7,
        Angry => 2,
    };
    happiness_level
}

fn main() {
    let my_mood = Mood::Happy;
    let happiness_level = match_mood(&my_mood);
    println!("Out of 1 to 10, my happiness is {}", happiness_level);
}
```


`enum` 的部分也可以变成一个整数。这是因为 Rust 给 `enum` 的每个arm提供了一个以 0 开头的数字，供它自己使用。如果你的枚举中没有任何其他数据，你可以用它来做一些事情。

```rust
enum Season {
    Spring, // 如果写成 Spring(String) 之类就不会生效
    Summer,
    Autumn,
    Winter,
}

fn main() {
    use Season::*;
    let four_seasons = vec![Spring, Summer, Autumn, Winter];
    for season in four_seasons {
        println!("{}", season as u32);
    }
}
```

这个打印:

```text
0
1
2
3
```

不过如果你想的话，你可以给它一个不同的数字--Rust并不在意，可以用同样的方式来使用它。只需在你想要的变体上加一个 `=` 和你的数字。你不必给所有的都分配一个数字。但如果你不这样做，Rust就会从前一个arm加1来赋值给当前arm。

```rust
enum Star {
    BrownDwarf = 10,
    RedDwarf = 50,
    YellowStar = 100,
    RedGiant = 1000,
    DeadStar, // 想想这个。它会是几？
}

fn main() {
    use Star::*;
    let starvec = vec![BrownDwarf, RedDwarf, YellowStar, RedGiant];
    for star in starvec {
        match star as u32 {
            size if size <= 80 => println!("Not the biggest star."), // 记住：size 没有特殊含义，只是我们起的名字以便打印
            size if size >= 80 => println!("This is a good-sized star."),
            _ => println!("That star is pretty big!"),
        }
    }
    println!("What about DeadStar? It's the number {}.", DeadStar as u32);
}
```

这个打印:


```text
Not the biggest star.
Not the biggest star.
This is a good-sized star.
This is a good-sized star.
What about DeadStar? It's the number 1001.
```

`DeadStar`本来是4号，但现在是1001。

## 使用多种类型的枚举

你知道`Vec`、数组等中的元素都需要相同的类型(只有tuple不同)。但其实你可以用一个枚举来放不同的类型。想象一下，我们想有一个`Vec`，有`u32`或`i32`。当然，你可以创建一个`Vec<(u32, i32)>`(一个带有`(u32, i32)`元组的vec)，但是我们每次只想要一个。所以这里可以使用一个枚举。下面是一个简单的例子。

```rust
enum Number {
    U32(u32),
    I32(i32),
}

fn main() {}
```

所以有两个变体:`U32`变体里面有`u32`，`I32`变体里面有`i32`。`U32`和`I32`只是我们起的名字。它们可能是`UThirtyTwo`或`IThirtyTwo`或其他任何东西。

现在，如果我们把它们放到 `Vec` 中，我们就会有一个 `Vec<Number>`，编译器很高兴，因为都是同一个类型。编译器并不在乎我们有 `u32` 或 `i32`，因为它们都在一个叫做 `Number` 的单一类型里面。因为它是一个枚举，你必须选择一个，这就是我们想要的。我们将使用`.is_positive()`方法来挑选。如果是 `true`，那么我们将选择 `U32`，如果是 `false`，那么我们将选择 `I32`。

现在的代码是这样的。

```rust
enum Number {
    U32(u32),
    I32(i32),
}

fn get_number(input: i32) -> Number {
    let number = match input.is_positive() {
        true => Number::U32(input as u32), // 若为正数则转为 u32
        false => Number::I32(input), // 否则直接返回，因为它已经是 i32
    };
    number
}


fn main() {
    let my_vec = vec![get_number(-800), get_number(8)];

    for item in my_vec {
        match item {
            Number::U32(number) => println!("It's a u32 with the value {}", number),
            Number::I32(number) => println!("It's an i32 with the value {}", number),
        }
    }
}
```

这就打印出了我们想看到的东西。

```text
It's an i32 with the value -800
It's a u32 with the value 8
```
