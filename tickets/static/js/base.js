function toggleDropdown() {
  const dropdown = document.getElementById('profileDropdown');
  dropdown.classList.toggle('show');
}

// Закрытие при клике вне блока
window.addEventListener('click', function (e) {
  const dropdown = document.getElementById('profileDropdown');
  if (dropdown && !dropdown.contains(e.target)) {
    dropdown.classList.remove('show');
  }
});

// Назначаем обработчик клика на стрелку
document.addEventListener("DOMContentLoaded", function () {
  const arrow = document.getElementById("dropdownArrow");

  if (arrow) {
    arrow.addEventListener("click", function (e) {
      e.stopPropagation();
      toggleDropdown();
    });
  }
});
