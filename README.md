# HTML Table Parser

Парсер для извлечения таблиц из HTML файлов и сохранения их в Excel формат.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Использование

1. Поместите HTML-файл с таблицами в папку `data/` под именем `test.html`.
2. Запустите скрипт:

```bash
python src/Html_parser.py
```

При необходимости вы можете изменить пути к входному и выходному файлам в `src/Html_parser.py` (переменные `data_dir`, `html_file`, `output_excel_path`).

## Функции

- `parse_html_tables(source)` — парсит все таблицы из HTML с помощью pandas
- `parse_html_table(html, index)` — парсит конкретную таблицу с помощью BeautifulSoup
- Автоматическое сохранение всех найденных таблиц в Excel-файл

## Результат

Скрипт создаст файл `data/all_tables2.xlsx` с отдельными листами для каждой найденной таблицы.

## Пример HTML структуры

```html
<table>
    <tr>
        <th>Заголовок 1</th>
        <th>Заголовок 2</th>
    </tr>
    <tr>
        <td>Данные 1</td>
        <td>Данные 2</td>
    </tr>
</table>
```
