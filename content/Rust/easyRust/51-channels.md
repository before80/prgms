+++
title = "51-Channels（通道）"
date = 2026-08-21T12:46:00+08:00
weight = 52
type = "docs"
description = "Channels（通道） — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_50.html](https://dhghomon.github.io/easy_rust/Chapter_50.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Channels（通道）

A channel is an easy way to use many threads that send to one place.它们相当流行，因为它们很容易组合在一起。你可以在Rust中用`std::sync::mpsc`创建一个channel。`mpsc`的意思是 "多个生产者，单个消费者"，所以 "many threads sending to one place"。要启动一个通道，你可以使用 `channel()`。这将创建一个 `Sender` 和一个 `Receiver`，它们被绑在一起。你可以在函数签名中看到这一点。

```rust
// 🚧
pub fn channel<T>() -> (Sender<T>, Receiver<T>)
```

所以你要选择一个发送者的名字和一个接收者的名字。通常你会看到像`let (sender, receiver) = channel();`这样的开头。因为它是泛型函数，如果你只写这个，Rust不会知道类型。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel(); // ⚠️
}
```

编译器说:

```text
error[E0282]: type annotations needed for `(std::sync::mpsc::Sender<T>, std::sync::mpsc::Receiver<T>)`
  --> src\main.rs:30:30
   |
30 |     let (sender, receiver) = channel();
   |         ------------------   ^^^^^^^ cannot infer type for type parameter `T` declared on the function `channel`
   |         |
   |         consider giving this pattern the explicit type `(std::sync::mpsc::Sender<T>, std::sync::mpsc::Receiver<T>)`, where
the type parameter `T` is specified
```

它建议为`Sender`和`Receiver`添加一个类型。如果你愿意的话，可以这样做:

```rust
use std::sync::mpsc::{channel, Sender, Receiver}; // 这里加上了 Sender 和 Receiver

fn main() {
    let (sender, receiver): (Sender<i32>, Receiver<i32>) = channel();
}
```

但你不必这样做: 一旦你开始使用`Sender`和`Receiver`，Rust就能猜到类型。

所以我们来看一下最简单的使用通道的方法。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel();

    sender.send(5);
    receiver.recv(); // recv = receive（接收），不是 "rec v"
}
```

现在编译器知道类型了。`sender`是`Result<(), SendError<i32>>`，`receiver`是`Result<i32, RecvError>`。所以你可以用`.unwrap()`来看看发送是否有效，或者使用更好的错误处理。我们加上`.unwrap()`，也加上`println!`，看看得到什么。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel();

    sender.send(5).unwrap();
    println!("{}", receiver.recv().unwrap());
}
```

这样就可以打印出`5`。

`channel`就像`Arc`一样，因为你可以克隆它，并将克隆的内容发送到其他线程中。让我们创建两个线程，并将值发送到`receiver`。这段代码可以工作，但它并不完全是我们想要的。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel();
    let sender_clone = sender.clone();

    std::thread::spawn(move|| { // 把 sender 移进去
        sender.send("Send a &str this time").unwrap();
    });

    std::thread::spawn(move|| { // 把 sender_clone 移进去
        sender_clone.send("And here is another &str").unwrap();
    });

    println!("{}", receiver.recv().unwrap());
}
```

两个线程开始发送，然后我们`println!`。它可能会打印 `Send a &str this time` 或 `And here is another &str`，这取决于哪个线程先完成。让我们创建一个join句柄来等待它们完成。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel();
    let sender_clone = sender.clone();
    let mut handle_vec = vec![]; // 把 handle 放进这里

    handle_vec.push(std::thread::spawn(move|| {  // 把这个推进 vec
        sender.send("Send a &str this time").unwrap();
    }));

    handle_vec.push(std::thread::spawn(move|| {  // 再把这个推进 vec
        sender_clone.send("And here is another &str").unwrap();
    }));

    for _ in handle_vec { // 现在 handle_vec 有 2 项。打印它们
        println!("{:?}", receiver.recv().unwrap());
    }
}
```

这个将打印:

```text
"Send a &str this time"
"And here is another &str"
```

现在我们不打印，我们创建一个`results_vec`。

```rust
use std::sync::mpsc::channel;

fn main() {
    let (sender, receiver) = channel();
    let sender_clone = sender.clone();
    let mut handle_vec = vec![];
    let mut results_vec = vec![];

    handle_vec.push(std::thread::spawn(move|| {
        sender.send("Send a &str this time").unwrap();
    }));

    handle_vec.push(std::thread::spawn(move|| {
        sender_clone.send("And here is another &str").unwrap();
    }));

    for _ in handle_vec {
        results_vec.push(receiver.recv().unwrap());
    }

    println!("{:?}", results_vec);
}
```

现在结果在我们的vec中:`["Send a &str this time", "And here is another &str"]`。

现在让我们假设我们有很多工作要做，并且想要使用线程。我们有一个大的VEC，里面有1百万个元素，都是0，我们想把每个0都变成1，我们将使用10个线程，每个线程将做十分之一的工作。我们将创建一个新的VEC，并使用`.extend()`来收集结果。

```rust
use std::sync::mpsc::channel;
use std::thread::spawn;

fn main() {
    let (sender, receiver) = channel();
    let hugevec = vec![0; 1_000_000];
    let mut newvec = vec![];
    let mut handle_vec = vec![];

    for i in 0..10 {
        let sender_clone = sender.clone();
        let mut work: Vec<u8> = Vec::with_capacity(hugevec.len() / 10); // 新的 vec 用来装工作数据，大小是原来的 1/10
        work.extend(&hugevec[i*100_000..(i+1)*100_000]); // 第一段是 0..100_000，下一段是 100_000..200_000，以此类推
        let handle =spawn(move || { // 创建一个 handle

            for number in work.iter_mut() { // 做实际工作
                *number += 1;
            };
            sender_clone.send(work).unwrap(); // 用 sender_clone 把结果发给 receiver
        });
        handle_vec.push(handle);
    }

    for handle in handle_vec { // 等到这些线程都结束
        handle.join().unwrap();
    }

    while let Ok(results) = receiver.try_recv() {
        newvec.push(results); // 把 receiver.recv() 的结果推进 vec
    }

    // 现在是 Vec<Vec<u8>>。拼成一个可以用 .flatten()
    let newvec = newvec.into_iter().flatten().collect::<Vec<u8>>(); // 现在是一个有 1_000_000 个 u8 的 vec

    println!("{:?}, {:?}, total length: {}", // 打印一些数字，确认都是 1
        &newvec[0..10], &newvec[newvec.len()-10..newvec.len()], newvec.len() // 并确认长度是 1_000_000
    );

    for number in newvec { // 如果有任何一个数不是 1，就让它 panic
        if number != 1 {
            panic!();
        }
    }
}
```
