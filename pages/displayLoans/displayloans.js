document.getElementById("searchForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const userId = document.getElementById("userId").value.trim();

  if (!userId) {
      alert("Please enter a user ID.");
      return;
  }

  const data = { id: userId };

  fetch('http://127.0.0.1:5000/userloans', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(loans => {
      const loansList = document.getElementById("loansList");
      loansList.innerHTML = '';

      if (loans.length > 0) {
          loans.forEach(loan => {
              const li = document.createElement("li");
              li.textContent = `${loan.book_title} - Loan Date: ${loan.loan_date} | Return Date: ${loan.return_date}`;
              loansList.appendChild(li);
          });
      } else {
          const li = document.createElement("li");
          li.textContent = "No pending loans found for this user.";
          loansList.appendChild(li);
      }
  })
  .catch(error => {
      console.error("Error fetching loans:", error);
      alert("Failed to fetch loans.");
  });
});
