import os
from fastapi import APIRouter, Request, Response

router = APIRouter()
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "AI_PRO_HUB")

@router.get("/")
async def root():
    return {"message": "AI Pro Hub is running ✅"}

@router.get("/health")
async def health():
    return {"status": "running", "account": "@career_goals36"}

@router.get("/debug-token")
async def debug_token():
    from instagram_api import ACCESS_TOKEN, IG_ACCOUNT_ID, verify_token
    import requests
    ok, data = verify_token()
    
    ig_check = requests.get(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}",
        params={"fields": "id,name,username", "access_token": ACCESS_TOKEN},
        timeout=15
    ).json()
    
    return {
        "token_valid": ok,
        "token_first_20": ACCESS_TOKEN[:20] if ACCESS_TOKEN else "EMPTY",
        "token_length": len(ACCESS_TOKEN) if ACCESS_TOKEN else 0,
        "me_result": data,
        "ig_account_check": ig_check
    }

@router.get("/debug-page-token")
async def debug_page_token():
    from instagram_api import ACCESS_TOKEN, IG_ACCOUNT_ID
    import requests

    pages = requests.get(
        "https://graph.facebook.com/v22.0/me/accounts",
        params={
            "fields": "id,name,access_token,instagram_business_account{id,username}",
            "access_token": ACCESS_TOKEN
        },
        timeout=15
    ).json()

    return {
        "note": "Use the 'access_token' from the page that has your instagram_business_account as your NEW Page Access Token in Railway. Also use 'id' as PAGE_ID if needed.",
        "current_ig_account_id": IG_ACCOUNT_ID,
        "pages": pages
    }

@router.get("/token-info")
async def token_info():
    from instagram_api import ACCESS_TOKEN, _PAGE_TOKEN, IG_ACCOUNT_ID
    import requests

    result = {"user_token_set": bool(ACCESS_TOKEN), "page_token_set": bool(_PAGE_TOKEN), "ig_account_id": IG_ACCOUNT_ID}

    if ACCESS_TOKEN:
        try:
            r = requests.get("https://graph.facebook.com/v22.0/me",
                params={"access_token": ACCESS_TOKEN},
                timeout=10
            )
            result["user_token_test"] = r.json()
        except Exception as e:
            result["user_token_error"] = str(e)

    if _PAGE_TOKEN:
        try:
            r = requests.get("https://graph.facebook.com/v22.0/me",
                params={"access_token": _PAGE_TOKEN},
                timeout=10
            )
            result["page_token_test"] = r.json()
        except Exception as e:
            result["page_token_error"] = str(e)

    return result

@router.get("/trigger-post")
async def trigger_post(post_type: str = "AI"):
    from scheduler import run_9am_post, run_8pm_post
    import threading
    if post_type.upper() == "AI":
        threading.Thread(target=run_9am_post, daemon=True).start()
        return {"status": "triggered", "post_type": "AI (9AM)"}
    else:
        threading.Thread(target=run_8pm_post, daemon=True).start()
        return {"status": "triggered", "post_type": "STUDENT (8PM)"}
