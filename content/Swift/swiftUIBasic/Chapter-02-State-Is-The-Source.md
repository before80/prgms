+++
title = "第 2 章 状态是唯一的事实来源"
weight = 20
date = "2026-09-20T11:40:00+08:00"
type = "docs"
description = "@State / @Binding / @Observable / @Environment 的选择判据，以及「改了数据界面不刷新」的四种病因与定位方法"
isCJKLanguage = true
draft = false
+++

# 第 2 章：状态是唯一的事实来源

> 第 1 章说"视图是描述"。这一章回答下一个问题：**描述依据什么生成？** 答案是状态。而 SwiftUI 里绝大多数的 bug，都能归结成一句话——**你以为的那个状态，框架没在看。**

## 2.1 `@State` 到底是什么

先看一段最普通的代码：

```swift
import SwiftUI

struct Counter: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("点了 \(count) 次")
            Button("加一") { count += 1 }
        }
    }
}
```

第 1 章刚说过"`body` 里不能改 `self`"，可这里 `count += 1` 明明改的就是 `self` 的一部分——为什么合法？

因为 `@State` **不是存储属性**，它是**属性包装器**：编译器在背后把它换成另一个类型，并提供了一个可写的投影。展开之后大致是这样（📘 **这是概念模型，不是合法源码**——写出来是为了让你看清 `nonmutating` 从哪来）：

```text
struct Counter: View {
    // 你写的
    @State private var count = 0

    // 编译器背后约等于生成的东西
    private var _count: State<Int> = State(wrappedValue: 0)
    private var count: Int {
        get { _count.wrappedValue }
        nonmutating set { _count.wrappedValue = newValue }
    }
}
```

关键在于最后那个 **`nonmutating set`**：`count` 的 setter 不改 `self`，它改的是 `_count` **指向的那块外部存储**。

🔥 这就是全部秘密：`@State` 把值**存到了视图结构体之外的某个地方**，视图里只留一个"取用它的入口"。所以：

- 视图结构体可以是一次性的、被丢弃的值，状态却不会跟着丢；
- `body` 里的 `count += 1` 改的是那块外部存储，不违反"`self` 不可变"；
- 这块存储一变，SwiftUI 就知道"这个视图要重画了"。

⚠️ 一条铁律顺势而来：**`@State` 必须标在 `var` 上**。标在 `let` 上编译器直接拒绝，因为它需要那个 setter：

```text
error: '@State' can only be applied to a 'var' declaration (from macro 'State')
```

## 2.2 `@State` 的三条规则

### 规则一：`@State` 是"视图私有"的，外面不该碰它

`@State` 的正确用法是**这个视图自己用的、外部不关心的**数据。一旦你想让父视图也能改它，就该换成 `@Binding`（下一节）。

⚠️ 常见的错法是给 `@State` 加 `private` 之外的可访问性、然后从父视图直接赋值——那等于绕过 SwiftUI 的数据流，会出现"父视图改了、子视图不刷新"的怪事。

💭 惯例：**`@State` 永远配 `private`**。如果你发现需要去掉 `private`，那通常说明这个状态放错了地方。

### 规则二：`@State` 的初始值"惰性 + 只算一次"

像这样给初值（📘 单行示意，不是完整类型）：

```text
@State private var items = Self.loadItems()
```

这个 `Self.loadItems()` 什么时候执行？答案是**两个都出乎直觉**：

🔬 **实测一：它是惰性的**——创建视图值的时候**一次都不执行**。只有真正开始渲染时才求值：

```text
① 只执行 `_ = ViewA()`（创建视图值）      → 初始化表达式执行 0 次
② 渲染这个视图                            → 执行 1 次
```

🔬 **实测二：同一个视图反复布局，只执行一次**：

```text
第 1 次布局 → 求值次数 1
第 2 次布局 → 求值次数 1     ← 没有重新执行
第 3 次布局 → 求值次数 1
```

💭 这两条合起来的意思是：**"这个视图的记忆"在它第一次真正出现时建立，之后就一直沿用。** 对性能是好事（`Self.loadItems()` 这种重活不会反复跑），但也带来一个陷阱：

🝖 **顺手看一眼机制**：翻 `SwiftUICore` 的接口文件，`State` 有两个初始化器——

```text
public init(wrappedValue value: Value)
@available(iOS 17.0, macOS 14.0, *)
internal init(wrappedValue thunk: @autoclosure @escaping () -> Value)
    where Value : AnyObject, Value : Observation.Observable
```

第二个带 `@autoclosure`，也就是"先不求值，等真要用了再算"——这正是惰性的来源，而且它**专门服务于 `@Observable` 类**。这解释了为什么"用 `@State` 持有一个 `@Observable` 模型"在新代码里被推荐：初始化的开销被推迟到你真正需要它的时候。

```swift
struct Bad: View {
    var seed: Int
    @State private var value = 0

    init(seed: Int) {
        self.seed = seed
        _value = State(wrappedValue: seed)    // ⚠️ 只在"这个视图第一次出现"时生效
    }

    var body: some View { Text("\(value)") }
}
```

🔬 实测：父视图把 `seed` 从 1 改成 2，`value` **仍然是 1**。

```text
init(seed:1) → body: seed=1 value=1
init(seed:2) → body: seed=2 value=1     ← value 没跟着变
```

`init` 确实被重新执行了（所以 `seed` 变成了 2），但那句 `_value = State(...)` 对已经建立的存储**不再起作用**。

🔥 记住这条：**`@State` 表达的是"这个视图自己的记忆"，不是"父视图传入的值的副本"。** 想让内部跟着外部走，你要么用 `@Binding`，要么用 `.onChange(of:)` / `.task(id:)` 显式响应。

### 规则三：`@State` 装引用类型时，只认"换掉整个实例"

这是最贵的一课。`@State` 判断"变没变"的方式是**比较那个值本身**。装结构体时一切正常；装普通类时：

🔬 **实测对比**（用 Observation 的追踪机制直接观测，不涉及界面）：

```swift
import SwiftUI
import Observation

final class Plain { var value = 0 }          // 普通类
@Observable final class Tracked { var value = 0 }

// 分别"读一次 value，然后改 value"，看 onChange 会不会被触发
// 普通类   改属性: onChange 触发 0 次
// @Observable 改属性: onChange 触发 1 次
```

| 你写的 | 会发生什么 |
| --- | --- |
| `@State private var c = Plain()`<br>`c.value += 1` | 🛑 **界面不刷新**。`Plain` 实例本身没变（还是同一个指针），框架看不出任何变化 |
| `@State private var c = Plain()`<br>`c = Plain()` | ✅ 刷新。整个实例被换掉了，框架看得见 |
| `@State private var c = Tracked()`（`@Observable`）<br>`c.value += 1` | ✅ 刷新。`@Observable` 会逐属性上报变化 |

💭 一句话：**`@State` 适合装值类型；要装对象并观察它的属性变化，那个对象必须标 `@Observable`。** 下面第 2.4 节会把这件事讲透。

## 2.3 `@Binding`：把"写权限"借出去

子视图想改父视图的状态，但它不该拥有那份状态。这时用 `@Binding`：

```swift
struct Stepper: View {
    @Binding var value: Int          // 不是我拥有的，是借来的

    var body: some View {
        HStack {
            Button("−") { value -= 1 }
            Text("\(value)").monospacedDigit()
            Button("+") { value += 1 }
        }
    }
}

struct Parent: View {
    @State private var count = 0

    var body: some View {
        Stepper(value: $count)       // $ 取出"绑定"，而不是值
        Text("父视图看到的：\(count)")
    }
}
```

### `$` 是什么

`$count` 拿到的是 `Binding<Int>`——一个**读写通道**，不是值的拷贝。子视图通过它读到的永远是父视图当前的值，写进去的也直接落到父视图的状态上。

| 写法 | 拿到什么 | 用在哪 |
| --- | --- | --- |
| `count` | `Int`（当前值） | 在 `body` 里读、参与运算 |
| `$count` | `Binding<Int>`（读写通道） | 传给子视图、传给需要绑定的控件 |

⚠️ 三个高频报错，都跟这个有关。为了看清它们，先约定一个"需要绑定"的子视图：

```swift
struct Child: View {
    @Binding var n: Int
    var body: some View { Text("\(n)") }
}
```

现在看三种写法错在哪：

```swift
// ① 来源是 let 属性 —— 它没有可写通道，所以没有 $ 可用
struct P: View {
    let n = 0
    var body: some View { Child(n: $n) }   // 🛑 cannot find '$n' in scope
}

// ② 忘了写 $ —— 传过去的是"值"，不是"通道"
struct Q: View {
    @State private var count = 0
    var body: some View { Child(n: count) }   // 🛑 cannot convert value of type 'Int'
                                              //    to expected argument type 'Binding<Int>'
}

// ③ 在 @Binding 属性上多写了 $ —— 打出来的是 Binding 的描述，不是数字
struct R: View {
    @Binding var value: Int
    var body: some View { Text("\($value)") }  // ⚠️ 不报错，但打印结果不是你以为的
}
```

🔥 三条规律：

| 情况 | `$` 能不能用 |
| --- | --- |
| `@State` / `@Binding` / `@Bindable` 属性 | ✅ 有 `$` |
| 普通 `let` / 普通 `var` 属性 | ❌ 没有 `$`，报 `cannot find '$x' in scope` |
| 需要绑定参数的控件，却传了裸值 | ❌ 报 `cannot convert value of type 'T' to expected argument type 'Binding<T>'` |

💭 记忆法：**`$` 只在"需要别人能改"的时候用**。读值不加 `$`，传绑定加 `$`。

### `@Binding` 值不值得用

`@Binding` 会让子视图**不能被单独预览**（它需要一个外部的状态来源）。如果你的子视图只是想显示数据、不想改数据，就老老实实传值：

```swift
struct Label: View {
    let value: Int        // ✅ 只读就传值，好预览、好测试
    var body: some View { Text("\(value)") }
}
```

🔥 判据：**子视图要"改"才用 `@Binding`，只"看"就传普通值。**

## 2.4 `@Observable`：给对象装上"变化上报"

`@State` 装普通类不刷新，那共享的对象数据该怎么办？答案是 `@Observable`（Swift 5.9 / iOS 17 起）：

```swift
import SwiftUI

@Observable
final class Cart {
    var items: [String] = []
    var total: Int = 0
    var note: String = ""          // 给下面 @Bindable 的例子用

    func add(_ name: String) {
        items.append(name)
        total += name.count
    }
}
```

`@Observable` 是宏，它给每个存储属性加上"被读时登记、被写时上报"的能力。**关键特性是它是按属性追踪的**：

🔬 **实测**：只读过 `count`，然后改 `name`，不会触发；改 `count` 才触发。

```swift
// 只读 count，然后：
//   改 name  → onChange 触发 0 次
//   改 count → onChange 触发 1 次
```

这意味着"改一个属性只刷新用到它的视图"，而不是"改任何属性全量刷新"。这是它相比老的 `ObservableObject` 最大的改进。

### 怎么用

```swift
struct CartView: View {
    @State private var cart = Cart()      // ✅ 自己创建并拥有它

    var body: some View {
        VStack {
            Text("共 \(cart.total) 元")
            Button("加一本书") { cart.add("书") }
        }
    }
}
```

```swift
struct DetailView: View {
    let cart: Cart                        // ✅ 只是借用来看，用 let 就够
    var body: some View { Text("\(cart.items.count) 件") }
}
```

⚠️ 注意第二个例子：**子视图接收 `@Observable` 对象时用朴素的 `let`，不需要任何 `@` 前缀**。这和老的 `@ObservedObject` 写法完全不同，也是很多人从旧教程迁移时最容易多写的地方。

| 你的意图 | 该写什么 |
| --- | --- |
| 我创建并拥有这个模型 | `@State private var model = Model()` |
| 别人给我，我只读 | `let model: Model` |
| 别人给我，我要**改它的属性**并生成绑定 | `@Bindable var model: Model` |
| 从环境里取 | `@Environment(Model.self) private var model` |

### `@Bindable`：给可观察对象造绑定

`@Observable` 对象的属性要接到 `TextField`、`Toggle` 这类需要 `Binding` 的控件上时，用 `@Bindable`：

```swift
import SwiftUI

@Observable
final class Cart {
    var items: [String] = []
    var note: String = ""
}

struct EditView: View {
    @Bindable var cart: Cart            // ← 有了它，才能写出 $cart.xxx

    var body: some View {
        VStack {
            TextField("备注", text: $cart.note)
            // 普通 let 属性是写不出 $cart.note 的，
            // 因为 $ 前缀只有 @State / @Binding / @Bindable 才有
        }
    }
}
```

⚠️ `@Bindable` 只能用在**对象**上。套在结构体上会报：

```text
error: 'init(wrappedValue:)' is unavailable: The wrapped value must be an object
```

💭 `@State` 和 `@Bindable` 的分工：**`@State` 负责"拥有"，`@Bindable` 负责"给别人的对象造绑定"。**

## 2.5 `@Environment`：看不见的传递通道

有些值需要穿过很多层视图，一层层传太啰嗦。`@Environment` 让它们"从空气里取"：

```swift
struct DeepView: View {
    @Environment(\.colorScheme) private var colorScheme     // 系统内置
    @Environment(\.dynamicTypeSize) private var typeSize

    var body: some View {
        Text(colorScheme == .dark ? "暗色模式" : "亮色模式")
    }
}
```

自定义环境值现在用 `@Entry`（Swift 6 / iOS 18 起），比老的 `EnvironmentKey` 样板省很多：

```swift
extension EnvironmentValues {
    @Entry var themeColor: Color = .blue
}

struct Themed: View {
    @Environment(\.themeColor) private var themeColor
    var body: some View { Text("主题色").foregroundStyle(themeColor) }
}

// 注入
Themed().environment(\.themeColor, .orange)
```

⚠️ **环境值的默认值必须有**。忘了给默认值、又没有注入，会直接崩溃（`@Entry` 要求你写默认值，就是为了堵住这个）。

## 2.6 选择判据：一张决策表

不用背，遇到新状态时按顺序问自己：

| 问题 | 是 | 否 |
| --- | --- | --- |
| 这个数据是**这个视图自己**的记忆吗？ | `@State private` | 往下问 |
| 是父视图给的、我需要**改**它吗？ | `@Binding` | 往下问 |
| 是一个**要在多个视图间共享的对象**吗？ | `@Observable` 类型 + 拥有者用 `@State` | 往下问 |
| 需要穿过很多层、或者本身就是环境概念吗？ | `@Environment` | 传普通值 |

再补三条经验：

| 场景 | 建议 |
| --- | --- |
| 派生数据（能算出来的） | **不要**存成状态。写成计算属性，避免两份数据打架 |
| 只在子视图内部用 | 放在最靠近使用处的那个视图里，别提前上提到顶层 |
| 需要持久化 | `@AppStorage`（小配置）或写文件/数据库（正式数据） |

🔥 **最重要的一条**：**能算出来的就不要存。** 两份互相矛盾的状态，是所有诡异 bug 的根源。

## 2.7 「改了数据界面不刷新」的三种病因

这是 SwiftUI 最经典的 bug，症状一样，病因通常是这三种。按出现频率排：

### 病因一：用普通类当状态（最高频）

⚠️ 先说清楚：**下面这段能编译，问题全在运行期**——点按钮，界面纹丝不动。

```swift
final class Model { var items: [String] = [] }   // 少了 @Observable

struct List1: View {
    @State private var model = Model()
    var body: some View {
        Button("加一条") { model.items.append("新") }
        Text("\(model.items.count)")
    }
}
```

**诊断**：给类加上 `@Observable`。**根因**：`Model` 实例本身没变（还是同一个引用），SwiftUI 没有任何途径知道它的属性被改了。

💭 这类"编译通过、运行期不工作"的问题，才是 SwiftUI 最费时间的一类 bug——编译器帮不了你，只能靠数据流的模型去推。

### 病因二：状态放错了位置

⚠️ 同样**能编译**，问题在于"够不着"：

```swift
struct Row: View {
    @State private var liked = false     // 每一行各有一份，外部无法控制
    var body: some View { Button(liked ? "已赞" : "点赞") { liked.toggle() } }
}
```

单独看没问题，但如果你想"一键全部取消赞"，就会发现够不着这些状态。

**诊断**：把状态上提到父视图，用 `@Binding` 传下去，或者在模型里存一个 `Set<ID>`。

### 病因三：数组里的元素是引用类型

这是病因一的"变种"，而且更隐蔽，因为它**看起来是在改数组**：

```swift
final class Item {                // 普通类
    var name: String
    init(name: String) { self.name = name }
}

struct List3: View {
    @State private var items = [Item(name: "a")]

    var body: some View {
        VStack {
            // ⚠️ 能编译，但界面不刷新
            Button("改名") { items[0].name = "新名字" }
            Text(items[0].name)
        }
    }
}
```

**为什么不动？** 因为 `items` 这个数组**本身没有变**——变的只是它指向的那个对象内部的属性。SwiftUI 比较的是数组的值，数组里存的还是同一个引用，所以它认为"什么都没发生"。

⚠️ 对照组：如果 `Item` 是 **`struct`**，那么 `items[0].name = ...` 会真的修改数组里那个元素的值，数组变了，界面就刷新。

| 数组元素类型 | `items[0].name = "x"` 的结果 |
| --- | --- |
| `struct Item` | ✅ 数组值变了，界面刷新 |
| 普通 `class Item` | 🛑 数组看起来没变，界面不动 |
| `@Observable class Item` | ✅ 属性变化会被上报，界面刷新 |

**诊断**：把 `Item` 改成 `struct`（首选，值语义更简单），或者给它加 `@Observable`。

### 顺便澄清一个流传很广的误解

网上常有一种说法："`@Observable` 的追踪只在 `body` 里直接读属性才有效，一旦把值存进局部变量、或者通过函数读，就追踪不到了。"

🔬 **实测：这是错的。** 三种读法**全都正常触发**（用 `withObservationTracking` 观测，改 `total` 后看回调）：

| 读法 | 是否触发 |
| --- | --- |
| `body: { _ = $0.total }` 直接读 | ✅ 触发 1 次 |
| `body: { let s = $0.total; _ = s }` 先存局部常量 | ✅ 触发 1 次 |
| `body: { _ = helper($0) }` 通过普通函数读 | ✅ 触发 1 次 |

**原因**：`@Observable` 追踪的是"**这个属性有没有在本次求值过程中被访问过**"，跟"在哪一行、隔着几层函数"毫无关系。

💭 所以你不必为了"保住追踪"而刻意避免辅助函数或局部变量——该抽函数就抽。真正会让追踪失效的，是前面那三种病因（类没标 `@Observable`、状态放错位置、数组装普通类）。

### 定位工具：`Self._printChanges()`

这是 SwiftUI 自带的诊断方法（macOS 12 / iOS 15 起），在 `body` 开头调用，它会在控制台打印出**这次 `body` 为什么被调用、哪个属性变了**：

```text
var body: some View {
    let _ = Self._printChanges()      // 🔥 只在调试时加，别提交
    VStack { ... }                    // 你原来的内容
}
```

输出形如：

```text
Counter: _count changed.
Detail: @self changed.
```

🔥 这是排查"刷新问题"的第一把工具。看到 `@self changed` 说明**这个视图被整个重建了**（通常是身份变了，见第 6 章）；看到具体属性名就说明是那个属性触发的。

⚠️ 它会污染控制台、也有性能开销，**只用来临时定位，定位完删掉**。

## 2.8 完整可运行文件

```swift
import SwiftUI

// 共享模型：必须 @Observable，否则改属性不会刷新
@Observable
final class ShoppingCart {
    var items: [String] = []
    var note: String = ""

    var count: Int { items.count }              // 派生数据用计算属性，不另存一份

    func add(_ name: String) { items.append(name) }
    func removeAll() { items.removeAll() }
}

// 只读子视图：用 let 接收，不需要 @ 前缀
struct CartSummary: View {
    let cart: ShoppingCart

    var body: some View {
        Text("共 \(cart.count) 件")
            .font(.headline)
    }
}

// 需要改属性的子视图：用 @Bindable 才能写 $cart.note
struct CartEditor: View {
    @Bindable var cart: ShoppingCart

    var body: some View {
        TextField("备注", text: $cart.note)
            .textFieldStyle(.roundedBorder)
    }
}

// 借用写权限：@Binding
struct AddButton: View {
    @Binding var names: [String]

    var body: some View {
        Button("加一件") { names.append("商品 \(names.count + 1)") }
    }
}

struct Chapter02Demo: View {
    @State private var cart = ShoppingCart()     // 我拥有这个模型

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 16) {
                CartSummary(cart: cart)

                CartEditor(cart: cart)           // 传对象本身，不是 $

                AddButton(names: $cart.items)    // 传绑定，要 $

                List(cart.items, id: \.self) { Text($0) }

                Button("清空", role: .destructive) { cart.removeAll() }
            }
            .padding()
            .navigationTitle("购物车")
        }
    }
}

#Preview {
    Chapter02Demo()
}
```

⚠️ 这个文件里藏着三个容易写错的地方，对照一下你有没有踩：

| 位置 | 为什么这么写 |
| --- | --- |
| `CartSummary(cart: cart)` | 只读，传**对象**（不是 `$cart`） |
| `CartEditor(cart: cart)` | 同样传对象；`@Bindable` 在**子视图内部**声明 |
| `AddButton(names: $cart.items)` | 要改数组，传**绑定**（`$`）；注意 `$` 加在 `cart` 上而不是 `items` 上 |

## 2.9 本章易错点速查

| 你会怎么写 | 实际发生什么 | 正确做法 |
| --- | --- | --- |
| `@State private let x = 0` | `'@State' can only be applied to a 'var' declaration` | 改成 `var` |
| 普通类 + `@State`，改属性 | 界面不刷新 | 类加 `@Observable` |
| 从 `let` 属性取 `$x` | `cannot find '$x' in scope` | 只有 `@State`/`@Binding`/`@Bindable` 才有 `$` |
| `Child(n: count)` 想传绑定 | `cannot convert value of type 'Int' to expected argument type 'Binding<Int>'` | 写 `Child(n: $count)` |
| 子视图收 `@Observable` 对象写成 `@ObservedObject` | 老教程的写法，新代码里多余甚至报错 | 直接写 `let model: Model` |
| `@Bindable` 用在 struct 上 | `The wrapped value must be an object` | `@Bindable` 只用于类 |
| 派生数据也存一份 `@State` | 两份数据不一致，bug 难查 | 写成计算属性 |
| 初始值放进 `init` 里赋给 `@State` | 只在该视图**首次出现**时生效，`seed` 变了它不跟随（实测 `seed=2` 时 `value` 仍是 1） | 用 `@Binding` 或 `.onChange(of:)` |
| 以为 `@State` 的初值表达式在创建视图时就算 | 它是**惰性**的：不渲染就不求值 | — |
| 忘了给 `@Environment` 自定义值默认值 | 运行期崩溃 | `@Entry var x: T = 默认值` |

## 2.10 下一章

到现在为止，你已经能正确管理状态了。但还有一个更基础的问题没解决：**这些视图到底怎么决定自己该多大、摆在哪？**

这是 SwiftUI 里唯一"不看数字就学不会"的部分，也是绝大多数界面问题的根源。下一章我们用实测数据把布局规则拆开——包括 `Spacer` 到底分走多少、`frame` 的四层含义、以及为什么你的视图总是不听话。
