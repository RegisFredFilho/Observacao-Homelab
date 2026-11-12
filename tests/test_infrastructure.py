
from unittest.mock import Mock, patch

import requests

from scripts.check_infrastructure import check_service, main


def test_service_online():
    """Deve retornar True quando recebe HTTP 200."""
    response = Mock()
    response.status_code = 200

    with patch("scripts.check_infrastructure.requests.get",
               return_value=response) as mock_get:
        result = check_service(
            "Grafana",
            "http://localhost:3000/api/health"
        )

    assert result is True
    mock_get.assert_called_once_with(
        "http://localhost:3000/api/health",
        timeout=5
    )


def test_unexpected_http_status():
    """Deve retornar False para um status inesperado."""
    response = Mock()
    response.status_code = 503

    with patch("scripts.check_infrastructure.requests.get",
               return_value=response):
        result = check_service(
            "Zabbix",
            "http://localhost/zabbix/"
        )

    assert result is False


def test_connection_timeout():
    """Deve detectar um serviço que não responde."""
    with patch(
        "scripts.check_infrastructure.requests.get",
        side_effect=requests.exceptions.Timeout("Timeout")
    ):
        result = check_service(
            "Grafana",
            "http://localhost:3000"
        )

    assert result is False


def test_proxmox_http_401():
    """Deve aceitar HTTP 401 no endpoint protegido."""
    response = Mock()
    response.status_code = 401

    with patch("scripts.check_infrastructure.requests.get",
               return_value=response):
        result = check_service(
            "Proxmox",
            "https://localhost:8006/api2/json/version",
            expected_status=401
        )

    assert result is True


def test_missing_configuration(monkeypatch):
    """Deve falhar quando não há URLs configuradas."""
    for key in ("PROXMOX_URL", "ZABBIX_URL", "GRAFANA_URL"):
        monkeypatch.delenv(key, raising=False)

    with patch("scripts.check_infrastructure.load_dotenv"):
        result = main()

    assert result == 1
