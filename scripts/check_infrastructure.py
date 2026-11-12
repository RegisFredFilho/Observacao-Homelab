
import os
import sys

import requests
from dotenv import load_dotenv


def check_service(name, url, expected_status=200):
    """Verifica se um endpoint HTTP responde com o status esperado."""
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == expected_status:
            print(f"[OK] {name}: HTTP {response.status_code}")
            return True

        print(f"[CRITICAL] {name}: HTTP {response.status_code}")
        return False

    except requests.RequestException as error:
        print(f"[CRITICAL] {name}: {error}")
        return False


def main():
    load_dotenv()

    services = [
        ("Proxmox", "PROXMOX_URL", 401),
        ("Zabbix", "ZABBIX_URL", 200),
        ("Grafana", "GRAFANA_URL", 200),
    ]

    results = []

    for name, env_var, expected_status in services:
        url = os.getenv(env_var)

        if not url:
            print(f"[CRITICAL] {name}: {env_var} não configurada")
            results.append(False)
            continue

        results.append(check_service(name, url, expected_status))

    if all(results):
        print("\nTodos os serviços responderam corretamente.")
        return 0

    print("\nUm ou mais serviços apresentaram problemas.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
