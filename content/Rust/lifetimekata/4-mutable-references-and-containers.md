+++
title = "4 可变引用与容器"
date = 2026-08-23T16:26:00+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_4.html](https://tfpk.github.io/lifetimekata/chapter_4.html)

就生命周期省略而言，可变引用的工作方式与普通引用完全相同。不过我们单独设一章来讲它们，是因为如果你持有可变引用，即使没有返回值，也可能需要向编译器说明生命周期。

例如，来看下面这个例子：

```rust
fn insert_value(my_vec: &mut Vec<&i32>, value: &i32) {
    my_vec.push(value);
}
```

我们没有返回任何东西；所以生命周期不重要，对吧？

不幸的是，生命周期仍然很重要。引用 `value` 实际上需要与向量中的内容存活同样长的时间。如果不是这样，向量里就可能包含无效引用。例如，在下面这个场景中会发生什么？

```rust
fn insert_value(my_vec: &mut Vec<&i32>, value: &i32) {
    my_vec.push(value);
}

fn main() {
    let x = 1;
    let my_vec = vec![&x];
    {
        let y = 2;
        insert_value(&mut my_vec, &y);
    }
    println!("{my_vec:?}");
}
```

当我们尝试打印向量时，上面例子中对 `y` 的引用已经悬空了！

我们可以用生命周期来确保这两个引用存活同样长的时间：

```rust
fn insert_value<'vec_lifetime, 'contents_lifetime>(my_vec: &'vec_lifetime mut Vec<&'contents_lifetime i32>, value: &'contents_lifetime i32) {
    my_vec.push(value)
}
fn main(){
    let mut my_vec = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1);
    insert_value(&mut my_vec, &val2);
    
    println!("{my_vec:?}");
}
```

这个签名表明存在两个生命周期：

 - `'vec_lifetime`：我们传给函数的向量需要存活一段时间。
 - `'contents_lifetime`：向量的内容需要存活一段时间。重要的是，我们要插入的新 `value` 需要与向量中的内容存活同样长的时间。如果不是这样，你最终会得到一个包含无效引用的向量。

## 我们真的需要两个生命周期吗？

你可能会想，如果不提供两个生命周期会怎样。只用一个生命周期可以吗？

```rust
fn insert_value<'one_lifetime>(my_vec: &'one_lifetime mut Vec<&'one_lifetime i32>, value: &'one_lifetime i32) {
    my_vec.push(value)
}

fn main(){
    let mut my_vec: Vec<&i32> = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1);
    insert_value(&mut my_vec, &val2);
    
    println!("{my_vec:?}");
}
```

不行。我们会得到两个错误。先看第一个：

```
error[E0499]: cannot borrow `my_vec` as mutable more than once at a time
  --> /tmp/rust.rs:11:18
   |
10 |     insert_value(&mut my_vec, &val1);
   |                  ----------- first mutable borrow occurs here
11 |     insert_value(&mut my_vec, &val2);
   |                  ^^^^^^^^^^^
   |                  |
   |                  second mutable borrow occurs here
   |                  first borrow later used here

```

这看起来很奇怪——为什么不能借用 `my_vec`？

好吧，让我们看看编译器眼中的情况：

`&val` 需要与 `my_vec` 存在的时间一样长：

```rust
# fn insert_value<'one_lifetime>(my_vec: &'one_lifetime mut Vec<&'one_lifetime i32>, value: &'one_lifetime i32) {
#     my_vec.push(value)
# }
# 
# fn main(){
    let mut my_vec: Vec<&i32> = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1); // \
    insert_value(&mut my_vec, &val2); // | - &val1 需要存活这么久。
                                      // |
    println!("{my_vec:?}");           // /
# }
```

而 `&mut my_vec` 只需要在 `insert_value` 执行期间存活。

```rust
# fn insert_value<'one_lifetime>(my_vec: &'one_lifetime mut Vec<&'one_lifetime i32>, value: &'one_lifetime i32) {
#     my_vec.push(value)
# }
# 
# fn main(){
    let mut my_vec: Vec<&i32> = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1); // <- &mut my_vec 只需要存活这么久。
    insert_value(&mut my_vec, &val2); 
    
    println!("{my_vec:?}");
# }
```

但是，我们告诉编译器 `&val1` 和 `&mut my_vec` 的借用需要共享同一个生命周期。因此编译器会延长 `&mut my_vec` 的借用以确保它们共享生命周期：
它看到如果让 `&mut my_vec` 与 `&val1` 存活一样久，就会有下面这段代码区域：

```rust
# fn insert_value<'one_lifetime>(my_vec: &'one_lifetime mut Vec<&'one_lifetime i32>, value: &'one_lifetime i32) {
#     my_vec.push(value)
# }
# 
# fn main(){
    let mut my_vec: Vec<&i32> = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1); // \
    insert_value(&mut my_vec, &val2); // | - 'one_lifetime 必须是这段代码区域。
                                      // |
    println!("{my_vec:?}");           // /
# }
```

这没问题。但现在编译器执行到下一行，发现你又想借用 `&mut my_vec`。

编译器已经决定 `&mut my_vec` 必须存在到函数结束。
所以现在，你要求它创建*两个*可变引用……而这是不允许的。

因此编译器会报错——你不允许再次借用 `&mut my_vec`。


## 为什么两个生命周期能修复这个错误？

在阅读本节之前先想一想——为什么两个生命周期能解决这个问题？

之前，编译器不得不认定 `&mut my_vec` 和 `&val1` 共享一个生命周期。
换句话说，它们彼此存活同样长。

通过使用两个生命周期，我们告诉编译器 `&mut my_vec` 和 `&val1` 不一定需要存活同样长的时间。于是，
编译器会找到以下生命周期：

```rust
fn insert_value<'vec_lifetime, 'contents_lifetime>(my_vec: &'vec_lifetime mut Vec<&'contents_lifetime i32>, value: &'contents_lifetime i32) {
    my_vec.push(value)
}

fn main(){
    let mut my_vec: Vec<&i32> = vec![];
    let val1 = 1;
    let val2 = 2;
    
    insert_value(&mut my_vec, &val1); // <- 'vec_lifetime \
    insert_value(&mut my_vec, &val2); //                  | 'contents_lifetime
                                      //                  |
    println!("{my_vec:?}");           //                  /
}
```

## 练习第一部分：另一个错误

首先，让我们看看上一节得到的另一个错误：

```
error[E0502]: cannot borrow `my_vec` as immutable because it is also borrowed as mutable
  --> /tmp/rust.rs:13:16
   |
10 |     insert_value(&mut my_vec, &val1);
   |                  ----------- mutable borrow occurs here
...
13 |     println!("{my_vec:?}");
   |                ^^^^^^
   |                |
   |                immutable borrow occurs here
   |                mutable borrow later used here
   |
```

你能解释为什么会出现这个错误吗？用 50 个词或更少写出来。

## 练习第二部分：自己动手写

为练习中的函数添加合适的生命周期。
