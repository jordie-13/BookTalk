document.addEventListener('DOMContentLoaded', function() {
    // Check if referrer is available and the user is landing on the book_detail page for the first time
    if (document.referrer && !localStorage.getItem('bookDetailReferrer')) {
        localStorage.setItem('bookDetailReferrer', document.referrer);
    }
});


function goBack() {
    // Get the stored referrer URL
    const referrer = localStorage.getItem('bookDetailReferrer');
    
    // Check if the referrer URL is available
    if (referrer) {
        // Navigate back to the referrer URL
        window.location.href = referrer;
        
        // Optionally, clear the stored referrer after navigating back
        localStorage.removeItem('bookDetailReferrer');
    } else {
        // Fallback if there is no stored referrer
        window.history.back();
    }
}
