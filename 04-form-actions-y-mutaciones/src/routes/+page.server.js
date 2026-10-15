import { fail } from '@sveltejs/kit';

// Base de datos en memoria para propósitos de la guía
let sensoresInventario = [
  { id: 'S-101', tag: 'PT100-LINEA-1', tipo: 'Temperatura', valor: 22.4, calibrado: true },
  { id: 'S-102', tag: 'PIEZO-ALTA-PRES', tipo: 'Presión', valor: 4.8, calibrado: false }
];

export async function load() {
  return {
    sensores: sensoresInventario
  };
}

export const actions = {
  // Acción para dar de alta un nuevo sensor
  crear: async ({ request }) => {
    // Simulación de delay de red/escritura en disco
    await new Promise(r => setTimeout(r, 600));

    const formData = await request.formData();
    const tag = formData.get('tag')?.toString().trim();
    const tipo = formData.get('tipo')?.toString().trim();
    const valorInicialStr = formData.get('valorInicial')?.toString().trim();

    // Validaciones de ingeniería
    if (!tag || tag.length < 3) {
      return fail(400, {
        error: 'El Tag identificador debe contener al menos 3 caracteres.',
        campos: { tag, tipo, valorInicial: valorInicialStr }
      });
    }

    const valorInicial = parseFloat(valorInicialStr || '0');
    if (isNaN(valorInicial)) {
      return fail(400, {
        error: 'El valor inicial debe ser una magnitud numérica válida.',
        campos: { tag, tipo, valorInicial: valorInicialStr }
      });
    }

    const nuevoSensor = {
      id: `S-${Math.floor(100 + Math.random() * 900)}`,
      tag: tag.toUpperCase(),
      tipo: tipo || 'General',
      valor: valorInicial,
      calibrado: false
    };

    sensoresInventario.push(nuevoSensor);

    return {
      exito: true,
      mensaje: `Sensor ${nuevoSensor.tag} registrado exitosamente con ID ${nuevoSensor.id}.`
    };
  },

  // Acción nominada para calibrar un sensor existente
  calibrar: async ({ request }) => {
    await new Promise(r => setTimeout(r, 400));
    const formData = await request.formData();
    const id = formData.get('id')?.toString();

    const sensor = sensoresInventario.find(s => s.id === id);
    if (!sensor) {
      return fail(404, { error: `No se halló el sensor con ID ${id} para calibrar.` });
    }

    sensor.calibrado = true;
    return {
      exito: true,
      mensaje: `Sensor ${sensor.tag} recalibrado a cero de referencia.`
    };
  },

  // Acción nominada para eliminar un sensor
  eliminar: async ({ request }) => {
    const formData = await request.formData();
    const id = formData.get('id')?.toString();

    sensoresInventario = sensoresInventario.filter(s => s.id !== id);
    return {
      exito: true,
      mensaje: `Sensor ${id} dado de baja de la línea.`
    };
  }
};
