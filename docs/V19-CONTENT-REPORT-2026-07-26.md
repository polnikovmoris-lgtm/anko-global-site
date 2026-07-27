# ANKO GLOBAL v19 — контентная доработка товарных карточек

Дата: 26 июля 2026 года  
Основа: отдельная проверенная сборка v18  
Область изменений: только контент 34 товарных карточек и документация сборки

## Результат

Закрыта оставшаяся задача `CONTENT-01` из аудита v17/v18. Все 34 карточки,
которые содержали менее 180 видимых слов, получили самостоятельные полезные
блоки. Диагностический фильтр повторно запущен: страниц ниже порога не осталось,
минимальный объём составляет 180 слов, медиана по 68 товарам — 203 слова.

Порог используется только как средство поиска слабых страниц. Тексты не
дополнялись механически до заданного объёма: каждая вставка описывает
назначение, проверку источника, исходные данные для подбора, совместимость,
комплектность или ограничения публикации.

## Принцип достоверности

- Для CETCO, Baroid, BAULUX/Bentolux, Goodeng, КЗБО и Normet использованы
  официальные страницы производителей.
- В карточках добавлены прямые ссылки на официальные источники и дата проверки,
  когда источник однозначно относится к конкретному продукту.
- Для FDP и PolymersPlus не опубликованы неподтверждённые модели, дозировки и
  паспортные числа. Карточки прямо требуют TDS/SDS или паспорт конкретной
  поставки.
- Для инструмента без закреплённого производителя добавлены не характеристики,
  а конкретные данные, необходимые для идентификации и согласования
  совместимости: модель установки, артикул, резьба, размеры, чертёж и фото
  маркировки.
- Цены, наличие, гарантии, сертификаты, рейтинги и коммерческие статусы не
  придумывались и не менялись.

## Официальные источники

| Группа | Источник |
|---|---|
| Baroid TUNNEL-GEL PLUS | https://www.baroididp.com/en/products/tunnel-gel-plus |
| CETCO HYDRAUL-EZ | https://www.mineralstech.com/cetco/drilling-products/drilling-products-catalog/hydraul-ez |
| CETCO SUPER GEL-X | https://www.mineralstech.com/cetco/drilling-products/drilling-products-catalog/super-gel-x |
| CETCO SUSPEND-IT | https://www.mineralstech.com/cetco/drilling-products/drilling-products-catalog/suspend-it |
| CETCO ULTRA GEL | https://www.mineralstech.com/cetco/drilling-products/drilling-products-catalog/ultra-gel |
| Bentolux Horizont PHPA | https://bentolux.ru/products/dlya-gnb/ximicheskie-reagentyi/bentolux-horizont-phpa/ |
| BAULUX/Bentolux | Ссылки на соответствующие официальные карточки сохранены на страницах товаров |
| Goodeng | https://www.goodeng.com/g-series-horizontal-directional-drills/ |
| КЗБО «Игла-20ТВМ» | https://bur116.ru/ustanovka-prokola-grunta-igla/ustanovka-prokola-grunta-igla-20tv.html |
| Normet TamSil 290 | https://www.normet.com/en/products-and-services/construction-chemicals/waterproofing-coating-and-additives/penetrative-waterproofing-sealers/tamsil-290 |

## Исправленные содержательные дефекты

- В карточке Baroid удалено ошибочное начало `Hydraul-EZ` и исправлено описание
  TUNNEL-GEL PLUS.
- Уточнены официальные назначения HYDRAUL-EZ, SUPER GEL-X и SUSPEND-IT.
- Исправлены орфография, пунктуация и неоднозначное описание Polymers Plus PAM H.
- Для смешанных карточек оборудования и инструмента исключено впечатление, что
  общая карточка является паспортом конкретной модели.

## Обновлённые карточки

### Буровые растворы и строительная химия

- `product-baroid-tunnel-gel-plus.php`
- `product-baulux-pbma.php`
- `product-baulux-pbmb.php`
- `product-baulux-pbmv.php`
- `product-bentolux-horizont-phpa.php`
- `product-bentolux-horizont-pr.php`
- `product-bentolux-pac-hv.php`
- `product-cetco-hydraul-ez.php`
- `product-cetco-insta-vis-dry.php`
- `product-cetco-rel-pac.php`
- `product-cetco-super-gel-x.php`
- `product-cetco-suspend-it.php`
- `product-cetco-ultragel.php`
- `product-normet-tamsil.php`
- `product-polymersplus-hv.php`
- `product-polymersplus-pam-h.php`
- `product-polymersplus-vis.php`

### Оборудование и локация

- `product-fdp-hdd.php`
- `product-goodeng-hdd.php`
- `product-igla-20tvm.php`
- `product-lokatori-rf.php`
- `product-nsu.php`

### Буровой инструмент

- `product-adapter.php`
- `product-burovie-golovi.php`
- `product-burovoi-nozh.php`
- `product-burovoi-pilot.php`
- `product-kluch-trubnii.php`
- `product-mufta-startovoy.php`
- `product-shtanga-burovaya.php`
- `product-shtanga-startovaya.php`
- `product-smazka-rf.php`
- `product-vkladishi-tiskov.php`
- `product-vstavki-nozha.php`
- `product-zahvat-tsangovii.php`

## Контрольные показатели

| Проверка | Результат |
|---|---:|
| Канонические товары | 68 |
| Обновлённые карточки | 34 |
| Карточки менее 180 слов | 0 |
| Минимальный объём карточки | 180 слов |
| Медиана по товарам | 203 слова |
| Индексируемые URL | 81 |
| Редиректные страницы | 2 |
| Локальные ссылки и ресурсы | 1 132 |
| Растровые изображения | 415 |
| JSON-LD блоки | 163 |
| PHP-файлы, разобранные независимым парсером | 90, ошибок 0 |
| Галереи / дополнительные изображения | 24 / 72, ошибок порядка 0 |

Финальный статический аудит завершён со статусом `passed`, без ошибок и
предупреждений. Различия между `site/` v18 и v19 ограничены ровно 34
перечисленными товарными карточками.

## Ограничения

Серверные ответы, отправка форм, HTTPS, защитные заголовки, адаптивное
отображение на реальных устройствах, Lighthouse и Core Web Vitals в этом этапе
не проверялись. Эти проверки выполняются только после публикации и получения
HTTPS URL.
