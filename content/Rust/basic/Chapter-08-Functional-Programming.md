+++
title = "第 8 章 函数式编程"
weight = 80
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter 08 函数式编程（Functional-Programming）

想象一下，你走进一家神奇的餐厅。这家餐厅的菜单上不是具体的菜品，而是一系列"烹饪指令"。你告诉服务员："我想要一份先把食材切成丁，然后用油炒一下，最后加盐的菜。" 服务员面带微笑地接过这张小纸条，不慌不忙地走向厨房。几分钟后，一道热气腾腾的菜品就端到了你面前。

恭喜你，你刚刚体验了一把函数式编程的精髓——你描述的是"做什么"而不是"怎么做"。在传统的命令式编程中，你可能会这样点餐："先去冰箱拿食材，开火，倒油，放入食材，用铲子翻炒30秒，加盐，关火，装盘。" 但在函数式编程的世界里，你只需要说："给我来一个炒的、加盐的、切成丁的版本。"

Rust 这门语言可不仅仅是一门"安全系统编程语言"这么单调。它还藏着一颗函数式编程的心脏，而且这颗心脏跳得相当有力。在这一章里，我们将一起探索 Rust 中三大函数式神器：闭包（Closure）、迭代器（Iterator）和函数式错误处理。它们就像是《哈利·波特》里的三件圣器，各有各的魔法，但组合在一起时，能让你的代码变得既优雅又强大。

> 温馨提示：阅读本章时，请保持轻松愉快的心情。如果你在阅读过程中笑出声来，那正是作者追求的效果。如果没笑... 那一定是我的幽默细胞今天请假了。

## 8.1 闭包（Closure）

### 8.1.1 闭包的定义与语法

好，让我们来聊聊闭包。闭包是什么？想象一下，你正在写一封情书，但是你不打算立刻送出去。你把情书写在一张小纸条上，然后把这张小纸条塞进口袋里，打算等一个合适的时机再拿出来。这张小纸条上写着你当时的心情和想法，而且它一直保留着那一刻的状态。

在编程的世界里，闭包就是这么一个"随身携带的小纸条"。它是一个可以捕获其定义时周围环境（我们称之为"作用域"）中变量的函数。闭包可以像普通函数一样被调用，但它们还偷偷记住了定义时那些变量的值。

在 Rust 中，闭包的语法非常简洁，简直就是程序员偷懒的完美范例：

```rust
let add_one = |x: i32| -> i32 { x + 1 };  // 一个简单的闭包，给数字加1
```

看到了吗？闭包的语法由三部分组成：

- 管道符号 `|...|` 之间是参数，就像函数的参数列表，但是用竖线包起来
- `->` 后面是返回类型（有时候可以省略，Rust 的类型推断会帮你搞定）
- 大括号 `{}` 里面是闭包的函数体

如果你写过 Python 的 lambda 表达式或者 JavaScript 的箭头函数，你会发现 Rust 的闭包语法简直是它们的"表哥"——长得像，但更有型。

#### 8.1.1.1 闭包的基本语法

让我们从最基础的说起。Rust 闭包的基本语法如下：

```rust
let closure_name = |parameters| -> return_type { body };
```

或者更简洁的版本（省略返回类型，让类型推断来处理）：

```rust
let closure_name = |parameters| { body };
```

再或者，如果函数体只有一行表达式，甚至可以省略大括号：

```rust
let closure_name = |parameters| expression;
```

下面是一些实际例子：

```rust
fn main() {
    // 带完整类型标注的闭包
    let square = |x: i32| -> i32 { x * x };  // 计算平方
    println!("5 的平方是: {}", square(5));  // 25

    // 省略返回类型，编译器会自动推断
    let double = |x: i32| { x * 2 };  // 计算两倍
    println!("7 的两倍是: {}", double(7));  // 14

    // 单行表达式可以省略大括号
    let is_even = |x: i32| x % 2 == 0;  // 判断是否为偶数
    println!("8 是偶数吗? {}", is_even(8));  // true

    // 没有参数的闭包
    let answer = || { 42 };  // 直接返回一个值
    println!("生命的意义是: {}", answer());  // 42
}
```

> 等等，你说没有参数的闭包？那它闭了个什么？答案是：它闭住的是"定义时的上下文"，比如它可以访问定义时作用域内的变量。没错，闭包不一定要"闭"什么参数，但它永远都会"闭"住它的环境。

#### 8.1.1.2 单参数 / 多参数 / 无参数闭包

闭包的参数可以是零个、一个或多个。Rust 的类型系统会根据你如何使用闭包来推断参数和返回值的类型。

```rust
fn main() {
    // 单参数闭包：判断一个数是否大于10
    let greater_than_ten = |x: i32| -> bool { x > 10 };
    println!("15 > 10 吗? {}", greater_than_ten(15));  // true

    // 多参数闭包：计算两个数的和与积
    let add_and_multiply = |a: i32, b: i32| -> (i32, i32) {
        (a + b, a * b)
    };
    let (sum, product) = add_and_multiply(3, 4);
    println!("3 + 4 = {}, 3 * 4 = {}", sum, product);  // 7, 12

    // 无参数闭包：返回一个固定值
    let get_max_i32 = || -> i32 { i32::MAX };
    println!("i32 的最大值是: {}", get_max_i32());  // 2147483647

    // 无参数闭包：访问外部变量
    let base = 100;
    let add_to_base = || -> i32 { base + 50 };
    println!("100 + 50 = {}", add_to_base());  // 150
}
```

多参数闭包的类型推断有时候会需要一点小技巧，但 Rust 编译器通常很聪明，能够自动推断出正确的类型。就像一个尽职的图书管理员，你不需要告诉他书在哪里，他自己会找到。

#### 8.1.1.3 闭包作为变量

在 Rust 中，闭包可以像普通变量一样被赋值、传递和存储。这可是闭包真正厉害的地方——它们是"一等公民"（first-class citizen）。这意味着闭包可以：

1. 赋给变量
2. 作为函数参数传递
3. 作为函数返回值返回
4. 存储在数据结构中

```rust
fn main() {
    // 闭包赋值给变量
    let greet = |name: &str| {
        format!("你好, {}! 欢迎来到 Rust 的世界!", name)
    };
    println!("{}", greet("小明"));  // 你好, 小明! 欢迎来到 Rust 的世界!

    // 闭包存储在 Vector 中（但需要使用 Box 包装）
    let mut calculators: Vec<Box<dyn Fn(i32) -> i32>> = Vec::new();
    calculators.push(Box::new(|x| x * 2));  // 两倍
    calculators.push(Box::new(|x| x * x));  // 平方
    calculators.push(Box::new(|x| x - 1));  // 减一

    // 使用下标调用不同的闭包
    println!("8 的两倍是: {}", calculators[0](8));  // 16
    println!("8 的平方是: {}", calculators[1](8));  // 64
    println!("8 减 1 是: {}", calculators[2](8));  // 7

    // 将闭包作为函数参数传递（稍后会详细讲解）
    let numbers = vec![1, 2, 3, 4, 5];
    let result = apply_with_op(&numbers, |x| x * 2);
    println!("每个数翻倍: {:?}", result);  // [2, 4, 6, 8, 10]
}

// 一个接受闭包作为参数的函数
fn apply_with_op(nums: &[i32], op: impl Fn(i32) -> i32) -> Vec<i32> {
    nums.iter().map(|&x| op(x)).collect()
}
```

> 为什么我们需要 `Box<dyn Fn(...)>` 呢？因为闭包的大小在编译时可能是未知的（不同的闭包可能有不同的"重量级"）。`Box` 就像一个指针，给闭包分配一个固定大小的"门牌号"，这样 Rust 就知道怎么管理它们了。

#### 8.1.1.4 多行闭包

有些闭包比较复杂，一行写不下怎么办？别担心，大括号 `{}` 就是为这种情况准备的：

```rust
fn main() {
    // 多行闭包：复杂的数学计算
    let complex_calc = |x: f64| -> f64 {
        let part1 = x.powi(2);  // x 的平方
        let part2 = (x * std::f64::consts::PI).sin();  // x * π 的正弦
        let part3 = x.sqrt();  // x 的平方根
        (part1 + part2) / part3  // 返回组合结果
    };

    println!("当 x=4.0 时的复杂计算结果: {:.4}", complex_calc(4.0));

    // 多行闭包：字符串处理
    let process_text = |text: &str| -> String {
        let trimmed = text.trim();  // 去除首尾空白
        let uppercased = trimmed.to_uppercase();  // 转大写
        let words: Vec<&str> = uppercased.split_whitespace().collect();  // 分词
        words.join("_")  // 用下划线连接
    };

    let input = "  Hello Rust World  ";
    println!("处理后的文本: {}", process_text(input));  // HELLO_RUST_WORLD

    // 多行闭包：模拟一个简单的状态机
    let tick_tock = |state: &mut bool| -> &str {
        *state = !*state;  // 切换状态
        if *state {
            "Tick"
        } else {
            "Tock"
        }
    };

    let mut is_tick = true;
    println!("{}", tick_tock(&mut is_tick));  // Tick
    println!("{}", tick_tock(&mut is_tick));  // Tock
    println!("{}", tick_tock(&mut is_tick));  // Tick
    println!("{}", tick_tock(&mut is_tick));  // Tock
}
```

多行闭包就像是一份详细的购物清单，你可以把所有的步骤都写在一起，然后一次性执行。在实际开发中，当闭包的逻辑变得复杂时，使用多行语法会让代码更清晰、更易维护。

### 8.1.2 闭包的类型推断

Rust 是一门静态类型语言，但它同时也是一门极其聪明的类型推断语言。闭包的类型推断尤其有趣，因为它涉及到一个独特的特性：每个闭包实例都有自己独特的类型。

#### 8.1.2.1 闭包类型是唯一的

在 Rust 中，每一个闭包表达式都会产生一个唯一的、匿名的类型。就像世界上没有两片完全相同的雪花一样，Rust 里也没有两个完全相同的闭包类型。这听起来很浪漫，但实际上它是 Rust 能够在编译时进行大量优化的关键。

```rust
fn main() {
    // 闭包 add_a 和 add_b 看起来完全一样，但它们是不同的类型！
    let add_a = |x: i32| x + 5;
    let add_b = |x: i32| x + 5;

    // 即使类型签名相同，下面的代码也无法编译：
    // let another_add = add_a;  // 错误：不能这样赋值
    // 原因：闭包的类型是私有的，编译器自动生成的，没人知道它叫啥

    // 正确的方式：使用泛型或者 dyn trait
    let mut closures: Vec<Box<dyn Fn(i32) -> i32>> = Vec::new();
    closures.push(Box::new(add_a));  // 包装成 dyn Fn
    // closures.push(Box::new(add_b));  // 同样可以添加另一个闭包

    println!("使用闭包 add_a: {}", closures[0](10));  // 15

    // 如果你想让多个闭包有相同的类型以便存储在一起，必须使用 trait 对象
    fn use_closure<F>(f: F) where F: Fn(i32) -> i32 {
        println!("结果是: {}", f(100));
    }

    let my_closure = |x| x * 2;
    use_closure(my_closure);  // 200
    use_closure(|x| x + 1);  // 101，直接使用内联闭包
}
```

这里有一个非常有意思的现象：虽然 `add_a` 和 `add_b` 的行为完全一致，但 Rust 编译器把它们当作完全不同的类型。这是为什么呢？

因为闭包不仅要存储它的"行为"（代码），还要存储它"捕获"的变量。想象一下，如果有两个闭包都捕获了同一个变量 `n`，但它们捕获的方式不同（比如一个是只读引用，另一个是可变引用），那它们能一样吗？显然不能！

```rust
fn main() {
    let value = 10;

    // 这个闭包捕获的是 value 的不可变引用
    let read_value = || println!("value 是: {}", value);

    // 这个闭包... 等等，如果你想修改 value，你需要用 mut
    let mut value = 10;  // 注意：这里是可变的 value
    let read_and_increment = || {
        value += 1;
        println!("value 变成了: {}", value);
    };

    read_value();  // value 是: 10
    read_and_increment();  // value 变成了: 11
    read_and_increment();  // value 变成了: 12

    // 每次调用 read_and_increment，value 都会变化
    // 因为这个闭包捕获的是 value 的可变引用
}
```

> 闭包类型唯一性是 Rust 实现"零成本抽象"的基础。因为编译器知道每个闭包的确切类型，所以它可以进行激进的优化，甚至把闭包"内联"（inline）——也就是说，把闭包的代码直接插入到调用点，就好像根本没有闭包这个东西一样。这就是 Rust 所谓的"你不需要为抽象付出运行时成本"。

### 8.1.3 Fn / FnMut / FnOnce 三种 trait

如果说闭包是 Rust 函数式编程的肌肉，那么 `Fn`、`FnMut` 和 `FnOnce` 这三个 trait 就是定义这些肌肉如何工作的筋骨。它们就像是超级英雄的三种变身形态，每个都有自己独特的超能力。

trait 是 Rust 中定义共享行为的方式，类似于其他语言中的接口（interface）。这三个 trait 专门用来描述闭包的调用方式，它们之间的区别在于闭包如何处理捕获的变量。

#### 8.1.3.1 Fn trait

`Fn` trait 是最"温和"的闭包形态。一个实现了 `Fn` trait 的闭包可以无数次调用，而且不会消耗（consume）它捕获的变量。这就像一个永远都有电的手电筒，你想照多少次就照多少次。

```rust
fn main() {
    let greeting = "你好".to_string();

    // 这个闭包实现了 Fn trait，因为它只是"借用"了 greeting
    let say_hello = || {
        println!("{}, 世界!", greeting);  // greeting 被借用，不是被移动
    };

    // 可以调用任意多次
    say_hello();  // 你好, 世界!
    say_hello();  // 你好, 世界!
    say_hello();  // 你好, 世界!

    // greeting 仍然有效！
    println!("闭包调用完毕后，greeting 还在: {}", greeting);  // 你好

    // Fn 闭包可以作为函数参数
    fn call_twice<F: Fn()>(f: F) {
        f();
        f();
    }

    call_twice(say_hello);
    // 你好, 世界!
    // 你好, 世界!
}
```

#### 8.1.3.2 FnMut trait

`FnMut` trait 代表那些会修改捕获变量的闭包。这种闭包不能被多次调用而不受影响——每次调用都可能改变它的状态。把它想象成一个电灯开关：你按一次，灯亮了；再按一次，灯灭了。闭包本身的状态在改变。

```rust
fn main() {
    let mut counter = 0;

    // 这个闭包实现了 FnMut trait，因为它修改了 counter
    let mut increment = || {
        counter += 1;
        println!("计数器的当前值: {}", counter);
    };

    // 第一次调用
    increment();  // 计数器的当前值: 1

    // 第二次调用
    increment();  // 计数器的当前值: 2

    // 第三次调用
    increment();  // 计数器的当前值: 3

    // FnMut 闭包可以作为可变借用的参数
    fn call_mutually<F: FnMut()>(mut f: F) {
        f();
        f();
    }

    let mut base = 10;
    call_mutually(|| {
        base *= 2;
        println!("base 翻倍了: {}", base);
    });
    // base 翻倍了: 20
    // base 翻倍了: 40
}
```

#### 8.1.3.3 FnOnce trait

`FnOnce` trait 是最"霸道"的闭包形态。这种闭包会"吃掉"（consume）它捕获的变量，只能被调用一次。就像那句歌词——"只爱你一次，吻完就消失"。一旦调用完毕，闭包捕获的那些变量就"没有了"。

为什么叫 `Once`？因为有些操作只能做一次。比如把一个值移动（move）走，这个动作一辈子只能做一次。

```rust
fn main() {
    let words = vec!["Rust", "是", "很", "酷", "的"];

    // 这个闭包实现了 FnOnce trait，因为它"吃掉"了 words
    let consume_and_print = || {
        // words 被移动进这个闭包了
        let copied_words = words;  // 所有权转移
        println!("被吃掉的 words: {:?}", copied_words);
    };

    // 只能调用一次！
    consume_and_print();

    // 下面的代码无法编译，因为 words 已经被"吃掉"了：
    // consume_and_print();  // 错误：words 已经被移动
    // println!("{:?}", words);  // 错误：words 不再属于这里

    // FnOnce 经常与 move 一起使用
    let data = vec![1, 2, 3];
    let move_closure = move || {
        println!("data 被打包带走了: {:?}", data);
        // data 被移动进闭包，此后再也无法在外部访问
    };

    move_closure();
    // move_closure();  // 错误：只能调用一次

    // 有趣的是，FnOnce 闭包可以用闭包表达式（|| expr）直接调用一次
    (|| {
        let msg = String::from("一次性闭包");
        println!("{}", msg);
    })();
}
```

#### 8.1.3.4 三者的继承关系

这三个 trait 之间有一个美妙的层次关系：

```text
FnOnce
  ↑
FnMut
  ↑
Fn
```

简单来说：

- 所有的 `FnMut` 闭包同时也是 `FnOnce`
- 所有的 `Fn` 闭包同时也是 `FnMut` 和 `FnOnce`
- 但反过来不成立：`FnOnce` 不一定是 `FnMut`，`FnMut` 不一定是 `Fn`

这就像生物分类：所有的猫是哺乳动物，但并不是所有的哺乳动物都是猫。

```rust
fn main() {
    // 演示 trait 约束的使用
    fn call_fn<F: Fn()>(f: F) { f(); }           // 最严格，只能是 Fn
    fn call_fn_mut<F: FnMut()>(mut f: F) { f(); }  // 中等，可以是 Fn 或 FnMut
    fn call_fn_once<F: FnOnce()>(f: F) { f(); }     // 最宽松，都行

    let value = "Hello".to_string();

    // 这个闭包是 Fn，因为它只是借用了 value
    let read_only = || println!("读取: {}", value);

    // Fn 可以传递给任何接受 Fn/FnMut/FnOnce 的函数
    call_fn(read_only);       // OK: Fn -> Fn
    call_fn_mut(read_only);   // OK: Fn -> FnMut
    call_fn_once(read_only);  // OK: Fn -> FnOnce

    println!("\n--- 分割线 ---\n");

    // 演示 FnMut 的例子
    let mut count = 0;
    let mut increment = || { count += 1; };

    // FnMut 不能传递给只接受 Fn 的函数
    // call_fn(increment);  // 错误：FnMut 不能传给 Fn
    call_fn_mut(increment);   // OK: FnMut -> FnMut
    call_fn_once(increment);  // OK: FnMut -> FnOnce

    println!("\n--- 分割线 ---\n");

    // 演示 FnOnce 的例子
    let owned = vec![1, 2, 3];
    let consume = move || { owned };  // FnOnce，捕获的值会被移动

    // FnOnce 只能传给 FnOnce
    // call_fn(consume);     // 错误
    // call_fn_mut(consume); // 错误
    call_fn_once(consume);    // OK: FnOnce -> FnOnce

    println!("\n三者的关系总结:");
    println!("Fn: 可以多次调用，只借用环境");
    println!("FnMut: 可以多次调用，借用并修改环境");
    println!("FnOnce: 只调用一次，会消费环境中的值");
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                    FnOnce (最宽泛)                      │
│  "我只调用一次，但我不挑食，什么闭包都行"                  │
└───────────────────────┬─────────────────────────────────┘
                        │ 继承
┌───────────────────────▼─────────────────────────────────┐
│                    FnMut (中等)                          │
│  "我可以调用多次，但我可能会改变闭包的状态"                │
└───────────────────────┬─────────────────────────────────┘
                        │ 继承
┌───────────────────────▼─────────────────────────────────┐
│                      Fn (最严格)                         │
│  "我最守规矩，只读取不修改，可以随便调用"                   │
└─────────────────────────────────────────────────────────┘
```

> 记忆小技巧：把 `Fn` 想象成"读小说"——你可以读很多遍，小说本身不会改变。把 `FnMut` 想象成"填涂鸦书"——你每次涂，书本都会有变化。把 `FnOnce` 想象成"吃蛋糕"——吃完就没了，别想着再吃一次。

### 8.1.4 闭包的捕获方式

闭包最神奇的能力之一就是能够"捕获"定义时环境中的变量。但是，Rust 的编译器可是一丝不苟的，它会仔细审查闭包是如何捕获每个变量的。Rust 确定了四种捕获方式，每种都有其适用场景。

#### 8.1.4.1 按引用捕获

按引用捕获是最"温柔"的方式。闭包只是借用（borrow）环境中的变量，就像去图书馆借书——你可以看，但书还是图书馆的。

```rust
fn main() {
    let message = String::from("Rust 编程");

    // 按引用捕获，不会获得 message 的所有权
    let print_ref = || {
        println!("闭包中的 message (引用): {}", message);
    };

    print_ref();
    print_ref();
    print_ref();  // 想调用多少次都行

    // message 仍然有效，可以继续使用
    println!("闭包外部的 message: {}", message);  // Rust 编程

    // 另一个按引用捕获的例子
    let numbers = vec![1, 2, 3, 4, 5];
    let sum = || {
        numbers.iter().sum::<i32>()
    };

    println!("数字之和: {}", sum());  // 15
    println!("原始数组还在: {:?}", numbers);  // [1, 2, 3, 4, 5]
}
```

按引用捕获是最常用的方式，适用于闭包只需要读取环境变量的场景。Rust 的借用检查器确保在闭包执行期间，被借用的变量不会被移走或修改。

#### 8.1.4.2 按可变引用捕获

有些时候，闭包需要修改环境中的变量。这时候 Rust 就会使用可变引用（`&mut`）来捕获。这就像你借了一本书，然后在上面做笔记——书还是图书馆的，但被你涂涂改改了。

```rust
fn main() {
    let mut score = 0;

    // 按可变引用捕获，闭包需要修改 score
    let mut increment = || {
        score += 1;
        println!("分数增加了，当前分数: {}", score);
    };

    increment();  // 分数增加了，当前分数: 1
    increment();  // 分数增加了，当前分数: 2
    increment();  // 分数增加了，当前分数: 3

    // score 被修改了
    println!("最终分数: {}", score);  // 3

    // 另一个例子：闭包内部维护状态
    let mut state = String::from("初始状态");

    let mut modify_state = || {
        state.push_str(" -> 被修改");
        println!("状态更新: {}", state);
    };

    modify_state();
    // 外部的 state 也被修改了
    println!("外部观察: {}", state);  // 初始状态 -> 被修改

    // 注意：按可变引用捕获的闭包，在调用时不能有其他借用存在
    let text = String::from("Hello");

    let mut to_uppercase = || {
        // text.push_str(" World");  // 错误：text 被可变借用，但这是 FnMut
        println!("转换为大写: {}", text.to_uppercase());
    };

    to_uppercase();
    // text.to_uppercase() 创建了一个新的 String，没有修改 original
    println!("原始文本: {}", text);  // Hello
}
```

按可变引用捕获有一个重要的限制：在闭包执行期间，不能有任何其他的借用存在。这是为了避免数据竞争（data race）。

#### 8.1.4.3 按值捕获（move）

有些闭包需要"彻底拿走"环境中的变量——不仅仅是借用，而是完全接管所有权。这就是 `move` 闭包的用武之地。按值捕获就像你从图书馆买了一本书——这本书现在是你的了，图书馆再也没有副本了。

```rust
fn main() {
    let name = String::from("Rust");

    // 按值捕获，name 的所有权被移动进闭包
    let capture_by_value = move || {
        println!("闭包拥有 name: {}", name);
        // name 在这里被使用后就不再属于外部作用域了
    };

    capture_by_value();
    // capture_by_value();  // 错误：FnOnce 闭包只能调用一次

    // 下面的代码无法编译，因为 name 已经被移走了
    // println!("{}", name);  // 错误：name 被移动

    println!("\n--- 分割线 ---\n");

    // 常见场景：在多线程中使用闭包
    use std::thread;

    let data = vec![1, 2, 3, 4, 5];

    // 在新线程中使用闭包，必须 move，因为线程可能会在主线程结束前执行
    let handle = thread::spawn(move || {
        println!("子线程读取 data: {:?}", data);
        // data 在这里是独立的所有权
        let sum: i32 = data.iter().sum();
        sum
    });

    let result = handle.join().unwrap();
    println!("子线程计算结果: {}", result);  // 15

    // data 已经在主线程中无效了
    // println!("{:?}", data);  // 错误：data 已被移动

    println!("\n--- 分割线 ---\n");

    // 数值类型按值捕获仍然可以多次使用
    let number = 42;

    let print_number = move || {
        println!("捕获的数字: {}", number);
        println!("再捕获一次: {}", number);
    };

    print_number();  // 42, 42
    // print_number();  // 错误：虽然 i32 是 Copy，但 move 闭包是 FnOnce
}
```

> 为什么数值类型可以"再捕获一次"？因为 `i32` 这样的类型实现了 `Copy` trait，意味着它们被复制而不是被移动。所以即使按值捕获，闭包也会得到一个副本，原变量依然有效。而 `String` 这样的类型没有 `Copy`，只有 `Move`，所以一旦移走，原变量就无效了。

#### 8.1.4.4 捕获方式推断规则

Rust 编译器非常智能，它会自动推断闭包应该使用哪种捕获方式。推断规则遵循以下优先级：

1. 如果闭包内部没有修改捕获的变量，且变量没有实现 `Copy`，使用引用捕获（`&T`）
2. 如果闭包内部修改了捕获的变量，使用可变引用捕获（`&mut T`）
3. 如果闭包会消费（consume）捕获的变量（即调用 `FnOnce`），使用值捕获（`T`）
4. 如果变量实现了 `Copy`，总是使用值捕获

```rust
fn main() {
    // 规则1：不可变借用
    let text = String::from("Hello");
    let print = || println!("{}", text);  // &String
    print();
    println!("外部还能用: {}", text);  // Hello

    // 规则2：可变借用
    let mut counter = 0;
    let mut inc = || { counter += 1; };  // &mut counter
    inc();
    println!("计数器: {}", counter);  // 1

    // 规则3：消费变量（FnOnce）
    let owned = vec![1, 2, 3];
    let consume = || { owned };  // 消费 owned，owned 被移动
    let taken = consume();
    println!("取走的内容: {:?}", taken);  // [1, 2, 3]
    // println!("{:?}", owned);  // 错误：owned 已被移走

    // 规则4：Copy 类型总是值捕获
    let x = 5;
    let use_x = || println!("x = {}", x);  // 值捕获，因为 i32 是 Copy
    use_x();
    println!("x 还在: {}", x);  // x 还在，因为是副本
}
```

### 8.1.5 闭包作为函数参数

闭包作为"一等公民"最厉害的应用之一，就是可以把闭包作为参数传递给函数。这在 Rust 中被称为"高阶函数"（higher-order functions）——也就是接收函数作为参数或返回函数的函数。

#### 8.1.5.1 F: Fn(i32) -> i32

在 Rust 中，我们可以使用 trait bound 来约束函数参数必须是某种类型的闭包。`Fn(i32) -> i32` 表示一个接收 `i32` 参数并返回 `i32` 的闭包。

```rust
fn main() {
    // 使用泛型 + trait bound 接受闭包参数
    fn apply<F>(x: i32, f: F) -> i32
    where
        F: Fn(i32) -> i32,  // F 是一个接收 i32 返回 i32 的闭包
    {
        f(x)
    }

    // 使用具体的闭包
    let square = |x: i32| x * x;
    let triple = |x: i32| x * 3;
    let negate = |x: i32| -x;

    println!("平方: apply(5, square) = {}", apply(5, square));  // 25
    println!("三倍: apply(5, triple) = {}", apply(5, triple));  // 15
    println!("取反: apply(5, negate) = {}", apply(5, negate));  // -5

    // 直接传入内联闭包
    println!("加10: apply(7, |x| x + 10) = {}", apply(7, |x| x + 10));  // 17

    // 组合多个操作
    fn compose<A, B, C, F, G>(f: F, g: G) -> impl Fn(A) -> C
    where
        F: Fn(A) -> B,
        G: Fn(B) -> C,
    {
        move |x| g(f(x))
    }

    let add_one = |x: i32| x + 1;
    let double = |x: i32| x * 2;
    let add_one_then_double = compose(add_one, double);

    println!("(5 + 1) * 2 = {}", add_one_then_double(5));  // 12

    // 接受多个闭包参数
    fn apply_both<F, G>(x: i32, y: i32, f: F, g: G) -> i32
    where
        F: Fn(i32, i32) -> i32,
        G: Fn(i32) -> i32,
    {
        g(f(x, y))
    }

    let add = |a, b| a + b;
    println!("(3 + 4) * 10 = {}", apply_both(3, 4, add, |x| x * 10));  // 70
}
```

闭包作为参数的常见用途包括：

- `map`、`filter` 等迭代器方法
- 回调函数
- 策略模式（Strategy Pattern）
- 函数组合

```rust
// 策略模式的例子
fn main() {
    // 定义一个排序策略
    trait SortStrategy<T> {
        fn sort(&self, data: &mut [T])
        where
            T: Ord;
    }

    // 升序策略
    struct Ascending;
    impl<T: Ord> SortStrategy<T> for Ascending {
        fn sort(&self, data: &mut [T]) {
            data.sort();
        }
    }

    // 降序策略
    struct Descending;
    impl<T: Ord> SortStrategy<T> for Descending {
        fn sort(&self, data: &mut [T]) {
            data.sort_by(|a, b| b.cmp(a));
        }
    }

    // 使用闭包作为策略
    fn sort_with<F>(data: &mut [i32], compare: F)
    where
        F: Fn(&i32, &i32) -> std::cmp::Ordering,
    {
        data.sort_by(compare);
    }

    let mut numbers = vec![3, 1, 4, 1, 5, 9, 2, 6];

    // 使用闭包实现奇数优先排序
    sort_with(&mut numbers, |a, b| {
        let a_is_odd = a % 2 == 1;
        let b_is_odd = b % 2 == 1;
        if a_is_odd != b_is_odd {
            if a_is_odd { std::cmp::Ordering::Less } else { std::cmp::Ordering::Greater }
        } else {
            a.cmp(b)
        }
    });

    println!("奇数优先排序: {:?}", numbers);
}
```

### 8.1.6 闭包作为返回值

说完了闭包作为参数，怎么能不说闭包作为返回值呢？闭包不仅可以"进来"，还可以"出去"。把闭包作为返回值返回的函数就像是"工厂函数"——它们生产闭包。

#### 8.1.6.1 impl Trait

在 Rust 中，如果我们想返回一个闭包，需要使用 `impl Trait` 语法或者 `Box<dyn Fn(...)>` 来明确告诉编译器返回的类型。

```rust
fn main() {
    // 使用 impl Trait 语法返回闭包
    fn make_adder(n: i32) -> impl Fn(i32) -> i32 {
        move |x| x + n  // 返回一个捕获了 n 的闭包
    }

    let add_5 = make_adder(5);
    let add_10 = make_adder(10);
    let add_100 = make_adder(100);

    println!("5 + 5 = {}", add_5(5));   // 10
    println!("5 + 10 = {}", add_10(5));  // 15
    println!("5 + 100 = {}", add_100(5)); // 105

    // make_adder 是闭包工厂函数的经典例子
    // 每次调用都会创建一个新的闭包实例
    println!("\n--- 分割线 ---\n");

    // 返回可变的闭包
    fn make_counter(start: i32) -> impl FnMut() -> i32 {
        let mut current = start;
        move || {
            current += 1;
            current
        }
    }

    let mut counter1 = make_counter(0);
    let mut counter2 = make_counter(100);

    println!("计数器1: {}", counter1());  // 1
    println!("计数器1: {}", counter1());  // 2
    println!("计数器1: {}", counter1());  // 3
    println!("计数器2: {}", counter2());  // 101
    println!("计数器2: {}", counter2());  // 102

    println!("\n--- 分割线 ---\n");

    // 返回一次性闭包 (FnOnce)
    fn create_greeter(name: String) -> impl FnOnce() {
        move || {
            println!("你好, {}!", name);
        }
    }

    let greeter = create_greeter(String::from("Rustacean"));
    greeter();  // 你好, Rustacean!

    // 更复杂的例子：返回一个数学函数
    fn make_multiplier(factor: f64) -> impl Fn(f64) -> f64 {
        move |x| x * factor
    }

    let triple = make_multiplier(3.0);
    let root = make_multiplier(0.5);

    println!("5 * 3 = {}", triple(5.0));   // 15
    println!("5 * 0.5 = {}", root(5.0));    // 2.5
    println!("sqrt(16) = {}", triple(root(16.0)));  // 24
}
```

使用 `impl Trait` 返回闭包有几个限制：

1. 只能返回一种具体的闭包类型
2. 不能在同一个函数中根据条件返回不同的闭包类型

如果需要返回不同类型的闭包，就必须使用 trait 对象（`Box<dyn Fn(...)>`）：

```rust
fn main() {
    // 使用 Box<dyn Fn> 可以返回不同类型的闭包
    fn create_calculator(op: &str) -> Box<dyn Fn(i32, i32) -> i32> {
        match op {
            "add" => Box::new(|a, b| a + b),
            "sub" => Box::new(|a, b| a - b),
            "mul" => Box::new(|a, b| a * b),
            "div" => Box::new(|a, b| a / b),
            _ => Box::new(|_, _| 0),
        }
    }

    let calculator = create_calculator("add");
    println!("10 + 5 = {}", calculator(10, 5));  // 15

    let calculator = create_calculator("mul");
    println!("10 * 5 = {}", calculator(10, 5));  // 50
}
```

### 8.1.7 move 关键字

`move` 关键字是 Rust 闭包世界中的一位特殊角色。它就像是闭包的一剂"强心针"——打完之后，闭包就会不顾一切地把捕获的变量"抢"过来，不管这些变量是 `Copy` 还是 `Move`。

#### 8.1.7.1 move 强制获取所有权

`move` 关键字的主要用途是强制闭包获取捕获变量的所有权。这在以下场景特别有用：

1. **多线程编程**：线程可能在线程创建者销毁之后仍然运行，所以闭包需要拥有自己的数据副本
2. **确保闭包拥有数据**：避免悬垂引用（dangling reference）
3. **明确语义**：让代码的意图更加清晰

```rust
fn main() {
    // 基本用法：move 强制闭包获取变量的所有权
    let data = vec![1, 2, 3];

    // 没有 move：闭包借用 data
    let borrow_only = || println!("借用: {:?}", data);
    println!("调用前: {:?}", data);  // data 还在
    borrow_only();
    println!("调用后: {:?}", data);  // data 还在

    println!("\n--- 分割线 ---\n");

    // 有 move：闭包获取 data 的所有权
    let data2 = vec![4, 5, 6];
    let take_ownership = move || println!("所有权转移: {:?}", data2);
    take_ownership();
    // 下面的代码无法编译，因为 data2 已经被移走了
    // println!("{:?}", data2);  // 错误！

    println!("\n--- 分割线 ---\n");

    // move 在多线程中的重要性
    use std::thread;

    let shared_data = vec![1, 2, 3];

    // 在 spawn 中使用 move 确保数据在线程间安全传递
    let handle = thread::spawn(move || {
        println!("子线程读取: {:?}", shared_data);
        // shared_data 在这里是独立的所有权
    });

    handle.join().unwrap();

    // 主线程中 shared_data 已经无效
    // println!("{:?}", shared_data);  // 错误！

    println!("\n--- 分割线 ---\n");

    // move 闭包与 FnOnce 的关系
    fn call_once<F: FnOnce()>(f: F) {
        f();
    }

    let important_data = String::from("重要的数据");

    // 这里必须用 move，因为闭包是 FnOnce
    call_once(move || {
        println!("{}", important_data);
    });

    // 重要数据已经被"消费"了
    // println!("{}", important_data);  // 错误！

    println!("\n--- 分割线 ---\n");

    // move 与闭包捕获的组合
    let x = 10;
    let y = 20;

    // 同时使用 move 和其他捕获方式
    let closure_with_move = move || {
        // x 被移动进来了（i32 是 Copy，所以外部的 x 仍然有效）
        let copied_x = x;  // 复制了一份
        copied_x + y  // y 是借用的
    };

    println!("闭包结果: {}", closure_with_move());  // 30
    println!("x 还在: {}", x);  // 10，i32 是 Copy
    // println!("y 还在: {}", y);  // 错误：y 被借用了
}
```

> 一个小技巧：对于实现了 `Copy` trait 的类型（如 `i32`、`f64`、`bool` 等），`move` 并不会真正"拿走"什么，因为这些类型在被使用时会自动复制。所以外部的变量依然有效。但对于 `String`、`Vec`、`Box` 等没有 `Copy` 的类型，`move` 就真的是"拿走"了。

## 8.8 迭代器（Iterator）

如果说闭包是 Rust 函数式编程的心脏，那么迭代器就是它的四肢——负责实际执行那些优雅的操作。迭代器让你能够以一种声明式、函数式的方式处理序列数据，而不需要编写那些冗长的循环语句。

想象一下汽车生产线。在传统的命令式编程中，你是一个工人，需要手动拿起每个零件，检查它，组装它，最后放到传送带上。但在 Rust 的迭代器世界里，你只需要告诉机器："给我检查所有零件，把不合格的挑出来，然后把剩下的组装好。" 机器就会自动完成剩下的工作。

这就是函数式编程的魅力所在——描述"做什么"而不是"怎么做"。

### 8.8.1 Iterator Trait 定义

在 Rust 中，迭代器是一个实现了 `Iterator` trait 的类型。这个 trait 定义了迭代器的基本行为：如何逐个产生元素。

#### 8.8.1.1 trait Iterator

`Iterator` trait 是 Rust 标准库中最核心的 trait 之一。它的定义出奇的简单：

```rust
pub trait Iterator {
    type Item;  // 迭代器产生的元素类型

    // 核心方法：返回下一个元素
    fn next(&mut self) -> Option<Self::Item>;

    // 其他默认方法...
}
```

任何实现 `Iterator` 的类型都必须实现 `next` 方法。这个方法返回 `Option<Self::Item>`——要么是 `Some(item)`，要么是 `None`（当迭代完成时）。

```rust
fn main() {
    // 看看 Iterator trait 的基本结构
    let numbers = vec![1, 2, 3];

    // iter() 返回一个迭代器
    let mut iter = numbers.iter();

    // 手动调用 next 方法
    println!("第一个元素: {:?}", iter.next());  // Some(&1)
    println!("第二个元素: {:?}", iter.next());  // Some(&2)
    println!("第三个元素: {:?}", iter.next());  // Some(&3)
    println!("没有更多元素: {:?}", iter.next());  // None

    println!("\n--- 分割线 ---\n");

    // for 循环背后的秘密
    let fruits = vec!["苹果", "香蕉", "橙子"];

    println!("使用 for 循环遍历:");
    for fruit in &fruits {
        println!("  水果: {}", fruit);
    }

    // 等价于手动调用迭代器
    println!("\n手动调用 next():");
    let mut fruit_iter = fruits.iter();
    while let Some(fruit) = fruit_iter.next() {
        println!("  水果: {}", fruit);
    }

    println!("\n--- 分割线 ---\n");

    // 创建自定义迭代器
    struct Counter {
        count: u32,
    }

    impl Counter {
        fn new() -> Counter {
            Counter { count: 0 }
        }
    }

    impl Iterator for Counter {
        type Item = u32;

        fn next(&mut self) -> Option<Self::Item> {
            if self.count < 5 {
                self.count += 1;
                Some(self.count)
            } else {
                None
            }
        }
    }

    let counter = Counter::new();
    for num in counter {
        println!("计数器: {}", num);
    }
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                    Iterator Trait                       │
├─────────────────────────────────────────────────────────┤
│  type Item;        // 迭代器产生的元素类型               │
├─────────────────────────────────────────────────────────┤
│  fn next(&mut self) -> Option<Self::Item>               │
│                                                         │
│  返回值:                                                 │
│    Some(item) -> 还有元素，返回当前元素                  │
│    None      -> 迭代结束，没有更多元素                   │
└─────────────────────────────────────────────────────────┘
```

> Rust 的迭代器是"惰性的"（lazy）——除非你真正"消费"它们，否则它们不会做任何事情。这是一种优化策略：迭代器可以在编译时被优化，在某些情况下甚至可以完全消除迭代器的开销。

### 8.8.2 迭代器的创建

Rust 中有多种方式创建迭代器。不同的方法会产生不同"视角"的迭代器——有的只读，有的可变，有的获取所有权。

#### 8.8.2.1 iter / iter_mut / into_iter

这三个方法是创建迭代器的三种基本方式，它们代表了不同的借用/所有权语义：

```rust
fn main() {
    let data = vec![1, 2, 3, 4, 5];

    // iter(): 创建不可变引用的迭代器
    // 元素类型: &i32
    println!("=== iter() - 不可变引用 ===");
    for num in data.iter() {
        println!("  数值: {} (不可修改)", num);
    }
    // data 仍然完全拥有所有权
    println!("原始 vec 还在: {:?}", data);

    println!("\n--- 分割线 ---\n");

    // iter_mut(): 创建可变引用的迭代器
    // 元素类型: &mut i32
    let mut mutable_data = vec![1, 2, 3, 4, 5];
    println!("=== iter_mut() - 可变引用 ===");

    for num in mutable_data.iter_mut() {
        *num *= 2;  // 修改每个元素
        println!("  修改后的值: {}", num);
    }
    // data 被修改了
    println!("修改后的 vec: {:?}", mutable_data);

    println!("\n--- 分割线 ---\n");

    // into_iter(): 获取所有权的迭代器
    // 元素类型: i32 (所有权被移走)
    let owned_data = vec![10, 20, 30];
    println!("=== into_iter() - 获取所有权 ===");

    for num in owned_data.into_iter() {
        println!("  获取的值: {} (拥有所有权)", num);
    }
    // data 的所有权已经被移走，无法再使用
    // println!("{:?}", owned_data);  // 错误！

    println!("\n--- 分割线 ---\n");

    // 在 for 循环中直接使用这些方法
    let numbers = vec![1, 2, 3];

    // for item in numbers.iter()  等价于  for item in &numbers
    println!("使用 &numbers:");
    for n in &numbers {
        println!("  {}", n);
    }

    // for item in numbers.iter_mut()  等价于  for item in &mut numbers
    let mut nums = vec![1, 2, 3];
    println!("使用 &mut nums:");
    for n in &mut nums {
        *n += 10;
    }
    println!("  修改后: {:?}", nums);

    // for item in numbers.into_iter()  等价于  for item in numbers
    println!("使用 into_iter:");
    let nums2 = vec![1, 2, 3];
    for n in nums2 {
        println!("  {}", n);
    }
    // nums2 已经被移动
}
```

```text
┌─────────────────────────────────────────────────────────┐
│              迭代器创建方式对比                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  data.iter()       ->  Iterator<Item = &i32>           │
│                      只读借用                           │
│                      data 仍然有效                      │
│                                                         │
│  data.iter_mut()   ->  Iterator<Item = &mut i32>       │
│                      可变借用                           │
│                      data 可以被修改                    │
│                                                         │
│  data.into_iter()  ->  Iterator<Item = i32>            │
│                      获取所有权                         │
│                      data 不再有效                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> 记忆小技巧：想象 `iter` 是"用眼睛看"，`iter_mut` 是"用手摸"，`into_iter` 是"一口吞下"。看的时候东西还在，摸了之后可能有变化，吞下去就没了。

#### 8.8.2.2 Range

在 Rust 中，`Range` 是一种创建迭代器的简单方式，特别适用于数字序列。它有两种形式：

- `start..end`：从 `start`（包含）到 `end`（不包含）
- `start..=end`：从 `start`（包含）到 `end`（包含）

```rust
fn main() {
    // 基础 range: start..end (不包含 end)
    println!("=== start..end (不包含 end) ===");
    for i in 0..5 {
        print!("{} ", i);  // 0 1 2 3 4
    }
    println!();

    // 包含 end 的 range: start..=end
    println!("\n=== start..=end (包含 end) ===");
    for i in 0..=5 {
        print!("{} ", i);  // 0 1 2 3 4 5
    }
    println!();

    // 字符 range
    println!("\n=== 字符 range ===");
    for c in 'a'..='e' {
        print!("{} ", c);  // a b c d e
    }
    println!();

    // 使用 range 创建迭代器
    println!("\n=== range 迭代器的各种方法 ===");

    // collect: 收集到 Vec
    let squares: Vec<i32> = (1..=5).map(|x| x * x).collect();
    println!("1-5 的平方: {:?}", squares);  // [1, 4, 9, 16, 25]

    // sum: 求和
    let total: i32 = (1..=100).sum();
    println!("1-100 的和: {}", total);  // 5050

    // product: 求积
    let product: i32 = (1..=5).product();
    println!("1-5 的积: {}", product);  // 120

    // reverse: 反向
    let reversed: Vec<i32> = (1..=5).rev().collect();
    println!("反向: {:?}", reversed);  // [5, 4, 3, 2, 1]

    // step_by: 跳过指定步长
    let evens: Vec<i32> = (0..=10).step_by(2).collect();
    println!("偶数: {:?}", evens);  // [0, 2, 4, 6, 8, 10]

    // float range (需要使用特定方法)
    println!("\n=== Float Range ===");
    use std::iter::successors;

    // 模拟浮点数 range
    let float_range: Vec<f64> = successors(Some(0.0), |&x| {
        Some((x + 0.5).min(2.5))
    }).collect();

    println!("浮点数序列: {:?}", float_range);
    // [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
}
```

### 8.8.3 迭代器适配器：转换类

迭代器适配器（Iterator Adapters）是一些不会立即消费迭代器的方法，它们只是"改造"迭代器，返回一个新的迭代器。转换类适配器是最常用的一类，它们可以将一个迭代器转换成另一个迭代器。

#### 8.8.3.1 map

`map` 是最基础的迭代器适配器，它对每个元素应用一个函数，返回一个新的迭代器。就像一条流水线上的加工站，每个产品经过时都会被贴上一个标签。

```rust
fn main() {
    // 基本的 map 用法
    let numbers = vec![1, 2, 3, 4, 5];

    // 将每个数平方
    let squares: Vec<i32> = numbers.iter().map(|x| x * x).collect();
    println!("平方: {:?}", squares);  // [1, 4, 9, 16, 25]

    // 将字符串转换为大写
    let words = vec!["hello", "rust", "world"];
    let uppercased: Vec<String> = words.iter().map(|s| s.to_uppercase()).collect();
    println!("大写: {:?}", uppercased);  // ["HELLO", "RUST", "WORLD"]

    // map 可以链式调用
    let result: Vec<i32> = (1..=5)
        .map(|x| x * 2)     // 先翻倍: [2, 4, 6, 8, 10]
        .map(|x| x + 10)    // 再加10: [12, 14, 16, 18, 20]
        .map(|x| x % 7)     // 取模7
        .collect();
    println!("链式 map: {:?}", result);  // [5, 0, 2, 4, 6]

    println!("\n--- 分割线 ---\n");

    // map 与闭包组合
    #[derive(Debug)]
    struct Person {
        name: String,
        age: u32,
    }

    let people = vec![
        Person { name: String::from("Alice"), age: 30 },
        Person { name: String::from("Bob"), age: 25 },
        Person { name: String::from("Charlie"), age: 35 },
    ];

    // 提取所有人的名字
    let names: Vec<&str> = people.iter().map(|p| p.name.as_str()).collect();
    println!("所有人的名字: {:?}", names);  // ["Alice", "Bob", "Charlie"]

    // 计算每个人的年龄段
    let age_groups: Vec<&str> = people.iter().map(|p| {
        match p.age {
            0..=17 => "未成年",
            18..=35 => "青年",
            36..=60 => "中年",
            _ => "老年",
        }
    }).collect();
    println!("年龄段: {:?}", age_groups);  // ["青年", "青年", "中年"]

    println!("\n--- 分割线 ---\n");

    // map 不会立即执行（惰性求值）
    let numbers = vec![1, 2, 3];
    let lazy_map = numbers.iter().map(|x| {
        println!("处理: {}", x);  // 这行不会立即执行
        x * 2
    });

    println!("迭代器已创建，但还没有处理任何元素");

    // 只有当消费迭代器时，map 才会真正执行
    println!("开始消费:");
    let result: Vec<i32> = lazy_map.collect();
    println!("结果: {:?}", result);
}
```

> 记住：迭代器是惰性的！`map` 创建一个新的迭代器，但不会执行任何操作，直到你"消费"这个迭代器（使用 `collect`、`for` 循环、`sum` 等方法）。

#### 8.8.3.2 filter

`filter` 就像一个严格的质检员，它检查每个元素，只让符合条件的元素通过。就像面试官筛选简历一样，只有满足条件的才能进入下一轮。

```rust
fn main() {
    // 基本的 filter 用法
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // 过滤出偶数
    let evens: Vec<&i32> = numbers.iter().filter(|x| *x % 2 == 0).collect();
    println!("偶数: {:?}", evens);  // [2, 4, 6, 8, 10]

    // 过滤出大于5的数
    let greater_than_five: Vec<&i32> = numbers.iter().filter(|x| **x > 5).collect();
    println!("大于5的数: {:?}", greater_than_five);  // [6, 7, 8, 9, 10]

    println!("\n--- 分割线 ---\n");

    // map 和 filter 组合
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // 找出偶数，然后平方
    let result: Vec<i32> = numbers
        .iter()
        .filter(|x| *x % 2 == 0)  // 先过滤
        .map(|x| x * x)           // 再映射
        .collect();
    println!("偶数的平方: {:?}", result);  // [4, 16, 36, 64, 100]

    // 过滤字符串
    let words = vec!["apple", "banana", "cherry", "date", "elderberry"];

    // 过滤长度大于5的单词，并转换为大写
    let long_words: Vec<String> = words
        .iter()
        .filter(|w| w.len() > 5)
        .map(|w| w.to_uppercase())
        .collect();
    println!("长单词(大写): {:?}", long_words);  // ["BANANA", "CHERRY", "ELDERBERRY"]

    println!("\n--- 分割线 ---\n");

    // filter 使用更复杂的条件
    #[derive(Debug)]
    struct Product {
        name: String,
        price: f64,
        in_stock: bool,
    }

    let products = vec![
        Product { name: String::from("笔记本"), price: 59.99, in_stock: true },
        Product { name: String::from("手机"), price: 999.99, in_stock: false },
        Product { name: String::from("耳机"), price: 149.99, in_stock: true },
        Product { name: String::from("充电器"), price: 29.99, in_stock: true },
        Product { name: String::from("平板电脑"), price: 399.99, in_stock: false },
    ];

    // 过滤：在库存中且价格小于100的
    let affordable_in_stock: Vec<&Product> = products
        .iter()
        .filter(|p| p.in_stock && p.price < 100.0)
        .collect();

    println!("便宜且有货的产品:");
    for product in &affordable_in_stock {
        println!("  {} - ¥{:.2}", product.name, product.price);
    }
    // 笔记本 - ¥59.99
    // 耳机 - ¥149.99 (这个不会出现在结果中，因为 > 100)
    // 充电器 - ¥29.99

    println!("\n--- 分割线 ---\n");

    // filter_map: 同时过滤和转换
    let strings = vec!["1", "two", "3", "four", "5"];

    // filter_map 会过滤掉 None，只保留 Some
    let numbers: Vec<i32> = strings
        .iter()
        .filter_map(|s| s.parse::<i32>().ok())
        .collect();
    println!("解析出的数字: {:?}", numbers);  // [1, 3, 5]

    // 等价的 map + filter
    let numbers2: Vec<i32> = strings
        .iter()
        .map(|s| s.parse::<i32>().ok())
        .filter(|opt| opt.is_some())
        .map(|opt| opt.unwrap())
        .collect();
    println!("用 map+filter 实现: {:?}", numbers2);  // [1, 3, 5]
}
```

#### 8.8.3.3 take / skip

`take` 和 `skip` 是两个互补的迭代器适配器，它们分别用于"取前几个"和"跳过前几个"元素。

```rust
fn main() {
    // take: 取前 n 个元素
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let first_three: Vec<&i32> = numbers.iter().take(3).collect();
    println!("前3个: {:?}", first_three);  // [1, 2, 3]

    // take 可以用于无限迭代器
    println!("\n=== 无限迭代器 + take ===");
    let evens = (0..).step_by(2);  // 无限偶数序列: 0, 2, 4, 6, ...
    let first_5_evens: Vec<i32> = evens.take(5).collect();
    println!("前5个偶数: {:?}", first_5_evens);  // [0, 2, 4, 6, 8]

    println!("\n--- 分割线 ---\n");

    // skip: 跳过前 n 个元素
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let after_three: Vec<&i32> = numbers.iter().skip(3).collect();
    println!("跳过前3个: {:?}", after_three);  // [4, 5, 6, 7, 8, 9, 10]

    // skip 和 take 组合
    let middle: Vec<&i32> = numbers.iter().skip(2).take(4).collect();
    println!("跳过2个后取4个: {:?}", middle);  // [3, 4, 5, 6]

    println!("\n--- 分割线 ---\n");

    // 实用场景：从文件读取行
    println!("=== 模拟文件行处理 ===");
    let lines = vec![
        "# 这是配置文件",
        "# 注释行",
        "host = localhost",
        "port = 8080",
        "debug = true",
    ];

    // 跳过注释行
    let config_lines: Vec<&str> = lines
        .iter()
        .skip(2)  // 跳过前两行
        .collect();

    println!("配置内容:");
    for line in config_lines {
        println!("  {}", line);
    }

    println!("\n--- 分割线 ---\n");

    // take_while / skip_while: 根据条件取/跳过
    let numbers = vec![1, 2, 3, 4, 5, 1, 2, 3];

    // take_while: 遇到不满足条件的就停止
    let taken: Vec<&i32> = numbers.iter().take_while(|x| **x <= 3).collect();
    println!("take_while(<=3): {:?}", taken);  // [1, 2, 3]

    // skip_while: 跳过满足条件的，直到遇到不满足的
    let skipped: Vec<&i32> = numbers.iter().skip_while(|x| **x <= 3).collect();
    println!("skip_while(<=3): {:?}", skipped);  // [4, 5, 1, 2, 3]

    println!("\n--- 分割线 ---\n");

    // 组合使用
    let numbers = 1..=20;  // 1 到 20

    // 取奇数，但只看前5个
    let result: Vec<i32> = numbers
        .filter(|x| x % 2 == 1)  // 奇数: 1, 3, 5, ..., 19
        .take(5)                  // 只取前5个
        .collect();
    println!("前5个奇数: {:?}", result);  // [1, 3, 5, 7, 9]

    // 跳过前3个奇数，然后取2个
    let result2: Vec<i32> = numbers
        .filter(|x| x % 2 == 1)
        .skip(3)
        .take(2)
        .collect();
    println!("跳过前3个后取2个: {:?}", result2);  // [9, 11]
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                   迭代器适配器对比                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  numbers:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]             │
│                                                         │
│  take(3)    →  [1, 2, 3]                               │
│  skip(3)    →  [4, 5, 6, 7, 8, 9, 10]                  │
│  take(3).skip(2)  →  [1, 2, 3] → [3]                   │
│  skip(3).take(4)  →  [4, 5, 6, 7, 8, 9, 10] → [4, 5, 6, 7] │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.8.4 迭代器适配器：组合类

组合类适配器用于将多个迭代器组合在一起，创建更复杂的数据处理流程。

#### 8.8.4.1 zip

`zip` 将两个迭代器组合成一个，每个元素变成一个元组。当一个迭代器耗尽时，`zip` 就停止。

```rust
fn main() {
    // 基本的 zip 用法
    let numbers = vec![1, 2, 3, 4, 5];
    let words = vec!["一", "二", "三", "四", "五"];

    let zipped: Vec<(&&i32, &&str)> = numbers.iter().zip(words.iter()).collect();
    println!("配对结果: {:?}", zipped);
    // [(1, "一"), (2, "二"), (3, "三"), (4, "四"), (5, "五")]

    println!("\n--- 分割线 ---\n");

    // 长度不同时，zip 会在较短的那个耗尽时停止
    let a = vec![1, 2, 3];
    let b = vec!["A", "B", "C", "D", "E"];

    let zipped: Vec<(&i32, &str)> = a.iter().zip(b.iter()).collect();
    println!("长度不同: {:?}", zipped);
    // [(1, "A"), (2, "B"), (3, "C")]

    println!("\n--- 分割线 ---\n");

    // zip 配合 map 使用
    let prices = vec![10.0, 20.0, 30.0];
    let quantities = vec![2, 3, 1];

    let total_prices: Vec<f64> = prices
        .iter()
        .zip(quantities.iter())
        .map(|(price, qty)| price * qty)
        .collect();
    println!("总价: {:?}", total_prices);  // [20.0, 60.0, 30.0]

    println!("\n--- 分割线 ---\n");

    // 实用场景：合并配置
    println!("=== 合并配置示例 ===");
    let keys = vec!["host", "port", "debug"];
    let values = vec!["localhost", "8080", "true"];

    let config: Vec<String> = keys
        .iter()
        .zip(values.iter())
        .map(|(k, v)| format!("{} = {}", k, v))
        .collect();

    for item in &config {
        println!("  {}", item);
    }

    println!("\n--- 分割线 ---\n");

    // zip 与多个迭代器链式使用
    let names = vec!["Alice", "Bob", "Charlie"];
    let ages = vec![30, 25, 35];
    let cities = vec!["北京", "上海", "深圳"];

    let people: Vec<String> = names
        .iter()
        .zip(ages.iter())
        .zip(cities.iter())
        .map(|((name, age), city)| {
            format!("{}，{}岁，住{}", name, age, city)
        })
        .collect();

    println!("人员信息:");
    for person in &people {
        println!("  {}", person);
    }
    // Alice，30岁，住北京
    // Bob，25岁，住上海
    // Charlie，35岁，住深圳

    println!("\n--- 分割线 ---\n");

    // 使用 unzip 将配对拆分回来
    let paired: Vec<(i32, &str)> = vec![(1, "one"), (2, "two"), (3, "three")];

    let (numbers, words): (Vec<i32>, Vec<&str>) = paired.into_iter().unzip();
    println!("拆分结果 - numbers: {:?}", numbers);  // [1, 2, 3]
    println!("拆分结果 - words: {:?}", words);     // ["one", "two", "three"]
}
```

#### 8.8.4.2 enumerate

`enumerate` 为迭代器的每个元素添加一个索引。就像给元素贴上编号标签一样：0号、1号、2号...

```rust
fn main() {
    // 基本的 enumerate 用法
    let fruits = vec!["苹果", "香蕉", "橙子", "葡萄"];

    for (index, fruit) in fruits.iter().enumerate() {
        println!("{}: {}", index, fruit);
    }
    // 0: 苹果
    // 1: 香蕉
    // 2: 橙子
    // 3: 葡萄

    println!("\n--- 分割线 ---\n");

    // enumerate 返回 (索引, 元素) 的元组
    let result: Vec<(usize, &str)> = fruits.iter().enumerate().collect();
    println!("enumerate 结果: {:?}", result);
    // [(0, "苹果"), (1, "香蕉"), (2, "橙子"), (3, "葡萄")]

    // 从1开始的索引
    println!("\n=== 从1开始计数 ===");
    for (i, fruit) in fruits.iter().enumerate().map(|(i, f)| (i + 1, f)) {
        println!("{}: {}", i, fruit);
    }
    // 1: 苹果
    // 2: 香蕉
    // 3: 橙子
    // 4: 葡萄

    println!("\n--- 分割线 ---\n");

    // 找到第一个满足条件的元素的索引
    let numbers = vec![3, 7, 1, 9, 2, 8];

    // 找到第一个大于5的数的索引
    let index = numbers
        .iter()
        .enumerate()
        .find(|(_, &x)| x > 5)
        .map(|(i, _)| i);

    println!("第一个大于5的数的索引: {:?}", index);  // Some(1) (数字7)

    // position: 返回匹配元素的索引（而非元素本身），类型为 Option<usize>
    let position = numbers.iter().position(|&x| x > 5);
    println!("第一个大于5的数的位置: {:?}", position);  // Some(1)

    println!("\n--- 分割线 ---\n");

    // 实用场景：表格输出
    println!("=== 表格输出 ===");
    let headers = vec!["姓名", "年龄", "城市"];
    let data = vec![
        vec!["张三", "28", "北京"],
        vec!["李四", "35", "上海"],
        vec!["王五", "42", "深圳"],
    ];

    // 输出表头
    for (i, header) in headers.iter().enumerate() {
        if i > 0 { print!(" | "); }
        print!("{}", header);
    }
    println!();
    println!("{}", "-".repeat(30));

    // 输出数据
    for row in &data {
        for (i, cell) in row.iter().enumerate() {
            if i > 0 { print!(" | "); }
            print!("{}", cell);
        }
        println!();
    }

    println!("\n--- 分割线 ---\n");

    // enumerate 与其他适配器组合
    let text = vec!["hello", "world", "rust", "programming"];

    // 找出长度最长的单词的索引
    let longest_index = text
        .iter()
        .enumerate()
        .max_by_key(|(_, word)| word.len())
        .map(|(i, _)| i);

    println!("最长的单词在索引 {}: {:?}", longest_index, text[longest_index.unwrap()]);
    // 最长的单词在索引 3: programming
}
```

#### 8.8.4.3 chain

`chain` 将两个迭代器首尾相连，创建一个更长的迭代器。就像把两条绳子拧在一起变成一条长绳子。

```rust
fn main() {
    // 基本的 chain 用法
    let first = vec![1, 2, 3];
    let second = vec![4, 5, 6];

    let chained: Vec<&i32> = first.iter().chain(second.iter()).collect();
    println!("链接结果: {:?}", chained);  // [1, 2, 3, 4, 5, 6]

    println!("\n--- 分割线 ---\n");

    // chain 可以链接多个迭代器
    let a = vec![1, 2];
    let b = vec![3, 4];
    let c = vec![5, 6];
    let d = vec![7, 8];

    let all: Vec<i32> = a.into_iter()
        .chain(b)
        .chain(c)
        .chain(d)
        .collect();
    println!("链接多个: {:?}", all);  // [1, 2, 3, 4, 5, 6, 7, 8]

    println!("\n--- 分割线 ---\n");

    // 混合不同类型的迭代器（通过 trait 对象）
    let numbers = vec![1, 2, 3];
    let more_numbers = 4..=6;

    let chained: Vec<i32> = numbers
        .into_iter()
        .chain(more_numbers)
        .collect();
    println!("混合类型链接: {:?}", chained);  // [1, 2, 3, 4, 5, 6]

    println!("\n--- 分割线 ---\n");

    // 实用场景：合并多个数据源
    println!("=== 合并学生成绩 ===");
    let midterm = vec![("Alice", 85), ("Bob", 92)];
    let final_exam = vec![("Alice", 88), ("Charlie", 78)];
    let project = vec![("Bob", 95), ("David", 82)];

    #[derive(Debug)]
    struct Score(&'static str, i32);

    let all_scores: Vec<Score> = midterm
        .into_iter()
        .map(|(name, score)| Score(name, score))
        .chain(final_exam.into_iter().map(|(name, score)| Score(name, score)))
        .chain(project.into_iter().map(|(name, score)| Score(name, score)))
        .collect();

    println!("所有成绩:");
    for Score(name, score) in &all_scores {
        println!("  {}: {}", name, score);
    }

    println!("\n--- 分割线 ---\n");

    // chain 与 filter/map 组合
    let evens = vec![2, 4, 6, 8];
    let odds = vec![1, 3, 5, 7, 9];

    // 链接后过滤大于5的
    let result: Vec<i32> = evens
        .into_iter()
        .chain(odds)
        .filter(|&x| x > 5)
        .collect();
    println!("大于5的数字: {:?}", result);  // [6, 8, 7, 9]

    // 或者先平方再链接
    let squares: Vec<i32> = evens.into_iter().map(|x| x * x);
    let cubes: Vec<i32> = odds.into_iter().map(|x| x * x * x);

    let math_results: Vec<i32> = squares.chain(cubes).collect();
    println!("数学运算结果: {:?}", math_results);
    // [4, 16, 36, 64, 1, 27, 125, 343, 729]
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                      chain 示意图                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  iter1: [1, 2, 3]                                       │
│  iter2: [4, 5, 6]                                       │
│                                                         │
│  chain: [1, 2, 3, 4, 5, 6]                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.8.5 迭代器消费者

迭代器消费者是真正"消耗"迭代器的方法。它们会调用迭代器的 `next()`，直到迭代器返回 `None`。消费者是迭代器流水线的终点。

#### 8.8.5.1 collect

`collect` 是最常用的消费者，它将迭代器的所有元素收集到一个集合中。返回类型取决于你指定的类型或上下文。

```rust
fn main() {
    // 收集到 Vec
    let numbers = (1..=5).collect::<Vec<i32>>();
    println!("收集到 Vec: {:?}", numbers);  // [1, 2, 3, 4, 5]

    // 收集到 String（适用于字符迭代器）
    let chars = vec!['R', 'u', 's', 't'];
    let word: String = chars.into_iter().collect();
    println!("收集到 String: {}", word);  // Rust

    // 收集到 HashSet（去重）
    use std::collections::HashSet;
    let numbers = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    let unique: HashSet<i32> = numbers.into_iter().collect();
    println!("收集到 HashSet: {:?}", unique);  // {1, 2, 3, 4}

    // 收集到 HashMap
    use std::collections::HashMap;
    let keys = vec!["a", "b", "c"];
    let values = vec![1, 2, 3];
    let map: HashMap<_, _> = keys.into_iter().zip(values.into_iter()).collect();
    println!("收集到 HashMap: {:?}", map);
    // {"a": 1, "b": 2, "c": 3}

    println!("\n--- 分割线 ---\n");

    // 使用 iter().collect::<Vec<_>>() 来明确类型
    let doubled: Vec<i32> = (1..=5)
        .map(|x| x * 2)
        .collect();
    println!("翻倍: {:?}", doubled);  // [2, 4, 6, 8, 10]

    // FromIterator 实现
    let pairs = vec![(1, "一"), (2, "二"), (3, "三")];
    let map: HashMap<i32, &str> = pairs.into_iter().collect();
    println!("HashMap: {:?}", map);  // {1: "一", 2: "二", 3: "三"}

    println!("\n--- 分割线 ---\n");

    // 实用场景：从输入构建复杂结构
    #[derive(Debug)]
    struct Student {
        name: String,
        grade: char,
    }

    let data = vec![
        ("张三", 95),
        ("李四", 87),
        ("王五", 92),
        ("赵六", 78),
    ];

    // 过滤并收集
    let top_students: Vec<Student> = data
        .into_iter()
        .filter(|(_, score)| *score >= 90)
        .map(|(name, score)| {
            let grade = match score / 10 {
                10 | 9 => 'A',
                8 => 'B',
                7 => 'C',
                6 => 'D',
                _ => 'F',
            };
            Student { name: name.to_string(), grade }
        })
        .collect();

    println!("优秀学生:");
    for student in &top_students {
        println!("  {:?} (Grade: {})", student.name, student.grade);
    }
}
```

#### 8.8.5.2 fold

`fold` 是一个强大的消费者，它将迭代器的所有元素"折叠"成一个值。想象一下把一张纸反复对折——每次折叠都会把所有层压成一个更小的单元。

```rust
fn main() {
    // 基本的 fold 用法
    let numbers = vec![1, 2, 3, 4, 5];

    // 求和: fold(初始值, 闭包)
    let sum = numbers.iter().fold(0, |acc, &x| acc + x);
    println!("求和: {}", sum);  // 15

    // 求积
    let product = numbers.iter().fold(1, |acc, &x| acc * x);
    println!("求积: {}", product);  // 120

    println!("\n--- 分割线 ---\n");

    // 字符串连接
    let words = vec!["Hello", " ", "Rust", " ", "World"];
    let sentence = words.iter().fold(String::new(), |acc, s| acc + s);
    println!("句子: {}", sentence);  // Hello Rust World

    // 更高效的字符串连接
    let words = vec!["Rust", "is", "awesome"];
    let sentence = words.join(" ");
    println!("join: {}", sentence);  // Rust is awesome

    println!("\n--- 分割线 ---\n");

    // 使用 fold 实现其他消费者
    let numbers = vec![1, 2, 3, 4, 5];

    // 实现 sum
    let sum = numbers.iter().fold(0, |acc, &x| acc + x);
    println!("sum: {}", sum);  // 15

    // 实现 product
    let product = numbers.iter().fold(1, |acc, &x| acc * x);
    println!("product: {}", product);  // 120

    // 实现 find（找第一个偶数）
    let first_even = numbers.iter().fold(None, |acc, &x| {
        if acc.is_some() { acc } else { Some(x) }
    }).filter(|&x| x % 2 == 0);
    println!("第一个偶数: {:?}", first_even);  // Some(2)

    println!("\n--- 分割线 ---\n");

    // fold 与复杂逻辑
    #[derive(Debug)]
    struct BankAccount {
        name: String,
        balance: f64,
    }

    let accounts = vec![
        BankAccount { name: String::from("张三"), balance: 1000.0 },
        BankAccount { name: String::from("李四"), balance: 2500.0 },
        BankAccount { name: String::from("王五"), balance: 500.0 },
        BankAccount { name: String::from("赵六"), balance: 10000.0 },
    ];

    // 计算总余额
    let total_balance = accounts.iter().fold(0.0, |acc, accnt| acc + accnt.balance);
    println!("总资产: ¥{:.2}", total_balance);  // ¥14000.00

    // 找出最高余额
    let max_balance = accounts.iter().fold(f64::MIN, |acc, accnt| {
        acc.max(accnt.balance)
    });
    println!("最高余额: ¥{:.2}", max_balance);  // ¥10000.00

    // 统计有多少账户余额超过1000
    let rich_count = accounts.iter().fold(0, |acc, accnt| {
        if accnt.balance > 1000.0 { acc + 1 } else { acc }
    });
    println!("高净值账户数: {}", rich_count);  // 2

    println!("\n--- 分割线 ---\n");

    // 使用 fold 实现 map 的等价功能
    let numbers = vec![1, 2, 3, 4, 5];

    // 用 fold 实现 map
    let doubled = numbers.iter().fold(Vec::new(), |mut acc, &x| {
        acc.push(x * 2);
        acc
    });
    println!("用 fold 实现 map: {:?}", doubled);  // [2, 4, 6, 8, 10]

    // 用 fold 实现 filter
    let evens = numbers.iter().fold(Vec::new(), |mut acc, &x| {
        if x % 2 == 0 { acc.push(x); }
        acc
    });
    println!("用 fold 实现 filter: {:?}", evens);  // [2, 4]
}
```

> `fold` 的第一个参数叫做"初始累加器"（initial accumulator），也叫"种子值"（seed）。这个值会被闭包的第一个参数接收。对于求和，通常用 0 作为初始值；对于求积，用 1。

#### 8.8.5.3 find / position

`find` 和 `position` 是两个用于在迭代器中查找元素的消费者。它们返回第一个匹配条件的元素，但返回的形式不同。

```rust
fn main() {
    // find: 返回第一个满足条件的元素的引用
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let found = numbers.iter().find(|&&x| x > 5);
    println!("第一个大于5的数: {:?}", found);  // Some(&6)

    let not_found = numbers.iter().find(|&&x| x > 100);
    println!("大于100的数: {:?}", not_found);  // None

    println!("\n--- 分割线 ---\n");

    // position: 返回第一个满足条件的元素的索引
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let pos = numbers.iter().position(|&x| x > 5);
    println!("第一个大于5的数的索引: {:?}", pos);  // Some(5) (0-indexed)

    let not_found = numbers.iter().position(|&x| x > 100);
    println!("大于100的数的索引: {:?}", not_found);  // None

    // 如果有多个匹配，position 只返回第一个
    let fruits = vec!["苹果", "香蕉", "樱桃", "香蕉", "葡萄"];
    let first_banana = fruits.iter().position(|&f| f == "香蕉");
    println!("第一个'香蕉'的位置: {:?}", first_banana);  // Some(1)

    // 找最后一个匹配（需要反向迭代）
    let last_banana = fruits.iter().rev().position(|&f| f == "香蕉");
    println!("最后一个'香蕉'的位置(从后数): {:?}", last_banana);  // Some(1)
    // 转换为从前的索引
    if let Some(from_end) = last_banana {
        let from_start = fruits.len() - 1 - from_end;
        println!("最后一个'香蕉'的实际索引: {}", from_start);  // 3
    }

    println!("\n--- 分割线 ---\n");

    // 使用 find 实现复杂查找
    #[derive(Debug)]
    struct User {
        id: u32,
        name: String,
        email: String,
        active: bool,
    }

    let users = vec![
        User { id: 1, name: String::from("张三"), email: String::from("zhang@example.com"), active: true },
        User { id: 2, name: String::from("李四"), email: String::from("li@example.com"), active: false },
        User { id: 3, name: String::from("王五"), email: String::from("wang@example.com"), active: true },
    ];

    // 找一个活跃用户
    let active_user = users.iter().find(|u| u.active);
    println!("第一个活跃用户: {:?}", active_user.map(|u| &u.name));  // Some("张三")

    // 通过 ID 查找
    let user_by_id = users.iter().find(|u| u.id == 2);
    println!("ID为2的用户: {:?}", user_by_id.map(|u| &u.name));  // Some("李四")

    // 通过邮箱查找
    let user_by_email = users.iter().find(|u| u.email == "wang@example.com");
    println!("通过邮箱查找: {:?}", user_by_email.map(|u| &u.name));  // Some("王五")

    println!("\n--- 分割线 ---\n");

    // any / all: 返回布尔值的查找方法
    let numbers = vec![1, 2, 3, 4, 5];

    // any: 是否有任何元素满足条件
    let has_even = numbers.iter().any(|&x| x % 2 == 0);
    println!("是否有偶数: {}", has_even);  // true

    // all: 是否所有元素都满足条件
    let all_positive = numbers.iter().all(|&x| x > 0);
    println!("是否全是正数: {}", all_positive);  // true

    let all_less_than_10 = numbers.iter().all(|&x| x < 10);
    println!("是否都小于10: {}", all_less_than_10);  // true

    println!("\n--- 分割线 ---\n");

    // count: 计算满足条件的元素数量
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let even_count = numbers.iter().filter(|&&x| x % 2 == 0).count();
    println!("偶数个数: {}", even_count);  // 5

    let greater_than_5_count = numbers.iter().take_while(|&&x| x > 5).count();
    println!("大于5的个数(使用take_while): {}", greater_than_5_count);  // 0
}
```

### 8.8.6 FromIterator / IntoIterator

这两个 trait 是 Rust 集合与迭代器之间的桥梁。它们定义了"从哪里来"和"到哪里去"的转换规则。

#### 8.8.6.1 FromIterator

`FromIterator` trait 描述了如何从迭代器构建一个集合。它是 `collect` 方法的基础。

```rust
fn main() {
    use std::collections::{HashMap, HashSet, BTreeMap, VecDeque};

    // 从迭代器收集到 Vec
    let numbers: Vec<i32> = (1..=5).collect();
    println!("收集到 Vec: {:?}", numbers);  // [1, 2, 3, 4, 5]

    // 从迭代器收集到 HashSet（自动去重）
    let numbers = vec![1, 2, 2, 3, 3, 3, 4, 4, 4, 4];
    let unique: HashSet<i32> = numbers.into_iter().collect();
    println!("收集到 HashSet: {:?}", unique);  // {1, 2, 3, 4}

    // 从键值对收集到 HashMap
    let pairs = vec![("a", 1), ("b", 2), ("c", 3)];
    let map: HashMap<&str, i32> = pairs.into_iter().collect();
    println!("收集到 HashMap: {:?}", map);  // {"a": 1, "b": 2, "c": 3}

    println!("\n--- 分割线 ---\n");

    // 从迭代器收集到 String
    let chars = vec!['H', 'e', 'l', 'l', 'o'];
    let word: String = chars.into_iter().collect();
    println!("字符收集到 String: {}", word);  // Hello

    // 从字符串收集（按字符）
    let text = "Hello Rust";
    let chars: Vec<char> = text.chars().collect();
    println!("字符串拆分为字符: {:?}", chars);  // ['H', 'e', 'l', 'l', 'o', ' ', 'R', 'u', 's', 't']

    // 从字符串收集（按单词）
    let text = "Hello Rust World";
    let words: Vec<&str> = text.split_whitespace().collect();
    println!("字符串拆分为单词: {:?}", words);  // ["Hello", "Rust", "World"]

    println!("\n--- 分割线 ---\n");

    // 收集到 VecDeque（双端队列）
    let numbers: VecDeque<i32> = (1..=5).collect();
    println!("收集到 VecDeque: {:?}", numbers);

    // 收集到 BTreeMap（有序映射）
    let pairs = vec![(3, "C"), (1, "A"), (2, "B")];
    let sorted_map: BTreeMap<i32, &str> = pairs.into_iter().collect();
    println!("收集到 BTreeMap (按键排序): {:?}", sorted_map);
    // {1: "A", 2: "B", 3: "C"}

    println!("\n--- 分割线 ---\n");

    // 自定义类型实现 FromIterator
    #[derive(Debug)]
    struct ShoppingList(Vec<String>);

    impl FromIterator<String> for ShoppingList {
        fn from_iter<I: IntoIterator<Item = String>>(iter: I) -> Self {
            ShoppingList(iter.into_iter().collect())
        }
    }

    let items = vec![
        String::from("牛奶"),
        String::from("面包"),
        String::from("鸡蛋"),
    ];

    let list: ShoppingList = items.into_iter().collect();
    println!("购物清单: {:?}", list);
    // ShoppingList(["牛奶", "面包", "鸡蛋"])
}
```

#### 8.8.6.2 IntoIterator

`IntoIterator` trait 允许类型被转换为迭代器。它是 `for` 循环语法糖背后的机制。

```rust
fn main() {
    // Vec 实现了 IntoIterator
    let numbers = vec![1, 2, 3, 4, 5];

    // 直接在 Vec 上调用 into_iter()
    for n in numbers.into_iter() {
        println!("数字: {}", n);  // 消费每个元素
    }
    // numbers 已经被移动，无法再使用

    println!("\n--- 分割线 ---\n");

    // 数组的 IntoIterator
    let arr = [1, 2, 3, 4, 5];
    let sum: i32 = arr.iter().sum();  // 使用引用迭代
    println!("数组元素和: {}", sum);  // 15

    // 数组也可以移动迭代
    let arr = [1, 2, 3];
    let moved: Vec<i32> = arr.into_iter().collect();
    println!("数组移动到 Vec: {:?}", moved);  // [1, 2, 3]

    println!("\n--- 分割线 ---\n");

    // 字符串的 IntoIterator（按字符）
    let text = String::from("Rust");
    let chars: Vec<char> = text.chars().collect();
    println!("字符串按字符: {:?}", chars);  // ['R', 'u', 's', 't']

    // 字符串的 IntoIterator（按字节）
    let text = String::from("Rust");
    let bytes: Vec<u8> = text.into_bytes();
    println!("字符串按字节: {:?}", bytes);  // [82, 117, 115, 116]

    println!("\n--- 分割线 ---\n");

    // HashMap 的 IntoIterator
    use std::collections::HashMap;
    let mut scores = HashMap::new();
    scores.insert(String::from("Alice"), 100);
    scores.insert(String::from("Bob"), 95);

    // 迭代 (key, value) 元组
    for (name, score) in scores {
        println!("{} 的分数: {}", name, score);
    }

    println!("\n--- 分割线 ---\n");

    // Range 的 IntoIterator
    let range = 1..=5;
    let collected: Vec<i32> = range.into_iter().collect();
    println!("Range into_iter: {:?}", collected);  // [1, 2, 3, 4, 5]

    // 字符 Range
    let char_range = 'a'..='c';
    let chars: Vec<char> = char_range.into_iter().collect();
    println!("字符 Range: {:?}", chars);  // ['a', 'b', 'c']

    println!("\n--- 分割线 ---\n");

    // 实现自定义类型的 IntoIterator
    #[derive(Debug)]
    struct Countdown(u32);

    impl IntoIterator for Countdown {
        type Item = u32;
        type IntoIter = std::vec::IntoIter<Self::Item>;

        fn into_iter(self) -> Self::IntoIter {
            (1..=self.0).collect::<Vec<_>>().into_iter()
        }
    }

    let countdown = Countdown(5);
    for n in countdown {
        print!("{}... ", n);
    }
    println!("发射！");
}
```

### 8.8.7 自定义迭代器

Rust 允许我们为任何类型实现 `Iterator` trait，从而创建自定义的迭代器。这使得我们可以让自己的类型也拥有函数式编程的能力。

#### 8.8.7.1 为自定义类型实现 Iterator

实现 `Iterator` trait 只需要实现 `next` 方法。这给了我们创建任意类型迭代器的灵活性。

```rust
fn main() {
    // 创建一个产生斐波那契数列的迭代器
    struct Fibonacci {
        current: u64,
        next: u64,
    }

    impl Fibonacci {
        fn new() -> Fibonacci {
            Fibonacci {
                current: 0,
                next: 1,
            }
        }
    }

    impl Iterator for Fibonacci {
        type Item = u64;

        fn next(&mut self) -> Option<Self::Item> {
            let current = self.current;
            self.current = self.next;
            self.next = current + self.next;
            Some(current)
        }
    }

    println!("=== 斐波那契数列 ===");
    let fib = Fibonacci::new();
    let first_10: Vec<u64> = fib.take(10).collect();
    println!("前10个斐波那契数: {:?}", first_10);
    // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    println!("\n--- 分割线 ---\n");

    // 创建一个产生等差数列的迭代器
    struct ArithmeticSequence {
        current: i32,
        step: i32,
        limit: i32,
    }

    impl ArithmeticSequence {
        fn new(start: i32, step: i32, limit: i32) -> Self {
            ArithmeticSequence {
                current: start,
                step,
                limit,
            }
        }
    }

    impl Iterator for ArithmeticSequence {
        type Item = i32;

        fn next(&mut self) -> Option<Self::Item> {
            if self.current > self.limit {
                None
            } else {
                let result = self.current;
                self.current += self.step;
                Some(result)
            }
        }
    }

    println!("=== 等差数列 (1, 4, 7, 10, 13, ...) ===");
    let seq = ArithmeticSequence::new(1, 3, 20);
    println!("等差数列: {:?}", seq.collect::<Vec<_>>());  // [1, 4, 7, 10, 13, 16, 19]

    println!("\n--- 分割线 ---\n");

    // 创建一个迭代器的迭代器（二维迭代）
    struct Grid<T> {
        data: Vec<Vec<T>>,
        row: usize,
        col: usize,
    }

    impl<T> Grid<T> {
        fn new(data: Vec<Vec<T>>) -> Self {
            Grid { data, row: 0, col: 0 }
        }
    }

    impl<T: Clone> Iterator for Grid<T> {
        type Item = T;

        fn next(&mut self) -> Option<Self::Item> {
            // 如果当前行有效
            if self.row < self.data.len() {
                let current_row = &self.data[self.row];

                if self.col < current_row.len() {
                    let element = current_row[self.col].clone();
                    self.col += 1;
                    return Some(element);
                }

                // 移动到下一行
                self.row += 1;
                self.col = 0;
                self.next()
            } else {
                None
            }
        }
    }

    println!("=== 二维网格迭代 ===");
    let grid = Grid::new(vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ]);

    let flattened: Vec<i32> = grid.collect();
    println!("展平后的网格: {:?}", flattened);  // [1, 2, 3, 4, 5, 6, 7, 8, 9]

    println!("\n--- 分割线 ---\n");

    // 实现一个无限质数生成器（使用筛选法）
    struct PrimeGenerator {
        primes: Vec<u64>,
        current: u64,
    }

    impl PrimeGenerator {
        fn new() -> PrimeGenerator {
            PrimeGenerator {
                primes: Vec::new(),
                current: 2,
            }
        }
    }

    impl Iterator for PrimeGenerator {
        type Item = u64;

        fn next(&mut self) -> Option<Self::Item> {
            let mut candidate = self.current;

            loop {
                // 检查 candidate 是否被已知质数整除
                let is_prime = self.primes.iter().all(|&p| candidate % p != 0);

                if is_prime {
                    self.primes.push(candidate);
                    self.current = candidate + 1;
                    return Some(candidate);
                }

                candidate += 1;
            }
        }
    }

    println!("=== 前20个质数 ===");
    let primes = PrimeGenerator::new().take(20).collect::<Vec<_>>();
    println!("质数列表: {:?}", primes);
    // [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
}
```

### 8.8.8 迭代器性能

Rust 的迭代器其中一个最重要的特性就是它能够实现"零成本抽象"。这意味着使用迭代器通常不会引入任何运行时开销——它和手写的循环一样快。

#### 8.8.8.1 零成本抽象

Rust 的迭代器是零成本抽象的典范。在编译时，迭代器的调用会被高度优化，最终生成的机器码与手写的 `for` 循环几乎完全一样。

```rust
fn main() {
    println!("=== 迭代器 vs 手写循环 ===");

    // 方法1：使用迭代器
    fn sum_with_iter(numbers: &[i32]) -> i32 {
        numbers.iter().sum()
    }

    // 方法2：手写循环
    fn sum_with_loop(numbers: &[i32]) -> i32 {
        let mut sum = 0;
        for n in numbers {
            sum += *n;
        }
        sum
    }

    let data: Vec<i32> = (1..=1000).collect();

    // 两者结果相同
    println!("迭代器求和: {}", sum_with_iter(&data));   // 500500
    println!("循环求和: {}", sum_with_loop(&data));     // 500500

    println!("\n--- 分割线 ---\n");

    // 更复杂的例子
    fn process_with_iter(numbers: &[i32]) -> i32 {
        numbers
            .iter()
            .filter(|&&x| x % 2 == 0)  // 只取偶数
            .map(|x| x * x)            // 平方
            .sum()                     // 求和
    }

    fn process_with_loop(numbers: &[i32]) -> i32 {
        let mut sum = 0;
        for n in numbers {
            if *n % 2 == 0 {
                sum += *n * *n;
            }
        }
        sum
    }

    println!("迭代器处理: {}", process_with_iter(&data));   // 167167000
    println!("循环处理: {}", process_with_loop(&data));     // 167167000

    println!("\n--- 分割线 ---\n");

    // Rust 编译器会优化掉迭代器的间接调用
    // 在 release 模式下 (-O)，迭代器链会被完全展开
    println!("零成本抽象意味着:");
    println!("1. 没有运行时分配");
    println!("2. 没有虚函数调用开销");
    println!("3. 编译器可以进行激进优化");
    println!("4. 最终机器码与手写循环几乎相同");

    println!("\n--- 分割线 ---\n");

    // 迭代器的惰性求值意味着不会有多余的计算
    let numbers: Vec<i32> = (1..=100).collect();

    // 这行代码本身不会做任何计算
    let lazy_chain = numbers
        .iter()
        .map(|x| {
            println!("map: {}", x);  // 这行不会执行
            x * 2
        })
        .filter(|x| {
            println!("filter: {}", x);  // 这行也不会执行
            x % 3 == 0
        });

    println!("迭代器已创建，但还没有执行任何操作");

    // 只有当我们消费迭代器时，计算才会发生
    println!("\n开始消费:");
    let result: Vec<&i32> = lazy_chain.collect();
    println!("\n结果: {:?}", result);
}
```

> 在 Rust 中使用迭代器不仅仅是"函数式编程的优雅写法"，更是一种高效的编程范式。Rust 的迭代器实现在编译时会进行大量的优化，包括内联、循环展开、向量化等。这意味着你可以同时享受函数式编程的简洁和命令式编程的性能。

## 8.9 函数式错误处理

到目前为止，我们看到的都是"Happy Path"——一切都顺利进行的场景。但现实世界总是充满意外：文件可能不存在、网络可能断开、用户可能输入了无效数据。函数式编程提供了一种优雅的方式来处理这些"意外"，而不需要大量的 `if err != nil` 或 `try-catch` 语句。

Rust 的 `Option` 和 `Result` 类型配合函数式方法，提供了一种强大的错误处理范式。

### 8.9.1 Option 上的函数式方法

`Option` 类型代表一个值可能存在（`Some`）或不存在（`None`）。`Option` 提供了一系列方法，让我们可以用函数式的方式来处理这种"可能存在"的情况。

#### 8.9.1.1 map / and_then

`map` 和 `and_then` 是 `Option` 上最常用的两个函数式方法。它们让我们可以在不进行显式 `match` 的情况下转换和组合 `Option` 值。

```rust
fn main() {
    println!("=== Option 的 map 和 and_then ===");

    // map: 转换 Some 中的值
    let some_number: Option<i32> = Some(5);
    let doubled = some_number.map(|x| x * 2);
    println!("Some(5) * 2 = {:?}", doubled);  // Some(10)

    let none_number: Option<i32> = None;
    let doubled = none_number.map(|x| x * 2);
    println!("None * 2 = {:?}", doubled);  // None

    println!("\n--- 分割线 ---\n");

    // and_then: 链式调用可能返回 None 的操作
    fn parse_number(s: &str) -> Option<i32> {
        s.parse::<i32>().ok()
    }

    let result = Some("42")
        .and_then(parse_number)
        .map(|x| x * 2);
    println!("Some(\"42\") -> parse -> *2 = {:?}", result);  // Some(84)

    let result = Some("hello")
        .and_then(parse_number)
        .map(|x| x * 2);
    println!("Some(\"hello\") -> parse -> *2 = {:?}", result);  // None

    let result: Option<i32> = None
        .and_then(parse_number)
        .map(|x| x * 2);
    println!("None -> parse -> *2 = {:?}", result);  // None

    println!("\n--- 分割线 ---\n");

    // 实际场景：解析配置
    #[derive(Debug)]
    struct Config {
        host: String,
        port: u16,
    }

    fn parse_config(raw: Option<&str>, default_port: u16) -> Option<Config> {
        raw.and_then(|s| s.parse::<std::net::SocketAddr>().ok())
            .map(|(host, port)| Config { host, port })
            .or(Some(Config {
                host: String::from("localhost"),
                port: default_port,
            }))
    }

    println!("解析配置:");
    println!("  Some(\"127.0.0.1:8080\") = {:?}", parse_config(Some("127.0.0.1:8080"), 80));
    println!("  None = {:?}", parse_config(None, 8080));

    println!("\n--- 分割线 ---\n");

    // 其他常用的 Option 方法
    let value = Some(42);

    // unwrap_or: 提供默认值
    println!("unwrap_or: {}", value.unwrap_or(0));  // 42
    println!("None.unwrap_or(0) = {}", (None as Option<i32>).unwrap_or(0));  // 0

    // unwrap_or_else: 使用闭包提供默认值
    println!("unwrap_or_else: {}", value.unwrap_or_else(|| {
        println!("计算默认值...");
        100
    }));  // 42（不打印，因为有值）

    // or: 提供备选的 Option
    println!("or: {:?}", value.or(Some(999)));  // Some(42)
    println!("or: {:?}", (None as Option<i32>).or(Some(999)));  // Some(999)

    // filter: 保留满足条件的 Some
    println!("filter: {:?}", value.filter(|x| *x > 100));  // None
    println!("filter: {:?}", value.filter(|x| *x > 10));   // Some(42)

    println!("\n--- 分割线 ---\n");

    // 链式操作示例
    #[derive(Debug)]
    struct User {
        id: u32,
        name: String,
    }

    fn find_user(id: u32) -> Option<User> {
        match id {
            1 => Some(User { id: 1, name: String::from("Alice") }),
            2 => Some(User { id: 2, name: String::from("Bob") }),
            _ => None,
        }
    }

    fn get_email(user: &User) -> Option<String> {
        match user.id {
            1 => Some(String::from("alice@example.com")),
            _ => None,
        }
    }

    // 链式调用
    let email = find_user(1)
        .and_then(get_email)
        .map(|e| e.to_uppercase());

    println!("用户1的邮箱(大写): {:?}", email);  // Some("ALICE@EXAMPLE.COM")

    let email = find_user(2)
        .and_then(get_email)
        .map(|e| e.to_uppercase());

    println!("用户2的邮箱: {:?}", email);  // None（用户2没有邮箱）

    let email = find_user(999)
        .and_then(get_email)
        .map(|e| e.to_uppercase());

    println!("不存在的用户的邮箱: {:?}", email);  // None
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                    Option 方法一览                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  map        → 转换 Some 的值，None 保持 None             │
│  and_then   → 链式可能失败的操作                        │
│  filter     → 只保留满足条件的 Some                      │
│  unwrap_or  → 提供默认值                                │
│  or         → 提供备选的 Option                         │
│  is_some    → 检查是否有值                              │
│  is_none    → 检查是否无值                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.9.2 Result 上的函数式方法

`Result` 类型代表可能失败的操作。与 `Option` 不同，`Result` 可以携带错误信息。`Result` 也有类似 `Option` 的函数式方法。

#### 8.9.2.1 map / map_err

`Result` 的 `map` 和 `map_err` 允许我们转换成功值或错误值，而不进行显式的 `match`。

```rust
fn main() {
    println!("=== Result 的 map 和 map_err ===");

    // 基础用法
    let ok_value: Result<i32, &str> = Ok(5);
    let doubled = ok_value.map(|x| x * 2);
    println!("Ok(5) * 2 = {:?}", doubled);  // Ok(10)

    let err_value: Result<i32, &str> = Err("出错了");
    let doubled = err_value.map(|x| x * 2);
    println!("Err(\"出错了\") * 2 = {:?}", doubled);  // Err("出错了")

    println!("\n--- 分割线 ---\n");

    // map_err: 只转换错误值
    #[derive(Debug)]
    enum MyError {
        NotFound,
        InvalidInput,
        IoError(String),
    }

    fn parse_positive(s: &str) -> Result<i32, MyError> {
        match s.parse::<i32>() {
            Ok(n) if n > 0 => Ok(n),
            Ok(_) => Err(MyError::InvalidInput),
            Err(_) => Err(MyError::InvalidInput),
        }
    }

    // 成功情况
    let result = parse_positive("42").map(|n| n * 2);
    println!("parse(\"42\") * 2 = {:?}", result);  // Ok(84)

    // 错误情况
    let result = parse_positive("-5").map(|n| n * 2);
    println!("parse(\"-5\") * 2 = {:?}", result);  // Err(InvalidInput)

    println!("\n--- 分割线 ---\n");

    // map_err: 转换错误类型
    use std::num::ParseIntError;

    fn convert_error(e: ParseIntError) -> String {
        format!("解析错误: {}", e)
    }

    let ok: Result<i32, ParseIntError> = Ok(42);
    let mapped_ok = ok.map_err(convert_error);
    println!("Ok(42).map_err = {:?}", mapped_ok);  // Ok(42)

    let err: Result<i32, ParseIntError> = "abc".parse();
    let mapped_err = err.map_err(convert_error);
    println!("Err(\"abc\").map_err = {:?}", mapped_err);
    // Err("解析错误: invalid digit...")

    println!("\n--- 分割线 ---\n");

    // and_then: 链式可能失败的操作
    fn reciprocal(n: i32) -> Result<f64, &'static str> {
        if n == 0 {
            Err("不能除以零")
        } else {
            Ok(1.0 / n as f64)
        }
    }

    let result = Ok(2).and_then(reciprocal).and_then(reciprocal);
    println!("1/(1/2) = {:?}", result);  // Ok(2.0)

    let result = Ok(0).and_then(reciprocal);
    println!("1/0 = {:?}", result);  // Err("不能除以零")

    println!("\n--- 分割线 ---\n");

    // 实际场景：链式文件操作
    println!("=== 文件处理示例 ===");

    fn read_file(path: &str) -> Result<String, std::io::Error> {
        std::fs::read_to_string(path)
    }

    fn parse_number(s: &str) -> Result<i32, std::num::ParseIntError> {
        s.trim().parse()
    }

    fn process_file(path: &str) -> Result<i32, Box<dyn std::error::Error>> {
        let content = read_file(path)?;  // ? 操作符
        let number = parse_number(&content)?;
        Ok(number * 2)
    }

    // 注意：下面的代码需要实际的文件才能运行
    // 这里演示类型和用法
    println!("使用 ? 操作符的链式调用:");
    println!("  1. read_file() 返回 Result<String, Error>");
    println!("  2. ? 操作符会传播错误");
    println!("  3. parse_number() 返回 Result<i32, ParseIntError>");
    println!("  4. 最终返回 Result<i32, Box<dyn Error>>");

    println!("\n--- 分割线 ---\n");

    // Result 的其他常用方法
    let ok: Result<i32, &str> = Ok(42);

    // unwrap_or: 提供默认值
    println!("unwrap_or: {}", ok.unwrap_or(0));  // 42
    println!("Err.unwrap_or(0) = {}", Err::<i32, &str>("error").unwrap_or(0));  // 0

    // unwrap_or_else: 使用闭包提供默认值
    println!("unwrap_or_else: {}", ok.unwrap_or_else(|_| {
        println!("计算默认值...");  // 不会执行
        100
    }));  // 42

    // or: 提供备选的 Result
    println!("or: {:?}", ok.or(Ok(999)));  // Ok(42)
    println!("or: {:?}", Err::<i32, _>("e").or(Ok(999)));  // Ok(999)

    // is_ok / is_err
    println!("is_ok: {}", ok.is_ok());  // true
    println!("is_err: {}", ok.is_err());  // false
}
```

### 8.9.3 组合子（Combinator）

组合子（Combinator）是将多个函数组合在一起工作的函数式编程技术。在 Rust 中，我们经常使用组合子来链式调用 `Option` 和 `Result` 上的方法。

#### 8.9.3.1 链式调用示例

组合子的强大之处在于它们可以链式调用，创造出优雅而强大的数据处理管道。

```rust
fn main() {
    println!("=== 组合子链式调用示例 ===");

    println!("\n--- 示例1: 用户配置解析 ---");
    #[derive(Debug)]
    struct ServerConfig {
        host: String,
        port: u16,
        ssl: bool,
    }

    #[derive(Debug)]
    struct ParseError(String);

    fn parse_host(s: &str) -> Result<String, ParseError> {
        if s.is_empty() {
            Err(ParseError("主机名不能为空".to_string()))
        } else {
            Ok(s.to_string())
        }
    }

    fn parse_port(s: &str) -> Result<u16, ParseError> {
        s.parse::<u16>()
            .map_err(|_| ParseError("端口必须是数字".to_string()))
    }

    fn parse_ssl(s: &str) -> Result<bool, ParseError> {
        match s.to_lowercase().as_str() {
            "true" | "1" | "yes" => Ok(true),
            "false" | "0" | "no" => Ok(false),
            _ => Err(ParseError("SSL必须是 true/false".to_string())),
        }
    }

    // 模拟配置数据
    let config_data = vec![
        ("host", "localhost"),
        ("port", "8080"),
        ("ssl", "true"),
    ];

    let config: Result<ServerConfig, _> = config_data
        .iter()
        .map(|(key, value)| {
            let parsed = match *key {
                "host" => parse_host(value).map(|v| ("host", v)),
                "port" => parse_port(value).map(|v| ("port", v)),
                "ssl" => parse_ssl(value).map(|v| ("ssl", v)),
                _ => Err(ParseError(format!("未知配置项: {}", key))),
            };
            (key, parsed)
        })
        .collect::<Result<Vec<_>, _>>()
        .and_then(|items| {
            let mut host = None;
            let mut port = None;
            let mut ssl = None;

            for (key, value) in items {
                match key {
                    "host" => host = Some(value),
                    "port" => port = Some(value),
                    "ssl" => ssl = Some(value),
                    _ => {}
                }
            }

            match (host, port, ssl) {
                (Some(h), Some(p), Some(s)) => Ok(ServerConfig { host: h, port: p, ssl: s }),
                _ => Err(ParseError("缺少必需的配置项".to_string())),
            }
        });

    println!("解析结果: {:?}", config);

    println!("\n--- 示例2: 成绩计算 ---");
    #[derive(Debug)]
    struct Student {
        name: String,
        scores: Vec<Option<i32>>,
    }

    fn average_score(scores: &[Option<i32>]) -> Option<f64> {
        let valid_scores: Vec<i32> = scores.iter().filter_map(|&s| s).collect();
        if valid_scores.is_empty() {
            None
        } else {
            Some(valid_scores.iter().sum::<i32>() as f64 / valid_scores.len() as f64)
        }
    }

    let student = Student {
        name: String::from("小明"),
        scores: vec![Some(85), Some(92), None, Some(78), Some(88)],
    };

    let avg = average_score(&student.scores);
    println!("{} 的平均分: {:?}", student.name, avg);  // Some(85.75)

    println!("\n--- 示例3: 嵌套 Option ---");
    #[derive(Debug)]
    struct Address {
        street: Option<String>,
        city: Option<String>,
    }

    #[derive(Debug)]
    struct Person {
        name: String,
        address: Option<Address>,
    }

    let people = vec![
        Person {
            name: String::from("张三"),
            address: Some(Address {
                street: Some(String::from("中山路123号")),
                city: Some(String::from("北京")),
            }),
        },
        Person {
            name: String::from("李四"),
            address: Some(Address {
                street: None,
                city: Some(String::from("上海")),
            }),
        },
        Person {
            name: String::from("王五"),
            address: None,
        },
    ];

    for person in &people {
        // 获取城市的嵌套 Option
        let city = person
            .address
            .as_ref()
            .and_then(|addr| addr.city.as_ref())
            .map(|s| s.as_str());

        println!("{} 住在: {:?}", person.name, city);
    }
    // 张三 住在: Some("北京")
    // 李四 住在: Some("上海")
    // 王五 住在: None

    println!("\n--- 示例4: 计算管道 ---");
    // 模拟一个数据处理管道
    fn validate_positive(n: i32) -> Option<i32> {
        if n > 0 { Some(n) } else { None }
    }

    fn square(n: i32) -> i32 {
        n * n
    }

    fn to_string(n: i32) -> String {
        format!("数字是: {}", n)
    }

    let result = Some(5)
        .and_then(validate_positive)  // Some(5)
        .map(square)                    // Some(25)
        .map(to_string);                // Some("数字是: 25")

    println!("管道结果: {:?}", result);  // Some("数字是: 25")

    // 如果输入是 -5
    let result = Some(-5)
        .and_then(validate_positive)  // None（验证失败）
        .map(square)                    // None
        .map(to_string);                // None

    println!("无效输入的结果: {:?}", result);  // None

    println!("\n--- 示例5: 错误累积 ---");
    #[derive(Debug)]
    struct ValidationErrors(Vec<String>);

    impl ValidationErrors {
        fn new() -> Self {
            ValidationErrors(Vec::new())
        }

        fn add(&mut self, msg: &str) {
            self.0.push(msg.to_string());
        }
    }

    fn validate_age(age: i32) -> Result<i32, String> {
        if age >= 0 && age <= 150 {
            Ok(age)
        } else {
            Err("年龄必须在0-150之间".to_string())
        }
    }

    fn validate_name(name: &str) -> Result<String, String> {
        if name.len() >= 2 && name.len() <= 50 {
            Ok(name.to_string())
        } else {
            Err("名字长度必须在2-50之间".to_string())
        }
    }

    fn validate_email(email: &str) -> Result<String, String> {
        if email.contains('@') && email.contains('.') {
            Ok(email.to_string())
        } else {
            Err("邮箱格式不正确".to_string())
        }
    }

    // 使用 fold 累积所有错误
    fn validate_user(name: &str, age: i32, email: &str) -> Result<(String, i32, String), Vec<String>> {
        let results = vec![
            validate_name(name).map(|n| (1, n)),
            validate_age(age).map(|a| (2, a)),
            validate_email(email).map(|e| (3, e)),
        ];

        let (names, errors): (Vec<_>, Vec<_>) = results
            .into_iter()
            .partition(Result::is_ok);

        if errors.is_empty() {
            Ok((
                names[0].as_ref().unwrap().1.clone(),
                names[1].as_ref().unwrap().1,
                names[2].as_ref().unwrap().1.clone(),
            ))
        } else {
            Err(errors.into_iter().filter_map(Result::err).collect())
        }
    }

    // 测试各种情况
    println!("\n验证有效用户:");
    match validate_user("张三", 25, "zhang@example.com") {
        Ok((name, age, email)) => println!("  成功: {} ({}岁), {}", name, age, email),
        Err(errors) => println!("  错误: {:?}", errors),
    }

    println!("\n验证无效用户:");
    match validate_user("张", 200, "invalid-email") {
        Ok((name, age, email)) => println!("  成功: {} ({}岁), {}", name, age, email),
        Err(errors) => {
            println!("  验证失败:");
            for error in &errors {
                println!("    - {}", error);
            }
        }
    }
}
```

```text
┌─────────────────────────────────────────────────────────┐
│                 函数式错误处理流程图                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  传统方式:                                               │
│    fn process() {                                        │
│        if let Ok(x) = step1() {                         │
│            if let Ok(y) = step2(x) {                    │
│                if let Ok(z) = step3(y) {                │
│                    return Ok(z);                         │
│                } else { return Err(...); }              │
│            } else { return Err(...); }                  │
│        } else { return Err(...); }                      │
│    }                                                    │
│                                                         │
│  函数式方式:                                             │
│    fn process() -> Result<T, E> {                       │
│        step1()                                          │
│            .and_then(step2)                            │
│            .and_then(step3)                            │
│    }                                                    │
│                                                         │
│  优势: 简洁、可组合、可读性强                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 本章小结

在这一章中，我们深入探索了 Rust 的函数式编程特性。让我来回顾一下我们学到的主要内容：

### 闭包（Closure）

闭包是 Rust 中一种强大的匿名函数形式，它可以捕获定义时环境中的变量。闭包的语法简洁而富有表现力，使用 `|params| body` 的形式。我们学习了三种闭包捕获方式：按引用（`&T`）、按可变引用（`&mut T`）和按值（`move`）。Rust 的编译器会根据闭包的使用方式自动推断最佳的捕获方式。`Fn`、`FnMut` 和 `FnOnce` 三个 trait 定义了闭包的调用约定，它们之间有严格的继承关系——所有的 `Fn` 都是 `FnMut` 和 `FnOnce`，但反过来不成立。

### 迭代器（Iterator）

迭代器是 Rust 函数式编程的核心。`Iterator` trait 定义了迭代器的基本行为：每次调用 `next()` 返回一个元素。Rust 提供了三种创建迭代器的方式：`iter()`（不可变引用）、`iter_mut()`（可变引用）和 `into_iter()`（获取所有权）。迭代器适配器如 `map`、`filter`、`take`、`skip`、`zip`、`enumerate` 和 `chain` 允许我们以函数式的方式转换和组合迭代器。迭代器消费者如 `collect`、`fold`、`find` 和 `position` 最终消费迭代器产生结果。最重要的是，迭代器是"零成本抽象"——使用迭代器的代码与手写的 `for` 循环具有相同的性能。

### 函数式错误处理

Rust 的 `Option` 和 `Result` 类型配合函数式方法，提供了一种优雅的错误处理方式。`map` 和 `and_then` 方法允许我们转换和链式调用可能失败的操作，而不需要大量的 `if-else` 或 `match` 语句。组合子模式使得我们可以构建复杂的数据处理管道，同时保持代码的简洁性和可读性。

### 核心设计思想

Rust 的函数式编程特性不仅仅是语法糖，它们体现了 Rust 的核心设计哲学：

1. **零成本抽象**：高级抽象在运行时没有开销
2. **编译时安全**：通过类型系统和借用检查器在编译时捕获错误
3. **组合优于继承**：通过 trait 和闭包组合出灵活的行为
4. **明确的所有权语义**：每个值都有明确的生命周期和所有权

掌握这些函数式编程技巧，将帮助你写出更加优雅、高效和安全的 Rust 代码。无论是处理集合、操作数据流，还是管理错误，Rust 的函数式特性都能让你得心应手。

> 恭喜你完成了函数式编程章节的学习！现在你已经拥有了 Rust 函数式编程的"三件套"。闭包给了你定义行为的能力，迭代器给了你处理序列的能力，函数式错误处理给了你处理异常的能力。好好练习，你很快就能写出既简洁又高效的 Rust 代码了！
