window.Delivery = (() => {
  const clave = 'delivery_token';
  function token() { return sessionStorage.getItem(clave); }
  function guardarToken(valor) { sessionStorage.setItem(clave, valor); }
  function salir() { sessionStorage.removeItem(clave); location.assign('/login/'); }
  async function api(url, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.body !== undefined) headers.set('Content-Type', 'application/json');
    if (token()) headers.set('Authorization', 'Token ' + token());
    const response = await fetch(url, { ...options, headers });
    const raw = await response.text();
    let datos;
    try { datos = raw ? JSON.parse(raw) : null; } catch { datos = raw; }
    if (!response.ok) {
      const detalle = typeof datos === 'object' && datos !== null
        ? (datos.detail || Object.entries(datos).map(([k, v]) => `${k}: ${v}`).join(' | '))
        : String(datos || 'Error en el servidor');
      throw new Error(`HTTP ${response.status}: ${detalle}`);
    }
    return datos;
  }
  function mostrar(elemento, mensaje, correcto = true) {
    elemento.textContent = mensaje;
    elemento.className = 'alert mt-3 ' + (correcto ? 'alert-success' : 'alert-danger');
  }
  async function perfil() {
    if (!token()) { location.assign('/login/'); return null; }
    try { return await api('/api/auth/yo/'); }
    catch (error) { mostrar(document.getElementById('avisoGlobal'), error.message, false); return null; }
  }
  return { token, guardarToken, salir, api, mostrar, perfil };
})();