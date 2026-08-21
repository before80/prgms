+++
title = "41-生命周期"
date = 2026-08-21T12:46:00+08:00
weight = 42
type = "docs"
description = "生命周期 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_40.html](https://dhghomon.github.io/easy_rust/Chapter_40.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 生命周期

生命期的意思是 "变量的生命期有多长"。你只需要考虑引用的生命期。这是因为引用的生命期不能比它们来自的对象更长。例如，这个函数就不能用。

```rust
fn returns_reference() -> &str {
    let my_string = String::from("I am a string");
    &my_string // ⚠️
}

fn main() {}
```

问题是`my_string`只存在于`returns_reference`中。我们试图返回 `&my_string`，但是 `&my_string` 不能没有 `my_string`。所以编译器说不行。

这个代码也不行。

```rust
fn returns_str() -> &str {
    let my_string = String::from("I am a string");
    "I am a str" // ⚠️
}

fn main() {
    let my_str = returns_str();
    println!("{}", my_str);
}
```

但几乎是成功的。编译器说:

```text
error[E0106]: missing lifetime specifier
 --> src\main.rs:6:21
  |
6 | fn returns_str() -> &str {
  |                     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value for it to be borrowed from
help: consider using the `'static` lifetime
  |
6 | fn returns_str() -> &'static str {
  |                     ^^^^^^^^
```

`missing lifetime specifier`的意思是，我们需要加一个`'`的生命期。然后说它`contains a borrowed value, but there is no value for it to be borrowed from`。也就是说，`I am a str`不是借来的。它写`&'static str`就说`consider using the 'static lifetime`。所以它认为我们应该尝试说这是一个字符串的文字。

现在它工作了。

```rust
fn returns_str() -> &'static str {
    let my_string = String::from("I am a string");
    "I am a str"
}

fn main() {
    let my_str = returns_str();
    println!("{}", my_str);
}
```

这是因为我们返回了一个 `&str`，生命期为 `static`。同时，`my_string`只能以`String`的形式返回:我们不能返回对它的引用，因为它将在下一行死亡。

所以现在`fn returns_str() -> &'static str`告诉Rust， "别担心，我们只会返回一个字符串字面量". 字符串字面量在整个程序中都是有效的，所以Rust很高兴。你会注意到，这与泛型类似。当我们告诉编译器类似 `<T: Display>` 的东西时，我们承诺我们将只使用实现了 `Display` 的输入。生命期也类似:我们并没有改变任何变量的生命期。我们只是告诉编译器输入的生命期是多少。

但是`'static`并不是唯一的生命期。实际上，每个变量都有一个生命期，但通常我们不必写出来。编译器很聪明，一般都能自己算出来。只有在编译器不知道的时候，我们才需要写出生命期。

下面是另一个生命期的例子。想象一下，我们想创建一个`City`结构，并给它一个`&str`的名字。我们可能想这样做，因为这样做的性能比用`String`快。所以我们这样写，但还不能用。

```rust
#[derive(Debug)]
struct City {
    name: &str, // ⚠️
    date_founded: u32,
}

fn main() {
    let my_city = City {
        name: "Ichinomiya",
        date_founded: 1921,
    };
}
```

编译器说:

```text
error[E0106]: missing lifetime specifier
 --> src\main.rs:3:11
  |
3 |     name: &str,
  |           ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
2 | struct City<'a> {
3 |     name: &'a str,
  |
```

Rust 需要 `&str` 的生命期，因为 `&str` 是一个引用。如果`name`指向的值被丢弃了会怎样？那就不安全了。

`'static`呢，能用吗？我们以前用过。我们试试吧。

```rust
#[derive(Debug)]
struct City {
    name: &'static str, // 把 &str 改成 &'static str
    date_founded: u32,
}

fn main() {
    let my_city = City {
        name: "Ichinomiya",
        date_founded: 1921,
    };

    println!("{} was founded in {}", my_city.name, my_city.date_founded);
}
```

好的，这就可以了。也许这就是你想要的结构。但是，请注意，我们只能接受 "字符串字面量"，所以不能接受对其他东西的引用。所以这将无法工作。

```rust
#[derive(Debug)]
struct City {
    name: &'static str, // 必须与整个程序同寿
    date_founded: u32,
}

fn main() {
    let city_names = vec!["Ichinomiya".to_string(), "Kurume".to_string()]; // city_names 不会活过整个程序

    let my_city = City {
        name: &city_names[0], // ⚠️ 这是 &str，但不是 &'static str。它是对 city_names 内部值的引用
        date_founded: 1921,
    };

    println!("{} was founded in {}", my_city.name, my_city.date_founded);
}
```

编译器说:

```text
error[E0597]: `city_names` does not live long enough
  --> src\main.rs:12:16
   |
12 |         name: &city_names[0],
   |                ^^^^^^^^^^
   |                |
   |                borrowed value does not live long enough
   |                requires that `city_names` is borrowed for `'static`
...
18 | }
   | - `city_names` dropped here while still borrowed
```

这一点很重要，因为我们给它的引用其实已经够长寿了。但是我们承诺只给它一个`&'static str`，这就是问题所在。

所以现在我们就试试之前编译器的建议。它说尝试写`struct City<'a>`和`name: &'a str`。这就意味着，只有当`name`活到`City`一样寿命的情况下，它才会接受`name`的引用。

```rust
#[derive(Debug)]
struct City<'a> { // City 有生命周期 'a
    name: &'a str, // name 也有生命周期 'a。
    date_founded: u32,
}

fn main() {
    let city_names = vec!["Ichinomiya".to_string(), "Kurume".to_string()];

    let my_city = City {
        name: &city_names[0],
        date_founded: 1921,
    };

    println!("{} was founded in {}", my_city.name, my_city.date_founded);
}
```

另外记住，如果你愿意，你可以写任何东西来代替`'a`。这也和泛型类似，我们写`T`和`U`，但实际上可以写任何东西。

```rust
#[derive(Debug)]
struct City<'city> { // 生命周期现在叫 'city
    name: &'city str, // name 拥有 'city 生命周期
    date_founded: u32,
}

fn main() {}
```

所以一般都会写`'a, 'b, 'c`等，因为这样写起来比较快，也是常用的写法。但如果你想的话，你可以随时更改。有一个很好的建议是，如果代码非常复杂，把生命期改成一个 "人类可读"的名字可以帮助你阅读代码。

我们再来看看与trait的比较，对于泛型。比如说

```rust
use std::fmt::Display;

fn prints<T: Display>(input: T) {
    println!("T is {}", input);
}

fn main() {}
```

当你写`T: Display`的时候，它的意思是 "只有当T有Display时，才取T"。
而不是说: "我把Display给T".

对于生命期也是如此。当你在这里写 'a:

```rust
#[derive(Debug)]
struct City<'a> {
    name: &'a str,
    date_founded: u32,
}

fn main() {}
```

意思是 "如果`name`的生命期至少与`City`一样长，才接受`name`的输入"。
它的意思不是说: "我会让`name`的输入与`City`一样长寿"。


现在我们可以了解一下之前看到的`<'_>`。这被称为 "匿名生命期"，是使用引用的一个指标。例如，当你在实现结构时，Rust会向你建议使用。这里有一个几乎可以工作的结构体，但还不能工作：

```rust
    // ⚠️
struct Adventurer<'a> {
    name: &'a str,
    hit_points: u32,
}

impl Adventurer {
    fn take_damage(&mut self) {
        self.hit_points -= 20;
        println!("{} has {} hit points left!", self.name, self.hit_points);
    }
}

fn main() {}
```

所以我们对`struct`做了我们需要做的事情:首先我们说`name`来自于一个`&str`。这就意味着我们需要lifetime，所以我们给了它`<'a>`。然后我们必须对`struct`做同样的处理，以证明它们至少和这个生命期一样长。但是Rust却告诉我们要这样做:

```text
error[E0726]: implicit elided lifetime not allowed here
 --> src\main.rs:6:6
  |
6 | impl Adventurer {
  |      ^^^^^^^^^^- help: indicate the anonymous lifetime: `<'_>`
```

它想让我们加上那个匿名的生命期，以表明有一个引用被使用。所以如果我们这样写，它就会很高兴。

```rust
struct Adventurer<'a> {
    name: &'a str,
    hit_points: u32,
}

impl Adventurer<'_> {
    fn take_damage(&mut self) {
        self.hit_points -= 20;
        println!("{} has {} hit points left!", self.name, self.hit_points);
    }
}

fn main() {}
```

这个生命期是为了让你不必总是写诸如`impl<'a> Adventurer<'a>`这样的东西，因为结构已经显示了生命期。

在Rust中，生命期是很困难的，但这里有一些技巧可以避免对它们太过紧张。

- 你可以继续使用自有类型，使用克隆等，如果你想暂时避免它们。
- 很多时候，当编译器想要lifetime的时候，你只要在这里和那里写上<'a>就可以了。这只是一种 "别担心，我不会给你任何不够长寿的东西"的说法。
- 你可以每次只探索一下生命期。写一些拥有值的代码，然后把一个代码变成一个引用。编译器会开始抱怨，但也会给出一些建议。如果它变得太复杂，你可以撤销它，下次再试。

让我们用我们的代码来做这个，看看编译器怎么说。首先我们回去把生命期拿出来，同时实现`Display`。`Display`就打印`Adventurer`的名字。

```rust
// ⚠️
struct Adventurer {
    name: &str,
    hit_points: u32,
}

impl Adventurer {
    fn take_damage(&mut self) {
        self.hit_points -= 20;
        println!("{} has {} hit points left!", self.name, self.hit_points);
    }
}

impl std::fmt::Display for Adventurer {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{} has {} hit points.", self.name, self.hit_points)
        }
}

fn main() {}
```

第一个抱怨就是这个:

```text
error[E0106]: missing lifetime specifier
 --> src\main.rs:2:11
  |
2 |     name: &str,
  |           ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 | struct Adventurer<'a> {
2 |     name: &'a str,
  |
```

它建议怎么做:在Adventurer后面加上`<'a>`，以及`&'a str`。所以我们就这么做。

```rust
// ⚠️
struct Adventurer<'a> {
    name: &'a str,
    hit_points: u32,
}

impl Adventurer {
    fn take_damage(&mut self) {
        self.hit_points -= 20;
        println!("{} has {} hit points left!", self.name, self.hit_points);
    }
}

impl std::fmt::Display for Adventurer {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{} has {} hit points.", self.name, self.hit_points)
        }
}

fn main() {}
```

现在它对这些部分很满意，但对`impl`块感到奇怪。它希望我们提到它在使用引用。

```text
error[E0726]: implicit elided lifetime not allowed here
 --> src\main.rs:6:6
  |
6 | impl Adventurer {
  |      ^^^^^^^^^^- help: indicate the anonymous lifetime: `<'_>`

error[E0726]: implicit elided lifetime not allowed here
  --> src\main.rs:12:28
   |
12 | impl std::fmt::Display for Adventurer {
   |                            ^^^^^^^^^^- help: indicate the anonymous lifetime: `<'_>`
```

好了，我们将这些写进去......现在它工作了！现在我们可以创建一个`Adventurer`，然后用它做一些事情:

```rust
struct Adventurer<'a> {
    name: &'a str,
    hit_points: u32,
}

impl Adventurer<'_> {
    fn take_damage(&mut self) {
        self.hit_points -= 20;
        println!("{} has {} hit points left!", self.name, self.hit_points);
    }
}

impl std::fmt::Display for Adventurer<'_> {

        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{} has {} hit points.", self.name, self.hit_points)
        }
}

fn main() {
    let mut billy = Adventurer {
        name: "Billy",
        hit_points: 100_000,
    };
    println!("{}", billy);
    billy.take_damage();
}
```

这个将打印:

```text
Billy has 100000 hit points.
Billy has 99980 hit points left!
```

所以你可以看到，lifetimes往往只是编译器想要确定。而且它通常很聪明，几乎可以猜到你想要的生命期，只需要你告诉它，它就可以确定了。
