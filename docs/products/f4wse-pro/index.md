# FlyingRC® F4WSE PRO 固定翼飞控

![F4WSE PRO](../../assets/f4wse-pro/product-hero.jpg){ width="360" }

**型号**：F4WSE Pro  
**类别**：固定翼飞控  
**状态**：在售（本店销量靠前）  
**手册更新日期**：2026-08-15（**全站公共内容口径以本手册为准**）  
**官方零售价参考**：140 元

---

## 产品简介

F4WSE PRO 在 F4WSE 基础上全面升级：Boot 按钮、免焊 USB 小板、可直插四合一电调 / 接收机 / GPS / 高清天空端、双模拟摄像头切换、2OZ 厚铜电流计。适合小型 FPV 载机、改装手抛机，也可用于 Y3 / 四轴 / 垂起固定翼（VTOL）。

### 相对 F4WSE 的升级

1. 升级 Boot 按钮，方便使用
2. USB 小板无需焊接
3. 可直插 4 合 1 电调，轻松制作四轴垂起
4. 可直插接收机、GPS、高清天空端
5. 增加双模拟摄像头切换功能
6. PCB 工艺升级至 2OZ 厚铜板，增强电流计持续过流能力

### 产品特点

- 体积小，适合小型 FPV 载机或改装手抛机
- 共 12 路 PWM，可扩展 Y3 / 四轴 / 大型载机 / VTOL
- 高精度陀螺仪与气压计
- 板载电流计，双路 5V BEC
- 外置 USB 小板、外置 TF 卡小板，装机布局更灵活
- 支持 ArduPilot（出厂默认）与 INAV
- 可接 WS2812 灯带

---

## 基础参数

| 项目 | 参数 |
|------|------|
| 型号 | FlyingRC® F4WSE Pro |
| 主控 | STM32F405RGT6，168 MHz，Flash 1 MB，RAM 192 KB |
| IMU | ICM-42688-P；BMI270（2026/5/25 后上市产品） |
| 气压计 | SPA06-001 |
| 磁力计 | 无板载 |
| 模拟 OSD | AT7465E |
| 尺寸 | 22.86 × 43.18 × 9 mm |
| 质量 | 9.1 g |
| UART | 6 组：UART1–UART6 |
| PWM | 共 12 路：2.54 排针 6 路 + 焊盘 2 路 + 四合一电调接口 4 路 |
| I2C | 1 |
| 电流计 ADC | 支持，持续 80A，瞬间 120A |
| 蜂鸣器 | 有，支持无源蜂鸣器 |
| LED 灯带 | WS2812（INAV 灯带信号接 S12 焊盘） |
| BEC-设备 | 5V3A（MP9943+MP9447） |
| BEC-舵机 | 5V5A |
| 电源输入 / VBAT | 7–28 V DC，2–6S LiPo |
| USB | Type-C 外置 USB 小板 |
| 黑匣子 | 外接 TF 卡模块，可用最大 4GB，最高支持 32GB |
| SBUS | 内置反向器，内部连接至 UART2 RX |
| 工作温度 | -10–100 ℃ |
| 存储温度 | 0–40 ℃ |
| 固件 | ArduPilot ✓（出厂默认）/ INAV ✓ / Betaflight ✓ / PX4 ✗ |

### 固件 Target

飞控直接兼容 **MatekF405-TE** 固件。

| 固件 | Target / 版本示例 |
|------|-------------------|
| ArduPlane | V4.6.3 MatekF405-TE |
| ArduCopter | V4.6.3 MatekF405-TE |
| INAV | 8.0.1 MatekF405TE_SD |
| Betaflight | MatekF405-TE |

!!! warning "BMI270 批次"

    官方淘宝店 **2026 年 5 月 23 日后**出售的最新版本陀螺仪更换为 BMI270，刷写 AP / INAV 固件请进入官方 QQ 群下载对应版本。

---

## 使用方法

### 布局

![正面](../../assets/f4wse-pro/layout-front.jpg)

![反面](../../assets/f4wse-pro/layout-back.jpg)

![插口功能](../../assets/f4wse-pro/connector-functions.jpg)

### 使用前准备

工具与耗材：

- 数控烙铁 / 焊台（推荐 T12 或 936 系列）
- 焊锡丝（推荐 63% 含锡量）
- 硅胶线：信号线 28–30 AWG，电源线 14–18 AWG
- 35V 470uF 固态电容（并联在电源输入焊盘，可不焊）
- 10V 2A 降压模块（可选；大疆 / 蜗牛高清及部分滤波不佳的模拟摄像头与图传需要）

### USB 小板与 TF 卡小板

![USB 接线](../../assets/f4wse-pro/usb-board-wiring.jpg)

![USB 引脚](../../assets/f4wse-pro/usb-board-pinout.png)

![TF 线序](../../assets/f4wse-pro/tf-board-wiring.jpg)

![TF 连接](../../assets/f4wse-pro/tf-board-connection.jpg)

!!! note "端子"

    信号线需使用硅胶线；接线端子为 SH1.0，插拔时请用手抵住插座后部，防止插座受力脱落。

### 固件与教程

固定翼推荐 ArduPlane / INAV，出厂默认已刷 ArduPlane。

- 可通过 Mission Planner 等地面站直接刷写 MatekF405-TE

![Mission Planner](../../assets/f4wse-pro/mission-planner-target.png)

### 接线

#### 完整示例

![完整接线](../../assets/f4wse-pro/wiring-full-example.jpg)

!!! warning "四合一电调接口"

    4 合 1 电调接口**只用于电压检测，无法为飞控供电**。  
    电调有 V3.2 与 V4.0 两版，接线顺序不同；V4.0 符合 BF 线序规范。

![版本识别](../../assets/f4wse-pro/esc-v32-v40-socket.png)

![丝印版本](../../assets/f4wse-pro/esc-version-marks.jpg)

#### 分设备接线

![ELRS](../../assets/f4wse-pro/wiring-elrs.jpg)

![SBUS](../../assets/f4wse-pro/wiring-sbus.jpg)

![GPS](../../assets/f4wse-pro/wiring-gps.jpg)

!!! warning "GPS 线序"

    请仔细查看 GPS 上的丝印标识。

![模拟摄像头](../../assets/f4wse-pro/wiring-analog-camera.png)

![4IN1 V3.2](../../assets/f4wse-pro/wiring-4in1-v32.jpg)

![4IN1 V4.0](../../assets/f4wse-pro/wiring-4in1-v40.jpg)

![高清图传](../../assets/f4wse-pro/wiring-hd-vtx-sbus.jpg)

![O4 BEC](../../assets/f4wse-pro/wiring-o4-bec.png)

![40A 电调](../../assets/f4wse-pro/wiring-40a-esc.jpg)

![75A 电调](../../assets/f4wse-pro/wiring-75a-esc.jpg)

![二合一电调](../../assets/f4wse-pro/wiring-dual-esc.jpg)

#### 双模拟摄像头切换（AP）

两路摄像头视频信号分别接 **C0、C1**，图传视频输入接 **VTX**；摄像头与图传共地并按额定电压供电。

控制脚 **PB5**（hwdef 中 PINIO2 / GPIO82）可配置为 Relay2：

| 参数 | 值 |
|------|-----|
| RELAY2_PIN | 82 |
| RELAY2_FUNCTION | 1 |
| RELAY2_DEFAULT | 0 |
| RELAY2_INVERTED | 0 |
| 示例 RC8_OPTION | 34（Relay2） |

默认画面相反时可将 `RELAY2_INVERTED` 改为 1，或交换两路视频线。

### PWM 输出（ArduPilot）

| Group | 通道 | GPIO | Timer | DMA/DShot |
|-------|------|------|-------|-----------|
| 1 | S1 排针（单体电调） | GPIO50 | TIM8_CH4 | DMA/DShot |
| 1 | S2 排针（单体电调） | GPIO51 | TIM8_CH3 | DMA/DShot |
| 2 | S3 排针（舵机） | GPIO52 | TIM1_CH3N | DMA/DShot |
| 2 | S4 排针（舵机） | GPIO53 | TIM1_CH1 | DMA/DShot |
| 3 | S5–S8 插口（四合一） | GPIO54–57 | TIM2 | DMA/DShot |
| 4 | S9 排针（舵机） | GPIO58 | TIM12_CH1 | 无 DMA |
| 5 | S10 排针（舵机） | GPIO59 | TIM13_CH1 | 无 DMA |
| 6 | S11 焊盘（舵机） | GPIO60 | TIM4_CH1 | 无 DMA |
| 7 | S12 焊盘（WS2812） | GPIO61 | TIM3_CH4 | DMA/DShot |

- LED：`SERVO12_FUNCTION 120`，`NTF_LED_TYPES neopixel`
- 同组 PWM 不可同时用于 DShot 电调和 50Hz 舵机
- **S9、S10、S11 无 DMA，不能接 DShot 电调**

### 串口映射

| PCB 丝印 | UART | Protocol | 建议功能 | SERIAL |
|----------|------|----------|----------|--------|
| USB | USB | console | — | SERIAL0 |
| TX1 RX1 | USART1 | with DMA | MSP Displayport | SERIAL1 |
| TX3 RX3 | USART3 | NO DMA | USER | SERIAL2 |
| TX5 RX5 | UART5 | NO DMA | GPS | SERIAL3 |
| TX4 RX4 | UART4 | NO DMA | USER | SERIAL4 |
| TX6 RX6 | USART6 | TX6 with DMA | USER | SERIAL5 |
| TX2 RX2 / SBUS | USART2 | with DMA | SBUS | SERIAL6 |

数据量大的设备（CRSF、高清天空端）推荐接 **UART1（SERIAL1）** 或 **UART2（SERIAL6）**。

!!! important "焊接后必须改参数"

    例如 GPS 接 R5/T5 → Serial3，则需将 `Serial3_Protocol` 设为 GPS，并确认其它端口未被设为 GPS。

### I2C

- Compass：`COMPASS_AUTODEC=1`
- 板载气压计 SPA06-001 地址 **0x76**，外部不可再接 0x76 设备
- 空速计：MS4525（`ARSPD_TYPE=1`）或 DLVLR-L10D（`ARSPD_TYPE=9`）

### 通用参数

**ArduPilot**

```text
LOG_BACKEND_TYPE = 1
BATT_VOLT_PIN    = 14
BATT_VOLT_MULT   = 21.0
BATT_CURR_PIN    = 15
BATT_AMP_PERVLT  = 100
```

**INAV**

- 电压计比例默认值 2100
- 电流计比例默认值 100

### 发货清单

![发货清单](../../assets/f4wse-pro/packing-list.png){ width="420" }

---

## USB 驱动与连接

--8<-- "shared/flight-controller/usb-driver.md"

---

## ArduPilot 固件说明

--8<-- "shared/flight-controller/ardupilot-flashing.md"

---

## INAV 固件说明

--8<-- "shared/flight-controller/inav-flashing.md"

---

## 接收机连接

--8<-- "shared/flight-controller/receiver-wiring.md"

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

!!! note "固件支持范围"

    本产品 ArduPilot 固件提供有限技术支持，INAV 和 BF 固件无技术支持。

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
