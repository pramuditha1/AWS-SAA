(function () {
  const grid = document.getElementById("service-catalog");
  if (!grid || !window.SAA_CATALOG) return;

  const priBtns = document.querySelectorAll("[data-priority]");
  const catBtns = document.querySelectorAll("[data-category]");
  const countEl = document.getElementById("shown-count");
  let priority = "all";
  let category = "all";

  function apply() {
    const cards = grid.querySelectorAll(".svc-card");
    let shown = 0;
    cards.forEach((card) => {
      const p = card.getAttribute("data-priority");
      const c = card.getAttribute("data-category");
      const okP = priority === "all" || p === priority;
      const okC = category === "all" || c === category;
      const show = okP && okC;
      card.classList.toggle("hidden", !show);
      if (show) shown += 1;
    });
    if (countEl) countEl.textContent = String(shown);
  }

  priBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      priority = btn.getAttribute("data-priority");
      priBtns.forEach((b) => b.classList.toggle("active", b === btn));
      apply();
    });
  });
  catBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      category = btn.getAttribute("data-category");
      catBtns.forEach((b) => b.classList.toggle("active", b === btn));
      apply();
    });
  });
  apply();
})();
