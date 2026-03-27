+++
title = "第30章 Vue 3 应用部署"
weight = 300
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十章 Vue 3 应用部署

> 代码写完了，接下来最重要的事情就是部署。本章我们将从构建分析开始，讲解如何优化打包体积、配置 Nginx、实现 Docker 容器化、集成监控告警，以及搭建完整的 CI/CD 流程。学完本章，你的应用就能从"本地玩具"变成"生产级服务"。

## 30.1 构建与资源优化

### 30.1.1 构建分析

Vite 内置了构建分析工具，可以直观地看到打包后的体积分布：

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  build: {
    // 生成打包分析报告
    rollupOptions: {
      plugins: [
        visualizer({
          filename: 'dist/stats.html',  // 分析报告输出位置
          open: true,                    // 自动打开
          gzipSize: true,                // 显示 gzip 后的大小
          brotliSize: true,              // 显示 brotli 压缩后的大小
        }),
      ],
    },
  },
})
```

```bash
# 构建后查看分析报告
npm run build
# 会在 dist/stats.html 生成可视化报告
```

### 30.1.2 优化打包体积

构建完成后，第一件事就是看"谁最肥"——哪个包的体积太大，需要优化。`vite-plugin-visualizer` 可以生成可视化报告，让你直观看到每个依赖占多大体积。针对性地优化最大的那个包，效果最明显。

**除了分析，还有这些常用优化手段：**

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  build: {
    // 目标浏览器
    target: 'es2015',
    
    // 输出路径
    outDir: 'dist',
    
    // 是否生成 sourcemap
    sourcemap: false,  // 生产环境不需要
    
    // 压缩配置
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,      // 移除 console
        drop_debugger: true,     // 移除 debugger
        pure_funcs: ['console.log'], // 移除特定函数
      },
    },
    
    // CSS 代码分割
    cssCodeSplit: true,
    
    // 动态 import 分割
    rollupOptions: {
      output: {
        // 手动分包
        manualChunks: {
          'vue-runtime': ['vue'],
          'vue-router': ['vue-router'],
          'pinia': ['pinia'],
          'vendor': ['lodash-es', 'axios'],
        },
      },
    },
    
    // 体积限制警告
    chunkSizeWarningLimit: 500,  // KB
  },
})
```

### 30.1.3 静态资源处理

静态资源（图片、字体、视频等）有不同的优化策略：太小的图片内联成 base64 可以减少请求数，太大的资源用 CDN 加载更快：

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    // assetsInlineLimit：小于多少字节的图片，会被转成 base64 直接嵌入 HTML
    // 4096 = 4KB，图片小于 4KB 时直接内联，减少 HTTP 请求
    // 太大的图片不适合内联（base64 比原文件大 33%），会反而拖慢加载
    assetsInlineLimit: 4096,

    // publicDir：静态资源根目录，打包时会原样复制到 dist
    // 放不需要处理的公共资源，如 favicon.ico、robots.txt
    publicDir: 'public',

    // assetsDir：构建产物中静态资源的输出路径
    assetsDir: 'assets',

    // 文件名哈希（缓存优化的关键）
    // 有哈希的文件名，内容变化时哈希就变，浏览器就会重新请求
    // 没有变化的文件，哈希不变，浏览器直接用缓存
    rollupOptions: {
      output: {
        // 带哈希的文件名
        entryFileNames: 'js/[name]-[hash].js',
        chunkFileNames: 'js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.')
          const ext = info[info.length - 1]
          if (/\.(png|jpe?g|svg|gif|webp|ico)$/.test(assetInfo.name)) {
            return `images/[name]-[hash][extname]`
          }
          if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
            return `fonts/[name]-[hash][extname]`
          }
          return `[name]-[hash][extname]`
        },
      },
    },
  },
})
```

### 30.1.4 CDN 配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

const cdnBase = 'https://cdn.example.com'

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // CDN 基础路径
        publicPath: '/',
        
        // 外部化 CDN 依赖
        external: ['vue', 'vue-router', 'pinia'],
      },
    },
  },
  
  // 或者在 HTML 模板中手动引入 CDN
  // 这种方式更灵活，可以选择具体的 CDN 服务商
})

// index.html
/*
<script src="https://cdn.bootcdn.net/ajax/libs/vue/3.4.0/vue.global.prod.js"></script>
*/
```

## 30.2 Nginx 配置

### 30.2.1 SPA 路由配置

Vue Router 使用 history 模式时，URL 像普通 URL 一样，但服务器上并没有对应的文件。需要配置 Nginx 将所有请求重定向到 index.html：

```nginx
# /etc/nginx/conf.d/vue-app.conf

server {
    listen 80;
    server_name example.com;
    
    # Vue Router history 模式的关键配置
    location / {
        root /usr/share/nginx/html;  # 静态文件目录
        index index.html;
        
        # try_files 是关键：
        # 尝试查找文件，找不到就返回 index.html
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理（如果前后端分离）
    location /api/ {
        proxy_pass http://backend:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket 支持
    location /ws/ {
        proxy_pass http://backend:3000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /usr/share/nginx/html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 30.2.2 Gzip 压缩

```nginx
server {
    # 开启 gzip
    gzip on;
    gzip_vary on;
    
    # gzip 压缩级别（1-9，越高压缩率越大，CPU 消耗越多）
    gzip_comp_level 6;
    
    # 不压缩的资源
    gzip_proxied any;
    gzip_min_length 1000;
    
    # 压缩的文件类型
    gzip_types 
        text/plain
        text/css
        text/xml
        application/json
        application/javascript
        application/xml
        application/xml+rss
        application/vnd.ms-fontobject
        application/x-font-ttf
        font/opentype
        image/svg+xml
        image/x-icon;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 30.2.3 安全配置

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/example.com.pem;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    
    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # HSTS（可选，启用后浏览器会强制使用 HTTPS）
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 30.2.4 负载均衡配置

```nginx
# upstream 定义后端服务器组
upstream backend {
    least_conn;  # 最少连接数负载均衡
    server backend1.example.com:3000;
    server backend2.example.com:3000;
    server backend3.example.com:3000;
}

server {
    listen 80;
    server_name example.com;
    
    location /api/ {
        proxy_pass http://backend/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 连接超时配置
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 失败重试
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## 30.3 Docker 容器化

### 30.3.1 Dockerfile 基础

```dockerfile
# Stage 1: 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源码
COPY . .

# 构建
RUN npm run build

# Stage 2: 运行阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理（如果有后端）
    location /api/ {
        proxy_pass http://backend:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 30.3.2 多阶段构建优化

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

# 利用 Docker 缓存，只在 package.json 变化时重新安装依赖
COPY package*.json ./
RUN npm ci

# 复制源码
COPY . .

# 使用 npm 而非pnpm（Alpine 生态更完善）
# 构建生产版本
RUN npm run build -- --mode production

# 运行阶段 - 使用更小的镜像
FROM node:20-alpine AS runner

WORKDIR /app

# 复制构建产物
COPY --from=builder /app/dist ./dist

# 如果是 SSR 应用，还需要复制 node_modules
# COPY --from=builder /app/node_modules ./node_modules

ENV NODE_ENV=production

# 非 root 用户运行（更安全）
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
    
USER appuser

CMD ["node", "dist/server.js"]  # SSR 应用的启动命令
```

### 30.3.3 docker-compose 编排

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 前端应用
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

  # 后端 API
  backend:
    image: node:20-alpine
    working_dir: /app
    command: node server.js
    volumes:
      - ./server:/app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
    networks:
      - app-network

  # 数据库
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
```

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建
docker-compose up -d --build
```

### 30.3.4 Nuxt 3 的 Docker 配置

```dockerfile
# 用于 Nuxt SSR 应用的 Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci

# 复制源码
COPY . .

# 构建 Nuxt 应用
RUN npm run build

# 运行阶段
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# 安装 dumb-init（处理信号传递）
RUN apk add --no-cache dumb-init

# 创建非 root 用户
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nuxt

# 复制构建产物
COPY --from=builder --chown=nuxt:nodejs /app/.output /app/.output

USER nuxt

EXPOSE 3000

# 使用 dumb-init 正确处理 SIGTERM 信号
CMD ["dumb-init", "node", ".output/server/index.mjs"]
```

## 30.4 监控与性能

### 30.4.1 Sentry 错误监控

Sentry 是最流行的前端错误监控平台：

```bash
npm install @sentry/vue @sentry/tracing
```

```typescript
// main.ts 或 composables/useSentry.ts
import * as Sentry from '@sentry/vue'
import { BrowserTracing } from '@sentry/tracing'

export function initSentry(app: App) {
  Sentry.init({
    app,
    dsn: 'https://xxxxx@sentry.io/xxxxx',  // 你的 DSN
    
    // 采样率（0-1）
    tracesSampleRate: 0.1,
    
    // 采样错误
    sampleRate: 1.0,
    
    // 集成
    integrations: [
      new BrowserTracing({
        // 追踪页面性能
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
        // 追踪资源加载
        resourceTracking: true,
      }),
      new Sentry.Replay(),  // 录屏功能
    ],
    
    // 忽略的错误
    ignoreErrors: [
      'ResizeObserver loop',
      'Non-Error promise rejection',
    ],
    
    // beforeSend 可以在发送前修改错误数据
    beforeSend(event) {
      // 过滤敏感信息
      if (event.user) {
        delete event.user.email
        delete event.user.ip_address
      }
      return event
    },
  })
}
```

```vue
<script setup lang="ts">
import { initSentry } from '~/composables/useSentry'

// 在 setup 中初始化
onMounted(() => {
  initSentry(app)
})
</script>
```

### 30.4.2 性能监控（Web Vitals）

```typescript
// composables/useWebVitals.ts
import { onMounted } from 'vue'

export function useWebVitals(callback: (metric: any) => void) {
  onMounted(() => {
    if ('PerformanceObserver' in window) {
      // LCP - 最大内容绘制
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries()
        const lastEntry = entries[entries.length - 1] as any
        callback({
          name: 'LCP',
          value: lastEntry.renderTime || lastEntry.loadTime,
          rating: lastEntry.renderTime > 2500 ? 'poor' : 'good',
        })
      })
      lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true })
      
      // FID - 首次输入延迟
      const fidObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          callback({
            name: 'FID',
            value: entry.processingTime - entry.startTime,
            rating: entry.processingTime > 100 ? 'poor' : 'good',
          })
        }
      })
      fidObserver.observe({ type: 'first-input', buffered: true })
      
      // CLS - 累积布局偏移
      let clsValue = 0
      let clsEntries: any[] = []
      
      const clsObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsEntries.push(entry)
            clsValue += (entry as any).value
          }
        }
      })
      clsObserver.observe({ type: 'layout-shift', buffered: true })
      
      // 页面隐藏时报告 CLS
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          callback({
            name: 'CLS',
            value: clsValue,
            entries: clsEntries,
            rating: clsValue > 0.1 ? 'poor' : 'good',
          })
        }
      })
    }
  })
}

// 使用
// useWebVitals((metric) => {
//   // 上报到你的监控服务
//   console.log(metric)
// })
```

### 30.4.3 自定义埋点

```typescript
// utils/analytics.ts

// 页面访问
export function trackPageView(path: string) {
  // 发送到你的分析服务
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      event: 'page_view',
      path,
      timestamp: Date.now(),
      userAgent: navigator.userAgent,
    }),
  }).catch(() => {})  // 埋点失败不影响业务
}

// 点击事件
export function trackClick(category: string, action: string, label?: string) {
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      event: 'click',
      category,
      action,
      label,
      timestamp: Date.now(),
    }),
  }).catch(() => {})
}

// Vue 指令
export const track = {
  mounted(el: HTMLElement, binding: any) {
    el.addEventListener('click', () => {
      trackClick(
        binding.value.category,
        binding.value.action,
        binding.value.label
      )
    })
  },
}

// 使用
// <button v-track="{ category: 'button', action: 'click', label: '提交' }">
```

## 30.5 CI/CD 流水线

### 30.5.1 GitHub Actions 基础

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # 测试 job
  test:
    name: Test
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Type check
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Unit tests
        run: npm run test:unit
      
      - name: E2E tests
        run: npm run test:e2e

  # 构建 job
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          NODE_ENV: production
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist
          retention-days: 7

  # 部署 job
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            # 部署命令
            cd /var/www/vue-app
            docker-compose pull
            docker-compose up -d
```

### 30.5.2 完整的部署流水线

```yaml
# 完整的 CI/CD 配置
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint-and-test:
    name: Lint & Test
    runs-on: ubuntu-latest
    
    services:
      # 如果需要数据库
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Type check
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Unit tests with coverage
        run: npm run test:unit -- --coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
      
      - name: E2E tests
        run: npm run test:e2e
        env:
          CYPRESS_BASE_URL: http://localhost:3000

  build-image:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: lint-and-test
    if: github.event_name == 'push'
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/develop'
    
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - name: Deploy to staging server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          envs: IMAGE_TAG
          script: |
            # 拉取最新镜像
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            
            # 更新 docker-compose
            sed -i 's|image:.*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}|' docker-compose.staging.yml
            
            # 重启服务
            docker-compose -f docker-compose.staging.yml up -d
            
            # 等待健康检查
            sleep 10

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/main'
    
    environment:
      name: production
      url: https://example.com
    
    steps:
      - name: Deploy to production server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PRODUCTION_HOST }}
          username: ${{ secrets.PRODUCTION_USER }}
          key: ${{ secrets.PRODUCTION_SSH_KEY }}
          script: |
            # 部署流程（更谨慎）
            cd /var/www/vue-app
            
            # 备份当前版本
            docker-compose exec -T app tar czf /tmp/backup-$(date +%Y%m%d%H%M%S).tar.gz ./data
            
            # 滚动更新
            docker-compose pull
            docker-compose up -d --no-deps app
            
            # 健康检查
            for i in {1..30}; do
              if curl -sf http://localhost/health > /dev/null; then
                echo "Health check passed"
                exit 0
              fi
              echo "Waiting for health check... ($i/30)"
              sleep 2
            done
            
            echo "Health check failed, rolling back..."
            docker-compose pull backup
            docker-compose up -d --no-deps app
            exit 1
```

### 30.5.3 环境变量管理

```bash
# .env.staging
VITE_API_BASE=https://api.staging.example.com
VITE_SENTRY_DSN=https://xxx@staging.sentry.io/xxx

# .env.production
VITE_API_BASE=https://api.example.com
VITE_SENTRY_DSN=https://xxx@sentry.io/xxx
```

```bash
# .gitignore
.env
.env.local
.env.*.local

# 但保留示例文件
# !.env.example
```

### 30.5.4 GitHub Secrets 配置

在 GitHub 仓库的 Settings > Secrets and variables > Actions 中配置：

| Secret 名称 | 说明 |
|-------------|------|
| `SERVER_HOST` | 服务器 IP 或域名 |
| `SERVER_USER` | SSH 用户名 |
| `SERVER_SSH_KEY` | SSH 私钥 |
| `STAGING_HOST` | 预发布环境服务器 |
| `STAGING_USER` | 预发布 SSH 用户 |
| `STAGING_SSH_KEY` | 预发布 SSH 私钥 |
| `PRODUCTION_HOST` | 生产环境服务器 |
| `PRODUCTION_USER` | 生产 SSH 用户 |
| `PRODUCTION_SSH_KEY` | 生产 SSH 私钥 |
| `DOCKER_USERNAME` | Docker Hub 用户名 |
| `DOCKER_PASSWORD` | Docker Hub 密码 |

## 30.6 本章小结

本章我们学习了 Vue 3 应用部署的完整流程：

1. **构建分析**：使用 visualizer 分析打包体积，配置优化选项
2. **Nginx 配置**：SPA 路由、Gzip 压缩、安全头、负载均衡
3. **Docker 容器化**：多阶段构建、docker-compose 编排
4. **监控与埋点**：Sentry 错误监控、Web Vitals 性能监控、自定义埋点
5. **CI/CD 流水线**：GitHub Actions 自动测试、构建、部署

部署是软件开发的最后一公里，也是最重要的一环。只有部署好了，用户才能真正用到你的应用。

下一章，也是本教程的最后一章，我们将深入 Vue 3 的源码，从宏观到微观，全面理解 Vue 3 的设计理念和实现细节。🔍
