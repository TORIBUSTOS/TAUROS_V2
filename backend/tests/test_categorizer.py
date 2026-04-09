import pytest
from src.services.categorizer import CategorizerService
from src.models.movement import Movimiento, CascadaRule

def test_categorizer_applies_rule(db):
    """Categorizer debe aplicar regla de DB"""
    # Crear regla
    rule = CascadaRule(
        categoria="Obra Social",
        patron="OSPACA",
        peso=0.95,
        veces_usada=1,
        activo=1
    )
    db.add(rule)
    db.commit()

    # Crear movimiento
    mov = Movimiento(
        fecha="2024-01-01",
        descripcion="Pago OSPACA",
        monto=1000.0,
        categoria="Sin categorizar",
        confianza=0.0
    )

    # Categorizar
    categoria = CategorizerService.categorize(mov, db)

    assert categoria == "Obra Social"
    assert mov.categoria == "Obra Social"
    assert mov.confianza == 0.95

def test_categorizer_no_match(db):
    """Sin match → Sin categorizar"""
    mov = Movimiento(
        fecha="2024-01-01",
        descripcion="Transacción desconocida XYZ",
        monto=100.0,
        categoria="Sin categorizar",
        confianza=0.0
    )

    categoria = CategorizerService.categorize(mov, db)

    assert categoria == "Sin categorizar"
    assert mov.confianza == 0.0

def test_categorizer_picks_highest_weight(db):
    """Con múltiples matches, elige la de mayor peso"""
    # Dos reglas
    db.add(CascadaRule(categoria="Proveedores", patron="PROV", peso=0.50, activo=1))
    db.add(CascadaRule(categoria="Servicios", patron="PROV SVC", peso=0.90, activo=1))
    db.commit()

    mov = Movimiento(
        fecha="2024-01-01",
        descripcion="Pago PROV SVC",
        monto=500.0
    )

    categoria = CategorizerService.categorize(mov, db)

    # Debe elegir "Servicios" porque tiene mayor peso (0.90 > 0.50)
    assert categoria == "Servicios"
    assert mov.confianza == 0.90

def test_categorizer_case_insensitive(db):
    """Búsqueda debe ser case-insensitive"""
    db.add(CascadaRule(categoria="Obra Social", patron="OSPACA", peso=0.95, activo=1))
    db.commit()

    # Test variaciones de caso
    for desc in ["ospaca", "Ospaca", "OSPACA", "oSpAcA"]:
        mov = Movimiento(fecha="2024-01-01", descripcion=f"Pago {desc}", monto=1000.0)
        categoria = CategorizerService.categorize(mov, db)
        assert categoria == "Obra Social", f"Failed for: {desc}"

def test_categorizer_ignores_inactive_rules(db):
    """Reglas inactivas no deben aplicarse"""
    db.add(CascadaRule(categoria="Obra Social", patron="OSPACA", peso=0.95, activo=0))
    db.commit()

    mov = Movimiento(fecha="2024-01-01", descripcion="Pago OSPACA", monto=1000.0)
    categoria = CategorizerService.categorize(mov, db)

    assert categoria == "Sin categorizar"
