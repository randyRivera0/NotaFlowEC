# NotaFlow EC

MVP para asistir a operadores de casas de valores en el ingreso, validación y preparación de negociación de notas de crédito tributarias en Ecuador.

Proyecto del **Track 4: Asistencia Inteligente para el Ingreso y Negociación de Notas de Crédito Tributarias en Ecuador** del Hackathon de Agentes Financieros IA.

## Problema y propuesta

El ingreso de una nota de crédito exige recopilar documentos, revisar información previamente validada, comprobar el título y preparar la negociación. NotaFlow EC reúne ese recorrido en un expediente único, propone datos mediante un agente simulado, aplica controles determinísticos y mantiene la decisión final en manos del operador.

La aplicación no ejecuta liquidaciones, transferencias, endosos ni transacciones financieras. Estas acciones quedan como propuestas o solicitudes de aprobación humana.

## Historias oficiales cubiertas

### 1. Ingreso asistido y antecedentes

- Recibe PDF y los datos de titular, RUC, título, tipo de nota, valor nominal y saldo.
- El agente simulado propone valores con fuente, fecha y confianza.
- Busca antecedentes por RUC o número de título.
- Exige confirmar, editar o rechazar cada sugerencia antes de crear el expediente.

### 2. Validación y siguiente acción

- Consulta una fuente SRI simulada.
- Comprueba existencia, estado, bloqueos, saldo y RUC.
- Detecta campos y documentos faltantes, duplicados, valores inválidos y coincidencias de riesgo.
- Presenta severidad, explicación, evidencia requerida y siguiente acción priorizada.
- Toda continuación sensible requiere aprobación humana.

### 3. Negociación y cierre asistido

- Calcula valor bruto, comisión y valor neto.
- Genera una ficha de negociación en estado `BORRADOR`.
- Conserva responsable, fechas, observaciones, documentos e historial durante la sesión.
- Liquidación, transferencia y endoso solo generan solicitudes de aprobación.

## Arquitectura

```text
Operador
   |
   v
NiceGUI (páginas y eventos)
   |
   v
Servicios de aplicación
   |-- IntakeService ------> AIProvider / MockAIProvider
   |-- ValidationService --> Reglas determinísticas
   |                         Fuente SRI simulada
   `-- NegotiationService -> Borrador y aprobación humana
   |
   v
Expediente demostrativo en memoria

FastAPI comparte la misma aplicación ASGI y expone /api/health.
```

La lógica de negocio no depende de NiceGUI. Un sistema empresarial podría reemplazar la interfaz, el proveedor de IA, la fuente simulada o el almacenamiento sin reescribir las reglas principales.

## Agente y controles antialucinación

`AIProvider` define el contrato de extracción asistida. El MVP utiliza `MockAIProvider`, un proveedor determinístico y sin conexión externa para que la demostración sea reproducible.

El agente solamente **propone** información. No aprueba títulos ni ejecuta decisiones financieras. Los datos requieren revisión humana y los controles críticos se resuelven con reglas determinísticas y evidencia visible. En producción, `MockAIProvider` podría sustituirse por Gemini u otro modelo, conservando validaciones y aprobación humana.

## Integración empresarial propuesta

- Sustituir el almacenamiento en memoria por PostgreSQL o el gestor documental de la casa de valores.
- Conectar una fuente autorizada de títulos y saldos en lugar del SRI simulado.
- Integrar identidad corporativa y roles de operador, cumplimiento y aprobador.
- Publicar los servicios mediante FastAPI para consumirlos desde un portal existente.
- Conservar auditoría, documentos y decisiones según las políticas regulatorias de la organización.

## Stack

- Python
- NiceGUI
- FastAPI
- Pydantic
- Pytest
- PyMuPDF y SQLAlchemy preparados como dependencias de evolución

## Instalación local

Requiere Python 3.12.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.main
```

Abra `http://127.0.0.1:8000`. La documentación de la API está en `/docs`.

## Pruebas automatizadas

```powershell
pytest
```

La suite cubre:

- Disponibilidad de API y páginas.
- Coherencia y trazabilidad del agente simulado.
- Búsqueda de antecedentes.
- Diez validaciones financieras y de cumplimiento.
- Priorización de la siguiente acción.
- Cálculos de negociación.
- Bloqueo de acciones sensibles sin borrador y solicitud de aprobación humana.

## Casos manuales de demostración

| Entrada | Resultado esperado | Resultado verificado |
|---|---|---|
| Crear expediente y analizar PDF de prueba | Seis sugerencias pendientes con fuente y confianza | Correcto |
| Intentar guardar con sugerencias pendientes | El sistema bloquea el guardado | Correcto |
| Buscar RUC `1790012345001` | Muestra el antecedente `EXP-2026-001` | Correcto |
| Validar `EXP-2026-001` | Todos los controles pasan; preparar negociación | Correcto |
| Validar `EXP-2026-002` | Diferencia de saldo y documento faltante | Correcto |
| Validar `EXP-2026-003` | Detecta bloqueo; enviar a cumplimiento | Correcto |
| Validar `EXP-2026-004` | Título inexistente y coincidencia de riesgo | Correcto |
| Generar negociación al 100 % y comisión 1,5 % | Muestra bruto, comisión, neto y estado BORRADOR | Correcto |
| Solicitar transferencia o endoso | Registra solicitud; no ejecuta la acción | Correcto |

## Limitaciones transparentes del MVP

- El agente es simulado; no invoca un LLM externo.
- El PDF se recibe, pero su contenido todavía no se extrae automáticamente.
- Los datos se almacenan en memoria y se reinician al detener la aplicación.
- La fuente SRI y las coincidencias de riesgo son simuladas.
- No se ejecutan acciones reguladas ni transacciones reales.
