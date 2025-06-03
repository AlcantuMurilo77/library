document.getElementById("deleteBook").addEventListener("submit", function(event) {
  event.preventDefault();

  const bookId = document.getElementById("bookId").value.trim();

  if (!bookId) {
    alert("Please enter the book ID.");
    return;
  }

  fetch('http://localhost:5000/deletebook', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: bookId,
    }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Server response:', data);
    alert(data.message || data.error);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to delete the book!');
  });
});
