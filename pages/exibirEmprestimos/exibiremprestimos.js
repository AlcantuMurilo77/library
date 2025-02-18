 // Espera o evento de submit do formulário
 document.getElementById("buscaForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Evita o envio padrão do formulário

  // Pega o valor do ID do usuário inserido no input
  const idUsuario = document.getElementById("idUsuario").value;

  // Valida se o ID foi preenchido
  if (!idUsuario) {
      alert("Por favor, insira um ID de usuário.");
      return;
  }

  // Cria o objeto com o ID para enviar na requisição
  const dados = { id: idUsuario };

  // Faz a requisição para a API
  fetch('http://127.0.0.1:5000/exibirlivrosemprestadosporusuario', {
      method: 'POST', // Método POST para enviar o ID do usuário
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados) // Envia o ID do usuário no corpo da requisição
  })
  .then(response => response.json()) // Converte a resposta para JSON
  .then(data => {
      // Limpa a lista de empréstimos atual
      const listaEmprestimos = document.getElementById("listaEmprestimos");
      listaEmprestimos.innerHTML = '';

      // Se a resposta for bem-sucedida, popula a lista com os livros emprestados
      if (data.length > 0) {
          data.forEach(item => {
              const li = document.createElement("li");
              li.textContent = `${item.titulo_livro} - Empréstimo em: ${item.data_emprestimo} | Devolução em: ${item.data_devolucao}`;
              listaEmprestimos.appendChild(li);
          });
      } else {
          // Se não houver empréstimos, exibe uma mensagem
          const li = document.createElement("li");
          li.textContent = "Não há empréstimos pendentes para esse usuário.";
          listaEmprestimos.appendChild(li);
      }
  })
  .catch(error => {
      // Exibe um erro caso a requisição falhe
      console.error("Erro ao buscar empréstimos:", error);
      alert("Erro ao buscar empréstimos.");
  });
});