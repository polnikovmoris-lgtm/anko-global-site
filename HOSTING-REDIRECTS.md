# ANKO GLOBAL — домены и редиректы

## Канонический адрес

Основной домен сайта:

`https://ankoglobal.by`

В папке `site/` все canonical, Open Graph, Schema.org, Sitemap и robots.txt
переведены на этот адрес.

## Если оба домена подключены к одному корню сайта

Загрузите содержимое `site/` в корень сайта и подключите к этому корню:

- `ankoglobal.by`;
- `www.ankoglobal.by`;
- `a-line.by`;
- `www.a-line.by`.

Файл `site/.htaccess` выполняет постоянный редирект `301` со старого домена
на `https://ankoglobal.by`, сохраняя путь и параметры запроса.

Пример:

`https://a-line.by/catalog.php?from=old`

перенаправляется на:

`https://ankoglobal.by/catalog.php?from=old`

## Если a-line.by находится на отдельном хостинге

Установите файл `hosting/a-line.by/.htaccess` в корень старого сайта. Не
переносите туда остальные файлы новой сборки.

## Что обязательно настроить в панели хостинга

1. Направить DNS-записи `ankoglobal.by` и `www.ankoglobal.by` на новый сервер.
2. Подключить `a-line.by` и `www.a-line.by` как алиасы того же сайта либо
   установить отдельный redirect-файл из этой сборки на старом хостинге.
3. Выпустить действующие SSL-сертификаты для обоих доменов до включения
   постоянного редиректа.
4. Проверить, что переменная `LEAD_TO_EMAIL`, если она задана в панели,
   содержит `main.accentline@gmail.com`. В коде это уже адрес по умолчанию.

## Контроль после публикации

Проверить ответы без перехода на промежуточные адреса:

- `http://a-line.by/` → `301` → `https://ankoglobal.by/`;
- `https://a-line.by/catalog.php` → `301` →
  `https://ankoglobal.by/catalog.php`;
- `https://www.ankoglobal.by/` → `301` → `https://ankoglobal.by/`;
- `http://ankoglobal.by/` → `301` → `https://ankoglobal.by/`;
- `https://ankoglobal.by/` → `200`.
