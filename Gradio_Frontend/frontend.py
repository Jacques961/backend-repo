import gradio as gr
from backend.models.product_model import Create_Product
from backend.models.user_model import Create_User
from backend.models import chat_model
from backend.services import product_service
from backend.services import cart_service
from backend.services import chat_service
from backend.data.database import Cart_db, Product_db, Checkout_db, CheckoutItem_db
from backend.data.database import get_db, User_db
from sqlalchemy.orm import Session
import uuid

import requests

BASE_URL = "http://localhost:8000"  # optional if you switch to requests later

auth_token = None  # Global variable to store token

def login(username, password):
    global auth_token
    response = requests.post(f"{BASE_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        auth_token = response.json()["access_token"]
        return f"✅ Logged in as {username}"
    else:
        auth_token = None
        return f"❌ Login failed: {response.text}"

# ========== PRODUCT FUNCTIONS ==========
def view_products(category=None):
    if category and category.lower() != "all":
        response = requests.get(f"{BASE_URL}/products/category/{category}")
    else:
        response = requests.get(f"{BASE_URL}/products")

    if response.status_code != 200:
        return []

    products = response.json()
    return [(p['image'], f"ID: {p['id']} | {p['name']} - ${p['price']}") for p in products]

def add_product(name, category, price, image_url):
    payload = {
        "name": name,
        "category": category,
        "price": price,
        "image": image_url
    }

    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.post(f"{BASE_URL}/products", json=payload, headers=headers)

    if response.status_code == 200:
        product = response.json()
        return f"✅ Product '{product['name']}' added with ID: {product['id']}"
    return f"❌ Error: {response.text}"

def update_product(product_id, name, category, price, image_url):
    payload = {
        "name": name or "string",
        "category": category or "string",
        "price": price,
        "image": image_url or "string"
    }

    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=payload, headers=headers)

    if response.status_code == 200:
        updated = response.json()
        return f"✅ Product '{updated['name']}' updated."
    return f"❌ Error: {response.text}"


def delete_product(product_id):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)

    if response.status_code == 200:
        deleted = response.json()
        return f"🗑️ Product '{deleted['name']}' deleted."
    return f"❌ Error: {response.text}"


# ========== USER FUNCTIONS ==========
def view_users():
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code != 200:
        return "No users found."
    users = response.json()
    return "\n".join([f"ID: {u['id']} | Name: {u['name']}" for u in users])

def add_user(name: str):
    payload = {"name": name}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    if response.status_code == 200:
        user = response.json()
        return f"✅ User '{user['name']}' added with ID: {user['id']}"
    return f"❌ {response.text}"

def delete_user(user_id):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    if response.status_code == 200:
        user = response.json()
        return f"🗑️ User '{user['name']}' deleted."
    return "❌ User not found."

# ========== CART FUNCTIONS ==========
def view_cart(user_id: int):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.get(f"{BASE_URL}/cart/{user_id}", headers=headers)
    if response.status_code != 200:
        return "🛒 Cart is empty."

    data = response.json()
    items = data["items"]
    total = data["total"]
    lines = [f"{item['product']['name']} x{item['quantity']} - ${item['product']['price'] * item['quantity']:.2f}" for item in items]
    lines.append(f"\n💰 Total: ${total:.2f}")
    return "\n".join(lines)

def add_to_cart(user_id: int, product_id: str, quantity: int):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    payload = {
        "product_id": product_id,
        "quantity": quantity
    }
    params = {
        "user_id": user_id
    }
    response = requests.post(f"{BASE_URL}/cart", json=payload, params=params, headers=headers)

    if response.status_code == 200:
        item = response.json()
        return f"✅ Added {quantity} of '{item['product']['name']}' to user {user_id}'s cart."
    return f"❌ {response.text}"

def remove_from_cart(user_id: int, product_id: str):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

    response = requests.delete(f"{BASE_URL}/cart/{user_id}/{product_id}", headers=headers)
    if response.status_code == 200:
        return f"🗑️ {response.json()['message']}"
    return f"❌ Item not found in cart."

def checkout_cart(user_id: int):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.post(f"{BASE_URL}/checkout/{user_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        return f"✅ Checkout completed!\nCheckout ID: {result['checkout_id']}\nTotal: ${result['total']:.2f}"
    return "❌ Cart is empty. Nothing to checkout."

def get_order_history(user_id: int):
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    response = requests.get(f"{BASE_URL}/orders/{user_id}", headers=headers)
    if response.status_code != 200:
        return "No orders found for this user."
    orders = response.json()
    history_lines = []

    for order in orders:
        order_header = f"🧾 Order #{order['checkout_id']} - Total: ${order['total_price']:.2f}"
        history_lines.append(order_header)

        for item in order["items"]:
            # Format the date nicely (optional)
            date_str = item["date"].split("T")[0]  # just the date part
            product_line = (
                f"  🛍️ {item['product_name']} (x{item['quantity']}) "
                f"@ ${item['unit_price']:.2f} = ${item['total']:.2f} "
                f"on {date_str}"
            )
            history_lines.append(product_line)

        history_lines.append("-" * 40)  # separator line

    return "\n".join(history_lines)

# ========== CHAT FUNCTIONS ==========
def chat_with_bot(message: str, history: list):
    payload = {"message": message}
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        return f"❌ Error: {response.text}"
    except Exception as e:
        return f"❌ Request failed: {e}"

# ========== GRADIO UI ==========
with gr.Blocks() as demo:
    with gr.Tab("📦 Products"):
        with gr.Tab("📃 View Products"):
            category_input = gr.Textbox(label="Filter by Category (or leave empty)")
            product_refresh = gr.Button("🔄 Refresh Product List")
            product_gallery = gr.Gallery(label="All Products")
            product_refresh.click(fn=view_products, inputs=[category_input], outputs=product_gallery)

        with gr.Tab("➕ Add Product"):
            name = gr.Textbox(label="Name")
            category = gr.Textbox(label="Category")
            price = gr.Number(label="Price")
            image_url = gr.Textbox(label="Image URL")
            add_btn = gr.Button("Add Product")
            add_output = gr.Textbox(label="Result")
            add_btn.click(fn=add_product, inputs=[name, category, price, image_url], outputs=add_output)

        with gr.Tab("✏️ Update Product"):
            upd_id = gr.Textbox(label="Product ID")
            upd_name = gr.Textbox(label="New Name")
            upd_category = gr.Textbox(label="New Category")
            upd_price = gr.Number(label="New Price")
            upd_image = gr.Textbox(label="New Image URL")
            upd_btn = gr.Button("Update Product")
            upd_output = gr.Textbox(label="Result")
            upd_btn.click(fn=update_product, inputs=[upd_id, upd_name, upd_category, upd_price, upd_image], outputs=upd_output)

        with gr.Tab("🗑️ Delete Product"):
            del_id = gr.Textbox(label="Product ID")
            del_btn = gr.Button("Delete Product")
            del_output = gr.Textbox(label="Result")
            del_btn.click(fn=delete_product, inputs=[del_id], outputs=del_output)

    with gr.Tab("👤 Users"):
        with gr.Tab("📋 View Users"):
            view_user_btn = gr.Button("🔄 Refresh User List")
            user_list_output = gr.Textbox(label="User List", lines=10)
            view_user_btn.click(fn=view_users, outputs=user_list_output)

        with gr.Tab("➕ Add User"):
            user_name = gr.Textbox(label="User Name")
            user_add_btn = gr.Button("Add User")
            user_add_output = gr.Textbox(label="Result")
            user_add_btn.click(fn=add_user, inputs=[user_name], outputs=user_add_output)

        with gr.Tab("🗑️ Delete User"):
            del_user_id = gr.Number(label="User ID")
            del_user_btn = gr.Button("Delete User")
            del_user_output = gr.Textbox(label="Result")
            del_user_btn.click(fn=delete_user, inputs=[del_user_id], outputs=del_user_output)
    
    with gr.Tab("🛒 Cart"):
        with gr.Tab("📋 View Cart"):
            cart_user_id = gr.Number(label="User ID")
            view_cart_btn = gr.Button("View Cart")
            cart_output = gr.Textbox(label="Cart Details", lines=10)
            view_cart_btn.click(fn=view_cart, inputs=[cart_user_id], outputs=cart_output)

        with gr.Tab("➕ Add to Cart"):
            add_user_id = gr.Number(label="User ID")
            add_product_id = gr.Textbox(label="Product ID")
            add_quantity = gr.Number(label="Quantity", value=1)
            add_cart_btn = gr.Button("Add Item")
            add_cart_output = gr.Textbox(label="Result")
            add_cart_btn.click(fn=add_to_cart, inputs=[add_user_id, add_product_id, add_quantity], outputs=add_cart_output)

        with gr.Tab("🗑️ Remove from Cart"):
            rem_user_id = gr.Number(label="User ID")
            rem_product_id = gr.Textbox(label="Product ID")
            rem_cart_btn = gr.Button("Remove Item")
            rem_cart_output = gr.Textbox(label="Result")
            rem_cart_btn.click(fn=remove_from_cart, inputs=[rem_user_id, rem_product_id], outputs=rem_cart_output)

        with gr.Tab("💳 Checkout"):
            checkout_user_id = gr.Number(label="User ID")
            checkout_btn = gr.Button("Checkout Now")
            checkout_output = gr.Textbox(label="Result")
            checkout_btn.click(fn=checkout_cart, inputs=[checkout_user_id], outputs=checkout_output)
        
        with gr.Tab("📜 Order History"):
            history_user_id = gr.Number(label="User ID")
            history_btn = gr.Button("Show Order History")
            history_output = gr.Textbox(label="Order History", lines=10)
            history_btn.click(fn=get_order_history, inputs=[history_user_id], outputs=history_output)
    
    with gr.Tab("🤖 Chat Bot"):
        chatbot = gr.ChatInterface(
            fn=chat_with_bot,
            title="🛍️ Shopping Assistant",
            textbox=gr.Textbox(placeholder="Ask me anything about shipping, products, or returns..."),
        )
    with gr.Tab("🔐 Login"):
        login_username = gr.Textbox(label="Username")
        login_password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_output = gr.Textbox(label="Login Status")
        login_btn.click(fn=login, inputs=[login_username, login_password], outputs=login_output)


    
if __name__ == "__main__":
    demo.launch()
