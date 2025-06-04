    document.addEventListener('DOMContentLoaded', function () {
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const usernameSpan = document.getElementById('deleteUsername');

    document.querySelectorAll('button[data-bs-target="#confirmDeleteModal"]').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');
            const username = this.getAttribute('data-username');

            confirmDeleteBtn.setAttribute('formaction', `/user/${userId}/delete`);
            usernameSpan.textContent = username;
        });
    });
    confirmDeleteBtn.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');
            const username = this.getAttribute('data-username');
            console.log(userId + " " + user.id)
            confirmDeleteBtn.setAttribute('formaction', `/user/${userId}/delete`);
            usernameSpan.textContent = username;
        });
});