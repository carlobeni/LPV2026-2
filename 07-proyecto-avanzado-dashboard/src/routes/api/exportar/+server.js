/**
 * Endpoint de exportación de auditoría y registros SCADA en CSV.
 */
export function GET() {
  const encabezado = 'Timestamp,Hora,Temperatura_C,Presion_bar,RPM_Turbina,Vibracion_mms,Potencia_kW,Estado';
  
  // Generar 20 muestras históricas de auditoría
  const filas = [encabezado];
  const ahora = Date.now();

  for (let i = 20; i >= 1; i--) {
    const t = new Date(ahora - i * 60000);
    const temp = (81.0 + Math.sin(i / 3) * 4.5).toFixed(2);
    const pres = (4.7 + Math.cos(i / 4) * 0.4).toFixed(2);
    const rpm = Math.round(1720 + Math.sin(i / 2) * 60);
    const vib = (1.12 + Math.random() * 0.1).toFixed(3);
    const kw = (88.4 + Math.random() * 3).toFixed(1);
    const estado = parseFloat(temp) > 85 ? 'ADVERTENCIA' : 'NORMAL';

    filas.push(`${t.toISOString()},${t.toLocaleTimeString('es-PY')},${temp},${pres},${rpm},${vib},${kw},${estado}`);
  }

  return new Response(filas.join('\r\n'), {
    status: 200,
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': `attachment; filename="auditoria_scada_${new Date().toISOString().slice(0, 10)}.csv"`
    }
  });
}
