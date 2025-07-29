
import pandas as pd
import re

def convertir_fecha(valor):
    """
    Convierte un valor a una fecha:
    - Si es número (float/int), lo interpreta como fecha de Excel.
    - Si es cadena, limpia caracteres y aplica dayfirst=True.
    - Devuelve NaT si no se puede convertir.
    """
    try:
        if isinstance(valor, (int, float)):
            return pd.to_datetime('1899-12-30') + pd.to_timedelta(valor, unit='D')
        elif isinstance(valor, str):
            valor = re.sub(r"[^\d/]", "", valor.strip())
            return pd.to_datetime(valor, dayfirst=True, errors='coerce')
    except:
        return pd.NaT
