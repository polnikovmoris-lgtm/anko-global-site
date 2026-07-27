/* ==========================================================================
   ANKO GLOBAL — умный поиск по всему каталогу
   - ищет по всем актуальным позициям с любой страницы
   - исправляет неверную раскладку (,tynjybn → бентонит)
   - прощает опечатки (бентанит → бентонит)
   - понимает синонимы (бэкример → расширитель)
   ========================================================================== */
(function () {
  'use strict';

  /* Индекс каталога — встроен, чтобы работало и локально, и на сервере.
     Пересобрать после изменения каталога: см. README. */
  var INDEX_DATA = [{"t":"cat","u":"category-bentonit.php","n":"Бентониты для ГНБ","d":"Бентонит — основа бурового раствора при ГНБ. Удерживает стенки скважины от обрушения, выносит выбуренную пород","k":"бентониты для гнб ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"cat","u":"category-instrument.php","n":"Буровой инструмент для ГНБ","d":"Полный комплект бурового инструмента для ГНБ: от пилотной головки до расширителей и штанг. В наличии и под зак","k":"буровой инструмент для гнб"},{"t":"cat","u":"category-lokacia.php","n":"Локационные системы для ГНБ","d":"Локационные системы для контроля положения буровой головы: определяют глубину, уклон и направление. Американск","k":"локационные системы для гнб digitrak дигитрак зонд зонды локатор локаторы локационная система локационные системы локация передатчик приемник приёмник"},{"t":"cat","u":"category-normet.php","n":"Химия Normet для ГНБ","d":"Линейка строительной химии Normet для подземного и тоннельного строительства: инъекционные составы, гидроизоля","k":"химия normet для гнб geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"cat","u":"category-polimer.php","n":"Полимеры и реагенты для ГНБ","d":"Полимеры повышают вязкость раствора, снижают фильтрацию и защищают глинистые грунты от набухания. Применяются ","k":"полимеры и реагенты для гнб добавка добавки полимер полимеры реагент реагенты"},{"t":"cat","u":"category-smazki.php","n":"Смазочные материалы для ГНБ","d":"Смазочные материалы для резьбовых соединений буровых штанг. Снижают износ резьбы, облегчают свинчивание и разв","k":"смазочные материалы для гнб pipe dope резьбовая смазка резьбовой состав смазка смазка резьбы смазки смазочные материалы солидол"},{"t":"cat","u":"category-trubi.php","n":"ПЭ трубы для ГНБ","d":"Полиэтиленовые трубы для протяжки в скважину методом ГНБ — для водоснабжения и газоснабжения.","k":"пэ трубы для гнб пнд пнд труба полиэтиленовая труба пэ труба пэ трубы труба трубы"},{"t":"cat","u":"category-ustanovki.php","n":"Буровые установки для ГНБ","d":"Установки горизонтально направленного бурения разной мощности, а также техника для вертикального и шнекового б","k":"буровые установки для гнб буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-adapter.php","n":"Адаптеры","d":"Адаптер соединяет элементы колонны с разными типами резьбы — например, штангу одного стандарта с расширителем ","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"адаптеры буровой инструмент буровой инструмент   адаптер адаптеры переходник переходники"},{"t":"prod","u":"product-ankobent-plus.php","n":"AnkoBent Plus","d":"Высокопроизводительная смесь природно-натриевого бентонита для ГНБ и микротоннелирования.","c":"Бентониты","b":"AnkoBent","codes":"Fann-35 Fann35","k":"ankobent plus ankobent бентониты fann-35 fann35  ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-ankobent-ultra.php","n":"AnkoBent Ultra","d":"Бентонит премиум-класса, разработанный после более чем 10-летней работы с бентонитами ключевых производителей ","c":"Бентониты","b":"AnkoBent","codes":"Fann-35 Fann35","k":"ankobent ultra ankobent бентониты fann-35 fann35  ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-baroid-tunnel-gel-plus.php","n":"Baroid TUNNEL-GEL PLUS","d":"Премиальная бентонитовая система для тоннелирования и сложных буровых работ.","c":"Бентониты","b":"BAROID","codes":"","k":"baroid tunnel-gel plus baroid бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-baulux-pbma.php","n":"BAULUX ПБМА","d":"Химия для бурения водозаборных скважин.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"baulux пбма baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-baulux-pbmb.php","n":"BAULUX ПБМБ","d":"Химия для бурения водозаборных скважин.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"baulux пбмб baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-baulux-pbmv.php","n":"BAULUX ПБМВ","d":"Химия для бурения водозаборных скважин.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"baulux пбмв baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-bentolux-horizon-vis.php","n":"BENTOLUX Horizon VIS","d":"Полимер-загуститель для быстрого повышения вязкости бурового раствора.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"bentolux horizon vis baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-bentolux-horizont-phpa.php","n":"BENTOLUX Horizont PHPA","d":"PHPA-полимер для ингибирования и стабилизации активных глин.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"bentolux horizont phpa baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-bentolux-horizont-pr.php","n":"Bentolux Horizont PR","d":"Бентонитовый порошок для приготовления бурового раствора при ГНБ.","c":"Бентониты","b":"BAULUX","codes":"","k":"bentolux horizont pr baulux бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-bentolux-pac-hv.php","n":"Bentolux Horizont PAC-HV","d":"Полимерная добавка для бурового раствора.","c":"Полимеры и реагенты","b":"BAULUX","codes":"","k":"bentolux horizont pac-hv baulux полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-burovie-golovi.php","n":"Сменные буровые головы","d":"Буровая голова — сменный узел на конце колонны. Внутри неё размещается зонд локационной системы, снаружи крепя","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"сменные буровые головы буровой инструмент буровой инструмент  "},{"t":"prod","u":"product-burovoi-nozh.php","n":"Буровые ножи (лопатки)","d":"Буровой нож — сменный режущий элемент пилотной головы. Это расходный материал: изнашивается в работе и меняетс","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"буровые ножи (лопатки) буровой инструмент буровой инструмент   буровой нож лопатка лопатки ножи резец резцы"},{"t":"prod","u":"product-burovoi-pilot.php","n":"Буровые пилоты","d":"Пилотный инструмент проходит первую скважину по проектной трассе. От него зависит точность выхода в заданную т","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"буровые пилоты буровой инструмент буровой инструмент   буровая голова буровой пилот пилот пилотная головка пилоты"},{"t":"prod","u":"product-cetco-hydraul-ez.php","n":"CETCO HYDRAUL-EZ","d":"Бентонитовая система для горизонтально-направленного бурения.","c":"Бентониты","b":"CETCO","codes":"","k":"cetco hydraul-ez cetco бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-cetco-insta-vis-dry.php","n":"CETCO INSTA-VIS DRY","d":"Полимерная добавка для повышения вязкости бурового раствора.","c":"Полимеры и реагенты","b":"CETCO","codes":"","k":"cetco insta-vis dry cetco полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-cetco-rel-pac.php","n":"CETCO REL-PAC","d":"Полимерная добавка для бурового раствора.","c":"Полимеры и реагенты","b":"CETCO","codes":"","k":"cetco rel-pac cetco полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-cetco-super-gel-x.php","n":"CETCO SUPER GEL X","d":"Высококачественный натриевый бентонит для буровых растворов.","c":"Бентониты","b":"CETCO","codes":"","k":"cetco super gel x cetco бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-cetco-suspend-it.php","n":"CETCO SUSPEND-IT","d":"Полимерная добавка для повышения несущей и суспендирующей способности раствора.","c":"Полимеры и реагенты","b":"CETCO","codes":"","k":"cetco suspend-it cetco полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-cetco-ultragel.php","n":"CETCO ULTRA GEL","d":"Бентонитовый порошок производства CETCO для приготовления буровых растворов.","c":"Бентониты","b":"CETCO","codes":"","k":"cetco ultra gel cetco бентониты  ultra gel ultragel cetco ultragel cetco ultra-gel product-ultra-gel.php ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-ditchwitch-hdd.php","n":"Буровые установки Ditch Witch","d":"Установки ГНБ серии JT. Обозначения честные: число в названии соответствует усилию протяжки в тысячах фунтов —","c":"Буровые установки","b":"Ditch Witch","codes":"20 32 40 D24X40JT D24x40JT D40X55JT D40x55JT F3 JT 20 JT 32 JT 40 JT-20 JT-32 JT-40 JT20 JT32 JT40","k":"буровые установки ditch witch ditch witch буровые установки 20 32 40 d24x40jt d24x40jt d40x55jt d40x55jt f3 jt 20 jt 32 jt 40 jt-20 jt-32 jt-40 jt20 jt32 jt40  буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-fdp-hdd.php","n":"Установки ГНБ FDP","d":"Семейство установок горизонтально направленного бурения FDP для бестраншейной прокладки коммуникаций.","c":"Буровые установки","b":"DBRILL","codes":"","k":"установки гнб fdp dbrill буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-goodeng-hdd.php","n":"Буровые установки Goodeng","d":"Установки горизонтально направленного бурения Goodeng. Разумный баланс цены и возможностей — вариант для подря","c":"Буровые установки","b":"Goodeng","codes":"","k":"буровые установки goodeng goodeng буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-igla-20t.php","n":"Установка прокола грунта Игла-20Т","d":"Компактная колодезная установка статического прокола грунта с усилием 20 тонн.","c":"Буровые установки","b":"КЗБО","codes":"","k":"установка прокола грунта игла-20т кзбо буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-igla-20tvm.php","n":"Установка прокола грунта Игла-20ТВМ","d":"Котлованная установка для управляемого прокола грунта с гидровращателем.","c":"Буровые установки","b":"КЗБО","codes":"","k":"установка прокола грунта игла-20твм кзбо буровые установки  игла-20тб игла 20тб igla 20tb igla-20tb буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-igla-32t.php","n":"Установка прокола грунта Игла-32Т","d":"Котлованная установка статического прокола грунта с усилием 32 тонны.","c":"Буровые установки","b":"КЗБО","codes":"","k":"установка прокола грунта игла-32т кзбо буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-kluch-trubnii.php","n":"Ключи трубные","d":"Трубные ключи применяются для ручного свинчивания и развинчивания элементов буровой колонны и оснастки.","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"ключи трубные буровой инструмент буровой инструмент   ключ ключ трубный ключи трубный ключ"},{"t":"prod","u":"product-lokatori-digitrak.php","n":"DigiTrak Falcon F5+ и Subsite Marksman","d":"Локационная система — глаза оператора под землёй. Зонд в буровой голове передаёт на приёмник положение инструм","c":"Локационные системы","b":"DigiTrak · Subsite","codes":"F5 Falcon F5 Falcon-F5 FalconF5","k":"digitrak falcon f5+ и subsite marksman digitrak · subsite локационные системы f5 falcon f5 falcon-f5 falconf5  digitrak дигитрак зонд зонды локатор локаторы локационная система локационные системы локация передатчик приемник приёмник"},{"t":"prod","u":"product-lokatori-rf.php","n":"Локационные системы РФ","d":"Локационные системы российского производства. Решают ту же задачу — проводку буровой головы по трассе — при за","c":"Локационные системы","b":"РФ","codes":"","k":"локационные системы рф рф локационные системы   digitrak дигитрак зонд зонды локатор локаторы локационная система локационные системы локация передатчик приемник приёмник"},{"t":"prod","u":"product-mufta-startovoy.php","n":"Муфта стартовой штанги","d":"Муфта соединяет стартовую штангу с буровой колонной. Расходный элемент — изнашивается вместе с резьбой.","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"муфта стартовой штанги буровой инструмент буровой инструмент   drill pipe буровая штанга муфта муфты труба буровая штанга штанги"},{"t":"prod","u":"product-normet-geotek.php","n":"GeoTek — геотехнические решения","d":"Геотехнические инъекционные решения Normet для стабилизации грунта, консолидации пород и контроля водопритока.","c":"Химия Normet","b":"","codes":"Normet 24 Normet-24 Normet24","k":"geotek — геотехнические решения  химия normet normet 24 normet-24 normet24 geotek ac geotek hs geotek lv geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamacryl.php","n":"TamAcryl — акрилатные инъекционные составы","d":"Акрилатные инъекционные смолы Normet сверхнизкой вязкости для герметизации трещин, швов, инъекционных трубок и","c":"Химия Normet","b":"","codes":"2000 3000 4000 Normet 24 Normet-24 Normet24 TamAcryl 2000 TamAcryl 3000 TamAcryl 4000 TamAcryl-2000 TamAcryl-3000 TamAcryl-4000 TamAcryl2000 TamAcryl3000 TamAcryl4000","k":"tamacryl — акрилатные инъекционные составы  химия normet 2000 3000 4000 normet 24 normet-24 normet24 tamacryl 2000 tamacryl 3000 tamacryl 4000 tamacryl-2000 tamacryl-3000 tamacryl-4000 tamacryl2000 tamacryl3000 tamacryl4000 tamacryl 2000 tamacryl 3000 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamcem.php","n":"TamCem — добавки для бетона и растворов","d":"Добавки Normet для бетона, торкрет-бетона, микроцементных инъекционных растворов и растворов заобделочного наг","c":"Химия Normet","b":"","codes":"15 23 60 66 Normet 24 Normet-24 Normet24 TamCem 15 TamCem 23 TamCem 60 TamCem 66 TamCem-15 TamCem-23 TamCem-60 TamCem-66 TamCem15 TamCem23 TamCem60 TamCem66","k":"tamcem — добавки для бетона и растворов  химия normet 15 23 60 66 normet 24 normet-24 normet24 tamcem 15 tamcem 23 tamcem 60 tamcem 66 tamcem-15 tamcem-23 tamcem-60 tamcem-66 tamcem15 tamcem23 tamcem60 tamcem66 tamcem 8bfg tamcem 9bfg tamcem 23ssr tamcem 60 tamcem ibond tamcem hca tamcem microsilica tamcem nanosilica geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil добавка добавки нормет полимер полимеры реагент реагенты химия"},{"t":"prod","u":"product-normet-tamcrete.php","n":"TamCrete — цементные системы для инъекции и ремонта","d":"Цементные ремонтные растворы, безусадочные подливочные составы, водоостанавливающие материалы и смеси для сухо","c":"Химия Normet","b":"","codes":"40HB Normet 24 Normet-24 Normet24 TamCrete 40HB TamCrete-40HB TamCrete40HB","k":"tamcrete — цементные системы для инъекции и ремонта  химия normet 40hb normet 24 normet-24 normet24 tamcrete 40hb tamcrete-40hb tamcrete40hb tamcrete 400cs tamcrete cr tamcrete pii tamcrete pll tamcrete mfc tamcrete ufc tamcrete plug tamcrete polyplug tamcrete poly plug tamcrete sbr geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamgrease.php","n":"TamGrease — смазочные составы","d":"Смазочные и герметизирующие составы Normet для главного подшипника тоннелепроходческих комплексов.","c":"Химия Normet","b":"","codes":"EP2 Normet 24 Normet-24 Normet24","k":"tamgrease — смазочные составы  химия normet ep2 normet 24 normet-24 normet24 tamgrease bl11 tamgrease bs1 tamgrease bs11 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tampur.php","n":"TamPur — полиуретановые инъекционные смолы","d":"Инъекционные смолы Normet для консолидации пород, заполнения пустот, крепления анкеров и герметизации трещин.","c":"Химия Normet","b":"","codes":"116T 117 Normet 24 Normet-24 Normet24 TamPur 116T TamPur 117 TamPur-116T TamPur-117 TamPur116T TamPur117","k":"tampur — полиуретановые инъекционные смолы  химия normet 116t 117 normet 24 normet-24 normet24 tampur 116t tampur 117 tampur-116t tampur-117 tampur116t tampur117 tampur 100 tampur 116t tampur 125 tampur 130 tampur 150 tampur 170 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamrez.php","n":"TamRez — эпоксидные смолы","d":"Эпоксидные смолы, праймеры, ремонтные и клеевые системы Normet для бетона и металлических элементов.","c":"Химия Normet","b":"","codes":"210 220 310 Normet 24 Normet-24 Normet24 TamRez 210 TamRez 220 TamRez 310 TamRez-210 TamRez-220 TamRez-310 TamRez210 TamRez220 TamRez310","k":"tamrez — эпоксидные смолы  химия normet 210 220 310 normet 24 normet-24 normet24 tamrez 210 tamrez 220 tamrez 310 tamrez-210 tamrez-220 tamrez-310 tamrez210 tamrez220 tamrez310 tamrez 440 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamseal.php","n":"TamSeal — гидроизоляционные системы","d":"Гидроизоляционные мембраны, покрытия, герметики и уплотняющие материалы Normet для тоннелей и бетонных сооруже","c":"Химия Normet","b":"","codes":"10F 800 Normet 24 Normet-24 Normet24 TG91 TamSeal 10F TamSeal 800 TamSeal-10F TamSeal-800 TamSeal10F TamSeal800","k":"tamseal — гидроизоляционные системы  химия normet 10f 800 normet 24 normet-24 normet24 tg91 tamseal 10f tamseal 800 tamseal-10f tamseal-800 tamseal10f tamseal800 tamseal 10f tamseal 10gm tamseal 290 tamseal 20 tamseal 23 tamseal 23e tamseal 1500 tamseal 4000e tamseal 800 tamseal admix tamseal br tamseal bbr tamseal ep11 tamseal im tamseal r tamseal rc tamseal tg11 tamseal tg12 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamshot.php","n":"TamShot — ускорители для торкрет-бетона","d":"Ускорители схватывания Normet для мокрого торкретирования и специальных цементных растворов.","c":"Химия Normet","b":"","codes":"100AF 10SS 80AF Normet 24 Normet-24 Normet24 TamShot 100AF TamShot 10SS TamShot 80AF TamShot-100AF TamShot-10SS TamShot-80AF TamShot100AF TamShot10SS TamShot80AF","k":"tamshot — ускорители для торкрет-бетона  химия normet 100af 10ss 80af normet 24 normet-24 normet24 tamshot 100af tamshot 10ss tamshot 80af tamshot-100af tamshot-10ss tamshot-80af tamshot100af tamshot10ss tamshot80af tamshot 80af tamshot 110af tamshot 210af geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamsil.php","n":"TamSil — силикатные составы","d":"Силикатные и силан-силоксановые составы Normet для глубокой защиты пористых минеральных оснований.","c":"Химия Normet","b":"","codes":"290 Normet 24 Normet-24 Normet24 TamSil 290 TamSil-290 TamSil290","k":"tamsil — силикатные составы  химия normet 290 normet 24 normet-24 normet24 tamsil 290 tamsil-290 tamsil290 tamsil 1 tamsil 7 geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-normet-tamsoil.php","n":"TamSoil — кондиционирование грунта для ТПМК","d":"Пены, полимеры, антиприлипающие и противоизносные добавки Normet для кондиционирования грунта при работе ТПМК.","c":"Химия Normet","b":"","codes":"195CF 200CF 260CF 265CF 281AC 285AC 500CP 600CP 700CP 800AD Normet 24 Normet-24 Normet24 TamSoil 195CF TamSoil 281AC TamSoil 500CP TamSoil 800AD TamSoil-195CF TamSoil-281AC TamSoil-500CP TamSoil-800AD TamSoil195CF TamSoil281AC TamSoil500CP TamSoil800AD","k":"tamsoil — кондиционирование грунта для тпмк  химия normet 195cf 200cf 260cf 265cf 281ac 285ac 500cp 600cp 700cp 800ad normet 24 normet-24 normet24 tamsoil 195cf tamsoil 281ac tamsoil 500cp tamsoil 800ad tamsoil-195cf tamsoil-281ac tamsoil-500cp tamsoil-800ad tamsoil195cf tamsoil281ac tamsoil500cp tamsoil800ad tamsoil 190cf tamsoil 200cf tamsoil 260cf tamsoil 267cf tamsoil 280ac tamsoil 287ac tamsoil 600cp tamsoil 1000cp tamsoil 2000cp geotek normet tamacryl tamcem tamcrete tampur tamrez tamseal tamshot tamsoil нормет химия"},{"t":"prod","u":"product-nsu.php","n":"Насосно-смесительный узел (НСУ)","d":"Насосно-смесительный узел готовит буровой раствор и подаёт его в скважину. От качества замешивания напрямую за","c":"Буровой инструмент","b":"Оборудование","codes":"","k":"насосно-смесительный узел (нсу) оборудование буровой инструмент   миксер насосно смесительный узел насосно-смесительный узел нсу смеситель"},{"t":"prod","u":"product-pe-pipe-gaz.php","n":"ПЭ труба для газоснабжения","d":"Полиэтиленовые трубы для газоснабжения, пригодные для протяжки методом ГНБ. К газовым трубам предъявляются пов","c":"ПЭ трубы","b":"ПЭ трубы","codes":"SDR","k":"пэ труба для газоснабжения пэ трубы пэ трубы sdr  пнд пнд труба полиэтиленовая труба пэ труба пэ трубы труба трубы"},{"t":"prod","u":"product-pe-pipe-voda.php","n":"ПЭ труба для водоснабжения","d":"Полиэтиленовые трубы для водоснабжения, пригодные для протяжки в скважину методом ГНБ. Полиэтилен хорошо перен","c":"ПЭ трубы","b":"ПЭ трубы","codes":"SDR","k":"пэ труба для водоснабжения пэ трубы пэ трубы sdr  пнд пнд труба полиэтиленовая труба пэ труба пэ трубы труба трубы"},{"t":"prod","u":"product-phrikolat-pac.php","n":"PHRIKOLAT PAC (L / LV / ULV)","d":"Полианионная целлюлоза для снижения фильтрационных потерь бурового раствора. Выпускается в модификациях разной","c":"Полимеры и реагенты","b":"PHRIKOLAT","codes":"Bag 1000 Bag-1000 Bag1000 PAC","k":"phrikolat pac (l / lv / ulv) phrikolat полимеры и реагенты bag 1000 bag-1000 bag1000 pac  добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-phrikolat-rheopur.php","n":"PHRIKOLAT Rheopur","d":"Полимерная смесь, разработанная специально для ГНБ. Объединяет свойства нескольких полимерных добавок, за счёт","c":"Полимеры и реагенты","b":"PHRIKOLAT","codes":"","k":"phrikolat rheopur phrikolat полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-phrikolat-typ-w-premium.php","n":"PHRIKOLAT Bentonit Typ W Premium","d":"Бентонит, разработанный специально для крупной буровой техники ГНБ. Обладает выраженно сдвигоразжижающей реоло","c":"Бентониты","b":"PHRIKOLAT","codes":"PAC","k":"phrikolat bentonit typ w premium phrikolat бентониты pac  ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-phrikolat-type-w.php","n":"PHRIKOLAT Bentonit Typ W","d":"Высокоэффективная основа бурового раствора на природном натриевом бентоните вайомингского типа. Мелкий помол и","c":"Бентониты","b":"PHRIKOLAT","codes":"","k":"phrikolat bentonit typ w phrikolat бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-phrikolat-w-plus.php","n":"PHRIKOLAT Bentonit W plus","d":"Готовая универсальная смесь для ГНБ: мелкозернистый натриевый бентонит вайомингского типа с высоким содержание","c":"Бентониты","b":"PHRIKOLAT","codes":"","k":"phrikolat bentonit w plus phrikolat бентониты   ankobent анкобент бентонит бентонитовый порошок бентониты буровой раствор глина глинопорошок"},{"t":"prod","u":"product-polymersplus-hv.php","n":"Polymers Plus HV","d":"Высоковязкий полимер для регулирования свойств бурового раствора.","c":"Полимеры и реагенты","b":"PolymersPlus","codes":"","k":"polymers plus hv polymersplus полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-polymersplus-pam-h.php","n":"Polymers Plus PAM H","d":"Инкапсулирующий PHPA-полимер для стабилизации глинистых пород.","c":"Полимеры и реагенты","b":"PolymersPlus","codes":"","k":"polymers plus pam h polymersplus полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-polymersplus-vis.php","n":"PolymersPlus VIS","d":"Полимерная добавка для повышения вязкости раствора.","c":"Полимеры и реагенты","b":"PolymersPlus","codes":"","k":"polymersplus vis polymersplus полимеры и реагенты   добавка добавки полимер полимеры реагент реагенты"},{"t":"prod","u":"product-rasshiritel.php","n":"Расширители (бэкримеры)","d":"Расширитель увеличивает диаметр пилотной скважины до размера, необходимого для протяжки трубопровода. Он не пр","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"расширители (бэкримеры) буровой инструмент буровой инструмент   backreamer бекример бэкример расширители расширитель ример"},{"t":"prod","u":"product-shtanga-burovaya.php","n":"Штанги буровые","d":"Буровые штанги американского производства: Vermeer, Ditch Witch, Hunting, Primier Drill Pipe, а также китайско","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"штанги буровые буровой инструмент буровой инструмент   drill pipe буровая штанга труба буровая штанга штанги"},{"t":"prod","u":"product-shtanga-startovaya.php","n":"Штанги стартовые","d":"Стартовая штанга — первая в буровой колонне. На неё приходятся максимальные нагрузки при забуривании, поэтому ","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"штанги стартовые буровой инструмент буровой инструмент   drill pipe буровая штанга труба буровая штанга штанги"},{"t":"prod","u":"product-smazka-ditchwitch.php","n":"Резьбовой состав для установок Ditch Witch","d":"Состав для смазывания резьбовых соединений буровых штанг. Точный производитель, артикул и допуски выбираются п","c":"Смазочные материалы","b":"Совместимо с Ditch Witch","codes":"","k":"резьбовой состав для установок ditch witch совместимо с ditch witch смазочные материалы   pipe dope резьбовая смазка резьбовой состав смазка смазка резьбы смазки смазочные материалы солидол"},{"t":"prod","u":"product-smazka-jet-lube.php","n":"Jet-Lube HDD Environmental","d":"Неметаллический и непроводящий состав для резьбовых соединений, буровых штанг и tool joints установок ГНБ.","c":"Смазочные материалы","b":"Jet-Lube","codes":"","k":"jet-lube hdd environmental jet-lube смазочные материалы   pipe dope резьбовая смазка резьбовой состав смазка смазка резьбы смазки смазочные материалы солидол"},{"t":"prod","u":"product-smazka-rf.php","n":"Резьбовая смазка для буровых штанг — РФ","d":"Категория российских резьбовых составов для обслуживания буровой колонны. Конкретный производитель и техническ","c":"Смазочные материалы","b":"Производство РФ — поставщик уточняется","codes":"","k":"резьбовая смазка для буровых штанг — рф производство рф — поставщик уточняется смазочные материалы   pipe dope резьбовая смазка резьбовой состав смазка смазка резьбы смазки смазочные материалы солидол"},{"t":"prod","u":"product-smazka-vermeer.php","n":"Vermeer Bio-Stick — смазка для ГНБ","d":"Фирменная линейка Vermeer Bio-Stick для обслуживания инструмента и резьбовых соединений при горизонтально напр","c":"Смазочные материалы","b":"Vermeer","codes":"","k":"vermeer bio-stick — смазка для гнб vermeer смазочные материалы   pipe dope резьбовая смазка резьбовой состав смазка смазка резьбы смазки смазочные материалы солидол"},{"t":"prod","u":"product-universal-hdd.php","n":"Установки ГНБ Universal HDD","d":"Линейка установок горизонтально направленного бурения Universal HDD для бестраншейной прокладки коммуникаций.","c":"Буровые установки","b":"Universal HDD","codes":"","k":"установки гнб universal hdd universal hdd буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-vermeer-hdd.php","n":"Буровые установки Vermeer","d":"Установки ГНБ серии Navigator. Важный момент: обозначения Vermeer вводят в заблуждение — цифры в названии не с","c":"Буровые установки","b":"Vermeer","codes":"28 40 D23X30 D23x30 D24X40 D24x40 D40X55 D40x55 D60X90 D60x90 JT 28 JT 40 JT-28 JT-40 JT28 JT40 S3 gpmD24x40 gpmD60x90","k":"буровые установки vermeer vermeer буровые установки 28 40 d23x30 d23x30 d24x40 d24x40 d40x55 d40x55 d60x90 d60x90 jt 28 jt 40 jt-28 jt-40 jt28 jt40 s3 gpmd24x40 gpmd60x90  буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-vertlugi.php","n":"Вертлюги","d":"Вертлюг изолирует протягиваемый трубопровод от вращения буровой колонны. Без него крутящий момент передавался ","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"вертлюги буровой инструмент буровой инструмент   swivel вертлюг вертлюги вертлюжок"},{"t":"prod","u":"product-vkladishi-tiskov.php","n":"Вкладыши (губки) тисков","d":"Вкладыши тисков удерживают штангу при свинчивании и развинчивании колонны. Изнашиваются в работе и подлежат ре","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"вкладыши (губки) тисков буровой инструмент буровой инструмент   вкладыши вкладыши тисков губки губки тисков"},{"t":"prod","u":"product-vstavki-nozha.php","n":"Твердосплавные вставки ножа","d":"Твердосплавные вставки усиливают режущую кромку бурового ножа. Резко продлевают срок службы инструмента в абра","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"твердосплавные вставки ножа буровой инструмент буровой инструмент  "},{"t":"prod","u":"product-wamet-add.php","n":"Установки шнекового бурения WAMET","d":"Семейство установок WAMET для горизонтального шнекового бурения из стартового котлована.","c":"Буровые установки","b":"WAMET","codes":"","k":"установки шнекового бурения wamet wamet буровые установки   буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-xcmg-hdd.php","n":"Буровые установки XCMG","d":"Установки ГНБ серии XZ. В обозначении модели зашито усилие протяжки в килоньютонах: XZ180 — 180 кН, XZ320 — 32","c":"Буровые установки","b":"XCMG","codes":"1000 120E 1350 1600 160A 180 1801 200 2200 260 280 3000 320 320D 320E 360F 400 420E 450 500 5000 6600 680 900 XZ 1000 XZ 120E XZ 1350 XZ 1600 XZ 160A XZ 180 XZ 1801 XZ 200 XZ 2200 XZ 260 XZ 280 XZ 3000 XZ 320 XZ 320D XZ 320E XZ 360F XZ 400 XZ 420E XZ 450 XZ 500 XZ 5000 XZ 6600 XZ 680 XZ 900 XZ-1000 XZ-120E XZ-1350 XZ-1600 XZ-160A XZ-180 XZ-1801 XZ-200 XZ-2200 XZ-260 XZ-280 XZ-3000 XZ-320 XZ-320D XZ-320E XZ-360F XZ-400 XZ-420E XZ-450 XZ-500 XZ-5000 XZ-6600 XZ-680 XZ-900 XZ1000 XZ120E XZ1350 XZ1600 XZ160A XZ180 XZ1801 XZ200 XZ2200 XZ260 XZ280 XZ3000 XZ320 XZ320D XZ320E XZ360F XZ400 XZ420E XZ450 XZ500 XZ5000 XZ6600 XZ680 XZ900","k":"буровые установки xcmg xcmg буровые установки 1000 120e 1350 1600 160a 180 1801 200 2200 260 280 3000 320 320d 320e 360f 400 420e 450 500 5000 6600 680 900 xz 1000 xz 120e xz 1350 xz 1600 xz 160a xz 180 xz 1801 xz 200 xz 2200 xz 260 xz 280 xz 3000 xz 320 xz 320d xz 320e xz 360f xz 400 xz 420e xz 450 xz 500 xz 5000 xz 6600 xz 680 xz 900 xz-1000 xz-120e xz-1350 xz-1600 xz-160a xz-180 xz-1801 xz-200 xz-2200 xz-260 xz-280 xz-3000 xz-320 xz-320d xz-320e xz-360f xz-400 xz-420e xz-450 xz-500 xz-5000 xz-6600 xz-680 xz-900 xz1000 xz120e xz1350 xz1600 xz160a xz180 xz1801 xz200 xz2200 xz260 xz280 xz3000 xz320 xz320d xz320e xz360f xz400 xz420e xz450 xz500 xz5000 xz6600 xz680 xz900  буровая буровая установка буровые установки гнб установка машина станок установка установки"},{"t":"prod","u":"product-zahvat-tsangovii.php","n":"Захваты цанговые для ПЭ труб","d":"Цанговый захват фиксирует полиэтиленовую трубу при обратной протяжке. Распределяет тяговое усилие по стенке тр","c":"Буровой инструмент","b":"Буровой инструмент","codes":"","k":"захваты цанговые для пэ труб буровой инструмент буровой инструмент   захват захваты цанга цанговый захват"},{"t":"prod","u":"product-zondi.php","n":"Зонды (передатчики)","d":"Зонд — передатчик, который ставится в буровую голову и шлёт данные на приёмник. Работает в тяжёлых условиях: у","c":"Локационные системы","b":"Зонды","codes":"","k":"зонды (передатчики) зонды локационные системы   digitrak дигитрак зонд зонды локатор локаторы локационная система локационные системы локация передатчик приемник приёмник"}];

  var input = document.querySelector('[data-search]');
  if (!input) return;

  input.setAttribute('role', 'combobox');
  input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-expanded', 'false');
  input.setAttribute('aria-controls', 'search-suggestions');

  var INDEX = INDEX_DATA;
  var box = null;
  var active = -1;

  /* ---------- Раскладка: латиница → кириллица ---------- */
  var LAYOUT = {
    q:'й',w:'ц',e:'у',r:'к',t:'е',y:'н',u:'г',i:'ш',o:'щ',p:'з','[':'х',']':'ъ',
    a:'ф',s:'ы',d:'в',f:'а',g:'п',h:'р',j:'о',k:'л',l:'д',';':'ж',"'":'э',
    z:'я',x:'ч',c:'с',v:'м',b:'и',n:'т',m:'ь',',':'б','.':'ю','/':'.'
  };

  function fixLayout(s) {
    var out = '', ch;
    for (var i = 0; i < s.length; i++) {
      ch = s[i].toLowerCase();
      out += LAYOUT[ch] || s[i];
    }
    return out;
  }

  /* ---------- Нормализация: убираем окончания, ё→е ---------- */
  function norm(s) {
    return s.toLowerCase()
      .replace(/ё/g, 'е')
      .replace(/[^a-zа-я0-9\s×x-]/g, ' ')   // оставляем дефис и x (для D24x40)
      .replace(/×/g, 'x')
      .replace(/\s+/g, ' ')
      .trim();
  }

  /* Код артикула? (есть цифра + буква, или вида D24x40) */
  function isCode(w) {
    return /\d/.test(w) && /[a-zа-я]/.test(w) || /\d+x\d+/.test(w);
  }

  /* Убираем дефисы/пробелы для сравнения кодов: pac-hv → pachv */
  function bare(s) {
    return s.replace(/[\s-]/g, '');
  }

  /* Отсекаем русские окончания — «штанги» и «штангу» ищут «штанг» */
  function stem(w) {
    if (w.length <= 4) return w;
    return w.replace(/(ами|ями|ов|ев|ей|ий|ая|ое|ые|ых|ым|ом|ах|ях|у|ю|а|я|ы|и|е|о)$/,'');
  }

  /* ---------- Расстояние Левенштейна (опечатки) ---------- */
  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 99;
    var m = [], i, j;
    for (i = 0; i <= b.length; i++) m[i] = [i];
    for (j = 0; j <= a.length; j++) m[0][j] = j;
    for (i = 1; i <= b.length; i++) {
      for (j = 1; j <= a.length; j++) {
        m[i][j] = b[i-1] === a[j-1]
          ? m[i-1][j-1]
          : Math.min(m[i-1][j-1] + 1, m[i][j-1] + 1, m[i-1][j] + 1);
      }
    }
    return m[b.length][a.length];
  }

  /* ---------- Оценка совпадения ---------- */
  function score(item, words) {
    var key = norm(item.k);
    var name = norm(item.n);
    var keyBare = bare(key);
    var total = 0;

    for (var i = 0; i < words.length; i++) {
      var w = words[i], best = 0;

      /* 0. Код артикула — сравниваем без дефисов и пробелов, точно */
      if (isCode(w)) {
        var wb = bare(w);
        if (wb.length >= 2 && keyBare.indexOf(wb) !== -1) {
          best = 200;                        // код совпал — максимальный приоритет
          if (bare(name).indexOf(wb) !== -1) best = 260;
        }
        if (!best) return 0;                 // код набран, но не найден — пропускаем
        total += best;
        continue;
      }

      /* 1. Точное вхождение — самый сильный сигнал */
      if (key.indexOf(w) !== -1) {
        best = 100;
        /* слово стоит в начале названия — ещё лучше */
        if (name.indexOf(w) === 0) best = 160;
        else if (name.indexOf(w) !== -1) best = 130;
      } else {
        /* 2. Совпадение по корню (штанги → штанг) */
        var st = stem(w);
        if (st.length >= 4 && key.indexOf(st) !== -1) {
          best = name.indexOf(st) !== -1 ? 80 : 60;
        } else {
          /* 3. Опечатка — только как последнее средство, вес низкий */
          var parts = key.split(' ');
          for (var j = 0; j < parts.length; j++) {
            if (parts[j].length < 4) continue;
            var d = lev(w, parts[j]);
            if (d === 1 && w.length >= 4) best = Math.max(best, 35);
            else if (d === 2 && w.length >= 7) best = Math.max(best, 18);
          }
        }
      }
      if (!best) return 0;
      total += best;
    }

    if (item.t === 'cat') total += 15;
    return total;
  }

  /* ---------- Поиск ---------- */
  function find(q) {
    var raw = norm(q);
    if (raw.length < 2) return [];

    var variants = [raw];
    var fixed = norm(fixLayout(q));
    if (fixed !== raw) variants.push(fixed);   // пробуем другую раскладку

    var best = [];
    for (var v = 0; v < variants.length; v++) {
      var words = variants[v].split(' ').filter(function (w) { return w.length > 1; });
      if (!words.length) continue;

      var res = [];
      for (var i = 0; i < INDEX.length; i++) {
        var s = score(INDEX[i], words);
        if (s > 0) res.push({ item: INDEX[i], s: s });
      }
      if (res.length > best.length) best = res;
    }

    best.sort(function (a, b) { return b.s - a.s; });
    return best.slice(0, 8);
  }

  /* ---------- Выпадающий список ---------- */
  function ensureBox() {
    if (box) return box;
    box = document.createElement('div');
    box.className = 'search-drop';
    box.id = 'search-suggestions';
    box.setAttribute('role', 'listbox');
    box.setAttribute('aria-label', 'Результаты поиска');
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(box);
    return box;
  }

  function render(items, q) {
    var b = ensureBox();
    active = -1;

    if (!items.length) {
      b.innerHTML =
        '<div class="search-drop__empty">' +
        '<p class="search-drop__empty-title">Ничего не нашли по запросу «' + esc(q) + '»</p>' +
        '<p class="search-drop__empty-text">Позвоните — подберём по описанию: ' +
        '<a href="tel:+375296526709">+375 29 652-67-09</a></p></div>';
      b.classList.add('is-open');
      input.setAttribute('aria-expanded', 'true');
      input.removeAttribute('aria-activedescendant');
      return;
    }

    var html = '';
    items.forEach(function (r, i) {
      var it = r.item;
      var tag = it.t === 'cat' ? 'Раздел' : (it.c || 'Товар');
      html +=
        '<a class="search-drop__item" id="search-option-' + i + '" href="' + it.u + '" role="option" aria-selected="false" data-i="' + i + '">' +
        '<span class="search-drop__tag">' + esc(tag) + '</span>' +
        '<span class="search-drop__name">' + esc(it.n) + '</span>' +
        (it.d ? '<span class="search-drop__desc">' + esc(it.d) + '</span>' : '') +
        '</a>';
    });
    b.innerHTML = html;
    b.classList.add('is-open');
    input.setAttribute('aria-expanded', 'true');
    input.removeAttribute('aria-activedescendant');
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c];
    });
  }

  function close() {
    if (box) {
      box.classList.remove('is-open');
      box.querySelectorAll('[role="option"]').forEach(function (el) { el.setAttribute('aria-selected', 'false'); });
    }
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    active = -1;
  }

  /* ---------- Фильтрация карточек на странице (как было) ---------- */
  var cards = document.querySelectorAll('[data-search-name]');
  function filterCards(q) {
    var n = norm(q);
    cards.forEach(function (c) {
      var name = norm(c.getAttribute('data-search-name') || '');
      c.hidden = n !== '' && name.indexOf(n) === -1 && name.indexOf(norm(fixLayout(q))) === -1;
    });
  }

  /* ---------- События ---------- */
  var timer;
  input.addEventListener('input', function () {
    var q = this.value;
    filterCards(q);

    clearTimeout(timer);
    if (q.trim().length < 2) { close(); return; }

    timer = setTimeout(function () {
      render(find(q), q);
    }, 120);
  });

  input.addEventListener('keydown', function (e) {
    if (!box || !box.classList.contains('is-open')) return;
    var items = box.querySelectorAll('.search-drop__item');
    if (!items.length) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      active = (active + 1) % items.length;
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      active = active <= 0 ? items.length - 1 : active - 1;
    } else if (e.key === 'Enter' && active >= 0) {
      e.preventDefault();
      window.location.href = items[active].getAttribute('href');
      return;
    } else if (e.key === 'Escape') {
      close();
      return;
    } else return;

    items.forEach(function (el, i) {
      var selected = i === active;
      el.classList.toggle('is-active', selected);
      el.setAttribute('aria-selected', selected ? 'true' : 'false');
    });
    input.setAttribute('aria-activedescendant', items[active].id);
    items[active].scrollIntoView({ block: 'nearest' });
  });

  document.addEventListener('click', function (e) {
    if (box && !input.contains(e.target) && !box.contains(e.target)) close();
  });

  input.addEventListener('focus', function () {
    if (this.value.trim().length >= 2 && box && box.innerHTML) {
      box.classList.add('is-open');
      input.setAttribute('aria-expanded', 'true');
    }
  });
})();
