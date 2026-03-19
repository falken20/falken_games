<script setup>
import { computed, onMounted, ref, watch } from "vue";
import GuessNumberGame from "./games/GuessNumberGame.vue";
import MemoryGame from "./games/MemoryGame.vue";
import PongGame from "./games/PongGame.vue";
import ReflexGame from "./games/ReflexGame.vue";
import SharpEyeGame from "./games/SharpEyeGame.vue";
import SnakeGame from "./games/SnakeGame.vue";
import { fetchGames, fetchScores, saveScore } from "./services/api";

const componentMap = {
  snake: SnakeGame,
  pong: PongGame,
  memory: MemoryGame,
  "guess-number": GuessNumberGame,
  reflex: ReflexGame,
  "sharp-eye": SharpEyeGame
};

const fallbackGames = [
  {
    id: "snake",
    name: "Snake",
    description: "Move, eat and grow. Do not hit walls.",
    controls: "Arrow keys"
  },
  {
    id: "pong",
    name: "Pong Solo",
    description: "Keep the ball alive with your paddle.",
    controls: "Left/Right arrows"
  },
  {
    id: "memory",
    name: "Memoria",
    description: "Find all card pairs with few attempts.",
    controls: "Click"
  },
  {
    id: "guess-number",
    name: "Adivina el Numero",
    description: "Guess a number between 1 and 100.",
    controls: "Keyboard"
  },
  {
    id: "reflex",
    name: "Reflejos",
    description: "React quickly when the color turns green.",
    controls: "Click"
  },
  {
    id: "sharp-eye",
    name: "Agudeza Visual",
    description: "Find the tile with a slightly different color before each round gets harder.",
    controls: "Click/Tap"
  }
];

const games = ref([]);
const selectedGameId = ref(null);
const loadingGames = ref(true);
const loadingScores = ref(false);
const error = ref("");
const playerName = ref("Player1");
const scoreMessage = ref("");
const topScores = ref([]);

const activeGame = computed(() =>
  games.value.find((game) => game.id === selectedGameId.value) || null
);
const activeComponent = computed(() => componentMap[selectedGameId.value] || null);

async function loadGames() {
  loadingGames.value = true;
  error.value = "";
  try {
    games.value = await fetchGames();
  } catch {
    games.value = fallbackGames;
    error.value = "API not available. Running with local catalog.";
  } finally {
    loadingGames.value = false;
  }
}

async function loadScores() {
  if (!selectedGameId.value) return;
  loadingScores.value = true;
  try {
    topScores.value = await fetchScores(selectedGameId.value, 7);
  } catch {
    topScores.value = [];
  } finally {
    loadingScores.value = false;
  }
}

function selectGame(gameId) {
  selectedGameId.value = gameId;
  scoreMessage.value = "";
}

function backToMenu() {
  selectedGameId.value = null;
  scoreMessage.value = "";
}

async function onScoreSubmit(score) {
  if (!selectedGameId.value) return;
  const safeName = playerName.value.trim() || "Player";

  try {
    await saveScore(selectedGameId.value, safeName.slice(0, 24), score);
    scoreMessage.value = `Score saved: ${score}`;
    await loadScores();
  } catch {
    scoreMessage.value = `Score (local only): ${score}`;
  }
}

watch(selectedGameId, async (nextValue) => {
  if (!nextValue) {
    topScores.value = [];
    return;
  }
  await loadScores();
});

onMounted(loadGames);
</script>

<template>
  <main class="app-root">
    <header class="top-header">
      <h1>Falken Games</h1>
      <p>6 mini-games, single player, browser-based</p>
    </header>

    <section v-if="!selectedGameId" class="menu-view">
      <div class="player-form">
        <label for="playerName">Player name:</label>
        <input id="playerName" v-model="playerName" maxlength="24" />
      </div>

      <p v-if="loadingGames">Loading games...</p>
      <p v-else-if="error" class="warning">{{ error }}</p>

      <div class="game-menu">
        <article v-for="game in games" :key="game.id" class="game-card">
          <h2>{{ game.name }}</h2>
          <p>{{ game.description }}</p>
          <small>Controls: {{ game.controls }}</small>
          <button @click="selectGame(game.id)">Play</button>
        </article>
      </div>
    </section>

    <section v-else-if="activeGame" class="play-view">
      <div class="play-main">
        <div class="play-toolbar">
          <button class="ghost-btn" @click="backToMenu">Back to menu</button>
          <div>
            <h2>{{ activeGame.name }}</h2>
            <p>Controls: {{ activeGame.controls }}</p>
            <p class="mobile-hint">On mobile, use the on-screen controls when available.</p>
          </div>
        </div>

        <component
          :is="activeComponent"
          :key="selectedGameId"
          @submit-score="onScoreSubmit"
        />

        <p v-if="scoreMessage" class="score-msg">{{ scoreMessage }}</p>
      </div>

      <aside class="score-panel">
        <h3>Top Scores</h3>
        <p v-if="loadingScores">Loading...</p>
        <p v-else-if="!topScores.length">No scores yet.</p>
        <ol v-else>
          <li v-for="(entry, index) in topScores" :key="`${entry.player_name}-${index}`">
            <strong>{{ entry.player_name }}</strong>
            <span>{{ entry.score }}</span>
          </li>
        </ol>
      </aside>
    </section>
  </main>
</template>
