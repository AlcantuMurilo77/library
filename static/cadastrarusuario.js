document.getElementById("cadastrarusuario").addEventListener("submit", function(event) {
    event.preventDefault(); // Impede o comportamento padrão de envio do formulário

    // Obtendo o valor do campo de nome de usuário
    const nomeUsuario = document.getElementById("nomeUsuario").value;

    // Checando se o nome do usuário foi preenchido
    if (!nomeUsuario) {
        alert("Por favor, preencha o nome do usuário.");
        return;
    }

    // Enviando a requisição POST para o Flask
    fetch('http://localhost:5000/cadastrarusuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Indica que estamos enviando JSON
        },
        body: JSON.stringify({
            nome_usuario: nomeUsuario, // Passando o nome do usuário no corpo da requisição
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        // Exibe a mensagem de sucesso ou erro
        alert(data.mensagem || data.erro);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao cadastrar usuário!');
    });
});
