+++
title = "第7章 插槽（Slots）"
weight = 70
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第七章 插槽（Slots）

> 如果说 Props 是给组件"喂数据"，那插槽就是给组件"喂 UI"。插槽是 Vue 最独特的特性之一——它允许你在父组件里定义子组件的部分内容，让组件变得极度灵活和可复用。学完这一章，你会对"组件不仅仅是标签，更是可塑的容器"这句话有全新的理解。

## 7.1 插槽的基本用法

在正式进入插槽的世界之前，让我们先思考一个问题：为什么需要插槽？

想象你去一家奶茶店点单。如果你只告诉店员"我要一杯奶茶"，店员还得追问"要几分糖？什么温度？加不加料？"——这就像组件只有 Props，每次都得传一堆参数。但如果店员说"我们这有三种杯型可选，您自己选一个"，这就是插槽的思路——把"填充内容"的权力交给使用者。

**插槽就是 Vue 提供的一种"让父组件决定子组件内部长什么样"的机制。**

```vue
<!-- 子组件：Card.vue -->
<script setup lang="ts">
</script>

<template>
  <div class="card">
    <!-- <slot> 是占位符，父组件传过来的内容会渲染在这里 -->
    <slot></slot>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background: white;
}
</style>
```

```vue
<!-- 父组件：使用插槽 -->
<script setup>
import Card from './Card.vue'
</script>

<template>
  <Card>
    <!-- 这里的内容会渲染到子组件的 <slot> 位置 -->
    <h2>我叫小明</h2>
    <p>我是一名前端工程师</p>
  </Card>
</template>
```

渲染出来的实际 HTML 结构是：

```html
<div class="card">
  <h2>我叫小明</h2>
  <p>我是一名前端工程师</p>
</div>
```

这就是插槽的魔力——`Card` 组件负责"外壳"（边框、内边距、背景色），父组件负责"内容"（标题和描述）。一个负责"形"，一个负责"神"，各司其职。

## 7.2 默认插槽

默认插槽就是没有命名的那种插槽——子组件里写一个 `<slot>`，父组件里直接往子组件标签里塞内容就行了。

```vue
<!-- 子组件：Alert.vue -->
<template>
  <div class="alert" :class="`alert-${type}`">
    <slot></slot>
  </div>
</template>
```

```vue
<!-- 父组件：直接往 Alert 标签里塞内容 -->
<Alert type="warning">
  <strong>注意！</strong> 您的账户余额不足，请及时充值。
</Alert>
```

如果父组件没有往插槽里传任何内容，插槽会显示**后备内容（fallback content）**——这是子组件在 `<slot>` 标签里写的默认内容：

```vue
<!-- 子组件：Button.vue -->
<template>
  <button class="btn">
    <!-- 如果父组件没传内容，就显示"默认按钮" -->
    <slot>默认按钮</slot>
  </button>
</template>
```

```vue
<!-- 父组件：不传内容，使用后备内容 -->
<MyButton />  <!-- 显示"默认按钮" -->

<!-- 父组件：传了内容，覆盖后备内容 -->
<MyButton>点我</MyButton>  <!-- 显示"点我" -->
```

这个后备内容的机制非常有用——它让组件有了"合理的默认值"，使用者不传内容时也不会出现空白。

## 7.3 具名插槽

### 7.3.1 v-slot 缩写（#）

当一个组件有**多个插槽**时，就需要给每个插槽起个名字来区分——这就是**具名插槽**。

```vue
<!-- 子组件：BaseLayout.vue -->
<template>
  <div class="layout">
    <header>
      <!-- 具名插槽：name="header" -->
      <slot name="header"></slot>
    </header>

    <main>
      <!-- 默认插槽（没有 name 属性，就是默认插槽） -->
      <slot></slot>
    </main>

    <footer>
      <!-- 具名插槽：name="footer" -->
      <slot name="footer"></slot>
    </footer>
  </div>
</template>
```

```vue
<!-- 父组件：用 v-slot 指令往具名插槽里传内容 -->
<BaseLayout>
  <!-- v-slot:插槽名 的简写是 #插槽名 -->
  <template v-slot:header>
    <h1>网站标题</h1>
    <nav>导航菜单</nav>
  </template>

  <!-- 默认插槽的内容直接写在父组件的子组件标签里 -->
  <p>这是主要内容区域</p>

  <template #footer>
    <p>版权所有 2024</p>
  </template>
</BaseLayout>
```

**`#` 是 `v-slot:` 的简写**，两者完全等价。`v-slot:header` 等于 `#header`，`v-slot:default` 等于 `#default`（默认插槽）。

### 7.3.2 动态插槽名

Vue 3 支持**动态插槽名**——插槽名可以用变量来指定。这在封装一些"通用布局组件"时特别有用。

```vue
<!-- 子组件：Panel.vue -->
<template>
  <div class="panel">
    <slot name="title"></slot>
    <div class="panel-body">
      <slot name="content"></slot>
    </div>
    <slot name="footer"></slot>
  </div>
</template>
```

```vue
<!-- 父组件：用变量指定插槽名 -->
<script setup>
const panelSlot = ref('title')
</script>

<template>
  <Panel>
    <template #[panelSlot]>
      <h2>动态插槽内容</h2>
    </template>
  </Panel>
</template>
```

`#[panelSlot]` 是 `v-slot:[panelSlot]` 的缩写——当 `panelSlot` 的值是 `'title'` 时，就等于 `#title`。这个语法在实际业务中可能用得不多，但在做"插槽名可配置"的通用组件时会派上用场。

## 7.4 作用域插槽

### 7.4.1 父组件访问子组件数据

普通插槽的内容是**父组件决定的**，但有时候子组件需要把自己内部的数据也传给插槽——让父组件在决定内容长什么样的同时，也能用到子组件的数据。这就是**作用域插槽**。

举一个经典的例子：渲染一个列表，子组件负责获取和处理数据，父组件负责决定每一条数据渲染成什么样子。

```vue
<!-- 子组件：ArticleList.vue -->
<script setup lang="ts">
import { ref } from 'vue'

const articles = ref([
  { id: 1, title: 'Vue 3 入门', views: 1000, author: '小明' },
  { id: 2, title: 'TypeScript 进阶', views: 2000, author: '李四' },
  { id: 3, title: 'Vite 性能优化', views: 500, author: '王五' }
])
</script>

<template>
  <div class="article-list">
    <!-- 向父组件暴露 articles 数据 -->
    <!-- 父组件可以在插槽内容里使用这些数据 -->
    <slot :articles="articles" :total="articles.length"></slot>
  </div>
</template>
```

```vue
<!-- 父组件：使用子组件暴露的数据，决定渲染方式 -->
<ArticleList v-slot="{ articles, total }">
  <!-- articles 和 total 是子组件通过 slot prop 传过来的 -->
  <p>共 {{ total }} 篇文章：</p>
  <div v-for="article in articles" :key="article.id" class="article-item">
    <h3>{{ article.title }}</h3>
    <span>作者：{{ article.author }}</span>
    <span>阅读：{{ article.views }}</span>
  </div>
</ArticleList>
```

`v-slot` 的默认 slot prop 是 `{ articles, total }` ——这两个数据是子组件通过 `:articles="articles"` 和 `:total="articles.length"` 传给插槽的。父组件可以在插槽内容里使用这些数据，决定渲染的样式。

### 7.4.2 解构插槽 Prop

作用域插槽的 slot prop（也就是子组件通过 `<slot :xxx="yyy">` 传过来的数据）是一个对象。如果不想用完整对象，可以直接**解构**：

```vue
<!-- 解构前 -->
<ArticleList v-slot="{ articles, total }">
  <p>共 {{ total }} 篇文章</p>
</ArticleList>

<!-- 解构后：用更语义化的变量名 -->
<ArticleList v-slot="{ articles: articleList, total: articleCount }">
  <p>共 {{ articleCount }} 篇文章</p>
</ArticleList>
```

作用域插槽是 Vue 最强大的特性之一，它让"**子组件提供数据，父组件决定样式**"成为可能——两者各司其职，又紧密配合。

## 7.5 插槽的默认值（fallback content）

前面提到了后备内容，这是子组件在 `<slot>` 标签里写的默认内容。插槽的后备内容会在**父组件没有传内容时**显示。

```vue
<!-- 子组件：Badge.vue -->
<template>
  <span class="badge">
    <slot name="icon"></slot>
    <!-- icon 插槽的后备内容 -->
    <slot name="label">标签</slot>
  </span>
</template>
```

```vue
<!-- 父组件 -->
<Badge>
  <!-- 只传了 label，没传 icon —— icon 会显示后备内容 -->
  <template #label>新消息</template>
</Badge>
<!-- 显示：<span class="badge">标签新消息</span> -->
```

后备内容让组件在"使用者没传内容"时也能优雅地展示，不至于留白。

## 7.6 插槽的编译作用域

插槽内容是在**父组件的作用域**里编译的，意思是说：模板里能访问什么数据，由**定义插槽内容的组件**（父组件）决定，而不是子组件。

```vue
<script setup>
import { ref } from 'vue'

const userName = ref('小明')  // 父组件自己定义的数据
</script>

<template>
  <ChildComponent>
    <!-- 这里能访问 userName，因为这段内容在父组件里编译 -->
    <p>用户名：{{ userName }}</p>

    <!-- 这里不能用 ChildComponent 里的数据 -->
    <!-- {{ childData }} —— 如果 childData 是 ChildComponent 里定义的，这里访问不到 -->
  </ChildComponent>
</template>
```

反过来，作用域插槽可以让**子组件的数据**流入**父组件的插槽内容**，从而让父组件在编译时能访问到子组件的数据——这就是作用域插槽的核心原理。

## 7.7 实战：插槽设计模式

### 7.7.1 布局插槽（Header / Body / Footer）

插槽最经典的应用就是**布局组件**——组件提供页面的骨架，使用者填充各个区域的内容。

```vue
<!-- 子组件：AppLayout.vue —— 提供"三明治"布局骨架 -->
<template>
  <div class="app-layout">
    <header class="layout-header">
      <slot name="header">
        <!-- 默认 header 区域的内容 -->
        <h1>默认标题</h1>
      </slot>
    </header>

    <aside class="layout-sidebar">
      <slot name="sidebar">
        <!-- 默认 sidebar 区域 -->
        <p>默认侧边栏</p>
      </slot>
    </aside>

    <main class="layout-main">
      <slot></slot>  <!-- 默认插槽：主内容区 -->
    </main>

    <footer class="layout-footer">
      <slot name="footer">
        <p>&copy; 2024 默认页脚</p>
      </slot>
    </footer>
  </div>
</template>

<style scoped>
.app-layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 250px 1fr;
  min-height: 100vh;
}

.layout-header { grid-area: header; background: #42b883; color: white; padding: 16px; }
.layout-sidebar { grid-area: sidebar; background: #f5f5f5; padding: 16px; }
.layout-main { grid-area: main; padding: 16px; overflow-y: auto; }
.layout-footer { grid-area: footer; background: #333; color: white; padding: 12px; }
</style>
```

```vue
<!-- 父组件：填充各个区域 -->
<AppLayout>
  <template #header>
    <div class="header-content">
      <h1>我的博客</h1>
      <nav>
        <a href="/">首页</a>
        <a href="/about">关于</a>
        <a href="/archive">归档</a>
      </nav>
    </div>
  </template>

  <template #sidebar>
    <UserProfileCard />
    <TagCloud />
    <RecentComments />
  </template>

  <!-- 主内容区用默认插槽 -->
  <ArticleList />
  <Pagination />

  <template #footer>
    <div class="footer-content">
      <p>Powered by Vue 3 + Vite</p>
      <p>联系我：hello@example.com</p>
    </div>
  </template>
</AppLayout>
```

这样，`AppLayout` 组件封装了页面结构（header、sidebar、main、footer），父组件只需要填充各个区域的具体内容。这种"结构与内容分离"的模式是插槽最常见的使用场景之一。

### 7.7.2 表格列插槽

另一个经典的插槽应用场景是**可配置的表格组件**——表格的整体结构（表头、表格行、底部分页栏）是固定的，但每一列的渲染方式是由使用者决定的。

```vue
<!-- 子组件：DataTable.vue -->
<script setup lang="ts" generic="T">
import { ref } from 'vue'

defineProps<{
  data: T[]
  loading?: boolean
}>()

// 定义列的配置，每列有 name（列名）、key（数据字段）、slot（对应的插槽名）
const columns = [
  { name: 'ID', key: 'id', slot: 'col-id' },
  { name: '标题', key: 'title', slot: 'col-title' },
  { name: '状态', key: 'status', slot: 'col-status' },
  { name: '操作', slot: 'col-actions' }
]
</script>

<template>
  <div class="data-table">
    <table>
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">{{ col.name }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="columns.length" class="loading-cell">加载中...</td>
        </tr>
        <tr v-else v-for="(row, index) in data" :key="row.id || index">
          <td v-for="col in columns" :key="col.key">
            <!-- 作用域插槽：向父组件暴露整行数据 -->
            <slot :name="col.slot" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

```vue
<!-- 父组件：决定每一列怎么渲染 -->
<script setup lang="ts">
import { ref } from 'vue'
import DataTable from './DataTable.vue'

const articles = ref([
  { id: 1, title: 'Vue 3 入门指南', status: 'published', views: 1000 },
  { id: 2, title: 'TypeScript 完全指南', status: 'draft', views: 500 },
  { id: 3, title: 'Vite 性能优化', status: 'published', views: 2000 }
])
</script>

<template>
  <DataTable :data="articles" :loading="false">
    <!-- 自定义 ID 列的渲染 -->
    <template #col-id="{ row }">
      <code>#{{ row.id }}</code>
    </template>

    <!-- 自定义标题列的渲染 -->
    <template #col-title="{ row }">
      <a :href="`/article/${row.id}`">{{ row.title }}</a>
    </template>

    <!-- 自定义状态列的渲染 -->
    <template #col-status="{ value }">
      <span :class="['status-badge', `status-${value}`]">
        {{ value === 'published' ? '已发布' : '草稿' }}
      </span>
    </template>

    <!-- 自定义操作列 -->
    <template #col-actions="{ row }">
      <button @click="editArticle(row.id)">编辑</button>
      <button @click="deleteArticle(row.id)">删除</button>
    </template>
  </DataTable>
</template>
```

这就是一个典型的"配置化表格"模式——`DataTable` 负责数据遍历、loading 状态、分页等通用逻辑，使用者只需要关心"每一列怎么渲染"这个局部问题。相关逻辑内聚，通用逻辑复用，分工明确。

### 7.7.3 表单插槽

表单组件也经常用到插槽——一个通用的表单容器组件，负责整体布局、验证提示、提交按钮等通用逻辑，使用者在里面填充具体的表单项。

```vue
<!-- 子组件：SmartForm.vue -->
<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', values: Record<string, unknown>): void
}>()

const values = ref<Record<string, unknown>>({})
const errors = ref<Record<string, string>>({})

function setFieldValue(field: string, value: unknown) {
  values.value[field] = value
  // 清除错误
  if (errors.value[field]) {
    delete errors.value[field]
  }
}

function handleSubmit() {
  emit('submit', values.value)
}

defineExpose({ setFieldValue })
</script>

<template>
  <form class="smart-form" @submit.prevent="handleSubmit">
    <!-- 作用域插槽：向父组件暴露 setFieldValue 方法和当前值 -->
    <slot :values="values" :errors="errors" :setFieldValue="setFieldValue" />

    <div class="form-actions">
      <button type="button" @click="$emit('cancel')">取消</button>
      <button type="submit" class="primary">提交</button>
    </div>
  </form>
</template>
```

```vue
<!-- 父组件 -->
<SmartForm @submit="handleSubmit" @cancel="handleCancel" #default="{ values, errors, setFieldValue }">
  <!-- 用户名 -->
  <div class="form-field">
    <label>用户名</label>
    <input
      type="text"
      :value="values.username"
      @input="setFieldValue('username', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="errors.username" class="error">{{ errors.username }}</span>
  </div>

  <!-- 邮箱 -->
  <div class="form-field">
    <label>邮箱</label>
    <input
      type="email"
      :value="values.email"
      @input="setFieldValue('email', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="errors.email" class="error">{{ errors.email }}</span>
  </div>
</SmartForm>
```

---

## 本章小结

本章我们深入学习了 Vue 的插槽系统：

- **插槽是什么**：父组件向子组件传递"UI 结构"的方式，子组件用 `<slot>` 占位，父组件用 `<template v-slot>` 或 `#` 往里填内容。
- **默认插槽**：没有 name 属性的插槽，内容直接写在子组件标签里。
- **具名插槽**：通过 name 区分的多个插槽，用 `v-slot:name` 或 `#name` 指定内容。
- **作用域插槽**：子组件通过 slot prop 向父组件暴露内部数据，父组件在决定 UI 的同时能用上这些数据。
- **后备内容**：`<slot>` 标签里的默认内容，父组件不传时显示。
- **编译作用域**：插槽内容在父组件编译，能访问父组件的数据；作用域插槽让子组件数据流入父组件的插槽内容。
- **实战设计模式**：布局插槽（Header/Body/Footer）、表格列插槽、表单插槽——都是插槽最经典的应用场景。

下一章我们会学习 Vue 的**高级组件特性**——动态组件、KeepAlive 缓存、异步组件、Teleport、$attrs、递归组件和依赖注入。这些是 Vue 组件化开发中的"高级武器"，掌握了它们，你能构建出更复杂的应用架构！

