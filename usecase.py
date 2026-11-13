from PIL import Image, ImageDraw, ImageFont
import math

# REPLACEMENT SCRIPT:
# This script now uses Pillow (PIL) instead of Graphviz.
# It allows us to manually draw the diagram with perfect alignment 
# and NO external software requirements.

def create_use_case_diagram():
    # Canvas Settings - Increased height for more use cases
    width, height = 1000, 850
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Load Fonts
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        title_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # --- DRAWING FUNCTIONS ---

    def draw_actor(x, y, label):
        # Draw Stick Figure
        # Head
        draw.ellipse((x-15, y-50, x+15, y-20), outline="black", width=2)
        # Body
        draw.line((x, y-20, x, y+20), fill="black", width=2)
        # Arms
        draw.line((x-20, y-10, x+20, y-10), fill="black", width=2)
        # Legs
        draw.line((x, y+20, x-15, y+50), fill="black", width=2)
        draw.line((x, y+20, x+15, y+50), fill="black", width=2)
        
        # Label
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text((x - text_w/2, y+55), label, fill="black", font=font)
        return (x, y)

    def draw_usecase(x, y, label):
        w, h = 190, 50
        bbox = [x - w/2, y - h/2, x + w/2, y + h/2]
        draw.ellipse(bbox, outline="black", width=2, fill="white")
        
        # Center Text
        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        draw.text((x - text_w/2, y - text_h/2 - 2), label, fill="black", font=font)
        return (x, y, w, h) # Return center and dimensions

    def draw_arrow(start, end, label=None, dashed=False):
        # Draw Line
        if dashed:
            total_len = math.hypot(end[0]-start[0], end[1]-start[1])
            step = 10
            for i in range(0, int(total_len), step*2):
                t1 = i / total_len
                t2 = min((i+step) / total_len, 1.0)
                x1 = start[0] + (end[0]-start[0])*t1
                y1 = start[1] + (end[1]-start[1])*t1
                x2 = start[0] + (end[0]-start[0])*t2
                y2 = start[1] + (end[1]-start[1])*t2
                draw.line((x1, y1, x2, y2), fill="black", width=1)
        else:
            draw.line(start + end, fill="black", width=2)

        # Draw Arrowhead
        angle = math.atan2(end[1]-start[1], end[0]-start[0])
        arrow_len = 10
        x_arrow1 = end[0] - arrow_len * math.cos(angle - math.pi/6)
        y_arrow1 = end[1] - arrow_len * math.sin(angle - math.pi/6)
        x_arrow2 = end[0] - arrow_len * math.cos(angle + math.pi/6)
        y_arrow2 = end[1] - arrow_len * math.sin(angle + math.pi/6)
        draw.polygon([end, (x_arrow1, y_arrow1), (x_arrow2, y_arrow2)], fill="black")

        # Draw Label with White Background
        if label:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            lbl_bbox = draw.textbbox((0, 0), label, font=small_font)
            lbl_w = lbl_bbox[2] - lbl_bbox[0] + 10
            lbl_h = lbl_bbox[3] - lbl_bbox[1] + 6
            
            draw.rectangle(
                [mid_x - lbl_w/2, mid_y - lbl_h/2, mid_x + lbl_w/2, mid_y + lbl_h/2], 
                fill="white"
            )
            draw.text((mid_x - lbl_w/2 + 5, mid_y - lbl_h/2 + 2), label, fill="#333", font=small_font)

    # --- LAYOUT & RENDERING ---

    # 1. System Boundary
    sys_x1, sys_y1 = 280, 50
    sys_x2, sys_y2 = 720, 800
    draw.rectangle([sys_x1, sys_y1, sys_x2, sys_y2], outline="black", width=3)
    draw.text((sys_x1 + 20, sys_y1 + 10), "NeuroQuest: Adaptive Puzzle System", fill="black", font=title_font)

    # 2. Actors
    player = draw_actor(140, 350, "Child Player")
    parent = draw_actor(860, 250, "Parent/Guardian")
    ai = draw_actor(860, 600, "Adaptive AI System")

    # 3. Use Cases (Specific to Project Modules)
    uc_home = draw_usecase(500, 100, "Choose Puzzle Type")
    uc_play = draw_usecase(420, 220, "Play Puzzle Game")
    uc_interact = draw_usecase(580, 220, "Interact (Drag/Tap)")
    uc_reward = draw_usecase(500, 320, "Receive Rewards")
    
    uc_analytics = draw_usecase(500, 420, "View Child's Progress")
    uc_export = draw_usecase(610, 500, "Export PDF Report")
    
    uc_settings = draw_usecase(500, 580, "Manage Sensory Profile")
    
    uc_diff = draw_usecase(420, 700, "Adjust Difficulty")
    uc_track = draw_usecase(580, 700, "Monitor Performance")

    # 4. Actor Relationships
    # Player
    draw.line((player[0], player[1], uc_home[0]-95, uc_home[1]), fill="black", width=2)
    draw.line((player[0], player[1], uc_play[0]-95, uc_play[1]), fill="black", width=2)
    
    # Parent
    draw.line((parent[0], parent[1], uc_analytics[0]+95, uc_analytics[1]), fill="black", width=2)
    draw.line((parent[0], parent[1], uc_settings[0]+95, uc_settings[1]), fill="black", width=2)
    
    # AI
    draw.line((ai[0], ai[1], uc_diff[0]+95, uc_diff[1]), fill="black", width=2)
    draw.line((ai[0], ai[1], uc_track[0]+95, uc_track[1]), fill="black", width=2)

    # 5. Internal Relationships (Include/Extend)
    
    # Choose -> Play (Include)
    draw_arrow((uc_home[0], uc_home[1]+25), (uc_play[0], uc_play[1]-25), "<<include>>", dashed=True)
    
    # Play -> Interact (Include)
    draw_arrow((uc_play[0]+95, uc_play[1]), (uc_interact[0]-95, uc_interact[1]), "<<include>>", dashed=True)
    
    # Play -> Reward (Include)
    draw_arrow((uc_play[0]+40, uc_play[1]+25), (uc_reward[0]-40, uc_reward[1]-25), "<<include>>", dashed=True)

    # View Analytics -> Export Report (Extend)
    draw_arrow((uc_export[0]-40, uc_export[1]-25), (uc_analytics[0]+40, uc_analytics[1]+25), "<<extend>>", dashed=True)

    # Play -> Adjust Difficulty (Extend - AI logic)
    draw_arrow((uc_diff[0], uc_diff[1]-25), (uc_play[0], uc_play[1]+25), "<<extend>>", dashed=True)

    # Play -> Track Metrics (Include)
    draw_arrow((uc_play[0]+20, uc_play[1]+25), (uc_track[0]-20, uc_track[1]-25), "<<include>>", dashed=True)

    # Save
    filename = "use_case_diagram_neuroquest.png"
    img.save(filename)
    print(f"Diagram updated successfully: {filename}")

if __name__ == '__main__':
    create_use_case_diagram()