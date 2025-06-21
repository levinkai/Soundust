from typing import Dict
from AppKit import (
    NSWindow, NSColor, NSFont, NSTextField, NSMakeRect,
    NSBorderlessWindowMask, NSBackingStoreBuffered, NSScreen
)
import objc
from PyObjCTools import AppHelper


class MacOSOverlayWindow:
    """
    A transparent overlay window for macOS that displays text in the bottom-right corner.

    Attributes:
        window (NSWindow): The transparent overlay window.
        text_field (NSTextField): The text field displaying content.
    """

    def __init__(
        self,
        text: str = "Hello macOS!",
        width: int = 100,
        height: int = 50,
        margin: int = 10,
        font_name: str = "Helvetica",
        font_size: int = 24,
        text_color: NSColor = NSColor.whiteColor()
    ):
        """
        Initialize the overlay window.

        Args:
            text: Text to display.
            width: Window width in pixels.
            height: Window height in pixels.
            margin: Margin from screen edges in pixels.
            font_name: Name of the font to use.
            font_size: Size of the font.
            text_color: Color of the text (NSColor object).
        """
        self.text = text
        self.width = width
        self.height = height
        self.margin = margin
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color

        self.window = None
        self.text_field = None

        self._create_window()
        self._setup_text_field()
        self._position_window()

    def _create_window(self) -> None:
        """Create the transparent NSWindow."""
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(0, 0, self.width, self.height),
            NSBorderlessWindowMask,
            NSBackingStoreBuffered,
            False
        )
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setOpaque_(False)
        self.window.setLevel_(3)  # Ensure window stays on top

    def _setup_text_field(self) -> None:
        """Configure the text field with specified properties."""
        self.text_field = NSTextField.alloc().initWithFrame_(
            NSMakeRect(0, 0, self.width, self.height)
        )
        self.text_field.setStringValue_(self.text)
        self.text_field.setBezeled_(False)
        self.text_field.setDrawsBackground_(False)
        self.text_field.setEditable_(False)
        self.text_field.setFont_(NSFont.fontWithName_size_(self.font_name, self.font_size))
        self.text_field.setTextColor_(self.text_color)

        self.window.contentView().addSubview_(self.text_field)

    def _position_window(self) -> None:
        """Position the window at the bottom-right corner of the screen."""
        screen = NSScreen.mainScreen()
        screen_width = screen.frame().size.width
        screen_height = screen.frame().size.height

        x = screen_width - self.width - self.margin
        y = self.margin  # macOS coordinate system has origin at bottom-left

        self.window.setFrame_display_(NSMakeRect(x, y, self.width, self.height), True)

    def show(self) -> None:
        """Display the window."""
        self.window.makeKeyAndOrderFront_(None)

    def run(self) -> None:
        """Start the application event loop."""
        AppHelper.runConsoleEventLoop()

    @staticmethod
    def get_dock_rect() -> Dict[str, float]:
        """
        Get the rectangle occupied by the macOS Dock.

        Returns:
            Dictionary with keys 'x', 'y', 'width', 'height' representing
            the Dock's position and dimensions.
        """
        screen = NSScreen.mainScreen()
        screen_frame = screen.frame()
        visible_frame = screen.visibleFrame()

        dock_rect = {
            "x": 0.0,
            "y": 0.0,
            "width": 0.0,
            "height": 0.0
        }

        # Dock at bottom
        if visible_frame.origin.y > 0:
            dock_rect.update({
                "width": screen_frame.size.width,
                "height": visible_frame.origin.y
            })
        # Dock at left
        elif visible_frame.origin.x > 0:
            dock_rect.update({
                "width": visible_frame.origin.x,
                "height": screen_frame.size.height
            })
        # Dock at right
        elif visible_frame.size.width < screen_frame.size.width:
            dock_rect.update({
                "x": visible_frame.size.width,
                "width": screen_frame.size.width - visible_frame.size.width,
                "height": screen_frame.size.height
            })

        return dock_rect


if __name__ == "__main__":
    # Example usage
    overlay = MacOSOverlayWindow(
        text="Custom Overlay Text",
        width=150,
        height=60,
        margin=20,
        font_name="Menlo",
        font_size=18,
        #text_color=NSColor.greenColor()
    )
    overlay.show()
    
    # Print dock information
    print("Dock position:", overlay.get_dock_rect())
    
    overlay.run()