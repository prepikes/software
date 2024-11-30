let currentTemp = 25;
let targetTemp = 25;
let fanSpeed = 0; // 0-5 代表六档风速（包括关闭）
let isOn = false; // 默认关机

function togglePower() {
    isOn = !isOn;
    if (isOn) {
        document.getElementById('target-temp').value = targetTemp;
        document.getElementById('display-temp').textContent = `${targetTemp}°`;
        document.querySelector('.power-status').classList.add('on');
    } else {
        document.getElementById('display-temp').textContent = '';
        fanSpeed = 0;
        document.querySelector('.power-status').classList.remove('on');
    }
    updateFanSpeedIcon();
}

function changeFanSpeed() {
    if (isOn) {
        fanSpeed = (fanSpeed + 1) % 6;  // 0-5循环
        updateFanSpeedIcon();
    }
}

function setTargetTemp() {
    if (isOn) {
        const tempInput = document.getElementById('target-temp');
        const newTemp = parseInt(tempInput.value, 10);
        if (newTemp >= 18 && newTemp <= 30) {
            targetTemp = newTemp;
            currentTemp = newTemp; // 简化版本，实际可能需要渐变
            updateDisplayTemp();
        } else {
            alert('温度必须在18-30度之间');
        }
    }
}

function updateDisplayTemp() {
    if (isOn) {
        const tempElement = document.getElementById('display-temp');
        tempElement.textContent = `${currentTemp}°`;
    }
}

function updateFanSpeedIcon() {
    const iconElement = document.getElementById('fan-speed-icon');
    iconElement.innerHTML = ''; 
    
    // 创建五个风速条，每个高度递增
    for (let i = 0; i < 5; i++) {
        const bar = document.createElement('div');
        bar.className = 'fan-bar';
        const height = 12 + (i * 5);
        bar.style.height = `${height}px`;
        // 只有在开机状态下才显示激活的风速条
        if (isOn && i < fanSpeed) {
            bar.classList.add('active');
        }
        iconElement.appendChild(bar);
    }
}

// 添加花费统计图相关代码
function initExpenseChart() {
    const ctx = document.getElementById('expense-chart').getContext('2d');
    
    // 模拟数据
    const data = {
        labels: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
        datasets: [{
            label: '空调费用 (元/小时)',
            data: [2.5, 3.0, 2.8, 3.2, 2.7, 3.1],
            borderColor: '#3498db',
            backgroundColor: 'rgba(52, 152, 219, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,  // 保持宽高比
            plugins: {
                title: {
                    display: false
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    min: 0,
                    max: 5,
                    ticks: {
                        stepSize: 1
                    },
                    title: {
                        display: true,
                        text: '费用 (元)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '时间'
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

// 修改初始化部分
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('display-temp').textContent = ''; // 初始显示为空
    updateFanSpeedIcon(); // 初始化风速图标
    initExpenseChart(); // 初始化费用图表
});