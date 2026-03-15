console.log('yres')
$(document).ready(function () {

    $('#userTable').DataTable({
        pageLength: 5,
        order: [[0, "desc"]],
        lengthChange: false,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/ru.json"
        }
    });

});



document.querySelectorAll('.delete-user').forEach(button => {

    button.addEventListener('click', function () {

        const userId = this.dataset.userId;
        console.log(userId)


        if (!confirm("Удалить пользователя?")) return;

        fetch(`delete-user/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.closest('tr').remove(); // удаляем строку из таблицы
            }
        });

    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
