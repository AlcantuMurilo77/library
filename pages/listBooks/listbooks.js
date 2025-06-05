document.addEventListener("DOMContentLoaded", function () {
  fetch("http://localhost:5000/listbooks")
    .then(response => response.json())
    .then(data => {
      const bookTable = document.getElementById("bookTable");

      if (!data.length) {
        bookTable.innerHTML = "<tr><td colspan='5'>No books found.</td></tr>";
        return;
      }

      data.forEach(book => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${book.id}</td>
          <td>${book.title}</td>
          <td>${book.author}</td>
          <td>${book.year}</td>
          <td>${book.available ? "Yes" : "No"}</td>
        `;

        bookTable.appendChild(row);
      });
    })
    .catch(error => {
      console.error("Error fetching books:", error);
      document.getElementById("bookTable").innerHTML = "<tr><td colspan='5'>Failed to load books.</td></tr>";
    });
});
