async function loadHomePage() {
  const grid = document.getElementById("featured-grid");
  if (!grid) return;
 
  try {
    const data = await window.api.apiGet("/events?per_page=4&sort_by=date_asc");
    if (data.events.length === 0) {
      grid.innerHTML = `<p data-i18n="no_events">${window.i18n.t("no_events")}</p>`;
      return;
    }
    grid.innerHTML = data.events.map((ev) => eventCard(ev)).join("");
  } catch (err) {
    grid.innerHTML = `<p class="error">${err.message}</p>`;
  }
}
 
function eventCard(ev) {
  const date = new Date(ev.starts_at).toLocaleDateString(window.i18n.getLang() === "el" ? "el-GR" : "en-US", {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
  return `
    <div class="event-card" onclick="window.location.href='/event.html?id=${ev.id}'">
      <div class="event-card-badge">${ev.category}</div>
      <h3>${ev.title}</h3>
      <p class="event-card-venue">${ev.venue}, ${ev.city}</p>
      <p class="event-card-date">${date}</p>
      <a href="/event.html?id=${ev.id}" class="btn btn-primary btn-sm" data-i18n="view_details">${window.i18n.t("view_details")}</a>
    </div>
  `;
}
 
window.loadHomePage = loadHomePage;
window.eventCard = eventCard;