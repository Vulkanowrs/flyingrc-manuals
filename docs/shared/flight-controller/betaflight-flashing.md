# Betaflight 固件说明

## 支持情况

部分 FlyingRC® 飞控支持 **Betaflight**（多为穿越机飞控）。请以产品参数为准。

## 刷写步骤

1. USB 连接，打开 Betaflight Configurator。
2. 选择对应 Target / Board。
3. 下载并刷写固件。
4. 重新配置端口、接收机、电机顺序等。

## 注意

- 刷写前备份 CLI `dump`。
- 穿越机飞控请确认电机协议（DShot）与 PWM 分组限制。
- 部分产品 BF **无官方技术支持**。
