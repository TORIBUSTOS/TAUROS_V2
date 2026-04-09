# CLAUDE.md — Briefing para Claude en TORO_Prime

> Contexto de trabajo para Claude sessions en este proyecto.  
> Léelo al iniciar, actualiza si descubres nuevos patrones.

---

## Protocolo TORO LAB v2

Este proyecto **SIGUE ESTRICTAMENTE** el Protocolo TORO LAB v2:

- **Gates** (4): Validación progresiva antes de código
- **Bloques Negros** (8): Unidades de trabajo independientes
- **ADRs**: Decisiones arquitectónicas documentadas
- **Tracks**: A (Backend/Claude) + B (Frontend/Gemini) en paralelo

---

## Stack Técnico (FIJO - No cambiar sin ADR)

### Backend (Track A)
- **Runtime**: Python 3.12+
- **Framework**: FastAPI ^0.104
- **ORM**: SQLAlchemy ^2.0
- **Database**: SQLite v3 (local)
- **Validation**: Pydantic v2
- **Data Processing**: Pandas ^2.0
- **Testing**: Pytest ^7.0, >85% coverage
- **Backend puertos**: API 9000 (no 8000), CORS permite localhost:7000

### Frontend (Track B)
- **Runtime**: Node.js 18+
- **Framework**: Next.js 14+ (App Router)
- **UI**: React 18 + Hooks + Context API
- **Styling**: CSS Vanilla + CSS Variables
- **HTTP**: Axios ^1.6
- **Testing**: Vitest + React Testing Library, >70% coverage
- **Frontend puertos**: localhost 7000 (no 3000)

---

## El Diferenciador: Motor de INSIGHTS Inteligente

**TORO_Prime SÍ es**: Plataforma que entrega **INSIGHTS ESTRATÉGICOS REALES** filtrando RUIDO

### Ejemplo: OSPACA (Obra Social)
- ❌ **Dicho superficial**: "OSPACA es 40% de ingresos"
- ✅ **TORO_Prime insight**: "OSPACA este mes: 2x su monto normal porque pagó en el siguiente mes del anterior. No es cambio estructural, es timing."

**Motor Insights PRIME vs TAUROS:** Filtra RUIDO (timing: OSPACA 2x = desfasaje mes anterior, no cambio estructural) vs PATRONES REALES (nuevas recurrencias, cambios en montos).

---

## Bloques Negros (8 Unidades de Trabajo)

| BN | Nombre | Track | Status |
|:---|:---|:---|:---|
| **001** | Parser + Categorización | A | ✅ COMPLETO |
| **002** | Motor de INSIGHTS | A | ✅ COMPLETO |
| **003** | Forecasting 3 meses | A | ✅ COMPLETO |
| **004** | API REST | A | 🔄 En progreso |
| **005** | Dashboard Base | B | ⏳ AG comienza |
| **006** | Reportes (P&L) | B | ⏳ Espera BN-005 |
| **007** | Analytics | B | ⏳ Espera BN-005 |
| **008** | Integración Frontend | B | 🔴 Bloqueado por BN-004 |

---

## Principios de Código

### 1. Sin Hardcoding
```python
# ✅ SÍ
CATEGORIAS = db.query(CascadaRule).all()  # Lee de DB
config = get_settings()  # Lee de .env
```

### 2. Funciones Pequeñas
- Una responsabilidad por función
- Testeable en aislamiento
- Nombre describe qué hace

### 3. Type Safety
```python
# ✅ Siempre type hints
def categorize(movimiento: Movimiento, db: Session) -> str:
    ...
```

### 4. Testing First (TDD)
- Backend: >85% coverage (Pytest)
- Frontend: >70% coverage (Vitest)
- Critical paths: 100% (parser, insights, forecast)

### 5. conftest.py Pattern
- Test DB separada (test.db)
- Fixtures con rollback per test
- Nunca tocar DB principal durante tests

---

## Ejecución

### Token Budget
**Usuario en presupuesto limitado.** Si pide "compacta" → respuestas ultra-concisas sin repeticiones.

**Calidad NO NEGOCIA:** TDD >85% coverage, type safety, zero hardcoding → NO atajos por velocidad.

### Git & Bash
- **Bash en Windows:** Use `/c/Users/mauri/...` not `C:\Users\mauri\...`
- **Commit format:** `feat(BN-NNN): title` con bullets detallados
- **Repo:** https://github.com/TORIBUSTOS/TAUROS_V2.git

### Paralelo: Claude + Gemini/AG
- **Track A (Claude):** BN-001→004 Backend independiente
- **Track B (AG):** BN-005→007 Frontend con mock data (no espera API)
- **BN-008:** Integración, bloqueada por BN-004

---

## Preferencias Usuario
- Confía en recomendaciones técnicas
- UI/UX es su dominio
- **Etapas no timelines** (flexible, no deadlines fijos)
- Valora arquitectura limpia + calidad de producto

---

*Versión: 2.0*  
*Última actualización: 2026-04-09*  
*Responsable: Claude*
