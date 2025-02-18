document.querySelector("form").addEventListener("submit", function(event) {
  event.preventDefault();
  
  const idLivro = document.getElementById("idLivro").value.trim();
  
  if (!idLivro) {
      alert("Por favor, insira um ID de livro válido.");
      return;
  }
  
  fetch("http://localhost:5000/buscarlivro", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: idLivro })
  })
  .then(response => response.json())
  .then(data => {
      if (data.erro) {
          alert(data.erro);
          return;
      }

      // Mostrar informações do livro
      document.querySelector("#infoLivro").style.display = "block"; // Exibe a seção de informações

      document.getElementById("tituloLivro").textContent = data.titulo || "Título não disponível";
      document.getElementById("autorLivro").textContent = data.autor || "Autor não disponível";
      document.getElementById("anoLivro").textContent = data.ano || "Ano não disponível";
      document.getElementById("disponibilidadeLivro").textContent = data.disponivel ? "Disponível" : "Indisponível";
  })
  .catch(error => {
      console.error("Erro: ", error);
      alert("Erro ao buscar o livro.");
  });
});
