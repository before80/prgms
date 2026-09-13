+++
title = "5 文本输入与输出"
date = 2026-09-12T12:47:47+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/text-input-and-output](https://developer.apple.com/documentation/swiftui/text-input-and-output)

# 5 文本输入与输出

显示格式化文本，并获取用户输入的文本。

## 概述 {#Overview}

要显示只读文本，或显示与图像配对的只读文本，分别使用内置的 [Text](https://developer.apple.com/documentation/swiftui/text) 或 [Label](https://developer.apple.com/documentation/swiftui/label) 视图。当需要收集用户输入的文本时，使用合适的文本输入视图，例如 [TextField](https://developer.apple.com/documentation/swiftui/textfield) 或 [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor)。

![](./images/text-input-and-output-hero@2x.png)

你可以添加视图修饰符来控制文本的字体、可否选择、对齐方式、布局方向等。即使你没有显式定义 [Text](https://developer.apple.com/documentation/swiftui/text) 视图，这些修饰符也会影响其他显示文本的视图，例如控件上的标签。

关于设计指导，请参阅 Human Interface Guidelines 中的 [排版](https://developer.apple.com/design/human-interface-guidelines/typography)。

## 显示文本 {#Displaying-text}

- [Text](https://developer.apple.com/documentation/swiftui/text) — 一种显示一行或多行只读文本的视图。
- [Label](https://developer.apple.com/documentation/swiftui/label) — 用于用户界面项目的标准标签，由一个图标和一个标题组成。
- [labelStyle(_:)](https://developer.apple.com/documentation/swiftui/view/labelstyle(_:)) — 设置该视图内标签的样式。

## 获取文本输入 {#Getting-text-input}

- [构建丰富的 SwiftUI 文本体验](5.1-BuildingRichSwiftuiTextExperiences/) — 使用 SwiftUI 文本编辑器视图和属性字符串，构建用于格式化文本的编辑器。
- [TextField](https://developer.apple.com/documentation/swiftui/textfield) — 一种显示可编辑文本界面的控件。
- [textFieldStyle(_:)](https://developer.apple.com/documentation/swiftui/view/textfieldstyle(_:)) — 设置该视图内文本输入框的样式。
- [SecureField](https://developer.apple.com/documentation/swiftui/securefield) — 一种让用户安全输入私密文本的控件。
- [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor) — 一种可以显示并编辑长文本的视图。

## 选择文本 {#Selecting-text}

- [textSelection(_:)](https://developer.apple.com/documentation/swiftui/view/textselection(_:)) — 控制人们是否可以在该视图中选择文本。
- [TextSelectability](https://developer.apple.com/documentation/swiftui/textselectability) — 描述选择文本能力的类型。
- [TextSelection](https://developer.apple.com/documentation/swiftui/textselection) — 表示一段被选中的文本。
- [textSelectionAffinity(_:)](https://developer.apple.com/documentation/swiftui/view/textselectionaffinity(_:)) — 设置选区或光标相对于某个文本字符的方向。
- [textSelectionAffinity](https://developer.apple.com/documentation/swiftui/environmentvalues/textselectionaffinity) — 选区或光标相对于某个文本字符的方向或关联关系的表示。在处理双向文本（同时包含从左到右和从右到左文字系统的文本，例如英文与阿拉伯文混排）时，这个概念会变得重要得多。
- [TextSelectionAffinity](https://developer.apple.com/documentation/swiftui/textselectionaffinity) — 选区或光标相对于某个文本字符的方向或关联关系的表示。在处理双向文本（同时包含从左到右和从右到左文字系统的文本，例如英文与阿拉伯文混排）时，这个概念会变得重要得多。
- [AttributedTextSelection](https://developer.apple.com/documentation/swiftui/attributedtextselection) — 表示一段被选中的属性文本。

## 设置字体 {#Setting-a-font}

- [为文本应用自定义字体](5.3-ApplyingCustomFontsToText/) — 在应用中加入并使用一种可以随动态字体大小缩放的字体。
- [font(_:)](https://developer.apple.com/documentation/swiftui/view/font(_:)) — 设置该视图中文本的默认字体。
- [fontDesign(_:)](https://developer.apple.com/documentation/swiftui/view/fontdesign(_:)) — 设置该视图中文本的字体设计。
- [fontWeight(_:)](https://developer.apple.com/documentation/swiftui/view/fontweight(_:)) — 设置该视图中文本的字体粗细。
- [fontWidth(_:)](https://developer.apple.com/documentation/swiftui/view/fontwidth(_:)) — 设置该视图中文本的字体宽度。
- [font](https://developer.apple.com/documentation/swiftui/environmentvalues/font) — 该环境的默认字体。
- [Font](https://developer.apple.com/documentation/swiftui/font) — 一种依赖环境的字体。

## 调整文字大小 {#Adjusting-text-size}

- [textScale(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/textscale(_:isenabled:)) — 对视图中的文本应用文字缩放。
- [dynamicTypeSize(_:)](https://developer.apple.com/documentation/swiftui/view/dynamictypesize(_:)) — 把视图内的动态字体大小设置为给定值。
- [dynamicTypeSize](https://developer.apple.com/documentation/swiftui/environmentvalues/dynamictypesize) — 当前的动态字体大小。
- [DynamicTypeSize](https://developer.apple.com/documentation/swiftui/dynamictypesize) — 一种动态字体大小，指定可缩放内容应有多大。
- [ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric) — 一种动态属性，用于缩放数值。
- [TextVariantPreference](https://developer.apple.com/documentation/swiftui/textvariantpreference) — 用于控制文本视图大小变体的协议。
- [FixedTextVariant](https://developer.apple.com/documentation/swiftui/fixedtextvariant) — 默认的文本变体偏好，选择可用的最大变体。
- [SizeDependentTextVariant](https://developer.apple.com/documentation/swiftui/sizedependenttextvariant) — 这种依赖大小的变体偏好允许文本在选择要显示的变体时把可用空间考虑在内。

## 控制文本样式 {#Controlling-text-style}

- [bold(_:)](https://developer.apple.com/documentation/swiftui/view/bold(_:)) — 为该视图中的文本应用粗体字重。
- [italic(_:)](https://developer.apple.com/documentation/swiftui/view/italic(_:)) — 为该视图中的文本应用斜体。
- [underline(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/underline(_:pattern:color:)) — 为该视图中的文本应用下划线。
- [strikethrough(_:pattern:color:)](https://developer.apple.com/documentation/swiftui/view/strikethrough(_:pattern:color:)) — 为该视图中的文本应用删除线。
- [textCase(_:)](https://developer.apple.com/documentation/swiftui/view/textcase(_:)) — 设置该视图所含文本在显示时的大小写转换方式。
- [textCase](https://developer.apple.com/documentation/swiftui/environmentvalues/textcase) — 一种样式覆盖，在显示时使用环境的语言区域转换 `Text` 的大小写。
- [monospaced(_:)](https://developer.apple.com/documentation/swiftui/view/monospaced(_:)) — 在可能的情况下，把所有子视图的字体改为当前字体的等宽变体。
- [monospacedDigit()](https://developer.apple.com/documentation/swiftui/view/monospaceddigit()) — 在可能的情况下，把所有子视图的字体改为使用等宽数字，同时让其他字符保持比例间距。
- [AttributedTextFormattingDefinition](https://developer.apple.com/documentation/swiftui/attributedtextformattingdefinition) — 用于定义视图中文本可以如何设置样式的协议。
- [AttributedTextValueConstraint](https://developer.apple.com/documentation/swiftui/attributedtextvalueconstraint) — 用于定义某个属性取值约束的协议。
- [AttributedTextFormatting](https://developer.apple.com/documentation/swiftui/attributedtextformatting) — 与属性文本格式化定义相关的类型的命名空间。

## 管理文本布局 {#Managing-text-layout}

- [truncationMode(_:)](https://developer.apple.com/documentation/swiftui/view/truncationmode(_:)) — 设置太长、无法放入可用空间的文本行的截断模式。
- [truncationMode](https://developer.apple.com/documentation/swiftui/environmentvalues/truncationmode) — 一个值，指示布局如何截断最后一行文本以放入可用空间。
- [allowsTightening(_:)](https://developer.apple.com/documentation/swiftui/view/allowstightening(_:)) — 设置该视图中的文本在需要把文本放入一行时是否可以压缩字符之间的间距。
- [allowsTightening](https://developer.apple.com/documentation/swiftui/environmentvalues/allowstightening) — 一个布尔值，指示是否应收缩字符间距以把文本放入可用空间。
- [minimumScaleFactor(_:)](https://developer.apple.com/documentation/swiftui/view/minimumscalefactor(_:)) — 设置该视图中文本为放入可用空间而缩小到的下限。
- [minimumScaleFactor](https://developer.apple.com/documentation/swiftui/environmentvalues/minimumscalefactor) — 为把文本放入可用空间而缩小字号时允许的最小比例。
- [baselineOffset(_:)](https://developer.apple.com/documentation/swiftui/view/baselineoffset(_:)) — 设置该视图中文本相对于其基线的垂直偏移量。
- [kerning(_:)](https://developer.apple.com/documentation/swiftui/view/kerning(_:)) — 设置该视图中文本字符之间的间距（即字距）。
- [tracking(_:)](https://developer.apple.com/documentation/swiftui/view/tracking(_:)) — 设置该视图中文本的字距调整。
- [flipsForRightToLeftLayoutDirection(_:)](https://developer.apple.com/documentation/swiftui/view/flipsforrighttoleftlayoutdirection(_:)) — 设置当布局方向为从右到左时，该视图是否水平镜像其内容。
- [TextAlignment](https://developer.apple.com/documentation/swiftui/textalignment) — 文本沿水平轴的对齐位置。

## 渲染文本 {#Rendering-text}

- [用 SwiftUI 创建视觉效果](5.4-CreatingVisualEffectsWithSwiftui/) — 使用着色器和文本渲染器添加滚动效果、丰富的颜色处理、自定义过渡以及高级效果。
- [TextAttribute](https://developer.apple.com/documentation/swiftui/textattribute) — 一种可以附加到文本视图上、并可被文本渲染器查询的值。
- [textRenderer(_:)](https://developer.apple.com/documentation/swiftui/view/textrenderer(_:)) — 返回一个新视图，使其中的任何文本视图都使用 `renderer` 来绘制自身。
- [TextRenderer](https://developer.apple.com/documentation/swiftui/textrenderer) — 一种可以替换文本视图默认渲染行为的值。
- [TextProxy](https://developer.apple.com/documentation/swiftui/textproxy) — 供自定义文本渲染器使用的文本视图代理。

## 限制多行文本的行数 {#Limiting-line-count-for-multiline-text}

- [lineLimit(_:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:)) — 把文本在该视图中可以占用的行数设置为一个闭区间。
- [lineLimit(_:reservesSpace:)](https://developer.apple.com/documentation/swiftui/view/linelimit(_:reservesspace:)) — 设置文本在该视图中可以占用的行数上限。
- [lineLimit](https://developer.apple.com/documentation/swiftui/environmentvalues/linelimit) — 文本在视图中可以占用的最大行数。

## 设置多行文本格式 {#Formatting-multiline-text}

- [lineSpacing(_:)](https://developer.apple.com/documentation/swiftui/view/linespacing(_:)) — 设置该视图中文本行之间的间距。
- [lineSpacing](https://developer.apple.com/documentation/swiftui/environmentvalues/linespacing) — 一行文本的底部与下一行文本的顶部之间以点为单位表示的距离。
- [multilineTextAlignment(_:)](https://developer.apple.com/documentation/swiftui/view/multilinetextalignment(_:)) — 设置包含多行文本的文本视图的对齐方式。
- [multilineTextAlignment](https://developer.apple.com/documentation/swiftui/environmentvalues/multilinetextalignment) — 一个环境值，指示当内容发生换行或包含换行符时文本视图如何对齐其各行。

## 格式化日期与时间 {#Formatting-date-and-time}

- [SystemFormatStyle](https://developer.apple.com/documentation/swiftui/systemformatstyle) — 一组格式样式，用于在文本视图中显示实时更新的时间信息。
- [TimeDataSource](https://developer.apple.com/documentation/swiftui/timedatasource) — 与时间相关的数据来源。

## 管理文本输入 {#Managing-text-entry}

- [autocorrectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/autocorrectiondisabled(_:)) — 设置是否对该视图停用自动更正。
- [autocorrectionDisabled](https://developer.apple.com/documentation/swiftui/environmentvalues/autocorrectiondisabled) — 一个布尔值，决定视图层级是否启用了自动更正。
- [keyboardType(_:)](https://developer.apple.com/documentation/swiftui/view/keyboardtype(_:)) — 设置该视图的键盘类型。
- [scrollDismissesKeyboard(_:)](https://developer.apple.com/documentation/swiftui/view/scrolldismisseskeyboard(_:)) — 配置可滚动内容与软件键盘交互的行为。
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)) — 设置该视图的文本内容类型，当用户在 macOS 上输入文本时，系统用它来提供建议。
- [textInputAutocapitalization(_:)](https://developer.apple.com/documentation/swiftui/view/textinputautocapitalization(_:)) — 设置键盘上的 Shift 键自动启用的频率。
- [TextInputAutocapitalization](https://developer.apple.com/documentation/swiftui/textinputautocapitalization) — 文本输入期间应用的大写自动转换行为的种类。
- [textInputBorderShape(_:)](https://developer.apple.com/documentation/swiftui/view/textinputbordershape(_:)) — 设置视图层级中文本输入控件的边框形状。
- [TextInputBorderShape](https://developer.apple.com/documentation/swiftui/textinputbordershape) — 用于绘制文本输入控件边框的形状。
- [textInputCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/textinputcompletion(_:)) — 当该视图用作文本输入建议时，把一个完整成形的字符串与其值关联起来。
- [textInputSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:)) — 配置该视图的文本输入建议。
- [textInputSuggestions(_:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:content:)) — 配置该视图的文本输入建议。
- [textInputSuggestions(_:id:content:)](https://developer.apple.com/documentation/swiftui/view/textinputsuggestions(_:id:content:)) — 配置该视图的文本输入建议。
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-4dqqb) — 设置该视图的文本内容类型，当用户在 watchOS 设备上输入文本时，系统用它来提供建议。
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-6fic1) — 设置该视图的文本内容类型，当用户在 macOS 上输入文本时，系统用它来提供建议。
- [textContentType(_:)](https://developer.apple.com/documentation/swiftui/view/textcontenttype(_:)-ufdv) — 设置该视图的文本内容类型，当用户在 iOS 或 tvOS 设备上输入文本时，系统用它来提供建议。
- [textInputFormattingControlVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/textinputformattingcontrolvisibility(_:for:)) — 指定人们可以使用哪些系统文本格式化控件来设置文本格式。
- [TextInputFormattingControlPlacement](https://developer.apple.com/documentation/swiftui/textinputformattingcontrolplacement) — 一种结构体，定义每个平台上可用的系统文本格式化控件。

## 听写文本 {#Dictating-text}

- [searchDictationBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchdictationbehavior(_:)) — 配置由 searchable 修饰符所配置的任何搜索框的听写行为。
- [TextInputDictationActivation](https://developer.apple.com/documentation/swiftui/textinputdictationactivation)
- [TextInputDictationBehavior](https://developer.apple.com/documentation/swiftui/textinputdictationbehavior)

## 配置写作工具行为 {#Configuring-the-Writing-Tools-behavior}

- [writingToolsBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsbehavior(_:)) — 指定环境中文本与文本输入的写作工具行为。
- [WritingToolsBehavior](https://developer.apple.com/documentation/swiftui/writingtoolsbehavior) — 文本与文本输入的写作工具编辑体验。
- [writingToolsAffordanceVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/writingtoolsaffordancevisibility(_:)) — 指定系统是否应为受该环境影响的文本输入视图显示写作工具提示。

## 指定文本等价项 {#Specifying-text-equivalents}

- [typeSelectEquivalent(_:)](https://developer.apple.com/documentation/swiftui/view/typeselectequivalent(_:)) — 在集合（例如列表或表格）中设置显式的键入选择等价文本。

## 本地化文本 {#Localizing-text}

- [为本地化准备视图](5.5-PreparingViewsForLocalization/) — 指定提示信息并添加字符串，从而本地化你的 SwiftUI 视图。
- [LocalizedStringKey](https://developer.apple.com/documentation/swiftui/localizedstringkey) — 用于在 strings 文件或 strings 字典文件中查找条目的键。
- [locale](https://developer.apple.com/documentation/swiftui/environmentvalues/locale) — 视图应使用的当前语言区域。
- [typesettingLanguage(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/typesettinglanguage(_:isenabled:)) — 指定排版所用的语言。
- [TypesettingLanguage](https://developer.apple.com/documentation/swiftui/typesettinglanguage) — 定义文本的排版语言如何确定。

## 已弃用的类型 {#Deprecated-types}

- [ContentSizeCategory](https://developer.apple.com/documentation/swiftui/contentsizecategory) — 你可以为内容指定的各种尺寸。
