async function loadEventDetail() {
  const container = document.getElementById("event-detail");
  if (!container) return;
 
  const params = new URLSearchParams(window.location.search);
  const eventId = params.get("id");
  if (!eventId) {
    container.innerHTML = `<p class="error">No event ID provided.</p>`;
    return;
  }
 
  try {
    const event = await window.api.apiGet(`/events/${eventId}`);
    const listings = await window.api.apiGet(`/events/${eventId}/listings`);
    renderEventDetail(event, listings, container);
  } catch (err) {
    container.innerHTML = `<p class="error">${err.message}</p>`;
  }
}
 
function renderEventDetail(event, listings, container) {
  const t = window.i18n.t;
  const date = new Date(event.starts_at).toLocaleDateString(window.i18n.getLang() === "el" ? "el-GR" : "en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
 
  let listingsHtml = "";
  if (listings.length === 0) {
    listingsHtml = `<p class="empty-state" data-i18n="no_listings">${t("no_listings")}</p>`;
  } else {
    listingsHtml = `<div class="listings-grid">`;
    for (const l of listings) {
      listingsHtml += `
        <div class="listing-card">
          <div class="listing-info">
            <h4>${l.ticket_type || "Standard"}</h4>
            ${l.section ? `<p><span data-i18n="section">${t("section")}</span>: ${l.section}</p>` : ""}
            ${l.row_name ? `<p><span data-i18n="row">${t("row")}</span>: ${l.row_name}</p>` : ""}
            ${l.seat ? `<p><span data-i18n="seat">${t("seat")}</span>: ${l.seat}</p>` : ""}
            <p class="listing-seller"><span data-i18n="seller">${t("seller")}</span>: ${l.seller_name || "-"}</p>
          </div>
          <div class="listing-price-action">
            <p class="listing-price">&euro;${parseFloat(l.price).toFixed(2)} <small data-i18n="per_ticket">${t("per_ticket")}</small></p>
            <p class="listing-avail">${l.quantity_available} ${t("available")}</p>
            <div class="listing-add">
              <input type="number" min="1" max="${l.quantity_available}" value="1" id="qty-listing-${l.id}" class="qty-input">
              <button class="btn btn-primary btn-sm" onclick="addToCartFromListing(${l.id})" data-i18n="add_to_cart">${t("add_to_cart")}</button>
            </div>
          </div>
        </div>
      `;
    }
    listingsHtml += `</div>`;
  }
 
  container.innerHTML = `
    <div class="event-hero">
      <div class="event-hero-info">
        <span class="badge">${event.category}</span>
        <h1>${event.title}</h1>
        <p class="event-meta"><strong data-i18n="venue">${t("venue")}</strong>: ${event.venue}, ${event.city}</p>
        <p class="event-meta"><strong data-i18n="date_time">${t("date_time")}</strong>: ${date}</p>
        ${event.description ? `<p class="event-desc">${event.description}</p>` : ""}
      </div>
    </div>
    <h2 data-i18n="available_tickets">${t("available_tickets")}</h2>
    ${listingsHtml}
    <a href="/events.html" class="btn btn-outline" data-i18n="back">${t("back")}</a>
  `;
  window.i18n.translatePage();
}
 
function addToCartFromListing(listingId) {
  const input = document.getElementById(`qty-listing-${listingId}`);
  const qty = parseInt(input?.value || "1");
  if (isNaN(qty) || qty < 1) return;
  window.addToCart(listingId, qty);
}
 
window.loadEventDetail = loadEventDetail;
window.addToCartFromListing = addToCartFromListing;