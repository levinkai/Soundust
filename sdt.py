#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sdt.py
@说明    : 透明悬浮窗贴近dock边缘，自动适应dock方向与自动调整大小与字体方向
@时间    :2025/06/24 13:19:23
@作者    :LevinKai
@版本    :2.1
'''

from typing import Dict, Tuple, Literal
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QScreen, QFont, QPainter, QPixmap, QColor
import sys

class VerticalLabel(QLabel):
    """竖排显示文本的QLabel（自定义paintEvent实现）"""
    def __init__(self, text, parent=None, clockwise=True):
        super().__init__(text, parent)
        self.clockwise = clockwise  # True: 逆时针旋转90度, False: 顺时针旋转90度

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 竖排旋转
        if self.clockwise:
            # 从左到右旋转90度
            painter.translate(self.width(), 0)
            painter.rotate(90)
            rect = QRect(0, 0, self.height(), self.width())
        else:
            # 从右到左旋转270度
            painter.translate(0, self.height())
            painter.rotate(-90)
            rect = QRect(0, 0, self.height(), self.width())
        # 设置透明背景
        painter.setOpacity(1.0)
        # 使用label的字体和样式
        painter.setFont(self.font())
        pen = painter.pen()
        pen.setColor(self.palette().color(self.foregroundRole()))
        painter.setPen(pen)
        painter.drawText(rect, self.alignment(), self.text())

class TransparentOverlay:
    """
    透明悬浮窗，自动适应dock位置与方向，窗口大小根据字体自动调整。
    """

    def __init__(
        self,
        text: str = "Hello PySide!",
        margin: int = 10,
        font_color: str = "white",
        font_size: int = 24
    ):
        """
        初始化透明悬浮窗。

        Args:
            text: 显示的文本
            margin: 距离dock或屏幕边缘的间距
            font_color: 字体颜色
            font_size: 字号
        """
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.text = text
        self.margin = margin
        self.font_color = font_color
        self.font_size = font_size

        self._setup_ui()
        self._position_window()

    def _setup_ui(self) -> None:
        """设置透明窗口UI和字体参数。"""
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        self.window.setStyleSheet("background: transparent;")

        self.font = QFont()
        self.font.setPointSize(self.font_size)

        # label先留空，方向在_position_window时根据dock方向设置
        self.label = None

    def _position_window(self) -> None:
        """将窗口贴近dock边缘，并根据dock方向调整窗口和字体方向与大小。"""
        screen = QApplication.primaryScreen()
        screen_rect: QRect = screen.geometry()
        avail_rect: QRect = screen.availableGeometry()
        dock_rect, dock_pos = self.get_dock_rect_and_pos(screen, screen_rect, avail_rect)

        # 横向/竖向
        if dock_pos in ("left", "right"):
            # 竖向显示（自定义label）
            label = VerticalLabel(self.text, self.window, clockwise=(dock_pos == "right"))
            label.setFont(self.font)
            label.setStyleSheet(f"color: {self.font_color}; background: transparent;")
            label.setAlignment(Qt.AlignCenter)
            text_size = self._get_text_size_vertical(self.text, self.font)
            window_width = text_size.height() + 2 * self.margin
            window_height = text_size.width() + 2 * self.margin
        else:
            # 横向显示
            label = QLabel(self.text, self.window)
            label.setFont(self.font)
            label.setStyleSheet(f"color: {self.font_color}; background: transparent;")
            label.setAlignment(Qt.AlignCenter)
            text_size = self._get_text_size_horizontal(self.text, self.font)
            window_width = text_size.width() + 2 * self.margin
            window_height = text_size.height() + 2 * self.margin
        self.label = label

        # 计算窗口位置
        x, y = 0, 0
        pos_comment = ""
        if dock_pos == "bottom":
            # 右上角贴紧底部dock
            x = dock_rect['x'] + dock_rect['width'] - window_width - self.margin
            y = dock_rect['y'] - window_height - self.margin
            pos_comment = "右上角贴紧底部dock"
        elif dock_pos == "top":
            # 右下角贴紧顶部dock
            x = dock_rect['x'] + dock_rect['width'] - window_width - self.margin
            y = dock_rect['y'] + dock_rect['height'] + self.margin
            pos_comment = "右下角贴紧顶部dock"
        elif dock_pos == "right":
            # 左下角贴紧右侧dock
            x = dock_rect['x'] - window_width - self.margin
            y = dock_rect['y'] + dock_rect['height'] - window_height - self.margin
            pos_comment = "左下角贴紧右侧dock"
        elif dock_pos == "left":
            # 右下角贴紧左侧dock
            x = dock_rect['x'] + dock_rect['width'] + self.margin
            y = dock_rect['y'] + dock_rect['height'] - window_height - self.margin
            pos_comment = "右下角贴紧左侧dock"
        else:
            # 没有dock，右下角
            x = screen_rect.width() - window_width - self.margin
            y = screen_rect.height() - window_height - self.margin
            pos_comment = "右下角贴紧屏幕"

        # 防止出界
        x = max(0, min(x, screen_rect.width() - window_width))
        y = max(0, min(y, screen_rect.height() - window_height))

        self.window.setGeometry(x, y, window_width, window_height)
        self.label.setGeometry(0, 0, window_width, window_height)

        # 打印详细信息
        print("="*40)
        print(f"屏幕rect:         {screen_rect}")
        print(f"可用空间rect:     {avail_rect}")
        print(f"Dock rect:        {dock_rect}")
        print(f"Dock位置:         {dock_pos}")
        print(f"窗口size:         {window_width}x{window_height}")
        print(f"窗口rect:         [{x}, {y}, {window_width}, {window_height}]")
        print(f"窗口相对dock:     {pos_comment}")
        print("="*40)

    def _get_text_size_horizontal(self, text: str, font: QFont) -> QSize:
        """获取横向文本的最佳显示尺寸。"""
        label = QLabel(text)
        label.setFont(font)
        return label.sizeHint()

    def _get_text_size_vertical(self, text: str, font: QFont) -> QSize:
        """
        获取竖排文本的最佳显示尺寸。
        实际为文本宽高互换。
        """
        label = QLabel(text)
        label.setFont(font)
        size = label.sizeHint()
        # 宽高互换
        return QSize(size.height(), size.width())

    @staticmethod
    def get_dock_rect_and_pos(screen, screen_rect: QRect, avail_rect: QRect) -> Tuple[Dict[str, int], Literal['top', 'bottom', 'left', 'right', 'none']]:
        """返回dock的rect和dock在屏幕的方向。"""
        dock_rect = {
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
        }
        dock_pos = "none"
        # 上
        if avail_rect.y() > 0:
            dock_rect = {
                "x": screen_rect.x(),
                "y": screen_rect.y(),
                "width": screen_rect.width(),
                "height": avail_rect.y()
            }
            dock_pos = "top"
        # 左
        elif avail_rect.x() > 0:
            dock_rect = {
                "x": screen_rect.x(),
                "y": screen_rect.y(),
                "width": avail_rect.x(),
                "height": screen_rect.height()
            }
            dock_pos = "left"
        # 右
        elif avail_rect.width() < screen_rect.width():
            dock_rect = {
                "x": avail_rect.width(),
                "y": screen_rect.y(),
                "width": screen_rect.width() - avail_rect.width(),
                "height": screen_rect.height()
            }
            dock_pos = "right"
        # 下
        elif avail_rect.height() < screen_rect.height():
            dock_rect = {
                "x": screen_rect.x(),
                "y": avail_rect.height(),
                "width": screen_rect.width(),
                "height": screen_rect.height() - avail_rect.height()
            }
            dock_pos = "bottom"
        return dock_rect, dock_pos

    def show(self) -> None:
        """显示悬浮窗。"""
        self.label.setParent(self.window)
        self.label.show()
        self.window.show()

    def run(self) -> None:
        """运行应用。"""
        sys.exit(self.app.exec())

if __name__ == "__main__":
    # 示例用法
    overlay = TransparentOverlay(
        text="Hello",
        margin=10,
        font_color="orange",
        font_size=20
    )
    overlay.show()
    overlay.run()