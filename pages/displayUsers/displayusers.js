document.addEventListener("DOMContentLoaded", function () {
  fetch('http://localhost:5000/listusers')
    .then(response => response.json())
    .then(data => {
      const userList = document.getElementById("userList");
      userList.innerHTML = "";

      data.forEach(user => {
        let li = document.createElement("li");
        li.textContent = `ID: ${user.id} - Name: ${user.name}`;
        userList.appendChild(li);
      });
    })
    .catch(error => console.error("Error fetching users: ", error));
});
