(() => {
    const digits = (value, limit) => value.replace(/\D/g, '').slice(0, limit);

    function cpf(value) {
        const number = digits(value, 11);
        return number
            .replace(/^(\d{3})(\d)/, '$1.$2')
            .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1-$2');
    }

    function phone(value) {
        const number = digits(value, 11);
        if (number.length <= 10) {
            return number
                .replace(/^(\d{2})(\d)/, '($1) $2')
                .replace(/(\d{4})(\d)/, '$1-$2');
        }
        return number
            .replace(/^(\d{2})(\d)/, '($1) $2')
            .replace(/(\d{5})(\d)/, '$1-$2');
    }

    const formatters = { cpf, phone };

    document.querySelectorAll('[data-mask]').forEach((input) => {
        const format = formatters[input.dataset.mask];
        if (!format) return;

        const apply = () => {
            const cursorAtEnd = input.selectionStart === input.value.length;
            input.value = format(input.value);
            if (cursorAtEnd) input.setSelectionRange(input.value.length, input.value.length);
        };

        input.addEventListener('input', apply);
        input.addEventListener('blur', apply);
        apply();
    });
})();
