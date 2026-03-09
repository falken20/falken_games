const API_BASE = import.meta.env.VITE_API_URL || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "API request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function fetchGames() {
  return request("/api/games");
}

export function fetchScores(gameId, limit = 10) {
  return request(`/api/scores/${gameId}?limit=${limit}`);
}

export function saveScore(gameId, playerName, score) {
  return request("/api/scores", {
    method: "POST",
    body: JSON.stringify({ game_id: gameId, player_name: playerName, score })
  });
}
