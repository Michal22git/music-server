const playerDashboard = document.querySelector('.player-dashboard');
const playerDashboardTitle = document.querySelector('.player-dashboard-title');
const playerDashboardTimer = document.querySelector('.player-dashboard-timer');
const progressBar = document.querySelector('.progress');
const progressBarContainer = document.querySelector('.progress-bar');
let audio = null;
let click = false;

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

function handlePlayButtonClick(element) {
    const songTitle = element.getAttribute('data-title');
    const songTime = element.getAttribute('data-time');
    const songUrl = element.getAttribute('name');

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
    });

    changeDashboardData(songTime, songTitle);
    playerDashboard.style.opacity = 1;
    audio.play();
}

document.querySelectorAll('.play-button').forEach((playButton) => {
    playButton.addEventListener('click', () => {
        handlePlayButtonClick(playButton);
    });
});

document.querySelector('.stop-button-dashboard').addEventListener('click', () => {
    if (audio) {
        audio.pause();
        audio = null;
        playerDashboard.style.opacity = 0;
        progressBar.style.width = '0%';
        playerDashboardTimer.textContent = '0:00/0:00';
    }
});

progressBarContainer.addEventListener('click', (event) => {
    if (audio) {
        const rect = progressBarContainer.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const percentage = (offsetX / rect.width) * 100;
        const newAudioTime = (percentage / 100) * audio.duration;
        audio.currentTime = newAudioTime;
        console.log(rect)
        console.log(offsetX)
        console.log(percentage)
        console.log(newAudioTime)
        click = true;
        updateProgressBar();
    }
});
