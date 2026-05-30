import os
import re

# ==============================================================================
# 🛠️ EDIT YOUR SKILLS HERE
# ==============================================================================
SKILLS = {
    "active": [
        {"name": "Next.js", "status": "blue_star", "filename": "nextjs.svg"},
        {"name": "TypeScript", "status": "blue_star", "filename": "typescript.svg"},
        {"name": "Tailwind CSS", "status": "blue_star", "filename": "tailwind.svg"},
        {"name": "Shadcn/ui", "status": "blue_star", "filename": "shadcnui.svg"},
        {"name": "Convex", "status": "purple_star", "filename": "convex.svg"},
        {"name": "Node.js", "status": "green_star", "filename": "nodejs.svg"},
        {"name": "Python", "status": "purple_star", "filename": "python.svg"},
        {"name": "Docker", "status": "red_star", "filename": "docker.svg"},
        {"name": "React Native", "status": "purple_star", "filename": "reactnative.svg"},
        {"name": "SQL DB", "status": "green_star", "filename": "sqldb.svg"},
        {"name": "NoSQL DB", "status": "green_star", "filename": "nosqldb.svg"},
        {"name": "Linux", "status": "gray_star", "filename": "linux.svg"},
        {"name": "Git", "status": "yellow_star", "filename": "git.svg"},
    ],
    "secondary": [
        {"name": "C#", "status": "archived", "filename": "csharp.svg"},
        {"name": "Java", "status": "archived", "filename": "java.svg"},
        {"name": "Kubernetes", "status": "archived", "filename": "kubernetes.svg"},
        {"name": "Arduino/ESP32", "status": "archived", "filename": "arduino.svg"},
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

STATUS_CONFIG = {
    "blue_star": {
        "color": "#0088ff",
        "icon": "star"
    },
    "red_star": {
        "color": "#ff2a2a",
        "icon": "star"
    },
    "purple_star": {
        "color": "#b624ff",
        "icon": "star"
    },
    "gray_star": {
        "color": "#888888",
        "icon": "star"
    },
    "green_star": {
        "color": "#00cc66",
        "icon": "star"
    },
    "yellow_star": {
        "color": "#ffcc00",
        "icon": "star"
    },
    "archived": {
        "color": "#d29054",  # Cardboard brown
        "icon": "box"
    }
}

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

def create_svg(tech_name, status, icons_dir, output_path):
    config = STATUS_CONFIG.get(status)
    if not config:
        print(f"Error: Status {status} not found for {tech_name}")
        return
        
    color = config["color"]
    icon_type = config["icon"]
    
    if icon_type == "star":
        status_icon_svg = f'<path d="{STAR_PATH}" fill="{color}"/>'
    else:
        status_icon_svg = f'''<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M3.27 6.96L12 12.01l8.73-5.05" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 22.08V12" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'''
        
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
  <!-- Background Card -->
  <rect width="300" height="40" rx="8" fill="#0d0d0f" stroke="{color}" stroke-width="1.5"/>
  
{icon_element}
  
  <!-- Tech Name -->
  <text x="42" y="24" fill="#ffffff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">{tech_name}</text>
  
  <!-- Status Icon -->
  <svg x="268" y="10" width="20" height="20" viewBox="0 0 24 24">
    {status_icon_svg}
  </svg>
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
    
    print("Generating skill badges with technology icons & star status...")
    for skill in SKILLS["active"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["status"], icons_dir, path)
        print(f"  [Active]    {skill['name']} ({skill['status']}) -> {skill['filename']}")
        
    for skill in SKILLS["secondary"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["status"], icons_dir, path)
        print(f"  [Secondary] {skill['name']} ({skill['status']}) -> {skill['filename']}")
        
    print("\nGeneration complete! SVGs saved in assets/skills/")
