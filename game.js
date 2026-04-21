const canvas = document.getElementById("game-canvas");
const ctx = canvas.getContext("2d");

const scoreValue = document.getElementById("score");
const bestScoreValue = document.getElementById("best-score");
const starsCollectedValue = document.getElementById("stars-collected");
const shieldsValue = document.getElementById("shields");
const statusText = document.getElementById("status-text");
const startButton = document.getElementById("start-button");
const jumpscare = document.getElementById("jumpscare");
const jumpscareAudio = document.getElementById("jumpscare-audio");

const BEST_SCORE_KEY = "meteor-sprint-best-score";
const keys = new Set();
let jumpscareTimeoutId = null;
let audioUnlocked = false;

let pointerDragActive = false;
let pointerDragPointerId = null;
const pointerDragOffset = { x: 0, y: 0 };

function canvasPointFromClient(clientX, clientY) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (clientX - rect.left) * scaleX,
    y: (clientY - rect.top) * scaleY,
  };
}

function releasePointerDrag() {
  if (pointerDragPointerId !== null) {
    try {
      if (canvas.hasPointerCapture(pointerDragPointerId)) {
        canvas.releasePointerCapture(pointerDragPointerId);
      }
    } catch {
      // Some browsers throw if capture was already released.
    }
  }

  pointerDragActive = false;
  pointerDragPointerId = null;
}

function applyPointerToShip(clientX, clientY) {
  if (!state.isRunning || !state.ship || !pointerDragActive) {
    return;
  }

  const point = canvasPointFromClient(clientX, clientY);
  const ship = state.ship;
  ship.x = clamp(
    point.x - pointerDragOffset.x,
    14,
    canvas.width - ship.width - 14
  );
  ship.y = clamp(
    point.y - pointerDragOffset.y,
    16,
    canvas.height - ship.height - 16
  );
}

function readBestScore() {
  try {
    const parsedScore = Number.parseInt(localStorage.getItem(BEST_SCORE_KEY) || "0", 10);
    return Number.isFinite(parsedScore) ? parsedScore : 0;
  } catch {
    return 0;
  }
}

function writeBestScore(score) {
  try {
    localStorage.setItem(BEST_SCORE_KEY, score.toString());
  } catch {
    // Ignore storage failures so the game still runs in restricted browser modes.
  }
}

async function unlockAudio() {
  if (!jumpscareAudio) {
    return;
  }

  jumpscareAudio.volume = 0;

  try {
    await jumpscareAudio.play();
    jumpscareAudio.pause();
    jumpscareAudio.currentTime = 0;
    jumpscareAudio.volume = 1;
    audioUnlocked = true;
  } catch {
    audioUnlocked = false;
  }
}

function playJumpscareSound() {
  if (!jumpscareAudio || !audioUnlocked) {
    return;
  }

  jumpscareAudio.pause();
  jumpscareAudio.currentTime = 0;
  jumpscareAudio.volume = 1;
  void jumpscareAudio.play().catch(() => {
    audioUnlocked = false;
  });
}

function hideJumpscare() {
  if (!jumpscare) {
    return;
  }

  if (jumpscareTimeoutId) {
    window.clearTimeout(jumpscareTimeoutId);
    jumpscareTimeoutId = null;
  }

  jumpscare.classList.remove("is-visible");
  jumpscare.setAttribute("aria-hidden", "true");
  document.body.classList.remove("jumpscare-active");

  if (jumpscareAudio) {
    jumpscareAudio.pause();
    jumpscareAudio.currentTime = 0;
  }
}

function triggerJumpscare() {
  if (!jumpscare) {
    return;
  }

  hideJumpscare();
  jumpscare.classList.remove("is-visible");
  void jumpscare.offsetWidth;
  jumpscare.classList.add("is-visible");
  jumpscare.setAttribute("aria-hidden", "false");
  document.body.classList.add("jumpscare-active");
  playJumpscareSound();

  jumpscareTimeoutId = window.setTimeout(() => {
    jumpscare.classList.remove("is-visible");
    jumpscare.setAttribute("aria-hidden", "true");
    document.body.classList.remove("jumpscare-active");
    jumpscareTimeoutId = null;
  }, 1450);
}

const state = {
  isRunning: false,
  isGameOver: false,
  lastTime: 0,
  spawnTimer: 0,
  starTimer: 0,
  score: 0,
  bestScore: readBestScore(),
  starsCollected: 0,
  meteorSpeed: 220,
  ship: null,
  meteors: [],
  stars: [],
  backgroundStars: [],
};

function createShip() {
  return {
    x: canvas.width * 0.15,
    y: canvas.height * 0.5,
    width: 28,
    height: 18,
    speed: 320,
    shields: 3,
    invulnerableFor: 0,
  };
}

function createMeteor() {
  const radius = randomInRange(16, 36);
  return {
    x: canvas.width + radius + randomInRange(0, 120),
    y: randomInRange(radius, canvas.height - radius),
    radius,
    speed: state.meteorSpeed + randomInRange(20, 160),
    spin: randomInRange(-3, 3),
    rotation: randomInRange(0, Math.PI * 2),
  };
}

function createStar() {
  return {
    x: canvas.width + randomInRange(20, 120),
    y: randomInRange(30, canvas.height - 30),
    radius: 10,
    speed: state.meteorSpeed * 0.9,
    pulse: randomInRange(0, Math.PI * 2),
  };
}

function createBackgroundStars() {
  return Array.from({ length: 70 }, () => ({
    x: randomInRange(0, canvas.width),
    y: randomInRange(0, canvas.height),
    size: randomInRange(1, 3),
    speed: randomInRange(12, 70),
  }));
}

function resetGame() {
  releasePointerDrag();
  hideJumpscare();
  state.ship = createShip();
  state.meteors = [];
  state.stars = [];
  state.score = 0;
  state.starsCollected = 0;
  state.meteorSpeed = 220;
  state.spawnTimer = 0;
  state.starTimer = 0;
  state.isGameOver = false;
  state.isRunning = true;
  state.lastTime = 0;

  statusText.textContent =
    "Meteor storm incoming. Drag on the game to steer, or use keys. Dodge meteors and collect stars.";
  startButton.textContent = "Restart game";
  syncHud();
}

function syncHud() {
  scoreValue.textContent = Math.floor(state.score).toString();
  bestScoreValue.textContent = state.bestScore.toString();
  starsCollectedValue.textContent = state.starsCollected.toString();
  shieldsValue.textContent = state.ship ? state.ship.shields.toString() : "0";
}

function randomInRange(min, max) {
  return Math.random() * (max - min) + min;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function circleTouchesShip(circle, ship) {
  const closestX = clamp(circle.x, ship.x, ship.x + ship.width);
  const closestY = clamp(circle.y, ship.y, ship.y + ship.height);
  const dx = circle.x - closestX;
  const dy = circle.y - closestY;
  return dx * dx + dy * dy <= circle.radius * circle.radius;
}

function damageShip() {
  if (state.ship.invulnerableFor > 0) {
    return;
  }

  state.ship.shields -= 1;
  state.ship.invulnerableFor = 1.25;
  syncHud();

  if (state.ship.shields <= 0) {
    endGame();
  } else {
    statusText.textContent = `Shield hit! ${state.ship.shields} shield${
      state.ship.shields === 1 ? "" : "s"
    } left.`;
  }
}

function collectStar() {
  state.starsCollected += 1;
  state.score += 50;

  if (state.starsCollected % 5 === 0 && state.ship.shields < 5) {
    state.ship.shields += 1;
    statusText.textContent = "Shield restored! Keep the streak going.";
  } else {
    statusText.textContent = "Star collected! Bonus score awarded.";
  }

  syncHud();
}

function endGame() {
  releasePointerDrag();
  state.isRunning = false;
  state.isGameOver = true;
  triggerJumpscare();

  const roundedScore = Math.floor(state.score);
  if (roundedScore > state.bestScore) {
    state.bestScore = roundedScore;
    writeBestScore(state.bestScore);
    statusText.textContent = `New best score: ${roundedScore}. Tap the game, press Space, or Restart game.`;
  } else {
    statusText.textContent = `Run over at ${roundedScore} points. Tap the game, press Space, or Restart game.`;
  }

  syncHud();
}

function update(deltaSeconds) {
  if (!state.isRunning || !state.ship) {
    return;
  }

  const ship = state.ship;

  if (!pointerDragActive) {
    let xInput = 0;
    let yInput = 0;

    if (keys.has("ArrowLeft") || keys.has("a")) {
      xInput -= 1;
    }
    if (keys.has("ArrowRight") || keys.has("d")) {
      xInput += 1;
    }
    if (keys.has("ArrowUp") || keys.has("w")) {
      yInput -= 1;
    }
    if (keys.has("ArrowDown") || keys.has("s")) {
      yInput += 1;
    }

    const magnitude = Math.hypot(xInput, yInput) || 1;
    ship.x += (xInput / magnitude) * ship.speed * deltaSeconds;
    ship.y += (yInput / magnitude) * ship.speed * deltaSeconds;
    ship.x = clamp(ship.x, 14, canvas.width - ship.width - 14);
    ship.y = clamp(ship.y, 16, canvas.height - ship.height - 16);
  }
  ship.invulnerableFor = Math.max(0, ship.invulnerableFor - deltaSeconds);

  state.score += deltaSeconds * 24;
  state.meteorSpeed += deltaSeconds * 6;
  state.spawnTimer -= deltaSeconds;
  state.starTimer -= deltaSeconds;

  const spawnInterval = clamp(1.08 - state.score / 1100, 0.32, 1.08);
  if (state.spawnTimer <= 0) {
    state.meteors.push(createMeteor());
    state.spawnTimer = spawnInterval;
  }

  const starInterval = clamp(2.2 - state.score / 2200, 1.1, 2.2);
  if (state.starTimer <= 0) {
    state.stars.push(createStar());
    state.starTimer = starInterval;
  }

  state.meteors = state.meteors.filter((meteor) => {
    meteor.x -= meteor.speed * deltaSeconds;
    meteor.rotation += meteor.spin * deltaSeconds;

    if (circleTouchesShip(meteor, ship)) {
      damageShip();
      return false;
    }

    return meteor.x + meteor.radius > -40;
  });

  if (!state.isRunning) {
    syncHud();
    return;
  }

  state.stars = state.stars.filter((star) => {
    star.x -= star.speed * deltaSeconds;
    star.pulse += deltaSeconds * 5;

    if (circleTouchesShip(star, ship)) {
      collectStar();
      return false;
    }

    return star.x + star.radius > -20;
  });

  syncHud();
}

function drawBackground() {
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, "#04061b");
  gradient.addColorStop(1, "#0e1738");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (const star of state.backgroundStars) {
    star.x -= star.speed * 0.016;
    if (star.x < -star.size) {
      star.x = canvas.width + star.size;
      star.y = randomInRange(0, canvas.height);
    }

    ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
    ctx.fillRect(star.x, star.y, star.size, star.size);
  }

  for (let i = 0; i < 4; i += 1) {
    const stripeY = (i + 1) * 95;
    ctx.strokeStyle = `rgba(74, 138, 255, ${0.08 + i * 0.02})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, stripeY);
    ctx.quadraticCurveTo(canvas.width / 2, stripeY - 40, canvas.width, stripeY);
    ctx.stroke();
  }
}

function drawShip(ship) {
  const flashing = ship.invulnerableFor > 0 && Math.floor(ship.invulnerableFor * 10) % 2 === 0;
  if (flashing) {
    return;
  }

  ctx.save();
  ctx.translate(ship.x, ship.y);

  ctx.fillStyle = "#5ef0ff";
  ctx.beginPath();
  ctx.moveTo(0, ship.height / 2);
  ctx.lineTo(ship.width - 8, 0);
  ctx.lineTo(ship.width, ship.height / 2);
  ctx.lineTo(ship.width - 8, ship.height);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.moveTo(8, ship.height / 2);
  ctx.lineTo(ship.width - 10, 4);
  ctx.lineTo(ship.width - 4, ship.height / 2);
  ctx.lineTo(ship.width - 10, ship.height - 4);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#9d6bff";
  ctx.beginPath();
  ctx.moveTo(-8, ship.height / 2);
  ctx.lineTo(0, 4);
  ctx.lineTo(4, ship.height / 2);
  ctx.lineTo(0, ship.height - 4);
  ctx.closePath();
  ctx.fill();

  ctx.restore();
}

function drawMeteor(meteor) {
  ctx.save();
  ctx.translate(meteor.x, meteor.y);
  ctx.rotate(meteor.rotation);

  ctx.fillStyle = "#ff875a";
  ctx.beginPath();
  for (let i = 0; i < 8; i += 1) {
    const angle = (Math.PI * 2 * i) / 8;
    const radius = meteor.radius + (i % 2 === 0 ? 6 : -4);
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#2f1128";
  ctx.beginPath();
  ctx.arc(-meteor.radius * 0.2, -meteor.radius * 0.1, meteor.radius * 0.28, 0, Math.PI * 2);
  ctx.arc(meteor.radius * 0.28, meteor.radius * 0.14, meteor.radius * 0.18, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawStarCollectible(star) {
  const pulseRadius = star.radius + Math.sin(star.pulse) * 1.5;
  ctx.save();
  ctx.translate(star.x, star.y);

  ctx.fillStyle = "#ffe16b";
  ctx.beginPath();
  for (let i = 0; i < 10; i += 1) {
    const angle = -Math.PI / 2 + (Math.PI * 2 * i) / 10;
    const radius = i % 2 === 0 ? pulseRadius : pulseRadius * 0.45;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }
  ctx.closePath();
  ctx.fill();

  ctx.restore();
}

function drawOverlay() {
  if (state.isRunning || !state.ship) {
    return;
  }

  ctx.fillStyle = "rgba(2, 4, 15, 0.54)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.textAlign = "center";
  ctx.fillStyle = "#f5f7ff";

  if (state.isGameOver) {
    ctx.font = "700 36px Inter, system-ui, sans-serif";
    ctx.fillText("Storm Breached", canvas.width / 2, canvas.height / 2 - 24);
    ctx.font = "500 18px Inter, system-ui, sans-serif";
    ctx.fillText(
      `Final score: ${Math.floor(state.score)}`,
      canvas.width / 2,
      canvas.height / 2 + 10
    );
    ctx.fillText(
      "Tap canvas, Space, or Restart game",
      canvas.width / 2,
      canvas.height / 2 + 40
    );
  } else {
    ctx.font = "700 34px Inter, system-ui, sans-serif";
    ctx.fillText("Meteor Sprint", canvas.width / 2, canvas.height / 2 - 18);
    ctx.font = "500 18px Inter, system-ui, sans-serif";
    ctx.fillText(
      "Keys, or drag on the game to steer. Collect stars, avoid meteors.",
      canvas.width / 2,
      canvas.height / 2 + 16
    );
    ctx.fillText("Tap canvas, Space, or Start game", canvas.width / 2, canvas.height / 2 + 44);
  }
}

function render() {
  drawBackground();

  if (state.ship) {
    for (const meteor of state.meteors) {
      drawMeteor(meteor);
    }

    for (const star of state.stars) {
      drawStarCollectible(star);
    }

    drawShip(state.ship);
  }

  drawOverlay();
}

function gameLoop(timestamp) {
  if (!state.lastTime) {
    state.lastTime = timestamp;
  }

  const deltaSeconds = Math.min((timestamp - state.lastTime) / 1000, 0.05);
  state.lastTime = timestamp;

  update(deltaSeconds);
  render();
  requestAnimationFrame(gameLoop);
}

function normalizeKey(key) {
  return key.length === 1 ? key.toLowerCase() : key;
}

window.addEventListener("keydown", (event) => {
  void unlockAudio();
  const key = normalizeKey(event.key);

  if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(event.key)) {
    event.preventDefault();
  }

  if (key === " ") {
    if (!state.isRunning) {
      resetGame();
    }
    return;
  }

  keys.add(key);
});

window.addEventListener("keyup", (event) => {
  keys.delete(normalizeKey(event.key));
});

canvas.addEventListener("pointerdown", (event) => {
  if (event.button !== undefined && event.button !== 0) {
    return;
  }

  event.preventDefault();
  void unlockAudio();

  const point = canvasPointFromClient(event.clientX, event.clientY);

  if (!state.isRunning) {
    resetGame();
  }

  if (!state.isRunning || !state.ship) {
    return;
  }

  try {
    canvas.setPointerCapture(event.pointerId);
  } catch {
    // setPointerCapture can fail in rare cases; movement still works without capture.
  }

  pointerDragPointerId = event.pointerId;
  pointerDragActive = true;
  pointerDragOffset.x = point.x - state.ship.x;
  pointerDragOffset.y = point.y - state.ship.y;
  applyPointerToShip(event.clientX, event.clientY);
});

canvas.addEventListener("pointermove", (event) => {
  if (!pointerDragActive || event.pointerId !== pointerDragPointerId) {
    return;
  }

  event.preventDefault();
  applyPointerToShip(event.clientX, event.clientY);
});

canvas.addEventListener("pointerup", (event) => {
  if (event.pointerId !== pointerDragPointerId) {
    return;
  }

  event.preventDefault();
  releasePointerDrag();
});

canvas.addEventListener("pointercancel", (event) => {
  if (event.pointerId !== pointerDragPointerId) {
    return;
  }

  releasePointerDrag();
});

canvas.addEventListener("lostpointercapture", (event) => {
  if (event.pointerId !== pointerDragPointerId) {
    return;
  }

  releasePointerDrag();
});

startButton.addEventListener("click", () => {
  void unlockAudio();
  resetGame();
});

state.backgroundStars = createBackgroundStars();
state.ship = createShip();
syncHud();
render();
requestAnimationFrame(gameLoop);