## Project Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following content:
   ```env
   OPENAPI_KEY=<your_openai_api_key>
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the API at:
   ```
   http://localhost:8000/api/
   ```

### Production Deployment
For production deployment, make sure to:
- Set `DEBUG=False` in your environment variables
- Configure proper database settings
- Set up a proper web server (e.g., Nginx + Gunicorn)
- Configure static files handling

## API Usage

BASE_URL = https://c2f4-2405-201-203f-684f-c81f-3f1-8b4c-34a7.ngrok-free.app

### 1. Ask a Question
**Endpoint:** `POST /api/ask/`

**Request:**
```json
{
    "question": "Your question here"
}
```

**Response (Success):**
```json
{
    "answer": "AI-generated answer"
}
```

**Response (Error):**
```json
{
    "error": "Error message"
}
```

**Example using fetch:**
```javascript
const askQuestion = async (question) => {
    const response = await fetch('/api/ask/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question })
    });
    return await response.json();
};
```

### 2. Get Q&A History
**Endpoint:** `GET /api/history/`

**Response:**
```json
[
    {
        "question": "First question",
        "answer": "First answer"
    },
    {
        "question": "Second question",
        "answer": "Second answer"
    }
]
```

**Example using fetch:**
```javascript
const getHistory = async () => {
    const response = await fetch('/api/history/');
    return await response.json();
};
```

### Error Handling
All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad request (missing/invalid parameters)
- 500: Server error

Always check the response status and handle errors appropriately in your frontend code.
