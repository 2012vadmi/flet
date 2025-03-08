import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    error_text = ft.Text("", color="red")

    def handle_close_proverka(e):
        page.close(proverka)

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

    login = ft.TextField(label="login", smart_dashes_type=True)
    passwordd = ft.TextField(label="password", smart_dashes_type=True, password=True)

    def answer_form(e):
        answer_login = login.value
        answer_password = passwordd.value
        if login.value == "":
            if passwordd.value == "":
                passwordd.error_text = "Поле не заполнено!"
                passwordd.bgcolor = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
                error_text.value = "Поле должно быть заполнено."
            else:
                passwordd.error_text = None
                passwordd.bgcolor = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
                error_text.value = ""
                print("hbnyiubyb")
            login.error_text = "Поле не заполнено!"
            login.bgcolor = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
            error_text.value = "Поле должно быть заполнено."
        else:
            if passwordd.value == "":
                passwordd.error_text = "Поле не заполнено!"
                passwordd.bgcolor = ft.Colors.with_opacity(0.5, '#ff0000')  # ft.Colors.RED
                error_text.value = "Поле должно быть заполнено."
            else:
                passwordd.error_text = None
                passwordd.bgcolor = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
                error_text.value = ""
            login.error_text = None
            login.bgcolor = ft.Colors.with_opacity(0.5, '#ffffff')  # ft.Colors.white
            error_text.value = ""
        print(f"{login.value},{passwordd.value}")

    form = ft.Column([
        ft.Text("Вход:", style=ft.TextStyle(weight="bold")),
        login,
        passwordd,
        ft.ElevatedButton("Записаться", on_click=answer_form),
    ])

    page.add(form)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
