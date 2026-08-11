+++
title = "13.2 用迭代器处理一系列项"
date = 2026-08-05T08:44:00+08:00
weight = 58
type = "docs"
description = "讲解 Iterator 特征、消费适配器与迭代器适配器"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用迭代器处理一系列项


> 原文链接: [https://doc.rust-lang.org/stable/book/ch13-02-iterators.html](https://doc.rust-lang.org/stable/book/ch13-02-iterators.html)


## 用迭代器处理一系列项

　　迭代器模式让你能依次对序列中的各项执行某项任务。迭代器负责遍历每一项的逻辑，并判断序列何时结束。使用迭代器时，不必自己反复实现那套逻辑。

　　在 Rust 中，迭代器是*惰性的*（lazy）：在调用会消耗迭代器的方法之前，它们不会产生任何效果。例如，示例 13-10 通过对 `Vec<T>` 调用 `iter`，为向量 `v1` 中的项创建了迭代器。单凭这段代码本身并没有什么实际作用。

**文件名：`src/main.rs`**
```rust
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();
```

**示例 13-10：创建一个迭代器**

　　迭代器保存在变量 `v1_iter` 中。创建之后，可以用多种方式使用它。在示例 3-5 中，我们用 `for` 循环遍历数组并对每一项执行代码。实际上，这会隐式创建并消耗一个迭代器，但当时我们略过了具体机制。

　　示例 13-11 把迭代器的创建与在 `for` 循环中的使用分开。当 `for` 循环使用 `v1_iter` 中的迭代器时，迭代器的每个元素都会在循环的一轮迭代中被使用，从而打印每个值。

**文件名：`src/main.rs`**
```rust
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();

    for val in v1_iter {
        println!("Got: {val}");
    }
```

**示例 13-11：在 `for` 循环中使用迭代器**

　　在标准库不提供迭代器的语言里，你多半会这样实现同样功能：从索引 0 的变量开始，用它索引向量取值，在循环中递增该变量，直到达到向量中的项数。

　　迭代器替你处理了所有这些逻辑，减少了可能写错的重复代码。迭代器还让你更灵活地把同一套逻辑用于多种序列，而不仅是像向量那样可索引的数据结构。下面看看它是怎么做到的。

### `Iterator` 特征与 `next` 方法 {#the-iterator-trait-and-the-next-method}

　　所有迭代器都实现标准库中名为 `Iterator` 的特征。该特征的定义大致如下：

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

　　注意这里用了新语法：`type Item` 和 `Self::Item`，它们为该特征定义了一个关联类型。第 20 章会深入讲解关联类型。眼下只需知道：实现 `Iterator` 特征时必须定义 `Item` 类型，而这个 `Item` 会用作 `next` 方法的返回类型。换言之，`Item` 就是迭代器返回的类型。

　　`Iterator` 特征只要求实现者定义一个方法：`next`。它每次返回迭代器中的一项（包在 `Some` 里），迭代结束时返回 `None`。

　　我们可以直接对迭代器调用 `next`；示例 13-12 演示了对从向量创建的迭代器反复调用 `next` 会返回什么。

**文件名：`src/lib.rs`**
```rust
    #[test]
    fn iterator_demonstration() {
        let v1 = vec![1, 2, 3];

        let mut v1_iter = v1.iter();

        assert_eq!(v1_iter.next(), Some(&1));
        assert_eq!(v1_iter.next(), Some(&2));
        assert_eq!(v1_iter.next(), Some(&3));
        assert_eq!(v1_iter.next(), None);
    }
```

**示例 13-12：对迭代器调用 `next` 方法**

　　注意我们需要让 `v1_iter` 可变：对迭代器调用 `next` 会改变其内部状态，用以跟踪序列中的当前位置。换言之，这段代码会*消耗*（consume）迭代器。每次调用 `next` 都会吃掉迭代器中的一项。用 `for` 循环时不必把 `v1_iter` 标为可变，因为循环会取得 `v1_iter` 的所有权，并在背后把它变成可变的。

　　还要注意：从 `next` 得到的值是对向量中值的不可变引用。`iter` 方法产生的是不可变引用的迭代器。若想创建取得 `v1` 所有权并返回所有权值的迭代器，可调用 `into_iter` 而不是 `iter`。同理，若要迭代可变引用，可调用 `iter_mut` 而不是 `iter`。

### 消耗迭代器的方法

　　`Iterator` 特征有许多带默认实现的方法，可在标准库 API 文档的 `Iterator` 特征页面查阅。其中一些方法会在定义中调用 `next`，这也是实现 `Iterator` 时必须实现 `next` 的原因。

　　调用 `next` 的方法称为*消费适配器*（consuming adapter），因为调用它们会用尽迭代器。一个例子是 `sum` 方法：它取得迭代器的所有权，通过反复调用 `next` 遍历各项，从而消耗迭代器；遍历时把各项加到累计和中，迭代结束后返回总和。示例 13-13 的测试演示了 `sum` 的用法。

**文件名：`src/lib.rs`**
```rust
    #[test]
    fn iterator_sum() {
        let v1 = vec![1, 2, 3];

        let v1_iter = v1.iter();

        let total: i32 = v1_iter.sum();

        assert_eq!(total, 6);
    }
```

**示例 13-13：调用 `sum` 方法求迭代器中所有项的总和**

　　调用 `sum` 之后不能再使用 `v1_iter`，因为 `sum` 取得了被调用迭代器的所有权。

### 产生其他迭代器的方法

　　*迭代器适配器*（iterator adapter）是定义在 `Iterator` 特征上、不会消耗迭代器的方法。它们通过改变原迭代器的某些方面，产生不同的迭代器。

　　示例 13-14 展示了对迭代器适配器方法 `map` 的调用：它接收一个闭包，在遍历各项时对每一项调用该闭包。`map` 返回一个产生修改后各项的新迭代器。这里的闭包创建的新迭代器中，向量的每一项都会加 1。

**文件名：`src/main.rs`**
```rust
    let v1: Vec<i32> = vec![1, 2, 3];

    v1.iter().map(|x| x + 1);
```

**示例 13-14：调用迭代器适配器 `map` 创建新迭代器**

　　不过这段代码会产生警告：

```console
$ cargo run
   Compiling iterators v0.1.0 (file:///projects/iterators)
warning: unused `Map` that must be used
 --> src/main.rs:4:5
  |
4 |     v1.iter().map(|x| x + 1);
  |     ^^^^^^^^^^^^^^^^^^^^^^^^
  |
  = note: iterators are lazy and do nothing unless consumed
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
  |
4 |     let _ = v1.iter().map(|x| x + 1);
  |     +++++++

warning: `iterators` (bin "iterators") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.47s
     Running `target/debug/iterators`
```

　　示例 13-14 的代码实际上什么也没做；我们指定的闭包从未被调用。警告提醒了原因：迭代器适配器是惰性的，这里需要消耗迭代器。

　　要消除警告并消耗迭代器，可使用我们在示例 12-1 中与 `env::args` 一起用过的 `collect` 方法。它会消耗迭代器，并把结果值收集进某种集合数据类型。

　　示例 13-15 把对 `map` 返回的迭代器遍历的结果收集进一个向量。该向量最终包含原向量中每一项加 1 后的值。

**文件名：`src/main.rs`**
```rust
    let v1: Vec<i32> = vec![1, 2, 3];

    let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();

    assert_eq!(v2, vec![2, 3, 4]);
```

**示例 13-15：调用 `map` 创建新迭代器，再调用 `collect` 消耗它并创建向量**

　　因为 `map` 接收闭包，你可以指定想对每一项执行的任意操作。这很好地说明了：闭包让你自定义部分行为，同时复用 `Iterator` 特征提供的迭代行为。

　　你可以链式调用多个迭代器适配器，以可读的方式完成复杂操作。但因为所有迭代器都是惰性的，要从迭代器适配器的调用中得到结果，必须再调用某个消费适配器方法。

### 捕获其环境的闭包

　　许多迭代器适配器以闭包为参数，而我们传给它们的闭包常常会捕获其环境。

　　本例使用接收闭包的 `filter` 方法。闭包从迭代器取得一项并返回 `bool`：若返回 `true`，该值会包含在 `filter` 产生的迭代器中；若返回 `false`，则不会包含。

　　示例 13-16 用 `filter` 和一个从环境捕获 `shoe_size` 的闭包，遍历 `Shoe` 结构体实例的集合，只返回指定尺码的鞋。

**文件名：`src/lib.rs`**
```rust
#[derive(PartialEq, Debug)]
struct Shoe {
    size: u32,
    style: String,
}

fn shoes_in_size(shoes: Vec<Shoe>, shoe_size: u32) -> Vec<Shoe> {
    shoes.into_iter().filter(|s| s.size == shoe_size).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn filters_by_size() {
        let shoes = vec![
            Shoe {
                size: 10,
                style: String::from("sneaker"),
            },
            Shoe {
                size: 13,
                style: String::from("sandal"),
            },
            Shoe {
                size: 10,
                style: String::from("boot"),
            },
        ];

        let in_my_size = shoes_in_size(shoes, 10);

        assert_eq!(
            in_my_size,
            vec![
                Shoe {
                    size: 10,
                    style: String::from("sneaker")
                },
                Shoe {
                    size: 10,
                    style: String::from("boot")
                },
            ]
        );
    }
}
```

**示例 13-16：用捕获 `shoe_size` 的闭包配合 `filter` 方法**

　　`shoes_in_size` 函数取得鞋向量的所有权以及一个鞋码作为参数，返回只包含指定尺码鞋子的向量。

　　在函数体中，先调用 `into_iter` 创建取得向量所有权的迭代器，再调用 `filter`，把它适配成只包含闭包返回 `true` 的元素的新迭代器。

　　闭包从环境捕获 `shoe_size` 参数，与每只鞋的尺码比较，只保留指定尺码的鞋。最后调用 `collect`，把适配后迭代器返回的值收集进向量并由函数返回。

　　测试表明：调用 `shoes_in_size` 时，只会得到与指定尺码相同的鞋。
