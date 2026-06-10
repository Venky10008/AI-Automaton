import os
from database import get_post, log_dm_sent, has_dm_been_sent
from instagram_api import send_reply, like_comment, check_is_follower

IG_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")

def process_new_comment(comment_id, username, user_id, post_id, page_id="me"):
    print(f"Processing @{username} (user_id: {user_id}) on post {post_id}")

    # 1. Skip duplicates
    if has_dm_been_sent(username, post_id):
        print(f"Already processed @{username} — skip")
        return False

    # 2. Skip own account
    if user_id == IG_ACCOUNT_ID:
        print("Own account comment — skip")
        return False

    # 3. Get post from database
    post = get_post(post_id)
    if not post:
        print(f"Post {post_id} not in DB — skip")
        return False

    post_type = post["post_type"]
    source_link = post["source_link"]

    # 4. Check Follower Status
    is_follower = check_is_follower(user_id)

    # 5. Build reply text
    if is_follower:
        reply_text = f"Here you go @{username}! 🚀\n🔗 {source_link}\n\nFollow @career_goals36 for daily drops!"
    else:
        reply_text = f"Hey @{username}! Please follow @career_goals36 first, then comment again to get the link 🔒"

    # 6. Like + Reply publicly
    like_comment(comment_id)
    send_reply(comment_id, reply_text)

    # 7. Mark as processed only if link was delivered (so user can re-comment after following)
    if is_follower:
        log_dm_sent(username, post_id)

    return True
