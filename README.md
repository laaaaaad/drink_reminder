# 喝水提醒小程序

一款运行在 Windows 系统托盘的喝水提醒工具，帮助你养成健康的饮水习惯。

## 功能特点

- 系统托盘运行，不打扰正常工作
- 工作日定时提醒（周一至周五）
- 智能提醒时段：
  - 上午：9:30 - 12:00
  - 下午：14:00 - 19:30
- 每半小时提醒一次（半点提醒）
- 右键托盘图标可发送测试通知或退出程序

## 使用方法

### 方式一：直接运行 Python 脚本

```bash
python drink_reminder.py
```

### 方式二：运行打包后的 exe

1. 双击 `drink_reminder.exe` 启动
2. 或双击 `start.vbs` 启动（无窗口后台运行）

### 开机自启动

将 `start.vbs` 或 `dist\drink_reminder.exe` 的快捷方式放入以下目录：
```
C:\Users\<用户名>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

## 打包 exe

如果需要重新打包，运行：

```bash
build.bat
```

打包后的文件位于 `dist\drink_reminder.exe`

## 依赖

- Python 3.8+
- pystray
- Pillow

安装依赖：
```bash
pip install -r requirements.txt
```

## 文件说明

| 文件 | 说明 |
|------|------|
| drink_reminder.py | 主程序 |
| build.bat | 打包脚本 |
| start.vbs | 后台启动脚本 |
| dist\drink_reminder.exe | 打包后的可执行文件 |
