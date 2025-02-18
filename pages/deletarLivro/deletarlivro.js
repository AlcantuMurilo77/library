document.getElementById("deletarlivro").addEventListener("submit", function(event){
  event.preventDefault();

  const idLivro = document.getElementById("idLivro").value; 

  if (!idLivro){
    alert("Por favor, preencha o nome do usuário.");
    return;
  }

  fetch('http://localhost:5000/deletalivro', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify ({
      id: idLivro,
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Resposta do servidor: ', data);
    alert(data.mensagem || data.erro);
  })
  .catch(error => {
    console.error('Erro: ', error);
    alert('Erro ao deletar Livro!')
  })




})