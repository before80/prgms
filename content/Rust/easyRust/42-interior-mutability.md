+++
title = "42-内部可变性"
date = 2026-08-21T12:46:00+08:00
weight = 43
type = "docs"
description = "内部可变性 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_41.html](https://dhghomon.github.io/easy_rust/Chapter_41.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 内部可变性

## Cell

**内部可变性**的意思是在内部有一点可变性。还记得在Rust中，你需要用`mut`来改变一个变量吗？也有一些方法可以不用`mut`这个词来改变它们。这是因为Rust有一些方法可以让你安全地在一个不可变的结构里面改变值。每一种方法都遵循一些规则，确保改变值仍然是安全的。

首先，让我们看一个简单的例子，我们会想要这样做:想象一下，一个叫`PhoneModel`的结构体有很多字段:

```rust
struct PhoneModel {
    company_name: String,
    model_name: String,
    screen_size: f32,
    memory: usize,
    date_issued: u32,
    on_sale: bool,
}

fn main() {
    let super_phone_3000 = PhoneModel {
        company_name: "YY Electronics".to_string(),
        model_name: "Super Phone 3000".to_string(),
        screen_size: 7.5,
        memory: 4_000_000,
        date_issued: 2020,
        on_sale: true,
    };

}
```

`PhoneModel`中的字段最好是不可变的，因为我们不希望数据改变。比如说`date_issued`和`screen_size`永远不会变。

但是里面有一个字段叫`on_sale`。一个手机型号先是会有销售(`true`)，但是后来公司会停止销售。我们能不能只让这一个字段可变？因为我们不想写`let mut super_phone_3000`。如果我们这样做，那么每个字段都会变得可变。

Rust有很多方法可以让一些不可变的东西里面有一些安全的可变性，最简单的方法叫做`Cell`。首先我们使用`use std::cell::Cell`，这样我们就可以每次只写`Cell`而不是`std::cell::Cell`。

然后我们把`on_sale: bool`改成`on_sale: Cell<bool>`。现在它不是一个bool:它是一个`Cell`，容纳了一个`bool`。

`Cell`有一个叫做`.set()`的方法，在这里你可以改变值。我们用`.set()`把`on_sale: true`改为`on_sale: Cell::new(true)`。

```rust
use std::cell::Cell;

struct PhoneModel {
    company_name: String,
    model_name: String,
    screen_size: f32,
    memory: usize,
    date_issued: u32,
    on_sale: Cell<bool>,
}

fn main() {
    let super_phone_3000 = PhoneModel {
        company_name: "YY Electronics".to_string(),
        model_name: "Super Phone 3000".to_string(),
        screen_size: 7.5,
        memory: 4_000_000,
        date_issued: 2020,
        on_sale: Cell::new(true),
    };

    // 十年后，super_phone_3000 不再在售
    super_phone_3000.on_sale.set(false);
}
```

`Cell` 适用于所有类型，但对简单的 Copy 类型效果最好，因为它给出的是值，而不是引用。`Cell`有一个叫做`get()`的方法，它只对Copy类型有效。

另一个可以使用的类型是 `RefCell`。

## RefCell

`RefCell`是另一种无需声明`mut`而改变值的方法。它的意思是 "引用单元格"，就像 `Cell`，但使用引用而不是副本。

我们将创建一个 `User` 结构。到目前为止，你可以看到它与 `Cell` 类似。

```rust
use std::cell::RefCell;

#[derive(Debug)]
struct User {
    id: u32,
    year_registered: u32,
    username: String,
    active: RefCell<bool>,
    // 还有很多其他字段
}

fn main() {
    let user_1 = User {
        id: 1,
        year_registered: 2020,
        username: "User 1".to_string(),
        active: RefCell::new(true),
    };

    println!("{:?}", user_1.active);
}
```

这样就可以打印出`RefCell { value: true }`。

`RefCell`的方法有很多。其中两种是`.borrow()`和`.borrow_mut()`。使用这些方法，你可以做与`&`和`&mut`相同的事情。规则都是一样的:

- 多个不可变借用可以
- 一个可变的借用可以
- 但可变和不可变借用在一起是不行的

所以改变`RefCell`中的值是非常容易的。

```rust
// 🚧
user_1.active.replace(false);
println!("{:?}", user_1.active);
```

而且还有很多其他的方法，比如`replace_with`使用的是闭包。

```rust
// 🚧
let date = 2020;

user_1
    .active
    .replace_with(|_| if date < 2000 { true } else { false });
println!("{:?}", user_1.active);
```


但是你要小心使用`RefCell`，因为它是在运行时而不是编译时检查借用。运行时是指程序实际运行的时候(编译后)。所以这将会被编译，即使它是错误的。

```rust
use std::cell::RefCell;

#[derive(Debug)]
struct User {
    id: u32,
    year_registered: u32,
    username: String,
    active: RefCell<bool>,
    // 还有很多其他字段
}

fn main() {
    let user_1 = User {
        id: 1,
        year_registered: 2020,
        username: "User 1".to_string(),
        active: RefCell::new(true),
    };

    let borrow_one = user_1.active.borrow_mut(); // 第一次可变借用——没问题
    let borrow_two = user_1.active.borrow_mut(); // 第二次可变借用——不行
}
```

但如果你运行它，它就会立即崩溃。

```text
thread 'main' panicked at 'already borrowed: BorrowMutError', C:\Users\mithr\.rustup\toolchains\stable-x86_64-pc-windows-msvc\lib/rustlib/src/rust\src\libcore\cell.rs:877:9
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
error: process didn't exit successfully: `target\debug\rust_book.exe` (exit code: 101)
```

`already borrowed: BorrowMutError`是重要的部分。所以当你使用`RefCell`时，好编译**并**运行检查。

## Mutex

`Mutex`是另一种改变数值的方法，不需要声明`mut`。Mutex的意思是`mutual exclusion`，也就是 "一次只能改一个"。这就是为什么`Mutex`是安全的，因为它每次只让一个进程改变它。为了做到这一点，它使用了`.lock()`。`Lock`就像从里面锁上一扇门。你进入一个房间，锁上门，现在你可以在房间里面改变东西。别人不能进来阻止你，因为你把门锁上了。

`Mutex`通过例子更容易理解:

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5); // 新建 Mutex<i32>。不必写 mut
    let mut mutex_changer = my_mutex.lock().unwrap(); // mutex_changer 是 MutexGuard
                                                     // 必须是 mut，因为我们要改它
                                                     // 现在它可以访问 Mutex 了
                                                     // 打印 my_mutex 看看：

    println!("{:?}", my_mutex); // 这会打印 "Mutex { data: <locked> }"
                                // 所以现在不能再用 my_mutex 访问数据，
                                // 只能用 mutex_changer

    println!("{:?}", mutex_changer); // 打印 5。我们把它改成 6。

    *mutex_changer = 6; // mutex_changer 是 MutexGuard<i32>，用 * 改里面的 i32

    println!("{:?}", mutex_changer); // 现在显示 6
}
```

但是`mutex_changer`做完后还是有锁。我们该如何阻止它呢？`Mutex`在`MutexGuard`超出范围时就会被解锁。"超出范围"表示该代码块已经完成。比如说:

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);
    {
        let mut mutex_changer = my_mutex.lock().unwrap();
        *mutex_changer = 6;
    } // mutex_changer 离开作用域——它没了。锁也解开了

    println!("{:?}", my_mutex); // 现在显示：Mutex { data: 6 }
}
```

如果你不想使用不同的`{}`代码块，你可以使用`std::mem::drop(mutex_changer)`。`std::mem::drop`的意思是 "让这个超出范围"。

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);
    let mut mutex_changer = my_mutex.lock().unwrap();
    *mutex_changer = 6;
    std::mem::drop(mutex_changer); // drop mutex_changer——它现在没了
                                   // my_mutex 也解锁了

    println!("{:?}", my_mutex); // 现在显示：Mutex { data: 6 }
}
```

你必须小心使用 `Mutex`，因为如果另一个变量试图 `lock`它，它会等待。

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);
    let mut mutex_changer = my_mutex.lock().unwrap(); // mutex_changer 持有锁
    let mut other_mutex_changer = my_mutex.lock().unwrap(); // other_mutex_changer 也想要锁
                                                            // 程序在等待
                                                            // 还在等
                                                            // 而且会永远等下去。

    println!("This will never print...");
}
```

还有一种方法是`try_lock()`。然后它会试一次，如果没能锁上就会放弃。`try_lock().unwrap()`就不要做了，因为如果不成功它就会崩溃。`if let`或`match`比较好。

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);
    let mut mutex_changer = my_mutex.lock().unwrap();
    let mut other_mutex_changer = my_mutex.try_lock(); // 尝试获取锁

    if let Ok(value) = other_mutex_changer {
        println!("The MutexGuard has: {}", value)
    } else {
        println!("Didn't get the lock")
    }
}
```

另外，你不需要创建一个变量来改变`Mutex`。你可以直接这样做:

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);

    *my_mutex.lock().unwrap() = 6;

    println!("{:?}", my_mutex);
}
```

`*my_mutex.lock().unwrap() = 6;`的意思是 "解锁my_mutex并使其成为6"。没有任何变量来保存它，所以你不需要调用 `std::mem::drop`。如果你愿意，你可以做100次--这并不重要。

```rust
use std::sync::Mutex;

fn main() {
    let my_mutex = Mutex::new(5);

    for _ in 0..100 {
        *my_mutex.lock().unwrap() += 1; // 加锁解锁 100 次
    }

    println!("{:?}", my_mutex);
}
```

## RwLock

`RwLock`的意思是 "读写锁"。它像`Mutex`，但也像`RefCell`。你用`.write().unwrap()`代替`.lock().unwrap()`来改变它。但你也可以用`.read().unwrap()`来获得读权限。它和`RefCell`一样，遵循这些规则:

- 很多`.read()`变量可以
- 一个`.write()`变量可以
- 但多个`.write()`或`.read()`与`.write()`一起是不行的

如果在无法访问的情况下尝试`.write()`，程序将永远运行。

```rust
use std::sync::RwLock;

fn main() {
    let my_rwlock = RwLock::new(5);

    let read1 = my_rwlock.read().unwrap(); // 一次 .read() 没问题
    let read2 = my_rwlock.read().unwrap(); // 两次 .read() 也没问题

    println!("{:?}, {:?}", read1, read2);

    let write1 = my_rwlock.write().unwrap(); // 糟糕，现在程序会永远等下去
}
```

所以我们用`std::mem::drop`，就像用`Mutex`一样。

```rust
use std::sync::RwLock;
use std::mem::drop; // 我们会多次使用 drop()

fn main() {
    let my_rwlock = RwLock::new(5);

    let read1 = my_rwlock.read().unwrap();
    let read2 = my_rwlock.read().unwrap();

    println!("{:?}, {:?}", read1, read2);

    drop(read1);
    drop(read2); // 两个都 drop 了，现在可以用 .write()

    let mut write1 = my_rwlock.write().unwrap();
    *write1 = 6;
    drop(write1);
    println!("{:?}", my_rwlock);
}
```

而且你也可以使用`try_read()`和`try_write()`。

```rust
use std::sync::RwLock;

fn main() {
    let my_rwlock = RwLock::new(5);

    let read1 = my_rwlock.read().unwrap();
    let read2 = my_rwlock.read().unwrap();

    if let Ok(mut number) = my_rwlock.try_write() {
        *number += 10;
        println!("Now the number is {}", number);
    } else {
        println!("Couldn't get write access, sorry!")
    };
}
```
