+++
title = "47-多线程"
date = 2026-08-21T12:46:00+08:00
weight = 48
type = "docs"
description = "多线程 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_46.html](https://dhghomon.github.io/easy_rust/Chapter_46.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 多线程

如果你使用多个线程，你可以同时做很多事情。现代计算机有一个以上的核心，所以它们可以同时做多件事情，Rust让你使用它们。Rust使用的线程被称为 "OS线程"。OS线程意味着操作系统在不同的核上创建线程。(其他一些语言使用 "green threads"，功能较少)


你用`std::thread::spawn`创建线程，然后用一个闭包来告诉它该怎么做。线程很有趣，因为它们同时运行，你可以测试它，看看会发生什么。下面是一个简单的例子。

```rust
fn main() {
    std::thread::spawn(|| {
        println!("I am printing something");
    });
}
```

如果你运行这个，每次都会不一样。有时会打印，有时不会打印(这也取决于你的电脑速度)。这是因为有时`main()`在线程完成之前就完成了。而当`main()`完成后，程序就结束了。这在`for`循环中更容易看到。

```rust
fn main() {
    for _ in 0..10 { // 创建十个线程
        std::thread::spawn(|| {
            println!("I am printing something");
        });
    }   // 现在线程开始运行。
}       // main() 结束前能完成几个？
```

通常在`main`结束之前，大约会打印出四条线程，但总是不一样。如果你的电脑速度比较快，那么可能就不会打印了。另外，有时线程会崩溃。

```text
thread 'thread 'I am printing something
thread '<unnamed><unnamed>thread '' panicked at '<unnamed>I am printing something
' panicked at 'thread '<unnamed>cannot access stdout during shutdown' panicked at '<unnamed>thread 'cannot access stdout during
shutdown
```

这是在程序关闭时，线程试图做一些正确的事情时出现的错误。

你可以给电脑做一些事情，这样它就不会马上关闭了。

```rust
fn main() {
    for _ in 0..10 {
        std::thread::spawn(|| {
            println!("I am printing something");
        });
    }
    for _ in 0..1_000_000 { // 让程序声明一百万次 "let x = 9"
                            // 必须先做完这个才能退出 main
        let _x = 9;
    }
}
```

但这是一个让线程有时间完成的愚蠢方法。更好的方法是将线程绑定到一个变量上。如果你加上 `let`，你就能创建一个 `JoinHandle`。你可以在`spawn`的签名中看到这一点:

```text
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
where
    F: FnOnce() -> T,
    F: Send + 'static,
    T: Send + 'static,
```

(`f`是闭包--我们将在后面学习如何将闭包放入我们的函数中)

所以现在我们每次都有`JoinHandle`。

```rust
fn main() {
    for _ in 0..10 {
        let handle = std::thread::spawn(|| {
            println!("I am printing something");
        });

    }
}
```

`handle`现在是`JoinHandle`。我们怎么处理它呢？我们使用一个叫做 `.join()` 的方法。这个方法的意思是 "等待所有线程完成"(它等待线程加入它)。所以现在只要写`handle.join()`，它就会等待每个线程完成。

```rust
fn main() {
    for _ in 0..10 {
        let handle = std::thread::spawn(|| {
            println!("I am printing something");
        });

        handle.join(); // 等待线程完成
    }
}
```

现在我们就来了解一下三种类型的闭包。这三种类型是

- `FnOnce`: 取整个值
- `FnMut`: 取一个可变引用
- `Fn`: 取一个普通引用

如果可以的话，闭包会尽量使用`Fn`。但如果它需要改变值，它将使用 `FnMut`，而如果它需要取整个值，它将使用 `FnOnce`。`FnOnce`是个好名字，因为它解释了它的作用:它取一次值，然后就不能再取了。

下面是一个例子。

```rust
fn main() {
    let my_string = String::from("I will go into the closure");
    let my_closure = || println!("{}", my_string);
    my_closure();
    my_closure();
}
```

`String`没有实现`Copy`，所以`my_closure()`是`Fn`: 它拿到一个引用

如果我们改变`my_string`，它变成`FnMut`。

```rust
fn main() {
    let mut my_string = String::from("I will go into the closure");
    let mut my_closure = || {
        my_string.push_str(" now");
        println!("{}", my_string);
    };
    my_closure();
    my_closure();
}
```

这个打印:

```text
I will go into the closure now
I will go into the closure now now
```

而如果按值获取，则是`FnOnce`。

```rust
fn main() {
    let my_vec: Vec<i32> = vec![8, 9, 10];
    let my_closure = || {
        my_vec
            .into_iter() // into_iter 取得所有权
            .map(|x| x as u8) // 转成 u8
            .map(|x| x * 2) // 乘以 2
            .collect::<Vec<u8>>() // 收集成 Vec
    };
    let new_vec = my_closure();
    println!("{:?}", new_vec);
}
```

我们是按值取的，所以我们不能多跑`my_closure()`次。这就是名字的由来。

那么现在回到线程。让我们试着从外部引入一个值:

```rust
fn main() {
    let mut my_string = String::from("Can I go inside the thread?");

    let handle = std::thread::spawn(|| {
        println!("{}", my_string); // ⚠️
    });

    handle.join();
}
```

编译器说这个不行。

```text
error[E0373]: closure may outlive the current function, but it borrows `my_string`, which is owned by the current function
  --> src\main.rs:28:37
   |
28 |     let handle = std::thread::spawn(|| {
   |                                     ^^ may outlive borrowed value `my_string`
29 |         println!("{}", my_string);
   |                        --------- `my_string` is borrowed here
   |
note: function requires argument type to outlive `'static`
  --> src\main.rs:28:18
   |
28 |       let handle = std::thread::spawn(|| {
   |  __________________^
29 | |         println!("{}", my_string);
30 | |     });
   | |______^
help: to force the closure to take ownership of `my_string` (and any other referenced variables), use the `move` keyword
   |
28 |     let handle = std::thread::spawn(move || {
   |                                     ^^^^^^^
```

这条信息很长，但很有用:它说到``use the `move` keyword``。问题是我们可以在线程使用`my_string`时对它做任何事情，但线程并不拥有它。这将是不安全的。

让我们试试其他行不通的东西。

```rust
fn main() {
    let mut my_string = String::from("Can I go inside the thread?");

    let handle = std::thread::spawn(|| {
        println!("{}", my_string); // 现在 my_string 被当作引用使用
    });

    std::mem::drop(my_string);  // ⚠️ 我们试图在这里 drop。但线程还需要它。

    handle.join();
}
```

所以你要用`move`来取值，现在安全了:

```rust
fn main() {
    let mut my_string = String::from("Can I go inside the thread?");

    let handle = std::thread::spawn(move|| {
        println!("{}", my_string);
    });

    std::mem::drop(my_string);  // ⚠️ 不能 drop，因为 handle 持有它。所以这样不行

    handle.join();
}
```

所以我们把`std::mem::drop`删掉，现在就可以了。`handle`取`my_string`，我们的代码就安全了。

```rust
fn main() {
    let mut my_string = String::from("Can I go inside the thread?");

    let handle = std::thread::spawn(move|| {
        println!("{}", my_string);
    });

    handle.join();
}
```

所以只要记住:如果你在线程中需要一个来自线程外的值，你需要使用`move`。
