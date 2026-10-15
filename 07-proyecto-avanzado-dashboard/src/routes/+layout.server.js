/**
 * Carga de datos global para el layout del dashboard.
 */
export async function load({ locals }) {
  return {
    usuario: locals.user,
    versionSistema: 'v2.4.0-Svelte5',
    nodoId: 'NODE-FIUNA-ASU-01'
  };
}
