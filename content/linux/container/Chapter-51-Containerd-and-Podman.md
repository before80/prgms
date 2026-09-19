+++
title = "第51章：Containerd 与 Podman"
weight = 510
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第五十一章：Containerd 与 Podman

## 51.1 Containerd 简介

### Containerd是什么？

如果说Docker是一个"全能管家"，那**Containerd**就是管家的"专业部门"——专门负责容器生命周期的管理。

Containerd是CNCF（云原生计算基金会）的毕业项目，它是从Docker中**剥离出来的容器运行时**。

```mermaid
flowchart TB
    subgraph "用 Docker 的场景"
        DC[docker CLI] --> DD[dockerd]
        DD --> C1[containerd]
        C1 --> R1[runc]
        R1 --> Cont1[容器]
    end
    
    subgraph "用 Kubernetes 的场景"
        K[kubelet] --> C2[containerd<br/>的 CRI 插件]
        C2 --> R2[runc]
        R2 --> Cont2[容器]
    end
    
    style C1 fill:#ff9999
    style C2 fill:#ff9999
```

可以看出：不管上层的工具是 Docker 还是 Kubernetes，**真正干活的那一层都是 containerd + runc**。
Docker 多出来的部分是镜像构建（buildkit）、CLI、Compose 等"周边服务"，而 Kubernetes 只需要
containerd 暴露的 CRI 接口就够了。

### Containerd的历史

```
2016年：containerd从Docker中拆分出来、独立开源；
        Docker 1.11 也开始用containerd管理容器的生命周期
    ↓
2017年：Docker把containerd捐给CNCF托管（社区中立治理）
    ↓
2019年：containerd从CNCF毕业，成为顶级项目
    ↓
2022年：Kubernetes 1.24移除dockershim，
        containerd（或CRI-O）成为K8s的默认运行时
    ↓
2024年：containerd 2.0发布，配置与1.x基本兼容
```

> 提醒一句：网上常见"2015年捐赠""2017年 Docker 1.11"这类时间线是把几件事记串了。
> 记住三个关键年份就够了——**2016 年独立开源、2017 年捐给 CNCF、2019 年从 CNCF 毕业**。

### Containerd vs Docker

| 对比项 | Containerd | Docker |
|--------|-----------|--------|
| **定位** | 容器运行时 | 容器平台 |
| **功能** | 容器生命周期管理 | 构建、运行、网络、存储... |
| **复杂性** | 简单 | 复杂 |
| **使用场景** | Kubernetes节点 | 开发、测试 |

### Containerd的架构

```mermaid
flowchart TB
    subgraph "Containerd架构"
        API[Containerd API<br/>GRPC]
        API --> S[Service Layer<br/>服务层]
        S --> M[Metadata Store<br/>元数据]
        S --> S2[Snapshotter<br/>快照管理]
        S --> C[Container<br/>容器]
        C --> R[runtime<br/>运行时]
        R --> O[OCI Runtime<br/>如runc]
    end
    
    style API fill:#99ccff
    style S fill:#90EE90
    style R fill:#ff9999
```

**Containerd的核心功能：**
- **镜像管理**：拉取、推送镜像
- **容器管理**：创建、启动、停止容器
- **快照管理**：管理容器的文件系统快照
- **网络管理**：管理容器网络

### 为什么要用Containerd？

**理由1：Kubernetes默认运行时**
- Kubernetes从1.24开始默认使用containerd
- 更轻量，更稳定

**理由2：简单直接**
- 没有Docker那么复杂
- 只需要容器运行时

**理由3：减少依赖**
- 不需要完整的Docker
- 减少维护成本

### Containerd适用场景

| 场景 | 适合使用Containerd |
|------|-------------------|
| Kubernetes节点 | ✅ 最常见 |
| 边缘计算 | ✅ 资源受限 |
| 嵌入式系统 | ✅ 轻量 |

### 小结

Containerd是什么？
- **容器运行时**：管理容器生命周期
- **Docker的组件**：从Docker剥离出来
- **CNCF项目**：云原生标准

Containerd vs Docker：
- 更轻量
- 更专注
- K8s默认支持

下一节我们将学习如何安装Containerd！

## 51.2 Containerd 安装

### 安装前准备

Containerd需要以下组件：
- **containerd**：主程序
- **runc**：OCI运行时
- **cni**：网络插件（可选）

### 在Ubuntu上安装

#### 方法一：使用apt安装

```bash
# 1. 更新软件包
sudo apt update

# 2. 安装containerd
sudo apt install -y containerd

# 3. 生成默认配置
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# 4. 修改配置，开启SystemdCgroup
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# 5. 重启服务
sudo systemctl restart containerd

# 6. 验证安装
containerd --version
# containerd github.com/containerd/containerd/v2 v2.0.5 ...
# （1.6、1.7 等旧版现在仍在很多系统里使用，命令输出格式略有差别）

# 7. 设置开机自启
sudo systemctl enable --now containerd
```

> 版本提醒：Ubuntu 官方仓库里的 `containerd` 往往比 Docker 仓库的 `containerd.io` 旧，
> Kubernetes 新版本一般要求 containerd ≥ 1.6，所以生产上更推荐用 Docker 仓库的 `containerd.io`
> 或者 containerd 官方 release 的二进制包。

### 在CentOS上安装

```bash
# 1. 添加Docker仓库（CentOS Stream 9 / Rocky 9 / AlmaLinux 9 用 dnf）
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 2. 安装containerd
sudo dnf install -y containerd.io

# 3. 生成配置
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# 4. 修改配置
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# 5. 重启服务
sudo systemctl enable --now containerd
```

> ⚠️ CentOS Linux 7 已于 2024-06-30 停止维护，CentOS Linux 8 更早在 2021-12-31 就 EOL 了。
> 新环境请用 Rocky Linux 9 / AlmaLinux 9 / CentOS Stream 9，命令统一用 `dnf`。
> 如果不想引入 Docker 的仓库，也可以直接 `sudo dnf install -y containerd`（发行版自带版本通常略旧）。

### 配置文件说明

```bash
# 查看配置文件
cat /etc/containerd/config.toml

# 关键配置项说明：

# SystemdCgroup - 使用systemd管理cgroup
[plugins."io.containerd.grpc.v1.cri"]
  SystemdCgroup = true

# 镜像加速器配置
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.9"
  
# 日志配置
[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"

# 存储驱动配置
[plugins."io.containerd.snapshotter.v1.overlayfs"]
  root_path = "/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs"
```

### 安装runc

Containerd需要runc作为OCI运行时：

```bash
# 下载runc（版本号请到 opencontainers/runc 的 release 页取最新）
curl -LO https://github.com/opencontainers/runc/releases/download/v1.2.5/runc.amd64

# 安装runc
sudo mv runc.amd64 /usr/local/bin/runc
sudo chmod +x /usr/local/bin/runc

# 验证
runc --version
# runc version 1.2.5
```

> 注意：如果已经装了 `containerd.io` 包，runc 通常已经作为依赖装好了，
> 这时再手动覆盖 `/usr/local/bin/runc` 属于"抢优先级"的做法，升级前先确认版本关系。

### 安装CNI网络插件

```bash
# 下载CNI插件（版本号请取 release 页最新，架构按 uname -m 选 amd64/arm64）
curl -LO https://github.com/containernetworking/plugins/releases/download/v1.6.2/cni-plugins-linux-amd64-v1.6.2.tgz

# 解压到指定目录
sudo mkdir -p /opt/cni/bin
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-v1.6.2.tgz

# 验证
ls /opt/cni/bin/
# bridge dhcp dummy flannel host-device host-local ipvlan loopback macvlan portmap ptp sample static vlan
```

### Containerd作为Kubernetes运行时

如果要将Containerd配置为Kubelet的运行时：

```bash
# 方式一：kubeadm 集群，在 kubeadm 配置里指定 CRI socket（推荐）
# ClusterConfiguration 之外的 kubeletExtraArgs 或 InitConfiguration 里写：
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
  criSocket: unix:///run/containerd/containerd.sock

# 方式二：编辑 kubelet 自己的配置 /var/lib/kubelet/config.yaml
# 注意字段名是 containerRuntimeEndpoint，不是 runtimeEndpoint
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
imagePullProgressDeadline: 10m

# 改完重启 kubelet
sudo systemctl restart kubelet

# 检查是否连上了容器运行时
kubectl get nodes -o wide    # 节点状态应为 Ready
```

> 小坑提醒：旧教程里写的 `runtimeEndpoint:` 并不是 KubeletConfiguration 的合法字段，
> kubelet 解析配置时会直接报未知字段的错误。老版本 kubelet 用的是命令行参数
> `--container-runtime-endpoint=unix:///run/containerd/containerd.sock`，这个参数在新版本里也已移除。

### 一图总结安装流程

```mermaid
flowchart TD
    A[安装Containerd] --> B[安装runc]
    B --> C[安装CNI]
    C --> D[配置containerd]
    D --> E[启动服务]
    E --> F[验证安装]
    
    style A fill:#99ccff
    style F fill:#90EE90
```

### 小结

Containerd安装要点：
- `apt install containerd` 或 `yum install containerd.io`
- 生成配置文件：`containerd config default`
- 开启 `SystemdCgroup = true`
- 安装runc和CNI插件

下一节我们将学习 **nerdctl命令**，这是containerd的命令行工具！

## 51.3 nerdctl 命令

### nerdctl是什么？

**nerdctl** 是containerd的官方命令行工具，类似于Docker CLI。

```mermaid
flowchart LR
    A[nerdctl] --> B[containerd]
    C[docker] --> D[dockerd]
```

### 安装nerdctl

```bash
# 下载nerdctl（版本号请到 release 页取最新，这里以 2.x 为例）
curl -LO https://github.com/containerd/nerdctl/releases/download/v2.0.3/nerdctl-2.0.3-linux-amd64.tar.gz

# 解压
sudo tar -C /usr/local/bin -xzf nerdctl-2.0.3-linux-amd64.tar.gz

# 验证
nerdctl --version
# nerdctl version 2.0.3
```

> 小贴士：如果只是想在单机上用 Docker 一样的体验，直接装 `nerdctl-full` 包最省事——
> 它把 containerd、runc、CNI 插件、buildkit 全打包在一起，省得自己一个个装。
> 跑 Kubernetes 集群时真正被用的是 containerd 的 CRI 接口，nerdctl 只是给人用的 CLI。

### nerdctl vs docker 命令对比

nerdctl的很多命令和Docker类似：

| Docker命令 | nerdctl命令 | 说明 |
|-----------|-------------|------|
| `docker pull` | `nerdctl pull` | 拉取镜像 |
| `docker images` | `nerdctl images` | 查看镜像 |
| `docker run` | `nerdctl run` | 运行容器 |
| `docker ps` | `nerdctl ps` | 查看容器 |
| `docker exec` | `nerdctl exec` | 进入容器 |
| `docker logs` | `nerdctl logs` | 查看日志 |
| `docker build` | `nerdctl build` | 构建镜像 |

### 镜像操作

```bash
# 拉取镜像
nerdctl pull nginx:latest

# 查看本地镜像
nerdctl images

# 删除镜像
nerdctl rmi nginx:latest

# 清理未使用的镜像
nerdctl image prune
```

### 容器操作

```bash
# 运行容器
nerdctl run -d --name nginx nginx:latest

# 查看容器
nerdctl ps

# 查看所有容器（包括已停止）
nerdctl ps -a

# 停止容器
nerdctl stop nginx

# 启动容器
nerdctl start nginx

# 删除容器
nerdctl rm nginx

# 进入容器
nerdctl exec -it nginx /bin/bash

# 查看日志
nerdctl logs -f nginx
```

### 构建镜像

```bash
# 构建镜像（支持Dockerfile）
nerdctl build -t myapp:v1 .

# 带参数构建
nerdctl build --build-arg VERSION=1.0 -t myapp:v1 .
```

### nerdctl特有功能

```bash
# 查看compose（nerdctl支持compose）
nerdctl compose up -d

# 登录镜像仓库
nerdctl login -u username registry.example.com

# 推送镜像
nerdctl push registry.example.com/myapp:v1

# 镜像加密（nerdctl特有）
nerdctl image encrypt --recipient jwe:mykey.pem myapp:v1 myapp:v1.enc

# 镜像解密
nerdctl image decrypt --key mykey.pem myapp:v1.enc myapp:v1
```

### 使用nerdctl作为Docker替代

```bash
# 创建别名（可选）
echo "alias docker=nerdctl" >> ~/.bashrc
source ~/.bashrc

# 现在可以像使用docker一样使用nerdctl
docker pull nginx:latest
docker run -d -p 80:80 nginx:latest
```

### 小结

nerdctl命令：
- nerdctl是containerd的CLI工具
- 命令与Docker类似
- 支持镜像加密等特有功能

下一节我们将学习 **Podman**，这是Docker的无守护进程替代品！

## 51.4 Podman 简介

### Podman是什么？

**Podman** 是Docker的**无守护进程**替代品，由Red Hat开发。

最大的特点：**不需要Docker守护进程（daemon）！**

```mermaid
flowchart LR
    subgraph "Docker架构"
        D[Docker Daemon<br/>需要root运行]
        D --> C[容器]
    end
    
    subgraph "Podman架构"
        U[Podman<br/>无守护进程]
        U --> C2[容器]
    end
    
    style D fill:#ff9999
    style U fill:#90EE90
```

### Podman vs Docker

| 对比项 | Podman | Docker |
|--------|--------|--------|
| **守护进程** | 无 | 需要 |
| **运行用户** | 普通用户 | 需要root |
| **Pod支持** | 原生支持 | 需要额外工具 |
| **兼容性** | 兼容Docker | - |
| **开发公司** | Red Hat | Docker Inc. |

> 两点补充，避免被"绝对化"的说法带偏：
> 1. **Docker 现在也有 rootless 模式**（`dockerd-rootless-setuptool.sh`），并非只能 root 运行；
>    只是默认安装方式仍然以 root 守护进程为主。
> 2. **Podman 说"无守护进程"是指没有常驻的中央守护进程**，它仍然会为每个容器启动一个
>    `conmon` 监控进程，底层同样依赖 `runc`/`crun`。在 macOS/Windows 上，Podman 还需要
>    先 `podman machine init && podman machine start` 起一台 Linux 虚拟机才能跑容器。

### Podman的优势

**1. 无守护进程**
- 不需要运行Docker daemon
- 减少资源占用
- 减少攻击面

**2. 可以非root运行**
- 普通用户可以运行容器
- 更安全

**3. 原生支持Pod**
- Pod是Kubernetes的概念
- Podman直接支持

**4. 兼容Docker**
- 可以直接替换Docker
- 零成本迁移

### Podman的核心概念

**Pod（容器组）：**
```
┌───────────────────────────────────┐
│           Pod                     │
│  ┌───────────┐  ┌───────────┐     │
│  │ Container1│  │ Container2│     │
│  └───────────┘  └───────────┘     │
│         共享网络和存储            │
└───────────────────────────────────┘
```

### Podman的适用场景

| 场景 | 说明 |
|------|------|
| 开发环境 | 无需root，更安全 |
| 替代Docker | 零成本迁移 |
| 学习K8s | 原生Pod支持 |
| 桌面环境 | 减少资源占用 |

### 小结

Podman是什么？
- **Docker替代品**：无守护进程
- **Red Hat开发**：企业级
- **兼容Docker**：命令几乎一样

Podman vs Docker：
- 无需守护进程
- 可非root运行
- 原生Pod支持

下一节我们将详细对比Podman和Docker！

## 51.5 Podman vs Docker

### 命令对比

Podman的命令与Docker几乎完全兼容：

| Docker命令 | Podman命令 | 区别 |
|-----------|-----------|------|
| `docker pull` | `podman pull` | 相同 |
| `docker push` | `podman push` | 相同 |
| `docker images` | `podman images` | 相同 |
| `docker run` | `podman run` | 相同 |
| `docker build` | `podman build` | 相同 |
| `docker-compose` | `podman-compose` | 需要安装 |

### 架构对比

```mermaid
flowchart TB
    subgraph "Docker"
        D[Docker Daemon<br/>root运行]
        D --> R[runc]
        R --> C[容器]
    end
    
    subgraph "Podman"
        P[Podman<br/>普通用户运行]
        P --> R2[runc]
        R2 --> C2[容器]
        
        V[Volume插件]
        V -.->|volumes| C2
    end
    
    style D fill:#ff9999
    style P fill:#90EE90
```

### 安全对比

| 特性 | Docker | Podman |
|------|--------|--------|
| root运行 | 需要 | 不需要 |
| 容器root映射 | 可能需要 | 可选 |
| 攻击面 | 较大（daemon） | 较小 |
| SELinux支持 | 有限 | 完整 |

### Podman的高级功能

**1. 无根容器（Rootless）**
```bash
# 普通用户直接运行容器
podman run -d nginx:latest

# 不需要sudo，不需要daemon
```

**2. 原生Pod支持**
```bash
# 创建Pod
podman pod create --name mypod

# 在Pod中添加容器
podman run -d --pod mypod nginx:latest
podman run -d --pod mypod redis:latest
```

### 迁移到Podman

```bash
# 1. 安装Podman
# Ubuntu
sudo apt install podman

# CentOS
sudo yum install podman

# macOS
brew install podman

# 2. 创建别名（平滑过渡）
echo "alias docker=podman" >> ~/.bashrc
source ~/.bashrc

# 3. 验证
docker --version
# podman version 4.6.2
```

### 小结

Podman vs Docker：
- 命令兼容，可以无缝切换
- 无守护进程，更安全
- 原生支持Pod

下一节我们将学习Podman的实际使用！

## 51.6 Podman 使用

### Podman安装

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install podman -y

# CentOS/RHEL
sudo yum install podman -y

# macOS
brew install podman

# 验证安装
podman --version
```

### 镜像操作

```bash
# 拉取镜像
podman pull nginx:latest

# 查看镜像
podman images

# 删除镜像
podman rmi nginx:latest

# 清理未使用的镜像
podman image prune
```

### 容器操作

```bash
# 运行容器
podman run -d --name nginx nginx:latest

# 查看容器
podman ps
podman ps -a  # 包括已停止的

# 停止容器
podman stop nginx

# 启动容器
podman start nginx

# 删除容器
podman rm nginx

# 进入容器
podman exec -it nginx /bin/bash

# 查看日志
podman logs -f nginx
```

### Pod操作

Podman原生支持Kubernetes Pod：

```bash
# 创建Pod
podman pod create --name mypod

# 查看Pod
podman pod ls

# 在Pod中运行容器
podman run -d --pod mypod nginx:latest
podman run -d --pod mypod redis:latest

# 查看Pod中的容器
podman ps --pod

# 停止/删除Pod（会删除所有容器）
podman pod stop mypod
podman pod rm mypod
```

### Pod + 多容器示例

```bash
# 1. 创建Pod
podman pod create --name webapp

# 2. 运行应用容器
podman run -d --pod webapp --name app myapp:latest

# 3. 运行Nginx反向代理
podman run -d --pod webapp --name nginx -p 8080:80 nginx:latest

# 4. 查看Pod状态
podman pod inspect webapp

# 5. 停止整个Pod
podman pod stop webapp

# 6. 删除Pod
podman pod rm -f webapp
```

### 构建镜像

```bash
# 使用Podman Buildah（内置）
podman build -t myapp:v1 .

# 使用Dockerfile
podman build -f Dockerfile -t myapp:v1 .
```

### 与Docker无缝切换

```bash
# 1. 查看Podman信息
podman info

# 2. 登录镜像仓库
podman login docker.io

# 3. 推送镜像
podman push myapp:v1 docker.io/myuser/myapp:v1

# 4. Docker Compose 兼容层
#    Podman 4.1+ 自带 podman compose 子命令（内部会调用 docker-compose 或 podman-compose）
podman compose up -d

#    也可以单独安装 podman-compose（Python 实现，功能没那么全）
#    注意：不建议再用 pip 装到系统 Python 里，优先用发行版的包
sudo apt install podman-compose      # Debian/Ubuntu
sudo dnf install podman-compose      # Fedora/RHEL 系
podman-compose up -d
```

### Podman生成Kubernetes YAML

```bash
# 从Pod生成K8s YAML（Podman 4.9+ 的新写法）
podman kube generate mypod > mypod.yaml
# 旧写法（已废弃，但很多老教程还在用）：podman generate kube mypod > mypod.yaml

# 创建Pod from K8s YAML
podman play kube mypod.yaml
```

### 常用配置

```bash
# 配置镜像仓库（/etc/containers/registries.conf）
[registries.search]
registries = ['docker.io', 'quay.io']

# 配置存储（/etc/containers/storage.conf）
[storage]
driver = "overlay"
```

### 小结

Podman使用要点：
- 安装：`apt install podman` 或 `brew install podman`
- 命令与Docker几乎相同
- 原生支持Pod
- 支持无根运行

---

## 本章小结

本章我们学习了Containerd和Podman：

### Containerd
| 命令 | 说明 |
|------|------|
| `containerd --version` | 查看版本 |
| 配置文件 | `/etc/containerd/config.toml` |

### nerdctl
- containerd的CLI工具
- 命令与Docker类似
- 支持镜像加密等特有功能

### Podman
| 特性 | 说明 |
|------|------|
| 无守护进程 | 更安全 |
| 可非root运行 | 更灵活 |
| 兼容Docker | 零成本迁移 |
| 原生Pod支持 | K8s友好 |

### 命令对比

| 功能 | Docker | Podman | nerdctl |
|------|--------|--------|---------|
| 拉取镜像 | `docker pull` | `podman pull` | `nerdctl pull` |
| 运行容器 | `docker run` | `podman run` | `nerdctl run` |
| 构建镜像 | `docker build` | `podman build` | `nerdctl build` |

### 下章预告

下一章我们将学习 **Kubernetes**，这是容器编排的王者，敬请期待！

> **趣味彩蛋**：Containerd和Podman在一起喝茶，讨论谁是Docker的最佳替代品。
>
> Containerd说："我是Docker的亲儿子，K8s都用我！"
> Podman说："我是无守护进程，安全性碾压你！"
>
> Docker在旁边默默喝着咖啡，心想："你们都是我生的..." 😏
>
> 记住：**没有最好的工具，只有最适合你场景的工具！** 🛠️
