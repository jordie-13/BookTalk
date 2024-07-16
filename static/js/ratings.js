document.addEventListener('DOMContentLoaded', function () {
    // Select all star icons, current user rating, and average book rating elements
    const stars = document.querySelectorAll('.star-icon');
    const userRatingElement = document.getElementById('user-rating');
    const averageRatingElement = document.getElementById('average-rating');

    // Attach event listeners to each star
    stars.forEach(star => {
        star.addEventListener('mouseover', handleStarHover);
        star.addEventListener('mouseout', handleStarHoverOut);
        star.addEventListener('click', handleStarClick);
    });


    // Function to handle star hover event
    function handleStarHover(event) {
        const value = parseFloat(event.target.getAttribute('data-value'));
        fillUserStars(value);
    }


    // Function to handle mouseout event
    function handleStarHoverOut() {
        const userRating = parseFloat(userRatingElement.textContent);
        fillUserStars(userRating);
    }


    // Function to handle star click event
    function handleStarClick(event) {
        event.preventDefault(); // Prevent the default form submission 
        const form = event.target.closest('form');
        const value = parseFloat(event.target.getAttribute('data-value'));
        userRatingElement.textContent = value;
        fillUserStars(value);
        submitForm(form, value); // Submit the form via AJAX using our submitForm function
    }
    

    // Function to colour/fill star icons up to a given value
    function fillUserStars(value) {
        // For each star check to see how many need to be filled to match user rating
        stars.forEach(star => {
            // Get the selected star icons data-value
            const starValue = parseFloat(star.getAttribute('data-value'));
            // Add filled class to any star up to the user rating. 
            if (starValue <= value) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled',);
            }
        });
    }


    // Function to colour/fill star icons to display a books ave. rating
    function fillBookStars(average_rating) {
        const starIcons = document.querySelectorAll('.book-star-ratings .book-rating-star');

        starIcons.forEach(starIcon => {
            const value = parseInt(starIcon.getAttribute('data-value'));

            // Handle full filled stars
            if (average_rating >= value) {
                starIcon.classList.add('fas'); // Fill the star
                starIcon.classList.remove('far');
            } else {
                starIcon.classList.remove('fas'); // Empty the star
                starIcon.classList.add('far');
            }

            // Calculate remainder after filling full stars
            const remainder = average_rating - Math.floor(average_rating);

            // Handle half-filled stars, when average_rating rounds to 0.5. 
            if (remainder >= 0.3 && remainder <= 0.7 && Math.floor(average_rating) === value - 1) {
                starIcon.classList.add('half-filled');
                starIcon.classList.add('fas');
            } else {
                starIcon.classList.remove('half-filled');
            }
        });
    }


    function bookRatingText(average_rating, total_ratings) {
        // Display books ave. rating in text, check for plural format
        let averageRatingText;
            // Check if average_rating is not null
            if (average_rating !== null) {
                let ratingText;
                // Determine if it's singular or plural based on total_ratings
                if (total_ratings === 1) {
                    ratingText = 'rating';
                } else {
                    ratingText = 'ratings';
                }
                // put together the averageRatingText string and round ave. rating to one decimal
                averageRatingText = `${average_rating.toFixed(1)} from ${total_ratings} ${ratingText}`;
            // If there are no ratings, display a message 
            } else {
                averageRatingText = 'No ratings yet';
            }  
        // Update the HTML content of averageRatingElement with the calculated/put together averageRatingText
        averageRatingElement.innerHTML = `<p>${averageRatingText}</p>`;
    } 

    // Function to submit the form via AJAX
    function submitForm(form, value) {
        const formData = new FormData(form); // Create FormData object from form
        formData.set('rating', value); // Set the rating value in the FormData object

        // Send a fetch request to the form action
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // CSRF token for security
                'X-Requested-With': 'XMLHttpRequest' // Indicate AJAX request
            }
        })
        .then(response => response.json()) // Convert response to JSON
        .then(data => {
            // If the rating was submitted successfully update user rating and average rating display
            if (data.message === 'Rating submitted successfully') {
                // Update books average rating display
                userRatingElement.textContent = data.user_rating; 
                
                // Refill user rating stars based on updated user rating
                fillUserStars(parseFloat(userRatingElement.textContent)); 
                // Refill books average rating stars based on all reviews
                fillBookStars(data.average_rating);
                // Create and display the rating text below books stars
                bookRatingText(data.average_rating, data.total_ratings);
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);
        });
    }
   
    // Colour/fill the stars for the books ave. rating when the page loads
    fillBookStars(parseFloat(averageRatingElement.textContent));
    // Colour/fill the stars based on the user's existing rating 
    // when the page loads if the users has previously rated 
    if (userRatingElement) {
        fillUserStars(parseFloat(userRatingElement.textContent));
    } 


});


