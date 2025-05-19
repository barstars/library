from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_login_admin():
    res = client.post("/admin/login", json={
        "email": "admin@gmail.com",
        "password": "admin"
    })
    assert res.status_code == 200
    assert "jwt" in res.cookies
    print("JWT:", res.cookies.get("jwt"))

def test_register_admin():
    # тут client уже содержит куку с JWT после test_login_admin
    res = client.post("/admin/register", json={
        "username": "new_admin",
        "email": "new_admin@gmail.com",
        "password": "newadmin"
        , cookies=admin_cookie})
    assert res.status_code == 200
    print("Регистрация:", res.json())

def test_login_newadmin():
    res = client.post("/admin/login", json={
        "email": "new_admin@gmail.com",
        "password": "newadmin"
    })
    assert res.status_code == 200
    print("Новый логин:", res.json())
