/**
 * Endpoint de transmisión Server-Sent Events (SSE).
 * Envía paquetes de telemetría continuos al cliente cada 1 segundo.
 */
export function GET() {
  let timer;

  const stream = new ReadableStream({
    start(controller) {
      timer = setInterval(() => {
        const payload = {
          temperatura: Number((75 + Math.random() * 8).toFixed(1)),
          presion: Number((4.2 + Math.random() * 0.6).toFixed(2)),
          rpm: Math.floor(1450 + Math.random() * 80),
          timestamp: new Date().toLocaleTimeString('es-PY')
        };

        const eventoSSE = `data: ${JSON.stringify(payload)}\n\n`;
        controller.enqueue(new TextEncoder().encode(eventoSSE));
      }, 1000);
    },
    cancel() {
      if (timer) clearInterval(timer);
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}
