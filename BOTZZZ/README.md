# BOTZZZ Admin API

FastAPI-based backend for logging, stats, and integrations.

## 🚀 Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🔑 Environment Variables
Create a `.env` file:

```
ADMIN_TOKEN=changeme_admin_token_123
SMM_PANEL_URL=https://example-smm-panel.com/api/v2
SMM_API_KEY=your_smm_api_key_here
```

## 📡 Endpoints
- `GET /` – Health check
- `GET /admin/logs/boosts` – View boost logs
- `GET /admin/logs/stats/hosts` – Host performance stats
- `POST /admin/logs/smm/order` – Place SMM follower order
- `GET /admin/logs/zefoy/mirrors` – Discover Zefoy mirrors
