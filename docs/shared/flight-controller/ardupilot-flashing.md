# ArduPilot 固件说明

## 支持情况

FlyingRC® 多款飞控支持 **ArduPilot（ArduPlane / ArduCopter）**。固定翼推荐使用 ArduPlane。

## 固件获取

- 官方 QQ 群文件
- 官网固件下载页
- 请以产品页标注的 **Board ID / Target** 为准，不要刷入其他型号固件

## 刷写方式

### Mission Planner

1. 连接飞控 USB。
2. 打开 Mission Planner → 初始设置 → 安装固件。
3. 选择对应机型与固件版本。
4. 等待刷写完成后重启。

### 其他

- 也可使用 `ardupilot` 官方工具链 / beta 固件站（需自行确认 Target）。

## 典型默认串口映射

不同产品串口定义不同，请以本产品「串口映射」章节为准。固定翼常见推荐：

- **ELRS / 接收机** → Serial1（UART1）
- **GPS** → Serial3（UART5 或 UART2，视型号）
- **MSP OSD / 高清图传** → Serial4（UART4）

## 注意

!!! info "技术支持范围"

    部分产品仅 ArduPilot 固件提供有限技术支持，INAV / Betaflight 可能无官方技术支持。
