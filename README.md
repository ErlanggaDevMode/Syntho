# Syntho

> A self-hosted AI assistant for notes, expenses, and personal insights.

Syntho helps you capture expenses, ideas, reminders, and daily notes through Telegram using natural language.

Instead of opening multiple apps or filling out forms, you can simply send a message like:

* "Bought coffee for 20k"
* "Salary received: 3 million"
* "Remind me to pay electricity next Friday"
* "Idea: build a dashboard for temple inventory management"

Syntho automatically organizes your information, stores it securely, and generates useful reports and insights.

---

## Features

### Expense Tracking

* Record income and expenses using natural language
* Automatic category detection
* Transaction history and filtering
* Monthly summaries and spending analysis

### Notes & Knowledge Capture

* Quick note-taking through Telegram
* Automatic tagging and summarization
* Searchable note archive
* Convert notes into reminders or tasks

### Reporting & Insights

* Daily, weekly, and monthly reports
* Spending trends and patterns
* Personalized recommendations
* Export to PDF and spreadsheet formats

### Telegram Integration

* Chat-first experience
* Instant notifications
* Scheduled reminders
* Fast commands and shortcuts

### Privacy First

* Fully self-hosted
* Local AI inference with Ollama
* No external AI API required
* Your data stays under your control

---

## Tech Stack

| Layer         | Technology          |
| :------------ | :------------------ |
| Frontend      | React + TypeScript  |
| Backend       | FastAPI             |
| Database      | PostgreSQL          |
| Cache         | Redis               |
| AI Runtime    | Ollama              |
| Default Model | kwangsuklee/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF |
| Bot Framework | python-telegram-bot |
| Scheduling    | APScheduler         |
| Containers    | Docker Compose      |
| CI/CD         | GitHub Actions      |

---

## Architecture

```text
Telegram User
      │
      ▼
Telegram Bot
      │
      ▼
FastAPI Backend
      │
 ┌────┼───────────┐
 ▼    ▼           ▼

AI  PostgreSQL  Redis
 │
 ▼

Ollama
 │
 ▼

Web Dashboard
```

---

## Project Structure

```text
syntho/
├── backend/
├── frontend/
├── bot/
├── ai/
├── infrastructure/
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── AGENTS.md
│   ├── API_SPEC.md
│   ├── DATABASE_SCHEMA.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   ├── ROADMAP.md
│   ├── TESTING.md
│   └── OBSERVABILITY.md
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Docker
* Docker Compose
* Git

Optional:

* Make

---

### Clone the Repository

```bash
git clone https://github.com/your-username/syntho.git

cd syntho
```

---

### Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update the required values:

```env
TELEGRAM_BOT_TOKEN=
JWT_SECRET=
```

See `docs/ENVIRONMENT_VARIABLES.md` for the full configuration reference.

---

### Start the Development Environment

On Linux/macOS:
```bash
docker compose up -d
```

Pull the AI model:
```bash
make pull-model
```

On Windows (using shortcuts):
* Double-click `.bin/up.bat` to build and start the containers.
* Double-click `.bin/pull-model.bat` to download the AI model.

Verify that all services are running:
```bash
docker compose ps
```

---

## Available Commands

For Linux/macOS (Makefile):
```bash
make up
make down
make restart
make logs
make build
make test
make lint
make format
make pull-model
```

For Windows (.bin/):
* `.bin\up.bat` - Start and build services
* `.bin\down.bat` - Stop services
* `.bin\logs.bat` - Follow service logs
* `.bin\pull-model.bat` - Pull the Ollama AI model

---

## Development

Run the test suite:

```bash
make test
```

Check code quality:

```bash
make lint
```

Format source code:

```bash
make format
```

Additional documentation:

* `CONTRIBUTING.md`
* `CODE_STYLE.md`
* `TESTING.md`

---

## Roadmap

### Version 0.1

* Telegram bot integration
* Expense tracking
* Note management
* AI-powered categorization
* Basic reporting dashboard

### Version 0.2

* Reminder system
* PDF exports
* Weekly insights

### Version 0.3

* Receipt OCR
* Voice input
* Advanced analytics

### Future Plans

* Mobile application
* Shared wallets
* Calendar integration
* Multi-user workspaces

---

## Security

If you discover a security issue, please do not open a public issue.

Refer to `docs/SECURITY.md` for responsible disclosure guidelines.

---

## Contributing

Contributions are welcome.

Before opening a pull request, please read:

* `CONTRIBUTING.md`
* `CODE_STYLE.md`
* `TESTING.md`

---

## License

This project is released under the MIT License.

See the `LICENSE` file for details.

---

## Support

If you find this project useful:

* Star the repository
* Report bugs through GitHub Issues
* Suggest new features
* Submit pull requests

---

Built for people who prefer sending a message over filling out a form.
