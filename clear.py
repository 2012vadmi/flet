import flet as ft


def main(page: ft.Page):
    btn_clear = ft.ElevatedButton("Очистить", width=100)

    text_field_1 = ft.TextField(label="Текст 1", expand=True)
    text_field_2 = ft.TextField(label="Текст 2", expand=True)
    button_1 = ft.ElevatedButton("Кнопка 1")
    button_2 = ft.ElevatedButton("Кнопка 2")
    container = ft.Container(content=ft.Text("Текст в контейнере"), bgcolor="blue", padding=10)

    def clear_all(e):
        for control in page.controls[
                       :]:  # Создаем копию списка, чтобы избежать ошибки при изменении списка во время итерации
            if control != btn_clear:
                page.controls.remove(control)
        page.update()

    page.add(
        btn_clear,
        text_field_1,
        text_field_2,
        button_1,
        button_2,
        container,
    )
    btn_clear.on_click = clear_all
    page.update()


ft.app(target=main)
