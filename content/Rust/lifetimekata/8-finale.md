+++
title = "8 终章"
date = 2026-08-23T16:26:00+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++


> 原文链接: [https://tfpk.github.io/lifetimekata/chapter_8.html](https://tfpk.github.io/lifetimekata/chapter_8.html)

恭喜你读到了 LifetimeKata 的结尾。接下来两章还有更多脚注和延伸阅读，但这一章可以算是某种意义上的「终章」。

在本练习中，我们将构建一个非常简单的 glob 系统克隆。
它可以让使用者判断某段文本是否符合某种描述。

值得一提的是，完整实现整个练习可能需要长达一小时。如果你只想练习生命周期相关的内容，
可以从 `solution` 复制代码，但完整做完这个练习既有趣也很有收获。

例如，glob 模式 `ab(cd|ef|gh)` 可以匹配以下任意字符串：`abcd`、`abef`、`abgh`。

你将创建一个 `Matcher` 结构体，它有三个字段：

 - 一个 `&str`，表示我们正则表达式的文本形式。
 - 一个 `Vec<MatcherTokens>`，按顺序表示正则表达式的各个组成部分。
 - 一个整数，用于记录我们的正则表达式最长匹配到了多少。

要创建它，你会拿到类似这样的字符串：`hello.(town|world|universe).its.me`。
它包含三种组成部分：

 - 普通文本，例如 `hello`、`its` 或 `me`，只应匹配完全相同的文本
 - 通配符（`.` 字符），匹配任意单个字符。
 - 可选文本，例如 `(town|world|universe)`，匹配列表中的恰好一个
   字符串。因此 `(town|world|universe)` 匹配 `town`，或 `world`，或 `universe`。
   
 这些组成部分可以任意顺序组合（但不会出现彼此嵌套的情况）。
 对于这个字符串，你应创建一个 `MatcherTokens` 向量，其中的元素引用该字符串的相应部分。
 
 然后你会编写一个函数，接收另一个字符串，并判断该字符串与 `Matcher`
 匹配了多少。你会返回一个 `(MatcherToken, &str)` 的向量，其中
 `MatcherToken` 是匹配到某段文本的 token，`&str` 是被匹配到的文本。
 
 
## 示例

假设你有匹配器 `(Black|Bridge)(rock|stone|water).company`。它可以拆成四部分：
 - `OneOfText(["Black", "Bridge"])`
 - `OneOfText(["rock", "stone", "water"])`
 - `Wildcard`
 - `RawText("company")`

现在，假设我们得到以下文本：`BlackBridge`。`Black` 匹配第一个 token，
但 `Bridge` 不匹配第二个 token。
因此，我们会返回：`vec![(OneOfText(["Black", "Bridge"]), "Black")]`。我们匹配到的 token 数量最多为 1。

再看另一个例子：`Bridgestone_Tyres`。
`Bridge` 匹配第一个匹配器，`stone` 匹配
第二个匹配器，`_` 匹配第三个匹配器，
但 `Tyres` 不匹配 `company`。因此我们最多匹配到 3 个 token。我们会返回一个包含以下内容的 vec：
 
 - (`OneOfText(["Black", "Bridge"])`, `Bridge`)
 - (`OneOfText(["rock", "stone", "water"])`, `"stone"`)
 - (`Wildcard`, `"_"`)

### 关于 Unicode 的说明

Rust 可以在字符串中处理 Unicode 字符（例如 emoji 或日文汉字）。
当然，这会让像把字符串拆成片段这样的简单操作变得更复杂，
因为有可能不小心把某个字符从中间切开。

示例中的测试*并未*使用 Unicode，但如果你想获得更「正宗」的 Rust 体验，
可以把测试改成包含 Unicode 字符（注释里有一个例子）。
