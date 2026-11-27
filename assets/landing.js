// Helio landing page behaviour. Works without it: every section is readable with JS off.

// Paste the App Store link here once Helio is live; every "download" button picks it up.
const APP_STORE_URL = "";

document.documentElement.classList.remove("no-js");

// Download buttons
document.querySelectorAll("[data-download]").forEach((a) => {
  if (APP_STORE_URL) {
    a.href = APP_STORE_URL;
    a.rel = "noopener";
    const live = a.getAttribute("data-live-label");
    if (live) a.querySelector("[data-label]").textContent = live;
  }
});

// Header border once the page scrolls
const header = document.querySelector(".top");
const onScroll = () => header && header.classList.toggle("scrolled", window.scrollY > 8);
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Feature tabs
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab, focus) {
  tabs.forEach((t) => {
    const on = t === tab;
    t.setAttribute("aria-selected", on);
    t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
  });
  if (focus) tab.focus();
}
tabs.forEach((t, i) => {
  t.addEventListener("click", () => selectTab(t));
  t.addEventListener("keydown", (e) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
    if (!step) return;
    e.preventDefault();
    selectTab(tabs[(i + step + tabs.length) % tabs.length], true);
  });
});
if (tabs.length) selectTab(tabs[0]);

// Monthly / yearly prices
const billingButtons = document.querySelectorAll("[data-billing]");
billingButtons.forEach((b) =>
  b.addEventListener("click", () => {
    const mode = b.dataset.billing;
    billingButtons.forEach((x) => x.setAttribute("aria-pressed", x === b));
    document.querySelectorAll("[data-monthly]").forEach((el) => {
      el.textContent = el.dataset[mode];
    });
  })
);

// Reveal on scroll
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const items = document.querySelectorAll(".reveal");
if (reduce || !("IntersectionObserver" in window)) {
  items.forEach((el) => el.classList.add("in"));
} else {
  const io = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      }),
    { rootMargin: "0px 0px -8% 0px" }
  );
  items.forEach((el) => io.observe(el));
}
