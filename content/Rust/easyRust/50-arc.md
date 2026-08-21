+++
title = "50-Arc"
date = 2026-08-21T12:46:00+08:00
weight = 51
type = "docs"
description = "Arc — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_49.html](https://dhghomon.github.io/easy_rust/Chapter_49.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# Arc

你还记得我们用`Rc`来给一个变量一个以上的所有者。如果我们在线程中做同样的事情，我们需要一个 `Arc`。`Arc`的意思是 "atomic reference counter"(原子引用计数器)。原子的意思是它使用计算机的处理器，所以每次只写一次数据。这一点很重要，因为如果两个线程同时写入数据，你会得到错误的结果。例如，想象一下，如果你能在Rust中做到这一点。

```rust
// 🚧
let mut x = 10;

for i in 0..10 { // 线程 1
    x += 1
}
for i in 0..10 { // 线程 2
    x += 1
}
```


如果线程1和线程2一起启动，也许就会出现这种情况。

- 线程1看到10，写下11，然后线程2看到11，写下12 然后线程2看到11，写入12。到目前为止没有问题。
- 线程1看到12。同时，线程2看到12。线程一看到13，写下13 线程2也写了13 现在我们有13个，但应该是14个 Now we have 13, but it should be 14. 这是个大问题。

`Arc`使用处理器来确保这种情况不会发生，所以当你有线程时必须使用这种方法。不过不建议单线程上用`Arc`，因为`Rc`更快一些。

不过你不能只用一个`Arc`来改变数据。所以你用一个`Mutex`把数据包起来，然后用一个`Arc`把`Mutex`包起来。

所以我们用一个`Mutex`在一个`Arc`里面来改变一个数字的值。首先我们设置一个线程。

```rust
fn main() {

    let handle = std::thread::spawn(|| {
        println!("The thread is working!") // 只是测试一下线程
    });

    handle.join().unwrap(); // 让主线程在此等待，直到子线程结束
    println!("Exiting the program");
}
```

到目前为止，这个只打印:

```text
The thread is working!
Exiting the program
```

很好，现在让我们把它放在`for`的循环中，进行`0..5`。

```rust
fn main() {

    let handle = std::thread::spawn(|| {
        for _ in 0..5 {
            println!("The thread is working!")
        }
    });

    handle.join().unwrap();
    println!("Exiting the program");
}
```

这也是可行的。我们得到以下结果:

```text
The thread is working!
The thread is working!
The thread is working!
The thread is working!
The thread is working!
Exiting the program
```

现在我们再加一个线程。每个线程都会做同样的事情。你可以看到，这些线程是在同一时间工作的。有时会先打印`Thread 1 is working!`，但其他时候`Thread 2 is working!`先打印。这就是所谓的**并发**，也就是 "一起运行"的意思。

```rust
fn main() {

    let thread1 = std::thread::spawn(|| {
        for _ in 0..5 {
            println!("Thread 1 is working!")
        }
    });

    let thread2 = std::thread::spawn(|| {
        for _ in 0..5 {
            println!("Thread 2 is working!")
        }
    });

    thread1.join().unwrap();
    thread2.join().unwrap();
    println!("Exiting the program");
}
```

这将打印:

```text
Thread 1 is working!
Thread 1 is working!
Thread 1 is working!
Thread 1 is working!
Thread 1 is working!
Thread 2 is working!
Thread 2 is working!
Thread 2 is working!
Thread 2 is working!
Thread 2 is working!
Exiting the program
```

现在我们要改变`my_number`的数值。现在它是一个`i32`。我们将把它改为 `Arc<Mutex<i32>>`:一个可以改变的 `i32`，由 `Arc` 保护。

```rust
// 🚧
let my_number = Arc::new(Mutex::new(0));
```

现在我们有了这个，我们可以克隆它。每个克隆可以进入不同的线程。我们有两个线程，所以我们将做两个克隆。

```rust
// 🚧
let my_number = Arc::new(Mutex::new(0));

let my_number1 = Arc::clone(&my_number); // 这个克隆会进入线程 1
let my_number2 = Arc::clone(&my_number); // 这个克隆会进入线程 2
```

现在，我们已经将安全克隆连接到`my_number`，我们可以将它们`move`到其他线程中，没有问题。

```rust
use std::sync::{Arc, Mutex};

fn main() {
    let my_number = Arc::new(Mutex::new(0));

    let my_number1 = Arc::clone(&my_number);
    let my_number2 = Arc::clone(&my_number);

    let thread1 = std::thread::spawn(move || { // 只有克隆进入线程 1
        for _ in 0..10 {
            *my_number1.lock().unwrap() +=1; // 锁定 Mutex，再改值
        }
    });

    let thread2 = std::thread::spawn(move || { // 只有克隆进入线程 2
        for _ in 0..10 {
            *my_number2.lock().unwrap() += 1;
        }
    });

    thread1.join().unwrap();
    thread2.join().unwrap();
    println!("Value is: {:?}", my_number);
    println!("Exiting the program");
}
```

程序打印:

```text
Value is: Mutex { data: 20 }
Exiting the program
```

所以这是一个成功的案例。

然后我们可以将两个线程连接在一起，形成一个`for`循环，并使代码更短。

我们需要保存句柄，这样我们就可以在循环外对每个线程调用`.join()`。如果我们在循环内这样做，它将等待第一个线程完成后再启动新的线程。

```rust
use std::sync::{Arc, Mutex};

fn main() {
    let my_number = Arc::new(Mutex::new(0));
    let mut handle_vec = vec![]; // JoinHandle 会放进这里

    for _ in 0..2 { // 做两次
        let my_number_clone = Arc::clone(&my_number); // 启动线程前先做好克隆
        let handle = std::thread::spawn(move || { // 把克隆放进去
            for _ in 0..10 {
                *my_number_clone.lock().unwrap() += 1;
            }
        });
        handle_vec.push(handle); // 保存 handle，以便在循环外调用 join
                                 // 如果不推进 vec，它会在这里直接被丢弃
    }

    handle_vec.into_iter().for_each(|handle| handle.join().unwrap()); // 对所有 handle 调用 join
    println!("{:?}", my_number);
}
```

最后这个打印`Mutex { data: 20 }`。

这看起来很复杂，但`Arc<Mutex<SomeType>>>`在Rust中使用的频率很高，所以它变得很自然。另外，你也可以随时写你的代码，让它更干净。这里是同样的代码，多了一条`use`语句和两个函数。这些函数并没有做任何新的事情，但是它们把一些代码从`main()`中移出。如果你很难读懂的话，可以尝试重写这样的代码。

```rust
use std::sync::{Arc, Mutex};
use std::thread::spawn; // 现在可以直接写 spawn

fn make_arc(number: i32) -> Arc<Mutex<i32>> { // 只是用来在 Arc 里包一个 Mutex 的函数
    Arc::new(Mutex::new(number))
}

fn new_clone(input: &Arc<Mutex<i32>>) -> Arc<Mutex<i32>> { // 只是方便写成 new_clone 的函数
    Arc::clone(&input)
}

// 现在 main() 更好读了
fn main() {
    let mut handle_vec = vec![]; // 每个 handle 会放进这里
    let my_number = make_arc(0);

    for _ in 0..2 {
        let my_number_clone = new_clone(&my_number);
        let handle = spawn(move || {
            for _ in 0..10 {
                let mut value_inside = my_number_clone.lock().unwrap();
                *value_inside += 1;
            }
        });
        handle_vec.push(handle);    // handle 建好了，放进向量
    }

    handle_vec.into_iter().for_each(|handle| handle.join().unwrap()); // 让每个线程都等待结束

    println!("{:?}", my_number);
}
```
