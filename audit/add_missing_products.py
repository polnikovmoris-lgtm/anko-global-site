#!/usr/bin/env python3
from pathlib import Path
from lxml import html as lxml_html
from PIL import Image
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ALINE = Path("/tmp/anko-v16-KeTYPI/a-line.by")

PRODUCTS = [
    dict(src="bentonit-ankobent-plus.html", slug="ankobent-plus", category="bentonit",
         name="AnkoBent Plus", brand="AnkoBent", image="AnkoBentPlus.png",
         lead="Высокопроизводительная смесь природно-натриевого бентонита для ГНБ и микротоннелирования."),
    dict(src="bentonit-ultragel.html", slug="ultra-gel", category="bentonit",
         name="Ultra Gel", brand="AnkoBent", image="CetcoUltraGel.jpg",
         lead="Универсальный бентонитовый материал для приготовления буровых растворов."),
    dict(src="bentonit-cetco-supergelx.html", slug="cetco-super-gel-x", category="bentonit",
         name="CETCO SUPER GEL X", brand="CETCO", image="CetcosuperGelX.jpg",
         lead="Высококачественный натриевый бентонит для буровых растворов."),
    dict(src="bentonit-cetco-hydraulez.html", slug="cetco-hydraul-ez", category="bentonit",
         name="CETCO HYDRAUL-EZ", brand="CETCO", image="CetcoHydraulEz.jpg",
         lead="Бентонитовая система для горизонтально-направленного бурения."),
    dict(src="bentonit-barroid-tunnel-gelplus.html", slug="baroid-tunnel-gel-plus", category="bentonit",
         name="Baroid TUNNEL-GEL PLUS", brand="BAROID", image="BarroidTunnGPlus.jpg",
         lead="Премиальная бентонитовая система для тоннелирования и сложных буровых работ."),
    dict(src="polimer-cetco-suspend-it.html", slug="cetco-suspend-it", category="polimer",
         name="CETCO SUSPEND-IT", brand="CETCO", image="CetcoSuspendIT.png",
         lead="Полимерная добавка для повышения несущей и суспендирующей способности раствора."),
    dict(src="polimer-polimersplus-hv.html", slug="polymersplus-hv", category="polimer",
         name="Polymers Plus HV", brand="PolymersPlus", image="PolymersPlusHV.jpg",
         lead="Высоковязкий полимер для регулирования свойств бурового раствора."),
    dict(src="polimer-polimersplus-pam-phpa.html", slug="polymersplus-pam-h", category="polimer",
         name="Polymers Plus PAM H", brand="PolymersPlus", image="PolymersPamPlusH.jpg",
         lead="Инкапсулирующий PHPA-полимер для стабилизации глинистых пород."),
    dict(src="polimer-benotolux-horizont-phpa.html", slug="bentolux-horizont-phpa", category="polimer",
         name="BENTOLUX Horizont PHPA", brand="BAULUX", image="BentoluxHorizonPHPA.png",
         lead="PHPA-полимер для ингибирования и стабилизации активных глин."),
    dict(src="polimer-bentolux-vis.html", slug="bentolux-horizon-vis", category="polimer",
         name="BENTOLUX Horizon VIS", brand="BAULUX", image="BentoluxHorizonVIS.png",
         lead="Полимер-загуститель для быстрого повышения вязкости бурового раствора."),
]


def clean_description(path):
    doc = lxml_html.fromstring(path.read_text(encoding="utf-8"))
    node = doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " item-descr ")]')[0]
    for bad in node.xpath('.//script | .//button | .//*[contains(concat(" ", normalize-space(@class), " "), " btn-holder ")]'):
        bad.getparent().remove(bad)
    for el in node.xpath('.//*[@style]'):
        el.attrib.pop("style", None)
    for table in node.xpath('.//table'):
        table.attrib.clear()
        table.attrib["class"] = "spec-table"
    for div in node.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " table-scroll ")]'):
        div.attrib["class"] = "table-scroll"
    text = (node.text or "") + "".join(lxml_html.tostring(x, encoding="unicode") for x in node)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    first = node.xpath('.//p')
    summary = " ".join(first[0].text_content().split()) if first else ""
    return text, summary


def make_images(p):
    source = ALINE / "img" / "bentonitPolimer" / p["image"]
    outbase = SITE / "img" / "generated" / f"{p['category']}-{p['slug']}"
    with Image.open(source) as src:
        src = src.convert("RGBA")
        for width, suffix in [(640, "-640"), (960, "-960"), (1280, "")]:
            height = round(width * 800 / 1280)
            canvas = Image.new("RGBA", (width, height), "white")
            copy = src.copy()
            copy.thumbnail((round(width * .82), round(height * .82)), Image.Resampling.LANCZOS)
            canvas.alpha_composite(copy, ((width-copy.width)//2, (height-copy.height)//2))
            canvas.convert("RGB").save(str(outbase) + suffix + ".webp", "WEBP", quality=86, method=6)
            if width == 1280:
                canvas.convert("RGB").save(str(outbase) + ".jpg", "JPEG", quality=90, optimize=True)
    return f"img/generated/{p['category']}-{p['slug']}"


def product_page(p, body):
    cat_name = "Бентониты" if p["category"] == "bentonit" else "Полимеры и реагенты"
    base = f"img/generated/{p['category']}-{p['slug']}"
    canonical = f"product-{p['slug']}.php"
    jname = json.dumps(p["name"], ensure_ascii=False)
    jlead = json.dumps(p["lead"], ensure_ascii=False)
    jbrand = json.dumps(p["brand"], ensure_ascii=False)
    return f"""<?php
$page_title = '{p["name"]} — купить в Минске, цена | ANKO GLOBAL';
$page_desc  = '{p["lead"]} Склад в Минске, доставка по Беларуси и СНГ. Цена по запросу.';
$canonical  = '{canonical}';
$og_image = '{base}.jpg';
$og_type = 'product';
$preload_image = '{base}.webp';
$preload_srcset = '{base}-640.webp 640w, {base}-960.webp 960w, {base}.webp 1280w';
$preload_sizes = '(max-width: 900px) 100vw, 50vw';
$active = 'catalog';
$extra_head = <<<'HTML'
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Product","name":{jname},"image":"https://a-global.by/{base}.jpg","description":{jlead},"brand":{{"@type":"Brand","name":{jbrand}}},"url":"https://a-global.by/{canonical}"}}</script>
HTML;
require __DIR__ . '/inc/head.php';
?>
<main>
  <nav class="crumbs" aria-label="Хлебные крошки"><div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span><a href="catalog.php">Каталог</a><span class="crumbs__sep">/</span><a href="category-{p["category"]}.php">{cat_name}</a><span class="crumbs__sep">/</span>{p["name"]}</div></nav>
  <div class="wrap">
    <div class="pdp">
      <div class="gallery"><div class="gallery__main"><picture>
        <source srcset="{base}-640.webp 640w, {base}-960.webp 960w, {base}.webp 1280w" sizes="(max-width: 900px) 100vw, 50vw" type="image/webp">
        <img class="gallery__img" src="{base}.jpg" alt="{html.escape(p["name"])}" width="1280" height="800" data-gallery-main decoding="async" fetchpriority="high">
      </picture></div></div>
      <div class="pdp__info">
        <span class="pdp__brand">{p["brand"]}</span>
        <h1 class="pdp__title">{p["name"]}</h1>
        <p class="pdp__lead">{p["lead"]}</p>
        <div class="buybox">
          <p class="buybox__price">Цена по запросу</p>
          <p class="buybox__note">Стоимость зависит от объёма партии. Позвоните — назовём цену и проверим наличие.</p>
          <a class="buybox__phone" href="tel:+375296526709">+375 29 652-67-09</a>
          <div class="buybox__buttons"><a class="btn btn--primary" href="tel:+375296526709">Узнать цену</a><button class="btn btn--outline" type="button" data-kp-open>Запросить КП</button></div>
        </div>
        <h2 class="section__subtitle">Характеристики</h2>
        <table class="spec-table"><tbody><tr><td>Бренд</td><td>{p["brand"]}</td></tr><tr><td>Наличие</td><td>Уточняйте по телефону</td></tr></tbody></table>
      </div>
    </div>
    <div class="pdp-content">
      <h2>Описание и технические характеристики</h2>
      {body}
      <h2>Доставка и оплата</h2>
      <p>Отгрузка со склада в Минске. Доставка по Беларуси и странам СНГ. Работаем с юридическими лицами по безналичному расчёту.</p>
    </div>
    <div class="usps">
      <div class="usp"><p class="usp__title">15 лет опыта</p><p class="usp__text">Знаем, что нужно на объекте</p></div>
      <div class="usp"><p class="usp__title">Склад в Минске</p><p class="usp__text">Ходовые позиции в наличии</p></div>
      <div class="usp"><p class="usp__title">Подбор аналога</p><p class="usp__text">Без потери качества</p></div>
      <div class="usp"><p class="usp__title">Доставка</p><p class="usp__text">По Беларуси и СНГ</p></div>
    </div>
  </div>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
"""


def card(p, summary):
    base = f"img/generated/{p['category']}-{p['slug']}"
    link = f"product-{p['slug']}.php"
    summary = summary or p["lead"]
    if len(summary) > 180:
        summary = summary[:177].rsplit(" ", 1)[0] + "…"
    return f"""
          <article class="product card" data-brand="{p['brand']}" data-stock="in" data-search-name="{p['name']} {p['brand']}">
            <a href="{link}"><picture>
              <source srcset="{base}-640.webp 640w, {base}-960.webp 960w, {base}.webp 1280w" sizes="(max-width: 620px) calc(100vw - 32px), (max-width: 1000px) 50vw, 33vw" type="image/webp">
              <img class="product__img" src="{base}.jpg" alt="{html.escape(p['name'])}" width="1280" height="800" loading="lazy" decoding="async">
            </picture></a>
            <div class="product__body">
              <span class="product__brand">{p['brand']}</span>
              <h2 class="product__title"><a href="{link}">{p['name']}</a></h2>
              <p class="product__text">{html.escape(summary)}</p>
              <div class="product__row"><span class="product__price">Цена <span>по запросу</span></span><a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a></div>
            </div>
          </article>"""


summaries = {}
for product in PRODUCTS:
    description, summaries[product["slug"]] = clean_description(ALINE / product["src"])
    make_images(product)
    (SITE / f"product-{product['slug']}.php").write_text(product_page(product, description), encoding="utf-8")

for category in ("bentonit", "polimer"):
    path = SITE / f"category-{category}.php"
    text = path.read_text(encoding="utf-8")
    marker = "        </div>\n      </div>"
    additions = "".join(card(p, summaries[p["slug"]]) for p in PRODUCTS if p["category"] == category)
    text = text.replace(marker, additions + "\n" + marker, 1)
    total = len(re.findall(r'<article class="product card"', text))
    text = re.sub(r'"numberOfItems":\d+', f'"numberOfItems":{total}', text, count=1)
    path.write_text(text, encoding="utf-8")

(ROOT / "audit" / "missing-products-manifest.json").write_text(
    json.dumps({"count": len(PRODUCTS), "products": PRODUCTS}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
