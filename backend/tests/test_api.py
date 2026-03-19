def test_health_returns_ok(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_games_returns_expected_catalog(client) -> None:
    response = client.get("/api/games")

    assert response.status_code == 200
    game_ids = {item["id"] for item in response.json()}
    assert game_ids == {"snake", "pong", "memory", "guess-number", "reflex", "sharp-eye"}


def test_get_scores_with_invalid_game_returns_404(client) -> None:
    response = client.get("/api/scores/invalid-game")

    assert response.status_code == 404
    assert response.json() == {"detail": "Juego no encontrado"}


def test_save_score_trims_player_name(client) -> None:
    response = client.post(
        "/api/scores",
        json={"game_id": "snake", "player_name": "  Alice  ", "score": 120},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["player_name"] == "Alice"
    assert payload["score"] == 120
    assert payload["timestamp"].endswith("Z")


def test_save_score_with_whitespace_name_returns_422(client) -> None:
    response = client.post(
        "/api/scores",
        json={"game_id": "snake", "player_name": "   ", "score": 77},
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "Nombre de jugador invalido"}


def test_save_score_with_invalid_game_returns_404(client) -> None:
    response = client.post(
        "/api/scores",
        json={"game_id": "invalid-game", "player_name": "Alice", "score": 5},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Juego no encontrado"}


def test_scores_endpoint_returns_sorted_and_limited_results(client) -> None:
    client.post("/api/scores", json={"game_id": "snake", "player_name": "P1", "score": 7})
    client.post("/api/scores", json={"game_id": "snake", "player_name": "P2", "score": 42})
    client.post("/api/scores", json={"game_id": "snake", "player_name": "P3", "score": 19})

    response = client.get("/api/scores/snake?limit=2")

    assert response.status_code == 200
    payload = response.json()
    assert [item["player_name"] for item in payload] == ["P2", "P3"]
    assert [item["score"] for item in payload] == [42, 19]
