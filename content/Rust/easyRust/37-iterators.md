+++
title = "37-迭代器"
date = 2026-08-21T12:46:00+08:00
weight = 38
type = "docs"
description = "迭代器 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_36.html](https://dhghomon.github.io/easy_rust/Chapter_36.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 迭代器

迭代器是一个构造，它可以给你集合中的元素，一次一个。实际上，我们已经使用了很多迭代器:`for`循环给你一个迭代器。当你想在其他时候使用迭代器时，你必须选择什么样的迭代器:

- `.iter()` 引用的迭代器
- `.iter_mut()` 可变引用的迭代器
- `.into_iter()` 值的迭代器(不是引用)

`for`循环其实只是一个拥有值的迭代器。这就是为什么可以让它变得可变，然后你可以在使用的时候改变值。

我们可以这样使用迭代器。

```rust
fn main() {
    let vector1 = vec![1, 2, 3]; // 我们会对这个用 .iter() 和 .into_iter()
    let vector1_a = vector1.iter().map(|x| x + 1).collect::<Vec<i32>>();
    let vector1_b = vector1.into_iter().map(|x| x * 10).collect::<Vec<i32>>();

    let mut vector2 = vec![10, 20, 30]; // 我们会对这个用 .iter_mut()
    vector2.iter_mut().for_each(|x| *x +=100);

    println!("{:?}", vector1_a);
    println!("{:?}", vector2);
    println!("{:?}", vector1_b);
}
```

这个将打印:

```text
[2, 3, 4]
[110, 120, 130]
[10, 20, 30]
```

前两个我们用了一个叫`.map()`的方法。这个方法可以让你对每一个元素做一些事情，然后把它传递下去。最后我们用的是一个叫`.for_each()`的方法。这个方法只是让你对每一个元素做一些事情。`.iter_mut()`加上`for_each()`基本上就是一个`for`的循环。在每一个方法里面，我们可以给每一个元素起一个名字(我们刚才叫它 `x`)，然后用它来改变它。这些被称为闭包，我们将在下一节学习它们。

让我们再来看看它们，一次一个。

首先我们用`.iter()`对`vector1`进行引用。我们给每个元素都加了1，并使其成为一个新的Vec。`vector1`还活着，因为我们只用了引用:我们没有按值取。现在我们有 `vector1`，还有一个新的 Vec 叫 `vector1_a`。因为`.map()`只是传递了它，所以我们需要使用`.collect()`把它变成一个`Vec`。

然后我们用`into_iter`从`vector1`中按值得到一个迭代器。这样就破坏了`vector1`，因为这就是`into_iter()`的作用。所以我们做了`vector1_b`之后，就不能再使用`vector1`了。

最后我们在`vector2`上使用`.iter_mut()`。它是可变的，所以我们不需要使用`.collect()`来创建一个新的Vec。相反，我们用可变引用改变同一Vec中的值。所以`vector2`仍然存在。因为我们不需要一个新的Vec，我们使用`for_each`:它就像一个`for`循环。


## 迭代器如何工作

迭代器的工作原理是使用一个叫做 `.next()` 的方法，它给出一个 `Option`。当你使用迭代器时，Rust会一遍又一遍地调用`next()`。如果得到 `Some`，它就会继续前进。如果得到 `None`，它就停止。

你还记得 `assert_eq!` 宏吗？在文档中，你经常看到它。这里它展示了迭代器的工作原理。

```rust
fn main() {
    let my_vec = vec!['a', 'b', '거', '柳']; // 只是普通的 Vec

    let mut my_vec_iter = my_vec.iter(); // 现在是 Iterator 类型，但还没调用

    assert_eq!(my_vec_iter.next(), Some(&'a'));  // 用 .next() 取第一项
    assert_eq!(my_vec_iter.next(), Some(&'b'));  // 再取下一项
    assert_eq!(my_vec_iter.next(), Some(&'거')); // 再来一次
    assert_eq!(my_vec_iter.next(), Some(&'柳')); // 再来一次
    assert_eq!(my_vec_iter.next(), None);        // 没有了：只剩 None
    assert_eq!(my_vec_iter.next(), None);        // 还可以继续调用 .next()，但永远是 None
}
```

为自己的struct或enum实现`Iterator`并不难。首先我们创建一个书库，想一想。

```rust
#[derive(Debug)] // 想用 {:?} 打印
struct Library {
    library_type: LibraryType, // 这是我们的枚举
    books: Vec<String>, // 书单
}

#[derive(Debug)]
enum LibraryType { // 图书馆可以是城市或乡村图书馆
    City,
    Country,
}

impl Library {
    fn add_book(&mut self, book: &str) { // 用 add_book 添加新书
        self.books.push(book.to_string()); // 接受 &str，转成 String，再加入 Vec
    }

    fn new() -> Self { // 创建一个新 Library
        Self {
            library_type: LibraryType::City, // 多数在城市，所以选 City
                                             // 大多数时候
            books: Vec::new(),
        }
    }
}

fn main() {
    let mut my_library = Library::new(); // 新建一个图书馆
    my_library.add_book("The Doom of the Darksword"); // 加几本书
    my_library.add_book("Demian - die Geschichte einer Jugend");
    my_library.add_book("구운몽");
    my_library.add_book("吾輩は猫である");

    println!("{:?}", my_library.books); // 可以打印书单
}
```

这很好用。现在我们想为库实现`Iterator`，这样我们就可以在`for`循环中使用它。现在如果我们尝试 `for` 循环，它就无法工作。

```rust
for item in my_library {
    println!("{}", item); // ⚠️
}
```

它说:

```text
error[E0277]: `Library` is not an iterator
  --> src\main.rs:47:16
   |
47 |    for item in my_library {
   |                ^^^^^^^^^^ `Library` is not an iterator
   |
   = help: the trait `std::iter::Iterator` is not implemented for `Library`
   = note: required by `std::iter::IntoIterator::into_iter`
```

但是我们可以用`impl Iterator for Library`把库做成迭代器。`Iterator`trait的信息在标准库中。[https://doc.rust-lang.org/std/iter/trait.Iterator.html](https://doc.rust-lang.org/std/iter/trait.Iterator.html)

在页面的左上方写着:`Associated Types: Item`和`Required Methods: next`。"关联类型"的意思是 "一起使用的类型"。我们的关联类型将是`String`，因为我们希望迭代器给我们提供String。

在页面中，它有一个看起来像这样的例子。

```rust
// 在 Some 与 None 之间交替的迭代器
struct Alternate {
    state: i32,
}

impl Iterator for Alternate {
    type Item = i32;

    fn next(&mut self) -> Option<i32> {
        let val = self.state;
        self.state = self.state + 1;

        // 偶数则 Some(i32)，否则 None
        if val % 2 == 0 {
            Some(val)
        } else {
            None
        }
    }
}

fn main() {}
```

你可以看到`impl Iterator for Alternate`下面写着`type Item = i32`。这就是关联类型。我们的迭代器将针对我们的书籍列表，这是一个`Vec<String>`。当我们调用next的时候。
 它将给我们一个`String`。所以我们就写`type Item = String;`。这就是关联项。

为了实现 `Iterator`，你需要写 `fn next()` 函数。这是你决定迭代器应该做什么的地方。对于我们的 `Library`，我们首先希望它给我们最后一本书。所以我们将`match`与`.pop()`一起，如果是`Some`的话，就把最后一项去掉。我们还想为每个元素打印 "is found!"。现在它看起来像这样:

```rust
#[derive(Debug, Clone)]
struct Library {
    library_type: LibraryType,
    books: Vec<String>,
}

#[derive(Debug, Clone)]
enum LibraryType {
    City,
    Country,
}

impl Library {
    fn add_book(&mut self, book: &str) {
        self.books.push(book.to_string());
    }

    fn new() -> Self {
        Self {
            library_type: LibraryType::City,
            // 大多数时候
            books: Vec::new(),
        }
    }
}

impl Iterator for Library {
    type Item = String;

    fn next(&mut self) -> Option<String> {
        match self.books.pop() {
            Some(book) => Some(book + " is found!"), // Rust 允许 String + &str
            None => None,
        }
    }
}

fn main() {
    let mut my_library = Library::new();
    my_library.add_book("The Doom of the Darksword");
    my_library.add_book("Demian - die Geschichte einer Jugend");
    my_library.add_book("구운몽");
    my_library.add_book("吾輩は猫である");

    for item in my_library.clone() { // 现在可以用 for 循环了。给它一个 clone，这样 Library 不会被销毁
        println!("{}", item);
    }
}
```

这个打印:

```text
吾輩は猫である is found!
구운몽 is found!
Demian - die Geschichte einer Jugend is found!
The Doom of the Darksword is found!
```
