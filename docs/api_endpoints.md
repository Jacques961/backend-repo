# API Endpoints Documentation

## Products
- **GET /products**  
  Description: Retrieve all products  
  Response: JSON array of product objects

- **POST /products**  
  Description: Create a new product  
  Request Body: Product details in JSON  
  Response: Created product object

- **GET /products/{product_id}**  
  Description: Retrieve a product by its ID  
  Response: Product object

- **PUT /products/{product_id}**  
  Description: Update product information  
  Request Body: Updated product data in JSON  
  Response: Updated product object

- **DELETE /products/{product_id}**  
  Description: Delete a product by its ID  
  Response: Success message

- **GET /products/category/{category}**  
  Description: Retrieve products filtered by category  
  Response: JSON array of product objects

---

## Cart
- **GET /cart**  
  Description: Retrieve current cart items  
  Response: JSON array of cart item objects

- **POST /cart**  
  Description: Add an item to the cart  
  Request Body: `{ "product_id": int, "quantity": int }` (and optionally user info)  
  Response: Updated cart details

- **DELETE /cart/{product_id}**  
  Description: Remove an item from the cart by product ID  
  Response: Success message

---

## Checkout
- **POST /checkout**  
  Description: Place an order with current cart items  
  Request Body: Order and payment details  
  Response: Order confirmation

---

## Orders
- **GET /orders/{user_id}**  
  Description: Retrieve order history for a specific user  
  Response: JSON array of past orders

---

## Users
- **GET /users**  
  Description: Get a list of all users  
  Response: JSON array of user objects

- **POST /users**  
  Description: Create a new user  
  Request Body: User details in JSON  
  Response: Created user object

- **GET /users/{user_id}**  
  Description: Retrieve user details by ID  
  Response: User object

- **DELETE /users/{user_id}**  
  Description: Delete a user by ID  
  Response: Success message

---

## Chatbot
- **POST /chat**  
  Description: Send a chat message to the chatbot endpoint  
  Request Body: `{ "message": "string" }`  
  Response: Chatbot reply text

---

## Authentication
- **POST /auth/token**  
  Description: Login to get access token  
  Request Body: Credentials (username/password)  
  Response: JWT access token
