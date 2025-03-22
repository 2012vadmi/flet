import flet as ft
import os # для работы с файлами
import datetime

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    error_text = ft.Text("", color="red")  # Текст ошибки

    nametext =  ft.TextField(label="Имя", smart_dashes_type=True)
    phonetext = ft.TextField(label="Телефон")
    datetext = ft.Text(value=datetime
                       .datetime.now().strftime('%Y-%m-%d'))
    datebutton = ft.ElevatedButton(
        "Pick date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2025, month=2, day=22),
                last_date=datetime.datetime(year=2026, month=2, day=22),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
    )
    # Данные (замените на ваши данные)
    schedule = """
    Понедельник: 10:00 - 11:00, 18:00 - 19:00
    Вторник: 10:00 - 11:00
    Среда: 18:00 - 19:00
    """
    price = "1000 руб. за тренировку"
    reviews = ["Отличный тренер!", "Замечательные тренировки!"]
    contacts = "Телефон: +79123456789, Email: info@example.com"
    online_training = "https://www.worldclass.ru/" # Замените на вашу ссылку

    # Виджеты
    page.title = "Запись на тренировки"
    page.appbar = ft.AppBar(title=ft.Text("Запись на тренировки"))
    def forym():
        forym_page = ft.Column([
            btn_clear,
            nametext,
            phonetext,
            datebutton,
            datetext,
            ft.ElevatedButton("Записаться", on_click=submit_form),
        ])
        page.add(forym_page)
        page.update()


    def clear_all():
        for control in page.controls[
                       :]:  # Создаем копию списка, чтобы избежать ошибки при изменении списка во время итерации
            if control != btn_clear:
                page.controls.remove(control)
        page.update()

    def exitt(e):
        login = ft.TextField(label="login", smart_dashes_type=True)
        passwordd = ft.TextField(label="password", smart_dashes_type=True, password=True)
        clear_all()
        page.update()
        def answer_form(e):
            if login.value == "":
                if passwordd.value == "":
                    passwordd.error_text = "Поле не заполнено!"
                    passwordd.Colors = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
                    error_text.value = "Поле должно быть заполнено."
                else:
                    passwordd.error_text = None
                    passwordd.Colors = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
                    error_text.value = ""
                login.error_text = "Поле не заполнено!"
                login.Colors = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
                error_text.value = "Поле должно быть заполнено."
            else:
                if passwordd.value == "":
                    passwordd.error_text = "Поле не заполнено!"
                    passwordd.Colors = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
                    error_text.value = "Поле должно быть заполнено."
                else:
                    passwordd.error_text = None
                    passwordd.Colors = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
                    error_text.value = ""
                login.error_text = None
                login.Colors = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
                error_text.value = ""
            clear_all()
            forym()
            print(f"{login.value},{passwordd.value}")
        form_exitt = ft.Column([
            ft.Text("Вход:", style=ft.TextStyle(weight="bold")),
            login,
            passwordd,
            ft.ElevatedButton("Вход", on_click=answer_form),
        ])
        page.add(form_exitt)
    # Форма записи
    btn_clear = ft.ElevatedButton("Вход/выход", width=100, on_click=exitt)

    def handle_close(e):
        page.close(dlg_modal)

    def handle_close_proverka(e):
        page.close(proverka)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Точно хотите подтвердить?"),
        content=ft.Text("Вы действительно хотите подтвердить тренеровку эту тренеровку?"),
        actions=[
            ft.TextButton("Да", on_click=handle_close),
            ft.TextButton("Нет", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print(
            "Тренеровка не подтверждена"
        ),
    )
    proverka = ft.AlertDialog(
        modal=True,
        title=ft.Text("Поле не заполнено"),
        content=ft.Text("поле не заполнено продлжте за полнять"),
        actions=[
            ft.TextButton("Продолжеть", on_click=handle_close_proverka),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print('кнопка не нажата')

    )
    def handle_change(e):
        datetext.value = e.control.value.strftime('%Y-%m-%d')

    def handle_dismissal(e):
        datetext.value = "DatePicker dismissed"

    def submit_form(e):
        name = nametext.value
        phone = phonetext.value
        date = datetext.value
        print(f"Запись: {name}, {phone}, {date}")
        if nametext.value == "":
            if phonetext.value == "":
                phonetext.error_text = "Поле не заполнено!"
                phonetext.Colors = ft.colors.RED_100
                error_text.value = "Поле должно быть заполнено."
            else:
                phonetext.error_text = None
                phonetext.Colors = ft.colors.WHITE
                error_text.value = ""
            nametext.error_text = "Поле не заполнено!"
            nametext.Colors = ft.colors.RED_100
            error_text.value = "Поле должно быть заполнено."
        else:
            if phonetext.value == "":
                phonetext.error_text = "Поле не заполнено!"
                phonetext.Colors = ft.colors.RED_100
                error_text.value = "Поле должно быть заполнено."
            else:
                phonetext.error_text = None
                phonetext.Colors = ft.colors.WHITE
                error_text.value = ""
            nametext.error_text = None
            nametext.Colors = ft.colors.WHITE
            error_text.value = ""
        page.update()



    form = ft.Column([
        btn_clear,
        nametext,
        phonetext,
        datebutton,
        datetext,
        ft.ElevatedButton("Записаться", on_click=submit_form),
    ])

    # Отображение информации
    info_section = ft.Column([
        ft.Text("Расписание:",style=ft.TextStyle(weight="bold")),
        ft.Text(schedule),
        ft.Text("Цена:", style=ft.TextStyle(weight="bold")),
        ft.Text(price),
        ft.Text("Отзывы:", style=ft.TextStyle(weight="bold")),
        ft.Column([ft.Text(review) for review in reviews]), # Просто выводит отзывы
        ft.Text("Контакты:", style=ft.TextStyle(weight="bold")),
        ft.Text(contacts),
        ft.Text("Онлайн тренировки:", style=ft.TextStyle(weight="bold")),
        ft.ElevatedButton(
            "Ссылка на онлайн тренировку",
            on_click=lambda e: page.launch_url(online_training)
        )
    ])

    page.add(form, info_section) # Добавление виджетов на страницу


ft.app(target=main, view=ft.AppView.WEB_BROWSER)