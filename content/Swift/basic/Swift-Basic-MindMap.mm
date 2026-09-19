<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="Swift 6.3 快速入门" FOLDED="false">
    <font NAME="SansSerif" SIZE="16" BOLD="true"/>

    <node TEXT="学习基线" POSITION="right">
      <node TEXT="语言版本：Swift 6.3.x（示例基准 6.3.3）"/>
      <node TEXT="语言模式：按 Swift 6 编写，迁移处说明差异"/>
      <node TEXT="源文件编码：只接受 UTF-8"/>
      <node TEXT="代码约定：结果写在同一代码块，用 // prints: 标注"/>
      <node TEXT="学习方式：先读文字，再跑代码，最后看小结与易错点"/>
    </node>

    <node TEXT="第一篇 起步（第 1–3 章）" POSITION="right">
      <node TEXT="第 1 章 装上 Swift 6.3，把第一行代码跑起来">
        <node TEXT="版本对齐：语言版本与工具链版本是两回事"/>
        <node TEXT="安装工具链：macOS / Linux / Windows"/>
        <node TEXT="四种把代码跑起来的方式"/>
        <node TEXT="第一个程序 hello.swift"/>
        <node TEXT="编译模式：留下真正的可执行文件"/>
        <node TEXT="语言模式：让编译器多管一点事"/>
      </node>
      <node TEXT="第 2 章 一段 Swift 源码的解剖">
        <node TEXT="源文件编码：UTF-8 是硬要求"/>
        <node TEXT="空白、分号与注释"/>
        <node TEXT="标识符：名字能取成什么样"/>
        <node TEXT="关键字：哪些词不能随便用"/>
        <node TEXT="字面量：源码里直接写出来的值"/>
        <node TEXT="特殊字面量：#file、#line 与它们的同伴"/>
        <node TEXT="#sourceLocation：正当地骗编译器"/>
        <node TEXT="#warning 与 #error：会说话的注释"/>
      </node>
      <node TEXT="第 3 章 SwiftPM 与第一个项目">
        <node TEXT="为什么需要包"/>
        <node TEXT="三十秒生成一个项目"/>
        <node TEXT="目录结构：约定大于配置"/>
        <node TEXT="Package.swift：用 Swift 写的说明书"/>
        <node TEXT="三件套命令：build / run / test"/>
        <node TEXT="程序入口：main.swift、@main 与顶层代码"/>
        <node TEXT="加一个依赖：三行清单，一行 import"/>
      </node>
    </node>

    <node TEXT="第二篇 语言主干（第 4–15、15B 章）" POSITION="right">
      <node TEXT="第 4 章 常量、变量与数值">
        <node TEXT="let 与 var：默认选 let"/>
        <node TEXT="类型推断与类型标注"/>
        <node TEXT="整数家族：默认用 Int"/>
        <node TEXT="浮点家族：默认用 Double；nan 与 isNaN"/>
        <node TEXT="没有隐式转换：Swift 最硬的一条规则"/>
        <node TEXT="溢出：选择崩掉，而不是回绕"/>
        <node TEXT="数字小工具：abs、min、max、isMultiple 等"/>
      </node>
      <node TEXT="第 5 章 字符串与字符">
        <node TEXT="Character 和 String 是两个类型"/>
        <node TEXT="count 数的不是字节"/>
        <node TEXT="为什么 str[0] 不合法"/>
        <node TEXT="切片是 Substring，不是 String"/>
        <node TEXT="常用操作速查"/>
        <node TEXT="比较：== 判的是用户眼中的相等"/>
      </node>
      <node TEXT="第 6 章 正则表达式">
        <node TEXT="默认姿势：#/.../#"/>
        <node TEXT="正则字面量也是有类型的"/>
        <node TEXT="三种匹配语义，别混着用"/>
        <node TEXT="捕获：位置与命名"/>
        <node TEXT="替换"/>
        <node TEXT="运行时生成的正则"/>
        <node TEXT="RegexBuilder：给看正则头疼的人"/>
        <node TEXT="什么时候不要用正则"/>
      </node>
      <node TEXT="第 7 章 运算符与表达式">
        <node TEXT="算术运算符"/>
        <node TEXT="比较运算符"/>
        <node TEXT="恒等运算符 === 与 !=="/>
        <node TEXT="逻辑运算符：会偷懒的短路求值"/>
        <node TEXT="位运算"/>
        <node TEXT="区间：... 与 ..&lt;"/>
        <node TEXT="三元运算符与空合运算符"/>
        <node TEXT="赋值与复合赋值"/>
        <node TEXT="优先级与结合性"/>
        <node TEXT="自定义运算符"/>
        <node TEXT="if 和 switch 也能当表达式"/>
      </node>
      <node TEXT="第 8 章 元组、类型别名与类型判断">
        <node TEXT="元组：把几个值放进同一个包裹"/>
        <node TEXT="解构与交换"/>
        <node TEXT="用元组返回多个结果"/>
        <node TEXT="元组的比较与限制"/>
        <node TEXT="类型别名 typealias"/>
        <node TEXT="类型判断：is、as? 与 as!"/>
      </node>
      <node TEXT="第 9 章 可选值">
        <node TEXT="nil 不是空对象，而是没有值"/>
        <node TEXT="读取可选值：先证明它存在"/>
        <node TEXT="guard let：提前退场，主干更清爽"/>
        <node TEXT="空合运算符：给缺席的值准备替补"/>
        <node TEXT="可选链：一路问号，一路安全"/>
        <node TEXT="map 与 flatMap：在盒子里做变换"/>
        <node TEXT="强制解包 ! 与隐式解包：能不用就别用"/>
        <node TEXT="嵌套可选与可选模式"/>
      </node>
      <node TEXT="第 10 章 集合">
        <node TEXT="Array：有顺序的列表"/>
        <node TEXT="Dictionary：用键找值"/>
        <node TEXT="Set：只关心有没有"/>
        <node TEXT="值语义：复制的是内容，不是地址"/>
        <node TEXT="遍历、筛选与变换"/>
      </node>
      <node TEXT="第 11 章 控制流（一）">
        <node TEXT="if：条件必须是 Bool"/>
        <node TEXT="if 也是表达式"/>
        <node TEXT="for-in：遍历是主旋律"/>
        <node TEXT="while 与 repeat-while"/>
        <node TEXT="break、continue 与标签"/>
        <node TEXT="where：给循环再加一道门槛"/>
        <node TEXT="defer：离开作用域前的收尾"/>
      </node>
      <node TEXT="第 12 章 控制流（二）：switch 与模式匹配">
        <node TEXT="基本形态：必须穷尽"/>
        <node TEXT="区间匹配"/>
        <node TEXT="值绑定与 where"/>
        <node TEXT="元组模式"/>
        <node TEXT="枚举关联值模式"/>
        <node TEXT="可选值模式"/>
        <node TEXT="类型转换模式：is 与 as"/>
        <node TEXT="表达式模式：~= 背后的魔法"/>
        <node TEXT="复合模式、fallthrough 与 @unknown default"/>
        <node TEXT="switch 表达式"/>
      </node>
      <node TEXT="第 13 章 函数">
        <node TEXT="定义与调用"/>
        <node TEXT="参数标签：让调用处说人话"/>
        <node TEXT="默认值、可变参数与 inout"/>
        <node TEXT="返回多个值和提前退出"/>
        <node TEXT="嵌套函数：把辅助逻辑关在门内"/>
        <node TEXT="函数类型：函数也是值"/>
        <node TEXT="@discardableResult 与重载"/>
        <node TEXT="参数模式与可变参数的小陷阱"/>
      </node>
      <node TEXT="第 14 章 闭包">
        <node TEXT="闭包表达式：从完整写法到极简写法"/>
        <node TEXT="尾随闭包：把代码块放到括号外面"/>
        <node TEXT="捕获：闭包会记住外面的变量"/>
        <node TEXT="捕获列表：把值固定下来"/>
        <node TEXT="逃逸与非逃逸"/>
        <node TEXT="自动闭包：把表达式变成惰性参数"/>
        <node TEXT="@Sendable 与并发"/>
      </node>
      <node TEXT="第 15 章 错误处理">
        <node TEXT="定义错误类型"/>
        <node TEXT="throw 与 throws"/>
        <node TEXT="分类捕获"/>
        <node TEXT="try? 与 try!"/>
        <node TEXT="defer：无论成败都收尾"/>
        <node TEXT="Result：把成功或失败当作值"/>
        <node TEXT="类型化抛出"/>
        <node TEXT="rethrows：把错误原样转交"/>
        <node TEXT="LocalizedError：给用户看的错误"/>
      </node>
      <node TEXT="第 15B 章 语法糖与特殊写法">
        <node TEXT="总原则：写法不同，语义相同"/>
        <node TEXT="类型的糖：[Int]、[K: V]、Int?"/>
        <node TEXT="字面量的糖：数字与字符串的各种写法"/>
        <node TEXT="省掉 return：单表达式就是答案"/>
        <node TEXT="函数的语法糖"/>
        <node TEXT="结构体的语法糖"/>
        <node TEXT="隐式 self：省略是常态，写出来是信号"/>
        <node TEXT="可选值的简写：把重复的名字去掉"/>
        <node TEXT="闭包与函数值的简写"/>
        <node TEXT="把运算符和键路径当值传"/>
        <node TEXT="模式匹配的简写：if case、for case 与 where"/>
        <node TEXT="表达式化的 if / switch"/>
        <node TEXT="隐式成员与 .init：省略类型名"/>
        <node TEXT="让自定义类型长出语法：callAsFunction、subscript、字面量协议"/>
        <node TEXT="自定义运算符与自定义字符串插值"/>
        <node TEXT="编译器替你写代码：自动合成与编译期字面量"/>
        <node TEXT="零碎但常见的写法"/>
        <node TEXT="结果构建器：@ViewBuilder 那一类块状糖"/>
      </node>
    </node>

    <node TEXT="第三篇 自定义类型与抽象（第 16–26 章）" POSITION="right">
      <node TEXT="第 16 章 枚举">
        <node TEXT="基本枚举与穷尽检查"/>
        <node TEXT="原始值：和底层值建立映射"/>
        <node TEXT="关联值：每个分支携带不同数据"/>
        <node TEXT="方法、计算属性与 mutating"/>
        <node TEXT="CaseIterable：遍历所有分支"/>
        <node TEXT="递归枚举：用 indirect 表达树"/>
        <node TEXT="实战：用枚举表达状态机"/>
        <node TEXT="可选值的真身"/>
      </node>
      <node TEXT="第 17 章 结构体与值语义">
        <node TEXT="定义与成员逐一初始化"/>
        <node TEXT="值语义：赋值得到新的一份"/>
        <node TEXT="mutating 方法：原地修改值"/>
        <node TEXT="常量结构体与可变属性的关系"/>
        <node TEXT="自定义初始化器"/>
        <node TEXT="嵌套的值语义"/>
        <node TEXT="结构体里放类的陷阱"/>
        <node TEXT="结构体适合什么"/>
      </node>
      <node TEXT="第 18 章 类与继承">
        <node TEXT="定义类与引用语义"/>
        <node TEXT="继承与方法重写"/>
        <node TEXT="super：调用父类实现"/>
        <node TEXT="final 与继承边界"/>
        <node TEXT="类的初始化与反初始化入口"/>
        <node TEXT="向上转换与向下转换"/>
        <node TEXT="类的身份、共享与生命周期"/>
        <node TEXT="什么时候用类"/>
      </node>
      <node TEXT="第 19 章 属性、方法与下标">
        <node TEXT="存储属性与计算属性"/>
        <node TEXT="属性观察器：变化前后插一脚"/>
        <node TEXT="lazy：第一次需要时才生成"/>
        <node TEXT="类型属性：属于类型本身"/>
        <node TEXT="实例方法、类型方法与 self"/>
        <node TEXT="下标：用方括号访问自定义容器"/>
        <node TEXT="属性包装器：把读写规则装进类型"/>
      </node>
      <node TEXT="第 20 章 初始化与反初始化">
        <node TEXT="初始化器与默认值"/>
        <node TEXT="结构体的初始化器委托"/>
        <node TEXT="类的指定初始化器与便利初始化器"/>
        <node TEXT="继承中的初始化规则"/>
        <node TEXT="两阶段初始化"/>
        <node TEXT="可失败初始化器"/>
        <node TEXT="required 初始化器"/>
        <node TEXT="反初始化 deinit：资源的最后一道门"/>
        <node TEXT="isolated deinit"/>
      </node>
      <node TEXT="第 21 章 扩展与嵌套类型">
        <node TEXT="扩展能添加什么"/>
        <node TEXT="用扩展组织协议实现"/>
        <node TEXT="用扩展补充初始化器"/>
        <node TEXT="条件扩展：满足条件才拥有能力"/>
        <node TEXT="扩展外部类型：别乱认亲戚"/>
        <node TEXT="嵌套类型：把相关名字收进命名空间"/>
        <node TEXT="扩展不是万能补丁"/>
      </node>
      <node TEXT="第 22 章 协议">
        <node TEXT="定义与遵循协议"/>
        <node TEXT="协议继承与组合"/>
        <node TEXT="类专用协议与弱引用委托"/>
        <node TEXT="默认实现：共享行为的捷径"/>
        <node TEXT="关联类型：协议里的占位类型"/>
        <node TEXT="some 与 any"/>
        <node TEXT="协议中的初始化器"/>
        <node TEXT="@resultBuilder：把语句拼成结果"/>
      </node>
      <node TEXT="第 23 章 泛型">
        <node TEXT="泛型函数"/>
        <node TEXT="泛型类型"/>
        <node TEXT="约束：把范围收窄到可操作的类型"/>
        <node TEXT="泛型下标与泛型方法"/>
        <node TEXT="关联类型与泛型的配合"/>
        <node TEXT="some 与 any 的选择"/>
        <node TEXT="值泛型与参数包"/>
        <node TEXT="类型化抛出与泛型"/>
      </node>
      <node TEXT="第 24 章 类型系统补全">
        <node TEXT="Any 与 AnyObject"/>
        <node TEXT="元类型：类型本身也是值"/>
        <node TEXT="Self：当前动态类型"/>
        <node TEXT="Never：没有正常返回"/>
        <node TEXT="键路径：把属性访问变成值"/>
        <node TEXT="callAsFunction：让实例像函数一样调用"/>
        <node TEXT="动态成员查找：点语法接住任意名字"/>
        <node TEXT="类型擦除：把具体类型藏进稳定的盒子"/>
        <node TEXT="Codable：把模型变成可传输的数据"/>
        <node TEXT="常用标准协议"/>
        <node TEXT="反射：Mirror"/>
        <node TEXT="自定义字面量"/>
      </node>
      <node TEXT="第 25 章 访问控制、模块与条件编译">
        <node TEXT="五级访问控制"/>
        <node TEXT="private、fileprivate 和扩展"/>
        <node TEXT="模块与包"/>
        <node TEXT="条件编译"/>
        <node TEXT="可用性检查"/>
        <node TEXT="模块选择器"/>
        <node TEXT="Objective-C 互操作标记"/>
        <node TEXT="导入的形式"/>
      </node>
      <node TEXT="第 26 章 宏">
        <node TEXT="宏是什么，不是什么"/>
        <node TEXT="自由宏：以 # 调用"/>
        <node TEXT="附着宏：贴在声明上的 @"/>
        <node TEXT="宏的实现依赖编译器插件"/>
        <node TEXT="亲手写一个最小宏"/>
        <node TEXT="宏的边界"/>
        <node TEXT="什么时候用宏"/>
      </node>
    </node>

    <node TEXT="第四篇 内存与并发（第 27–32 章）" POSITION="right">
      <node TEXT="第 27 章 值语义、写时复制与 ARC">
        <node TEXT="值语义与引用语义再对照"/>
        <node TEXT="写时复制：先共享，修改再分开"/>
        <node TEXT="自己实现一个 COW 盒子"/>
        <node TEXT="ARC：类实例的自动引用计数"/>
        <node TEXT="强引用、弱引用和无主引用预览"/>
        <node TEXT="引用计数的性能直觉"/>
      </node>
      <node TEXT="第 28 章 循环引用">
        <node TEXT="强引用环的形成"/>
        <node TEXT="weak：自动变 nil 的引用"/>
        <node TEXT="委托模式：弱引用最经典的舞台"/>
        <node TEXT="unowned：确定对方不会先走"/>
        <node TEXT="闭包捕获强引用"/>
        <node TEXT="异步任务里的 self"/>
      </node>
      <node TEXT="第 29 章 内存安全与所有权">
        <node TEXT="独占访问：同一时间只能有一个写手"/>
        <node TEXT="borrowing：只借不改"/>
        <node TEXT="consuming：把值交给函数"/>
        <node TEXT="~Copyable：不可复制类型"/>
        <node TEXT="consume 与 copy：在调用点控制值"/>
        <node TEXT="~Escapable 与 Span"/>
        <node TEXT="InlineArray：固定大小、避免堆分配"/>
        <node TEXT="所有权不是越新越要用"/>
      </node>
      <node TEXT="第 30 章 并发（一）：async/await 与结构化并发">
        <node TEXT="async 与 await"/>
        <node TEXT="async let：并行等待多个独立结果"/>
        <node TEXT="Task：从同步世界进入异步世界"/>
        <node TEXT="任务取消：协作式，不是强杀"/>
        <node TEXT="任务组：动态数量的结构化并发"/>
        <node TEXT="优先级与任务局部值"/>
        <node TEXT="续体：桥接回调和 async/await"/>
      </node>
      <node TEXT="第 31 章 并发（二）：隔离域、actor 与 Sendable">
        <node TEXT="数据竞争从哪里来"/>
        <node TEXT="actor：受隔离保护的状态"/>
        <node TEXT="@MainActor：UI 的主舞台"/>
        <node TEXT="Sendable：跨隔离域传递的安全凭证"/>
        <node TEXT="隔离检查失败的典型错误"/>
        <node TEXT="isolated 参数与 nonisolated"/>
        <node TEXT="actor 是可重入的"/>
        <node TEXT="AsyncSequence 与 for await"/>
      </node>
      <node TEXT="第 32 章 并发（三）：迁移与 Approachable Concurrency">
        <node TEXT="Swift 6 语言模式：严格并发检查"/>
        <node TEXT="默认隔离：让 UI 代码少写 @MainActor"/>
        <node TEXT="nonisolated(nonsending)：不隔离但留在调用者身边"/>
        <node TEXT="@concurrent：明确要求并发执行"/>
        <node TEXT="sending：把值的所有权安全送走"/>
        <node TEXT="迁移策略：从警告到错误"/>
        <node TEXT="数据竞争安全不是没有并发"/>
      </node>
    </node>

    <node TEXT="第五篇 工程与质量（第 33–35 章）" POSITION="right">
      <node TEXT="第 33 章 包与工程">
        <node TEXT="一个完整的包清单"/>
        <node TEXT="依赖与版本解析"/>
        <node TEXT="资源与本地化"/>
        <node TEXT="模块拆分"/>
        <node TEXT="C 互操作与系统库"/>
        <node TEXT="Swift Build 与构建产物"/>
        <node TEXT="延伸：Android 与跨平台"/>
      </node>
      <node TEXT="第 34 章 测试">
        <node TEXT="Swift Testing：@Test 与 #expect"/>
        <node TEXT="#require：先拿到必要条件"/>
        <node TEXT="测试抛错与异步代码"/>
        <node TEXT="参数化测试"/>
        <node TEXT="@Suite 与测试组织"/>
        <node TEXT="XCTest：现有项目的主力"/>
        <node TEXT="好测试的共同特征"/>
      </node>
      <node TEXT="第 35 章 调试与性能">
        <node TEXT="断言：让错误尽早出现"/>
        <node TEXT="编译期位置信息"/>
        <node TEXT="日志与 os.Logger"/>
        <node TEXT="断点与调试器"/>
        <node TEXT="计时与性能度量"/>
        <node TEXT="优化属性"/>
        <node TEXT="构建配置与性能"/>
      </node>
    </node>

    <node TEXT="第六篇 动手做（第 36–39 章）" POSITION="right">
      <node TEXT="第 36 章 命令行工具实战">
        <node TEXT="先把壳搭出来"/>
        <node TEXT="数据模型：一行都别多写"/>
        <node TEXT="存储层：把文件关在一个盒子里"/>
        <node TEXT="参数解析：把字符串变成命令"/>
        <node TEXT="主程序：把零件装起来"/>
        <node TEXT="退出码与输出流：UNIX 世界的礼貌"/>
        <node TEXT="可以继续升级的方向"/>
      </node>
      <node TEXT="第 37 章 SwiftUI 入门">
        <node TEXT="第一个视图，以及它周围的骨架"/>
        <node TEXT="@State：视图自己的小状态"/>
        <node TEXT="@Binding：让子视图修改父视图状态"/>
        <node TEXT="@Observable：现代状态模型"/>
        <node TEXT="旧式 ObservableObject 与 @StateObject"/>
        <node TEXT="列表、导航与异步任务"/>
        <node TEXT="状态应该放在哪里"/>
      </node>
      <node TEXT="第 38 章 综合实战：支出记录器">
        <node TEXT="需求与边界"/>
        <node TEXT="模型：只描述数据"/>
        <node TEXT="存储协议：先定接口，再定实现"/>
        <node TEXT="业务规则：服务层只做判断和聚合"/>
        <node TEXT="异步版本：当存储变成会慢的东西"/>
        <node TEXT="测试：把试过没问题变成证据"/>
        <node TEXT="如果今天就要接界面"/>
        <node TEXT="继续扩展"/>
      </node>
      <node TEXT="第 39 章 选读：服务端 Swift">
        <node TEXT="服务端 Swift 的组成"/>
        <node TEXT="一个最小路由"/>
        <node TEXT="请求与模型"/>
        <node TEXT="并发与共享状态"/>
        <node TEXT="配置与秘密"/>
        <node TEXT="测试与部署"/>
        <node TEXT="官方资料与延伸阅读"/>
      </node>
    </node>

    <node TEXT="第七篇 SwiftUI（第 40–47 章）" POSITION="right">
      <node TEXT="第 40 章 SwiftUI 的心智模型">
        <node TEXT="从摆控件到描述结果"/>
        <node TEXT="视图是结构体，不是屏幕上的控件"/>
        <node TEXT="body 每次都重新计算，为什么不用怕"/>
        <node TEXT="some View：为什么这个返回类型写不出来"/>
        <node TEXT="状态是唯一的事实来源"/>
        <node TEXT="视图的身份：为什么列表需要 id"/>
        <node TEXT="一个 App 的最小骨架"/>
      </node>
      <node TEXT="第 41 章 状态与数据流">
        <node TEXT="三个问题决定一切"/>
        <node TEXT="@State：视图自己的一块私房钱"/>
        <node TEXT="$ 与 @Binding：只借出写权限"/>
        <node TEXT="@Observable：跨视图共享的业务模型"/>
        <node TEXT="@Bindable：给可观察模型造绑定"/>
        <node TEXT="@Environment：看不见的传递通道"/>
        <node TEXT="老代码里一定会遇到的 ObservableObject"/>
        <node TEXT="数据流只有两个方向"/>
      </node>
      <node TEXT="第 42 章 布局与视图组合">
        <node TEXT="三条规则，一次谈判"/>
        <node TEXT="Stack：最简单的三种排列"/>
        <node TEXT="谁拿走剩余空间：Spacer 与 frame(maxWidth:)"/>
        <node TEXT="frame 的四层含义"/>
        <node TEXT="layoutPriority：谈判里的我先说"/>
        <node TEXT="GeometryReader：拿父视图给的真实尺寸"/>
        <node TEXT="Grid 与 Lazy 网格"/>
        <node TEXT="两种换布局：ViewThatFits 与 AnyLayout"/>
        <node TEXT="自定义 Layout：当 Stack 都不够用"/>
        <node TEXT="ViewModifier：给一串修饰符起个名字"/>
        <node TEXT="修饰符的顺序，就是包装的顺序"/>
        <node TEXT="组合：把大 body 拆成小视图"/>
      </node>
      <node TEXT="第 43 章 列表、导航与弹窗">
        <node TEXT="List 的三种写法"/>
        <node TEXT="身份：SwiftUI 里最贵的一课"/>
        <node TEXT="删除、移动、选择、刷新"/>
        <node TEXT="分区、搜索与分组"/>
        <node TEXT="NavigationStack：一条路径，一层页面"/>
        <node TEXT="弹窗家族：五种浮在上面的东西"/>
        <node TEXT="标题、工具栏与多标签"/>
        <node TEXT="一个可运行的多页面骨架"/>
      </node>
      <node TEXT="第 44 章 表单与用户输入">
        <node TEXT="Form：不是容器，是排版风格"/>
        <node TEXT="TextField 的三种取值方式"/>
        <node TEXT="多行文本：TextEditor 还是 TextField(axis:)"/>
        <node TEXT="密码框、键盘选项与提交行为"/>
        <node TEXT="选择类控件：Toggle / Picker / Slider / Stepper / DatePicker"/>
        <node TEXT="表单校验：三处地方，只有一个是对的"/>
        <node TEXT="一个完整的表单页面"/>
      </node>
      <node TEXT="第 45 章 动画与转场">
        <node TEXT="动画到底是什么：两个值之间的补间"/>
        <node TEXT="withAnimation 与 animation(_:value:)"/>
        <node TEXT="哪些属性能动画，哪些不能"/>
        <node TEXT="转场：视图进入和离开时的动画"/>
        <node TEXT="matchedGeometryEffect：让同一个东西在两处飞"/>
        <node TEXT="phaseAnimator 与 keyframeAnimator"/>
        <node TEXT="挑一个合适的动画曲线"/>
        <node TEXT="动画的两条纪律"/>
      </node>
      <node TEXT="第 46 章 异步、网络与生命周期">
        <node TEXT=".task 不是 onAppear 的异步版"/>
        <node TEXT=".task(id:)：值一变，旧任务自动取消"/>
        <node TEXT="三态建模：加载中 / 成功 / 失败"/>
        <node TEXT="并发请求：async let 与任务组"/>
        <node TEXT="网络请求：朴素但完整的一套"/>
        <node TEXT="从网络到界面：把零件接起来"/>
        <node TEXT="AsyncImage：三行显示远程图片"/>
      </node>
      <node TEXT="第 47 章 预览、测试、可访问性与发布">
        <node TEXT="#Preview：把改一行、等编译、点一下变成一秒钟"/>
        <node TEXT="让预览好用的是结构，不是预览本身"/>
        <node TEXT="SwiftUI 代码该测什么"/>
        <node TEXT="用 Swift Testing 写测试"/>
        <node TEXT="可访问性：不是加分项，是及格线"/>
        <node TEXT="发布前的清单"/>
      </node>
    </node>

    <node TEXT="第八篇 概念专题（第 48–52 章）" POSITION="right">
      <node TEXT="第 48 章 序列与集合协议">
        <node TEXT="三层协议一次说清：IteratorProtocol / Sequence / Collection"/>
        <node TEXT="自己写一个迭代器"/>
        <node TEXT="只遵循 Sequence：套用整套算法"/>
        <node TEXT="遵循 Collection：把下标能力交出去"/>
        <node TEXT="惰性求值：把算完再筛变成边算边筛"/>
        <node TEXT="无限序列与 AnySequence"/>
        <node TEXT="该遵循哪个协议"/>
      </node>
      <node TEXT="第 49 章 数值协议与格式化">
        <node TEXT="四个协议各管一件事"/>
        <node TEXT="用 Numeric 写对任何数字都成立的代码"/>
        <node TEXT="位宽与边界：整数独有的信息"/>
        <node TEXT="溢出：普通运算符会崩，和号系列会回绕"/>
        <node TEXT="浮点：FloatingPoint 保证的那些怪事"/>
        <node TEXT="Decimal：钱的正确容器"/>
        <node TEXT="格式化：FormatStyle 是唯一的正解"/>
        <node TEXT="带单位的数字：Measurement"/>
      </node>
      <node TEXT="第 50 章 属性与下标全形态">
        <node TEXT="属性家族全景：存储 / 计算 / 观察器 / lazy / 类型 / 包装器"/>
        <node TEXT="三条容易混的边界"/>
        <node TEXT="属性包装器：一个标注，三个成员 _x / x / $x"/>
        <node TEXT="下标家族全景：多参数、静态、安全版重载"/>
        <node TEXT="动态成员查找 @dynamicMemberLookup"/>
        <node TEXT="该选哪一种：决策表"/>
      </node>
      <node TEXT="第 51 章 标准库算法工具箱">
        <node TEXT="zip：配对，以短的为准"/>
        <node TEXT="stride：等差数列"/>
        <node TEXT="sequence(first:next:) 与 sequence(state:next:)"/>
        <node TEXT="repeatElement 与 enumerated"/>
        <node TEXT="reduce(into:)：累积到字典或数组"/>
        <node TEXT="Dictionary(grouping:by:)：一次分组"/>
        <node TEXT="查找与判定：first(where:)、allSatisfy、count(where:)"/>
        <node TEXT="切分与分块：prefix / suffix / split"/>
        <node TEXT="惰性管道：lazy 视图"/>
      </node>
      <node TEXT="第 52 章 反射与内存布局">
        <node TEXT="description 与 debugDescription"/>
        <node TEXT="LosslessStringConvertible：字符串还原成值"/>
        <node TEXT="Mirror：运行时看一眼结构"/>
        <node TEXT="superclassMirror：继承链逐层取"/>
        <node TEXT="CustomReflectable 与 dump"/>
        <node TEXT="MemoryLayout：size / stride / alignment"/>
        <node TEXT="填充字节与字段顺序"/>
        <node TEXT="offset(of:)：字段偏移"/>
        <node TEXT="withUnsafeBytes：看字节"/>
        <node TEXT="反射的边界：Swift 只读反射"/>
      </node>
    </node>

    <node TEXT="附录" POSITION="right">
      <node TEXT="附录A 语法地图：官方指南到章节"/>
      <node TEXT="附录B 标准库与 Foundation 的分界"/>
      <node TEXT="附录C @ 属性与 # 指令速查"/>
      <node TEXT="附录D 术语表（含中英对照）"/>
      <node TEXT="附录E 版本差异与易错点清单"/>
      <node TEXT="附录F 官方资料与延伸阅读"/>
      <node TEXT="复习顺序建议">
        <node TEXT="第 4、5、7、9、10 章：日常最常用的基础"/>
        <node TEXT="第 11–15、15B 章：控制流、函数、闭包、错误处理与语法糖"/>
        <node TEXT="第 16–23 章：自定义类型、协议、泛型"/>
        <node TEXT="第 27–32 章：内存与并发"/>
        <node TEXT="第 33–39 章：工程、测试、调试与实战"/>
        <node TEXT="第 48–52 章：概念专题，当字典查"/>
      </node>
    </node>

  </node>
</map>
