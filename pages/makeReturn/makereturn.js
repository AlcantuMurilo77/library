document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const userId = document.getElementById("userId").value.trim();
    const bookId = document.getElementById("bookId").value.trim();

    if (!userId || !bookId) {
      alert("Please fill in both fields.");
      return;
    }

    const data = {
      user_id: userId,
      book_id: bookId
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/returnbook", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        alert("Return successful!");
      } else {
        alert("Error: " + result.error);
      }
    } catch (error) {
      console.error("Error connecting to server:", error);
      alert("Error connecting to server. Please try again later.");
    }
  });
});
