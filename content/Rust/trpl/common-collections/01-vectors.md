+++
title = "8.1 用向量存储值的列表"
date = 2026-08-05T08:44:00+08:00
weight = 34
type = "docs"
description = "创建、更新、读取与遍历 Vec，并用枚举存放多种类型"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用向量存储值的列表


> 原文链接: [https://doc.rust-lang.org/stable/book/ch08-01-vectors.html](https://doc.rust-lang.org/stable/book/ch08-01-vectors.html)


## 用向量存储值的列表

　　我们要看的第一种集合类型是 `Vec<T>`，也称为向量（vector）。向量让你能把多个值存放在同一个数据结构中，并在内存里彼此相邻。向量只能存放相同类型的值。当你有一份列表时——例如文件中的文本行，或购物车里商品的价格——向量就很有用。

### 创建新向量

　　要创建一个新的空向量，我们调用 `Vec::new` 函数，如示例 8-1 所示。

```rust
    let v: Vec<i32> = Vec::new();
```

**示例 8-1：创建一个用来存放 `i32` 类型值的新空向量**

　　注意这里我们加了类型注解。因为还没有向这个向量插入任何值，Rust 不知道我们打算存放哪种元素。这一点很重要。向量是用泛型实现的；我们将在第 10 章介绍如何在自己的类型上使用泛型。现在只需知道，标准库提供的 `Vec<T>` 类型可以存放任意类型。创建用于存放特定类型的向量时，可以在尖括号中指定类型。在示例 8-1 中，我们告诉 Rust：`v` 中的 `Vec<T>` 将存放 `i32` 类型的元素。

　　更常见的情况是，你会带着初始值创建 `Vec<T>`，Rust 会推断你想存放的值的类型，因此很少需要写这种类型注解。Rust 还方便地提供了 `vec!` 宏，它会创建一个包含你所给值的新向量。示例 8-2 创建了一个包含值 `1`、`2` 和 `3` 的新 `Vec<i32>`。整数类型是 `i32`，因为那是默认的整数类型，正如我们在第 3 章[「数据类型」][data-types]一节中讨论的。

```rust
    let v = vec![1, 2, 3];
```

**示例 8-2：创建一个包含值的新向量**

　　因为我们给出了初始的 `i32` 值，Rust 可以推断出 `v` 的类型是 `Vec<i32>`，因此不需要类型注解。接下来看看如何修改向量。

### 更新向量

　　要创建向量并向其中添加元素，可以使用 `push` 方法，如示例 8-3 所示。

```rust
    let mut v = Vec::new();

    v.push(5);
    v.push(6);
    v.push(7);
    v.push(8);
```

**示例 8-3：用 `push` 方法向向量添加值**

　　与任何变量一样，若希望能够改变它的值，就需要用 `mut` 关键字使其可变，这在第 3 章讨论过。我们放入的数字都是 `i32` 类型，Rust 会从数据中推断出来，因此不需要 `Vec<i32>` 注解。

### 读取向量中的元素

　　引用向量中存储的值有两种方式：通过索引，或使用 `get` 方法。在下面的例子中，我们为这些函数返回值的类型加了注解，以便更清晰。

　　示例 8-4 展示了访问向量中某个值的两种方法：索引语法和 `get` 方法。

```rust
    let v = vec![1, 2, 3, 4, 5];

    let third: &i32 = &v[2];
    println!("The third element is {third}");

    let third: Option<&i32> = v.get(2);
    match third {
        Some(third) => println!("The third element is {third}"),
        None => println!("There is no third element."),
    }
```

**示例 8-4：使用索引语法和 `get` 方法访问向量中的项**

　　这里有几处细节需要注意。我们用索引值 `2` 获取第三个元素，因为向量按数字索引，且从零开始。使用 `&` 和 `[]` 会得到该索引处元素的引用。当我们把索引作为参数传给 `get` 方法时，会得到一个可以配合 `match` 使用的 `Option<&T>`。

　　Rust 提供这两种引用元素的方式，是为了让你可以选择：当试图使用超出已有元素范围的索引时，程序应如何表现。例如，假设我们有一个包含五个元素的向量，然后分别用这两种技巧访问索引 100 处的元素，如示例 8-5 所示。

```rust
    let v = vec![1, 2, 3, 4, 5];

    let does_not_exist = &v[100];
    let does_not_exist = v.get(100);
```

**示例 8-5：尝试访问含五个元素的向量中索引为 100 的元素**

　　运行这段代码时，第一种 `[]` 方法会使程序 panic，因为它引用了不存在的元素。若你希望一旦有人尝试访问向量末尾之后的元素程序就崩溃，用这种方法最合适。

　　当传给 `get` 方法的索引超出向量范围时，它会返回 `None` 而不会 panic。若在正常情况下偶尔可能访问到向量范围之外的元素，就适合用这种方法。然后你的代码需要有处理 `Some(&element)` 或 `None` 的逻辑，正如第 6 章所讨论的。例如，索引可能来自用户输入的数字。若他们不小心输入了过大的数字，程序得到 `None`，你就可以告诉用户当前向量中有多少项，并再给他们一次输入有效值的机会。这比因用户一次输入错误就让程序崩溃要友好得多！

　　当程序持有有效引用时，借用检查器会强制执行所有权与借用规则（第 4 章讲过），以确保该引用以及指向向量内容的任何其他引用都保持有效。回想那条规则：不能在同一作用域中同时拥有可变引用和不可变引用。示例 8-6 就适用这条规则：我们持有向量第一个元素的不可变引用，又试图在末尾添加一个元素。若我们还想在函数后面引用那个元素，这个程序就无法工作。

```rust
    let mut v = vec![1, 2, 3, 4, 5];

    let first = &v[0];

    v.push(6);

    println!("The first element is: {first}");
```

**示例 8-6：在持有某项引用的同时尝试向向量添加元素**

　　编译这段代码会得到如下错误：

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:6:5
  |
4 |     let first = &v[0];
  |                  - immutable borrow occurs here
5 |
6 |     v.push(6);
  |     ^^^^^^^^^ mutable borrow occurs here
7 |
8 |     println!("The first element is: {first}");
  |                                      ----- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `collections` (bin "collections") due to 1 previous error
```

　　示例 8-6 中的代码看起来似乎应该能工作：为什么对第一个元素的引用要关心向量末尾的改动？这个错误源于向量的工作方式：因为向量把值彼此相邻地放在内存中，若当前位置没有足够空间让所有元素继续相邻存放，在末尾添加新元素可能需要分配新内存，并把旧元素复制到新空间。那样的话，指向第一个元素的引用就会指向已释放的内存。借用规则阻止程序陷入这种局面。

> 注意：关于 `Vec<T>` 类型实现细节的更多内容，请参阅[《The Rustonomicon》][nomicon]。

### 遍历向量中的值

　　要依次访问向量中的每个元素，我们会遍历所有元素，而不是用索引一次取一个。示例 8-7 展示了如何用 `for` 循环获取 `i32` 值向量中每个元素的不可变引用并打印它们。

```rust
    let v = vec![100, 32, 57];
    for i in &v {
        println!("{i}");
    }
```

**示例 8-7：用 `for` 循环遍历元素并打印向量中的每一项**

　　我们也可以遍历可变向量中每个元素的可变引用，以便修改所有元素。示例 8-8 中的 `for` 循环会给每个元素加上 `50`。

```rust
    let mut v = vec![100, 32, 57];
    for i in &mut v {
        *i += 50;
    }
```

**示例 8-8：遍历向量中元素的可变引用**

　　要改变可变引用所指向的值，必须先用 `*` 解引用运算符得到 `i` 中的值，然后才能使用 `+=` 运算符。我们会在第 15 章[「跟随引用到达值」][deref]一节中更多地讨论解引用运算符。

　　无论是不可变还是可变地遍历向量，在借用检查器规则下都是安全的。若我们试图在示例 8-7 和示例 8-8 的 `for` 循环体中插入或删除项，就会得到与示例 8-6 代码类似的编译错误。`for` 循环所持有的对向量的引用，会阻止同时修改整个向量。

### 用枚举来存储多种类型

　　向量只能存放相同类型的值。这有时会不方便；确实存在需要存储不同类型项列表的用例。幸好，枚举的各个变体都定义在同一个枚举类型之下，因此当我们需要用一种类型表示不同类型的元素时，可以定义并使用枚举！

　　例如，假设我们要从电子表格的一行中取值，其中有些列是整数，有些是浮点数，有些是字符串。我们可以定义一个枚举，其变体分别持有不同的值类型，而所有枚举变体都被视为同一类型：即该枚举的类型。然后可以创建一个存放该枚举的向量，从而最终存放不同的类型。我们在示例 8-9 中演示了这一点。

```rust
    enum SpreadsheetCell {
        Int(i32),
        Float(f64),
        Text(String),
    }

    let row = vec![
        SpreadsheetCell::Int(3),
        SpreadsheetCell::Text(String::from("blue")),
        SpreadsheetCell::Float(10.12),
    ];
```

**示例 8-9：定义枚举以便在一个向量中存储不同类型的值**

　　Rust 需要在编译期知道向量中会有哪些类型，这样才能确切知道堆上存储每个元素需要多少内存。我们也必须明确指出这个向量允许哪些类型。若 Rust 允许向量存放任意类型，就可能有一种或多种类型会在对向量元素执行操作时引发错误。使用枚举加上 `match` 表达式，意味着 Rust 会在编译期确保每个可能的情况都被处理，正如第 6 章所讨论的。

　　若你在运行时才知道程序会把哪些完整类型集合存进向量，枚举技巧就不适用了。这时可以使用特征对象（trait object），我们会在第 18 章介绍。

　　既然我们已经讨论了使用向量的一些最常见方式，请务必查阅[API 文档][vec-api]，了解标准库在 `Vec<T>` 上定义的众多有用方法。例如，除了 `push`，还有 `pop` 方法可以移除并返回最后一个元素。

### 丢弃向量也会丢弃其元素

　　与任何其他 `struct` 一样，向量在离开作用域时会被释放，如示例 8-10 中的标注所示。

```rust
    {
        let v = vec![1, 2, 3, 4];

        // do stuff with v
    } // <- v goes out of scope and is freed here
```

**示例 8-10：展示向量及其元素被丢弃的位置**

　　当向量被丢弃时，其全部内容也会被丢弃，也就是说它所容纳的整数会被清理干净。借用检查器确保：对向量内容的任何引用，都只在向量本身仍然有效时才被使用。

　　让我们进入下一种集合类型：`String`！

[data-types]: /trpl/common-programming-concepts/02-data-types/#data-types
[nomicon]: https://doc.rust-lang.org/nomicon/vec/vec.html
[vec-api]: https://doc.rust-lang.org/stable/std/vec/struct.Vec.html
[deref]: /trpl/smart-pointers/02-deref/#following-the-pointer-to-the-value-with-the-dereference-operator
