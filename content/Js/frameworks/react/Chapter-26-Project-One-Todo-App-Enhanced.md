+++
title = "第26章 项目一——Todo App增强版"
weight = 260
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-26 - 项目一——Todo App 增强版

## 26.1 项目需求分析与结构设计

### 26.1.1 功能列表：增删改查、筛选、分类、持久化

一个完整的 Todo App 增强版不只是"能记事情"这么简单——它要像一个小型的效率工具，让用户感受到"我在掌控我的任务"。

**核心 CRUD** 是根基：添加任务不用多说；删除任务要考虑"误删怎么办"，可以加个确认；编辑任务最自然的交互是双击进入编辑状态；完成任务则是点击复选框，给用户一种"划掉"的满足感。

**筛选和分类**是让 Todo App 从"能用"到"好用"的关键。当任务多了之后，用户不想每次都看到所有任务——"只看没完成的"是最常见需求，所以至少要有全部/已完成/未完成三档筛选。如果再加上按标签分类，就更有组织性了。

**本地持久化（localStorage）** 让数据不丢失——页面刷新甚至关掉浏览器，下次打开任务还在。这不需要后端，一个浏览器内置 API 就够了，是纯前端项目练手的完美选择。

**拖拽排序**是加分项，让用户可以自由调整任务优先级，把最重要的拖到最上面。这需要用到 `@dnd-kit` 或 `react-beautiful-dnd` 等库。

### 26.1.2 目录结构设计

```
src/
├── features/
│   └── todos/
│       ├── components/
│       │   ├── TodoItem.jsx
│       │   ├── TodoList.jsx
│       │   ├── TodoForm.jsx
│       │   ├── TodoFilter.jsx
│       │   └── TodoStats.jsx
│       ├── hooks/
│       │   └── useTodos.js
│       ├── stores/
│       │   └── todoStore.js
│       └── types/
│           └── index.js
├── App.jsx
└── main.jsx
```

### 26.1.3 技术选型：纯 React vs + 状态管理

| 方案 | 适用场景 |
|------|---------|
| 纯 useState + useReducer | 简单 Todo |
| Zustand | 中等复杂度 |
| Redux Toolkit | 大型应用 |

---

## 26.2 组件划分

### 26.2.1 组件拆分方案

```
TodoApp (根组件)
├── TodoHeader
├── TodoForm (添加表单)
├── TodoFilter (筛选器)
├── TodoList (列表容器)
│   └── TodoItem (单个任务项)
│       ├── TodoCheckbox
│       ├── TodoText
│       └── TodoActions
└── TodoStats (统计)
```

### 26.2.2 TodoItem / TodoList / TodoForm / TodoFilter 组件设计

```jsx
// TodoItem 组件
function TodoItem({ todo, onToggle, onDelete, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false)
  const [editText, setEditText] = useState(todo.text)

  function handleDoubleClick() {
    setIsEditing(true)
  }

  function handleSave() {
    onUpdate(todo.id, { text: editText })
    setIsEditing(false)
  }

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />

      {isEditing ? (
        <input
          value={editText}
          onChange={e => setEditText(e.target.value)}
          onBlur={handleSave}
          onKeyDown={e => { if (e.key === 'Enter') handleSave() }}
          autoFocus
        />
      ) : (
        <span onDoubleClick={handleDoubleClick}>{todo.text}</span>
      )}

      <button onClick={() => onDelete(todo.id)}>删除</button>
    </div>
  )
}
```

### 26.2.3 目录组织：feature-based 结构

```javascript
// features/todos/store/todoStore.js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useTodoStore = create(
  persist(
    (set, get) => ({
      todos: [],

      addTodo: (text) => set(state => ({
        todos: [
          ...state.todos,
          {
            id: Date.now(),
            text,
            completed: false,
            createdAt: new Date().toISOString()
          }
        ]
      })),

      toggleTodo: (id) => set(state => ({
        todos: state.todos.map(t =>
          t.id === id ? { ...t, completed: !t.completed } : t
        )
      })),

      deleteTodo: (id) => set(state => ({
        todos: state.todos.filter(t => t.id !== id)
      })),

      updateTodo: (id, updates) => set(state => ({
        todos: state.todos.map(t =>
          t.id === id ? { ...t, ...updates } : t
        )
      })),

      clearCompleted: () => set(state => ({
        todos: state.todos.filter(t => !t.completed)
      }))
    }),
    { name: 'todo-storage' }
  )
)
```

---

## 26.3 状态管理

### 26.3.1 纯 useState 方案

```jsx
function useTodos() {
  const [todos, setTodos] = useState([])

  const addTodo = (text) => {
    setTodos(prev => [...prev, { id: Date.now(), text, completed: false }])
  }

  const toggleTodo = (id) => {
    setTodos(prev =>
      prev.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
    )
  }

  return { todos, addTodo, toggleTodo }
}
```

### 26.3.2 useReducer 方案

```jsx
const todoReducer = (state, action) => {
  switch (action.type) {
    case 'ADD':
      return [...state, action.payload]
    case 'TOGGLE':
      return state.map(t =>
        t.id === action.payload.id ? { ...t, completed: !t.completed } : t
      )
    case 'DELETE':
      return state.filter(t => t.id !== action.payload.id)
    default:
      return state
  }
}

function useTodosReducer() {
  const [todos, dispatch] = useReducer(todoReducer, [])

  return {
    todos,
    addTodo: (text) => dispatch({ type: 'ADD', payload: { id: Date.now(), text, completed: false } }),
    toggleTodo: (id) => dispatch({ type: 'TOGGLE', payload: { id } }),
    deleteTodo: (id) => dispatch({ type: 'DELETE', payload: { id } })
  }
}
```

### 26.3.3 本地持久化：useLocalStorage 自定义 Hook

```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value) => {
    try {
      setStoredValue(value)
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('localStorage 写入失败:', error)
    }
  }

  return [storedValue, setValue]
}
```

---

## 26.4 样式实现

### 26.4.1 Tailwind CSS 实现

```jsx
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <div className={`flex items-center gap-3 p-3 rounded-lg ${todo.completed ? 'bg-gray-100' : 'bg-white'}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        className="w-5 h-5 rounded text-blue-500"
      />

      <span className={`flex-1 ${todo.completed ? 'line-through text-gray-400' : 'text-gray-800'}`}>
        {todo.text}
      </span>

      <button
        onClick={() => onDelete(todo.id)}
        className="px-3 py-1 text-sm text-red-500 hover:bg-red-50 rounded"
      >
        删除
      </button>
    </div>
  )
}
```

### 26.4.2 响应式设计

```jsx
function TodoApp() {
  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">Todo App</h1>

      {/* 移动端和桌面端自适应 */}
      <div className="block sm:hidden">
        <p>移动端布局</p>
      </div>

      <div className="hidden sm:block">
        <p>桌面端布局</p>
      </div>
    </div>
  )
}
```

---

## 26.5 功能迭代

### 26.5.1 筛选功能：全部 / 已完成 / 未完成 / 分类

```jsx
function TodoFilter({ filter, onFilterChange, categories }) {
  return (
    <div className="flex gap-2 mb-4">
      {['all', 'active', 'completed'].map(f => (
        <button
          key={f}
          onClick={() => onFilterChange(f)}
          className={`px-3 py-1 rounded ${filter === f ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          {f === 'all' ? '全部' : f === 'active' ? '未完成' : '已完成'}
        </button>
      ))}
    </div>
  )
}

function useFilteredTodos(todos, filter) {
  return useMemo(() => {
    switch (filter) {
      case 'active':
        return todos.filter(t => !t.completed)
      case 'completed':
        return todos.filter(t => t.completed)
      default:
        return todos
    }
  }, [todos, filter])
}
```

### 26.5.2 编辑功能：双击编辑

```jsx
function TodoItem({ todo, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false)
  const [editText, setEditText] = useState(todo.text)

  function handleSave() {
    if (editText.trim()) {
      onUpdate(todo.id, { text: editText.trim() })
    }
    setIsEditing(false)
  }

  return (
    <div onDoubleClick={() => !todo.completed && setIsEditing(true)}>
      {isEditing ? (
        <input
          value={editText}
          onChange={e => setEditText(e.target.value)}
          onBlur={handleSave}
          onKeyDown={e => { if (e.key === 'Enter') handleSave() }}
          className="border border-blue-500 px-2 py-1 rounded"
        />
      ) : (
        <span>{todo.text}</span>
      )}
    </div>
  )
}
```

### 26.5.3 批量操作：全选、批量删除

```jsx
function TodoList({ todos, onToggle, onDelete }) {
  const allCompleted = todos.length > 0 && todos.every(t => t.completed)

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={allCompleted}
          onChange={() => {
            if (!allCompleted) {
              todos.forEach(t => !t.completed && onToggle(t.id))
            } else {
              todos.forEach(t => t.completed && onToggle(t.id))
            }
          }}
        />
        全选
      </label>

      {todos.map(todo => (
        <TodoItem key={todo.id} todo={todo} onToggle={onToggle} onDelete={onDelete} />
      ))}
    </div>
  )
}
```

### 26.5.4 拖拽排序

拖拽排序推荐使用 `@dnd-kit`，它比 `react-beautiful-dnd` 更轻量、兼容性更好，且支持更多场景。

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

```jsx
import { useState } from 'react'
import {
  DndContext,           // DnD 上下文，包裹整个列表
  closestCenter         // 拖拽对齐算法：找到最近的中心点
} from '@dnd-kit/core'
import {
  SortableContext,              // 包裹可排序列表
  verticalListSortingStrategy, // 列表纵向排序策略
  useSortable                  // 让一个元素变成可拖拽的
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

// --------------------------------------------------
// 单个可拖拽的任务项
// --------------------------------------------------
function SortableItem({ todo, onDelete }) {
  // useSortable：让这个 div 变为可拖拽元素
  // id 必须唯一，dnd-kit 用它来追踪是哪个元素被拖拽
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
    id: todo.id
  })

  // transform：拖拽过程中的位移（CSS transform 值），需要用 CSS.Transform.toString() 转换
  // transition：松手后的动画过渡
  const style = {
    transform: CSS.Transform.toString(transform),
    transition
  }

  return (
    // setNodeRef：注册 DOM 引用，dnd-kit 需要它来获取元素位置
    // {...attributes} 和 {...listeners}：包含拖拽所需的事件（onPointerDown 等），要展开到元素上
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {todo.text}
      <button onClick={() => onDelete(todo.id)}>删除</button>
    </div>
  )
}

// --------------------------------------------------
// 拖拽列表容器（父组件）
// --------------------------------------------------
function TodoList({ todos, onDelete, onReorder }) {
  const [activeId, setActiveId] = useState(null)

  function handleDragEnd(event) {
    // event.active：被拖拽的元素
    // event.over：当前鼠标位置下的目标元素
    const { active, over } = event

    if (active.id !== over?.id) {
      // 找到了新位置，调用 onReorder 更新顺序
      const oldIndex = todos.findIndex(t => t.id === active.id)
      const newIndex = todos.findIndex(t => t.id === over.id)
      onReorder(oldIndex, newIndex)
    }
    setActiveId(null)
  }

  return (
    // DndContext：必须包裹整个可拖拽列表
    // onDragEnd：拖拽结束时触发，在此计算新顺序
    <DndContext
      collisionDetection={closestCenter}
      onDragStart={({ active }) => setActiveId(active.id)}
      onDragEnd={handleDragEnd}
    >
      {/* SortableContext：管理列表中所有可排序项
          items：所有项的 id 数组，dnd-kit 据此知道有多少项需要管理
          strategy：指定排序策略（纵向列表用 verticalListSortingStrategy） */}
      <SortableContext
        items={todos.map(t => t.id)}
        strategy={verticalListSortingStrategy}
      >
        {todos.map(todo => (
          <SortableItem key={todo.id} todo={todo} onDelete={onDelete} />
        ))}
      </SortableContext>
    </DndContext>
  )
}
```

---

## 26.6 部署上线

### 26.6.1 Vercel / Netlify 免费部署

**Vercel 部署（推荐）：**

```bash
# 1. GitHub 上创建仓库
# 2. 登录 vercel.com
# 3. 点击 "New Project"
# 4. 选择 GitHub 仓库
# 5. 点击 "Deploy"
# 自动构建并部署！
```

**Netlify 部署：**

```bash
# 1. GitHub 上创建仓库
# 2. 登录 netlify.com
# 3. 点击 "Add new site" -> "Import from Git"
# 4. 选择 GitHub 仓库
# 5. 构建命令留空或填 npm run build
# 6. 发布目录填 dist
```

### 26.6.2 自动化部署配置

在 GitHub 仓库设置中配置：
- Branch: `main`
- Build Command: `npm run build`
- Output Directory: `dist`

每次 push 到 main 分支，自动触发构建和部署！

---

## 本章小结

本章我们完整实现了一个 Todo App 增强版项目：

- **功能完整**：增删改查、筛选、分类、持久化、批量操作
- **组件设计**：清晰的组件拆分，从根组件到原子组件
- **状态管理**：useReducer 方案作为演示，Zustand + persist 是更优方案
- **样式**：Tailwind CSS 实现响应式设计
- **部署**：Vercel/Netlify 免费一键部署

这是一个很好的入门实战项目！下一章我们将实现一个更复杂的 **社交类应用**！💬