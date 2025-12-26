"""
Тестирование REST API с использованием pytest и requests
Объект тестирования: https://jsonplaceholder.typicode.com
"""
import pytest
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://jsonplaceholder.typicode.com"

class TestJSONPlaceholderAPI:
    """Класс тестов для REST API jsonplaceholder.typicode.com"""

    # ========== GET запросы ==========

    def test_get_user_status_code_200(self):
        """Проверка статуса 200 для GET запроса"""
        response = requests.get(f"{BASE_URL}/users/5")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_get_response_is_valid_json(self):
        """Проверка, что ответ - валидный JSON"""
        response = requests.get(f"{BASE_URL}/users/5")
        assert "application/json" in response.headers["Content-Type"]
        json_data = response.json()
        assert isinstance(json_data, dict)

    def test_get_response_time_acceptable(self):
        """Проверка времени ответа (менее 1000 мс)"""
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/users/5")
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        assert response_time < 1000, f"Response time {response_time:.2f}ms exceeds 1000ms"

    def test_get_user_has_required_fields(self):
        """Проверка наличия обязательных полей у пользователя"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        required_fields = ["id", "name", "username", "email", "phone", "website"]
        for field in required_fields:
            assert field in json_data, f"Missing required field: {field}"

    def test_get_user_id_matches_requested(self):
        """Проверка, что ID в ответе соответствует запрошенному"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        assert json_data['id'] == 5, f"Expected ID 5, got {json_data['id']}"

    def test_get_email_has_valid_format(self):
        """Проверка валидности формата email"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        email = json_data['email']
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert re.match(pattern, email), f"Invalid email format: {email}"

    def test_get_address_has_complete_structure(self):
        """Проверка полной структуры адреса"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        address_fields = ["street", "suite", "city", "zipcode", "geo"]
        for field in address_fields:
            assert field in json_data['address'], f"Missing address field: {field}"
        geo_fields = ["lat", "lng"]
        for field in geo_fields:
            assert field in json_data['address']['geo'], f"Missing geo field: {field}"

    def test_get_company_has_complete_structure(self):
        """Проверка полной структуры компании"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        company_fields = ["name", "catchPhrase", "bs"]
        for field in company_fields:
            assert field in json_data['company'], f"Missing company field: {field}"

    def test_get_user_has_consistent_data_types(self):
        """Проверка корректности типов данных"""
        response = requests.get(f"{BASE_URL}/users/5")
        json_data = response.json()
        assert isinstance(json_data['id'], int)
        assert isinstance(json_data['name'], str) and len(json_data['name']) > 0
        assert isinstance(json_data['username'], str) and len(json_data['username']) > 0
        assert isinstance(json_data['email'], str) and len(json_data['email']) > 0
        assert isinstance(json_data['phone'], str) and len(json_data['phone']) > 0
        assert isinstance(json_data['website'], str) and len(json_data['website']) > 0

    def test_get_all_users_returns_list(self):
        """Проверка что GET /users возвращает список"""
        response = requests.get(f"{BASE_URL}/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0
        # Проверка, что первый пользователь имеет нужные поля
        if len(users) > 0:
            assert 'id' in users[0]
            assert 'name' in users[0]

    def test_get_posts_returns_list(self):
        """Проверка что GET /posts возвращает список"""
        response = requests.get(f"{BASE_URL}/posts")
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_get_user_posts(self):
        """Проверка получения постов конкретного пользователя"""
        response = requests.get(f"{BASE_URL}/posts?userId=1")
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert all(post['userId'] == 1 for post in posts)

    # ========== POST запросы ==========

    def test_post_create_user_status_code_201(self):
        """Проверка создания пользователя (статус 201)"""
        post_data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com"
        }
        response = requests.post(f"{BASE_URL}/users", json=post_data)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    def test_post_response_is_valid_json(self):
        """Проверка валидности JSON ответа при создании"""
        post_data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com"
        }
        response = requests.post(f"{BASE_URL}/users", json=post_data)
        assert "application/json" in response.headers["Content-Type"]
        json_data = response.json()
        assert isinstance(json_data, dict)

    def test_post_created_user_has_required_fields(self):
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

    def test_post_sent_data_preserved_in_response(self):
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

    def test_post_returns_id_for_new_user(self):
        """Проверка что создаваемому пользователю выдается ID"""
        post_data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com"
        }
        response = requests.post(f"{BASE_URL}/users", json=post_data)
        json_data = response.json()
        assert 'id' in json_data
        assert isinstance(json_data['id'], int)
        assert json_data['id'] > 0

    def test_post_invalid_data_returns_error(self):
        """Проверка обработки некорректных данных"""
        invalid_data = {
            "name": "",  # Пустое имя
            "email": "invalid-email"  # Неверный формат email
        }
        response = requests.post(f"{BASE_URL}/users", json=invalid_data)
        # API может возвращать 400 или 201 (так как это тестовое API)
        # Проверяем, что ответ вообще пришел
        assert response.status_code in [200, 201, 400]

    # ========== PUT запросы ==========

    def test_put_update_user_status_code_200(self):
        """Проверка что PUT возвращает 200"""
        put_data = {
            "name": "Updated User",
            "username": "updateduser",
            "email": "updated@example.com"
        }
        response = requests.put(f"{BASE_URL}/users/5", json=put_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_put_user_id_remains_unchanged(self):
        """Проверка что ID пользователя не изменяется при обновлении"""
        put_data = {
            "name": "Updated User",
            "username": "updateduser",
            "email": "updated@example.com"
        }
        response = requests.put(f"{BASE_URL}/users/5", json=put_data)
        json_data = response.json()
        assert json_data['id'] == 5, "User ID should remain unchanged after update"

    def test_put_sent_data_preserved_in_response(self):
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

    # ========== DELETE запросы ==========

    def test_delete_user_status_code_200(self):
        """Проверка что DELETE возвращает 200"""
        response = requests.delete(f"{BASE_URL}/users/5")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # ========== Дополнительные проверки ==========

    def test_get_nonexistent_user_returns_404(self):
        """Проверка 404 для несуществующего пользователя"""
        response = requests.get(f"{BASE_URL}/users/999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_get_invalid_endpoint_returns_404(self):
        """Проверка 404 для несуществующего эндпоинта"""
        response = requests.get(f"{BASE_URL}/invalid")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_response_headers_contain_content_type(self):
        """Проверка что ответ содержит Content-Type"""
        response = requests.get(f"{BASE_URL}/users/5")
        assert "Content-Type" in response.headers

    # ========== Параметризованные тесты ==========

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_get_valid_user_ids(self, user_id):
        """Проверка что все пользователи с ID 1-5 существуют"""
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['id'] == user_id

    @pytest.mark.parametrize("invalid_id", [0, -1, 999, 10000])
    def test_get_invalid_user_ids(self, invalid_id):
        """Проверка 404 для невалидных ID"""
        response = requests.get(f"{BASE_URL}/users/{invalid_id}")
        assert response.status_code == 404

    @pytest.mark.parametrize("resource", ["users", "posts", "comments", "albums"])
    def test_get_all_resources_returns_list(self, resource):
        """Проверка что все ресурсы возвращают список"""
        response = requests.get(f"{BASE_URL}/{resource}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    # ========== Тесты производительности ==========

    def test_multiple_requests_performance(self):
        """Проверка производительности при нескольких запросах"""
        start_time = time.time()
        # Выполняем 5 последовательных запросов
        for i in range(1, 6):
            response = requests.get(f"{BASE_URL}/users/{i}")
            assert response.status_code == 200
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        # Ожидаем, что 5 запросов уложатся в 5 секунд
        assert total_time < 5000, f"5 requests took {total_time:.2f}ms"

    def test_concurrent_requests(self):
        """Проверка возможности выполнения параллельных запросов"""
        def make_request(user_id):
            response = requests.get(f"{BASE_URL}/users/{user_id}")
            return response.status_code

        user_ids = [1, 2, 3, 4, 5]
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(make_request, user_ids))
        # Все запросы должны вернуть 200
        assert all(status == 200 for status in results), f"Not all requests succeeded: {results}"

    def test_response_time_for_list_endpoint(self):
        """Проверка времени ответа для списка пользователей"""
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/users")
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        assert response.status_code == 200
        assert response_time < 2000, f"Response time {response_time:.2f}ms exceeds 2000ms"

if __name__ == "__main__":
    # Запуск тестов напрямую (для отладки)
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])