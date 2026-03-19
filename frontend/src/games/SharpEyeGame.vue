<script setup>
import { computed, ref } from "vue";

const emit = defineEmits(["submit-score"]);

const TOTAL_ROUNDS = 8;

const phase = ref("idle");
const round = ref(0);
const score = ref(0);
const message = ref("Find the tile with the slightly different color.");

const cells = ref([]);
const targetIndex = ref(0);
const columns = ref(3);
const baseColor = ref("hsl(200 70% 52%)");
const oddColor = ref("hsl(200 70% 62%)");

const roundLabel = computed(() => `${Math.min(round.value, TOTAL_ROUNDS)}/${TOTAL_ROUNDS}`);

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function buildRound(nextRound) {
  // Round 1 → 6 cells, delta 28%; Round 8 → 25 cells, delta 8%.
  // Gradual ramp: every round adds ~3 cells and loses ~3 lightness points.
  const cellCount = Math.min(6 + (nextRound - 1) * 3, 25);
  columns.value = Math.min(5, Math.max(3, Math.round(Math.sqrt(cellCount))));
  cells.value = Array.from({ length: cellCount }, (_, index) => index);
  targetIndex.value = randomInt(0, cellCount - 1);

  const hue = randomInt(0, 359);
  const delta = Math.max(28 - (nextRound - 1) * 3, 8);
  const lightness = randomInt(40, 54);

  baseColor.value = `hsl(${hue} 72% ${lightness}%)`;
  oddColor.value = `hsl(${hue} 72% ${lightness + delta}%)`;
}

function startGame() {
  phase.value = "playing";
  round.value = 1;
  score.value = 0;
  message.value = "Round 1: tap the different tile.";
  buildRound(round.value);
}

function finishGame() {
  phase.value = "done";
  message.value = `Finished. Final score: ${score.value}`;
  emit("submit-score", score.value);
}

function handleTileClick(index) {
  if (phase.value !== "playing") return;

  if (index === targetIndex.value) {
    score.value += 20 + round.value * 3;
    if (round.value >= TOTAL_ROUNDS) {
      finishGame();
      return;
    }

    round.value += 1;
    message.value = `Great! Round ${round.value}: now it is harder.`;
    buildRound(round.value);
    return;
  }

  score.value = Math.max(score.value - 6, 0);
  message.value = "Not that one. Try again.";
}

function tileStyle(index) {
  return {
    background: index === targetIndex.value ? oddColor.value : baseColor.value
  };
}
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Agudeza Visual</h2>
      <p>Round: {{ roundLabel }} | Score: {{ score }}</p>
    </div>

    <div class="controls-row">
      <button @click="startGame">{{ phase === "playing" ? "Restart" : "Start" }}</button>
      <span>Find the odd color tile in each round</span>
    </div>

    <p class="sharp-eye-msg">{{ message }}</p>

    <div
      class="sharp-eye-grid"
      :style="{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }"
      aria-label="Agudeza visual game board"
    >
      <button
        v-for="index in cells"
        :key="index"
        class="sharp-eye-tile"
        :style="tileStyle(index)"
        :disabled="phase !== 'playing'"
        @click="handleTileClick(index)"
      />
    </div>
  </section>
</template>

<style scoped>
.sharp-eye-msg {
  margin: 0;
  font-weight: 600;
  color: #0f172a;
}

.sharp-eye-grid {
  width: min(94vw, 520px);
  display: grid;
  gap: 8px;
}

.sharp-eye-tile {
  border: 1px solid rgba(15, 23, 42, 0.25);
  border-radius: 8px;
  min-height: 46px;
  padding: 0;
}

.sharp-eye-tile:disabled {
  opacity: 0.65;
  cursor: default;
}

@media (max-width: 520px) {
  .sharp-eye-grid {
    gap: 6px;
  }

  .sharp-eye-tile {
    min-height: 42px;
  }
}
</style>
