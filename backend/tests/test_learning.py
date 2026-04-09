import pytest
from src.services.categorizer import CategorizerService
from src.models.movement import Movimiento, CascadaRule

def test_user_remembers_rule(db):
    """Usuario edita + 'Recordar' → nueva regla guardada"""
    # Crear movimiento
    mov = Movimiento(
        fecha="2024-01-01",
        descripcion="Pago OSPACA Enero",
        monto=1000.0,
        categoria="Sin categorizar"
    )
    db.add(mov)
    db.commit()

    # Usuario marca "Recordar regla"
    rule = CategorizerService.save_rule(
        descripcion="Pago OSPACA Enero",
        categoria="Obra Social",
        confianza=0.95,
        db=db
    )

    # Verificar que regla existe
    stored = db.query(CascadaRule).filter_by(
        patron="OSPACA",
        categoria="Obra Social"
    ).first()

    assert stored is not None
    assert stored.peso == 0.95
    assert stored.veces_usada == 1
    assert rule.id == stored.id

def test_rule_increases_on_reuse(db):
    """Guardar la misma regla 2 veces → aumenta uso + confianza"""
    # Primera vez
    rule1 = CategorizerService.save_rule(
        descripcion="Pago OSPACA",
        categoria="Obra Social",
        confianza=0.80,
        db=db
    )

    # Segunda vez (mismo patrón + categoría)
    rule2 = CategorizerService.save_rule(
        descripcion="OSPACA Payment",
        categoria="Obra Social",
        confianza=0.85,
        db=db
    )

    # Debe ser la misma regla
    assert rule1.id == rule2.id
    assert rule2.veces_usada == 2
    assert rule2.peso > 0.80  # Aumentó

def test_extract_pattern_gets_first_word(db):
    """_extract_pattern debe sacar primer palabra >3 chars"""
    tests = [
        ("Pago OSPACA Enero", "OSPACA"),
        ("ABC OSPACA", "OSPACA"),  # ABC es <3, salta
        ("Xyz Abc OSPACA", "OSPACA"),
        ("OSPACA 123", "OSPACA"),
    ]

    for desc, expected in tests:
        pattern = CategorizerService._extract_pattern(desc)
        assert pattern == expected, f"Failed for: {desc}"

def test_update_rule_usage_increases_confidence(db):
    """update_rule_usage debe aumentar confianza logarítmicamente"""
    rule = CascadaRule(
        categoria="Test",
        patron="TEST",
        peso=0.50,
        veces_usada=1,
        activo=1
    )
    db.add(rule)
    db.commit()

    initial_peso = rule.peso

    # Aumentar uso 5 veces
    for _ in range(5):
        CategorizerService.update_rule_usage(rule, db)
        db.refresh(rule)

    # Confianza debe ser mayor
    assert rule.peso > initial_peso
    assert rule.veces_usada == 6
    # Debe converger a ~0.95, no a 1.0
    assert rule.peso < 0.99

def test_save_rule_caps_confidence_at_99(db):
    """Confianza máxima debe ser 0.99, no 1.0"""
    # Crear regla con confianza baja
    rule = CategorizerService.save_rule(
        descripcion="Test",
        categoria="Test",
        confianza=0.50,
        db=db
    )

    # Incrementar muchas veces
    for _ in range(100):
        CategorizerService.update_rule_usage(rule, db)
        db.refresh(rule)

    # Nunca debe llegar a 1.0
    assert rule.peso < 0.99
    assert rule.peso >= 0.95
