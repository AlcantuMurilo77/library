document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  
  form.addEventListener("submit", async function (event) {
      event.preventDefault(); // Evita o recarregamento da página

      // Captura os valores dos campos do formulário
      const titulo = document.getElementById("tituloLivro").value.trim();
      const autor = document.getElementById("autorLivro").value.trim();
      const ano = document.getElementById("anoLivro").value.trim();

      if (!titulo || !autor || !ano) {
          alert("Por favor, preencha todos os campos.");
          return;
      }

      const livro = {
          titulo: titulo,
          autor: autor,
          ano: ano
      };

      try {
          const response = await fetch("http://127.0.0.1:5000/cadastrarlivro", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(livro)
          });

          const data = await response.json();
          
          if (response.ok) {
              alert("Livro cadastrado com sucesso!");
              form.reset(); // Limpa o formulário após o cadastro
          } else {
              alert("Erro ao cadastrar livro: " + data.erro || "Erro desconhecido");
          }
      } catch (error) {
          console.error("Erro na requisição:", error);
          alert("Falha ao conectar com o servidor.");
      }
  });
});
