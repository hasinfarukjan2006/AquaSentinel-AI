# AquaSentinel AI — Production Deployment & Operation Guide

This guide outlines step-by-step instructions for deploying the **AquaSentinel AI** application (React PWA Frontend + Flask REST API Backend) to production cloud services.

---

## 1. System Architecture Overview

```
                  ┌─────────────────────────────────────────┐
                  │          Vercel / Netlify / CDN         │
                  │    React PWA Frontend (HTTPS Domain)    │
                  └────────────────────┬────────────────────┘
                                       │
                         REST API Requests (HTTPS)
                         VITE_API_BASE_URL
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       Render / Railway / Fly.io         │
                  │       Flask REST API (Gunicorn)         │
                  └────────────────────┬────────────────────┘
                                       │
                                 SQLite Engine
                                       ▼
                          jalrakshak.db (1,233 records)
```

---

## 2. Environment Variables Summary

### Frontend Environment Variables (`frontend/`)

| Variable Name | Required | Example Production Value | Description |
|---|---|---|---|
| `VITE_API_BASE_URL` | Yes | `https://jalrakshak-api.onrender.com` | Base HTTPS URL of the deployed Flask REST API. |

> [!IMPORTANT]
> **No Secrets in Frontend:** Vite environment variables prefixed with `VITE_` are bundled into client JavaScript code. **Never** put sensitive API secrets or private database credentials in `frontend/.env`.

---

### Backend Environment Variables (`backend/`)

| Variable Name | Required | Example Production Value | Description |
|---|---|---|---|
| `CORS_ALLOWED_ORIGINS` | Yes | `https://jalrakshak.vercel.app,https://jalrakshak.netlify.app` | Comma-separated list of allowed frontend origins for CORS headers. Use `*` to allow all origins. |
| `SECRET_KEY` | Recommended | `jalrakshak-prod-secret-9823478912` | Flask app secret key for session encryption. |
| `FLASK_ENV` | Optional | `production` | Set execution environment mode (`production` / `development`). |
| `FLASK_DEBUG` | Optional | `False` | Disable Flask debug mode in production. |
| `PORT` | Optional | `5000` or assigned by host | Port number on which Gunicorn listens. |
| `DATABASE_PATH` | Optional | `/var/data/jalrakshak.db` | Custom path to SQLite database if mounted on persistent storage. |

---

## 3. Backend Deployment Instructions

### Option A: Render (Recommended for Flask + Gunicorn)
1. Sign in to [Render](https://render.com) and create a **Web Service**.
2. Connect your Git repository.
3. Configure settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.wsgi:app -c gunicorn.conf.py`
4. Add Environment Variables in Render Dashboard:
   - `CORS_ALLOWED_ORIGINS`: `https://YOUR-FRONTEND-SUBDOMAIN.vercel.app`
   - `SECRET_KEY`: `<RANDOM-SECRET-STRING>`
   - `FLASK_ENV`: `production`
5. Click **Create Web Service**. Note the deployed Backend URL (e.g. `https://jalrakshak-api.onrender.com`).

---

### Option B: Railway / Fly.io / Docker
Deploy using the included `Procfile`:
```procfile
web: gunicorn backend.wsgi:app -c gunicorn.conf.py
```

---

## 4. Frontend Deployment Instructions

### Option A: Vercel (Recommended for React PWAs)
1. Sign in to [Vercel](https://vercel.com) and click **Add New Project**.
2. Import your Git repository.
3. Set **Framework Preset**: `Vite`.
4. Set **Root Directory**: `frontend`.
5. Under **Environment Variables**, add:
   - Name: `VITE_API_BASE_URL`
   - Value: `https://jalrakshak-api.onrender.com` *(Replace with your deployed backend URL)*
6. Click **Deploy**. Vercel will build the production static files into `dist/` and assign an HTTPS URL (e.g., `https://jalrakshak.vercel.app`).

---

### Option B: Netlify
1. Import repository on [Netlify](https://netlify.com).
2. Base Directory: `frontend`
3. Build Command: `node node_modules/vite/bin/vite.js build`
4. Publish Directory: `dist`
5. Environment Variable: `VITE_API_BASE_URL` = `https://YOUR-BACKEND-URL`

---

## 5. CORS Configuration & Troubleshooting

JalRakshak Flask API handles Cross-Origin Resource Sharing (CORS) via `flask-cors`.

### Verification Steps for CORS:
- Test an OPTIONS preflight request using curl:
  ```bash
  curl -i -X OPTIONS https://YOUR-BACKEND-URL/api/health \
    -H "Origin: https://YOUR-FRONTEND-URL" \
    -H "Access-Control-Request-Method: GET"
  ```
- Expected Response Headers:
  - `Access-Control-Allow-Origin: https://YOUR-FRONTEND-URL` (or `*`)
  - `Access-Control-Allow-Methods: GET, POST, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type, Authorization, Accept`

If CORS errors occur in browser console (`Access-Control-Allow-Origin missing`), check that `CORS_ALLOWED_ORIGINS` in your backend environment contains the exact protocol and hostname of your frontend (`https://your-app.vercel.app` without trailing slash).

---

## 6. Progressive Web App (PWA) HTTPS Requirement

> [!WARNING]
> **HTTPS is Mandatory for PWAs:** Service Workers and Web App Install Prompts will **only** register and function on secure origins (`https://`) or `localhost`.

### PWA Post-Deployment Verification Checklist:
1. **Manifest File**: Open `https://YOUR-FRONTEND-URL/manifest.webmanifest` in a browser to ensure it returns HTTP 200 with JSON contents.
2. **Service Worker Registration**: Open DevTools > Application > Service Workers. Verify `service-worker.js` status is `Activated and running`.
3. **App Icons**: Verify `icon-192.png`, `icon-512.png`, and `icon-maskable.png` load without 404 errors.
4. **Offline Mode Test**: In Chrome DevTools > Application > Service Workers, check `Offline` mode and refresh the page. Verify the `Offline — Showing cached information` banner appears and cached risk data loads seamlessly.
5. **Install Prompt**: Test on Android Chrome or Desktop Chrome — verify the JalRakshak Install banner appears or the browser address bar displays the install icon.

---

## 7. Production Health & API Verification Checklist

Once both services are deployed, verify the following endpoints:

| Action / Verification | Endpoint / Feature | Expected Result |
|---|---|---|
| **Backend Health Check** | `GET /api/health` | Returns `{"status": "healthy", "database": "healthy", "total_indexed_records": 1233}` |
| **Frontend Root Load** | `GET /` | Returns HTML shell, registers Service Worker, displays top header & bottom nav |
| **Summary API Request** | `GET /api/summary` | Returns total monitored locations, risk distribution, and high-risk list |
| **District Risk Data** | `GET /api/risk` | Loads risk scores across Andhra Pradesh districts |
| **Water Quality Data** | `GET /api/water-quality` | Returns pH, Turbidity, Conductance, TDS, and Coliform safety flags |
| **Rainfall Trends** | `GET /api/rainfall` | Returns historical rainfall time-series data |
| **ML Model Diagnostics** | `GET /api/model/status` | Returns Random Forest & Isolation Forest status report |
| **Data Quality Summary** | `GET /api/data-quality` | Returns dataset completeness indicators |
| **PWA Installation** | Home Screen Install | Installs JalRakshak as standalone mobile PWA |

---

## 8. Example Production Deployment URLs

- **Production Frontend App:** `https://jalrakshak.vercel.app`
- **Production Backend REST API:** `https://jalrakshak-api.onrender.com`
- **Production API Health Check:** `https://jalrakshak-api.onrender.com/api/health`
