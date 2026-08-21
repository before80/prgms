+++
title = "01-动态字符串 String"
date = 2026-08-12T20:00:00+08:00
weight = 32
type = "docs"
description = "动态字符串 String — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/collections/string.html](https://practice-rust-zh.beatai.org/collections/string.html)

# 动态字符串 String
`std::string::String` 是 UTF-8 编码、可增长的动态字符串. 它也是我们日常开发中最常用的字符串类型，同时对于它所拥有的内容拥有所有权。

### 基本操作
1. 🌟🌟
```rust

// 填空并修复错误
// 1. 不要使用 `to_string()`
// 2. 不要添加/删除任何代码行
fn main() {
    let mut s: String = "hello, ";
    s.push_str("world".to_string());
    s.push(__);

    move_ownership(s);

    assert_eq!(s, "hello, world!");

    println!("Success!")
}

fn move_ownership(s: String) {
    println!("ownership of \"{}\" is moved here!", s)
}
```

### String and &str
虽然 `String` 的底层是 `Vec<u8>` 也就是字节数组的形式存储的，但是它是基于 UTF-8 编码的字符序列。`String` 分配在堆上、可增长且不是以 `null` 结尾。

而 `&str` 是[切片引用](https://course.rs/confonding/slice.html)类型( `&[u8]` )，指向一个合法的 UTF-8 字符序列，总之，`&str` 和 `String` 的关系类似于 `&[T]` 和 `Vec<T>` 。

如果大家想了解更多，可以看看[易混淆概念解析 - &str 和 String](https://course.rs/difficulties/string.html)。


2. 🌟🌟
```rust
// 填空
fn main() {  
   let mut s = String::from("hello, world");

   let slice1: &str = __; // 使用两种方法
   assert_eq!(slice1, "hello, world");

   let slice2 = __;
   assert_eq!(slice2, "hello");

   let slice3: __ = __; 
   slice3.push('!');
   assert_eq!(slice3, "hello, world!");

   println!("Success!")
}
```

3. 🌟🌟
```rust

// 问题:  我们的代码中发生了多少次堆内存分配？
// 你的回答: 
fn main() {  
    // 基于 `&str` 类型创建一个 String,
    // 字符串字面量的类型是 `&str`
   let s: String = String::from("hello, world!");

   // 创建一个切片引用指向 String `s`
   let slice: &str = &s;

   // 基于刚创建的切片来创建一个 String
   let s: String = slice.to_string();

   assert_eq!(s, "hello, world!");

   println!("Success!")
}
```

### UTF-8 & 索引
由于 String 都是 UTF-8 编码的，这会带来几个影响:

- 如果你需要的是非 UTF-8 字符串，可以考虑 [OsString](https://doc.rust-lang.org/stable/std/ffi/struct.OsString.html) 
- 无法通过索引的方式访问一个 String

具体请看[字符串索引](https://course.rs/basic/compound-type/string-slice.html#字符串索引)。

4. 🌟🌟🌟 我们无法通过索引的方式访问字符串中的某个字符，但是可以通过切片的方式来获取字符串的某一部分 `&s1[start..end]`

```rust

// 填空并修复错误
fn main() {
    let s = String::from("hello, 世界");
    let slice1 = s[0]; //提示: `h` 在 UTF-8 编码中只占用 1 个字节
    assert_eq!(slice1, "h");

    let slice2 = &s[3..5];// 提示: `世` 在 UTF-8 编码中占用 3 个字节
    assert_eq!(slice2, "世");
    
    // 迭代 s 中的所有字符
    for (i, c) in s.__ {
        if i == 7 {
            assert_eq!(c, '世')
        }
    }

    println!("Success!")
}
```


#### utf8_slice
我们可以使用 [utf8_slice](https://docs.rs/utf8_slice/1.0.0/utf8_slice/fn.slice.html) 来按照字符的自然索引方式对 UTF-8 字符串进行切片访问，与之前的切片方式相比，它索引的是字符，而之前的方式索引的是字节.

**示例**
```rust
use utf8_slice;
fn main() {
   let s = "The 🚀 goes to the 🌑!";

   let rocket = utf8_slice::slice(s, 4, 5);
   // Will equal "🚀"
}
```


5. 🌟🌟🌟
> 提示: 也许你需要使用 `from_utf8` 方法

```rust

// 填空
fn main() {
    let mut s = String::new();
    __;

    let v = vec![104, 101, 108, 108, 111];

    // 将字节数组转换成 String
    let s1 = __;
    
    
    assert_eq!(s, s1);

    println!("Success!")
}
```

### 内部表示
事实上 `String` 是一个智能指针，它作为一个结构体存储在栈上，然后指向存储在堆上的字符串底层数据。

存储在栈上的智能指针结构体由三部分组成：一个指针只指向堆上的字节数组，已使用的长度以及已分配的容量 capacity (已使用的长度小于等于已分配的容量，当容量不够时，会重新分配内存空间)。

6. 🌟🌟 如果 String 的当前容量足够，那么添加字符将不会导致新的内存分配
```rust

// 修改下面的代码以打印如下内容: 
// 25
// 25
// 25
// 循环中不会发生任何内存分配
fn main() {
    let mut s = String::new();

    println!("{}", s.capacity());

    for _ in 0..2 {
        s.push_str("hello");
        println!("{}", s.capacity());
    }

    println!("Success!")
}
```

7. 🌟🌟🌟
```rust

// 填空
use std::mem;

fn main() {
    let story = String::from("Rust By Practice");

    // 阻止 String 的数据被自动 drop
    let mut story = mem::ManuallyDrop::new(story);

    let ptr = story.__();
    let len = story.__();
    let capacity = story.__();

    assert_eq!(16, len);

    // 我们可以基于 ptr 指针、长度和容量来重新构建 String. 
    // 这种操作必须标记为 unsafe，因为我们需要自己来确保这里的操作是安全的
    let s = unsafe { String::from_raw_parts(ptr, len, capacity) };

    assert_eq!(*story, s);

    println!("Success!")
}
```


### 常用方法(TODO)
关于 String 的常用方法练习，可以查看[这里](../std/String.md).

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/collections/String.md)找到答案(在 solutions 路径下) 
