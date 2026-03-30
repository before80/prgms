+++
title = "第36章 Maven 与 Gradle——项目构建工具"
weight = 360
date = "2026-03-30T14:33:56.920+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十六章 Maven 与 Gradle——项目构建工具

> "写代码一时爽，依赖地狱火葬场。"——每个被 JAR 包折磨过的 Java 程序员

各位好，欢迎来到 Java 世界中两个最"卷"的工具——**Maven** 和 **Gradle** 的主场。

话说有一天，小明写了一个 Java 程序，兴奋地编译运行，结果报错：`NoClassDefFoundError`。小明懵了：我明明写了这个类啊！旁边老程序员拍了拍他的肩膀："欢迎来到依赖管理地狱，年轻人。"

这就是为什么我们需要 **构建工具（Build Tool）**。它们就像是 Java 项目的大管家，帮我们处理依赖管理、编译打包、自动化测试、发布部署这些脏活累活。没有它们，一个稍微大点的项目光配置依赖就能让你怀疑人生。

本章我们就来聊聊 Java 生态中两代最具代表性的构建工具——Maven 和 Gradle。

---

## 36.1 Maven

### 36.1.1 Maven 的前世今生

**Maven** 是 Apache 软件基金会的开源项目，最早诞生于 2004 年左右。它的名字很有意思——中文意思是"专家"或"内行"，而它的 Logo 是一只可爱的海狸（ Beaver）。为什么是海狸？因为海狸是"建筑大师"，擅长筑坝，这正好隐喻 Maven 在项目中扮演的"构建者"角色。

Maven 的核心贡献是引入了 **项目对象模型（Project Object Model，简称 POM）** 的概念。简单来说，你只需要在一个 `pom.xml` 文件里声明"我需要什么依赖"、"我要怎么编译"，Maven 就会自动帮你搞定一切。

### 36.1.2 Maven 的核心概念

在学习 Maven 之前，我们需要理解几个核心概念：

- **POM（Project Object Model）**：项目对象模型，就是那个 `pom.xml` 文件。它是 Maven 工作的核心配置文件，定义了项目的基本信息、依赖、插件、构建配置等。
- **坐标（Coordinates）**：Maven 用 `groupId`、`artifactId`、`version` 三个坐标来唯一标识一个构件（artifact）。就像 GPS 坐标能精确定位地球上的任意位置一样，Maven 坐标能精确定位仓库中的任意 JAR 包。
- **仓库（Repository）**：存储 JAR 包和其他构建产物的地方。包括本地仓库（在你电脑的 `.m2` 目录下）和远程仓库（最著名的是 Maven Central）。
- **依赖传递（Transitive Dependencies）**：你依赖的库可能又依赖其他库，Maven 会自动把这些传递依赖也下载下来。当然，这也可能是"依赖地狱"的开始。

### 36.1.3 目录结构—— Maven 的"强迫症"

Maven 是一个有洁癖的工具，它要求项目严格遵循**标准化的目录结构**：

```
my-project/
├── pom.xml                    # Maven 配置文件（必须放根目录）
├── src/
│   ├── main/
│   │   ├── java/              # Java 源代码
│   │   └── resources/         # 资源文件（配置文件、图片等）
│   └── test/
│       ├── java/              # 测试源代码
│       └── resources/         # 测试资源文件
├── target/                    # 编译输出目录（Maven 自动生成）
│   └── classes/               # 编译后的 .class 文件
└── LICENSE
```

这种"约定优于配置（Convention Over Configuration）"的设计哲学，是 Maven 区别于 Ant 的重要特征。简单来说，Maven 已经帮你定好了最好的规矩，你最好乖乖遵守。

> 💡 **小贴士**：如果你不喜欢 Maven 的默认目录结构，也可以在 `pom.xml` 中自定义。但一般情况下，没事儿别改，保持和团队一致最重要。

### 36.1.4 pom.xml 详解

让我们来看一个典型的 `pom.xml` 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 坐标信息：唯一标识这个项目 -->
    <groupId>com.example</groupId>              <!-- 组织名称，通常是公司域名倒写 -->
    <artifactId>my-app</artifactId>            <!-- 项目名称 -->
    <version>1.0.0</version>                   <!-- 版本号 -->

    <!-- 打包方式：jar、war、pom 等 -->
    <packaging>jar</packaging>

    <!-- 项目名称和描述（可读性信息） -->
    <name>My Application</name>
    <description>A simple Maven demo</description>

    <!-- 属性配置 -->
    <properties>
        <java.version>17</java.version>       <!-- Java 版本 -->
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- 依赖列表：Maven 的精髓所在 -->
    <dependencies>
        <!-- 依赖 Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>

        <!-- 依赖 JUnit 测试 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>                 <!-- 只在测试时使用 -->
        </dependency>
    </dependencies>

    <!-- 构建配置 -->
    <build>
        <!-- 插件列表 -->
        <plugins>
            <!-- Maven 编译插件：指定 Java 版本 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>

            <!-- Maven 打包插件：生成可执行 JAR -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <archive>
                        <manifest>
                            <!-- 指定程序入口类 -->
                            <mainClass>com.example.App</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### 36.1.5 Maven 常用命令

Maven 的命令是在命令行中执行的，基本格式是 `mvn 命令`，后面可以跟各种参数。常见命令如下：

| 命令 | 说明 |
|------|------|
| `mvn clean` | 清理 `target` 目录，删除所有编译产物 |
| `mvn compile` | 编译项目，生成 `.class` 文件到 `target/classes` |
| `mvn test` | 运行测试用例 |
| `mvn package` | 打包项目，生成 JAR 或 WAR 文件 |
| `mvn install` | 将打包产物安装到本地仓库，供其他项目引用 |
| `mvn deploy` | 将打包产物发布到远程仓库 |
| `mvn dependency:tree` | 查看项目的依赖树（排依赖冲突神器） |
| `mvn clean package -DskipTests` | 清理并打包，跳过测试（赶时间专用） |

```bash
# 一个典型的 Maven 项目构建流程
cd my-project

# 第一次运行会下载很多依赖，请耐心等待...
# Maven 在下载依赖时会在控制台打印进度条
mvn clean package

# 如果你只想快速编译看看有没有语法错误
mvn compile

# 查看依赖树（排查依赖冲突时的必杀技）
mvn dependency:tree | head -50
```

### 36.1.6 依赖作用域（Dependency Scope）

Maven 的依赖是有"作用域"的，不同作用域的依赖在不同场景下生效：

- **compile（默认）**：编译、测试、运行都有效
- **test**：仅在测试时有效（如 JUnit）
- **provided**：编译和测试有效，但运行时由容器提供（如 Servlet API）
- **runtime**：编译时不需要，运行时才需要（如 JDBC 驱动）
- **system**：使用系统提供的 JAR，不从仓库获取（不推荐）

```xml
<!-- 示例： Servlet API 是 provided 作用域 -->
<!-- 因为 Tomcat、Jetty 等容器已经提供了这些类 -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>4.0.1</version>
    <scope>provided</scope>
</dependency>

<!-- 示例：JDBC 驱动是 runtime 作用域 -->
<!-- 编译时不需要，运行时由数据库厂商提供 -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.7.0</version>
    <scope>runtime</scope>
</dependency>
```

### 36.1.7 Maven 的优点与局限

Maven 作为一个"老前辈"，有其不可替代的优势：

**优点：**
- 约定大于配置，简单易用
- 依赖管理非常成熟，仓库生态丰富
- 生命周期清晰，命令标准化
- 插件生态丰富
- 几乎所有 Java 项目都认识它

**局限：**
- XML 配置有时候过于冗长
- 依赖冲突排查有时比较麻烦
- 编译速度相对于 Gradle 较慢
- 扩展性不如 Gradle 灵活

### 36.1.8 Maven 仓库结构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Maven 仓库体系                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐      ┌─────────────────┐                  │
│   │  本地仓库       │      │   远程仓库       │                  │
│   │  (~/.m2/repository) │◄───►│  (Maven Central) │                  │
│   │                 │      │  或公司私有仓库   │                  │
│   └────────┬────────┘      └────────┬────────┘                  │
│            │                        │                           │
│            │    依赖查找顺序          │                           │
│            ▼                        ▼                           │
│   ┌────────────────────────────────────────────┐                │
│   │  1. 先查本地仓库，有则直接使用              │                │
│   │  2. 本地没有则查远程仓库，下载到本地        │                │
│   │  3. 远程也没有？报错了事 :)                │                │
│   └────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 36.2 Gradle

### 36.2.1 Gradle 的诞生——青出于蓝

如果说 Maven 是一个成熟稳重的老大哥，那 **Gradle** 就是一个年轻有为的后起之秀。

Gradle 诞生于 2007 年，2009 年开源，2015 年成为 Android 官方构建工具。它巧妙地结合了 Maven 的约定优于配置理念和 Ant 的灵活性，同时引入了 **Groovy**（后来是 **Kotlin**）作为 DSL（领域特定语言），让构建脚本变得像写代码一样灵活。

Gradle 的 Logo 是一只大象——"Elephant"（因为 Gradle 发音类似... 好吧这是强行关联）。但大象负重能力强、记忆力好，这倒也挺符合 Gradle 处理复杂构建任务的能力。

### 36.2.2 Groovy 与 Kotlin DSL

Gradle 使用 **Groovy** 或 **Kotlin** 来编写构建脚本。相比 Maven 的 XML，代码式的 DSL 更加灵活、表达力更强。

```groovy
// build.gradle（Groovy DSL）- 传统方式
plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0.0'

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

// 依赖管理
repositories {
    mavenCentral()
}

dependencies {
    // implementation：仅编译时可见，不泄露到其他依赖
    implementation 'org.springframework.boot:spring-boot-starter-web:3.2.0'

    // testImplementation：仅测试时可见
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

// 应用程序入口
application {
    mainClass = 'com.example.App'
}
```

```kotlin
// build.gradle.kts（Kotlin DSL）- 现代推荐方式
// Kotlin DSL 提供了更好的 IDE 支持和类型安全

plugins {
    java
    application
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:3.2.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}

application {
    mainClass.set("com.example.App")
}
```

### 36.2.3 Gradle 项目目录结构

Gradle 的目录结构与 Maven 非常相似（毕竟都是"约定优于配置"）：

```
my-gradle-project/
├── build.gradle              # 构建脚本（根项目）
├── build.gradle.kts          # 或 Kotlin DSL 版本
├── settings.gradle           # 项目设置（定义包含哪些子项目）
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties  # Gradle 版本配置
├── gradlew                   # Linux/Mac 启动脚本
├── gradlew.bat               # Windows 启动脚本
├── src/
│   ├── main/
│   │   ├── java/            # Java 源代码
│   │   └── resources/       # 资源文件
│   └── test/
│       ├── java/            # 测试源代码
│       └── resources/       # 测试资源文件
└── app/                     # 可以有多个子项目
    └── build.gradle
```

### 36.2.4 Gradle 任务（Tasks）

Gradle 的核心是 **Task（任务）**。你可以把 Task 理解为一系列操作，比如编译、测试、打包等。你也可以定义自己的 Task。

```groovy
// build.gradle

// 定义一个自定义任务：生成项目报告
task generateReport {
    description = '生成项目的构建报告'
    group = 'build'

    doLast {
        // doLast：任务执行完毕后的回调
        println "正在生成报告..."
        println "项目名称: ${project.name}"
        println "版本: ${project.version}"
        println "Gradle 用户目录: ${gradle.gradleUserHome}"
        println "报告生成完毕！"
    }
}

// 定义一个依赖于其他任务的任务
task buildAll {
    description = '执行完整的构建流程'
    dependsOn clean, compileJava, test, jar
    // dependsOn：指定依赖的其他任务

    doLast {
        println "✅ 构建完成！"
    }
}

// 任务也可以链式调用
task deploy {
    dependsOn(build)
    doFirst {
        println "准备部署..."
    }
    doLast {
        println "部署完成！"
    }
}
```

### 36.2.5 Gradle 依赖配置（Configuration）

Gradle 使用不同的 **Configuration** 来区分依赖的使用范围，这比 Maven 的 scope 更灵活：

```groovy
dependencies {
    // implementation：内部依赖，编译时可见
    // 好处：不会泄露到依赖该模块的其他模块，减少"依赖污染"
    implementation 'org.springframework:spring-core:6.1.0'

    // api（等价于旧版的 compile）：公开依赖，编译和运行时都可见
    // 用于模块需要将依赖暴露给消费者的场景
    api 'org.apache.commons:commons-lang3:3.14.0'

    // compileOnly：仅编译时需要，运行时不需要
    compileOnly 'org.projectlombok:lombok:1.18.30'

    // testImplementation：仅测试时使用
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    testImplementation 'org.mockito:mockito-core:5.8.0'

    // runtimeOnly：运行时需要，编译时不需要
    runtimeOnly 'com.h2database:h2:2.2.224'
}
```

### 36.2.6 Gradle 常用命令

| 命令 | 说明 |
|------|------|
| `gradle build` | 构建项目 |
| `gradle clean build` | 清理并构建 |
| `gradle run` | 运行应用程序（需要配置 Application 插件） |
| `gradle test` | 运行测试 |
| `gradle tasks --all` | 列出所有可用任务 |
| `gradle dependencies` | 查看依赖树 |
| `gradle build --scan` | 构建并上传构建扫描报告到 Gradle Cloud |
| `gradle wrapper` | 生成 Gradle Wrapper 脚本 |

```bash
# Gradle Wrapper：确保团队使用相同版本的 Gradle
# 第一次需要安装 Gradle，之后可以用 gradlew 代替 gradle 命令
gradle wrapper --gradle-version 8.5

# 之后团队成员只需要运行
./gradlew build

# 查看依赖树（解决依赖冲突的利器）
gradle dependencies --configuration compileClasspath

# 运行应用
gradle run

# 快速测试（跳过完整构建）
gradle check
```

### 36.2.7 Gradle 多模块项目

Gradle 非常擅长管理 **多模块项目**。想象一下，你的项目有 `web`、`service`、`dao` 三个模块，Gradle 可以轻松管理它们之间的依赖关系。

```groovy
// settings.gradle
rootProject.name = 'my-multi-module-project'

// 包含子模块
include 'web', 'service', 'dao'
```

```groovy
// web 模块的 build.gradle
plugins {
    id 'java'
}

dependencies {
    implementation project(':service')  // 依赖 service 模块
}
```

```groovy
// service 模块的 build.gradle
plugins {
    id 'java'
}

dependencies {
    implementation project(':dao')       // 依赖 dao 模块
    implementation 'org.springframework:spring-context:6.1.0'
}
```

```
多模块项目结构示例：
┌─────────────────────────────────────────┐
│          my-multi-module-project        │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   web   │  │ service │  │   dao   │ │
│  │  模块   │──│  模块   │──│  模块   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│       │            │            │       │
│       └────────────┴────────────┘       │
│                    │                    │
│              所有模块依赖                 │
│              公共配置                     │
└─────────────────────────────────────────┘
```

### 36.2.8 Gradle 与 Maven 对决

让我们来一个全面的对比：

| 特性 | Maven | Gradle |
|------|-------|--------|
| **配置语言** | XML | Groovy/Kotlin DSL |
| **学习曲线** | 较平缓 | 稍陡 |
| **构建速度** | 较慢 | 快（增量构建、并行构建） |
| **灵活性** | 一般 | 高 |
| **依赖管理** | 成熟稳定 | 同样强大 |
| **IDE 支持** | 非常好 | 非常好 |
| **生态** | 非常成熟 | 快速发展中 |
| **XML 冗长** | 是 | 否（DSL 更简洁） |
| **增量构建** | 支持但较简单 | 智能增量构建 |
| **构建缓存** | 有限 | 强大的构建缓存 |
| **Android 支持** | 官方不支持 | 官方首选 |
| **社区** | 超大 | 大 |

### 36.2.9 Gradle 的独门绝技

Gradle 有几个 Maven 难以比拟的优势：

**1. 增量构建（Incremental Build）**
Gradle 只会重新构建有变化的部分，而不是像 Maven 那样每次都重新编译所有内容。这在大型项目中可以节省大量时间。

**2. 构建缓存与共享缓存**
Gradle 可以缓存构建结果，甚至可以在不同机器间共享缓存。配合 CI/CD 使用，效果拔群。

**3. 配置缓存（Configuration Cache）**
Gradle 可以缓存任务配置的结果，使得后续构建启动更快。

**4. 并行执行**
Gradle 可以并行执行相互独立的任务，充分利用多核 CPU。

```groovy
// 开启并行构建和构建缓存
// 在 gradle.properties 中配置
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
```

### 36.2.10 从 Maven 迁移到 Gradle

如果你有一个 Maven 项目，想迁移到 Gradle，Gradle 提供了一个便捷的命令：

```bash
# 在 Maven 项目目录下执行
gradle init --type pom

# 这会自动生成 build.gradle 文件
# 但由于 Maven 和 Gradle 的概念差异，部分配置可能需要手动调整
```

迁移时需要注意以下几点：

- Maven 的 `<properties>` 映射为 Gradle 的 `ext` 或直接在根作用域定义
- Maven 的 `<dependencies>` 直接映射为 `dependencies` 块
- Maven 的 `<plugins>` 映射为 `plugins` 块
- Maven 的 `<profile>`（不同环境不同配置）需要用 Gradle 的 **Task** 或 **Source Set** 重构

---

## 36.3 Maven 与 Gradle 结构图对比

```
┌────────────────────────────────────────────────────────────────────┐
│                    构建工具全景对比图                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │                       Maven                              │     │
│   │  ┌─────────────────────────────────────────────────────┐ │     │
│   │  │                    pom.xml                          │ │     │
│   │  │  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │ │     │
│   │  │  │ <groupId> │  │<artifactId>│  │  <version>   │   │ │     │
│   │  │  └───────────┘  └───────────┘  └───────────────┘   │ │     │
│   │  │       ▲              ▲               ▲             │ │     │
│   │  │       └──────────────┴───────────────┘             │ │     │
│   │  │                   坐标系统                         │ │     │
│   │  └─────────────────────────────────────────────────────┘ │     │
│   │                           │                               │     │
│   │                           ▼                               │     │
│   │  ┌─────────────────────────────────────────────────────┐ │     │
│   │  │                  生命周期（Lifecycle）                │ │     │
│   │  │  compile → test → package → install → deploy        │ │     │
│   │  └─────────────────────────────────────────────────────┘ │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                    │
│                          VS                                        │
│                                                                    │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │                       Gradle                             │     │
│   │  ┌─────────────────────────────────────────────────────┐ │     │
│   │  │               build.gradle / .kts                   │ │     │
│   │  │  plugins { java }                                   │ │     │
│   │  │  dependencies { implementation '...' }              │ │     │
│   │  │  tasks.register('hello') {                         │ │     │
│   │  │      doLast { println 'Hello!' }                    │ │     │
│   │  │  }                                                  │ │     │
│   │  └─────────────────────────────────────────────────────┘ │     │
│   │                           │                               │     │
│   │                           ▼                               │     │
│   │  ┌─────────────────────────────────────────────────────┐ │     │
│   │  │                   Task 图（DAG）                      │ │     │
│   │  │      [clean] ──► [compile] ──► [test] ──► [jar]      │ │     │
│   │  │            └──► [build] ◄─────────────────────────  │ │     │
│   │  └─────────────────────────────────────────────────────┘ │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 36.4 实战：创建一个 Spring Boot 项目

### 36.4.1 使用 Maven 创建

```bash
# 使用 Spring Boot 官方提供的 Maven 原型创建项目
mvn archetype:generate \
    -DgroupId=com.example \
    -DartifactId=spring-boot-demo \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DarchetypeVersion=1.4 \
    -DinteractiveMode=false

# 然后转换为 Spring Boot 项目（或者直接用 Spring Initializr 更方便）
# 推荐：https://start.spring.io/
```

或者手动创建 `pom.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <!-- Spring Boot 的父 POM，定义了依赖版本 -->
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>spring-boot-demo</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>Spring Boot Demo</name>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Web 起步依赖 -->
        <!-- 包含了 Spring MVC、Tomcat、Jackson 等 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Boot 测试起步依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Spring Boot Maven 插件：打包成可执行 JAR -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

```java
// src/main/java/com/example/DemoApplication.java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication  // 标记为 Spring Boot 应用
@RestController          // 标记为 REST 控制器
public class DemoApplication {

    public static void main(String[] args) {
        // 启动 Spring Boot 应用
        SpringApplication.run(DemoApplication.class, args);
    }

    @GetMapping("/hello")
    public String hello() {
        return "你好，Maven 构建的 Spring Boot 应用！";
    }
}
```

```bash
# 构建并运行
mvn clean package
java -jar target/spring-boot-demo-1.0.0.jar

# 访问 http://localhost:8080/hello
```

### 36.4.2 使用 Gradle 创建

```groovy
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Boot Web 起步依赖
    implementation("org.springframework.boot:spring-boot-starter-web")

    // 测试依赖
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

// Spring Boot 插件会自动处理依赖管理
```

```java
// src/main/java/com/example/DemoApplication.kt
package com.example

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
@RestController
class DemoApplication

fun main(args: Array<String>) {
    runApplication<DemoApplication>(*args)
}

@GetMapping("/hello")
fun hello(): String = "你好，Gradle 构建的 Spring Boot 应用！"
```

```bash
# 构建并运行
./gradlew bootJar
java -jar build/libs/demo-application-1.0.0.jar

# 或直接运行
./gradlew bootRun

# 访问 http://localhost:8080/hello
```

---

## 本章小结

本章我们学习了 Java 项目构建工具的核心知识：

| 概念 | 说明 |
|------|------|
| **Maven** | Apache 出品的经典构建工具，使用 `pom.xml` 和 XML 配置，约定优于配置，生态成熟 |
| **Gradle** | 新一代构建工具，使用 Groovy/Kotlin DSL，更加灵活，构建速度更快 |
| **POM** | Maven 的项目对象模型，定义项目坐标、依赖、插件等 |
| **坐标（Coordinates）** | `groupId:artifactId:version`，唯一标识 Maven 构件 |
| **仓库（Repository）** | 存储依赖的地方，分本地仓库和远程仓库 |
| **依赖作用域（Scope）** | Maven 区分依赖使用范围的方式：`compile`、`test`、`provided` 等 |
| **Configuration** | Gradle 区分依赖使用范围的方式：`implementation`、`api`、`testImplementation` 等 |
| **Task** | Gradle 的基本工作单元，类似 Maven 的 goal |
| **增量构建** | Gradle 的核心优势，只构建变化的部分，节省时间 |

**实战要点：**

1. **选择建议**：新项目推荐 Gradle，老项目或团队熟悉 Maven 则继续用 Maven
2. **依赖冲突**：使用 `mvn dependency:tree` 或 `gradle dependencies` 排查
3. **构建速度**：Gradle 的增量构建和并行执行在大项目中优势明显
4. **团队协作**：使用 Maven Wrapper 或 Gradle Wrapper 确保版本一致

> "工具没有最好，只有最适合。" 理解 Maven 和 Gradle 的设计哲学，才能在不同的项目中做出正确的选择。下一章我们将学习 Java 自动化测试，敬请期待！
