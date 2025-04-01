import flet as ft
from datetime import datetime
import json
import os

# Константы
USERS_FILE = "users.txt"
TRAININGS_FILE = "trainings.txt"
ROLES = ["Player", "Coach", "Administration", "Owner"]


# Загрузка данных
def load_data():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(TRAININGS_FILE):
        with open(TRAININGS_FILE, "w") as f:
            json.dump([], f)

    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    with open(TRAININGS_FILE, "r") as f:
        trainings = json.load(f)
    return users, trainings


# Сохранение данных
def save_data(users, trainings):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    with open(TRAININGS_FILE, "w") as f:
        json.dump(trainings, f, indent=2)


def main(page: ft.Page):
    page.title = "Sports Training App"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # Загрузка данных
    users, trainings = load_data()
    current_user = None

    # Элементы интерфейса
    def create_text_field(label, width=300, password=False):
        return ft.TextField(
            label=label,
            width=width,
            password=password,
            border_color=ft.colors.BLUE_200,
            focused_border_color=ft.colors.BLUE_400,
        )

    login_field = create_text_field("Логин")
    password_field = create_text_field("Пароль", password=True)
    phone_field = create_text_field("Телефон")
    name_field = create_text_field("ФИО")
    role_dropdown = ft.Dropdown(
        label="Роль",
        width=300,
        options=[ft.dropdown.Option(r) for r in ROLES],
        border_color=ft.colors.BLUE_200,
    )

    # Элементы для записи на тренировку
    coach_dropdown = ft.Dropdown(label="Тренер", width=300)
    training_type = ft.Dropdown(
        label="Тип тренировки",
        width=300,
        options=[
            ft.dropdown.Option("Футбол"),
            ft.dropdown.Option("Баскетбол"),
            ft.dropdown.Option("Теннис"),
            ft.dropdown.Option("Плавание"),
        ]
    )
    date_picker = ft.TextField(label="Дата (ДД.ММ.ГГГГ)", width=300)
    time_picker = ft.Dropdown(
        label="Время",
        width=300,
        options=[ft.dropdown.Option(f"{h}:00") for h in range(8, 22)]
    )
    rating_slider = ft.Slider(min=1, max=5, divisions=4, label="Рейтинг: {value}")
    review_field = ft.TextField(label="Отзыв", multiline=True, width=300)

    # Сообщения
    error_text = ft.Text(color=ft.colors.RED, visible=False)
    success_text = ft.Text(color=ft.colors.GREEN, visible=False)

    # Обновление списка тренеров
    def update_coaches():
        coach_dropdown.options = [
            ft.dropdown.Option(u)
            for u in users
            if users[u]["role"] == "Coach"
        ]
        page.update()

    # Очистка полей
    def clear_fields():
        for field in [login_field, password_field, phone_field, name_field,
                      date_picker, review_field]:
            field.value = ""
        error_text.visible = False
        success_text.visible = False
        page.update()

    # Навигация
    def show_auth():
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Вход / Регистрация", size=24, weight=ft.FontWeight.BOLD),
                login_field,
                password_field,
                ft.Row([
                    ft.ElevatedButton(
                        "Войти",
                        on_click=auth_user,
                        style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
                    ),
                    ft.TextButton(
                        "Регистрация",
                        on_click=lambda e: show_register(e),
                        style=ft.ButtonStyle(color=ft.colors.BLUE_200)
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                error_text,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def show_register(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Регистрация", size=24, weight=ft.FontWeight.BOLD),
                login_field,
                password_field,
                ft.Row([
                    ft.Text("Показать пароль"),
                    ft.Switch(on_change=lambda e: toggle_password_visibility())
                ]),
                phone_field,
                name_field,
                role_dropdown,
                ft.ElevatedButton(
                    "Зарегистрироваться",
                    on_click=register_user,
                    style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
                ),
                ft.TextButton(
                    "Назад",
                    on_click=lambda e: show_auth(),
                    style=ft.ButtonStyle(color=ft.colors.BLUE_200)
                ),
                error_text,
                success_text,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def toggle_password_visibility():
        password_field.password = not password_field.password
        page.update()

    # Авторизация
    def auth_user(e):
        nonlocal current_user
        login = login_field.value.strip()
        password = password_field.value.strip()

        if login in users and users[login]["password"] == password:
            current_user = {
                "login": login,
                "role": users[login]["role"],
                "phone": users[login]["phone"],
                "name": users[login]["name"],
            }
            show_main_menu()
        else:
            error_text.value = "Неверный логин или пароль!"
            error_text.visible = True
        page.update()

    # Регистрация
    def register_user(e):
        login = login_field.value.strip()
        password = password_field.value.strip()
        phone = phone_field.value.strip()
        name = name_field.value.strip()
        role = role_dropdown.value

        if not all([login, password, phone, name, role]):
            error_text.value = "Заполните все поля!"
            error_text.visible = True
        elif login in users:
            error_text.value = "Логин уже занят!"
            error_text.visible = True
        else:
            users[login] = {
                "password": password,
                "phone": phone,
                "name": name,
                "role": role,
            }
            save_data(users, trainings)
            success_text.value = "Регистрация успешна! Войдите."
            success_text.visible = True
            clear_fields()
        page.update()

    # Главное меню
    def show_main_menu():
        page.clean()
        update_coaches()

        header = ft.Text(
            f"Добро пожаловать, {current_user['name']} ({current_user['role']})",
            size=20,
            weight=ft.FontWeight.BOLD
        )

        logout_btn = ft.ElevatedButton(
            "Выйти",
            on_click=lambda e: (clear_fields(), show_auth()),
            style=ft.ButtonStyle(bgcolor=ft.colors.RED_800)
        )

        if current_user["role"] == "Player":
            show_player_menu(header, logout_btn)
        elif current_user["role"] == "Coach":
            show_coach_menu(header, logout_btn)
        elif current_user["role"] == "Administration":
            show_admin_menu(header, logout_btn)
        elif current_user["role"] == "Owner":
            show_owner_menu(header, logout_btn)

    # Меню Player
    def show_player_menu(header, logout_btn):
        page.add(
            ft.Column([
                header,
                ft.ElevatedButton(
                    "Записаться на тренировку",
                    on_click=show_training_form,
                    style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
                ),
                logout_btn,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def show_training_form(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Запись на тренировку", size=24, weight=ft.FontWeight.BOLD),
                name_field,
                phone_field,
                coach_dropdown,
                training_type,
                date_picker,
                time_picker,
                rating_slider,
                review_field,
                ft.Row([
                    ft.ElevatedButton(
                        "Записаться",
                        on_click=add_training,
                        style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
                    ),
                    ft.TextButton(
                        "Назад",
                        on_click=show_main_menu,
                        style=ft.ButtonStyle(color=ft.colors.BLUE_200)
                    ),
                ]),
                error_text,
                success_text,
            ], spacing=15)
        )
        name_field.value = current_user["name"]
        phone_field.value = current_user["phone"]
        page.update()

    def add_training(e):
        required_fields = [
            name_field.value,
            phone_field.value,
            coach_dropdown.value,
            training_type.value,
            date_picker.value,
            time_picker.value
        ]

        if not all(required_fields):
            error_text.value = "Заполните все обязательные поля!"
            error_text.visible = True
        else:
            trainings.append({
                "player_name": name_field.value,
                "player_phone": phone_field.value,
                "coach": coach_dropdown.value,
                "type": training_type.value,
                "date": date_picker.value,
                "time": time_picker.value,
                "rating": rating_slider.value,
                "review": review_field.value,
            })
            save_data(users, trainings)
            success_text.value = "Вы успешно записаны на тренировку!"
            success_text.visible = True
            clear_fields()
        page.update()

    # Меню Coach
    def show_coach_menu(header, logout_btn):
        coach_trainings = [
            t for t in trainings
            if t["coach"] == current_user["login"]
        ]

        trainings_list = ft.Column(
            [ft.Text("Ваши записи:", size=18, weight=ft.FontWeight.BOLD)] +
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Игрок: {t['player_name']}"),
                            ft.Text(f"Тип: {t['type']}"),
                            ft.Text(f"Дата: {t['date']} {t['time']}"),
                            ft.Text(f"Рейтинг: {'★' * int(t['rating'])}"),
                            ft.Text(f"Отзыв: {t['review']}") if t["review"] else ft.Text(""),
                        ], spacing=5),
                        padding=10,
                    ),
                    elevation=5,
                    margin=5,
                )
                for t in coach_trainings
            ],
            scroll=ft.ScrollMode.AUTO,
            height=400,
        )

        page.add(
            ft.Column([
                header,
                trainings_list,
                logout_btn,
            ], spacing=15)
        )

    # Меню Administration
    def show_admin_menu(header, logout_btn):
        all_trainings = ft.Column(
            [ft.Text("Все записи:", size=18, weight=ft.FontWeight.BOLD)] +
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Игрок: {t['player_name']} ({t['player_phone']})"),
                            ft.Text(f"Тренер: {t['coach']}"),
                            ft.Text(f"Тип: {t['type']}"),
                            ft.Text(f"Дата: {t['date']} {t['time']}"),
                        ], spacing=5),
                        padding=10,
                    ),
                    elevation=5,
                    margin=5,
                )
                for t in trainings
            ],
            scroll=ft.ScrollMode.AUTO,
            height=400,
        )

        page.add(
            ft.Column([
                header,
                all_trainings,
                logout_btn,
            ], spacing=15)
        )

    # Меню Owner
    def show_owner_menu(header, logout_btn):
        users_list = ft.Column(
            [ft.Text("Все пользователи:", size=18, weight=ft.FontWeight.BOLD)] +
            [
                ft.ListTile(
                    title=ft.Text(u),
                    subtitle=ft.Text(f"{users[u]['role']} - {users[u]['name']}"),
                    leading=ft.Icon(ft.icons.PERSON),
                )
                for u in users
            ],
            scroll=ft.ScrollMode.AUTO,
            height=200,
        )

        trainings_list = ft.Column(
            [ft.Text("Все записи:", size=18, weight=ft.FontWeight.BOLD)] +
            [
                ft.ListTile(
                    title=ft.Text(f"{t['player_name']} → {t['coach']}"),
                    subtitle=ft.Text(f"{t['type']} - {t['date']} {t['time']}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, idx=i: delete_training(idx),
                    ),
                )
                for i, t in enumerate(trainings)
            ],
            scroll=ft.ScrollMode.AUTO,
            height=300,
        )

        page.add(
            ft.Column([
                header,
                ft.ElevatedButton(
                    "Добавить сотрудника",
                    on_click=lambda e: show_register(e),
                    style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
                ),
                users_list,
                trainings_list,
                logout_btn,
            ], spacing=15)
        )

    def delete_training(idx):
        trainings.pop(idx)
        save_data(users, trainings)
        show_owner_menu()

    # Запуск приложения
    show_auth()


ft.app(target=main)