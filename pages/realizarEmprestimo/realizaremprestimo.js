document.getElementById("realizaEmprestimo").addEventListener("submit", function(event) {
  event.preventDefault();

  const idUsuario = document.getElementById("usuarioEmprestimo").value.trim();
  const idLivro = document.getElementById("livroEmprestimo").value.trim();

  if (!idUsuario || !idLivro) {
      alert("Por favor, insira todos os valores.");
      return;
  }

  const dados = {
      id_usuario: idUsuario,
      id_livro: idLivro
  };

  fetch('http://localhost:5000/emprestarlivro', {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
  })
  .then((response) => response.json())
  .then(data => {
      if (data.erro) {
          alert(`Erro: ${data.erro}`);
      } else {
          alert("Empréstimo realizado com sucesso!");
          document.getElementById("realizaEmprestimo").reset();
      }
  })
  .catch(error => {
      console.error("Erro ao tentar realizar o empréstimo:", error);
      alert("Erro ao conectar com o servidor.");
  });
});
