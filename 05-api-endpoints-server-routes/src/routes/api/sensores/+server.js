import { json } from '@sveltejs/kit';

let registrosAPI = [
  { id: '1', tag: 'PT100-INTERCAMBIADOR', valor: 85.3, unidad: '°C' },
  { id: '2', tag: 'TRANSD-PRESION-LINEA', valor: 5.12, unidad: 'bar' },
  { id: '3', tag: 'CAUDALIMETRO-INYECCION', valor: 34.2, unidad: 'L/min' }
];

export async function GET({ url }) {
  const filtro = url.searchParams.get('q');
  
  let resultado = registrosAPI;
  if (filtro) {
    resultado = registrosAPI.filter(r => 
      r.tag.toLowerCase().includes(filtro.toLowerCase())
    );
  }

  return json({
    total: resultado.length,
    sensores: resultado
  }, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*'
    }
  });
}

export async function POST({ request }) {
  try {
    const cuerpo = await request.json();

    if (!cuerpo.tag || typeof cuerpo.valor !== 'number') {
      return json({
        error: 'El cuerpo debe incluir un "tag" (string) y un "valor" (numérico).'
      }, { status: 400 });
    }

    const nuevoItem = {
      id: String(registrosAPI.length + 1),
      tag: cuerpo.tag.toUpperCase(),
      valor: cuerpo.valor,
      unidad: cuerpo.unidad || 'u'
    };

    registrosAPI.push(nuevoItem);

    return json(nuevoItem, { status: 201 });
  } catch {
    return json({ error: 'Cuerpo de petición JSON inválido.' }, { status: 400 });
  }
}
