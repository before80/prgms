+++
title = "01-生命周期基础"
date = 2026-08-12T20:00:00+08:00
weight = 52
type = "docs"
description = "生命周期基础 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/lifetime/basic.html](https://practice-rust-zh.beatai.org/lifetime/basic.html)

# 生命周期基础

编译器通过生命周期来确保所有的借用都是合法的，典型的，一个变量在创建时生命周期随之开始，销毁时生命周期也随之结束。


## 生命周期的范围
1. 🌟
```rust
/* 为 `i` 和 `borrow2` 标注合适的生命周期范围 */


// `i` 拥有最长的生命周期，因为它的作用域完整的包含了 `borrow1` 和 `borrow2` 。
// 而 `borrow1` 和 `borrow2` 的生命周期并无关联，因为它们的作用域没有重叠
fn main() {
    let i = 3;                                             
    {                                                    
        let borrow1 = &i; // `borrow1` 生命周期开始. ──┐
        //                                                │
        println!("borrow1: {}", borrow1); //              │
    } // `borrow1` 生命周期结束. ──────────────────────────────────┘
    {                                                    
        let borrow2 = &i; 
                                                        
        println!("borrow2: {}", borrow2);               
    }                                                   
}   
```

2. 🌟🌟

**示例**
```rust
{
    let x = 5;            // ----------+-- 'b
                          //           |
    let r = &x;           // --+-- 'a  |
                          //   |       |
    println!("r: {}", r); //   |       |
                          // --+       |
}                         // ----------+
```


```rust
/* 像上面的示例一样，为 `r` 和 `x` 标注生命周期，然后从生命周期的角度. */

fn main() {  
    {
        let r;                // ---------+-- 'a
                              //          |
        {                     //          |
            let x = 5;        // -+-- 'b  |
            r = &x;           //  |       |
        }                     // -+       |
                              //          |
        println!("r: {}", r); //          |
    }                         // ---------+
}
```

## 生命周期标注
Rust 的借用检查器使用显式的生命周期标注来确定一个引用的合法范围。但是对于用户来说，我们在大多数场景下，都无需手动去标注生命周期，原因是编译器会在某些情况下自动应用生命周期消除规则。

在了解编译器使用哪些规则帮我们消除生命周期之前，首先还是需要知道该如何手动标记生命周期。


#### 函数
**大家先忽略生命周期消除规则**，让我们看看，函数签名中的生命周期有哪些限制:

- 需要为每个引用标注上合适的生命周期
- 返回值中的引用，它的生命周期要么跟某个引用参数相同，要么是 `'static`

**示例**
```rust
// 引用参数中的生命周期 'a 至少要跟函数活得一样久
fn print_one<'a>(x: &'a i32) {
    println!("`print_one`: x is {}", x);
}

// 可变引用依然需要标注生命周期
fn add_one<'a>(x: &'a mut i32) {
    *x += 1;
}

// 下面代码中，每个参数都拥有自己独立的生命周期，事实上，这个例子足够简单，因此它们应该被标记上相同的生命周期 `'a`，但是对于复杂的例子而言，独立的生命周期标注是可能存在的
fn print_multi<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("`print_multi`: x is {}, y is {}", x, y);
}

// 返回一个通过参数传入的引用是很常见的，但是这种情况下需要标注上正确的生命周期
fn pass_x<'a, 'b>(x: &'a i32, _: &'b i32) -> &'a i32 { x }

fn main() {
    let x = 7;
    let y = 9;
    
    print_one(&x);
    print_multi(&x, &y);
    
    let z = pass_x(&x, &y);
    print_one(z);

    let mut t = 3;
    add_one(&mut t);
    print_one(&t);
}
```

3. 🌟
```rust
/* 添加合适的生命周期标注，让下面的代码工作 */
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {}
```
4. 🌟🌟🌟
```rust
/* 使用三种方法修复下面的错误  */
fn invalid_output<'a>() -> &'a String { 
    &String::from("foo") 
}

fn main() {
}
```

5. 🌟🌟
```rust
// `print_refs` 有两个引用参数，它们的生命周期 `'a` 和 `'b` 至少得跟函数活得一样久
fn print_refs<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("x is {} and y is {}", x, y);
}

/* 让下面的代码工作 */
fn failed_borrow<'a>() {
    let _x = 12;

    // ERROR: `_x` 活得不够久does not live long enough
    let y: &'a i32 = &_x;

    // 在函数内使用 `'a` 将会报错，原因是 `&_x` 的生命周期显然比 `'a` 要小
    // 你不能将一个小的生命周期强转成大的
}

fn main() {
    let (four, nine) = (4, 9);
    

    print_refs(&four, &nine);
    // 这里，four 和 nice 的生命周期必须要比函数 print_refs 长
    
    failed_borrow();
    // `failed_borrow`  没有传入任何引用去限制生命周期 `'a`，因此，此时的 `'a` 生命周期是没有任何限制的，它默认是 `'static`
}
```

#### Structs
6. 🌟
```rust
/* 增加合适的生命周期标注，令代码正常工作 */

// `i32` 的引用必须比 `Borrowed` 活得更久
#[derive(Debug)]
struct Borrowed(&i32);

// 类似的，下面两个引用也必须比结构体 `NamedBorrowed` 活得更久
#[derive(Debug)]
struct NamedBorrowed {
    x: &i32,
    y: &i32,
}

#[derive(Debug)]
enum Either {
    Num(i32),
    Ref(&i32),
}

fn main() {
    let x = 18;
    let y = 15;

    let single = Borrowed(&x);
    let double = NamedBorrowed { x: &x, y: &y };
    let reference = Either::Ref(&x);
    let number    = Either::Num(y);

    println!("x is borrowed in {:?}", single);
    println!("x and y are borrowed in {:?}", double);
    println!("x is borrowed in {:?}", reference);
    println!("y is *not* borrowed in {:?}", number);
}
```


7. 🌟🌟
```rust
/* 让代码工作 */

#[derive(Debug)]
struct NoCopyType {}

#[derive(Debug)]
struct Example<'a, 'b> {
    a: &'a u32,
    b: &'b NoCopyType
}

fn main()
{ 
  let var_a = 35;
  let example: Example;
  
  {
    let var_b = NoCopyType {};
    
    /* 修复错误 */
    example = Example { a: &var_a, b: &var_b };
  }
  
  println!("(Success!) {:?}", example);
}
```


8. 🌟🌟
```rust

#[derive(Debug)]
struct NoCopyType {}

#[derive(Debug)]
#[allow(dead_code)]
struct Example<'a, 'b> {
    a: &'a u32,
    b: &'b NoCopyType
}

/* 修复函数的签名 */
fn fix_me(foo: &Example) -> &NoCopyType
{ foo.b }

fn main()
{
    let no_copy = NoCopyType {};
    let example = Example { a: &1, b: &no_copy };
    fix_me(&example);
    println!("Success!")
}
```

## 方法
方法的生命周期标注跟函数类似。

**示例**
```rust
struct Owner(i32);

impl Owner {
    fn add_one<'a>(&'a mut self) { self.0 += 1; }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

fn main() {
    let mut owner = Owner(18);

    owner.add_one();
    owner.print();
}
```

9. 🌟🌟
```rust
/* 添加合适的生命周期让下面代码工作 */
struct ImportantExcerpt {
    part: &str,
}

impl ImportantExcerpt {
    fn level(&'a self) -> i32 {
        3
    }
}

fn main() {}
```

## 生命周期消除( Elision )

有一些生命周期的标注方式很常见，因此编译器提供了一些规则，可以让我们在一些场景下无需去标注生命周期，既节省了敲击键盘的繁琐，又能提升可读性。

这种规则被称为生命周期消除规则( Elision )，该规则之所以存在，仅仅是因为这些场景太通用了，为了方便用户而已。事实上对于借用检查器而言，该有的生命周期一个都不能少，只不过对于用户而言，可以省去一些。


10. 🌟🌟
```rust
/* 移除所有可以消除的生命周期标注 */

fn nput<'a>(x: &'a i32) {
    println!("`annotated_input`: {}", x);
}

fn pass<'a>(x: &'a i32) -> &'a i32 { x }

fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    x
}

struct Owner(i32);

impl Owner {
    fn add_one<'a>(&'a mut self) { self.0 += 1; }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

struct Person<'a> {
    age: u8,
    name: &'a str,
}

enum Either<'a> {
    Num(i32),
    Ref(&'a i32),
}

fn main() {}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/lifetime/basic.md)找到答案(在 solutions 路径下)
