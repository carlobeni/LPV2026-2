/**
 * Endpoint para generación y descarga inmediata de archivo CSV.
 */
export function GET() {
  const lineas = [
    'Timestamp,ID,Tag,Variable,Valor,Unidad,Estado',
    '2026-10-15T18:00:00Z,S-01,PT100-HORNO-1,Temperatura,245.8,C,NORMAL',
    '2026-10-15T18:00:01Z,S-02,PIEZO-TUBERIA-B,Presion,6.2,bar,ADVERTENCIA',
    '2026-10-15T18:00:02Z,S-03,MAG-CAUDAL-ENTRADA,Flujo,142.5,L/min,NORMAL',
    '2026-10-15T18:00:03Z,S-04,ACC-TURBINA-PPAL,Vibracion,1.45,mm/s,NORMAL'
  ];

  const contenidoCSV = lineas.join('\r\n');

  return new Response(contenidoCSV, {
    status: 200,
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': 'attachment; filename="telemetria_lpv_fiuna.csv"'
    }
  });
}
