(() => {
  "use strict";
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
    for (const link of nav.querySelectorAll("a")) {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    }
  }
  const buttons = document.querySelectorAll("[data-filter]");
  const shots = document.querySelectorAll(".shot[data-category]");
  for (const button of buttons) {
    button.addEventListener("click", () => {
      const selection = button.dataset.filter;
      for (const item of buttons) {
        const selected = item === button;
        item.classList.toggle("active", selected);
        item.setAttribute("aria-pressed", String(selected));
      }
      for (const card of shots) {
        card.hidden = selection !== "all" && card.dataset.category !== selection;
      }
    });
  }
})();
