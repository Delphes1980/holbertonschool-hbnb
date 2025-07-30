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


function loginButtonVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
	const loginButton = document.querySelector('.login-button');

    if (loginLink) {
        if (!token) {
          loginLink.style.display = 'block';
        } else {
          loginLink.style.display = 'none';
        }
      }
		if (loginButton) {
      if (!token) {
        loginButton.style.display = 'block';
      } else {
        loginButton.style.display = 'none';
      }
    }
    console.log('Login button visibility update');
  }


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
    console.log('showPlaceDetails: hidden place ID set to: ', reviewPlaceIdInput.value); //debug

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
