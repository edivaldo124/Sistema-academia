const gradePlanos = document.querySelector('.grid-planos');

const formatadorDePreco = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

document.querySelectorAll('[data-preco]').forEach(function (preco) {
    const valor = Number(preco.dataset.preco);

    if (!Number.isNaN(valor)) {
        preco.textContent = formatadorDePreco.format(valor);
    }
});

if (gradePlanos) {
    const planoAtual = gradePlanos.dataset.planoAtual;

    document.querySelectorAll('.card-plano').forEach(function (card) {
        if (planoAtual && card.dataset.planoId === planoAtual) {
            const botao = card.querySelector('.btn-escolher');
            card.classList.add('plano-atual');
            botao.disabled = true;
            botao.textContent = 'Plano atual';
        }
    });
}
