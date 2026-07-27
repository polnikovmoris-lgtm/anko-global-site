<?php
$page_title = 'Контакты ANKO GLOBAL — телефоны, адрес, реквизиты | Минск';
$page_desc  = 'Контакты ANKO GLOBAL: три телефона, факс, email, адрес склада в Тарасово под Минском. Работаем Пн–Пт 9:00–21:00. Поставки для ГНБ по Беларуси и СНГ.';
$canonical  = 'contacts.php';
$active     = 'contacts';
$extra_head = <<<'HTML'
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","@id":"https://ankoglobal.by/#organization","name":"ANKO GLOBAL","alternateName":"ООО «Анко-глобал»",
"url":"https://ankoglobal.by/","telephone":["+375296526709","+375296399139","+375296399972"],
"faxNumber":"+375175156000","email":"main.accentline@gmail.com","foundingDate":"2011",
"address":{"@type":"PostalAddress","streetAddress":"пер. 2-ой Школьный, д. 1А-1, пом. 14, д. Тарасово",
"addressRegion":"Минская область","postalCode":"223015","addressCountry":"BY"},
"openingHoursSpecification":{"@type":"OpeningHoursSpecification",
"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
"opens":"09:00","closes":"21:00"},
"areaServed":["BY","RU","KZ"]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Главная","item":"https://ankoglobal.by/"},
{"@type":"ListItem","position":2,"name":"Контакты","item":"https://ankoglobal.by/contacts.php"}]}
</script>
HTML;
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <nav class="crumbs" aria-label="Хлебные крошки">
    <div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span>Контакты</div>
  </nav>

  <div class="wrap page-head">
    <span class="eyebrow">Контакты</span>
    <h1 class="page-head__title">Свяжитесь с нами</h1>
    <p class="page-head__text">Звоните в рабочее время — ответим и подберём позицию под вашу задачу. Если не дозвонились, оставьте заявку: перезвоним сами.</p>
  </div>

  <!-- ТЕЛЕФОНЫ -->
  <section class="section section--tight">
    <div class="wrap">
      <h2 class="section__subtitle section__subtitle--first">Телефоны</h2>
      <div class="contact-grid">
          <a class="contact-card" href="tel:+375296526709">
            <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg></span>
            <span class="contact-card__body">
              <span class="contact-card__label">Основной</span>
              <span class="contact-card__value">+375 29 652-67-09</span>
            </span>
          </a>
          <a class="contact-card" href="tel:+375296399139">
            <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg></span>
            <span class="contact-card__body">
              <span class="contact-card__label">Дополнительный</span>
              <span class="contact-card__value">+375 29 639-91-39</span>
            </span>
          </a>
          <a class="contact-card" href="tel:+375296399972">
            <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg></span>
            <span class="contact-card__body">
              <span class="contact-card__label">Дополнительный</span>
              <span class="contact-card__value">+375 29 639-99-72</span>
            </span>
          </a>
        <div class="contact-card contact-card--static">
          <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2M6 14h12v8H6z"/></svg></span>
          <span class="contact-card__body">
            <span class="contact-card__label">Факс</span>
            <span class="contact-card__value">+375 17 515-60-00</span>
          </span>
        </div>
      </div>

      <h2 class="section__subtitle">Почта, адрес и режим работы</h2>
      <div class="contact-grid">
        <a class="contact-card" href="mailto:main.accentline@gmail.com">
          <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16v16H4zM4 6l8 6 8-6"/></svg></span>
          <span class="contact-card__body">
            <span class="contact-card__label">Электронная почта</span>
            <span class="contact-card__value contact-card__value--sm">main.accentline@gmail.com</span>
          </span>
        </a>
        <div class="contact-card contact-card--static">
          <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span>
          <span class="contact-card__body">
            <span class="contact-card__label">Режим работы</span>
            <span class="contact-card__value contact-card__value--sm">Пн–Пт 9:00–21:00</span>
          </span>
        </div>
        <div class="contact-card contact-card--static contact-card--wide">
          <span class="contact-card__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-6 8-12a8 8 0 10-16 0c0 6 8 12 8 12z"/><circle cx="12" cy="10" r="3"/></svg></span>
          <span class="contact-card__body">
            <span class="contact-card__label">Адрес склада и офиса</span>
            <span class="contact-card__value contact-card__value--sm">223015, Минская область, Минский район, д. Тарасово, переулок 2-ой Школьный, д. 1А-1, пом. 14</span>
          </span>
        </div>
      </div>
    </div>
  </section>

  <!-- КАРТА -->
  <section class="section section--sand">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Как добраться</span>
        <h2 class="section__title">Мы находимся в Тарасово</h2>
        <p class="section__lead">Это Минский район, недалеко от МКАД. Точку на карте пришлём в мессенджере — позвоните, объясним дорогу.</p>
      </div>

      <div class="map-block">
        <div class="map-block__route">
          <span class="map-block__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-6 8-12a8 8 0 10-16 0c0 6 8 12 8 12z"/><circle cx="12" cy="10" r="3"/></svg></span>
          <p class="map-block__title">Построить маршрут до ANKO GLOBAL</p>
          <p class="map-block__text">Откройте адрес склада и офиса в удобном картографическом сервисе.</p>
          <p class="map-block__addr">д. Тарасово, пер. 2-ой Школьный, 1А-1</p>
          <div class="map-block__actions">
            <a class="btn btn--primary btn--sm" href="https://yandex.by/maps/?text=223015%2C%20%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%2C%20%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9%20%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%2C%20%D0%B4.%20%D0%A2%D0%B0%D1%80%D0%B0%D1%81%D0%BE%D0%B2%D0%BE%2C%20%D0%BF%D0%B5%D1%80.%202-%D0%BE%D0%B9%20%D0%A8%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%2C%201%D0%90-1" target="_blank" rel="noopener noreferrer">Яндекс Карты</a>
            <a class="btn btn--outline btn--sm" href="https://www.google.com/maps/search/?api=1&amp;query=223015%2C%20%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%2C%20%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9%20%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%2C%20%D0%B4.%20%D0%A2%D0%B0%D1%80%D0%B0%D1%81%D0%BE%D0%B2%D0%BE%2C%20%D0%BF%D0%B5%D1%80.%202-%D0%BE%D0%B9%20%D0%A8%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%2C%201%D0%90-1" target="_blank" rel="noopener noreferrer">Google Maps</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- РЕКВИЗИТЫ -->
  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <span class="eyebrow">Для договора</span>
        <h2 class="section__title">Реквизиты</h2>
        <p class="section__lead">Работаем с юридическими лицами по безналичному расчёту. Предоставляем полный пакет документов.</p>
      </div>

      <div class="table-scroll" role="region" aria-label="Реквизиты компании" tabindex="0"><table class="spec-table spec-table--wide">
        <tbody>
          <tr><th scope="row">Наименование</th><td>ООО «Анко-глобал»</td></tr>
          <tr><th scope="row">УНП</th><td>693415351</td></tr>
          <tr><th scope="row">Юридический адрес</th><td>223015, Минская область, Минский район, д. Тарасово, переулок 2-ой Школьный, д. 1А-1, пом. 14</td></tr>
          <tr><th scope="row">Телефон</th><td>+375 29 652-67-09</td></tr>
          <tr><th scope="row">Факс</th><td>+375 17 515-60-00</td></tr>
          <tr><th scope="row">Электронная почта</th><td>main.accentline@gmail.com</td></tr>
        </tbody>
      </table></div>
      <p class="table-note">Банковские реквизиты, свидетельство и полный комплект документов вышлем по запросу — напишите на почту или позвоните.</p>
    </div>
  </section>

  <!-- ЗАЯВКА -->
  <section class="lead-section" id="lead">
    <div class="wrap">
      <div class="lead">
        <div>
          <h2 class="lead__title">Не дозвонились? Оставьте заявку</h2>
          <p class="lead__text">Перезвоним в рабочее время. Опишите задачу — подберём материалы, инструмент или технику под ваш объект.</p>
          <a class="lead__phone" href="tel:+375296526709"><svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>+375 29 652-67-09</a>
          <p class="lead__hours">Пн–Пт 9:00–21:00</p>
        </div>
        <div>
          <form class="form" data-lead-form>
            <input type="hidden" name="csrf" value="<?= e($csrf_token) ?>">
            <input type="hidden" name="product" value="Заявка со страницы контактов">
            <div class="form__honeypot" aria-hidden="true"><label>Не заполняйте это поле <input name="company" type="text" tabindex="-1" autocomplete="off"></label></div>
            <label class="form__label" for="c-name">Ваше имя</label>
            <input class="form__input" id="c-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name">

            <label class="form__label" for="c-phone">Телефон <span class="form__req">*</span></label>
            <input class="form__input" id="c-phone" name="phone" type="tel" placeholder="+375 __ ___-__-__" autocomplete="tel" inputmode="tel" minlength="7" required>

            <label class="form__label" for="c-msg">Что нужно?</label>
            <textarea class="form__input form__input--area" id="c-msg" name="message" rows="3" placeholder="Например: бентонит 5 тонн, доставка в Гомель"></textarea>

            <label class="form__consent">
              <input type="checkbox" class="form__consent-check" name="consent" value="1" data-consent required>
              <span>Я согласен на обработку персональных данных и принимаю <a href="policy.php" target="_blank" rel="noopener noreferrer">политику конфиденциальности</a></span>
            </label>
            <p class="form__status" data-form-status aria-live="assertive"></p>
            <button class="btn btn--primary btn--block" type="submit">Отправить заявку</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
