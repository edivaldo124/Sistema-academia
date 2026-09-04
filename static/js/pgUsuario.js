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

const dialogs = document.querySelectorAll('.sheet-dialog');
document.addEventListener('click', function (event) {
    const opener = event.target.closest('[data-open-dialog]');
    if (opener) document.getElementById(opener.dataset.openDialog)?.showModal();

    const closeButton = event.target.closest('[data-close-dialog]');
    if (closeButton) closeButton.closest('dialog')?.close();

    const detailsButton = event.target.closest('[data-payment-details]');
    if (detailsButton) {
        const dialog = document.getElementById('payment-dialog');
        ['plan', 'value', 'due', 'paid', 'status', 'method'].forEach(function (field) {
            const target = dialog.querySelector(`[data-detail="${field}"]`);
            if (target) target.textContent = detailsButton.dataset[field] || '—';
        });
        dialog.showModal();
    }
});

dialogs.forEach(function (dialog) {
    dialog.addEventListener('click', function (event) {
        const bounds = dialog.getBoundingClientRect();
        if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    });
});

const photoInput = document.getElementById('foto-perfil');
if (photoInput) photoInput.addEventListener('change', function () {
    const file = photoInput.files[0];
    if (!file) return;
    const image = document.createElement('img');
    image.alt = 'Prévia da nova foto';
    image.src = URL.createObjectURL(file);
    image.onload = () => URL.revokeObjectURL(image.src);
    document.getElementById('photo-preview').replaceChildren(image);
});
