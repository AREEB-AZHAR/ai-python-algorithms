import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

# --- 1. Define the Project Data (Based on your Modified Schedule) ---
# Format: (ID, Task Name, Start Date (YYYY-MM-DD), Duration (Days), Is_Milestone)
data = [
    (1, "Literature Review", "2025-11-11", 14, False),
    (2, "Requirement Gathering", "2025-11-25", 14, False),
    (3, "System Architecture", "2025-12-09", 21, False),
    (4, "UI/UX Wireframing", "2025-12-30", 21, False),
    (5, "Algorithm Logic Design", "2026-01-20", 14, False),
    (6, "FYP-1 Presentation", "2026-02-03", 0, True),  # Milestone
    (7, "Game Engine Setup", "2026-02-04", 7, False),
    (8, "Core Mechanics Dev", "2026-02-11", 21, False),
    (9, "Prototype Level 1", "2026-03-04", 14, False),
    (10, "Adaptive Algorithm Dev", "2026-03-18", 28, False),
    (11, "Data Analytics Integration", "2026-04-15", 14, False),
    (12, "Advanced Level Design", "2026-04-29", 21, False),
    (13, "Alpha & Beta Testing", "2026-05-20", 21, False),
    (14, "Final Polish & Doc", "2026-06-10", 14, False),
    (15, "Final Submission", "2026-06-24", 0, True)   # Milestone
]

# Create DataFrame
df = pd.DataFrame(data, columns=["ID", "Task Name", "Start", "Duration", "Milestone"])
df["Start"] = pd.to_datetime(df["Start"])
df["Finish"] = df.apply(lambda x: x["Start"] + timedelta(days=x["Duration"]), axis=1)

# Reverse order for plotting (top-down)
df = df.iloc[::-1].reset_index(drop=True)

# --- 2. Setup Plot Layout ---
# Increased width to 16 to prevent text overlap
fig, ax = plt.subplots(figsize=(16, 9))

# Split plot into two parts: Table (left) and Gantt (right)
ax.set_xlim(0, 1) 
ax.set_ylim(0, len(df) + 2) # Added extra space at top
ax.axis('off') 

# --- 3. Draw the Gantt Chart (Right Side) ---
# Shifted start to 0.5 (50% mark) to give table more space
ax_gantt = ax.inset_axes([0.5, 0, 0.5, 1]) 
ax_gantt.set_ylim(0, len(df) + 2)
ax_gantt.set_yticks([]) 

# Plot Bars and Milestones
for i, row in df.iterrows():
    y_pos = i + 0.5
    
    if row["Milestone"]:
        # Draw Diamond for Milestone
        ax_gantt.plot(row["Start"], y_pos, marker='D', color='black', markersize=8, zorder=10)
        # Add Date Label next to milestone
        ax_gantt.text(row["Start"] + timedelta(days=3), y_pos, 
                     row["Start"].strftime('%m/%d'), 
                     fontsize=9, va='center', fontweight='bold')
    else:
        # Draw Blue Bar
        duration_days = row["Duration"]
        ax_gantt.barh(y_pos, duration_days, left=row["Start"], height=0.5, 
                     color='#6fa8dc', edgecolor='#3d85c6', hatch='////') 

# Format Time Axis
ax_gantt.xaxis_date()
ax_gantt.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
ax_gantt.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax_gantt.grid(True, axis='x', linestyle='--', alpha=0.5)

# Add Top Axis for Timeline labels
ax_gantt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
ax_gantt.spines['left'].set_visible(True) 

# --- 4. Draw the Table (Left Side) ---
# Adjusted positions to fill the 0.0 to 0.5 space
# ID: 0.01, Task: 0.05, Start: 0.30, Finish: 0.40
header_y = len(df) + 0.5
font_size = 10

# Headers
plt.text(0.01, header_y, "ID", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(0.05, header_y, "Task Name", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(0.30, header_y, "Start", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(0.40, header_y, "Finish", fontsize=font_size, fontweight='bold', transform=ax.transData)

# Draw Separator Line under header
plt.plot([0, 0.49], [len(df), len(df)], color='black', linewidth=1, transform=ax.transData)

# Draw Table Rows
for i, row in df.iterrows():
    y_pos = i + 0.5
    
    # ID
    plt.text(0.01, y_pos, str(row["ID"]), fontsize=font_size, va='center', transform=ax.transData)
    
    # Task Name
    plt.text(0.05, y_pos, row["Task Name"], fontsize=font_size, va='center', transform=ax.transData)
    
    # Start Date
    start_str = row["Start"].strftime('%a %d/%m/%y')
    plt.text(0.30, y_pos, start_str, fontsize=font_size, va='center', transform=ax.transData)
    
    # Finish Date
    finish_str = row["Finish"].strftime('%a %d/%m/%y')
    plt.text(0.40, y_pos, finish_str, fontsize=font_size, va='center', transform=ax.transData)
    
    # Horizontal grid lines
    plt.plot([0, 0.99], [i, i], color='lightgray', linewidth=0.5, transform=ax.transData)

# Vertical Separator Line between Table and Gantt (moved to 0.49)
plt.plot([0.49, 0.49], [0, len(df)+2], color='black', linewidth=1, transform=ax.transData)

# --- 5. Save ---
plt.tight_layout()
# Adjusted margins
plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
filename = "ms_project_style_gantt.png"
plt.savefig(filename, dpi=300)

print(f"MS Project Style Chart saved as {filename}")