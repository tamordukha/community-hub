document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-like").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const form = button.closest("form");
            const url = form.action;
            const img = button.querySelector("img");
            const countSpan = button.querySelector(".like-count");
            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            })
                .then((response) => {
                    if (response.status === 401) {
                        window.location.href = "/login";  // редирект на логин
                        return;
                    }
                    return response.json();
                })
                .then((data) => {
                    if (!data) return;  // если был редирект — выходим
                    if (data.liked) {
                        img.src = "/static/icons/like_active.png";
                    } else {
                        img.src = "/static/icons/like_inactive.png";
                    }
                    countSpan.textContent = data.count;
                })
                .catch((error) => {
                    console.error("Like error:", error);
                });
        });
    });


    document.querySelectorAll(".btn-comment-like").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const form = button.closest("form");
            const url = form.action;
            const img = button.querySelector("img");
            const countSpan = button.querySelector(".comment-like-count");
            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            })
                .then((response) => {
                    if (response.status === 401) {
                        window.location.href = "/login";  // редирект на логин
                        return;
                    }
                    return response.json();
                })
                .then((data) => {
                    if (!data) return;  // если был редирект — выходим
                    if (data.liked) {
                        img.src = "/static/icons/like_active.png";
                    } else {
                        img.src = "/static/icons/like_inactive.png";
                    }
                    countSpan.textContent = data.count;
                })
                .catch((error) => {
                    console.error("Like error:", error);
                });
        });
    });


    document.querySelectorAll(".btn-reply-like").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const form = button.closest("form");
            const url = form.action;
            const img = button.querySelector("img");
            const countSpan = button.querySelector(".reply-like-count");
            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            })
                .then((response) => {
                    if (response.status === 401) {
                        window.location.href = "/login";  // редирект на логин
                        return;
                    }
                    return response.json();
                })
                .then((data) => {
                    if (!data) return;  // если был редирект — выходим
                    if (data.liked) {
                        img.src = "/static/icons/like_active.png";
                    } else {
                        img.src = "/static/icons/like_inactive.png";
                    }
                    countSpan.textContent = data.count;
                })
                .catch((error) => {
                    console.error("Like error:", error);
                });
        });
    });
});