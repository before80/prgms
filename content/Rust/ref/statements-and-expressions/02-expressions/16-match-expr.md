+++
title = "16-match 表达式"
date = 2026-08-18T08:45:00+08:00
weight = 59
type = "docs"
description = "match 表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/match-expr.html](https://doc.rust-lang.org/reference/expressions/match-expr.html)

r[expr.match]
# match 表达式

r[expr.match.syntax]
```grammar,expressions
MatchExpression ->
    `match` Scrutinee `{`
        InnerAttribute*
        MatchArms?
    `}`

Scrutinee -> Expression _except [StructExpression]_

MatchArms ->
    ( MatchArm `=>` ( ExpressionWithoutBlock `,` | ExpressionWithBlock `,`? ) )*
    MatchArm `=>` Expression `,`?

MatchArm -> OuterAttribute* Pattern MatchArmGuard?

MatchArmGuard -> `if` MatchConditions

MatchConditions ->
     MatchGuardChain
   | Expression

MatchGuardChain -> MatchGuardCondition ( `&&` MatchGuardCondition )*

MatchGuardCondition ->
     Expression _except [ExcludedMatchConditions]_
   | OuterAttribute* `let` Pattern `=` MatchGuardScrutinee

MatchGuardScrutinee -> Expression _except [ExcludedMatchConditions]_

@root ExcludedMatchConditions ->
      LazyBooleanExpression
    | RangeExpr
    | RangeFromExpr
    | RangeInclusiveExpr
    | AssignmentExpression
    | CompoundAssignmentExpression
```
<!-- TODO: The exception above isn't accurate, see https://github.com/rust-lang/reference/issues/569 -->

r[expr.match.intro]
*`match` 表达式*根据模式进行分支。具体发生何种匹配取决于[模式][pattern]。

r[expr.match.scrutinee]
`match` 表达式有一个*[被检视表达式][scrutinee]*，即要与各模式比较的值。

r[expr.match.scrutinee-constraint]
被检视表达式与各模式必须具有相同的类型。

r[expr.match.scrutinee-behavior]
`match` 的行为取决于被检视表达式是[位置表达式还是值表达式][place expression]。

r[expr.match.scrutinee-value]
若被检视表达式是[值表达式][value expression]，则首先将其求值到一个临时位置，然后将得到的值依次与各分支中的模式比较，直到找到匹配。第一个模式匹配成功的分支被选为 `match` 的跳转目标，模式所绑定的变量被赋给该分支块中的局部变量，然后控制进入该块。

r[expr.match.scrutinee-place]
当被检视表达式是[位置表达式][place expression]时，match 不会分配临时位置；不过，按值绑定仍可能从该内存位置复制或移出。在可能的情况下，更推荐对位置表达式进行匹配，因为这些匹配的生命周期继承自该位置表达式，而不是被限制在 match 内部。

`match` 表达式的示例：

```rust
let x = 1;

match x {
    1 => println!("one"),
    2 => println!("two"),
    3 => println!("three"),
    4 => println!("four"),
    5 => println!("five"),
    _ => println!("something else"),
}
```

r[expr.match.pattern-vars]
模式中绑定的变量作用域为 match 守卫以及该分支的表达式。

r[expr.match.pattern-var-binding]
[绑定模式][binding mode]（移动、复制或引用）取决于该模式。

r[expr.match.or-pattern]
多个匹配模式可以用 `|` 运算符连接。各模式会按从左到右的顺序测试，直到找到成功的匹配。

```rust
let x = 9;
let message = match x {
    0 | 1  => "not many",
    2 ..= 9 => "a few",
    _      => "lots"
};

assert_eq!(message, "a few");

// 演示模式匹配顺序。
struct S(i32, i32);

match S(1, 2) {
    S(z @ 1, _) | S(_, z @ 2) => assert_eq!(z, 1),
    _ => panic!(),
}
```

> **注意**
> `2..=9` 是[区间模式][Range Pattern]，不是[区间表达式][Range Expression]。因此，match 分支中只能使用区间模式所支持的那些区间类型。

r[expr.match.or-patterns-restriction]
由 `|` 分隔的每个模式中的每个绑定，都必须出现在该分支的所有模式中。

r[expr.match.binding-restriction]
同名的每个绑定必须具有相同的类型，并且具有相同的绑定模式。

r[expr.match.type]
整个 `match` 表达式的类型是各个 match 分支的[最小上界][least upper bound]。

r[expr.match.empty]
若没有任何 match 分支，则该 `match` 表达式是[发散][diverging]的，类型为 [`!`]。

> [!EXAMPLE]
> ```rust
> # fn make<T>() -> T { loop {} }
> enum Empty {}
>
> fn diverging_match_no_arms() -> ! {
>     let e: Empty = make();
>     match e {}
> }
> ```


r[expr.match.diverging]
若被检视表达式发散，或所有 match 分支都发散，则整个 `match` 表达式也发散。

r[expr.match.guard]
## match 守卫

r[expr.match.guard.intro]
match 分支可以接受 _match 守卫_，以进一步细化匹配某一情况的条件。

r[expr.match.guard.condition]
模式守卫出现在模式之后、跟在 `if` 关键字后面，由具有[布尔类型][type.bool]的[表达式][Expression]或条件式 `let` 匹配组成。

r[expr.match.guard.behavior]
当模式匹配成功时，会执行模式守卫。若所有守卫条件操作数都求值为 `true`，且所有 `let` 模式都成功匹配其[被检视表达式][scrutinee]，则该 match 分支匹配成功，并执行分支体。

r[expr.match.guard.next]
否则，会测试下一个模式，包括同一分支中用 `|` 运算符连接的其它匹配。

```rust
## let maybe_digit = Some(0);
## fn process_digit(i: i32) { }
## fn process_other(i: i32) { }
let message = match maybe_digit {
    Some(x) if x < 10 => process_digit(x),
    Some(x) => process_other(x),
    None => panic!(),
};
```

> **注意**
> 使用 `|` 运算符的多个匹配可能导致模式守卫及其副作用执行多次。例如：
>
> ```rust
> # use std::cell::Cell;
> let i : Cell<i32> = Cell::new(0);
> match 1 {
>     1 | _ if { i.set(i.get() + 1); false } => {}
>     _ => {}
> }
> assert_eq!(i.get(), 2);
> ```

r[expr.match.guard.bound-variables]
模式守卫可以引用紧随其后的模式中所绑定的变量。

r[expr.match.guard.shared-ref]
在求值守卫之前，会对变量所匹配的那部分被检视表达式取共享引用。求值守卫时，访问该变量就使用这个共享引用。

r[expr.match.guard.value]
只有当守卫求值成功时，才会从被检视表达式把值移动或复制到该变量中。这允许在守卫中使用共享借用，而不会在守卫匹配失败时从被检视表达式中移出。

r[expr.match.guard.no-mutation]
此外，通过在求值守卫时持有共享引用，也阻止了在守卫内部进行修改。

r[expr.match.guard.let]
守卫可以使用 `let` 模式来有条件地匹配被检视表达式，并在模式匹配成功时把新变量绑定到作用域中。

> [!EXAMPLE]
> 本例中会求值守卫条件 `let Some(first_char) = name.chars().next()`。若该 `let` 模式匹配成功（即字符串至少有一个字符），则执行该分支的函数体。否则，模式匹配继续到下一个分支。
>
> 该 `let` 模式会创建新绑定（`first_char`），它可以与原始模式绑定（`name`）一起在该分支的函数体中使用。
> ```rust
> # enum Command {
> #     Run(String),
> #     Stop,
> # }
> let cmd = Command::Run("example".to_string());
>
> match cmd {
>     Command::Run(name) if let Some(first_char) = name.chars().next() => {
>         // 此处 `name` 和 `first_char` 都可用
>         println!("Running: {name} (starts with '{first_char}')");
>     }
>     Command::Run(name) => {
>         println!("{name} is empty");
>     }
>     _ => {}
> }
> ```

r[expr.match.guard.chains]
## match 守卫链

r[expr.match.guard.chains.intro]
多个守卫条件操作数可以用 `&&` 分隔。

> [!EXAMPLE]
> ```rust
> # let foo = Some([123]);
> # let already_checked = false;
> match foo {
>     Some(xs) if let [single] = xs && !already_checked => { dbg!(single); }
>     _ => {}
> }
> ```

r[expr.match.guard.chains.order]
与 `&&` [LazyBooleanExpression] 类似，各操作数从左到右求值，直到某个操作数求值为 `false` 或某个 `let` 匹配失败，此后的操作数不再求值。

r[expr.match.guard.chains.bindings]
每个 `let` 模式的绑定都会进入作用域，供下一个条件操作数和 match 分支体使用。

r[expr.match.guard.chains.or]
若任一守卫条件操作数是 `let` 模式，则任何条件操作数都不能是 `||` [惰性布尔运算符表达式][expr.bool-logic]，以免与 `let` 被检视表达式产生歧义和优先级问题。

> [!EXAMPLE]
> 若需要 `||` 表达式，可以使用圆括号。例如：
>
> ```rust
> # let foo = Some([123]);
> match foo {
>     Some(xs) if let [x] = xs
>         // 此处需要圆括号。
>         && (x < -100 || x > 20) => {}
>     _ => {}
> }
> ```

r[expr.match.attributes]
## match 分支上的属性

r[expr.match.attributes.outer]
match 分支上允许外部属性。在 match 分支上有意义的属性只有 [`cfg`] 和 [lint 检查属性][lint check attributes]。

r[expr.match.attributes.inner]
[内部属性][Inner attributes]允许直接出现在 match 表达式的开括号之后，其表达式上下文与[块表达式上的属性][attributes on block expressions]相同。

[`!`]: type.never
[`cfg`]: ../conditional-compilation.md
[attributes on block expressions]: block-expr.md#attributes-on-block-expressions
[binding mode]: ../patterns.md#binding-modes
[diverging]: divergence
[Inner attributes]: ../attributes.md
[least upper bound]: coerce.least-upper-bound
[lint check attributes]: ../attributes/diagnostics.md#lint-check-attributes
[pattern]: ../patterns.md
[place expression]: ../expressions.md#place-expressions-and-value-expressions
[Range Expression]: range-expr.md
[Range Pattern]: ../patterns.md#range-patterns
[scrutinee]: ../glossary.md#scrutinee
[value expression]: ../expressions.md#place-expressions-and-value-expressions
