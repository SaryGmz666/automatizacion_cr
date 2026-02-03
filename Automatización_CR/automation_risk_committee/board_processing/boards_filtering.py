import attr
import pandas as pd
import warnings

from ..config import build_context

warnings.filterwarnings("ignore")


@attr.s(slots=True)
class BoardFiltering:
    boards: dict[str, pd.DataFrame] = attr.ib()
    catalog_keys: pd.DataFrame = attr.ib()
    necessary_keys: list[str] = attr.ib()
    required_dates: dict[str, str] = attr.ib()

    def get_matching_keys(self) -> list[str]:
        """Con las claves marcadas en el código, va abuscar coincidencias para localizar
        los tableros a los que hace referencia."""
        necessary_boards = list(
            self.catalog_keys[self.catalog_keys["c"].isin(self.necessary_keys)][
                "tablero"
            ].unique()
        )

        keys_not_located = [
            k for k in self.necessary_keys if k not in self.catalog_keys["c"].values
        ]
        if len(keys_not_located) > 0:
            print(
                "ADVERTENCIA: Las siguientes claves no se encontraron en el catálogo y "
                f"no serán consideradas en el procesamiento: {keys_not_located}."
            )

        return necessary_boards

    def data_filtering(self, necessary_boards: list[str]) -> dict:
        """Filtra los tableros necesarios por claves y fechas requeridas,
        y construye el contexto plano utilizado por el motor de evaluación."""
        context = {}

        for board in necessary_boards:
            board_select = self.boards[board]
            board_filter = board_select[["clave", *self.required_dates.values()]]

            # Aveces las claves no se leen como str, tons vamos a convertirlo por si acaso
            board_filter["clave"] = board_filter["clave"].astype(str)

            board_filter = board_filter[board_filter["clave"].isin(self.necessary_keys)]

            context.update(build_context(board_filter))

        return context

    def run(self):
        necessary_boards = self.get_matching_keys()
        return self.data_filtering(necessary_boards)
