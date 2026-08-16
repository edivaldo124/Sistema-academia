const modal = document.getElementById('meuModal');
const input_senha = document.getElementById('senhausuario');
const icone_senha = document.getElementById('iconeSenha');

function abrirmodal(){
    modal.hidden = false;
    document.body.classList.add('modal-open');
    document.getElementById('inputnome').focus();
}

function fechar(){
    modal.hidden = true;
    document.body.classList.remove('modal-open');
}

function mostrarSenha(){
    if(input_senha.type === 'password'){
        input_senha.type = 'text';
        icone_senha.textContent = 'Ocultar';
        icone_senha.setAttribute('aria-label', 'Ocultar senha');
    } else {
        input_senha.type = 'password';
        icone_senha.textContent = 'Ver';
        icone_senha.setAttribute('aria-label', 'Mostrar senha');
    }
}

document.addEventListener('keydown', function (evento) {
    if (evento.key === 'Escape' && !modal.hidden) fechar();
});
