import os
import re
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "assets", "skills.json")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        SKILLS = json.load(f)
except Exception as e:
    print(f"Error loading skills.json: {e}")
    SKILLS = {"active": [], "secondary": []}

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

STATUS_MAPPING = {
    "constant": {"color": "#0088ff", "icon": "star"},
    "favorite": {"color": "#ff2a2a", "icon": "star"},
    "learning": {"color": "#b624ff", "icon": "star"},
    "touched": {"color": "#888888", "icon": "star"},
    "implemented": {"color": "#00cc66", "icon": "star"},
    "deep experience": {"color": "#ffcc00", "icon": "star"},
    "archived": {"color": "#d29054", "icon": "box"},
}

ORDERED_STATUS_KEYS = [
    "constant",
    "favorite",
    "learning",
    "implemented",
    "deep experience",
    "touched",
    "archived"
]

STAR_PATH = "M12 .587l3.668 7.431 8.2 1.192-5.934 5.784 1.4 8.168L12 18.896l-7.334 3.857 1.4-8.168L.132 9.21l8.2-1.192z"

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

def create_svg(tech_name, indicators, icons_dir, output_path):
    # Border color is the first active indicator's color, or default dark gray
    border_color = indicators[0].get("color", "#333336") if indicators else "#333336"
    
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
        
    # Render all active indicators from right to left
    status_icons_svg = []
    for i, ind in enumerate(indicators):
        color = ind.get("color", "#888888")
        icon_type = ind.get("type", "star")
        
        # Position from right to left: 268, 246, 224, 202, ...
        x_pos = 268 - (i * 22)
        
        if icon_type == "star":
            path_svg = f'<path d="{STAR_PATH}" fill="{color}"/>'
        else:
            path_svg = f'''<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M3.27 6.96L12 12.01l8.73-5.05" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 22.08V12" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'''
            
        status_icons_svg.append(f"""  <!-- Status Icon {i} ({icon_type}) -->
  <svg x="{x_pos}" y="10" width="20" height="20" viewBox="0 0 24 24">
    {path_svg}
  </svg>""")
        
    status_elements = "\n".join(status_icons_svg)
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" height="40" viewBox="0 0 300 40">
  <!-- Background Card -->
  <rect width="300" height="40" rx="8" fill="#0d0d0f" stroke="{border_color}" stroke-width="1.5"/>
  
{icon_element}
  
  <!-- Tech Name -->
  <text x="42" y="24" fill="#ffffff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">{tech_name}</text>
  
{status_elements}
</svg>
"""
    # Ensure folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def process_skill(skill, output_dir, icons_dir):
    path = os.path.join(output_dir, skill["filename"])
    
    status_data = skill.get("status", {})
    indicators = []
    
    # Handle dict status
    if isinstance(status_data, dict):
        # Normalize keys to lowercase and strip whitespace
        normalized_status = {k.lower().strip(): v for k, v in status_data.items()}
        
        # Build indicators in defined priority order
        for key in ORDERED_STATUS_KEYS:
            if normalized_status.get(key) is True:
                config = STATUS_MAPPING.get(key)
                if config:
                    indicators.append({
                        "type": config["icon"],
                        "color": config["color"]
                    })
    # Fallback to string status
    elif isinstance(status_data, str):
        normalized_str = status_data.lower().strip()
        # Direct lookup or map from configuration
        config = STATUS_MAPPING.get(normalized_str)
        if config:
            indicators.append({
                "type": config["icon"],
                "color": config["color"]
            })
            
    create_svg(skill["name"], indicators, icons_dir, path)

if __name__ == "__main__":
    output_dir = os.path.join(script_dir, "assets", "skills")
    icons_dir = os.path.join(script_dir, "assets", "technology_icons")
    
    print("Generating skill badges with technology icons & customizable status configurations...")
    for skill in SKILLS["active"]:
        process_skill(skill, output_dir, icons_dir)
        print(f"  [Active]    {skill['name']} -> {skill['filename']}")
        
    for skill in SKILLS["secondary"]:
        process_skill(skill, output_dir, icons_dir)
        print(f"  [Secondary] {skill['name']} -> {skill['filename']}")
        
    print("\nGeneration complete! SVGs saved in assets/skills/")
