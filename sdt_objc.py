from AppKit import NSWindow, NSColor, NSFont, NSTextField, NSMakeRect
from AppKit import NSBorderlessWindowMask, NSBackingStoreBuffered, NSScreen
import objc

# 获取主屏幕的完整尺寸（包括 Dock 的区域）
screen = NSScreen.mainScreen()
screen_width = screen.frame().size.width
screen_height = screen.frame().size.height

# 窗口位置（直接定位到屏幕右下角）
window_width = 100
window_height = 50
margin = 10  # 距离边缘的边距

x = screen_width - window_width - margin
y = margin  # 从屏幕底部向上计算（坐标系原点在左下角）

window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    NSMakeRect(x, y, window_width, window_height),
    NSBorderlessWindowMask,
    NSBackingStoreBuffered,
    False
)
window.setBackgroundColor_(NSColor.clearColor())
window.setOpaque_(False)
window.setLevel_(3)  # 确保窗口在最上层

# 添加文字
text = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, window_width, window_height))
text.setStringValue_("Hello macOS!")
text.setBezeled_(False)
text.setDrawsBackground_(False)
text.setEditable_(False)
text.setFont_(NSFont.fontWithName_size_("Helvetica", 24))
text.setTextColor_(NSColor.whiteColor())

window.contentView().addSubview_(text)
window.makeKeyAndOrderFront_(None)

from PyObjCTools import AppHelper
AppHelper.runConsoleEventLoop()