document.getElementById("registerUser").addEventListener("submit", function(event) {
    event.preventDefault();

    const userName = document.getElementById("userName").value;

    if (!userName) {
        alert("Please fill in the user name.");
        return;
    }

    fetch('http://localhost:5000/cadastrarusuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome_usuario: userName,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        alert(data.mensagem || data.erro);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error registering user!');
    });
});
