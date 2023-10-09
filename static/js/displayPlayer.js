const playerDashboard = document.querySelector('.player-dashboard');
const playerDashboardTitle = document.querySelector('.player-dashboard-title');
const playerDashboardTimer = document.querySelector('.player-dashboard-timer');
const progressBar = document.querySelector('.progress');
const progressBarContainer = document.querySelector('.progress-bar');
let audio = null;
let isPaused = true;

function formatTime(timeInSeconds) {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.round(timeInSeconds % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

function changeDashboardData(timer, title) {
    playerDashboardTimer.innerHTML = `0/${timer}`;
    playerDashboardTitle.innerHTML = title;
}

function updateProgressBar() {
    const progress = (audio.currentTime / audio.duration) * 100;
    progressBar.style.width = `${progress}%`;
    const currentTimeFormatted = formatTime(audio.currentTime);
    playerDashboardTimer.textContent = `${currentTimeFormatted}/${formatTime(audio.duration)}`;
}

document.querySelectorAll('.play-button').forEach((playButton) => {
    playButton.addEventListener('click', () => {
        const songTitle = playButton.getAttribute('data-title');
        const songTime = playButton.getAttribute('data-time');
        const songUrl = playButton.getAttribute('name');

        if (audio) {
            audio.pause();
        }

        audio = new Audio(songUrl);

        audio.addEventListener('timeupdate', updateProgressBar);
        audio.addEventListener('ended', () => {
            playerDashboard.style.opacity = 0;
            progressBar.style.width = '0%';
            playerDashboardTimer.textContent = '0:00/0:00';
            audio = null;
            isPaused = true;
            document.querySelector('.play-stop-button').textContent = 'Play';
        });

        changeDashboardData(songTime, songTitle);
        playerDashboard.style.opacity = 1;
        audio.play();
        isPaused = false;
        document.querySelector('.play-stop-button').textContent = 'Pause';
    });
});

document.querySelector('.play-stop-button').addEventListener('click', () => {
    if (audio) {
        if (isPaused) {
            audio.play();
            isPaused = false;
            document.querySelector('.play-stop-button').textContent = 'Pause';
        } else {
            audio.pause();
            isPaused = true;
            document.querySelector('.play-stop-button').textContent = 'Play';
        }
    }
});

progressBarContainer.addEventListener('click', (event) => {
    if (audio) {
        const rect = progressBarContainer.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const percentage = (offsetX / rect.width) * 100;
        const newAudioTime = (percentage / 100) * audio.duration;
        audio.currentTime = newAudioTime;
        updateProgressBar();
    }
});
