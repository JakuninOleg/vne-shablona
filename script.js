const menuButton = document.querySelector('.menu-toggle');
const siteNav = document.querySelector('.site-nav');
const siteHeader = document.querySelector('.site-header');

function closeMenu() {
  if (!menuButton || !siteNav) return;
  siteNav.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Открыть меню');
}

menuButton?.addEventListener('click', () => {
  const isOpen = siteNav.classList.toggle('is-open');
  siteHeader?.classList.remove('is-scroll-hidden');
  menuButton.setAttribute('aria-expanded', String(isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Закрыть меню' : 'Открыть меню');
});

let lastScrollY = window.scrollY;
let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (scrollTicking) return;
  scrollTicking = true;
  window.requestAnimationFrame(() => {
    const scrollY = window.scrollY;
    siteHeader?.classList.toggle('is-scrolled', scrollY > 70);
    if (window.innerWidth <= 1100 && siteHeader) {
      const goingDown = scrollY > lastScrollY + 5;
      const goingUp = scrollY < lastScrollY - 5;
      if (scrollY < 80 || goingUp || siteNav?.classList.contains('is-open')) {
        siteHeader.classList.remove('is-scroll-hidden');
      } else if (goingDown) {
        siteHeader.classList.add('is-scroll-hidden');
      }
      if (goingDown || goingUp || scrollY < 80) lastScrollY = scrollY;
    } else {
      lastScrollY = scrollY;
    }
    scrollTicking = false;
  });
}, { passive: true });

window.addEventListener('resize', () => {
  if (window.innerWidth > 1100) siteHeader?.classList.remove('is-scroll-hidden');
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});

document.addEventListener('click', (event) => {
  if (!event.target.closest('.site-header')) closeMenu();
});

window.matchMedia('(min-width: 1101px)').addEventListener('change', (event) => {
  if (event.matches) closeMenu();
});

siteNav?.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', closeMenu);
});

// Bend each complete line into the hand-lettered arches of the mockup.
document.querySelectorAll('[data-arc]').forEach((line) => {
  const isMobileLine = Boolean(line.closest('.hero-title__variant--mobile'));
  const arcDepth = isMobileLine ? 0.32 : 0.48;
  const arcTilt = isMobileLine ? 3.2 : 4.5;
  const characters = Array.from(line.textContent);
  line.textContent = '';
  characters.forEach((character, index) => {
    const point = characters.length === 1 ? 0 : (index / (characters.length - 1)) * 2 - 1;
    const span = document.createElement('span');
    span.className = 'arc-char';
    span.textContent = character === ' ' ? '\u00a0' : character;
    span.style.setProperty('--arc-y', `${((point * point - 0.27) * arcDepth).toFixed(3)}em`);
    span.style.setProperty('--arc-r', `${(point * arcTilt).toFixed(2)}deg`);
    line.append(span);
  });
});

const leadForm = document.querySelector('#lead-form');
if (leadForm) {
  const submitButton = leadForm.querySelector('button[type="submit"]');
  const submitLabel = submitButton.querySelector('.contact__submit-label');
  const status = leadForm.querySelector('.contact__form-status');
  let isSubmitting = false;

  leadForm.addEventListener('input', (event) => {
    if (event.target.matches('[required]')) event.target.setCustomValidity('');
    if (status.dataset.state === 'error' || status.dataset.state === 'success') {
      status.textContent = '';
      delete status.dataset.state;
    }
  });

  leadForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (isSubmitting) return;

    const fields = {};
    for (const [name, value] of new FormData(leadForm)) {
      if (typeof value === 'string' && value.trim()) fields[name] = value.trim();
    }

    for (const field of leadForm.querySelectorAll('input[required]:not([type="checkbox"]), textarea[required]')) {
      if (!field.value.trim()) {
        field.setCustomValidity('Заполните это поле.');
        field.reportValidity();
        return;
      }
    }

    fields['Согласие на обработку персональных данных'] = `Да; редакция 27.09.2026; отправлено ${new Date().toISOString()}`;

    isSubmitting = true;
    submitButton.disabled = true;
    submitLabel.textContent = 'Отправляем…';
    status.textContent = 'Отправляем заявку…';
    status.dataset.state = 'pending';
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch('https://jakuninoleg.dev/api/landing-lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fields),
        signal: controller.signal,
      });
      const result = await response.json().catch(() => null);

      if (!response.ok || !result?.ok) {
        if (response.status === 429) throw new Error('Слишком много заявок. Подождите минуту и попробуйте ещё раз.');
        if ([400, 413, 415].includes(response.status)) throw new Error('Проверьте заполнение полей и попробуйте ещё раз.');
        throw new Error('Заявку не удалось отправить. Попробуйте ещё раз чуть позже.');
      }

      leadForm.reset();
      status.textContent = 'Заявка отправлена! Мы свяжемся с вами по указанному контакту.';
      status.dataset.state = 'success';
    } catch (error) {
      status.textContent = error.name === 'AbortError'
        ? 'Сервер долго не отвечает. Попробуйте отправить заявку ещё раз.'
        : error.name === 'TypeError'
          ? 'Не удалось связаться с сервером. Попробуйте ещё раз позже.'
          : error.message || 'Заявку не удалось отправить. Попробуйте ещё раз позже.';
      status.dataset.state = 'error';
    } finally {
      window.clearTimeout(timeout);
      isSubmitting = false;
      submitButton.disabled = false;
      submitLabel.textContent = 'Отправить заявку';
    }
  });
}

const sketchTablet = document.querySelector('.sketch-tablet');
if (sketchTablet) {
  if ('IntersectionObserver' in window) {
    const sketchObserver = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      sketchTablet.classList.add('is-drawing');
      sketchObserver.disconnect();
    }, { threshold: 0.35 });
    sketchObserver.observe(sketchTablet);
  } else {
    sketchTablet.classList.add('is-drawing');
  }
}
