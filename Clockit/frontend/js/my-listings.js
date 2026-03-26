async function loadMyListings() {
  const container = document.getElementById("my-listings-content");
  if (!container) return;
 
  if (!window.auth.requireAuth()) return;
 
  try {
    const listings = await window.api.apiGet("/listings/my");
    renderMyListings(listings, container);
  } catch (err) {
    container.innerHTML = `<p class="error">${err.message}</p>`;
  }
}
 
function renderMyListings(listings, container) {
  const t = window.i18n.t;
 
  if (listings.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p data-i18n="no_my_listings">${t("no_my_listings")}</p>
        <a href="/sell.html" class="btn btn-primary" data-i18n="nav_sell">${t("nav_sell")}</a>
      </div>
    `;
    window.i18n.translatePage();
    return;
  }
 
  let rows = "";
  for (const l of listings) {
    const statusClass = l.status === "active" ? "status-active" : "status-deactivated";
    const statusText = l.status === "active" ? t("active") : t("deactivated");
    const deactivateBtn =
      l.status === "active"
        ? `<button class="btn btn-danger btn-sm" onclick="deactivateListing(${l.id})" data-i18n="btn_deactivate">${t("btn_deactivate")}</button>`
        : "";
 
    rows += `
      <tr>
        <td>${l.event_title || "-"}</td>
        <td>${l.ticket_type || "-"}</td>
        <td>${l.quantity_available}</td>
        <td>&euro;${parseFloat(l.price).toFixed(2)}</td>
        <td><span class="status-badge ${statusClass}">${statusText}</span></td>
        <td>${deactivateBtn}</td>
      </tr>
    `;
  }
 
  container.innerHTML = `
    <table class="cart-table">
      <thead>
        <tr>
          <th>Event</th>
          <th data-i18n="ticket_type">${t("ticket_type")}</th>
          <th data-i18n="quantity">${t("quantity")}</th>
          <th data-i18n="price">${t("price")}</th>
          <th data-i18n="status">${t("status")}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
    <a href="/sell.html" class="btn btn-primary" data-i18n="nav_sell">${t("nav_sell")}</a>
  `;
  window.i18n.translatePage();
}
 
async function deactivateListing(listingId) {
  try {
    await window.api.apiPatch(`/listings/${listingId}/deactivate`, {});
    showToast("Listing deactivated.");
    loadMyListings();
  } catch (err) {
    showToast(err.message, "error");
  }
}
 
window.loadMyListings = loadMyListings;
window.deactivateListing = deactivateListing;