<script setup>
import { computed, ref } from "vue";

const emit = defineEmits(["submit-score"]);

const CARD_VALUES = ["A", "B", "C", "D", "E", "F"];

const cards = ref([]);
const firstCardId = ref(null);
const secondCardId = ref(null);
const lockBoard = ref(false);
const attempts = ref(0);
const finished = ref(false);

const matches = computed(
  () => cards.value.filter((card) => card.matched).length / 2
);

function shuffle(array) {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function buildDeck() {
  const doubled = [...CARD_VALUES, ...CARD_VALUES];
  return shuffle(doubled).map((value, index) => ({
    id: index + 1,
    value,
    flipped: false,
    matched: false
  }));
}

function restart() {
  cards.value = buildDeck();
  firstCardId.value = null;
  secondCardId.value = null;
  lockBoard.value = false;
  attempts.value = 0;
  finished.value = false;
}

function scoreValue() {
  const raw = 140 - attempts.value * 9;
  return Math.max(raw, 10);
}

function revealCard(cardId) {
  if (lockBoard.value || finished.value) return;

  const target = cards.value.find((card) => card.id === cardId);
  if (!target || target.flipped || target.matched) return;

  target.flipped = true;

  if (firstCardId.value === null) {
    firstCardId.value = cardId;
    return;
  }

  secondCardId.value = cardId;
  attempts.value += 1;
  lockBoard.value = true;

  const first = cards.value.find((card) => card.id === firstCardId.value);
  const second = cards.value.find((card) => card.id === secondCardId.value);

  if (first.value === second.value) {
    first.matched = true;
    second.matched = true;
    firstCardId.value = null;
    secondCardId.value = null;
    lockBoard.value = false;

    if (cards.value.every((card) => card.matched)) {
      finished.value = true;
      emit("submit-score", scoreValue());
    }
    return;
  }

  window.setTimeout(() => {
    first.flipped = false;
    second.flipped = false;
    firstCardId.value = null;
    secondCardId.value = null;
    lockBoard.value = false;
  }, 700);
}

restart();
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Memoria</h2>
      <p>Attempts: {{ attempts }} | Pairs: {{ matches }}/6</p>
    </div>

    <div class="controls-row">
      <button @click="restart">Restart</button>
      <span>Find all matching pairs</span>
    </div>

    <div class="memory-grid">
      <button
        v-for="card in cards"
        :key="card.id"
        class="memory-card"
        :class="{ flipped: card.flipped || card.matched, matched: card.matched }"
        @click="revealCard(card.id)"
      >
        <span v-if="card.flipped || card.matched">{{ card.value }}</span>
        <span v-else>?</span>
      </button>
    </div>

    <p v-if="finished" class="status-msg">Level complete. Score submitted.</p>
  </section>
</template>

<style scoped>
.memory-grid {
  width: min(94vw, 520px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.memory-card {
  aspect-ratio: 3 / 4;
  border: none;
  border-radius: 10px;
  background: #1e293b;
  color: #f8fafc;
  font-size: 1.6rem;
  font-weight: 700;
  cursor: pointer;
}

.memory-card.flipped {
  background: #0ea5e9;
}

.memory-card.matched {
  background: #16a34a;
}

.status-msg {
  color: #166534;
  font-weight: 600;
}

@media (max-width: 520px) {
  .memory-grid {
    gap: 8px;
  }

  .memory-card {
    font-size: 1.25rem;
  }
}
</style>
