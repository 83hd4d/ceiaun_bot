from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import settings


def get_new_sheet(title: str) -> Workbook:
    """
    Create new report from base excel template and return workbook.
    """

    workbook = load_workbook(filename=settings.EXCEL_BASE_TEMPLATE)
    sheet = workbook.active
    sheet["B1"] = title

    return workbook


def find_empty_row(sheet: Worksheet, start_row_number: int = 3) -> int:
    """
    Find empty row number and return it.

    Note: Start with row number 3 by default.
    """

    row_number = start_row_number
    while True:
        if sheet[f"A{row_number}"].value is None:
            return row_number

        row_number += 1


def write_data_to_sheet(title: str, data: list[list], columns: list) -> str:
    """
    Write data from first empty row of sheet and return file path.

    Example:
         >>> write_data_to_sheet("example title", [["data-1-a", "data-1-b"], ["data-2-a", "data-2-b"]], ["A", "B"])
    """

    workbook = get_new_sheet(title)
    sheet = workbook.active
    row_number = find_empty_row(sheet)

    for d in data:
        for i, column in enumerate(columns):
            try:
                sheet[f"{column}{row_number}"] = d[i]
            except IndexError:
                pass

        row_number += 1

    file_path = settings.EXCEL_GENERATED_FILES_DIR / f"{title}.xlsx"
    workbook.save(filename=file_path)

    return file_path
