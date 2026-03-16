def test_create_hero(client):
    response = client.post(
        "/api/v7/database/heroes/",
        json={
            "name": "Spiderman",
            "age": 25,
            "secret_name": "some",
            "active": True,
            "team_id": 1,
        },
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Spiderman"
    assert data["age"] == 25
    assert "id" in data
