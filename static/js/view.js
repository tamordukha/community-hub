const commentInput = document.getElementById('comment-input');
const commentSubmit = document.getElementById('comment-submit');
const commentCancel = document.getElementById('comment-cancel');
const menuToggle = document.getElementById('post-menu-trigger')
const dropdownMenu = document.getElementById('post-dropdown-menu');

// Открытие меню (изменить/удалить) при нажатии на 3 точки

if (menuToggle && dropdownMenu) {
    
    // 1. Клик по троеточию: открываем или закрываем меню
    menuToggle.addEventListener('click', function(event) {
        // Запрещаем клику «идти дальше» по странице, иначе сработает глобальный обработчик ниже
        event.stopPropagation(); 
        
        // Метод toggle добавляет класс .show, если его нет, и удаляет, если он есть
        dropdownMenu.classList.toggle('show');
    });

    // 2. Клик в ЛЮБОЕ МЕСТО экрана: закрываем меню, если оно открыто
    document.addEventListener('click', function(event) {
        // Если кликнули МИМО самого меню и МИМО кнопки-троеточия
        if (!dropdownMenu.contains(event.target) && event.target !== menuToggle) {
            dropdownMenu.classList.remove('show'); // Принудительно прячем меню
        }
    });
}

// Логика блокировки/активации кнопки отправки при вводе текста
commentInput.addEventListener('input', function() {
    if (commentInput.value.trim().length > 0) {
        commentSubmit.removeAttribute('disabled');
    } else {
        commentSubmit.setAttribute('disabled', 'true');
    }
});

// Логика очистки текста по клику на «Отмена»
commentCancel.addEventListener('click', function() {
    commentInput.value = ''; 
    commentSubmit.setAttribute('disabled', 'true'); 
});

