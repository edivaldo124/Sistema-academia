const campoBusca = document.getElementById('busca-aluno');
const linhasDeAlunos = document.querySelectorAll('.aluno-item');
const contadorAlunos = document.getElementById('contador-alunos');
const avisoSemResultados = document.getElementById('sem-resultados');
const formularioPlano = document.getElementById('form-plano');
const campoPreco = document.getElementById('preco-plano');
const campoDuracao = document.getElementById('duracao-dias');

const formatadorDePreco = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

function normalizarTexto(texto) {
    return texto
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase();
}

function atualizarListaDeAlunos() {
    const busca = normalizarTexto(campoBusca.value.trim());
    let encontrados = 0;

    linhasDeAlunos.forEach(function (linha) {
        const nome = normalizarTexto(linha.dataset.nome);
        const deveAparecer = nome.includes(busca);
        linha.hidden = !deveAparecer;

        if (deveAparecer) {
            encontrados += 1;
        }
    });

    contadorAlunos.textContent = encontrados === 1
        ? '1 aluno'
        : `${encontrados} alunos`;

    if (avisoSemResultados && linhasDeAlunos.length > 0) {
        avisoSemResultados.hidden = encontrados !== 0;
    }
}

if (campoBusca) {
    campoBusca.addEventListener('input', atualizarListaDeAlunos);
}

document.querySelectorAll('.preco-plano').forEach(function (preco) {
    const valor = Number(preco.dataset.preco);

    if (!Number.isNaN(valor)) {
        preco.textContent = formatadorDePreco.format(valor);
    }
});

if (formularioPlano) {
    campoPreco.addEventListener('input', function () {
        campoPreco.setCustomValidity('');
    });

    campoDuracao.addEventListener('input', function () {
        campoDuracao.setCustomValidity('');
    });

    formularioPlano.addEventListener('submit', function (evento) {
        const preco = Number(campoPreco.value.trim().replace(',', '.'));
        const duracao = Number(campoDuracao.value);

        if (!Number.isFinite(preco) || preco <= 0) {
            evento.preventDefault();
            campoPreco.setCustomValidity('Informe um preço maior que zero.');
            campoPreco.reportValidity();
            return;
        }

        if (!Number.isInteger(duracao) || duracao <= 0) {
            evento.preventDefault();
            campoDuracao.setCustomValidity('Informe uma duração maior que zero.');
            campoDuracao.reportValidity();
            return;
        }

        campoPreco.value = preco.toFixed(2);

        const botao = formularioPlano.querySelector('.btn-cadastrar');
        botao.disabled = true;
        botao.textContent = 'Cadastrando...';
    });
}
