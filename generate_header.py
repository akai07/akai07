import re

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def extract_svg_content(svg_str):
    viewbox_match = re.search(r'viewBox="([^"]+)"', svg_str)
    viewbox = viewbox_match.group(1) if viewbox_match else "0 0 100 100"
    
    start_tag_end = svg_str.find('>')
    svg_start = svg_str.find('<svg')
    
    if svg_start != -1 and start_tag_end != -1:
        body = svg_str[start_tag_end+1:]
        body = body.replace('</svg>', '')
        return viewbox, body.strip()
    return viewbox, ""

try:
    kai_school = read_file('Kaischoollogo.svg')
    kai_bot = read_file('Kaibotlogo.svg')
    
    kai_school_content = kai_school.replace('fill="#020202"', 'fill="#FFFFFF"')
    kai_school_content = kai_school_content.replace('fill="#010101"', 'fill="#FFFFFF"')
    kai_bot_content = kai_bot.replace('fill="#010101"', 'fill="#FFFFFF"')
    kai_bot_content = kai_bot_content.replace('fill="#020202"', 'fill="#FFFFFF"')
    
    ks_vb, ks_inner = extract_svg_content(kai_school_content)
    kb_vb, kb_inner = extract_svg_content(kai_bot_content)
    
    ks_parts = ks_vb.split()
    kb_parts = kb_vb.split()
    ks_w, ks_h = float(ks_parts[2]), float(ks_parts[3])
    kb_w, kb_h = float(kb_parts[2]), float(kb_parts[3])
    
    ks_ratio = ks_w / ks_h
    kb_ratio = kb_w / kb_h
    
    logo_height = 220
    ks_display_w = int(logo_height * ks_ratio)
    ks_display_h = logo_height
    kb_display_w = int(logo_height * kb_ratio)
    kb_display_h = logo_height
    
    ks_x = int(225 - ks_display_w / 2)
    kb_x = int(675 - kb_display_w / 2)
    
    svg_template = f'''<svg width="900" height="400" viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19" stop-opacity="1"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1" stop-opacity="1"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="1"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softglow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="400" rx="20" fill="url(#bg-grad)" stroke="#1E293B" stroke-width="1"/>

  <!-- Subtle dot grid -->
  <pattern id="dots" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
    <circle cx="15" cy="15" r="0.8" fill="#6366F1" opacity="0.06"/>
  </pattern>
  <rect width="900" height="400" rx="20" fill="url(#dots)"/>

  <!-- Top accent bar -->
  <rect x="0" y="0" width="900" height="3" rx="1.5" fill="url(#accent)" opacity="0.8"/>
  
  <!-- Decorative accent glow behind logos -->
  <ellipse cx="225" cy="160" rx="130" ry="120" fill="#6366F1" opacity="0.03" filter="url(#softglow)"/>
  <ellipse cx="675" cy="160" rx="140" ry="120" fill="#06B6D4" opacity="0.03" filter="url(#softglow)"/>

  <!-- Center divider - subtle vertical line -->
  <line x1="450" y1="80" x2="450" y2="320" stroke="url(#accent)" stroke-width="0.5" opacity="0.15"/>
  
  <!-- Center connecting dot (animated) -->
  <circle cx="450" cy="200" r="5" fill="url(#accent)">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="r" values="5;7;5" dur="3s" repeatCount="indefinite"/>
  </circle>

  <!-- LEFT: KAISCHOOL -->
  <g>
    <!-- Card background -->
    <rect x="{ks_x - 15}" y="48" width="{ks_display_w + 30}" height="{logo_height + 100}" rx="16" fill="#FFFFFF" opacity="0.02" stroke="#6366F1" stroke-width="0.5" stroke-opacity="0.15"/>
    
    <g transform="translate({ks_x}, 68)">
      <animateTransform attributeName="transform" type="translate" values="{ks_x},68; {ks_x},58; {ks_x},68" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      
      <!-- Logo -->
      <svg width="{ks_display_w}" height="{ks_display_h}" viewBox="{ks_vb}" preserveAspectRatio="xMidYMid meet" filter="url(#glow)">
        {ks_inner}
      </svg>
    </g>
    
    <!-- Label -->
    <text x="{ks_x + ks_display_w/2}" y="320" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="700" font-size="20" fill="#E2E8F0" letter-spacing="6">KAISCHOOL</text>
    <text x="{ks_x + ks_display_w/2}" y="342" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="400" font-size="11" fill="#64748B" letter-spacing="3">SCHOOL MANAGEMENT</text>
  </g>

  <!-- RIGHT: KAIBOT -->
  <g>
    <!-- Card background -->
    <rect x="{kb_x - 15}" y="48" width="{kb_display_w + 30}" height="{logo_height + 100}" rx="16" fill="#FFFFFF" opacity="0.02" stroke="#06B6D4" stroke-width="0.5" stroke-opacity="0.15"/>
    
    <g transform="translate({kb_x}, 68)">
      <animateTransform attributeName="transform" type="translate" values="{kb_x},68; {kb_x},78; {kb_x},68" dur="6s" begin="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
      
      <!-- Logo -->
      <svg width="{kb_display_w}" height="{kb_display_h}" viewBox="{kb_vb}" preserveAspectRatio="xMidYMid meet" filter="url(#glow)">
        {kb_inner}
      </svg>
    </g>
    
    <!-- Label -->
    <text x="{kb_x + kb_display_w/2}" y="320" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="700" font-size="20" fill="#E2E8F0" letter-spacing="6">KAIBOT</text>
    <text x="{kb_x + kb_display_w/2}" y="342" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="400" font-size="11" fill="#64748B" letter-spacing="3">AI AGENT</text>
  </g>

</svg>'''
    
    with open('profile-header.svg', 'w') as f:
        f.write(svg_template)
    print("Successfully generated profile-header.svg")

except Exception as e:
    print(f"Error: {e}")
