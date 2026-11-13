from PIL import Image, ImageDraw, ImageFont
import os

def create_prototype(filename, title, elements):
    # Create a blank white image (Mobile aspect ratio)
    width, height = 400, 800
    img = Image.new('RGB', (width, height), color='#F9FAFB') # Slightly lighter gray bg
    draw = ImageDraw.Draw(img)

    # Draw Phone Bezel
    draw.rectangle([10, 10, width-10, height-10], outline='#333', width=5)

    # Draw UI Elements
    for elem in elements:
        etype = elem['type']
        
        if etype == 'navbar':
            bbox = elem['box']
            color = elem.get('color', '#4F46E5')
            draw.rectangle(bbox, fill=color)
            # Menu Icon
            mx, my = bbox[0]+20, bbox[1]+20
            draw.line([mx, my, mx+25, my], fill='white', width=3)
            draw.line([mx, my+8, mx+25, my+8], fill='white', width=3)
            draw.line([mx, my+16, mx+25, my+16], fill='white', width=3)
            # Title
            text = elem.get('text', '')
            draw.text((bbox[0]+140, bbox[1]+20), text, fill='white')

        elif etype == 'rect':
            bbox = elem['box']
            color = elem.get('color', '#D1D5DB')
            text = elem.get('text', '')
            outline = elem.get('outline', '#6B7280')
            draw.rectangle(bbox, fill=color, outline=outline)
            if text:
                # Basic text centering/placement logic
                text_x = bbox[0] + 10
                text_y = bbox[1] + (bbox[3]-bbox[1])/2 - 5
                draw.text((text_x, text_y), text, fill='#111827')

        elif etype == 'circle':
            bbox = elem['box']
            color = elem.get('color', '#D1D5DB')
            text = elem.get('text', '')
            draw.ellipse(bbox, fill=color, outline=color)
            if text:
                draw.text((bbox[0]+20, bbox[1]+15), text, fill='white')

        elif etype == 'button':
            bbox = elem['box']
            color = elem.get('color', '#F59E0B')
            text = elem.get('text', '')
            draw.rectangle(bbox, fill=color, outline=color)
            draw.text((bbox[0]+25, bbox[1]+12), text, fill='white')
            
        elif etype == 'text':
             xy = elem['xy']
             text = elem['text']
             color = elem.get('color', 'black')
             draw.text(xy, text, fill=color)

    # Save
    img.save(filename)
    print(f"Generated: {filename}")

# --- Screen 5: Home / Game Selection ---
home_ui = [
    # 1. Header / Navbar
    {'type': 'navbar', 'box': [10, 10, 390, 70], 'text': 'NeuroQuest', 'color': '#4F46E5'},
    
    # 2. Welcome Section
    {'type': 'text', 'xy': (20, 90), 'text': 'Welcome back! 🚀', 'color': '#111827'},
    {'type': 'text', 'xy': (20, 115), 'text': 'Ready to train your brain?', 'color': '#6B7280'},
    
    # 3. Game List
    # Game Card 1: Connect Dots
    {'type': 'rect', 'box': [20, 150, 380, 270], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    # Left colored strip
    {'type': 'rect', 'box': [20, 150, 130, 270], 'text': '', 'color': '#E0E7FF', 'outline': '#E0E7FF'},
    {'type': 'circle', 'box': [45, 180, 105, 240], 'text': '☍', 'color': '#4F46E5'},
    # Text Details
    {'type': 'text', 'xy': (145, 170), 'text': 'Connect Dots', 'color': '#111827'},
    {'type': 'text', 'xy': (145, 195), 'text': 'Skill: Focus & Motor', 'color': '#6B7280'},
    {'type': 'button', 'box': [280, 215, 360, 255], 'text': 'Play', 'color': '#4F46E5'},

    # Game Card 2: Memory Match
    {'type': 'rect', 'box': [20, 290, 380, 410], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'rect', 'box': [20, 290, 130, 410], 'text': '', 'color': '#FEF3C7', 'outline': '#FEF3C7'},
    {'type': 'rect', 'box': [45, 320, 105, 380], 'text': ' ? ', 'color': '#F59E0B', 'outline': '#F59E0B'},
    {'type': 'text', 'xy': (145, 310), 'text': 'Memory Match', 'color': '#111827'},
    {'type': 'text', 'xy': (145, 335), 'text': 'Skill: Recall', 'color': '#6B7280'},
    {'type': 'button', 'box': [280, 355, 360, 395], 'text': 'Play', 'color': '#F59E0B'},

    # Game Card 3: Pattern Logic
    {'type': 'rect', 'box': [20, 430, 380, 550], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'rect', 'box': [20, 430, 130, 550], 'text': '', 'color': '#D1FAE5', 'outline': '#D1FAE5'},
    {'type': 'circle', 'box': [45, 460, 105, 520], 'text': 'ABC', 'color': '#10B981'},
    {'type': 'text', 'xy': (145, 450), 'text': 'Sequence', 'color': '#111827'},
    {'type': 'text', 'xy': (145, 475), 'text': 'Skill: Logic', 'color': '#6B7280'},
    {'type': 'button', 'box': [280, 495, 360, 535], 'text': 'Play', 'color': '#10B981'},

    # 4. Bottom Navigation Bar
    {'type': 'rect', 'box': [10, 710, 390, 790], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    # Home Icon
    {'type': 'text', 'xy': (60, 735), 'text': '🏠\nHome', 'color': '#4F46E5'},
    # Stats Icon
    {'type': 'text', 'xy': (180, 735), 'text': '📊\nStats', 'color': '#9CA3AF'},
    # Settings Icon
    {'type': 'text', 'xy': (300, 735), 'text': '⚙️\nSettings', 'color': '#9CA3AF'},
]

create_prototype('proto_5_home.png', 'Home Screen', home_ui)