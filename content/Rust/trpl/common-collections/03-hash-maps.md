+++
title = "8.3 用哈希映射存储键值对"
date = 2026-08-05T08:44:00+08:00
weight = 36
type = "docs"
description = "用 HashMap 存储键值对，并更新、查询与管理所有权"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用哈希映射存储键值对


> 原文链接: [https://doc.rust-lang.org/stable/book/ch08-03-hash-maps.html](https://doc.rust-lang.org/stable/book/ch08-03-hash-maps.html)


## 在哈希映射中存储带关联值的键

　　我们要讲的最后一种常见集合是哈希映射。类型 `HashMap<K, V>` 借助*哈希函数*（hashing function）存储类型为 `K` 的键到类型为 `V` 的值的映射；哈希函数决定如何把这些键和值放入内存。许多编程语言都支持这类数据结构，但往往使用不同的名字，例如 *hash*、*map*、*object*、*hash table*、*dictionary* 或 *associative array* 等等。

　　当你想按键而不是像向量那样按索引查找数据，且键可以是任意类型时，哈希映射很有用。例如，在游戏中，你可以用哈希映射跟踪每支队伍的得分：每个键是队名，值是该队得分。给定队名，就可以取回其得分。

　　本节会介绍哈希映射的基本 API，但标准库在 `HashMap<K, V>` 上定义的函数里还有更多好东西。一如既往，请查阅标准库文档了解更多信息。

### 创建新的哈希映射

　　创建空哈希映射的一种方式是使用 `new`，并用 `insert` 添加元素。在示例 8-20 中，我们跟踪两支队伍的得分，队名分别是 *Blue* 和 *Yellow*。蓝队从 10 分开始，黄队从 50 分开始。

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
```

**示例 8-20：创建新的哈希映射并插入一些键和值**

　　注意，我们需要先从标准库的 `collections` 模块 `use` 引入 `HashMap`。在我们讲的三种常见集合中，这种用得最少，因此没有包含在预导入（prelude）自动引入作用域的特性里。哈希映射从标准库得到的支持也较少；例如，没有内置的宏来构造它们。

　　与向量一样，哈希映射把数据存放在堆上。这个 `HashMap` 的键类型是 `String`，值类型是 `i32`。与向量一样，哈希映射是同质的：所有键必须是同一类型，所有值也必须是同一类型。

### 访问哈希映射中的值 {#accessing-values-in-a-hash-map}

　　我们可以通过把键传给 `get` 方法，从哈希映射中取出一个值，如示例 8-21 所示。

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    let team_name = String::from("Blue");
    let score = scores.get(&team_name).copied().unwrap_or(0);
```

**示例 8-21：访问哈希映射中存储的蓝队得分**

　　这里，`score` 将是与蓝队关联的值，结果是 `10`。`get` 方法返回 `Option<&V>`；若哈希映射中没有该键的值，`get` 会返回 `None`。这个程序通过调用 `copied` 把 `Option` 变成 `Option<i32>` 而不是 `Option<&i32>`，再用 `unwrap_or` 在 `scores` 没有该键的条目时把 `score` 设为零，来处理这个 `Option`。

　　我们可以像遍历向量那样，用 `for` 循环遍历哈希映射中的每个键值对：

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    for (key, value) in &scores {
        println!("{key}: {value}");
    }
```

　　这段代码会以任意顺序打印每一对：

```text
Yellow: 50
Blue: 10
```

### 管理哈希映射中的所有权

　　对于实现了 `Copy` 特征的类型（如 `i32`），值会被复制进哈希映射。对于像 `String` 这样拥有所有权的值，值会被移动，哈希映射将成为这些值的所有者，如示例 8-22 所示。

```rust
    use std::collections::HashMap;

    let field_name = String::from("Favorite color");
    let field_value = String::from("Blue");

    let mut map = HashMap::new();
    map.insert(field_name, field_value);
    // field_name and field_value are invalid at this point, try using them and
    // see what compiler error you get!
```

**示例 8-22：展示键和值在插入后由哈希映射拥有**

　　在调用 `insert` 把变量 `field_name` 和 `field_value` 移入哈希映射之后，我们就无法再使用它们了。

　　若我们把值的引用插入哈希映射，值本身不会被移入哈希映射。引用所指向的值必须至少在哈希映射有效期间保持有效。我们会在第 10 章[「用生命周期校验引用」][validating-references-with-lifetimes]中更多地讨论这些问题。

### 更新哈希映射

　　虽然键值对的数量可以增长，但每个唯一的键在同一时刻只能关联一个值（反过来则不然：例如，蓝队和黄队都可以在 `scores` 哈希映射中存储值 `10`）。

　　当你想更改哈希映射中的数据时，必须决定如何处理键已经有关联值的情况。你可以完全无视旧值，用新值替换它。你可以保留旧值并忽略新值，只在键*还没有*值时才加入新值。或者你可以把旧值与新值结合起来。我们来看看如何分别做到这些！

#### 覆盖一个值

　　若我们向哈希映射插入一个键和值，然后再用不同的值插入同一个键，与该键关联的值就会被替换。尽管示例 8-23 中的代码调用了两次 `insert`，哈希映射也只会包含一对键值，因为我们两次都是在为蓝队的键插入值。

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Blue"), 25);

    println!("{scores:?}");
```

**示例 8-23：替换存储在特定键下的值**

　　这段代码会打印 `{"Blue": 25}`。原来的值 `10` 已被覆盖。

#### 仅在键不存在时添加键和值

　　常见做法是检查哈希映射中某个键是否已有值，然后采取如下行动：若键已存在，现有值应保持不变；若不存在，则插入该键及其值。

　　哈希映射为此提供了名为 `entry` 的特殊 API，它接受你想检查的键作为参数。`entry` 方法的返回值是一个名为 `Entry` 的枚举，表示一个可能存在也可能不存在的值。假设我们想检查黄队的键是否已有关联值。若没有，就插入值 `50`；对蓝队也一样。使用 `entry` API 时，代码如示例 8-24 所示。

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);

    scores.entry(String::from("Yellow")).or_insert(50);
    scores.entry(String::from("Blue")).or_insert(50);

    println!("{scores:?}");
```

**示例 8-24：用 `entry` 方法仅在键尚无值时插入**

　　`Entry` 上的 `or_insert` 方法定义为：若对应 `Entry` 键已存在，就返回指向该值的可变引用；若不存在，则把参数作为该键的新值插入，并返回指向新值的可变引用。这种技巧比自己写逻辑干净得多，而且也更利于与借用检查器协作。

　　运行示例 8-24 中的代码会打印 `{"Yellow": 50, "Blue": 10}`。第一次调用 `entry` 会插入黄队的键和值 `50`，因为黄队此前没有值。第二次调用 `entry` 不会改变哈希映射，因为蓝队已经有值 `10`。

#### 基于旧值更新值

　　哈希映射的另一个常见用例是查找某个键的值，然后基于旧值更新它。例如，示例 8-25 展示了统计某段文本中每个词出现次数的代码。我们用哈希映射以词为键，并递增值来跟踪我们见过该词多少次。若是第一次见到某个词，就先插入值 `0`。

```rust
    use std::collections::HashMap;

    let text = "hello world wonderful world";

    let mut map = HashMap::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }

    println!("{map:?}");
```

**示例 8-25：用存储词与计数的哈希映射统计词的出现次数**

　　这段代码会打印 `{"world": 2, "hello": 1, "wonderful": 1}`。你也可能看到相同的键值对以不同顺序打印：回想[「访问哈希映射中的值」][access]，遍历哈希映射是以任意顺序进行的。

　　`split_whitespace` 方法返回一个迭代器，按空白分隔遍历 `text` 中的值的子切片。`or_insert` 方法返回指定键对应值的可变引用（`&mut V`）。这里我们把该可变引用存进 `count` 变量，因此要给那个值赋值，必须先用星号（`*`）解引用 `count`。可变引用在 `for` 循环结束时离开作用域，因此所有这些更改都是安全的，且为借用规则所允许。

### 哈希函数

　　默认情况下，`HashMap` 使用一种名为 *SipHash* 的哈希函数，它能提供针对涉及哈希表的拒绝服务（DoS）攻击的抵抗能力[^siphash]。这不是可用的最快哈希算法，但以一定性能下降换取更好的安全性是值得的。若你分析代码后发现默认哈希函数对你的用途太慢，可以通过指定不同的 hasher 切换到另一种函数。*hasher* 是实现了 `BuildHasher` 特征的类型。我们将在[第 10 章][traits]讨论特征以及如何实现它们。你不一定要从头实现自己的 hasher；[crates.io](https://crates.io/) 上有其他 Rust 用户分享的库，提供实现了许多常见哈希算法的 hasher。

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## 小结

　　当你需要存储、访问和修改数据时，向量、字符串和哈希映射会提供程序所需的大量功能。下面这些练习你现在应该有能力解决了：

1. 给定一个整数列表，使用向量返回该列表的中位数（排序后位于中间位置的值）和众数（出现次数最多的值；这里哈希映射会很有帮助）。
1. 把字符串转换成 Pig Latin。每个单词的第一个辅音移到词尾并加上 *ay*，因此 *first* 变成 *irst-fay*。以元音开头的词则在词尾加上 *hay*（*apple* 变成 *apple-hay*）。别忘了 UTF-8 编码的细节！
1. 使用哈希映射和向量，创建一个文本界面，允许用户把员工姓名加到公司的某个部门；例如「将 Sally 加入 Engineering」或「将 Amir 加入 Sales」。然后让用户检索某个部门的所有人员列表，或按部门检索公司所有人员，并按字母顺序排序。

　　标准库 API 文档描述了向量、字符串和哈希映射上对完成这些练习会有帮助的方法！

　　我们正进入操作可能失败的更复杂程序，因此正是讨论错误处理的好时机。下一章我们就来做这件事！

[validating-references-with-lifetimes]: /trpl/generics/03-lifetime-syntax/#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: /trpl/generics/02-traits/
