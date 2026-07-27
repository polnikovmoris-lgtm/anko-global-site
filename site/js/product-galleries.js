(function () {
  'use strict';

  var galleries = {
    'product-adapter.php': ['adapter/adapter-1.webp', 'adapter/adapter-2.webp', 'adapter/adapter-3.webp'],
    'product-burovoi-nozh.php': ['lopatki/noj1.webp', 'lopatki/noj2.webp', 'lopatki/noj3.webp'],
    'product-burovoi-pilot.php': ['piloti/pilot-0.webp', 'piloti/pilot-1.webp', 'piloti/pilot-2.webp'],
    'product-kluch-trubnii.php': ['kluch/kluch-0.webp', 'kluch/kluch-1.webp', 'kluch/kluch-2.webp'],
    'product-mufta-startovoy.php': ['mufta/mufta-0.webp', 'mufta/mufta-1.webp', 'mufta/mufta-2.webp'],
    'product-nsu.php': ['nsu/nsu-0.webp', 'nsu/nsu-2.webp', 'nsu/nsu-3.webp'],
    'product-rasshiritel.php': ['rasshiritel/rasshiritel-0.webp', 'rasshiritel/rasshiritel-1.webp', 'rasshiritel/rasshiritel-2.webp'],
    'product-shtanga-burovaya.php': ['shangi/shtanga-1.webp', 'shangi/shtanga-2.webp', 'shangi/shtanga-3.webp'],
    'product-shtanga-startovaya.php': ['shtanga-startovaya/shtangav-0.webp', 'shtanga-startovaya/shtangav-1.webp', 'shtanga-startovaya/shtangav-2.webp'],
    'product-burovie-golovi.php': ['smenniegolovi/golova-0.webp', 'smenniegolovi/golova-1.webp', 'smenniegolovi/golova-2.webp'],
    'product-vertlugi.php': ['vertlugi/vertluga-0.webp', 'vertlugi/vertluga-1.webp', 'vertlugi/vertluga-3.webp'],
    'product-vkladishi-tiskov.php': ['vkladish/vkladish-0.webp', 'vkladish/vkladish-1.webp', 'vkladish/vkladish-2.webp'],
    'product-vstavki-nozha.php': ['rezci/rezec-0.webp', 'rezci/rezec-1.webp', 'rezci/rezec-2.webp'],
    'product-zahvat-tsangovii.php': ['zahvati/zahvat-0.webp', 'zahvati/zahvat-1.webp', 'zahvati/zahvat-2.webp'],
    'product-lokatori-digitrak.php': ['locator/AmLocator.webp', 'locator/am2.webp', 'locator/am3.webp'],
    'product-lokatori-rf.php': ['locator/era2.webp', 'locator/era5.webp', 'locator/era3.webp'],
    'product-ditchwitch-hdd.php': ['ditchwitch/ditchWitch-0.webp', 'ditchwitch/ditchWitch-1.webp', 'ditchwitch/ditchWitch-2.webp'],
    'product-fdp-hdd.php': ['fdp/fpd1.webp', 'fdp/fdp2.webp', 'fdp/fdp3.webp'],
    'product-goodeng-hdd.php': ['goodeng/photo_2020-05-17_12-48-48.webp', 'goodeng/photo_2020-05-17_12-48-42.webp', 'goodeng/photo_2020-05-17_12-48-27.webp'],
    'product-igla-20t.php': ['bur-igla/igla-1.webp', 'bur-igla/igla-0.webp', 'bur-igla/igla-2.webp'],
    'product-igla-20tvm.php': ['bur-igla/igla-1.webp', 'bur-igla/igla-0.webp', 'bur-igla/igla-2.webp'],
    'product-igla-32t.php': ['bur-igla/igla-1.webp', 'bur-igla/igla-0.webp', 'bur-igla/igla-2.webp'],
    'product-vermeer-hdd.php': ['vermeer/vermeer-0.webp', 'vermeer/vermeer-1.webp', 'vermeer/vermeer-2.webp'],
    'product-xcmg-hdd.php': ['xcmg/xcmg-0.webp', 'xcmg/XCMG-Xz1500-150t-Horizontal-Directional-Drilling-Drill.webp', 'xcmg/xcmg-1.webp']
  };

  var page = window.location.pathname.split('/').pop() || '';
  var images = galleries[page];
  var gallery = document.querySelector('.gallery');
  var mainImg = document.querySelector('[data-gallery-main]');
  if (!images || !gallery || !mainImg) return;

  var mainSource = mainImg.getAttribute('src');
  var mainAlt = mainImg.getAttribute('alt') || 'Изображение товара';
  var allImages = [mainSource].concat(images.map(function (path) {
    return 'img/gallery/a-line/' + path;
  }));
  var thumbs = document.createElement('div');
  thumbs.className = 'gallery__thumbs';
  thumbs.setAttribute('role', 'group');
  thumbs.setAttribute('aria-label', 'Фотографии товара');
  mainImg.id = mainImg.id || 'product-gallery-image';

  function selectImage(button, src, focusThumb) {
    var picture = mainImg.closest('picture');
    if (picture) {
      picture.querySelectorAll('source').forEach(function (source) {
        source.remove();
      });
    }
    mainImg.src = src;
    mainImg.srcset = '';
    mainImg.alt = button.getAttribute('data-gallery-alt') || mainAlt;
    thumbs.querySelectorAll('[data-gallery-thumb]').forEach(function (thumb) {
      thumb.classList.remove('is-active');
      thumb.setAttribute('aria-pressed', 'false');
    });
    button.classList.add('is-active');
    button.setAttribute('aria-pressed', 'true');
    if (focusThumb) button.focus();
  }

  allImages.forEach(function (src, index) {
    var button = document.createElement('button');
    button.className = 'gallery__thumb' + (index === 0 ? ' is-active' : '');
    button.type = 'button';
    button.setAttribute('aria-controls', mainImg.id);
    button.setAttribute('data-gallery-thumb', '');
    button.setAttribute('aria-label', 'Показать фотографию ' + (index + 1));
    button.setAttribute('aria-pressed', index === 0 ? 'true' : 'false');
    button.setAttribute('data-gallery-alt', mainAlt + ' — фото ' + (index + 1));

    var image = document.createElement('img');
    image.src = src;
    image.setAttribute('data-full', src);
    image.alt = '';
    image.loading = index === 0 ? 'eager' : 'lazy';
    image.decoding = 'async';
    button.appendChild(image);

    button.addEventListener('click', function () {
      selectImage(button, src, false);
    });

    thumbs.appendChild(button);
  });

  thumbs.addEventListener('keydown', function (event) {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    var buttons = Array.prototype.slice.call(thumbs.querySelectorAll('[data-gallery-thumb]'));
    var current = buttons.indexOf(document.activeElement);
    if (current < 0) current = buttons.findIndex(function (button) {
      return button.classList.contains('is-active');
    });
    var next = current;
    if (event.key === 'ArrowRight') next = (current + 1) % buttons.length;
    if (event.key === 'ArrowLeft') next = (current - 1 + buttons.length) % buttons.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = buttons.length - 1;
    event.preventDefault();
    selectImage(buttons[next], allImages[next], true);
    buttons[next].scrollIntoView({ block: 'nearest', inline: 'nearest' });
  });

  gallery.appendChild(thumbs);
}());
