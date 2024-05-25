document.addEventListener('DOMContentLoaded', function() {
    const pasteContainer = document.getElementById('paste-container');
    const uploadForm = document.getElementById('upload-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    pasteContainer.addEventListener('paste', function(event) {
        const items = (event.clipboardData || event.originalEvent.clipboardData).items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const file = items[i].getAsFile();
                const formData = new FormData();
                formData.append('image', file);
                formData.append('csrfmiddlewaretoken', csrfToken);

                fetch(uploadForm.action, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    document.body.innerHTML = data;
                })
                .catch(error => console.error('Error:', error));
            }
        }
    });
});
