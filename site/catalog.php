<?php
$page_title = 'Каталог для ГНБ — бентонит, установки, инструмент | ANKO';
$page_desc  = 'Каталог для горизонтально направленного бурения: бентониты AnkoBent и CETCO, полимеры, буровые установки, инструмент, ПЭ трубы, химия Normet. Склад в Минске.';
$canonical  = 'catalog.php';
$active     = 'catalog';
$extra_head = <<<'HTML'
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://ankoglobal.by/"},{"@type":"ListItem","position":2,"name":"Каталог","item":"https://ankoglobal.by/catalog.php"}]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"Каталог продукции для ГНБ","url":"https://ankoglobal.by/catalog.php","mainEntity":{"@type":"ItemList","numberOfItems":8,"itemListElement":[{"@type":"ListItem","position":1,"name":"Бентониты","url":"https://ankoglobal.by/category-bentonit.php"},{"@type":"ListItem","position":2,"name":"Полимеры и реагенты","url":"https://ankoglobal.by/category-polimer.php"},{"@type":"ListItem","position":3,"name":"Буровые установки","url":"https://ankoglobal.by/category-ustanovki.php"},{"@type":"ListItem","position":4,"name":"Буровой инструмент","url":"https://ankoglobal.by/category-instrument.php"},{"@type":"ListItem","position":5,"name":"ПЭ трубы","url":"https://ankoglobal.by/category-trubi.php"},{"@type":"ListItem","position":6,"name":"Смазочные материалы","url":"https://ankoglobal.by/category-smazki.php"},{"@type":"ListItem","position":7,"name":"Локационные системы","url":"https://ankoglobal.by/category-lokacia.php"},{"@type":"ListItem","position":8,"name":"Химия Normet","url":"https://ankoglobal.by/category-normet.php"}]}}</script>
HTML;
$body_scripts = '<script src="js/search.js?v=20260726-v26"></script>';
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <nav class="crumbs" aria-label="Хлебные крошки">
    <div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span>Каталог</div>
  </nav>

  <div class="wrap page-head">
    <span class="eyebrow">Каталог</span>
    <h1 class="page-head__title">Каталог продукции для ГНБ</h1>
    <p class="page-head__text">Всё для горизонтально направленного бурения — от бурового раствора до установки. Собственная марка бентонита AnkoBent и бренды из каталога. Не нашли нужное — позвоните, подберём аналог.</p>
  </div>

  <div class="wrap">
    <div class="searchbar">
      <label class="visually-hidden" for="catalog-search">Поиск по каталогу</label>
      <input class="searchbar__input" id="catalog-search" type="search" placeholder="Поиск — например, бентонит или расширитель" data-search>
      <a class="btn btn--call" href="tel:+375296526709"><svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>Спросить у менеджера</a>
    </div>
  </div>

  <div class="wrap">
    <div class="categories categories--catalog">
        <a class="category card" href="category-bentonit.php" data-search-name="Бентониты AnkoBent CETCO PHRIKOLAT BAROID BAULUX">
          <picture><source srcset="img/generated/bentonite-cetco-ultragel-640.webp 640w, img/generated/bentonite-cetco-ultragel-960.webp 960w, img/generated/bentonite-cetco-ultragel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/generated/bentonite-cetco-ultragel.jpg" alt="Бентонит CETCO для ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Бентониты</h2>
            <p class="category__text">Бентонитовые порошки для приготовления буровых растворов.</p>
            <p class="category__brands">AnkoBent · CETCO · PHRIKOLAT · BAROID</p>
            <span class="category__count">4 позиции</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-polimer.php" data-search-name="Полимеры и реагенты CETCO PolymersPlus BAULUX">
          <picture><source srcset="img/category-cover-polimery-640.webp 640w, img/category-cover-polimery-960.webp 960w, img/category-cover-polimery.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/category-cover-polimery.jpg" alt="Полимеры и реагенты для бурового раствора ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Полимеры и реагенты</h2>
            <p class="category__text">Добавки для стабилизации скважины и улучшения бурового раствора.</p>
            <p class="category__brands">CETCO · PolymersPlus · BAULUX</p>
            <span class="category__count">7 позиций</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-ustanovki.php" data-search-name="Буровые установки XCMG Goodeng Vermeer Ditch Witch FDP Universal HDD WAMET Игла">
          <picture><source srcset="img/category-cover-ustanovki-640.webp 640w, img/category-cover-ustanovki-960.webp 960w, img/category-cover-ustanovki.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/category-cover-ustanovki.jpg" alt="Буровая установка ГНБ на светлом фоне" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Буровые установки</h2>
            <p class="category__text">Установки ГНБ, вертикального и шнекового бурения, прокола грунта.</p>
            <p class="category__brands">XCMG · Goodeng · Vermeer · Ditch Witch</p>
            <span class="category__count">10 позиций</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-instrument.php" data-search-name="Буровой инструмент Vermeer Ditch Witch Hunting DRILLTO XCMG Goodeng">
          <picture><source srcset="img/product-rasshiritel-640.webp 640w, img/product-rasshiritel-960.webp 960w, img/product-rasshiritel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/product-rasshiritel.jpg" alt="Расширитель — буровой инструмент для ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Буровой инструмент</h2>
            <p class="category__text">Расширители, вертлюги, пилоты, штанги, головы, адаптеры и оснастка.</p>
            <p class="category__brands">Vermeer · Ditch Witch · Hunting · DRILLTO</p>
            <span class="category__count">14 позиций</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-trubi.php" data-search-name="ПЭ трубы ">
          <picture><source srcset="img/product-pe-pipe-voda-640.webp 640w, img/product-pe-pipe-voda-960.webp 960w, img/product-pe-pipe-voda.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/product-pe-pipe-voda.jpg" alt="ПЭ трубы для прокладки методом ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">ПЭ трубы</h2>
            <p class="category__text">Полиэтиленовые трубы для водоснабжения и газоснабжения.</p>
            
            <span class="category__count">2 позиции</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-smazki.php" data-search-name="Смазочные материалы Vermeer Ditch Witch Jet Lube">
          <picture><source srcset="img/category-cover-smazki-640.webp 640w, img/category-cover-smazki-960.webp 960w, img/category-cover-smazki.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/category-cover-smazki.jpg" alt="Смазочные материалы для буровых штанг ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Смазочные материалы</h2>
            <p class="category__text">Смазки для буровых штанг и резьбовых соединений.</p>
            <p class="category__brands">Vermeer · Ditch Witch · Jet Lube</p>
            <span class="category__count">4 позиции</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-lokacia.php" data-search-name="Локационные системы DigiTrak SubSite">
          <picture><source srcset="img/category-cover-lokacia-640.webp 640w, img/category-cover-lokacia-960.webp 960w, img/category-cover-lokacia.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/category-cover-lokacia.jpg" alt="Локационная система для горизонтально направленного бурения" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Локационные системы</h2>
            <p class="category__text">Локаторы и зонды для проводки и контроля трассы бурения.</p>
            <p class="category__brands">DigiTrak · SubSite</p>
            <span class="category__count">3 позиции</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-normet.php" data-search-name="Химия Normet Normet">
          <picture><source srcset="img/category-cover-normet-640.webp 640w, img/category-cover-normet-960.webp 960w, img/category-cover-normet.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 360px" type="image/webp"><img class="category__img" src="img/category-cover-normet.jpg" alt="Строительная химия Normet в фирменной таре" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h2 class="category__title">Химия Normet</h2>
            <p class="category__text">Профессиональная строительная химия для подземного строительства.</p>
            <p class="category__brands">Normet</p>
            <span class="category__count">11 позиций</span>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
    </div>
  </div>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
