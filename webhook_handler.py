import os
from fastapi import APIRouter, Request, Response
from automation_engine import process_new_comment

router = APIRouter()
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "AI_PRO_HUB")

@router.get("/")
async def root():
    return {"message": "AI Pro Hub is running ✅"}

@router.get("/health")
async def health():
    return {"status": "running", "account": "@career_goals36"}

@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return Response(content=challenge, status_code=200)
        else:
            return Response(status_code=403)
    return Response(status_code=400)

@router.post("/webhook")
async def handle_webhook(request: Request):
    body = await request.json()
    
    if body.get("object") == "instagram":
        for entry in body.get("entry", []):
            page_id = entry.get("id")
            for change in entry.get("changes", []):
                if change.get("field") == "comments":
                    value = change.get("value", {})
                    
                    comment_id = value.get("id")
                    username = value.get("from", {}).get("username")
                    user_id = value.get("from", {}).get("id")
                    post_id = value.get("media", {}).get("id")
                    
                    if comment_id and username and user_id and post_id:
                        # Process comment asynchronously to return 200 OK fast
                        import asyncio
                        asyncio.create_task(
                            run_comment_processor(comment_id, username, user_id, post_id, page_id)
                        )
    
    return {"status": "success"}

async def run_comment_processor(comment_id, username, user_id, post_id, page_id):
    import asyncio
    await asyncio.to_thread(process_new_comment, comment_id, username, user_id, post_id, page_id)
