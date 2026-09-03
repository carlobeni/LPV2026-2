"""
Suite de pruebas automatizadas para la API de Sensores y Telemetría.
"""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from src.app import app
from src.database import DatabaseManager, get_db


@pytest.fixture
def client_test(tmp_path: Path):
    """
    Fixture que proporciona un TestClient configurado con una base de datos SQLite aislada.
    """
    test_db_path = tmp_path / "test_api.db"
    test_db = DatabaseManager(test_db_path)

    # Sobreescribir dependencia de base de datos
    app.dependency_overrides[get_db] = lambda: test_db

    with TestClient(app) as client:
        yield client

    # Limpiar override
    app.dependency_overrides.clear()


def test_root_endpoint(client_test: TestClient):
    response = client_test.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "operativo"
    assert "/docs" in data["documentacion_swagger"]


def test_crear_sensor_exitoso(client_test: TestClient):
    payload = {
        "nombre": "Sensor Térmico Motor 1",
        "tipo": "temperatura",
        "ubicacion": "Banco de Pruebas A",
        "unidad": "°C",
        "umbral_alerta": 80.0
    }
    response = client_test.post("/sensores", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nombre"] == payload["nombre"]
    assert data["tipo"] == "temperatura"
    assert data["activo"] is True


def test_crear_sensor_validacion_pydantic_error(client_test: TestClient):
    # Payload con nombre vacío (debe fallar la validación de Pydantic con HTTP 422)
    payload = {
        "nombre": "   ",
        "tipo": "temperatura",
        "ubicacion": "Planta 1",
        "unidad": "°C",
        "umbral_alerta": 50.0
    }
    response = client_test.post("/sensores", json=payload)
    assert response.status_code == 422


def test_listar_y_filtrar_sensores(client_test: TestClient):
    # Registrar dos tipos distintos de sensores
    client_test.post("/sensores", json={
        "nombre": "Termocupla 1", "tipo": "temperatura", "ubicacion": "Horno", "unidad": "°C", "umbral_alerta": 100.0
    })
    client_test.post("/sensores", json={
        "nombre": "Transductor 1", "tipo": "presion", "ubicacion": "Tubería Principal", "unidad": "bar", "umbral_alerta": 10.0
    })

    # Listar todos
    resp_todos = client_test.get("/sensores")
    assert resp_todos.status_code == 200
    assert len(resp_todos.json()) == 2

    # Filtrar por tipo 'temperatura'
    resp_temp = client_test.get("/sensores?tipo=temperatura")
    assert resp_temp.status_code == 200
    sensores_temp = resp_temp.json()
    assert len(sensores_temp) == 1
    assert sensores_temp[0]["tipo"] == "temperatura"


def test_registrar_lecturas_y_alertas(client_test: TestClient):
    # 1. Crear sensor con umbral de 75.0 °C
    res_sensor = client_test.post("/sensores", json={
        "nombre": "Sensor Rodamiento", "tipo": "temperatura", "ubicacion": "Eje CNC", "unidad": "°C", "umbral_alerta": 75.0
    })
    sensor_id = res_sensor.json()["id"]

    # 2. Lectura normal (bajo umbral)
    res_l1 = client_test.post(f"/sensores/{sensor_id}/lecturas", json={"valor": 60.5})
    assert res_l1.status_code == 201
    assert res_l1.json()["alerta_activa"] is False

    # 3. Lectura anómala (sobre umbral)
    res_l2 = client_test.post(f"/sensores/{sensor_id}/lecturas", json={"valor": 88.2, "observacion": "Sobrecalentamiento"})
    assert res_l2.status_code == 201
    assert res_l2.json()["alerta_activa"] is True

    # 4. Consultar historial
    res_historial = client_test.get(f"/sensores/{sensor_id}/lecturas")
    assert res_historial.status_code == 200
    assert len(res_historial.json()) == 2

    # 5. Consultar resumen estadístico
    res_resumen = client_test.get(f"/sensores/{sensor_id}/resumen")
    assert res_resumen.status_code == 200
    resumen_data = res_resumen.json()
    assert resumen_data["total_lecturas"] == 2
    assert resumen_data["alertas_registradas"] == 1
    assert resumen_data["maximo_valor"] == 88.2
    assert resumen_data["minimo_valor"] == 60.5


def test_eliminar_sensor(client_test: TestClient):
    res_sensor = client_test.post("/sensores", json={
        "nombre": "Sensor a Borrar", "tipo": "corriente", "ubicacion": "Tablero", "unidad": "A", "umbral_alerta": 25.0
    })
    sensor_id = res_sensor.json()["id"]

    # Eliminar
    del_resp = client_test.delete(f"/sensores/{sensor_id}")
    assert del_resp.status_code == 204

    # Verificar que ya no existe
    get_resp = client_test.get(f"/sensores/{sensor_id}")
    assert get_resp.status_code == 404
