# Public demo for recruiters (Render)

Host the app on the internet so anyone can open it with a link (no Docker on your laptop required).

## One-time setup (~10 minutes)

### 1. Deploy from GitHub

1. Sign in at [render.com](https://render.com) (free account).
2. Open this link (uses `render.yaml` in the repo):

   **https://render.com/deploy?repo=https://github.com/SirGwaine19/Diet-LLM-Recommendation**

3. Click **Apply** to create:
   - PostgreSQL database
   - API (`diet-recommendation-api`)
   - Website (`diet-recommendation-web`)

### 2. Add your OpenAI key

When prompted (or in each service → **Environment**):

| Variable | Value |
|----------|--------|
| `OPENAI_API_KEY` | Your key from [OpenAI API keys](https://platform.openai.com/api-keys) |

Save — Render will redeploy the API.

### 3. Wait for green “Live”

First deploy can take **10–15 minutes**. When both web services are **Live**, open:

| What | URL |
|------|-----|
| **Share with recruiters** | **https://diet-recommendation-web.onrender.com** |
| API docs (optional) | https://diet-recommendation-api.onrender.com/docs |

Put the **web** URL on your resume / LinkedIn / portfolio.

---

## What recruiters should expect

- **First visit after idle**: Free tier sleeps after ~15 minutes; the first load can take **30–60 seconds**. Say “allow a minute for cold start” on your resume if you like.
- **Register**: They create their own account (data is isolated per user).
- **Meal logging** needs a valid OpenAI key on your Render API service.

---

## Updating the live site

Push to GitHub `main` — Render auto-redeploys if auto-deploy is enabled (default).

```bash
git push origin main
```

---

## Costs & limits (free tier)

- Render free web services spin down when idle.
- Free PostgreSQL has storage/time limits; fine for demos, not production scale.
- OpenAI usage is billed on your OpenAI account.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Site loads but login/API fails | Check API logs on Render; confirm `OPENAI_API_KEY` is set on **diet-recommendation-api**. |
| CORS error in browser | `CORS_ORIGINS` on the API must be `https://diet-recommendation-web.onrender.com` (set in `render.yaml`). |
| Build failed on frontend | See build logs; run `npm run build` locally to reproduce. |
| Custom domain | Render dashboard → **diet-recommendation-web** → **Settings** → **Custom Domains**. |

Local Docker deploy is still documented in [DEPLOYMENT.md](DEPLOYMENT.md).
