import os
import re

# ==============================================================================
# 🛠️ EDIT YOUR SKILLS HERE
# You can change the percentages, add new skills, or change titles.
# ==============================================================================
SKILLS = {
    # Active Tech Stack (will be styled with bright neon orange gradients)
    "active": [
        {"name": "Next.js", "proficiency": 60, "filename": "nextjs.svg"},
        {"name": "TypeScript", "proficiency": 60, "filename": "typescript.svg"},
        {"name": "Tailwind CSS", "proficiency": 40, "filename": "tailwind.svg"},
        {"name": "Shadcn/ui", "proficiency": 80, "filename": "shadcnui.svg"},
        {"name": "Convex", "proficiency": 50, "filename": "convex.svg"},
        {"name": "Node.js", "proficiency": 35, "filename": "nodejs.svg"},
        {"name": "Python", "proficiency": 35, "filename": "python.svg"},
        {"name": "Docker", "proficiency": 60, "filename": "docker.svg"},
        {"name": "React Native", "proficiency": 50, "filename": "reactnative.svg"},
        {"name": "SQL DB", "proficiency": 60, "filename": "sqldb.svg"},
        {"name": "NoSQL DB", "proficiency": 50, "filename": "nosqldb.svg"},
        {"name": "Linux", "proficiency": 35, "filename": "linux.svg"},
        {"name": "Git", "proficiency": 70, "filename": "git.svg"},
    ],
    # Secondary Tech Stack (will be styled with slate gray borders and gradients)
    "secondary": [
        {"name": "C#", "proficiency": 10, "filename": "csharp.svg"},
        {"name": "Java", "proficiency": 5, "filename": "java.svg"},
        {"name": "Kubernetes", "proficiency": 30, "filename": "kubernetes.svg"},
        {"name": "Arduino/ESP32", "proficiency": 30, "filename": "arduino.svg"},
    ]
}

ICON_MAPPING = {
    "Next.js": "nextjs_icon_dark.svg",
    "TypeScript": "typescript.svg",
    "Tailwind CSS": "tailwindcss.svg",
    "Shadcn/ui": "shadcn-ui_dark.svg",
    "Convex": "convex.svg",
    "Node.js": "nodejs.svg",
    "Python": "python.svg",
    "Docker": "docker.svg",
    "React Native": "react_dark.svg",
    "SQL DB": "postgresql.svg",
    "NoSQL DB": "mongodb-icon-dark.svg",
    "Linux": "linux.svg",
    "Git": "git.svg",
    "C#": "csharp.svg",
    "Java": "java.svg",
    "Kubernetes": "kubernetes.svg",
    "Arduino/ESP32": "arduino.svg"
}
# ==============================================================================

def get_icon_svg(tech_name, icons_dir):
    filename = ICON_MAPPING.get(tech_name)
    if not filename:
        return ""
    
    icon_path = os.path.join(icons_dir, filename)
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file not found for {tech_name} at {icon_path}")
        return ""
        
    try:
        with open(icon_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        viewbox_match = re.search(r'viewBox=["\']([^"\']+)["\']', content)
        viewbox = viewbox_match.group(1) if viewbox_match else "0 0 24 24"
        
        svg_start = content.find('<svg')
        if svg_start == -1:
            return ""
        start_tag_end = content.find('>', svg_start)
        end_tag_start = content.rfind('</svg>')
        if start_tag_end == -1 or end_tag_start == -1:
            return ""
            
        inner_content = content[start_tag_end+1:end_tag_start].strip()
        return f'<svg x="12" y="10" width="20" height="20" viewBox="{viewbox}">{inner_content}</svg>'
    except Exception as e:
        print(f"Error reading icon for {tech_name}: {e}")
        return ""

def create_svg(tech_name, proficiency, is_active, icons_dir, output_path):
    track_width = 95
    fill_width = int(track_width * (proficiency / 100.0))
    
    if is_active:
        border_color = "#ff4a00"
        fill_color = "url(#orangeGrad)"
        text_color = "#ff4a00"
    else:
        border_color = "#4b5563"  # gray-600
        fill_color = "url(#grayGrad)"
        text_color = "#9ca3af"  # gray-400
        
    icon_svg = get_icon_svg(tech_name, icons_dir)
    
    if icon_svg:
        # Next.js and Shadcn/ui are white logos, so they need a dark background circle to be visible.
        # Other logos stand out beautifully on a white background circle.
        if tech_name in ["Next.js", "Shadcn/ui"]:
            circle_fill = "#1a1a1e"
        else:
            circle_fill = "#ffffff"
            
        icon_element = f"""  <!-- Background Circle for Icon -->
  <circle cx="22" cy="20" r="12" fill="{circle_fill}"/>
  {icon_svg}"""
    else:
        icon_element = ""
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" height="40" viewBox="0 0 300 40">
  <defs>
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff3e00" />
      <stop offset="100%" stop-color="#ff7300" />
    </linearGradient>
    <linearGradient id="grayGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4b5563" />
      <stop offset="100%" stop-color="#6b7280" />
    </linearGradient>
    <filter id="grayscale">
      <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0
                                           0.33 0.33 0.33 0 0
                                           0.33 0.33 0.33 0 0
                                           0    0    0    1 0"/>
    </filter>
  </defs>
  <!-- Background Card -->
  <rect width="300" height="40" rx="8" fill="#0d0d0f" stroke="{border_color}" stroke-width="1.5"/>
  
{icon_element}
  
  <!-- Tech Name -->
  <text x="42" y="24" fill="#ffffff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">{tech_name}</text>
  
  <!-- Progress Bar Track -->
  <rect x="145" y="16" width="{track_width}" height="8" rx="4" fill="#1f1f23"/>
  
  <!-- Progress Bar Fill -->
  <rect x="145" y="16" width="{fill_width}" height="8" rx="4" fill="{fill_color}"/>
  
  <!-- Percentage Text -->
  <text x="252" y="24" fill="{text_color}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="12" font-weight="bold">{proficiency}%</text>
</svg>
"""
    # Ensure folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == "__main__":
    # Resolve paths relative to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "assets", "skills")
    icons_dir = os.path.join(script_dir, "assets", "technology_icons")
    
    print("Generating skill badges with technology icons...")
    for skill in SKILLS["active"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["proficiency"], True, icons_dir, path)
        print(f"  [Active]    {skill['name']} ({skill['proficiency']}%) -> {skill['filename']}")
        
    for skill in SKILLS["secondary"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["proficiency"], False, icons_dir, path)
        print(f"  [Secondary] {skill['name']} ({skill['proficiency']}%) -> {skill['filename']}")
        
    print("\nGeneration complete! SVGs saved in assets/skills/")
