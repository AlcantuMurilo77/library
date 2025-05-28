document.querySelector("form").addEventListener("submit", function(event) {
  event.preventDefault();

  const bookId = document.getElementById("bookId").value.trim();

  if (!bookId) {
      alert("Please enter a valid book ID.");
      return;
  }

  fetch("http://localhost:5000/searchbook", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: bookId })
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          alert(data.error);
          return;
      }

      document.querySelector("#bookInfo").style.display = "block";

      document.getElementById("bookTitle").textContent = data.title || "Title not available";
      document.getElementById("bookAuthor").textContent = data.author || "Author not available";
      document.getElementById("bookYear").textContent = data.year || "Year not available";
      document.getElementById("bookAvailability").textContent = data.available ? "Available" : "Unavailable";
  })
  .catch(error => {
      console.error("Error: ", error);
      alert("Error searching for the book.");
  });
});
