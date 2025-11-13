document.addEventListener("DOMContentLoaded", () => {
  const logoutBtn = document.getElementById("logoutBtn");
  const menuButtons = document.querySelectorAll(".menu-btn");
  const sections = document.querySelectorAll(".admin-section");

  logoutBtn.addEventListener("click", () => {
    window.location.href = "/";
  });

  menuButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-section");

      menuButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      sections.forEach((section) => {
        const id = section.id.replace("section-", "");
        section.classList.toggle("visible", id === target);
      });
    });
  });
});
