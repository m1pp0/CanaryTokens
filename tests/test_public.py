def test_trigger_token_creates_event(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    token = client.post("/tokens", json={"label": "Приманка"}, headers=headers).json()

    response = client.get(f"/t/{token['uuid']}")
    assert response.status_code == 200
    assert "Документ недоступен" in response.text

    events = client.get("/events", headers=headers).json()
    assert events["total"] == 1
    assert events["items"][0]["token_id"] == token["id"]


def test_trigger_unknown_uuid(client):
    response = client.get("/t/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404