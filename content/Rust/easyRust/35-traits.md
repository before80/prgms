+++
title = "35-Trait（特性）"
date = 2026-08-21T12:46:00+08:00
weight = 36
type = "docs"
description = "Trait（特性） — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_34.html](https://dhghomon.github.io/easy_rust/Chapter_34.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Trait（特性）

我们以前见过trait:`Debug`、`Copy`、`Clone`都是trait。要给一个类型一个trait，就必须实现它。因为`Debug`和其他的trait都很常见，所以我们有自动实现的属性。这就是当你写下`#[derive(Debug)]`所发生的事情:你自动实现了`Debug`。

```rust
#[derive(Debug)]
struct MyStruct {
    number: usize,
}

fn main() {}
```

但是其他的特性就比较困难了，所以需要用`impl`手动实现。例如，`Add`(在`std::ops::Add`处找到)是用来累加两个东西的。但是Rust并不知道你到底要怎么累加，所以你必须告诉它。

```rust
struct ThingsToAdd {
    first_thing: u32,
    second_thing: f32,
}

fn main() {}
```

我们可以累加`first_thing`和`second_thing`，但我们需要提供更多信息。也许我们想要一个`f32`，所以像这样:

```rust
// 🚧
let result = self.second_thing + self.first_thing as f32
```

但也许我们想要一个整数，所以像这样:

```rust
// 🚧
let result = self.second_thing as u32 + self.first_thing
```

或者我们想把`self.first_thing`放在`self.second_thing`旁边，这样加。所以如果我们把55加到33.4，我们要看到的是5533.4，而不是88.4。

所以首先我们看一下如何创建一个trait。关于`trait`，要记住的重要一点是，它们是关于行为的。要创建一个trait，写下单词`trait`，然后创建一些函数。

```rust
struct Animal { // 一个简单的结构体——Animal 只有名字
    name: String,
}

trait Dog { // Dog trait 提供一些功能
    fn bark(&self) { // 它可以叫
        println!("Woof woof!");
    }
    fn run(&self) { // 也可以跑
        println!("The dog is running!");
    }
}

impl Dog for Animal {} // 现在 Animal 拥有 Dog trait

fn main() {
    let rover = Animal {
        name: "Rover".to_string(),
    };

    rover.bark(); // 现在 Animal 可以使用 bark()
    rover.run();  // 也可以使用 run()
}
```

这个是可以的，但是我们不想打印 "狗在跑"。如果你想的话，你可以改变`trait`给你的方法，但你必须有相同的签名。这意味着它需要接受同样的东西，并返回同样的东西。例如，我们可以改变 `.run()` 的方法，但我们必须遵循签名。签名说

```rust
// 🚧
fn run(&self) {
    println!("The dog is running!");
}
```

`fn run(&self)`的意思是 "fn `run()`以`&self`为参数，不返回任何内容"。所以你不能这样做:

```rust
fn run(&self) -> i32 { // ⚠️
    5
}
```

Rust会说。

```text
   = note: expected fn pointer `fn(&Animal)`
              found fn pointer `fn(&Animal) -> i32`
```

但我们可以做到这一点。

```rust
struct Animal { // 一个简单的结构体——Animal 只有名字
    name: String,
}

trait Dog { // Dog trait 提供一些功能
    fn bark(&self) { // 它可以叫
        println!("Woof woof!");
    }
    fn run(&self) { // 也可以跑
        println!("The dog is running!");
    }
}

impl Dog for Animal {
    fn run(&self) {
        println!("{} is running!", self.name);
    }
}

fn main() {
    let rover = Animal {
        name: "Rover".to_string(),
    };

    rover.bark(); // 现在 Animal 可以使用 bark()
    rover.run();  // 也可以使用 run()
}
```

现在它打印的是 `Rover is running!`。这是好的，因为我们返回的是 `()`，或者说什么都没有，这就是trait所说的。


当你写一个trait的时候，你可以直接写函数签名，但如果你这样做，用户将不得不写函数实现。我们来试试。现在我们把`bark()`和`run()`改成只说`fn bark(&self);`和`fn run(&self);`。这不是一个完整的函数实现，所以必须由用户来写。

```rust
struct Animal {
    name: String,
}

trait Dog {
    fn bark(&self); // bark() 需要 &self，不返回任何值
    fn run(&self); // run() 需要 &self，不返回任何值。
                   // 所以现在必须自己实现它们。
}

impl Dog for Animal {
    fn bark(&self) {
        println!("{}, stop barking!!", self.name);
    }
    fn run(&self) {
        println!("{} is running!", self.name);
    }
}

fn main() {
    let rover = Animal {
        name: "Rover".to_string(),
    };

    rover.bark();
    rover.run();
}
```

所以，当你创建一个trait时，你必须思考:"我应该写哪些功能？而用户应该写哪些函数？" 如果你认为用户每次使用函数的方式应该是一样的，那么就把函数写出来。如果你认为用户会以不同的方式使用，那就写出函数签名即可。

所以，让我们尝试为我们的struct实现Display特性。首先我们将创建一个简单的结构体:

```rust
struct Cat {
    name: String,
    age: u8,
}

fn main() {
    let mr_mantle = Cat {
        name: "Reggie Mantle".to_string(),
        age: 4,
    };
}
```

现在我们要打印`mr_mantle`。调试很容易得出。

```rust
#[derive(Debug)]
struct Cat {
    name: String,
    age: u8,
}

fn main() {
    let mr_mantle = Cat {
        name: "Reggie Mantle".to_string(),
        age: 4,
    };

    println!("Mr. Mantle is a {:?}", mr_mantle);
}
```

但Debug打印不是最漂亮的方式，因为它看起来是这样的:

```text
Mr. Mantle is a Cat { name: "Reggie Mantle", age: 4 }
```

因此，如果我们想要更好的打印，就需要实现`Display`为`Cat`。在[https://doc.rust-lang.org/std/fmt/trait.Display.html](https://doc.rust-lang.org/std/fmt/trait.Display.html)上我们可以看到Display的信息，还有一个例子。它说

```rust
use std::fmt;

struct Position {
    longitude: f32,
    latitude: f32,
}

impl fmt::Display for Position {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.longitude, self.latitude)
    }
}

fn main() {}
```

有些部分我们还不明白，比如`<'_>`和`f`在做什么。但我们理解`Position`结构体:它只是两个`f32`。我们也明白，`self.longitude`和`self.latitude`是结构体中的字段。所以，也许我们的结构体就可以用这个代码，用`self.name`和`self.age`。另外，`write!`看起来很像`println!`，所以很熟悉。所以我们这样写。

```rust
use std::fmt;

struct Cat {
    name: String,
    age: u8,
}

impl fmt::Display for Cat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} is a cat who is {} years old.", self.name, self.age)
    }
}

fn main() {}
```

让我们添加一个`fn main()`。现在我们的代码是这样的。

```rust
use std::fmt;

struct Cat {
    name: String,
    age: u8,
}

impl fmt::Display for Cat {
  fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
      write!(f, "{} is a cat who is {} years old.", self.name, self.age)
  }
}

fn main() {
    let mr_mantle = Cat {
        name: "Reggie Mantle".to_string(),
        age: 4,
    };

    println!("{}", mr_mantle);
}
```

成功了! 现在，当我们使用`{}`打印时，我们得到`Reggie Mantle is a cat who is 4 years old.`。这看起来好多了。


顺便说一下，如果你实现了`Display`，那么你就可以免费得到`ToString`的特性。这是因为你使用`format!`宏来实现`.fmt()`函数，这让你可以用`.to_string()`来创建一个`String`。所以我们可以做这样的事情，我们把`reggie_mantle`传给一个想要`String`的函数，或者其他任何东西。

```rust
use std::fmt;
struct Cat {
    name: String,
    age: u8,
}

impl fmt::Display for Cat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} is a cat who is {} years old.", self.name, self.age)
    }
}

fn print_cats(pet: String) {
    println!("{}", pet);
}

fn main() {
    let mr_mantle = Cat {
        name: "Reggie Mantle".to_string(),
        age: 4,
    };

    print_cats(mr_mantle.to_string()); // 在这里把它变成 String
    println!("Mr. Mantle's String is {} letters long.", mr_mantle.to_string().chars().count()); // 转成字符再计数
}
```

这个打印:

```text
Reggie Mantle is a cat who is 4 years old.
Mr. Mantle's String is 42 letters long.
```




关于trait，要记住的是，它们是关于某些东西的行为。你的`struct`是如何行动的？它能做什么？这就是trait的作用。如果你想想我们到目前为止所看到的一些trait，它们都是关于行为的:`Copy`是一个类型可以做的事情。`Display`也是一个类型能做的事情。`ToString`是另一个trait，它也是一个类型可以做的事情:它可以变化成一个`String`。在我们的 `Dog` trait中，*Dog*这个词并不意味着你能做的事情，但它给出了一些让它做事情的方法。
 你也可以为 `struct Poodle` 或 `struct Beagle` 实现它，它们都会得到 `Dog` 方法。


让我们再看一个与单纯行为联系更紧密的例子。我们将想象一个有一些简单角色的幻想游戏。一个是`Monster`，另外两个是`Wizard`和`Ranger`。`Monster`只是有`health`，所以我们可以攻击它，其他两个还没有什么。但是我们做了两个trait。一个叫`FightClose`，让你近身作战。另一个是`FightFromDistance`，让你在远处战斗。只有`Ranger`可以使用`FightFromDistance`。下面是它的样子:

```rust
struct Monster {
    health: i32,
}

struct Wizard {}
struct Ranger {}

trait FightClose {
    fn attack_with_sword(&self, opponent: &mut Monster) {
        opponent.health -= 10;
        println!(
            "You attack with your sword. Your opponent now has {} health left.",
            opponent.health
        );
    }
    fn attack_with_hand(&self, opponent: &mut Monster) {
        opponent.health -= 2;
        println!(
            "You attack with your hand. Your opponent now has {} health left.",
            opponent.health
        );
    }
}
impl FightClose for Wizard {}
impl FightClose for Ranger {}

trait FightFromDistance {
    fn attack_with_bow(&self, opponent: &mut Monster, distance: u32) {
        if distance < 10 {
            opponent.health -= 10;
            println!(
                "You attack with your bow. Your opponent now has {} health left.",
                opponent.health
            );
        }
    }
    fn attack_with_rock(&self, opponent: &mut Monster, distance: u32) {
        if distance < 3 {
            opponent.health -= 4;
        }
        println!(
            "You attack with your rock. Your opponent now has {} health left.",
            opponent.health
        );
    }
}
impl FightFromDistance for Ranger {}

fn main() {
    let radagast = Wizard {};
    let aragorn = Ranger {};

    let mut uruk_hai = Monster { health: 40 };

    radagast.attack_with_sword(&mut uruk_hai);
    aragorn.attack_with_bow(&mut uruk_hai, 8);
}
```

这个打印:

```text
You attack with your sword. Your opponent now has 30 health left.
You attack with your bow. Your opponent now has 20 health left.
```

我们在trait里面一直传递`self`，但是我们现在不能用它做什么。那是因为 Rust 不知道什么类型会使用它。它可能是一个 `Wizard`，也可能是一个 `Ranger`，也可能是一个叫做 `Toefocfgetobjtnode` 的新结构，或者其他任何东西。为了让`self`具有一定的功能，我们可以在trait中添加必要的trait。比如说，如果我们想用`{:?}`打印，那么我们就需要`Debug`。你只要把它写在`:`(冒号)后面，就可以把它添加到trait中。现在我们的代码是这样的。


```rust
struct Monster {
    health: i32,
}

#[derive(Debug)] // 现在 Wizard 有 Debug
struct Wizard {
    health: i32, // 现在 Wizard 有 health
}
#[derive(Debug)] // Ranger 也一样
struct Ranger {
    health: i32, // Ranger 也一样
}

trait FightClose: std::fmt::Debug { // 现在类型需要 Debug 才能使用 FightClose
    fn attack_with_sword(&self, opponent: &mut Monster) {
        opponent.health -= 10;
        println!(
            "You attack with your sword. Your opponent now has {} health left. You are now at: {:?}", // 有了 Debug，现在可以用 {:?} 打印 self
            opponent.health, &self
        );
    }
    fn attack_with_hand(&self, opponent: &mut Monster) {
        opponent.health -= 2;
        println!(
            "You attack with your hand. Your opponent now has {} health left.  You are now at: {:?}",
            opponent.health, &self
        );
    }
}
impl FightClose for Wizard {}
impl FightClose for Ranger {}

trait FightFromDistance: std::fmt::Debug { // 也可以写成 trait FightFromDistance: FightClose，因为 FightClose 需要 Debug
    fn attack_with_bow(&self, opponent: &mut Monster, distance: u32) {
        if distance < 10 {
            opponent.health -= 10;
            println!(
                "You attack with your bow. Your opponent now has {} health left.  You are now at: {:?}",
                opponent.health, self
            );
        }
    }
    fn attack_with_rock(&self, opponent: &mut Monster, distance: u32) {
        if distance < 3 {
            opponent.health -= 4;
        }
        println!(
            "You attack with your rock. Your opponent now has {} health left.  You are now at: {:?}",
            opponent.health, self
        );
    }
}
impl FightFromDistance for Ranger {}

fn main() {
    let radagast = Wizard { health: 60 };
    let aragorn = Ranger { health: 80 };

    let mut uruk_hai = Monster { health: 40 };

    radagast.attack_with_sword(&mut uruk_hai);
    aragorn.attack_with_bow(&mut uruk_hai, 8);
}
```

现在这个打印:

```text
You attack with your sword. Your opponent now has 30 health left. You are now at: Wizard { health: 60 }
You attack with your bow. Your opponent now has 20 health left.  You are now at: Ranger { health: 80 }
```

在真实的游戏中，可能最好为每个类型重写这个，因为`You are now at: Wizard { health: 60 }`看起来有点可笑。这也是为什么trait里面的方法通常很简单，因为你不知道什么类型会使用它。例如，你不能写出 `self.0 += 10` 这样的东西。但是这个例子表明，我们可以在我们正在写的trait里面使用其他的trait。当我们这样做的时候，我们会得到一些我们可以使用的方法。



另外一种使用trait的方式是使用所谓的`trait bounds`。意思是 "通过一个trait进行限制"。trait限制很简单，因为一个trait实际上不需要任何方法，或者说根本不需要任何东西。让我们用类似但不同的东西重写我们的代码。这次我们的trait没有任何方法，但我们有其他需要trait使用的函数。

```rust
use std::fmt::Debug;  // 这样就不用每次都写 std::fmt::Debug 了

struct Monster {
    health: i32,
}

#[derive(Debug)]
struct Wizard {
    health: i32,
}
#[derive(Debug)]
struct Ranger {
    health: i32,
}

trait Magic{} // 这些 trait 都没有方法，只是用作 trait bound
trait FightClose {}
trait FightFromDistance {}

impl FightClose for Ranger{} // 每个类型都获得 FightClose，
impl FightClose for Wizard {}
impl FightFromDistance for Ranger{} // 但只有 Ranger 获得 FightFromDistance
impl Magic for Wizard{}  // 只有 Wizard 获得 Magic

fn attack_with_bow<T: FightFromDistance + Debug>(character: &T, opponent: &mut Monster, distance: u32) {
    if distance < 10 {
        opponent.health -= 10;
        println!(
            "You attack with your bow. Your opponent now has {} health left.  You are now at: {:?}",
            opponent.health, character
        );
    }
}

fn attack_with_sword<T: FightClose + Debug>(character: &T, opponent: &mut Monster) {
    opponent.health -= 10;
    println!(
        "You attack with your sword. Your opponent now has {} health left. You are now at: {:?}",
        opponent.health, character
    );
}

fn fireball<T: Magic + Debug>(character: &T, opponent: &mut Monster, distance: u32) {
    if distance < 15 {
        opponent.health -= 20;
        println!("You raise your hands and cast a fireball! Your opponent now has {} health left. You are now at: {:?}",
    opponent.health, character);
    }
}

fn main() {
    let radagast = Wizard { health: 60 };
    let aragorn = Ranger { health: 80 };

    let mut uruk_hai = Monster { health: 40 };

    attack_with_sword(&radagast, &mut uruk_hai);
    attack_with_bow(&aragorn, &mut uruk_hai, 8);
    fireball(&radagast, &mut uruk_hai, 8);
}
```

这个打印出来的东西几乎是一样的。

```text
You attack with your sword. Your opponent now has 30 health left. You are now at: Wizard { health: 60 }
You attack with your bow. Your opponent now has 20 health left.  You are now at: Ranger { health: 80 }
You raise your hands and cast a fireball! Your opponent now has 0 health left. You are now at: Wizard { health: 60 }
```

所以你可以看到，当你使用traits时，有很多方法可以做同样的事情。这一切都取决于什么对你正在编写的程序最有意义。

现在让我们来看看如何实现一些在Rust中使用的主要trait。

## From trait

*From*是一个非常方便的trait，你知道这一点，因为你已经看到了很多。使用*From*，你可以从一个`&str`创建一个`String`，你也可以用许多其他类型创建多种类型。例如，Vec使用*From*来创建以下类型:

```text
From<&'_ [T]>
From<&'_ mut [T]>
From<&'_ str>
From<&'a Vec<T>>
From<[T; N]>
From<BinaryHeap<T>>
From<Box<[T]>>
From<CString>
From<Cow<'a, [T]>>
From<String>
From<Vec<NonZeroU8>>
From<Vec<T>>
From<VecDeque<T>>
```

这里有很多`Vec::from()`我们还没有用过。我们来做几个，看看会怎么样:

```rust
use std::fmt::Display; // 我们会写泛型函数来打印，所以需要 Display

fn print_vec<T: Display>(input: &Vec<T>) { // 接受任意 Vec<T>，只要 T 实现了 Display
    for item in input {
        print!("{} ", item);
    }
    println!();
}

fn main() {

    let array_vec = Vec::from([8, 9, 10]); // 试试从数组创建
    print_vec(&array_vec);

    let str_vec = Vec::from("What kind of vec will I be?"); // 从 &str 创建？这会很有意思
    print_vec(&str_vec);

    let string_vec = Vec::from("What kind of vec will a String be?".to_string()); // 也可以从 String 创建
    print_vec(&string_vec);
}
```

它打印的内容如下。

```text
8 9 10
87 104 97 116 32 107 105 110 100 32 111 102 32 118 101 99 32 119 105 108 108 32 73 32 98 101 63
87 104 97 116 32 107 105 110 100 32 111 102 32 118 101 99 32 119 105 108 108 32 97 32 83 116 114 105 110 103 32 98 101 63
```

如果从类型上看，第二个和第三个向量是`Vec<u8>`，也就是`&str`和`String`的字节。所以你可以看到`From`是非常灵活的，用的也很多。我们用自己的类型来试试。

我们将创建两个结构体，然后为其中一个结构体实现`From`。一个结构体将是`City`，另一个结构体将是`Country`。我们希望能够做到这一点。`let country_name = Country::from(vector_of_cities)`.

它看起来是这样的:

```rust
#[derive(Debug)] // 这样就能打印 City
struct City {
    name: String,
    population: u32,
}

impl City {
    fn new(name: &str, population: u32) -> Self { // 只是一个 new 函数
        Self {
            name: name.to_string(),
            population,
        }
    }
}
#[derive(Debug)] // Country 也需要能打印
struct Country {
    cities: Vec<City>, // 城市放在这里
}

impl From<Vec<City>> for Country { // 注意：不必写 From<City>，也可以写
                                   // From<Vec<City>>。所以也可以为不是我们创建的类型
                                   // 实现 From
    fn from(cities: Vec<City>) -> Self {
        Self { cities }
    }
}

impl Country {
    fn print_cities(&self) { // 打印 Country 中城市的函数
        for city in &self.cities {
            // 加 &，因为 Vec<City> 没有 Copy
            println!("{:?} has a population of {:?}.", city.name, city.population);
        }
    }
}

fn main() {
    let helsinki = City::new("Helsinki", 631_695);
    let turku = City::new("Turku", 186_756);

    let finland_cities = vec![helsinki, turku]; // 这就是 Vec<City>
    let finland = Country::from(finland_cities); // 现在可以使用 From 了

    finland.print_cities();
}
```

这个将打印:

```text
"Helsinki" has a population of 631695.
"Turku" has a population of 186756.
```

你可以看到，`From`很容易从你没有创建的类型中实现，比如`Vec`、`i32`等等。这里还有一个例子，我们创建一个有两个向量的向量。第一个向量存放偶数，第二个向量存放奇数。对于`From`，你可以给它一个`i32`的向量，它会把它变成`Vec<Vec<i32>>`:一个容纳`i32`的向量。

```rust
use std::convert::From;

struct EvenOddVec(Vec<Vec<i32>>);

impl From<Vec<i32>> for EvenOddVec {
    fn from(input: Vec<i32>) -> Self {
        let mut even_odd_vec: Vec<Vec<i32>> = vec![vec![], vec![]]; // 里面有两个空 Vec 的 Vec
                                                                    // 这是返回值，但先要填满它
        for item in input {
            if item % 2 == 0 {
                even_odd_vec[0].push(item);
            } else {
                even_odd_vec[1].push(item);
            }
        }
        Self(even_odd_vec) // 完成了，作为 Self 返回（Self = EvenOddVec）
    }
}

fn main() {
    let bunch_of_numbers = vec![8, 7, -1, 3, 222, 9787, -47, 77, 0, 55, 7, 8];
    let new_vec = EvenOddVec::from(bunch_of_numbers);

    println!("Even numbers: {:?}\nOdd numbers: {:?}", new_vec.0[0], new_vec.0[1]);
}
```

这个打印:

```text
Even numbers: [8, 222, 0, 8]
Odd numbers: [7, -1, 3, 9787, -47, 77, 55, 7]
```

像 `EvenOddVec` 这样的类型可能最好是通用 `T`，这样我们就可以使用许多数字类型。如果你想练习的话，你可以试着把这个例子做成通用的。

## 在函数中使用字符串和&str

有时你想让一个函数可以同时接受 `String` 和 `&str`。你可以通过泛型和 `AsRef` 特性来实现这一点。`AsRef` 用于从一个类型向另一个类型提供引用。如果你看看 `String` 的文档，你可以看到它对许多类型都有 `AsRef`。

[https://doc.rust-lang.org/std/string/struct.String.html](https://doc.rust-lang.org/std/string/struct.String.html)

下面是它们的一些函数签名。

`AsRef<str>`:

```rust
// 🚧
impl AsRef<str> for String

fn as_ref(&self) -> &str
```

`AsRef<[u8]>`:

```rust
// 🚧
impl AsRef<[u8]> for String

fn as_ref(&self) -> &[u8]
```

`AsRef<OsStr>`:

```rust
// 🚧
impl AsRef<OsStr> for String

fn as_ref(&self) -> &OsStr
```

你可以看到，它需要`&self`，并给出另一个类型的引用。这意味着，如果你有一个通用类型T，你可以说它需要`AsRef<str>`。如果你这样做，它将能够使用一个`&str`和一个`String`。

我们先说说泛型函数。这个还不能用。

```rust
fn print_it<T>(input: T) {
    println!("{}", input) // ⚠️
}

fn main() {
    print_it("Please print me");
}
```

Rust说`error[E0277]: T doesn't implement std::fmt::Display`。所以我们会要求T实现Display。

```rust
use std::fmt::Display;

fn print_it<T: Display>(input: T) {
    println!("{}", input)
}

fn main() {
    print_it("Please print me");
}
```

现在可以用了，打印出`Please print me`。这是好的，但T仍然可以是多种类型。
可以是`i8`，也可以是`f32`，或者其他任何实现了`Display`的类型。我们加上`AsRef<str>`，现在T需要`AsRef<str>`和`Display`。

```rust
use std::fmt::Display;

fn print_it<T: AsRef<str> + Display>(input: T) {
    println!("{}", input)
}

fn main() {
    print_it("Please print me");
    print_it("Also, please print me".to_string());
    // print_it(7); <- 这样不会打印
}
```

现在，它不会接受`i8`这样的类型。

不要忘了，当函数变长时，你可以用`where`来写不同的函数。如果我们加上Debug，那么就会变成`fn print_it<T: AsRef<str> + Display + Debug>(input: T)`，这一行就很长了。所以我们可以这样写。

```rust
use std::fmt::{Debug, Display}; // 加上 Debug

fn print_it<T>(input: T) // 这一行现在好读了
where
    T: AsRef<str> + Debug + Display, // 这些 trait 也好读
{
    println!("{}", input)
}

fn main() {
    print_it("Please print me");
    print_it("Also, please print me".to_string());
}
```
