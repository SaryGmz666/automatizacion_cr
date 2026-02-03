import attr

from ..config import PATH_OUTPUT, REF_PATTERN


@attr.s(slots=True)
class ExcelResultWriter:
    """Aplica el motor de evaluación sobre las celdas objetivo y escribe los resultados
    en la plantilla Excel sin modificar el formato original."""

    workbook = attr.ib()
    cell_positioning: list = attr.ib()
    context_data: dict[str, float] = attr.ib()
    months_needed: dict[str, str] = attr.ib()

    def _transform_formula(self, formula: str):
        refs = REF_PATTERN.findall(formula)
        transformed = formula
        missing = []

        for clave, period_token in refs:
            if period_token not in self.months_needed:
                missing.append(f"{clave}_{period_token} (periodo no definido)")
                continue

            yyyymm = self.months_needed[period_token]
            context_key = f"{clave}_{yyyymm}"

            value = self.context_data.get(context_key)

            if value is None or value == "":
                missing.append(context_key)
                continue

            transformed = transformed.replace(
                f"ref({clave},{period_token})", str(value)
            )

        return transformed, missing

    def process_cells(self):
        errors = []

        for cell in self.cell_positioning:
            original_value = cell.value

            try:
                transformed, missing = self._transform_formula(original_value)

                if missing:
                    print(
                        f"ADVERTENCIA: Celda {cell.coordinate}: valores no encontrados {missing}"
                    )
                    continue

                result = eval(transformed, {"__builtins__": {}}, {})

                cell.value = result

            except Exception as e:
                print(
                    f"ERROR: Celda {cell.coordinate}: no se pudo evaluar la fórmula. "
                    f"Se conserva el valor original."
                )
                cell.value = original_value

        return errors

    def save(self, output_name: str):
        path = f"{PATH_OUTPUT}{output_name}.xlsx"
        self.workbook.save(path)

    def run(self, output_name: str):
        self.process_cells()
        self.save(output_name)
