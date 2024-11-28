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

// 页面切换功能
function switchPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
        page.style.opacity = '0';
    });
    
    const targetPage = document.getElementById(pageId);
    targetPage.classList.add('active');
    
    // 添加简单的淡入效果
    setTimeout(() => {
        targetPage.style.opacity = '1';
    }, 100);
    
    // 只有在切换主要页面时才更新导航按钮状态
    if (pageId === 'room-management' || pageId === 'bill-management') {
        document.querySelectorAll('.nav-button').forEach(button => {
            button.classList.remove('active');
        });
        document.querySelector(`[onclick="switchPage('${pageId}')"]`).classList.add('active');
    }
}

// 初始化房间数据（示例）
function initializeRooms() {
    // 这里可以从后端获取房间数据
    const rooms = [
        { number: '101', temp: 26, acStatus: '运行中', setTemp: 22, occupied: true },
        { number: '102', temp: 24, acStatus: '关闭', setTemp: 25, occupied: false },
        { number: '103', temp: 25, acStatus: '运行中', setTemp: 23, occupied: true },
        { number: '104', temp: 23, acStatus: '关闭', setTemp: 24, occupied: false },
        // 可以添加更多房间...
    ];
    
    // 清空现有的房间卡片
    const roomGrid = document.querySelector('.room-grid');
    roomGrid.innerHTML = '';
    
    // 渲染房间卡片
    rooms.forEach(room => {
        const roomCard = createRoomCard(room);
        roomGrid.appendChild(roomCard);
    });
}

// 创建房间卡片
function createRoomCard(room) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'room-card';
    cardDiv.innerHTML = `
        <div class="room-header">
            <h3>房间 ${room.number}</h3>
            <span class="status ${room.occupied ? 'occupied' : ''}">${room.occupied ? '已入住' : '空闲'}</span>
        </div>
        <div class="room-info">
            <p>当前温度: ${room.temp}°C</p>
            <p>空调状态: ${room.acStatus}</p>
            <p>设定温度: ${room.setTemp}°C</p>
        </div>
        <div class="room-controls">
            <button class="control-btn" onclick="showDetails('${room.number}')">查看详情</button>
            <button class="control-btn" onclick="showControl('${room.number}')">控制空调</button>
        </div>
    `;
    return cardDiv;
}

// 添加显示详情和控制面板的函数
function showDetails(roomNumber) {
    document.getElementById('detail-room-number').textContent = roomNumber;
    // 这里可以添加从后端获取详细数据的逻辑
    switchPage('ac-details');
}

function showControl(roomNumber) {
    document.getElementById('control-room-number').textContent = roomNumber;
    // 这里可以添加从后端获取空调状态的逻辑
    switchPage('ac-control');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeRooms();
});