import attr

from ..config import to_snake_case


@attr.s(slots=True)
class BoardFormatter:
    boards: dict = attr.ib()

    def format_keys(self) -> dict:
        """Formatea las llaves del diccionario a snake_case."""
        formatted_boards = {
            to_snake_case(key): value for key, value in self.boards.items()
        }
        return formatted_boards

    def format_columns(self) -> list[str]:
        """Formatea las columnas del diccionario."""

        for sheet_name, dataframe in self.boards.items():
            if dataframe.columns[0] == "Unnamed: 0":
                dataframe.columns = dataframe.iloc[0]
                dataframe = dataframe[1:].reset_index(drop=True)

            dataframe.columns = [to_snake_case(col) for col in dataframe.columns]

            self.boards[sheet_name] = dataframe

    def run(self):
        self.format_columns()
        return self.format_keys()
