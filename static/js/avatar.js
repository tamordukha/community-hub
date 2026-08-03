document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.querySelector(".profile-avatar-wrapper");
    const fileInput = wrapper.querySelector(".profile-avatar-input");
    const form = wrapper.closest("form");
    console.log('wrapper:', wrapper);
    console.log('form:', form);

    wrapper.addEventListener("click", function (event) {
        event.stopPropagation(); // чтобы случайно не сработало что-то лишнее
        fileInput.click(); // открывает проводник
    });

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            form.submit(); // отправляет форму → бэкенд сохраняет фото → редирект
        }
    });
});

