import os
import requests
import time

# Credentials
_USER_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
IG_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")

def _get_page_access_token():
    """
    Exchange the User Token for the correct Page Access Token.
    Instagram Graph API requires a Page token to publish media.
    """
    try:
        # Get list of pages the user manages
        r = requests.get(
            "https://graph.facebook.com/v22.0/me/accounts",
            params={"access_token": _USER_TOKEN},
            timeout=15
        )
        data = r.json()
        pages = data.get("data", [])
        if pages:
            # Return the first page's access token
            page_token = pages[0]["access_token"]
            print(f"Page Access Token obtained for: {pages[0]['name']}")
            return page_token
    except Exception as e:
        print(f"Page token fetch error: {e}")
    # Fallback to user token
    print("Warning: Using User Token directly (may fail for some endpoints)")
    return _USER_TOKEN

# Get the correct token on module load
ACCESS_TOKEN = _get_page_access_token()


def upload_to_imgbb(image_path):
    from image_builder import compress_image
    
    # Compress first
    compressed = image_path.replace(".png", "_compressed.jpg")
    try:
        compress_image(image_path, compressed, max_kb=450)
        
        import base64
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
        # Cleanup compressed
        if os.path.exists(compressed):
            os.remove(compressed)

def post_carousel_to_instagram(image_urls, caption):
    # Step 1: Create item containers
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
        time.sleep(1)  # avoid rate limiting

    # Step 2: Create carousel
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

    # Step 3: Publish
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
    r = requests.post(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT_ID}/messages",
        json={
            "recipient": {"id": user_id},
            "message": {"text": message_text},
            "access_token": ACCESS_TOKEN
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
    # Step 1: Create media for story
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
    time.sleep(1)

    # Step 2: Publish story
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
    """
    Attempts to check if the user is a follower using the Messaging API.
    Note: Meta's Graph API restricts this data unless the user has messaged the bot before.
    If the API blocks it, it defaults to True to avoid penalizing real followers.
    """
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
            # If the field exists, use it. Otherwise, return True.
            if "is_user_follow_business" in data:
                return data["is_user_follow_business"]
    except Exception as e:
        print(f"Follower check error: {e}")
        
    # Default to True if the API doesn't provide the info
    return True
