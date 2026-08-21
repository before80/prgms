+++
title = "03-KV 存储 HashMap"
date = 2026-08-12T20:00:00+08:00
weight = 34
type = "docs"
description = "KV 存储 HashMap — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/collections/hashmap.html](https://practice-rust-zh.beatai.org/collections/hashmap.html)

# KV 存储 HashMap

`HashMap` 默认使用 `SipHash 1-3` 哈希算法，该算法对于抵抗 `HashDos` 攻击非常有效。在性能方面，如果你的 key 是中型大小的，那该算法非常不错，但是如果是小型的 key( 例如整数 )亦或是大型的 key ( 例如字符串 )，那你需要采用社区提供的其它算法来提高性能。

哈希表的算法是基于 Google 的 [SwissTable](https://abseil.io/blog/20180927-swisstables)，你可以在[这里](https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h)找到 C++ 的实现，同时在 [CppCon talk](https://www.youtube.com/watch?v=ncHmEUmJZf4) 上也有关于算法如何工作的演讲。

### 基本操作

1. 🌟🌟

```rust

// 填空并修复错误
use std::collections::HashMap;
fn main() {
    let mut scores = HashMap::new();
    scores.insert("Sunface", 98);
    scores.insert("Daniel", 95);
    scores.insert("Ashley", 69.0);
    scores.insert("Katie", "58");

    // get 返回一个 Option<&V> 枚举值
    let score = scores.get("Sunface");
    assert_eq!(score, Some(98));

    if scores.contains_key("Daniel") {
        // 索引返回一个值 V
        let score = scores["Daniel"];
        assert_eq!(score, __);
        scores.remove("Daniel");
    }

    assert_eq!(scores.len(), __);

    for (name, score) in scores {
        println!("The score of {} is {}", name, score)
    }
}
```

2. 🌟🌟

```rust

use std::collections::HashMap;
fn main() {
    let teams = [
        ("Chinese Team", 100),
        ("American Team", 10),
        ("France Team", 50),
    ];

    let mut teams_map1 = HashMap::new();
    for team in &teams {
        teams_map1.insert(team.0, team.1);
    }

    // 使用两种方法实现 team_map2
    // 提示:其中一种方法是使用 `collect` 方法
    let teams_map2...

    assert_eq!(teams_map1, teams_map2);

    println!("Success!")
}
```

3. 🌟🌟

```rust

// 填空
use std::collections::HashMap;
fn main() {
    // 编译器可以根据后续的使用情况帮我自动推断出 HashMap 的类型，当然你也可以显式地标注类型：HashMap<&str, u8>
    let mut player_stats = HashMap::new();

    // 查询指定的 key, 若不存在时，则插入新的 kv 值
    player_stats.entry("health").or_insert(100);

    assert_eq!(player_stats["health"], __);

    // 通过函数来返回新的值
    player_stats.entry("health").or_insert_with(random_stat_buff);
    assert_eq!(player_stats["health"], __);

    let health = player_stats.entry("health").or_insert(50);
    assert_eq!(health, __);
    *health -= 50;
    assert_eq!(*health, __);

    println!("Success!")
}

fn random_stat_buff() -> u8 {
    // 为了简单，我们没有使用随机，而是返回一个固定的值
    42
}
```

### HashMap key 的限制

任何实现了 `Eq` 和 `Hash` 特征的类型都可以用于 `HashMap` 的 key，包括:

- `bool` (虽然很少用到，因为它只能表达两种 key)
- `int`, `uint` 以及它们的变体，例如 `u8`、`i32` 等
- `String` 和 `&str` (提示: `HashMap` 的 key 是 `String` 类型时，你其实可以使用 `&str` 配合 `get` 方法进行查询

需要注意的是，`f32` 和 `f64` 并没有实现 `Hash`，原因是 [浮点数精度](https://en.wikipedia.org/wiki/Floating-point_arithmetic#Accuracy_problems) 的问题会导致它们无法进行相等比较。

如果一个集合类型的所有字段都实现了 `Eq` 和 `Hash`,那该集合类型会自动实现 `Eq` 和 `Hash`。例如 `Vect<T>` 要实现 `Hash`，那么首先需要 `T` 实现 `Hash`。

4. 🌟🌟

```rust

// 修复错误
// 提示: `derive` 是实现一些常用特征的好办法
use std::collections::HashMap;

struct Viking {
    name: String,
    country: String,
}

impl Viking {
    fn new(name: &str, country: &str) -> Viking {
        Viking {
            name: name.to_string(),
            country: country.to_string(),
        }
    }
}

fn main() {
    // 使用 HashMap 来存储 viking 的生命值
    let vikings = HashMap::from([
        (Viking::new("Einar", "Norway"), 25),
        (Viking::new("Olaf", "Denmark"), 24),
        (Viking::new("Harald", "Iceland"), 12),
    ]);

    // 使用 derive 的方式来打印 viking 的当前状态
    for (viking, health) in &vikings {
        println!("{:?} has {} hp", viking, health);
    }
}
```

### 容量

关于容量，我们在之前的 [Vector](https://practice-zh.course.rs/collections/vector.html#容量) 中有详细的介绍，而 `HashMap` 也可以调整容量: 你可以通过 `HashMap::with_capacity(uint)` 使用指定的容量来初始化，或者使用 `HashMap::new()` ，后者会提供一个默认的初始化容量。

#### 示例

```rust

use std::collections::HashMap;
fn main() {
    let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);
    map.insert(1, 2);
    map.insert(3, 4);
    // 事实上，虽然我们使用了 100 容量来初始化，但是 map 的容量很可能会比 100 更多
    assert!(map.capacity() >= 100);

    // 对容量进行收缩，你提供的值仅仅是一个允许的最小值，实际上，Rust 会根据当前存储的数据量进行自动设置，当然，这个值会尽量靠近你提供的值，同时还可能会预留一些调整空间

    map.shrink_to(50);
    assert!(map.capacity() >= 50);

    // 让 Rust  自行调整到一个合适的值，剩余策略同上
    map.shrink_to_fit();
    assert!(map.capacity() >= 2);
    println!("Success!")
}
```

### 所有权

对于实现了 `Copy` 特征的类型，例如 `i32`，那类型的值会被拷贝到 `HashMap` 中。而对于有所有权的类型，例如 `String`，它们的值的所有权将被转移到 `HashMap` 中。

5. 🌟🌟

```rust
// 修复错误，尽可能少的去修改代码
// 不要移除任何代码行！
use std::collections::HashMap;
fn main() {
  let v1 = 10;
  let mut m1 = HashMap::new();
  m1.insert(v1, v1);
  println!("v1 is still usable after inserting to hashmap : {}", v1);

  let v2 = "hello".to_string();
  let mut m2 = HashMap::new();
  // 所有权在这里发生了转移
  m2.insert(v2, v1);

  assert_eq!(v2, "hello");

   println!("Success!")
}
```

### 三方库 Hash 库

在开头，我们提到过如果现有的 `SipHash 1-3` 的性能无法满足你的需求，那么可以使用社区提供的替代算法。

例如其中一个社区库的使用方式如下：

```rust
use std::hash::BuildHasherDefault;
use std::collections::HashMap;
// 引入第三方的哈希函数
use twox_hash::XxHash64;


let mut hash: HashMap<_, _, BuildHasherDefault<XxHash64>> = Default::default();
hash.insert(42, "the answer");
assert_eq!(hash.get(&42), Some(&"the answer"));
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice/blob/master/solutions/collections/Hashmap.md)找到答案(在 solutions 路径下) 
