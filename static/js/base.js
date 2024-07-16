// Automatically close messages after 3 seconds
document.addEventListener("DOMContentLoaded", function() {
    
    setTimeout(function() {
        console.log("Timeout function executed.");
        
        let messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            console.log("Hiding message:", message.textContent);
            message.style.display = 'none';
        });
    }, 3000);

});