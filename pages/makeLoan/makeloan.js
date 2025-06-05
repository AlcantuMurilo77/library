document.getElementById("makeLoan").addEventListener("submit", function(event) {
  event.preventDefault();

  const userId = document.getElementById("loanUser").value.trim();
  const bookId = document.getElementById("loanBook").value.trim();

  if (!userId || !bookId) {
      alert("Please enter all values.");
      return;
  }

  const data = {
      user_id: userId,
      book_id: bookId
  };

  fetch('http://localhost:5000/borrowbook', {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      if (data.erro) {
          alert(`Error: ${data.erro}`);
      } else {
          alert("Loan completed successfully!");
          document.getElementById("makeLoan").reset();
      }
  })
  .catch(error => {
      console.error("Error trying to make the loan:", error);
      alert("Failed to connect to the server.");
  });
});
