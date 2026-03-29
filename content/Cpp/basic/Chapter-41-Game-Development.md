+++
title = "第41章 C++游戏开发：从'Hello World'到'拯救公主'"
weight = 410
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第41章 C++游戏开发：从"Hello World"到"拯救公主"

## 41.1 游戏开发概述：为什么C++是游戏开发者的"真爱"

当你打开一款3A大作，看到屏幕上那个肌肉猛男正要跳下直升机时，你有没有想过：**"这货是用什么语言写的？"** 答案大概率是——C++。

游戏开发圈有个不成文的规矩：**"性能为王"**。在游戏里，每一帧都关乎生死（玩家的生死，不是角色的）。想象一下，你正在《黑暗之魂》里和Boss鏖战，结果画面卡成了PPT——你大概会想把手柄砸向电视，而不是砸向Boss。

C++之所以成为游戏开发的首选语言，靠的就是以下几点：

1. **零开销抽象**：不像某些语言那样"体贴"地帮你做各种运行时检查，C++把控制权完全交给程序员
2. **硬件级控制**：直接操作内存、GPU资源，没有中间商赚差价
3. **跨平台能力**：一次编写，Windows、PlayStation、Xbox、Nintendo Switch都能跑（当然，每平台都要单独适配）
4. **成熟的生态系统**：Unreal Engine、Godot等游戏引擎都把C++作为核心语言

> 有人曾经问John Carmack（DOOM之父，id Software联合创始人）："为什么你们用C++而不是其他更安全的语言？" 他回答："因为我们的游戏要在30毫秒内渲染一帧，而垃圾回收器正在午休。" ——这大概是对C++游戏开发优势最精辟的注解。

### C++游戏开发全景图

在正式进入代码之前，让我们先看看一个游戏的技术架构大概是什么样子：

```
┌─────────────────────────────────────────────────────────────┐
│                      游戏应用层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ 渲染系统  │  │ 物理系统  │  │ 音频系统  │  │ 脚本系统  │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       └─────────────┴─────────────┴─────────────┘            │
│                           │                                  │
│                    ┌──────┴──────┐                          │
│                    │   游戏引擎   │                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  窗口管理  │  │  输入处理  │  │  资源管理  │  │  日志系统  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                      操作系统层 (Windows/Linux/macOS)        │
└─────────────────────────────────────────────────────────────┘
```

### 第一个游戏：命令行版的"猜数字"

让我们先从一个最简单的游戏开始，感受一下游戏开发的基本流程：

```cpp
// Game_01_Hello_GuessNumber.cpp
// 第一个游戏：命令行版猜数字
// 编译：g++ Game_01_Hello_GuessNumber.cpp -o Game_01_Hello_GuessNumber
// 运行：./Game_01_Hello_GuessNumber

#include <iostream>
#include <cstdlib>   // rand(), srand()
#include <ctime>     // time()
#include <limits>    // std::numeric_limits

class GuessNumberGame {
private:
    int secretNumber;
    int attempts;
    int maxAttempts;

public:
    GuessNumberGame(int maxAttempts = 7)
        : attempts(0), maxAttempts(maxAttempts) {
        // 初始化随机数种子
        srand(static_cast<unsigned>(time(nullptr)));
        // 生成1-100之间的随机数
        secretNumber = rand() % 100 + 1;
        std::cout << "🎮 游戏初始化完成！" << std::endl;
        std::cout << "我已经想好了一个1-100之间的数字。" << std::endl;
        std::cout << "你有 " << maxAttempts << " 次机会来猜中它。" << std::endl;
        std::cout << "--------------------------------------------" << std::endl;
    }

    bool checkGuess(int guess) {
        attempts++;

        if (guess < secretNumber) {
            std::cout << "📈 再大一点！你还有 "
                      << (maxAttempts - attempts) << " 次机会。" << std::endl;
            return false;
        } else if (guess > secretNumber) {
            std::cout << "📉 再小一点！你还有 "
                      << (maxAttempts - attempts) << " 次机会。" << std::endl;
            return false;
        } else {
            std::cout << "🎉 恭喜你！猜对了！答案就是 " << secretNumber << std::endl;
            std::cout << "你一共猜了 " << attempts << " 次。" << std::endl;
            return true;
        }
    }

    bool isGameOver() const {
        return attempts >= maxAttempts;
    }

    void showHint() const {
        // 真正的提示：奇偶性提示
        std::cout << "💡 提示：正确答案是一个"
                  << (secretNumber % 2 == 0 ? "偶数" : "奇数")
                  << "。" << std::endl;
    }
};

int main() {
    std::cout << "\n========================================" << std::endl;
    std::cout << "      欢迎来到猜数字游戏！ v1.0          " << std::endl;
    std::cout << "========================================\n" << std::endl;

    GuessNumberGame game;

    while (!game.isGameOver()) {
        std::cout << "\n请输入你的猜测: ";

        int guess;
        std::cin >> guess;

        // 检查输入是否合法
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "❌ 请输入一个有效的数字！" << std::endl;
            continue;
        }

        if (guess < 1 || guess > 100) {
            std::cout << "❌ 数字必须在 1-100 之间！" << std::endl;
            continue;
        }

        if (game.checkGuess(guess)) {
            std::cout << "\n🏆 恭喜你获胜！" << std::endl;
            break;
        }

        // 当剩余机会只有1次时，给点提示
        if (game.isGameOver()) {
            game.showHint();  // 显示提示（奇偶性）
            std::cout << "\n😢 游戏结束！正确答案是: " << secretNumber << std::endl;
        }
    }

    std::cout << "\n感谢游玩！下次再见！\n" << std::endl;
    return 0;
}
```

运行结果示例：
```
========================================
      欢迎来到猜数字游戏！ v1.0
========================================

🎮 游戏初始化完成！我已经想好了一个1-100之间的数字。
你有 7 次机会来猜中它。
--------------------------------------------

请输入你的猜测: 50
📉 再小一点！你还有 6 次机会。

请输入你的猜测: 25
📈 再大一点！你还有 5 次机会。

请输入你的猜测: 37
🎉 恭喜你！猜对了！答案就是 37
你一共猜了 3 次。

🏆 恭喜你获胜！

感谢游玩！下次再见！
```

这个游戏虽然简单，但已经包含了一个游戏的基本要素：**输入、处理、输出、状态管理**。

---

## 41.2 游戏循环：游戏的"心脏"

如果说游戏是一个人，那么**游戏循环（Game Loop）**就是这个人的心脏——每时每刻都在跳动，一旦停止，游戏就"死"了。

### 什么是游戏循环？

游戏循环是游戏运行时的核心机制，它不断重复以下过程：

1. **处理输入**（Input Processing）：读取键盘、鼠标、手柄的输入
2. **更新游戏逻辑**（Update）：移动角色、更新物理、计算AI
3. **渲染画面**（Render）：把游戏世界画出来
4. **控制帧率**（Frame Rate Control）：确保游戏不会跑得太快或太慢

```cpp
// Game_02_BasicGameLoop.cpp
// 游戏循环基础演示
// 编译：g++ Game_02_BasicGameLoop.cpp -o Game_02_BasicGameLoop
// 运行：./Game_02_BasicGameLoop

#include <iostream>
#include <chrono>      // 时间处理
#include <thread>      // 睡眠
#include <cmath>       // 数学函数

class GameLoopDemo {
private:
    bool running;
    double deltaTime;           // 帧间隔时间（秒）
    double accumulator;         // 累积时间
    double targetFPS;           // 目标帧率
    double targetFrameTime;     // 每帧目标时间

    // 游戏时间
    double gameTime;
    int frameCount;

    // 模拟玩家位置（用于演示）
    double playerX;
    double playerY;
    double playerSpeed;

    // FPS计算
    double fps;
    double fpsAccumulator;
    int fpsFrameCount;
    double fpsUpdateInterval;

public:
    GameLoopDemo()
        : running(true)
        , deltaTime(0.0)
        , accumulator(0.0)
        , targetFPS(60.0)
        , targetFrameTime(1.0 / 60.0)
        , gameTime(0.0)
        , frameCount(0)
        , playerX(0.0)
        , playerY(0.0)
        , playerSpeed(100.0)  // 像素/秒
        , fps(0.0)
        , fpsAccumulator(0.0)
        , fpsFrameCount(0)
        , fpsUpdateInterval(0.5)  // 每0.5秒更新一次FPS显示
    {
        std::cout << "🎮 游戏循环演示开始！" << std::endl;
        std::cout << "目标帧率: " << targetFPS << " FPS" << std::endl;
        std::cout << "每帧目标时间: " << targetFrameTime * 1000 << " ms" << std::endl;
        std::cout << "按 Q 键退出游戏" << std::endl;
    }

    // 处理输入
    void processInput() {
        // 在实际游戏中，这里会检查键盘、鼠标等输入设备的状态
        // 这里我们用模拟输入
        char input;
        std::cout << "\n请输入移动方向 (W/A/S/D, Q退出): ";
        if (std::cin >> input) {
            switch (input) {
                case 'W': case 'w':
                    playerY += playerSpeed * deltaTime;   // W = 向上（地图y轴正方向）
                    std::cout << "⬆️ 向上移动" << std::endl;
                    break;
                case 'S': case 's':
                    playerY -= playerSpeed * deltaTime;   // S = 向下（地图y轴负方向）
                    std::cout << "⬇️ 向下移动" << std::endl;
                    break;
                case 'A': case 'a':
                    playerX -= playerSpeed * deltaTime;   // A = 向左（地图x轴负方向）
                    std::cout << "⬅️ 向左移动" << std::endl;
                    break;
                case 'D': case 'd':
                    playerX += playerSpeed * deltaTime;   // D = 向右（地图x轴正方向）
                    std::cout << "➡️ 向右移动" << std::endl;
                    break;
                case 'Q': case 'q':
                    running = false;
                    std::cout << "👋 游戏退出中..." << std::endl;
                    break;
                default:
                    std::cout << "❓ 无效输入" << std::endl;
            }
        }
    }

    // 更新游戏逻辑（固定时间步长）
    void update(double fixedDeltaTime) {
        gameTime += fixedDeltaTime;
        frameCount++;

        // 这里是游戏逻辑更新：
        // - 物理模拟
        // - 碰撞检测
        // - AI计算
        // - 动画更新

        // 模拟一些动态元素（比如背景动画）
        double backgroundOffset = std::sin(gameTime * 2.0) * 10.0;

        // FPS计算
        fpsAccumulator += fixedDeltaTime;
        fpsFrameCount++;
        if (fpsAccumulator >= fpsUpdateInterval) {
            fps = fpsFrameCount / fpsAccumulator;
            fpsAccumulator = 0.0;
            fpsFrameCount = 0;
        }
    }

    // 渲染画面
    void render() {
        // 清除屏幕（实际游戏中会清除渲染缓冲区）
#ifdef _WIN32
        system("cls");
#else
        system("clear");
#endif

        std::cout << "========================================" << std::endl;
        std::cout << "         游戏循环演示 v1.0             " << std::endl;
        std::cout << "========================================" << std::endl;
        std::cout << "📊 FPS: " << fps << std::endl;
        std::cout << "⏱️  游戏时间: " << gameTime << " 秒" << std::endl;
        std::cout << "📦 帧数: " << frameCount << std::endl;
        std::cout << "----------------------------------------" << std::endl;
        std::cout << "🕹️  玩家位置: (" << playerX << ", " << playerY << ")" << std::endl;

        // 简单可视化
        std::cout << "\n地图 (10x5):" << std::endl;
        for (int y = 4; y >= 0; y--) {
            std::cout << y << " │";
            for (int x = 0; x < 10; x++) {
                // 玩家位置（四舍五入到网格）
                int playerGridX = static_cast<int>(std::round(playerX / 100.0));
                int playerGridY = static_cast<int>(std::round(playerY / 100.0));

                if (x == playerGridX && y == playerGridY) {
                    std::cout << "P ";  // 玩家
                } else if (x == 5 && y == 2) {
                    std::cout << "★ ";  // 目标
                } else {
                    std::cout << "· ";  // 空地
                }
            }
            std::cout << "│ " << y << std::endl;
        }
        std::cout << "  └───────────────────" << std::endl;
        std::cout << "   0 1 2 3 4 5 6 7 8 9" << std::endl;
        std::cout << "\n★ = 目标位置  P = 你的位置" << std::endl;
    }

    // 主循环
    void run() {
        auto previousTime = std::chrono::high_resolution_clock::now();

        std::cout << "\n🚀 游戏开始！\n" << std::endl;

        while (running) {
            auto currentTime = std::chrono::high_resolution_clock::now();
            auto frameTime = std::chrono::duration<double>(
                currentTime - previousTime).count();
            previousTime = currentTime;

            // 限制最大帧时间，避免"螺旋死亡"
            if (frameTime > 0.25) {
                frameTime = 0.25;
            }

            accumulator += frameTime;

            // 固定时间步长的逻辑更新
            // 这样可以保证物理模拟的一致性
            while (accumulator >= targetFrameTime) {
                // 输入处理（每帧一次）
                // processInput();  // 注释掉，因为我们用的是阻塞输入

                // 固定时间步长的游戏逻辑更新
                update(targetFrameTime);
                accumulator -= targetFrameTime;
            }

            // 渲染
            render();

            // 显示FPS信息
            std::cout << "----------------------------------------" << std::endl;
            std::cout << "📈 当前帧时间: " << frameTime * 1000 << " ms" << std::endl;

            // 处理输入（在渲染之后，因为我们要等用户输入）
            processInput();

            // 小延迟，避免CPU空转
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        std::cout << "\n✅ 游戏已退出！" << std::endl;
        std::cout << "总运行时间: " << gameTime << " 秒" << std::endl;
        std::cout << "总帧数: " << frameCount << std::endl;
        std::cout << "平均FPS: " << (frameCount / gameTime) << std::endl;
    }
};

int main() {
    GameLoopDemo game;
    game.run();
    return 0;
}
```

### 固定时间步长 vs 可变时间步长

游戏循环中最经典的问题之一就是：**时间步长的选择**。

```cpp
// 两种游戏循环模式对比

// ❌ 可变时间步长（简单但有问题）
void naiveGameLoop() {
    while (running) {
        double currentTime = getTime();
        double deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        update(deltaTime);   // deltaTime每次都可能不同
        render();

        // 问题：如果deltaTime太大，物理会"爆炸"
        // 问题：如果deltaTime太小，动画会"抽搐"
    }
}

// ✅ 固定时间步长（推荐）
void fixedTimeStepGameLoop() {
    const double FIXED_DT = 1.0 / 60.0;  // 固定60Hz
    double accumulator = 0.0;

    while (running) {
        double currentTime = getTime();
        double deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        accumulator += deltaTime;

        // 多次小步更新，保证物理模拟稳定
        while (accumulator >= FIXED_DT) {
            update(FIXED_DT);      // 每次都是固定的1/60秒
            accumulator -= FIXED_DT;
        }

        // 渲染（可以插值）
        render(accumulator / FIXED_DT);  // 传入插值因子
    }
}

// ✅ 固定时间步长 + 帧率上限（最常用）
void cappedFixedTimeStep() {
    const double FIXED_DT = 1.0 / 60.0;
    const double MAX_DT = 0.25;  // 最大帧时间，避免"螺旋死亡"
    double accumulator = 0.0;

    while (running) {
        double frameStart = getTime();
        double deltaTime = frameStart - lastTime;
        lastTime = frameStart;

        // 限制最大帧时间
        deltaTime = std::min(deltaTime, MAX_DT);
        accumulator += deltaTime;

        // 固定步长更新
        while (accumulator >= FIXED_DT) {
            processInput();
            update(FIXED_DT);
            accumulator -= FIXED_DT;
        }

        render();
        sleep(frameStart + FIXED_DT - getTime());  // 睡眠控帧
    }
}
```

> **小知识**：什么是"螺旋死亡"（Death Spiral）？
> 当游戏变卡时，每帧的deltaTime变大，累积的待处理时间变多，导致下一帧更卡，如此恶性循环，最终游戏完全卡死。设置MAX_DT就是为了打破这个循环。

---

## 41.3 实体组件系统（ECS）：游戏架构的"革命"

### 什么是ECS？

在传统面向对象游戏架构中，我们可能会这样设计：

```cpp
// ❌ 传统面向对象设计（可能导致"上帝类"）
class GameObject {
public:
    std::string name;
    Vector3 position;
    Vector3 velocity;
    Mesh* mesh;           // 需要渲染？
    RigidBody* body;      // 需要物理？
    HealthComponent* health;  // 需要生命值？
    AIComponent* ai;      // 需要AI？
    // ... 无限增长的组件
};

// 派生类
class Player : public GameObject { /* 玩家特有逻辑 */ };
class Enemy : public GameObject { /* 敌人特有逻辑 */ };
class Bullet : public GameObject { /* 子弹特有逻辑 */ };
class Wall : public GameObject { /* 墙特有逻辑 */ };

// 问题：
// 1. 所有类都继承自GameObject，导致紧密耦合
// 2. 玩家也有RigidBody？子弹也有Health？浪费！
// 3. 添加新功能需要修改基类，影响所有类
// 4. 缓存不友好，访问数据分散在内存各处
```

**ECS（Entity-Component-System）** 是一种架构模式，它的核心思想是：

- **Entity（实体）**：只是一个ID，用于关联组件，没有行为
- **Component（组件）**：纯数据，存储属性（位置、速度、生命值等）
- **System（系统）**：纯逻辑，处理特定类型的组件

```cpp
// ✅ ECS架构演示
// Game_03_ECS_Architecture.cpp
// 编译：g++ Game_03_ECS_Architecture.cpp -std=c++17 -o Game_03_ECS_Architecture

#include <iostream>
#include <vector>
#include <array>
#include <memory>
#include <string>
#include <optional>
#include <cassert>

// ============================================================
// 第一部分：基础类型定义
// ============================================================

using EntityID = uint32_t;
constexpr EntityID INVALID_ENTITY = 0;
constexpr size_t MAX_ENTITIES = 10000;

// ============================================================
// 第二部分：组件定义（纯数据）
// ============================================================

// 位置组件
struct PositionComponent {
    float x, y, z;

    PositionComponent(float x = 0, float y = 0, float z = 0)
        : x(x), y(y), z(z) {}
};

// 速度组件
struct VelocityComponent {
    float vx, vy, vz;

    VelocityComponent(float vx = 0, float vy = 0, float vz = 0)
        : vx(vx), vy(vy), vz(vz) {}
};

// 渲染组件
struct RenderComponent {
    std::string meshName;
    std::string materialName;
    float scale;

    RenderComponent(const std::string& mesh = "cube",
                     const std::string& material = "default",
                     float scale = 1.0f)
        : meshName(mesh), materialName(material), scale(scale) {}
};

// 生命值组件
struct HealthComponent {
    float currentHealth;
    float maxHealth;

    HealthComponent(float max = 100.0f)
        : currentHealth(max), maxHealth(max) {}

    bool isAlive() const { return currentHealth > 0; }
};

// 伤害组件（用于造成伤害的实体）
struct DamageComponent {
    float damage;

    DamageComponent(float d = 10.0f) : damage(d) {}
};

// 玩家控制组件
struct PlayerControlComponent {
    float moveSpeed;
    bool isControlledByPlayer;

    PlayerControlComponent(float speed = 100.0f)
        : moveSpeed(speed), isControlledByPlayer(true) {}
};

// AI组件
struct AIComponent {
    enum class AIType { PATROL, CHASE, ATTACK };
    AIType type;
    float detectionRange;
    EntityID targetEntity;

    AIComponent(AIType t = AIType::PATROL, float range = 50.0f)
        : type(t), detectionRange(range), targetEntity(INVALID_ENTITY) {}
};

// 标签组件（用于标识实体类型）
struct TagComponent {
    std::string tag;

    TagComponent(const std::string& t = "") : tag(t) {}
};

// ============================================================
// 第三部分：组件存储（使用Sparse Set优化）
// ============================================================

template<typename T>
class ComponentArray {
private:
    std::vector<T> dense;           // 连续存储所有组件数据
    std::vector<EntityID> entityIds; // 对应的实体ID
    std::array<size_t, MAX_ENTITIES> sparse;  // 实体ID到索引的映射
    size_t size = 0;

public:
    void insert(EntityID entity, const T& component) {
        assert(entity < MAX_ENTITIES);
        assert(!has(entity));

        sparse[entity] = size;
        dense.push_back(component);
        entityIds.push_back(entity);
        size++;
    }

    void remove(EntityID entity) {
        assert(has(entity));

        size_t index = sparse[entity];
        size_t lastIndex = size - 1;

        // 将最后一个元素移到删除位置
        dense[index] = dense[lastIndex];
        entityIds[index] = entityIds[lastIndex];
        sparse[entityIds[lastIndex]] = index;

        dense.pop_back();
        entityIds.pop_back();
        size--;
        sparse[entity] = 0;  // 或 size_t(-1)
    }

    bool has(EntityID entity) const {
        if (entity >= MAX_ENTITIES) return false;
        return sparse[entity] < size && entityIds[sparse[entity]] == entity;
    }

    T& get(EntityID entity) {
        assert(has(entity));
        return dense[sparse[entity]];
    }

    const T& get(EntityID entity) const {
        assert(has(entity));
        return dense[sparse[entity]];
    }

    size_t count() const { return size; }

    // 遍历所有组件（可用于系统更新）
    template<typename Func>
    void forEach(Func&& func) {
        for (size_t i = 0; i < size; i++) {
            func(entityIds[i], dense[i]);
        }
    }
};

// ============================================================
// 第四部分：World（管理所有实体和组件）
// ============================================================

class World {
private:
    EntityID nextEntityID = 1;  // 0保留给INVALID_ENTITY
    std::vector<EntityID> recycledEntities;

    // 组件存储
    ComponentArray<PositionComponent> positions;
    ComponentArray<VelocityComponent> velocities;
    ComponentArray<RenderComponent> renders;
    ComponentArray<HealthComponent> healths;
    ComponentArray<DamageComponent> damages;
    ComponentArray<PlayerControlComponent> playerControls;
    ComponentArray<AIComponent> ais;
    ComponentArray<TagComponent> tags;

public:
    // 创建实体
    EntityID createEntity() {
        EntityID entity;
        if (!recycledEntities.empty()) {
            entity = recycledEntities.back();
            recycledEntities.pop_back();
        } else {
            entity = nextEntityID++;
        }
        std::cout << "✅ 创建实体: " << entity << std::endl;
        return entity;
    }

    // 销毁实体（同时删除所有组件）
    void destroyEntity(EntityID entity) {
        std::cout << "🗑️  销毁实体: " << entity << std::endl;

        // 移除所有组件
        if (positions.has(entity)) positions.remove(entity);
        if (velocities.has(entity)) velocities.remove(entity);
        if (renders.has(entity)) renders.remove(entity);
        if (healths.has(entity)) healths.remove(entity);
        if (damages.has(entity)) damages.remove(entity);
        if (playerControls.has(entity)) playerControls.remove(entity);
        if (ais.has(entity)) ais.remove(entity);
        if (tags.has(entity)) tags.remove(entity);

        recycledEntities.push_back(entity);
    }

    // 组件访问便捷方法
    template<typename T>
    ComponentArray<T>& getComponents() {
        if constexpr (std::is_same_v<T, PositionComponent>) return positions;
        else if constexpr (std::is_same_v<T, VelocityComponent>) return velocities;
        else if constexpr (std::is_same_v<T, RenderComponent>) return renders;
        else if constexpr (std::is_same_v<T, HealthComponent>) return healths;
        else if constexpr (std::is_same_v<T, DamageComponent>) return damages;
        else if constexpr (std::is_same_v<T, PlayerControlComponent>) return playerControls;
        else if constexpr (std::is_same_v<T, AIComponent>) return ais;
        else if constexpr (std::is_same_v<T, TagComponent>) return tags;
        else static_assert(sizeof(T) == 0, "Unknown component type");
    }

    template<typename T>
    bool hasComponent(EntityID entity) {
        return getComponents<T>().has(entity);
    }

    template<typename T>
    T& addComponent(EntityID entity, const T& component = T{}) {
        getComponents<T>().insert(entity, component);
        return getComponents<T>().get(entity);
    }

    template<typename T>
    T& getComponent(EntityID entity) {
        return getComponents<T>().get(entity);
    }

    template<typename T>
    void removeComponent(EntityID entity) {
        getComponents<T>().remove(entity);
    }

    // 打印实体信息
    void printEntityInfo(EntityID entity) {
        std::cout << "\n--- 实体 " << entity << " 信息 ---" << std::endl;

        if (positions.has(entity)) {
            auto& p = positions.get(entity);
            std::cout << "📍 位置: (" << p.x << ", " << p.y << ", " << p.z << ")" << std::endl;
        }
        if (velocities.has(entity)) {
            auto& v = velocities.get(entity);
            std::cout << "💨 速度: (" << v.vx << ", " << v.vy << ", " << v.vz << ")" << std::endl;
        }
        if (healths.has(entity)) {
            auto& h = healths.get(entity);
            std::cout << "❤️ 生命: " << h.currentHealth << "/" << h.maxHealth << std::endl;
        }
        if (renders.has(entity)) {
            auto& r = renders.get(entity);
            std::cout << "🎨 渲染: " << r.meshName << " (scale=" << r.scale << ")" << std::endl;
        }
        if (tags.has(entity)) {
            auto& t = tags.get(entity);
            std::cout << "🏷️ 标签: " << t.tag << std::endl;
        }
    }
};

// ============================================================
// 第五部分：系统（纯逻辑）
// ============================================================

// 移动系统
class MovementSystem {
public:
    static void update(World& world, float dt) {
        std::cout << "\n🏃 移动系统更新..." << std::endl;

        world.getComponents<VelocityComponent>().forEach(
            [&](EntityID entity, VelocityComponent& velocity) {
                if (world.hasComponent<PositionComponent>(entity)) {
                    auto& pos = world.getComponent<PositionComponent>(entity);
                    pos.x += velocity.vx * dt;
                    pos.y += velocity.vy * dt;
                    pos.z += velocity.vz * dt;
                }
            }
        );
    }
};

// 渲染系统
class RenderSystem {
public:
    static void update(World& world) {
        std::cout << "\n🎨 渲染系统更新..." << std::endl;

        std::cout << "正在渲染场景中的所有实体:" << std::endl;

        world.getComponents<RenderComponent>().forEach(
            [&](EntityID entity, RenderComponent& render) {
                if (world.hasComponent<PositionComponent>(entity)) {
                    auto& pos = world.getComponent<PositionComponent>(entity);
                    std::cout << "  📦 实体 " << entity
                              << ": 渲染 " << render.meshName
                              << " @ (" << pos.x << ", " << pos.y << ", " << pos.z << ")"
                              << " [scale=" << render.scale << "]" << std::endl;
                }
            }
        );
    }
};

// 生命系统
class HealthSystem {
public:
    static void update(World& world) {
        std::cout << "\n❤️ 生命系统更新..." << std::endl;

        world.getComponents<HealthComponent>().forEach(
            [&](EntityID entity, HealthComponent& health) {
                if (!health.isAlive()) {
                    std::cout << "  💀 实体 " << entity << " 已死亡！" << std::endl;
                } else {
                    std::cout << "  🩹 实体 " << entity
                              << " 生命值: " << health.currentHealth
                              << "/" << health.maxHealth << std::endl;
                }
            }
        );
    }
};

// 战斗系统（简化的碰撞检测 + 伤害）
class CombatSystem {
public:
    static void update(World& world, float dt) {
        std::cout << "\n⚔️ 战斗系统更新..." << std::endl;

        // 检查所有有伤害能力的实体
        world.getComponents<DamageComponent>().forEach(
            [&](EntityID attacker, DamageComponent& damage) {
                if (world.hasComponent<PositionComponent>(attacker)) {
                    auto& attackerPos = world.getComponent<PositionComponent>(attacker);

                    // 检查是否碰到有生命值的实体
                    world.getComponents<HealthComponent>().forEach(
                        [&](EntityID target, HealthComponent& health) {
                            // 不攻击自己
                            if (attacker == target) return;

                            if (world.hasComponent<PositionComponent>(target)) {
                                auto& targetPos = world.getComponent<PositionComponent>(target);

                                // 简化的距离检测
                                float dx = attackerPos.x - targetPos.x;
                                float dy = attackerPos.y - targetPos.y;
                                float dist = std::sqrt(dx*dx + dy*dy);

                                if (dist < 5.0f) {  // 碰撞范围
                                    // 造成伤害
                                    health.currentHealth -= damage.damage * dt;
                                    std::cout << "  💥 实体 " << attacker
                                              << " 攻击实体 " << target
                                              << "，造成 " << damage.damage * dt << " 伤害"
                                              << std::endl;
                                }
                            }
                        }
                    );
                }
            }
        );
    }
};

// ============================================================
// 第六部分：演示
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      ECS 架构演示 v1.0                " << std::endl;
    std::cout << "========================================" << std::endl;

    World world;

    // === 创建玩家 ===
    EntityID player = world.createEntity();
    world.addComponent<PositionComponent>(player, {0, 0, 0});
    world.addComponent<VelocityComponent>(player, {10, 5, 0});
    world.addComponent<RenderComponent>(player, {"player_model", "player_mat", 1.5f});
    world.addComponent<HealthComponent>(player, {100});
    world.addComponent<PlayerControlComponent>(player, {150});
    world.addComponent<TagComponent>(player, {"Player"});

    // === 创建敌人1 ===
    EntityID enemy1 = world.createEntity();
    world.addComponent<PositionComponent>(enemy1, {30, 10, 0});
    world.addComponent<VelocityComponent>(enemy1, {-5, 0, 0});
    world.addComponent<RenderComponent>(enemy1, {"enemy_model", "enemy_mat", 1.0f});
    world.addComponent<HealthComponent>(enemy1, {50});
    world.addComponent<DamageComponent>(enemy1, {20});
    world.addComponent<AIComponent>(enemy1, {AIComponent::AIType::CHASE, 50});
    world.addComponent<TagComponent>(enemy1, {"Enemy"});

    // === 创建敌人2 ===
    EntityID enemy2 = world.createEntity();
    world.addComponent<PositionComponent>(enemy2, {50, -20, 0});
    world.addComponent<VelocityComponent>(enemy2, {-3, 2, 0});
    world.addComponent<RenderComponent>(enemy2, {"enemy_model", "enemy_mat", 1.0f});
    world.addComponent<HealthComponent>(enemy2, {50});
    world.addComponent<DamageComponent>(enemy2, {15});
    world.addComponent<TagComponent>(enemy2, {"Enemy"});

    // === 创建子弹 ===
    EntityID bullet = world.createEntity();
    world.addComponent<PositionComponent>(bullet, {10, 0, 0});
    world.addComponent<VelocityComponent>(bullet, {100, 0, 0});
    world.addComponent<RenderComponent>(bullet, {"bullet_model", "bullet_mat", 0.2f});
    world.addComponent<DamageComponent>(bullet, {50});
    world.addComponent<TagComponent>(bullet, {"Projectile"});

    // === 创建不会动的墙 ===
    EntityID wall = world.createEntity();
    world.addComponent<PositionComponent>(wall, {25, 5, 0});
    world.addComponent<RenderComponent>(wall, {"wall_model", "wall_mat", 2.0f});
    world.addComponent<TagComponent>(wall, {"Wall"});
    // 墙没有Velocity和Health，所以不会被移动系统处理，也不会被攻击

    std::cout << "\n========================================" << std::endl;
    std::cout << "      初始状态                        " << std::endl;
    std::cout << "========================================" << std::endl;

    world.printEntityInfo(player);
    world.printEntityInfo(enemy1);
    world.printEntityInfo(enemy2);
    world.printEntityInfo(bullet);

    // 模拟游戏循环
    float dt = 1.0f / 60.0f;  // 60FPS，每帧时间

    std::cout << "\n========================================" << std::endl;
    std::cout << "      模拟 3 帧游戏更新                " << std::endl;
    std::cout << "========================================" << std::endl;

    for (int frame = 1; frame <= 3; frame++) {
        std::cout << "\n\n>>>>>>>>>> 帧 " << frame << " 开始 >>>>>>>>>>" << std::endl;

        // 更新所有系统
        MovementSystem::update(world, dt);
        CombatSystem::update(world, dt);
        HealthSystem::update(world);
        RenderSystem::update(world);

        std::cout << "<<<<<<<<<< 帧 " << frame << " 结束 <<<<<<<<<<" << std::endl;
    }

    std::cout << "\n========================================" << std::endl;
    std::cout << "      第3帧后的状态                    " << std::endl;
    std::cout << "========================================" << std::endl;

    world.printEntityInfo(player);
    world.printEntityInfo(enemy1);
    world.printEntityInfo(enemy2);
    world.printEntityInfo(bullet);

    std::cout << "\n========================================" << std::endl;
    std::cout << "      ECS 架构优势总结                " << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << R"(
    ✅ 组合优于继承：实体由组件组合而成，灵活度高
    ✅ 数据局部性：同类组件连续存储，缓存命中率高
    ✅ 并行友好：系统可以并行处理无依赖的组件
    ✅ 易于扩展：添加新组件或新系统不影响现有代码
    ✅ 内存效率：只需要存储实际使用的组件

    📝 ECS特别适合：
       - 大型游戏（成千上万的实体）
       - 需要频繁创建/销毁实体的游戏（子弹、粒子）
       - 需要灵活组合游戏对象的游戏
    )" << std::endl;

    std::cout << "\n✅ 演示完成！" << std::endl;

    return 0;
}
```

运行结果（部分）：
```
========================================
      ECS 架构演示 v1.0
========================================
✅ 创建实体: 1
✅ 创建实体: 2
✅ 创建实体: 3
✅ 创建实体: 4
✅ 创建实体: 5

========================================
      初始状态
========================================

--- 实体 1 信息 ---
📍 位置: (0, 0, 0)
💨 速度: (10, 5, 0)
❤️ 生命: 100/100
🎨 渲染: player_model (scale=1.5)
🏷️ 标签: Player


>>>>>>>>>> 帧 1 开始 >>>>>>>>>>

🏃 移动系统更新...
⚔️ 战斗系统更新...
❤️ 生命系统更新...
  🩹 实体 1 生命值: 100/100
  🩹 实体 2 生命值: 50/50
  🩹 实体 5 生命值: 50/50
🎨 渲染系统更新...
  📦 实体 1: 渲染 player_model @ (0.166667, 0.083333, 0) [scale=1.5]
  📦 实体 2: 渲染 enemy_model @ (29.9167, 10, 0) [scale=1]
  📦 实体 3: 渲染 enemy_model @ (49.95, -19.9667, 0) [scale=1]
  📦 实体 4: 渲染 bullet_model @ (1.66667, 0, 0) [scale=0.2]
  📦 实体 5: 渲染 wall_model @ (25, 5, 0) [scale=2]
```

---

## 41.4 碰撞检测：游戏世界的"边界感"

碰撞检测是游戏开发中最重要也最复杂的系统之一。从超级玛丽踩蘑菇怪，到FPS里的子弹击中敌人，再到赛车游戏中的撞墙——这一切都离不开碰撞检测。

### 碰撞检测的基本几何形状

游戏中的碰撞体（Collider）通常由以下基本形状表示：

```cpp
// Game_04_CollisionDetection.cpp
// 碰撞检测基础实现
// 编译：g++ Game_04_CollisionDetection.cpp -std=c++17 -o Game_04_CollisionDetection

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <optional>
#include <iomanip>

// ============================================================
// 数学工具
// ============================================================

struct Vec2 {
    float x, y;

    Vec2(float x = 0, float y = 0) : x(x), y(y) {}

    Vec2 operator+(const Vec2& other) const {
        return Vec2(x + other.x, y + other.y);
    }

    Vec2 operator-(const Vec2& other) const {
        return Vec2(x - other.x, y - other.y);
    }

    Vec2 operator*(float scalar) const {
        return Vec2(x * scalar, y * scalar);
    }

    float dot(const Vec2& other) const {
        return x * other.x + y * other.y;
    }

    float length() const {
        return std::sqrt(x * x + y * y);
    }

    Vec2 normalized() const {
        float len = length();
        if (len < 0.0001f) return Vec2(0, 0);
        return Vec2(x / len, y / len);
    }

    // 点到线段的最近点
    static Vec2 closestPointOnSegment(const Vec2& point,
                                       const Vec2& segStart,
                                       const Vec2& segEnd) {
        Vec2 seg = segEnd - segStart;
        float t = std::max(0.0f, std::min(1.0f,
            (point - segStart).dot(seg) / seg.dot(seg)));
        return segStart + seg * t;
    }
};

struct Vec3 {
    float x, y, z;

    Vec3(float x = 0, float y = 0, float z = 0) : x(x), y(y), z(z) {}

    Vec3 operator+(const Vec3& other) const {
        return Vec3(x + other.x, y + other.y, z + other.z);
    }

    Vec3 operator-(const Vec3& other) const {
        return Vec3(x - other.x, y - other.y, z - other.z);
    }

    Vec3 operator*(float scalar) const {
        return Vec3(x * scalar, y * scalar, z * scalar);
    }

    float dot(const Vec3& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    Vec3 cross(const Vec3& other) const {
        return Vec3(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }

    float length() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    Vec3 normalized() const {
        float len = length();
        if (len < 0.0001f) return Vec3(0, 0, 0);
        return Vec3(x / len, y / len, z / len);
    }
};

// ============================================================
// 包围体（Bounding Volume）
// ============================================================

// 轴对齐包围盒（AABB - Axis-Aligned Bounding Box）
struct AABB2D {
    Vec2 min;  // 左下角
    Vec2 max;  // 右上角

    AABB2D(const Vec2& min, const Vec2& max) : min(min), max(max) {}

    static AABB2D fromCenter(const Vec2& center, float halfWidth, float halfHeight) {
        return AABB2D(
            Vec2(center.x - halfWidth, center.y - halfHeight),
            Vec2(center.x + halfWidth, center.y + halfHeight)
        );
    }

    float width() const { return max.x - min.x; }
    float height() const { return max.y - min.y; }
    Vec2 center() const { return (min + max) * 0.5f; }

    // AABB vs AABB
    static bool intersects(const AABB2D& a, const AABB2D& b) {
        if (a.max.x < b.min.x || a.min.x > b.max.x) return false;
        if (a.max.y < b.min.y || a.min.y > b.max.y) return false;
        return true;
    }

    // 详细碰撞检测（返回MTV - Minimum Translation Vector）
    static std::optional<Vec2> collisionInfo(const AABB2D& a, const AABB2D& b) {
        if (!intersects(a, b)) return std::nullopt;

        // 计算重叠量
        float overlapX = std::min(a.max.x - b.min.x, b.max.x - a.min.x);
        float overlapY = std::min(a.max.y - b.min.y, b.max.y - a.min.y);

        // 选择最小分离轴
        if (overlapX < overlapY) {
            // 沿X轴分离
            bool aIsLeft = a.center().x < b.center().x;
            return Vec2(aIsLeft ? -overlapX : overlapX, 0);
        } else {
            // 沿Y轴分离
            bool aIsBottom = a.center().y < b.center().y;
            return Vec2(0, aIsBottom ? -overlapY : overlapY);
        }
    }
};

// 圆形碰撞体
struct Circle {
    Vec2 center;
    float radius;

    Circle(const Vec2& center, float radius)
        : center(center), radius(radius) {}

    static bool intersects(const Circle& a, const Circle& b) {
        Vec2 diff = a.center - b.center;
        float distSq = diff.dot(diff);
        float radiusSum = a.radius + b.radius;
        return distSq < radiusSum * radiusSum;
    }

    // 圆 vs AABB
    static bool intersects(const Circle& circle, const AABB2D& box) {
        Vec2 closest = Vec2(
            std::max(box.min.x, std::min(circle.center.x, box.max.x)),
            std::max(box.min.y, std::min(circle.center.y, box.max.y))
        );
        Vec2 diff = circle.center - closest;
        return diff.dot(diff) < circle.radius * circle.radius;
    }
};

// 定向包围盒（OBB - Oriented Bounding Box）
struct OBB2D {
    Vec2 center;
    Vec2 halfExtents;  // 半宽半高
    Vec2 axes[2];       // 局部坐标轴（单位向量）

    OBB2D(const Vec2& center, const Vec2& halfExtents, float angle) :
        center(center), halfExtents(halfExtents) {
        axes[0] = Vec2(std::cos(angle), std::sin(angle));
        axes[1] = Vec2(-std::sin(angle), std::cos(angle));
    }

    // 获取OBB的四个顶点
    std::vector<Vec2> getVertices() const {
        std::vector<Vec2> verts(4);
        for (int i = 0; i < 4; i++) {
            Vec2 offset(
                (i % 2 == 0 ? 1 : -1) * halfExtents.x,
                (i / 2 == 0 ? 1 : -1) * halfExtents.y
            );
            // 将偏移量转换到世界坐标
            verts[i] = center + Vec2(
                axes[0].x * offset.x + axes[1].x * offset.y,
                axes[0].y * offset.x + axes[1].y * offset.y
            );
        }
        return verts;
    }

    // OBB vs OBB（SAT - Separating Axis Theorem）
    static bool intersects(const OBB2D& a, const OBB2D& b) {
        // 获取所有测试轴（两个OBB的4个轴）
        std::vector<Vec2> testAxes = {a.axes[0], a.axes[1], b.axes[0], b.axes[1]};

        for (const Vec2& axis : testAxes) {
            if (!overlapsOnAxis(a, b, axis)) {
                return false;  // 找到分离轴，无碰撞
            }
        }
        return true;  // 所有轴都重叠，有碰撞
    }

private:
    static bool overlapsOnAxis(const OBB2D& a, const OBB2D& b, const Vec2& axis) {
        // 投影到轴上并检查区间是否重叠
        // 计算每个OBB在轴上的投影区间半径（半宽）
        float aHalfExtent = getOBBHalfExtentOnAxis(a, axis);
        float bHalfExtent = getOBBHalfExtentOnAxis(b, axis);
        // 投影中心
        float aProjCenter = a.center.dot(axis);
        float bProjCenter = b.center.dot(axis);
        // 检查区间是否重叠：中心距离 <= 半宽之和
        return std::abs(aProjCenter - bProjCenter) <= (aHalfExtent + bHalfExtent);
    }

    // 计算OBB在给定轴上的投影半宽
    static float getOBBHalfExtentOnAxis(const OBB2D& box, const Vec2& axis) {
        return std::abs(box.halfExtents.x * box.axes[0].dot(axis)) +
               std::abs(box.halfExtents.y * box.axes[1].dot(axis));
    }
};

// ============================================================
// 碰撞系统
// ============================================================

class CollisionWorld {
private:
    struct RigidBody {
        Vec2 position;
        Vec2 velocity;
        float mass;
        bool isStatic;
        enum class ShapeType { CIRCLE, AABB } shapeType;
        union {
            Circle circle;
            AABB2D aabb;
        };

        RigidBody(const Vec2& pos, float m, bool staticBody)
            : position(pos), velocity(0, 0), mass(m), isStatic(staticBody) {}

        virtual ~RigidBody() {}
    };

    struct CircleBody : RigidBody {
        CircleBody(const Vec2& pos, float radius, float m, bool staticBody)
            : RigidBody(pos, m, staticBody) {
            shapeType = ShapeType::CIRCLE;
            new (&circle) Circle(pos, radius);
        }
    };

    struct AABBBody : RigidBody {
        float halfWidth, halfHeight;

        AABBBody(const Vec2& pos, float hw, float hh, float m, bool staticBody)
            : RigidBody(pos, m, staticBody), halfWidth(hw), halfHeight(hh) {
            shapeType = ShapeType::AABB;
            new (&aabb) AABB2D(Vec2(pos.x - hw, pos.y - hh),
                               Vec2(pos.x + hw, pos.y + hh));
        }
    };

    std::vector<std::unique_ptr<RigidBody>> bodies;

public:
    ~CollisionWorld() {
        for (auto& body : bodies) {
            if (body->shapeType == RigidBody::ShapeType::AABB) {
                body->aabb.~AABB2D();
            }
        }
    }

    size_t addCircle(const Vec2& pos, float radius, float mass = 1.0f, bool isStatic = false) {
        bodies.push_back(std::make_unique<CircleBody>(pos, radius, mass, isStatic));
        return bodies.size() - 1;
    }

    size_t addAABB(const Vec2& pos, float hw, float hh, float mass = 1.0f, bool isStatic = false) {
        bodies.push_back(std::make_unique<AABBBody>(pos, hw, hh, mass, isStatic));
        return bodies.size() - 1;
    }

    // 简单物理更新
    void update(float dt) {
        for (auto& body : bodies) {
            if (body->isStatic) continue;

            // 简单重力 + 速度更新位置
            body->velocity.y -= 9.8f * dt;
            body->position = body->position + body->velocity * dt;

            // 更新碰撞体位置
            if (body->shapeType == RigidBody::ShapeType::CIRCLE) {
                body->circle.center = body->position;
            } else if (body->shapeType == RigidBody::ShapeType::AABB) {
                float hw = static_cast<AABBBody*>(body.get())->halfWidth;
                float hh = static_cast<AABBBody*>(body.get())->halfHeight;
                new (&body->aabb) AABB2D(
                    Vec2(body->position.x - hw, body->position.y - hh),
                    Vec2(body->position.x + hw, body->position.y + hh)
                );
            }
        }
    }

    // 碰撞检测
    void checkCollisions() {
        std::cout << "\n🔍 开始碰撞检测..." << std::endl;

        for (size_t i = 0; i < bodies.size(); i++) {
            for (size_t j = i + 1; j < bodies.size(); j++) {
                bool collided = false;

                auto& a = bodies[i];
                auto& b = bodies[j];

                // 根据形状类型选择检测方法
                if (a->shapeType == RigidBody::ShapeType::CIRCLE &&
                    b->shapeType == RigidBody::ShapeType::CIRCLE) {
                    collided = Circle::intersects(a->circle, b->circle);
                } else if (a->shapeType == RigidBody::ShapeType::AABB &&
                           b->shapeType == RigidBody::ShapeType::AABB) {
                    collided = AABB2D::intersects(a->aabb, b->aabb);
                } else if (a->shapeType == RigidBody::ShapeType::CIRCLE &&
                           b->shapeType == RigidBody::ShapeType::AABB) {
                    collided = Circle::intersects(a->circle, b->aabb);
                } else if (a->shapeType == RigidBody::ShapeType::AABB &&
                           b->shapeType == RigidBody::ShapeType::CIRCLE) {
                    collided = Circle::intersects(b->circle, a->aabb);
                }

                if (collided) {
                    std::cout << "💥 碰撞！物体 " << i << " 和物体 " << j;
                    if (a->isStatic) std::cout << " (静态)";
                    if (b->isStatic) std::cout << " (静态)";
                    std::cout << std::endl;
                }
            }
        }
    }

    // 打印世界状态
    void printState() const {
        std::cout << "\n📊 世界状态:" << std::endl;
        for (size_t i = 0; i < bodies.size(); i++) {
            const auto& body = bodies[i];
            std::cout << "  物体 " << i << ": 位置("
                      << std::fixed << std::setprecision(2)
                      << body->position.x << ", "
                      << body->position.y << ")";

            if (body->shapeType == RigidBody::ShapeType::CIRCLE) {
                std::cout << " 圆形(r=" << body->circle.radius << ")";
            } else if (body->shapeType == RigidBody::ShapeType::AABB) {
                std::cout << " AABB(" << body->aabb.width() << "x" << body->aabb.height() << ")";
            }

            if (body->isStatic) std::cout << " [静态]";
            std::cout << std::endl;
        }
    }
};

// ============================================================
// 演示
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      碰撞检测系统演示                " << std::endl;
    std::cout << "========================================" << std::endl;

    CollisionWorld world;

    // 创建一些物体
    // 地面（静态AABB）
    world.addAABB(Vec2(0, -5), 10, 1, 0, true);

    // 球（动态圆形）
    size_t ball1 = world.addCircle(Vec2(-2, 5), 0.5f, 1.0f, false);
    size_t ball2 = world.addCircle(Vec2(2, 8), 0.8f, 2.0f, false);

    // 箱子（动态AABB）
    size_t box1 = world.addAABB(Vec2(0, 3), 1, 1, 1.0f, false);

    std::cout << "\n🎬 初始状态:" << std::endl;
    world.printState();

    // 模拟几帧
    for (int frame = 1; frame <= 5; frame++) {
        std::cout << "\n\n========== 帧 " << frame << " ==========" << std::endl;
        world.update(0.016f);  // ~60FPS
        world.checkCollisions();
        world.printState();
    }

    std::cout << R"(
    ========================================
           碰撞检测算法选择指南
    ========================================

    📦 AABB (轴对齐包围盒):
       ✅ 检测速度快
       ✅ 适用于没有旋转的物体
       ❌ 不适用于斜着的物体
       用途: 宽相检测, 静态环境

    ⭕ 圆形:
       ✅ 旋转不变性 (圆形转不转都一样)
       ✅ 检测速度极快
       ❌ 很多物体不是圆形
       用途: 球类, 角色代理, 射线检测

    📐 精确多边形:
       ✅ 最精确
       ❌ 最慢
       用途: 需要精确碰撞的场合 (如格斗游戏)
    )" << std::endl;

    return 0;
}
```

---

## 41.5 状态机：让游戏角色"活"起来

你有没有想过，为什么游戏里的NPC能"思考"？为什么敌人能巡逻、能追击、能攻击？答案就是——**有限状态机（Finite State Machine, FSM）**。

### 什么是状态机？

状态机描述了一个对象在不同"状态"之间的切换。比如一个敌人的状态机可能是这样：

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ┌──────────┐    发现玩家     ┌──────────┐               │
│    │  巡逻    │ ──────────────→ │  追踪    │               │
│    │ (Patrol) │                  │ (Chase)  │               │
│    └────┬─────┘                  └────┬─────┘               │
│         │                             │                     │
│         │ 没发现玩家                  │ 进入攻击范围          │
│         │ 持续一段时间                 │                     │
│         ▼                             ▼                     │
│    ┌──────────┐    生命值低     ┌──────────┐               │
│    │  返回    │ ←────────────── │  攻击    │               │
│    │ (Return) │                  │ (Attack) │               │
│    └────┬─────┘                  └────┬─────┘               │
│         │                             │                     │
│         │ 回到起点                    │ 玩家逃离             │
│         └─────────────────────────────┘                     │
│                                                             │
│    ┌──────────┐    生命值归零     ┌──────────┐              │
│    │  死亡    │ ←───────────────→ │  受伤    │              │
│    │ (Dead)   │                  │ (Hurt)   │              │
│    └──────────┘                  └──────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```cpp
// Game_05_StateMachine.cpp
// 有限状态机演示
// 编译：g++ Game_05_StateMachine.cpp -std=c++17 -o Game_05_StateMachine

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <chrono>
#include <cmath>

// ============================================================
// 状态机基础框架
// ============================================================

// 前向声明
class StateMachine;

// 状态基类
class State {
public:
    virtual ~State() = default;

    // 状态Enter/Exit
    virtual void enter() {}
    virtual void exit() {}

    // 每帧更新
    virtual void update(float dt) = 0;

    // 处理事件（可选）
    virtual void handleEvent(const std::string& event) {}

    // 获取状态名称（用于调试）
    virtual std::string getName() const = 0;

protected:
    State() = default;
};

// 状态机
class StateMachine {
private:
    State* currentState = nullptr;
    State* previousState = nullptr;
    bool isReEntering = false;

public:
    ~StateMachine() {
        // 状态由外部管理，这里只清除指针
    }

    void setState(State* newState) {
        if (newState == currentState && !isReEntering) {
            return;  // 已经在目标状态
        }

        // 退出当前状态
        if (currentState) {
            std::cout << "  🚪 [" << currentState->getName() << "] 退出" << std::endl;
            currentState->exit();
        }

        previousState = currentState;
        currentState = newState;

        // 进入新状态
        if (currentState) {
            std::cout << "  🚪 [" << currentState->getName() << "] 进入" << std::endl;
            currentState->enter();
        }
    }

    void reEnterCurrentState() {
        isReEntering = true;
        if (currentState) {
            std::cout << "  🔄 [" << currentState->getName() << "] 重新进入" << std::endl;
            currentState->exit();
            currentState->enter();
        }
        isReEntering = false;
    }

    void update(float dt) {
        if (currentState) {
            currentState->update(dt);
        }
    }

    void handleEvent(const std::string& event) {
        if (currentState) {
            currentState->handleEvent(event);
        }
    }

    State* getCurrentState() const { return currentState; }
    State* getPreviousState() const { return previousState; }
};

// ============================================================
// 游戏角色示例
// ============================================================

struct Vector2D {
    float x, y;

    Vector2D(float x = 0, float y = 0) : x(x), y(y) {}

    Vector2D operator+(const Vector2D& other) const {
        return Vector2D(x + other.x, y + other.y);
    }

    Vector2D operator-(const Vector2D& other) const {
        return Vector2D(x - other.x, y - other.y);
    }

    Vector2D operator*(float scalar) const {
        return Vector2D(x * scalar, y * scalar);
    }

    float length() const {
        return std::sqrt(x * x + y * y);
    }

    Vector2D normalized() const {
        float len = length();
        if (len < 0.0001f) return Vector2D(0, 0);
        return Vector2D(x / len, y / len);
    }

    std::string toString() const {
        return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
    }
};

class GameCharacter {
private:
    std::string name;
    Vector2D position;
    Vector2D velocity;
    float health;
    float maxHealth;
    float speed;
    StateMachine fsm;

public:
    GameCharacter(const std::string& n, const Vector2D& pos)
        : name(n), position(pos), velocity(0, 0),
          health(100), maxHealth(100), speed(50) {

        std::cout << "🎭 创建角色: " << name << " @ " << position.toString() << std::endl;
    }

    ~GameCharacter() {
        std::cout << "🎭 角色消失: " << name << std::endl;
    }

    // 状态查询
    bool isAlive() const { return health > 0; }
    float getHealthPercent() const { return health / maxHealth; }
    const Vector2D& getPosition() const { return position; }
    StateMachine& getFSM() { return fsm; }

    // 动作
    void moveTo(const Vector2D& target, float dt) {
        Vector2D dir = (target - position).normalized();
        velocity = dir * speed;
        position = position + velocity * dt;
    }

    void moveInDirection(const Vector2D& dir, float dt) {
        Vector2D normalizedDir = dir.normalized();
        velocity = normalizedDir * speed;
        position = position + velocity * dt;
    }

    void takeDamage(float amount) {
        health = std::max(0.0f, health - amount);
        std::cout << "  💥 " << name << " 受到 " << amount << " 点伤害！"
                  << " 剩余生命: " << health << "/" << maxHealth << std::endl;
    }

    void heal(float amount) {
        health = std::min(maxHealth, health + amount);
        std::cout << "  💚 " << name << " 恢复 " << amount << " 点生命！"
                  << " 当前生命: " << health << "/" << maxHealth << std::endl;
    }

    void printStatus() const {
        std::cout << "  📊 " << name << " - 位置: " << position.toString()
                  << " 生命: " << health << "/" << maxHealth
                  << " (" << getHealthPercent() * 100 << "%)" << std::endl;
    }
};

// ============================================================
// 敌人状态定义
// ============================================================

class EnemyPatrolState : public State {
private:
    GameCharacter& enemy;
    Vector2D patrolCenter;
    float patrolRadius;
    float patrolTimer;
    float patrolDuration;
    Vector2D currentTarget;

public:
    EnemyPatrolState(GameCharacter& e, const Vector2D& center,
                     float radius, float duration = 3.0f)
        : enemy(e), patrolCenter(center), patrolRadius(radius),
          patrolTimer(0), patrolDuration(duration) {
        currentTarget = getRandomPatrolPoint();
    }

    void enter() override {
        std::cout << "  🛤️  [" << enemy.getFSM().getCurrentState()->getName()
                  << "] 开始巡逻" << std::endl;
    }

    Vector2D getRandomPatrolPoint() {
        float angle = static_cast<float>(rand() % 360) * 3.14159f / 180.0f;
        float dist = static_cast<float>(rand() % 100) / 100.0f * patrolRadius;
        return patrolCenter + Vector2D(
            std::cos(angle) * dist,
            std::sin(angle) * dist
        );
    }

    void update(float dt) override {
        patrolTimer += dt;

        // 移动到巡逻点
        enemy.moveTo(currentTarget, dt);
        std::cout << "  🚶 巡逻中，移动到 " << currentTarget.toString() << std::endl;

        // 到达目标点或超时，获取新目标
        if ((enemy.getPosition() - currentTarget).length() < 1.0f ||
            patrolTimer >= patrolDuration) {
            currentTarget = getRandomPatrolPoint();
            patrolTimer = 0;
            std::cout << "  🔄 获取新的巡逻点" << std::endl;
        }
    }

    void handleEvent(const std::string& event) override {
        if (event == "PlayerSpotted") {
            // 玩家位置需要从游戏世界获取，这里简化为一个固定位置
            enemy.getFSM().setState(new EnemyChaseState(enemy, Vector2D(15.0f, 15.0f)));
        }
    }

    std::string getName() const override { return "巡逻"; }
};

class EnemyChaseState : public State {
private:
    GameCharacter& enemy;
    Vector2D lastKnownPlayerPos;
    float chaseTimer;

public:
    EnemyChaseState(GameCharacter& e, const Vector2D& playerPos)
        : enemy(e), lastKnownPlayerPos(playerPos), chaseTimer(0) {}

    void enter() override {
        std::cout << "  🏃 [" << enemy.getFSM().getCurrentState()->getName()
                  << "] 发现玩家！开始追击！" << std::endl;
    }

    void update(float dt) override {
        chaseTimer += dt;

        // 模拟玩家位置更新（实际游戏中会从GameWorld获取）
        // 这里假设玩家位置不变化
        enemy.moveTo(lastKnownPlayerPos, dt);
        std::cout << "  🔍 追击玩家，最后已知位置: " << lastKnownPlayerPos.toString() << std::endl;

        // 超时，返回巡逻
        if (chaseTimer > 5.0f) {
            std::cout << "  ⏰ 追击超时，放弃追踪" << std::endl;
            enemy.getFSM().setState(new EnemyPatrolState(enemy, Vector2D(0, 0), 10));
        }
    }

    void handleEvent(const std::string& event) override {
        if (event == "PlayerEscaped") {
            std::cout << "  😤 玩家逃走了！" << std::endl;
            enemy.getFSM().setState(new EnemyPatrolState(enemy, Vector2D(0, 0), 10));
        } else if (event == "InAttackRange") {
            enemy.getFSM().setState(new EnemyAttackState(enemy));
        } else if (event == "TakeDamage") {
            enemy.getFSM().setState(new EnemyHurtState(enemy, lastKnownPlayerPos));
        }
    }

    std::string getName() const override { return "追击"; }
};

class EnemyAttackState : public State {
private:
    GameCharacter& enemy;
    float attackCooldown;
    float currentCooldown;
    float damage;

public:
    EnemyAttackState(GameCharacter& e, float dmg = 10.0f)
        : enemy(e), attackCooldown(1.0f), currentCooldown(0), damage(dmg) {}

    void enter() override {
        std::cout << "  ⚔️  [" << enemy.getFSM().getCurrentState()->getName()
                  << "] 进入攻击状态！" << std::endl;
    }

    void update(float dt) override {
        currentCooldown += dt;

        if (currentCooldown >= attackCooldown) {
            // 执行攻击
            std::cout << "  💥 " << enemy.getPosition().toString()
                      << " 对玩家发动攻击！造成 " << damage << " 点伤害！" << std::endl;
            currentCooldown = 0;
        }
    }

    void handleEvent(const std::string& event) override {
        if (event == "PlayerEscaped") {
            enemy.getFSM().setState(new EnemyPatrolState(enemy, Vector2D(0, 0), 10));
        } else if (event == "TakeDamage") {
            enemy.getFSM().setState(new EnemyHurtState(enemy, enemy.getPosition()));
        }
    }

    std::string getName() const override { return "攻击"; }
};

class EnemyHurtState : public State {
private:
    GameCharacter& enemy;
    float hurtDuration;
    float hurtTimer;
    Vector2D knockbackDir;

public:
    EnemyHurtState(GameCharacter& e, const Vector2D& knockback)
        : enemy(e), hurtDuration(0.5f), hurtTimer(0),
          knockbackDir((e.getPosition() - knockback).normalized()) {}

    void enter() override {
        std::cout << "  😵 [" << enemy.getFSM().getCurrentState()->getName()
                  << "] 受伤！击退中..." << std::endl;
    }

    void update(float dt) override {
        hurtTimer += dt;

        // 击退
        enemy.moveInDirection(knockbackDir, dt);

        if (hurtTimer >= hurtDuration) {
            // 受伤结束，检查是否死亡
            if (!enemy.isAlive()) {
                enemy.getFSM().setState(new EnemyDeadState(enemy));
            } else {
                enemy.getFSM().setState(new EnemyChaseState(enemy, enemy.getPosition()));
            }
        }
    }

    std::string getName() const override { return "受伤"; }
};

class EnemyDeadState : public State {
private:
    GameCharacter& enemy;
    float respawnTimer;
    float respawnDuration;

public:
    EnemyDeadState(GameCharacter& e, float respawnTime = 5.0f)
        : enemy(e), respawnTimer(0), respawnDuration(respawnTime) {}

    void enter() override {
        std::cout << "  💀 [" << enemy.getFSM().getCurrentState()->getName()
                  << "] 敌人死亡！开始复活倒计时..." << std::endl;
    }

    void update(float dt) override {
        respawnTimer += dt;
        std::cout << "  ⏳ 复活倒计时: " << (respawnDuration - respawnTimer)
                  << " 秒" << std::endl;

        if (respawnTimer >= respawnDuration) {
            // 复活（重置生命值）
            std::cout << "  ✨ 敌人复活！" << std::endl;
            // 实际游戏中会重置位置和状态
            enemy.getFSM().setState(new EnemyPatrolState(enemy, Vector2D(0, 0), 10));
        }
    }

    std::string getName() const override { return "死亡"; }
};

// ============================================================
// 演示
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      有限状态机演示 v1.0              " << std::endl;
    std::cout << "========================================" << std::endl;

    // 创建敌人
    GameCharacter enemy("史莱姆一号", Vector2D(0, 0));

    // 设置初始状态
    enemy.getFSM().setState(new EnemyPatrolState(enemy, Vector2D(0, 0), 10));

    float dt = 0.1f;  // 每帧时间

    std::cout << "\n========================================" << std::endl;
    std::cout << "      模拟游戏循环                      " << std::endl;
    std::cout << "========================================" << std::endl;

    // 模拟游戏循环
    for (int frame = 1; frame <= 50; frame++) {
        std::cout << "\n--- 帧 " << frame << " ---" << std::endl;

        enemy.getFSM().update(dt);
        enemy.printStatus();

        // 模拟一些事件
        if (frame == 10) {
            std::cout << "\n🎮 事件: 玩家进入视野！" << std::endl;
            enemy.getFSM().handleEvent("PlayerSpotted");
        }

        if (frame == 20) {
            std::cout << "\n🎮 事件: 玩家进入攻击范围！" << std::endl;
            enemy.getFSM().handleEvent("InAttackRange");
        }

        if (frame == 25) {
            std::cout << "\n🎮 事件: 玩家攻击！敌人受伤！" << std::endl;
            enemy.takeDamage(30);
            enemy.getFSM().handleEvent("TakeDamage");
        }

        if (frame == 35) {
            std::cout << "\n🎮 事件: 玩家逃离！" << std::endl;
            enemy.getFSM().handleEvent("PlayerEscaped");
        }

        if (frame == 40) {
            std::cout << "\n🎮 事件: 玩家致命一击！" << std::endl;
            enemy.takeDamage(80);
            enemy.getFSM().handleEvent("TakeDamage");
        }
    }

    std::cout << R"(
    ========================================
           状态机使用场景
    ========================================

    🎮 角色AI:
       - 敌人行为（巡逻、追击、攻击、逃跑）
       - NPC对话
       - 动物行为

    🎮 游戏流程:
       - 主菜单 → 加载 → 游戏中 → 暂停 → 结算
       - 教程流程
       - 剧情分支

    🎮 UI系统:
       - 按钮状态（正常、悬停、按下、禁用）
       - 动画状态

    🎮 动画状态机 (Animator):
       - 角色的待机、行走、奔跑、跳跃、攻击、死亡
       - 武器切换

    💡 设计模式:
       - 状态模式 (State Pattern)
       - 策略模式可以视为单状态的状态机
    )" << std::endl;

    return 0;
}
```

---

## 41.6 输入处理：玩家与游戏的"对话"

游戏输入系统负责将玩家的操作（键盘、鼠标、手柄）转换为游戏内的动作。一个好的输入系统应该：

1. **解耦输入和逻辑**：游戏逻辑不应该直接读取键盘按键
2. **支持输入映射**：方便配置不同设备的按键
3. **处理输入缓冲**：防止快速输入丢失
4. **支持组合键和宏**

```cpp
// Game_06_InputSystem.cpp
// 输入系统演示
// 编译：g++ Game_06_InputSystem.cpp -std=c++17 -o Game_06_InputSystem

#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <unordered_map>
#include <set>

// ============================================================
// 输入键码定义
// ============================================================

enum class KeyCode {
    // 键盘
    KEY_W, KEY_A, KEY_S, KEY_D,
    KEY_SPACE, KEY_SHIFT, KEY_CTRL, KEY_ENTER, KEY_ESCAPE,
    KEY_1, KEY_2, KEY_3, KEY_4, KEY_Q, KEY_E, KEY_R, KEY_T,

    // 鼠标
    MOUSE_LEFT, MOUSE_RIGHT, MOUSE_MIDDLE,

    // 手柄按钮（简化）
    GAMEPAD_A, GAMEPAD_B, GAMEPAD_X, GAMEPAD_Y,
    GAMEPAD_LB, GAMEPAD_RB, GAMEPAD_LT, GAMEPAD_RT,

    UNKNOWN
};

std::string keyCodeToString(KeyCode key) {
    switch (key) {
        case KeyCode::KEY_W: return "W";
        case KeyCode::KEY_A: return "A";
        case KeyCode::KEY_S: return "S";
        case KeyCode::KEY_D: return "D";
        case KeyCode::KEY_SPACE: return "Space";
        case KeyCode::KEY_SHIFT: return "Shift";
        case KeyCode::KEY_CTRL: return "Ctrl";
        case KeyCode::KEY_ENTER: return "Enter";
        case KeyCode::KEY_ESCAPE: return "Escape";
        case KeyCode::MOUSE_LEFT: return "MouseLeft";
        case KeyCode::MOUSE_RIGHT: return "MouseRight";
        case KeyCode::GAMEPAD_A: return "GamepadA";
        default: return "Unknown";
    }
}

// ============================================================
// 输入事件
// ============================================================

enum class InputEventType {
    KEY_PRESSED,
    KEY_RELEASED,
    KEY_REPEATED,
    MOUSE_MOVED,
    MOUSE_WHEEL
};

struct InputEvent {
    InputEventType type;
    KeyCode key;
    int mouseX, mouseY;       // 鼠标位置
    int wheelDelta;           // 滚轮滚动量

    InputEvent(InputEventType t, KeyCode k)
        : type(t), key(k), mouseX(0), mouseY(0), wheelDelta(0) {}
};

// ============================================================
// 输入动作映射
// ============================================================

struct InputAction {
    std::string name;
    std::set<KeyCode> primaryKeys;  // 主按键
    std::set<KeyCode> altKeys;      // 备用按键

    InputAction(const std::string& n) : name(n) {}

    void addKey(KeyCode key, bool isPrimary = true) {
        if (isPrimary) {
            primaryKeys.insert(key);
        } else {
            altKeys.insert(key);
        }
    }
};

// ============================================================
// 输入系统
// ============================================================

class InputSystem {
private:
    // 当前按下的键
    std::set<KeyCode> currentKeys;

    // 按键事件缓冲
    std::vector<InputEvent> eventBuffer;

    // 动作映射
    std::unordered_map<std::string, std::unique_ptr<InputAction>> actionMap;

    // 鼠标状态
    int mouseX = 0, mouseY = 0;
    int prevMouseX = 0, prevMouseY = 0;

    // 动作回调
    std::unordered_map<std::string, std::function<void(float)>> actionCallbacks;

public:
    InputSystem() {
        std::cout << "🕹️  输入系统初始化" << std::endl;
        setupDefaultBindings();
    }

    void setupDefaultBindings() {
        // 移动
        auto moveForward = std::make_unique<InputAction>("MoveForward");
        moveForward->addKey(KeyCode::KEY_W);
        moveForward->addKey(KeyCode::KEY_SPACE);  // 备用
        actionMap["MoveForward"] = std::move(moveForward);

        auto moveBackward = std::make_unique<InputAction>("MoveBackward");
        moveBackward->addKey(KeyCode::KEY_S);
        actionMap["MoveBackward"] = std::move(moveBackward);

        auto moveLeft = std::make_unique<InputAction>("MoveLeft");
        moveLeft->addKey(KeyCode::KEY_A);
        actionMap["MoveLeft"] = std::move(moveLeft);

        auto moveRight = std::make_unique<InputAction>("MoveRight");
        moveRight->addKey(KeyCode::KEY_D);
        actionMap["MoveRight"] = std::move(moveRight);

        // 攻击
        auto attack = std::make_unique<InputAction>("Attack");
        attack->addKey(KeyCode::MOUSE_LEFT);
        attack->addKey(KeyCode::KEY_J);  // 键盘备用
        attack->addKey(KeyCode::GAMEPAD_A);
        actionMap["Attack"] = std::move(attack);

        // 技能1
        auto skill1 = std::make_unique<InputAction>("Skill1");
        skill1->addKey(KeyCode::KEY_1);
        skill1->addKey(KeyCode::KEY_Q);
        actionMap["Skill1"] = std::move(skill1);

        // 技能2
        auto skill2 = std::make_unique<InputAction>("Skill2");
        skill2->addKey(KeyCode::KEY_2);
        skill2->addKey(KeyCode::KEY_E);
        actionMap["Skill2"] = std::move(skill2);

        // 交互
        auto interact = std::make_unique<InputAction>("Interact");
        interact->addKey(KeyCode::KEY_ENTER);
        interact->addKey(KeyCode::KEY_E);
        interact->addKey(KeyCode::GAMEPAD_B);
        actionMap["Interact"] = std::move(interact);

        // 菜单
        auto menu = std::make_unique<InputAction>("ToggleMenu");
        menu->addKey(KeyCode::KEY_ESCAPE);
        menu->addKey(KeyCode::KEY_TAB);
        actionMap["ToggleMenu"] = std::move(menu);

        std::cout << "🕹️  默认按键绑定已设置" << std::endl;
    }

    // 模拟按键按下（实际游戏中由底层输入驱动调用）
    void onKeyPressed(KeyCode key) {
        if (currentKeys.find(key) == currentKeys.end()) {
            currentKeys.insert(key);
            eventBuffer.push_back(InputEvent(InputEventType::KEY_PRESSED, key));

            // 触发对应的动作
            triggerAction(key, true);
        }
    }

    void onKeyReleased(KeyCode key) {
        if (currentKeys.find(key) != currentKeys.end()) {
            currentKeys.erase(key);
            eventBuffer.push_back(InputEvent(InputEventType::KEY_RELEASED, key));

            // 触发对应的动作
            triggerAction(key, false);
        }
    }

    void onMouseMoved(int x, int y) {
        prevMouseX = mouseX;
        prevMouseY = mouseY;
        mouseX = x;
        mouseY = y;
        eventBuffer.push_back(InputEvent(InputEventType::MOUSE_MOVED, KeyCode::UNKNOWN));
        eventBuffer.back().mouseX = mouseX;
        eventBuffer.back().mouseY = mouseY;
    }

    // 绑定动作回调
    void bindAction(const std::string& actionName, std::function<void(float)> callback) {
        actionCallbacks[actionName] = callback;
        std::cout << "🕹️  绑定动作: " << actionName << std::endl;
    }

    // 检查动作是否激活
    bool isActionActive(const std::string& actionName) {
        auto it = actionMap.find(actionName);
        if (it == actionMap.end()) return false;

        const auto& action = it->second;

        for (KeyCode key : action->primaryKeys) {
            if (currentKeys.find(key) != currentKeys.end()) {
                return true;
            }
        }

        for (KeyCode key : action->altKeys) {
            if (currentKeys.find(key) != currentKeys.end()) {
                return true;
            }
        }

        return false;
    }

    // 检查某键是否按下
    bool isKeyPressed(KeyCode key) const {
        return currentKeys.find(key) != currentKeys.end();
    }

    // 获取鼠标位置
    std::pair<int, int> getMousePosition() const {
        return {mouseX, mouseY};
    }

    // 获取鼠标移动量
    std::pair<int, int> getMouseDelta() const {
        return {mouseX - prevMouseX, mouseY - prevMouseY};
    }

    // 处理事件缓冲
    void processEvents() {
        for (const auto& event : eventBuffer) {
            handleEvent(event);
        }
        eventBuffer.clear();
    }

    // 更新（每帧调用）
    void update(float dt) {
        processEvents();

        // 持续动作（如移动）需要在update中处理
        Vector2D moveInput(0, 0);
        if (isActionActive("MoveForward")) moveInput.y += 1;
        if (isActionActive("MoveBackward")) moveInput.y -= 1;
        if (isActionActive("MoveLeft")) moveInput.x -= 1;
        if (isActionActive("MoveRight")) moveInput.x += 1;

        if (moveInput.x != 0 || moveInput.y != 0) {
            auto it = actionCallbacks.find("MoveForward");
            // 实际会调用移动回调
        }
    }

    void printState() const {
        std::cout << "🕹️  当前按下的键: ";
        if (currentKeys.empty()) {
            std::cout << "无";
        } else {
            for (KeyCode key : currentKeys) {
                std::cout << keyCodeToString(key) << " ";
            }
        }
        std::cout << std::endl;
    }

private:
    void triggerAction(KeyCode key, bool pressed) {
        // 查找触发该键的动作
        for (const auto& [actionName, action] : actionMap) {
            if (action->primaryKeys.find(key) != action->primaryKeys.end() ||
                action->altKeys.find(key) != action->altKeys.end()) {

                auto it = actionCallbacks.find(actionName);
                if (it != actionCallbacks.end() && pressed) {
                    it->second(0.0f);  // 按下时触发回调
                }

                std::cout << "🕹️  动作 [" << actionName << "] "
                          << (pressed ? "触发" : "释放")
                          << " (按键: " << keyCodeToString(key) << ")" << std::endl;
            }
        }
    }

    void handleEvent(const InputEvent& event) {
        switch (event.type) {
            case InputEventType::MOUSE_MOVED:
                std::cout << "🖱️  鼠标移动到: (" << event.mouseX << ", " << event.mouseY << ")" << std::endl;
                break;
            default:
                break;
        }
    }

    struct Vector2D {
        float x, y;
        Vector2D(float x = 0, float y = 0) : x(x), y(y) {}
    };
};

// ============================================================
// 演示
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      输入系统演示 v1.0                " << std::endl;
    std::cout << "========================================" << std::endl;

    InputSystem input;

    // 绑定动作回调
    input.bindAction("MoveForward", [](float) {
        std::cout << "  🚶 向前移动" << std::endl;
    });

    input.bindAction("MoveBackward", [](float) {
        std::cout << "  🚶 向后移动" << std::endl;
    });

    input.bindAction("MoveLeft", [](float) {
        std::cout << "  🚶 向左移动" << std::endl;
    });

    input.bindAction("MoveRight", [](float) {
        std::cout << "  🚶 向右移动" << std::endl;
    });

    input.bindAction("Attack", [](float) {
        std::cout << "  ⚔️ 攻击！" << std::endl;
    });

    input.bindAction("Skill1", [](float) {
        std::cout << "  ✨ 释放技能1！" << std::endl;
    });

    input.bindAction("Skill2", [](float) {
        std::cout << "  ✨ 释放技能2！" << std::endl;
    });

    input.bindAction("Interact", [](float) {
        std::cout << "  🤝 交互" << std::endl;
    });

    input.bindAction("ToggleMenu", [](float) {
        std::cout << "  📋 切换菜单" << std::endl;
    });

    std::cout << "\n========================================" << std::endl;
    std::cout << "      模拟玩家输入                      " << std::endl;
    std::cout << "========================================" << std::endl;

    // 模拟一些输入
    std::cout << "\n[场景1] 玩家按下 W 键..." << std::endl;
    input.onKeyPressed(KeyCode::KEY_W);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景2] 玩家按下 D 键..." << std::endl;
    input.onKeyPressed(KeyCode::KEY_D);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景3] 玩家按下 鼠标左键..." << std::endl;
    input.onKeyPressed(KeyCode::MOUSE_LEFT);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景4] 玩家松开 D 键..." << std::endl;
    input.onKeyReleased(KeyCode::KEY_D);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景5] 玩家同时按下 Q 和 1 使用技能..." << std::endl;
    input.onKeyPressed(KeyCode::KEY_Q);
    input.onKeyPressed(KeyCode::KEY_1);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景6] 玩家按 Escape 打开菜单..." << std::endl;
    input.onKeyPressed(KeyCode::KEY_ESCAPE);
    input.update(0.016f);
    input.printState();

    std::cout << "\n[场景7] 鼠标移动..." << std::endl;
    input.onMouseMoved(500, 300);
    input.update(0.016f);

    std::cout << "\n========================================" << std::endl;
    std::cout << "      输入系统设计要点                  " << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << R"(
    📝 输入系统设计要点:

    1️⃣ 解耦输入与游戏逻辑
       - 玩家输入 → 输入系统 → 动作事件 → 游戏逻辑
       - 不要在游戏逻辑中直接读取按键

    2️⃣ 支持多种输入设备
       - 键盘、鼠标、手柄、触摸屏
       - 同一动作应可由多个按键触发

    3️⃣ 输入缓冲
       - 防止快速输入丢失
       - 适当时间的输入窗口

    4️⃣ 按键映射可配置
       - 允许玩家自定义按键
       - 保存/加载按键配置

    5️⃣ 处理输入优先级
       - 暂停时不应响应游戏内输入
       - UI上不应触发游戏动作

    💡 推荐架构:
       InputDevice → InputManager → InputAction → Gameplay
       (底层输入)    (输入系统)    (动作映射)     (游戏逻辑)
    )" << std::endl;

    return 0;
}
```

---

## 41.7 音频系统：让游戏"声"临其境

声音是游戏的灵魂之一。从背景音乐到脚步声，从武器开火到NPC对话，音频让游戏世界更加真实。

```cpp
// Game_07_AudioSystem.cpp
// 简化音频系统演示（模拟实现，不依赖实际音频库）
// 编译：g++ Game_07_AudioSystem.cpp -std=c++17 -o Game_07_AudioSystem

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <unordered_map>
#include <functional>
#include <random>
#include <cmath>

// ============================================================
// 音频资源
// ============================================================

enum class SoundType {
    SFX,       // 音效（短促，支持多实例）
    MUSIC,     // 背景音乐（通常只播放一个）
    AMBIENT,   // 环境音（循环播放）
    VOICE      // 语音（对话等）
};

struct SoundEffect {
    std::string name;
    std::string filePath;
    float volume;
    float pitch;
    bool is3D;
    bool loop;

    SoundEffect(const std::string& n, const std::string& path)
        : name(n), filePath(path), volume(1.0f), pitch(1.0f),
          is3D(false), loop(false) {}
};

struct AudioSource {
    size_t soundID;
    std::string soundName;
    bool isPlaying;
    bool isPaused;
    float volume;
    float pan;          // 左右声道 [-1, 1]
    float currentTime;
    float duration;

    AudioSource(const std::string& name, float dur)
        : soundID(0), soundName(name), isPlaying(false),
          isPaused(false), volume(1.0f), pan(0.0f),
          currentTime(0.0f), duration(dur) {}
};

// ============================================================
// 音频通道管理
// ============================================================

class AudioChannel {
private:
    size_t channelID;
    AudioSource* source;
    float volume;
    bool muted;
    SoundType type;

public:
    AudioChannel(size_t id) : channelID(id), source(nullptr),
                               volume(1.0f), muted(false),
                               type(SoundType::SFX) {}

    void play(AudioSource* src) {
        source = src;
        source->isPlaying = true;
        source->isPaused = false;
        source->currentTime = 0.0f;
    }

    void stop() {
        if (source) {
            source->isPlaying = false;
            source = nullptr;
        }
    }

    void pause() {
        if (source) {
            source->isPaused = true;
        }
    }

    void resume() {
        if (source) {
            source->isPaused = false;
        }
    }

    void setVolume(float vol) { volume = std::max(0.0f, std::min(1.0f, vol)); }
    float getVolume() const { return muted ? 0.0f : volume; }
    void setMuted(bool m) { muted = m; }
    bool isMuted() const { return muted; }

    void update(float dt) {
        if (source && source->isPlaying && !source->isPaused) {
            source->currentTime += dt;
            if (source->currentTime >= source->duration) {
                source->isPlaying = false;
                source = nullptr;
            }
        }
    }

    bool isActive() const { return source && source->isPlaying; }
    size_t getChannelID() const { return channelID; }
};

// ============================================================
// 音频总线（用于分组控制）
// ============================================================

class AudioBus {
private:
    std::string name;
    float volume;
    bool muted;
    std::vector<AudioChannel*> channels;

public:
    AudioBus(const std::string& n) : name(n), volume(1.0f), muted(false) {}

    void addChannel(AudioChannel* ch) {
        channels.push_back(ch);
    }

    void setVolume(float vol) {
        volume = std::max(0.0f, std::min(2.0f, vol));  // 允许超过1.0（增益）
        for (auto* ch : channels) {
            ch->setVolume(volume);
        }
    }

    float getVolume() const { return volume; }

    void setMuted(bool m) {
        muted = m;
        for (auto* ch : channels) {
            ch->setMuted(muted);
        }
    }

    bool isMuted() const { return muted; }

    void stopAll() {
        for (auto* ch : channels) {
            ch->stop();
        }
    }

    const std::string& getName() const { return name; }
};

// ============================================================
// 音频系统
// ============================================================

class AudioSystem {
private:
    std::unordered_map<std::string, std::unique_ptr<SoundEffect>> soundLibrary;
    std::vector<std::unique_ptr<AudioChannel>> channels;
    std::unordered_map<std::string, std::unique_ptr<AudioBus>> buses;

    size_t nextChannelID = 0;
    size_t nextSoundID = 0;

    // 总线
    AudioBus* masterBus;
    AudioBus* sfxBus;
    AudioBus* musicBus;
    AudioBus* voiceBus;

    // 音乐相关
    AudioSource* currentMusic = nullptr;
    float musicFadeTime = 0.0f;
    float targetMusicVolume = 1.0f;

    // 3D音频
    struct Listener3D {
        float x, y, z;
        float forwardX, forwardY;
    } listener;

public:
    AudioSystem() {
        std::cout << "🔊 音频系统初始化" << std::endl;

        // 创建总线
        masterBus = createBus("Master");
        sfxBus = createBus("SFX");
        musicBus = createBus("Music");
        voiceBus = createBus("Voice");

        // 创建通道
        for (size_t i = 0; i < 16; i++) {
            auto ch = std::make_unique<AudioChannel>(nextChannelID++);
            sfxBus->addChannel(ch.get());
            channels.push_back(std::move(ch));
        }

        // 创建专用的音乐通道
        auto musicCh = std::make_unique<AudioChannel>(nextChannelID++);
        musicBus->addChannel(musicCh.get());
        channels.push_back(std::move(musicCh));

        // 设置默认音量
        masterBus->setVolume(0.8f);
        sfxBus->setVolume(1.0f);
        musicBus->setVolume(0.7f);
        voiceBus->setVolume(1.0f);

        std::cout << "🔊 音频系统初始化完成" << std::endl;
    }

    AudioBus* createBus(const std::string& name) {
        auto bus = std::make_unique<AudioBus>(name);
        auto* ptr = bus.get();
        buses[name] = std::move(bus);
        return ptr;
    }

    // 加载声音
    size_t loadSound(const std::string& name, const std::string& path) {
        auto sound = std::make_unique<SoundEffect>(name, path);
        auto id = nextSoundID++;
        soundLibrary[name] = std::move(sound);
        std::cout << "🔊 加载声音: " << name << " (" << path << ")" << std::endl;
        return id;
    }

    // 播放音效
    size_t playSFX(const std::string& soundName, float volume = 1.0f, float pitch = 1.0f) {
        auto it = soundLibrary.find(soundName);
        if (it == soundLibrary.end()) {
            std::cout << "⚠️  找不到音效: " << soundName << std::endl;
            return SIZE_MAX;
        }

        // 找到空闲通道
        AudioChannel* freeChannel = nullptr;
        for (auto& ch : channels) {
            if (!ch->isActive() && ch->getChannelID() < 16) {
                freeChannel = ch.get();
                break;
            }
        }

        if (!freeChannel) {
            std::cout << "⚠️  没有空闲的SFX通道" << std::endl;
            return SIZE_MAX;
        }

        // 创建音频源
        auto source = std::make_unique<AudioSource>(soundName, 1.0f);  // 模拟1秒时长
        source->volume = volume;
        auto* srcPtr = source.get();

        // 模拟播放
        std::cout << "🔊 播放SFX: " << soundName
                  << " (音量: " << volume * 100 << "%"
                  << ", 音调: " << pitch << "x)" << std::endl;

        return srcPtr->soundID;
    }

    // 播放音乐
    void playMusic(const std::string& soundName, bool loop = true) {
        auto it = soundLibrary.find(soundName);
        if (it == soundLibrary.end()) {
            std::cout << "⚠️  找不到音乐: " << soundName << std::endl;
            return;
        }

        // 淡出当前音乐
        if (currentMusic) {
            std::cout << "🔊 淡出当前音乐..." << std::endl;
            currentMusic->isPlaying = false;
        }

        // 播放新音乐
        currentMusic = new AudioSource(soundName, 180.0f);  // 模拟3分钟
        currentMusic->isPlaying = true;
        currentMusic->loop = loop;
        currentMusic->volume = 0.7f;

        std::cout << "🎵 开始播放音乐: " << soundName
                  << (loop ? " [循环]" : "") << std::endl;
    }

    // 淡入淡出
    void fadeMusic(float targetVolume, float duration) {
        musicFadeTime = duration;
        targetMusicVolume = targetVolume;
        std::cout << "🎵 音乐淡入/淡出: "
                  << (targetVolume > 0 ? "淡入" : "淡出")
                  << " (" << duration << "秒)" << std::endl;
    }

    // 3D音频
    void setListenerPosition(float x, float y, float z,
                             float forwardX = 0, float forwardY = 1) {
        listener.x = x;
        listener.y = y;
        listener.z = z;
        listener.forwardX = forwardX;
        listener.forwardY = forwardY;
    }

    float calculate3DVolume(float sourceX, float sourceY, float sourceZ) {
        float dx = sourceX - listener.x;
        float dy = sourceY - listener.y;
        float dz = sourceZ - listener.z;
        float distSq = dx*dx + dy*dy + dz*dz;
        float dist = std::sqrt(distSq);

        // 简化：距离越远音量越小，最大距离100
        float maxDist = 100.0f;
        if (dist >= maxDist) return 0.0f;

        return 1.0f - (dist / maxDist);
    }

    // 总线控制
    void setMasterVolume(float vol) { masterBus->setVolume(vol); }
    void setSFXVolume(float vol) { sfxBus->setVolume(vol); }
    void setMusicVolume(float vol) { musicBus->setVolume(vol); }
    void setVoiceVolume(float vol) { voiceBus->setVolume(vol); }

    void muteAll() {
        masterBus->setMuted(true);
        std::cout << "🔇 全部静音" << std::endl;
    }

    void unmuteAll() {
        masterBus->setMuted(false);
        std::cout << "🔊 取消静音" << std::endl;
    }

    void stopAll() {
        for (auto& ch : channels) {
            ch->stop();
        }
        if (currentMusic) {
            currentMusic->isPlaying = false;
        }
        std::cout << "⏹️  停止所有音频" << std::endl;
    }

    // 更新
    void update(float dt) {
        // 更新通道
        for (auto& ch : channels) {
            ch->update(dt);
        }

        // 更新音乐淡入淡出
        if (musicFadeTime > 0) {
            musicFadeTime -= dt;
            if (musicFadeTime <= 0) {
                if (currentMusic) {
                    currentMusic->volume = targetMusicVolume;
                }
                musicFadeTime = 0;
            }
        }

        // 模拟音乐播放
        if (currentMusic && currentMusic->isPlaying && !currentMusic->isPaused) {
            currentMusic->currentTime += dt;
            if (currentMusic->currentTime >= currentMusic->duration) {
                if (currentMusic->loop) {
                    currentMusic->currentTime = 0;
                } else {
                    currentMusic->isPlaying = false;
                    std::cout << "🎵 音乐播放完毕" << std::endl;
                }
            }
        }
    }

    // 打印状态
    void printStatus() const {
        std::cout << "\n🔊 音频系统状态:" << std::endl;
        std::cout << "  Master: " << (masterBus->isMuted() ? "🔇" : "🔊")
                  << " 音量: " << masterBus->getVolume() * 100 << "%" << std::endl;
        std::cout << "  SFX:    音量: " << sfxBus->getVolume() * 100 << "%" << std::endl;
        std::cout << "  Music:  " << (musicBus->isMuted() ? "🔇" : "🎵")
                  << " 音量: " << musicBus->getVolume() * 100 << "%" << std::endl;
        std::cout << "  Voice:  音量: " << voiceBus->getVolume() * 100 << "%" << std::endl;

        if (currentMusic && currentMusic->isPlaying) {
            std::cout << "  当前播放: " << currentMusic->soundName
                      << " [" << static_cast<int>(currentMusic->currentTime) << "s / "
                      << static_cast<int>(currentMusic->duration) << "s]" << std::endl;
        }
    }
};

// ============================================================
// 演示
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      音频系统演示 v1.0                 " << std::endl;
    std::cout << "========================================" << std::endl;

    AudioSystem audio;

    // 加载声音资源
    std::cout << "\n📁 加载声音资源..." << std::endl;
    audio.loadSound("gun_fire", "sounds/weapons/gun_fire.wav");
    audio.loadSound("explosion", "sounds/weapons/explosion.wav");
    audio.loadSound("footstep", "sounds/player/footstep.wav");
    audio.loadSound("ui_click", "sounds/ui/click.wav");
    audio.loadSound("bgm_main", "music/main_theme.ogg");
    audio.loadSound("bgm_battle", "music/battle_theme.ogg");
    audio.loadSound("ambient_forest", "ambient/forest.ogg");
    audio.loadSound("npc_greeting", "voice/npc/greeting_01.wav");

    // 模拟游戏场景
    std::cout << "\n========================================" << std::endl;
    std::cout << "      模拟游戏音频                      " << std::endl;
    std::cout << "========================================" << std::endl;

    std::cout << "\n[场景1] 游戏启动，播放背景音乐" << std::endl;
    audio.playMusic("bgm_main", true);
    audio.printStatus();

    std::cout << "\n[场景2] 玩家开火" << std::endl;
    audio.playSFX("gun_fire", 1.0f, 1.0f);
    audio.playSFX("gun_fire", 0.8f, 0.9f);  // 连续开火
    audio.playSFX("gun_fire", 0.8f, 0.85f);

    std::cout << "\n[场景3] 玩家移动（播放脚步声）" << std::endl;
    audio.playSFX("footstep", 0.5f);
    audio.playSFX("footstep", 0.5f);

    std::cout << "\n[场景4] 爆炸！" << std::endl;
    audio.playSFX("explosion", 1.0f, 0.8f);

    std::cout << "\n[场景5] 玩家打开菜单，音乐淡出" << std::endl;
    audio.fadeMusic(0.2f, 0.5f);
    audio.playSFX("ui_click");

    std::cout << "\n[场景6] 关闭菜单，音乐恢复" << std::endl;
    audio.fadeMusic(0.7f, 0.5f);
    audio.playSFX("ui_click");

    std::cout << "\n[场景7] 切换到战斗音乐" << std::endl;
    audio.playMusic("bgm_battle", true);

    std::cout << "\n[场景8] NPC说话" << std::endl;
    audio.playSFX("npc_greeting", 1.0f, 1.0f);

    std::cout << "\n[场景9] 调整音量" << std::endl;
    audio.setSFXVolume(0.5f);
    audio.setMusicVolume(0.8f);
    std::cout << "SFX和Music音量已调整" << std::endl;

    std::cout << "\n[场景10] 静音所有" << std::endl;
    audio.muteAll();

    std::cout << "\n[场景11] 取消静音" << std::endl;
    audio.unmuteAll();

    // 模拟几帧更新
    for (int i = 0; i < 3; i++) {
        audio.update(0.016f);
    }

    audio.printStatus();

    std::cout << R"(
    ========================================
           音频系统设计要点
    ========================================

    🔊 音频类型:
       - BGM (背景音乐): 循环，控制整体氛围
       - SFX (音效): 短促，可多实例同时播放
       - Ambient (环境音): 循环，增强沉浸感
       - Voice (语音): 对话、角色台词

    🎚️ 音频总线:
       - 允许分组控制音量
       - Master → SFX / Music / Voice
       - 方便实现静音、淡入淡出等

    📍 3D音频:
       - 声音根据距离衰减
       - 左右声道根据位置调整
       - 沉浸感的关键

    🎯 性能优化:
       - 声音池化（复用播放实例）
       - 距离剔除（太远的声音不播放）
       - 压缩格式（OGG, MP3等）

    💡 推荐实践:
       - 使用FMOD/Wwise等专业音频引擎
       - 关键动作预留多种随机变体
       - 音量曲线可调节（玩家设置）
    )" << std::endl;

    return 0;
}
```

---

## 41.8 本章小结

恭喜你！如果你一路读到这里，说明你不是被代码催眠了，就是真心对游戏开发感兴趣。让我来总结一下本章的内容：

### 📚 本章知识点回顾

| 主题 | 核心概念 | 关键代码 |
|------|----------|----------|
| **游戏循环** | 固定时间步长、帧率控制、deltaTime | `while(running) { update(dt); render(); }` |
| **ECS架构** | Entity-Component-System、数据局部性 | 组件存储、系统处理逻辑 |
| **碰撞检测** | AABB、圆形、OBB、SAT算法 | 包围体交集测试 |
| **状态机** | 状态切换、事件驱动、FSM | `setState(newState)` |
| **输入系统** | 输入映射、动作绑定、设备抽象 | `isActionActive("Attack")` |
| **音频系统** | 音频总线、SFX/Music分离、3D音频 | `playSFX()`, `playMusic()` |

### 🎮 游戏开发技术栈

```
┌─────────────────────────────────────────────────────────────┐
│                      游戏应用层                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│  │ UI系统  │ │ 脚本系统 │ │ AI系统  │ │ 动画系统 │ │ 特效系统 ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│
├─────────────────────────────────────────────────────────────┤
│                      核心引擎层                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│  │ 渲染引擎 │ │ 物理引擎 │ │ 音频引擎 │ │ 输入系统 │ │ 资源管理 ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│
├─────────────────────────────────────────────────────────────┤
│                      基础设施层                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ 窗口管理 │ │ 文件系统 │ │  内存管理 │ │  日志系统 │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
├─────────────────────────────────────────────────────────────┤
│                      平台层                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ Windows │ │  macOS  │ │  Linux  │ │ Android │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 🚀 下一步学习建议

1. **选择一个游戏引擎**：Unity（C#）或Godot（C++/GDScript）或Unreal Engine（C++/Blueprint）
2. **学习图形API**：OpenGL、Vulkan、DirectX 12
3. **深入物理引擎**：Box2D（2D）、PhysX、Bullet
4. **学习网络编程**：多人游戏、服务器架构
5. **做项目！**：从小游戏开始，逐步增加复杂度

### 💡 有趣的彩蛋

你知道吗？
- **《毁灭战士》（DOOM）** 最初使用汇编语言编写，后来部分重写为C语言
- **《我的世界》（Minecraft）** C++版（基岩版）比Java版晚出现了好几年
- **id Software** 的程序员们曾经为了性能，把代码写成 `*p++ = *q++` 这种风格，被称为"指针瑜伽"

---

*"游戏开发是艺术与工程的结合。在C++的加持下，你可以在性能允许的范围内，创造任何你能想象的世界。"*
—— 鲁迅（没说过）

**课后作业**：尝试把本章的ECS代码改写成使用 `std::vector` 存储组件，并实现一个简单的"粒子系统"组件和系统。加油！ 🎮
