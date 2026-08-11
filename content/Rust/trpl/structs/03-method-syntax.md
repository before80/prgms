+++
title = "5.3 方法"
date = 2026-08-05T08:44:00+08:00
weight = 22
type = "docs"
description = "方法语法：在 impl 块中为结构体定义方法与关联函数"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 方法


> 原文链接: [https://doc.rust-lang.org/stable/book/ch05-03-method-syntax.html](https://doc.rust-lang.org/stable/book/ch05-03-method-syntax.html)


## 方法

　　方法与函数类似：用 `fn` 关键字和名字声明，可以有参数和返回值，并包含从别处调用时运行的代码。与函数不同的是，方法定义在结构体（或枚举，或特征对象——分别在[第 6 章][enums]和[第 18 章][trait-objects]讨论）的上下文中，并且第一个参数总是 `self`，表示调用该方法的结构体实例。

### 方法语法 {#method-syntax}

　　我们来改写以 `Rectangle` 实例为参数的 `area` 函数，改为在 `Rectangle` 结构体上定义的 `area` 方法，如示例 5-13 所示。

**文件名：`src/main.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

**示例 5-13：在 `Rectangle` 结构体上定义 `area` 方法**

　　要在 `Rectangle` 的上下文中定义函数，我们为 `Rectangle` 开启一个 `impl`（implementation，实现）块。该 `impl` 块内的一切都会与 `Rectangle` 类型关联。然后把 `area` 函数移入 `impl` 的花括号内，并把签名和函数体中的第一个（此处也是唯一一个）参数改为 `self`。在 `main` 里，原先调用 `area` 函数并传入 `rect1` 的地方，可以改用*方法语法*在我们的 `Rectangle` 实例上调用 `area` 方法。方法语法写在实例之后：加点号、方法名、圆括号以及任意参数。

　　在 `area` 的签名中，我们使用 `&self` 而不是 `rectangle: &Rectangle`。`&self` 实际上是 `self: &Self` 的简写。在 `impl` 块内，类型 `Self` 是该 `impl` 所针对类型的别名。方法的第一个参数必须是名为 `self`、类型为 `Self` 的参数，因此 Rust 允许你在第一个参数位置只用名字 `self` 作为简写。注意：我们仍需在 `self` 简写前使用 `&`，以表明该方法借用 `Self` 实例，就像以前写 `rectangle: &Rectangle` 一样。方法可以取得 `self` 的所有权、像这里一样不可变地借用 `self`，或可变地借用 `self`，就像对待其他任何参数一样。

　　这里选择 `&self` 的原因，与函数版本中使用 `&Rectangle` 相同：我们不想取得所有权，只想读取结构体中的数据，而不写入。若希望方法在执行过程中修改被调用的实例，第一个参数应使用 `&mut self`。用单独的 `self` 作为第一个参数从而取得实例所有权的方法很少见；这种手法通常用于方法把 `self` 变换成别的东西，并且希望阻止调用方在变换之后继续使用原始实例。

　　除了提供方法语法、以及不必在每个方法签名中重复 `self` 的类型之外，使用方法而非函数的主要原因是组织性。我们把能对某一类型实例做的事都放在一个 `impl` 块里，而不是让未来的代码使用者在我们提供的库中四处查找 `Rectangle` 的能力。

　　注意：我们可以选择让方法与结构体的某个字段同名。例如，可以在 `Rectangle` 上定义一个也叫 `width` 的方法：

**文件名：`src/main.rs`**
```rust
impl Rectangle {
    fn width(&self) -> bool {
        self.width > 0
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    if rect1.width() {
        println!("The rectangle has a nonzero width; it is {}", rect1.width);
    }
}
```

　　这里我们选择让 `width` 方法在实例的 `width` 字段值大于 `0` 时返回 `true`，为 `0` 时返回 `false`：同名方法内可以任意目的使用该字段。在 `main` 中，当 `rect1.width` 后面跟有圆括号时，Rust 知道我们指的是方法 `width`；没有圆括号时，Rust 知道我们指的是字段 `width`。

　　常常（但并非总是）当我们给方法起与字段相同的名字时，只想返回字段中的值而不做别的事。这类方法称为 getter（取值方法），Rust 不会像某些其他语言那样自动为结构体字段实现它们。Getter 很有用，因为你可以把字段设为私有、把方法设为公有，从而在类型的公共 API 中提供对该字段的只读访问。什么是公有与私有，以及如何把字段或方法指定为公有或私有，会在[第 7 章][public]讨论。

> ### `->` 运算符哪去了？ {#wheres-the---operator}
>
> 在 C 和 C++ 中，调用方法要用两种不同的运算符：直接在对象上调用方法用 `.`；若在指向对象的指针上调用方法并需要先解引用，则用 `->`。换言之，若 `object` 是指针，`object->something()` 类似于 `(*object).something()`。
>
> Rust 没有与 `->` 等价的运算符；取而代之的是称为*自动引用与解引用*（automatic referencing and dereferencing）的特性。调用方法是 Rust 中少数具有这种行为的地方之一。
>
> 工作方式如下：当你用 `object.something()` 调用方法时，Rust 会自动加上 `&`、`&mut` 或 `*`，使 `object` 与方法的签名匹配。换言之，下面两种写法等价：
>
> 
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> 第一种写法干净得多。这种自动引用行为之所以可行，是因为方法有明确的接收者——`self` 的类型。给定接收者和方法名，Rust 能明确判断该方法是在读取（`&self`）、修改（`&mut self`）还是消费（`self`）。Rust 对方法接收者隐式借用，是让所有权在实践中好用的重要一环。

### 带有更多参数的方法

　　通过在 `Rectangle` 结构体上实现第二个方法来练习使用方法。这次我们希望 `Rectangle` 的实例接受另一个 `Rectangle` 实例，若第二个 `Rectangle` 能完全放进 `self`（第一个 `Rectangle`）内则返回 `true`，否则返回 `false`。也就是说，定义好 `can_hold` 方法后，我们希望能写出示例 5-14 所示的程序。

**文件名：`src/main.rs`**
```rust
fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    let rect2 = Rectangle {
        width: 10,
        height: 40,
    };
    let rect3 = Rectangle {
        width: 60,
        height: 45,
    };

    println!("Can rect1 hold rect2? {}", rect1.can_hold(&rect2));
    println!("Can rect1 hold rect3? {}", rect1.can_hold(&rect3));
}
```

**示例 5-14：使用尚未编写的 `can_hold` 方法**

　　预期输出如下，因为 `rect2` 的两个维度都小于 `rect1`，而 `rect3` 比 `rect1` 更宽：

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

　　我们知道要定义的是方法，因此它会放在 `impl Rectangle` 块内。方法名是 `can_hold`，参数是对另一个 `Rectangle` 的不可变借用。从调用方法的代码可以看出参数类型：`rect1.can_hold(&rect2)` 传入 `&rect2`，即对 `Rectangle` 实例 `rect2` 的不可变借用。这说得通，因为我们只需读取 `rect2`（而不是写入，写入则需要可变借用），并且希望 `main` 保留 `rect2` 的所有权，以便在调用 `can_hold` 之后还能再用。`can_hold` 的返回值是布尔值，实现会分别检查 `self` 的宽和高是否大于另一个 `Rectangle` 的宽和高。把新的 `can_hold` 方法加入示例 5-13 的 `impl` 块，如示例 5-15 所示。

**文件名：`src/main.rs`**
```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

**示例 5-15：在 `Rectangle` 上实现以另一个 `Rectangle` 实例为参数的 `can_hold` 方法**

　　用示例 5-14 中的 `main` 函数运行这段代码，会得到期望的输出。方法可以在 `self` 参数之后的签名中加入多个参数，这些参数的工作方式与函数中的参数相同。

### 关联函数

　　在 `impl` 块内定义的所有函数都称为*关联函数*（associated function），因为它们与 `impl` 后面的那个类型相关联。我们也可以定义第一个参数不是 `self` 的关联函数（因此它们不是方法），因为它们不需要该类型的实例就能工作。我们已经用过一个这样的函数：定义在 `String` 类型上的 `String::from`。

　　不是方法的关联函数常被用作构造函数，返回结构体的新实例。它们常常叫做 `new`，但 `new` 并不是特殊名字，也不是语言内置的。例如，我们可以提供一个名为 `square` 的关联函数：它接受一个维度参数，同时用作宽和高，从而更容易创建正方形 `Rectangle`，而不必把同一个值写两遍：

<span class="filename">文件名： src/main.rs</span>

```rust
impl Rectangle {
    fn square(size: u32) -> Self {
        Self {
            width: size,
            height: size,
        }
    }
}
```

　　返回类型和函数体中的 `Self` 关键字都是 `impl` 关键字后面那个类型的别名，此处即 `Rectangle`。

　　要调用这个关联函数，需要使用结构体名加上 `::`，例如 `let sq = Rectangle::square(3);`。调用关联函数时要在结构体名前加 `::`；同样的 `::` 语法也用于访问模块中的项。模块会在[第 7 章][modules]讨论。

### 多个 `impl` 块

　　每个结构体允许有多个 `impl` 块。例如，示例 5-15 等价于示例 5-16 所示的代码，后者把每个方法放在各自的 `impl` 块中。

```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

**示例 5-16：用多个 `impl` 块重写示例 5-15**

　　这里没有必要把这些方法拆进多个 `impl` 块，但这种语法是合法的。第 10 章讨论泛型类型和特征时，我们会看到多个 `impl` 块有用的情形。

## 总结

　　结构体让你创建对领域有意义的自定义类型。通过使用结构体，可以把相关联的数据块维系在一起，并为每一块命名，使代码更清晰。在 `impl` 块中可以定义与类型相关联的函数；方法是一种关联函数，让你指定结构体实例所具有的行为。

　　但结构体并非创建自定义类型的唯一方式：接下来转向 Rust 的枚举特性，为你的工具箱再添一件利器。

[enums]: ../../enums/
[trait-objects]: ../../oop/02-trait-objects/
[public]: ../../modules/03-paths-for-referring-to-an-item-in-the-module-tree/
[modules]: ../../modules/02-defining-modules-to-control-scope-and-privacy/
