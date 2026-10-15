/**
 * Middleware del Servidor SCADA SvelteKit 2
 * Gestiona autenticación por cookies, trazabilidad de latencia y control de seguridad.
 */
export async function handle({ event, resolve }) {
  event.locals.tiempoInicio = performance.now();

  // Lectura de la cookie de sesión del operador/ingeniero
  const sesionCookie = event.cookies.get('scada_auth_token');

  if (sesionCookie === 'token_ingeniero') {
    event.locals.user = {
      id: 'ING-2026',
      nombre: 'Ing. Carlos Benítez',
      rol: 'ingeniero_jefe'
    };
  } else if (sesionCookie === 'token_operador') {
    event.locals.user = {
      id: 'OP-042',
      nombre: 'Operador Mecatrónico',
      rol: 'operador_planta'
    };
  } else {
    // Por defecto, usuario operador predeterminado si no hay cookie
    event.locals.user = {
      id: 'OP-GUEST',
      nombre: 'Operador Invitado',
      rol: 'operador_planta'
    };
  }

  const response = await resolve(event);

  // Inyección de métricas de rendimiento estándar
  const duracionMs = (performance.now() - event.locals.tiempoInicio).toFixed(2);
  response.headers.set('Server-Timing', `scada_core;dur=${duracionMs};desc="SCADA Core Server Execution"`);
  response.headers.set('X-Robots-Tag', 'noindex, nofollow');

  return response;
}
