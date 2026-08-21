+++
title = "60-外部 crate"
date = 2026-08-21T12:46:00+08:00
weight = 61
type = "docs"
description = "外部 crate — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_59.html](https://dhghomon.github.io/easy_rust/Chapter_59.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 外部 crate

外部crate的意思是 "别人的crate"。

在本节中，你*差不多*需要安装Rust，但我们仍然可以只使用Playground。现在我们要学习如何导入别人写的crate。这在Rust中很重要，原因有二。

- 导入其他的crate很容易，并且...
- Rust标准库是相当小的。

这意味着，在Rust中，很多基本功能都需要用到外部Crate，这很正常。我们的想法是，如果使用外部Crate很方便，那么你可以选择最好的一个。也许一个人会为一个功能创建一个crate，然后其他人会创建一个更好的crate。

在本书中，我们只看最流行的crate，也就是每个使用Rust的人都知道的crate。

要开始学习外部Crate，我们将从最常见的Crate开始。`rand`.

## rand

你有没有注意到，我们还没有使用任何随机数？那是因为随机数不在标准库中。但是有很多crate "几乎是标准库"，因为大家都在使用它们。在任何情况下，带入一个 crate 是非常容易的。如果你的电脑上有Rust，有一个叫`Cargo.toml`的文件，里面有这些信息。`Cargo.toml`文件在你启动时是这样的。

```text
[package]
name = "rust_book"
version = "0.1.0"
authors = ["David MacLeod"]
edition = "2018"

# 更多键及其说明见 https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
```

现在，如果你想添加`rand` crate，在`crates.io`上搜索它，这是所有crate的去处。这将带你到`https://crates.io/crates/rand`。当你点击那个，你可以看到一个屏幕，上面写着`Cargo.toml   rand = "0.7.3"`。你所要做的就是在[dependencies]下添加这样的内容:

```text
[package]
name = "rust_book"
version = "0.1.0"
authors = ["David MacLeod"]
edition = "2018"

# 更多键及其说明见 https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
rand = "0.7.3"
```

然后Cargo会帮你完成剩下的工作。然后你就可以在`rand`文档网站上开始编写像[本例代码](https://docs.rs/rand/0.7.3/rand/)这样的代码。要想进入文档，你可以点击[crates.io上的页面](https://crates.io/crates/rand)中的`docs`按钮。

关于Cargo的介绍就到这里了:我们现在使用的还只是playground。幸运的是，playground已经安装了前100个crate。所以你还不需要写进`Cargo.toml`。在playground上，你可以想象，它有一个这样的长长的列表，有100个crate。


```text
[dependencies]
rand = "0.7.3"
some_other_crate = "0.1.0"
another_nice_crate = "1.7"
```


也就是说，如果要使用`rand`，你可以直接这样做:

```rust
use rand; // 表示整个 rand crate
          // 在本机上不能直接这样写；
          // 得先在 Cargo.toml 里声明

fn main() {
    for _ in 0..5 {
        let random_u16 = rand::random::<u16>();
        print!("{} ", random_u16);
    }
}
```

每次都会打印不同的`u16`号码，比如`42266 52873 56528 46927 6867`。



`rand`中的主要功能是`random`和`thread_rng`(rng的意思是 "随机数发生器")。而实际上如果你看`random`，它说:"这只是`thread_rng().gen()`的一个快捷方式"。所以其实是`thread_rng`基本做完了一切。

下面是一个简单的例子，从1到10的数字。为了得到这些数字，我们在1到11之间使用`.gen_range()`。

```rust
use rand::{thread_rng, Rng}; // 懒的话也可以 use rand::*;

fn main() {
    let mut number_maker = thread_rng();
    for _ in 0..5 {
        print!("{} ", number_maker.gen_range(1, 11));
    }
}
```

这将打印出`7 2 4 8 6`这样的东西。

用随机数我们可以做一些有趣的事情，比如为游戏创建角色。我们将使用`rand`和其他一些我们知道的东西来创建它们。在这个游戏中，我们的角色有六种状态，用一个d6来表示他们。d6是一个立方体，当你投掷它时，它能给出1、2、3、4、5或6。每个角色都会掷三次d6，所以每个统计都在3到18之间。

但是有时候如果你的角色有一些低的东西，比如3或4，那就不公平了。比如说你的力量是3，你就不能拿东西。所以还有一种方法是用d6四次。你掷四次，然后扔掉最低的数字。所以如果你掷3，3，1，6，那么你保留3，3，6=12。我们也会把这个方法做出来，所以游戏的主人可以决定。

这是我们简单的角色创建器。我们为数据统计创建了一个`Character`结构，甚至还实现了`Display`来按照我们想要的方式打印。

```rust
use rand::{thread_rng, Rng}; // 懒的话也可以 use rand::*;
use std::fmt; // 准备为角色实现 Display


struct Character {
    strength: u8,
    dexterity: u8,    // 意思是「身体敏捷」
    constitution: u8, // 意思是「体质/生命」
    intelligence: u8,
    wisdom: u8,
    charisma: u8, // 意思是「受欢迎程度」
}

fn three_die_six() -> u8 { // "die" 就是掷点用的骰子
    let mut generator = thread_rng(); // 创建随机数生成器
    let mut stat = 0; // 这是合计
    for _ in 0..3 {
        stat += generator.gen_range(1..=6); // 每次加上
    }
    stat // 返回合计
}

fn four_die_six() -> u8 {
    let mut generator = thread_rng();
    let mut results = vec![]; // 先把数字放进 vec
    for _ in 0..4 {
        results.push(generator.gen_range(1..=6));
    }
    results.sort(); // 现在像 [4, 3, 2, 6] 会变成 [2, 3, 4, 6]
    results.remove(0); // 现在是 [3, 4, 6]
    results.iter().sum() // 返回这个结果
}

enum Dice {
    Three,
    Four
}

impl Character {
    fn new(dice: Dice) -> Self { // true 用三颗骰，false 用四颗
        match dice {
            Dice::Three => Self {
                strength: three_die_six(),
                dexterity: three_die_six(),
                constitution: three_die_six(),
                intelligence: three_die_six(),
                wisdom: three_die_six(),
                charisma: three_die_six(),
            },
            Dice::Four => Self {
                strength: four_die_six(),
                dexterity: four_die_six(),
                constitution: four_die_six(),
                intelligence: four_die_six(),
                wisdom: four_die_six(),
                charisma: four_die_six(),
            },
        }
    }
    fn display(&self) { // 因为下面实现了 Display，所以可以这样做
        println!("{}", self);
        println!();
    }
}

impl fmt::Display for Character { // 照着 https://doc.rust-lang.org/std/fmt/trait.Display.html 的写法稍改即可
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Your character has these stats:
strength: {}
dexterity: {}
constitution: {}
intelligence: {}
wisdom: {}
charisma: {}",
            self.strength,
            self.dexterity,
            self.constitution,
            self.intelligence,
            self.wisdom,
            self.charisma
        )
    }
}



fn main() {
    let weak_billy = Character::new(Dice::Three);
    let strong_billy = Character::new(Dice::Four);
    weak_billy.display();
    strong_billy.display();
}
```

它会打印出这样的东西。

```rust
Your character has these stats:
strength: 9
dexterity: 15
constitution: 15
intelligence: 8
wisdom: 11
charisma: 9

Your character has these stats:
strength: 9
dexterity: 13
constitution: 14
intelligence: 16
wisdom: 16
charisma: 10
```

有四个骰子的角色通常在大多数事情上都会好一点。


## rayon

`rayon` 是一个流行的crate，它可以让你加快 Rust 代码的速度。它之所以受欢迎，是因为它无需像 `thread::spawn` 这样的东西就能创建线程。换句话说，它之所以受欢迎是因为它既有效又容易编写。比如说

- `.iter()`, `.iter_mut()`, `into_iter()`在rayon中是这样写的:
- `.par_iter()`, `.par_iter_mut()`, `par_into_iter()`. 所以你只要加上`par_`，你的代码就会变得快很多。(par的意思是 "并行")

其他方法也一样:`.chars()`就是`.par_chars()`，以此类推。

这里举个例子，一段简单的代码，却让计算机做了很多工作。
```rust
fn main() {
    let mut my_vec = vec![0; 200_000];
    my_vec.iter_mut().enumerate().for_each(|(index, number)| *number+=index+1);
    println!("{:?}", &my_vec[5000..5005]);
}
```

它创建了一个有20万项的向量:每一项都是0，然后调用`.enumerate()`来获取每个数字的索引，并将0改为索引号。它的打印时间太长，所以我们只打印5000到5004项。这在Rust中还是非常快的，但如果你愿意，你可以用Rayon让它更快。代码几乎是一样的。

```rust
use rayon::prelude::*; // 导入 rayon

fn main() {
    let mut my_vec = vec![0; 200_000];
    my_vec.par_iter_mut().enumerate().for_each(|(index, number)| *number+=index+1); // 在 iter_mut 前加 par_
    println!("{:?}", &my_vec[5000..5005]);
}
```

就这样了。`rayon`还有很多其他的方法来定制你想做的事情，但最简单的就是 "添加`_par`，让你的程序更快"。

## serde

`serde`是一个流行的crate，它可以在JSON、YAML等格式间相互转换。最常见的使用方法是通过创建一个`struct`，上面有两个属性。[它看起来是这样的](https://serde.rs/)。

```rust
#[derive(Serialize, Deserialize, Debug)]
struct Point {
    x: i32,
    y: i32,
}
```

`Serialize`和`Deserialize`trait是使转换变得简单的原因。(这也是`serde`这个名字的由来)如果你的结构体上有这两个trait，那么你只需要调用一个方法就可以把它转化为JSON或其他任何东西。

## regex

[regex](https://crates.io/crates/regex) crate 可以让你使用 [正则表达式](https://en.wikipedia.org/wiki/Regular_expression) 搜索文本。有了它，你可以通过一次搜索得到诸如 `colour`, `color`, `colours` 和 `colors` 的匹配信息。正则表达式是另一门语言，如果你想使用它们，也必须学会。

## chrono

[chrono](https://crates.io/crates/chrono)是为那些需要更多时间功能的人准备的主要crate。我们现在来看一下标准库，它有时间的功能，但是如果你需要更多的功能，那么这个crate是一个不错的选择。
