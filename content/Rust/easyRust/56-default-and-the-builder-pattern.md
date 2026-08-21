+++
title = "56-默认值和建造者模式"
date = 2026-08-21T12:46:00+08:00
weight = 57
type = "docs"
description = "默认值和建造者模式 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_55.html](https://dhghomon.github.io/easy_rust/Chapter_55.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 默认值和建造者模式

你可以实现 `Default` trait，给你认为最常见的 `struct` 或 `enum` 赋值。建造者模式可以很好地与之配合，让用户在需要时轻松地进行修改。首先我们来看看`Default`。实际上，Rust中的大多数通用类型已经有`Default`。它们并不奇怪。0, ""(空字符串), `false`, 等等。

```rust
fn main() {
    let default_i8: i8 = Default::default();
    let default_str: String = Default::default();
    let default_bool: bool = Default::default();

    println!("'{}', '{}', '{}'", default_i8, default_str, default_bool);
}
```

这将打印`'0', '', 'false'`。

所以`Default`就像`new`函数一样，除了你不需要输入任何东西。首先我们要创建一个`struct`，它还没有实现`Default`。它有一个`new`函数，我们用它来创建一个名为Billy的角色，并提供一些统计信息。

```rust
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
}

enum LifeState {
    Alive,
    Dead,
    NeverAlive,
    Uncertain
}

impl Character {
    fn new(name: String, age: u8, height: u32, weight: u32, alive: bool) -> Self {
        Self {
            name,
            age,
            height,
            weight,
            lifestate: if alive { LifeState::Alive } else { LifeState::Dead },
        }
    }
}

fn main() {
    let character_1 = Character::new("Billy".to_string(), 15, 170, 70, true);
}
```

但也许在我们的世界里，我们希望大部分角色都叫比利，年龄15岁，身高170，体重70，还活着。我们可以实现`Default`，这样我们就可以直接写`Character::default()`。它看起来是这样的:

```rust
#[derive(Debug)]
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
}

#[derive(Debug)]
enum LifeState {
    Alive,
    Dead,
    NeverAlive,
    Uncertain,
}

impl Character {
    fn new(name: String, age: u8, height: u32, weight: u32, alive: bool) -> Self {
        Self {
            name,
            age,
            height,
            weight,
            lifestate: if alive {
                LifeState::Alive
            } else {
                LifeState::Dead
            },
        }
    }
}

impl Default for Character {
    fn default() -> Self {
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
        }
    }
}

fn main() {
    let character_1 = Character::default();

    println!(
        "The character {:?} is {:?} years old.",
        character_1.name, character_1.age
    );
}
```

打印出`The character "Billy" is 15 years old.`，简单多了!

现在我们来看建造者模式。我们会有很多Billy，所以我们会保留默认的。但是很多其他角色只会有一点不同。建造者模式让我们可以把小方法链接起来，每次改变一个值。这里是一个`Character`的方法:

```rust
fn height(mut self, height: u32) -> Self {    // 🚧
    self.height = height;
    self
}
```

一定要注意，它取的是`mut self`。我们之前看到过一次，它不是一个可变引用(`&mut self`)。它占用了`Self`的所有权，有了`mut`，它将是可变的，即使它之前不是可变的。这是因为`.height()`拥有完全的所有权，别人不能碰它，所以它是安全的，可变。它只是改变`self.height`，然后返回`Self`(就是`Character`)。

所以我们有三个这样的构建方法。它们几乎是一样的:

```rust
fn height(mut self, height: u32) -> Self {     // 🚧
    self.height = height;
    self
}

fn weight(mut self, weight: u32) -> Self {
    self.weight = weight;
    self
}

fn name(mut self, name: &str) -> Self {
    self.name = name.to_string();
    self
}
```

每一个都会改变一个变量，并回馈给`Self`:这就是你在建造者模式中看到的。所以现在我们类似这样写来创建一个角色:`let character_1 = Character::default().height(180).weight(60).name("Bobby");`。如果你正在构建一个库给别人使用，这可以让他们很容易用起来。对最终用户来说很容易，因为它几乎看起来像自然的英语。"给我一个默认角色，身高为180，体重为60，名字为Bobby." 到目前为止，我们的代码看起来是这样的:

```rust
#[derive(Debug)]
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
}

#[derive(Debug)]
enum LifeState {
    Alive,
    Dead,
    NeverAlive,
    Uncertain,
}

impl Character {
    fn new(name: String, age: u8, height: u32, weight: u32, alive: bool) -> Self {
        Self {
            name,
            age,
            height,
            weight,
            lifestate: if alive {
                LifeState::Alive
            } else {
                LifeState::Dead
            },
        }
    }

    fn height(mut self, height: u32) -> Self {
        self.height = height;
        self
    }

    fn weight(mut self, weight: u32) -> Self {
        self.weight = weight;
        self
    }

    fn name(mut self, name: &str) -> Self {
        self.name = name.to_string();
        self
    }
}

impl Default for Character {
    fn default() -> Self {
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
        }
    }
}

fn main() {
    let character_1 = Character::default().height(180).weight(60).name("Bobby");

    println!("{:?}", character_1);
}
```

最后一个要添加的方法通常叫`.build()`。这个方法是一种最终检查。当你给用户提供一个像`.height()`这样的方法时，你可以确保他们只输入一个`u32()`，但是如果他们输入5000的身高怎么办？这在你正在做的游戏中可能就不对了。我们最后将使用一个名为`.build()`的方法，返回一个`Result`。在它里面我们将检查用户输入是否正常，如果正常，我们将返回一个 `Ok(Self)`。

不过首先我们要改变`.new()`方法。我们不希望用户再自由创建任何一种角色。所以我们将把`impl Default`的值移到`.new()`。而现在`.new()`不接受任何输入。

```rust
    fn new() -> Self {    // 🚧
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
        }
    }
```

这意味着我们不再需要`impl Default`了，因为`.new()`有所有的默认值。所以我们可以删除`impl Default`。

现在我们的代码是这样的。

```rust
#[derive(Debug)]
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
}

#[derive(Debug)]
enum LifeState {
    Alive,
    Dead,
    NeverAlive,
    Uncertain,
}

impl Character {
    fn new() -> Self {
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
        }
    }

    fn height(mut self, height: u32) -> Self {
        self.height = height;
        self
    }

    fn weight(mut self, weight: u32) -> Self {
        self.weight = weight;
        self
    }

    fn name(mut self, name: &str) -> Self {
        self.name = name.to_string();
        self
    }
}

fn main() {
    let character_1 = Character::new().height(180).weight(60).name("Bobby");

    println!("{:?}", character_1);
}
```

这样打印出来的结果是一样的:`Character { name: "Bobby", age: 15, height: 180, weight: 60, lifestate: Alive }`。

我们几乎已经准备好写`.build()`方法了，但是有一个问题:如何让用户使用它？现在用户可以写`let x = Character::new().height(76767);`，然后得到一个`Character`。有很多方法可以做到这一点，也许你能想出自己的方法。但是我们会在`Character`中增加一个`can_use: bool`的值。

```rust
#[derive(Debug)]       // 🚧
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
    can_use: bool, // 设置用户能否使用该角色
}

\\ Cut other code

    fn new() -> Self {
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
            can_use: true, // .new() 总是给出可用角色，所以是 true
        }
    }
```

而对于其他的方法，比如`.height()`，我们会将`can_use`设置为`false`。只有`.build()`会再次设置为`true`，所以现在用户要用`.build()`做最后的检查。我们要确保`height`不高于200，`weight`不高于300。另外，在我们的游戏中，有一个不好的字叫`smurf`，我们不希望任何角色使用它。

我们的`.build()`方法是这样的:

```rust
fn build(mut self) -> Result<Character, String> {      // 🚧
    if self.height < 200 && self.weight < 300 && !self.name.to_lowercase().contains("smurf") {
        self.can_use = true;
        Ok(self)
    } else {
        Err("Could not create character. Characters must have:
1) Height below 200
2) Weight below 300
3) A name that is not Smurf (that is a bad word)"
            .to_string())
    }
}
```

`!self.name.to_lowercase().contains("smurf")` 确保用户不会写出类似 "SMURF"或 "IamSmurf"的字样。它让整个 `String` 都变成小写(小字母)，并检查 `.contains()` 而不是 `==`。而前面的`!`表示 "不是"。

如果一切正常，我们就把`can_use`设置为`true`，然后把`Ok`里面的字符给用户。

现在我们的代码已经完成了，我们将创建三个不工作的角色，和一个工作的角色。最后的代码是这样的。

```rust
#[derive(Debug)]
struct Character {
    name: String,
    age: u8,
    height: u32,
    weight: u32,
    lifestate: LifeState,
    can_use: bool, // 这是新字段
}

#[derive(Debug)]
enum LifeState {
    Alive,
    Dead,
    NeverAlive,
    Uncertain,
}

impl Character {
    fn new() -> Self {
        Self {
            name: "Billy".to_string(),
            age: 15,
            height: 170,
            weight: 70,
            lifestate: LifeState::Alive,
            can_use: true,  // .new() 做出可用角色，所以是 true
        }
    }

    fn height(mut self, height: u32) -> Self {
        self.height = height;
        self.can_use = false; // 现在用户不能用这个角色了
        self
    }

    fn weight(mut self, weight: u32) -> Self {
        self.weight = weight;
        self.can_use = false;
        self
    }

    fn name(mut self, name: &str) -> Self {
        self.name = name.to_string();
        self.can_use = false;
        self
    }

    fn build(mut self) -> Result<Character, String> {
        if self.height < 200 && self.weight < 300 && !self.name.to_lowercase().contains("smurf") {
            self.can_use = true;   // 一切正常，设为 true
            Ok(self)               // 并返回角色
        } else {
            Err("Could not create character. Characters must have:
1) Height below 200
2) Weight below 300
3) A name that is not Smurf (that is a bad word)"
                .to_string())
        }
    }
}

fn main() {
    let character_with_smurf = Character::new().name("Lol I am Smurf!!").build(); // 这个名字含 "smurf" — 不行
    let character_too_tall = Character::new().height(400).build(); // 太高 — 不行
    let character_too_heavy = Character::new().weight(500).build(); // 太重 — 不行
    let okay_character = Character::new()
        .name("Billybrobby")
        .height(180)
        .weight(100)
        .build();   // 这个角色可以。名字、身高、体重都没问题

    // 现在它们不是 Character，而是 Result<Character, String>。放进 Vec 方便查看：
    let character_vec = vec![character_with_smurf, character_too_tall, character_too_heavy, okay_character];

    for character in character_vec { // Ok 就打印角色，Err 就打印错误
        match character {
            Ok(character_info) => println!("{:?}", character_info),
            Err(err_info) => println!("{}", err_info),
        }
        println!(); // 再空一行
    }
}
```

这将打印:

```text
Could not create character. Characters must have:
1) Height below 200
2) Weight below 300
3) A name that is not Smurf (that is a bad word)

Could not create character. Characters must have:
1) Height below 200
2) Weight below 300
3) A name that is not Smurf (that is a bad word)

Could not create character. Characters must have:
1) Height below 200
2) Weight below 300
3) A name that is not Smurf (that is a bad word)

Character { name: "Billybrobby", age: 15, height: 180, weight: 100, lifestate: Alive, can_use: true }
```
