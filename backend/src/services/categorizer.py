import math
from sqlalchemy.orm import Session
from src.models.movement import Movimiento, CascadaRule

class CategorizerService:
    """Motor cascada: aplica reglas + learning automático"""

    @staticmethod
    def categorize(movimiento: Movimiento, db: Session) -> str:
        """
        Aplica cascada de reglas a un movimiento.

        Busca en CascadaRule ordenadas por peso (mayor primero).
        Primera que coincida es la categoría.
        """
        desc = movimiento.descripcion.lower()

        # Obtener reglas activas, ordenadas por peso (DESC)
        rules = db.query(CascadaRule).filter(
            CascadaRule.activo == 1
        ).order_by(CascadaRule.peso.desc()).all()

        for rule in rules:
            if rule.patron.lower() in desc:
                movimiento.categoria = rule.categoria
                movimiento.confianza = rule.peso
                return rule.categoria

        movimiento.categoria = "Sin categorizar"
        movimiento.confianza = 0.0
        return "Sin categorizar"

    @staticmethod
    def save_rule(descripcion: str, categoria: str, confianza: float, db: Session) -> CascadaRule:
        """
        Guardar regla aprendida (usuario edita + marca 'Recordar').

        Extrae patrón normalizado y crea/actualiza regla.
        """
        patron = CategorizerService._extract_pattern(descripcion)

        # Verificar si ya existe
        existing = db.query(CascadaRule).filter(
            CascadaRule.patron == patron,
            CascadaRule.categoria == categoria
        ).first()

        if existing:
            # Aumentar uso
            existing.veces_usada += 1
            existing.peso = min(0.99, existing.peso + 0.05)
            db.commit()
            return existing
        else:
            # Crear nueva
            rule = CascadaRule(
                categoria=categoria,
                patron=patron,
                peso=confianza,
                veces_usada=1,
                activo=1
            )
            db.add(rule)
            db.commit()
            return rule

    @staticmethod
    def _extract_pattern(descripcion: str) -> str:
        """
        Normaliza descripción → patrón reutilizable.

        Ej: "Pago OSPACA Enero 2024" → "OSPACA"
        """
        words = descripcion.split()

        # Busca primer palabra >3 caracteres
        for word in words:
            clean_word = word.upper().strip('.,')
            if len(clean_word) > 3:
                return clean_word

        # Fallback: primeros 10 caracteres
        return descripcion.upper()[:10]

    @staticmethod
    def update_rule_usage(rule: CascadaRule, db: Session):
        """
        Cada vez que se aplica una regla → aumenta confianza.

        Usa factor logarítmico para evitar que converja a 1.0 rápido.
        """
        rule.veces_usada += 1

        # Confianza aumenta logarítmicamente
        # Factor: 1 + (0.5 / log(veces_usada + 2))
        factor = 1 + (0.5 / math.log(rule.veces_usada + 2))
        rule.peso = min(0.99, rule.peso * factor)

        db.commit()
