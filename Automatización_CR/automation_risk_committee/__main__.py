import pandas as pd

from .config import PATH_CATALOG_KEYS, PATH_CONSOLIDATED
from .board_processing import BoardFiltering, BoardFormatter
from .template_manipulation import (
    ExcelTemplateProcessor,
    ExcelResultWriter,
)


def main(name_sheet: str, name_output: str, months_needed: dict[str, str]) -> None:

    boards = pd.read_excel(
        PATH_CONSOLIDATED + "Tableros Consolidados.xlsx", sheet_name=None
    )
    keys = pd.read_pickle(PATH_CATALOG_KEYS + "catalogo_claves.pkl")

    # ---------------------------------------------------------- LIMPIEZA DEL TABLERO CONSOLIDADO
    df = BoardFormatter(boards)
    data_boards = df.run()

    # ---------------------------------------------------------- INICIO DEL PROCESO
    xlsx_proces = ExcelTemplateProcessor(name_sheet, months_needed)
    output = xlsx_proces.run()

    bf = BoardFiltering(
        data_boards, keys, output["necessary_keys"], output["required_dates"]
    )
    context_data = bf.run()

    writer = ExcelResultWriter(
        output["workbook"], output["target_cells"], context_data, months_needed
    )
    writer.run(name_output)


if __name__ == "__main__":
    import time

    start = time.time()

    # ---------------------------------------------------------- INPUTS
    name_sheet = "plantilla_lamina_ccl_ref"
    name_output = "apoco_si_tilin"
    months_needed = {
        "dic_comparative": "202412",
        "previous_month": "202509",
        "current_month": "202510",
    }

    main(name_sheet, name_output, months_needed)

    print(
        f"""El proceso tardó {time.time() - start: .2f} segundos, que equivale a """
        f"""{(time.time() - start)/(60*60*24): .6f} dias.\nPodrías ejecutar el código"""
        f""" {365*24*60*60/(time.time() - start): ,.2f} veces en un año.\n"""
    )
