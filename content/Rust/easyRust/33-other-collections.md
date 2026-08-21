+++
title = "33-其他集合类型"
date = 2026-08-21T12:46:00+08:00
weight = 34
type = "docs"
description = "其他集合类型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_32.html](https://dhghomon.github.io/easy_rust/Chapter_32.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 其他集合类型

Rust还有很多集合类型。你可以在标准库中的 https://doc.rust-lang.org/beta/std/collections/ 看到它们。那个页面对为什么要使用一种类型有很好的解释，所以如果你不知道你想要什么类型，就去那里。这些集合都在标准库的`std::collections`里面。使用它们的最好方法是使用 `use` 语句。
 就像我们的`enums`一样。我们将从`HashMap`开始，这是很常见的。

## HashMap和BTreeMap

HashMap是由*keys*和*values*组成的集合。你使用键来查找与键匹配的值。你可以只用`HashMap::new()`创建一个新的`HashMap`，并使用`.insert(key, value)`来插入元素。

`HashMap`是没有顺序的，所以如果你把`HashMap`中的每一个键都打印在一起，可能会打印出不同的结果。我们可以在一个例子中看到这一点。

```rust
use std::collections::HashMap; // 这样每次只需写 HashMap，而不必写 std::collections::HashMap

struct City {
    name: String,
    population: HashMap<u32, u32>, // 存放年份以及该年的人口
}

fn main() {

    let mut tallinn = City {
        name: "Tallinn".to_string(),
        population: HashMap::new(), // 目前 HashMap 还是空的
    };

    tallinn.population.insert(1372, 3_250); // 插入三个日期
    tallinn.population.insert(1851, 24_000);
    tallinn.population.insert(2020, 437_619);


    for (year, population) in tallinn.population { // HashMap 类型是 HashMap<u32, u32>，所以每次得到两个值
        println!("In the year {} the city of {} had a population of {}.", year, tallinn.name, population);
    }
}
```

这个打印:

```text
In the year 1372 the city of Tallinn had a population of 3250.
In the year 2020 the city of Tallinn had a population of 437619.
In the year 1851 the city of Tallinn had a population of 24000.
```

或者可能会打印。

```text
In the year 1851 the city of Tallinn had a population of 24000.
In the year 2020 the city of Tallinn had a population of 437619.
In the year 1372 the city of Tallinn had a population of 3250.
```

你可以看到，它不按顺序排列。

如果你想要一个可以排序的`HashMap`，你可以用`BTreeMap`。其实它们之间是非常相似的，所以我们可以快速的把我们的`HashMap`改成`BTreeMap`来看看。大家可以看到，这几乎是一样的代码。

```rust
use std::collections::BTreeMap; // 只需把 HashMap 改成 BTreeMap

struct City {
    name: String,
    population: BTreeMap<u32, u32>, // 只需把 HashMap 改成 BTreeMap
}

fn main() {

    let mut tallinn = City {
        name: "Tallinn".to_string(),
        population: BTreeMap::new(), // 只需把 HashMap 改成 BTreeMap
    };

    tallinn.population.insert(1372, 3_250);
    tallinn.population.insert(1851, 24_000);
    tallinn.population.insert(2020, 437_619);

    for (year, population) in tallinn.population {
        println!("In the year {} the city of {} had a population of {}.", year, tallinn.name, population);
    }
}
```

现在会一直打印。

```text
In the year 1372 the city of Tallinn had a population of 3250.
In the year 1851 the city of Tallinn had a population of 24000.
In the year 2020 the city of Tallinn had a population of 437619.
```

现在我们再来看看`HashMap`。

只要把键放在`[]`的方括号里，就可以得到`HashMap`的值。在接下来的这个例子中，我们将带出`Bielefeld`这个键的值，也就是`Germany`。但是要注意，因为如果没有键，程序会崩溃。比如你写了`println!("{:?}", city_hashmap["Bielefeldd"]);`，那么就会崩溃，因为`Bielefeldd`不存在。

如果你不确定会有一个键，你可以使用`.get()`，它返回一个`Option`。如果它存在，将是`Some(value)`，如果不存在，你将得到`None`，而不是使程序崩溃。这就是为什么 `.get()` 是从 `HashMap` 中获取一个值的比较安全的方法。

```rust
use std::collections::HashMap;

fn main() {
    let canadian_cities = vec!["Calgary", "Vancouver", "Gimli"];
    let german_cities = vec!["Karlsruhe", "Bad Doberan", "Bielefeld"];

    let mut city_hashmap = HashMap::new();

    for city in canadian_cities {
        city_hashmap.insert(city, "Canada");
    }
    for city in german_cities {
        city_hashmap.insert(city, "Germany");
    }

    println!("{:?}", city_hashmap["Bielefeld"]);
    println!("{:?}", city_hashmap.get("Bielefeld"));
    println!("{:?}", city_hashmap.get("Bielefeldd"));
}
```

这个打印:

```text
"Germany"
Some("Germany")
None
```

这是因为*Bielefeld*存在，但*Bielefeldd*不存在。

如果`HashMap`已经有一个键，当你试图把它放进去时，它将覆盖它的值。

```rust
use std::collections::HashMap;

fn main() {
    let mut book_hashmap = HashMap::new();

    book_hashmap.insert(1, "L'Allemagne Moderne");
    book_hashmap.insert(1, "Le Petit Prince");
    book_hashmap.insert(1, "섀도우 오브 유어 스마일");
    book_hashmap.insert(1, "Eye of the World");

    println!("{:?}", book_hashmap.get(&1));
}
```

这将打印出 `Some("Eye of the World")`，因为它是你最后使用 `.insert()` 的条目。

检查一个条目是否存在是很容易的，因为你可以用 `.get()` 检查，它给出了 `Option`。

```rust
use std::collections::HashMap;

fn main() {
    let mut book_hashmap = HashMap::new();

    book_hashmap.insert(1, "L'Allemagne Moderne");

    if book_hashmap.get(&1).is_none() { // is_none() 返回 bool：是 None 则为 true，是 Some 则为 false
        book_hashmap.insert(1, "Le Petit Prince");
    }

    println!("{:?}", book_hashmap.get(&1));
}
```

这个打印`Some("L\'Allemagne Moderne")`是因为已经有了key为`1`的，所以我们没有插入`Le Petit Prince`。

`HashMap`有一个非常有趣的方法，叫做`.entry()`，你一定要试试。有了它，你可以在没有键的情况下，用如`.or_insert()`这类方法来插入值。有趣的是，它还给出了一个可变引用，所以如果你想的话，你可以改变它。首先是一个例子，我们只是在每次插入书名到`HashMap`时插入一个`true`。

让我们假设我们有一个图书馆，并希望跟踪我们的书籍。

```rust
use std::collections::HashMap;

fn main() {
    let book_collection = vec!["L'Allemagne Moderne", "Le Petit Prince", "Eye of the World", "Eye of the World"]; // Eye of the World 出现了两次

    let mut book_hashmap = HashMap::new();

    for book in book_collection {
        book_hashmap.entry(book).or_insert(true);
    }
    for (book, true_or_false) in book_hashmap {
        println!("Do we have {}? {}", book, true_or_false);
    }
}
```

这个将打印:

```text
Do we have Eye of the World? true
Do we have Le Petit Prince? true
Do we have L'Allemagne Moderne? true
```

但这并不是我们想要的。也许最好是数一下书的数量，这样我们就知道*世界之眼* 有两本。首先让我们看看`.entry()`做了什么，以及`.or_insert()`做了什么。`.entry()`其实是返回了一个名为`Entry`的`enum`。

```rust
pub fn entry(&mut self, key: K) -> Entry<K, V> // 🚧
```


[Entry文档页](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html)。下面是其代码的简单版本。`K`表示key，`V`表示value。

```rust
// 🚧
use std::collections::hash_map::*;

enum Entry<K, V> {
    Occupied(OccupiedEntry<K, V>),
    Vacant(VacantEntry<K, V>),
}
```

然后当我们调用`.or_insert()`时，它就会查看枚举，并决定该怎么做。

```rust
fn or_insert(self, default: V) -> &mut V { // 🚧
    match self {
        Occupied(entry) => entry.into_mut(),
        Vacant(entry) => entry.insert(default),
    }
}
```

有趣的是，它返回一个`mut`的引用。`&mut V`. 这意味着你可以使用`let`将其附加到一个变量上，并改变变量来改变`HashMap`中的值。所以对于每本书，如果没有条目，我们就会插入一个0。而如果有的话，我们将在引用上使用`+= 1`来增加数字。现在它看起来像这样:

```rust
use std::collections::HashMap;

fn main() {
    let book_collection = vec!["L'Allemagne Moderne", "Le Petit Prince", "Eye of the World", "Eye of the World"];

    let mut book_hashmap = HashMap::new();

    for book in book_collection {
        let return_value = book_hashmap.entry(book).or_insert(0); // return_value 是可变引用。若还没有条目则为 0
        *return_value +=1; // 现在 return_value 至少为 1。若已有同名书，则再加 1
    }

    for (book, number) in book_hashmap {
        println!("{}, {}", book, number);
    }
}
```


重要的部分是`let return_value = book_hashmap.entry(book).or_insert(0);`。如果去掉 `let`，你会得到 `book_hashmap.entry(book).or_insert(0)`。如果没有`let`，它什么也不做:它插入了0，没有获取指向0的可变引用。所以我们把它绑定到`return_value`上，这样我们就可以保留0。然后我们把值增加1，这样`HashMap`中的每本书都至少有1。然后当`.entry()`再看*世界之眼*时，它不会插入任何东西，但它给我们一个可变的1。然后我们把它增加到2，所以它才会打印出这样的结果。

```text
L'Allemagne Moderne, 1
Le Petit Prince, 1
Eye of the World, 2
```


你也可以用`.or_insert()`做一些事情，比如插入一个vec，然后推入数据。让我们假设我们问街上的男人和女人他们对一个政治家的看法。他们给出的评分从0到10。然后我们要把这些数字放在一起，看看这个政治家是更受男人欢迎还是女人欢迎。它可以是这样的。


```rust
use std::collections::HashMap;

fn main() {
    let data = vec![ // 这是原始数据
        ("male", 9),
        ("female", 5),
        ("male", 0),
        ("female", 6),
        ("female", 5),
        ("male", 10),
    ];

    let mut survey_hash = HashMap::new();

    for item in data { // 得到一个 (&str, i32) 元组
        survey_hash.entry(item.0).or_insert(Vec::new()).push(item.1); // 把数字推进里面的 Vec
    }

    for (male_or_female, numbers) in survey_hash {
        println!("{:?}: {:?}", male_or_female, numbers);
    }
}
```

这个打印:

```text
"female", [5, 6, 5]
"male", [9, 0, 10]
```

重要的一行是:`survey_hash.entry(item.0).or_insert(Vec::new()).push(item.1);`，所以如果它看到 "女"，就会检查`HashMap`中是否已经有 "女"。如果没有，它就会插入一个`Vec::new()`，然后把数字推入。如果它看到 "女性"已经在`HashMap`中，它将不会插入一个新的Vec，而只是将数字推入其中。

## HashSet和BTreeSet

`HashSet`实际上是一个只有key的`HashMap`。在[HashSet的页面](https://doc.rust-lang.org/std/collections/struct.HashSet.html)上面有解释。


`A hash set implemented as a HashMap where the value is ().` 所以这是一个`HashMap`，有键，没有值。

如果你只是想知道一个键是否存在，或者不存在，你经常会使用`HashSet`。

想象一下，你有100个随机数，每个数字在1和100之间。如果你这样做，有些数字会出现不止一次，而有些数字根本不会出现。如果你把它们放到`HashSet`中，那么你就会有一个所有出现的数字的列表。

```rust
use std::collections::HashSet;

fn main() {
    let many_numbers = vec![
        94, 42, 59, 64, 32, 22, 38, 5, 59, 49, 15, 89, 74, 29, 14, 68, 82, 80, 56, 41, 36, 81, 66,
        51, 58, 34, 59, 44, 19, 93, 28, 33, 18, 46, 61, 76, 14, 87, 84, 73, 71, 29, 94, 10, 35, 20,
        35, 80, 8, 43, 79, 25, 60, 26, 11, 37, 94, 32, 90, 51, 11, 28, 76, 16, 63, 95, 13, 60, 59,
        96, 95, 55, 92, 28, 3, 17, 91, 36, 20, 24, 0, 86, 82, 58, 93, 68, 54, 80, 56, 22, 67, 82,
        58, 64, 80, 16, 61, 57, 14, 11];

    let mut number_hashset = HashSet::new();

    for number in many_numbers {
        number_hashset.insert(number);
    }

    let hashset_length = number_hashset.len(); // 长度告诉我们里面有多少个数
    println!("There are {} unique numbers, so we are missing {}.", hashset_length, 100 - hashset_length);

    // 看看缺了哪些数
    let mut missing_vec = vec![];
    for number in 0..100 {
        if number_hashset.get(&number).is_none() { // 若 .get() 返回 None，
            missing_vec.push(number);
        }
    }

    print!("It does not contain: ");
    for number in missing_vec {
        print!("{} ", number);
    }
}
```

这个打印:

```text
There are 66 unique numbers, so we are missing 34.
It does not contain: 1 2 4 6 7 9 12 21 23 27 30 31 39 40 45 47 48 50 52 53 62 65 69 70 72 75 77 78 83 85 88 97 98 99
```

`BTreeSet`与`HashSet`相似，就像`BTreeMap`与`HashMap`相似一样。如果我们把`HashSet`中的每一项都打印出来，就不知道顺序是什么了。

```rust
for entry in number_hashset { // 🚧
    print!("{} ", entry);
}
```

也许它能打印出这个。`67 28 42 25 95 59 87 11 5 81 64 34 8 15 13 86 10 89 63 93 49 41 46 57 60 29 17 22 74 43 32 38 36 76 71 18 14 84 61 16 35 90 56 54 91 19 94 44 3 0 68 80 51 92 24 20 82 26 58 33 55 96 37 66 79 73`. 但它几乎不会再以同样的方式打印。

在这里也一样，如果你决定需要订购的话，很容易把你的`HashSet`改成`BTreeSet`。在我们的代码中，我们只需要做两处改动，就可以从`HashSet`切换到`BTreeSet`。

```rust
use std::collections::BTreeSet; // 把 HashSet 改成 BTreeSet

fn main() {
    let many_numbers = vec![
        94, 42, 59, 64, 32, 22, 38, 5, 59, 49, 15, 89, 74, 29, 14, 68, 82, 80, 56, 41, 36, 81, 66,
        51, 58, 34, 59, 44, 19, 93, 28, 33, 18, 46, 61, 76, 14, 87, 84, 73, 71, 29, 94, 10, 35, 20,
        35, 80, 8, 43, 79, 25, 60, 26, 11, 37, 94, 32, 90, 51, 11, 28, 76, 16, 63, 95, 13, 60, 59,
        96, 95, 55, 92, 28, 3, 17, 91, 36, 20, 24, 0, 86, 82, 58, 93, 68, 54, 80, 56, 22, 67, 82,
        58, 64, 80, 16, 61, 57, 14, 11];

    let mut number_btreeset = BTreeSet::new(); // 把 HashSet 改成 BTreeSet

    for number in many_numbers {
        number_btreeset.insert(number);
    }
    for entry in number_btreeset {
        print!("{} ", entry);
    }
}
```

现在会按顺序打印。`0 3 5 8 10 11 13 14 15 16 17 18 19 20 22 24 25 26 28 29 32 33 34 35 36 37 38 41 42 43 44 46 49 51 54 55 56 57 58 59 60 61 63 64 66 67 68 71 73 74 76 79 80 81 82 84 86 87 89 90 91 92 93 94 95 96`.

## 二叉堆

`BinaryHeap`是一种有趣的集合类型，因为它大部分是无序的，但也有一点秩序。它把最大的元素放在前面，但其他元素是按任何顺序排列的。

我们将用另一个元素列表来举例，但这次数据少些。

```rust
use std::collections::BinaryHeap;

fn show_remainder(input: &BinaryHeap<i32>) -> Vec<i32> { // 此函数显示 BinaryHeap 中剩余的元素。其实迭代器会
                                                         // 比函数更快——我们以后再学。
    let mut remainder_vec = vec![];
    for number in input {
        remainder_vec.push(*number)
    }
    remainder_vec
}

fn main() {
    let many_numbers = vec![0, 5, 10, 15, 20, 25, 30]; // 这些数字是有序的

    let mut my_heap = BinaryHeap::new();

    for number in many_numbers {
        my_heap.push(number);
    }

    while let Some(number) = my_heap.pop() { // 有数字时 .pop() 返回 Some(number)，否则返回 None。它从最前面弹出
        println!("Popped off {}. Remaining numbers are: {:?}", number, show_remainder(&my_heap));
    }
}
```

这个打印:

```text
Popped off 30. Remaining numbers are: [25, 15, 20, 0, 10, 5]
Popped off 25. Remaining numbers are: [20, 15, 5, 0, 10]
Popped off 20. Remaining numbers are: [15, 10, 5, 0]
Popped off 15. Remaining numbers are: [10, 0, 5]
Popped off 10. Remaining numbers are: [5, 0]
Popped off 5. Remaining numbers are: [0]
Popped off 0. Remaining numbers are: []
```

你可以看到，0指数的数字总是最大的。25, 20, 15, 10, 5, 然后是0.

使用`BinaryHeap<(u8, &str)>`的一个好方法是用于一个事情的集合。这里我们创建一个`BinaryHeap<(u8, &str)>`，其中`u8`是任务重要性的数字。`&str`是对要做的事情的描述。

```rust
use std::collections::BinaryHeap;

fn main() {
    let mut jobs = BinaryHeap::new();

    // 添加一天中要做的工作
    jobs.push((100, "Write back to email from the CEO"));
    jobs.push((80, "Finish the report today"));
    jobs.push((5, "Watch some YouTube"));
    jobs.push((70, "Tell your team members thanks for always working hard"));
    jobs.push((30, "Plan who to hire next for the team"));

    while let Some(job) = jobs.pop() {
        println!("You need to: {}", job.1);
    }
}
```

这将一直打印:

```text
You need to: Write back to email from the CEO
You need to: Finish the report today
You need to: Tell your team members thanks for always working hard
You need to: Plan who to hire next for the team
You need to: Watch some YouTube
```

## VecDeque

`VecDeque`就是一个`Vec`，既能从前面弹出item，又能从后面弹出item。Rust有`VecDeque`是因为`Vec`很适合从后面(最后一个元素)弹出，但从前面弹出就不那么好了。当你在`Vec`上使用`.pop()`的时候，它只是把右边最后一个item取下来，其他的都不会动。但是如果你把它从其他部分取下来，右边的所有元素都会向左移动一个位置。你可以在`.remove()`的描述中看到这一点。


```text
Removes and returns the element at position index within the vector, shifting all elements after it to the left.
```

所以如果你这样做:

```rust
fn main() {
    let mut my_vec = vec![9, 8, 7, 6, 5];
    my_vec.remove(0);
}
```

它将删除 `9`。索引1中的`8`将移到索引0，索引2中的`7`将移到索引1，以此类推。想象一下，一个大停车场，每当有一辆车离开时，右边所有的车都要移过来。

比如说，这对计算机来说是一个*很大*的工作量。事实上，如果你在playground上运行它，它可能会因为工作太多而直接放弃。

```rust
fn main() {
    let mut my_vec = vec![0; 600_000];
    for i in 0..600000 {
        my_vec.remove(0);
    }
}
```

这是60万个零的`Vec`。每次你用`remove(0)`，它就会把每个零向左移动一个空格。然后它就会做60万次。

用`VecDeque`就不用担心这个问题了。它通常比`Vec`慢一点，但如果你要在两端都做事情，那么它就快多了。你可以直接用`VecDeque::from`与`Vec`来创建一个。那么我们上面的代码就是这样的。

```rust
use std::collections::VecDeque;

fn main() {
    let mut my_vec = VecDeque::from(vec![0; 600000]);
    for i in 0..600000 {
        my_vec.pop_front(); // pop_front 类似 .pop，但是从前面弹出
    }
}
```

现在速度快了很多，在playground上，它在一秒内完成，而不是放弃。

在接下来的这个例子中，我们在一个`Vec`上做一些事。我们创建一个`VecDeque`，用`.push_front()`把它们放在前面，所以我们添加的第一个元素会在右边。但是我们推送的每一个元素都是一个`(&str, bool)`:`&str`是描述, `false`表示还没有完成。我们用`done()`函数从后面弹出一个元素，但是我们不想删除它。相反，我们把`false`改成`true`，然后把它推到前面，这样我们就可以保留它。

它看起来是这样的:

```rust
use std::collections::VecDeque;

fn check_remaining(input: &VecDeque<(&str, bool)>) { // 每一项都是 (&str, bool)
    for item in input {
        if item.1 == false {
            println!("You must: {}", item.0);
        }
    }
}

fn done(input: &mut VecDeque<(&str, bool)>) {
    let mut task_done = input.pop_back().unwrap(); // 从后面弹出
    task_done.1 = true;                            // 现在完成了——标记为 true
    input.push_front(task_done);                   // 再放到前面
}

fn main() {
    let mut my_vecdeque = VecDeque::new();
    let things_to_do = vec!["send email to customer", "add new product to list", "phone Loki back"];

    for thing in things_to_do {
        my_vecdeque.push_front((thing, false));
    }

    done(&mut my_vecdeque);
    done(&mut my_vecdeque);

    check_remaining(&my_vecdeque);

    for task in my_vecdeque {
        print!("{:?} ", task);
    }
}
```

这个打印:

```text
You must: phone Loki back
("add new product to list", true) ("send email to customer", true) ("phone Loki back", false)
```
