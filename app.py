import os
from dotenv import load_dotenv

# Load env variables before everything else
load_dotenv()

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from webhook_handler import router as webhook_router
from scheduler import setup_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting AI Pro Hub...")
    init_db()
    setup_scheduler()
    yield
    # Shutdown (nothing needed)

app = FastAPI(title="AI Pro Hub - Instagram Agent", lifespan=lifespan)

# Include Webhook Router
app.include_router(webhook_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
