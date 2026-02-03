import datetime as dt
import pandas as pd
import re
import unicodedata


# PATRON DE BUSQUEDA
REF_PATTERN = re.compile(r"ref\((\d+),\s*([a-zA-Z0-9_]+)\)", re.IGNORECASE)


MONTHS: list[str] = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def transform_date_string(date: str) -> str:
    """Ingresamos la fecha en formato string `yyyymm` y se retorna en formato `ene-yy`."""
    if len(date) != 6:
        return date

    year = date[:4]
    month = int(date[4:]) - 1
    return MONTHS[month][:3].lower() + "-" + year[2:]


def pattern_decryptor(pattern: str) -> list:
    """Busca las refencias haciendo uso del patrón usado dentro de las plantillas."""
    return REF_PATTERN.findall(pattern)


def build_context(df: pd.DataFrame) -> dict:
    """Convierte un dataframe a diccionario plano."""
    return {
        f"{row.clave}_{col}": row[col]
        for _, row in df.iterrows()
        for col in df.columns
        if col != "clave"
    }


def to_snake_case(text: str) -> str:
    """Convierte cadenas a snake_case, sin acentos ni caracteres especiales."""

    if isinstance(text, dt.datetime):
        return text.strftime("%Y%m")

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()
    text = re.sub(r"[\s\-]+", "_", text)
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-zA-Z0-9_]", "", text)

    return text.lower()
