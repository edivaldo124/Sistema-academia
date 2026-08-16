const gradePlanos = document.querySelector('.grid-planos');
const formulariosPlano = document.querySelectorAll('.form-contratar-plano');
const linkSair = document.getElementById('link-sair');

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

formulariosPlano.forEach(function (formulario) {
    formulario.addEventListener('submit', function (evento) {
        const nomePlano = formulario.dataset.planoNome;
        const confirmou = confirm(`Deseja contratar o plano ${nomePlano}?`);

        if (!confirmou) {
            evento.preventDefault();
            return;
        }

        const botao = formulario.querySelector('.btn-escolher');
        botao.disabled = true;
        botao.textContent = 'Processando...';
    });
});

if (linkSair) {
    linkSair.addEventListener('click', function (evento) {
        if (!confirm('Deseja realmente sair da sua conta?')) {
            evento.preventDefault();
        }
    });
}
