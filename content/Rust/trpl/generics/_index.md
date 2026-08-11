+++
title = "第10章 泛型类型、Trait 与生命周期"
date = 2026-08-05T08:44:00+08:00
weight = 41
type = "docs"
description = "用泛型、trait 与生命周期消除重复并保证引用有效"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 泛型类型、Trait 与生命周期 {#generic-types-traits-and-lifetimes}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch10-00-generics.html](https://doc.rust-lang.org/stable/book/ch10-00-generics.html)


　　每种编程语言都有有效处理概念重复的工具。在 Rust 中，其中之一是*泛型（generics）*：具体类型或其他属性的抽象占位符。我们可以表达泛型的行为，或它们与其他泛型的关系，而无需在编译与运行时知道最终会填入什么。

　　函数可以接受某种泛型类型的参数，而不是像 `i32` 或 `String` 这样的具体类型——正如它们可以接受未知具体值的参数，以便对多个具体值运行同一段代码。事实上，我们已经在第 6 章用过 `Option<T>`，第 8 章用过 `Vec<T>` 与 `HashMap<K, V>`，第 9 章用过 `Result<T, E>`。本章将探索如何用泛型定义自己的类型、函数与方法！

　　首先，我们回顾如何通过提取函数来减少代码重复。然后用同样的手法，把两个仅参数类型不同的函数做成一个泛型函数。我们还会说明如何在结构体与枚举定义中使用泛型类型。

　　接着，你会学习如何用 trait 以通用方式定义行为。可以把 trait 与泛型类型结合，约束泛型只接受具有特定行为的类型，而不是任意类型。

　　最后，我们讨论*生命周期（lifetime）*：一类向编译器说明引用之间如何关联的泛型。有了生命周期，我们就能为借用值提供足够信息，让编译器在更多场景下确保引用有效——若没有我们的帮助，它做不到这些。

## 通过提取函数消除重复

　　泛型让我们用代表多种类型的占位符替换具体类型，从而消除代码重复。在深入泛型语法之前，我们先看一种不涉及泛型类型的消除重复方式：提取一个函数，用代表多个值的占位符替换具体值。然后，再把同样的手法用到提取泛型函数上！学会识别可提取为函数的重复代码后，你也会开始识别可用泛型处理的重复代码。

　　我们从示例 10-1 的短程序开始：在列表中找出最大的数。

**文件名：`src/main.rs`**
```rust
fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");

}
```

**示例 10-1：在数字列表中找出最大的数**

　　我们把整数列表存入变量 `number_list`，并把对列表中第一个数的引用放入名为 `largest` 的变量。然后遍历列表中的所有数：若当前数大于 `largest` 中存储的数，就替换该变量中的引用；若当前数小于或等于目前见过的最大数，变量不变，继续处理下一个。考虑完列表中所有数后，`largest` 应指向最大的数，本例中是 100。

　　现在我们需要在两个不同的数字列表中找出最大数。为此可以选择复制示例 10-1 的代码，在程序两处使用相同逻辑，如示例 10-2 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");
}
```

**示例 10-2：在*两个*数字列表中找出最大数的代码**

　　虽然能工作，但复制代码既乏味又易错。想改逻辑时，还得记得在多处同步更新。

　　为消除重复，我们通过定义一个对作为参数传入的任意整数列表进行操作的函数来建立抽象。这样代码更清晰，也能抽象地表达“在列表中找最大数”这一概念。

　　在示例 10-3 中，我们把找最大数的代码提取到名为 `largest` 的函数里，再调用它找出示例 10-2 中两个列表的最大数。将来若有其他 `i32` 值的列表，也可以用这个函数。

**文件名：`src/main.rs`**
```rust
fn largest(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {result}");

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];

    let result = largest(&number_list);
    println!("The largest number is {result}");

}
```

**示例 10-3：抽象后、在两个列表中找最大数的代码**

　　`largest` 函数有一个参数 `list`，代表我们可能传入的任意具体 `i32` 值切片。因此调用函数时，代码会在我们传入的具体值上运行。

　　总结一下，从示例 10-2 改到示例 10-3 的步骤是：

1. 识别重复代码。
1. 把重复代码提取到函数体中，并在函数签名中标明该代码的输入与返回值。
1. 把两处重复代码更新为改为调用该函数。

　　接下来，我们用同样的步骤配合泛型来减少重复。正如函数体可以对抽象的 `list` 而非具体值操作，泛型也让代码能对抽象类型操作。

　　例如，假设我们有两个函数：一个在 `i32` 值切片中找最大项，一个在 `char` 值切片中找最大项。如何消除那种重复？我们马上就会看到！
