# 🛍️ AI-Powered E-Commerce App

## Overview
This project is an AI-powered e-commerce platform with the following stack:

- **Frontend**: React chatbot (Vite)
- **Backend**: FastAPI
- **Chatbot**: OpenAI / Local model (via FastAPI routes)
- **Gradio**: Admin/Support frontend for backend services
- **Database**: SQLite

## Project Structure
```

project/
├── backend/          # FastAPI models, routes, services
├── frontend/         # React chatbot (Vite)
│   └── app/
├── frontend.py       # Gradio-based interface
├── main.py           # FastAPI entry point
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md

````

## Setup Instructions

### Backend (FastAPI)
```bash
pip install -r requirements.txt
uvicorn main:app --reload
````

### Frontend (React)

```bash
cd frontend/app
npm install
npm run dev
```

### Gradio Interface

```bash
python frontend.py
```

## Features

* ✅ Product & Cart APIs
* ✅ Chatbot Support
* ✅ React Chat UI
* 🔄 Auth with JWT (work in progress)
* 🔄 Stripe integration (optional)

## License

MIT License

© 2025 Jacques El Nahri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[The full MIT License text can be found here](https://choosealicense.com/licenses/mit/)
