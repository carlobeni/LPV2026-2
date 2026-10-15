import { fail } from '@sveltejs/kit';

// Estado global de la planta en memoria del servidor
let estadoPlanta = {
  modoOperativo: 'AUTOMATICO', // 'AUTOMATICO' | 'MANUAL' | 'MANTENIMIENTO' | 'EMERGENCIA'
  setpointPresion: 5.0,
  setpointTemp: 80.0,
  paradaEmergenciaActiva: false,
  actuadores: [
    { id: 'ACT-01', tag: 'Bomba Principal Hidráulica', encendido: true, potenciaPct: 78 },
    { id: 'ACT-02', tag: 'Compresor de Aire Auxiliar', encendido: true, potenciaPct: 62 },
    { id: 'ACT-03', tag: 'Válvula de Alivio Seguridad', encendido: false, potenciaPct: 0 },
    { id: 'ACT-04', tag: 'Ventilador Torre Enfriamiento', encendido: true, potenciaPct: 85 }
  ],
  bitacoraEventos: [
    { timestamp: new Date(Date.now() - 360000).toLocaleTimeString('es-PY'), mensaje: 'Sistema SCADA iniciado en modo AUTOMATICO', tipo: 'INFO' },
    { timestamp: new Date(Date.now() - 180000).toLocaleTimeString('es-PY'), mensaje: 'Comprobación de bus CAN: Todos los nodos sincronizados', tipo: 'INFO' }
  ]
};

export async function load() {
  return {
    planta: estadoPlanta,
    timestampCarga: new Date().toLocaleTimeString('es-PY')
  };
}

export const actions = {
  // Disparo de parada de emergencia general
  paradaEmergencia: async () => {
    estadoPlanta.paradaEmergenciaActiva = true;
    estadoPlanta.modoOperativo = 'EMERGENCIA';

    // Desconectar actuadores por seguridad física
    estadoPlanta.actuadores.forEach(a => {
      a.encendido = false;
      a.potenciaPct = 0;
    });

    // Abrir válvula de alivio
    const valvulaAlivio = estadoPlanta.actuadores.find(a => a.id === 'ACT-03');
    if (valvulaAlivio) valvulaAlivio.encendido = true;

    estadoPlanta.bitacoraEventos.unshift({
      timestamp: new Date().toLocaleTimeString('es-PY'),
      mensaje: 'DISPARO DE PARADA DE EMERGENCIA - Actuadores desacoplados',
      tipo: 'PELIGRO'
    });

    return {
      exito: true,
      mensaje: 'PARADA DE EMERGENCIA EJECUTADA: Planta en estado seguro.'
    };
  },

  // Rearmar el sistema tras normalizar la planta
  rearmarSistema: async () => {
    estadoPlanta.paradaEmergenciaActiva = false;
    estadoPlanta.modoOperativo = 'AUTOMATICO';

    const valvulaAlivio = estadoPlanta.actuadores.find(a => a.id === 'ACT-03');
    if (valvulaAlivio) valvulaAlivio.encendido = false;

    estadoPlanta.bitacoraEventos.unshift({
      timestamp: new Date().toLocaleTimeString('es-PY'),
      mensaje: 'Sistema rearmado satisfactoriamente por el operador.',
      tipo: 'OK'
    });

    return {
      exito: true,
      mensaje: 'Sistema rearmado. Modo AUTOMÁTICO restablecido.'
    };
  },

  // Calibración de Setpoint de Presión
  ajustarSetpoint: async ({ request }) => {
    const formData = await request.formData();
    const presionStr = formData.get('presion')?.toString();
    const nuevoValor = parseFloat(presionStr || '');

    if (isNaN(nuevoValor)) {
      return fail(400, {
        error: 'El valor de consigna debe ser un número decimal válido.',
        campo: 'presion'
      });
    }

    // Límites físicos de diseño de la caldera
    if (nuevoValor < 1.0 || nuevoValor > 8.0) {
      return fail(400, {
        error: `El setpoint ${nuevoValor} bar está fuera de los límites de seguridad (1.0 bar a 8.0 bar).`,
        campo: 'presion'
      });
    }

    estadoPlanta.setpointPresion = nuevoValor;

    estadoPlanta.bitacoraEventos.unshift({
      timestamp: new Date().toLocaleTimeString('es-PY'),
      mensaje: `Setpoint de presión ajustado a ${nuevoValor.toFixed(2)} bar`,
      tipo: 'INFO'
    });

    return {
      exito: true,
      mensaje: `Consigna de presión actualizada a ${nuevoValor.toFixed(2)} bar.`
    };
  },

  // Alternar estado individual de actuador
  alternarActuador: async ({ request }) => {
    if (estadoPlanta.paradaEmergenciaActiva) {
      return fail(400, {
        error: 'No se pueden maniobrar actuadores individuales mientras persista la PARADA DE EMERGENCIA.'
      });
    }

    const formData = await request.formData();
    const id = formData.get('id')?.toString();

    const act = estadoPlanta.actuadores.find(a => a.id === id);
    if (!act) {
      return fail(404, { error: 'Actuador no hallado en el bus.' });
    }

    act.encendido = !act.encendido;
    act.potenciaPct = act.encendido ? 75 : 0;

    estadoPlanta.bitacoraEventos.unshift({
      timestamp: new Date().toLocaleTimeString('es-PY'),
      mensaje: `Actuador ${act.tag} [${act.id}]: ${act.encendido ? 'ARRANCADO' : 'DETENIDO'}`,
      tipo: 'MANIOBRA'
    });

    return { exito: true };
  }
};
