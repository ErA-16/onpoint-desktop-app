from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
from PySide6.QtGui import QPixmap
from resource_path import get_resource_path


def build_login_page():
    login_page= QWidget()

    logo_label = QLabel()
    logo_img = QPixmap(get_resource_path("images/logo.png"))
    if not logo_img.isNull():
        logo_label.setPixmap(logo_img.scaledToHeight(180, Qt.TransformationMode.SmoothTransformation))


    login_header = QLabel("Login to your Account")
    login_header.setStyleSheet("font-size: 24px; font-weight: bold;")


    username_input = QLineEdit()
    username_input.setPlaceholderText("Username")
    username_input.setFixedHeight(40)

    user_password = QLineEdit()
    user_password.setPlaceholderText("Password")
    user_password.setFixedHeight(40)
    user_password.setEchoMode(QLineEdit.EchoMode.Password)


    remember_me = QCheckBox("Remember me")

    forgot_password = QLabel("<a href='#'>Forgot Password?</a>")
    forgot_password.setTextFormat(Qt.TextFormat.RichText)
    forgot_password.setCursor(Qt.CursorShape.PointingHandCursor)

    remember_row = QHBoxLayout()
    remember_row.addWidget(remember_me)
    remember_row.addStretch()
    remember_row.addWidget(forgot_password)


    login_button = QPushButton("Login")
    login_button.setFixedHeight(48)
    login_button.setCursor(Qt.CursorShape.PointingHandCursor)
    login_button.setStyleSheet("""
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


    text = QLabel("Don't have an account?")

    create_account = QLabel("<a href='#'>Sign up</a>")
    create_account.setTextFormat(Qt.TextFormat.RichText)
    create_account.setCursor(Qt.CursorShape.PointingHandCursor)

    signup_row = QHBoxLayout()
    signup_row.addStretch()
    signup_row.addWidget(text)
    signup_row.addWidget(create_account)
    signup_row.addStretch()


    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(24, 24, 24, 24) 
    main_layout.setSpacing(14)

    main_layout.addWidget(logo_label)
    main_layout.addSpacing(-50)
    main_layout.addWidget(login_header)
    main_layout.addWidget(username_input)
    main_layout.addWidget(user_password)
    main_layout.addLayout(remember_row)
    main_layout.addWidget(login_button)
    main_layout.addLayout(signup_row)
    main_layout.addStretch()

    login_page.setLayout(main_layout)
    return login_page, create_account, username_input, user_password, login_button