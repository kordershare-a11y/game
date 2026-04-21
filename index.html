const canvas = document.getElementById("game");
const context = canvas.getContext("2d");
const scoreElement = document.getElementById("score");
const highScoreElement = document.getElementById("high-score");
const statusElement = document.getElementById("status");
const startButton = document.getElementById("start-button");
const restartButton = document.getElementById("restart-button");

const gameState = {
  running: false,
  gameOver: false,
  score: 0,
  highScore: Number.parseInt(localStorage.getItem("neon-dodge-high-score") || "0", 10),
  lastFrameTime: 0,
  spawnTimer: 0,
  spawnInterval: 0.85,
  speedScale: 1,
  backgroundOffset: 0,
  player: {
    width: 72,
    height: 20,
    x: canvas.width / 2 - 36,
    y: canvas.height - 60,
    speed: 340,
    color: "#6cf8ff"
  },
  hazards: [],
  keys: {
    left: false,
    right: false
  }
};

highScoreElement.textContent = String(gameState.highScore);

function setStatus(text) {
  statusElement.textContent = text;
}

function saveHighScore() {
  localStorage.setItem("neon-dodge-high-score", String(gameState.highScore));
}

function resetPlayer() {
  gameState.player.x = canvas.width / 2 - gameState.player.width / 2;
}

function resetGame() {
  gameState.running = false;
  gameState.gameOver = false;
  gameState.score = 0;
  gameState.lastFrameTime = 0;
  gameState.spawnTimer = 0;
  gameState.spawnInterval = 0.85;
  gameState.speedScale = 1;
  gameState.backgroundOffset = 0;
  gameState.hazards = [];
  resetPlayer();
  scoreElement.textContent = "0";
  setStatus("Ready");
}

function startGame() {
  resetGame();
  gameState.running = true;
  setStatus("Running");
  requestAnimationFrame(gameLoop);
}

function endGame() {
  gameState.running = false;
  gameState.gameOver = true;
  setStatus("Crashed");
}

function createHazard() {
  const width = 50 + Math.random() * 70;
  const height = 16 + Math.random() * 20;
  const x = Math.random() * (canvas.width - width);
  const speed = 180 + Math.random() * 120 + gameState.speedScale * 45;

  gameState.hazards.push({
    x,
    y: -height,
    width,
    height,
    speed,
    hue: Math.floor(Math.random() * 120) + 300
  });
}

function updatePlayer(deltaTime) {
  const direction = (gameState.keys.right ? 1 : 0) - (gameState.keys.left ? 1 : 0);
  gameState.player.x += direction * gameState.player.speed * deltaTime;
  gameState.player.x = Math.max(0, Math.min(canvas.width - gameState.player.width, gameState.player.x));
}

function updateHazards(deltaTime) {
  gameState.spawnTimer += deltaTime;
  if (gameState.spawnTimer >= gameState.spawnInterval) {
    gameState.spawnTimer = 0;
    createHazard();
    gameState.spawnInterval = Math.max(0.3, gameState.spawnInterval - 0.01);
  }

  gameState.hazards = gameState.hazards.filter((hazard) => {
    hazard.y += hazard.speed * deltaTime;
    return hazard.y < canvas.height + hazard.height;
  });
}

function checkCollisions() {
  const player = gameState.player;

  return gameState.hazards.some((hazard) => {
    return (
      player.x < hazard.x + hazard.width &&
      player.x + player.width > hazard.x &&
      player.y < hazard.y + hazard.height &&
      player.y + player.height > hazard.y
    );
  });
}

function updateScore(deltaTime) {
  gameState.score += deltaTime * 12;
  gameState.speedScale += deltaTime * 0.22;
  const roundedScore = Math.floor(gameState.score);
  scoreElement.textContent = String(roundedScore);

  if (roundedScore > gameState.highScore) {
    gameState.highScore = roundedScore;
    highScoreElement.textContent = String(gameState.highScore);
    saveHighScore();
  }
}

function drawBackground() {
  context.clearRect(0, 0, canvas.width, canvas.height);

  const gradient = context.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#050816");
  gradient.addColorStop(1, "#120f30");
  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);

  gameState.backgroundOffset = (gameState.backgroundOffset + 1.5) % 40;
  context.strokeStyle = "rgba(108, 248, 255, 0.14)";
  context.lineWidth = 1;

  for (let y = -40; y < canvas.height + 40; y += 40) {
    context.beginPath();
    context.moveTo(0, y + gameState.backgroundOffset);
    context.lineTo(canvas.width, y + gameState.backgroundOffset);
    context.stroke();
  }

  for (let x = 0; x < canvas.width; x += 40) {
    context.beginPath();
    context.moveTo(x, 0);
    context.lineTo(x, canvas.height);
    context.stroke();
  }
}

function drawPlayer() {
  const { x, y, width, height, color } = gameState.player;
  context.save();
  context.shadowColor = color;
  context.shadowBlur = 18;
  context.fillStyle = color;
  context.fillRect(x, y, width, height);
  context.fillStyle = "#c8fcff";
  context.fillRect(x + 10, y - 6, width - 20, 6);
  context.restore();
}

function drawHazards() {
  gameState.hazards.forEach((hazard) => {
    context.save();
    context.fillStyle = `hsl(${hazard.hue}, 90%, 60%)`;
    context.shadowColor = `hsla(${hazard.hue}, 100%, 70%, 0.8)`;
    context.shadowBlur = 16;
    context.fillRect(hazard.x, hazard.y, hazard.width, hazard.height);
    context.restore();
  });
}

function drawOverlay() {
  if (gameState.running) {
    return;
  }

  context.save();
  context.fillStyle = "rgba(2, 6, 23, 0.54)";
  context.fillRect(0, 0, canvas.width, canvas.height);

  context.textAlign = "center";
  context.fillStyle = "#eef5ff";
  context.font = "700 32px Arial";
  context.fillText(gameState.gameOver ? "Game Over" : "Neon Dodge", canvas.width / 2, canvas.height / 2 - 18);

  context.font = "400 18px Arial";
  context.fillStyle = "#b6c7e5";
  const message = gameState.gameOver
    ? "Press Space or Restart to try again"
    : "Press Space or Start Game to begin";
  context.fillText(message, canvas.width / 2, canvas.height / 2 + 18);
  context.restore();
}

function render() {
  drawBackground();
  drawHazards();
  drawPlayer();
  drawOverlay();
}

function gameLoop(timestamp) {
  if (!gameState.running) {
    render();
    return;
  }

  if (gameState.lastFrameTime === 0) {
    gameState.lastFrameTime = timestamp;
  }

  const deltaTime = Math.min((timestamp - gameState.lastFrameTime) / 1000, 0.032);
  gameState.lastFrameTime = timestamp;

  updatePlayer(deltaTime);
  updateHazards(deltaTime);
  updateScore(deltaTime);

  if (checkCollisions()) {
    endGame();
  }

  render();

  if (gameState.running) {
    requestAnimationFrame(gameLoop);
  }
}

function handleKeyChange(event, isPressed) {
  if (event.code === "ArrowLeft" || event.code === "KeyA") {
    gameState.keys.left = isPressed;
  }

  if (event.code === "ArrowRight" || event.code === "KeyD") {
    gameState.keys.right = isPressed;
  }

  if (event.code === "Space") {
    event.preventDefault();
    if (isPressed && !gameState.running) {
      startGame();
    }
  }
}

window.addEventListener("keydown", (event) => handleKeyChange(event, true));
window.addEventListener("keyup", (event) => handleKeyChange(event, false));

startButton.addEventListener("click", () => {
  if (!gameState.running) {
    startGame();
  }
});

restartButton.addEventListener("click", () => {
  startGame();
});

resetGame();
render();
