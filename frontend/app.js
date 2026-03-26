// API 配置
const API_BASE = 'http://localhost:8000';

// 全局状态
let currentStoryId = null;
let currentTurn = 1;

// DOM 元素
const setupScreen = document.getElementById('setup-screen');
const gameScreen = document.getElementById('game-screen');
const storyContent = document.getElementById('story-content');
const choicesContainer = document.getElementById('choices-container');
const turnIndicator = document.getElementById('turn-indicator');
const loadingOverlay = document.getElementById('loading-overlay');

// 显示加载状态
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// 显示剧情文本
async function displayStory(text, container) {
    container.innerHTML = text.replace(/\n/g, '<br>');
}

// 显示选项按钮
function displayChoices(choices) {
    choicesContainer.innerHTML = '';
    choices.forEach((choice, index) => {
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.textContent = `${index + 1}. ${choice}`;
        btn.onclick = () => makeChoice(choice);
        choicesContainer.appendChild(btn);
    });
}

// 开始新故事
async function startStory() {
    const world = document.getElementById('world-select').value;
    const opening = document.getElementById('opening-input').value.trim();
    
    if (!opening) {
        alert('请描述你的开场场景');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/story/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                world: world,
                opening: opening
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        currentStoryId = data.story_id;
        currentTurn = 1;
        
        // 切换到游戏界面
        setupScreen.classList.remove('active');
        gameScreen.classList.add('active');
        
        // 显示剧情
        await displayStory(data.content, storyContent);
        displayChoices(data.choices);
        turnIndicator.textContent = `第 ${currentTurn} 轮`;
        
    } catch (error) {
        console.error('开始故事失败:', error);
        alert('开始故事失败，请确保后端服务已启动');
    } finally {
        hideLoading();
    }
}

// 做出选择
async function makeChoice(choice) {
    if (!currentStoryId) return;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/story/continue`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                story_id: currentStoryId,
                user_choice: choice
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        currentTurn = data.turn_number;
        
        // 显示新剧情
        await displayStory(data.content, storyContent);
        displayChoices(data.choices);
        turnIndicator.textContent = `第 ${currentTurn} 轮`;
        
    } catch (error) {
        console.error('继续故事失败:', error);
        alert('继续故事失败，请重试');
    } finally {
        hideLoading();
    }
}

// 重置游戏
function resetGame() {
    currentStoryId = null;
    currentTurn = 1;
    setupScreen.classList.add('active');
    gameScreen.classList.remove('active');
    document.getElementById('opening-input').value = '';
    storyContent.innerHTML = '<p class="placeholder">等待故事开始...</p>';
    choicesContainer.innerHTML = '';
}

// 绑定事件
document.getElementById('start-btn').addEventListener('click', startStory);
document.getElementById('new-game-btn').addEventListener('click', resetGame);

console.log('前端已加载，API地址:', API_BASE);