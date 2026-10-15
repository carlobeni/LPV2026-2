export const actions = {
  iniciarAdmin: async ({ cookies }) => {
    cookies.set('scada_session', 'token_admin', {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      maxAge: 60 * 60
    });
    return { exito: true };
  },

  iniciarOperador: async ({ cookies }) => {
    cookies.set('scada_session', 'token_operador', {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      maxAge: 60 * 60
    });
    return { exito: true };
  },

  cerrarSesion: async ({ cookies }) => {
    cookies.delete('scada_session', { path: '/' });
    return { exito: true };
  }
};
