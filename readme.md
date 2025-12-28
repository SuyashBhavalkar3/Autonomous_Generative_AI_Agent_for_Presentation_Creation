# Autonomous Generative AI Agent for Presentation Creation

## 📌 Project Overview

This project is an **Autonomous Generative AI Agent** designed to automatically create professional presentations from minimal user input. The system leverages **Generative AI**, **FastAPI**, and **Google Authentication** to provide a secure, scalable, and intelligent solution for presentation creation.

Users can sign up, log in (including via **Google OAuth**), submit a topic or prompt, and receive a structured, AI-generated presentation outline or content.

---

## 🚀 Key Features

* 🔐 **Authentication System**

  * Email & Password Signup/Login
  * Google OAuth 2.0 Login (ID Token based)
* 🤖 **Generative AI Agent**

  * Converts prompts into structured presentation content
  * Slide-wise logical flow
* ⚡ **FastAPI Backend**

  * High performance REST APIs
  * Automatic API documentation with Swagger
* 🗄️ **Database Integration**

  * User management
  * Secure token handling
* 🧪 **Token Validation Utilities**

  * Google ID token verification

---

## 🏗️ Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy**
* **OAuth 2.0 (Google Authentication)**
* **JWT**

### AI

* **Generative AI / LLMs** (OpenAI / compatible models)

### Tools

* Postman / cURL for API testing
* Git & GitHub for version control

---

## 📂 Project Structure

```
backend/
│── auth/
│   ├── routes.py        # Auth routes (signup, login, google-login)
│   ├── schemas.py       # Pydantic models
│   ├── service.py       # Business logic
│   ├── gAuth.py         # Google token verification
│
│── utils/
│   ├── dependencies.py # DB dependencies
│
│── main.py              # FastAPI app entry point
│── test.py              # Google ID token validation script
│── requirements.txt
```

---

## 🔐 Authentication Flow

### 1️⃣ Email/Password Authentication

* `/auth/signup`
* `/auth/login`

### 2️⃣ Google OAuth Authentication

1. User logs in via Google
2. Frontend obtains **Google ID Token**
3. ID Token is sent to backend `/auth/google-login`
4. Backend:

   * Verifies token audience & issuer
   * Extracts user email
   * Creates or logs in user
   * Returns application JWT token

---

## 🧪 Testing Google Login (Backend Only)

You can test Google ID token validity using:

```bash
python test.py
```

The script:

* Accepts Google ID Token
* Validates audience, issuer & expiry
* Confirms whether the token is valid

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/autonomous-ai-presentation-agent.git
cd autonomous-ai-presentation-agent/backend
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv genAI_env
genAI_env\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
JWT_SECRET=your_jwt_secret
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

API Docs available at:

* Swagger UI: `http://127.0.0.1:8000/docs`
* OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

---

## 📌 Example API Call (Google Login)

```bash
curl -X POST http://127.0.0.1:8000/auth/google-login \
-H "Content-Type: application/json" \
-d '{"google_token": "<GOOGLE_ID_TOKEN>"}'
```

---

## 🔮 Future Enhancements

* Frontend integration (React / Next.js)
* PPT/PDF auto-generation
* Multi-language presentation support
* Presentation templates
* Voice-based prompt input

---

## 👨‍💻 Author

**Suyash Bhavalkar**

---

## ⭐ Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under the MIT License.