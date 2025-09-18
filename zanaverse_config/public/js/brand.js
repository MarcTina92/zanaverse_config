// Minimal, Desk-safe: do NOT change markup or styles — only retarget Help links.
(() => {
  const onDOMReady = (fn) => {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn, { once: true });
  };

  // Your targets
  const TARGETS = {
    docs:    "https://docs.zanaverse.com",
    help:    "https://help.zanaverse.com",
    support: "mailto:support@zanaverse.com"
  };

  // Matchers for existing items (by label or href patterns)
  const matchers = [
    // User Guide / Documentation → your Help/Docs
    { test: (label, href) => /user guide|documentation/i.test(label) || /erpnext\.com|frappeframework\.com/i.test(href),
      to: () => TARGETS.help },
    // Report an Issue → your support channel
    { test: (label, href) => /report an issue|raise an issue/i.test(label) || /github\.com\/.*\/issues/i.test(href),
      to: () => TARGETS.support },
    // Knowledge Base style items → your Docs
    { test: (label) => /knowledge base|learn|docs/i.test(label),
      to: () => TARGETS.docs },
  ];

  const rewriteHelpLinks = () => {
    // Find the Help dropdown (varies slightly across versions)
    const menus = document.querySelectorAll(
      '.dropdown-help, .help-dropdown, .navbar .dropdown:has([data-label="Help"])'
    );
    if (!menus.length) return;

    menus.forEach((menu) => {
      const container = menu.querySelector("ul, .dropdown-menu") || menu;
      if (!container) return;

      container.querySelectorAll("a[href]").forEach((a) => {
        const label = (a.textContent || "").trim();
        const href  = a.getAttribute("href") || "";
        for (const m of matchers) {
          if (m.test(label, href)) {
            a.href = m.to();
            a.target = "_blank";
            a.rel = "noopener";
            break; // first match wins
          }
        }
      });
    });
  };

  const run = () => {
    rewriteHelpLinks();
    // keep it working across SPA re-renders
    new MutationObserver(rewriteHelpLinks).observe(document.documentElement, { childList: true, subtree: true });
  };

  onDOMReady(run);
})();
