# Community Hub

Социальная платформа на Flask с ролями, системой прав доступа, вложенными комментариями и лайками.

## Возможности

- Три роли пользователей: user, moderator, admin
- Публичные и приватные посты
- Комментарии и вложенные ответы
- Лайки постов и комментариев
- Загрузка аватарок
- Сортировка комментариев
- Полное тестирование прав доступа

## Установка

```bash
git clone <url>
cd community-hub
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## Запуск
```bash
flask run
```

## Тесты
```bash
pytest
```
