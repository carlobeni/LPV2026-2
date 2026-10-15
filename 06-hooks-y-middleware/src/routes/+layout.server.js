/**
 * Carga de datos a nivel de layout raíz:
 * Expone event.locals.user a todas las páginas hijas.
 */
export async function load({ locals }) {
  return {
    usuario: locals.user
  };
}
