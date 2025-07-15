from backend.models import chat_model

def chat_bot(message: str):
    message = message.lower()

def chat_bot(message: str):
    message = message.lower()

    if any(greet in message for greet in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "👋 Hello! Welcome to our shop. How can I assist you today?"

    if 'shipping' in message:
        return '📦 Shipping usually takes 4 to 5 working days. You’ll receive a tracking link once it’s shipped.'
    
    elif 'refund' in message or 'return' in message:
        return "💸 Refunds are processed within 7 days of receiving the returned item. Make sure it's in its original condition."
    
    elif 'category' in message or 'categories' in message:
        return '🛍️ We offer various product categories like electronics, clothing, and toys. You can browse them on the products page.'

    elif 'product' in message or 'products' in message:
        return ("🛒 You can find detailed product information, prices, and reviews on each product page. "
                "Use the search bar to quickly find what you need!")

    elif 'cancel' in message:
        return '❌ To cancel an order, please contact support within 12 hours of placing the order.'

    elif 'help' in message:
        return ("🧠 I can assist with shipping, refunds, categories, payments, order status, and more.\n"
                "Just ask a question like: 'How do I track my order?' or 'What payment methods are accepted?'")

    else:
        return "🤖 I'm not sure I understood that. Please ask me about shipping, refunds, categories, products, or support."