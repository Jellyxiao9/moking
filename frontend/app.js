// API 配置
const API_BASE = 'http://localhost:8000';

// 全局状态
let currentStoryId = null;
let currentTurn = 1;

// 标签推荐相关变量
let selectedTags = [];
let currentWorldForTags = 'noir';

// DOM 元素
const setupScreen = document.getElementById('setup-screen');
const gameScreen = document.getElementById('game-screen');
const storyContent = document.getElementById('story-content');
const choicesContainer = document.getElementById('choices-container');
const turnIndicator = document.getElementById('turn-indicator');
const loadingOverlay = document.getElementById('loading-overlay');
const templateSelect = document.getElementById('template-select');

// 显示加载状态
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// 显示剧情文本（打字机效果）
async function displayStory(text, container) {
    container.innerHTML = '';
    const chars = text.split('');

    for (let i = 0; i < chars.length; i++) {
        const char = chars[i];
        if (char === '\n') {
            container.innerHTML += '<br>';
        } else {
            container.innerHTML += char;
        }
        storyContent.scrollTop = storyContent.scrollHeight;
        const delay = ['.', '。', '!', '！', '?', '？', '，', ','].includes(char) ? 80 : 30;
        await new Promise(resolve => setTimeout(resolve, delay));
    }
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

// 加载模板
async function loadTemplates(world) {
    if (!templateSelect) return;
    templateSelect.innerHTML = '<option value="">自定义开场</option>';
    
    try {
        const response = await fetch(`${API_BASE}/world/${world}/templates`);
        const data = await response.json();
        
        if (data.templates && data.templates.length > 0) {
            data.templates.forEach(template => {
                const option = document.createElement('option');
                option.value = template.opening;
                option.textContent = `${template.name} - ${template.description}`;
                templateSelect.appendChild(option);
            });
            console.log(`已加载 ${data.templates.length} 个模板`);
        }
    } catch (error) {
        console.log('模板加载失败:', error);
    }
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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ world: world, opening: opening })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        currentStoryId = data.story_id;
        currentTurn = 1;

        setupScreen.classList.remove('active');
        gameScreen.classList.add('active');

        hideLoading();
        await displayStory(data.content, storyContent);
        displayChoices(data.choices);
        turnIndicator.textContent = `第 ${currentTurn} 轮`;

    } catch (error) {
        console.error('开始故事失败:', error);
        hideLoading();
        alert('开始故事失败，请确保后端服务已启动');
    }
}

// 做出选择
async function makeChoice(choice) {
    if (!currentStoryId) return;

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/story/continue`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ story_id: currentStoryId, user_choice: choice })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        currentTurn = data.turn_number;

        hideLoading();
        await displayStory(data.content, storyContent);
        displayChoices(data.choices);
        turnIndicator.textContent = `第 ${currentTurn} 轮`;

    } catch (error) {
        console.error('继续故事失败:', error);
        hideLoading();
        alert('继续故事失败，请重试');
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

// 监听世界观变化
const worldSelect = document.getElementById('world-select');
if (worldSelect) {
    worldSelect.addEventListener('change', (e) => {
        // 清空选中的标签
        selectedTags = [];
        // 清空标签高亮
        document.querySelectorAll('.tag').forEach(tag => {
            tag.classList.remove('selected');
        });
        // 隐藏推荐区域
        const recContainer = document.getElementById('recommendations-container');
        if (recContainer) recContainer.style.display = 'none';
        // 重新加载标签
        loadTags();
        // 重新加载模板
        loadTemplates(e.target.value);
    });
}

// 监听模板选择变化
if (templateSelect) {
    templateSelect.addEventListener('change', (e) => {
        if (e.target.value) {
            document.getElementById('opening-input').value = e.target.value;
        }
    });
}

// 页面加载时加载默认模板
const initialWorld = document.getElementById('world-select').value;
loadTemplates(initialWorld);

// 加载标签（只加载当前世界观的标签）
async function loadTags() {
    const tagsContainer = document.getElementById('tags-container');
    if (!tagsContainer) return;
    
    const world = document.getElementById('world-select').value;
    
    tagsContainer.innerHTML = '<span class="tag-loading">加载标签中...</span>';
    
    try {
        // 获取当前世界观的所有模板
        const response = await fetch(`${API_BASE}/world/${world}/templates`);
        const data = await response.json();
        
        // 收集所有标签
        const allTags = new Set();
        data.templates.forEach(template => {
            if (template.tags) {
                template.tags.forEach(tag => allTags.add(tag));
            }
        });
        
        // 转换为数组并排序
        const tags = Array.from(allTags).sort();
        
        tagsContainer.innerHTML = '';
        if (tags.length === 0) {
            tagsContainer.innerHTML = '<span class="tag-loading">暂无标签</span>';
            return;
        }
        
        tags.forEach(tag => {
            const tagElement = document.createElement('span');
            tagElement.className = 'tag';
            tagElement.textContent = tag;
            tagElement.onclick = () => toggleTag(tag, tagElement);
            tagsContainer.appendChild(tagElement);
        });
        
    } catch (error) {
        console.error('加载标签失败:', error);
        tagsContainer.innerHTML = '<span class="tag-loading">加载标签失败</span>';
    }
}

// 切换标签选中状态
async function toggleTag(tag, element) {
    if (selectedTags.includes(tag)) {
        // 取消选中
        selectedTags = selectedTags.filter(t => t !== tag);
        element.classList.remove('selected');
    } else {
        // 选中
        selectedTags.push(tag);
        element.classList.add('selected');
    }
    
    // 如果选中了标签，获取推荐
    if (selectedTags.length > 0) {
        await getRecommendations();
    } else {
        // 没有选中标签，隐藏推荐区域
        document.getElementById('recommendations-container').style.display = 'none';
    }
}

// 获取推荐模板
async function getRecommendations() {
    if (selectedTags.length === 0) return;
    
    const world = document.getElementById('world-select').value;
    currentWorldForTags = world;
    
    try {
        const response = await fetch(`${API_BASE}/world/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                preferred_tags: selectedTags,
                world_id: world,
                limit: 3
            })
        });
        
        const data = await response.json();
        displayRecommendations(data.recommendations);
        
    } catch (error) {
        console.error('获取推荐失败:', error);
    }
}

// 显示推荐模板
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    const listContainer = document.getElementById('recommendations-list');
    
    if (!recommendations || recommendations.length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'block';
    listContainer.innerHTML = '';
    
    recommendations.forEach(rec => {
        const template = rec.template;
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.onclick = () => {
            // 点击推荐模板，填充开场
            document.getElementById('opening-input').value = template.opening;
            // 可选：自动选择这个模板
            if (templateSelect) {
                // 在模板下拉框中添加或选中
                const option = document.createElement('option');
                option.value = template.opening;
                option.textContent = `${template.name} - ${template.description} (推荐)`;
                templateSelect.appendChild(option);
                templateSelect.value = template.opening;
            }
        };
        
        item.innerHTML = `
            <div class="recommendation-name">
                ${template.name}
                <span class="recommendation-score">匹配度: ${rec.score}</span>
            </div>
            <div class="recommendation-desc">${template.description}</div>
            <div class="recommendation-tags">标签: ${template.tags.join(' · ')}</div>
        `;
        listContainer.appendChild(item);
    });
}

// 监听世界观变化时，刷新标签推荐
if (worldSelect) {
    const originalChange = worldSelect.onchange;
    worldSelect.addEventListener('change', () => {
        // 清空选中的标签
        selectedTags = [];
        // 重新加载标签（可选，标签是全局的，不需要重新加载）
        // 清除推荐区域
        document.getElementById('recommendations-container').style.display = 'none';
        // 清除标签高亮
        document.querySelectorAll('.tag').forEach(tag => {
            tag.classList.remove('selected');
        });
    });
}

// 页面加载时加载标签
loadTags();

// AI 生成新模板
async function generateTemplateByAI() {
    if (selectedTags.length === 0) {
        alert('请先选择至少一个标签');
        return;
    }
    
    const world = document.getElementById('world-select').value;
    
    // 显示加载状态
    const generateBtn = document.getElementById('ai-generate-btn');
    if (!generateBtn) return;
    
    const originalText = generateBtn.textContent;
    generateBtn.textContent = 'AI 生成中...';
    generateBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/world/generate-template`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                world_id: world,
                tags: selectedTags
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const template = await response.json();
        
        // 显示生成的模板
        displayAIGeneratedTemplate(template);
        
    } catch (error) {
        console.error('AI 生成失败:', error);
        alert('AI 生成失败，请重试');
    } finally {
        generateBtn.textContent = originalText;
        generateBtn.disabled = false;
    }
}

// 显示 AI 生成的模板
function displayAIGeneratedTemplate(template) {
    // 在推荐区域显示 AI 生成的模板
    const container = document.getElementById('recommendations-container');
    const listContainer = document.getElementById('recommendations-list');
    
    if (!container || !listContainer) return;
    
    container.style.display = 'block';
    
    // 创建 AI 生成模板的卡片
    const item = document.createElement('div');
    item.className = 'recommendation-item';
    item.style.borderLeftColor = '#ffaa44';
    item.style.background = 'rgba(255, 170, 68, 0.1)';
    item.onclick = () => {
        const openingInput = document.getElementById('opening-input');
        if (openingInput) {
            openingInput.value = template.opening;
        }
        // 可选：在模板下拉框中添加
        const templateSelect = document.getElementById('template-select');
        if (templateSelect) {
            const option = document.createElement('option');
            option.value = template.opening;
            option.textContent = `${template.name} - ${template.description} (AI生成)`;
            templateSelect.appendChild(option);
            templateSelect.value = template.opening;
        }
    };
    
    item.innerHTML = `
        <div class="recommendation-name">
            🤖 ${template.name}
            <span class="recommendation-score">AI 生成</span>
        </div>
        <div class="recommendation-desc">${template.description}</div>
        <div class="recommendation-tags">标签: ${template.tags.join(' · ')}</div>
    `;
    
    // 插入到推荐列表最前面
    if (listContainer.firstChild) {
        listContainer.insertBefore(item, listContainer.firstChild);
    } else {
        listContainer.appendChild(item);
    }
    
    // 添加提示
    const tip = document.createElement('div');
    tip.className = 'recommendation-tip';
    tip.style.fontSize = '12px';
    tip.style.color = '#ffaa44';
    tip.style.marginBottom = '10px';
    tip.innerHTML = '✨ AI 根据你选择的标签生成了新模板，点击使用';
    
    if (listContainer.firstChild && listContainer.firstChild !== item) {
        listContainer.insertBefore(tip, listContainer.firstChild);
    } else {
        listContainer.insertBefore(tip, item);
    }
}

// 绑定 AI 生成按钮（等待 DOM 加载完成）
document.addEventListener('DOMContentLoaded', () => {
    const aiGenerateBtn = document.getElementById('ai-generate-btn');
    if (aiGenerateBtn) {
        aiGenerateBtn.addEventListener('click', generateTemplateByAI);
    }
});

console.log('前端已加载，API地址:', API_BASE);