"""
Esquemas y modelos de datos implementados con Pydantic v2.
"""
from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class TipoSensor(str, Enum):
    TEMPERATURA = "temperatura"
    PRESION = "presion"
    VIBRACION = "vibracion"
    CORRIENTE = "corriente"
    FLUJO = "flujo"


class SensorBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre identificador del sensor en planta",
        examples=["Termocupla Horno 1"]
    )
    tipo: TipoSensor = Field(
        ...,
        description="Magnitud física censada"
    )
    ubicacion: str = Field(
        ...,
        min_length=2,
        max_length=60,
        description="Ubicación física de la máquina o estación",
        examples=["Brazo Robótico - Eje 2"]
    )
    unidad: str = Field(
        ...,
        min_length=1,
        max_length=15,
        description="Unidad métrica o técnica de medición",
        examples=["°C", "bar", "m/s²", "A"]
    )
    umbral_alerta: float = Field(
        ...,
        description="Valor límite que activa alerta de sobrecarga/sobretemperatura",
        examples=[85.0]
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v_strip = v.strip()
        if not v_strip:
            raise ValueError("El nombre del sensor no puede contener solo espacios en blanco")
        return v_strip


class SensorCreate(SensorBase):
    pass


class SensorResponse(SensorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID único autoincremental del sensor")
    activo: bool = Field(True, description="Estado operativo del sensor")
    creado_en: datetime = Field(..., description="Fecha y hora de registro")


class LecturaCreate(BaseModel):
    valor: float = Field(
        ...,
        description="Magnitud numérica leída por el convertidor ADC",
        examples=[76.4]
    )
    observacion: Optional[str] = Field(
        default=None,
        max_length=150,
        description="Notas operativas opcionales",
        examples=["Muestreo en régimen estacionario"]
    )


class LecturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    valor: float
    unidad: str
    alerta_activa: bool
    observacion: Optional[str]
    timestamp: datetime


class ResumenSensor(BaseModel):
    sensor: SensorResponse
    total_lecturas: int
    promedio_valor: Optional[float]
    minimo_valor: Optional[float]
    maximo_valor: Optional[float]
    alertas_registradas: int
