// Constants
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const WIDTH = 500, HEIGHT = 500;
const ROWS = 5, COLS = 5;
const SQUARE_SIZE = WIDTH / COLS;

const RED = "red";
const BLUE = "blue";
const WHITE = "#ffffff";
const BLACK = "#000000";

// Game Variables
let grid = Array(ROWS).fill().map(() => Array(COLS).fill(0)); // Particles grid
let control = Array(ROWS).fill().map(() => Array(COLS).fill(null)); // Control grid
let points = { R: 0, B: 0 }; // Scores
let playerTurn = 'R'; // Current player ('R' for Red, 'B' for Blue)
let gameOver = false; // Game over flag

// DOM Elements for score and turn info
const scoreElement = document.getElementById("score");
const turnElement = document.getElementById("turn");
const explosionSound = document.getElementById("explosionSound");
const resetButton = document.getElementById("resetBtn");

// Function to draw the grid
function drawGrid() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            // Draw the square
            ctx.strokeStyle = BLACK;
            ctx.strokeRect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE);

            // Draw the particles if any
            let particles = grid[row][col];
            if (particles > 0) {
                let color = control[row][col] === 'R' ? RED : BLUE;
                ctx.fillStyle = color;
                ctx.font = "30px Arial";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(particles, col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2);
            }
        }
    }
    // Update score and turn info
    scoreElement.textContent = `Red: ${points.R} | Blue: ${points.B}`;
    turnElement.textContent = `Current Turn: ${playerTurn === 'R' ? 'Red' : 'Blue'}`;
}

// Function to handle adding particles with animation
function addParticle(row, col) {
    if (gameOver) {
        return; // If the game is over, do nothing
    }

    if (grid[row][col] < 4 && (control[row][col] === null || control[row][col] === playerTurn)) {
        grid[row][col] += 1;
        if (control[row][col] === null) {
            control[row][col] = playerTurn;
        }
        if (grid[row][col] === 4) {
            collapse(row, col);
        }
        checkForWinner();
        playerTurn = playerTurn === 'R' ? 'B' : 'R'; // Switch turn
        drawGrid();
    }
}

// Collapse logic with explosion animation
function collapse(row, col) {
    let collapsingPlayer = control[row][col];
    points[collapsingPlayer] += 1;

    // Play explosion sound
    explosionSound.play();

    // Enhanced Explosion Effect
    let explosionSize = 50;
    let frames = 10;
    let frame = 0;

    // Exploding particle animation
    const explosionInterval = setInterval(() => {
        frame++;
        ctx.clearRect(0, 0, WIDTH, HEIGHT);
        drawGrid();  // Redraw grid

        // Draw explosion effect with particle-like visual
        ctx.fillStyle = collapsingPlayer === 'R' ? RED : BLUE;
        for (let i = 0; i < 8; i++) {
            ctx.beginPath();
            let angle = i * (Math.PI / 4);
            let x = col * SQUARE_SIZE + SQUARE_SIZE / 2 + Math.cos(angle) * explosionSize * (1 - frame / frames);
            let y = row * SQUARE_SIZE + SQUARE_SIZE / 2 + Math.sin(angle) * explosionSize * (1 - frame / frames);
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }

        if (frame === frames) {
            clearInterval(explosionInterval);
            grid[row][col] = 0;
            control[row][col] = null;
            distributeParticles(row, col, collapsingPlayer);
            drawGrid();
        }
    }, 100);
}

// Distribute particles to neighboring squares
function distributeParticles(row, col, player) {
    let neighbors = [
        [row - 1, col], [row + 1, col], [row, col - 1], [row, col + 1]
    ];
    neighbors.forEach(([r, c]) => {
        if (r >= 0 && r < ROWS && c >= 0 && c < COLS) {
            grid[r][c] += 1;
            if (control[r][c] === null) {
                control[r][c] = player;
            }
            if (grid[r][c] === 4) {
                collapse(r, c);
            }
        }
    });
}

// Check for winner and end game if a player wins
function checkForWinner() {
    if (points.R >= 10) {
        alert("Red wins!");
        setTimeout(resetGame, 3000); // Automatically reset after 3 seconds
        gameOver = true;
    } else if (points.B >= 10) {
        alert("Blue wins!");
        setTimeout(resetGame, 3000); // Automatically reset after 3 seconds
        gameOver = true;
    } else if (grid.flat().every(p => p === 3)) {
        alert("Draw! No more moves possible.");
        setTimeout(resetGame, 3000); // Automatically reset after 3 seconds
        gameOver = true;
    }
}

// Handle mouse click
canvas.addEventListener("click", (e) => {
    let x = e.offsetX, y = e.offsetY;
    let row = Math.floor(y / SQUARE_SIZE), col = Math.floor(x / SQUARE_SIZE);
    addParticle(row, col);
});

// Reset game function
function resetGame() {
    grid = Array(ROWS).fill().map(() => Array(COLS).fill(0));
    control = Array(ROWS).fill().map(() => Array(COLS).fill(null));
    points = { R: 0, B: 0 };
    playerTurn = 'R';
    gameOver = false;
    drawGrid();
}
// Add this line to attach the reset function to the reset button
resetButton.addEventListener('click', resetGame);

// Reset game function
function resetGame() {
    grid = Array(ROWS).fill().map(() => Array(COLS).fill(0));
    control = Array(ROWS).fill().map(() => Array(COLS).fill(null));
    points = { R: 0, B: 0 };
    playerTurn = 'R';
    gameOver = false;
    drawGrid();
}
// Initialize the game
drawGrid();
