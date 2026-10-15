import { redirect } from '@sveltejs/kit';

/**
 * Hook universal de servidor: intercepta cada petición antes de resolver la ruta.
 */
export async function handle({ event, resolve }) {
  const inicio = performance.now();

  // 1. Lectura de cookie de sesión simulada
  const token = event.cookies.get('scada_session');
  
  if (token === 'token_admin') {
    event.locals.user = { id: 'ADM-01', nombre: 'Ing. Carlos Benítez', rol: 'administrador' };
  } else if (token === 'token_operador') {
    event.locals.user = { id: 'OP-44', nombre: 'Operador de Turno', rol: 'operador' };
  } else {
    event.locals.user = null;
  }

  // 2. Protección de rutas críticas (RBAC: Role-Based Access Control)
  if (event.url.pathname.startsWith('/admin')) {
    if (!event.locals.user) {
      // Si no ha iniciado sesión, redirigir a la página principal con flag
      redirect(303, '/?alerta=debe_iniciar_sesion');
    }

    if (event.locals.user.rol !== 'administrador') {
      // Si está autenticado pero no es administrador, denegar acceso
      redirect(303, '/?alerta=acceso_denegado_requiere_admin');
    }
  }

  // 3. Resolución normal de la ruta
  const response = await resolve(event);

  // 4. Inyección de métricas de rendimiento y seguridad
  const tiempoMs = (performance.now() - inicio).toFixed(2);
  response.headers.set('Server-Timing', `app;dur=${tiempoMs};desc="SvelteKit Processing"`);
  response.headers.set('X-Content-Type-Options', 'nosniff');

  return response;
}

export function handleError({ error, event, status, message }) {
  console.error(`[SCADA Server Error] ${status} en ${event.url.pathname}:`, error);
  return {
    message: message || 'Fallo interno en el subsistema de telemetría.'
  };
}
