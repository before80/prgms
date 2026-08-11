+++
title = "13.1 闭包"
date = 2026-08-05T08:44:00+08:00
weight = 57
type = "docs"
description = "讲解闭包语法、捕获环境与 Fn、FnMut、FnOnce 特征"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 闭包


> 原文链接: [https://doc.rust-lang.org/stable/book/ch13-01-closures.html](https://doc.rust-lang.org/stable/book/ch13-01-closures.html)


## 闭包

　　Rust 的闭包是可以保存在变量中、或作为参数传给其他函数的匿名函数。你可以在一处创建闭包，再在别处调用它，以便在不同上下文中求值。与函数不同，闭包可以捕获定义它们的作用域中的值。下面演示这些闭包特性如何带来代码复用与行为定制。

### 捕获环境

　　我们先看看如何用闭包捕获定义时所在环境中的值，供稍后使用。场景如下：我们的 T 恤公司偶尔会向邮件列表中的某人赠送限量版专属衬衫作为促销。列表上的人可以选择在资料中填写最喜欢的颜色。若获赠者设置了喜欢的颜色，就送该颜色衬衫；若未指定，则送公司当前库存最多的那种颜色。

　　实现方式有很多。本例使用枚举 `ShirtColor`，变体为 `Red` 和 `Blue`（为简单起见限制颜色数量）。用结构体 `Inventory` 表示公司库存，其字段 `shirts` 是 `Vec<ShirtColor>`，表示当前库存衬衫的颜色。定义在 `Inventory` 上的方法 `giveaway` 取得免费衬衫获奖者可选的颜色偏好，并返回此人将得到的衬衫颜色。设置如示例 13-1 所示。

**文件名：`src/main.rs`**
```rust
#[derive(Debug, PartialEq, Copy, Clone)]
enum ShirtColor {
    Red,
    Blue,
}

struct Inventory {
    shirts: Vec<ShirtColor>,
}

impl Inventory {
    fn giveaway(&self, user_preference: Option<ShirtColor>) -> ShirtColor {
        user_preference.unwrap_or_else(|| self.most_stocked())
    }

    fn most_stocked(&self) -> ShirtColor {
        let mut num_red = 0;
        let mut num_blue = 0;

        for color in &self.shirts {
            match color {
                ShirtColor::Red => num_red += 1,
                ShirtColor::Blue => num_blue += 1,
            }
        }
        if num_red > num_blue {
            ShirtColor::Red
        } else {
            ShirtColor::Blue
        }
    }
}

fn main() {
    let store = Inventory {
        shirts: vec![ShirtColor::Blue, ShirtColor::Red, ShirtColor::Blue],
    };

    let user_pref1 = Some(ShirtColor::Red);
    let giveaway1 = store.giveaway(user_pref1);
    println!(
        "The user with preference {:?} gets {:?}",
        user_pref1, giveaway1
    );

    let user_pref2 = None;
    let giveaway2 = store.giveaway(user_pref2);
    println!(
        "The user with preference {:?} gets {:?}",
        user_pref2, giveaway2
    );
}
```

**示例 13-1：T 恤公司赠送活动场景**

　　`main` 中定义的 `store` 在这次限量促销中还剩两件蓝衬衫和一件红衬衫。我们分别对偏好红衬衫的用户和没有任何偏好的用户调用 `giveaway`。

　　同样，这段代码可以用许多方式实现；为聚焦闭包，除了使用闭包的 `giveaway` 方法体外，我们只用了你已学过的概念。在 `giveaway` 中，用户偏好是类型为 `Option<ShirtColor>` 的参数，我们对其调用 `unwrap_or_else`。[`Option<T>` 上的 `unwrap_or_else` 方法][unwrap-or-else] 由标准库定义。它接收一个参数：不带参数并返回 `T` 的闭包（与 `Option<T>` 的 `Some` 变体中存储的类型相同，这里是 `ShirtColor`）。若 `Option<T>` 是 `Some`，`unwrap_or_else` 返回其中的值；若是 `None`，则调用闭包并返回闭包的返回值。

　　我们把闭包表达式 `|| self.most_stocked()` 作为参数传给 `unwrap_or_else`。这是一个本身不带参数的闭包（若有参数，会写在两条竖线之间）。闭包体调用 `self.most_stocked()`。我们在这里定义闭包，而 `unwrap_or_else` 的实现会在需要结果时再求值该闭包。

　　运行这段代码会打印：

```console
$ cargo run
   Compiling shirt-company v0.1.0 (file:///projects/shirt-company)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.27s
     Running `target/debug/shirt-company`
The user with preference Some(Red) gets Red
The user with preference None gets Blue
```

　　这里有趣的一点是：我们传入的闭包会在当前 `Inventory` 实例上调用 `self.most_stocked()`。标准库不必了解我们定义的 `Inventory` 或 `ShirtColor` 类型，也不必了解本场景要用的逻辑。闭包捕获了对 `self` 这个 `Inventory` 实例的不可变引用，并连同我们指定的代码一起传给 `unwrap_or_else`。函数则无法以这种方式捕获其环境。

### 推断与标注闭包类型 {#closure-type-inference-and-annotation}

　　函数与闭包还有更多区别。闭包通常不必像 `fn` 函数那样标注参数或返回值的类型。函数需要类型标注，因为类型是暴露给用户的显式接口的一部分。严格定义该接口，对确保各方就函数使用与返回的值类型达成一致很重要。闭包则不同：它们存在变量里，使用时不必命名，也不会作为库的接口暴露给用户。

　　闭包通常很短，且只在狭窄上下文中有意义，而非任意场景。在这些有限上下文中，编译器能推断参数类型和返回类型，就像能推断大多数变量的类型一样（少数情况下编译器也需要闭包类型标注）。

　　与变量一样，若想增加明确性与清晰度，也可以添加类型标注，代价是比严格必要的写法更冗长。为闭包标注类型看起来会像示例 13-2。本例中我们定义闭包并存进变量，而不是像示例 13-1 那样在传参处内联定义。

**文件名：`src/main.rs`**
```rust
    let expensive_closure = |num: u32| -> u32 {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    };
```

**示例 13-2：在闭包中为参数和返回值类型添加可选标注**

　　加上类型标注后，闭包语法更接近函数语法。下面定义一个参数加 1 的函数，以及行为相同的闭包以便对比。我们加了一些空格对齐相关部分。可以看出：除了使用竖线，以及有多少语法可选之外，闭包语法与函数语法很相似：

```rust
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

　　第一行是函数定义，第二行是完整标注的闭包定义。第三行去掉了闭包的类型标注。第四行去掉了花括号——因为闭包体只有一个表达式，花括号可选。这些都是有效定义，调用时行为相同。`add_one_v3` 和 `add_one_v4` 需要先对闭包求值才能编译，因为类型要从用法推断。这类似于 `let v = Vec::new();` 需要类型标注或向 `Vec` 插入某类型的值，Rust 才能推断类型。

　　对闭包定义，编译器会为每个参数和返回值推断出一种具体类型。例如示例 13-3 定义了一个很短的闭包，只是返回收到的参数值。除了本例的目的外它没什么用。注意定义中没有任何类型标注。因为没有类型标注，我们可以用任意类型调用该闭包——第一次用了 `String`。若再尝试用整数调用 `example_closure`，就会得到错误。

**文件名：`src/main.rs`**
```rust
    let example_closure = |x| x;

    let s = example_closure(String::from("hello"));
    let n = example_closure(5);
```

**示例 13-3：尝试用两种不同的类型调用类型被推断的闭包**

　　编译器给出这样的错误：

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
error[E0308]: mismatched types
 --> src/main.rs:5:29
  |
5 |     let n = example_closure(5);
  |             --------------- ^ expected `String`, found integer
  |             |
  |             arguments to this function are incorrect
  |
note: expected because the closure was earlier called with an argument of type `String`
 --> src/main.rs:4:29
  |
4 |     let s = example_closure(String::from("hello"));
  |             --------------- ^^^^^^^^^^^^^^^^^^^^^ expected because this argument is of type `String`
  |             |
  |             in this closure call
note: closure parameter defined here
 --> src/main.rs:2:28
  |
2 |     let example_closure = |x| x;
  |                            ^
help: try using a conversion method
  |
5 |     let n = example_closure(5.to_string());
  |                              ++++++++++++

For more information about this error, try `rustc --explain E0308`.
error: could not compile `closure-example` (bin "closure-example") due to 1 previous error
```

　　第一次用 `String` 值调用 `example_closure` 时，编译器推断 `x` 和闭包返回类型为 `String`。这些类型随即锁定在 `example_closure` 中的闭包上；再用不同类型调用同一闭包就会得到类型错误。

### 捕获引用或转移所有权 {#capturing-references-or-moving-ownership}

　　闭包可以用三种方式从环境捕获值，直接对应函数接收参数的三种方式：不可变借用、可变借用，以及取得所有权。闭包会根据函数体如何使用被捕获的值来决定采用哪一种。

　　示例 13-4 定义了一个闭包，它捕获对名为 `list` 的向量的不可变引用，因为打印该值只需要不可变引用。

**文件名：`src/main.rs`**
```rust
fn main() {
    let list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    let only_borrows = || println!("From closure: {list:?}");

    println!("Before calling closure: {list:?}");
    only_borrows();
    println!("After calling closure: {list:?}");
}
```

**示例 13-4：定义并调用捕获不可变引用的闭包**

　　本例也说明：变量可以绑定到闭包定义，之后可以用变量名加括号像调用函数一样调用该闭包。

　　因为可以同时存在多个对 `list` 的不可变引用，所以在闭包定义之前、定义之后但调用之前，以及调用之后，代码仍可访问 `list`。这段代码能编译、运行并打印：

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/closure-example`
Before defining closure: [1, 2, 3]
Before calling closure: [1, 2, 3]
From closure: [1, 2, 3]
After calling closure: [1, 2, 3]
```

　　接下来在示例 13-5 中，我们改闭包体，让它向 `list` 向量添加元素。此时闭包捕获的是可变引用。

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    let mut borrows_mutably = || list.push(7);

    borrows_mutably();
    println!("After calling closure: {list:?}");
}
```

**示例 13-5：定义并调用捕获可变引用的闭包**

　　这段代码能编译、运行并打印：

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/closure-example`
Before defining closure: [1, 2, 3]
After calling closure: [1, 2, 3, 7]
```

　　注意：在定义与调用 `borrows_mutably` 闭包之间不再有 `println!`。定义 `borrows_mutably` 时，它捕获了对 `list` 的可变引用。调用后我们不再使用该闭包，因此可变借用结束。在闭包定义与调用之间，不允许再有用于打印的不可变借用，因为存在可变借用时不允许其他借用。试着在那里加一个 `println!`，看看会得到什么错误信息！

　　若希望即使闭包体并不严格需要所有权，也强制闭包取得环境中所用值的所有权，可以在参数列表前使用 `move` 关键字。

　　这种技巧主要用于把闭包传给新线程，从而把数据移入并由新线程拥有。第 16 章讨论并发时会详细讲解线程以及为何要用它们；眼下先简要看看用需要 `move` 关键字的闭包生成新线程。示例 13-6 在示例 13-4 基础上修改，改为在新线程而不是主线程中打印向量。

**文件名：`src/main.rs`**
```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    thread::spawn(move || println!("From thread: {list:?}"))
        .join()
        .unwrap();
}
```

**示例 13-6：用 `move` 强制线程的闭包取得 `list` 的所有权**

　　我们生成一个新线程，并把要运行的闭包作为参数传给它。闭包体打印该列表。在示例 13-4 中，闭包只用不可变引用捕获 `list`，因为打印只需要最少限度的访问。本例中，即便闭包体仍只需要不可变引用，也必须在闭包定义开头加上 `move`，指明 `list` 应移入闭包。若主线程在对新线程调用 `join` 之前还执行更多操作，新线程可能先结束，也可能主线程先结束。若主线程仍拥有 `list` 却先结束并丢弃了 `list`，线程中的不可变引用就会失效。因此编译器要求把 `list` 移入传给新线程的闭包，以保证引用有效。试着去掉 `move`，或在闭包定义后于主线程使用 `list`，看看会得到什么编译错误！

### 把捕获的值移出闭包 {#moving-captured-values-out-of-closures}

　　一旦闭包从定义它的环境中捕获了引用或取得了值的所有权（从而影响有什么东西——若有的话——被移*入*闭包），闭包体中的代码就决定了稍后求值时这些引用或值会发生什么（从而影响有什么东西——若有的话——被移*出*闭包）。

　　闭包体可以做以下任一事情：把捕获的值移出闭包、修改捕获的值、既不移动也不修改该值，或者一开始就不从环境捕获任何东西。

　　闭包捕获与处理环境中值的方式，会影响它实现哪些特征；而特征正是函数和结构体用来规定能接受何种闭包的方式。闭包会自动以累加方式实现下列 `Fn` 特征中的一个、两个或全部三个，具体取决于闭包体如何处理这些值：

* `FnOnce` 适用于可调用一次的闭包。所有闭包至少实现该特征，因为所有闭包都能被调用。若闭包把捕获的值移出其函数体，则只实现 `FnOnce` 而不实现其他 `Fn` 特征，因为它只能被调用一次。
* `FnMut` 适用于不会把捕获值移出函数体、但可能修改捕获值的闭包。这类闭包可被多次调用。
* `Fn` 适用于既不把捕获值移出函数体、也不修改捕获值的闭包，以及不从环境捕获任何东西的闭包。这类闭包可被多次调用且不修改其环境，这在例如并发多次调用同一闭包时很重要。

　　来看示例 13-1 中用过的 `Option<T>` 上 `unwrap_or_else` 方法的定义：

```rust
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

　　回想一下：`T` 是表示 `Option` 的 `Some` 变体中值类型的泛型类型。该类型 `T` 也是 `unwrap_or_else` 函数的返回类型：例如对 `Option<String>` 调用 `unwrap_or_else` 会得到 `String`。

　　接下来注意 `unwrap_or_else` 还有额外的泛型类型参数 `F`。`F` 是名为 `f` 的参数的类型，也就是调用 `unwrap_or_else` 时提供的闭包。

　　泛型类型 `F` 上的特征约束是 `FnOnce() -> T`，表示 `F` 必须能被调用一次、不接收参数，并返回 `T`。在特征约束中使用 `FnOnce` 表达了这样的限制：`unwrap_or_else` 不会多次调用 `f`。在函数体中可以看到：若 `Option` 是 `Some`，不会调用 `f`；若是 `None`，会调用一次 `f`。因为所有闭包都实现 `FnOnce`，`unwrap_or_else` 接受全部三种闭包，灵活度尽可能高。

> 注意：若我们想做的事并不需要从环境捕获值，可以在需要实现某个 `Fn` 特征的地方使用函数名而不是闭包。例如，对 `Option<Vec<T>>` 值可以调用 `unwrap_or_else(Vec::new)`，在值为 `None` 时得到新的空向量。编译器会自动为函数定义实现适用的 `Fn` 特征。

　　再看定义在切片上的标准库方法 `sort_by_key`，了解它与 `unwrap_or_else` 有何不同，以及为何特征约束用 `FnMut` 而不是 `FnOnce`。该闭包接收一个参数，形式是对当前正在考虑的切片项的引用，并返回可排序的类型 `K` 的值。当你想按每项的某个特定属性排序切片时，这个函数很有用。示例 13-7 中有一组 `Rectangle` 实例，我们用 `sort_by_key` 按 `width` 属性从低到高排序。

**文件名：`src/main.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    list.sort_by_key(|r| r.width);
    println!("{list:#?}");
}
```

**示例 13-7：用 `sort_by_key` 按宽度对矩形排序**

　　这段代码打印：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/rectangles`
[
    Rectangle {
        width: 3,
        height: 5,
    },
    Rectangle {
        width: 7,
        height: 12,
    },
    Rectangle {
        width: 10,
        height: 1,
    },
]
```

　　`sort_by_key` 定义为接收 `FnMut` 闭包，是因为它会多次调用该闭包：切片中每一项一次。闭包 `|r| r.width` 不捕获、不修改、也不从环境移出任何东西，因此满足特征约束。

　　相比之下，示例 13-8 展示了一个只实现 `FnOnce` 的闭包，因为它把值移出了环境。编译器不允许把这个闭包用于 `sort_by_key`。

**文件名：`src/main.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    let mut sort_operations = vec![];
    let value = String::from("closure called");

    list.sort_by_key(|r| {
        sort_operations.push(value);
        r.width
    });
    println!("{list:#?}");
}
```

**示例 13-8：尝试在 `sort_by_key` 中使用 `FnOnce` 闭包**

　　这是一种刻意绕弯、实际上行不通的写法，试图统计对 `list` 排序时 `sort_by_key` 调用闭包的次数。它把来自闭包环境的 `String` 值 `value` 推进 `sort_operations` 向量来计数。闭包捕获 `value`，再通过把 `value` 的所有权转移给 `sort_operations` 向量而把 `value` 移出闭包。该闭包只能调用一次；再调用第二次行不通，因为环境中已没有 `value` 可再推进 `sort_operations`！因此它只实现 `FnOnce`。尝试编译时会得到错误：`value` 不能移出闭包，因为闭包必须实现 `FnMut`：

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
error[E0507]: cannot move out of `value`, a captured variable in an `FnMut` closure
  --> src/main.rs:18:30
   |
15 |     let value = String::from("closure called");
   |         -----   ------------------------------ move occurs because `value` has type `String`, which does not implement the `Copy` trait
   |         |
   |         captured outer variable
16 |
17 |     list.sort_by_key(|r| {
   |                      --- captured by this `FnMut` closure
18 |         sort_operations.push(value);
   |                              ^^^^^ `value` is moved here
   |
help: `Fn` and `FnMut` closures require captured values to be able to be consumed multiple times, but `FnOnce` closures may consume them only once
  --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/alloc/src/slice.rs:249:11
help: consider cloning the value if the performance cost is acceptable
   |
18 |         sort_operations.push(value.clone());
   |                                   ++++++++

For more information about this error, try `rustc --explain E0507`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

　　错误指向闭包体中把 `value` 移出环境的那一行。要修复它，需要改闭包体，使其不把值移出环境。在环境中保留一个计数器并在闭包体中递增，是统计闭包调用次数更直接的方式。示例 13-9 中的闭包可以与 `sort_by_key` 一起使用，因为它只捕获对计数器 `num_sort_operations` 的可变引用，因此可以多次调用。

**文件名：`src/main.rs`**
```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    let mut num_sort_operations = 0;
    list.sort_by_key(|r| {
        num_sort_operations += 1;
        r.width
    });
    println!("{list:#?}, sorted in {num_sort_operations} operations");
}
```

**示例 13-9：允许在 `sort_by_key` 中使用 `FnMut` 闭包**

　　在定义或使用依赖闭包的函数或类型时，`Fn` 特征很重要。下一节讨论迭代器。许多迭代器方法接收闭包参数，请在继续学习时记住这些闭包细节！

[unwrap-or-else]: https://doc.rust-lang.org/stable/std/option/enum.Option.html#method.unwrap_or_else
