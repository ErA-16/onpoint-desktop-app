from PySide6.QtCore import Qt, QSize, QStringListModel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTextEdit, QFileDialog, QScrollArea, QLineEdit, QCompleter
from resource_path import get_resource_path
import requests



def load_pixmap_from_source(path):
    pixmap = QPixmap()
    if path.startswith("http"):
        try:
            response = requests.get(path, timeout=10)
            pixmap.loadFromData(response.content)
        except Exception:
            pixmap.load(get_resource_path("images/user_icon.png"))
    else:
        pixmap.load(path)
    return pixmap



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
    source = load_pixmap_from_source(path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

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
    discover_button = build_sidebar_button("Discover")
    messages_button = build_sidebar_button("Messages")
    about_button = build_sidebar_button("About")
    profile_button = build_sidebar_button("Profile")
    contact_button = build_sidebar_button("Contact")
    logout_button = build_sidebar_button("Logout")
    logout_button.setCheckable(False)

    nav_widgets = [user_row, home_button, discover_button, messages_button, about_button, profile_button, contact_button, logout_button]
    nav_page_buttons = [home_button, discover_button, messages_button, about_button, profile_button, contact_button]

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

    image_preview_label = QLabel()
    image_preview_label.setStyleSheet("border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 8px;")
    image_preview_label.setVisible(False)
    image_preview_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    remove_image_button = QPushButton("Remove image")
    remove_image_button.setStyleSheet("color: #E62B2B; border: none; background: transparent; font-size: 11px; text-align: left;")
    remove_image_button.setCursor(Qt.CursorShape.PointingHandCursor)
    remove_image_button.setVisible(False)

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

    attach_image_button = QPushButton()
    attach_image_button.setIcon(QIcon(get_resource_path("images/camera_icon.png")))
    attach_image_button.setIconSize(QSize(18, 18))
    attach_image_button.setFixedSize(32, 32)
    attach_image_button.setCursor(Qt.CursorShape.PointingHandCursor)
    attach_image_button.setStyleSheet("""
        QPushButton {
            background-color: #f0f0f0;
            border: none;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
    """)

    post_button_row = QHBoxLayout()
    post_button_row.addWidget(attach_image_button)
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
    posts_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    posts_scroll_area.setStyleSheet("border: none;")

    home_layout = QVBoxLayout()
    home_layout.setContentsMargins(24, 12, 24, 24)
    home_layout.addWidget(welcome_label)
    home_layout.addWidget(welcome_subtitle)
    home_layout.addWidget(post_input)
    home_layout.addWidget(image_preview_label)
    home_layout.addWidget(remove_image_button)
    home_layout.addLayout(post_button_row)
    home_layout.addWidget(posts_scroll_area)
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
    sidebar_layout.addWidget(discover_button)
    sidebar_layout.addWidget(messages_button)
    sidebar_layout.addWidget(about_button)
    sidebar_layout.addWidget(profile_button)
    sidebar_layout.addWidget(contact_button)
    sidebar_layout.addStretch()
    sidebar_layout.addWidget(logout_button)
    sidebar.setLayout(sidebar_layout)

    discover_page = QWidget()

    discover_title = QLabel("Discover")
    discover_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1a1a1a;")

    discover_posts_container = QWidget()
    discover_posts_layout = QVBoxLayout()
    discover_posts_layout.setSpacing(10)
    discover_posts_layout.addStretch()
    discover_posts_container.setLayout(discover_posts_layout)

    discover_scroll_area = QScrollArea()
    discover_scroll_area.setWidget(discover_posts_container)
    discover_scroll_area.setWidgetResizable(True)
    discover_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    discover_scroll_area.setStyleSheet("border: none;")

    discover_layout = QVBoxLayout()
    discover_layout.setContentsMargins(24, 12, 24, 24)
    discover_layout.addWidget(discover_title)
    discover_layout.addWidget(discover_scroll_area)
    discover_page.setLayout(discover_layout)

    messages_page = QWidget()

    messages_title = QLabel("Messages")
    messages_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1a1a1a;")

    search_user_input = QLineEdit()
    search_user_input.setPlaceholderText("Search username...")
    search_user_input.setFixedHeight(40)

    completer_model = QStringListModel()
    search_completer = QCompleter()
    search_completer.setModel(completer_model)
    search_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    search_completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
    search_user_input.setCompleter(search_completer)


    search_user_button = QPushButton("Search")
    search_user_button.setFixedSize(90, 36)
    search_user_button.setCursor(Qt.CursorShape.PointingHandCursor)
    search_user_button.setStyleSheet("""
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

    search_row = QHBoxLayout()
    search_row.addWidget(search_user_input)
    search_row.addWidget(search_user_button)

    inbox_container = QWidget()
    inbox_layout = QVBoxLayout()
    inbox_layout.setSpacing(6)
    inbox_layout.addStretch()
    inbox_container.setLayout(inbox_layout)

    inbox_scroll_area = QScrollArea()
    inbox_scroll_area.setWidget(inbox_container)
    inbox_scroll_area.setWidgetResizable(True)
    inbox_scroll_area.setStyleSheet("border: none;")

    inbox_page = QWidget()
    inbox_page_layout = QVBoxLayout()
    inbox_page_layout.setContentsMargins(0, 0, 0, 0)
    inbox_page_layout.addWidget(messages_title)
    inbox_page_layout.addLayout(search_row)
    inbox_page_layout.addWidget(inbox_scroll_area)
    inbox_page.setLayout(inbox_page_layout)

    back_to_inbox_button = QPushButton("← Back")
    back_to_inbox_button.setCursor(Qt.CursorShape.PointingHandCursor)
    back_to_inbox_button.setStyleSheet("border: none; background: transparent; color: #E62B2B; font-weight: bold; text-align: left;")

    chat_header_avatar = QLabel()
    chat_header_avatar.setFixedSize(36, 36)

    chat_header_username = QLabel("username")
    chat_header_username.setStyleSheet("font-size: 15px; font-weight: bold;")

    chat_header_row = QHBoxLayout()
    chat_header_row.addWidget(chat_header_avatar)
    chat_header_row.addWidget(chat_header_username)
    chat_header_row.addStretch()

    chat_container = QWidget()
    chat_layout = QVBoxLayout()
    chat_layout.setSpacing(8)
    chat_layout.addStretch()
    chat_container.setLayout(chat_layout)

    chat_scroll_area = QScrollArea()
    chat_scroll_area.setWidget(chat_container)
    chat_scroll_area.setWidgetResizable(True)
    chat_scroll_area.setStyleSheet("border: none;")

    message_input = QLineEdit()
    message_input.setPlaceholderText("Type a message...")
    message_input.setFixedHeight(40)

    send_message_button = QPushButton("Send")
    send_message_button.setFixedSize(80, 36)
    send_message_button.setCursor(Qt.CursorShape.PointingHandCursor)
    send_message_button.setStyleSheet("""
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

    send_row = QHBoxLayout()
    send_row.addWidget(message_input)
    send_row.addWidget(send_message_button)

    chat_view_page = QWidget()
    chat_view_layout = QVBoxLayout()
    chat_view_layout.setContentsMargins(0, 0, 0, 0)
    chat_view_layout.addWidget(back_to_inbox_button)
    chat_view_layout.addLayout(chat_header_row)
    chat_view_layout.addWidget(chat_scroll_area)
    chat_view_layout.addLayout(send_row)
    chat_view_page.setLayout(chat_view_layout)

    messages_stack = QStackedWidget()
    messages_stack.addWidget(inbox_page)
    messages_stack.addWidget(chat_view_page)
    messages_stack.setCurrentIndex(0)

    messages_layout = QVBoxLayout()
    messages_layout.setContentsMargins(24, 12, 24, 24)
    messages_layout.addWidget(messages_stack)
    messages_page.setLayout(messages_layout)

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

    change_username_button = QPushButton("Change Username")
    change_username_button.setCursor(Qt.CursorShape.PointingHandCursor)
    change_username_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: #E62B2B;
            border: none;
            font-weight: bold;
            font-size: 13px;
            text-align: left;
            margin-top: 6px;
        }
        QPushButton:hover {
            text-decoration: underline;
        }
    """)

    info_card_layout = QVBoxLayout()
    info_card_layout.setContentsMargins(16, 14, 16, 14)
    info_card_layout.addWidget(username_row_label)
    info_card_layout.addWidget(username_value_label)
    info_card_layout.addWidget(change_username_button)
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

    contact_title = QLabel("Contact Info")
    contact_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a1a1a;")

    contact_subtitle = QLabel("Keep this up to date so people can reach you.")
    contact_subtitle.setStyleSheet("font-size: 13px; color: #999; margin-bottom: 8px;")

    contact_email_input = QLineEdit()
    contact_email_input.setPlaceholderText("Email")
    contact_email_input.setFixedHeight(40)

    contact_phone_input = QLineEdit()
    contact_phone_input.setPlaceholderText("Phone number")
    contact_phone_input.setFixedHeight(40)

    save_contact_button = QPushButton("Save")
    save_contact_button.setFixedSize(100, 36)
    save_contact_button.setCursor(Qt.CursorShape.PointingHandCursor)
    save_contact_button.setStyleSheet("""
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

    contact_layout = QVBoxLayout()
    contact_layout.setContentsMargins(24, 12, 24, 24)
    contact_layout.setSpacing(10)
    contact_layout.addWidget(contact_title)
    contact_layout.addWidget(contact_subtitle)
    contact_layout.addWidget(contact_email_input)
    contact_layout.addWidget(contact_phone_input)
    contact_layout.addWidget(save_contact_button)
    contact_layout.addStretch()
    contact_page.setLayout(contact_layout)

    content_stack = QStackedWidget()
    content_stack.addWidget(home_page)
    content_stack.addWidget(discover_page)
    content_stack.addWidget(messages_page)
    content_stack.addWidget(about_page)
    content_stack.addWidget(profile_page)
    content_stack.addWidget(contact_page)

    def set_active_button(clicked_button):
        for button in nav_page_buttons:
            button.setChecked(button is clicked_button)

    
    def reset_to_home():
        content_stack.setCurrentIndex(0)
        set_active_button(home_button)

    home_button.clicked.connect(lambda: content_stack.setCurrentIndex(0))
    discover_button.clicked.connect(lambda: content_stack.setCurrentIndex(1))
    messages_button.clicked.connect(lambda: content_stack.setCurrentIndex(2))
    about_button.clicked.connect(lambda: content_stack.setCurrentIndex(3))
    profile_button.clicked.connect(lambda: content_stack.setCurrentIndex(4))
    contact_button.clicked.connect(lambda: content_stack.setCurrentIndex(5))

    home_button.clicked.connect(lambda: set_active_button(home_button))
    discover_button.clicked.connect(lambda: set_active_button(discover_button))
    messages_button.clicked.connect(lambda: set_active_button(messages_button))
    about_button.clicked.connect(lambda: set_active_button(about_button))
    profile_button.clicked.connect(lambda: set_active_button(profile_button))
    contact_button.clicked.connect(lambda: set_active_button(contact_button))

    home_button.setChecked(True)

    page_layout = QHBoxLayout()
    page_layout.setContentsMargins(0, 0, 0, 0)
    page_layout.addWidget(sidebar)
    page_layout.addWidget(content_stack)
    welcome_page.setLayout(page_layout)

    return welcome_page, welcome_label, username_label, logout_button, collapse_sidebar, post_input, post_button, posts_layout, profile_name_label, username_value_label, fullname_value_label, change_password_button, set_avatar_from_path, contact_email_input, contact_phone_input, save_contact_button, change_username_button, attach_image_button, discover_posts_layout, image_preview_label, remove_image_button, search_user_input, search_user_button, chat_layout, message_input, send_message_button, inbox_layout, back_to_inbox_button, chat_header_avatar, chat_header_username, messages_stack, reset_to_home, completer_model, search_completer