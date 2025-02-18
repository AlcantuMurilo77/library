document.addEventListener("DOMContentLoaded", function () {
  fetch('http://localhost:5000/listarusuarios')
  .then(response => response.json())
  .then(data => {
    const listaUsuarios = document.getElementById("listausuarios");
    listaUsuarios.innerHTML = "";

    data.forEach(usuario => {
      let li = document.createElement("li");
      li.textContent = `ID: ${usuario.id} - Nome: ${usuario.nome}`;
      listaUsuarios.appendChild(li);
    });
  })
  .catch(error => console.error("Erro ao buscar usuários: ", error));
});