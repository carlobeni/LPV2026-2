import { error } from '@sveltejs/kit';

const BASE_DATOS_SENSORES = {
  'temp-01': {
    id: 'temp-01',
    tag: 'PT100-HORNO-1',
    tipo: 'Sensor de Temperatura RTD',
    rango: '-50 °C a 400 °C',
    precision: '± 0.15 °C (Clase A)',
    bus: 'RS-485 Modbus RTU',
    direccion: '0x0A',
    ultimaCalibracion: '2026-08-15',
    historialMuestras: [242.1, 243.8, 244.5, 245.8]
  },
  'pres-02': {
    id: 'pres-02',
    tag: 'PIEZO-TUBERIA-B',
    tipo: 'Transductor Piezorresistivo',
    rango: '0 a 16 bar',
    precision: '± 0.25% FS',
    bus: '4-20 mA Loop Alimentado',
    direccion: 'Canal Analógico AI-02',
    ultimaCalibracion: '2026-09-02',
    historialMuestras: [5.8, 6.0, 6.1, 6.2]
  }
};

export async function load({ params }) {
  const { id } = params;
  const sensor = BASE_DATOS_SENSORES[id];

  // Si el sensor no existe en la base de datos, abortamos con error 404
  if (!sensor) {
    error(404, {
      message: `El sensor '${id}' no existe o fue dado de baja en el sistema SCADA.`,
      codigo: 'ERR_SENSOR_INEXISTENTE',
      timestamp: new Date().toISOString()
    });
  }

  return {
    sensor
  };
}
