async function initSellPage() {
  if (!window.auth.requireAuth()) return;
 
  const select = document.getElementById("sell-event");
  if (!select) return;
 
  try {
    const data = await window.api.apiGet("/events?per_page=50&sort_by=date_asc");
    data.events.forEach((ev) => {
      const opt = document.createElement("option");
      opt.value = ev.id;
      const date = new Date(ev.starts_at).toLocaleDateString("en-US", { month: "short", day: "numeric" });
      opt.textContent = `${ev.title} (${date}) - ${ev.city}`;
      select.appendChild(opt);
    });
  } catch (err) {
    showToast(err.message, "error");
  }
 
  const form = document.getElementById("sell-form");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const eventId = parseInt(document.getElementById("sell-event").value);
      const ticketType = document.getElementById("sell-ticket-type").value || null;
      const section = document.getElementById("sell-section").value || null;
      const rowName = document.getElementById("sell-row").value || null;
      const seat = document.getElementById("sell-seat").value || null;
      const qty = parseInt(document.getElementById("sell-qty").value);
      const price = parseFloat(document.getElementById("sell-price").value);
 
      if (!eventId || isNaN(qty) || qty < 1 || isNaN(price) || price <= 0) {
        showToast("Please fill in all required fields correctly.", "error");
        return;
      }
 
      try {
        await window.api.apiPost("/listings", {
          event_id: eventId,
          ticket_type: ticketType,
          section: section,
          row_name: rowName,
          seat: seat,
          quantity_available: qty,
          price: price,
          currency: "EUR",
        });
        showToast(window.i18n.t("listing_created"));
        setTimeout(() => (window.location.href = "/my-listings.html"), 1000);
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  }
}
 
window.initSellPage = initSellPage;