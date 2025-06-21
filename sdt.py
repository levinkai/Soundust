from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen

import sys

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()


# 获取屏幕的完整尺寸（无视 Dock）
screen_rect = screen.geometry()
screen_width = screen_rect.width()
screen_height = screen_rect.height()

# 窗口位置（直接定位到屏幕右下角）
window_width = 100
window_height = 50
margin = 10  # 边距

x = screen_width - window_width - margin
y = screen_height - window_height - margin  # 从顶部向下计算（坐标系原点在左上角）

window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
window.setAttribute(Qt.WA_TranslucentBackground)
window.setStyleSheet("background: transparent;")
window.setGeometry(x, y, window_width, window_height)

label = QLabel("Hello PySide!", window)
label.setStyleSheet("color: white; font-size: 24px; background: transparent;")
label.setAlignment(Qt.AlignCenter)

window.show()

def get_dock_rect():
    """返回 Dock 的坐标和大小 (QRect)"""
    screen = QApplication.primaryScreen()
    screen_rect = screen.geometry()
    available_rect = screen.availableGeometry()
    
    dock_rect = {
        "x": 0,
        "y": 0,
        "width": 0,
        "height": 0
    }
    
    # Dock 在底部
    if available_rect.y() > 0:
        dock_rect["x"] = 0
        dock_rect["y"] = 0
        dock_rect["width"] = screen_rect.width()
        dock_rect["height"] = available_rect.y()
    # Dock 在左侧
    elif available_rect.x() > 0:
        dock_rect["x"] = 0
        dock_rect["y"] = 0
        dock_rect["width"] = available_rect.x()
        dock_rect["height"] = screen_rect.height()
    # Dock 在右侧
    elif available_rect.width() < screen_rect.width():
        dock_rect["x"] = available_rect.width()
        dock_rect["y"] = 0
        dock_rect["width"] = screen_rect.width() - available_rect.width()
        dock_rect["height"] = screen_rect.height()
    
    return dock_rect

sys.exit(app.exec())