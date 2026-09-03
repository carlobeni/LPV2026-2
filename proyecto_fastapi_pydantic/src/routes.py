"""
Rutas y endpoints REST para la gestión de sensores y telemetría.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.database import DatabaseManager, get_db
from src.models import (
    SensorCreate,
    SensorResponse,
    LecturaCreate,
    LecturaResponse,
    ResumenSensor,
    TipoSensor
)

router = APIRouter(prefix="/sensores", tags=["Sensores & Telemetría"])


@router.get(
    "",
    response_model=List[SensorResponse],
    summary="Listar todos los sensores registrados",
    description="Permite filtrar sensores por tipo físico (temperatura, presión, etc.) y por estado activo."
)
def listar_sensores(
    tipo: Optional[TipoSensor] = Query(None, description="Filtrar por tipo de magnitud física"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado operativo"),
    db: DatabaseManager = Depends(get_db)
):
    tipo_str = tipo.value if tipo else None
    return db.obtener_sensores(tipo=tipo_str, activo=activo)


@router.post(
    "",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dar de alta un nuevo sensor mecatrónico",
    description="Registra un sensor en el sistema validando sus datos mediante Pydantic v2."
)
def crear_sensor(
    sensor_in: SensorCreate,
    db: DatabaseManager = Depends(get_db)
):
    sensor = db.crear_sensor(sensor_in)
    return sensor


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    summary="Consultar detalle de un sensor",
    description="Obtiene las especificaciones de un sensor a partir de su ID único."
)
def obtener_sensor(
    sensor_id: int,
    db: DatabaseManager = Depends(get_db)
):
    sensor = db.obtener_sensor(sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El sensor con ID {sensor_id} no existe en el sistema."
        )
    return sensor


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un sensor mecatrónico",
    description="Elimina el sensor y todas sus lecturas históricas asociadas."
)
def eliminar_sensor(
    sensor_id: int,
    db: DatabaseManager = Depends(get_db)
):
    exito = db.eliminar_sensor(sensor_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se pudo eliminar: sensor con ID {sensor_id} no encontrado."
        )
    return None


@router.post(
    "/{sensor_id}/lecturas",
    response_model=LecturaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva lectura física",
    description="Almacena una medición y evalúa automáticamente si sobrepasa el umbral de alerta."
)
def registrar_lectura(
    sensor_id: int,
    lectura_in: LecturaCreate,
    db: DatabaseManager = Depends(get_db)
):
    lectura = db.registrar_lectura(sensor_id, lectura_in)
    if not lectura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede registrar lectura: el sensor {sensor_id} no existe o está inactivo."
        )
    return lectura


@router.get(
    "/{sensor_id}/lecturas",
    response_model=List[LecturaResponse],
    summary="Obtener historial de lecturas de un sensor",
    description="Retorna las lecturas más recientes ordenadas cronológicamente."
)
def listar_lecturas(
    sensor_id: int,
    limit: int = Query(50, ge=1, le=500, description="Cantidad máxima de lecturas a retornar"),
    db: DatabaseManager = Depends(get_db)
):
    sensor = db.obtener_sensor(sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado."
        )
    return db.obtener_lecturas(sensor_id, limit=limit)


@router.get(
    "/{sensor_id}/resumen",
    response_model=ResumenSensor,
    summary="Resumen estadístico de un sensor",
    description="Calcula cantidad de lecturas, promedio, mínimo, máximo y número de alertas disparadas."
)
def obtener_resumen_sensor(
    sensor_id: int,
    db: DatabaseManager = Depends(get_db)
):
    resumen = db.obtener_resumen(sensor_id)
    if not resumen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado."
        )
    return resumen
