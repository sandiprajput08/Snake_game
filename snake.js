// Simple, robust Snake implementation for the web
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const grid = 20; // cell size
const cols = canvas.width / grid | 0;
const rows = canvas.height / grid | 0;

let snake = [{x: Math.floor(cols/2)*grid, y: Math.floor(rows/2)*grid}];
let dir = {x:0,y:0};
let food = {};
let score = 0;
let speed = 100; // ms per tick
let running = false;
let loopId = null;

// Read best (localStorage)
const bestKey = 'snake_web_best_v1';
let best = parseInt(localStorage.getItem(bestKey) || '0', 10);
document.getElementById('best').textContent = 'Best: ' + best;

function placeFood(){
  // pick a cell not occupied by snake
  const occupied = new Set(snake.map(s => s.x + ':' + s.y));
  let fx, fy;
  do {
    fx = Math.floor(Math.random() * cols) * grid;
    fy = Math.floor(Math.random() * rows) * grid;
    // avoid header area (top 0.. keep whole canvas)
  } while (occupied.has(fx + ':' + fy));
  food = {x: fx, y: fy};
}

function resetGame(){
  snake = [{x: Math.floor(cols/2)*grid, y: Math.floor(rows/2)*grid}];
  dir = {x:0,y:0};
  score = 0;
  placeFood();
  document.getElementById('score').textContent = 'Score: ' + score;
}

function tick(){
  // move head
  const head = {x: snake[snake.length-1].x + dir.x*grid, y: snake[snake.length-1].y + dir.y*grid};

  // if not moving, just draw
  if(dir.x === 0 && dir.y === 0){ draw(); return; }

  // wall collision
  if(head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height){
    gameOver();
    return;
  }

  // self collision
  for(let i=0;i<snake.length;i++){
    if(snake[i].x === head.x && snake[i].y === head.y){ gameOver(); return; }
  }

  snake.push(head);

  // food
  if(head.x === food.x && head.y === food.y){
    score += 10;
    document.getElementById('score').textContent = 'Score: ' + score;
    placeFood();
    // small speedup every 50 points
    if(score % 50 === 0 && speed > 40) speed -= 6;
  } else {
    // move: remove tail
    snake.shift();
  }

  draw();
}

function draw(){
  // background
  ctx.fillStyle = '#01121a';
  ctx.fillRect(0,0,canvas.width,canvas.height);

  // draw food
  ctx.fillStyle = '#ff4646';
  ctx.fillRect(food.x, food.y, grid, grid);
  ctx.fillStyle = '#ffb84d';
  ctx.fillRect(food.x + 3, food.y + 3, grid - 6, grid - 6);

  // draw snake
  for(let i=0;i<snake.length;i++){
    const s = snake[i];
    if(i === snake.length-1){
      // head
      ctx.fillStyle = '#ffff66';
      ctx.fillRect(s.x, s.y, grid, grid);
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2;
      ctx.strokeRect(s.x, s.y, grid, grid);
      // eyes
      ctx.fillStyle = '#000000';
      ctx.beginPath(); ctx.arc(s.x + 6, s.y + 6, 3, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(s.x + grid - 6, s.y + 6, 3, 0, Math.PI*2); ctx.fill();
    } else {
      ctx.fillStyle = '#0ef08f';
      ctx.fillRect(s.x, s.y, grid, grid);
      ctx.strokeStyle = '#0a6f4e'; ctx.lineWidth = 1; ctx.strokeRect(s.x, s.y, grid, grid);
    }
  }
}

function gameOver(){
  running = false;
  clearInterval(loopId);
  loopId = null;
  // show overlay simple alert or message
  if(score > best){ best = score; localStorage.setItem(bestKey, String(best)); document.getElementById('best').textContent = 'Best: ' + best; }
  setTimeout(()=>{ alert('Game Over! Score: ' + score); }, 10);
}

// input handling
window.addEventListener('keydown', e=>{
  if(e.key === 'ArrowLeft' || e.key === 'a') { if(dir.x===0) dir = {x:-1,y:0}; }
  if(e.key === 'ArrowRight' || e.key === 'd'){ if(dir.x===0) dir = {x:1,y:0}; }
  if(e.key === 'ArrowUp' || e.key === 'w'){ if(dir.y===0) dir = {x:0,y:-1}; }
  if(e.key === 'ArrowDown' || e.key === 's'){ if(dir.y===0) dir = {x:0,y:1}; }
});

// controls
document.getElementById('start').addEventListener('click', ()=>{
  if(!running){
    running = true;
    if(loopId) clearInterval(loopId);
    loopId = setInterval(tick, speed);
  }
});

document.getElementById('pause').addEventListener('click', ()=>{
  running = false; if(loopId) clearInterval(loopId); loopId = null;
});

document.getElementById('restart').addEventListener('click', ()=>{ resetGame(); if(loopId) clearInterval(loopId); speed = 100; loopId = setInterval(tick, speed); running = true; });

// initialize
resetGame();
// start automatically
// loopId = setInterval(tick, speed); running = false;