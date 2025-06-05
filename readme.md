# Inventory Management System

A full-stack inventory management system with a FastAPI backend and Streamlit frontend.  
Manage inventory items by adding, updating, deleting, and filtering through a simple UI.

---

## Features

### Backend (FastAPI)

- Add new inventory items with optional AI-generated descriptions
- Update and delete items by UUID
- Search items by name, category, status, quantity, and description content
- In-memory store (for demo/testing purposes)
- REST API with JSON responses

### Frontend (Streamlit)

- Add new inventory items via form
- View and filter inventory items live
- Communicates with backend via HTTP requests

---

## Tech Stack

- Backend: [FastAPI](https://fastapi.tiangolo.com/)
- Frontend: [Streamlit](https://streamlit.io/)
- Python data models with Pydantic
- UUIDs for item identifiers
- OpenAI GPT API for description generation and adding items NLP

---

## Getting Started

### Prerequisites

- Python 3.7 or newer
- [pip](https://pip.pypa.io/en/stable/installation/)
- pip install -r requirements.txt

### Installation

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd <repo_folder>
   ```

## Setup Instructions

### 1. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### 2. Create .env file and add the api key of openai

pip install fastapi uvicorn streamlit requests pydantic openai python-dotenv or pip install -r requirements.txt

Backend API

uvicorn app:app --reload --host 0.0.0.0 --port 8000
The API will be available at: http://localhost:8000

Frontend Streamlit App

streamlit run app.py
The app will open in your browser at: http://localhost:8501
```
