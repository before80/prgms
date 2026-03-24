+++
title = "第30章：网络配置"
weight = 300
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第三十章：网络配置

上一章我们学了网络理论知识，知道了IP地址、子网掩码、网关都是什么。这一章，我们要把理论变成实践——在Linux系统上配置网络。

类比一下：上一章是学交通规则，这一章是学怎么开车。理论上你能背下所有路标，但坐进驾驶座你得知道油门在哪、刹车在哪。

Linux配置网络的命令有好几代：`ifconfig`是爷爷辈的，`ip`是现在的扛把子，还有Netplan、NetworkManager等高级工具。Ubuntu 18.04+推荐用Netplan，桌面环境用NetworkManager，服务器用`ip`命令。

> 本章配套视频：你的Linux突然连不上网了，别慌，按这一章来，一步步排查。

## 30.1 ip 命令：新一代网络配置工具

`ip`命令是iproute2工具包的核心成员，是`ifconfig`的接班人。Linux内核2.2引入iproute2，从此`ip`命令一统江湖。

`ip`命令功能强大到离谱——查看IP、MAC、路由表、隧道、VLAN……一个命令全搞定。

### 30.1.1 ip addr：查看 IP 地址

```bash
# 查看所有网络接口的IP配置
ip addr show

# 简写形式
ip a
```

```bash
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:5a:6b:7c brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 604783sec preferred_lft 604783sec
```

输出解读：

- `1:` 和 `2:` 是网卡编号（interface index）
- `lo` 是环回接口（loopback），IP固定是127.0.0.1，用于本机内部通信
- `eth0` 是第一块以太网网卡（Ethernet）
- `inet 192.168.1.100/24`：IPv4地址是192.168.1.100，子网掩码/24（即255.255.255.0）
- `brd 192.168.1.255`：广播地址
- `state UP`：网卡状态是开启的

### 30.1.2 ip link：查看网络接口

```bash
# 查看所有网络接口的链路状态
ip link show

# 简写
ip l
```

```bash
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:5a:6b:7c brd ff:ff:ff:ff:ff:ff
```

- `BROADCAST`：支持广播
- `MULTICAST`：支持多播
- `UP`：接口启用
- `LOWER_UP`：物理层就绪（网线插好）

**开启和关闭网卡**：

```bash
# 关闭网卡（相当于拔网线）
sudo ip link set eth0 down

# 开启网卡
sudo ip link set eth0 up
```

> 💡 **救命小技巧**：如果你远程SSH连接服务器时，不小心把唯一的网卡`eth0`给`down`了，导致SSH断开连不上服务器怎么办？
> - 如果有VNC/IPMI/iDRAC等带外管理，可以通过这些方式登录重新开启网卡
> - 如果没有带外管理，只能联系机房管理员或重启服务器
> - **建议**：远程操作时，最好通过多个连接（比如同时开两个SSH窗口），或者使用`screen`/`tmux`保持会话

### 30.1.3 ip route：查看路由表

```bash
# 查看路由表
ip route show

# 简写
ip r
```

```bash
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.100 metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

解读：

- `default via 192.168.1.1 dev eth0`：默认路由，走192.168.1.1网关，从eth0出去
- `192.168.1.0/24 dev eth0`：本地网络路由，说明192.168.1.x这个网段可以直接从eth0到达
- `proto dhcp`：这条路由是通过DHCP学来的
- `metric 100`：路由优先级，数字越小优先级越高

**添加静态路由**：

```bash
# 添加到达10.0.0.0/8网络，走192.168.1.254网关
sudo ip route add 10.0.0.0/8 via 192.168.1.254 dev eth0

# 删除路由
sudo ip route del 10.0.0.0/8 via 192.168.1.254 dev eth0
```

### 30.1.4 ip addr add：添加 IP

```bash
# 给eth0添加一个临时IP（重启后消失）
sudo ip addr add 192.168.1.200/24 dev eth0

# 给eth0添加第二个IP（一个网卡可以绑定多个IP）
sudo ip addr add 192.168.1.201/24 dev eth0 label eth0:1

# 删除IP
sudo ip addr del 192.168.1.200/24 dev eth0
```

> **实战技巧**：`ip addr add`添加的IP是临时的，重启就没了。想永久生效？往下看Netplan和NetworkManager。

## 30.2 ifconfig 命令：传统网络配置

`ifconfig`是网络配置的"老前辈"，属于net-tools工具包。在`ip`命令出现之前，它是Linux网络配置的标配。

虽然现在推荐用`ip`命令，但`ifconfig`依然广泛存在于各种教程和脚本中，老系统维护工程师必须认识它。

### 30.2.1 ifconfig：查看

```bash
# 查看所有网卡配置
ifconfig

# 查看指定网卡
ifconfig eth0
```

```bash
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        ether 00:0c:29:5a:6b:7c  txqueuelen 1000  (Ethernet)
        RX packets 123456  bytes 98765432 (94.1 MiB)
        TX packets 654321  bytes 12345678 (11.7 MiB)

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        UP LOOPBACK RUNNING  mtu 65536  metric 1
        RX packets 1234  bytes 123456 (120.5 KiB)
        TX packets 1234  bytes 123456 (120.5 KiB)
```

输出中：

- `UP`：网卡已启用
- `BROADCAST`：支持广播
- `RUNNING`：正在运行
- `MULTICAST`：支持多播
- `mtu 1500`：最大传输单元1500字节
- `txqueuelen 1000`：发送队列长度

### 30.2.2 ifconfig eth0 up/down

```bash
# 开启网卡
sudo ifconfig eth0 up

# 关闭网卡
sudo ifconfig eth0 down

# 设置IP地址（临时，重启失效）
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# 同时设置IP和广播地址
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0 broadcast 192.168.1.255
```

> **警告**：`ifconfig`设置的IP在重启后会丢失，这是临时的。如果你在远程通过SSH配置网络，**千万不要**用`ifconfig eth0 down`——你会断开连接，想恢复就得去机房插显示器。

## 30.3 网络接口配置文件

说了这么多临时配置，该讲讲永久生效的方法了。Linux的网络配置文件分布在不同的目录，Debian/Ubuntu和CentOS的方案完全不同。

### 30.3.1 Debian/Ubuntu：/etc/network/interfaces

Debian系（Debian、Ubuntu）的传统网络配置方式是编辑`/etc/network/interfaces`文件。

```bash
# 查看当前配置
cat /etc/network/interfaces
```

```bash
# This file describes the network interfaces available on your system
# and how to activate them.

# Loopback回环接口
auto lo
iface lo inet loopback

# 第一块以太网网卡，使用DHCP自动获取IP
auto eth0
iface eth0 inet dhcp

# 如果想手动指定静态IP，注释上面几行，取消下面这几行的注释
# auto eth0
# iface eth0 inet static
#     address 192.168.1.100
#     netmask 255.255.255.0
#     gateway 192.168.1.1
#     dns-nameservers 8.8.8.8 223.5.5.5
```

配置说明：

- `auto eth0`：开机自动启动eth0
- `iface eth0 inet dhcp`：eth0使用DHCP获取IP
- `iface eth0 inet static`：eth0使用静态IP
- `address`：IP地址
- `netmask`：子网掩码
- `gateway`：网关
- `dns-nameservers`：DNS服务器（多个用空格分隔）

修改配置后，需要重启网络服务使配置生效：

```bash
# Debian/Ubuntu重启网络
sudo systemctl restart networking

# 或者
sudo /etc/init.d/networking restart
```

### 30.3.2 CentOS：/etc/sysconfig/network-scripts/ifcfg-eth0

CentOS/RHEL的网络配置文件在`/etc/sysconfig/network-scripts/`目录下，文件名格式是`ifcfg-<网卡名>`。

```bash
# 查看第一块网卡的配置文件
cat /etc/sysconfig/network-scripts/ifcfg-eth0
```

```bash
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
# 自动获取IP（DHCP模式）
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eth0
UUID=5a6b7c8d-9e0f-1234-5678-9abcdef01234
DEVICE=eth0
ONBOOT=yes
```

关键参数说明：

| 参数 | 说明 |
|------|------|
| `BOOTPROTO=dhcp` | 使用DHCP；改成`static`则用静态IP |
| `ONBOOT=yes` | 开机自动启用 |
| `DEVICE=eth0` | 网卡设备名 |
| `NAME=eth0` | 连接名称 |
| `UUID` | 设备的唯一标识 |

**如果想改成静态IP**，修改配置如下：

```bash
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
# 改成static就是静态IP
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eth0
UUID=5a6b7c8d-9e0f-1234-5678-9abcdef01234
DEVICE=eth0
ONBOOT=yes
# 以下是静态IP的配置项
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=223.5.5.5
```

CentOS重启网络：

```bash
sudo systemctl restart network
```

## 30.4 Netplan 配置：Ubuntu 18.04+ 网络配置

Ubuntu 17.10开始，引入了Netplan——一个用YAML声明式配置网络的工具。Netplan是"网络配置的革命"，把配置文件统一放在`/etc/netplan/`目录。

### 30.4.1 /etc/netplan/*.yaml

Netplan的配置文件是YAML格式，安装Ubuntu Server版时，安装程序会生成一个`/etc/netplan/00-installer-config.yaml`文件。

```bash
# 查看所有netplan配置
ls -la /etc/netplan/

# 查看当前网络配置
cat /etc/netplan/00-installer-config.yaml
```

```bash
# 这是安装时自动生成的DHCP配置
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```

Netplan配置的核心概念：

- `version: 2`：Netplan版本号，固定写2
- `renderer`：网络渲染器，可选`networkd`（systemd-networkd）或`NetworkManager`
- `ethernets`：以太网网卡配置
- `dhcp4: true/false`：是否启用IPv4 DHCP

### 30.4.2 netplan apply

Netplan的工作流程：写YAML配置文件 → 运行`netplan apply` → 生成对应的systemd-networkd或NetworkManager配置。

**配置静态IP示例**：

```bash
sudo vim /etc/netplan/00-installer-config.yaml
```

写入以下内容：

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 223.5.5.5
        search: []
```

配置说明：

- `dhcp4: false`：关闭DHCP，启用静态IP
- `addresses: [192.168.1.100/24]`：IP地址和CIDR前缀
- `gateway4: 192.168.1.1`：IPv4网关
- `nameservers.addresses`：DNS服务器列表

**应用配置并生效**：

```bash
# 先尝试生成配置看是否有错误（不实际应用）
sudo netplan generate

# 应用配置
sudo netplan apply

# 如果配置有问题，想回退到之前的配置
sudo netplan try
# netplan try 会开启120秒超时，如果超时或按Ctrl+C，会自动回退配置
```

> **Netplan的优雅之处**：你可以在`/etc/netplan/`目录下放多个配置文件，Netplan会按文件名顺序合并加载。数字小的先加载，所以可以用`01-`开头的自定义配置覆盖`00-`开头的默认配置。

## 30.5 NetworkManager：桌面环境网络管理

NetworkManager（NM）是Linux桌面环境的主流网络管理工具，Ubuntu桌面版、Fedora、CentOS桌面版默认都用它。NetworkManager最大的优点是——插上网线或连上WiFi，它自动搞定一切。

### 30.5.1 nmcli 命令

`nmcli`是NetworkManager的命令行工具，图形界面能干的事它都能干。

**查看网络连接状态**：

```bash
# 查看所有连接
nmcli connection show

# 查看活动连接
nmcli connection show --active
```

```bash
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  5a6b7c8d-9e0f-1234-5678-9abcdef01234  ethernet  eth0
```

**启动/停止连接**：

```bash
# 启动连接
sudo nmcli connection up "Wired connection 1"

# 停止连接
sudo nmcli connection down "Wired connection 1"
```

**创建新连接**：

```bash
# 创建一个使用DHCP的以太网连接
sudo nmcli connection add type ethernet con-name my-ethernet ifname eth0

# 创建一个使用静态IP的以太网连接
sudo nmcli connection add type ethernet con-name my-static-ethernet ifname eth0 \
    ip4 192.168.1.100/24 gw4 192.168.1.1

# 同时指定DNS
sudo nmcli connection modify my-static-ethernet ipv4.dns "8.8.8.8,223.5.5.5"

# 激活连接
sudo nmcli connection up my-static-ethernet
```

**修改现有连接**：

```bash
# 修改IP地址（DHCP改为静态）
sudo nmcli connection modify "Wired connection 1" \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8,223.5.5.5" \
    ipv4.method manual

# 将DHCP模式改回自动
sudo nmcli connection modify "Wired connection 1" ipv4.method auto

# 应用修改（需要重启连接）
sudo nmcli connection down "Wired connection 1" && sudo nmcli connection up "Wired connection 1"
```

### 30.5.2 nmtui 文本界面

如果觉得命令行太硬核，`nmtui`提供了友好的文本图形界面。

```bash
# 启动nmtui
sudo nmtui
```

界面操作方式：

- 用方向键移动光标
- Enter确认选择
- Tab切换选项
- Esc返回上层菜单

nmtui可以做的事：编辑连接、激活/停用连接、设置系统主机名。

## 30.6 主机名配置

主机名（Hostname）是Linux系统的"名字"，用于在网络中标识这台机器。

### 30.6.1 hostname：查看

```bash
# 查看当前主机名
hostname

# 查看主机名（包含域名）
hostname -f
```

```bash
my-server
```

### 30.6.2 /etc/hostname：永久配置

在Debian/Ubuntu和CentOS中，主机名保存在`/etc/hostname`文件中。

```bash
# 查看主机名配置文件
cat /etc/hostname
```

```bash
my-server
```

修改主机名（需要root权限）：

```bash
# 方法1：直接编辑文件
sudo vim /etc/hostname

# 方法2：用hostnamectl命令修改（推荐）
sudo hostnamectl set-hostname new-server-name

# 方法3：用echo修改
sudo echo new-server-name > /etc/hostname
```

修改完后，新主机名不会立即在当前shell中生效，需要重新登录或手动执行：

```bash
sudo hostname new-server-name
```

### 30.6.3 hostnamectl：系统级

`hostnamectl`是systemd提供的综合主机名管理工具，支持三种主机名：

1. **静态主机名（Static）**：`/etc/hostname`里存储的，由管理员设置
2. **瞬态主机名（Transient）**：系统运行时临时设置，重启后丢失
3. **灵活主机名（Pretty）**：人类可读的名字，可以包含特殊字符和空格（如"My Awesome Server"）

```bash
# 查看所有主机名
hostnamectl status
```

```bash
   Static hostname: my-server
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 5a6b7c8d9e0f123456789abcdef01234
           Boot ID: abcdef1234567890abcdef1234567890
    Virtualization: vmware
  Operating System: Ubuntu 22.04.1 LTS
            Kernel: Linux 5.15.0-60-generic
      Architecture: x86-64
```

**设置灵活主机名**：

```bash
# 设置灵活主机名（可以包含空格和特殊字符）
sudo hostnamectl set-hostname "My Awesome Server" --pretty
```

## 30.7 DNS 配置

DNS配置决定了你的Linux系统通过哪个DNS服务器解析域名。

### 30.7.1 /etc/resolv.conf

Linux的DNS配置在`/etc/resolv.conf`文件中。

```bash
cat /etc/resolv.conf
```

```bash
nameserver 8.8.8.8
nameserver 223.5.5.5
nameserver 1.1.1.1
```

`/etc/resolv.conf`中的`nameserver`指令告诉系统用哪个DNS服务器来解析域名。最多可以配置3个nameserver，系统会按顺序尝试解析。

### 30.7.2 nameserver

手动添加DNS服务器：

```bash
# 在resolv.conf中添加DNS服务器
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
```

### 30.7.3 resolv.conf 被覆盖的问题

这是Linux DNS配置中最容易踩的坑——你手动改了`/etc/resolv.conf`，但重启后又被覆盖了！

为什么？因为在很多Linux发行版中，`/etc/resolv.conf`是由DHCP客户端或NetworkManager动态生成的，是"符号链接"或"软链接"指向别处。

检查一下：

```bash
ls -la /etc/resolv.conf
```

```bash
lrwxrwxrwx 1 root root 27 Nov 15 10:00 /etc/resolv.conf -> ../run/resolvconf/resolv.conf
```

如果是符号链接，说明DNS由resolvconf管理。

还有一种情况：

```bash
-rw-r--r-- 1 root root 207 Jan 10 10:00 /etc/resolv.conf
```

这是普通文件，可能是NetworkManager或dhclient覆盖的。

**正确的DNS配置方法**：

在Debian/Ubuntu上，如果用Netplan：

```yaml
# 在Netplan配置中指定DNS（见30.4节）
nameservers:
  addresses:
    - 8.8.8.8
    - 223.5.5.5
```

在CentOS上，编辑`/etc/sysconfig/network-scripts/ifcfg-eth0`，添加：

```
DNS1=8.8.8.8
DNS2=223.5.5.5
```

> **避坑指南**：永远不要直接编辑`/etc/resolv.conf`来永久修改DNS。它会被系统工具覆盖。正确做法是通过Netplan、NetworkManager或网卡配置文件来设置DNS。

## 30.8 /etc/hosts 本地解析

`/etc/hosts`是本地静态的"域名→IP"映射表，优先级比DNS还高。

```bash
# 查看hosts文件
cat /etc/hosts
```

```bash
127.0.0.1   localhost
127.0.1.1   my-server

# 下面是你可以添加的自定义解析
192.168.1.100   mydatabase.local    # 访问数据库服务器
192.168.1.101   myweb.local         # 访问Web服务器
10.0.0.50       gitlab.internal     # 内网GitLab服务器
```

hosts文件的格式：`IP地址    主机名    [别名]`

**使用场景**：

- 开发测试时，给自己定义一个域名（如`myapp.test`指向`127.0.0.1`）
- 内网环境没有DNS服务器时，用hosts文件做域名解析
- 屏蔽广告网站（把广告域名指向`127.0.0.1`）

> **冷知识**：在大型集群环境中，`/etc/hosts`管理是个噩梦——每次加机器都要改一堆服务器的hosts文件。这也是为什么要有DNS的原因。

## 30.9 网络诊断工具

网络配置好了，怎么验证通了？下一章会详细介绍每个工具，这里先给出常用诊断命令的快速用法。

```bash
# 测试网络连通性（需要目标主机回应ICMP）
ping -c 4 8.8.8.8

# 测试DNS解析是否正常
nslookup www.baidu.com

# 查看本机网络接口状态
ip addr

# 查看路由表
ip route

# 查看端口监听状态
ss -tulpn

# 测试端口是否开放（nc工具）
nc -zv 192.168.1.1 80
```

```bash
# ping结果示例
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=118 time=11.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 11.8/12.0/12.3/0.2 ms
```

---

## 本章小结

本章我们实战了Linux网络配置的核心技能：

- **`ip addr/link/route`**：新一代全能网络工具，`ip addr`查IP，`ip link`查网卡，`ip route`查路由表
- **`ifconfig`**：老前辈，服务器运维必须认识，但生产环境推荐用`ip`
- **Debian/Ubuntu网络配置**：`/etc/network/interfaces`文件
- **CentOS网络配置**：`/etc/sysconfig/network-scripts/ifcfg-eth0`文件
- **Netplan**（Ubuntu 18.04+）：YAML声明式配置，配置写在`/etc/netplan/*.yaml`，用`netplan apply`生效
- **NetworkManager**：桌面环境的网络神器，`nmcli`命令行和`nmtui`文本界面
- **主机名**：`/etc/hostname`文件，`hostnamectl`命令管理
- **DNS配置**：通过Netplan或NetworkManager设置，不要直接改`/etc/resolv.conf`
- **本地解析**：`/etc/hosts`文件，优先级高于DNS

网络配置是Linux服务器管理的基础功，配错了就是"失联"。配置前先想清楚，配完后用`ping`验证。
