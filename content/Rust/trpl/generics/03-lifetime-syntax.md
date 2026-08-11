+++
title = "10.3 用生命周期校验引用"
date = 2026-08-05T08:44:00+08:00
weight = 44
type = "docs"
description = "用生命周期注解确保引用始终有效"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用生命周期校验引用


> 原文链接: [https://doc.rust-lang.org/stable/book/ch10-03-lifetime-syntax.html](https://doc.rust-lang.org/stable/book/ch10-03-lifetime-syntax.html)


## 用生命周期校验引用 {#validating-references-with-lifetimes}

　　生命周期是我们其实已经在用的另一类泛型。它要确保的不是类型具有我们想要的行为，而是引用在我们需要的时间内始终有效。

　　第 4 章[「引用与借用」][references-and-borrowing]一节里我们没细谈的一点是：Rust 中每个引用都有生命周期，即该引用有效的作用域。多数时候生命周期是隐式的、可推断的——正如多数时候类型也可推断。只有当存在多种可能类型时，我们才需要标注类型；类似地，当引用的生命周期可能以几种不同方式相互关联时，我们必须标注生命周期。Rust 要求我们用泛型生命周期参数标注这些关系，以确保运行时实际使用的引用一定有效。

　　标注生命周期在多数其他编程语言中甚至不存在，因此会感觉陌生。本章不会覆盖生命周期的全部内容，但会讨论你可能遇到的常见生命周期语法，以便熟悉这一概念。

### 悬垂引用

　　生命周期的主要目标是防止悬垂引用（dangling reference）：若允许存在，程序就会引用到并非它本意要引用的数据。考虑示例 10-16 中的程序，它有一个外层作用域和一个内层作用域。

```rust
fn main() {
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {r}");
}
```

**示例 10-16：尝试使用值已离开作用域的引用**

> 注意：示例 10-16、10-17 与 10-23 中的例子声明变量时未赋初值，因此变量名存在于外层作用域。乍看这似乎与“Rust 没有空值”冲突。不过，若在赋值前使用变量，会得到编译期错误，这说明 Rust 确实不允许空值。

　　外层作用域声明了没有初值的变量 `r`，内层作用域声明了初值为 `5` 的变量 `x`。在内层作用域中，我们尝试把 `r` 的值设为对 `x` 的引用。然后内层作用域结束，我们尝试打印 `r` 中的值。这段代码无法编译，因为在我们使用 `r` 之前，它所引用的值已经离开了作用域。错误信息如下：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0597]: `x` does not live long enough
 --> src/main.rs:6:13
  |
5 |         let x = 5;
  |             - binding `x` declared here
6 |         r = &x;
  |             ^^ borrowed value does not live long enough
7 |     }
  |     - `x` dropped here while still borrowed
8 |
9 |     println!("r: {r}");
  |                   - borrow later used here

For more information about this error, try `rustc --explain E0597`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　错误信息说变量 `x` “有效期不够长”。原因是：内层作用域在第 7 行结束时 `x` 就会离开作用域，而 `r` 在外层作用域中仍然有效；因为它的作用域更大，我们说它“活得更久”（有效期更长）。若 Rust 允许这段代码通过编译，`r` 就会引用 `x` 离开作用域后已释放的内存，对 `r` 的任何使用都会出错。那么 Rust 如何判定这段代码无效？它使用借用检查器。

### 借用检查器

　　Rust 编译器有一个*借用检查器（borrow checker）*，通过比较作用域来判断所有借用是否有效。示例 10-17 展示了与示例 10-16 相同的代码，但加上了标注变量生命周期的注释。

```rust
fn main() {
    let r;                // ---------+-- 'a
                          //          |
    {                     //          |
        let x = 5;        // -+-- 'b  |
        r = &x;           //  |       |
    }                     // -+       |
                          //          |
    println!("r: {r}");   //          |
}                         // ---------+
```

**示例 10-17：分别标注为 `'a` 与 `'b` 的 `r` 与 `x` 的生命周期**

　　这里我们把 `r` 的生命周期标为 `'a`，把 `x` 的标为 `'b`。可以看出，内层 `'b` 块远小于外层 `'a` 生命周期块。编译时，Rust 比较两个生命周期的大小，发现 `r` 的生命周期是 `'a`，但它引用的内存生命周期是 `'b`。程序被拒绝，因为 `'b` 比 `'a` 短：引用的目标活得没有引用本身久。

　　示例 10-18 修复了代码，使之没有悬垂引用，并能无错误地编译。

```rust
fn main() {
    let x = 5;            // ----------+-- 'b
                          //           |
    let r = &x;           // --+-- 'a  |
                          //   |       |
    println!("r: {r}");   //   |       |
                          // --+       |
}                         // ----------+
```

**示例 10-18：有效的引用，因为数据的生命周期比引用更长**

　　这里 `x` 的生命周期是 `'b`，在本例中大于 `'a`。这意味着 `r` 可以引用 `x`，因为 Rust 知道在 `x` 有效期间，`r` 中的引用始终有效。

　　既然知道了引用生命周期在哪里，以及 Rust 如何分析生命周期以确保引用始终有效，接下来探索函数参数与返回值中的泛型生命周期。

### 函数中的泛型生命周期

　　我们要写一个返回两个字符串切片中较长者的函数。该函数接受两个字符串切片并返回一个字符串切片。实现 `longest` 之后，示例 10-19 中的代码应打印 `The longest string is abcd`。

**文件名：`src/main.rs`**
```rust
fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    let result = longest(string1.as_str(), string2);
    println!("The longest string is {result}");
}
```

**示例 10-19：调用 `longest` 找出两个字符串切片中较长者的 `main` 函数**

　　注意我们希望函数接受字符串切片（引用）而不是字符串，因为不想让 `longest` 取得参数的所有权。关于示例 10-19 所用参数为何合适，更多讨论见第 4 章[「字符串切片作为参数」][string-slices-as-parameters]。

　　若像示例 10-20 那样实现 `longest`，将无法编译。

**文件名：`src/main.rs`**
```rust
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}
```

**示例 10-20：返回两个字符串切片中较长者、但尚不能编译的 `longest` 实现**

　　相反，我们会得到谈论生命周期的如下错误：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0106]: missing lifetime specifier
 --> src/main.rs:9:33
  |
9 | fn longest(x: &str, y: &str) -> &str {
  |               ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `x` or `y`
help: consider introducing a named lifetime parameter
  |
9 | fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
  |           ++++     ++          ++          ++

For more information about this error, try `rustc --explain E0106`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　帮助文本揭示：返回类型需要泛型生命周期参数，因为 Rust 无法判断返回的引用指向 `x` 还是 `y`。其实我们也不知道，因为函数体的 `if` 块返回对 `x` 的引用，`else` 块返回对 `y` 的引用！

　　定义这个函数时，我们不知道会传入哪些具体值，因此不知道会执行 `if` 还是 `else`。也不知道将传入的引用的具体生命周期，因此不能像示例 10-17 与 10-18 那样查看作用域，以判断返回的引用是否始终有效。借用检查器同样无法判定，因为它不知道 `x` 与 `y` 的生命周期如何与返回值的生命周期关联。要修复该错误，我们添加定义引用之间关系的泛型生命周期参数，以便借用检查器能进行分析。

### 生命周期注解语法

　　生命周期注解并不会改变任何引用实际存活多久。它们描述多个引用的生命周期之间的关系，而不影响这些生命周期。正如签名指定泛型类型参数时函数可接受任意类型，通过指定泛型生命周期参数，函数也可接受具有任意生命周期的引用。

　　生命周期注解的语法略显特别：生命周期参数名必须以撇号（`'`）开头，通常全小写且很短，与泛型类型类似。多数人把第一个生命周期注解命名为 `'a`。我们把生命周期参数注解放在引用的 `&` 之后，并用空格把它与引用的类型分开。

　　下面是一些例子——不带生命周期参数的对 `i32` 的引用、带名为 `'a` 的生命周期参数的对 `i32` 的引用，以及同样具有生命周期 `'a` 的对 `i32` 的可变引用：

```rust
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

　　单独一个生命周期注解意义不大，因为注解的目的是告诉 Rust：多个引用的泛型生命周期参数如何相互关联。我们来看看在 `longest` 函数的语境中，这些注解如何相互关联。

### 在函数签名中

　　要在函数签名中使用生命周期注解，需要像泛型类型参数那样，在函数名与参数列表之间的尖括号内声明泛型生命周期参数。

　　我们希望签名表达如下约束：只要两个参数都有效，返回的引用就有效。这就是参数与返回值生命周期之间的关系。我们把该生命周期命名为 `'a`，并把它加到每个引用上，如示例 10-21 所示。

**文件名：`src/main.rs`**
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

**示例 10-21：指定签名中所有引用必须具有相同生命周期 `'a` 的 `longest` 函数定义**

　　与示例 10-19 中的 `main` 一起使用时，这段代码应能编译并产生我们想要的结果。

　　现在函数签名告诉 Rust：对于某个生命周期 `'a`，函数接受两个参数，二者都是至少与生命周期 `'a` 一样长的字符串切片。签名还告诉 Rust：函数返回的字符串切片也将至少与生命周期 `'a` 一样长。实践中，这意味着 `longest` 返回的引用的生命周期，等于函数参数所引用值的生命周期中较短的那个。这些关系正是我们希望 Rust 在分析这段代码时使用的。

　　记住：在函数签名中指定生命周期参数时，我们并没有改变传入或返回的任何值的生命周期。我们只是指明：借用检查器应拒绝任何不符合这些约束的值。注意 `longest` 不必确切知道 `x` 与 `y` 会活多久，只需知道某个作用域可以代入 `'a` 并满足该签名即可。

　　在函数中标注生命周期时，注解出现在函数签名中，而不是函数体中。生命周期注解成为函数契约的一部分，正如签名中的类型。让函数签名包含生命周期契约，意味着 Rust 编译器的分析可以更简单。若函数的标注方式或调用方式有问题，编译器错误能更精确地指向代码中的相关部分与约束。若相反，编译器对我们意图中的生命周期关系做更多推断，它或许只能指向距离问题根源很远的某次使用。

　　当我们把具体引用传给 `longest` 时，代入 `'a` 的具体生命周期是 `x` 的作用域与 `y` 的作用域重叠的那一部分。换句话说，泛型生命周期 `'a` 会得到等于 `x` 与 `y` 生命周期中较短者的具体生命周期。因为我们用同一生命周期参数 `'a` 标注了返回的引用，返回的引用在 `x` 与 `y` 较短生命周期的长度内也有效。

　　我们通过传入具有不同具体生命周期的引用来看看生命周期注解如何限制 `longest`。示例 10-22 是一个直截了当的例子。

**文件名：`src/main.rs`**
```rust
fn main() {
    let string1 = String::from("long string is long");

    {
        let string2 = String::from("xyz");
        let result = longest(string1.as_str(), string2.as_str());
        println!("The longest string is {result}");
    }
}
```

**示例 10-22：用指向具有不同具体生命周期的 `String` 值的引用调用 `longest`**

　　本例中，`string1` 有效直到外层作用域结束，`string2` 有效直到内层作用域结束，而 `result` 引用的东西有效直到内层作用域结束。运行这段代码，你会看到借用检查器通过了：它会编译并打印 `The longest string is long string is long`。

　　接下来看一个例子，说明 `result` 中引用的生命周期必须是两个参数中较短的那个。我们把 `result` 变量的声明移到内层作用域外，但把对 `result` 的赋值留在有 `string2` 的作用域内。然后把使用 `result` 的 `println!` 移到内层作用域外、内层作用域结束之后。示例 10-23 中的代码将无法编译。

**文件名：`src/main.rs`**
```rust
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("The longest string is {result}");
}
```

**示例 10-23：尝试在 `string2` 离开作用域后使用 `result`**

　　尝试编译时会得到如下错误：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0597]: `string2` does not live long enough
 --> src/main.rs:6:44
  |
5 |         let string2 = String::from("xyz");
  |             ------- binding `string2` declared here
6 |         result = longest(string1.as_str(), string2.as_str());
  |                                            ^^^^^^^ borrowed value does not live long enough
7 |     }
  |     - `string2` dropped here while still borrowed
8 |     println!("The longest string is {result}");
  |                                      ------ borrow later used here

For more information about this error, try `rustc --explain E0597`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　该错误表明：要使 `result` 对 `println!` 语句有效，`string2` 需要一直有效到外层作用域结束。Rust 之所以知道这一点，是因为我们用同一生命周期参数 `'a` 标注了函数参数与返回值的生命周期。

　　作为人类，我们可以看这段代码并看出 `string1` 比 `string2` 长，因此 `result` 会包含对 `string1` 的引用。因为 `string1` 尚未离开作用域，对 `string1` 的引用对 `println!` 仍然有效。然而编译器在这种情况下看不出引用有效。我们已经告诉 Rust：`longest` 返回的引用的生命周期等于传入引用中较短者的生命周期。因此借用检查器不允许示例 10-23 中的代码，因为它可能含有无效引用。

　　试着设计更多实验：改变传入 `longest` 的引用的值与生命周期，以及返回引用的使用方式。在编译前先假设实验能否通过借用检查器，再检查你是否正确！

### 关系

　　需要如何指定生命周期参数，取决于函数在做什么。例如，若把 `longest` 的实现改成总是返回第一个参数而不是较长的字符串切片，就不必在 `y` 参数上指定生命周期。下面的代码可以编译：

**文件名：`src/main.rs`**
```rust
fn longest<'a>(x: &'a str, y: &str) -> &'a str {
    x
}
```

　　我们为参数 `x` 与返回类型指定了生命周期参数 `'a`，但没有为参数 `y` 指定，因为 `y` 的生命周期与 `x` 或返回值的生命周期没有任何关系。

　　从函数返回引用时，返回类型的生命周期参数需要与某个参数的生命周期参数匹配。若返回的引用*不*指向任一参数，它就必须指向在本函数内创建的值。但这会是悬垂引用，因为该值会在函数结束时离开作用域。考虑下面这个无法编译的 `longest` 尝试实现：

**文件名：`src/main.rs`**
```rust
fn longest<'a>(x: &str, y: &str) -> &'a str {
    let result = String::from("really long string");
    result.as_str()
}
```

　　这里即便我们为返回类型指定了生命周期参数 `'a`，该实现仍无法编译，因为返回值的生命周期与参数的生命周期完全无关。错误信息如下：

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0515]: cannot return value referencing local variable `result`
  --> src/main.rs:11:5
   |
11 |     result.as_str()
   |     ------^^^^^^^^^
   |     |
   |     returns a value referencing data owned by the current function
   |     `result` is borrowed here

For more information about this error, try `rustc --explain E0515`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

　　问题在于：`result` 在 `longest` 函数结束时离开作用域并被清理，而我们还试图从函数返回对 `result` 的引用。没有任何生命周期参数能改变这种悬垂引用，Rust 也不会允许我们创建悬垂引用。这种情况下，最好的修复是返回拥有所有权的数据类型而不是引用，再由调用方负责清理该值。

　　归根结底，生命周期语法是在连接函数各个参数与返回值的生命周期。一旦连接起来，Rust 就有足够信息允许内存安全的操作，并禁止会创建悬垂指针或以其他方式破坏内存安全的操作。

### 在结构体定义中

　　到目前为止，我们定义的结构体都保存拥有所有权的类型。我们也可以定义保存引用的结构体，但那种情况下需要为结构体定义中的每个引用添加生命周期注解。示例 10-24 有一个保存字符串切片的结构体 `ImportantExcerpt`。

**文件名：`src/main.rs`**
```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();
    let i = ImportantExcerpt {
        part: first_sentence,
    };
}
```

**示例 10-24：保存引用、因而需要生命周期注解的结构体**

　　该结构体只有一个字段 `part`，保存字符串切片，也就是一个引用。与泛型数据类型一样，我们在结构体名后的尖括号内声明泛型生命周期参数，以便在结构体定义体中使用。这个注解意味着：`ImportantExcerpt` 实例的有效期不能超过其 `part` 字段所持引用的有效期。

　　这里的 `main` 创建了一个 `ImportantExcerpt` 实例，保存由变量 `novel` 所拥有的 `String` 中第一句的引用。`novel` 中的数据在创建 `ImportantExcerpt` 实例之前就存在；此外，`novel` 在 `ImportantExcerpt` 离开作用域之后才离开作用域，因此实例中的引用有效。

### 生命周期省略

　　你已经知道每个引用都有生命周期，并且对使用引用的函数或结构体需要指定生命周期参数。然而，我们在示例 4-9（此处重现为示例 10-25）中有一个函数，在没有生命周期注解的情况下也能编译。

**文件名：`src/lib.rs`**
```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

**示例 10-25：我们在示例 4-9 中定义的函数：尽管参数与返回类型都是引用，却没有生命周期注解也能编译**

　　该函数能在没有生命周期注解的情况下编译，原因是历史性的：在早期（1.0 之前）的 Rust 中，这段代码无法编译，因为每个引用都需要显式生命周期。那时函数签名会写成这样：

```rust
fn first_word<'a>(s: &'a str) -> &'a str {
```

　　写了大量 Rust 代码后，Rust 团队发现程序员在特定情形下反复输入相同的生命周期注解。这些情形可预测，并遵循若干确定性模式。开发者把这些模式编进编译器，使借用检查器能在这些情形下推断生命周期，而不再需要显式注解。

　　这段 Rust 历史之所以相关，是因为将来可能出现更多确定性模式并加入编译器。未来甚至可能需要更少的生命周期注解。

　　编进 Rust 对引用分析的这些模式称为*生命周期省略规则（lifetime elision rules）*。它们不是要求程序员遵守的规则，而是编译器会考虑的一组特定情形：若你的代码符合这些情形，就不必显式写出生命周期。

　　省略规则并不提供完整推断。若 Rust 应用规则后，引用的生命周期仍有歧义，编译器不会猜测其余引用的生命周期应是什么。它不会猜测，而是给出错误，你可以通过添加生命周期注解来解决。

　　函数或方法参数上的生命周期称为*输入生命周期（input lifetime）*，返回值上的称为*输出生命周期（output lifetime）*。

　　没有显式注解时，编译器使用三条规则来弄清引用的生命周期。第一条适用于输入生命周期，第二、三条适用于输出生命周期。若走完三条规则后仍有引用的生命周期无法确定，编译器就以错误停止。这些规则适用于 `fn` 定义以及 `impl` 块。

　　第一条规则是：编译器为每个是引用的参数各分配一个生命周期参数。换句话说，单参数函数得到一个生命周期参数：`fn foo<'a>(x: &'a i32)`；双参数函数得到两个不同的生命周期参数：`fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`；以此类推。

　　第二条规则是：若恰好只有一个输入生命周期参数，就把该生命周期赋给所有输出生命周期参数：`fn foo<'a>(x: &'a i32) -> &'a i32`。

　　第三条规则是：若有多个输入生命周期参数，但其中一个是 `&self` 或 `&mut self`（因为这是方法），就把 `self` 的生命周期赋给所有输出生命周期参数。第三条规则让方法读起来、写起来都更轻松，因为需要的符号更少。

　　假装我们是编译器。我们应用这些规则，弄清示例 10-25 中 `first_word` 函数签名里引用的生命周期。签名开始时引用上没有任何生命周期：

```rust
fn first_word(s: &str) -> &str {
```

　　然后编译器应用第一条规则：每个参数获得自己的生命周期。我们照例称之为 `'a`，于是签名变成：

```rust
fn first_word<'a>(s: &'a str) -> &str {
```

　　因为恰好只有一个输入生命周期，第二条规则适用：把这一个输入参数的生命周期赋给输出生命周期，于是签名现在是：

```rust
fn first_word<'a>(s: &'a str) -> &'a str {
```

　　现在该函数签名中的所有引用都有了生命周期，编译器可以继续分析，而无需程序员在这个函数签名中标注生命周期。

　　再看另一个例子，这次是我们在示例 10-20 开始处理时还没有生命周期参数的 `longest` 函数：

```rust
fn longest(x: &str, y: &str) -> &str {
```

　　应用第一条规则：每个参数获得自己的生命周期。这次有两个参数而不是一个，因此有两个生命周期：

```rust
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

　　可以看出第二条规则不适用，因为输入生命周期不止一个。第三条也不适用，因为 `longest` 是函数而不是方法，参数中没有 `self`。走完三条规则后，我们仍未弄清返回类型的生命周期。这就是尝试编译示例 10-20 的代码时出错的原因：编译器走完了生命周期省略规则，仍无法弄清签名中所有引用的生命周期。

　　因为第三条规则实际上只适用于方法签名，接下来我们在方法语境中看生命周期，以理解为何第三条规则意味着我们很少需要在方法签名中标注生命周期。

### 在方法定义中

　　在带生命周期的结构体上实现方法时，我们使用与泛型类型参数相同的语法，如示例 10-11 所示。在何处声明与使用生命周期参数，取决于它们与结构体字段相关，还是与方法参数及返回值相关。

　　结构体字段的生命周期名总是需要在 `impl` 关键字后声明，然后在结构体名后使用，因为那些生命周期是结构体类型的一部分。

　　在 `impl` 块内的方法签名中，引用可能与结构体字段中引用的生命周期绑定，也可能彼此独立。此外，生命周期省略规则常常使方法签名中不必写生命周期注解。我们用示例 10-24 中定义的结构体 `ImportantExcerpt` 看几个例子。

　　首先，使用名为 `level` 的方法：其唯一参数是对 `self` 的引用，返回值是 `i32`，不是对任何东西的引用：

```rust
impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

　　`impl` 后的生命周期参数声明及其在类型名后的使用是必需的，但由于第一条省略规则，我们不必标注对 `self` 的引用的生命周期。

　　下面是第三条生命周期省略规则适用的例子：

```rust
impl<'a> ImportantExcerpt<'a> {
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {announcement}");
        self.part
    }
}
```

　　有两个输入生命周期，因此 Rust 应用第一条省略规则，给 `&self` 与 `announcement` 各自的生命周期。然后，因为其中一个参数是 `&self`，返回类型获得 `&self` 的生命周期，所有生命周期就都确定了。

### 静态生命周期

　　需要讨论的一个特殊生命周期是 `'static`，它表示受影响的引用*可以*存活于整个程序期间。所有字符串字面量都具有 `'static` 生命周期，可以这样标注：

```rust
let s: &'static str = "I have a static lifetime.";
```

　　该字符串的文本直接存储在程序的二进制中，始终可用。因此所有字符串字面量的生命周期都是 `'static`。

　　你可能在错误信息中看到建议使用 `'static` 生命周期。但在把引用的生命周期指定为 `'static` 之前，先想想：你拥有的引用是否真的存活于整个程序生命周期，以及你是否希望如此。多数时候，建议 `'static` 的错误信息来自试图创建悬垂引用，或可用生命周期不匹配。那种情况下，解决办法是修复那些问题，而不是指定 `'static` 生命周期。

## 泛型类型参数、Trait 约束与生命周期

　　我们简要看看在同一个函数中同时指定泛型类型参数、trait 约束与生命周期的语法！

```rust
use std::fmt::Display;

fn longest_with_an_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> &'a str
where
    T: Display,
{
    println!("Announcement! {ann}");
    if x.len() > y.len() { x } else { y }
}
```

　　这是示例 10-21 中返回两个字符串切片中较长者的 `longest` 函数。但现在它多了一个名为 `ann`、类型为泛型 `T` 的参数，可由任何实现了 `Display` trait 的类型填入（由 `where` 子句指定）。这个额外参数会用 `{}` 打印，因此需要 `Display` trait 约束。因为生命周期也是一种泛型，生命周期参数 `'a` 与泛型类型参数 `T` 的声明都放在函数名后同一组尖括号列表中。

## 小结

　　本章内容很多！既然了解了泛型类型参数、trait 与 trait 约束，以及泛型生命周期参数，你就可以写出不重复、又能在许多不同场景下工作的代码。泛型类型参数让你把代码应用到不同的类型。Trait 与 trait 约束确保：即便类型是泛型的，也会具有代码所需的行为。你学会了如何用生命周期注解确保这种灵活的代码不会有悬垂引用。而这一切分析都发生在编译期，不影响运行时性能！

　　信不信由你，我们讨论的主题还有更多可学：第 18 章讨论 trait 对象，那是使用 trait 的另一种方式。还有一些仅在非常高级的场景中才需要的、涉及生命周期注解的更复杂情形；那些应阅读 [Rust 参考手册][reference]。不过接下来，你会学习如何在 Rust 中编写测试，以确保代码按预期工作。

[references-and-borrowing]: ../../understanding-ownership/02-references-and-borrowing/
[string-slices-as-parameters]: ../../understanding-ownership/03-slices/#string-slices-as-parameters
[reference]: https://doc.rust-lang.org/reference/trait-bounds.html
