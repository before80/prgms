+++
title = "HTTP 状态码"
date = 2026-04-18T11:30:20+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

## 📊 HTTP 状态码完整速查表（RFC 9110 标准版）

> 🔍 **图例**：`✅` 核心标准｜`🌐` WebDAV/协议扩展｜`⚠️` 已废弃/保留｜`🔬` 实验性｜`📉` 极少使用/历史遗留

###  1xx 信息性（Informational）
| 状态码 | 英文名称            | 中文译名 | 标准来源 | 核心说明与典型场景                                    |
| ------ | ------------------- | -------- | -------- | ----------------------------------------------------- |
| `100`  | Continue            | 继续     | RFC 9110 | 客户端应继续发送请求体（配合 `Expect: 100-continue`） |
| `101`  | Switching Protocols | 切换协议 | RFC 9110 | 服务器同意升级协议（如 `Upgrade: websocket`）         |
| `102`  | Processing          | 处理中   | RFC 4918 | WebDAV 扩展，防代理/客户端超时，需异步返回进度        |
| `103`  | Early Hints         | 早期提示 | RFC 8297 | 在完整响应前预加载关键资源（如 `<link rel=preload>`） |

### 2xx 成功（Success）
| 状态码 | 英文名称                      | 中文译名       | 标准来源 | 核心说明与典型场景                                 |
| ------ | ----------------------------- | -------------- | -------- | -------------------------------------------------- |
| `200`  | OK                            | 成功           | RFC 9110 | 请求成功，响应体含结果（GET/POST/PUT 默认）        |
| `201`  | Created                       | 已创建         | RFC 9110 | 新资源已创建，**必须**返回 `Location` 头指向新资源 |
| `202`  | Accepted                      | 已接受         | RFC 9110 | 请求已入队异步处理，不保证最终成功（如后台任务）   |
| `203`  | Non-Authoritative Information | 非授权信息     | RFC 9110 | 响应来自中间节点（代理/缓存），非源服务器权威数据  |
| `204`  | No Content                    | 无内容         | RFC 9110 | 成功但无响应体（常用于 `DELETE`/`PUT`）            |
| `205`  | Reset Content                 | 重置内容       | RFC 9110 | 成功，要求客户端重置表单/视图（如清空输入框）      |
| `206`  | Partial Content               | 部分内容       | RFC 9110 | 范围请求成功（断点续传，需 `Content-Range`）       |
| `207`  | Multi-Status                  | 多状态         | RFC 4918 | WebDAV，XML 响应包含多个子资源独立状态             |
| `208`  | Already Reported              | 已报告         | RFC 5842 | WebDAV，集合成员已在本响应中报告，避免重复列举     |
| `226`  | IM Used                       | 实例操纵已使用 | RFC 3229 | Delta 编码/差异更新成功                            |

###  3xx 重定向（Redirection）
| 状态码 | 英文名称           | 中文译名     | 标准来源 | 核心说明与典型场景                                         |
| ------ | ------------------ | ------------ | -------- | ---------------------------------------------------------- |
| `300`  | Multiple Choices   | 多种选择     | RFC 9110 | 资源有多种表示（语言/格式），需客户端自行选择              |
| `301`  | Moved Permanently  | 永久移动     | RFC 9110 | 资源永久迁移，**SEO 权重转移**，缓存长期有效               |
| `302`  | Found              | 临时重定向   | RFC 9110 | ⚠️ 历史兼容码。浏览器**可能**将 POST 转为 GET，语义不严格   |
| `303`  | See Other          | 查看其他位置 | RFC 9110 | 明确指示用 `GET` 请求新 URI，**防表单重复提交**            |
| `304`  | Not Modified       | 未修改       | RFC 9110 | 缓存有效，不返回主体（配合 `If-None-Match` 等）            |
| `305`  | Use Proxy          | 使用代理     | RFC 9110 | ⚠️ **已废弃**，存在安全风险，现代客户端已忽略               |
| `306`  | Unused             | 未使用       | RFC 9110 | ⚠️ IANA 保留码，无定义，不应使用                            |
| `307`  | Temporary Redirect | 临时重定向   | RFC 9110 | **严格保持原请求方法**（POST→POST），替代 302 的现代标准   |
| `308`  | Permanent Redirect | 永久重定向   | RFC 9110 | **严格保持原请求方法**，替代 301 的现代标准（原 RFC 7538） |

###  4xx 客户端错误（Client Error）
| 状态码 | 英文名称                        | 中文译名         | 标准来源 | 核心说明与典型场景                                           |
| ------ | ------------------------------- | ---------------- | -------- | ------------------------------------------------------------ |
| `400`  | Bad Request                     | 错误请求         | RFC 9110 | 语法错误、参数无效、JSON/XML 解析失败                        |
| `401`  | Unauthorized                    | 未认证           | RFC 9110 | **缺少或无效凭证**，响应**必须**包含 `WWW-Authenticate` 头   |
| `402`  | Payment Required                | 需付费           | RFC 9110 | ⚠️ IANA 保留，预留给数字支付系统，极少使用                    |
| `403`  | Forbidden                       | 禁止访问         | RFC 9110 | 服务器理解请求但拒绝执行（权限不足、IP 封禁等）              |
| `404`  | Not Found                       | 未找到           | RFC 9110 | 资源不存在或 URI 路径错误                                    |
| `405`  | Method Not Allowed              | 方法不允许       | RFC 9110 | 请求方法不被支持，响应**必须**包含 `Allow` 头                |
| `406`  | Not Acceptable                  | 不可接受         | RFC 9110 | 无法提供 `Accept` 要求的媒体类型/语言/编码                   |
| `407`  | Proxy Authentication Required   | 需代理认证       | RFC 9110 | 需通过 HTTP 代理身份验证（类似 401，但针对代理）             |
| `408`  | Request Timeout                 | 请求超时         | RFC 9110 | 客户端未在服务器等待时间内完成请求                           |
| `409`  | Conflict                        | 冲突             | RFC 9110 | 请求与当前资源状态冲突（如并发修改、版本不一致）             |
| `410`  | Gone                            | 已失效           | RFC 9110 | 资源**永久删除**，客户端应移除相关缓存与链接                 |
| `411`  | Length Required                 | 需内容长度       | RFC 9110 | 缺少 `Content-Length` 头（严格模式服务器要求）               |
| `412`  | Precondition Failed             | 前置条件失败     | RFC 9110 | `If-Match`/`If-Unmodified-Since` 等条件不满足                |
| `413`  | Payload Too Large               | 请求体过大       | RFC 9110 | 原名 `Request Entity Too Large`，RFC 7231 更新               |
| `414`  | URI Too Long                    | URI 过长         | RFC 9110 | 请求 URI 超过服务器限制（通常 >2KB~8KB）                     |
| `415`  | Unsupported Media Type          | 不支持的媒体类型 | RFC 9110 | `Content-Type` 不被服务器接受                                |
| `416`  | Range Not Satisfiable           | 范围无法满足     | RFC 9110 | `Range` 头指定范围无效或超出资源大小                         |
| `417`  | Expectation Failed              | 期望失败         | RFC 9110 | `Expect` 头要求（如 `100-continue`）无法满足                 |
| `418`  | I'm a teapot                    | 我是个茶壶       | RFC 2324 | 🔬 实验性状态码，IANA 正式注册，常用于防爬虫或 API 彩蛋       |
| `421`  | Misdirected Request             | 错误定向的请求   | RFC 9110 | HTTP/2+ 中请求发往不支持该目标主机的服务器                   |
| `422`  | Unprocessable Entity            | 无法处理的实体   | RFC 9110 | ✅ **核心标准**（原 WebDAV 扩展，2022 年正式并入）。REST API 事实标准：语义/业务校验失败 |
| `423`  | Locked                          | 已锁定           | RFC 4918 | WebDAV，资源被锁定防止并发修改                               |
| `424`  | Failed Dependency               | 依赖失败         | RFC 4918 | WebDAV，因前置请求失败导致当前请求失败                       |
| `425`  | Too Early                       | 过早             | RFC 8470 | 拒绝处理可能被重放的请求（TLS 早期数据/0-RTT）               |
| `426`  | Upgrade Required                | 需升级           | RFC 9110 | 客户端需升级协议版本才能继续                                 |
| `428`  | Precondition Required           | 需前置条件       | RFC 6585 | 要求使用条件请求头防并发覆盖（常配 `If-Match`）              |
| `429`  | Too Many Requests               | 请求过多         | RFC 6585 | 限流触发，通常配合 `Retry-After` 头                          |
| `431`  | Request Header Fields Too Large | 请求头过大       | RFC 6585 | 请求头字段超过限制（如 Cookie 过大）                         |
| `451`  | Unavailable For Legal Reasons   | 因法律原因不可用 | RFC 7725 | 政府审查、版权下架、合规限制                                 |

### 5xx 服务器错误（Server Error）
| 状态码 | 英文名称                        | 中文译名        | 标准来源 | 核心说明与典型场景                                  |
| ------ | ------------------------------- | --------------- | -------- | --------------------------------------------------- |
| `500`  | Internal Server Error           | 服务器内部错误  | RFC 9110 | 通用未预料异常（代码抛异常、配置错误、依赖崩溃）    |
| `501`  | Not Implemented                 | 未实现          | RFC 9110 | 服务器不支持该请求方法                              |
| `502`  | Bad Gateway                     | 网关错误        | RFC 9110 | 反向代理/网关收到上游无效响应                       |
| `503`  | Service Unavailable             | 服务不可用      | RFC 9110 | 临时过载/维护，**建议**配合 `Retry-After`           |
| `504`  | Gateway Timeout                 | 网关超时        | RFC 9110 | 代理/网关未及时收到上游响应                         |
| `505`  | HTTP Version Not Supported      | HTTP 版本不支持 | RFC 9110 | 服务器不支持请求的 HTTP 版本                        |
| `506`  | Variant Also Negotiates         | 变体也协商      | RFC 2295 | 📉 透明内容协商循环，现代架构极少使用                |
| `507`  | Insufficient Storage            | 存储空间不足    | RFC 4918 | WebDAV，服务器无法存储资源表示（磁盘满/配额超）     |
| `508`  | Loop Detected                   | 检测到循环      | RFC 5842 | WebDAV，处理集合时检测到无限循环                    |
| `510`  | Not Extended                    | 未扩展          | RFC 2774 | 📉 已基本被现代 API 弃用                             |
| `511`  | Network Authentication Required | 需网络认证      | RFC 6585 | 拦截式门户（Captive Portal）要求登录（如酒店 WiFi） |

---
## 🛠️ 本次核心修正与最佳实践

| 易错点         | 修正说明                                                     | 工程建议                                                     |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `422` 标准归属 | 2022 年 RFC 9110 已将 `422` 从 WebDAV 提升为 **HTTP 核心标准**。 | RESTful API 参数/业务校验失败时，**优先使用 `422`** 而非 `400`，便于前后端区分“语法错误”与“语义错误”。 |
| `302` 方法转换 | RFC 9110 §15.4.3 明确：方法转换是**历史浏览器行为**，非协议强制。 | 新项目统一使用 `307`（临时）/`308`（永久）保证方法一致性，避免 POST 数据丢失。 |
| `401` 强制头   | RFC 9110 §15.5.2 规定：`401` 响应**必须**携带 `WWW-Authenticate` 挑战头。 | 未登录/Token 失效时返回 `401` 并附带 `WWW-Authenticate: Bearer` 或 `Basic`。 |
| `500` 滥用     | `500` 仅用于**未捕获的未知异常**。                           | 已知故障应使用更精准状态码：上游超时→`504`，依赖不可用→`503`，配置缺失→`501`。 |
| 云厂商私有码   | `444`, `499`, `520~527` 等**非 HTTP 标准**，仅限特定生态内部使用。 | 对外 API 严禁返回私有码；内部系统若使用需在文档中明确定义。  |

---
## 🌐 权威参考网址（官方标准）

| 资源类型                       | 链接                                                         | 说明                                                  |
| ------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------- |
| **IANA 官方注册表**            | [https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml) | 全球唯一权威来源，实时更新                            |
| **RFC 9110（HTTP Semantics）** | [https://www.rfc-editor.org/rfc/rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html) | 2022 年发布，整合并替代 RFC 7231/7235/7230 等核心语义 |
| **RFC 6585（扩展状态码）**     | [https://www.rfc-editor.org/rfc/rfc6585.html](https://www.rfc-editor.org/rfc/rfc6585.html) | `428`/`429`/`431`/`511` 来源                          |
| **RFC 4918 / 5842（WebDAV）**  | [https://www.rfc-editor.org/rfc/rfc4918.html](https://www.rfc-editor.org/rfc/rfc4918.html)<br>[https://www.rfc-editor.org/rfc/rfc5842.html](https://www.rfc-editor.org/rfc/rfc5842.html) | `102`/`207`/`208`/`423`/`424`/`507`/`508` 来源        |
| **RFC 8297（Early Hints）**    | [https://www.rfc-editor.org/rfc/rfc8297.html](https://www.rfc-editor.org/rfc/rfc8297.html) | `103` 状态码规范                                      |
| **Mozilla MDN 文档**           | [https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status) | 开发者友好解读，含浏览器兼容性说明                    |

> 💡 **提示**：所有状态码的最终解释权以 **IANA Registry** 为准。实际开发中建议结合业务网关/监控体系自定义错误码（如 `code: 10001, msg: "xxx"`），HTTP 状态码仅用于表达**传输层与协议层语义**。



