document.addEventListener("DOMContentLoaded", function() {
    // Automatically close messages after 3 seconds
    setTimeout(function() {
        console.log("Timeout function executed.");
        
        let messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            console.log("Hiding message:", message.textContent);
            message.style.display = 'none';
        });
    }, 3000);

    // Toggle search form visibility
    document.querySelector('.search-icon').addEventListener('click', function() {
        var form = document.querySelector('.form-inline');
        form.classList.toggle('show');
    });
});