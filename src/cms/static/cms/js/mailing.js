const column = document.querySelector(".col-md-6");
column.querySelector("#allUsers").checked = true


const progressBar = document.getElementById("mailing-progress");


document.addEventListener("DOMContentLoaded", function() {

    const progressBar = document.getElementById("mailing-progress");
    const startBtn = document.getElementById("start-mailing-btn");

    function checkActiveMailing() {
        fetch("/admin/api/active-mailing/")  // вот сюда обращаемся
        .then(r => r.json())
        .then(data => {
            console.log('data with backend',data)
            console.log('')

            if (!data.active) {
                startBtn.disabled = false;  // кнопка запуска активна
                progressBar.style.width = "0%";
                progressBar.innerText = "0%";
                return;
            }

            // Если есть активная рассылка
            // startBtn.disabled = true; // блокируем запуск новой

            const mailingId = data.mailing_id;




            // WebSocket для live обновлений
            const socket = new WebSocket(`ws://${window.location.host}/ws/mailing/${mailingId}/`);
            socket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                console.log('live update',data)

            };
        });
    }

    // Проверяем при загрузке страницы
    checkActiveMailing();


});



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
            console.log(data.status)
            if (data.status === 'ok') {
                const mail_list = document.getElementById('mail_list');
                const newItem = document.createElement('div');
                newItem.className = 'form-check';
                newItem.innerHTML = `<input class="form-check-input" type="checkbox"><label class="form-check-label">${data.filename}</label>
            <a href="#" class="text-danger float-right">Удалить</a>
        `;
                if (mail_list.children.length === 0) {
                    mail_list.appendChild(newItem);
                }
                else {
                    mail_list.insertBefore(newItem, mail_list.firstChild);
                }
                if (mail_list.children.length > 5) {
                    mail_list.removeChild(mail_list.lastChild);
                }
                fileInput.value = '';
                fileLabel.textContent = 'Выбрать файл';
            }})})


});



document.addEventListener('DOMContentLoaded', function() {
    const mailList = document.getElementById('mail_list');
    const lastLoadedLink = document.querySelector('p:first-of-type a');
    // Делегирование событий - обрабатываем клики на чекбоксы внутри mail_list
    mailList.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox') {
            // Снимаем все остальные чекбоксы
            const checkboxes = mailList.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (cb !== e.target) cb.checked = false;
            });

            // Если чекбокс отмечен, подставляем имя файла
            if (e.target.checked) {
                const fileName = e.target.closest('.form-check').querySelector('label').textContent.trim();
                lastLoadedLink.textContent = fileName;
            } else {
                // Если сняли галочку, очищаем
                lastLoadedLink.textContent = 'Выбырите фаил для рассылки';
            }
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const startBtn = document.querySelector(".btn-success");

    startBtn.addEventListener("click", function () {
        const selectedCheckbox = document.querySelector("#mail_list input[type='checkbox']:checked");

        if (!selectedCheckbox) {
            alert("Выберите шаблон для рассылки");
            return;
        }

        const mailingId = selectedCheckbox.dataset.mailingId; // присвоить data-mailing-id каждому div

        fetch("/admin/api/start-mailing/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ mailing_id: mailingId })
        })
        .then(r => r.json())
        .then(data => {
            console.log(data)
            if (data.status === "ok") {
                alert("Рассылка запущена!");
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
            // cookie начинается с name=
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }






