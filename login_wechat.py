import win32gui
import pyautogui
import win32con

# 获取应用程序窗口句柄
handle = win32gui.FindWindow(None, '微信')

# 将窗口置顶
win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
left, top, right, bottom = win32gui.GetWindowRect(handle)

# # 计算窗口中心点坐标
x = (left + right) // 2
y = (top + bottom) // 2
print(x, y)

# 将鼠标移动到窗口中心并点击
pyautogui.click(x, y)

# 模拟按回车，就可以登录
pyautogui.press('enter')
