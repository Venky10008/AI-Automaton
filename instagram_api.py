import os
import requests
import time

# Credentials — .strip() removes any accidental whitespace/newlines from Railway env vars
_USER_TOKEN = (os.environ.get("INSTAGRAM_ACCESS_TOKEN") or "").strip()
IG_ACCOUNT_ID = (os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID") or "").strip()
IMGBB_API_KEY = (os.environ.get("IMGBB_API_KEY") or "").strip()

# Page Access Token for DMs — separate from User Token used for content publishing
_PAGE_TOKEN = (os.environ.get("PAGE_ACCESS_TOKEN") or "").strip()
PAGE_ID = (os.environ.get("PAGE_ID") or "").strip()

# ── On startup: print token info so we can see it in Railway logs ──────────────
if _USER_TOKEN:
    print(f"[TOKEN] Loaded. First 20 chars: {_USER_TOKEN[:20]}... Last 10: ...{_USER_TOKEN[-10:]}")
    print(f"[TOKEN] Total length: {len(_USER_TOKEN)}")
else:
    print("[TOKEN] ERROR: INSTAGRAM_ACCESS_TOKEN is EMPTY! Set it in Railway variables.")

if IG_ACCOUNT_ID:
    print(f"[ACCOUNT] IG Account ID: {IG_ACCOUNT_ID}")
else:
    print("[ACCOUNT] ERROR: INSTAGRAM_BUSINESS_ACCOUNT_ID is EMPTY!")

# ── Token: Use the user token directly for Instagram Graph API ─────────────────
# Instagram Content Publishing uses the User Access Token directly, NOT a Page token.
ACCESS_TOKEN = _USER_TOKEN


def verify_token():
    """Test if the token works. Called at startup and from /debug-token endpoint."""
    r = requests.get(
        "https://graph.facebook.com/v22.0/me",
        params={"access_token": ACCESS_TOKEN, "fields": "id,name"},
        timeout=15
    )
    data = r.json()
    if "id" in data:
        print(f"[TOKEN] Valid ✅ — Authenticated as: {data.get('name', data['id'])}")
        return True, data
    else:
        print(f"[TOKEN] INVALID ❌ — Error: {data}")
        return False, data


# Verify token on module load
try:
    verify_token()
except Exception as e:
    print(f"[TOKEN] Verify failed: {e}")


def upload_to_imgbb(image_path):
    from image_builder import compress_image
    import base64

    compressed = image_path.replace(".png", "_compressed.jpg")
    try:
        compress_image(image_path, compressed, max_kb=450)

        with open(compressed, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY, "image": b64, "expiration": 600},
            timeout=30
        )
        data = response.json()
        if "data" not in data or "url" not in data["data"]:
            raise Exception(f"ImgBB upload failed: {data}")

        url = data["data"]["url"]
        print(f"Uploaded to imgbb: {url}")
        return url
    finally:
        if os.path.exists(compressed):
            os.remove(compressed)


def post_carousel_to_instagram(image_urls, caption):
    container_ids = []
    for i, url in enumerate(image_urls):
        r = requests.post(
            f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/media",
            params={"access_token": ACCESS_TOKEN},
            json={"image_url": url, "is_carousel_item": True},
            timeout=30
        )
        data = r.json()
        if "id" not in data:
            raise Exception(f"Slide {i+1} container failed: {data}")
        container_ids.append(data["id"])
        print(f"Container {i+1} created: {data['id']}")
        time.sleep(2)

    # Create carousel
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/media",
        params={"access_token": ACCESS_TOKEN},
        json={
            "media_type": "CAROUSEL",
            "children": ",".join(container_ids),
            "caption": caption
        },
        timeout=30
    )
    data = r.json()
    if "id" not in data:
        raise Exception(f"Carousel creation failed: {data}")
    carousel_id = data["id"]
    print(f"Carousel created: {carousel_id}")

    time.sleep(3)

    # Publish
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/media_publish",
        params={"access_token": ACCESS_TOKEN},
        json={"creation_id": carousel_id},
        timeout=30
    )
    data = r.json()
    real_post_id = data.get("id")
    if not real_post_id:
        raise Exception(f"Publishing failed: {data}")

    print(f"POSTED! Real Instagram Post ID: {real_post_id}")
    return real_post_id


def send_dm(user_id, message_text):
    dm_token = _PAGE_TOKEN or ACCESS_TOKEN
    dm_id = PAGE_ID or IG_ACCOUNT_ID

    r = requests.post(
        f"https://graph.facebook.com/v22.0/{dm_id}/messages",
        params={"access_token": dm_token},
        json={
            "recipient": {"id": user_id},
            "message": {"text": message_text}
        },
        timeout=15
    )
    if r.status_code == 200:
        print(f"DM sent successfully")
        return True
    print(f"DM failed: {r.status_code} {r.json()}")
    return False


def send_reply(comment_id, message):
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{comment_id}/replies",
        params={"access_token": ACCESS_TOKEN},
        json={"message": message},
        timeout=15
    )
    if r.status_code == 200:
        print(f"Public reply sent")
        return True
    print(f"Reply failed: {r.status_code} {r.json()}")
    return False


def like_comment(comment_id):
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{comment_id}/likes",
        params={"access_token": ACCESS_TOKEN},
        timeout=15
    )
    if r.status_code == 200:
        print(f"Comment liked")
        return True
    print(f"Like failed: {r.status_code} {r.json()}")
    return False


def post_story(image_url):
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/media",
        params={"access_token": ACCESS_TOKEN},
        json={"image_url": image_url, "media_type": "STORIES"},
        timeout=30
    )
    data = r.json()
    if "id" not in data:
        print(f"Story creation failed: {data}")
        return False

    creation_id = data["id"]
    print(f"Story container created: {creation_id}")
    time.sleep(2)

    r = requests.post(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/media_publish",
        params={"access_token": ACCESS_TOKEN},
        json={"creation_id": creation_id},
        timeout=30
    )
    data = r.json()
    if "id" not in data:
        print(f"Story publish failed: {data}")
        return False

    print(f"Story POSTED! ID: {data['id']}")
    return True


def check_is_follower(user_id):
    try:
        r = requests.get(
            f"https://graph.facebook.com/v22.0/{user_id}",
            params={
                "fields": "is_user_follow_business",
                "access_token": ACCESS_TOKEN
            },
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            if "is_user_follow_business" in data:
                return data["is_user_follow_business"]
    except Exception as e:
        print(f"Follower check error: {e}")
    return True
