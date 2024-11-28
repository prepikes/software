let currentTemp = 25;
let fanSpeed = 1; // 1, 2, 3 - 代表低、中、高风速
let isOn = false;

function increaseTemp() {
    if (isOn && currentTemp < 30) {
        currentTemp++;
        updateDisplayTemp();
    }
}

function decreaseTemp() {
    if (isOn && currentTemp > 18) {
        currentTemp--;
        updateDisplayTemp();
    }
}

function togglePower() {
    isOn = !isOn;
    if (isOn) {
        document.getElementById('ac-temp').value = currentTemp;
        updateDisplayTemp();
    } else {
        document.getElementById('display-temp').textContent = '关';
    }
}

function changeFanSpeed() {
    if (isOn) {
        fanSpeed = (fanSpeed % 3) + 1;
        updateFanSpeedIcon();
    }
}

function updateDisplayTemp() {
    if (isOn) {
        const tempElement = document.getElementById('display-temp');
        tempElement.textContent = `${currentTemp}°`;
        document.getElementById('ac-temp').value = currentTemp;
    }
}

function updateFanSpeedIcon() {
    const iconElement = document.getElementById('fan-speed-icon');
    switch (fanSpeed) {
        case 1:
            iconElement.innerHTML = '&#9734;&#9734;&#9734;';
            break;
        case 2:
            iconElement.innerHTML = '&#9733;&#9734;&#9734;';
            break;
        case 3:
            iconElement.innerHTML = '&#9733;&#9733;&#9733;';
            break;
    }
}

// 初始化
updateDisplayTemp();
updateFanSpeedIcon();

// 滑动条变化时更新显示温度
document.getElementById('ac-temp').addEventListener('input', function() {
    if (isOn) {
        currentTemp = parseInt(this.value, 10);
        updateDisplayTemp();
    }
});