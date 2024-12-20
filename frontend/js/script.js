const botaoAtivar = document.getElementById("botao-ativar");
const mensagem = document.getElementById("mensagem");

let capturando = false;

// Função para iniciar/parar a gravação
botaoAtivar.addEventListener("click", () => {
    if (!capturando) {
        iniciarGravacao();
    } else {
        pararGravacao();
    }
});

function iniciarGravacao() {
    capturando = true;
    mensagem.innerText = "Prontinho! Pode falar";
    botaoAtivar.classList.remove("botao-play");
    botaoAtivar.classList.add("botao-gravando");
}

function pararGravacao() {
    capturando = false;
    mensagem.innerText = "Aperte para falar com a assistente";
    botaoAtivar.classList.remove("botao-gravando");
    botaoAtivar.classList.add("botao-play");

    const comando = "teste";
    processarComando(comando);
}

function processarComando(comando) {
    fetch("http://localhost:5000/assistente/ativar", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })    
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        alert(data.message);
    })
    .catch((error) => {
        console.error("Erro ao processar o comando:", error);
    });
}