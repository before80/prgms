+++
title = "第34章 React与AI"
weight = 340
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-34 - React 与 AI

## 34.1 AI API 集成

### 34.1.1 OpenAI API 的基本调用

**React + AI 可以做什么？** 这是个开放问题，答案很多：
- **AI 聊天机器人**：像 ChatGPT 一样的对话界面
- **内容生成**：输入标题 AI 生成文章、输入描述生成图片
- **智能客服**：理解用户问题，自动回复或转人工
- **代码助手**：解释代码、debug、生成代码
- **多模态**：输入图片+文字，AI 理解图片内容

本质上，AI API 让 React 应用有了"理解"和"生成"的能力——不只是展示静态内容，而是能对话、能思考、能创造。

下面来看怎么接入。

```bash
npm install openai
```

```javascript
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY
})

async function generateText(prompt) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 500
  })

  return response.choices[0].message.content
}
```

### 34.1.2 Anthropic Claude API 集成

```javascript
async function chatWithClaude(messages) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': import.meta.env.VITE_ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-3-sonnet',
      max_tokens: 1024,
      messages
    })
  })

  return response.json()
}
```

### 34.1.3 流式响应（Streaming）：Server-Sent Events

```javascript
async function* streamChat(prompt) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      stream: true
    })
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value)
    const lines = chunk.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data !== '[DONE]') {
          yield JSON.parse(data).choices[0].delta.content
        }
      }
    }
  }
}
```

---

## 34.2 React 中的 AI 集成

### 34.2.1 流式响应的 React 实现

```jsx
import { useState } from 'react'
// streamChat 是 34.1.3 节定义的生成器函数
// import { streamChat } from './api/chat'

function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!input.trim()) return

    setStreaming(true)
    setMessages(prev => [...prev, { role: 'user', content: input }])
    setInput('')

    const response = []
    for await (const chunk of streamChat(input)) {
      response.push(chunk)
      // 每次收到新的 chunk，就更新最后一条消息（打字机效果）
      setMessages(prev => {
        const last = prev[prev.length - 1]
        return [...prev.slice(0, -1), { role: 'assistant', content: response.join('') }]
      })
    }

    setStreaming(false)
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={m.role}>{m.content}</div>
        ))}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} disabled={streaming} />
      <button type="submit" disabled={streaming}>发送</button>
    </form>
  )
}
```

### 34.2.2 AI 对话组件的设计

```jsx
function AIChatbot() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  async function sendMessage(content) {
    setIsLoading(true)
    setMessages(prev => [...prev, { role: 'user', content }])

    try {
      const response = await generateText(content)
      setMessages(prev => [...prev, { role: 'assistant', content: response }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'error', content: '请求失败' }])
    }

    setIsLoading(false)
  }

  return <ChatInterface messages={messages} onSend={sendMessage} isLoading={isLoading} />
}
```

### 34.2.3 多模态输入：图片 + 文本

```javascript
async function multimodal(input, imageBase64) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4-vision-preview',
    messages: [{
      role: 'user',
      content: [
        { type: 'text', text: input },
        { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${imageBase64}` }}
      ]
    }]
  })

  return response.choices[0].message.content
}
```

---

## 34.3 前端 prompt 工程

### 34.3.1 Prompt 模板设计

**Prompt 工程**不是 AI 领域独有的概念——在前端场景中，它本质上是你给 AI 设定"行为规则"和"上下文"的方式。常见的做法是设计一个 `systemPrompt`（系统提示词）作为"首席指挥官"，再把用户问题拼在后面发给 AI。

```javascript
const systemPrompt = `你是一个专业的React开发助手。
请用简洁的语言回答问题，并在适当时机给出代码示例。`

async function ask(question) {
  return generateText(`${systemPrompt}\n\n用户问题：${question}`)
}
```

### 34.3.2 Few-shot 示例

**Few-shot**（少样本）是一种让 AI"照着例子学"的技巧——在提示词里给几个输入-输出示例，AI 会模仿这些示例的风格或逻辑来回答。适合任务格式固定但变化多端的场景（如翻译、分类、格式化输出）。

```javascript
const fewShotPrompt = `将以下英语翻译成中文：

示例：
输入：Hello, world!
输出：你好，世界！

输入：The quick brown fox jumps over the lazy dog.
输出：`
```

---

## 本章小结

本章我们探索了 React 与 AI 的结合：

- **AI API 集成**：OpenAI API、Anthropic Claude API 的基本调用
- **流式响应**：Server-Sent Events 实现打字机效果
- **React 中的 AI 集成**：聊天组件设计、流式响应实现
- **Prompt 工程**：系统提示词、Few-shot 示例

AI 时代，React 与 AI 的结合是大势所趋！下一章我们将学习 **跨平台桌面开发**！🖥️