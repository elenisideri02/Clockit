let currentPage = 1;
let totalPages = 1;
 
async function loadEvents() {
  const grid = document.getElementById("events-grid");
  if (!grid) return;
 
  await loadFilters();
 
  const params = buildParams();
  try {
    const data = await window.api.apiGet(`/events?${params}`);
    totalPages = Math.ceil(data.total / data.per_page);
    currentPage = data.page;
 
    if (data.events.length === 0) {
      grid.innerHTML = `<p class="empty-state" data-i18n="no_events">${window.i18n.t("no_events")}</p>`;
    } else {
      grid.innerHTML = data.events.map((ev) => window.eventCard(ev)).join("");
    }
    renderPagination();
  } catch (err) {
    grid.innerHTML = `<p class="error">${err.message}</p>`;
  }
  window.i18n.translatePage();
}
 
async function loadFilters() {
  const catSelect = document.getElementById("filter-category");
  const citySelect = document.getElementById("filter-city");
 
  if (catSelect && catSelect.options.length <= 1) {
    try {
      const cats = await window.api.apiGet("/events/categories");
      cats.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        catSelect.appendChild(opt);
      });
    } catch {}
  }
 
  if (citySelect && citySelect.options.length <= 1) {
    try {
      const cities = await window.api.apiGet("/events/cities");
      cities.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        citySelect.appendChild(opt);
      });
    } catch {}
  }
}
 
function buildParams() {
  const search = document.getElementById("search-input")?.value || "";
  const category = document.getElementById("filter-category")?.value || "";
  const city = document.getElementById("filter-city")?.value || "";
  const sort = document.getElementById("sort-select")?.value || "date_asc";
 
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (category) params.set("category", category);
  if (city) params.set("city", city);
  params.set("sort_by", sort);
  params.set("page", currentPage);
  params.set("per_page", 12);
  return params.toString();
}
 
function renderPagination() {
  const container = document.getElementById("pagination");
  if (!container) return;
  if (totalPages <= 1) {
    container.innerHTML = "";
    return;
  }
 
  let html = "";
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="page-btn ${i === currentPage ? "active" : ""}" onclick="goToPage(${i})">${i}</button>`;
  }
  container.innerHTML = html;
}
 
function goToPage(page) {
  currentPage = page;
  loadEvents();
}
 
function onSearchOrFilter() {
  currentPage = 1;
  loadEvents();
}
 
window.loadEvents = loadEvents;
window.goToPage = goToPage;
window.onSearchOrFilter = onSearchOrFilter;