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
        
        elif etype == 'toggle':
            bbox = elem['box']
            state = elem.get('state', False)
            draw.rectangle(bbox, fill='#E5E7EB', outline='#9CA3AF')
            if state:
                # Draw 'On' circle
                draw.ellipse([bbox[2]-25, bbox[1]+2, bbox[2]-5, bbox[3]-2], fill='#10B981')
            else:
                 # Draw 'Off' circle
                draw.ellipse([bbox[0]+5, bbox[1]+2, bbox[0]+25, bbox[3]-2], fill='#9CA3AF')

    # Save
    img.save(filename)
    print(f"Generated: {filename}")

# --- Screen 6: Memory Match Gameplay ---
memory_ui = [
    # 1. Navbar
    {'type': 'navbar', 'box': [10, 10, 390, 70], 'text': 'Memory Match', 'color': '#F59E0B'},
    
    # 2. Stats Bar
    {'type': 'rect', 'box': [20, 85, 190, 125], 'text': 'Matches: 2/6', 'color': 'white', 'outline': '#F59E0B'},
    {'type': 'rect', 'box': [210, 85, 380, 125], 'text': 'Moves: 8', 'color': 'white', 'outline': '#F59E0B'},

    # 3. Card Grid (4x3)
    # Row 1
    {'type': 'rect', 'box': [40, 150, 110, 240], 'text': '🍎', 'color': 'white', 'outline': '#D1D5DB'}, # Face Up
    {'type': 'rect', 'box': [120, 150, 190, 240], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'}, # Face Down
    {'type': 'rect', 'box': [200, 150, 270, 240], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    {'type': 'rect', 'box': [280, 150, 350, 240], 'text': '🍎', 'color': 'white', 'outline': '#10B981'}, # Face Up (Matched)

    # Row 2
    {'type': 'rect', 'box': [40, 260, 110, 350], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    {'type': 'rect', 'box': [120, 260, 190, 350], 'text': '🚗', 'color': 'white', 'outline': '#D1D5DB'},
    {'type': 'rect', 'box': [200, 260, 270, 350], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    {'type': 'rect', 'box': [280, 260, 350, 350], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},

    # Row 3
    {'type': 'rect', 'box': [40, 370, 110, 460], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    {'type': 'rect', 'box': [120, 370, 190, 460], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    {'type': 'rect', 'box': [200, 370, 270, 460], 'text': '🐶', 'color': 'white', 'outline': '#D1D5DB'},
    {'type': 'rect', 'box': [280, 370, 350, 460], 'text': '', 'color': '#F59E0B', 'outline': '#B45309'},
    
    # 4. Feedback Text
    {'type': 'text', 'xy': (120, 500), 'text': 'Find the matching pair!', 'color': '#6B7280'},

    # 5. Bottom Controls
    {'type': 'rect', 'box': [10, 650, 390, 790], 'text': '', 'color': '#F3F4F6', 'outline': '#F3F4F6'},
    {'type': 'button', 'box': [30, 700, 150, 750], 'text': 'Pause', 'color': '#6B7280'},
    {'type': 'button', 'box': [170, 700, 370, 750], 'text': 'Peek Hint (2)', 'color': '#4F46E5'},
]

create_prototype('proto_6_memory.png', 'Memory Game', memory_ui)

# --- Screen 7: Settings & Accessibility ---
settings_ui = [
    # 1. Navbar
    {'type': 'navbar', 'box': [10, 10, 390, 70], 'text': 'Settings', 'color': '#374151'},
    
    # 2. Sensory Profile
    {'type': 'text', 'xy': (20, 90), 'text': 'SENSORY PROFILE', 'color': '#6B7280'},
    {'type': 'rect', 'box': [20, 110, 380, 170], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'text', 'xy': (35, 135), 'text': 'Background Music', 'color': '#111827'},
    {'type': 'toggle', 'box': [310, 125, 360, 155], 'state': False}, # Off by default for sensory friendly

    {'type': 'rect', 'box': [20, 180, 380, 240], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'text', 'xy': (35, 205), 'text': 'Sound Effects', 'color': '#111827'},
    {'type': 'toggle', 'box': [310, 195, 360, 225], 'state': True},

    # 3. Visual Accessibility
    {'type': 'text', 'xy': (20, 260), 'text': 'VISUAL ACCESSIBILITY', 'color': '#6B7280'},
    {'type': 'rect', 'box': [20, 280, 380, 340], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'text', 'xy': (35, 305), 'text': 'Color Blind Mode', 'color': '#111827'},
    {'type': 'toggle', 'box': [310, 295, 360, 325], 'state': False},

    {'type': 'rect', 'box': [20, 350, 380, 410], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'text', 'xy': (35, 375), 'text': 'High Contrast', 'color': '#111827'},
    {'type': 'toggle', 'box': [310, 365, 360, 395], 'state': True},

    # 4. Difficulty
    {'type': 'text', 'xy': (20, 430), 'text': 'GAMEPLAY', 'color': '#6B7280'},
    {'type': 'rect', 'box': [20, 450, 380, 510], 'text': '', 'color': 'white', 'outline': '#E5E7EB'},
    {'type': 'text', 'xy': (35, 475), 'text': 'Adaptive Difficulty', 'color': '#111827'},
    {'type': 'toggle', 'box': [310, 465, 360, 495], 'state': True},

    # 5. Save Button
    {'type': 'button', 'box': [20, 700, 380, 750], 'text': 'Save Preferences', 'color': '#10B981'},
]

create_prototype('proto_7_settings.png', 'Settings', settings_ui)