document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('.modal');
    const bsModals = Array.from(modals).map(modal => new bootstrap.Modal(modal));

    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function() {
            const slug = this.getAttribute('data-book-slug');
            const title = this.getAttribute('data-book-title');
            const author = this.getAttribute('data-book-author');
            const genre = this.getAttribute('data-book-genre');
            const status = this.getAttribute('data-book-status');
            const notes = this.getAttribute('data-book-notes');
            const quotes = this.getAttribute('data-book-quotes');

            document.getElementById(`modalBookTitle${slug}`).innerText = title;
            document.getElementById(`modalBookAuthor${slug}`).innerText = author;
            document.getElementById(`modalBookGenre${slug}`).innerText = genre;
            document.getElementById(`modalBookStatus${slug}`).innerText = status;
            document.getElementById(`modalBookNotes${slug}`).value = notes;
            document.getElementById(`modalBookQuotes${slug}`).value = quotes;

            const detailLink = document.getElementById(`BookDetailLink${slug}`);
            detailLink.href = `/books/${slug}/`;

            bsModals.forEach(modal => {
                if (modal._element.id === `bookModal${slug}`) {
                    modal.show();
                }
            });
        });
    });

    document.querySelectorAll('.notes-form').forEach(form => {
        const editButton = form.querySelector('button[type="button"]');
        const saveButton = form.querySelector('button[type="submit"]');
        const textarea = form.querySelector('textarea');

        editButton.addEventListener('click', function() {
            textarea.removeAttribute('readonly');
            editButton.classList.add('d-none');
            saveButton.classList.remove('d-none');
        });
    });

    document.querySelectorAll('.quotes-form').forEach(form => {
        const editButton = form.querySelector('button[type="button"]');
        const saveButton = form.querySelector('button[type="submit"]');
        const textarea = form.querySelector('textarea');

        editButton.addEventListener('click', function() {
            textarea.removeAttribute('readonly');
            editButton.classList.add('d-none');
            saveButton.classList.remove('d-none');
        });
    });
});
