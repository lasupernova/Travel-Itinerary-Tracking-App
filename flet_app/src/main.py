import flet as ft
from travel_app import notion, itinerary_db_id, today, filter, collect_paginated_api
import os

all_results = collect_paginated_api(
    notion.databases.query, 
    database_id=itinerary_db_id, 
    filter=filter
)

def main(page: ft.Page):
    counter = ft.Text(all_results, size=50, data=0)

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