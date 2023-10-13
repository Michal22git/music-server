document.addEventListener('DOMContentLoaded', function() {
const deleteForm = document.getElementById('delete-form');
    deleteForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (window.confirm('Do you want to delete this playlist?')) {
            // add logic
        }
    });
});