const column = document.querySelector(".col-md-6");
column.querySelector("#allUsers").checked = true

document.addEventListener("DOMContentLoaded", function () {
    // Находим только нужную колонку
    const column = document.querySelector(".col-md-6");
    const allUsers = column.querySelector("#allUsers");
    const selectedUsers = column.querySelector("#selectedUsers");

    allUsers.addEventListener("change", function () {
        if (this.checked) {
            selectedUsers.checked = false;
        }
    });
    selectedUsers.addEventListener("change", function () {
        if (this.checked) {
            allUsers.checked = false;
        }
    });

});



document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('htmlFile');
    const fileLabel = document.querySelector('.custom-file-label');
    const uploadBtn = document.querySelector('.btn-primary');

    fileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name;
        if (fileName) {
            fileLabel.textContent = fileName;
        }
    });

    uploadBtn.addEventListener('click', function() {
        const file = fileInput.files[0];

        if (!file) {
            alert('Выберите файл');
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        fetch('/admin/api/upload-mailing/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                alert('Файл сохранен');
                fileInput.value = '';
                fileLabel.textContent = 'Выбрать файл';
            }})})


});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // cookie начинается с name=
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }




