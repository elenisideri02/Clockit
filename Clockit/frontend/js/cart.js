async function loadCart() {
  const container = document.getElementById("cart-content");
  if (!container) return;
 
  if (!window.auth.requireAuth()) return;
 
  try {
    const cart = await window.api.apiGet("/cart");
    renderCart(cart, container);
  } catch (err) {
    container.innerHTML = `<p class="error">${err.message}</p>`;
  }
}
 
function renderCart(cart, container) {
  if (!cart.items || cart.items.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p data-i18n="empty_cart">${window.i18n.t("empty_cart")}</p>
        <a href="/events.html" class="btn btn-primary" data-i18n="nav_events">${window.i18n.t("nav_events")}</a>
      </div>
    `;
    window.i18n.translatePage();
    return;
  }
 
  let rows = "";
  for (const item of cart.items) {
    const subtotal = (parseFloat(item.unit_price_snapshot) * item.quantity).toFixed(2);
    rows += `
      <tr>
        <td>${item.event_title || "-"}</td>
        <td>${item.ticket_type || "-"}</td>
        <td>&euro;${parseFloat(item.unit_price_snapshot).toFixed(2)}</td>
        <td>
          <div class="qty-control">
            <input type="number" min="1" value="${item.quantity}" id="qty-${item.id}" class="qty-input">
            <button class="btn btn-sm" onclick="updateCartItem(${item.id})" data-i18n="btn_update">${window.i18n.t("btn_update")}</button>
          </div>
        </td>
        <td>&euro;${subtotal}</td>
        <td><button class="btn btn-danger btn-sm" onclick="removeCartItem(${item.id})" data-i18n="btn_remove">${window.i18n.t("btn_remove")}</button></td>
      </tr>
    `;
  }
 
  container.innerHTML = `
    <table class="cart-table">
      <thead>
        <tr>
          <th>Event</th>
          <th data-i18n="ticket_type">${window.i18n.t("ticket_type")}</th>
          <th data-i18n="unit_price">${window.i18n.t("unit_price")}</th>
          <th data-i18n="quantity">${window.i18n.t("quantity")}</th>
          <th data-i18n="subtotal">${window.i18n.t("subtotal")}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="cart-footer">
      <div class="cart-total">
        <span data-i18n="total">${window.i18n.t("total")}</span>: <strong>&euro;${parseFloat(cart.total).toFixed(2)}</strong>
      </div>
      <button class="btn btn-danger" onclick="clearCart()" data-i18n="btn_clear">${window.i18n.t("btn_clear")}</button>
    </div>
  `;
  window.i18n.translatePage();
}
 
async function updateCartItem(itemId) {
  const input = document.getElementById(`qty-${itemId}`);
  const qty = parseInt(input.value);
  if (isNaN(qty) || qty < 1) return;
  try {
    const cart = await window.api.apiPatch(`/cart/items/${itemId}`, { quantity: qty });
    renderCart(cart, document.getElementById("cart-content"));
    showToast(window.i18n.t("cart_updated"));
  } catch (err) {
    showToast(err.message, "error");
  }
}
 
async function removeCartItem(itemId) {
  try {
    const cart = await window.api.apiDelete(`/cart/items/${itemId}`);
    renderCart(cart, document.getElementById("cart-content"));
    showToast(window.i18n.t("item_removed"));
  } catch (err) {
    showToast(err.message, "error");
  }
}
 
async function clearCart() {
  try {
    const cart = await window.api.apiDelete("/cart");
    renderCart(cart, document.getElementById("cart-content"));
    showToast(window.i18n.t("cart_cleared"));
  } catch (err) {
    showToast(err.message, "error");
  }
}
 
async function addToCart(listingId, quantity) {
  if (!window.auth.requireAuth()) return;
  try {
    await window.api.apiPost("/cart/items", { listing_id: listingId, quantity: quantity });
    showToast(window.i18n.t("added_to_cart"));
    setTimeout(() => (window.location.href = "/cart.html"), 1000);
  } catch (err) {
    showToast(err.message, "error");
  }
}
 
window.loadCart = loadCart;
window.updateCartItem = updateCartItem;
window.removeCartItem = removeCartItem;
window.clearCart = clearCart;
window.addToCart = addToCart;
 