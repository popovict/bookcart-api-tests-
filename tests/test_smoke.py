import pytest
import time
from utils.api_client import BookCartAPIClient

@pytest.fixture(scope="module")
def api_client():
    return BookCartAPIClient()

def test_register_and_login(api_client):
    # Generate unique username to avoid conflicts
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    password = "Test@123"
    first_name = "Test"
    last_name = "User"
    gender = "Male"

    # Register user
    response = api_client.register_user(username, password, first_name, last_name, gender)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    user_id = response.json().get("userId")
    assert user_id is not None, "User ID not returned"

    # Login user
    response = api_client.login_user(username, password)
    assert response.status_code == 200, f"Login failed: {response.text}"
    assert response.json().get("token"), "Token not returned"

    return user_id  # Return user_id for use in other tests

def test_browse_and_add_to_cart(api_client, test_register_and_login):
    user_id = test_register_and_login

    # Get categories
    response = api_client.get_categories()
    assert response.status_code == 200, f"Failed to retrieve categories: {response.text}"
    categories = response.json()
    assert len(categories) > 0, "No categories returned"
    category_id = categories[0]["categoryId"]

    # Get books by category
    response = api_client.get_books_by_category(category_id)
    assert response.status_code == 200, f"Failed to retrieve books: {response.text}"
    books = response.json()
    assert len(books) > 0, "No books returned"
    book_id = books[0]["bookId"]

    # Get book details
    response = api_client.get_book_details(book_id)
    assert response.status_code == 200, f"Failed to retrieve book details: {response.text}"
    assert response.json()["bookId"] == book_id, "Incorrect book details"

    # Add book to cart
    response = api_client.add_to_cart(user_id, book_id, 1)
    assert response.status_code == 200, f"Failed to add book to cart: {response.text}"
