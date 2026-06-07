import os
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

async def render_html_to_png(html_content, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page(
            viewport={"width": 1080, "height": 1080}
        )
        await page.set_content(html_content)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=output_path, type="png")
        await browser.close()
    return output_path

def compress_image(input_path, output_path, max_kb=450):
    img = Image.open(input_path)
    img = img.convert("RGB")
    quality = 90
    while True:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= max_kb or quality <= 40:
            break
        quality -= 5
    print(f"Compressed {input_path} to {size_kb:.0f}KB at quality {quality}")
    return output_path

def get_pexels_background(topic):
    import requests
    import random
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        return ""
        
    query_map = {
        'ai_tool': 'artificial intelligence technology',
        'research': 'futuristic technology',
        'ai': 'cyberpunk city',
        'github': 'hacker computer screen code',
        'internship': 'modern office skyscraper',
        'hackathon': 'neon gaming setup',
        'jobs': 'success business motivation',
        'course': 'studying late night aesthetic',
        'fellowship': 'graduation university'
    }
    
    query = query_map.get(str(topic).lower(), 'cyberpunk aesthetic')
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=15"
    headers = {"Authorization": api_key}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data.get('photos'):
            photo = random.choice(data['photos'])
            return photo['src']['large2x']
    except Exception as e:
        print(f"Pexels fetch failed: {e}")
    return ""

async def build_slides(topic, hook_text, what_line1, what_line2, what_line3, steps, points, post_type, prefix="slide"):
    from slide_templates import (get_template_for_topic, build_slide1_overlay, 
                                 get_slide2_overlay, get_slide3_overlay, 
                                 get_slide4_overlay, get_slide5_overlay)
    
    # Topic icons mapped to what we passed
    topic_icons = {
        'ai_tool': '🤖', 'research': '🤖', 'ai': '🤖',
        'github': '💻', 'internship': '🏢', 'hackathon': '🏆',
        'jobs': '🚀', 'course': '📚', 'fellowship': '🎓'
    }
    
    import datetime
    day_idx = datetime.datetime.now().weekday()
    themes = [
        {"accent": "#00FFFF", "glow": "0,255,255", "badge": "CYBER DROP"}, # Mon
        {"accent": "#B040FF", "glow": "176,64,255", "badge": "SPACE DROP"}, # Tue
        {"accent": "#FFD700", "glow": "255,215,0", "badge": "GOLD DROP"}, # Wed
        {"accent": "#39FF14", "glow": "57,255,20", "badge": "MATRIX DROP"}, # Thu
        {"accent": "#FF4500", "glow": "255,69,0", "badge": "FIRE DROP"}, # Fri
        {"accent": "#00FFB3", "glow": "0,255,179", "badge": "AURORA DROP"}, # Sat
        {"accent": "#F7E7CE", "glow": "247,231,206", "badge": "PURE DROP"} # Sun
    ]
    theme = themes[day_idx]
    accent = theme["accent"]
    glow = theme["glow"]
    badge = theme["badge"]
    topic_icon = topic_icons.get(str(topic).lower(), '🤖')

    template_func = get_template_for_topic(topic)
    
    # Get Pexels Background for Slide 1
    bg_image_url = get_pexels_background(topic)
    
    # Slide 1 (Pass bg_image_url)
    overlay1 = build_slide1_overlay(hook_text, topic_icon, accent, glow, badge)
    html1 = template_func(accent, glow, badge, overlay1, bg_image_url)
    
    # Slide 2 (No bg image)
    overlay2 = get_slide2_overlay("WHAT IS THIS? 🤔", what_line1, what_line2, what_line3, accent, glow)
    html2 = template_func(accent, glow, badge, overlay2, "")
    
    # Slide 3
    overlay3 = get_slide3_overlay("HOW TO USE IT ⚡", steps, accent, glow)
    html3 = template_func(accent, glow, badge, overlay3, "")
    
    # Slide 4
    overlay4 = get_slide4_overlay("WHY THIS MATTERS 🌍", points, topic_icon, accent, glow)
    html4 = template_func(accent, glow, badge, overlay4, "")
    
    # Slide 5
    overlay5 = get_slide5_overlay(post_type, accent, glow)
    html5 = template_func(accent, glow, badge, overlay5, "")

    images = []
    for i, html in enumerate([html1, html2, html3, html4, html5]):
        out_png = f"{prefix}_{i+1}.png"
        await render_html_to_png(html, out_png)
        images.append(out_png)
        print(f"Generated {out_png}")
        
    return images
