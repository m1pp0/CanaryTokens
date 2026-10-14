def test_list_events_empty(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/events", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_list_events_filter_by_token(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    t1 = client.post("/tokens", json={"label": "Первый"}, headers=headers).json()
    t2 = client.post("/tokens", json={"label": "Второй"}, headers=headers).json()

    client.get(f"/t/{t1['uuid']}")
    client.get(f"/t/{t1['uuid']}")
    client.get(f"/t/{t2['uuid']}")

    all_events = client.get("/events", headers=headers).json()
    assert all_events["total"] == 3

    filtered = client.get(f"/events?token_id={t1['id']}", headers=headers).json()
    assert filtered["total"] == 2
    for item in filtered["items"]:
        assert item["token_id"] == t1["id"]


def test_get_event(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    token = client.post("/tokens", json={"label": "Тест"}, headers=headers).json()
    client.get(f"/t/{token['uuid']}")

    events = client.get("/events", headers=headers).json()
    event_id = events["items"][0]["id"]

    response = client.get(f"/events/{event_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["ip"] is not None
    assert data["token_id"] == token["id"]


def test_event_isolation(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    token = client.post("/tokens", json={"label": "Мой"}, headers=headers).json()
    client.get(f"/t/{token['uuid']}")

    other = client.post(
        "/auth/register",
        json={"email": "other@example.com", "password": "secret123"},
    )
    login = client.post(
        "/auth/login",
        data={"username": "other@example.com", "password": "secret123"},
    ).json()
    other_headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = client.get("/events", headers=other_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 0