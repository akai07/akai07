import re

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def extract_svg_content(svg_str):
    # Extract viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_str)
    viewbox = viewbox_match.group(1) if viewbox_match else "0 0 100 100"
    
    # Extract inner content (everything between <svg> and </svg>)
    # Simple parsing: find first > after <svg and last </svg>
    start_tag_end = svg_str.find('>')
    svg_start = svg_str.find('<svg')
    
    if svg_start != -1 and start_tag_end != -1:
        # Find the closing tag
        body = svg_str[start_tag_end+1:]
        body = body.replace('</svg>', '')
        return viewbox, body.strip()
    return viewbox, ""

try:
    kai_school = read_file('Kaischoollogo.svg')
    kai_bot = read_file('Kaibotlogo.svg')
    
    # Replace black fills with White (#FFFFFF) for visibility on dark background
    # This preserves the logo's neutrality while making it visible
    kai_school_content = kai_school.replace('fill="#020202"', 'fill="#FFFFFF"')
    kai_bot_content = kai_bot.replace('fill="#010101"', 'fill="#FFFFFF"')
    
    ks_vb, ks_inner = extract_svg_content(kai_school_content)
    kb_vb, kb_inner = extract_svg_content(kai_bot_content)
    
    # Advanced Anime.js-style SVG Template
    # Changes: 
    # 1. Logos are now White (neutral) instead of Cyan
    # 2. Both logos constrained to identical 160x160 box for visual consistency
    # 3. Cleaned up background and glow effects
    svg_template = f'''<svg width="800" height="350" viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Dark SaaS Background -->
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
        </linearGradient>
        
        <!-- Subtle Glow for White Logos -->
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- Circuit Line Gradient -->
        <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#38bdf8" stop-opacity="0" />
          <stop offset="50%" stop-color="#38bdf8" stop-opacity="1" />
          <stop offset="100%" stop-color="#38bdf8" stop-opacity="0" />
        </linearGradient>
      </defs>

      <!-- Background Container -->
      <rect width="800" height="350" rx="16" fill="url(#bg-grad)" stroke="#334155" stroke-width="1" />
      
      <!-- Animated Grid (Subtler) -->
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#38bdf8" stroke-width="0.5" opacity="0.05"/>
      </pattern>
      <rect width="800" height="350" rx="16" fill="url(#grid)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="0 40" dur="4s" repeatCount="indefinite" />
      </rect>

      <!-- Connecting Circuit Line -->
      <!-- Drawn between center points: ~250 (Left) to ~550 (Right) -->
      <path d="M 330 155 L 470 155" stroke="url(#line-grad)" stroke-width="2" stroke-dasharray="140" stroke-dashoffset="140" opacity="0.8">
        <animate attributeName="stroke-dashoffset" values="140;0;140" dur="3s" repeatCount="indefinite" fill="freeze" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1" />
      </path>
      <circle cx="400" cy="155" r="4" fill="#38bdf8">
        <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite" />
      </circle>

      <!-- LEFT LOGO: KAISCHOOL -->
      <!-- Centered at x=200 -->
      <g transform="translate(150, 60)">
        <!-- Floating Animation -->
        <animateTransform attributeName="transform" type="translate" values="150,60; 150,50; 150,60" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" />
        
        <!-- Logo Container: 200x200 box, centered content -->
        <!-- Using preserveAspectRatio="xMidYMid meet" to force same size constraints -->
        <svg width="200" height="200" viewBox="{ks_vb}" preserveAspectRatio="xMidYMid meet" filter="url(#glow)">
          {ks_inner}
        </svg>
        
        <!-- Label -->
        <text x="100" y="230" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-weight="600" fill="#cbd5e1" font-size="16" letter-spacing="4">KAISCHOOL</text>
      </g>

      <!-- RIGHT LOGO: KAIBOT -->
      <!-- Centered at x=600 (450 + 150 offset) -->
      <g transform="translate(450, 60)">
         <!-- Floating Animation (Staggered) -->
        <animateTransform attributeName="transform" type="translate" values="450,60; 450,70; 450,60" dur="6s" begin="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" />
        
        <!-- Logo Container: 200x200 box, centered content -->
        <svg width="200" height="200" viewBox="{kb_vb}" preserveAspectRatio="xMidYMid meet" filter="url(#glow)">
          {kb_inner}
        </svg>
        
        <!-- Label -->
        <text x="100" y="230" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-weight="600" fill="#cbd5e1" font-size="16" letter-spacing="4">KAIBOT</text>
      </g>

    </svg>'''
    
    with open('profile-header.svg', 'w') as f:
        f.write(svg_template)
    print("Successfully generated profile-header.svg")

except Exception as e:
    print(f"Error: {e}")
