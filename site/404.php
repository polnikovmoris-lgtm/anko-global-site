<?php
http_response_code(404);
$page_title = 'Страница не найдена — ANKO GLOBAL';
$page_desc = 'Запрошенная страница не найдена. Перейдите в каталог ANKO GLOBAL или свяжитесь с нами.';
$canonical = '';
$robots = 'noindex,follow';
require __DIR__ . '/inc/head.php';
?>
<main id="main-content"><section class="section"><div class="wrap pdp-content"><span class="eyebrow">Ошибка 404</span><h1>Страница не найдена</h1><p>Возможно, ссылка устарела или адрес введён с ошибкой.</p><p><a class="btn btn--primary" href="catalog.php">Перейти в каталог</a> <a class="btn btn--outline" href="contacts.php">Связаться с нами</a></p></div></section></main>
<?php require __DIR__ . '/inc/footer.php'; ?>
