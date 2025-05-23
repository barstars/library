from fastapi.testclient import TestClient
from app.main import app

import uuid


client = TestClient(app)



def test():
    # 1: Пытаемся регистрировать админ без jwt
    # 1.1: новый админ регистрируем
    res = client.post("/admin/register", json={
        "username":"new_admin",
        "email": "new_admin",
        "password": "new_admin"
    })
    print(res.json())
    assert res.status_code == 400
    assert False == res.json()['success']

    # 1.2: Попытка регистраций существуещего админа
    res = client.post("/admin/register", json={
        "username":"admin",
        "email": "admin",
        "password": "admin"
    })
    print(res.json())
    assert res.status_code == 400
    assert False == res.json()['success']

    # Логин на админ
    res = client.post("/admin/login", json={
        "email": "admin",
        "password": "admin"
    })
    print(res.json())
    assert res.status_code == 200
    print(res.cookies)
    jwt = res.cookies.get("jwt")
    assert True == res.json()['success']

    # Создания читателя
    res = client.post("/reader/register", cookies={"jwt":jwt}, json={
        "username":"pipl",
        "email": "pipl",
        "password": "pipl"
    })
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    # Создания книги
    res = client.post("/book/register", cookies={"jwt":jwt}, json={
        "name":"first",
        "author": "admin",
        "copies": 5
    })
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    res = client.post("/book/register", cookies={"jwt":jwt}, json={
        "name":"asd",
        "author": "admin",
        "copies": -1
    })
    print(res.json())
    assert res.status_code == 400
    assert False == res.json()['success']

    res = client.post("/book/register", cookies={"jwt":jwt}, json={
        "name":"2",
        "author": "admin",
        "copies": 5
    })
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    res = client.post("/book/register", cookies={"jwt":jwt}, json={
        "name":"3",
        "author": "admin",
        "copies": 5
    })
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    res = client.post("/book/register", cookies={"jwt":jwt}, json={
        "name":"4",
        "author": "admin",
        "copies": 5
    })
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    # Login как читатель
    res = client.post("/reader/login", json={
        "username":"pipl",
        "email": "pipl"
    })
    print(res.json())
    assert res.status_code == 200
    jwt = res.cookies.get("jwt")
    assert True == res.json()['success']

    # Взять книгу
    # Узнать все книги
    res = client.get("/book/")
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']
    books = res.json()["data"]

    # Попытки взять всех книг то есть больше 3
    count_book = 0
    for book in range(len(books)):
        res = client.post("/book/borrow", cookies={"jwt":jwt}, json={"id":str(book.get("id"))})
        if count_book < 3:
            count_book += 1
            print(res.json())
            assert res.status_code == 200
    
            assert True == res.json()['success']
        else:
            print(res.json())
            assert res.status_code == 400
    
            assert False == res.json()['success']

    # Логин на админ
    res = client.post("/admin/login", json={
        "email": "admin",
        "password": "admin"
    })
    print(res.json())
    assert res.status_code == 200
    jwt = res.cookies.get("jwt")
    assert True == res.json()['success']

    # Удаление книги который нет в связи borrow
    res = client.post("/admin/login", cookies={"jwt":jwt}, json={
        "id": books[-1]["id"]})
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    # Удаление книги который есть в связи borrow
    res = client.post("/admin/login", cookies={"jwt":jwt}, json={
        "id": books[0]["id"]})
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']

    # Login как читатель
    res = client.post("/reader/login", json={
        "username":"pipl",
        "email": "pipl"
    })
    print(res.json())
    assert res.status_code == 200
    jwt = res.cookies.get("jwt")
    assert True == res.json()['success']

    # Взять все активные книги читателья
    res = client.post("/book/getborrows/active", cookies={"jwt":jwt})
    print(res.json())
    assert res.status_code == 200
    assert True == res.json()['success']
    assert 2 == len(res.json()['data'])

test()