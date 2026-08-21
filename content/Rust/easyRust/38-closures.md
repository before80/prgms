+++
title = "38-闭包"
date = 2026-08-21T12:46:00+08:00
weight = 39
type = "docs"
description = "闭包 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_37.html](https://dhghomon.github.io/easy_rust/Chapter_37.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 闭包

闭包就像快速函数，不需要名字。有时它们被称为lambda。Closures很容易辨识，因为它们使用`||`而不是`()`。它们在 Rust 中非常常见，一旦你学会了使用它们，你就会爱不释手。

你可以将一个闭包绑定到一个变量上，然后当你使用它时，它看起来就像一个函数一样。

```rust
fn main() {
    let my_closure = || println!("This is a closure");
    my_closure();
}
```

所以这个闭包什么都不需要:`||`，并打印一条信息。`This is a closure`.

在`||`之间我们可以添加输入变量和类型，就像在`()`里面添加函数一样。

```rust
fn main() {
    let my_closure = |x: i32| println!("{}", x);

    my_closure(5);
    my_closure(5+5);
}
```

这个打印:

```text
5
10
```

当闭包变得更复杂时，你可以添加一个代码块。那就可以随心所欲的长。

```rust
fn main() {
    let my_closure = || {
        let number = 7;
        let other_number = 10;
        println!("The two numbers are {} and {}.", number, other_number);
          // 这个闭包可以想写多长就多长，就像函数一样。
    };

    my_closure();
}
```

但是闭包是特殊的，因为它可以接受闭包之外的变量，即使你只写`||`。所以你可以这样做:

```rust
fn main() {
    let number_one = 6;
    let number_two = 10;

    let my_closure = || println!("{}", number_one + number_two);
    my_closure();
}
```

所以这就打印出了`16`。你不需要在 `||` 中放入任何东西，因为它可以直接取 `number_one` 和 `number_two` 并添加它们。

顺便说一下，这就是**closure**这个名字的由来，因为它们会取变量并将它们 "包围"在里面。如果你想很正确的说。

- 一个`||`如果不把变量从外面包围起来 那就是一个 "匿名函数". 匿名的意思是 "没有名字"。它的工作原理更像一个普通函数。
- `||` 从外部包围变量的函数是 "closure"。它把周围的变量 "封闭"起来使用。

但是人们经常会把所有的`||`函数都叫做闭包，所以你不用担心名字的问题。我们只对任何带有`||`的函数说 "closure"，但请记住，它可能意味着一个 "匿名函数"。

为什么要知道这两者的区别呢？因为匿名函数其实和有名字的函数做的机器代码是一样的。它们给人的感觉是 "高层抽象"，所以有时候大家会觉得机器代码会很复杂。但是Rust用它生成的机器码和普通函数一样快。


所以我们再来看看闭包能做的一些事情。你也可以这样做:

```rust
fn main() {
    let number_one = 6;
    let number_two = 10;

    let my_closure = |x: i32| println!("{}", number_one + number_two + x);
    my_closure(5);
}
```

这个闭包取`number_one`和`number_two`。我们还给了它一个新的变量 `x`，并说 `x` 是 5.然后它把这三个加在一起打印 `21`。

通常在Rust中，你会在一个方法里面看到闭包，因为里面有一个闭包是非常方便的。我们在上一节的 `.map()` 和 `.for_each()` 中看到了闭包。在那一节中，我们写了 `|x|` 来引入迭代器中的下一个元素，这就是一个闭包。

下面再举一个例子:我们知道，如果`unwrap`不起作用，可以用`unwrap_or`方法给出一个值。之前我们写的是:`let fourth = my_vec.get(3).unwrap_or(&0);`。但是还有一个`unwrap_or_else`方法，里面有一个闭包。所以你可以这样做:

```rust
fn main() {
    let my_vec = vec![8, 9, 10];

    let fourth = my_vec.get(3).unwrap_or_else(|| { // 尝试 unwrap。如果失败，
        if my_vec.get(0).is_some() {               // 看 my_vec 在索引 [0] 有没有值
            &my_vec[0]                             // 有的话就给索引 0 的数字
        } else {
            &0 // 否则给一个 &0
        }
    });

    println!("{}", fourth);
}
```

当然，闭包也可以很简单。例如，你可以只写`let fourth = my_vec.get(3).unwrap_or_else(|| &0);`。你不需要总是因为有一个闭包就使用`{}`并写出复杂的代码。只要你把`||`放进去，编译器就知道你放了你需要的闭包。

最常用的闭包方法可能是`.map()`。我们再来看看它。下面是一种使用方法。

```rust
fn main() {
    let num_vec = vec![2, 4, 6];

    let double_vec = num_vec        // 取 num_vec
        .iter()                     // 对它迭代
        .map(|number| number * 2)   // 每个元素乘以 2
        .collect::<Vec<i32>>();     // 再做成新的 Vec
    println!("{:?}", double_vec);
}
```

另一个很好的例子是在`.enumerate()`之后使用`.for_each()`。`.enumerate()`方法给出一个带有索引号和元素的迭代器。例如:`[10, 9, 8]`变成`(0, 10), (1, 9), (2, 8)`。这里每个项的类型是`(usize, i32)`。所以你可以这样做:

```rust
fn main() {
    let num_vec = vec![10, 9, 8];

    num_vec
        .iter()      // 迭代 num_vec
        .enumerate() // 得到 (索引, 数字)
        .for_each(|(index, number)| println!("Index number {} has number {}", index, number)); // 对每一项做点事
}
```

这个将打印:

```text
Index number 0 has number 10
Index number 1 has number 9
Index number 2 has number 8
```

在这种情况下，我们用`for_each`代替`map`。`map`是用于对**每个元素做一些事情，并将其传递出去，而`for_each`是当你看到每个元素**时做一些事情。另外，`map`不做任何事情，除非你使用`collect`这样的方法。

其实，这就是迭代器的有趣之处。如果你尝试`map`而不使用`collect`这样的方法，编译器会告诉你，它什么也不做。它不会崩溃，但编译器会告诉你，你什么都没做。

```rust
fn main() {
    let num_vec = vec![10, 9, 8];

    num_vec
        .iter()
        .enumerate()
        .map(|(index, number)| println!("Index number {} has number {}", index, number));

}
```

它说:

```text
warning: unused `std::iter::Map` that must be used
 --> src\main.rs:4:5
  |
4 | /     num_vec
5 | |         .iter()
6 | |         .enumerate()
7 | |         .map(|(index, number)| println!("Index number {} has number {}", index, number));
  | |_________________________________________________________________________________________^
  |
  = note: `#[warn(unused_must_use)]` on by default
  = note: iterators are lazy and do nothing unless consumed
```

这是一个**警告**，所以这不是一个错误:程序运行正常。但是为什么num_vec没有任何作用呢？我们可以看看类型就知道了。

- `let num_vec = vec![10, 9, 8];` 现在是一个`Vec<i32>`。
- `.iter()` 现在是一个 `Iter<i32>`。所以它是一个迭代器，其元素为 `i32`。

- `.enumerate()`现在是一个`Enumerate<Iter<i32>>`型。所以它是`Enumerate`型的`Iter`型的`i32`。
- `.map()`现在是一个`Map<Enumerate<Iter<i32>>>`的类型。所以它是一个类型`Map`的类型`Enumerate`的类型`Iter`的类型`i32`。

我们所做的只是做了一个越来越复杂的结构。所以这个`Map<Enumerate<Iter<i32>>>`是一个准备好了的结构，但只有当我们告诉它要做什么的时候，它才会去做。Rust这样做是因为它需要保证足够快。它不想这样做:

- 遍历Vec中所有的`i32`
- 然后从迭代器中枚举出所有的`i32`
- 然后将所有列举的`i32`映射过来

Rust 只想做一次计算，所以它创建结构并等待。然后，如果我们说`.collect::<Vec<i32>>()`，它知道该怎么做，并开始移动。这就是`iterators are lazy and do nothing unless consumed`的意思。迭代器在你 "消耗"它们(用完它们)之前不会做任何事情。


你甚至可以用`.collect()`创建像`HashMap`这样复杂的东西，所以它非常强大。下面是一个如何将两个向量放入`HashMap`的例子。首先我们把两个向量创建出来，然后我们会对它们使用`.into_iter()`来得到一个值的迭代器。然后我们使用`.zip()`方法。这个方法将两个迭代器连接在一起，就像拉链一样。最后，我们使用`.collect()`来创建`HashMap`。

下面是代码。

```rust
use std::collections::HashMap;

fn main() {
    let some_numbers = vec![0, 1, 2, 3, 4, 5]; // 一个 Vec<i32>
    let some_words = vec!["zero", "one", "two", "three", "four", "five"]; // 一个 Vec<&str>

    let number_word_hashmap = some_numbers
        .into_iter()                 // 现在是一个迭代器
        .zip(some_words.into_iter()) // 在 .zip() 里放入另一个迭代器。现在它们绑在一起了。
        .collect::<HashMap<_, _>>();

    println!("For key {} we get {}.", 2, number_word_hashmap.get(&2).unwrap());
}
```

这个将打印:

```text
For key 2 we get two.
```

你可以看到，我们写了 `<HashMap<_, _>>`，因为这足以让 Rust 决定 `HashMap<i32, &str>` 的类型。如果你想写 `.collect::<HashMap<i32, &str>>();`也行，也可以这样写:

```rust
use std::collections::HashMap;

fn main() {
    let some_numbers = vec![0, 1, 2, 3, 4, 5]; // 一个 Vec<i32>
    let some_words = vec!["zero", "one", "two", "three", "four", "five"]; // 一个 Vec<&str>
    let number_word_hashmap: HashMap<_, _> = some_numbers  // 因为这里已经告诉它类型了……
        .into_iter()
        .zip(some_words.into_iter())
        .collect(); // 这里就不用再写类型了
}
```

还有一种方法，就像`.enumerate()`的`char`。`char_indices()`. (Indices的意思是 "索引")。你用它的方法是一样的。假设我们有一个由3位数组成的大字符串。

```rust
fn main() {
    let numbers_together = "140399923481800622623218009598281";

    for (index, number) in numbers_together.char_indices() {
        match (index % 3, number) {
            (0..=1, number) => print!("{}", number), // 有余数就只打印数字
            _ => print!("{}\t", number), // 否则打印数字再加一个制表符
        }
    }
}
```

打印`140     399     923     481     800     622     623     218     009     598    281`。


## 闭包中的|_|

有时你会在一个闭包中看到 `|_|`。这意味着这个闭包需要一个参数(比如 `x`)，但你不想使用它。所以 `|_|` 意味着 "好吧，这个闭包需要一个参数，但我不会给它一个名字，因为我不关心它"。

下面是一个错误的例子，当你不这样做的时候。

```rust
fn main() {
    let my_vec = vec![8, 9, 10];

    println!("{:?}", my_vec.iter().for_each(|| println!("We didn't use the variables at all"))); // ⚠️
}
```

Rust说

```text
error[E0593]: closure is expected to take 1 argument, but it takes 0 arguments
  --> src\main.rs:28:36
   |
28 |     println!("{:?}", my_vec.iter().for_each(|| println!("We didn't use the variables at all")));
   |                                    ^^^^^^^^ -- takes 0 arguments
   |                                    |
   |                                    expected closure that takes 1 argument
```

编译器其实给你一些帮助。

```text
help: consider changing the closure to take and ignore the expected argument
   |
28 |     println!("{:?}", my_vec.iter().for_each(|_| println!("We didn't use the variables at all")));
```

这是很好的建议。如果你把`||`改成`|_|`就可以了。

## 闭包和迭代器的有用方法

一旦你熟悉了闭包，Rust就会成为一种非常有趣的语言。有了闭包，你可以将方法互相*链接*起来，用很少的代码做很多事情。下面是一些我们还没有见过的闭包和使用闭包的方法。

`.filter()`: 这可以让你在迭代器中保留你想保留的元素。让我们过滤一年中的月份。

```rust
fn main() {
    let months = vec!["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    let filtered_months = months
        .into_iter()                         // 做成迭代器
        .filter(|month| month.len() < 5)     // 不要长度超过 5 字节的月份。
                                             // 每个字母一个字节，所以用 .len() 没问题
        .filter(|month| month.contains("u")) // 而且我们只喜欢带字母 u 的月份
        .collect::<Vec<&str>>();

    println!("{:?}", filtered_months);
}
```

这个打印`["June", "July"]`。



`.filter_map()`. 这个叫做`filter_map()`，因为它做了`.filter()`和`.map()`。闭包必须返回一个 `Option<T>`，然后对每个`Option`, 如果是 `Some`, `filter_map()`将取出它的值。所以比如说你`.filter_map()`一个`vec![Some(2), None, Some(3)]`，它就会返回`[2, 3]`。

我们将用一个`Company`结构体来写一个例子。每个公司都有一个`name`，所以这个字段是`String`，但是CEO可能最近已经辞职了。所以`ceo`字段是`Option<String>`。我们会`.filter_map()`过一些公司，只保留CEO名字。

```rust
struct Company {
    name: String,
    ceo: Option<String>,
}

impl Company {
    fn new(name: &str, ceo: &str) -> Self {
        let ceo = match ceo {
            "" => None,
            name => Some(name.to_string()),
        }; // ceo 已定，现在返回 Self
        Self {
            name: name.to_string(),
            ceo,
        }
    }

    fn get_ceo(&self) -> Option<String> {
        self.ceo.clone() // 只返回 CEO 的克隆（结构体没有 Copy）
    }
}

fn main() {
    let company_vec = vec![
        Company::new("Umbrella Corporation", "Unknown"),
        Company::new("Ovintiv", "Doug Suttles"),
        Company::new("The Red-Headed League", ""),
        Company::new("Stark Enterprises", ""),
    ];

    let all_the_ceos = company_vec
        .into_iter()
        .filter_map(|company| company.get_ceo()) // filter_map 需要 Option<T>
        .collect::<Vec<String>>();

    println!("{:?}", all_the_ceos);
}
```

这就打印出了`["Unknown", "Doug Suttles"]`。

既然 `.filter_map()` 需要 `Option`，那么 `Result` 呢？没问题:有一个叫做 `.ok()` 的方法，可以把 `Result` 变成 `Option`。之所以叫`.ok()`，是因为它能发送的只是`Ok`的结果(`Err`的信息没有了)。你记得`Option`是`Option<T>`，而`Result`是`Result<T, E>`，同时有`Ok`和`Err`的信息。所以当你使用`.ok()`时，任何`Err`的信息都会丢失，变成`None`。

使用 `.parse()` 是一个很简单的例子，我们尝试解析一些用户输入。`.parse()`在这里接受一个`&str`，并试图把它变成一个`f32`。它返回一个 `Result`，但我们使用的是 `filter_map()`，所以我们只需抛出错误。`Err`的任何内容都会变成`None`，并被`.filter_map()`过滤掉。

```rust
fn main() {
    let user_input = vec!["8.9", "Nine point nine five", "8.0", "7.6", "eleventy-twelve"];

    let actual_numbers = user_input
        .into_iter()
        .filter_map(|input| input.parse::<f32>().ok())
        .collect::<Vec<f32>>();

    println!("{:?}", actual_numbers);
}
```

将打印: `[8.9, 8.0, 7.6]`。

与`.ok()`相对的是`.ok_or()`和`ok_or_else()`。这样就把`Option`变成了`Result`。之所以叫`.ok_or()`，是因为`Result`给出了一个`Ok`**或**`Err`，所以你必须让它知道`Err`的值是多少。这是因为`None`中的`Option`没有任何信息。另外，你现在可以看到，这些方法名称中的*else*部分意味着它有一个闭包。

我们可以把我们的`Option`从`Company`结构中取出来，然后这样把它变成一个`Result`。对于长期的错误处理，最好是创建自己的错误类型。
 但是现在我们只是给它一个错误信息，所以它就变成了`Result<String, &str>`。

```rust
// main() 之前的内容完全一样
struct Company {
    name: String,
    ceo: Option<String>,
}

impl Company {
    fn new(name: &str, ceo: &str) -> Self {
        let ceo = match ceo {
            "" => None,
            name => Some(name.to_string()),
        };
        Self {
            name: name.to_string(),
            ceo,
        }
    }

    fn get_ceo(&self) -> Option<String> {
        self.ceo.clone()
    }
}

fn main() {
    let company_vec = vec![
        Company::new("Umbrella Corporation", "Unknown"),
        Company::new("Ovintiv", "Doug Suttles"),
        Company::new("The Red-Headed League", ""),
        Company::new("Stark Enterprises", ""),
    ];

    let mut results_vec = vec![]; // 假装我们也要收集错误结果

    company_vec
        .iter()
        .for_each(|company| results_vec.push(company.get_ceo().ok_or("No CEO found")));

    for item in results_vec {
        println!("{:?}", item);
    }
}
```

这行是最大的变化:

```rust
// 🚧
.for_each(|company| results_vec.push(company.get_ceo().ok_or("No CEO found")));
```

它的意思是:"每家公司，用`get_ceo()`. 如果你得到了，那就把`Ok`里面的数值传给你。如果没有，就在`Err`里面传递 "没有找到CEO"。然后把这个推到vec里。"

所以当我们打印`results_vec`的时候，就会得到这样的结果。

```text
Ok("Unknown")
Ok("Doug Suttles")
Err("No CEO found")
Err("No CEO found")
```

所以现在我们有了所有四个条目。现在让我们使用 `.ok_or_else()`，这样我们就可以使用一个闭包，并得到一个更好的错误信息。现在我们有空间使用`format!`来创建一个`String`，并将公司名称放在其中。然后我们返回`String`。

```rust
// main() 之前的内容完全一样
struct Company {
    name: String,
    ceo: Option<String>,
}

impl Company {
    fn new(name: &str, ceo: &str) -> Self {
        let ceo = match ceo {
            "" => None,
            name => Some(name.to_string()),
        };
        Self {
            name: name.to_string(),
            ceo,
        }
    }

    fn get_ceo(&self) -> Option<String> {
        self.ceo.clone()
    }
}

fn main() {
    let company_vec = vec![
        Company::new("Umbrella Corporation", "Unknown"),
        Company::new("Ovintiv", "Doug Suttles"),
        Company::new("The Red-Headed League", ""),
        Company::new("Stark Enterprises", ""),
    ];

    let mut results_vec = vec![];

    company_vec.iter().for_each(|company| {
        results_vec.push(company.get_ceo().ok_or_else(|| {
            let err_message = format!("No CEO found for {}", company.name);
            err_message
        }))
    });

    for item in results_vec {
        println!("{:?}", item);
    }
}
```

这样一来，我们就有了。

```text
Ok("Unknown")
Ok("Doug Suttles")
Err("No CEO found for The Red-Headed League")
Err("No CEO found for Stark Enterprises")
```


`.and_then()`是一个有用的方法，它接收一个`Option`，然后让你对它的值做一些事情，并把它传递出去。所以它的输入是一个 `Option`，输出也是一个 `Option`。这有点像一个安全的 "解包，然后做一些事情，然后再包"。

一个简单的例子是，我们使用 `.get()` 从一个 vec 中得到一个数字，因为它返回一个 `Option`。现在我们可以把它传给 `and_then()`，如果它是 `Some`，我们可以对它做一些数学运算。如果是`None`，那么`None`就会被传递过去。

```rust
fn main() {
    let new_vec = vec![8, 9, 0]; // 只是一个装数字的 Vec

    let number_to_add = 5;       // 稍后用在计算里
    let mut empty_vec = vec![];  // 结果放这里


    for index in 0..5 {
        empty_vec.push(
            new_vec
               .get(index)
                .and_then(|number| Some(number + 1))
                .and_then(|number| Some(number + number_to_add))
        );
    }
    println!("{:?}", empty_vec);
}
```

这就打印出了`[Some(14), Some(15), Some(6), None, None]`。你可以看到`None`并没有被过滤掉，只是传递了。




`.and()`有点像`Option`的`bool`。你可以匹配很多个`Option`，如果它们都是`Some`，那么它会给出最后一个。而如果其中一个是`None`，那么就会给出`None`。

首先这里有一个`bool`的例子来帮助想象。你可以看到，如果你用的是`&&`(和)，哪怕是一个`false`，也会让一切`false`。

```rust
fn main() {
    let one = true;
    let two = false;
    let three = true;
    let four = true;

    println!("{}", one && three); // 打印 true
    println!("{}", one && two && three && four); // 打印 false
}
```

现在这里的`.and()`也是一样的。想象一下，我们做了五次操作，并把结果放在一个Vec<Option<&str>>中。如果我们得到一个值，我们就把`Some("success!")`推到Vec中。然后我们再做两次这样的操作。之后我们用`.and()`每次只显示得到`Some`的索引。

```rust
fn main() {
    let first_try = vec![Some("success!"), None, Some("success!"), Some("success!"), None];
    let second_try = vec![None, Some("success!"), Some("success!"), Some("success!"), Some("success!")];
    let third_try = vec![Some("success!"), Some("success!"), Some("success!"), Some("success!"), None];

    for i in 0..first_try.len() {
        println!("{:?}", first_try[i].and(second_try[i]).and(third_try[i]));
    }
}
```

这个打印:

```text
None
None
Some("success!")
Some("success!")
None
```

第一个(索引0)是`None`，因为在`second_try`中有一个`None`为索引0。第二个是`None`，因为在`first_try`中有一个`None`。其次是`Some("success!")`，因为`first_try`、`second try`、`third_try`中没有`None`。



`.any()`和`.all()`在迭代器中非常容易使用。它们根据你的输入返回一个`bool`。在这个例子中，我们做了一个非常大的vec(大约20000个元素)，包含了从`'a'`到`'働'`的所有字符。然后我们创建一个函数来检查是否有字符在其中。

接下来我们创建一个更小的vec，问它是否都是字母(用`.is_alphabetic()`方法)。然后我们问它是不是所有的字符都小于韩文字符`'행'`。

还要注意放一个参照物，因为`.iter()`给了一个参照物，你需要一个`&`和另一个`&`进行比较。

```rust
fn in_char_vec(char_vec: &Vec<char>, check: char) {
    println!("Is {} inside? {}", check, char_vec.iter().any(|&char| char == check));
}

fn main() {
    let char_vec = ('a'..'働').collect::<Vec<char>>();
    in_char_vec(&char_vec, 'i');
    in_char_vec(&char_vec, '뷁');
    in_char_vec(&char_vec, '鑿');

    let smaller_vec = ('A'..'z').collect::<Vec<char>>();
    println!("All alphabetic? {}", smaller_vec.iter().all(|&x| x.is_alphabetic()));
    println!("All less than the character 행? {}", smaller_vec.iter().all(|&x| x < '행'));
}
```

这个打印:

```text
Is i inside? true
Is 뷁 inside? false
Is 鑿 inside? false
All alphabetic? false
All less than the character 행? true
```

顺便说一下，`.any()`只检查到一个匹配的元素，然后就停止了。如果它已经找到了一个匹配项，它不会检查所有的元素。如果您要在 `Vec` 上使用 `.any()`，最好把可能匹配的元素推到前面。或者你可以在 `.iter()` 之后使用 `.rev()` 来反向迭代。这里有一个这样的vec。

```rust
fn main() {
    let mut big_vec = vec![6; 1000];
    big_vec.push(5);
}
```

所以这个`Vec`有1000个`6`，后面还有一个`5`。我们假设我们要用`.any()`来看看它是否包含5。首先让我们确定`.rev()`是有效的。记住，一个`Iterator`总是有`.next()`，让你每次都检查它的工作。

```rust
fn main() {
    let mut big_vec = vec![6; 1000];
    big_vec.push(5);

    let mut iterator = big_vec.iter().rev();
    println!("{:?}", iterator.next());
    println!("{:?}", iterator.next());
}
```

它的打印。

```text
Some(5)
Some(6)
```

我们是对的:有一个`Some(5)`，然后1000个`Some(6)`开始。所以我们可以这样写。

```rust
fn main() {
    let mut big_vec = vec![6; 1000];
    big_vec.push(5);

    println!("{:?}", big_vec.iter().rev().any(|&number| number == 5));
}
```

而且因为是`.rev()`，所以它只调用`.next()`一次就停止了。如果我们不用`.rev()`，那么它将调用`.next()` 1001次才停止。这段代码显示了它。

```rust
fn main() {
    let mut big_vec = vec![6; 1000];
    big_vec.push(5);

    let mut counter = 0; // 开始计数
    let mut big_iter = big_vec.into_iter(); // 做成 Iterator

    loop {
        counter +=1;
        if big_iter.next() == Some(5) { // 一直调用 .next()，直到得到 Some(5)
            break;
        }
    }
    println!("Final counter is: {}", counter);
}
```

这将打印出 `Final counter is: 1001`，所以我们知道它必须调用 `.next()` 1001 次才能找到 5。




`.find()` 告诉你一个迭代器是否有东西，而 `.position()` 告诉你它在哪里。`.find()`与`.any()`不同，因为它返回一个`Option`，里面有值(或`None`)。同时，`.position()`也是一个带有位置号的`Option`，或`None`。换句话说

- `.find()`: "我尽量帮你拿"
- `.position()`:"我帮你找找看在哪里"

下面是一个简单的例子。

```rust
fn main() {
    let num_vec = vec![10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

    println!("{:?}", num_vec.iter().find(|&number| number % 3 == 0)); // find 接受引用，所以传 &number
    println!("{:?}", num_vec.iter().find(|&number| number * 2 == 30));

    println!("{:?}", num_vec.iter().position(|&number| number % 3 == 0));
    println!("{:?}", num_vec.iter().position(|&number| number * 2 == 30));

}
```

这个打印:

```text
Some(30) // 这是数字本身
None // 没有数字乘以 2 等于 30
Some(2) // 这是位置
None
```



使用 `.cycle()` 你可以创建一个永远循环的迭代器。这种类型的迭代器与 `.zip()` 很好地结合在一起，可以创建新的东西，就像这个例子，它创建了一个 `Vec<(i32, &str)>`。

```rust
fn main() {
    let even_odd = vec!["even", "odd"];

    let even_odd_vec = (0..6)
        .zip(even_odd.into_iter().cycle())
        .collect::<Vec<(i32, &str)>>();
    println!("{:?}", even_odd_vec);
}
```

所以，即使`.cycle()`可能永远不会结束，但当把它们压缩在一起时，另一个迭代器只运行了6次。
 也就是说，`.cycle()`所做的迭代器不会再被`.next()`调用，所以六次之后就完成了。输出的结果是

```
[(0, "even"), (1, "odd"), (2, "even"), (3, "odd"), (4, "even"), (5, "odd")]
```

类似的事情也可以用一个没有结尾的范围来完成。如果你写`0..`，那么你就创建了一个永不停止的范围。你可以很容易地使用这个方法。

```rust
fn main() {
    let ten_chars = ('a'..).take(10).collect::<Vec<char>>();
    let skip_then_ten_chars = ('a'..).skip(1300).take(10).collect::<Vec<char>>();

    println!("{:?}", ten_chars);
    println!("{:?}", skip_then_ten_chars);
}
```

两者都是打印十个字符，但第二个跳过1300位，打印的是亚美尼亚语的十个字母。

```
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
['յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ', 'ռ', 'ս', 'վ']
```


另一种流行的方法叫做`.fold()`。这个方法经常用于将迭代器中的元素加在一起，但你也可以做更多的事情。它与`.for_each()`有些类似。在 `.fold()` 中，你首先添加一个起始值 (如果你是把元素加在一起，那么就是 0)，然后是一个逗号，然后是闭包。结尾给你两个元素:到目前为止的总数，和下一个元素。首先这里有一个简单的例子，显示`.fold()`将元素加在一起。

```rust
fn main() {
    let some_numbers = vec![9, 6, 9, 10, 11];

    println!("{}", some_numbers
        .iter()
        .fold(0, |total_so_far, next_number| total_so_far + next_number)
    );
}
```

所以，在第1步中，它从0开始，再加上下一个数字:9。

- 第1步，从0开始，加上下一个数字9
- 然后把9加上6: 15。
- 然后把15加上9: 24。
- 然后取24，再加上10: 34。
- 最后取34，再加上11: 45。所以它的打印结果是`45`.


但是你不需要只用它来添加东西。下面是一个例子，我们在每一个字符上加一个'-'，就会变成`String`。

```rust
fn main() {
    let a_string = "I don't have any dashes in me.";

    println!(
        "{}",
        a_string
            .chars() // 现在是迭代器
            .fold("-".to_string(), |mut string_so_far, next_char| { // 从 String "-" 开始。每次可变地带入，连同下一个字符
                string_so_far.push(next_char); // 先 push 字符，再 push '-'
                string_so_far.push('-');
                string_so_far} // 别忘了把它传给下一轮
            ));
}
```

这个打印:

```text
-I- -d-o-n-'-t- -h-a-v-e- -a-n-y- -d-a-s-h-e-s- -i-n- -m-e-.-
```



还有很多其他方便的方法，比如

- `.take_while()`，只要得到`true`，就会带入一个迭代器(例如`take while x > 5`)
- `.cloned()`，它在迭代器内做了一个克隆。这将一个引用变成了一个值。
- `.by_ref()`，它使迭代器取一个引用。这很好的保证了你使用`Vec`或类似的方法来创建迭代器后可以使用它。
- 许多其他的`_while`方法:`.skip_while()`、`.map_while()`等等。
- `.sum()`:就是把所有的东西加在一起。



`.chunks()`和`.windows()`是将矢量切割成你想要的尺寸的两种方法。你把你想要的尺寸放在括号里。比如说你有一个有10个元素的矢量，你想要一个3的尺寸，它的工作原理是这样的。

- `.chunks()`会给你4个切片: [0, 1, 2], 然后是[3, 4, 5], 然后是[6, 7, 8], 最后是[9]. 所以它会尝试用三个元素创建一个切片，但如果它没有三个元素，那么它就不会崩溃。它只会给你剩下的东西。

- `.windows()`会先给你一个[0, 1, 2]的切片。然后它将移过一片，给你[1, 2, 3]。它将一直这样做，直到最后到达3的最后一片，然后停止。

所以让我们在一个简单的数字向量上使用它们。它看起来像这样:

```rust
fn main() {
    let num_vec = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 0];

    for chunk in num_vec.chunks(3) {
        println!("{:?}", chunk);
    }
    println!();
    for window in num_vec.windows(3) {
        println!("{:?}", window);
    }
}
```

这个打印:

```text
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
[0]

[1, 2, 3]
[2, 3, 4]
[3, 4, 5]
[4, 5, 6]
[5, 6, 7]
[6, 7, 8]
[7, 8, 9]
[8, 9, 0]
```

顺便说一下，如果你什么都不给它，`.chunks()`会崩溃。你可以为一个只有一项的向量写`.chunks(1000)`，但你不能为任何长度为0的东西写`.chunks()`。 如果你点击[src]，你可以在函数中看到这一点，因为它说`assert!(chunk_size != 0);`。



`.match_indices()` 让你把 `String` 或 `&str` 里面所有符合你的输入的东西都提取出来，并给你索引。它与 `.enumerate()` 类似，因为它返回一个包含两个元素的元组。

```rust
fn main() {
    let rules = "Rule number 1: No fighting. Rule number 2: Go to bed at 8 pm. Rule number 3: Wake up at 6 am.";
    let rule_locations = rules.match_indices("Rule").collect::<Vec<(_, _)>>(); // 实际是 Vec<(usize, &str)>，这里让 Rust 自己推断
    println!("{:?}", rule_locations);
}
```

这个打印:

```text
[(0, "Rule"), (28, "Rule"), (62, "Rule")]
```



`.peekable()` 让你创建一个迭代器，在那里你可以看到 (窥视) 下一个元素。它就像调用 `.next()` (它给出了一个 `Option`)，除了迭代器不会移动，所以你可以随意使用它。实际上，你可以把peekable看成是 "可停止"的，因为你可以想停多久就停多久。下面是一个例子，我们对每个元素都使用`.peek()`三次。我们可以永远使用`.peek()`，直到我们使用`.next()`移动到下一个元素。

```rust
fn main() {
    let just_numbers = vec![1, 5, 100];
    let mut number_iter = just_numbers.iter().peekable(); // 这其实创建了一种叫 Peekable 的迭代器

    for _ in 0..3 {
        println!("I love the number {}", number_iter.peek().unwrap());
        println!("I really love the number {}", number_iter.peek().unwrap());
        println!("{} is such a nice number", number_iter.peek().unwrap());
        number_iter.next();
    }
}
```

这个打印:

```text
I love the number 1
I really love the number 1
1 is such a nice number
I love the number 5
I really love the number 5
5 is such a nice number
I love the number 100
I really love the number 100
100 is such a nice number
```

下面是另一个例子，我们使用`.peek()`对一个元素进行匹配。使用完后，我们调用`.next()`。


```rust
fn main() {
    let locations = vec![
        ("Nevis", 25),
        ("Taber", 8428),
        ("Markerville", 45),
        ("Cardston", 3585),
    ];
    let mut location_iter = locations.iter().peekable();
    while location_iter.peek().is_some() {
        match location_iter.peek() {
            Some((name, number)) if *number < 100 => { // .peek() 给出引用，所以需要 *
                println!("Found a hamlet: {} with {} people", name, number)
            }
            Some((name, number)) => println!("Found a town: {} with {} people", name, number),
            None => break,
        }
        location_iter.next();
    }
}
```

这个打印:

```text
Found a hamlet: Nevis with 25 people
Found a town: Taber with 8428 people
Found a hamlet: Markerville with 45 people
Found a town: Cardston with 3585 people
```

最后，这里有一个例子，我们也使用`.match_indices()`。在这个例子中，我们根据`&str`中的空格数，将名字放入`struct`中。

```rust
#[derive(Debug)]
struct Names {
    one_word: Vec<String>,
    two_words: Vec<String>,
    three_words: Vec<String>,
}

fn main() {
    let vec_of_names = vec![
        "Caesar",
        "Frodo Baggins",
        "Bilbo Baggins",
        "Jean-Luc Picard",
        "Data",
        "Rand Al'Thor",
        "Paul Atreides",
        "Barack Hussein Obama",
        "Bill Jefferson Clinton",
    ];

    let mut iter_of_names = vec_of_names.iter().peekable();

    let mut all_names = Names { // 从一个空的 Names 结构体开始
        one_word: vec![],
        two_words: vec![],
        three_words: vec![],
    };

    while iter_of_names.peek().is_some() {
        let next_item = iter_of_names.next().unwrap(); // 可以用 .unwrap()，因为我们知道是 Some
        match next_item.match_indices(' ').collect::<Vec<_>>().len() { // 用 .match_indices 快速建一个 Vec 并检查长度
            0 => all_names.one_word.push(next_item.to_string()),
            1 => all_names.two_words.push(next_item.to_string()),
            _ => all_names.three_words.push(next_item.to_string()),
        }
    }

    println!("{:?}", all_names);
}
```

这将打印:

```text
Names { one_word: ["Caesar", "Data"], two_words: ["Frodo Baggins", "Bilbo Baggins", "Jean-Luc Picard", "Rand Al\'Thor", "Paul Atreides"], three_words:
["Barack Hussein Obama", "Bill Jefferson Clinton"] }
```
