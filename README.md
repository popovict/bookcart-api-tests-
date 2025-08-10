# bookcart-api-tests-
This repository contains automated API tests for the BookCart application (https://bookcart.azurewebsites.net). The tests focus on validating core user flows, including user registration, login, browsing books, and adding items to the cart, using Python, `pytest`, and the `requests` library.

## API Test Cases
Below are test cases focusing on real user flows, combining multiple API calls where applicable to simulate realistic scenarios. Each test case includes a description, preconditions, steps, and expected results.

**Test Case 1: Register and Login User**<br />
* Description: Simulate a new user registering and logging in to obtain an authentication token.<br/>
* Category: Positive<br />
* Preconditions: None<br />
* Steps:
1. POST /api/User/register with valid user data (e.g., username, password, firstName, lastName, gender).
2. Verify the response status is 200 and contains a userId.
3. POST /api/User/login with the same username and password.
4. Verify the response status is 200 and returns a JWT token.

* Expected Result:<br />
* Registration: 200 OK, userId returned.<br />
* Login: 200 OK, valid JWT token returned.<br />
* Priority: High (core functionality)  

**Test Case 2: Browse Books and Add to Cart**<br />
* Description: Simulate a user browsing books by category, retrieving book details, and adding a book to their cart.<br />
* Category: Positive<br />
* Preconditions: User is authenticated (token from login).<br />
* Steps:  
1. GET /api/Book/categories to retrieve available categories.
2. Verify the response status is 200 and contains a list of categories.
3. GET /api/Book?categoryId={categoryId} using a categoryId from step 1.
4. Verify the response status is 200 and returns a list of books.
5. GET /api/Book/{bookId} for a specific book from step 3.
6. Verify the response status is 200 and returns book details.
7. POST /api/ShoppingCart with userId, bookId, and quantity.
8. Verify the response status is 200 and the book is added to the cart.

* Expected Result:
  - Categories retrieved successfully.<br />
  - Books retrieved for the selected category.<br />
  - Book details retrieved successfully.<br />
  - Book added to cart, 200 OK.<br />

* Priority: High (core e-commerce flow)  

**Test Case 3: Add and Remove Book from Favorites**<br />
* Description: Simulate a user adding a book to their favorites and then removing it.<br />
* Category: Positive<br />
* Preconditions: User is authenticated, bookId exists.<br />
* Steps:<br />
1. POST /api/Favourite with userId and bookId.
2. Verify the response status is 200 and the book is added to favorites.
3. GET /api/Favourite/{userId} to retrieve the user’s favorites.
4. Verify the response status is 200 and includes the bookId.
5. DELETE /api/Favourite/{userId}/{bookId} to remove the book.
6. Verify the response status is 200.
7. GET /api/Favourite/{userId} again.
8. Verify the bookId is no longer in the favorites list.

* Expected Result:<BR />
  - Book added to favorites, 200 OK.<br />
  - Favorites list includes the book.<br />
  - Book removed from favorites, 200 OK.<br />
  - Favorites list no longer includes the book.<br />

* Priority: Medium

**Test Case 4: Invalid Login Attempt**  
* Description: Attempt to log in with incorrect credentials.<br />
* Category: Negative<br />
* Preconditions: None<br />
* Steps:<br />
1. POST /api/User/login with invalid username or password.<br />
2. Verify the response status is 401 Unauthorized or similar error code.<br />

* Expected Result:  
  - 401 Unauthorized, error message indicating invalid credentials.<br />
* Priority: Medium<br />

**Test Case 5: Add Non-Existent Book to Cart**  
* Description: Attempt to add a book with an invalid bookId to the cart.<br />
* Category: Negative<br />
* Preconditions: User is authenticated.<br />
* Steps:  
1. POST /api/ShoppingCart with userId and an invalid bookId (e.g., 99999).<br />
2. Verify the response status is 400 Bad Request or similar error code.<br />

* Expected Result: 400 Bad Request, error message indicating invalid bookId.<br />
* Priority: Medium<br />

**Test Case 6: Update Cart with Invalid Quantity**  
* Description: Attempt to update the cart with an invalid quantity (e.g., negative or zero).<br />
* Category: Negative<br />
* Preconditions: User is authenticated, book is in cart.<br />
* Steps:  
1. POST /api/ShoppingCart to add a book to the cart.<br />
2. PUT /api/ShoppingCart with userId, bookId, and quantity = -1 or 0.<br />
3. Verify the response status is 400 Bad Request or similar error code.<br />

* Expected Result: 400 Bad Request, error message indicating invalid quantity.<br />
* Priority: Medium  

**Smoke Test Identification**  
Smoke Test:  
Test Case 1 (Register and Login User) and Test Case 2 (Browse Books and Add to Cart).  
Rationale: These test cases cover the core user flows of the application:  
Test Case 1 ensures user authentication, which is critical for accessing protected endpoints.< br />
Test Case 2 validates the primary e-commerce functionality (browsing books and adding to cart), which is central to the application’s purpose.

Smoke tests are designed to verify the stability of the system’s core features. These two test cases cover authentication and the primary shopping flow, making them ideal candidates.

**Positive and Negative Test Cases**  
Positive Test Cases:  
* Test Case 1: Register and Login User
* Test Case 2: Browse Books and Add to Cart
* Test Case 3: Add and Remove Book from Favorites

Negative Test Cases:  
* Test Case 4: Invalid Login Attempt
* Test Case 5: Add Non-Existent Book to Cart
* Test Case 6: Update Cart with Invalid Quantity
* Test Case 7: Retrieve Book by Invalid ID

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/popovict/bookcart-api-tests-.git
   cd bookcart-api-tests
  
2. **Create a virual environment**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Run Tests:**
   ```bash
   pytest tests/test_smoke.py -v

## Bug Reporting

During the investigation and test creation, I encountered the following potential issues with the API. These are based on assumptions from the Swagger documentation and typical API behavior, as I couldn’t execute the tests due to the hypothetical nature of this response.

**Bug 1: Lack of Input Validation on Registration**  
Description: The /api/User/register endpoint may accept weak passwords or invalid email formats.<br />

Steps to Reproduce:<br />
1. POST /api/User/register with payload {"username": "testuser", "password": "123", "firstName": "Test", "lastName": "User", "gender": "Male"}.<br />
2. Observe the response.<br />

Expected Behavior: 400 Bad Request with an error message about password complexity (e.g., requiring minimum length, special characters).<br />
Actual Behavior: (Hypothetical) Accepts weak password, returns 200 OK.<br />
Severity: Medium<br />
Notes: Needs verification with actual API execution.<br />

**Bug 2: No Rate Limiting on Login Endpoint**  
Description: The /api/User/login endpoint may not have rate limiting, allowing brute-force attacks.<br />

Steps to Reproduce:<br />
1. Send multiple POST requests to /api/User/login with incorrect credentials in rapid succession.<br />
2. Check if the API responds with 429 Too Many Requests after a threshold.<br />

Expected Behavior: 429 Too Many Requests after excessive attempts.<br />
Actual Behavior: (Hypothetical) Continues to respond with 401 Unauthorized without rate limiting.<br />
Severity: High<br />
Notes: Security concern; needs testing to confirm.<br />

**Bug 3: Inconsistent Error Messages**  
Description: Negative test cases (e.g., invalid bookId) may return generic error messages instead of specific ones.<br />

Steps to Reproduce:  
1. GET /api/Book/99999 with an invalid bookId.<br />
2. Observe the error message in the response.<br />

Expected Behavior: 404 Not Found with a message like “Book with ID 99999 not found.”<br />
Actual Behavior: (Hypothetical) Generic 404 or 500 error without clear details.<br />
Severity: Low<br />
Notes: Improves developer experience; needs verification<br />















