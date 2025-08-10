import requests
import json

class BookCartAPIClient:
    def __init__(self, config_path="config/config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.base_url = self.config["base_url"]
        self.headers = {"Content-Type": "application/json"}
        self.token = None

    def register_user(self, username, password, first_name, last_name, gender):
        payload = {
            "username": username,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "gender": gender
        }
        response = requests.post(
            f"{self.base_url}{self.config['api_endpoints']['register']}",
            json=payload,
            headers=self.headers
        )
        return response

    def login_user(self, username, password):
        payload = {"username": username, "password": password}
        response = requests.post(
            f"{self.base_url}{self.config['api_endpoints']['login']}",
            json=payload,
            headers=self.headers
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers["Authorization"] = f"Bearer {self.token}"
        return response

    def get_categories(self):
        response = requests.get(
            f"{self.base_url}{self.config['api_endpoints']['categories']}",
            headers=self.headers
        )
        return response

    def get_books_by_category(self, category_id):
        endpoint = self.config["api_endpoints"]["books_by_category"].format(categoryId=category_id)
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response

    def get_book_details(self, book_id):
        endpoint = self.config["api_endpoints"]["book_details"].format(bookId=book_id)
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response

    def add_to_cart(self, user_id, book_id, quantity):
        payload = {"userId": user_id, "bookId": book_id, "quantity": quantity}
        response = requests.post(
            f"{self.base_url}{self.config['api_endpoints']['add_to_cart']}",
            json=payload,
            headers=self.headers
        )
        return response
