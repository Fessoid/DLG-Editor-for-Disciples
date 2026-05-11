"""
DLG Editor for Disciples by Fessoid — визуальный редактор .dlg файлов.

Запуск:
    python dlg_editor.py [путь_к_файлу.dlg]
"""

import configparser
import os
import re
import sys
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage

# Название программы — единственное место, где оно задаётся.
APP_TITLE = "DLG Editor for Disciples"

# Путь к файлу настроек — лежит рядом с exe / скриптом.
SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "DLG_Editor_settings.ini"
)

# =============================================================================
# ЛОКАЛИЗАЦИЯ — все строки программы.
# Чтобы добавить или изменить текст, отредактируйте словари ниже.
# Ключ — внутренний идентификатор, значение — текст для пользователя.
# =============================================================================

# Контакты для окна «О программе». Формат: (название, URL).
# Для email используйте mailto: — программа автоматически откроет почтовый клиент.
ABOUT_LINKS = [
    ("Boosty",  "https://boosty.to/fessoid"),
    ("YouTube", "https://www.youtube.com/@Fessoid"),
    ("Steam",   "https://steamcommunity.com/id/fessoid/"),
    ("",        ""),                                         # пустая строка
    ("Github",  "https://github.com/Fessoid/DLG-Editor-for-Disciples/"),
    ("Email",   "mailto:fessoid@gmail.com"),
]

STRINGS = {
    "ru": {
        # --- Меню ---
        "menu_file":             "Файл",
        "menu_open":             "Открыть...",
        "menu_save":             "Сохранить",
        "menu_save_as":          "Сохранить как...",
        "menu_exit":             "Выход",
        "menu_language":         "Язык",
        "menu_lang_ru":          "Русский",
        "menu_lang_en":          "English",
        "menu_lang_pl":          "Polski",
        "menu_lang_zh":          "简体中文",
        "menu_about":            "О программе",

        # --- Левая панель ---
        "sections_label":        "Секции DIALOG:",

        # --- Статус ---
        "status_open_hint":      "Откройте .dlg файл (Ctrl+O)",
        "status_loaded":         "Загружено: {fname} — секций: {count}",
        "status_saved":          "Сохранено: {path}",

        # --- Правая панель ---
        "elements_label":        "Элементы:",
        "dialog_size_label":     "Размер окна DIALOG",
        "coord_label":           "Координаты выбранного элемента",
        "hints_label":           "Подсказки",
        "hint_text": (
            "• Клик по элементу — выделить\n"
            "• Тянуть за центр — переместить\n"
            "• Тянуть за край/угол — изменить размер\n"
            "• Тянуть правый/нижний край окна —\n"
            "  менять размер DIALOG\n"
            "• Ctrl+S — сохранить файл"
        ),
        "dlg_size_fixed":        "X1, Y1 = 0 (фиксировано)",
        "dlg_size_warn":         "Внимание: вторая пара = {w}×{h}, "
                                 "при сохранении будет синхронизирована.",

        # --- Кнопки ---
        "btn_save":              "Сохранить",
        "btn_revert":            "Отменить",

        # --- Диалоги ---
        "err_read_title":        "Ошибка чтения",
        "err_read_msg":          "Не удалось прочитать файл:\n{err}",
        "err_write_title":       "Ошибка записи",
        "err_write_msg":         "Не удалось сохранить:\n{err}",
        "unsaved_title":         "Несохранённые изменения",
        "unsaved_msg":           "В файле есть несохранённые изменения.\n"
                                 "Сохранить перед продолжением?",

        # --- О программе ---
        "about_title":           "О программе",
        "about_name":            APP_TITLE + " by Fessoid",
        "about_version":         "версия 1.1",
        "about_text": (
            "Визуальный редактор .dlg файлов для интерактивного\n"
            "изменения размеров и положения элементов интерфейса.\n"
            "Позволяет открыть файл, выбрать секцию DIALOG из\n"
            "списка, увидеть все элементы на холсте, перетаскивать\n"
            "и менять размеры мышью или вводить координаты вручную,\n"
            "после чего сохранить изменения обратно в файл\n"
            "с сохранением исходного синтаксиса."
        ),
    },
    "en": {
        # --- Menu ---
        "menu_file":             "File",
        "menu_open":             "Open...",
        "menu_save":             "Save",
        "menu_save_as":          "Save As...",
        "menu_exit":             "Exit",
        "menu_language":         "Language",
        "menu_lang_ru":          "Русский",
        "menu_lang_en":          "English",
        "menu_lang_pl":          "Polski",
        "menu_lang_zh":          "简体中文",
        "menu_about":            "About",

        # --- Left panel ---
        "sections_label":        "DIALOG Sections:",

        # --- Status ---
        "status_open_hint":      "Open a .dlg file (Ctrl+O)",
        "status_loaded":         "Loaded: {fname} — sections: {count}",
        "status_saved":          "Saved: {path}",

        # --- Right panel ---
        "elements_label":        "Elements:",
        "dialog_size_label":     "DIALOG Window Size",
        "coord_label":           "Selected Element Coordinates",
        "hints_label":           "Tips",
        "hint_text": (
            "• Click an element to select it\n"
            "• Drag from center to move\n"
            "• Drag edge/corner to resize\n"
            "• Drag right/bottom edge of window\n"
            "  to resize DIALOG\n"
            "• Ctrl+S to save file"
        ),
        "dlg_size_fixed":        "X1, Y1 = 0 (fixed)",
        "dlg_size_warn":         "Warning: second pair = {w}×{h}, "
                                 "will be synced on save.",

        # --- Buttons ---
        "btn_save":              "Save",
        "btn_revert":            "Revert",

        # --- Dialogs ---
        "err_read_title":        "Read Error",
        "err_read_msg":          "Could not read file:\n{err}",
        "err_write_title":       "Write Error",
        "err_write_msg":         "Could not save file:\n{err}",
        "unsaved_title":         "Unsaved Changes",
        "unsaved_msg":           "There are unsaved changes.\n"
                                 "Save before continuing?",

        # --- About ---
        "about_title":           "About",
        "about_name":            APP_TITLE + " by Fessoid",
        "about_version":         "version 1.1",
        "about_text": (
            "A visual editor for .dlg files that lets you\n"
            "interactively change positions and sizes of\n"
            "interface elements. Open a file, pick a DIALOG\n"
            "section from the list, see all elements on the\n"
            "canvas, drag and resize them or type coordinates\n"
            "manually, then save changes back to the file\n"
            "preserving the original syntax."
        ),
    },
    "pl": {
        # --- Menu ---
        "menu_file":             "Plik",
        "menu_open":             "Otwórz...",
        "menu_save":             "Zapisz",
        "menu_save_as":          "Zapisz jako...",
        "menu_exit":             "Wyjście",
        "menu_language":         "Język",
        "menu_lang_ru":          "Русский",
        "menu_lang_en":          "English",
        "menu_lang_pl":          "Polski",
        "menu_lang_zh":          "简体中文",
        "menu_about":            "O programie",

        # --- Left panel ---
        "sections_label":        "Sekcje DIALOG:",

        # --- Status ---
        "status_open_hint":      "Otwórz plik .dlg (Ctrl+O)",
        "status_loaded":         "Wczytano: {fname} — sekcji: {count}",
        "status_saved":          "Zapisano: {path}",

        # --- Right panel ---
        "elements_label":        "Elementy:",
        "dialog_size_label":     "Rozmiar okna DIALOG",
        "coord_label":           "Współrzędne wybranego elementu",
        "hints_label":           "Wskazówki",
        "hint_text": (
            "• Kliknij element, aby go wybrać\n"
            "• Przeciągnij ze środka, aby przesunąć\n"
            "• Przeciągnij krawędź/róg, aby zmienić rozmiar\n"
            "• Przeciągnij prawą/dolną krawędź okna,\n"
            "  aby zmienić rozmiar DIALOG\n"
            "• Ctrl+S — zapisz plik"
        ),
        "dlg_size_fixed":        "X1, Y1 = 0 (stałe)",
        "dlg_size_warn":         "Uwaga: druga para = {w}×{h}, "
                                 "zostanie zsynchronizowana przy zapisie.",

        # --- Buttons ---
        "btn_save":              "Zapisz",
        "btn_revert":            "Cofnij",

        # --- Dialogs ---
        "err_read_title":        "Błąd odczytu",
        "err_read_msg":          "Nie udało się odczytać pliku:\n{err}",
        "err_write_title":       "Błąd zapisu",
        "err_write_msg":         "Nie udało się zapisać pliku:\n{err}",
        "unsaved_title":         "Niezapisane zmiany",
        "unsaved_msg":           "Plik zawiera niezapisane zmiany.\n"
                                 "Zapisać przed kontynuacją?",

        # --- About ---
        "about_title":           "O programie",
        "about_name":            APP_TITLE + " by Fessoid",
        "about_version":         "wersja 1.1",
        "about_text": (
            "Edytor wizualny plików .dlg do interaktywnej\n"
            "zmiany rozmiarów i pozycji elementów interfejsu.\n"
            "Otwórz plik, wybierz sekcję DIALOG z listy,\n"
            "zobacz elementy na płótnie, przeciągaj i zmieniaj\n"
            "rozmiary myszą lub wpisuj współrzędne ręcznie,\n"
            "a następnie zapisz zmiany z zachowaniem\n"
            "oryginalnej składni."
        ),
    },
    "zh": {
        # --- 菜单 ---
        "menu_file":             "文件",
        "menu_open":             "打开...",
        "menu_save":             "保存",
        "menu_save_as":          "另存为...",
        "menu_exit":             "退出",
        "menu_language":         "语言",
        "menu_lang_ru":          "Русский",
        "menu_lang_en":          "English",
        "menu_lang_pl":          "Polski",
        "menu_lang_zh":          "简体中文",
        "menu_about":            "关于",

        # --- 左面板 ---
        "sections_label":        "DIALOG 区段：",

        # --- 状态 ---
        "status_open_hint":      "请打开 .dlg 文件（Ctrl+O）",
        "status_loaded":         "已加载：{fname} — 区段数：{count}",
        "status_saved":          "已保存：{path}",

        # --- 右面板 ---
        "elements_label":        "元素：",
        "dialog_size_label":     "DIALOG 窗口尺寸",
        "coord_label":           "所选元素坐标",
        "hints_label":           "提示",
        "hint_text": (
            "• 单击元素以选中\n"
            "• 从中心拖动以移动\n"
            "• 拖动边缘/角以调整大小\n"
            "• 拖动窗口的右/下边缘\n"
            "  以调整 DIALOG 大小\n"
            "• Ctrl+S 保存文件"
        ),
        "dlg_size_fixed":        "X1、Y1 = 0（固定）",
        "dlg_size_warn":         "注意：第二组值 = {w}×{h}，"
                                 "保存时将自动同步。",

        # --- 按钮 ---
        "btn_save":              "保存",
        "btn_revert":            "撤销",

        # --- 对话框 ---
        "err_read_title":        "读取错误",
        "err_read_msg":          "无法读取文件：\n{err}",
        "err_write_title":       "写入错误",
        "err_write_msg":         "无法保存文件：\n{err}",
        "unsaved_title":         "未保存的更改",
        "unsaved_msg":           "文件中有未保存的更改。\n"
                                 "是否在继续之前保存？",

        # --- 关于 ---
        "about_title":           "关于",
        "about_name":            APP_TITLE + " by Fessoid",
        "about_version":         "版本 1.1",
        "about_text": (
            "用于 .dlg 文件的可视化编辑器，可交互式地\n"
            "更改界面元素的大小和位置。打开文件后从列表\n"
            "中选择 DIALOG 区段，在画布上查看所有元素，\n"
            "通过鼠标拖拽或手动输入坐标来调整，然后将\n"
            "更改保存回文件，同时保留原始语法。"
        ),
    },
}

# =============================================================================
# ПАРСИНГ ФАЙЛА
# =============================================================================

ELEMENT_TYPES = {
    "BUTTONSD", "EDIT", "IMAGE", "LBOX", "RADIO", "SCROLL",
    "SPIN", "TEXT", "TLBOX", "TOGGLE", "TOGGLESD",
}

COLOR_BG_WINDOW    = "#c8c0b0"
COLOR_BG_APP       = "#d4d0c8"
COLOR_BORDER_DARK  = "#404040"
COLOR_BORDER_MED   = "#808080"
COLOR_BORDER_LIGHT = "#ffffff"
COLOR_INPUT_BG     = "#ffffff"
COLOR_BUTTON_BG    = "#d4d0c8"
COLOR_TEXT         = "#000000"
COLOR_TEXT_MUTED   = "#606060"
COLOR_SELECTION    = "#0a64a4"
COLOR_DIALOG_FRAME = "#000000"
COLOR_WARN         = "#a04020"


class DlgElement:
    def __init__(self, line_index, raw_line, kind, name, x1, y1, x2, y2,
                 prefix, suffix):
        self.line_index = line_index
        self.raw_line = raw_line
        self.kind = kind
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.prefix = prefix
        self.suffix = suffix


class DlgSection:
    def __init__(self, name, header_line_index, header_raw,
                 x1, y1, x2, y2, w2, h2,
                 prefix, middle, tail,
                 begin_line_index, end_line_index):
        self.name = name
        self.header_line_index = header_line_index
        self.header_raw = header_raw
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.w2 = w2
        self.h2 = h2
        self.header_prefix = prefix
        self.header_middle = middle
        self.header_tail = tail
        self.begin_line_index = begin_line_index
        self.end_line_index = end_line_index
        self.elements = []


_ELEMENT_RE = re.compile(
    r"^(?P<prefix>\s+(?P<kind>[A-Z]+)\s+(?P<n>[A-Za-z0-9_]+),)"
    r"(?P<x1>-?\d+),(?P<y1>-?\d+),(?P<x2>-?\d+),(?P<y2>-?\d+)"
    r"(?P<suffix>.*)$"
)

_DIALOG_RE = re.compile(
    r"^(?P<prefix>DIALOG\s+(?P<n>[A-Za-z0-9_]+),)"
    r"(?P<x1>-?\d+),(?P<y1>-?\d+),(?P<x2>-?\d+),(?P<y2>-?\d+)"
    r"(?P<middle>,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,)"
    r"(?P<w2>-?\d+),(?P<h2>-?\d+)"
    r"(?P<tail>.*)$"
)


def parse_dlg_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    line_ending = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("cp1252", errors="replace")
    lines = text.split(line_ending)
    sections = []
    current = None
    in_body = False
    for i, line in enumerate(lines):
        if not in_body:
            m = _DIALOG_RE.match(line)
            if m:
                current = DlgSection(
                    name=m.group("n"), header_line_index=i, header_raw=line,
                    x1=int(m.group("x1")), y1=int(m.group("y1")),
                    x2=int(m.group("x2")), y2=int(m.group("y2")),
                    w2=int(m.group("w2")), h2=int(m.group("h2")),
                    prefix=m.group("prefix"), middle=m.group("middle"),
                    tail=m.group("tail"),
                    begin_line_index=-1, end_line_index=-1,
                )
                continue
            if current is not None and line.strip().upper() == "BEGIN":
                current.begin_line_index = i
                in_body = True
                continue
        else:
            if line.strip().upper() == "END":
                current.end_line_index = i
                sections.append(current)
                current = None
                in_body = False
                continue
            m = _ELEMENT_RE.match(line)
            if m and m.group("kind") in ELEMENT_TYPES:
                el = DlgElement(
                    line_index=i, raw_line=line,
                    kind=m.group("kind"), name=m.group("n"),
                    x1=int(m.group("x1")), y1=int(m.group("y1")),
                    x2=int(m.group("x2")), y2=int(m.group("y2")),
                    prefix=m.group("prefix"), suffix=m.group("suffix"),
                )
                current.elements.append(el)
    return lines, sections, line_ending


def write_dlg_file(path, lines, sections, line_ending):
    out_lines = list(lines)
    for section in sections:
        out_lines[section.header_line_index] = (
            f"{section.header_prefix}"
            f"{section.x1},{section.y1},{section.x2},{section.y2}"
            f"{section.header_middle}"
            f"{section.w2},{section.h2}"
            f"{section.header_tail}"
        )
        for el in section.elements:
            out_lines[el.line_index] = (
                f"{el.prefix}{el.x1},{el.y1},{el.x2},{el.y2}{el.suffix}"
            )
    text = line_ending.join(out_lines)
    with open(path, "wb") as f:
        f.write(text.encode("cp1252", errors="replace"))


# =============================================================================
# GUI
# =============================================================================

CANVAS_W = 800
CANVAS_H = 600
HANDLE_SIZE = 6

HIT_NONE = 0
HIT_INSIDE = 1
HIT_L = 2
HIT_R = 4
HIT_T = 8
HIT_B = 16
HIT_DIALOG = "dialog"


class DlgEditorApp:
    def __init__(self, root, initial_path=None):
        self.root = root
        self.root.geometry("1320x780")
        self.root.minsize(900, 500)
        self.root.configure(bg=COLOR_BG_APP)

        self.lang = "ru"
        self.file_path = None
        self.lines = []
        self.sections = []
        self.line_ending = "\r\n"
        self.current_section = None
        self.selected_element = None
        self.dirty = False

        self.drag_target = None
        self.drag_mode = HIT_NONE
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_orig = None

        self.element_to_rect = {}
        self.dialog_rect_id = None

        # Загружаем настройки до построения UI, чтобы язык был сразу верным.
        saved_lang, saved_file, saved_maximized, saved_section = self._load_settings()
        if saved_lang and saved_lang in STRINGS:
            self.lang = saved_lang

        self._setup_styles()
        self._build_ui()
        self._bind_shortcuts()
        self._apply_language()

        if saved_maximized:
            self.root.state("zoomed")

        # Приоритет: аргумент командной строки > сохранённый файл.
        open_path = initial_path if initial_path else saved_file
        if open_path and os.path.isfile(open_path):
            self._open_file(open_path)
            if saved_section and not initial_path:
                self._select_section_by_name(saved_section)

    def t(self, key, **kw):
        s = STRINGS.get(self.lang, STRINGS["en"]).get(key, key)
        if kw:
            s = s.format(**kw)
        return s

    # --- Settings ----------------------------------------------------------

    def _load_settings(self):
        """Читает settings.ini, возвращает (lang, last_file, maximized, last_section)."""
        cfg = configparser.ConfigParser()
        try:
            cfg.read(SETTINGS_PATH, encoding="utf-8")
            lang = cfg.get("General", "language", fallback=None)
            last_file = cfg.get("General", "last_file", fallback=None)
            maximized = cfg.get("General", "maximized", fallback="0")
            last_section = cfg.get("General", "last_section", fallback=None)
            return lang, last_file, maximized == "1", last_section
        except Exception:
            return None, None, False, None

    def _save_settings(self):
        """Записывает текущие настройки в settings.ini."""
        cfg = configparser.ConfigParser()
        cfg["General"] = {
            "language": self.lang,
            "last_file": self.file_path or "",
            "maximized": "1" if self.root.state() == "zoomed" else "0",
            "last_section": self.current_section.name if self.current_section else "",
        }
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                cfg.write(f)
        except Exception:
            pass  # не критично — если не получилось записать, работаем дальше

    # --- Style -------------------------------------------------------------

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=COLOR_BG_APP, foreground=COLOR_TEXT,
                        fieldbackground=COLOR_INPUT_BG)
        style.configure("TFrame", background=COLOR_BG_APP)
        style.configure("TLabel", background=COLOR_BG_APP, foreground=COLOR_TEXT)
        style.configure("TLabelframe", background=COLOR_BG_APP,
                        foreground=COLOR_TEXT)
        style.configure("TLabelframe.Label", background=COLOR_BG_APP,
                        foreground=COLOR_TEXT)
        style.configure("TEntry", fieldbackground=COLOR_INPUT_BG,
                        foreground=COLOR_TEXT)
        style.configure("Treeview", background=COLOR_INPUT_BG,
                        fieldbackground=COLOR_INPUT_BG, foreground=COLOR_TEXT)
        style.configure("Treeview.Heading", background=COLOR_BG_APP,
                        foreground=COLOR_TEXT)
        style.configure("TButton", background=COLOR_BG_APP,
                        foreground=COLOR_TEXT)
        # Цветные кнопки.
        style.configure("Save.TButton",
                        background="#64DF85", foreground=COLOR_TEXT)
        style.map("Save.TButton",
                  background=[("active", "#50C870"), ("pressed", "#40B860")])
        style.configure("Revert.TButton",
                        background="#FFDF40", foreground=COLOR_TEXT)
        style.map("Revert.TButton",
                  background=[("active", "#E8CC38"), ("pressed", "#D4BA30")])

    # --- UI build ----------------------------------------------------------

    def _build_ui(self):
        self._build_menu()

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=0, minsize=240)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=0, minsize=320)
        main.rowconfigure(0, weight=1)

        # --- Левая колонка ---
        left = ttk.Frame(main, padding=4)
        left.grid(row=0, column=0, sticky="nsew")
        left.rowconfigure(3, weight=1)
        left.columnconfigure(0, weight=1)

        self.lbl_sections = ttk.Label(left, text="...")
        self.lbl_sections.grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write",
                                   lambda *a: self._refresh_section_list())
        ttk.Entry(left, textvariable=self.search_var).grid(
            row=1, column=0, sticky="ew", pady=(2, 4))

        # --- Фильтры по размеру ---
        filter_frame = ttk.Frame(left)
        filter_frame.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        filter_frame.columnconfigure(1, weight=1)

        ttk.Label(filter_frame, text="W").grid(row=0, column=0, padx=(0, 2))
        self.filter_w_op = tk.StringVar(value="—")
        self.filter_w_val = tk.StringVar(value="")
        ttk.Combobox(filter_frame, textvariable=self.filter_w_op,
                     values=["—", "=", ">", ">=", "<", "<="],
                     width=3, state="readonly").grid(row=0, column=1, padx=2)
        ttk.Entry(filter_frame, textvariable=self.filter_w_val,
                  width=5, justify="right").grid(row=0, column=2, padx=(2, 0))

        ttk.Label(filter_frame, text="H").grid(row=1, column=0, padx=(0, 2),
                                                pady=(2, 0))
        self.filter_h_op = tk.StringVar(value="—")
        self.filter_h_val = tk.StringVar(value="")
        ttk.Combobox(filter_frame, textvariable=self.filter_h_op,
                     values=["—", "=", ">", ">=", "<", "<="],
                     width=3, state="readonly").grid(row=1, column=1, padx=2,
                                                      pady=(2, 0))
        ttk.Entry(filter_frame, textvariable=self.filter_h_val,
                  width=5, justify="right").grid(row=1, column=2, padx=(2, 0),
                                                  pady=(2, 0))

        for var in (self.filter_w_op, self.filter_w_val,
                    self.filter_h_op, self.filter_h_val):
            var.trace_add("write", lambda *a: self._refresh_section_list())

        self.section_listbox = tk.Listbox(
            left, exportselection=False, activestyle="dotbox",
            bg=COLOR_INPUT_BG, fg=COLOR_TEXT,
            selectbackground=COLOR_SELECTION, selectforeground="#ffffff",
            highlightthickness=1, highlightbackground=COLOR_BORDER_DARK,
            relief="flat", borderwidth=0,
        )
        self.section_listbox.grid(row=3, column=0, sticky="nsew")
        sb = ttk.Scrollbar(left, orient="vertical",
                           command=self.section_listbox.yview)
        sb.grid(row=3, column=1, sticky="ns")
        self.section_listbox.config(yscrollcommand=sb.set)
        self.section_listbox.bind("<<ListboxSelect>>", self._on_section_select)

        # --- Центральная колонка: canvas ---
        center = ttk.Frame(main, padding=4)
        center.grid(row=0, column=1, sticky="nsew")
        center.rowconfigure(1, weight=1)
        center.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="...")
        ttk.Label(center, textvariable=self.status_var,
                  foreground=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w")

        canvas_frame = ttk.Frame(center)
        canvas_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 0))
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            canvas_frame, bg=COLOR_BG_APP, highlightthickness=0, bd=0,
            scrollregion=(0, 0, CANVAS_W, CANVAS_H),
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal",
                                       command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical",
                                       command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(xscrollcommand=self.h_scroll.set,
                               yscrollcommand=self.v_scroll.set)

        self.canvas.bind("<Motion>", self._on_canvas_motion)
        self.canvas.bind("<ButtonPress-1>", self._on_canvas_press)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

        # --- Правая колонка ---
        right = ttk.Frame(main, padding=4)
        right.grid(row=0, column=2, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        self.lbl_elements = ttk.Label(right, text="...")
        self.lbl_elements.grid(row=0, column=0, sticky="w")
        list_frame = ttk.Frame(right)
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 4))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        cols = ("kind", "name", "x1", "y1", "x2", "y2")
        self.element_tree = ttk.Treeview(list_frame, columns=cols,
                                         show="headings", height=14)
        for col, w in zip(cols, (70, 140, 40, 40, 40, 40)):
            self.element_tree.heading(col, text=col.upper())
            self.element_tree.column(col, width=w, anchor="w" if col in
                                     ("kind", "name") else "e")
        self.element_tree.grid(row=0, column=0, sticky="nsew")
        et_sb = ttk.Scrollbar(list_frame, orient="vertical",
                              command=self.element_tree.yview)
        et_sb.grid(row=0, column=1, sticky="ns")
        self.element_tree.config(yscrollcommand=et_sb.set)
        self.element_tree.bind("<<TreeviewSelect>>",
                                self._on_element_tree_select)

        # Размер DIALOG.
        self.win_box = ttk.LabelFrame(right, text="...")
        self.win_box.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        for c in range(2):
            self.win_box.columnconfigure(c, weight=1)
        ttk.Label(self.win_box, text="Width").grid(row=0, column=0, padx=2,
                                                    pady=2)
        ttk.Label(self.win_box, text="Height").grid(row=0, column=1, padx=2,
                                                     pady=2)
        self.dlg_w_var = tk.IntVar(value=0)
        self.dlg_h_var = tk.IntVar(value=0)
        e_w = ttk.Entry(self.win_box, textvariable=self.dlg_w_var, width=8,
                        justify="right")
        e_h = ttk.Entry(self.win_box, textvariable=self.dlg_h_var, width=8,
                        justify="right")
        e_w.grid(row=1, column=0, padx=2, pady=(0, 2), sticky="ew")
        e_h.grid(row=1, column=1, padx=2, pady=(0, 2), sticky="ew")
        for e in (e_w, e_h):
            e.bind("<Return>", lambda _ev: self._apply_dialog_size())
            e.bind("<FocusOut>", lambda _ev: self._apply_dialog_size())
        self.dlg_size_hint = ttk.Label(self.win_box, text="...",
                                        foreground=COLOR_TEXT_MUTED)
        self.dlg_size_hint.grid(row=2, column=0, columnspan=2, padx=2,
                                 pady=(0, 4), sticky="w")

        # Координаты элемента.
        self.coord_box = ttk.LabelFrame(right, text="...")
        self.coord_box.grid(row=3, column=0, sticky="ew", pady=(0, 4))
        for c in range(4):
            self.coord_box.columnconfigure(c, weight=1)
        self.coord_vars = {}
        for i, label in enumerate(("X1", "Y1", "X2", "Y2")):
            ttk.Label(self.coord_box, text=label).grid(row=0, column=i,
                                                        padx=2, pady=2)
            v = tk.IntVar(value=0)
            e = ttk.Entry(self.coord_box, textvariable=v, width=6,
                          justify="right")
            e.grid(row=1, column=i, padx=2, pady=(0, 4), sticky="ew")
            e.bind("<Return>", lambda _ev: self._apply_coord_entries())
            e.bind("<FocusOut>", lambda _ev: self._apply_coord_entries())
            self.coord_vars[label] = v

        # Подсказки.
        self.hints_box = ttk.LabelFrame(right, text="...")
        self.hints_box.grid(row=4, column=0, sticky="ew")
        self.lbl_hints = ttk.Label(self.hints_box, justify="left", text="...")
        self.lbl_hints.pack(anchor="w", padx=4, pady=4)

        # Кнопки.
        btn_frame = ttk.Frame(right)
        btn_frame.grid(row=5, column=0, sticky="ew", pady=(6, 0))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.btn_save = ttk.Button(btn_frame, text="...",
                                    command=self.cmd_save,
                                    style="Save.TButton")
        self.btn_save.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        self.btn_revert = ttk.Button(btn_frame, text="...",
                                      command=self.cmd_revert,
                                      style="Revert.TButton")
        self.btn_revert.grid(row=0, column=1, sticky="ew", padx=(3, 0))

    # --- Language ----------------------------------------------------------

    def _set_language(self, lang):
        if lang == self.lang:
            return
        self.lang = lang
        self._apply_language()
        self._save_settings()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=self.t("menu_open"), command=self.cmd_open,
                              accelerator="Ctrl+O")
        filemenu.add_command(label=self.t("menu_save"), command=self.cmd_save,
                              accelerator="Ctrl+S")
        filemenu.add_command(label=self.t("menu_save_as"),
                              command=self.cmd_save_as)
        filemenu.add_separator()
        filemenu.add_command(label=self.t("menu_exit"), command=self.cmd_exit)
        menubar.add_cascade(label=self.t("menu_file"), menu=filemenu)

        langmenu = tk.Menu(menubar, tearoff=0)
        langmenu.add_command(label=self.t("menu_lang_ru"),
                              command=lambda: self._set_language("ru"))
        langmenu.add_command(label=self.t("menu_lang_en"),
                              command=lambda: self._set_language("en"))
        langmenu.add_command(label=self.t("menu_lang_pl"),
                              command=lambda: self._set_language("pl"))
        langmenu.add_command(label=self.t("menu_lang_zh"),
                              command=lambda: self._set_language("zh"))
        menubar.add_cascade(label=self.t("menu_language"), menu=langmenu)

        menubar.add_command(label=self.t("menu_about"), command=self.cmd_about)
        self.root.config(menu=menubar)

    def _apply_language(self):
        self._update_title()
        self._build_menu()
        self.lbl_sections.config(text=self.t("sections_label"))
        self.lbl_elements.config(text=self.t("elements_label"))
        self.win_box.config(text=self.t("dialog_size_label"))
        self.coord_box.config(text=self.t("coord_label"))
        self.hints_box.config(text=self.t("hints_label"))
        self.lbl_hints.config(text=self.t("hint_text"))
        self.btn_save.config(text=self.t("btn_save"))
        self.btn_revert.config(text=self.t("btn_revert"))
        if not self.file_path:
            self.status_var.set(self.t("status_open_hint"))
        self._update_dialog_size_entries()

    # --- Shortcuts ---------------------------------------------------------

    def _bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda _e: self.cmd_open())
        self.root.bind("<Control-O>", lambda _e: self.cmd_open())
        self.root.bind("<Control-s>", lambda _e: self.cmd_save())
        self.root.bind("<Control-S>", lambda _e: self.cmd_save())
        self.root.protocol("WM_DELETE_WINDOW", self.cmd_exit)

    # --- File commands -----------------------------------------------------

    def cmd_open(self):
        if not self._confirm_discard_changes():
            return
        path = filedialog.askopenfilename(
            title=self.t("menu_open"),
            filetypes=[("DLG files", "*.dlg"), ("All files", "*.*")],
        )
        if path:
            self._open_file(path)

    def _open_file(self, path):
        try:
            lines, sections, line_ending = parse_dlg_file(path)
        except Exception as exc:
            messagebox.showerror(self.t("err_read_title"),
                                  self.t("err_read_msg", err=exc))
            return
        self.file_path = path
        self.lines = lines
        self.sections = sections
        self.line_ending = line_ending
        self.current_section = None
        self.selected_element = None
        self.dirty = False
        self._update_title()
        self._refresh_section_list()
        self._clear_canvas()
        self._refresh_element_list()
        self._update_coord_entries()
        self._update_dialog_size_entries()
        self.status_var.set(
            self.t("status_loaded",
                   fname=os.path.basename(path), count=len(sections)))
        self._save_settings()

    def cmd_save(self):
        if not self.file_path:
            return self.cmd_save_as()
        try:
            write_dlg_file(self.file_path, self.lines, self.sections,
                           self.line_ending)
        except Exception as exc:
            messagebox.showerror(self.t("err_write_title"),
                                  self.t("err_write_msg", err=exc))
            return
        self.dirty = False
        self._update_title()
        self.status_var.set(self.t("status_saved", path=self.file_path))

    def cmd_save_as(self):
        if not self.sections:
            return
        path = filedialog.asksaveasfilename(
            title=self.t("menu_save_as"), defaultextension=".dlg",
            filetypes=[("DLG files", "*.dlg"), ("All files", "*.*")],
        )
        if not path:
            return
        self.file_path = path
        self.cmd_save()

    def cmd_revert(self):
        if not self.file_path:
            return
        old_section_name = (self.current_section.name
                            if self.current_section else None)
        self._open_file(self.file_path)
        if old_section_name:
            for i, s in enumerate(self._filtered_sections):
                if s.name == old_section_name:
                    self.section_listbox.selection_clear(0, tk.END)
                    self.section_listbox.selection_set(i)
                    self.section_listbox.see(i)
                    self.current_section = s
                    self._draw_section()
                    self._refresh_element_list()
                    self._update_coord_entries()
                    self._update_dialog_size_entries()
                    break

    def cmd_exit(self):
        if not self._confirm_discard_changes():
            return
        self._save_settings()
        self.root.destroy()

    def cmd_about(self):
        win = tk.Toplevel(self.root)
        win.title(self.t("about_title"))
        win.resizable(False, False)
        win.configure(bg=COLOR_BG_APP)
        win.transient(self.root)
        win.grab_set()

        pad = ttk.Frame(win, padding=20)
        pad.pack(fill="both", expand=True)

        # Иконка 64×64. Файл icon.png должен лежать рядом с exe / скриптом.
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(sys.argv[0])), "icon.png")
        if os.path.isfile(icon_path):
            self._about_icon = PhotoImage(file=icon_path)
            icon_lbl = ttk.Label(pad, image=self._about_icon,
                                  background=COLOR_BG_APP)
            icon_lbl.pack(anchor="w", pady=(0, 8))

        ttk.Label(pad, text=self.t("about_name"),
                  font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(pad, text=self.t("about_version"),
                  foreground=COLOR_TEXT_MUTED,
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 10))
        ttk.Label(pad, text=self.t("about_text"),
                  justify="left").pack(anchor="w", pady=(0, 10))

        # Ссылки из ABOUT_LINKS.
        for link_name, link_url in ABOUT_LINKS:
            if not link_name and not link_url:
                # Пустая строка-разделитель.
                ttk.Label(pad, text="").pack(anchor="w")
                continue
            if link_url.startswith("mailto:"):
                display = f"{link_name}: {link_url[7:]}"
            else:
                display = f"{link_name}: {link_url}"
            lbl = ttk.Label(pad, text=display, foreground=COLOR_SELECTION,
                            cursor="hand2",
                            font=("Segoe UI", 9, "underline"))
            lbl.pack(anchor="w", pady=(0, 2))
            lbl.bind("<Button-1>",
                     lambda _e, url=link_url: webbrowser.open(url))

        ttk.Button(pad, text="OK", command=win.destroy).pack(pady=(14, 0))

    def _confirm_discard_changes(self):
        if not self.dirty:
            return True
        ans = messagebox.askyesnocancel(
            self.t("unsaved_title"), self.t("unsaved_msg"))
        if ans is None:
            return False
        if ans:
            self.cmd_save()
            return not self.dirty
        return True

    def _update_title(self):
        title = APP_TITLE
        if self.file_path:
            title += f" — {os.path.basename(self.file_path)}"
        if self.dirty:
            title += " *"
        self.root.title(title)

    def _mark_dirty(self):
        if not self.dirty:
            self.dirty = True
            self._update_title()

    # --- Section list ------------------------------------------------------

    def _check_filter(self, value, op_var, val_var):
        """Проверяет, проходит ли числовое value через фильтр op+val."""
        op = op_var.get()
        if op == "—":
            return True
        try:
            threshold = int(val_var.get())
        except (ValueError, tk.TclError):
            return True
        if op == "=":  return value == threshold
        if op == ">":  return value > threshold
        if op == ">=": return value >= threshold
        if op == "<":  return value < threshold
        if op == "<=": return value <= threshold
        return True

    def _refresh_section_list(self):
        self.section_listbox.delete(0, tk.END)
        query = self.search_var.get().strip().lower()
        self._filtered_sections = []
        for s in self.sections:
            if query and query not in s.name.lower():
                continue
            if not self._check_filter(s.x2, self.filter_w_op, self.filter_w_val):
                continue
            if not self._check_filter(s.y2, self.filter_h_op, self.filter_h_val):
                continue
            self._filtered_sections.append(s)
            self.section_listbox.insert(
                tk.END, f"{s.name}   [{s.x2}×{s.y2}]")
        if self.current_section in self._filtered_sections:
            idx = self._filtered_sections.index(self.current_section)
            self.section_listbox.selection_set(idx)
            self.section_listbox.see(idx)

    def _on_section_select(self, _ev):
        sel = self.section_listbox.curselection()
        if not sel:
            return
        section = self._filtered_sections[sel[0]]
        if section is self.current_section:
            return
        self.current_section = section
        self.selected_element = None
        self._draw_section()
        self._refresh_element_list()
        self._update_coord_entries()
        self._update_dialog_size_entries()

    def _select_section_by_name(self, name):
        """Находит секцию по имени и выбирает её в списке."""
        for i, s in enumerate(self._filtered_sections):
            if s.name == name:
                self.section_listbox.selection_clear(0, tk.END)
                self.section_listbox.selection_set(i)
                self.section_listbox.see(i)
                self.current_section = s
                self._draw_section()
                self._refresh_element_list()
                self._update_coord_entries()
                self._update_dialog_size_entries()
                break

    # --- Element list ------------------------------------------------------

    def _refresh_element_list(self):
        for item in self.element_tree.get_children():
            self.element_tree.delete(item)
        if not self.current_section:
            return
        for i, el in enumerate(self.current_section.elements):
            self.element_tree.insert(
                "", "end", iid=str(i),
                values=(el.kind, el.name, el.x1, el.y1, el.x2, el.y2))
        if isinstance(self.selected_element, DlgElement) and \
                self.selected_element in self.current_section.elements:
            i = self.current_section.elements.index(self.selected_element)
            self.element_tree.selection_set(str(i))
            self.element_tree.see(str(i))

    def _on_element_tree_select(self, _ev):
        sel = self.element_tree.selection()
        if not sel or not self.current_section:
            return
        el = self.current_section.elements[int(sel[0])]
        if el is self.selected_element:
            return
        self.selected_element = el
        self._update_coord_entries()
        self._redraw_selection_highlight()

    def _refresh_selected_row(self):
        if not isinstance(self.selected_element, DlgElement) or \
                not self.current_section:
            return
        idx = self.current_section.elements.index(self.selected_element)
        el = self.selected_element
        self.element_tree.item(
            str(idx),
            values=(el.kind, el.name, el.x1, el.y1, el.x2, el.y2))

    # --- Coord panel -------------------------------------------------------

    def _update_coord_entries(self):
        el = self.selected_element if isinstance(self.selected_element,
                                                 DlgElement) else None
        for label in ("X1", "Y1", "X2", "Y2"):
            self.coord_vars[label].set(
                getattr(el, label.lower()) if el else 0)

    def _apply_coord_entries(self):
        el = self.selected_element
        if not isinstance(el, DlgElement) or not self.current_section:
            return
        try:
            x1 = int(self.coord_vars["X1"].get())
            y1 = int(self.coord_vars["Y1"].get())
            x2 = int(self.coord_vars["X2"].get())
            y2 = int(self.coord_vars["Y2"].get())
        except (tk.TclError, ValueError):
            self._update_coord_entries()
            return
        if x2 < x1: x1, x2 = x2, x1
        if y2 < y1: y1, y2 = y2, y1
        sec = self.current_section
        x1 = max(0, min(sec.x2, x1)); x2 = max(0, min(sec.x2, x2))
        y1 = max(0, min(sec.y2, y1)); y2 = max(0, min(sec.y2, y2))
        if (x1, y1, x2, y2) == (el.x1, el.y1, el.x2, el.y2):
            self._update_coord_entries()
            return
        el.x1, el.y1, el.x2, el.y2 = x1, y1, x2, y2
        self._mark_dirty()
        self._update_coord_entries()
        self._refresh_selected_row()
        self._draw_section()

    # --- Dialog size panel -------------------------------------------------

    def _update_dialog_size_entries(self):
        sec = self.current_section
        if sec is None:
            self.dlg_w_var.set(0)
            self.dlg_h_var.set(0)
            self.dlg_size_hint.config(text=self.t("dlg_size_fixed"),
                                       foreground=COLOR_TEXT_MUTED)
            return
        self.dlg_w_var.set(sec.x2)
        self.dlg_h_var.set(sec.y2)
        if (sec.w2, sec.h2) != (sec.x2, sec.y2):
            self.dlg_size_hint.config(
                text=self.t("dlg_size_warn", w=sec.w2, h=sec.h2),
                foreground=COLOR_WARN)
        else:
            self.dlg_size_hint.config(text=self.t("dlg_size_fixed"),
                                       foreground=COLOR_TEXT_MUTED)

    def _apply_dialog_size(self):
        sec = self.current_section
        if sec is None:
            return
        try:
            w = int(self.dlg_w_var.get())
            h = int(self.dlg_h_var.get())
        except (tk.TclError, ValueError):
            self._update_dialog_size_entries()
            return
        min_w, min_h = 10, 10
        for el in sec.elements:
            min_w = max(min_w, el.x2)
            min_h = max(min_h, el.y2)
        w = max(min_w, min(CANVAS_W, w))
        h = max(min_h, min(CANVAS_H, h))
        if (w, h) == (sec.x2, sec.y2) and (w, h) == (sec.w2, sec.h2):
            self._update_dialog_size_entries()
            return
        sec.x2, sec.y2 = w, h
        sec.w2, sec.h2 = w, h
        self._mark_dirty()
        self._update_dialog_size_entries()
        self._refresh_section_list()
        self._draw_section()

    # --- Canvas drawing ----------------------------------------------------

    def _clear_canvas(self):
        self.canvas.delete("all")
        self.element_to_rect = {}
        self.dialog_rect_id = None

    def _draw_section(self):
        self._clear_canvas()
        sec = self.current_section
        if not sec:
            self.canvas.configure(scrollregion=(0, 0, CANVAS_W, CANVAS_H))
            return
        sw, sh = sec.x2, sec.y2
        self.canvas.configure(scrollregion=(0, 0,
                                             max(sw + 20, CANVAS_W),
                                             max(sh + 20, CANVAS_H)))
        self.dialog_rect_id = self.canvas.create_rectangle(
            0, 0, sw, sh, outline=COLOR_DIALOG_FRAME, width=1,
            fill=COLOR_BG_WINDOW)
        self.canvas.create_text(
            6, 4, text=f"{sec.name}  ({sw}×{sh})", anchor="nw",
            fill=COLOR_TEXT, font=("Segoe UI", 9, "bold"))
        for el in sec.elements:
            self._draw_element(el)
        self._redraw_selection_highlight()

    def _draw_element(self, el):
        x1, y1, x2, y2 = el.x1, el.y1, el.x2, el.y2
        kind = el.kind
        if kind in ("BUTTONSD", "TOGGLE", "TOGGLESD"):
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_BUTTON_BG, width=1)
            self.canvas.create_line(x1, y1, x2 - 1, y1,
                                     fill=COLOR_BORDER_LIGHT)
            self.canvas.create_line(x1, y1, x1, y2 - 1,
                                     fill=COLOR_BORDER_LIGHT)
        elif kind == "EDIT":
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_INPUT_BG, width=1)
        elif kind in ("LBOX", "TLBOX"):
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_INPUT_BG, width=1)
        elif kind == "TEXT":
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_MED,
                fill="", width=1, dash=(2, 2))
        elif kind == "IMAGE":
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_BG_WINDOW, width=1)
            self.canvas.create_line(x1, y1, x2, y2, fill=COLOR_BORDER_MED)
            self.canvas.create_line(x1, y2, x2, y1, fill=COLOR_BORDER_MED)
        elif kind == "SPIN":
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_INPUT_BG, width=1)
        else:
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=COLOR_BORDER_DARK,
                fill=COLOR_BUTTON_BG, width=1)
        self.element_to_rect[el] = rect
        w, h = x2 - x1, y2 - y1
        if w >= 30 and h >= 12:
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=el.name, anchor="center",
                fill=COLOR_TEXT, font=("Segoe UI", 7))

    def _redraw_selection_highlight(self):
        self.canvas.delete("selection")
        for el, rect in self.element_to_rect.items():
            self.canvas.itemconfigure(rect, width=1)
        if self.dialog_rect_id is not None:
            self.canvas.itemconfigure(self.dialog_rect_id,
                                       outline=COLOR_DIALOG_FRAME, width=1)
        sel = self.selected_element
        if sel is HIT_DIALOG and self.current_section:
            sec = self.current_section
            self.canvas.itemconfigure(self.dialog_rect_id,
                                       outline=COLOR_SELECTION, width=2)
            h = HANDLE_SIZE
            self.canvas.create_rectangle(
                sec.x2 - h, sec.y2 - h, sec.x2, sec.y2,
                fill=COLOR_SELECTION, outline=COLOR_BORDER_DARK,
                tags=("selection",))
            return
        if isinstance(sel, DlgElement) and sel in self.element_to_rect:
            rect = self.element_to_rect[sel]
            self.canvas.itemconfigure(rect, outline=COLOR_SELECTION, width=2)
            self.canvas.tag_raise(rect)
            h = HANDLE_SIZE
            cx = (sel.x1 + sel.x2) / 2
            cy = (sel.y1 + sel.y2) / 2
            for hx, hy in (
                (sel.x1, sel.y1), (sel.x2, sel.y1),
                (sel.x1, sel.y2), (sel.x2, sel.y2),
                (cx, sel.y1), (cx, sel.y2),
                (sel.x1, cy), (sel.x2, cy),
            ):
                self.canvas.create_rectangle(
                    hx - h / 2, hy - h / 2, hx + h / 2, hy + h / 2,
                    fill=COLOR_SELECTION, outline=COLOR_BORDER_DARK,
                    tags=("selection",))

    # --- Canvas interaction ------------------------------------------------

    def _canvas_coords(self, event):
        return (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def _hit_test_rect(self, x1, y1, x2, y2, px, py, only_right_bottom=False):
        h = HANDLE_SIZE
        if not (x1 - h <= px <= x2 + h and y1 - h <= py <= y2 + h):
            return HIT_NONE
        flags = 0
        if not only_right_bottom and abs(px - x1) <= h:
            flags |= HIT_L
        elif abs(px - x2) <= h:
            flags |= HIT_R
        if not only_right_bottom and abs(py - y1) <= h:
            flags |= HIT_T
        elif abs(py - y2) <= h:
            flags |= HIT_B
        if flags:
            return flags
        if x1 < px < x2 and y1 < py < y2:
            return HIT_NONE if only_right_bottom else HIT_INSIDE
        return HIT_NONE

    def _find_target_at(self, cx, cy):
        sec = self.current_section
        if not sec:
            return None, HIT_NONE
        if isinstance(self.selected_element, DlgElement):
            hit = self._hit_test_rect(
                self.selected_element.x1, self.selected_element.y1,
                self.selected_element.x2, self.selected_element.y2, cx, cy)
            if hit:
                return self.selected_element, hit
        for el in reversed(sec.elements):
            hit = self._hit_test_rect(el.x1, el.y1, el.x2, el.y2, cx, cy)
            if hit:
                return el, hit
        hit = self._hit_test_rect(0, 0, sec.x2, sec.y2, cx, cy,
                                  only_right_bottom=True)
        if hit and (hit & (HIT_R | HIT_B)):
            return HIT_DIALOG, hit
        return None, HIT_NONE

    def _cursor_for_hit(self, hit):
        if hit == HIT_INSIDE: return "fleur"
        if hit & HIT_L and hit & HIT_T: return "top_left_corner"
        if hit & HIT_R and hit & HIT_T: return "top_right_corner"
        if hit & HIT_L and hit & HIT_B: return "bottom_left_corner"
        if hit & HIT_R and hit & HIT_B: return "bottom_right_corner"
        if hit & HIT_L: return "left_side"
        if hit & HIT_R: return "right_side"
        if hit & HIT_T: return "top_side"
        if hit & HIT_B: return "bottom_side"
        return ""

    def _on_canvas_motion(self, event):
        if self.drag_mode != HIT_NONE:
            return
        cx, cy = self._canvas_coords(event)
        target, hit = self._find_target_at(cx, cy)
        self.canvas.config(cursor=self._cursor_for_hit(hit) if target else "")

    def _on_canvas_press(self, event):
        cx, cy = self._canvas_coords(event)
        target, hit = self._find_target_at(cx, cy)
        if not target:
            self.selected_element = None
            self._redraw_selection_highlight()
            self._update_coord_entries()
            self.element_tree.selection_remove(self.element_tree.selection())
            return
        if target is HIT_DIALOG:
            self.selected_element = HIT_DIALOG
            self.element_tree.selection_remove(self.element_tree.selection())
            self._update_coord_entries()
            self._redraw_selection_highlight()
            sec = self.current_section
            self.drag_target = HIT_DIALOG
            self.drag_mode = hit
            self.drag_start_x = cx
            self.drag_start_y = cy
            self.drag_orig = (0, 0, sec.x2, sec.y2)
            return
        if target is not self.selected_element:
            self.selected_element = target
            idx = self.current_section.elements.index(target)
            self.element_tree.selection_set(str(idx))
            self.element_tree.see(str(idx))
            self._update_coord_entries()
            self._redraw_selection_highlight()
        self.drag_target = target
        self.drag_mode = hit
        self.drag_start_x = cx
        self.drag_start_y = cy
        self.drag_orig = (target.x1, target.y1, target.x2, target.y2)

    def _on_canvas_drag(self, event):
        if self.drag_mode == HIT_NONE or self.drag_target is None:
            return
        cx, cy = self._canvas_coords(event)
        sec = self.current_section
        ox1, oy1, ox2, oy2 = self.drag_orig
        dx = cx - self.drag_start_x
        dy = cy - self.drag_start_y

        if self.drag_target is HIT_DIALOG:
            new_w, new_h = ox2, oy2
            if self.drag_mode & HIT_R: new_w = ox2 + dx
            if self.drag_mode & HIT_B: new_h = oy2 + dy
            min_w, min_h = 10, 10
            for el in sec.elements:
                min_w = max(min_w, el.x2)
                min_h = max(min_h, el.y2)
            new_w = max(min_w, min(CANVAS_W, int(new_w)))
            new_h = max(min_h, min(CANVAS_H, int(new_h)))
            sec.x2, sec.y2 = new_w, new_h
            sec.w2, sec.h2 = new_w, new_h
            self.canvas.coords(self.dialog_rect_id, 0, 0, new_w, new_h)
            self._update_dialog_size_entries()
            self._redraw_selection_highlight()
            return

        el = self.drag_target
        sw, sh = sec.x2, sec.y2
        if self.drag_mode == HIT_INSIDE:
            w = ox2 - ox1
            h = oy2 - oy1
            nx1 = max(0, min(sw - w, ox1 + dx))
            ny1 = max(0, min(sh - h, oy1 + dy))
            el.x1, el.y1 = int(nx1), int(ny1)
            el.x2, el.y2 = el.x1 + w, el.y1 + h
        else:
            nx1, ny1, nx2, ny2 = ox1, oy1, ox2, oy2
            if self.drag_mode & HIT_L: nx1 = max(0, min(ox2 - 1, ox1 + dx))
            if self.drag_mode & HIT_R: nx2 = max(ox1 + 1, min(sw, ox2 + dx))
            if self.drag_mode & HIT_T: ny1 = max(0, min(oy2 - 1, oy1 + dy))
            if self.drag_mode & HIT_B: ny2 = max(oy1 + 1, min(sh, oy2 + dy))
            el.x1, el.y1, el.x2, el.y2 = int(nx1), int(ny1), int(nx2), int(ny2)

        rect = self.element_to_rect.get(el)
        if rect:
            self.canvas.coords(rect, el.x1, el.y1, el.x2, el.y2)
        self._redraw_selection_highlight()
        self._update_coord_entries()
        self._refresh_selected_row()

    def _on_canvas_release(self, _event):
        if self.drag_mode == HIT_NONE or self.drag_target is None:
            self.drag_mode = HIT_NONE
            self.drag_target = None
            return
        sec = self.current_section
        if self.drag_target is HIT_DIALOG:
            ox1, oy1, ox2, oy2 = self.drag_orig
            if (sec.x2, sec.y2) != (ox2, oy2):
                self._mark_dirty()
                self._refresh_section_list()
        else:
            el = self.drag_target
            if self.drag_orig != (el.x1, el.y1, el.x2, el.y2):
                self._mark_dirty()
        self.drag_mode = HIT_NONE
        self.drag_target = None
        self.drag_orig = None
        self._draw_section()


def main():
    initial = sys.argv[1] if len(sys.argv) > 1 else None
    root = tk.Tk()
    DlgEditorApp(root, initial_path=initial)
    root.mainloop()


if __name__ == "__main__":
    main()
