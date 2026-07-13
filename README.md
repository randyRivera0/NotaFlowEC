# NotaFlow EC

MVP demostrable para asistir el ingreso, validación y negociación de notas de crédito tributarias en Ecuador. FastAPI y NiceGUI comparten la misma aplicación ASGI mediante `ui.run_with(app)`.

## Alcance

- Dashboard con métricas y expedientes ficticios en memoria.
- Ingreso asistido con IA simulada, antecedentes y aprobación de cada sugerencia.
- Diez validaciones determinísticas contra una fuente SRI simulada, con evidencia y próxima acción.
- Borrador de negociación, cálculos, historial y solicitudes de aprobación humana.
- Detalle con resumen, documentos, sugerencias, validaciones, negociación e historial.
- Endpoint `GET /api/health`.
- Capas separadas para servicios, reglas e integraciones.

La aplicación no ejecuta transacciones financieras ni acciones reguladas. Los datos permanecen en memoria y se reinician al detener la aplicación.

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
