+++
title = "第2章 语句"
date = 2026-08-18T22:00:00+08:00
weight = 30
type = "docs"
description = "语句 — The Rust Style Guide"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)

> 原文链接: [https://doc.rust-lang.org/nightly/style-guide/statements.html](https://doc.rust-lang.org/nightly/style-guide/statements.html)

# 语句

## let 语句 {#let-statements}

在 `:` 之后以及 `=` 的两侧（若存在）各放一个空格。
不要在分号之前放空格。

```rust
// 一条注释。
let pattern: Type = expr;

let pattern;
let pattern: Type;
let pattern = expr;
```

尽可能将声明格式化为单行。若无法做到，则尝试在 `=` 之后换行，若声明能放在两行内。对表达式使用块缩进。

```rust
let pattern: Type =
    expr;
```

若第一行仍无法放在单行内，则在 `:` 之后换行，并使用块缩进。若类型需要多行——即使在 `:` 之后换行之后仍如此——则将第一行放在与 `:` 同一行，并遵循[合并规则](../expressions/#combinable-expressions)。

```rust
let pattern:
    Type =
    expr;
```

例如：

```rust
let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> =
    Foo { f, g };

let (abcd,
    defg):
    Baz =
{ ... }
```

若表达式跨越多行：若表达式的第一行能放进剩余空间，则它与 `=` 保持在同一行，且表达式的其余部分不再进一步缩进。若第一行放不下，则将表达式放在后续行上，并使用块缩进。若表达式是一个块，且类型或模式跨越多行，则将开括号放在新行且不缩进（这样可将块内部与类型分开）；否则，开括号跟在 `=` 之后。

示例：

```rust
let foo = Foo {
    f: abcd,
    g: qwer,
};

let foo =
    ALongName {
        f: abcd,
        g: qwer,
    };

let foo: Type = {
    an_expression();
    ...
};

let foo:
    ALongType =
{
    an_expression();
    ...
};

let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> = Foo {
    f: blimblimblim,
    g: blamblamblam,
};

let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> = foo(
    blimblimblim,
    blamblamblam,
);
```

### else 块（let-else 语句） {#else-blocks-let-else-statements}

let 语句可以包含 `else` 部分，从而成为 let-else 语句。
在这种情况下，对 `else` 块之前的各部分（即 `let pattern: Type = initializer_expr` 部分）始终应用与[其他 let 语句](#let-statements)相同的格式化规则。

若以下条件全部满足，则将整个 let-else 语句格式化为单行：

* 整个语句是*短*的
* `else` 块仅包含一个单行表达式，且没有语句
* `else` 块不包含注释
* `else` 块之前的 let 语句各部分可格式化为单行

```rust
let Some(1) = opt else { return };
```

否则，let-else 语句需要一些换行。

若将 let-else 语句拆成多行，切勿在 `else` 与 `{` 之间换行，并始终在 `}` 之前换行。

若 `else` 之前的 let 语句各部分可格式化为单行，但整个 let-else 不符合全部放在单行的条件，则将 `else {` 放在与初始化表达式同一行，两者之间留一个空格，然后在 `{` 之后换行。将闭合的 `}` 缩进到与 `let` 对齐，并将所含块再缩进一级。

```rust
let Some(1) = opt else {
    return;
};

let Some(1) = opt else {
    // 不行
    return
};
```

若 `else` 之前的 let 语句各部分可格式化为单行，但 `else {` 无法放在同一行，则在 `else` 之前换行。

```rust
    let Some(x) = some_really_really_really_really_really_really_really_really_really_long_name
    else {
        return;
    };
```

若初始化表达式是多行的，则将 `else` 关键字与块的开括号（即 `else {`）放在初始化表达式结束的同一行，两者之间留一个空格，当且仅当以下条件全部满足时：

* 初始化表达式以一个或多个闭合的圆括号、方括号和/或花括号结尾
* 该行上没有其他内容
* 该行与最初的 `let` 关键字具有相同的缩进级别

例如：

```rust
let Some(x) = y.foo(
    "abc",
    fairly_long_identifier,
    "def",
    "123456",
    "string",
    "cheese",
) else {
    bar()
}
```

否则，将 `else` 关键字与开括号放在初始化表达式结束之后的下一行，且 `else` 关键字与 `let` 关键字具有相同的缩进级别。

例如：

```rust
fn main() {
    let Some(x) = abcdef()
        .foo(
            "abc",
            some_really_really_really_long_ident,
            "ident",
            "123456",
        )
        .bar()
        .baz()
        .qux("fffffffffffffffff")
    else {
        return
    };

    let Some(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) =
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    else {
        return;
    };

    let LongStructName(AnotherStruct {
        multi,
        line,
        pattern,
    }) = slice.as_ref()
    else {
        return;
    };

    let LongStructName(AnotherStruct {
        multi,
        line,
        pattern,
    }) = multi_line_function_call(
        arg1,
        arg2,
        arg3,
        arg4,
    ) else {
        return;
    };
}
```

## 语句位置的宏 {#macros-in-statement-position}

对于语句位置的宏调用，使用圆括号或方括号作为定界符，并以分号结尾。不要在名称、`!`、定界符或 `;` 周围放空格。

```rust
// 一条注释。
a_macro!(...);
```

## 语句位置的表达式 {#expressions-in-statement-position}

不要在表达式与分号之间放空格。

```
<expr>;
```

终止语句位置的所有表达式时使用分号，除非它们以块结尾，或被用作块的值。

例如：

```rust
{
    an_expression();
    expr_as_value()
}

return foo();

loop {
    break;
}
```

当表达式具有 void 类型时使用分号，即使它本可以被传播。例如：

```rust
fn foo() { ... }

fn bar() {
    foo();
}
```
