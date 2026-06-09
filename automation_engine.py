import random
import os
from database import get_post, log_dm_sent, has_dm_been_sent
from instagram_api import send_dm, send_reply, like_comment, check_is_follower

IG_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")

FOLLOWER_DM_9AM = """Hey {username}! 👋

You showed interest in our post — here it is!
🔗 {link}

We share exclusive AI tools DAILY to our followers 🔥
Follow @career_goals36 so our DMs always reach you!

🕘 9AM — Latest AI tools nobody talks about
🕗 8PM — Free student resources

See you tomorrow! 🚀
— Career Goals 36"""

FOLLOWER_DM_8PM = """Hey {username}! 🎉

Here's the free resource from our post!
🔗 {link}

We drop FREE resources daily — internships, GitHub repos,
courses, PDFs, hackathons — completely free 💯

Follow @career_goals36 so you never miss tomorrow's drop!
Something bigger coming tomorrow 👀

— Career Goals 36"""

REPLY_9AM = [
    "Sent! Check your DMs @{username} 🔥",
    "DM incoming @{username}! Follow so it reaches you 📩",
    "Just sent it @{username}! Check your inbox 👀",
    "Done @{username}! DM sent 🚀 Follow for tomorrow's drop!",
    "Link sent to your DM @{username} 💌",
    "Checked ✅ DM sent @{username}! Follow us to receive it"
]

REPLY_8PM = [
    "Sent @{username}! Check your DMs 📩🔥",
    "DM incoming @{username}! Follow so you don't miss more!",
    "Just sent it @{username}! Check your inbox 🎉",
    "Done! DM sent @{username} 🚀 Follow for daily drops",
    "Free resource sent @{username}! Check DMs 💌",
    "Checked ✅ Sent to your DMs @{username}!"
]

def process_new_comment(comment_id, username, user_id, post_id, page_id="me"):
    print(f"Processing @{username} on post {post_id}")

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

    # 5. Build DM and Reply text
    if is_follower:
        if post_type == "AI":
            dm_text = FOLLOWER_DM_9AM.format(username=username, link=source_link)
            reply_text = random.choice(REPLY_9AM).format(username=username)
        else:
            dm_text = FOLLOWER_DM_8PM.format(username=username, link=source_link)
            reply_text = random.choice(REPLY_8PM).format(username=username)
    else:
        dm_text = f"Hey {username}! 👋\n\nOur exclusive resources are for followers only.\n\nPlease follow @career_goals36 and comment again to get the link automatically! 🚀"
        reply_text = f"Hey @{username}! Please follow us first, then comment again to get the link in your DMs 🔒"

    # 6. Send public reply first (always)
    like_comment(comment_id)
    send_reply(comment_id, reply_text)

    # 7. Send DM only to followers (Instagram blocks unsolicited DMs to non-followers)
    if is_follower:
        dm_success = send_dm(user_id, dm_text)
        log_dm_sent(username, post_id)
        return dm_success

    return True
