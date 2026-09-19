+++
title = "继承"
date = 2026-09-19T12:00:00+08:00
weight = 14
type = "docs"
description = "18 种语言的继承对照：继承与子类型、覆盖与多态、无继承语言的复用方式、继承的经典陷阱"
isCJKLanguage = true
draft = false
+++

# 继承：18 种语言对照

继承在大多数教材里被当成面向对象的起点，但 18 门语言给出的答案是分裂的：Java、C#、Kotlin、Swift、Dart、PHP、Ruby 只允许单继承并用接口或 mixin 补足横向复用，C++ 允许真正的多继承（并因此背上菱形与虚继承），Python 允许类多继承但要靠 MRO 线性化，而 Rust、Go、Julia、Zig、C、Lua、R 干脆没有继承关键字，各自用 trait、嵌入、多分派、组合、元表和泛型函数解决问题。本页因此按三条线索组织：先看**继承与子类型**（谁有继承、谁只有子类型关系），再看**覆盖与多态**（`virtual`/`override`/`final`/`sealed` 的完整矩阵与派发机制），然后看**没有继承的语言怎么复用**（这才是多数现代语言的实际做法），最后集中记录**继承的陷阱**——脆弱基类、菱形、对象切片、构造期调用被覆盖方法、`equals`/`hashCode` 契约破坏等。理解这四组差异之后，语言选型时"要不要给类开 `open`"这类问题就不再是口味问题，而是可推演的工程判断。

## 继承

**一页速览**

| 语言 | 有没有继承 / 关键字写法 | 一句话说明 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | 没有 | `trait` + `impl Trait for Type`，`dyn Trait` 做动态派发 | 没有字段继承，只有行为共享；`dyn` 是胖指针 |
| Swift | 有：单继承 | `class Sub: Base`、`override`、`final`、协议 | 值类型（`struct`/`enum`）不能继承，只有 `class` 能 |
| Go | 没有 | 结构体嵌入（embedding）提升字段与方法，接口是隐式实现 | 嵌入是组合不是继承，没有虚表，遮蔽 ≠ 覆盖 |
| Python | 有：多继承 | `class Sub(Base1, Base2)` + MRO 线性化，`super()` 协作 | MRO 顺序依赖、菱形、`super()` 在非协作体系里会断链 |
| Kotlin | 有：单继承 | `open class`、`override`、`final`（默认）、`sealed`、`by` 委托 | 类与成员默认 `final`，忘了 `open` 就编译不过 |
| Java | 有：单继承 + 接口 | `extends`、`implements`、`abstract`、`final`、`sealed`（17 起） | 基类构造期调用被覆盖方法会读到未初始化字段 |
| C++ | 有：多继承 | `class D : public B`、`virtual`、`override`、`final`、纯虚函数 | 对象切片、菱形继承要虚继承、`class` 默认私有继承 |
| C | 没有 | 结构体首成员模拟布局，函数指针表手工构造 vtable | 没有 RTTI 与自动派发，转型全靠约定与强制转换 |
| Julia | 没有 | `abstract type` + `struct <: T` 给子类型关系，行为靠多分派 | 子类型只约束方法签名，不继承字段与实现 |
| C# | 有：单继承 + 接口 | `class D : B, I`、`virtual`、`override`、`sealed`、默认接口实现（8 起） | `struct` 不能继承；方法默认非虚；`new` 是遮蔽不是覆盖 |
| Dart | 有：单继承 + mixin | `extends`、`implements`、`with`、`sealed`（3.0 class modifiers） | 每个类都隐式是接口；`mixin` 线性化顺序决定覆盖结果 |
| R | 没有 | S3 用 `class()`/`UseMethod`，S4 用 `setClass`/`setGeneric`，R6 用 `R6Class` | S3 没有结构校验，`NextMethod` 分派靠 `class` 向量顺序 |
| Zig | 没有 | 组合 + `comptime` 生成，接口靠手工 vtable（如 `std.mem.Allocator`） | 没有隐式派发，所有函数指针都要自己填 |
| Lua | 没有 | 元表 `__index` 构成原型链，`setmetatable` 手工搭继承 | 只有表与元方法，没有编译期检查，拼错字段名不报错 |
| TypeScript | 有：类的单继承 | `extends`、`implements`、`abstract`、声明合并 | 类型只在编译期，运行时仍是 JS 原型；`private` 可绕过 |
| JavaScript | 有：原型链单继承 | `class`/`extends`/`super`/`instanceof`，底层是 `[[Prototype]]` | 没有接口；方法在原型上；改原型会影响所有实例 |
| PHP | 有：单继承 + 接口 + trait | `extends`、`implements`、`trait` + `use` | 无多继承；trait 冲突要 `insteadof`/`as`；方法默认非虚 |
| Ruby | 有：单继承 + module | `<`、`include`、`extend`、`prepend`、`module` | 祖先链与 `prepend` 顺序决定结果；没有多继承 |

本表合计 18 行，统计口径为「该语言是否提供把实现一并复用的类继承关键字」：**有类继承的 11 门**是 Swift、Python、Kotlin、Java、C++、C#、Dart、TypeScript、JavaScript、PHP、Ruby，**没有类继承的 7 门**是 Rust、Go、C、Julia、R、Zig、Lua；其中只有 C++ 与 Python 支持一个类有多个父类，其余 9 门有继承语言都是「单继承 + 接口/协议/mixin」，Rust、Go、Julia 另有不涉及继承的子类型关系（`trait`、接口、抽象类型）。

### 继承与子类型

继承是几乎每门语言都给它"打了折"的机制：有的语言砍掉多继承，有的语言把它换成 trait 或嵌入，还有的语言干脆只保留子类型关系而删掉实现复用。这一节逐语言给出**有没有继承、关键字怎么写、子类型关系怎么建立**三个答案。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有类、没有继承、也没有子类型多态意义上的父类指针：结构体之间不能互相转换，字段也不可能被"继承"复用。它把继承要解决的两件事拆开了——**行为的多态**交给 `trait` 与 `dyn Trait`（运行时派发）或泛型（编译期单态化），**数据的复用**交给组合与结构体嵌入字段。这一节最该先记住：`impl Trait for Type` 是"这个类型支持这套行为"，而不是"这个类型是那个类型的子类"。

```rust
trait Shape {                       // trait 只描述行为，不含字段
    fn area(&self) -> f64;
    fn name(&self) -> String {      // 默认方法：trait 提供实现
        format!("shape({:.1})", self.area())
    }
}

struct Circle { r: f64 }
struct Square { side: f64 }

impl Shape for Circle {             // 一个类型可以 impl 任意多个 trait
    fn area(&self) -> f64 { 3.0 * self.r * self.r }
}
impl Shape for Square {
    fn area(&self) -> f64 { self.side * self.side }
}

fn total(shapes: &[Box<dyn Shape>]) -> f64 {   // trait 对象：动态派发
    shapes.iter().map(|s| s.area()).sum()
}

fn main() {
    let c = Circle { r: 2.0 };
    println!("{}", c.name());       // shape(12.0)
    let v: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { r: 2.0 }),
        Box::new(Square { side: 3.0 }),
    ];
    println!("{:.1}", total(&v));   // 21.0
    println!("{}", std::mem::size_of::<&dyn Shape>());  // 16：数据指针 + vtable 指针
}
```

字段复用只能靠组合：把公共字段抽成一个结构体，再放进各个结构体里，需要访问就显式转发或实现 `Deref`。`dyn Trait` 是胖指针（16 字节，包含数据指针与 vtable 指针），`Box<dyn Trait>`、`&dyn Trait` 都是如此；要向下转型就要求 `trait Any` 并用 `downcast_ref`，Rust 不会替你猜。泛型参数 `T: Shape` 则相反：单态化为每种具体类型生成一份代码，零运行时开销但代码膨胀。选择的判据很实际——集合里放不同实现用 `dyn`，只有一两种实现且在乎性能用泛型，只是想复用代码就直接组合函数。

📘 [Rust · Object Oriented Programming Features](https://doc.rust-lang.org/book/ch18-00-oop.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的继承只属于 `class`，而且是单继承：`class Sub: Base`，`struct`、`enum`、`actor` 都是值语义，不能继承也不被继承。类实例是引用类型，赋值与传参共享同一个对象；协议（`protocol`）负责跨类型的行为约定，`struct` 与 `enum` 通过遵循协议参与多态，这就构成了 Swift 里"继承管引用类型、协议管一切类型"的分工。

```swift
class Animal {
    var name: String
    init(name: String) { self.name = name }
    func speak() -> String { "..." }        // 类方法默认可被覆盖
    final func id() -> String { "animal:\(name)" }   // final 禁止覆盖
}

class Dog: Animal {
    override func speak() -> String { "Woof" }       // 必须写 override
}

protocol Shape {                            // 协议：struct 也能遵循
    func area() -> Double
}
extension Shape {                           // 协议扩展提供默认实现
    func describe() -> String { "area=\(area())" }
}
struct Circle: Shape {
    var r: Double
    func area() -> Double { 3.0 * r * r }
}

let animals: [Animal] = [Animal(name: "x"), Dog(name: "Rex")]
print(animals[1].speak())                  // Woof
print(animals[0].speak())                  // ...
let shapes: [any Shape] = [Circle(r: 2.0)] // existential：写成 any Shape 更清楚（ExistentialAny）
print(shapes[0].describe())                // area=12.0
print(Dog(name: "Rex").id())               // animal:Rex
```

`class` 实例通过 vtable 动态派发，`final` 或 `private` 的方法可以被静态派发（`whole-module` 优化下甚至能内联），这是 `final` 在性能之外的设计理由。协议作为类型使用时应该写成 `any Shape`（existential type）：`any` 语法自 Swift 5.6 起可用，Swift 5.8 起可以打开 upcoming feature `ExistentialAny` 把"裸协议名当类型"变成编译警告（`use of protocol 'Shape' as a type must be written 'any Shape'`），并计划在未来的语言模式里升级为错误——Swift 6.4 的默认语言模式下它仍然只是警告，所以别把 `any` 当成"不写就编译不过"；`some Shape` 则是不透明类型，编译期就确定了唯一的底层类型，没有装箱开销。陷阱集中在初始化：`init` 里调用可被覆盖的方法时，子类的字段还没初始化，Swift 编译器会直接拒绝这种写法（在 `super.init` 之前不能调用实例方法），这比 Java、C# 安全。需要在类之间横向复用代码时，用协议扩展而不是深继承。

📘 [Swift · Inheritance](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/inheritance/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 明确没有继承，也没有 `extends`/`super` 这类关键字，官方的说法是"用组合代替继承"。它提供的两个近似物是**结构体嵌入**（embedding，匿名字段，字段与方法被提升到外层）和**接口**（隐式实现，任何类型只要方法集匹配就自动满足接口）。先记住最反直觉的一点：嵌入不是继承，`Dog` 嵌入 `Animal` 不等于 `Dog` 是 `Animal` 的子类型，两者之间的转换必须显式取字段。

```go
package main

import "fmt"

type Animal struct{ Name string }

func (a Animal) Speak() string { return "..." }

type Dog struct {
	Animal                  // 匿名字段：嵌入
	Breed  string
}

func (d Dog) Speak() string { return "Woof" } // 遮蔽外层提升的方法（不是 override）

type Speaker interface{ Speak() string }      // 接口：隐式实现

func main() {
	d := Dog{Animal{Name: "Rex"}, "poodle"}
	fmt.Println(d.Speak())        // Woof：Dog 自己的方法优先
	fmt.Println(d.Animal.Speak()) // ...：显式调回被遮蔽的方法
	fmt.Println(d.Name)           // Rex：字段被提升

	var s Speaker = d             // Dog 的方法集包含 Speak，自动满足接口
	fmt.Println(s.Speak())        // Woof

	fmt.Println(interface{}(d.Animal) == interface{}(d)) // false：Animal 与 Dog 无关
}
```

嵌入的规则要记牢：外层类型的方法集包含内层类型的方法（值接收者提升到值方法集，指针接收者只提升到指针方法集），字段可以像自己的一样用 `d.Name` 访问，但编译器只是帮你写成了 `d.Animal.Name`。遮蔽不是覆盖——通过 `Animal` 类型的变量调用 `Speak` 永远得到 `Animal` 的实现，因为没有 vtable，方法在编译期就确定以哪个接收者调用。接口是 Go 唯一的运行时多态：接口值内部是（类型, 数据）二元组，赋值时才做方法集检查。因此 Go 的复用方式是：共享字段用嵌入，共享行为用接口加小函数，需要"模板方法"时把可变部分作为函数字段或接口参数传入，而不是留一个可覆盖的钩子。

📘 [Go spec · Struct types](https://go.dev/ref/spec#Struct_types) ｜ 📘 [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)

{{% /tab %}}

{{% tab header="Python" %}}

Python 有真正的类多继承，语法是 `class Sub(Base1, Base2)`，所有类最终都继承自 `object`。方法解析靠 C3 线性化算出的 MRO（Method Resolution Order），可以用 `Sub.__mro__` 直接检查。它属于纯运行时的动态机制：属性查找在每次访问时沿 MRO 进行，没有任何编译期检查，也没有 `private` 强制。

```python
class Animal:
    def speak(self) -> str:
        return "..."

class SwimMixin:                       # mixin：只提供一组方法，不打算独立实例化
    def swim(self) -> str:
        return "swimming"

class Duck(Animal, SwimMixin):         # 多继承：MRO 决定查找顺序
    pass

print(Duck().speak())                  # ...
print([c.__name__ for c in Duck.__mro__])  # ['Duck', 'Animal', 'SwimMixin', 'object']
print(Duck().swim())                   # swimming

class Base:
    def hello(self) -> str:
        return "base"
class Mid(Base):
    def hello(self) -> str:
        return "mid+" + super().hello()   # 协作式 super：沿 MRO 往下走
class Leaf(Mid):
    def hello(self) -> str:
        return "leaf+" + super().hello()
print(Leaf().hello())                  # leaf+mid+base

class Sq2(Base):                        # 继承 Base 即可复用 hello
    pass
print(issubclass(Sq2, Base), isinstance(Sq2(), Base))  # True True
```

MRO 的规则是"子类优先、声明顺序在左的优先、单调性"，`super()` 不是"调用父类"，而是"调用 MRO 上的下一个类"，所以它只有在所有类都协作调用 `super()` 时才能串成链；混入的类如果直接写 `Base.hello(self)`，就会破坏链并可能重复执行。没有 ABC 时多继承还可以用来做 mixin（`SwimMixin` 这类只提供方法、不单独实例化的类），这是 Python 里最常见的横向复用方式。子类型关系靠 `issubclass`/`isinstance` 在运行时检查，鸭子类型则连这层关系都不需要；要做接口约束就用 `abc.ABC` + `@abstractmethod` 或 `typing.Protocol`（结构化子类型，`@runtime_checkable` 才能 `isinstance`）。

📘 [Python · 类与 MRO](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的类默认是 `final` 的：要允许继承必须显式写 `open class`，成员方法也默认 `final`，可覆盖的成员要标 `open`，覆盖时必须写 `override`。继承限定为单继承（`: Base()`），横向复用靠接口、接口默认实现和 `by` 委托。这套"默认封闭"的设计是为了避免 Java 里那种"类被无意继承、方法被无意覆盖"的脆弱基类问题。

```kotlin
open class Animal(val name: String) {      // open 才可被继承
    open fun speak(): String = "..."       // open 才可被覆盖
    fun id(): String = "animal:$name"      // 默认 final，子类不能碰
}

class Dog(name: String) : Animal(name) {   // 单继承，冒号后调用父构造器
    override fun speak(): String = "Woof"  // 必须写 override
}

interface Shape {                          // 接口可以有默认实现
    fun area(): Double
    fun describe(): String = "area=${area()}"
}

class Circle(val r: Double) : Shape {
    override fun area(): Double = 3.0 * r * r
}

interface Named { val label: String }
class Tagged(val label0: String) : Named by TaggedLabel(label0)   // 接口委托

class TaggedLabel(private val s: String) : Named {                 // 委托实现体
    override val label: String = "tag:$s"
}

fun main() {
    val animals: List<Animal> = listOf(Animal("x"), Dog("Rex"))
    println(animals[1].speak())       // Woof
    println((animals[1] as Animal).id())  // animal:Rex
    println(Circle(2.0).describe())   // area=12.0
    val t: Named = Tagged("a")
    println(t.label)                  // tag:a
    val x: Animal = Dog("Rex")
    println(x is Animal)              // true
    val s: Shape = Circle(1.0)
    println(s is Shape)               // true
}
```

`open`/`override`/`final` 三件套是 Kotlin 继承的全部开关：`open` 打开继承，`override` 声明覆盖（覆盖后的成员默认仍是开放的，要禁止继续覆盖就写 `final override`），`final` 关掉继承。`sealed class`/`sealed interface` 把子类限定在同一模块与同一包内，配合 `when` 可以做穷尽性检查。接口可以有属性与默认方法，多个接口的默认实现冲突时必须显式覆盖并用 `super<A>.f()` 消歧。`by` 委托把接口实现转发给另一个对象，是 Kotlin 特有的"组合优于继承"写法——编译期生成转发代码，不去改祖先链。Kotlin 里没有多继承，也没有菱形问题。

📘 [Kotlin · Inheritance](https://kotlinlang.org/docs/inheritance.html) ｜ 📘 [Kotlin · Delegation](https://kotlinlang.org/docs/delegation.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的类继承是单继承：`class Sub extends Base`，一个类只能有一个直接父类，但可以实现任意多个接口（`implements A, B`）。接口从 Java 8 起能有 `default`/`static` 方法，Java 9 起能有 `private` 方法，因此"接口只声明不实现"的旧印象已经过时。类型系统里所有引用类型都隐式继承 `Object`。

```java
class Animal {
    protected final String name;
    Animal(String name) { this.name = name; }
    String speak() { return "..."; }                 // 默认可覆盖
    final String id() { return "animal:" + name; }   // final 禁止覆盖
}

class Dog extends Animal {                            // 单继承
    Dog(String name) { super(name); }
    @Override String speak() { return "Woof"; }       // 注解帮编译器检查
}

interface Shape {                                     // 接口
    double area();
    default String describe() { return "area=" + area(); }   // Java 8 默认方法
}
interface Named { String label(); }

class Circle implements Shape, Named {                // 多接口
    private final double r;
    Circle(double r) { this.r = r; }
    public double area() { return 3.0 * r * r; }
    public String label() { return "circle"; }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog("Rex");
        System.out.println(a.speak());          // Woof：动态派发
        System.out.println(a.id());             // animal:Rex
        System.out.println(a instanceof Dog);   // true
        Shape s = new Circle(2.0);
        System.out.println(s.describe());       // area=12.0
        System.out.println(s instanceof Named); // true：同一对象多接口
    }
}
```

`extends` 表达"是一个"，`implements` 表达"能做这些事"，这是 Java 里选择继承还是接口的基本判据。所有非 `static`、非 `final`、非 `private` 的方法都是虚方法，调用点通过 vtable（JVM 的 invokevirtual）派发，`final` 与 `private` 方法可以被静态绑定或内联。Java 17 起有 `sealed`/`permits`：`sealed interface Shape permits Circle, Square` 限定实现者集合，配合 `switch` 模式匹配可以做穷尽性检查（Java 21 的模式匹配 switch）。Java 16 起的 `record` 是隐式 `final` 的，不能继承也不被继承，天然适合做 sealed 层级的叶子节点。接口的默认方法只在需要"给已有接口加方法而不破坏实现类"时才是正确工具，它不引入状态（不能有实例字段），这个限制恰好避免了多继承的菱形状态问题，但默认方法之间的冲突仍要显式覆盖消解。

📘 [Java · Inheritance](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html) ｜ 📘 [JLS · Sealed Classes](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.1.1.2)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有真正的多继承：`class D : public B1, public B2`，而且 `class` 的默认继承是 **private**，只有 `struct` 的默认继承才是 public，这是 C++ 最容易被绊倒的语法细节之一。它同时是唯一同时拥有值语义、多继承和虚继承的主流语言，因此对象布局、切片、菱形这些问题在 C++ 里最尖锐。

```cpp
#include <iostream>
#include <string>

struct Base {                                  // struct 默认 public 继承、public 成员
    virtual ~Base() = default;                 // 多态基类必须有虚析构
    virtual std::string name() const { return "Base"; }
    int tag = 0;
};

struct Derived : Base {                        // 等价于 public Base
    std::string name() const override { return "Derived"; }
    int extra = 1;
};

class PrivDerived : Base {                     // ⚠️ class 默认 private 继承
public:
    std::string name() const override { return "Priv"; }
};

int main() {
    Derived d;
    Base b = d;                                // ⚠️ 对象切片：extra 被切掉
    std::cout << b.name() << "\n";             // Base：不是 Derived
    Base& r = d;                               // 引用/指针才有多态
    std::cout << r.name() << "\n";             // Derived
    std::cout << sizeof(Base) << " " << sizeof(Derived) << "\n";  // 16 16：新增的 int 恰好吃掉尾部填充
    // Base* p = &d; 可以隐式转换；PrivDerived* -> Base* 在类外不可转换
}
```

多继承的语义是"合并多个基类子对象"，因此 `Derived*` 转 `Base*` 时编译器会自动加上偏移量，指针值可能改变（第二基类的地址与派生类地址不同）；`static_cast`/`dynamic_cast` 会处理偏移，`reinterpret_cast` 不会。为共享基类去重需要 `virtual` 继承（`struct D : virtual Base`），它让所有路径共享同一个 `Base` 子对象，代价是对象里多一个虚基类指针、布局更复杂、构造不能直接调用虚基类构造。C++ 里继承的另一个重要语义是访问控制：`public` 继承表达"是一个"（里氏替换成立），`private`/`protected` 继承只是实现复用（"用基类的实现来构造"，外部看不到子类型关系），Effective C++ 因此建议除非是 public 继承，否则优先用组合。多态基类还必须声明 `virtual ~Base()`，否则通过基类指针 `delete` 是未定义行为。

📘 [cppreference · Derived classes](https://en.cppreference.com/w/cpp/language/derived_class)

{{% /tab %}}

{{% tab header="C" %}}

C 没有继承、没有类、没有虚函数，唯一的结构化手段是 `struct`。但 C 用两个约定模拟出了继承：**首成员布局**（派生结构体把基类结构体放在第一个成员，于是两者的地址相同，指针可以互相转换）与**函数指针表**（把一组函数指针打包成 vtable，运行时按对象里的指针派发）。GTK 的 GObject、Linux 内核的 `struct file_operations` 都是这个套路。

```c
#include <stdio.h>

/* 基类：首成员是 vtable 指针 */
typedef struct Shape Shape;
typedef struct {
    double (*area)(const Shape *self);      /* 函数指针表 = 手工 vtable */
} ShapeVtbl;
struct Shape { const ShapeVtbl *vtbl; };

static double shape_area(const Shape *s) { (void)s; return 0.0; }
static const ShapeVtbl SHAPE_VTBL = { shape_area };

typedef struct { Shape base; double r; } Circle;   /* 基类必须是首成员 */

static double circle_area(const Shape *s) {
    const Circle *c = (const Circle *)s;    /* 向下转换靠布局约定，不检查 */
    return 3.0 * c->r * c->r;
}
static const ShapeVtbl CIRCLE_VTBL = { circle_area };

static double total(Shape *const *xs, int n) {     /* 多态派发 */
    double sum = 0;
    for (int i = 0; i < n; i++) sum += xs[i]->vtbl->area(xs[i]);
    return sum;
}

int main(void) {
    Circle c = { { &CIRCLE_VTBL }, 2.0 };
    Shape s = { &SHAPE_VTBL };
    Shape *xs[2] = { &c.base, &s };                /* &c 与 &c.base 地址相同 */
    printf("%.1f\n", total(xs, 2));                /* 12.0 */
    printf("%d\n", (void *)&c == (void *)&c.base); /* 1：首成员地址相同 */
    return 0;
}
```

约定只有两条却很容易踩：基类子对象必须是派生结构的**第一个**成员（否则指针转换要手工加偏移），以及必须自己保证 `vtbl` 指向正确的表——C 不会替你填，也不会检查你把 `Shape*` 转回 `Circle*` 时类型是否正确，写错了就是未定义行为而不是异常。`total()` 里对每个元素做一次间接调用，这就是 C 里唯一的动态派发形式，与 C++ 的 vtable 相比少了 RTTI、`dynamic_cast` 和自动析构：`Shape*` 上调用 `delete` 不会触发 `Circle` 的清理逻辑，资源释放必须靠显式的 `destroy` 函数放进 vtable。因此 C 的"继承"更适合用在插件接口、IO 抽象这类生命周期由框架统一管理的场景，别用它模拟完整的对象模型。

📘 [C · struct 与成员访问](https://en.cppreference.com/w/c/language/struct)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 没有类、没有继承、也没有方法归属对象的语法。它把面向对象的两个组成拆成了两个独立系统：**类型层次**用 `abstract type` 与 `struct <: 父类型` 表达（只表达"是什么"，不携带字段与实现），**行为**用多重分派的方法表达（`f(x::Dog)` 比 `f(x::Animal)` 更具体就自动被选中）。因此 Julia 有子类型关系，但没有实现继承。

```julia
abstract type Animal end              # 抽象类型：只能当父类型，不能实例化
struct Dog <: Animal                  # 具体结构体声明子类型关系
    name::String
end
struct Cat <: Animal
    name::String
end

speak(::Animal) = "..."               # 泛型函数的一个方法
speak(d::Dog) = "Woof $(d.name)"      # 更具体的方法，自动优先
speak(c::Cat) = "Meow $(c.name)"

struct Robot end                      # 与 Animal 无子类型关系

describe(x) = "$(typeof(x)): $(speak(x))"   # 动态派发发生在调用时
describe(::Robot) = "robot: no speak"       # 为 Robot 单独定义，避免报错

a::Animal = Dog("Rex")                # ✅ 子类型可赋给父类型变量
println(speak(a))                     # Woof Rex：按运行时类型选方法
println(a isa Animal)                 # true
println(Dog <: Animal, Cat <: Animal) # true true
println(describe(Robot()))            # robot: no speak
# struct Bad <: Dog end               # 🛑 具体类型不能当父类型
println(methods(speak))               # 3 个方法
```

子类型在 Julia 里只做两件事：约束变量与容器（`Vector{Animal}` 能装 `Dog`），以及参与方法选择的特异性排序。字段不会被继承——`Dog` 与 `Cat` 各自声明 `name` 字段，抽象类型 `Animal` 里根本没有字段；如果想让所有子类型都有某个字段，得定义一个 `abstract type` 加接口约定（例如要求实现 `name(x)`），或者让各个具体类型嵌一个共享的结构体字段。`abstract type` 只能出现在类型层次的上层，具体 `struct` 不能作为父类型，所以 Julia 没有"类继承"这个词可用。运行时派发由 JIT 编译的方法表完成：调用 `speak(a)` 时按 `a` 的实际类型查表，命中具体方法就内联，这也是 Julia 所谓"多次派发"的性能来源；`Robot` 这种没有 `speak` 方法的类型只有在真正调用时才会抛 `MethodError`，编译期不检查。

📘 [Julia · Types](https://docs.julialang.org/en/v1/manual/types/) ｜ 📘 [Julia · Methods](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的类是单继承：`class Dog : Animal`，可以实现多个接口 `class Circle : Shape, Named`。两个必须记住的差异：**`struct` 不能继承**（值类型隐式继承 `System.ValueType`，不能有子类），以及**方法默认非虚**——不写 `virtual` 的方法不能用 `override` 覆盖，只能被 `new` 遮蔽。C# 8 起接口可以有默认实现，这让接口也能承担一部分 mixin 的职责。

```csharp
using System;

class Animal {
    protected readonly string Name;
    public Animal(string name) { Name = name; }
    public string Speak() => "...";              // 非虚：不能 override
    public virtual string Describe() => "animal:" + Name;   // virtual 才可覆盖
    public string Id() => "id:" + Name;
}

class Dog : Animal {                             // 单继承
    public Dog(string name) : base(name) { }
    public override string Describe() => "dog:" + Name;     // 覆盖
    public new string Speak() => "Woof";          // ⚠️ 遮蔽，不是覆盖
}

interface IShape {
    double Area();
    string Describe() => $"area={Area()}";        // C# 8 默认接口实现
}

class Circle : IShape {                           // 多接口
    private readonly double r;
    public Circle(double r) => this.r = r;
    public double Area() => 3.0 * r * r;
}

struct Point : IShape {                           // struct 不能继承类，但能实现接口
    public double Area() => 0.0;
}

class Program {
    static void Main() {
        Animal a = new Dog("Rex");
        Console.WriteLine(a.Describe());          // dog:Rex：虚方法派发
        Console.WriteLine(a.Speak());             // ...：静态绑定到 Animal.Speak
        Console.WriteLine(((Dog)a).Speak());      // Woof
        IShape s = new Circle(2.0);
        Console.WriteLine(s.Describe());          // area=12.0
        Console.WriteLine(new Point() is IShape); // True
    }
}
```

`virtual`/`override` 是覆盖，走 vtable 派发；`new` 是遮蔽，只在编译期按变量的静态类型选方法——上面 `a.Speak()` 得到 `...` 正是因为 `a` 的静态类型是 `Animal`，这是 C# 里最常见的"为什么我的方法没被调用"来源。`abstract` 成员必须被覆盖，`sealed override` 可以把某个覆盖点重新封死。默认接口实现（C# 8）只在通过接口类型调用时才可见，通过类的类型调用看不到它，而且接口不能声明实例字段，所以它不会带来菱形状态问题；它的定位是"给已发布的接口加成员而不破坏既有实现类"，不是让人拿接口当基类用。需要值语义的多态时，`struct` 走接口装箱，或者用 `record struct` 加接口。

📘 [C# · Inheritance](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance) ｜ 📘 [C# · Default interface methods](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interface-implementation/default-interface-methods-versions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的类体系是单继承加 mixin：`class Dog extends Animal` 表达继承，`with` 混入 mixin，`implements` 则把任意类的接口当作契约来实现。这里有一个经常被忽略的事实——**Dart 里每个类都隐式定义了一个接口**，所以 `implements Animal` 不要求 `Animal` 是抽象类，只是要求你实现它的全部实例成员。Dart 3.0 引入的 class modifiers（`base`、`interface`、`final`、`sealed`、`mixin`）把这层隐式约定变成了显式声明。

```dart
class Animal {
  final String name;
  Animal(this.name);
  String speak() => "...";               // 实例方法默认可被覆盖
}

class Dog extends Animal {               // 单继承
  Dog(super.name);
  @override
  String speak() => "Woof";
}

// mixin：用 on 限定可混入的父类型
mixin Swimmer on Animal {
  String swim() => "$name is swimming";
}

class Duck extends Animal with Swimmer { // with 线性化混入
  Duck(super.name);
}

// implements 实现的是隐式接口，不继承任何实现
class Robot implements Animal {
  @override
  final String name = "R2";
  @override
  String speak() => "beep";
}

void main() {
  final animals = <Animal>[Animal("x"), Dog("Rex")];
  print(animals[1].speak());              // Woof：动态派发
  print(animals[1] is Animal);            // true
  print(Duck("Donald").swim());           // Donald is swimming
  print(Robot() is Animal);               // false：implements 不建立继承关系
  print(Dog("Rex").runtimeType);          // Dog
}
```

`extends` 带实现并建立 `is` 关系，`implements` 只带契约、不建立 `is` 关系（所以 `Robot() is Animal` 是 `false`），`with` 把 mixin 的方法按书写顺序叠在父类之上。mixin 用 `on` 指定超类约束，从而可以调用 `name` 这样的成员；多个 mixin 有同名方法时，**靠后的 mixin 覆盖靠前的**，这就是 Dart 的线性化规则。Dart 3.0 的 modifier 让类可以声明自己的使用方式：`base class` 只允许被 `extends` 不允许被 `implements`，`interface class` 只允许被 `implements` 不允许被 `extends`，`final class` 禁止在本库之外继承或实现，`sealed class` 限定同库子类并让 `switch` 具备穷尽性，`mixin class` 既可以当类继承也可以当 mixin 混入。默认（无 modifier）的类既可以被继承也可以被实现，这正是 Dart 3 之前让库作者无法收窄 API 的原因。

📘 [Dart · Class modifiers](https://dart.dev/language/class-modifiers) ｜ 📘 [Dart · Inheritance](https://dart.dev/language/extend)

{{% /tab %}}

{{% tab header="R" %}}

R 没有 `class` 关键字，也没有继承语法，它有三套各自独立的面向对象系统：**S3**（最轻，靠 `class()` 属性加泛型函数 `UseMethod` 分派）、**S4**（正式，`setClass` 声明含类型校验的槽位，`setGeneric`/`setMethod` 定义分派）、**R5/R6**（引用语义，`R6::R6Class` 提供类似 Java 的封装）。三者都能表达"子类复用父类"，但没有一个用继承关键字。

```r
# ---- S3：class 属性 + UseMethod 分派 ----
new_animal <- function(name) structure(list(name = name), class = c("dog", "animal"))
speak <- function(x, ...) UseMethod("speak")          # 泛型函数
speak.animal <- function(x, ...) "..."                # 默认方法
speak.dog <- function(x, ...) paste("Woof", x$name)   # 更具体的方法
d <- new_animal("Rex")
print(speak(d))            # [1] "Woof Rex"
print(class(d))            # [1] "dog"    "animal"
print(inherits(d, "animal"))  # [1] TRUE

# ---- S4：正式类，含槽位类型校验 ----
setClass("Animal", representation(name = "character"))
setClass("Dog", contains = "Animal")                  # contains 表达继承
setGeneric("speak4", function(x) standardGeneric("speak4"))
setMethod("speak4", "Animal", function(x) "...")
setMethod("speak4", "Dog", function(x) paste("Woof", x@name))
print(speak4(new("Dog", name = "Rex")))   # [1] "Woof Rex"
print(is(new("Dog", name = "Rex"), "Animal"))  # [1] TRUE

# ---- R6：引用语义类（R5 的现代实现） ----
library(R6)
Animal6 <- R6Class("Animal6",
  public = list(name = NULL, initialize = function(name) self$name <- name,
                speak = function() "..."))
Dog6 <- R6Class("Dog6", inherit = Animal6,            # inherit 表达继承
  public = list(speak = function() paste("Woof", self$name)))
print(Dog6$new("Rex")$speak())            # [1] "Woof Rex"
```

S3 的继承完全由 `class` 属性的**字符串向量顺序**决定：`UseMethod` 依次在环境里查找 `speak.dog`、`speak.animal`、`speak.default`，找到就用；对象本身只是一个 list 或原子向量，没有任何结构校验，写错字段名不会报错。S4 把类定义变成正式对象（`setClass` 的 `representation` 校验槽位类型），`contains` 形成多重继承的名称层次，方法分派时按距离选最具体的；代价是样板代码多、调试信息晦涩。R6 用环境实现引用语义（`self` 可变、方法调用是 `obj$method()`），`inherit` 建立单继承，并带 `private`/`active` 绑定。做数据分析时最常见的取舍是：内部小工具用 S3，要给用户提供稳定 API 的包用 S4 或 R6；tidyverse 生态用 vctrs 把 S3 类做成"向量类"（`new_vctr`、`vec_ptype2`、`vec_cast`），从而拥有类型安全的子类与强制转换规则；`proto` 包则提供更传统的原型式对象。

📘 [R · S3 methods](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatching) ｜ 📘 [R6 · Reference classes](https://cran.r-project.org/web/packages/R6/index.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有继承、没有方法、没有隐式派发，也没有运行时类型信息。它的复用方式只有两种：**结构体组合**（把一个结构体当字段放进另一个）和 **`comptime` 生成**（用函数在编译期构造类型，把"模板方法"变成参数）。需要多态时，Zig 的标准做法是让接口持有数据指针与一组函数指针（`std.mem.Allocator` 就是这个形状），也就是手工装配 vtable。

```zig
const std = @import("std");

const Shape = struct {
    ptr: *anyopaque,                       // 类型擦除的数据指针
    vtable: *const VTable,

    const VTable = struct {
        area: *const fn (ptr: *anyopaque) f64,
    };

    fn area(self: Shape) f64 {             // 统一入口，手工派发
        return self.vtable.area(self.ptr);
    }
};

const Circle = struct {
    r: f64,
    fn areaImpl(ptr: *anyopaque) f64 {     // 取出具体类型再算
        const self: *Circle = @ptrCast(@alignCast(ptr));
        return 3.0 * self.r * self.r;
    }
    fn shape(self: *Circle) Shape {        // 构造接口视图
        return .{ .ptr = self, .vtable = &.{ .area = areaImpl } };
    }
};

pub fn main() void {
    var c = Circle{ .r = 2.0 };
    const s = c.shape();
    std.debug.print("{d:.1}\n", .{s.area()});   // 12.0
}
```

`*anyopaque` + vtable 的组合就是 Zig 版的 `dyn Trait`：`@ptrCast` 与 `@alignCast` 把数据指针还原成具体类型，写错类型是未定义行为，编译器帮不上忙——这是显式设计的代价，换来零隐藏分配与可读的机器码。`comptime` 承担了另一半复用：写 `fn List(comptime T: type) type { return struct { ... }; }` 就能为每种元素类型生成独立结构体（相当于 C++ 模板/单态化），也可以在编译期检查某个类型是否提供所需函数并据此生成代码（duck typing 式的接口约定）。Zig 没有 drop 与继承析构，接口的释放责任由约定承担：`std.mem.Allocator` 的 `vtable` 里有 `alloc`/`resize`/`free`/`remap`，谁分配谁释放的规则写在文档里而不是类型系统里。

📘 [Zig · Documentation](https://ziglang.org/documentation/master/) ｜ 📘 [Zig · `std.mem.Allocator`](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有类与继承，但有一张万能的表（table）和元表（metatable）。`__index` 元方法让"访问表里不存在的键"变成"去另一张表里找"，这条链就构成了原型继承；`setmetatable` 手工把实例指向原型、原型指向父原型。整个机制是纯运行时的：查找失败只会得到 `nil`，不会有编译错误。

```lua
local Animal = {}                        -- 原型（相当于类）
Animal.__index = Animal                  -- 实例查不到时回到 Animal 找
function Animal.new(name)
  local self = setmetatable({}, Animal)  -- 实例的原型是 Animal
  self.name = name
  return self
end
function Animal:speak() return "..." end -- 冒号 = 隐式 self
function Animal:describe() return self.name .. ": " .. self:speak() end

local Dog = setmetatable({}, { __index = Animal })  -- 中间类：原型链
Dog.__index = Dog
function Dog.new(name)
  local self = Animal.new(name)
  return setmetatable(self, Dog)         -- 换成 Dog 原型
end
function Dog:speak() return "Woof" end   -- 遮蔽父原型的同名方法

local d = Dog.new("Rex")
print(d:describe())        -- Rex: Woof（self:speak() 动态查找）
print(d:speak())           -- Woof
print(Dog.new("x").name)   -- x
print(getmetatable(d) == Dog)  -- true
print(rawget(d, "speak"))  -- nil：方法不在实例里，在原型链上
```

查找规则是：先看实例表自己的键，没有就顺着 `__index` 链向上找（`__index` 可以是表，也可以是函数，函数形式就能实现动态计算甚至循环引用检测）。`Animal.new` 里 `setmetatable({}, Animal)` 建立实例→原型的关系，`Dog` 通过 `setmetatable({}, { __index = Animal })` 成为 `Animal` 的"子类"，`Dog.new` 再把实例的元表改成 `Dog`，于是查找路径变成实例 → `Dog` → `Animal`。陷阱有三处：忘记写 `__index` 会让原型链断掉（表现为找不到方法）、`rawget`/`rawset` 会绕过元表、以及 `__index` 链是线性查找，层次深了每次方法调用都要走一遍。要复用时更常见的做法是**组合**而非深链：在实例里放 `self.items = ...`，把方法实现为局部函数表，需要哪个就拷贝哪个键（用 `pairs` 遍历 Mixin 并逐个赋值的方法），或者用 `setmetatable` 加多个 `__index` 层做受控 mixin。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4) ｜ 📘 [Lua · Programming in Lua · Inheritance](https://www.lua.org/pil/16.2.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 有 `class` 与单继承 `extends`，同时有只有类型层面存在的 `interface` 与 `implements`。最关键的一点是**它有两套并行的东西**：类的成员在运行时是真实的 JS 原型属性，而 `interface`、`implements`、`abstract`、`private` 全都在编译期被擦除，运行时看不到任何痕迹。所以 TypeScript 的"继承"是 JS 原型继承加上一层静态检查。

```typescript
abstract class Animal {                    // abstract：不能直接实例化
  constructor(public readonly name: string) {}
  speak(): string { return "..."; }        // 普通方法
  abstract kind(): string;                 // 抽象方法：子类必须实现
}

class Dog extends Animal {                 // 单继承
  override speak(): string { return "Woof"; }   // override 关键字（4.3+ 可开 noImplicitOverride）
  kind(): string { return "dog"; }
}

interface Named { label: string; }         // 纯编译期契约
interface Aged { age: number; }
interface Named { extra?: boolean; }       // 声明合并：同名接口自动合并

class Tagged extends Animal implements Named, Aged {   // 多接口
  label = "tag";
  age = 1;
  kind(): string { return "tagged"; }
}

const animals: Animal[] = [new Dog("Rex"), new Tagged("t")];
console.log(animals[0].speak());           // Woof
console.log(animals[0] instanceof Animal); // true（运行时真实检查）
console.log(animals[1].kind());            // tagged
const obj = { label: "x", age: 3 };              // 新鲜字面量先落到变量上
const n: Named = obj;                            // ✅ 结构化兼容：只要求有 label
console.log(n.label);                      // x
// const bad: Animal = { name: "x" };      // 🛑 缺少 kind/speak，编译错误
```

`extends` 在运行时产生真正的原型链（`Object.getPrototypeOf(Dog.prototype) === Animal.prototype`），`implements` 只做静态检查、不产生任何代码。TypeScript 的类型兼容是**结构化**的：`Named` 不看对象是不是某个类的实例，只看有没有 `label` 字段（"鸭子类型"的静态版本），这与 Java 的名义类型完全不同，也因此 `interface` 之间可以相互赋值只要形状兼容。需要多个来源的行为时，TypeScript 用接口组合（`interface A extends B, C`）或 mixin 函数——因为 `extends` 只能写一个父类。`abstract` 只在编译期有效，运行时 `Animal` 依然能被 `new`（除非用 `private constructor` 或运行时守卫），所以库作者不要把它当作运行时的安全边界。工具链层面：TypeScript 7（官方 2026-07 发布）是把编译器用 Go 重写后的原生实现，语言语义与 6.x 保持一致（类型检查规则不变，改的是编译速度与编辑器响应），因此本页列出的所有类型层结论在 7 里同样成立。

📘 [TypeScript · Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html) ｜ 📘 [TypeScript · Mixins](https://www.typescriptlang.org/docs/handbook/mixins.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 只有原型继承：每个对象有一个内部槽 `[[Prototype]]`（用 `Object.getPrototypeOf` 读，`__proto__` 是非标准的访问器），属性查找失败时沿这条链向上找。ES2015 的 `class`/`extends`/`super` 是这套原型机制的语法糖，`instanceof` 检查的也是原型链。它属于纯运行时的动态机制，没有接口、没有抽象方法、没有访问控制。

```javascript
class Animal {
  constructor(name) { this.name = name; }   // 实例自己的属性
  speak() { return "..."; }                  // 方法挂在 Animal.prototype 上
}
class Dog extends Animal {
  speak() { return "Woof"; }                 // 覆盖原型上的方法
}
const d = new Dog("Rex");
console.log(d.speak());                      // Woof
console.log(d instanceof Dog, d instanceof Animal);        // true true
console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype); // true
console.log(Object.hasOwn(d, "speak"));      // false：方法在原型上
console.log(Object.keys(d));                 // [ 'name' ]

// 不用 class 的手工原型链（等价形式）
function Cat(name) { this.name = name; }
Cat.prototype = Object.create(Animal.prototype);   // 建立原型链
Cat.prototype.constructor = Cat;
Cat.prototype.speak = function () { return "Meow"; };
console.log(new Cat("Tom").speak());         // Meow
console.log(new Cat("Tom") instanceof Animal); // true

// mixin：把方法拷进原型（没有多继承，只能复制）
const Swimmer = {
  swim() { return `${this.name} swims`; },
};
Object.assign(Dog.prototype, Swimmer);
console.log(new Dog("Rex").swim());          // Rex swims
```

`class` 只是语法糖：方法定义在 `prototype` 上而不是每个实例上，因此 `hasOwn` 为 `false`，改 `Dog.prototype.speak` 会立即影响所有实例（包括已创建的）——这是"运行时改类"能力与风险同源的地方。`extends` 同时设置两条链：构造函数的 `[[Prototype]]` 指向父构造函数（静态成员继承），原型的 `[[Prototype]]` 指向父原型（实例成员继承）。JavaScript 没有多继承，横向复用只能靠 mixin（`Object.assign` 或 `class extends Mixin(Base)` 的高阶函数写法），代价是方法被复制进原型、`instanceof` 无法识别 mixin 来源。`super` 在构造函数里必须在使用 `this` 之前调用；箭头函数没有自己的 `this`，放进原型方法里要小心。`new.target`、`Object.setPrototypeOf` 可以事后改原型，但会破坏引擎的隐藏类优化。

📘 [MDN · Classes](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes) ｜ 📘 [MDN · Inheritance and the prototype chain](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的类继承是单继承：`class Dog extends Animal`，一个类只能有一个父类；横向复用由接口（`implements`）和 trait（`trait` 加 `use`）承担。trait 是 PHP 特有的机制——它像一段可以粘贴进类的方法集合，用来绕过单继承的限制。另一个需要澄清的点是：PHP 没有 `virtual` 关键字，但非 `final`、非 `private`、非 `static` 的实例方法在子类里都能被重定义，也就是"默认就是虚方法"的语义，这与 Java 相同，而与 C#、Kotlin 的"默认非虚"相反。

```php
<?php
class Animal {
    public function __construct(protected string $name) {}
    public function speak(): string { return "..."; }
    final public function id(): string { return "animal:{$this->name}"; }
}

class Dog extends Animal {                       // 单继承
    public function speak(): string { return "Woof"; }   // 重定义（无需关键字）
}

trait Swimmer {                                  // trait：横向复用
    public function swim(): string { return "{$this->name} swims"; }
}

interface Shape { public function area(): float; }

class Circle implements Shape {                  // 接口
    use Swimmer;                                 // 混入 trait
    public function __construct(private float $r) {}
    public function area(): float { return 3.0 * $this->r ** 2; }
}

$animals = [new Animal("x"), new Dog("Rex")];
echo $animals[1]->speak(), PHP_EOL;              // Woof（动态派发）
echo $animals[0]->speak(), PHP_EOL;              // ...
echo ($animals[1] instanceof Animal ? "yes" : "no"), PHP_EOL;  // yes
$c = new Circle(2.0);
echo $c->area(), PHP_EOL;                        // 12
echo $c->swim(), PHP_EOL;                        // ⚠️ 运行时警告：Circle 没有 $name 属性
```

trait 的语义是**编译期拷贝**：`use Swimmer;` 把方法原样插入类定义，`$this` 指向使用 trait 的那个实例，`instanceof Swimmer` 永远为 `false`，因为 trait 不是类型。因此 trait 里的方法可以访问 `$this->name` 这样的属性，但属性本身必须由使用它的类提供，否则运行时才会报错（上面 `Circle` 没有 `$name`，`swim()` 会在运行时触发警告而不是编译错误——这正是 trait 的典型陷阱）。多个 trait 有同名方法时必须显式解决冲突：`use A, B { A::hello insteadof B; B::hello as helloB; }`。抽象类（`abstract class` 加 `abstract function`）用于"有部分实现、必须被继承"的场景，接口用于只声明契约；PHP 8 起接口方法可以有默认实现吗？不能——接口方法仍然只能是声明，没有默认方法体（这与 Java 8 不同）。要限制继承用 `final class`，要禁止覆盖某个方法用 `final public function`。

📘 [PHP · Object Inheritance](https://www.php.net/manual/en/language.oop5.inheritance.php) ｜ 📘 [PHP · Traits](https://www.php.net/manual/en/language.oop5.traits.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的类继承是单继承：`class Dog < Animal`，每个类只有一个直接超类（`Dog.superclass`），而 `Object` 之上是 `BasicObject`。它用 module 补足横向复用：`include` 把 module 的方法插入祖先链（实例方法），`extend` 把它们变成对象或类的方法，`prepend` 则插到类**之前**从而能覆盖类自身的方法并调用 `super`。属于纯运行时机制，祖先链（`Module#ancestors`）可以随时检查。

```ruby
module Greet
  def greet = "hello from #{self.class}"       # 无参方法定义（3.0+）
end

class Animal
  include Greet            # 祖先链：Animal -> Greet -> Object
  def initialize(name) = @name = name
  def speak = "..."
  def describe = "#{self.class}(#{@name}): #{speak}"   # 动态派发
end

class Dog < Animal
  def speak = "Woof"
end

puts Dog.new("Rex").describe      # Dog(Rex): Woof
puts Dog.superclass               # Animal
puts Dog.ancestors.take(3).inspect  # [Dog, Animal, Greet]（Dog -> Animal -> Animal 里 include 的 Greet）
puts Dog.new("Rex").greet         # hello from Dog

module Over
  def speak = "over+" + super     # prepend：优先于 Cat 自己的 speak
end
class Cat < Animal
  prepend Over
  def speak = "meow"
end
puts Cat.new("Tom").speak         # over+meow
puts Cat.ancestors.take(3).inspect  # [Over, Cat, Animal]
```

祖先链的顺序是 Ruby 复用机制的全部：`include` 把 module 插在当前类**之后**（所以类自己定义的同名方法优先，`Dog#speak` 赢过 module 里的 `speak`），`prepend` 插在**之前**（所以 `Over#speak` 赢过 `Cat#speak`，并且它里面的 `super` 会调用 `Cat#speak`），多个 `include` 的先后决定谁的版本胜出。`extend` 把 module 的方法加到单件类上，是"给某个对象或某个类添加方法"的方式。因为只有单继承，Ruby 没有菱形问题，但 module 的多重混入仍然会带来顺序依赖，这也是 Ruby 项目里最需要写注释说明的地方之一。要复用而非继承时，Ruby 提供 `Forwardable` 的 `def_delegators`、`Delegator`/`SimpleDelegator` 以及 `method_missing` 转发，让组合的成本降到接近继承。

📘 [Ruby · Modules and classes](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html) ｜ 📘 [Ruby · Module](https://docs.ruby-lang.org/en/master/Module.html)

{{% /tab %}}

{{< /tabpane >}}

### 覆盖与多态

覆盖（overriding）与多态（polymorphism）在 18 门语言里的开关密度完全不同：C++ 与 Java 默认所有实例方法都是虚函数，Kotlin 与 Swift 要求显式 `open`/`override`，C#、PHP 需要 `virtual`（或对 `abstract` 显式覆盖），而 Rust、Go、C、Zig、Lua、R 根本没有"覆盖"这个概念，多态只能通过 `dyn Trait`、接口、手工 vtable 或泛型函数分派实现。这一节给出 `virtual`/`override`/`abstract`/`sealed`/`final` 的完整矩阵，并说明动态派发（vtable）与静态派发分别在什么条件下发生。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有 `virtual`/`override` 关键字，也没有"子类覆盖父类方法"这回事。它的多态有两个通道：**`dyn Trait`** 走 vtable（运行期查表，代价是一次间接调用），**泛型 `T: Trait`** 走单态化（编译期确定为具体类型，零开销但每实例化一次就生成一份代码）。trait 的默认方法相当于"父类提供的实现"，类型自己的 `impl` 里的同名方法优先。

```rust
trait Greet {
    fn name(&self) -> String;
    fn hello(&self) -> String { format!("hi {}", self.name()) }   // 默认方法
}
trait Loud: Greet {                                              // 父 trait 约束
    fn hello(&self) -> String { format!("{}!", Greet::name(self)) }
}
struct A;
struct C;
impl Greet for A { fn name(&self) -> String { "A".into() } }
impl Greet for C { fn name(&self) -> String { "C".into() } }
impl Loud for C {}

// 两个 trait 都提供 hello 时选择是歧义的：固有 impl 负责消歧
impl C {
    fn hello(&self) -> String { <C as Greet>::hello(self) }
}
fn main() {
    println!("{}", A.hello());                 // hi A
    println!("{}", C.hello());                 // hi C（固有方法优先）
    println!("{}", <C as Loud>::hello(&C));    // C!（显式限定 trait）
    let v: Vec<Box<dyn Greet>> = vec![Box::new(A), Box::new(C)];
    for x in &v { println!("{}", x.hello()); } // hi A / hi C：vtable 派发
}
```

如果没有上面的固有 `impl`，`C.hello()` 会直接编译失败并报 `E0034: multiple applicable items in scope`——Rust 拒绝替你在两个 trait 之间猜，必须写 `<C as Greet>::hello(&c)` 或 `<C as Loud>::hello(&c)`。这与 Java 8 默认方法的菱形冲突是同一类问题，处理方式更显式。`dyn Trait` 的方法表里只包含该 trait 需要的方法，因此 trait 对象只能调用 trait 声明的方法（额外的固有方法必须先向下转型）；trait 若带泛型方法或返回 `Self`，就不能做成 trait object（不是 object-safe）。选择通道的判据：需要在同一集合里存放异构实现、或在运行时插件化加载，用 `dyn`；只在编译期已知的类型之间共享代码、且在乎性能，用泛型；只是想少写重复实现，用默认方法与 blanket impl（`impl<T: Display> MyTrait for T`）。

📘 [Rust Reference · Trait objects](https://doc.rust-lang.org/reference/types/trait-object.html) ｜ 📘 [Rust Book · Trait objects（对象安全与动态派发）](https://doc.rust-lang.org/book/ch18-02-trait-objects.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的类方法默认可以被覆盖，覆盖必须写 `override`，禁止继续覆盖写 `final`；`final class` 连继承一起封死。协议（`protocol`）用扩展（`extension`）提供默认实现，但**协议扩展里的方法不参与动态派发**——如果具体类型自己也实现了同名方法，通过 `any P` 调用时走的是扩展版本，这是一个很隐蔽的坑。

```swift
class Animal {
    func speak() -> String { "..." }            // 默认可覆盖
    func kind() -> String { "animal" }
}
class Dog: Animal {
    override func speak() -> String { "Woof" }
}
final class Puppy: Dog {                        // final class：不能再被继承
    override func kind() -> String { "puppy" }
}

protocol Shape { func area() -> Double }
extension Shape {
    func describe() -> String { "area=\(area())" }   // 协议扩展默认实现
}
struct Circle: Shape { var r: Double; func area() -> Double { 3.0 * r * r } }
protocol Named { var label: String { get } }
protocol Aged { var age: Int { get } }
typealias NamedAged = Named & Aged              // 协议组合

struct Person: Named, Aged { var label: String; var age: Int }

let shapes: [any Shape] = [Circle(r: 2.0)]      // existential：写成 any Shape 更清楚
print(shapes[0].describe())                     // area=12.0
let p: any NamedAged = Person(label: "x", age: 3)
print(p.label, p.age)                           // x 3
print(Puppy().kind())                           // puppy
func make() -> some Shape { Circle(r: 1.0) }    // 不透明类型：静态派发
print(make().describe())                        // area=3.0
```

需要区分三种"多态"的成本：类继承走 vtable，`final` 方法可以被静态派发（`whole-module-optimization` 下可内联），`any P` 是 existential 装箱（有间接调用与可能的堆分配），`some P` 与泛型 `T: P` 则让编译器知道唯一的具体类型、完全没有装箱。协议扩展的方法在 existential 上是静态派发的：假设 `Shape` 扩展里有 `describe()`，而 `Circle` 自己又定义了一个 `describe()`，那么 `let s: any Shape = Circle(...)` 上调用 `s.describe()` 得到的是扩展版本而非 `Circle` 的版本；要得到动态行为必须把方法写进协议要求本身。Swift 里 `override` 与 `required`（`required init`）是针对类的，协议要求的初始化器用 `required` 保证子类也实现；跨类型复用优先用协议组合（`Named & Aged`）而不是造一层基类。

📘 [Swift · Inheritance](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/inheritance/) ｜ 📘 [Swift · Protocols](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有 `virtual`、没有 `override`、没有抽象方法，"覆盖"在 Go 里只能靠**遮蔽**实现：外层类型定义同名方法，于是提升自嵌入类型的方法被挡住。这个区别是致命的——遮蔽只在编译期按接收者的静态类型选择，通过 `Animal` 类型的变量调用永远得到 `Animal` 的方法，没有 vtable。Go 唯一的动态派发入口是接口。

```go
package main

import "fmt"

type Animal struct{ Name string }

func (a Animal) Speak() string { return "..." }
func (a Animal) Kind() string  { return "animal" }

type Dog struct{ Animal }                  // 嵌入

func (d Dog) Speak() string { return "Woof" }   // 遮蔽，不是 override

type Speaker interface{ Speak() string }   // 接口：隐式实现

func run(s Speaker) string { return s.Speak() } // 传接口才有多态

func main() {
	fmt.Println(run(Dog{Animal{"Rex"}}))   // Woof
	fmt.Println(run(Animal{"x"}))          // ...
	fmt.Println(Dog{Animal{"Rex"}}.Kind()) // animal：方法被提升
	fmt.Println(Dog{Animal{"Rex"}}.Animal.Speak()) // ...：显式调回被遮蔽的方法
	// 接口组合：Go 没有继承，接口也不互相继承，只是把方法集并起来
}
```

方法集规则决定接口满足关系：值接收者的方法同时属于 `T` 与 `*T` 的方法集，指针接收者的方法只属于 `*T`；因此如果 `Speak` 定义在 `*Dog` 上，`Dog{...}` 不满足 `Speaker`，必须取地址 `&d`（或把变量声明为 `*Dog`）。接口值的内部表示是（动态类型, 数据）二元组，接口之间转换是零分配的，但把具体类型装进接口可能引起堆分配与逃逸分析变化。Go 里没有"默认方法冲突"的问题，因为接口不能带实现；需要类似"抽象类 + 默认实现"的效果时，标准做法是写一个基础结构体提供默认方法，让其他类型嵌入它并遮蔽需要变化的方法——但要清楚通过接口调用时派发的仍是接口方法，而不是嵌入结构体里的实现。检查行为是否满足用编译期断言 `var _ Speaker = Dog{}`。

📘 [Go spec · Method sets](https://go.dev/ref/spec#Method_sets) ｜ 📘 [Effective Go · Interfaces](https://go.dev/doc/effective_go#interfaces)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的所有实例方法在语义上都是虚方法：属性查找每次访问都沿 MRO 进行，没有关键字控制，也没有编译期检查。抽象类由 `abc.ABC` 与 `@abstractmethod` 表达（实例化抽象类会抛 `TypeError`），但抽象方法只在实例化时检查，不会在定义子类时立即报错。`super()` 不是"父类"，而是"MRO 上的下一个类"，这是协作式多继承的基础。

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    def describe(self) -> str:               # 模板方法：调用被子类覆盖的 area
        return f"area={self.area()}"

class Sq(Shape):
    def __init__(self, s: float) -> None: self.s = s
    def area(self) -> float: return float(self.s ** 2)

class Cube(Sq):                              # 覆盖 + super() 链
    def area(self) -> float: return 6.0 * super().area()

print(Sq(3).describe())      # area=9.0
print(Cube(2).describe())    # area=24.0：Cube.area -> Sq.area -> ...
print([c.__name__ for c in Cube.__mro__])   # ['Cube', 'Sq', 'Shape', 'ABC', 'object']
try:
    Shape()
except TypeError as e:
    print(type(e).__name__)  # TypeError：抽象类不能实例化
```

`@abstractmethod` 只是把类标成不可实例化，它**不阻止**你调用 `Shape.area(self)` 这类绕过方式；想让子类必须覆盖某个方法，除了 `ABC` 还可以在方法体里 `raise NotImplementedError`（运行时报错而不是实例化时报错）。协变返回类型在 Python 里不是问题——类型注解留给静态检查器（mypy、pyright）判断，运行时不检查，因此重写方法可以返回更具体的类型（`Self` 注解从 3.11 起可用）。默认实现冲突在 Python 里表现为 MRO 顺序：多个父类都有 `describe` 时，只有排在最前面的那个被选中，其余必须显式调用（`Other.describe(self)`），不存在 Java 式的编译期冲突错误——错误会在运行时以"行为不对"的形式暴露。需要接口约束而不想引入继承时，用 `typing.Protocol`（结构化子类型，加 `@runtime_checkable` 才能 `isinstance`）。

📘 [Python · abc](https://docs.python.org/3/library/abc.html) ｜ 📘 [Python · super()](https://docs.python.org/3/library/functions.html#super)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 把"可覆盖"变成必须显式声明的东西：类要 `open` 才能被继承，成员要 `open` 才能被覆盖，覆盖时必须写 `override`。`abstract` 成员必须被覆盖，`final` 禁止覆盖，`sealed` 把子类限定在同一模块与包内，接口可以有默认实现但多个接口冲突时必须显式消解。这套规则与默认 `final` 的类定义合起来，构成 Kotlin 对脆弱基类问题的正面回答。

```kotlin
open class Animal(val name: String) {
    open fun speak(): String = "..."            // open 才可覆盖
    fun kind(): String = "animal"               // 默认 final
}
class Dog(name: String) : Animal(name) {
    override fun speak(): String = "Woof"
}
sealed class Result {                            // sealed：子类限定在同模块
    class Ok(val v: Int) : Result()
    class Err(val msg: String) : Result()
}

interface A { fun greet(): String = "A" }
interface B { fun greet(): String = "B" }
class AB : A, B {
    override fun greet(): String = super<A>.greet() + super<B>.greet()  // 必须消解
}

fun describe(r: Result): String = when (r) {     // 穷尽性：编译器检查
    is Result.Ok -> "ok ${r.v}"
    is Result.Err -> "err ${r.msg}"
}

fun main() {
    val a: Animal = Dog("Rex")
    println(a.speak())            // Woof：vtable 派发
    println(AB().greet())         // AB
    println(describe(Result.Ok(1)))   // ok 1
    val open2: Animal = Animal("x")
    println(open2.kind())         // animal
}
```

`open` 是类继承的开关，`override` 是覆盖的开关，覆盖后的成员默认仍然开放（想封死写 `final override`）。`super<A>.greet()` 是接口默认实现冲突的唯一消解方式——Kotlin 要求必须显式覆盖，不会像 Java 8 那样在某些情况下静默选择。`sealed class`/`sealed interface` 的穷尽性检查是编译期的：`when` 漏掉一个分支直接编译失败（作为表达式时），这比 Java 17 的 `sealed` 加模式匹配 switch 更早成为语言核心。属性也可以覆盖：父类声明 `open val x`，子类用 `override val x` 或在构造器参数里 `override val x`；规则是 `val` 可以被 `val` 或 `var` 覆盖，而 `var` 只能被 `var` 覆盖（反过来会被编译器拒绝）。`interface` 的默认实现不能持有状态（不能有 backing field），所以 Kotlin 用接口 + `by` 委托替代"带状态的基类"。

📘 [Kotlin · Inheritance](https://kotlinlang.org/docs/inheritance.html) ｜ 📘 [Kotlin · Sealed classes](https://kotlinlang.org/docs/sealed-classes.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的实例方法默认就是虚方法（除 `static`、`final`、`private` 与构造器），覆盖不强制写关键字，但从 Java 5 起建议加 `@Override` 让编译器校验签名拼写。`abstract` 方法必须被具体子类实现，`final` 方法禁止覆盖，Java 17 起 `sealed` 限定子类集合，Java 16 起的 `record` 隐式为 `final`。默认方法（Java 8 起）让接口能带实现，但多接口的默认方法冲突必须显式消解。

```java
abstract class Animal {                       // 抽象类
    protected final String name;
    Animal(String name) { this.name = name; }
    abstract String speak();                  // 抽象方法：子类必须实现
    String describe() { return name + ": " + speak(); }  // 模板方法
}

class Dog extends Animal {
    Dog(String name) { super(name); }
    @Override String speak() { return "Woof"; }
}

sealed interface Shape permits Circle, Square { double area(); }   // Java 17+
record Circle(double r) implements Shape {                         // record 隐式 final
    public double area() { return 3.0 * r * r; }
}
record Square(double side) implements Shape {
    public double area() { return side * side; }
}

interface A { default String greet() { return "A"; } }
interface B { default String greet() { return "B"; } }
class AB implements A, B {
    @Override public String greet() { return A.super.greet() + B.super.greet(); }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog("Rex");
        System.out.println(a.describe());      // Rex: Woof
        Shape s = new Circle(2.0);
        System.out.println(s.area());          // 12.0
        System.out.println(new AB().greet());  // AB
        System.out.println(s instanceof Shape); // true
    }
}
```

`A.super.greet()` 是 Java 消解默认方法冲突的唯一语法，且必须重写该方法，否则编译报错（"class inherits unrelated defaults"）；这也是接口默认方法被称为"受控的多继承"的原因：它继承了行为，但接口不能有实例字段，因此不会产生菱形状态。`abstract class` 与接口的分工是：需要字段、构造器、受保护状态时用抽象类（只能有一个），只声明能力或给无状态默认实现时用接口（可以有多个）。Java 的 `sealed` 要求子类与被密封类处于同一模块（具名模块）或同一包（无名模块），写不写 `permits` 都不改变这条约束，与 `record` 和模式匹配 `switch` 组合后可以做穷尽性检查。方法调用在字节码层用 `invokevirtual`（普通虚方法）/`invokeinterface`（接口方法）/`invokespecial`（构造器、`private`、`super`）/`invokestatic` 四类指令区分，JIT 通过内联缓存把单态调用点优化成直接调用，因此"全部虚方法"并不等于"每次调用都查表"。

📘 [Java · Polymorphism](https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html) ｜ 📘 [JLS · Method overriding](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.4.8)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 用 `virtual` 显式打开动态派发，`override` 让编译器校验"确实覆盖了某个虚函数"（C++11 起），`final` 封死覆盖（可用于函数、类），纯虚函数 `= 0` 让类成为抽象类。这里有一个必须记住的行为：**构造期与析构期调用虚函数不会派发到派生类**——因为此时派生类部分还没构造或已经析构。

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Base {
    Base() { std::cout << "ctor calls " << name() << "\n"; }  // ⚠️ 只派发到 Base
    virtual ~Base() = default;                                // 多态基类必须有虚析构
    virtual std::string name() const { return "Base"; }
    virtual int size() const = 0;                             // 纯虚：抽象类
    virtual Base* clone() const = 0;                          // 协变：基类返回 Base*
};
struct Mid : Base {
    std::string name() const override { return "Mid"; }
    int size() const override { return 1; }
    Mid* clone() const override { return new Mid(*this); }     // 返回 Mid*，是 Base* 的协变
};
struct Fin : Mid {
    std::string name() const final { return "Fin"; }          // final：禁止继续覆盖
    int size() const override { return 2; }
    Fin* clone() const override { return new Fin(*this); }    // 返回类型协变到 Fin*
};
int main() {
    Fin f;                                   // ctor calls Base
    Base* p = &f;
    std::cout << p->name() << "\n";           // Fin
    std::cout << p->size() << "\n";           // 2
    Mid m;                                    // ctor calls Base
    Base* q = &m;
    std::cout << q->name() << "\n";           // Mid
    std::cout << sizeof(Base) << "\n";        // 8：对象里只有一个 vptr
    auto c = f.clone();                       // 静态类型是 Fin*（协变返回），动态类型也是 Fin
    std::cout << c->name() << "\n";           // Fin
    delete c;
}
```

派生类里写 `virtual` 是可选的（一旦基类是虚函数，覆盖它自动是虚函数），但 `override` 强烈建议写：它能捕获签名不匹配、基类函数不是虚函数等错误，否则你可能写出一个"看起来是覆盖，实际是新函数"的版本。`final` 让编译器可以做去虚化（devirtualization）直接内联。构造函数里虚表指针被设置为当前正在构造的类，因此 `Base()` 里调用 `name()` 返回 `"Base"`——Java、C# 会派发到子类，C++ 不会，这是同一段模板方法代码在不同语言里行为相反的地方。协变返回类型只允许指针与引用（`Base*` → `Derived*`），返回值类型不行。抽象类必须有虚析构函数，否则通过基类指针 `delete` 派生对象是未定义行为；`= default` 的虚析构在 C++11 起可用，别漏写。C++20 的 `concepts` 可以把"运行时虚接口"换成编译期约束，通常能同时换来更好的性能与更清楚的错误信息。

📘 [cppreference · virtual specifier](https://en.cppreference.com/w/cpp/language/virtual) ｜ 📘 [cppreference · override / final](https://en.cppreference.com/w/cpp/language/override)

{{% /tab %}}

{{% tab header="C" %}}

C 没有任何覆盖或多态关键字：没有 `virtual`、没有 vtable、没有 RTTI，函数调用在编译期就绑定了具体函数地址。要获得运行时派发，只有一条路——把函数指针放进结构体，调用时通过指针间接调用。标准库自身也用这个办法：`FILE` 的 `struct _IO_FILE` 里就有 `_IO_jump_t *vtable`，`struct file_operations` 则是 Linux 内核的典型例子。

```c
#include <stdio.h>

typedef struct Base Base;
typedef struct { const char *(*name)(const Base *); int (*size)(const Base *); } Vtbl;
struct Base { const Vtbl *vtbl; };

static const char *base_name(const Base *b) { (void)b; return "Base"; }
static int base_size(const Base *b) { (void)b; return 0; }
static const Vtbl BASE_VTBL = { base_name, base_size };

typedef struct { Base base; int extra; } Sub;      /* 首成员 = 基类 */

static const char *sub_name(const Base *b) {
    const Sub *s = (const Sub *)b;                 /* 向下转换：不检查 */
    static char buf[32];
    snprintf(buf, sizeof buf, "Sub%d", s->extra);
    return buf;
}
static int sub_size(const Base *b) { return ((const Sub *)b)->extra; }
static const Vtbl SUB_VTBL = { sub_name, sub_size };

int main(void) {
    Sub s = { { &SUB_VTBL }, 7 };
    Base *p = &s.base;                             /* 向上转换：偏移 0，隐式安全 */
    printf("%s %d\n", p->vtbl->name(p), p->vtbl->size(p));    /* Sub7 7 */
    printf("%s %d\n", BASE_VTBL.name(p), BASE_VTBL.size(p));  /* Base 0：显式选基类实现 */
    return 0;
}
```

"覆盖"在 C 里就是**换一张表**：`Sub` 的实例把自己的 `vtbl` 指向 `SUB_VTBL`，于是通过 `Base*` 的调用落到 `sub_name`。想调用被遮蔽的基类实现，就直接写 `BASE_VTBL.name(p)`——因为函数指针是数据，你完全可以显式选任何一个实现，这是 C 比 C++ 灵活也更危险的地方（C++ 里 `Base::name()` 是唯一入口，C 里谁都可以改表）。陷阱有三个：忘记初始化 `vtbl` 会在调用时崩溃；函数指针签名必须与调用点完全一致，否则是未定义行为（C 没有虚函数协变，连 `void*` 转换都要自己保证）；基类对象不能按值拷贝进"基类容器"，因为真正的多态信息在 `vtbl` 指针里，一旦对象被切片复制、`vtbl` 仍指向子类的表而 `extra` 字段已经不存在了，这是 C 版对象切片。发布这类接口时通常再配一个 `destroy` 函数放进表里作为"虚析构"。

📘 [C · struct](https://en.cppreference.com/w/c/language/struct) ｜ 📘 [C · Pointer declarations](https://en.cppreference.com/w/c/language/pointer)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 没有覆盖，因为方法不属于类型：它把所有同名函数的不同签名看成**同一个泛型函数的多个方法**，调用时按参数的具体类型选最具体的方法（多重分派）。因此"子类改变父类行为"在 Julia 里是"给子类型加一个更具体的方法"，完全不需要 `virtual`/`override`；抽象类型只负责建立子类型关系与约束方法签名。

```julia
abstract type Animal end
struct Dog <: Animal; name::String; end
struct Cat <: Animal; name::String; end

speak(::Animal) = "..."                # 泛型函数的默认方法
speak(d::Dog) = "Woof $(d.name)"
speak(c::Cat) = "Meow $(c.name)"

describe(x::Animal) = "$(typeof(x)): $(speak(x))"   # 模板方法风格
println(describe(Dog("Rex")))          # Dog: Woof Rex
println(describe(Cat("Tom")))          # Cat: Meow Tom

struct Robot end
speak(r::Robot) = "beep"               # 不与 Animal 共享层次，也能加入
println(speak(Robot()))                # beep
println(Dog <: Animal, Robot <: Animal)  # true false
println(methods(speak))                # 4 个方法
println(which(speak, (Dog,)))          # 选中的方法
println(applicable(speak, 1))          # false：Int 没有方法
```

"选最具体"是运行时可观察的行为：`speak(d::Dog)` 比 `speak(::Animal)` 更具体，所以 `Dog` 实例走前者；两个方法无法比较特异性时（例如 `f(::Int, ::Animal)` 与 `f(::Animal, ::Int)` 对 `(Int, Int)` 调用）会抛 `MethodError: ambiguous`，必须显式加一个更具体的方法消解——这与 Java 默认方法冲突、Rust trait 方法歧义属于同类问题。抽象类型不能有字段，因此"覆盖父类行为"时你无法像类继承那样先复用父类实现再改一点；要复用就抽出一个普通函数（`base_speak`）在自己的方法里调用它，或者把共享字段做成显式结构体字段。多重分派也意味着扩展别人的类型不需要改别人的代码（Open/Closed 在语法层面成立），这是 Julia 生态用 trait 库（如 SimpleTraits.jl、Traits.jl）做"接口约定"的原因：类型层次表达"是什么"，trait 表达"能做什么"，两者正交。

📘 [Julia · Methods](https://docs.julialang.org/en/v1/manual/methods/) ｜ 📘 [Julia · Interfaces](https://docs.julialang.org/en/v1/manual/interfaces/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的关键字梯度最细：`virtual` 打开覆盖，`override` 声明覆盖，`new` 声明遮蔽（隐藏基类成员），`abstract` 要求子类实现，`sealed override` 封死后续覆盖，`sealed class` 封死继承。接口从 C# 8 起有默认实现，`static abstract` 成员（C# 11）让接口可以要求静态成员从而支持泛型数学。方法默认**不是**虚的，这是 C# 与 Java 的核心差异。

```csharp
using System;

abstract class Animal {                        // 抽象类
    protected readonly string Name;
    protected Animal(string name) { Name = name; }
    public abstract string Speak();            // 抽象方法
    public virtual string Describe() => Name + ": " + Speak();  // 虚方法
    public string Kind() => "animal";          // 非虚：不能 override
}

class Dog : Animal {
    public Dog(string name) : base(name) { }
    public override string Speak() => "Woof";
    public new string Kind() => "dog";         // ⚠️ 遮蔽，走静态绑定
}

sealed class Puppy : Dog {                     // sealed class
    public override string Speak() => "Yip";
}

sealed record Circle(double R) {               // record：按值相等；这里显式 sealed（record 默认并不 sealed）
    public double Area() => 3.0 * R * R;
}

interface IShape {
    double Area();
    string Describe() => $"area={Area()}";     // C# 8 默认接口实现
}
class Sq : IShape {
    private readonly double _s;
    public Sq(double s) => _s = s;
    public double Area() => _s * _s;
}

class Program {
    static void Main() {
        Animal a = new Puppy("Rex");
        Console.WriteLine(a.Describe());        // Rex: Yip：虚方法派发
        Console.WriteLine(a.Kind());             // animal：静态绑定到 Animal.Kind
        Console.WriteLine(((Dog)a).Kind());      // dog
        IShape s = new Sq(3);
        Console.WriteLine(s.Describe());         // area=9
        Console.WriteLine(new Circle(2).Area()); // 12
    }
}
```

`virtual`/`override` 是运行期按对象实际类型派发（vtable slot），`new` 是编译期按变量静态类型绑定——这是 C# 面试与排错里出现频率最高的区别，编译器在 `new` 处给出警告 CS0108 通常正是提示你写错了。`sealed override` 在继承链中间封死某个方法，`sealed class` 则连继承一起禁止（对 `ToString` 这类方法常见）。默认接口实现（C# 8）只能通过接口类型调用，通过类类型调用看不到它；接口不能有实例字段，因此默认实现不能保存状态，这与 Java 8 的默认方法限制相同。`record` 的继承链只允许 `record` 之间继承，且编译器生成的 `Equals`/`GetHashCode` 基于所有字段——与后面"继承陷阱"里讨论的 `equals` 契约密切相关。

📘 [C# · Inheritance](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance) ｜ 📘 [C# · virtual](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/virtual)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的实例方法默认可以被覆盖，覆盖建议写 `@override`（从 Dart 2 起该注解可选，但分析器会提示），抽象方法只能出现在 `abstract class` 里，`sealed`/`final`/`base`/`interface` 这些 class modifier 则限制类能以什么方式被使用。这里最该先知道的是：**Dart 的 `@override` 是分析器级别的检查**，不是编译器强制，而 class modifier 是真正的编译期约束。

```dart
abstract class Animal {
  final String name;
  Animal(this.name);
  String speak() => "...";
  String describe() => "$name: ${speak()}";     // 模板方法
}

class Dog extends Animal {
  Dog(super.name);
  @override
  String speak() => "Woof";
  @override
  String describe() => "dog " + super.describe();   // super 调用父实现
}

sealed class Result {}                            // sealed：同库子类 + 穷尽 switch
class Ok extends Result { final int v; Ok(this.v); }
class Err extends Result { final String msg; Err(this.msg); }

mixin Loud {
  String loud(String s) => s.toUpperCase();
}

class Wolf extends Animal with Loud {
  Wolf(super.name);
  @override
  String speak() => loud("woof");                 // 直接用 mixin 方法
}

void main() {
  final animals = <Animal>[Animal("x"), Dog("Rex")];
  print(animals[1].describe());        // dog Rex: Woof
  print(animals[0].speak());           // ...
  print(Wolf("W").speak());            // WOOF
  final r = Ok(1);
  print(switch (r) { Ok(v: var v) => "ok $v", Err(msg: var m) => "err $m" });  // ok 1
  print(Wolf("W") is Animal);          // true
}
```

`@override` 只在你开启 `annotate_overrides` lint（或使用 `flutter_lints` 之类的推荐规则集）时才会让分析器给出警告，这与 Java 的 `@Override` 直接触发编译错误不同，因此在 Dart 项目里应把该 lint 打开。`super.describe()` 沿继承链找**直接父类的实现**，`with` 混入的 mixin 方法也可以在那里被 `super` 调用（线性化之后 `super` 指向链上的下一个实现）。抽象方法不必写 `abstract`——在 `abstract class` 里只声明签名并以分号结尾的方法就是抽象方法，具体子类必须实现，否则该类也必须声明为 `abstract`。class modifier 决定复用方向：`sealed` 限定子类必须在同一库内从而让 `switch` 的穷尽性检查成立，`final` 连库外继承都禁止，`base` 禁止 `implements`（强制复用实现而不是只抄契约），`interface` 反过来禁止 `extends`，`mixin class` 两种用法都允许。需要"接口默认实现冲突"时，Dart 用 mixin 的线性化顺序处理：后写的 mixin 覆盖先写的，要显式选择就在类里自己覆盖一次并用 `super` 指定来源。

📘 [Dart · Class modifiers](https://dart.dev/language/class-modifiers) ｜ 📘 [Dart · Extend a class](https://dart.dev/language/extend)

{{% /tab %}}

{{% tab header="R" %}}

R 里没有"方法覆盖"这个概念，取而代之的是**泛型函数分派**：`UseMethod` 按第一个参数的 `class` 属性向量顺序找方法（S3），S4 按参数的类层次找最具体的方法，R6 则用类似 Java 的方法解析（`inherit` 链上找，找不到再向上）。因此"覆盖"在 R 里就是"给同一个泛型函数定义一个更具体的方法"，而 `NextMethod` 相当于 `super`。

```r
# ---- S3：UseMethod 分派 + NextMethod 调下一个 ----
speak <- function(x, ...) UseMethod("speak")
speak.default <- function(x, ...) "..."
speak.dog <- function(x, ...) paste("Woof", NextMethod())   # 调 speak.animal 或 default
new_dog <- function(name) structure(list(name = name), class = c("dog", "animal"))
speak.animal <- function(x, ...) paste0("[", x$name, "]")
print(speak(new_dog("Rex")))     # [1] "Woof [Rex]"
print(class(new_dog("Rex")))     # [1] "dog"    "animal"

# ---- S4：setGeneric / setMethod，方法按类层次选最具体 ----
setClass("Animal4", representation(name = "character"))
setClass("Dog4", contains = "Animal4")
setGeneric("speak4", function(x) standardGeneric("speak4"))
setMethod("speak4", "Animal4", function(x) paste0("[", x@name, "]"))
setMethod("speak4", "Dog4", function(x) paste("Woof", callNextMethod()))  # callNextMethod
print(speak4(new("Dog4", name = "Rex")))     # [1] "Woof [Rex]"
print(is(new("Dog4", name = "Rex"), "Animal4"))  # [1] TRUE

# ---- R6：方法与继承 ----
library(R6)
Animal6 <- R6Class("Animal6", public = list(
  name = NULL, initialize = function(name) self$name <- name,
  speak = function() "...", describe = function() paste0(self$name, ": ", self$speak())))
Dog6 <- R6Class("Dog6", inherit = Animal6,
  public = list(speak = function() "Woof"))
print(Dog6$new("Rex")$describe())    # [1] "Rex: Woof"
```

S3 的 `NextMethod()` 是**按 class 属性向量的下一个元素**去找方法，而不是按"父类"这个静态概念，所以 `class(x) <- c("dog", "animal")` 里的顺序就是分派顺序；如果 `speak.dog` 里硬写 `speak.animal(x)` 就会跳过可能的 `speak.default`，破坏协作链。S4 用 `callNextMethod()` 表示"调用本方法所覆盖的那个方法"，语义比 S3 清晰，也有 `is()` 与 `slot` 检查。R6 的方法解析沿 `inherit` 链上溯，`super$speak()` 是它的父类调用语法（`super` 是 R6 注入的对象）。`UseMethod` 只在**一个对象**上分派（默认取泛型函数的第一个参数，也可以用 `UseMethod("speak", x)` 的第二个参数显式指定分派对象），所以 S3 天生做不了多重分派；这是 S3 与 S4 最根本的分工。日常 R 代码最常见的多态是 S3 泛型（`print`、`summary`、`plot`、`format` 全是），写包时若要求字段校验或按多个参数分派，就升级到 S4 或 R6。

📘 [R · Method dispatch](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatching) ｜ 📘 [R · R6](https://cran.r-project.org/web/packages/R6/index.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有 `virtual`、没有覆盖、没有方法。多态只有一种形态：**手工装配的接口结构体**（数据指针 + 函数指针表），标准库的 `std.mem.Allocator` 就是范例。所谓"覆盖"就是换掉表里的函数指针，所谓"super 调用"就是直接调用那个原函数。编译期多态则由 `comptime` 参数与 `anytype` 承担。

```zig
const std = @import("std");

const Shape = struct {
    ptr: *anyopaque,
    vtable: *const VTable,

    const VTable = struct {
        area: *const fn (ptr: *anyopaque) f64,
        name: *const fn (ptr: *anyopaque) []const u8,
    };

    fn area(self: Shape) f64 { return self.vtable.area(self.ptr); }
    fn name(self: Shape) []const u8 { return self.vtable.name(self.ptr); }
};

const Circle = struct {
    r: f64,
    fn areaImpl(ptr: *anyopaque) f64 {
        const self: *Circle = @ptrCast(@alignCast(ptr));
        return 3.0 * self.r * self.r;
    }
    fn nameImpl(_: *anyopaque) []const u8 { return "circle"; }
    fn shape(self: *Circle) Shape {
        return .{ .ptr = self, .vtable = &.{ .area = areaImpl, .name = nameImpl } };
    }
};

fn describe(s: Shape) void {
    std.debug.print("{s}: {d:.1}\n", .{ s.name(), s.area() });   // 手工派发
}
fn total(comptime T: type, items: []const T, f: fn (T) f64) f64 {  // 编译期多态
    var sum: f64 = 0;
    for (items) |it| sum += f(it);
    return sum;
}
fn circleArea(c: Circle) f64 { return 3.0 * c.r * c.r; }

pub fn main() void {
    var c = Circle{ .r = 2.0 };
    describe(c.shape());                                      // circle: 12.0
    const cs = [_]Circle{ .{ .r = 1.0 }, .{ .r = 2.0 } };
    std.debug.print("{d:.1}\n", .{total(Circle, &cs, circleArea)});  // 15.0
}
```

`*anyopaque` + `@ptrCast(@alignCast(...))` 是 Zig 版的向下转型：类型信息被抹掉，恢复时没有任何检查，写错类型是未定义行为（`@alignCast` 在安全模式下会检查对齐）。`comptime T: type` 参数加 `fn (T) f64` 函数参数是 Zig 的静态多态：`total(Circle, ...)` 在编译期为 `Circle` 生成一份专门的代码，没有间接调用；`anytype` 参数则让编译器按调用点实际类型实例化函数（隐式泛型），配合 `@hasDecl`/`@hasField`/`@typeInfo` 可以在编译期断言"这个类型有 `area` 方法"，这就是 Zig 的 duck typing。与 Rust 的 `dyn Trait` 相比，Zig 的接口不携带类型标识，因此不能可靠地做 `downcast`（也没法检查两个接口是否指向同一个对象）；与 Go 的接口相比，Zig 不自动生成方法集，必须手写 `shape()` 这样的适配函数。取舍很清楚：接口数量少、性能敏感、愿意手写胶水代码时 Zig 的显式方案最直接。

📘 [Zig · Documentation](https://ziglang.org/documentation/master/) ｜ 📘 [Zig · `std.mem.Allocator`](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的多态完全由元表查找实现：`obj:method()` 先查 `obj` 自己的键，没有就沿 `__index` 链向上找，找到的第一个函数就是被调用的实现。所以"覆盖"就是**在更靠近实例的那张表里放同名键**，"super 调用"就是显式去父原型表里取函数（`Animal.speak(self)`）。没有关键字，也没有任何编译期检查。

```lua
local Animal = {}
Animal.__index = Animal
function Animal.new(name) return setmetatable({ name = name }, Animal) end
function Animal:speak() return "..." end
function Animal:describe() return self.name .. ": " .. self:speak() end

local Dog = setmetatable({}, { __index = Animal })
Dog.__index = Dog
function Dog.new(name)
  local self = Animal.new(name)
  return setmetatable(self, Dog)          -- 换成 Dog 原型
end
function Dog:speak() return "Woof" end    -- 覆盖（更近的一层）
function Dog:describe()
  return "dog " .. Animal.describe(self)  -- 显式调用父原型实现（super）
end

local d = Dog.new("Rex")
print(d:describe())          -- dog Rex: Woof
print(d:speak())             -- Woof
print(Animal.speak(d))       -- ...：显式选父实现
print(getmetatable(d) == Dog, Dog.__index == Dog)  -- true true
print(rawget(d, "speak"))    -- nil：方法在原型上
```

动态派发的成本就是一次或多次表查找（`__index` 是表时循环上溯，是函数时调用函数），因此深度继承链在 Lua 里会明显变慢，实践中更常见的做法是深度不超过 2 到 3 层，或者用"拷贝方法"的 mixin（`for k, v in pairs(Animal) do if Dog[k] == nil then Dog[k] = v end end`）把链压平。`self:speak()` 里的冒号是语法糖，等价于 `self.speak(self)`，所以覆盖要生效必须用冒号调用（或用 `obj.speak(obj)`），写成 `obj.speak()` 会丢 `self`。多态派发在 `describe` 里发生，因此子类不必改 `describe` 就能改变行为——这是模板方法模式在 Lua 里的标准形态。Lua 5.5 把 `global` 加进了保留字表，并新增了 `global` 声明语句，但**默认仍然是 global-by-default**：每个 chunk 等价于以 `global *` 开头，写 `x = 1` 依旧会创建全局变量，只有显式写出 `global` 声明（例如 `global x`，或 `global<const> *` 把未声明的自由名字全部变成只读）才会取消这个默认、让未声明的名字报错；所以"必须写 `_G.x` 才能改全局"是误传。同一版本起，数值 `for` 与泛型 `for` 的控制变量都是只读（`const`）变量，循环体里给它赋值会直接报错，这也顺带挡住了把循环变量误当成全局或原型表成员改写的写法。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4) ｜ 📘 [Lua · Programming in Lua · Inheritance](https://www.lua.org/pil/16.2.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的覆盖规则是"编译期检查 + 运行时 JavaScript 原型"：`override` 关键字（4.3 起）在开启 `noImplicitOverride` 或显式书写时会校验"父类确实有这个方法"，`abstract` 成员必须在具体子类中实现，`abstract class` 不能实例化——但这些约束**只在编译期**存在。接口之间可以 `extends` 多个接口，同名接口会自动声明合并。

```typescript
abstract class Animal {                       // abstract：编译期约束
  constructor(public readonly name: string) {}
  speak(): string { return "..."; }
  abstract kind(): string;                    // 子类必须实现
  describe(): string { return `${this.name}: ${this.speak()}`; }
}

class Dog extends Animal {
  override speak(): string { return "Woof"; } // override 让编译器校验
  kind(): string { return "dog"; }
}

class Puppy extends Dog {
  override describe(): string { return "puppy " + super.describe(); }  // super 调用
}

interface Named { label: string; }
interface Aged { age: number; }
interface Named { extra?: boolean; }          // 声明合并：与上一个 Named 合成
interface Person extends Named, Aged {}       // 接口多继承

const p: Person = { label: "x", age: 3, extra: true };
const animals: Animal[] = [new Dog("Rex"), new Puppy("Yip")];
console.log(animals[0].describe());           // Rex: Woof
console.log(animals[1].describe());           // puppy Yip: Woof
console.log(p.label, p.age);                  // x 3
// const a = new Animal("x");                 // 🛑 编译错误：抽象类不能实例化
console.log(Object.getPrototypeOf(Puppy.prototype) === Dog.prototype);  // true
```

`override` 与 `abstract` 都是**类型层面的检查**：编译产物里没有它们，运行时 `Animal` 依然可以被 `new`（因为 `abstract` 被擦除），要真正防止实例化必须再加运行时守卫（例如构造器里检查 `new.target === Animal` 就抛错）。`super.describe()` 编译成 `Dog.prototype.describe.call(this)` 之类的形式，是真正的原型链调用。`implements` 只检查类的实例侧形状，不检查静态成员，也不会把接口成员"实现"进类（没有默认实现——接口的默认实现需要用抽象类或 mixin 函数）。TypeScript 的协变返回类型由类型检查器判断：子类重写方法返回更具体的类型是允许的（`string` 覆盖 `string | number` 不行，但 `"a"` 覆盖 `string` 可以），方法参数则是双变（bivariant）的（除非开启 `strictFunctionTypes`，方法参数仍然保留双变以兼容常见写法）。需要菱形默认实现时用 mixin 函数或抽象基类，TypeScript 没有接口默认方法。

📘 [TypeScript · Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html) ｜ 📘 [TypeScript · Declaration merging](https://www.typescriptlang.org/docs/handbook/declaration-merging.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的"覆盖"就是往原型链更近的一层写同名方法：实例自己的属性最优先，其次是自己构造函数的 `prototype`，再沿 `[[Prototype]]` 向上。没有 `abstract`、没有接口、没有访问控制，覆盖完全是运行时行为——方法可以在对象创建之后被替换。

```javascript
class Base {
  name() { return "Base"; }
  size() { return 0; }
}
class Sub extends Base {
  constructor() { super(); this.extra = 7; }
  name() { return "Sub" + this.extra; }        // 覆盖：写在 Sub.prototype 上
  size() { return this.extra; }
}
const s = new Sub();
console.log(s.name(), s.size());               // Sub7 7
// 显式调用被覆盖的父实现：直接在父原型上取函数并绑定 this
console.log(Base.prototype.name.call(s), Base.prototype.size.call(s));  // Base 0
console.log(Object.hasOwn(Sub.prototype, "name"));   // true：方法在原型上
console.log(Object.hasOwn(s, "name"));                // false：实例上没有

// 运行时改原型会影响已有实例（危险，但也很有用）
const saved = Sub.prototype.name;
Sub.prototype.name = function () { return "patched"; };
console.log(s.name());                          // patched
Sub.prototype.name = saved;

// mixin：没有多继承，只能把方法拷进原型
const Loud = { loud() { return this.name().toUpperCase(); } };
Object.assign(Sub.prototype, Loud);
console.log(s.loud());                          // SUB7
```

`super.name()` 在类方法里等价于在父原型上找 `name` 并绑定当前 `this`，构造函数里 `super()` 必须在 `this` 之前调用。方法定义在原型上是共享的（`hasOwn` 为 `false`），因此修改原型会影响所有实例——上面 `Sub.prototype.name` 的一次赋值让已有实例 `s` 立即改变行为，这既是热修补能力也是事故来源。没有多继承，横向复用靠 `Object.assign(Target.prototype, Mixin)` 或高阶 mixin 函数 `class extends Mixin(Base)`；用 `Object.assign` 会丢失 `super` 的链接（因为方法被复制成普通函数，`super` 在对象字面量方法里不可用），要保留 `super` 就得用高阶函数形式。`Object.getPrototypeOf` 与 `Object.setPrototypeOf` 可以运行期改链，但后者会让 V8 弃用该对象的快速属性访问（hidden class 失效），性能敏感场景应避免。

📘 [MDN · Classes](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes) ｜ 📘 [MDN · super](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/super)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的方法默认可以被重定义，`final` 阻止重定义（可用于方法或类），`abstract` 要求子类实现，接口只声明契约（PHP 的接口**没有**默认方法体），trait 提供横向实现复用。PHP 8.0 起支持 `mixed`、联合类型、构造器属性提升；`#[\Override]` 属性自 PHP 8.3 起可用，PHP 8.5 起还可用于属性，它把"确实重写了父类方法"从约定变成编译期错误，思路与 Java 的 `@Override` 一致。

```php
<?php
abstract class Animal {
    public function __construct(protected string $name) {}
    abstract public function speak(): string;      // 抽象方法
    public function describe(): string {           // 模板方法
        return "{$this->name}: {$this->speak()}";
    }
    final public function id(): string { return "animal:{$this->name}"; }
}

class Dog extends Animal {
    #[\Override]                                    // PHP 8.3+：校验确实重写了父方法
    public function speak(): string { return "Woof"; }
    public function describe(): string { return "dog " . parent::describe(); }  // parent::
}

trait Loud {
    public function loud(string $s): string { return strtoupper($s); }
}

interface Shape { public function area(): float; }

final class Circle implements Shape {               // final class：禁止继承
    use Loud;                                       // trait：横向复用
    public function __construct(private float $r) {}
    public function area(): float { return 3.0 * $this->r ** 2; }
    public function shout(): string { return $this->loud("circle"); }
}

$animals = [new Dog("Rex")];
echo $animals[0]->describe(), PHP_EOL;      // dog Rex: Woof
echo $animals[0]->id(), PHP_EOL;            // animal:Rex
$c = new Circle(2.0);
echo $c->area(), PHP_EOL;                   // 12
echo $c->shout(), PHP_EOL;                  // CIRCLE
var_dump($c instanceof Shape, $c instanceof Circle);  // true true
// $c instanceof Loud                        // 🛑 trait 不是类型，不能 instanceof
```

`parent::describe()` 是 PHP 的父类实现调用语法（`parent::` 静态解析到直接父类，不是 `$this->` 的动态查找）；`static::` 则是后期静态绑定，会派发到运行时的类。抽象类可以有构造器与字段（`protected string $name`），接口只能有常量与方法签名，因此"共享状态 + 默认实现"必须用抽象类或 trait，不能用接口。trait 的冲突必须显式解决：`use A, B { A::hello insteadof B; B::hello as helloB; }`；`insteadof` 选一个，`as` 给另一个改名保留，都不写就是致命错误。`#[\Override]` 自 PHP 8.3 起可用（8.5 起扩展到属性），典型用途是防止重构时父类方法改名导致子类方法静默变成新方法。PHP 里所有非 `final`、非 `private`、非 `static` 的实例方法都是虚方法，调用通过对象的类表派发，`final` 让引擎可以走更快的直接路径。PHP 8.4 起属性也能带 hook（`get`/`set`），hook 同样可继承、可覆盖：子类可以只重写其中一个 hook 并用 `parent::$prop::get()` 显式调用父实现，`final` hook 禁止被覆盖，属性整体声明为 `final` 时子类完全不能重新声明它——这把"属性访问"也纳入了覆盖体系，成为 trait 与抽象类之外的第三个横向复用点。

📘 [PHP · Object Inheritance](https://www.php.net/manual/en/language.oop5.inheritance.php) ｜ 📘 [PHP · Traits](https://www.php.net/manual/en/language.oop5.traits.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的方法查找完全沿 `ancestors` 链进行：单件类（singleton class）→ `prepend` 的 module → 类自己 → `include` 的 module（按 include 的逆序）→ 父类，以此类推。因此"覆盖"不需要关键字，只要在更靠前的链节上定义同名方法；`super` 沿链继续向上找下一个定义，是 Ruby 里最常用的父类调用语法。

```ruby
class Animal
  def initialize(name) = @name = name
  def speak = "..."
  def describe = "#{@name}: #{speak}"          # 模板方法
end

class Dog < Animal
  def speak = "Woof"
  def describe = "dog " + super                # super：链上的下一个 describe
end

module Over
  def describe = "over+" + super                # prepend 后位于 Dog 之前
end
class Cat < Animal
  prepend Over
  def speak = "Meow"
end

puts Dog.new("Rex").describe  # dog Rex: Woof
puts Cat.new("Tom").describe  # over+Tom: Meow
puts Dog.ancestors.take(3).inspect  # [Dog, Animal, Object]
puts Cat.ancestors.take(3).inspect  # [Over, Cat, Animal]

module Greet
  def greet = "hi #{self.class}"
end
class Dog; include Greet; end
puts Dog.new("Rex").greet     # hi Dog
puts Dog.ancestors.include?(Greet)   # true
puts Dog.new("Rex").respond_to?(:greet)  # true
```

`super` 不带括号时会**原样转发全部参数**（包括块），`super()` 才是不传参数，这是 Ruby 里非常常见的坑（父类 `initialize` 参数个数不对时就会暴露）。`prepend` 的 module 排在整个类之前，因此它的 `describe` 会先被调用，而它内部的 `super` 落到 `Dog#describe`——这种"环绕"能力是 Ruby 实现装饰器、日志、缓存的标准手法，AOP 风格的 gem 大量依赖它。`respond_to?` 与 `method(:speak)` 可以在运行时查询方法归属（`Dog.instance_method(:describe).owner` 给出定义所在的类或 module），这是有反射的 Ruby 比静态语言调试覆盖问题时更省事的地方。单继承 + module 的组合意味着 Ruby 没有菱形继承，但**同一 module 被多条路径 include 时只会插入一次**（Ruby 会去重），顺序依赖依然存在。

📘 [Ruby · Modules and classes](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html) ｜ 📘 [Ruby · Method lookup](https://docs.ruby-lang.org/en/master/Module.html#method-i-ancestors)

{{% /tab %}}

{{< /tabpane >}}

### 没有继承的语言怎么复用

把"复用"从"继承"里拆出来看，会发现没有继承的语言并不缺工具，只是换了默认姿势：Rust 用 trait 与 blanket impl，Go 用嵌入与接口组合，Julia 用抽象类型加多分派，Zig 用 `comptime`，Lua 用 `__index` 原型链，C 用首成员布局与函数指针表，R 用泛型函数分派。即使是有继承的语言，也普遍提供了这套"不用继承的复用"补充方案：Python 与 Ruby 的 mixin、Kotlin 的接口委托、Swift 与 Dart 的协议或 mixin、TypeScript 与 JavaScript 的 mixin 函数、PHP 的 trait、Java 与 C# 的默认方法加组合。这一节逐语言给出可用的替代方案与各自的取舍。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的复用全部通过 trait 完成，有四层工具：**trait 默认方法**（提供实现）、**blanket impl**（给所有满足约束的类型批量实现）、**trait 对象 `dyn`**（运行期异构集合）、以及**mixin 模式**（用 `Self: Sized` 的默认方法给类型"附加"能力）。没有字段继承，所以共享数据一律靠组合。

```rust
trait Named { fn name(&self) -> String; }
trait Greet: Named {                                  // 父 trait 约束
    fn hello(&self) -> String { format!("hi {}", self.name()) }   // 默认方法
}
impl<T: Named> Greet for T {}                         // blanket impl：所有 Named 自动 Greet

struct User { id: u32 }
impl Named for User { fn name(&self) -> String { format!("user#{}", self.id) } }
struct Robot;
impl Named for Robot { fn name(&self) -> String { "robot".into() } }

trait Timestamped: Sized {                            // mixin 模式
    fn touch(self) -> Self { self }
}
impl Timestamped for User {}

fn main() {
    println!("{}", User { id: 7 }.hello());           // hi user#7
    println!("{}", Robot.hello());                    // hi robot
    let objs: Vec<Box<dyn Greet>> = vec![Box::new(User { id: 1 }), Box::new(Robot)];
    for o in &objs { println!("{}", o.hello()); }     // hi user#1 / hi robot
    println!("{}", User { id: 7 }.touch().name());    // user#7
}
```

`trait Greet: Named` 是 supertrait 约束：任何实现 `Greet` 的类型必须同时实现 `Named`，因此默认方法里可以调用 `self.name()`。blanket impl（`impl<T: Named> Greet for T`）让新能力自动覆盖所有既有类型，标准库用同样的手法给所有 `Display` 类型实现 `ToString`；它的风险是"全局唯一性"——同一对（trait, 类型）只能有一份 impl，所以 blanket impl 一旦发布就很难再加特例，否则会与用户自己的 impl 冲突（`E0119`）。`dyn Greet` 与泛型的选择标准是"是否需要异构集合"：`Vec<Box<dyn Greet>>` 能同时装 `User` 与 `Robot`，代价是堆分配与间接调用；`fn f<T: Greet>(t: T)` 零开销但每种类型生成一份代码。mixin 模式用带 `Self: Sized` 约束的默认方法给类型附加链式能力，但它不能给类型加字段——要加状态只能组合一个结构体字段。

📘 [Rust · Traits](https://doc.rust-lang.org/book/ch10-02-traits.html) ｜ 📘 [Rust Reference · Trait objects](https://doc.rust-lang.org/reference/types/trait-object.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的"不用继承的复用"有两个主角：**协议扩展**（给所有遵循者提供默认实现）与**协议组合**（`A & B` 表达"同时满足多个协议"）。值类型（`struct`/`enum`）不能继承，但可以遵循协议并复用扩展里的实现，因此 Swift 里大量横向复用发生在协议层而不是类层次。

```swift
protocol Named { var name: String { get } }
protocol Greet {
    func hello() -> String
}
extension Greet where Self: Named {                 // 条件扩展：约束下的默认实现
    func hello() -> String { "hi \(name)" }
}
struct User: Named, Greet { var name: String }
struct Robot: Named, Greet { var name: String }

protocol Aged { var age: Int { get } }
typealias NamedAged = Named & Aged                  // 协议组合
struct Person: Named, Aged { var name: String; var age: Int }

func describe(_ x: any NamedAged) -> String { "\(x.name)/\(x.age)" }

print(User(name: "Rex").hello())          // hi Rex
print(Robot(name: "R2").hello())          // hi R2
print(describe(Person(name: "Al", age: 30)))  // Al/30
func helloAll(_ xs: [any Greet & Named]) -> [String] { xs.map { $0.hello() } }
print(helloAll([User(name: "A"), Robot(name: "B")]))  // ["hi A", "hi B"]
```

协议扩展最大的优势是**可以给别人的类型加能力**：`extension Greet where Self: Named` 不要求 `User` 与 `Robot` 有任何共同父类，只需各自遵循协议；`typealias NamedAged = Named & Aged` 让"同时满足两个协议"成为可命名的类型，`any NamedAged` 则把它做成 existential。代价是前面提过的派发规则：协议扩展的方法在 existential 上是静态派发的，且**不能**做成协议要求之外的重载分派点；如果某个遵循者自己实现了同名方法，通过 `any` 调用仍然走扩展版本。协议组合还能用于泛型约束（`func f<T: Named & Aged>(_ t: T)`），这时没有装箱开销，但函数体内对协议要求的调用仍默认走 witness table，编译器只在看得到具体类型时才特化。取舍是：需要为类型家族共享实现且要求"是一个"的语义时用类继承加 `override`，需要横切能力、想让值类型也参与时用协议扩展加组合，想避免 existential 的间接调用就用 `some` 或泛型约束。

📘 [Swift · Protocols](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/) ｜ 📘 [Swift · Protocol compositions](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/#Protocol-Composition)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的复用只有两件工具：**结构体嵌入**（字段与方法提升，等价于组合的语法糖）与**接口组合**（把多个接口的方法集并起来）。它们都刻意不提供"实现继承"：嵌入不会把你变成父类型，接口不能带实现，因此也没有虚表。

```go
package main

import "fmt"

type Animal struct{ Name string }

func (a Animal) Kind() string { return "animal:" + a.Name }

type Dog struct {
	Animal                              // 嵌入：字段与方法被提升
	Breed  string
}

type Speaker interface{ Kind() string }
type Walker interface{ Walk() string }

type DogWalker interface {               // 接口组合：方法集并集
	Speaker
	Walker
}

func (d Dog) Walk() string { return d.Name + " walks" }

func main() {
	d := Dog{Animal{"Rex"}, "poodle"}
	fmt.Println(d.Kind())     // animal:Rex：方法提升
	var w DogWalker = d
	fmt.Println(w.Walk())     // Rex walks
	fmt.Println(w.Kind())     // animal:Rex
	var s Speaker = d         // 隐式满足接口
	fmt.Println(s.Kind())     // animal:Rex
	fmt.Println(d.Animal.Kind())  // animal:Rex：显式取嵌入字段
}
```

嵌入的语义是"字段提升 + 方法提升"：`d.Kind()` 编译成 `d.Animal.Kind()`，接口方法集也把嵌入类型的方法算进来，所以 `Dog` 自动满足 `Speaker`。它的价值在于把共享实现放在一个基础结构体里、被多个类型嵌入，从而实现类似"多继承实现"的效果，同时仍然保留 Go 的扁平类型系统。取舍与陷阱：提升的方法里 `self` 是**嵌入的那个内层值**，不是外层值——如果 `Animal` 的某个方法内部调用另一个被外层遮蔽的方法，得到的仍是 `Animal` 的版本（没有 vtable）；要让外层行为生效，必须在外层显式实现该方法。接口组合不是继承：`DogWalker` 不能给 `Dog` 增加任何实现，它只是要求"同时具备两组方法"。Go 1.18 起的泛型把"约束"也交给接口：约束里可以写 union 类型集（例如 `interface{ ~int | ~string }`），但**含类型集的接口只能当类型参数约束**，不能用来声明变量、字段或参数——规范原文是这类接口 "cannot be the types of values or variables"，所以 `var x interface{ ~int | ~string }` 直接编译失败（报 `interface contains type constraints`），这与 Rust 的 `dyn Trait`（trait 可以当类型）、Zig 的接口结构体（普通 struct）形成鲜明对照。跨类型共享状态用嵌入、共享契约用接口、需要运行期异构集合用 `[]Speaker`、需要编译期约束用类型参数，这是 Go 里替代继承的固定搭配。

📘 [Go spec · Struct types](https://go.dev/ref/spec#Struct_types) ｜ 📘 [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有继承也能复用，而且方式很多：**mixin**（只提供方法、不单独实例化的类）、**`Protocol`**（结构化子类型，不要求继承关系）、**组合加 `__getattr__` 转发**、以及**猴子补丁**（给类动态加方法）。mixin 实际上仍然通过继承实现，但语义上只是"把一组方法拷进来"；`Protocol` 则完全绕开了继承。

```python
class JsonMixin:
    def to_json(self) -> str:                 # mixin：假定子类有可序列化字段
        import json
        return json.dumps({k: v for k, v in vars(self).items()})

class Point(JsonMixin):
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

print(Point(1, 2).to_json())                  # {"x": 1, "y": 2}

from typing import Protocol, runtime_checkable

@runtime_checkable
class Sized(Protocol):                        # 结构化子类型
    def __len__(self) -> int: ...

def size_of(x: Sized) -> int: return len(x)

print(size_of([1, 2, 3]))                     # 3
print(isinstance([1, 2], Sized))              # True（不改 list 的定义）
print(isinstance(42, Sized))                  # False

class Registry:
    def __init__(self) -> None: self._d: dict[str, object] = {}
    def __setitem__(self, k: str, v: object) -> None: self._d[k] = v
    def __len__(self) -> int: return len(self._d)

print(isinstance(Registry(), Sized))          # True（隐式满足协议）
```

`vars(self)` 拿到实例的 `__dict__`，这是 mixin 依赖子类"字段都放在实例字典里"的隐式契约——用 `__slots__` 的类会让 `to_json` 直接报错，这是 mixin 与传统继承一样脆弱的地方。`Protocol` 的好处是 `list`、`Registry` 这些互不相关的类型不需要声明继承关系就能被 `size_of` 接受，检查只在静态类型检查器（mypy、pyright）里做，`@runtime_checkable` 才额外提供运行时的 `isinstance`（它只检查方法是否存在，不检查签名）。组合加 `__getattr__` 可以做到零代码转发（`def __getattr__(self, k): return getattr(self._inner, k)`），适合包装第三方对象。真正需要"共享状态 + 默认实现"时用普通基类或 `ABC`；只想共享无状态行为时用 mixin 或 `Protocol`，后者不会污染 MRO。

📘 [Python · Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) ｜ 📘 [Python · Multiple inheritance / mixins](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的类默认 `final`，所以"复用"的首选不是继承而是**接口加 `by` 委托**与**扩展函数**：前者把接口实现转发给另一个对象（编译期生成转发代码，不改祖先链），后者给已有类型附加函数而不修改它。只有确实需要共享状态与构造逻辑时才用 `open class`。

```kotlin
interface Logger { fun log(msg: String): String }
class ConsoleLogger : Logger {                       // 真正的实现
    override fun log(msg: String) = "[console] $msg"
}
class Service(logger: Logger) : Logger by logger     // 委托：自动转发 log
class Timestamped : Logger {
    override fun log(msg: String) = "[ts] $msg"
}
class Both(private val a: Logger, private val b: Logger) : Logger by a {  // 委托给 a，覆盖后再补 b
    override fun log(msg: String) = a.log(msg) + "|" + b.log(msg)
}
fun String.shout(): String = uppercase() + "!"       // 扩展函数
fun Logger.logTwice(msg: String) = log(msg) + log(msg)  // 给接口加扩展

fun main() {
    println(Service(ConsoleLogger()).log("hi"))      // [console] hi
    println("hey".shout())                            // HEY!
    println(ConsoleLogger().logTwice("x"))            // [console] x[console] x
    println(Timestamped().log("t"))                   // [ts] t
}
```

`class Service(logger: Logger) : Logger by logger` 生成的 `log` 直接调用 `logger.log`，因此委托对象是可替换的策略；委托成员可以直接当自己的成员使用（`Both` 没覆盖 `log` 时，`log("x")` 就等于 `a.log("x")`）。想在委托之上加逻辑就必须显式覆盖，而覆盖里不能用 `super.log()` 回到委托实现——要把委托对象声明成 `private val` 属性（如 `Both` 里的 `a`），覆盖时显式写 `a.log(msg)`；构造参数如果只写成 `a: Logger`（没有 `val`），它在成员函数体里根本不可见，这是 Kotlin 新手最常撞的一条规则。扩展函数是**静态解析**的：调用哪个版本取决于变量的静态类型，而不是运行时类型——`open class` 定义的成员函数优先于扩展函数，成员与扩展同名时成员赢，扩展之间同名时作用域更具体的赢。扩展函数不能访问私有成员，也不能在子类里被"覆盖"。取舍很清楚：需要横向共享行为且不涉及状态，用接口默认实现或扩展；需要把实现来源参数化，用 `by` 委托；需要共享字段与构造流程，才用 `open class` 加 `abstract`。

📘 [Kotlin · Delegation](https://kotlinlang.org/docs/delegation.html) ｜ 📘 [Kotlin · Extensions](https://kotlinlang.org/docs/extensions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 只有单继承，所以"不用继承的复用"主要落在三处：**接口默认方法**（无状态的实现复用）、**组合加转发**（持有委托对象并转发调用）、以及**静态工具方法**。Java 8 之前接口不能带实现，那时横向复用只能靠组合或复制代码；默认方法补上了"给接口加方法"这一格，但仍然不允许状态。

```java
interface Logger { String log(String msg); }
interface Prefixing extends Logger {
    String prefix();
    @Override default String log(String msg) { return prefix() + msg; }  // 无状态默认实现
}

class ConsoleLogger implements Logger {
    public String log(String msg) { return "[console] " + msg; }
}
class TaggedLogger implements Prefixing {
    private final Logger inner;                       // 组合：持有委托对象
    TaggedLogger(Logger inner) { this.inner = inner; }
    public String prefix() { return "[tag] "; }
    public String log(String msg) { return prefix() + inner.log(msg); }  // 显式转发
}
class TimestampLogger implements Logger {             // 用默认方法零代码获得 log
    private final Logger inner;
    TimestampLogger(Logger inner) { this.inner = inner; }
    public String log(String msg) { return "[ts] " + inner.log(msg); }
}

public class Main {
    static String twice(Logger l, String m) { return l.log(m) + l.log(m); }  // 面向接口
    public static void main(String[] args) {
        Logger l = new ConsoleLogger();
        System.out.println(new TaggedLogger(l).log("hi"));   // [tag] [console] hi
        System.out.println(new TimestampLogger(l).log("hi")); // [ts] [console] hi
        System.out.println(twice(l, "x"));                    // [console] x[console] x
    }
}
```

组合优于继承在这里体现得最清楚：`TaggedLogger` 与 `TimestampLogger` 都不继承 `ConsoleLogger`，而是持有一个 `Logger`，因此可以任意嵌套（装饰器模式），也不会被 `ConsoleLogger` 的实现变化牵连。代价是必须手写转发方法——方法多时非常啰嗦，这正是 Kotlin 用 `by`、Swift 用协议扩展、Dart 用 mixin、PHP 用 trait 想要省掉的样板。接口默认方法适合放**无状态**的派生逻辑（例如 `Comparator.thenComparing`、`Iterable.forEach`），一旦需要字段就必须换成抽象类，因为接口不能有实例字段（可以有 `static final` 常量）。Java 没有扩展方法（C# 有），要给别人的类型加方法只能用静态工具类（`Collections.sort`、`Objects.requireNonNull` 这类）或包装类，这也是 Java 生态里静态工具类特别多的原因。

📘 [Java · Default methods](https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html) ｜ 📘 [Java · Composition over inheritance](https://docs.oracle.com/javase/tutorial/java/IandI/objectclass.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有继承，但社区共识是"优先组合"，而在必须做静态多态时有两个零开销工具：**CRTP**（奇异递归模板模式，编译期多态）与 **`concepts`**（C++20 约束模板参数）。CRTP 让基类模板通过 `static_cast` 调用派生类的实现，完全不需要 vtable；`concepts` 则把"类型必须提供某方法"从文档约定变成编译期约束。

```cpp
#include <iostream>
#include <string>
#include <type_traits>

template <class D>
struct Shape {                                        // CRTP 基类
    double area() const { return static_cast<const D *>(this)->areaImpl(); }
    std::string describe() const { return "area=" + std::to_string(area()); }
};
struct Circle : Shape<Circle> {
    double r = 0;
    double areaImpl() const { return 3.0 * r * r; }
};
struct Square : Shape<Square> {
    double s = 0;
    double areaImpl() const { return s * s; }
};

template <class T>
concept HasArea = requires(T t) { { t.area() } -> std::convertible_to<double>; };

template <HasArea A, HasArea B>
double total(const A &a, const B &b) { return a.area() + b.area(); }

int main() {
    Circle c; c.r = 2.0;
    Square s; s.s = 3.0;
    std::cout << c.describe() << "\n";            // area=12.000000
    std::cout << total(c, s) << "\n";             // 21
    std::cout << sizeof(Circle) << " " << sizeof(Square) << "\n";  // 8 8
    std::cout << std::is_same_v<decltype(c.area()), double> << "\n";  // 1
}
```

CRTP 的机制是"派生类把自己作为模板参数传给基类"，于是基类的静态类型转换在编译期就解析到 `Circle::areaImpl`，调用可以被内联，对象里没有 vptr（`sizeof(Circle)` 只有 `double` 的 8 字节）。代价是：不同派生类的 CRTP 基类**不是同一个类型**，`Shape<Circle>` 与 `Shape<Square>` 无关，因此不能放进同一个容器，也不能用基类指针做运行期多态——这正是它与虚函数的分工（静态多态换性能，动态多态换异构集合）。`concept HasArea` 让 `total` 在实例化前就被检查：传入不满足的类型会得到一条清楚的"constraint not satisfied"错误，而不是几百行模板展开信息。真正需要运行期异构时还是得回到 `virtual` + `unique_ptr<Base>`，或者用 `std::variant` + `std::visit`（值语义的封闭多态）。mixin 在 C++ 里通常就写成带默认实现的模板基类或 CRTP 基类，配合 `using` 引入；`concepts` 还能替代 SFINAE 做重载约束，是 C++20 之后的首选。

📘 [cppreference · CRTP](https://en.cppreference.com/w/cpp/language/crtp) ｜ 📘 [cppreference · Constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints)

{{% /tab %}}

{{% tab header="C" %}}

C 的复用只有三条路：**结构体组合**、**首成员模拟单继承**、**函数指针表模拟多态**，再加上一个工程化答案——**GObject 模式**（把类结构体、实例结构体与函数表分开，用统一的 `new`/`finalize` 与引用计数管理生命周期）。这一节给出后两者的最小实现，展示 C 如何在没有语言支持的情况下做到"继承 + 虚析构"。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Animal Animal;
typedef struct AnimalClass {
    const char *(*speak)(const Animal *self);
    void (*finalize)(Animal *self);          /* 相当于虚析构 */
} AnimalClass;
struct Animal { const AnimalClass *klass; char *name; };   /* 首成员 = class 指针 */

static const char *animal_speak(const Animal *self) { (void)self; return "..."; }
static void animal_finalize(Animal *self) { free(self->name); free(self); }
static const AnimalClass ANIMAL_CLASS = { animal_speak, animal_finalize };

Animal *animal_new(const char *name) {
    Animal *a = malloc(sizeof *a);
    a->klass = &ANIMAL_CLASS;
    a->name = strdup(name);
    return a;
}

typedef struct { Animal parent; int bark_count; } Dog;      /* 派生：首成员 */
static const char *dog_speak(const Animal *self) {
    const Dog *d = (const Dog *)self;
    static char buf[64];
    snprintf(buf, sizeof buf, "Woof x%d", d->bark_count);
    return buf;
}
static void dog_finalize(Animal *self) { animal_finalize(self); }
static const AnimalClass DOG_CLASS = { dog_speak, dog_finalize };

Dog *dog_new(const char *name, int n) {
    Dog *d = malloc(sizeof *d);
    d->parent.klass = &DOG_CLASS;
    d->parent.name = strdup(name);
    d->bark_count = n;
    return d;
}

int main(void) {
    Animal *a = animal_new("x");
    Dog *d = dog_new("Rex", 3);
    Animal *objs[2] = { a, (Animal *)d };    /* 首成员布局：指针互转安全 */
    for (int i = 0; i < 2; i++) printf("%s\n", objs[i]->klass->speak(objs[i]));
    for (int i = 0; i < 2; i++) objs[i]->klass->finalize(objs[i]);   /* 虚析构 */
    return 0;
}
/* 输出：
...
Woof x3
*/
```

GObject 模式的核心就是把 C++ 编译器自动做的事全部写成约定：每个类有一份 `XxxClass` 结构体（vtable 加类级数据）、每个实例的第一成员是父类实例、`xxx_new` 负责分配与初始化、`finalize` 负责释放，构造函数里通常用 `g_object_new` 配合 `GObjectClass` 的 `constructor`/`constructed` 两阶段初始化来处理"构造期调用虚函数"的问题。这套约定能编译进插件系统并被语言绑定自动使用，代价是全靠人工遵守：没有编译期检查、没有 `override` 校验、没有 RAII，任何一步写错都是未定义行为。实践中若不需要跨语言绑定，直接用 C++ 更省事；若必须用 C（内核、驱动、嵌入式、跨语言 ABI），就接受这套手工纪律，并把它封装成宏来减少重复（内核的 `container_of`、GObject 的 `G_DEFINE_TYPE` 都是这个思路）。

📘 [C · struct](https://en.cppreference.com/w/c/language/struct) ｜ 📘 [GObject Reference Manual](https://docs.gtk.org/gobject/concepts.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的复用不依赖继承，而是三个正交机制的组合：**抽象类型**给出子类型关系、**多分派**把行为绑定到具体类型、**接口约定**（非正式但被 `Base` 文档化）规定"要实现哪几个方法才算支持某功能"。因此"给所有支持 `iterate` 的类型免费获得一堆函数"这件事，比类继承体系更松耦合。

```julia
abstract type Animal end                    # 只表达子类型关系
struct Dog <: Animal; name::String; end
struct Cat <: Animal; name::String; end

speak(::Animal) = "..."                     # 默认方法
speak(d::Dog) = "Woof $(d.name)"
speak(c::Cat) = "Meow $(c.name)"

struct Robot end                            # 与 Animal 无关，也能加入
speak(::Robot) = "beep"

describe(x) = "$(typeof(x)): $(speak(x))"   # 对所有类型通用
println(describe(Dog("Rex")))               # Dog: Woof Rex
println(describe(Robot()))                  # Robot: beep
println(Dog <: Animal, Robot <: Animal)     # true false
println(methods(speak))                     # 4 个方法

# 接口约定：只要实现了 iterate/length，就自动获得 collect、sum、for 等能力
struct Countdown; n::Int; end
Base.iterate(c::Countdown, i::Int = c.n) = i <= 0 ? nothing : (i, i - 1)
Base.length(c::Countdown) = c.n
println(collect(Countdown(3)))              # [3, 2, 1]
println(sum(c for c in Countdown(4)))       # 10
```

`Base.iterate` 与 `Base.length` 就是 Julia 的"接口"：实现了它们，`for`、`collect`、`sum`、`in`、`first` 等几十个函数自动可用，因为那些函数都是按 `iterate` 定义的泛型函数。这与继承体系的关键差异是**没有类型归属**——`Countdown` 不需要声明"我实现 Iterable 接口"，也不需要继承任何东西，只要方法签名齐全。代价是没有编译期检查：漏实现 `iterate` 时，错误在调用 `collect` 时才以 `MethodError` 出现（可以用 `hasmethod` 提前检查）。trait 库（如 SimpleTraits.jl、Traits.jl）补上了"声明式 trait"这一层：把"能做什么"与"是什么类型"分开，并用 `@traitimpl` 显式注册，从而让特化方法可以按能力而不是按类型书写。共享状态的复用一律靠组合字段或者把公共函数取出来调用——Julia 没有字段继承，抽象类型也装不下字段。

📘 [Julia · Interfaces](https://docs.julialang.org/en/v1/manual/interfaces/) ｜ 📘 [Julia · Methods](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的"不用继承的复用"比 Java 多两件武器：**默认接口实现**（C# 8，让接口也能带实现）与**扩展方法**（C# 3，让"给别人的类型加方法"成为库的一等公民）。再加上组合与 `partial`，就构成了完整的替代继承的工具箱。这里最该先记住的是扩展方法的解析规则：它是编译期的静态调用，**实例方法永远优先于扩展方法**。

```csharp
using System;
using System.Collections.Generic;

interface IProcessor<T> {
    T Process(T input);
    T ProcessTwice(T input) => Process(Process(input));   // C# 8 默认接口实现
}

class Trim : IProcessor<string> {
    public string Process(string input) => input.Trim();
}

static class ProcessorExtensions {                  // 扩展方法：静态类 + this 参数
    public static string Describe<T>(this IProcessor<T> p) => p.GetType().Name;
    public static IEnumerable<T> Repeat<T>(this IEnumerable<T> src, int n) {
        for (int i = 0; i < n; i++) foreach (var x in src) yield return x;
    }
}

class Counting<T> : IProcessor<T> {                 // 组合：持有被装饰的实现
    private readonly IProcessor<T> _inner;
    private int _count;
    public Counting(IProcessor<T> inner) => _inner = inner;
    public T Process(T input) { _count++; return _inner.Process(input); }
    public int Count => _count;
}

class Program {
    static void Main() {
        IProcessor<string> p = new Trim();
        Console.WriteLine(p.ProcessTwice("  hi  "));        // hi
        Console.WriteLine(p.Describe());                     // Trim
        Console.WriteLine(string.Join(",", new[] { 1, 2 }.Repeat(2)));  // 1,2,1,2
        var c = new Counting<string>(new Trim());
        c.Process("a"); c.Process("b");
        Console.WriteLine(c.Count);                          // 2
        // new Trim().ProcessTwice("x")                      // 🛑 编译错误：类类型看不到默认实现
    }
}
```

扩展方法的解析全部发生在编译期：`p.Describe()` 编译成静态调用 `ProcessorExtensions.Describe(p)`，因此它不能是虚方法、不能被覆盖、也不会出现在接口或基类的成员表里；遇到同名冲突时**实例方法优先**，没有实例方法时更内层命名空间或 `using static` 引入的候选优先。规则多、隐式候选集合大，是大型项目里"为什么调不到我的扩展方法"的常见原因，所以扩展方法应尽量少并放在专用命名空间。C# 14 又把这条路线推进了一步：**扩展成员（extension members）**允许在静态类里写 `extension(IShape s) { public double ScaledArea => ...; }` 这样的 extension block，从而给已有类型加扩展属性、扩展运算符、扩展静态成员，而不只是扩展方法；解析规则与扩展方法同源（编译期静态绑定、实例成员优先），所以表达力变强了，类型身份仍然不会变。默认接口实现（C# 8）只能通过接口类型调用，`IProcessor<T> p` 上能调 `ProcessTwice`，`new Trim()` 上不能；接口仍然不能声明实例字段，因此它只适合无状态的派生逻辑。需要"共享状态 + 部分实现"时，C# 的答案是抽象类（单继承）或组合（`Counting` 那样的装饰器）：装饰器可以任意嵌套、与被装饰类型解耦，是替代继承最稳妥的写法。`Partial` 只是把同一个类拆到多个文件，不解决复用问题，不要把它当继承的替身。

📘 [C# · Extension methods](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/extension-methods) ｜ 📘 [C# · Default interface methods](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interface-implementation/default-interface-methods-versions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的横向复用主角是 **mixin**：`mixin` 声明一组方法（可用 `on` 约束它能混入的父类型），`with` 把它们按顺序线性化进类。与 `implements` 相比 mixin 带实现，与 `extends` 相比 mixin 可以叠多个，因此 `extends` 的父类只有一个、`with` 后面却可以跟一串。Dart 3.0 起还可以用 `mixin class` 让同一个声明既能被继承也能被混入。

```dart
mixin Swimmer on Animal {                 // on 约束：只能混入 Animal 及其子类
  String swim() => "$name is swimming";
}

mixin Loud {
  String loud(String s) => s.toUpperCase();
}

abstract class Animal {
  final String name;
  Animal(this.name);
  String speak() => "...";
  String describe() => "$name: ${speak()}";
}

class Duck extends Animal with Swimmer, Loud {   // 线性化：Swimmer 在前、Loud 在后
  Duck(super.name);
  @override
  String speak() => loud("quack");               // 可直接用 mixin 方法
}

class Silent extends Animal with Loud {
  Silent(super.name);                            // 不覆盖 speak，沿用父实现
}

void main() {
  final d = Duck("Donald");
  print(d.speak());        // QUACK
  print(d.describe());     // Donald: QUACK
  print(d.swim());         // Donald is swimming
  print(d is Animal);      // true
  print(d is Swimmer);     // true：mixin 进入类型层次
  print(Silent("S").speak());  // ...
}
```

mixin 与 `implements` 的关键区别是：`with` 的 mixin **进入 `is` 关系**（`d is Swimmer` 为 `true`，Dart 会为 mixin 应用生成一个合成超类），`implements` 不会，因此需要"这个对象确实具备某能力"的运行期判断时用 mixin。`on Animal` 让 mixin 里可以访问 `name`，同时限制它只能被 `Animal` 的子类混入；没有 `on` 的 mixin 只能访问 `Object` 的成员。多个 mixin 有同名成员时按 `with` 的顺序线性化、**后写的覆盖先写的**，`super` 沿线性化顺序指向上一层，这与 Python 的 MRO、Ruby 的 `include` 属于同一类规则。`mixin class`（Dart 3.0）让一个声明既能被 `extends` 也能被 `with`，但不能同时是 `sealed`/`base`/`final`/`interface`。选型上：需要共享状态与方法且要求类型身份就用 mixin，只需要接口契约就用 `implements` 或 `interface class`，需要单线继承加少量横切能力就用 `extends` 配 `with`，只想给已有类型换一套静态接口就用 `extension type`。Dart 3.3 起提供的 `extension type`（例如 `extension type IdNumber(int id) { operator <(IdNumber o) => id < o.id; }`）是纯静态的包装：只在编译期生效、运行时被擦除且不产生包装对象，默认只暴露你显式声明的成员，想复用一个成员就得把它的声明抄一遍；它不建立运行期的 `is` 关系，只能通过 `implements` 声明与表示类型或其它 extension type 的静态子类型关系，因此"对象到底是不是某个类型"这类运行期判断仍然只能靠类层次或 mixin。

📘 [Dart · Mixins](https://dart.dev/language/mixins) ｜ 📘 [Dart · Class modifiers](https://dart.dev/language/class-modifiers)

{{% /tab %}}

{{% tab header="R" %}}

R 的复用方式按"正式程度"排成一条线：**S3**（函数名分派加 class 属性）、**S4**（正式类定义加槽位校验）、**R6/R5**（引用语义类）、**proto**（原型式对象）、**vctrs**（面向 tidyverse 的向量类，把 S3 类型做成类型安全的子类）。选哪一层取决于要不要类型校验、要不要引用语义、要不要与 tidyverse 兼容。

```r
# S3：给已有泛型函数加方法 = 复用
format_stats <- function(x, ...) UseMethod("format_stats")
format_stats.default <- function(x, ...) paste("n =", length(x))
format_stats.numeric <- function(x, ...) paste("mean =", round(mean(x), 2))
print(format_stats(1:3))          # [1] "mean = 2"
print(format_stats(letters))      # [1] "n = 26"

# S3 + 构造器：把 class 属性作为唯一契约
new_animal <- function(name, cls = "animal") structure(list(name = name), class = c(cls, "animal"))
speak <- function(x, ...) UseMethod("speak")
speak.animal <- function(x, ...) "..."
speak.cat <- function(x, ...) paste("Meow", x$name)
print(speak(new_animal("Tom", "cat")))   # [1] "Meow Tom"

# S4：正式类，带槽位类型校验与继承
setClass("Animal4", representation(name = "character"))
setClass("Cat4", contains = "Animal4")
setGeneric("speak4", function(x) standardGeneric("speak4"))
setMethod("speak4", "Animal4", function(x) "...")
setMethod("speak4", "Cat4", function(x) paste("Meow", x@name))
print(speak4(new("Cat4", name = "Tom")))  # [1] "Meow Tom"
print(is(new("Cat4", name = "Tom"), "Animal4"))  # [1] TRUE

# proto：原型式对象（无类定义，直接改对象）
library(proto)
p <- proto(name = "Rex", speak = function(.) paste("Woof", .$name))
print(p$speak())                  # [1] "Woof Rex"
q <- p$proto(name = "Tom")        # 派生：继承 p 的方法与字段
print(q$speak())                  # [1] "Woof Tom"
```

S3 的"复用"完全发生在函数名层面：`format_stats.numeric` 之所以被选中，只因为 `class(1:3)` 是 `"numeric"`；没有类定义、没有字段检查，`new_animal` 返回的就是个普通 list，谁都可以给它加 `class`。S4 用 `setClass` 声明槽位与类型，`contains` 形成单继承（可多父类），`setMethod` 分派时选最具体的类，代价是样板与性能开销。R6 用环境实现引用语义（`obj$method()` 改自身状态），适合状态机或长生命周期对象；`proto` 更轻，直接在对象上挂字段与方法，用 `$proto()` 派生。vctrs 的定位不同：它让 S3 类成为真正的"向量类型"（`new_vctr` 定义底层数据类型、`vec_ptype2` 定义类型提升、`vec_cast` 定义转换），从而既有 S3 的轻量又有接近 S4 的类型安全，是 tidyverse 生态推荐的自定义向量类方案。取舍原则：内部脚本用 S3；对外发布、要求字段校验用 S4 或 R6；要进入 dplyr/tibble 的列用 vctrs。

📘 [R · Method dispatch](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatching) ｜ 📘 [vctrs · S3 vectors](https://cran.r-project.org/web/packages/vctrs/vignettes/s3-vector.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 复用只有两个来源：**结构体组合**与 **`comptime`**。前者替代字段继承，后者替代泛型与"接口约定"：用 `comptime T: type` 或 `anytype` 让编译器按实际类型实例化函数，用 `@hasDecl`/`@hasField`/`@typeInfo` 在编译期断言类型提供了所需成员，用 `std.mem.Allocator` 那种结构体（数据指针 + 函数指针表）表达运行期接口。

```zig
const std = @import("std");

// comptime 泛型：为每种元素类型生成独立的实现
fn Stack(comptime T: type) type {
    return struct {
        items: []T,
        len: usize = 0,
        const Self = @This();
        fn push(self: *Self, v: T) void { self.items[self.len] = v; self.len += 1; }
        fn pop(self: *Self) ?T {
            if (self.len == 0) return null;
            self.len -= 1;
            return self.items[self.len];
        }
    };
}

// 编译期接口检查：要求类型有 area 与 name 声明
fn areaOf(comptime T: type, x: T) f64 {
    if (!@hasDecl(T, "area")) @compileError(@typeName(T) ++ " 缺少 area");
    return x.area();
}
const Circle = struct {
    r: f64,
    pub fn area(self: Circle) f64 { return 3.0 * self.r * self.r; }
    pub fn name(self: Circle) []const u8 { return "circle"; }
};

// 运行期接口：数据指针 + 函数指针表（手工 vtable）
const Shape = struct {
    ptr: *anyopaque,
    vtable: *const struct { area: *const fn (*anyopaque) f64 },
    fn area(self: Shape) f64 { return self.vtable.area(self.ptr); }
};

pub fn main() void {
    var buf: [8]i32 = undefined;
    var s = Stack(i32){ .items = &buf };
    s.push(1); s.push(2);
    std.debug.print("{?d}\n", .{s.pop()});          // 2
    std.debug.print("{?d}\n", .{s.pop()});          // 1
    std.debug.print("{d:.1}\n", .{areaOf(Circle, .{ .r = 2.0 })});  // 12.0
    var c = Circle{ .r = 1.0 };
    const sh = Shape{ .ptr = &c, .vtable = &.{ .area = struct {
        fn f(p: *anyopaque) f64 { return @as(*Circle, @ptrCast(@alignCast(p))).area(); }
    }.f } };
    std.debug.print("{d:.1}\n", .{sh.area()});      // 3.0
}
```

`Stack(T)` 是 Zig 的泛型：每次用新的 `T` 实例化都会生成一份独立的类型与代码（单态化），因此没有装箱与间接调用，代价是编译器要为每种类型编译一遍。`@hasDecl` + `@compileError` 把"这个类型必须提供 `area`"变成编译期错误，等价于 `concepts` 或 trait 约束，但完全靠库作者自己写检查——遇到不满足的类型得到的是你自定义的错误消息（这比 C++ 模板报错友好）。运行期接口必须自己定义结构体：`*anyopaque` 擦除类型、`@ptrCast` 加 `@alignCast` 恢复类型，vtable 是普通数据，所以可以运行时替换（也能做到"没有 RTTI 的 downcast"——你自己在接口里加一个类型标签字段）。取舍是：只需编译期多态就写 `comptime` 泛型（零开销、但代码膨胀），需要异构集合并要求 ABI 稳定就手工做 vtable（显式、可审计、没有隐藏分配）。Zig 不提供自动的混合（mixin），共享实现靠把公共字段放进一个结构体并被其他结构体嵌入使用。另外 Zig 0.15 把标准库集合也推向了"显式传 allocator"：`std.ArrayList` 现在就是非托管（unmanaged）版本，不再内嵌 allocator，`append`/`deinit` 都要显式传入 allocator，`std.ArrayListUnmanaged` 变成它的弃用别名，旧的托管版本移到已弃用的 `std.array_list.Managed`——这与 Zig "复用与资源都必须显式"的整体取向一致，写 0.14 之前的示例代码时要特别留意。

📘 [Zig · Documentation（comptime）](https://ziglang.org/documentation/master/#comptime) ｜ 📘 [Zig · `std.mem.Allocator`](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的复用围绕表与元表展开：**`__index` 原型链**实现方法共享、**中间类模式**把类本身也做成继承链（类方法沿 `getmetatable(c).__index` 向上找）、**compose** 把若干表的方法拷进目标表（真正的 mixin）。没有关键字，全部靠约定。

```lua
-- 一个极简 class 工厂：同时支持实例方法链与类方法链
local function class(parent)
  local c = {}
  c.__index = c
  if parent then setmetatable(c, { __index = parent }) end  -- 中间类：类方法也继承
  c.new = function(...)
    local obj = setmetatable({}, c)
    if obj.init then obj:init(...) end
    return obj
  end
  return c
end

local Animal = class()
function Animal:init(name) self.name = name end
function Animal:speak() return "..." end
function Animal:describe() return self.name .. ": " .. self:speak() end

local Dog = class(Animal)                       -- 原型链：Dog -> Animal
function Dog:speak() return "Woof" end
print(Dog.new("Rex"):describe())                -- Rex: Woof
print(getmetatable(Dog).__index == Animal)      -- true

-- compose：把若干表的方法并进目标（先到先得，不覆盖已有键）
local function compose(target, ...)
  for _, src in ipairs({ ... }) do
    for k, v in pairs(src) do
      if target[k] == nil then target[k] = v end
    end
  end
  return target
end
local Swimmer = { swim = function(self) return self.name .. " swims" end }
local Runner  = { run  = function(self) return self.name .. " runs" end }
compose(Dog, Swimmer, Runner)                   -- 多来源 mixin
print(Dog.new("Rex"):swim())                    -- Rex swims
print(Dog.new("Rex"):run())                     -- Rex runs
print(rawget(Dog, "swim") ~= nil)               -- true：方法被拷进 Dog 自身
```

`class(parent)` 里 `setmetatable(c, { __index = parent })` 让 `Dog` 的**类级**查找也走原型链，于是 `Dog.new` 这类类方法能被继承；`c.__index = c` 则负责实例级查找。compose 与继承的关键区别是"拷贝"还是"查链"：compose 把方法复制进目标表，因此运行期改源表不会影响已复用的类型，而且查找只有一层（更快），代价是失去动态派发——目标表里的方法一旦被调用就固定了实现，除非再 compose 一次。`if target[k] == nil` 保证先混入的优先，要"后者覆盖前者"就把条件去掉；这个小小的方向选择就是 mixin 冲突解决的全部。Lua 的常见工程做法是：数据组合用普通字段（`self.inner = ...`）、行为共享用 compose 或浅的原型链、需要运行期接口时用元表 `__index` 指向一个"接口表"，把"多态"限制在一层查找内。Lua 5.5 把 `global` 列为保留字并新增了 `global` 声明语句，但默认语义仍是 global-by-default（要杜绝误写全局得显式加 `global` 声明，或用 `global<const> *` 把自由名字变成只读）；同版本起 `for` 的控制变量是只读的 `const` 变量，循环体里不能再给它赋值。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4) ｜ 📘 [Lua · Programming in Lua · Inheritance](https://www.lua.org/pil/16.2.html)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的复用有三层：**接口组合与声明合并**（类型层面的横向拼装）、**mixin 函数**（运行时把行为叠加到类上，因为 `extends` 只能写一个父类）、以及**工具类型**（`Pick`、`Omit`、`Partial` 等对形状做变换）。类型层面的复用是零成本的，运行时复用要靠 mixin 或组合。

```typescript
interface Named { label: string; }
interface Aged { age: number; }
interface Serializable { toJSON(): string; }
interface Person extends Named, Aged {}          // 接口多继承（只拼类型）
interface Person extends Serializable { extra?: boolean; }  // 声明合并

const p: Person = { label: "x", age: 3, toJSON: () => "{}", extra: true };

// mixin 函数：约束构造函数类型，返回一个叠加了方法的子类
type Ctor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Ctor>(Base: TBase) {
  return class extends Base {
    stamp(): string { return `stamp:${JSON.stringify(this)}`; }
  };
}
function Named2<TBase extends Ctor>(Base: TBase) {
  return class extends Base {
    label(): string { return this.constructor.name; }
  };
}

class Entity { constructor(public id: number) {} }

class User extends Named2(Timestamped(Entity)) {  // 多个 mixin 叠加
  constructor(id: number, public userName: string) { super(id); }
}

const u = new User(7, "Rex");
console.log(u.stamp());                  // stamp:{"id":7,"userName":"Rex"}
console.log(u.label());                  // User
console.log(u instanceof Entity);        // true：原型链保留
type Summary = Pick<Person, "label" | "age">;   // 工具类型复用形状
const s: Summary = { label: "y", age: 1 };
console.log(s.label, p.extra);           // y true
```

`interface Person extends Named, Aged` 让接口可以同时继承多个其它接口，这是类型层面唯一"多继承"的地方，而且不会产生菱形问题（接口之间没有状态，冲突时同名成员类型必须兼容，否则报错）。`mixin 函数` 用 `TBase extends Ctor` 约束"可以 new 的类"，返回匿名子类，于是 `extends Named2(Timestamped(Entity))` 把两层行为串成一条原型链，`instanceof Entity` 依然为真。注意 `this` 在 mixin 返回的类里需要类型断言（`this as any`）才能访问叠加后的成员，这是 TypeScript mixin 的已知摩擦点；另外 `private`/`protected` 在 mixin 组合后不会自动合并（同名 private 成员会冲突报错）。工具类型（`Pick`/`Omit`/`Partial`/`Readonly`/`Required`）是"类型层面的组合优于继承"的直接体现：要复用一部分形状就派生一个映射类型，不必造一条继承链。运行时真的需要多继承语义时，只剩组合（持有对象）与 mixin 两条路。

📘 [TypeScript · Mixins](https://www.typescriptlang.org/docs/handbook/mixins.html) ｜ 📘 [TypeScript · Utility types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有接口、没有 trait，`extends` 也只能有一个父类，因此横向复用只有两条路：**高阶 mixin 函数**（`class extends Mixin(Base)`，保留原型链与 `super`）与 **`Object.assign` 拷贝**（最简单，但会丢 `super` 与身份）。此外还可以用组合加转发（`Forwardable` 式的委托）。

```javascript
const SerializableMixin = (Base) => class extends Base {
  toJSON() { return JSON.stringify({ ...this }); }
};
const TimestampMixin = (Base) => class extends Base {
  stamp() { return `${this.constructor.name}@${this.id}`; }
};

class Entity {
  constructor(id) { this.id = id; }
  name() { return `entity#${this.id}`; }
}
class User extends TimestampMixin(SerializableMixin(Entity)) {
  constructor(id, name) { super(id); this.userName = name; }
}
const u = new User(7, "Rex");
console.log(u.name());                 // entity#7
console.log(u.stamp());                // User@7
console.log(u.toJSON());               // {"id":7,"userName":"Rex"}
console.log(u instanceof Entity);      // true：原型链完整

// Object.assign：拷方法，代价是丢 super 与原型身份
const plain = { id: 1 };
Object.assign(plain, { extra() { return "extra"; } });
console.log(plain.extra());            // extra
console.log(Object.hasOwn(plain, "extra"), Object.hasOwn(u, "stamp"));  // true false

// 组合 + 转发：不改原型链，行为来自持有对象
const delegate = { save() { return "saved"; } };
class Repo {
  constructor(d) { this.d = d; }
  save() { return "repo:" + this.d.save(); }   // 显式转发
}
console.log(new Repo(delegate).save());        // repo:saved
```

高阶 mixin 的写法要求 `Mixin(Base)` 返回一个类，因此 `extends` 链上可以叠加任意多个 mixin，`super` 与 `instanceof` 都保持正确语义（`u instanceof Entity` 为 `true`），这是它优于 `Object.assign` 的原因；代价是每次调用 mixin 都创建新类，类型信息（`constructor.name`）会变，而且不能访问私有字段 `#x`（私有字段属于定义它的类，mixin 生成的子类无法直接读父类私有字段）。`Object.assign` 版本会把方法复制成自身属性，因此 `super` 引用会失效（`super` 只在类方法里合法，复制到普通对象上会直接语法错误或运行时错误）、`hasOwn` 为 `true`、也无法被 `instanceof` 追踪来源。组合加转发是三者中耦合最低的，适合"我需要这个能力但不想暴露被包装对象"的场景（装饰器）。选择顺序通常是：能用组合就用组合，需要类型身份与 `super` 链就用高阶 mixin，只是临时打补丁才用 `Object.assign`。

📘 [MDN · Classes](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes) ｜ 📘 [MDN · Object.assign](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的 trait 是横向复用的主力：它把一组方法**复制**进使用它的类，`$this` 指向使用 trait 的实例，因此 trait 方法可以访问类自己的属性（前提是使用方提供了那些属性）。多个 trait 有同名方法时必须用 `insteadof` 选一个、`as` 给另一个改名，这是 PHP 里最典型的"冲突显式解决"。

```php
<?php
trait Greet {
    public function greet(): string { return "hi from " . static::class; }
}
trait Loud {
    public function greet(): string { return "LOUD"; }
    public function shout(string $s): string { return strtoupper($s); }
}
class Base { public function greet(): string { return "base"; } }

class Talker extends Base {
    use Greet, Loud {           // 冲突：两个 trait 都有 greet
        Greet::greet insteadof Loud;   // 用 Greet 的 greet
        Loud::greet as greetLoud;      // Loud 的 greet 改名为 greetLoud
    }
    public function greet(): string { return "talker:" . parent::greet() . ":" . $this->greetLoud(); }
}

class Shouter {
    use Greet;
    public string $name = "Rex";       // trait 方法可读使用方的属性
    public function who(): string { return $this->greet() . " " . $this->name; }
}

echo (new Talker())->greet(), PHP_EOL;      // talker:base:LOUD（parent:: 是类关系，不是 trait）
echo (new Talker())->greetLoud(), PHP_EOL;  // LOUD
echo (new Shouter())->who(), PHP_EOL;       // hi from Shouter Rex
var_dump(in_array("Greet", class_uses("Shouter"), true));   // true：trait 不是类型，要查 class_uses

interface Named { public function label(): string; }
trait LabelTrait { public function label(): string { return "label"; } }
class Tag implements Named { use LabelTrait; }   // trait 实现接口要求
echo (new Tag())->label(), PHP_EOL;         // label
```

trait 的语义是编译期拷贝：`use` 把方法插入类体，所以 **trait 不是类型**——它不能出现在 `instanceof` 右侧或任何类型声明（参数、返回、属性类型）里，想知道某个类用了哪些 trait 要用 `class_uses()`，trait 本身也不能被实例化或被继承。`insteadof` 是"选一个"，`as` 是"保留一个别名"，两者配合能把冲突完全展开成显式选择；如果不写，PHP 会直接致命错误。trait 可以声明抽象方法要求使用方实现（`abstract public function x(): string;`），也可以有静态方法与属性（PHP 8.2 起 trait 里可以有常量）。与接口的分工：接口只声明契约、可以 `implements` 多个，trait 提供实现但没有类型身份；要"契约 + 实现"两者兼得就 `implements` 一个接口再 `use` 一个 trait。与继承的分工：`extends` 表达"是一个"且只能一个，`use` 表达"复制这段实现"且可以多个，这也是 PHP 里绕开单继承的标准手法。

📘 [PHP · Traits](https://www.php.net/manual/en/language.oop5.traits.php) ｜ 📘 [PHP · Interfaces](https://www.php.net/manual/en/language.oop5.interfaces.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 module 承担一切横向复用：`include` 把 module 插入祖先链（实例方法），`extend` 把它加到单件类（类方法或对象方法），`prepend` 插到类之前以覆盖类自身方法。此外标准库提供 `Forwardable`（`def_delegators`）与 `Delegator`/`SimpleDelegator` 支持组合转发，避免为复用而制造继承层次。

```ruby
require "forwardable"

module Persistable                        # module：横向共享行为
  def save = "#{self.class} saved"
end
module ClassInfo
  def kind = "#{name} is a class"          # 通过 extend 变成类方法
end

class Record
  extend Forwardable                       # 类级 extend：拿到 def_delegators
  extend ClassInfo                         # 类方法复用
  include Persistable                      # 实例方法复用
  def_delegators :@rows, :size, :first     # 委托代替继承
  def initialize = @rows = [1, 2, 3]
end

r = Record.new
puts r.save                   # Record saved
puts r.size                   # 3
puts r.first                  # 1
puts Record.kind              # Record is a class
puts Record.ancestors.take(3).inspect  # [Record, Persistable, Object]

# SimpleDelegator：对象级委托，转发未定义的方法
require "delegate"
class Wrapper < SimpleDelegator
  def shout = __getobj__.to_s.upcase
end
puts Wrapper.new("abc").shout  # ABC
puts Wrapper.new([1, 2]).size  # 2（转发给被包装对象）

module Prepend
  def save = "prepend+" + super     # prepend 能包裹类自己的实现
end
class Record2
  include Persistable
  prepend Prepend
  def save = "own"
end
puts Record2.new.save            # prepend+own
```

`include` 的模块插在类**之后**（类自己的方法优先），`prepend` 插在类**之前**（模块优先且能用 `super` 回到类实现），`extend` 作用在单件类上因此只影响被 extend 的那个对象或类。`def_delegators :@rows, :size, :first` 在编译该行时动态定义转发方法，等价于手写 `def size = @rows.size`，但零样板；`SimpleDelegator` 进一步用 `method_missing` 转发所有未定义方法，代价是 `respond_to?` 需要重写、性能低于直接调用、调试时栈更深。选型建议：共享无状态行为用 `include`；需要在方法前后包裹逻辑（日志、缓存、事务）用 `prepend`；要限制扩展范围用 `extend`；要把实现来源参数化（换数据库、换客户端）用 `Forwardable` 或显式组合。Ruby 的单继承加 module 让祖先链成为唯一真相来源，用 `Dog.ancestors` 或 `method(:x).owner` 可以在运行时确认到底执行了谁的实现，这是排查"方法没被调用"最快的手段。

📘 [Ruby · Modules and classes](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html) ｜ 📘 [Ruby · Forwardable](https://docs.ruby-lang.org/en/master/Forwardable.html)

{{% /tab %}}

{{< /tabpane >}}

### 继承的陷阱

继承是唯一一种"改动祖先会影响所有后代"的耦合形式，因此它的坑集中在两类：**结构性的**（脆弱基类、菱形继承、对象切片、深层次与上帝对象、`protected` 破坏封装、顺序依赖）与**契约性的**（构造期调用被覆盖方法、`equals`/`hashCode` 契约、里氏替换被破坏、默认方法冲突、`sealed` 与穷尽性）。这一节逐语言给出最常踩的几个，并说明每门语言用什么机制减轻它们。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有继承，因此没有脆弱基类、菱形继承、对象切片与构造期派发问题——这些坑被机制本身消灭了。代价是坑换了个形态：trait 默认方法依赖的"钩子方法"如果实现者用 `panic!`/`unimplemented!` 敷衍，问题会推迟到运行时；trait 对象有 object safety 限制；`dyn` 与泛型的选择会影响性能与集合异构性；而且 trait 的默认实现一旦被大量使用，也会变成一种"事实上的脆弱基类"。

```rust
trait Save {
    fn payload(&self) -> String;                                    // 契约：必须实现
    fn save(&self) -> String { format!("saved:{}", self.payload()) }  // 默认实现依赖它
}
struct Doc { content: String }
impl Save for Doc { fn payload(&self) -> String { self.content.clone() } }
struct Broken;
impl Save for Broken { fn payload(&self) -> String { panic!("未实现") } }  // ⚠️ 运行时才炸

fn main() {
    println!("{}", Doc { content: "a".into() }.save());   // saved:a
    let b = Broken;
    let r = std::panic::catch_unwind(|| b.save());
    println!("{}", r.is_err());                           // true
    let objs: Vec<Box<dyn Save>> = vec![Box::new(Doc { content: "x".into() })];
    println!("{}", objs[0].save());                       // saved:x
    // 以下都会编译失败，而不是运行时出错：
    // trait 带泛型方法或返回 Self → 不能做成 dyn（object safety）
    // struct 字面量少给字段 → missing field（不存在"未初始化的基类部分"）
    // 把 Dog 赋给 Animal 变量 → 类型不匹配（没有子类型转换）
}
```

Rust 的"陷阱"与其它语言有一处根本不同：**绝大多数错误在编译期就被拒绝**。trait 对象要求 object safe（不能有泛型方法、不能返回 `Self`、不能有 `where Self: Sized` 之外的限制），否则使用 `dyn` 时会得到明确的编译错误；结构体字段必须全部初始化，因此 C++、Java 那种"基类构造器读到子类未初始化的字段"根本不可能发生；类型之间没有隐式子类型转换，所以切片也不存在。真正的运行时风险是默认实现里对钩子的**语义依赖**：上面的 `payload` 是 trait 必填项，编译器保证它存在，但拦不住实现者用 `unimplemented!()` 占位；默认方法里若调用 `self.some_inherent_method()` 则更糟——trait 里根本不允许调用不在 trait 中的固有方法，所以这类错误也被挡住了。结论是：Rust 用 trait 复用时要保证默认方法只依赖 trait 自身声明的方法，把"必须提供的数据"做成必填方法而不是可选钩子；需要运行时异构集合就用 `dyn` 并接受一次间接调用，需要性能就用泛型单态化，两者不要混着当"继承"用。

📘 [Rust Reference · Trait objects（object safety）](https://doc.rust-lang.org/reference/types/trait-object.html) ｜ 📘 [Rust API Guidelines · Future proofing](https://rust-lang.github.io/api-guidelines/future-proofing.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的继承陷阱集中在四处：**类继承会带来引用语义**（共享可变状态）、**`final` 与访问控制决定派发方式**（影响性能与行为）、**协议扩展的方法不参与 existential 的动态派发**、以及**初始化期间不能调用可被覆盖的方法**（编译器直接禁止，属于"被消除的陷阱"）。此外类与结构体的语义差异（引用 vs 值）是 Swift 里最常见的设计事故来源。

```swift
class Counter {                       // 类：引用语义
    var value = 0
}
func bump(_ c: Counter) { c.value += 1 }
let c = Counter()
bump(c)
print(c.value)                        // 1 ⚠️ 调用方看到被修改

struct Point {                        // 结构体：值语义
    var x = 0
}
func bump(_ p: Point) -> Point { var p = p; p.x += 1; return p }
let p = Point()
print(bump(p).x, p.x)                 // 1 0：值拷贝，无副作用

class Base {
    func name() -> String { "Base" }
    final func fixed() -> String { "Base.fixed" }   // final → 静态派发
}
class Derived: Base {
    override func name() -> String { "Derived" }
}
let b: Base = Derived()
print(b.name())                       // Derived
print(b.fixed())                      // Base.fixed
print(type(of: b))                    // Derived

protocol P { func value() -> Int }
extension P { func describe() -> String { "P" } }   // 扩展方法：静态派发
struct S: P {
    func value() -> Int { 1 }
    func describe() -> String { "S" }                // ⚠️ 不参与 existential 派发
}
let anys: [any P] = [S()]
print(anys[0].describe())             // P（不是 S）
let concrete = S()
print(concrete.describe())            // S
```

`final` 的收益是可量化的：编译器可以对 `final` 方法做直接调用与内联（类的扩展方法、`private` 方法同理），而跨模块的非 `final` 类方法必须走 vtable 或消息派发（`@objc dynamic` 走 Objective-C runtime 更慢）。协议扩展的静态派发是最容易踩的语义坑：上面 `anys[0].describe()` 得到 `"P"`，因为 existential 上的调用按协议扩展的静态版本解析；要在 `any P` 上获得具体类型的行为，必须把方法写进协议要求本身。类继承的引用语义在集合与函数传参时会带来共享修改，Swift 因此推崇"默认用 `struct`，只在需要身份、继承或共享可变状态时才用 `class`"；`final` 与"类默认封闭"的风气也在朝同一方向走。初始化期禁止调用实例方法（必须先完成自身字段初始化、再 `super.init`）直接消除了构造期调用被覆盖方法的问题，这也是 Swift 相对 Java、C# 更安全的一处。

📘 [Swift · Inheritance](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/inheritance/) ｜ 📘 [Swift · Protocols（扩展与派发）](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有继承，所以没有脆弱基类与菱形继承；但它的嵌入机制制造了两个专属陷阱：**遮蔽不改变基类方法内部的调用绑定**（基类的模板方法永远调用基类自己的实现），以及**方法提升造成的"看似有接口实现"**（外层类型自动满足接口，但行为可能不是你要的）。此外值接收者与指针接收者混用会悄悄破坏方法集。

```go
package main

import "fmt"

type Animal struct{ Name string }

func (a Animal) Describe() string { return "animal:" + a.speak() }  // 静态绑定
func (a Animal) speak() string    { return "..." }

type Dog struct{ Animal }

func (d Dog) speak() string { return "Woof" }   // 遮蔽：只影响 d.speak()

type Speaker interface{ Speak() string }

type Dog2 struct{ Animal }
func (d *Dog2) Speak() string { return "Woof" } // 指针接收者

func main() {
	d := Dog{Animal{"Rex"}}
	fmt.Println(d.Describe())          // animal:...（不是 Woof）
	fmt.Println(d.speak())             // Woof
	fmt.Println(d.Animal.speak())      // ...
	var s interface{ Speak() string }
	// s = Dog2{}                       // 🛑 Dog2 值不满足：Speak 是指针接收者
	s = &Dog2{Animal{"Rex"}}
	fmt.Println(s.Speak())             // Woof
	_ = s
	// 遮蔽造成的"多态错觉"在接口上同样如此：接口方法必须是动态的那一个
}
```

第一个陷阱的根源是 Go 没有 vtable：`Animal.Describe` 内部的 `a.speak()` 在编译期就绑定到 `Animal.speak`，`Dog` 再定义 `speak` 也改变不了它。Java、C++、Swift 里同样的代码会输出 `animal:Woof`（模板方法模式依赖动态派发），Go 里输出 `animal:...`——把这段代码从 Java 翻到 Go 是最常见的语义事故之一。想在 Go 里实现模板方法，必须把可变步骤做成接口字段或函数字段（`type Animal struct { Speak func() string }`），让 `Describe` 通过 `a.Speak()` 这个函数值调用，这才是动态的。第二个陷阱是方法集：值接收者的方法属于 `T` 与 `*T`，指针接收者的方法只属于 `*T`，因此"为什么我的类型不满足接口"通常就是接收者写错或忘了取地址；反过来，把带互斥锁的结构体按值装进接口会导致锁被复制（`go vet` 的 `copylocks` 检查会提示）。嵌入还会把内层类型的所有导出方法都提升上来，可能意外让外层类型满足了某个接口（包括 `String()`、`MarshalJSON()` 这类有特殊含义的方法），从而改变格式化或序列化行为。

📘 [Go spec · Method sets](https://go.dev/ref/spec#Method_sets) ｜ 📘 [Go FAQ · Methods on values or pointers](https://go.dev/doc/faq#methods_on_values_or_pointers)

{{% /tab %}}

{{% tab header="Python" %}}

Python 有真正的多继承，因此菱形、MRO 顺序依赖、协作式 `super()` 断裂它都会遇到；同时因为一切都在运行时，抽象契约与类型约束也很容易被绕过。最典型的三类事故是：**MRO 顺序决定行为**（同一组基类换个顺序结果不同）、**某个类不调用 `super()`**（链断掉且不报错）、**构造期动态派发**（基类 `__init__` 调用被子类覆盖的方法，读到尚未赋值的属性）。

```python
# 陷阱 1：MRO 顺序依赖
class A:
    def hello(self) -> str: return "A"
class B:
    def hello(self) -> str: return "B"
class AB(A, B): pass
class BA(B, A): pass
print(AB().hello(), BA().hello())        # A B：同一组基类，结果不同

# 陷阱 2：非协作式调用破坏 super 链
class Base:
    def setup(self) -> list[str]: return ["base"]
class Mid(Base):
    def setup(self) -> list[str]: return ["mid"]          # ⚠️ 没有 super()
class Leaf(Mid):
    def setup(self) -> list[str]: return ["leaf"] + super().setup()
print(Leaf().setup())                    # ['leaf', 'mid']：base 永远不执行

# 陷阱 3：构造期调用被覆盖方法
class Shape:
    def __init__(self) -> None:
        self.area = self.compute_area()  # ⚠️ 动态派发到子类
    def compute_area(self) -> float: return 0.0
class Circle(Shape):
    def __init__(self, r: float) -> None:
        self.r = r
        super().__init__()
    def compute_area(self) -> float: return 3.0 * self.r ** 2
print(Circle(2.0).area)                  # 12.0（这次 r 已赋值）

# 陷阱 4：正方形继承矩形破坏里氏替换
class Rectangle:
    def __init__(self) -> None: self._w = self._h = 1
    def set_width(self, w: int) -> None: self._w = w
    def set_height(self, h: int) -> None: self._h = h
    def area(self) -> int: return self._w * self._h
class Square(Rectangle):
    def set_width(self, w: int) -> None: self._w = self._h = w
    def set_height(self, h: int) -> None: self._w = self._h = h
def stretch(r: Rectangle) -> int:        # 契约：宽高互相独立
    r.set_width(2); r.set_height(3)
    return r.area()
print(stretch(Rectangle()), stretch(Square()))   # 6 9：Square 破坏了契约
```

菱形继承在 Python 里不会像 C++ 那样产生两份基类子对象（每个类在 MRO 里只出现一次），但会带来顺序依赖：`class AB(A, B)` 与 `class BA(B, A)` 的 `hello()` 结果不同，而且 `A.__mro__` 里谁在前面会连带影响 `super()` 的去向。协作式 `super()` 是唯一能让链完整执行的写法，它要求整条链上的每个类都调用 `super()`（`Leaf` 里的 `["leaf"] + super().setup()` 只有在 `Mid` 也调 `super()` 时才能到达 `Base`）；用 `Base.setup(self)` 显式调用会直接跳过 `Mid` 之后的节点并可能重复执行。构造期派发的危险在于"调用时属性还没赋值"——上面 `Circle` 把 `self.r = r` 放在 `super().__init__()` 之前所以侥幸正确，一旦顺序颠倒就会 `AttributeError`。正方形继承矩形是里氏替换的教科书反例：`stretch` 对矩形成立的前提（宽高独立）对正方形不成立，因此 `Square` 不该是 `Rectangle` 的子类——正确做法是让二者都实现一个 `Shape` 协议或抽象基类，或者干脆各自独立（`Square` 用 `Rectangle` 组合）。Python 没有访问控制，`_protected` 与 `__private`（名称改写）都只是约定，因此"`protected` 破坏封装"的问题在这里表现为"深继承层次里谁都改内部状态"，用 `__slots__`、`@property`、`frozen dataclass` 能缓解一部分。

📘 [Python · MRO](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance) ｜ 📘 [Python · super()](https://docs.python.org/3/library/functions.html#super)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的设计几乎就是冲着继承陷阱来的：**类默认 `final`** 让"无意继承"不可能发生，**默认 `final` 的成员**让"无意覆盖"也被挡住，**`sealed` 加 `when` 的穷尽性检查**把"漏处理子类型"变成编译错误，**默认参数与接口委托**让装饰器模式不用手写转发，**数据类（`data class`）默认 `final` 且不允许继承**从而避开 `equals`/`hashCode` 契约在继承下的经典破坏。要说的坑只剩"显式 `open` 之后自己要负责"。

```kotlin
open class Base(val id: Int) {
    open fun label(): String = "base:$id"
    fun describe(): String = "desc:" + label()   // 模板方法依赖动态派发
}
open class Mid(id: Int) : Base(id) {
    override fun label(): String = "mid"          // ⚠️ 覆盖后没调 super
}
class Leaf(id: Int) : Mid(id) {
    override fun label(): String = "leaf+" + super.label()
}
data class Point(val x: Int, val y: Int)          // 隐式 final；equals 按字段

sealed interface Shape {
    data class Circle(val r: Double) : Shape
    data class Square(val s: Double) : Shape
}
fun area(s: Shape): Double = when (s) {           // 穷尽性：漏一个就编译失败
    is Shape.Circle -> 3.0 * s.r * s.r
    is Shape.Square -> s.s * s.s
}
interface Logger { fun log(m: String): String }
class Sys : Logger { override fun log(m: String) = "[sys] $m" }
class Counted(private val inner: Logger) : Logger by inner {   // 委托代替继承
    var n = 0
    override fun log(m: String): String { n++; return inner.log(m) }
}
fun main() {
    println(Leaf(1).describe())        // desc:leaf+mid（Base.label 被绕过）
    println(Point(1, 2) == Point(1, 2))   // true：data class 按字段比较
    println(area(Shape.Circle(2.0)))   // 12.0
    val c = Counted(Sys())
    println(c.log("x") + c.n)          // [sys] x1
}
```

Kotlin 的默认 `final` 直接消灭了"脆弱基类问题"的大半：Java 里"给基类加一个方法可能意外改变子类行为"的情况在 Kotlin 里不会发生，因为子类必须显式 `override`。数据类的 `equals`/`hashCode` 按构造器属性生成且类不可继承，因此不存在 Java 那种"子类加字段后 `equals` 不对称"的问题；反过来，需要"数据类参与继承"时只能写成普通 `open class` 并手写 `equals`。`sealed` 与 `when` 组合把"上帝对象式深层次"替换成"扁平穷尽分支"，`when` 作为表达式漏分支会编译失败，作为语句时 Kotlin 1.7 起对 `sealed`、`enum`、`Boolean` 主题的漏分支同样报编译错误（1.6 只是警告）。真正剩下的坑是 `open` 之后的责任：`Mid.label()` 覆盖后不调用 `super.label()` 让模板方法链断了，运行时不报错只是行为不对；`describe()` 是 `final`（默认 final，所以子类不能重写它）。覆盖的返回类型允许协变（子类可以返回更具体的类型），但参数类型必须与父类完全一致，否则那是重载而不是覆盖。选型建议很简单：能不 `open` 就不 `open`，要横向能力用接口默认实现或 `by` 委托，要封闭层级用 `sealed`。

📘 [Kotlin · Inheritance（final by default）](https://kotlinlang.org/docs/inheritance.html) ｜ 📘 [Kotlin · Data classes](https://kotlinlang.org/docs/data-classes.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的继承陷阱最完整，因为它同时具备"方法默认虚""字段可以被隐藏""`equals`/`hashCode` 可覆盖""`protected` 可见""深继承层次常见"这几个条件。最著名的四个是：**构造期调用被覆盖方法**（读到子类未初始化的字段）、**`equals` 在继承下破坏对称性**、**`protected` 暴露内部实现**、以及**深层次与上帝对象**导致的脆弱基类问题。

```java
class Base {
    protected int value = 1;
    Base() {
        System.out.println("ctor: " + describe());   // ⚠️ 派发到子类
    }
    String describe() { return "base(" + value + ")"; }
}
class Sub extends Base {
    private final int extra;
    Sub(int extra) {
        super();                                   // 此时 extra 还没赋值
        this.extra = extra;
    }
    @Override String describe() { return "sub(" + value + "," + extra + ")"; }
}

class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    @Override public boolean equals(Object o) {
        if (!(o instanceof Point p)) return false;      // ⚠️ instanceof 允许子类
        return p.x == x && p.y == y;
    }
    @Override public int hashCode() { return 31 * x + y; }
}
class ColorPoint extends Point {
    private final String color;
    ColorPoint(int x, int y, String color) { super(x, y); this.color = color; }
    @Override public boolean equals(Object o) {
        if (!(o instanceof ColorPoint c)) return false;  // 与 Point.equals 不对称
        return super.equals(o) && c.color.equals(color);
    }
}
public class Main {
    public static void main(String[] args) {
        new Sub(5);                                   // ctor: sub(1,0)：extra 还是 0
        Point p = new Point(1, 2);
        ColorPoint cp = new ColorPoint(1, 2, "red");
        System.out.println(p.equals(cp));              // true
        System.out.println(cp.equals(p));              // false ← 对称性被破坏
        System.out.println(p.hashCode() == cp.hashCode());  // true
    }
}
```

构造期派发是 Java 里最隐蔽的坑之一：`Base()` 里调用 `describe()` 会走 vtable 到 `Sub.describe()`，而此刻 `Sub.extra` 仍是默认值 `0`（`final` 字段此时甚至还没赋值），输出 `sub(1,0)` 而不是你预期的最终状态。规避办法是把"需要子类参与的逻辑"移到构造器之外（工厂方法、`init()` 模板、`Builder`），或者在基类构造器里只调用 `private`/`final`/`static` 方法。Java 25 起多了一条正面的解法：JEP 513（Flexible Constructor Bodies，在 JDK 25 定稿）允许把语句写在 `super(...)`/`this(...)` 之前，这段 prologue 里可以校验参数、也可以给本类的无初始化器字段赋值（但不能通过 `this` 读字段或调实例方法，也不能用 `super.` 访问父类成员），于是"父类构造器回调被覆盖方法时读到默认值"这个坑可以靠"在 `super()` 之前先把字段填好"来消除。`equals` 的对称性问题来自"用 `instanceof` 允许子类"的写法：`p.equals(cp)` 为 `true` 而 `cp.equals(p)` 为 `false`，把 `Point` 与 `ColorPoint` 放进同一个 `HashSet` 就会出现重复元素。Java 社区的两条标准建议是：优先用组合而不是继承（《Effective Java》第 18 条），以及"要么为继承设计并提供文档，要么禁止继承"（第 19 条，用 `final` 或 `private` 构造器加静态工厂）。`protected` 的问题在于它把字段与实现细节暴露给所有子类与同包类，子类一旦依赖这些细节，基类就无法演化（脆弱基类问题），因此现代 Java 代码更倾向 `private` 字段加 `protected` 或 `public` 的少量方法。Java 17 起的 `sealed` 与 `record` 正是用"封闭层级 + 不可继承"来替代"深继承 + 可覆盖"的官方方案。

📘 [Java · Inheritance（设计建议）](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html) ｜ 📘 [JLS · Overriding and hiding](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.4.8)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 把继承的所有危险都放到台面上，因为它同时有值语义、多继承与手工内存管理。四个必须掌握的陷阱是：**对象切片**（按值传参或容器存基类会切掉派生部分）、**构造/析构期调用虚函数不派发到派生类**、**菱形继承与虚继承**、以及**非虚析构导致 `delete` 基类指针是未定义行为**。`protected` 成员与默认 `private` 继承（`class`）也是常见误解来源。

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <memory>

struct Base {
    Base() { std::cout << "ctor: " << name() << "\n"; }   // ⚠️ 只派发到 Base
    virtual ~Base() = default;                            // 必须虚析构
    virtual std::string name() const { return "Base"; }
    std::string pad = "x";
};
struct Derived : Base {
    std::string name() const override { return "Derived"; }
    std::string extra = "payload";
};
void print(Base b) { std::cout << b.name() << "\n"; }     // ⚠️ 值传递：切片

int main() {
    Derived d;                               // ctor: Base
    print(d);                                // Base（切片）
    std::vector<Base> v; v.push_back(d);     // ⚠️ 容器存基类：同样切片
    std::cout << v[0].name() << "\n";        // Base
    std::vector<std::unique_ptr<Base>> w;
    w.push_back(std::make_unique<Derived>());
    std::cout << w[0]->name() << "\n";       // Derived（指针不切片）
    const Base& r = d;
    std::cout << r.name() << "\n";           // Derived
    std::cout << sizeof(Base) << " " << sizeof(Derived) << "\n";  // 32 56
}
```

切片的本质是"按基类的大小拷贝"，派生类新增的成员没有地方放，被静默丢弃；`std::vector<Base>` 与按值传参都会切片，要保留多态必须用 `Base*`、`Base&`、`std::unique_ptr<Base>`，或者在 C++17 之后用 `std::variant` 加 `std::visit` 做值语义的封闭多态。构造期不派发的规则（构造与析构期间虚表指针指向当前正在构造/析构的类）意味着"基类构造器里调用模板方法"在 C++ 里得不到子类的实现，这与 Java、C# 的运行时行为相反；如果子类部分依赖它来初始化，程序逻辑就会错（而 C++ 不会像 Python 那样抛 `AttributeError`，只是静默给出基类结果）。菱形继承出现在 `struct D : B1, B2` 且 `B1`、`B2` 都继承自 `A` 时，`D` 里会有两份 `A` 子对象，访问 `A` 的成员必须写 `d.B1::member` 消歧；要让两份合并成一份必须用 `virtual` 继承（`struct B1 : virtual A`），代价是对象里增加虚基类指针、布局更复杂、并且**最派生类必须负责初始化虚基类**（`B1` 的构造器里对 `A` 的初始化会被忽略）。最后，通过基类指针 `delete` 一个没有虚析构函数的派生对象是未定义行为，实践中表现为派生类的析构不执行、资源泄漏，所以"多态基类必须有 `virtual ~Base()`"是一条不可省略的纪律。

📘 [cppreference · Object slicing 与虚析构](https://en.cppreference.com/w/cpp/language/derived_class) ｜ 📘 [cppreference · virtual（构造/析构期）](https://en.cppreference.com/w/cpp/language/virtual)

{{% /tab %}}

{{% tab header="C" %}}

C 没有继承，因此没有菱形继承、虚基类、构造期派发这些语言级问题；它的"继承陷阱"全部来自那两套约定：**首成员布局的约定一旦破坏就静默出错**（转换指针得到错误偏移、读到错误字段）、**函数指针表与生命周期手工管理**（忘记初始化 `vtbl`、忘记虚析构、悬垂指针）、以及**没有类型检查导致的下转型错误**。这些都是未定义行为，不会抛异常也不会在编译期报错。

```c
#include <stdio.h>
#include <string.h>

typedef struct Base Base;
typedef struct { const char *(*name)(const Base *); } Vtbl;
struct Base { const Vtbl *vtbl; int id; };

static const char *base_name(const Base *b) { (void)b; return "Base"; }
static const Vtbl BASE_VTBL = { base_name };

/* ✅ 正确：基类在第一个成员 */
typedef struct { Base base; int extra; } Good;
/* 🛑 错误：基类不是首成员，指针转换会读到错误数据 */
typedef struct { int extra; Base base; } Bad;

int main(void) {
    Good g = { { &BASE_VTBL, 2 }, 0 };             /* base.id = 2，extra = 0 */
    Bad bad = { 3, { &BASE_VTBL, 4 } };            /* extra = 3，base.id = 4 */

    Base *p1 = &g.base;
    printf("%d\n", p1->id);                        /* 2：布局一致，安全 */
    Base *p2 = (Base *)&bad;                       /* 🛑 UB：偏移不对 */
    printf("%d\n", p2->id);                        /* 读到 extra 或填充字节，值不可预测 */
    printf("%d\n", (int)sizeof(Base) + (int)sizeof(Good) + (int)sizeof(Bad));  /* 64 = 16+24+24 */

    Base *uninit = (Base *)&bad;                   /* 忘了设置 vtbl 的对象 */
    (void)uninit;
    /* uninit->vtbl->name(uninit) 会崩溃或跳到随机地址 */
    return 0;
}
```

`Bad` 结构体演示了最典型的 C 版继承事故：`(Base *)&bad` 得到的指针指向 `bad` 的开头，而那里是 `extra` 字段，于是 `p2->id` 读到的是内存错位后的值——编译器不会警告，运行结果也不稳定（还取决于对齐与填充）。GObject 与内核用宏和文档纪律来防这件事（`G_DEFINE_TYPE` 里强制把父类实例作为第一个成员、`container_of` 用成员地址反推，靠已知偏移），但语言层面没有保护。第二类事故是生命周期：C 没有 RAII，对象的释放顺序、谁拥有对象、什么时候调用 `finalize` 全靠约定；基类指针 `free(p)` 而不是 `p->vtbl->finalize(p)` 会跳过派生部分的清理（等价于"非虚析构"），这在长生命周期框架里会造成难以定位的泄漏。第三类是把 `void*` 转回错误的具体类型——C 的 `vtbl` 方式擦除了类型，任何 downcast 都是"我相信调用方"。结论是：C 的继承模拟只适合边界清晰、生命周期集中的场景，并且要把"首成员契约""必须调用 `finalize`""禁止跨类型转换"写进文档并用 `static_assert`（C11 `_Static_assert`）与代码审查守护。

📘 [C · struct（布局与对齐）](https://en.cppreference.com/w/c/language/struct) ｜ 📘 [C · Pointer conversions](https://en.cppreference.com/w/c/language/pointer)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的陷阱与类继承语言完全不同：抽象类型只建立子类型关系、不带字段与实现，因此"脆弱基类"的形态是**给抽象类型加新的抽象子类型后破坏了穷尽假设**；**方法歧义**（两个方法无法比较特异性）在运行时才报 `MethodError`；**类型不稳定**（返回类型推断不出来）会摧毁性能；以及**用具体类型做父类型的层次设计**会导致无法扩展。

```julia
abstract type Animal end
struct Dog <: Animal end
struct Cat <: Animal end
struct Wolf <: Animal end          # 新加的子类型

kind(::Dog) = "dog"
kind(::Cat) = "cat"
# kind(::Animal) 没有兜底方法：新子类型会直接 MethodError

println(kind(Dog()))               # dog
try
    kind(Wolf())
catch e
    println(typeof(e))             # MethodError：新子类型忘了加方法
end

# 方法歧义：两个方法无法比较特异性
f(::Animal, ::Int) = "animal,int"
f(::Dog, ::Any) = "dog,any"
struct Bird <: Animal end
try
    f(Dog(), 1)                    # 两个候选互不更具体
catch e
    println(typeof(e))             # MethodError（ambiguous）
end

# 类型不稳定：返回类型可能是 String 也可能是 Int
unstable(x::Int) = x > 0 ? "pos" : 0     # 推断出的返回类型是 Union{Int64, String}
println(typeof(unstable(1)))             # String（这一次的实际类型）
println(typeof(unstable(-1)))            # Int64（同一个函数两次调用类型不同 → 不稳定）
# 字段类型必须具体，才能让编译器生成高效代码
struct Bad
    v                          # Any：类型不稳定
end
println(typeof(Bad(1).v))      # Int64（值），但字段声明是 Any
```

第一个陷阱的根因是 Julia 的方法表是开放的：任何人都能给 `Animal` 加子类型，因此定义 `kind(::Dog)`、`kind(::Cat)` 而不写 `kind(::Animal)` 兜底，就等于给未来埋下 `MethodError`。惯用做法是永远给抽象类型写一个默认方法（`kind(::Animal) = "unknown"`）或把接口方法写进文档并用 `hasmethod` 检查。第二个陷阱是多重分派的固有代价：`f(::Animal, ::Int)` 与 `f(::Dog, ::Any)` 对 `(Dog, Int)` 都适用且互不更具体，Julia 会拒绝猜测并抛歧义错误，必须补一个 `f(::Dog, ::Int)` 显式消解——这与 Java 默认方法冲突、Rust trait 方法歧义同源。第三个陷阱是性能而非正确性：如果抽象类型出现在字段声明里（`v` 未标注类型就是 `Any`），每次访问都要动态派发，Julia 的类型推断会失败（`@code_warntype` 会标红）；解法是用参数化类型（`struct Box{T}; v::T; end`）而不是抽象字段类型。最后，"上帝对象"在 Julia 里表现为一个抽象类型下挂几十个具体子类型却只靠 `if isa` 分支处理——正确姿势是为每个子类型定义方法，让多重分派替你写分支。

📘 [Julia · Methods（歧义）](https://docs.julialang.org/en/v1/manual/methods/#Ambiguities) ｜ 📘 [Julia · Performance Tips（类型稳定）](https://docs.julialang.org/en/v1/manual/performance-tips/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的陷阱与 Java 高度重合，但有两处不同：`new` 关键字造成的**遮蔽与覆盖混淆**（编译期按静态类型选方法），以及接口默认实现带来的**"通过接口能调用、通过类不能"的可见性差异**。`struct` 不能继承，因此值类型不存在对象切片，但装箱会带来另一类性能与身份问题。

```csharp
using System;
using System.Collections.Generic;

class Base {
    public Base() { Console.WriteLine("ctor: " + Describe()); }  // ⚠️ 派发到子类
    public virtual string Describe() => "base(" + Value + ")";
    public int Value = 1;
    public override string ToString() => Describe();
}
class Sub : Base {
    public int Extra;
    public Sub(int extra) { Extra = extra; }                     // Extra 默认 0
    public override string Describe() => $"sub({Value},{Extra})";
}
class A { public string Who() => "A"; }
class B : A { public new string Who() => "B"; }                  // 遮蔽

interface IShape { double Area(); string Describe() => $"area={Area()}"; }
class Circle : IShape { public double Area() => 12.0; }

class Program {
    static void Main() {
        var s = new Sub(5);                     // ctor: sub(1,0)
        Console.WriteLine(s.Describe());        // sub(1,5)

        A a = new B();
        Console.WriteLine(a.Who());             // A：静态绑定到 A.Who
        Console.WriteLine(((B)a).Who());        // B

        IShape shape = new Circle();
        Console.WriteLine(shape.Describe());    // area=12（接口默认实现）
        // new Circle().Describe()              // 🛑 编译错误：类类型看不到默认实现

        var point = new Point(1, 2);            // struct：值语义，无切片
        object boxed = point;                   // 装箱：复制到堆
        Console.WriteLine(ReferenceEquals(boxed, boxed));  // True（同一个箱子）
        Console.WriteLine(ReferenceEquals(boxed, point));  // False（装箱是新对象）
    }
}
struct Point { public int X, Y; public Point(int x, int y) { X = x; Y = y; } }
```

构造期派发与 Java 完全一样：`Base()` 里调用虚方法 `Describe()` 输出 `sub(1,0)`，因为 `Extra` 此时还是默认值；规避方式同样是不要在构造器里调用可被覆盖的成员（编译器对虚方法调用会给出 CA2214 警告，可据此找出问题）。`new` 遮蔽是 C# 特有的坑：`A a = new B(); a.Who()` 得到 `"A"`，因为 `Who` 不是虚方法，方法在编译期按变量类型绑定；`new` 处的 CS0108 警告就是提醒你"你可能想写 `override`"。接口默认实现的可见性限制（只能通过接口类型调用）意味着它不能被当作"基类方法"使用，也**不能访问实现类的字段**，所以它只适合无状态派生逻辑。`struct` 不能继承所以没有切片，但把一个 `struct` 装进 `object` 或接口会发生装箱（堆分配 + 复制），并且每次装箱都产生新的对象身份——`ReferenceEquals(boxed, boxed)` 为 `True` 只是因为同一个装箱结果被复用；把 `struct` 放进 `List<object>` 或与接口一起用会带来可观的 GC 压力，这是 C# 里值类型"看起来像继承"时的另一类代价。

📘 [C# · Inheritance](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance) ｜ 📘 [C# · virtual / new](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/new-modifier)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的陷阱集中在 mixin 的**线性化顺序**与 class modifier 的**语义边界**：`with A, B` 里后写的 mixin 覆盖先写的、`super` 沿线性化顺序指向上一层；`implements` 不建立 `is` 关系却要求实现全部成员（包括具体方法）；`sealed` 的穷尽性只在同一库内成立；`factory` 构造器绕过普通构造流程也会带来初始化不一致。此外可空类型与非空断言（`!`）在深层次继承里会放大运行时风险。

```dart
abstract class Who { String who(); }             // on 约束的宿主：mixin 里的 super 需要它有 who

mixin A on Who { String who() => "A"; }
mixin B on Who { String who() => "B"; }
mixin C on Who { String who() => "C+" + super.who(); }   // super 沿线性化向上

class AB extends Who with A, B {}
class BA extends Who with B, A {}
class ABC extends Who with A, B, C {}             // 线性化：C 最后写，最先执行

abstract class Animal {
  final String name;
  Animal(this.name);
  String speak() => "...";
}
class Robot implements Animal {                   // implements：只要契约
  @override
  final String name = "R2";
  @override
  String speak() => "beep";
  int? cache;
  int forceCache() => cache!;                     // ⚠️ cache 为 null 时抛 TypeError（空断言失败）
}
sealed class Result {}                            // 子类必须同库
class Ok extends Result { final int v; Ok(this.v); }
class Err extends Result { final String m; Err(this.m); }

void main() {
  print(AB().who());                     // B（后写的 B 优先）
  print(BA().who());                     // A
  print(ABC().who());                    // C+B（C 调 super 落到 B）
  print(Robot() is Animal);              // false：implements 不建立 is
  try { Robot().forceCache(); } catch (e) { print(e); }  // Null check operator used on a null value
  final r = Ok(1);
  print(switch (r) { Ok(v: var v) => "ok $v", Err(m: var m) => "err $m" });  // ok 1
}
```

线性化规则是 Dart 里最容易出错的地方：`with` 列表按书写顺序叠加、**后面的覆盖前面的**，`super` 从当前 mixin 往线性化的上一层走，因此 `ABC().who()` 得到 `"C+B"` 而不是 `"C+A"`。调换 mixin 顺序会静默改变行为（`AB` 与 `BA` 的 `who()` 不同），所以 mixin 设计上应避免同名成员，或者像 `C` 那样把 `super` 调用写成可读的链条。`implements` 的陷阱是语义误判：`Robot implements Animal` 只表示"具备这些成员"，`Robot() is Animal` 为 `false`，不能拿它做类型分支；而且 `implements` 会连带要求实现具体方法，父类新增方法会让所有 `implements` 它的类编译失败——这正是 Dart 3.0 引入 class modifier 的动机（库作者可以声明"这个类只允许被 `implements`"或"只允许被 `extends`"，控制破坏性变更的传播方向）。`sealed` 的穷尽性只在同库内有效，因为子类集合在库外不可见；跨库要么用 `final`（禁止任何外部继承）要么用枚举。最后，深继承链加上可空字段会让 `!` 断言散落各处，空值错误只在运行时暴露（`Null check operator used on a null value`），更稳的写法是把可空状态收敛到少数几个方法里处理。

📘 [Dart · Class modifiers](https://dart.dev/language/class-modifiers) ｜ 📘 [Dart · Sound null safety](https://dart.dev/null-safety/understanding-null-safety)

{{% /tab %}}

{{% tab header="R" %}}

R 的陷阱来自"没有正式类定义也能工作"这件事：S3 的 `class` 属性是**任意字符串向量**，写错不会报错只会走错分派；`NextMethod` 的顺序依赖 `class` 向量；S4 的槽位校验与分派失败信息晦涩；R6 的引用语义会让人误以为赋值是拷贝。再加上 `UseMethod` 的参数数量限制与 `NA` 的传染性，R 的"继承"问题通常是"静默走了 default 分支"。

```r
speak <- function(x, ...) UseMethod("speak")
speak.default <- function(x, ...) "no method"      # 兜底：容易掩盖拼写错误
speak.dog <- function(x, ...) "Woof"

d <- structure(list(name = "Rex"), class = c("dog", "animal"))
print(speak(d))                        # [1] "Woof"
typo <- structure(list(name = "Rex"), class = c("Dog", "animal"))  # 大小写不同
print(speak(typo))                     # [1] "no method"  ⚠️ 静默降级

# class 向量顺序就是分派顺序
both <- structure(list(), class = c("dog", "cat"))
speak.cat <- function(x, ...) "Meow"
print(speak(both))                     # [1] "Woof"（dog 排在前面）

# NextMethod 沿 class 向量走，而不是"父类"概念
speak.puppy <- function(x, ...) paste("Yip", NextMethod())
p <- structure(list(), class = c("puppy", "dog", "animal"))
print(speak(p))                        # [1] "Yip Woof"

# S4：槽位校验在 new() 时才发生
setClass("Animal4", representation(name = "character"))
setClass("Cat4", contains = "Animal4")
print(tryCatch(new("Cat4", name = 1), error = function(e) "error"))  # 类型不符：error
print(is(new("Cat4", name = "Tom"), "Animal4"))                       # [1] TRUE

# R6：引用语义（$ 修改会影响所有引用者）
library(R6)
Counter <- R6Class("Counter", public = list(n = 0, inc = function() self$n <- self$n + 1))
a <- Counter$new(); b <- a; a$inc()
print(b$n)                             # [1] 1 ⚠️ b 也被改了（引用语义）
```

S3 的 `class` 属性没有注册表也没有校验，因此 `"Dog"` 与 `"dog"`、`"data.frame"` 与 `"dataframe"` 这类拼写差异会让分派悄悄落到 `speak.default`；这也是为什么大型 R 包在 S3 方法里常写 `.NotYetImplemented()` 或对未知类直接 `stop()`——"友好兜底"反而掩盖错误。`NextMethod()` 的语义是"沿 `class` 属性的下一个元素找方法"，所以 `class` 向量的顺序就是继承链，而不是 `setClass` 里的 `contains` 关系；把 `"dog"` 写在 `"animal"` 后会静默改变行为。S4 的类型校验在 `new()` 时发生（不在 `setClass` 时），赋值给槽位时也会校验，错误信息不友好但至少会报错；性能上 `setMethod` 的查找比 S3 慢。R6 用环境实现引用语义，`b <- a` 是引用复制而不是值复制，这与 R 其它地方的值语义习惯冲突，容易产生"为什么这个变量被改了"的困惑；S4 是值语义（`new()` 与赋值会复制底层数据），这也是它在生物统计包里长期流行的原因之一。最后，`UseMethod` 只在单个对象上分派（默认第一个参数，`UseMethod("speak", x)` 也能显式指定），没有多重分派，又没有注册表与结构校验，所以 `class` 属性一旦写错就只能落到 `default` 分支；需要按多个参数分派或要求槽位类型校验时，改用 S4 的 `setGeneric`/`setMethod` 或 R6。

📘 [R · Method dispatch](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatching) ｜ 📘 [R methods · setClass（S4 正式类）](https://stat.ethz.ch/R-manual/R-devel/library/methods/html/setClass.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 用"没有隐式行为"换掉了一整类继承陷阱：没有 vtable 就没有构造期派发与虚析构顺序问题，没有隐式转换就没有对象切片，没有名字继承就没有脆弱基类。剩下的是显式设计带来的成本：**手工 vtable 的指针转换错误是未定义行为**（`@ptrCast`/`@alignCast` 不检查类型）、**`comptime` 泛型造成的代码膨胀与编译时间**、**接口缺少类型标签导致无法安全 downcast**，以及**没有析构函数**因此资源释放必须显式传递 allocator。

```zig
const std = @import("std");

// ✅ 显式传递 allocator：没有析构函数，释放责任写在函数签名里
fn makeBuffer(alloc: std.mem.Allocator, n: usize) ![]u8 {
    const buf = try alloc.alloc(u8, n);
    defer alloc.free(buf);            // 谁分配谁释放，defer 保证路径唯一
    return buf;                       // 🛑 悬垂：返回后 buf 已被 free
}

// 手工 vtable：类型信息被抹掉，恢复时没有检查
const Any = struct {
    ptr: *anyopaque,
    vtable: *const struct { name: *const fn (*anyopaque) []const u8 },
    fn name(self: Any) []const u8 { return self.vtable.name(self.ptr); }
};
const Circle = struct {
    r: f64,
    fn nameImpl(_: *anyopaque) []const u8 { return "circle"; }
};
const Square = struct {
    s: f64,
    fn nameImpl(_: *anyopaque) []const u8 { return "square"; }
};

pub fn main() void {
    var c = Circle{ .r = 1.0 };
    var sq = Square{ .s = 2.0 };
    const a = Any{ .ptr = &c, .vtable = &.{ .name = Circle.nameImpl } };
    const b = Any{ .ptr = &sq, .vtable = &.{ .name = Square.nameImpl } };
    std.debug.print("{s} {s}\n", .{ a.name(), b.name() });   // circle square

    // 想 downcast 只能自己加类型标签；否则把 ptr 转成错误的类型是 UB
    const wrong: *Square = @ptrCast(@alignCast(a.ptr));      // 🛑 类型不匹配
    std.debug.print("{d}\n", .{wrong.s});                    // 1：把 Circle.r 的位模式当成 Square.s 读出来

    var buf: [4]u8 = undefined;
    const alloc = std.heap.page_allocator;
    if (makeBuffer(alloc, 4)) |_| {} else |_| {}
}
```

第一个坑是 `defer alloc.free(buf)` 与 `return buf` 共存：`defer` 在函数返回前执行，所以返回的切片指向已释放内存（Zig 的类型系统不会拦这个，只有借用检查器（如未来的 `-fbounds` 类工具或第三方静态分析）才可能提示），正确写法是把分配的所有权转移出去、把释放交给调用者，并在函数文档里写清。第二个坑是 downcast：`Any` 里只有 `*anyopaque` 与函数表，没有类型标识，因此 `@ptrCast(@alignCast(a.ptr))` 转成 `Square` 时不会报错，读到的是 `Circle.r` 的位模式（打印出 1.0），这类错误在优化后的二进制里极难定位；要安全 downcast 必须自己在接口里加 `type_id` 字段并断言。第三个坑是 `comptime` 泛型的代码膨胀：为许多类型实例化大型函数会显著增加二进制大小与编译时间（可以用 `@sizeOf` 与 `-fno-...` 之类的开关观察），权衡点与 C++ 模板相同。综合起来，Zig 的"零隐藏控制流"意味着每个陷阱都可以通过读代码发现——代价是没有编译器替你兜底，所以约定与测试更重要。

📘 [Zig · Documentation](https://ziglang.org/documentation/master/) ｜ 📘 [Zig · `std.mem.Allocator`](https://ziglang.org/documentation/master/std/#std.mem.Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的继承陷阱全部来自"表 + 元表"的自由度：**忘记设 `__index` 会静默断链**（表现为 `attempt to call a nil value`）、**`__index` 链深了会变慢**、**拼错键名不报错**（读 `nil`，写则生成新字段）、**`self` 丢失**（用 `.` 而不是 `:` 调用）、以及 **`pairs` 遍历顺序不确定**（在 mixin 拷贝时导致顺序依赖）。没有编译期检查，所以这些问题通常在运行时才暴露。

```lua
local Animal = {}
Animal.__index = Animal                 -- 忘记这行 → 实例找不到方法
function Animal.new(name) return setmetatable({ name = name }, Animal) end
function Animal:speak() return "..." end

local Broken = setmetatable({}, {})     -- 🛑 没有 __index
local d = Broken.new and Broken.new("x") or nil
print(d)                                -- nil（连 new 都找不到）
print(rawget(Animal, "__index") == Animal)  -- true

local a = Animal.new("Rex")
print(a:speak())                        -- ...
print(pcall(function() return a.speak() end))  -- true, "..."：方法取得到，但 self 是 nil
print(pcall(function() return a.spaek() end))  -- false（拼错方法名 → attempt to call a nil value）

a.name = "Tom"                          -- 写操作永远落在实例自己身上
print(a.name, Animal.name)              -- Tom nil
print(a.spaek)                          -- nil：读不存在的键不报错

-- pairs 顺序不确定 → mixin 拷贝顺序不可控
local M1 = { f = function() return "M1" end }
local M2 = { f = function() return "M2" end }
local Target = {}
for _, m in ipairs({ M1, M2 }) do       -- ipairs 可控顺序
  for k, v in pairs(m) do Target[k] = v end   -- ⚠️ pairs 不保证顺序
end
print(Target.f())                       -- M2（本例按数组顺序，最后写入者胜）
```

第一类事故是 `__index` 缺失：`setmetatable({}, {})` 得到的对象读任何键都是 `nil`，因此连 `new` 都找不到（`Broken.new` 为 `nil`），这类问题在 Lua 里不会给出"缺少 `__index`"的提示，只会在某个调用点报 `attempt to call a nil value`。第二类是方法与字段的拼写：`a:spaek()` 与 `a.spaek` 都只是读到一个不存在的键，`a.name = "Tom"` 会在实例上新建字段而不是修改原型（要改原型得写 `Animal.name = ...`），这两点在动态语言里很常见但 Lua 因为没有默认的字段名检查（可用 `__newindex` 或 `__index` 函数实现严格模式）而更隐蔽。第三类是 `self` 丢失：`a.speak()` 会用 `nil` 当 `self`，上面的 `Animal.speak` 恰好没用 `self`，所以侥幸返回了 `"..."`；方法内部只要访问 `self.x`（例如 `self.name`）就会报 `attempt to index a nil value`，而 `a:speak()` 才是正确写法；把方法存进变量再调用（`local f = a.speak; f()`）同样会丢 `self`。第四类是 `pairs` 的顺序不确定（Lua 不保证遍历顺序），在 mixin 拷贝时"后写覆盖先写"的语义因此可能不稳定；要确定性必须用数组加 `ipairs`（如上例），或者显式指定优先级（`if Target[k] == nil then ...`）。最后，深 `__index` 链的成本在热路径上不可忽略，实践中建议把链压平（拷贝方法到目标表）或最多保留两层。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4) ｜ 📘 [Lua 5.5 · `pairs`](https://www.lua.org/manual/5.5/manual.html#pdf-pairs)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的继承陷阱有一半是**类型系统与运行时的落差**：`private`/`protected`/`abstract`/`readonly` 在运行时全部消失，`as` 断言可以骗过编译器，`this` 在回调里会丢，字段初始化顺序在 `useDefineForClassFields` 打开后与旧行为不同，而结构化类型让"看起来兼容"的对象也能通过检查。

```typescript
abstract class Base {
  private secret = 42;                          // 运行时只是普通属性
  protected value = 1;
  abstract kind(): string;
  describe(): string { return `${this.kind()}:${this.value}`; }
}
class Sub extends Base {
  kind(): string { return "sub"; }              // 实现抽象成员（这里加 @ts-expect-error 反而会报"未使用"）
  peek(): number {
    // return this.secret;                      // 🛑 编译错误：private 只在本类可见
    return (this as any).secret;                // ⚠️ 断言可以绕过
  }
}
const s = new Sub();
console.log(s.describe());                      // sub:1
console.log(s.peek());                          // 42
console.log(Object.keys(s));                    // [ 'secret', 'value' ]：私有并不隐藏

// 字段初始化顺序：父类构造器里读子类字段会是 undefined
class Parent {
  constructor() { console.log("parent sees", (this as any).child); }
}
class Child extends Parent {
  child = "set-later";
}
new Child();                                    // parent sees undefined（然后才是赋值）

// this 丢失
class Counter {
  n = 0;
  inc() { this.n++; }
}
const c = new Counter();
const f = c.inc;
try { f(); } catch (e) { console.log("this 丢了:", (e as Error).constructor.name); }
const bound = c.inc.bind(c); bound();
console.log(c.n);                               // 1

// 结构化类型：多一个字段也算兼容
class Rect { constructor(public w: number, public h: number) {} }
class Square { constructor(public w: number, public h: number, public label: string) {} }
const r: Rect = new Square(1, 1, "sq");         // ✅ 结构兼容（但语义未必）
console.log(r.w);                               // 1
```

`private`/`protected` 与 `abstract` 只影响编译期：`Object.keys(s)` 能列出 `secret`，`as any` 可以读它，JavaScript 侧的代码也能直接改它；真正需要运行期私有必须用 `#field`（ECMAScript 私有字段，编译后仍是私有的，且 `Object.keys` 看不到），代价是 mixin 无法访问父类私有字段。字段初始化顺序的陷阱很实在：TypeScript 默认（`useDefineForClassFields` 为 `true` 的现代配置下）子类字段在 `super()` 返回后按声明顺序初始化，因此父类构造器里读子类字段一律是 `undefined`——这与 Java/C# 的"字段先初始化再执行构造器体"不同（Java 的子类字段在 `super()` 之后才初始化，但读到的是默认值而不是 `undefined`，语义相近却有不同的报错方式）。`this` 丢失来自 JS 的调用语义：`const f = c.inc; f()` 里 `this` 是 `undefined`（严格模式），要么 `bind`、要么用箭头函数字段（`inc = () => { this.n++ }`，代价是每个实例一份函数、且无法被 `super` 调用）。结构化类型让 `Square` 能被赋给 `Rect` 变量（形状兼容），这比名义类型宽松，因此"里氏替换"在 TypeScript 里更多是语义约定而非类型保证：只要形状对得上就能通过检查，`Square extends Rect` 那种经典陷阱不会被类型系统拦住。

📘 [TypeScript · Classes（private / #field）](https://www.typescriptlang.org/docs/handbook/2/classes.html) ｜ 📘 [TypeScript · Type compatibility](https://www.typescriptlang.org/docs/handbook/type-compatibility.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的继承陷阱来自原型链的共享性：**在原型上放引用类型会被所有实例共享**、**改原型会影响所有已创建实例**、**`this` 绑定丢失**、**`super` 在构造函数里必须在 `this` 之前**、以及**没有真正的私有（直到 `#field`）**。此外 `class` 与 `function` 混用、`Object.setPrototypeOf` 事后改链都会带来性能与语义问题。

```javascript
class Config {
  tags = [];                     // ✅ 每个实例一份数组（字段初始化器）
  static defaults = { retries: 1 };
}
class BadConfig {}
BadConfig.prototype.tags = [];   // 🛑 原型上的数组被所有实例共享
const a = new BadConfig(), b = new BadConfig();
a.tags.push("x");
console.log(b.tags);            // [ 'x' ]：b 也被改了

const c1 = new Config(), c2 = new Config();
c1.tags.push("x");
console.log(c2.tags);           // []：正确隔离

// 改原型影响所有已存在的实例
class Base { who() { return "Base"; } }
const inst = new Base();
Base.prototype.who = function () { return "patched"; };
console.log(inst.who());        // patched

// this 丢失 / super 顺序
class Counter {
  n = 0;
  inc() { this.n++; return this.n; }
}
const c = new Counter();
const f = c.inc;
try { f(); } catch (e) { console.log(e.constructor.name); }   // TypeError
console.log(c.inc.call(c));     // 1

class A { constructor() { this.ready = true; } }
class B extends A {
  constructor(flag) {
    // console.log(this.ready);   // 🛑 ReferenceError：super() 之前不能用 this
    super();
    this.flag = flag;
    console.log(this.ready, this.flag);   // true true
  }
}
new B(1);

// 运行时改链：可行但会破坏隐藏类优化
const obj = { x: 1 };
Object.setPrototypeOf(obj, { y: 2 });
console.log(obj.y, Object.getPrototypeOf(obj).y);   // 2 2

// #field：真正的私有（原型上的方法无法访问子类的 #field）
class Secret {
  #v = 42;
  get value() { return this.#v; }
}
const s = new Secret();
console.log(s.value, Object.keys(s));   // 42 []
// console.log(s.#v)                    // 🛑 SyntaxError
```

第一个陷阱是原型上的可变数据共享：把数组或对象放在 `prototype` 上（旧式写法或 `BadConfig` 那种）会让所有实例共用同一个引用，这是"为什么两个实例数据串了"的经典原因；用类字段初始化器（`tags = []`）能保证每个实例一份。第二个陷阱是原型的动态性：修改 `Base.prototype.who` 会立即改变所有实例（包括已创建的 `inst`），调试时"方法行为突然变了"通常源于某个库在往原型上打补丁。第三是 `this`：把方法取出单独调用会得到 `undefined`（严格模式）或全局对象（非严格模式），`call`/`bind`/箭头函数字段是三种解决方式，箭头函数字段的代价是每实例一个闭包且不能被 `super` 调用。第四是 `super()` 之前不能用 `this`：派生类构造器必须先调用 `super()`，否则直接 `ReferenceError`，这与 Java 的隐式 `super()` 不同（Java 会自动插入）。最后，`Object.setPrototypeOf` 与"运行时删/加属性"会让 V8 弃用该对象的隐藏类（hidden class）从而显著变慢，性能敏感代码应避免；修改原型本身在多数引擎里也会触发去优化。要真正私有就用 `#field`，但 `#field` 不能被原型上的方法访问，因此 mixin 无法像共享属性那样简单地读取它。

📘 [MDN · Classes（字段与私有）](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes) ｜ 📘 [MDN · Object.setPrototypeOf](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的继承陷阱集中在 trait 与 `parent::` 的语义、静态绑定（`self::` vs `static::`）、以及 `clone`/魔术方法与属性可见性的交互上：**trait 里写 `parent::` 会解析到使用方的父类**（复用被无关的类层次绑架）、**`self::` 是定义时的类而 `static::` 是运行时的类**（后期静态绑定）、**`private` 属性在子类不可见却同名可共存**、以及 **`__construct` 不遵守 `override` 签名检查**（PHP 8.3 的 `#[\Override]` 明确排除构造器）。

```php
<?php
trait Helper {
    public function call(): string { return "helper:" . $this->tag(); }  // 依赖宿主提供 tag()
}
class Service {
    use Helper;
    public function tag(): string { return "svc"; }
}
echo (new Service())->call(), PHP_EOL;     // helper:svc

class Widget {
    use Helper;
    public function tag(): string { return "wid"; }
}
echo (new Widget())->call(), PHP_EOL;      // helper:wid

trait Bad {
    public function up(): string { return strtoupper(parent::up()); }  // 🛑 依赖 parent
}
class Standalone { use Bad; }              // Standalone 没有父类
try {
    (new Standalone())->up();
} catch (Error $e) {
    echo get_class($e), PHP_EOL;           // Error: Cannot use "parent" when current class scope has no parent
}

class Base {
    public static function create(): static { return new static(); }  // 后期静态绑定
    public static function who(): string { return static::class; }
    private string $secret = "base";
    public function secret(): string { return $this->secret; }
}
class Derived extends Base {
    private string $secret = "derived";    // ⚠️ 与父类 private 同名：两个独立属性
    public function secret(): string { return $this->secret; }
}
$d = new Derived();
echo get_class(Derived::create()), PHP_EOL;   // Derived
echo Derived::who(), PHP_EOL;                 // Derived
echo $d->secret(), PHP_EOL;                   // derived
echo (new Base())->secret(), PHP_EOL;         // base

class Cloneable {
    public array $items = [];
    public function __clone() { $this->items = []; }   // clone 时清空
}
$o = new Cloneable(); $o->items[] = 1;
$copy = clone $o;
echo count($copy->items), PHP_EOL;            // 0（浅拷贝 + __clone 修正）
```

trait 里写 `parent::` 是典型的"复用被上下文绑架"：`Bad::up()` 只有被嵌套在"有父类且父类有 `up`"的类里才能工作，换个使用方就抛 `Error`（`Cannot use "parent" when current class scope has no parent`）；可复用的 trait 应只调用**使用方自己声明的接口**（如上例的 `tag()`），需要父类协作就写成抽象方法要求使用方实现。`self::` 与 `static::` 的区别是 PHP 的后期静态绑定（Late Static Binding）：`self::who()` 取定义时的类，`static::who()` 取运行时调用的类，工厂方法与前缀常量都必须用 `static::`，否则子类调用会拿到父类结果。`private` 属性与父类同名时是两个独立属性（子类的方法无法访问父类的那个），这既是不出错也是容易迷惑的地方——调试时看到"我在父类方法里改了字段但子类没变"就是这个原因；用 `protected` 才能共享。`clone` 是浅拷贝，引用类型字段仍共享，必须用 `__clone` 修正，深层次继承让 `__clone` 的责任分散（父类 `__clone` 不会自动被调用，子类覆盖后要用 `parent::__clone()`），这也是一类典型的"深继承 + 生命周期钩子"陷阱。最后，`__construct` 有意不参与签名检查，因为子类构造器签名本来就与父类不同，所以 `#[\Override]` 不能（也不必）标在构造器上。

📘 [PHP · Traits](https://www.php.net/manual/en/language.oop5.traits.php) ｜ 📘 [PHP · Late static binding](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的陷阱几乎都与"祖先链顺序"有关：**`include` 的顺序决定谁覆盖谁**（后 include 的排得更前）、**module 依赖宿主的方法名**（宿主改名就 `NoMethodError`）、**`prepend` 的包裹顺序敏感**、**`method_missing` 与 `respond_to_missing?` 必须成对**、以及**深祖先链带来的调试成本**（还好 `ancestors`、`instance_method`、`owner` 让定位很快）。

```ruby
module M1
  def who = "M1"
end
module M2
  def who = "M2"
end
class C1
  include M1
  include M2
end
class C2
  include M2
  include M1
end
puts C1.new.who                      # M2（后 include 的优先）
puts C2.new.who                      # M1
puts C1.ancestors.take(3).inspect    # [C1, M2, M1]

module Saver
  def save = "saved:#{self.payload}"   # 依赖宿主提供 payload（显式接收者，缺失时是 NoMethodError）
end
class Doc
  include Saver
  def payload = "doc"
end
puts Doc.new.save                    # saved:doc
begin
  Class.new { include Saver }.new.save
rescue NoMethodError => e
  puts "NoMethodError"               # 宿主没提供 payload
end

module P1
  def who = "P1+" + super
end
module P2
  def who = "P2+" + super
end
class C3
  prepend P1
  prepend P2
  def who = "C3"
end
puts C3.new.who                      # P2+P1+C3

# method_missing 与 respond_to_missing? 必须成对，否则 respond_to? 说谎
class Ghost
  def method_missing(name, *args)
    name.to_s.start_with?("ghost_") ? "boo" : super
  end
  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("ghost_") || super
  end
end
g = Ghost.new
puts g.ghost_x                        # boo
puts g.respond_to?(:ghost_x)          # true
puts g.respond_to?(:nope)             # false
puts C3.instance_method(:who).owner   # P2：prepend 的 module 才是真正被调用的定义处
```

`include` 的顺序语义是最需要背下来的一条：先 `include` 的 module 在祖先链里更靠后，因此**后 include 的覆盖先 include 的**（`C1.new.who` 得到 `"M2"`），这与 Dart 的 `with` 列表一致，而与"先注册优先"的直觉相反。`prepend` 同理，最后 `prepend` 的 module 最先被调用（`C3.new.who` 得到 `"P2+P1+C3"`），因此日志/事务这类环绕逻辑的叠加顺序要靠调整 `prepend` 顺序来控制——这正是"顺序依赖"最容易出事的地方，建议为每个 prepend 模块写一句注释说明它相对谁在前。module 依赖宿主方法名的问题在 Ruby 里很常见（module 无法声明"使用方必须有 `payload`"），缓解方式是让 module 在被 include 时用 `included` 钩子检查（`raise unless host.method_defined?(:payload)`）或者用 `Module#abstract_method` 之类的约定（Ruby 本身没有抽象方法关键字，2.7 起 `module` 内可以声明 `def payload; end` 只作为文档）。`method_missing` 是 Ruby 的动态派发终极手段（也是 `SimpleDelegator` 的实现基础），但覆盖它时必须同时实现 `respond_to_missing?`，否则 `respond_to?`、`method`、`duck typing` 检查都会给出错误答案，而且每次未命中都会走异常路径（性能差）。好处是 Ruby 的反射非常透明：`instance_method(:who).owner`、`ancestors`、`method(:x).source_location` 能在几秒内定位"到底执行了谁的实现"，这是动态语言在排查继承问题时的最大优势。

📘 [Ruby · Modules and classes](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html) ｜ 📘 [Ruby · method_missing](https://docs.ruby-lang.org/en/master/BasicObject.html#method-i-method_missing)

{{% /tab %}}

{{< /tabpane >}}
