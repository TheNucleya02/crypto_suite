# Momentum Crypto Suite

An AI-powered cryptocurrency analysis and portfolio management application. The React frontend communicates with a FastAPI backend that uses a multi-agent CrewAI system to deliver real-time market summaries, news analysis, and portfolio tracking.

---

## Features

- **Dashboard** — live portfolio value, P/L, and AI-generated market summaries
- **Portfolio tracker** — add/remove holdings with real-time P/L via CoinGecko prices
- **AI assistant** — multi-agent crew (news, price, fear & greed) powered by a Hugging Face LLM
- **Market page** — live prices and sentiment indicators
- **Auth** — JWT-based registration and login; sessions stored in `localStorage`

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Radix UI, TanStack Query |
| Backend | Python 3.12, FastAPI, SQLAlchemy, SQLite (`auth.db`) |
| AI agents | CrewAI, LiteLLM, Hugging Face Inference |
| External data | CoinGecko (prices), Alpha Vantage (history), CoinMarketCap (Fear & Greed), Exa (news) |
| Optional cloud | Supabase (chat thread + cloud portfolio persistence) |

---

## Project structure

```
/
├── app/                    # FastAPI backend
│   ├── main.py             # Routes, CORS, static-file SPA mount
│   ├── auth.py             # JWT creation & verification
│   ├── crud.py             # Database helpers
│   ├── database.py         # SQLAlchemy models & SQLite engine
│   ├── models.py           # Pydantic schemas
│   └── analysis.py         # CrewAI agents & tools
├── frontend/               # React + Vite app
│   ├── src/
│   │   ├── pages/          # Dashboard, Portfolio, Assistant, Market
│   │   ├── components/     # Shared UI components
│   │   ├── services/api.ts # Backend + Supabase API calls
│   │   └── lib/supabase.ts # Optional Supabase client
│   ├── .env.example        # Frontend environment variable template
│   └── vite.config.ts
├── .env.example            # Backend environment variable template
├── requirements.txt        # Python dependencies
└── auth.db                 # SQLite database (auto-created)
```

---

## Quick start (local development)

### Prerequisites

- Python 3.12+
- Node.js 20+
- pip

### 1. Clone and install

```bash
git clone <repo-url>
cd momentum-crypto-suite

# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Configure environment variables

```bash
# Backend
cp .env.example .env
# Edit .env — fill in SECRET and any API keys you want to enable

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env — set VITE_API_BASE_URL=http://localhost:8000
```

See [Environment variables](#environment-variables) below for details on each variable.

### 3. Run

Open two terminals:

```bash
# Terminal 1 — backend (port 8000)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend dev server (port 5000)
cd frontend && npm run dev
```

Open `http://localhost:5000` in your browser.

Interactive API docs are available at `http://localhost:8000/docs`.

---

## Environment variables

### Backend — `.env`

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET` | **Yes (prod)** | Secret key for signing JWT tokens. Generate with `python -c "import secrets; print(secrets.token_hex(32))"`. Defaults to an insecure placeholder in dev. |
| `HF_TOKEN` | For AI summary | Hugging Face access token — [create one here](https://huggingface.co/settings/tokens). |
| `HF_MODEL` | No | Hugging Face model path. Defaults to `huggingface/meta-llama/Llama-3.1-8B-Instruct`. |
| `EXA_API` | For AI summary | Exa API key for news search — [exa.ai](https://exa.ai). |
| `ALPHA_API` | For AI summary | Alpha Vantage key for historical price data — [alphavantage.co](https://www.alphavantage.co/support/#api-key). |
| `CMC_API` | For AI summary | CoinMarketCap key for the Fear & Greed index — [coinmarketcap.com/api](https://coinmarketcap.com/api/). |
| `CORS_ORIGINS` | No | Comma-separated allowed frontend origins. Defaults to `*` (all). Set to your deployed frontend URL in production, e.g. `https://myapp.replit.app`. |

### Frontend — `frontend/.env`

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | No | Backend URL. Defaults to `http://localhost:8000`. Set to your deployed backend URL in production. |
| `VITE_SUPABASE_URL` | No | Supabase project URL. Only needed for cloud chat/portfolio persistence. |
| `VITE_SUPABASE_ANON_KEY` | No | Supabase anonymous key. Only needed alongside `VITE_SUPABASE_URL`. |

---

## Production deployment

The backend serves the built React frontend as a single-page application when `frontend/dist/` exists:

```bash
# 1. Build the frontend
cd frontend && npm run build && cd ..

# 2. Start the backend (serves both API and frontend)
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

Before going live:

1. Set `SECRET` to a strong random value.
2. Set `CORS_ORIGINS` to your frontend domain.
3. Set all AI API keys you want to enable.

On **Replit**, set these in the **Secrets** tab (the padlock icon). The app is pre-configured to build and deploy with a single click via the **Deploy** button.

---

## API overview

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/register` | — | Create a new user account |
| `POST` | `/token` | — | Log in and receive a JWT |
| `GET` | `/users/me` | Bearer | Current user profile |
| `GET` | `/portfolio` | Bearer | List portfolio entries with live P/L |
| `POST` | `/portfolio/add` | Bearer | Add a holding |
| `GET` | `/portfolio/{id}` | Bearer | Single entry with live price |
| `DELETE` | `/portfolio/{id}` | Bearer | Remove a holding |
| `POST` | `/summary/` | Bearer | Run AI multi-agent market summary |

Full interactive docs at `/docs` (Swagger) and `/redoc`.

---

## Password requirements

User passwords must be at least 8 characters and include an uppercase letter, a lowercase letter, a digit, and a special character.

---

## License

MIT — see [LICENSE](LICENSE).
