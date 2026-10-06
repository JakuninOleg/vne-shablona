(() => {
  const id = 113500820;
  const storageKey = 'vne-analytics-consent-v1';
  let consent = null;
  let started = false;
  try { consent = localStorage.getItem(storageKey); } catch {}
  const cleanUrl = () => location.origin + location.pathname;
  const start = () => {
    if (started || consent !== 'yes') return;
    started = true;
    window.ym = window.ym || function () { (window.ym.a = window.ym.a || []).push(arguments); };
    window.ym.l = Date.now();
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://mc.yandex.ru/metrika/tag.js';
    document.head.append(script);
    let referrer = '';
    try { referrer = new URL(document.referrer).origin; } catch {}
    window.ym(id, 'init', {clickmap:false, trackLinks:false, webvisor:false, accurateTrackBounce:true, url:cleanUrl(), referrer});
  };
  const goal = (name) => { if (consent === 'yes') { start(); window.ym(id,'reachGoal',name); } };
  const panel = document.createElement('section');
  panel.className = 'analytics-consent';
  panel.setAttribute('aria-label','Настройки аналитики');
  panel.innerHTML = '<p>Разрешить аналитику посещений? Это помогает улучшать сайт. <a href="/legal/#analytics">Подробнее</a></p><div><button type="button" data-consent="yes">Разрешить</button><button type="button" data-consent="no">Без аналитики</button></div>';
  panel.hidden = consent !== null;
  document.body.append(panel);
  const settings = document.createElement('button');
  settings.type = 'button'; settings.className = 'analytics-settings'; settings.textContent = 'Настройки аналитики';
  document.body.append(settings);
  settings.addEventListener('click', () => { panel.hidden = false; panel.querySelector('button').focus(); });
  panel.addEventListener('click', (event) => {
    const choice = event.target.closest('[data-consent]');
    if (!choice) return;
    const wasStarted = started;
    consent = choice.dataset.consent;
    try { localStorage.setItem(storageKey,consent); } catch {}
    panel.hidden = true;
    if (consent === 'yes') start();
    else if (wasStarted) { window.ym?.(id,'destruct'); location.reload(); }
  });
  document.addEventListener('click', (event) => {
    if (event.target.closest('a[href="#contact"],a[href="/#contact"]')) goal('contact_cta');
  });
  document.addEventListener('vne:lead-success', () => goal('lead_success'));
  if (consent === 'yes') {
    if ('requestIdleCallback' in window) requestIdleCallback(start,{timeout:2000});
    else setTimeout(start,1000);
  }
})();
