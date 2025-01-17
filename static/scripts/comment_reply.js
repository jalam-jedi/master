document.addEventListener('DOMContentLoaded', function () {
    // Handle adding a new comment
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(commentForm);
            formData.append('action', 'add_comment');

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === 'success') {
                        location.reload(); // Reload to show the new comment
                    } else {
                        alert('Failed to add comment.');
                    }
                });
        });
    }

    // Handle adding a reply
    document.querySelectorAll('.replyForm').forEach((form) => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            formData.append('action', 'add_reply');

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === 'success') {
                        location.reload(); // Reload to show the new reply
                    } else {
                        alert('Failed to add reply.');
                    }
                });
        });
    });
});
