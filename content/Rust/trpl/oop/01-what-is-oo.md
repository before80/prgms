+++
title = "18.1 面向对象语言的特征"
date = 2026-08-05T08:44:00+08:00
weight = 87
type = "docs"
description = "从对象、封装与继承三方面审视面向对象特征，以及 Rust 如何对应"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 面向对象语言的特征


> 原文链接: [https://doc.rust-lang.org/stable/book/ch18-01-what-is-oo.html](https://doc.rust-lang.org/stable/book/ch18-01-what-is-oo.html)


## 面向对象语言的特征

　　编程社区对一门语言必须具备哪些特性才算面向对象并无共识。Rust 受到多种编程范式影响，也包括 OOP；例如，我们在第 13 章探讨过源自函数式编程的特性。可以说，OOP 语言共享某些常见特征——即对象、封装与继承。下面逐一看这些特征的含义，以及 Rust 是否支持。

### 对象包含数据与行为

　　Erich Gamma、Richard Helm、Ralph Johnson 与 John Vlissides 所著的 *Design Patterns: Elements of Reusable Object-Oriented Software*（Addison-Wesley，1994）——俗称*四人帮*（The Gang of Four）之书——是一本面向对象设计模式目录。它这样定义 OOP：

> 面向对象程序由对象构成。一个**对象**把数据以及对这些数据操作的过程打包在一起。这些过程通常称为**方法**或**操作**。

　　按这一定义，Rust 是面向对象的：结构体与枚举拥有数据，`impl` 块则为结构体与枚举提供方法。尽管带方法的结构体与枚举并不被*称为*对象，但按四人帮对对象的定义，它们提供了相同的功能。

### 隐藏实现细节的封装 {#encapsulation-that-hides-implementation-details}

　　另一项常与 OOP 关联的方面是*封装*（encapsulation）：对象的实现细节对使用该对象的代码不可见。因此，与对象交互的唯一方式是通过其公共 API；使用对象的代码不应能直接访问其内部数据或行为。这使得程序员可以改动、重构对象内部，而不必改动使用该对象的代码。

　　我们在第 7 章讨论过如何控制封装：可以用 `pub` 关键字决定代码中哪些模块、类型、函数与方法应为公开，其余默认私有。例如，我们可以定义结构体 `AveragedCollection`，其中一个字段保存 `i32` 值的向量，另一个字段保存向量中各值的平均值，这样就不必每次有人需要时都现场计算。换句话说，`AveragedCollection` 会替我们缓存算好的平均值。示例 18-1 给出了该结构体的定义。

**文件名：`src/lib.rs`**
```rust
pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}
```

**示例 18-1：维护整数列表及其平均值的 `AveragedCollection` 结构体**

　　结构体标为 `pub` 以便其他代码使用，但结构体内的字段仍保持私有。这一点在此很重要，因为我们要确保每当向列表添加或移除值时，平均值也会更新。我们通过在结构体上实现 `add`、`remove` 与 `average` 方法来做到这一点，如示例 18-2 所示。

**文件名：`src/lib.rs`**
```rust
impl AveragedCollection {
    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        match result {
            Some(value) => {
                self.update_average();
                Some(value)
            }
            None => None,
        }
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    fn update_average(&mut self) {
        let total: i32 = self.list.iter().sum();
        self.average = total as f64 / self.list.len() as f64;
    }
}
```

**示例 18-2：在 `AveragedCollection` 上实现公共方法 `add`、`remove` 与 `average`**

　　公共方法 `add`、`remove` 与 `average` 是访问或修改 `AveragedCollection` 实例中数据的唯一途径。当用 `add` 向 `list` 添加项，或用 `remove` 移除项时，各自的实现都会调用私有的 `update_average` 方法，由它负责同步更新 `average` 字段。

　　我们把 `list` 与 `average` 字段留作私有，这样外部代码就无法直接向 `list` 添加或移除项；否则当 `list` 变化时，`average` 字段可能不同步。`average` 方法返回 `average` 字段中的值，允许外部代码读取平均值但不能修改它。

　　因为我们已经封装了结构体 `AveragedCollection` 的实现细节，将来很容易改动诸如数据结构等方面。例如，可以用 `HashSet<i32>` 代替 `Vec<i32>` 作为 `list` 字段。只要 `add`、`remove` 与 `average` 公共方法的签名保持不变，使用 `AveragedCollection` 的代码就无需改动。若我们把 `list` 做成公开，情况就未必如此：`HashSet<i32>` 与 `Vec<i32>` 增删项的方法不同，若外部代码直接修改 `list`，就很可能也要跟着改。

　　若封装是语言被视为面向对象的必要条件，那么 Rust 满足这一要求。对代码不同部分选择使用或不使用 `pub`，就能封装实现细节。

### 作为类型系统与代码共享的继承

　　*继承*（inheritance）是一种机制：对象可以从另一对象的定义继承元素，从而获得父对象的数据与行为，而无需再次定义它们。

　　若一门语言必须有继承才算面向对象，那么 Rust 不是这样的语言。没有办法在不用宏的情况下定义一个结构体去继承父结构体的字段与方法实现。

　　不过，若你习惯在工具箱里使用继承，可以根据当初求助于继承的原因，在 Rust 中采用其他方案。

　　选择继承主要有两个理由。一是为了复用代码：你可以为一种类型实现特定行为，继承则让你把该实现复用到另一种类型上。在 Rust 中可以用 trait 方法的默认实现有限地做到这一点——你在示例 10-14 中见过我们为 `Summary` trait 的 `summarize` 方法添加默认实现。任何实现 `Summary` trait 的类型都会自动拥有 `summarize` 方法，无需额外代码。这类似于父类有方法实现，继承的子类也拥有该方法实现。实现 `Summary` trait 时我们也可以覆盖 `summarize` 的默认实现，这类似于子类覆盖从父类继承的方法实现。

　　使用继承的另一理由与类型系统有关：让子类型能用在父类型可用的相同位置。这也称为*多态*（polymorphism），意思是：若多个对象共享某些特征，就可以在运行时彼此替换。

> ### 多态
>
> 对许多人来说，多态几乎等同于继承。但它其实是更一般的概念，指能处理多种类型数据的代码。对继承而言，那些类型通常是子类。
>
> Rust 则用泛型抽象不同可能的类型，并用 trait 约束规定这些类型必须提供什么。这有时称为*有界参数多态*（bounded parametric polymorphism）。

　　Rust 选择不提供继承，是另一套取舍。继承常常有共享过多代码的风险。子类不应总是共享父类的全部特征，但继承会如此。这会使程序设计更不灵活。它还带来在子类上调用并不适用、甚至导致错误的方法的可能。此外，有些语言只允许*单继承*（子类只能继承一个类），进一步限制了程序设计的灵活性。

　　基于这些原因，Rust 采用不同的做法：用 trait 对象而非继承来实现运行时多态。接下来看看 trait 对象如何工作。
