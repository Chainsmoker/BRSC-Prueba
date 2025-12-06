const mobileNav = document.querySelector(".hamburger");
const navbar = document.querySelector(".menubar");
const dropdown = document.querySelector(".dropdown");
const dropdownBtn = document.querySelector(".dropdown-btn");

const toggleNav = () => {
  navbar.classList.toggle("active");
  mobileNav.classList.toggle("hamburger-active");
};

mobileNav.addEventListener("click", () => toggleNav());

const toggleDrop = () => {
  dropdown.classList.toggle("active-dropdown");
  dropdownBtn.classList.toggle("dropdown-btn-active");
};

dropdownBtn.addEventListener("click", (event) => {
  event.stopPropagation(); // 👈 Esto evita que el clic en el botón cierre el menú inmediatamente
  toggleDrop();
});

// ✅ Cierra el dropdown si haces clic fuera
document.addEventListener("click", (event) => {
  const isClickInside = dropdown.contains(event.target) || dropdownBtn.contains(event.target);
  if (!isClickInside) {
    dropdown.classList.remove("active-dropdown");
    dropdownBtn.classList.remove("dropdown-btn-active");
  }
});

function mostrarAlerta(event) {
        event.preventDefault();
        Swal.fire({
            icon: "error",
            title: "Módulo en desarrollo",
            text: "La funcionalidad seleccionada se encuentra en proceso de implementación.",
        });
    }