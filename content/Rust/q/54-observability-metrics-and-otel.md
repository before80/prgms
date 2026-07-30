+++
title = "54-observability-metrics-and-otel"
date = 2026-07-28T14:49:00+08:00
weight = 540
type = "docs"
description = "面向 Go 用户讲清 Prometheus 指标、/metrics、tracing 分工与 OpenTelemetry"
isCJKLanguage = true
draft = false

+++

# 可观测性：指标与 OpenTelemetry (Observability, Metrics and OTel)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否会 `slog`/`zap` + Prometheus，却不知 Rust 里 **metrics** / **tracing** / **OTel** 怎么分工？
- 你是否想给 axum 挂 **`/metrics`**，对标 Go `promhttp`？
- 你是否想把 **trace_id** 从 HTTP 传到下游，却只会打日志？
- 你是否分不清健康检查端口和指标端口该不该拆？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| metrics | — | 指标 | 可聚合的数值时间序列 | Prometheus client |
| Prometheus | — | 监控系统 | 拉取 `/metrics` 文本格式常见 | 同名 |
| counter | — | 计数器 | 只增不减的累计值 | `Counter` |
| histogram | — | 直方图 | 观察值分布（延迟常用） | `Histogram` |
| gauge | — | 仪表盘 | 可上可下的瞬时值 | `Gauge` |
| **OpenTelemetry** / OTel | — | 可观测性标准 | traces/metrics/logs 的厂商中立 API | `go.opentelemetry.io` |
| OTLP | OTel Protocol | 导出协议 | 把遥测发到 Collector | 同名 |
| trace_id | — | 追踪 ID | 一次请求跨服务的关联键 | 同概念 |
| span | — | 跨度 | 一次操作的时间区间；见 [39](../39-logging-and-tracing/) | 同概念 |
| RED | Rate/Errors/Duration | 请求三类指标 | 监控服务的常用配方 | 同概念 |
| USE | Utilization/Saturation/Errors | 资源三类指标 | 监控主机/池的常用配方 | 同概念 |
| scrape | — | 抓取 | Prometheus 拉指标 | 同概念 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. Prometheus 指标在 Rust 里怎么埋？ {#q1}
**Tags:** `hot` `Prometheus` `metrics` `counter` `histogram`
**适用版本:** `metrics` / `prometheus` crate；以文档为准

**一句话答案：**
两条常见路：**`metrics` crate**（门面 + 适配器导出）或直接用 **`prometheus`** crate 的 `IntCounter`/`Histogram`。对标 Go `prometheus/client_golang`：在业务点 `inc` / `observe`，另起 `/metrics` 暴露。

**解答：**
```toml
[dependencies]
metrics = "0.24"
# 再选 exporter，例如 metrics-exporter-prometheus
```

```text
metrics::counter!("http_requests_total", "path" => "/api").increment(1);
metrics::histogram!("http_request_duration_seconds").record(0.042);
```

```rust
fn main() {
    // 命名：snake_case + _total / _seconds 等 Prometheus 惯例
    let name = "http_requests_total";
    assert!(name.ends_with("_total"));
}
```

**Go 对比：**
```go
requests.WithLabelValues("GET", "/api").Inc()
```
- **Go 怎么做**：client_golang 注册 + handler。
- **Rust 为什么不同**：crate 分裂，但指标类型相同。
- **Go 程序员易踩的坑**：高基数 label（用户 ID）打爆时序。

**记忆点：**
- counter / histogram / gauge 三件套。
- label 低基数。

---

## Q2. axum 怎么暴露 `/metrics`？（对标 `promhttp`） {#q2}
**Tags:** `hot` `axum` `promhttp` `/metrics`
**适用版本:** axum + prometheus exporter

**一句话答案：**
挂一条 `GET /metrics`，handler 返回 Prometheus **文本格式**正文；或用独立端口只给内网 scrape。对标 Go `promhttp.Handler()`。

**解答：**
```text
// 示意：metrics-exporter-prometheus 装好后
// Router::new().route("/metrics", get(|| async { encode_metrics() }))
```

```toml
# 示意组合
# axum + metrics-exporter-prometheus / prometheus crate gather
```

```rust
fn main() {
    // 生产：/metrics 勿对公网裸奔；用网络策略或独立 listen
    println!("scrape endpoint ≠ public API");
}
```

**Go 对比：**
```go
http.Handle("/metrics", promhttp.Handler())
```
- 心智相同。
- **Go 程序员易踩的坑**：和业务鉴权绑同一中间件导致 Prometheus 拉不到。

**记忆点：**
- `/metrics` 专用、可内网端口。
- 与 [49-deployment Q12](../49-deployment-and-docker/#q12) 呼应。

---

## Q3. tracing span 和 Prometheus 指标怎么分工？ {#q3}
**Tags:** `hot` `tracing` `metrics` `分工`
**适用版本:** 概念

**一句话答案：**
**指标**：聚合看「系统健康」（QPS、P99、错误率）。**tracing span**：单次请求排障（谁慢、父子调用）。日志：事件叙述。三者互补，不是互相替代（日志详见 [39](../39-logging-and-tracing/)）。

**解答：**
```text
看板红了 ──► 看 metrics（哪条路径错了）
需要根因 ──► 用 trace_id 拉 spans / 日志
```

```rust
fn main() {
    println!("RED metrics for alerts; spans for debug");
}
```

```text
# 反模式：只打 info 日志当监控——告警与聚合都很痛苦
```

**Go 对比：**
- 同样三分法。
- **Go 程序员易踩的坑**：span 当唯一监控，成本高。

**记忆点：**
- 告警靠指标；深潜靠追踪。
- 日志别冒充时序库。

---

## Q4. OpenTelemetry 最小怎么接线？ {#q4}
**Tags:** `hot` `OpenTelemetry` `OTLP` `exporter`
**适用版本:** opentelemetry Rust SDK；以当前文档为准

**一句话答案：**
引入 OTel SDK + **OTLP** exporter，指向 Collector；用 tracing-opentelemetry 桥接 **tracing** span，或用 OTel API 直接打。对标 Go `otel` SDK + exporter。

**解答：**
```toml
# 示意（版本锁定随项目）
# opentelemetry = "..."
# opentelemetry-otlp = "..."
# tracing-opentelemetry = "..."
```

```text
# 流程
# 1. 建 TracerProvider + OTLP exporter
# 2. 设全局 propagator（W3C TraceContext）
# 3. tracing subscriber 加 OpenTelemetryLayer
# 4. 进程退出前 shutdown provider（冲刷）
```

```rust
fn main() {
    println!("app → OTLP → collector → Jaeger/Tempo/...");
}
```

**Go 对比：**
- 架构相同：SDK → exporter → backend。
- **Go 程序员易踩的坑**：忘了 shutdown 导致尾部 span 丢失。

**记忆点：**
- OTLP 进 Collector，别把厂商 SDK 写死进业务。
- 退出要 flush。

---

## Q5. `trace_id` 怎么从 HTTP 传到下游？ {#q5}
**Tags:** `hot` `trace_id` `propagation` `W3C`
**适用版本:** W3C Trace Context；OTel propagator

**一句话答案：**
用标准传播头（常见 **`traceparent`**）注入出站请求；入站中间件提取并创建子 span。手写时也可透传 `X-Request-Id`，但跨厂商互通优先 W3C。

**解答：**
```text
入站：extractor 读 traceparent → 建 span
出站：injector 写到 reqwest/tonic metadata
日志：tracing 的 %span 或显式记 trace_id 字段
```

```text
# reqwest：中间件或手动 header
# tonic：metadata 拦截器
```

```rust
fn main() {
    let header = "traceparent";
    assert_eq!(header, "traceparent");
}
```

**Go 对比：**
```go
otel.GetTextMapPropagator().Inject(ctx, ...)
```
- 同标准。
- **Go 程序员易踩的坑**：只在日志生成 UUID，不传到下游。

**记忆点：**
- 传播头 + 中间件，不是靠巧合。
- 日志带同一 id。

---

## Q6. JSON 日志如何带上 span 字段？ {#q6}
**Tags:** `common` `JSON` `logging` `span`
**适用版本:** tracing-subscriber json

**一句话答案：**
`tracing-subscriber` 的 JSON 格式层可输出 span 上下文；业务用 `info_span!`/`instrument` 包住请求。详见 [39](../39-logging-and-tracing/)，本篇只强调「和 metrics/OTel 一起想」。

**解答：**
```toml
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

```text
tracing_subscriber::fmt().json().init();
let span = tracing::info_span!("request", path = %path);
let _g = span.enter();
tracing::info!("handled");
```

```rust
fn main() {
    println!("JSON logs + span fields = join with traces");
}
```

**Go 对比：**
- zap 字段里塞 `trace_id`。
- **Go 程序员易踩的坑**：文本日志无结构化字段，平台搜不动。

**记忆点：**
- 结构化日志 + 关联 id。
- 与 [39](../39-logging-and-tracing/) 交叉。

---

## Q7. RED / USE 在 Rust 服务里怎么落地？ {#q7}
**Tags:** `common` `RED` `USE` `SLO`
**适用版本:** 监控配方

**一句话答案：**
服务接口埋 **RED**：Rate（QPS）、Errors、Duration（延迟直方图）。资源池埋 **USE**：利用率、饱和度、错误。Rust 只是用 counter/histogram 实现这些名字。

**解答：**
```text
http_requests_total{path,status}
http_request_duration_seconds_bucket{path}
db_pool_connections_in_use
db_pool_acquire_timeout_total
```

```rust
fn main() {
    println!("name metrics after questions you alert on");
}
```

**Go 对比：**
- 配方与语言无关。
- **Go 程序员易踩的坑**：只埋 gauge「当前连接」没有延迟分布。

**记忆点：**
- API → RED；池/CPU → USE。
- 直方图服务 P99。

---

## Q8. 和 Go otel + prometheus 对照表？ {#q8}
**Tags:** `common` `cheatsheet` `Go`
**适用版本:** 概念对照

**一句话答案：**
Go client_golang ≈ Rust `prometheus`/`metrics`；`promhttp` ≈ `/metrics` handler；`otel` SDK ≈ Rust OTel + tracing 桥。日志常用 tracing 而不是 std log。

**解答：**

| Go | Rust |
|----|------|
| client_golang | metrics / prometheus crate |
| promhttp | `/metrics` 路由 |
| otel SDK | opentelemetry-* |
| zap/slog 字段 | tracing + JSON subscriber |
| net/http/pprof | 见 [51](../51-profiling-and-benchmarking/) |

```rust
fn main() {
    println!("same signals; different crate names");
}
```

**记忆点：**
- 信号模型照搬 Go；换 crate。
- 剖析走 51，日志走 39。

---

## Q9. 采样 / 动态日志级别怎么做？ {#q9}
**Tags:** `common` `sampling` `RUST_LOG`
**适用版本:** 生产惯例

**一句话答案：**
追踪用**头采样/尾采样**（Collector 或 SDK）；日志用 `RUST_LOG` / reload 层调级别。全量 debug + 全量 trace 会先打垮 I/O 与账单。

**解答：**
```text
# 运行时
RUST_LOG=info,my_crate=debug

# 追踪：生产常 1%~10% 或按错误强制留样
```

```rust
fn main() {
    println!("sample traces; keep error logs hot");
}
```

**Go 对比：**
- 同样要采样。
- **Go 程序员易踩的坑**：开发开全量，生产忘记关。

**记忆点：**
- 追踪采样；日志分级。
- 错误路径可强制采样。

---

## Q10. 健康检查 vs readiness vs metrics 端口怎么拆？ {#q10}
**Tags:** `common` `health` `readiness` `ports`
**适用版本:** K8s/容器惯例；见 [49](../49-deployment-and-docker/)

**一句话答案：**
**liveness** 探活进程；**readiness** 表示能否接流量（依赖就绪）；**metrics** 给 Prometheus。可以同端口不同路径，或 metrics 单独 listen。关停时先让 readiness 失败。

**解答：**
```text
:8080/healthz     liveness
:8080/readyz      readiness（查 DB/MQ）
:9090/metrics     scrape（可内网）
```

```rust
fn main() {
    println!("ready=false during drain; metrics still scrapable optional");
}
```

**Go 对比：**
- 同 K8s 探针模型。
- **Go 程序员易踩的坑**：liveness 里查 DB——依赖抖则杀循环。

**记忆点：**
- live ≠ ready ≠ metrics。
- 关停顺序：ready 下线 → 排空 → 退出。

---

## Q11. 库代码里该不该 init 全局 metrics/tracer？ {#q11}
**Tags:** `common` `library` `init`
**适用版本:** 库 vs 二进制边界

**一句话答案：**
**库只埋点、不 init 全局 subscriber/exporter**；由二进制/`main` 组装。对标 Go 库不抢 `http.DefaultServeMux`、不强制全局 prometheus Registerer（尽量可注入）。

**解答：**
```text
library: metrics::counter!("...") / tracing::info!(...)
binary:  metrics exporter + tracing subscriber + otel provider
```

```rust
fn main() {
    println!("same rule as 39: libs don't init logging");
}
```

**Go 对比：**
- 同样分层。
- **Go 程序员易踩的坑**：库里 `MustRegister` 全局指标导致测试冲突。

**记忆点：**
- 库埋点；应用接线。
- 测试可换 Noop exporter。

---

## Q12. 落地检查清单（Go 迁 Rust 服务） {#q12}
**Tags:** `common` `checklist`
**适用版本:** 上线前

**一句话答案：**
先有 RED 指标 + `/metrics`，再有结构化日志与 `trace_id`，最后接 OTLP。别一上来全链路平台化却没有基本 counter。

**解答：**
```text
[ ] http_requests_total + latency histogram
[ ] /metrics 可 scrape
[ ] RUST_LOG 结构化
[ ] 入站/出站传播 traceparent
[ ] readiness 与关停
[ ] 高基数 label 审查
[ ] 库不 init 全局
```

```rust
fn main() {
    println!("metrics first, otel when the team is ready");
}
```

**记忆点：**
- 指标 → 日志关联 → 分布式追踪。
- 本篇 + 39 + 49 + 51 组成可观测全家桶。
