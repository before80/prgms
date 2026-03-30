+++
title = "第46章 常用工具速查"
weight = 460
date = "2026-03-30T14:33:56.933+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第四十六章 常用工具速查

> 磨刀不误砍柴工，工欲善其事，必先利其器。作为一个 Java 开发者，手里头没几把趁手的兵器，都不好意思跟人说自己是写代码的。这一章咱们就来盘点一下 Java 开发中那些离不开的工具，从 IDE 到 JVM 调优，从压测到 API 调试，保证让你看完直呼"原来还能这么干"！

---

## 46.1 开发工具

开发工具是程序员的"武器"，选对了武器，打怪升级效率翻倍。

### 46.1.1 IntelliJ IDEA — Java IDE 中的"战斗机"

如果说 Eclipse 是"老年活动中心"，那 IntelliJ IDEA 就是"高铁头等舱"。作为 JetBrains 家的当家花旦，IDEA 堪称 Java IDE 领域的扛把子，智能补全、重构、调试，样样精通。

**常用快捷键速查：**

```java
// 最重要的几个快捷键，背下来！
// Ctrl + Shift + F10        运行当前文件
// Ctrl + Shift + F          全局搜索
// Ctrl + N                   搜索类
// Ctrl + Shift + N           搜索文件
// Alt + Enter               万能提示（最重要！）
// Ctrl + Alt + L            格式化代码
// Ctrl + D                  复制当前行
// Ctrl + Y                  删除当前行
// Shift + F6                重命名
// Ctrl + Alt + M            提取方法
// Ctrl + Alt + V            提取变量
// Ctrl + /                  注释/取消注释
// Ctrl + Shift + /         块注释
// F2 / Shift + F2           跳转到上/下一个错误
```

**IDEA 实用配置：**

```properties
# 在 idea64.exe.vmoptions 中调整 JVM 参数，让 IDEA 飞起来
-Xms2048m              # 初始堆大小，建议 2G+
-Xmx4096m              # 最大堆大小，建议 4G+
-XX:ReservedCodeCacheSize=512m   # 代码缓存，增加编译速度
-XX:+UseG1GC           # 使用 G1 垃圾回收器
```

> 💡 小贴士：IDEA 的 Memory Indicator 插件可以让你实时看到内存使用情况，妈妈再也不用担心你的 IDEA 动不动就卡死了！

### 46.1.2 Maven — 依赖管理界的"淘宝"

Maven 是 Java 项目构建和依赖管理的标配，用 `pom.xml` 声明依赖，坐等 Maven 自动下载，省心省力。

**标准 Maven 项目结构：**

```
my-project/
├── pom.xml                  # 项目对象模型配置文件
├── src/
│   ├── main/
│   │   ├── java/            # Java 源代码
│   │   └── resources/       # 资源文件（配置文件等）
│   └── test/
│       ├── java/            # 测试源代码
│       └── resources/       # 测试资源文件
└── target/                  # 编译输出目录（Maven 自动生成）
```

**常用 Maven 命令：**

```bash
# 创建项目 - 一行命令搞定项目脚手架
mvn archetype:generate -DgroupId=com.example -DartifactId=my-app -DarchetypeArtifactId=maven-archetype-quickstart

# 编译项目
mvn clean compile

# 运行测试
mvn test

# 打包（jar/war）
mvn clean package

# 安装到本地仓库（其他项目可以引用）
mvn clean install

# 跳过测试快速打包
mvn clean package -DskipTests

# 查看依赖树 - 排查依赖冲突神器！
mvn dependency:tree

# 排除依赖中的某个包
mvn dependency:tree -Dincludes=org.springframework:spring-core
```

**pom.xml 示例：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 项目坐标，GAV：GroupId + ArtifactId + Version -->
    <groupId>com.example</groupId>
    <artifactId>spring-boot-demo</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <!-- 依赖管理 -->
    <dependencies>
        <!-- Spring Boot 起步依赖，一网打尽 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>

        <!-- Lombok：帮你生成 getter/setter/constructor，妈妈再也不用担心我写太多样板代码 -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.30</version>
            <scope>provided</scope>
        </dependency>

        <!-- 测试依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <!-- 构建配置 -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>3.2.0</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### 46.1.3 Gradle — 新时代的"构建之王"

Gradle 是 Android 官方推荐的构建工具，也是 Spring Boot 2.x 之后的默认构建工具。它用 Groovy 或 Kotlin DSL 写配置，比 Maven 的 XML 简洁太多。

**build.gradle 示例：**

```groovy
// plugins 块声明项目使用的插件
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
}

// 项目基本信息
group = 'com.example'
version = '1.0.0'

// 仓库配置
repositories {
    mavenCentral()
}

// 依赖管理，类似 Maven 的 dependencyManagement
dependencies {
    // Spring Boot Web
    implementation 'org.springframework.boot:spring-boot-starter-web'
    
    // Tomcat 内嵌服务器
    implementation 'org.springframework.boot:spring-boot-starter-tomcat'
    
    // 测试
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    
    // Lombok - 编译时注解处理器
    compileOnly 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'
}

// 打包为可执行 jar
bootJar {
    archiveFileName = 'app.jar'
}

// Java 版本
java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}
```

**常用 Gradle 命令：**

```bash
# 构建项目
gradle build

# 运行项目
gradle bootRun

# 清理并构建
gradle clean build

# 查看依赖树
gradle dependencies

# 运行测试
gradle test

# 交互式终端（修改代码后自动重载）
gradle bootRun --continuous
```

---

## 46.2 JVM 工具

Java 之所以能"一次编译，到处运行"，全靠 JVM（Java Virtual Machine，Java 虚拟机）在中间充当翻译官。但这个翻译官偶尔也会"摆烂"，这时候就需要我们用工具来"敲打敲打"它。

### 46.2.1 jps — 进程界的"雷达"

`jps`（Java Virtual Machine Process Status Tool）是 JDK 内置的工具，用来查看当前系统中有哪些 Java 进程在运行，相当于 Linux 的 `ps` 命令的 Java 特供版。

```bash
# 查看所有 Java 进程（显示进程ID和启动类名）
jps -l

# 查看详细输出（包含 JVM 参数）
jps -lv

# 查看所有进程，包括已经结束的（刚结束不久的）
jps -lvm

# 示例输出：
# 12345 com.example.Application          # 进程ID 12345，运行的是 Application 类
# 22334 jar -jar myapp.jar               # 通过 jar 命令启动
# 30301 sun.tools.jps.Jps -lvm           # jps 自己
```

### 46.2.2 jstat — JVM 统计信息的"情报员"

`jstat`（Java Virtual Machine Statistics Monitoring Tool）是 JVM 的统计信息监控工具，可以查看类加载、内存、GC（Garbage Collection，垃圾回收）、JIT 编译等数据。

```bash
# 语法：jstat -<option> <pid> <interval> <count>
# <interval> 是采样间隔（毫秒），<count> 是采样次数

# 查看类加载统计
jstat -class <pid>

# 示例输出：
# Loaded  Bytes  Unloaded  Bytes     Time
#   2,345  4,567.8    0     0.0       3.21
# Loaded: 加载的类数量
# Bytes: 加载的类占用的空间
# Unloaded: 卸载的类数量
# Time: 花费的时间

# 查看垃圾回收统计（最常用的命令之一）
jstat -gc <pid>

# 示例输出：
# S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCU    YGC     YGCT    FGC    FGCT     CGC    GCT
# 8704.0 8704.0 0.0    512.0   69632.0  5120.0   174784.0   67584.0  48896.0 47936.0 6144.0 6016.0    120    2.315     3    0.430     2    0.123
# S0C/S1C: Survivor 0/1 区容量
# S0U/S1U: Survivor 0/1 区使用量
# EC: Eden 区容量
# EU: Eden 区使用量
# OC: Old 区容量
# OU: Old 区使用量
# YGC: Young GC 次数
# YGCT: Young GC 总耗时
# FGC: Full GC 次数
# FGCT: Full GC 总耗时

# 每 1 秒采样一次，共采样 10 次
jstat -gc <pid> 1000 10

# 查看 JIT 编译统计
jstat -compiler <pid>

# 查看 GC 容量统计（容量 KB 为单位）
jstat -gccapacity <pid>
```

### 46.2.3 jstack — 线程 Dump 的"全景相机"

`jstack` 是生成 Java 虚拟机当前时刻的线程快照（thread dump）的工具，主要用来排查线程死锁、死循环、CPU 占用高等问题。

```bash
# 生成线程快照并输出到文件
jstack -F <pid> > threaddump.txt

# 同时输出锁的信息
jstack -l <pid> > threaddump.txt

# 查看线程堆栈的典型输出：
# "http-nio-8080-exec-1" #32 daemon prio=5 os_prio=0 tid=0x... nid=0x... waiting on condition
#    java.lang.Thread.State: WAITING (parking)
#         at sun.misc.Unsafe.park(Native Method)
#         at java.util.concurrent.locks.LockSupport.park(LockSupport.java:304)
#         at ...
#
# "main" #1 prio=5 os_prio=0 tid=0x... nid=0x... runnable
#    java.lang.Thread.State: RUNNABLE
#         at com.example.Application.main(Application.java:10)
```

**线程状态解读：**

| 状态 | 含义 | 常见原因 |
|------|------|----------|
| `NEW` | 新建 | 线程刚创建，还没 start() |
| `RUNNABLE` | 可运行 | 正在 JVM 中执行或在等待 CPU |
| `BLOCKED` | 阻塞 | 等待获取监视器锁 |
| `WAITING` | 等待 | 调用了 wait() 或 join() 等 |
| `TIMED_WAITING` | 限时等待 | 调用了 sleep() 或 wait(timeout) |
| `TERMINATED` | 终止 | 线程执行完毕 |

### 46.2.4 jmap — 内存映像的"CT 扫描仪"

`jmap`（Java Memory Map）用于生成堆内存转储快照（heap dump），相当于给 JVM 的内存做一次 CT 扫描，可以用来分析内存占用、排查内存泄漏。

```bash
# 生成堆转储文件（HPROF 格式）
jmap -dump:format=b,file=heap.hprof <pid>

# 生成带时间戳的堆转储文件
jmap -dump:format=b,file=heap_$(date +%Y%m%d_%H%M%S).hprof <pid>

# 查看堆内存使用摘要
jmap -heap <pid>

# 示例输出：
# Heap Configuration:
#    MaxHeapSize              = 4294967296 (4096.0MB)   # 最大堆
#    NewSize                  = 1073741824 (1024.0MB)  # 年轻代大小
#    OldSize                  = 3221225472 (3072.0MB)  # 老年代大小
#
# Heap Usage:
#    New Generation (Eden + 2 Survivor Space):
#       capacity = 928018432 (885.0MB)
#       used     = 412067328 (392.9MB)
#       free     = 515951104 (492.1MB)
#       44.39% used

# 查看类加载统计（包含每个类的实例数量和大小）
jmap -histo <pid>

# 只看前 20 个占用最多的类
jmap -histo <pid> | head -20
```

### 46.2.5 jinfo — JVM 配置的"透视镜"

`jinfo` 可以实时查看和修改 JVM 的运行参数，是调优时的得力助手。

```bash
# 查看 JVM 的所有系统属性
jinfo -sysprops <pid>

# 查看 JVM 的 flags（命令行参数）
jinfo -flags <pid>

# 查看某个特定 flag 的值
jinfo -flag MaxHeapSize <pid>
jinfo -flag PrintGCDetails <pid>

# 动态开启/关闭某个 flag（不需要重启 JVM！）
jinfo -flag +PrintGCDetails <pid>   # 开启
jinfo -flag -PrintGCDetails <pid>   # 关闭
```

### 46.2.6 Arthas — 阿里开源的"Java 诊断神器"

Arthas 是阿里开源的 Java 诊断工具，相比 JDK 自带的小工具，它更加直观和强大，支持热修复、方法追踪、反编译等功能。

**启动 Arthas：**

```bash
# 下载 arthas-boot.jar 并启动
java -jar arthas-boot.jar

# 或者一步到位
curl -s https://arthas.aliyun.com/arthas-boot.jar | java -jar -

# 然后选择要诊断的 Java 进程
```

**常用 Arthas 命令：**

```bash
# 仪表盘 - 查看系统实时状态（CPU、内存、线程、GC 等）
dashboard

# 查看类的方法
sc -d com.example.UserService

# 反编译类
jad com.example.UserService

# 查看方法的调用参数和返回值
watch com.example.UserService login "{params, returnObj}" -x 3

# 追踪方法调用
trace com.example.UserService login

# 生成火焰图（需要支持异步profiler）
profiler start
profiler stop --format html > flame.html

# 查找加载指定类的 ClassLoader
classloader -l

# 动态修改日志级别
logger -n com.example - DEBUG
```

### 46.2.7 GCEasy — GC 日志的"智能分析师"

GC 日志动辄几百行，人眼根本看不过来。GCEasy 是一个在线工具（也有离线版），上传 GC 日志就能自动分析出内存问题、GC 调优建议。

**生成 GC 日志的 JVM 参数：**

```bash
# 开启 GC 日志
java -Xlog:gc*:file=gc.log:time,uptime,level -jar myapp.jar

# 或者使用古老的参数（Java 8 及以前）
java -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:+PrintGCDetails \
     -Xloggc:gc.log -jar myapp.jar
```

**GC 日志关键指标解读：**

| 指标 | 含义 | 理想值 |
|------|------|--------|
| Young GC 频率 | 年轻代垃圾回收多久发生一次 | 越少越好 |
| Full GC 频率 | 老年代垃圾回收多久发生一次 | 尽量避免 |
| GC 总耗时 | GC 花费的总时间 | 占运行时间 < 5% |
| 内存分配速率 | 对象创建的速度 | 与业务相关 |

---

## 46.3 压测工具

上线前不压测，就像开车不系安全带——不是不能跑，是出了事就完了。压测工具帮你摸清系统的极限，找到性能瓶颈。

### 46.3.1 JMeter — 性能测试的"老大哥"

Apache JMeter 是 Apache 基金会开源的压测工具，支持 Web、HTTP、JDBC、SOAP、JMS 等多种协议，是业界最流行的压测工具之一。

**JMeter 测试计划示例（.jmx 文件）：**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <!-- 线程组配置 -->
    <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="压测线程组">
      <stringProp name="ThreadGroup.num_threads">100</stringProp>  <!-- 并发线程数：100 -->
      <stringProp name="ThreadGroup.ramp_time">10</stringProp>      <!-- 启动时间：10秒内启动100个线程 -->
      <stringProp name="ThreadGroup.duration">300</stringProp>       <!-- 持续时间：300秒 -->
      <stringProp name="ThreadGroup.delay"></stringProp>
    </ThreadGroup>
    
    <hashTree>
      <!-- HTTP 请求配置 -->
      <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="登录接口">
        <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
        <stringProp name="HTTPSampler.port">8080</stringProp>
        <stringProp name="HTTPSampler.path">/api/login</stringProp>
        <stringProp name="HTTPSampler.method">POST</stringProp>
        <boolProp name="HTTPSampler.autoRedirects">false</boolProp>
        <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
          <collectionProp name="Arguments.arguments">
            <!-- 请求体 -->
            <elementProp name="" elementType="HTTPArgument">
              <stringProp name="Argument.value">{"username":"test","password":"123456"}</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
          </collectionProp>
        </elementProp>
      </HTTPSamplerProxy>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

**JMeter 核心指标解读：**

| 指标 | 含义 | 参考值 |
|------|------|--------|
| Throughput | 吞吐量（TPS/QPS） | 越高越好 |
| Response Time | 响应时间 | P95 < 500ms |
| Error % | 错误率 | < 1% |
| 90% Line | 90 分位响应时间 | 衡量长尾延迟 |

### 46.3.2 wrk — HTTP 压测的"轻量级选手"

wrk 是一款小巧但强大的 HTTP 压测工具，基于系统底层异步 I/O，性能极高，适合快速摸底接口性能。

**安装：**

```bash
# Linux/macOS
git clone https://github.com/wg/wrk.git
cd wrk && make

# Windows 可以用 WSL
```

**常用命令：**

```bash
# 基础用法：100 个线程，连接保持 30 秒，100 个并发
wrk -t12 -c100 -d30s http://localhost:8080/api/users

# 高级用法：带自定义头、POST 请求
wrk -t8 -c200 -d30s -H "Content-Type: application/json" \
    -H "Authorization: Bearer token123" \
    --latency \
    -s post.lua http://localhost:8080/api/login

# 报告解读：
# Running 30s @ http://localhost:8080/api/users
# Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency   12.34ms    5.67ms  89.12ms   85.23%
#     Req/Sec    8.56k     1.23k   12.34k    70.12%
#   12 threads and 100 connections
#   1234567 requests in 30.01s, 567.89MB read
# Requests/sec:  41152.34    # QPS
# Transfer/sec:     18.92MB  # 吞吐量
# Latency Distribution:
#      50%   11.56ms
#      75%   15.23ms
#      90%   19.87ms
#      99%   35.12ms
```

**wrk Lua 脚本示例（自定义 POST 请求）：**

```lua
-- post.lua - wrk 的 Lua 脚本
wrk.method = "POST"                    -- 设置 HTTP 方法
wrk.body   = '{"username":"test","password":"123456"}'  -- 请求体
wrk.headers["Content-Type"] = "application/json"         -- 请求头
```

### 46.3.3 ab — Apache Bench 的"简单粗暴"

ab（Apache Bench）是 Apache 自带的压测工具，安装简单，命令好记，适合快速验证接口能不能抗住。

```bash
# 安装（Windows 下安装 Apache 即可，Linux/macOS 一般自带）
# 发送 10000 个请求，100 个并发
ab -n 10000 -c 100 http://localhost:8080/api/users

# 带 POST 数据
ab -n 1000 -c 50 -p data.json -T application/json \
   http://localhost:8080/api/login

# 报告输出：
# Server Software:        Apache-Coyote/1.1
# Server Hostname:        localhost
# Server Port:            8080
#
# Document Path:          /api/users
# Document Length:        1234 bytes
#
# Concurrency Level:      100
# Time taken for tests:   5.678 seconds
# Complete requests:      10000
# Failed requests:        0
# Total transferred:      13567890 bytes
# HTML transferred:       12340000 bytes
# Requests per second:    1761.23 [#/sec] (mean)    # QPS
# Time per request:       56.78 [ms] (mean)          # 平均响应时间
# Time per request:       0.57 [ms] (mean, across all concurrent requests)
# Transfer rate:          2335.67 [Kbytes/sec] received
#
# Connection Times (ms)
#               min  mean[+/-sd] median   max
# Connect:        0    0   0.1      0       1
# Processing:    10   56  12.3     52     189
# Waiting:        9   55  12.1     51     188
# Total:         10   56  12.3     52     189
#
# Percentage of the requests served within a certain time (ms)
#   50%     52      # 50 分位
#   66%     58
#   75%     63
#   90%     75
#   95%     89
#   98%    102
#   99%    115
#  100%    189 (longest request)
```

### 46.3.4 Hey — API 压测的"后起之秀"

Hey（原名 boom）是 Go 语言写的压测工具，安装简单，输出直观，是 wrk 的好替代品。

```bash
# 安装
go install github.com/rakyll/hey@latest

# 基础用法
hey -n 10000 -c 100 http://localhost:8080/api/users

# 带请求体
hey -n 1000 -c 50 -m POST -d '{"username":"test"}' \
    -H "Content-Type: application/json" \
    http://localhost:8080/api/login

# 关键指标：
# Summary:
#   Total:        5.2340 secs
#   Slowest:     0.1890 secs
#   Fastest:     0.0102 secs
#   Average:     0.0523 secs
#   Requests/sec:  1908.67      # QPS
#   Total data:   12345678 bytes
#   Size/request: 1234 bytes
```

---

## 46.4 API 调试工具

前后端分离的时代，API 调试是每个开发者的日常。没有趁手的工具，就像没有钥匙还想开门——费劲！

### 46.4.1 Postman — API 调试的"瑞士军刀"

Postman 是 API 开发领域最流行的工具，支持请求构建、环境变量、集合、自动化测试等功能。

**Postman 集合示例（导出为 JSON）：**

```json
{
  "info": {
    "name": "用户管理 API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "登录",
      "request": {
        "method": "POST",
        "url": "http://localhost:8080/api/login",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"admin\",\"password\":\"123456\"}"
        }
      }
    },
    {
      "name": "获取用户列表",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:8080/api/users?page=1&size=20",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8080",
          "path": ["api", "users"],
          "query": [
            {"key": "page", "value": "1"},
            {"key": "size", "value": "20"}
          ]
        },
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}"
          }
        ]
      }
    }
  ]
}
```

**环境变量示例：**

```json
{
  "id": "local-env",
  "name": "本地环境",
  "values": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8080",
      "type": "default"
    },
    {
      "key": "token",
      "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "type": "secret"
    },
    {
      "key": "username",
      "value": "admin",
      "type": "default"
    }
  ]
}
```

### 46.4.2 cURL — 命令行的"HTTP 万能钥匙"

cURL 是命令行工具中的瑞士军刀，发 HTTP 请求只是它的技能之一。虽然没有图形界面，但熟练之后效率极高，而且天然适合脚本化。

**常用 cURL 命令：**

```bash
# GET 请求（最基本用法）
curl https://api.example.com/users

# GET 带查询参数
curl "https://api.example.com/users?id=1&name=test"

# POST JSON 数据
curl -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'

# POST 表单数据
curl -X POST http://localhost:8080/api/login \
  -d "username=admin" \
  -d "password=123456"

# 带自定义请求头
curl -X GET http://localhost:8080/api/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Accept: application/json" \
  -H "X-Request-ID: 123456"

# 上传文件
curl -X POST http://localhost:8080/api/upload \
  -F "file=@/path/to/file.pdf" \
  -F "description=测试文件"

# 下载文件（-O 使用远程文件名，-o 指定本地文件名）
curl -O https://example.com/largefile.zip
curl -o localfile.zip https://example.com/largefile.zip

# 带 Cookie
curl -X GET http://localhost:8080/api/profile \
  -b "session=abc123" \
  -c cookies.txt      # -b 读取 cookie，-c 保存 cookie

# 跟随重定向
curl -L http://short.url/abc

# 静默模式（不显示进度条）
curl -s https://api.example.com/data

# 显示响应头
curl -i https://api.example.com/users
# HTTP/1.1 200 OK
# Date: Mon, 30 Mar 2026 14:00:00 GMT
# Content-Type: application/json
# Content-Length: 1234
#
# {"data": [...]}

# 只显示响应头
curl -I https://api.example.com/users
curl --head https://api.example.com/users

# 详细输出（显示请求和响应的完整过程）
curl -v https://api.example.com/users
curl --verbose https://api.example.com/users

# 超时设置
curl --connect-timeout 10 --max-time 30 https://api.example.com/users
# --connect-timeout: 连接超时
# --max-time: 总超时

# 限速（防止压测时被封）
curl --limit-rate 1m https://api.example.com/largefile.zip

# 输出到文件而非 stdout
curl https://api.example.com/data -o result.json

# 使用代理
curl -x http://proxy.example.com:8080 https://api.example.com/users

# 跳过 SSL 证书验证（测试环境用，生产环境别用！）
curl -k https://localhost:8443/api/users
curl --insecure https://localhost:8443/api/users
```

**cURL 实战脚本：**

```bash
#!/bin/bash
# api-test.sh - API 自动化测试脚本

BASE_URL="http://localhost:8080/api"
TOKEN=""

echo "===== 1. 登录获取 Token ====="
LOGIN_RESP=$(curl -s -X POST "${BASE_URL}/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}')

echo "登录响应: $LOGIN_RESP"
TOKEN=$(echo $LOGIN_RESP | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Token: $TOKEN"
echo ""

echo "===== 2. 获取用户列表 ====="
curl -s -X GET "${BASE_URL}/users?page=1&size=10" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" | jq .

echo ""
echo "===== 3. 创建用户 ====="
curl -s -X POST "${BASE_URL}/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"name":"张三","email":"zhangsan@example.com"}' | jq .
```

### 46.4.3 Apifox — API 管理的"后起之秀"

Apifox 是国产的 API 管理工具，集 API 设计、调试、测试、文档生成于一体，Postman 的优秀替代品，中文界面对国内开发者非常友好。

**Apifox 的核心功能：**

```yaml
# API 设计 - 类似 OpenAPI 规范
openapi: 3.0.0
info:
  title: 用户管理系统
  version: 1.0.0
paths:
  /users:
    get:
      summary: 获取用户列表
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    example: 0
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
```

### 46.4.4 HTTPie — 命令行的"人类友好版 cURL"

HTTPie 发音为 "aitch-tee-tee-pie"，是一个命令行 HTTP 客户端，设计目标是让人更容易使用，语法比 cURL 自然很多。

```bash
# 安装
# pip install httpie

# GET 请求（简洁语法）
https GET localhost:8080/api/users

# POST 请求（自动 JSON 格式化）
https POST localhost:8080/api/login username=admin password=123456

# 带认证
https GET localhost:8080/api/profile Authorization:"Bearer token123"

# 下载文件
https download localhost:8080/files/report.pdf

# 使用 session（自动管理 Cookie 和 Header）
https session-local api GET localhost:8080/api/profile
https session-local api POST localhost:8080/api/logout

# 漂亮输出（带颜色和格式）
https --print=hHbB localhost:8080/api/users
# h: request headers
# H: response headers
# b: response body
# B: response body (pretty printed)

# 模拟不同方法
https DELETE localhost:8080/api/users/1
https PUT localhost:8080/api/users/1 name=newname
https PATCH localhost:8080/api/users/1 name=newname
```

### 46.4.5 Insomnia — 开发者的"API 调试工作站"

Insomnia 是一款跨平台的 API 调试工具，界面美观，支持 GraphQL、WebSocket、gRPC 等协议。

**Insomnia 环境配置示例：**

```json
{
  "_id": "env_123456",
  "_type": "environment",
  "name": "Development",
  "data": {
    "baseUrl": "http://localhost:8080",
    "apiKey": "dev-key-12345",
    "timeout": 30000
  }
}
```

**Insomnia GraphQL 支持：**

```graphql
# Query 编辑器支持语法高亮、自动补全
query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    email
    createdAt
  }
}

# 变量面板
{
  "id": "1"
}
```

---

## 本章小结

本章我们走马观花地浏览了 Java 开发中最常用的工具，涵盖了四大领域：

### 工具速查表

| 类别 | 工具 | 一句话定位 |
|------|------|------------|
| **开发工具** | IntelliJ IDEA | Java IDE 界的扛把子 |
| | Maven | XML 配置的老牌构建工具 |
| | Gradle | Kotlin/Groovy DSL 的新锐构建工具 |
| **JVM 工具** | jps | 进程雷达，查看 Java 进程 |
| | jstat | 统计信息，监控 GC/类加载 |
| | jstack | 线程快照，排查死锁 |
| | jmap | 内存映像，生成堆转储 |
| | jinfo | 参数透视，查看/修改 JVM 参数 |
| | Arthas | 阿里开源的诊断神器 |
| | GCEasy | GC 日志智能分析 |
| **压测工具** | JMeter | 功能全面的企业级压测 |
| | wrk | 轻量级 HTTP 压测 |
| | ab | Apache 自带的简单压测 |
| | hey | Go 写的后起之秀 |
| **API 调试** | Postman | 瑞士军刀，API 调试标配 |
| | cURL | 命令行万能钥匙 |
| | Apifox | 国产 API 管理新星 |
| | HTTPie | 人类友好版 cURL |
| | Insomnia | 跨平台 API 调试工作站 |

### 核心记忆点

1. **JVM 工具六件套**：jps → jstat → jstack → jmap → jinfo → Arthas，故障排查的经典套路
2. **压测关注三个指标**：QPS（吞吐量）、响应时间（P50/P95/P99）、错误率
3. **API 调试核心**：请求方法、URL、Header、Body、认证，这是任何工具都绕不开的五要素

> 工具虽多，但不必样样精通。根据自己的工作场景选择几款顺手的深入使用，其他的了解个大概即可。毕竟，工具有价，思维无价！

下一章我们将进入 **实战篇**，把手头的工具用起来，真正开始"造轮子"！
