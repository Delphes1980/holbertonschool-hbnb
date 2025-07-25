// Function that log in a user
async function loginUser(email, password) {
	try {
		const response = await fetch(`${DATA_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		});

		if (response.ok) {
    		try {
				const data = await response.json();
				if (data && data.access_token) {
					// Return the token into a cookie
					document.cookie = `token=${data.access_token}; path=/; secure;`;
					window.location.href = 'index.html';
				} else {
					alert('Login failed: ' + response.statusText);
				}
			} catch (jsonError) {
				console.error('Error parsing JSON:', jsonError);
			}
		} else {
			let errorMessage = 'Login failed';
			try {
				const errorData = await response.json();
				if (errorData && errorData.message) {
					errorMessage += ' ' + errorData.message;
				} else {
					errorMessage += ' Status: ' + response.statusText;
				}
			} catch (networkError) {
				console.error('Network error during login:', networkError);
			}
			alert(errorMessage);
		}
	} catch (e) {
		console.error('Unexpected error during login:', e);
	}
}


document.addEventListener('DOMContentLoaded', () => {
	loginButtonVisibility();

	console.log('DOMContentLoaded s\'est déclenché.');
	const loginForm = document.getElementById('login-form');

	if (loginForm) {
		console.log('Formulaire login-form trouvé');  //debug
		loginForm.addEventListener('submit', async (event) => {
			console.log('Événement "submit" du formulaire détecté.');  //debug
			event.preventDefault();
			console.log('preventDefault() exécuté. Le formulaire ne devrait pas rechargé la page');  //debug

			const validateEmail = document.getElementById('email').value;
			const validatePassword = document.getElementById('password').value;
			console.log('Email:', email, 'Password:', password); // debug

			if (validateEmail === "") {
				alert('Email must be filled out');
				return;
			}

			if (validatePassword === "") {
				alert('Password must be filled out');
				return;
			}
			await loginUser(validateEmail, validatePassword);
			console.log('Fonction loginUser appelée.'); //debug
		});
	} else {
		console.error('Le formulaire avec l\'ID "login-form" n\'a PAS été trouvé');
		}
});
