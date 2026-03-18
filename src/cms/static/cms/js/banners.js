




document.addEventListener('DOMContentLoaded', function () {

    const isUseImageInput = document.getElementById('id_is_use_image');
    console.log(isUseImageInput)

    const PLACEHOLDER =
        'https://www.nomadfoods.com/wp-content/uploads/2018/08/placeholder-1-e1533569576673-960x960.png';
    const bgImageRadio = document.getElementById('bgImage'); // кнопка для картинки

    const bgColorRadio = document.getElementById('bgColor'); /// кнопка для фона

    const uploadBtn = document.getElementById('uploadLogoBtn'); // кнопка загрузки
    const deleteBtn = document.getElementById('deleteLogoBtn'); // кнопка удаления

    const fileInput = document.querySelector('#imageInputBlock input[type="file"]');
    const preview = document.getElementById('mainImagePreview');
    const deleteImageInput = document.getElementById('deleteImageInput');

    /// переклоюбчение радоикнопки на выбор изображения если нажал загрузить

    uploadBtn.addEventListener('click', function (event){
        event.preventDefault();
        bgImageRadio.checked = true;
        fileInput.click();
        isUseImageInput.value = 'True'

    })
    /// замена плейсхолдера на каритинку
    fileInput.addEventListener('change', function (event){
        const reader = new FileReader();
         const file = event.target.files[0];
         const img = document.getElementById('mainImagePreview')
          reader.onload = function (e) {
                    img.src = e.target.result
                };
          reader.readAsDataURL(file);

          console.log('yesss')
    })

    /// удаление картинки
    deleteBtn.addEventListener('click', function (event) {
        console.log('delete btn')
        event.preventDefault();
        bgColorRadio.checked = true;
        preview.src = PLACEHOLDER;
        fileInput.value = '';
        deleteImageInput.value = 'true';




    })

    bgColorRadio.addEventListener('change', function () {
    if (!this.checked) return;

    preview.src = PLACEHOLDER;   // убираем превью
    fileInput.value = '';        // сбрасываем file input
    deleteImageInput.value = 'true';  // говорим серверу удалить файл
    isUseImageInput.value = 'False'
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




     document.querySelectorAll('.ajax-bg-banner-from').forEach(function (form) {
         form.addEventListener('submit', function (even) {
             even.preventDefault();
             const data = new FormData(form);
             fetch(form.action, {

                method: 'POST',
                body: data,
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
    })





    console.log('news')
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



    /// яакс для баннера на заднем фоне




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
















