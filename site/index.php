<?php
$page_title = 'ANKO GLOBAL — материалы и оборудование для ГНБ в Минске';
$page_desc  = 'Бентонит, полимеры, буровые установки и инструмент для горизонтально направленного бурения. 15 лет на рынке, склад в Минске, доставка по РБ и СНГ. +375 29 652-67-09.';
$canonical  = '/';
$preload_image = 'img/hero-goodeng-final.webp';
$preload_srcset = 'img/hero-goodeng-final-640.webp 640w, img/hero-goodeng-final-960.webp 960w, img/hero-goodeng-final.webp 1248w';
$preload_sizes = '(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 525px';
$extra_head = <<<'HTML'
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","@id":"https://ankoglobal.by/#organization","name":"ANKO GLOBAL","alternateName":"ООО «Анко-глобал»",
"url":"https://ankoglobal.by/","image":"https://ankoglobal.by/img/og-image.jpg","logo":"https://ankoglobal.by/img/logo.svg","telephone":"+375296526709","faxNumber":"+375175156000","email":"main.accentline@gmail.com","foundingDate":"2011",
"address":{"@type":"PostalAddress","streetAddress":"пер. 2-ой Школьный, д. 1А-1, пом. 14, д. Тарасово","addressLocality":"Минский район","addressRegion":"Минская область","postalCode":"223015","addressCountry":"BY"},
"areaServed":["BY","RU","KZ"],"openingHours":"Mo-Fr 09:00-21:00"}
</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","@id":"https://ankoglobal.by/#website","name":"ANKO GLOBAL","url":"https://ankoglobal.by/","inLanguage":"ru-BY","publisher":{"@id":"https://ankoglobal.by/#organization"}}</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"Доставляете по всей Беларуси и в СНГ?","acceptedAnswer":{"@type":"Answer","text":"Да, отгружаем на объект по всей Беларуси и в страны СНГ."}},
{"@type":"Question","name":"Можно подобрать аналог дешевле?","acceptedAnswer":{"@type":"Answer","text":"Да, подберём аналог под задачу и бюджет без потери качества."}},
{"@type":"Question","name":"Работаете с юрлицами по безналу?","acceptedAnswer":{"@type":"Answer","text":"Да, по безналичному расчёту, с полным пакетом документов."}},
{"@type":"Question","name":"Есть товар в наличии на складе?","acceptedAnswer":{"@type":"Answer","text":"Ходовые позиции держим на складе в Минске."}}]}
</script>
HTML;
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <!-- HERO -->
  <section class="hero">
    <div class="wrap hero__inner">
      <div class="hero__content">
        <span class="eyebrow">Горизонтально направленное бурение</span>
        <h1 class="hero__title">Материалы и оборудование для ГНБ со склада в Минске</h1>
        <p class="hero__text">Бентонит, полимеры, буровые установки и инструмент. Прямые поставки от производителей. Работаем 15 лет.</p>

        <div class="hero__callrow">
          <a class="phone-big" href="tel:+375296526709">+375 29 652-67-09<small>Звоните — ответим в рабочее время</small></a>
          <a class="btn btn--call" href="tel:+375296526709"><svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>Позвонить</a>
        </div>

        <div class="hero__buttons">
          <a class="btn btn--primary" href="catalog.php">Открыть каталог</a>
          <a class="btn btn--outline" href="#lead">Получить прайс-лист</a>
        </div>

        <p class="hero__trust">
          <span><b>15 лет</b> на рынке</span>
          <span><b>Склад</b> в Минске</span>
          <span><b>Доставка</b> по РБ и СНГ</span>
        </p>
      </div>

      <div class="hero__media">
        <picture>
          <source srcset="img/hero-goodeng-final-640.webp 640w, img/hero-goodeng-final-960.webp 960w, img/hero-goodeng-final.webp 1248w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 525px" type="image/webp">
          <img class="hero__img" src="img/hero-goodeng-final.jpg" alt="Буровая установка Goodeng, бентонит, полимер и смазка для ГНБ" width="1248" height="1260" fetchpriority="high" decoding="async">
        </picture>
      </div>
    </div>
  </section>

  <!-- ФАКТЫ -->
  <section class="trustbar">
    <div class="wrap trustbar__inner">
      <div class="trustbar__item">
        <span class="trustbar__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2l3 6 6 .9-4.5 4.3 1 6.3L12 17l-5.5 2.5 1-6.3L3 8.9 9 8z"/></svg></span>
        <span><span class="trustbar__value">15 лет</span><span class="trustbar__label">на рынке ГНБ</span></span>
      </div>
      <div class="trustbar__item">
        <span class="trustbar__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-6 9 6v11H3zM9 20v-6h6v6"/></svg></span>
        <span><span class="trustbar__value">Свой склад</span><span class="trustbar__label">в Минске</span></span>
      </div>
      <div class="trustbar__item">
        <span class="trustbar__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 12l2 2 4-4M12 2a10 10 0 100 20 10 10 0 000-20z"/></svg></span>
        <span><span class="trustbar__value">Прямые</span><span class="trustbar__label">поставки для ГНБ</span></span>
      </div>
      <div class="trustbar__item">
        <span class="trustbar__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 7h13v10H3zM16 10h3l2 3v4h-5M6 20a2 2 0 100-4 2 2 0 000 4zM18 20a2 2 0 100-4 2 2 0 000 4z"/></svg></span>
        <span><span class="trustbar__value">Доставка</span><span class="trustbar__label">по РБ и СНГ</span></span>
      </div>
    </div>
  </section>

  <!-- БРЕНДЫ (кликабельные) -->
  <section class="brands">
    <div class="wrap brands__inner">
      <span class="brands__label">Бренды в каталоге:</span>
      <div class="brands__list">
        <a class="brands__item" href="category-bentonit.php" aria-label="Товары бренда CETCO">
          <img class="brands__img" src="img/brand-cetco-official.png" alt="CETCO" width="1040" height="174" loading="lazy" decoding="async">
        </a>
        <a class="brands__item" href="category-ustanovki.php" aria-label="Товары бренда XCMG">
          <img class="brands__img" src="img/brand-xcmg-official.png" alt="XCMG" width="130" height="28" loading="lazy" decoding="async">
        </a>
        <a class="brands__item" href="product-goodeng-hdd.php" aria-label="Буровые установки Goodeng">
          <img class="brands__img" src="img/brand-goodeng-official.png" alt="GOODENG" width="520" height="131" loading="lazy" decoding="async">
        </a>
        <a class="brands__item" href="product-vermeer-hdd.php" aria-label="Буровые установки Vermeer">
          <img class="brands__img" src="img/brand-vermeer-official.png" alt="VERMEER" width="1040" height="247" loading="lazy" decoding="async">
        </a>
        <a class="brands__item" href="product-ditchwitch-hdd.php" aria-label="Буровые установки Ditch Witch">
          <img class="brands__img" src="img/brand-ditchwitch-official.png" alt="DITCH WITCH" width="520" height="74" loading="lazy" decoding="async">
        </a>
        <a class="brands__item" href="category-normet.php" aria-label="Товары бренда NORMET">
          <img class="brands__img" src="img/brand-normet.png" alt="Normet" width="600" height="140" loading="lazy" decoding="async">
        </a>
      </div>
    </div>
  </section>

  <!-- КАТАЛОГ -->
  <section class="section" id="catalog">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Каталог</span>
        <h2 class="section__title">Каталог товаров</h2>
        <p class="section__lead">Всё для бурения в одном месте — от раствора до установки. Подберём аналог под вашу задачу.</p>
      </div>
      <div class="categories">
        <a class="category card" href="category-bentonit.php">
          <picture><source srcset="img/generated/bentonite-cetco-ultragel-640.webp 640w, img/generated/bentonite-cetco-ultragel-960.webp 960w, img/generated/bentonite-cetco-ultragel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 66px) / 2), 266px" type="image/webp"><img class="category__img" src="img/generated/bentonite-cetco-ultragel.jpg" alt="Бентонит CETCO для ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h3 class="category__title">Бентонит</h3>
            <p class="category__text">Порошок для буровых растворов, разные марки и фасовки.</p>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-polimer.php">
          <picture><source srcset="img/category-cover-polimery-640.webp 640w, img/category-cover-polimery-960.webp 960w, img/category-cover-polimery.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 66px) / 2), 266px" type="image/webp"><img class="category__img" src="img/category-cover-polimery.jpg" alt="Полимеры и реагенты для бурового раствора ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h3 class="category__title">Полимеры</h3>
            <p class="category__text">Реагенты и добавки для стабилизации скважины.</p>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-ustanovki.php">
          <picture><source srcset="img/category-cover-ustanovki-640.webp 640w, img/category-cover-ustanovki-960.webp 960w, img/category-cover-ustanovki.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 66px) / 2), 266px" type="image/webp"><img class="category__img" src="img/category-cover-ustanovki.jpg" alt="Буровая установка ГНБ на светлом фоне" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h3 class="category__title">Буровые установки</h3>
            <p class="category__text">Машины ГНБ разной мощности — продажа и подбор.</p>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
        <a class="category card" href="category-instrument.php">
          <picture><source srcset="img/product-rasshiritel-640.webp 640w, img/product-rasshiritel-960.webp 960w, img/product-rasshiritel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 66px) / 2), 266px" type="image/webp"><img class="category__img" src="img/product-rasshiritel.jpg" alt="Расширитель — буровой инструмент для ГНБ" width="1280" height="800" loading="lazy" decoding="async"></picture>
          <div class="category__body">
            <h3 class="category__title">Буровой инструмент</h3>
            <p class="category__text">Штанги, расширители, буровые головки, вертлюги.</p>
            <span class="category__link">Смотреть товары →</span>
          </div>
        </a>
      </div>
    </div>
  </section>

  <!-- ПОПУЛЯРНОЕ -->
  <section class="section section--sand">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Популярное</span>
        <h2 class="section__title">Часто заказывают</h2>
        <p class="section__lead">Цену и наличие уточним по телефону под ваш объём — звоните.</p>
      </div>
      <div class="products">
        <article class="product card">
          <a href="product-cetco-ultragel.php">
            <picture>
              <source srcset="img/generated/bentonite-cetco-ultragel-640.webp 640w, img/generated/bentonite-cetco-ultragel-960.webp 960w, img/generated/bentonite-cetco-ultragel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
              <img class="product__img" src="img/generated/bentonite-cetco-ultragel.jpg" alt="CETCO ULTRA-GEL — бентонит для ГНБ, мешок 25 кг" width="1280" height="800" loading="lazy" decoding="async">
            </picture>
          </a>
          <div class="product__body">
            <span class="product__brand">CETCO · бентонит</span>
            <h3 class="product__title"><a href="product-cetco-ultragel.php">CETCO ULTRA-GEL</a></h3>
            <p class="product__text">Натриевый бентонит для приготовления бурового раствора.</p>
            <span class="product__stock"><i></i> В наличии на складе</span>
            <div class="product__row">
              <span class="product__price">Цена <span>по запросу</span></span>
              <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
            </div>
          </div>
        </article>
        <article class="product card">
          <a href="product-rasshiritel.php">
            <picture>
              <source srcset="img/product-rasshiritel-640.webp 640w, img/product-rasshiritel-960.webp 960w, img/product-rasshiritel.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
              <img class="product__img" src="img/product-rasshiritel.jpg" alt="Расширители и бэкримеры для ГНБ" width="1280" height="800" loading="lazy" decoding="async">
            </picture>
          </a>
          <div class="product__body">
            <span class="product__brand">Инструмент</span>
            <h3 class="product__title"><a href="product-rasshiritel.php">Расширители</a></h3>
            <p class="product__text">Под разные грунты и диаметры протяжки.</p>
            <span class="product__stock"><i></i> В наличии на складе</span>
            <div class="product__row">
              <span class="product__price">Цена <span>по запросу</span></span>
              <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
            </div>
          </div>
        </article>
        <article class="product card">
          <a href="product-xcmg-hdd.php">
            <picture>
              <source srcset="img/product-xcmg-hdd-640.webp 640w, img/product-xcmg-hdd-960.webp 960w, img/product-xcmg-hdd.webp 1280w" sizes="(max-width: 620px) calc(100vw - 40px), (max-width: 1000px) calc(100vw - 48px), 360px" type="image/webp">
              <img class="product__img" src="img/product-xcmg-hdd.jpg" alt="Буровые установки XCMG для ГНБ" width="1280" height="800" loading="lazy" decoding="async">
            </picture>
          </a>
          <div class="product__body">
            <span class="product__brand">XCMG · техника</span>
            <h3 class="product__title"><a href="product-xcmg-hdd.php">Буровые установки XCMG</a></h3>
            <p class="product__text">Подбор модели под задачи и бюджет объекта.</p>
            <span class="product__stock"><i></i> В наличии на складе</span>
            <div class="product__row">
              <span class="product__price">Цена <span>по запросу</span></span>
              <a class="btn btn--primary btn--sm" href="tel:+375296526709">Узнать цену</a>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- ЦИФРЫ -->
  <section class="stats">
    <div class="wrap stats__inner">
      <div class="stat"><p class="stat__value">15<em> лет</em></p><p class="stat__label">на рынке ГНБ</p></div>
      <div class="stat"><p class="stat__value">59</p><p class="stat__label">товарных карточек</p></div>
      <div class="stat"><p class="stat__value">РБ<em>·</em>СНГ</p><p class="stat__label">доставка на объект</p></div>
      <div class="stat"><p class="stat__value">Подбор</p><p class="stat__label">под задачу и грунт</p></div>
    </div>
  </section>

  <!-- КАК РАБОТАЕМ -->
  <section class="section section--sand" id="process">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Как работаем</span>
        <h2 class="section__title">От заявки до объекта</h2>
        <p class="section__lead">Простой и понятный порядок — от звонка до доставки.</p>
      </div>
      <div class="steps">
        <div class="step"><p class="step__num">1</p><h3 class="step__title">Заявка</h3><p class="step__text">Звоните или пишете список позиций.</p></div>
        <div class="step"><p class="step__num">2</p><h3 class="step__title">Подбор и цена</h3><p class="step__text">Подбираем товар, готовим КП.</p></div>
        <div class="step"><p class="step__num">3</p><h3 class="step__title">Согласование</h3><p class="step__text">Утверждаем спецификацию и сроки.</p></div>
        <div class="step"><p class="step__num">4</p><h3 class="step__title">Отгрузка</h3><p class="step__text">Комплектуем со склада, документы.</p></div>
        <div class="step"><p class="step__num">5</p><h3 class="step__title">Доставка</h3><p class="step__text">Привозим на объект по РБ и СНГ.</p></div>
      </div>
    </div>
  </section>

  <!-- УСЛУГИ -->
  <section class="section" id="services">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Услуги</span>
        <h2 class="section__title">Наши услуги</h2>
        <p class="section__lead">Закрываем полный цикл снабжения буровых работ.</p>
      </div>
      <div class="services">
        <div class="service card"><span class="service__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 7h13v10H3zM16 10h3l2 3v4h-5M6 20a2 2 0 100-4 2 2 0 000 4zM18 20a2 2 0 100-4 2 2 0 000 4z"/></svg></span><div><h3 class="service__title">Поставка материалов</h3><p class="service__text">Бентонит, полимеры, смазки, трубы — со склада и под заказ.</p></div></div>
        <div class="service card"><span class="service__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 17h4l2-9h6l2 9h4M8 8V5h8v3"/></svg></span><div><h3 class="service__title">Продажа установок</h3><p class="service__text">Подбор буровой техники ГНБ под задачи объекта.</p></div></div>
        <div class="service card"><span class="service__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 4l6 6-3 3-6-6zM11 7L4 14v6h6l7-7"/></svg></span><div><h3 class="service__title">Ремонт инструмента</h3><p class="service__text">Восстановление и обслуживание оснастки.</p></div></div>
        <div class="service card"><span class="service__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 11l3 3 8-8M20 12v6a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h9"/></svg></span><div><h3 class="service__title">Комплектация объектов</h3><p class="service__text">Полный комплект материалов под ваш проект.</p></div></div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section section--sand" id="faq">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Вопросы и ответы</span>
        <h2 class="section__title">Частые вопросы</h2>
      </div>
      <div class="faq">
        <details class="faq__item">
          <summary class="faq__q">Доставляете по всей Беларуси и в СНГ?</summary>
          <p class="faq__a">Да, отгружаем на объект по всей Беларуси и в страны СНГ. Сроки и стоимость уточняем при заказе.</p>
        </details>
        <details class="faq__item">
          <summary class="faq__q">Можно подобрать аналог дешевле?</summary>
          <p class="faq__a">Да, подберём аналог под задачу и бюджет без потери качества — по составу и характеристикам.</p>
        </details>
        <details class="faq__item">
          <summary class="faq__q">Работаете с юрлицами по безналу?</summary>
          <p class="faq__a">Да, по безналичному расчёту, с полным пакетом документов.</p>
        </details>
        <details class="faq__item">
          <summary class="faq__q">Есть товар в наличии на складе?</summary>
          <p class="faq__a">Ходовые позиции держим на складе в Минске. Наличие уточним по телефону за пару минут.</p>
        </details>
      </div>
    </div>
  </section>

  <!-- ОТЗЫВЫ И БЛАГОДАРСТВЕННЫЕ ПИСЬМА -->
  <section class="section" id="reviews">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Отзывы</span>
        <h2 class="section__title">Отзывы заказчиков о нашей работе</h2>
        <p class="section__lead">Благодарственные письма от строительных организаций. Нажмите на документ, чтобы открыть оригинал в полном размере.</p>
      </div>
      <div class="letters">
        <a class="letter" href="img/reviews/hydrogeoservice-letter.jpg" data-review-gallery aria-label="Открыть благодарственное письмо ООО «Гидрогеосервис»">
          <img class="letter__img" src="img/reviews/hydrogeoservice-letter-thumb.webp" alt="Благодарственное письмо ООО «Гидрогеосервис»" width="640" height="905" loading="lazy" decoding="async">
        </a>
        <a class="letter" href="img/reviews/bursetstroy-letter.jpg" data-review-gallery aria-label="Открыть отзыв ООО «Бурсетстрой»">
          <img class="letter__img" src="img/reviews/bursetstroy-letter-thumb.webp" alt="Отзыв ООО «Бурсетстрой» о поставленных материалах и оборудовании" width="640" height="905" loading="lazy" decoding="async">
        </a>
        <a class="letter" href="img/reviews/minskmetrostroy-letter.jpg" data-review-gallery aria-label="Открыть отзыв УП «Минскметрострой»">
          <img class="letter__img" src="img/reviews/minskmetrostroy-letter-thumb.webp" alt="Отзыв УП «Минскметрострой» о поставках бентонита" width="640" height="905" loading="lazy" decoding="async">
        </a>
        <a class="letter" href="img/reviews/proftec-letter.jpg" data-review-gallery aria-label="Открыть отзыв ООО «Новые строительные технологии ПрофТэк»">
          <img class="letter__img" src="img/reviews/proftec-letter-thumb.webp" alt="Отзыв ООО «Новые строительные технологии ПрофТэк» о поставленных материалах" width="640" height="905" loading="lazy" decoding="async">
        </a>
      </div>
      <p class="letters__note">Оригиналы писем опубликованы без изменения содержания.</p>
    </div>
  </section>

  <!-- ЗАЯВКА -->
  <section class="lead-section" id="lead">
    <div class="wrap">
      <div class="lead">
        <div>
          <h2 class="lead__title">Нужен прайс или подбор под объект?</h2>
          <p class="lead__text">Позвоните — ответим в рабочее время. Или оставьте телефон, перезвоним сами.</p>
          <a class="lead__phone" href="tel:+375296526709"><svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>+375 29 652-67-09</a>
        </div>
        <div>
          <form class="form" data-lead-form>
            <input type="hidden" name="csrf" value="<?= e($csrf_token) ?>">
            <input type="hidden" name="product" value="Общая заявка с главной страницы">
            <div class="form__honeypot" aria-hidden="true"><label>Не заполняйте это поле <input name="company" type="text" tabindex="-1" autocomplete="off"></label></div>
            <label class="form__label" for="lead-name">Ваше имя</label>
            <input class="form__input" id="lead-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name">
            <label class="form__label" for="lead-phone">Телефон</label>
            <input class="form__input" id="lead-phone" name="phone" type="tel" placeholder="+375 __ ___-__-__" autocomplete="tel" inputmode="tel" minlength="7" required>
            <label class="form__consent">
              <input type="checkbox" class="form__consent-check" name="consent" value="1" data-consent required>
              <span>Я согласен на обработку персональных данных и принимаю <a href="policy.php" target="_blank" rel="noopener noreferrer">политику конфиденциальности</a></span>
            </label>
            <p class="form__status" data-form-status aria-live="assertive"></p>
            <button class="btn btn--primary btn--block" type="submit">Перезвоните мне</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
