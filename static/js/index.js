const modal = document.getElementById('meuModal');
const input_senha = document.getElementById('senhausuario');
const icone_senha = document.getElementById('iconeSenha');

function abrirmodal(){
    modal.style.display = 'block';
}

function fechar(){
    modal.style.display = 'none';
}

function mostrarSenha(){
    if(input_senha.type === 'password'){
        input_senha.type = 'text';
        icone_senha.textContent = '🙈';
        icone_senha.setAttribute('aria-label', 'Ocultar senha');
    } else {
        input_senha.type = 'password';
        icone_senha.textContent = '👁️';
        icone_senha.setAttribute('aria-label', 'Mostrar senha');
    }
}
