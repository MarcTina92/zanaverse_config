(() => {
  console.log("[zanaverse_config] brand.js loaded");
})();

// --- Zanaverse: hard-kill Frappe CRM SPA onboarding (runs from brand.js) ---
(function () {
  console.log("[zanaverse_config] onboarding killer active");

  const SELECTORS = [
    '[data-testid*="onboard" i]',
    '[class*="onboard" i]',
    '[id*="onboard" i]',
    '.crm-onboarding',
    '.crm-getting-started'
  ];

  function routeStr() {
    try { return (window.frappe?.get_route?.() || []).join('/').toLowerCase(); } catch { return ''; }
  }

  function isCRMRoute() {
    const r = routeStr();
    const h = (window.location.hash || '').toLowerCase();
    return r.includes('crm') || r.includes('frappe-crm') || h.includes('/crm') || h.includes('/frappe-crm');
  }

  function ensureCSS() {
    if (document.getElementById('zv-kill-onboarding')) return;
    const s = document.createElement('style');
    s.id = 'zv-kill-onboarding';
    s.textContent = `
      [data-testid*="onboard" i],
      [class*="onboard" i],
      [id*="onboard" i],
      .crm-onboarding,
      .crm-getting-started {
        display: none !important;
      }
    `;
    document.head.appendChild(s);
  }

  function nuke() {
    if (!isCRMRoute()) return;
    SELECTORS.forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
    document.querySelectorAll('section,div,aside').forEach(el => {
      const t = (el.innerText || '').toLowerCase();
      if (el.offsetParent && (t.includes('getting started') || t.includes('onboarding') || t.includes('complete your setup'))) {
        el.remove();
      }
    });
  }

  function onRouteChange() {
    ensureCSS();
    setTimeout(nuke, 120);
  }

  document.addEventListener('DOMContentLoaded', () => {
    onRouteChange();
    new MutationObserver(() => { if (isCRMRoute()) nuke(); })
      .observe(document, { childList: true, subtree: true });
  });
  try { window.frappe?.router?.on?.('change', onRouteChange); } catch {}
})();

// --- Zanaverse: onboarding killer active (v2: immediate + route-aware) ---
(function () {
  console.log("[zanaverse_config] onboarding killer active (v2)");

  const SELECTORS = [
    '[data-testid*="onboard" i]',
    '[class*="onboard" i]',
    '[id*="onboard" i]',
    '.crm-onboarding',
    '.crm-getting-started'
  ];

  function routeStr() {
    try { return (window.frappe?.get_route?.() || []).join('/').toLowerCase(); } catch { return ''; }
  }

  function isCRMRoute() {
    const r = routeStr();
    const h = (window.location.hash || '').toLowerCase();
    return r.includes('crm') || r.includes('frappe-crm') || h.includes('/crm') || h.includes('/frappe-crm');
  }

  function ensureCSS() {
    if (document.getElementById('zv-kill-onboarding')) return;
    const s = document.createElement('style');
    s.id = 'zv-kill-onboarding';
    s.textContent = `
      [data-testid*="onboard" i],
      [class*="onboard" i],
      [id*="onboard" i],
      .crm-onboarding,
      .crm-getting-started { display: none !important; }
    `;
    (document.head || document.documentElement).appendChild(s);
  }

  function nuke() {
    if (!isCRMRoute()) return;
    SELECTORS.forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
    document.querySelectorAll('section,div,aside').forEach(el => {
      const t = (el.innerText || '').toLowerCase();
      if (el.offsetParent && (t.includes('getting started') || t.includes('onboarding') || t.includes('complete your setup'))) el.remove();
    });
  }

  try { ensureCSS(); setTimeout(nuke, 120); } catch {}

  document.addEventListener('DOMContentLoaded', () => { ensureCSS(); setTimeout(nuke, 120); });
  try { window.frappe?.router?.on?.('change', () => { ensureCSS(); setTimeout(nuke, 120); }); } catch {}
  new MutationObserver(() => { if (isCRMRoute()) nuke(); }).observe(document, { childList: true, subtree: true });
})();

// --- Zanaverse: kill "Getting started" popup/banner (SPA-safe) ---
(function () {
  const PHRASES = [
    "getting started", "get started", "complete your setup",
    "welcome to crm", "onboarding", "let's get started"
  ];

  function looksLikeGettingStarted(el) {
    if (!el) return false;
    if (el.tagName === 'SYMBOL' || el.closest && el.closest('svg')) return false;
    const txt = (el.innerText || el.textContent || "").toLowerCase();
    return PHRASES.some(p => txt.includes(p));
  }

  function dismiss() {
    document.querySelectorAll('button, [role="button"], .btn').forEach(btn => {
      const t = (btn.innerText || btn.ariaLabel || "").toLowerCase();
      const isDismiss = ["skip","close","dismiss","got it","x","okay","ok"].some(s => t.includes(s));
      const dialog = btn.closest('[role="dialog"], .modal, .frappe-modal, .frappe-ui-modal, .dialog, .toast, .banner');
      if (isDismiss && dialog && looksLikeGettingStarted(dialog)) {
        try { btn.click(); } catch {}
      }
    });

    document.querySelectorAll(`
      [role="dialog"], .modal, .frappe-modal, .frappe-ui-modal, .dialog,
      .banner, .toast, .alert, section, div, article
    `).forEach(el => {
      if (el.offsetParent !== null && looksLikeGettingStarted(el)) {
        el.remove();
      }
    });
  }

  function ensureCSS() {
    if (document.getElementById('zv-kill-getting-started')) return;
    const s = document.createElement('style');
    s.id = 'zv-kill-getting-started';
    s.textContent = `
      symbol[id*="onboard" i], use[href*="icon-onboarding" i] { display: initial !important; }
      :where(aside,div,section,nav,main,article)[class*="onboard" i],
      :where(aside,div,section,nav,main,article)[id*="onboard" i],
      :where(aside,div,section,nav,main,article).crm-onboarding,
      :where(aside,div,section,nav,main,article).crm-getting-started {
        display: none !important;
      }
    `;
    (document.head || document.documentElement).appendChild(s);
  }

  function setFlags() {
    try {
      ["crm_onboarding_dismissed","crm_onboarding_completed",
       "crm_getting_started_dismissed","frappe_crm_onboarding_seen"]
        .forEach(k => localStorage.setItem(k, "1"));
    } catch {}
  }

  function tick() { ensureCSS(); setFlags(); setTimeout(dismiss, 100); }

  tick();
  document.addEventListener('DOMContentLoaded', tick);
  try { window.frappe?.router?.on?.('change', tick); } catch {}
  new MutationObserver(() => { if (document.visibilityState === 'visible') dismiss(); })
    .observe(document, { childList: true, subtree: true });
})();

// --- Zanaverse: ULTIMATE killer for CRM "Getting started" (drawer/modal/banner) ---
(function () {
  console.log("[zanaverse_config] ultimate getting-started killer loaded");

  const PHRASES = [
    "getting started",
    "welcome to frappe crm",
    "complete your setup",
    "0/9 steps completed",
    "help centre",
  ];

  function isVisible(el) {
    return !!el && el.offsetParent !== null && !el.closest('svg') && el.tagName !== 'SYMBOL';
  }

  function looksLikeGettingStarted(el) {
    if (!isVisible(el)) return false;
    const txt = (el.innerText || el.textContent || "").toLowerCase();
    return PHRASES.some(p => txt.includes(p));
  }

  function killOnce(root=document) {
    try {
      ["crm_onboarding_dismissed","crm_onboarding_completed","crm_getting_started_dismissed","frappe_crm_onboarding_seen"]
        .forEach(k => localStorage.setItem(k,"1"));
    } catch {}

    root.querySelectorAll('button,[role="button"],.btn,.button').forEach(btn => {
      const label = (btn.innerText || btn.ariaLabel || "").toLowerCase().trim();
      const isDismiss = ["skip all","skip","close","dismiss","got it","x","okay","ok"].some(s => label.includes(s));
      const host = btn.closest('[role="dialog"], .dialog, .modal, .frappe-modal, .frappe-ui-modal, .drawer, .frappe-ui-drawer, aside, section, div, article');
      if (isDismiss && host && looksLikeGettingStarted(host)) {
        try { btn.click(); } catch {}
      }
    });

    root.querySelectorAll('[role="dialog"], .dialog, .modal, .frappe-modal, .frappe-ui-modal, .drawer, .frappe-ui-drawer, aside, section, div, article')
      .forEach(el => { if (looksLikeGettingStarted(el)) el.remove(); });

    if (!document.getElementById('zv-kill-gs-css')) {
      const s = document.createElement('style');
      s.id = 'zv-kill-gs-css';
      s.textContent = `
        symbol[id*="onboard" i], use[href*="icon-onboarding" i] { display: initial !important; }
        .frappe-ui-drawer, .frappe-ui-modal, .frappe-modal, .modal, .dialog, .banner, .toast, .alert { }
      `;
      (document.head || document.documentElement).appendChild(s);
    }
  }

  killOnce();
  document.addEventListener('DOMContentLoaded', () => setTimeout(killOnce, 60));
  try { window.frappe?.router?.on?.('change', () => setTimeout(killOnce, 60)); } catch {}
})();
