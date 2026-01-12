




document.addEventListener('DOMContentLoaded', function () {

    console.log('wwwwwwwwwwwwwwwwwwwwwwww')
    $(document).ready(function () {
        $('.status-toggle').bootstrapToggle({
            on: 'ВКЛ',
            off: 'ВЫКЛ',
            onstyle: 'success',
            offstyle: 'danger',
            size: 'small'
        });

    const speedInput = document.querySelectorAll('input[name$="-speed"]')
        console.log(speedInput)
    document.querySelectorAll('.btn-group button').forEach(button => {
        button.addEventListener('click', () => {
            speedInput.value = button.dataset.value;
            console.log('Speed set to', speedInput.value);
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



    /// ajax для отправки на бэкэнд
    document.querySelectorAll('.ajax-banner-form').forEach(function (form){
        const bannerType = form.dataset.bannerType;

        form.addEventListener('submit', function (even) {
            even.preventDefault();
            const formData = new FormData(form);
            formData.append('bannerType', bannerType);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }})
                .then(function (response){
                    return response.json();
                })
                .then(function (data){
                    if (data.success){
                        $('#successModal').modal('show');
                    }
                })
        })



        const wrapper = form.querySelector('.banner-wrapper');

        const container = wrapper.querySelector('.banner-container');

        const totalFormsInput = wrapper.querySelector('input[name$="-TOTAL_FORMS"]');

        const emptyForm = wrapper.querySelector('.empty-banner-item');

            /// загрузка картинки
        wrapper.addEventListener('click', function (even){
            if (even.target.classList.contains('upload-btn')) {
                console.log('click upload btn')
                 const input = even.target.closest('.banner-item').querySelector('input[type="file"]');
                 input.click();
            }
                /// удаление формы
             if (even.target.classList.contains('remove-btn')) {
                 console.log('click delete btn')
                 const bannerItemForm = even.target.closest('.banner-item');
                 const deleteInput = bannerItemForm.querySelector('input[type="checkbox"][name$="-DELETE"]');
                 const inputId = bannerItemForm.querySelector('input[name$="-id"]');
                 if (inputId && inputId.value) {
                     if(deleteInput) {
                         deleteInput.checked = true;
                         bannerItemForm.hidden = true;
                         console.log('удалил форму с бэкенда');
                     }
                 }
                 else {
                     bannerItemForm.remove();
                     totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
                      console.log('удалил форму с фронтенда')

                 }


             }
             /// добавлеие формы
              if (even.target.closest('#add-banner-form-btn')){
                  console.log('add btn')
                  let banner_form_count = parseInt(totalFormsInput.value);
                  console.log('banner_form_count', totalFormsInput);
                  let new_form_top_banner = emptyForm.cloneNode(true);
                  console.log('new_form_top_banner', new_form_top_banner);

                new_form_top_banner.innerHTML = new_form_top_banner.innerHTML.replace(/__prefix__/g, banner_form_count);
                totalFormsInput.value = banner_form_count + 1;
                new_form_top_banner.hidden = false;
                container.appendChild(new_form_top_banner);
              }




        })
        wrapper.addEventListener('change', function (event) {
            console.log('press upload')
            if (event.target.type === 'file') {
                const reader = new FileReader();
                /// если в событии тип фаил то запипсываю фаил в костанту
                const file = event.target.files[0];
                /// тут получаю место где лежит старая картинка или плейсхолдер
                const img = event.target.closest('.banner-item').querySelector('.preview');
                // тут я обращаюсь к reader и меняю старое фото на новое
                reader.onload = function (e) {
                    img.src = e.target.result
                };
                // передаю путь к изображени в url формате для вывода
                reader.readAsDataURL(file)
                console.log('ywe')
            }
        })

    })})})
















