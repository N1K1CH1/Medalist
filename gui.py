from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QRadioButton, 
                               QButtonGroup, QMessageBox, QScrollArea, QGridLayout, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QIcon, QPixmap

from logic import load_questions, get_options, calculate_profile, user_data, save_to_excel, delete_last_record, resource_path
import os
import sys
import subprocess

def get_age_declension(age: int) -> str:
    age = int(age)
    if 11 <= age % 100 <= 14:
        return "лет"
    
    last_digit = age % 10
    if last_digit == 1:
        return "год"
    elif 2 <= last_digit <= 4:
        return "года"
    else:
        return "лет"
    
class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(parent.rect())
        
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        image_path = resource_path("start.png")
        pixmap = QPixmap(image_path)
        
        if pixmap.isNull():
            label = QLabel("Загрузка...")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 16))
            layout.addWidget(label)
        else:
            scaled_pixmap = pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            lbl = QLabel()
            lbl.setPixmap(scaled_pixmap)
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        for child in self.findChildren(QLabel):
            if not child.text():
                pixmap = child.pixmap()
                if pixmap:
                    scaled_pixmap = pixmap.scaled(
                        self.size(), 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                    child.setPixmap(scaled_pixmap)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.questions = load_questions()
        self.options = get_options()
        
        if not self.questions:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить вопросы.")
            return

        self.current_index = 0
        self.user_answers = [None] * len(self.questions)

        self.active_shortcuts = []
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        self.init_style()
        self.show_splash_then_start()

        icon_path = resource_path("Icon.ico")
        self.setWindowIcon(QIcon(icon_path))

    def init_style(self):
        self.setWindowTitle("Эмоциональное тестирование")
        self.setGeometry(150, 150, 900, 600)

        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setStyleSheet("""
            QMainWindow { background-color: #000000; }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #005ecb; }
            QPushButton:disabled { background-color: #ccc; }
            QRadioButton { font-size: 16px; padding: 10px; }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #007AFF; }
            QRadioButton {
                spacing: 10px; /* Отступ между кружком и текстом */
                font-size: 16px;
                padding: 8px 0;
            }
        """)

    def show_splash_then_start(self):
        self.splash = SplashScreen(self)
        self.splash.show()
        
        self.splash_timer = QTimer(self)
        self.splash_timer.setSingleShot(True)
        self.splash_timer.timeout.connect(self.fade_out_splash)
        self.splash_timer.start(5000)

    def fade_out_splash(self):
        self.animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.animation.finished.connect(self.on_splash_finished)
        self.animation.start()

    def on_splash_finished(self):
        self.splash.hide()
        self.splash.deleteLater()
        self.show_start_screen()

    def add_footer(self):
        footer_label = QLabel("© 2026 Nakasima Studio. Приложение разработано на основе тестов, созданными D. Gill и T. Deeter, D. Conroy, J. Nicholls, R. Vallerand. ") #добавить ссылку на файл
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #aaa; font-size: 12px; margin-top: 20px;")
        self.main_layout.addWidget(footer_label)

    def clear_shortcuts(self):
        for shortcut in self.active_shortcuts:
            shortcut.setEnabled(False)
            shortcut.deleteLater()
        self.active_shortcuts.clear()

    def show_greeting(self):
        return

    def show_start_screen(self):
        self.clear_shortcuts()
        self.clear_layout(self.main_layout)
        
        self.setWindowTitle("Эмоциональное тестирование")
        title = QLabel("Добро пожаловать!")
        title.setStyleSheet("color: #fff; font-size: 24px; font-weigth: 700")
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)
        
        subtitle = QLabel("Пожалуйста, введите свои данные перед началом теста.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        self.main_layout.addWidget(subtitle)
        
        spacer1 = QWidget()
        spacer1.setFixedHeight(30)
        self.main_layout.addWidget(spacer1)

        name_layout = QHBoxLayout()
        name_label = QLabel("ФИО:")
        name_label.setStyleSheet("color: #fff; font-size: 14px; font-weight: 700")
        name_label.setFixedWidth(100)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Иванов Иван")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        self.main_layout.addLayout(name_layout)

        age_layout = QHBoxLayout()
        age_label = QLabel("Возраст:")
        age_label.setStyleSheet("color: #fff; font-size: 14px; font-weight: 700")
        age_label.setFixedWidth(100)
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Например, 25")
        self.age_input.setMaxLength(3)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        self.main_layout.addLayout(age_layout)
        
        spacer2 = QWidget()
        spacer2.setFixedHeight(40)
        self.main_layout.addWidget(spacer2)

        btn_layout1 = QHBoxLayout()

        hol1_btn = QPushButton("")
        hol1_btn.setStyleSheet("""
            QPushButton { background-color: #000000; }
            QPushButton:hover { background-color: #000000; }
            QPushButton:pressed { background-color: #000000; }
        """)

        des_btn = QPushButton("Описание к программе")
        des_btn.clicked.connect(self.open_describe_file)

        hol2_btn = QPushButton("")
        hol2_btn.setStyleSheet("""
            QPushButton { background-color: #000000; }
            QPushButton:hover { background-color: #000000; }
            QPushButton:pressed { background-color: #000000; }
        """)

        btn_layout1.addWidget(hol1_btn)
        btn_layout1.addWidget(des_btn)
        btn_layout1.addWidget(hol2_btn)

        self.main_layout.addLayout(btn_layout1)

        btn_layout = QHBoxLayout()

        history_btn = QPushButton("Открыть историю результатов")
        history_btn.clicked.connect(self.open_history_file)
        history_btn.setStyleSheet("""
            QPushButton { background-color: #34C759; }
            QPushButton:hover { background-color: #2DA84E; }
            QPushButton:pressed { background-color: #248F42; }
        """)

        start_btn = QPushButton("Начать тестирование")
        start_btn.clicked.connect(self.start_test)

        history_shortcut = QShortcut(QKeySequence(Qt.Key_Tab), self)
        history_shortcut.activated.connect(self.open_history_file)
        self.active_shortcuts.append(history_shortcut)

        start_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        start_shortcut.activated.connect(self.start_test)
        self.active_shortcuts.append(start_shortcut)

        btn_layout.addWidget(history_btn)
        btn_layout.addWidget(start_btn)

        self.main_layout.addLayout(btn_layout)

        self.add_footer()

    def open_describe_file(self):
        filename = "Описание.txt"
        filepath = resource_path(filename)
        
        if os.path.exists(filepath):
            try:
                if sys.platform == "win32":
                    os.startfile(filepath)
                elif sys.platform == "darwin":
                    subprocess.call(['open', filepath])
                else:
                    subprocess.call(['xdg-open', filepath])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Файл не найден", f"Файл '{filename}' не найден внутри приложения.")

    def open_history_file(self):
            filename = "results.xlsx"
            
            if sys.platform == "win32":
                app_data = os.getenv("APPDATA")
                dir_name = "TestApp"
            elif sys.platform == "darwin": # macOS
                app_data = os.path.expanduser("~/Library/Application Support")
                dir_name = "TestApp"
            else:
                app_data = os.path.expanduser("~/.local/share")
                dir_name = "testapp"
                
            folder_path = os.path.join(app_data, dir_name)
            filepath = os.path.join(folder_path, filename)

            if not os.path.exists(filepath):
                QMessageBox.information(self, "Информация", "История тестов пока пуста. Пройдите тест, чтобы сохранить результат.")
                return

            try:
                if sys.platform == "win32":
                    os.startfile(filepath)
                elif sys.platform == "darwin":
                    subprocess.call(['open', filepath])
                else:
                    subprocess.call(['xdg-open', filepath])
                    
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}\n\nПуть к файлу:\n{filepath}")                    

    def start_test(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, введите ваше ФИО.")
            return
        if not age or not age.isdigit():
            QMessageBox.warning(self, "Внимание", "Пожалуйста, введите корректный возраст (число).")
            return
            
        user_data.name = name
        user_data.age = age
        
        self.current_index = 0
        self.user_answers = [None] * len(self.questions)
        self.show_question()

    def show_question(self):
        self.clear_shortcuts()
        self.clear_layout(self.main_layout)

        if self.current_index >= len(self.questions):
            self.show_results()
            return

        q_data = self.questions[self.current_index]

        progress_label = QLabel(f"Вопрос {self.current_index + 1} из {len(self.questions)}")
        progress_label.setStyleSheet("color: #888; font-size: 14px;")
        self.main_layout.addWidget(progress_label)

        age_val = user_data.age
        age_word = get_age_declension(age_val)

        person_label = QLabel(f"Испытуемый: {user_data.name}, возраст: {age_val} {age_word}")
        person_label.setStyleSheet("color: #888; font-size: 14px;")
        self.main_layout.addWidget(person_label)

        question_text = QLabel(q_data["question"])
        question_text.setStyleSheet("color: #fffff1; font-size: 20px; font-weight: 700")
        question_text.setWordWrap(True)
        self.main_layout.addWidget(question_text)
        
        spacer = QWidget()
        spacer.setFixedHeight(30)
        self.main_layout.addWidget(spacer)

        self.button_group = QButtonGroup()
        for idx, opt in enumerate(self.options):
            rb_layout = QHBoxLayout()
            rb = QRadioButton(opt["text"])
            rb.setStyleSheet("color: white; font-size: 18px; font-weight: 600") 
            self.button_group.addButton(rb, idx)
            
            rb_layout.addWidget(rb)
            rb_layout.addStretch()
            
            self.main_layout.addLayout(rb_layout)
            
            shortcut = QShortcut(QKeySequence(str(idx + 1)), self)
            shortcut.activated.connect(lambda i=idx: self.select_option(i))
            self.active_shortcuts.append(shortcut)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()

        back_btn = QPushButton("Назад")
        back_btn.setObjectName("backBtn")
        back_btn.clicked.connect(self.prev_question)
        if self.current_index == 0:
            back_btn.setEnabled(False)
            
        btn_layout.addWidget(back_btn)
        
        
        next_btn = QPushButton("Далее")
        next_btn.clicked.connect(self.next_question)
        btn_layout.addWidget(next_btn)
        
        self.main_layout.addWidget(btn_container)

        if self.current_index > 0:
            back_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
            back_shortcut.activated.connect(self.prev_question)
            self.active_shortcuts.append(back_shortcut)

        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self.next_question)
        self.active_shortcuts.append(enter_shortcut)

        self.add_footer()


    def select_option(self, index):
        buttons = self.button_group.buttons()
        if 0 <= index < len(buttons):
            buttons[index].setChecked(True)

    def next_question(self):
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Внимание", "Выберите вариант ответа.")
            return
        
        self.user_answers[self.current_index] = selected_id
        self.current_index += 1
        self.show_question()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.user_answers[self.current_index] = None
            self.show_question()

    def show_results(self):
        self.clear_shortcuts()
        self.clear_layout(self.main_layout)
        
        data = calculate_profile(self.questions, self.user_answers)
        profile = data["scales"]

        header_layout = QVBoxLayout()
        title = QLabel(f"Результаты: {user_data.name}")
        title.setStyleSheet("color: #fff; font-size: 24px; font-weight: 700")
        title.setAlignment(Qt.AlignCenter)

        age_val = user_data.age
        age_word = get_age_declension(age_val)
        
        age_label = QLabel(f"Имя: {user_data.name}, возраст: {age_val} {age_word}")
        age_label.setAlignment(Qt.AlignCenter)
        age_label.setStyleSheet("color: #666; font-size: 14px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(age_label)
        self.main_layout.addLayout(header_layout)
        
        separator = QWidget()
        separator.setFixedHeight(20)
        self.main_layout.addWidget(separator)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none;")
        
        table_widget = self.create_clean_table(profile, data["total_score"], data["total_max"])
        scroll.setWidget(table_widget)
        
        self.main_layout.addWidget(scroll)

        btn_layout1 = QHBoxLayout()

        hole1_btn = QPushButton("")
        hole1_btn.setStyleSheet("""
            QPushButton { background-color: #000000; }
            QPushButton:hover { background-color: #000000; }
            QPushButton:pressed { background-color: #000000; }
        """)

        file_btn = QPushButton("Пояснение к результатам")
        file_btn.clicked.connect(self.show_recommendations)

        hole2_btn = QPushButton("")
        hole2_btn.setStyleSheet("""
            QPushButton { background-color: #000000; }
            QPushButton:hover { background-color: #000000; }
            QPushButton:pressed { background-color: #000000; }
        """)

        btn_layout1.addWidget(hole1_btn)
        btn_layout1.addWidget(file_btn)
        btn_layout1.addWidget(hole2_btn)

        self.main_layout.addLayout(btn_layout1)

        btn_layout = QHBoxLayout()

        delete_btn = QPushButton("Удалить последнюю запись")
        delete_btn.setToolTip("Удаляет последнюю строку из файла results.xlsx")
        delete_btn.clicked.connect(self.delete_last_from_excel)
        delete_btn.setStyleSheet("""
            QPushButton { background-color: #FF3B30; }
            QPushButton:hover { background-color: #D63228; }
            QPushButton:pressed { background-color: #BF2C22; }
            QPushButton { margin-top: 20px; }
        """)

        save_btn = QPushButton("Записать результат в таблицу")
        save_btn.clicked.connect(lambda: self.save_results(data))
        save_btn.setStyleSheet("""
            QPushButton { background-color: #34C759; }
            QPushButton:hover { background-color: #2DA84E; }
            QPushButton:pressed { background-color: #248F42; }
            QPushButton { margin-top: 20px; }
        """)

        restart_btn = QPushButton("Пройти заново")
        restart_btn.clicked.connect(self.show_start_screen)
        restart_btn.setStyleSheet("margin-top: 20px;") 

        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(restart_btn)

        self.main_layout.addLayout(btn_layout)

        restart_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        restart_shortcut.activated.connect(self.show_start_screen)
        self.active_shortcuts.append(restart_shortcut)

        save_shortcut = QShortcut(QKeySequence(Qt.Key_Tab), self)
        save_shortcut.activated.connect(self.open_history_file)
        self.active_shortcuts.append(save_shortcut)

        self.add_footer()

    def show_recommendations(self):
        filename = "Характеристика.txt"
        filepath = resource_path(filename)
        
        if os.path.exists(filepath):
            try:
                if sys.platform == "win32":
                    os.startfile(filepath)
                elif sys.platform == "darwin":
                    subprocess.call(['open', filepath])
                else:
                    subprocess.call(['xdg-open', filepath])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Файл не найден", f"Файл '{filename}' не найден внутри приложения.")
    
    def delete_last_from_excel(self):
        success, message = delete_last_record()
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.warning(self, "Внимание", message)

    def save_results(self, data):
        try:
            filepath = save_to_excel(user_data.name, user_data.age, data)
            QMessageBox.information(self, "Успех", f"Результаты сохранены в файл:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def create_clean_table(self, profile, total_score, total_max):
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(20)
        grid.setContentsMargins(30, 30, 30, 30)

        grid.addWidget(QLabel(""), 0, 0)
        
        for col_idx, item in enumerate(profile):
            header_label = QLabel(item["scale_name"])
            header_label.setFont(QFont("Helvetica", 11, QFont.Bold))
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setWordWrap(True)
            header_label.setStyleSheet("background-color: #f5f5f7; padding: 8px; border-radius: 6px; color: #555;")
            grid.addWidget(header_label, 0, col_idx + 1)

        total_header = QLabel("ВСЕГО")
        total_header.setFont(QFont("Helvetica", 11, QFont.Bold))
        total_header.setAlignment(Qt.AlignCenter)
        total_header.setStyleSheet("background-color: #e8e8ed; padding: 8px; border-radius: 6px; color: #333;")
        grid.addWidget(total_header, 0, 6)

        row_label_1 = QLabel("Баллы")
        row_label_1.setFont(QFont("Helvetica", 12, QFont.Bold))
        row_label_1.setStyleSheet("color: #888;")
        grid.addWidget(row_label_1, 1, 0, alignment=Qt.AlignVCenter)

        for col_idx, item in enumerate(profile):
            val_label = QLabel(f"{item['score']}/{item['max']}")
            val_label.setFont(QFont("Helvetica", 14, QFont.Bold))
            val_label.setAlignment(Qt.AlignCenter)
            color = "#34C759" if item['percentage'] >= 70 else ("#FF9500" if item['percentage'] >= 40 else "#FF3B30")
            val_label.setStyleSheet(f"color: {color};")
            grid.addWidget(val_label, 1, col_idx + 1)

        total_val = QLabel(f"{total_score}/{total_max}")
        total_val.setFont(QFont("Helvetica", 14, QFont.Bold))
        total_val.setAlignment(Qt.AlignCenter)
        total_val.setStyleSheet("color: #007AFF;")
        grid.addWidget(total_val, 1, 6)

        row_label_2 = QLabel("Оценка")
        row_label_2.setFont(QFont("Helvetica", 12, QFont.Bold))
        row_label_2.setStyleSheet("color: #888;")
        grid.addWidget(row_label_2, 2, 0, alignment=Qt.AlignVCenter | Qt.AlignTop)

        for col_idx, item in enumerate(profile):
            char_label = QLabel(item["recommendation"])
            char_label.setAlignment(Qt.AlignCenter)
            char_label.setWordWrap(True)
            char_label.setFont(QFont("Helvetica", 10))
            char_label.setStyleSheet("color: #555; line-height: 140%;")
            char_label.setMinimumWidth(100)
            grid.addWidget(char_label, 2, col_idx + 1, alignment=Qt.AlignTop)

        for i in range(7):
            grid.setColumnStretch(i, 1)

        return container
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self.clear_layout(sub_layout)