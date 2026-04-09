import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from src.models.movement import Movimiento, ImportBatch

class ParserService:
    """Parsea Excel/CSV → Movimientos en DB"""

    REQUIRED_COLUMNS = ['fecha', 'descripcion', 'monto']

    @staticmethod
    def parse_excel(file_bytes: bytes, filename: str, db: Session) -> ImportBatch:
        """
        Parse Excel file y crear Movimientos.

        Args:
            file_bytes: contenido del archivo
            filename: nombre del archivo
            db: sesión SQLAlchemy

        Returns:
            ImportBatch creado

        Raises:
            ValueError: si faltan columnas o error de parseo
        """
        try:
            df = pd.read_excel(BytesIO(file_bytes))

            # Validar columnas requeridas
            missing = [col for col in ParserService.REQUIRED_COLUMNS if col not in df.columns]
            if missing:
                raise ValueError(f"Faltan columnas: {missing}")

            # Crear batch
            batch = ImportBatch(
                nombre_archivo=filename,
                cantidad_movimientos=len(df)
            )
            db.add(batch)
            db.flush()

            # Crear movimientos
            for idx, row in df.iterrows():
                try:
                    mov = Movimiento(
                        fecha=pd.to_datetime(row['fecha']).date(),
                        descripcion=str(row['descripcion']).strip(),
                        monto=float(row['monto']),
                        categoria="Sin categorizar",
                        confianza=0.0
                    )
                    db.add(mov)
                except Exception as e:
                    raise ValueError(f"Error en fila {idx + 2}: {str(e)}")

            db.commit()
            return batch

        except Exception as e:
            db.rollback()
            raise ValueError(f"Parse error: {str(e)}")
