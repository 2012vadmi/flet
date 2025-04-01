import flet as ft
import json
import uuid
import os
from typing import List, Dict, Optional


class TestSystem:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.initialize_data()
        self.show_role_selection()

    def setup_page(self):
        self.page.title = "Test System"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 800
        self.page.window_height = 900

    def initialize_data(self):
        """Инициализация данных и папок"""
        if not os.path.exists("media"):
            os.makedirs("media")

        self.tests = self.load_tests()
        self.current_test = None
        self.current_question_index = 0
        self.user_score = 0
        self.admin_questions = []
        self.admin_media = None

        # Инициализация FilePicker
        self.file_picker = ft.FilePicker(on_result=self.handle_media_upload)
        self.page.overlay.append(self.file_picker)

    def load_tests(self) -> Dict:
        """Загрузка тестов из файла"""
        try:
            with open("tests.json", "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_tests(self):
        """Сохранение тестов в файл"""
        with open("tests.json", "w", encoding='utf-8') as f:
            json.dump(self.tests, f, ensure_ascii=False, indent=4)

    def show_role_selection(self):
        """Экран выбора роли"""
        self.page.clean()

        self.page.add(
            ft.Column(
                [
                    ft.Text("Выберите вашу роль:", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Player",
                                on_click=lambda e: self.show_player_interface(),
                                width=200,
                                height=50
                            ),
                            ft.ElevatedButton(
                                "Administrator",
                                on_click=lambda e: self.show_admin_interface(),
                                width=200,
                                height=50
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40
            )
        )

    # Player Interface
    def show_player_interface(self):
        """Интерфейс игрока"""
        self.page.clean()

        self.test_code_field = ft.TextField(
            label="Введите код теста",
            width=400,
            height=50
        )

        self.page.add(
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: self.show_role_selection(),
                        icon_size=30
                    ),
                    ft.Text("Прохождение теста", size=24, weight=ft.FontWeight.BOLD),
                    self.test_code_field,
                    ft.ElevatedButton(
                        "Начать тест",
                        on_click=lambda e: self.start_test(self.test_code_field.value),
                        width=200,
                        height=50
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

    def start_test(self, test_code: str):
        """Начало теста"""
        if not test_code:
            self.show_snackbar("Введите код теста!")
            return

        if test_code not in self.tests:
            self.show_snackbar("Тест с таким кодом не найден!")
            return

        self.current_test = self.tests[test_code]
        self.current_question_index = 0
        self.user_score = 0
        self.show_question()

    def show_question(self):
        """Отображение вопроса"""
        question_data = self.current_test["questions"][self.current_question_index]

        self.page.clean()

        # Прогресс теста
        progress = ft.Text(
            f"Вопрос {self.current_question_index + 1}/{len(self.current_test['questions'])}",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        # Текст вопроса
        question_text = ft.Text(
            question_data["question"],
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Медиа контент
        media_widget = self.create_media_widget(question_data.get("media"))

        # Варианты ответов
        options = []
        for i, option in enumerate(question_data["options"]):
            options.append(
                ft.ElevatedButton(
                    option,
                    on_click=lambda e, idx=i: self.check_answer(idx),
                    width=400,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            )

        self.page.add(
            ft.Column(
                [
                    progress,
                    question_text,
                    media_widget,
                    *options
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

    def check_answer(self, option_index: int):
        """Проверка ответа и переход к следующему вопросу"""
        question_data = self.current_test["questions"][self.current_question_index]

        if option_index == question_data["correct"]:
            self.user_score += question_data.get("points", 1)

        self.current_question_index += 1

        if self.current_question_index < len(self.current_test["questions"]):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        """Отображение результатов теста"""
        total_points = sum(q.get("points", 1) for q in self.current_test["questions"])

        self.page.clean()

        self.page.add(
            ft.Column(
                [
                    ft.Text("Результаты теста", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"Вы набрали {self.user_score} из {total_points} баллов!",
                        size=20,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"Успешность: {self.user_score / total_points * 100:.1f}%",
                        size=18,
                        color=ft.colors.GREEN if self.user_score / total_points >= 0.7 else ft.colors.RED
                    ),
                    ft.ElevatedButton(
                        "Вернуться к выбору роли",
                        on_click=lambda e: self.show_role_selection(),
                        width=200,
                        height=50
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30
            )
        )

    # Admin Interface
    def show_admin_interface(self):
        """Интерфейс администратора"""
        self.page.clean()
        self.admin_questions = []
        self.admin_media = None

        # Поля для ввода вопроса
        self.question_field = ft.TextField(
            label="Текст вопроса",
            multiline=True,
            min_lines=2,
            max_lines=5,
            width=600
        )

        # Поля для вариантов ответа
        self.option_fields = [
            ft.TextField(
                label=f"Вариант ответа {i + 1}",
                width=500,
                on_change=self.validate_options
            )
            for i in range(4)
        ]

        # Поле для баллов
        self.points_field = ft.TextField(
            label="Баллы за вопрос",
            value="1",
            width=150,
            input_filter=ft.NumbersOnlyInputFilter()
        )

        # Выбор правильного ответа
        self.correct_option = ft.Dropdown(
            label="Правильный вариант",
            options=[ft.dropdown.Option(str(i + 1)) for i in range(4)],
            width=150,
            on_change=self.validate_correct_option
        )

        # Кнопки
        buttons = ft.Row(
            [
                ft.ElevatedButton(
                    "Добавить медиа",
                    icon=ft.icons.ADD_PHOTO_ALTERNATE,
                    on_click=lambda _: self.file_picker.pick_files(
                        allow_multiple=False,
                        allowed_extensions=["jpg", "jpeg", "png", "gif", "mp4"]
                    ),
                    width=200
                ),
                ft.ElevatedButton(
                    "Добавить вопрос",
                    icon=ft.icons.ADD,
                    on_click=self.add_question_handler,
                    width=200,
                    disabled=True
                ),
                ft.ElevatedButton(
                    "Завершить тест",
                    icon=ft.icons.DONE,
                    on_click=lambda e: self.finish_test(),
                    width=200,
                    disabled=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Список добавленных вопросов
        self.questions_list = ft.ListView(expand=True)
        self.update_questions_list()

        # Сборка интерфейса
        self.page.add(
            ft.Column(
                [
                    ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: self.show_role_selection(),
                        icon_size=30
                    ),
                    ft.Text("Создание теста", size=24, weight=ft.FontWeight.BOLD),
                    self.question_field,
                    *self.option_fields,
                    ft.Row(
                        [
                            self.points_field,
                            self.correct_option
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=50
                    ),
                    buttons,
                    ft.Divider(),
                    ft.Text("Добавленные вопросы:", weight=ft.FontWeight.BOLD),
                    self.questions_list
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            )
        )

        # Состояние кнопок
        self.add_question_btn = buttons.controls[1]
        self.finish_test_btn = buttons.controls[2]

    def validate_options(self, e):
        """Проверка заполнения вариантов ответа"""
        filled_options = sum(1 for field in self.option_fields if field.value)
        self.add_question_btn.disabled = filled_options < 2 or not self.question_field.value
        self.page.update()

    def validate_correct_option(self, e):
        """Проверка выбора правильного варианта"""
        if self.correct_option.value:
            idx = int(self.correct_option.value) - 1
            if not self.option_fields[idx].value:
                self.show_snackbar("Выбранный вариант не заполнен!")
                self.correct_option.value = None
        self.page.update()

    def add_question_handler(self, e):
        """Обработчик добавления вопроса"""
        question_text = self.question_field.value.strip()
        options = [field.value.strip() for field in self.option_fields if field.value.strip()]
        correct_index = int(self.correct_option.value) - 1 if self.correct_option.value else None

        try:
            points = max(1, int(self.points_field.value))
        except ValueError:
            points = 1

        # Валидация
        if not question_text:
            self.show_snackbar("Введите текст вопроса!")
            return

        if len(options) < 2:
            self.show_snackbar("Должно быть хотя бы 2 варианта ответа!")
            return

        if correct_index is None or correct_index >= len(options):
            self.show_snackbar("Выберите правильный вариант!")
            return

        # Создание вопроса
        question_data = {
            "question": question_text,
            "options": options,
            "correct": correct_index,
            "points": points
        }

        if self.admin_media:
            question_data["media"] = self.admin_media
            self.admin_media = None

        self.admin_questions.append(question_data)
        self.update_questions_list()
        self.clear_question_fields()
        self.show_snackbar("Вопрос добавлен!")

        # Активируем кнопку завершения теста
        self.finish_test_btn.disabled = False
        self.page.update()

    def clear_question_fields(self):
        """Очистка полей после добавления вопроса"""
        self.question_field.value = ""
        for field in self.option_fields:
            field.value = ""
        self.points_field.value = "1"
        self.correct_option.value = None
        self.add_question_btn.disabled = True
        self.page.update()

    def update_questions_list(self):
        """Обновление списка добавленных вопросов"""
        self.questions_list.controls = []

        for i, q in enumerate(self.admin_questions):
            media_info = ""
            if "media" in q:
                media_type = "Изображение" if q["media"]["type"] == "image" else "Видео"
                media_info = f" ({media_type})"

            self.questions_list.controls.append(
                ft.ListTile(
                    leading=ft.Text(f"{i + 1}."),
                    title=ft.Text(q["question"], max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    subtitle=ft.Text(
                        f"Баллы: {q['points']} | " +
                        f"Правильный: {q['options'][q['correct']]}" +
                        media_info
                    ),
                    trailing=ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e, idx=i: self.remove_question(idx),
                        tooltip="Удалить вопрос"
                    )
                )
            )
        self.page.update()

    def remove_question(self, index: int):
        """Удаление вопроса"""
        if 0 <= index < len(self.admin_questions):
            # Удаление связанных медиафайлов
            if "media" in self.admin_questions[index]:
                media_path = self.admin_questions[index]["media"]["path"]
                if os.path.exists(media_path):
                    os.remove(media_path)

            self.admin_questions.pop(index)
            self.update_questions_list()
            self.show_snackbar("Вопрос удален!")

            # Деактивируем кнопку завершения, если вопросов нет
            if not self.admin_questions:
                self.finish_test_btn.disabled = True
                self.page.update()

    def handle_media_upload(self, e: ft.FilePickerResultEvent):
        """Обработка загрузки медиафайлов"""
        if not e.files:
            return

        file = e.files[0]
        ext = file.name.split(".")[-1].lower()
        media_type = "image" if ext in ["jpg", "jpeg", "png", "gif"] else "video"

        # Сохранение файла
        new_filename = f"media/{uuid.uuid4()}.{ext}"
        os.rename(file.path, new_filename)

        self.admin_media = {
            "type": media_type,
            "path": new_filename
        }

        self.show_snackbar(f"Медиафайл добавлен: {file.name}")

    def finish_test(self):
        """Завершение создания теста"""
        test_code = str(uuid.uuid4())[:8]
        self.tests[test_code] = {
            "questions": self.admin_questions
        }
        self.save_tests()

        self.page.clean()

        self.page.add(
            ft.Column(
                [
                    ft.Text("Тест успешно создан!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Код теста: {test_code}", size=20),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Копировать код",
                                icon=ft.icons.COPY,
                                on_click=lambda e: self.page.set_clipboard(test_code),
                                width=200
                            ),
                            ft.ElevatedButton(
                                "Создать новый тест",
                                icon=ft.icons.ADD,
                                on_click=lambda e: self.show_admin_interface(),
                                width=200
                            ),
                            ft.ElevatedButton(
                                "В главное меню",
                                icon=ft.icons.HOME,
                                on_click=lambda e: self.show_role_selection(),
                                width=200
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40
            )
        )

    def create_media_widget(self, media_info: Optional[Dict]) -> ft.Control:
        """Создание виджета для медиа"""
        if not media_info:
            return ft.Container(height=0)

        media_type = media_info["type"]
        path = media_info["path"]

        if media_type == "image":
            return ft.Image(
                src=path,
                width=400,
                height=300,
                fit=ft.ImageFit.CONTAIN,
                border_radius=ft.border_radius.all(10)
            )
        elif media_type == "video":
            return ft.Video(
                path,
                width=400,
                height=300,
                autoplay=False,
                controls=True,
                border_radius=ft.border_radius.all(10)
            )
        return ft.Container(height=0)

    def show_snackbar(self, message: str):
        """Показать уведомление"""
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            behavior=ft.SnackBarBehavior.FLOATING
        )
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    TestSystem(page)


if __name__ == "__main__":
    ft.app(target=main)