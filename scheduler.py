import asyncio
import os
import traceback
import datetime
from content_engine import generate_ai_content, generate_student_content
from image_builder import build_slides, build_story_image
from instagram_api import upload_to_imgbb, post_carousel_to_instagram, post_story
from database import save_post

def run_9am_post():
    print(f"[{datetime.datetime.now()}] Starting 9AM AI Post Pipeline")
    try:
        # 1. Fetch content
        content = generate_ai_content()
        print(f"Generated content: {content['title'] if 'title' in content else content['hook_text']}")

        # 2. Generate 5 slides
        # Running async function in a sync wrapper since apscheduler calls sync func
        images = asyncio.run(build_slides(
            topic=content['topic'],
            hook_text=content['hook_text'],
            what_line1=content['what_line1'],
            what_line2=content['what_line2'],
            what_line3=content['what_line3'],
            steps=content['steps'],
            points=content['points'],
            post_type=content['post_type'],
            source_link=content['source_link'],
            prefix="ai_slide"
        ))

        # 3 & 4. Compress & Upload to imgbb
        image_urls = []
        for img in images:
            url = upload_to_imgbb(img)
            image_urls.append(url)

        # 5. Build Caption
        caption = f"""{content['caption_hook']}

{content['what_line1']}
{content['what_line2']}

Built for: {content['what_line3']}

🔗 Link in the carousel 👉 swipe right!
💬 Comment "AI" to boost reach!
🔁 Share with someone who needs this!
💾 Save for later!
📌 Follow @career_goals36 for daily drops!

#AITools #ArtificialIntelligence #NewAI #AIUpdate
#MachineLearning #AIForBeginners #TechNews #FutureOfAI
#AIResearch #AIRevolution #TechTrends #AILaunch
#DeepLearning #AITrends #TechIndia #AIIndia
#IndianDeveloper #StudentLife #CodingLife #LearnAI
#FreeAITools #AIHacks #TechHacks #ProductivityTools
#AIForStudents #TechUpdate #AIWorld #BuildWithAI
#ToolsOfTheTrade #AIDaily"""

        # 6. Post Carousel
        post_id = post_carousel_to_instagram(image_urls, caption)

        # 7. Post Story (dedicated 9:16 story image promoting the post)
        story_img = "ai_story.png"
        asyncio.run(build_story_image(content['topic'], content['hook_text'], content['post_type'], story_img))
        story_url = upload_to_imgbb(story_img)
        if story_url:
            post_story(story_url)

        # 8. Save to DB
        save_post(post_id, content['topic'], content['source_link'], content['post_type'])

        # 8. Cleanup local files
        for img in images:
            if os.path.exists(img):
                os.remove(img)
                print(f"Cleaned up {img}")
            comp_img = img.replace(".png", "_compressed.jpg")
            if os.path.exists(comp_img):
                os.remove(comp_img)
                print(f"Cleaned up {comp_img}")
        if os.path.exists(story_img):
            os.remove(story_img)
            print(f"Cleaned up {story_img}")

        print(f"[{datetime.datetime.now()}] 9AM AI Post Pipeline SUCCESS - Post ID: {post_id}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ERROR in 9AM Pipeline: {e}")
        traceback.print_exc()

def run_8pm_post():
    print(f"[{datetime.datetime.now()}] Starting 8PM Student Post Pipeline")
    try:
        # 1. Fetch content
        content = generate_student_content()
        print(f"Generated content: {content['title'] if 'title' in content else content['hook_text']}")

        # 2. Generate 5 slides
        images = asyncio.run(build_slides(
            topic=content['topic'],
            hook_text=content['hook_text'],
            what_line1=content['what_line1'],
            what_line2=content['what_line2'],
            what_line3=content['what_line3'],
            steps=content['steps'],
            points=content['points'],
            post_type=content['post_type'],
            source_link=content['source_link'],
            prefix="student_slide"
        ))

        # 3 & 4. Compress & Upload to imgbb
        image_urls = []
        for img in images:
            url = upload_to_imgbb(img)
            image_urls.append(url)

        # 5. Build Caption
        caption = f"""{content['caption_hook']}

{content['what_line1']}
{content['what_line2']}

Built for: {content['what_line3']}

🔗 Link in the carousel 👉 swipe right!
💬 Comment "SEND" to boost reach!
🔁 Tag a friend who needs this!
💾 Save before it gets buried!
📌 Follow @career_goals36 for daily drops!

#StudentLife #CSStudents #Internship2025
#HackathonIndia #FreeResources #GitHubTips
#CodingLife #TechStudents #AIJobs #FresherJobs
#LearnToCode #ComputerScience #IndiaJobs
#Placement #CampusLife #EngineeringStudents
#BTech #TechIndia #AIInternship #HackathonAlert
#FreeOnlineCourse #CodingResources #StudentDeveloper
#AIForStudents #JobAlert #InternshipAlert
#GithubRepo #OpenSource #TechOpportunity #CareerGoals"""

        # 6. Post Carousel
        post_id = post_carousel_to_instagram(image_urls, caption)

        # 7. Post Story (dedicated 9:16 story image promoting the post)
        story_img = "student_story.png"
        asyncio.run(build_story_image(content['topic'], content['hook_text'], content['post_type'], story_img))
        story_url = upload_to_imgbb(story_img)
        if story_url:
            post_story(story_url)

        # 8. Save to DB
        save_post(post_id, content['topic'], content['source_link'], content['post_type'])

        # 8. Cleanup local files
        for img in images:
            if os.path.exists(img):
                os.remove(img)
                print(f"Cleaned up {img}")
            comp_img = img.replace(".png", "_compressed.jpg")
            if os.path.exists(comp_img):
                os.remove(comp_img)
                print(f"Cleaned up {comp_img}")
        if os.path.exists(story_img):
            os.remove(story_img)
            print(f"Cleaned up {story_img}")

        print(f"[{datetime.datetime.now()}] 8PM Student Post Pipeline SUCCESS - Post ID: {post_id}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ERROR in 8PM Pipeline: {e}")
        traceback.print_exc()

def setup_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler
    import pytz

    scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Kolkata'))
    
    # 9 AM IST AI Post
    scheduler.add_job(run_9am_post, 'cron', hour=9, minute=0)
    
    # 8 PM IST Student Post
    scheduler.add_job(run_8pm_post, 'cron', hour=20, minute=0)
    
    scheduler.start()
    print("Scheduler started. Jobs configured for 09:00 and 20:00 IST.")
    return scheduler
