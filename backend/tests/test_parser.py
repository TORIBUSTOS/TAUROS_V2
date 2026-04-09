import pytest
import pandas as pd
from io import BytesIO
from src.services.parser import ParserService
from src.models.movement import Movimiento

def test_parser_excel_valid(db):
    """Parser debe leer Excel y crear Movimientos"""
    # Crear Excel test
    df = pd.DataFrame({
        'fecha': ['2024-01-01', '2024-01-02'],
        'descripcion': ['OSPACA', 'Proveedores XYZ'],
        'monto': [1000.0, 500.0]
    })

    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    # Parse
    batch = ParserService.parse_excel(excel_bytes.getvalue(), "test.xlsx", db)

    # Validaciones
    assert batch.cantidad_movimientos == 2
    assert batch.nombre_archivo == "test.xlsx"

    movs = db.query(Movimiento).all()
    assert len(movs) == 2
    assert movs[0].descripcion == "OSPACA"
    assert movs[0].categoria == "Sin categorizar"
    assert movs[0].confianza == 0.0

def test_parser_missing_columns(db):
    """Parser debe rechazar Excel sin columnas requeridas"""
    df = pd.DataFrame({'fecha': ['2024-01-01']})
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    with pytest.raises(ValueError, match="Faltan columnas"):
        ParserService.parse_excel(excel_bytes.getvalue(), "bad.xlsx", db)

def test_parser_invalid_data_type(db):
    """Parser debe rechazar datos con tipos inválidos"""
    df = pd.DataFrame({
        'fecha': ['2024-01-01'],
        'descripcion': ['Test'],
        'monto': ['no es número']
    })
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    with pytest.raises(ValueError):
        ParserService.parse_excel(excel_bytes.getvalue(), "bad.xlsx", db)

def test_parser_strips_whitespace(db):
    """Parser debe trimear espacios en descripciones"""
    df = pd.DataFrame({
        'fecha': ['2024-01-01'],
        'descripcion': ['  OSPACA  '],
        'monto': [1000.0]
    })
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    batch = ParserService.parse_excel(excel_bytes.getvalue(), "test.xlsx", db)
    mov = db.query(Movimiento).first()

    assert mov.descripcion == "OSPACA"
    assert mov.descripcion != "  OSPACA  "
