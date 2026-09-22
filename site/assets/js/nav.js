(function () {
  const btn = document.querySelector(".menu-btn");
  const sidebar = document.querySelector(".sidebar");
  if (btn && sidebar) {
    btn.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
    document.addEventListener("click", (e) => {
      if (!sidebar.classList.contains("open")) return;
      if (sidebar.contains(e.target) || btn.contains(e.target)) return;
      sidebar.classList.remove("open");
    });
  }
})();
