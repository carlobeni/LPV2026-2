import { json } from '@sveltejs/kit';

export async function GET({ params }) {
  const { id } = params;

  return json({
    id,
    tag: `SENSOR-CANAL-${id}`,
    estadoBus: 'SINCRONIZADO',
    tiempoRespuestaMs: 12
  });
}

export async function DELETE({ params }) {
  const { id } = params;
  console.log(`Petición DELETE recibida para desasociar canal ${id}`);

  // En APIs REST bien diseñadas, un DELETE exitoso sin contenido devuelve 204
  return new Response(null, { status: 204 });
}
