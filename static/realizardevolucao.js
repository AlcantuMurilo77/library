document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  
  form.addEventListener("submit", async function (event) {
      event.preventDefault(); // Impede o envio padrão do formulário
      
      const idUsuario = document.getElementById("idUsuario").value.trim();
      const idLivro = document.getElementById("idLivro").value.trim();
      
      if (!idUsuario || !idLivro) {
          alert("Por favor, preencha ambos os campos.");
          return;
      }
      
      const requestData = {
          id_usuario: idUsuario,
          id_livro: idLivro
      };
      
      try {
          const response = await fetch("http://127.0.0.1:5000/devolverlivro", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(requestData)
          });
          
          const responseData = await response.json();
          
          if (response.ok) {
              alert("Devolução realizada com sucesso!");
          } else {
              alert("Erro: " + responseData.erro);
          }
      } catch (error) {
          console.error("Erro ao conectar com o servidor:", error);
          alert("Erro ao conectar com o servidor. Tente novamente mais tarde.");
      }
  });
});
