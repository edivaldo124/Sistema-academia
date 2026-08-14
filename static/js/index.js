const input_nome = document.getElementById('inputnome');
const modal = document.getElementById('meuModal');
const msg_alerta = document.getElementById('msgalerta');

function abrirmodal(){
    modal.style.display = 'block';
}

function fechar(){
    modal.style.display = 'none';
}

function alertardoidao(){
    alert("corre que o homi ta doido");
}

function mudou(){

    if(input_nome.value === ""){
        msg_alerta.style.color = "red";
        msg_alerta.style.fontSize = "8px";
        msg_alerta.textContent = "Falta você colocar algo";
    }
}