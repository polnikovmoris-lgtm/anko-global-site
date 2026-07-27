<?php
/* ==========================================================================
   ОБЩАЯ НИЖНЯЯ ЧАСТЬ: футер + мобильная панель звонка + куки + скрипты
   --------------------------------------------------------------------------
   Страница перед подключением может задать:
     $body_scripts — доп. скрипты (напр. '<script src="js/search.js?v=20260726-v26"></script>')
   Затем:  require 'inc/footer.php';
   ========================================================================== */

$body_scripts = $body_scripts ?? '';
$phone_main   = $SITE['phones'][0];
$PHONE_SVG    = $PHONE_SVG ?? '<svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>';
?>
<footer class="footer" id="contacts">
  <div class="wrap">
    <div class="footer__inner">
      <div>
        <div class="footer__logo">
          <img class="logo-img logo-img--footer" src="img/logo-white.svg" alt="<?= e($SITE['name']) ?>" width="155" height="35">
        </div>
        <p class="footer__about">Поставщик материалов и оборудования для горизонтально направленного бурения. 15 лет на рынке. Минск, Беларусь.</p>
      </div>
      <div>
        <p class="footer__title">Каталог</p>
        <ul class="footer__list">
          <li><a href="category-bentonit.php">Бентониты</a></li>
          <li><a href="category-polimer.php">Полимеры</a></li>
          <li><a href="category-ustanovki.php">Буровые установки</a></li>
          <li><a href="category-instrument.php">Буровой инструмент</a></li>
          <li><a href="catalog.php">Весь каталог</a></li>
        </ul>
      </div>
      <div>
        <p class="footer__title">Компания</p>
        <ul class="footer__list">
          <li><a href="about.php">О компании</a></li>
          <li><a href="index.php#reviews">Отзывы</a></li>
          <li><a href="delivery.php">Доставка и оплата</a></li>
          <li><a href="contacts.php">Контакты</a></li>
        </ul>
      </div>
      <div>
        <p class="footer__title">Контакты</p>
        <?php foreach ($SITE['phones'] as $ph): ?>
        <a class="footer__phone" href="tel:<?= e($ph['raw']) ?>"><?= e($ph['show']) ?></a>
        <?php endforeach; ?>
        <p class="footer__contacts">
          Факс: <?= e($SITE['fax']) ?><br>
          <a href="mailto:<?= e($SITE['email']) ?>"><?= e($SITE['email']) ?></a><br>
          <?= e($SITE['address_full']) ?><br>
          <?= e($SITE['hours']) ?>
        </p>
      </div>
    </div>
    <p class="footer__bar">© <?= date('Y') ?> <?= e($SITE['name']) ?> · <?= e($SITE['company']) ?> · УНП <?= e($SITE['unp']) ?> · <a href="policy.php">Политика конфиденциальности</a></p>
  </div>
</footer>

<div class="callbar">
  <a class="callbar__btn callbar__btn--primary" href="tel:<?= e($phone_main['raw']) ?>"><?= $PHONE_SVG ?>Позвонить</a>
  <button class="callbar__btn callbar__btn--outline" type="button" data-kp-open>Заявка</button>
</div>

<div class="cookie" data-cookie role="region" aria-label="Уведомление о cookie" hidden>
  <p class="cookie__text">Мы используем файлы cookie, чтобы сайт работал лучше. Продолжая пользоваться сайтом, вы соглашаетесь с <a href="policy.php">политикой конфиденциальности</a>.</p>
  <button class="cookie__btn" type="button" data-cookie-ok>ОК</button>
</div>


<!-- Модальное окно "Запросить КП" -->
<div class="modal" data-kp-modal hidden>
  <div class="modal__overlay" data-kp-close></div>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="kp-title" aria-describedby="kp-description">
    <button class="modal__close" type="button" data-kp-close aria-label="Закрыть">&times;</button>
    <h2 class="modal__title" id="kp-title">Запросить коммерческое предложение</h2>
    <p class="modal__sub" id="kp-description" data-kp-product>Оставьте контакты — пришлём цену и условия.</p>
    <form class="form" data-lead-form>
      <input type="hidden" name="csrf" value="<?= e($csrf_token) ?>">
      <input type="hidden" name="product" data-kp-product-field value="">
      <div class="form__honeypot" aria-hidden="true">
        <label>Не заполняйте это поле <input name="company" type="text" tabindex="-1" autocomplete="off"></label>
      </div>
      <label class="form__label" for="kp-name">Ваше имя</label>
      <input class="form__input" id="kp-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name">
      <label class="form__label" for="kp-phone">Телефон <span class="form__req">*</span></label>
      <input class="form__input" id="kp-phone" name="phone" type="tel" placeholder="+375 __ ___-__-__" autocomplete="tel" inputmode="tel" minlength="7" required>
      <label class="form__label" for="kp-msg">Комментарий</label>
      <textarea class="form__input form__input--area" id="kp-msg" name="message" rows="2" placeholder="Объём, доставка, вопросы"></textarea>
      <label class="form__consent">
        <input type="checkbox" class="form__consent-check" name="consent" value="1" data-consent required>
        <span>Согласен на обработку данных и принимаю <a href="policy.php" target="_blank" rel="noopener noreferrer">политику конфиденциальности</a></span>
      </label>
      <p class="form__status" data-form-status aria-live="assertive"></p>
      <button class="btn btn--primary btn--block" type="submit">Отправить заявку</button>
    </form>
  </div>
</div>


<!-- Галерея отзывов: открывается поверх страницы, без новой вкладки -->
<div class="review-lightbox" data-review-lightbox hidden>
  <div class="review-lightbox__backdrop" data-review-close></div>
  <div class="review-lightbox__dialog" role="dialog" aria-modal="true" aria-labelledby="review-lightbox-title">
    <h2 class="visually-hidden" id="review-lightbox-title">Благодарственное письмо</h2>
    <button class="review-lightbox__close" type="button" data-review-close aria-label="Закрыть галерею">&times;</button>
    <button class="review-lightbox__nav review-lightbox__prev" type="button" data-review-prev aria-label="Предыдущее письмо">&#8249;</button>
    <figure class="review-lightbox__figure">
      <img class="review-lightbox__image" data-review-image src="img/reviews/hydrogeoservice-letter-thumb.webp" alt="" width="1240" height="1754">
      <figcaption class="review-lightbox__caption" data-review-caption></figcaption>
    </figure>
    <button class="review-lightbox__nav review-lightbox__next" type="button" data-review-next aria-label="Следующее письмо">&#8250;</button>
    <p class="review-lightbox__counter" data-review-counter aria-live="polite"></p>
  </div>
</div>

<script src="js/main.js?v=20260726-v26"></script>
<script src="js/product-galleries.js?v=20260726-v26"></script>
<?= $body_scripts ?>
</body>
</html>
