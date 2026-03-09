<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const emit = defineEmits(["submit-score"]);

const GRID_SIZE = 15;
const SPEED_MS = 130;

const snake = ref([]);
const direction = ref("right");
const nextDirection = ref("right");
const food = ref({ x: 5, y: 5 });
const running = ref(false);
const gameOver = ref(false);
const score = ref(0);

let timerId = null;

const cells = computed(() =>
  Array.from({ length: GRID_SIZE * GRID_SIZE }, (_, index) => ({
    x: index % GRID_SIZE,
    y: Math.floor(index / GRID_SIZE)
  }))
);

function randomFood(currentSnake) {
  while (true) {
    const candidate = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE)
    };
    const occupied = currentSnake.some(
      (part) => part.x === candidate.x && part.y === candidate.y
    );
    if (!occupied) {
      return candidate;
    }
  }
}

function isOpposite(dirA, dirB) {
  return (
    (dirA === "up" && dirB === "down") ||
    (dirA === "down" && dirB === "up") ||
    (dirA === "left" && dirB === "right") ||
    (dirA === "right" && dirB === "left")
  );
}

function moveHead(head, dir) {
  if (dir === "up") return { x: head.x, y: head.y - 1 };
  if (dir === "down") return { x: head.x, y: head.y + 1 };
  if (dir === "left") return { x: head.x - 1, y: head.y };
  return { x: head.x + 1, y: head.y };
}

function tick() {
  direction.value = nextDirection.value;
  const current = snake.value;
  const head = current[0];
  const newHead = moveHead(head, direction.value);

  const outOfBounds =
    newHead.x < 0 ||
    newHead.x >= GRID_SIZE ||
    newHead.y < 0 ||
    newHead.y >= GRID_SIZE;

  const hitsSelf = current.some(
    (part) => part.x === newHead.x && part.y === newHead.y
  );

  if (outOfBounds || hitsSelf) {
    stopGame();
    return;
  }

  const nextSnake = [newHead, ...current];
  const ateFood = newHead.x === food.value.x && newHead.y === food.value.y;

  if (ateFood) {
    score.value += 10;
    food.value = randomFood(nextSnake);
  } else {
    nextSnake.pop();
  }

  snake.value = nextSnake;
}

function startGame() {
  snake.value = [
    { x: 7, y: 7 },
    { x: 6, y: 7 },
    { x: 5, y: 7 }
  ];
  direction.value = "right";
  nextDirection.value = "right";
  score.value = 0;
  gameOver.value = false;
  running.value = true;
  food.value = randomFood(snake.value);

  if (timerId) clearInterval(timerId);
  timerId = setInterval(tick, SPEED_MS);
}

function stopGame() {
  running.value = false;
  gameOver.value = true;
  if (timerId) {
    clearInterval(timerId);
    timerId = null;
  }
  emit("submit-score", score.value);
}

function handleKeydown(event) {
  const keyMap = {
    ArrowUp: "up",
    ArrowDown: "down",
    ArrowLeft: "left",
    ArrowRight: "right"
  };
  const mapped = keyMap[event.key];
  if (!mapped || !running.value) return;
  if (isOpposite(mapped, direction.value)) return;
  nextDirection.value = mapped;
}

function cellClass(cell) {
  if (food.value.x === cell.x && food.value.y === cell.y) {
    return "food";
  }
  const index = snake.value.findIndex(
    (part) => part.x === cell.x && part.y === cell.y
  );
  if (index === 0) return "head";
  if (index > 0) return "body";
  return "empty";
}

onMounted(() => {
  window.addEventListener("keydown", handleKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKeydown);
  if (timerId) {
    clearInterval(timerId);
  }
});
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Snake</h2>
      <p>Score: {{ score }}</p>
    </div>

    <div class="controls-row">
      <button @click="startGame">{{ running ? "Restart" : "Start" }}</button>
      <span>Use arrow keys</span>
    </div>

    <div class="snake-grid">
      <div
        v-for="cell in cells"
        :key="`${cell.x}-${cell.y}`"
        class="snake-cell"
        :class="cellClass(cell)"
      />
    </div>

    <p v-if="gameOver" class="status-msg">Game over. Press Start to play again.</p>
  </section>
</template>

<style scoped>
.snake-grid {
  width: min(92vw, 420px);
  aspect-ratio: 1 / 1;
  display: grid;
  grid-template-columns: repeat(15, 1fr);
  gap: 2px;
  background: #0f172a;
  padding: 6px;
  border-radius: 10px;
}

.snake-cell {
  border-radius: 3px;
  background: #1e293b;
}

.snake-cell.food {
  background: #f97316;
}

.snake-cell.head {
  background: #22c55e;
}

.snake-cell.body {
  background: #16a34a;
}

.status-msg {
  color: #b91c1c;
  font-weight: 600;
}
</style>
