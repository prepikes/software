// script.js

// Buttons for selecting login type
const userLoginBtn = document.getElementById('userLoginBtn');
const adminLoginBtn = document.getElementById('adminLoginBtn');

// Forms for user and admin login
const userLoginForm = document.getElementById('userLoginForm');
const adminLoginForm = document.getElementById('adminLoginForm');

// Show user login form when user login button is clicked
userLoginBtn.addEventListener('click', () => {
    userLoginForm.style.display = 'block';
    adminLoginForm.style.display = 'none';
});

// Show admin login form when admin login button is clicked
adminLoginBtn.addEventListener('click', () => {
    adminLoginForm.style.display = 'block';
    userLoginForm.style.display = 'none';
});

// Handle user login
document.getElementById('userLoginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const roomNumber = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simulate user login validation (room number and ID card check)
    if (roomNumber==='123' && password === '123') {
        alert('欢迎您!');
        window.location.href = '../html/index.html';  // Redirect to user page
    } else {
        document.getElementById('error-message').innerText = 'Invalid room number or ID card.';
    }
});

// Handle admin login
document.getElementById('adminLoginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const adminUsername = document.getElementById('adminUsername').value;
    const adminPassword = document.getElementById('adminPassword').value;

    // Simulate admin login validation
    if (adminUsername === 'admin' && adminPassword === '123') {
        alert('欢迎您，管理员!');
        window.location.href = '../html/admin_index.html';  // Redirect to admin page
    } else {
        document.getElementById('error-message').innerText = 'Invalid admin username or password.';
    }
});
