// Agora usando Supabase diretamente (API base não é mais usada)
// const API_BASE = ... (removido)

// Estado da aplicação
let currentUser = null;
let allCoins = [];
let filteredCoins = [];

// Elementos do DOM
let coinsGrid, loginModal, coinModal, addCoinModal;

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    initializeElements();
    setupEventListeners();
    await loadCoins();
    checkAuthStatus();
});

function initializeElements() {
    coinsGrid = document.querySelector('.coins-grid');
    loginModal = document.getElementById('loginModal');
    coinModal = document.getElementById('coinModal');
    addCoinModal = document.getElementById('addCoinModal');
}

function setupEventListeners() {
    // Botões de login/logout
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const addCoinBtn = document.getElementById('addCoinBtn');
    
    if (loginBtn) loginBtn.addEventListener('click', showLoginModal);
    if (logoutBtn) logoutBtn.addEventListener('click', logout);
    if (addCoinBtn) addCoinBtn.addEventListener('click', showAddCoinModal);
    
    // Forms
    const loginForm = document.getElementById('loginForm');
    const addCoinForm = document.getElementById('addCoinForm');
    
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (addCoinForm) addCoinForm.addEventListener('submit', handleAddCoin);
    
    // Filtros
    setupFilters();
}

// === FUNÇÕES DE API ===
async function loadCoins() {
    if (!window.supabaseClient) {
        showError('Supabase não inicializado');
        return;
    }
    try {
        showLoading(true);
        const { data, error } = await supabaseClient
            .from('coins')
            .select('id,name,period,region,material,denomination,historia,contexto,referencia,image_front,image_back')
            .order('id');
        if (error) throw error;
        allCoins = data || [];
        filteredCoins = [...allCoins];
        renderCoins(filteredCoins);
        updateFilters();
    } catch (err) {
        console.error('Erro Supabase loadCoins:', err);
        showError('Erro ao carregar moedas: ' + err.message);
        allCoins = [];
        filteredCoins = [];
        renderCoins(filteredCoins);
    } finally {
        showLoading(false);
    }
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('token', data.token);
            currentUser = { username };
            updateAuthUI();
            hideModal(loginModal);
            showSuccess('Login realizado com sucesso!');
        } else {
            showError(data.message || 'Credenciais inválidas');
        }
        
        return data;
    } catch (error) {
        console.error('Erro no login:', error);
        showError('Erro ao fazer login. Tente novamente.');
    }
}

async function addCoin(coinData) {
    try {
        const { data, error } = await supabaseClient.from('coins').insert([coinData]).select();
        if (error) throw error;
        showSuccess('Moeda adicionada!');
        hideModal(addCoinModal);
        await loadCoins();
        return data?.[0];
    } catch (err) {
        console.error('Erro addCoin:', err);
        showError('Erro ao adicionar: ' + err.message);
    }
}

async function updateCoin(coinId, coinData) {
    try {
        const { data, error } = await supabaseClient
            .from('coins')
            .update(coinData)
            .eq('id', coinId)
            .select();
        if (error) throw error;
        showSuccess('Moeda atualizada!');
        hideModal(addCoinModal);
        await loadCoins();
        return data?.[0];
    } catch (err) {
        console.error('Erro updateCoin:', err);
        showError('Erro ao atualizar: ' + err.message);
    }
}

async function deleteCoin(coinId) {
    if (!confirm('Tem certeza que deseja excluir esta moeda?')) return;
    try {
        const { error } = await supabaseClient.from('coins').delete().eq('id', coinId);
        if (error) throw error;
        showSuccess('Moeda excluída!');
        await loadCoins();
    } catch (err) {
        console.error('Erro deleteCoin:', err);
        showError('Erro ao excluir: ' + err.message);
    }
}

// === FUNÇÕES DE UI ===
function renderCoins(coins) {
    if (!coinsGrid) return;
    
    if (coins.length === 0) {
        coinsGrid.innerHTML = '<p class="no-results">Nenhuma moeda encontrada.</p>';
        return;
    }
    
    coinsGrid.innerHTML = coins.map(coin => `
        <article class="coin-card" data-coin-id="${coin.id}">
            <div class="coin-image-container">
                <img src="${coin.image_front || 'https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400'}" 
                     alt="${coin.name}" 
                     class="coin-image"
                     onerror="this.src='https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400'">
            </div>
            <div class="coin-info">
                <h3 class="coin-title">${coin.name}</h3>
                <p class="coin-period">${coin.period || 'Período não informado'}</p>
                <p class="coin-region">${coin.region || 'Região não informada'}</p>
                <p class="coin-material">${coin.material || 'Material não informado'}</p>
                ${currentUser ? `
                    <div class="coin-actions">
                        <button onclick="editCoin(${coin.id})" class="btn-edit">✏️</button>
                        <button onclick="deleteCoin(${coin.id})" class="btn-delete">🗑️</button>
                    </div>
                ` : ''}
            </div>
        </article>
    `).join('');
    
    // Adicionar listeners para os cards
    document.querySelectorAll('.coin-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('.coin-actions')) return; // Não abrir modal se clicou em ação
            const coinId = parseInt(card.dataset.coinId);
            const coin = coins.find(c => c.id === coinId);
            if (coin) showCoinModal(coin);
        });
    });
}

function showCoinModal(coin) {
    if (!coinModal) return;
    
    // Atualizar conteúdo do modal
    const modalContent = coinModal.querySelector('.modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h2>${coin.name}</h2>
            <button class="close-modal" onclick="hideModal(coinModal)">&times;</button>
        </div>
        <div class="modal-body">
            <div class="coin-tabs">
                <button class="tab-btn active" data-tab="detalhes">Detalhes</button>
                <button class="tab-btn" data-tab="historia">História</button>
                <button class="tab-btn" data-tab="contexto">Contexto</button>
                <button class="tab-btn" data-tab="imagens">Imagens</button>
            </div>
            <div class="tab-content">
                <div class="tab-pane active" data-tab="detalhes">
                    <div class="coin-details">
                        <p><strong>Período:</strong> ${coin.period || 'Não informado'}</p>
                        <p><strong>Região:</strong> ${coin.region || 'Não informado'}</p>
                        <p><strong>Material:</strong> ${coin.material || 'Não informado'}</p>
                        <p><strong>Denominação:</strong> ${coin.denomination || 'Não informado'}</p>
                        <p><strong>Ano:</strong> ${coin.year || 'Não informado'}</p>
                        <p><strong>Descrição:</strong> ${coin.description || 'Sem descrição'}</p>
                    </div>
                </div>
                <div class="tab-pane" data-tab="historia">
                    <p>${coin.historia || 'História não disponível'}</p>
                </div>
                <div class="tab-pane" data-tab="contexto">
                    <p>${coin.contexto || 'Contexto não disponível'}</p>
                </div>
                <div class="tab-pane" data-tab="imagens">
                    <div class="coin-images">
                        <div class="image-container">
                            <h4>Cara</h4>
                            <img src="${coin.image_front || 'https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400'}" alt="Cara da moeda">
                        </div>
                        <div class="image-container">
                            <h4>Coroa</h4>
                            <img src="${coin.image_back || 'https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400'}" alt="Coroa da moeda">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Configurar abas
    setupTabs();
    
    coinModal.style.display = 'flex';
}

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            // Remover classe active de todos
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // Adicionar classe active aos selecionados
            btn.classList.add('active');
            document.querySelector(`[data-tab="${tabId}"].tab-pane`).classList.add('active');
        });
    });
}

function setupFilters() {
    // Implementar filtros baseados nos dados reais
    updateFilters();
}

function updateFilters() {
    const filterContainer = document.querySelector('.filters');
    if (!filterContainer || allCoins.length === 0) return;
    
    // Extrair valores únicos para filtros
    const periods = [...new Set(allCoins.map(coin => coin.period).filter(Boolean))];
    const materials = [...new Set(allCoins.map(coin => coin.material).filter(Boolean))];
    const regions = [...new Set(allCoins.map(coin => coin.region).filter(Boolean))];
    
    filterContainer.innerHTML = `
        <h3>Filtros</h3>
        <div class="filter-section">
            <h4>Período</h4>
            ${periods.map(period => `
                <label>
                    <input type="checkbox" name="period" value="${period}"> ${period}
                </label>
            `).join('')}
        </div>
        <div class="filter-section">
            <h4>Material</h4>
            ${materials.map(material => `
                <label>
                    <input type="checkbox" name="material" value="${material}"> ${material}
                </label>
            `).join('')}
        </div>
        <div class="filter-section">
            <h4>Região</h4>
            ${regions.map(region => `
                <label>
                    <input type="checkbox" name="region" value="${region}"> ${region}
                </label>
            `).join('')}
        </div>
        <button id="clearFilters" class="btn-secondary">Limpar Filtros</button>
    `;
    
    // Adicionar listeners para filtros
    const filterInputs = filterContainer.querySelectorAll('input[type="checkbox"]');
    filterInputs.forEach(input => {
        input.addEventListener('change', applyFilters);
    });
    
    document.getElementById('clearFilters')?.addEventListener('click', clearFilters);
}

function applyFilters() {
    const filters = {
        period: [],
        material: [],
        region: []
    };
    
    // Coletar filtros selecionados
    document.querySelectorAll('.filters input[type="checkbox"]:checked').forEach(input => {
        filters[input.name].push(input.value);
    });
    
    // Aplicar filtros
    filteredCoins = allCoins.filter(coin => {
        return (filters.period.length === 0 || filters.period.includes(coin.period)) &&
               (filters.material.length === 0 || filters.material.includes(coin.material)) &&
               (filters.region.length === 0 || filters.region.includes(coin.region));
    });
    
    renderCoins(filteredCoins);
}

function clearFilters() {
    document.querySelectorAll('.filters input[type="checkbox"]').forEach(input => {
        input.checked = false;
    });
    filteredCoins = [...allCoins];
    renderCoins(filteredCoins);
}

// === FUNÇÕES DE AUTENTICAÇÃO ===
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    if (token) {
        // Simular usuário logado (em produção, validar token)
        currentUser = { username: 'admin' };
        updateAuthUI();
    }
}

function updateAuthUI() {
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const addCoinBtn = document.getElementById('addCoinBtn');
    
    if (currentUser) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        if (addCoinBtn) addCoinBtn.style.display = 'inline-block';
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (addCoinBtn) addCoinBtn.style.display = 'none';
    }
    
    // Re-renderizar moedas para mostrar/ocultar botões de ação
    renderCoins(filteredCoins);
}

function showLoginModal() {
    if (loginModal) loginModal.style.display = 'flex';
}

function logout() {
    localStorage.removeItem('token');
    currentUser = null;
    updateAuthUI();
    showSuccess('Logout realizado com sucesso!');
}

function showAddCoinModal() {
    if (addCoinModal) {
        // Limpar o formulário
        const form = addCoinModal.querySelector('form');
        if (form) {
            form.reset();
            delete form.dataset.editingCoinId;
            
            // Restaurar título e botão para modo de adição
            const modalTitle = addCoinModal.querySelector('.modal-header h2');
            if (modalTitle) modalTitle.textContent = 'Adicionar Moeda';
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn) submitBtn.textContent = 'Adicionar Moeda';
        }
        addCoinModal.style.display = 'flex';
    }
}

// === HANDLERS DE EVENTOS ===
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const username = formData.get('username');
    const password = formData.get('password');
    
    await login(username, password);
}

async function handleAddCoin(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    const coinData = {
        name: formData.get('name'),
        period: formData.get('period'),
        region: formData.get('region'),
        material: formData.get('material'),
        denomination: formData.get('denomination'),
        year: formData.get('year'),
        description: formData.get('description'),
        historia: formData.get('historia'),
        contexto: formData.get('contexto'),
        referencia: formData.get('referencia'),
        image_front: formData.get('image_front'),
        image_back: formData.get('image_back')
    };
    
    // Verificar se estamos editando uma moeda existente
    const editingCoinId = form.dataset.editingCoinId;
    if (editingCoinId) {
        await updateCoin(parseInt(editingCoinId), coinData);
        // Limpar o estado de edição
        delete form.dataset.editingCoinId;
        const modalTitle = addCoinModal.querySelector('.modal-header h2');
        if (modalTitle) modalTitle.textContent = 'Adicionar Moeda';
        const submitBtn = form.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.textContent = 'Adicionar Moeda';
    } else {
        await addCoin(coinData);
    }
}

// === FUNÇÕES UTILITÁRIAS ===
function hideModal(modal) {
    if (modal) modal.style.display = 'none';
}

function showLoading(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = show ? 'block' : 'none';
    }
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    // Criar notificação temporária
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Expor funções globalmente para uso inline
window.deleteCoin = deleteCoin;
window.editCoin = function(coinId) {
    const coin = allCoins.find(c => c.id === coinId);
    if (!coin) {
        showError('Moeda não encontrada');
        return;
    }
    
    // Preencher o formulário de adicionar com os dados da moeda
    if (addCoinModal) {
        const form = addCoinModal.querySelector('form');
        if (form) {
            form.querySelector('[name="name"]').value = coin.name || '';
            form.querySelector('[name="period"]').value = coin.period || '';
            form.querySelector('[name="region"]').value = coin.region || '';
            form.querySelector('[name="material"]').value = coin.material || '';
            form.querySelector('[name="denomination"]').value = coin.denomination || '';
            form.querySelector('[name="historia"]').value = coin.historia || '';
            form.querySelector('[name="contexto"]').value = coin.contexto || '';
            form.querySelector('[name="referencia"]').value = coin.referencia || '';
            form.querySelector('[name="image_front"]').value = coin.image_front || '';
            form.querySelector('[name="image_back"]').value = coin.image_back || '';
            
            // Alterar o título e comportamento do modal para edição
            const modalTitle = addCoinModal.querySelector('.modal-header h2');
            if (modalTitle) modalTitle.textContent = 'Editar Moeda';
            
            // Remover listener anterior e adicionar novo para edição
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn) submitBtn.textContent = 'Atualizar Moeda';
            
            // Guardar ID da moeda sendo editada
            form.dataset.editingCoinId = coinId;
            
            showModal(addCoinModal);
        }
    }
};
window.hideModal = hideModal;