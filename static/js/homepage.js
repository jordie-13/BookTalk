// books display list scroll arrows
function scrollBooks(direction) {
    const bookGrid = document.querySelector('.home-book-grid');
    const scrollAmount = 1220; // Adjust this value to change the scroll distance
    if (direction === 'left') {
        bookGrid.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else if (direction === 'right') {
        bookGrid.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}
