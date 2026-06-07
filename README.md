# Instagram Automation Agent

A production-ready Instagram automation agent that creates and posts daily AI news and student resources using Playwright and CSS-based dynamic templates.

## Deployment Checklist

1. Create a Railway project.
2. Link the repository to Railway.
3. Configure Environment Variables in Railway:
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`
   - `INSTAGRAM_ACCESS_TOKEN`
   - `VERIFY_TOKEN` (e.g., `AI_PRO_HUB`)
   - `PEXELS_API_KEY`
   - `IMGBB_API_KEY`
   - `HF_API_KEY`
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
   - `DB_PATH=/app/data/database.db`
   - `PORT=8000`
   - `PLAYWRIGHT_BROWSERS_PATH=0`
4. Create a Volume in Railway for persistence.
   - Mount path: `/app/data`
5. Deploy the application.
6. Set up the Meta Webhook:
   - Go to developers.facebook.com -> your app.
   - Set Callback URL to `https://<YOUR-RAILWAY-URL>/webhook`.
   - Set Verify Token to `AI_PRO_HUB`.
   - Subscribe to: `comments`, `mentions`, `messages`.

## Features
- Daily scheduled posts at 9 AM and 8 PM IST.
- Dynamically generated images using HTML/CSS and Playwright.
- Comment automation with DMs.
- Image compression for quick upload to ImgBB.
