+++
title = "2 生命周期详解"
date = 2026-08-23T16:26:00+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_2.html](https://tfpk.github.io/lifetimekata/chapter_2.html)

我们可以看到，悬垂引用是因为函数丢失了关于引用来源的信息而产生的。

编译器只有在了解输入与输出的生命周期如何相互关联时，才能判断函数是否正确。因此我们需要告诉编译器：哪些输入与输出的生命周期是相同的。

我们可以告诉编译器：「只要这些输入/输出的生命周期相同，我的函数对任意生命周期都成立」。来看看相关语法：

```rust
fn some_if_greater<'lifetime1, 'lifetime2>(number: &'lifetime1 i32, greater_than: &'lifetime2 i32) -> Option<&'lifetime1 i32> {
    if number > greater_than {
        Some(number)
    } else {
        None
    }
}
# fn main() {
#     let (n, gt) = (7, 4);
#     let test = some_if_greater(&n, &gt);
# }
```

逐步说明其作用：

 - `fn my_function<'lifetime1, 'lifetime2>(...)`：我们为程序所需的生命周期选取名称。
 - `number: &'lifetime1 i32`：告诉编译器，该引用必须在名为 `'lifetime1` 的代码区域内有效。
 - `greater_than: &'lifetime2 i32`：告诉编译器，该引用必须在名为 `'lifetime2` 的代码区域内有效。这意味着 `greater_than` 与 `number` 的生命周期不必有任何关联。
 - `-> Option<&'lifetime1 i32>`：生命周期在这里至关重要。我们说的是 `number` 与返回值必须在完全相同的代码区域内有效。

也就是说，我们告诉编译器：只有当 `number` 与返回值在相同的代码区域内都有效时，才能调用这个函数。

# 练习：标注生命周期

为初步练习，本节要求你对前两章中的一些例子标注生命周期。

你需要：
 - 判断需要多少个生命周期参数
 - 为每个生命周期参数命名，并放在函数名后的 `<` 尖括号 `>` 中
 - 为每个引用标注恰当的生命周期
 - 确认代码能通过编译
 - 思考每个生命周期可能对应哪段代码区域
 
你会注意到每个函数都有 `#[lifetimes_required(!)]` 注解。完成练习时需要保留它。它会指示编译器在你遗漏生命周期时抛出错误，即使编译器本不需要该生命周期。
