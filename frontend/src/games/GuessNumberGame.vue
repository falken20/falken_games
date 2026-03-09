<script setup>
import { ref } from "vue";

const emit = defineEmits(["submit-score"]);

const guess = ref("");
const attempts = ref(0);
const secret = ref(0);
const message = ref("Try to guess a number between 1 and 100.");
const finished = ref(false);

function newSecret() {
  return Math.floor(Math.random() * 100) + 1;
}

function scoreValue() {
  const raw = 120 - attempts.value * 12;
  return Math.max(raw, 10);
}

function restart() {
  secret.value = newSecret();
  guess.value = "";
  attempts.value = 0;
  message.value = "Try to guess a number between 1 and 100.";
  finished.value = false;
}

function submitGuess() {
  if (finished.value) return;
  const value = Number.parseInt(guess.value, 10);
  if (Number.isNaN(value) || value < 1 || value > 100) {
    message.value = "Enter a valid integer from 1 to 100.";
    return;
  }

  attempts.value += 1;

  if (value < secret.value) {
    message.value = "Too low.";
  } else if (value > secret.value) {
    message.value = "Too high.";
  } else {
    finished.value = true;
    message.value = `Correct! Secret number: ${secret.value}.`;
    emit("submit-score", scoreValue());
  }

  guess.value = "";
}

restart();
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Adivina el Numero</h2>
      <p>Attempts: {{ attempts }}</p>
    </div>

    <div class="guess-input-row">
      <input
        v-model="guess"
        type="number"
        min="1"
        max="100"
        placeholder="1-100"
        @keyup.enter="submitGuess"
      />
      <button @click="submitGuess">Try</button>
      <button @click="restart">Reset</button>
    </div>

    <p class="guess-message">{{ message }}</p>
  </section>
</template>

<style scoped>
.guess-input-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

input {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #94a3b8;
  width: 140px;
  font-size: 1rem;
}

.guess-message {
  font-weight: 600;
  color: #0f172a;
}
</style>
