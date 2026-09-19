+++
title = "第二篇 语言主干"
weight = 20
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "常量、字符串、正则、运算符、可选值、集合、控制流、函数、闭包、错误处理与语法糖"
isCJKLanguage = true
draft = false
+++

# 第二篇：语言主干

> 这一篇的十三个章节，是 Swift 日常代码里出现频率最高的部分。学完之后，你已经能读懂绝大多数 Swift 文件。

顺序不是随便排的：先用类型和字符串建立“值”的概念，再学会用运算符和集合处理数据，然后用控制流、函数、闭包把逻辑组织起来，最后用错误处理收尾——把失败也变成类型系统能管住的东西。

其中第 5 章的字符串索引、第 9 章的可选值、第 12 章的 `switch` 模式匹配，是三个最容易“以为自己懂了”的地方，值得放慢速度。第 15B 章则像一篇“写法总复习”：把前面各章零散出现的短写法集中起来，并说清它们的边界。

## 本篇章节

1. [常量、变量与数值]({{< relref "Chapter-04-Constants-Variables-and-Numbers.md" >}})
2. [字符串与字符]({{< relref "Chapter-05-Strings-and-Characters.md" >}})
3. [正则表达式]({{< relref "Chapter-06-Regular-Expressions.md" >}})
4. [运算符与表达式]({{< relref "Chapter-07-Operators-and-Expressions.md" >}})
5. [元组、类型别名与基础类型判断]({{< relref "Chapter-08-Tuples-Typealias-and-Type-Checking.md" >}})
6. [可选值]({{< relref "Chapter-09-Optionals.md" >}})
7. [集合]({{< relref "Chapter-10-Collections.md" >}})
8. [控制流（一）]({{< relref "Chapter-11-Control-Flow-Part-1.md" >}})
9. [控制流（二）：switch 与模式匹配]({{< relref "Chapter-12-Control-Flow-Part-2.md" >}})
10. [函数]({{< relref "Chapter-13-Functions.md" >}})
11. [闭包]({{< relref "Chapter-14-Closures.md" >}})
12. [错误处理]({{< relref "Chapter-15-Error-Handling.md" >}})
13. [语法糖与特殊写法]({{< relref "Chapter-15B-Sugar-and-Special-Forms.md" >}})

## 读完你应该能

- 判断什么时候该用 `let`、什么时候必须用 `var`，并且说清类型推断的边界。
- 解释为什么字符串下标不能用整数，并正确使用索引与切片。
- 用 `if let`、`guard let`、`??` 处理可选值，而不是到处 `!`。
- 用 `switch` 做区间、元组、枚举和可选值的模式匹配。
- 把失败写成 `throws`、`do-catch` 和 `Result`，而不是返回一个魔法数字。
- 认出常见语法糖（省 `return`、隐式 `self`、`if let x`、`map(\.name)`、`if`/`switch` 表达式），并知道它们各自的限制。
