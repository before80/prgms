+++
title = "48-函数中的闭包"
date = 2026-08-21T12:46:00+08:00
weight = 49
type = "docs"
description = "函数中的闭包 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_47.html](https://dhghomon.github.io/easy_rust/Chapter_47.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 函数中的闭包

闭包是伟大的。那么我们如何把它们放到自己的函数中呢？

你可以创建自己的函数来接受闭包，但是在函数里面就不那么自由了，你必须决定类型。在函数外部，一个闭包可以在`Fn`、`FnMut`和`FnOnce`之间自行决定，但在函数内部你必须选择一个。最好的理解方式是看几个函数签名。
 这里是`.all()`的那个。我们记得，它检查一个迭代器，看看所有的东西是否是`true`(取决于你决定是`true`还是`false`)。它的部分签名是这样说的。


```rust
    fn all<F>(&mut self, f: F) -> bool    // 🚧
    where
        F: FnMut(Self::Item) -> bool,
```

`fn all<F>`:这告诉你有一个通用类型`F`。一个闭包总是泛型，因为每次都是不同的类型。

`(&mut self, f: F)`:`&mut self`告诉你这是一个方法。`f: F`通常你看到的是一个闭包:这是变量名和类型。 当然，`f`和`F`并没有什么特别之处，它们可以是不同的名字。如果你愿意，你可以写`my_closure: Closure`--这并不重要。但在签名中，你几乎总是看到`f: F`。

接下来是关于闭包的部分:`F: FnMut(Self::Item) -> bool`。在这里，它决定了闭包是 `FnMut`，所以它可以改变值。它改变了`Self::Item`的值，这是它所取的迭代器。而且它必须返回 `true` 或 `false`。

这里是一个更简单的签名，有一个闭包。

```rust
fn do_something<F>(f: F)    // 🚧
where
    F: FnOnce(),
{
    f();
}
```

这只是说它接受一个闭包，取值(`FnOnce`=取值)，而不返回任何东西。所以现在我们可以调用这个什么都不取的闭包，做我们喜欢做的事情。我们将创建一个 `Vec`，然后对它进行迭代，只是为了展示我们现在可以做什么。

```rust
fn do_something<F>(f: F)
where
    F: FnOnce(),
{
    f();
}

fn main() {
    let some_vec = vec![9, 8, 10];
    do_something(|| {
        some_vec
            .into_iter()
            .for_each(|x| println!("The number is: {}", x));
    })
}
```

一个更真实的例子，我们将再次创建一个 `City` 结构体。这次 `City` 结构体有更多关于年份和人口的数据。它有一个 `Vec<u32>` 来表示所有的年份，还有一个 `Vec<u32>` 来表示所有的人口。

`City`有两个方法:`new()`用于创建一个新的`City`, `.city_data()`有个闭包参数。当我们使用 `.city_data()` 时，它给我们提供了年份和人口以及一个闭包，所以我们可以对数据做我们想做的事情。闭包类型是 `FnMut`，所以我们可以改变数据。它看起来像这样:

```rust
#[derive(Debug)]
struct City {
    name: String,
    years: Vec<u32>,
    populations: Vec<u32>,
}

impl City {
    fn new(name: &str, years: Vec<u32>, populations: Vec<u32>) -> Self {

        Self {
            name: name.to_string(),
            years,
            populations,
        }
    }

    fn city_data<F>(&mut self, mut f: F) // 引入 self，但只有 f 是泛型 F。f 就是闭包

    where
        F: FnMut(&mut Vec<u32>, &mut Vec<u32>), // 闭包接受 u32 的可变向量
                                                // 也就是年份和人口数据
    {
        f(&mut self.years, &mut self.populations) // 这才是真正的函数体。它的意思是
                                                  // “对 self.years 和 self.populations 使用闭包”
                                                  // 闭包里可以做任何想做的事
    }
}

fn main() {
    let years = vec![
        1372, 1834, 1851, 1881, 1897, 1925, 1959, 1989, 2000, 2005, 2010, 2020,
    ];
    let populations = vec![
        3_250, 15_300, 24_000, 45_900, 58_800, 119_800, 283_071, 478_974, 400_378, 401_694,
        406_703, 437_619,
    ];
    // 现在可以创建城市了
    let mut tallinn = City::new("Tallinn", years, populations);

    // 现在有了带闭包的 .city_data() 方法。我们可以为所欲为。

    // 先把 5 年的数据合在一起打印。
    tallinn.city_data(|city_years, city_populations| { // 参数名可以随便起
        let new_vec = city_years
            .into_iter()
            .zip(city_populations.into_iter()) // 把两者 zip 在一起
            .take(5)                           // 但只取前 5 个
            .collect::<Vec<(_, _)>>(); // 让 Rust 推断元组里的类型
        println!("{:?}", new_vec);
    });

    // 现在为 2030 年加一些数据
    tallinn.city_data(|x, y| { // 这次参数就叫 x 和 y
        x.push(2030);
        y.push(500_000);
    });

    // 我们不要 1834 年的数据了
    tallinn.city_data(|x, y| {
        let position_option = x.iter().position(|x| *x == 1834);
        if let Some(position) = position_option {
            println!(
                "Going to delete {} at position {:?} now.",
                x[position], position
            ); // 确认删对了项
            x.remove(position);
            y.remove(position);
        }
    });

    println!(
        "Years left are {:?}\nPopulations left are {:?}",
        tallinn.years, tallinn.populations
    );
}
```

这将打印出我们调用`.city_data().`的所有时间的结果:

```text
[(1372, 3250), (1834, 15300), (1851, 24000), (1881, 45900), (1897, 58800)]
Going to delete 1834 at position 1 now.
Years left are [1372, 1851, 1881, 1897, 1925, 1959, 1989, 2000, 2005, 2010, 2020, 2030]
Populations left are [3250, 24000, 45900, 58800, 119800, 283071, 478974, 400378, 401694, 406703, 437619, 500000]
```
