# FlyingRC® AM32 75A ESC V2.5 单体电调

![AM32 75A](../../assets/am32-75a-v25/product-hero.png){ width="320" }

**型号**：AM32 75A Single ESC V2.5  
**类别**：单体电调  
**状态**：在售  
**官方零售价参考**：87 元（不带 BEC 版本）

---

## 产品简介

英飞凌金封 MOS 单体电调，持续 75A（4S 测试条件），支持 AM32 固件、DShot/OneShot/PWM，可选板载 BEC（5V4A / 可调 7V3A）。适合小型 FPV 载机及攀爬车等低速大扭矩场景。

### 产品特点

- AT32F421K8U7 + FD6288/JSM6288Q + 英飞凌 IRF7480 金封 MOS
- Rdson 约 0.95 mΩ@10V，双面散热
- 贴片方形铜条，电阻较上代降低约 60%
- 板载 TVS 浪涌抑制
- 可选 SC8102 BEC：5V4A，短接焊盘可调 7V3A
- 正弦波启动 + 失速保护（可选）
- 支持 DShot150/300/600、OneShot、PWM

---

## 基础参数

| 项目 | 参数 |
|------|------|
| 型号 | FlyingRC® AM32 75A Single ESC |
| 持续电流 | 75A（测试条件：4S） |
| 瞬间电流 | 85A（测试条件：4S） |
| VBAT | 7–28 V DC，2–6S LiPo |
| 尺寸 | 38 × 19 × 7.4 mm |
| 质量 | 8 g |
| 主控 | AT32F421K8U7，120 MHz，Flash 64 KB，RAM 16 KB |
| 栅极驱动 | FD6288 / JSM6288Q |
| MOS | 英飞凌 IRF7480 金封 |
| BEC | SC8102，5V4A，可调至 7V3A |
| 固件 | AM32 |
| 控制信号 | DShot150/300/600、OneShot、PWM 等 |
| 遥测 | 有转速回传 |
| LED | 无 |
| 工作温度 | -10–100 ℃ |
| 存储温度 | 0–40 ℃ |

---

## 使用方法

### 布局

![控制板](../../assets/am32-75a-v25/layout-control-board.png)

![功率板](../../assets/am32-75a-v25/layout-power-board.png)

![焊盘定义](../../assets/am32-75a-v25/pad-definition.png)

### 焊盘定义

| 序号 | 名称 | 定义 |
|------|------|------|
| 1 | S | PWM/DShot 信号输入 |
| 2 | TX | 电调回传 TX |
| 3 | G | GND |
| 4 | BEC+ | 5V / 7.4V BEC 正极 |
| 5 | BEC- | 5V / 7.4V BEC 负极 |
| 6 | 7.4V | 短接此焊盘，BEC 输出 7.4V |
| 7 | V+ | 接电池正极 |
| 8 | V- | 接电池负极 |
| 9 | - | 接电机三相线 |

### 接线图

![H7Wlite](../../assets/am32-75a-v25/wiring-h7wlite.jpg)

![F4WSE PRO](../../assets/am32-75a-v25/wiring-f4wse-pro.jpg)

![F4Wing Mini](../../assets/am32-75a-v25/wiring-f4wing-mini.jpg)

![调参器](../../assets/am32-75a-v25/wiring-am32-programmer.png)

### 使用前准备

#### 粘贴散热片（不可省略）

1. 涂抹优质导热硅脂到六个 MOS，均匀覆盖。

![步骤1](../../assets/am32-75a-v25/heatsink-step1.png)

2. 按压散热片时四周滑动，使硅脂布满 MOS。

![步骤2](../../assets/am32-75a-v25/heatsink-step2.png)

3. 使用针筒涂抹导热硅胶固定散热片。

![步骤3](../../assets/am32-75a-v25/heatsink-step3.png)

![步骤4](../../assets/am32-75a-v25/heatsink-step4.png)

![步骤5](../../assets/am32-75a-v25/heatsink-step5.png)

![完成](../../assets/am32-75a-v25/heatsink-done.png)

硅胶约 2 小时凝固，可用吹风加速。

#### 电容焊接

![BEC 电容](../../assets/am32-75a-v25/cap-bec.png)

包装内 **10V 330uF** 固态电容焊到 BEC+、BEC-。  
注意：电容顶部红色横线对应引脚接 **BEC-**。

![功率电容](../../assets/am32-75a-v25/cap-power.png)

包装内 **50V 470uF** 固态电容焊到功率板反面两个小焊盘。  
注意：电容外皮黄色横线对应引脚接 **负极**。

#### 电源线与信号线

![电源线](../../assets/am32-75a-v25/wiring-power.jpg)

- 下方黑线（负极）、红线（正极）接电源；铜线可接铜条以增大过流。
- 上方三根线接无刷电机三相。
- 确保焊点饱满，与旁边元器件无短路。

![带 BEC 信号](../../assets/am32-75a-v25/wiring-signal-with-bec.jpg)

带板载 BEC：白（信号）、黑（负极）、红（BEC 输出正极）。

![不带 BEC](../../assets/am32-75a-v25/wiring-signal-no-bec.jpg)

不带板载 BEC：白（信号）、黑（负极）、红悬空。

---

## 固件与调参

--8<-- "shared/esc/am32-setup.md"

--8<-- "shared/esc/motor-direction.md"

---

## 安全须知

--8<-- "shared/safety.md"

---

## 焊接注意

--8<-- "shared/soldering.md"

---

## 首次使用检查

--8<-- "shared/first-use-check.md"

---

## 技术支持

--8<-- "shared/support.md"

---

## 售后与保修

--8<-- "shared/warranty.md"

---

## 常见问题

--8<-- "shared/faq.md"

---

## 品牌介绍

--8<-- "shared/brand-intro.md"

---

## 免责声明

--8<-- "shared/disclaimer.md"
