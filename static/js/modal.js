(() => {
    const dialog = document.getElementById('confirm-dialog');
    if (!dialog) return;

    const title = dialog.querySelector('#confirm-dialog-title');
    const message = dialog.querySelector('#confirm-dialog-message');
    const eyebrow = dialog.querySelector('#confirm-dialog-eyebrow');
    const accept = dialog.querySelector('[data-modal-accept]');
    const cancel = dialog.querySelector('[data-modal-cancel]');
    let pendingTarget = null;
    let previousFocus = null;

    function openModal(target) {
        pendingTarget = target;
        previousFocus = document.activeElement;
        title.textContent = target.dataset.modalTitle || 'Você tem certeza?';
        message.textContent = target.dataset.modalMessage || 'Revise esta ação antes de continuar.';
        eyebrow.textContent = target.dataset.modalEyebrow || 'Confirmar ação';
        accept.textContent = target.dataset.modalConfirm || 'Confirmar';
        dialog.dataset.variant = target.dataset.modalVariant || 'default';
        dialog.showModal();
        cancel.focus();
    }

    function closeModal() {
        dialog.close();
        if (previousFocus) previousFocus.focus();
        pendingTarget = null;
    }

    document.addEventListener('click', (event) => {
        const link = event.target.closest('a[data-confirm-modal]');
        if (!link) return;
        event.preventDefault();
        openModal(link);
    });

    document.addEventListener('submit', (event) => {
        const form = event.target.closest('form[data-confirm-modal]');
        if (!form || form.dataset.modalConfirmed === 'true') return;
        event.preventDefault();
        openModal(form);
    });

    cancel.addEventListener('click', closeModal);
    dialog.addEventListener('cancel', (event) => {
        event.preventDefault();
        closeModal();
    });
    dialog.addEventListener('click', (event) => {
        const box = dialog.getBoundingClientRect();
        const outside = event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
        if (outside) closeModal();
    });

    accept.addEventListener('click', () => {
        if (!pendingTarget) return;
        const target = pendingTarget;
        if (target.tagName === 'A') {
            window.location.assign(target.href);
            return;
        }
        target.dataset.modalConfirmed = 'true';
        accept.disabled = true;
        accept.textContent = target.dataset.loadingText || 'Processando…';
        target.requestSubmit();
    });
})();
