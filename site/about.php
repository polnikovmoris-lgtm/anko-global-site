<?php
$page_title = 'О компании ANKO GLOBAL — поставщик для ГНБ в Беларуси';
$page_desc = 'ANKO GLOBAL поставляет материалы, оборудование и оснастку для ГНБ с 2011 года. Склад в Минске, поставки по Беларуси и СНГ.';
$canonical = 'about.php';
$extra_head = <<<'HTML'
<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","@id":"https://ankoglobal.by/about.php#webpage","name":"О компании ANKO GLOBAL","url":"https://ankoglobal.by/about.php","isPartOf":{"@id":"https://ankoglobal.by/#website"},"mainEntity":{"@id":"https://ankoglobal.by/#organization"}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://ankoglobal.by/"},{"@type":"ListItem","position":2,"name":"О компании","item":"https://ankoglobal.by/about.php"}]}</script>
HTML;
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <nav class="crumbs" aria-label="Хлебные крошки"><div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span>О компании</div></nav>
  <section class="section"><div class="wrap info-page">
    <span class="eyebrow">ANKO GLOBAL</span>
    <h1>Материалы и оборудование для ГНБ — с пониманием задач на объекте</h1>
    <p class="section__lead">Мы поставляем материалы, технику и оснастку для горизонтально направленного бурения с 2011 года. Работаем с подрядчиками, строительными и коммунальными организациями в Беларуси и странах СНГ.</p>
    <h2>Чем помогаем</h2>
    <ul class="bullets"><li>Подбираем буровой раствор, инструмент и технику под грунт, тип перехода и бюджет.</li><li>Поставляем ходовые материалы со склада в Минске и позиции под заказ.</li><li>Комплектуем объект: от бентонита и полимеров до труб, расширителей и локации.</li><li>Оформляем поставки для юридических лиц с безналичным расчётом и комплектом документов.</li></ul>
    <h2>Прозрачный подбор вместо универсальных обещаний</h2>
    <p>Для точного предложения менеджеру нужны исходные данные: тип грунта, диаметр и длина перехода, модель установки, срок поставки и требуемый объём. Это позволяет предложить совместимые позиции и заранее назвать условия поставки.</p>
    <h2>Контакты и реквизиты</h2>
    <p>ANKO GLOBAL · <?= e($SITE['company']) ?> · УНП <?= e($SITE['unp']) ?>.<br><?= e($SITE['address_full']) ?>.<br>Телефон: <a href="tel:<?= e($phone_main['raw']) ?>"><?= e($phone_main['show']) ?></a> · <a href="mailto:<?= e($SITE['email']) ?>"><?= e($SITE['email']) ?></a>.</p>
    <p><a class="btn btn--primary" href="contacts.php">Связаться с нами</a></p>
  </div></section>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
