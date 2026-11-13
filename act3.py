from PIL import Image, ImageDraw, ImageFont
import os

def create_prototype(filename, title, elements):
    # Create a blank white image (Mobile aspect ratio)
    width, height = 400, 800
    img = Image.new('RGB', (width, height), color='#F3F4F6')
    draw = ImageDraw.Draw(img)

    # Draw Phone Bezel
    draw.rectangle([10, 10, width-10, height-10], outline='#333', width=5)

    # Standard Header (Default, can be overridden by navbar element)
    # We only draw this if there isn't a custom navbar defined in elements to avoid overlap
    has_navbar = any(e['type'] == 'navbar' for e in elements)
    if not has_navbar:
        draw.rectangle([10, 10, width-10, 80], fill='#4F46E5')
        draw.text((30, 30), title, fill='white', size=20)

    # Draw UI Elements
    for elem in elements:
        etype = elem['type']
        
        if etype == 'navbar':
            # Custom Navbar
            bbox = elem['box']
            color = elem.get('color', '#4F46E5')
            draw.rectangle(bbox, fill=color)
            
            # Menu Icon (Left - 3 lines)
            mx, my = bbox[0]+20, bbox[1]+20
            draw.line([mx, my, mx+25, my], fill='white', width=3)
            draw.line([mx, my+8, mx+25, my+8], fill='white', width=3)
            draw.line([mx, my+16, mx+25, my+16], fill='white', width=3)
            
            # Title (Center)
            text = elem.get('text', '')
            draw.text((bbox[0]+130, bbox[1]+20), text, fill='white')
            
            # Hint/Option (Right)
            if elem.get('hint'):
                draw.text((bbox[2]-60, bbox[1]+20), "Hint 💡", fill='white')

        elif etype == 'rect':
            bbox = elem['box']
            color = elem.get('color', '#D1D5DB')
            text = elem.get('text', '')
            outline = elem.get('outline', '#6B7280')
            draw.rectangle(bbox, fill=color, outline=outline)
            if text:
                # Text wrapping/positioning (Basic)
                text_x = bbox[0] + 15
                text_y = bbox[1] + (bbox[3]-bbox[1])/2 - 5
                # Handle newlines in text
                if '\n' in text:
                    lines = text.split('\n')
                    draw.text((text_x, bbox[1] + 15), lines[0], fill='#111827')
                    draw.text((text_x, bbox[1] + 35), lines[1], fill='#111827')
                else:
                    draw.text((text_x, text_y), text, fill='#111827')

        elif etype == 'circle':
            bbox = elem['box']
            color = elem.get('color', '#D1D5DB')
            text = elem.get('text', '')
            draw.ellipse(bbox, fill=color, outline='#6B7280')
            if text:
                # Center text in circle
                draw.text((bbox[0]+15, bbox[1]+12), text, fill='white')

        elif etype == 'line':
            coords = elem['coords']
            color = elem.get('color', 'black')
            width_line = elem.get('width', 3)
            draw.line(coords, fill=color, width=width_line)

        elif etype == 'button':
            bbox = elem['box']
            color = elem.get('color', '#F59E0B')
            text = elem.get('text', '')
            draw.rectangle(bbox, fill=color, outline='#B45309')
            draw.text((bbox[0]+20, bbox[1]+15), text, fill='white')
            
        elif etype == 'text':
             xy = elem['xy']
             text = elem['text']
             color = elem.get('color', 'black')
             draw.text(xy, text, fill=color)

    # Save
    img.save(filename)
    print(f"Generated: {filename}")

# --- Screen 1: Gameplay (Connect the Dots) ---
gameplay_ui = [
    # 1. Navbar
    {'type': 'navbar', 'box': [10, 10, 390, 70], 'text': 'Connect Dots', 'hint': True, 'color': '#4F46E5'},
    
    # 2. Top-Middle Current Level
    {'type': 'rect', 'box': [130, 90, 270, 130], 'text': '   Level 5', 'color': '#E0E7FF', 'outline': '#4F46E5'},
    
    # 3. Middle Game Screen
    {'type': 'rect', 'box': [20, 150, 380, 630], 'text': '', 'color': '#FFFFFF', 'outline': '#333'}, 
    
    # Game Elements (Dots and Lines)
    # Connected lines
    {'type': 'line', 'coords': [80, 250, 200, 200], 'color': '#4F46E5', 'width': 4},
    {'type': 'line', 'coords': [200, 200, 320, 250], 'color': '#4F46E5', 'width': 4},
    # Dots (Nodes)
    {'type': 'circle', 'box': [60, 230, 100, 270], 'text': '1', 'color': '#4F46E5'},
    {'type': 'circle', 'box': [180, 180, 220, 220], 'text': '2', 'color': '#4F46E5'},
    {'type': 'circle', 'box': [300, 230, 340, 270], 'text': '3', 'color': '#4F46E5'},
    {'type': 'circle', 'box': [180, 350, 220, 390], 'text': '4', 'color': '#9CA3AF'}, # Next target
    {'type': 'circle', 'box': [180, 500, 220, 540], 'text': '5', 'color': '#9CA3AF'},
    
    # 4. Bottom Screen Options
    {'type': 'rect', 'box': [10, 650, 390, 790], 'text': '', 'color': '#F3F4F6', 'outline': '#F3F4F6'}, # Footer bg
    {'type': 'button', 'box': [30, 700, 120, 750], 'text': 'Reset', 'color': '#EF4444'},
    {'type': 'button', 'box': [140, 700, 260, 750], 'text': 'Hint (3)', 'color': '#F59E0B'},
    {'type': 'button', 'box': [280, 700, 370, 750], 'text': 'Restart', 'color': '#10B981'},
]
create_prototype('proto_1_gameplay.png', 'Gameplay', gameplay_ui)

# --- Screen 2: Level Select (Standard) ---
level_ui = [
    {'type': 'circle', 'box': [160, 150, 240, 230], 'text': '1', 'color': '#10B981'}, 
    {'type': 'circle', 'box': [80, 280, 160, 360], 'text': '2', 'color': '#10B981'},
    {'type': 'circle', 'box': [240, 280, 320, 360], 'text': '3', 'color': '#F59E0B'}, 
    {'type': 'circle', 'box': [160, 410, 240, 490], 'text': '4', 'color': '#9CA3AF'}, 
    {'type': 'rect', 'box': [50, 600, 350, 700], 'text': 'Current Focus: Memory', 'color': '#E0E7FF'}
]
create_prototype('proto_2_levels.png', 'Select Level', level_ui)

# --- Screen 3: Rewards (Standard) ---
reward_ui = [
    {'type': 'rect', 'box': [50, 200, 350, 400], 'text': 'LEVEL COMPLETE!', 'color': '#FEF3C7'},
    {'type': 'circle', 'box': [150, 250, 250, 350], 'text': '★', 'color': '#F59E0B'},
    {'type': 'rect', 'box': [50, 450, 350, 500], 'text': 'Focus Score: 95%', 'color': '#FFFFFF'},
    {'type': 'rect', 'box': [50, 520, 350, 570], 'text': 'Time: 45s', 'color': '#FFFFFF'},
    {'type': 'button', 'box': [100, 650, 300, 700], 'text': 'Next Level >>'}
]
create_prototype('proto_3_reward.png', 'Great Job!', reward_ui)

# --- Screen 4: Dashboard (Better Layout) ---
dashboard_ui = [
    # Header
    {'type': 'navbar', 'box': [10, 10, 390, 70], 'text': 'Parent Dashboard', 'color': '#059669'},
    
    # Stats Row
    {'type': 'rect', 'box': [20, 90, 130, 160], 'text': 'Focus\n  85%', 'color': '#DBEAFE'},
    {'type': 'rect', 'box': [140, 90, 250, 160], 'text': 'Memory\n  72%', 'color': '#D1FAE5'},
    {'type': 'rect', 'box': [260, 90, 370, 160], 'text': 'Time\n 2.5h', 'color': '#FEF3C7'},
    
    # Main Graph
    {'type': 'rect', 'box': [20, 180, 380, 400], 'text': '', 'color': 'white', 'outline': '#9CA3AF'},
    {'type': 'text', 'xy': (30, 190), 'text': 'Weekly Progress', 'color': '#6B7280'},
    # Graph Line
    {'type': 'line', 'coords': [40, 350, 100, 300], 'color': '#4F46E5', 'width': 3},
    {'type': 'line', 'coords': [100, 300, 160, 320], 'color': '#4F46E5', 'width': 3},
    {'type': 'line', 'coords': [160, 320, 220, 250], 'color': '#4F46E5', 'width': 3},
    {'type': 'line', 'coords': [220, 250, 280, 270], 'color': '#4F46E5', 'width': 3},
    {'type': 'line', 'coords': [280, 270, 360, 200], 'color': '#4F46E5', 'width': 3},
    
    # Recent Activity
    {'type': 'text', 'xy': (20, 420), 'text': 'Recent Sessions', 'color': '#333'},
    {'type': 'rect', 'box': [20, 450, 380, 500], 'text': 'Level 5: Completed (3m)', 'color': 'white'},
    {'type': 'rect', 'box': [20, 510, 380, 560], 'text': 'Level 4: Completed (4m)', 'color': 'white'},
    {'type': 'rect', 'box': [20, 570, 380, 620], 'text': 'Level 3: Failed', 'color': '#FEE2E2'},
    
    # Bottom Button
    {'type': 'button', 'box': [80, 700, 320, 750], 'text': 'Export Report', 'color': '#4F46E5'}
]
create_prototype('proto_4_dashboard.png', 'Dashboard', dashboard_ui)