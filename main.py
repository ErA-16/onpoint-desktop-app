from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPixmap, QPainter, QPainterPath, QFontMetrics
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QLabel, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QDialog, QLineEdit, QPushButton, QFileDialog, QVBoxLayout as QVBoxLayoutDialog
from login_interface import build_login_page
from signup_interface import build_signup_page
from database import username_exists, add_user, seed_default_user, get_stored_password, hash_password, get_full_name, add_post, get_posts_by_user, update_password, update_photo_path, get_photo_path, update_contact_info, get_contact_info, update_username, upload_post_image, get_all_posts, send_message, get_conversation, get_conversations_list, search_usernames
from toast import Toast
from welcome_interface import build_welcome_page, load_pixmap_from_source
from network_status import is_online
from resource_path import get_resource_path


app = QApplication([])

try:
    if is_online():
        seed_default_user()
except Exception:
    pass

current_user = [None]
selected_post_image = [None]
current_chat_partner = [None]


def on_photo_change(file_path):
    if current_user[0]:
        update_photo_path(current_user[0], file_path)


login_page, signup_link, username_input, user_password, login_button = build_login_page()
signup_page, login_link, name_input, signup_username_input, email_input, signup_password, confirm_password, check_box, signup_button = build_signup_page()
welcome_page, welcome_label, username_label, logout_button, collapse_sidebar, post_input, post_button, posts_layout, profile_name_label, username_value_label, fullname_value_label, change_password_button, set_avatar_from_path, contact_email_input, contact_phone_input, save_contact_button, change_username_button, attach_image_button, discover_posts_layout, image_preview_label, remove_image_button, search_user_input, search_user_button, chat_layout, message_input, send_message_button, inbox_layout, back_to_inbox_button, chat_header_avatar, chat_header_username, messages_stack, reset_to_home, completer_model, search_completer = build_welcome_page(on_photo_change)


def make_circular_avatar(username, size):
    photo_path = get_photo_path(username)
    source_path = photo_path if photo_path else get_resource_path("images/user_icon.png")

    source = load_pixmap_from_source(source_path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

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


def create_post_card(content, timestamp, image_url=None, author=None):
    card = QWidget()
    card.setStyleSheet("""
        QWidget {
            background-color: white;
            border-radius: 10px;
            border-left: 4px solid #E62B2B;
        }
    """)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(2)
    shadow.setColor(QColor(0, 0, 0, 30))
    card.setGraphicsEffect(shadow)

    content_label = QLabel(content)
    content_label.setWordWrap(True)
    content_label.setStyleSheet("font-size: 13px; color: #222; border: none;")

    post_image_label = None
    if image_url:
        import requests

        response = requests.get(image_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        post_image_label = QLabel()
        post_image_label.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
        post_image_label.setStyleSheet("border: none; margin-top: 6px;")

    time_label = QLabel(timestamp)
    time_label.setStyleSheet("font-size: 10px; color: #999; border: none;")

    card_layout = QVBoxLayout()
    card_layout.setContentsMargins(14, 12, 14, 12)
    card_layout.setSpacing(4)

    if author:
        author_label = QLabel(f"@{author}")
        author_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #E62B2B; border: none;")
        card_layout.addWidget(author_label)

    card_layout.addWidget(content_label)
    if post_image_label:
        card_layout.addWidget(post_image_label)
    card_layout.addWidget(time_label)
    card.setLayout(card_layout)

    return card


def check_login():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    login_button.setText("Logging in...")
    login_button.setEnabled(False)
    QApplication.processEvents()

    entered_username = username_input.text().lower()
    entered_password = user_password.text()

    try:
        stored_hash = get_stored_password(entered_username)
    except Exception:
        Toast("Something went wrong connecting to the server. Please try again.", main_window)
        login_button.setText("Login")
        login_button.setEnabled(True)
        return

    if stored_hash is None:
        Toast("Username does not exist.", main_window)
        login_button.setText("Login")
        login_button.setEnabled(True)
    elif hash_password(entered_password) == stored_hash:
        try:
            full_name = get_full_name(entered_username)
            first_name = full_name.split()[0]

            current_user[0] = entered_username
            welcome_label.setText(f"Welcome, {first_name}!")
            username_label.setText(entered_username)
            profile_name_label.setText(full_name)
            username_value_label.setText(entered_username)
            fullname_value_label.setText(full_name)
            set_avatar_from_path(get_photo_path(entered_username))
            saved_email, saved_phone = get_contact_info(entered_username)
            contact_email_input.setText(saved_email or "")
            contact_phone_input.setText(saved_phone or "")
            reset_to_home()
            collapse_sidebar()
            refresh_posts()
            refresh_discover()
            refresh_inbox()
            main_window.setCurrentIndex(2)
        except Exception:
            Toast("Something went wrong loading your account. Please try again.", main_window)
        login_button.setText("Login")
        login_button.setEnabled(True)
    else:
        Toast("Wrong username or password.", main_window)
        login_button.setText("Login")
        login_button.setEnabled(True)


def check_signup():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    signup_button.setText("Signing up...")
    signup_button.setEnabled(False)
    QApplication.processEvents()

    if not check_box.isChecked():
        Toast("You must agree to the terms.", main_window)
        signup_button.setText("Sign up")
        signup_button.setEnabled(True)
    else:
        full_name = name_input.text().strip().capitalize()

        if full_name == "":
            Toast("Full name cannot be empty.", main_window)
            signup_button.setText("Sign up")
            signup_button.setEnabled(True)
        elif not all(char.isalpha() or char.isspace() for char in full_name):
            Toast("Full name can only contain letters and spaces.", main_window)
            signup_button.setText("Sign up")
            signup_button.setEnabled(True)
        else:
            username = signup_username_input.text().lower()

            if not username.isalnum():
                Toast("Username can only contain letters and numbers.", main_window)
                signup_button.setText("Sign up")
                signup_button.setEnabled(True)
            elif username_exists(username):
                Toast("Username already exists.", main_window)
                signup_button.setText("Sign up")
                signup_button.setEnabled(True)
            else:
                email = email_input.text().strip()

                if "@" not in email or "." not in email:
                    Toast("Please enter a valid email.", main_window)
                    signup_button.setText("Sign up")
                    signup_button.setEnabled(True)
                else:
                    pw = signup_password.text()
                    confirm = confirm_password.text()

                    has_upper = any(char.isupper() for char in pw)
                    has_lower = any(char.islower() for char in pw)
                    has_special = any(not char.isalnum() for char in pw)

                    if len(pw) < 8:
                        Toast("Password must be at least 8 characters", main_window)
                    elif pw != confirm:
                        Toast("Password do not match", main_window)
                    elif not has_upper:
                        Toast("Password must contain an uppercase letter.", main_window)
                    elif not has_lower:
                        Toast("Password must contain a lowercase letter.", main_window)
                    elif not has_special:
                        Toast("Password must contain a special character.", main_window)
                    else:
                        add_user(username, full_name, pw, email)
                        Toast("Account created successfully!", main_window)
                        main_window.setCurrentIndex(0)

                    signup_button.setText("Sign up")
                    signup_button.setEnabled(True)


def choose_post_image():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    file_path, _ = QFileDialog.getOpenFileName(welcome_page, "Choose an image", "", "Images (*.png *.jpg *.jpeg)")
    if file_path:
        selected_post_image[0] = file_path

        pixmap = QPixmap(file_path).scaledToWidth(340, Qt.TransformationMode.SmoothTransformation)
        image_preview_label.setPixmap(pixmap)
        image_preview_label.setVisible(True)
        remove_image_button.setVisible(True)


def remove_selected_image():
    selected_post_image[0] = None
    image_preview_label.clear()
    image_preview_label.setVisible(False)
    remove_image_button.setVisible(False)

remove_image_button.clicked.connect(remove_selected_image)


def handle_post():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    content = post_input.toPlainText().strip()

    if content == "":
        Toast("Write something before posting.", main_window)
    else:
        image_url = None
        if selected_post_image[0]:
            image_url = upload_post_image(current_user[0], selected_post_image[0])

        add_post(current_user[0], content, image_url)
        post_input.clear()
        selected_post_image[0] = None
        image_preview_label.clear()
        image_preview_label.setVisible(False)
        remove_image_button.setVisible(False)
        refresh_posts()
        refresh_discover()


def refresh_posts():
    while posts_layout.count() > 1:
        item = posts_layout.takeAt(0)
        item.widget().deleteLater()

    posts = get_posts_by_user(current_user[0])

    for content, timestamp, image_url in posts:
        card = create_post_card(content, timestamp, image_url)
        posts_layout.insertWidget(posts_layout.count() - 1, card)


def refresh_discover():
    while discover_posts_layout.count() > 1:
        item = discover_posts_layout.takeAt(0)
        item.widget().deleteLater()

    posts = get_all_posts()

    for username, content, timestamp, image_url in posts:
        card = create_post_card(content, timestamp, image_url, author=username)
        discover_posts_layout.insertWidget(discover_posts_layout.count() - 1, card)


def open_change_password_dialog():
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Change Password")
    dialog.setFixedSize(300, 220)

    current_pw_input = QLineEdit()
    current_pw_input.setPlaceholderText("Current password")
    current_pw_input.setEchoMode(QLineEdit.EchoMode.Password)

    new_pw_input = QLineEdit()
    new_pw_input.setPlaceholderText("New password")
    new_pw_input.setEchoMode(QLineEdit.EchoMode.Password)

    confirm_pw_input = QLineEdit()
    confirm_pw_input.setPlaceholderText("Confirm new password")
    confirm_pw_input.setEchoMode(QLineEdit.EchoMode.Password)

    save_button = QPushButton("Save")
    save_button.setStyleSheet("background-color: #E62B2B; color: white; border-radius: 6px; padding: 8px;")

    def save_new_password():
        if not is_online():
            Toast("No internet connection.", main_window)
            return

        current_pw = current_pw_input.text()
        new_pw = new_pw_input.text()
        confirm_pw = confirm_pw_input.text()

        stored_hash = get_stored_password(current_user[0])

        if hash_password(current_pw) != stored_hash:
            Toast("Current password is incorrect.", main_window)
        elif len(new_pw) < 8:
            Toast("New password must be at least 8 characters.", main_window)
        elif new_pw != confirm_pw:
            Toast("New passwords do not match.", main_window)
        elif not any(c.isupper() for c in new_pw):
            Toast("New password must contain an uppercase letter.", main_window)
        elif not any(c.islower() for c in new_pw):
            Toast("New password must contain a lowercase letter.", main_window)
        elif not any(not c.isalnum() for c in new_pw):
            Toast("New password must contain a special character.", main_window)
        else:
            update_password(current_user[0], new_pw)
            Toast("Password updated successfully!", main_window)
            dialog.close()

    save_button.clicked.connect(save_new_password)

    layout = QVBoxLayoutDialog()
    layout.addWidget(current_pw_input)
    layout.addWidget(new_pw_input)
    layout.addWidget(confirm_pw_input)
    layout.addWidget(save_button)
    dialog.setLayout(layout)

    dialog.exec()


def open_change_username_dialog():
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Change Username")
    dialog.setFixedSize(300, 150)

    new_username_input = QLineEdit()
    new_username_input.setPlaceholderText("New username")

    save_button = QPushButton("Save")
    save_button.setStyleSheet("background-color: #E62B2B; color: white; border-radius: 6px; padding: 8px;")

    def save_new_username():
        if not is_online():
            Toast("No internet connection.", main_window)
            return

        new_username = new_username_input.text().strip().lower()

        if not new_username.isalnum():
            Toast("Username can only contain letters and numbers.", main_window)
        elif username_exists(new_username):
            Toast("That username is already taken.", main_window)
        else:
            old_username = current_user[0]
            update_username(old_username, new_username)
            current_user[0] = new_username

            username_label.setText(new_username)
            username_value_label.setText(new_username)

            Toast("Username updated successfully!", main_window)
            dialog.close()

    save_button.clicked.connect(save_new_username)

    layout = QVBoxLayoutDialog()
    layout.addWidget(new_username_input)
    layout.addWidget(save_button)
    dialog.setLayout(layout)

    dialog.exec()


def save_contact():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    email = contact_email_input.text().strip()
    phone = contact_phone_input.text().strip()

    if "@" not in email or "." not in email:
        Toast("Please enter a valid email.", main_window)
    elif not phone.isdigit() or len(phone) != 11:
        Toast("Phone number must be 11 digits.", main_window)
    else:
        update_contact_info(current_user[0], email, phone)
        Toast("Contact info updated!", main_window)


def create_message_bubble(sender, content):
    bubble_row = QHBoxLayout()

    bubble = QLabel(content)
    bubble.setWordWrap(True)
    bubble.setMaximumWidth(240)

    text_width = QFontMetrics(bubble.font()).horizontalAdvance(content) + 28
    bubble.setMinimumWidth(min(text_width, 240))

    if sender == current_user[0]:
        bubble.setStyleSheet("""
            QLabel {
                background-color: #E62B2B;
                color: white;
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)
        bubble_row.addStretch()
        bubble_row.addWidget(bubble)
    else:
        bubble.setStyleSheet("""
            QLabel {
                background-color: #e2e2e2;
                border: 1px solid #d0d0d0;
                color: #222;
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)
        bubble_row.addWidget(bubble)
        bubble_row.addStretch()

    return bubble_row


def refresh_chat():
    while chat_layout.count() > 1:
        item = chat_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            while item.layout().count():
                sub_item = item.layout().takeAt(0)
                if sub_item.widget():
                    sub_item.widget().deleteLater()

    messages = get_conversation(current_user[0], current_chat_partner[0])

    for sender, content, timestamp in messages:
        bubble_row = create_message_bubble(sender, content)
        chat_layout.insertLayout(chat_layout.count() - 1, bubble_row)


def open_chat(username):
    current_chat_partner[0] = username
    chat_header_username.setText(f"@{username}")
    chat_header_avatar.setPixmap(make_circular_avatar(username, 36))
    messages_stack.setCurrentIndex(1)
    refresh_chat()


def go_back_to_inbox():
    messages_stack.setCurrentIndex(0)
    refresh_inbox()

back_to_inbox_button.clicked.connect(go_back_to_inbox)


def create_inbox_row(other_username, last_message):
    row = QPushButton()
    row.setCursor(Qt.CursorShape.PointingHandCursor)
    row.setMinimumHeight(64)
    row.setStyleSheet("""
        QPushButton {
            background-color: #fafafa;
            border: none;
            border-radius: 8px;
            text-align: left;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
    """)

    avatar = QLabel()
    avatar.setFixedSize(40, 40)
    avatar.setPixmap(make_circular_avatar(other_username, 40))

    username_label_row = QLabel(f"@{other_username}")
    username_label_row.setStyleSheet("font-weight: bold; font-size: 13px; border: none; background: transparent;")

    preview_text = last_message if len(last_message) <= 40 else last_message[:40] + "..."
    preview_label = QLabel(preview_text)
    preview_label.setStyleSheet("font-size: 11px; color: #888; border: none; background: transparent;")

    text_col = QVBoxLayout()
    text_col.setSpacing(2)
    text_col.addWidget(username_label_row)
    text_col.addWidget(preview_label)

    row_layout = QHBoxLayout()
    row_layout.setContentsMargins(10, 8, 10, 8)
    row_layout.addWidget(avatar)
    row_layout.addLayout(text_col)
    row_layout.addStretch()
    row.setLayout(row_layout)

    row.clicked.connect(lambda: open_chat(other_username))

    return row


def refresh_inbox():
    while inbox_layout.count() > 1:
        item = inbox_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

    conversations = get_conversations_list(current_user[0])

    for other_username, (last_message, timestamp) in conversations.items():
        row = create_inbox_row(other_username, last_message)
        inbox_layout.insertWidget(inbox_layout.count() - 1, row)


def search_user():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    target_username = search_user_input.text().strip().lower().lstrip("@")

    if target_username == current_user[0]:
        Toast("You can't message yourself.", main_window)
    elif not username_exists(target_username):
        Toast(f"User '{target_username}' not found.", main_window)
    else:
        search_user_input.clear()
        open_chat(target_username)

search_user_button.clicked.connect(search_user)


search_debounce_timer = QTimer()
search_debounce_timer.setSingleShot(True)

def run_username_search():
    term = search_user_input.text().strip().lower()
    if term == "":
        completer_model.setStringList([])
        return

    if not is_online():
        return

    results = search_usernames(term, current_user[0])
    completer_model.setStringList([f"@{u}" for u in results])

def on_search_text_changed():
    search_debounce_timer.stop()
    search_debounce_timer.start(300)

search_debounce_timer.timeout.connect(run_username_search)
search_user_input.textChanged.connect(on_search_text_changed)


def open_chat_from_search(selected_text):
    target_username = selected_text.lstrip("@")
    search_user_input.clear()
    open_chat(target_username)

search_completer.activated.connect(open_chat_from_search)


def handle_send_message():
    if not is_online():
        Toast("No internet connection.", main_window)
        return

    if not current_chat_partner[0]:
        Toast("Search for a user to message first.", main_window)
        return

    content = message_input.text().strip()

    if content == "":
        Toast("Type something first.", main_window)
    else:
        send_message(current_user[0], current_chat_partner[0], content)
        message_input.clear()
        refresh_chat()
        refresh_inbox()

send_message_button.clicked.connect(handle_send_message)


def poll_active_chat():
    if messages_stack.currentIndex() == 1 and current_chat_partner[0]:
        refresh_chat()

chat_poll_timer = QTimer()
chat_poll_timer.timeout.connect(poll_active_chat)
chat_poll_timer.start(3000)


def logout():
    username_input.clear()
    user_password.clear()
    main_window.setCurrentIndex(0)


main_window = QStackedWidget()
main_window.setWindowTitle("OnPoint")
main_window.setFixedSize(420, 600)

main_window.addWidget(login_page)
main_window.addWidget(signup_page)
main_window.addWidget(welcome_page)
main_window.setCurrentIndex(0)

signup_link.linkActivated.connect(lambda: main_window.setCurrentIndex(1))
login_link.linkActivated.connect(lambda: main_window.setCurrentIndex(0))
login_button.clicked.connect(check_login)
signup_button.clicked.connect(check_signup)
logout_button.clicked.connect(logout)
post_button.clicked.connect(handle_post)
change_password_button.clicked.connect(open_change_password_dialog)
save_contact_button.clicked.connect(save_contact)
change_username_button.clicked.connect(open_change_username_dialog)
attach_image_button.clicked.connect(choose_post_image)

main_window.show()
app.exec()