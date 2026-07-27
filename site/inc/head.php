<?php
/* ==========================================================================
   ОБЩАЯ ВЕРХНЯЯ ЧАСТЬ: <head> + шапка сайта
   --------------------------------------------------------------------------
   Каждая страница ПЕРЕД подключением этого файла задаёт свои переменные:

     $page_title  — <title> страницы (уникальный!)
     $page_desc   — meta description (уникальный!)
     $canonical   — канонический URL страницы, напр. 'catalog.html' или ''
     $og_image    — (необяз.) картинка для соцсетей, по умолчанию og-image.jpg
     $extra_head  — (необяз.) доп. теги в <head>: JSON-LD, noindex и т.п.
     $active      — (необяз.) активный пункт меню: catalog|contacts|''
     $body_scripts— (необяз.) доп. скрипты перед </body> (напр. search.js)

   Затем:  require 'inc/head.php';
   ========================================================================== */

require_once __DIR__ . '/config.php';

$page_title   = $page_title   ?? $SITE['name'];
$page_desc    = $page_desc    ?? '';
$canonical    = $canonical    ?? '';
$og_image     = $og_image     ?? 'img/og-image.jpg';
$og_type      = $og_type      ?? 'website';
$og_image_alt = $og_image_alt ?? $page_title;
$robots       = $robots       ?? 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1';
$preload_image = $preload_image ?? '';
$preload_srcset = $preload_srcset ?? '';
$preload_sizes = $preload_sizes ?? '(max-width: 620px) calc(100vw - 68px), (max-width: 1000px) calc(100vw - 88px), 520px';
$extra_head   = $extra_head   ?? '';
$active       = $active       ?? '';
$phone_main   = $SITE['phones'][0];

/* CSP вводится безопасно в два этапа. По умолчанию браузер только сообщает
   о нарушениях в консоли. После проверки опубликованного сайта установите
   переменную окружения CSP_ENFORCE=1, чтобы включить блокировку. */
$csp_nonce = base64_encode(random_bytes(18));
$csp_script_sources = ["'self'", "'nonce-" . $csp_nonce . "'"];
$csp_connect_sources = ["'self'"];
$csp_image_sources = ["'self'", 'data:'];
if (!empty($SITE['metrika_id'])) {
    $csp_script_sources[] = 'https://mc.yandex.ru';
    $csp_script_sources[] = 'https://mc.yandex.com';
    $csp_script_sources[] = 'https://yastatic.net';
    $csp_connect_sources[] = 'https://mc.yandex.ru';
    $csp_connect_sources[] = 'https://mc.yandex.com';
    $csp_image_sources[] = 'https://mc.yandex.ru';
    $csp_image_sources[] = 'https://mc.yandex.com';
}
if (!empty($SITE['ga_id'])) {
    $csp_script_sources[] = 'https://www.googletagmanager.com';
    $csp_connect_sources[] = 'https://*.google-analytics.com';
    $csp_image_sources[] = 'https://*.google-analytics.com';
}
$csp = implode('; ', [
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "frame-ancestors 'self'",
    "form-action 'self'",
    'script-src ' . implode(' ', array_unique($csp_script_sources)),
    "style-src 'self'",
    "font-src 'self' data:",
    'img-src ' . implode(' ', array_unique($csp_image_sources)),
    'connect-src ' . implode(' ', array_unique($csp_connect_sources)),
    "frame-src 'none'",
    "upgrade-insecure-requests",
]);
if (!headers_sent()) {
    $csp_header = getenv('CSP_ENFORCE') === '1'
        ? 'Content-Security-Policy'
        : 'Content-Security-Policy-Report-Only';
    header($csp_header . ': ' . $csp);
}
$extra_head = preg_replace(
    '/<script\b(?![^>]*\bnonce=)/i',
    '<script nonce="' . e($csp_nonce) . '"',
    (string) $extra_head
) ?? (string) $extra_head;


$og_width = 1200;
$og_height = 630;
$og_mime = 'image/jpeg';
$og_local = dirname(__DIR__) . '/' . ltrim($og_image, '/');
if (is_file($og_local)) {
    $og_info = @getimagesize($og_local);
    if (is_array($og_info)) {
        $og_width = (int) ($og_info[0] ?? $og_width);
        $og_height = (int) ($og_info[1] ?? $og_height);
        $og_mime = (string) ($og_info['mime'] ?? $og_mime);
    }
}

function nav_class($name, $active) {
    return $name === $active ? 'nav__link nav__link--active' : 'nav__link';
}

// SVG телефона (используется в шапке и мобильной панели)
$PHONE_SVG = '<svg class="btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.6A2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.8a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6a2 2 0 011.7 2z"/></svg>';
?><!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($page_title) ?></title>
<meta name="description" content="<?= e($page_desc) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<meta name="theme-color" content="#0c3454">
<?php if ($canonical !== ''): ?>
<link rel="canonical" href="<?= e($SITE['domain'] . '/' . ltrim($canonical, '/')) ?>">
<?php endif; ?>
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="<?= e($og_type) ?>">
<meta property="og:locale" content="ru_BY">
<meta property="og:title" content="<?= e($page_title) ?>">
<meta property="og:description" content="<?= e($page_desc) ?>">
<meta property="og:image" content="<?= e($SITE['domain'] . '/' . ltrim($og_image, '/')) ?>">
<meta property="og:image:type" content="<?= e($og_mime) ?>">
<meta property="og:image:width" content="<?= e((string) $og_width) ?>">
<meta property="og:image:height" content="<?= e((string) $og_height) ?>">
<meta property="og:image:alt" content="<?= e($og_image_alt) ?>">
<meta property="og:site_name" content="ANKO GLOBAL">
<?php if ($canonical !== ''): ?><meta property="og:url" content="<?= e($SITE['domain'] . '/' . ltrim($canonical, '/')) ?>"><?php else: ?><meta property="og:url" content="<?= e($SITE['domain'] . '/') ?>"><?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page_title) ?>">
<meta name="twitter:description" content="<?= e($page_desc) ?>">
<meta name="twitter:image" content="<?= e($SITE['domain'] . '/' . ltrim($og_image, '/')) ?>">
<meta name="twitter:image:alt" content="<?= e($og_image_alt) ?>">
<?php if ($preload_image !== ''): ?>
<link rel="preload" as="image" href="<?= e($preload_image) ?>"<?php if ($preload_srcset !== ''): ?> imagesrcset="<?= e($preload_srcset) ?>" imagesizes="<?= e($preload_sizes) ?>"<?php endif; ?>>
<?php endif; ?>
<link rel="stylesheet" href="css/style.css?v=20260726-v26">
<?= $extra_head ?>
<?php
// Яндекс.Метрика — подключается только если задан ID в config.php
if (!empty($SITE['metrika_id'])):
    $mid = $SITE['metrika_id'];
?>
<script type="text/javascript" nonce="<?= e($csp_nonce) ?>">
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym(<?= e($mid) ?>,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true});
window.METRIKA_ID = <?= e($mid) ?>;
</script>
<noscript><div><img class="analytics-pixel" src="https://mc.yandex.ru/watch/<?= e($mid) ?>" alt=""></div></noscript>
<?php endif; ?>
<?php if (!empty($SITE['ga_id'])): $ga = $SITE['ga_id']; ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= e($ga) ?>"></script>
<script nonce="<?= e($csp_nonce) ?>">window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());gtag('config','<?= e($ga) ?>');</script>
<?php endif; ?>
</head>
<body>
<a class="skip-link" href="#main-content">Перейти к содержимому</a>

<header class="header">
  <div class="wrap header__inner">
    <a class="logo-link" href="index.php">
      <img class="logo-img" src="img/logo.svg" alt="ANKO GLOBAL — поставки для ГНБ" width="188" height="42">
    </a>
    <nav class="nav">
      <a class="<?= nav_class('catalog', $active) ?>" href="catalog.php">Каталог</a>
      <a class="nav__link" href="index.php#services">Услуги</a>
      <a class="nav__link" href="index.php#process">Как работаем</a>
      <a class="nav__link" href="about.php">О компании</a>
      <a class="<?= nav_class('contacts', $active) ?>" href="contacts.php">Контакты</a>
    </nav>
    <div class="header__right">
      <a class="header__phone" href="tel:<?= e($phone_main['raw']) ?>"><?= e($phone_main['show']) ?><small><?= e($SITE['hours']) ?></small></a>
      <a class="btn btn--call btn--icon-mobile" href="tel:<?= e($phone_main['raw']) ?>"><?= $PHONE_SVG ?>Позвонить</a>
      <button class="burger" type="button" data-menu-toggle aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <nav class="mobile-menu" id="mobile-menu" data-menu aria-hidden="true">
    <a href="catalog.php">Каталог</a>
    <a href="index.php#services">Услуги</a>
    <a href="index.php#process">Как работаем</a>
    <a href="index.php#reviews">Отзывы</a>
    <a href="about.php">О компании</a>
    <a href="contacts.php">Контакты</a>
  </nav>
</header>
