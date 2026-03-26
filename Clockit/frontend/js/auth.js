let currentUser = null;
 
async function checkAuth() {
  const token = localStorage.getItem("clockit_token");
  if (!token) {
    currentUser = null;
    return null;
  }
  try {
    currentUser = await window.api.apiGet("/auth/me");
    return currentUser;
  } catch {
    localStorage.removeItem("clockit_token");
    currentUser = null;
    return null;
  }
}
 
function logout() {
  localStorage.removeItem("clockit_token");
  currentUser = null;
  window.location.href = "/";
}
 
function isLoggedIn() {
  return !!localStorage.getItem("clockit_token");
}
 
function requireAuth() {
  if (!isLoggedIn()) {
    showToast(window.i18n.t("requires_login"), "warning");
    setTimeout(() => (window.location.href = "/login.html"), 1000);
    return false;
  }
  return true;
}
 
function getUser() {
  return currentUser;
}
 
window.auth = { checkAuth, logout, isLoggedIn, requireAuth, getUser };