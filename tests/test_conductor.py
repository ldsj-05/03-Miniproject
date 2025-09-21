import pathlib
import sys

# Ensure src/ is on the path
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import conductor  # type: ignore


def test_play_note_posts_to_all_devices(requests_mock, monkeypatch):
    test_ips = ["127.0.0.1", "192.0.2.10"]
    monkeypatch.setattr(conductor, "PICO_IPS", test_ips, raising=True)

    # Mock POST endpoints for each device
    for ip in test_ips:
        requests_mock.post(f"http://{ip}/tone", status_code=204)

    # Call
    conductor.play_note_on_all_picos(440, 250)

    # Verify all mocked endpoints were hit
    for ip in test_ips:
        history = [h for h in requests_mock.request_history if h.url == f"http://{ip}/tone"]
        assert history, f"Expected POST to http://{ip}/tone"
        # Verify payload
        assert history[0].json() == {"freq": 440, "ms": 250, "duty": 0.5}


def test_play_note_handles_errors_gracefully(requests_mock, monkeypatch):
    # One IP works, one times out/connection error
    test_ips = ["127.0.0.1", "192.0.2.99"]
    monkeypatch.setattr(conductor, "PICO_IPS", test_ips, raising=True)

    requests_mock.post("http://127.0.0.1/tone", status_code=204)
    requests_mock.post("http://192.0.2.99/tone", exc=Exception("boom"))

    # Should not raise
    conductor.play_note_on_all_picos(262, 100) 