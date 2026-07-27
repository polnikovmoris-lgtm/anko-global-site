<?php
$page_title = 'Доставка и оплата — ANKO GLOBAL';
$page_desc = 'Условия поставки материалов и оборудования для ГНБ: отгрузка из Минска и под заказ, доставка по Беларуси и СНГ, безналичный расчёт для юридических лиц.';
$canonical = 'delivery.php';
$extra_head = <<<'HTML'
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Доставка и оплата — ANKO GLOBAL","url":"https://ankoglobal.by/delivery.php"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://ankoglobal.by/"},{"@type":"ListItem","position":2,"name":"Доставка и оплата","item":"https://ankoglobal.by/delivery.php"}]}</script>
HTML;
require __DIR__ . '/inc/head.php';
?>
<main id="main-content">
  <nav class="crumbs" aria-label="Хлебные крошки"><div class="wrap"><a href="index.php">Главная</a><span class="crumbs__sep">/</span>Доставка и оплата</div></nav>
  <section class="section"><div class="wrap info-page">
    <span class="eyebrow">Условия поставки</span>
    <h1>Доставка и оплата</h1>
    <p class="section__lead">Отгружаем материалы и оборудование для ГНБ со склада в Минске и организуем поставку под заказ. Работаем с юридическими лицами по безналичному расчёту.</p>
    <h2>Как оформить заказ</h2>
    <ol class="steps order-steps"><li>Сообщите, что требуется: наименование, объём, параметры объекта и адрес поставки.</li><li>Мы уточним наличие, совместимость и срок поставки, затем подготовим коммерческое предложение.</li><li>После согласования условий оформляем документы и согласовываем отгрузку или доставку.</li></ol>
    <h2>Доставка</h2>
    <p>Доставка возможна по Беларуси и в страны СНГ. Срок и стоимость зависят от веса, габаритов, точки разгрузки и наличия товара. Для буровых установок, труб и крупногабаритных партий логистику согласовываем индивидуально.</p>
    <h2>Оплата и документы</h2>
    <p>Работаем с юридическими лицами по безналичному расчёту. По запросу подготовим счёт, договор и комплект закрывающих документов. Точные условия оплаты и поставки фиксируются в коммерческом предложении или договоре.</p>
    <h2>Что указать в заявке</h2>
    <p>Добавьте к заявке тип грунта, длину и диаметр перехода, модель установки, нужное количество и город доставки. Это ускорит подбор и поможет избежать несовместимости материалов и оснастки.</p>
    <p><button class="btn btn--primary" type="button" data-kp-open>Запросить коммерческое предложение</button></p>
  </div></section>
</main>
<?php require __DIR__ . '/inc/footer.php'; ?>
