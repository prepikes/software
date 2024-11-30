let rooms = {
    '101': { currentTemp: 25, targetTemp: 25, fanSpeed: 2, isOn: true },
    '102': { currentTemp: 25, targetTemp: 25, fanSpeed: 0, isOn: false },
    '103': { currentTemp: 25, targetTemp: 25, fanSpeed: 3, isOn: true },
    '104': { currentTemp: 25, targetTemp: 25, fanSpeed: 0, isOn: false }
};

let currentRoom = null;

function changeTemp(roomId, targetTemp) {
    if (!roomId || targetTemp < 18 || targetTemp > 30) return;
    
    let room = rooms[roomId];
    if (room && room.isOn) {
        room.targetTemp = targetTemp;
        room.currentTemp = targetTemp;
        updateDisplayTemp();
        updateRoomDisplay();
    }
}

function togglePower() {
    if (!currentRoom) return;
    let room = rooms[currentRoom];
    room.isOn = !room.isOn;
    if (room.isOn) {
        document.getElementById('target-temp').value = room.targetTemp;
        document.getElementById('display-temp').textContent = `${room.targetTemp}°`;
        document.querySelector('.power-status').classList.add('on');
    } else {
        document.getElementById('display-temp').textContent = '';
        room.fanSpeed = 0;
        document.querySelector('.power-status').classList.remove('on');
    }
    updateFanSpeedIcon();
    updateRoomDisplay();
}

function changeFanSpeed() {
    if (!currentRoom) return;
    let room = rooms[currentRoom];
    if (room.isOn) {
        room.fanSpeed = (room.fanSpeed + 1) % 6;
        updateFanSpeedIcon();
    }
    updateRoomDisplay();
}

function updateDisplayTemp() {
    if (!currentRoom) return;
    let room = rooms[currentRoom];
    if (room.isOn) {
        const tempElement = document.getElementById('display-temp');
        tempElement.textContent = `${room.currentTemp}°`;
        document.getElementById('ac-temp').value = room.currentTemp;
    }
}

function updateFanSpeedIcon() {
    if (!currentRoom) return;
    let room = rooms[currentRoom];
    const iconElement = document.getElementById('fan-speed-icon');
    iconElement.innerHTML = ''; 
    
    for (let i = 0; i < 5; i++) {
        const bar = document.createElement('div');
        bar.className = 'fan-bar';
        const height = 12 + (i * 5);
        bar.style.height = `${height}px`;
        if (room.isOn && i < room.fanSpeed) {
            bar.classList.add('active');
        }
        iconElement.appendChild(bar);
    }
}

// 更新房间显示信息
function updateRoomDisplay() {
    const roomCards = document.querySelectorAll('.room-card');
    roomCards.forEach(card => {
        const roomNumber = card.querySelector('h3').textContent.split(' ')[1];
        const room = rooms[roomNumber];
        const infoDiv = card.querySelector('.room-info');
        infoDiv.innerHTML = `
            <p>当前温度: ${room.currentTemp}°C</p>
            <p>空调状态: ${room.isOn ? '运行中' : '关闭'}</p>
            <p>风速: ${room.fanSpeed}</p>
        `;
    });
}

// 初始化房间数据
function initializeRooms() {
    const roomsData = [
        { number: '101', temp: 26, occupied: true },
        { number: '102', temp: 24, occupied: false },
        { number: '103', temp: 25, occupied: true },
        { number: '104', temp: 23, occupied: false },
    ];
    
    const roomGrid = document.querySelector('.room-grid');
    roomGrid.innerHTML = '';
    
    roomsData.forEach(room => {
        const roomCard = createRoomCard(room);
        roomGrid.appendChild(roomCard);
    });
    updateRoomDisplay();
}

function createRoomCard(room) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'room-card';
    cardDiv.innerHTML = `
        <div class="room-header">
            <h3>房间 ${room.number}</h3>
            <span class="status ${room.occupied ? 'occupied' : ''}">${room.occupied ? '已入住' : '空闲'}</span>
        </div>
        <div class="room-info">
            <p>
                <span class="power-status ${rooms[room.number].isOn ? 'on' : ''}"></span>
                当前温度: ${room.temp}°C
            </p>
            <p>空调状态: ${rooms[room.number].isOn ? '运行中' : '关闭'}</p>
            <p>风速: ${rooms[room.number].fanSpeed}</p>
        </div>
        <div class="room-controls">
            <button class="control-btn" onclick="showDetails('${room.number}')">查看详情</button>
            <button class="control-btn" onclick="showControl('${room.number}')">控制空调</button>
        </div>
    `;
    return cardDiv;
}

function showControl(roomNumber) {
    currentRoom = roomNumber;
    document.getElementById('control-room-number').textContent = roomNumber;
    
    // 更新控制面板显示当前房间的状态
    const room = rooms[roomNumber];
    const powerStatus = document.querySelector('.power-status');
    
    if (room.isOn) {
        document.getElementById('target-temp').value = room.targetTemp;
        document.getElementById('display-temp').textContent = `${room.targetTemp}°`;
        powerStatus.classList.add('on');
    } else {
        document.getElementById('display-temp').textContent = '';
        powerStatus.classList.remove('on');
    }
    updateFanSpeedIcon();
    
    switchPage('ac-control');
}

function setTargetTemp() {
    if (!currentRoom) return;
    let room = rooms[currentRoom];
    if (room.isOn) {
        const targetTempInput = document.getElementById('target-temp');
        const targetTemp = parseInt(targetTempInput.value, 10);
        if (targetTemp >= 18 && targetTemp <= 30) {
            changeTemp(currentRoom, targetTemp);
        } else {
            alert('温度必须在18-30度之间');
        }
    }
}

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

// 添加显示详情和控制面板的函数
function showDetails(roomNumber) {
    document.getElementById('detail-room-number').textContent = roomNumber;
    // 这里可以添加从后端获取详细数据的逻辑
    switchPage('ac-details');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeRooms();
});