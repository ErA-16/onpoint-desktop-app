from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel
from resource_path import get_resource_path

def build_signup_page():
    signup_page = QWidget()


    logo_label = QLabel()
    logo_img = QPixmap(get_resource_path("images/logo.png"))
    if not logo_img.isNull():
        logo_label.setPixmap(logo_img.scaledToHeight(180, Qt.TransformationMode.SmoothTransformation))
        
    heading_text = QLabel("Create your account")
    heading_text.setStyleSheet("font-size: 24px; font-weight: bold;")

    sub_heading = QLabel("Sign up to get started")

    heading = QVBoxLayout()
    heading.setSpacing(2)
    heading.addWidget(heading_text)
    heading.addWidget(sub_heading)

    name_input = QLineEdit()
    name_input.setPlaceholderText("Full name")
    name_input.setFixedHeight(40)

    username_input = QLineEdit()
    username_input.setPlaceholderText("Username")
    username_input.setFixedHeight(40)

    # email_input = QLineEdit()
    # email_input.setPlaceholderText("Email")
    # email_input.setFixedHeight(40)

    password = QLineEdit()
    password.setPlaceholderText("Password")
    password.setFixedHeight(40)
    password.setEchoMode(QLineEdit.EchoMode.Password)

    confirm_password = QLineEdit()
    confirm_password.setPlaceholderText("Confirm Password")
    confirm_password.setFixedHeight(40)
    confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

    fields_column = QVBoxLayout()
    fields_column.setSpacing(10)
    fields_column.addWidget(name_input)
    fields_column.addWidget(username_input)
    # fields_column.addWidget(email_input)
    fields_column.addWidget(password)
    fields_column.addWidget(confirm_password)

    check_box = QCheckBox("I agree to the terms")

    signup_button = QPushButton("Sign up")
    signup_button.setFixedHeight(48)
    signup_button.setCursor(Qt.CursorShape.PointingHandCursor)
    signup_button.setStyleSheet("""
        QPushButton {
            background-color: #FF3131;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #E62B2B;
        }
    """)

    footer_text = QLabel("Already have an account?")

    footer_link = QLabel("<a href='#'>Login</a>")
    footer_link.setTextFormat(Qt.TextFormat.RichText)
    footer_link.setCursor(Qt.CursorShape.PointingHandCursor)

    footer = QHBoxLayout()
    footer.addStretch()
    footer.addWidget(footer_text)
    footer.addWidget(footer_link)
    footer.addStretch()

    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(24, 8, 24, 24)
    main_layout.setSpacing(14)

    main_layout.addWidget(logo_label)
    main_layout.addSpacing(-60)
    main_layout.addLayout(heading)
    main_layout.addLayout(fields_column)
    main_layout.addWidget(check_box)
    main_layout.addWidget(signup_button)
    main_layout.addLayout(footer)
    main_layout.addStretch()

    signup_page.setLayout(main_layout)
    return signup_page, footer_link, name_input, username_input, password, confirm_password, check_box, signup_button