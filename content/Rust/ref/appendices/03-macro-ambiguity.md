+++
title = "03-宏 follow 集歧义形式化规范"
date = 2026-08-18T08:45:00+08:00
weight = 118
type = "docs"
description = "宏 follow 集歧义形式化规范 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/macro-ambiguity.html](https://doc.rust-lang.org/reference/macro-ambiguity.html)

r[macro.ambiguity]
# 宏 follow 集歧义形式化规范

本页记录 [Macros By Example] 的 follow 规则的形式化规范。它们最初在 [RFC 550] 中规定，本文大部分文字即摘自该 RFC，并在后续 RFC 中加以扩展。

r[macro.ambiguity.convention]
## 定义与约定

r[macro.ambiguity.convention.defs]
  - `macro`：源码中任何可按 `foo!(...)` 调用的东西。
  - `MBE`：macro-by-example，由 `macro_rules` 定义的宏。
  - `matcher`：`macro_rules` 调用中一条规则的左侧，或其某一子部分。
  - `macro parser`：Rust 解析器中将使用由所有 matcher 导出的文法来解析输入的那部分代码。
  - `fragment`：给定 matcher 将接受（或“匹配”）的那一类 Rust 语法。
  - `repetition`：遵循规则重复模式的 fragment
  - `NT`：非终结符，可出现在 matcher 中的各种“元变量”或重复 matcher，在 MBE 语法中以前导 `$` 字符指定。
  - `simple NT`：“元变量”非终结符（下文进一步讨论）。
  - `complex NT`：经由重复运算符（`*`、`+`、`?`）指定的重复匹配非终结符。
  - `token`：matcher 的原子元素；即标识符、运算符、开/闭定界符，*以及* simple NT。
  - `token tree`：由 token（叶节点）、complex NT 以及 token tree 的有限序列形成的树结构。
  - `delimiter token`：意在划分一个 fragment 的结尾与下一 fragment 的开头的 token。
  - `separator token`：complex NT 中可选的 delimiter token，用于分隔所匹配重复中的每一对元素。
  - `separated complex NT`：具有自己的 separator token 的 complex NT。
  - `delimited sequence`：在序列起止处带有适当开、闭定界符的 token tree 序列。
  - `empty fragment`：分隔 token 的那一类不可见 Rust 语法，即空白，或（在某些词法上下文中）空 token 序列。
  - `fragment specifier`：simple NT 中指定该 NT 接受何种 fragment 的标识符。
  - `language`：上下文无关语言。

示例：

```rust
macro_rules! i_am_an_mbe {
    (start $foo:expr $($i:ident),* end) => ($foo)
}
```

r[macro.ambiguity.convention.matcher]
`(start $foo:expr $($i:ident),* end)` 是一个 matcher。整个 matcher 是一个 delimited sequence（开、闭定界符为 `(` 与 `)`），而 `$foo` 与 `$i` 是分别以 `expr` 与 `ident` 为 fragment specifier 的 simple NT。

r[macro.ambiguity.convention.complex-nt]
`$(i:ident),*` *也*是一个 NT；它是匹配逗号分隔的标识符重复的 complex NT。`,` 是该 complex NT 的 separator token；它出现在所匹配 fragment 的每一对元素之间（若有）。

另一个 complex NT 的例子是 `$(hi $e:expr ;)+`，它匹配形如 `hi <expr>; hi <expr>; ...` 的任何 fragment，其中 `hi <expr>;` 至少出现一次。注意此 complex NT 没有专用的 separator token。

（注意，Rust 的解析器确保 delimited sequence 始终以正确嵌套的 token tree 结构以及正确匹配的开、闭定界符出现。）

r[macro.ambiguity.convention.vars]
我们倾向于用变量 “M” 表示 matcher，用变量 “t” 与 “u” 表示任意单个 token，用变量 “tt” 与 “uu” 表示任意 token tree。（使用 “tt” 因其作为 fragment specifier 的额外角色而可能带来歧义；但根据上下文将清楚意指何种解释。）

r[macro.ambiguity.convention.set]
“SEP” 将遍历 separator token，“OP” 遍历重复运算符 `*`、`+` 与 `?`，“OPEN”/“CLOSE” 遍历包围 delimited sequence 的匹配 token 对（例如 `[` 与 `]`）。

r[macro.ambiguity.convention.sequence-vars]
希腊字母 “α” “β” “γ” “δ” 表示可能为空的 token-tree 序列。（不过，希腊字母 “ε”（epsilon）在表述中有特殊角色，并不表示 token-tree 序列。）

  * 这种希腊字母约定通常仅在序列的存在是技术细节时采用；特别地，当我们希望*强调*我们在操作 token-tree 序列时，将对该序列使用记号 “tt ...”，而非希腊字母。

注意，matcher 仅仅是一个 token tree。如上所述，“simple NT” 是元变量 NT；因此它不是重复。例如，`$foo:ty` 是 simple NT，但 `$($foo:ty)+` 是 complex NT。

还要注意，在本形式化的上下文中，术语 “token” 一般*包括* simple NT。

最后，读者宜牢记：根据本形式化的定义，没有 simple NT 匹配 empty fragment，同样也没有 token 匹配 Rust 语法的 empty fragment。（因此，*唯一*能匹配 empty fragment 的 NT 是 complex NT。）这实际上并不成立，因为 `vis` matcher 可以匹配 empty fragment。因此，就本形式化而言，我们将把 `$v:vis` 实际视为 `$($v:vis)?`，并要求该 matcher 匹配 empty fragment。

r[macro.ambiguity.invariant]
### Matcher 不变量

r[macro.ambiguity.invariant.list]
要成为有效，matcher 必须满足下列三个不变量。FIRST 与 FOLLOW 的定义稍后描述。

1.  对于 matcher `M` 中任意两个相继的 token tree 序列（即 `M = ... tt uu ...`），若 `uu ...` 非空，则必须有 FOLLOW(`... tt`) ∪ {ε} ⊇ FIRST(`uu ...`)。
1.  对于 matcher 中的任意 separated complex NT，`M = ... $(tt ...) SEP OP ...`，必须有 `SEP` ∈ FOLLOW(`tt ...`)。
1.  对于 matcher 中的 unseparated complex NT，`M = ... $(tt ...) OP ...`，若 OP = `*` 或 `+`，则必须有 FOLLOW(`tt ...`) ⊇ FIRST(`tt ...`)。

r[macro.ambiguity.invariant.follow-matcher]
第一个不变量说的是：无论 matcher 之后实际跟什么 token（若有），都必须位于预先确定的 follow 集中的某处。这确保合法的宏定义将继续对何处结束 `... tt`、何处开始 `uu ...` 作出相同判定，即便向语言添加了新的语法形式。

r[macro.ambiguity.invariant.separated-complex-nt]
第二个不变量说的是：separated complex NT 必须使用属于其内部内容预先确定 follow 集的一部分的 separator token。这确保合法的宏定义将继续把输入 fragment 解析为相同的 `tt ...` delimited sequence，即便向语言添加了新的语法形式。

r[macro.ambiguity.invariant.unseparated-complex-nt]
第三个不变量说的是：当我们有一个可以匹配同一事物的两个或更多副本且其间无分隔的 complex NT 时，按第一个不变量它们必须被允许彼此相邻放置。此不变量还要求它们非空，从而消除了一种可能的歧义。

**注意：由于历史疏忽以及对既有行为的大量依赖，第三个不变量目前未被强制执行。目前尚未决定今后如何处理。不遵守该行为的宏可能在未来的 Rust edition 中变为无效。见 [tracking issue]。**

r[macro.ambiguity.sets]
### FIRST 与 FOLLOW，非正式说明

r[macro.ambiguity.sets.intro]
给定 matcher M 映射到三个集合：FIRST(M)、LAST(M) 与 FOLLOW(M)。

这三个集合均由 token 组成。FIRST(M) 与 LAST(M) 还可能包含一个特殊的非 token 元素 ε（“epsilon”），它表示 M 可以匹配 empty fragment。（但 FOLLOW(M) 始终只是 token 的集合。）

非正式地：

r[macro.ambiguity.sets.first]
  * FIRST(M)：收集将 fragment 匹配到 M 时可能首先使用的 token。

r[macro.ambiguity.sets.last]
  * LAST(M)：收集将 fragment 匹配到 M 时可能最后使用的 token。

r[macro.ambiguity.sets.follow]
  * FOLLOW(M)：允许紧跟在由 M 匹配的某一 fragment 之后的 token 集合。

    换言之：t ∈ FOLLOW(M) 当且仅当存在（可能为空的）token 序列 α、β、γ、δ，使得：

      * M 匹配 β，

      * t 匹配 γ，并且

      * 拼接 α β γ δ 是可解析的 Rust 程序。

r[macro.ambiguity.sets.universe]
我们用简写 ANYTOKEN 表示所有 token（包括 simple NT）的集合。例如，若 matcher M 之后任意 token 都合法，则 FOLLOW(M) = ANYTOKEN。

（为检验对上述非正式描述的理解，读者此时可能想先跳到 [FIRST/LAST 的例子](#examples-of-first-and-last)，再阅读其形式化定义。）

r[macro.ambiguity.sets.def]
### FIRST、LAST

r[macro.ambiguity.sets.def.intro]
以下是 FIRST 与 LAST 的形式化归纳定义。

r[macro.ambiguity.sets.def.notation]
“A ∪ B” 表示集合并，“A ∩ B” 表示集合交，“A \\ B” 表示集合差（即 A 中不在 B 中出现的所有元素）。

r[macro.ambiguity.sets.def.first]
#### FIRST

r[macro.ambiguity.sets.def.first.intro]
FIRST(M) 通过对序列 M 及其第一个 token-tree（若有）的结构进行情形分析来定义：

r[macro.ambiguity.sets.def.first.epsilon]
  * 若 M 是空序列，则 FIRST(M) = { ε }，

r[macro.ambiguity.sets.def.first.token]
  * 若 M 以 token t 开头，则 FIRST(M) = { t }，

    （注意：这涵盖 M 以 delimited token-tree 序列开头的情形，`M = OPEN tt ... CLOSE ...`，此时 `t = OPEN`，因而 FIRST(M) = { `OPEN` }。）

    （注意：这关键地依赖于没有 simple NT 匹配 empty fragment 这一性质。）

r[macro.ambiguity.sets.def.first.complex]
  * 否则，M 是以 complex NT 开头的 token-tree 序列：`M = $( tt ... ) OP α`，或 `M = $( tt ... ) SEP OP α`，（其中 `α` 是 matcher 其余部分的（可能为空的）token tree 序列）。

      * 令 SEP\_SET(M) = { SEP } 若 SEP 存在且 ε ∈ FIRST(`tt ...`)；否则 SEP\_SET(M) = {}。

  * 令 ALPHA\_SET(M) = FIRST(`α`) 若 OP = `*` 或 `?`，且 ALPHA\_SET(M) = {} 若 OP = `+`。
  * FIRST(M) = (FIRST(`tt ...`) \\ {ε}) ∪ SEP\_SET(M) ∪ ALPHA\_SET(M)。

complex NT 的定义值得一些说明。SEP\_SET(M) 定义了 separator 可能成为 M 的有效首 token 的可能性，这发生在定义了 separator 且重复 fragment 可能为空时。ALPHA\_SET(M) 定义了 complex NT 可能为空的可能性，意味着 M 的有效首 token 是后续 token-tree 序列 `α` 的那些。这发生在使用 `*` 或 `?` 时，此时可能有零次重复。理论上，若 `+` 与可能为空的重复 fragment 一起使用，这也可能发生，但这被第三个不变量所禁止。

由此，显然 FIRST(M) 可以包含来自 SEP\_SET(M) 或 ALPHA\_SET(M) 的任何 token，并且若 complex NT 匹配非空，则任何以 FIRST(`tt ...`) 开头的 token 也可以。最后需要考虑的是 ε。SEP\_SET(M) 与 FIRST(`tt ...`) \\ {ε} 不能包含 ε，但 ALPHA\_SET(M) 可以。因此，此定义允许 M 接受 ε 当且仅当 ε ∈ ALPHA\_SET(M)。这是正确的，因为要让 M 在 complex NT 情形下接受 ε，complex NT 与 α 都必须接受它。若 OP = `+`，意味着 complex NT 不能为空，则按定义 ε ∉ ALPHA\_SET(M)。否则，complex NT 可以接受零次重复，于是 ALPHA\_SET(M) = FOLLOW(`α`)。因此此定义对于 ε 也是正确的。

r[macro.ambiguity.sets.def.last]
#### LAST

r[macro.ambiguity.sets.def.last.intro]
LAST(M) 通过对 M 本身（token-tree 序列）进行情形分析来定义：

r[macro.ambiguity.sets.def.last.empty]
  * 若 M 是空序列，则 LAST(M) = { ε }

r[macro.ambiguity.sets.def.last.token]
  * 若 M 是单例 token t，则 LAST(M) = { t }

r[macro.ambiguity.sets.def.last.rep-star]
  * 若 M 是重复零次或更多次的单例 complex NT，`M = $( tt ... ) *`，或 `M = $( tt ... ) SEP *`

      * 令 sep_set = { SEP } 若 SEP 存在；否则 sep_set = {}。

      * 若 ε ∈ LAST(`tt ...`)，则 LAST(M) = LAST(`tt ...`) ∪ sep_set

      * 否则，序列 `tt ...` 必须非空；LAST(M) = LAST(`tt ...`) ∪ {ε}。

r[macro.ambiguity.sets.def.last.rep-plus]
  * 若 M 是重复一次或更多次的单例 complex NT，`M = $( tt ... ) +`，或 `M = $( tt ... ) SEP +`

      * 令 sep_set = { SEP } 若 SEP 存在；否则 sep_set = {}。

      * 若 ε ∈ LAST(`tt ...`)，则 LAST(M) = LAST(`tt ...`) ∪ sep_set

      * 否则，序列 `tt ...` 必须非空；LAST(M) = LAST(`tt ...`)

r[macro.ambiguity.sets.def.last.rep-question]
  * 若 M 是重复零次或一次的单例 complex NT，`M = $( tt ...) ?`，则 LAST(M) = LAST(`tt ...`) ∪ {ε}。

r[macro.ambiguity.sets.def.last.delim]
  * 若 M 是 delimited token-tree 序列 `OPEN tt ... CLOSE`，则 LAST(M) = { `CLOSE` }。

r[macro.ambiguity.sets.def.last.sequence]
  * 若 M 是非空的 token-tree 序列 `tt uu ...`，

      * 若 ε ∈ LAST(`uu ...`)，则 LAST(M) = LAST(`tt`) ∪ (LAST(`uu ...`) \\ { ε })。

      * 否则，序列 `uu ...` 必须非空；则 LAST(M) = LAST(`uu ...`)。

### FIRST 与 LAST 的例子

以下是 FIRST 与 LAST 的一些例子。（特别注意特殊元素 ε 如何根据输入各部分的交互被引入与消除。）

我们的第一个例子以树结构呈现，以阐述对 matcher 的分析如何组合。（一些较简单的子树已省略。）

```text
INPUT:  $(  $d:ident   $e:expr   );*    $( $( h )* );*    $( f ; )+   g
            ~~~~~~~~   ~~~~~~~                ~
                |         |                   |
FIRST:   { $d:ident }  { $e:expr }          { h }


INPUT:  $(  $d:ident   $e:expr   );*    $( $( h )* );*    $( f ; )+
            ~~~~~~~~~~~~~~~~~~             ~~~~~~~           ~~~
                        |                      |               |
FIRST:          { $d:ident }               { h, ε }         { f }

INPUT:  $(  $d:ident   $e:expr   );*    $( $( h )* );*    $( f ; )+   g
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~    ~~~~~~~~~~~~~~    ~~~~~~~~~   ~
                        |                       |              |       |
FIRST:        { $d:ident, ε }            {  h, ε, ;  }      { f }   { g }


INPUT:  $(  $d:ident   $e:expr   );*    $( $( h )* );*    $( f ; )+   g
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                        |
FIRST:                       { $d:ident, h, ;,  f }
```

因此：

 * FIRST(`$($d:ident $e:expr );* $( $(h)* );* $( f ;)+ g`) = { `$d:ident`, `h`, `;`, `f` }

但注意：

 * FIRST(`$($d:ident $e:expr );* $( $(h)* );* $($( f ;)+ g)*`) = { `$d:ident`, `h`, `;`, `f`, ε }

以下是类似的例子，但现在针对 LAST。

 * LAST(`$d:ident $e:expr`) = { `$e:expr` }
 * LAST(`$( $d:ident $e:expr );*`) = { `$e:expr`, ε }
 * LAST(`$( $d:ident $e:expr );* $(h)*`) = { `$e:expr`, ε, `h` }
 * LAST(`$( $d:ident $e:expr );* $(h)* $( f ;)+`) = { `;` }
 * LAST(`$( $d:ident $e:expr );* $(h)* $( f ;)+ g`) = { `g` }

r[macro.ambiguity.sets.def.follow]
### FOLLOW(M)

r[macro.ambiguity.sets.def.follow.intro]
最后，FOLLOW(M) 的定义如下构建。pat、expr 等表示具有给定 fragment specifier 的简单非终结符。

r[macro.ambiguity.sets.def.follow.pat]
  * FOLLOW(pat) = {`=>`, `,`, `=`, `|`, `if`, `in`}`.

r[macro.ambiguity.sets.def.follow.expr-stmt]
  * FOLLOW(expr) = FOLLOW(expr_2021) = FOLLOW(stmt) =  {`=>`, `,`, `;`}`.

r[macro.ambiguity.sets.def.follow.ty-path]
  * FOLLOW(ty) = FOLLOW(path) = {`{`, `[`, `,`, `=>`, `:`, `=`, `>`, `>>`, `;`, `|`, `as`, `where`, block 非终结符}.

r[macro.ambiguity.sets.def.follow.vis]
  * FOLLOW(vis) = {`,`；除非裸 `priv` 外的任何关键字或标识符；任何可以开始类型的 token；ident、ty 与 path 非终结符}。

r[macro.ambiguity.sets.def.follow.simple]
  * 对任何其他简单 token，FOLLOW(t) = ANYTOKEN，包括 block、ident、tt、item、lifetime、literal 与 meta 简单非终结符，以及所有终结符。

r[macro.ambiguity.sets.def.follow.other-matcher]
  * 对任何其他 M，FOLLOW(M) 定义为：当 t 遍历 (LAST(M) \\ {ε}) 时，FOLLOW(t) 的交集。

r[macro.ambiguity.sets.def.follow.type-first]
截至撰写时，可以开始类型的 token 为 {`(`, `[`, `!`, `*`, `&`, `&&`, `?`, lifetimes, `>`, `>>`, `::`, 任何非关键字标识符, `super`, `self`, `Self`, `extern`, `crate`, `$crate`, `_`, `for`, `impl`, `fn`, `unsafe`, `typeof`, `dyn`}，尽管此列表可能不完整，因为人们并不总会在添加新项时记得更新附录。

复杂 M 的 FOLLOW 例子：

 * FOLLOW(`$( $d:ident $e:expr )*`) = FOLLOW(`$e:expr`)
 * FOLLOW(`$( $d:ident $e:expr )* $(;)*`) = FOLLOW(`$e:expr`) ∩ ANYTOKEN = FOLLOW(`$e:expr`)
 * FOLLOW(`$( $d:ident $e:expr )* $(;)* $( f |)+`) = ANYTOKEN

### 有效与无效 matcher 的例子

有了上述规范，我们就可以给出为何某些 matcher 合法而另一些不合法的论证。

 * `($ty:ty < foo ,)` ：非法，因为 FIRST(`< foo ,`) = { `<` } ⊈ FOLLOW(`ty`)

 * `($ty:ty , foo <)` ：合法，因为 FIRST(`, foo <`) = { `,` }  ⊆ FOLLOW(`ty`)。

 * `($pa:pat $pb:pat $ty:ty ,)` ：非法，因为 FIRST(`$pb:pat $ty:ty ,`) = { `$pb:pat` } ⊈ FOLLOW(`pat`)，并且 FIRST(`$ty:ty ,`) = { `$ty:ty` } ⊈ FOLLOW(`pat`)。

 * `( $($a:tt $b:tt)* ; )` ：合法，因为 FIRST(`$b:tt`) = { `$b:tt` } ⊆ FOLLOW(`tt`) = ANYTOKEN，FIRST(`;`) = { `;` } 亦然。

 * `( $($t:tt),* , $(t:tt),* )` ：合法，（尽管任何实际使用此宏的尝试都会在展开期间发出局部歧义错误）。

 * `($ty:ty $(; not sep)* -)` ：非法，因为 FIRST(`$(; not sep)* -`) = { `;`, `-` } 不在 FOLLOW(`ty`) 中。

 * `($($ty:ty)-+)` ：非法，因为 separator `-` 不在 FOLLOW(`ty`) 中。

 * `($($e:expr)*)` ：非法，因为 expr NT 不在 FOLLOW(expr NT) 中。

[Macros by Example]: macros-by-example.md
[RFC 550]: https://github.com/rust-lang/rfcs/blob/master/text/0550-macro-future-proofing.md
[tracking issue]: https://github.com/rust-lang/rust/issues/56575
