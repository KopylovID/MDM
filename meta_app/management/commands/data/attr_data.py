AttrData = [
    ("COLUMN_NAME", "Column_name", "Наименование колонки", "TEXT", "DB", None),
    ("DESCRIPTION", "Description", "Описание", "TEXT", "DB", {"attr_code_link": ["COLUMN_NAME"]}),
    ("UNIQUE", "Unique", "Уникальный ключ", "NULL", "DB", {"attr_code_link": ["COLUMN_NAME"]}),
    ("IS_SHOW", "Show", "Отобразить", "BOOL", "VIEW", {"attr_code_link": ["COLUMN_NAME"]}),
    ("DEFAULT", "Default", "Значение по умолчанию", "TEXT", "DB", {"attr_code_link": ["COLUMN_NAME"], "attr_type": None}),
    ("PLACEHOLDER", "Placeholder", "Текст при отображении элемента", "TEXT", "VIEW", {"attr_code_link": ["COLUMN_NAME"]}),
]
