from typing import Dict, Tuple
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QScreen
import sys


class TransparentOverlay:
    """
    A transparent overlay widget that can be positioned on the screen.

    Attributes:
        app (QApplication): The Qt application instance.
        window (QWidget): The main transparent window.
    """

    def __init__(self, text: str = "Hello PySide!", width: int = 100, height: int = 50, margin: int = 10):
        """
        Initialize the transparent overlay.

        Args:
            text: Text to display on the overlay.
            width: Width of the overlay window.
            height: Height of the overlay window.
            margin: Margin from screen edges.
        """
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.text = text
        self.width = width
        self.height = height
        self.margin = margin

        self._setup_ui()
        self._position_window()

    def _setup_ui(self) -> None:
        """Set up the transparent window UI."""
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        self.window.setStyleSheet("background: transparent;")

        self.label = QLabel(self.text, self.window)
        self.label.setStyleSheet("color: white; font-size: 24px; background: transparent;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.width, self.height)

    def _position_window(self) -> None:
        """Position the window at the bottom-right corner of the screen."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        
        x = screen_rect.width() - self.width - self.margin
        y = screen_rect.height() - self.height - self.margin
        
        self.window.setGeometry(x, y, self.width, self.height)

    @staticmethod
    def get_dock_rect() -> Dict[str, int]:
        """
        Get the rectangle occupied by the dock.

        Returns:
            A dictionary with keys 'x', 'y', 'width', 'height' representing dock position and size.
        """
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        available_rect = screen.availableGeometry()
        
        dock_rect = {
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
        }
        
        if available_rect.y() > 0:  # Dock at bottom
            dock_rect.update({
                "width": screen_rect.width(),
                "height": available_rect.y()
            })
        elif available_rect.x() > 0:  # Dock at left
            dock_rect.update({
                "width": available_rect.x(),
                "height": screen_rect.height()
            })
        elif available_rect.width() < screen_rect.width():  # Dock at right
            dock_rect.update({
                "x": available_rect.width(),
                "width": screen_rect.width() - available_rect.width(),
                "height": screen_rect.height()
            })
        
        return dock_rect

    def show(self) -> None:
        """Show the overlay window."""
        self.window.show()

    def run(self) -> None:
        """Run the application."""
        sys.exit(self.app.exec())


if __name__ == "__main__":
    # Example usage
    overlay = TransparentOverlay(
        text="Hello World!",
        width=200,
        height=60,
        margin=20
    )
    overlay.show()
    
    # Print dock information
    print("Dock position:", overlay.get_dock_rect())
    
    overlay.run()