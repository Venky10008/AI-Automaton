import os
import asyncio
from dotenv import load_dotenv

# Load env before importing modules
load_dotenv()

from content_engine import generate_ai_content, generate_student_content
from image_builder import build_slides, compress_image
from database import init_db, save_post, get_post, log_dm_sent, has_dm_been_sent
from instagram_api import upload_to_imgbb
import automation_engine

def test_content_9am():
    print("\n--- TEST: 9AM Content ---")
    content = generate_ai_content()
    print(content)
    if content:
        print("PASS")
    else:
        print("FAIL")

def test_content_8pm():
    print("\n--- TEST: 8PM Content ---")
    content = generate_student_content()
    print(content)
    if content:
        print("PASS")
    else:
        print("FAIL")

def test_slides_9am():
    print("\n--- TEST: 9AM Slides ---")
    content = generate_ai_content()
    images = asyncio.run(build_slides(
        topic=content['topic'],
        hook_text=content['hook_text'],
        what_line1=content['what_line1'],
        what_line2=content['what_line2'],
        what_line3=content['what_line3'],
        steps=content['steps'],
        points=content['points'],
        post_type=content['post_type'],
        prefix="test_ai_slide"
    ))
    print(f"Generated images: {images}")
    if len(images) == 5:
        print("PASS")
    else:
        print("FAIL")
    return images

def test_slides_8pm():
    print("\n--- TEST: 8PM Slides ---")
    content = generate_student_content()
    images = asyncio.run(build_slides(
        topic=content['topic'],
        hook_text=content['hook_text'],
        what_line1=content['what_line1'],
        what_line2=content['what_line2'],
        what_line3=content['what_line3'],
        steps=content['steps'],
        points=content['points'],
        post_type=content['post_type'],
        prefix="test_student_slide"
    ))
    print(f"Generated images: {images}")
    if len(images) == 5:
        print("PASS")
    else:
        print("FAIL")
    return images

def test_compress():
    print("\n--- TEST: Image Compression ---")
    # Check if we have an image to test
    if os.path.exists("test_ai_slide_1.png"):
        img = "test_ai_slide_1.png"
    elif os.path.exists("test_student_slide_1.png"):
        img = "test_student_slide_1.png"
    else:
        print("No image found to compress. Run test_slides first.")
        print("FAIL")
        return
        
    out = "test_compress_output.jpg"
    orig_kb = os.path.getsize(img) / 1024
    compress_image(img, out)
    new_kb = os.path.getsize(out) / 1024
    print(f"Original: {orig_kb:.0f}KB -> Compressed: {new_kb:.0f}KB")
    if new_kb <= 450:
        print("PASS")
    else:
        print("FAIL")
        
def test_imgbb():
    print("\n--- TEST: ImgBB Upload ---")
    if not os.environ.get("IMGBB_API_KEY"):
        print("FAIL: No IMGBB_API_KEY in .env")
        return
        
    if os.path.exists("test_ai_slide_1.png"):
        img = "test_ai_slide_1.png"
    else:
        print("No image found to upload. Run test_slides first.")
        print("FAIL")
        return
        
    try:
        url = upload_to_imgbb(img)
        print(f"URL: {url}")
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")

def test_database():
    print("\n--- TEST: Database ---")
    init_db()
    # Test save
    save_post("test_123", "ai_tool", "https://example.com", "AI")
    
    # Test retrieve
    post = get_post("test_123")
    if post and post["source_link"] == "https://example.com":
        print("Post DB: PASS")
    else:
        print("Post DB: FAIL")
        
    # Test DM logs
    log_dm_sent("test_user", "test_123")
    if has_dm_been_sent("test_user", "test_123"):
        print("DM Log: PASS")
    else:
        print("DM Log: FAIL")

def test_caption_9am():
    print("\n--- TEST: 9AM Caption ---")
    content = generate_ai_content()
    caption = f"""{content['caption_hook']}

{content['what_line1']}
{content['what_line2']}

Built for: {content['what_line3']}

💬 Comment "AI" below 👇
📩 I'll DM you the link in 5 minutes!
⚠️ Follow first — DMs only reach followers!
💾 Save this post so you don't lose it!

#AITools #ArtificialIntelligence #NewAI #AIUpdate
#MachineLearning #AIForBeginners #TechNews #FutureOfAI
#AIResearch #AIRevolution #TechTrends #AILaunch
#DeepLearning #AITrends #TechIndia #AIIndia
#IndianDeveloper #StudentLife #CodingLife #LearnAI
#FreeAITools #AIHacks #TechHacks #ProductivityTools
#AIForStudents #TechUpdate #AIWorld #BuildWithAI
#ToolsOfTheTrade #AIDaily"""
    print(caption)
    print("PASS")

def test_caption_8pm():
    print("\n--- TEST: 8PM Caption ---")
    content = generate_student_content()
    caption = f"""{content['caption_hook']}

{content['what_line1']}
{content['what_line2']}

Built for: {content['what_line3']}

💬 Comment "SEND" below 👇
📩 I'll DM you the link in 5 minutes!
⚠️ Follow first — DMs only reach followers!
🔁 Tag a friend who needs this!
💾 Save before it gets buried!

#StudentLife #CSStudents #Internship2025
#HackathonIndia #FreeResources #GitHubTips
#CodingLife #TechStudents #AIJobs #FresherJobs
#LearnToCode #ComputerScience #IndiaJobs
#Placement #CampusLife #EngineeringStudents
#BTech #TechIndia #AIInternship #HackathonAlert
#FreeOnlineCourse #CodingResources #StudentDeveloper
#AIForStudents #JobAlert #InternshipAlert
#GithubRepo #OpenSource #TechOpportunity #CareerGoals"""
    print(caption)
    print("PASS")

if __name__ == "__main__":
    init_db()
    test_content_9am()
    test_content_8pm()
    test_slides_9am()
    test_slides_8pm()
    test_compress()
    test_imgbb()
    test_database()
    test_caption_9am()
    test_caption_8pm()
    print("\nAll tests completed.")
