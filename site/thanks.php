<?php
$page_title = 'Заявка принята — спасибо! | ANKO GLOBAL';
$page_desc  = 'Спасибо за заявку. Менеджер ANKO GLOBAL перезвонит вам в рабочее время.';
$canonical  = 'thanks.php';
$robots = 'noindex,follow';
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <div class="thanks">
    <div class="wrap thanks__inner">
      <div class="thanks__icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
      </div>
      <h1 class="thanks__title">Спасибо! Заявка принята</h1>
      <p class="thanks__text">Мы получили вашу заявку и перезвоним в рабочее время — Пн–Пт с 9:00 до 21:00. Если вопрос срочный, позвоните сами.</p>
      <a class="thanks__phone" href="tel:+375296526709">+375 29 652-67-09</a>
      <div class="thanks__actions">
        <a class="btn btn--primary" href="catalog.php">Вернуться в каталог</a>
        <a class="btn btn--outline" href="index.php">На главную</a>
      </div>
    </div>
  </div>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
