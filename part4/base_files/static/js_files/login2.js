// Add the event listener for the form submission
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
              // Your code to handle form submission
        });
    }
});

// Make the AJAX request to the API
async function loginUser(email, password) {
    const response = await fetch('https://your-api-url/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    }),
      // Handle the response
        success: function(response) {
            if (response.code === 200) {
                alert("Connexion réussie");
                window.location.href = "index.html";
            } else {
                alert("Nom d'utilisateur ou mot de passe incorrect");
            }
        },
        error: function(xhr, status, error) {
            console.error("La requête AJAX a échoué: " + status + "," + error);
        };
}

// Handle the API response and store the token in a cookie
if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
} else {
    alert('Login failed: ' + response.statusText);
}
