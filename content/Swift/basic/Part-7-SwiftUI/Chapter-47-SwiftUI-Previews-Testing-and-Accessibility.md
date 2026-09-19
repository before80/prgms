+++
title = "第47章 预览、测试、可访问性与发布"
weight = 470
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "#Preview 的实用写法、SwiftUI 代码怎么测、可访问性清单，以及上架前该过一遍的检查项"
isCJKLanguage = true
draft = false
+++

# 第四十七章：预览、测试、可访问性与发布

> 前面八章教你"把界面写出来"。这一章解决最后那段最容易偷懒的路：**写完到交付之间。** 预览让你不用每次跑起来才能看一眼；测试把"我点一遍好像没问题"变成可重复的证据；可访问性决定你的界面能被多少人用；发布清单决定它能不能顺利进商店。四件事都不难，只是不做就会一直疼。

## 47.1 `#Preview`：把"改一行、等编译、点一下"变成一秒钟

预览是 SwiftUI 开发体验里最值钱的东西。它有一个宏形态 `#Preview`，写完立刻能在 Xcode 右侧看到界面：

```swift
import SwiftUI

struct Badge: View {
    let text: String
    var highlighted = false

    var body: some View {
        Text(text)
            .font(.caption.bold())
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(highlighted ? AnyShapeStyle(.tint) : AnyShapeStyle(.quaternary), in: Capsule())
    }
}

#Preview("普通") {
    Badge(text: "草稿")
}

#Preview("高亮") {
    Badge(text: "已发布", highlighted: true)
}

// 界面效果：右侧预览里并排显示两个胶囊标签，第二个用主题色填充
```

真正让预览好用起来的，是下面这几种写法：

```swift
import SwiftUI

struct ProfileCard: View {
    var name: String
    var body: some View {
        VStack(alignment: .leading) {
            Text(name).font(.headline)
            Text("这是说明文字").foregroundStyle(.secondary)
        }
        .padding()
    }
}

#Preview("紧凑尺寸", traits: .sizeThatFitsLayout) {
    ProfileCard(name: "Mia")
}

#Preview("深色模式") {
    ProfileCard(name: "Mia")
        .preferredColorScheme(.dark)
}

#Preview("超大字号（辅助功能）") {
    ProfileCard(name: "Mia")
        .environment(\.dynamicTypeSize, .accessibility3)
}

#Preview("固定画布") {
    ProfileCard(name: "Mia")
        .frame(width: 320, height: 200)
        .background(.background)
}

// 界面效果：Xcode 的预览选择器里出现四个入口，
// 分别展示紧凑高度、深色、超大字号和固定尺寸下的样子
```

预览里也需要状态时，用 `@Previewable` 就地声明，不必为此专门造一个包装视图：

```swift
import SwiftUI

#Preview("可编辑预览") {
    @Previewable @State var text = "在这里改文字"

    VStack {
        TextField("输入", text: $text)
        Text("长度：\(text.count)")
    }
    .padding()
}

// 界面效果：预览里直接可以打字，下面实时显示字数
```

⚠️ 两个关于预览的"基本功"：

- **预览崩了不等于代码崩了。** 预览是最容易受缓存影响的工具，遇到莫名其妙的失败先按 `⌘⇧K` 清一次；还是不行再怀疑代码。
- **`#Preview` 里的代码不参与正式构建。** 它是编译期被剥离的，所以里面可以随便写假数据、`fatalError`，不用有心理负担。

## 47.2 让预览好用的是"结构"，不是预览本身

预览卡住的时间，通常不是预览的问题，而是视图**没法被单独构造**：

```swift
import SwiftUI
import Observation

@Observable
final class FeedModel {
    var items: [String] = []
    func load() async { items = ["从网络来的数据"] }
}

// ❌ 视图自己造模型、自己发请求
// 预览一打开就真的去请求网络，只能看到转圈
struct BadFeed: View {
    @State private var model = FeedModel()
    var body: some View {
        List(model.items, id: \.self) { Text($0) }
            .task { await model.load() }
    }
}

// ✅ 数据从外部传进来，谁来构造由调用方决定
struct GoodFeed: View {
    let items: [String]
    var body: some View {
        List(items, id: \.self) { Text($0) }
    }
}

#Preview("有数据") {
    GoodFeed(items: ["第一条", "第二条"])
}

#Preview("空状态") {
    GoodFeed(items: [])
}

// 界面效果：两个预览分别显示两行列表和一块空白列表
```

所以"方便预览"的写法其实和"方便测试"的写法是同一件事：**视图拿数据、不造数据。** 造数据的工作交给上层（真实运行时是模型，预览和测试时是假数据）。

同一条思路也能用在自己写的模型上：给模型留一个"测试用"的初始化方式，或者干脆定义一份假数据集合：

```swift
import SwiftUI

/// 仅供预览与测试使用的示例数据
let sampleItems = ["写周报", "约会议室", "买咖啡豆"]

#Preview("示例数据") {
    List(sampleItems, id: \.self) { Text($0) }
}
```

## 47.3 SwiftUI 代码该测什么

先接受一个现实：**视图的像素不需要你来测**（那是 Xcode 预览和快照工具的活）。真正值得自动化测试的是三样东西：

1. **模型的状态转换**：点一下"开始"之后状态是不是从 `idle` 变成 `running`；
2. **从状态到展示文案的映射**：空列表该显示什么、错误该显示什么；
3. **从表单到有效数据的转换**：校验规则、格式化。

这三样都能在不启动界面的情况下测，速度以毫秒计。做法是把它们从视图中抽出来，例如把第 44 章那个表单校验抽成独立的可测对象：

```swift
import Foundation

struct SignupValidator {
    func emailError(_ email: String) -> String? {
        guard !email.isEmpty else { return nil }
        return email.contains("@") ? nil : "邮箱格式看起来不对"
    }

    func passwordError(_ password: String) -> String? {
        guard !password.isEmpty else { return nil }
        return password.count >= 8 ? nil : "密码至少 8 位"
    }

    func canSubmit(email: String, password: String, accepted: Bool) -> Bool {
        !email.isEmpty && email.contains("@")
            && password.count >= 8 && accepted
    }
}
```

这样的类型没有任何 SwiftUI 依赖，不需要模拟器，随手就能测。**"把逻辑搬到能被测试的地方"这件事本身，就是 SwiftUI 项目里最重要的架构决策之一。**

## 47.4 用 Swift Testing 写测试

Swift 官方的新测试框架用 `@Test` 和 `#expect`，写法比 XCTest 更接近自然语言：

```swift
import Testing

struct SignupValidator {
    func emailError(_ email: String) -> String? {
        guard !email.isEmpty else { return nil }
        return email.contains("@") ? nil : "邮箱格式看起来不对"
    }

    func canSubmit(email: String, password: String, accepted: Bool) -> Bool {
        !email.isEmpty && email.contains("@") && password.count >= 8 && accepted
    }
}

@Test func 邮箱缺少at时报错() {
    let validator = SignupValidator()
    #expect(validator.emailError("mia.example.com") == "邮箱格式看起来不对")
}

@Test func 邮箱为空时不报错() {
    #expect(SignupValidator().emailError("") == nil)
}

@Test("提交条件", arguments: [
    ("mia@example.com", "12345678", true, true),    // 全部满足
    ("mia@example.com", "12345678", false, false),  // 没同意条款
    ("mia@example.com", "1234", true, false),       // 密码太短
    ("", "12345678", true, false),                  // 邮箱为空
])
func 提交条件按预期判断(email: String, password: String, accepted: Bool, expected: Bool) {
    #expect(SignupValidator().canSubmit(email: email, password: password, accepted: accepted) == expected)
}
```

要点只有几个：

| 你会用到的 | 作用 |
| --- | --- |
| `@Test func 名字()` | 声明一个测试；函数名可以直接写中文 |
| `#expect(条件)` | 断言；失败时打印表达式两侧的实际值 |
| `@Test(arguments:)` | 参数化测试，一份逻辑跑多组数据 |
| `#require(可选值)` | 解包并断言非空，失败即结束该测试 |
| `withKnownIssue { }` | 标记已知问题，不阻塞流水线 |
| `@Suite` | 把相关测试归为一组 |

**XCTest 还值得学吗？** 需要。UI 自动化测试（`XCUIApplication`）目前仍然是 XCTest 的领域；而且大量现有项目用的是 `XCTestCase`。三者的选择可以这样记：

| 测试类型 | 推荐 |
| --- | --- |
| 纯逻辑、模型、工具函数 | Swift Testing（`@Test`） |
| 需要操作真实界面的端到端测试 | XCTest + `XCUIApplication` |
| 老项目里已有的测试 | 保持 XCTest，新测试用 Swift Testing，两者可以在同一目标里共存 |

在 SwiftPM 项目里，测试放在 `Tests/` 目录下，`swift test` 一次跑完；在 Xcode 应用项目里，测试目标里 `import Testing` 即可。

### 测异步与状态变化

视图模型是异步的，测试也得是异步的——`@Test` 函数直接写 `async`：

```swift
import Foundation
import Testing
import Observation

struct Article: Identifiable, Hashable {
    let id: Int
    let title: String
}

enum LoadState<Value>: Equatable where Value: Equatable {
    case idle, loading
    case loaded(Value)
    case failed(String)
}

@Observable
final class FeedModel {
    var state: LoadState<[Article]> = .idle
    private let loader: @Sendable () async throws -> [Article]

    init(loader: @escaping @Sendable () async throws -> [Article]) {
        self.loader = loader
    }

    func load() async {
        state = .loading
        do {
            state = .loaded(try await loader())
        } catch {
            state = .failed(error.localizedDescription)
        }
    }
}

@Test func 加载成功后状态变成loaded() async {
    let model = FeedModel { [Article(id: 1, title: "A")] }
    await model.load()
    #expect(model.state == .loaded([Article(id: 1, title: "A")]))
}

@Test func 加载失败后状态变成failed() async {
    struct Boom: Error { }
    let model = FeedModel { throw Boom() }
    await model.load()
    if case .failed = model.state {
        // 符合预期
    } else {
        Issue.record("期望失败状态，实际是 \(model.state)")
    }
}
```

注意 `FeedModel` 的初始化器接收一个**闭包**当作数据来源。这就是"依赖注入"最轻量的形态：正式运行时注入真实的网络请求，测试时注入一行假数据或一个错误。这样测试不碰网络，稳定且飞快。

## 47.5 可访问性：不是加分项，是及格线

界面上有一半信息（图标、颜色、布局位置）在"看不见屏幕"的用户那里会全部消失。SwiftUI 的可访问性 API 大部分是**免费的**（`Text`、`Button` 自带标签），你只需要补上它猜不出来的部分：

```swift
import SwiftUI

struct CartRow: View {
    let name: String
    let price: Int
    @State private var quantity = 1

    var body: some View {
        HStack {
            // 图标本身没有语义，必须给标签
            Image(systemName: "cart")
                .accessibilityLabel("购物车")

            Text(name)

            Spacer()

            // 两个分离的文字在语音里会被读成两段，合并成一条更自然
            HStack(spacing: 4) {
                Text("小计")
                Text("¥\(price * quantity)")
            }
            .accessibilityElement(children: .combine)

            Stepper(
                "数量",
                value: $quantity,
                in: 1...99
            )

            // 纯装饰元素要藏起来，否则语音会读一堆废话
            Rectangle()
                .fill(.quaternary)
                .frame(width: 1)
                .accessibilityHidden(true)
        }
        .padding(.vertical, 4)
    }
}

// 界面效果：一行购物车条目：图标 + 名称 + 小计 + 数量加减；
// 打开旁白后会被读成"购物车，拿铁，小计 38 元，数量，1"
```

常用修饰符速查：

| 修饰符 | 用在哪 |
| --- | --- |
| `.accessibilityLabel("…")` | 图标按钮、只有颜色没有文字的控件 |
| `.accessibilityHint("…")` | 说明"做了会发生什么"，别重复标签内容 |
| `.accessibilityValue("…")` | 滑块、进度、"3 之 5"这类当前值 |
| `.accessibilityElement(children: .combine)` | 把一组小控件合成一个语音条目 |
| `.accessibilityElement(children: .ignore)` | 完全自己描述这一块 |
| `.accessibilityHidden(true)` | 纯装饰元素，不参与朗读 |
| `.accessibilityIdentifier("…")` | 给 UI 测试用的稳定标识（用户看不见） |
| `.accessibilitySortPriority(_:)` | 调整朗读顺序 |

还有两件和可访问性强相关、又常常被忽略的事：

```swift
import SwiftUI

struct DynamicTypeSafe: View {
    @Environment(\.dynamicTypeSize) private var typeSize

    var body: some View {
        // 1. 用系统的语义字号（.title/.body/.caption），不要写死 .system(size: 14)
        // 字号随用户设置放大时，布局要能跟着变
        let layout = typeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading, spacing: 8))
            : AnyLayout(HStackLayout(spacing: 12))

        layout {
            Text("标题").font(.headline)
            Text("说明").font(.body)
        }
        .padding()
        // 2. 颜色对比不足时，用 .primary/.secondary 这类语义色，
        // 而不是自己调一个看起来很淡的灰色
    }
}

// 界面效果：正常字号时标题与说明左右排列；
// 把系统字号调到最大，自动改为上下排列，文字不再被挤成三角形
```

一句话总结这一节：**能不能用系统语义（语义字号、语义颜色、语义图标），决定你的界面在"别人的设置"下崩不崩。**

## 47.6 发布前的清单

代码写完之后，还有一列和代码无关但会卡住你的事。列成清单，逐条打勾：

**工程配置**

- 应用图标（macOS 还需要 `AppIcon.appiconset` 的多尺寸）、启动后的首屏不空白；
- `Info.plist` 里声明会用到的权限描述（相机、定位、相册），没有描述却调用权限会直接崩溃（iOS）；
- macOS 应用如需联网，要打开沙盒的 `com.apple.security.network.client` entitlements；
- 版本号与构建号（`CFBundleShortVersionString` / `CFBundleVersion`）每次提交都要递增。

**功能与体验**

- 所有网络请求在无网络时给出可理解的提示，而不是转圈到永远；
- 所有表单在键盘弹出、超大字号、深色模式下都不遮挡关键按钮；
- 用旁白过一遍主流程（这一步的收获往往比跑一遍 UI 测试还大）；
- 处理"返回/关闭"路径：任何弹窗都要能退出。

**发布流程**

- 归档（Product → Archive），走一遍真实签名；
- 上传到 App Store Connect，用 TestFlight 装到真机上点一遍；
- iOS 应用提交时准备好截图与隐私说明；macOS 应用如要分发到商店之外，还需要公证（notarization）。

清单里最容易漏掉的是"深色模式"和"超大字号"两项——它们在开发机上通常默认不打开，所以一定要手动切一遍。

## 47.7 本章小结

| 概念 | 一句话 |
| --- | --- |
| `#Preview` | 宏形态的预览；可命名、可指定布局特性、可切深色与字号 |
| `@Previewable` | 在预览里就地声明状态，不需要造包装视图 |
| 可预览的结构 | 视图拿数据、不造数据；依赖注入让预览和测试同时受益 |
| 该测什么 | 状态转换、展示映射、表单校验——不测像素 |
| Swift Testing | `@Test` + `#expect` + 参数化；`async` 测试直接写 |
| XCTest 的位置 | UI 自动化测试仍然用它；老项目里两者可以共存 |
| 依赖注入 | 用闭包当数据来源，测试时注入假数据 |
| 可访问性 | 图标要标签、组合要合并、装饰要隐藏、字号要语义 |
| 动态字体 | 用语义字号 + `dynamicTypeSize` 驱动的换布局 |
| 发布清单 | 图标、权限描述、沙盒、版本号、深色与超大字号、归档与 TestFlight |

## 47.8 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| 视图内部自己创建模型并请求网络 | 预览和测试都会被网络拖住；数据从外部传入 |
| 预览失败就认定代码坏了 | 先清预览缓存（⌘⇧K），再查代码 |
| 花大力气测视图的像素 | 预览/快照工具更合适；自动化测试盯逻辑 |
| 测试直接打真实网络 | 用闭包注入假数据；测试要快、要稳、要离线可跑 |
| 图标按钮不给 `accessibilityLabel` | 旁白只会读成"按钮"，用户不知道点它干什么 |
| 装饰性图形不隐藏 | 旁白里全是无意义内容；`.accessibilityHidden(true)` |
| 字号写死 `.system(size:)` | 用户放大字号时布局崩；用 `.body`/`.headline`/`.caption` |
| 只测浅色模式 | 深色模式和超大字号是高频翻车区，发布前手动过一遍 |
| 版本号忘了递增 | 上传会被拒；归档前检查 `CFBundleVersion` |
| macOS 应用忘了联网权限 | 沙盒下请求全部失败，且报错信息不通俗 |

## 47.9 第七篇收尾

回头看这八章，其实只在练一件能力：**把"界面"看成"状态的函数"。**

- 第 40 章给了心智模型：视图是值，状态是源头；
- 第 41 章回答了"状态放哪"；
- 第 42 章讲了状态变成布局的规则；
- 第 43、44 章处理数据的进出；
- 第 45 章让变化被看懂；
- 第 46 章把真实数据接进来；
- 第 47 章保证它可用、可测、可交付。

接下来最好的练习不是继续读，而是找一个你自己每天在用的 App，用这套结构把它的一两个页面复刻出来。写的过程中，你会重新遇到这篇里所有的坑——那时它们就不再是知识点了，而是你的经验。

（SwiftUI 每年都会跟着系统更新一批 API。遇到不确定的写法，优先查官方文档与当年的 What's New 说明，而不是几年前的技术博客。）
