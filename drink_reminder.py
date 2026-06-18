import pystray
from pystray import MenuItem as Item
from PIL import Image, ImageDraw
import threading
import time
import subprocess
import sys

# 由于你确认是 Windows 系统，直接调用原生命令即可，无需判断其他系统
# 这种方式不需要安装 plyer，且兼容性好

def send_native_notification(title, message):
    """
    使用 Windows 原生命令发送通知
    基于 WScript.Shell，无需任何额外依赖库
    """
    try:
        # 使用 PowerShell 调用 WScript.Shell.Popup 显示弹窗通知
        # 参数：消息内容，超时(秒), 标题, 图标类型(64=信息, 48=警告, 32=错误)
        command = (
            f'powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; '
            f'$WshShell.Popup(\'{message}\', 10, \'{title}\', 64)"'
        )

        # 尝试运行命令，shell=True 确保 PowerShell 能正确解析
        subprocess.run(command, shell=True, check=True)
        
        print(f"✅ 通知已发送: {title}")
        
    except Exception as e:
        # 如果弹窗失败（例如权限问题），至少打印到控制台
        print(f"❌ 通知发送失败 (原生命令): {e}")
        print(f"💡 提示: {title} - {message}")

def create_icon_image():
    """生成一个蓝色的图标"""
    img = Image.new('RGB', (64, 64), color='#2196F3')
    draw = ImageDraw.Draw(img)
    draw.ellipse([16, 8, 48, 40], fill='#64B5F6')
    draw.ellipse([24, 16, 40, 32], fill='#BBDEFB')
    return img

def send_notification():
    """发送桌面通知（使用原生 Windows 方法）"""
    title = '喝水提醒 💧'
    message = '该起来喝水啦！保持身体健康~'
    send_native_notification(title, message)

def is_work_time():
    """检查当前是否在工作时间内"""
    now = time.localtime()
    weekday = now.tm_wday  # 0=周一, 6=周日
    hour = now.tm_hour
    minute = now.tm_min

    # 仅工作日（周一到周五）
    if weekday >= 5:  # 周六、周日
        return False

    # 上午时段: 9:30-12:00
    morning_start = (9, 30)
    morning_end = (12, 0)

    # 下午时段: 14:00-19:30
    afternoon_start = (14, 0)
    afternoon_end = (19, 30)

    current = (hour, minute)

    in_morning = morning_start <= current < morning_end
    in_afternoon = afternoon_start <= current < afternoon_end

    return in_morning or in_afternoon

def is_half_hour():
    """检查当前是否在半点（30分）"""
    now = time.localtime()
    return now.tm_min == 30

def reminder_loop(stop_event):
    """定时任务循环 - 工作日半点提醒"""
    while not stop_event.is_set():
        now = time.localtime()
        weekday_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.tm_wday]
        print(f"[{now.tm_hour:02d}:{now.tm_min:02d}] 检查提醒... ({weekday_name})")

        # 检查是否满足提醒条件
        if is_work_time() and is_half_hour():
            send_notification()
            print(f"✅ 已发送提醒")

        # 每30秒检查一次，减少资源占用
        for _ in range(30):
            if stop_event.is_set():
                break
            time.sleep(1)

def on_quit(icon, item):
    """退出回调"""
    icon.stop()

def main():
    stop_event = threading.Event()

    icon_image = create_icon_image()

    menu = (
        Item('发送测试通知', lambda icon, item: send_notification()),
        Item('退出', on_quit),
    )

    try:
        icon = pystray.Icon(
            'drink_reminder',
            icon_image,
            '喝水提醒 - 工作日半点提醒',
            menu
        )

        print("🚀 喝水提醒程序已启动...")
        print("📅 提醒规则: 工作日 9:30-12:00 / 14:00-19:30 的半点提醒")
        print("👉 点击任务栏托盘图标可以发送测试通知或退出")
        
        reminder_thread = threading.Thread(target=reminder_loop, args=(stop_event,), daemon=True)
        reminder_thread.start()
        
        icon.run()
    except Exception as e:
        print(f"程序运行时出错: {e}")
        send_native_notification("程序启动失败", "请检查 pystray 依赖是否正确安装")

if __name__ == '__main__':
    main()
