// Function that submit a review
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const headers = { 'Content-Type': 'application/json'};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${DATA_URL}/reviews/`, {
            method: 'POST',
            headers: headers,
            credentials: 'include',
            body: JSON.stringify({
                text : reviewText,
                place_id: placeId,
                rating: rating})
        });
        if (response.ok) {
            try {
                console.log('Success for review submission');
                const data = await response.json();
                console.log('Response for review submission: ', data);

                const reviewFormReinitializated = document.getElementById('review-form');
                if (reviewFormReinitializated) {
                    reviewFormReinitializated.reset();
                }

            } catch (jsonError) {
                console.error('Error parsing JSON: ', jsonError);
            }

        } else {
            let errorMessage = 'Review submission failed';
            try {
                const errorData = await response.json();
                if (errorData && errorData.message) {
                    errorMessage += 'Details: ' + errorData.message;
                } else {
                    errorMessage += 'Status: ' + response.statusText;
                }
            } catch (networkError) {
                console.error('Network error during review submission', networkError);
            }
            alert(errorMessage);
        }
    } catch (error) {
        console.error('Unexpected error during review submission', error);
    }
}

// document.addEventListener('DOMContentLoaded', () => {
//     loginButtonVisibility();
//     ratingSubmit();

//     const reviewForm = document.getElementById('review-form');
//     if (reviewForm) {
//         reviewForm.addEventListener('submit', async(event) => {
//             event.preventDefault();

//             const placeId = new URLSearchParams(window.location.search).get('id');
//             const reviewText = document.getElementById('review-text').value;
//             const ratingInput = reviewForm.querySelector('input[name="rating"]');
//             const rating = ratingInput ? parseInt(ratingInput.value) : 0;

//             const token = getCookie('token');

//             if (!token) {
//                 alert('You should be authenticated to submit a review');
//                 return;
//             }

//             await submitReview(token, placeId, reviewText, rating);
//             // Rappel de la fonction qui gère le rafraichissement des commentaires 
//         });
//             const cancelButton = reviewForm.querySelector('.btn-cancel');
//             if (cancelButton) {
//                 cancelButton.addEventListener('click', () => {
//                     reviewForm.reset();

//                     const stars = document.querySelectorAll('#review-form .rating .star');
//                     const ratingInput = document.getElementById('rating-input');
//                     if (ratingInput) {
//                         ratingInput.value = '';
//                         stars.forEach(s => {
//                             s.classList.remove('bxs-star');
//                             s.classList.add('bx-star');
//                             s.classList.remove('active');
//                         });
//                     }
//             });
//         }
//     }
// });
