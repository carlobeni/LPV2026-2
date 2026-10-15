/**
 * Endpoint de Telemetría Continua por Server-Sent Events (SSE)
 * Emite paquetes a 1 Hz con variables físicas industriales y fluctuaciones estocásticas realistas.
 */
export function GET() {
  /** @type {any} */
  let timerId = null;

  // Variables de estado del proceso físico
  let baseTemp = 82.5;
  let basePresion = 4.8;
  let baseRPM = 1750;
  let baseVibracion = 1.15;

  const stream = new ReadableStream({
    start(controller) {
      const emitirTrama = () => {
        // Generación de pequeñas perturbaciones de proceso y ruido gaussiano
        const deltaTemp = (Math.random() - 0.48) * 0.8;
        const deltaPres = (Math.random() - 0.49) * 0.15;
        const deltaRPM = Math.floor((Math.random() - 0.5) * 35);
        const deltaVib = (Math.random() - 0.5) * 0.08;

        baseTemp = Math.max(50, Math.min(120, baseTemp + deltaTemp));
        basePresion = Math.max(1, Math.min(10, basePresion + deltaPres));
        baseRPM = Math.max(1200, Math.min(2200, baseRPM + deltaRPM));
        baseVibracion = Math.max(0.1, Math.min(5.0, baseVibracion + deltaVib));

        const paquete = {
          timestamp: new Date().toISOString(),
          horaFormato: new Date().toLocaleTimeString('es-PY'),
          temperatura: Number(baseTemp.toFixed(2)),
          presion: Number(basePresion.toFixed(2)),
          rpm: Math.round(baseRPM),
          vibracion: Number(baseVibracion.toFixed(3)),
          potenciaKW: Number(((baseRPM * 0.045) + (basePresion * 3.2)).toFixed(1)),
          estadoGlobal: baseTemp > 95 || basePresion > 6.5 ? 'ALERTA' : 'NORMAL'
        };

        const evento = `data: ${JSON.stringify(paquete)}\n\n`;
        controller.enqueue(new TextEncoder().encode(evento));
      };

      // Emitir primer dato inmediatamente
      emitirTrama();
      // Y luego cada 1000ms
      timerId = setInterval(emitirTrama, 1000);
    },
    cancel() {
      if (timerId) clearInterval(timerId);
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no'
    }
  });
}
