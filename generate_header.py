import re

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def extract_svg_content(svg_str):
    # Extract viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_str)
    viewbox = viewbox_match.group(1) if viewbox_match else "0 0 100 100"
    
    # Remove XML declaration and doctype
    content = re.sub(r'<\?xml.*?\?>', '', svg_str)
    content = re.sub(r'<!DOCTYPE.*?>', '', content)
    
    # Find the content inside the <svg> tags
    # We use a simple approach: find the first > after <svg and the last </svg>
    start_tag_end = content.find('>')
    svg_start = content.find('<svg')
    
    if svg_start != -1 and start_tag_end != -1:
        # Get content after <svg...>
        body = content[start_tag_end+1:]
        # Remove last </svg>
        body = body.replace('</svg>', '')
        return viewbox, body.strip()
    
    return viewbox, ""

try:
    kai_school = read_file('Kaischoollogo.svg')
    kai_bot = read_file('Kaibotlogo.svg')

    # Change colors to cyan/white for dark mode
    # Kaischool uses #020202
    kai_school_content = kai_school.replace('fill="#020202"', 'fill="#00f2ff"') # Cyan Neon
    
    # Kaibot uses #010101
    kai_bot_content = kai_bot.replace('fill="#010101"', 'fill="#00f2ff"') # Cyan Neon

    ks_vb, ks_inner = extract_svg_content(kai_school_content)
    kb_vb, kb_inner = extract_svg_content(kai_bot_content)

    svg_template = f'''<svg width="800" height="350" viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
        </linearGradient>
        
        <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:0" />
          <stop offset="50%" style="stop-color:#38bdf8;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#38bdf8;stop-opacity:0" />
        </linearGradient>

        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <!-- Background with Rounded Corners -->
      <rect width="800" height="350" rx="12" fill="url(#bg-grad)" stroke="#334155" stroke-width="1" />

      <!-- Animated Grid Background -->
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#38bdf8" stroke-width="0.5" opacity="0.1"/>
      </pattern>
      <rect width="800" height="350" rx="12" fill="url(#grid)">
        <animateTransform attributeName="transform" type="translate" from="0 0" to="0 40" dur="3s" repeatCount="indefinite" />
      </rect>

      <!-- HUD Decor Lines -->
      <line x1="50" y1="50" x2="750" y2="50" stroke="url(#line-grad)" stroke-width="1" opacity="0.3">
         <animate attributeName="opacity" values="0.1;0.5;0.1" dur="4s" repeatCount="indefinite" />
      </line>
      <line x1="50" y1="300" x2="750" y2="300" stroke="url(#line-grad)" stroke-width="1" opacity="0.3">
         <animate attributeName="opacity" values="0.1;0.5;0.1" dur="4s" repeatCount="indefinite" />
      </line>

      <!-- Center Circuit Connection -->
      <path d="M 330 175 L 470 175" stroke="#38bdf8" stroke-width="2" stroke-dasharray="140" stroke-dashoffset="140" opacity="0.8">
        <animate attributeName="stroke-dashoffset" values="140;0" dur="1.5s" begin="0.5s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.25 0.1 0.25 1" />
      </path>
      
      <!-- Central Node Pulse -->
      <circle cx="400" cy="175" r="3" fill="#38bdf8">
        <animate attributeName="r" values="3;6;3" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite" />
      </circle>

      <!-- KaiSchool Container (Left) -->
      <g transform="translate(130, 75)">
        <!-- Hover Animation -->
        <animateTransform attributeName="transform" type="translate" values="130,75; 130,65; 130,75" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" />
        
        <!-- Logo -->
        <svg width="200" height="200" viewBox="{ks_vb}" filter="url(#glow)">
          {ks_inner}
        </svg>
        
        <!-- Label -->
        <text x="100" y="210" text-anchor="middle" font-family="Segoe UI, Verdana, sans-serif" font-weight="700" fill="#fff" font-size="20" letter-spacing="3" opacity="0.9">KAISCHOOL</text>
      </g>

      <!-- KaiBot Container (Right) -->
      <g transform="translate(470, 90)">
        <!-- Hover Animation (Staggered) -->
        <animateTransform attributeName="transform" type="translate" values="470,90; 470,100; 470,90" dur="6s" begin="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" />
        
        <!-- Logo (Aspect Ratio Adjusted) -->
        <svg width="200" height="170" viewBox="{kb_vb}" filter="url(#glow)">
          {kb_inner}
        </svg>
        
        <!-- Label -->
        <text x="100" y="195" text-anchor="middle" font-family="Segoe UI, Verdana, sans-serif" font-weight="700" fill="#fff" font-size="20" letter-spacing="3" opacity="0.9">KAIBOT</text>
      </g>

      <!-- Status Text -->
      <text x="400" y="30" text-anchor="middle" font-family="Consolas, monospace" fill="#64748b" font-size="10" letter-spacing="2">/// SYSTEM.STATUS: ONLINE ///</text>
      <text x="400" y="330" text-anchor="middle" font-family="Consolas, monospace" fill="#64748b" font-size="10" letter-spacing="2">ARCHITECTING THE FUTURE OF ED-TECH</text>

    </svg>'''

    with open('profile-header.svg', 'w') as f:
        f.write(svg_template)
    print("Successfully generated profile-header.svg")

except Exception as e:
    print(f"Error: {e}")
