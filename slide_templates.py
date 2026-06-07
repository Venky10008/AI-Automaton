import random

def colorize_keywords(text, accent_color):
    POWER_WORDS = {
        "FREE","NOBODY","SECRET","HIDDEN","NEW","JUST",
        "NOW","TODAY","DROPPED","BEST","MOST","ONLY",
        "FIRST","NEVER","ALWAYS","EVERY","ALERT","URGENT",
        "LIMITED","EXCLUSIVE","WIN","TOP","HUGE","THIS",
        "ZERO","MASSIVE","BROKE","VIRAL","LEAKED"
    }
    words = text.split()
    result = []
    for word in words:
        clean = ''.join(c for c in word if c.isalpha()).upper()
        if (clean in POWER_WORDS or
            any(char.isdigit() for char in word) or
            any(char in "🔥👀⚡😱🤯💰📚🚀💸🔒" for char in word)):
            result.append(
                f'<span style="color:{accent_color};">{word}</span>'
            )
        else:
            result.append(word)
    return " ".join(result)

def build_slide1_overlay(hook_text, topic_icon, accent, glow, badge):
    hook_html = colorize_keywords(hook_text, accent)
    return f"""
    <div style="position:absolute;top:45px;left:45px;
        background:rgba(0,0,0,0.65);
        border:1px solid rgba({glow},0.5);
        border-radius:50px;padding:10px 25px;
        font-family:'Montserrat',sans-serif;
        font-size:26px;font-weight:700;
        color:rgba(255,255,255,0.9);letter-spacing:2px;
        display:flex;align-items:center;gap:10px;
        backdrop-filter:blur(8px);z-index:100;">
        <div style="width:10px;height:10px;border-radius:50%;
            background:{accent};
            box-shadow:0 0 8px {accent};"></div>
        {badge}
    </div>
    <div style="position:absolute;bottom:210px;right:50px;
        font-size:85px;z-index:100;
        filter:drop-shadow(0 0 20px rgba({glow},0.8));">
        {topic_icon}
    </div>
    <div style="position:absolute;bottom:175px;
        left:50px;right:160px;z-index:100;
        font-family:'Bebas Neue',cursive;
        font-size:88px;color:white;line-height:1.05;
        letter-spacing:2px;
        text-shadow:0 0 50px rgba({glow},0.6),
                    0 3px 20px rgba(0,0,0,1);">
        {hook_html}
    </div>
    <div style="position:absolute;bottom:168px;left:50px;
        width:90px;height:5px;background:{accent};
        box-shadow:0 0 15px rgba({glow},0.8);
        border-radius:3px;z-index:100;"></div>
    <div style="position:absolute;bottom:115px;left:50%;
        transform:translateX(-50%);
        display:flex;align-items:center;gap:15px;
        z-index:100;white-space:nowrap;">
        <div style="height:1px;width:90px;
            background:rgba(255,255,255,0.35);"></div>
        <div style="font-family:'Montserrat',sans-serif;
            font-size:23px;font-weight:700;
            color:rgba(255,255,255,0.65);letter-spacing:2px;">
            @career_goals36
        </div>
        <div style="height:1px;width:90px;
            background:rgba(255,255,255,0.35);"></div>
    </div>
    <div style="position:absolute;bottom:55px;
        left:50px;right:50px;
        display:flex;justify-content:space-between;
        align-items:center;z-index:100;">
        <div style="font-family:'Montserrat',sans-serif;
            font-size:26px;font-weight:700;
            color:rgba(255,255,255,0.55);letter-spacing:3px;">
            Here is how →
        </div>
        <div style="font-family:'Montserrat',sans-serif;
            font-size:22px;font-weight:600;
            color:rgba(255,255,255,0.4);">
            @career_goals36
        </div>
    </div>
    """

def template_neural(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.4; mix-blend-mode: overlay;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:radial-gradient(ellipse at 40% 35%, #001a3a 0%, #000510 50%, #000000 100%);
}}
.bg-img {{ {bg_style} }}
.grid {{
    position:absolute;inset:0;
    background-image:
        linear-gradient(rgba(0,255,255,0.025) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,255,255,0.025) 1px,transparent 1px);
    background-size:60px 60px;
}}
.glow-tl {{
    position:absolute;top:-150px;left:-150px;
    width:600px;height:600px;border-radius:50%;
    background:radial-gradient(circle, rgba(0,255,255,0.13) 0%, transparent 70%);
    pointer-events:none;
}}
.glow-br {{
    position:absolute;bottom:-150px;right:-150px;
    width:500px;height:500px;border-radius:50%;
    background:radial-gradient(circle, rgba(0,100,255,0.09) 0%, transparent 70%);
    pointer-events:none;
}}
.hex-tl {{
    position:absolute;top:-15px;left:-15px;
    font-size:160px;color:rgba(0,255,255,0.04);
    font-weight:900;line-height:1;pointer-events:none;
}}
.hex-br {{
    position:absolute;bottom:200px;right:-15px;
    font-size:120px;color:rgba(0,255,255,0.03);
    pointer-events:none;
}}
.line-top {{
    position:absolute;top:120px;left:60px;right:60px;height:1px;
    background:linear-gradient(90deg,transparent, rgba(0,255,255,0.25),transparent);
}}
.line-bottom {{
    position:absolute;bottom:120px;left:60px;right:60px;height:1px;
    background:linear-gradient(90deg,transparent, rgba(0,255,255,0.2),transparent);
}}
.connections {{ position:absolute;inset:0; width:1080px;height:1080px; }}
.node {{ position:absolute;border-radius:50%; background:{accent}; box-shadow:0 0 15px {accent}, 0 0 30px {accent}; }}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:60%;
    background:linear-gradient(transparent,rgba(0,0,10,0.98));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="grid"></div>
    <div class="glow-tl"></div>
    <div class="glow-br"></div>
    <div class="hex-tl">⬡</div>
    <div class="hex-br">⬡</div>
    <div class="line-top"></div>
    <div class="line-bottom"></div>
    <svg class="connections" viewBox="0 0 1080 1080">
        <defs>
            <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        <line x1="200" y1="160" x2="540" y2="380" stroke="rgba(0,255,255,0.18)" stroke-width="1.5" filter="url(#glow)"/>
        <line x1="850" y1="180" x2="540" y2="380" stroke="rgba(0,255,255,0.15)" stroke-width="1.5" filter="url(#glow)"/>
        <line x1="160" y1="450" x2="540" y2="380" stroke="rgba(0,255,255,0.12)" stroke-width="1" filter="url(#glow)"/>
        <line x1="900" y1="420" x2="540" y2="380" stroke="rgba(0,255,255,0.12)" stroke-width="1" filter="url(#glow)"/>
        <line x1="280" y1="650" x2="540" y2="380" stroke="rgba(0,100,255,0.1)" stroke-width="1"/>
        <line x1="780" y1="600" x2="540" y2="380" stroke="rgba(0,100,255,0.1)" stroke-width="1"/>
        <circle cx="540" cy="380" r="16" fill="{accent}" filter="url(#glow)" style="box-shadow:0 0 30px {accent};"/>
        <circle cx="200" cy="160" r="9" fill="{accent}" opacity="0.85" filter="url(#glow)"/>
        <circle cx="850" cy="180" r="7" fill="{accent}" opacity="0.75" filter="url(#glow)"/>
        <circle cx="160" cy="450" r="6" fill="#0080FF" opacity="0.6" filter="url(#glow)"/>
        <circle cx="900" cy="420" r="6" fill="#0080FF" opacity="0.6" filter="url(#glow)"/>
        <circle cx="280" cy="650" r="5" fill="#0060FF" opacity="0.4"/>
        <circle cx="780" cy="600" r="5" fill="#0060FF" opacity="0.4"/>
    </svg>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_terminal(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.3; mix-blend-mode: luminosity;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{width:1080px;height:1080px;position:relative;background:#000;}}
.bg-img {{ {bg_style} }}
.terminal {{
    position:absolute;
    top:80px;left:80px;right:80px;bottom:280px;
    border:2px solid rgba({glow},0.35);
    border-radius:12px;
    background:rgba(0,20,0,0.4);
    overflow:hidden;
}}
.terminal-bar {{
    height:35px;
    background:rgba({glow},0.08);
    border-bottom:1px solid rgba({glow},0.2);
    display:flex;align-items:center;
    padding:0 15px;gap:8px;
}}
.dot {{width:12px;height:12px;border-radius:50%;}}
.dot-r {{background:#FF5F56;}}
.dot-y {{background:#FFBD2E;}}
.dot-g {{background:#27C93F;}}
.code-lines {{
    padding:20px;
    font-family:monospace;font-size:20px;
    color:rgba({glow},0.2);
    line-height:1.9;
    white-space:pre-wrap;
}}
.octocat {{
    position:absolute;top:50%;left:50%;
    transform:translate(-50%,-60%);
    font-size:320px;opacity:0.06;
    pointer-events:none;
}}
.scanline {{
    position:absolute;inset:0;
    background:linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
    background-size:100% 4px;
    opacity:0.2; pointer-events:none;
}}
.matrix-col {{
    position:absolute;top:0;bottom:0;width:40px;
    font-family:monospace;font-size:18px;color:{accent};opacity:0.07;
    overflow:hidden;word-break:break-all;
}}
.bracket-l {{position:absolute;top:20px;left:20px;font-size:80px;color:rgba({glow},0.1);font-family:monospace;}}
.bracket-r {{position:absolute;top:20px;right:20px;font-size:80px;color:rgba({glow},0.1);font-family:monospace;}}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:40%;
    background:linear-gradient(transparent,rgba(0,0,0,0.98));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="matrix-col" style="left:10px;">{'10'*500}</div>
    <div class="matrix-col" style="right:10px;">{'01'*500}</div>
    <div class="bracket-l">&lt;</div>
    <div class="bracket-r">&gt;</div>
    <div class="octocat">🐱</div>
    <div class="terminal">
        <div class="terminal-bar">
            <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
        </div>
        <div class="code-lines">
import os
import sys
def init_system():
    # initializing secure connection
    connect("127.0.0.1", port=443)
    auth_token = os.getenv("SECRET")
    print("Access Granted.")
    run_sequence(auto=True)
    while True:
        data = stream.read(1024)
        if not data: break
        process(data)
        </div>
    </div>
    <div class="scanline"></div>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_city(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.4; mix-blend-mode: screen;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:linear-gradient(180deg, #000510 0%, #000a1a 30%, #001030 60%, #000820 100%);
}}
.bg-img {{ {bg_style} }}
.stars {{
    position:absolute;top:0;left:0;right:0;height:65%;
}}
.stars::after {{
    content:'';position:absolute;top:10px;left:10px;width:2px;height:2px;background:white;
    box-shadow: 100px 50px white, 300px 150px white, 500px 80px white, 700px 200px white, 900px 40px white,
                150px 300px white, 350px 450px white, 600px 380px white, 800px 500px white, 1000px 250px white,
                200px 100px white, 400px 50px white, 650px 180px white, 850px 90px white, 50px 400px white;
    opacity:0.4;
}}
.skyline {{
    position:absolute;bottom:0;left:0;right:0;height:400px;
    display:flex;align-items:flex-end;opacity:0.8;
}}
.bldg {{
    background:#0a1526; border-top:1px solid #1a2a40; border-right:1px solid #1a2a40;
    background-image: radial-gradient(#FFD700 1px, transparent 1px);
    background-size: 15px 15px; background-position: 0 0;
}}
.trend-line {{
    position:absolute;bottom:150px;left:0;width:1080px;height:400px;
    pointer-events:none;
}}
.arrow-bg {{
    position:absolute;top:100px;right:100px;font-size:400px;color:rgba(255,255,255,0.03);
    font-weight:bold;pointer-events:none;
}}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:50%;
    background:linear-gradient(transparent,rgba(0,0,0,0.95));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="stars"></div>
    <div class="arrow-bg">↑</div>
    <div class="skyline">
        <div class="bldg" style="width:80px;height:150px;"></div>
        <div class="bldg" style="width:120px;height:300px;"></div>
        <div class="bldg" style="width:90px;height:220px;"></div>
        <div class="bldg" style="width:150px;height:350px;"></div>
        <div class="bldg" style="width:100px;height:180px;"></div>
        <div class="bldg" style="width:130px;height:280px;"></div>
        <div class="bldg" style="width:110px;height:380px;"></div>
        <div class="bldg" style="width:140px;height:250px;"></div>
        <div class="bldg" style="width:90px;height:200px;"></div>
        <div class="bldg" style="width:70px;height:120px;"></div>
    </div>
    <svg class="trend-line" viewBox="0 0 1080 400">
        <path d="M 0 350 Q 200 300 400 320 T 700 200 T 1080 50"
              fill="none" stroke="{accent}" stroke-width="4"
              style="filter:drop-shadow(0 0 10px {accent});"/>
    </svg>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_hackathon(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.35; mix-blend-mode: lighten;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:radial-gradient(ellipse at center, #1a0500 0%, #0d0000 50%, #000000 100%);
}}
.bg-img {{ {bg_style} }}
.trophy {{
    position:absolute;top:40%;left:50%;transform:translate(-50%,-50%);
    width:160px;height:180px;
}}
.trophy-top {{
    width:100%;height:100px;background:linear-gradient(135deg, #FFD700, #DAA520);
    border-radius:10px 10px 40px 40px;
    box-shadow:0 0 50px rgba(255,215,0,0.4);
}}
.trophy-base {{
    width:80px;height:60px;background:linear-gradient(135deg, #DAA520, #B8860B);
    margin:0 auto; clip-path: polygon(20% 0, 80% 0, 100% 100%, 0% 100%);
}}
.trophy-stem {{
    width:20px;height:20px;background:#DAA520;margin:0 auto;
}}
.bolts {{
    position:absolute;inset:0;
}}
.particles {{
    position:absolute;inset:0;
}}
.particles::after {{
    content:'';position:absolute;top:50%;left:50%;width:4px;height:4px;background:#FFD700;
    box-shadow: 100px -150px #FFD700, -200px 150px #FFD700, 300px 80px #FFD700, -100px -200px #FFD700,
                150px 200px #FFD700, -300px -50px #FFD700, 200px -250px #FFD700, -150px 250px #FFD700;
    border-radius:50%; opacity:0.6; filter:blur(1px);
}}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:50%;
    background:linear-gradient(transparent,rgba(0,0,0,0.95));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <svg class="bolts" viewBox="0 0 1080 1080">
        <polygon points="540,540 800,200 750,450 950,400" fill="rgba(255,215,0,0.1)"/>
        <polygon points="540,540 280,200 330,450 130,400" fill="rgba(255,215,0,0.1)"/>
        <polygon points="540,540 800,880 750,630 950,680" fill="rgba(255,215,0,0.05)"/>
        <polygon points="540,540 280,880 330,630 130,680" fill="rgba(255,215,0,0.05)"/>
    </svg>
    <div class="particles"></div>
    <div class="trophy">
        <div class="trophy-top"></div>
        <div class="trophy-stem"></div>
        <div class="trophy-base"></div>
    </div>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_knowledge(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.3; mix-blend-mode: overlay;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:radial-gradient(ellipse at 50% 60%, #1a0e00 0%, #0d0800 40%, #000000 100%);
}}
.bg-img {{ {bg_style} }}
.book {{
    position:absolute;top:45%;left:50%;transform:translate(-50%,-50%);
    display:flex; justify-content:center;
}}
.page-l, .page-r {{
    width:120px;height:160px;
    background:linear-gradient(135deg, rgba(255,215,0,0.8), rgba(218,165,32,0.4));
    border-radius:10px 5px 5px 10px;
    box-shadow:inset 0 0 20px rgba(255,255,255,0.5);
}}
.page-l {{ transform:perspective(400px) rotateY(20deg); transform-origin:right; border-right:2px solid #fff; }}
.page-r {{ transform:perspective(400px) rotateY(-20deg); transform-origin:left; border-left:2px solid #fff; }}
.rays {{
    position:absolute;top:0;left:0;right:0;bottom:40%;
    background:conic-gradient(from -90deg at 50% 100%, transparent 40deg, rgba(255,215,0,0.15) 60deg, transparent 80deg, rgba(255,215,0,0.1) 100deg, transparent 120deg);
}}
.symbols {{
    position:absolute;inset:0;font-size:40px;color:rgba(255,255,255,0.08);font-family:serif;
}}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:50%;
    background:linear-gradient(transparent,rgba(0,0,0,0.98));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="rays"></div>
    <div class="symbols">
        <span style="position:absolute;top:100px;left:200px;">∑</span>
        <span style="position:absolute;top:200px;right:250px;">π</span>
        <span style="position:absolute;top:300px;left:300px;">∞</span>
        <span style="position:absolute;top:150px;right:400px;">∂</span>
        <span style="position:absolute;top:400px;left:150px;">√</span>
    </div>
    <div class="book">
        <div class="page-l"></div>
        <div class="page-r"></div>
    </div>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_achievement(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.35; mix-blend-mode: soft-light;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:linear-gradient(135deg, #000510 0%, #000820 50%, #000510 100%);
}}
.bg-img {{ {bg_style} }}
.spotlight {{
    position:absolute;top:0;left:20%;right:20%;height:60%;
    background:conic-gradient(from 150deg at 50% 0%, transparent 0deg, rgba(255,215,0,0.1) 30deg, transparent 60deg);
}}
.cap {{
    position:absolute;top:35%;left:50%;transform:translate(-50%,-50%);
    width:140px;height:140px;
}}
.cap-top {{
    width:140px;height:140px;background:linear-gradient(135deg, #FFD700, #DAA520);
    transform:rotate(45deg) scaleY(0.6);
    box-shadow:0 0 30px rgba(255,215,0,0.4);
}}
.cap-base {{
    position:absolute;top:70px;left:35px;width:70px;height:50px;
    background:#111; border-radius:0 0 50% 50%;
}}
.confetti {{
    position:absolute;inset:0;
}}
.confetti::after {{
    content:'';position:absolute;width:10px;height:20px;background:#FFD700;
    box-shadow: 100px 150px #fff, 300px 80px {accent}, 500px 200px #FFD700, 700px 50px #fff, 900px 250px {accent},
                200px 300px #FFD700, 400px 180px #fff, 600px 350px {accent}, 800px 120px #FFD700;
    transform:rotate(45deg); opacity:0.6;
}}
.stars-bg {{ position:absolute;inset:0;font-size:30px;color:rgba(255,215,0,0.3); }}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:50%;
    background:linear-gradient(transparent,rgba(0,0,0,0.98));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="spotlight"></div>
    <div class="stars-bg">
        <span style="position:absolute;top:150px;left:200px;">⭐</span>
        <span style="position:absolute;top:250px;right:250px;">⭐</span>
        <span style="position:absolute;top:350px;left:400px;">⭐</span>
    </div>
    <div class="confetti"></div>
    <div class="cap">
        <div class="cap-base"></div>
        <div class="cap-top"></div>
    </div>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def template_career(accent, glow, badge, text_overlay, bg_image=""):
    bg_style = f"background: url('{bg_image}') center/cover; position:absolute; inset:0; opacity:0.3; mix-blend-mode: overlay;" if bg_image else ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:1080px;height:1080px;overflow:hidden;background:#000;}}
.slide {{
    width:1080px;height:1080px;position:relative;
    background:linear-gradient(180deg, #050010 0%, #0a0020 50%, #050010 100%);
}}
.bg-img {{ {bg_style} }}
.road {{
    position:absolute;bottom:0;left:50%;transform:translateX(-50%);
    width:800px;height:500px;
    background:#111;
    clip-path: polygon(40% 0, 60% 0, 100% 100%, 0% 100%);
}}
.center-line {{
    position:absolute;bottom:0;left:50%;transform:translateX(-50%);
    width:6px;height:500px;
    background:repeating-linear-gradient(0deg, #fff 0, #fff 40px, transparent 40px, transparent 80px);
    opacity:0.5;
}}
.milestone {{
    position:absolute;left:50%;transform:translateX(-50%);
    width:20px;height:10px;background:{accent};border-radius:50%;
    box-shadow:0 0 20px {accent};
}}
.sky {{ position:absolute;top:0;left:0;right:0;height:50%; }}
.moon {{
    position:absolute;top:100px;right:150px;width:100px;height:100px;
    background:#fff;border-radius:50%;box-shadow:0 0 50px rgba(255,255,255,0.5);
    opacity:0.8;
}}
.rocket {{
    position:absolute;top:150px;left:200px;font-size:120px;opacity:0.07;
    transform:rotate(45deg);
}}
.gradient-bottom {{
    position:absolute;bottom:0;left:0;right:0;height:40%;
    background:linear-gradient(transparent,rgba(0,0,0,0.98));
}}
</style>
</head>
<body>
<div class="slide">
    <div class="bg-img"></div>
    <div class="sky">
        <div class="moon"></div>
        <div class="rocket">🚀</div>
    </div>
    <div class="road">
        <div class="center-line"></div>
        <div class="milestone" style="bottom:100px;width:40px;height:20px;"></div>
        <div class="milestone" style="bottom:250px;width:30px;height:15px;"></div>
        <div class="milestone" style="bottom:380px;width:20px;height:10px;"></div>
    </div>
    <div class="gradient-bottom"></div>
    {text_overlay}
</div>
</body>
</html>"""

def get_template_for_topic(topic):
    topic = str(topic).lower()
    if topic in ['ai_tool', 'research', 'ai']: return template_neural
    if topic == 'github': return template_terminal
    if topic == 'internship': return template_city
    if topic == 'hackathon': return template_hackathon
    if topic == 'course': return template_knowledge
    if topic == 'fellowship': return template_achievement
    if topic == 'jobs': return template_career
    return template_neural # default

def get_slide2_overlay(heading, what_line1, what_line2, what_line3, accent, glow):
    return f"""
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.72);z-index:50;"></div>
    <div style="position:absolute;top:80px;left:60px;z-index:100;
        font-family:'Bebas Neue',cursive;font-size:90px;color:{accent};
        text-shadow:0 0 30px rgba({glow},0.5);">{heading}</div>
    <div style="position:absolute;top:220px;left:60px;right:60px;z-index:100;display:flex;flex-direction:column;gap:30px;">
        <div style="background:rgba(0,0,0,0.75);border-left:8px solid {accent};border-radius:0 20px 20px 0;padding:30px;">
            <div style="color:{accent};font-family:'Montserrat',sans-serif;font-size:26px;font-weight:800;letter-spacing:2px;margin-bottom:10px;">WHAT IT DOES</div>
            <div style="color:white;font-family:'Montserrat',sans-serif;font-size:46px;font-weight:800;line-height:1.2;">{what_line1}</div>
        </div>
        <div style="background:rgba(0,0,0,0.75);border-left:6px solid white;border-radius:0 20px 20px 0;padding:30px;">
            <div style="color:#aaa;font-family:'Montserrat',sans-serif;font-size:24px;font-weight:700;letter-spacing:2px;margin-bottom:10px;">THE PROBLEM IT SOLVES</div>
            <div style="color:white;font-family:'Montserrat',sans-serif;font-size:42px;font-weight:700;line-height:1.2;">{what_line2}</div>
        </div>
        <div style="background:rgba({glow},0.12);border:1px solid {accent};border-radius:16px;padding:30px;text-align:center;">
            <div style="color:white;font-family:'Montserrat',sans-serif;font-size:40px;font-weight:700;">👥 Built for: {what_line3}</div>
        </div>
    </div>
    <div style="position:absolute;bottom:40px;right:60px;z-index:100;font-family:'Montserrat',sans-serif;font-size:24px;color:rgba(255,255,255,0.4);font-weight:600;">@career_goals36</div>
    """

def get_slide3_overlay(heading, steps, accent, glow):
    steps_html = ""
    for i, step in enumerate(steps):
        steps_html += f"""
        <div style="display:flex;align-items:center;gap:30px;">
            <div style="width:80px;height:80px;border-radius:50%;background:{accent};box-shadow:0 0 25px rgba({glow},0.7);display:flex;justify-content:center;align-items:center;font-family:'Bebas Neue',cursive;font-size:55px;color:black;">{i+1}</div>
            <div style="background:rgba(0,0,0,0.75);padding:20px 30px;border-radius:16px;flex:1;color:white;font-family:'Montserrat',sans-serif;font-size:44px;font-weight:700;">{step}</div>
        </div>
        """
        if i < len(steps) - 1:
            steps_html += f'<div style="text-align:center;color:{accent};font-size:40px;margin:10px 0;">↓</div>'

    return f"""
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.72);z-index:50;"></div>
    <div style="position:absolute;top:80px;left:60px;z-index:100;font-family:'Bebas Neue',cursive;font-size:85px;color:{accent};text-shadow:0 0 30px rgba({glow},0.5);">{heading}</div>
    <div style="position:absolute;top:200px;left:60px;right:60px;z-index:100;display:flex;flex-direction:column;">
        {steps_html}
    </div>
    <div style="position:absolute;bottom:120px;left:0;right:0;text-align:center;z-index:100;color:{accent};font-family:'Montserrat',sans-serif;font-size:42px;font-weight:700;">That is literally it. 🎯</div>
    <div style="position:absolute;bottom:40px;right:60px;z-index:100;font-family:'Montserrat',sans-serif;font-size:24px;color:rgba(255,255,255,0.4);font-weight:600;">@career_goals36</div>
    """

def get_slide4_overlay(heading, points, topic_icon, accent, glow):
    labels = ["IMPACT", "WHO BENEFITS", "NOW POSSIBLE"]
    points_html = ""
    for i, point in enumerate(points):
        bg = f"rgba({glow},0.12)" if i == 2 else "rgba(0,0,0,0.72)"
        border = f"border:1px solid {accent};border-radius:16px;" if i==2 else f"border-left:6px solid {accent};border-radius:0 16px 16px 0;"
        points_html += f"""
        <div style="background:{bg};{border}padding:25px;display:flex;align-items:center;gap:25px;">
            <div style="font-size:52px;">{topic_icon}</div>
            <div style="display:flex;flex-direction:column;gap:5px;">
                <div style="color:{accent};font-family:'Montserrat',sans-serif;font-size:26px;font-weight:800;letter-spacing:2px;">{labels[i]}</div>
                <div style="color:white;font-family:'Montserrat',sans-serif;font-size:44px;font-weight:800;line-height:1.2;">{point}</div>
            </div>
        </div>
        """

    return f"""
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.72);z-index:50;"></div>
    <div style="position:absolute;top:80px;left:60px;z-index:100;font-family:'Bebas Neue',cursive;font-size:85px;color:{accent};text-shadow:0 0 30px rgba({glow},0.5);">{heading}</div>
    <div style="position:absolute;top:220px;left:60px;right:60px;z-index:100;display:flex;flex-direction:column;gap:35px;">
        {points_html}
    </div>
    <div style="position:absolute;bottom:120px;left:0;right:0;text-align:center;z-index:100;color:{accent};font-family:'Montserrat',sans-serif;font-size:42px;font-weight:900;">The future is already here. 🚀</div>
    <div style="position:absolute;bottom:40px;right:60px;z-index:100;font-family:'Montserrat',sans-serif;font-size:24px;color:rgba(255,255,255,0.4);font-weight:600;">@career_goals36</div>
    """

def get_slide5_overlay(post_type, accent, glow):
    if post_type == "AI":
        cta_word = "AI"
        tag_text = "👇 What do you think about this?"
        follow_sub = "Daily AI drops 🔥"
    else:
        cta_word = "SEND"
        tag_text = "👇 Tag a friend who needs this!"
        follow_sub = "Daily AI + Student drops 🔥"

    return f"""
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.72);z-index:50;"></div>
    <div style="position:absolute;top:100px;left:0;right:0;text-align:center;z-index:100;font-family:'Bebas Neue',cursive;font-size:108px;color:white;text-shadow:0 0 40px rgba({glow},0.8);">WANT THE LINK? 🔗</div>
    <div style="position:absolute;top:260px;left:60px;right:60px;z-index:100;background:rgba({glow},0.12);border:2px solid {accent};border-radius:24px;padding:50px 40px;display:flex;flex-direction:column;gap:25px;text-align:center;">
        <div style="color:white;font-family:'Montserrat',sans-serif;font-size:50px;font-weight:800;">💬 Comment "{cta_word}" below</div>
        <div style="color:white;font-family:'Montserrat',sans-serif;font-size:50px;font-weight:800;">📩 I'll DM you the link in 5 mins!</div>
        <div style="color:#FFB800;font-family:'Montserrat',sans-serif;font-size:40px;font-weight:700;margin-top:10px;">⚠️ Follow first — DMs only reach followers!</div>
    </div>
    <div style="position:absolute;top:620px;left:200px;right:200px;height:4px;background:linear-gradient(90deg,transparent,{accent},transparent);z-index:100;"></div>
    <div style="position:absolute;top:680px;left:0;right:0;text-align:center;z-index:100;color:white;font-family:'Montserrat',sans-serif;font-size:40px;font-weight:700;">{tag_text}</div>
    <div style="position:absolute;bottom:100px;left:150px;right:150px;z-index:100;background:white;border-radius:20px;padding:30px;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,0.5);">
        <div style="color:black;font-family:'Bebas Neue',cursive;font-size:52px;line-height:1;">FOLLOW @career_goals36</div>
        <div style="color:#333;font-family:'Montserrat',sans-serif;font-size:28px;font-weight:600;margin-top:5px;">{follow_sub}</div>
    </div>
    """
