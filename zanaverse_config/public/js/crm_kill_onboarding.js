/**
 * Zanaverse: remove Frappe CRM SPA onboarding banner/checklist.
 * Loads via app_include_js so it runs on /app/crm.
 */
(function () {
  const SELECTORS = [
    '[data-testid*="onboard" i]',
    '[class*="onboard" i]',
    '[id*="onboard" i]',
    '.crm-onboarding',
    '.crm-getting-started'
  ];

  function getRouteStr() {
    try {
      const r = (window.frappe?.get_route?.() || []).join('/');
      return (r || '').toLowerCase();
    } catch { return ''; }
  }
  function isCRMRoute() {
    return getRouteStr().startsWith('crm');
  }
  function nukeNow() {
    if (!isCRMRoute()) return;
    SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => el.remove());
    });
    // fallback: remove visible blocks that look like onboarding
    document.querySelectorAll('section,div,aside').forEach(el => {
      const t = (el.innerText || '').toLowerCase();
      if (el.offsetParent !== null && (t.includes('getting started') || t.includes('onboarding') || t.includes('complete your setup'))) {
        el.remove();
      }
    });
  }
  function injectCSS() {
    if (document.getElementById('zv-kill-onboarding')) return;
    const style = document.createElement('style');
    style.id = 'zv-kill-onboarding';
    style.textContent = `
      [data-testid*="onboard" i],
      [class*="onboard" i],
      [id*="onboard" i],
      .crm-onboarding,
      .crm-getting-started { display: none !important; }
    `;
    document.head.appendChild(style);
  }
  function onRouteChange() {
    injectCSS();
    setTimeout(nukeNow, 120); // after SPA renders
  }
  document.addEventListener('DOMContentLoaded', () => {
    onRouteChange();
    new MutationObserver(() => { if (isCRMRoute()) nukeNow(); })
      .observe(document, { childList: true, subtree: true });
  });
  try { window.frappe?.router?.on?.('change', onRouteChange); } catch {}
})();
