"""
Инструмент для конвертации .txt файлов, содержащих HTML-разметку, в .html файлы.

Использование из консоли:
    python -m src.txt_to_html path/to/input.txt [-o path/to/output.html] [--title "Мой заголовок"]



from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional


def read_text_file(file_path: Path) -> str:
    """Читает текстовый файл, пробуя несколько типичных кодировок.

    Сначала пробуем UTF-8, затем CP1251 (актуально для Windows), затем ISO-8859-1 как последний шанс.
    Возвращает содержимое файла как строку.
    """
    encodings_to_try = ("utf-8", "cp1251", "iso-8859-1")
    last_error: Optional[Exception] = None
    for enc in encodings_to_try:
        try:
            return file_path.read_text(encoding=enc)
        except Exception as exc:  # noqa: BLE001 - осознанно логируем последнюю ошибку
            last_error = exc
            continue
    if last_error:
        raise last_error
    return ""


def looks_like_full_html(document: str) -> bool:
    """Грубая проверка, является ли текст полноценным HTML-документом."""
    lowered = document.strip().lower()
    return ("<html" in lowered) or ("<!doctype html" in lowered)


def ensure_html_document(html_fragment_or_document: str, title: str) -> str:
    """Возвращает полноценный HTML-документ.

    Если вход уже содержит <html> или <!doctype html>, возвращаем как есть.
    Иначе оборачиваем во внешний каркас с <head> и <meta charset>.
    """
    if looks_like_full_html(html_fragment_or_document):
        return html_fragment_or_document

    return (
        "<!doctype html>\n"
        "<html lang=\"ru\">\n"
        "<head>\n"
        "    <meta charset=\"utf-8\">\n"
        f"    <title>{title}</title>\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "    <style>body{margin:16px;font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif}</style>\n"
        "</head>\n"
        "<body>\n"
        f"{html_fragment_or_document}\n"
        "</body>\n"
        "</html>\n"
    )


def write_html_file(content: str, output_path: Path) -> None:
    """Сохраняет HTML содержимое в файл в UTF-8."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8", newline="\n")


def infer_output_path(input_path: Path) -> Path:
    """Формирует путь для выходного .html рядом со входным .txt."""
    if input_path.suffix.lower() == ".txt":
        return input_path.with_suffix(".html")
    return input_path.with_name(input_path.stem + ".html")


def convert_txt_html_to_html(input_file: Path, output_file: Optional[Path] = None, title: Optional[str] = None) -> Path:
    """Конвертирует .txt (с HTML внутри) в .html.

    Возвращает путь к созданному .html файлу.
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Файл не найден: {input_file}")

    raw_html = read_text_file(input_file)

    document_title = title if title else input_file.stem
    html_document = ensure_html_document(raw_html, title=document_title)

    target_path = output_file if output_file else infer_output_path(input_file)
    write_html_file(html_document, target_path)
    return target_path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="txt_to_html",
        description=(
            "Конвертация .txt файла, содержащего HTML-разметку, в .html. "
            "Если входной файл — фрагмент, он будет обёрнут в минимальный HTML-документ."
        ),
    )
    parser.add_argument("input", nargs="?", type=str, help="Путь к входному .txt файлу", default=None)
    parser.add_argument("-o", "--output", type=str, help="Путь к выходному .html файлу", default=None)
    parser.add_argument("--title", type=str, help="Заголовок HTML-документа (если нужно)", default=None)
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    # Поддержка запуска без аргументов: используем data/test.txt рядом с корнем проекта
    if args.input is None:
        default_input = Path(__file__).resolve().parents[1] / "data" / "test.txt"
        input_path = default_input
    else:
        input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    try:
        created = convert_txt_html_to_html(input_path, output_path, title=args.title)
        print(f"Готово: {created}")
    except Exception as exc:  # noqa: BLE001 - печатаем сообщение пользователю
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()


