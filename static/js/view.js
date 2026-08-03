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


// Открытие меню комментария (изменить/удалить/скрыть) при нажатии на 3 точки

// 1. Находим СВЕРХУ ВСЕ кнопки троеточия у комментариев на странице
const commentMenuButtons = document.querySelectorAll('.comment-options-btn');

// 2. Запускаем цикл по всем найденным кнопкам
commentMenuButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        // Останавливаем всплытие клика, чтобы сразу не сработал обработчик закрытия на документе
        event.stopPropagation();
        
        document.querySelectorAll('.comment-dropdown-menu.show, .reply-dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });

        // Сначала закрываем ВСЕ другие открытые меню комментариев на странице, 
        // чтобы одновременно не висело несколько открытых окошек
        document.querySelectorAll('.comment-dropdown-menu.show').forEach(openMenu => {
            // Закрываем только чужие меню, текущее переключим ниже
            if (openMenu !== this.nextElementSibling) {
                openMenu.classList.remove('show');
            }
        });

        // Находим родительский контейнер опций именно ЭТОГО комментария
        const parentOptions = this.closest('.comment-options');
        
        if (parentOptions) {
            // Ищем блок меню СТРОГО внутри этого родительского контейнера опций
            const dropdownMenu = parentOptions.querySelector('.comment-dropdown-menu');
            
            if (dropdownMenu) {
                // Переключаем класс видимости: если меню скрыто — покажем, если открыто — спрячем
                dropdownMenu.classList.toggle('show');
            }
        }
    });
});

// 3. Глобальный клик по экрану: закрываем любое открытое меню комментариев, если кликнули мимо
document.addEventListener('click', function(event) {
    // Находим все открытые меню на странице
    const activeMenus = document.querySelectorAll('.comment-dropdown-menu.show');
    
    activeMenus.forEach(menu => {
        // Находим кнопку, которая принадлежит этому меню
        const parentOptions = menu.closest('.comment-options');
        const associatedButton = parentOptions ? parentOptions.querySelector('.comment-options-btn') : null;
        
        // Если кликнули НЕ по самому меню и НЕ по его кнопке-троеточию — принудительно закрываем
        if (!menu.contains(event.target) && event.target !== associatedButton) {
            menu.classList.remove('show');
        }
    });
});






// Открытие меню ответа (изменить/удалить/скрыть) при нажатии на 3 точки

// 1. Находим СВЕРХУ ВСЕ кнопки троеточия у комментариев на странице
const replyMenuButtons = document.querySelectorAll('.reply-options-btn');

// 2. Запускаем цикл по всем найденным кнопкам
replyMenuButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        // Останавливаем всплытие клика, чтобы сразу не сработал обработчик закрытия на документе
        event.stopPropagation();
        
        document.querySelectorAll('.comment-dropdown-menu.show, .reply-dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });

        // Сначала закрываем ВСЕ другие открытые меню комментариев на странице, 
        // чтобы одновременно не висело несколько открытых окошек
        document.querySelectorAll('.reply-dropdown-menu.show').forEach(openMenu => {
            // Закрываем только чужие меню, текущее переключим ниже
            if (openMenu !== this.nextElementSibling) {
                openMenu.classList.remove('show');
            }
        });

        // Находим родительский контейнер опций именно ЭТОГО комментария
        const parentOptions = this.closest('.reply-options');
        
        if (parentOptions) {
            // Ищем блок меню СТРОГО внутри этого родительского контейнера опций
            const dropdownMenu = parentOptions.querySelector('.reply-dropdown-menu');
            
            if (dropdownMenu) {
                // Переключаем класс видимости: если меню скрыто — покажем, если открыто — спрячем
                dropdownMenu.classList.toggle('show');
            }
        }
    });
});

// 3. Глобальный клик по экрану: закрываем любое открытое меню комментариев, если кликнули мимо
document.addEventListener('click', function(event) {
    // Находим все открытые меню на странице
    const activeMenus = document.querySelectorAll('.reply-dropdown-menu.show');
    
    activeMenus.forEach(menu => {
        // Находим кнопку, которая принадлежит этому меню
        const parentOptions = menu.closest('.reply-options');
        const associatedButton = parentOptions ? parentOptions.querySelector('.reply-options-btn') : null;
        
        // Если кликнули НЕ по самому меню и НЕ по его кнопке-троеточию — принудительно закрываем
        if (!menu.contains(event.target) && event.target !== associatedButton) {
            menu.classList.remove('show');
        }
    });
});




// ЛОГИКА РАСКРЫТИЯ/СКРЫТИЯ ПОСТА

// 1. Находим ВСЕ кнопки «Read more...» и «Hide» на странице
const postReadMoreButtons = document.querySelectorAll('.post-read-more');
const postHideButtons = document.querySelectorAll('.post-hide');

// 2. Обрабатываем клики по кнопкам «Read more...»
postReadMoreButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Находим общий родительский контейнер текста для ЭТОГО конкретного комментария
        const parentPostContent = this.closest('.post-detail-content');
        
        if (parentPostContent) {
            // Находим блоки короткого и полного текста СТРОГО внутри этого комментария
            const postShortBlock = parentPostContent.querySelector('.post-content-short');
            const postFullBlock = parentPostContent.querySelector('.post-content-full');
            
            // Переключаем классы видимости (которые мы прописали в CSS)
            if (postShortBlock && postFullBlock) {
                postShortBlock.classList.add('hidden'); // Прячем короткий текст
                postFullBlock.classList.add('active');   // Показываем полный текст
            }
        }
    });
});

// 3. Обрабатываем клики по кнопкам «Hide» (обратное действие)
postHideButtons.forEach(button => {
    button.addEventListener('click', function() {
        const parentPostContent = this.closest('.post-detail-content');
        
        if (parentPostContent) {
            const postShortBlock = parentPostContent.querySelector('.post-content-short');
            const postFullBlock = parentPostContent.querySelector('.post-content-full');
            
            if (postShortBlock && postFullBlock) {
                postShortBlock.classList.remove('hidden'); // Возвращаем короткий текст
                postFullBlock.classList.remove('active');   // Прячем полный текст
            }
        }
    });
});





// ЛОГИКА РАСКРЫТИЯ/СКРЫТИЯ КОММЕНТАРИЕВ

// 1. Находим ВСЕ кнопки «Read more...» и «Hide» на странице
const readMoreButtons = document.querySelectorAll('.comment-read-more');
const hideButtons = document.querySelectorAll('.comment-hide');

// 2. Обрабатываем клики по кнопкам «Read more...»
readMoreButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Находим общий родительский контейнер текста для ЭТОГО конкретного комментария
        const parentContent = this.closest('.comment-item-content');
        
        if (parentContent) {
            // Находим блоки короткого и полного текста СТРОГО внутри этого комментария
            const shortBlock = parentContent.querySelector('.comment-content-short');
            const fullBlock = parentContent.querySelector('.comment-content-full');
            
            // Переключаем классы видимости (которые мы прописали в CSS)
            if (shortBlock && fullBlock) {
                shortBlock.classList.add('hidden'); // Прячем короткий текст
                fullBlock.classList.add('active');   // Показываем полный текст
            }
        }
    });
});

// 3. Обрабатываем клики по кнопкам «Hide» (обратное действие)
hideButtons.forEach(button => {
    button.addEventListener('click', function() {
        const parentContent = this.closest('.comment-item-content');
        
        if (parentContent) {
            const shortBlock = parentContent.querySelector('.comment-content-short');
            const fullBlock = parentContent.querySelector('.comment-content-full');
            
            if (shortBlock && fullBlock) {
                shortBlock.classList.remove('hidden'); // Возвращаем короткий текст
                fullBlock.classList.remove('active');   // Прячем полный текст
            }
        }
    });
});



// ЛОГИКА РАСКРЫТИЯ/СКРЫТИЯ ОТВЕТОВ

// 1. Находим ВСЕ кнопки «Read more...» и «Hide» на странице
const replyReadMoreButtons = document.querySelectorAll('.reply-read-more');
const replyHideButtons = document.querySelectorAll('.reply-hide');

// 2. Обрабатываем клики по кнопкам «Read more...»
replyReadMoreButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Находим общий родительский контейнер текста для ЭТОГО конкретного комментария
        const replyParentContent = this.closest('.reply-item-content');
        
        if (replyParentContent) {
            // Находим блоки короткого и полного текста СТРОГО внутри этого комментария
            const replyShortBlock = replyParentContent.querySelector('.reply-content-short');
            const replyFullBlock = replyParentContent.querySelector('.reply-content-full');
            
            // Переключаем классы видимости (которые мы прописали в CSS)
            if (replyShortBlock && replyFullBlock) {
                replyShortBlock.classList.add('hidden'); // Прячем короткий текст
                replyFullBlock.classList.add('active');   // Показываем полный текст
            }
        }
    });
});

// 3. Обрабатываем клики по кнопкам «Hide» (обратное действие)
replyHideButtons.forEach(button => {
    button.addEventListener('click', function() {
        const replyParentContent = this.closest('.reply-item-content');
        
        if (replyParentContent) {
            const replyShortBlock = replyParentContent.querySelector('.reply-content-short');
            const replyFullBlock = replyParentContent.querySelector('.reply-content-full');
            
            if (replyShortBlock && replyFullBlock) {
                replyShortBlock.classList.remove('hidden'); // Возвращаем короткий текст
                replyFullBlock.classList.remove('active');   // Прячем полный текст
            }
        }
    });
});







const commentInput = document.getElementById('comment-input');
const commentSubmit = document.getElementById('comment-submit');
const commentCancel = document.getElementById('comment-cancel');

if (commentInput && commentCancel && commentSubmit){
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
}







// Функция ОБНОВЛЕНИЯ комментария

// 1. Находим СВЕРХУ ВСЕ кнопки изменить у комментариев на странице
const commentEditButton = document.querySelectorAll('.comment-edit-trigger-btn');
const commentEditCancelButton = document.querySelectorAll('.btn-comment-edit-form[type="button"]');

// 2. Запускаем цикл по всем найденным кнопкам
commentEditButton.forEach(button => {
    button.addEventListener('click', function(event) {
        // Останавливаем всплытие клика, чтобы сразу не сработал обработчик закрытия на документе
        event.stopPropagation();

        // Находим родительский контейнер опций именно ЭТОГО комментария
        const commentItem = this.closest('.comment-item');
        
        if (commentItem) {
            // Ищем блок меню СТРОГО внутри этого родительского контейнера опций
            const commentEditForm = commentItem.querySelector('.comment-edit-form');
            const commentItemMain = commentItem.querySelector('.comment-item-main');
            const commentItemContent = commentItem.querySelector('.comment-item-content');
            const commentItemFooter = commentItem.querySelector('.comment-item-footer');

            if (!commentEditForm.dataset.commentItemContent) {
                const commentEditContent = commentItemContent.textContent.trim();
                commentEditForm.dataset.commentItemContent = commentEditContent;
            };
            
            if (commentEditForm && commentItemMain && commentItemContent && commentItemFooter) {
                commentEditForm.classList.remove("hidden");
                commentEditForm.classList.add("active");
                commentItemMain.classList.add("hidden");
                commentItemContent.classList.add("hidden");
                commentItemFooter.classList.add("hidden");

                
            }
        }
    
    });
});

commentEditCancelButton.forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation();

        const commentItem = this.closest('.comment-item');

        if (commentItem) {
            const commentEditForm = commentItem.querySelector('.comment-edit-form');
            const commentItemMain = commentItem.querySelector('.comment-item-main');
            const commentItemContent = commentItem.querySelector('.comment-item-content');
            const commentItemFooter = commentItem.querySelector('.comment-item-footer');
            const commentEditFormInput = commentItem.querySelector('.comment-edit-form-input');

            const commentEditContent = commentEditForm.dataset.commentItemContent;
            
            if (commentEditForm && commentItemMain && commentItemContent && commentItemFooter) {
                commentEditForm.classList.remove("active");
                commentEditForm.classList.add("hidden");
                commentItemMain.classList.remove("hidden");
                commentItemContent.classList.remove("hidden");
                commentItemFooter.classList.remove("hidden");
                commentEditFormInput.value = commentEditContent;
            }
        }
    });
});


// 1. Находим все формы редактирования
const commentEditForms = document.querySelectorAll('.comment-edit-form');

// 2. Для каждой формы добавляем логику
commentEditForms.forEach(form => {
    const commentEditInput = form.querySelector('.comment-edit-form-input');
    const commentEditSubmit = form.querySelector('.btn-comment-edit-form[type="submit"]');
    const commentEditCancel = form.querySelector('.btn-comment-edit-form[type="button"]');
    
    // Логика блокировки/активации кнопки отправки
    if (commentEditInput && commentEditSubmit) {
        commentEditSubmit.setAttribute('disabled', 'true'); // Изначально отключена
        
        commentEditInput.addEventListener('input', function() {
            if (commentEditInput.value.trim().length > 0) {
                commentEditSubmit.removeAttribute('disabled');
            } else {
                commentEditSubmit.setAttribute('disabled', 'true');
            }
        });
    }
});



// Функция ОБНОВЛЕНИЯ ОТВЕТА

// 1. Находим СВЕРХУ ВСЕ кнопки изменить у комментариев на странице
const replyEditButton = document.querySelectorAll('.reply-edit-trigger-btn');
const replyEditCancelButton = document.querySelectorAll('.btn-reply-edit-form[type="button"]');

// 2. Запускаем цикл по всем найденным кнопкам
replyEditButton.forEach(button => {
    button.addEventListener('click', function(event) {
        // Останавливаем всплытие клика, чтобы сразу не сработал обработчик закрытия на документе
        event.stopPropagation();

        // Находим родительский контейнер опций именно ЭТОГО комментария
        const replyItem = this.closest('.reply-item');
        
        if (replyItem) {
            // Ищем блок меню СТРОГО внутри этого родительского контейнера опций
            const replyEditForm = replyItem.querySelector('.reply-edit-form');
            const replyItemMain = replyItem.querySelector('.reply-item-main');
            const replyItemContent = replyItem.querySelector('.reply-item-content');
            const replyItemFooter = replyItem.querySelector('.reply-item-footer');

            if (!replyEditForm.dataset.replyItemContent) {
                const replyEditContent = replyItemContent.textContent.trim();
                replyEditForm.dataset.replyItemContent = replyEditContent;
            };
            
            if (replyEditForm && replyItemMain && replyItemContent && replyItemFooter) {
                replyEditForm.classList.remove("hidden");
                replyEditForm.classList.add("active");
                replyItemMain.classList.add("hidden");
                replyItemContent.classList.add("hidden");
                replyItemFooter.classList.add("hidden");

                
            }
        }
    
    });
});

replyEditCancelButton.forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation();

        const replyItem = this.closest('.reply-item');

        if (replyItem) {
            const replyEditForm = replyItem.querySelector('.reply-edit-form');
            const replyItemMain = replyItem.querySelector('.reply-item-main');
            const replyItemContent = replyItem.querySelector('.reply-item-content');
            const replyItemFooter = replyItem.querySelector('.reply-item-footer');
            const replyEditFormInput = replyItem.querySelector('.reply-edit-form-input');

            const replyEditContent = replyEditForm.dataset.replyItemContent;
            
            if (replyEditForm && replyItemMain && replyItemContent && replyItemFooter) {
                replyEditForm.classList.remove("active");
                replyEditForm.classList.add("hidden");
                replyItemMain.classList.remove("hidden");
                replyItemContent.classList.remove("hidden");
                replyItemFooter.classList.remove("hidden");
                replyEditFormInput.value = replyEditContent;
            }
        }
    });
});


// 1. Находим все формы редактирования
const replyEditForms = document.querySelectorAll('.reply-edit-form');

// 2. Для каждой формы добавляем логику
replyEditForms.forEach(form => {
    const replyEditInput = form.querySelector('.reply-edit-form-input');
    const replyEditSubmit = form.querySelector('.btn-reply-edit-form[type="submit"]');
    const replyEditCancel = form.querySelector('.btn-reply-edit-form[type="button"]');
    
    // Логика блокировки/активации кнопки отправки
    if (replyEditInput && replyEditSubmit) {
        replyEditSubmit.setAttribute('disabled', 'true'); // Изначально отключена
        
        replyEditInput.addEventListener('input', function() {
            if (replyEditInput.value.trim().length > 0) {
                replyEditSubmit.removeAttribute('disabled');
            } else {
                replyEditSubmit.setAttribute('disabled', 'true');
            }
        });
    }
});


// Функция ОТВЕТА к КОММЕНТАРИЮ

const CommentReplyButton = document.querySelectorAll(".comment-item-reply")
const CommentCancelReplyButton = document.querySelectorAll(".btn-reply-form[type='button']")

CommentReplyButton.forEach(button => {
    button.addEventListener('click', function(event){
        event.stopPropagation();

        const commentItem = this.closest('.comment-item');

        if (commentItem) {
            const ReplyForm = commentItem.querySelector('.reply-form');

            if  (ReplyForm) {
                ReplyForm.classList.remove("hidden")
                ReplyForm.classList.add("active")
            }
        }
    });
});

CommentCancelReplyButton.forEach(button => {
    button.addEventListener('click', function(event){
        event.stopPropagation();

        const commentItem = this.closest('.comment-item');
        const ReplyContent = commentItem.querySelector('#reply-input');

        if (commentItem) {
            const ReplyForm = commentItem.querySelector('.reply-form');

            if  (ReplyForm) {
                ReplyForm.classList.remove("active")
                ReplyForm.classList.add("hidden")
                ReplyContent.value = '';
            }
        }
    });
});



// 1. Находим все формы ответа
const replyForms = document.querySelectorAll('.reply-form');

// 2. Для каждой формы добавляем логику
replyForms.forEach(form => {
    const replyInput = form.querySelector('.reply-form-input');
    const replySubmit = form.querySelector('.btn-reply-form[type="submit"]');
    const replyCancel = form.querySelector('.btn-reply-form[type="button"]');
    
    // Логика блокировки/активации кнопки отправки
    if (replyInput && replySubmit) {
        replySubmit.setAttribute('disabled', 'true'); // Изначально отключена
        
        replyInput.addEventListener('input', function() {
            if (replyInput.value.trim().length > 0) {
                replySubmit.removeAttribute('disabled');
            } else {
                replySubmit.setAttribute('disabled', 'true');
            }
        });
    }
    
    // Логика очистки при отмене
    if (replyCancel && replyInput) {
        replyCancel.addEventListener('click', function() {
            replyInput.value = '';
            if (replySubmit) {
                replySubmit.setAttribute('disabled', 'true');
            }
        });
    }
});



// Функция ОТВЕТА к ОТВЕТУ

const ReplyToReplyButton = document.querySelectorAll(".reply-item-reply")
const ReplyCancelReplyButton = document.querySelectorAll(".btn-reply-to-reply-form")

ReplyToReplyButton.forEach(button => {
    button.addEventListener('click', function(event){
        event.stopPropagation();

        const replyItem = this.closest('.reply-item');

        if (replyItem) {
            const ReplyToReplyForm = replyItem.querySelector('.reply-to-reply-form');

            if  (ReplyToReplyForm) {
                ReplyToReplyForm.classList.remove("hidden")
                ReplyToReplyForm.classList.add("active")
            }
        }
    });
});

ReplyCancelReplyButton.forEach(button => {
    button.addEventListener('click', function(event){
        event.stopPropagation();

        const replyItem = this.closest('.reply-item');
        const ReplyToReplyContent = replyItem.querySelector('#reply-to-reply-input');

        if (replyItem) {
            const ReplyToReplyForm = replyItem.querySelector('.reply-to-reply-form');

            if  (ReplyToReplyForm) {
                ReplyToReplyForm.classList.remove("active")
                ReplyToReplyForm.classList.add("hidden")
                ReplyToReplyContent.value = '';
            }
        }
    });
});



// 1. Находим все формы ответа
const replyToReplyForms = document.querySelectorAll('.reply-to-reply-form')

// 2. Для каждой формы добавляем логику
replyToReplyForms.forEach(form => {
    const replyToReplyInput = form.querySelector('.reply-to-reply-form-input');
    const replyToReplySubmit = form.querySelector('.btn-reply-to-reply-form[type="submit"]');
    const replyToReplyCancel = form.querySelector('.btn-reply-to-reply-form[type="button"]');
    
    // Логика блокировки/активации кнопки отправки
    if (replyToReplyInput && replyToReplySubmit) {
        replyToReplySubmit.setAttribute('disabled', 'true'); // Изначально отключена
        
        replyToReplyInput.addEventListener('input', function() {
            if (replyToReplyInput.value.trim().length > 0) {
                replyToReplySubmit.removeAttribute('disabled');
            } else {
                replyToReplySubmit.setAttribute('disabled', 'true');
            }
        });
    }
    
    // Логика очистки при отмене
    if (replyToReplyCancel && replyToReplyInput) {
        replyToReplyCancel.addEventListener('click', function() {
            replyToReplyInput.value = '';
            if (replyToReplySubmit) {
                replyToReplySubmit.setAttribute('disabled', 'true');
            }
        });
    }
});






// Функция ЧИТАТЬ ОТВЕТЫ

const toggleReplyButton = document.querySelectorAll(".toggle-reply")

toggleReplyButton.forEach(button => {
    button.addEventListener('click', function(event){
        event.stopPropagation();

        const commentItem = this.closest('.comment-item')
        const replies = commentItem.querySelector('.replies');
        
        if (replies) {
            const action = this.dataset.action; // "show" или "hide"
            
            if (action === 'show') {
                replies.classList.remove("hidden");
                replies.classList.add("active");
                const count = this.textContent.match(/\d+/)?.[0] || '0'; // Извлекаем число
                this.textContent = `Скрыть ответы (${count})`;
                this.dataset.action = "hide";
            } else if (action === 'hide') {
                replies.classList.remove("active");
                replies.classList.add("hidden");
                const count = this.textContent.match(/\d+/)?.[0] || '0';
                this.textContent = `Показать ответы (${count})`;
                this.dataset.action = "show";
            }
        }
    });
});


// функция СОРТИРОВКИ КОММЕНТАРИЕВ 


document.addEventListener("DOMContentLoaded", function () {
    const sortButtons = document.querySelectorAll('.sort-btn');
    const sortInput = document.getElementById('sort-input');

    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const chosenValue = this.getAttribute('data-value');
            sortInput.value = chosenValue;
            this.closest('form').submit();
        });
    });
});


