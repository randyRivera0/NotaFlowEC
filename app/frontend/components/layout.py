from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui


@contextmanager
def main_layout(page_title: str) -> Iterator[None]:
    with ui.header().classes("bg-white text-slate-800 border-b h-16 items-center"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).props("flat round color=primary")
        ui.label(page_title).classes("text-lg font-semibold")
        ui.space()
        ui.icon("notifications_none").classes("text-slate-500 text-xl")
        with ui.avatar(color="primary", text_color="white", size="36px"):
            ui.label("AO")
        ui.label("Ana Ortiz").classes("text-sm font-medium")
    with ui.left_drawer(value=True).classes("nf-sidebar p-4") as drawer:
        with ui.column().classes("w-full gap-1"):
            with ui.row().classes("items-center gap-3 mb-7 px-2"):
                ui.icon("account_balance", size="30px").classes("text-cyan-300")
                with ui.column().classes("gap-0"):
                    ui.label("NotaFlow EC").classes("text-xl font-bold")
                    ui.label("Gestión tributaria").classes("text-xs text-blue-100")
            ui.button("Dashboard", icon="dashboard", on_click=lambda: ui.navigate.to("/")).props("flat no-caps").classes("nf-nav")
            ui.button("Nuevo expediente", icon="add_circle_outline", on_click=lambda: ui.navigate.to("/cases/new")).props("flat no-caps").classes("nf-nav")
            ui.separator().classes("my-4 opacity-30")
            ui.label("OPERACIÓN").classes("text-xs tracking-wider text-blue-200 px-3")
            ui.button("Expedientes", icon="folder_open").props("flat no-caps disable").classes("nf-nav")
            ui.button("Solicitudes", icon="approval").props("flat no-caps disable").classes("nf-nav")
            ui.label("Entorno de demostración").classes("text-xs text-blue-200 px-3 mt-8")
    with ui.column().classes("nf-page"):
        yield
