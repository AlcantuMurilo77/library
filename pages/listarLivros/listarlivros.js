document.addEventListener("DOMContentLoaded", function () {
  fetch("http://localhost:5000/listarlivros")
      .then(response => response.json())
      .then(data => {
          const tabelaLivros = document.getElementById("tabelaLivros");

          if (data.length === 0) {
              tabelaLivros.innerHTML = "<tr><td colspan='5'>Nenhum livro encontrado.</td></tr>";
              return;
          }

          data.forEach(livro => {
              const row = document.createElement("tr");

              row.innerHTML = `
                  <td>${livro.id}</td>
                  <td>${livro.titulo}</td>
                  <td>${livro.autor}</td>
                  <td>${livro.ano}</td>
                  <td>${livro.disponivel}</td>
              `;

              tabelaLivros.appendChild(row);
          });
      })
      .catch(error => {
          console.error("Erro ao buscar livros:", error);
          document.getElementById("tabelaLivros").innerHTML = "<tr><td colspan='5'>Erro ao carregar os livros.</td></tr>";
      });
});
