# Chatbot Logic Documentation

- The chatbot receives user messages via the `/chat` POST endpoint.
- Incoming messages are processed by:
  - Converting to lowercase.
  - Checking for certain keywords and responding accordingly:
    - "shipping" → Returns shipping info message.
    - "refund" or "return" → Returns refund policy info.
    - "category" or "categories" → Lists available product categories.
  - If no keywords match, a fallback message is returned, e.g.,  
    "Sorry, I didn't understand your question. Could you please rephrase?"
- The chatbot currently uses a rule-based approach.
- Future plans include integrating OpenAI or other language models for enhanced responses.
- The chatbot is implemented as a FastAPI route, making it accessible to both React frontend and Gradio admin interfaces.
