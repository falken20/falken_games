<script setup>
import { computed, onBeforeUnmount, ref } from "vue";

const emit = defineEmits(["submit-score"]);

const TOTAL_ROUNDS = 3;

const phase = ref("idle");
const round = ref(0);
const times = ref([]);
const message = ref("Run 3 rounds and click as fast as possible.");
const completed = ref(false);

let timeoutId = null;
let startTime = 0;

const averageMs = computed(() => {
  if (!times.value.length) return 0;
  const sum = times.value.reduce((acc, value) => acc + value, 0);
  return Math.round(sum / times.value.length);
});

function clearReadyTimer() {
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
}

function scheduleReady() {
  phase.value = "waiting";
  message.value = `Round ${round.value}/${TOTAL_ROUNDS}: wait for green...`;
  const delay = 1200 + Math.random() * 2400;

  clearReadyTimer();
  timeoutId = setTimeout(() => {
    phase.value = "ready";
    startTime = performance.now();
    message.value = "Click now!";
  }, delay);
}

function scoreValue() {
  const raw = 350 - averageMs.value;
  return Math.max(raw, 10);
}

function start() {
  clearReadyTimer();
  round.value = 1;
  times.value = [];
  phase.value = "waiting";
  completed.value = false;
  message.value = "Get ready...";
  scheduleReady();
}

function handleAreaClick() {
  if (phase.value === "idle") return;

  if (phase.value === "waiting") {
    message.value = "Too early. Round is restarting...";
    phase.value = "penalty";
    clearReadyTimer();
    timeoutId = setTimeout(() => {
      scheduleReady();
    }, 900);
    return;
  }

  if (phase.value !== "ready") return;

  const reaction = Math.round(performance.now() - startTime);
  times.value = [...times.value, reaction];

  if (round.value >= TOTAL_ROUNDS) {
    completed.value = true;
    phase.value = "done";
    message.value = `Finished. Avg reaction: ${averageMs.value} ms.`;
    emit("submit-score", scoreValue());
    return;
  }

  round.value += 1;
  phase.value = "pause";
  message.value = `Round ${round.value - 1} time: ${reaction} ms`;
  timeoutId = setTimeout(() => {
    scheduleReady();
  }, 800);
}

onBeforeUnmount(() => {
  clearReadyTimer();
});
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Reflejos</h2>
      <p>Round: {{ round || 0 }}/{{ TOTAL_ROUNDS }}</p>
    </div>

    <div class="controls-row">
      <button @click="start">{{ phase === "idle" || completed ? "Start" : "Restart" }}</button>
      <span v-if="times.length">Avg: {{ averageMs }} ms</span>
    </div>

    <button class="reaction-area" :class="phase" @click="handleAreaClick">
      {{ message }}
    </button>

    <ul class="times-list" v-if="times.length">
      <li v-for="(time, index) in times" :key="index">Round {{ index + 1 }}: {{ time }} ms</li>
    </ul>
  </section>
</template>

<style scoped>
.reaction-area {
  width: min(94vw, 520px);
  min-height: 180px;
  border: none;
  border-radius: 12px;
  color: #f8fafc;
  font-size: 1.1rem;
  font-weight: 700;
  padding: 22px;
  cursor: pointer;
  background: #334155;
}

.reaction-area.waiting,
.reaction-area.penalty,
.reaction-area.pause {
  background: #dc2626;
}

.reaction-area.ready {
  background: #16a34a;
}

.reaction-area.done {
  background: #0f766e;
}

.times-list {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 0;
  margin: 0;
  list-style: none;
}
</style>
