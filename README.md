# NotaFlow EC

Esqueleto inicial para asistir la gestión y negociación de notas de crédito tributarias en Ecuador. FastAPI y NiceGUI comparten la misma aplicación ASGI mediante `ui.run_with(app)`.

## Alcance

- Dashboard con métricas y expedientes ficticios en memoria.
- Formulario visual para crear un expediente.
- Detalle con pestañas de resumen, documentos, sugerencias, validaciones, negociación e historial.
- Endpoint `GET /api/health`.
- Capas preparadas para servicios, reglas, repositorios e integraciones.

Este incremento no persiste datos ni implementa extracción PDF, IA, validaciones o transacciones financieras.

## Instalación y ejecución

Requiere Python 3.12.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.main
```

Abra `http://127.0.0.1:8000`. La documentación API está en `/docs`.

## Pruebas

```powershell
pytest
```

## Estructura

```text
app/
├── api/             # Endpoints FastAPI
├── frontend/        # Páginas, componentes y tema NiceGUI
├── integrations/    # Integraciones futuras
├── repositories/    # Persistencia futura
├── rules/           # Reglas futuras
├── services/        # Casos de uso futuros
└── main.py           # Aplicación ASGI compartida
```
