let dialogTag = null;
let allPlaces = [];
const DATA_URL = 'http://localhost:5000/api/v1';

let modal = null;
let closeButton = null;
let modalPlaceName = null;
let reviewForm = null;
let reviewPlaceIdInput = null;
let reviewTextInput = null;
let ratingInput = null;
let cancelButton = null;

// Mapping for the image associated to a specific place ID
const placeImageMapping = {
  '121c0d34-a070-4773-b1bf-b850da8b2607': '../images/bedroom.jpg',
  '1992dcc6-c608-4874-ac01-76d8c58bbd64': '../images/maison_campagne.jpg',
  'f428ffc2-b4e3-4117-b393-7ed9df361785': '../images/apartment_perdu.jpg',
  'cb1bcb40-200e-4f60-941a-5fb4e3a15b68': '../images/loft_mer.jpg',
  '44e18cdb-56c6-468e-92ec-edf5d9e69381': '../images/cute_little_house.jpg',
  '6afb6d48-82b3-413b-9449-f618469dde8c': '../images/modern_house.jpg',
  '21128672-c321-49d0-87d8-b34c76059e02': '../images/cozy_cottage.jpg',
  '32d5bab8-599f-47ba-a291-03e5cd3795f9': '../images/city_apartment.jpg'
};

// Function to get the image URL of a place
function getPlaceImage(placeId) {
  return placeImageMapping[placeId] || '../images/no_image.png';
}


// Close the modal
    const closeModal = () => {
      if (modal) {
        modal.style.display = 'none';
      }
      document.body.classList.remove('modal-open');
    };


// Function to redirect the login button to the login page
function loginRedirection() {
  const clickLogin = document.querySelector('.login-button');
  if (clickLogin) {
    clickLogin.addEventListener('click', () => {
      window.location.href = "login.html";
      console.log('Redirection to the login page');
    });
} else {
  console.error('Login button not found');
}
}


// Function that log out a user
function logoutUser() {
	document.cookie = 'token=; path=/; Max-Age=0; secure;';
  alert('You are deconnected, please login');
	console.log('Token cookie successfully deleted');
	window.location.href = 'login.html'; // Redirection to the login page
}


// Function that switch between the login button and the logout button
function loginButtonVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
	const loginButton = document.querySelector('.login-button');
  const logoutButton = document.getElementById('logout-button');

    if (token) {
        if (loginLink) {
          loginLink.style.display = 'none';
        }
        if (loginButton) {
          loginButton.style.display = 'none';
        }
        if (logoutButton) {
          logoutButton.style.display = 'inline-block';

          logoutButton.removeEventListener('click', logoutUser);
          logoutButton.addEventListener('click', logoutUser);
        }
      } else {
        if (loginLink) {
          loginLink.style.display = 'block';
        }
        if (loginButton) {
          loginButton.style.display = 'inline-block';
        }
        if (logoutButton) {
          logoutButton.style.display = 'none';
        }
      }
      console.log('Login button visibility update');
  }


// Function that redirect to the home page by clicking on the logo
function homeRedirection() {
  const cliskHome = document.querySelector('.logo');
  if (cliskHome) {
    cliskHome.addEventListener('click', () => {
      window.location.href = "index.html";
      console.log('Redirection to the index page');
    });
  } else {
    console.error('Logo button not found');
  }
}


// Function to get a cookie by its name
function getCookie(name) {
	const cookies = document.cookie.split("; ");
  const foundCookie = cookies.find(c => {
    return c.startsWith(name);
  })

	let value = undefined;
  if (foundCookie) {
    value = foundCookie.split("=")[1];
  }

  if (value === undefined) {
    return null;
  }
  return value;
}


// Function that display a review form for authenticated user
function userReviewForm() {
    const reviewFormSection = document.getElementById('add-review');
    const token = getCookie('token');

    if (reviewFormSection) {
        if (token) {
            reviewFormSection.style.display = 'flex';
            console.log('Review form displayed for authenticated user');
        } else {
        reviewFormSection.style.display = 'none';
        console.log('Review form hidden for non authenticated user');
        }
    } else {
        console.error('The "add-review" section was not found on the page');
    }
}


// Function that submit rating stars
function ratingSubmit() {
    const allStar = document.querySelectorAll('.rating .star');
    const ratingInput = document.getElementById('rating-input');

    if (!allStar.length || !ratingInput) {
      console.warn('Rating stars or input not found');
      return;
    }

    allStar.forEach((item, idx) => {
        item.addEventListener('click', () => {
          let click = 0;

        ratingInput.value = item.dataset.value;
        console.log('Selected rating value: ', ratingInput.value)

        // Reinitialization of all stars
        allStar.forEach(star => {
            star.classList.replace('bxs-star', 'bx-star');
            star.classList.remove('active');
        });

        // For visual effects
        for(let i = 0; i < allStar.length; i++) {
          const starCurrentValue = parseInt(allStar[i].dataset.value);
          const selectedRating = parseInt(ratingInput.value);

            if (starCurrentValue <= selectedRating) {
                allStar[i].classList.replace('bx-star', 'bxs-star');
                allStar[i].classList.add('active');
                allStar[i].style.setProperty('--i', i);

            } else {
                allStar[i].classList.replace('bxs-star', 'bx-star');
                allStar[i].classList.remove('active');
                allStar[i].style.setProperty('--i', click);
                click++;
            }
        }
    });
});
}


  /* Function to show a card containing a review form
  when clicking on the 'submit review' button of the place card*/

async function showPlaceDetails(placeId, placeTitle) {
    if (!modal || !closeButton || !modalPlaceName ||!reviewForm || !reviewPlaceIdInput || !reviewTextInput || !ratingInput || !cancelButton) {
      console.error('One or many elements of the modal were not found');
      return;
    }

    modal = document.getElementById('placeDetailsModal');
    closeButton = document.querySelector('.close-button');
    modalPlaceName = document.getElementById('modal-place-name');
    reviewForm = document.getElementById('review-form');
    reviewPlaceIdInput = document.getElementById('review-place-id-input');
    reviewTextInput = document.getElementById('review-text');
    ratingInput = document.getElementById('rating-input');
    cancelButton = document.querySelector('.btn-cancel');

    if (!modal || !closeButton || !modalPlaceName ||!reviewForm || !reviewPlaceIdInput || !reviewTextInput || !ratingInput || !cancelButton) {
      console.error('Critical error: still missing modal elements');
      return;
    }

    modalPlaceName.textContent = `Submit a review for: ${placeTitle}`;

    reviewPlaceIdInput.value = placeId;

    // Reinitialize stars & form at every modal opening
    reviewForm.reset();
    const stars = reviewForm.querySelectorAll('.rating .star');
    stars.forEach(s => {
      s.classList.remove('bxs-star', 'active');
      s.classList.add('bx-star');
    });
    ratingInput.value = '';

    // Display the modal
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
  }
