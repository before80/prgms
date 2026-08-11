+++
title = "4.1 什么是所有权？"
date = 2026-08-05T08:44:00+08:00
weight = 16
type = "docs"
description = "什么是所有权？栈与堆、移动、克隆，以及所有权如何管理内存"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 什么是所有权？


> 原文链接: [https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html](https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html)


## 什么是所有权？

　　*所有权*（ownership）是一套规则，用来管理 Rust 程序如何使用内存。所有程序在运行时都要管理计算机内存的使用方式。有些语言靠垃圾回收在运行过程中定期查找不再使用的内存；另一些语言则要求程序员显式分配和释放内存。Rust 采用第三种方式：通过所有权系统以及一组由编译器检查的规则来管理内存。只要违反任一规则，程序就无法编译。所有权相关的特性都不会在运行时拖慢你的程序。

　　对许多程序员来说，所有权是新概念，确实需要一点时间适应。好消息是：你越熟悉 Rust 和所有权规则，就越容易自然写出既安全又高效的代码。坚持下去！

　　理解了所有权，你就有了扎实基础去把握那些让 Rust 与众不同的特性。本章会通过一些例子来学习所有权，这些例子围绕一种非常常见的数据结构：字符串。

> ### 栈与堆 {#the-stack-and-the-heap}
>
> 许多编程语言并不常要求你考虑栈（stack）和堆（heap）。但在像 Rust 这样的系统编程语言里，值是在栈上还是堆上，会影响语言的行为，也会解释你为何要做出某些决策。本章后面会结合栈和堆来描述所有权的部分内容，因此这里先做简要说明作为铺垫。
>
> 栈和堆都是运行时可供代码使用的内存区域，但组织方式不同。栈按获得值的顺序存放，并以相反的顺序移除——这称为*后进先出*（last in, first out，LIFO）。可以想象一摞盘子：继续加盘子时放在最上面，需要盘子时也从最上面取；从中间或底部取放都不方便。往栈上加数据叫做*压栈*（pushing onto the stack），移除数据叫做*出栈*（popping off the stack）。栈上存放的所有数据都必须有已知的固定大小。编译期大小未知、或运行时大小可能变化的数据，则必须存放在堆上。
>
> 堆的组织程度较低：把数据放到堆上时，你请求一定大小的空间。内存分配器在堆中找到足够大的空闲位置，将其标记为已使用，并返回一个*指针*（pointer），也就是该位置的地址。这个过程叫做*在堆上分配*（allocating on the heap），有时也简称为*分配*（allocating）（往栈上压值通常不叫分配）。因为指向堆的指针本身大小已知且固定，你可以把它存在栈上；但要访问真正的数据，就必须顺着指针去找。可以类比去餐厅就座：进门时说明一行有几个人，服务员找到能坐下所有人的空桌并带你过去。若有人迟到，可以先问你们坐在哪一桌再来找你。
>
> 压栈比在堆上分配更快，因为分配器不必搜寻存放新数据的位置——位置总是栈顶。相对地，在堆上分配空间开销更大：分配器必须先找到足够大的空间，再做簿记以便下次分配。
>
> 访问堆上的数据通常也比访问栈上慢，因为你得先跟着指针走。当代处理器在内存中跳转越少往往越快。继续用餐厅类比：服务员给许多桌点单时，最有效率的做法是先在一桌拿齐所有订单再去下一桌。若在 A 桌拿一份、再到 B 桌拿一份、又回 A、再回 B，就会慢得多。同理，处理器处理彼此靠近的数据（如栈上）通常比处理相距较远的数据（堆上可能如此）更高效。
>
> 代码调用函数时，传入的值（其中可能包括指向堆数据的指针）以及函数的局部变量会被压入栈。函数结束后，这些值再出栈。
>
> 跟踪哪些代码在使用堆上的哪些数据、尽量减少堆上的重复数据、清理不再使用的堆数据以免空间耗尽——这些问题正是所有权要解决的。一旦理解了所有权，你就不需要经常去想栈和堆。但知道所有权的主要目的是管理堆数据，有助于解释它为何如此设计。

### 所有权规则

　　首先来看所有权规则。阅读后面用来说明这些规则的例子时，请把它们记在心里：

- Rust 中每个值都有一个*所有者*（owner）。
- 同一时间只能有一个所有者。
- 当所有者离开作用域时，该值会被丢弃（drop）。

### 变量作用域

　　我们已经过了基础语法阶段，后面的例子不再一律写出完整的 `fn main() {`；若你跟着敲代码，请自行把示例放进 `main` 函数。这样例子会更简洁，好把注意力放在真正重要的细节上，而不是样板代码。

　　作为所有权的第一个例子，我们来看一些变量的作用域。*作用域*（scope）是程序中某项有效的范围。看下面这个变量：

```rust
let s = "hello";
```

　　变量 `s` 指向一个字符串字面量，字符串的值被硬编码在程序文本里。从声明之处起，到当前作用域结束为止，该变量都有效。示例 4-1 用注释标出了变量 `s` 在何处有效。

```rust
    {                      // s is not valid here, since it's not yet declared
        let s = "hello";   // s is valid from this point forward

        // do stuff with s
    }                      // this scope is now over, and s is no longer valid
```

**示例 4-1：一个变量及其有效作用域**

　　换句话说，这里有两个重要时间点：

- 当 `s` *进入*作用域时，它变得有效。
- 它一直有效，直到*离开*作用域。

　　到目前为止，作用域与变量何时有效的关系，和其他编程语言类似。接下来我们在此基础上引入 `String` 类型。

### `String` 类型

　　为了说明所有权规则，我们需要比第 3 章[「数据类型」](../../common-programming-concepts/02-data-types/)一节更复杂的数据类型。此前介绍的类型大小已知，可以存在栈上，作用域结束时出栈，也能在另一段代码需要同一值时快速、简单地复制出独立实例。但我们想看存放在堆上的数据，以及 Rust 如何知道何时清理它们；`String` 类型就是很好的例子。

　　我们会把重点放在与所有权相关的 `String` 部分。这些方面同样适用于其他复杂数据类型，无论来自标准库还是你自己创建。`String` 中与所有权无关的方面会在[第 8 章](../../common-collections/02-strings/)讨论。

　　我们已经见过字符串字面量——字符串值被硬编码进程序。字面量很方便，但并非所有需要文本的场景都适用。原因之一是它们不可变；另一点是写代码时并非总能知道全部字符串内容：例如，若要接收用户输入并保存呢？正是为这些情况，Rust 提供了 `String` 类型。该类型管理堆上分配的数据，因而能存放编译期未知长度的文本。可以用 `from` 函数从字符串字面量创建 `String`，像这样：

```rust
let s = String::from("hello");
```

　　双冒号 `::` 运算符让我们可以把这个特定的 `from` 函数作为 `String` 的关联函数来调用，而不必使用诸如 `string_from` 之类的名字。第 5 章[「方法」](../../structs/03-method-syntax/)一节，以及第 7 章[「用来指代模块树中某一项的路径」](../../modules/03-paths-for-referring-to-an-item-in-the-module-tree/)讨论模块路径时，会再谈这种语法。

　　这种字符串*可以*被修改：

```rust
    let mut s = String::from("hello");

    s.push_str(", world!"); // push_str() appends a literal to a String

    println!("{s}"); // this will print `hello, world!`
```

　　那么区别在哪？为什么 `String` 可变而字面量不行？差别在于这两种类型如何处理内存。

### 内存与分配

　　对于字符串字面量，内容在编译期已知，因此文本被直接硬编码进最终可执行文件。这正是字面量又快又高效的原因。但这些性质来自字面量的不可变性。不幸的是，我们无法为每一段编译期大小未知、运行时还可能变化的文本，都在二进制里预留一块内存。

　　使用 `String` 时，为了支持可变、可增长的文本，需要在堆上分配编译期未知大小的内存来存放内容。这意味着：

- 必须在运行时向内存分配器请求内存。
- 用完 `String` 后，需要一种方式把这块内存还给分配器。

　　第一部分由我们完成：调用 `String::from` 时，其实现会请求所需内存。这在编程语言中相当普遍。

　　第二部分则不同。在带有*垃圾回收器*（garbage collector，GC）的语言里，GC 会跟踪并清理不再使用的内存，我们不必操心。在多数没有 GC 的语言里，识别内存何时不再使用并显式调用代码释放（就像请求时一样）是我们的责任。历史上，正确做到这一点一直很难：忘了就会浪费内存；过早释放会得到无效变量；释放两次也是 bug。我们需要让每一次分配内存都恰好对应一次释放内存。

　　Rust 走了另一条路：一旦拥有该内存的变量离开作用域，内存就会自动归还。下面是把示例 4-1 中的作用域例子改成使用 `String` 而非字符串字面量的版本：

```rust
    {
        let s = String::from("hello"); // s is valid from this point forward

        // do stuff with s
    }                                  // this scope is now over, and s is no
                                       // longer valid
```

　　有一个自然的时间点可以把 `String` 所需的内存还给分配器：当 `s` 离开作用域时。变量离开作用域时，Rust 会为我们调用一个特殊函数，叫做 `drop`，`String` 的作者可以在其中放入归还内存的代码。Rust 在闭合花括号处自动调用 `drop`。

> 注意：在 C++ 中，这种在项生命周期结束时释放资源的模式有时称为 *RAII*（Resource Acquisition Is Initialization，资源获取即初始化）。若你用过 RAII，会对 Rust 的 `drop` 感到熟悉。

　　这种模式深刻影响了 Rust 代码的写法。眼下看起来或许简单，但当我们希望多个变量使用堆上已分配的数据时，更复杂场景下的行为可能出人意料。接下来就来探索其中一些情况。

#### 变量与数据的交互方式：移动 {#variables-and-data-interacting-with-move}

　　在 Rust 中，多个变量可以以不同方式与同一数据交互。示例 4-2 给出一个使用整数的例子。

```rust
    let x = 5;
    let y = x;
```

**示例 4-2：将变量 `x` 的整数值赋给 `y`**

　　我们大概能猜到在做什么：「把值 `5` 绑定到 `x`；然后把 `x` 中的值复制一份并绑定到 `y`。」现在有两个变量 `x` 和 `y`，都等于 `5`。事实的确如此，因为整数是大小已知且固定的简单值，这两个 `5` 都被压到了栈上。

　　再看 `String` 版本：

```rust
    let s1 = String::from("hello");
    let s2 = s1;
```

　　看起来很相似，我们可能以为工作方式也一样：第二行会复制 `s1` 中的值并绑定到 `s2`。但实际并非完全如此。

　　看图 4-1，了解 `String` 底层发生了什么。`String` 由三部分组成（左侧所示）：指向存放字符串内容的内存的指针、长度，以及容量。这组数据存放在栈上。右侧是堆上存放内容的内存。

<img alt="两张表：第一张表示栈上的 s1，包含长度（5）、容量（5）以及指向第二张表中第一个值的指针。第二张表是堆上逐字节的字符串数据。" src="img/trpl04-01.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-1：绑定到 `s1`、内容为 `"hello"` 的 `String` 在内存中的表示</span>

　　长度是 `String` 内容当前占用的字节数。容量是 `String` 从分配器获得的总字节数。长度与容量的差别很重要，但与当前讨论无关，暂时可以忽略容量。

　　当我们把 `s1` 赋给 `s2` 时，复制的是 `String` 的数据，也就是复制栈上的指针、长度和容量。我们*不会*复制指针所指向的堆数据。换言之，内存中的数据表示如图 4-2。

<img alt="三张表：分别表示栈上的 s1 和 s2，两者都指向堆上同一份字符串数据。" src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-2：变量 `s2` 复制了 `s1` 的指针、长度和容量后的内存表示</span>

　　这种表示*不会*像图 4-3 那样——那是若 Rust 也复制堆数据时内存应有的样子。若 Rust 那样做，当堆上数据很大时，`s2 = s1` 在运行时性能上会非常昂贵。

<img alt="四张表：两张表示 s1 和 s2 的栈数据，各自指向堆上各自一份字符串数据副本。" src="img/trpl04-03.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-3：若 Rust 也复制堆数据，`s2 = s1` 可能呈现的另一种情形</span>

　　前面说过，变量离开作用域时，Rust 会自动调用 `drop` 并清理该变量的堆内存。但图 4-2 显示两个数据指针指向同一位置。这就有问题了：当 `s2` 和 `s1` 离开作用域时，它们都会试图释放同一块内存。这称为*二次释放*（double free）错误，正是我们之前提到的内存安全缺陷之一。释放两次可能导致内存损坏，进而可能引发安全漏洞。

　　为确保内存安全，在 `let s2 = s1;` 这一行之后，Rust 会认为 `s1` 不再有效，因此当 `s1` 离开作用域时不必释放任何东西。看看在创建 `s2` 之后再使用 `s1` 会发生什么——行不通：

```rust
    let s1 = String::from("hello");
    let s2 = s1;

    println!("{s1}, world!");
```

　　你会得到类似下面的错误，因为 Rust 阻止你使用已失效的引用：

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0382]: borrow of moved value: `s1`
 --> src/main.rs:5:16
  |
2 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `String`, which does not implement the `Copy` trait
3 |     let s2 = s1;
  |              -- value moved here
4 |
5 |     println!("{s1}, world!");
  |                ^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let s2 = s1.clone();
  |                ++++++++

For more information about this error, try `rustc --explain E0382`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

　　若你在其他语言中听过*浅拷贝*（shallow copy）和*深拷贝*（deep copy），那么只复制指针、长度和容量而不复制数据，听起来很像浅拷贝。但因为 Rust 同时使第一个变量失效，所以不叫浅拷贝，而称为*移动*（move）。在这个例子中，我们会说 `s1` 被*移动*到了 `s2`。实际发生的情况如图 4-4。

<img alt="三张表：分别表示栈上的 s1 和 s2，都指向堆上同一份字符串数据。由于 s1 不再有效，表 s1 被灰显；只有 s2 可用于访问堆数据。" src="img/trpl04-04.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-4：`s1` 失效后的内存表示</span>

　　问题就这样解决了！只有 `s2` 有效，它离开作用域时会独自释放内存，到此结束。

　　此外，这还隐含了一个设计选择：Rust 永远不会自动对你的数据做「深」拷贝。因此，任何*自动*发生的复制，都可以假定在运行时性能上代价很低。

#### 作用域与赋值

　　作用域、所有权，以及通过 `drop` 释放内存之间的关系，反过来也成立。当你给已有变量赋一个全新的值时，Rust 会立刻调用 `drop` 并释放原值的内存。例如下面的代码：

```rust
    let mut s = String::from("hello");
    s = String::from("ahoy");

    println!("{s}, world!");
```

　　我们先声明变量 `s`，绑定到值为 `"hello"` 的 `String`。接着立刻创建值为 `"ahoy"` 的新 `String` 并赋给 `s`。此时堆上原来的值已经没有任何引用。图 4-5 展示了此时的栈和堆数据：

<img alt="一张表示栈上字符串值的表，指向堆上第二段字符串数据（ahoy）；原来的字符串数据（hello）被灰显，因为已无法再访问。" src="img/trpl04-05.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-5：初始值被整体替换后的内存表示</span>

　　因此原始字符串立即离开作用域。Rust 会对其运行 `drop`，内存马上被释放。最后打印时，值将是 `"ahoy, world!"`。

#### 变量与数据的交互方式：克隆 {#variables-and-data-interacting-with-clone}

　　若我们*确实*想深拷贝 `String` 的堆数据，而不只是栈数据，可以使用常用方法 `clone`。第 5 章会讨论方法语法；不过方法在许多语言中都很常见，你大概已经见过。

　　下面是 `clone` 方法的实际例子：

```rust
    let s1 = String::from("hello");
    let s2 = s1.clone();

    println!("s1 = {s1}, s2 = {s2}");
```

　　这完全可行，并显式产生图 4-3 所示的行为——堆数据*确实*被复制了。

　　看到对 `clone` 的调用时，你就知道正在执行某些可能代价不菲的代码。这是一个视觉信号：这里发生了不同寻常的事。

#### 仅栈上的数据：Copy {#stack-only-data-copy}

　　还有一点我们尚未谈及。下面这段使用整数的代码——其中一部分已在示例 4-2 中出现——是有效的：

```rust
    let x = 5;
    let y = x;

    println!("x = {x}, y = {y}");
```

　　但这似乎与刚才学到的矛盾：我们没有调用 `clone`，`x` 仍然有效，也没有被移动到 `y`。

　　原因是：像整数这样在编译期已知大小的类型完全存放在栈上，复制实际值很快。因此没有理由在创建 `y` 后阻止 `x` 继续有效。换言之，这里深拷贝和浅拷贝没有区别，调用 `clone` 也不会比通常的浅拷贝多做什么，所以可以省略。

　　Rust 有一个特殊注解，叫做 `Copy` 特征（trait），可以放在像整数这样存放在栈上的类型上（特征会在[第 10 章](../../generics/02-traits/)详谈）。若类型实现了 `Copy`，使用它的变量在赋值给另一变量时不会移动，而是被简单地复制，赋值后原变量仍然有效。

　　若某个类型或其任何部分已实现 `Drop` 特征，Rust 就不允许我们再为其标注 `Copy`。若类型在值离开作用域时需要做特殊处理，却又加上了 `Copy` 注解，会得到编译期错误。如何为类型添加 `Copy` 注解以实现该特征，见附录 C 的[「可派生特征」](../../appendix/03-c-derivable-traits/)。

　　那么哪些类型实现了 `Copy`？可以查阅具体类型的文档确认，但一般规则是：任何一组简单标量值都可以实现 `Copy`；需要分配内存或某种资源的类型则不能。下面是一些实现了 `Copy` 的类型：

- 所有整数类型，如 `u32`。
- 布尔类型 `bool`，值为 `true` 和 `false`。
- 所有浮点类型，如 `f64`。
- 字符类型 `char`。
- 元组——仅当其中包含的类型也都实现 `Copy` 时。例如 `(i32, i32)` 实现了 `Copy`，但 `(i32, String)` 没有。

### 所有权与函数

　　把值传给函数的机制，与把值赋给变量类似。把变量传给函数会发生移动或复制，和赋值一样。示例 4-3 给出带注释的例子，标出了变量何时进入和离开作用域。

**文件名：`src/main.rs`**
```rust
fn main() {
    let s = String::from("hello");  // s comes into scope

    takes_ownership(s);             // s's value moves into the function...
                                    // ... and so is no longer valid here

    let x = 5;                      // x comes into scope

    makes_copy(x);                  // Because i32 implements the Copy trait,
                                    // x does NOT move into the function,
                                    // so it's okay to use x afterward.

} // Here, x goes out of scope, then s. However, because s's value was moved,
  // nothing special happens.

fn takes_ownership(some_string: String) { // some_string comes into scope
    println!("{some_string}");
} // Here, some_string goes out of scope and `drop` is called. The backing
  // memory is freed.

fn makes_copy(some_integer: i32) { // some_integer comes into scope
    println!("{some_integer}");
} // Here, some_integer goes out of scope. Nothing special happens.
```

**示例 4-3：带有所有权与作用域注释的函数**

　　若在调用 `takes_ownership` 之后再使用 `s`，Rust 会报编译期错误。这些静态检查保护我们免于犯错。试着在 `main` 里加入使用 `s` 和 `x` 的代码，看看哪里能用、哪里被所有权规则拦住。

### 返回值与作用域

　　返回值也可以转移所有权。示例 4-4 展示一个返回某值的函数，注释风格与示例 4-3 类似。

**文件名：`src/main.rs`**
```rust
fn main() {
    let s1 = gives_ownership();        // gives_ownership moves its return
                                       // value into s1

    let s2 = String::from("hello");    // s2 comes into scope

    let s3 = takes_and_gives_back(s2); // s2 is moved into
                                       // takes_and_gives_back, which also
                                       // moves its return value into s3
} // Here, s3 goes out of scope and is dropped. s2 was moved, so nothing
  // happens. s1 goes out of scope and is dropped.

fn gives_ownership() -> String {       // gives_ownership will move its
                                       // return value into the function
                                       // that calls it

    let some_string = String::from("yours"); // some_string comes into scope

    some_string                        // some_string is returned and
                                       // moves out to the calling
                                       // function
}

// This function takes a String and returns a String.
fn takes_and_gives_back(a_string: String) -> String {
    // a_string comes into
    // scope

    a_string  // a_string is returned and moves out to the calling function
}
```

**示例 4-4：转移返回值的所有权**

　　变量所有权每次都遵循同一模式：把值赋给另一变量会移动它。当包含堆数据的变量离开作用域时，除非数据的所有权已移给另一变量，否则该值会由 `drop` 清理。

　　虽然可行，但每个函数都先拿走所有权再还回来有点繁琐。若只想让函数使用某个值而不取得所有权呢？凡是传进去的东西若还想再用，就得再传回来，再加上函数体里可能想返回的其他数据——这确实烦人。

　　Rust 确实允许用元组返回多个值，如示例 4-5 所示。

**文件名：`src/main.rs`**
```rust
fn main() {
    let s1 = String::from("hello");

    let (s2, len) = calculate_length(s1);

    println!("The length of '{s2}' is {len}.");
}

fn calculate_length(s: String) -> (String, usize) {
    let length = s.len(); // len() returns the length of a String

    (s, length)
}
```

**示例 4-5：归还参数的所有权**

　　但对一个本应很常见的概念来说，过于繁琐。幸运的是，Rust 有一种在不转移所有权的情况下使用值的特性：引用。

[data-types]: ../../common-programming-concepts/02-data-types/
[ch8]: ../../common-collections/02-strings/
[traits]: ../../generics/02-traits/
[derivable-traits]: ../../appendix/03-c-derivable-traits/
[methods]: ../../structs/03-method-syntax/
[paths-module-tree]: ../../modules/03-paths-for-referring-to-an-item-in-the-module-tree/
