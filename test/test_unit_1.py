from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test():
    res = client.post("/admin/login", json={
        "email": "admin",
        "password": "admin"
    })
    print(res.json())
    assert res.status_code == 200
    assert res.json()['success'] is True
    jwt_admin = res.cookies.get("jwt")
    print(jwt_admin)
    print(type(jwt_admin))

# def test():
    # 1. Попытка регистрации администратора без JWT
    # res = client.post("/admin/register", json={
    #     "username": "new_admin",
    #     "email": "new_admin",
    #     "password": "new_admin"
    # })
    # assert res.status_code == 400
    # assert res.json()['success'] is False

    # # 2. Регистрация существующего администратора без JWT
    # res = client.post("/admin/register", json={
    #     "username": "admin",
    #     "email": "admin",
    #     "password": "admin"
    # })
    # assert res.status_code == 400
    # assert res.json()['success'] is False

    # # 3. Логин администратора
    # res = client.post("/admin/login", json={
    #     "email": "admin",
    #     "password": "admin"
    # })
    # assert res.status_code == 200
    # assert res.json()['success'] is True
    # jwt_admin = res.cookies.get("jwt")
    

    # assert jwt_admin is not None

    # # 4. Создание читателя
    # res = client.post("/reader/register", json={"username":"pipl", "email":"pipl", "password":"pipl"})
    # assert res.status_code == 200
    # assert res.json()['success'] is True

    # # 5. Регистрация книг
    # book_names = ["first", "second", "third", "fourth"]
    # for name in book_names:
    #     res = client.post("/book/register", json={
    #         "name": name,
    #         "author": "admin",
    #         "copies": 5
    #     })
    #     assert res.status_code == 200
    #     assert res.json()['success'] is True

    # # 6. Попытка регистрации книги
    # res = client.post("/book/register", json={
    #     "name": "invalid",
    #     "author": "admin",
    #     "copies": -1
    # })
    # assert res.status_code == 400
    # assert res.json()['success'] is False

    # # 7. Логин как читатель
    # res = client.post("/reader/login", json={
    #     "username": "pipl",
    #     "email": "pipl"
    # })
    # assert res.status_code == 200
    # jwt_reader = res.cookies.get("jwt")
    
    # assert jwt_reader is not None

    # # 8. Получение всех книг
    # res = client.get("/book/")
    # assert res.status_code == 200
    # assert res.json()['success'] is True
    # books = res.json()['data']

    # # 9. Попытка взять более 3 книг читателем
    # for i, book in enumerate(books):
    #     res = client.post("/book/borrow", json={"id": book["id"]})
    #     if i < 3:
    #         assert res.status_code == 200
    #         assert res.json()['success'] is True
    #     else:
    #         assert res.status_code == 400
    #         assert res.json()['success'] is False

    # # 10. Проверка активных книг читателя
    # res = client.post("/book/getborrows/active")
    # assert res.status_code == 200
    # assert res.json()['success'] is True
    # assert len(res.json()['data']) == 3

    # # 11. Логин админа и удаление книг
    # res = client.post("/admin/login", json={"email": "admin", "password": "admin"})
    # jwt_admin = res.cookies.get("jwt")
    

    # # Удаление книги, которая не выдана
    # res = client.post("/book/delete", json={"id": books[-1]["id"]})
    # assert res.status_code == 200
    # assert res.json()['success'] is True

    # # Удаление книги, которая уже выдана
    # res = client.post("/book/delete", json={"id": books[0]["id"]})
    # assert res.status_code == 400  # допустим, не может удалить выданную книгу
    # assert res.json()['success'] is False

    # # Проверка активных книг читателя
    
    # res = client.post("/book/getborrows/active")
    # assert res.status_code == 200
    # assert res.json()['success'] is True
    # assert len(res.json()['data']) == 2