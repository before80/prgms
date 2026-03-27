+++
title = "第 5 章 Trait"
weight = 50
date = "2026-03-27T17:24:46+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter 05 Trait（特征）

> 想象一下，你是一家公司的 HR 经理。每天你要面对各种职位描述（Job Description）：会计要会做账、程序员要会写代码、设计师要会画图。但问题是，你不能因为会计会做账就让他去 debug 代码——虽然听起来像是老板会干的事。
>
> 在 Rust 的世界里，**Trait 就是这个"职位描述"**。它告诉编译器："嘿，拥有这个 trait 的类型，必须能完成这些任务！"无论是打印自己、相比较大小、还是克隆一份，你都可以用 trait 来约束它们。
>
> 换句话说，trait 就是 Rust 版的"接口"（Interface），只不过它比 Java 的接口更优雅，比 Go 的 interface 更安全，比你老板的"全能型人才"要求更现实。 trait 这个词本身的意思是"特征"、"品质"——恰好说明它描述的是类型的"性格特点"：这个类型能做什么？它像谁？它有什么拿手绝活？

## 5.1 Trait 基础

好，现在让我们正式认识一下 trait这位新朋友。它是 Rust 类型系统的灵魂，是抽象行为的基石，是让你从"写代码的"升级为"设计系统架构的"敲门砖。

### 5.1.1 Trait 定义

Trait 定义是整个 trait 系统的起点。你可以把它想象成一份"能力清单"——在这份清单上，你列出某种类型应该具备的所有能力（方法）。至于这个能力怎么实现，那是后面 impl 的时候才需要操心的事。这种"先定义接口，后实现细节"的思想，正是面向接口编程的精髓。

#### 5.1.1.1 trait 声明语法（带详细解释）

声明一个 trait 就像发布一份职位招聘启事，你需要列出候选人的必备技能。

```rust
// 定义一个名为 Greeting 的 trait
// 翻译过来就是："所有自称会打招呼的类型，必须实现 say_hello 方法"
trait Greeting {
    // 方法签名：返回 String，没有参数
    // 这是抽象的，不提供默认实现
    fn say_hello(&self) -> String;

    // 还可以有更多方法签名...
    fn say_goodbye(&self) -> String;
}
```

> **语法详解：**
>
> - `trait` 关键字：告诉编译器"这是一个 trait 定义"
> - `Greeting`：trait 的名字，遵循 Rust 的命名规范（PascalCase）
> - 大括号 `{}` 内部：列出所有方法签名（method signature）
> - `fn say_hello(&self) -> String`：方法签名，类似于函数的声明，但不需要 `impl` 块中那样写函数体
> - `&self`：表示这个方法会借用 self，类似于其他语言中的 `this`
> - 注意 trait 内部的方法签名以分号 `;` 结尾，而不是大括号 `{}`，因为我们只声明，不定义

```rust
// 再来一个更贴近生活的例子：Printable trait
// 任何想要被"打印"的东西，都得实现这个 trait
trait Printable {
    // 要求实现者提供一个 format 方法
    // 返回一个 String，这个 String 应该是格式化后的表示
    fn format(&self) -> String;
}
```

> **为什么要用 trait 而不是直接写方法？**
>
> 因为 trait 定义了"能力接口"，而具体类型可以以不同方式实现这个能力。比如 `Person` 类型可能返回 "我是张三，今年18岁"，而 `Dog` 类型可能返回 "汪汪汪，我是旺财"。同一个 trait，不同的实现，这正是多态（polymorphism）的魅力所在。

#### 5.1.1.2 trait 方法签名（带详细解释）

方法签名是 trait 定义中最核心的部分。它告诉编译器："实现这个 trait 的类型，必须提供这样一个方法"。方法签名包括方法名、参数列表、返回值类型，但不包含实现。

```rust
// 让我们定义一个更复杂的 trait，包含各种"签名风格"
trait Animal {
    // 基础版：无参数，返回 String
    fn name(&self) -> String;

    // 进阶版：带参数，返回 bool
    // 这个方法检查某种食物是否喜欢
    fn likes_food(&self, food: &str) -> bool;

    // 高阶版：可变引用 self，可以修改内部状态
    fn rename(&mut self, new_name: String);

    // 终极版：不消耗 self，但也不返回任何东西
    fn make_sound(&self);

    // 独占版：消耗 self，这个 animal 之后就不能用了
    fn into_string(self) -> String where Self: Sized;
    // where Self: Sized 是默认约束，表示 self 有确定大小
    // 大部分时候你可以省略这个约束
}
```

> **方法签名语法小课堂：**
>
> | 签名形式 | 含义 | 类比 |
> |---------|------|------|
> | `fn foo(&self)` | 只读借用 | 你可以看看这只动物叫什么名字，但不能给它改名字 |
> | `fn foo(&mut self)` | 可变借用 | 你可以给它改名字，但它的"动物身份"还是不变的 |
> | `fn foo(self)` | 消耗所有权 | 你要把它变成字符串形式，原来的动物对象就没了 |
> | `fn foo() -> T` | 静态方法/关联函数 | 类似于构造函数，比如 `String::from("xxx")` |
>
> 记住这个口诀：**&self 看看，&mut self 改改，self 吃掉别浪费**。

### 5.1.2 Trait 实现

定义 trait 只是画饼，**实现 trait 才是真的把饼做出来**。这一步你要告诉 Rust："这个具体的类型，我要用这种方式来实现刚才定义的 trait"。就像招聘启事发出去后，终于有人来面试了，现在你要决定怎么让他展示能力。

#### 5.1.2.1 impl Trait for Type 语法

这是 Rust 中实现 trait 的标准语法，读作"为 Type 实现 Trait"。

```rust
// 先定义一个 trait
trait Cookable {
    fn cook(&self) -> String;
}

// 再定义一个类型
struct Egg {
    // 鸡蛋的属性：新鲜程度，0-100
    freshness: u8,
}

// 关键语法：为 Egg 实现 Cookable trait
impl Cookable for Egg {
    // 实现具体的方法
    fn cook(&self) -> String {
        if self.freshness > 50 {
            format!("煎个荷包蛋，鲜度{}%，完美！", self.freshness)
        } else {
            format!("这蛋不太新鲜了({}%),还是做熟透了吧...", self.freshness)
        }
    }
}

fn main() {
    let my_egg = Egg { freshness: 85 };
    println!("{}", my_egg.cook());
    // 打印结果: 煎个荷包蛋，鲜度85%，完美！
}
```

> **语法分解：**
>
> - `impl`：关键词，表示"我要开始实现了"
> - `Cookable`：要实现的 trait 名字
> - `for Egg`：为哪个类型实现，这里是 for Egg，翻译成"针对 Egg"
> - 大括号 `{}` 内部：具体的方法实现，也就是填上 trait 定义中那些"空白"
>
> 整个结构读起来就是：**"impl Cookable for Egg" = "为 Egg 这个人颁发 Cookable（会做饭）证书"**

再来看一个更贴近生活的例子：

```rust
// 定义一个 Describable trait
trait Describable {
    fn describe(&self) -> String;
}

// 定义几种类型
struct Water {
    temperature: f32,  // 水温，单位摄氏度
}

struct Coffee {
    strength: u8,      // 浓郁度，1-10
    caffeine_mg: u32,  // 咖啡因含量，毫克
}

// 为 Water 实现 Describable
impl Describable for Water {
    fn describe(&self) -> String {
        if self.temperature < 0.0 {
            "冰块警告！".to_string()
        } else if self.temperature < 30.0 {
            "凉白开，养生首选"
        } else if self.temperature < 60.0 {
            "温水，暖胃"
        } else {
            "热水，烫嘴预警"
        }.to_string()
    }
}

// 为 Coffee 实现 Describable
impl Describable for Coffee {
    fn describe(&self) -> String {
        format!(
            "咖啡：浓郁度{}级，咖啡因{}毫克，{}",
            self.strength,
            self.caffeine_mg,
            if self.caffeine_mg > 200 { "今晚别想睡了" } else { "还能接受" }
        )
    }
}

fn main() {
    let water = Water { temperature: 45.0 };
    let coffee = Coffee { strength: 7, caffeine_mg: 250 };

    println!("水: {}", water.describe());
    println!("咖啡: {}", coffee.describe());
    // 打印结果:
    // 水: 温水，暖胃
    // 咖啡: 咖啡因250毫克，今晚别想睡了
}
```

#### 5.1.2.2 trait 作为约束（静态分发）

当你在泛型函数中使用 trait 约束时，Rust 会在编译时为每种具体类型生成专门的代码。这种方式叫做**静态分发（Static Dispatch）**——因为具体调用哪个实现，在编译阶段就决定了，没有运行时的查找开销。

```rust
// T: Greeting 是一个 trait 约束
// 意思是："T 必须实现了 Greeting 这个 trait"
fn print_greeting<T: Greeting>(item: &T) {
    // 这里编译器知道 T 一定实现了 say_hello
    // 所以可以直接调用
    println!("{}", item.say_hello());
}

// 也可以用 where 语法，代码更清晰
fn print_greeting_clean<T>(item: &T)
where
    T: Greeting,
{
    println!("{}", item.say_hello());
}

// 多个约束也是可以的
fn print_multiple<T>(item: &T)
where
    T: Greeting + Printable,
    // T 必须同时实现 Greeting 和 Printable
{
    println!("{}", item.format());
    println!("{}", item.say_hello());
}

// 实现一下 Greeting trait 先
struct Robot {
    name: String,
}

impl Greeting for Robot {
    fn say_hello(&self) -> String {
        format!("01011001，你好！我是机器人{}", self.name)
    }
    fn say_goodbye(&self) -> String {
        format!("再见，人类！{}下线了", self.name)
    }
}

fn main() {
    let robot = Robot { name: "R2-D2".to_string() };
    print_greeting(&robot);
    // 打印结果: 01011001，你好！我是机器人R2-D2
}
```

> **静态分发 vs 动态分发 的区别：**
>
> 静态分发就像是你去餐厅点菜，服务员说"等一下，厨师专门为你做这道菜"。菜是现做的、新鲜的、专属于你的，但需要更多时间准备（编译时间长）。
>
> 动态分发则像是你去吃自助餐，你拿了一个"通用餐盘"，厨房做好了各种菜，你 runtime 的时候才决定往盘子里放哪道菜。准备快（编译快），但吃的时候要自己选（运行时查找）。
>
> Rust 的泛型约束默认是静态分发，dyn Trait 是动态分发。

### 5.1.3 默认方法实现

有时候，你希望 trait 中的某些方法有一个"开箱即用"的默认实现。这样实现这个 trait 的类型如果不满意默认实现，可以自己 override；如果觉得默认实现挺不错，直接用就行。这就像公司提供的"标准工作流程"——新人可以选择遵守，也可以提出改进方案。

#### 5.1.3.1 trait 中的默认方法实现

在 trait 定义中，你可以直接给出方法的具体实现，实现者可以"拿来就用"或者"稍作修改"。

```rust
// 定义一个带有默认实现的 trait
trait Discountable {
    // 这个方法没有默认实现，实现者必须自己写
    fn original_price(&self) -> f64;

    // 这个方法有默认实现！
    fn discounted_price(&self, discount: f64) -> f64 {
        // 默认逻辑：原价的 discount 折
        // 也就是说 discount=0.8 表示打八折
        self.original_price() * discount
    }

    // 再来一个默认方法：格式化输出价格
    fn price_tag(&self) -> String {
        format!("原价: {:.2}, 现价: {:.2}",
            self.original_price(),
            self.discounted_price(1.0))
    }
}

struct Product {
    name: String,
    price: f64,
}

impl Discountable for Product {
    // 必须实现 original_price
    fn original_price(&self) -> f64 {
        self.price
    }
    // discounted_price 和 price_tag 都使用默认实现
}

fn main() {
    let phone = Product {
        name: "iPhone 99".to_string(),
        price: 9999.0,
    };

    println!("{}", phone.price_tag());
    println!("七折后: {:.2}", phone.discounted_price(0.7));
    // 打印结果:
    // 原价: 9999.00, 现价: 9999.00
    // 七折后: 6999.30
}
```

> **默认方法的实现原理：**
>
> 实际上，当你在 trait 中提供默认方法实现时，Rust 会在编译时把这个默认实现"复制"到每个使用默认实现的实现中。这不是真正的继承，而是代码生成。所以不存在什么"父类方法被子类继承"的问题，trait 之间是"组合"关系而非"继承"关系。

#### 5.1.3.2 重写默认方法

如果你觉得默认实现太 low，完全可以自己写一个更炫酷的版本。这就像老板给的模板你嫌土，自己用 PPT 做了一个更专业的。

```rust
trait Greeting {
    fn say(&self) -> String;
}

// 默认实现
trait FormalGreeting {
    fn say(&self) -> String {
        "你好，阁下".to_string()  // 默认版：正式但有点古板
    }
}

// VIPS顾客
struct VIPCustomer {
    name: String,
    level: u8,  // VIP等级，1-5
}

impl FormalGreeting for VIPCustomer {
    // 重写！VIP 要享受特殊待遇
    fn say(&self) -> String {
        match self.level {
            5 => format!("尊贵的钻石会员{}，欢迎回家！", self.name),
            4 => format!("亲爱的金卡会员{}，好久不见！", self.name),
            _ => format!("{}先生/女士，这边请~", self.name),
        }
    }
}

struct RegularCustomer {
    name: String,
}

impl FormalGreeting for RegularCustomer {
    // 普通顾客就用默认实现吧
}

fn main() {
    let vip = VIPCustomer { name: "马爸爸".to_string(), level: 5 };
    let regular = RegularCustomer { name: "张三".to_string() };

    println!("VIP: {}", vip.say());
    println!("普通人: {}", regular.say());
    // 打印结果:
    // VIP: 尊贵的钻石会员马爸爸，欢迎回家！
    // 普通人: 你好，阁下
}
```

#### 5.1.3.3 调用默认方法

有时候在你的自定义实现中，你可能想调用默认方法，然后再做一些额外的事情。这种情况下，你可以在 impl 块中使用 `<Type as Trait>::method()` 语法来显式调用默认实现。

```rust
trait Printable {
    fn format(&self) -> String {
        // 默认实现就是简单粗暴的 Debug 格式
        format!("{:?}", self)
    }

    fn print_it(&self) {
        // 这个默认方法会调用 format()
        println!("{}", self.format());
    }
}

struct Book {
    title: String,
    pages: u32,
}

impl Printable for Book {
    // 我们重写 format，但想保留 print_it 的默认行为
    fn format(&self) -> String {
        format!("《{}》共{}页", self.title, self.pages)
    }
}

fn main() {
    let book = Book {
        title: "Rust 权威指南".to_string(),
        pages: 666,
    };

    book.print_it();  // 这里的 print_it 还是用的默认实现
    // 打印结果: 《Rust 权威指南》共666页
}
```

> **注意：** 上面 `print_it` 调用的 `self.format()` 是动态分发的，会正确地调用到 `Book` 的实现。

### 5.1.4 Trait 继承

在 Rust 中，trait 可以"继承"其他 trait。这意味着如果你想让类型实现子 trait，它必须同时实现所有父 trait。这就像是你发布了一个"高级厨师"的职位描述，但其中写着"必须先有厨师资格证"——想要高级职位？先把基础要求满足了。

#### 5.1.4.1 trait Sub: Base 语法

```rust
// 父 trait：基础能力
trait CanRead {
    fn read(&self) -> String;
}

// 子 trait：继承 CanRead，还要加一个写的能力
trait CanWrite: CanRead {
    fn write(&self, content: &str) -> String;
}

// 如果你想实现 CanWrite，你必须先实现 CanRead
struct Writer {
    name: String,
    articles_written: u32,
}

impl CanRead for Writer {
    fn read(&self) -> String {
        format!("{}正在阅读参考资料...", self.name)
    }
}

impl CanWrite for Writer {
    fn write(&self, content: &str) -> String {
        format!("{}正在撰写文章，内容: {}", self.name, content)
    }
}

fn main() {
    let writer = Writer {
        name: "小明".to_string(),
        articles_written: 10,
    };

    println!("{}", writer.read());
    println!("{}", writer.write("Rust真有趣！"));
    // 打印结果:
    // 小明正在阅读参考资料...
    // 小明正在撰写文章，内容: Rust真有趣！
}
```

> **语法解释：**
>
> `trait CanWrite: CanRead` 中的 `:` 意思是"继承"或"扩展"。可以理解为：
> - "CanWrite 是 CanRead 的子集"
> - "要成为 CanWrite，必须先满足 CanRead 的要求"
> - "CanWrite 在 CanRead 基础上加了自己的要求"

#### 5.1.4.2 子 trait 的完整约束

当你在泛型中使用继承了其他 trait 的 trait 时，你需要列出完整的约束。

```rust
// 继续上面的例子，加入更多层级
trait CanSpeak: CanRead {
    fn speak(&self) -> String;
}

// 顶级 trait：什么都会
trait CanTeach: CanWrite + CanSpeak {
    fn teach(&self) -> String;
}

// 普通讲师
struct Lecturer {
    name: String,
    field: String,
}

impl CanRead for Lecturer {
    fn read(&self) -> String {
        format!("{}在研究{}", self.name, self.field)
    }
}

impl CanSpeak for Lecturer {
    fn speak(&self) -> String {
        format!("{}开始讲课了！", self.name)
    }
}

impl CanWrite for Lecturer {
    fn write(&self, content: &str) -> String {
        format!("{}写了: {}", self.name, content)
    }
}

impl CanTeach for Lecturer {
    fn teach(&self) -> String {
        format!("{}开设了一门课: {}", self.name, self.field)
    }
}

// 使用时，约束要完整
fn teach_someone<T: CanTeach>(teacher: &T) {
    println!("{}", teacher.read());
    println!("{}", teacher.speak());
    println!("{}", teacher.write("教案"));
    println!("{}", teacher.teach());
}

fn main() {
    let lecturer = Lecturer {
        name: "王教授".to_string(),
        field: "Rust系统编程".to_string(),
    };
    teach_someone(&lecturer);
    // 打印结果:
    // 王教授在研究Rust系统编程
    // 王教授开始讲课了！
    // 王教授写了: 教案
    // 王教授开设了一门课: Rust系统编程
}
```

### 5.1.5 孤儿规则（Orphan Rule）

这是 Rust 中一个非常重要的概念，也是让很多人挠头的"奇怪规则"。为什么要有这个规则？它到底在限制什么？让我们一探究竟。

#### 5.1.5.1 孤儿规则定义

**孤儿规则**：如果你想为某个类型实现某个 trait，那么要么这个 trait 定义在当前 crate 中，要么这个类型定义在当前 crate 中，**二者至少要有其一**。

```text
翻译成人话就是：
"你不能给别人的孩子（类型）穿别人的衣服（trait）"
"除非这个衣服是你自己做的，或者这个孩子是你亲生的"
```

> **为什么要有孤儿规则？**
>
> 想象一下，如果允许为任何类型实现任何 trait，会发生什么？
>
> 我可以给 `String` 实现 `Display`，返回 "Hacked!";
> 你也可以给 `String` 实现 `Display`，返回 "Hello";
>
> 然后在某段代码里，调用 `println!("{}", some_string)`，到底该调用哪个？编译器都不知道，Rust 引入了孤儿规则来避免这种"实现冲突"的噩梦。

```rust
// 假设我们要给标准库的 Vec<String> 实现一个自定义 trait
// 因为 Vec 不是我们定义的，所以这会违反孤儿规则

// 错误示例（请不要尝试编译）：
// impl MyTrait for Vec<String> { ... }
// 错误: 只能为当前 crate 中定义的类型实现外部 crate 的 trait

// 但是我们可以这样：定义一个自己的类型，然后给它实现标准库的 trait
mod my_module {
    pub struct MyVec<T>(pub Vec<T>);  // 包装一下，就是"新类型"

    // 现在我们可以为 MyVec<T> 实现标准库的 trait 了
    impl<T: std::fmt::Debug> std::fmt::Debug for MyVec<T> {
        fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
            write!(f, "MyVec({:?})", self.0)
        }
    }
}
```

#### 5.1.5.2 新类型模式（Newtype Pattern）

为了绕过孤儿规则，Rust 社区发明了一种经典技巧：**新类型模式（Newtype Pattern）**。就是用元组结构体包装一下别人的类型，这样就创造出了一个"名义上是你自己的类型"，然后你就可以光明正大地给它实现各种 trait 了。

```rust
// 标准库的 String
use std::fmt;

// 创建一个新类型包装 String
struct Username(String);

// 为我们的新类型实现 Display
impl fmt::Display for Username {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[用户: {}]", self.0)
    }
}

// 还可以实现更多 trait...
impl Clone for Username {
    fn clone(&self) -> Self {
        Username(self.0.clone())
    }
}

fn main() {
    let name = Username("Rustacean".to_string());
    println!("{}", name);
    println!("克隆一个: {}", name.clone());
    // 打印结果:
    // [用户: Rustacean]
    // 克隆一个: [用户: Rustacean]
}
```

> **新类型模式的精髓：**
>
> 它的原理很简单：元组结构体 `struct Wrapper(T)` 在名义上是一个全新的类型，和原来的 `T` 是不同的。虽然它内部就是 `T`，但在 Rust 的类型系统眼里，它是"Wrapper"不是"T"。
>
> 这就像你把一封信装进信封，信的内容没变，但信封让它变成了"邮件"这种新东西，可以贴邮票、盖邮戳——这些都是"邮件"能做的事，"裸信"做不了。

#### 5.1.5.3 原则：两个实现至少有一个是本地的

这条规则确保了实现的唯一性。如果 `trait` 和 `type` 都来自外部，那么就有可能和其他人冲突。Rust 强制你"要么你定义能力，要么你定义类型，至少占一样"。

```rust
// 场景1：为自己的类型实现标准库的 trait ✓
trait Serializable {
    fn serialize(&self) -> String;
}

struct MyConfig {
    name: String,
    version: u32,
}

impl Serializable for MyConfig {
    fn serialize(&self) -> String {
        format!("{{\"name\": \"{}\", \"version\": {}}}", self.name, self.version)
    }
}

// 场景2：为标准库类型实现自己的 trait ✓
trait Printable {
    fn print(&self);
}

impl Printable for Vec<i32> {
    fn print(&self) {
        println!("Vec<i32>: {:?}", self);
    }
}

// 场景3：为标准库类型实现标准库的 trait ✗（不允许！）
// impl Display for Vec<i32> { ... }  // 错误！

// 场景4：为外部 crate 的类型实现外部 crate 的 trait ✗（不允许！）
// 假设 weixin 和 pay 都是外部 crate
// impl pay::Payment for weixin::WeChatPay { ... }  // 错误！

fn main() {
    let config = MyConfig {
        name: "MyApp".to_string(),
        version: 1,
    };
    println!("{}", config.serialize());
    // 打印结果: {"name": "MyApp", "version": 1}

    let numbers = vec![1, 2, 3];
    numbers.print();
    // 打印结果: Vec<i32>: [1, 2, 3]
}
```

## 5.2 标准库常用 Trait

如果说 trait 是 Rust 的灵魂，那么标准库提供的这些 trait 就是 Rust 的"标配技能包"。它们让类型拥有了各种开箱即用的能力：可以打印、可以比较、可以克隆、可以迭代......就像 RPG 游戏里角色自带的被动技能。

掌握这些常用 trait，你就能更好地理解标准库的设计逻辑，也能写出更"符合人体工程学"的代码。

### 5.2.1 Debug Trait

Debug trait 是 Rust 标准库中最常用的 trait 之一，它让你的类型能够被 debug 打印。在开发和调试过程中，能够 print 出来看看内部状态是非常重要的技能。

#### 5.2.1.1 Debug trait 定义

Debug trait 定义在 `std::fmt` 模块中，它只有一个方法 `fmt`，签名如下：

```rust
pub trait Debug {
    fn fmt(&self, f: &mut Formatter) -> Result<(), Error>;
}
```

这个 trait 的作用是：定义如何把一个类型的实例格式化成可读的字符串（用于调试）。和 Display 不同，Debug 的输出格式是给程序员看的，可能包含字段名、括号等结构信息。

#### 5.2.1.2 {:?} 格式化占位符

`{:?}` 是 Debug 格式化的占位符。当你使用 `println!("{:?}", value)` 或 `dbg!` 宏时，就是在调用 Debug trait 的实现。

```rust
fn main() {
    let number = 42;
    let text = "hello";
    let array = [1, 2, 3];

    // {:?} 是 Debug 格式
    println!("数字: {:?}", number);
    println!("文本: {:?}", text);
    println!("数组: {:?}", array);

    // {:#?} 是美化输出的 Debug 格式
    println!("数组(美化): {:#?}", array);
    // 打印结果:
    // 数字: 42
    // 文本: "hello"
    // 数组: [1, 2, 3]
    // 数组(美化): [
    //     1,
    //     2,
    //     3,
    // ]
}
```

#### 5.2.1.3 #[derive(Debug)] 派生

Rust 提供了一个神奇的派生宏 `#[derive(Debug)]`，它可以自动为你的类型生成 Debug trait 的实现。对于简单的 struct 和 enum，这比手写 fmt 方法省事多了。

```rust
#[derive(Debug)]  // 一行顶一百行
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
enum Direction {
    North,
    South,
    East,
    West,
}

#[derive(Debug)]
struct Rectangle {
    top_left: Point,
    bottom_right: Point,
}

fn main() {
    let p = Point { x: 10, y: 20 };
    let d = Direction::North;
    let rect = Rectangle {
        top_left: Point { x: 0, y: 10 },
        bottom_right: Point { x: 10, y: 0 },
    };

    println!("点: {:?}", p);
    println!("方向: {:?}", d);
    println!("矩形: {:?}", rect);

    // 打印结果:
    // 点: Point { x: 10, y: 20 }
    // 方向: North
    // 矩形: Rectangle { top_left: Point { x: 0, y: 10 }, bottom_right: Point { x: 10, y: 0 } }
}
```

> **derive 宏的神奇之处：**
>
> `#[derive(Debug)]` 实际上是一个过程宏，它会在编译时自动生成 `impl Debug for Point { ... }` 的代码。对于普通 struct，它会生成类似这样的代码：
>
> ```rust
> impl Debug for Point {
>     fn fmt(&self, f: &mut Formatter) -> Result<(), Error> {
>         f.debug_struct("Point")
>             .field("x", &self.x)
>             .field("y", &self.y)
>             .finish()
>     }
> }
> ```
>
> 想象一下如果手写这个要多久？`derive` 就是 Rust 给你发的福利。

#### 5.2.1.4 Debug::fmt 方法签名详解

如果你不想用 derive，也可以自己实现 Debug trait。方法签名的参数 `f: &mut Formatter` 是一个格式化器，你通过调用它的各种方法来构建输出。

```rust
use std::fmt;

// 手动实现 Debug
struct Person {
    name: String,
    age: u8,
    height: f64,
}

impl fmt::Debug for Person {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // debug_struct 创建一个结构体风格的调试输出
        // "Person" 是结构体名称
        f.debug_struct("Person")
            .field("name", &self.name)           // 字段名和值
            .field("age", &self.age)
            .field("height", &format!("{:.1}", self.height))  // 格式化一下
            .finish()                               // 结束，必须调用
    }
}

fn main() {
    let person = Person {
        name: "张三".to_string(),
        age: 28,
        height: 175.5,
    };

    println!("{:?}", person);
    // 打印结果: Person { name: "张三", age: 28, height: "175.5" }
}
```

> **Formatter 提供的辅助方法：**
>
> | 方法 | 效果 | 类比 |
> |------|------|------|
> | `debug_struct` | 结构体风格 | `Point { x: 1, y: 2 }` |
> | `debug_tuple` | 元组风格 | `Tuple(...)` |
> | `debug_list` | 列表风格 | `[1, 2, 3]` |
> | `debug_set` | 集合风格 | `{1, 2, 3}` |
> | `debug_map` | 映射风格 | `{"a": 1, "b": 2}` |
> | `debug_enum` | 枚举风格 | 根据 variant 分发 |

#### 5.2.1.5 {:?} 与 {:#?}（单行 vs 多行格式化）

`{:?}` 输出单行格式，适合紧凑展示；`{:#?}` 输出多行格式（pretty print），适合查看复杂的嵌套结构。

```rust
#[derive(Debug)]
struct Company {
    name: String,
    employees: Vec<Employee>,
}

#[derive(Debug)]
struct Employee {
    name: String,
    salary: u32,
}

fn main() {
    let company = Company {
        name: "宇宙科技".to_string(),
        employees: vec![
            Employee { name: "张三".to_string(), salary: 30000 },
            Employee { name: "李四".to_string(), salary: 35000 },
        ],
    };

    println!("单行格式:");
    println!("{:?}", company);

    println!("\n多行格式:");
    println!("{:#?}", company);

    // 打印结果:
    // 单行格式:
    // Company { name: "宇宙科技", employees: [Employee { name: "张三", salary: 30000 }, Employee { name: "李四", salary: 35000 }] }
    //
    // 多行格式:
    // Company {
    //     name: "宇宙科技",
    //     employees: [
    //         Employee {
    //             name: "张三",
    //             salary: 30000,
    //         },
    //         Employee {
    //             name: "李四",
    //             salary: 35000,
    //         },
    //     ],
    // }
}
```

#### 5.2.1.6 无法派生的场景

有些类型不能直接 derive Debug，通常是因为它们包含了一些"特殊"的字段。

```rust
// 场景1：包含没有实现 Debug 的类型
struct CannotDerive {
    name: String,           // String 实现了 Debug，可以
    // data: Rc<RefCell<...>>,  // 如果 Rc 没实现 Debug，就不能 derive
}

// 场景2：包含裸指针
// struct WithRawPointer {
    // ptr: *const i32,  // 裸指针没有实现 Debug
// }

// 场景3：枚举的某些 variant 携带非 Debug 类型
// 这时需要手动实现，为不能 Debug 的字段写个替代品

use std::fmt;

struct PartialDebug;

impl fmt::Debug for PartialDebug {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "<non-debuggable data>")
    }
}

#[derive(Debug)]
struct MayHaveSecrets {
    name: String,
    // secret: PartialDebug,  // 用一个实现了 Debug 的占位
}

fn main() {
    let m = MayHaveSecrets {
        name: "秘密项目".to_string(),
    };
    println!("{:?}", m);
    // 打印结果: MayHaveSecrets { name: "秘密项目" }
}
```

### 5.2.2 Display Trait

如果说 Debug 是给程序员看的，那 Display 就是给用户看的。它定义了类型的"公开形象"——如何被格式化输出。

#### 5.2.2.1 Display trait 定义

```rust
pub trait Display {
    fn fmt(&self, f: &mut Formatter) -> Result<(), Error>;
}
```

Display 和 Debug 的签名几乎一样，区别在于：Debug 有 `?`，Display 没有；Debug 面向程序员，Display 面向用户。

```rust
// Display 的签名特点：没有 ? 标记，说明不能失败
// 实际上 Result<(), Error> 在成功时总是 Ok(())
```

#### 5.2.2.2 {} 格式化占位符

`{}` 是 Display 的占位符，这就是你最常用的 `println!("{}", value)`。

```rust
use std::fmt;

struct Money {
    amount: f64,
    currency: String,
}

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // 使用 write! 宏将格式化字符串写入 Formatter
        write!(f, "{:.2} {}", self.amount, self.currency)
    }
}

fn main() {
    let wallet = Money {
        amount: 1234.567,
        currency: "人民币".to_string(),
    };

    println!("余额: {}", wallet);
    // 打印结果: 余额: 1234.57 人民币
}
```

#### 5.2.2.3 Display 不能直接派生

与 Debug 不同，**Display 不能 derive**。这是有意为之的设计决策：编译器无法猜测你希望如何向用户展示数据，所以必须手动实现。

```rust
// 这是行不通的：
// #[derive(Display)]  // 错误！Display 不能 derive

// 你必须手写：
// impl Display for MyType {
//     fn fmt(&self, f: &mut Formatter) -> Result<(), Error> {
//         ...
//     }
// }
```

为什么不能 derive？因为 Display 的输出是给用户看的，而用户可能有不同的期望。比如一个分数 `Rational(1, 3)`，你可能想显示为 "1/3"，也可能想显示为 "0.333..."，编译器怎么猜？

#### 5.2.2.4 ToString trait

ToString trait 提供了 `to_string` 方法，它实际上是调用了 `Display` trait。所以如果你已经实现了 Display，就自动获得了 to_string 的能力。

```rust
use std::fmt;

struct Temperature {
    celsius: f64,
}

impl fmt::Display for Temperature {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}°C", self.celsius)
    }
}

fn main() {
    let temp = Temperature { celsius: 36.6 };

    // to_string 内部调用了 Display
    let s = temp.to_string();
    println!("字符串: {}", s);
    println!("字符串: {:?}", s);  // 这里 s 已经是 String 了

    // 也可以用 .to_string() 直接转换
    let s2 = temp.to_string();
    // 打印结果:
    // 字符串: 36.6°C
    // 字符串: "36.6°C"
}
```

> **Display vs ToString：**
>
> | 特性 | Display | ToString |
> |------|---------|----------|
> | derive | 不能 | 不能 |
> | 目的 | 给用户看 | 转成 String |
> | 实现 | 必须手写 | 自动获得（如果实现了 Display） |
> | 方法 | `fmt(&self, f: &mut Formatter)` | `to_string(&self) -> String` |

### 5.2.3 Clone Trait

Clone 是 Rust 中用于创建"完整副本"的 trait。如果你需要复制一个值的所有权，而不只是借用，Clone 就是你的好帮手。

#### 5.2.3.1 Clone trait 定义

```rust
pub trait Clone {
    fn clone(&self) -> Self;
}
```

就这么简单！`clone` 方法返回一个 `Self` 类型的值，这个值应该是原值的完整拷贝。

#### 5.2.3.2 #[derive(Clone)] 派生

对于简单类型（所有字段都实现了 Clone），可以直接 derive。

```rust
#[derive(Clone, Debug)]
struct Book {
    title: String,        // String 实现了 Clone
    author: String,       // String 实现了 Clone
    pages: u32,          // u32 实现了 Clone
}

fn main() {
    let book1 = Book {
        title: "Rust 实战".to_string(),
        author: "老王".to_string(),
        pages: 520,
    };

    // clone 一个副本
    let book2 = book1.clone();

    println!("原件: {:?}", book1);  // book1 还能用！
    println!("克隆: {:?}", book2);
    // 打印结果:
    // 原件: Book { title: "Rust 实战", author: "老王", pages: 520 }
    // 克隆: Book { title: "Rust 实战", author: "老王", pages: 520 }
}
```

#### 5.2.3.3 深拷贝语义

Clone 实现的是**深拷贝**。如果你的 struct 包含堆分配的数据（如 String、Vec），clone 会复制这些数据，而不是只复制引用。

```rust
#[derive(Clone, Debug)]
struct Classroom {
    name: String,          // 堆上的字符串
    students: Vec<String>, // 堆上的动态数组
}

fn main() {
    let class1 = Classroom {
        name: "CS101".to_string(),
        students: vec!["张三".to_string(), "李四".to_string()],
    };

    let class2 = class1.clone();

    // 修改克隆后的对象，不会影响原件
    // (如果是引用拷贝/浅拷贝，就会互相影响)

    println!("原件: {:?}", class1);
    println!("克隆: {:?}", class2);

    // 打印结果:
    // 原件: Classroom { name: "CS101", students: ["张三", "李四"] }
    // 克隆: Classroom { name: "CS101", students: ["张三", "李四"] }
}
```

> **Clone vs Copy：**
>
> | 特性 | Clone | Copy |
> |------|-------|------|
> | 推导方式 | 必须 derive 或手动实现 | 编译器自动识别 |
> | 代价 | 可能较重（深拷贝） | 很轻（按位复制） |
> | 调用方式 | 必须显式调用 `.clone()` | 隐式发生 |
> | 例子 | `String`, `Vec`, `Box<T>` | `i32`, `bool`, `char` |

#### 5.2.3.4 clone 方法

clone 方法是 Clone trait 的核心，使用时注意所有权问题：clone 会复制数据，所以原件仍然归你使用。

```rust
#[derive(Clone, Debug)]
struct Password {
    plaintext: String,  // 假设这是敏感信息
    hash: String,
}

fn main() {
    let original = Password {
        plaintext: "123456".to_string(),
        hash: "e10adc3949ba59abbe56e057f20f883e".to_string(),
    };

    // clone 后原件还能用
    let backup = original.clone();

    // 但你有两个独立的 Password 对象了
    println!("原件: {:?}", original);
    println!("备份: {:?}", backup);

    // 打印结果:
    // 原件: Password { plaintext: "123456", hash: "e10adc3949ba59abbe56e057f20f883e" }
    // 备份: Password { plaintext: "123456", hash: "e10adc3949ba59abbe56e057f20f883e" }
}
```

### 5.2.4 Copy Trait

Copy 是 Rust 中一个"神奇"的 trait —— 它没有方法，只是一个标记 trait（marker trait）。实现了 Copy 的类型，在赋值时会发生"按位复制"，不需要显式调用任何方法，这种复制对用户来说是完全隐式的。

#### 5.2.4.1 Copy trait 定义

```rust
pub trait Copy: Clone {}
// Copy 继承自 Clone
// 意思是：如果你想让你的类型是 Copy，它必须也是 Clone
```

Copy 没有任何方法，它只是一个**标记**，告诉编译器："这个类型可以在赋值时按位复制"。

#### 5.2.4.2 Copy 是 Clone 的子集

这条规则 `Copy: Clone` 意味着：**所有 Copy 的类型都必须是 Clone 的**。这是合理的 —— 如果你的类型可以隐式复制，那它当然也可以显式复制（clone）。

```text
类比理解：
- Copy 是"复印机"：一键自动复印，你感觉不到发生了什么
- Clone 是"手动复印"：你需要按复印键，而且可能要等久一点

如果一个类型可以"一键复印"（Copy），它当然也可以"手动复印"（Clone）。
但反过来不一定对：手动复印可以做到的事情（深拷贝复杂结构），一键复印可能做不到。
```

#### 5.2.4.3 哪些类型可以 Copy

Rust 规定：只有那些"不需要堆分配、可以按位复制的简单类型"才能是 Copy。

```text
✓ 可以 Copy 的类型：
  - 所有原始类型：i32, u64, f64, bool, char
  - 只包含 Copy 类型的数组和元组
  - 不可变借用 &T（只要 T 是 Copy）
  - 固定大小的数组（元素是 Copy）

✗ 不能 Copy 的类型：
  - String（堆分配）
  - Vec（堆分配）
  - Box<T>（堆分配）
  - 所有自定义 struct/enum（除非显式标记）
  - 闭包（可能捕获环境）
```

```rust
fn main() {
    // 原始类型都是 Copy
    let a: i32 = 42;
    let b = a;  // 隐式复制，没有 move
    println!("a = {}, b = {}", a, b);  // a 还能用！

    let c: f64 = 3.14;
    let d = c;
    println!("c = {}, d = {}", c, d);  // c 还能用！

    // 数组（元素是 Copy）是 Copy
    let arr1 = [1, 2, 3];
    let arr2 = arr1;
    println!("arr1 = {:?}", arr1);  // arr1 还能用！

    // 元组（元素都是 Copy）是 Copy
    let tuple1 = (1, 2.0, 'a');
    let tuple2 = tuple1;
    println!("tuple1 = {:?}", tuple1);  // tuple1 还能用！

    // 打印结果:
    // a = 42, b = 42
    // c = 3.14, d = 3.14
    // arr1 = [1, 2, 3]
    // tuple1 = (1, 2.0, 'a')
}
```

#### 5.2.4.4 #[derive(Copy, Clone)]

对于自定义类型，如果所有字段都是 Copy 的，你可以 derive 这两个 trait。

```rust
#[derive(Copy, Clone, Debug)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Copy, Clone, Debug)]
struct Color {
    r: u8,
    g: u8,
    b: u8,
}

#[derive(Copy, Clone, Debug)]
struct Pixel(Point, Color);  // 元组结构体，字段都是 Copy

fn main() {
    let p = Point { x: 10, y: 20 };
    let p2 = p;  // Copy，p 还能用
    println!("p = {:?}", p);
    println!("p2 = {:?}", p2);

    let px = Pixel(Point { x: 0, y: 0 }, Color { r: 255, g: 0, b: 0 });
    let px2 = px;  // Copy，px 还能用
    println!("px = {:?}", px);
    println!("px2 = {:?}", px2);

    // 打印结果:
    // p = Point { x: 10, y: 20 }
    // p2 = Point { x: 10, y: 20 }
    // px = Pixel(Point { x: 0, y: 0 }, Color { r: 255, g: 0, b: 0 })
    // px2 = Pixel(Point { x: 0, y: 0 }, Color { r: 255, g: 0, b: 0 })
}
```

#### 5.2.4.5 Copy 的隐含语义

Copy 的"隐式复制"发生在：
- 赋值：`let b = a;`
- 函数传参：`foo(a)` （按值传递）
- 返回值：`return a;`

```rust
#[derive(Copy, Clone, Debug)]
struct Metric {
    value: f64,
}

fn double(x: Metric) -> Metric {
    Metric { value: x.value * 2.0 }
}

fn main() {
    let m = Metric { value: 42.0 };

    // 按值传参，m 被复制
    let result = double(m);

    // m 还在！因为 Metric 是 Copy
    println!("原始: {:?}", m);
    println!("翻倍: {:?}", result);

    // 打印结果:
    // 原始: Metric { value: 42.0 }
    // 翻倍: Metric { value: 84.0 }
}
```

> **为什么 Rust 要区分 Copy 和 Clone？**
>
> 这是 Rust 追求**明确性**和**性能**的结果：
>
> 1. **明确性**：Clone 需要显式调用 `.clone()`，程序员知道这可能是个昂贵的操作
> 2. **性能**：Copy 类型按位复制，非常快，隐式发生也不影响性能
> 3. **安全**：Rust 的所有权系统要求你对"复制"行为有清晰的认识
>
> 简单说：Copy 是给"简单便宜的类型"准备的，Clone 是给"可能很贵的类型"准备的。

### 5.2.5 Drop Trait

Drop trait 让你在值离开作用域前执行一些清理工作，比如释放资源、关闭文件、打印日志等。Rust 的 RAII（Resource Acquisition Is Initialization）模式就依赖于 Drop。

#### 5.2.5.1 Drop trait 定义

```rust
pub trait Drop {
    fn drop(&mut self);
}
```

只有这一个方法！当值离开作用域时，Rust 自动调用这个方法。

#### 5.2.5.2 drop 方法

drop 方法是你"自定义清理逻辑"的地方。在这个方法里，你可以做任何需要"收尾"的事情。

```rust
struct Connection {
    ip: String,
    port: u16,
}

impl Drop for Connection {
    fn drop(&mut self) {
        // 当 Connection 离开作用域时，自动调用这里
        println!("关闭连接: {}:{}", self.ip, self.port);
    }
}

fn main() {
    let conn = Connection {
        ip: "192.168.1.1".to_string(),
        port: 8080,
    };

    println!("建立连接: {}:{}", conn.ip, conn.port);
    println!("使用连接...");

    // conn 在这里离开作用域，drop 被自动调用
    // 打印结果:
    // 建立连接: 192.168.1.1:8080
    // 使用连接...
    // 关闭连接: 192.168.1.1:8080
}
```

#### 5.2.5.3 mem::drop 显式调用

有时候你想提前释放资源，而不是等作用域结束。Rust 提供了 `std::mem::drop` 函数来做这件事。

```rust
use std::mem::drop;

struct File {
    name: String,
}

impl Drop for File {
    fn drop(&mut self) {
        println!("文件 {} 被关闭", self.name);
    }
}

fn main() {
    let file = File { name: "data.txt".to_string() };
    println!("打开文件: {}", file.name);

    // 显式调用 drop，提前释放
    drop(file);

    println!("干点别的事情...");

    // 注意：file 已经不可用了，因为我们显式 drop 了
    // 打印结果:
    // 打开文件: data.txt
    // 文件 data.txt 被关闭
    // 干点别的事情...
}
```

> **drop 函数的原理：**
>
> `std::mem::drop` 实际上就是调用了值的 `drop` 方法：
>
> ```rust
> pub fn drop<T>(x: T) {
>     // x 在这里离开作用域，Drop::drop 被调用
> }
> ```
>
> 所以 `drop(x)` 和 `x.drop()`（如果 Drop 有 pub 方法的话）效果是一样的。但 `drop()` 函数更安全，因为它确保了 drop 一定会发生。

#### 5.2.5.4 Drop 与 Copy 的互斥

这是一个有趣的规则：**不能同时为同一个类型实现 Copy 和 Drop**。为什么？

```text
原因分析：
- Copy 的语义是"按位复制，之后两个值独立存在"
- Drop 的语义是"清理资源"

如果一个类型既是 Copy 又是 Drop：
1. 赋值时发生 Copy，比如 let b = a;
2. a 和 b 都存在
3. a 离开作用域，调用 Drop
4. b 也要离开作用域，再调用 Drop
5. 资源被释放两次！(use-after-free bug)

所以 Rust 禁止了这种组合。
```

```rust
// 这个代码无法编译：
// #[derive(Copy, Clone)]
// struct BadExample {
//     data: String,  // String 不是 Copy，所以其实不会冲突
// }

// 但如果你试图让一个包含非 Copy 字段的类型变成 Copy，
// 编译器会拒绝：
// error: the trait `Copy` cannot be derived for structs containing non-`Copy` types

// Rust 的设计让你不会犯这个错误。
```

```rust
// 正确的做法：选择 Clone 或 Drop
// 方案1：只要 Clone，不要 Copy
#[derive(Clone)]
struct CloneOnly {
    data: String,
}

// 方案2：Clone 和 Drop 都要
struct BothNeeded {
    resource: Vec<u8>,
}

impl Drop for BothNeeded {
    fn drop(&mut self) {
        println!("释放资源...");
    }
}

fn main() {
    let c = CloneOnly { data: "hello".to_string() };
    let c2 = c.clone();  // 显式克隆
    println!("c = {}, c2 = {}", c.data, c2.data);
}
```

### 5.2.6 Default Trait

Default trait 提供了一个创建"默认值"的方式。这在你需要初始化一个对象但又不想指定每个字段时很有用，比如和 struct update 语法搭配。

#### 5.2.6.1 Default trait 定义

```rust
pub trait Default {
    fn default() -> Self;
}
```

这就是全部了！返回一个 `Self` 类型的默认值。

#### 5.2.6.2 #[derive(Default)] 派生

对于所有字段都实现了 Default 的类型，可以直接 derive。

```rust
#[derive(Default, Debug)]
struct Config {
    host: String,        // String 默认是空字符串
    port: u16,           // u16 默认是 0
    max_connections: usize,  // usize 默认是 0
    debug_mode: bool,   // bool 默认是 false
}

fn main() {
    let default_config = Config::default();
    println!("默认配置: {:?}", default_config);
    // 打印结果: 默认配置: Config { host: "", port: 0, max_connections: 0, debug_mode: false }
}
```

#### 5.2.6.3 Default::default() 用法

有两种使用方式：直接调用 `Type::default()` 或者使用 `..Default::default()`。

```rust
#[derive(Default, Debug)]
struct Player {
    name: String,
    health: u32,
    level: u8,
    score: u64,
}

fn main() {
    // 方式1：直接调用
    let default_player = Player::default();
    println!("默认玩家: {:?}", default_player);

    // 方式2：struct update 语法，部分字段覆盖
    let hero = Player {
        name: "超级玛丽".to_string(),
        health: 100,
        ..Default::default()  // 其他字段用默认值
    };
    println!("英雄玩家: {:?}", hero);

    // 打印结果:
    // 默认玩家: Player { name: "", health: 0, level: 0, score: 0 }
    // 英雄玩家: Player { name: "超级玛丽", health: 100, level: 0, score: 0 }
}
```

#### 5.2.6.4 struct Update 模式

struct update 语法 `..Default::default()` 是 Default trait 最常用的场景之一。

```rust
#[derive(Default, Debug)]
struct ServerConfig {
    ip: String,
    port: u16,
    workers: u32,
    timeout_secs: u64,
}

fn main() {
    // 开发环境配置
    let dev_config = ServerConfig {
        ip: "127.0.0.1".to_string(),
        port: 8080,
        ..Default::default()
    };

    // 生产环境配置
    let prod_config = ServerConfig {
        ip: "0.0.0.0".to_string(),
        port: 80,
        workers: 16,
        timeout_secs: 300,
        ..Default::default()
    };

    println!("开发环境: {:?}", dev_config);
    println!("生产环境: {:?}", prod_config);

    // 打印结果:
    // 开发环境: ServerConfig { ip: "127.0.0.1", port: 8080, workers: 0, timeout_secs: 0 }
    // 生产环境: ServerConfig { ip: "0.0.0.0", port: 80, workers: 16, timeout_secs: 300 }
}
```

### 5.2.7 From Trait

From trait 定义了类型之间的转换关系。如果你能从类型 A 转换成类型 B，那么为 A 实现 `From<B>` 或者为 B 实现 `From<A>` 即可。

#### 5.2.7.1 From trait 定义

```rust
pub trait From<T> {
    fn from(value: T) -> Self;
}
```

`From<T>` 表示"可以从 T 创建 Self"。

#### 5.2.7.2 From 实现举例

```rust
// 1. 从 String 到 String（其实不需要，但可以展示）
impl From<String> for String {
    fn from(s: String) -> String {
        s
    }
}

// 2. 从 &str 到 String
impl From<&str> for String {
    fn from(s: &str) -> String {
        String::from(s)
    }
}

// 3. 从 i32 到 f64
impl From<i32> for f64 {
    fn from(n: i32) -> f64 {
        n as f64
    }
}

// 4. 从数组到 Vec
impl From<[i32; 3]> for Vec<i32> {
    fn from(arr: [i32; 3]) -> Vec<i32> {
        vec![arr[0], arr[1], arr[2]]
    }
}

fn main() {
    // 使用 .into() 方法，Rust 会自动推断使用哪个 From 实现
    let s1: String = String::from("hello");
    let s2: String = "world".into();
    let n: f64 = 42.into();
    let v: Vec<i32> = [1, 2, 3].into();

    println!("s1 = {}", s1);
    println!("s2 = {}", s2);
    println!("n = {}", n);
    println!("v = {:?}", v);

    // 打印结果:
    // s1 = hello
    // s2 = world
    // n = 42
    // v = [1, 2, 3]
}
```

#### 5.2.7.3 From 与 Into 的关系

`From` 和 `Into` 是同一个硬币的两面。如果你实现了 `From<T>`，你就自动获得了 `Into<T>` 的能力。

```rust
fn main() {
    // Into 是 From 的反函数
    // 如果 T: From<U>，那么 U: Into<T>

    let s: String = "hello".into();  // 相当于 String::from("hello")
    // 或者显式写：
    let s2: String = Into::<String>::into("hello");

    println!("s = {}, s2 = {}", s, s2);

    // 什么时候用 From？什么时候用 Into？
    // - 写库/类型定义时：实现 From，因为 Into 是自动获得的
    // - 调用方代码时：用 .into() 更简洁
    // 打印结果:
    // s = hello, s2 = hello
}
```

> **实现 From 的规则：**
>
> 1. **互反性**：如果你为 A 实现了 `From<B>`，那你可能也想为 B 实现 `From<A>`，但这不是强制的
> 2. **单向转换**：From 定义的是"单向转换"，不要假设它是对称的
> 3. **正确性**：转换应该保持语义，比如把"10"（字符串）转换成 10（数字）是合理的，但把 "hello" 转换成 0 就不太对

### 5.2.8 Into Trait

Into 是 From 的"镜像"，它让你可以用 `value.into()` 的方式转换类型。

#### 5.2.8.1 Into trait 定义

```rust
pub trait Into<T> {
    fn into(self) -> T;
}
```

实际上在标准库中，`Into` 的完整定义更复杂（包含泛型约束），但本质就是这样。

```rust
// 标准库中 Into 的真实签名是：
// impl<T> Into<T> for U where U: From<T> { ... }
// 所以 Into 的实现是由 From 自动派生的
```

#### 5.2.8.2 T: Into<U> 约束

在泛型函数中，你可以通过 `T: Into<U>` 来约束参数类型。

```rust
// 这个函数接受任何可以转换成 String 的类型
fn to_string<S: Into<String>>(value: S) -> String {
    value.into()
}

// 更灵活的版本，返回类型由调用方指定
fn convert<T, U>(value: T) -> U
where
    T: Into<U>,
{
    value.into()
}

fn main() {
    // 各种类型转 String
    println!("{}", to_string("hello"));
    println!("{}", to_string(String::from("world")));
    println!("{}", to_string(123.to_string()));

    // 通用转换
    let s: String = convert("你好");
    let i: i32 = convert(3.14_f64);  // f64 到 i32 会截断
    println!("s = {}, i = {}", s, i);

    // 打印结果:
    // hello
    // world
    // 123
    // s = 你好, i = 3
}
```

#### 5.2.8.3 与 From 的选用原则

```text
选 From：
- 在你的类型上定义转换逻辑
- 需要明确指定转换的源类型

选 Into：
- 在调用方代码中使用
- 想让函数接受更灵活的类型

简单记忆：定义时用 From，调用时用 Into。
```

### 5.2.9 AsRef / AsMut Trait

AsRef 和 AsMut 提供了"廉价借用转换"的抽象。它们是 Rust 用来处理"可以转换为什么引用"的 trait。

#### 5.2.9.1 AsRef trait 定义

```rust
pub trait AsRef<T: ?Sized> {
    fn as_ref(&self) -> &T;
}
```

`AsRef<T>` 意味着"可以借用成 T 的引用"。注意 `?Sized` 约束允许 T 是动态大小的类型（如 str）。

#### 5.2.9.2 AsMut trait 定义

```rust
pub trait AsMut<T: ?Sized> {
    fn as_mut(&mut self) -> &mut T;
}
```

可变版本的 AsRef，提供可变借用转换。

#### 5.2.9.3 通用实现

标准库为很多类型提供了 AsRef 的实现。

```rust
fn main() {
    // String 实现了 AsRef<str>
    let s = String::from("hello");
    let s_ref: &str = s.as_ref();
    println!("s_ref = {}", s_ref);

    // Vec<T> 实现了 AsRef<[T]>
    let v = vec![1, 2, 3];
    let slice: &[i32] = v.as_ref();
    println!("slice = {:?}", slice);

    // String 也实现了 AsRef<[u8]> (即 bytes)
    let bytes: &[u8] = s.as_ref();
    println!("bytes = {:?}", bytes);

    // 数组也实现了 AsRef<[T; N]>
    let arr = [1, 2, 3];
    let slice: &[i32] = arr.as_ref();
    println!("arr as slice = {:?}", slice);

    // 打印结果:
    // s_ref = hello
    // slice = [1, 2, 3]
    // bytes = [104, 101, 108, 108, 111]
    // arr as slice = [1, 2, 3]
}
```

#### 5.2.9.4 AsRef 作为泛型约束

AsRef 常被用作泛型约束，让函数接受多种可以转换成引用的类型。

```rust
// 这个函数可以接受任何可以转换成 &str 的类型
fn print_if_valid(input: impl AsRef<str>) {
    let s = input.as_ref();
    if !s.is_empty() {
        println!("有效输入: {}", s);
    }
}

fn main() {
    print_if_valid("hello");           // &str
    print_if_valid(String::from("world"));  // String
    print_if_valid("你好".to_string());     // String again

    // 打印结果:
    // 有效输入: hello
    // 有效输入: world
    // 有效输入: 你好
}
```

> **AsRef vs From/Into：**
>
> | Trait | 转换代价 | 返回类型 | 用途 |
> |-------|---------|---------|------|
> | AsRef | 无代价（只是借用） | `&T` | 通用引用接受 |
> | From/Into | 可能需要分配/复制 | `T` | 值转换 |
>
> 简单说：AsRef 不拿走所有权，只是借个参考；From/Into 可能要搬东西。

### 5.2.10 Borrow / BorrowMut Trait

Borrow 和 BorrowMut 类似于 AsRef/AsMut，但它们额外承诺了**哈希稳定性**——同一个值 Borrow 出来的引用，在哈希时会得到相同的结果。这对 HashMap 的键来说非常重要。

#### 5.2.10.1 Borrow trait 定义

```rust
pub trait Borrow<Borrowed> {
    fn borrow(&self) -> &Borrowed;
}
```

Borrow 返回一个借用，但比 AsRef 更严格：它要求"借用的值在哈希时等于原值"。

#### 5.2.10.2 BorrowMut trait 定义

```rust
pub trait BorrowMut<Borrowed>: Borrow<Borrowed> {
    fn borrow_mut(&mut self) -> &mut Borrowed;
}
```

可变借用版本，也继承自 Borrow。

#### 5.2.10.3 HashMap 的键约束

当你用 `HashMap<K, V>` 时，K 必须实现 `Borrow<Q>`，这样你才能用 `Q` 类型的值来查找 `K` 类型的键。

```rust
use std::collections::HashMap;

fn main() {
    let mut scores: HashMap<String, u32> = HashMap::new();

    scores.insert(String::from("Alice"), 100);
    scores.insert(String::from("Bob"), 85);
    scores.insert(String::from("Charlie"), 92);

    // 用 &str 查找 String 键！这就是 Borrow 的威力
    // 因为 String 实现了 Borrow<str>
    if let Some(&score) = scores.get("Alice") {
        println!("Alice 的分数: {}", score);
    }

    // 如果没有 Borrow，你得这样：
    // scores.get(&String::from("Alice"))
    // 有了 Borrow，直接用字符串字面量就行

    // 打印结果:
    // Alice 的分数: 100
}
```

#### 5.2.10.4 Borrow vs AsRef

```text
关键区别：
- AsRef：只要求"可以转换"，不保证哈希等价
- Borrow：要求"可以转换，并且哈希等价"（对 HashMap 键查找很重要）

举例：
- String 实现了 AsRef<str> 和 AsRef<[u8]>
- String 也实现了 Borrow<str> 和 Borrow<[u8]>（保证哈希等价）
- 但注意：AsRef<[u8]> 和 Borrow<[u8]> 是不同的约束，适用于不同场景
```

```rust
use std::borrow::Borrow;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

fn hash<T: Hash>(value: &T) -> u64 {
    let mut hasher = DefaultHasher::new();
    value.hash(&mut hasher);
    hasher.finish()
}

fn main() {
    let s = String::from("hello");
    let s_str: &str = s.borrow();

    println!("String hash: {}", hash(&s));
    println!("str hash: {}", hash(s_str));
    println!("相等: {}", hash(&s) == hash(s_str));
    // Borrow 保证哈希等价

    // 打印结果:
    // String hash: 9835680345717941425
    // str hash: 9835680345717941425
    // 相等: true
}
```

### 5.2.11 Eq / PartialEq Trait

相等性比较是 Rust 中最常用的操作之一。PartialEq 允许"部分相等"（可以有 NaN 这样的情况），Eq 则是"完全相等"。

#### 5.2.11.1 PartialEq trait 定义

```rust
pub trait PartialEq<Rhs: ?Sized = Self> {
    fn eq(&self, other: &Rhs) -> bool;
    fn ne(&self, other: &Rhs) -> bool { !self.eq(other) }
}
```

`PartialEq` 的"Partial"来自于数学上的"偏序关系"——它不要求自反性（a == a 在浮点数中不一定成立）。

#### 5.2.11.2 #[derive(PartialEq)] 派生

```rust
#[derive(PartialEq, Debug)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

#[derive(PartialEq)]
enum Direction {
    North,
    South,
    East,
    West,
}

fn main() {
    let v1 = Version { major: 1, minor: 2, patch: 3 };
    let v2 = Version { major: 1, minor: 2, patch: 3 };
    let v3 = Version { major: 1, minor: 2, patch: 4 };

    println!("v1 == v2: {}", v1 == v2);  // true
    println!("v1 == v3: {}", v1 == v3);  // false

    let d1 = Direction::North;
    let d2 = Direction::South;
    println!("North == North: {}", d1 == d1);  // true
    println!("North == South: {}", d1 == d2);  // false

    // 打印结果:
    // v1 == v2: true
    // v1 == v3: false
    // North == North: true
    // North == South: false
}
```

#### 5.2.11.3 Eq trait

Eq 是一个标记 trait，表示"完全相等"。

```rust
pub trait Eq: PartialEq<Self> {}
// 没有任何额外方法，只是标记
```

Eq 要求 `PartialEq` 满足：
- 自反性：`a == a` 总是 true
- 对称性：`a == b` 意味着 `b == a`
- 传递性：`a == b && b == c` 意味着 `a == c`

#### 5.2.11.4 f32 / f64 不是 Eq 的原因

```rust
fn main() {
    // 浮点数的 NaN 是著名的"不等于自己"
    let nan = f64::NAN;
    println!("NaN == NaN: {}", nan == nan);  // false！
    println!("NaN.is_nan(): {}", nan.is_nan());  // true

    // 所以 f64 只能实现 PartialEq，不能实现 Eq
    // 因为 Eq 要求自反性（a == a 必须为 true）

    // 其他 NaN 相关的坑：
    println!("0.0 == -0.0: {}", 0.0_f64 == -0.0_f64);  // true
    println!("1.0 / 0.0: {}", 1.0 / 0.0);  // inf
    println!("-1.0 / 0.0: {}", -1.0 / 0.0);  // -inf

    // 打印结果:
    // NaN == NaN: false
    // NaN.is_nan(): true
    // 0.0 == -0.0: true
    // 1.0 / 0.0: inf
    // -1.0 / 0.0: -inf
}
```

### 5.2.12 Ord / PartialOrd Trait

排序 trait 让你可以对值进行比较。和相等性一样，排序也分"部分"和"完全"。

#### 5.2.12.1 PartialOrd trait 定义

```rust
pub trait PartialOrd<Rhs: ?Sized = Self>: PartialEq<Rhs> {
    fn partial_cmp(&self, other: &Rhs) -> Option<Ordering>;
    fn lt(&self, other: &Rhs) -> bool { ... }
    fn le(&self, other: &Rhs) -> bool { ... }
    fn gt(&self, other: &Rhs) -> bool { ... }
    fn ge(&self, other: &Rhs) -> bool { ... }
}
```

`partial_cmp` 返回 `Option<Ordering>`，因为有些值可能无法比较（如 NaN）。

#### 5.2.12.2 Ordering 枚举

```rust
pub enum Ordering {
    Less,       // self < other
    Equal,      // self == other
    Greater,    // self > other
}
```

Ordering 是比较结果的枚举，用于精确表达"谁大谁小"。

```rust
fn compare<T: Ord>(a: &T, b: &T) -> Ordering {
    a.cmp(b)
}

fn main() {
    let x = 10;
    let y = 20;

    println!("x.cmp(&y) = {:?}", x.cmp(&y));  // Less
    println!("y.cmp(&x) = {:?}", y.cmp(&x));  // Greater
    println!("x.cmp(&x) = {:?}", x.cmp(&x));  // Equal

    // 也可以用 matches 检查
    println!("x < y: {}", matches!(x.cmp(&y), Ordering::Less));
    println!("x > y: {}", matches!(x.cmp(&y), Ordering::Greater));

    // 打印结果:
    // x.cmp(&y) = Less
    // y.cmp(&x) = Greater
    // x.cmp(&x) = Equal
    // x < y: true
    // x > y: false
}
```

#### 5.2.12.3 #[derive(PartialOrd)] 派生

```rust
#[derive(PartialOrd, PartialEq, Debug)]
struct Product {
    name: String,
    price: f64,
}

fn main() {
    let p1 = Product { name: "苹果".to_string(), price: 5.0 };
    let p2 = Product { name: "香蕉".to_string(), price: 3.0 };
    let p3 = Product { name: "樱桃".to_string(), price: 50.0 };

    // 按价格排序
    println!("p1 < p2: {}", p1 < p2);  // 5.0 < 3.0? false
    println!("p2 < p3: {}", p2 < p3);  // 3.0 < 50.0? true

    // derive 的 PartialOrd 按字典序比较字段
    // 先比较 name，如果相等再比较 price
    let p4 = Product { name: "苹果".to_string(), price: 10.0 };
    println!("p1 < p4: {}", p1 < p4);  // true (price 更小)

    // 打印结果:
    // p1 < p2: false
    // p2 < p3: true
    // p1 < p4: true
}
```

#### 5.2.12.4 Ord trait

Ord 要求完全排序，定义如下：

```rust
pub trait Ord: Eq + PartialOrd<Self> {
    fn cmp(&self, other: &Self) -> Ordering;
}
```

Ord 和 PartialOrd 的区别：
- PartialOrd 返回 `Option<Ordering>`（因为可能无法比较）
- Ord 返回 `Ordering`（一定可以比较）

#### 5.2.12.5 Ord 的完全性要求

```text
Ord 要求：
1. 自反：cmp(a, a) == Equal
2. 反对称：cmp(a, b) == Less 当且仅当 cmp(b, a) == Greater
3. 传递：cmp(a, b) == Less && cmp(b, c) == Less 意味着 cmp(a, c) == Less

这些条件保证了一个"完全有序"的状态。
```

```rust
#[derive(Eq, PartialEq, Ord, Debug)]
struct Student {
    name: String,
    score: u32,
}

fn main() {
    let mut students = vec![
        Student { name: "张三".to_string(), score: 85 },
        Student { name: "李四".to_string(), score: 92 },
        Student { name: "王五".to_string(), score: 78 },
        Student { name: "赵六".to_string(), score: 92 },
    ];

    // 排序（按 score 降序，score 相同时按 name 升序）
    students.sort();

    for s in &students {
        println!("{:?}", s);
    }

    // 打印结果:
    // Student { name: "王五", score: 78 }
    // Student { name: "张三", score: 85 }
    // Student { name: "李四", score: 92 }
    // Student { name: "赵六", score: 92 }
}
```

### 5.2.13 Hash Trait

Hash trait 允许你把值哈希成一个字节序列，用于 HashMap、HashSet 等哈希数据结构的键。

#### 5.2.13.1 Hash trait 定义

```rust
pub trait Hash {
    fn hash<H: Hasher>(&self, state: &mut H);
    fn hash_slice<H: Hasher>(data: &[Self], state: &mut H)
    where Self: Sized { ... }
}
```

核心是 `hash` 方法，它把数据写入一个 `Hasher`。

#### 5.2.13.2 #[derive(Hash)] 派生

```rust
#[derive(Hash, Eq, PartialEq, Debug)]
struct CacheKey {
    namespace: String,
    key: String,
}

fn main() {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::Hash;

    let key1 = CacheKey {
        namespace: "users".to_string(),
        key: "12345".to_string(),
    };

    let key2 = CacheKey {
        namespace: "users".to_string(),
        key: "12345".to_string(),
    };

    let key3 = CacheKey {
        namespace: "users".to_string(),
        key: "67890".to_string(),
    };

    // 计算哈希值
    let mut hasher = DefaultHasher::new();
    key1.hash(&mut hasher);
    let hash1 = hasher.finish();

    let mut hasher2 = DefaultHasher::new();
    key2.hash(&mut hasher2);
    let hash2 = hasher2.finish();

    let mut hasher3 = DefaultHasher::new();
    key3.hash(&mut hasher3);
    let hash3 = hasher3.finish();

    println!("key1 hash: {}", hash1);
    println!("key2 hash: {}", hash2);
    println!("key3 hash: {}", hash3);
    println!("key1 == key2: {}", key1 == key2);
    println!("key1 == key3: {}", key1 == key3);

    // 打印结果:
    // key1 hash: <哈希值>
    // key2 hash: <相同的哈希值>
    // key3 hash: <不同的哈希值>
    // key1 == key2: true
    // key1 == key3: false
}
```

#### 5.2.13.3 Hash 与 Eq 的协同要求

这是一个重要规则：**如果 a == b，则 hash(a) == hash(b)**。

```text
为什么这个规则很重要？
- HashMap 用哈希值来快速查找
- 如果两个相等的值哈希值不同，HashMap 就找不到它
- 这就是"哈希碰撞"，会导致 bug

Rust 编译器会警告你如果 derive 了 Hash 但没有 derive Eq：
"you should implement Eq if Hash is implemented"
```

```rust
use std::collections::HashMap;
use std::hash::Hash;

#[derive(Hash, Eq, PartialEq, Debug)]
struct Username(String);

fn main() {
    let mut map: HashMap<Username, u32> = HashMap::new();

    map.insert(Username("alice".to_string()), 100);
    map.insert(Username("bob".to_string()), 85);

    // 查找，Username 必须 Hash 和 Eq 都实现
    let alice_key = Username("alice".to_string());
    if let Some(&score) = map.get(&alice_key) {
        println!("Alice 的分数: {}", score);
    }

    // 打印结果:
    // Alice 的分数: 100
}
```

### 5.2.14 ToOwned Trait

ToOwned 提供了从借用数据创建有所有权数据的能力，是 Clone 的更通用版本。

#### 5.2.14.1 ToOwned trait 定义

```rust
pub trait ToOwned {
    type Owned: Borrow<Self>;

    fn to_owned(&self) -> Self::Owned;

    fn clone_into(&self, target: &mut Self::Owned) { ... }
}
```

ToOwned 允许你从 `&T` 创建 `T` 的所有者版本。

#### 5.2.14.2 to_owned vs clone

```rust
fn main() {
    // &str 到 String
    let s: &str = "hello";
    let owned_str: String = s.to_owned();  // ToOwned
    let owned_clone: String = s.to_string();  // 用 Display/ToString

    // &[i32] 到 Vec<i32>
    let slice: &[i32] = &[1, 2, 3];
    let owned_vec: Vec<i32> = slice.to_owned();  // ToOwned
    let owned_clone2: Vec<i32> = slice.to_vec();  // 专用方法

    // str 是一个特殊的类型，它没有所有权
    // to_owned() 返回 String
    let s2: &str = "world";
    let owned2: String = ToOwned::to_owned(s2);

    println!("owned_str: {}", owned_str);
    println!("owned_clone: {}", owned_clone);
    println!("owned_vec: {:?}", owned_vec);
    println!("owned_clone2: {:?}", owned_clone2);
    println!("owned2: {}", owned2);

    // 打印结果:
    // owned_str: hello
    // owned_clone: hello
    // owned_vec: [1, 2, 3]
    // owned_clone2: [1, 2, 3]
    // owned2: world
}
```

> **ToOwned 的优势：**
>
> ToOwned 比 Clone 更通用。Clone 要求 `&self -> Self`，但 ToOwned 的返回类型可以是"拥有相同数据但类型不同"的东西。
>
> 例如，`str` 是 `ToOwned<String>`，因为 `&str` 可以变成 `String`（不同的类型）。但 `String` 不是 Clone 自 `&str`，因为 `Clone` 只能从 `&String` 到 `String`。

### 5.2.15 Iterator Trait

Iterator 是 Rust 中最强大的 trait 之一，它定义了迭代器的基本行为。通过实现 Iterator，你可以让任何类型成为可迭代的。

#### 5.2.15.1 Iterator trait 定义

```rust
pub trait Iterator {
    type Item;  // 迭代器的元素类型

    fn next(&mut self) -> Option<Self::Item>;

    // 还有很多默认方法...
    fn collect<B>(self) -> B where B: FromIterator<Self::Item> { ... }
    fn map<B, F>(self, f: F) -> Map<Self, F> { ... }
    fn filter<P>(self, predicate: P) -> Filter<Self, P> { ... }
    // ... 还有几十个
}
```

Iterator trait 是 Rust 迭代器的核心，它只有一个必须实现的方法：`next`。

#### 5.2.15.2 next 方法

`next()` 返回下一个元素，用 `Option` 包装：
- `Some(item)` - 有下一个元素
- `None` - 迭代结束

```rust
struct Counter {
    current: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Self {
        Counter { current: 0, max }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            self.current += 1;
            Some(self.current)
        } else {
            None
        }
    }
}

fn main() {
    let mut counter = Counter::new(5);

    println!("next: {:?}", counter.next());  // Some(1)
    println!("next: {:?}", counter.next());  // Some(2)
    println!("next: {:?}", counter.next());  // Some(3)
    println!("next: {:?}", counter.next());  // Some(4)
    println!("next: {:?}", counter.next());  // Some(5)
    println!("next: {:?}", counter.next());  // None
    println!("next: {:?}", counter.next());  // None (之后永远是 None)

    // 打印结果:
    // next: Some(1)
    // next: Some(2)
    // next: Some(3)
    // next: Some(4)
    // next: Some(5)
    // next: None
    // next: None
}
```

#### 5.2.15.3 IntoIterator trait

IntoIterator 让你可以用 `for item in collection` 的语法。

```rust
pub trait IntoIterator<Item = Self::Item> {
    type Item;
    type IntoIter: Iterator<Item = Self::Item>;

    fn into_iter(self) -> Self::IntoIter;
}
```

实现 IntoIterator 后，你就可以用 `for` 循环遍历你的类型。

```rust
struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
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

impl IntoIterator for Fibonacci {
    type Item = u64;
    type IntoIter = Fibonacci;

    fn into_iter(self) -> Self::IntoIter {
        self
    }
}

fn main() {
    let fib = Fibonacci::new();

    // IntoIterator 让我们可以这样写
    for (i, n) in fib.take(10).enumerate() {
        println!("F{} = {}", i, n);
    }

    // 打印结果:
    // F0 = 0
    // F1 = 1
    // F2 = 1
    // F3 = 2
    // F4 = 3
    // F5 = 5
    // F6 = 8
    // F7 = 13
    // F8 = 21
    // F9 = 34
}
```

#### 5.2.15.4 for 循环与 IntoIterator 的交互

`for` 循环实际上是语法糖，它会被展开成 `into_iter()` 调用。

```rust
fn main() {
    let v = vec![1, 2, 3];

    // 这是
    for item in v {
        println!("{}", item);
    }

    // 展开后等价于：
    let mut iter = v.into_iter();
    while let Some(item) = iter.next() {
        println!("{}", item);
    }

    // 打印结果:
    // 1
    // 2
    // 3
    // 1
    // 2
    // 3
}
```

> **三种迭代方式：**
>
> | 方式 | 语法 | 消耗所有权 | 返回类型 |
> |------|------|-----------|---------|
> | `iter()` | `for item in &v` | 否 | `&Item` |
> | `iter_mut()` | `for item in &mut v` | 否 | `&mut Item` |
> | `into_iter()` | `for item in v` | 是 | `Item` |

### 5.2.16 Fn / FnMut / FnOnce Trait

这三个 trait 描述了闭包（closure）和函数（function）的行为。它们是 Rust 函数式编程的基础。

#### 5.2.16.1 Fn trait

Fn 表示"可以多次调用，且不修改捕获的变量"。

```rust
pub trait Fn<Args> {
    extern "rust-call" fn call(&self, args: Args) -> Self::Output;
}
```

Fn 闭包可以：
- 被多次调用
- 读取捕获的变量
- 不能修改捕获的变量
- 可以被复制（如果所有捕获的东西都是 Copy）

```rust
fn main() {
    let x = 10;

    // Fn 闭包：只读取 x
    let print_x = || println!("x = {}", x);

    print_x();
    print_x();
    print_x();  // 想调用多少次都行

    // 打印结果:
    // x = 10
    // x = 10
    // x = 10
}
```

#### 5.2.16.2 FnMut trait

FnMut 表示"可以多次调用，且可以修改捕获的变量"。

```rust
pub trait FnMut<Args>: Fn<Args> {
    extern "rust-call" fn call_mut(&mut self, args: Args) -> Self::Output;
}
```

FnMut 闭包可以：
- 被多次调用
- 读取和修改捕获的变量
- 因为会修改环境，所以不能被复制

```rust
fn main() {
    let mut count = 0;

    // FnMut 闭包：修改捕获的 count
    let mut increment = || {
        count += 1;
        println!("count = {}", count);
    };

    increment();
    increment();
    increment();

    println!("最终 count = {}", count);

    // 打印结果:
    // count = 1
    // count = 2
    // count = 3
    // 最终 count = 3
}
```

#### 5.2.16.3 FnOnce trait

FnOnce 表示"只能被调用一次"。这听起来像是个限制，但实际上很多场景下你只需要调用一次。

```rust
pub trait FnOnce<Args> {
    extern "rust-call" fn call_once(self, args: Args) -> Self::Output;
}
```

FnOnce 闭包可以：
- 只被调用一次
- 可以消耗（move）捕获的变量
- 因为会消耗环境，所以不能被复制或再次调用

```rust
fn main() {
    let data = vec![1, 2, 3];

    // FnOnce 闭包：消耗 data
    let consume_data = || {
        println!("消耗掉: {:?}", data);
        // data 在这里被消耗了，不能再用了
    };

    consume_data();
    // consume_data();  // 编译错误！已经调用过了

    // 打印结果:
    // 消耗掉: [1, 2, 3]
}
```

#### 5.2.16.4 三者的继承关系

```text
FnOnce
  ↑
FnMut
  ↑
Fn

继承关系解释：
- Fn: 什么都不消耗，可以多次调用
- FnMut: 可能消耗/修改，可以多次调用
- FnOnce: 一定消耗，只能调用一次

所有 Fn 都是 FnMut，所有 FnMut 都是 FnOnce。
但反过来不成立。

类比理解：
- Fn = 图书馆的书：可以反复读
- FnMut = 笔记本：可以反复写
- FnOnce = 一次性口罩：用完就扔
```

```rust
fn apply<F>(f: F)
where
    F: Fn(),  // Fn 约束
{
    f();
    f();
}

fn apply_once<F>(f: F)
where
    F: FnOnce(),  // FnOnce 约束
{
    f();
    // f();  // 错误！
}

fn main() {
    let x = 5;
    let print_fn = || println!("Fn: {}", x);
    apply(print_fn);  // Fn 可以传给 Fn/FnMut/FnOnce 约束

    let mut y = 5;
    let mut increment = || { y += 1; println!("FnMut: {}", y); };
    // 错误！apply 需要 Fn 约束，但 increment 是 FnMut，不是 Fn
    // apply(increment);  // 取消注释会编译失败
    // 注意：FnMut 可以传给 FnMut/FnOnce 约束，但不能传给 Fn 约束
    // 正确做法：把 apply 改成 FnMut 约束

    let data = vec![1, 2];
    let consume = || println!("FnOnce: {:?}", data);
    apply_once(consume);  // FnOnce 只能传给 FnOnce
}
```

#### 5.2.16.5 闭包的 trait 实现

在 Rust 中，闭包会自动实现这三个 trait 中的一个（或者多个）。具体实现哪个，取决于闭包如何使用捕获的变量。

```rust
// 闭包类型 | 能实现哪些 Fn trait
// --------|----------------------
// 只读    | Fn, FnMut, FnOnce
// 写      | FnMut, FnOnce
// 消耗    | FnOnce

fn main() {
    // 场景1：只读捕获 -> Fn
    let a = 10;
    let fn_closure = || a * 2;  // Fn
    println!("fn_closure(): {}", fn_closure());

    // 场景2：修改捕获 -> FnMut
    let mut b = 10;
    let fnmut_closure = || { b *= 2; b };  // FnMut
    println!("fnmut_closure(): {}", fnmut_closure());

    // 场景3：消耗捕获 -> FnOnce
    let c = vec![1, 2];
    let fnonce_closure = || {
        let _owned = c;  // 消耗 c
        42
    };
    println!("fnonce_closure(): {}", fnonce_closure());

    // 打印结果:
    // fn_closure(): 20
    // fnmut_closure(): 20
    // fnonce_closure(): 42
}
```

---

## 5.3 Trait 对象与动态分发

想象一下，你经营一家动物园。动物园里有老虎、兔子、鸭子......每天你要给它们喂食。但问题是：老虎吃肉，兔子吃草，鸭子吃虫子。你不可能写一个函数同时处理所有情况，因为你需要**在运行时才知道具体是哪种动物**。

在编程世界里，这种"需要在运行时决定具体类型"的场景叫做**多态（Polymorphism）**。Rust 用 **trait 对象（Trait Object）** 来解决这个问题。

### 5.3.1 dyn Trait 语法

`dyn Trait` 是 Rust 中表示"trait 对象"的语法。它代表"实现了某个 trait 的任意类型"。

#### 5.3.1.1 trait 对象定义

```rust
// 使用 dyn Trait 作为类型
let animal: &dyn Animal;
// 或者 Box<dyn Animal>
let animal: Box<dyn Animal>;
```

`dyn` 关键字告诉 Rust："这是一个动态大小的类型，它的实际类型要在运行时才能确定"。

```rust
trait Animal {
    fn make_sound(&self) -> String;
}

struct Dog;
struct Cat;
struct Duck;

impl Animal for Dog {
    fn make_sound(&self) -> String {
        "汪汪汪！".to_string()
    }
}

impl Animal for Cat {
    fn make_sound(&self) -> String {
        "喵喵喵！".to_string()
    }
}

impl Animal for Duck {
    fn make_sound(&self) -> String {
        "嘎嘎嘎！".to_string()
    }
}

fn main() {
    // animal 是 trait 对象，它指向一个 Dog
    let animal: &dyn Animal = &Dog;

    // 调用方法时，Rust 会在运行时决定调用哪个具体实现
    println!("狗叫: {}", animal.make_sound());
    // 打印结果: 狗叫: 汪汪汪！
}
```

#### 5.3.1.2 虚表（vtable）机制

trait 对象背后是**虚表（vtable，Virtual Table）** 的魔法。当 Rust 创建 trait 对象时，它会：
1. 创建一个指向数据的指针
2. 创建一个指向 vtable 的指针

vtable 包含了每个方法的具体实现地址。

```text
trait 对象内存布局：

┌─────────────────────────────────────┐
│  Data Pointer  ──────────────────┐  │
│  (指向实际数据)                    │  │
├─────────────────────────────────────┤  │
│  VTable Pointer ──────────────┐   │  │
│  (指向虚表)                      │   │  │
└─────────────────────────────────────┘  │
                                      │  │
       ┌──────────────────────────────┘
       ▼
┌─────────────────────────────────────┐
│  vtable for Dog:                    │
│  - make_sound: 0x1000 (地址)        │
│  - ...                              │
├─────────────────────────────────────┤
│  vtable for Cat:                   │
│  - make_sound: 0x2000 (地址)        │
│  - ...                              │
└─────────────────────────────────────┘
```

这就是为什么 trait 对象有运行时开销：每次方法调用都要通过 vtable 查找，而不是像静态分发那样直接内联。

#### 5.3.1.3 胖指针（Fat Pointer）

我们把同时包含数据指针和 vtable 指针的指针叫做**胖指针（Fat Pointer）**。普通的 `&T` 是单个指针（8 字节 on 64-bit 系统），但 `&dyn Trait` 是两个指针（16 字节）。

```rust
use std::mem;

trait Shape {
    fn area(&self) -> f64;
}

struct Circle { radius: f64 }
struct Square { side: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }
}

fn main() {
    let circle = Circle { radius: 2.0 };

    // 胖指针的大小
    println!("&Circle 大小: {} 字节", mem::size_of::<&Circle>());
    println!("&dyn Shape 大小: {} 字节", mem::size_of::<&dyn Shape>());
    println!("Box<dyn Shape> 大小: {} 字节", mem::size_of::<Box<dyn Shape>>());

    // 打印结果:
    // &Circle 大小: 8 字节
    // &dyn Shape 大小: 16 字节
    // Box<dyn Shape> 大小: 16 字节
    // (在 64 位系统上)
}
```

### 5.3.2 Trait 对象的使用场景

Trait 对象适合那些"需要异构集合"或"需要运行时多态"的场景。

#### 5.3.2.1 异构集合

异构集合是指集合中包含不同类型的元素。在使用泛型时，你只能放同类型的元素；但使用 trait 对象，你可以放各种不同的类型。

```rust
trait Printable {
    fn print(&self);
}

struct Document { content: String }
struct Image { data: Vec<u8>, format: String }
struct Video { duration_secs: u32 }

impl Printable for Document {
    fn print(&self) {
        println!("📄 文档: {}", self.content);
    }
}

impl Printable for Image {
    fn print(&self) {
        println!("🖼️ 图片: {} 格式, {} 字节", self.format, self.data.len());
    }
}

impl Printable for Video {
    fn print(&self) {
        println!("🎬 视频: {} 秒", self.duration_secs);
    }
}

fn main() {
    // 异构集合！包含 Document, Image, Video 三种类型
    let items: Vec<Box<dyn Printable>> = vec![
        Box::new(Document { content: "Hello World".to_string() }),
        Box::new(Image { data: vec![0u8; 1024], format: "PNG".to_string() }),
        Box::new(Video { duration_secs: 120 }),
    ];

    // 统一遍历调用
    for item in &items {
        item.print();
    }

    // 打印结果:
    // 📄 文档: Hello World
    // 🖼️ 图片: PNG 格式, 1024 字节
    // 🎬 视频: 120 秒
}
```

#### 5.3.2.2 运行时多态

当你在编译时不知道具体类型，只能在运行时决定时，trait 对象就是你的好帮手。

```rust
use std::io::{self, Write};

trait Operation {
    fn execute(&self, a: i32, b: i32) -> i32;
}

struct Add;
struct Subtract;
struct Multiply;

impl Operation for Add {
    fn execute(&self, a: i32, b: i32) -> i32 {
        a + b
    }
}

impl Operation for Subtract {
    fn execute(&self, a: i32, b: i32) -> i32 {
        a - b
    }
}

impl Operation for Multiply {
    fn execute(&self, a: i32, b: i32) -> i32 {
        a * b
    }
}

// 运行时根据用户输入决定用哪个操作
fn get_operation(op: &str) -> Box<dyn Operation> {
    match op {
        "+" => Box::new(Add),
        "-" => Box::new(Subtract),
        "*" => Box::new(Multiply),
        _ => panic!("未知操作符: {}", op),
    }
}

fn main() {
    let mut input = String::new();

    print!("输入操作符 (+, -, *): ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).unwrap();
    let op = input.trim();

    let operation = get_operation(op);

    let result = operation.execute(10, 5);
    println!("10 {} 5 = {}", op, result);

    // 示例交互：
    // 输入 + -> 10 + 5 = 15
    // 输入 - -> 10 - 5 = 5
    // 输入 * -> 10 * 5 = 50
}
```

#### 5.3.2.3 回调与策略模式

Trait 对象常用于实现回调系统和策略模式。你可以把函数/策略封装成 trait 对象，然后传给其他函数。

```rust
trait Strategy {
    fn execute(&self, data: &[i32]) -> i32;
}

struct SumStrategy;
struct MaxStrategy;
struct MinStrategy;

impl Strategy for SumStrategy {
    fn execute(&self, data: &[i32]) -> i32 {
        data.iter().sum()
    }
}

impl Strategy for MaxStrategy {
    fn execute(&self, data: &[i32]) -> i32 {
        *data.iter().max().unwrap_or(&0)
    }
}

impl Strategy for MinStrategy {
    fn execute(&self, data: &[i32]) -> i32 {
        *data.iter().min().unwrap_or(&0)
    }
}

// 接受策略作为参数
fn process_data(data: &[i32], strategy: &dyn Strategy) -> i32 {
    println!("使用策略处理数据: {:?}", data);
    let result = strategy.execute(data);
    println!("结果: {}", result);
    result
}

fn main() {
    let data = vec![1, 5, 3, 9, 2, 8];

    println!("=== 数据处理演示 ===");
    process_data(&data, &SumStrategy);
    println!();
    process_data(&data, &MaxStrategy);
    println!();
    process_data(&data, &MinStrategy);

    // 打印结果:
    // === 数据处理演示 ===
    // 使用策略处理数据: [1, 5, 3, 9, 2, 8]
    // 结果: 28
    //
    // 使用策略处理数据: [1, 5, 3, 9, 2, 8]
    // 结果: 9
    //
    // 使用策略处理数据: [1, 5, 3, 9, 2, 8]
    // 结果: 1
}
```

### 5.3.3 静态分发 vs 动态分发

Rust 同时支持两种分发方式，各有优劣。

#### 5.3.3.1 泛型 <T: Trait>

泛型约束使用**静态分发**：编译器为每种具体类型生成专门的代码。

```rust
trait Animal {
    fn speak(&self) -> String;
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn speak(&self) -> String {
        "汪！".to_string()
    }
}

impl Animal for Cat {
    fn speak(&self) -> String {
        "喵~".to_string()
    }
}

// 静态分发：泛型函数
fn animal_speak<T: Animal>(animal: &T) {
    println!("{}", animal.speak());
}

fn main() {
    let dog = Dog;
    let cat = Cat;

    animal_speak(&dog);
    animal_speak(&cat);

    // 编译后实际上有两份 animal_speak 函数：
    // - animal_speak::<Dog>
    // - animal_speak::<Cat>

    // 打印结果:
    // 汪！
    // 喵~
}
```

#### 5.3.3.2 dyn Trait

dyn Trait 使用**动态分发**：运行时通过 vtable 查找方法。

```rust
// 动态分发：trait 对象
fn animal_speak_dynamic(animal: &dyn Animal) {
    println!("{}", animal.speak());
}

fn main() {
    let dog = Dog;
    let cat = Cat;

    animal_speak_dynamic(&dog);
    animal_speak_dynamic(&cat);

    // 编译后只有一份函数，通过 vtable 调用

    // 打印结果:
    // 汪！
    // 喵~
}
```

#### 5.3.3.3 何时选择

```text
选择静态分发（泛型 <T: Trait>）的场景：
✓ 编译时知道具体类型
✓ 性能关键，零运行时开销
✓ 需要内联优化
✓ 同类型集合（Vec<T> 而非 Vec<&dyn T>）

选择动态分发（dyn Trait）的场景：
✓ 需要异构集合
✓ 运行时才知道类型
✓ 需要减少编译后代码大小（泛型会生成多份代码）
✓ 插件系统、回调、策略模式
✓ 暴露 C API（dyn Trait 更适合跨语言边界）
```

```rust
use std::time::Instant;

trait Compute {
    fn run(&self) -> u64;
}

struct HeavyComputation;
struct LightComputation;

impl Compute for HeavyComputation {
    fn run(&self) -> u64 {
        // 模拟耗时计算
        (0..1_000_000).map(|x| x * x).sum::<u64>() as u64
    }
}

impl Compute for LightComputation {
    fn run(&self) -> u64 {
        42
    }
}

// 静态分发版本
fn static_compute<C: Compute>(c: &C) -> u64 {
    c.run()
}

// 动态分发版本
fn dynamic_compute(c: &dyn Compute) -> u64 {
    c.run()
}

fn main() {
    let heavy = HeavyComputation;

    // 性能对比
    let start = Instant::now();
    for _ in 0..1000 {
        static_compute(&heavy);
    }
    println!("静态分发耗时: {:?}", start.elapsed());

    let start = Instant::now();
    for _ in 0..1000 {
        dynamic_compute(&heavy);
    }
    println!("动态分发耗时: {:?}", start.elapsed());

    // 动态分发通常稍慢一点（vtable 查找开销）
    // 但在实际应用中，这个差距通常可以忽略
}
```

### 5.3.4 Box<dyn Trait> 与 &dyn Trait

trait 对象可以有不同的"包装"形式，每种形式有不同的所有权语义。

#### 5.3.4.1 Box<dyn Trait>

`Box<dyn Trait>` 把 trait 对象放在堆上，整个值拥有所有权。

```rust
trait Drawable {
    fn draw(&self);
}

struct Circle { x: f64, y: f64, radius: f64 }
struct Square { x: f64, y: f64, side: f64 }

impl Drawable for Circle {
    fn draw(&self) {
        println!("绘制圆形: 圆心({},{}), 半径{}", self.x, self.y, self.radius);
    }
}

impl Drawable for Square {
    fn draw(&self) {
        println!("绘制正方形: 左上角({},{}), 边长{}", self.x, self.y, self.side);
    }
}

fn render(shape: Box<dyn Drawable>) {
    // Box<dyn Drawable> 拥有所有权
    shape.draw();
}

fn main() {
    // 创建堆分配的 trait 对象
    let circle = Box::new(Circle { x: 0.0, y: 0.0, radius: 1.0 });
    let square = Box::new(Square { x: 1.0, y: 1.0, side: 2.0 });

    render(circle);   // 所有权转移给 render，circle 在这里被消耗
    // render(square);  // 如果取消注释，square 也被移动，但 circle 已经在上面被消耗了

    // 注意：render 消耗（move）它的参数，所以每个 Box<dyn Drawable>只能用一次

    // 打印结果:
    // 绘制圆形: 圆心(0,0), 半径1
}
```

#### 5.3.4.2 &dyn Trait

`&dyn Trait` 是借用 trait 对象，不获取所有权。

```rust
fn describe(shape: &dyn Drawable) {
    // 只借用，不需要所有权
    shape.draw();
}

fn main() {
    let circle = Circle { x: 0.0, y: 0.0, radius: 1.0 };
    let square = Square { x: 1.0, y: 1.0, side: 2.0 };

    // 借用
    describe(&circle);
    describe(&square);

    // 借用后，原对象还能用
    println!("圆形还在: {:?}", circle.radius);

    // 打印结果:
    // 绘制圆形: 圆心(0,0), 半径1
    // 绘制正方形: 左上角(1,1), 边长2
    // 圆形还在: 1.0
}
```

#### 5.3.4.3 Arc<dyn Trait>

`Arc<dyn Trait>` 用于多所有权场景：多个线程/模块需要共享同一个 trait 对象。

```rust
use std::sync::Arc;
use std::thread;

trait Task {
    fn execute(&self);
}

struct BackgroundTask { name: String }
struct LightTask { name: String }

impl Task for BackgroundTask {
    fn execute(&self) {
        println!("执行后台任务: {}", self.name);
    }
}

impl Task for LightTask {
    fn execute(&self) {
        println!("执行轻量任务: {}", self.name);
    }
}

fn main() {
    // 创建 Arc 包装的 trait 对象
    let task1 = Arc::new(BackgroundTask { name: "数据备份".to_string() });
    let task2 = Arc::new(LightTask { name: "日志清理".to_string() });

    // 在多个线程中使用（简化示例，单线程模拟多线程）
    let t1 = task1.clone();
    let t2 = task2.clone();

    // 模拟线程1
    println!("线程1开始");
    t1.execute();

    // 模拟线程2
    println!("线程2开始");
    t2.execute();

    // task1 和 task2 还能用（Arc 的所有权）
    println!("任务完成");

    // 打印结果:
    // 线程1开始
    // 执行后台任务: 数据备份
    // 线程2开始
    // 执行轻量任务: 日志清理
    // 任务完成
}
```

### 5.3.5 对象安全（Object Safety）

不是所有的 trait 都可以作为 trait 对象。只有"对象安全（Object Safe）"的 trait 才能被用作 `dyn Trait`。这是因为 trait 对象缺少具体类型信息，某些方法无法在运行时调用。

#### 5.3.5.1 对象安全规则

一个 trait 是对象安全的条件：
1. **所有方法都是对象安全的**
2. trait 本身不能有泛型方法
3. 不能返回 `Self`

**方法对象安全的要求：**
- 不能有泛型参数 `<T>`
- 如果返回 `Self`，不能在 `&self` 方法中返回（但在 `&mut self` 或 `static` 方法中可以）

```rust
// 这个 trait 是对象安全的
trait Safe {
    fn method(&self);
    fn another(&self) -> i32;
}

// 这个 trait 不是对象安全的
trait NotSafe: Clone {
    fn generic_method<T>(&self, value: T);  // 泛型方法
    // fn returns_self(&self) -> Self;  // 返回 Self
}
```

#### 5.3.5.2 返回 Self 的方法

返回 `Self` 的方法在 trait 对象中是有问题的，因为 trait 对象不知道 `Self` 的具体类型。

```rust
// 这个 trait 不能作为 dyn Trait
trait Clonable {
    fn clone(&self) -> Self;  // 返回 Self
}

// 原因：Box<dyn Clonable>.clone() 返回什么类型？Box<dyn Clonable>？

// 但标准库的 Clone trait 为什么可以？答案在于：
// Clone trait 有隐式的 Sized 约束：Clone: Sized
// 这意味着 Clone trait 不能用于 dyn Trait
// Rust 特殊处理了 Clone，让它可以显式地调用 .clone()，但不能作为 trait 对象
```

```rust
// 正确的设计：使用泛型或关联类型
trait Factory {
    type Product;

    fn create(&self) -> Self::Product;
}

trait Serializer {
    fn serialize(&self) -> Vec<u8>;
}

// 这两个都是对象安全的
struct MyData { value: i32 }

impl Factory for MyData {
    type Product = Self;
    fn create(&self) -> Self::Product {
        MyData { value: self.value }
    }
}

impl Serializer for MyData {
    fn serialize(&self) -> Vec<u8> {
        format!("{}", self.value).into_bytes()
    }
}

fn main() {
    // dyn Factory 是可以的（虽然不常用）
    let data: &dyn Factory<Product = MyData> = &MyData { value: 42 };
    let new_data = data.create();
    println!("创建: {:?}", new_data.value);

    // dyn Serializer 更常见
    let ser: &dyn Serializer = &MyData { value: 42 };
    let bytes = ser.serialize();
    println!("序列化: {:?}", bytes);

    // 打印结果:
    // 创建: 42
    // 序列化: [52, 50]
}
```

#### 5.3.5.3 泛型方法

泛型方法让 trait 无法成为 trait 对象，因为泛型在编译时需要单态化，但 trait 对象运行时才知道具体类型。

```rust
// 这个 trait 不是对象安全的
trait Generic {
    fn process<T>(&self, value: T);
}

// 尝试创建 dyn Generic 会失败
// let _: Box<dyn Generic>;  // 编译错误！

// 但如果你真的需要泛型行为，可以这样：
trait Flexible {
    fn process_boxed(&self, value: Box<dyn std::any::Any>);
}

struct Handler;

impl Flexible for Handler {
    fn process_boxed(&self, value: Box<dyn std::any::Any>) {
        // 可以尝试 downcast
        if let Ok(n) = value.downcast_ref::<i32>() {
            println!("收到 i32: {}", n);
        } else if let Ok(s) = value.downcast_ref::<String>() {
            println!("收到 String: {}", s);
        }
    }
}

fn main() {
    let handler = Handler;
    handler.process_boxed(Box::new(42_i32));
    handler.process_boxed(Box::new("hello".to_string()));

    // 打印结果:
    // 收到 i32: 42
    // 收到 String: hello
}
```

## 本章小结

本章我们深入学习了 Rust 的 trait 系统：

- **Trait 基础**：trait 是 Rust 版的"接口"，定义行为规范，由具体类型来实现
- **Trait 约束与静态分发**：泛型约束 `<T: Trait>` 和 `where T: Trait` 实现编译时静态分发
- **默认方法实现**：trait 可以提供默认方法实现，实现者可以选择覆盖或使用默认
- **Trait 继承**：子 trait 继承父 trait，实现子 trait 必须同时实现所有父 trait
- **孤儿规则**：为类型实现 trait 需要类型或 trait 至少有一个是本地定义的
- **标准库常用 Trait**：Debug、Display、Clone、Copy、Drop、Default、From/Into、AsRef/AsMut、Borrow/BorrowMut、Eq/PartialEq、Ord/PartialOrd、Hash、ToOwned、Iterator、IntoIterator、Fn/FnMut/FnOnce
- **Trait 对象与动态分发**：`dyn Trait` 实现运行时多态，通过 vtable 查找方法
- **对象安全**：只有对象安全的 trait 才能作为 dyn Trait

Trait 是 Rust 类型系统的灵魂，掌握它你就能写出优雅、灵活、类型安全的代码！
