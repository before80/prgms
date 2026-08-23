+++
title = "5 类型上的生命周期"
date = 2026-08-23T16:26:00+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_5.html](https://tfpk.github.io/lifetimekata/chapter_5.html)

到目前为止，我们只讨论过应用于函数的生命周期。
函数并不是唯一需要显式生命周期的地方。类型（结构体和枚举）也可以有生命周期。

这是因为如果结构体包含引用，用户需要说明它能存活多久。

假设我们想把一个 `&str` 分成两部分，并创建一个带有 `start` 和 `end` 字段的结构体？

我们可以这样写函数：

```rust
struct SplitStr {
    start: &str,
    end: &str
}

fn split<'text, 'delim>(text: &'text str, delimiter: &'delim str) -> Option<SplitStr> {
    let (start, end) = text.split_once(delimiter)?;
    
    Some(SplitStr {
        start,
        end
    })
}

# fn main() {}
```

这样就完成了！对吧？

那么，那些字符串引用能存活多久呢？

如果我们这样调用函数会怎样：


```rust
# struct SplitStr {
#     start: &str,
#     end: &str
# }
# 
# fn split<'text, 'delim>(text: &'text str, delimiter: &'delim str) -> Option<SplitStr> {
#     let (start, end) = text.split_once(delimiter)?;
#     
#     Some(SplitStr {
#         start,
#         end
#     })
# }

fn main() {
    let mut parts_of_string: Option<SplitStr> = None;
    {
        let my_string = String::from("First line;Second line");
        parts_of_string = split(&my_string, ";");
    }
    
    println!("{parts_of_string:?}");
}
```

那么，`SplitStr` 结构体内部的引用现在就悬空了，
因为它们都指向 `my_string`；而 `my_string` 只存在于花括号内部。

因此，Rust 强制我们指定结构体内所有引用的生命周期。
下面是我们修复代码的方式：

```rust
struct SplitStr<'str_lifetime> {
    start: &'str_lifetime str,
    end: &'str_lifetime str
}

fn split<'text, 'delim>(text: &'text str, delimiter: &'delim str) -> Option<SplitStr<'text>> {
    let (start, end) = text.split_once(delimiter)?;
    
    Some(SplitStr {
        start,
        end
    })
}

# fn main() {}
```

现在，当我们返回 `Option<SplitStr<'text>>` 时，编译器知道结构体内部的引用
都必须与 `'text` 存活同样长的时间。如果我们尝试返回一个引用无法存活 `'text` 的 `SplitStr`，
那将是编译错误。

## 关于枚举的说明

引用在枚举中的工作方式与在结构体中完全相同。
我们这里不详细展开，因为它们是可以互换的。

```rust
enum StringOption<'a> {
    Some(&'a str),
    None
}
# fn main() {}
```


## 两个生命周期

偶尔，结构体上会有多个生命周期。
当其中的数据来自两个不同的地方、具有两个生命周期时，就会发生这种情况。

以在一个程序中找出两句话之间不重复单词为例。

第一句话可能是 `"I love to swim and surf."`，第二句是 `"I love to ski and snowboard."`。第一句独有的词是 `"swim"` 和 `"surf"`。第二句独有的词是 `"ski"` 和 `"snowboard"`。

如果你说两句话必须共享一个生命周期，就会
强迫用户确保两句话来自同一个
地方，因此具有相同的生命周期。但如果一句来自程序运行期间一直打开的文件，而第二句是在
循环内部扫描进来的呢？

在这种情况下，编译器会坚持要求扫描进来的值在整个程序期间都保存着，这就不够人性化了。

## 练习：结构体上的两个生命周期

在本练习中，我们将修改一个找出两个字符串之间不重复单词的小程序。目前它没有任何生命周期
标注，因此无法编译。

我们的目标是返回一个结构体，其中包含第一个字符串的所有不重复单词，以及第二个字符串的所有不重复单词。它们应该
具有各自独立的生命周期。
