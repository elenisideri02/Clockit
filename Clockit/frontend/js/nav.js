function buildNav() {
  const nav = document.getElementById("main-nav");
  if (!nav) return;
 
  const user = window.auth.getUser();
  const loggedIn = window.auth.isLoggedIn();
 
  let userLinks = "";
  if (loggedIn && user) {
    userLinks = `
      <span class="nav-welcome">${window.i18n.t("nav_welcome")} ${user.display_name}</span>
      <a href="/sell.html" data-i18n="nav_sell">${window.i18n.t("nav_sell")}</a>
      <a href="/my-listings.html" data-i18n="nav_my_listings">${window.i18n.t("nav_my_listings")}</a>
      <a href="/cart.html" class="nav-cart" data-i18n="nav_cart">${window.i18n.t("nav_cart")}</a>
      <button class="nav-btn" onclick="window.auth.logout()" data-i18n="nav_logout">${window.i18n.t("nav_logout")}</button>
    `;
  } else {
    userLinks = `
      <a href="/login.html" data-i18n="nav_login">${window.i18n.t("nav_login")}</a>
    `;
  }
 
  nav.innerHTML = `
    <div class="nav-container">
      <a href="/" class="nav-logo">
        <img src="/assets/clockit-logo.png" alt="Clockit" onerror="this.style.display='none';this.nextElementSibling.style.display='inline'">
        <span class="logo-text" style="display:none">Clockit</span>
        <span class="logo-text-always">Clockit</span>
      </a>
      <button class="hamburger" id="hamburger-btn" onclick="toggleMobileMenu()">&#9776;</button>
      <div class="nav-links" id="nav-links">
        <a href="/" data-i18n="nav_home">${window.i18n.t("nav_home")}</a>
        <a href="/events.html" data-i18n="nav_events">${window.i18n.t("nav_events")}</a>
        <a href="/about.html" data-i18n="nav_about">${window.i18n.t("nav_about")}</a>
        <a href="/help.html" data-i18n="nav_help">${window.i18n.t("nav_help")}</a>
        ${userLinks}
        <button class="lang-btn" id="lang-toggle" onclick="window.i18n.toggleLang(); buildNav();">${window.i18n.t("lang_toggle")}</button>
      </div>
    </div>
  `;
}
 
function toggleMobileMenu() {
  const links = document.getElementById("nav-links");
  if (links) links.classList.toggle("open");
}
 
function buildFooter() {
  const footer = document.getElementById("main-footer");
  if (!footer) return;
  footer.innerHTML = `
    <div class="footer-container">
      <p data-i18n="footer_text">${window.i18n.t("footer_text")}</p>
      <p>&copy; 2026 Clockit</p>
    </div>
  `;
}
 
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 10);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
 
window.showToast = showToast;
 
async function initPage() {
  await window.auth.checkAuth();
  buildNav();
  buildFooter();
  window.i18n.translatePage();
}
 
window.initPage = initPage;