from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class Toast(QWidget):
    def __init__(self, message, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            background-color: #2f2f2f;
            border-radius: 8px;
        """)

        message_label = QLabel(message)
        message_label.setStyleSheet("color: white; font-size: 13px;")

        close_button = QPushButton("✕")
        close_button.setFixedSize(20, 20)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 12px;
            }
        """)
        close_button.clicked.connect(self.close)

        layout = QHBoxLayout()
        layout.addWidget(message_label)
        layout.addWidget(close_button)
        self.setLayout(layout)

        self.adjustSize()
        self.move(parent.width() - self.width() - 20, 20)
        self.show()

        QTimer.singleShot(3000, self.close)