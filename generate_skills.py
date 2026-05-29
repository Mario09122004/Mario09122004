import os

# ==============================================================================
# 🛠️ EDIT YOUR SKILLS HERE
# You can change the percentages, add new skills, or change titles.
# ==============================================================================
SKILLS = {
    # Active Tech Stack (will be styled with bright neon orange gradients)
    "active": [
        {"name": "Next.js", "proficiency": 95, "filename": "nextjs.svg"},
        {"name": "TypeScript", "proficiency": 90, "filename": "typescript.svg"},
        {"name": "Tailwind CSS", "proficiency": 90, "filename": "tailwind.svg"},
        {"name": "Shadcn/ui", "proficiency": 85, "filename": "shadcnui.svg"},
        {"name": "Convex", "proficiency": 80, "filename": "convex.svg"},
        {"name": "Node.js", "proficiency": 85, "filename": "nodejs.svg"},
        {"name": "Python", "proficiency": 75, "filename": "python.svg"},
        {"name": "Docker", "proficiency": 80, "filename": "docker.svg"},
    ],
    # Secondary Tech Stack (will be styled with slate gray borders and gradients)
    "secondary": [
        {"name": "C#", "proficiency": 50, "filename": "csharp.svg"},
        {"name": "Java", "proficiency": 45, "filename": "java.svg"},
    ]
}
# ==============================================================================

def create_svg(tech_name, proficiency, is_active, output_path):
    track_width = 110
    fill_width = int(track_width * (proficiency / 100.0))
    
    if is_active:
        border_color = "#ff4a00"
        fill_color = "url(#orangeGrad)"
        text_color = "#ff4a00"
    else:
        border_color = "#4b5563"  # gray-600
        fill_color = "url(#grayGrad)"
        text_color = "#9ca3af"  # gray-400
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="40" viewBox="0 0 300 40">
  <defs>
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff3e00" />
      <stop offset="100%" stop-color="#ff7300" />
    </linearGradient>
    <linearGradient id="grayGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4b5563" />
      <stop offset="100%" stop-color="#6b7280" />
    </linearGradient>
  </defs>
  <!-- Background Card -->
  <rect width="300" height="40" rx="8" fill="#0d0d0f" stroke="{border_color}" stroke-width="1.5"/>
  
  <!-- Tech Name -->
  <text x="15" y="24" fill="#ffffff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">{tech_name}</text>
  
  <!-- Progress Bar Track -->
  <rect x="130" y="16" width="{track_width}" height="8" rx="4" fill="#1f1f23"/>
  
  <!-- Progress Bar Fill -->
  <rect x="130" y="16" width="{fill_width}" height="8" rx="4" fill="{fill_color}"/>
  
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
    
    print("Generating skill badges...")
    for skill in SKILLS["active"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["proficiency"], True, path)
        print(f"  [Active]    {skill['name']} ({skill['proficiency']}%) -> {skill['filename']}")
        
    for skill in SKILLS["secondary"]:
        path = os.path.join(output_dir, skill["filename"])
        create_svg(skill["name"], skill["proficiency"], False, path)
        print(f"  [Secondary] {skill['name']} ({skill['proficiency']}%) -> {skill['filename']}")
        
    print("\nGeneration complete! SVGs saved in assets/skills/")
