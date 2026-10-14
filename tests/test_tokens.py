def test_create_token(client, auth_token):
    response = client.post(
        "/tokens",
        json={"label": "Договор №1", "memo": "Приманка"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["label"] == "Договор №1"
    assert data["memo"] == "Приманка"
    assert "uuid" in data
    assert "url" in data
    assert data["url"].endswith(data["uuid"])


def test_list_tokens(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/tokens", json={"label": "Первый"}, headers=headers)
    client.post("/tokens", json={"label": "Второй"}, headers=headers)

    response = client.get("/tokens", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_own_token(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    created = client.post("/tokens", json={"label": "Мой"}, headers=headers).json()

    response = client.get(f"/tokens/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["label"] == "Мой"


def test_delete_token(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    created = client.post("/tokens", json={"label": "Удалить"}, headers=headers).json()

    response = client.delete(f"/tokens/{created['id']}", headers=headers)
    assert response.status_code == 204

    after = client.get(f"/tokens/{created['id']}", headers=headers)
    assert after.status_code == 404