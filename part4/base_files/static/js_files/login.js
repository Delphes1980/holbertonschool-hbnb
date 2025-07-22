// Add the event listener for the form submission
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
              // Your code to handle form submission
			const validateMail = document.forms['login-form']['email'].value;
			if (validateMail == "") {
				alert('Email must be filled out');
				return false;
			}
			const validatePassword = document.forms['login-form']['password'].value;
			if (validatePassword == "") {
				alert('Password must be filled out');
				return false;
			}
        });
    }
});

// Make the AJAX request to the API
async function loginUser(email, password) {
    const response = await fetch('https://localhost:5000/api/v1/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
      // Handle the response
	if (response.ok) {  // Handle the API response and store the token in a cookie
    try {
		const data = await response.json();
    	document.cookie = `token=${data.access_token}; path=/`;
    	window.location.href = 'templates/index.html';
	} catch {
    	alert('Login failed: ' + response.statusText);
	}
};
}
