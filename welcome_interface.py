from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTextEdit, QFileDialog, QScrollArea
from resource_path import get_resource_path


def build_sidebar_button(text):
    button = QPushButton(text)
    button.setFixedHeight(40)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    button.setCheckable(True)
    button.setStyleSheet("""
        QPushButton {
            color: white;
            background-color: transparent;
            border: none;
            text-align: left;
            padding-left: 12px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #FF3131;
        }
        QPushButton:checked {
            background-color: #B71C1C;
            border-left: 3px solid white;
            font-weight: bold;
        }
    """)
    return button


def make_circular_pixmap(path, size):
    source = QPixmap(path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

    circular = QPixmap(size, size)
    circular.fill(Qt.GlobalColor.transparent)

    painter = QPainter(circular)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    clip_path = QPainterPath()
    clip_path.addEllipse(0, 0, size, size)
    painter.setClipPath(clip_path)

    painter.drawPixmap(0, 0, source)
    painter.end()

    return circular


def build_welcome_page(on_photo_change=None):
    welcome_page = QWidget()

    sidebar = QWidget()
    sidebar.setStyleSheet("background-color: #E62B2B;")
    sidebar.setFixedWidth(160)

    toggle_button = QPushButton()
    toggle_button.setIcon(QIcon(get_resource_path("images/hamburger.png")))
    toggle_button.setIconSize(QSize(20, 20))
    toggle_button.setFixedSize(40, 40)
    toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
    toggle_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    toggle_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: #FF3131;
        }
    """)

    sidebar_avatar = QLabel()
    sidebar_avatar.setFixedSize(36, 36)
    sidebar_avatar.setPixmap(make_circular_pixmap(get_resource_path("images/user_icon.png"), 36))

    username_label = QLabel("username")
    username_label.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")

    user_row = QWidget()
    user_row_layout = QHBoxLayout()
    user_row_layout.setContentsMargins(4, 8, 4, 12)
    user_row_layout.setSpacing(10)
    user_row_layout.addWidget(sidebar_avatar)
    user_row_layout.addWidget(username_label)
    user_row_layout.addStretch()
    user_row.setLayout(user_row_layout)

    home_button = build_sidebar_button("Home")
    about_button = build_sidebar_button("About")
    profile_button = build_sidebar_button("Profile")
    contact_button = build_sidebar_button("Contact")
    logout_button = build_sidebar_button("Logout")
    logout_button.setCheckable(False)

    nav_widgets = [user_row, home_button, about_button, profile_button, contact_button, logout_button]
    nav_page_buttons = [home_button, about_button, profile_button, contact_button]

    home_page = QWidget()

    welcome_label = QLabel("Welcome!")
    welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a1a1a;")

    welcome_subtitle = QLabel("What's on your mind today?")
    welcome_subtitle.setStyleSheet("font-size: 13px; color: #999; margin-bottom: 8px;")

    post_input = QTextEdit()
    post_input.setPlaceholderText("Write something...")
    post_input.setFixedHeight(70)
    post_input.setStyleSheet("""
        QTextEdit {
            border: 1.5px solid #e0e0e0;
            border-radius: 10px;
            padding: 10px;
            font-size: 13px;
            background-color: #fafafa;
        }
        QTextEdit:focus {
            border: 1.5px solid #E62B2B;
            background-color: white;
        }
    """)

    post_button = QPushButton("Post")
    post_button.setFixedSize(80, 32)
    post_button.setCursor(Qt.CursorShape.PointingHandCursor)
    post_button.setStyleSheet("""
        QPushButton {
            background-color: #E62B2B;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #FF3131;
        }
    """)

    post_button_row = QHBoxLayout()
    post_button_row.addStretch()
    post_button_row.addWidget(post_button)

    posts_container = QWidget()
    posts_layout = QVBoxLayout()
    posts_layout.setSpacing(10)
    posts_layout.addStretch()
    posts_container.setLayout(posts_layout)

    posts_scroll_area = QScrollArea()
    posts_scroll_area.setWidget(posts_container)
    posts_scroll_area.setWidgetResizable(True)
    posts_scroll_area.setStyleSheet("border: none;")

    home_layout = QVBoxLayout()
    home_layout.setContentsMargins(24, 12, 24, 24)
    home_layout.addWidget(welcome_label)
    home_layout.addWidget(welcome_subtitle)
    home_layout.addWidget(post_input)
    home_layout.addLayout(post_button_row)
    home_layout.addWidget(posts_scroll_area)
    home_layout.addStretch()
    home_page.setLayout(home_layout)

    sidebar_expanded = [True]

    def collapse_sidebar():
        sidebar.setFixedWidth(40)
        sidebar.setStyleSheet("background-color: transparent;")
        home_layout.setContentsMargins(12, 12, 24, 24)
        for widget in nav_widgets:
            widget.setVisible(False)
        sidebar_expanded[0] = False

    def toggle_sidebar():
        if sidebar_expanded[0]:
            collapse_sidebar()
        else:
            sidebar.setFixedWidth(160)
            sidebar.setStyleSheet("background-color: #E62B2B;")
            home_layout.setContentsMargins(24, 12, 24, 24)
            for widget in nav_widgets:
                widget.setVisible(True)
            sidebar_expanded[0] = True

    toggle_button.clicked.connect(toggle_sidebar)
    collapse_sidebar()

    sidebar_layout = QVBoxLayout()
    sidebar_layout.setContentsMargins(4, 8, 4, 8)
    sidebar_layout.addWidget(toggle_button)
    sidebar_layout.addWidget(user_row)
    sidebar_layout.addSpacing(20)
    sidebar_layout.addWidget(home_button)
    sidebar_layout.addWidget(about_button)
    sidebar_layout.addWidget(profile_button)
    sidebar_layout.addWidget(contact_button)
    sidebar_layout.addStretch()
    sidebar_layout.addWidget(logout_button)
    sidebar.setLayout(sidebar_layout)

    about_page = QWidget()

    about_title = QLabel("About This Project")
    about_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a1a1a;")

    about_text = QLabel(
        "This app was built as a personal challenge from my uncle, David a way to push "
        "myself into real desktop application development using Python and PySide6.\n\n"
        "I used AI assistance throughout the process, especially for concepts I hadn't "
        "worked with before (multi-page navigation, database integration, password hashing) "
        "it helped me move faster and understand why things work, not just copy code. "
        "Every feature here, I read, tested, and debugged myself.\n\n"
        "This is one step in becoming a better developer. There's another project coming after this one."
    )
    about_text.setWordWrap(True)
    about_text.setStyleSheet("font-size: 13px; color: #444; line-height: 150%;")

    about_layout = QVBoxLayout()
    about_layout.setContentsMargins(24, 12, 24, 24)
    about_layout.setSpacing(12)
    about_layout.addWidget(about_title)
    about_layout.addWidget(about_text)
    about_layout.addStretch()
    about_page.setLayout(about_layout)

    profile_page = QWidget()

    avatar_label = QLabel()
    avatar_label.setFixedSize(100, 100)
    avatar_label.setPixmap(make_circular_pixmap(get_resource_path("images/user_icon.png"), 100))

    profile_name_label = QLabel("Full Name")
    profile_name_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 12px;")

    info_card = QWidget()
    info_card.setStyleSheet("""
        QWidget {
            background-color: #f7f7f7;
            border-radius: 10px;
        }
    """)

    username_row_label = QLabel("Username")
    username_row_label.setStyleSheet("font-size: 11px; color: #999; border: none;")
    username_value_label = QLabel("username")
    username_value_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #222; border: none;")

    fullname_row_label = QLabel("Full Name")
    fullname_row_label.setStyleSheet("font-size: 11px; color: #999; border: none; margin-top: 10px;")
    fullname_value_label = QLabel("Full Name")
    fullname_value_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #222; border: none;")

    change_password_button = QPushButton("Change Password")
    change_password_button.setCursor(Qt.CursorShape.PointingHandCursor)
    change_password_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #E62B2B;
            border: none;
            font-weight: bold;
            font-size: 13px;
            text-align: left;
            margin-top: 14px;
        }
        QPushButton:hover {
            text-decoration: underline;
        }
    """)

    info_card_layout = QVBoxLayout()
    info_card_layout.setContentsMargins(16, 14, 16, 14)
    info_card_layout.addWidget(username_row_label)
    info_card_layout.addWidget(username_value_label)
    info_card_layout.addWidget(fullname_row_label)
    info_card_layout.addWidget(fullname_value_label)
    info_card_layout.addWidget(change_password_button)
    info_card.setLayout(info_card_layout)

    change_photo_button = QPushButton("Change photo")
    change_photo_button.setFixedSize(140, 32)

    def change_photo():
        file_path, _ = QFileDialog.getOpenFileName(profile_page, "Choose a profile photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            avatar_label.setPixmap(make_circular_pixmap(file_path, 100))
            sidebar_avatar.setPixmap(make_circular_pixmap(file_path, 36))
            if on_photo_change:
                on_photo_change(file_path)

    def set_avatar_from_path(path):
        if path:
            avatar_label.setPixmap(make_circular_pixmap(path, 100))
            sidebar_avatar.setPixmap(make_circular_pixmap(path, 36))
        else:
            avatar_label.setPixmap(make_circular_pixmap(get_resource_path("images/user_icon.png"), 100))
            sidebar_avatar.setPixmap(make_circular_pixmap(get_resource_path("images/user_icon.png"), 36))

    change_photo_button.clicked.connect(change_photo)

    profile_layout = QVBoxLayout()
    profile_layout.setContentsMargins(24, 12, 24, 24)
    profile_layout.addWidget(avatar_label)
    profile_layout.addWidget(profile_name_label)
    profile_layout.addWidget(info_card)
    profile_layout.addWidget(change_photo_button)
    profile_layout.addStretch()
    profile_page.setLayout(profile_layout)

    contact_page = QWidget()
    contact_label = QLabel("Contact")
    contact_layout = QVBoxLayout()
    contact_layout.setContentsMargins(24, 12, 24, 24)
    contact_layout.addWidget(contact_label)
    contact_layout.addStretch()
    contact_page.setLayout(contact_layout)

    content_stack = QStackedWidget()
    content_stack.addWidget(home_page)
    content_stack.addWidget(about_page)
    content_stack.addWidget(profile_page)
    content_stack.addWidget(contact_page)

    def set_active_button(clicked_button):
        for button in nav_page_buttons:
            button.setChecked(button is clicked_button)

    home_button.clicked.connect(lambda: content_stack.setCurrentIndex(0))
    about_button.clicked.connect(lambda: content_stack.setCurrentIndex(1))
    profile_button.clicked.connect(lambda: content_stack.setCurrentIndex(2))
    contact_button.clicked.connect(lambda: content_stack.setCurrentIndex(3))

    home_button.clicked.connect(lambda: set_active_button(home_button))
    about_button.clicked.connect(lambda: set_active_button(about_button))
    profile_button.clicked.connect(lambda: set_active_button(profile_button))
    contact_button.clicked.connect(lambda: set_active_button(contact_button))

    home_button.setChecked(True)

    page_layout = QHBoxLayout()
    page_layout.setContentsMargins(0, 0, 0, 0)
    page_layout.addWidget(sidebar)
    page_layout.addWidget(content_stack)
    welcome_page.setLayout(page_layout)

    return welcome_page, welcome_label, username_label, logout_button, collapse_sidebar, post_input, post_button, posts_layout, profile_name_label, username_value_label, fullname_value_label, change_password_button, set_avatar_from_path