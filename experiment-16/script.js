// Theme Switcher
const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeIcon = document.getElementById('themeIcon');

themeToggleBtn.addEventListener('click', () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  if (currentTheme === 'cyberpunk') {
    document.documentElement.removeAttribute('data-theme');
    themeIcon.textContent = '✨';
  } else {
    document.documentElement.setAttribute('data-theme', 'cyberpunk');
    themeIcon.textContent = '⚡';
  }
});

// Ping Button Simulation
const pingBtn = document.getElementById('pingBtn');
const pingNotification = document.getElementById('pingNotification');

pingBtn.addEventListener('click', () => {
  pingNotification.classList.remove('hidden');
  setTimeout(() => {
    pingNotification.classList.add('hidden');
  }, 4000);
});

// Uptime Counter
let seconds = 0;
const uptimeElement = document.getElementById('uptimeCounter');

setInterval(() => {
  seconds++;
  const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
  const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  uptimeElement.textContent = `${hrs}:${mins}:${secs}`;
}, 1000);
