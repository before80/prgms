+++
title = "20-拷贝类型"
date = 2026-08-21T12:46:00+08:00
weight = 21
type = "docs"
description = "拷贝类型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_19.html](https://dhghomon.github.io/easy_rust/Chapter_19.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 拷贝类型

Rust中的一些类型非常简单。它们被称为**拷贝类型**。这些简单的类型都在栈中，编译器知道它们的大小。这意味着它们非常容易复制，所以当你把它发送到一个函数时，编译器总是会复制。它总是复制，因为它们是如此的小而简单，没有理由不复制。所以你不需要担心这些类型的所有权问题。

这些简单的类型包括:整数、浮点数、布尔值(`true`和`false`)和`char`。

如何知道一个类型是否**实现**复制？(实现 = 能够使用)你可以查看文档。例如，这里是 char 的文档:

[https://doc.rust-lang.org/std/primitive.char.html](https://doc.rust-lang.org/std/primitive.char.html)

在左边你可以看到**Trait Implementations**。例如你可以看到**Copy**, **Debug**, 和 **Display**。所以你知道，当你把一个`char`:

- 当你把它发送到一个函数(**Copy**)时，它就被复制了。
- 可以用`{}`打印(**Display**)
- 可以用`{:?}`打印(**Debug**)

```rust
fn prints_number(number: i32) { // 没有 ->，所以不返回任何东西
                             // 如果 number 不是拷贝类型，函数会拿走它
                             // 我们就无法再用
    println!("{}", number);
}

fn main() {
    let my_number = 8;
    prints_number(my_number); // 打印 8。prints_number 得到 my_number 的副本
    prints_number(my_number); // 再打印 8。
                              // 没问题，因为 my_number 是拷贝类型！
}
```

但是如果你看一下String的文档，它不是拷贝类型。

[https://doc.rust-lang.org/std/string/struct.String.html](https://doc.rust-lang.org/std/string/struct.String.html)

在左边的**Trait Implementations**中，你可以按字母顺序查找。A、B、C......C中没有**Copy**，但是有**Clone**。**Clone**和**Copy**类似，但通常需要更多的内存。另外，你必须用`.clone()`来调用它--它不会自己克隆。

在这个例子中，`prints_country()`打印的是国家名称，一个`String`。我们想打印两次，但我们不能。

```rust
fn prints_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Kiribati");
    prints_country(country);
    prints_country(country); // ⚠️
}
```

但现在我们明白了这个信息。

```text
error[E0382]: use of moved value: `country`
 --> src\main.rs:4:20
  |
2 |     let country = String::from("Kiribati");
  |         ------- move occurs because `country` has type `std::string::String`, which does not implement the `Copy` trait
3 |     prints_country(country);
  |                    ------- value moved here
4 |     prints_country(country);
  |                    ^^^^^^^ value used here after move
```

重要的部分是`which does not implement the Copy trait`。但是在文档中我们看到String实现了`Clone`的特性。所以我们可以在代码中添加`.clone()`。这样就创建了一个克隆，然后我们将克隆发送到函数中。现在 `country` 还活着，所以我们可以使用它。

```rust
fn prints_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Kiribati");
    prints_country(country.clone()); // 做一个克隆交给函数。只有克隆进去，country 还活着
    prints_country(country);
}
```

当然，如果`String`非常大，`.clone()`就会占用很多内存。一个`String`可以是一整本书的长度，我们每次调用`.clone()`都会复制这本书。所以，如果可以的话，使用`&`来做引用是比较快的。例如，这段代码将`&str`推送到`String`上，然后每次在函数中使用时都会进行克隆。

```rust
fn get_length(input: String) { // 取得 String 的所有权
    println!("It's {} words long.", input.split_whitespace().count()); // 按空白拆分以统计单词数
}

fn main() {
    let mut my_string = String::new();
    for _ in 0..50 {
        my_string.push_str("Here are some more words "); // 追加这些词
        get_length(my_string.clone()); // 每次给它一个克隆
    }
}
```

它的打印。

```text
It's 5 words long.
It's 10 words long.
...
It's 250 words long.
```

这就是50个克隆。这里是用引用代替更好:

```rust
fn get_length(input: &String) {
    println!("It's {} words long.", input.split_whitespace().count());
}

fn main() {
    let mut my_string = String::new();
    for _ in 0..50 {
        my_string.push_str("Here are some more words ");
        get_length(&my_string);
    }
}
```

不是50个克隆，而是0个。



## 无值变量

一个没有值的变量叫做 "未初始化"变量。未初始化的意思是 "还没有开始"。它们很简单:只需写上`let`和变量名。

```rust
fn main() {
    let my_variable; // ⚠️
}
```

但是你还不能使用它，如果任何东西都没有被初始化，Rust就不会编译。

但有时它们会很有用。一个很好的例子是当:

- 你有一个代码块，而你的变量值就在里面，并且
- 变量需要活在代码块之外。

```rust
fn loop_then_return(mut counter: i32) -> i32 {
    loop {
        counter += 1;
        if counter % 50 == 0 {
            break;
        }
    }
    counter
}

fn main() {
    let my_number;

    {
        // 假装我们需要这个代码块
        let number = {
            // 假装这里有代码来生成一个数字
            // 很多代码，最后是：
            57
        };

        my_number = loop_then_return(number);
    }

    println!("{}", my_number);
}
```

这将打印出 `100`。

你可以看到 `my_number` 是在 `main()` 函数中声明的，所以它一直活到最后。但是它的值是在循环里面得到的。然而，这个值和`my_number`一样长，因为`my_number`有这个值。而如果你在块里面写了`let my_number = loop_then_return(number)`，它就会马上死掉。

如果你简化代码，对想象是有帮助的。`loop_then_return(number)`给出的结果是100，所以我们删除它，改写`100`。另外，现在我们不需要 `number`，所以我们也删除它。现在它看起来像这样:

```rust
fn main() {
    let my_number;
    {
        my_number = 100;
    }

    println!("{}", my_number);
}
```

所以说`let my_number = { 100 };`差不多。

另外注意，`my_number`不是`mut`。我们在给它50之前并没有给它一个值，所以它的值一直没有改变。最后，`my_number`的真正代码只是`let my_number = 100;`。
