<?php
$page_title = 'Локационные системы ГНБ — DigiTrak, SubSite, зонды';
$page_desc  = 'Локационные системы для горизонтально направленного бурения: DigiTrak, SubSite, локаторы российского производства, зонды. Доставка по РБ и СНГ.';
$canonical  = 'category-lokacia.php';
$og_image = 'img/category-cover-lokacia.jpg';
$active     = 'catalog';
$extra_head = <<<'HTML'
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://ankoglobal.by/"},{"@type":"ListItem","position":2,"name":"Каталог","item":"https://ankoglobal.by/catalog.php"},{"@type":"ListItem","position":3,"name":"Локационные системы","item":"https://ankoglobal.by/category-lokacia.php"}]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"Локационные системы ГНБ — DigiTrak, SubSite, зонды","url":"https://ankoglobal.by/category-lokacia.php","mainEntity":{"@type":"ItemList","numberOfItems":3,"itemListElement":[{"@type":"ListItem","position":1,"name":"DigiTrak Falcon F5+ / Subsite Marksman","url":"https://ankoglobal.by/product-lokatori-digitrak.php"},{"@type":"ListItem","position":2,"name":"Локационные системы РФ","url":"https://ankoglobal.by/product-lokatori-rf.php"},{"@type":"ListItem","position":3,"name":"Зонды для локационных систем","url":"https://ankoglobal.by/product-zondi.php"}]}}</script>
HTML;
$body_scripts = '<script src="js/search.js?v=20260726-v26"></script>';
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <nav class="crumbs" aria-label="Хлебные крошки">
    <div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span><a href="catalog.php">Каталог</a><span class="crumbs__sep">/</span>Локационные системы</div>
  </nav>

  <div class="wrap page-head">
    <span class="eyebrow">Каталог · Локационные системы</span>
    <h1 class="page-head__title">Локационные системы для ГНБ</h1>
    <p class="page-head__text">Локационные системы для контроля положения буровой головы: определяют глубину, уклон и направление. Американские DigiTrak и SubSite, системы российского производства, а также зонды.</p>
  </div>

  <div class="wrap">
    <div class="catalog-full">
        <div class="searchbar searchbar--tight">
          <label class="visually-hidden" for="cat-search">Поиск в категории</label>
          <input class="searchbar__input" id="cat-search" type="search" placeholder="Поиск в категории" data-search>
        </div>
        <div class="products">
          <article class="product card" data-brand="DigiTrak, SubSite" data-stock="in" data-search-name="DigiTrak Falcon F5+ / Subsite Marksman DigiTrak, SubSite">
            <a href="product-lokatori-digitrak.php">
              <picture>
                <source srcset="img/product-lokatori-digitrak-640.webp 640w, img/product-lokatori-digitrak-960.webp 960w, img/product-lokatori-digitrak.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
                <img class="product__img" src="img/product-lokatori-digitrak.jpg" alt="Локационные системы DigiTrak Falcon F5+ и Subsite Marksman" width="1280" height="800" loading="lazy" decoding="async">
              </picture>
            </a>
            <div class="product__body">
              <span class="product__brand">DigiTrak · Subsite</span>
              
              <h2 class="product__title"><a href="product-lokatori-digitrak.php">DigiTrak Falcon F5+ / Subsite Marksman</a></h2>
              <p class="product__text">Проверенные локационные системы для ГНБ; комплектация зависит от выбранной модели.</p>
              <div class="product__row">
                <span class="product__price">Цена <span>по запросу</span></span>
                <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
              </div>
            </div>
          </article>
          <article class="product card" data-brand="РФ" data-stock="in" data-search-name="Локационные системы РФ РФ">
            <a href="product-lokatori-rf.php">
              <picture>
                <source srcset="img/product-lokatori-rf-640.webp 640w, img/product-lokatori-rf-960.webp 960w, img/product-lokatori-rf.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
                <img class="product__img" src="img/product-lokatori-rf.jpg" alt="Локационная система для ГНБ без привязки к конкретному бренду" width="1280" height="800" loading="lazy" decoding="async">
              </picture>
            </a>
            <div class="product__body">
              <span class="product__brand">РФ</span>
              
              <h2 class="product__title"><a href="product-lokatori-rf.php">Локационные системы РФ</a></h2>
              <p class="product__text">Локаторы российского производства.</p>
              <div class="product__row">
                <span class="product__price">Цена <span>по запросу</span></span>
                <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
              </div>
            </div>
          </article>
          <article class="product card" data-brand="Зонды" data-stock="in" data-search-name="Зонды для локационных систем Зонды">
            <a href="product-zondi.php">
              <picture>
                <source srcset="img/product-zondi-640.webp 640w, img/product-zondi-960.webp 960w, img/product-zondi.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
                <img class="product__img" src="img/product-zondi.jpg" alt="Зонд-передатчик для локационной системы ГНБ" width="1280" height="800" loading="lazy" decoding="async">
              </picture>
            </a>
            <div class="product__body">
              <span class="product__brand">Зонды</span>
              
              <h2 class="product__title"><a href="product-zondi.php">Зонды для локационных систем</a></h2>
              <p class="product__text">Передатчики для локационных систем.</p>
              <div class="product__row">
                <span class="product__price">Цена <span>по запросу</span></span>
                <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
<section class="section section--sand">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Как выбрать</span>
        <h2 class="section__title">Главное — как система ведёт себя в помехах</h2>
        <p class="section__lead">Локатор — это глаза оператора под землёй. В чистом поле работает любой. Разница видна в городе.</p>
      </div>

      <div class="notice notice--warn">
        <p class="notice__title">Помехи «ослепляют» локатор</p>
        <p class="notice__text">Светофорные петли, ЛЭП, арматура в бетоне, силовые кабели — всё это создаёт помехи. Система с одной фиксированной частотой в такой обстановке может просто перестать видеть зонд. Приёмники, умеющие сканировать диапазон и переключать полосы, работают там, где простые встают.</p>
      </div>

      <h3 class="section__subtitle">Что показывает система</h3>
      <table class="spec-table spec-table--wide">
        <tbody>
          <tr><th scope="row" class="rig__model">Глубина</th><td>На какой глубине сейчас буровая голова</td></tr>
          <tr><th scope="row" class="rig__model">Уклон (pitch)</th><td>Наклон головы — задаёт профиль скважины</td></tr>
          <tr><th scope="row" class="rig__model">Поворот (roll)</th><td>Куда голова пойдёт при следующей подаче</td></tr>
          <tr><th scope="row" class="rig__model">Температура</th><td>Перегрев зонда — сигнал остановиться</td></tr>
          <tr><th scope="row" class="rig__model">Заряд батареи</th><td>Остаток ресурса зонда</td></tr>
        </tbody>
      </table>

      <h3 class="section__subtitle">На что смотреть при выборе</h3>
      <ul class="bullets">
        <li>Город и застройка — нужен приёмник со сканированием частот.</li>
        <li>Простые заходы и подключения к домам — достаточно базовой системы.</li>
        <li>Зонд подбирается строго под модель приёмника: совместимость обязательна.</li>
        <li>Запись данных бурения даёт протокол прокола для заказчика — иногда это условие контракта.</li>
      </ul>

      <p class="calc__concl"><b>Что делать:</b> расскажите, где работаете — город или трасса, — и мы подберём систему под ваши условия. <a href="tel:+375296526709">+375 29 652-67-09</a>.</p>
    </div>
  </section>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
