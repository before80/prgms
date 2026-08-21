+++
title = "57-Deref 和 DerefMut"
date = 2026-08-21T12:46:00+08:00
weight = 58
type = "docs"
description = "Deref 和 DerefMut — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_56.html](https://dhghomon.github.io/easy_rust/Chapter_56.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Deref 和 DerefMut

`Deref`是让你用`*`来解引用某些东西的trait。我们知道，一个引用和一个值是不一样的。

```rust
// ⚠️
fn main() {
    let value = 7; // 这是 i32
    let reference = &7; // 这是 &i32
    println!("{}", value == reference);
}
```

而Rust连`false`都不给，因为它甚至不会比较两者。

```text
error[E0277]: can't compare `{integer}` with `&{integer}`
 --> src\main.rs:4:26
  |
4 |     println!("{}", value == reference);
  |                          ^^ no implementation for `{integer} == &{integer}`
```

当然，这里的解法是使用`*`。所以这将打印出`true`。

```rust
fn main() {
    let value = 7;
    let reference = &7;
    println!("{}", value == *reference);
}
```


现在让我们想象一下一个简单的类型，它只是容纳一个数字。它就像一个`Box`，我们有一些想法为它提供一些额外的功能。但如果我们只是给它一个数字，
 它就不能做那么多了。

我们不能像使用`Box`那样使用`*`:

```rust
// ⚠️
struct HoldsANumber(u8);

fn main() {
    let my_number = HoldsANumber(20);
    println!("{}", *my_number + 20);
}
```

错误信息是:

```text
error[E0614]: type `HoldsANumber` cannot be dereferenced
  --> src\main.rs:24:22
   |
24 |     println!("{:?}", *my_number + 20);
```

我们当然可以做到这一点。`println!("{:?}", my_number.0 + 20);`. 但是这样的话，我们就是在20的基础上再单独加一个`u8`。如果我们能把它们加在一起就更好了。`cannot be dereferenced`这个消息给了我们一个线索:我们需要实现`Deref`。实现`Deref`的简单东西有时被称为 "智能指针"。一个智能指针可以指向它的元素，有它的信息，并且可以使用它的方法。因为现在我们可以添加`my_number.0`，这是一个`u8`，但我们不能用`HoldsANumber`做其他的事情:到目前为止，它只有`Debug`。

有趣的是:`String`其实是`&str`的智能指针，`Vec`是数组(或其他类型)的智能指针。所以我们其实从一开始就在使用智能指针。

实现`Deref`并不难，标准库中的例子也很简单。[下面是标准库中的示例代码](https://doc.rust-lang.org/std/ops/trait.Deref.html)。

```rust
use std::ops::Deref;

struct DerefExample<T> {
    value: T
}

impl<T> Deref for DerefExample<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.value
    }
}

fn main() {
    let x = DerefExample { value: 'a' };
    assert_eq!('a', *x);
}
```


所以我们按照这个来，现在我们的`Deref`是这样的。

```rust
// 🚧
impl Deref for HoldsANumber {
    type Target = u8; // 记住，这是「关联类型」：一起配套的类型。
                      // Target = 必须写成你想返回的正确类型

    fn deref(&self) -> &Self::Target { // 使用 * 时 Rust 会调用 .deref()。我们把 Target 定为 u8，所以很好理解
        &self.0   // 选 &self.0 是因为这是元组结构体。具名字段结构体大概会写成 "&self.number"
    }
}
```

所以现在我们可以用`*`来做:

```rust
use std::ops::Deref;
#[derive(Debug)]
struct HoldsANumber(u8);

impl Deref for HoldsANumber {
    type Target = u8;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let my_number = HoldsANumber(20);
    println!("{:?}", *my_number + 20);
}
```

所以，这样就可以打印出`40`，我们不需要写`my_number.0`。这意味着我们得到了 `u8` 的方法，我们可以为 `HoldsANumber` 写出我们自己的方法。我们将添加自己的简单方法，并使用我们从`u8`中得到的另一个方法，称为`.checked_sub()`。`.checked_sub()`方法是一个安全的减法，它能返回一个`Option`。如果它能做减法，那么它就会在`Some`里面给你，如果它不能做减法，那么它就会给出一个`None`。记住，`u8`不能是负数，所以还是`.checked_sub()`比较安全，这样就不会崩溃了。

```rust
use std::ops::Deref;

struct HoldsANumber(u8);

impl HoldsANumber {
    fn prints_the_number_times_two(&self) {
        println!("{}", self.0 * 2);
    }
}

impl Deref for HoldsANumber {
    type Target = u8;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let my_number = HoldsANumber(20);
    println!("{:?}", my_number.checked_sub(100)); // 这个方法来自 u8
    my_number.prints_the_number_times_two(); // 这是我们自己的方法
}
```

这个打印:

```text
None
40
```

我们也可以实现`DerefMut`，这样我们就可以通过`*`来改变数值。它看起来几乎是一样的。在实现`DerefMut`之前，你需要先实现`Deref`。

```rust
use std::ops::{Deref, DerefMut};

struct HoldsANumber(u8);

impl HoldsANumber {
    fn prints_the_number_times_two(&self) {
        println!("{}", self.0 * 2);
    }
}

impl Deref for HoldsANumber {
    type Target = u8;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for HoldsANumber { // 这里不用再写 type Target = u8;，因为 Deref 已经告诉过了
    fn deref_mut(&mut self) -> &mut Self::Target { // 其余一样，只是到处都是 mut
        &mut self.0
    }
}

fn main() {
    let mut my_number = HoldsANumber(20);
    *my_number = 30; // DerefMut 让我们可以这样做
    println!("{:?}", my_number.checked_sub(100));
    my_number.prints_the_number_times_two();
}
```

所以你可以看到，`Deref`给你的类型提供了强大的力量。

这也是为什么标准库说:`Deref should only be implemented for smart pointers to avoid confusion`。这是因为对于一个复杂的类型，你可以用 `Deref` 做一些奇怪的事情。让我们想象一个非常混乱的例子来理解它们的含义。我们将从一个游戏的 `Character` 结构开始。一个新的`Character`需要一些数据，比如智力和力量。所以这里是我们的第一个角色。

```rust
struct Character {
    name: String,
    strength: u8,
    dexterity: u8,
    health: u8,
    intelligence: u8,
    wisdom: u8,
    charm: u8,
    hit_points: i8,
    alignment: Alignment,
}

impl Character {
    fn new(
        name: String,
        strength: u8,
        dexterity: u8,
        health: u8,
        intelligence: u8,
        wisdom: u8,
        charm: u8,
        hit_points: i8,
        alignment: Alignment,
    ) -> Self {
        Self {
            name,
            strength,
            dexterity,
            health,
            intelligence,
            wisdom,
            charm,
            hit_points,
            alignment,
        }
    }
}

enum Alignment {
    Good,
    Neutral,
    Evil,
}

fn main() {
    let billy = Character::new("Billy".to_string(), 9, 8, 7, 10, 19, 19, 5, Alignment::Good);
}
```

现在让我们想象一下，我们要把人物的hit points放在一个大的vec里。也许我们会把怪物数据也放进去，把它放在一起。由于 `hit_points` 是一个 `i8`，我们实现了 `Deref`，所以我们可以对它进行各种计算。但是看看现在我们的`main()`函数中，它看起来多么奇怪。


```rust
use std::ops::Deref;

// 直到 enum Alignment 之后，其他代码都一样
struct Character {
    name: String,
    strength: u8,
    dexterity: u8,
    health: u8,
    intelligence: u8,
    wisdom: u8,
    charm: u8,
    hit_points: i8,
    alignment: Alignment,
}

impl Character {
    fn new(
        name: String,
        strength: u8,
        dexterity: u8,
        health: u8,
        intelligence: u8,
        wisdom: u8,
        charm: u8,
        hit_points: i8,
        alignment: Alignment,
    ) -> Self {
        Self {
            name,
            strength,
            dexterity,
            health,
            intelligence,
            wisdom,
            charm,
            hit_points,
            alignment,
        }
    }
}

enum Alignment {
    Good,
    Neutral,
    Evil,
}

impl Deref for Character { // 为 Character 实现 Deref。现在可以随便做整数运算了！
    type Target = i8;

    fn deref(&self) -> &Self::Target {
        &self.hit_points
    }
}



fn main() {
    let billy = Character::new("Billy".to_string(), 9, 8, 7, 10, 19, 19, 5, Alignment::Good); // 创建两个角色：billy 和 brandy
    let brandy = Character::new("Brandy".to_string(), 9, 8, 7, 10, 19, 19, 5, Alignment::Good);

    let mut hit_points_vec = vec![]; // 生命值数据放这里
    hit_points_vec.push(*billy);     // 推进 *billy？
    hit_points_vec.push(*brandy);    // 推进 *brandy？

    println!("{:?}", hit_points_vec);
}
```

这只打印了`[5, 5]`。我们的代码现在让人读起来感觉非常奇怪。我们可以在`main()`上面看到`Deref`，然后弄清楚`*billy`的意思是`i8`，但是如果有很多代码呢？可能我们的代码有2000行，突然要弄清楚为什么要`.push()` `*billy`。`Character`当然不仅仅是`i8`的智能指针。

当然，写`hit_points_vec.push(*billy)`并不违法，但这让代码看起来非常奇怪。也许一个简单的`.get_hp()`方法会好得多，或者另一个存放角色的结构体。然后你可以迭代并推送每个角色的 `hit_points`。`Deref`提供了很多功能，但最好确保代码的逻辑性。
