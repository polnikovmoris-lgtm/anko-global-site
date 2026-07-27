#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пересборка поискового индекса ANKO GLOBAL.

Запускать из корня сайта после того, как добавили/изменили товары:

    python3 build-search.py

Скрипт читает все category-*.php и product-*.php, собирает индекс
и встраивает его прямо в js/search.js.
"""
import glob, re, json, html, os, sys

# ---------------------------------------------------------------------------
# СИНОНИМЫ — как ещё могут назвать товар.
# Клиент ищет «бэкример», а у нас «расширитель» — здесь это связывается.
# Добавляйте сюда всё, что слышите от клиентов по телефону.
# ---------------------------------------------------------------------------
SYNONYMS = {
    "расширитель": ["бэкример", "бекример", "backreamer", "ример", "расширители"],
    "вертлюг": ["swivel", "вертлюжок", "вертлюги"],
    "штанга": ["штанги", "буровая штанга", "drill pipe", "труба буровая"],
    "бентонит": ["бентониты", "глинопорошок", "бентонитовый порошок",
                 "буровой раствор", "глина", "ankobent", "анкобент"],
    "полимер": ["полимеры", "реагент", "реагенты", "добавка", "добавки"],
    "смазка": ["смазки", "смазочные материалы", "резьбовая смазка",
               "смазка резьбы", "pipe dope", "солидол", "резьбовой состав"],
    "локационная система": ["локационные системы", "локатор", "локаторы", "локация",
                            "digitrak", "дигитрак", "зонд", "зонды",
                            "приёмник", "приемник", "передатчик"],
    "буровая установка": ["буровые установки", "установка", "установки",
                          "машина", "буровая", "станок", "гнб установка"],
    "пэ труба": ["пэ трубы", "полиэтиленовая труба", "пнд", "пнд труба", "труба", "трубы"],
    "нсу": ["насосно-смесительный узел", "смеситель", "миксер", "насосно смесительный узел"],
    "буровой нож": ["ножи", "лопатка", "лопатки", "резец", "резцы"],
    "буровой пилот": ["пилот", "пилоты", "пилотная головка", "буровая голова"],
    "адаптер": ["адаптеры", "переходник", "переходники"],
    "захват": ["захваты", "цанга", "цанговый захват"],
    "вкладыши": ["губки", "губки тисков", "вкладыши тисков"],
    "normet": ["нормет", "химия", "tamcem", "tamseal", "tampur", "tamshot",
               "tamcrete", "tamrez", "tamacryl", "tamsoil", "geotek"],
    "ключ трубный": ["ключи", "ключ", "трубный ключ"],
    "муфта": ["муфты"],
}

# Старые названия и модели из архива a-line.
# Они не создают отдельные тонкие карточки: точный запрос ведёт на актуальную
# объединённую карточку семейства ANKO.
PAGE_ALIASES = {
    "product-cetco-ultragel.php": [
        "Ultra Gel", "Ultragel", "CETCO Ultragel", "CETCO Ultra-Gel",
        "product-ultra-gel.php",
    ],
    "product-igla-20tvm.php": [
        "Игла-20ТБ", "Игла 20ТБ", "Igla 20TB", "Igla-20TB",
    ],
    "product-normet-geotek.php": [
        "GeoTek AC", "GeoTek HS", "GeoTek LV",
    ],
    "product-normet-tamacryl.php": [
        "TamAcryl 2000", "TamAcryl 3000",
    ],
    "product-normet-tamcem.php": [
        "TamCem 8BFG", "TamCem 9BFG", "TamCem 23SSR", "TamCem 60",
        "TamCem iBond", "TamCem HCA", "TamCem MicroSilica", "TamCem NanoSilica",
    ],
    "product-normet-tamcrete.php": [
        "TamCrete 400CS", "TamCrete CR", "TamCrete PII", "TamCrete Pll",
        "TamCrete MFC", "TamCrete UFC", "TamCrete Plug",
        "TamCrete PolyPlug", "TamCrete Poly Plug", "TamCrete SBR",
    ],
    "product-normet-tamgrease.php": [
        "TamGrease BL11", "TamGrease BS1", "TamGrease BS11",
    ],
    "product-normet-tampur.php": [
        "TamPur 100", "TamPur 116T", "TamPur 125", "TamPur 130",
        "TamPur 150", "TamPur 170",
    ],
    "product-normet-tamrez.php": [
        "TamRez 440",
    ],
    "product-normet-tamseal.php": [
        "TamSeal 10F", "TamSeal 10GM", "TamSeal 290", "TamSeal 20",
        "TamSeal 23", "TamSeal 23E", "TamSeal 1500", "TamSeal 4000E",
        "TamSeal 800", "TamSeal Admix", "TamSeal BR", "TamSeal BBR",
        "TamSeal EP11", "TamSeal IM", "TamSeal R", "TamSeal RC",
        "TamSeal TG11", "TamSeal TG12",
    ],
    "product-normet-tamshot.php": [
        "TamShot 80AF", "TamShot 110AF", "TamShot 210AF",
    ],
    "product-normet-tamsil.php": [
        "TamSil 1", "TamSil 7",
    ],
    "product-normet-tamsoil.php": [
        "TamSoil 190CF", "TamSoil 200CF", "TamSoil 260CF",
        "TamSoil 267CF", "TamSoil 280AC", "TamSoil 287AC",
        "TamSoil 600CP", "TamSoil 1000CP", "TamSoil 2000CP",
    ],
}



# Регулярка кодов артикулов: XZ180, JT40, D24x40, TamPur 138, 400CS, 80AF, F5, PAC-HV
CODE_RE = re.compile(
    r"\b("
    r"[A-Za-z]{1,6}[-\s]?\d{1,4}[A-Za-z]{0,4}"   # XZ180, JT40, TamPur138, 80AF, F5
    r"|[A-Za-z]{2,}\d+x\d+"                        # D24x40, D40x55
    r"|\d{2,4}[A-Za-z]{1,3}"                        # 400CS, 90AF
    r"|[A-Z]{2,5}(?:-[A-Z]{1,3})?"                  # PAC, PAC-HV, SDR, НСУ
    r")\b"
)

STOP_CODES = {"HDD","ГНБ","СНГ","MSDS","SDS","TDS","BYN","USD","NSF","ANSI",
              "OG","ID","УНП","ООО","SVG","PNG","JPG","CSS","HTML","URL"}

# Названия линеек, после которых идёт номер модели: "TamPur 138", "XZ 320"
FAMILY_RE = re.compile(
    r"\b(TamPur|TamCem|TamCrete|TamShot|TamSeal|TamRez|TamAcryl|TamSoil|TamGrease|"
    r"TamSil|GeoTek|Falcon|XZ|JT|Navigator)\s*"
    r"([A-Za-z]?\d{1,4}[A-Za-z]{0,4}(?:/[0-9A-Za-z]{1,6})?)",
    re.IGNORECASE)

def extract_codes(text):
    """Достаёт коды артикулов и моделей из текста карточки"""
    found = set()

    # 1. Линейка + номер: "TamPur 138", "TamShot 80AF", "XZ 320"
    for fam, num in FAMILY_RE.findall(text):
        for variant in (f"{fam}{num}", f"{fam} {num}", f"{fam}-{num}", num):
            found.add(variant)
        # если номер вида 80AF/10SS — добавляем и голую цифру, и буквы
        found.add(num)

    # 1b. Модели вида D40x55, D24x40 — ищем везде, даже в слипшемся тексте
    for m in re.findall(r"[A-Za-z]\d{1,3}x\d{1,3}[A-Za-z]{0,3}", text):
        found.add(m)
        found.add(m.upper())

    # 2. Отдельные коды: D24x40, 400CS, PAC-HV, JT40
    for m in CODE_RE.findall(text):
        m = m.strip()
        if len(m) < 2:
            continue
        up = m.upper().replace(" ", "")
        if up in STOP_CODES:
            continue
        if any(c.isdigit() for c in m) or up in ("PAC","НСУ","SDR","ПЭ","ПНД"):
            found.add(m)
            found.add(m.replace(" ", "").replace("-", ""))
            found.add(m.replace(" ", "-"))

    # чистим мусор
    return {c.strip() for c in found if 2 <= len(c.strip()) <= 20}


def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def build():
    index = []

    # ---- Категории ----
    for f in sorted(glob.glob("category-*.php")):
        h = open(f, encoding="utf-8").read()
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        if not h1:
            continue
        desc = re.search(r'<p class="page-head__text">(.*?)</p>', h, re.S)
        brands = re.findall(
            r'<label class="filters__option"><input type="checkbox"[^>]*>\s*([^<]+)</label>', h)
        name = clean(h1.group(1))
        index.append({
            "t": "cat", "u": f, "n": name,
            "d": clean(desc.group(1))[:110] if desc else "",
            "k": " ".join([name] + [b.strip() for b in brands]).lower(),
        })

    # ---- Товары ----
    for f in sorted(glob.glob("product-*.php")):
        h = open(f, encoding="utf-8").read()
        h1 = re.search(r'<h1 class="pdp__title">(.*?)</h1>', h, re.S)
        if not h1:
            continue
        brand = re.search(r'<span class="pdp__brand">(.*?)</span>', h, re.S)
        lead = re.search(r'<p class="pdp__lead">(.*?)</p>', h, re.S)
        crumbs = re.findall(r'<a href="category-[^"]+\.php">([^<]+)</a>', h)
        name = clean(h1.group(1))
        b = clean(brand.group(1)) if brand else ""
        cat = clean(crumbs[0]) if crumbs else ""
        # текст всей карточки — для вытаскивания кодов артикулов
        body = clean(re.sub(r"<script.*?</script>", "", h, flags=re.S))
        codes = extract_codes(body)
        aliases = PAGE_ALIASES.get(f, [])
        index.append({
            "t": "prod", "u": f, "n": name,
            "d": clean(lead.group(1))[:110] if lead else "",
            "c": cat, "b": b,
            "codes": " ".join(sorted(codes)),
            "k": (
                f"{name} {b} {cat} "
                + " ".join(sorted(codes))
                + " "
                + " ".join(aliases)
            ).lower(),
        })

    # ---- Синонимы ----
    for item in index:
        extra = set()
        k = item["k"]
        for base, syns in SYNONYMS.items():
            hit = base in k or any(s in k for s in syns)
            if hit:
                extra.add(base)
                extra.update(syns)
        if extra:
            item["k"] = k + " " + " ".join(sorted(extra))

    return index


def inject(index):
    path = "js/search.js"
    if not os.path.exists(path):
        sys.exit("Не найден js/search.js")

    js = open(path, encoding="utf-8").read()
    data = json.dumps(index, ensure_ascii=False, separators=(",", ":"))

    # Ищем строку "var INDEX_DATA = [...];" (в одну строку после сборки)
    marker = "var INDEX_DATA = "
    start = js.find(marker)
    if start == -1:
        sys.exit("Не нашёл INDEX_DATA в search.js — индекс не обновлён")
    # конец — первый "];" после начала массива
    end = js.find("];", start)
    if end == -1:
        sys.exit("Повреждён INDEX_DATA в search.js")
    end += 2  # включаем "];"
    new = js[:start] + marker + data + ";" + js[end:]

    if new == js:
        print("Индекс не изменился (каталог тот же)")
        return len(data)

    open(path, "w", encoding="utf-8").write(new)
    return len(data)


if __name__ == "__main__":
    idx = build()
    size = inject(idx)
    cats = sum(1 for i in idx if i["t"] == "cat")
    prods = sum(1 for i in idx if i["t"] == "prod")
    print(f"Индекс пересобран: {cats} категорий + {prods} товаров = {len(idx)} записей")
    print(f"Встроен в js/search.js ({size/1024:.1f} КБ)")
