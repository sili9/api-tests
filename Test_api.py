import pytest
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://jsonplaceholder.typicode.com"

# --------------------- GET запросы ---------------------

def test_get_user_status_code_200():
    """Проверка что GET запрос возвращает 200"""
    response = requests.get(f"{BASE_URL}/users/5")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_get_response_is_valid_json():
    """Проверка что ответ содержит валидный JSON"""
    response = requests.get(f"{BASE_URL}/users/5")
    assert "application/json" in response.headers["Content-Type"]
    json_data = response.json()
    assert isinstance(json_data, dict)

def test_get_response_time_acceptable():
    """Проверка времени ответа < 1000ms"""
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/users/5")
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    assert response_time < 1000, f"Response time {response_time:.2f}ms exceeds 1000ms"

def test_get_user_has_required_fields():
    """Проверка наличия обязательных полей"""
    response = requests.get(f"{BASE_URL}/users/5")
    json_data = response.json()
    required_fields = ["id", "name", "username", "email", "phone", "website"]
    for field in required_fields:
        assert field in json_data, f"Missing required field: {field}"

def test_get_email_has_valid_format():
    """Проверка формата email"""
    response = requests.get(f"{BASE_URL}/users/5")
    json_data = response.json()
    email = json_data["email"]
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    assert re.match(pattern, email), f"Invalid email format: {email}"

def test_get_address_has_complete_structure():
    """Проверка структуры адреса"""
    response = requests.get(f"{BASE_URL}/users/5")
    json_data = response.json()
    address_fields = ["street", "suite", "city", "zipcode", "geo"]
    for field in address_fields:
        assert field in json_data["address"], f"Missing address field: {field}"

    geo_fields = ["lat", "lng"]
    for field in geo_fields:
        assert field in json_data["address"]["geo"], f"Missing geo field: {field}"

def test_get_company_has_complete_structure():
    """Проверка структуры компании"""
    response = requests.get(f"{BASE_URL}/users/5")
    json_data = response.json()
    company_fields = ["name", "catchPhrase", "bs"]
    for field in company_fields:
        assert field in json_data["company"], f"Missing company field: {field}"

# --------------------- POST запросы ---------------------

def test_post_create_user_status_code_201():
    """Проверка что POST возвращает 201"""
    post_data = {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=post_data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

def test_post_response_is_valid_json():
    """Проверка валидности JSON в POST ответе"""
    post_data = {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=post_data)
    assert "application/json" in response.headers["Content-Type"]
    json_data = response.json()
    assert isinstance(json_data, dict)

def test_post_created_user_has_required_fields():
    """Проверка обязательных полей в созданном пользователе"""
    post_data = {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=post_data)
    json_data = response.json()
    required_fields = ["id", "name", "username", "email"]
    for field in required_fields:
        assert field in json_data, f"Missing required field: {field}"

def test_post_sent_data_preserved_in_response():
    """Проверка что отправленные данные присутствуют в ответе"""
    post_data = {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=post_data)
    json_data = response.json()
    assert json_data['name'] == post_data['name']
    assert json_data['username'] == post_data['username']
    assert json_data['email'] == post_data['email']

# --------------------- PUT запросы ---------------------

def test_put_update_user_status_code_200():
    """Проверка что PUT возвращает 200"""
    put_data = {
        "name": "Updated User",
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/5", json=put_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_put_user_id_remains_unchanged():
    """Проверка что ID пользователя не изменяется при обновлении"""
    put_data = {
        "name": "Updated User",
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/5", json=put_data)
    json_data = response.json()
    assert json_data['id'] == 5, "User ID should remain unchanged after update"

def test_put_sent_data_preserved_in_response():
    """Проверка что обновленные данные присутствуют в ответе"""
    put_data = {
        "name": "Updated User",
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/5", json=put_data)
    json_data = response.json()
    assert json_data['name'] == put_data['name']
    assert json_data['username'] == put_data['username']
    assert json_data['email'] == put_data['email']

# --------------------- DELETE запросы ---------------------

def test_delete_user_status_code_200():
    """Проверка что DELETE возвращает 200"""
    response = requests.delete(f"{BASE_URL}/users/5")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# --------------------- Дополнительные проверки ---------------------

def test_get_nonexistent_user_returns_404():
    """Проверка 404 для несуществующего пользователя"""
    response = requests.get(f"{BASE_URL}/users/999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

def test_get_all_users_returns_list():
    """Проверка что GET /users возвращает список"""
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert 'id' in users[0]
    assert 'name' in users[0]

def test_get_posts_returns_list():
    """Проверка что GET /posts возвращает список"""
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0

def test_get_user_posts():
    """Проверка получения постов конкретного пользователя"""
    response = requests.get(f"{BASE_URL}/posts?userId=1")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert all(post['userId'] == 1 for post in posts)

# --------------------- Производительность ---------------------

def test_multiple_requests_performance():
    """Проверка что 5 последовательных запросов выполняются за < 5000ms"""
    start_time = time.time()
    for i in range(1, 6):
        response = requests.get(f"{BASE_URL}/users/{i}")
        assert response.status_code == 200
    total_time = (time.time() - start_time) * 1000
    assert total_time < 5000, f"5 requests took {total_time:.2f}ms"

def test_concurrent_requests():
    """Проверка одновременных запросов"""
    def make_request(user_id):
        return requests.get(f"{BASE_URL}/users/{user_id}").status_code

    user_ids = [1, 2, 3, 4, 5]
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(make_request, user_ids))
    assert all(status == 200 for status in results), f"Not all requests succeeded: {results}"

# --------------------- Параметризованные тесты ---------------------

@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
def test_get_valid_user_ids(user_id):
    """Проверка что все пользователи с ID 1-5 существуют"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200

@pytest.mark.parametrize("invalid_id", [0, -1, 999, 10000])
def test_get_invalid_user_ids(invalid_id):
    """Проверка 404 для невалидных ID"""
    response = requests.get(f"{BASE_URL}/users/{invalid_id}")
    assert response.status_code == 404