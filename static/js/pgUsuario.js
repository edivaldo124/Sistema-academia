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

const statusMensalidade = document.getElementById('statusMensalidade');

if (statusMensalidade) {
    const status = statusMensalidade.textContent.trim().toLowerCase();

    if (status === 'em dia') {
        statusMensalidade.classList.add('status-em-dia');
    } else if (status === 'pendente') {
        statusMensalidade.classList.add('status-pendente');
    } else if (status === 'inativo') {
        statusMensalidade.classList.add('status-inativo');
    }
}
const dataVencimento = document.getElementById('dataVencimento');
const contagemVencimento = document.getElementById('contagemVencimento');

if (dataVencimento && contagemVencimento) {
    const data = dataVencimento.dataset.vencimento;
    const partes = data.split('-');

    const ano = Number(partes[0]);
    const mes = Number(partes[1]) - 1;
    const dia = Number(partes[2]);

    const vencimento = new Date(ano, mes, dia);
    const hoje = new Date();

    hoje.setHours(0, 0, 0, 0);

    const umDia = 1000 * 60 * 60 * 24;
    const diasRestantes = Math.ceil((vencimento - hoje) / umDia);

    if (diasRestantes > 1) {
        contagemVencimento.textContent =
            `Faltam ${diasRestantes} dias para o vencimento.`;

        contagemVencimento.classList.add('vencimento-normal');
    } else if (diasRestantes === 1) {
        contagemVencimento.textContent = 'O plano vence amanhã.';

        contagemVencimento.classList.add('vencimento-proximo');
    } else if (diasRestantes === 0) {
        contagemVencimento.textContent = 'O plano vence hoje.';

        contagemVencimento.classList.add('vencimento-proximo');
    } else {
        contagemVencimento.textContent =
            `Plano vencido há ${Math.abs(diasRestantes)} dias.`;

        contagemVencimento.classList.add('vencimento-vencido');
    }
}

