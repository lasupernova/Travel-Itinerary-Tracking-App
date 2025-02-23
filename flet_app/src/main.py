import flet as ft
from travel_app import *
import os


# travel_app.
token = os.environ['NOTION_TOKEN']
itinerary_db_id = os.environ['DB_ID']  

def main(page: ft.Page):
    counter = ft.Text(token, size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)