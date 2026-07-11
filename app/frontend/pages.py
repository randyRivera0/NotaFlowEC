from nicegui import ui

from app.frontend.components.layout import main_layout
from app.frontend.data import CASES, find_case
from app.frontend.theme import apply_theme


def register_pages() -> None:
    apply_theme()

    @ui.page("/")
    def dashboard() -> None:
        with main_layout("Dashboard"):
            with ui.row().classes("w-full items-end"):
                with ui.column().classes("gap-1"):
                    ui.label("Expedientes").classes("text-2xl font-bold")
                    ui.label("Seguimiento de notas de crédito tributarias").classes("nf-muted")
                ui.space()
                ui.button("Crear expediente", icon="add", on_click=lambda: ui.navigate.to("/cases/new")).props("unelevated no-caps")
            with ui.grid(columns=4).classes("w-full gap-4"):
                for label, value, icon, color in [
                    ("Expedientes activos", "12", "folder_open", "blue"),
                    ("En validación", "5", "fact_check", "orange"),
                    ("Listos para negociar", "3", "verified", "green"),
                    ("Valor nominal", "$239.751", "payments", "purple"),
                ]:
                    with ui.card().classes("nf-card p-5"):
                        with ui.row().classes("w-full items-center"):
                            with ui.column().classes("gap-1"):
                                ui.label(label).classes("text-sm nf-muted")
                                ui.label(value).classes("text-2xl font-bold")
                            ui.space()
                            ui.icon(icon, color=color, size="30px")
            with ui.card().classes("nf-card w-full p-0"):
                with ui.row().classes("w-full items-center p-5 pb-2"):
                    ui.label("Expedientes recientes").classes("text-lg font-semibold")
                    ui.space()
                    ui.input(placeholder="Buscar por RUC o título").props("dense outlined clearable").classes("w-72")
                    ui.select(["Todos", "En validación", "Documentos pendientes"], value="Todos").props("dense outlined").classes("w-48")
                columns = [
                    {"name": "id", "label": "EXPEDIENTE", "field": "id", "align": "left"},
                    {"name": "holder", "label": "TITULAR", "field": "holder", "align": "left"},
                    {"name": "ruc", "label": "RUC", "field": "ruc", "align": "left"},
                    {"name": "title", "label": "TÍTULO", "field": "title", "align": "left"},
                    {"name": "amount", "label": "VALOR NOMINAL", "field": "amount_display"},
                    {"name": "status", "label": "ESTADO", "field": "status", "align": "left"},
                    {"name": "updated", "label": "ACTUALIZADO", "field": "updated", "align": "left"},
                ]
                table = ui.table(columns=columns, rows=CASES, row_key="id").classes("w-full").props("flat")
                table.on("rowClick", lambda event: ui.navigate.to(f"/cases/{event.args[1]['id']}"))

    @ui.page("/cases/new")
    def new_case() -> None:
        with main_layout("Nuevo expediente"):
            ui.label("Crear expediente").classes("text-2xl font-bold")
            ui.label("Registre la información inicial de la nota de crédito.").classes("nf-muted")
            with ui.card().classes("nf-card w-full p-6"):
                ui.label("Documento principal").classes("text-lg font-semibold")
                with ui.column().classes("w-full items-center border-2 border-dashed border-slate-300 rounded-xl p-8 bg-slate-50"):
                    ui.icon("upload_file", size="46px").classes("text-slate-400")
                    ui.label("Cargue la nota de crédito en PDF").classes("font-medium")
                    ui.label("La extracción automática se habilitará en una próxima fase.").classes("text-sm nf-muted")
                    ui.upload(label="Seleccionar PDF", auto_upload=False).props("accept=.pdf flat color=primary")
                ui.separator().classes("my-4")
                ui.label("Información del título").classes("text-lg font-semibold")
                with ui.grid(columns=2).classes("w-full gap-5"):
                    ui.input("Titular").props("outlined")
                    ui.input("RUC o identificación").props("outlined")
                    ui.input("Número de título").props("outlined")
                    ui.select(["Nota de crédito tributaria", "Otro"], label="Tipo de nota").props("outlined")
                    ui.number("Valor nominal", format="%.2f", prefix="$ ").props("outlined")
                    ui.number("Saldo", format="%.2f", prefix="$ ").props("outlined")
                with ui.row().classes("w-full justify-end mt-4"):
                    ui.button("Cancelar", on_click=lambda: ui.navigate.to("/")).props("flat no-caps")
                    ui.button("Crear expediente", icon="save", on_click=lambda: ui.notify("Demo: el expediente aún no se guarda", type="info")).props("unelevated no-caps")

    @ui.page("/cases/{case_id}")
    def case_detail(case_id: str) -> None:
        case = find_case(case_id)
        with main_layout("Detalle del expediente"):
            if case is None:
                ui.label("Expediente no encontrado").classes("text-2xl font-bold")
                ui.button("Volver al dashboard", on_click=lambda: ui.navigate.to("/"))
                return
            with ui.row().classes("w-full items-center"):
                with ui.column().classes("gap-1"):
                    ui.label(str(case["id"])).classes("text-2xl font-bold")
                    ui.label(f"{case['holder']} · RUC {case['ruc']}").classes("nf-muted")
                ui.space()
                ui.badge(str(case["status"]), color="blue").props("outline")
            tab_names = ("Resumen", "Documentos", "Datos sugeridos", "Validaciones", "Negociación", "Historial")
            with ui.tabs().classes("w-full text-slate-600") as tabs:
                tab_elements = {name: ui.tab(name) for name in tab_names}
            with ui.tab_panels(tabs, value=tab_elements["Resumen"]).classes("w-full bg-transparent p-0"):
                with ui.tab_panel(tab_elements["Resumen"]):
                    with ui.grid(columns=3).classes("w-full gap-4"):
                        values = [("Titular", case["holder"]), ("Número de título", case["title"]), ("Valor nominal", f"$ {case['amount']:,.2f}"), ("RUC", case["ruc"]), ("Responsable", "Ana Ortiz"), ("Actualizado", case["updated"])]
                        for label, value in values:
                            with ui.card().classes("nf-card p-5"):
                                ui.label(label).classes("text-sm nf-muted")
                                ui.label(str(value)).classes("font-semibold")
                for name in tab_names[1:]:
                    with ui.tab_panel(tab_elements[name]):
                        with ui.card().classes("nf-card w-full p-8 items-center"):
                            ui.icon("construction", size="42px").classes("text-slate-400")
                            ui.label(name).classes("text-lg font-semibold")
                            ui.label("Esta sección se habilitará en la siguiente fase.").classes("nf-muted")
