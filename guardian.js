// static/guardian.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  if (form) {
    form.addEventListener("submit", () => {
      Swal.fire({
        title: "Generating QR Code...",
        text: "Please wait a moment.",
        icon: "info",
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true
      });
    });
  }
});