import os
from dotenv import load_dotenv

# Load env variables before everything else
load_dotenv()

import uvicorn
from fastapi import FastAPI
from database import init_db
from webhook_handler import router as webhook_router
from scheduler import setup_scheduler

app = FastAPI(title="AI Pro Hub - Instagram Agent")

# Include Webhook Router
app.include_router(webhook_router)

@app.on_event("startup")
async def startup_event():
    print("Starting AI Pro Hub...")
    # Initialize DB
    init_db()
    # Start Scheduler
    setup_scheduler()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
