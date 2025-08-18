# -*- coding: utf-8 -*-
# Auto-converted from Jupyter Notebook to Python (.py)
# Source notebook: Html_parser.ipynb
# Converted: 2025-08-12T13:57:09
# Cell markers `# %%` preserve original cell boundaries.

# %%
"""
Модуль для парсинга HTML таблиц.
Содержит функции для извлечения табличных данных из HTML-документов
и сохранения их в различных форматах (DataFrame, Excel).
"""

# Импортируем необходимые библиотеки
import pandas as pd  # Для работы с табличными данными и Excel
from bs4 import BeautifulSoup  # Для парсинга HTML
import os  # Для работы с файловой системой

def parse_html_tables(source: str):
    """
    Парсит все HTML таблицы из указанного источника.
    
    Эта функция использует pandas.read_html() для автоматического извлечения
    всех таблиц из HTML-документа. Подходит для простых случаев, когда
    таблицы имеют стандартную структуру.

    Parameters
    ----------
    source : str
        HTML текст, путь к локальному файлу или URL-адрес.

    Returns
    -------
    list[pd.DataFrame]
        Список DataFrame'ов для каждой найденной таблицы.
        Если таблицы не найдены, возвращает пустой список.
    """
    try:
        # Используем pandas для автоматического парсинга всех таблиц
        tables = pd.read_html(source)
        return tables
    except ValueError:
        # Если таблицы не найдены, pandas выбросит ValueError
        print("⚠️ Таблицы не найдены в указанном источнике")
        return []


def parse_html_table(html: str, index: int = 0):
    """
    Парсит одну HTML таблицу с помощью BeautifulSoup.
    
    Эта функция предоставляет более детальный контроль над процессом парсинга
    и позволяет извлекать данные из таблиц со сложной структурой.
    Использует BeautifulSoup для ручного обхода DOM-дерева.

    Parameters
    ----------
    html : str
        HTML разметка, содержащая как минимум одну таблицу.
    index : int, optional
        Индекс таблицы для парсинга (по умолчанию 0 - первая таблица).

    Returns
    -------
    list[list[str]]
        Распарсенная таблица в виде списка строк с ячейками.
        Каждая строка представлена списком строковых значений ячеек.
    """
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Находим все элементы <table> в HTML
    tables = soup.find_all('table')
    
    # Проверяем, найдены ли таблицы и существует ли указанный индекс
    if not tables or index >= len(tables):
        print(f"⚠️ Таблица с индексом {index} не найдена")
        return []
    
    # Выбираем нужную таблицу по индексу
    table = tables[index]

    # Список для хранения всех строк таблицы
    rows: list[list[str]] = []
    
    # Проходим по всем строкам таблицы (<tr>)
    for tr in table.find_all('tr'):
        # Извлекаем текст из всех ячеек (как <td>, так и <th>)
        # strip=True удаляет лишние пробелы в начале и конце
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        
        # Добавляем строку только если в ней есть ячейки
        if cells:
            rows.append(cells)
    
    return rows


def main():
    """
   
    
    Эта функция выполняет полный цикл обработки:
    1. Определяет путь к файлу test.html
    2. Проверяет существование файла
    3. Читает HTML-контент
    4. Парсит таблицы двумя способами (BeautifulSoup и pandas)
    5. Сохраняет результаты в Excel-файл
    """
    # Получаем абсолютный путь к директории, где находится сам скрипт
    # Это позволяет работать с файлами относительно расположения скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Формируем путь к входному HTML-файлу в папке data (на уровень выше src)
    data_dir = os.path.abspath(os.path.join(script_dir, os.pardir, 'data'))
    html_file = os.path.join(data_dir, 'test.html')
    
    # Проверяем существование файла перед обработкой
    if not os.path.exists(html_file):
        print(f"❌ Файл {html_file} не найден!")
        print("Создайте файл data/test.html с HTML-кодом, содержащим таблицы.")
        return
    
    try:
        # Открываем HTML-файл для чтения с кодировкой UTF-8
        # Это обеспечивает корректное отображение русских символов
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Парсим таблицу с помощью BeautifulSoup (первый способ)
        print("🔍 Парсинг таблицы с помощью BeautifulSoup...")
        result = parse_html_table(html_content)
        
        if result:
            print(f"✅ Найдено {len(result)} строк в таблице")
            # Выводим первые несколько строк для проверки
            for i, row in enumerate(result[:3]):
                print(f"   Строка {i+1}: {row}")
        else:
            print("❌ Таблицы не найдены в HTML-файле.")

        # Парсинг с помощью pandas (второй способ)
        print("\n🔍 Парсинг таблиц с помощью pandas...")
        tables = pd.read_html(html_file)

        if tables:
            print(f"✅ Найдено {len(tables)} таблиц")
            
            # Формируем путь для сохранения Excel-файла в папке data
            output_excel_path = os.path.join(data_dir, "all_tables2.xlsx")
            
            # Создаем Excel-файл с несколькими листами (по одному на таблицу)
            with pd.ExcelWriter(output_excel_path, engine="openpyxl") as writer:
                for i, table in enumerate(tables):
                    # Сохраняем каждую таблицу на отдельный лист
                    # sheet_name=f"Table_{i+1}" - именуем листы как Table_1, Table_2, etc.
                    # index=False - не сохраняем индексы строк
                    table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
                    print(f"   Таблица {i+1}: {table.shape[0]} строк, {table.shape[1]} столбцов")
            
            print(f"✅ Файл Excel успешно сохранён: {output_excel_path}")
        else:
            print("❌ Таблицы не найдены в HTML-файле.")
            
    except Exception as e:
        # Обрабатываем любые ошибки, которые могут возникнуть
        print(f"❌ Ошибка при обработке файла: {e}")
        print("Проверьте, что файл содержит корректный HTML-код с таблицами")


# Точка входа в программу
# Код выполняется только при прямом запуске скрипта
if __name__ == "__main__":
    main()

# %%

# %%

# %%

# %%


