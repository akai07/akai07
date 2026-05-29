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
    
    ks_vb, ks_inner = extract_svg_content(kai_school)
    kb_vb, kb_inner = extract_svg_content(kai_bot)
    
    ks_parts = ks_vb.split()
    kb_parts = kb_vb.split()
    ks_w, ks_h = float(ks_parts[2]), float(ks_parts[3])
    kb_w, kb_h = float(kb_parts[2]), float(kb_parts[3])
    
    logo_size = 200
    ks_scale = logo_size / max(ks_w, ks_h)
    kb_scale = logo_size / max(kb_w, kb_h)
    ks_display_w = int(ks_w * ks_scale)
    ks_display_h = int(ks_h * ks_scale)
    kb_display_w = int(kb_w * kb_scale)
    kb_display_h = int(kb_h * kb_scale)
    
    badge_radius = 155
    ks_x = int(225 - ks_display_w / 2)
    kb_x = int(675 - kb_display_w / 2)
    
    svg_template = f'''<svg width="900" height="420" viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19" stop-opacity="1"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1" stop-opacity="1"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="badge-ks" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A1B2E" stop-opacity="1"/>
      <stop offset="100%" stop-color="#2D2F4A" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="badge-kb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F2027" stop-opacity="1"/>
      <stop offset="100%" stop-color="#1A3A47" stop-opacity="1"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="badgeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="900" height="420" rx="20" fill="url(#bg-grad)" stroke="#1E293B" stroke-width="1"/>

  <pattern id="dots" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
    <circle cx="15" cy="15" r="0.8" fill="#6366F1" opacity="0.06"/>
  </pattern>
  <rect width="900" height="420" rx="20" fill="url(#dots)"/>

  <rect x="0" y="0" width="900" height="3" rx="1.5" fill="url(#accent)" opacity="0.8"/>

  <ellipse cx="225" cy="160" rx="100" ry="100" fill="#6366F1" opacity="0.04" filter="url(#badgeGlow)"/>
  <ellipse cx="675" cy="160" rx="100" ry="100" fill="#06B6D4" opacity="0.04" filter="url(#badgeGlow)"/>

  <line x1="450" y1="50" x2="450" y2="270" stroke="url(#accent)" stroke-width="0.5" opacity="0.15"/>

  <circle cx="450" cy="160" r="5" fill="url(#accent)">
    <animate attributeName="opacity" values="0.2;1;0.2" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="r" values="5;8;5" dur="3s" repeatCount="indefinite"/>
  </circle>

  <g>
    <circle cx="225" cy="160" r="{badge_radius}" fill="url(#badge-ks)" stroke="#6366F1" stroke-width="1" stroke-opacity="0.3"/>
    <circle cx="225" cy="160" r="{badge_radius}" fill="none" stroke="#6366F1" stroke-width="2" stroke-opacity="0.1" filter="url(#glow)"/>

    <g transform="translate({ks_x}, {int(160 - ks_display_h/2)})">
      <animateTransform attributeName="transform" type="translate" values="{ks_x},{int(160 - ks_display_h/2)}; {ks_x},{int(150 - ks_display_h/2)}; {ks_x},{int(160 - ks_display_h/2)}" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>

      <svg width="{ks_display_w}" height="{ks_display_h}" viewBox="{ks_vb}" preserveAspectRatio="xMidYMid meet">
        {ks_inner}
      </svg>
    </g>

    <text x="225" y="340" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="700" font-size="20" fill="#E2E8F0" letter-spacing="6">KAISCHOOL</text>
    <text x="225" y="360" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="400" font-size="11" fill="#64748B" letter-spacing="3">SCHOOL MANAGEMENT</text>
  </g>

  <g>
    <circle cx="675" cy="160" r="{badge_radius}" fill="url(#badge-kb)" stroke="#06B6D4" stroke-width="1" stroke-opacity="0.3"/>
    <circle cx="675" cy="160" r="{badge_radius}" fill="none" stroke="#06B6D4" stroke-width="2" stroke-opacity="0.1" filter="url(#glow)"/>

    <g transform="translate({kb_x}, {int(160 - kb_display_h/2)})">
      <animateTransform attributeName="transform" type="translate" values="{kb_x},{int(160 - kb_display_h/2)}; {kb_x},{int(170 - kb_display_h/2)}; {kb_x},{int(160 - kb_display_h/2)}" dur="6s" begin="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>

      <svg width="{kb_display_w}" height="{kb_display_h}" viewBox="{kb_vb}" preserveAspectRatio="xMidYMid meet">
        {kb_inner}
      </svg>
    </g>

    <text x="675" y="340" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="700" font-size="20" fill="#E2E8F0" letter-spacing="6">KAIBOT</text>
    <text x="675" y="360" text-anchor="middle" font-family="'Inter', 'Segoe UI', -apple-system, sans-serif" font-weight="400" font-size="11" fill="#64748B" letter-spacing="3">AI AGENT</text>
  </g>

</svg>'''
    
    with open('profile-header.svg', 'w') as f:
        f.write(svg_template)
    print("Successfully generated profile-header.svg")

except Exception as e:
    print(f"Error: {e}")
