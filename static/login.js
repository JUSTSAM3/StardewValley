document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const errorBox = document.getElementById("loginError");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    errorBox.textContent = "";

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
      errorBox.textContent = "Por favor, completa usuario y contraseña.";
      return;
    }

    if (username === "admin" && password === "admin") {
      window.location.href = "/admin";
    } else {
      errorBox.textContent = "Usuario o contraseña incorrectos.";
    }
  });

  [usernameInput, passwordInput].forEach((input) => {
    input.addEventListener("input", () => {
      if (errorBox.textContent) {
        errorBox.textContent = "";
      }
    });
  });
});
