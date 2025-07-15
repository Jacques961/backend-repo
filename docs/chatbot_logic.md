# Chatbot Logic Documentation

- The chatbot functionality is provided via a FastAPI backend endpoint (`/chat`), which handles incoming user messages.

- There are two main chatbot interfaces:
  - **React Chatbot**: The user-facing chatbot integrated into the React frontend, designed for customers to ask questions and get quick responses.
  - **Gradio Chatbot**: An admin/support interface built with Gradio, used internally for testing, monitoring, and support purposes.

- Both interfaces use the same underlying chatbot logic:
  - Incoming messages are converted to lowercase.
  - The chatbot checks for specific keywords to determine responses:
    - "shipping" → Provides shipping information.
    - "refund" or "return" → Provides refund policy.
    - "category" or "categories" → Lists product categories.
  - If no keywords match, it responds with a fallback message such as:  
    "Sorry, I didn't understand your question. Could you please rephrase?"

- The chatbot currently follows a rule-based approach with predefined responses.

- Future plans include integrating advanced AI or OpenAI models to enhance the chatbot’s conversational abilities.
