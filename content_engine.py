import requests
from bs4 import BeautifulSoup
import datetime
import random

def get_huggingface_papers():
    url = "https://huggingface.co/papers"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        papers = soup.select('div.relative.flex.flex-col.overflow-hidden.rounded-xl')
        for paper in papers:
            title_el = paper.select_single('h3')
            if title_el:
                title = title_el.text.strip()
                desc_el = paper.select_single('p')
                desc = desc_el.text.strip() if desc_el else "New AI research breakthrough."
                link_el = paper.find('a')
                if link_el:
                    link = "https://huggingface.co" + link_el['href']
                    return {"title": title, "description": desc, "url": link}
    except Exception as e:
        print(f"HF Error: {e}")
    return None

def get_producthunt_ai():
    url = "https://www.producthunt.com/topics/artificial-intelligence"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Very rough parsing, product hunt has complex react classes
        items = soup.select('a[data-test="product-item-name"]')
        for item in items:
            title = item.text.strip()
            desc_el = item.find_next_sibling('div')
            desc = desc_el.text.strip() if desc_el else "Amazing new AI tool."
            link = "https://www.producthunt.com" + item['href']
            return {"title": title, "description": desc, "url": link}
    except Exception as e:
        print(f"ProductHunt Error: {e}")
    return None

def get_arxiv_ai():
    url = "https://arxiv.org/list/cs.AI/recent"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        dts = soup.find_all('dt')
        dds = soup.find_all('dd')
        if dts and dds:
            title = dds[0].find('div', class_='list-title').text.replace('Title:', '').strip()
            link = "https://arxiv.org" + dts[0].find('a', title='Abstract')['href']
            return {"title": title, "description": "New breakthrough in AI research.", "url": link}
    except Exception as e:
        print(f"Arxiv Error: {e}")
    return None

def get_github_trending():
    url = "https://github.com/trending"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        repos = soup.select('article.Box-row')
        for repo in repos:
            h2 = repo.find('h2')
            a = h2.find('a')
            title = a.text.strip().replace('\n', '').replace(' ', '')
            desc_p = repo.find('p')
            desc = desc_p.text.strip() if desc_p else "Trending repository on GitHub."
            link = "https://github.com" + a['href']
            return {"title": title, "description": desc, "url": link}
    except Exception as e:
        print(f"Github Error: {e}")
    return None

# Fallback basic content for testing
FALLBACK_AI = {
    "title": "New Auto-Coding Agent Framework Released",
    "description": "A new framework for building autonomous coding agents was just open sourced. It can build full stack web apps from scratch in minutes.",
    "url": "https://github.com/trending"
}

FALLBACK_STUDENT = {
    "title": "Google Summer of Code 2026",
    "description": "Google is accepting applications for GSOC 2026. Get paid a massive stipend to contribute to open source projects this summer.",
    "url": "https://summerofcode.withgoogle.com/"
}

def generate_ai_content():
    # Rotate sources based on day
    day = datetime.datetime.now().weekday()
    raw = None
    if day % 3 == 0:
        raw = get_huggingface_papers() or get_producthunt_ai()
    elif day % 3 == 1:
        raw = get_producthunt_ai() or get_arxiv_ai()
    else:
        raw = get_arxiv_ai() or get_huggingface_papers()
        
    if not raw:
        raw = FALLBACK_AI
        
    hooks = [
        "THIS NEW AI JUST MADE CHATGPT LOOK BASIC 🤯",
        "NOBODY IS TALKING ABOUT THIS NEW AI MODEL 👀",
        "THIS AI WAS JUST RELEASED AND IT CHANGES EVERYTHING ⚡",
        "SCIENTISTS JUST BUILT AN AI THAT NOBODY THOUGHT POSSIBLE 😱",
        "THIS FREE TOOL JUST REPLACED 5 PAID SUBSCRIPTIONS 💸"
    ]
    
    return {
        "topic": "ai_tool",
        "post_type": "AI",
        "hook_text": random.choice(hooks),
        "what_line1": raw['title'][:45],
        "what_line2": raw['description'][:65],
        "what_line3": "Developers & Researchers 🧠",
        "steps": [
            "Visit the link in the next slide",
            "Explore the tool/resource",
            "Start using it right away 🚀"
        ],
        "points": [
            "Saves hours of manual work ⏱️",
            "Anyone with a laptop can use it 💻",
            "The future is already here 🌍"
        ],
        "source_link": raw['url'],
        "caption_hook": random.choice(hooks)
    }

def generate_student_content():
    day = datetime.datetime.now().weekday()
    raw = None
    topic = "github"
    hook = "THIS FREE REPO HAS 10K STARS AND NOBODY KNOWS IT 🔥"
    
    if day == 0 or day == 6: # Mon/Sun
        raw = get_github_trending()
        topic = "github"
        hook = "THE MOST STARRED REPO THIS WEEK AND IT IS FREE 🌟"
    elif day == 1 or day == 4: # Tue/Fri
        raw = FALLBACK_STUDENT
        topic = "internship"
        hook = "INTERNSHIP ALERT — APPLY BEFORE IT CLOSES ⚡"
    else:
        raw = FALLBACK_STUDENT
        topic = "course"
        hook = "FREE COURSE THAT COSTS ₹50,000 ELSEWHERE 📚"
        
    if not raw:
        raw = FALLBACK_STUDENT
        
    return {
        "topic": topic,
        "post_type": "STUDENT",
        "hook_text": hook,
        "what_line1": raw['title'][:45],
        "what_line2": raw['description'][:65],
        "what_line3": "CS Students & Freshers 🎓",
        "steps": [
            "Open the link from the post",
            "Create your account/profile",
            "Apply or start learning today 💪"
        ],
        "points": [
            "Huge boost for your resume 📄",
            "Perfect for students & freshers 👨‍🎓",
            "Don't miss this opportunity 🎯"
        ],
        "source_link": raw['url'],
        "caption_hook": hook
    }
