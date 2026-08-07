document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.querySelector(".profile-avatar-wrapper");
    if (wrapper){
        const fileInput = wrapper.querySelector(".profile-avatar-input");
        const form = wrapper.closest("form");

        wrapper.addEventListener("click", function (event) {
            event.stopPropagation(); // чтобы случайно не сработало что-то лишнее
            fileInput.click(); // открывает проводник
        });

        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                form.submit(); // отправляет форму → бэкенд сохраняет фото → редирект
            }
        });
    }


    const menuToggle = document.getElementById('button-role');
    const dropdownMenu = document.getElementById('profile-dropdown-menu');

    if (menuToggle && dropdownMenu){

        // Открытие меню (изменить/удалить) при нажатии на 3 точки

        if (menuToggle && dropdownMenu) {
            
            menuToggle.addEventListener('click', function(event) {
                event.stopPropagation(); 
                dropdownMenu.classList.toggle('show');
            });
            
            document.addEventListener('click', function(event) {
                if (!dropdownMenu.contains(event.target) && event.target !== menuToggle) {
                    dropdownMenu.classList.remove('show');
                }
            });
        }
    }
});

