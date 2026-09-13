+++
title = "4 持久化存储"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/persistent-storage](https://developer.apple.com/documentation/swiftui/persistent-storage)

# 4 持久化存储

存储数据，供应用多次会话之间使用。

## 概述 {#Overview}

操作系统提供了在应用关闭时存储数据的方式，这样人们下次打开应用时就能不中断地继续之前的工作。具体使用哪种机制，取决于你需要存储什么、要存多少、是否需要顺序访问或随机访问等等。

![](./images/persistent-storage-hero@2x.png)

在 SwiftUI 应用中使用的存储方式，与其他任何应用相同。例如，你可以用 [FileManager](https://developer.apple.com/documentation/foundation/filemanager) 接口访问磁盘上的文件。不过，SwiftUI 也提供了一些便利，让某些类型的持久化存储在声明式环境中更易使用。例如，你可以用 [FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest) 和 [FetchedResults](https://developer.apple.com/documentation/swiftui/fetchedresults) 与 Core Data 模型交互。

## 在应用多次启动之间保存状态 {#Saving-state-across-app-launches}

- [用 SwiftUI 恢复应用状态](4.1-RestoringYourAppSStateWithSwiftui/) —— 保留用户当前的活动，为使用者提供应用连续性。
- [defaultAppStorage(_:)](https://developer.apple.com/documentation/swiftui/view/defaultappstorage(_:)) —— 该视图内 `AppStorage` 使用的默认存储。
- [AppStorage](https://developer.apple.com/documentation/swiftui/appstorage) —— 反映 `UserDefaults` 中的值、并在该用户默认值变化时使视图失效的属性包装器类型。
- [SceneStorage](https://developer.apple.com/documentation/swiftui/scenestorage) —— 读写持久化的、按场景存储的数据的属性包装器类型。

## 访问 Core Data {#Accessing-Core-Data}

- [加载并显示大型数据源](4.2-LoadingAndDisplayingALargeDataFeed/) —— 在后台消费数据，并通过批量导入和防止重复记录来降低内存占用。
- [managedObjectContext](https://developer.apple.com/documentation/swiftui/environmentvalues/managedobjectcontext)
- [FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest) —— 从 Core Data 持久化存储中获取实体的属性包装器类型。
- [FetchedResults](https://developer.apple.com/documentation/swiftui/fetchedresults) —— 从 Core Data 存储中获取的结果集合。
- [SectionedFetchRequest](https://developer.apple.com/documentation/swiftui/sectionedfetchrequest) —— 从 Core Data 持久化存储中获取实体并按分区归组的属性包装器类型。
- [SectionedFetchResults](https://developer.apple.com/documentation/swiftui/sectionedfetchresults) —— 从 Core Data 持久化存储中获取并按分区归组的结果集合。
