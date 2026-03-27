+++
title = "第 6 章 集合"
weight = 60
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter 06 集合（Collections）

欢迎来到 Rust 世界中最激动人心的章节之一——集合（Collections）！如果说 Rust 的所有权系统是这座语言大厦的钢筋水泥，那么集合就是这座大厦的储物间、衣柜、冰箱和杂货铺。想象一下，你搬进了一栋设计精巧的智能公寓，公寓里的每个家具都能自动适应你的存储需求，需要多少空间就自动伸展多少空间，这就是 Rust 集合带给你的体验。

在编程的日常工作中，我们每天都在和"一堆数据"打交道。你需要存储用户的购物车内容、需要记住游戏里所有敌人的坐标、需要快速查找某个单词的释义——这些统统离不开集合。Rust 的标准库为我们提供了强大而多样的集合类型，它们各自有自己的超能力，也各自有自己的使用场景。学会选择和使用正确的集合，就如同学会使用瑞士军刀上的每一把小工具——看似简单，实则大有学问。

在本章中，我们将深入探索 Rust 标准库中最常用的集合类型。我们会从最受欢迎的 Vec<T> 开始，然后钻进神秘的 Box<T> 堆世界，接着探索 HashMap 和 HashSet 的哈希魔法，还会顺便拜访一下 LinkedList、VecDeque、BinaryHeap 等其他有趣的集合类型。最后，我们还会介绍一些标准库中的核心类型，如 Option<T>、Iterator、Range、Cow 和 Cell/RefCell，它们虽然严格来说不全是"集合"，但在 Rust 编程中扮演着不可或缺的角色，我们当然不能冷落这些重要的配角。

让我们开始这场关于 Rust 集合的奇妙冒险吧！

## 6.1 Vec<T>（动态数组）

Vec<T> 是 Rust 中最常用、最讨喜、最能装的集合类型。它的名字 "Vec" 来自 "Vector"（向量）的缩写，但你完全可以把它想象成一个魔法口袋——一个可以自动伸缩的购物袋、一个会变大变小的衣柜、或者一只胃容量可以随食物数量自动调节的神秘生物。在 Rust 编程中，几乎没有什么问题是创建一个 Vec 不能解决的，如果一个问题真的解决不了，那就创建两个 Vec。

Vec<T> 中的 T 是一个泛型参数，意味着它可以存储任何你喜欢的类型：整数、字符串、结构体、甚至另一个 Vec（嵌套 Vec，完美符合递归美学）。Vec 在内存中的表示非常有趣：它把所有的元素紧紧地排列在一块连续的内存区域中，就像酒店走廊两侧紧挨着的房间。这种内存布局带来了一些很有意思的特性——访问元素快如闪电（只需要计算偏移量），CPU 缓存命中率高得让其他动态数据结构羡慕不已。

但是等等，Vec 凭什么能够"动态"伸缩呢？毕竟连续的内存区域不是你想变大就能变大的呀？这个问题问得好！Vec 实际上是这么工作的：它会在堆（heap）上预先申请一块比当前需要更大的内存空间，这块空间叫做容量（capacity）。当你往 Vec 里塞元素时，只要元素数量还没达到容量限制，Vec 就只需要把新元素塞到下一个空闲位置就行了，根本不需要重新分配内存。只有当元素数量真的要爆表的时候，Vec 才会痛苦地（实际上是一个非常昂贵的操作）申请一块更大的内存，把所有元素搬过去，然后悄悄地扩容。这就像是一个有远见的搬家工人，总是提前打包好比现在需要的更大的箱子，这样下次有新东西要装的时候，就不用每次都重新打包了。

### 6.1.1 创建方式

创建 Vec 的方法有三种，每种都有它独特的适用场景和使用美学。让我来一一介绍这些创建 Vec 的"姿势"。

#### 6.1.1.1 vec![] 宏

vec![] 宏是创建 Vec 最便捷、最直观的方式，尤其适合在初始化时就知道要放什么元素的情况。这个宏的语法设计得非常优雅，看起来就像是 Rust 语言本身在告诉你："嘿，我这里有一个向量字面量！"

```rust
fn main() {
    // 创建一个包含整数的 Vec，使用 vec![] 宏
    // 这是最直观的方式，就像是在说："给我来一个装着 1, 2, 3, 4, 5 的盒子"
    let numbers = vec![1, 2, 3, 4, 5];
    println!("numbers = {:?}", numbers); // numbers = [1, 2, 3, 4, 5]

    // vec![] 宏还支持重复字面量的语法，使用 初始值, 长度 的格式
    // 想象一下你要初始化一个全明星篮球队，全是 MVP 级别的球员（虽然不太现实）
    let all_stars = vec!["MVP"; 5];
    println!("all_stars = {:?}", all_stars); // all_stars = ["MVP", "MVP", "MVP", "MVP", "MVP"]

    // 如果你想创建一个空 Vec 但带上类型注解（类型很重要！Rust 是静态类型语言）
    let empty_vec: Vec<i32> = vec![];
    println!("empty_vec = {:?}", empty_vec); // empty_vec = []

    // 创建包含字符串的 Vec
    let fruits = vec!["apple", "banana", "orange"];
    println!("fruits = {:?}", fruits); // fruits = ["apple", "banana", "orange"]

    // 创建嵌套 Vec - 这就像是在一个抽屉里放更多的小抽屉
    let matrix = vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]];
    println!("matrix = {:?}", matrix); // matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
}
```

vec![] 宏的内部实现其实非常巧妙。当你使用 vec![1, 2, 3] 这样的语法时，宏会在编译时就计算出你需要的元素个数，然后调用 Vec::with_capacity 来预先分配合适的内存，最后再一一填入元素。这个过程快得飞起，而且完全没有运行时的语法解析开销。

#### 6.1.1.2 Vec::new()

有时候你在创建 Vec 的时候还不太清楚里面要放什么元素，或者元素是在后面的代码中一点一点添加进来的。这时候 Vec::new() 就派上用场了。顾名思义，Vec::new() 就是创建一个全新的、空的 Vec。

```rust
fn main() {
    // 创建一个空的 Vec，类型注解是必须的，否则 Rust 不知道你想存什么
    // 这就像是在说："我需要一个盒子，但里面装什么我还没想好，先留空"
    let mut empty_vec: Vec<i32> = Vec::new();
    println!("empty_vec before push = {:?}", empty_vec); // empty_vec before push = []

    // 往空 Vec 里添加元素
    empty_vec.push(1);
    empty_vec.push(2);
    empty_vec.push(3);
    println!("empty_vec after push = {:?}", empty_vec); // empty_vec after push = [1, 2, 3]

    // 创建一个存储字符串的空白 Vec
    let mut names: Vec<String> = Vec::new();
    names.push(String::from("Alice"));
    names.push(String::from("Bob"));
    names.push(String::from("Charlie"));
    println!("names = {:?}", names); // names = ["Alice", "Bob", "Charlie"]

    // 创建一个存储自定义结构体的 Vec
    struct Person {
        name: String,
        age: u32,
    }

    let mut people: Vec<Person> = Vec::new();
    people.push(Person {
        name: String::from("David"),
        age: 25,
    });
    people.push(Person {
        name: String::from("Eve"),
        age: 30,
    });
    println!("people = {:?}", people);
    // people = [Person { name: "David", age: 25 }, Person { name: "Eve", age: 30 }]
}
```

Vec::new() 实际上调用的是 Vec::with_capacity(0)，也就是说，它创建了一个容量为 0 的空 Vec。第一次往里面添加元素时，Rust 会触发一次容量为 1 的分配。这对于那些你确定只会添加一两个元素的场景来说是很高效的，但如果你的 Vec 预计会存储很多元素，使用 with_capacity 预分配可能会更聪明一些。

#### 6.1.1.3 Vec::with_capacity(capacity)

Vec::with_capacity() 是那种"我全知道"的创建方式——你知道你大概需要多少空间，提前跟 Rust 说好，让它一次性准备好一切。这种方式特别适合那些你知道大致规模的场景，避免了 Vec 多次扩容的性能开销。

```rust
fn main() {
    // 创建一个预分配能存 100 个元素的 Vec
    // 这就像是在说："我要开一个大型派对，预计来 100 人，我先准备好足够的座位"
    let mut prealloc_vec: Vec<i32> = Vec::with_capacity(100);
    println!("初始容量 = {}", prealloc_vec.capacity()); // 初始容量 = 100
    println!("初始长度 = {}", prealloc_vec.len()); // 初始长度 = 0

    // 现在往里面添加元素，在容量耗尽之前，都不需要重新分配内存
    for i in 0..50 {
        prealloc_vec.push(i);
    }
    println!("添加50个元素后，长度 = {}, 容量 = {}", prealloc_vec.len(), prealloc_vec.capacity());
    // 添加50个元素后，长度 = 50, 容量 = 100

    // 再添加 50 个，恰好用完预分配的容量
    for i in 50..100 {
        prealloc_vec.push(i);
    }
    println!("添加100个元素后，长度 = {}, 容量 = {}", prealloc_vec.len(), prealloc_vec.capacity());
    // 添加100个元素后，长度 = 100, 容量 = 100

    // 添加第 101 个元素时，Vec 会触发扩容
    prealloc_vec.push(100);
    println!("添加101个元素后，长度 = {}, 容量 = {}", prealloc_vec.len(), prealloc_vec.capacity());
    // 添加101个元素后，长度 = 101, 容量 = 200

    // 另一个例子：读取文件所有行
    // 假设我们知道文件大概有 1000 行
    let mut lines: Vec<String> = Vec::with_capacity(1000);
    // 模拟添加一些"行"
    lines.push(String::from("第一行内容"));
    lines.push(String::from("第二行内容"));
    lines.push(String::from("第三行内容"));
    println!("lines 实际使用了 {} 个元素，预分配了 {} 个元素的空间",
             lines.len(), lines.capacity());
    // lines 实际使用了 3 个元素，预分配了 1000 个元素的空间
}
```

使用 with_capacity 的艺术在于，你需要对你的用例有一个合理的预估。分配太多会造成内存浪费（虽然不是泄漏，但那些预留的空间你不用别人也用不了），分配太少又会回到频繁扩容的老路。一般来说，如果你能猜到大概的数量级（比如"几十个"、"几百个"、"几千个"），那预分配一个差不多大小的容量就是个好主意。

下面是一个有趣的对比实验，展示了预分配和不预分配的性能差异：

```rust
fn main() {
    use std::time::Instant;

    // 场景1：不预分配，频繁扩容
    let start = Instant::now();
    let mut no_prealloc = Vec::new();
    for i in 0..10_000 {
        no_prealloc.push(i);
    }
    let no_prealloc_duration = start.elapsed();
    println!("不预分配耗时: {:?}", no_prealloc_duration);
    // 不预分配耗时: ~几十到几百微秒（取决于系统状态）

    // 场景2：预分配足够的容量
    let start = Instant::now();
    let mut with_prealloc = Vec::with_capacity(10_000);
    for i in 0..10_000 {
        with_prealloc.push(i);
    }
    let with_prealloc_duration = start.elapsed();
    println!("预分配耗时: {:?}", with_prealloc_duration);
    // 预分配耗时: ~几微秒到几十微秒

    // 场景3：严重低估容量
    let start = Instant::now();
    let mut under_prealloc = Vec::with_capacity(10);
    for i in 0..10_000 {
        under_prealloc.push(i);
    }
    let under_prealloc_duration = start.elapsed();
    println!("严重低估容量耗时: {:?}", under_prealloc_duration);
    // 严重低估容量耗时: 比不预分配还慢，因为多了一次"以为够用结果不够"的痛苦

    // 结论：预分配合适的容量是王道
    println!("性能对比：预分配 vs 不预分配 = {:.2}x",
             no_prealloc_duration.as_nanos() as f64 / with_prealloc.as_nanos() as f64);
}
```

### 6.1.2 元素的增删改查

如果说创建一个 Vec 是拿到了一个空盒子，那么对 Vec 进行增删改查就是在这个盒子里塞东西、取东西、换东西、找东西的艺术。这一节我们将详细介绍 Vec 的各种元素操作方法。记住一个重要的原则：Vec 在 Rust 中是可变的（通过 mut 关键字），你可以随时改变它的内容，但这些改变必须遵守所有权和借用的规则。

#### 6.1.2.1 push 追加元素

push 是往 Vec 的尾部添加元素的 method。这是 Vec 最常用的操作之一，因为很多场景下我们都是从空集合开始，一点一点往里面添加元素的。想象 push 就像是往一个右边开口的队列里扔球，球会一个接一个地排列在最后面。

```rust
fn main() {
    // 创建一个空的 Vec 用于存储整数
    let mut numbers: Vec<i32> = Vec::new();

    // 使用 push 方法往尾部添加元素
    // push 的特点是：总是把元素加到"最后面"
    numbers.push(10);
    println!("push 10 后: {:?}", numbers); // push 10 后: [10]

    numbers.push(20);
    println!("push 20 后: {:?}", numbers); // push 20 后: [10, 20]

    numbers.push(30);
    println!("push 30 后: {:?}", numbers); // push 30 后: [10, 20, 30]

    // push 可以连续使用，形成链式操作的视觉效果
    let mut fruits: Vec<&str> = Vec::new();
    fruits.push("apple");
    fruits.push("banana");
    fruits.push("orange");
    fruits.push("grape");
    fruits.push("watermelon");
    println!("水果列表: {:?}", fruits);
    // 水果列表: ["apple", "banana", "orange", "grape", "watermelon"]

    // push 的性能特点：
    // - 如果 Vec 还有剩余容量，push 是 O(1) 操作，非常快
    // - 如果 Vec 容量不足，需要扩容，push 会变成 O(n) 操作（需要移动所有元素）
    // 所以如果你知道大概要存多少元素，用 with_capacity 预分配是明智之举

    // 一个有趣的例子：用 push 构建一个斐波那契数列
    let mut fibonacci: Vec<u64> = Vec::new();
    fibonacci.push(0);
    fibonacci.push(1);
    println!("斐波那契: {:?}", fibonacci);
    // 斐波那契: [0, 1]

    while fibonacci.len() < 20 {
        let len = fibonacci.len();
        let next = fibonacci[len - 1] + fibonacci[len - 2];
        fibonacci.push(next);
    }
    println!("前20个斐波那契数: {:?}", fibonacci);
    // 前20个斐波那契数: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181]
}
```

push 方法的签名是 `fn push(&mut self, value: T)`，它获取了 Vec 的可变引用，这意味着在 push 执行期间，你不能有其他对这个 Vec 的借用。这通常不是问题，因为 push 通常是一个很快的操作。但如果你的 Vec 非常大，每次 push 都要小心翼翼地遵守借用规则，有时候还是挺烦人的（开玩笑的，Rust 编译器比你更烦人，它会帮你揪出所有的借用错误）。

#### 6.1.2.2 pop 弹出末尾元素

pop 是 push 的反义词——它从 Vec 的尾部移除一个元素，并返回这个元素的值。如果 Vec 是空的，pop 会返回 None。这就像是一个右边开口的队列，你只能从右边取走最后放进去的那个球。经典的"后进先出"（LIFO）数据结构操作。

```rust
fn main() {
    let mut stack: Vec<i32> = vec![10, 20, 30, 40, 50];
    println!("原始 stack: {:?}", stack); // 原始 stack: [10, 20, 30, 40, 50]

    // pop 返回的是 Option<T>，因为 Vec 可能为空
    // 使用 match 来处理可能的情况
    let top = stack.pop();
    match top {
        Some(value) => println!("pop 出来的元素: {}", value), // pop 出来的元素: 50
        None => println!("Vec 是空的！"),
    }
    println!("pop 一次后: {:?}", stack); // pop 一次后: [10, 20, 30, 40]

    // 连续 pop，模拟栈的行为
    let mut elements: Vec<char> = vec!['A', 'B', 'C', 'D', 'E'];
    println!("\n元素队列: {:?}", elements); // 元素队列: ['A', 'B', 'C', 'D', 'E']

    // 栈的特点是后进先出，所以 pop 的顺序是 E, D, C, B, A
    while !elements.is_empty() {
        let item = elements.pop().unwrap(); // 使用 unwrap 是安全的，因为我们已经检查了 !is_empty()
        println!("pop 出了: {}", item);
    }
    // pop 出了: E
    // pop 出了: D
    // pop 出了: C
    // pop 出了: B
    // pop 出了: A

    println!("全部 pop 完后: {:?}", elements); // 全部 pop 完后: []

    // pop 的一个经典应用：检查括号匹配
    let expression = "(())";
    let mut balance: Vec<char> = Vec::new();
    let mut is_balanced = true;

    for c in expression.chars() {
        match c {
            '(' => balance.push('('),
            ')' => {
                if balance.pop() != Some('(') {
                    is_balanced = false;
                    break;
                }
            }
            _ => {}
        }
    }

    if is_balanced && balance.is_empty() {
        println!("括号 \"{}\" 是匹配的", expression); // 括号 "(())" 是匹配的
    } else {
        println!("括号 \"{}\" 不匹配", expression);
    }

    // 另一个例子：模拟撤销操作
    #[derive(Debug, Clone)]
    struct Document {
        content: String,
    }

    let mut document = Document { content: String::new() };
    let mut history: Vec<Document> = Vec::new();

    document.content = "第一版内容".to_string();
    history.push(document.clone());
    println!("保存版本1: {:?}", document.content); // 保存版本1: 第一版内容

    document.content = "第二版内容".to_string();
    history.push(document.clone());
    println!("保存版本2: {:?}", document.content); // 保存版本2: 第二版内容

    document.content = "第三版内容".to_string();
    println!("当前版本: {:?}", document.content); // 当前版本: 第三版内容

    // 撤销到上一个版本
    if let Some(previous) = history.pop() {
        document = previous;
        println!("撤销到: {:?}", document.content); // 撤销到: 第二版内容
    }
}
```

pop 和 push 配合使用，就形成了一个完美的栈（Stack）数据结构。栈在计算机科学中的应用非常广泛：函数调用栈、括号匹配、撤销/重做功能、表达式求值、深度优先搜索等等。掌握 Vec 的 push 和 pop，就掌握了半个数据结构的世界。

#### 6.1.2.3 insert(i, value)

insert 是在 Vec 的任意位置插入元素的方法，而不像 push 那样只能加到末尾。insert 的签名是 `fn insert(&mut self, index: usize, element: T)`，它会在 index 位置插入 element，原先在这个位置及之后的元素都会向右移动一位。

```rust
fn main() {
    let mut colors: Vec<&str> = vec!["red", "green", "blue"];
    println!("原始列表: {:?}", colors); // 原始列表: ["red", "green", "blue"]

    // 在索引 0 处插入元素，原来的元素都向右移动
    colors.insert(0, "yellow");
    println!("在索引0插入 'yellow': {:?}", colors); // 在索引0插入 'yellow': ["yellow", "red", "green", "blue"]

    // 在中间插入
    colors.insert(2, "purple");
    println!("在索引2插入 'purple': {:?}", colors); // 在索引2插入 'purple': ["yellow", "red", "purple", "green", "blue"]

    // 在末尾插入（虽然用 push 更方便）
    colors.insert(colors.len(), "orange");
    println!("在末尾插入 'orange': {:?}", colors); // 在末尾插入 'orange': ["yellow", "red", "purple", "green", "blue", "orange"]

    // insert 的性能警告：这是一个 O(n) 操作！
    // 因为插入位置之后的所有元素都需要向右移动一位
    // 如果你经常在开头插入元素，考虑使用 VecDeque（后面会讲到）

    let mut large_vec: Vec<i32> = (0..1000).collect();
    println!("大 Vec 的长度: {}, 前5个元素: {:?}", large_vec.len(), &large_vec[..5]);
    // 大 Vec 的长度: 1000, 前5个元素: [0, 1, 2, 3, 4]

    // 在开头插入一个元素
    large_vec.insert(0, -1);
    println!("插入后，前6个元素: {:?}", &large_vec[..6]);
    // 插入后，前6个元素: [-1, 0, 1, 2, 3, 4]
    // 整个 Vec 的尾巴都被推后了一位

    // 场景：维护一个有序列表
    let mut sorted: Vec<i32> = vec![1, 3, 5, 7, 9];
    println!("\n有序列表: {:?}", sorted); // 有序列表: [1, 3, 5, 7, 9]

    // 找到正确的插入位置
    let new_value = 6;
    let insert_pos = sorted.iter().position(|&x| x > new_value).unwrap_or(sorted.len());
    sorted.insert(insert_pos, new_value);
    println!("插入 {} 后: {:?}", new_value, sorted); // 插入 6 后: [1, 3, 5, 6, 7, 9]

    // 注意：insert 可能导致 panic！
    // 如果 index > len，程序会崩溃
    let mut short_vec = vec![1, 2, 3];
    // short_vec.insert(100, 4); // 这行如果取消注释，运行时会 panic!
    println!("short_vec = {:?}", short_vec);
}
```

insert 方法虽然灵活，但它的性能代价是昂贵的。如果你在 Vec 的开头或中间插入元素，所有后面的元素都需要移动一位，这在元素数量庞大的时候会成为性能瓶颈。如果你需要频繁地在序列两端进行插入操作，VecDeque<T> 是一个更好的选择，它专门优化了双端的插入操作。

#### 6.1.2.4 remove(i)

remove 与 insert 恰恰相反——它根据索引移除元素，被移除元素后面的所有元素都会向左移动一位填补空缺。remove 返回被移除的值，如果索引越界（大于等于 Vec 的长度），则会触发 panic。

```rust
fn main() {
    let mut animals: Vec<&str> = vec!["dog", "cat", "elephant", "giraffe", "lion"];
    println!("动物列表: {:?}", animals); // 动物列表: ["dog", "cat", "elephant", "giraffe", "lion"]

    // 移除索引 2 的元素 ("elephant")
    let removed = animals.remove(2);
    println!("移除了 '{}'", removed); // 移除了 'elephant'
    println!("移除后: {:?}", animals); // 移除后: ["dog", "cat", "giraffe", "lion"]

    // 再移除索引 0 的元素 ("dog")
    let first = animals.remove(0);
    println!("移除了第一个 '{}'", first); // 移除了第一个 'dog'
    println!("再移除后: {:?}", animals); // 再移除后: ["cat", "giraffe", "lion"]

    // remove 也会导致后面的元素向左移动
    let mut numbers: Vec<i32> = vec![10, 20, 30, 40, 50];
    println!("\n数字序列: {:?}", numbers); // 数字序列: [10, 20, 30, 40, 50]

    let removed_middle = numbers.remove(1); // 移除 20
    println!("移除索引1的元素: {}，剩余: {:?}", removed_middle, numbers);
    // 移除索引1的元素: 20，剩余: [10, 30, 40, 50]

    // remove 的性能：O(n)，因为需要移动被移除元素之后的所有元素
    // 这和 insert 是同样的复杂度

    // 场景：移除所有满足条件的元素（注意迭代中修改 Vec 的陷阱）
    let mut scores: Vec<i32> = vec![85, 92, 45, 78, 99, 60, 35, 88];
    println!("\n原始分数: {:?}", scores); // 原始分数: [85, 92, 45, 78, 99, 60, 35, 88]

    // 错误的方法：不要在遍历 Vec 时直接 remove（会导致索引错乱）
    // for i in 0..scores.len() {
    //     if scores[i] < 60 {
    //         scores.remove(i); // 危险！索引会乱掉
    //     }
    // }

    // 正确的方法1：使用 retain（后面会讲）
    scores.retain(|&score| score >= 60);
    println!("60分以上的分数: {:?}", scores); // 60分以上的分数: [85, 92, 78, 99, 60, 88]

    // 正确的方法2：收集要移除的索引，然后反向移除
    let mut data: Vec<char> = vec!['a', 'b', 'c', 'd', 'e', 'f'];
    println!("\n字符数据: {:?}", data); // 字符数据: ['a', 'b', 'c', 'd', 'e', 'f']

    let indices_to_remove: Vec<usize> = data.iter()
        .enumerate()
        .filter(|(_, &c)| c == 'b' || c == 'd' || c == 'f')
        .map(|(i, _)| i)
        .collect();

    for index in indices_to_remove.iter().rev() {
        let removed_char = data.remove(*index);
        println!("移除了 '{}'", removed_char);
    }
    println!("最终数据: {:?}", data); // 最终数据: ['a', 'c', 'e']

    // 场景：实现一个简单的待办事项列表
    #[derive(Debug)]
    struct Task {
        id: u32,
        description: String,
        completed: bool,
    }

    let mut tasks: Vec<Task> = vec![
        Task { id: 1, description: String::from("写代码"), completed: false },
        Task { id: 2, description: String::from("写文档"), completed: true },
        Task { id: 3, description: String::from("测试"), completed: false },
    ];
    println!("\n任务列表: {:?}", tasks);

    // 移除已完成的任务
    let initial_len = tasks.len();
    tasks.retain(|task| !task.completed);
    println!("移除了 {} 个已完成任务，剩余: {:?}", initial_len - tasks.len(), tasks);
    // 移除了 1 个已完成任务，剩余: [Task { id: 1, ... }, Task { id: 3, ... }]
}
```

remove 方法虽然简单直接，但在处理大量数据时要注意它的性能问题。每次 remove 都需要移动被移除元素之后的所有元素，时间复杂度是 O(n)。如果你需要频繁地从 Vec 中删除元素，可能需要考虑其他数据结构，比如 LinkedList（但 LinkedList 也有它自己的问题，我们后面会详细讨论）。

#### 6.1.2.5 get(i) / get_mut(i)

get 和 get_mut 是 Vec 的安全访问方法，它们接受一个索引，返回一个指向元素的引用（get 返回 `Option<&T>`，get_mut 返回 `Option<&mut T>`）。与直接使用下标 `vec[i]` 不同，get 方法不会在索引越界时直接 panic，而是返回一个 None，让你有机会优雅地处理这种情况。

```rust
fn main() {
    let fruits: Vec<&str> = vec!["apple", "banana", "orange", "grape", "mango"];
    println!("水果列表: {:?}", fruits); // 水果列表: ["apple", "banana", "orange", "grape", "mango"]

    // 使用 get 方法安全访问元素
    // get 返回 Option<&T>，所以需要处理 None 的情况
    match fruits.get(0) {
        Some(fruit) => println!("第一个水果: {}", fruit), // 第一个水果: apple
        None => println!("索引越界！"),
    }

    match fruits.get(2) {
        Some(fruit) => println!("第三个水果: {}", fruit), // 第三个水果: orange
        None => println!("索引越界！"),
    }

    // 访问越界索引不会 panic，只会返回 None
    match fruits.get(100) {
        Some(fruit) => println!("第101个水果: {}", fruit),
        None => println!("索引100越界了，返回 None，很安全！"), // 索引100越界了，返回 None，很安全！
    }

    // get 方法也可以直接用 if let 来简化
    if let Some(fruit) = fruits.get(1) {
        println!("第二个水果是: {}", fruit); // 第二个水果是: banana
    }

    // 使用 get_mut 获取可变引用，可以修改元素
    let mut numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\n原始数字: {:?}", numbers); // 原始数字: [1, 2, 3, 4, 5]

    // 获取索引 2 的可变引用并修改
    if let Some(num) = numbers.get_mut(2) {
        *num *= 10; // 把第三个元素乘以 10
    }
    println!("修改后: {:?}", numbers); // 修改后: [1, 2, 30, 4, 5]

    // 批量修改偶数位置的元素
    for i in 0..numbers.len() {
        if i % 2 == 0 {
            if let Some(num) = numbers.get_mut(i) {
                *num += 100; // 偶数索引的元素加 100
            }
        }
    }
    println!("偶数索引+100后: {:?}", numbers); // 偶数索引+100后: [101, 2, 30, 4, 105]

    // 安全的遍历修改
    let mut temperatures: Vec<f64> = vec![22.5, 18.0, 25.3, 19.8, 21.0];
    println!("\n温度记录: {:?}", temperatures);
    // 温度记录: [22.5, 18.0, 25.3, 19.8, 21.0]

    for temp in temperatures.iter_mut() {
        // 将摄氏度转换为华氏度
        *temp = *temp * 9.0 / 5.0 + 32.0;
    }
    println!("转换为华氏度: {:?}", temperatures);
    // 转换为华氏度: [72.5, 64.4, 77.54, 67.64, 69.8]

    // get 和 get_mut 的使用场景：
    // 1. 不确定索引是否有效时
    // 2. 需要在索引无效时做特殊处理时
    // 3. 在循环中安全地访问可能不存在的元素时

    // 例子：查找元素并返回前后元素
    let data: Vec<i32> = vec![10, 20, 30, 40, 50];
    let target_index = 3;

    println!("\n查找目标索引 {} 的上下文", target_index);
    // 使用 get 安全地获取前一个、当前、后一个元素
    if let Some(prev) = data.get(target_index.wrapping_sub(1)) {
        println!("前一个元素: {}", prev); // 前一个元素: 30
    }

    if let Some(current) = data.get(target_index) {
        println!("当前元素: {}", current); // 当前元素: 40
    }

    if let Some(next) = data.get(target_index.saturating_add(1)) {
        println!("后一个元素: {}", next); // 后一个元素: 50
    }

    // 使用 saturating_add 而不是直接 +1，是因为如果 target_index 已经是 usize::MAX，
    // 直接 +1 会溢出，而 saturating_add 会返回 usize::MAX
}
```

get 和 get_mut 是 Rust 推崇的"安全优先"哲学的体现。在很多其他编程语言中，访问一个越界的数组索引可能会导致未定义行为（Undefined Behavior），比如 C 和 C++ 中可能会访问到不该访问的内存，引发各种奇怪的 bug。而在 Rust 中，get 方法通过返回 Option 类型强制你处理越界的情况，让你的代码更加健壮。

#### 6.1.2.6 [] 下标访问

除了 get 方法，Vec 还支持直接使用下标语法 `vec[index]` 来访问元素。这种方式简洁直观，就像在 Python 或 JavaScript 中访问数组一样。但是，这里有一个重要的区别——如果你访问了一个无效的索引，Rust 会毫不客气地触发 panic，而不是温柔地返回 None。

```rust
fn main() {
    let mut scores: Vec<u32> = vec![95, 87, 92, 78, 88];
    println!("分数列表: {:?}", scores); // 分数列表: [95, 87, 92, 78, 88]

    // 直接使用下标访问元素
    let first_score = scores[0];
    println!("第一个分数: {}", first_score); // 第一个分数: 95

    let last_score = scores[scores.len() - 1];
    println!("最后一个分数: {}", last_score); // 最后一个分数: 88

    // 修改元素 - 需要可变借用
    scores[1] = 90;
    println!("修改第二个分数后: {:?}", scores); // 修改第二个分数后: [95, 90, 92, 78, 88]

    // scores[100] = 0; // 危险！这会 panic!
    // thread 'main' panicked at 'index out of bounds: the len is 5 but the index is 100'

    // 使用下标的正确姿势：
    // 1. 你确定索引肯定有效（很少推荐）
    // 2. 在安全的循环中使用
    let mut inventory: Vec<&str> = vec!["sword", "shield", "potion", "key"];
    println!("\n背包物品: {:?}", inventory); // 背包物品: ["sword", "shield", "potion", "key"]

    // 在 for 循环中使用下标是安全的，因为你控制了索引范围
    for i in 0..inventory.len() {
        println!("物品 #{}: {}", i, inventory[i]);
    }
    // 物品 #0: sword
    // 物品 #1: shield
    // 物品 #2: potion
    // 物品 #3: key

    // 使用下标访问嵌套的 Vec
    let mut matrix: Vec<Vec<i32>> = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    println!("\n矩阵: {:?}", matrix); // 矩阵: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    // 访问矩阵元素
    let element = matrix[1][2]; // 第二行第三列
    println!("matrix[1][2] = {}", element); // matrix[1][2] = 6

    // 修改矩阵元素
    matrix[2][0] = 99;
    println!("修改后 matrix[2][0] = {}", matrix[2][0]); // 修改后 matrix[2][0] = 99
    println!("修改后矩阵: {:?}", matrix); // 修改后矩阵: [[1, 2, 3], [4, 5, 6], [99, 8, 9]]

    // [] 索引语法的实现原理
    // Vec 实现了 Index trait，允许使用 [] 语法
    // 实际上调用的是 index(&self, index: usize) -> &T
    // 如果越界，会调用 index_panic() 触发 panic

    // Vec 的下标访问返回的是 &T（不可变引用），
    // 如果你需要可变引用，使用 &mut vec[index]
    let mut grades: Vec<i32> = vec![85, 92, 78];
    let grade_ref: &i32 = &grades[0]; // 获取不可变引用
    println!("第一个成绩: {}", grade_ref); // 第一个成绩: 85

    let grade_mut_ref: &mut i32 = &mut grades[0]; // 获取可变引用
    *grade_mut_ref = 95; // 修改它
    println!("修改后第一个成绩: {}", grades[0]); // 修改后第一个成绩: 95

    // [] vs get() 的选择：
    // - 当你确定索引不会越界，且性能至关重要时，用 []
    // - 当你不确定索引是否有效，或需要优雅处理越界时，用 get()
    // - 实际应用中，建议优先使用 get()，除非你已经在代码中证明索引是安全的
}
```

下标访问 `[]` 是 Vec 实现的 Index trait 的语法糖。这种方式简洁高效，是很多程序员的最爱。但正所谓"能力越大，责任越大"，使用下标访问时，你需要确保你的索引在有效范围内。否则，Rust 会用 panic 的方式告诉你："嘿，你越界了！"这是一种"快速失败"的设计哲学——宁可程序崩溃，也不能让你继续运行在一个未定义的状态下，导致更难追踪的 bug。

### 6.1.3 切片操作

切片（Slice）是 Rust 中一个非常重要的概念。切片是对 Vec（或其他序列类型，如数组、字符串等）的一部分数据的引用。切片本身不拥有数据，它只是指向原始数据的一个"视图"（view）。这种设计非常优雅——你可以在不复制数据的情况下，操作一个大型数据结构的一部分。

想象一下，你有一整栋楼的钥匙（这就是 Vec），但现在你只需要某一层楼的钥匙（这就是切片）。切片告诉你"从第3层到第7层"，你就有了访问那些楼层的权限，而不需要复制任何东西。这种"引用而不是复制"的思想贯穿整个 Rust 的设计。

#### 6.1.3.1 &vec[start..end] 切片

切片语法 `&vec[start..end]` 创建了一个从 start 索引（包含）到 end 索引（不包含）的引用。这就是 Rust 的半开区间（half-open interval）约定——包括了起始点，但不包括结束点。这种设计可以避免很多边界错误：两个相邻的切片 `[0..2]` 和 `[2..4]` 完美衔接，不会遗漏也不会重复任何元素。

```rust
fn main() {
    let numbers: Vec<i32> = vec![0, 10, 20, 30, 40, 50, 60, 70, 80, 90];
    println!("完整数组: {:?}", numbers); // 完整数组: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    // 基本切片语法：&vec[start..end]
    // 记住这是半开区间：[start, end)，包含 start，不包含 end
    let slice_1_to_4 = &numbers[1..4];
    println!("numbers[1..4] = {:?}", slice_1_to_4); // numbers[1..4] = [10, 20, 30]

    // 从开头开始
    let slice_0_to_3 = &numbers[..3];
    println!("numbers[..3] = {:?}", slice_0_to_3); // numbers[..3] = [0, 10, 20]

    // 到末尾结束
    let slice_7_to_end = &numbers[7..];
    println!("numbers[7..] = {:?}", slice_7_to_end); // numbers[7..] = [70, 80, 90]

    // 整个 Vec 的切片
    let slice_all = &numbers[..];
    println!("numbers[..] = {:?}", slice_all); // numbers[..] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    // 切片的长度
    println!("slice_1_to_4 的长度 = {}", slice_1_to_4.len()); // slice_1_to_4 的长度 = 3

    // 切片的 is_empty
    println!("slice_all.is_empty() = {}", slice_all.is_empty()); // slice_all.is_empty() = false

    // 切片不复制数据——它们只是引用
    // 下面我们验证这一点
    let original_ptr = numbers.as_ptr(); // 获取 Vec 的原始指针
    let slice_ptr = slice_1_to_4.as_ptr(); // 获取切片的指针

    // 指针地址应该相同（或者至少指向同一个内存区域）
    unsafe {
        println!("Vec 首元素地址: {:?}", original_ptr);
        println!("切片首元素地址: {:?}", slice_ptr);
        println!("地址偏移验证: 切片应该从索引1开始，所以地址应该偏移 1 * size_of::<i32>() = {} 字节",
                 std::mem::size_of::<i32>());
    }

    // 修改切片指向的数据（通过可变借用）
    let mut data: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\n原始数据: {:?}", data); // 原始数据: [1, 2, 3, 4, 5]

    {
        // 获取一个可变切片
        let slice_mut = &mut data[1..4];
        println!("可变切片 data[1..4]: {:?}", slice_mut); // 可变切片 data[1..4]: [2, 3, 4]

        // 修改切片中的元素
        slice_mut[0] = 20;
        slice_mut[1] = 30;
        slice_mut[2] = 40;
    } // slice_mut 在这里离开作用域

    println!("修改后 data: {:?}", data); // 修改后 data: [1, 20, 30, 40, 5]
    // 注意：原始 Vec 的元素被修改了！

    // 切片的实际应用：处理字符串
    let message: String = String::from("Hello, Rust Programming!");
    println!("\n原始消息: {}", message); // 原始消息: Hello, Rust Programming!

    // 获取字符串的切片
    let hello = &message[0..5];
    println!("前5个字符: {}", hello); // 前5个字符: Hello

    let rust = &message[7..11];
    println!("'Rust' 出现的位置: {}", rust); // 'Rust' 出现的位置: Rust

    // 注意：中文字符不能简单用字节切片处理，这里只是演示概念
    let chinese: String = String::from("你好，世界");
    // &chinese[0..3] // 如果取消注释，可能只拿到半个中文字符，导致 panic!
    // 正确的做法是按字符索引：&chinese[..3] 尝试按字节切，可能出问题
    // 对于 Unicode，最好使用 chars() 方法

    // 切片的借用规则
    let values: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\nvalues: {:?}", values); // values: [1, 2, 3, 4, 5]

    let first_three = &values[..3];
    println!("前三个元素: {:?}", first_three); // 前三个元素: [1, 2, 3]

    // 在创建不可变切片后，可以继续创建其他不可变切片
    let last_two = &values[3..];
    println!("后两个元素: {:?}", last_two); // 后两个元素: [4, 5]

    // 但是注意借用规则！
    // let mutable_slice = &mut values[0..2]; // 这会报错，因为已经存在不可变借用
    // error: cannot borrow `values` as mutable because it is also borrowed as immutable

    // 验证切片的内存共享
    println!("\n验证切片内存共享:");
    let vec_of_strings: Vec<String> = vec![
        String::from("one"),
        String::from("two"),
        String::from("three"),
        String::from("four"),
    ];
    let slice_strings = &vec_of_strings[1..3];
    println!("原始 Vec: {:?}", vec_of_strings); // 原始 Vec: ["one", "two", "three", "four"]
    println!("切片 [1..3]: {:?}", slice_strings); // 切片 [1..3]: ["two", "three"]
    // 注意：切片中的元素是借用的引用，而不是新的 String
}
```

切片是 Rust 中非常强大的特性。它允许你以零成本（no-cost abstraction）的方式操作数据集合的一部分。切片不复制任何数据——它们只是创建了一个指向原始 Vec 的某个片段的引用。这意味着你可以在 O(1) 的时间内创建任意数量的切片，而不管原始 Vec 有多大。这对于处理大型数据集、字符串解析、网络协议解析等场景来说，是非常高效的。

#### 6.1.3.2 Vec<T> → &[T]

在 Rust 中，Vec<T> 可以隐式地转换为切片 `&[T]`。这种转换是"免费"的（零成本抽象），因为 Vec 在内存中的布局和切片完全兼容——它们都是一块连续的数据加上一个长度。Vec 实现了 `Deref<Target = [T]>` trait，这意味着你可以在需要 `&[T]` 的地方直接传一个 `&Vec<T>`，Rust 会自动帮你解引用。

```rust
fn main() {
    let numbers: Vec<i32> = vec![10, 20, 30, 40, 50];

    // Vec<T> 可以直接传给需要 &[T] 的函数
    // 这行代码展示了 Vec 到切片的隐式转换
    print_slice(&numbers); // 这里的 &numbers 会被自动转换为 &[i32]

    // 或者显式地创建切片
    let slice: &[i32] = &numbers[..];
    print_slice(slice);

    // Vec::as_slice() 方法返回一个完整的切片引用
    let full_slice = numbers.as_slice();
    print_slice(full_slice);

    // Vec::as_mut_slice() 返回可变切片
    let mut mutable_numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
    {
        let slice_mut: &mut [i32] = mutable_numbers.as_mut_slice();
        for i in 0..slice_mut.len() {
            slice_mut[i] *= 2;
        }
    }
    println!("\n翻倍后的 mutable_numbers: {:?}", mutable_numbers);
    // 翻倍后的 mutable_numbers: [2, 4, 6, 8, 10]

    // 利用自动解引用，直接传递 Vec 给需要切片的函数
    let data: Vec<i32> = vec![5, 10, 15, 20, 25];
    let sum = sum_of_slice(&data); // 这里 Vec 被自动转换为 &[i32]
    println!("\ndata = {:?}, sum = {}", data, sum); // data = [5, 10, 15, 20, 25], sum = 75

    // 切片方法的威力：可以直接在 Vec 上调用 slice 的方法
    // 因为 Deref 强制转换，Vec 可以使用切片的所有方法
    let scores: Vec<u32> = vec![85, 92, 78, 95, 88, 73, 90];
    println!("\n所有分数: {:?}", scores); // 所有分数: [85, 92, 78, 95, 88, 73, 90]

    // 切片方法
    println!("第一个和最后一个: {}, {}", scores.first().unwrap(), scores.last().unwrap());
    // 第一个和最后一个: 85, 90

    println!("包含 100 吗? {}", scores.contains(&100)); // 包含 100 吗? false
    println!("最大值: {}，最小值: {}", scores.iter().max().unwrap(), scores.iter().min().unwrap());
    // 最大值: 95，最小值: 73

    println!("前3个: {:?}", &scores[..3]); // 前3个: [85, 92, 78]
    println!("后3个: {:?}", &scores[scores.len()-3..]); // 后3个: [88, 73, 90]

    // binary_search 是切片提供的强大功能
    let sorted_scores: Vec<u32> = vec![60, 70, 75, 80, 85, 90, 95, 100];
    println!("\n排序后的分数: {:?}", sorted_scores);
    match sorted_scores.binary_search(&85) {
        Ok(index) => println!("找到 85 在索引 {}", index), // 找到 85 在索引 4
        Err(_) => println!("没找到 85"),
    }

    match sorted_scores.binary_search(&82) {
        Ok(index) => println!("找到 82 在索引 {}", index),
        Err(insert_pos) => println!("没找到 82，它应该插入在索引 {}", insert_pos),
        // 没找到 82，它应该插入在索引 4
    }

    // split_at 将 Vec 切分为两个切片
    let colors: Vec<&str> = vec!["red", "green", "blue", "yellow", "purple"];
    let (primary, secondary) = ( &colors[..3], &colors[3..]);
    println!("三原色: {:?}", primary); // 三原色: ["red", "green", "blue"]
    println!("其他颜色: {:?}", secondary); // 其他颜色: ["yellow", "purple"]
}

// 这个函数接受一个切片引用，而不是 Vec
fn print_slice(slice: &[i32]) {
    println!("切片内容: {:?}", slice);
}

// 计算切片所有元素的和
fn sum_of_slice(slice: &[i32]) -> i32 {
    slice.iter().sum()
}
```

Vec<T> 到 `&[T]` 的转换是 Rust 零成本抽象的完美体现。由于 Vec 实现了 Deref trait，指向 Vec 的引用在需要时会自动转换为指向其内部数组的切片引用。这意味着你可以编写一个函数，接受 `&[T]` 类型的参数，然后随意传递 Vec、数组、甚至是另一个切片给它——函数不需要关心你传的是什么具体类型，它只需要一块连续的数据和长度就够了。

这种设计哲学在 Rust 的标准库中随处可见。比如，一个接受 `&str` 的函数可以同时接受 String 和 &str；一个接受 `&[T]` 的函数可以同时接受 Vec<T>、&[T]、和 [T; N]。这就是 Rust 的"组合优于继承"设计——通过 trait 和 Deref，而不是类的继承层次，来实现类型之间的可替代性。

### 6.1.4 容量与重新分配

Vec 的容量（capacity）和长度（length）是两个容易混淆但非常重要的概念。长度是你实际存储了多少元素，而容量是 Vec 已经为未来存储更多元素预留了多少空间。理解这两个概念的区别，以及 Rust 何时会触发重新分配，对于编写高效的 Rust 代码至关重要。

#### 6.1.4.1 capacity / len / is_empty

这三个方法是查看 Vec 状态的"三剑客"。capacity 返回 Vec 的总容量，len 返回当前元素的数量，is_empty 则是一个布尔值，告诉你 Vec 是否为空。它们就像是检查一个容器的"已用空间"、"总空间"和"是否空的"。

```rust
fn main() {
    // 创建一个空的 Vec
    let empty: Vec<i32> = Vec::new();
    println!("空 Vec:");
    println!("  长度 (len): {}", empty.len()); // 长度 (len): 0
    println!("  容量 (capacity): {}", empty.capacity()); // 容量 (capacity): 0
    println!("  是否为空 (is_empty): {}", empty.is_empty()); // 是否为空 (is_empty): true

    // 创建一个有预分配容量的 Vec
    let with_capacity: Vec<i32> = Vec::with_capacity(10);
    println!("\n预分配容量10的 Vec:");
    println!("  长度 (len): {}", with_capacity.len()); // 长度 (len): 0
    println!("  容量 (capacity): {}", with_capacity.capacity()); // 容量 (capacity): 10
    println!("  是否为空 (is_empty): {}", with_capacity.is_empty()); // 是否为空 (is_empty): true

    // 使用 vec![] 宏创建 Vec
    let initialized: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\n初始化了5个元素的 Vec:");
    println!("  长度 (len): {}", initialized.len()); // 长度 (len): 5
    println!("  容量 (capacity): {}", initialized.capacity()); // 容量 (capacity): 5
    println!("  是否为空 (is_empty): {}", initialized.is_empty()); // 是否为空 (is_empty): false

    // 演示 len 和 capacity 的关系
    let mut growing: Vec<i32> = Vec::with_capacity(3);
    println!("\n容量变化演示:");
    println!("  初始状态 - len: {}, capacity: {}", growing.len(), growing.capacity());
    // 初始状态 - len: 0, capacity: 3

    growing.push(1);
    println!("  push 1 后 - len: {}, capacity: {}", growing.len(), growing.capacity());
    // push 1 后 - len: 1, capacity: 3

    growing.push(2);
    println!("  push 2 后 - len: {}, capacity: {}", growing.len(), growing.capacity());
    // push 2 后 - len: 2, capacity: 3

    growing.push(3);
    println!("  push 3 后 - len: {}, capacity: {}", growing.len(), growing.capacity());
    // push 3 后 - len: 3, capacity: 3

    // 现在 Vec 已经满了，再添加元素会触发扩容
    growing.push(4);
    println!("  push 4 后（触发扩容）- len: {}, capacity: {}", growing.len(), growing.capacity());
    // push 4 后（触发扩容）- len: 4, capacity: 6 (或者更大的值)

    // is_empty 的典型用法
    let mut stack: Vec<char> = Vec::new();
    println!("\n栈操作演示:");

    // 栈为空时的处理
    if stack.is_empty() {
        println!("  栈是空的，不能 pop！");
    } else {
        println!("  栈顶元素: {:?}", stack.last());
    }

    stack.push('A');
    stack.push('B');
    stack.push('C');

    // 栈非空时的处理
    while !stack.is_empty() {
        print!("  pop: {:?}, 剩余: {:?} -> ", stack.pop(), stack);
    }
    println!("(栈已空)");
    // pop: Some('C'), 剩余: ['A', 'B'] -> pop: Some('B'), 剩余: ['A'] -> pop: Some('A'), 剩余: [] -> (栈已空)

    // 深入理解 len vs capacity
    let mut data: Vec<u8> = Vec::with_capacity(8);
    println!("\nlen vs capacity 深入理解:");
    println!("  开始时 - len: {}, capacity: {}", data.len(), data.capacity());
    // 开始时 - len: 0, capacity: 8

    for i in 0..8 {
        data.push(i);
        println!("  push {} 后 - len: {}, capacity: {}", i, data.len(), data.capacity());
    }
    // push 0 后 - len: 1, capacity: 8
    // push 1 后 - len: 2, capacity: 8
    // ... 以此类推
    // push 7 后 - len: 8, capacity: 8

    println!("  当前 len == capacity: {}", data.len() == data.capacity());
    // 当前 len == capacity: true

    // 再 push 一个元素
    data.push(8);
    println!("  push 8（扩容）后 - len: {}, capacity: {}", data.len(), data.capacity());
    // push 8（扩容）后 - len: 9, capacity: 16 (典型策略)
}
```

理解 len 和 capacity 的区别是掌握 Vec 行为的关键。capacity 就像是你租的仓库的总面积，而 len 是你实际存放的货物占用的面积。你可以免费使用已经租下的仓库的每一寸空间，但当你需要存放更多货物时，你可能需要租一个更大的仓库——这会涉及到搬家（重新分配）的成本。

#### 6.1.4.2 容量翻倍策略

当 Vec 的容量不够用时，它需要重新分配一块更大的内存。Rust 的 Vec 实现使用了一种"容量翻倍"的策略——当容量不足时，新的容量会是旧容量的两倍（或者略大于两倍，取决于实现细节）。这种策略确保了均摊后每次 push 的时间复杂度是 O(1)。

```rust
fn main() {
    // 观察容量翻倍的策略
    let mut capacities: Vec<usize> = Vec::with_capacity(1);
    let initial_capacity = 1;
    capacities.push(initial_capacity);

    println!("容量增长策略演示:");
    println!("  初始容量: {}", initial_capacity);

    let mut prev_capacity = initial_capacity;
    for i in 0..15 {
        if capacities.len() == capacities.capacity() {
            capacities.push(prev_capacity * 2);
            println!("  扩容 {} -> {}", prev_capacity, capacities.capacity());
            prev_capacity = capacities.capacity();
        }

        // 添加足够多元素触发多次扩容
        let mut v: Vec<usize> = Vec::with_capacity(prev_capacity);
        for j in 0..=prev_capacity {
            if v.len() == v.capacity() {
                v.push(j);
            }
        }
    }

    // 实际演示容量变化
    println!("\n实际容量变化:");
    let mut vec: Vec<i32> = Vec::with_capacity(1);
    println!("初始: len={}, capacity={}", vec.len(), vec.capacity());
    // 初始: len=0, capacity=1

    vec.push(1);
    println!("push 1: len={}, capacity={}", vec.len(), vec.capacity());
    // push 1: len=1, capacity=1

    vec.push(2);
    println!("push 2: len={}, capacity={}", vec.len(), vec.capacity());
    // push 2: len=2, capacity=2 (扩容!)

    vec.push(3);
    println!("push 3: len={}, capacity={}", vec.len(), vec.capacity());
    // push 3: len=3, capacity=4 (扩容!)

    vec.push(4);
    println!("push 4: len={}, capacity={}", vec.len(), vec.capacity());
    // push 4: len=4, capacity=4

    vec.push(5);
    println!("push 5: len={}, capacity={}", vec.len(), vec.capacity());
    // push 5: len=5, capacity=8 (扩容!)

    // 容量翻倍策略的优势：均摊 O(1) 复杂度
    // 考虑 push n 个元素的场景：
    // - 如果每次都只扩容 1，需要 1+2+3+...+n = O(n²) 次内存操作
    // - 如果每次都翻倍，需要最多 log(n) 次扩容，均摊下来每次 push 是 O(1)

    println!("\n均摊复杂度分析:");
    let n = 1000000;
    let mut total_allocations = 0;
    let mut vec: Vec<i32> = Vec::with_capacity(1);
    total_allocations += 1; // 初始分配

    for i in 0..n {
        if vec.len() == vec.capacity() {
            // 模拟扩容
            total_allocations += 1;
        }
        vec.push(i);
    }

    println!("  push {} 个元素总共分配了 {} 次内存", n, total_allocations);
    println!("  平均每次 push 需要的分配次数: {:.6}", total_allocations as f64 / n as f64);
    // 平均每次 push 需要的分配次数: 约 0.000001 (即 1000000 次 push 只分配了约 20 次)

    // 对比：如果每次只扩容 1
    let mut naive_allocations = 0;
    let mut naive_vec: Vec<i32> = Vec::new();

    for i in 0..n {
        naive_vec.push(i);
        // 每次容量不足时扩容 1
        if naive_vec.len() > naive_vec.capacity() {
            naive_allocations += 1;
        }
    }
    println!("  如果每次只扩容 1，分配次数: {} (大约是 n*(n+1)/2 次，总共约 {} 字节移动)",
             naive_allocations, n * n / 2);
}
```

容量翻倍策略是计算机科学中"均摊分析"的经典案例。虽然偶尔会有一次昂贵的扩容操作（比如从 8192 扩容到 16384，需要移动 8192 个元素），但这种扩容发生的频率越来越低。总体来看，无论你往 Vec 中添加多少元素，每次 push 的均摊成本都是常数级别的。

这种策略的数学原理很有意思：如果你的 Vec 当前容量是 C，当你 push 到容量满的时候，它会扩容到 2C。下一次扩容会在你 push 了 C 个元素之后发生，然后又可以用 C 次 push。然后再次扩容到 4C，以此类推。所以添加 n 个元素的总成本是：C + C + C + C + ... （log(n) 次），也就是 O(n)。

#### 6.1.4.3 shrink_to / shrink_to_fit

有时候你的 Vec 可能预分配了很大的容量，但实际只使用了一小部分。这时候你可能想要释放多余的容量，节省内存。shrink_to 和 shrink_to_fit 就是用来做这件事的。

```rust
fn main() {
    // 预分配一个大容量
    let mut large_vec: Vec<i32> = Vec::with_capacity(10000);
    println!("初始预分配:");
    println!("  len: {}, capacity: {}", large_vec.len(), large_vec.capacity());
    // 初始预分配: len: 0, capacity: 10000

    // 只添加少量元素
    for i in 0..100 {
        large_vec.push(i);
    }
    println!("\n添加100个元素后:");
    println!("  len: {}, capacity: {}", large_vec.len(), large_vec.capacity());
    // 添加100个元素后: len: 100, capacity: 10000

    // shrink_to_fit 尝试释放多余的容量
    large_vec.shrink_to_fit();
    println!("\nshrink_to_fit() 后:");
    println!("  len: {}, capacity: {}", large_vec.len(), large_vec.capacity());
    // shrink_to_fit() 后: len: 100, capacity: 100 (或者略大)

    // shrink_to 可以指定一个最小容量
    let mut vec: Vec<i32> = (0..1000).collect();
    println!("\n收集1000个元素后:");
    println!("  len: {}, capacity: {}", vec.len(), vec.capacity());
    // 收集1000个元素后: len: 1000, capacity: 1000

    // 使用 shrink_to 保留至少 500 的容量
    vec.shrink_to(500);
    println!("\nshrink_to(500) 后:");
    println!("  len: {}, capacity: {}", vec.len(), vec.capacity());
    // shrink_to(500) 后: len: 1000, capacity: 1000
    // 注意：如果 len < shrink_to 的参数，容量不会减少到 len 以下

    // 模拟一个真实的场景：读取文件内容
    println!("\n场景：读取文件前100行");
    let mut lines: Vec<String> = Vec::with_capacity(10000); // 假设文件可能有10000行

    // 模拟读取文件（实际只有100行）
    for i in 0..100 {
        lines.push(format!("这是第 {} 行内容", i + 1));
    }

    println!("读取完成:");
    println!("  实际行数: {}", lines.len()); // 实际行数: 100
    println!("  预分配容量: {}", 10000);

    // 处理完后释放多余的容量
    lines.shrink_to_fit();
    println!("释放多余容量后:");
    println!("  实际行数: {}", lines.len()); // 实际行数: 100
    println!("  当前容量: {}", lines.capacity()); // 当前容量: 100 (或略大)

    // shrink_to 的实际用途：当你知道最小需要多少容量时
    let mut buffer: Vec<u8> = Vec::with_capacity(1024);
    // 假设我们知道数据不会超过 256 字节
    buffer.extend_from_slice(&[1, 2, 3, 4, 5]);
    buffer.shrink_to(256); // 保留 256 的最小容量，即使我们只用了 5 字节
    println!("\nbuffer len: {}, capacity: {}", buffer.len(), buffer.capacity());
    // buffer len: 5, capacity: 256

    // 注意事项：shrink_to_fit 可能不会释放所有多余的容量
    // 具体行为取决于 Rust 的实现和内存分配器
    // 另外，调用 shrink_to_fit 可能会导致一次内存重新分配（复制数据）
    // 所以如果你还会继续添加大量元素，可能不值得 shrink_to_fit
}
```

shrink_to 和 shrink_to_fit 是手动内存管理的工具。在大多数情况下，你不需要手动调用它们，因为 Rust 的内存分配器会自动管理内存。但是，在某些特殊场景下，比如你的程序在处理完一个大数据块后需要长期运行，或者你需要在内存受限的环境中运行程序，手动释放多余的容量可能会带来显著的内存节省。

#### 6.1.4.4 reserve / reserve_exact

reserve 和 reserve_exact 允许你主动增加 Vec 的容量，而不需要添加任何元素。这在你知道即将要添加大量元素，但想避免多次扩容的开销时非常有用。

```rust
fn main() {
    // 创建一个空的 Vec
    let mut vec: Vec<i32> = Vec::new();
    println!("初始状态:");
    println!("  len: {}, capacity: {}", vec.len(), vec.capacity());
    // 初始状态: len: 0, capacity: 0

    // 预留 1000 个元素的容量
    vec.reserve(1000);
    println!("\nreserve(1000) 后:");
    println!("  len: {}, capacity: {}", vec.len(), vec.capacity());
    // reserve(1000) 后: len: 0, capacity: 1000

    // 现在可以快速添加元素，不会触发扩容
    for i in 0..1000 {
        vec.push(i);
    }
    println!("\n添加1000个元素后:");
    println!("  len: {}, capacity: {}", vec.len(), vec.capacity());
    // 添加1000个元素后: len: 1000, capacity: 1000

    // reserve_exact 确保精确的容量，不多也不少
    let mut exact_vec: Vec<i32> = Vec::new();
    exact_vec.reserve_exact(100);
    println!("\nreserve_exact(100) 后:");
    println!("  len: {}, capacity: {}", exact_vec.len(), exact_vec.capacity());
    // reserve_exact(100) 后: len: 0, capacity: 100

    // 实际应用场景：读取并处理 CSV 文件
    println!("\n场景：处理 CSV 文件");
    struct Record {
        id: u32,
        name: String,
        value: f64,
    }

    // 假设 CSV 文件有 10000 行
    let csv_line_count = 10000;
    let mut records: Vec<Record> = Vec::with_capacity(csv_line_count);

    // 模拟读取 CSV
    for i in 0..csv_line_count {
        records.push(Record {
            id: i,
            name: format!("Record_{}", i),
            value: i as f64 * 1.5,
        });
    }

    println!("读取了 {} 条记录", records.len());
    println!("预分配的容量: {}", csv_line_count);
    println!("实际使用的容量: {}", records.capacity());

    // 场景2：分批处理数据
    println!("\n场景：分批处理数据");
    let mut batch_vec: Vec<i32> = Vec::new();

    // 每批处理 1000 个元素
    let batch_size = 1000;
    let total_items = 5500; // 总共需要处理 5500 个

    // 处理第一批
    batch_vec.reserve(batch_size);
    for i in 0..1000 {
        batch_vec.push(i);
    }
    println!("第一批完成: len={}, capacity={}", batch_vec.len(), batch_vec.capacity());
    // 第一批完成: len=1000, capacity=1000

    // 处理完后清空（但保持容量）
    batch_vec.clear();
    println!("清空后: len={}, capacity={}", batch_vec.len(), batch_vec.capacity());
    // 清空后: len=0, capacity=1000

    // 预留更多空间为下一批做准备
    batch_vec.reserve(batch_size);
    println!("再预留后: len={}, capacity={}", batch_vec.len(), batch_vec.capacity());
    // 再预留后: len=0, capacity=1000

    // reserve 和 capacity 的关系
    let mut v: Vec<i32> = vec![1, 2, 3];
    println!("\n容量关系演示:");
    println!("  vec![1,2,3]: len={}, capacity={}", v.len(), v.capacity());
    // vec![1,2,3]: len=3, capacity=3

    v.reserve(10); // 请求至少 10 的额外空间
    println!("  reserve(10) 后: len={}, capacity={}", v.len(), v.capacity());
    // reserve(10) 后: len=3, capacity=13 (3 + 10)

    v.reserve(100); // 请求至少 100 的额外空间
    println!("  reserve(100) 后: len={}, capacity={}", v.len(), v.capacity());
    // reserve(100) 后: len=3, capacity=103

    // reserve_exact 更加精确
    let mut exact: Vec<i32> = vec![1, 2, 3];
    println!("\nreserve_exact 演示:");
    println!("  vec![1,2,3]: len={}, capacity={}", exact.len(), exact.capacity());
    // vec![1,2,3]: len=3, capacity=3

    exact.reserve_exact(10); // 精确请求 10 的额外空间
    println!("  reserve_exact(10) 后: len={}, capacity={}", exact.len(), exact.capacity());
    // reserve_exact(10) 后: len=3, capacity=13

    // 注意：如果当前容量已经 >= len + additional，reserve 不会做任何事
    let mut small: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("\n无需扩容的情况:");
    println!("  当前: len={}, capacity={}", small.len(), small.capacity());
    // 当前: len=10, capacity=10

    small.reserve(5); // 需要 15，现在只有 10，不够
    println!("  reserve(5) 后: len={}, capacity={}", small.len(), small.capacity());
    // reserve(5) 后: len=10, capacity=15

    small.reserve(3); // 现在需要 13，已经有 15，够了
    println!("  reserve(3)（已满足）后: len={}, capacity={}", small.len(), small.capacity());
    // reserve(3)（已满足）后: len=10, capacity=15
}
```

reserve 和 reserve_exact 是性能优化的利器。如果你知道你要往 Vec 中添加多少元素，提前预留好空间可以避免多次内存重新分配的开销。唯一的区别是：reserve 可能会分配比请求的略多的空间（因为容量翻倍策略），而 reserve_exact 则会尽量精确地分配你请求的空间。在大多数情况下，reserve 是更好的选择，因为它给 Rust 更多优化内存分配的灵活性。

### 6.1.5 常用方法

除了 push、pop、insert、remove 这些基础操作，Vec 还提供了许多实用的高级方法。这些方法让你的代码更加简洁、表达力更强，也更符合 Rust 的惯用风格。让我来一一介绍这些"瑞士军刀"上的小工具。

#### 6.1.5.1 extend / append

extend 允许你一次性添加另一个可迭代对象的所有元素，而 append 则是将另一个 Vec 的全部元素移动（不是复制）到当前 Vec 的末尾。这两个方法在处理批量数据时非常有用。

```rust
fn main() {
    // extend: 扩展 Vec 的内容
    let mut numbers: Vec<i32> = vec![1, 2, 3];
    println!("extend 前: {:?}", numbers); // extend 前: [1, 2, 3]

    // 从一个迭代器 extend
    numbers.extend(4..=6);
    println!("extend(4..=6) 后: {:?}", numbers); // extend(4..=6) 后: [1, 2, 3, 4, 5, 6]

    // 从数组 extend
    let more_numbers = [7, 8, 9];
    numbers.extend(more_numbers);
    println!("extend([7,8,9]) 后: {:?}", numbers); // extend([7,8,9]) 后: [1, 2, 3, 4, 5, 6, 7, 8, 9]

    // 从另一个 Vec extend（引用）
    let extra: Vec<i32> = vec![10, 11, 12];
    numbers.extend(extra); // extra 的所有权会被移动（如果使用引用则不会）
    println!("extend(extra) 后: {:?}", numbers); // extend(extra) 后: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    // append: 将另一个 Vec 的元素移动到当前 Vec
    let mut first: Vec<i32> = vec![1, 2, 3];
    let mut second: Vec<i32> = vec![4, 5, 6];
    println!("\nappend 前:");
    println!("  first: {:?}", first); // first: [1, 2, 3]
    println!("  second: {:?}", second); // second: [4, 5, 6]

    first.append(&mut second);
    println!("\nfirst.append(&mut second) 后:");
    println!("  first: {:?}", first); // first: [1, 2, 3, 4, 5, 6]
    println!("  second: {:?}", second); // second: [] (被清空了！)

    // extend 和 append 的区别：
    // - extend: 从任何可迭代对象添加元素，不获取所有权（对于迭代器）或获取所有权（对于 Vec）
    // - append: 只能从 Vec 获取元素，并且会把源 Vec 清空

    // 实际应用：合并多个数据源
    let mut combined: Vec<String> = Vec::new();
    let source1 = vec!["Apple".to_string(), "Banana".to_string()];
    let source2 = vec!["Cherry".to_string(), "Date".to_string()];
    let source3 = vec!["Elderberry".to_string()];

    combined.extend(source1); // source1 被移动
    combined.extend(source2); // source2 被移动
    combined.extend(source3); // source3 被移动

    println!("\n合并后的水果: {:?}", combined);
    // 合并后的水果: ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

    // 使用 extend_from_slice 作为 append 的替代
    let mut letters: Vec<char> = vec!['A', 'B', 'C'];
    let slice = ['D', 'E', 'F'];
    letters.extend_from_slice(&slice);
    println!("\nextend_from_slice 后: {:?}", letters); // extend_from_slice 后: ['A', 'B', 'C', 'D', 'E', 'F']

    // extend 的性能
    println!("\n性能考虑:");
    let mut v: Vec<i32> = Vec::with_capacity(10000);
    let start = std::time::Instant::now();

    // 方式1：逐个 push
    let mut v1: Vec<i32> = Vec::new();
    for i in 0..10000 {
        v1.push(i);
    }
    println!("逐个 push 耗时: {:?}", start.elapsed()); // 逐个 push 耗时: ~几十到几百微秒

    // 方式2：一次性 extend
    let start = std::time::Instant::now();
    let mut v2: Vec<i32> = Vec::new();
    v2.extend(0..10000);
    println!("extend 耗时: {:?}", start.elapsed()); // extend 耗时: ~几微秒

    // extend 通常比逐个 push 快，因为可以一次性分配足够的内存
}
```

extend 和 append 是处理批量数据的利器。extend 特别强大，因为它可以接受任何实现了 IntoIterator trait 的类型，包括数组、切片、Range、甚至是你自己创建的可迭代对象。而 append 则专门用于 Vec 之间的合并，它的特点是会"掏空"源 Vec——所有元素被移动走之后，源 Vec 会变成空的。

#### 6.1.5.2 split_at / split_at_mut

split_at 将一个 Vec（或者切片）在指定索引处切成两半，返回两个切片。而 split_at_mut 则返回两个可变切片，允许你同时修改这两部分。这两个方法在需要将数据分成两部分分别处理时非常有用。

```rust
fn main() {
    let data: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("原始数据: {:?}", data); // 原始数据: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    // split_at 在索引 5 处切开
    let (left, right) = data.split_at(5);
    println!("\nsplit_at(5):");
    println!("  left (索引 0-4): {:?}", left); // left (索引 0-4): [1, 2, 3, 4, 5]
    println!("  right (索引 5-9): {:?}", right); // right (索引 5-9): [6, 7, 8, 9, 10]

    // split_at_mut：可变版本，可以修改切分后的两部分
    let mut mutable_data: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    {
        let (evens, odds) = mutable_data.split_at_mut(5);
        println!("\nsplit_at_mut(5):");

        // 把偶数部分翻倍
        for num in evens.iter_mut() {
            *num *= 2;
        }
        println!("  evens 翻倍后: {:?}", evens); // evens 翻倍后: [2, 4, 6, 8, 10]

        // 把奇数部分加 10
        for num in odds.iter_mut() {
            *num += 10;
        }
        println!("  odds 加10后: {:?}", odds); // odds 加10后: [16, 17, 18, 19, 20]
    }
    println!("  整体结果: {:?}", mutable_data); // 整体结果: [2, 4, 6, 8, 10, 16, 17, 18, 19, 20]

    // split_at 的变体：split_at_unchecked（不安全版本）
    // 这个版本不做边界检查，如果你确定索引是安全的，可以使用它来获得一点性能提升
    // 但通常 split_at 就够了，因为它足够快

    // 实际应用：处理网络数据包
    println!("\n实际应用：解析网络数据包");
    struct Packet {
        header: [u8; 4],
        payload: Vec<u8>,
    }

    // 模拟一个数据包：前4字节是头部，后面是载荷
    let raw_packet: Vec<u8> = vec![
        0x01, 0x02, 0x03, 0x04, // 头部
        0xDE, 0xAD, 0xBE, 0xEF  // 载荷
    ];

    let (header_bytes, payload_bytes) = raw_packet.split_at(4);
    let header: [u8; 4] = [header_bytes[0], header_bytes[1], header_bytes[2], header_bytes[3]];
    println!("  解析出的头部: {:?}", header); // 解析出的头部: [1, 2, 3, 4]
    println!("  载荷: {:?}", payload_bytes); // 载荷: [222, 173, 190, 239]

    // 实际应用：并行处理数组的两半
    println!("\n并行处理示例（模拟）:");
    let mut large_array: Vec<i64> = (0..20).map(|i| i as i64).collect();
    println!("  处理前: {:?}", large_array);

    let mid = large_array.len() / 2;
    {
        let (first_half, second_half) = large_array.split_at_mut(mid);

        // 模拟并行处理：前半部分平方，后半部分立方
        for num in first_half.iter_mut() {
            *num = *num * *num;
        }

        for num in second_half.iter_mut() {
            *num = *num * *num * *num;
        }
    }
    println!("  处理后: {:?}", large_array);
    // 处理后: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 512, 1728, 4096, 8000, 15625, 27000, 46656, 68921, 110592, 175616]
    // 前10个: 0²,1²,2²...9²
    // 后10个: 10³,11³...19³

    // 另一个例子：安全的边界切分
    let small_vec: Vec<i32> = vec![1, 2];
    let (left, right) = small_vec.split_at(1);
    println!("\n切分 [1, 2] at 1:");
    println!("  left: {:?}", left); // left: [1]
    println!("  right: {:?}", right); // right: [2]

    // split_at 的 panic 情况
    // let (_left, _right) = small_vec.split_at(10); // panic! 索引越界
    // thread 'main' panicked at 'index out of bounds: the len is 2 but the index is 10'
}
```

split_at 和 split_at_mut 是那种看起来简单但实际非常强大的方法。它们在算法实现中经常出现——无论是并行计算、数据解析、还是需要将数据分成两部分分别处理，split_at 都是你的好帮手。唯一需要注意的是，split_at 会检查索引是否有效，如果越界会触发 panic，所以请确保你的索引在合理范围内。

#### 6.1.5.3 dedup / dedup_by

dedup（deduplicate）用于移除 Vec 中相邻的重复元素，只保留第一个。这在处理需要去重但又不能改变元素顺序的场景时非常有用。dedup_by 则允许你自定义比较规则来决定什么是"重复"。

```rust
fn main() {
    // dedup: 移除相邻的重复元素
    let mut data: Vec<i32> = vec![1, 1, 2, 2, 2, 3, 1, 1, 4, 4, 5];
    println!("dedup 前: {:?}", data); // dedup 前: [1, 1, 2, 2, 2, 3, 1, 1, 4, 4, 5]

    data.dedup();
    println!("dedup 后: {:?}", data); // dedup 后: [1, 2, 3, 1, 4, 5]

    // dedup 只移除相邻的重复，所以不相邻的相同元素会保留
    // 上面例子中，开头的 1,1 和中间的 1,1 分别被处理

    // dedup_by: 自定义去重规则
    let mut words: Vec<&str> = vec!["apple", "Apple", "apples", "banana", "BANANA", "banana"];
    println!("\ndedup_by 前: {:?}", words); // dedup_by 前: ["apple", "Apple", "apples", "banana", "BANANA", "banana"]

    // 使用不区分大小写的比较
    words.dedup_by(|a, b| a.to_lowercase() == b.to_lowercase());
    println!("dedup_by (不区分大小写) 后: {:?}", words);
    // dedup_by (不区分大小写) 后: ["apple", "apples", "banana"]

    // dedup_by 的另一个用途：自定义等价关系
    let mut numbers: Vec<i32> = vec![1, 2, 3, 6, 7, 8, 9, 10];
    println!("\ndedup_by 前: {:?}", numbers); // dedup_by 前: [1, 2, 3, 6, 7, 8, 9, 10]

    // 移除连续的递增序列中的多余元素（保留连续递增的部分）
    // 每次比较相邻两个元素：如果差值为 1，则后一个元素被移除
    // 结果：1 被保留，2, 3 因与前一个元素差值为 1 被移除
    //       6 被保留，7, 8, 9, 10 都因与前一个被移除元素差值为 1 被移除
    numbers.dedup_by(|a, b| b - a == 1); // 如果 b = a + 1，认为是"重复"
    println!("dedup_by (移除连续递增) 后: {:?}", numbers);
    // dedup_by (移除连续递增) 后: [1, 6]

    // 实际应用：处理用户输入
    println!("\n实际应用：处理用户输入");
    let mut user_inputs: Vec<String> = Vec::new();
    user_inputs.push(String::from("hello"));
    user_inputs.push(String::from("hello")); // 重复
    user_inputs.push(String::from("world"));
    user_inputs.push(String::from("world")); // 重复
    user_inputs.push(String::from("rust"));
    user_inputs.push(String::from("hello")); // 不相邻，可以保留

    println!("  原始输入: {:?}", user_inputs);
    user_inputs.dedup();
    println!("  去重后: {:?}", user_inputs);
    // 原始输入: ["hello", "hello", "world", "world", "rust", "hello"]
    // 去重后: ["hello", "world", "rust", "hello"]

    // 如果需要不区分顺序的去重，需要使用其他方法
    // 比如先排序再 dedup，或者使用 HashSet

    // dedup 的性能
    // dedup 是 O(n) 的时间复杂度，因为它需要移动剩余的元素
    // 但是它不需要额外的内存

    // dedup_by_mut 存在吗？是的，它是 dedup_by 的可变版本... 等等
    // 实际上 dedup_by 已经是可变的了，因为需要修改 Vec

    // 另一个例子：处理日志文件中的重复条目
    let mut log_entries: Vec<&str> = vec![
        "INFO: Server started",
        "INFO: Server started", // 重复
        "DEBUG: Loading config",
        "DEBUG: Loading config", // 重复
        "INFO: Connection accepted",
        "ERROR: Connection failed",
        "ERROR: Connection failed", // 重复
    ];

    println!("\n处理日志条目:");
    println!("  原始: {:?}", log_entries);
    log_entries.dedup();
    println!("  去重后: {:?}", log_entries);
    // 原始: ["INFO: Server started", "INFO: Server started", "DEBUG: Loading config", ...]
    // 去重后: ["INFO: Server started", "DEBUG: Loading config", "INFO: Connection accepted", "ERROR: Connection failed"]

    // dedup 要求 Vec 是可变的
    // 如果你有一个不可变的 Vec，你需要先变成可变的
    let immutable_data: Vec<i32> = vec![1, 1, 2, 2, 3, 3];
    let mut mutable_version = immutable_data;
    mutable_version.dedup();
    println!("\nimmutable 通过可变借用去重: {:?}", mutable_version);
    // immutable 通过可变借用去重: [1, 2, 3]
}
```

dedup 是一个非常实用的方法，尤其在处理用户输入、日志数据、网络消息等可能有重复的场景时。它的特点是只处理相邻的重复元素，这既是它的优势（不需要排序，保留原始顺序），也是它的限制（如果你需要完全去重，可能需要先排序或者使用 HashSet）。

#### 6.1.5.4 reverse / rotate

reverse 顾名思义，就是把 Vec 中的元素顺序完全颠倒。而 rotate 则是将 Vec 中的元素按照指定的索引进行"旋转"，有点像是把一个循环数组进行旋转操作。

```rust
fn main() {
    // reverse: 反转 Vec 的顺序
    let mut numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("原始: {:?}", numbers); // 原始: [1, 2, 3, 4, 5]

    numbers.reverse();
    println!("reverse 后: {:?}", numbers); // reverse 后: [5, 4, 3, 2, 1]

    // reverse 是 in-place 的，O(n) 时间复杂度，O(1) 空间复杂度

    // rotate: 旋转 Vec
    let mut data: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("\n原始: {:?}", data); // 原始: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    // rotate_left(3) 将元素向左旋转3位
    // 也就是索引 0,1,2 的元素会移到末尾
    data.rotate_left(3);
    println!("rotate_left(3) 后: {:?}", data); // rotate_left(3) 后: [4, 5, 6, 7, 8, 9, 10, 1, 2, 3]

    // rotate_right(2) 将元素向右旋转2位
    data.rotate_right(2);
    println!("rotate_right(2) 后: {:?}", data); // rotate_right(2) 后: [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]

    // 重新设置以便演示
    let mut example: Vec<char> = vec!['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    println!("\n原始字母: {:?}", example); // 原始字母: ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    example.rotate_left(2);
    println!("rotate_left(2) 后: {:?}", example);
    // rotate_left(2) 后: ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    // 'A', 'B' 被移到了末尾

    // 旋转的数学原理
    // rotate_left(k) 等价于：
    // 1. 把 Vec 分成 [0..k] 和 [k..len] 两部分
    // 2. 调换这两部分的顺序

    // rotate_left(0) 或 rotate_right(0) 不会改变任何东西
    let mut unchanged: Vec<i32> = vec![1, 2, 3, 4, 5];
    unchanged.rotate_left(0);
    println!("\nrotate_left(0) 后: {:?}", unchanged); // rotate_left(0) 后: [1, 2, 3, 4, 5]

    // 旋转一整圈会回到原始状态
    let mut original: Vec<i32> = vec![1, 2, 3, 4, 5];
    original.rotate_left(5); // 旋转的长度等于 Vec 的长度
    println!("rotate_left(5) 完整旋转后: {:?}", original); // rotate_left(5) 完整旋转后: [1, 2, 3, 4, 5]

    // 实际应用：实现循环缓冲区
    println!("\n实际应用：循环缓冲区");
    struct CircularBuffer<T> {
        data: Vec<T>,
        read_index: usize,
    }

    impl<T> CircularBuffer<T> {
        fn new() -> Self {
            CircularBuffer {
                data: Vec::new(),
                read_index: 0,
            }
        }

        fn push(&mut self, item: T) {
            self.data.push(item);
        }

        fn rotate(&mut self) {
            if !self.data.is_empty() {
                self.data.rotate_left(1);
            }
        }
    }

    let mut buffer = CircularBuffer::new();
    for i in 1..=5 {
        buffer.push(i);
    }
    println!("初始 buffer: {:?}", buffer.data); // 初始 buffer: [1, 2, 3, 4, 5]

    buffer.rotate();
    println!("旋转一次后: {:?}", buffer.data); // 旋转一次后: [2, 3, 4, 5, 1]

    buffer.rotate();
    println!("旋转两次后: {:?}", buffer.data); // 旋转两次后: [3, 4, 5, 1, 2]

    // 实际应用：处理音乐播放列表（循环播放）
    println!("\n音乐播放列表循环播放:");
    let mut playlist: Vec<&str> = vec!["Song A", "Song B", "Song C", "Song D"];
    println!("当前播放: {}", playlist[0]); // 当前播放: Song A

    // 切到下一首（循环）
    playlist.rotate_left(1);
    println!("切换后播放: {}", playlist[0]); // 切换后播放: Song B

    // 切到下一首（循环）
    playlist.rotate_left(1);
    println!("切换后播放: {}", playlist[0]); // 切换后播放: Song C

    // 切到下一首（循环）
    playlist.rotate_left(1);
    println!("切换后播放: {}", playlist[0]); // 切换后播放: Song D

    // 切到下一首（循环）
    playlist.rotate_left(1);
    println!("切换后播放: {}", playlist[0]); // 切换后播放: Song A (回到第一首)
}
```

reverse 和 rotate 虽然都是"重新排列"元素，但它们的语义完全不同。reverse 是把顺序完全颠倒，而 rotate 则是将元素像轮子一样滚动。在实际应用中，reverse 常用于需要"后进先出"显示的场景（比如聊天记录、撤销历史），而 rotate 则用于循环队列、轮播图、任务调度等需要"轮转"的场景。

#### 6.1.5.5 retain / retain_mut

retain 是 Vec 提供的一种强大的过滤方法，它接受一个闭包（closure），只保留让闭包返回 true 的元素。retain_mut 则是可变版本，允许你修改保留的元素。

```rust
fn main() {
    // retain: 只保留满足条件的元素
    let mut numbers: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("原始: {:?}", numbers); // 原始: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    // 只保留偶数
    numbers.retain(|&x| x % 2 == 0);
    println!("retain 偶数后: {:?}", numbers); // retain 偶数后: [2, 4, 6, 8, 10]

    // retain 的闭包接收的是元素的引用（&T）
    // 所以如果你需要值，需要解引用

    let mut words: Vec<String> = vec![
        String::from("apple"),
        String::from("banana"),
        String::from("cherry"),
        String::from("date"),
        String::from("elderberry"),
    ];
    println!("\n水果列表: {:?}", words);

    // 只保留长度大于5的水果
    words.retain(|word| word.len() > 5);
    println!("长度>5 的水果: {:?}", words);
    // 长度>5 的水果: ["banana", "cherry", "elderberry"]

    // retain_mut: 可变版本，可以在过滤时修改元素
    let mut data: Vec<i32> = vec![10, 20, 30, 40, 50];
    println!("\n原始数据: {:?}", data); // 原始数据: [10, 20, 30, 40, 50]

    // 保留小于 30 的元素，并且把它们翻倍
    data.retain_mut(|x| {
        if *x < 30 {
            *x *= 2; // 小于 30 的翻倍
            true // 保留
        } else {
            false // 大于等于 30 的移除
        }
    });
    println!("retain_mut 处理后: {:?}", data);
    // retain_mut 处理后: [20, 40]
    // 10 < 30 → 翻倍成 20，保留
    // 20 < 30 → 翻倍成 40，保留
    // 30 >= 30 → 移除（不翻倍）
    // 40 >= 30 → 移除
    // 50 >= 30 → 移除

    // 重新理解 retain_mut
    let mut numbers: Vec<i32> = vec![10, 20, 30, 40, 50];
    numbers.retain_mut(|x| {
        if *x <= 30 {
            *x *= 2;
            true  // 保留翻倍后的元素
        } else {
            false // 移除大于30的
        }
    });
    println!("只保留 <=30 并翻倍: {:?}", numbers);
    // 只保留 <=30 并翻倍: [20, 40, 60]
    // 10 → 20 (保留), 20 → 40 (保留), 30 → 60 (保留), 40 → 移除, 50 → 移除

    // 实际应用：过滤用户输入
    println!("\n过滤用户输入:");
    let mut user_entries: Vec<String> = vec![
        String::from("alice"),
        String::from(""), // 空字符串，无效
        String::from("Bob"),
        String::from("   "), // 只包含空格，无效
        String::from("Charlie"),
    ];

    println!("  原始输入: {:?}", user_entries);

    user_entries.retain(|entry| {
        !entry.trim().is_empty() // 移除空字符串和只包含空格的字符串
    });

    println!("  过滤后: {:?}", user_entries);
    // 过滤后: ["alice", "Bob", "Charlie"]

    // 实际应用：实现简单的权限过滤
    println!("\n权限过滤:");
    #[derive(Debug)]
    struct Permission {
        name: String,
        level: u8,
    }

    let mut permissions: Vec<Permission> = vec![
        Permission { name: String::from("read"), level: 1 },
        Permission { name: String::from("write"), level: 2 },
        Permission { name: String::from("delete"), level: 3 },
        Permission { name: String::from("admin"), level: 4 },
        Permission { name: String::from("super_admin"), level: 5 },
    ];

    // 只保留 level <= 3 的权限
    let max_level = 3;
    permissions.retain(|p| p.level <= max_level);
    println!("  保留 <= {} 的权限: {:?}", max_level, permissions);
    // 保留 <= 3 的权限: [Permission { name: "read", level: 1 }, Permission { name: "write", level: 2 }, Permission { name: "delete", level: 3 }]

    // retain 的性能
    // retain 需要保持元素的相对顺序
    // 它使用 swap-remove 的策略，所以时间复杂度是 O(n)
    // 但它不会因为移除元素而打乱剩余元素的顺序

    // 一个有趣的问题：如何反向过滤？
    let mut data: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\n反向过滤示例:");
    println!("  原始: {:?}", data); // 原始: [1, 2, 3, 4, 5]

    // 收集反向迭代器，然后 reverse
    let filtered: Vec<i32> = data.iter().copied().filter(|&x| x % 2 == 0).collect();
    println!("  只保留偶数（不修改原 Vec）: {:?}", filtered); // 只保留偶数（不修改原 Vec）: [2, 4]

    // 如果你需要原地反向过滤，需要一些技巧
    let mut mixed: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9];
    println!("  混合数据: {:?}", mixed); // 混合数据: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    mixed.retain(|&x| x % 2 != 0); // 只保留奇数
    println!("  只保留奇数: {:?}", mixed); // 只保留奇数: [1, 3, 5, 7, 9]
}
```

retain 和 retain_mut 是 Vec 的瑞士军刀中最锋利的小刀之一。它们允许你用最少的代码实现复杂的数据过滤和转换。retain 的工作原理是遍历 Vec，对每个元素调用闭包，然后根据闭包的返回值决定是保留还是丢弃。由于它保持了元素的相对顺序，它是一种"稳定"的过滤操作。

#### 6.1.5.6 splice / drain

splice 可以将 Vec 中某个范围内的元素替换成另一个迭代器的元素，而 drain 则是将某个范围内的元素"抽出来"，产生一个可迭代的 Drain 对象，同时从 Vec 中移除这些元素。

```rust
fn main() {
    // splice: 替换某个范围内的元素
    let mut numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("原始: {:?}", numbers); // 原始: [1, 2, 3, 4, 5]

    // 将索引 1..3 的元素（2, 3）替换成 [10, 20, 30]
    let replaced: Vec<i32> = numbers.splice(1..3, vec![10, 20, 30]).collect();
    println!("被替换的元素: {:?}", replaced); // 被替换的元素: [2, 3]
    println!("替换后: {:?}", numbers); // 替换后: [1, 10, 20, 30, 4, 5]

    // drain: 移除某个范围内的元素
    let mut colors: Vec<&str> = vec!["red", "green", "blue", "yellow", "purple"];
    println!("\n原始颜色: {:?}", colors); // 原始颜色: ["red", "green", "blue", "yellow", "purple"]

    // drain 索引 1..3 的元素
    let drained: Vec<&str> = colors.drain(1..4).collect();
    println!("被移除的元素: {:?}", drained); // 被移除的元素: ["green", "blue", "yellow"]
    println!("移除后: {:?}", colors); // 移除后: ["red", "purple"]

    // drain 可以 drain 到末尾
    let mut letters: Vec<char> = vec!['A', 'B', 'C', 'D', 'E'];
    println!("\n原始字母: {:?}", letters); // 原始字母: ['A', 'B', 'C', 'D', 'E']

    letters.drain(2..); // 从索引 2 一直 drain 到末尾
    println!("drain(2..) 后: {:?}", letters); // drain(2..) 后: ['A', 'B']

    // drain 全集
    let mut all: Vec<i32> = vec![1, 2, 3];
    println!("\n原始: {:?}", all); // 原始: [1, 2, 3]
    all.drain(..);
    println!("drain(..) 后: {:?}", all); // drain(..) 后: []

    // splice 的替换可以是空的
    let mut data: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("\n原始数据: {:?}", data); // 原始数据: [1, 2, 3, 4, 5]

    // 在索引 2 处插入 10, 20（不删除任何元素）
    data.splice(2..2, vec![10, 20]);
    println!("插入后: {:?}", data); // 插入后: [1, 2, 10, 20, 3, 4, 5]

    // splice 可以清空替换（替换成空迭代器）
    let mut clear_test: Vec<i32> = vec![1, 2, 3, 4, 5];
    clear_test.splice(1..4, std::iter::empty::<i32>()); // 空迭代器意味着只删除
    println!("删除中间元素后: {:?}", clear_test); // 删除中间元素后: [1, 5]

    // 实际应用：实现文本替换
    println!("\n文本替换示例:");
    let mut text_chars: Vec<char> = "Hello, World!".chars().collect();
    println!("原始文本: {:?}", text_chars); // 原始文本: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!']

    // 替换 "World" (索引 8..13)
    let replacement: String = "Rust".chars().collect();
    text_chars.splice(8..13, replacement.chars());
    let result: String = text_chars.into_iter().collect();
    println!("替换后: {}", result); // 替换后: Hello, Rust!

    // 实际应用：实现历史记录管理（撤销功能）
    println!("\n历史记录管理:");
    let mut history: Vec<String> = vec![
        String::from("版本1"),
        String::from("版本2"),
        String::from("版本3"),
        String::from("版本4"),
        String::from("版本5"),
    ];

    println!("  完整历史: {:?}", history);

    // 假设用户撤销了版本4和版本5（恢复到版本3）
    let removed = history.drain(3..);
    println!("  移除的版本: {:?}", removed.collect::<Vec<_>>());
    // 移除的版本: ["版本4", "版本5"]

    println!("  撤销后历史: {:?}", history);
    // 撤销后历史: ["版本1", "版本2", "版本3"]

    // splice 的返回值是一个迭代器
    // 可以用来获取被替换/删除的元素
    let mut nums: Vec<i32> = vec![1, 2, 3, 4, 5];
    let old: Vec<i32> = nums.splice(1..4, vec![10, 20]).collect();
    println!("\n原始数据: [1,2,3,4,5]");
    println!("被替换的元素: {:?}", old); // 被替换的元素: [2, 3, 4]
    println!("最终结果: {:?}", nums); // 最终结果: [1, 10, 20, 5]
}
```

splice 和 drain 都是"范围操作"，它们接受一个 Range 参数（可以是 `start..end`、`start..`、`..end`、或者 `..`）。splice 是"替换"，返回被替换的元素；drain 是"抽取"，返回被抽取的元素。两者都会从 Vec 中移除指定的元素，区别在于 drain 只移除不替换，splice 则会用新的元素填充被移除的位置。

#### 6.1.5.7 contains / binary_search

contains 检查 Vec 是否包含某个元素（使用 `==` 进行比较），返回布尔值。binary_search 则在已排序的 Vec 中二分查找某个元素，如果找到返回 Ok(index)，如果没找到返回 Err(insert_position)。

```rust
fn main() {
    // contains: 检查是否包含元素
    let fruits: Vec<&str> = vec!["apple", "banana", "orange", "grape", "mango"];
    println!("水果列表: {:?}", fruits); // 水果列表: ["apple", "banana", "orange", "grape", "mango"]

    println!("包含 'banana'? {}", fruits.contains(&"banana")); // 包含 'banana'? true
    println!("包含 'cherry'? {}", fruits.contains(&"cherry")); // 包含 'cherry'? false

    // contains 使用的是引用，所以要传递 &value
    // 对于实现了 Copy trait 的类型（如 i32），&value 和 value 是一样的
    // 但对于 String 或其他非 Copy 类型，需要传递引用

    // binary_search: 二分查找（要求 Vec 已排序）
    let sorted_numbers: Vec<i32> = vec![1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
    println!("\n排序后的数字: {:?}", sorted_numbers);
    // 排序后的数字: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    match sorted_numbers.binary_search(&7) {
        Ok(index) => println!("找到 7 在索引 {}", index), // 找到 7 在索引 3
        Err(_) => println!("没找到 7"),
    }

    match sorted_numbers.binary_search(&8) {
        Ok(index) => println!("找到 8 在索引 {}", index),
        Err(insert_pos) => println!("没找到 8，它应该插入在索引 {} 保持排序", insert_pos),
        // 没找到 8，它应该插入在索引 4 保持排序
    }

    match sorted_numbers.binary_search(&20) {
        Ok(index) => println!("找到 20 在索引 {}", index),
        Err(insert_pos) => println!("没找到 20，它应该插入在索引 {}", insert_pos),
        // 没找到 20，它应该插入在索引 10（末尾）
    }

    // binary_search_by: 自定义比较函数
    println!("\nbinary_search_by 示例:");
    #[derive(Debug)]
    struct Person {
        name: String,
        age: u32,
    }

    let mut people: Vec<Person> = vec![
        Person { name: String::from("Alice"), age: 25 },
        Person { name: String::from("Bob"), age: 30 },
        Person { name: String::from("Charlie"), age: 35 },
        Person { name: String::from("David"), age: 40 },
    ];

    // 按姓名排序后查找
    people.sort_by(|a, b| a.name.cmp(&b.name));

    match people.binary_search_by(|p| p.name.cmp("Charlie")) {
        Ok(index) => println!("找到 Charlie 在索引 {}，年龄 {}", index, people[index].age),
        // 找到 Charlie 在索引 1，年龄 35
        Err(_) => println!("没找到"),
    }

    // binary_search_by_key: 先按键值排序，再查找
    println!("\nbinary_search_by_key 示例:");
    let students: Vec<(&str, u32)> = vec![
        ("Tom", 85),
        ("Jerry", 92),
        ("Spike", 78),
        ("Tyke", 88),
    ];

    // 按分数排序
    let mut sorted_students: Vec<(&str, u32)> = students.clone();
    sorted_students.sort_by_key(|s| s.1);

    // 二分查找分数为 88 的学生
    match sorted_students.binary_search_by_key(&88, |s| s.1) {
        Ok(index) => println!("找到分数 88: {}", sorted_students[index].0), // 找到分数 88: Tyke
        Err(_) => println!("没找到"),
    }

    // contains 的性能是 O(n)，因为需要线性扫描
    // binary_search 的性能是 O(log n)，但要求数据已排序
    // 如果你需要频繁查找，考虑使用 HashSet 或 HashMap

    println!("\n性能对比:");
    let large_vec: Vec<i32> = (0..1_000_000).collect();

    let start = std::time::Instant::now();
    let found = large_vec.contains(&500000);
    let contains_time = start.elapsed();
    println!("  contains 查找 500000: {:?}, found={}", contains_time, found);
    // contains 查找 500000: ~几十毫秒, found=true

    let start = std::time::Instant::now();
    let result = large_vec.binary_search(&500000);
    let binary_time = start.elapsed();
    println!("  binary_search 查找 500000: {:?}, result={:?}", binary_time, result);
    // binary_search 查找 500000: ~几微秒, result=Ok(500000)

    // 结论：对于已排序的大数据，binary_search 远比 contains 快
}
```

contains 和 binary_search 是 Vec 提供的两种查找接口。contains 简单直接，适用于小规模数据或一次性查找。binary_search 则利用了二分查找的威力，在已排序的数据中能够以 O(log n) 的时间复杂度找到目标，比 contains 的 O(n) 快得多，特别是在大数据集上。如果你需要频繁查找，考虑使用 HashMap 或 HashSet，它们可以在 O(1) 时间内完成查找。

### 6.1.6 Vec<T> 与 [T; N] 的区别

Vec<T> 和 [T; N]（固定大小数组）是 Rust 中两个相似但本质不同的类型。虽然它们都用于存储同类型元素的有序序列，但它们在大小确定性、内存位置和性能特性上有显著差异。

#### 6.1.6.1 长度是否编译期确定

数组 [T; N] 的大小（长度 N）必须在编译期确定，而 Vec<T> 的大小可以在运行时动态变化。这是它们最根本的区别。

```rust
fn main() {
    // 数组 [T; N]：大小在编译期确定
    // 下面的数组长度是 5，这是编译期就知道的
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    println!("数组 arr: {:?}", arr); // 数组 arr: [1, 2, 3, 4, 5]
    println!("数组长度（编译期确定）: {}", arr.len()); // 数组长度（编译期确定）: 5

    // Vec<T>：大小在运行时确定，可以动态变化
    let mut vec: Vec<i32> = Vec::new(); // 初始为空
    vec.push(1);
    vec.push(2);
    vec.push(3);
    vec.push(4);
    vec.push(5);
    println!("\nVec: {:?}", vec); // Vec: [1, 2, 3, 4, 5]
    println!("Vec 长度（运行时确定）: {}", vec.len()); // Vec 长度（运行时确定）: 5

    // Vec 可以随时改变大小
    vec.push(6);
    vec.push(7);
    vec.push(8);
    println!("添加3个元素后: {:?}", vec); // 添加3个元素后: [1, 2, 3, 4, 5, 6, 7, 8]
    println!("新长度: {}", vec.len()); // 新长度: 8

    vec.pop();
    vec.pop();
    println!("移除2个元素后: {:?}", vec); // 移除2个元素后: [1, 2, 3, 4, 5, 6]
    println!("新长度: {}", vec.len()); // 新长度: 6

    // 数组不能这样做！
    // arr.push(6); // 错误！数组没有 push 方法
    // arr.pop();   // 错误！数组没有 pop 方法

    // 数组的大小必须是编译期常量
    const ARRAY_SIZE: usize = 10;
    let const_size_arr: [i32; ARRAY_SIZE] = [0; ARRAY_SIZE]; // 用 0 初始化
    println!("\n常量大小的数组: {:?}", const_size_arr);
    // 常量大小的数组: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    // 使用宏创建编译期已知的数组
    let macro_arr = [1; 100]; // 100 个元素，全部初始化为 1
    println!("宏创建的数组长度: {}", macro_arr.len()); // 宏创建的数组长度: 100

    // Vec 适合大小未知的场景
    println!("\n场景：读取未知数量的用户输入");
    let user_count = 5; // 假设这是运行时才知道的数量
    let mut user_names: Vec<String> = Vec::with_capacity(user_count);

    // 模拟读取用户
    for i in 0..user_count {
        user_names.push(format!("User_{}", i + 1));
    }
    println!("读取到的用户: {:?}", user_names);
    // 读取到的用户: ["User_1", "User_2", "User_3", "User_4", "User_5"]

    // 数组适合大小已知的场景
    println!("\n场景：表示一周的天数（固定7个）");
    let weekdays: [&str; 7] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ];
    println!("一周的天数: {:?}", weekdays);
    // 一周的天数: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
}
```

编译期确定大小 vs 运行时动态大小的区别，决定了它们的使用场景。数组适合大小固定、已知的场景，比如坐标 (x, y, z)、颜色 RGB、矩阵维度等。Vec 适合大小未知、会变化、需要动态添加/删除元素的场景，比如用户列表、文件内容、实时数据流等。

#### 6.1.6.2 栈上 vs 堆上分配

数组 [T; N] 通常存储在栈（Stack）上，而 Vec<T> 总是存储在堆（Heap）上。这是两种完全不同的内存分配策略，有着各自的优缺点。

```rust
fn main() {
    // 数组 - 存储在栈上
    // 栈是连续的内存空间，访问速度极快
    let stack_array: [i32; 5] = [1, 2, 3, 4, 5];
    println!("栈上数组: {:?}", stack_array);

    // Vec - 存储在堆上
    // 堆是动态分配的内存区域，访问速度稍慢，但大小灵活
    let heap_vec: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("堆上 Vec: {:?}", heap_vec);

    // 栈的优势：访问极快，分配极快（就是移动栈指针）
    // 栈的劣势：大小固定，空间有限（栈空间通常只有几 MB）
    println!("\n栈空间特点:");
    println!("  数组大小（字节）: {}", std::mem::size_of::<[i32; 5]>()); // 数组大小（字节）: 20
    println!("  Vec 大小（字节）: {}", std::mem::size_of::<Vec<i32>>()); // Vec 大小（字节）: 24

    // Vec 本身占 24 字节（3 个 usize）：
    // - 指向堆的指针（8 字节）
    // - 长度（8 字节）
    // - 容量（8 字节）
    // 而实际数据存储在堆上

    // 栈溢出的危险
    println!("\n栈溢出风险:");
    println!("  如果创建过大的数组在栈上，可能导致栈溢出");
    println!("  栈空间通常只有 1-8 MB，而堆可以到 GB 级别");

    // 示例：处理大数组 vs 大 Vec
    println!("\n大数组（栈）:");
    let large_stack: [u8; 1000] = [0; 1000]; // 1 KB，在栈上
    println!("  1000 字节数组在栈上，大小: {} 字节", std::mem::size_of_val(&large_stack));

    println!("\n大 Vec（堆）:");
    let large_heap: Vec<u8> = vec![0; 1_000_000]; // 1 MB，在堆上
    println!("  1MB Vec 实际数据在堆上，Vec 本身栈上只占 24 字节");
    println!("  Vec 的栈部分大小: {} 字节", std::mem::size_of::<Vec<u8>>()); // Vec 的栈部分大小: 24

    // 借用和所有权
    println!("\n借用规则:");
    let arr = [1, 2, 3];
    let arr_ref: &[i32] = &arr; // 数组引用可以直接转换为切片
    println!("  数组引用: {:?}", arr_ref);

    let vec = vec![1, 2, 3];
    let vec_ref: &[i32] = &vec; // Vec 引用自动解引用为切片
    println!("  Vec 引用: {:?}", vec_ref);

    // 性能测试
    println!("\n性能对比（访问元素）:");
    let arr: [i32; 10000] = [0; 10000];
    let vec: Vec<i32> = vec![0; 10000];

    let start = std::time::Instant::now();
    let _sum_arr = arr.iter().sum::<i32>();
    let arr_time = start.elapsed();

    let start = std::time::Instant::now();
    let _sum_vec = vec.iter().sum::<i32>();
    let vec_time = start.elapsed();

    println!("  数组遍历耗时: {:?}", arr_time);
    println!("  Vec 遍历耗时: {:?}", vec_time);
    // 两者差距很小，因为数据都在内存中
    // 真正影响性能的是缓存命中率、内存分配等因素

    // 实际建议
    println!("\n选择建议:");
    println!("  使用 [T; N] 当:");
    println!("    - 数据大小在编译期已知");
    println!("    - 数据较小（KB 级别）");
    println!("    - 需要极致性能");
    println!("  使用 Vec<T> 当:");
    println!("    - 数据大小在运行时确定");
    println!("    - 数据可能增长或缩小");
    println!("    - 数据较大（MB 或更大）");
    println!("    - 需要频繁添加/删除元素");
}
```

栈和堆的区别是理解 Vec 和数组差异的关键。栈上的数据分配和释放几乎是零成本的（只需要移动栈指针），但栈空间有限且大小固定。堆上的数据分配有开销（需要找到合适的空闲空间），释放也有开销（需要标记和回收），但堆空间几乎是无限的。

#### 6.1.6.3 性能差异

虽然 Vec 和数组在访问单个元素时性能几乎相同（都是 O(1) 的随机访问），但在分配、扩容、数据移动等方面有显著差异。

```rust
fn main() {
    use std::time::Instant;

    println!("性能对比实验:");

    // 1. 创建开销
    println!("\n1. 创建开销:");
    let start = Instant::now();
    for _ in 0..10000 {
        let arr: [i32; 100] = [0; 100];
        // 栈上创建，只是设置初始值
    }
    println!("  创建 10000 个数组（栈）: {:?}", start.elapsed());
    // 创建 10000 个数组（栈）: ~几百微秒

    let start = Instant::now();
    for _ in 0..10000 {
        let vec: Vec<i32> = vec![0; 100];
        // 堆上分配，需要系统调用
    }
    println!("  创建 10000 个 Vec（堆）: {:?}", start.elapsed());
    // 创建 10000 个 Vec（堆）: ~几毫秒

    // 2. 扩容开销
    println!("\n2. 扩容开销:");
    let start = Instant::now();
    let mut vec = Vec::with_capacity(1);
    for i in 0..1000 {
        vec.push(i);
    }
    println!("  Vec 1000 次 push（多次扩容）: {:?}", start.elapsed());
    // Vec 1000 次 push（多次扩容）: ~几十微秒

    let start = Instant::now();
    let mut vec = Vec::with_capacity(1000);
    for i in 0..1000 {
        vec.push(i);
    }
    println!("  Vec 1000 次 push（预分配）: {:?}", start.elapsed());
    // Vec 1000 次 push（预分配）: ~几微秒

    // 3. 遍历性能
    println!("\n3. 遍历性能:");
    let arr: [i32; 100000] = [0; 100000];
    let vec: Vec<i32> = vec![0; 100000];

    let start = Instant::now();
    let _sum_arr: i64 = arr.iter().map(|x| *x as i64).sum();
    println!("  数组遍历 + 映射 + 求和: {:?}", start.elapsed());

    let start = Instant::now();
    let _sum_vec: i64 = vec.iter().map(|x| *x as i64).sum();
    println!("  Vec 遍历 + 映射 + 求和: {:?}", start.elapsed());
    // 两者差距极小

    // 4. 内存占用
    println!("\n4. 内存占用:");
    let arr: [i32; 1000] = [0; 1000];
    println!("  数组 [i32; 1000] 栈占用: {} 字节", std::mem::size_of_val(&arr));

    let vec = vec![0; 1000];
    println!("  Vec<i32> 栈占用: {} 字节", std::mem::size_of::<Vec<i32>>());
    println!("  Vec<i32> 堆占用: {} 字节", std::mem::size_of_val(&vec));
    // 数组所有数据在栈上，Vec 只有元数据在栈上，数据在堆上

    // 5. 拷贝开销
    println!("\n5. 拷贝开销:");
    let arr: [i32; 100] = [0; 100];
    let start = Instant::now();
    for _ in 0..10000 {
        let _copy = arr; // 栈拷贝，整个数组复制
    }
    println!("  拷贝数组 10000 次: {:?}", start.elapsed());
    // 拷贝数组 10000 次: ~几毫秒（取决于数组大小）

    let vec = vec![0; 100];
    let start = Instant::now();
    for _ in 0..10000 {
        let _copy = vec.clone(); // 堆拷贝，只复制元数据和指针
    }
    println!("  克隆 Vec 10000 次: {:?}", start.elapsed());
    // 克隆 Vec 10000 次: ~几毫秒（只复制元数据）

    // 总结
    println!("\n=== 性能总结 ===");
    println!("  创建: 数组快（栈分配），Vec 慢（堆分配）");
    println!("  扩容: Vec 有扩容成本，预分配可以避免");
    println!("  访问: 两者都是 O(1)，几乎无差别");
    println!("  遍历: 两者几乎无差别");
    println!("  拷贝: 数组拷贝整个数据，Vec 只拷贝元数据");
    println!("  内存: 数组在栈，Vec 在堆");
    println!("\n选择建议:");
    println!("  - 小而固定的数据用数组");
    println!("  - 大小不确定或需要变化的数据用 Vec");
    println!("  - 对性能敏感的核心算法可以考虑数组");
    println!("  - 日常编程 Vec 更灵活，足够高效");
}
```

性能对比的结果很清楚：数组在创建和拷贝小数据时有优势，而 Vec 在大数据和灵活性上有优势。但在实际应用中，两者的访问性能几乎相同，因为现代 CPU 的缓存机制使得栈和堆的访问速度差异在大多数场景下可以忽略不计。选择数组还是 Vec，主要取决于你的数据大小是否固定，以及你需要哪种灵活性。

---

## 6.2 Box<T>（堆分配）

如果说 Vec 是 Rust 世界里最受欢迎的储物箱，那 Box<T> 就是那个最基础、最直接的"把东西扔到堆上"的工具。Box 是 "Boxed" 的缩写，它是一种智能指针（Smart Pointer），用于将数据存储在堆上而不是栈上。

为什么需要 Box？想象一下这个场景：你有一个超大的结构体，里面包含了几十兆字节的数据。如果这个结构体存在栈上，你的函数调用栈可能会被撑爆；如果存在堆上，栈上只需要存一个指向堆的指针就行了。Box 就是帮你做这件事的——它把数据"装箱"后放到堆上，然后在栈上留下一个"地址牌"（指针）。

Box 的使用场景非常广泛：递归类型（链表、树等）需要 Box 来打破编译期的大小计算；Trait 对象需要 Box 来实现动态分发；大型数据需要避免栈溢出时也需要 Box。在 Rust 的世界里，Box 是通往堆内存的最简单、最直接的大门。

### 6.2.1 堆分配基础

Box<T> 是 Rust 提供的最简单的堆分配方式。它将数据存储在堆上，只在栈上保留一个指针。Box 实现了 Deref 和 Drop trait，所以你可以像使用普通引用一样使用 Box，同时 Box 会在离开作用域时自动释放堆上的内存。

#### 6.2.1.1 Box::new(value)

Box::new() 是创建 Box 最直接的方式。它接受一个值，把它"装箱"后放到堆上，并返回一个指向该值的 Box。

```rust
fn main() {
    // 创建一个 Box
    let boxed_number = Box::new(42);
    println!("Box 里的数字: {}", boxed_number); // Box 里的数字: 42

    // Box 实现了 Deref，所以可以使用 * 解引用
    println!("解引用后的数字: {}", *boxed_number); // 解引用后的数字: 42

    // 创建包含复杂数据的 Box
    let point = Box::new((0.0, 0.0));
    println!("原点坐标: {:?}", point); // 原点坐标: (0.0, 0.0)

    // 创建包含结构体的 Box
    struct Person {
        name: String,
        age: u32,
    }

    let person = Box::new(Person {
        name: String::from("Alice"),
        age: 30,
    });
    println!("\n人物信息:");
    println!("  姓名: {}", person.name); // 姓名: Alice
    println!("  年龄: {}", person.age); // 年龄: 30

    // Box 的本质：栈上存指针，堆上存数据
    // Box::new(value) 会：
    // 1. 在堆上分配足够的内存存储 value
    // 2. 把 value 拷贝到堆上
    // 3. 返回一个 Box 指针，指向堆上的数据

    // 访问 Box 内部数据的方式
    let data = Box::new(vec![1, 2, 3, 4, 5]);
    println!("\nBox<Vec> 数据: {:?}", data); // Box<Vec> 数据: [1, 2, 3, 4, 5]

    // 使用 & 解引用
    println!("第一个元素: {}", &data[0]); // 第一个元素: 1

    // 使用解引用操作符
    println!("数据总和: {}", data.iter().sum::<i32>()); // 数据总和: 15

    // 嵌套 Box
    let nested = Box::new(Box::new(100));
    println!("\n嵌套 Box: {}", **nested); // 嵌套 Box: 100
    // 需要两次解引用：第一次从 Box<Box<i32>> 到 Box<i32>，第二次从 Box<i32> 到 i32

    // Box 的大小
    println!("\nBox 的内存大小:");
    println!("  Box<i32> 在栈上占: {} 字节", std::mem::size_of::<Box<i32>>()); // Box<i32> 在栈上占: 8 字节（指针）
    println!("  i32 在堆上占: {} 字节", std::mem::size_of::<i32>()); // i32 在堆上占: 4 字节

    // Box 的性能
    println!("\n创建 Box 的性能:");
    let start = std::time::Instant::now();
    for _ in 0..1_000_000 {
        let _b = Box::new(42);
    }
    println!("  创建 1000000 个 Box: {:?}", start.elapsed());
    // 创建 1000000 个 Box: ~几十到几百毫秒

    // Box vs 直接栈变量
    let start = std::time::Instant::now();
    for _ in 0..1_000_000 {
        let _n = 42;
    }
    println!("  创建 1000000 个栈变量: {:?}", start.elapsed());
    // 创建 1000000 个栈变量: ~几毫秒

    // 结论：Box 有额外的堆分配开销，但带来了灵活性
}
```

Box::new() 看起来简单，但背后做了很多事情：堆内存分配、数据拷贝（如果是 Copy 类型）或移动、返回指针。当 Box 被 drop 时（离开作用域），堆上的内存会被自动释放。这使得 Box 成为 Rust 中最安全的堆分配方式——你不需要手动调用 free，你只需要让 Box 离开作用域。

#### 6.2.1.2 Box::leak(boxed)

Box::leak() 是一个有趣的方法，它消费一个 Box，然后返回内部值的可变引用。关键是：这个 Box 永远不会被 drop，也就是说堆上的内存永远不会被释放。这听起来像内存泄漏，但有时候这正是你需要的！

什么情况下需要"故意泄漏"内存？最常见的场景是：你需要创建一个在整个程序运行期间都存在的全局变量。比如，一个配置对象，你想让它从程序开始到结束都存在，中途不会被释放。在这种情况下，Box::leak() 是完美的工具。

```rust
fn main() {
    // Box::leak 的基本用法
    let boxed = Box::new(42);
    // 消费 Box，获取内部值的可变引用，并且"泄漏"它
    let leaked = Box::leak(boxed);
    println!("泄漏的值: {}", leaked); // 泄漏的值: 42

    // 现在 leaked 是一个 &'static mut i32
    // 它指向的内存永远不会释放

    // 修改泄漏的值
    *leaked = 100;
    println!("修改后: {}", leaked); // 修改后: 100

    // 实际应用：创建全局可变的配置
    println!("\n全局配置示例:");

    struct Config {
        debug_mode: bool,
        max_connections: u32,
        timeout_seconds: u64,
    }

    // 创建一个配置并泄漏它
    let config = Box::new(Config {
        debug_mode: false,
        max_connections: 100,
        timeout_seconds: 30,
    });

    // 泄漏 Box，获取静态引用
    let static_config: &'static mut Config = Box::leak(config);

    // 修改配置
    static_config.debug_mode = true;
    static_config.max_connections = 200;
    println!("当前配置: debug={}, connections={}, timeout={}",
             static_config.debug_mode, static_config.max_connections, static_config.timeout_seconds);
    // 当前配置: debug=true, connections=200, timeout=30

    // 注意：这个配置永远不会释放！
    // 这对于全局状态来说是可以接受的

    // 另一个应用：构建一个永不释放的缓存
    println!("\n永久缓存示例:");
    struct Cache {
        data: Vec<String>,
    }

    let cache = Box::new(Cache {
        data: vec![
            String::from("常驻数据1"),
            String::from("常驻数据2"),
            String::from("常驻数据3"),
        ],
    });

    let static_cache: &'static mut Cache = Box::leak(cache);
    println!("永久缓存: {:?}", static_cache.data);
    // 永久缓存: ["常驻数据1", "常驻数据2", "常驻数据3"]

    // 可以继续添加数据
    static_cache.data.push(String::from("动态添加的数据"));
    println!("添加后: {:?}", static_cache.data);
    // 添加后: ["常驻数据1", "常驻数据2", "常驻数据3", "动态添加的数据"]

    // Box::leak 只能用于可变的 Box
    // let immut_box = Box::new(42);
    // let _leaked = Box::leak(immut_box); // 错误！Box::leak 要求 Box<T>

    // 实际上 Box::leak 的签名是：fn leak<'a>(b: Box<T>) -> &'a mut T
    // 它消费 Box，返回可变引用

    // leak 在 Rust 标准库中的使用场景
    println!("\nleak 在标准库中的应用:");

    // String::leak 和 Vec::leak
    let s = String::from("hello world");
    let leaked_string: &'static str = Box::leak(s.into_boxed_str());
    println!("泄漏的字符串: {}", leaked_string); // 泄漏的字符串: hello world

    let v = vec![1, 2, 3, 4, 5];
    let leaked_vec: &'static mut [i32] = Box::leak(v.into_boxed_slice());
    println!("泄漏的 Vec: {:?}", leaked_vec); // 泄漏的 Vec: [1, 2, 3, 4, 5]

    // 注意：泄漏后的数据是 'static 生命周期的
    // 这意味着它可以被任何需要 'static 生命周期的上下文中使用
}
```

Box::leak 是一个非常特殊的工具，它打破了 Rust 正常的内存管理规则。在大多数情况下，你应该让 Box 正常 drop，自动释放内存。但当你确实需要一个"全局的、永久存在的"数据时，Box::leak 是正确且安全的选择。与 C/C++ 中的全局变量不同，Box::leak 仍然让你能够修改数据，而且不会有未定义行为的风险。

#### 6.2.1.3 Box::into_raw / from_raw

Box::into_raw() 消费 Box，返回一个原始指针（`*mut T`），让你完全控制这个指针。Box::from_raw() 则相反，它接受一个原始指针，重新构建出一个 Box。这两个方法配合使用，可以让你在 Rust 和其他语言（或不安全的代码）之间传递指针。

```rust
fn main() {
    // Box::into_raw: 从 Box 获取原始指针
    println!("Box::into_raw 示例:");
    let boxed = Box::new(42);
    println!("Box 原始值: {}", boxed); // Box 原始值: 42

    // into_raw 消费 Box，返回原始指针
    // Box 不再自动 drop，内存管理权转交给了你
    let raw_ptr = Box::into_raw(boxed);
    println!("原始指针: {:?}", raw_ptr); // 原始指针: 0x...（内存地址）

    // 通过原始指针访问数据（需要 unsafe）
    unsafe {
        println!("通过指针读取: {}", *raw_ptr); // 通过指针读取: 42
        *raw_ptr = 100;
        println!("修改后: {}", *raw_ptr); // 修改后: 100
    }

    // 重要：手动释放内存，否则内存泄漏
    unsafe {
        drop(Box::from_raw(raw_ptr));
        // 现在 raw_ptr 已经无效，不能再使用
        println!("内存已释放");
    }

    // Box::from_raw: 从原始指针重建 Box
    println!("\nBox::from_raw 示例:");

    // 分配内存并创建结构体
    struct Person {
        name: String,
        age: u32,
    }

    // 创建一个 Box
    let person_box = Box::new(Person {
        name: String::from("Bob"),
        age: 25,
    });

    // 转换为原始指针
    let person_ptr = Box::into_raw(person_box);

    // 使用原始指针传递数据（模拟 FFI 调用）
    println!("通过原始指针访问 Person:");
    unsafe {
        println!("  姓名: {}", (*person_ptr).name); // 姓名: Bob
        println!("  年龄: {}", (*person_ptr).age); // 年龄: 25
    }

    // 使用 from_raw 重建 Box 并自动管理内存
    let _rebuilt_box = unsafe { Box::from_raw(person_ptr) };
    // 重建后，当这个 Box 离开作用域时，内存会自动释放

    // into_raw 和 from_raw 的配对使用
    println!("\n配对使用示例:");
    let data = vec![1, 2, 3, 4, 5];

    // 把 Vec 转换成 Box<[i32]>，然后获取原始指针
    let boxed_slice = data.into_boxed_slice();
    let raw = Box::into_raw(boxed_slice);

    // 模拟通过 FFI 传递指针
    println!("传递指针到外部...");
    println!("原始指针: {:?}", raw);

    // 重建 Box 并使用
    let restored = unsafe { Box::from_raw(raw) };
    println!("重建后的 Vec: {:?}", restored.to_vec());
    // 重建后的 Vec: [1, 2, 3, 4, 5]

    // 实际应用：与 C 语言交互
    println!("\n与 C 风格代码交互:");
    extern "C" {
        // 假设这是 C 库的函数
        fn c_allocate(size: usize) -> *mut i32;
        fn c_deallocate(ptr: *mut i32);
    }

    // 模拟一个场景：从某个地方获取指针
    // let ptr = unsafe { c_allocate(10) };
    // ... 使用 ptr ...
    // unsafe { c_deallocate(ptr) }; // 需要手动释放

    // 更安全的方式：包装成 Box
    // let ptr = unsafe { c_allocate(10) };
    // let _box = unsafe { Box::from_raw(ptr) };
    // ... 使用 _box ...
    // 当 _box 离开作用域时，c_deallocate 不会被调用！
    // 所以你需要自己处理...

    // 正确的模式：使用 into_raw 后手动 drop
    let boxed = Box::new(42);
    let raw = Box::into_raw(boxed);
    unsafe {
        // 使用指针...
        let box_for_cleanup = Box::from_raw(raw);
        // ... 使用 box_for_cleanup ...
        // 正常 drop
    }

    println!("Box 已正确清理");

    // 注意事项：不要 double-free
    // let boxed = Box::new(42);
    // let raw = Box::into_raw(boxed);
    // drop(boxed); // 错误！boxed 已经被消费了
    // let _ = unsafe { Box::from_raw(raw) }; // ok
}
```

Box::into_raw 和 Box::from_raw 是 Rust 提供的一对"拆箱"和"装箱"工具。它们让你在安全的 Box 和危险的原始指针之间自由转换。这种能力在系统编程、与 C/C++ 库交互、以及实现自定义内存分配策略时非常有用。但请记住：使用原始指针时，你需要自己保证内存安全。忘记调用 drop 会导致内存泄漏，多次 drop 会导致 double-free 崩溃。

#### 6.2.1.4 Box::pin

Box::pin() 是一个专门用于"固定"（pinning）数据的特殊方法。固定是什么意思呢？固定的数据保证永远不会在内存中移动位置。这听起来很奇怪——为什么要保证数据不移动呢？

答案在于 Rust 的异步编程和自引用结构体。当你使用 async/await 时，Rust 编译器会生成状态机，这些状态机可能会包含指向自身内部数据的指针。如果这些数据在内存中移动（比如因为 GC 或者栈收缩），这些指针就会变成悬空指针。Box::pin 就是为了解决这个问题——它保证数据一旦分配，就永远不会移动。

```rust
fn main() {
    // Box::pin 的基本用法
    println!("Box::pin 示例:");
    let pinned: Box<Pin<i32>> = Box::pin(42);
    println!("固定的值: {}", *pinned); // 固定的值: 42

    // Pin<Box<T>> 实现了 Deref，所以可以像普通 Box 一样使用
    let value = *pinned;
    println!("解引用: {}", value); // 解引用: 42

    // Box::pin<T> 实际上是 Pin<Box<T>> 的别名
    // 所以上面等价于: let pinned = Pin::new(Box::new(42));

    // pinned 数据不能被移动
    println!("\nPin 的特性:");
    let mut pinned_data = Box::pin(vec![1, 2, 3, 4, 5]);
    println!("固定的数据: {:?}", pinned_data); // 固定的数据: [1, 2, 3, 4, 5]

    // 可以修改数据本身
    pinned_data[0] = 100;
    println!("修改后: {:?}", pinned_data); // 修改后: [100, 2, 3, 4, 5]

    // 但是不能把数据从 Box 中取出来然后放到别处
    // 下面这行代码会编译失败：
    // let data = Pin::into_inner(pinned_data); // 错误！

    // 正确的方式是使用 as_mut() 来访问内部数据
    let mut pinned_i32 = Box::pin(42);
    Pin::as_mut(&mut pinned_i32).set(100);
    println!("通过 set 修改: {}", *pinned_i32); // 通过 set 修改: 100

    // Pin 在异步编程中的应用
    println!("\nPin 在 async 中的应用（概念示例）:");
    println!("  当使用 async/await 时，生成的状态机可能包含自引用");
    println!("  如果状态机在内存中移动，自引用指针会失效");
    println!("  Pin 保证状态机在内存中的位置不变");

    // 自引用结构体的问题
    println!("\n自引用结构体问题:");
    struct SelfRef {
        value: i32,
        // 这个指针指向 value，但如果 SelfRef 在内存中移动，指针就失效了
        // pointer_to_value: *const i32,
    }

    // 如果没有 Pin，这样的结构体是不安全的
    // 使用 Pin 可以安全地处理这种情况

    // Box::pin 与 Box::new 的区别
    println!("\nBox::new vs Box::pin:");
    let normal_box = Box::new(String::from("hello"));
    let pinned_box = Box::pin(String::from("world"));

    // 都可以解引用
    println!("普通 Box: {}", normal_box);
    println!("固定 Box: {}", pinned_box);

    // 但 Pin 保证数据不移动
    // normal_box 可以通过 into_inner() 取出数据
    // pinned_box 不行（除非 T: Unpin）

    // 实际上，对于实现了 Unpin 的类型（如 i32, String 等），
    // Pin<Box<T>> 基本上和 Box<T> 一样，因为 Unpin 类型可以安全地移动

    // 什么类型不是 Unpin？
    // - Future（异步计算的状态）
    // - Generator（协程）
    // - 手动实现 !Unpin 的类型

    // 示例：创建一个 !Unpin 的类型
    println!("\n!Unpin 类型:");
    struct NotUnpin {
        data: *mut i32,
    }

    impl !Unpin for NotUnpin {}

    // Box<NotUnpin> 不能直接使用
    // 需要使用 Box::pin 来创建
    let mut pinned_not_unpin: Pin<Box<NotUnpin>> = Box::pin(NotUnpin {
        data: std::ptr::null_mut(),
    });

    // 不能把数据移出来
    // let _data = Pin::into_inner(pinned_not_unpin); // 错误！

    println!("成功创建了 Pin<Box<NotUnpin>>");
}
```

Box::pin 看起来很神秘，但它的用途非常具体：支持异步编程和自引用数据结构。在日常的同步代码中，你可能很少需要直接使用 Box::pin。但是当你开始写 async 代码时，Pin 会成为你不可或缺的工具。理解 Pin 的关键是理解"固定"的含义——被固定的数据不能被移动到内存的其他位置，这对于维护指针的有效性至关重要。

### 6.2.2 递归类型的堆分配

递归类型是指包含自身实例的类型，比如链表、树等。问题是：Rust 需要在编译期知道每个类型的大小。但如果一个结构体包含自身，那么它的大小就是无限的（结构体包含自己，自己包含自己，循环往复，永远算不出大小）。

解决方案是使用 Box——因为 Box 是指针类型，指针的大小是固定的（通常是 8 字节），Rust 可以轻松计算包含 Box 的递归类型的大小。

#### 6.2.2.1 链表

链表是最经典的递归数据结构。让我们用 Rust 实现一个简单的单向链表。

```rust
fn main() {
    // 定义一个单向链表节点
    // Node 包含一个 i32 值，和一个指向下一个节点的 Box
    enum List {
        Cons(i32, Box<List>), // Cons 是"构造"（construct）的缩写
        Nil,                   // Nil 表示空链表（结束）
    }

    use List::*;

    // 创建链表: 1 -> 2 -> 3 -> Nil
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));

    // 遍历链表
    fn print_list(list: &List) {
        match list {
            Cons(value, next) => {
                print!("{} -> ", value);
                print_list(next);
            }
            Nil => println!("Nil"),
        }
    }

    println!("链表: ");
    print_list(&list);
    // 输出: 1 -> 2 -> 3 -> Nil

    // 如果不用 Box，编译会失败
    // enum BadList {
    //     Cons(i32, BadList), // 错误：BadList 没有固定大小
    //     Nil,
    // }

    // 链表的常用操作
    println!("\n链表操作:");

    // 长度
    fn length(list: &List) -> usize {
        match list {
            Cons(_, next) => 1 + length(next),
            Nil => 0,
        }
    }
    println!("链表长度: {}", length(&list)); // 链表长度: 3

    // 累加
    fn sum(list: &List) -> i32 {
        match list {
            Cons(value, next) => value + sum(next),
            Nil => 0,
        }
    }
    println!("链表元素和: {}", sum(&list)); // 链表元素和: 6

    // 查找
    fn contains(list: &List, target: i32) -> bool {
        match list {
            Cons(value, next) => {
                if *value == target {
                    true
                } else {
                    contains(next, target)
                }
            }
            Nil => false,
        }
    }
    println!("包含 2? {}", contains(&list, 2)); // 包含 2? true
    println!("包含 5? {}", contains(&list, 5)); // 包含 5? false
}
```

链表是理解递归类型和 Box 的经典案例。在这个例子中，`List` 是一个递归枚举（recursive enum），它要么是一个包含值和下一个节点的 `Cons`，要么是一个表示结束的 `Nil`。关键是使用 `Box<List>` 来包装下一个节点的引用——因为 Box 的大小是固定的（就是一个指针），Rust 可以轻松计算出 `Cons(i32, Box<List>)` 的大小。

### 链表 vs Vec：谁才是真正的王者？

这是一个永恒的编程话题。Vec 在大多数场景下都比链表更好，原因如下：

1. **缓存友好**：Vec 的元素在内存中是连续存储的，CPU 缓存可以一次性预取多个元素；链表的节点在内存中分散存储，每次访问下一个节点都可能引发缓存未命中。
2. **随机访问**：Vec 可以 O(1) 随机访问任意元素，链表访问第 n 个元素需要 O(n)。
3. **内存开销**：链表每个节点都需要额外的指针开销，Vec 没有这个成本。

> 但链表在插入和删除操作上有优势——在已知位置的情况下，这些操作是 O(1)。不过，由于随机访问的成本，在链表中"到达目标位置"这个步骤往往是 O(n)。

### 链表的基本操作：头插法与头删法

```rust
fn main() {
    // 链表节点定义
    enum List {
        Cons(i32, Box<List>),
        Nil,
    }

    use List::*;

    // 头插法：在链表头部插入新节点
    fn push_front(list: &List, value: i32) -> List {
        Cons(value, Box::new(list.clone()))
    }

    // 头删法：删除链表头部节点
    fn pop_front(list: &List) -> Option<(&i32, &List)> {
        match list {
            Cons(value, next) => Some((value, next)),
            Nil => None,
        }
    }

    // 使用示例
    let empty: List = Nil;
    let list1 = Cons(1, Box::new(Nil));
    let list2 = Cons(2, Box::new(list1.clone()));
    let list3 = Cons(3, Box::new(list2.clone()));

    println!("原始链表:");
    fn print_list(list: &List) {
        match list {
            Cons(value, next) => {
                print!("{} -> ", value);
                print_list(next);
            }
            Nil => println!("Nil"),
        }
    }
    print_list(&list3);
    // 输出: 3 -> 2 -> 1 -> Nil

    // 头删法演示
    println!("\n头删法:");
    if let Some((value, rest)) = pop_front(&list3) {
        println!("删除头节点: {}，剩余: {:?}", value, rest);
        // 删除头节点: 3，剩余: Cons(2, ...)
    }

    // 链表反转（经典面试题）
    println!("\n链表反转:");
    fn reverse(list: &List) -> List {
        let mut current = list;
        let mut reversed = Box::new(Nil);

        loop {
            match current {
                Cons(value, next) => {
                    // 创建新节点，指向前一个反转结果
                    let new_node: Box<List> = Box::new(Cons(*value, reversed));
                    reversed = new_node;
                    current = next;
                }
                Nil => break,
            }
        }
        *reversed
    }

    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
    print!("原链表: ");
    print_list(&list);
    println!();

    let reversed = reverse(&list);
    print!("反转后: ");
    print_list(&reversed);
    // 输出: 原链表: 1 -> 2 -> 3 -> Nil
    //       反转后: 3 -> 2 -> 1 -> Nil
}
```

#### 6.2.2.2 树结构

如果说链表是"一维的递归"，那树就是"二维的递归"。树结构在计算机科学中无处不在——文件系统、XML/JSON 解析、表达式求值、排序算法（二叉搜索树）、图的实现等。让我来实现一个最简单的二叉树。

```rust
fn main() {
    // 二叉树节点定义
    // 每个节点有一个值，左子树，右子树
    enum Tree<T> {
        Node {
            value: T,
            left: Box<Tree<T>>,
            right: Box<Tree<T>>,
        },
        Empty,
    }

    use Tree::*;

    // 创建一个叶子节点
    fn leaf(value: i32) -> Tree<i32> {
        Node {
            value,
            left: Box::new(Empty),
            right: Box::new(Empty),
        }
    }

    // 手动构建一棵树
    //        4
    //       / \
    //      2   6
    //     / \ / \
    //    1  3 5  7
    let tree = Node {
        value: 4,
        left: Box::new(Node {
            value: 2,
            left: leaf(1),
            right: leaf(3),
        }),
        right: Box::new(Node {
            value: 6,
            left: leaf(5),
            right: leaf(7),
        }),
    };

    // 前序遍历：根 -> 左 -> 右
    fn preorder(tree: &Tree<i32>) {
        match tree {
            Node { value, left, right } => {
                print!("{} ", value);
                preorder(left);
                preorder(right);
            }
            Empty => {}
        }
    }

    // 中序遍历：左 -> 根 -> 右
    fn inorder(tree: &Tree<i32>) {
        match tree {
            Node { value, left, right } => {
                inorder(left);
                print!("{} ", value);
                inorder(right);
            }
            Empty => {}
        }
    }

    // 后序遍历：左 -> 右 -> 根
    fn postorder(tree: &Tree<i32>) {
        match tree {
            Node { value, left, right } => {
                postorder(left);
                postorder(right);
                print!("{} ", value);
            }
            Empty => {}
        }
    }

    println!("树结构遍历:");
    println!("     4");
    println!("    / \\");
    println!("   2   6");
    println!("  / \\ / \\");
    println!(" 1  3 5  7");
    println!();

    println!("前序遍历 (根-左-右): ");
    preorder(&tree);
    println!(); // 4 2 1 3 6 5 7

    println!("中序遍历 (左-根-右): ");
    inorder(&tree);
    println!(); // 1 2 3 4 5 6 7

    println!("后序遍历 (左-右-根): ");
    postorder(&tree);
    println!(); // 1 3 2 5 7 6 4

    // 计算树的深度
    fn depth<T>(tree: &Tree<T>) -> usize {
        match tree {
            Node { left, right, .. } => {
                1 + std::cmp::max(depth(left), depth(right))
            }
            Empty => 0,
        }
    }

    println!("\n树的深度: {}", depth(&tree)); // 树的深度: 3

    // 计算树的节点数
    fn size<T>(tree: &Tree<T>) -> usize {
        match tree {
            Node { left, right, .. } => 1 + size(left) + size(right),
            Empty => 0,
        }
    }

    println!("树的节点数: {}", size(&tree)); // 树的节点数: 7

    // 在树中查找值
    fn find(tree: &Tree<i32>, target: i32) -> bool {
        match tree {
            Node { value, left, right } => {
                if *value == target {
                    true
                } else {
                    find(left, target) || find(right, target)
                }
            }
            Empty => false,
        }
    }

    println!("\n查找 5: {}", find(&tree, 5)); // 查找 5: true
    println!("查找 10: {}", find(&tree, 10)); // 查找 10: false

    // 二叉搜索树（BST）的插入
    // BST 的性质：左子树所有节点小于根，右子树所有节点大于根
    fn insert(tree: &Tree<i32>, value: i32) -> Tree<i32> {
        match tree {
            Node { value: v, left, right } => {
                if value < *v {
                    Node {
                        value: *v,
                        left: Box::new(insert(left, value)),
                        right: right.clone(),
                    }
                } else {
                    Node {
                        value: *v,
                        left: left.clone(),
                        right: Box::new(insert(right, value)),
                    }
                }
            }
            Empty => leaf(value),
        }
    }

    let bst = Empty;
    let bst = insert(&bst, 5);
    let bst = insert(&bst, 3);
    let bst = insert(&bst, 7);
    let bst = insert(&bst, 1);
    let bst = insert(&bst, 4);

    println!("\nBST 中序遍历 (应该是有序的):");
    inorder(&bst);
    println!(); // 1 3 4 5 7
}
```

树的递归性质在这里展现得淋漓尽致。遍历、搜索、插入、删除……几乎所有操作都可以用递归简洁地表达。这得益于树的天然递归结构——树由子树组成，而子树也是树。

> 你知道吗？文件系统的目录结构就是一棵树。每个目录是节点，目录里的文件是叶子，目录里的子目录是子树。所以当你用递归算法遍历文件系统时，你其实就是在遍历一棵树！

### 6.2.3 Trait 对象

Trait 对象是 Rust 实现"多态"的方式。想象一下，你有一群"会叫"的动物（狗、猫、鸟），你想写一个函数让它们各自发出自己的声音。在传统的面向对象语言中，你可能会用继承——创建一个"动物"基类，然后让狗、猫、鸟继承它。但在 Rust 中，我们用 Trait 和 Trait 对象来实现同样的效果。

#### 6.2.3.1 Box<dyn Trait>

`dyn Trait` 是 Rust 中表示"实现了某个 Trait 的任意类型"的方式。加上 `Box`，就是"一个指向实现了某 Trait 的任意类型的堆分配指针"。

```rust
fn main() {
    // 定义一个 Trait：会叫的东西
    trait Speak {
        fn speak(&self) -> String;
    }

    // 实现 Speak for Dog
    struct Dog {
        name: String,
    }

    impl Speak for Dog {
        fn speak(&self) -> String {
            format!("{} 说: 汪汪！", self.name)
        }
    }

    // 实现 Speak for Cat
    struct Cat {
        name: String,
    }

    impl Speak for Cat {
        fn speak(&self) -> String {
            format!("{} 说: 喵喵~", self.name)
        }
    }

    // 实现 Speak for Bird
    struct Bird {
        name: String,
    }

    impl Speak for Bird {
        fn speak(&self) -> String {
            format!("{} 说: 叽叽喳喳！", self.name)
        }
    }

    // 创建一个动物数组，但使用 Trait 对象
    let animals: Vec<Box<dyn Speak>> = vec![
        Box::new(Dog { name: String::from("旺财") }),
        Box::new(Cat { name: String::from("小咪") }),
        Box::new(Bird { name: String::from("小鹦") }),
        Box::new(Dog { name: String::from("阿黄") }),
    ];

    println!("动物们在说话:");
    for animal in &animals {
        println!("  {}", animal.speak());
    }
    // 动物们在说话:
    //   旺财 说: 汪汪！
    //   小咪 说: 喵喵~
    //   小鹦 说: 叽叽喳喳！
    //   阿黄 说: 汪汪！

    // Trait 对象允许我们在运行时决定调用哪个具体实现
    // 这叫做"动态分发"（dynamic dispatch）
    // 对比之下，泛型在编译时就知道具体类型，叫做"静态分发"（static dispatch）

    // 动态分发 vs 静态分发的权衡
    println!("\n动态分发 vs 静态分发:");

    // 静态分发（泛型）：编译时展开，每个类型生成一份代码
    fn speak_all_static<T: Speak>(animals: &[T]) {
        for animal in animals {
            println!("  {}", animal.speak());
        }
    }

    // 动态分发（Trait 对象）：运行时查虚表，代码共享
    fn speak_all_dynamic(animals: &[Box<dyn Speak>]) {
        for animal in animals {
            println!("  {}", animal.speak());
        }
    }

    println!("静态分发示例:");
    let dogs = vec![Dog { name: String::from("狗1") }, Dog { name: String::from("狗2") }];
    speak_all_static(&dogs);

    println!("\n动态分发示例:");
    let animals: Vec<Box<dyn Speak>> = vec![
        Box::new(Dog { name: String::from("动物1") }),
        Box::new(Cat { name: String::from("动物2") }),
    ];
    speak_all_dynamic(&animals);

    // Box<dyn Trait> 的内存布局
    println!("\nBox<dyn Trait> 的内存布局:");
    println!("  Box<dyn Speak> 栈上大小: {} 字节", std::mem::size_of::<Box<dyn Speak>>());
    // Box<dyn Speak> 在栈上只占 8 字节（一个指针，指向堆上的数据）
    // 堆上的数据包含：实际对象 + vtable 指针
    // - 指针指向堆上的实际数据
    // - vtable（虚表）也在堆上，存储方法指针、drop 函数、size/align 信息

    // vtable 包含什么？
    // - 指向实现的 speak 方法的指针
    // - drop 需要的清理函数指针
    // - size_of 和 align_of 信息

    // Box<dyn Trait> 的限制
    println!("\nBox<dyn Trait> 的限制:");

    // 1. 只能调用 Trait 中定义的方法
    // struct Duck { weight: f32 }
    // impl Speak for Duck {
    //     fn speak(&self) -> String { String::from("嘎嘎") }
    // }
    // let duck = Box::new(Duck { weight: 3.5 });
    // println!("{}", duck.weight); // 错误！Trait 对象只能访问 Trait 中的方法

    // 2. 返回具体类型时可以使用 impl Trait 语法
    fn create_speaker(animal: &str) -> impl Speak {
        if animal == "dog" {
            Dog { name: String::from("默认狗") }
        } else {
            Cat { name: String::from("默认猫") }
        }
    }

    let speaker = create_speaker("dog");
    println!("创建了一个 speaker: {}", speaker.speak());
    // 创建了一个 speaker: 默认狗 说: 汪汪！

    // impl Trait 在返回位置的使用
    // 注意：所有分支必须返回同一个具体类型
    // fn create_speaker2(animal: &str) -> impl Speak {
    //     if animal == "dog" {
    //         Dog { name: String::from("狗") } // 返回 Dog
    //     } else {
    //         Cat { name: String::from("猫") } // 返回 Cat
    //     }
    // } // 错误！Dog 和 Cat 是不同类型，不能用 impl Speak 返回
}
```

`Box<dyn Trait>` 是 Rust 实现运行时多态的核心工具。`dyn` 关键字明确表示这是一个"动态分发"的值——具体是哪种类型，要到运行时才能知道。背后的实现机制是虚表（vtable），每个实现了 Trait 的类型都有一个隐藏的 vtable 指针，指向它的方法实现。

> 动态分发虽然灵活，但有性能成本。每次方法调用都需要通过 vtable 查找实际的方法地址，这比静态分发（直接调用）要慢一些。不过，在大多数应用场景下，这个开销可以忽略不计。

### 6.2.3.2 &dyn Trait vs Box<dyn Trait>

`&dyn Trait` 和 `Box<dyn Trait>` 都可以存储实现了 Trait 的类型，但它们有重要区别。

```rust
fn main() {
    trait Draw {
        fn draw(&self) -> String;
    }

    struct Circle;
    struct Square;

    impl Draw for Circle {
        fn draw(&self) -> String {
            String::from("○")
        }
    }

    impl Draw for Square {
        fn draw(&self) -> String {
            String::from("□")
        }
    }

    // 方式1：&dyn Trait（引用）
    println!("&dyn Trait 方式:");
    let shapes: Vec<&dyn Draw> = vec![&Circle, &Square];

    for shape in &shapes {
        println!("  {}", shape.draw());
    }
    // ○
    // □

    // 方式2：Box<dyn Trait>（堆分配的所有权）
    println!("\nBox<dyn Trait> 方式:");
    let shapes: Vec<Box<dyn Draw>> = vec![Box::new(Circle), Box::new(Square)];

    for shape in shapes {
        println!("  {}", shape.draw());
    }
    // ○
    // □

    // 关键区别：
    println!("\n关键区别:");

    // &dyn Trait：引用，不拥有数据
    let circle = Circle;
    let dyn_ref: &dyn Draw = &circle;
    println!("  &dyn Trait 大小: {} 字节", std::mem::size_of_val(&dyn_ref));
    // &dyn Trait 占两个指针的大小（数据指针 + vtable 指针）

    // Box<dyn Trait>：拥有数据，在堆上
    let boxed_dyn: Box<dyn Draw> = Box::new(Circle);
    println!("  Box<dyn Trait> 栈大小: {} 字节", std::mem::size_of::<Box<dyn Draw>>());
    println!("  Box<dyn Trait> 堆大小: {}", std::mem::size_of::<Circle>());

    // 生命周期差异
    println!("\n生命周期差异:");

    // &dyn Trait 的生命周期
    fn use_trait_ref(animal: &dyn Draw) {
        println!("  {}", animal.draw());
    }

    let circle = Circle;
    use_trait_ref(&circle); // &circle 的生命周期被借用

    // Box<dyn Trait> 可以被传递和存储
    fn use_trait_box(animal: Box<dyn Draw>) {
        println!("  {}", animal.draw());
    }

    use_trait_box(Box::new(Square)); // Box 移动进函数

    // 何时使用哪种？
    println!("\n选择建议:");
    println!("  使用 &dyn Trait 当:");
    println!("    - 只是借用，不需要拥有权");
    println!("    - 数据已经存在于某个地方");
    println!("    - 不想承担堆分配的开销");
    println!();
    println!("  使用 Box<dyn Trait> 当:");
    println!("    - 需要拥有数据的所有权");
    println!("    - 需要把数据存储在集合中（Vec、HashMap 等）");
    println!("    - 需要在数据结构中存储不同类型的值");
    println!("    - 需要跨越作用域边界传递");

    // 实际应用场景
    println!("\n实际应用:");

    // GUI 系统中的组件
    trait UIComponent {
        fn render(&self);
        fn name(&self) -> &str;
    }

    struct Button {
        label: String,
    }

    struct TextField {
        placeholder: String,
    }

    impl UIComponent for Button {
        fn render(&self) { println!("[  {}  ]", self.label); }
        fn name(&self) -> &str { "Button" }
    }

    impl UIComponent for TextField {
        fn render(&self) { println!("[ {} ]", self.placeholder); }
        fn name(&self) -> &str { "TextField" }
    }

    // 存储不同类型的 UI 组件
    let components: Vec<Box<dyn UIComponent>> = vec![
        Box::new(Button { label: String::from("点击我") }),
        Box::new(TextField { placeholder: String::from("输入文字...") }),
        Box::new(Button { label: String::from("提交") }),
    ];

    println!("渲染 UI 组件:");
    for comp in &components {
        println!("  {}: ", comp.name());
        comp.render();
    }
}
```

`&dyn Trait` 和 `Box<dyn Trait>` 的选择取决于你是否需要拥有数据的所有权。如果只是借用，使用 `&dyn Trait` 更轻量；如果需要把数据存在集合中或传递到别处，使用 `Box<dyn Trait>`。

---

## 6.3 HashMap<K, V> 与 HashSet<T>

如果说 Vec 是"编号的储物柜"，那 HashMap 就是"带名字的储物柜"。Vec 用整数索引（0, 1, 2...）来访问元素，而 HashMap 用任意类型的键（Key）来访问值（Value）。

HashMap 是 Rust 标准库中用于存储键值对的核心数据结构。它通过哈希函数（Hash function）将键映射到桶（bucket）中，实现近乎 O(1) 的查找、插入和删除操作。

> 想象一下图书馆的图书检索系统。在 Vec 中，你需要知道书的编号才能找到它；但在 HashMap 中，你只需要知道书名（键），系统就会自动帮你找到对应的书架位置（值）。

### 6.3.1 创建与基本操作

#### 6.3.1.1 HashMap::new

创建 HashMap 的方式有多种，每种适合不同的场景。

```rust
fn main() {
    use std::collections::HashMap;

    // 方式1：new() 创建空的 HashMap
    let mut scores: HashMap<String, i32> = HashMap::new();

    // HashMap 需要显式引入，因为它是 std::collections 的一部分
    // Vec 和 Option 等是更常用的，所以它们在 prelude 中

    // 方式2：from() 从键值对数组创建
    let data = vec![
        ("Alice".to_string(), 95),
        ("Bob".to_string(), 87),
        ("Charlie".to_string(), 92),
    ];
    let scores_from_vec: HashMap<_, _> = HashMap::from(data);
    println!("从 Vec 创建: {:?}", scores_from_vec);
    // 从 Vec 创建: {"Alice": 95, "Bob": 87, "Charlie": 92}

    // 方式3：collect() 从迭代器收集
    let names = vec!["Apple", "Banana", "Apple", "Cherry", "Banana", "Apple"];
    let mut fruit_counts: HashMap<&str, i32> = HashMap::new();

    for name in names {
        // entry API 是处理"如果不存在则插入"的好方法
        // 后面会详细介绍
        fruit_counts.entry(name).or_insert(0);
        *fruit_counts.get_mut(name).unwrap() += 1;
    }

    println!("\n水果计数: {:?}", fruit_counts);
    // 水果计数: {"Apple": 3, "Banana": 2, "Cherry": 1}

    // 方式4：with_capacity() 预分配容量
    let mut large_map: HashMap<i32, String> = HashMap::with_capacity(10000);
    println!("\n预分配容量: {}", large_map.capacity()); // 预分配容量: 16384（或更大）

    // 预分配可以减少扩容开销
    // 当你大约知道需要存储多少元素时使用

    // insert 基本用法
    scores.insert(String::from("David"), 88);
    scores.insert(String::from("Eve"), 91);
    println!("\n插入后的分数: {:?}", scores);
    // 插入后的分数: {"David": 88, "Eve": 91}

    // 注意：HashMap 的键需要实现 Eq 和 Hash trait
    // 基本类型（i32, String, &str 等）都实现了这些 trait

    // 获取值
    match scores.get("David") {
        Some(score) => println!("David 的分数: {}", score), // David 的分数: 88
        None => println!("David 不存在"),
    }

    // get 返回 Option<&V>
    // 如果值不存在，返回 None
    match scores.get("Frank") {
        Some(score) => println!("Frank 的分数: {}", score),
        None => println!("Frank 不存在"), // Frank 不存在
    }

    // HashMap 的所有权规则
    println!("\n所有权规则:");

    // 对于实现了 Copy 的类型（如 i32），值会被拷贝
    let mut int_map: HashMap<String, i32> = HashMap::new();
    int_map.insert(String::from("x"), 10);
    let value = int_map.get("x").unwrap(); // value 是 &i32
    println!("获取的值: {}", value); // 10

    // 对于 String 这样的非 Copy 类型，HashMap 获得所有权
    let mut owned_map: HashMap<String, Vec<i32>> = HashMap::new();
    owned_map.insert(String::from("numbers"), vec![1, 2, 3]);

    // 下面的代码会出错，因为键和值都被 HashMap 拥有了
    // let key = String::from("numbers"); // 错误！key 已经被 HashMap 拥有
    // let value = vec![1, 2, 3]; // 错误！value 也被 HashMap 拥有

    // 如果你想借用，使用引用作为值
    let mut borrow_map: HashMap<&str, &Vec<i32>> = HashMap::new();
    let data = vec![1, 2, 3];
    borrow_map.insert("data", &data);
    println!("借用 map: {:?}", borrow_map);
    // 注意：data 必须保持有效，否则会出现悬垂引用
}
```

HashMap::new() 是最直接的创建方式，但它会创建一个空的 HashMap。标准库还提供了 `HashMap::from()` 和通过 `collect()` 从迭代器创建的方式。如果你大约知道需要存储多少元素，使用 `with_capacity()` 预分配可以减少后续扩容的开销。

#### 6.3.1.2 insert / get / contains_key

HashMap 的三大基础操作：插入、获取、检查是否存在。

```rust
fn main() {
    use std::collections::HashMap;

    let mut inventory: HashMap<&str, i32> = HashMap::new();

    // insert: 插入键值对
    println!("插入操作:");
    inventory.insert("apples", 5);
    inventory.insert("bananas", 3);
    inventory.insert("oranges", 8);

    println!("  库存: {:?}", inventory);
    // 库存: {"apples": 5, "bananas": 3, "oranges": 8}

    // insert 会返回被替换的旧值（如果存在）
    let old = inventory.insert("apples", 10);
    println!("  插入 'apples' = 10，旧值: {:?}", old);
    // 插入 'apples' = 10，旧值: Some(5)

    // 如果键不存在，insert 返回 None
    let old = inventory.insert("grapes", 15);
    println!("  插入 'grapes' = 15，旧值: {:?}", old);
    // 插入 'grapes' = 15，旧值: None

    // get: 获取值
    println!("\n获取操作:");

    match inventory.get("apples") {
        Some(count) => println!("  apples 有 {} 个", count), // apples 有 10 个
        None => println!("  apples 不存在"),
    }

    match inventory.get("mangoes") {
        Some(count) => println!("  mangoes 有 {} 个", count),
        None => println!("  mangoes 不存在"), // mangoes 不存在
    }

    // get 返回 &V，是借用的引用
    // HashMap 不会转移值的所有权给你

    // 常见的"先检查后获取"模式
    let key = "bananas";
    if inventory.contains_key(key) {
        // 两次查找，效率稍低
        let count = inventory.get(key).unwrap();
        println!("  {} 存在，数量是 {}", key, count);
    } else {
        println!("  {} 不存在", key);
    }

    // contains_key: 检查键是否存在
    println!("\n检查键是否存在:");
    println!("  包含 'apples'? {}", inventory.contains_key("apples")); // true
    println!("  包含 'mangoes'? {}", inventory.contains_key("mangoes")); // false

    // 小技巧：使用 get_mut 获取可变引用并修改
    println!("\n使用 get_mut 修改:");
    if let Some(count) = inventory.get_mut("oranges") {
        *count += 10; // 直接修改，不需要再次查找
    }
    println!("  oranges 现在有 {} 个", inventory.get("oranges").unwrap()); // oranges 现在有 18 个

    // 批量操作：from_iter
    println!("\n批量创建:");
    let pairs = vec![
        ("one", 1),
        ("two", 2),
        ("three", 3),
    ];
    let map: HashMap<_, _> = pairs.into_iter().collect();
    println!("  {:?}", map);
    // {"one": 1, "two": 2, "three": 3}

    // 扩展已有 HashMap
    let mut map1 = HashMap::from([("a", 1), ("b", 2)]);
    let map2 = HashMap::from([("c", 3), ("d", 4)]);
    map1.extend(map2);
    println!("  合并后: {:?}", map1);
    // {"a": 1, "b": 2, "c": 3, "d": 4}

    // 实际应用：词频统计
    println!("\n词频统计:");
    let text = "hello world hello rust hello world rust programming rust coding";

    let mut word_count: HashMap<&str, i32> = HashMap::new();

    for word in text.split_whitespace() {
        let count = word_count.entry(word).or_insert(0);
        *count += 1;
    }

    println!("  文本: \"{}\"", text);
    println!("  词频: {:?}", word_count);
    // {"hello": 3, "world": 2, "rust": 3, "programming": 1, "coding": 1}
}
```

HashMap 的 insert、get、contains_key 是最常用的三个操作。insert 会覆盖已存在的值并返回旧值；get 返回 `Option<&V>`；contains_key 返回布尔值。注意，get 返回的是借用引用，不会获取值的所有权。

#### 6.3.1.3 remove

HashMap 的 remove 操作用于删除键值对。

```rust
fn main() {
    use std::collections::HashMap;

    let mut scores: HashMap<&str, i32> = HashMap::new();
    scores.insert(String::from("Alice"), 95);
    scores.insert(String::from("Bob"), 87);
    scores.insert(String::from("Charlie"), 92);

    println!("原始分数: {:?}", scores);
    // 原始分数: {"Alice": 95, "Bob": 87, "Charlie": 92}

    // remove: 删除键值对，返回被删除的值
    let removed = scores.remove("Bob");
    println!("\n删除 'Bob'，返回值: {:?}", removed);
    // 删除 'Bob'，返回值: Some(87)

    println!("删除后: {:?}", scores);
    // 删除后: {"Alice": 95, "Charlie": 92}

    // 删除不存在的键，返回 None
    let removed = scores.remove("David");
    println!("删除 'David'，返回值: {:?}", removed);
    // 删除 'David'，返回值: None

    // remove_if_exists（实际就是 remove，但可以这样理解）
    let key = "Alice";
    if let Some(value) = scores.remove(key) {
        println!("删除了 {} = {}", key, value);
    } else {
        println!("{} 不存在", key);
    }

    println!("最终: {:?}", scores);
    // 最终: {"Charlie": 92}

    // 一次性清空 HashMap
    let mut map: HashMap<i32, &str> = HashMap::new();
    map.insert(1, "one");
    map.insert(2, "two");
    map.insert(3, "three");

    println!("\n清空前: {:?}", map);
    map.clear();
    println!("清空后: {:?}", map);
    // 清空后: {}

    // drain: 批量删除并返回迭代器
    let mut map: HashMap<&str, i32> = HashMap::new();
    map.insert("a", 1);
    map.insert("b", 2);
    map.insert("c", 3);

    println!("\nDrain 操作:");
    println!("  drain 前: {:?}", map);

    let drained: Vec<(_, _)> = map.drain().collect();
    println!("  抽出的元素: {:?}", drained);
    // [("a", 1), ("b", 2), ("c", 3)]

    println!("  drain 后: {:?}", map);
    // drain 后: {}

    // 保留符合条件的元素
    let mut ages: HashMap<&str, i32> = HashMap::new();
    ages.insert("Alice", 25);
    ages.insert("Bob", 15);
    ages.insert("Charlie", 30);
    ages.insert("David", 17);

    println!("\n保留年龄 >= 18 的:");
    println!("  原始: {:?}", ages);

    ages.retain(|_name, &mut age| age >= 18);
    println!("  保留后: {:?}", ages);
    // {"Alice": 25, "Charlie": 30}

    // HashMap 的性能
    println!("\n性能考虑:");
    let mut map: HashMap<i32, i32> = HashMap::new();

    // insert 平均 O(1)
    let start = std::time::Instant::now();
    for i in 0..10000 {
        map.insert(i, i * 2);
    }
    println!("  10000 次 insert: {:?}", start.elapsed());

    // get 平均 O(1)
    let start = std::time::Instant::now();
    for i in 0..10000 {
        map.get(&i);
    }
    println!("  10000 次 get: {:?}", start.elapsed());

    // remove O(1)
    let start = std::time::Instant::now();
    for i in 0..10000 {
        map.remove(&i);
    }
    println!("  10000 次 remove: {:?}", start.elapsed());
}
```

HashMap 的 remove 操作是 O(1) 平均时间复杂度（哈希表的经典保证）。drain 方法特别有用，它可以让你遍历并删除所有元素，常用于需要处理完所有数据后清空的场景。

### 6.3.2 Entry API

Entry API 是 HashMap 提供的一个强大工具，用于处理"键可能存在也可能不存在"的情况。它避免了先检查再操作的两次查找。

#### 6.3.2.1 Entry enum

Entry 代表 HashMap 中一个键的存在与否的状态。

```rust
fn main() {
    use std::collections::HashMap;

    let mut scores: HashMap<&str, i32> = HashMap::new();

    // entry() 返回一个 Entry 枚举
    // Vacant 表示键不存在，Occupied 表示键存在
    let entry = scores.entry("Alice");

    println!("Entry 类型: {:?}", entry);
    // Entry 类型: Vacant(Entry { key: "Alice", ... })

    // Entry 的变体
    println!("\nEntry 枚举的两种状态:");

    // VacantEntry - 键不存在时的入口
    scores.entry("Bob").or_insert(0);
    println!("  插入 Bob: {:?}", scores);
    // {"Bob": 0}

    // OccupiedEntry - 键已存在时的入口
    scores.entry("Bob").or_insert(100); // Bob 已存在，所以不会改变
    println!("  Bob 不变: {:?}", scores);
    // {"Bob": 0}

    // 演示 Vacant 和 Occupied
    let mut map: HashMap<&str, Vec<i32>> = HashMap::new();

    // 第一次插入：键不存在，创建新的 Vec
    map.entry("primes").or_insert_with(Vec::new).push(2);
    map.entry("primes").or_insert_with(Vec::new).push(3);
    map.entry("primes").or_insert_with(Vec::new).push(5);

    // 第二次插入：键存在，直接使用已有的 Vec
    map.entry("evens").or_insert_with(Vec::new).push(2);
    map.entry("evens").or_insert_with(Vec::new).push(4);

    println!("\n分组数据: {:?}", map);
    // {"primes": [2, 3, 5], "evens": [2, 4]}

    // 使用 and_modify 进行条件修改
    println!("\nand_modify 示例:");
    let mut counter: HashMap<&str, i32> = HashMap::new();
    counter.entry("visits").and_modify(|c| *c += 1).or_insert(1);

    println!("  第一次访问: {:?}", counter.get("visits")); // Some(1)

    counter.entry("visits").and_modify(|c| *c += 1).or_insert(1);
    println!("  第二次访问: {:?}", counter.get("visits")); // Some(2)

    counter.entry("visits").and_modify(|c| *c += 1).or_insert(1);
    println!("  第三次访问: {:?}", counter.get("visits")); // Some(3)

    // Entry 的 and_modify 和 or_insert 组合
    println!("\n组合使用:");
    let mut staff: HashMap<&str, Vec<&str>> = HashMap::new();

    // 如果部门不存在，创建并添加员工；如果存在，追加员工
    staff.entry("Engineering").or_insert_with(Vec::new).push("Alice");
    staff.entry("Engineering").or_insert_with(Vec::new).push("Bob");
    staff.entry("Marketing").or_insert_with(Vec::new).push("Charlie");

    println!("  {:?}", staff);
    // {"Engineering": ["Alice", "Bob"], "Marketing": ["Charlie"]}

    // 获取并修改
    println!("\n获取并修改:");
    let mut scores: HashMap<&str, i32> = HashMap::new();
    scores.insert(String::from("TeamA"), 100);

    // 修改已存在的值
    scores.entry("TeamA").and_modify(|score| *score += 50);
    println!("  TeamA 加 50 后: {:?}", scores.get("TeamA")); // Some(150)

    // 如果不存在，插入新值
    scores.entry("TeamB").and_modify(|score| *score += 50).or_insert(0);
    println!("  TeamB: {:?}", scores.get("TeamB")); // Some(0)
}
```

Entry API 的精髓在于：它让你在一次操作中同时处理"键存在"和"键不存在"两种情况，而不需要两次查找。这不仅代码更简洁，也避免了竞态条件（如果你在检查和插入之间有其他线程修改了 map）。

#### 6.3.2.2 or_insert

or_insert 是 Entry 最常用的方法之一：如果键不存在，插入默认值；如果存在，返回可变引用。

```rust
fn main() {
    use std::collections::HashMap;

    // or_insert: 如果键不存在，插入默认值；如果存在，返回可变引用
    let mut map: HashMap<&str, i32> = HashMap::new();

    // 键不存在，插入默认值 0
    let value = map.entry("score").or_insert(0);
    println!("第一次 or_insert: {}", value); // 0
    *value += 1; // 修改它
    println!("修改后: {:?}", map); // {"score": 1}

    // 键已存在，or_insert 不起作用，直接返回可变引用
    let value = map.entry("score").or_insert(100); // 100 不会被插入
    *value += 1;
    println!("再次 or_insert: {:?}", map); // {"score": 2}

    // 实际应用：统计词频
    println!("\n词频统计:");
    let text = "the quick brown fox jumps over the lazy dog the fox";

    let mut word_count: HashMap<&str, i32> = HashMap::new();

    for word in text.split_whitespace() {
        // 每次遇到单词，计数加 1
        *word_count.entry(word).or_insert(0) += 1;
    }

    println!("  文本: \"{}\"", text);
    println!("  词频: {:?}", word_count);
    // {"the": 2, "quick": 1, "brown": 1, "fox": 2, "jumps": 1, ...}

    // or_insert 用于初始化计数器
    println!("\n计数器初始化:");
    let mut votes: HashMap<&str, i32> = HashMap::new();

    // 记录投票
    fn record_vote(votes: &mut HashMap<&str, i32>, candidate: &str) {
        *votes.entry(candidate).or_insert(0) += 1;
    }

    record_vote(&mut votes, "Alice");
    record_vote(&mut votes, "Bob");
    record_vote(&mut votes, "Alice");
    record_vote(&mut votes, "Alice");
    record_vote(&mut votes, "Charlie");

    println!("  投票结果: {:?}", votes);
    // {"Alice": 3, "Bob": 1, "Charlie": 1}

    // or_insert 用于分组
    println!("\n分组数据:");
    let data = vec![
        ("fruit", "apple"),
        ("fruit", "banana"),
        ("vegetable", "carrot"),
        ("fruit", "orange"),
        ("vegetable", "broccoli"),
    ];

    let mut groups: HashMap<&str, Vec<&str>> = HashMap::new();

    for (category, item) in data {
        groups.entry(category).or_insert_with(Vec::new).push(item);
    }

    println!("  {:?}", groups);
    // {"fruit": ["apple", "banana", "orange"], "vegetable": ["carrot", "broccoli"]}

    // or_insert vs or_insert_with
    // or_insert 接受一个值，适合 Copy 类型
    // or_insert_with 接受一个闭包，适合需要计算默认值的场景
}
```

or_insert 是处理"计数"场景的完美工具。它让"如果不存在则初始化为 0，然后加 1"这样的常见操作变得异常简洁。

#### 6.3.2.3 or_insert_with

or_insert_with 与 or_insert 类似，但接受一个闭包来生成默认值。这在你需要"按需计算"默认值时很有用。

```rust
fn main() {
    use std::collections::HashMap;

    // or_insert_with：接受一个闭包，按需计算默认值
    let mut map: HashMap<&str, Vec<i32>> = HashMap::new();

    // 使用 or_insert_with，因为 Vec 需要用 new() 创建
    map.entry("numbers").or_insert_with(Vec::new).push(1);
    map.entry("numbers").or_insert_with(Vec::new).push(2);
    map.entry("numbers").or_insert_with(Vec::new).push(3);

    println!("numbers: {:?}", map.get("numbers"));
    // numbers: Some([1, 2, 3])

    // or_insert vs or_insert_with 的区别
    println!("\n区别:");

    // or_insert 每次调用都会复制值（即使是 unused）
    let mut h1: HashMap<&str, String> = HashMap::new();
    h1.entry("key").or_insert(String::from("default")); // 总是创建 String

    // or_insert_with 只在需要时才调用闭包
    let mut h2: HashMap<&str, Vec<i32>> = HashMap::new();
    // h2.entry("key").or_insert(vec![1, 2, 3]); // 总是创建 Vec，即使不需要
    h2.entry("key").or_insert_with(|| vec![1, 2, 3]); // 只在需要时创建

    // 实际应用：缓存计算结果
    println!("\n缓存示例:");
    let mut cache: HashMap<i32, i32> = HashMap::new();

    fn expensive_calculation(n: i32) -> i32 {
        // 模拟耗时计算
        println!("  计算 {}...", n);
        std::thread::sleep(std::time::Duration::from_millis(10));
        n * n
    }

    fn get_cached(n: i32, cache: &mut HashMap<i32, i32>) -> i32 {
        *cache.entry(n).or_insert_with(|| expensive_calculation(n))
    }

    let mut c = HashMap::new();
    println!("  第一次: {}", get_cached(10, &mut c));
    println!("  第二次: {}", get_cached(10, &mut c)); // 使用缓存，不计算
    println!("  3^2: {}", get_cached(3, &mut c));

    // or_insert_with 的延迟计算优势
    println!("\n延迟计算优势:");
    let mut map: HashMap<&str, String> = HashMap::new();

    // 假设默认值需要复杂的计算
    fn compute_default() -> String {
        println!("    计算默认值的耗时操作...");
        String::from("computed")
    }

    // 只在需要时才计算
    map.entry("lazy").or_insert_with(compute_default);
    println!("  插入 'lazy' 后");

    map.entry("eager").or_insert_with(compute_default);
    println!("  插入 'eager' 后");

    // or_insert_with 在键已存在时不会调用闭包
    // 所以 compute_default 只被调用了一次

    // and_modify 可以与 or_insert_with 组合
    println!("\nand_modify + or_insert_with:");
    let mut settings: HashMap<&str, Vec<i32>> = HashMap::new();

    // 如果键不存在，插入 [0]；如果存在，给第一个元素加 10
    settings.entry("attempts").and_modify(|v| v[0] += 10).or_insert_with(|| vec![0]);

    println!("  第一次: {:?}", settings.get("attempts")); // Some([0])

    settings.entry("attempts").and_modify(|v| v[0] += 10).or_insert_with(|| vec![0]);
    println!("  第二次: {:?}", settings.get("attempts")); // Some([10])

    settings.entry("attempts").and_modify(|v| v[0] += 10).or_insert_with(|| vec![0]);
    println!("  第三次: {:?}", settings.get("attempts")); // Some([20])
}
```

or_insert_with 的优势在于"延迟计算"——只有当键真正不存在时，闭包才会被执行。这在你需要生成复杂默认值时非常有用，可以避免不必要的计算开销。

### 6.3.3 HashSet<T>

HashSet<T> 实际上就是一个只有键没有值的 HashMap<K, V>。它用于存储唯一值（不重复）的集合。

#### 6.3.3.1 HashSet 创建

HashSet 的创建方式与 HashMap 类似。

```rust
fn main() {
    use std::collections::HashSet;

    // HashSet 只存储唯一的值
    let mut fruits: HashSet<&str> = HashSet::new();

    // insert 添加元素
    fruits.insert("apple");
    fruits.insert("banana");
    fruits.insert("orange");

    println!("水果集合: {:?}", fruits);
    // {"banana", "orange", "apple"} (顺序不保证)

    // from 使用数组创建
    let numbers: HashSet<i32> = HashSet::from([1, 2, 3, 4, 5]);
    println!("数字集合: {:?}", numbers);

    // collect 从迭代器创建
    let data = vec!["a", "b", "a", "c", "b", "d"];
    let unique: HashSet<_> = data.iter().collect();
    println!("去重后: {:?}", unique);
    // {"a", "b", "c", "d"}

    // with_capacity 预分配
    let mut large: HashSet<i32> = HashSet::with_capacity(1000);
    for i in 0..100 {
        large.insert(i);
    }
    println!("预分配集合大小: {}", large.capacity());

    // HashSet 的特点：无序、唯一
    println!("\nHashSet 特点:");
    let s1: HashSet<i32> = HashSet::from([1, 2, 3, 4, 5]);
    let s2: HashSet<i32> = HashSet::from([3, 4, 5, 6, 7]);

    println!("  s1 = {:?}", s1);
    println!("  s2 = {:?}", s2);

    // 插入重复元素不会生效
    let mut set: HashSet<i32> = HashSet::new();
    set.insert(1);
    set.insert(1);
    set.insert(1);
    println!("\n插入三次 1: {:?}", set);
    // {1} - 只有一个元素

    // 基本操作
    println!("\n基本操作:");
    let mut set = HashSet::new();
    set.insert(10);
    set.insert(20);
    set.insert(30);

    println!("  contains 30? {}", set.contains(&30)); // true
    println!("  contains 40? {}", set.contains(&40)); // false

    println!("  len: {}", set.len()); // 3
    println!("  is_empty: {}", set.is_empty()); // false

    set.remove(&20);
    println!("  remove 20 后: {:?}", set);
    // {10, 30}

    // 迭代
    println!("\n迭代:");
    let set: HashSet<i32> = HashSet::from([1, 2, 3]);
    for val in &set {
        println!("  {}", val);
    }
}
```

HashSet 本质上就是 `HashMap<T, ()>`——一个只有键没有值的哈希表。这使得每个键都是唯一的，自动去重。

#### 6.3.3.2 集合运算

HashSet 支持丰富的集合运算：交集、并集、差集、对称差。

```rust
fn main() {
    use std::collections::HashSet;

    let a: HashSet<i32> = HashSet::from([1, 2, 3, 4, 5]);
    let b: HashSet<i32> = HashSet::from([4, 5, 6, 7, 8]);

    println!("集合 A: {:?}", a);
    println!("集合 B: {:?}", b);
    // 集合 A: {1, 2, 3, 4, 5}
    // 集合 B: {4, 5, 6, 7, 8}

    // 交集：A ∩ B（既在 A 又在 B 的元素）
    let intersection: HashSet<_> = a.intersection(&b).collect();
    println!("\n交集 A ∩ B: {:?}", intersection);
    // {4, 5}

    // 并集：A ∪ B（A 或 B 中的所有元素）
    let union: HashSet<_> = a.union(&b).collect();
    println!("并集 A ∪ B: {:?}", union);
    // {1, 2, 3, 4, 5, 6, 7, 8}

    // 差集：A - B（在 A 但不在 B 的元素）
    let difference: HashSet<_> = a.difference(&b).collect();
    println!("差集 A - B: {:?}", difference);
    // {1, 2, 3}

    // 对称差集：A △ B（在 A 或 B 但不同时在两者的元素）
    let symmetric_diff: HashSet<_> = a.symmetric_difference(&b).collect();
    println!("对称差集 A △ B: {:?}", symmetric_diff);
    // {1, 2, 3, 6, 7, 8}

    // 检查子集关系
    println!("\n子集关系:");
    let small: HashSet<i32> = HashSet::from([1, 2, 3]);
    let large: HashSet<i32> = HashSet::from([1, 2, 3, 4, 5]);

    println!("  {{1,2,3}} 是 {{1,2,3,4,5}} 的子集? {}", small.is_subset(&large)); // true
    println!("  {{1,2,3,4,5}} 是 {{1,2,3}} 的子集? {}", large.is_subset(&small)); // false

    println!("  {{1,2,3}} 是 {{1,2,3,4,5}} 的超集? {}", large.is_superset(&small)); // true

    // 检查交集是否为空
    let set1: HashSet<i32> = HashSet::from([1, 2, 3]);
    let set2: HashSet<i32> = HashSet::from([4, 5, 6]);

    println!("\n{{1,2,3}} 和 {{4,5,6}} 有交集? {}", !set1.is_disjoint(&set2));
    // false

    let set3: HashSet<i32> = HashSet::from([3, 4, 5]);
    println!("{{1,2,3}} 和 {{3,4,5}} 有交集? {}", !set1.is_disjoint(&set3));
    // true

    // 修改操作
    println!("\n修改操作:");

    // 清除所有元素
    let mut set: HashSet<i32> = HashSet::from([1, 2, 3]);
    set.clear();
    println!("  clear 后: {:?}", set);
    // {}

    // 保留在另一个集合中的元素
    let mut set1: HashSet<i32> = HashSet::from([1, 2, 3, 4, 5]);
    let set2: HashSet<i32> = HashSet::from([3, 4, 5, 6, 7]);

    set1.retain(|x| set2.contains(x));
    println!("  retain 后的 set1: {:?}", set1);
    // {3, 4, 5}

    // 实际应用：找出数组中的唯一值
    println!("\n实际应用 - 去重:");
    let nums = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5];
    let unique: Vec<i32> = nums.into_iter().collect::<HashSet<_>>().into_iter().collect();
    println!("  原始: [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]");
    println!("  去重: {:?}", unique);
    // [1, 2, 3, 4, 5]

    // 实际应用：找出两篇文章的共同词
    println!("\n共同词:");
    let article1_words = vec!["rust", "programming", "memory", "safety", "performance"];
    let article2_words = vec!["rust", "safety", "concurrency", "threads", "performance"];

    let set1: HashSet<_> = article1_words.iter().collect();
    let set2: HashSet<_> = article2_words.iter().collect();

    let common: HashSet<_> = set1.intersection(&set2).collect();
    println!("  文章1: {:?}", article1_words);
    println!("  文章2: {:?}", article2_words);
    println!("  共同词: {:?}", common);
    // {"rust", "safety", "performance"}
}
```

HashSet 的集合运算是处理"去重"、"找共同点"、"找不同点"等问题的利器。在数据处理、文本分析、权限管理等场景中非常有用。

### 6.3.4 BTreeMap<K, V> 与 BTreeSet<T>

BTreeMap 和 BTreeSet 是 HashMap 和 HashSet 的"有序版本"。它们使用平衡二叉搜索树（实际上是 B 树）来存储数据，保持键的有序排列。

#### 6.3.4.1 有序版本

当你需要按顺序遍历数据时，BTreeMap 和 BTreeSet 是更好的选择。

```rust
fn main() {
    use std::collections::{BTreeMap, BTreeSet};

    // BTreeMap：按键排序的键值对
    println!("BTreeMap:");
    let mut scores: BTreeMap<&str, i32> = BTreeMap::new();

    scores.insert("Charlie", 92);
    scores.insert("Alice", 95);
    scores.insert("Bob", 87);

    println!("  按键排序: {:?}", scores);
    // {"Alice": 95, "Bob": 87, "Charlie": 92}

    // BTreeSet：按键排序的唯一值集合
    println!("\nBTreeSet:");
    let mut set: BTreeSet<i32> = BTreeSet::new();

    set.insert(30);
    set.insert(10);
    set.insert(50);
    set.insert(20);
    set.insert(40);

    println!("  按值排序: {:?}", set);
    // {10, 20, 30, 40, 50}

    // 有序迭代
    println!("\n有序迭代:");
    let set: BTreeSet<i32> = BTreeSet::from([5, 3, 1, 4, 2]);
    for val in &set {
        print!("{} ", val);
    }
    println!();
    // 1 2 3 4 5

    // 范围查询
    println!("\n范围查询:");
    let set: BTreeSet<i32> = (1..=10).collect();

    println!("  1..5: {:?}", set.range(1..5).collect::<Vec<_>>());
    // [1, 2, 3, 4]

    println!("  5..: {:?}", set.range(5..).collect::<Vec<_>>());
    // [5, 6, 7, 8, 9, 10]

    println!("  ..=5: {:?}", set.range(..=5).collect::<Vec<_>>());
    // [1, 2, 3, 4, 5]

    // BTreeMap 的 first_entry 和 last_entry
    println!("\n首尾元素:");
    let mut map: BTreeMap<&str, i32> = BTreeMap::from([
        ("a", 1),
        ("b", 2),
        ("c", 3),
    ]);

    if let Some((k, v)) = map.first_key_value() {
        println!("  第一个: {} = {}", k, v); // a = 1
    }

    if let Some((k, v)) = map.last_key_value() {
        println!("  最后一个: {} = {}", k, v); // c = 3
    }

    // HashMap vs BTreeMap
    println!("\nHashMap vs BTreeMap:");
    println!("  HashMap:");
    println!("    - 查找 O(1)，无序");
    println!("    - 适合快速查找，不需要顺序遍历");
    println!("    - 键需要实现 Hash trait");
    println!();
    println!("  BTreeMap:");
    println!("    - 查找 O(log n)，有序");
    println!("    - 适合需要顺序遍历的场景");
    println!("    - 键需要实现 Ord trait（比较）");

    // 实际应用：排行榜
    println!("\n排行榜（有序）:");
    let mut leaderboard: BTreeMap<i32, Vec<&str>> = BTreeMap::new();

    // 按分数（键）排序，分数高的在前
    leaderboard.insert(95, vec!["Alice"]);
    leaderboard.insert(87, vec!["Bob", "Charlie"]);
    leaderboard.insert(92, vec!["David"]);

    println!("  排名:");
    for (score, names) in leaderboard.iter().rev() {
        println!("    {} 分: {:?}", score, names);
    }
    // 95 分: ["Alice"]
    // 92 分: ["David"]
    // 87 分: ["Bob", "Charlie"]

    // 实际应用：区间查找
    println!("\n区间查找:");
    let mut ranges: BTreeMap<i32, i32> = BTreeMap::new();
    ranges.insert(0, 10);   // 0-9
    ranges.insert(10, 20);  // 10-19
    ranges.insert(20, 30);  // 20-29

    // 找 15 在哪个区间
    let point = 15;
    if let Some((&start, &end)) = ranges.range(..=point).last() {
        if point < end {
            println!("  {} 在区间 [{}-{}]", point, start, end - 1);
        }
    }
}
```

BTreeMap 和 BTreeSet 在需要"有序"操作的场景中非常有用。虽然查找比 HashMap 慢（O(log n) vs O(1)），但它们提供了有序迭代、范围查询等 HashMap 没有的功能。

---

## 6.4 链表与树

Rust 标准库提供了 `LinkedList<T>` 和多种树结构。虽然这些在日常编程中不如 Vec 和 HashMap 常用，但了解它们有助于理解 Rust 集合库的设计。

### 6.4.1 LinkedList<T>

Rust 的 `std::collections::LinkedList<T>` 是一个双向链表，每个节点包含值和指向前后节点的指针。

```rust
fn main() {
    use std::collections::LinkedList;

    // 创建链表
    let mut list: LinkedList<i32> = LinkedList::new();
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);

    println!("链表: {:?}", list);
    // 链表: [1, 2, 3]

    // push_front 在头部插入
    list.push_front(0);
    println!("push_front(0): {:?}", list);
    // [0, 1, 2, 3]

    // pop_front 从头部删除
    if let Some(v) = list.pop_front() {
        println!("pop_front: {}", v); // 0
    }
    println!("pop_front 后: {:?}", list);
    // [1, 2, 3]

    // push_back / pop_back
    list.push_back(4);
    list.push_back(5);
    println!("push_back 4, 5: {:?}", list);
    // [1, 2, 3, 4, 5]

    // 迭代器
    println!("\n迭代:");
    for item in &list {
        print!("{} ", item);
    }
    println!();

    // 双向迭代
    println!("反向迭代:");
    for item in list.iter().rev() {
        print!("{} ", item);
    }
    println!();

    // 基本操作
    println!("\n基本操作:");
    let mut list: LinkedList<&str> = LinkedList::new();
    list.push_front("world");
    list.push_front("hello");

    println!("  len: {}", list.len()); // 2
    println!("  is_empty: {}", list.is_empty()); // false

    // front / back
    println!("  front: {:?}", list.front()); // Some("hello")
    println!("  back: {:?}", list.back()); // Some("world")

    // 转换为 Vec
    let vec: Vec<_> = list.into_iter().collect();
    println!("  转换为 Vec: {:?}", vec);
    // ["hello", "world"]

    // LinkedList vs Vec
    println!("\nLinkedList vs Vec:");
    println!("  LinkedList:");
    println!("    - 插入/删除 O(1)（已知位置）");
    println!("    - 不支持随机访问 O(1)");
    println!("    - 节点在内存中不连续");
    println!("    - 每个节点有额外的指针开销");
    println!();
    println!("  Vec:");
    println!("    - 插入/删除 O(n)（中间位置）");
    println!("    - 随机访问 O(1)");
    println!("    - 元素在内存中连续（缓存友好）");
    println!("    - 无额外指针开销");

    // 什么时候用 LinkedList？
    println!("\n何时使用 LinkedList:");
    println!("  - 需要 O(1) 的头部/尾部插入删除");
    println!("  - 需要频繁合并、拆分链表");
    println!("  - 数据结构本身是链表（如文件系统）");
    println!("  - 大多数情况下，Vec 是更好的选择");

    // 实际应用：实现栈
    println!("\n用 LinkedList 实现栈:");
    struct Stack<T> {
        data: LinkedList<T>,
    }

    impl<T> Stack<T> {
        fn new() -> Self {
            Stack { data: LinkedList::new() }
        }

        fn push(&mut self, item: T) {
            self.data.push_front(item);
        }

        fn pop(&mut self) -> Option<T> {
            self.data.pop_front()
        }

        fn peek(&self) -> Option<&T> {
            self.data.front()
        }

        fn is_empty(&self) -> bool {
            self.data.is_empty()
        }

        fn len(&self) -> usize {
            self.data.len()
        }
    }

    let mut stack = Stack::new();
    stack.push(1);
    stack.push(2);
    stack.push(3);

    println!("  栈: {:?}", stack.len()); // 3
    println!("  peek: {:?}", stack.peek()); // Some(3)

    while let Some(v) = stack.pop() {
        print!("{} ", v);
    }
    println!(); // 3 2 1
}
```

LinkedList 在 Rust 中不像在 C/C++ 中那样常用，因为 Vec 在大多数场景下性能更好。但 LinkedList 仍然有其用武之地，特别是在需要频繁在头部插入/删除，或者需要将链表合并/拆分的场景中。

## 6.5 其他集合类型

除了我们详细介绍的 Vec、HashMap、LinkedList，Rust 标准库还提供了其他一些有用的集合类型。

### 6.5.1 VecDeque<T>

VecDeque<T> 是"双端队列"（double-ended queue）的实现。它是一种两端都可以高效插入和删除的序列。

```rust
fn main() {
    use std::collections::VecDeque;

    // 创建 VecDeque
    let mut deque: VecDeque<i32> = VecDeque::new();

    // 从 VecDeque 创建
    let deque: VecDeque<_> = (1..=5).collect();
    println!("VecDeque: {:?}", deque);
    // VecDeque([1, 2, 3, 4, 5])

    // 从前面插入/删除（O(1)）
    let mut deque = VecDeque::new();
    deque.push_front(1);
    deque.push_front(0);
    println!("push_front 后: {:?}", deque);
    // [0, 1]

    deque.push_back(2);
    deque.push_back(3);
    println!("push_back 后: {:?}", deque);
    // [0, 1, 2, 3]

    // 从前面/后面弹出
    if let Some(v) = deque.pop_front() {
        println!("pop_front: {}", v); // 0
    }
    println!("pop_front 后: {:?}", deque);
    // [1, 2, 3]

    if let Some(v) = deque.pop_back() {
        println!("pop_back: {}", v); // 3
    }
    println!("pop_back 后: {:?}", deque);
    // [1, 2]

    // VecDeque vs Vec
    println!("\nVecDeque vs Vec:");
    println!("  VecDeque:");
    println!("    - 两端操作 O(1)");
    println!("    - 内部是环形缓冲区");
    println!("    - 比 Vec 稍微复杂一点");
    println!();
    println!("  Vec:");
    println!("    - 尾部操作 O(1)");
    println!("    - 头部操作 O(n)");
    println!("    - 简单高效");

    // 实际应用：滑动窗口
    println!("\n滑动窗口示例:");
    let data = vec![1, 3, -1, -3, 5, 3, 6, 7];
    let window_size = 3;

    let mut window = VecDeque::new();
    let mut results = Vec::new();

    for (i, &num) in data.iter().enumerate() {
        // 移除窗口外的元素
        while let Some(&idx) = window.front() {
            if idx <= i.saturating_sub(window_size) {
                window.pop_front();
            } else {
                break;
            }
        }

        // 维护窗口内的最大值索引
        while let Some(&idx) = window.back() {
            if data[idx] <= num {
                window.pop_back();
            } else {
                break;
            }
        }

        window.push_back(i);

        // 窗口形成后记录结果
        if i >= window_size - 1 {
            results.push(data[*window.front().unwrap()]);
        }
    }

    println!("  数据: {:?}", data);
    println!("  窗口大小: {}", window_size);
    println!("  每窗口最大值: {:?}", results);
    // [3, 3, 5, 5, 6, 7]

    // 实际应用：工作队列
    println!("\n工作队列示例:");
    #[derive(Debug)]
    struct Task {
        id: u32,
        name: String,
    }

    let mut queue: VecDeque<Task> = VecDeque::new();

    // 添加任务
    queue.push_back(Task { id: 1, name: String::from("下载") });
    queue.push_back(Task { id: 2, name: String::from("处理") });
    queue.push_back(Task { id: 3, name: String::from("上传") });

    // 优先处理某些任务
    queue.push_front(Task { id: 4, name: String::from("紧急任务") });

    println!("  任务队列:");
    while let Some(task) = queue.pop_front() {
        println!("    处理: {:?}", task);
    }
    // 处理: Task { id: 4, name: "紧急任务" }
    // 处理: Task { id: 1, name: "下载" }
    // ...

    // 容量操作
    println!("\n容量操作:");
    let mut deque: VecDeque<i32> = VecDeque::with_capacity(10);
    println!("  capacity: {}", deque.capacity()); // 10

    deque.push_back(1);
    deque.push_back(2);
    println!("  len: {}, capacity: {}", deque.len(), deque.capacity());

    // drain
    let mut deque: VecDeque<_> = (1..=5).collect();
    let drained: Vec<_> = deque.drain(1..4).collect();
    println!("  drain(1..4): {:?}", drained);
    println!("  drain 后: {:?}", deque);
    // [1, 5]
}
```

VecDeque 是实现"队列"和"工作队列"的理想数据结构。如果你需要从两端高效添加和删除元素，VecDeque 比 LinkedList 更高效（因为它是连续的内存）。

### 6.5.2 BinaryHeap<T>

BinaryHeap<T> 是一个最大堆（默认情况下），它保证最大的元素总是在堆顶。

```rust
fn main() {
    use std::collections::BinaryHeap;

    // 创建 BinaryHeap
    let mut heap: BinaryHeap<i32> = BinaryHeap::new();

    // push 添加元素
    heap.push(3);
    heap.push(1);
    heap.push(4);
    heap.push(1);
    heap.push(5);

    println!("Heap: {:?}", heap);
    // Heap: [5, 4, 3, 1, 1]

    // pop 获取并移除最大元素
    println!("\nPop 操作:");
    while let Some(max) = heap.pop() {
        print!("{} ", max);
    }
    println!();
    // 5 4 3 1 1

    // peek 查看最大元素（不移除）
    let mut heap: BinaryHeap<_> = (1..=10).rev().collect();
    println!("\nPeek: {:?}", heap.peek()); // Some(10)

    // BinaryHeap 是最大堆
    println!("\n最大堆 vs 最小堆:");
    let mut max_heap: BinaryHeap<i32> = BinaryHeap::new();
    max_heap.push(3);
    max_heap.push(1);
    max_heap.push(2);

    println!("  最大堆顺序:");
    while let Some(v) = max_heap.pop() {
        print!("{} ", v);
    }
    println!();
    // 3 2 1

    // 如果需要最小堆，可以使用 Reverse 包装
    println!("\n使用 Reverse 实现最小堆:");
    use std::cmp::Reverse;

    let mut min_heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    min_heap.push(Reverse(3));
    min_heap.push(Reverse(1));
    min_heap.push(Reverse(2));

    println!("  最小堆顺序:");
    while let Some(Reverse(v)) = min_heap.pop() {
        print!("{} ", v);
    }
    println!();
    // 1 2 3

    // 实际应用：Top-K 问题
    println!("\nTop-K 问题:");
    let data = vec![10, 2, 8, 7, 3, 5, 9, 1, 6, 4];
    let k = 3;

    let mut heap: BinaryHeap<_> = data.iter().take(k).collect();

    // 保持只有 k 个最大元素
    for &num in data.iter().skip(k) {
        if num > *heap.peek().unwrap() {
            heap.pop();
            heap.push(num);
        }
    }

    println!("  数据: {:?}", data);
    println!("  Top {}: {:?}", k, heap.into_sorted_vec());
    // Top 3: [10, 9, 8]

    // 实际应用：优先级队列
    println!("\n优先级队列:");
    #[derive(Debug)]
    struct Task {
        priority: u8,
        name: String,
    }

    let mut pq: BinaryHeap<_> = BinaryHeap::new();

    pq.push(Task { priority: 2, name: String::from("普通任务") });
    pq.push(Task { priority: 1, name: String::from("低优先级") });
    pq.push(Task { priority: 5, name: String::from("紧急任务") });
    pq.push(Task { priority: 3, name: String::from("高优先级") });

    println!("  按优先级处理:");
    while let Some(task) = pq.pop() {
        println!("    优先级 {}: {}", task.priority, task.name);
    }
    // 优先级 5: 紧急任务
    // 优先级 3: 高优先级
    // 优先级 2: 普通任务
    // 优先级 1: 低优先级

    // 容量
    println!("\n容量操作:");
    let mut heap = BinaryHeap::with_capacity(10);
    println!("  capacity: {}", heap.capacity()); // 10

    heap.push(1);
    println!("  len: {}, capacity: {}", heap.len(), heap.capacity());

    // into_sorted_vec
    let mut heap: BinaryHeap<_> = (1..=5).rev().collect();
    let sorted = heap.into_sorted_vec();
    println!("  into_sorted_vec: {:?}", sorted);
    // [1, 2, 3, 4, 5]

    // VecDeque 和 BinaryHeap 都是 collections 模块的一部分
    // 使用前需要引入
}
```

BinaryHeap 是实现"优先级队列"的理想数据结构。在需要不断获取"最大"或"最小"元素的场景中，BinaryHeap 的 O(1) peek 和 O(log n) push/pop 非常高效。

## 6.6 标准库其他核心类型

除了集合类型，Rust 标准库还提供了一些非常重要的核心类型，它们不是集合，但在 Rust 编程中无处不在。

### 6.6.1 Option<T> 详解

`Option<T>` 是 Rust 处理"可能存在也可能不存在"的值的方式。它是一个枚举，有两个变体：`Some(T)` 表示值存在，`None` 表示值不存在。

```rust
fn main() {
    // Option 的定义
    // enum Option<T> {
    //     None,
    //     Some(T),
    // }

    // 基本用法
    println!("Option 基本用法:");

    // Some 表示值存在
    let some_value: Option<i32> = Some(42);
    println!("  Some(42): {:?}", some_value);

    // None 表示值不存在
    let no_value: Option<i32> = None;
    println!("  None: {:?}", no_value);

    // 匹配 Option
    fn process_option(opt: Option<i32>) {
        match opt {
            Some(value) => println!("  值为: {}", value),
            None => println!("  没有值"),
        }
    }

    process_option(Some(100));
    process_option(None);

    // unwrap 系列方法
    println!("\nunwrap 方法:");
    let some = Some(10);
    println!("  Some(10).unwrap(): {}", some.unwrap()); // 10

    // None 调用 unwrap 会 panic
    // let none: Option<i32> = None;
    // none.unwrap(); // panic!

    // unwrap_or 提供默认值
    let none: Option<i32> = None;
    println!("  None.unwrap_or(0): {}", none.unwrap_or(0)); // 0

    // unwrap_or_else 按需计算默认值
    let result = none.unwrap_or_else(|| {
        println!("  计算默认值...");
        expensive_computation()
    });

    // map 转换内部值
    println!("\nmap 转换:");
    let some = Some(5);
    let doubled = some.map(|x| x * 2);
    println!("  Some(5).map(|x| x * 2): {:?}", doubled); // Some(10)

    let none: Option<i32> = None;
    let doubled = none.map(|x| x * 2);
    println!("  None.map(|x| x * 2): {:?}", doubled); // None

    // and_then 链式调用
    println!("\nand_then 链式调用:");
    fn square(x: i32) -> Option<i32> { Some(x * x) }
    fn half(x: i32) -> Option<i32> { if x % 2 == 0 { Some(x / 2) } else { None } }

    let result = Some(4).and_then(square).and_then(half);
    println!("  Some(4).and_then(square).and_then(half): {:?}", result); // Some(8)

    let result = Some(3).and_then(square).and_then(half);
    println!("  Some(3).and_then(square).and_then(half): {:?}", result); // None (3²=9 是奇数)

    // filter 过滤
    println!("\nfilter:");
    let some = Some(8);
    let filtered = some.filter(|x| x % 2 == 0);
    println!("  Some(8).filter(|x| x % 2 == 0): {:?}", filtered); // Some(8)

    let some = Some(7);
    let filtered = some.filter(|x| x % 2 == 0);
    println!("  Some(7).filter(|x| x % 2 == 0): {:?}", filtered); // None

    // or 和 or_else
    println!("\nor:");
    let none: Option<i32> = None;
    println!("  None.or(Some(5)): {:?}", none.or(Some(5))); // Some(5)
    println!("  Some(3).or(Some(5)): {:?}", Some(3).or(Some(5))); // Some(3)

    let result = none.or_else(|| Some(expensive_computation()));
    println!("  None.or_else(|| Some(...)): {:?}", result);

    // get 返回的 &T 自动包装成 Option
    println!("\n与 Vec 配合:");
    let vec = vec![1, 2, 3, 4, 5];
    println!("  vec.get(2): {:?}", vec.get(2)); // Some(&3)
    println!("  vec.get(100): {:?}", vec.get(100)); // None

    // Option 是 Rust 的"空安全"机制
    println!("\nOption 的优势:");
    println!("  - 编译期强制处理 None 情况");
    println!("  - 不会有 null 引用异常");
    println!("  - 明确表达'可能没有值'的语义");

    // Option 在标准库中的广泛使用
    println!("\n标准库中的 Option:");
    // HashMap::get 返回 Option<&V>
    use std::collections::HashMap;
    let mut map = HashMap::new();
    map.insert("key", "value");

    let present = map.get("key");
    let absent = map.get("missing");
    println!("  get(\"key\"): {:?}", present); // Some(&"value")
    println!("  get(\"missing\"): {:?}", absent); // None

    // Vec::pop 返回 Option<T>
    let mut stack = vec![1, 2, 3];
    println!("  pop(): {:?}", stack.pop()); // Some(3)
    println!("  pop(): {:?}", stack.pop()); // Some(2)
    println!("  pop(): {:?}", stack.pop()); // Some(1)
    println!("  pop(): {:?}", stack.pop()); // None

    // Vec::first / last
    println!("  first(): {:?}", vec![].first()); // None
    println!("  last(): {:?}", vec![].last()); // None
}

fn expensive_computation() -> i32 {
    println!("    [expensive_computation 被调用]");
    42
}
```

Option 是 Rust 最特色的类型之一。它强制你在编译期处理"值不存在"的情况，从根本上消灭了 null 引用导致的无数 bug。相比之下，Java、C# 等语言中，null 可以出现在任何地方，导致运行时 NullPointerException。

### 6.6.2 Iterator 详解

Iterator 是 Rust 中处理序列的核心抽象。它代表一个可以逐个产生元素的对象。

```rust
fn main() {
    // Iterator 的定义（简化版）
    // trait Iterator {
    //     type Item;
    //     fn next(&mut self) -> Option<Self::Item>;
    //     // ... 还有其他很多默认方法
    // }

    // 创建迭代器
    println!("创建迭代器:");

    // Vec 的迭代器
    let vec = vec![1, 2, 3];
    let iter = vec.iter();
    println!("  vec.iter(): {:?}", iter);

    // 数组的迭代器
    let arr = [1, 2, 3, 4, 5];
    for item in arr.iter() {
        print!("{} ", item);
    }
    println!();

    // Range 迭代器
    for i in 0..5 {
        print!("{} ", i);
    }
    println!();
    // 0 1 2 3 4

    // 使用迭代器
    println!("\n使用迭代器:");

    let vec = vec![1, 2, 3, 4, 5];
    let mut iter = vec.iter();

    println!("  next(): {:?}", iter.next()); // Some(&1)
    println!("  next(): {:?}", iter.next()); // Some(&2)
    println!("  next(): {:?}", iter.next()); // Some(&3)
    println!("  next(): {:?}", iter.next()); // Some(&4)
    println!("  next(): {:?}", iter.next()); // Some(&5)
    println!("  next(): {:?}", iter.next()); // None

    // 迭代器消耗
    println!("\n迭代器消耗:");
    let vec = vec![1, 2, 3];
    let sum: i32 = vec.iter().sum();
    println!("  sum: {}", sum); // 6

    // 迭代器适配器
    println!("\n迭代器适配器:");

    // map: 转换每个元素
    let vec = vec![1, 2, 3, 4, 5];
    let doubled: Vec<_> = vec.iter().map(|x| x * 2).collect();
    println!("  map(*2): {:?}", doubled);
    // [2, 4, 6, 8, 10]

    // filter: 过滤元素
    let evens: Vec<_> = vec.iter().filter(|x| *x % 2 == 0).collect();
    println!("  filter(偶数): {:?}", evens);
    // [2, 4]

    // 链式调用
    let result: Vec<_> = vec.iter()
        .map(|x| x * x)
        .filter(|x| x % 2 == 0)
        .collect();
    println!("  链式 (平方后过滤偶数): {:?}", result);
    // [4, 16]

    // take / skip
    println!("\ntake / skip:");
    let vec = vec![1, 2, 3, 4, 5];
    let first_three: Vec<_> = vec.iter().take(3).collect();
    println!("  take(3): {:?}", first_three);
    // [1, 2, 3]

    let last_two: Vec<_> = vec.iter().skip(3).collect();
    println!("  skip(3): {:?}", last_two);
    // [4, 5]

    // enumerate: 获取索引
    println!("\nenumerate:");
    let names = vec!["Alice", "Bob", "Charlie"];
    for (i, name) in names.iter().enumerate() {
        println!("  {}: {}", i, name);
    }

    // zip: 合并两个迭代器
    println!("\nzip:");
    let a = vec![1, 2, 3];
    let b = vec!["one", "two", "three"];
    for (num, word) in a.iter().zip(b.iter()) {
        print!("{}={} ", num, word);
    }
    println!();

    // fold: 折叠
    println!("\nfold:");
    let sum = vec![1, 2, 3, 4, 5].iter().fold(0, |acc, x| acc + x);
    println!("  sum: {}", sum); // 15

    let product = vec![1, 2, 3, 4, 5].iter().fold(1, |acc, x| acc * x);
    println!("  product: {}", product); // 120

    // collect: 收集到不同容器
    println!("\ncollect:");
    let iter = 0..10;

    // 收集到 Vec
    let vec: Vec<i32> = iter.clone().collect();
    println!("  收集到 Vec: {:?}", vec);

    // 收集到 HashSet
    use std::collections::HashSet;
    let set: HashSet<_> = iter.collect();
    println!("  收集到 HashSet: {:?}", set);

    // 收集到 String
    let chars = vec!['h', 'e', 'l', 'l', 'o'];
    let s: String = chars.iter().collect();
    println!("  收集到 String: {}", s);

    // any / all
    println!("\nany / all:");
    let vec = vec![1, 2, 3, 4, 5];
    println!("  包含偶数? {}", vec.iter().any(|x| x % 2 == 0)); // true
    println!("  全部大于 0? {}", vec.iter().all(|x| *x > 0)); // true

    // find / position
    println!("\nfind / position:");
    let vec = vec![1, 2, 3, 4, 5];
    println!("  第一个大于 3: {:?}", vec.iter().find(|&&x| x > 3)); // Some(4)
    println!("  第一个大于 10: {:?}", vec.iter().find(|&&x| x > 10)); // None

    println!("  3 的位置: {:?}", vec.iter().position(|&x| x == 3)); // Some(2)
    println!("  10 的位置: {:?}", vec.iter().position(|&x| x == 10)); // None

    // 迭代器的惰性求值
    println!("\n惰性求值:");
    let v = vec![1, 2, 3, 4, 5];
    let iter = v.iter().map(|x| {
        println!("  处理 {}", x);
        x * 2
    });
    println!("  创建了迭代器，map 的闭包还没执行");

    println!("  调用 collect:");
    let result: Vec<_> = iter.collect();
    println!("  结果: {:?}", result);

    // 迭代器是 Rust 高效编程的核心
    println!("\n迭代器的优势:");
    println!("  - 惰性求值，性能优化");
    println!("  - 链式调用，表达力强");
    println!("  - 零成本抽象");
    println!("  - 函数式编程风格");
}
```

Iterator 是 Rust 的"瑞士军刀"。它的惰性求值意味着只有在真正需要结果时才会执行计算，这让性能优化成为可能。通过链式调用适配器，你可以用极其优雅的方式表达复杂的数据处理逻辑。

### 6.6.3 Range 类型

Rust 的 Range 类型用于表示一个区间或序列，在循环、切片、迭代中非常有用。

```rust
fn main() {
    // Range 类型
    println!("Range 类型:");

    // 1..5 是 Range<i32>，不包含结束值
    println!("  1..5:");
    for i in 1..5 {
        print!("{} ", i);
    }
    println!();
    // 1 2 3 4

    // 1..=5 是 RangeInclusive<i32>，包含结束值
    println!("  1..=5:");
    for i in 1..=5 {
        print!("{} ", i);
    }
    println!();
    // 1 2 3 4 5

    // 各种 Range
    println!("\n各种 Range:");

    // Range: start..end
    let r: Range<i32> = 0..10;
    println!("  Range<i32>: {:?}", r);
    println!("  包含 start，不包含 end");

    // RangeFrom: start..
    let r = 5..;
    println!("  RangeFrom<i32>: {:?}", r);
    println!("  从 5 开始，无限");

    // RangeTo: ..end
    let r = ..5;
    println!("  RangeTo<i32>: {:?}", r);

    // RangeFull: ..
    let r = ..;
    println!("  RangeFull: {:?}", r);
    println!("  表示整个范围");

    // 在切片中使用
    println!("\n切片中使用:");
    let arr = [1, 2, 3, 4, 5];
    println!("  arr[..3]: {:?}", &arr[..3]); // [1, 2, 3]
    println!("  arr[2..]: {:?}", &arr[2..]); // [3, 4, 5]
    println!("  arr[1..4]: {:?}", &arr[1..4]); // [2, 3, 4]

    // Range 在索引中
    println!("\nRange 索引:");
    let s = "Hello, World!";
    println!("  s[0..5]: {}", &s[0..5]); // Hello
    println!("  s[7..12]: {}", &s[7..12]); // World

    // char 的 Range
    println!("\n字符 Range:");
    let s = "你好世界";
    println!("  中文字符:");
    for c in s.chars() {
        print!("{} ", c);
    }
    println!();

    // 使用 RangeInclusive
    println!("\nRangeInclusive:");
    use std::ops::RangeInclusive;

    let r: RangeInclusive<i32> = 1..=5;
    println!("  1..=5: {:?}", r.into_iter().collect::<Vec<_>>());
    // [1, 2, 3, 4, 5]

    // contains
    println!("\ncontains:");
    println!("  (1..5).contains(&3): {}", (1..5).contains(&3)); // true
    println!("  (1..5).contains(&5): {}", (1..5).contains(&5)); // false
    println!("  (1..=5).contains(&5): {}", (1..=5).contains(&5)); // true

    // StepBy
    println!("\nStepBy:");
    let v: Vec<_> = (0..10).step_by(2).collect();
    println!("  (0..10).step_by(2): {:?}", v);
    // [0, 2, 4, 6, 8]

    let v: Vec<_> = (1..=10).step_by(3).collect();
    println!("  (1..=10).step_by(3): {:?}", v);
    // [1, 4, 7, 10]

    // 反向 Range
    println!("\n反向迭代:");
    let v: Vec<_> = (0..5).rev().collect();
    println!("  (0..5).rev(): {:?}", v);
    // [4, 3, 2, 1, 0]

    // Range 的适用类型
    println!("\nRange 的适用类型:");
    println!("  - 所有实现了 Step trait 的类型");
    println!("  - i8, i16, i32, i64, i128, isize");
    println!("  - u8, u16, u32, u64, u128, usize");
    println!("  - char");
    println!("  - &str (字节范围), String (字节范围)");
    println!("  - 自定义类型可以手动实现 Step");

    // 实际应用：分页
    println!("\n分页应用:");
    let total = 100;
    let page_size = 10;
    let total_pages = (total + page_size - 1) / page_size;

    println!("  总记录数: {}", total);
    println!("  每页大小: {}", page_size);
    println!("  总页数: {}", total_pages);

    for page in 0..total_pages {
        let start = page * page_size;
        let end = (start + page_size).min(total);
        println!("  第 {} 页: {}..{}", page + 1, start, end);
    }
    // 第 1 页: 0..10
    // 第 2 页: 10..20
    // ...
    // 第 10 页: 90..100
}
```

Range 是 Rust 中处理序列和区间的基础工具。从简单的循环到复杂的分页逻辑，Range 都扮演着重要角色。

### 6.6.4 Cell / RefCell

`Cell<T>` 和 `RefCell<T>` 是 Rust 提供的内部可变性（Interior Mutability）工具。它们允许你在持有不可变引用的同时修改数据。

```rust
fn main() {
    // 内部可变性：即使 &self 是不可变的，也能修改数据
    println!("Cell / RefCell 内部可变性:");

    use std::cell::Cell;

    // Cell<T> 适用于 Copy 类型
    let cell = Cell::new(5);
    println!("  Cell::new(5): {:?}", cell);

    // get 获取值
    println!("  get(): {}", cell.get()); // 5

    // set 设置值
    cell.set(10);
    println!("  set(10): {:?}", cell);

    // 即使有不可变引用，也能修改
    let cell = Cell::new(5);
    fn modify(cell: &Cell<i32>) {
        cell.set(100);
    }
    modify(&cell);
    println!("  通过 &Cell 修改后: {:?}", cell); // 100

    // Cell vs 普通变量
    println!("\n普通变量的限制:");
    let x = 5;
    // fn modify_normal(y: &i32) {
    //     // *y = 100; // 错误！不能通过不可变引用修改
    // }

    // RefCell<T> 适用于非 Copy 类型
    println!("\nRefCell:");
    use std::cell::RefCell;

    let data = RefCell::new(vec![1, 2, 3]);
    println!("  RefCell::new([1,2,3]): {:?}", data);

    // borrow / borrow_mut
    {
        let v = data.borrow(); // &Vec<i32>
        println!("  borrow(): {:?}", v);
    }

    {
        let mut v = data.borrow_mut(); // &mut Vec<i32>
        v.push(4);
        println!("  borrow_mut() push 4: {:?}", v);
    }

    // RefCell 的运行时检查
    println!("\n运行时借用检查:");
    let data = RefCell::new(vec![1, 2, 3]);

    // 同时持有两个可变引用会 panic
    // let r1 = data.borrow_mut();
    // let r2 = data.borrow_mut(); // panic!

    // 正确的使用方式
    {
        let mut v = data.borrow_mut();
        v.push(4);
    }
    {
        let v = data.borrow();
        println!("  之后: {:?}", v);
    }

    // Cell / RefCell 的使用场景
    println!("\n使用场景:");
    println!("  - 单线程环境中需要内部可变性时");
    println!("  - 封装复杂数据结构时");
    println!("  - 实现观察者模式时");
    println!("  - 在不可变上下文中需要修改状态时");

    // Rc<T> + RefCell<T> 组合
    println!("\nRc<RefCell<T>> 组合:");
    use std::cell::RefCell;
    use std::rc::Rc;

    let shared = Rc::new(RefCell::new(vec![1, 2, 3]));

    // 多个所有者
    let a = Rc::clone(&shared);
    let b = Rc::clone(&shared);

    // 都能修改
    a.borrow_mut().push(4);
    println!("  a 修改后: {:?}", shared.borrow());

    b.borrow_mut().push(5);
    println!("  b 修改后: {:?}", shared.borrow());

    println!("  引用计数: {}", Rc::strong_count(&shared)); // 3

    // 注意：Rc<RefCell<T>> 是单线程的
    // 多线程场景应该用 Mutex<T>

    // RefCell 的 borrow 检查
    println!("\nborrow 检查:");
    let data = RefCell::new(42);

    let a = data.borrow();
    println!("  a borrow: {}", a);

    // let b = data.borrow(); // panic! 同时不可变借用
    // let c = data.borrow_mut(); // panic! 同时可变借用

    drop(a); // 释放 a 的借用

    let b = data.borrow();
    println!("  a 释放后 b borrow: {}", b);

    // Cow<'a, B>
    println!("\nCow (Clone-on-Write):");
    use std::borrow::Cow;

    // Cow 是一个枚举：Borrowed 或 Owned
    fn process(s: &str) -> Cow<str> {
        if s.len() > 10 {
            Cow::Owned(s.to_uppercase())
        } else {
            Cow::Borrowed(s)
        }
    }

    let short = "hello";
    let long = "this is a very long string";

    println!("  short: {:?}", process(short));
    println!("  long: {:?}", process(long));
}
```

Cell 和 RefCell 是 Rust 提供的重要工具，它们在特定场景下（单线程内部可变性）非常有用。但要谨慎使用，因为它们把借用检查从编译期移到了运行时——你可能会在运行时遇到 panic。

### 6.6.5 Cow<'a, B>

`Cow<'a, B>` 是 Rust 的" Clone-on-Write"抽象。它表示一个要么是借用的（Borrowed），要么是拥有的（Owned）的数据。

```rust
fn main() {
    use std::borrow::Cow;

    println!("Cow (Clone-on-Write):");

    // Cow 的定义
    // enum Cow<'a, B> {
    //     Borrowed(&'a B),  // 借用
    //     Owned(B),         // 拥有
    // }

    // 创建一个 Borrowed Cow
    let borrowed: Cow<str> = Cow::Borrowed("hello");
    println!("  Borrowed: {:?}", borrowed);

    // 创建一个 Owned Cow
    let owned: Cow<str> = Cow::Owned(String::from("world"));
    println!("  Owned: {:?}", owned);

    // into_owned 将 Cow 转换为 Owned
    let s: String = borrowed.into_owned();
    println!("  into_owned(): {}", s);

    // Cow 的使用场景：函数参数和返回值
    println!("\n函数参数优化:");
    fn greet(name: &str) -> Cow<str> {
        Cow::Owned(format!("Hello, {}!", name))
    }

    let name = "Alice";
    let greeting = greet(name);
    println!("  {}", greeting);

    // 如果已经是 'static， Cow 直接返回
    fn identity(s: &str) -> Cow<str> {
        Cow::Borrowed(s) // 不需要复制
    }

    let static_str = "constant";
    let result = identity(static_str);
    println!("  {:?}", result);

    // Cow 在字符串处理中的应用
    println!("\n字符串处理:");
    fn transform(s: &str) -> Cow<str> {
        if s.chars().any(|c| c.is_uppercase()) {
            Cow::Owned(s.to_lowercase())
        } else {
            Cow::Borrowed(s)
        }
    }

    let mixed = "Hello WORLD";
    let lower = transform(mixed);
    println!("  \"{}\" -> \"{}\"", mixed, lower);

    let already_lower = "hello world";
    let lower = transform(already_lower);
    println!("  \"{}\" -> \"{}\"", already_lower, lower);
    // "hello world" -> "hello world" (没有复制)

    // Cow 在 Vec 处理中的应用
    println!("\nVec 处理:");
    fn double_if_needed(vec: &[i32]) -> Cow<[i32]> {
        // 检查是否需要修改
        let needs_change = vec.iter().any(|x| *x < 0);

        if needs_change {
            Cow::Owned(vec.iter().map(|x| x * 2).collect())
        } else {
            Cow::Borrowed(vec)
        }
    }

    let positive = [1, 2, 3];
    let result = double_if_needed(&positive);
    println!("  正数: {:?}", result);
    // Borrowed，无复制

    let mixed = [1, -2, 3];
    let result = double_if_needed(&mixed);
    println!("  混合: {:?}", result);
    // Owned，有复制

    // Cow 与 to_string / clone
    println!("\n优势对比:");
    fn process_borrowed(s: &str) -> String {
        s.to_uppercase()
    }

    fn process_cow(s: &str) -> Cow<str> {
        if s.starts_with("test") {
            Cow::Owned(s.replace("test", "TETETE"))
        } else {
            Cow::Borrowed(s)
        }
    }

    let input = "hello";
    let result = process_cow(input);
    println!("  处理 \"{}\": {:?}", input, result);
    // 不需要复制，直接返回 Borrowed

    // 实际应用：配置处理
    println!("\n配置处理:");
    #[derive(Debug)]
    struct Config {
        value: Cow<str>,
    }

    impl Config {
        fn new(default: &str) -> Self {
            Config {
                value: Cow::Borrowed(default),
            }
        }

        fn override_if_needed(&mut self, new_value: &str) {
            if new_value != self.value.as_ref() {
                self.value = Cow::Owned(new_value.to_string());
            }
        }
    }

    let mut config = Config::new("default_value");
    println!("  初始: {:?}", config.value);

    config.override_if_needed("user_provided");
    println!("  覆盖后: {:?}", config.value);

    config.override_if_needed("user_provided"); // 相同，不复制
    println!("  再次覆盖（相同）: {:?}", config.value);

    // Cow 的限制
    println!("\n限制:");
    println!("  - B 必须同时实现 ToOwned");
    println!("  - Borrowed 必须是 'a 生命周期");
    println!("  - 不适合需要多次修改的场景");

    // Cow 实现的 Trait
    println!("\n实现的 Trait:");
    let cow: Cow<str> = Cow::Borrowed("test");

    // Deref，自动解引用
    println!("  deref: {}", &cow);

    // AsRef<T>
    let s: &str = cow.as_ref();
    println!("  as_ref: {}", s);

    // Display
    println!("  display: {}", cow);
}
```

Cow 是 Rust 的"零成本抽象"在内存管理上的体现——默认使用借用，只有在真正需要时才复制数据。这在处理字符串和字节序列时特别有用，可以显著减少不必要的内存分配。

---

## 本章小结

恭喜你完成了 Rust 集合类型和核心类型的学习！本章我们涵盖了：

### Vec<T> - 动态数组
- 创建方式：vec![]、Vec::new()、with_capacity()
- 元素操作：push/pop、insert/remove、get/get_mut
- 切片：零成本转换为 &[T]
- 容量管理：len、capacity、reserve/shrink_to_fit
- 常用方法：extend、split_at、dedup、retain、splice、binary_search

### Box<T> - 堆分配
- Box::new() 创建堆分配的值
- Box::leak() 创建永驻内存
- Box::into_raw/from_raw 原始指针转换
- Box::pin() 固定数据支持异步

### 递归类型
- 链表：Cons/Nil 结构，需要 Box 打破无限大小
- 树：二叉树的前序/中序/后序遍历

### Trait 对象
- Box<dyn Trait> 实现动态分发
- &dyn Trait vs Box<dyn Trait> 的选择

### HashMap<K, V> / HashSet<T>
- 创建与基本操作
- Entry API：优雅处理键不存在的情况
- or_insert/or_insert_with
- 集合运算：交集、并集、差集、对称差

### BTreeMap/BTreeSet
- 有序版本，适合范围查询

### 其他集合
- LinkedList：双向链表
- VecDeque：双端队列
- BinaryHeap：优先级队列

### 核心类型
- Option<T>：空安全
- Iterator：惰性序列处理
- Range：区间表示
- Cell/RefCell：内部可变性
- Cow：Clone-on-Write

Rust 的集合库设计体现了几个核心价值观：安全、性能、表达力。通过零成本抽象、标准库的一致性设计、以及强大的类型系统，Rust 让你可以写出既安全又高效的代码。

> 记住：没有最好的数据结构，只有最适合的数据结构。理解每种集合的特点，才能在实际编程中做出正确的选择。继续练习，继续探索，Rust 的世界还有很多精彩等着你！
