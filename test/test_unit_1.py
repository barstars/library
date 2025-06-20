import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

pytest_plugins = ('pytest_asyncio',)

NUMBER = "1"
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "admin"

@pytest.mark.asyncio
async def test_api():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        
        # 1. Попытка регистрации администратора без JWT
        res = await client.post("/admin/register/", json={
            "username": "new_admin",
            "email": "new_admin",
            "password": "new_admin"
        })
        print(res.json())
        assert res.status_code == 400
        assert res.json()['success'] is False

        # 2. Регистрация существующего администратора без JWT
        res = await client.post("/admin/register/", json={
            "username": ADMIN_USERNAME,
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert res.status_code == 400
        assert res.json()['success'] is False

        # 3. Логин администратора
        res = await client.post("/admin/login/", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert res.status_code == 200
        jwt_admin = res.cookies.get("jwt")
        print(jwt_admin)
        

        assert jwt_admin is not None

        # 4. Создание читателя
        res = await client.post("/reader/register/", json={"username":("pipl"+NUMBER), "email":("pipl"+NUMBER), "password":("pipl"+NUMBER)})
        print(res.json())
        assert res.status_code == 200

        # 5. Регистрация книг
        book_names = [("first"+NUMBER), ("second"+NUMBER), ("third"+NUMBER), ("fourth"+NUMBER)]
        for name in book_names:
            res = await client.post("/book/register/", json={
                "name": name,
                "author": ADMIN_USERNAME,
                "copies": 5
            })
            assert res.status_code == 200
            assert res.json()['success'] is True

        # 6. Попытка регистрации книги
        res = await client.post("/book/register/", json={
            "name": "invalid",
            "author": ADMIN_USERNAME,
            "copies": -1
        })
        assert res.status_code == 400
        assert res.json()['success'] is False

        # 7. Логин как читатель
        res = await client.post("/reader/login/", json={
            "email": ("pipl"+NUMBER),
            "password": ("pipl"+NUMBER)
        })
        assert res.status_code == 200
        assert res.cookies.get("jwt")

        # 8. Получение всех книг
        res = await client.get("/book/")
        assert res.status_code == 200
        assert res.json()['success'] is True
        books = res.json()['data']

        # 9. Попытка взять более 3 книг читателем
        for i, book in enumerate(books):
            res = await client.post("/book/borrow/", json={"id": book["id"]})
            if i < 3:
                assert res.status_code == 200
                assert res.json()['success'] is True
            else:
                assert res.status_code == 400
                assert res.json()['success'] is False

        # 10. Проверка активных книг читателя
        res = await client.get("/book/getborrows/active")
        assert res.status_code == 200
        assert res.json()['success'] is True
        assert len(res.json()['data']) == 3

        # 11. Логин админа
        res = await client.post("/admin/login/", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert res.status_code == 200
        assert res.json()['success'] is True
        

        # Удаление книги, которая не выдана
        res = await client.post("/book/delete/", json={"id": books[-1]["id"]})
        assert res.status_code == 200
        assert res.json()['success'] is True

        # Удаление книги, которая уже выдана
        res = await client.post("/book/delete/", json={"id": books[0]["id"]})
        assert res.status_code == 200
        assert res.json()['success'] is True

        # Логин как читатель
        res = await client.post("/reader/login/", json={
            "email": ("pipl"+NUMBER),
            "password": ("pipl"+NUMBER)
        })
        assert res.status_code == 200
        assert res.cookies.get("jwt")

        # Проверка активных книг читателя
        res = await client.get("/book/getborrows/active")
        assert res.status_code == 200
        assert res.json()['success'] is True
        assert len(res.json()['data']) == 2