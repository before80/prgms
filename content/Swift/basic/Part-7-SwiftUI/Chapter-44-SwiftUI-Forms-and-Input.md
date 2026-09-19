+++
title = "第44章 表单与用户输入：把数据请进门"
weight = 440
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "Form 自动排版、TextField 的三种取值方式、各种输入控件、焦点管理与表单校验该放在哪"
isCJKLanguage = true
draft = false
+++

# 第四十四章：表单与用户输入：把数据请进门

> 前面所有章节的数据都是"你自己造的"。真实的 App 里，绝大部分数据是用户敲进去的——而用户会空着不填、写错格式、在密码框里粘贴表情符号。这一章把输入控件、焦点和校验一次讲完，顺便给出一个能直接抄的表单模型写法。

## 44.1 `Form`：不是容器，是"排版风格"

`Form` 在 iOS 上会渲染成系统的分组列表样式（灰底白卡片），在 macOS 上渲染成带标签栏的设置面板。它和 `VStack` 最大的区别是：**你几乎不用管排版。**

```swift
import SwiftUI

struct PreferencesForm: View {
    @State private var nickname = ""
    @State private var notifyByEmail = true
    @State private var theme = "跟随系统"

    var body: some View {
        Form {
            Section("个人资料") {
                TextField("昵称", text: $nickname)
                Toggle("邮件通知", isOn: $notifyByEmail)
            }
            Section {
                Picker("主题", selection: $theme) {
                    Text("跟随系统").tag("跟随系统")
                    Text("浅色").tag("浅色")
                    Text("深色").tag("深色")
                }
            } header: {
                Text("外观")
            } footer: {
                Text("深色模式会在系统切换时自动跟随。")
            }
        }
        .formStyle(.grouped)     // macOS 上更像设置面板；iOS 上可省略
    }
}

// 界面效果：两个分组。第一组两行；第二组是一行选择器，
// 上方分组标题，下方一句灰色说明文字
```

三个要点：

- `Section` 的 `header` / `footer` 用尾随闭包写在内容之后，顺序不能反。
- `.formStyle(.grouped)` 在 macOS 上把表单渲染成"设置面板"样式；不写会得到更紧凑的样式。iOS 上 `Form` 本身已经是分组样式。
- **`Form` 里的每一行只放一个主要控件**，系统会自动帮你排版并加分隔线。硬塞一个 `HStack` 塞三个控件，是把自己辛苦赚来的自动排版又还回去。

## 44.2 `TextField` 的三种取值方式

同一个 `TextField` 有三种"拿数据"的方式，选错了要么编译不过，要么悄悄引入 bug：

```swift
import SwiftUI

struct TextFieldKinds: View {
    @State private var text = ""          // 方式一：绑定字符串
    @State private var count = 0          // 方式二：绑定数值 + 格式

    var body: some View {
        Form {
            // 方式一：text
            TextField("评论", text: $text)

            // 方式二：value + format，控件负责解析与格式化
            TextField("数量", value: $count, format: .number)

            // 方式三：axis 让它在视觉上变多行，但依然是"单行字符串"
            TextField("备注", text: $text, axis: .vertical)
                .lineLimit(2...5)
        }
    }
}

// 界面效果：三个输入行；第三个会随文字增多自动长高，最多 5 行
```

| 写法 | 绑定类型 | 用户输入非法时 |
| --- | --- | --- |
| `text: $string` | `String` | 无所谓，什么都能存 |
| `value: $number, format:` | `Int` / `Double` / `Date` 等 | **不会写回绑定**，原值保持不变 |
| `text: $string, axis: .vertical` | 仍是 `String` | 无所谓，只是视觉上多行 |

方式二的"非法输入不写回"是个很贴心的默认行为：用户敲了 `abc` 时，`count` 还是原来的值，界面上那一格会显示成非法状态。想要"用户输什么我都接住再自己校验"，就用方式一。

日期和数字还能顺手加上格式：

```swift
import SwiftUI

struct FormattedInputs: View {
    @State private var price = 0.0
    @State private var deadline = Date()

    var body: some View {
        Form {
            TextField("价格", value: $price, format: .currency(code: "CNY"))
            TextField("截止日期", value: $deadline, format: .dateTime.year().month().day())
        }
    }
}
```

## 44.3 多行文本：`TextEditor` 还是 `TextField(axis:)`

要一段真正能写几百字、带滚动的文本域，用 `TextEditor`：

```swift
import SwiftUI

struct NoteEditor: View {
    @State private var body_ = ""

    var body: some View {
        TextEditor(text: $body_)
            .frame(minHeight: 160)
            .overlay(alignment: .topLeading) {
                // TextEditor 没有占位符，自己叠一个
                if body_.isEmpty {
                    Text("写点什么……")
                        .foregroundStyle(.tertiary)
                        .padding(.top, 8)
                        .padding(.leading, 5)
                        .allowsHitTesting(false)
                }
            }
            .padding()
    }
}

// 界面效果：一块可滚动的大文本框，空的时候显示灰色提示语
```

两者的选择标准很直接：

| 需求 | 用 |
| --- | --- |
| 一两行、要回车提交 | `TextField` |
| 两三行可以长高，但要随父布局伸缩 | `TextField(_, text:, axis: .vertical)` + `.lineLimit(_:)` |
| 一整块正文、内部自己滚动 | `TextEditor` |

⚠️ `TextEditor` 没有 `placeholder`，也没有 `.lineLimit` 语义，占位提示得自己叠；同时它默认有内边距偏移，所以上面用了 `.padding(.leading, 5)` 让提示语和文字对齐。这类"手工对齐"是 `TextEditor` 唯一的麻烦之处。

## 44.4 密码框、键盘选项与提交行为

```swift
import SwiftUI

struct LoginForm: View {
    enum Field: Hashable { case account, password }
    @FocusState private var focus: Field?
    @State private var account = ""
    @State private var password = ""
    @State private var submitted = false

    var body: some View {
        Form {
            TextField("账号", text: $account)
                .focused($focus, equals: .account)
                .submitLabel(.next)                     // 回车键显示"下一项"
                .onSubmit { focus = .password }         // 回车后跳到密码框

            SecureField("密码", text: $password)         // 输入内容显示为圆点
                .focused($focus, equals: .password)
                .submitLabel(.go)
                .onSubmit { submitted = true }
        }
        .onAppear { focus = .account }                   // 进入页面自动聚焦
        .alert("登录中…", isPresented: $submitted) { Button("好") { } }
    }
}

// 界面效果：打开页面光标在账号栏；回车跳到密码栏；
// 密码栏回车弹出提示
```

`@FocusState` 是表单里最值得早学的东西，它解决三个实际问题：

1. **回车依次跳转**：`.submitLabel` 决定回车键文字，`.onSubmit` 决定跳到哪。
2. **收起键盘**：把焦点设为 `nil`。
3. **滚动到出错项**：校验失败时把焦点挪到第一个不合格的输入框，用户立刻知道问题在哪。

平台差异提醒：`\.keyboardType`、`.textInputAutocapitalization`、`.autocorrectionDisabled` 这些修饰符**只在 iOS 系列平台可用**，在 macOS 上编译会报"没有这个成员"。跨平台项目要包条件编译，比如：

```swift
import SwiftUI

struct CrossPlatformField: View {
    @State private var email = ""

    var body: some View {
        TextField("邮箱", text: $email)
            #if os(iOS)
            .keyboardType(.emailAddress)
            .textInputAutocapitalization(.never)
            #endif
            .autocorrectionDisabled()      // 这个 macOS 也支持
    }
}
```

## 44.5 选择类控件：`Toggle` / `Picker` / `Slider` / `Stepper` / `DatePicker`

它们全都遵循同一个模式：**一个 `Binding` 管值，一个"怎么显示"的闭包管样子。** 值一律是 `Hashable` 的标签，不要手动去解析字符串。

```swift
import SwiftUI

enum Plan: String, CaseIterable, Identifiable {
    case free = "免费"
    case pro = "专业版"
    case team = "团队版"
    var id: Self { self }
}

struct ControlGallery: View {
    @State private var plan: Plan = .free
    @State private var enableLimit = false
    @State private var limit = 10.0
    @State private var guests = 2
    @State private var start = Date()
    @State private var segments = 1

    var body: some View {
        Form {
            // 1. 下拉/菜单式选择：值用枚举，天然避免拼错的字符串
            Picker("套餐", selection: $plan) {
                ForEach(Plan.allCases) { p in
                    Text(p.rawValue).tag(p)
                }
            }

            // 2. 分段控件：iOS/macOS 上都支持的紧凑多选一
            Picker("频率", selection: $segments) {
                Text("每天").tag(1)
                Text("每周").tag(7)
                Text("每月").tag(30)
            }
            .pickerStyle(.segmented)

            // 3. 开关 + 联动禁用
            Toggle("限制用量", isOn: $enableLimit)
            Slider(value: $limit, in: 1...100, step: 5) {
                Text("上限")
            } minimumValueLabel: {
                Text("1")
            } maximumValueLabel: {
                Text("100")
            }
            .disabled(!enableLimit)      // 关掉开关，滑块就变灰
            Text("当前上限：\(Int(limit))")

            // 4. 步进器：自带 +/-
            Stepper("访客人数：\(guests)", value: $guests, in: 1...20)

            // 5. 日期时间
            DatePicker("开始时间", selection: $start, displayedComponents: [.date, .hourAndMinute])
        }
    }
}

// 界面效果：五行控件；关掉"限制用量"后滑块变灰不可拖；
// 拖动滑块时下方文字同步显示 5 的倍数
```

⚠️ `Picker` 有一个经典报错：**"每个 tag 的类型必须和 selection 的类型一致"**。如果你写 `selection: $plan`（`Plan` 类型）却给 `Text("免费").tag("免费")`（`String`），标签就选不中——界面能显示，点击却没反应。要么统一成枚举，要么统一成字符串。

## 44.6 表单校验：三处地方，只有一个是对的

校验逻辑放哪，决定了这份表单是"好维护"还是"一改就炸"。三种做法摆一起看：

```swift
import SwiftUI

struct ValidationThreeWays: View {
    @State private var email = ""

    var body: some View {
        Form {
            // ❌ 做法一：在 body 里临时算，一旦要复用就得复制粘贴
            TextField("邮箱", text: $email)
            if !email.isEmpty && !email.contains("@") {
                Text("缺少 @").foregroundStyle(.red)
            }

            // ⚠️ 做法二：onChange 里算完存进另一个 @State，
            // 状态变多了两倍，容易出现"两份状态不一致"
            TextField("再次输入", text: $email)
                .onChange(of: email) { _, newValue in
                    _ = newValue.contains("@")
                }

            // ✅ 做法三：规则写在表单模型里，界面只负责显示
        }
    }
}
```

推荐做法三——把校验写成模型上的**计算属性**：

```swift
import SwiftUI
import Observation

@Observable
final class SignupForm {
    var email = ""
    var password = ""
    var acceptedTerms = false

    var emailError: String? {
        guard !email.isEmpty else { return nil }        // 还没填就不报错
        return email.contains("@") ? nil : "邮箱格式看起来不对"
    }

    var passwordError: String? {
        guard !password.isEmpty else { return nil }
        return password.count >= 8 ? nil : "密码至少 8 位"
    }

    var isValid: Bool {
        emailError == nil && passwordError == nil
            && !email.isEmpty && acceptedTerms
    }
}

struct SignupView: View {
    @State private var form = SignupForm()

    var body: some View {
        @Bindable var form = form
        Form {
            Section("账号") {
                TextField("邮箱", text: $form.email)
                if let error = form.emailError {
                    Text(error).font(.caption).foregroundStyle(.red)
                }
                SecureField("密码（至少 8 位）", text: $form.password)
                if let error = form.passwordError {
                    Text(error).font(.caption).foregroundStyle(.red)
                }
            }
            Section {
                Toggle("我已阅读并同意条款", isOn: $form.acceptedTerms)
                Button("注册") { }
                    .disabled(!form.isValid)
            }
        }
    }
}

// 界面效果：输入 "abc" 时邮箱栏下方出现红字；
// 三个条件都满足前，"注册"按钮一直是灰的
```

这种写法有三个好处，值得逐条对照：

1. **规则只有一份**，界面和测试读的都是 `form.isValid`；
2. **错误信息是算出来的**，不存在"改了值忘了清错误"的可能；
3. 想给"点了提交之后才高亮错误"这种更细的体验，只要在模型上加一个 `var didAttemptSubmit = false`，错误显示条件改成 `didAttemptSubmit ? emailError : nil` 即可，界面一行都不用动。

## 44.7 一个完整的表单页面

```swift
import SwiftUI
import Observation

struct Expense: Hashable {
    var title: String
    var amount: Double
    var date: Date
    var category: String
}

@Observable
final class ExpenseForm {
    var title = ""
    var amountText = ""
    var date = Date()
    var category = "餐饮"

    static let categories = ["餐饮", "交通", "购物", "其他"]

    var amount: Double? { Double(amountText) }

    var titleError: String? {
        title.isEmpty ? "请填写名称" : (title.count > 20 ? "名称最多 20 个字" : nil)
    }

    var amountError: String? {
        guard !amountText.isEmpty else { return "请填写金额" }
        guard let amount else { return "金额必须是数字" }
        return amount > 0 ? nil : "金额要大于 0"
    }

    var isValid: Bool { titleError == nil && amountError == nil }

    func makeExpense() -> Expense? {
        guard let amount, isValid else { return nil }
        return Expense(title: title, amount: amount, date: date, category: category)
    }
}

struct ExpenseEditor: View {
    @State private var form = ExpenseForm()
    @Environment(\.dismiss) private var dismiss
    var onSave: (Expense) -> Void

    var body: some View {
        @Bindable var form = form
        NavigationStack {
            Form {
                Section("基本信息") {
                    TextField("名称", text: $form.title)
                    if let message = form.titleError, !form.title.isEmpty {
                        Text(message).font(.caption).foregroundStyle(.red)
                    }
                    TextField("金额", text: $form.amountText)
                    if let message = form.amountError, !form.amountText.isEmpty {
                        Text(message).font(.caption).foregroundStyle(.red)
                    }
                    DatePicker("日期", selection: $form.date, displayedComponents: .date)
                }
                Section("分类") {
                    Picker("分类", selection: $form.category) {
                        ForEach(ExpenseForm.categories, id: \.self) { Text($0).tag($0) }
                    }
                    .pickerStyle(.segmented)
                }
            }
            .navigationTitle("记一笔")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("取消") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("保存") {
                        if let expense = form.makeExpense() {
                            onSave(expense)
                            dismiss()
                        }
                    }
                    .disabled(!form.isValid)
                }
            }
        }
        .frame(minWidth: 320, minHeight: 320)
    }
}

// 界面效果：一个"记一笔"表单；名称为空或金额不是正数时，
// 对应栏下方出现红色提示，"保存"按钮保持灰色不可点
```

注意 `makeExpense()` 返回的是可选值：**表单模型负责"能不能转成有效数据"，界面的保存按钮只负责调用。** 这个分工让"按钮禁用"和"实际保存条件"用的是同一套判断，不会出现"按钮亮了但保存失败"的不一致。

## 44.8 本章小结

| 概念 | 一句话 |
| --- | --- |
| `Form` / `Section` | 系统排版的分组表单；一行一个主控件 |
| `TextField(text:)` | 绑字符串，什么输入都接受 |
| `TextField(value:format:)` | 绑数值/日期，解析失败不写回 |
| `TextField(axis: .vertical)` | 视觉多行但仍是单行字符串 |
| `TextEditor` | 大块多行文本，需自己加占位符 |
| `SecureField` | 密码输入，显示圆点 |
| `@FocusState` | 控制焦点：自动聚焦、回车跳转、收起键盘 |
| `Picker` | 值的 tag 类型必须与 selection 一致 |
| `Toggle` / `Slider` / `Stepper` / `DatePicker` | 统一模式：`Binding` 管值，闭包管显示 |
| 校验 | 写成模型的计算属性，界面只读 `error` / `isValid` |
| 保存 | 模型提供"生成有效数据"的方法，按钮只负责调用 |

## 44.9 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| `Picker` 点了没反应 | `tag` 的类型和 `selection` 不一致，二者必须同类型 |
| 用 `value:` 绑定却想接住任意输入 | 解析失败不会写回；要"什么都收"就用 `text:` |
| 在 `body` 里写 `if 不合法 { 显示 }` 的复杂规则 | 规则会到处复制；提到模型的计算属性里 |
| 用 `onChange` 把校验结果另存一份状态 | 两份状态容易不同步，直接算出来 |
| `TextEditor` 里期待占位符 | 它没有；用 `.overlay` 自己叠一个并关掉命中测试 |
| 忘了 `.allowsHitTesting(false)` | 占位文字会挡住点击，光标点不进去 |
| 在 macOS 上用 `.keyboardType` / `.textInputAutocapitalization` | 这些是 iOS 专属，要条件编译 |
| 编辑表单直接改主数据 | 用草稿模型，"取消"才不需要回滚逻辑 |
| sheet 太窄 | 给 `.frame(minWidth:minHeight:)` |

## 44.10 下章预告

表单让界面"能用了"，但还不好看——准确地说是没有"说清楚发生了什么"。下一章讲动画：`withAnimation` 和 `.animation` 的区别、转场、`matchedGeometryEffect` 和新的 `phaseAnimator`，以及那条最实用的原则——动画只该用来解释变化，不该用来炫耀。
