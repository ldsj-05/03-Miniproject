import pathlib
import sys

# Ensure src/ is on the path
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import requests
import dashboard  # type: ignore


def test_get_device_status_success(requests_mock):
    ip = "127.0.0.1"
    requests_mock.get(f"http://{ip}/health", json={"ip": ip, "device_id": "SIM-1", "status": "ok"})
    requests_mock.get(f"http://{ip}/sensor", json={"norm": 0.75})

    status = dashboard.get_device_status(ip)

    assert status["ip"] == ip
    assert status["device_id"] == "SIM-1"
    assert status["status"] == "ok"
    assert status["norm"] == 0.75


def test_get_device_status_offline(requests_mock):
    ip = "192.0.2.5"  # TEST-NET-1
    requests_mock.get(f"http://{ip}/health", exc=requests.exceptions.ConnectTimeout)

    status = dashboard.get_device_status(ip)

    assert status["ip"] == ip
    assert status["status"].startswith("Offline")
    # norm remains default when offline
    assert status["norm"] == 0.0 