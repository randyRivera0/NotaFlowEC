from nicegui import ui

from app.frontend.components.layout import main_layout
from app.frontend.data import CASES, find_case
from app.frontend.theme import apply_theme
from app.integrations.ai_provider import MockAIProvider
from app.integrations.sri_source import MockSRISource
from app.services.intake import IntakeService
from app.services.negotiation import NegotiationService
from app.services.validation import ValidationService


intake_service = IntakeService(MockAIProvider())
validation_service = ValidationService(MockSRISource())
negotiation_service = NegotiationService()


def register_pages() -> None:
    @ui.page("/")
    def dashboard() -> None:
        apply_theme()
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
        apply_theme()
        suggestions: list[dict[str, object]] = []
        document_name = {"value": "nota_credito_demo.pdf"}

        with main_layout("Nuevo expediente"):
            ui.label("Crear expediente").classes("text-2xl font-bold")
            ui.label("Cargue el documento, revise las sugerencias y apruebe cada dato antes de guardar.").classes("nf-muted")
            with ui.card().classes("nf-card w-full p-6"):
                ui.label("Documento principal").classes("text-lg font-semibold")
                with ui.column().classes("w-full items-center border-2 border-dashed border-slate-300 rounded-xl p-8 bg-slate-50"):
                    ui.icon("upload_file", size="46px").classes("text-slate-400")
                    ui.label("Cargue la nota de crédito en PDF").classes("font-medium")
                    ui.label("El modo IA simulado propone datos; nada se guarda sin su aprobación.").classes("text-sm nf-muted")

                    def remember_upload(event: object) -> None:
                        name = getattr(event, "name", None)
                        document_name["value"] = str(name or "nota_credito_demo.pdf")
                        ui.notify(f"Documento listo: {document_name['value']}", type="positive")

                    ui.upload(label="Seleccionar PDF", on_upload=remember_upload).props("accept=.pdf flat color=primary")
                ui.separator().classes("my-4")
                ui.label("Información del título").classes("text-lg font-semibold")
                with ui.grid(columns=2).classes("w-full gap-5"):
                    holder = ui.input("Titular").props("outlined")
                    ruc = ui.input("RUC o identificación").props("outlined")
                    title = ui.input("Número de título").props("outlined")
                    note_type = ui.select(["Nota de crédito tributaria", "Otro"], label="Tipo de nota").props("outlined")
                    amount = ui.number("Valor nominal", format="%.2f", prefix="$ ").props("outlined")
                    balance = ui.number("Saldo", format="%.2f", prefix="$ ").props("outlined")

                ui.label("Antecedentes reutilizables").classes("text-lg font-semibold mt-5")
                background_area = ui.column().classes("w-full")

                def search_background() -> None:
                    background_area.clear()
                    matches = intake_service.find_background(str(ruc.value or ""), str(title.value or ""))
                    with background_area:
                        if not matches:
                            ui.label("No se encontraron antecedentes con esos criterios.").classes("nf-muted")
                        for match in matches:
                            with ui.card().classes("w-full p-4 border"):
                                ui.label(f"{match['case_id']} · {match['holder']}").classes("font-semibold")
                                ui.label(
                                    f"RUC {match['ruc']} · Título {match['title']} · "
                                    f"Fuente: {match['source']} · Fecha: {match['date']} · Estado: {match['status']}"
                                ).classes("text-sm nf-muted")

                ui.button("Buscar antecedentes", icon="manage_search", on_click=search_background).props("outline no-caps")

                ui.label("Datos sugeridos por IA").classes("text-lg font-semibold mt-5")
                suggestion_area = ui.column().classes("w-full gap-2")

                def analyze() -> None:
                    suggestions.clear()
                    suggestions.extend(intake_service.suggest(document_name["value"]))
                    suggestion_area.clear()
                    field_inputs = {
                        "Titular": holder,
                        "RUC": ruc,
                        "Número de título": title,
                        "Tipo de nota": note_type,
                        "Valor nominal": amount,
                        "Saldo": balance,
                    }
                    with suggestion_area:
                        for suggestion in suggestions:
                            with ui.card().classes("w-full p-4 border"):
                                with ui.row().classes("w-full items-center"):
                                    with ui.column().classes("gap-0 grow"):
                                        ui.label(str(suggestion["field"])).classes("font-semibold")
                                        ui.label(str(suggestion["value"])).classes("text-base")
                                        ui.label(
                                            f"Fuente: {suggestion['source']} · Fecha: {suggestion['date']} · "
                                            f"Confianza: {float(suggestion['confidence']):.0%}"
                                        ).classes("text-xs nf-muted")
                                    status = ui.badge("Pendiente", color="orange")

                                    def decide(action: str, item: dict[str, object] = suggestion, badge: object = status) -> None:
                                        item["status"] = action
                                        badge.set_text(action)  # type: ignore[attr-defined]
                                        color = {"Confirmado": "green", "Editado": "blue", "Rechazado": "red"}[action]
                                        badge.props(f"color={color}")  # type: ignore[attr-defined]
                                        if action in {"Confirmado", "Editado"}:
                                            target = field_inputs[str(item["field"])]
                                            value: object = item["value"]
                                            if str(item["field"]) in {"Valor nominal", "Saldo"}:
                                                value = float(str(value))
                                            target.value = value
                                            target.update()

                                    ui.button("Confirmar", on_click=lambda s=suggestion, b=status: decide("Confirmado", s, b)).props("flat dense no-caps color=positive")
                                    ui.button("Editar", on_click=lambda s=suggestion, b=status: decide("Editado", s, b)).props("flat dense no-caps color=primary")
                                    ui.button("Rechazar", on_click=lambda s=suggestion, b=status: decide("Rechazado", s, b)).props("flat dense no-caps color=negative")

                ui.button("Analizar con IA simulada", icon="auto_awesome", on_click=analyze).props("unelevated no-caps")

                def save_case() -> None:
                    if suggestions and any(item["status"] == "Pendiente" for item in suggestions):
                        ui.notify("Confirme o rechace cada sugerencia antes de guardar.", type="warning")
                        return
                    if not all([holder.value, ruc.value, title.value, note_type.value, amount.value, balance.value]):
                        ui.notify("Complete todos los datos requeridos.", type="warning")
                        return
                    case = intake_service.create_case(
                        {"holder": holder.value, "ruc": ruc.value, "title": title.value, "amount": amount.value, "balance": balance.value, "documents": ["nota_credito"]}
                    )
                    ui.notify("Expediente creado con aprobación del operador.", type="positive")
                    ui.navigate.to(f"/cases/{case['id']}")

                with ui.row().classes("w-full justify-end mt-4"):
                    ui.button("Cancelar", on_click=lambda: ui.navigate.to("/")).props("flat no-caps")
                    ui.button("Crear expediente", icon="save", on_click=save_case).props("unelevated no-caps")

    @ui.page("/cases/{case_id}")
    def case_detail(case_id: str) -> None:
        apply_theme()
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
                with ui.tab_panel(tab_elements["Documentos"]):
                    with ui.card().classes("nf-card w-full p-5"):
                        ui.label("Documentos del expediente").classes("text-lg font-semibold")
                        documents = list(case.get("documents") or [])
                        if documents:
                            for document in documents:
                                with ui.row().classes("w-full items-center border rounded-lg p-3"):
                                    ui.icon("picture_as_pdf", color="red")
                                    ui.label("Nota de crédito tributaria" if document == "nota_credito" else str(document))
                                    ui.space()
                                    ui.badge("Adjunto", color="green").props("outline")
                        else:
                            ui.label("No hay documentos adjuntos.").classes("nf-muted")
                with ui.tab_panel(tab_elements["Datos sugeridos"]):
                    with ui.card().classes("nf-card w-full p-8 items-center"):
                        ui.icon("verified_user", size="42px").classes("text-green-600")
                        ui.label("Datos revisados por el operador").classes("text-lg font-semibold")
                        ui.label("Los datos visibles en el resumen fueron confirmados antes de crear el expediente.").classes("nf-muted")
                with ui.tab_panel(tab_elements["Validaciones"]):
                    validation = validation_service.validate(case)
                    with ui.card().classes("nf-card w-full p-5"):
                        with ui.row().classes("w-full items-center"):
                            with ui.column().classes("gap-1"):
                                ui.label("Próxima acción recomendada").classes("text-sm nf-muted")
                                ui.label(str(validation["next_action"])).classes("text-xl font-bold")
                                ui.label(str(validation["source"])).classes("text-xs nf-muted")
                            ui.space()
                            ui.badge("Requiere aprobación humana", color="orange").props("outline")
                    for item in validation["results"]:
                        color = "green" if item["passed"] else ("red" if item["severity"] == "critical" else "orange")
                        icon = "check_circle" if item["passed"] else "error"
                        with ui.card().classes("nf-card w-full p-4"):
                            with ui.row().classes("w-full items-start no-wrap"):
                                ui.icon(icon, color=color, size="26px")
                                with ui.column().classes("gap-1 grow"):
                                    with ui.row().classes("items-center"):
                                        ui.label(str(item["code"])).classes("font-bold")
                                        ui.badge("Superado" if item["passed"] else str(item["severity"]).capitalize(), color=color)
                                    ui.label(str(item["explanation"])).classes("text-sm")
                                    ui.label(f"Evidencia: {item['evidence']}").classes("text-sm nf-muted")
                                    if not item["passed"]:
                                        ui.label(f"Acción: {item['action']}").classes("text-sm font-semibold")
                    with ui.row().classes("w-full justify-end"):
                        ui.button(
                            f"Solicitar aprobación: {validation['next_action']}",
                            icon="approval",
                            on_click=lambda: ui.notify("Solicitud registrada para revisión humana.", type="positive"),
                        ).props("unelevated no-caps")
                with ui.tab_panel(tab_elements["Negociación"]):
                    with ui.card().classes("nf-card w-full p-5"):
                        ui.label("Preparación de negociación").classes("text-lg font-semibold")
                        ui.label("Revise los cálculos y genere un borrador antes de solicitar aprobación.").classes("nf-muted")
                        with ui.grid(columns=3).classes("w-full gap-4"):
                            ui.number("Saldo confirmado", value=float(case.get("balance") or case["amount"]), prefix="$ ").props("outlined readonly")
                            negotiation_percentage = ui.number("Porcentaje de negociación", value=100, min=0.01, max=100, suffix=" %").props("outlined")
                            commission_percentage = ui.number("Comisión", value=1.5, min=0, max=100, suffix=" %").props("outlined")
                        draft_area = ui.column().classes("w-full")

                        def show_draft(draft: dict[str, object]) -> None:
                            draft_area.clear()
                            with draft_area:
                                with ui.card().classes("w-full bg-slate-50 border p-5"):
                                    ui.label("FICHA DE NEGOCIACIÓN · BORRADOR").classes("font-bold text-primary")
                                    ui.label(f"Expediente: {draft['case_id']} · Título: {draft['title']}")
                                    ui.label(f"Titular: {draft['holder']} · RUC: {draft['ruc']}")
                                    with ui.grid(columns=3).classes("w-full gap-3 mt-2"):
                                        for label, key in (
                                            ("Valor bruto", "gross_value"),
                                            ("Comisión", "commission"),
                                            ("Valor neto", "net_value"),
                                        ):
                                            with ui.card().classes("p-3 border"):
                                                ui.label(label).classes("text-xs nf-muted")
                                                ui.label(f"$ {float(draft[key]):,.2f}").classes("font-bold")
                                    ui.label(f"Responsable: {draft['responsible']} · Estado: {draft['status']}").classes("text-sm nf-muted")

                        def generate_draft() -> None:
                            try:
                                draft = negotiation_service.generate_draft(
                                    case,
                                    float(negotiation_percentage.value or 0),
                                    float(commission_percentage.value or 0),
                                )
                            except ValueError as error:
                                ui.notify(str(error), type="warning")
                                return
                            show_draft(draft)
                            ui.notify("Borrador generado para revisión; aún no está aprobado.", type="positive")

                        ui.button("Generar borrador", icon="description", on_click=generate_draft).props("outline no-caps")
                        ui.separator().classes("my-4")
                        with ui.grid(columns=2).classes("w-full gap-4"):
                            approval_action = ui.select(
                                ["Negociación", "Liquidación", "Transferencia", "Endoso"],
                                value="Negociación",
                                label="Acción propuesta",
                            ).props("outlined")
                            observation = ui.input("Observación para el aprobador").props("outlined")

                        def request_negotiation_approval() -> None:
                            try:
                                negotiation_service.request_approval(
                                    case,
                                    str(approval_action.value),
                                    str(observation.value or ""),
                                )
                            except ValueError as error:
                                ui.notify(str(error), type="warning")
                                return
                            ui.notify("Solicitud enviada. No se ejecutó ninguna acción regulada.", type="positive")

                        with ui.row().classes("w-full justify-end"):
                            ui.button("Solicitar aprobación humana", icon="approval", on_click=request_negotiation_approval).props("unelevated no-caps")
                with ui.tab_panel(tab_elements["Historial"]):
                    with ui.card().classes("nf-card w-full p-5"):
                        ui.label("Trazabilidad del expediente").classes("text-lg font-semibold")
                        ui.label(f"Responsable actual: {case.get('responsible', 'Ana Ortiz')}").classes("nf-muted")
                        for event in reversed(list(case.get("history") or [])):
                            with ui.row().classes("w-full items-start border-b py-3 no-wrap"):
                                ui.icon("history", color="primary")
                                with ui.column().classes("gap-0"):
                                    ui.label(str(event["event"])).classes("font-semibold")
                                    ui.label(f"{event['date']} · {event['responsible']}").classes("text-xs nf-muted")
                        observations = list(case.get("observations") or [])
                        if observations:
                            ui.label("Observaciones").classes("font-semibold mt-4")
                            for item in observations:
                                ui.label(f"• {item}").classes("text-sm")
