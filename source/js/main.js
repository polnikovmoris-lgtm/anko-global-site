/* ==========================================================================
   ANKO GLOBAL — main.js
   ==========================================================================

   ┌────────────────────────────────────────────────────────────────────┐
   │  Отправка заявок выполняется через защищённый серверный send.php.  │
   │  Токены и пароли не должны попадать в JavaScript браузера.          │
   └────────────────────────────────────────────────────────────────────┘
   ========================================================================== */

var LEAD_CONFIG = {
  endpoint: 'send.php',
  successPage: 'thanks.php'
};

/* ========================================================================== */

(function () {
  'use strict';

  /* ---------- Ссылка пропуска навигации ---------- */
  var skipLink = document.querySelector('.skip-link');
  var mainContent = document.getElementById('main-content');
  if (skipLink && mainContent) {
    skipLink.addEventListener('click', function () {
      mainContent.setAttribute('tabindex', '-1');
      window.setTimeout(function () { mainContent.focus(); }, 0);
    });
  }

  /* ---------- Мобильное меню ---------- */
  var burger = document.querySelector('[data-menu-toggle]');
  var menu = document.querySelector('[data-menu]');
  if (burger && menu) {
    function setMenu(open, returnFocus) {
      menu.classList.toggle('is-open', open);
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
      document.body.classList.toggle('menu-open', open);
      if (!open && returnFocus) burger.focus();
    }

    burger.addEventListener('click', function () {
      setMenu(burger.getAttribute('aria-expanded') !== 'true', false);
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false, false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        setMenu(false, true);
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000 && burger.getAttribute('aria-expanded') === 'true') {
        setMenu(false, false);
      }
    });
  }

  /* ---------- Куки-баннер ---------- */
  var cookie = document.querySelector('[data-cookie]');
  if (cookie) {
    var accepted = false;
    try { accepted = document.cookie.indexOf('anko_cookie_ok=1') !== -1; } catch (e) {}
    if (!accepted) cookie.hidden = false;
    var okBtn = cookie.querySelector('[data-cookie-ok]');
    if (okBtn) {
      okBtn.addEventListener('click', function () {
        try {
          var d = new Date();
          d.setFullYear(d.getFullYear() + 1);
          document.cookie = 'anko_cookie_ok=1; expires=' + d.toUTCString() + '; path=/; SameSite=Lax';
        } catch (e) {}
        cookie.hidden = true;
      });
    }
  }

  /* ---------- Отправка заявки ---------- */

  function collect(form) {
    var d = {};
    ['name', 'phone', 'message', 'product', 'csrf', 'company'].forEach(function (k) {
      var el = form.querySelector('[name="' + k + '"]');
      d[k] = el ? el.value.trim() : '';
    });
    var consent = form.querySelector('[name="consent"]');
    d.consent = consent && consent.checked ? '1' : '0';
    d.page = document.title;
    d.url = window.location.href;
    return d;
  }

  function send(d) {
    return fetch(LEAD_CONFIG.endpoint, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(d)
    }).then(function (r) {
      if (!r.ok) {
        return r.json().catch(function () { return {}; }).then(function (data) {
          throw new Error(data.error || ('HTTP ' + r.status));
        });
      }
      return r.json();
    });
  }

  function showSuccessInline(form) {
    form.setAttribute('aria-busy', 'false');
    form.innerHTML =
      '<div class="form__success" role="status" tabindex="-1">' +
      '<p class="form__success-title">Спасибо!</p>' +
      '<p class="form__success-text">Заявка принята. Перезвоним в рабочее время.</p>' +
      '</div>';
    form.querySelector('.form__success').focus();
  }

  function showError(form, btn, original) {
    var err = form.querySelector('[data-form-status]');
    if (!err) {
      err = document.createElement('p');
      err.className = 'form__status';
      err.setAttribute('data-form-status', '');
      err.setAttribute('aria-live', 'assertive');
      btn.parentNode.insertBefore(err, btn.nextSibling);
    }
    err.textContent = 'Не удалось отправить. Позвоните нам: +375 29 652-67-09';
    form.setAttribute('aria-busy', 'false');
    btn.disabled = false;
    btn.textContent = original;
  }

  document.querySelectorAll('[data-lead-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var btn = form.querySelector('button[type="submit"]');
      if (!btn || btn.disabled) return;
      var status = form.querySelector('[data-form-status]');
      if (status) status.textContent = '';

      // проверка галочки согласия
      var consent = form.querySelector('[data-consent]');
      if (consent && !consent.checked) {
        consent.focus();
        return;
      }

      // проверка телефона
      var phone = form.querySelector('[name="phone"]');
      if (phone && phone.value.trim().length < 7) {
        phone.focus();
        return;
      }

      var original = btn.textContent;
      form.setAttribute('aria-busy', 'true');
      btn.disabled = true;
      btn.textContent = 'Отправляем…';

      send(collect(form))
        .then(function () {
          form.setAttribute('aria-busy', 'false');
          if (window.ym && window.METRIKA_ID) { window.ym(window.METRIKA_ID, 'reachGoal', 'lead_submit'); }
          if (window.gtag) { window.gtag('event', 'generate_lead', { form_location: document.title }); }
          if (LEAD_CONFIG.successPage) {
            window.location.href = LEAD_CONFIG.successPage;
          } else {
            showSuccessInline(form);
          }
        })
        .catch(function (err) {
          console.error('ANKO: ошибка отправки заявки', err);
          showError(form, btn, original);
        });
    });
  });


  /* ---------- Галерея отзывов поверх страницы ---------- */
  var reviewLinks = Array.prototype.slice.call(document.querySelectorAll('[data-review-gallery]'));
  var reviewLightbox = document.querySelector('[data-review-lightbox]');
  if (reviewLinks.length && reviewLightbox) {
    var reviewImage = reviewLightbox.querySelector('[data-review-image]');
    var reviewCaption = reviewLightbox.querySelector('[data-review-caption]');
    var reviewCounter = reviewLightbox.querySelector('[data-review-counter]');
    var reviewPrev = reviewLightbox.querySelector('[data-review-prev]');
    var reviewNext = reviewLightbox.querySelector('[data-review-next]');
    var reviewClosers = reviewLightbox.querySelectorAll('[data-review-close]');
    var reviewIndex = 0;
    var reviewLastOpener = null;
    var reviewInerted = [];

    function setReviewBackgroundInert(active) {
      if (active) {
        reviewInerted = [];
        Array.prototype.forEach.call(document.body.children, function (child) {
          if (child === reviewLightbox || child.tagName === 'SCRIPT' || child.inert) return;
          child.inert = true;
          reviewInerted.push(child);
        });
      } else {
        reviewInerted.forEach(function (child) { child.inert = false; });
        reviewInerted = [];
      }
    }

    function reviewShow(index) {
      reviewIndex = (index + reviewLinks.length) % reviewLinks.length;
      var link = reviewLinks[reviewIndex];
      var thumb = link.querySelector('img');
      var label = link.getAttribute('aria-label') || (thumb ? thumb.alt : 'Благодарственное письмо');
      var cleanLabel = label.replace(/^Открыть\s+/i, '');
      reviewImage.src = link.getAttribute('href');
      reviewImage.alt = thumb ? thumb.alt : cleanLabel;
      reviewCaption.textContent = cleanLabel;
      reviewCounter.textContent = (reviewIndex + 1) + ' из ' + reviewLinks.length;
    }

    function reviewOpen(index, opener) {
      reviewLastOpener = opener || document.activeElement;
      reviewShow(index);
      reviewLightbox.hidden = false;
      document.body.classList.add('lightbox-open');
      setReviewBackgroundInert(true);
      window.setTimeout(function () {
        var closeButton = reviewLightbox.querySelector('.review-lightbox__close');
        if (closeButton) closeButton.focus();
      }, 0);
    }

    function reviewClose() {
      reviewLightbox.hidden = true;
      document.body.classList.remove('lightbox-open');
      setReviewBackgroundInert(false);
      reviewImage.removeAttribute('src');
      if (reviewLastOpener && typeof reviewLastOpener.focus === 'function') reviewLastOpener.focus();
    }

    reviewLinks.forEach(function (link, index) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        reviewOpen(index, link);
      });
    });
    reviewClosers.forEach(function (button) { button.addEventListener('click', reviewClose); });
    reviewPrev.addEventListener('click', function () { reviewShow(reviewIndex - 1); });
    reviewNext.addEventListener('click', function () { reviewShow(reviewIndex + 1); });

    document.addEventListener('keydown', function (event) {
      if (reviewLightbox.hidden) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        reviewClose();
        return;
      }
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        reviewShow(reviewIndex - 1);
        return;
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        reviewShow(reviewIndex + 1);
        return;
      }
      if (event.key === 'Tab') {
        var focusable = reviewLightbox.querySelectorAll('button:not([disabled]), [href], [tabindex]:not([tabindex="-1"])');
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  /* ---------- Модальное окно "Запросить КП" ---------- */
  var kpModal = document.querySelector('[data-kp-modal]');
  if (kpModal) {
    var kpOpeners = document.querySelectorAll('[data-kp-open]');
    var kpClosers = kpModal.querySelectorAll('[data-kp-close]');
    var kpProductLabel = kpModal.querySelector('[data-kp-product]');
    var kpProductField = kpModal.querySelector('[data-kp-product-field]');
    var kpLastOpener = null;
    var kpInerted = [];

    function setBackgroundInert(active) {
      if (active) {
        kpInerted = [];
        Array.prototype.forEach.call(document.body.children, function (child) {
          if (child === kpModal || child.tagName === 'SCRIPT' || child.inert) return;
          child.inert = true;
          kpInerted.push(child);
        });
      } else {
        kpInerted.forEach(function (child) { child.inert = false; });
        kpInerted = [];
      }
    }

    function kpOpen(opener) {
      kpLastOpener = opener || document.activeElement;
      // название товара берём из h1 страницы
      var h1 = document.querySelector('.pdp__title, h1');
      var name = h1 ? h1.textContent.trim() : '';
      if (name) {
        if (kpProductLabel) kpProductLabel.textContent = 'Товар: ' + name;
        if (kpProductField) kpProductField.value = name;
      }
      kpModal.hidden = false;
      document.body.classList.add('modal-open');
      setBackgroundInert(true);
      var phone = kpModal.querySelector('[name="phone"]');
      if (phone) setTimeout(function () { phone.focus(); }, 50);
    }
    function kpClose() {
      kpModal.hidden = true;
      document.body.classList.remove('modal-open');
      setBackgroundInert(false);
      if (kpLastOpener && typeof kpLastOpener.focus === 'function') kpLastOpener.focus();
    }
    kpOpeners.forEach(function (b) {
      b.addEventListener('click', function () { kpOpen(b); });
    });
    kpClosers.forEach(function (b) { b.addEventListener('click', kpClose); });
    document.addEventListener('keydown', function (e) {
      if (kpModal.hidden) return;
      if (e.key === 'Escape') {
        kpClose();
        return;
      }
      if (e.key === 'Tab') {
        var focusable = kpModal.querySelectorAll('button, [href], input:not([type="hidden"]):not([tabindex="-1"]), textarea, select');
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    });
  }

})();
