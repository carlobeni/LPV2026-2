/**
 * Función de carga en el servidor para la raíz de la sección.
 * Se ejecuta 100% en el servidor Node.js/Vite antes de enviar el HTML.
 */
export async function load({ url }) {
  // Simulación de consulta a base de datos o bus de telemetría industrial
  const sensoresBD = [
    { id: 'temp-01', tag: 'PT100-HORNO-1', tipo: 'temperatura', valor: 245.8, unidad: '°C', estado: 'NORMAL' },
    { id: 'pres-02', tag: 'PIEZO-TUBERIA-B', tipo: 'presion', valor: 6.2, unidad: 'bar', estado: 'ADVERTENCIA' },
    { id: 'fluj-03', tag: 'MAG-CAUDAL-ENTRADA', tipo: 'flujo', valor: 142.5, unidad: 'L/min', estado: 'NORMAL' },
    { id: 'vibr-04', tag: 'ACC-TURBINA-PPAL', tipo: 'vibracion', valor: 1.45, unidad: 'mm/s', estado: 'NORMAL' }
  ];

  // Filtro opcional por searchParams (?tipo=...)
  const tipoFiltro = url.searchParams.get('tipo');
  const sensoresFiltrados = tipoFiltro
    ? sensoresBD.filter(s => s.tipo.toLowerCase() === tipoFiltro.toLowerCase())
    : sensoresBD;

  return {
    sensores: sensoresFiltrados,
    totalDispositivos: sensoresBD.length,
    filtroActivo: tipoFiltro ?? 'todos',
    timestampServidor: new Date().toLocaleTimeString('es-PY')
  };
}
