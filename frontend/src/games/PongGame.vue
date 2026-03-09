<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const emit = defineEmits(["submit-score"]);

const WIDTH = 520;
const HEIGHT = 320;
const PADDLE_WIDTH = 96;
const PADDLE_HEIGHT = 12;
const PADDLE_Y = HEIGHT - 28;
const BALL_RADIUS = 8;

const canvasRef = ref(null);
const score = ref(0);
const running = ref(false);
const gameOver = ref(false);

const keys = {
  left: false,
  right: false
};

let paddleX = (WIDTH - PADDLE_WIDTH) / 2;
let ballX = WIDTH / 2;
let ballY = HEIGHT / 2;
let velocityX = 3;
let velocityY = -3;
let timerId = null;

function draw() {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#0b1220";
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  ctx.fillStyle = "#334155";
  ctx.fillRect(0, 0, WIDTH, 14);

  ctx.fillStyle = "#22d3ee";
  ctx.fillRect(paddleX, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT);

  ctx.beginPath();
  ctx.fillStyle = "#f97316";
  ctx.arc(ballX, ballY, BALL_RADIUS, 0, Math.PI * 2);
  ctx.fill();
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function tick() {
  if (keys.left) paddleX -= 7;
  if (keys.right) paddleX += 7;
  paddleX = clamp(paddleX, 0, WIDTH - PADDLE_WIDTH);

  ballX += velocityX;
  ballY += velocityY;

  if (ballX <= BALL_RADIUS || ballX >= WIDTH - BALL_RADIUS) {
    velocityX *= -1;
    ballX = clamp(ballX, BALL_RADIUS, WIDTH - BALL_RADIUS);
  }

  if (ballY <= BALL_RADIUS + 14) {
    velocityY *= -1;
    ballY = BALL_RADIUS + 14;
  }

  const hitsPaddle =
    ballY + BALL_RADIUS >= PADDLE_Y &&
    ballY - BALL_RADIUS <= PADDLE_Y + PADDLE_HEIGHT &&
    ballX >= paddleX &&
    ballX <= paddleX + PADDLE_WIDTH &&
    velocityY > 0;

  if (hitsPaddle) {
    const hitOffset = (ballX - (paddleX + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2);
    velocityX += hitOffset * 1.2;
    velocityY = -Math.abs(velocityY) * 1.03;
    score.value += 1;
  }

  if (ballY - BALL_RADIUS > HEIGHT) {
    endGame();
    return;
  }

  draw();
}

function startGame() {
  paddleX = (WIDTH - PADDLE_WIDTH) / 2;
  ballX = WIDTH / 2;
  ballY = HEIGHT / 2;
  velocityX = Math.random() > 0.5 ? 3 : -3;
  velocityY = -3;

  score.value = 0;
  gameOver.value = false;
  running.value = true;

  if (timerId) clearInterval(timerId);
  timerId = setInterval(tick, 16);
  draw();
}

function endGame() {
  running.value = false;
  gameOver.value = true;
  if (timerId) {
    clearInterval(timerId);
    timerId = null;
  }
  emit("submit-score", score.value);
}

function handleKeydown(event) {
  if (event.key === "ArrowLeft") keys.left = true;
  if (event.key === "ArrowRight") keys.right = true;
}

function handleKeyup(event) {
  if (event.key === "ArrowLeft") keys.left = false;
  if (event.key === "ArrowRight") keys.right = false;
}

onMounted(() => {
  window.addEventListener("keydown", handleKeydown);
  window.addEventListener("keyup", handleKeyup);
  draw();
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKeydown);
  window.removeEventListener("keyup", handleKeyup);
  if (timerId) {
    clearInterval(timerId);
  }
});
</script>

<template>
  <section class="game-shell">
    <div class="game-header">
      <h2>Pong Solo</h2>
      <p>Hits: {{ score }}</p>
    </div>

    <div class="controls-row">
      <button @click="startGame">{{ running ? "Restart" : "Start" }}</button>
      <span>Move with Left / Right arrows</span>
    </div>

    <canvas ref="canvasRef" :width="WIDTH" :height="HEIGHT" class="pong-canvas" />

    <p v-if="gameOver" class="status-msg">Game over. Press Start to try again.</p>
  </section>
</template>

<style scoped>
.pong-canvas {
  width: min(94vw, 520px);
  border-radius: 10px;
  border: 2px solid #1f2937;
  background: #0b1220;
}

.status-msg {
  color: #b91c1c;
  font-weight: 600;
}
</style>
