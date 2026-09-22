(function () {
  const input = document.getElementById("site-search");
  const box = document.getElementById("search-results");
  if (!input || !box || !window.SAA_CATALOG) return;

  const root = document.body.getAttribute("data-root") || "";
  const catalog = window.SAA_CATALOG;

  function render(q) {
    const query = q.trim().toLowerCase();
    if (!query) {
      box.hidden = true;
      box.innerHTML = "";
      return;
    }
    const hits = catalog.filter((item) => {
      const hay = (item.name + " " + item.category + " " + item.blurb + " " + (item.aliases || "")).toLowerCase();
      return hay.includes(query);
    }).slice(0, 12);

    if (!hits.length) {
      box.hidden = false;
      box.innerHTML = '<div class="search-empty">No matching services or pages.</div>';
      return;
    }
    box.hidden = false;
    box.innerHTML = hits.map((item, i) => (
      '<a class="search-item' + (i === 0 ? ' active' : '') + '" href="' + root + item.href + '">' +
        '<div class="kicker">' + item.category + ' · ' + item.priority + '</div>' +
        '<div>' + item.name + '</div>' +
      '</a>'
    )).join("");
  }

  input.addEventListener("input", () => render(input.value));
  input.addEventListener("focus", () => render(input.value));
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      box.hidden = true;
      input.blur();
    }
    if (e.key === "Enter") {
      const first = box.querySelector(".search-item");
      if (first) location.href = first.getAttribute("href");
    }
  });
  document.addEventListener("click", (e) => {
    if (!box.contains(e.target) && e.target !== input) box.hidden = true;
  });
})();
