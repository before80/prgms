+++
title = "第3章 表达式"
date = 2026-08-18T22:00:00+08:00
weight = 40
type = "docs"
description = "表达式 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/expressions.html](https://doc.rust-lang.org/nightly/style-guide/expressions.html)

# 表达式

## 块 {#blocks}

除非根据其他风格规则可以写成单行，块表达式必须在起始 `{` 之后以及结束 `}` 之前各有一个换行。

块之前的关键字（如 `unsafe` 或 `async`）必须与开括号在同一行，关键字与开括号之间留一个空格。缩进块的内容。

```rust
fn block_as_stmt() {
    a_call();

    {
        a_call_inside_a_block();

        // 块中的注释
        the_value
    }
}

fn block_as_expr() {
    let foo = {
        a_call_inside_a_block();

        // 块中的注释
        the_value
    };
}

fn unsafe_block_as_stmt() {
    a_call();

    unsafe {
        a_call_inside_a_block();

        // 块中的注释
        the_value
    }
}
```

若块带有属性，将其单独放在块之前的一行：

```rust
fn block_as_stmt() {
    #[an_attribute]
    {
        #![an_inner_attribute]

        // 块中的注释
        the_value
    }
}
```

避免在任一括号所在行写注释。

空块写成 `{}`。

在以下情况下将块写成单行：

- 它用于表达式位置（而非语句位置），或者是语句位置上的 unsafe 块，
- 它包含一个单行表达式且没有语句，并且
- 它不包含注释

对于单行块，在开括号之后和闭括号之前各放一个空格。

示例：

```rust
fn main() {
    // 单行
    let _ = { a_call() };
    let _ = unsafe { a_call() };

    // 不允许写成单行
    // 语句位置。
    {
        a_call()
    }

    // 包含语句
    let _ = {
        a_call();
    };
    unsafe {
        a_call();
    }

    // 包含注释
    let _ = {
        // 一条注释
    };
    let _ = {
        // 一条注释
        a_call()
    };

    // 多行
    let _ = {
        a_call();
        another_call()
    };
    let _ = {
        a_call(
            an_argument,
            another_arg,
        )
    };
}
```

## 闭包 {#closures}

不要在第一个 `|` 之前放额外空格（除非闭包带有 `move` 等关键字前缀）；在第二个 `|` 与闭包表达式之间放一个空格。两个 `|` 之间使用函数定义语法，但尽可能省略类型。

尽可能不使用包围的 `{}`。在有返回类型、有语句、闭包内部有注释，或主体表达式是跨越多行的控制流表达式时，再添加 `{}`。若使用花括号，遵循上文关于块的规则。示例：

```rust
|arg1, arg2| expr

move |arg1: i32, arg2: i32| -> i32 {
    expr1;
    expr2
}

|| Foo {
    field1,
    field2: 0,
}

|| {
    if true {
        blah
    } else {
        boo
    }
}

|x| unsafe {
    expr
}
```

## 结构体字面量 {#struct-literals}

若结构体字面量是*短*的，将其格式化为单行，且不要使用尾随逗号。否则，将其拆成多行，每个字段各占一行并使用块缩进，并使用尾随逗号。

对于每个 `field: value` 条目，仅在冒号之后放一个空格。

在开括号之前放一个空格。单行形式中，在开括号之后和闭括号之前各放一个空格。

```rust
Foo { field1, field2: 0 }
let f = Foo {
    field1,
    field2: an_expr,
};
```

函数式记录更新语法按字段对待，但绝不能带尾随逗号。不要在 `..` 之后放空格。

```rust
let f = Foo {
    field1,
    ..an_expr
};
```

## 单元字面量 {#unit-literals}

切勿在 `()` 单元字面量的开括号与闭括号之间换行。即使闭括号会超出最大行宽，也适用此规则。

## 元组字面量 {#tuple-literals}

尽可能使用单行形式。不要在开括号与第一个元素之间，或最后一个元素与闭括号之间放空格。元素之间用逗号后跟一个空格分隔。

无法使用单行形式时，将元组写成多行，元组的每个元素各占一行并使用块缩进，并使用尾随逗号。

```rust
(a, b, c)

let x = (
    a_long_expr,
    another_very_long_expr,
);
```

## 元组结构体字面量 {#tuple-struct-literals}

不要在标识符与开括号之间放空格。除此之外，遵循元组字面量的规则：

```rust
Foo(a, b, c)

let x = Foo(
    a_long_expr,
    another_very_long_expr,
);
```

## 枚举字面量 {#enum-literals}

遵循各类结构体字面量的格式化规则。优先使用枚举名作为限定名，除非该枚举位于 prelude 中：

```rust
Foo::Bar(a, b)
Foo::Baz {
    field1,
    field2: 1001,
}
Ok(an_expr)
```

## 数组字面量 {#array-literals}

将短的数组字面量写成单行。不要在开方括号与第一个元素之间，或最后一个元素与闭方括号之间放空格。元素之间用逗号后跟一个空格分隔。

若使用重复初始化器，仅在分号之后放一个空格。

使用 `vec!` 或类似的数组类宏时应用相同规则；对此类宏始终使用方括号。示例：

```rust
fn main() {
    let x = [1, 2, 3];
    let y = vec![a, b, c, d];
    let a = [42; 10];
}
```

对于必须拆成多行的数组，若使用重复初始化器，在 `;` 之后而非之前换行。否则，遵循下文函数调用的规则。无论哪种情况，对初始化器的内容使用块缩进，并在开方括号之后和闭方括号之前换行：

```rust
fn main() {
    [
        a_long_expression();
        1234567890
    ]
    let x = [
        an_expression,
        another_expression,
        a_third_expression,
    ];
}
```

## 数组访问、索引与切片 {#array-accesses-indexing-and-slicing}

不要在方括号周围放空格。尽可能避免换行。切勿在目标表达式与开方括号之间换行。若索引表达式必须换到后续行，或本身跨越多行，则对索引表达式使用块缩进，并在开方括号之后和闭方括号之前换行：

示例：

```rust
fn main() {
    foo[42];
    &foo[..10];
    bar[0..100];
    foo[4 + 5 / bar];
    a_long_target[
        a_long_indexing_expression
    ];
}
```

## 一元运算 {#unary-operations}

不要在一元运算符与其操作数之间放空格（即 `!x`，而不是 `! x`）。但 `&mut` 之后必须有一个空格。避免在一元运算符与其操作数之间换行。

## 二元运算 {#binary-operations}

二元运算符两侧要放空格（即 `x + 1`，而不是 `x+1`）（包括 `=` 以及 `+=`、`*=` 等其他赋值运算符）。

对于比较运算符，因为对于 `T op U`，`&T op &U` 同样已实现：若有 `t: &T` 和 `u: U`，优先使用 `*t op u` 而非 `t op &u`。一般而言，在表达式中优先解引用而非取引用，除非有必要（例如为了避免不必要的昂贵操作）。

宽松地使用圆括号；不必因为优先级而省略它们。工具不应自动插入或删除圆括号。不要用空格来表示优先级。

若换行，对后续每一行使用块缩进。对于赋值运算符，在运算符之后换行；对于所有其他运算符，将运算符放在后续行。每个子表达式各占一行：

```rust
foo_bar
    + bar
    + baz
    + qux
    + whatever
```

优先在赋值运算符（`=` 或 `+=` 等）处换行，而不是在其他二元运算符处换行。

### 转换（`as`） {#casts-as}

将 `as` 转换格式化为二元运算符。具体而言，始终在 `as` 两侧放空格；若换行，在 `as` 之前（切勿在之后）换行，并对后续行使用块缩进。右侧类型使用类型的格式化规则。

但与其他二元运算符不同，若链式使用一系列需要换行的 `as` 转换，且在第一个 `as` 之前换行就足以让剩余部分放入下一行，则不要在后续任何 `as` 之前换行；而是将这一系列类型都留在同一行：

```rust
let cstr = very_long_expression()
    as *const str as *const [u8] as *const std::os::raw::c_char;
```

若后续行仍需要换行，则与其他二元运算符一样，在每个 `as` 之前换行并使用块缩进。

## 控制流 {#control-flow}

不要为 `if` 和 `while` 表达式加上多余的圆括号。

```rust
if true {
}
```

优于

```rust
if (true) {
}
```

若多余的圆括号能让算术或逻辑表达式更易理解，则应当加上（`(x * 15) + (y * 20)` 是可以的）

## 函数调用 {#function-calls}

不要在函数名与开括号之间放空格。

不要在实参与其后的逗号之间放空格。

要在实参与其前的逗号之间放空格。

尽量不要在被调用表达式中换行。

对于无实参的函数调用（如 `func()` 这样的零元函数调用），切勿在括号内换行，也切勿在括号之间放空格。始终将零元函数调用写成单行调用，切勿写成多行调用。即使闭括号会超出最大行宽，也适用此规则。

### 单行调用 {#single-line-calls}

不要在函数名与开括号之间、开括号与第一个实参之间，或最后一个实参与闭括号之间放空格。

不要在最后一个实参之后放逗号。

```rust
foo(x, y, z)
```

### 多行调用 {#multi-line-calls}

若函数调用不是*短*的、否则会超出最大行宽，或任一实参或被调用者是多行的，则将调用格式化为多行。此时，每个实参各占一行并使用块缩进，在开括号之后和闭括号之前换行，并使用尾随逗号：

```rust
a_function_call(
    arg1,
    a_nested_call(a, b),
)
```

## 方法调用 {#method-calls}

调用时遵循函数调用的规则。

不要在 `.` 周围放任何空格。

```rust
x.foo().bar().baz(x, y, z);
```

## 宏的使用 {#macro-uses}

若宏可以像其他结构一样解析，则按那些结构来格式化。例如，宏使用 `foo!(a, b, c)` 可以像函数调用一样解析（忽略 `!`），因此使用函数调用的规则来格式化。

本风格指南为语言或标准库中的特定宏定义了具体格式。本风格指南不为任何第三方宏定义格式，即使它们与语言或标准库中的宏类似。

### 格式化字符串宏 {#format-string-macros}

对于接受格式化字符串的宏，若所有其他实参都是*短*的，则在放得下时将格式化字符串之前的实参格式化为单行，并在放得下时将格式化字符串之后的实参格式化为单行，格式化字符串单独占一行。若实参不是短的或放不下，则与函数一样将每个实参各占一行。例如：

```rust
println!(
    "Hello {} and {}",
    name1, name2,
);

assert_eq!(
    x, y,
    "x and y were not equal, see {}",
    reason,
);
```

## 字段与方法调用链 {#chains-of-fields-and-method-calls}

链是字段访问、方法调用和/或 try 运算符 `?` 的序列。例如，`a.b.c().d` 或 `foo?.bar().baz?`。

若链是「短」的且在其他方面可以这样做，则将链格式化为单行。若格式化为多行，则将链中的每个字段访问或方法调用各占一行，在 `.` 之前以及任何 `?` 之后换行。对后续每一行使用块缩进：

```rust
let foo = bar
    .baz?
    .qux();
```

若第一个元素最后一行的长度加上其缩进小于或等于第二行的缩进，则在放得下时将第一行与第二行合并。递归应用此规则。

```rust
x.baz?
    .qux()

x.y.z
    .qux()

let foo = x
    .baz?
    .qux();

foo(
    expr1,
    expr2,
).baz?
    .qux();
```

### 多行元素 {#multi-line-elements}

若链中任一元素被格式化为多行，则将该元素及其后的所有元素各占一行。

```rust
a.b.c()?
    .foo(
        an_expr,
        another_expr,
    )
    .bar
    .baz
```

注意，上例中因链以及函数调用而存在块缩进。

优先将整条链格式化为多行风格、每个元素各占一行，而不是让一些元素多行、另一些元素单行，例如：

```rust
// 更好
self.pre_comment
    .as_ref()
    .map_or(false, |comment| comment.starts_with("//"))

// 更差
self.pre_comment.as_ref().map_or(
    false,
    |comment| comment.starts_with("//"),
)
```

## 控制流表达式 {#control-flow-expressions}

本节涵盖 `for` 和 `loop` 表达式，以及带有其子表达式变体的 `if` 和 `while` 表达式。这包括带有单个 `let` 子表达式的形式（即 `if let` 和 `while let`），以及「let 链」：带有一个或多个 `let` 子表达式以及一个或多个布尔类型条件的形式（即 `if a && let Some(b) = c`）。

若放得下，将关键字、任何初始子句以及块的开括号都放在同一行。对块应用[块格式化](#blocks)的常规规则。

若存在 `else` 部分，则将闭括号、`else`、任何后续子句以及开括号都放在同一行，`else` 关键字前后各留一个空格：

```rust
if ... {
    ...
} else {
    ...
}

if let ... {
    ...
} else if ... {
    ...
} else {
    ...
}
```

若控制行需要换行，则对于放不下的 `if` 或 `while` 表达式中的任何 `let` 子表达式，优先在 `=` 之后换行；对于 `for` 表达式，在 `in` 之前换行；后续行应使用块缩进。若控制行因任何原因被换行，则开括号应单独占一行且不缩进。示例：

```rust
while let Some(foo)
    = a_long_expression
{
    ...
}

for foo
    in a_long_expression
{
    ...
}

if a_long_expression
    && another_long_expression
    || a_third_long_expression
{
    ...
}

if let Some(a) = b
    && another_long_expression
    && a_third_long_expression
{
    // ...
}

if let Some(relatively_long_thing)
    = a_long_expression
    && another_long_expression
    && a_third_long_expression
{
    // ...
}

if some_expr
    && another_long_expression
    && let Some(relatively_long_thing) =
        a_long_long_long_long_long_long_really_reallllllllllyyyyyyy_long_expression
    && a_third_long_expression
{
    // ...
}
```

若 let 链的控制行仅由两个子句组成，且左侧第一个操作数是字面量或 `ident`（其前可以有任意数量的一元前缀运算符），右侧第二个操作数是单行 `let` 子句，则允许将该控制行格式化为单行。否则，必须按上述规则将控制行换行并格式化。例如：

```rust
if a && let Some(b) = foo() {
    // ...
}

if true && let Some(b) = foo() {
    // ...
}

let operator = if !from_hir_call && let Some(p) = parent {
    // ...
};

if let Some(b) = foo()
    && a
{
    // ..
}

if foo()
    && let Some(b) = bar
{
    // ...
}

if gen_pos != GenericArgPosition::Type
    && let Some(b) = gen_args.bindings.first()
{
    // ..
}
```

当初始子句跨越多行并以一个或多个闭圆括号、方括号或花括号结尾，且该行上没有其他内容，且该行的缩进不超过控制流表达式第一行的缩进时，将块的开括号放在同一行，前面留一个空格。例如：

```rust
if !self.config.file_lines().intersects(
    &self.codemap.lookup_line_range(
        stmt.span,
    ),
) {  // 开括号与初始子句在同一行。
    ...
}
```

### 单行 `if else` {#single-line-if-else}

若 `if else` 或 `if let else` 出现在表达式上下文中（即不是独立语句）、只包含一个 `else` 子句，并且是*短*的，则将其写成单行：

```rust
let y = if x { 0 } else { 1 };

// 必须写成多行的示例。
let y = if something_very_long {
    not_small
} else {
    also_not_small
};

if x {
    0
} else {
    1
}
```

## match {#match}

尽量不要在判别式表达式内部换行。始终在开括号之后和闭括号之前换行。对 match 分支使用一级块缩进：

```rust
match foo {
    // 分支
}

let x = match foo.bar.baz() {
    // 分支
};
```

当且仅当不使用块时，为 match 分支使用尾随逗号。

切勿以 `|` 开始 match 分支的模式：

```rust
match foo {
    // 不要这样做。
    | foo => bar,
    // 也不要这样。
    | a_very_long_pattern
    | another_pattern
    | yet_another_pattern
    | a_fourth_pattern => {
        ...
    }
}
```

优先采用：

```rust
match foo {
    foo => bar,
    a_very_long_pattern
    | another_pattern
    | yet_another_pattern
    | a_fourth_pattern => {
        ...
    }
}
```

尽可能避免拆分 match 分支的左侧（`=>` 之前）。若 match 分支的右侧保持在同一行，切勿使用块（除非块为空）。

若右侧由多条语句组成，或有行注释，或该行起始部分无法与左侧放在同一行，则使用块。不要将只包含单个宏调用的右侧块展平，因为其展开形式可能包含尾随分号。

对块形式分支的主体使用块缩进。

示例：

```rust
match foo {
    foo => bar,
    a_very_long_pattern | another_pattern if an_expression() => {
        no_room_for_this_expression()
    }
    foo => {
        // 一条注释。
        an_expression()
    }
    foo => {
        let a = statement();
        an_expression()
    }
    bar => {}
    // 最后一项上的尾随逗号。
    foo => bar,
    baz => qux!(),
    lorem => {
        ipsum!()
    }
}
```

若主体是单个表达式、没有行注释且不是控制流表达式，则将其与左侧放在同一行。否则，它必须放在块中。示例：

```rust
match foo {
    // 可合并的表达式。
    foo => a_function_call(another_call(
        argument1,
        argument2,
    )),
    // 不可合并的表达式
    bar => {
        a_function_call(
            another_call(
                argument1,
                argument2,
            ),
            another_argument,
        )
    }
}
```

### 换行 {#line-breaking}

若在 match 分支右侧使用块形式可以避免在左侧换行，则这样做：

```rust
    // 假设下一行无法放入最大行宽
    a_very_long_pattern | another_pattern => ALongStructName {
        ...
    },
    // 优先采用这种写法
    a_very_long_pattern | another_pattern => {
        ALongStructName {
            ...
        }
    }
    // 而不是拆分模式。
```

切勿在不使用块形式主体的情况下在 `=>` 之后换行。

若左侧必须拆分且存在 `if` 子句，则在 `if` 之前换行并使用块缩进。此时，始终使用块主体，并在新行开始主体：

```rust
    a_very_long_pattern | another_pattern
        if expr =>
    {
        ...
    }
```

若必须拆分模式，则将模式的每个子句各占一行、不再额外缩进，并在 `|` 之前换行。若存在 `if` 子句，使用上述形式：

```rust
    a_very_long_pattern
    | another_pattern
    | yet_another_pattern
    | a_forth_pattern => {
        ...
    }
    a_very_long_pattern
    | another_pattern
    | yet_another_pattern
    | a_forth_pattern
        if expr =>
    {
        ...
    }
```

若模式是多行的，且最后一行的宽度小于缩进，则不要将 `if` 子句放在新行。例如：

```rust
    Token::Dimension {
         value,
         ref unit,
         ..
    } if num_context.is_ok(context.parsing_mode, value) => {
        ...
    }
```

若模式中每个子句都是*短*的，但整个模式无法放入一行，则将模式格式化为多行，每行尽可能多放子句。同样，在 `|` 之前换行：

```rust
    foo | bar | baz
    | qux => {
        ...
    }
```

若模式子句能放入单行，且匹配下列文法中的「small」，则我们将其定义为*短*的：

```
small:
    - small_no_tuple
    - 一元元组构造器：`(` small_no_tuple `,` `)`
    - `&` small

small_no_tuple:
    - 单个词法单元
    - `&` small_no_tuple
```

例如，`&&Some(foo)` 匹配，`Foo(4, Bar)` 不匹配。

## 可合并的表达式 {#combinable-expressions}

当函数调用只有一个实参，且该实参被格式化为多行时，若结果放得下，则将外层调用格式化为单行调用。将相同的合并行为应用于任何类似的表达式：它们具有由圆括号分隔的、多行且使用块缩进的子表达式列表（例如宏或元组结构体字面量）。例如：

```rust
foo(bar(
    an_expr,
    another_expr,
))

let x = foo(Bar {
    field: whatever,
});

foo(|param| {
    action();
    foo(param)
})

let x = combinable([
    an_expr,
    another_expr,
]);

let arr = [combinable(
    an_expr,
    another_expr,
)];
```

递归应用此行为。

对于有多个实参的函数，若最后一个实参是带显式块的多行闭包、没有其他闭包实参，且所有实参以及闭包的第一行都能放入第一行，则使用相同的合并行为：

```rust
foo(first_arg, x, |param| {
    action();
    foo(param)
})
```

## 范围 {#ranges}

不要在范围中放空格，例如 `0..10`、`x..=y`、`..x.len()`、`foo..`。

书写同时具有上界和下界的范围时，若必须在范围内换行，则在范围运算符之前换行，并对第二行使用块缩进：

```rust
a_long_expression
    ..another_long_expression
```

为表明优先级，若任一边界是复合表达式，则为其加上圆括号，例如 `..(x + 1)`、`(x.f)..(x.f.len())` 或 `0..(x - 10)`。

## 十六进制字面量 {#hexadecimal-literals}

十六进制字面量可以使用大写或小写字母，但不得在同一字面量中混用。项目应对所有字面量使用同一大小写，但我们不对使用小写还是大写作推荐。

## 模式 {#patterns}

按对应表达式的方式格式化模式。关于 match 分支中模式的额外格式化，参见 `match` 一节。
