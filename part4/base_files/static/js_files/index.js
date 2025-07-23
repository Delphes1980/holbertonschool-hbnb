function checkAuthentication() {
    const token = getCookie('auth_cookie');
    const loginLink = document.getElementById('login-link');
	const loginButton = document.querySelector('login-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
		if (loginButton) loginButton.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
		if (loginButton) loginButton.style.display = 'none';
          // Fetch places data if the user is authenticated
        fetchPlaces(token)
			.then(placesData => {
				addPlaceCard(placesData);
			})
			.catch(error => {
				console.error('Fail during display of places ofter authentication', error);
			});
		}
	}

async function fetchPlaces(token) {
      // Make a GET request to fetch places data
      // Include the token in the Authorization header
      // Handle the response and pass the data to displayPlaces function
	try {
		const authHeader = new Headers();
		authHeader.append('Authorization', `Bearer ${token}`);

		const response = await fetch(`${DATA_URL}/places/`, {
			method: 'GET',
			mode: 'cors',
			credentials: 'include', //for cookies & specific headers
			headers: authHeader,
		});

		if (!response.ok) {
			const errorBody = await response.text();
			console.error(`HTTP error during getting the places: ${response.status} ${response.statusText}`, errorBody);
			throw new Error(`Fail during getting the places: ${response.status} ${response.statusText}`);
		}

		const data = await response.json();
		console.log('Getting list of places succeed:', data);
		return data;
	} catch (error) {
		console.error('Error during fetching the places:', error);
		throw error;
	}
}
	// 		try{
	// 			const data = await response.json();
	// 			console.log('Get the list of places');
	// 		} catch {
	// 			console.log('Getting the list of places failed: ' + response.statusText);
	// 		}}
	// 	return response

	// } catch (jsonError) {
	// 	console.log('Error parsing JSON:', jsonError);
	// }
	// 	if (networkError) {
	// 		console.error('Network error during getting list of places', networkError);
	// 	};

document.addEventListener('DOMContentLoaded', () => {
	checkAuthentication();
});
