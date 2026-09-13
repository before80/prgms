+++
title = "2 Kotlin 入门"
date = 2026-09-13T08:50:47+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://kotlinlang.org/docs/getting-started.html](https://kotlinlang.org/docs/getting-started.html)

# 2 Kotlin 入门

> 最新 Kotlin 版本：**[2.4.20](../whatsnewinkotlin/4.1-Whatsnew2420/)**

Kotlin 是一门现代语言，它简洁、支持多平台，并且能与 Java 及其他语言互操作。

刚接触 Kotlin？可以参加我们的导览，直接在浏览器中学习基础知识。

[开始 Kotlin 之旅](../takekotlintour/3.1-KotlinTourWelcome/)

## 安装 Kotlin {#install-kotlin}

Kotlin 随每个 [IntelliJ IDEA](https://www.jetbrains.com/idea/download/) 和 [Android Studio](https://developer.android.com/studio) 版本一起提供。下载并安装其中一个 IDE，即可开始使用 Kotlin。

## 选择你的 Kotlin 使用场景 {#choose-your-kotlin-use-case}

**控制台**

在这里，你将学习如何用 Kotlin 开发控制台应用并编写单元测试。

1. **[用 IntelliJ IDEA 项目向导创建一个基础的 JVM 应用](../compilerandplugins/12.1-Kotlincompiler/12.1.3-JvmGetStarted/)。**

2. **[编写你的第一个单元测试](../development/6.1-Backenddevelopment/6.1.3-JvmTestUsingJunit/)。**

**后端**

在这里，你将学习如何用 Kotlin 在服务端开发后端应用。

* **把 Kotlin 引入你的 Java 项目：**

* [配置 Java 项目以便与 Kotlin 协同工作](../development/6.1-Backenddevelopment/6.1.2-MixingJavaKotlinIntellij/)
* [为你的 Java Maven 项目添加 Kotlin 测试](../development/6.1-Backenddevelopment/6.1.3-JvmTestUsingJunit/)

* **用 Kotlin 从零开始创建后端应用：**

* [用 Spring Boot 创建 RESTful Web 服务](../development/6.1-Backenddevelopment/6.1.7-Createawebappwithkotlinandspringboot/6.1.7.1-JvmGetStartedSpringBoot/)
* [用 Ktor 创建 HTTP API](https://ktor.io/docs/creating-http-apis.html)

**跨平台**

在这里，你将学习如何用 [Kotlin Multiplatform](https://kotlinlang.org/docs/multiplatform/get-started.html) 开发跨平台应用。

1. **[为跨平台开发搭建环境](https://kotlinlang.org/docs/multiplatform/quickstart.html)。**

2. **创建你的第一个 iOS 和 Android 应用：**

* 从零开始创建一个跨平台应用，并且：
* [共享业务逻辑，同时保持原生界面](https://kotlinlang.org/docs/multiplatform/multiplatform-create-first-app.html)
* [共享业务逻辑与界面](https://kotlinlang.org/docs/multiplatform/compose-multiplatform-create-first-app.html)
* [让你现有的 Android 应用也能在 iOS 上运行](https://kotlinlang.org/docs/multiplatform/multiplatform-integrate-in-existing-app.html)
* [用 Ktor 和 SQLDelight 创建跨平台应用](https://kotlinlang.org/docs/multiplatform/multiplatform-ktor-sqldelight.html)

3. **浏览[示例项目](https://kotlinlang.org/docs/multiplatform/multiplatform-samples.html)**。

**Android**

要开始在 Android 开发中使用 Kotlin，请阅读 [Google 关于在 Android 上入门 Kotlin 的建议](https://developer.android.com/kotlin/get-started)。

**数据分析**

从构建数据管道到把机器学习模型投入生产，Kotlin 都是处理数据并充分利用数据的绝佳选择。

1. **探索并试验你的数据：**

* [DataFrame](https://kotlin.github.io/dataframe/overview.html) —— 一个用于数据分析和操作的库。
* [Kandy](https://kotlin.github.io/kandy/welcome.html) —— 一个用于数据可视化的绘图工具。

2. **在 Twitter 上关注 Kotlin for Data Analysis：** [KotlinForData](http://twitter.com/KotlinForData)。

## 获取支持 {#get-support}

如果你遇到任何困难或问题，可以在 ![Slack](./images/slack.svg) Slack 中寻求帮助：[获取邀请](https://surveys.jetbrains.com/s3/kotlin-slack-sign-up)，或者在我们的[问题跟踪器](https://youtrack.jetbrains.com/issues/KT)中报告问题。

如果本页有任何遗漏或令人困惑之处，请[分享你的反馈](https://surveys.hotjar.com/d82e82b0-00d9-44a7-b793-0611bf6189df)。
