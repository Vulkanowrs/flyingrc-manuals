# USB 驱动与连接

## 飞控 USB

FlyingRC® 飞控板载 **Type-C** 接口（部分型号为 Micro-USB），连接电脑后：

1. 使用数据线（非仅充电线）连接电脑。
2. Windows 一般可自动识别为串口设备（COMx）。
3. 若地面站无法识别，安装对应 USB 驱动或使用 Zadig / STM32 驱动补丁。

## 地面站

| 固件 | 常用地面站 |
|------|------------|
| ArduPilot | Mission Planner / QGroundControl |
| INAV | INAV Configurator |
| Betaflight | Betaflight Configurator |

## 手机调参（部分型号）

Type-C 飞控可通过 **双 C 线**连接手机，使用手机版地面站调参：

- ArduPilot 建议使用 **QGroundControl App**
- 部分 BF/INAV 机型支持对应手机 App

## 常见问题

- **设备管理器无串口**：换数据线 / 换 USB 口；确认是否仅充电线。
- **驱动黄色感叹号**：安装 STM32 Virtual COM Port 驱动。
- **飞控需要 5V 外部供电**：部分超小型飞控仅 USB 可能无法稳定工作，确认已接 BEC 5V。
