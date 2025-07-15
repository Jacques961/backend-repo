from fastapi import FastAPI
from backend.routes import product_route, cart_route, user_route, chat_route, auth_route
from backend.data.database import Base, engine
import gradio as gr

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(product_route.router)
app.include_router(cart_route.router)
app.include_router(user_route.router)
app.include_router(chat_route.router)
app.include_router(auth_route.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI E-commerce App"}





