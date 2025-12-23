# Personal Assistant - AI Bill Payment Tracker

A full-stack AI-powered personal assistant application for tracking and managing utility bills. Built with FastAPI, LangChain, and Ollama for intelligent bill management with natural language processing capabilities.

## Features

- **AI-Powered Chat Interface** - Interact with your bills using natural language via LangChain agent
- **Smart Bill Tracking** - Automatically track bills with due dates, amounts, and payment status
- **Intelligent Alerts** - Multi-level notification system (overdue, critical, urgent, upcoming)
- **RESTful API** - Complete API for programmatic bill management
- **Automatic Status Updates** - Bills automatically marked as overdue when past due date
- **Payment History** - Track when bills were paid

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - LLM orchestration framework for AI agent
- **Ollama** - Local LLM inference (gemma3:8b model)
- **Pydantic** - Data validation and settings management
- **Python 3.13** - Core programming language

### AI Agent Capabilities
The LangChain agent has access to these tools:
- Check upcoming bills (customizable time range)
- Check overdue bills
- Add new bills
- Mark bills as paid
- List all bills

## Project Structure

```
personal assistant/
├── server/
│   └── app/
│       ├── main.py              # FastAPI application & API endpoints
│       ├── agent.py             # LangChain agent initialization
│       ├── tools.py             # Agent tools for bill management
│       ├── bills_config.py      # Bill data models & database
│       ├── bill_scheduler.py   # Notification & alert system
│       └── bills_db.json        # JSON storage (auto-generated)
├── .venv/                       # Python virtual environment
├── .gitignore
└── README.md
```

## Installation

### Prerequisites
- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running
- Ollama gemma3:8b model downloaded

### Setup Steps

1. **Clone the repository**
   ```bash
   cd "personal assistant"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pydantic langchain langchain-ollama langchain-community
   ```

4. **Download Ollama model**
   ```bash
   ollama pull gemma3:8b
   ```

5. **Start the server**
   ```bash
   cd server/app
   uvicorn main:app --reload
   ```

   Or with virtual environment Python:
   ```bash
   cd server/app
   ../../.venv/Scripts/python.exe -m uvicorn main:app --reload
   ```

6. **Access the application**
   - API: http://127.0.0.1:8000
   - Interactive Docs: http://127.0.0.1:8000/docs

## API Endpoints

### Bills Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/bills` | Get all bills |
| POST | `/bills` | Create a new bill |
| GET | `/bills/upcoming?days=7` | Get upcoming bills (default: 7 days) |
| GET | `/bills/overdue` | Get overdue bills |
| GET | `/bills/alerts` | Get bill alerts with categorized notifications |
| POST | `/bills/{bill_id}/pay` | Mark a bill as paid |
| DELETE | `/bills/{bill_id}` | Delete a bill |

### AI Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message to the AI agent |

## Usage Examples

### Using the API

**Add a new bill:**
```bash
curl -X POST "http://localhost:8000/bills" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electric Bill",
    "amount": 125.50,
    "due_date": "2025-01-25",
    "provider": "Power Company",
    "account_number": "ACC-12345"
  }'
```

**Check upcoming bills:**
```bash
curl "http://localhost:8000/bills/upcoming?days=7"
```

**Get bill alerts:**
```bash
curl "http://localhost:8000/bills/alerts"
```

**Chat with AI agent:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What bills are due this week?"}'
```

**Mark bill as paid:**
```bash
curl -X POST "http://localhost:8000/bills/{bill_id}/pay"
```

### Using the Interactive Docs

Visit http://127.0.0.1:8000/docs for a full interactive API interface where you can:
- Test all endpoints directly in your browser
- View request/response schemas
- Execute API calls without writing code

## Data Models

### Bill
```python
{
  "id": "uuid",
  "name": "string",
  "amount": float,
  "due_date": "YYYY-MM-DD",
  "status": "pending" | "paid" | "overdue",
  "provider": "string",
  "account_number": "string" (optional),
  "last_paid_date": "YYYY-MM-DD" (optional)
}
```

### Alert Categories
- **Overdue**: Past due date
- **Critical**: Due today
- **Urgent**: Due tomorrow
- **Upcoming**: Due within 7 days

## AI Agent Examples

The agent understands natural language commands:

- "What bills are due this week?"
- "Show me overdue bills"
- "Add my water bill for $45 due on January 30th from City Water"
- "Mark the electric bill as paid"
- "List all my bills"

## Data Storage

Bills are stored in `bills_db.json` in the `server/app/` directory. This file is automatically created when you add your first bill.

**Example:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Electric Bill",
    "amount": 125.5,
    "due_date": "2025-01-25",
    "status": "pending",
    "auto_pay_enabled": false,
    "provider": "Power Company",
    "account_number": "ACC-12345",
    "last_paid_date": null
  }
]
```

## Security Considerations

This is a basic implementation designed for personal use. For production deployment, consider:

- [ ] Add authentication (OAuth2, JWT tokens)
- [ ] Encrypt sensitive data (account numbers)
- [ ] Use a proper database (PostgreSQL, MongoDB)
- [ ] Implement rate limiting
- [ ] Add HTTPS/TLS encryption
- [ ] Never store actual payment credentials
- [ ] Add input validation and sanitization
- [ ] Implement proper error handling
- [ ] Add logging and monitoring

## Future Enhancements

- [ ] Next.js frontend interface
- [ ] Email/SMS notifications
- [ ] Recurring bill support
- [ ] Payment history analytics
- [ ] Budget tracking
- [ ] Bank API integration (Plaid)
- [ ] Calendar integration
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Bill payment automation (with manual approval)

## Development

### Running in Development Mode

The server runs with auto-reload enabled, so changes to Python files will automatically restart the server.

```bash
cd server/app
uvicorn main:app --reload
```

### Adding New Tools to the Agent

1. Define the function in [tools.py](server/app/tools.py)
2. Create a LangChain `Tool` wrapper
3. Add the tool to the agent in [agent.py](server/app/agent.py)

### Modifying Bill Schema

1. Update the `Bill` model in [bills_config.py](server/app/bills_config.py)
2. Update API request/response models in [main.py](server/app/main.py)
3. Delete `bills_db.json` or manually migrate existing data

## Troubleshooting

### Server won't start - "ModuleNotFoundError"
Make sure you've activated the virtual environment:
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### Ollama errors
Ensure Ollama is running:
```bash
ollama serve
ollama pull gemma3:8b
```

### Port already in use
Change the port:
```bash
uvicorn main:app --reload --port 8001
```

## Contributing

This is a personal project, but suggestions and improvements are welcome!

## License

MIT License - Feel free to use and modify for your own purposes.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [LangChain](https://www.langchain.com/)
- Local LLM via [Ollama](https://ollama.ai/)

---

**Note**: This application tracks bills and sends reminders but does not automatically execute payments. All payments must be manually approved and completed by the user for security reasons.
