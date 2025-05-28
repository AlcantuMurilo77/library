document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  
  form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const title = document.getElementById("bookTitle").value.trim();
      const author = document.getElementById("bookAuthor").value.trim();
      const year = document.getElementById("bookYear").value.trim();

      if (!title || !author || !year) {
          alert("Please fill in all fields.");
          return;
      }

      const book = {
          titulo: title,
          autor: author,
          ano: year
      };

      try {
          const response = await fetch("http://127.0.0.1:5000/cadastrarlivro", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(book)
          });

          const data = await response.json();
          
          if (response.ok) {
              alert("Book registered successfully!");
              form.reset();
          } else {
              alert("Error registering book: " + (data.erro || "Unknown error"));
          }
      } catch (error) {
          console.error("Request error:", error);
          alert("Failed to connect to the server.");
      }
  });
});
