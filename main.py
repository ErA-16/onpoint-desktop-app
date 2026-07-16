from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QLabel, QStackedWidget, QVBoxLayout, QWidget, QDialog, QLineEdit, QPushButton, QVBoxLayout as QVBoxLayoutDialog
from login_interface import build_login_page
from signup_interface import build_signup_page
from database import create_users_table, create_posts_table, username_exists, add_user, seed_default_user, get_stored_password, hash_password, get_full_name, add_post, get_posts_by_user, update_password, update_photo_path, get_photo_path
from toast import Toast
from welcome_interface import build_welcome_page
from PySide6.QtGui import QColor


app = QApplication([])

create_users_table()
create_posts_table()
seed_default_user()

current_user = [None]


def on_photo_change(file_path):
    if current_user[0]:
        update_photo_path(current_user[0], file_path)


login_page, signup_link, username_input, user_password, login_button = build_login_page()
signup_page, login_link, name_input, signup_username_input, signup_password, confirm_password, check_box, signup_button = build_signup_page()
welcome_page, welcome_label, username_label, logout_button, collapse_sidebar, post_input, post_button, posts_layout, profile_name_label, username_value_label, fullname_value_label, change_password_button, set_avatar_from_path = build_welcome_page(on_photo_change)


def create_post_card(content, timestamp):
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

    time_label = QLabel(timestamp)
    time_label.setStyleSheet("font-size: 10px; color: #999; border: none;")

    card_layout = QVBoxLayout()
    card_layout.setContentsMargins(14, 12, 14, 12)
    card_layout.setSpacing(4)
    card_layout.addWidget(content_label)
    card_layout.addWidget(time_label)
    card.setLayout(card_layout)

    return card


def check_login():
    entered_username = username_input.text().lower()
    entered_password = user_password.text()

    stored_hash = get_stored_password(entered_username)

    if stored_hash is None:
        Toast("Username does not exist.", main_window)
    elif hash_password(entered_password) == stored_hash:
        full_name = get_full_name(entered_username)
        first_name = full_name.split()[0]

        current_user[0] = entered_username
        welcome_label.setText(f"Welcome, {first_name}!")
        username_label.setText(entered_username)
        profile_name_label.setText(full_name)
        username_value_label.setText(entered_username)
        fullname_value_label.setText(full_name)
        set_avatar_from_path(get_photo_path(entered_username))
        collapse_sidebar()
        refresh_posts()
        main_window.setCurrentIndex(2)
    else:
        Toast("Wrong username or password.", main_window)


def check_signup():
    if not check_box.isChecked():
        Toast("You must agree to the terms.", main_window)
    else:
        full_name = name_input.text().strip().capitalize()

        if full_name == "":
            Toast("Full name cannot be empty.", main_window)
        elif not all(char.isalpha() or char.isspace() for char in full_name):
            Toast("Full name can only contain letters and spaces.", main_window)
        else:
            username = signup_username_input.text().lower()

            if not username.isalnum():
                Toast("Username can only contain letters and numbers.", main_window)
            elif username_exists(username):
                Toast("Username already exists.", main_window)
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
                    add_user(username, full_name, pw)
                    Toast("Account created successfully!", main_window)
                    main_window.setCurrentIndex(0)


def handle_post():
    content = post_input.toPlainText().strip()

    if content == "":
        Toast("Write something before posting.", main_window)
    else:
        add_post(current_user[0], content)
        post_input.clear()
        refresh_posts()


def refresh_posts():
    while posts_layout.count() > 1:
        item = posts_layout.takeAt(0)
        item.widget().deleteLater()

    posts = get_posts_by_user(current_user[0])

    for content, timestamp in posts:
        card = create_post_card(content, timestamp)
        posts_layout.insertWidget(posts_layout.count() - 1, card)


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

main_window.show()
app.exec()