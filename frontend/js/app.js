import { sampleCoins } from './data.js';

// Renderizar cards de moedas
function renderCoinCard(coin) {
    return `
        <article class="coin-card" data-coin-id="${coin.id}">
            <img src="${coin.image}" alt="${coin.name}" class="coin-image">
            <div class="coin-info">
                <h3>${coin.name}</h3>
                <p>${coin.period}</p>
                <p>${coin.country}</p>
                <p>${coin.metal}</p>
            </div>
        </article>
    `;
}

// Renderizar filtros
function renderFilters() {
    const filterSection = document.querySelector('.filters');
    filterSection.innerHTML = `
        <h2>Filtros</h2>
        <section>
            <h3>Período Histórico</h3>
            <label>
                <input type="checkbox" value="ancient"> Roma Antiga
            </label>
            <label>
                <input type="checkbox" value="medieval"> Medieval
            </label>
        </section>
        <section>
            <h3>Metal</h3>
            <label>
                <input type="checkbox" value="gold"> Ouro
            </label>
            <label>
                <input type="checkbox" value="silver"> Prata
            </label>
        </section>
    `;
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Renderizar moedas
    const coinsGrid = document.querySelector('.coins-grid');
    coinsGrid.innerHTML = sampleCoins.map(renderCoinCard).join('');

    // Renderizar filtros
    renderFilters();

    // Adicionar listeners
    document.querySelectorAll('.coin-card').forEach(card => {
        card.addEventListener('click', () => {
            const coinId = card.dataset.coinId;
            const coin = sampleCoins.find(c => c.id == coinId);
            showModal(coin);
        });
    });
});

// Função para mostrar modal
function showModal(coin) {
    const modal = document.getElementById('coinModal');
    modal.hidden = false;
    
    const content = modal.querySelector('.tab-content');
    content.innerHTML = `
        <div class="tab-pane active" data-tab="historia">
            <h2>${coin.name}</h2>
            <p>${coin.description}</p>
        </div>
    `;
}
export const sampleCoins = [
    {
        id: 1,
        name: "Denário Romano",
        period: "27 AC - 14 DC",
        country: "Império Romano",
        metal: "Prata",
        image: "https://example.com/coin1.jpg", // Substituir por imagem real
        description: "Moeda do período de Augusto..."
    },
    {
        id: 2,
        name: "Shekel Hebreu",
        period: "66-70 DC",
        country: "Judéia Antiga",
        metal: "Prata",
        image: "https://example.com/coin2.jpg", // Substituir por imagem real
        description: "Moeda da Revolta Judaica..."
    },
    // Adicione mais moedas de exemplo
];