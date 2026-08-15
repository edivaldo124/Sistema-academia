const modal = document.getElementById('meuModal');
const input_senha = document.getElementById('senhausuario');
const icone_senha = document.getElementById('iconeSenha');

function abrirmodal(){
    modal.style.display = 'block';
}

function fechar(){
    modal.style.display = 'none';
}

function mostrarSenha() {
    const senhaVisivel = input_senha.type === 'password';

    input_senha.type = senhaVisivel ? 'text' : 'password';
    icone_senha.classList.toggle('senha-visivel', senhaVisivel);
    icone_senha.setAttribute('aria-pressed', String(senhaVisivel));
    icone_senha.setAttribute('aria-label', senhaVisivel ? 'Ocultar senha' : 'Mostrar senha');
}
