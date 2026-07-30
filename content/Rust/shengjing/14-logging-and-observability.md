+++
title = "14-日志和监控"
date = 2026-07-28T14:49:00+08:00
weight = 140
type = "docs"
description = "《Rust语言圣经》「日志和监控」精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「日志和监控」

# 日志和监控

日志 + 监控是开发实践核心；AIOps 智能化运维依赖海量日志/指标数据分析。

## 日志详解

日志 = 某时间点向指定位置输出带级别、时间、事件的信息（与语言无关）。

### 日志级别和输出位置

常见级别（高→低）：

| 级别 | 典型场景 |
|------|----------|
| Fatal | 致命错误，程序无法继续 |
| Error | 程序/严重业务错误（非用户输错密码类） |
| Warn | 需关注、不确定是否错误 |
| Info | 运行状态、用户操作、请求起止 |
| Debug | 开发者调试细节 |
| Trace | 比 Debug 更细（tracing 中） |

生产环境设**最低级别**过滤（如 Info 则 Debug 不输出）。可按级别分输出目标：Debug→控制台，Error→文件。

**输出位置**：标准输出（控制台）、文件。容器场景常 stdout + 采集 agent，本地不落盘。

### 日志查看

- 控制台直接看 / `tail -f` / `grep`
- 文件内搜索
- 可视化：ES + Kibana/Grafana（需先采集集中存储）

### 日志采集

- 不必写文件：agent 读 stdout → 发送到 ES/Kafka 等
- 容器典型：进程 stdout → sidecar agent → 远端平台
- 工具：Filebeat、**Vector**（Rust，高性能）

### 中心化日志存储

集中采集 → 关键词索引存储（如 ElasticSearch）→ 按关键字检索，而非逐机翻文件。

## 日志门面 log

[log](https://github.com/rust-lang/log) = Rust 日志**门面**（facade），定义统一 API；具体输出由实现 crate 提供。

### Log 特征

```rust
trait Log: Sync + Send {
    fn enabled(&self, metadata: &Metadata) -> bool;
    fn log(&self, record: &Record);
    fn flush(&self);
}
```

### 日志宏

`trace!` / `debug!` / `info!` / `warn!` / `error!` / `log!(Level::..., ...)`

- `log_enabled!(Level::Debug)`：昂贵日志前先判断是否启用
- 库作者：只依赖 `log` 门面，不绑定具体实现

### 日志输出在哪里？

门面本身不输出；需注册 **logger 实现**（全局唯一）。

### 使用具体的日志库

**应用开发者**常用：

| crate | 特点 |
|-------|------|
| `env_logger` | 环境变量 `RUST_LOG=debug` 控制级别 |
| `simple_logger` | 简单 |
| `log4rs` | 可配置（类 log4j） |

**日志库开发者**：实现 `Log` trait + `set_logger` / `set_max_level`。

## 使用 tracing 记录日志

[tracing](https://github.com/tokio-rs/tracing) 本质是**分布式追踪 SDK**，兼容 `log` API，可作日志库。

### 一个简单例子

```toml
tracing = "0.1"
tracing-subscriber = "0.3"
```

```rust
tracing_subscriber::registry().with(fmt::layer()).init();
log::info!("via log facade");
tracing::info!(foo = 42, "via tracing");
```

须先 `init` subscriber 才有输出。

### 异步编程中的挑战

异步任务顺序不确定 → 纯时间点日志难串联。**Span** 记录时间段，带上下文，可嵌套。

### 核心概念

| 概念 | 说明 |
|------|------|
| **Span** | 时间段（开始/结束），可嵌套，RAII `enter()` |
| **Event** | 时间点事件，可在 span 内 |
| **Collector/Subscriber** | 收集 span/event（`tracing-subscriber`） |

### 使用方法

- `span!(Level::INFO, "name", key = val)`
- `#[instrument]`：自动为函数创建 span，记录参数
- `span.in_scope(|| { ... })`
- async：`Instrument` trait / `.instrument(span)`
- span 嵌套：子 span 自动关联父 span

宏配置：`target:`、`level:`、`?`（Debug 打印）、`%`（Display）、`Empty` 占位字段。

文件输出：`fmt::layer().with_writer(non_blocking(file))`。

## 自定义 tracing 的输出格式

基于 `tracing-subscriber` Layer 体系：

1. 实现 `Layer<S>` 或组合现有 layer
2. **访问者模式**：on_event 捕获 Event
3. 自定义 JSON logger：格式化字段 + span 扩展数据
4. span 数据存 `Extensions`；可自建存储

目标：输出结构化 JSON 日志，对接 ELK/Loki。

## 监控

### 可观测性

三大支柱：**Metrics（指标）** / **Log（日志）** / **Trace（链路）**

| 类型 | 描述 |
|------|------|
| Metric | 一段时间内行为次数/分布 |
| Log | 某时间点事件 |
| Trace | 一次请求跨服务完整路径 |

孤立使用效率低（告警后大海捞针）。**Trace 为纽带**：沿 trace 收集 log，按标签聚合 metric → 告警可直达根因 trace + 各服务细节。

落地链路：**采集** → **处理/存储**（各自格式） → **查询展示**。

推荐 **[OpenTelemetry](https://opentelemetry.io)**：协议 + API + 多语言 SDK。

### 分布式追踪

- 请求入口生成 `trace_id`，透传各服务（SDK 自动）
- 每服务用同一 `trace_id` 记录 span
- 查询时用 `trace_id` 还原全链路
- tracing 的 span 模型与 OTel 理念一致；可用 `tracing-opentelemetry` 导出

---

**选型建议**

| 场景 | 推荐 |
|------|------|
| 库 crate | 仅 `log` 门面 |
| 简单 CLI | `env_logger` |
| 异步/微服务 | `tracing` + `tracing-subscriber` |
| 可观测性平台 | OpenTelemetry + Vector 采集 |
