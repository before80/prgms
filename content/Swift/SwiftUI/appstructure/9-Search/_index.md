+++
title = "9 搜索"
date = 2026-09-12T12:47:47+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/search](https://developer.apple.com/documentation/swiftui/search)

# 9 搜索

让人们可以在应用中搜索文本或其他内容。

## 概述 {#Overview}

要在应用中呈现搜索框，先为搜索文本、以及可选的离散搜索词（称为*令牌*，token）创建并管理存储。然后把该存储绑定到搜索框上：对应用中的某个视图应用 searchable 视图修饰符即可。

![](./images/search-hero@2x.png)

当人们与该输入框交互时，他们会隐式地修改底层存储，从而修改搜索参数。你的应用会相应地更新界面的其他部分。为增强搜索交互，你还可以：

- 在搜索过程中为文本和令牌提供建议。
- 实现搜索作用域，帮助人们缩小搜索范围。
- 检测人们何时激活搜索框，并使用环境值以编程方式关闭搜索框。

关于设计指导，参见 Human Interface Guidelines 中的[搜索](https://developer.apple.com/design/human-interface-guidelines/searching)。

## 搜索应用的数据模型 {#Searching-your-apps-data-model}

- [为应用添加搜索界面](9.1-AddingASearchInterfaceToYourApp/) —— 提供一个界面，让人们可以在应用中搜索内容。
- [执行搜索操作](9.2-PerformingASearchOperation/) —— 根据搜索文本以及你存储的可选令牌更新搜索结果。
- [searchable(text:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:placement:prompt:)) —— 把该视图标记为可搜索，这会配置搜索框的显示。
- [searchable(text:tokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:placement:prompt:token:)) —— 把该视图标记为可用文本和令牌搜索。
- [searchable(text:editableTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:placement:prompt:token:)) —— 把该视图标记为可搜索，这会配置搜索框的显示。
- [SearchFieldPlacement](https://developer.apple.com/documentation/swiftui/searchfieldplacement) —— 搜索框在视图层级中的放置位置。

## 提供搜索建议 {#Making-search-suggestions}

- [提供搜索词建议](9.3-SuggestingSearchTerms/) —— 向在应用中搜索内容的人提供建议。
- [searchSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:)) —— 配置该视图的搜索建议。
- [searchSuggestions(_:for:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:for:)) —— 配置在该视图中如何显示搜索建议。
- [searchCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/searchcompletion(_:)) —— 当该视图用作搜索建议时，把一个完整构成的字符串与它的值关联起来。
- [searchable(text:tokens:suggestedTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:placement:prompt:token:)) —— 把该视图标记为可用文本、令牌和建议搜索。
- [SearchSuggestionsPlacement](https://developer.apple.com/documentation/swiftui/searchsuggestionsplacement) —— SwiftUI 显示搜索建议的方式。

## 限制搜索范围 {#Limiting-search-scope}

- [限定搜索操作的范围](9.4-ScopingASearchOperation/) —— 把搜索空间划分为几个宽泛的类别。
- [searchScopes(_:scopes:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:scopes:)) —— 配置该视图的搜索作用域。
- [searchScopes(_:activation:_:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:activation:_:)) —— 用指定的激活策略配置该视图的搜索作用域。
- [SearchScopeActivation](https://developer.apple.com/documentation/swiftui/searchscopeactivation) —— searchable 修饰符显示或隐藏搜索作用域的方式。

## 检测、激活和关闭搜索 {#Detecting-activating-and-dismissing-search}

- [管理搜索界面的激活](9.5-ManagingSearchInterfaceActivation/) —— 以编程方式检测并关闭搜索框。
- [isSearching](https://developer.apple.com/documentation/swiftui/environmentvalues/issearching) —— 表示用户是否正在搜索的布尔值。
- [dismissSearch](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisssearch) —— 结束当前搜索交互的动作。
- [DismissSearchAction](https://developer.apple.com/documentation/swiftui/dismisssearchaction) —— 可以结束搜索交互的动作。
- [searchable(text:isPresented:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:ispresented:placement:prompt:)) —— 把该视图标记为可搜索，并可编程方式呈现搜索框。
- [searchable(text:tokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:ispresented:placement:prompt:token:)) —— 把该视图标记为可用文本和令牌搜索，并支持以编程方式呈现。
- [searchable(text:editableTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:ispresented:placement:prompt:token:)) —— 把该视图标记为可搜索，这会配置搜索框的显示。
- [searchable(text:tokens:suggestedTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:ispresented:placement:prompt:token:)) —— 把该视图标记为可用文本、令牌和建议搜索，并支持以编程方式呈现。

## 在搜索期间显示工具栏内容 {#Displaying-toolbar-content-during-search}

- [searchPresentationToolbarBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchpresentationtoolbarbehavior(_:)) —— 为在该视图内的任何 searchable 修饰符配置搜索工具栏的呈现行为。
- [SearchPresentationToolbarBehavior](https://developer.apple.com/documentation/swiftui/searchpresentationtoolbarbehavior) —— 定义呈现搜索时工具栏行为的类型。

## 在视图中搜索文本 {#Searching-for-text-in-a-view}

- [findNavigator(isPresented:)](https://developer.apple.com/documentation/swiftui/view/findnavigator(ispresented:)) —— 为文本编辑器视图以编程方式呈现查找与替换界面。
- [findDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/finddisabled(_:)) —— 阻止在文本编辑器中进行查找与替换操作。
- [replaceDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/replacedisabled(_:)) —— 阻止在文本编辑器中进行替换操作。
- [FindContext](https://developer.apple.com/documentation/swiftui/findcontext) —— 支持文本编辑的视图中查找导航器的状态。
