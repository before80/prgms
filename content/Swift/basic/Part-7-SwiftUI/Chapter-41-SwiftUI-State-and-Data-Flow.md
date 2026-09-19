+++
title = "第41章 状态与数据流：谁拥有数据，谁只是借用"
weight = 410
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "@State、@Binding、@Observable、@Environment 的分工：一份状态该放在哪一层，数据为什么必须单向流动"
isCJKLanguage = true
draft = false
+++

# 第四十一章：状态与数据流：谁拥有数据，谁只是借用

> 上一章说"状态是唯一的事实来源"。可一旦界面有五六层嵌套，这句口号立刻变成一个更具体的问题：**这份状态放在哪一层？** 放高了，中间三层视图被迫当传话筒；放低了，兄弟视图读不到。这一章把 SwiftUI 里那四个属性包装器排成一张地图，从此不再靠猜。

## 41.1 三个问题决定一切

面对一份会变的数据，先问三个问题，答案基本就写死了：

1. **谁创建它？** 是某个视图自己造出来的临时状态，还是从外部传进来的？
2. **谁会改它？** 只有它自己改，还是需要让子视图、兄弟视图也能改？
3. **它活多久？** 跟着某个视图的生命周期，还是整个应用共享？

SwiftUI 的四个常用包装器，正好对应这几种组合：

| 包装器 | 谁拥有 | 谁能改 | 典型场景 |
| --- | --- | --- | --- |
| `@State` | 视图自己 | 视图自己（`$` 借给别人） | 展开/收起、输入框文字、选中的标签页 |
| `@Binding` | 别人 | 我（通过借来的引用） | 子视图里的输入控件、可复用组件 |
| `@Observable` 类的引用 | 创建它的那一层 | 读到它的任何视图 | 跨页面共享的业务模型 |
| `@Environment` | 祖先视图或系统 | 取决于注入方式 | 主题、语言、`dismiss`、共享模型 |

先记住一句话：**`@State` 和 `@Observable` 都是"拥有"，`@Binding` 和 `@Environment` 都是"借用"。** 下面逐个拆开。

## 41.2 `@State`：视图自己的一块私房钱

```swift
import SwiftUI

struct TabDemo: View {
    @State private var selected = "首页"
    @State private var isExpanded = false

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                ForEach(["首页", "发现", "我的"], id: \.self) { tab in
                    Button(tab) { selected = tab }
                        .fontWeight(selected == tab ? .bold : .regular)
                }
            }
            DisclosureGroup("更多设置", isExpanded: $isExpanded) {
                Text("展开后才显示的内容")
            }
        }
        .padding()
    }
}

// 界面效果：三个按钮中当前选中的加粗；点"更多设置"展开一段文字
```

两个按钮、一个展开箭头，全是界面状态，没有一条需要别的视图知道。这就是 `@State` 的主场：**只影响自己这一小块界面、别人不关心的数据。**

这里有个必须讲清楚的细节，它解释了很多"莫名其妙重置了"的 bug：**`@State` 的存储并不在结构体里。**

视图是结构体，结构体是值类型，每次 `body` 重算都会造一批新结构体。如果 `@State` 真存在结构体的某个字段里，那它每次重算就跟着重置，界面根本没法用。SwiftUI 的做法是：把这块存储放在视图树的一个旁挂位置，用"视图的身份"当钥匙。结构体只是每次重算时拿到一把指向那份存储的引用。

```swift
import SwiftUI

struct ResetDemo: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 8) {
            Text("count = \(count)")
            Button("加一") { count += 1 }
            // 每次 body 重算都会新建一个 ResetDemo 结构体，
            // 但 count 挂在视图树上，值还是接着往下数
            Text("这一行的结构体编号：\(UUID().uuidString.prefix(4))")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}

// 界面效果：点"加一"时 count 递增；
// 但那行小字里的随机编号每次重算都会变——它证明了结构体确实被重建了
```

这段代码给出了一个"看得见的证明"：编号每次都在变（结构体是新的），`count` 却不会归零（存储挂在外面）。理解这一点之后，第 43 章"列表一滚动数据就丢"的坑就有了解释。

### 用初始值初始化 `@State`

`@State private var count = 0` 这种写法编译器帮你生成了默认值。如果初始值来自外部参数，得自己在 `init` 里设，而且**必须写 `_count`**：

```swift
import SwiftUI

struct Countdown: View {
    @State private var remaining: Int

    init(start: Int) {
        // 注意是 _remaining，不是 remaining
        _remaining = State(initialValue: start)
    }

    var body: some View {
        Text("剩余 \(remaining)")
    }
}
```

为什么是 `_remaining`？因为 `@State var remaining` 展开以后，编译器生成的实际存储属性名字叫 `_remaining`，类型是 `State<Int>`；`remaining` 只是一个转发到 `wrappedValue` 的计算属性（第 15B.6 节讲过这种"一个标注换三个成员"的机制）。在 `init` 里，你有权对存储属性直接赋值，但没法对计算属性赋值。

⚠️ 一个高频误区：**`init` 里传进来的初始值只生效一次。** 父视图后来改了那个参数，`Countdown` 里的 `start` 不会跟着变——因为它已经存进自己的小仓库了。要让外部变化生效，就不该用 `@State` 存它（见 41.4）。

### `@State` 存引用类型会怎样

`@State` 能存类实例，但注释里那句话是对的：

```swift
import SwiftUI
import Observation

final class PlainCounter {
    var value = 0            // 普通类：改它不会通知 SwiftUI
}

@Observable
final class TrackedCounter {
    var value = 0            // @Observable：改它会通知 SwiftUI
}

struct StoreDemo: View {
    @State private var plain = PlainCounter()
    @State private var tracked = TrackedCounter()

    var body: some View {
        VStack {
            Text("普通类：\(plain.value)")     // 点按钮后这里不会更新
            Text("可观察类：\(tracked.value)") // 点按钮后这里会更新
            Button("都加一") {
                plain.value += 1
                tracked.value += 1
            }
        }
    }
}

// 界面效果：点一次按钮，第二行从 0 变 1；
// 第一行看上去没动——直到其他原因导致 body 重算，才突然显示最新值
```

第一行的"延迟显示"是典型症状：**数据其实改了，只是没人通知界面。** 只要给类加上 `@Observable`，观察机制就接上了。第 41.4 节会完整讲这个宏。

## 41.3 `$` 与 `@Binding`：只借出写权限

一个可复用组件（比如自定义的输入框、评分控件）不可能自己拥有数据——数据属于调用方。它需要的是一份"能读能写，但不拥有"的引用。这就是 `@Binding`。

```swift
import SwiftUI

struct StarRating: View {
    // 借用：不创建、不拥有，只负责读写
    @Binding var rating: Int
    var max = 5

    var body: some View {
        HStack {
            ForEach(1...max, id: \.self) { i in
                Image(systemName: i <= rating ? "star.fill" : "star")
                    .foregroundStyle(.yellow)
                    .onTapGesture { rating = i }
            }
        }
    }
}

struct ReviewForm: View {
    @State private var stars = 0          // 这里才是数据真正的家

    var body: some View {
        VStack(spacing: 12) {
            StarRating(rating: $stars)    // 用 $ 把写权限借出去
            Text(stars == 0 ? "还没打分" : "你打了 \(stars) 分")
        }
        .padding()
    }
}

// 界面效果：点第 3 颗星，五颗星的前三颗变黄，下面文字显示"你打了 3 分"
```

`$stars` 里的 `$` 是"投影值"（projected value）。对一个属性包装器来说，`星号` 和 `$星号` 常常是两种东西：

| 写法 | 类型 | 含义 |
| --- | --- | --- |
| `stars` | `Int` | 当前的**值** |
| `$stars` | `Binding<Int>` | 一份**读写通道**（get + set 闭包） |

因为 `Binding` 本质是"一个读闭包 + 一个写闭包"，所以它可以重新拼装——这招在处理嵌套模型时非常有用：

```swift
import SwiftUI
import Observation

@Observable
final class Profile {
    var name = ""
    var age = 0
}

struct ProfileEditor: View {
    @State private var profile = Profile()

    var body: some View {
        Form {
            // 手写 Binding：读 profile.name，写回 profile.name
            TextField("名字", text: Binding(
                get: { profile.name },
                set: { profile.name = $0 }
            ))
            // 同理做一个"只能是偶数"的年龄输入
            TextField("年龄", value: Binding(
                get: { profile.age },
                set: { profile.age = $0 - $0 % 2 }
            ), format: .number)
            Text("当前：\(profile.name.isEmpty ? "匿名" : profile.name)，\(profile.age) 岁")
        }
    }
}

// 界面效果：输入 "Mia" 立刻显示在下方；
// 输入年龄 7，下方显示 6（set 里抹掉了奇数部分）
```

自定义 `Binding` 是 SwiftUI 里少数几个"必须手写闭包"的场合之一，它也被称为**派生绑定**：数据仍存在原处，只是把一次写入做了加工。

最后一个常用工具是 `.constant(...)`，它造一个"能读、写无效"的只读绑定，专门用来喂预览和演示代码：

```swift
import SwiftUI

// 预览里不需要真的保存状态
struct PreviewUsage: View {
    var body: some View {
        StarRating(rating: .constant(3))
    }
}
```

## 41.4 `@Observable`：跨视图共享的业务模型

`@State` 适合"一份数据只服务一块界面"。一旦数据要被多个页面读、要在跳转后仍然存在、要包含业务逻辑（请求、校验、缓存），就该把它搬进一个类，并让这个类可观察。

Swift 的观察机制由 `Observation` 模块提供，用法极小：

```swift
import Foundation
import Observation

@Observable
final class CartModel {
    private(set) var items: [String] = []

    var total: Int { items.count }
    var isEmpty: Bool { items.isEmpty }

    func add(_ item: String) { items.append(item) }
    func removeAll() { items.removeAll() }
}

let cart = CartModel()
cart.add("咖啡")
cart.add("可颂")
print(cart.total, cart.isEmpty)
// prints: 2 false

cart.removeAll()
print(cart.total, cart.isEmpty)
// prints: 0 true
```

真正的魔法在视图里：**`@Observable` 不需要你再写 `@ObservedObject`、`@StateObject`、`@EnvironmentObject`，视图只要在 `body` 里读了某个属性，就自动订阅那一个属性。**

```swift
import SwiftUI
import Observation

@Observable
final class CartModel {
    private(set) var items: [String] = []
    var total: Int { items.count }
    func add(_ item: String) { items.append(item) }
}

struct CartBadge: View {
    let cart: CartModel          // 普通 let，不需要任何包装器

    var body: some View {
        // 这个 body 只在 items 变化时重算；
        // 假如 CartModel 还有别的属性，改它们不会连累这里
        Text("\(cart.total) 件")
            .padding(6)
            .background(.tint, in: Capsule())
    }
}

struct ShopView: View {
    @State private var cart = CartModel()   // 拥有者用 @State 保管引用

    var body: some View {
        VStack(spacing: 16) {
            CartBadge(cart: cart)
            Button("加一瓶牛奶") { cart.add("牛奶") }
        }
        .padding()
    }
}

// 界面效果：每次点按钮，徽标上的数字加一
```

请对照上一段的 `PlainCounter` 例子看：同一个类，加上 `@Observable` 之前"改了不刷新"，加上之后"改了就刷新"。原因在于 `@Observable` 宏会把每个存储属性改写成"带 `access`/`withMutation` 通知的版本"，而 SwiftUI 的 `body` 求值过程会自动记录读了哪些属性。这个机制叫**依赖追踪**（observation tracking），和第 33 章的属性观察器完全不是一回事。

### 三件必须知道的事

**一、粒度是属性级的。** 视图只订阅它在 `body` 里真正读过的属性。`CartModel` 里如果有十个属性，`CartBadge` 只读 `items`（通过 `total`），那么改其他九个属性不会让徽标重算。这是 `@Observable` 相对老 `ObservableObject`（对象级通知）最大的性能改进。

**二、追踪只穿透被观察的类型。** 如果 `CartModel` 里塞了一个普通类，改那个普通类的属性不会触发通知：

```swift
import Observation

final class Session {          // 没有 @Observable
    var token = ""
}

@Observable
final class AppState {
    var session = Session()
}
```

改 `state.session.token` 不会让任何视图刷新。想让嵌套也生效，嵌套的类也得标 `@Observable`。

**三、`@Observable` 只对类有效。** 结构体不需要它——结构体是值类型，改了就是换了一个新值，天然是"变化"。这点和上一章"值语义"的话题接得上。

## 41.5 `@Bindable`：给可观察模型造绑定

`@Observable` 模型的属性要接给 `TextField` 这类需要 `Binding` 的控件时，中间的桥就是 `@Bindable`：

```swift
import SwiftUI
import Observation

@Observable
final class Profile {
    var name = ""
    var nickname = ""
}

struct ProfileForm: View {
    @Bindable var profile: Profile        // 注意：这里用 @Bindable 而不是 let

    var body: some View {
        Form {
            TextField("真名", text: $profile.name)   // 可以直接 $ 了
            TextField("昵称", text: $profile.nickname)
        }
    }
}
```

也可以在 `body` 内部就地造一个绑定，让"借用"的范围更小：

```swift
import SwiftUI
import Observation

@Observable
final class Profile { var name = "" }

struct LimitedScope: View {
    var profile: Profile

    var body: some View {
        @Bindable var profile = profile
        TextField("名字", text: $profile.name)
    }
}
```

`@Bindable var` 写在 `body` 里是合法写法（局部属性包装器），它表达的正是"我在这一小段代码里临时借用一下写权限"。

四种近似写法别记混：

| 你的需求 | 写法 |
| --- | --- |
| 视图自己造、自己用 | `@State private var profile = Profile()` |
| 只读展示模型、不改它 | `let profile: Profile` |
| 模型来自外部、但我要给它做双向绑定 | `@Bindable var profile: Profile` |
| 只要一个指向模型某个字段的绑定 | `@Bindable var profile: Profile` + `$profile.name` |

## 41.6 `@Environment`：看不见的传递通道

有三类东西不该一层层往下传：主题与外观、系统提供的服务（`dismiss`、`openURL`、`colorScheme`），以及全局共享模型。它们走环境。

```swift
import SwiftUI
import Observation

@Observable
final class ShoppingCart {
    var items: [String] = []
}

@main
struct ShopApp: App {
    @State private var cart = ShoppingCart()

    var body: some Scene {
        WindowGroup {
            ShopRoot()
                .environment(cart)          // 注入：往下一整棵树都能拿到
        }
    }
}

struct ShopRoot: View {
    var body: some View {
        NavigationStack {
            DetailView()                    // 中间不需要任何传递
        }
    }
}

struct DetailView: View {
    @Environment(ShoppingCart.self) private var cart   // 取出
    @Environment(\.dismiss) private var dismiss        // 系统提供的动作

    var body: some View {
        VStack {
            Button("加入购物车") { cart.items.append("商品") }
            Button("返回") { dismiss() }
        }
    }
}
```

系统自带的环境值很多，常用的几个：

| 环境值 | 类型 | 用途 |
| --- | --- | --- |
| `\.dismiss` | `DismissAction` | 关闭当前模态/返回 |
| `\.colorScheme` | `ColorScheme` | 当前是深色还是浅色 |
| `\.openURL` | `OpenURLAction` | 打开链接 |
| `\.dynamicTypeSize` | `DynamicTypeSize` | 用户设定的字号档位 |
| `\.locale` / `\.calendar` / `\.timeZone` | 本地化相关 | 日期与数字格式化 |
| `\.horizontalSizeClass` | `UserInterfaceSizeClass?` | 宽窄布局切换 |
| `\.isEnabled` | `Bool` | 上层是否禁用了交互 |

读一个系统环境值只写一行，那么"自己定义环境值"呢？传统做法要三件套（定义 `EnvironmentKey`、写扩展、读），现在有了 `@Entry` 这个宏，一行就够：

```swift
import SwiftUI

extension EnvironmentValues {
    @Entry var brandTint: Color = .blue
}

struct BrandedCard: View {
    @Environment(\.brandTint) private var tint

    var body: some View {
        Text("品牌色卡片")
            .padding()
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(tint))
    }
}

struct BrandedPage: View {
    var body: some View {
        BrandedCard()
            .environment(\.brandTint, .orange)   // 只影响这棵子树
    }
}

// 界面效果：卡片的描边用橙色；把这个 .environment 去掉就变回蓝色
```

`@Entry` 同样能用在 `Transaction`、`ContainerValues`、`FocusedValues` 上，是这几版最省事的一个宏。

⚠️ 环境值有个容易忽略的性质：**它是按子树生效的，查找方向是"向上最近的注入点"。** 所以同一份环境值在不同分支里可以不同，这也是做主题切换的常用手法。

## 41.7 老代码里一定会遇到的 `ObservableObject`

你迟早会打开一份 Swift 5 时代（或从网上抄来）的 SwiftUI 代码，看到这几样东西：

```swift
import SwiftUI

final class OldModel: ObservableObject {
    @Published var count = 0
}

struct OldView: View {
    @StateObject private var model = OldModel()   // 拥有
    @ObservedObject var other: OldModel           // 借用
    @EnvironmentObject var shared: OldModel       // 从环境取

    var body: some View {
        Text("\(model.count) \(other.count) \(shared.count)")
    }
}
```

它们和 `@Observable` 的对应关系如下：

| 旧（Swift 5 风格） | 新（观察机制） |
| --- | --- |
| `class X: ObservableObject` | `@Observable final class X` |
| `@Published var a` | `var a`（已经自动观察） |
| `@StateObject` | `@State` |
| `@ObservedObject` | 普通 `let` / `var` |
| `@EnvironmentObject` | `@Environment(X.self)` |
| `.environmentObject(x)` | `.environment(x)` |
| 对象一改，所有订阅视图重算 | 只重算读了那个属性的视图 |

新代码统一用右边这一列。左边这一列不用背，能读懂就行——判断标准很简单：看到属性包装器以外还带 `Published`、`Object` 字样的，八成是旧写法。

## 41.8 数据流只有两个方向

把所有东西合起来看，SwiftUI 的数据流其实只有两条规矩：

- **数据向下流**：父视图 → 子视图，通过参数（`let`）或绑定（`@Binding`）。
- **事件向上走**：子视图 → 父视图，通过闭包回调，或者直接改共享的 `@Observable` 模型。

```swift
import SwiftUI

struct Row: View {
    let title: String
    let onDelete: () -> Void        // 事件向上走：闭包

    var body: some View {
        HStack {
            Text(title)             // 数据向下流：参数
            Spacer()
            Button("删除", action: onDelete)
        }
    }
}

struct ParentView: View {
    @State private var rows = ["草稿", "已发布"]

    var body: some View {
        List(rows.indices, id: \.self) { i in
            Row(title: rows[i]) { rows.remove(at: i) }
        }
    }
}

// 界面效果：每行一个标题加一个删除按钮，点删除该行消失
```

如果一个视图既接绑定又发回调，通常说明它承担了两件事——这在小组件里没问题，但你可以问问自己：是不是该把"改动"收拢成一个动作？

### 选错了会怎样：三种典型症状

| 症状 | 病因 | 药方 |
| --- | --- | --- |
| 界面不刷新 | 数据存在普通类里，或者改的是副本 | 换成 `@Observable` 类，或改对那一份 |
| 输入框打字没反应 | 控件拿到的是只读值，不是 `Binding` | 传 `$state`，或用 `@Bindable` |
| 跳转回来数据全没了 | 状态放在了会被销毁的那一层 | 往上提一层，或注入到环境 |

## 41.9 本章小结

| 概念 | 一句话 | 什么时候用 |
| --- | --- | --- |
| `@State` | 视图私有、值类型或引用类型的持有者 | 只影响自己那块界面的状态 |
| `$` 投影 | 生成 `Binding` 读写通道 | 把写权限借给子视图或控件 |
| `@Binding` | 借来的读写引用，不拥有 | 可复用组件、子视图编辑父数据 |
| `@Observable` | 类级别的自动依赖追踪 | 跨页面共享、带业务逻辑的模型 |
| `@Bindable` | 给可观察模型造绑定 | 把模型字段接给 `TextField` 等 |
| `@Environment` | 按子树传递的隐式参数 | 主题、系统服务、全局模型 |
| `@Entry` | 一行声明自定义环境值 | 自己的主题、配置项 |
| 数据流 | 向下传值，向上传事件 | 判断一段代码该用参数还是闭包 |

## 41.10 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| 在 `init` 里写 `remaining = State(...)` | 必须写 `_remaining = State(initialValue:)`，那才是真正的存储属性 |
| 以为 `init` 传进来的初值会跟着外部变 | `@State` 只在第一次生效，之后外部变化它不理会 |
| 给普通类加 `@State` 就以为能刷新 | 需要 `@Observable`，否则改了不通知 |
| 用 `let model: Model` 却想改它的字段 | 引用类型可以改内容，值类型不行；要双向绑定就上 `@Bindable` |
| 嵌套的类没标 `@Observable`，却指望它触发刷新 | 追踪不穿透，嵌套类型也要可观察 |
| 把 `@Environment(Model.self)` 用在没注入的树上 | 运行时会崩，必须沿途 `.environment(model)` |
| 到处用 `@EnvironmentObject` / `@StateObject` | 那是旧 API，新代码用 `@Observable` 那一套 |
| 状态放太高，中间视图被迫层层传递 | 用 `@Environment`，或把状态下沉到真正需要的层 |
| 子视图拿到的是父视图状态的副本 | 传值改不动父视图；要 `@Binding` |

## 41.11 下章预告

数据有了家，接下来要给它安排住处：`HStack` 里的两个视图为什么宽度不一样？`Spacer()` 到底怎么"挤"？`frame(maxWidth: .infinity)` 为什么有时一点用没有？下一章讲 SwiftUI 的布局规则——它不是 CSS，而是"父视图提出方案，子视图给出答复"的谈判过程。
