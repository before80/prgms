+++
title = "28-实现结构体和枚举"
date = 2026-08-21T12:46:00+08:00
weight = 29
type = "docs"
description = "实现结构体和枚举 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_27.html](https://dhghomon.github.io/easy_rust/Chapter_27.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 实现结构体和枚举

在这里你可以开始赋予你的结构体和枚举一些真正的力量。要调用 `struct` 或 `enum` 上的函数，请使用 `impl` 块。这些函数被称为**方法**。`impl`块中有两种方法。

- 方法：这些方法取**self**（或 **&self** 或 **&mut self** ）。常规方法使用"."（一个句号）。`.clone()`是一个常规方法的例子。
- 关联函数（在某些语言中被称为 "静态 "方法）：这些函数不使用self。关联的意思是 "与之相关"。它们的书写方式不同，使用`::`。`String::from()`是一个关联函数，`Vec::new()`也是。你看到的关联函数最常被用来创建新的变量。

在我们的例子中，我们将创建Animal并打印它们。

对于新的`struct`或`enum`，如果你想使用`{:?}`来打印，你需要给它**Debug**，所以我们将这样做:如果你在结构体或枚举上面写了`#[derive(Debug)]`，那么你就可以用`{:?}`来打印。这些带有`#[]`的信息被称为**属性**。你有时可以用它们来告诉编译器给你的结构体一个能力，比如`Debug`。属性有很多，我们以后会学习它们。但是`derive`可能是最常见的，你经常在结构体和枚举上面看到它。

```rust
#[derive(Debug)]
struct Animal {
    age: u8,
    animal_type: AnimalType,
}

#[derive(Debug)]
enum AnimalType {
    Cat,
    Dog,
}

impl Animal {
    fn new() -> Self {
        // Self 表示 Animal。
        // 也可以写 Animal 代替 Self

        Self {
            // 调用 Animal::new() 时，总是得到一只 10 岁的猫
            age: 10,
            animal_type: AnimalType::Cat,
        }
    }

    fn change_to_dog(&mut self) { // 因为在 Animal 内部，&mut self 就是 &mut Animal
                                  // 用 .change_to_dog() 把猫改成狗
                                  // 有了 &mut self 才能修改
        println!("Changing animal to dog!");
        self.animal_type = AnimalType::Dog;
    }

    fn change_to_cat(&mut self) {
        // 用 .change_to_cat() 把狗改成猫
        // 有了 &mut self 才能修改
        println!("Changing animal to cat!");
        self.animal_type = AnimalType::Cat;
    }

    fn check_type(&self) {
        // 我们只想读取 self
        match self.animal_type {
            AnimalType::Dog => println!("The animal is a dog"),
            AnimalType::Cat => println!("The animal is a cat"),
        }
    }
}



fn main() {
    let mut new_animal = Animal::new(); // 用于创建新 animal 的关联函数
                                        // 是一只 10 岁的猫
    new_animal.check_type();
    new_animal.change_to_dog();
    new_animal.check_type();
    new_animal.change_to_cat();
    new_animal.check_type();
}
```

这个打印:

```text
The animal is a cat
Changing animal to dog!
The animal is a dog
Changing animal to cat!
The animal is a cat
```


记住，Self(类型Self)和self(变量self)是缩写。(缩写=简写方式)

所以，在我们的代码中，Self = Animal。另外，`fn change_to_dog(&mut self)`的意思是`fn change_to_dog(&mut Animal)`。

下面再举一个小例子。这次我们将在`enum`上使用`impl`。

```rust
enum Mood {
    Good,
    Bad,
    Sleepy,
}

impl Mood {
    fn check(&self) {
        match self {
            Mood::Good => println!("Feeling good!"),
            Mood::Bad => println!("Eh, not feeling so good"),
            Mood::Sleepy => println!("Need sleep NOW"),
        }
    }
}

fn main() {
    let my_mood = Mood::Sleepy;
    my_mood.check();
}
```

打印出`Need sleep NOW`。
