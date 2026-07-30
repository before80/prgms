+++
title = "27-lifetimes"
date = 2026-07-28T14:49:00+08:00
weight = 270
type = "docs"
description = "面向 Go 用户重写生命周期：借用关系、`'static`、省略规则与常见报错"
isCJKLanguage = true
draft = false

+++

生命周期 (Lifetimes)

面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go；重点不是背语法，而是建立“生命周期描述借用关系，而不是延长寿命”的心智模型。

**本篇能解决什么：**
- 你是否总把生命周期理解成“让变量活得更久”的语法？
- 你是否在返回引用、结构体存引用、`'static`、`thread::spawn` 上频繁卡住？
- 你是否想知道什么时候该显式标注，什么时候交给省略规则？
- 你是否需要看得懂 `T: 'a`、`'a: 'b`、`for<'a>` 这些常见签名？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| lifetime | — | 生命周期 | 引用在多大范围内有效的关系描述 | Go 无直接对应物 |
| elision | — | 生命周期省略 | 编译器在简单场景自动补全标注 | 无 |
| `'static` | — | 静态生命周期 | 活到整个程序期，或不含短借用 | 全局静态数据的感觉 |
| outlives | — | 活得更久 | 一个生命周期至少和另一个一样长 | 无 |
| `HRTB` | Higher-Ranked Trait Bound | 高阶生命周期约束 | 表示“对任意生命周期都成立” | Go 无对应物 |
| borrow checker | — | 借用检查器 | 编译期检查借用是否合法 | Go 无对应物 |

**热度索引：**

| 热度 | 题目 |
|------|------|
| `common` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q16](#q16), [Q17](#q17), [Q18](#q18), [Q19](#q19), [Q20](#q20) |

## Q1. 生命周期标注 `'a` 到底在表达什么？ {#q1}
**Tags:** `common` `lifetime` `basics`
**适用版本:** Rust 1.0+

**一句话答案：** 它表达的是“这些引用之间谁至少和谁一样久”的关系，不会让任何值真的活久一点。

**详细解答：** 生命周期从来不是垃圾回收器，也不是延期释放器。它只是让编译器知道：返回的引用借自谁，或者两个输入引用之间有什么关系。

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let a = String::from("abcd");
    let b = String::from("xy");
    assert_eq!(longest(&a, &b), "abcd");
}
```

```rust
fn pick_first<'a>(x: &'a str, _y: &'a str) -> &'a str {
    x
}

fn main() {
    let text = String::from("hello");
    let result;
    {
        let other = String::from("xx");
        result = pick_first(&text, &other);
        assert_eq!(result, "hello");
    }
}
```

**🐹 Go 对比：** Go 指针不需要写这种关系，是因为 Go 选择把悬垂引用和内存回收问题交给运行时与 GC；Rust 则要求在编译期说明借用边界。

**记忆点：** 生命周期是在描述引用，不是在描述拥有者对象本身。

## Q2. 生命周期省略规则什么时候能帮我，什么时候帮不了？ {#q2}
**Tags:** `common` `elision`
**适用版本:** Rust 1.0+

**一句话答案：** 单输入引用、方法上的 `&self` 这类简单场景通常能省；多个输入引用又要返回引用时，往往必须手写。

**详细解答：** 最常用的三条省略规则是：每个输入引用各有一个生命周期；如果只有一个输入生命周期，它可传给输出；如果方法有 `&self`，输出通常默认绑到 `self` 上。

```rust
fn first_char(s: &str) -> &str {
    &s[..1]
}

fn main() {
    assert_eq!(first_char("rust"), "r");
}
```

```rust
struct Name(String);

impl Name {
    fn as_str(&self) -> &str {
        &self.0
    }
}

fn main() {
    let name = Name(String::from("Ada"));
    assert_eq!(name.as_str(), "Ada");
}
```

**🐹 Go 对比：** 这不是“语法糖 optional 不 optional”这么简单，而是 Rust 在减少样板的同时仍然要保证借用关系可推断。

**记忆点：** 多输入 + 返回引用，先怀疑“这里也许需要显式生命周期”。

## Q3. 为什么函数不能返回局部变量的引用？ {#q3}
**Tags:** `common` `dangling`
**适用版本:** Rust 1.0+

**一句话答案：** 因为局部变量在函数结束时就被销毁了，返回它的引用必然悬垂。

**详细解答：** 这是生命周期最核心的安全边界之一。真正该返回的，通常是所有权、输入参数的借用，或者 `'static` 数据。

```rust
fn make_string() -> String {
    String::from("owned")
}

fn main() {
    let s = make_string();
    assert_eq!(s, "owned");
}
```

```rust
fn first_byte_text(s: &str) -> &str {
    &s[..1]
}

fn main() {
    let text = String::from("hello");
    assert_eq!(first_byte_text(&text), "h");
}
```

**🐹 Go 对比：** Go 可以安全返回局部变量地址，是因为逃逸分析和 GC 会把它提升到堆上；Rust 不做这种隐式所有权转换。

**记忆点：** 需要把值带出函数时，默认优先想“返回所有权”。

## Q4. 结构体里为什么一存引用就要带生命周期参数？ {#q4}
**Tags:** `common` `struct` `reference`
**适用版本:** Rust 1.0+

**一句话答案：** 因为结构体本身要把“我借来的这段数据至少能活多久”写进类型里，否则编译器无法验证实例是否合法。

**详细解答：** 一旦结构体字段里有 `&T` 或 `&str`，生命周期就不再只是某个函数局部问题，而变成了这个类型定义的一部分。

```rust
struct Excerpt<'a> {
    part: &'a str,
}

fn main() {
    let text = String::from("Call me Ishmael");
    let excerpt = Excerpt { part: &text[..4] };
    assert_eq!(excerpt.part, "Call");
}
```

```rust
struct Excerpt<'a> {
    part: &'a str,
}

fn build<'a>(s: &'a str) -> Excerpt<'a> {
    Excerpt { part: s }
}

fn main() {
    let text = String::from("hello");
    let excerpt = build(&text);
    assert_eq!(excerpt.part, "hello");
}
```

**🐹 Go 对比：** Go 的 struct 字段若放指针，不需要把“借用谁、活多久”写进类型；Rust 这里选择显式化。

**记忆点：** “字段里存引用” 会把生命周期要求传染到整个类型签名。

## Q5. `'static` 到底是什么意思，为什么 `String` 也常能满足 `T: 'static`？ {#q5}
**Tags:** `common` `static`
**适用版本:** Rust 1.0+

**一句话答案：** `'static` 有两层常见含义：引用本身活到程序结束，或者某个拥有型值内部不含更短借用。

**详细解答：** 很多人误以为 `T: 'static` 就必须是字符串字面量，这是错的。`String`、`Vec<u8>` 这类拥有型值只要里面不借别人，也满足 `T: 'static`。

```rust
fn need_static_ref(s: &'static str) -> &'static str {
    s
}

fn main() {
    assert_eq!(need_static_ref("hello"), "hello");
}
```

```rust
fn needs_static_value<T: 'static>(value: T) -> T {
    value
}

fn main() {
    let s = needs_static_value(String::from("owned"));
    assert_eq!(s, "owned");
}
```

**🐹 Go 对比：** Go 没有 `'static` 这种类型约束；Rust 这里是在明确“这个值不能偷偷借用短命栈数据”。

**记忆点：** `T: 'static` 不等于“字面量”，而是“不携带短借用”。

## Q6. 结构体方法里返回 `&str`，什么时候要写成 `&'a str`，什么时候不用？ {#q6}
**Tags:** `common` `impl`
**适用版本:** Rust 1.0+

**一句话答案：** 如果返回值借自 `self` 当前借用，省略通常够用；如果你要把字段里更长寿命的借用原样穿透出来，就可能需要显式写结构体自己的 `'a`。

**详细解答：** 这是很多人第一次意识到“`self` 的借用寿命”和“字段原始来源寿命”不是一回事的地方。

```rust
struct Holder<'a> {
    text: &'a str,
}

impl<'a> Holder<'a> {
    fn view(&self) -> &str {
        &self.text[..1]
    }
}

fn main() {
    let source = String::from("rust");
    let holder = Holder { text: &source };
    assert_eq!(holder.view(), "r");
}
```

```rust
struct Holder<'a> {
    text: &'a str,
}

impl<'a> Holder<'a> {
    fn original(&self) -> &'a str {
        self.text
    }
}

fn main() {
    let source = String::from("rust");
    let original;
    {
        let holder = Holder { text: &source };
        original = holder.original();
    }
    assert_eq!(original, "rust");
}
```

**🐹 Go 对比：** Go 指针方法不会区分这两层借用关系；Rust 会严格区分“借自 `self` 这一瞬间”还是“借自 `self` 背后的外部源头”。

**记忆点：** 返回字段原始借用时，常常要显式写出结构体上的生命周期参数。

## Q7. `T: 'a` 和 `'a: 'b` 这种写法该怎么读？ {#q7}
**Tags:** `common` `outlives`
**适用版本:** Rust 1.0+

**一句话答案：** `T: 'a` 表示 `T` 内部所有借用至少活到 `'a`；`'a: 'b` 表示 `'a` 至少和 `'b` 一样长。

**详细解答：** 这两种语法都叫 outlives 关系，只是左边一个是类型，一个是生命周期本身。

```rust
fn store_ref<'a, T: 'a>(slot: &mut Option<&'a T>, value: &'a T) {
    *slot = Some(value);
}

fn main() {
    let value = 7;
    let mut slot = None;
    store_ref(&mut slot, &value);
    assert_eq!(slot, Some(&7));
}
```

```rust
fn choose<'a, 'b: 'a>(left: &'a str, _right: &'b str) -> &'a str {
    left
}

fn main() {
    let long = String::from("long");
    let short = String::from("x");
    assert_eq!(choose(&short, &long), "x");
}
```

**🐹 Go 对比：** Go 不会把“谁活得比谁久”写进签名；Rust 则允许你在非常细的层面表达这种关系。

**记忆点：** 冒号这里读作“至少满足……那么久”。

## Q8. `for<'a>` 这种高阶生命周期约束是在说什么？ {#q8}
**Tags:** `common` `HRTB`
**适用版本:** Rust 1.0+

**一句话答案：** 它表示“这个约束对任意生命周期 `'a` 都成立”，常用于可接受任意短借用的闭包或函数对象。

**详细解答：** 这类写法第一次看到会很抽象，但可以把它读成“不要只对某一个特定生命周期成立，而要真正泛化到所有生命周期”。

```rust
fn call_with_str<F>(f: F) -> usize
where
    F: for<'a> Fn(&'a str) -> usize,
{
    f("hello")
}

fn main() {
    let len = call_with_str(|s| s.len());
    assert_eq!(len, 5);
}
```

```rust
fn reuse_twice<F>(f: F) -> (usize, usize)
where
    F: for<'a> Fn(&'a str) -> usize,
{
    (f("a"), f("rust"))
}

fn main() {
    assert_eq!(reuse_twice(|s| s.len()), (1, 4));
}
```

**🐹 Go 对比：** Go 没有把生命周期本身参数化的语法，所以也没有对应形式。

**记忆点：** 看到 `for<'a>`，就把它翻译成“对任意 `'a`”。

## Q9. 匿名生命周期 `'_` 有什么实际用途？ {#q9}
**Tags:** `common` `anonymous-lifetime`
**适用版本:** Rust 1.31+

**一句话答案：** `'_` 表示“这里确实有个生命周期，但我不想给它起名字，交给编译器推断即可”。

**详细解答：** 它常见于实现块、返回类型或者某些显式占位场景，作用主要是减轻噪音，而不是改变语义。

```rust
struct Wrap<'a> {
    value: &'a str,
}

impl Wrap<'_> {
    fn len(&self) -> usize {
        self.value.len()
    }
}

fn main() {
    let text = String::from("abc");
    let wrap = Wrap { value: &text };
    assert_eq!(wrap.len(), 3);
}
```

```rust
fn first(s: &str) -> &'_ str {
    &s[..1]
}

fn main() {
    assert_eq!(first("rust"), "r");
}
```

**🐹 Go 对比：** 这更像“我知道这里有类型信息，但让编译器替我补名字”；Go 没有生命周期命名这层，自然也没有对应写法。

**记忆点：** `'_` 是显式存在、隐式命名，不是“没有生命周期”。

## Q10. 为什么 `thread::spawn` 常常要求我改成 owned 值或 `Arc`？ {#q10}
**Tags:** `common` `thread` `static`
**适用版本:** Rust 1.0+；`thread::scope` 自 Rust 1.63+

**一句话答案：** 因为新线程可能活得比当前函数更久，所以普通 `spawn` 不能安全地捕获短借用。

**详细解答：** 这不是线程 API 在刁难你，而是生命周期规则在防止线程拿到一块已经失效的栈内存。

```rust
use std::thread;

fn main() {
    let text = String::from("owned");
    let handle = thread::spawn(move || text.len());
    assert_eq!(handle.join().unwrap(), 5);
}
```

```rust
use std::thread;

fn main() {
    let numbers = vec![1, 2, 3];
    thread::scope(|scope| {
        scope.spawn(|| {
            assert_eq!(numbers.len(), 3);
        });
    });
}
```

**🐹 Go 对比：** Go goroutine 可以直接捕获外层变量，但数据竞争要靠程序员和工具兜底；Rust 则先问“这份借用到底能不能活到线程结束”。

**记忆点：** 跨线程共享时，优先区分“转移所有权”“作用域线程借用”“`Arc` 共享”。

## Q11. 为什么 Rust 不鼓励自引用结构体？ {#q11}
**Tags:** `common` `self-referential`
**适用版本:** Rust 1.0+

**一句话答案：** 因为结构体一旦移动，内部指向自身字段的引用就可能失效，而普通安全 Rust 很难表达“此后绝不再移动”。

**详细解答：** 大多数业务场景下，更简单可靠的替代方案是存索引、范围，或者把被引用数据放在结构体外部。

```rust
use std::ops::Range;

struct Excerpt {
    text: String,
    range: Range<usize>,
}

impl Excerpt {
    fn part(&self) -> &str {
        &self.text[self.range.clone()]
    }
}

fn main() {
    let excerpt = Excerpt {
        text: String::from("hello world"),
        range: 0..5,
    };
    assert_eq!(excerpt.part(), "hello");
}
```

```rust
struct View<'a> {
    part: &'a str,
}

fn make_view<'a>(text: &'a str) -> View<'a> {
    View { part: &text[..1] }
}

fn main() {
    let text = String::from("rust");
    let view = make_view(&text);
    assert_eq!(view.part, "r");
}
```

**🐹 Go 对比：** Go 里内部持有指向自己字段的指针不常被类型系统阻止；Rust 则更早把“移动后悬垂”的可能性拦住。

**记忆点：** 自引用需求先想“能否改成索引或外部持有”。

## Q12. 学生命周期时最容易走偏的地方是什么？ {#q12}
**Tags:** `common` `mental-model`
**适用版本:** Rust 1.0+

**一句话答案：** 最大误区是把生命周期当作一种“修报错的标注语法”，而不是用来表达借用设计的类型信息。

**详细解答：** 好的生命周期设计通常来自更清晰的数据流：谁拥有数据、谁只是暂借、借用要跨多远。很多“生命周期问题”本质上其实是“该不该拥有这份数据”的 API 设计问题。

```rust
fn better_api(text: String) -> String {
    text
}

fn main() {
    let text = String::from("owned");
    assert_eq!(better_api(text), "owned");
}
```

```rust
fn borrowed_api(text: &str) -> usize {
    text.len()
}

fn main() {
    let text = String::from("borrowed");
    assert_eq!(borrowed_api(&text), 8);
}
```

**🐹 Go 对比：** Rust 逼你更早想清楚所有权和借用边界；这会增加前期成本，但能换来更稳定的长期维护体验。

**记忆点：** 遇到生命周期报错时，不要第一反应就是乱加 `'a`；先重画数据流。

## Q13. 生命周期标注是不是在手动管 GC？ {#q13}
**Tags:** `common` `mental-model` `gc`
**适用版本:** Rust 1.0+

**一句话答案：** 不是。生命周期不分配、不回收、不延长对象寿命；它只描述“这些引用之间谁至少和谁一样久”，好让借用检查器在编译期拒绝悬垂引用。

**详细解答：** Go 靠 GC 在运行时追踪可达对象；Rust 默认靠所有权在作用域结束时 `drop`，再用生命周期证明借用没有活过拥有者。你在签名里写的 `'a` 不会让局部变量多活一纳秒——它只是给编译器看的关系标签。真正管内存的是拥有者（`String`、`Vec`、`Box` 等）和它们的析构时机。

```rust
fn first_word(s: &str) -> &str {
    match s.find(' ') {
        Some(idx) => &s[..idx],
        None => s,
    }
}

fn main() {
    let text = String::from("hello world");
    let word = first_word(&text);
    assert_eq!(word, "hello");
}
```

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() { x } else { y }
}

fn main() {
    let a = String::from("long");
    let b = String::from("tiny");
    assert_eq!(longest(&a, &b), "long");
}
```

这里没有任何“手动 free / 手动延长 GC 根”。标注只是在说：返回的 `&str` 不会比输入里较短的那份借用活得更久。

**🐹 Go 对比：** Go 程序员很少写“引用活多久”，因为 GC 会托底；Rust 把这层关系前置到类型里，换来无 GC 停顿和更早的悬垂引用诊断。

**记忆点：** `'a` 是借用关系说明书，不是迷你 GC。

## Q14. 函数要返回两个引用时生命周期怎么标？ {#q14}
**Tags:** `common` `return` `elision`
**适用版本:** Rust 1.0+

**一句话答案：** 两个返回引用若来自同一输入，共用一个生命周期参数；若分别来自不同输入，就给它们各自的生命周期，或打包进带生命周期的结构体/元组。

**详细解答：** 省略规则帮不了“多输入 + 返回引用”的多数情况，你必须说清每个输出借自谁。常见写法：

1. **都借自同一个 `s`**：一个 `'a` 就够。
2. **分别借自 `left` / `right`**：用 `'a` 和 `'b`，返回 `(&'a T, &'b U)`。
3. **逻辑上成套**：定义 `struct Pair<'a, 'b> { .. }` 把关系固化进类型。

```rust
fn head_tail(s: &str) -> (&str, &str) {
    if s.is_empty() {
        ("", "")
    } else {
        (&s[..1], &s[1..])
    }
}

fn main() {
    let (h, t) = head_tail("xyz");
    assert_eq!(h, "x");
    assert_eq!(t, "yz");
}
```

```rust
fn zip_refs<'a, 'b>(left: &'a str, right: &'b str) -> (&'a str, &'b str) {
    (left, right)
}

fn main() {
    let a = String::from("left");
    let b = String::from("right");
    let (l, r) = zip_refs(&a, &b);
    assert_eq!(l, "left");
    assert_eq!(r, "right");
}
```

第一例两个输出都来自同一 `&str`，省略即可；第二例两个输入寿命可能不同，必须分开标，否则编译器没法证明返回值安全。

**🐹 Go 对比：** Go 返回两个指针不需要寿命参数；Rust 要求你在签名里写清“每个返回引用依附哪份输入”。

**记忆点：** 同源共用 `'a`，异源拆开 `'a`/`'b`。

## Q15. 编译器让我加 `'a`，随便写一个能过就行吗？ {#q15}
**Tags:** `common` `diagnostics` `api-design`
**适用版本:** Rust 1.0+

**一句话答案：** 不行。能编译只说明这组标注自洽，不代表 API 语义正确；标错关系会把合法调用误伤，或把寿命绑得过死。

**详细解答：** 生命周期是类型的一部分。乱写常见后果：

1. **把无关输入绑在一起**：`fn f<'a>(x: &'a str, _y: &'a str) -> &'a str { x }` 会强迫调用方让 `y` 活得和返回值一样久，即使根本没用到 `y`。
2. **该分开却强行合并**：缩短了本可更长的借用。
3. **该返回拥有型却硬返回引用**：标注再漂亮也解决不了“数据在哪”的问题。

```rust
fn pick_left<'a>(left: &'a str, _right: &str) -> &'a str {
    left
}

fn main() {
    let left = String::from("keep");
    let result;
    {
        let right = String::from("temp");
        result = pick_left(&left, &right);
    }
    assert_eq!(result, "keep");
}
```

```rust
fn pick_left_wrong<'a>(left: &'a str, _right: &'a str) -> &'a str {
    left
}

fn main() {
    let left = String::from("keep");
    let right = String::from("temp");
    let result = pick_left_wrong(&left, &right);
    assert_eq!(result, "keep");
}
```

第二例虽然也能过编译，但 `_right` 被无绑进返回寿命：一旦 `right` 比结果先结束，合法的“只返回 left”用法会被误拒。正确做法是：先想清数据流，再让标注复述事实；必要时直接返回 `String`/`Vec` 而不是引用。

**🐹 Go 对比：** Go 没有“改个注解就改变哪些调用合法”的生命周期旋钮；Rust 里标注即 API 契约，不是过编译的装饰。

**记忆点：** 标注要复述真实借用关系，不能“能过就行”。

## Q16. 看到生命周期相关报错（如 E0106），第一反应查什么？ {#q16}
**Tags:** `common` `diagnostics` `E0106`
**适用版本:** Rust 1.0+

**一句话答案：** 先读报错里的“哪一个引用缺寿命 / 和谁有关”，再对照三类根因：该标未标、返回了局部、或结构体/异步边界把借用存久了。

**详细解答：** 常见编号与第一反应：

| 报错 | 第一反应 |
|------|----------|
| `E0106` missing lifetime specifier | 多输入引用要返回引用，或结构体字段是引用却没写生命周期参数 |
| `E0515` cannot return reference to local | 别返回局部；改返回拥有型或改借输入 |
| `E0597` borrowed value does not live long enough | 拥有者掉出作用域了；缩小借用范围或延长拥有者 |
| `E0499` / `E0502` | 先是借用冲突，不一定是寿命语法本身 |

排错顺序建议：

1. **数据流**：谁拥有？返回的到底借自谁？
2. **能不能改 API**：返回 `String`/`Vec`/`owned` 是否更简单？
3. **再写标注**：只给真实存在的借用关系命名。

```rust
struct Excerpt<'a> {
    part: &'a str,
}

fn build<'a>(text: &'a str) -> Excerpt<'a> {
    Excerpt { part: text }
}

fn main() {
    let text = String::from("hello");
    let excerpt = build(&text);
    assert_eq!(excerpt.part, "hello");
}
```

```rust
fn first_char(s: &str) -> &str {
    &s[..1]
}

fn main() {
    let owned = String::from("rust");
    assert_eq!(first_char(&owned), "r");
}
```

遇到 `E0106` 时，优先检查：是不是结构体少了 `<'a>`，或函数有多个 `&` 输入却要返回 `&`。先画借用箭头，再改签名，比盲目加 `'a` 快。

**🐹 Go 对比：** Go 几乎看不到这类“缺寿命标注”诊断；Rust 把悬垂引用问题前置成可定位的错误码，值得按码查阅而不是凭感觉堆符号。

**记忆点：** 见 `E0106` 先问“哪个引用缺关系”；见 `E0515` 先问“是不是在返回局部”。

## Q17. 函数该返回 `String` 还是 `&str`？ {#q17}
**Tags:** `common` `return` `api-design`
**适用版本:** Rust 1.0+

**一句话答案：** 数据是函数内部新建的，返回 `String`（或其它拥有型）；数据来自调用方已有缓冲区，才返回 `&str`。别为了“看起来零拷贝”硬返回本地 `String` 的引用。

**详细解答：** 返回类型先问“谁拥有这段字节”。函数里 `format!`、拼接、解析出来的新文本，调用方结束后还要用，就必须把所有权交出去——用 `String`。若只是从输入切片里切一段视图，返回 `&str` 并把寿命绑到输入上。`Cow<'_, str>` 适合“多数借用、少数才分配”的中间态（见智能指针篇），日常 API 先把 `String` / `&str` 选对。

```rust
fn make_label(id: u32) -> String {
    format!("item-{id}")
}

fn main() {
    let label = make_label(7);
    assert_eq!(label, "item-7");
}
```

```rust
fn first_word(s: &str) -> &str {
    match s.find(' ') {
        Some(i) => &s[..i],
        None => s,
    }
}

fn main() {
    let text = String::from("hello rust");
    assert_eq!(first_word(&text), "hello");
}
```

**🐹 Go 对比：** Go 里 `string` 是值语义拷贝（底层共享只读数据），返回局部 `string` 很自然；Rust 的 `&str` 是借用，不能指向马上销毁的本地 `String`。

**记忆点：** 新建数据 → `String`；切别人的数据 → `&str`。

## Q18. `impl` 块上的生命周期参数什么时候才需要写？ {#q18}
**Tags:** `common` `impl`
**适用版本:** Rust 1.0+

**一句话答案：** 类型本身带生命周期（如 `struct Foo<'a>`），或方法签名要把字段原始借用穿透出去、或约束多个寿命关系时，才在 `impl<'a>` 上写；纯拥有型 + 省略规则够用时，不必硬加。

**详细解答：** 三种常见情况：

1. **类型定义有 `'a`**：`impl<'a> Foo<'a> { ... }` 几乎总是要写（也可用 `impl Foo<'_>` 省略命名）。
2. **方法返回比 `&self` 更长的借用**：见 [Q6](#q6)，要显式用结构体上的 `'a`。
3. **无引用类型**：`impl Bar { fn len(&self) -> usize }` 通常完全不需要生命周期参数。

```rust
struct Owned(String);

impl Owned {
    fn as_str(&self) -> &str {
        &self.0
    }
}

fn main() {
    let o = Owned(String::from("ok"));
    assert_eq!(o.as_str(), "ok");
}
```

```rust
struct Borrowed<'a> {
    text: &'a str,
}

impl<'a> Borrowed<'a> {
    fn original(&self) -> &'a str {
        self.text
    }
}

fn main() {
    let source = String::from("rust");
    let b = Borrowed { text: &source };
    assert_eq!(b.original(), "rust");
}
```

**🐹 Go 对比：** Go 的方法接收者没有“寿命参数要不要写在类型上”这层决策；Rust 里 `impl` 上的 `'a` 是在延续类型定义里的借用契约。

**记忆点：** 类型无引用 → `impl` 常可省；类型有 `'a` 或要穿透字段借用 → 再写 `impl<'a>`。

## Q19. `dyn Trait + 'a` 到底在约束什么？ {#q19}
**Tags:** `common` `dyn` `trait-object`
**适用版本:** Rust 1.0+

**一句话答案：** `dyn Trait + 'a` 约束的是**这个 trait 对象内部携带的所有借用至少活到 `'a`**；不是给 Trait 本身“加寿命”，而是给对象里藏着的引用设下限。

**详细解答：** 胖指针 `dyn Trait` 背后可能是带短借用的具体类型。写成 `Box<dyn Trait + 'a>` / `&'a dyn Trait` 时，编译器要求：对象里不能偷偷塞比 `'a` 更短的引用。`dyn Trait + 'static` 表示对象内部不含短借用（拥有型实现者通常满足）。省略时常默认 `'static`（如 `Box<dyn Trait>`），这是很多 API 突然要求 `'static` 的来源之一。

```rust
trait Describe {
    fn describe(&self) -> &str;
}

impl Describe for String {
    fn describe(&self) -> &str {
        self.as_str()
    }
}

fn show(item: &dyn Describe) -> &str {
    item.describe()
}

fn main() {
    let s = String::from("hello");
    assert_eq!(show(&s), "hello");
}
```

```rust
trait Name {
    fn name(&self) -> &str;
}

struct BorrowedName<'a> {
    value: &'a str,
}

impl<'a> Name for BorrowedName<'a> {
    fn name(&self) -> &str {
        self.value
    }
}

fn as_name<'a>(n: &'a dyn Name) -> &'a str {
    n.name()
}

fn main() {
    let text = String::from("Ada");
    let b = BorrowedName { value: &text };
    assert_eq!(as_name(&b), "Ada");
}
```

**🐹 Go 对比：** Go 的 interface 值里塞指针不要求你写“对象活多久”；Rust 的 `dyn Trait + 'a` 把“对象里借用是否够久”写进类型。

**记忆点：** `+ 'a` 约束对象内部借用，不是给 trait 名字贴标签。

## Q20. 报错里的 `lifetime may not live long enough` 该怎么读？ {#q20}
**Tags:** `common` `diagnostics`
**适用版本:** Rust 1.0+

**一句话答案：** 把它读成：“你想让某段借用活到 A，但编译器只证明它活到更短的 B”——通常是返回/存入了比拥有者更久的引用，或把短命局部绑进了更长的签名。

**详细解答：** 这类信息常和 `E0597`、`E0515`、异步/闭包捕获一起出现。读法三步：

1. **哪一个值**被指出“不够久”（报错里的变量名）。
2. **谁要求它更久**（返回类型、结构体字段、`'static`、跨线程、跨 `await`）。
3. **修数据流**：延长拥有者、缩小借用范围，或改返回拥有型（见 [Q3](#q3)、[Q16](#q16)）。

```rust
fn first_char(s: &str) -> &str {
    &s[..1]
}

fn main() {
    let owned = String::from("rust");
    let ch = first_char(&owned);
    assert_eq!(ch, "r");
}
```

```rust
fn take_owned(s: String) -> String {
    s
}

fn main() {
    let result;
    {
        let local = String::from("ok");
        result = take_owned(local);
    }
    assert_eq!(result, "ok");
}
```

第一例借用绑在 `owned` 上，拥有者活着就安全。第二例若改成返回 `&local`，就会触发“lifetime may not live long enough / does not live long enough”——因为 `local` 在块结束时已销毁。看到这句，先对照“要求多久 vs 实际多久”，不要先乱加 `'a`。

**🐹 Go 对比：** Go 很少在编译期用这种措辞拒绝返回局部地址；Rust 把“引用比拥有者活得更久”直接写成可读的寿命诊断。

**记忆点：** 读作“要求的寿命 > 能证明的寿命”；先改数据流，再改标注。
